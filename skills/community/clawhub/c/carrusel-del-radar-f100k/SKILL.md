---
name: carrusel-del-radar-f100k
description: "Del radar al post: toma el tema más fuerte que trajeron tus radares (tendencias, virales, noticias), elige la ficha del recetario de carruseles F100K que mejor sirve al objetivo, escribe el guion y el caption, te lo manda por Telegram para tu ✅, renderiza las slides en HTML → PNG con portada de Gemini, las revisa una por una, te las manda para el ✅ final y recién entonces las publica en tu Instagram profesional (Composio). Guarda el estado de cada carrusel para retomar cuando contestes, aunque sea horas después. Activar con: «corre el carrusel del radar», «carrusel del radar», «hazme un carrusel de [tema]», «convierte el radar en carrusel», «ensayo, no publiques», o cuando la usuaria conteste a un ✅ pendiente de esta skill (1, 2, 3, ✅, «publícalo», «cambia…»). También la dispara la automatización de lunes y jueves. NO publica nunca sin ✅, NO hace historias, reels ni el carrusel noticiero."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta skill **solo existe en el agente**: no tiene versión de escritorio.
> **Antes de seguir, lee la skill `f100k-puente`**: herramientas, rutas y reglas que no se negocian.
> Esta skill no reescribe ningún método: **orquesta** las que ya tienes instaladas y guarda el hilo
> entre un ✅ y el siguiente.

# Carrusel del radar

Un carrusel a la vez, de punta a punta, con dos compuertas de la usuaria:

```
radar → tema → ficha → guion + caption → ✅1 → render → revisión → ✅2 → publicar → link
```

Skills que usa (todas vienen en este paquete): `radar-tendencias-f100k` (si hace falta un radar),
`carrusel-formatos-f100k` (catálogo de fichas + `build.js`, que renderiza y revisa),
`carrusel-viral-formula100k` (método del guion), `f100k-puente` §3.1 (imagen con Gemini) y
`publicar-ig` (reglas de publicación). Las rutas `skills/<nombre>/` son las de tu instalación.

Mensajes exactos para Telegram: `references/mensajes-telegram.md`.
Forma del estado: `references/estado.schema.json`.

---

## Antes de todo: ¿hay un carrusel abierto?

Siempre, en cada invocación, antes que nada:

```bash
grep -lE '"paso": *"(esperando_ok_(guion|slides|no_quedo)|publicando)"' entregables/carruseles/*/estado.json 2>/dev/null
```

- **Hay uno y la usuaria está contestando** (1, 2, 3, 4, ✅, «publícalo», «cambia…», «corrige la slide…»):
  lee ese `estado.json` y sigue desde su `paso`, con la tabla de **ese** paso. No empieces otro.
  Si el paso es `esperando_ok_slides`, un número suelto **no** es aprobación para publicar (ver ✅2).
- **Hay uno en `publicando`:** una corrida anterior se cortó mientras publicaba. No vuelvas a
  publicar a ciegas: sigue la «Protección contra doble publicación» del Paso 6.
- **Hay uno y te disparó la automatización:** no abras otro. Manda el recordatorio de
  `mensajes-telegram.md` («Tienes un carrusel esperando…») y termina.
- **Hay uno de hace más de 7 días sin respuesta** (menos si está en `publicando`, que nunca se
  descarta sin revisar): pásalo a `descartado`, avísalo en una línea y sigue.
- **No hay ninguno:** empieza en el Paso 0.

Cada vez que cambies de paso, **escribe el `estado.json` antes de mandar el mensaje**. Si te
cortan a mitad de camino, el archivo dice dónde ibas.

---

## Paso 0 · Chequeo (no gasta nada)

```bash
node -v
CHROME="${CHROME_PATH:-$(command -v google-chrome-stable || command -v google-chrome || command -v chromium || command -v chromium-browser)}"; [ -x "$CHROME" ] && echo "chrome ok" || echo "falta chrome"
[ -d skills/carrusel-formatos-f100k/node_modules/puppeteer-core ] && echo "puppeteer ok" || echo "falta puppeteer"
[ -n "$GEMINI_API_KEY" ] && echo "gemini ok" || echo "falta GEMINI_API_KEY"
python3 -c "import PIL" 2>/dev/null && echo "pillow ok" || (command -v ffmpeg >/dev/null && echo "ffmpeg ok" || echo "falta pillow y ffmpeg")
```

