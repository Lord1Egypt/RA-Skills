---
name: carrusel-viral-formula100k
description: "Crea carruseles virales de Instagram completos, slide por slide. Activar SIEMPRE que alguien pida: crear un carrusel, diseñar slides, convertir un reel en carrusel, hacer un post de varias diapositivas, estructurar o guionizar un carrusel. También con \"hazme un carrusel\", \"convierte esto en carrusel\", \"quiero hacer slides\", \"estructura mis diapositivas\". Conoce los 35 formatos del recetario de FÓRMULA 100K (F01–F20 y G01–G15: frase partida, tier list, checklist, libreta, garabatos sobre tu foto, chat, antes/después…) y elige uno por objetivo. Investiga referencias virales reales, entrega el guion completo con diseño, genera la imagen gancho con Gemini (Nano Banana) si hay llave, lo arma en Canva si está conectado y da instrucciones precisas de producción."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - La imagen gancho: usa `GEMINI_API_KEY` del entorno (o el modelo de imagen de OpenRouter). La skill `banana` y su script no vienen en este paquete: llama a la API directo como muestra el ejemplo con curl. Costo → ✅ → generar.
> - Construir en Canva solo si Canva está conectado (por ejemplo vía Composio). Si no, entrega el guion y el diseño slide por slide listos para armar.
> - Referencias virales: búsqueda web, o Apify con `APIFY_TOKEN`. Nunca navegador logueado.
> - La imagen se guarda en `entregables/imagenes/` y se manda por Telegram.

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

# Skill: Carrusel Viral — FORMULA 100K

Esta skill transforma una idea o guion en un carrusel de Instagram completamente guionizado, diseñado y construido. El proceso incluye investigación de ganchos virales reales, guion slide por slide con especificaciones de diseño, generación de imagen del gancho con **Nanobanana (skill banana / Gemini API)**, y construcción directa del carrusel en Canva si el usuario proporciona el enlace editable.

---

## PASO 0 — Cargar Perfil Visual de Marca

Este paso se ejecuta SIEMPRE, al principio de cada sesión. El perfil visual garantiza que todos los carruseles tengan coherencia de marca.

### 0.1 — Verificar si existe un perfil configurado

Lee el archivo `references/design_profile.md`.

**Si el archivo contiene `[PERFIL NO CONFIGURADO]` o está vacío:**
→ Ir al PASO 0.2 para hacer el setup inicial

**Si el archivo contiene un perfil completo con datos reales:**
→ Cargar el perfil en memoria y usarlo como base visual para todo el carrusel
→ Confirmar en un mensaje breve: *"✓ Perfil de marca cargado: [nombre de marca]."*
→ Ir directamente al PASO 0.5 para obtener la idea

---

### 0.2 — Setup inicial de marca (solo cuando no hay perfil)

Explicar al usuario:

> "Para crear carruseles con tu estilo visual consistente, necesito conocer tu identidad de marca. Tienes dos opciones:
>
> **Opción A — Compartir referencias visuales** *(recomendada)*
> Sube 1-3 screenshots de carruseles que representen tu estilo (pueden ser tuyos o de inspiración). Analizaré los colores, tipografía, layout y jerarquía visual.
>
> **Opción B — Describir tu marca**
> Responde estas preguntas:
> 1. ¿Nombre de tu marca/cuenta de Instagram?
> 2. ¿Colores de marca? (hex codes o descripción: azul marino, naranja, etc.)
> 3. ¿Tipografías? (si no las sabes: ¿bold/moderna/manuscrita/clásica?)
> 4. ¿Cómo describes tu estilo visual? (minimalista, colorido, profesional, vibrante…)
> 5. ¿Usas algún elemento visual fijo? (marcos, líneas, emojis recurrentes, íconos)"

Esperar la respuesta del usuario antes de continuar.

---

### 0.3 — Analizar referencia y generar el perfil

**Si el usuario compartió imágenes:**

Analiza cada imagen y extrae:

**JERARQUÍA VISUAL**
- Tamaño relativo de títulos vs. cuerpo de texto
- Posición del elemento principal (centrado / izquierda / arriba)
- Densidad de información por slide (minimalista / moderado / denso)
- Uso de espacio en blanco
- Orden de lectura: ¿cómo se mueve el ojo a través del slide?

**CONSISTENCIA DE MARCA**
- Paleta de colores: identifica los 3-5 colores principales, estima hex codes
- Tipografías: fuente de títulos y fuente de cuerpo (o estilo si no se puede identificar)
- Iconografía: flat / outline / ilustración / emoji / ninguno
- Tratamiento de imágenes: full bleed / con marco / circular / sin imágenes
- Tono visual: formal / casual / premium / accesible / energético

**PATRONES DE LAYOUT**
- ¿Texto centrado / izquierda / derecha?
- ¿Fondo sólido / gradiente / imagen / textura?
- ¿Elementos decorativos fijos? (líneas, formas geométricas, bordes)

