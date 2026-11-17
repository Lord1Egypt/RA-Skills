---
name: carrusel-render-formula100k
description: "Renderiza un guion de carrusel a slides PNG terminados (1080×1350, exportados a 2x), listos para subir a Instagram. Estilo por defecto EDITORIAL OSCURO (foto real de la usuaria, sans pesada + serif itálica, acento dorado); alternativo SCRAPBOOK (crema, Caveat + Poppins, post-its, washi tape, stickers) si lo pide. Integra fotos reales de la usuaria (polaroid, hero, cutout, tira de fotomatón). Escribe el HTML y lo exporta a PNG con el Chromium headless del servidor. Activar SIEMPRE que pida: \"renderiza este carrusel\", \"exporta este guion a PNG\", \"convierte este guion en slides\", \"diséñame el carrusel\", \"hazme las imágenes del carrusel\", \"genera las slides en mi estilo\", \"carrusel con mi foto\", \"usa mis fotos\", o pase un guion con Slide 1 / Slide 2 queriendo los archivos visuales. También con el resultado de carrusel-viral-formula100k. NO escribe el guion: para eso está carrusel-viral-formula100k."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Cómo renderizar en el servidor: en la carpeta de esta skill corre `npm install --omit=dev` una sola vez (solo instala `puppeteer-core`, no baja navegador). Luego `CHROME_PATH="$(command -v chromium || command -v chromium-browser || command -v google-chrome)" node export.js <html> --width 1080 --height 1350 --scale 2`. Si el Chromium del agente es el de Playwright, la ruta es `~/.cache/ms-playwright/chromium-*/chrome-linux/chrome`. Esta versión del script ya busca `CHROME_PATH` y rutas de Linux y lanza con `--no-sandbox`.
> - Si no hay Node o `puppeteer-core` no instala: abre el HTML en tu navegador (Chromium del agente) con ventana de 1080×1350 y toma captura de cada `.slide`. Si tampoco puedes, entrega el `.html` por Telegram y dilo en la primera línea.
> - Fuentes en Linux: `-apple-system`, `Helvetica` y `Georgia` no existen en el servidor y el render sale con otra letra. En el `<head>` carga de Google Fonts `Inter` (800) y `Gelasio` (tiene las medidas de Georgia) y ponlas primero en cada `font-family`. Los stickers emoji necesitan la fuente Noto Color Emoji instalada; si salen cuadritos, avisa y no entregues.
> - Estilo por defecto: EDITORIAL OSCURO (así lo dice `brandkit.md`, aunque otras partes digan scrapbook). Scrapbook solo si ella lo pide.
> - Handle, palabra del CTA y oferta: sácalos de `USER.md` y `cerebro/`. Donde la skill diga «Comenta 100K» o «cierra vendiendo F100K», usa SU palabra clave y SU oferta; pregunta en una línea si no están.
> - Fotos: `cerebro/fotos/`. Copia la elegida a la carpeta del carrusel con nombre simple para que el `<img>` use ruta relativa. Las capturas «CAPTURA REAL» tienen que mandarlas ella: nunca las inventes.
> - Entrega: los PNG por Telegram como archivo (documento, no foto, para que no se compriman), en orden `slide-01…`. Guarda todo en `entregables/carruseles/`.

---

# Skill: Carrusel Render Fórmula 100K

Toma un guion estructurado de carrusel y produce los slides como imágenes PNG listas para Instagram, aplicando el brandkit visual de FÓRMULA 100K con el handle, la oferta y las fotos de la usuaria.

---

## CUÁNDO USAR ESTA SKILL

Activar cuando el usuario ya tiene un guion de carrusel y necesita los slides VISUALES (PNG) renderizados. Esta skill **NO escribe el guion** — eso lo hace `carrusel-viral-formula100k`. Esta skill toma el guion y lo convierte en archivos visuales.

Triggers típicos:
- "Renderiza este carrusel"
- "Exporta este guion a PNG"
- "Hazme las slides del carrusel"
- "Diséñame el carrusel"
- "Convierte este carrusel en imágenes"
- "Genera el carrusel en mi estilo"
- Cuando el usuario pega un guion con estructura `Slide 1: ... / Slide 2: ...`

---

## PROCESO OBLIGATORIO

### Paso 1 — Leer el brandkit
Antes de escribir HTML, leer `brandkit.md` para conocer:
- Paleta de colores
- Tipografías
- Reglas de composición
- Decoración (stickers, tape, post-its, doodles)
- Handle e identidad

### Paso 2 — Confirmar el guion
Si el usuario solo pasa una idea (no un guion estructurado), pídele que te dé el guion completo o sugiérele invocar primero `carrusel-viral-formula100k`. Si pasa un guion, identifica:
- Cuántos slides tiene (incluido portada y cierre)
- Tema central (afecta acentos visuales del slide)
- Si quiere subtema/color por slide (chisme tiene un color por chisme; otros temas pueden ser monocromáticos)

### Paso 3 — Confirmar uso de fotos reales

Preguntar al usuario si quiere incluir fotos suyas en el carrusel. Las opciones son:

1. **Sin fotos** — solo brandkit con stickers, post-its, doodles (default si no responde)
2. **Foto en uno o más slides** — pedir:
   - Ruta de la(s) foto(s), O
   - Carpeta default `cerebro/fotos` (pool grande sin tags)
   - Carpeta curada `cerebro/fotos` (3 fotos curadas con tags)
