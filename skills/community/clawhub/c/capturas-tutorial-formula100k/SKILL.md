---
name: capturas-tutorial-formula100k
description: "Genera CAPTURAS UI tipo tutorial (cards de paso numerado, code blocks tipo terminal macOS con botón Copiar, callouts info/warning/success, screenshot frames, atajos de teclado, links, comparison antes/después, listas) con la estética F100K (fondo crema, círculos coral, DM Serif Display, Inter, JetBrains Mono). Render HTML+CSS+Puppeteer → PNG transparente o crema, 1920×1080. NO usa Nanobanana ni Higgsfield (la IA rompe el texto; HTML es pixel-perfect). Activar cuando pidan \"diséñame una captura tipo tutorial\", \"imagen del comando\", \"renderiza un terminal con este comando\", \"card de paso 1/2/3\", \"callout warning/info/success\", \"tarjeta de atajo Cmd+V\", \"comparison antes/después\", \"imagen UI para mi landing/artifact/carrusel\", \"overlays UI para mi video tutorial\", \"convierte este guion en capturas tutorial\". 2 modos: STANDALONE (PNGs sueltos) y BATCH (MANIFEST_UI.yml). También la invoca recursos-de-video-formula100k. NO renderiza video (editor-video-formula100k). NO usa stock."
allowed-tools: "Bash, Read, Write, Edit, AskUserQuestion"
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Render con Puppeteer sobre **el Chromium que ya trae OpenClaw**: instala las dependencias con `PUPPETEER_SKIP_DOWNLOAD=1 npm install` dentro de la carpeta de la skill (evita bajar otro Chrome de ~170 MB) y corre `render.mjs` con `PUPPETEER_EXECUTABLE_PATH=<ruta de tu Chromium>`. Primera instalación: dile qué se instala y espera ✅. Renderiza de a uno, no en paralelo.
> - Las fuentes (DM Serif Display, Inter, JetBrains Mono) se cargan de Google Fonts: el servidor necesita internet al renderizar. Si salen con la fuente genérica, vuelve a renderizar.
> - Tipo `screenshot`: la imagen llega por Telegram como archivo (guárdala en `entregables/capturas/`) o la tomas tú con tu navegador de una web **sin iniciar sesión** (landing, docs, app propia de la usuaria). Nunca capturas de Instagram/TikTok con sesión.
> - Mira cada PNG antes de entregarlo (texto cortado, comando incompleto). Entrega en `entregables/capturas/` y por Telegram como documento, no como foto (Telegram comprime y se pierde la transparencia). Varios PNG → un `.zip`.
> - Los anchos y duraciones «sobre video» son la sugerencia para que la usuaria los monte en su editor; aquí no se compone ningún video.

---

# Capturas Tutorial — FÓRMULA 100K

Skill que genera **capturas UI tipo tutorial** con la estética F100K: terminales macOS, cards de paso, callouts, screenshot frames, keyboard shortcuts, comparisons. Output: PNG.

**No usa IA generativa** para estos assets. Render = HTML + CSS + Puppeteer → PNG. Razón: Nanobanana/Higgsfield rompen texto de terminal y comandos; HTML garantiza que el `curl -fSL ...` exacto aparezca legible.

## Cuándo activar

- "Diséñame un terminal con este comando"
- "Card paso 1/2/3 sobre [tema]"
- "Callout warning de [advertencia]"
- "Tarjeta del atajo Cmd+V"
- "Comparison antes/después para mi carrusel"
- "Simula el input de Claude invocando esta skill"
- "Overlays UI para mi video tutorial"
- "Convierte este guion paso-a-paso en imágenes"
- Cuando `recursos-de-video-formula100k` detecta modo tutorial y delega aquí

## NO activar para

- Pixel-mascot / pixel-infografía con IA → `recursos-de-video-formula100k` modo IA
- B-roll real cazado de internet → `recursos-de-video-formula100k` modo WEB
- Carruseles completos de Instagram con foto + texto sobrepuesto → `carrusel-render-formula100k`
- Stories de Instagram → `historias-a-imagenes-nanobanana`
- Generar el video final → `editor-video-formula100k`
- Generar el guion del tutorial (texto) → `guionizacion-formula100k`