**Si el usuario respondió las preguntas:**
Completa el perfil usando sus respuestas, estimando valores faltantes según el estilo descrito.

---

### 0.4 — Generar y confirmar el Perfil Visual de Marca

Genera el perfil con este formato exacto:

```
# Perfil Visual de Marca — [Nombre de Marca]

## Identidad Visual
- Nombre de marca: [nombre]
- Estilo general: [minimalista / vibrante / profesional / casual / premium]
- Tono visual: [descripción en 1-2 oraciones]

## Paleta de Colores
- Color primario: #[hex] — [uso: "fondo principal"]
- Color secundario: #[hex] — [uso: "acentos, CTAs"]
- Color de énfasis: #[hex] — [uso: "palabras clave, highlights"]
- Color de fondo slides interiores: #[hex]
- Color de texto principal: #[hex]

## Tipografía
- Fuente de títulos: [nombre] — tamaño sugerido Slide 1: [X]px
- Fuente de cuerpo: [nombre] — tamaño sugerido slides interiores: [X]px
- Estilo tipográfico: [CAPS / title case / bold / italic / regular]

## Layout Base
- Orientación preferida: [texto centrado / texto izquierda / texto derecha]
- Fondo slides interiores: [color sólido / gradiente / textura]
- Uso de imágenes: [sí — estilo [X] / solo en Slide 1 / no]
- Elementos decorativos: [ninguno / líneas / formas / marcos / descripción]

## Jerarquía Visual
- Estructura del Slide 1 (gancho): [imagen grande + texto superpuesto / texto dominante / 50/50]
- Elemento de énfasis para palabras clave: [subrayado / círculo / highlight / bold / color diferente]
- CTA visual: [texto bold / color de énfasis / flecha / botón]

## Prompt de Diseño Canva
"Carrusel Instagram [nombre de marca]: fondo [color + hex], títulos en [fuente] [tamaño]px [color + hex], cuerpo en [fuente] [tamaño]px [color + hex], palabras clave en [color de énfasis + hex], layout [descripción], elementos decorativos: [descripción]. Estilo: [3 adjetivos que describan el look]."
```

Presenta el perfil al usuario y pregunta:
> "¿Está correcto o quieres ajustar algo? Una vez confirmado, usaré este perfil para todos tus carruseles."

Aplica los ajustes que pida.

Luego dile:
> "Para guardar este perfil para sesiones futuras, cópialo y reemplaza el contenido de `references/design_profile.md` en tu skill. Así no tendrás que configurarlo de nuevo."

---

### 0.5 — Obtener la idea o guion + preferencia de producción

Si el usuario ya proporcionó su idea o guion junto con la solicitud inicial, úsala directamente.

Si no la proporcionó, pregunta:
> "¿Cuál es la idea o guion que quieres convertir en carrusel? Puedes pegar el texto de un reel, describir el tema en 1-2 oraciones, o darme el mensaje central que quieres comunicar."

### 0.6 — Preguntar si quiere construcción directa en Canva

**Siempre preguntar esto**, ya sea que la idea haya venido en el mensaje inicial o no:

> "¿Quieres que construya el carrusel directamente en tu Canva? Si es así, pásame el enlace de edición (el que termina en `/edit`) y lo armo slide por slide con tu perfil de marca. Si prefieres hacerlo tú, te entrego el guion completo con instrucciones detalladas."

**Si el usuario proporciona un enlace de Canva:**
→ Guardar el enlace en memoria
→ Confirmar: *"✓ Link de Canva recibido. Construiré el carrusel ahí directamente después de generar el guion y la imagen del gancho."*
→ Ejecutar PASO 6 (construcción en Canva) después de PASO 5

**Si el usuario prefiere hacerlo él:**
→ Continuar con el flujo normal (guion + instrucciones detalladas)
→ Omitir PASO 6

---

## PASO 1 — Analizar el input

Antes de hacer cualquier investigación, extrae los siguientes elementos del input recibido:

1. **Tema central** — ¿de qué trata exactamente?
2. **Audiencia objetivo** — ¿a quién le habla? (creadores, emprendedores, coaches, etc.)
3. **Mensaje clave** — ¿cuál es la única cosa que el lector debe recordar?
4. **Objetivo del carrusel** — qué debe hacer la persona al terminar de deslizar: guardar, comentar, compartir, seguir, conectar o comprar. Si no está claro, pregúntalo en UNA línea: decide el formato del PASO 3
5. **Potencial de gancho** — ¿hay curiosity gap, dato sorprendente, promesa concreta o controversia?

---

## PASO 2 — Investigar referencias virales

**Este paso es obligatorio.** No se entrega el guion sin haber investigado primero.

### 2.1 — Buscar en TikTok (MCP preferido) e Instagram

**Opción A — TikTok MCP (davibauer/tiktok-mcp):**
Si el MCP `davibauer/tiktok-mcp` está disponible en el entorno, úsalo primero. Herramientas disponibles:

