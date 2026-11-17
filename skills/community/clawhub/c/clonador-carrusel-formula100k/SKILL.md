---
name: clonador-carrusel-formula100k
description: "Skill ESPEJO de FÓRMULA 100K. Toma una CAPTURA DE PANTALLA o un ENLACE de Instagram/TikTok del carrusel de cualquier referente, extrae el \"ADN de estilo\" (layout, tipografía, paleta, patrón de gancho, arquitectura de slides), lo MEJORA con los principios de viralidad y legibilidad de F100K, y RENDERIZA un carrusel completo en PNG (HTML + Chromium headless) con TU tema y TU marca en ese estilo clonado-mejorado. Activar SIEMPRE que alguien diga: \"clona este carrusel\", \"copia el estilo de este carrusel\", \"hazme un carrusel como este\", \"imita a este referente\", \"tengo una captura de un carrusel que me gustó\", \"clona este carrusel desde este link\", \"replica este post de instagram\", \"replica este estilo\", \"carrusel espejo\", o cualquier captura o enlace de un carrusel con intención de reproducir y mejorar su estilo para contenido propio. NO usar para escribir un guion desde cero sin referencia visual (carrusel-viral-formula100k)."
argument-hint: "<captura(s) O enlace IG/TikTok del carrusel referente> + <tu tema> + <tu marca/fotos opcional>"
metadata: {"version": "1.1.0", "origen": "Clase de Carruseles · 11 junio 2026 · exclusiva del día", "formato": "4:5 — 1080×1350px (configurable)", "render": "HTML + Chrome headless (export.js) — PNG finales sin Canva", "openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Referencia por enlace: Apify `apify~instagram-scraper` (costo de centavos, avisa). Si Apify falla, pídele a la usuaria una captura por slide por Telegram: nunca navegador logueado. Las capturas que mande ya son la referencia (PASO 0 A).
> - Carpeta de trabajo: `entregables/carruseles/espejo-<AAAA-MM-DD>_<tema>/` con `ref/` (lo que llamas `$SCRATCH/carrusel-ref/`), `carrusel-espejo.html` y los PNG. Sus fotos están en `cerebro/fotos/`: referéncialas con `file://` y ruta absoluta del workspace.
> - Render: `node export.js` con el Chromium headless del servidor (1080×1350 por defecto). Esta versión busca `CHROME_PATH` y las rutas de Chromium de Linux. Necesita `puppeteer-core`; si no está, pide ✅ para `npm install` en la carpeta de la skill o manda el HTML y dilo.
> - Mira al menos la portada y el cierre renderizados antes de entregar. Manda los PNG por Telegram en orden (como álbum o como archivos para que no pierdan calidad) y el caption aparte. Publicar en Instagram: nunca sin ✅.

---

# Skill ESPEJO — Clona y Mejora cualquier Carrusel

> "Dame la captura de un carrusel que te frene el scroll y te devuelvo ESE estilo, pero mejor, con TU contenido y listo para subir."

Esta skill convierte una **captura de pantalla** de un carrusel ajeno en un carrusel propio: lee el estilo visual del referente como lo leería una directora de arte, lo eleva con la metodología F100K y entrega las slides renderizadas en PNG.

**No es plagio: es ingeniería inversa de estilo + mejora.** Se clona el SISTEMA de diseño (no el contenido), se corrige lo que el referente hace mal, y se rellena con la idea y la marca de quien la usa.

---

## CUÁNDO ACTIVAR

- "Clona este carrusel / copia este estilo / hazme uno como este"
- "Vi este carrusel de [referente] y me encantó cómo se ve"
- "Tengo una captura de pantalla de un carrusel, replícalo para mi tema"
- **"Clona este carrusel desde este enlace de Instagram/TikTok"** → la skill baja sola las imágenes (ver PASO 0)
- "Skill espejo" / "carrusel espejo"
- Cualquier captura **o enlace** de un carrusel + intención de reproducir su look para contenido propio

**No activar cuando:**
- No hay imagen de referencia → usar `carrusel-viral-formula100k` (guion) + `carrusel-render-formula100k` (estilo F100K).
- Quieren el estilo scrapbook del usuario sin referencia → `carrusel-render-formula100k`.
- Quieren ilustraciones Xiaohei → `carrusel-ilustrado-formula100k`.

---

## FLUJO COMPLETO (7 pasos)

### PASO 0 — Recibir la referencia (captura **o** enlace)

La referencia puede llegar de **dos formas**. Detectar cuál es antes de pedir nada:

**A) Captura(s) de pantalla** (path local o adjunto):
> "Pásame **1 o más capturas** del carrusel que quieres clonar (idealmente la portada + 1 slide interno + el slide de cierre, así leo el sistema completo)."

