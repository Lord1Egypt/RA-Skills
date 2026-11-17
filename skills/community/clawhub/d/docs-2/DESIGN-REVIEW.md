# SENDER — DESIGN REVIEW

Crítica del estado construido, escena por escena. Escrito **después** de ver el
sitio renderizado en escritorio (1440×900) y en el perfil real de un Galaxy S24
(360×780, DPR 3), no de suponerlo.

**Método:** Design DNA → Prototipo → Design Loop → Crítica → Refinamiento.
Este documento es la fase de Crítica. Cada apartado dice qué se construyó, qué
funciona, **qué no**, qué debe cambiar y si viola el DNA.

**Fecha:** 2026-09-30 · **Estado:** 9 escenas construidas y verificadas.

---

## 0. Resumen ejecutivo

| Aspecto | Estado |
|---|---|
| Escenas construidas | 9 de 9 |
| Cumplimiento del auditor | **0 hallazgos** en 9 categorías |
| Contraste WCAG | 25/25 parejas ≥ AA |
| Desborde horizontal | ninguno, a 360 px |
| Errores de consola | 0 en escritorio y móvil, ES y EN |
| Bilingüismo | 680 pares `es`/`en` verificados |
| Peso del paquete inicial | 120 KB (gzip ≈ 38 KB) + three.js diferido |
| **Pendiente crítico** | **la aprobación visual del Hero por la persona** |

**Lo mejor de lo construido:** el campo de señal de la escena 01 y el diagrama
polar de la 03. Ninguno de los dos es decoración: uno es una propagación real
con decaimiento físico, el otro son lóbulos calculados con el factor de arreglo.
Son las dos piezas que **no podrían estar en la web de otra empresa**.

**Lo más débil:** la escena 05 PROYECTOS en móvil, y la densidad del raíl
horizontal de la 04. Detalle en §5 y §4.

---

## 1. Defectos encontrados y corregidos durante el Design Loop

Se registran porque son parte del proceso, no a pesar de él.

### 1.1 El campo 3D no se dibujaba nada — **CRÍTICO, corregido**

`SignalField.tsx` usaba `ALTO_MAX` dentro de la cadena GLSL. Es una constante de
JavaScript: **en GLSL no existe**. El shader no compilaba, el canvas se creaba
vacío y la escena 01 se veía como un fondo azul plano. Se inyecta el valor con
plantilla. Verificado después: el campo se ve.

### 1.2 El canvas nunca se montaba — **CRÍTICO, corregido**

`SignalCanvas` registraba el `IntersectionObserver` en un efecto con
dependencias `[]`. Pero el contenedor `div` **no existe en el primer render**
—hasta que el efecto de detección de WebGL resuelve—, así que el observer salía
por el `return` temprano y jamás volvía a engancharse. El canvas no se montaba
nunca en ningún navegador. La dependencia pasa a `[hayWebGL, roto]`.

### 1.3 Contenido invisible de forma sistemática — **CRÍTICO, corregido**

Ningún componente `Reveal` llegaba a revelarse. Dos causas acumuladas:

1. `threshold: 0.15` es **inalcanzable** cuando el elemento es más alto que el
   viewport, y casi todas las figuras de este sitio lo son.
2. Los elementos **saltados** por un desplazamiento rápido o por el índice de
   escenas quedaban fuera del área de observación y nunca se revelaban: la
   columna izquierda entera de PRODUCTOS se veía vacía.

Corregido: `threshold: 0`, resolución inicial **por geometría** (si el elemento
ya está en pantalla o ya pasó, se revela de inmediato) y `rootMargin` superior
enorme para que lo ya superado cuente como visible. Un elemento que ya pasó
**debe verse**: ocultarlo no protege a nadie.

### 1.4 Contraste por debajo del propio suelo — **corregido**