Y en Composio: que exista la acción `INSTAGRAM_POST_IG_USER_MEDIA` con su cuenta conectada.

| Si falta… | Qué haces |
|---|---|
| Chrome o `node` | Te detienes. Mensaje «falta algo» con: «te falta `<Chrome | node>` en el servidor» y cómo instalarlo. |
| `puppeteer-core` | Lo instalas tú: `cd skills/carrusel-formatos-f100k && npm install --omit=dev` (solo baja `puppeteer-core`, no un navegador). Si falla, te detienes y avisas. |
| `GEMINI_API_KEY` | Sigues, pero la portada sale **sin** fondo de Gemini (foto de `cerebro/fotos/` o color liso). Lo dices en el ✅1. |
| Pillow y ffmpeg | Sigues. En el Paso 6 no podrás pasar a JPEG: avisa y entrega a mano. |
| Instagram en Composio | Sigues. El Paso 6 entrega el paquete para subir a mano. Lo dices en el ✅1. |

Si algo te detiene, **un solo mensaje** con qué falta en la primera línea y cómo arreglarlo.

---

## Paso 1 · Tema

En este orden:

1. **Si la usuaria pidió un tema** («hazme un carrusel de X»), ese manda.
2. Si no, el informe de radar más reciente de las **últimas 72 horas**:
   ```bash
   find informes -type f \( -name '*.md' -o -name '*.json' \) -mtime -3 -path '*radar*' 2>/dev/null | xargs ls -t 2>/dev/null | head -5
   ```
3. Si no hay ninguno, corre `radar-tendencias-f100k` en corto (solo la señal, sin informe largo) y
   **guarda una copia** en `informes/radares/AAAA-MM-DD-tendencias.md` para la próxima vez.

Elige **un** tema. El mejor es el que cruza tres cosas: señal fuerte en el radar, cabe en el nicho
de `USER.md`, y se puede llevar a su oferta sin forzar. Guarda en el estado el `por_que` y la
`fuente` (link o informe).

**Cifras, fechas, nombres y hechos: solo los que trae la fuente.** Lo que no tenga fuente no entra
al guion, ni redondeado ni «aproximado».

Crea la carpeta y el estado:

```bash
mkdir -p entregables/carruseles/AAAA-MM-DD-<slug>
```

---

## Paso 2 · Ficha

Lee `skills/carrusel-formatos-f100k/references/catalogo.md` y elige la ficha **por objetivo**
(alcance, guardados, seguidores o venta), igual que la skill. Mira la columna «¿Quién lo fabrica?»
de `skills/carrusel-formatos-f100k/SKILL.md`.

**En este flujo solo entran fichas que se fabrican sin que ella te mande nada:**

| Entra | Condición |
|---|---|
| Fichas de plantilla `split`, `papel`, `datos` | siempre, **menos F17** (abajo). F18 con fondo de Gemini: +US$0,10 |
| Fichas G de **HTML libre** sin capturas ni grabaciones | siempre |
| `garabato` (F13) y fichas que llevan su foto | solo si hay fotos en `cerebro/fotos/` |
| Casos de éxito, capturas reales, fichas con su cara generada por IA, F05 (2 imágenes por slide) | **nunca en automático**: si el tema lo pide, lo propones en el ✅1 y esperas el material |
| F17 tier list | **nunca en automático**: sin una imagen por ítem, la plantilla dibuja cuadros grises con la inicial y parece sin terminar (`build.js` no lo avisa) |

Referencia visual de la ficha: solo la que ya trae el catálogo. **Nunca** busques una nueva por
caption: el caption dice de qué habla un post, no cómo está construido.

---

## Paso 3 · Guion y caption

Con el método de `carrusel-viral-formula100k` y el prompt de la ficha elegida
(`skills/carrusel-formatos-f100k/references/prompts-por-plataforma.md`). Voz y datos: `USER.md`,
`cerebro/` y `cerebro/voice-guide.md` si existe.

