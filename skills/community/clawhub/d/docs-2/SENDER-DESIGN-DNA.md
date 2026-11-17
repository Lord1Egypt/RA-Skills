# SENDER — DESIGN DNA

El sistema que gobierna cada decisión visual del sitio inmersivo de Sender.
Ninguna escena, componente o animación puede contradecir este documento.

**Versión** 1.0 · 2026-09-30 · Sustituye a cualquier valor por defecto de cualquier skill.
**Fuente de verdad** `content/` (textos bilingües auditados) y las 10 fotografías reales.

---

## 0. Principio rector

> Sender no vende señal. Sender **hace que la señal llegue**.
> El sitio no debe *parecer* tecnología. Debe comportarse como el oficio: preciso,
> silencioso, medido, y visible sólo cuando hace falta.

Tres consecuencias que ordenan todo lo demás:

1. **La señal no se ve; se experimenta.** (Texto de Sender, escena 01.) Por eso el
   movimiento, la luz y el color codifican *magnitudes físicas* —frecuencia, potencia,
   propagación—, no gusto.
2. **Veinte años no se decoran.** Nada de efectos que existan para impresionar. Cada
   animación tiene una razón técnica que se puede nombrar en una frase.
3. **Lo que no está documentado, no está.** Vale para el contenido y vale para la
   interfaz: no se inventan cifras, y tampoco se inventan adornos sin función.

---

## 1. COLOR

### 1.1 Paleta autorizada — cuatro colores, sin excepción

| Token | Hex | Rol |
|---|---|---|
| `paper` | `#FFFFFF` | Texto principal, altas luces, superficies claras |
| `azul` | `#1E73BE` | **Color de marca.** Acción, estructura, foco |
| `grafito` | `#494949` | Texto secundario, estructura neutra, superficies medias |
| `cian` | `#0085B2` | **Señal.** Datos, mediciones, estado vivo. Nunca decorativo |

Prohibidos explícitamente: morado, violeta, rosa, naranja, amarillo, dorado, verde.
Verificado por el auditor automático (`scripts/audit_palette.py`).

### 1.2 Escalas derivadas — y por qué son legítimas

Con cuatro valores puros no hay jerarquía de superficies, estados de foco ni
profundidad de campo. El sistema define **escalas de luminancia dentro de cada
familia**, que no introducen ningún matiz nuevo: son el mismo color a otro valor.

**Familia NEUTRA** — derivada de `grafito` `#494949` (H0 · S0%):

| Token | Hex | Uso |
|---|---|---|
| `noche` | `#0A0A0A` | Fondo base del sitio |
| `pozo` | `#131313` | Superficie 1 |
| `pizarra` | `#1E1E1E` | Tarjetas, paneles |
| `acero` | `#2E2E2E` | Bordes, divisores |
| `grafito` | `#494949` | **Sistema** |
| `ceniza` | `#6E6E6E` | Texto terciario |
| `plata` | `#A8A8A8` | Texto secundario sobre oscuro |
| `niebla` | `#D6D6D6` | Texto casi principal sobre oscuro |
| `papel` | `#FFFFFF` | **Sistema** |

**Familia AZUL** — derivada de `azul` `#1E73BE` (H209 · S73%):

| Token | Hex | Uso |
|---|---|---|
| `azul-noche` | `#061424` | Fondo de escena nocturna, cielo de ENTRY |
| `azul-profundo` | `#0B2540` | Superficies de instrumentación |
| `azul-hondo` | `#133A5E` | Rellenos en reposo |
| `azul` | `#1E73BE` | **Sistema** |
| `azul-claro` | `#4D97D6` | Foco, hover |
| `azul-alto` | `#8CBCE6` | Trazos de dato |
| `azul-tenue` | `#C7DFF5` | Texto sobre `azul-noche` |

**Familia CIAN** — derivada de `cian` `#0085B2` (H195 · S100%):

