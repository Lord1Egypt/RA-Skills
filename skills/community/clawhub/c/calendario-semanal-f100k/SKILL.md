---
name: calendario-semanal-f100k
description: "Módulo del Autopilot F100K que corre cada lunes: caza 7 virales de la semana anterior en TikTok para el nicho del usuario, genera un calendario completo de 7 días con guiones listos usando los frameworks de guionizacion-formula100k, exporta CSV + XLSX, y envía el digest por email. Usar cuando alguien diga: \"arma mi calendario de esta semana automáticamente\", \"genera mi calendario semanal\", \"ejecutar módulo calendario\", \"quiero mi semana lista\", o cuando el schedule automático lo invoque los lunes. Requiere config en cerebro/f100k-config.json."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Config en `cerebro/f100k-config.json` (si falta, créala desde `USER.md`).
> - Los 7 slots se alimentan primero de `ideas/aprobadas.md`, `ideas/banco.md` y `informes/`; Apify TikTok solo suma referencias si hay `APIFY_TOKEN`.
> - Guarda en `guiones/calendarios/`. El «Paso 6 — Gmail» se reemplaza por un mensaje de Telegram con la tabla y el archivo completo como documento.
> - Eventos en Google Calendar solo vía Composio y solo después del ✅ de la usuaria.

---

# Skill: Calendario Semanal — Autopilot F100K

Cada lunes por la mañana, este módulo caza los virales de la semana pasada en tu nicho, arma un calendario de 7 días completo con guiones listos y referencias reales, y te lo manda por email con el archivo listo para copiar a tu planner.

---

## FASE 1 — CARGAR CONFIG

```bash
cat cerebro/f100k-config.json
```

Si no existe → detener e instruir:
> "Corre `/rutina-maestra-formula100k` primero para configurar tu Autopilot."

Extraer: `niche`, `keywords`, `email`, `voice_profile`

---

## FASE 2 — CAZAR REFS VIRALES DE LA SEMANA

### Paso 2 — Apify TikTok para 7 slots

Para cada keyword en `config.keywords`, buscar con Apify `clockworks~tiktok-scraper`:
```json
{
  "searchQueries": ["[keyword]"],
  "resultsPerPage": 25,
  "shouldDownloadVideos": false
}
```

Filtrar:
- Publicados en los últimos 7 días
- Views mínimo: 200,000 (semana tiene más tiempo para acumular)

De todos los resultados, seleccionar los TOP 7 priorizando:
1. Diversidad de temas (no todos del mismo ángulo)
2. Distribución de formatos (educativo, historia, opinión, tendencia)
3. Máxima relevancia al nicho

Guardar cada viral: URL, caption (primeras 100 chars), views, autor, fecha.

---

## FASE 3 — ASIGNAR VIRALES A LOS 7 DÍAS

### Paso 3 — Distribución semanal (modo Crecimiento 40/50/10 — default)

Asignar cada viral al día más apropiado según el tipo de contenido:

| Día | Slot | Tipo de pieza |
|-----|------|---------------|
| LUN | Arranque fuerte | Viral de reacción o dato impactante |
| MAR | Educativo | Tutorial, tip con pasos, herramienta |
| MIE | Historia / Storytelling | Experiencia personal o caso de éxito |
| JUE | Educativo | Framework, sistema, comparativa |
| VIE | Venta suave | Mencionar comunidad/oferta en el CTA |
| SAB | Viral o Tendencia | Lo más caliente de la semana |
| DOM | Reflexión / Motivacional | Mindset, por qué esto importa |

---

## FASE 4 — GENERAR 7 GUIONES

### Paso 4 — Un guion por día

Para cada día, generar un guion de 45-60 segundos usando los patrones de `guionizacion-formula100k`:

Cada guion incluye:
- **Gancho verbal** (primeras 3-5 palabras que detienen el scroll)
- **Cuerpo** (3 puntos o pasos o revelaciones)
- **CTA** (patrón F100K: pregunta + palabra + promesa)
- Escrito con la voz de `voice_profile`
- Conectado al viral de referencia del día

Para el slot de VIERNES (venta suave), el CTA incluye:
> "Comenta [PALABRA] y te cuento cómo entrar a [comunidad/programa del usuario]"

---

## FASE 5 — EXPORTAR CALENDARIO

### Paso 5 — Generar CSV

Crear archivo en `guiones/calendarios/` con nombre:
`calendario_[fecha_lunes]_[nicho_slug].csv`

Donde `nicho_slug` = primeras 2 palabras del nicho en minúsculas con guión (ej: `finanzas-personales`, `marketing-digital`)

Columnas del CSV:
```
DÍA,IDEA,GUION,LLAMADO A LA ACCIÓN,FORMATO,REFERENCIA
```

Invocar `calendarizador-contenido-formula100k` con los 7 guiones + referencias para generar también el XLSX con formato visual.

---

## FASE 6 — EMAIL DEL LUNES

### Paso 6 — Enviar con Gmail MCP

Usar `mcp__claude_ai_Gmail__create_draft`:

**Para:** `config.email`

**Asunto:**
```
📅 Tu Calendario F100K — Semana del [fecha_lunes] al [fecha_domingo]
```

**Cuerpo:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅  CALENDARIO SEMANAL F100K
[Lunes fecha completa] → [Domingo fecha completa]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LUNES     | [idea corta] | Ref: [views] · [URL]
MARTES    | [idea corta] | Ref: [views] · [URL]
MIÉRCOLES | [idea corta] | Ref: [views] · [URL]
JUEVES    | [idea corta] | Ref: [views] · [URL]
VIERNES   | [idea corta] | Ref: [views] · [URL]
SÁBADO    | [idea corta] | Ref: [views] · [URL]
DOMINGO   | [idea corta] | Ref: [views] · [URL]


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁  ARCHIVO COMPLETO (con guiones)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

El calendario con todos los guiones está guardado en:
[ruta completa del archivo CSV/XLSX]

Copia los guiones desde ahí directo a tu planner.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡  TIP DE LA SEMANA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1 insight basado en los virales de la semana — algo que el patrón de los virales revela sobre el nicho del usuario]


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Autopilot F100K · fórmula100k.app
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