La tabla de contraste del DNA afirmaba 4,9 : 1 para `ceniza` sobre `noche`. Al
medirlo daba **3,88 : 1**. El token se cambió de `#6E6E6E` a `#828282` (5,15 : 1
sobre `noche`, 4,82 : 1 sobre `azul-noche`). Las cifras del DNA se sustituyeron
por valores medidos con script, no estimados.

### 1.5 `pizarra` con texto demasiado tenue — **documentado**

`ceniza` sobre `pizarra` da 4,34 : 1: no pasa AA. Ninguna escena usa esa pareja,
pero era una trampa latente para el futuro. Se documenta la restricción en
`tokens.css` y se verifica la pareja real en `contraste.py`.

### 1.6 El indicador de scroll colisionaba con los metadatos

En escritorio, «Desliza para explorar» (vertical) se solapaba con el bloque
BASE / OFICIO / BANDAS. Movido al margen izquierdo.

### 1.7 La torre no se veía en móvil

El recorte centrado del video dejaba fuera el sujeto de la fotografía. Se
desplaza el punto de interés a `62% 44%` y se levanta la exposición en vertical.

---

## 2. Escena 00 — ENTRY

**Construido.** Video real (`sender-hero.mp4`, 4,8 MB) a sangre, con el
transporte gobernado por el scroll: el visitante no ve una animación, mueve la
cámara. Wordmark en `display-xl` peso 300, claim y sub en el pie, tres
metadatos en mono, dos acciones. Recorrido de 320 svh.

**Funciona.** El grade por `mix-blend-mode: color` resuelve el problema central
del proyecto: el atardecer naranja saturado del video cae dentro de la familia
azul **conservando su luminancia**, así que el atardecer sigue ahí pero deja de
romper la paleta. El mástil de la torre queda legible con su balizamiento. La
secuencia tipográfica y el `object-position` por breakpoint llevan la torre al
encuadre en vertical.

**No funciona / debe cambiar.**
- **La aprobación visual es la persona.** Esta escena existe para ser aprobada o
  rechazada. Es el punto de control obligatorio del brief.
- El video pesa 4,8 MB en un solo archivo MP4. Sin WebM ni versiones por
  resolución. Debe pasar por el hito 09.
- Con el scroll al 100 % de la escena el video llega a su último fotograma y
  queda congelado unos 400 ms antes de que entre la 01. Se nota.
- El wordmark repite «SENDER» en el nav y en el hero. En la primera pantalla es
  deliberado; conviene revisar si cansa.

**Violaciones del DNA:** ninguna detectada.

**Móvil (360×780).** 2 496 px de recorrido. El apilado funciona; los dos CTA en
columna ocupan bastante. La torre se ve. Sin desborde.

**Rendimiento.** El video es el mayor coste del sitio. `preload="auto"` en un
móvil es discutible: debería ser `metadata` si no hay conexión rápida.

---

## 3. Escena 01 — SIGNAL

**Construido.** Campo 3D propio en GLSL: 21 120 vértices en **un solo draw
call** (`lineSegments`), con onda radial, decaimiento exponencial con la
distancia, batido de portadora y modulación de energía por el scroll. Mástil de
origen en el centro. Cinco etapas (A–E) cuyo resalte sigue el mismo número que
gobierna la energía del campo: **una sola causa para las dos cosas.**

**Funciona.** Es la pieza más fuerte del sitio. La propagación no es una
decoración: es la onda que describe el texto, con decaimiento real. El mástil
ancla el origen, sin el cual el campo flotaba sin causa. La sección se lee como
un instrumento, no como un efecto. El recorrido A→E con opacidad progresiva
convierte el texto que Sender ya tenía en el eje de la escena.

**No funciona / debe cambiar.**
- **La versión WebGL se ve mejor que el sustituto 2D, y eso es un problema.**
  El `<canvas>` 2D de respaldo es correcto pero claramente inferior. Debe
  mejorarse en el hito 10.
- El contraste de las etiquetas de etapa sobre el campo vivo no es estable: el
  velo ayuda, pero un pico de energía bajo un texto lo baja. El velo debería ser
  ligeramente más opaco en la franja de texto.