| Token | Hex | Uso |
|---|---|---|
| `cian-hondo` | `#00465E` | Rellenos |
| `cian-medio` | `#00719A` | Trazos |
| `cian` | `#0085B2` | **Sistema** |
| `cian-claro` | `#33A3CC` | Indicadores activos |
| `cian-alto` | `#66C0DC` | Trazos finos de dato |
| `cian-tenue` | `#99D8EC` | Realces puntuales |

### 1.3 Contrastes medidos

Medidos con la fórmula de luminancia relativa WCAG 2.1 sobre los fondos reales
del sitio, no estimados. Script: `scripts/contraste.py`.

| Combinación | Ratio | Veredicto | Uso |
|---|---|---|---|
| `paper` sobre `noche` | 19,80 : 1 | AAA | Texto principal |
| `niebla` sobre `noche` | 13,62 : 1 | AAA | Texto casi principal |
| `azul-tenue` sobre `azul-noche` | 13,50 : 1 | AAA | Enlace sobre escena |
| `plata` sobre `noche` | 8,33 : 1 | AAA | Texto secundario |
| `azul-alto` sobre `noche` | 9,85 : 1 | AAA | Titular acentuado |
| `grafito` sobre `paper` | 9,00 : 1 | AAA | Texto sobre superficie clara |
| `ceniza` sobre `noche` | 5,15 : 1 | AA | Texto terciario |
| `cian-claro` sobre `noche` | 6,84 : 1 | AA | Dato activo |
| `cian-claro` sobre `azul-noche` | 6,40 : 1 | AA | Dato sobre escena |
| `azul-claro` sobre `noche` | 6,33 : 1 | AA | Acento, foco |
| `paper` sobre `azul` | 4,94 : 1 | AA | Texto sobre acción |
| `azul` sobre `paper` | 4,94 : 1 | AA | Acento sobre claro |
| `niebla` sobre `pozo` | 12,78 : 1 | AAA | Prosa sobre panel |

**Nota de corrección.** La primera versión de esta tabla afirmaba 4,9 : 1 para
`ceniza` sobre `noche`. Al medirlo de verdad daba **3,88 : 1**, por debajo del
suelo AA que este mismo documento fija. El token se corrigió de `#6E6E6E` a
`#828282`. Queda registrado en vez de oculto: una tabla de contraste que no se
mide no vale nada.

### 1.4 Reglas de uso

- **Un acento por vista.** `azul` conduce; `cian` aparece sólo si hay un dato.
- `cian` **nunca** decora: si no mide algo, no es cian.
- El fondo nunca es `#000000` puro ni un degradado de dos colores cualesquiera.
  La profundidad se construye con las escalas y con la fotografía.
- Texto sobre fotografía: siempre con un velo derivado de `azul-noche` al 55–72 %
  **y** verificado el contraste resultante, nunca confiando en la foto.

---

## 2. TYPOGRAPHY

### 2.1 Familias — auto-hospedadas, licencia OFL

**IBM Plex Sans** para todo el discurso · **IBM Plex Mono** para todo lo que es dato.

Se auto-hospedan `woff2` con subset `latin` (22 KB/peso). Sin CDN, sin peticiones a
terceros, sin parpadeo. Pesos cargados: Sans 300/400/500/600/700, Mono 400/500/600.

La elección es deliberada: Plex nace como tipografía de **documento técnico e
instrumentación**. No es Inter, no es Roboto, no es Poppins. Es el registro exacto
del oficio de Sender.

### 2.2 Regla de convivencia

> **La mono es para datos. La sans es para el discurso. Nunca se intercambian.**

Frecuencias, potencias, modelos, bandas, códigos y unidades van en mono **en los dos
idiomas**: son nomenclatura técnica internacional, no prosa traducible.

### 2.3 Escala