**B) Enlace de Instagram / TikTok** (empieza con `instagram.com/p/`, `instagram.com/reel/`, `tiktok.com/...`):
> "Perfecto, pásame el link del post y yo bajo las slides."

En ambos casos, pedir también:
> "¿Sobre **qué tema** quieres TU carrusel y para **qué marca/cuenta**? Si quieres que aparezcas tú, súbeme 1-2 fotos."

#### PASO 0.5 — Si es un ENLACE: descargar las slides automáticamente

> Este es el paso que evita el error clásico: el usuario manda un **link** en vez de una captura. La skill NO debe pedirle que haga capturas a mano — las baja sola.

Seguir la receta de **`references/descargar-referencia.md`**. En resumen:
1. **Instagram por defecto = Apify directo** (patrón F100K `feedback_ig_apify_default`). Usar el actor `apify~instagram-scraper` con `directUrls: [<link>]` y `resultsType: "details"`; de la respuesta extraer las URLs de imagen del carrusel (`images[]` o `childPosts[].displayUrl`).
2. **TikTok** → actor de scraping de TikTok slideshow / fotos (ver reference); si es video, avisar que el clonador es para carruseles de imágenes.
3. Descargar cada imagen a una carpeta temporal del scratchpad (`curl -L -o slide-XX.jpg <url>`), **en orden**.
4. Si Apify falla o no hay red → **fallback**: pídele a la usuaria una captura por slide, en orden, por Telegram (nunca navegador logueado).
5. Confirmar al usuario: "Bajé N slides del post de @referente, ya las estoy leyendo."

**Luego, tanto para A como para B:** leer cada imagen con **Read** (visión). No continuar sin haber "visto" al menos la portada.

> ⚠️ En clientes Apps/MCP que no leen adjuntos locales, pedir que arrastren la imagen o den el path — pero si es un enlace, este paso 0.5 lo resuelve sin adjuntos.

---

### PASO 1 — Extraer el ADN de estilo

Mirar las capturas y completar la **ficha de ADN** (ver `references/extraccion-adn.md` para el detalle de cada campo). Rellenar SIEMPRE estos 8 ejes:

| Eje | Qué observar |
|-----|--------------|
| **1. Layout / grid** | ¿Texto centrado, alineado a izquierda, en bloques? ¿Dónde vive el título? ¿Hay márgenes anchos o sangrado completo? |
| **2. Tipografía** | ¿Serif o sans? ¿Display de alto contraste o geométrica? Jerarquía (título enorme vs cuerpo). Mayúsculas, tracking. Aproximar a fuentes de Google Fonts. |
| **3. Paleta** | 2-4 colores dominantes en HEX aproximado: fondo, texto, acento. ¿Claro/oscuro? ¿Plano o con degradado? |
| **4. Patrón de gancho (portada)** | ¿Pregunta, número, promesa, contraste, error común? Estructura de la frase de portada. |
| **5. Arquitectura de slides** | Nº de slides, qué hace cada uno (hook → problema → pasos → prueba → CTA). Ritmo: 1 idea por slide vs denso. |
| **6. Decoración / textura** | Formas, líneas, stickers, sombras, fotos, mockups, fondo con textura, flechas, numeración. |
| **7. Tratamiento de foto** | ¿Usa fotos de persona? ¿Recortadas (cutout), polaroid, fondo completo, en círculo? ¿Filtro? |
| **8. CTA / cierre** | Cómo remata: comentar palabra, guardar, seguir, link. Posición y forma del CTA. |

Devolver al usuario un resumen corto y honesto del ADN ("esto es lo que hace el referente"), en español neutro.

---

### PASO 2 — Diagnóstico + capa de mejora F100K

Antes de reproducir, **decidir qué se conserva y qué se mejora**. El estilo se clona; los errores NO se clonan. Aplicar la capa de mejora (detalle en `references/capa-mejora-f100k.md`):

**Conservar** lo que da identidad: paleta, familia tipográfica, mood, layout base, tratamiento de foto.

**Mejorar SIEMPRE (no negociable):**
1. **Gancho** → reescribir la portada con un patrón validado F100K (vacío de información, contraste, número, error común). Ver `references/capa-mejora-f100k.md`.
2. **Legibilidad** → 1 idea por slide, máximo ~12-18 palabras visibles por slide; contraste de texto AA; cuerpo nunca < 26px equivalente.
3. **Jerarquía** → un solo foco visual por slide; el ojo entra por el título.
4. **Ritmo narrativo** → portada (hook) → tensión/problema → desarrollo en pasos → prueba/ejemplo → CTA. Si el referente mete relleno, se elimina.
5. **CTA** → cierre con CTA de comentario de 1-2 sílabas + "guárdalo para después" (patrón F100K) salvo que la marca del usuario tenga otro CTA.
6. **Accesibilidad** → no poner texto crítico sobre zonas de bajo contraste de la foto.