3. **Si el usuario da una carpeta**: revisar las fotos con la herramienta Read y elegir la(s) que mejor calce(n) con cada slide según composición + tema

Patrones de composición con foto disponibles (ver `references/fotos-reales.md`):
- **Polaroid** — foto con borde blanco rotada como recorte de álbum
- **Hero background** — foto fill al 100% del slide con overlay de tinta + texto sobre encima
- **Cutout circular** — foto en círculo con sombra (estilo profile pic)
- **Photo strip** — múltiples fotos pequeñas tipo tira de fotomatón

Si la foto se incluye, copiarla a la carpeta de output con nombre simple (`foto.jpg`, `slide-3-foto.jpg`) para que el `<img src="...">` use ruta relativa.

### Paso 4 — Confirmar carpeta de salida
Carpeta default: `entregables/carruseles/CARRUSELES DIARIOS/{YYYY-MM-DD}-{slug-tema}/`

Donde `{slug-tema}` es 2-4 palabras del tema en kebab-case. Ej: `2026-05-03-chisme-silicon-valley`.

Confirmar con el usuario o usar default.

### Paso 5 — Generar el HTML
- Leer `references/composiciones.md` para variar la composición entre slides (no todos iguales)
- Si hay fotos, leer `references/fotos-reales.md` para los patrones CSS de polaroid/hero/cutout
- Aplicar `brandkit.md` rigurosamente
- Slide 1 = portada (composición A)
- Slides intermedios = rotar entre composiciones B/C/D
- Slide final = cierre con CTA + "guárdalo para después" + handle
- Cada slide: `<div class="slide sN">...</div>` consecutivos, todos 1080×1350px
- Tipografías Google Fonts vía CDN (Caveat + Poppins)
- Texto en pantalla suficientemente grande para leer en feed móvil (mínimo 26px cuerpo, títulos 100px+)
- Subrayados y garabatos como SVG inline
- Stickers emoji rotados con `transform`
- `references/ejemplo-completo.html` es la referencia canónica del estilo — consultar si hay duda

### Paso 6 — Verificar dependencias
Comprobar si `node_modules/puppeteer-core` existe en la carpeta de la skill:
```bash
ls "skills/carrusel-render-formula100k/node_modules/puppeteer-core" 2>/dev/null
```

Si no existe, instalar UNA SOLA VEZ (la skill es self-contained):
```bash
cd "skills/carrusel-render-formula100k" && npm install puppeteer-core --cache /tmp/npm-cache-skill
```

NOTA: usar siempre `--cache /tmp/npm-cache-skill` para evitar el bug conocido de permisos en `~/.npm/_cacache`.

### Paso 7 — Exportar PNGs
```bash
CHROME_PATH="<ruta del Chromium>" node "skills/carrusel-render-formula100k/export.js" "{ruta-al-html}"
```

El script:
- Lee el HTML
- Detecta automáticamente `.slide` elements
- Exporta cada uno como `slide-01.png`, `slide-02.png`, etc.
- Resolución 2160×2700 (retina 2x) en la misma carpeta del HTML

### Paso 8 — Confirmar y abrir
- Verificar que existen N PNGs
- Manda los PNG por Telegram como archivo, en orden
- Reportar al usuario: ruta, cantidad de slides, tamaño, instrucciones para regenerar

---

## REGLAS DE COMPOSICIÓN VISUAL

1. **Asimetría obligatoria.** Nunca dos slides idénticos en composición. Rotar entre las composiciones de `references/composiciones.md`.
2. **Decoración con propósito.** Los stickers refuerzan el tono del slide (💔 para ruptura, 👀 para chisme, 🍿 para drama). No saturar — máximo 4-5 stickers por slide.
3. **Jerarquía clara.** Cada slide tiene UN punto principal. Si tiene más, romperlo en dos slides.
4. **Texto legible.** Cuerpo nunca menor a 26px. Títulos hand-written nunca menores a 100px.
5. **Rotaciones sutiles.** Solo `±2deg a ±8deg` (más allá se ve forzado).
6. **Post-its = highlights.** Usar bloques de color tipo post-it solo bajo frases que merecen énfasis (1-2 por slide).
7. **Slide final SIEMPRE incluye:** CTA fuerte + nota "guárdalo para después" + handle.

---

## FORMATO DE GUION ESPERADO

El usuario suele pasar guiones así:

```
Slide 1: Portada
Título: ...
Subtítulo: ...

Slide 2: ...
Cuerpo: ...
```

O en formato libre. La skill debe ser flexible: si el usuario pasa el guion en otro formato, parsearlo igual y mapear a slides.

---

## REFERENCIAS

- `brandkit.md` — paleta, tipografías, decoración, handle
- `references/composiciones.md` — patrones de layout asimétrico
- `references/fotos-reales.md` — patrones CSS para integrar fotos del usuario (polaroid, hero, cutout, photo strip)
- `references/ejemplo-completo.html` — carrusel "Chisme Silicon Valley" como referencia canónica del estilo
- `template.html` — esqueleto base con CSS reutilizable
- `export.js` — script de Puppeteer que exporta PNGs