## Regla de modo PURO

Cuando el usuario pide "capturas-tutorial" / "modo UI" / "solo estilo tutorial" para un video, asumir **modo PURO**: TODOS los overlays del reel son de los 8 tipos de esta skill (`step`, `terminal`, `callout`, `screenshot`, `keys`, `link`, `comparison`, `list`). NO mezclar con pixel-mascot IA, NO complementar con WEB, NO generar `HOOK_*.png`. Si un cue del transcript no es léxicamente "tutorial" (ej: una frase de storytelling, una declaración, un CTA), convertirlo al tipo más cercano — típicamente `callout` variant `info` para declaraciones/facts o `callout` variant `success` para CTAs/cierres. Razón: la consistencia visual completa del estilo capturas-tutorial es lo que el usuario valida; el cambio de capa entre captura UI y mascot pixel rompe el flow del viewer.

## Catálogo de tipos (9)

| Tipo | Cuándo usar | Template |
|---|---|---|
| **step** | Card de paso numerado (círculo coral + heading italic + bajada) | `step.html` |
| **terminal** | Code block con chrome macOS + prompt $ + comando + botón "Copiar" | `terminal.html` |
| **callout** | Caja con border-left coloreado + ícono. Variantes: `info`, `warning`, `success`, `note`, `error` | `callout.html` |
| **claude-input** | Simulación del input de Claude con popup de autocompletado de slash commands + caja de input con cursor parpadeante. **OBLIGATORIO** siempre que el video mencione invocar una skill, escribir un slash command, "decirle a Claude que…" o cualquier acción de typing/prompting a Claude. Reemplaza al callout cuando el cue es "skill X especializada / Claude la usa / invoca esta skill / dile a Claude". | `claude-input.html` |
| **screenshot** | Frame de ventana macOS / browser alrededor de una imagen del usuario, con caption italic opcional | `screenshot.html` |
| **keys** | Visual de atajo de teclado: cajas blancas estilo Mac con `+` coral entre teclas | `keys.html` |
| **link** | URL con icono mundo + botón "Abrir" coral | `link.html` |
| **comparison** | Dos cajas lado a lado: ❌ rojo + ✓ verde (antes/después, malo/bueno) | `comparison.html` |
| **list** | Lista vertical 3-6 items con check coral o numeración (opcional con título italic) | `list.html` |

### Regla canónica de `claude-input`

Cuando el guion/transcript mencione UNA skill, slash command, prompt, o cualquier interacción de "escribirle/decirle a Claude algo", **el visual SIEMPRE debe ser un `claude-input` — no un callout**. Razón: la simulación de UI (popup + caja de input con cursor) comunica "skill" / "prompt" sin necesidad de un párrafo de texto, queda más vertical que un callout, y mantiene consistencia con el resto del flow Claude del video. Validado en producción: el callout horizontal pasó a claude-input vertical y el párrafo desapareció.

**Defaults del template** (si no se especifican en `data`):
- `popup_header`: `"Skills disponibles"`
- `icon_active` + `name_active` + `desc_active`: la skill que está siendo invocada (en español, descripción corta de 1 línea)
- `icon_2`, `name_2`, `icon_3`, `name_3`: otras 2 skills del catálogo F100K para que el popup se vea poblado (sin descripción visible)
- `typed`: typically igual a `name_active` (lo que se está escribiendo en el input)

**Catálogo de iconos sugeridos para skills F100K** (usar como `icon_active`/`icon_2`/`icon_3`):
- 📝 guionización · 🎬 carrusel · 🎯 optimizador-cta · 🧠 estrategia · 🚀 lanzamiento · 📊 analizador · 🎨 diseño · 🔍 investigación · 📅 calendario · ✨ historias · 🎙️ audio · 🎥 video

## Sistema visual (tokens)

Ver `templates/_tokens.css`. Resumen:

