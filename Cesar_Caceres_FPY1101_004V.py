import datetime
import json

# Datos de ejemplo
ventas = []

# Diccionario de precios según tipo y tamaño de pizza
precios_pizza = {
    "cuatro quesos": {"pequeña": 6000, "mediana": 9000, "familiar": 12000},
    "hawaiana": {"pequeña": 6000, "mediana": 9000, "familiar": 12000},
    "napolitana": {"pequeña": 5500, "mediana": 8500, "familiar": 11000},
    "peperoni": {"pequeña": 7000, "mediana": 10000, "familiar": 13000}
}

# Función para registrar una venta
def registrar_venta():
    nombre_cliente = input("Ingrese su nombre\n").strip()
    tipo_usuario = int(input("Ingrese el tipo de usuario: 1) Estudiante diurno - 2) Estudiante vespertino - 3) Administrativo\nSeleccione una opción\n"))
    ventas_cliente = []

    while True:
        tipo_pizza = input("Ingrese el tipo de pizza (Cuatro quesos - Hawaiana - Napolitana - Peperoni)\n").strip().lower()
        tamaño_pizza = input("Ingrese el tamaño de la pizza (Pequeña, Mediana, Familiar)\n").strip().lower()
        cantidad_pizza = int(input("Ingrese la cantidad de pizzas\n"))

        if tipo_pizza not in precios_pizza or tamaño_pizza not in precios_pizza[tipo_pizza]:
            print("Tipo o tamaño de pizza no válido. Intente de nuevo.")
            continue

        precio_base = precios_pizza[tipo_pizza][tamaño_pizza]
        descuento = 0
        
        if tipo_usuario == 1:
            descuento = 0.12
        elif tipo_usuario == 2:
            descuento = 0.14
        elif tipo_usuario == 3:
            descuento = 0.1

        total_sin_descuento = precio_base * cantidad_pizza
        total_con_descuento = total_sin_descuento * (1 - descuento)

        venta = {
            "nombre_cliente": nombre_cliente,
            "tipo_pizza": tipo_pizza,
            "tamaño_pizza": tamaño_pizza,
            "cantidad_pizza": cantidad_pizza,
            "precio_base": round(precio_base),
            "descuento": round(total_sin_descuento * descuento),
            "total_sin_descuento": round(total_sin_descuento),
            "total_con_descuento": round(total_con_descuento)
        }

        ventas_cliente.append(venta)
        print("Producto agregado con éxito!")

        # Preguntar al cliente si desea agregar otra pizza
        otra = input("¿Desea agregar otra pizza? (s/n)\n").strip().lower()
        if otra != 's':
            break

    # Calcular totales
    total_final_sin_descuento = sum(venta["total_sin_descuento"] for venta in ventas_cliente)
    total_final_con_descuento = sum(venta["total_con_descuento"] for venta in ventas_cliente)
    descuento_total = total_final_sin_descuento - total_final_con_descuento
    fecha_hora = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M:%S")

    ventas.append({
        "nombre_cliente": nombre_cliente,
        "tipo_usuario": tipo_usuario,
        "ventas": ventas_cliente,
        "total_final_sin_descuento": round(total_final_sin_descuento),
        "descuento_total": round(descuento_total),
        "total_final_con_descuento": round(total_final_con_descuento),
        "fecha_hora": fecha_hora
    })

    print("Venta registrada con éxito!")

# Función para mostrar todas las ventas
def mostrar_ventas():
    for venta in ventas:
        print(venta)

# Función para buscar ventas por nombre del cliente
def buscar_ventas_por_cliente():
    nombre_cliente = input("Ingrese el nombre del cliente para buscar sus ventas\n").strip().lower()
    ventas_cliente = [venta for venta in ventas if venta["nombre_cliente"].lower() == nombre_cliente]
    for venta in ventas_cliente:
        print(venta)

# Función para guardar las ventas en un archivo JSON
def guardar_ventas_en_archivo():
    with open("ventas.json", "w") as archivo:
        json.dump(ventas, archivo, indent=4)
    print("Ventas guardadas en ventas.json")

# Función para cargar las ventas desde un archivo JSON
def cargar_ventas_desde_archivo():
    global ventas
    try:
        with open("ventas.json", "r") as archivo:
            ventas = json.load(archivo)
        print("Ventas cargadas desde ventas.json")
    except FileNotFoundError:
        print("El archivo ventas.json no existe. No se han cargado ventas.")

# Función para generar una boleta
def generar_boleta(venta):
    print("\n--- BOLETA ---")
    print(f"Nombre del cliente: {venta['nombre_cliente']}")
    print(f"Fecha y hora: {venta['fecha_hora']}")
    tipo_usuario = ["Estudiante diurno", "Estudiante vespertino", "Administrativo"][venta["tipo_usuario"] - 1]
    print(f"Tipo de usuario: {tipo_usuario}")

    print("\n--- Detalles de la compra ---")
    for item in venta["ventas"]:
        print(f"- {item['cantidad_pizza']} x {item['tipo_pizza'].capitalize()} ({item['tamaño_pizza'].capitalize()}) - ${item['total_sin_descuento']}")
    
    print("\n--- Resumen de pagos ---")
    print(f"Precio original: ${venta['total_final_sin_descuento']}")
    print(f"Descuento total: ${venta['descuento_total']}")
    print(f"Total a pagar: ${venta['total_final_con_descuento']}")
    print("----------------\n")

# Función para el menú interactivo
def menu():
    while True:
        print("\nSistema de Ventas de Pizzas")
        print("1. Registrar una venta")
        print("2. Mostrar todas las ventas")
        print("3. Buscar ventas por cliente")
        print("4. Guardar las ventas en un archivo")
        print("5. Cargar las ventas desde un archivo")
        print("6. Imprimir boleta")
        print("7. Salir del programa")

        opción = int(input("Seleccione una opción\n"))

        if opción == 1:
            registrar_venta()
        elif opción == 2:
            mostrar_ventas()
        elif opción == 3:
            buscar_ventas_por_cliente()
        elif opción == 4:
            guardar_ventas_en_archivo()
        elif opción == 5:
            cargar_ventas_desde_archivo()
        elif opción == 6:
            nombre_cliente = input("Ingrese el nombre del cliente para imprimir la boleta: ").strip().lower()
            ventas_cliente = [venta for venta in ventas if venta["nombre_cliente"].lower() == nombre_cliente]
            if ventas_cliente:
                for venta in ventas_cliente:
                    generar_boleta(venta)
            else:
                print("No se encontraron ventas para este cliente.")
        elif opción == 7:
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Ejecutar el menú
menu()