```
# Buscar videos virales por tema
search_videos(query="[tema] [nicho]", count=10)

# Buscar por hashtag específico del nicho
search_videos(query="#[hashtag_relevante]", count=10)

# Buscar tendencias actuales en el nicho
search_videos(query="[tema] tips estrategia", count=10)
```

De los resultados del MCP, extrae:
- `play_count` / `digg_count` (likes) — filtra solo los que superan 100K vistas
- `desc` (descripción/gancho) — copia los primeros 15 palabras de los más virales
- `author.nickname` — nota qué cuentas dominan el tema
- `create_time` — prioriza contenido de los últimos 90 días

**Opción B — WebSearch (fallback si el MCP no está disponible):**

```
Búsquedas a realizar:
- "[tema] carrusel viral Instagram 2024 2025"
- "[tema] tiktok viral [mes actual] millones vistas"
- "[tema] instagram carousel hook viral"
- "site:tiktok.com [tema palabras clave]"
```

Busca al menos 3-5 referencias con evidencia de viralidad (millones de vistas, alto engagement).

**Nota:** Siempre intenta el MCP primero. Solo cae a WebSearch si el MCP lanza error de conexión o no está instalado.

### 2.2 — Extraer patrones del gancho

De los resultados encontrados (MCP o WebSearch), identifica:
- ¿Qué formato de gancho se repite en los más virales? (pregunta, dato, afirmación fuerte, antes/después)
- ¿Qué palabras o frases exactas aparecen en los títulos más virales?
- ¿Qué emoción dispara el primer slide? (curiosidad, miedo, esperanza, sorpresa, identificación)
- ¿Cuántas diapositivas usan los más virales?

### 2.3 — Validar el gancho del usuario

Compara la idea del usuario con los patrones encontrados:
- ¿El gancho propuesto genera suficiente curiosity gap?
- ¿Es específico y concreto (números, situaciones, promesas reales)?
- Si el gancho original no está validado por referencias virales, propone uno mejorado basado en lo encontrado

---

## PASO 3 — Elegir el FORMATO (uno de los 37) y la estructura

**Lee `references/formatos-carrusel-35.md`**: los 37 formatos del recetario de FÓRMULA 100K con su objetivo, mecánica, soporte, motor y qué tan bien los resuelve Nano Banana. No inventes un «tipo» si uno de los 37 ya lo cubre.

1. **Formato** — cruza el objetivo del PASO 1 con los patrones virales del PASO 2:
   - Si las referencias del nicho repiten una mecánica que coincide con una ficha (ej. todas son tier lists → **F17**), usa esa ficha.
   - Si no, propón **3 fichas** del objetivo, cada una con 1 línea de por qué, y deja elegir.
   - Si la persona ya nombró un formato («carrusel en libreta», «checklist», «tipo chat», «garabatos sobre mi foto», «F07»), úsalo directo.

   | Objetivo | Primero se proponen | También |
   |---|---|---|
   | Guardado | F07 chuleta · G01 checklist · G05 recursos | F18, F04, G06 glosario, G13 de A a B |
   | Comentario | F17 tier list · G03 qué tipo eres · G08 molde | F08, F14, G12 confesión, G10 frases |
   | Compartido | F01 causa y consecuencia · G10 frases · G06 glosario | F19 mapa |
   | Seguidor | F10 anáfora · F13 garabatos (post fijado) · F07 | F06 |
   | Conexión | F11 historia de origen · G11 errores propios · G12 confesión | F12 |
   | Venta | G07 caso de estudio · G14 antes/después · G15 FAQ en chat | F11, F20, F09 |
   | Autoridad / actualidad | G02 noticia · G04 lo que nadie te dice | F14 hot take |

   Ninguna encaja de verdad → dilo y usa la arquitectura simple (gancho → 3-5 puntos → cierre con CTA).
2. **Anatomía** — con la ficha elegida, abre su bloque en `skills/carrusel-formatos-f100k/references/catalogo.md` (`### <ID> · `) y respeta su anatomía slide por slide, su prompt de guion y su **error típico**. El número de slides lo manda la ficha (F17 puede ser 1 sola; F07, 2); si la ficha no lo fija: mínimo 5, máximo 10.
3. **CTA final** — específico y accionable ("Comenta X", "Guarda esto", "Envía a alguien que...")

**Fabricación según el formato:** el guion lo entregas aquí (PASO 4). Para los PNG del formato elegido (plantillas split / papel / datos / garabato, HTML libre de las fichas G, o los prompts listos para Gemini y ChatGPT si la persona no usa Claude Code), invoca `carrusel-formatos-f100k` con la ficha + el guion aprobado: esa skill tiene el visual detallado, las plantillas y su tabla de a qué skill derivar. El PASO 6 (Canva) queda para cuando la persona da un link de Canva.
**Nano Banana:** si el índice marca 2 o más arreglos para esa ficha, o si la slide lleva más de ~25 palabras o una lista, no le pidas el texto al modelo de imagen: texto en HTML (motor A) o fondo IA sin texto + texto encima (motor C).

---