| Token | Tamaño | Peso | Tracking | Interlínea | Uso |
|---|---|---|---|---|---|
| `display-xl` | `clamp(3.25rem, 10.5vw, 8.5rem)` | 300 | −0.040em | 0.90 | Wordmark, escenas 01/04 |
| `display-l` | `clamp(2.25rem, 6vw, 4.75rem)` | 300 | −0.030em | 0.96 | Títulos de escena |
| `display-m` | `clamp(1.625rem, 3.2vw, 2.75rem)` | 400 | −0.020em | 1.06 | Títulos de sección |
| `titulo` | `clamp(1.125rem, 1.6vw, 1.5rem)` | 500 | −0.010em | 1.25 | Encabezados de bloque |
| `cuerpo-l` | `clamp(1.0625rem, 1.15vw, 1.25rem)` | 400 | 0 | 1.60 | Entradillas |
| `cuerpo` | `1rem` | 400 | 0 | 1.65 | Prosa |
| `cuerpo-s` | `0.875rem` | 400 | 0 | 1.60 | Notas, pies |
| `etiqueta` | `0.6875rem` | 500 | 0.14em | 1.20 | Mayúsculas. Kickers, roles |
| `dato` | `0.8125rem` | 400 | 0.02em | 1.45 | Mono, `tabular-nums` |

### 2.4 Reglas

- Titulares en peso **300**, nunca bold. La autoridad viene del tamaño y del aire,
  no del grosor. (El bold se reserva a `titulo` y a énfasis dentro de prosa.)
- Interlineado negativo sólo por encima de `display-m`. En prosa nunca baja de 1,6.
- **Cifras siempre `tabular-nums`.** Una columna de especificaciones tiene que
  alinearse.
- Ancho de medida: 58–72 caracteres. Nunca una línea de prosa a todo el ancho.
- Nada de itálicas decorativas ni de versalitas falsas.

---

## 3. GRID

Retícula de **12 columnas**. Margen lateral fluido `clamp(1.25rem, 5vw, 5rem)`.
Gutter `clamp(0.75rem, 1.5vw, 1.5rem)`. Ancho máximo de contenido `1680px`.

### 3.1 La retícula de instrumentación

Sobre la retícula base hay una **capa de guías técnicas** —líneas a 1 px en
`acero` al 8–14 %— que se revela sólo durante las transiciones de escena y en los
bloques de datos. Es la firma visual del sitio: evoca el plano de ingeniería sin
dibujar un plano.

**Disciplina:** nunca visible de forma permanente; nunca más de una guía por borde;
nunca sobre texto.

### 3.2 Rotura de retícula

Se permite salir de la retícula en exactamente tres casos, y sólo con intención:

1. La fotografía a sangre completa (`full-bleed`), que ignora columnas.
2. Los números de escena (`00`–`08`), que se anclan al margen exterior.
3. Los diagramas de propagación y espectro, que son continuos por naturaleza.

---

## 4. SPACING

Base **8 px**, con 4 px como medio paso. Escala completa:

`4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128 · 160 · 200 · 256`

| Token | Valor | Uso |
|---|---|---|
| `space-2xs` | 4px | Separación dentro de una línea de datos |
| `space-xs` | 8px | Etiqueta ↔ valor |
| `space-s` | 16px | Párrafo ↔ párrafo |
| `space-m` | 32px | Bloque ↔ bloque |
| `space-l` | 64px | Subsección |
| `space-xl` | 128px | Sección |
| `space-2xl` | 200px | Transición de escena |

**Ritmo vertical:** cada escena ocupa `100svh` como mínimo. Las escenas que exigen
recorrido usan `250svh`–`400svh` con contenido anclado. Ninguna escena termina
exactamente al final del viewport: siempre hay 200 px de respiro antes de la
siguiente, para que el corte se sienta decidido y no apretado.

---

## 5. LAYOUTS

Seis plantillas. Toda escena usa una y sólo una como estructura dominante.

