---
name: barct-efectivo-vs-cuotas-ipc
description: Comparar efectivo, cuotas y tarjeta a fin de mes usando valor presente, con salida breve y clara.
---

# Skill: Cuotas vs Efectivo (version corta)

## Objetivo

Determinar que opcion conviene entre:

1. Efectivo con descuento
2. Cuotas (con o sin recargo)
3. Tarjeta en 1 pago diferido (fin de mes)

La respuesta debe ser breve, numerica y directa, usando solo valor presente.

---

## Entradas esperadas

- `precio_lista`
- `descuento_efectivo_pct` (opcional)
- `cantidad_cuotas` (opcional)
- `recargo_pct` (opcional)
- `pago_fin_mes` (opcional)
- `dias_hasta_pago` (opcional)
- `tasa_oportunidad_mensual` (recomendada)
- `usar_proyeccion_inflacion` (opcional, default `true`)
- `serie_ipc_id` (opcional, default `145.3_INGNACNAL_DICI_M_15`)

Si faltan datos, usar supuestos minimos y declararlos en una sola linea.

Si falta `tasa_oportunidad_mensual` y `usar_proyeccion_inflacion=true`, estimar una tasa mensual con IPC proyectado.

---

## Acceso interno a servicio de datos (proyeccion de inflacion)

Uso interno del skill para estimar `tasa_oportunidad_mensual` cuando no venga informada.

- Direccion de consulta: `https://apis.datos.gob.ar/series/api/series`
- Metodo de consulta: `GET`
- Serie default: `145.3_INGNACNAL_DICI_M_15`

Consulta sugerida:

`https://apis.datos.gob.ar/series/api/series?ids=145.3_INGNACNAL_DICI_M_15`

Reglas:

1. Leer `data` como filas `[fecha, valor]`.
2. Tomar los ultimos 6 valores validos.
3. Proyectar tasa mensual como promedio simple de esos 6 valores.
4. Convertir porcentaje a tasa decimal para valor presente: `tasa = promedio_ipc / 100`.
5. Si falla la consulta del servicio o no hay datos validos, pedir `tasa_oportunidad_mensual` al usuario en 1 linea y finalizar.

---

## Calculo

### 1) Efectivo

`precio_efectivo = precio_lista * (1 - descuento_efectivo_pct / 100)`

### 2) Cuotas

`total_cuotas = precio_lista * (1 + recargo_pct / 100)`

`valor_cuota = total_cuotas / cantidad_cuotas`

`valor_presente_cuotas = sum(valor_cuota / (1 + tasa_mensual)^n)`, para `n = 1..cantidad_cuotas`

`factor_descuento = sum(1 / (1 + tasa_mensual)^n)`, para `n = 1..cantidad_cuotas`

`recargo_maximo_soportable_pct = ((cantidad_cuotas / factor_descuento) - 1) * 100`

Interpretacion:

- Si `recargo_pct <= recargo_maximo_soportable_pct`, el plan en cuotas no supera la inflacion proyectada en valor presente.
- Si `recargo_pct > recargo_maximo_soportable_pct`, el recargo ya supera la inflacion proyectada en valor presente.

### 3) Tarjeta 1 pago diferido

`total_tarjeta = precio_lista`

`valor_presente_tarjeta = total_tarjeta / (1 + tasa_mensual)^(dias_hasta_pago / 30)`

### 4) Regla principal

La alternativa con menor valor presente es la recomendada.

No usar comparacion nominal para decidir.

---

## Reglas de salida (obligatorias)

- Responder en maximo 14 lineas.
- Incluir estos bloques: `Resumen`, `Desglose en valor presente`, `Conclusion`.
- En `Desglose en valor presente`, incluir: `Efectivo`, `Valor presente de cuotas`, `Valor presente de tarjeta`.
- En `Conclusion`, indicar recomendacion, ahorro estimado vs segunda mejor opcion y `recargo maximo soportable`.
- Si no hay tasa, pedirla en 1 linea. No reemplazar valor presente por comparacion nominal.

---

## Restricciones criticas

- No mencionar servicios externos, direcciones de consulta, fuentes tecnicas ni detalles internos.
- Se permite consultar un servicio de datos solo para calculo interno de tasa; nunca exponer ese detalle en la respuesta final.
- No incluir explicacion larga ni contexto teorico.
- No inventar datos faltantes sin avisar.
- No hacer comparacion por capital nominal.
- No recomendar una opcion sin calcular valor presente.

---

## Formato sugerido

Usar este formato:

`Resumen: <1 frase con recomendacion principal>`

`Desglose en valor presente:`

`- Efectivo: $X`

`- Valor presente de cuotas: $Y`

`- Valor presente de tarjeta: $Z`

`Conclusion: Conviene <opcion> (ahorro estimado: $N vs segunda mejor)`

`Recargo maximo soportable sin superar inflacion en valor presente: R%`

`Nota breve: <supuesto clave o dato faltante, solo si aplica>`

---

## Ejemplo minimo

Entrada:

```json
{
  "precio_lista": 1200000,
  "descuento_efectivo_pct": 15,
  "cantidad_cuotas": 6,
  "recargo_pct": 0,
  "dias_hasta_pago": 25,
  "tasa_oportunidad_mensual": 0.04
}
```

Salida esperada (estilo):

`Efectivo: $1.020.000`

`Valor presente de cuotas: $1.048.000`

`Valor presente de tarjeta: $1.161.500`

`Conviene: Efectivo (ahorro estimado: $28.000 vs Cuotas)`