## PASO 4 — Entregar el guion completo slide por slide

Para cada slide, entrega exactamente este formato:

```
---
### SLIDE [N] — [Nombre del slide]

**TEXTO PRINCIPAL:**
[El texto exacto que va en el slide — máximo 40-60 palabras]

**DISEÑO:**
*(Usar los valores del Perfil Visual de Marca cargado en PASO 0. Si no hay perfil, usar valores por defecto: Bebas Neue para títulos, Garet para cuerpo, fondo negro/blanco, acento naranja.)*
- Tipografía: [Fuente de títulos del perfil + tamaño sugerido / Fuente de cuerpo del perfil]
- Elemento de énfasis: [Elemento de énfasis del perfil: subrayado / círculo / highlight / bold]
- Layout: [Layout base del perfil: texto centrado / izquierda / derecha]
- Color de fondo: [Color de fondo del perfil para slides interiores]
- Color de texto: [Color de texto del perfil]
- Color de énfasis: [Color de énfasis del perfil para palabras clave]
- Emoji: [cuál y dónde según el estilo del perfil, o "ninguno"]

**INSTRUCCIÓN CANVA:**
[Instrucción específica paso a paso usando los valores exactos del Perfil Visual de Marca]
---
```

**Reglas de escritura del guion:**

- **Slide 1 (gancho) tiene estructura fija e inamovible:**
  - La imagen ocupa el **60% superior o central** del slide
  - El texto ocupa el **40% restante** (franja inferior o superpuesto sobre la imagen)
  - El texto es mínimo: **máximo 6-8 palabras** — solo el gancho principal, sin subtítulo ni cuerpo de texto
  - @usuario siempre visible, pequeño, en la parte superior
  - Layout visual obligatorio:
  ```
  ┌─────────────────────────────┐
  │   @usuario  (pequeño, top)  │
  │                             │
  │        IMAGEN               │
  │      (60% del slide)        │
  │                             │
  │─────────────────────────────│
  │  GANCHO EN 1-2 LÍNEAS       │  ← máx. 6-8 palabras, tipografía grande
  │                         →   │
  └─────────────────────────────┘
  ```

- **Slides interiores (2 en adelante) deben ser SOLO TEXTO** — sin grillas de íconos, sin elementos decorativos fijos. Esto garantiza compatibilidad total con edición automática vía Canva MCP. Los íconos de línea fijos no son reemplazables programáticamente.

- **⚠️ ADVERTENCIA DE TEMPLATE:** Antes de iniciar la construcción en Canva (PASO 6), verificar que el template del usuario NO tenga grillas de íconos de línea en los slides interiores. Si las tiene, advertirlo explícitamente y pedirle un template texto-only antes de continuar. Un template compatible tiene esta estructura en slides interiores:
  ```
  ┌─────────────────────────────┐
  │  TÍTULO GRANDE              │
  │                             │
  │  Texto de apoyo             │
  │  en 1-2 líneas              │
  │                             │
  │  Frase de cierre            │
  │                         →   │
  └─────────────────────────────┘
  ```

- Cada slide tiene UNA sola idea
- El texto debe leer solo, sin depender de la imagen
- Progresión lógica: cada slide hace querer ver el siguiente
- Slide final siempre termina con CTA específico y directo

---

## PASO 5 — Generar imagen gancho con Nanobanana (Gemini)

El slide 1 (gancho) necesita una imagen generada con IA. La herramienta es el **skill banana** (`skills/banana`), que usa la API de Gemini (Nano Banana 2 — `gemini-3.1-flash-image-preview`).

### 5.1 — Construir el prompt con la fórmula de 5 componentes

**NO pasar una descripción genérica.** Construir el prompt siguiendo los 5 componentes del skill banana:

| Componente | Peso | Qué incluir |
|------------|------|-------------|
| **Sujeto** | 30% | Elemento visual principal: persona con rasgos específicos, objeto con material/textura, escena con detalle |
| **Acción** | 10% | Verbo presente fuerte: "mira fijamente", "sostiene", "emerge desde" |
| **Contexto** | 15% | Ubicación + hora + atmósfera: "estudio oscuro a las 2am", "ciudad al amanecer" |
| **Composición** | 10% | Ángulo + encuadre: "plano medio bajo", "primer plano extremo", "toma aérea" |
| **Estilo + Luz** | 25% | Cámara real + focal + diafragma + iluminación + referencia de publicación |

**Reglas obligatorias (del skill banana):**
- NUNCA usar: "fotorrealista", "8K", "ultra detallado", "masterpiece" — degradan la calidad
- SIEMPRE nombrar cámara real: "Sony A7R IV", "Canon EOS R5", "iPhone 16 Pro Max"
- SIEMPRE especificar focal: "85mm f/1.4", "24mm gran angular"
- Usar anclas de prestigio: "editorial Vogue", "portada National Geographic", "WIRED magazine"
- La imagen NO debe tener texto (el texto se superpone en Canva)
- Usar la paleta de colores del Perfil Visual de Marca cargado en PASO 0
- Formato 4:5 para cubrir el slide completo, o 1:1 si solo es elemento superior

