# Assets de producto — estado 2026-10-03

Real Image Policy (brief §11): solo fotos reales. Registro de trazabilidad.

## Verificación inicial (2026-10-02)

Las 14 imágenes con nombre del brief no estaban en ningún repositorio accesible
ni en la librería de medios actual de sender.cl. Se registró la discrepancia
sin generar sustitutos.

## Resolución (2026-10-03)

La persona subió fotografías reales al repositorio. Verificación visual de las
subidas (identificación de contenido, no correspondencia asumida):

| Archivo | Contenido identificado | Estado |
|---|---|---|
| am-10000ss.jpg | Transmisor AMD-10000 ST, panel B.I.S. | en repo |
| familia-am.jpg | Cuatro transmisores AM 1000 (ST/BT) | en repo |
| stl-stal100.jpg | Enlace STL STAL 100 (Studio Transmitter Audio Link) | en repo |
| circuitos.jpg | Circuitos integrados (LM358P, NE555, 4N25) | en repo |
| torre-valparaiso.jpg | Montaje de torre con grúa | en repo |
| am-1000ss.png · am-2500ss.jpg · am-5000ss.jpg · antena-mast.jpg · atu.jpg · hf-balun.jpg · stl-banner.jpg · carro-fotovoltaico.jpg | (nombres del brief, subidos directamente) | en repo |
| sitio-torre.jpg | — | **FALTA: aún no está en el repositorio** |

## Integración

- `src/content/product-images.ts` conecta las fotos al catálogo por contenido
  verificado. El alt describe el archivo; no afirma instalaciones concretas.
- Se sirven estáticas desde `assets/images/products/` (public/).
- `scripts/fetch_product_images.mjs` queda disponible para sincronizar con la
  librería de medios de sender.cl si ésta se actualiza.
- Pendiente de la persona: subir `sitio-torre.jpg` si existe.