| # | Plantilla | Descripción | Escenas |
|---|---|---|---|
| L1 | **Full-bleed** | Medio a sangre, texto anclado a una esquina inferior | 00, 04 |
| L2 | **Split asimétrico** | 7/5 o 5/7. Nunca 6/6 | 02, 05 |
| L3 | **Rail lateral** | Columna estrecha de etiquetas fijas + contenido variable | 01, 07 |
| L4 | **Secuencia horizontal** | Recorrido lateral guiado por scroll vertical | 04, 06 |
| L5 | **Retícula de datos** | Filas de especificación con la mono alineada | 03, 07 |
| L6 | **Cierre centrado** | Medida corta, mucho aire, acción única | 08 |

**Prohibido: el 6/6.** La simetría perfecta es la firma del diseño genérico. Si dos
columnas miden lo mismo, una de las dos sobra.

---

## 6. IMAGE TREATMENT

### 6.1 La regla inquebrantable

Las **10 fotografías reales** y el **video real del hero** son el único material.
No hay stock, no hay imágenes generadas, no hay placeholders. Si falta una imagen,
se resuelve con tipografía, retícula o WebGL — **nunca inventando una foto**.

### 6.2 Rol de cada imagen

| Rol | Definición | Piezas |
|---|---|---|
| `ENTRY` | Apertura. Máxima presencia, movimiento | `hero.jpg`, `hero-wide.jpg`, `sender-hero.mp4` |
| `SENDER` | La empresa. Persona y operación | `about.jpg`, `cap-broadcast.jpg` |
| `ENGINEERING` | El oficio. Componente y sistema radiante | `cap-transmission.jpg`, `cap-rf.jpg` |
| `TRANSMISSION` | La cadena completa | `cap-critical.jpg` |
| `PROJECTS` | Obra documentada | `cap-antennas.jpg`, `proj-stl.jpg` |
| `PRODUCTS` | Equipo concreto | `proj-am.jpg` |

Ninguna foto se repite dentro de la misma escena, y ninguna se usa en un rol que
contradiga su contenido real.

### 6.3 Grade cromático — decisión explícita

**El problema:** el material fotográfico es coherente en tono (crepúsculo, niebla,
luz fría) **excepto el video del hero**, cuyo atardecer andino es naranja saturado.
La paleta no admite naranja.

**La decisión:** los archivos originales **se conservan intactos** en el repositorio.
El grade se aplica **en la presentación**, con `filter`, capas de mezcla y shaders.
Es reversible, ajustable y verificable, y **no altera la identidad fáctica**: el
sujeto, el lugar y el equipo siguen siendo exactamente los mismos. Es color, no
contenido.

Grade por defecto:

- **Duotono direccional.** Sombras hacia `azul-noche`, luces hacia `paper`.
  El cian no entra en el grade: se reserva al dato.
- **Desaturación global al 12–20 %.** Suficiente para que el naranja del cielo
  caiga dentro del sistema sin que el atardecer desaparezca.
- **Viñeta inferior** derivada de `noche` al 40 % cuando hay texto encima.
- **Grano fílmico** a `opacity: 0.028` para unificar las cuatro resoluciones
  distintas del archivo (1200×1600 a 1792×1008) y disolver el banding.
- **Contraste local +6 %** sólo en las escenas de producto, para que la
  instrumentación se lea.

### 6.4 Cámara y profundidad

Toda fotografía se mueve **más lento que el scroll** (parallax de 0,86× a 0,94×).
El recorte nunca corta el sujeto principal: la torre, la antena, el mástil y el
equipo siempre conservan su base y su extremo. El `object-position` se fija **por
foto**, no por defecto.

### 6.5 Pipeline imagen → video

Para las tres piezas con más peso narrativo, el still se convierte en un plano con
cámara:

1. **Profundidad.** La imagen se separa en 2–3 planos por luminancia y foco.
2. **Cámara.** Un desplazamiento lento (≤ 4 % del encuadre) y un `scale` de
   1,00 → 1,06 a lo largo de la escena. Nunca un zoom perceptible como zoom.
