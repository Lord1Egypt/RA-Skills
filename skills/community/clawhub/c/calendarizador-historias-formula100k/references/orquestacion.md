# ORQUESTACIÓN — Cómo coordinar las llamadas a Skill A

Esta skill (calendarizador) NO genera guiones por sí misma. Cada slot del calendario lo desarrolla
invocando `guionizacion-historias-formula100k` (Skill A).

---

## CÓMO INVOCAR SKILL A DESDE ESTA SKILL

Cuando estés en el flujo del calendarizador y necesites un guion para un slot:

1. **Construir el contexto** del slot:
   ```
   Categoría: [del slot]
   Idea: [asignada o autogenerada]
   Oferta: [si aplica]
   Día y hora: [del calendario]
   Posición en la semana: [día N de M]
   Coherencia narrativa: [resumen de qué se publicó antes y qué viene después]
   ```

2. **Invocar Skill A** con el contexto:

   Usando la herramienta Skill (interna):
   ```
   Skill(skill="guionizacion-historias-formula100k", args="<contexto>")
   ```

3. **Esperar** a que Skill A devuelva el path del .md generado.

4. **Guardar** ese path en la fila correspondiente del calendario maestro.

---

## ORDEN DE GENERACIÓN

Generar los slots del calendario en el siguiente orden (no en orden cronológico):

1. **Primero los slots de URGENCIA** — son los que más coherencia interna necesitan (escalada de presión).
2. **Después los slots ANCLA** del lanzamiento — anuncio principal, caso de éxito principal.
3. **Después los LEAD MAGNETS** — necesitan ofrecer algo distinto que los anuncios.
4. **Por último los slots LIBRES y ENCUESTAS** — los más flexibles.

Esto garantiza que el "esqueleto" del calendario quede cohesionado antes de rellenar los slots blandos.

---

## EVITAR DUPLICACIÓN DE PALABRAS CLAVE

Cada secuencia tiene una palabra clave de CTA (GPT, INFO, CASO, etc.). NO se pueden repetir
dentro del mismo día (rompe el sistema de DM automatizados del usuario).

Reglas:
- En **el mismo día**: nunca repetir palabra clave.
- En la **misma semana**: máximo 2 secuencias con la misma palabra clave (en días distintos).
- En el **mismo lanzamiento**: si una palabra es muy fuerte (ej. "GPT"), reservarla para el día más importante.

Mantén un set de palabras usadas en la sesión:

```python
palabras_usadas_hoy = set()
palabras_usadas_semana = {}  # palabra: count

for slot in calendario:
    palabras_usadas_hoy = set()  # reset al inicio de cada día
    for secuencia_del_dia in slots_del_dia:
        # Cuando recibas el guion de Skill A, validar:
        if secuencia.palabra_clave_cta in palabras_usadas_hoy:
            # Pedir a Skill A que use otra palabra
            regenerar_con_palabra_distinta(...)
        palabras_usadas_hoy.add(secuencia.palabra_clave_cta)
        palabras_usadas_semana[palabra] = palabras_usadas_semana.get(palabra, 0) + 1
```

---

## EVITAR DUPLICACIÓN DE ESTRUCTURAS

Si una semana tiene 14 secuencias y todas usan la #14 Mini Documental, se vuelve aburrida.

Regla: **máximo 3 secuencias con la misma estructura por semana**.

Si Skill A devuelve la 4ta del mismo tipo, regenerar pidiendo otra estructura.

---

## EVITAR DUPLICACIÓN DE ESCENARIOS

Si todas las fotos vienen del mismo escenario (todas en Japón), pierden frescura.

Regla: **idealmente 3-4 escenarios distintos por semana**.

Cuando construyas el contexto para Skill A, sugerir variar:
- Lunes: escenario A (escritorio)
- Martes: escenario B (calle/café)
- Miércoles: escenario A
- Jueves: escenario C (viaje)
- Viernes: escenario B
- Sábado: escenario D (lifestyle weekend)
- Domingo: escenario A

---

## CONSOLIDACIÓN DE PRODUCCIÓN

Después de generar todos los guiones, extrae de cada uno la sección **"Sesiones de grabación recomendadas"**
(que Skill A pone en cada .md) y CONSOLIDA en una sola lista en el calendario maestro:

```
SESIONES CONSOLIDADAS DE PRODUCCIÓN — SEMANA [X]

Sesión 1: ESCRITORIO
- Día/hora: domingo previo a la semana
- Clips a grabar: [lista]
- Para slides: [secuencia 1 slide 1, secuencia 5 slide 2, ...]
- Outfit sugerido: [...]

Sesión 2: VIAJE/EXTERIOR
- Día/hora: el sábado
- Clips a grabar: [lista]
- Para slides: [...]
- Outfit sugerido: [...]
```

Esto le ahorra al usuario tiempo: una sola sesión de grabación para 5-6 clips en vez de grabar a diario.

---

## OUTPUT XLSX

Para generar el .xlsx, usa Python con `openpyxl` o `pandas`. Estructura:

**Hoja 1: "Calendario"**
| A: Día | B: Hora | C: Categoría | D: Estructura | E: Idea | F: CTA | G: Slides | H: Guion |

**Hoja 2: "Producción Consolidada"**
Tabla con sesiones, clips, capturas necesarias.

**Hoja 3: "Resumen"**
Métricas: total secuencias, distribución por categoría (gráfico de torta opcional), palabras clave usadas.

Si Python/openpyxl no están disponibles:
- Generar como .csv (Excel los abre nativo)
- Avisar al usuario que el formato cae a CSV

---

## EJEMPLO DE FLUJO COMPLETO

**Input del usuario:**
> "Calendariza la semana del 6 al 12 de mayo. Modo lanzamiento. Vendo el GPT del primer segundo + Banco de Historias. Tengo estas ideas:
> 1. Caso de éxito de Brenda
> 2. Demo del GPT
> 3. Anunciar el banco
> 4. Subida de precio el viernes"

**Pasos del calendarizador:**

1. Cargar modo Lanzamiento (14 slots Lun-Dom)
2. Asignar las 4 ideas del usuario a slots compatibles:
   - Caso Brenda → Jueves (Caso) o Miércoles (One-Shot caso)
   - Demo del GPT → Martes (One-Shot Anuncio)
   - Anunciar el banco → Miércoles (Lead Magnet) o Lunes (preview)
   - Subida de precio → Viernes (Urgencia)
3. Autogenerar las 10 ideas faltantes:
   - Lunes 10am Encuestas: "¿Cuánto gana tu primera historia? A) 0-100 B) 100-1K C) 1K+"
   - Lunes 6pm Libre: "Por qué hoy estoy nerviosa"
   - ... etc
4. Llamar Skill A 14 veces (1 por slot), guardando cada path
5. Validar duplicación de palabras clave y estructuras
6. Generar consolidación de producción
7. Escribir .md maestro + .xlsx
8. Mostrar resumen al usuario
