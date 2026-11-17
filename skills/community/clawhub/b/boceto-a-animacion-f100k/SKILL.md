---
name: boceto-a-animacion-f100k
description: "Convierte un DIBUJO A MANO (foto o captura mandada por Telegram) o una frase del guion en un clip animado 9:16 de motion graphics para acompañar un reel. Lee el boceto como plano de composición (objetos, texto literal, movimiento implícito), decide si el dibujo es el cuadro INICIAL o el FINAL, elige estilo de un catálogo de 7, escribe los 3 prompts (primer cuadro, último cuadro, movimiento) y, con ✅ de créditos, lo genera en Higgsfield: GPT Image 2.5 con el boceto de referencia → el cuadro opuesto EDITANDO el primero → Seedance 2.0 con start_image + end_image. Entrega clip + cuadros + PROMPTS.md; el split «Animación | Boceto» y el revelado se arman en CapCut o Edits. Activar con 'anima este dibujo', 'convierte mi boceto en animación', 'de dibujo a video', 'primer y último cuadro', 'first frame last frame', 'dibujé esto, dale vida'. NO para overlays sobre la cara, historias con varios clips (storytelling-animado-f100k) ni para componer video grabado."
argument-hint: "<ruta del boceto o frase del guion> [estilo] [solo-prompts]"
allowed-tools: "Bash, Read, Write, Edit, AskUserQuestion, Skill, mcp__higgsfield__generate_image, mcp__higgsfield__generate_video, mcp__higgsfield__media_upload, mcp__higgsfield__media_confirm, mcp__higgsfield__jobs_wait, mcp__higgsfield__job_status, mcp__higgsfield__models_explore, mcp__higgsfield__balance, mcp__claude_ai_Higgsfield__generate_image, mcp__claude_ai_Higgsfield__generate_video, mcp__claude_ai_Higgsfield__media_upload, mcp__claude_ai_Higgsfield__media_confirm, mcp__claude_ai_Higgsfield__jobs_wait, mcp__claude_ai_Higgsfield__job_status, mcp__claude_ai_Higgsfield__models_explore, mcp__claude_ai_Higgsfield__balance"
metadata: {"version": "1.0.0", "mcp-required": ["higgsfield"], "origen": "reel @rajhere.in DbqARtpJnw4 (5-ago-2026, 344K vistas) + su skill first-last-frame-prompts, corregida y llevada de punta a punta", "openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - El boceto llega por Telegram: pídele que lo mande como archivo (no como foto comprimida) y guárdalo en `entregables/animaciones/<fecha>_<slug>/boceto.jpg`.
> - Paso 11 NO corre aquí (`scripts/componer.py` no viene en esta versión). Entrega `clips/clip.mp4` (ya sale 9:16 de Seedance), `frames/ancla.png`, `frames/opuesto.png`, `boceto.jpg` y `PROMPTS.md`, y explícale en 3 líneas cómo armar el split y el revelado en CapCut o Edits.
> - Paso 10: para revisar el borrador puedes sacar 4 cuadros con ffmpeg solo para mirarlos (no se entregan). Manda la hoja por Telegram y espera ✅ antes del final a 720p.
> - Costos: consulta `get_cost` y `balance` y muestra el total (≈33 créditos por clip) antes de generar. Sin ✅ no se genera nada; con `solo-prompts` o sin Higgsfield, entrega `PROMPTS.md`.
> - La elección de estilo va por Telegram con opciones numeradas (el recomendado primero).
> - `MANIFEST_BROLL.md` sirve para quien edita en una compu con `editor-video-formula100k`; genéralo igual si hay frase del guion.

---

# Boceto → Animación — F100K

Dibujas una idea en 30 segundos y sale un clip de motion graphics que parece hecho por un
estudio. El dibujo no se «mejora»: es el **plano**. Dice qué objetos van, dónde, y qué se
mueve. El estilo pone el material y la luz.

**Tres cosas que esta skill hace distinto de la original** (que solo escribía prompts para
copiar y pegar):

1. **Decide si el boceto es el principio o el final.** La mayoría de los bocetos dibujan la
   idea ya pasando, y ese dibujo tiene que ser el **último** cuadro. La original siempre lo
   ponía primero y se comía la sorpresa.
2. **El segundo cuadro se saca editando el primero**, no generando otro desde cero. Así los
   dos son la misma toma y el video no se deforma uniéndolos.
3. **Llega hasta el .mp4 y lo compone**: clip suelto, split «Animación | Boceto» y revelado.

---

## 🧭 Anclaje de rubro (manda sobre cualquier ejemplo)

Los ejemplos de esta skill (cofre de ideas, banco con tentáculos, tarjeta de $1,000) enseñan la
**mecánica**, no el tema. Los objetos del boceto salen del rubro real de quien dibuja. Si es
repostería, son mangas pasteleras y hornos, no embudos. Nunca asumas que el rubro es marketing.

---

## Cuándo usar esta skill (vs. las otras de motion)

| Tienes… | Skill |
|---|---|
| Un dibujo o una metáfora visual → UN clip animado | **esta** |
| Texto que dices y quieres verlo aparecer junto a tu cara | `motion-reels-f100k` |
| Un gráfico pegado al dedo que señala | `motion-tracking-dedo-f100k` |
| Una historia completa con 2-5 clips animados | `storytelling-animado-f100k` (puede llamar a esta para cada clip) |
| Un corto con personajes y continuidad | `cine-ia-f100k` (si la tienes instalada) |
| El video grabado para montar | `editor-video-formula100k` |

---

## Referenciales (cargar antes del Paso 2)

1. `references/lectura-boceto.md`: inventario, ancla, contrato de cuadros, plantillas de los 3 prompts, los 4 bocetos del reel decodificados, y qué hacer sin boceto
2. `references/estilos.md`: los 7 bloques de estilo y cómo elegir por tono
3. `scripts/componer.py`: el compositor (solo · split · revelado). No viene en esta versión: la composición no corre en el servidor

---

## Proceso

### Paso 1: Entrada

Lo que se necesita (si ya vino en el mensaje, no preguntes):

- **El boceto**: ruta local a la foto o captura. Si lo pegó en el chat y no hay ruta, pídele
  que lo guarde y te pase la ruta (Higgsfield necesita subir el archivo).
- **Para qué frase del reel es** (opcional pero valioso): define el tono → el estilo, y la
  keyword del MANIFEST.
- **Qué salida quiere**: clip suelto, split, revelado o las tres (por defecto: las tres).

Si trae **una frase y no un dibujo** → `lectura-boceto.md` §6: propón 3 metáforas físicas
(objeto + acción), que dibuje la que elija y vuelva. Si no quiere dibujar, sigue sin boceto y
**sin** split ni revelado.

Si pide **`solo-prompts`** o no hay Higgsfield conectado → corre Pasos 2-5 y entrega
`PROMPTS.md`. Es la versión gratis y sirve con cualquier herramienta (ChatGPT imagen +
Seedance/Kling a mano).

### Paso 2: Leer el boceto

Abre la imagen con `Read` y **mírala**. Escribe el bloque **LO QUE VEO** de
`lectura-boceto.md` §1: formato, vista, objetos contados con posición, texto literal,
movimiento implícito, dudas.

Muéstraselo. Si hay una duda que cambia el movimiento, esa es tu **única** pregunta.

### Paso 3: Ancla y movimiento

Aplica la tabla de `lectura-boceto.md` §2 y declara en una línea:

> *Ancla: FINAL. El dibujo ya muestra los íconos saliendo; el inicio es la carpeta cerrada y
> sin íconos.*

Y la acción en una línea: **un objeto protagonista + una acción física**. Si el boceto trae
dos acciones, son dos clips: díselo y pregunta cuál va primero.

### Paso 4: Estilo

Por la tabla de tono de `estilos.md`, ofrece **3 estilos** con `AskUserQuestion` (el
recomendado primero, con una línea de por qué). Si el reel ya tiene otros clips hechos con esta
skill, **se usa el mismo estilo** y no se pregunta.

### Paso 5: Los 3 prompts → `PROMPTS.md`

Con las plantillas de `lectura-boceto.md` §4:

1. **Cuadro ancla**: boceto como referencia de composición + bloque de estilo completo +
   objetos contados con posición + texto literal + estado.
2. **Cuadro opuesto**: «edit this exact image, change ONLY…» + el delta concreto.
3. **Movimiento**: 1-2 frases: orden, ritmo, cámara, qué queda quieto, «no new objects».

Escríbelos en `PROMPTS.md` (formato abajo). Si el modo es `solo-prompts`, **termina aquí**.

### Paso 6: Preflight de créditos (compuerta)

Consulta el costo **real** con `get_cost: true` (no gasta) y el saldo con `balance`. Precios
verificados el 2026-09-13 (pueden cambiar: por eso se consultan, no se copian):

| Peldaño | Modelo | Créditos |
|---|---|---|
| Cuadro ancla | `gpt_image_2_5`, quality `medium`, `2k`, 9:16 | 1,5 |
| Cuadro opuesto | `gpt_image_2_5` editando el ancla | 1,5 |
| Borrador de movimiento | `seedance_2_0` mode `fast`, 480p, 5 s | 7,5 |
| Final | `seedance_2_0` mode `std`, 720p, 5 s | 22,5 |
| **Total por clip** | | **33** |

Dile el total y pide aprobación con `AskUserQuestion`. **Sin un sí explícito no se genera
nada.** Si el saldo no alcanza: entrega `PROMPTS.md`, dilo claro y para.

`use_unlim`: **omítelo.** Si el servidor devuelve `unlim_choice`, esa pregunta es del usuario.

### Paso 7: Subir el boceto

```
media_upload({ filename: "boceto.jpg" })          → { media_id, upload_url }
curl -sS -X PUT -H "Content-Type: image/jpeg" --upload-file "<ruta>" "<upload_url>" -w "%{http_code}"
media_confirm({ type: "image", media_id })        (solo si el PUT dio 200)
```

### Paso 8: Cuadro ancla

```
generate_image({ params: {
  model: "gpt_image_2_5", quality: "medium", resolution: "2k", aspect_ratio: "9:16",
  prompt: "<prompt 1>",
  medias: [{ value: "<media_id del boceto>", role: "image_references" }]
}})
```

Espera con `job_status` (`sync: true`), baja el resultado a `frames/ancla.png` y **míralo
junto al boceto** (`Read` a los dos). Pasa el chequeo:

- [ ] Están **todos** los objetos del inventario y ninguno de más
- [ ] Cada uno en su tercio, con su tamaño relativo
- [ ] El texto está escrito **exacto**
- [ ] El estilo es el elegido, no una versión genérica

Si falla uno: corrige el prompt (nombra lo que faltó) y regenera **solo** este cuadro. Tras 2
intentos fallidos, muéstrale el mejor y pregúntale si sirve.

### Paso 9: Cuadro opuesto

```
generate_image({ params: {
  model: "gpt_image_2_5", quality: "medium", resolution: "2k", aspect_ratio: "9:16",
  prompt: "<prompt 2: edit this exact image…>",
  medias: [{ value: "<job_id del ancla>", role: "image_references" }]
}})
```

Baja a `frames/opuesto.png`, míralo junto al ancla: **fondo, cámara, luz y diseño de cada
objeto idénticos; solo cambió el delta.** Si cambió algo más, regenera.

Asigna los roles de video según el ancla: ancla FINAL → `start_image` = opuesto,
`end_image` = ancla. Ancla INICIAL → al revés.

### Paso 10: Movimiento (borrador → final)

**Borrador** (480p rápido):

```
generate_video({ params: {
  model: "seedance_2_0", mode: "fast", resolution: "480p", aspect_ratio: "9:16",
  duration: 5, generate_audio: false,
  prompt: "<prompt 3>",
  medias: [
    { value: "<job_id del cuadro inicial>", role: "start_image" },
    { value: "<job_id del cuadro final>",   role: "end_image" }
  ]
}})
```

Baja a `clips/borrador.mp4`. Saca 4 cuadros y míralos
(`ffmpeg -i clips/borrador.mp4 -vf "fps=1,scale=270:-1,tile=5x1" -frames:v 1 hoja.png`).
Busca: objetos que se deforman o se derriten, texto que baila, objetos nuevos que aparecen, y
que el movimiento sea **el** del prompt.

Muéstrale la hoja y pregunta: *¿vamos al final a 720p (22,5 créditos) o ajusto el
movimiento?* Si ajusta, se regenera el borrador, **nunca** los cuadros (esos ya pasaron).

**Final**: igual, con `mode: "std"`, `resolution: "720p"`. Baja a `clips/clip.mp4`.

Si `seedance_2_0` rechaza la combinación start+end: prueba `seedance_2_5` con
`mode: "omni_reference"` (mismos roles, 480p 12,5 / 720p 32,5 créditos) y avísale del cambio
de precio **antes** de lanzar.

### Paso 11: Componer (NO corre en este servidor: lee el bloque 🦞 de arriba)

```bash
S=skills/boceto-a-animacion-f100k/scripts/componer.py
python3 $S solo     --clip clips/clip.mp4 --out salida/clip_9x16.mp4
python3 $S split    --clip clips/clip.mp4 --boceto boceto.jpg --out salida/split.mp4 \
                    --titulo "Animación con IA" --etiquetas "Animación,Boceto" [--cta "Comenta DIBUJO"]
python3 $S revelado --clip clips/clip.mp4 --boceto boceto.jpg --out salida/revelado.mp4 \
                    [--sosten 1.2] [--transicion fade|circleopen|wipeup]
```

- El **título**, la **CTA** y las **etiquetas** los decide el usuario; no pongas la palabra
  gatillo sin preguntarle (una palabra quemada por uso repetido hunde los comentarios).
- `revelado` con ancla FINAL: el boceto se transforma en un clip que **termina** pareciéndose
  a él; es el gancho más fuerte. Con ancla INICIAL usa `--transicion fade`.

**Mira** un cuadro de cada salida antes de entregar
(`ffmpeg -ss 2 -i salida/split.mp4 -frames:v 1 -vf scale=540:-1 revisar.png`).

### Paso 12: Entregar

Carpeta: `entregables/animaciones/` (no hace falta preguntar la raíz):

```
YYYY-MM-DD_<slug>/
├── boceto.jpg
├── PROMPTS.md
├── frames/ancla.png · frames/opuesto.png
├── clips/borrador.mp4 · clips/clip.mp4
├── salida/clip_9x16.mp4 · salida/split.mp4 · salida/revelado.mp4
└── MANIFEST_BROLL.md        (si hay frase del guion)
```

`MANIFEST_BROLL.md`: la fila para pegar en el `MANIFEST.md` del reel, con el formato de
`editor-video-formula100k`. Keyword **verbatim** de la frase (4-8 palabras que de verdad va a
decir). El editor resuelve `Archivo` **relativo a la carpeta del reel**: dile que copie
`salida/clip_9x16.mp4` a `<carpeta del reel>/clips/<slug>.mp4` (o cópialo tú si te da la ruta).

```markdown
## B-roll

| Keyword                    | Archivo            | Duración | Estilo        |
|----------------------------|--------------------|----------|---------------|
| tu bóveda de ideas se abre | clips/<slug>.mp4   | 5        | monitor-photo |
```

Cierra con créditos gastados de verdad (suma de lo lanzado, no del presupuesto) y qué sigue.

---

## Formato de `PROMPTS.md`

```markdown
# <slug>: <la idea en una frase>

- **Boceto:** boceto.jpg
- **Ancla:** FINAL | INICIAL | AMBOS: <por qué, una línea>
- **Acción:** <objeto protagonista + acción física>
- **Estilo:** <id del catálogo>

## 1. Cuadro inicial
<prompt en inglés>

## 2. Cuadro final
<prompt en inglés>

## 3. Movimiento
<prompt en inglés>

=== EXPLICACIÓN ===
- Lo que vi en el boceto: …
- Por qué este estilo: …
- Cómo usarlo sin esta skill: genera el cuadro [ancla] con el boceto adjunto en ChatGPT/GPT
  Image, luego edita esa imagen con el prompt del otro cuadro, y en Seedance/Kling sube los
  dos como primer y último cuadro con el prompt de movimiento.
```

Los encabezados 1 y 2 van en **orden de tiempo** (inicial, final), no en orden de generación.
Anota junto a cada uno cuál es el ancla.

---

## Reglas duras

1. **Nunca generar sin aprobación explícita del costo.** Ni «ya que estamos».
2. **Nunca presentar como dibujo a mano algo que no lo es.** Sin boceto real no hay `split` ni
   `revelado`: la premisa del formato es «esto lo dibujé yo».
3. **Un clip = una acción.** Dos acciones son dos clips.
4. **El texto del boceto se copia exacto; no se inventa texto.** Máximo 3 palabras en imagen.
5. **`generate_audio: false` siempre.** El clip va bajo la voz de quien habla en el reel.
6. **Máximo 6 s por clip.** Más largo deja de acompañar y se vuelve el video.
7. **Mismo estilo en todos los clips de un reel.**
8. **Si el cuadro no pasa el chequeo, no se anima.** Animar un cuadro malo cuesta 22,5 créditos
   para confirmar que estaba malo.

---

## Gotchas

- **El orden del boceto:** si la animación «no tiene gracia», casi siempre es un ancla
  mal puesta (el dibujo cumbre quedó de inicio). Invierte roles antes de reescribir prompts.
- **Dos imágenes independientes ≠ misma toma.** Aunque el texto sea idéntico, cambian fondo,
  cámara y diseño; Seedance intenta unirlas derritiendo la escena. Por eso el Paso 9 edita.
- **Seedance deforma letras en movimiento.** Pon `the text stays static and locked` o saca el
  texto del clip.
- **Muchos ffmpeg no traen `drawtext`** (el de Homebrew, por ejemplo). `componer.py` dibuja todo el
  texto con Pillow y lo pega con `overlay`, así funciona en cualquiera. No lo «simplifiques» a drawtext.
- **`thumbnail()` de Pillow solo achica.** Un boceto de 300 px quedaba como estampilla en el
  panel; `contener()` escala hacia arriba a propósito.
- **Precios:** consulta siempre con `get_cost`. Los de la tabla son del 2026-09-13.
- **Sin prueba viva todavía (2026-09-13):** la cuenta de prueba no tenía créditos. Verificados: los
  modelos y sus roles (`start_image`/`end_image` en `seedance_2_0`, `image_references` en
  `gpt_image_2_5`), los costos y el compositor con material real del reel. **No verificado:**
  la edición del ancla con `job_id` como referencia y la generación completa. La primera
  corrida real debe mirar con más cuidado los Pasos 9 y 10 y corregir esta nota.