3. **Salida.** `WebM`/`VP9` con póster `AVIF` → `WebP` → `JPG` en cascada.
4. **Degradación.** Si no hay WebGL, queda el still con parallax en CSS. Si no hay
   video, queda el póster. Nunca una caja vacía.

---

## 7. MOTION

### 7.1 La ley

> **El scroll es la línea de tiempo. Todo lo demás está subordinado a él.**

Nada se mueve por parecer vivo. Cada animación declara qué magnitud representa:
llegada, propagación, amplificación, medición o corte de banda.

### 7.2 Curvas y duraciones

| Tipo | Duración | Curva | Ejemplo |
|---|---|---|---|
| Micro | 180–260 ms | `cubic-bezier(0.2, 0, 0.2, 1)` | Foco, hover, estado |
| Transición | 600–900 ms | `cubic-bezier(0.16, 1, 0.3, 1)` | Entrada de bloque |
| Escena | 1200–2000 ms | `cubic-bezier(0.16, 1, 0.3, 1)` | Cambio de escena |
| Salida | 400–600 ms | `cubic-bezier(0.7, 0, 0.84, 0)` | Bloque que se va |

Easing de firma: **expo-out**. Entra rápido y frena largo. Es el movimiento de algo
que llega y se asienta — que es literalmente lo que hace una señal.

### 7.3 Smooth scroll

Lenis con `lerp: 0.085`, `wheelMultiplier: 0.9`, `touchMultiplier: 1.6`. El scroll
nativo se detiene: la posición la gobierna el riel de la línea de tiempo.

### 7.4 Accesibilidad del movimiento

Con `prefers-reduced-motion: reduce`:

- Lenis se destruye; vuelve el scroll nativo.
- Todo `scrub` de video pasa a póster fijo.
- El parallax se anula (`translate 0`, `scale 1`).
- Los fundidos se mantienen a 200 ms — la opacidad no provoca mareo.
- La escena 3D entrega un fotograma fijo, no un bucle.

Además: `requestAnimationFrame` pausado cuando la pestaña no es visible, y todo
timeline de GSAP matado en el desmontaje de la escena.

---

## 8. 3D

### 8.1 Qué se modela y por qué

El 3D de este sitio **no es escenografía: es instrumentación.** Sujeto único:

> **El campo de señal** — cómo una onda nace, se le asigna una frecuencia, se amplifica,
> se irradia y llega.

Todo lo demás está prohibido. Concretamente, **no hay**:

- esfera, orbe, globo ni icosaedro girando;
- partículas en movimiento aleatorio sin campo que las gobierne;
- túneles infinitos, rejillas de neón ni cuadrículas retro;
- cualquier forma que pueda pertenecer a otro sitio cambiando el logo.

### 8.2 Las cuatro representaciones autorizadas

| Pieza | Qué es | Dónde | Técnica |
|---|---|---|---|
| `SignalField` | Frente de onda vertical irradiado desde un mástil | 01 SIGNAL | Shader GLSL de desplazamiento radial |
| `RadiationPattern` | Diagrama polar real de un arreglo de antenas | 03 ENGINEERING | Lóbulos calculados, línea de `azul-alto` |
| `Chain` | Recorrido estudio → antena → audiencia | 04 TRANSMISSION | Geometría ligera + cámara sobre riel |
| `Spectrum` | Espectro de la banda asignada | 07 PROCESS | Barras reactivas a datos documentados |

### 8.3 Presupuesto y disciplina

| Restricción | Límite |
|---|---|
| Triángulos en escena | ≤ 60 000 |
| Draw calls | ≤ 24 |
| Texturas | ≤ 8 MB, potencia de dos |
| Postprocesado | Máximo un paso (viñeta o grano). Sin bloom |
| `dpr` | `[1, 1.75]`; en móvil `1` |
| `useFrame` | Nada de `setState` por fotograma |
| Ciclo de vida | `dispose()` de geometría, material y render target en desmontaje |

