---
name: audio-post-motion
description: |
  Edición y post de audio para piezas de motion graphics. Úsala cuando el usuario pida
  "poner música", "sincronizar al beat", "quitar el ruido de la voz", "normalizar el volumen",
  "que la música no tape la voz", "agregar sonidos de impacto", "elegir la música",
  "medir LUFS", "exportar con audio", o cuando el audio de una pieza suene flojo, saturado o
  desincronizado. Incluye objetivos de loudness por plataforma, recetas ffmpeg (ducking,
  loudnorm, ebur128), detección de BPM, alineación de SFX al frame, y síntesis de score en
  WebAudio para que cada golpe caiga en el frame exacto.
version: 1.0.0
license: MIT
---

# Audio post para motion graphics

El audio no es el final del proceso: es lo que decide el ritmo. En MG, **el sonido se diseña con
la imagen, no encima de ella**.

## Cuándo activarse

- Sincronizar cortes o animaciones a música / BPM.
- Limpiar, normalizar o mezclar voz con música.
- Diseñar SFX (whoosh, impact, riser, pop, click, glitch) alineados al frame.
- Elegir o generar música con licencia segura.
- Verificar loudness antes de exportar.

## Orden de trabajo (no lo cambies)

1. **Voz primero.** Sin música. Corta silencios y errores, arregla niveles.
2. **Música después**, a −18/−20 dBFS de pico mientras haya voz.
3. **SFX al final**, uno por beat visual.
4. **Ducking** automático de música bajo la voz.
5. **Master**: EQ correctivo suave → compresor → limitador → loudness por destino.
6. **Medición**: LUFS integrado + true peak. Nunca “a oído”.

## Objetivos de loudness

| Destino | Integrado | True peak | Notas |
|---|---|---|---|
| YouTube / Reels / TikTok / web | **−14 LUFS** (−14 a −12) | ≤ −1 dBTP | YouTube normaliza a −14; subir más solo comprime |
| Podcast / voz hablada | −16 LUFS (−19 mono) | ≤ −1 dBTP | Inteligibilidad > volumen |
| Broadcast EBU R128 | **−23 LUFS** | ≤ −1 dBTP | Exigido por TV europea |
| Cine / sala | −27 a −24 LUFS | ≤ −2 dBTP | Dialnorm |

## Cadena ffmpeg (copiar y pegar)

```bash
# 1. Limpiar voz: high-pass, denoise, compresión suave
ffmpeg -i vo.wav -af "highpass=f=90,afftdn=nf=-25,\
acompressor=threshold=-18dB:ratio=3:attack=8:release=180" vo_clean.wav

# 2. Ducking de música bajo la voz (sidechain)
ffmpeg -i vo_clean.wav -i music.wav -filter_complex \
"[1:a]volume=0.55[m];[m][0:a]sidechaincompress=threshold=0.05:ratio=6:attack=10:release=280[duck];\
 [0:a][duck]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.891[a]" \
-map "[a]" mix.wav

# 3. Normalizar al destino (dos pasadas para precisión)
ffmpeg -i mix.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=summary" -ar 48000 mix_norm.wav

# 4. Verificar
ffmpeg -i mix_norm.wav -af "ebur128=peak=true" -f null - 2>&1 | tail -12
```

Script incluido: [`scripts/loudness.sh`](scripts/loudness.sh) (mide y normaliza, con salida legible).

## BPM y alineación al frame

```
frames_por_pulso = (60 / BPM) * fps
```

| BPM | fps 30 | fps 25 | fps 60 |
|---|---|---|---|
| 90 | 20 | 16,7 | 40 |
| 100 | 18 | 15 | 36 |
| 120 | 15 | 12,5 | 30 |
| 128 | 14,06 | 11,7 | 28,1 |
| 140 | 12,86 | 10,7 | 25,7 |

**Offsets que importan:**

- Impacto visual ↔ SFX: mismo frame (0 a +2 frames de retardo es aceptable; el oído tolera mejor
  el SFX ligeramente tardío que el adelantado, salvo que busques anticipación dramática).
