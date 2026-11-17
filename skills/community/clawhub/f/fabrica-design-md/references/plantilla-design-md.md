# Plantilla de DESIGN.md

Copia esta estructura y rellénala con los valores REALES extraídos de las piezas de la
persona. Los comentarios `#` explican qué va en cada campo — bórralos en el archivo final.

Regla de oro: **si un valor no salió de una pieza real, no entra.** Nada de rellenar
con valores "razonables" para que se vea completo. Un archivo corto y verdadero vale más
que uno largo e inventado.

```yaml
---
version: 1.0
name: <nombre-de-la-marca-en-minusculas>

# ─── EL CAMPO QUE HACE EL TRABAJO ───
# Prosa, no lista. Aquí va el CRITERIO: qué se ve, cuál es la firma, y sobre todo
# CUÁNDO cada cosa tiene derecho a aparecer. Si esto queda vacío o genérico,
# el archivo entero no sirve. Apunta a 4-8 frases.
description: "<Lienzo <X> con tinta <Y> y UN acento: <Z>. La firma es <la cosa que
  se repite y hace reconocible la marca>. El acento aparece en <lugares exactos> —
  nunca <los usos prohibidos>. Las superficies son <cómo se separan las cajas>.
  <Qué manda el ritmo: fotos reales, capturas, ilustración, tipografía sola>.>"

# ─── COLORES ───
# Tres grupos, y solo tres. Si salen dos acentos, uno es ruido: decide cuál.
colors:
  canvas: "<#______>"        # el fondo
  surface-1: "<#______>"     # cajas y paneles
  hairline: "<#______>"      # bordes

  ink: "<#______>"           # titulares
  ink-body: "<#______>"      # cuerpo
  ink-muted: "<#______>"     # secundario — MIDE ESTE, es el que suele fallar

  accent: "<#______>"        # UNO solo
  # opcional, solo si existen de verdad en las piezas:
  # semantic-ok / semantic-warn / semantic-error

# ─── TIPOGRAFÍA ───
# Declara SIEMPRE una pila de respaldo real: si la fuente no carga, el navegador
# se va a Times y arruina la pieza.
typography:
  stack-display: "<Fuente>, <respaldo>, sans-serif"
  stack-body: "<Fuente>, <respaldo>, sans-serif"
  stack-mono: "<Fuente>, ui-monospace, Menlo, monospace"   # si aplica

  display-lg:
    fontSize: <__px>
    fontWeight: <___>
    lineHeight: <_.__>
    letterSpacing: <-_._px>   # en titulares grandes casi siempre negativo
  display-md:
    fontSize: <__px>
    fontWeight: <___>
  body:
    fontSize: <__px>
    lineHeight: <_.__>
  eyebrow:                    # el rótulo pequeño en versalitas, si lo usa
    fontSize: <__px>
    fontWeight: <___>
    letterSpacing: <_px>
    textTransform: uppercase

# ─── FORMA Y AIRE ───
rounded:
  card: <__px>
  pill: 999px
spacing:
  base: <_px>
  scale: [<...>]

# ─── COMPONENTES ───
# Solo los que la marca de verdad usa. No inventes un catálogo.
components:
  boton-primario:
    background: accent
    color: <la tinta que MIDIÓ bien encima del acento>
    radius: pill
    minHeight: 44px           # piso táctil, nunca menos
  panel:
    background: surface-1
    border: "1px solid hairline"

# ─── REGLAS DE USO ───
# La parte que separa un sistema de una lista de colores.
rules:
  acento:
    - "El acento va en: <lugares exactos>."
    - "NUNCA <los usos prohibidos: fondo de sección, degradados, decoración>."
  tipografia:
    - "<La firma, escrita como orden ejecutable>."
    - "<Reglas de peso, interletrado, mezcla de familias>."
  contraste:
    - "Piso de texto secundario: <#______> (<ratio> medido). Por debajo no se usa."
  imagen:
    - "<Qué imágenes SÍ: fotos propias, capturas reales, ilustración propia>."
    - "<Qué imágenes NO: stock, IA genérica, logos ajenos>."
  prohibido:
    - "Degradado morado de IA, héroe centrado sobre malla oscura, tres tarjetas
       iguales en fila, glassmorphism en todo, todo centrado."
    - "Testimonios, cifras o logos de medios inventados."

  # ─── BLOQUE CÓDIGO ───
  # Universal: la IA reintroduce estos errores sola en casi toda pieza web.
  # Déjalo tal cual, y añade los que le hayan mordido a esta persona en particular.
  codigo:
    - "Toda animación de aparición por scroll lleva respaldo, o la página sale en
       blanco si el JS falla: <noscript><style>.rev{opacity:1;transform:none}</style></noscript>."
    - "Ningún botón de pago o de contacto se entrega con href='#'. O lleva el enlace
       real, o lleva un comentario imposible de pasar por alto."
    - "Nada se oculta solo con opacity:0 — el lector de pantalla igual lo lee.
       Usar hidden o display:none, y role='status' para lo que aparece tras una acción."
    - "Anclas de navegación: scroll-margin-top igual al alto del encabezado fijo."
    - "Barra fija inferior: la clase que compensa su alto en el body hay que AÑADIRLA
       en el JS, no solo declararla en el CSS."

# ─── EXCEPCIÓN ───
# Casi toda marca tiene dos superficies: una para VENDER y otra para ENSEÑAR o
# para la herramienta. Si existe, escríbela. Si de verdad no existe, borra el bloque.
exceptions:
  <nombre>:
    donde: "<dónde vive>"
    que: "<en qué se diferencia>"
    porque: "<la razón funcional, no estética>"
    regla: "No mezclar las dos superficies en una misma página."

# ─── DE DÓNDE SALIÓ ───
# Trazabilidad: en seis meses nadie se acuerda por qué el acento es ese.
sources:
  - "<pieza o archivo del que se extrajo>"
  - "Contrastes medidos el <fecha>, no estimados."
---
```
