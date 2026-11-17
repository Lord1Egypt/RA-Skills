# Auditoría profunda con Apify (modo opcional)

> Proceso para extraer N reels de un perfil de Instagram + transcripciones de audio del top por engagement, sin depender de browser logueado. Útil cuando agent-browser falla por detección CDP de Instagram o cuando se necesita escala (60+ reels en menos de 2 minutos).

## Cuándo usar este modo

Activar SOLO si el usuario respondió "sí" a la pregunta del PASO 1: **"¿Quieres una evaluación profunda con descarga de reels y transcripciones de audio? (usa Apify, costo ~$3-5 por análisis)"**.

Por default NO se ejecuta. La skill sigue usando agent-browser + Supadata para análisis ligero. Apify es ADICIONAL, no reemplazo:

| Necesidad | Motor |
|---|---|
| Métricas de Insights (retención, alcance no-seguidores, guardados) | agent-browser logueado (única opción) |
| Caption + comments count + views públicas de muchos reels | **Apify (más rápido y confiable)** |
| Transcripción de audio palabra por palabra | **Apify `includeTranscript: true`** |
| Comentarios completos de un video específico | agent-browser |
| Transcript suelto de un video aislado | Supadata |

## Costo aproximado

`apify~instagram-reel-scraper` cobra por evento:
- $0.0026 por reel (metadata)
- $0.001 por arranque del actor
- $0.048 por minuto de audio transcrito (solo si `includeTranscript: true`)

**Auditoría típica (60 reels metadata + transcripción del top 5):**
- 60 × $0.0026 = $0.156
- 2 arranques = $0.002
- ~5 minutos de audio × $0.048 = $0.24
- **Total ≈ $0.40-0.60 por auditoría** (más barato de lo que parece)

Para 100+ reels con transcript de top 10, sube a ~$2-3.

## Proceso de 2 pasadas

### Pasada 1 — Metadata masiva (barato)

Llamar al actor con N reels SIN transcript para tener el ranking por comentarios:

```json
{
  "username": ["nombre_de_usuario_sin_arroba"],
  "resultsLimit": 60,
  "skipPinnedPosts": false
}
```

Tool: `mcp__apify__call-actor` con `actor: "apify~instagram-reel-scraper"`.

Esperar a que termine (típico: 30-90 segundos para 60 reels). Luego `mcp__apify__get-dataset-items` con campos:

```
shortCode, url, commentsCount, likesCount, videoViewCount, videoPlayCount, caption, timestamp, videoDuration, isPinned, firstComment
```

**Ordenar el resultado por `commentsCount` descendente** y extraer las URLs del top 5 (o top N según pidió el usuario).

### Pasada 2 — Transcripciones del top (caro pero focalizado)

Llamar al mismo actor pasando las URLs específicas del top + `includeTranscript: true`:

```json
{
  "username": [
    "https://www.instagram.com/p/SHORTCODE1/",
    "https://www.instagram.com/p/SHORTCODE2/",
    "https://www.instagram.com/p/SHORTCODE3/",
    "https://www.instagram.com/p/SHORTCODE4/",
    "https://www.instagram.com/p/SHORTCODE5/"
  ],
  "includeTranscript": true
}
```

El actor devuelve para cada reel: `transcript` (string con el audio), `caption`, `commentsCount`, `videoDuration`, etc.

Tarda 10-20 segundos para 5 reels.

### Gotcha conocido

- El transcriber automático **confunde "Claude" con "Cloud" / "Clouds"**. Corregir manualmente en el reporte final cuando el perfil sea del usuario o cualquier persona que hable de Claude/IA.
- Si el actor no encuentra `videoViewCount` para un reel reciente (<24h), usar `videoPlayCount` como proxy (suele ser 3-4x más alto que views).
- `isPinned: true` puede inflar el `commentsCount` artificialmente (un reel pinned acumula durante meses). Marcar en el reporte si entró al top por estar pinned.

## Qué extraer del resultado para el reporte

Para cada reel del top:

1. **URL** (`https://www.instagram.com/p/{shortCode}/`)
2. **Métricas**: comentarios, likes, vistas, fecha
3. **Caption verbatim** (sin reformatear, con saltos de línea originales)
4. **Transcripción limpia** (corregir Claude/Cloud si aplica)
5. **CTA identificado**: la frase exacta del cierre que pide acción
6. **Palabra-llave del CTA**: la palabra clave que pide en comentarios
7. **Gancho del primer segundo**: descripción breve (verbal vs visual)

## Análisis de patrones de CTA

Después de extraer los reels, cruzar todos los CTAs contra esta tabla (ver también [[feedback-ctas-guiones]] en memoria):

| Patrón | Pregunta a responder |
|---|---|
| Palabra del CTA 1-2 sílabas | ¿Es corta? |
| Priming triple (caption + voz + hashtag) | ¿Cuántas veces aparece la palabra antes del CTA? |
| Recurso tangible invisible | ¿Promete algo concreto que NO está en bio? |
| Vacío de información | ¿Educa la mitad y retiene la mitad? |
| Topic de dolor caro | ¿El tema toca pérdida de tiempo/dinero/oportunidad? |
| Anula objeción de precio | ¿Dice "gratis" / "sin pagar nada extra"? |

Los CTAs que cumplen 4+ patrones son los reproducibles. Los que cumplen 1-2 patrones son outliers (ganaron por suerte o por gancho excepcional, no por CTA).

## Output del modo profundo

Además del reporte estándar del PASO 6, añadir una sección:

```markdown
## Auditoría profunda · Top N CTAs ganadores

### Ranking
[tabla con N filas: shortcode, comentarios, palabra-CTA, fecha]

### Por reel
[bloque por reel con: caption, transcripción, gancho, CTA, "por qué funcionó" con bullets atados a los 6 patrones]

### Patrones que se repiten
[tabla cruzada CTA-vs-patrones]

### Fórmula a replicar para próximos guiones
[2-4 reglas accionables basadas en lo que se repitió]
```

## Cuándo NO usar este modo

- Auditorías express ("dame 3 cosas a mejorar ya") → agent-browser solo
- Perfiles con menos de 15 reels → no hay muestra suficiente para extraer patrones
- Cuentas privadas → Apify no entra a contenido privado
- Cuando el objetivo es analizar **historias**, no reels → usar agent-browser
- Cuando el usuario quiere analizar el algoritmo desde insights propios → agent-browser (única vía a Insights)