```
COLOR
  crema base       #F5EFE6
  coral            #E89B7F   (círculos paso, botón Copiar, prompt $)
  coral oscuro     #D87A55   (hover/sombra)
  ink              #2B2B2B   (texto principal)
  terminal bg      #1E1E1E   (fondo terminal)
  success / warning / error / info  → border-left de callouts

FONTS
  display: DM Serif Display italic   → headings paso, comparison title
  body:    Inter 400/600/700         → bajadas, callouts, captions
  mono:    JetBrains Mono            → terminal, code inline, URL del link card

RADIUS
  card 20px · terminal 14px · callout 12px · key 8px
```

## Pipeline

### MODO 1 — STANDALONE (input directo)

Para capturas sueltas pegables en landings, artifacts, carruseles, threads, etc.

**Paso 1.** Bootstrap (idempotente):

```bash
bash skills/capturas-tutorial-formula100k/scripts/install.sh
```

Instala puppeteer + js-yaml en `node_modules/` local de la skill. Solo corre completo la primera vez.

**Paso 2.** Preguntar al usuario el contenido. Si no es obvio, usar `AskUserQuestion` para confirmar:
- ¿Qué tipo? (step / terminal / callout / etc.)
- ¿Contenido literal? (comando exacto, texto del paso, etc.)
- ¿Fondo crema o transparente?
- ¿Ruta de output?

**Paso 3.** Renderizar:

```bash
node skills/capturas-tutorial-formula100k/scripts/render.mjs \
  --type <tipo> \
  --out <ruta_archivo.png> \
  --data '<JSON>' \
  [--bg cream|transparent] \
  [--width 1920] [--height 1080]
```

Ejemplos:

```bash
# Terminal con comando
node render.mjs --type terminal --out terminal_claude.png \
  --data '{"command":"curl -fsSL https://claude.ai/install.sh | bash"}'

# Paso numerado
node render.mjs --type step --out paso_2.png --bg cream \
  --data '{"number":2,"title":"Pega el comando de instalación","body":"Copia el comando de abajo y pégalo en la Terminal con **Cmd+V** y presiona Enter."}'

# Callout info
node render.mjs --type callout --out callout_que_hace.png \
  --data '{"variant":"info","body":"**¿Qué hace este comando?** Descarga el instalador oficial de Anthropic, lo ejecuta y coloca Claude Code en `~/.local/bin`."}'

# Keyboard shortcut
node render.mjs --type keys --out atajo_cmdv.png \
  --data '{"keys":["Cmd ⌘","V"],"label":"Pegar en la Terminal"}'

# Screenshot enmarcado
node render.mjs --type screenshot --out captura_exito.png \
  --data '{"frame":"mac","title":"Terminal","image":"entregables/capturas/captura.png","caption":"Cuando termina vas a ver Claude Code successfully installed"}'

# Comparison antes/después
node render.mjs --type comparison --out compare.png \
  --data '{"no_title":"Sin Claude Code","no_body":"Editas archivos uno por uno.","yes_title":"Con Claude Code","yes_body":"Le dictas y él edita el repo completo."}'

# Lista
node render.mjs --type list --out checklist.png \
  --data '{"title":"Vas a necesitar","items":["Una Mac con macOS 12+","Una cuenta en claude.ai","5 minutos"]}'

# Link card
node render.mjs --type link --out link_claude.png \
  --data '{"label":"Sitio oficial","url":"claude.ai/install"}'

# Claude input simulando invocación de skill (popup + slash command + cursor)
node render.mjs --type claude-input --out skill_invoke.png \
  --data '{"popup_header":"Skills · F100K","icon_active":"📝","name_active":"guionizacion-formula100k","desc_active":"Crea guiones virales con tu voz y estrategia.","icon_2":"🎬","name_2":"carrusel-viral-formula100k","icon_3":"🎯","name_3":"optimizador-cta-formula100k","typed":"guionizacion-formula100k"}'
```

**Markdown ligero soportado en `body`/`text`**: `**negrita**` y `` `código inline` ``. No se acepta HTML directo (se escapa por seguridad).

**Paso 4.** Validación visual: leer el PNG generado con la tool `Read` y confirmar contra el contenido pedido. Si el texto está clipeado / el comando se cortó / el ícono no se ve → ajustar `data` o `width` y regenerar.

**Paso 5.** Entregar al usuario: `open <ruta>` para abrirlo en macOS.