- El campo tarda ~1,5 s en "asentarse" tras el montaje: el primer fotograma
  visible tiene el campo en reposo.

**Violaciones del DNA:** ninguna. Es la escena que más se apoya en §8.2.

**Móvil.** 2 432 px. El canvas a `dpr: 1` rinde bien. El campo pierde detalle
—esperable— pero conserva la lectura de propagación.

**Rendimiento.** Three.js (714 KB, ≈ 180 KB gzip) entra por `import()` diferido:
no toca el primer fotograma. Un solo draw call, sin postprocesado, `dispose()` en
desmontaje, `requestAnimationFrame` pausado fuera de pestaña.

---

## 4. Escena 02 — SENDER y 04 — TRANSMISSION

**02 · Construido.** `+20` en `display-xl` como única cifra, cuatro dominios en
`col-3`, cuatro tramos de historia sin fechas, y **la nota de honestidad del
proyecto visible en pantalla**: «Sender no publica cifras de proyectos ni fechas
de hitos». Split 7/5.

**02 · Funciona.** La honestidad como rasgo de diseño funciona: en vez de fingir
un «sobre nosotros», dice lo que no publica. El split 7/5 cumple la prohibición
del 6/6.

**02 · No funciona.** El bloque de historia (imagen + 4 tramos) es la parte más
convencional de todo el sitio: es una lista. Podría quedarse, pero es donde más
se parece a una web corporativa normal.

**04 · Construido.** Seis etapas de la cadena en un raíl horizontal que el scroll
vertical desplaza. Barra de progreso. Imagen de estación costera.

**04 · Funciona.** La metáfora es correcta: la cadena se recorre, no se lista.
El desplazamiento lateral sin secuestrar el scroll se siente natural.

**04 · No funciona.**
- **La densidad es baja:** seis tarjetas de 320 px en 1 601 px de recorrido.
  En una pantalla ancha sobra espacio vacío a la derecha.
- El raíl **no está topado**: con `overflow: hidden` el desplazamiento se calcula
  pero no se limita explícitamente; en pantallas muy anchas podría sobrar
  desplazamiento y quedar hueco al final.
- En `prefers-reduced-motion` el raíl se apila en columna: correcto, pero pierde
  por completo la idea de cadena. Debería conservar al menos el orden numerado
  con una línea de conexión.

**Violaciones del DNA:** ninguna.

**Móvil.** 04 baja a 1 524 px. La imagen de estación costera queda muy apretada
en vertical.

---

## 5. Escena 03 — ENGINEERING

**Construido.** Seis disciplinas en `col-4`, y **un diagrama polar cuyos lóbulos
se calculan de verdad** con el factor de arreglo
`AF(θ) = |sin(Nψ/2) / (N sin(ψ/2))|` para N = 5, d = 0,35 λ. Los nulos, los
lóbulos secundarios y sus amplitudes son los que da la física. Las seis bandas de
operación con sus rangos documentados, seleccionables. Bloque de materia con
`cap-rf`.

**Funciona.** El diagrama polar es la segunda pieza irremplazable del sitio. Un
lóbulo principal a lo largo del eje, lóbulos secundarios más pequeños, nulos
exactos: es un instrumento de medida, no un adorno. La retícula de medida del
propio SVG (anillos a 0,25, radios cada 30°) refuerza la lectura.

**No funciona / debe cambiar.**
- El panel instrumento + bandas deja **un vacío grande** debajo de las bandas en
  escritorio. La columna izquierda (420 px de diagrama) es mucho más corta que
  las seis bandas apiladas.
- El diagrama no cambia al seleccionar banda: solo cambia la etiqueta `banda NN`.
  Sería más honesto llamarlo lo que es —un patrón de referencia— o hacer que el
  espaciado `d` varíe con la banda.
- El `<figure>` tiene `role="img"` con `aria-label` correcto, pero **el pie con
  `N = 5`, `d = 0.35 λ` es `aria-hidden`**: esa información es el dato real y
  debería ser legible por un lector de pantalla.