**Plantilla de prompt:**
```
[Sujeto específico con edad/material/textura], [acción con verbo fuerte]
en [ubicación concreta + hora del día]. [Micro-detalle visual].
Captado con [cámara real], lente [focal] a [diafragma], [iluminación].
Paleta: [colores del perfil de marca].
Composición vertical limpia. Estilo editorial [referencia de publicación].
NEVER include any text or watermarks.
```

**Ejemplo aplicado (tema: productividad):**
```
A focused 28-year-old woman with sharp cheekbones and dark hair pulled back,
staring intensely at a glowing laptop screen in a minimal dark studio at 2am.
Blue light casting cool shadows across her face, single warm desk lamp behind.
Shot on Sony A7R IV, 85mm f/1.4 lens, shallow depth of field.
Deep navy and charcoal tones with warm amber accent. Clean vertical composition.
WIRED magazine editorial aesthetic. NEVER include any text or watermarks.
```

### 5.2 — Generar la imagen (cadena de herramientas)

Intentar en este orden exacto:

#### Opción A — MCP nanobanana (si las herramientas están activas en la sesión)

Si los tools `gemini_generate_image`, `set_aspect_ratio` etc. están disponibles:

```
set_aspect_ratio("4:5")
gemini_generate_image(prompt="[prompt de 5.1]", imageSize="2K")
```

#### Opción B — Script directo via bash (fallback principal)

```bash
API_KEY="$GEMINI_API_KEY"

GOOGLE_AI_API_KEY="$API_KEY" python3 skills/banana/scripts/generate.py \
  --prompt "[prompt de 5.1]" \
  --aspect-ratio "4:5" \
  --resolution "2K" \
  --model "gemini-3.1-flash-image-preview"
```

La imagen se guarda en `entregables/imagenes/`.

#### Opción C — curl directo (si hay error SSL de Python)

```bash
API_KEY="$GEMINI_API_KEY"

curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d @- <<\'JSONBODY\' -o /tmp/gemini_hook_response.json
{
  "contents": [{"parts": [{"text": "[PROMPT]"}]}],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "imageConfig": {"aspectRatio": "4:5", "imageSize": "2K"}
  }
}
JSONBODY

python3 -c "
import json, base64
with open(\'/tmp/gemini_hook_response.json\') as f: data = json.load(f)
for part in data[\'candidates\'][0][\'content\'][\'parts\']:
    if \'inlineData\' in part:
        with open(\'entregables/imagenes/hook_carrusel.png\', \'wb\') as f:
            f.write(base64.b64decode(part[\'inlineData\'][\'data\']))
        print(\'Guardada: entregables/imagenes/hook_carrusel.png\')
"
```

#### Opción D — Canva AI integrado (último recurso sin API)

Dentro de Canva → Apps → "Texto a imagen" → usar el prompt de 5.1.

### 5.3 — Verificar y registrar costo

Después de una generación exitosa:
1. Abrir la imagen para verificar paleta de marca y emoción del gancho
2. Si tiene texto no deseado o colores incorrectos: ajustar prompt y regenerar (máx. 3 veces)
3. Registrar costo:
```bash
python3 skills/banana/scripts/cost_tracker.py log \
  --model "gemini-3.1-flash-image-preview" \
  --resolution "2K" \
  --prompt "hook_carrusel — [tema breve]"
```

### 5.4 — Colocar imagen en Canva

La imagen va como fondo del Slide 1 completo (aspect 4:5) o en el 60% superior (aspect 1:1).

1. Sube la imagen en Canva (`Subidas > Subir archivos`)
2. Para 4:5: insertar como fondo del slide; oscurecer si el texto necesita contraste
3. Para 1:1: insertar como elemento en el 60% superior, texto en franja inferior
4. Texto del gancho: tipografía grande, máx. 6-8 palabras
5. @usuario pequeño visible en la parte superior

---

## PASO 6 — Construir el carrusel directamente en Canva

**Este paso solo se ejecuta si el usuario proporcionó un enlace de Canva editable en PASO 0.6.**
Si el usuario eligió hacer el diseño él mismo, omitir este paso y continuar con PASO 7.

---

### 6.A — FLUJO PRINCIPAL: Canva MCP Connector (PREFERIDO)

**Verificar disponibilidad:** Si los tools `mcp__canva__*` (o con prefijo de Canva) están disponibles en el entorno, usar SIEMPRE este flujo. Es más rápido, más preciso y no depende de la interfaz visual del navegador.

#### Paso 6.A.1 — Extraer Design ID

Del URL del usuario: `https://www.canva.com/design/{DESIGN_ID}/...`
Ejemplo: `https://www.canva.com/design/DAHEly0BYWc/RC2ybuD9olRxDlDUVkQMVQ/edit` → `design_id = DAHEly0BYWc`

#### Paso 6.A.2 — Analizar estructura del diseño

