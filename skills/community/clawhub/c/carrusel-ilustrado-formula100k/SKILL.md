---
name: carrusel-ilustrado-formula100k
description: "Skill para crear carruseles de Instagram RENDERIZADOS COMPLETAMENTE (PNG finales listos para publicar, sin Canva). Ilustraciones minimalistas estilo Xiaohei (hand-drawn, figura negra sólida, fondo blanco puro) generadas con Higgsfield + slides HTML renderizados con Chrome headless. Puede mezclar slides de ilustración y slides con mockups de UI. Activar SIEMPRE que alguien diga: \"carrusel ilustrado\", \"carrusel estilo Xiaohei\", \"ilustraciones minimalistas para carrusel\", \"carrusel con dibujos\", \"carrusel con ilustraciones\", \"slides ilustrados\", o cualquier variación que implique generar un carrusel con ilustraciones de personaje hand-drawn."
argument-hint: "[tema o guion del carrusel] [contexto: educativo / venta / storytelling] [mockups: sí/no]"
metadata: {"version": "2.0.0", "modelo": "nano_banana_2", "formato": "4:5 — 1080×1350px", "estilo": "Xiaohei hand-drawn · fondo blanco · acentos naranja F100K", "render": "HTML + Chrome headless — PNG finales sin Canva", "openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Las ilustraciones se generan con **Gemini directo (`GEMINI_API_KEY`, sección 3.1 del puente)**; si no hay llave, con el plugin de Higgsfield. Costo estimado y ✅ antes.
> - Sin ningún motor: entrega el guion slide por slide + el prompt en inglés de cada ilustración para generarlas a mano.
> - Las imágenes van a `entregables/` y se mandan por Telegram en orden de slide.

---

# Skill: Carrusel Ilustrado — Fórmula 100K

Genera carruseles de Instagram (5-8 slides) con ilustraciones estilo Xiaohei: figura sólida negra, fondo blanco puro, line art hand-drawn, acentos mínimos en naranja F100K (#F59E0B). Cada slide recibe el tipo de ilustración más efectivo para el concepto que comunica.

---

## CUÁNDO ACTIVAR

- "carrusel ilustrado de [tema]"
- "carrusel estilo Xiaohei"
- "ilustraciones minimalistas para carrusel"
- "carrusel con dibujos"
- "slides ilustrados sobre [concepto]"
- Cualquier carrusel donde el concepto sea abstracto y necesite visualización conceptual

**No usar esta skill cuando:** el carrusel necesita fotografías fotorrealistas de personas reales o diseño tipográfico puro sin ilustración. En esos casos → `higgsfield-carrusel-generador`.

**Sí soporta mockups de UI:** si el carrusel mezcla ilustraciones + pantallas de una app, generar los mockups como HTML + screenshot y combinarlos con las ilustraciones en el PASO 6.

---

## LOS 8 TIPOS DE ILUSTRACIÓN

Cada slide del carrusel recibe exactamente uno de estos tipos. La asignación se hace en el PASO 2.

| # | Tipo | Úsalo para | Xiaohei en escena |
|---|------|------------|-------------------|
| 1 | **Workflow** | Procesos secuenciales, metodologías, sistemas paso a paso | Caminando a lo largo de una línea de pasos numerados o subiendo escaleras |
| 2 | **System Locale** | Componentes de un sistema, stacks de herramientas, módulos de un curso | Parado en el centro con flechas o conexiones hacia los elementos del sistema |
| 3 | **Before/After Contrast** | Estado malo vs. bueno, antes/después de aprender algo | Dos versiones del mismo escenario: izquierda caótica, derecha ordenada |
| 4 | **Role Status** | Estado mental/situacional del lector (se identifica con Xiaohei) | Posturas expresivas: abrumado (papeles cayendo), enfocado (zoom en pantalla), victorioso (brazo arriba) |
| 5 | **Concept Metaphor** | Hacer tangible un concepto abstracto (algoritmo, engagement, autoridad) | Literalizando la metáfora: megáfono gigante, imán atrayendo personas, balanza con ideas |
| 6 | **Method Layering** | Jerarquías, pirámides, capas que se construyen una sobre otra | Construyendo o sosteniendo capas apiladas como bloques o plataformas |
| 7 | **Map/Route** | Roadmaps, journeys del cliente, secuencias de decisión | Viajando por un mapa con puntos de decisión o en un camino que se bifurca |
| 8 | **Comic Strip Sequence** | Historias cortas, "esto te ha pasado", storytelling en secuencia | En 3-4 paneles narrativos que cuentan una situación de principio a fin |

---

## FLUJO COMPLETO

### PASO 0 — Recibir el tema o guion

**⚠️ OBLIGATORIO: El guion debe venir de `carrusel-viral-formula100k` antes de ejecutar esta skill.**

Si el usuario solo da un tema sin guion slide-por-slide:
→ Invocar la skill `carrusel-viral-formula100k` para desarrollar el gancho con referencias virales reales y generar el guion completo. No continuar hasta tener el texto exacto de cada slide.

Si ya hay un guion completo (texto de cada slide definido):
→ Continuar al PASO 1 directamente.

---

### PASO 1 — Diseñar la arquitectura de slides

Determinar cuántos slides (recomendado: 5-8) y asignar a cada uno:
- **Número de slide**
- **Propósito** (hook / desarrollo / CTA / conclusión)
- **Concepto central** que debe comunicar

**Estructura tipo recomendada para carrusel educativo/venta F100K:**

| Slide | Propósito | Tipo recomendado |
|-------|-----------|-----------------|
| 1 | Hook visual — captura atención | Role Status o Concept Metaphor |
| 2 | Problema identificado | Before/After Contrast |
| 3-5 | Desarrollo del método o idea | Workflow o Method Layering |
| 6 | Sistema completo o visión | System Locale o Map/Route |
| 7-8 | CTA o llamada a acción | Role Status (victorioso) o Comic Strip |

---

### PASO 2 — Asignar tipo de ilustración a cada slide

Para cada slide, seleccionar el tipo más efectivo usando esta lógica:

```
¿El slide muestra un proceso con pasos ordenados?  → Workflow (1)
¿El slide muestra partes/herramientas de un sistema?  → System Locale (2)
¿El slide contrasta dos estados opuestos?  → Before/After Contrast (3)
¿El slide describe cómo se SIENTE el lector?  → Role Status (4)
¿El slide usa una metáfora para explicar algo abstracto?  → Concept Metaphor (5)
¿El slide muestra niveles, capas o jerarquía?  → Method Layering (6)
¿El slide muestra un camino, journey o decisión?  → Map/Route (7)
¿El slide cuenta una historia o situación narrativa?  → Comic Strip Sequence (8)
```

---

### PASO 3 — Construir prompts para Higgsfield

Para cada slide, construir el prompt en inglés usando esta plantilla base y reemplazando las secciones `[BRACKETED]`:

```
Minimalist hand-drawn illustration on pure white (#FFFFFF) background.
Black ink line art style, slightly irregular "hand-drawn" quality lines.

CHARACTER: Xiaohei — solid black figure, white dot eyes, thin stick legs, 
blank neutral expression. [DESCRIBE the specific action Xiaohei is performing 
related to the slide concept].

COMPOSITION: Subject occupies 45-55% of frame. Large white space around subject.
[DESCRIBE any props, arrows, labels, or annotation elements in the illustration].

ACCENTS: Minimal use of orange #F59E0B for emphasis annotations only. 
Maximum 2 accent elements total. No other colors.

STYLE: Eccentric and creative but clean. Not cute, not kawaii. 
"Absurd professional worker" aesthetic. Similar to Chinese editorial illustration style.
No gradients, no shadows, no textures. Pure geometric minimalism.
NEVER include any text or watermarks in the illustration.

FORMAT: 4:5 vertical composition optimized for Instagram (1080x1350px equivalent).
```

**Adaptaciones por tipo de ilustración:**

**Tipo 1 — Workflow:**
```
CHARACTER: Xiaohei walking along a horizontal path with [N] numbered circular 
nodes connected by arrows. At step [X], Xiaohei is positioned mid-stride 
pointing forward. Each node has a simple icon representing [step concepts].
COMPOSITION: Path extends across 80% of frame width. Xiaohei at center-left.
```

**Tipo 2 — System Locale:**
```
CHARACTER: Xiaohei standing at center with arms slightly raised. 
[N] labeled boxes or circles float around Xiaohei connected by thin arrows 
pointing inward/outward, representing [system components].
COMPOSITION: Xiaohei at exact center, components arranged in orbit around subject.
```

**Tipo 3 — Before/After Contrast:**
```
CHARACTER: Two instances of Xiaohei — LEFT: surrounded by [chaotic elements: 
scattered papers/tangled lines/question marks]. RIGHT: same pose but orderly, 
with [clean elements: organized stacks/clear arrow/checkmark].
COMPOSITION: Vertical dividing line at center. Left zone labeled "BEFORE" area, 
right zone labeled "AFTER" area. Each side occupies equal frame space.
```

**Tipo 4 — Role Status:**
```
CHARACTER: Xiaohei in [specific expressive pose]: 
- Overwhelmed: arms raised, surrounded by floating papers/notifications
- Focused: leaning toward glowing screen, one hand on chin
- Victorious: one arm raised, small star burst above head
- Confused: tilted head, question mark floating nearby
[Match the pose to the emotional state of the slide].
COMPOSITION: Xiaohei occupies center 50% of frame. Emotional props in surrounding space.
```

**Tipo 5 — Concept Metaphor:**
```
CHARACTER: Xiaohei holding/operating/interacting with [literal object that 
represents the concept]: a giant megaphone for reach, a magnet attracting 
tiny figures for engagement, a scale with ideas for decision-making, 
a telescope for strategy, a funnel for conversion.
COMPOSITION: The metaphor object is larger than Xiaohei (60-70% of frame height).
Xiaohei appears small but in control of the giant object.
```

**Tipo 6 — Method Layering:**
```
CHARACTER: Xiaohei standing beside or on top of a stack of [N] rectangular 
layers/platforms, each labeled with a simple icon. Bottom layer is widest, 
top layer is narrowest. Xiaohei is at the top layer, arms spread wide.
COMPOSITION: Pyramid/stack centered in frame. Xiaohei at apex. 
Orange accent on the top layer to indicate achievement.
```

**Tipo 7 — Map/Route:**
```
CHARACTER: Xiaohei walking or riding a simple vehicle along a winding path 
that connects [N] labeled waypoints: [list waypoints]. At a fork in the path, 
Xiaohei has one arm raised pointing toward the correct direction.
COMPOSITION: Path creates an S-curve or Z-pattern across the full frame. 
Start point at bottom-left, destination at top-right. Waypoints as small circles.
```

**Tipo 8 — Comic Strip Sequence:**
```
CHARACTER: Xiaohei in [3-4] equal panels arranged in a 2x2 grid or horizontal strip.
Panel 1: [action/situation]. Panel 2: [reaction/development]. 
Panel 3: [turning point]. Panel 4: [resolution/punchline].
COMPOSITION: Thin black borders separate panels. Each panel has equal size.
Xiaohei's expression/posture changes significantly between panels.
```

---

### PASO 4 — Generar imágenes en paralelo

Llamar a `mcp__higgsfield__generate_image` para TODOS los slides simultáneamente.

Parámetros para cada llamada:
```
model: "nano_banana_2"
prompt: [prompt construido en PASO 3]
aspect_ratio: "4:5"
quality: "high"
```

Esperar los resultados y anotar el job_id de cada generación.

---

### PASO 5 — Verificar y descargar resultados

Para cada job_id:
1. Llamar `mcp__higgsfield__job_status` hasta que el status sea "completed"
2. Obtener la URL de la imagen generada
3. Descargar a: `entregables/[YYYY-MM-DD]_carrusel-ilustrado-[slug-del-tema]/`
   - Naming: `slide-01-[tipo].png`, `slide-02-[tipo].png`, etc.

Si alguna imagen no refleja el estilo Xiaohei correctamente (fondos de color, sombras, kawaii):
→ Reforzar el prompt con: `"IMPORTANT: Pure white background only. Solid flat black figure. Zero gradients. Zero shadows. Zero cute/kawaii aesthetic."`
→ Regenerar ese slide solo.

---

### PASO 6 — Renderizar slides completos (HTML + Chrome headless)

**NO usar Canva. Renderizar directamente como PNG finales.**

Para cada slide, crear un archivo `render-NN.html` (1080×1350px) y capturarlo con Chrome headless.

#### 6a — Mockups de UI (si el carrusel los incluye)

Si algún slide muestra una pantalla de app, generarla primero como HTML independiente:

```html
<!-- mockup-[nombre].html — 1080×1350px, no necesita ser 4:5 exacto -->
<!DOCTYPE html>
<html><head>
<style>
  body { width:1080px; height:1350px; background:#F8F8F8; font-family:'Inter',system-ui; overflow:hidden; display:flex; }
  /* sidebar oscuro + main blanco + cards con datos reales */
</style></head><body>
  <!-- sidebar nav + contenido principal con KPIs, cards, listas, pipeline -->
</body></html>
```

Capturar con Chrome headless:
```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --no-sandbox --disable-gpu \
  --window-size=1080,1350 \
  --screenshot="$DIR/mockup-[nombre].png" \
  "file://$DIR/mockup-[nombre].html" 2>/dev/null
```

#### 6b — Template HTML para slides de ilustración

```html
<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { width:1080px; height:1350px; background:#fff; font-family:'Inter',system-ui,sans-serif;
       overflow:hidden; display:flex; flex-direction:column; align-items:center;
       justify-content:center; padding:60px; }

/* ELEMENTOS FIJOS */
.brand { position:absolute; top:44px; left:52px; font-size:24px; font-weight:900;
         color:#F59E0B; letter-spacing:-0.5px; }
.slide-num { position:absolute; top:44px; right:52px; font-size:24px; font-weight:700;
             color:#D1D5DB; letter-spacing:2px; }

/* TIPOGRAFÍA */
.eyebrow { font-size:28px; font-weight:700; color:#F59E0B; letter-spacing:4px;
           text-transform:uppercase; margin-bottom:16px;
           display:flex; align-items:center; gap:10px; align-self:flex-start; }
.eyebrow::before { content:''; width:28px; height:4px; background:#F59E0B;
                   border-radius:4px; display:block; }
.lead { font-size:52px; font-weight:500; color:#9CA3AF; text-align:center; margin-bottom:32px; }
.headline { font-size:88px; font-weight:900; color:#111827; text-align:center;
            line-height:1.0; margin-bottom:20px; }
.headline span { position:relative; display:inline-block; }
.headline span::after { content:''; position:absolute; bottom:-6px; left:0; right:0;
                         height:8px; background:#F59E0B; border-radius:4px; z-index:-1; }
.headline em { font-style:normal; color:#F59E0B; }
.subtext { font-size:44px; font-weight:400; color:#9CA3AF; text-align:center; line-height:1.4; }

/* ILUSTRACIÓN */
.illustration { width:660px; height:660px; object-fit:contain; margin-bottom:40px; }
.illustration.sm { width:560px; height:560px; }

/* INDICADOR DE SLIDES (paginación) */
.dot-row { display:flex; gap:10px; justify-content:center; margin-top:44px; }
.dot { width:10px; height:10px; border-radius:50%; background:#E5E7EB; }
.dot.active { background:#F59E0B; width:28px; border-radius:10px; }

/* BROWSER FRAME (para slides con mockups) */
.browser { margin-top:32px; width:960px; border-radius:16px; overflow:hidden;
           box-shadow:0 24px 80px rgba(0,0,0,0.15); border:1px solid #E5E7EB; }
.browser-bar { background:#F3F4F6; padding:12px 18px; display:flex; align-items:center;
               gap:8px; border-bottom:1px solid #E5E7EB; }
.browser-dot { width:12px; height:12px; border-radius:50%; }
.browser-url { flex:1; background:#fff; border-radius:6px; padding:6px 14px;
               font-size:13px; color:#9CA3AF; margin:0 12px; font-family:monospace;
               border:1px solid #E5E7EB; }
.browser-img { width:100%; display:block; height:680px; object-fit:cover; object-position:top; }
</style></head><body>

<div class="brand">NOMBRE·APP</div>
<div class="slide-num">01 / 07</div>

<!-- SLIDE DE ILUSTRACIÓN (ejemplo: hook) -->
<div class="lead">¿Texto introductorio...?</div>
<img class="illustration" src="slide-01-role-status.png">
<div class="headline">Titular<br><span>principal</span></div>
<div class="subtext">Subtexto de apoyo</div>

<!-- SLIDE CON MOCKUP (ejemplo: feature) -->
<!--
<div style="width:100%">
  <div class="eyebrow">MÓDULO 01</div>
  <div class="headline" style="text-align:left;font-size:72px;">Headline del feature.</div>
  <div class="subtext" style="text-align:left;font-size:28px;">Descripción breve.</div>
</div>
<div class="browser">
  <div class="browser-bar">
    <div class="browser-dot" style="background:#FF5F57;"></div>
    <div class="browser-dot" style="background:#FEBC2E;"></div>
    <div class="browser-dot" style="background:#28C840;"></div>
    <div class="browser-url">app.dominio.com/feature</div>
  </div>
  <img class="browser-img" src="mockup-feature.png">
</div>
-->

<div class="dot-row">
  <div class="dot active"></div><div class="dot"></div><div class="dot"></div>
  <div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div>
</div>

</body></html>
```

#### 6c — Slide CTA (fondo oscuro)

```html
<!-- Slide final CTA — fondo #111827 -->
<body style="background:#111827;">
  <div class="brand">NOMBRE·APP</div>
  <div class="slide-num" style="color:#374151;">07 / 07</div>
  <img class="illustration sm" src="slide-07-role-status-cta.png">
  <div class="headline" style="color:#fff;">Título<br>CTA.</div>
  <div class="url" style="font-size:36px;font-weight:700;color:#F59E0B;text-align:center;">app.dominio.com</div>
  <div class="subtext" style="font-size:24px;">Texto secundario o acceso</div>
</body>
```

#### 6d — Capturar TODOS los renders en paralelo

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DIR="[RUTA_SALIDA]"

for i in 01 02 03 04 05 06 07; do
  "$CHROME" --headless=new --no-sandbox --disable-gpu \
    --window-size=1080,1350 \
    --screenshot="$DIR/CARRUSEL-$i.png" \
    "file://$DIR/render-$i.html" 2>/dev/null &
done
wait
ls -lh "$DIR"/CARRUSEL-*.png
```

#### 6e — Verificar renders

Leer cada `CARRUSEL-NN.png` con el tool Read para confirmar que la imagen, tipografía y composición son correctas. Si algún slide tiene problemas → editar el HTML y re-capturar solo ese slide.

---

### SISTEMA DE DISEÑO (todos los renders)

| Elemento | Valor |
|----------|-------|
| Canvas | 1080×1350px (4:5) |
| Font | Inter Black 900 para headline, 700 para eyebrow, 400 para subtext |
| Headline | 88px (reducir a 72px si el texto es largo) |
| Lead (intro superior) | 52px, #9CA3AF |
| Eyebrow | 28px, #F59E0B, letter-spacing 4px, uppercase |
| Subtext | 44px, #9CA3AF |
| Acento principal | #F59E0B |
| Texto principal | #111827 |
| Brand fijo | top-left, 24px, #F59E0B |
| Slide num | top-right, 24px, #D1D5DB |
| Padding | 60px todos los lados |
| Dot-row paginación | siempre al fondo del slide, dot activo = pill naranja |

---

## REGLAS DE ESTILO XIAOHEI

Mantener en TODOS los slides:

- **Fondo**: #FFFFFF puro — sin grises, sin degradados, sin texturas
- **Figura Xiaohei**: negro sólido #000000 — sin gradientes, sin sombras, sin rellenos
- **Line art**: trazo irregular hand-drawn — NO vector perfecto, NO bordes suavizados
- **Ojos**: dos puntos blancos simples — NO expresión facial compleja
- **Piernas**: delgadas, de palo — NO anatomía realista
- **Tono**: excéntrico y profesional — NUNCA kawaii, NUNCA cute, NUNCA infantil
- **Espacio blanco**: abundante — el sujeto ocupa máximo 55% del frame
- **Color de acento**: naranja #F59E0B (F100K) — máximo 2 elementos por slide
- **Texto en imagen**: NINGUNO — la ilustración va limpia; todo el texto lo pone el HTML del slide en el PASO 6 (esta skill no usa Canva)

---

## CARPETA DE SALIDA

```
entregables/[YYYY-MM-DD]_carrusel-ilustrado-[slug]/
│
│  ── ASSETS FUENTE ──
├── slide-01-role-status.png          ← ilustraciones Higgsfield
├── slide-02-before-after.png
├── slide-03-system-locale.png
├── ...
│
│  ── MOCKUPS (si aplica) ──
├── mockup-[nombre].html              ← HTML de pantallas de app
├── mockup-[nombre].png               ← screenshot del mockup
│
│  ── RENDERS FINALES (publicar estos) ──
├── render-01.html                    ← HTML de cada slide compuesto
├── render-02.html
├── ...
├── CARRUSEL-01.png                   ← PNG final listo para Instagram
├── CARRUSEL-02.png
├── CARRUSEL-03.png
├── ...
└── CARRUSEL-07.png
```

**Los archivos `CARRUSEL-NN.png` son el entregable final. Verificar cada uno con Read antes de reportar como completo.**

---

## REFERENCIA RÁPIDA

Consultar `references/guia-ilustraciones.md` para:
- Ejemplos concretos de F100K por cada tipo de ilustración
- Tabla de elementos visuales con descripción en inglés para el prompt
- Galería de combinaciones de tipos por formato de contenido