- Gráfico ↔ palabra clave en voz: el gráfico entra 2–4 frames **antes** de la palabra.
- Corte ↔ downbeat: adelanta el corte 1 frame (compensa ~20–30 ms de latencia perceptiva).

Detección de BPM:

```bash
# aubio
aubio tempo music.mp3
# ffmpeg (energía por segundo, útil para ver pulsos)
ffmpeg -i music.mp3 -af "astats=metadata=1:reset=1" -f null - 2>&1 | grep -i rms
```

En el navegador: `web-audio-beat-detector` o analizar `AudioBuffer` con autocorrelación.
En Node: `essentia.js`.

## Diseño de SFX (mapa mínimo)

| Evento visual | SFX | Duración | Nivel relativo |
|---|---|---|---|
| Aparición de elemento | pop / click | 60–120 ms | −12 dB bajo la voz |
| Transición / barrido | whoosh | 300–700 ms | −8 dB |
| Golpe / cambio de escena | impact / thud | 150–500 ms | −3 dB (protagonista) |
| Tensión antes de revelar | riser | 800–2000 ms | sube de −20 a −6 dB |
| Dato que cuenta | tick por unidad | 20–40 ms | −18 dB |
| Error / glitch | digital glitch | 80–250 ms | −10 dB |

Regla: **un SFX por beat, no cinco**. El silencio también es un SFX.

## Música: opciones legales y prácticas

1. **Sintetizar el score en código** (recomendado para piezas de código): WebAudio o
   `music/score.mjs` de `kinetic-reel`. Cero problemas de licencia y golpes exactos al frame.
2. **Bibliotecas con licencia clara**: Artlist, Musicbed, Epidemic Sound (suscripción);
   Free Music Archive / ccMixter (verificar CC-BY y atribución).
3. **Nunca** uses música de YouTube/TikTok sin licencia en una pieza comercial: el reclamo llega
   después de la entrega.

Ver [`references/music-licensing.md`](references/music-licensing.md).

## Síntesis de score sincronizado (WebAudio)

Patrón de reloj con lookahead — el mismo que usa `demo/reel.js` en este repo:

```js
const ctx = new AudioContext();
const BPM = 120, BEAT = 60 / BPM;
let nextBeat = 0, beatIndex = 0;

function scheduler() {
  while (nextBeat < ctx.currentTime + 0.15) {   // 150 ms de lookahead
    scheduleKick(nextBeat);
    if (beatIndex % 4 === 2) scheduleHat(nextBeat);
    if (beatIndex % 2 === 0) scheduleBass(nextBeat);
    nextBeat += BEAT;
    beatIndex++;
  }
}
setInterval(scheduler, 25);
```

Y para derivar la animación del mismo reloj:

```js
const t = (ctx.currentTime - startTime);        // segundos desde el inicio
const beatPhase = (t / BEAT) % 1;               // 0..1 dentro del pulso
```

Así **imagen y audio nunca se desincronizan**: ambos leen el mismo reloj.

## Emparejar audio y video al exportar

```bash
# audio corto respecto al video: rellenar con silencio y cortar al final exacto
ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac -b:a 192k \
  -af "apad" -shortest final.mp4

# offset de sincronía (audio 120 ms tarde)
ffmpeg -i video.mp4 -itsoffset 0.12 -i audio.wav -c:v copy -c:a aac -shortest final.mp4
```

## Checklist de audio antes de entregar

- [ ] Voz inteligible en celular a volumen bajo.
- [ ] Música entre −18 y −22 dBFS durante la voz.
- [ ] Ningún SFX enmascara una palabra.
- [ ] Sin clicks ni cortes secos al inicio/final (fade de 20–40 ms).
- [ ] Loudness medido y dentro del objetivo del destino.
- [ ] True peak ≤ −1 dBTP (sin clipping inter-sample).
- [ ] El video funciona también en mute (versión muda exportada).
