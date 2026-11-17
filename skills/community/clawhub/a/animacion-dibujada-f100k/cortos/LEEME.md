# Cortos: del guion por escenas a un video de 30-90 s

Un corto es una fila de escenas. Cada escena es una pieza de la skill (cualquier estilo, armado con `armar.mjs`
y con su frase cambiada). `corto.mjs` las renderiza en paralelo, las une con transiciones, quema los subtítulos
y le pone la voz y la música. Un corto de 40 s tarda ~15-25 s en salir (la primera vez; con `--solo` o sin cambios, ~9 s).

```
node scripts/hoja-corto.mjs guion.json hoja.jpg      # 1. revisar el corto entero ANTES (≈10 s)
node scripts/corto.mjs guion.json corto.mp4          # 2. renderizar
node scripts/corto.mjs guion.json corto.mp4 --solo 3 # 3. si cambiaste solo la escena 3 (las demás salen de la caché)
```

## El guion (`guion.json`, rutas relativas a él)

```json
{
  "fps": 30,
  "voz": "voz.m4a",
  "musica": "musica.m4a",
  "volumen_musica": 0.18,
  "dur_transicion": 0.5,
  "subtitulos": { "activo": true, "estilo": "caja", "posicion": "auto", "sincronia": "palabra" },
  "escenas": [
    { "pieza": "escenas/01-gancho.html", "inicio": 0,     "transicion": "corte" },
    { "pieza": "escenas/02-libreta.html", "inicio": 3.87, "transicion": "barrido-izq",
      "subtitulo": "No subiría solo fotos bonitas de pasteles." },
    { "pieza": "escenas/07-cta.html",     "inicio": 24.4, "dur": 4.7, "transicion": "fundido" }
  ]
}
```

| Campo | Qué hace |
|---|---|
| `voz` | La voz **grabada de la persona** (m4a, mp3, wav). Si dura más que las escenas, la última se queda quieta hasta que termina. |
| `musica`, `volumen_musica` | Opcional (0.18 por defecto). Se repite si es corta, entra con fundido de 1,2 s, sale con fundido al final y **baja sola cuando hay voz** (ducking con `sidechaincompress`): en las pausas vuelve a subir. |
| `inicio` | Segundo de la voz en que entra la escena. Si **todas** lo traen, la duración de cada una sale de ahí: la imagen cambia cuando cambia la idea. Si no, usa `dur`. |
| `dur` | Cuánto se ve la escena. La última necesita `dur` aunque haya `inicio`. |
| `transicion` | Cómo **entra** la escena: `corte`, `fundido`, `barrido-izq`, `barrido-arriba`, `zoom`, `circulo` (o cualquier nombre de `xfade` de ffmpeg), o las dibujadas de la skill: **`tinta`** (mancha que se expande con borde de tinta y salpicaduras), **`pagina`** (se da vuelta la hoja, con dorso de papel y sombra) y **`pixel`** (bloques que se encienden en blanco de arriba hacia abajo). Dura `dur_transicion` (las dibujadas lucen mejor con 0.5-0.6). |
| `subtitulo` | Lo que se dice en la escena, tal cual (el texto correcto; los tiempos salen de la voz). |
| `subtitulos.sincronia` | **`palabra`**: transcribe la voz con Whisper local y enciende cada palabra justo cuando se dice (grupos de 2-5 palabras, la palabra dicha en amarillo, estilo reel). El texto que se ve es SIEMPRE el del guion: Whisper solo aporta los tiempos (se alinean aunque transcriba mal, p. ej. «cuantos ya» por «cuántos da»). `largo` (por defecto): trozos de ≤ 34 letras repartidos por largo. |
| `subtitulos.posicion` / `subtitulo_posicion` | **`auto`**: por escena, prueba 13 alturas y elige la franja sin texto ni objetos (mide el renglón más cargado en 3 momentos de la escena); a igualdad, abajo. Si ninguna está libre, avisa ⚠. También `abajo-seguro` (encima de los 450 px que tapa Instagram) o `arriba-seguro`. |
| `encajar` | Por defecto, si la animación no alcanza a terminar en su escena, se acelera lo justo (hasta 1.8×) para no cortarse a media frase. `false` = se corta tal cual. |

## Cómo se hace uno bien

1. **Primero la voz.** Graba el guion (o usa el audio del reel). Anota en qué segundo arranca cada idea: ese es el `inicio` de cada escena. Una escena = una idea, de 3 a 6 s.
2. **Una escena por idea, con su estilo.** Gancho → `escena-texto-cinetico` (golpe). Lista → `pizarra-tiza` o `post-its`. Lo que te escriben → `chat-que-vende`. Resultado → `grafica-que-sube` o `polaroid-que-se-revela`. Cierre → `escena-cta` con la palabra del CTA.
3. **Subtítulos solo donde la pantalla no dice ya lo mismo.** En las escenas de texto cinético y en el CTA, el texto ES la pantalla: sin `subtitulo`.
4. **Pocas transiciones distintas.** Un barrido para avanzar, un zoom para el golpe, un fundido para cerrar. Diez transiciones distintas se ven amateur.
5. **Paleta del rubro en todas las escenas** (los `COLORES` de cada pieza): así se siente un solo corto y no un collage.
6. **Revisa la hoja antes de renderizar.** Muestra lo que de verdad se verá (con el encaje aplicado), marca con un rectángulo dónde cae el subtítulo (amarillo = libre, rojo = choca) y avisa si una escena necesita más de 1.8× o se sostiene quieta mucho rato.
7. **Si el corto avisa «no hay franja limpia»**, casi siempre es porque la escena ya muestra ese texto (pizarra, post-its, ticket): quita el `subtitulo` de esa escena.
8. **Transiciones dibujadas con medida**: una `tinta` para el golpe emocional, una `pagina` para «capítulo nuevo», un `pixel` para lo digital. Una de cada por corto, no más.

## Voz provisional (solo para probar)

Para probar tiempos sin grabar: `say -v Paulina -r 198 -o 01.aiff "la frase"` (voces en español: `say -v '?' | grep es_`).
**El corto real lleva la voz grabada de la persona**: la voz de sistema suena robótica y no se publica.
Lo más fácil: escribe un plan de escenas y corre `node scripts/armar-corto.mjs plan.json <carpeta>`; arma escenas, voz de prueba y `guion.json` (formato en el comentario inicial de ese script).

## Subtítulos por palabra: qué necesita

Busca, en este orden: **mlx-whisper** (Apple Silicon, vía `uvx`, modelo `mlx-community/whisper-large-v3-turbo`; primero sin internet, desde la caché)
y **openai-whisper** (`whisper` en la terminal, modelo `small`). La transcripción queda en caché en `.corto-tmp/` (no se repite si la voz no cambia).
Si no hay ninguno, el corto sale igual con subtítulos por largo y lo avisa. Para instalar el rápido en Mac: `brew install uv` y la primera
corrida descarga el modelo (~1,6 GB, una sola vez). Se usa `--condition-on-previous-text False`: evita que Whisper se trabe repitiendo frases.

## Música de prueba

Para probar el ducking sin buscar música: una pista generada con matemáticas (acordes + arpegio) está en el ejemplo de v2.
La música que se publica tiene que ser con licencia (la de Instagram se pone en la app, no en el archivo).
