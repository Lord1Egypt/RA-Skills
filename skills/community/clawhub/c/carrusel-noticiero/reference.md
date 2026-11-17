# Referencia — portada animada, ffmpeg y publicación

## A) Portada ANIMADA (la firma del formato)

Recrea `slide-01-ANIMADO.mp4`. Todos los archivos intermedios van en `<carpeta>/recursos/`.

### 1. Imagen hero (Higgsfield `generate_image`)
- Modelo: `nano_banana_2`, calidad 4K, formato vertical (encuadre 4:5 / 1080×1350).
- Prompt: escena editorial/noticiero ligada a la noticia, cinematográfica, atmósfera oscura y
  dramática, **sin texto ni logos** (el texto lo pone el overlay). Deja aire arriba (píldora) y
  abajo (titular).
- Si la noticia es sobre una persona/empresa real, evita caras identificables falsas; usa
  escena conceptual (servidores, pantallas, salas de mando, etc.).
- Descarga el resultado a `recursos/cover.png`.
- **Créditos:** genera una sola vez; reusa `recursos/cover.png` si re-renderizas.

### 2. Animación (Higgsfield `generate_video`)
- Desde `recursos/cover.png`. Modelo `seedance` o `kling`. Movimiento **sutil**: parallax lento,
  zoom in muy leve, o luz que respira. Duración 4-6 s. Sin cortes.
- Descarga a `recursos/cover_anim_raw.mp4`.

### 3. Overlay de titular (transparente)
- Copia `cover/overlay.html` → `recursos/overlay.html`, pon el mismo titular/píldora que el cover.
- Renderiza a PNG con alpha:
  ```
  node skills/carrusel-noticiero/export.js "<carpeta>/recursos/overlay.html" \
    --width 1080 --height 1350 --scale 2 --transparent
  ```
- Sale `recursos/slide-01.png` (con alpha); renómbralo a `recursos/title-overlay.png`.

### 4. Composición ffmpeg (solo en una compu; NO corre en el servidor OpenClaw)
Superpone el overlay sobre el video y fija tamaño/fps. El overlay se renderiza a 2× (2160×2700),
así que escálalo al tamaño del video:
```
ffmpeg -y -i "<carpeta>/recursos/cover_anim_raw.mp4" -i "<carpeta>/recursos/title-overlay.png" \
  -filter_complex "[0:v]scale=1080:1350:force_original_aspect_ratio=increase,crop=1080:1350[bg]; \
                   [1:v]scale=1080:1350[ov]; [bg][ov]overlay=0:0:format=auto,format=yuv420p[v]" \
  -map "[v]" -r 30 -pix_fmt yuv420p -c:v libx264 -crf 18 \
  "<carpeta>/slide-01-ANIMADO.mp4"
```
- Verifica el resultado. La versión estática `slide-01.png` (de `cover_slide.html`) queda como
  fallback / miniatura del carrusel.

## B) Orden final de entrega
```
<carpeta>/
  slide-01.png            ← portada estática (cover_slide.html)
  slide-01-ANIMADO.mp4    ← portada animada
  slide-02.png … slide-08.png
  carrusel.html           ← cuerpo (tema)
  cover_slide.html        ← portada estática fuente
  recursos/               ← cover.png, cover_anim_raw.mp4, overlay.html, title-overlay.png
```
En Instagram: sube el `.mp4` como slide 1 y los PNG 2-8. (IG acepta video + imágenes en un carrusel.)

---

## C) Publicar

El carrusel no se publica desde aquí: se entrega por Telegram y la usuaria lo sube. Nada público sin ✅.