**Violaciones del DNA:** una menor. `D = 0.35` está escrito como constante
mientras el pie dice «banda NN»: la interfaz sugiere una variación que no
existe. Es una promesa incumplida de la propia interfaz.

**Móvil.** 4 259 px — la escena más larga. Las seis disciplinas se apilan y el
diagrama queda legible, pero el recorrido es largo.

---

## 6. Escena 05 — PROYECTOS

**Construido.** Seis instalaciones documentadas en una lista activa + ficha
sticky. Cada ficha lleva tecnología, lugar y **fuente enlazada cuando existe**
(Radio World para Ambato). Cuando no existe: «Sin fuente pública enlazada.»

**Funciona.** Enseñar la ausencia de fuente en vez de rellenarla con un logo de
cliente es exactamente lo que el brief pide. Que el modelo `Project` **no tenga
campo `year`** y la interfaz simplemente no lo muestre es la decisión de diseño
más disciplinada del proyecto.

**No funciona / debe cambiar.**
- **Es el punto más débil del sitio en móvil.** 2 001 px: la lista de seis
  elementos apilada sobre la ficha obliga a recorrer toda la lista antes de ver
  nada. En móvil debería colapsar a un acordeón: solo la ficha activa visible.
- La ficha sticky en escritorio se pega a `top: 128px` sin tener en cuenta la
  altura del nav cuando este reaparece al subir: puede quedar tapada.
- Dos proyectos comparten `img.capAntennas` (02 y 03) y eso se nota al recorrer
  la lista: la misma foto sirve a dos fichas distintas.
- `proj-am.jpg` no aparece en esta escena aunque es una foto de proyecto real
  (gabinete de transmisor). Está asignada a PRODUCTOS.

**Violaciones del DNA:** una, de §6.2. `cap-antennas` se usa en dos proyectos
distintos de la misma escena, lo que la regla prohíbe explícitamente. Es
consecuencia de tener solo diez fotografías para nueve escenas, pero la regla
dice lo que dice: o se acepta la repetición de forma declarada, o el rol de una
de las dos fichas cambia.

**Rendimiento.** Es la escena con más intercambio de imágenes al recorrerla.
Todas van `loading="lazy"` con `sizes` correcto.

---

## 7. Escena 06 — PRODUCTOS

**Construido.** Las 7 categorías como estaciones seleccionables y los 16
productos con sus especificaciones reales en una ficha modal: grupos de specs,
variantes, características, aplicaciones y `sourceUrl` a la ficha publicada.
`Esc` cierra, el foco entra en el botón de cierre, el scroll de fondo se detiene.

**Funciona.** Es el catálogo completo funcionando como instrumento: `DataRow` en
mono con `tabular-nums` hace que las columnas de especificaciones se alineen de
verdad. La ficha declara que la descarga está pendiente en lugar de ofrecer un
PDF que no existe.

**No funciona / debe cambiar.**
- **La ficha modal no atrapa el foco.** `autoFocus` en el botón de cierre y cierre
  con `Esc` están, pero **no hay focus trap**: con `Tab` se sale a la página de
  detrás. Es un incumplimiento real de accesibilidad, no un detalle.
- Catorce de los dieciséis productos comparten seis fotografías. Es inevitable
  con diez originales, pero conviene declararlo en la interfaz en vez de dejarlo
  como una repetición silenciosa.
- `proj-stl` y `cap-antennas` aparecen tanto en PROYECTOS como en PRODUCTOS
  (roles `PROJECTS` y `PRODUCTS`). Riesgo de lectura confusa.
- La lista de categorías en móvil se desplaza en horizontal sin indicación de que
  hay más a la derecha.

**Violaciones del DNA:** una de accesibilidad (§12 declara foco gestionado).
El focus trap falta.

**Móvil.** 2 646 px. La ficha modal funciona bien a 360 px, con ajuste de
`max-height: 92svh` y scroll interno.

---