---

### MODO 2 — BATCH (desde MANIFEST_UI.yml)

Para overlays de video tutorial. La skill `recursos-de-video-formula100k` genera el MANIFEST_UI.yml a partir del transcript Whisper aplicando los triggers léxicos (sección siguiente) y luego invoca este modo.

**Estructura del manifest:**

```yaml
recursos:
  - id: r01
    tipo: step
    bg: transparent
    width: 1920
    height: 1080
    data:
      number: 2
      title: "Pega el comando de instalación"
      body: "Copia el comando de abajo y pégalo en la Terminal con **Cmd+V** y presiona Enter."
      slug: "pega-comando"

  - id: r02
    tipo: terminal
    data:
      command: "curl -fsSL https://claude.ai/install.sh | bash"
      title: "Terminal — bash"
      slug: "curl-claude-install"

  - id: r03
    tipo: callout
    data:
      variant: info
      body: "**¿Qué hace este comando?** Descarga el instalador oficial de Anthropic, lo ejecuta y coloca Claude Code en `~/.local/bin`. No toca el resto del sistema."
      slug: "que-hace-instalador"
```

**Comando:**

```bash
node skills/capturas-tutorial-formula100k/scripts/render.mjs \
  --manifest entregables/recursos-video/2026-05-22_claude-install/MANIFEST_UI.yml \
  --out entregables/recursos-video/2026-05-22_claude-install/USER/
```

**IMPORTANTE — destino:** los PNGs van a `USER/`, **NO** a una subcarpeta `UI/`. Razón: `editor-video-formula100k` solo lee tres carpetas (`IA/`, `USER/`, `WEB/`) y consolida todos los overlays en UNA sola tabla `## Overlays` del MANIFEST.md principal. Las capturas tutorial conviven con los screenshots manuales del usuario en `USER/` — el editor las distingue por el prefijo del filename (`r<NN>_<tipo>_*` viene de batch UI; `T<N>_*` viene de captura manual).

Si el modo de invocación es `--out` explícito a otra carpeta, el default del script ya cambió a `USER/` (sibling al manifest), así que basta con omitir el flag y queda donde toca.

Naming auto de archivos: `<id>_<tipo>_<slug>.png`. Ej: `r01_step_pega-comando.png`.

**Post-procesado automático del script (v1.1.0):**
- Cada PNG sale al **tamaño real del contenido** (bbox de alpha + 40px de padding), NO al canvas 1920×1080. Típico: callout ~960×184, step ~870×270, terminal ~1000×280. Esto evita que Remotion intente decodificar texturas 1920×1080 transparentes (rompía el render del editor con `EncodingError`).
- `--scale 1` por default — el viewport y el output coinciden 1:1 en píxeles. NO subir a `--scale 2` (Remotion no decodifica 3840×2160 en paralelo, OOM).
- Para desactivar el trim (ej: si quieres preservar el canvas completo para componer en otro flujo), pasar `--no-trim`.

---

## Triggers léxicos (cómo identificar UI cues en un transcript)

Cuando la skill se invoca desde `recursos-de-video-formula100k` con transcript Whisper word-level, escanear cada segmento de 5-10s buscando estos patrones. Output: items para el MANIFEST_UI.yml.

### `step` — Paso numerado
- `"paso \d+"` · `"paso uno|dos|tres"`
- `"^primero,?"` · `"^segundo,?"` · `"^tercero,?"`
- `"después,?"` · `"luego,?"` · `"ahora vas a"` · `"lo siguiente es"` · `"a continuación"`

Extraer: número de orden (si no es explícito, contador incremental) + la frase que cierra el paso como `title` + el resto del segmento como `body`.

### `terminal` — Code block
- `"copia (este|el) comando"` · `"pega esto en (la|tu) terminal"`
- `"ejecuta"` · `"corre esto"` · `"corre el comando"`
- `"en la terminal,?"` · `"abre la terminal y"`
- `"escribe (esto|este comando)"`
- **Señal fuerte**: si el video muestra terminal real en pantalla, considerar OCR del frame para capturar el comando literal. Si el usuario dicta el comando, capturar verbatim limpiando muletillas.

