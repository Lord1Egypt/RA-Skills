---
name: analizador-referencias-virales-f100k
description: "Dado un keyword, busca los videos más virales en TikTok e Instagram (Apify), transcribe cada uno con Supadata, identifica el gancho verbal, textual y visual, y entrega una tabla lista para usar en calendarios, guiones o investigación. Usar cuando pidan 'busca referencias virales de [keyword]', 'qué está funcionando en TikTok/IG con [tema]', 'dame el gancho de estos virales', o cuando el calendarizador Modo D necesite enriquecer sus resultados. Soporta TikTok, Instagram Reels, o ambas plataformas en una sola corrida."
argument-hint: "[keyword(s) + plataforma — ej. \"colon irritable, SII | ambas\"]"
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - El motor es Apify con `APIFY_TOKEN`. Sin token: no hay métricas; pide los links y las capturas de vistas a la usuaria, o marca todo `[NO VERIFICADO — scrape no corrió]` como dice el PASO 4.5.
> - Transcripción: Supadata solo si existe `SUPADATA_API_KEY`. Si no, usa el campo de transcripción/subtítulos que devuelva el actor de Apify (`apify~instagram-reel-scraper` con `includeTranscript: true` para Reels); si tampoco hay, aplica el fallback `[sin transcripción]` del PASO 3.
> - Antes de lanzar los actores di el costo estimado de la tabla COSTOS y espera ✅. Corre las keywords una tras otra, no en paralelo.
> - Si una URL no la cubre Apify, se pide la captura: nunca navegador logueado. El archivo va a `informes/` y la tabla resumida al chat de Telegram.

---

## 🧭 ANCLAJE DE RUBRO (leer PRIMERO — manda sobre cualquier ejemplo de esta skill)

Esta skill enseña un **método**. El método es agnóstico de industria: sirve igual para
formulación cosmética, nutrición, repostería, fisioterapia, finanzas o jabonería.
Los ejemplos escritos aquí abajo son ilustraciones **del método**, nunca del tema.

**Antes de escribir nada:**

1. Identifica el **RUBRO real** de la persona (léelo de su Segundo Cerebro, de su perfil o
   pregúntaselo en una línea si no está claro). Decláralo: *"Rubro: ___"*.
2. Todos los ejemplos, analogías, comparaciones, objeciones, métricas y vocabulario salen
   de **ESE** rubro.
3. Si el rubro **no** es marketing, redes sociales, creación de contenido, ventas online o
   negocios digitales → queda **PROHIBIDO** el vocabulario de ese mundo (reels, algoritmo,
   embudo, lead magnet, engagement, "publicar sin vender", "clientes de alto ticket",
   "escalar tu negocio", "posicionarte como referente"), salvo que la persona lo escriba primero.
4. Si el rubro es **técnico, científico o de oficio**: NO borres el tecnicismo para
   "simplificar". Úsalo y **tradúcelo en su primera mención**. El término preciso ES la
   autoridad de esa creadora; quitarlo borra justo lo que la diferencia.
5. Si no tienes datos suficientes del negocio, dilo y usa marcadores explícitos
   (`[TU OFERTA]`, `[TU RESULTADO]`). **Nunca asumas que el rubro es marketing.**

**El método viaja, el rubro no.** El mismo molde, vestido con rubros distintos:

| Rubro | El mismo molde |
|---|---|
| Cocina | "Así es mi cena favorita para no dormir con el azúcar alta." |
| Relaciones | "5 señales de que estás forzando una relación que ya no funciona." |
| Finanzas | "La principal causa de un divorcio no es una infidelidad." |
| Formulación cosmética | "El conservante decide si tu crema dura tres meses o te da una infección. No el aceite." |
| Jabonería | "Si tu jabón se pone blando a los dos días, no fue el aceite. Fue la sosa." |
| Fisioterapia | "Ese dolor de rodilla al bajar escaleras casi nunca nace en la rodilla." |
| Repostería | "Tu bizcocho se hunde en el centro por la temperatura, no por la harina." |
| Jardinería | "Tu planta no se está muriendo de sed. Se está ahogando." |

Mismo molde en todos; ninguno menciona reels ni embudos. Haz exactamente eso.

---

# Skill: Analizador de Referencias Virales — Fórmula 100K

Convierte una keyword en una **tabla de referencias virales con guión transcrito y 3 tipos de gancho identificados**, lista para alimentar calendarios, guiones o estrategias de contenido.