## 8. Escena 07 — PROCESO

**Construido.** Consola de instrumentación con los **canales de monitoreo
documentados** del sistema NAVTEX y del procesador BIS-AP735: voltaje, potencia,
temperatura, audio, GPRS, control remoto, estado del sistema. Las cuatro razones
técnicas. Imagen de trampa de RF.

**Funciona.** El panel **declara en pantalla que es una interfaz demostrativa y
no telemetría en vivo** — es la diferencia exacta entre esto y un dashboard
genérico prohibido por §13.1.4. Los botones de banda del panel son informativos y
no simulan lecturas aleatorias: la posición de cada barra es estable, no ruido.
El `IntersectionObserver` apaga el intervalo cuando el panel sale de pantalla.

**No funciona / debe cambiar.**
- El panel es **estático**: las barras no cambian nunca. Un intervalo late el
  indicador de estado pero las barras quedan fijas. Es honesto pero muerto;
  conviene decidir si se quiere así.
- Los cuatro módulos usan `col-5`, lo que deja la fila descuadrada (2 + 2 con
  hueco a la derecha de 2 columnas). En escritorio se ve el desequilibrio.
- La densidad del panel en móvil: 7 canales apilados es una lista larga.

**Violaciones del DNA:** ninguna. Es la escena que mejor cumple §13.1.4 y §13.1.6.

---

## 9. Escena 08 — CONTACTO

**Construido.** Cierre centrado, medida corta. Dirección, teléfono y los dos
correos reales, con WhatsApp. Formulario que **compone el mensaje en el cliente
de correo**, con los diez tipos de requerimiento y la nota explícita de que el
sitio no almacena datos.

**Funciona.** El formulario sin backend es una decisión de diseño, no una
carencia: no recoger datos de nadie es coherente con una empresa que no publica
lo que no tiene documentado. La nota lo dice en los dos idiomas.

**No funciona / debe cambiar.**
- **El formulario no valida el mensaje vacío más allá de `required`** y no hay
  estado de error visible con `aria-live`. Si falta un campo, el navegador
  bloquea sin explicar.
- `mailto:` con cuerpo largo tiene un límite de longitud en algunos clientes: un
  mensaje extenso puede truncarse. Debería advertirse o acortarse el compuesto.
- **El `mailto` como acción principal es frágil.** Sin cliente de correo
  configurado (móvil sin app), no pasa nada visible. El WhatsApp como alternativa
  ayuda, pero es el canal secundario.

**Violaciones del DNA:** ninguna de forma; una de robustez (§13.3 pregunta 3).

**Móvil.** 2 039 px. El formulario apilado ocupa bastante, pero funciona.

---

## 10. Rendimiento

| Métrica | Valor |
|---|---|
| Paquete inicial | 120 KB (≈ 38 KB gzip) |
| React | 239 KB (≈ 76 KB gzip) |
| three.js + R3F + drei | 714 KB (≈ 180 KB gzip), **diferido** |
| Fuentes | 8 × woff2, 22–24 KB cada una, subset latin |
| Fotografías | AVIF 11–116 KB por variante; **AVIF primero**, WebP después, JPG de respaldo |
| Video del hero | 4,8 MB MP4, **sin WebM ni variantes** |

**Lo que está bien.** Three.js no entra en el primer fotograma. Cada escena es un
chunk propio. Las fotos se sirven por `srcSet` con `sizes` reales y formatos en
cascada. `dpr` acotado a [1, 1.75] y a 1 en móvil.

**Lo que falta.**
- **El video del hero no está optimizado.** Es el mayor peso del sitio con
  diferencia: 4,8 MB contra ~300 KB de todo lo demás. Sin WebM/VP9, sin
  variantes por resolución, con `preload="auto"`. Es la tarea más importante del
  hito 09.
- No hay preload de fuentes ni `font-display` selectivo por peso.
- Sin presupuesto de rendimiento automatizado en CI (Lighthouse).
- El grano fílmico es un `background-image` SVG con `feTurbulence` en cada
  figura: barato, pero repetido en cada `<figure>`.