```
get-design-pages(design_id)
→ Obtiene número de páginas y sus IDs

get-design-content(design_id, page_number=N)
→ Para cada página: element IDs, texto actual, posiciones
```

Mapear qué elementos de texto existen en cada página, sus IDs y contenido actual.

#### Paso 6.A.3 — Iniciar transacción de edición

```
start-editing-transaction(design_id)
→ Guardar el transaction_id devuelto
```

#### Paso 6.A.4 — Ejecutar todas las operaciones en bulk

Agrupar **TODAS las operaciones del carrusel en UN SOLO llamado** a `perform-editing-operations`.
No hacer múltiples llamadas individuales — una transacción bulk es más eficiente y atómica.

**Operaciones disponibles:**

| Operación | Parámetros clave | Uso |
|-----------|-----------------|-----|
| `replace_text` | page_number, element_id, new_text | Cambiar texto de un elemento existente |
| `format_text` | page_number, element_id, font_size, bold, italic, color, alignment | Formato tipográfico |
| `resize_element` | page_number, element_id, width, height | Cambiar dimensiones de un elemento |
| `position_element` | page_number, element_id, top, left | Mover elemento en el canvas |

**Ejemplo bulk (múltiples slides en una sola llamada):**
```json
[
  {"type": "replace_text", "page_number": 2, "element_id": "ABC", "new_text": "Texto slide 2..."},
  {"type": "format_text", "page_number": 2, "element_id": "ABC", "font_size": 54, "italic": true, "alignment": "center", "color": "#1A1A1A"},
  {"type": "replace_text", "page_number": 3, "element_id": "DEF", "new_text": "Texto slide 3..."},
  {"type": "format_text", "page_number": 3, "element_id": "DEF", "font_size": 54, "italic": true, "alignment": "center", "color": "#1A1A1A"},
  {"type": "resize_element", "page_number": 4, "element_id": "GHI", "width": 1080},
  {"type": "position_element", "page_number": 4, "element_id": "GHI", "top": 560, "left": 0}
]
```

#### Paso 6.A.5 — Verificar con thumbnails

```
get-design-thumbnail(design_id, page_number=N)
→ Para cada página modificada
```

Revisar visualmente que el contenido y formato se aplicaron correctamente antes de commitear.

#### Paso 6.A.6 — Confirmar con el usuario y hacer commit

Mostrar thumbnails al usuario y preguntar:
> "¿Se ve bien? ¿Hago commit para guardar los cambios de forma permanente?"

Si confirma → `commit-editing-transaction(transaction_id)`
Si hay problemas → `cancel-editing-transaction(transaction_id)` → corregir → nueva transacción

#### Limitaciones del Canva MCP

| Lo que NO puede hacer el MCP | Solución manual para el usuario |
|-------------------------------|----------------------------------|
| Agregar páginas nuevas | Clic en "+" en panel de páginas |
| Cambiar color de fondo de página | Clic en fondo → seleccionar color |
| Cambiar familia tipográfica | Seleccionar texto → menú fuente |
| Insertar elementos nuevos (texto, íconos) | Panel Elementos o Texto |

Para slides que requieren nueva página o cambio de fondo (ej: CTA con fondo negro), dar instrucciones claras al usuario para que lo haga manualmente, y continuar con el MCP para el contenido textual.

---

### 6.B — FLUJO FALLBACK: Claude in Chrome (cuando MCP no está disponible)

Usar solo si el Canva MCP connector **NO está activo** en la sesión.

#### Paso 6.B.1 — Abrir el diseño

1. Navega al enlace de Canva del usuario (debe terminar en `/edit`)
2. Espera a que cargue el editor completamente
3. Verifica que sea editable (no en modo solo lectura)

#### Paso 6.B.2 — Construir cada slide

**Para slides interiores:**
1. Clic en el elemento de texto → triple-clic para seleccionar todo → escribir nuevo contenido
2. Tamaño de fuente: clic en el campo numérico (NO en +/–) → Ctrl+A → escribir tamaño → **Tab para confirmar (NUNCA Enter)**
3. Alineación/estilo: Ctrl+Shift+C (centrar), Ctrl+B (negrita), Ctrl+I (cursiva)
4. Mover elementos: panel Posición (Ctrl+Shift+P) → ingresar coordenadas

**Precauciones Chrome:**
- NUNCA Enter para confirmar tamaño de fuente → agrega línea nueva al texto
- SIEMPRE desbloquear ratio antes de cambiar dimensiones
- Si se activa herramienta IA accidentalmente → Escape múltiple veces

---

### 6.C — CHECKLIST DE VERIFICACIÓN (aplica a ambos flujos)

- [ ] Slide 1: imagen de fondo, título visible, @username arriba, botón swipe abajo derecha
- [ ] Slides interiores: texto centrado, tamaño correcto, fondo del perfil de marca
- [ ] Slide CTA: fondo de acento, texto contrastado, palabra clave en color de énfasis
- [ ] Fuentes consistentes en todo el carrusel
- [ ] Sin cajas, bordes o fondos blancos en slides intermedios
- [ ] @username en todos los slides excepto CTA
- [ ] Botón swipe en todos los slides excepto CTA

