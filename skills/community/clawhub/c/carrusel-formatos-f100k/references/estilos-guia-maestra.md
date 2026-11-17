# GUÍA MAESTRA DE CARRUSELES — Generados directamente con Claude
> FÓRMULA 100K · Versión 2.0 · Mayo 2026 · 25 estilos

---

## CÓMO FUNCIONA ESTO

Claude puede generar carruseles de dos formas principales:

### MOTOR 1 — HTML/CSS (recomendado para la mayoría de estilos)
Claude genera un archivo `.html` completo que abres en cualquier navegador. Cada slide es una pantalla con diseño real: gradientes, glassmorphism, patrones, animaciones, tipografía de Google Fonts, emojis, formas geométricas, badges, etc.

**Para exportar como imágenes:** abres el HTML en el navegador, presionas cada slide y haces captura de pantalla, o usas la extensión "Full Page Screen Capture".

### MOTOR 2 — Imágenes con Banana (Gemini AI)
Claude genera cada slide como una imagen PNG real usando la skill de generación de imágenes. Ideal cuando quieres fotografías, personas, escenas o ilustraciones dentro del carrusel.

### MOTOR 3 — Híbrido
Banana genera las imágenes → se usan como fondos dentro de un HTML/CSS. Máximo control visual.

---

## CÓMO PEDIR UN CARRUSEL (estructura base)

Cuando pidas un carrusel a Claude, incluye siempre estos 5 datos:

```
1. MOTOR: HTML/CSS, Banana (imágenes), o Híbrido
2. ESTILO: nombre del estilo de esta guía (ej: "Dark Neón Tech")
3. PROPÓSITO: qué tipo de contenido (tutorial, lista, historia, estadísticas...)
4. TEMA: de qué trata el carrusel
5. SLIDES: cuántos slides quieres (recomendado: 7-10)
```

**Ejemplo mínimo funcional:**
> "Hazme un carrusel HTML/CSS estilo Bold Statement de 8 slides sobre los 7 errores que cometen los emprendedores al crear contenido."

---

---

# ESTILOS DE CARRUSEL — CATÁLOGO COMPLETO

---

## ESTILO 01 — BOLD STATEMENT

**Energía:** impacto inmediato, confianza, autoridad  
**Ideal para:** resultados, frases poderosas, tips cortos, lanzamientos, motivación  
**Motor:** HTML/CSS

### Características visuales
- Tipografía: Display ultra bold (Bebas Neue, Anton, Black Han Sans) — ocupa 70-80% del slide
- Máximo 3-5 palabras por slide
- Fondo: color sólido saturado (cambia por slide o constante)
- Texto: color de alto contraste con el fondo
- Sin imágenes
- Puede incluir emojis grandes como acento visual

### Paletas sugeridas
- Negro + Amarillo eléctrico
- Naranja intenso + Blanco
- Morado oscuro + Blanco
- Rojo + Blanco
- Azul royal + Amarillo

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo BOLD STATEMENT con estas especificaciones:

TEMA: [escribe tu tema aquí]
SLIDES: [número de slides, ej: 8]
PALETA: [ej: fondo negro, texto amarillo eléctrico / o elige tú]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografía: Bebas Neue (importada de Google Fonts) para titulares, DM Sans para textos secundarios
- Cada slide tiene un mensaje corto de máximo 5 palabras en tipografía gigante (mínimo 80px)
- Fondo sólido de color constante o que varía por slide (decide tú según el tema)
- Texto de alto contraste con el fondo
- Sin imágenes, solo tipografía y color
- Slide 1: hook de apertura impactante
- Slides 2-N: un punto por slide, mensaje ultra corto y directo
- Slide final: CTA simple ("Guárdalo 💾" o "Sígueme @[handle]")
- El HTML debe mostrar los slides en secuencia vertical para facilitar la captura de pantalla
- Cada slide separado visualmente con una línea o espacio
```

---

## ESTILO 02 — MINIMALISTA LIMPIO

**Energía:** calma, elegancia, lujo, claridad  
**Ideal para:** coaches, personal branding premium, reflexiones, tips de lifestyle, bienestar  
**Motor:** HTML/CSS

### Características visuales
- Tipografía: Serif elegante (Playfair Display, Cormorant) + Sans fina (DM Sans, Inter Light)
- Mucho espacio en blanco (negativo)
- Fondo: blanco, crema (#FAF8F5) o gris perla muy suave
- Máximo 2 colores en todo el carrusel + 1 acento pequeño
- Sin ruido visual, composición limpia centrada o alineada a la izquierda
- Líneas decorativas finas como separadores o acentos

### Paletas sugeridas
- Blanco + Negro + Dorado (acento)
- Crema + Marrón oscuro + Terracota (acento)
- Gris perla + Negro + Verde salvia (acento)
- Blanco + Azul navy + Sin acento

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo MINIMALISTA LIMPIO con estas especificaciones:

TEMA: [escribe tu tema aquí]
SLIDES: [número de slides, ej: 7]
PALETA: [ej: fondo crema #FAF8F5, texto marrón oscuro, acento terracota / o elige tú]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografías: Playfair Display (titulares, serif elegante) + DM Sans (cuerpo, sans limpia) — importar de Google Fonts
- Fondo claro (blanco, crema o gris muy suave)
- Mucho espacio en blanco — los elementos no llenan el slide, respiran
- Alineación: centrada o izquierda (elige la que mejor funcione)
- Líneas decorativas finas (1-2px) como separadores o acentos bajo los títulos
- Numeración elegante de slides (ej: "01", "02") en tipografía pequeña
- Máximo 2-3 colores en todo el carrusel
- Slide 1: título del tema + subtítulo corto
- Slides 2-N: titular del punto + 2-3 líneas de desarrollo
- Slide final: frase de cierre + handle de Instagram pequeño
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 03 — DARK NEÓN TECH

**Energía:** premium, misterioso, futurista, alto impacto  
**Ideal para:** marketing digital, emprendimiento, dinero, tecnología, fitness, resultados  
**Motor:** HTML/CSS

### Características visuales
- Fondo: negro (#000000) o gris carbón muy oscuro (#0D0D0D)
- Texto principal: color neón (verde #39FF14 / lila #BF5FFF / rosa #FF6B9D / cyan #00FFFF)
- Tipografía bold o sans moderna
- Efecto de glow/brillo en el texto neón (text-shadow CSS)
- Cards o badges con borde del color neón
- Puede incluir líneas decorativas finas en neón

### Paletas sugeridas
- Negro + Verde neón + Blanco (para texto secundario)
- Negro + Lila neón + Gris claro
- Negro + Cyan + Rosa (dos neones)
- Negro + Amarillo neón

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo DARK NEÓN TECH con estas especificaciones:

TEMA: [escribe tu tema aquí]
SLIDES: [número de slides, ej: 8]
COLOR NEÓN: [elige: verde #39FF14 / lila #BF5FFF / rosa #FF6B9D / cyan #00FFFF]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Fondo: negro #000000 o gris muy oscuro #0D0D0D
- Tipografía: Space Grotesk o DM Sans (bold para titulares) — importar de Google Fonts
- Color del texto principal: [el neón elegido] con efecto glow (text-shadow CSS)
- Texto secundario/cuerpo: blanco #FFFFFF o gris claro #CCCCCC
- Elementos decorativos: líneas finas del color neón, badges con borde neón, separadores
- Slide 1: portada con el hook principal en neón, grande
- Slides 2-N: número del punto en neón grande + titular + 2-3 líneas de desarrollo en blanco
- Slide final: CTA en neón + handle pequeño
- Efecto glow real en los textos de color neón usando CSS text-shadow
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 04 — EDITORIAL REVISTA

**Energía:** sofisticado, curado, intelectual, profesional  
**Ideal para:** personal branding de alto nivel, liderazgo, moda, marketing, educación premium  
**Motor:** HTML/CSS

### Características visuales
- Mezcla de Serif grande (titulares) + Sans pequeña (cuerpo) — contraste tipográfico
- Diseño asimétrico o en columnas
- Numeración elegante visible (01, 02, 03...)
- Uso de mayúsculas en palabras clave
- Líneas de separación horizontales y verticales como estructura
- Acento de color único y sofisticado
- Sensación de "portada de revista"

### Paletas sugeridas
- Blanco + Negro + Vino #8B0000
- Blanco + Negro + Dorado #C9A84C
- Blanco + Negro + Azul royal #1B3A6B
- Crema + Marrón + Rojo ladrillo

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo EDITORIAL REVISTA con estas especificaciones:

TEMA: [escribe tu tema aquí]
SLIDES: [número de slides, ej: 7]
COLOR ACENTO: [ej: vino #8B0000 / dorado #C9A84C / azul royal #1B3A6B]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografías: Playfair Display (titulares serif grandes) + Inter o DM Sans (cuerpo sans pequeña) — importar de Google Fonts
- Diseño con estructura de revista: texto organizado en zonas, líneas horizontales de separación, numeración visible ("01", "02") en tipografía pequeña
- Fondo blanco o crema muy suave
- El titular de cada slide en mayúsculas o small-caps, serif grande
- El color acento aparece solo en detalles: número, línea decorativa, una palabra resaltada — no en grandes bloques
- Composición asimétrica o con jerarquía clara (no todo centrado)
- Slide 1: portada estilo "cover de revista" con el título del tema
- Slides 2-N: número de slide (grande, acento) + titular serif + desarrollo en sans pequeña
- Slide final: cierre editorial + handle pequeño
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 05 — PASTEL SOFT & EMOJI HERO

**Energía:** amigable, accesible, dulce, cercana  
**Ideal para:** tips de bienestar, educación, contenido femenino, nutrición, lifestyle, comunidad  
**Motor:** HTML/CSS

### Características visuales
- Fondo en tonos pastel (melocotón, lila suave, menta, rosa palo, celeste)
- Emoji enorme como elemento visual principal de cada slide (reemplaza una imagen)
- Tipografía redondeada y amigable (Nunito, Poppins, Quicksand)
- Texto corto y directo
- Puede variar el color de fondo por slide dentro de la paleta pastel
- Borde redondeado en cards o elementos internos

### Paletas sugeridas
- Rosa palo #FFD1DC + Lila #DCC6E0 + Menta #C8E6C9 + Melocotón #FFDAB9
- Celeste #BDE0FE + Lavanda #CDB4DB + Verde suave #CAFFBF
- Amarillo mantequilla #FFF3B0 + Rosa suave #FFB3C1 + Verde menta #B5EAD7

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo PASTEL SOFT con EMOJI HERO con estas especificaciones:

TEMA: [escribe tu tema aquí]
SLIDES: [número de slides, ej: 8]
PALETA: [ej: rosa palo, lila, menta y melocotón / o elige tú una paleta pastel]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografía: Poppins o Nunito (redondeada, amigable) — importar de Google Fonts
- Cada slide tiene un emoji gigante (150-200px) como elemento visual principal, centrado en la parte superior o media
- El fondo de cada slide varía en tonos pastel suaves (distintos slides, distintos pasteles de la misma paleta)
- Texto corto: máximo 2 líneas de titular + 1-2 de desarrollo
- Esquinas redondeadas en elementos internos (cards, badges)
- Numeración discreta del punto (ej: "TIP 3" en badge pequeño redondeado)
- Slide 1: portada con emoji grande + título del tema
- Slides 2-N: emoji central + tip/punto en texto claro
- Slide final: emoji de celebración o corazón + CTA amigable
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 06 — GRADIENTE FLUIDO

**Energía:** vibrante, moderno, enérgico, visual  
**Ideal para:** lanzamientos, marketing digital, educación moderna, tecnología, bienestar  
**Motor:** HTML/CSS

### Características visuales
- Fondo: gradiente suave de 2-3 colores que cubre todo el slide
- Texto: blanco o muy oscuro (según el gradiente)
- Tipografía sans-serif bold o medium
- Sin imágenes, el gradiente ES el elemento visual
- Puede incluir formas geométricas semitransparentes como decoración
- El gradiente puede ser constante o variar de slide en slide

### Paletas sugeridas (pares de gradiente)
- Morado → Rosa: #7B2D8B → #FF6B9D
- Azul → Cyan: #1B3A6B → #00C9FF
- Naranja → Amarillo: #FF6B35 → #FFD700
- Verde → Azul: #11998E → #38EF7D
- Rosa → Naranja: #FC5C7D → #6A82FB

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo GRADIENTE FLUIDO con estas especificaciones:

TEMA: [escribe tu tema aquí]
SLIDES: [número de slides, ej: 8]
GRADIENTE: [ej: morado #7B2D8B → rosa #FF6B9D / o elige tú el gradiente]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografía: DM Sans o Montserrat (bold para titulares, regular para cuerpo) — importar de Google Fonts
- Fondo de cada slide: gradiente CSS linear-gradient de los colores indicados (puedes variar el ángulo entre slides para dar dinamismo)
- Texto: blanco (#FFFFFF) con text-shadow suave para legibilidad
- Elementos decorativos opcionales: círculos o elipses semitransparentes (rgba blanco 10-20% de opacidad) como elementos de fondo
- Números de slide en badge redondeado blanco semi-transparente
- Slide 1: portada con gradiente + título grande + subtítulo
- Slides 2-N: número/badge + titular bold + 2-3 líneas de desarrollo
- Slide final: CTA en blanco + separador + handle
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 07 — GLASSMORPHISM PREMIUM

**Energía:** futurista, premium, tech, innovador  
**Ideal para:** tecnología, apps, fintech, educación digital, emprendimiento moderno  
**Motor:** HTML/CSS

### Características visuales
- Fondo: gradiente colorido brillante (el "vidrio" necesita color detrás)
- Card central translúcida con efecto blur (backdrop-filter: blur)
- Borde sutil del card (rgba blanco 30%)
- Texto dentro del card en blanco o muy oscuro
- Sensación de profundidad y capas
- Tipografía moderna y limpia

### Paletas de fondo sugeridas
- Gradiente azul-morado intenso + cards blancos translúcidos
- Gradiente verde-azul + cards blancos translúcidos
- Gradiente naranja-rosa + cards blancos translúcidos

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo GLASSMORPHISM PREMIUM con estas especificaciones:

TEMA: [escribe tu tema aquí]
SLIDES: [número de slides, ej: 7]
GRADIENTE DE FONDO: [ej: azul intenso #1B3A6B → morado #7B2D8B / o elige tú]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografía: Inter o SF Pro (usar Inter desde Google Fonts)
- Fondo del slide: gradiente colorido intenso que cubre todo
- Sobre el fondo: una card central con efecto glassmorphism real:
  * background: rgba(255, 255, 255, 0.15)
  * backdrop-filter: blur(20px)
  * border: 1px solid rgba(255, 255, 255, 0.3)
  * border-radius: 24px
  * box-shadow: 0 8px 32px rgba(0,0,0,0.2)
- El contenido (texto) vive dentro del card translúcido
- Texto: blanco #FFFFFF para titulares, rgba(255,255,255,0.85) para cuerpo
- Puede haber elementos decorativos de fondo: círculos difuminados de colores (type: blur-circle)
- Slide 1: portada con card glassmorphism + título + subtítulo
- Slides 2-N: número en badge + titular + desarrollo dentro del card
- Slide final: CTA + handle
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 08 — SCRAPBOOK / COLLAGE HUMANO

**Energía:** auténtico, cálido, humano, imperfecto-perfecto  
**Ideal para:** detrás de escenas, historia personal, viaje, contenido casual, marca personal  
**Motor:** HTML/CSS (con elementos decorativos CSS)

### Características visuales
- Elementos en ángulos distintos (rotados ligeramente)
- Mezcla de tipografías: una display + una handwriting
- Paleta tierra o suave
- Fondo texturizado (simulado con CSS: ruido, papel)
- Elementos superpuestos: stickers, emojis, subrayados, círculos "dibujados"
- Sensación de "armado a mano", no perfecto

### Paletas sugeridas
- Beige #F5F0E8 + Verde salvia #8FAF8A + Terracota #C17F5A + Blanco roto
- Crema + Rosa palo + Marrón suave + Negro
- Blanco + Naranja tostado + Verde oliva + Amarillo mantequilla

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo SCRAPBOOK / COLLAGE con estas especificaciones:

TEMA: [escribe tu tema aquí]
SLIDES: [número de slides, ej: 7]
PALETA: [ej: beige, verde salvia, terracota / o elige tú paleta tierra o suave]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografías: Caveat o Indie Flower (handwriting) + Poppins o DM Sans (sans legible) — importar de Google Fonts
- Fondo: beige o crema con efecto de textura de papel (usar CSS noise o patrón sutil)
- Los elementos no están perfectamente centrados: rotaciones sutiles (±2° a ±5°) en bloques de texto
- Emojis usados como stickers decorativos, algunos rotados
- Subrayados y círculos decorativos dibujados en SVG inline simple (estilo "a mano")
- Cada slide tiene una composición distinta (no todas iguales)
- Usar bloques de color (post-it style) como fondo de partes del texto
- Slide 1: portada tipo "nota personal" con el tema
- Slides 2-N: composición asimétrica con el punto principal
- Slide final: nota de cierre + "guárdalo para después" + handle
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 09 — HEADLINE HERO (DATO GIGANTE)

**Energía:** impacto de datos, autoridad, estadísticas que golpean  
**Ideal para:** estadísticas, resultados de clientes, datos de mercado, antes/después numérico  
**Motor:** HTML/CSS

### Características visuales
- El número o porcentaje ocupa 60-70% del slide
- Texto explicativo pequeño abajo o arriba del número
- Fondo puede ser sólido, gradiente o dark
- Tipografía display para el número, sans para el texto
- 1 color de acento que destaca el número

### Paletas sugeridas
- Blanco + Negro + Acento naranja
- Negro + Blanco + Acento amarillo
- Azul oscuro + Blanco + Acento cyan
- Crema + Marrón oscuro + Acento terracota

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo HEADLINE HERO (dato gigante) con estas especificaciones:

TEMA: [escribe tu tema aquí — idealmente datos, estadísticas, resultados]
SLIDES: [número de slides, ej: 7]
PALETA: [ej: fondo blanco, número en negro, acento naranja / o elige tú]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografías: Bebas Neue o Anton (para el número/dato hero, gigante) + DM Sans (para texto explicativo) — importar de Google Fonts
- El número, porcentaje o dato principal: tipografía gigante (mínimo 180px), centrado, color de acento o color principal
- Texto explicativo: sans pequeña (18-24px), debajo o encima del número
- Fondo limpio (sólido o gradiente sutil)
- Línea decorativa fina o punto del color acento como separador
- Slide 1: portada con el dato más impactante del tema
- Slides 2-N: cada slide = 1 dato grande + explicación corta
- Slide final: síntesis o CTA
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 10 — SPLIT SCREEN (IMAGEN AI + TEXTO)

**Energía:** visual, equilibrado, moderno, dinámico  
**Ideal para:** tutoriales con visual, testimoniales, comparaciones, pasos con ejemplo  
**Motor:** Banco de imágenes Banana + HTML/CSS (híbrido)

### Características visuales
- Cada slide dividido horizontalmente o verticalmente: imagen arriba (o izquierda) / texto abajo (o derecha)
- La imagen la genera Banana (Gemini AI)
- Texto limpio en la mitad sin imagen
- Tipografía clara, buena jerarquía

### PROMPT PARA COPIAR Y PEGAR

```
Necesito un carrusel en formato SPLIT SCREEN con imagen generada por IA. 
El proceso es en dos pasos — síguelo exactamente:

PASO 1 — GENERA LAS IMÁGENES (con Banana/skill de imágenes):
Genera [número de slides] imágenes con este estilo visual: [describe el estilo: minimalista, lifestyle, abstracto, etc.]
Tema visual de las imágenes: [ej: "espacio de trabajo minimalista con laptop", "persona leyendo en café", "naturaleza abstracta suave"]
Formato de cada imagen: cuadrado o 1080x540px (mitad de slide portrait)

PASO 2 — GENERA EL HTML:
Con las imágenes generadas, crea el carrusel HTML/CSS con estas especificaciones:
- Formato total del slide: 1080x1350px (portrait 4:5)
- Cada slide dividido: mitad superior = imagen, mitad inferior = texto
- [O alternativa: dividido verticalmente: lado izquierdo imagen, lado derecho texto]
- Tipografía: [elige estilo y fuente]
- Paleta del texto: [colores]
- Slide 1: portada [puede ser solo texto o con imagen]
- Slides 2-N: split con imagen + punto de contenido
- Slide final: CTA
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 11 — FULL BLEED ATMOSFÉRICO

**Energía:** emocional, cinematográfico, storytelling, impacto visual total  
**Ideal para:** historias personales, narrativas de marca, inspiración, reflexiones profundas  
**Motor:** Banana (imagen de fondo) + HTML/CSS overlay