---

## 11. Accesibilidad

**Cumple.** `reduced-motion` neutralizado de forma global (no por archivo, para
no olvidar ninguno). Foco visible en todo. Skip link primero en el DOM. `lang`
declarado y actualizado por idioma. Todas las imágenes con `alt` bilingüe real.
Toda la navegación por teclado. Contrastes medidos y verificados.

**No cumple todavía.**
1. **Falta focus trap en la ficha de producto** — el único incumplimiento serio.
2. **El visor modal no devuelve el foco** al botón que lo abrió al cerrarse.
3. `aria-live` ausente en el resultado del formulario.
4. El pie del diagrama polar está `aria-hidden` siendo información real.
5. El raíl horizontal de TRANSMISSION no tiene equivalente navegable por teclado
   más allá del scroll de la página.

---

## 12. SEO

**Cumple.** Rutas `/es/` y `/en/` reales con `canonical` propio. `hreflang`
recíproco ES ↔ EN ↔ `x-default`. JSON-LD **independiente por idioma**:
`Organization`, `ItemList` del catálogo con 16 `Product`, bandas y las 6
instalaciones documentadas. `sitemap.xml` con 18 URLs anotadas con `hreflang`.
`robots.txt`. Open Graph y Twitter Card por idioma.

**Limitación declarada.** Al ser una SPA, las etiquetas se escriben en el cliente.
Los rastreadores que ejecutan JavaScript las ven completas; para los que no, hace
falta prerender o SSG. El contenido esencial está en el HTML servido y no depende
de ello para leerse, pero **un `title` correcto desde el servidor es mejor**.
Es la tarea principal del hito 09.

**Nota.** El sitio actual en WordPress no tiene meta description, no declara Open
Graph y no es bilingüe. En ese sentido, esta versión ya supera a producción en
todas esas dimensiones.

---

## 13. Cumplimiento del brief

| Requisito | Estado |
|---|---|
| Paleta de 4 colores, sin matices prohibidos | ✓ verificado por auditor (0 hallazgos) |
| Sin vocabulario prohibido | ✓ 5 términos ES/EN, 0 apariciones |
| Sin invención de clientes, fechas, cifras, certificaciones | ✓ auditor + regla del proyecto heredada |
| Solo fotografías reales, ninguna de stock | ✓ 10 originales, 0 peticiones externas |
| Bilingüe ES/EN completo | ✓ 680 pares; nomenclatura técnica idéntica por diseño |
| 9 escenas 00–08 | ✓ |
| Anti-slop: sin esfera, sin partículas aleatorias, sin glass, sin degradado genérico | ✓ |
| 3D con propósito | ✓ propagación y diagrama calculado |
| Accesibilidad WCAG | parcial — falta focus trap |
| Performance | parcial — falta optimizar el video |
| **Aprobación del Hero** | **pendiente: es la persona quien decide** |
| Rama `immersive-redesign` con 12 commits | pendiente — sin credenciales de escritura |

---

## 14. Qué debe cambiar, por prioridad

### Hito 09 — Rendimiento y entrega
1. **Optimizar el video del hero**: WebM/VP9 + 3 resoluciones + `preload` según
   conexión. Es el mayor lastre del sitio.
2. Prerender o SSG para que `title` y `hreflang` vengan del servidor.

### Hito 10 — Accesibilidad
3. **Focus trap en la ficha de producto** y devolución del foco al cerrar.
4. `aria-live` en el resultado del formulario.
5. Sacar el pie del diagrama polar de `aria-hidden`.
6. Mejorar el sustituto 2D del campo de señal.

### Hito 11 — Refinamiento visual
7. **PROYECTOS en móvil: acordeón** en vez de lista + ficha.
8. Equilibrar el panel instrumento/bandas de INGENIERÍA.
9. Elevar la densidad del raíl de TRANSMISSION o acortar su recorrido.
10. Resolver la repetición de `cap-antennas` en dos fichas de la misma escena.

