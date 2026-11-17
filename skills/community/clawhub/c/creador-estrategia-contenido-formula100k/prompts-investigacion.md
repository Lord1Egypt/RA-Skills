# Prompts de Investigación con MCPs

Stack en OpenClaw: Apify (cuentas públicas de IG/TikTok) + búsqueda web + vidIQ si está conectado + Supadata si hay llave. Los cuatro trabajan juntos, no se excluyen. Cada uno tiene zona donde nadie más entra.

---

## STACK PERMANENTE — REGLA DE ENTRADA

| # | Motor | Zona exclusiva | Cuándo entra |
|---|-------|----------------|--------------|
| 1 | **Apify** (`APIFY_TOKEN`) o capturas de la alumna | IG/TikTok públicos: captions verbatim, vistas, hashtags. Nunca navegador logueado | SIEMPRE que la alumna nombró 1+ cuenta referencia o el nicho es IG/TikTok |
| 2 | **Tavily MCP** | Web abierta, tendencias, artículos, validación cruzada | SIEMPRE para mapear tendencias + foros + Reddit + reportes |
| 3 | **vidIQ MCP** | YouTube outliers + transcripts + comentarios + keyword research | Cuando el nicho tiene actividad en YouTube (que es casi siempre) |
| 4 | **Supadata MCP** | Transcripts YouTube, landings sin login, blogs | Complemento. NO competir con Apify para IG/TikTok |

**Regla de oro:** si la alumna nombró cuentas de referencia, Apify entra primero (costo estimado y ✅). Si no hay `APIFY_TOKEN`, pídele links o capturas. Nunca se entra logueada a una red social desde el servidor.

---

## 1. AGENT-BROWSER (PRIMER MOTOR)

Solo si la alumna pasó 1+ cuenta IG/TikTok como referencia. Prompt reutilizable:

```
[Apify]

Corre con `APIFY_TOKEN` los actores públicos de Instagram y TikTok (perfil/reels y búsqueda). Solo datos públicos: nunca navegador logueado.

TAREA A — Para cada cuenta [@h1, @h2, @h3]:
  1. Visita instagram.com/[handle]/reels/
  2. Extrae los 9 reels más vistos: URL · caption completo · views · formato del primer frame (rostro/texto grande/split/B-roll).
  3. Si es TikTok, visita tiktok.com/@[handle] y haz lo mismo.

TAREA B — Búsquedas TikTok: [keyword1, keyword2]
  Para cada búsqueda: top 5 videos con URL · caption · handle · views.

TAREA C — Hashtags IG (opcional): [#hashtag1, #hashtag2]
  Top 9 posts por hashtag con caption + tipo (reel/carrusel/foto).

OUTPUT: markdown crudo, una sección por cuenta/búsqueda/hashtag. Sin análisis.
```

### Cómo procesar el output de Apify

Extrae para cada cuenta/búsqueda:
1. **Top 5-10 ganchos verbatim** (primera línea del caption o texto en pantalla)
2. **Formato dominante** del primer frame (rostro/texto/split/B-roll)
3. **Tipos de contenido** (reel/carrusel/foto) y frecuencia
4. **Cifras shock** (views, likes — si los muestra)

---

## 2. TAVILY MCP

Ejecuta 3 búsquedas en paralelo. Reemplaza `[NICHO]` y `[KEYWORDS]` con datos del bloque 3.

### Query 1 — Tendencias del nicho
```
mcp__tavily__tavily_search:
  query: "tendencias virales 2026 [NICHO] Instagram TikTok ganchos contenido reels"
  max_results: 10
  search_depth: "advanced"
```

### Query 2 — Preguntas frecuentes de la audiencia
```
mcp__tavily__tavily_search:
  query: "qué preguntas hace [AVATAR_DESCRIPTION] [NICHO] Reddit Quora foros"
  max_results: 8
```

### Query 3 — Competidores y referencias
```
mcp__tavily__tavily_search:
  query: "mejores creadores [NICHO] Instagram TikTok hispanos 2026 millones seguidores"
  max_results: 8
```

### Query 4 (opcional) — Investigación profunda
Si la alumna pidió análisis específico, usa `tavily_research`:
```
mcp__tavily__tavily_research:
  topic: "Análisis de contenido viral en [NICHO]: temas que más viralizan, ganchos comunes, formatos top, errores frecuentes"
  depth: "deep"
```