Reglas duras (si una no se cumple, reescribe antes del ✅1):

1. **Titular de cada slide: 35 caracteres o 2 líneas como máximo.** Si no cabe, se corta el copy;
   nunca se baja la letra.
2. **Slide 1 = el gancho.** Se entiende sin leer el caption y promete algo concreto.
3. **Una idea por slide.** Si una slide pide más de ~25 palabras, se parte en dos.
4. **CTA con SU palabra clave** (de `USER.md` o `cerebro/`), de 1-2 sílabas, y aparece 1-2 veces
   antes del cierre. Si no tiene palabra definida, pregúntala en el ✅1 y deja `[PALABRA]` visible.
5. **Caption completo:** gancho en la primera línea, desarrollo corto, CTA con la palabra, 3-5
   hashtags del nicho. Sin cifras sin fuente.
6. Tuteo, español neutro.

### ✅1 · Telegram

Escribe el estado con `paso: "esperando_ok_guion"` y manda el mensaje ✅1 de
`mensajes-telegram.md`: tema y por qué, ficha y por qué, guion slide por slide, caption, costo
(portada: ~US$0,10) y las cuatro opciones. Termina y espera.

Cuando conteste:

| Respuesta | Qué haces |
|---|---|
| `1` / ✅ / «dale» | Paso 4. El ✅ cubre el gasto que decía el mensaje. |
| `2` + cambios | Aplica los cambios, vuelve a mandar el ✅1 completo. |
| `3` | Otra ficha: propón 2 alternativas con su porqué, ella elige, rehaces guion, ✅1 otra vez. |
| `4` | `paso: "descartado"`, una línea de confirmación. Fin. |

---

## Paso 4 · Render

Carpeta de trabajo: `entregables/carruseles/AAAA-MM-DD-<slug>/`.

**Portada con Gemini** (si hay llave **y la slide 1 tiene dónde ponerlo**: `split` → `foto`, `papel` → `fondo`, `datos` → solo `cifras`, HTML libre → siempre; `tier` y `mapa` no llevan fondo, así que ahí no generes nada y el ✅1 dice costo US$0): el fondo de la slide 1, **sin texto dentro de la imagen**
(el titular va en HTML encima). Usa el comando de la §3.1 del puente con `aspectRatio: "4:5"`,
`imageSize: "2K"`, prompt en inglés que termine con `no text, no letters, no watermark` y deje
**espacio limpio** donde irá el titular. Guárdala como `portada-fondo.png` en la carpeta del
carrusel. Si la ficha lleva a la persona, pasa su foto de `cerebro/fotos/` como `inline_data`
primero (segundo bloque de la §3.1). Suma una línea a `informes/gasto-imagenes.md`:
`AAAA-MM-DD · carrusel-del-radar · <slug> · 1 imagen 2K · US$0,10`.

**Slides:**

- **Ficha de plantilla** → escribe `spec.json` con el formato de
  `skills/carrusel-formatos-f100k/references/plantillas.md` (hay ejemplos que ya renderizan en
  `skills/carrusel-formatos-f100k/ejemplos/`). El fondo de Gemini entra como `foto` (split),
  `fondo` + `caja` (papel) o `fondo` (datos, `cifras`).
- **Ficha G de HTML libre** → escribe `carrusel.html` con el contrato de `plantillas.md`
  (`<section class="slide">` de 1080×1350, Google Fonts con `<link>`, nunca `-apple-system`) y el
  estilo del soporte en `references/estilos-guia-maestra.md`. El fondo va como `<img>` con ruta
  relativa.
- **Firma:** su handle de `USER.md` en el campo `handle` (o en el HTML).

Renderiza:

```bash
cd entregables/carruseles/AAAA-MM-DD-<slug>
node ../../../skills/carrusel-formatos-f100k/build.js spec.json .      # o carrusel.html
```

Salen `slide-01.png`, `slide-02.png`… a 2160×2700. Si el comando puede pasar de 150 segundos
(más de 10 slides), córrelo en segundo plano y consulta con llamadas cortas: los comandos
largos se cortan solos.

## Paso 5 · Revisión (bloqueante)