Extraer: `command` = el comando exacto. Si la URL/dominio aparece, conservar.

### `callout_info`
- `"¿qué hace (esto|este|esta)\\?"` · `"esto significa"` · `"para qué sirve"` · `"lo que pasa es que"` · `"piensa en esto como"`

Variant: `info`. Body: el segmento completo, con **bold** sobre la primera frase clave.

### `callout_warning`
- `"ojo (con|que)"` · `"cuidado"` · `"importante:?"` · `"atención"` · `"advertencia"` · `"no (te |)olvides"` · `"no hagas"`

Variant: `warning`.

### `callout_success`
- `"cuando termine,?"` · `"si todo (salió|sale) bien"` · `"deberías ver"` · `"te va a (aparecer|mostrar) un mensaje"` · `"verás (un|el) mensaje"`

Variant: `success`.

### `callout_note`
- `"tip,?"` · `"bonus,?"` · `"extra,?"` · `"un detalle,?"` · `"por cierto"`

Variant: `note`.

### `claude-input` — Skill / slash command / prompt a Claude (OBLIGATORIO sobre callout)
- `"skill (de|para|que)"` · `"la skill (X|de X)"` · `"esta skill"` · `"una skill especializada"`
- `"slash command"` · `"comando /\w+"` · `"/\w+-formula100k"` · `"escribe /\w+"`
- `"le (dices|pides|escribes|dictas) a claude"` · `"claude (la usa|usa esta|tiene)"` · `"invocas (la|esta) skill"`
- `"pega esto en claude"` · `"escríbele a claude"` · `"prompt para claude"`

Cuando el cue matchea uno de estos patrones, generar **claude-input** (NO callout, aunque el contenido suene declarativo). Extraer:
- `name_active`: el nombre de la skill o slash command mencionado (sin la `/` inicial). Si no se nombra explícita, inferir del contexto.
- `desc_active`: la frase que describe qué hace la skill (1 línea, ≤80 chars, en español).
- `typed`: typically igual a `name_active`.
- `icon_active`: del catálogo de íconos sugeridos según el dominio de la skill.
- `icon_2`/`name_2`/`icon_3`/`name_3`: otras 2 skills relacionadas para poblar el popup (sin descripción).

### `screenshot`
- `"te va a aparecer"` · `"vas a ver (una pantalla|esto|así)"` · `"se ve (así|de esta forma)"` · `"como en la imagen"` · `"como esto"`

Flag: necesita asset del usuario (carpeta `USER/` en la convención de `recursos-de-video-formula100k`). Si no hay screenshot disponible, omitir el cue o degradar a `callout_success` con la descripción textual.

### `keys` — Keyboard shortcut
- `"(cmd|⌘|control|ctrl) ?\+ ?\w+"` · `"presiona (cmd|ctrl|shift|enter|tab)"`
- `"el atajo (es|de teclado es)"` · `"con (cmd|ctrl|shift)\+"`

Extraer: lista de teclas en orden de la frase.

### `link`
- `"ve a"` · `"entra a"` · `"abre (el navegador|chrome|safari) en"`
- Cualquier URL `https?://\S+` mencionada en el audio.

Extraer: URL completa. Si el usuario dice solo el dominio (`"entra a formula100k.app"`), reconstruir.

### `comparison`
- `"esto (NO|sí)"` con contraste · `"antes,? \w+ → ahora,?"` · `"no hagas X, haz Y"` · `"el error es,? .* lo correcto es"`

Estructura: extraer las dos mitades — ❌ y ✓.

### `list`
- `"vas a necesitar"` · `"los (tres|cuatro|cinco) pasos son"` · `"hay (3|4|5) cosas"` · `"requisitos:?"`

Extraer: items enumerados en el segmento.

---

## Heurísticas de posición sobre video (cuando se compone con editor-video)

Cada tipo tiene una posición y un tamaño sugeridos cuando se usa como overlay sobre talking-head 9:16 (canvas 1080w). Anchos calibrados para que el TEXTO sea legible una vez aplicado el trim del bbox + 40px de padding.

