# Cómo crear un tema nuevo para el carrusel noticiero

El **contenido** (qué dice cada slide) es fijo — lo define `SKILL.md`. El **estilo** es libre.
Un "tema" es un archivo `.md` en esta carpeta con un template HTML completo del CUERPO (slides 2-8).
`scrapbook.md` es el default.

## Pasos para un tema nuevo (ej. `revista.md`, `minimal.md`, `dark.md`)

1. **Duplica** `scrapbook.md` → `themes/<nombre>.md`.
2. **Reescribe solo el `<style>`** con tu nuevo look (colores, tipografías, fondo, adornos).
3. **Respeta el CONTRATO de estructura** para que el copy siga encajando. Cada slide debe conservar:
   - Un `.slide` de **1080×1350** con `overflow:hidden` (formato 4:5 obligatorio).
   - `.num` (X / 8) y `.handle` (@tuhandle) en cada slide.
   - Los roles y sus zonas de texto (tag/título/contenido/lista/CTA) — puedes renombrar clases,
     pero el ORDEN y el rol de los 8 slides no cambian:
     `s2` QUÉ PASÓ · `s3` EL MOTIVO · `s4` EL DATO · `s5` ¿Y A TI QUÉ? ·
     `s6` 3 JUGADAS (lista numerada) · `s7hero` REGLA DE ORO · `s8` CIERRE CTA.
   - El slide 8 **siempre** cierra con el CTA `Comenta "100K"` y el "Guárdalo".
4. **Portada:** si tu tema también cambia la portada, duplica `cover/cover-news.html` y
   `cover/overlay.html` y reestíllalos igual; mantén el titular Anton / píldora BREAKING o su
   equivalente. Si no, la portada noticiero default sirve para cualquier tema.
5. **Prueba** renderizando con `export.js` y revisa los 7 PNG del cuerpo antes de usarlo en serio.

## Reglas
- No cambies el tamaño 1080×1350 ni quites `num`/`handle`.
- Google Fonts por CDN en el `<head>`; `export.js` espera `document.fonts.ready`.
- Fuentes pixel (Press Start 2P/VT323) comen tildes y ñ — evítalas para texto en español
  (memoria `feedback_fuentes_pixel_sin_acentos`).
- Para usar un tema distinto del default, dilo al invocar la skill: "usa el tema <nombre>".