1. **Avisos de `build.js`:**
   - `⚠ no-cabe` / `⚠ letra-chica` → acorta **el texto** de esa slide y vuelve a renderizar.
     No achiques la plantilla.
   - `⚠ fuente` / `⚠ imagen` → no se entrega hasta resolverlo.
2. **Mira cada PNG, uno por uno.** Revisa: texto cortado o que se sale, tildes y eñes, cuadritos en
   lugar de emoji, cara tapada por texto, contraste, líneas cruzando el texto, que el titular de la
   portada se lea en el tamaño de miniatura, y **que ninguna slide deje media página vacía** (texto
   amontonado arriba y el resto en blanco: centra el bloque en vertical o sube el tamaño de la letra).
   Los avisos no reemplazan mirar: nada de esto lo detecta `build.js`.
3. Si corriges, suma 1 a `vueltas_revision`. **Máximo 2 vueltas.** Si a la tercera sigue fallando,
   escribe el estado con `paso: "esperando_ok_no_quedo"` (guarda la slide, el porqué y tu
   propuesta de texto corto en `no_quedo`) y manda el mensaje «no quedó» de `mensajes-telegram.md`.
   **Nunca mandes una slide rota.**

### «No quedó» · qué hacer con la respuesta

Esta tabla es la única que vale mientras el paso sea `esperando_ok_no_quedo`, y sus opciones son
las mismas del mensaje:

| Respuesta | Qué haces |
|---|---|
| `1` | Aplica el texto corto que propusiste en `no_quedo.propuesta`, `vueltas_revision: 0`, re-renderiza y vuelve al Paso 5. |
| `2` | Otra ficha: igual que la opción `3` del ✅1 (2 alternativas, ella elige, rehaces guion, ✅1 otra vez con `paso: "esperando_ok_guion"`). |
| `3` | `paso: "descartado"`, una línea de confirmación. Fin. |
| Otra cosa | Si trae un texto nuevo para esa slide, úsalo como en `1`. Si no, repite el mensaje «no quedó». |

### ✅2 · Telegram

Escribe el estado con `paso: "esperando_ok_slides"` y `slides_png`, y manda el ✅2: los PNG **como
documento** (no como foto: Telegram las comprime), en orden, más el caption final y las tres
opciones.

Publicar no se deshace, así que **la aprobación tiene que ser explícita**:

| Respuesta | Qué haces |
|---|---|
| «publícalo» / «✅ publica» (o esas palabras respondiendo directo al mensaje del ✅2) | Paso 6. |
| «corrige la slide N: …» | Corriges solo esa slide, re-renderizas, revisas (Paso 5), ✅2 otra vez. |
| «guárdalo» | Paso 6 en modo «a mano». |
| Cualquier otra cosa: un número suelto (`1`, `2`, `3`), un ✅ solo, «dale», «ok»… | **No es aprobación.** No publicas. Contesta con el mensaje «confirma» de `mensajes-telegram.md` y sigue esperando. |

---

## Paso 6 · Publicar

Reglas de `publicar-ig` (preview completo + ✅ ya se cumplieron en el ✅2). Aquí va directo por
Composio.

**1. A JPEG a 1080×1350** (Instagram solo acepta JPEG):

```bash
cd entregables/carruseles/AAAA-MM-DD-<slug>
python3 -c "
from PIL import Image; import glob
for f in sorted(glob.glob('slide-*.png')):
    Image.open(f).convert('RGB').resize((1080,1350), Image.LANCZOS).save(f[:-4]+'.jpg', quality=92)
    print(f[:-4]+'.jpg')
"
# sin Pillow: for f in slide-*.png; do ffmpeg -loglevel error -y -i "$f" -vf scale=1080:1350 -q:v 2 "${f%.png}.jpg"; done
```

**Protección contra doble publicación.** Antes de subir nada, mira el `estado.json`:

- Si ya tiene `post_url`, **ya está publicado**: no llames a nada, manda el mensaje «publicado» con
  ese link y deja `paso: "publicado"`.