Sin WebGL, cada pieza tiene su sustituto 2D: el `SignalField` pasa a una onda en
`<canvas>`, el `RadiationPattern` a un SVG polar, la `Chain` a un recorrido de
scroll tipográfico.

---

## 9. TRANSITIONS

El paso de una escena a otra es un **cambio de banda**: se corta la portadora
anterior y entra la nueva. Nunca un fundido a negro genérico.

| Transición | Mecánica | Uso |
|---|---|---|
| `tune` | Barrido de una línea de `cian` de 1 px que cruza la pantalla y arrastra el contenido | 00 → 01 |
| `propagate` | El contenido anterior se expande desde el centro y cede el paso | 01 → 02, 05 → 06 |
| `cut` | Corte seco, sin transición | 03 → 04, 06 → 07 |
| `settle` | El bloque baja 24 px y se asienta | 07 → 08 |

Duración 700–900 ms. Nunca más de una transición en curso. La transición **no
bloquea el scroll**: si el usuario sigue bajando, la siguiente escena ya está.

---

## 10. COPY

### 10.1 Voz

Técnica, llana, verificable. Frases cortas. Cero adjetivos de folleto. Se habla de
lo que se hace y de lo que existe. Cuando no hay dato, **se dice que no lo hay** —
y eso se convierte en un rasgo de honestidad visible en la interfaz.

> El proyecto ya se impuso esta regla: *no se inventan clientes, no se asignan años,
> no se agregan cifras de proyectos completados.*

### 10.2 Idiomas

Español e inglés **completos y equivalentes**. Interfaz, prosa, navegación, `alt`,
metadatos, JSON-LD y datos estructurados. **Cero mezcla.**

Excepción única y explícita: la **nomenclatura técnica internacional** (AM, FM, HF,
VHF, UHF, NAVTEX, RF, STL, nombres de modelo, unidades) es idéntica en los dos
idiomas, porque es un código, no una traducción.

### 10.3 Vocabulario prohibido

`innovative solutions` · `cutting-edge` · `revolutionary` · `next-generation` ·
`world-class` — y sus equivalentes en español: *soluciones innovadoras*, *de última
generación*, *revolucionario*, *de clase mundial*, *vanguardia*.

Verificado por el auditor automático.

### 10.4 Cifras

Sólo aparecen las documentadas: `+20 años`, `490 – 1700 kHz`, `87.5 – 108 MHz`,
`2 – 30 MHz`, `134 – 174 MHz`, `490 / 518 kHz`, `1 kW`, `60 m`.
Ninguna otra. Si una interfaz pide un número que no existe, se enseña la ausencia,
no un número.

---

## 11. SEO

- **Rutas por idioma reales:** `/es/` y `/en/`. HTML distinto, no un conmutador en
  el cliente. Cada idioma tiene su `<html lang>`, su `<title>` y su descripción.
- **`hreflang` recíproco** ES ↔ EN ↔ `x-default` apuntando a `/es/`.
- **JSON-LD independiente por idioma:** `Organization` con dirección, teléfono y
  área de servicio reales; `Product` por cada uno de los 16 productos; `BreadcrumbList`
  en las fichas; `ItemList` en el catálogo.
- **Open Graph y Twitter Card** con imagen propia por idioma.
- `sitemap.xml` con anotaciones `hreflang`, `robots.txt` y `canonical` absoluto.
- El contenido esencial **está en el HTML**, no sólo renderizado por JavaScript.

---

## 12. COMPONENTS