### Hito 12 — QA final
11. Lighthouse en móvil y escritorio con presupuesto en CI.
12. Repaso de contraste **con las imágenes cargadas**, no solo con los tokens.
13. Prueba con lector de pantalla en los dos idiomas.

---

## 15. Lo que no se toca

- Las diez fotografías: son las que son y no se sustituyen.
- Los precios: Sender no publica precios y el catálogo no los muestra porque no
  existen en la fuente.
- Las fechas de los proyectos: el modelo no tiene el campo y no se añadirá.
- La paleta: cuatro colores, sin excepción.
- Ninguna sección inventada para «redondear» el recorrido.

---

## 16. Refinamientos aplicados tras esta crítica

Los apartados §3 a §9 se escribieron **antes** de arreglar lo que describen. Se
dejan tal cual, con sus defectos, porque así queda el registro del ciclo. Esto es
lo que se corrigió después:

| Defecto | Apartado | Estado |
|---|---|---|
| Falta de foco atrapado en la ficha de producto | §7, §11 | **Corregido.** `useFocusTrap` atrapa el foco y lo devuelve al botón que abrió la ficha. |
| El pie del diagrama polar era `aria-hidden` siendo dato real | §5, §11 | **Corregido.** El `<figcaption>` es legible por lectores de pantalla. |
| PROYECTOS en móvil obligaba a recorrer la lista entera | §6, §14 | **Corregido.** Acordeón por debajo de 1000 px: la ficha se despliega dentro de la entrada. |
| Sin `aria-live` en el resultado del formulario | §9, §11 | **Corregido.** `role="status"` con `aria-live="polite"`. |
| El raíl de TRANSMISSION no estaba topado | §4 | **Corregido.** Desplazamiento acotado a lo que realmente sobra. |
| En movimiento reducido la cadena perdía su idea | §4 | **Corregido.** Se conserva con línea continua y nodos; ya no es una lista suelta. |
| El panel de INGENIERÍA dejaba un hueco visible | §5 | **Corregido.** Columnas centradas verticalmente. |
| El nombre del proyecto llegaba hasta el filo en móvil | §6 | **Corregido.** Espacio reservado para el marcador de despliegue. |

### Lo que sigue pendiente y por qué

- **La aprobación visual del Hero.** No es un defecto: es el punto de control del
  brief. No lo decide el agente.
- **Optimizar el video del hero.** Requiere recodificar a WebM/VP9 en varias
  resoluciones. Es una tarea del hito 09, no de la crítica.
- **Prerender.** Necesita decidir el modo de despliegue primero.
- **Repetición de `cap-antennas` en dos fichas de PROYECTOS.** Con diez
  fotografías para nueve escenas es una consecuencia aritmética. La salida
  honesta es declararlo en la interfaz, no disimularlo con un recorte distinto
  que finja ser otra foto. Queda como decisión abierta para la persona.
- **Contraste con las imágenes cargadas.** Los 25 pares medidos son de tokens
  sobre fondos planos. Falta medir el texto que va sobre fotografía, ya con el
  velo aplicado. Es parte del hito 12.

---

## 17. Veredicto

El sitio **cumple todas las reglas duras del brief**: paleta cerrada, sin
vocabulario prohibido, sin datos inventados, sin imágenes que no sean reales,
bilingüe completo, nueve escenas, cero hallazgos en el auditor automático y
cero errores de consola en los dos idiomas y los dos perfiles de pantalla.

Lo que lo separa de un ejercicio correcto son dos piezas: **el campo de
propagación** de la 01 y **el diagrama polar calculado** de la 03. Ninguna de las
dos podría estar en la web de otra empresa sin dejar de ser cierta, y ninguna de
las dos existiría si el diseño se hubiera limitado a ilustrar el contenido.

Lo que le falta es lo que decide si esto se publica: **la aprobación del Hero**,
que no corresponde al agente, y las tres tareas de rendimiento del hito 09.