**Cuándo invocar esta skill:**
- "Busca referencias virales de [keyword]"
- "¿Qué está funcionando en TikTok/IG con [tema]?"
- "Dame el gancho de estos videos"
- Cuando el **calendarizador Modo D** necesita enriquecer sus resultados
- Cuando **investigacion-contenido** necesita validar viralidad real en video

---

## LOS 3 GANCHOS QUE SE ANALIZAN

| Tipo | Qué es | Fuente |
|------|--------|--------|
| **Gancho verbal** | Primeras 3-10 palabras HABLADAS del video | Transcript de Supadata |
| **Gancho textual** | Texto visible en pantalla en los primeros 3 segundos | Caption de Apify + contexto del transcript |
| **Gancho visual** | Qué se VE en el primer frame (acción, objeto, situación) | Inferido del transcript + descripción del video |

> El gancho visual siempre se marca como `[inferido]` — es una aproximación de alta precisión, no una certeza. Para validación exacta, abrir la URL y ver el primer frame.

---

## PASO 0 — Entender el input

Detectar automáticamente:

| Campo | Señal | Default |
|-------|-------|---------|
| Keywords | Palabras/frases separadas por coma | — obligatorio |
| Plataforma | "TikTok", "IG", "Instagram", "ambas" | Ambas |
| Nicho / avatar | Contexto adicional de la audiencia | Opcional |
| Cantidad de refs | Número pedido por el usuario | 7 (un slot por día de calendario) |
| Modo de llamada | ¿Viene del calendarizador (Modo D) o es standalone? | Standalone |

Si las keywords no están claras, preguntar antes de buscar.

### MODO URLs DIRECTAS (cuando el usuario ya trae los videos)

Si el input contiene **URLs específicas** de TikTok/IG (el usuario ya cazó las referencias, o vienen de un brief) → **NO busques por keyword.** Buscar por keyword traería videos DISTINTOS a los que pidió y perderías sus métricas reales.

En su lugar:
1. Un **slot de salida por cada URL entregada** (no las mezcles con búsqueda por keyword salvo que el usuario lo pida).
2. Para cada URL, extraer las métricas reales de ESE video:
   - **TikTok:** `clockworks~tiktok-scraper` con `{ "postURLs": ["<url>"] }` (NO `searchQueries`).
   - **Instagram:** `apify~instagram-scraper` con `{ "directUrls": ["<url>"], "resultsType": "posts" }`.
   - Si Apify no cubre la URL: pídele a la usuaria la captura con las vistas (nunca navegador logueado).
3. Leer `playCount`/`videoPlayCount` de la respuesta = las views reales de ese video.
4. Si el scrape de una URL falla → esa fila va `[NO VERIFICADO — scrape falló]`, nunca inventes su métrica (ver Compuerta de Verificación).

---

## PASO 1 — Buscar videos virales con Apify

### 1A — TikTok (si plataforma = TikTok o Ambas)

Usar `fetch-actor-details` primero para verificar el schema, luego `call-actor`:
- **Actor:** `clockworks~tiktok-scraper`
- **waitSecs:** 45

```json
{
  "searchQueries": ["<keyword>"],
  "resultsPerPage": 20,
  "shouldDownloadVideos": false,
  "shouldDownloadCovers": false
}
```

Lanzar **1 corrida por keyword en paralelo** si hay múltiples keywords.

**Campos clave del resultado:**
- `webVideoUrl` → URL del video
- `playCount` → vistas
- `text` → caption
- `authorMeta.name` → @handle
- `videoMeta.duration` → duración en segundos

### 1B — Instagram (si plataforma = IG o Ambas)

Instagram no tiene búsqueda directa por keyword → **convertir keywords a hashtags**:

```
"colon irritable"      → #colonirritablee, #intestinoirritablee
"emprendedora digital" → #emprendedoradigital, #negocioonline
"mentalidad"           → #mentalidadganadora, #mindset
```

Regla: eliminar espacios + quitar tildes + probar 2 variantes de hashtag por keyword.

- **Actor:** `apify~instagram-scraper`
- **waitSecs:** 45

```json
{
  "directUrls": ["https://www.instagram.com/explore/tags/<hashtag>/"],
  "resultsType": "posts",
  "resultsLimit": 20
}
```

Lanzar **en paralelo con TikTok** si ambas plataformas fueron pedidas.

**Campos clave del resultado:**
- `url` o `shortCode` → URL del reel
- `videoPlayCount` o `likesCount` → proxy de viralidad
- `caption` → texto del post
- `ownerUsername` → @handle
- `videoDuration` → duración

---