- Si tiene `paso: "publicando"` y `contenedor_padre`, una corrida anterior se cortó cerca del
  PUBLISH. Consulta las publicaciones recientes de la cuenta (`INSTAGRAM_GET_IG_USER_MEDIA`) y
  compara el caption y la hora con los del estado. Si ya aparece, guarda su permalink en
  `post_url`, `paso: "publicado"` y avisa. Si no aparece y el padre tiene menos de 24 horas,
  publica **ese mismo** `contenedor_padre` (no crees contenedores nuevos). Si tiene más, empieza
  de cero desde el punto 2.

**2. Cupo del día:** `INSTAGRAM_GET_IG_USER_CONTENT_PUBLISHING_LIMIT`. Si no queda cupo, avisa y
deja el estado en `esperando_ok_slides`.

**3. Un contenedor por slide**, en orden, con `INSTAGRAM_POST_IG_USER_MEDIA`:
`ig_user_id`, `is_carousel_item: true` y el archivo en `image_file`. Composio sube el archivo a
una URL pública temporal: **no hace falta repo ni hosting**.
- Con el CLI de Composio: `composio execute INSTAGRAM_POST_IG_USER_MEDIA --file slide-01.jpg -d '{"ig_user_id":"…","is_carousel_item":true}'`
- Con Composio como herramienta: pasa la ruta del `.jpg` en `image_file`.

Guarda cada `id` en `contenedores_ig` del estado **en cuanto lo devuelve**.

**4. Contenedor padre** con `INSTAGRAM_POST_IG_USER_MEDIA`: `media_type: "CAROUSEL"`,
`children: [ids en orden]`, `caption`. Los `#` del caption van como `%23` (lo pide la acción).
Guarda su id en `contenedor_padre`.

**5. Publicar:** **antes** de llamar, escribe el estado con `paso: "publicando"` (con
`contenedores_ig` y `contenedor_padre` ya guardados). Luego `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`
con `creation_id` = `contenedor_padre`. En cuanto responda, guarda el id publicado en `media_id`,
pide el permalink, guárdalo en `post_url`, `paso: "publicado"` y manda el mensaje «publicado».

`ig_user_id`: la primera vez búscalo en su cuenta conectada y guárdalo en
`cerebro/memoria/instagram_page_id.md` (y súmalo a `cerebro/INDICE.md`), como dice `publicar-ig`.

**Modo ensayo** («ensayo, no publiques», o la primera corrida): haz los pasos 1 a 4 (así se prueba
que la subida funciona de verdad) y **no llames a PUBLISH**. Los contenedores sin publicar caducan
solos en 24 horas. Estado `entregado_a_mano`, mensaje «ensayo listo».

**A mano** (sin Instagram en Composio, sin JPEG posible, o eligió `3`): manda los `.jpg` (o los
PNG) como documento, en orden, y el caption en un mensaje aparte listo para copiar. Estado
`entregado_a_mano`.

**Si una llamada falla:** para ahí, no reintentes en bucle. Mensaje con el error en una línea y
qué slides alcanzaron a subirse. Nada queda publicado a medias: sin el PUBLISH final, Instagram
no muestra nada.

---

## Automatización

Cuando la usuaria pida dejarlo automático, muéstrale esto y espera ✅ antes de crearlo
(horas en la zona de `USER.md`):

> **Carrusel del radar** · lunes y jueves 8:00
> Corre la skill `carrusel-del-radar-f100k`. Si hay un carrusel esperando mi ✅, solo recuérdamelo.
> Nunca publiques sin mi ✅. Costo por corrida: ~US$0,10 (portada con Gemini).

---

## Lo que nunca haces

- Publicar sin el ✅2 explícito («publícalo» / «✅ publica») de ese mismo carrusel. Un número
  suelto no es ✅2, y un ✅ viejo no sirve para uno nuevo.
- Llamar a PUBLISH dos veces para el mismo carrusel.
- Tener dos carruseles abiertos a la vez.
- Poner en el guion una cifra, fecha, nombre o logro sin fuente.
- Inventar capturas, testimonios o resultados de clientas.
- Mandar una slide con texto cortado, cuadritos o la cara tapada.
- Buscar referencias por caption o entrar logueada a una red social desde el servidor.
- Guardar nada dentro de `skills/`: todo va en `entregables/carruseles/`.