| Componente | Función | Reglas |
|---|---|---|
| `SceneShell` | Envoltura de escena | Índice anclado al margen, `100svh`, respiro final |
| `SceneIndex` | Número `00`–`08` en mono | Nunca más de 24 px |
| `Kicker` | Etiqueta superior | `etiqueta`, `azul-claro` |
| `DisplayTitle` | Titular de escena | Peso 300, tracking negativo |
| `LeadParagraph` | Entradilla | Máx. 68 caracteres de medida |
| `DataRow` | Fila etiqueta ↔ valor | Mono, `tabular-nums`, borde inferior `acero` |
| `SpecGrid` | Retícula L5 de especificaciones | Se lee como ficha técnica real |
| `ProductCard` | Tarjeta de producto | Nombre, categoría, potencia. Sin precio: no se publica |
| `ProjectCard` | Ficha de instalación | Con `sourceUrl` cuando existe |
| `BandIndicator` | Banda activa | Sólo `cian`; mide, no decora |
| `Figure` | Imagen con rol y alt bilingüe | `loading`, `sizes` y grade obligatorios |
| `VideoScrub` | Video gobernado por scroll | Póster primero; `reduced-motion` → fotograma fijo |
| `SignalCanvas` | Host del canvas 3D | Montaje diferido y `dispose` garantizado |
| `LangSwitch` | Conmutador ES/EN | Cambia ruta completa; nunca texto suelto |
| `CTA` | Acción | Uno por escena como máximo |
| `SkipLink` | Salto a contenido | Primero en el DOM, visible al foco |
| `GuidesOverlay` | Retícula de instrumentación | Decorativa, `aria-hidden` |

---

## 13. ANTI-SLOP

Reglas de rechazo. Si algo de esta lista aparece, se elimina aunque quede bonito.

### 13.1 Los nueve rechazos del brief

1. **Hero genérico.** Aquí el hero es el video real de una torre real en la
   cordillera, con un transport gobernado por el scroll. No una frase centrada
   sobre un degradado.
2. **Degradado genérico.** Prohibido el degradado de relleno de fondo. La
   profundidad se hace con escalas tonales y fotografía.
3. **Esfera u orbe 3D.** No existe ninguna. El 3D modela propagación, no sólidos.
4. **Dashboard genérico.** Los paneles muestran canales y rangos documentados, y
   **declaran** que la interfaz es demostrativa, no telemetría viva.
5. **Partículas aleatorias.** Toda partícula pertenece a un campo que la gobierna.
6. **Paneles de cristal.** Prohibido `backdrop-filter` decorativo. Si hay
   translucidez, la causa es una capa de medio real, y se declara.
7. **Sombras excesivas.** Una sola sombra por elemento, apenas perceptible, y
   ninguna que simule elevación sobre un fondo ya plano.
8. **Iconos de relleno.** Cada icono se dibuja a medida y significa algo. Nada de
   librerías genéricas de 24 px con estilo de banco.
9. **Animaciones porque sí.** Ver §7.1. Si no se puede nombrar la magnitud que
   representa, no entra.

### 13.2 Marcas adicionales de diseño automático — prohibidas

- Simetría 6/6 y centrado universal.
- Texto justificado, o líneas de prosa a todo lo ancho.
- `border-radius` por encima de 2 px. **Este sistema es de ángulos rectos.** Un
  instrumento de rack no tiene esquinas redondeadas.
- Emojis en la interfaz. Ninguno. Jamás.
- Sombra de texto para hacer legible texto sobre foto: se usa velo y se mide.
- El mismo `.section` repetido nueve veces con distinto contenido.
- Botones con degradado, brillo o «glass».
- Contadores animados de cifras que no existen.
- Scroll-jacking que secuestra el control. Lenis suaviza; el usuario manda.
- Cualquier elemento que pudiera pertenecer a otra web sin cambiar una sola palabra.

### 13.3 La prueba final

Antes de dar una escena por buena, tres preguntas:

1. ¿Puedo nombrar la magnitud física o el hecho documentado que representa cada
   animación que he puesto?
2. Si le quito el logo, ¿sigue siendo inconfundiblemente Sender?
3. ¿Esto podría estar en la web de una empresa de radiodifusión de verdad, o
   parece la web de una startup que vende software?

Si la tercera respuesta es la segunda opción, la escena vuelve a empezar.