## PASO 2 — Filtrar por viralidad real

1. Ordenar por `playCount` / `videoPlayCount` descendente
2. Aplicar umbral:
   - ≥100K → ✅ viral confirmado
   - 50K-100K → ✅ aceptable
   - 20K-50K → ⚠️ nicho chico (mencionar al usuario)
   - <20K → ❌ no incluir
3. Seleccionar top N (default 7), mezclando TikTok + IG si ambas plataformas
4. Si <7 refs pasan el umbral → bajar un nivel y avisar
5. Máximo 2 videos del mismo @handle (diversidad de creadores)

---

## PASO 3 — Transcribir con Supadata

Para cada URL del top N, transcribir con el **MCP de Supadata disponible en la sesión**. El nombre exacto del tool cambia según el entorno (histórico había un typo `supadara`) → **localízalo con `ToolSearch("supadata transcript")` antes de llamarlo**, no lo hardcodees. El patrón es:

```
transcript: { "url": "<url_del_video>" }   → devuelve un id
check status: { "id": "<transcript_id>" }  → poll hasta READY
```

Reintentar hasta 3 veces con 5 segundos entre intentos.

**Fallback si Supadata falla:**
- Marcar gancho verbal como `[sin transcripción]`
- Usar caption de Apify como proxy del gancho textual
- Inferir gancho visual desde el caption y nicho
- No omitir el video — igual es referencia válida por views

---

## PASO 4 — Analizar los 3 ganchos

### Gancho verbal
- Primeras 3-10 palabras habladas del transcript (sin artículos innecesarios al inicio)
- Ejemplo → Transcript: "Si tienes el síndrome de intestino irritable y llevas años..." → Gancho: `"Si tienes intestino irritable"`
- ¿Empieza con pregunta / condicional "si" / número / negación / nombre del problema?

### Gancho textual
- Primera oración del caption (que suele ser el texto on-screen)
- Señal: si el caption empieza con mayúsculas o tiene estructura de titular → es el texto del video
- Ejemplo → Caption: `"El error que nadie te dice sobre el SII 👇"` → Gancho textual: `"El error que nadie te dice sobre el SII"`

### Gancho visual
- Inferido del contexto del transcript + duración + nicho
- Patrones por nicho:
  - Nutrición / salud: "Creadora sosteniendo alimento / mostrando plato / señalando texto"
  - Negocios / emprendimiento: "Pantalla con números / captura de resultados / texto animado"
  - Fitness: "Demostración de ejercicio / antes-después"
  - Educativo: "Texto en pizarra / lista apareciendo / creadora apuntando a pantalla"
- Siempre agregar `[inferido]` al final

### Detección de formato implícito (para uso en calendarizador)
- Caption con lista numerada + duración >45s → `Pizarra / Valor`
- Caption con "si tienes/sientes" + duración 15-30s → `POV / Viral`
- Caption con testimonio/caso + duración >60s → `Testimonio / Venta`
- Caption con tutorial + duración >60s → `Tutorial / Valor`
- Caption corto + duración <20s → `Sketch / Viral`

---

## PASO 4.5 — COMPUERTA DE VERIFICACIÓN (bloqueante — leer antes del output)

**Esta es la regla que evita entregar data inventada. Es obligatoria y bloquea el output.**

Cada métrica que salga en el output (views, likes, cualquier número) DEBE provenir de un **campo devuelto por el scraper en ESTA corrida** (`playCount` / `videoPlayCount` de Apify, o una captura que mandó la usuaria). Antes de escribir la tabla, verifica:

- ✅ ¿El actor de Apify **realmente corrió** en esta sesión (tienes un `runId`/`datasetId` real) o la usuaria mandó la captura con el dato? → puedes emitir el número.
- 🚩 ¿El actor **no corrió**, devolvió 0 resultados, falló auth, o el MCP no estaba conectado? → **PROHIBIDO emitir cualquier métrica.** Marca cada fila afectada `[NO VERIFICADO — scrape no corrió]` y **DETENTE** para avisar al usuario:
  > "⚠️ La herramienta de scraping no corrió (Apify sin conexión, sin saldo o sin `APIFY_TOKEN`). No puedo darte métricas reales. Arregla la conexión/sesión y reintento — no voy a rellenar números de memoria."