| Tipo | Posición default | Ancho px (sobre 1080w) | Duración mínima |
|---|---|---|---|
| step | overlay center | **940** | 3.0s |
| terminal | overlay center | **980** (1040 si el comando es largo) | 4.0s |
| callout (todos) | overlay bottom-third | **960** | 3.0s |
| claude-input | overlay center | **820** (ratio ~1.5:1, vertical) | 4.0s |
| screenshot | overlay center | **720** | 3.5s |
| keys | overlay center | **380** | 2.5s |
| link | overlay bottom-third | **560** | 2.5s |
| comparison | overlay center | **880** | 5.0s (necesita leer 2 cajas) |
| list | overlay center | **640** | 1.0s por item (min 3.0s) |

Estos defaults se incluyen en el MANIFEST.md como sugerencia. El editor-video los respeta salvo que el usuario los override.

**Por qué estos anchos:** sobre talking-head 9:16, los PNGs vienen ya recortados al bbox real del contenido (script aplica `sharp.trim() + extend(40px)`). Si el manifest pide 640, el overlay ocupa ~60% del canvas — texto se vuelve marginalmente legible en móvil. 940-980 es el sweet spot donde el contenido lee bien sin chocar con el header y sin tapar la cara del usuario.

---

## Reglas obligatorias

1. **NO 9:16 para overlays**: por preferencia del usuario. Default: 16:9 o 1:1.
2. **NO emojis decorativos** dentro de los textos salvo que el contenido los requiera (ej: el ícono del callout sí, un 🔥 al final de un body NO).
3. **NO inventar comandos / URLs / nombres de archivo**: si el usuario dice "el comando de install", pedirle el comando exacto antes de renderizar.
4. **Markdown ligero solamente**: `**bold**` y `` `code` ``. Cualquier otro HTML se escapa.
5. **PNG transparente por default** (el usuario decide en edición). Si pide explícitamente con fondo crema, usar `--bg cream`.
6. **Validar visual con Read después de renderizar**: confirmar que el texto no quedó clipeado, que el comando se ve completo, que las teclas no se desbordan.

## Errores y fallbacks

| Error | Acción |
|---|---|
| `puppeteer` falla al arrancar (sandbox) | Ya pasamos `--no-sandbox`. Si igual falla, `brew install chromium` y reintentar. |
| Fonts no cargan (sin internet) | El render espera `document.fonts.ready` — si timeout >10s, el PNG sale con fallback genérico. Sugerir reintentar con conexión. |
| Comando muy largo se sale del terminal | Aumentar `width` a 1280 o 1440. Si sigue sin caber, partirlo con `\` y newlines en el JSON. |
| Screenshot inválido / no encontrado | Validar `image` exists antes de renderizar. Si no, omitir el cue. |
| `js-yaml` no instalado para modo manifest | Correr `install.sh`. |

## Atajos conversacionales

- `/capturas-tutorial <tipo> <contenido>` → modo standalone, render directo
- `/capturas-tutorial manifest <ruta-yml>` → modo batch
- `/captura-terminal <comando>` → atajo para terminal
- `/captura-paso <N> <título> | <bajada>` → atajo para step

## Integración con otras skills

- **[[recursos-de-video-formula100k]]** invoca esta skill en modo BATCH cuando detecta video tutorial. Pasa el MANIFEST_UI.yml ya armado.
- **[[editor-video-formula100k]]** consume los PNGs de `USER/` (donde van tanto los screenshots manuales como las capturas UI tutorial generadas por esta skill en modo BATCH) y los compone sobre el video como overlays, igual que ya hace con los pixel-mascots de IA/.
- **[[generador-artifact-educativo-formula100k]]** puede invocar esta skill en modo STANDALONE para insertar capturas tipo tutorial dentro de un artifact HTML.
- **[[carrusel-render-formula100k]]** puede usar capturas individuales (terminal, callout) como elemento de un slide.

## Roadmap (futuro, no implementado)

- Animación: terminal con efecto "typing" del comando (APNG / WebM con alpha)
- OCR auto del frame del video cuando muestra terminal real → genera el `terminal.png` sin que el usuario dicte
- Variantes adicionales: `progress-bar`, `file-tree`, `diff-block`