### Características visuales
- Imagen generada por IA ocupa el 100% del slide como fondo
- Overlay oscuro semitransparente sobre la imagen para legibilidad del texto
- Texto en blanco, tipografía serif o sans elegante
- El texto es corto — la imagen hace el trabajo emocional
- Cada slide tiene una imagen distinta que evoca la historia

### PROMPT PARA COPIAR Y PEGAR

```
Necesito un carrusel FULL BLEED ATMOSFÉRICO. Dos pasos:

PASO 1 — GENERA LAS IMÁGENES (con Banana):
Para cada slide, genera una imagen de fondo atmosférica:
- Slide 1 (portada): [describe la escena — ej: "amanecer sobre ciudad, tonos cálidos, cinematográfico"]
- Slide 2: [escena para ese punto]
- Slide 3: [escena para ese punto]
[...continuar por slide]
Estilo general de las imágenes: [ej: cinematográfico, editorial, naturaleza, urbano] 
Paleta de tonos: [cálido / frío / neutro / oscuro]
Formato: 1080x1350px

PASO 2 — GENERA EL HTML:
Con las imágenes generadas, construí el carrusel con:
- Cada imagen como background-image de su slide (100% del slide, object-fit: cover)
- Overlay oscuro semitransparente: rgba(0,0,0,0.45) sobre cada imagen
- Texto centrado sobre el overlay, en blanco
- Tipografía: [elige — serif elegante tipo Playfair o sans bold tipo DM Sans]
- Texto corto: máximo 2-3 líneas por slide
- Slide 1: portada con título principal
- Slides 2-N: frase o punto corto con imagen evocadora de fondo
- Slide final: reflexión de cierre + CTA + handle
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 12 — MITOS VS REALIDAD (doble paleta)

**Energía:** autoridad, corrección, revelación, posicionamiento experto  
**Ideal para:** desmentir creencias, educar, posicionarse contra el mercado  
**Motor:** HTML/CSS

### Características visuales
- Slides de MITO: fondo oscuro o rojo, emoji ❌, texto del mito tachado o en color "error"
- Slides de REALIDAD: fondo claro o verde, emoji ✅, texto de la realidad en positivo
- Alternancia visual clara entre mito y realidad
- Bold tipografía para el contraste

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo MITOS VS REALIDAD con estas especificaciones:

TEMA: [escribe tu tema — ej: "mitos sobre crear contenido en Instagram"]
CANTIDAD DE PARES: [ej: 4 pares = 4 mitos + 4 realidades = 9 slides con portada y cierre]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografía: DM Sans bold para titulares, DM Sans regular para cuerpo — importar de Google Fonts
- SLIDES DE MITO:
  * Fondo oscuro: gris carbón #1A1A1A o negro
  * Badge "MITO ❌" en rojo o naranja arriba
  * El mito en texto blanco, tamaño grande
  * Energía: "esto es lo que crees, pero está mal"
- SLIDES DE REALIDAD:
  * Fondo claro: blanco o crema
  * Badge "REALIDAD ✅" en verde o el color de tu marca arriba
  * La realidad en texto oscuro, mismo tamaño
  * Energía: "esto es lo que realmente funciona"
- Slide 1: portada impactante sobre el tema
- Alternancia: slide portada → Mito 1 → Realidad 1 → Mito 2 → Realidad 2... → CTA
- Slide final: síntesis + CTA
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 13 — CHECKLIST INTERACTIVO

**Energía:** participación, autoevaluación, guardar, viralizar  
**Ideal para:** diagnósticos, puntos de chequeo, auditorías, "¿lo tienes o no?"  
**Motor:** HTML/CSS

### Características visuales
- Cada slide tiene un ítem con checkbox visual grande
- Los checkboxes pueden estar "marcados" o "vacíos" según el diseño
- Tipografía clara y legible
- Paleta limpia y amigable
- El último slide pregunta "¿cuántos marcaste?" con escala de resultado

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo CHECKLIST INTERACTIVO con estas especificaciones:

TEMA: [ej: "10 señales de que tu contenido no está funcionando"]
CANTIDAD DE ÍTEMS: [ej: 8 ítems = 10 slides con portada y cierre]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografía: Poppins o DM Sans — importar de Google Fonts
- Paleta: [ej: fondo blanco, texto oscuro, acento en [tu color de marca]]
- Cada slide de ítem tiene:
  * Checkbox grande visual (cuadrado redondeado, estilo UI moderno) — puede estar vacío o tachado/marcado
  * Número del ítem en badge pequeño
  * El ítem en tipografía grande y clara
  * Opcionalmente: 1 línea explicativa pequeña
- Los checkboxes vacíos sugieren "¿lo tienes?", los marcados confirman
- Slide 1: portada con hook + "¿cuántos de estos tienes?"
- Slides 2-N: un ítem por slide con su checkbox
- Slide final: escala de resultados ("0-3: necesitas trabajar en X / 4-6: vas bien / 7+: eres un crack") + CTA
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 14 — FAQ TIPO CHAT

**Energía:** conversacional, accesible, resuelve objeciones, humano  
**Ideal para:** responder preguntas frecuentes, vencer objeciones de venta, acercarse a la audiencia  
**Motor:** HTML/CSS

### Características visuales
- Simula una interfaz de mensajería (WhatsApp/DM style)
- Burbuja de pregunta (lado izquierdo, gris)
- Burbuja de respuesta (lado derecho, color de marca)
- Tipografía redondeada
- Fondo muy claro o blanco

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo FAQ TIPO CHAT (interfaz de mensajería) con estas especificaciones:

TEMA: [ej: "las preguntas más frecuentes sobre [tu producto/servicio]"]
CANTIDAD DE FAQs: [ej: 5 preguntas = 7 slides con portada y cierre]
COLOR DE MARCA (para las burbujas de respuesta): [hex de tu color]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografía: Poppins o Nunito (redondeada) — importar de Google Fonts
- Fondo: blanco o gris muy claro (#F5F5F5)
- Burbuja de PREGUNTA:
  * Alineada a la izquierda
  * Fondo gris claro (#E5E5EA)
  * Texto oscuro
  * Avatar o ícono de "usuario" pequeño a la izquierda
  * border-radius con esquina inferior izquierda recta (estilo chat real)
- Burbuja de RESPUESTA:
  * Alineada a la derecha
  * Fondo del color de marca
  * Texto blanco
  * Avatar o nombre de marca a la derecha
  * border-radius con esquina inferior derecha recta
- Slide 1: portada con título "Preguntas que me hacen todo el tiempo 💬"
- Slides 2-N: un par pregunta/respuesta por slide (o dos pares cortos si caben)
- Slide final: invitación a preguntar más + CTA
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 15 — ANTES / DESPUÉS DRAMÁTICO

**Energía:** transformación, prueba de resultado, emoción, ventas  
**Ideal para:** testimoniales, demostración de resultados, posicionamiento por contraste  
**Motor:** HTML/CSS o Banana + HTML/CSS (si quieres imágenes)

### Características visuales
- Slides "ANTES": paleta fría/oscura, energía pesada, problema evidente
- Slides "DESPUÉS": paleta cálida/vibrante, energía positiva, resultado claro
- Transición visual marcada entre las dos fases
- El contraste de color ES el storytelling

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo ANTES/DESPUÉS DRAMÁTICO con estas especificaciones:

TEMA/HISTORIA: [ej: "antes y después de aplicar la estrategia de contenido de FÓRMULA 100K"]
ESTRUCTURA: [ej: 2-3 slides de ANTES + 2-3 slides de DESPUÉS + portada y cierre]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografía: DM Sans bold — importar de Google Fonts
- SLIDES DE "ANTES":
  * Fondo oscuro o frío: gris oscuro, azul apagado o negro
  * Badge "ANTES" en esquina superior con fondo rojo o gris oscuro
  * Texto describiendo el problema/situación anterior — en blanco o gris claro
  * Emoji que refuerce la negatividad/dificultad (😤, 😩, ❌)
  * Energía pesada, opresiva
- SLIDES DE "DESPUÉS":
  * Fondo claro, cálido o vibrante: blanco, crema, o el color de marca
  * Badge "DESPUÉS" en esquina superior con fondo verde o dorado
  * Texto describiendo el resultado — en color oscuro
  * Emoji de celebración o éxito (🚀, ✅, 🎯, 💰)
  * Energía liviana, celebratoria
- Slide 1: portada que anticipa la transformación ("De [punto A] a [punto B]")
- Estructura: portada → ANTEs → ANTES → DESPUÉS → DESPUÉS → Cómo ocurrió → CTA
- Slide final: CTA con cómo acceder a ese resultado
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 16 — BRUTALIST / SWISS GRID

**Energía:** crudo, experto, anti-plantilla, autoridad de diseñador
**Ideal para:** opiniones contrarias, "reglas que rompo", takes fuertes, posicionamiento experto
**Motor:** HTML/CSS

### Características visuales
- Fondo blanco roto (#F4F1EA) o blanco puro — nada de gradientes ni sombras
- Líneas hairline negras (1px solid #111) que dividen el slide en una grilla visible
- Tipografía condensada gigantísima alineada a la izquierda (flush-left), sin centrar
- Un único bloque de color puro por slide (naranja #FF3B00 o azul #0000FE)
- Número de slide impreso enorme en una esquina
- Cero esquinas redondeadas, cero ruido — precisión cruda

### Paletas sugeridas
- Blanco roto #F4F1EA + Negro #111 + Naranja #FF3B00
- Blanco puro + Negro + Azul eléctrico #0000FE
- Blanco roto + Negro + Rojo #E5322D

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo BRUTALIST / SWISS GRID con estas especificaciones:

TEMA: [escribe tu tema aquí]
SLIDES: [número de slides, ej: 8]
COLOR ACENTO: [naranja #FF3B00 / azul #0000FE / rojo #E5322D]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografía: Archivo Black o Anton para titulares (condensada, gigante), Space Mono para etiquetas — importar de Google Fonts
- Fondo blanco roto #F4F1EA o blanco puro
- Líneas hairline negras (1px solid #111) que dividen el slide en una grilla visible (columnas y baseline)
- Titular flush-left (alineado a la izquierda), nunca centrado, ocupando gran parte del slide
- Un solo bloque de color acento por slide (un rectángulo sólido o una palabra resaltada)
- Número de slide impreso gigante en una esquina (ej: "01" en 120px+)
- Sin sombras, sin esquinas redondeadas, sin gradientes — estética cruda y precisa
- Slide 1: portada con el hook en tipografía condensada masiva
- Slides 2-N: un punto por slide con número grande + titular flush-left
- Slide final: CTA directo + handle
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 17 — RECIBO / TICKET / BOARDING PASS

**Energía:** novedoso, tangible, coleccionable, screenshot-eable
**Ideal para:** listas enmarcadas como "la cuenta", itinerarios de pasos, "lo que recibes", stack de valor/precio
**Motor:** HTML/CSS

### Características visuales
- Un objeto falso centrado por slide: recibo, ticket o pase de abordar
- Recibo: tira blanca angosta, texto monospace, divisores punteados, borde inferior dentado (mask con triángulos repetidos), código de barras falso (repeating-linear-gradient), línea "TOTAL"
- Boarding pass: tarjeta de dos paneles separados por línea perforada punteada con muescas (círculos ::before/::after del color de fondo)
- Fondo kraft o papel térmico apagado
- Sensación de objeto real que se reconoce al instante

### Paletas sugeridas
- Papel térmico #FBFBF7 + Tinta #1A1A1A + fondo kraft #D9CDB8
- Blanco recibo + Negro + acento rojo sello #C0392B
- Crema ticket #F4ECD8 + Marrón tinta + verde menta sello

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo RECIBO / TICKET / BOARDING PASS con estas especificaciones:

TEMA: [escribe tu tema aquí — ej: "lo que incluye mi programa" o "tu itinerario de 7 pasos"]
SLIDES: [número de slides, ej: 7]
OBJETO: [recibo / ticket de cine / pase de abordar — elige el que mejor encaje]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografía: Courier Prime o JetBrains Mono (monospace) — importar de Google Fonts
- Fondo del slide: kraft #D9CDB8 o papel térmico apagado
- Objeto falso centrado por slide con detalles skeuomórficos reales:
  * Recibo: tira blanca angosta, divisores punteados (border-bottom dashed), borde inferior DENTADO usando CSS mask con triángulos repetidos, código de barras falso con repeating-linear-gradient, línea "TOTAL" destacada
  * Boarding pass: tarjeta de 2 paneles separados por línea perforada punteada, con muescas circulares (::before/::after en color de fondo) a los lados de la perforación
- Encabezado del objeto con un "logo"/nombre de marca pequeño en mayúsculas
- Slide 1: portada — el objeto presentando el tema (ej: "TU TICKET A [resultado]")
- Slides 2-N: cada slide = un objeto con un punto/ítem detallado como línea de recibo
- Slide final: objeto con "TOTAL" = el resultado/CTA + handle
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 18 — CODE EDITOR / TERMINAL

**Energía:** insider, técnico, credibilidad inmediata, futurista
**Ideal para:** contenido de IA/tech, "los prompts que uso", frameworks como pseudo-código, lógica de pasos
**Motor:** HTML/CSS

### Características visuales
- Chrome de IDE oscuro (#1E1E2E Catppuccin o #282A36 Dracula)
- Barra de título con tres luces de semáforo (rojo #FF5F56, amarillo #FFBD2E, verde #27C93F)
- Gutter izquierdo con números de línea (#6272A4)
- Texto con resaltado de sintaxis: keywords rosa #FF79C6, strings verde #50FA7B, comentarios gris #6272A4
- Cursor de bloque parpadeante
- Alternativa terminal: prompt `$`, salida monospace

### Paletas sugeridas
- Dracula: fondo #282A36, rosa #FF79C6, verde #50FA7B, gris #6272A4
- Catppuccin: fondo #1E1E2E, lila #CBA6F7, verde #A6E3A1
- Terminal: fondo #0C0C0C, verde fósforo #39FF14, gris #888

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo CODE EDITOR / TERMINAL con estas especificaciones:

TEMA: [escribe tu tema aquí — ej: "5 prompts de IA que uso a diario"]
SLIDES: [número de slides, ej: 8]
TEMA DE COLOR: [Dracula #282A36 / Catppuccin #1E1E2E / Terminal negro #0C0C0C]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografía: JetBrains Mono o Fira Code (monospace) — importar de Google Fonts
- Cada slide es una ventana de editor de código o terminal:
  * Barra de título superior con 3 luces de semáforo (rojo #FF5F56, amarillo #FFBD2E, verde #27C93F) y un nombre de archivo (ej: "estrategia.md")
  * Gutter izquierdo con números de línea en gris #6272A4
  * Cuerpo con resaltado de sintaxis: keywords rosa #FF79C6, strings verde #50FA7B, comentarios gris
  * Cursor de bloque parpadeante al final
- Cada punto del contenido se presenta como una línea de "código" o comentario comentado (// tip 3: ...)
- Slide 1: portada — archivo abriéndose con el título del tema como comentario destacado
- Slides 2-N: una "función" o bloque por punto
- Slide final: línea de salida tipo `> guardado ✓` con CTA + handle como @comment
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 19 — Y2K / CHROME RETRO-FUTURISTA

**Energía:** nostálgico, juguetón, llamativo, Gen-Z
**Ideal para:** contenido de tendencia/pop culture, audiencias jóvenes, lanzamientos, hot takes divertidos
**Motor:** HTML/CSS

### Características visuales
- Texto en cromo líquido (linear-gradient plata #E8E8E8 → #A0A0A0 → #FFF recortado al texto con background-clip + drop-shadow)
- Fondo holográfico iridiscente (conic-gradient cyan/magenta/lima)
- Fuentes bubble/tech, sprites de estrellas y destellos (✦ ✧)
- Blobs de glow difuminados
- Energía loud y nostálgica de los 2000s

### Paletas sugeridas
- Cromo plata + fondo holográfico cyan/magenta/lima
- Cromo + fondo azul eléctrico #0066FF con blobs rosa #FF6EC7
- Cromo + fondo negro con conic-gradient iridiscente

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo Y2K / CHROME RETRO-FUTURISTA con estas especificaciones:

TEMA: [escribe tu tema aquí]
SLIDES: [número de slides, ej: 7]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografía: Orbitron o Chakra Petch para titulares, Baloo 2 para texto bubble — importar de Google Fonts
- Titular en efecto CROMO LÍQUIDO: linear-gradient(180deg, #FFF, #C8C8C8, #888, #FFF) recortado al texto con background-clip:text + color:transparent + drop-shadow
- Fondo HOLOGRÁFICO: conic-gradient o linear-gradient iridiscente (cyan #00FFFF, magenta #FF00FF, lima #CCFF00) con baja saturación o blobs difuminados
- Sprites decorativos: estrellas ✦ ✧ y destellos repartidos, glow blobs (filter: blur)
- Slide 1: portada — título cromado gigante sobre fondo holográfico
- Slides 2-N: un punto por slide con titular cromado + texto bubble
- Slide final: CTA cromado + handle con sparkles
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 20 — ACID / MAXIMALISTA

**Energía:** ruidoso, rebelde, confiado, editorial-caótico
**Ideal para:** ganchos atrevidos, opiniones controversiales, nichos creativos (música/moda), motivación alta energía
**Motor:** HTML/CSS

### Características visuales
- Neón vibrante de alto contraste (lima ácida #CCFF00 sobre #1A1A1A, o magenta #FF00A8 sobre amarillo #FFEB00)
- 5-7 fuentes chocando en un mismo slide
- Tipografía rotada, superpuesta, estirada, deformada
- Layout sticker-bomb, caos organizado
- Overlay opcional de halftone o grano

### Paletas sugeridas
- Lima ácida #CCFF00 + Negro #1A1A1A + Magenta #FF00A8
- Magenta #FF00A8 + Amarillo #FFEB00 + Negro
- Cyan #00E5FF + Naranja #FF5E00 + Blanco

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo ACID / MAXIMALISTA con estas especificaciones:

TEMA: [escribe tu tema aquí]
SLIDES: [número de slides, ej: 7]
PALETA: [lima #CCFF00 + negro / magenta #FF00A8 + amarillo #FFEB00 — elige una combinación de alto contraste]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografías (mezcla 4-6 chocando): Anton + Bungee + Monoton + Archivo Black + un script como Pacifico — importar de Google Fonts
- Colores vibrantes de alto contraste que "vibran" (ej: lima ácida sobre negro)
- Tipografía rotada (±5° a ±15°), superpuesta, con distintos tamaños chocando
- Layout sticker-bomb: palabras y elementos amontonados con intención (caos organizado)
- Overlay sutil de grano o halftone opcional
- Slide 1: portada — hook gritado en máximo contraste y choque tipográfico
- Slides 2-N: un punto por slide manteniendo la energía maximalista
- Slide final: CTA atrevido + handle
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 21 — BENTO GRID

**Energía:** moderno, premium, escaneable, SaaS-grade
**Ideal para:** desgloses de features, "todo lo que incluye", resúmenes multi-punto, stacks de herramientas, dashboards de tips
**Motor:** HTML/CSS

### Características visuales
- Cada slide es una grilla de tiles desiguales con esquinas redondeadas (CSS grid con celdas que ocupan varias columnas/filas, gap 12px, border-radius 20px)
- Cada tile = una micro-idea (un stat, un ícono, una etiqueta, un mini chart)
- Fondo neutro suave (#F5F5F7) con tiles en variaciones tonales o un tile de acento
- Sensación de keynote de Apple

### Paletas sugeridas
- Fondo #F5F5F7 + tiles blancos + 1 tile acento azul #2563EB
- Fondo #0E0E12 + tiles #1A1A22 + acento cyan #22D3EE (versión dark)
- Fondo crema #F5F0E8 + tiles blancos + acento terracota

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo BENTO GRID con estas especificaciones:

TEMA: [escribe tu tema aquí — ej: "todo lo que incluye FÓRMULA 100K"]
SLIDES: [número de slides, ej: 7]
PALETA: [fondo claro #F5F5F7 + acento azul #2563EB / versión dark #0E0E12 + cyan — elige una]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografía: Inter, Manrope o Geist — importar de Google Fonts
- Cada slide es una grilla CSS de tiles DESIGUALES (display:grid, grid-template-columns repetidas, algunas celdas con grid-column/grid-row span), gap:12px, border-radius:20px en cada tile
- Cada tile contiene una micro-idea: un stat grande, un ícono/emoji, una etiqueta corta, o un mini gráfico
- Fondo neutro suave; tiles en variaciones tonales + 1 tile de acento por slide
- Jerarquía visual: el tile más importante ocupa más espacio
- Slide 1: portada — tile grande con el título + tiles pequeños de "preview"
- Slides 2-N: cada slide agrupa 3-6 micro-ideas relacionadas en bento
- Slide final: tile CTA destacado + handle
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 22 — DATA-VIZ / INFOGRAFÍA

**Energía:** autoridad, prueba, credibilidad, "el dato manda"
**Ideal para:** resultados, casos de estudio, "los datos dicen", contenido de prueba, finanzas/marketing
**Motor:** HTML/CSS

### Características visuales
- Fondo claro limpio con gráficos construidos en CSS puro
- Barras (alturas de div), donuts/anillos de progreso (conic-gradient), callouts de stats con flechas arriba/abajo, barras comparativas
- Un color de acento (#2563EB) + escala de grises
- Líneas de eje, gridlines, etiquetas de datos
- Cada slide = un insight visualizado (distinto al "Dato Gigante": aquí son varios datos graficados con UI de chart real)

### Paletas sugeridas
- Blanco + grises + acento azul #2563EB
- Blanco + grises + acento verde #16A34A (crecimiento)
- Fondo #0E1116 + acento cyan #22D3EE (dark dashboard)

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo DATA-VIZ / INFOGRAFÍA con estas especificaciones:

TEMA: [escribe tu tema aquí — idealmente datos, resultados, estadísticas]
SLIDES: [número de slides, ej: 7]
COLOR ACENTO: [azul #2563EB / verde #16A34A / cyan #22D3EE]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografía: IBM Plex Sans o Inter (números con font tabular) — importar de Google Fonts
- Cada slide visualiza UN insight con un gráfico construido en CSS puro:
  * Barras: divs con height variable + etiquetas de valor
  * Anillo/donut de progreso: conic-gradient con porcentaje al centro
  * Callout de stat: número grande + flecha ▲/▼ + delta en acento/rojo
  * Barras comparativas (antes vs después)
- Líneas de eje y gridlines sutiles en gris claro, etiquetas de datos visibles
- Un solo color de acento + escala de grises
- Slide 1: portada — el dato/insight más fuerte graficado
- Slides 2-N: cada slide = un insight visualizado distinto
- Slide final: síntesis de los datos + CTA + handle
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 23 — NEWSPAPER / PRINT

**Energía:** urgente, importante, creíble, nostálgico-autoridad
**Ideal para:** anuncios, encuadre "breaking news", storytelling, thought-leadership
**Motor:** HTML/CSS

### Características visuales
- Fondo de papel periódico envejecido (#F2EFE6)
- Masthead (cabecera) negra con título en blackletter o serif grueso + línea hairline debajo
- Cuerpo en columnas justificadas, "dateline" (fecha/lugar)
- Bloque de foto falsa con patrón de halftone (radial-gradient de puntos)
- Pull-quotes con líneas, toda la tinta negra sobre crema

### Paletas sugeridas
- Papel #F2EFE6 + Tinta negra (clásico)
- Papel #EDE8DC + tinta negra + un sello rojo #B0271E "EXTRA"
- Periódico sepia #EFE6D2 + marrón tinta #2B2118

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo NEWSPAPER / PRINT con estas especificaciones:

TEMA: [escribe tu tema aquí]
SLIDES: [número de slides, ej: 7]
NOMBRE DEL "PERIÓDICO": [ej: "EL DIARIO 100K" o el nombre de tu marca]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografías: Playfair Display o UnifrakturCook para el masthead, PT Serif o Lora para el cuerpo, Oswald para kickers — importar de Google Fonts
- Fondo papel periódico envejecido #F2EFE6, toda la tinta negra sobre crema
- Slide 1: portada estilo PRIMERA PLANA — masthead con el nombre del periódico, línea hairline debajo, titular enorme en serif grueso, "dateline" con fecha
- Slides 2-N: estructura de nota: kicker pequeño en mayúsculas + titular serif + cuerpo en columnas justificadas (column-count:2)
- Bloque de foto falsa con patrón HALFTONE (radial-gradient de puntos repetidos)
- Pull-quote destacado con líneas arriba/abajo en algún slide
- Slide final: "sección de avisos" con el CTA + handle como pie de página
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 24 — NOTES-APP / TWEET SCREENSHOT

**Energía:** auténtico, crudo, relatable, sin pulir
**Ideal para:** hot takes, texto confesional/relatable, "lo escribí a las 2am", quotes, lista de pensamientos
**Motor:** HTML/CSS

### Características visuales
- Mock pixel-perfect de Notas de iOS (crema #FFFDF4, fuente de sistema, título + cuerpo, acento amarillo carpeta) o de un post de X/Twitter (tarjeta blanca, avatar circular, @handle, nombre en bold, meta gris claro, fila de íconos like/retweet, radius 16px)
- A veces apilado como un "hilo"
- Minimalista, se ve nativo (no "diseñado")

### Paletas sugeridas
- Notas iOS: fondo #FFFDF4 + texto #1C1C1E + acento amarillo #FFD60A
- Tweet light: tarjeta blanca + texto #0F1419 + azul #1D9BF0 + gris #536471
- Tweet dark: tarjeta #15202B + texto blanco + azul #1D9BF0

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo NOTES-APP / TWEET SCREENSHOT con estas especificaciones:

TEMA: [escribe tu tema aquí]
SLIDES: [número de slides, ej: 7]
FORMATO: [Notas de iOS / post de X (Twitter) — elige el que encaje]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografía: Inter o system-ui para imitar SF Pro — importar Inter de Google Fonts
- Imita la UI NATIVA pixel-perfect:
  * Notas iOS: fondo crema #FFFDF4, barra superior con flechas/acción en amarillo #FFD60A, título en bold + cuerpo, timestamp pequeño gris
  * Post de X: tarjeta blanca radius 16px, avatar circular + nombre bold + @handle gris + texto del post (un poco más grande) + fila de íconos comentario/retweet/like/vistas en gris #536471
- Centra la tarjeta sobre un fondo suave (gris claro o color de marca tenue)
- Texto que se sienta auténtico y conversacional, no "publicitario"
- Slide 1: portada — la nota/tweet con el hook principal
- Slides 2-N: una nota o tweet por slide (o apilados como hilo)
- Slide final: nota/tweet de cierre con CTA + handle real
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

## ESTILO 25 — PASO A PASO CON PROGRESS BAR

**Energía:** accionable, guía, completista, claridad
**Ideal para:** tutoriales, frameworks, "cómo hice X en 5 pasos", onboarding, metodologías
**Motor:** HTML/CSS

### Características visuales
- Cada slide es un paso numerado con un indicador de progreso persistente
- Barra superior que se llena (width 33% → 66% → 100%) o stepper de nodos (círculos llenos + línea conectora)
- Número de paso grande en un chip de color, título corto, línea de apoyo
- Acento consistente (#6D28D9) + fondo neutro
- Etiqueta opcional "Paso 2 de 5"
- Crea un loop de finalización (efecto Zeigarnik) que empuja a deslizar hasta el final

### Paletas sugeridas
- Fondo #FAFAFA + acento violeta #6D28D9
- Fondo blanco + acento naranja #FF6B35 (marca F100K)
- Fondo #0F1020 + acento cyan #22D3EE (dark)

### PROMPT PARA COPIAR Y PEGAR

```
Genérame un carrusel HTML/CSS estilo PASO A PASO CON PROGRESS BAR con estas especificaciones:

TEMA: [escribe tu tema aquí — ej: "cómo crear tu primer reel viral en 5 pasos"]
CANTIDAD DE PASOS: [ej: 5 pasos = 7 slides con portada y cierre]
COLOR ACENTO: [violeta #6D28D9 / naranja #FF6B35 / cyan #22D3EE]

ESPECIFICACIONES TÉCNICAS:
- Formato: 1080x1350px (portrait 4:5)
- Tipografía: Sora u Outfit para titulares + Inter para cuerpo — importar de Google Fonts
- Indicador de progreso PERSISTENTE en todos los slides de paso:
  * Opción A: barra superior fina que se llena progresivamente (width 20% → 40% → 60% ...)
  * Opción B: stepper de nodos (círculos; los pasos completados llenos del color acento, el actual con borde, los siguientes vacíos) unidos por una línea
- Etiqueta "Paso N de [total]" + número de paso grande en un chip del color acento
- Título del paso corto y accionable + 1-2 líneas de apoyo
- Fondo neutro, acento consistente
- Slide 1: portada — promesa del resultado + "en N pasos" (barra al 0%)
- Slides 2-N: un paso por slide con la barra/stepper avanzando
- Slide final: barra al 100% + "lo lograste" + CTA + handle
- El HTML muestra los slides en secuencia vertical para captura de pantalla
```

---

---

# MODIFICADORES — Combina con cualquier estilo

Además del estilo base, puedes pedir cualquiera de estos modificadores extra:

## MODIFICADOR: SEAMLESS / PANORÁMICO
Agrega esto al prompt de cualquier estilo:
```
MODIFICADOR SEAMLESS: Diseña el carrusel como un canvas continuo donde los elementos 
fluyen de un slide al siguiente. Que al deslizar se vea como una imagen panorámica continua. 
Usa elementos (línea, forma, gradiente, patrón) que crucen el borde entre slides.
```

## MODIFICADOR: NUMERACIÓN PROMINENTE
```
MODIFICADOR NUMERACIÓN: Cada slide tiene el número del punto muy grande y prominente 
(en bold, color de acento, mínimo 120px) como primer elemento visual, antes del contenido.
```

## MODIFICADOR: SOLO TEXTO EN CADA SLIDE (1 frase)
```
MODIFICADOR FRASE ÚNICA: Cada slide de contenido tiene UNA SOLA frase o idea completa, 
tipografía grande (mínimo 48px), sin subtítulos ni puntos extra. Impacto puro.
```

## MODIFICADOR: CON HANDLE Y BRANDING
```
MODIFICADOR BRANDING: En todos los slides, incluye en la esquina inferior derecha 
el handle "@[tu handle]" en tipografía pequeña (14-16px), color sutil, semi-transparente. 
El slide final es 100% de branding: logo/nombre grande + handle + CTA.
```

## MODIFICADOR: VARIACIÓN DE FONDO POR SLIDE
```
MODIFICADOR VARIACIÓN: Cada slide tiene un fondo de color diferente, 
todos dentro de la misma paleta definida. No todos del mismo color.
```

---

# INSTRUCCIONES PARA GENERAR EN CLAUDE (paso a paso)

```
1. Elige el ESTILO de esta guía (01 al 25)
2. Copia el PROMPT del estilo elegido
3. Completa los campos entre corchetes [ ] con tu información
4. Agrega los MODIFICADORES que quieras al final
5. Pégalo en Claude y envíalo
6. Claude va a generar el archivo HTML completo
7. Copia el código HTML → guárdalo como "carrusel-[tema].html" 
8. Ábrelo en Chrome o Safari
9. Usa capturas de pantalla para cada slide (herramienta de captura del sistema)
   → Mac: Cmd+Shift+4 → seleccioná cada slide
   → O usa la extensión "GoFullPage" en Chrome para capturar todo de una vez
10. Sube las imágenes a Instagram como carrusel
```

---

# PROMPT UNIVERSAL (cuando no sabes qué pedir)

Si quieres que Claude elija el estilo según el contenido, usa este prompt:

```
Voy a darte información sobre el carrusel que necesito. Elige el estilo más adecuado 
de tu catálogo de estilos y genérame el HTML completo:

TEMA: [tu tema]
OBJETIVO: [qué quieres lograr: educar / vender / conectar / viralizarse / autoridad]
AUDIENCIA: [a quién va dirigido]
CANTIDAD DE PUNTOS: [cuántos tips, pasos, razones, etc. tienes]
PALETA DE MARCA: [tus colores, o deja que Claude elija]
HANDLE: [@tuhandle]
MOTOR: HTML/CSS

Dime qué estilo elegiste y por qué antes de generarlo.
```

---

*Guía generada con Claude Code · FÓRMULA 100K · Abril 2026*
*Actualizar cuando se incorporen nuevos estilos o herramientas*