Reglas duras:
- **NUNCA uses followers ni 'likes acumulados' del perfil como sustituto de las views del video.** Son datos de perfil, no de rendimiento del reel; que aparezcan en vez de views es el síntoma #1 de que el scrape no corrió.
- **Fallo de herramienta ≠ nicho sin viralidad.** Distínguelos explícitamente: "la herramienta falló" es un problema de conexión; "el nicho no tiene virales" es un hallazgo real con el scraper corriendo. No los confundas en el reporte.
- Si dudas de si un número es real, trátalo como NO verificado. Es mejor un `[NO VERIFICADO]` honesto que una métrica bonita inventada.

---

## PASO 5 — Output

### Tabla en chat

```markdown
## 📊 Referencias Virales — [Keyword] · [Plataforma] · [Fecha]

| # | Red | @Handle | Views | Gancho verbal | Gancho textual | Gancho visual | URL |
|---|-----|---------|-------|---------------|----------------|---------------|-----|
| 1 | TT  | @handle | 230K  | "Si tienes intestino irritable" | "El error que nadie te dice" | Mujer sosteniendo tazón, mirando a cámara [inferido] | [ver](url) |
```

Debajo de la tabla:
- 📌 **N refs encontradas** — X de TikTok, Y de Instagram
- 📊 **Rango de views:** [min]K - [max]K
- 💡 **Patrón dominante de gancho verbal:** (ej. "70% usan condicional 'Si tienes/sientes'")
- ⚠️ URLs que no pudieron transcribirse (si aplica)

### Guardado en `informes/` (siempre, aunque el usuario no lo pida)

```
informes/refs-virales-[keyword-slug]-[YYYY-MM-DD].md
```

Formato del archivo:

```markdown
---
keyword: [keyword]
fecha: [YYYY-MM-DD]
plataforma: TikTok / IG / Ambas
total_refs: [N]
---

# Referencias Virales — [Keyword]
> Generado por `analizador-referencias-virales-f100k` · [fecha]

[tabla completa sin truncar]

## Patrón dominante de gancho verbal
[insight]

## Para usar
- En calendario: pega las URLs en calendarizador Modo C, o pásalas al Modo D como refs ya analizadas
- En guión: usa el gancho verbal como punto de partida para tu hook
```

### Cuando es llamada desde el calendarizador Modo D

Devolver los datos estructurados para mapeo inmediato:

```
Para cada ref: {
  url, views, handle, plataforma,
  gancho_verbal, gancho_textual, gancho_visual,
  transcript_extracto,
  formato_inferido   ← el calendarizador usa esto para asignar slots
}
```

---

## INTEGRACIÓN CON OTRAS SKILLS

| Skill que la invoca | Cuándo | Qué recibe |
|---------------------|--------|------------|
| `calendarizador-contenido-formula100k` Modo D | Después de extraer keywords del brief | Refs enriquecidas para mapear a slots del calendario |
| `investigacion-contenido-formula100k` | Para validar viralidad real de un tema | Refs con gancho identificado para la investigación |
| Standalone | Cuando se pide "analiza virales de X" directamente | Tabla completa en chat + guardado en `informes/` |

---

## COSTOS ESTIMADOS

| Componente | Costo aprox |
|------------|-------------|
| Apify TikTok (4-6 keywords × 20 posts) | $0.40-$0.60 |
| Apify Instagram (4-6 hashtags × 20 posts) | $0.40-$0.60 |
| Supadata transcripciones (7 videos) | Free tier cubre ~50/mes |
| **Total por sesión** | **~$0.80-$1.20** |

---

## REGLAS Y GUARDARRAÍLES

- ❌ NUNCA inventar URLs o métricas (ver **PASO 4.5 — Compuerta de Verificación**, es bloqueante). Si el scraper CORRIÓ y devolvió 0 resultados → reportar que el nicho no tiene viralidad medible con esa keyword. Si el scraper NO corrió (sin auth/sesión) → decirlo explícitamente y NO emitir números; son cosas distintas.
- ❌ NUNCA usar followers/likes-de-perfil como sustituto de las views del video. Si solo tienes datos de perfil, el scrape del video no corrió.
- ✅ Si el usuario entrega URLs específicas → usar el **MODO URLs DIRECTAS** del PASO 0 (no buscar por keyword).
- ❌ NUNCA omitir `[inferido]` en el gancho visual.
- ✅ Mezclar TikTok + IG siempre que sea posible.
- ✅ Máximo 2 videos del mismo @handle en la tabla.
- ✅ Si los resultados son en inglés, mencionar que la keyword tiene más tracción en inglés y sugerir alternativas en español.
- ✅ Guardar siempre en `informes/`.
- ✅ Si el nicho es muy específico (<20K views en todos los resultados), bajar el umbral y avisar — no inventar contenido.