### 6.D — Confirmar al usuario

> "✅ Carrusel construido en Canva. Revísalo en: [enlace]. Tienes [N] slides listos. Exporta desde `Compartir → Descargar` como JPG/PNG o PDF con páginas."

---

## PASO 7 — Entregar caption para el post

Después de los slides, entrega también el caption optimizado:

```
**CAPTION SUGERIDO:**
[Primera línea = gancho — igual o derivado del Slide 1]
[2-3 líneas de contexto o promesa]
[CTA específico]
.
.
.
[3-5 hashtags de nicho]
```

**Reglas del caption:**
- Primera línea visible sin "ver más": debe funcionar como gancho
- Máximo 1,500 caracteres para carruseles educativos
- Emojis al inicio de líneas, no en medio de oraciones
- CTA que refuerce el del último slide

---

## PASO 8 — Resumen ejecutivo de producción

Al final, entrega un resumen de acciones para que el usuario pueda producir de inmediato:

```
## ✅ CHECKLIST DE PRODUCCIÓN

**Imagen del gancho:**
- [ ] Imagen generada con Nanobanana (skill banana) — guardada en `entregables/imagenes/`
- [ ] Subir a Canva (si no se construyó en PASO 6)

**En Canva (1080 × 1350 px):**
*(Si el carrusel ya fue construido en PASO 6, este paso es de verificación final)*
- [ ] Slide 1: Colocar imagen de gancho + texto [TÍTULO] en fuente de títulos del perfil
- [ ] Slide 2: [descripción breve]
- [ ] Slide 3: [descripción breve]
- [ ] ... (un punto por slide)
- [ ] Slide final: CTA con fondo [color]

**Para publicar:**
- [ ] Exportar como JPG/PNG individual o PDF con páginas
- [ ] Caption listo arriba
- [ ] Agregar música en Instagram (opcional pero aumenta alcance)
- [ ] Publicar en horario óptimo (Martes/Jueves 9am o 6pm)
```

---

## PASO 9 — Generar calendario de contenido (30 días)

Después de entregar el carrusel completo, genera automáticamente un calendario de publicación de 30 días que extiende el contenido del carrusel a múltiples formatos y fechas.

### 8.1 — Principio base

El carrusel recién creado es la pieza ancla. A partir de él, se derivan:
- **Reels cortos** — cada slide interior puede convertirse en un reel de 15-30 segundos
- **Stories** — 3-5 historias que teasean el carrusel antes de publicarlo
- **Carruseles de seguimiento** — un segundo carrusel que profundiza en el punto más comentado
- **Post de texto** — reflexión personal relacionada con el tema del carrusel

### 8.2 — Formato del calendario

Entrega el calendario en esta tabla:

```
## 📅 CALENDARIO DE CONTENIDO — 30 DÍAS

**Semana 1 — Lanzamiento**
| Día | Formato | Tema/Gancho | Plataforma | Hora sugerida |
|---|---|---|---|---|
| Día 1 | Carrusel | [Gancho del carrusel recién creado] | Instagram | Mar/Jue 9am o 6pm |
| Día 2 | Story x3 | Teaser de los 3 puntos clave del carrusel | Instagram Stories | 10am |
| Día 3 | Reel 30s | [El tip más accionable del carrusel en formato reel] | Instagram / TikTok | 6pm |
| Día 5 | Post texto | Reflexión personal sobre [tema del carrusel] | Instagram | 12pm |
| Día 7 | Story encuesta | "¿Cuál de estos puntos te resultó más útil?" | Instagram Stories | 11am |

**Semana 2 — Profundización**
| Día | Formato | Tema/Gancho | Plataforma | Hora sugerida |
| Día 10 | Reel 60s | Desarrolla el punto #[N más importante] del carrusel | Instagram / TikTok | 6pm |
| Día 12 | Carrusel 2 | [Tema derivado — el punto que más generó preguntas] | Instagram | 9am |
| Día 14 | Story detrás | "El proceso de crear este contenido" | Instagram Stories | 3pm |

**Semana 3 — Engagement y repurpose**
| Día | Formato | Tema/Gancho | Plataforma | Hora sugerida |
| Día 17 | Reel 15s | Hook de una sola línea del carrusel con texto animado | TikTok / Reels | 6pm |
| Día 19 | Post Q&A | Responde las preguntas más frecuentes del carrusel | Instagram | 9am |
| Día 21 | Carrusel mini | Versión de 5 slides con resumen del carrusel original | Instagram | 6pm |

**Semana 4 — Cierre y próxima pieza**
| Día | Formato | Tema/Gancho | Plataforma | Hora sugerida |
| Día 24 | Reel detrás | Resultados y métricas del carrusel (si hay datos) | Instagram / TikTok | 6pm |
| Día 28 | Story serie | Serie de 5 stories con cada punto del carrusel (1/día) | Instagram Stories | 10am |
| Día 30 | Carrusel nuevo | [Nueva idea derivada de la conversación generada] | Instagram | 9am |
```