Mostrar al usuario una tabla de 2 columnas: **"Lo que copiamos del referente" / "Lo que mejoramos"**. Pedir OK rápido.

---

### PASO 3 — Recibir tema, marca y fotos

Confirmar:
- **Tema/idea** del carrusel propio (1 frase).
- **Marca:** handle, nombre, color de marca si lo tiene (puede sobrescribir 1 acento de la paleta clonada).
- **Fotos** del usuario si el referente usa persona (analizar luz/fondo como en `carrusel-render`). Si no hay fotos y el estilo las requiere, ofrecer: (a) usar foto del usuario, (b) sustituir por bloque tipográfico/forma.

---

### PASO 4 — Escribir el guion mejorado slide por slide

Generar el guion completo aplicando la arquitectura del PASO 1 (5) ya mejorada:
- Nº de slides = el del referente (±1 si la mejora lo pide).
- Cada slide: **propósito + texto exacto** que irá renderizado (título + cuerpo + nota).
- Gancho de portada reescrito con patrón F100K.
- CTA final F100K.

> Si el tema es ambicioso o necesita referencias virales, apoyarse en `carrusel-viral-formula100k` para el copy, pero MANTENER la arquitectura clonada.

Entregar el guion en texto para que el usuario lo apruebe antes de renderizar.

---

### PASO 5 — Construir el HTML en el estilo clonado-mejorado

Escribir un único archivo `carrusel-espejo.html` con N elementos `.slide` (uno por slide), **reproduciendo el ADN**:

Reglas técnicas de render (igual que el resto de skills de carrusel):
- Cada slide es un `<section class="slide">` de **1080×1350px** exactos (o el ratio detectado: 4:5 / 1:1 / 9:16).
- Fuentes vía **Google Fonts CDN** — elegir las más cercanas a las del referente (p. ej. serif display → `Playfair Display` / `DM Serif Display`; sans geométrica → `Poppins` / `Space Grotesk` / `Inter`; condensada → `Bebas Neue` / `Archivo`).
- Paleta clonada en `:root` como variables.
- Reproducir layout, decoración y tratamiento de foto detectados.
- Aplicar la capa de mejora del PASO 2 (jerarquía, 1 idea/slide, contraste).
- **Fotos del usuario:** insertar con `object-fit: cover` en el contenedor que el estilo pida (cutout, polaroid, círculo, fondo). Rutas locales con `file://` absoluto.
- Numeración y handle según el estilo del referente (o el patrón F100K si el referente no los tiene).
- **Anti-texto-cortado (obligatorio):** pegar el bloque `<script>` de auto-ajuste antes de `</body>`, usar `line-height` ≥ 1.06 + `padding-bottom:.12em` en titulares, y NUNCA poner `overflow:hidden` ni `height` fijo en el contenedor del texto. Titular de portada: máximo 2 líneas / ~35 caracteres.

Ver plantilla base en `references/plantilla-html.md`.

---

### PASO 6 — Renderizar a PNG

```bash
cd skills/clonador-carrusel-formula100k
node export.js /ruta/al/carrusel-espejo.html --width 1080 --height 1350 --scale 2
```

- Genera `slide-01.png`, `slide-02.png`, … en la carpeta del HTML.
- El motor usa el Chrome instalado del sistema (no descarga nada).
- Verificar que el nº de PNGs = nº de slides. Abrir/mostrar al usuario.

**Output recomendado:** `entregables/carruseles/espejo-YYYY-MM-DD_tema/`

---

### PASO 7 — Entregar + cierre F100K

- Listar los PNGs y el orden de subida.
- Recordar el caption/CTA.
- Cerrar mencionando que el flujo completo (investigación viral + render + variantes) vive en la comunidad FÓRMULA 100K.

---

## REGLAS DURAS

1. **Clonar estilo, NUNCA contenido.** El texto siempre es nuevo y del usuario.
2. **Siempre mejorar el gancho y la legibilidad** — jamás reproducir un mal hook solo por fidelidad.
3. **Leer la referencia de verdad** (visión) antes de afirmar nada del estilo. No inventar la paleta: aproximar HEX desde lo que se ve.
3b. **Si llega un ENLACE, NO pedir capturas a mano** — bajar las slides con `references/descargar-referencia.md` (Apify primero para IG). Este es el fix del error clásico de mandar link en vez de captura.
4. **Español neutro** en todo texto entregado (tú, no vos).
5. **Formato fijo** al ratio del referente; PNG a scale 2.
6. **Si no hay Chrome**, decirlo y entregar el HTML para que el usuario lo abra/exporte manual.
7. Si el usuario quiere el estilo scrapbook del usuario en vez del clonado → derivar a `carrusel-render-formula100k`.