**Tavily auth:** si Tavily no está autenticado, `WebSearch` nativo sirve como respaldo equivalente.

---

## 3. VIDIQ MCP (YouTube outliers)

Si el nicho tiene presencia en YouTube (casi siempre):

```
mcp__vidiq__outlier_detection:
  keyword: "[NICHO_KEYWORD]"
```

Para los top 3 outliers:
- `mcp__vidiq__video_transcript` → identifica el "momento ajá" exacto
- `mcp__vidiq__video_comments` → mina el dolor real de la audiencia

Convierte cada outlier → 1 idea de reel/short con la tabla YouTube → Reel.

---

## 4. SUPADATA MCP (complemento)

Útil para:
- Transcripts de videos YouTube específicos (cuando vidIQ no aplica)
- Landings públicas sin login (sales pages de competencia)

NO usar para IG/TikTok perfil — ahí ya está Apify.

---

## 5. FALLBACKS HONESTOS

| Caso | Qué hacer |
|------|-----------|
| Sin `APIFY_TOKEN` | Decir explícito: "no tengo Apify conectado; trabajo con búsqueda web y los links o capturas que me mandes". Procede sin captions verbatim. |
| Tavily sin auth | Usa WebSearch nativo con queries equivalentes |
| vidIQ sin auth | Avisa: "para outliers YouTube reales necesito vidIQ autenticado — corre `/mcp`" |
| Supadata limit-exceeded | Sin impacto, Apify y Tavily ya cubren lo crítico |
| NINGÚN motor disponible | Avisa a la alumna. Genera estrategia basada solo en avatar + oferta. Recomienda correr `investigacion-contenido-formula100k` después. |

---

## 6. CÓMO INTEGRAR LA INVESTIGACIÓN EN EL OUTPUT

Después de ejecutar los motores, presenta a la alumna un resumen breve antes de generar las 20 ideas:

```
🔍 Investigación completada · [NICHO]

CUENTAS REFERENCIA ANALIZADAS (Apify):
- @[cuenta1] · top reel: "[caption]" · [N] views · formato: [X]
- @[cuenta2] · top reel: "[caption]" · [N] views · formato: [X]

TEMAS QUE MÁS VIRALIZAN (Tavily):
- [tema 1]
- [tema 2]
- [tema 3]

OUTLIERS YOUTUBE (vidIQ):
- "[título]" · [Nx] del promedio · momento ajá: "[frase]"

GANCHOS QUE SE REPITEN (cruce Apify + Tavily):
- "[gancho 1]"
- "[gancho 2]"

FORMATOS DOMINANTES:
- [formato 1] ([%])
- [formato 2] ([%])

Ahora genero tus 20 ideas integrando esta data...
```

Esto le da contexto a la alumna y muestra que la investigación fue real, no fabricada.

---

## 7. CÓMO USAR LOS DATOS PARA GENERAR IDEAS

Cada idea generada debe poder rastrearse a:
- Un dolor del avatar (bloque 1) o
- Un gancho verbatim cazado con Apify o
- Un tema viral encontrado en Tavily o
- Un outlier YouTube identificado en vidIQ o
- Un patrón de la competencia (cruce Apify + análisis)

**Ejemplo:**
> Idea: "El error que comete el 90% al guionizar reels"
> Rastreo: dolor "no sé qué decir" del avatar + gancho similar cazado con Apify en @[cuenta_ref] con [N] views + dato en Tavily ("90% de creadores fallan en el gancho")

NO inventes ideas que no tengan rastreo. Si una idea no se sustenta, descártala o márcala como ÁNGULO ORIGINAL.

---

## 8. LÍMITES DE INVESTIGACIÓN

- Tiempo total objetivo: 2-3 minutos (más con Apify, vale la pena)
- Apify por cuenta: ~30 segundos
- NO ejecutes más de 4 búsquedas Tavily por sesión (cuesta tokens)
- NO ejecutes más de 5 outliers de vidIQ en transcripts (costo)
- Si la alumna pasó >5 cuentas referencia, prioriza las 3 más relevantes para Apify