### 8.3 — Personalizar el calendario

Antes de entregarlo, reemplaza todos los placeholders `[...]` con:
- El gancho real del carrusel que acabas de crear
- Los 3 puntos más fuertes del carrusel como piezas individuales
- Una idea de carrusel de seguimiento basada en el tema

### 8.4 — Nota de uso

Incluye siempre este bloque al final del calendario:

```
💡 **Cómo usar este calendario:**
- Graba los reels en un solo día de producción (batch)
- Crea las stories como extensión natural del carrusel
- El Día 30 ya tiene lista la siguiente idea — el ciclo nunca para
- Ajusta horarios según tus analytics de Instagram (Insights → Audiencia → Horas activas)
```

---

## CRITERIOS DE CALIDAD

Antes de entregar, verifica:

- [ ] ¿Se eligió uno de los 37 formatos (o se dijo por qué ninguno encaja) y se respeta su anatomía y su error típico?
- [ ] ¿El gancho genera curiosity gap real? ¿Hay una razón urgente para deslizar?
- [ ] ¿El gancho está validado por al menos 1-2 referencias virales encontradas en investigación?
- [ ] ¿Cada slide tiene UNA sola idea?
- [ ] ¿El texto de cada slide funciona sin la imagen?
- [ ] ¿Las instrucciones de Canva son específicas y accionables?
- [ ] ¿El prompt de imagen usa la fórmula de 5 componentes del skill banana (sujeto, acción, contexto, composición, estilo+luz)?
- [ ] Si el usuario dio link de Canva: ¿se construyó el carrusel completo slide por slide?
- [ ] ¿El CTA final es específico (pide una acción concreta, no genérica)?
- [ ] ¿El caption tiene la primera línea como gancho independiente?

---

## NOTAS IMPORTANTES

- **La investigación no es opcional.** Un gancho sin validación viral es una apuesta ciega. Siempre busca referencias antes de proponer el gancho final.
- **El Slide 1 vale el 80% del carrusel.** Si el gancho no detiene el scroll, nadie ve el resto. Invertir el mayor tiempo de diseño en esta diapositiva.
- **Imagen del gancho — prioridad de herramientas (ver PASO 5 para comandos exactos):**
  1. **MCP nanobanana** — si los tools `gemini_generate_image` / `set_aspect_ratio` están activos en la sesión
  2. **Script banana** — `GOOGLE_AI_API_KEY=... python3 skills/banana/scripts/generate.py` (API key en la variable de entorno `GEMINI_API_KEY`)
  3. **curl directo** — si hay error SSL de Python (ver Opción C en PASO 5)
  4. **Canva AI integrado** — Apps → "Texto a imagen" (sin API key, último recurso)
  - Siempre construir el prompt con la fórmula de 5 componentes del skill banana (NUNCA prompt genérico)
  - Registrar costo con `cost_tracker.py log` después de cada generación exitosa
- **Construcción en Canva (PASO 6):** Verificar SIEMPRE si el **Canva MCP Connector** está activo (tools con prefijo Canva disponibles en el entorno). Si sí → usar flujo 6.A (MCP). Si no → usar flujo 6.B (Chrome). El MCP es más rápido, preciso y confiable.
- **Operaciones Canva MCP en bulk:** Agrupar TODAS las operaciones del carrusel en UN SOLO llamado a `perform-editing-operations`. No hacer llamadas individuales por slide.
- **Limitaciones MCP:** No puede agregar páginas, cambiar fondos de página ni cambiar tipografía. Estas acciones se delegan al usuario con instrucciones claras.
- **Slides interiores = simples.** Tipografía sobre el fondo del perfil de marca. NO sobreproducir — los slides interiores son para comunicar, no para impresionar visualmente.
- **TikTok MCP:** Si `davibauer/tiktok-mcp` está disponible, úsalo en PASO 2 para obtener datos de engagement reales. Si no, WebSearch es válido como fallback.
- **Si el input es un guion de reel:** identifica el gancho verbal del reel (los primeros 3 segundos) y conviértelo en gancho visual del Slide 1. El resto del guion se distribuye en slides interiores.
- **El calendario (PASO 9) es automático** — se entrega siempre después del guion, sin que el usuario lo pida. Es parte del entregable estándar.
- **El Perfil Visual (PASO 0) se verifica en cada sesión.** Si `references/design_profile.md` tiene el placeholder `[PERFIL NO CONFIGURADO]`, disparar el setup. Si tiene contenido real, cargarlo sin preguntar nada y continuar.
- **Leer siempre** `references/design_profile.md` al inicio de cada sesión (el sistema visual de la marca vive ahí) y `references/formatos-carrusel-35.md` en el PASO 3 (los 37 formatos; se regenera desde el recetario, no se edita a mano).
