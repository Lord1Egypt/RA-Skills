# Prompts por plataforma · 35 fichas de carrusel

> GENERADO por el equipo de FÓRMULA 100K. No lo edites: edita la fuente y vuelve a correrlo.

## Cómo elegir dónde lo haces

| Herramienta | Cuándo | Costo | Texto |
|---|---|---|---|
| **Claude Code** (skill `carrusel-formatos-f100k`) | Tienes Claude Code instalado | Gratis con tu plan | Perfecto (HTML) |
| **HTML en cualquier chat** (Claude, ChatGPT o Gemini con Canvas) | No tienes Claude Code, quieres texto perfecto | Gratis con tu plan | Perfecto (HTML) |
| **Gemini** (Nano Banana) | Soportes físicos, fotos, ilustración, poco texto | Según tu plan de Gemini | Bueno, revisa tildes |
| **ChatGPT** (Imágenes) | Igual que Gemini; conversa mejor para corregir | Según tu plan de ChatGPT | Bueno, revisa tildes |

**Gemini:** usa el modelo de imagen (Nano Banana; si tu plan trae la versión Pro, escribe mejor el texto). Pide «vertical 4:5» en el prompt: el modelo lo acepta. **ChatGPT:** también acepta 4:5 si lo pides; si te devuelve otra proporción, pídela de nuevo o recorta dejando el texto dentro del margen.
**Siempre en este orden:** 1) guion con el prompt de guion (en cualquier chat) → 2) apruebas el texto → 3) fabricas.
**Variantes de imagen:** **A** desde la descripción (sin adjuntar nada) · **B** con tu marca · **C** solo el fondo sin texto (el texto va después en HTML).
Después de la portada usa el prompt **«seguir»** para cada slide, y **«arreglar»** si una palabra sale mal.

---

## F01 · Causa y consecuencia ("¿por qué te pasó esto?")

**Ejemplo:** @kennithlee_ · https://www.instagram.com/p/Dc4PCI6nz9f/ · 6.258 likes · 5 slides

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 110 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: dos fotos personales de celular apiladas a sangre, cada una el 50% del alto, sin separador; fotos NO producidas (casa, carro, playa) y de colores distintos entre la de arriba y la de abajo.
PALETA (usa SOLO estos colores): #FFFFFF = texto, con sombra negra difusa · #000000 = sombra del texto al 50%
TIPOGRAFÍA:
- frase de cada foto: Inter 400, minúsculas, sin negrita, 34 px; texto chico tipo subtítulo: la sorpresa es la frase, no la letra
PORTADA: NO hay portada con título: la primera slide ya es la mecánica. Mitad de arriba: «dejé de [acción]» centrado a ~28% del alto. Mitad de abajo: «y [lo que pasó]» centrado a ~76%. Una línea por foto, máx. 80% del ancho.
SLIDES DEL MEDIO: el mismo molde con otra pareja de fotos y otra frase partida («empecé a…» / «y…»); el cambio de color entre foto de arriba y de abajo marca el ritmo.
CIERRE: la frase que cambia la culpa de lugar («no alejaste a nadie» / «solo dejaste de doblarte para retenerlos»), mismo molde, sin CTA en la imagen.
ELEMENTOS GRÁFICOS: ninguno: sin logo, sin número, sin flecha · fotos reales tuyas, no de banco
EVITA: fotos de banco o caras que no son tuyas; revisa la frase letra por letra (un error de tipeo se nota en grande).
```

> Cada slide lleva poco texto (máx. ~12 palabras): el modelo lo puede escribir, pero revisa tildes y eñes letra por letra antes de publicar.

### 1 · Guion (cualquier chat)
```
Escribe un carrusel de 5 slides en formato "frase partida" sobre [TEMA: un cambio que hiciste en tu vida o negocio, ej. subir precios].
Cada slide tiene DOS mitades:
- ARRIBA: "dejé de [acción concreta]" o "empecé a [acción concreta]" (máx. 5 palabras).
- ABAJO: "y [consecuencia incómoda que vino después]" (máx. 6 palabras).
Slides 1-4 siguen ese molde, cada una más dura que la anterior.
Slide 5 es el reencuadre: ARRIBA "no [la culpa que te echaron]", ABAJO "solo [la verdad que eso significaba]".
Reglas: minúsculas, sin emojis, sin título de portada, sin CTA en las slides (el CTA va en el caption).
Para cada mitad sugiere qué foto MÍA usar (lugar + qué estoy haciendo), de carrete, nada posado.
Devuelve una tabla: slide | texto arriba | foto arriba | texto abajo | foto abajo.
```

### 2 · Claude Code
```
hazme un carrusel tipo F01 (Causa y consecuencia ("¿por qué te pasó esto?")) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 110 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: dos fotos personales de celular apiladas a sangre, cada una el 50% del alto, sin separador; fotos NO producidas (casa, carro, playa) y de colores distintos entre la de arriba y la de abajo.
PALETA (usa SOLO estos colores): #FFFFFF = texto, con sombra negra difusa · #000000 = sombra del texto al 50%
TIPOGRAFÍA:
- frase de cada foto: Inter 400, minúsculas, sin negrita, 34 px; texto chico tipo subtítulo: la sorpresa es la frase, no la letra
PORTADA: NO hay portada con título: la primera slide ya es la mecánica. Mitad de arriba: «dejé de [acción]» centrado a ~28% del alto. Mitad de abajo: «y [lo que pasó]» centrado a ~76%. Una línea por foto, máx. 80% del ancho.
SLIDES DEL MEDIO: el mismo molde con otra pareja de fotos y otra frase partida («empecé a…» / «y…»); el cambio de color entre foto de arriba y de abajo marca el ritmo.
CIERRE: la frase que cambia la culpa de lugar («no alejaste a nadie» / «solo dejaste de doblarte para retenerlos»), mismo molde, sin CTA en la imagen.
ELEMENTOS GRÁFICOS: ninguno: sin logo, sin número, sin flecha · fotos reales tuyas, no de banco
EVITA: fotos de banco o caras que no son tuyas; revisa la frase letra por letra (un error de tipeo se nota en grande).

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 110 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~10% a los lados y nada importante en el 9% de abajo.
FONDO: dos fotos personales de celular apiladas a sangre, cada una el 50% del alto, sin separador; fotos NO producidas (casa, carro, playa) y de colores distintos entre la de arriba y la de abajo.
PALETA (usa SOLO estos colores): #FFFFFF = texto, con sombra negra difusa · #000000 = sombra del texto al 50%
TIPOGRAFÍA:
- frase de cada foto: estilo Inter (400), minúsculas, sin negrita, letra de ~3% del alto; texto chico tipo subtítulo: la sorpresa es la frase, no la letra
COMPOSICIÓN DE ESTA SLIDE: NO hay portada con título: la primera slide ya es la mecánica. Mitad de arriba: «dejé de [acción]» centrado a ~28% del alto. Mitad de abajo: «y [lo que pasó]» centrado a ~76%. Una línea por foto, máx. 80% del ancho.
ELEMENTOS GRÁFICOS: ninguno: sin logo, sin número, sin flecha · fotos reales tuyas, no de banco
EVITA: fotos de banco o caras que no son tuyas; revisa la frase letra por letra (un error de tipeo se nota en grande).
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: dos fotos personales de celular apiladas a sangre, cada una el 50% del alto, sin separador; fotos NO producidas (casa, carro, playa) y de colores distintos entre la de arriba y la de abajo.
COMPOSICIÓN: NO hay portada con título: la primera slide ya es la mecánica. Mitad de arriba: «dejé de [acción]» centrado a ~28% del alto. Mitad de abajo: «y [lo que pasó]» centrado a ~76%. Una línea por foto, máx. 80% del ancho.
ELEMENTOS: ninguno: sin logo, sin número, sin flecha · fotos reales tuyas, no de banco
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: lleva tus fotos o capturas reales (dos fotos personales de celular apiladas a sangre, cada una el 50% del alto, sin separador; fotos NO producidas (casa, carro, playa) y de colores distintos entre la de arriba y la de abajo.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: el mismo molde con otra pareja de fotos y otra frase partida («empecé a…» / «y…»); el cambio de color entre foto de arriba y de abajo marca el ritmo.
(Si es la última slide, la composición es: la frase que cambia la culpa de lugar («no alejaste a nadie» / «solo dejaste de doblarte para retenerlos»), mismo molde, sin CTA en la imagen.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~10% a los lados y nada importante en el 9% de abajo.
FONDO: dos fotos personales de celular apiladas a sangre, cada una el 50% del alto, sin separador; fotos NO producidas (casa, carro, playa) y de colores distintos entre la de arriba y la de abajo.
PALETA (usa SOLO estos colores): #FFFFFF = texto, con sombra negra difusa · #000000 = sombra del texto al 50%
TIPOGRAFÍA:
- frase de cada foto: estilo Inter (400), minúsculas, sin negrita, letra de ~3% del alto; texto chico tipo subtítulo: la sorpresa es la frase, no la letra
COMPOSICIÓN DE ESTA SLIDE: NO hay portada con título: la primera slide ya es la mecánica. Mitad de arriba: «dejé de [acción]» centrado a ~28% del alto. Mitad de abajo: «y [lo que pasó]» centrado a ~76%. Una línea por foto, máx. 80% del ancho.
ELEMENTOS GRÁFICOS: ninguno: sin logo, sin número, sin flecha · fotos reales tuyas, no de banco
EVITA: fotos de banco o caras que no son tuyas; revisa la frase letra por letra (un error de tipeo se nota en grande).
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: dos fotos personales de celular apiladas a sangre, cada una el 50% del alto, sin separador; fotos NO producidas (casa, carro, playa) y de colores distintos entre la de arriba y la de abajo.
COMPOSICIÓN: NO hay portada con título: la primera slide ya es la mecánica. Mitad de arriba: «dejé de [acción]» centrado a ~28% del alto. Mitad de abajo: «y [lo que pasó]» centrado a ~76%. Una línea por foto, máx. 80% del ancho.
ELEMENTOS: ninguno: sin logo, sin número, sin flecha · fotos reales tuyas, no de banco
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: lleva tus fotos o capturas reales (dos fotos personales de celular apiladas a sangre, cada una el 50% del alto, sin separador; fotos NO producidas (casa, carro, playa) y de colores distintos entre la de arriba y la de abajo.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: el mismo molde con otra pareja de fotos y otra frase partida («empecé a…» / «y…»); el cambio de color entre foto de arriba y de abajo marca el ritmo.
(Si es la última slide, la composición es: la frase que cambia la culpa de lugar («no alejaste a nadie» / «solo dejaste de doblarte para retenerlos»), mismo molde, sin CTA en la imagen.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## F02 · Pantalla dividida: casos en serie

**Ejemplo:** @businessbulls.in · https://www.instagram.com/p/Dc-MNF-im1r/ · 2.703 likes · 6 slides

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 60 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: arriba (0-50%) foto de las personas del caso con degradado a negro en el borde inferior; abajo (50-100%) foto del resultado (local, producto, logo) con degradado a negro al pie.
PALETA (usa SOLO estos colores): #FEFDFD = texto de arriba · #ECF735 = texto de abajo, el golpe · #050105 = degradados
TIPOGRAFÍA:
- las dos frases: Montserrat 800, MAYÚSCULAS, centradas, 48 px; arriba termina en «…», abajo en «.»
PORTADA: el primer caso ya es la portada: franja de texto blanco a ~47% del alto sobre el degradado de la foto de arriba («DOS AMIGAS SE JUNTARON…») y franja amarilla lima a ~95% sobre el degradado de abajo («Y CREARON [RESULTADO].»); píldora «desliza ›» con borde blanco arriba a la derecha.
SLIDES DEL MEDIO: el MISMO molde idéntico con otro caso: solo cambian las dos fotos y el final de la frase (anáfora visual).
CIERRE: último caso con el remate más cercano al lector («Y AHORA TE TOCA A TI.»).
ELEMENTOS GRÁFICOS: degradados negros que sostienen el texto · píldora «desliza ›» con borde blanco · logo chico arriba a la izquierda en blanco semitransparente
EVITA: logos o píldoras de marcas ajenas; nunca generes con IA caras de personas reales: usa casos propios o de clientas con permiso.
```

> Cada slide lleva poco texto (máx. ~12 palabras): el modelo lo puede escribir, pero revisa tildes y eñes letra por letra antes de publicar.

### 1 · Guion (cualquier chat)
```
Crea un carrusel de 6 slides en formato "pantalla dividida en serie" sobre [TEMA: ej. clientas que empezaron sin seguidores].
Frase fija de ARRIBA (igual en las 6 slides, máx. 5 palabras, termina en "…"): [ej. "EMPEZÓ CON 200 SEGUIDORES…"].
Frase de ABAJO (cambia en cada slide, empieza con "Y", máx. 6 palabras): el resultado concreto y verificable de cada caso.
Ordena los casos de menos a más impactante.
Para cada slide dime: foto de arriba (la persona o el antes) y foto de abajo (el resultado visible: producto, local, pantalla con cifra).
Estilo: mayúsculas bold, texto de abajo en [COLOR DE ACENTO] sobre degradado oscuro.
Solo casos reales que yo te dé; si falta un dato, déjalo como [FALTA DATO], no lo inventes.
```

### 2 · Claude Code
```
hazme un carrusel tipo F02 (Pantalla dividida: casos en serie) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 60 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: arriba (0-50%) foto de las personas del caso con degradado a negro en el borde inferior; abajo (50-100%) foto del resultado (local, producto, logo) con degradado a negro al pie.
PALETA (usa SOLO estos colores): #FEFDFD = texto de arriba · #ECF735 = texto de abajo, el golpe · #050105 = degradados
TIPOGRAFÍA:
- las dos frases: Montserrat 800, MAYÚSCULAS, centradas, 48 px; arriba termina en «…», abajo en «.»
PORTADA: el primer caso ya es la portada: franja de texto blanco a ~47% del alto sobre el degradado de la foto de arriba («DOS AMIGAS SE JUNTARON…») y franja amarilla lima a ~95% sobre el degradado de abajo («Y CREARON [RESULTADO].»); píldora «desliza ›» con borde blanco arriba a la derecha.
SLIDES DEL MEDIO: el MISMO molde idéntico con otro caso: solo cambian las dos fotos y el final de la frase (anáfora visual).
CIERRE: último caso con el remate más cercano al lector («Y AHORA TE TOCA A TI.»).
ELEMENTOS GRÁFICOS: degradados negros que sostienen el texto · píldora «desliza ›» con borde blanco · logo chico arriba a la izquierda en blanco semitransparente
EVITA: logos o píldoras de marcas ajenas; nunca generes con IA caras de personas reales: usa casos propios o de clientas con permiso.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 60 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: arriba (0-50%) foto de las personas del caso con degradado a negro en el borde inferior; abajo (50-100%) foto del resultado (local, producto, logo) con degradado a negro al pie.
PALETA (usa SOLO estos colores): #FEFDFD = texto de arriba · #ECF735 = texto de abajo, el golpe · #050105 = degradados
TIPOGRAFÍA:
- las dos frases: estilo Montserrat (800), MAYÚSCULAS, centradas, letra de ~4% del alto; arriba termina en «…», abajo en «.»
COMPOSICIÓN DE ESTA SLIDE: el primer caso ya es la portada: franja de texto blanco a ~47% del alto sobre el degradado de la foto de arriba («DOS AMIGAS SE JUNTARON…») y franja amarilla lima a ~95% sobre el degradado de abajo («Y CREARON [RESULTADO].»); píldora «desliza ›» con borde blanco arriba a la derecha.
ELEMENTOS GRÁFICOS: degradados negros que sostienen el texto · píldora «desliza ›» con borde blanco · logo chico arriba a la izquierda en blanco semitransparente
EVITA: logos o píldoras de marcas ajenas; nunca generes con IA caras de personas reales: usa casos propios o de clientas con permiso.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: arriba (0-50%) foto de las personas del caso con degradado a negro en el borde inferior; abajo (50-100%) foto del resultado (local, producto, logo) con degradado a negro al pie.
COMPOSICIÓN: el primer caso ya es la portada: franja de texto blanco a ~47% del alto sobre el degradado de la foto de arriba («DOS AMIGAS SE JUNTARON…») y franja amarilla lima a ~95% sobre el degradado de abajo («Y CREARON [RESULTADO].»); píldora «desliza ›» con borde blanco arriba a la derecha.
ELEMENTOS: degradados negros que sostienen el texto · píldora «desliza ›» con borde blanco · logo chico arriba a la izquierda en blanco semitransparente
```
**C · Solo fondo, sin texto**
```
Genera SOLO EL FONDO de un slide de carrusel, imagen vertical 4:5, SIN NINGÚN TEXTO, letra, número ni logo.
Foto hiperrealista vertical partida en dos: arriba [PERSONAS DEL CASO] posando juntas, abajo [EL RESULTADO: local, producto], degradado negro en el borde inferior de cada mitad, sin texto ni logos.
Deja libre de objetos la zona donde irá el texto: la franja de ~45-50% y la de ~92-98% del alto.
Paleta: #FEFDFD = texto de arriba · #ECF735 = texto de abajo, el golpe · #050105 = degradados.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: el MISMO molde idéntico con otro caso: solo cambian las dos fotos y el final de la frase (anáfora visual).
(Si es la última slide, la composición es: último caso con el remate más cercano al lector («Y AHORA TE TOCA A TI.»).)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: arriba (0-50%) foto de las personas del caso con degradado a negro en el borde inferior; abajo (50-100%) foto del resultado (local, producto, logo) con degradado a negro al pie.
PALETA (usa SOLO estos colores): #FEFDFD = texto de arriba · #ECF735 = texto de abajo, el golpe · #050105 = degradados
TIPOGRAFÍA:
- las dos frases: estilo Montserrat (800), MAYÚSCULAS, centradas, letra de ~4% del alto; arriba termina en «…», abajo en «.»
COMPOSICIÓN DE ESTA SLIDE: el primer caso ya es la portada: franja de texto blanco a ~47% del alto sobre el degradado de la foto de arriba («DOS AMIGAS SE JUNTARON…») y franja amarilla lima a ~95% sobre el degradado de abajo («Y CREARON [RESULTADO].»); píldora «desliza ›» con borde blanco arriba a la derecha.
ELEMENTOS GRÁFICOS: degradados negros que sostienen el texto · píldora «desliza ›» con borde blanco · logo chico arriba a la izquierda en blanco semitransparente
EVITA: logos o píldoras de marcas ajenas; nunca generes con IA caras de personas reales: usa casos propios o de clientas con permiso.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: arriba (0-50%) foto de las personas del caso con degradado a negro en el borde inferior; abajo (50-100%) foto del resultado (local, producto, logo) con degradado a negro al pie.
COMPOSICIÓN: el primer caso ya es la portada: franja de texto blanco a ~47% del alto sobre el degradado de la foto de arriba («DOS AMIGAS SE JUNTARON…») y franja amarilla lima a ~95% sobre el degradado de abajo («Y CREARON [RESULTADO].»); píldora «desliza ›» con borde blanco arriba a la derecha.
ELEMENTOS: degradados negros que sostienen el texto · píldora «desliza ›» con borde blanco · logo chico arriba a la izquierda en blanco semitransparente
```
**C · Solo fondo, sin texto**
```
Crea una imagen vertical 4:5 que sirva de FONDO para un slide. Importante: SIN texto, letras, números, logos ni marcas de agua.
Foto hiperrealista vertical partida en dos: arriba [PERSONAS DEL CASO] posando juntas, abajo [EL RESULTADO: local, producto], degradado negro en el borde inferior de cada mitad, sin texto ni logos.
Deja vacía la zona de la franja de ~45-50% y la de ~92-98% del alto: ahí pondré el texto después.
Colores: #FEFDFD = texto de arriba · #ECF735 = texto de abajo, el golpe · #050105 = degradados.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: el MISMO molde idéntico con otro caso: solo cambian las dos fotos y el final de la frase (anáfora visual).
(Si es la última slide, la composición es: último caso con el remate más cercano al lector («Y AHORA TE TOCA A TI.»).)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## F03 · Tutorial comando → resultado

**Ejemplo:** @profesiondelfuturo · https://www.instagram.com/p/DdMlaYVoA7e/ · 9.011 likes · 178 comentarios · 8 slides

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: blanco #FFFFFF liso en instrucción y resultado; el cierre en celeste #67C1F5.
PALETA (usa SOLO estos colores): #FFFFFF = fondo · #000000 = texto · #131313 = caja de la captura del chat · #E53935 = subrayado a mano bajo el comando · #67C1F5 = fondo del cierre · #FFD33F = sticker amarillo del cierre · #F42484 = sticker rosa del cierre
TIPOGRAFÍA:
- titular: Poppins 700, 46 px
- comando dentro de la captura: JetBrains Mono 500, 34 px
PORTADA: ícono STOP rojo arriba al centro; titular de 2 líneas «Deja de publicar [lo malo] así» (8-30% del alto); 2 ejemplos malos lado a lado; «Usa estos 3 comandos en [herramienta] →» al pie.
SLIDES DEL MEDIO: alterna dos slides: INSTRUCCIÓN = titular arriba + captura del chat (caja negra, 85% del ancho) con el comando escrito y subrayado a mano en rojo; RESULTADO = la imagen que salió a sangre lateral con el titular arriba.
CIERRE: fondo celeste con 3 etiquetas tipo sticker (amarilla con texto negro, blanca, rosa con texto blanco) y el CTA.
ELEMENTOS GRÁFICOS: subrayado rojo hecho a mano bajo el comando · capturas REALES, nunca simuladas · firma gris muy claro al pie
EVITA: comandos que no probaste tú; tratar de «usted»; capturas simuladas.
```

> Cada slide lleva poco texto (máx. ~20 palabras): el modelo lo puede escribir, pero revisa tildes y eñes letra por letra antes de publicar.

### 1 · Guion (cualquier chat)
```
Arma un carrusel tutorial de 8 slides "comando → resultado" para [HERRAMIENTA] y [RESULTADO que quiere mi cliente ideal].
Slide 1: "Deja de [error visible que comete mi audiencia]" + describe 2 ejemplos del error + "Usa estos 3 [prompts/comandos] →".
Slides 2, 4 y 6: "Ahora escribe:" + el prompt/comando EXACTO (cópialo tal cual, corto) + qué captura de pantalla tomar.
Slides 3, 5 y 7: una línea de lo que logra ("Crea una publicidad limpia y sin cara de IA") + qué resultado mostrar a pantalla completa.
Slide 8: CTA "Comenta [PALABRA] y te mando [recurso]".
Reglas: fondo blanco, título negro bold arriba, máximo 12 palabras por slide. Los prompts deben funcionar de verdad: si no estás segura de que existe un comando, escríbelo como prompt completo en vez de inventar un atajo.
```

### 2 · Claude Code
```
hazme un carrusel tipo F03 (Tutorial comando → resultado) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: blanco #FFFFFF liso en instrucción y resultado; el cierre en celeste #67C1F5.
PALETA (usa SOLO estos colores): #FFFFFF = fondo · #000000 = texto · #131313 = caja de la captura del chat · #E53935 = subrayado a mano bajo el comando · #67C1F5 = fondo del cierre · #FFD33F = sticker amarillo del cierre · #F42484 = sticker rosa del cierre
TIPOGRAFÍA:
- titular: Poppins 700, 46 px
- comando dentro de la captura: JetBrains Mono 500, 34 px
PORTADA: ícono STOP rojo arriba al centro; titular de 2 líneas «Deja de publicar [lo malo] así» (8-30% del alto); 2 ejemplos malos lado a lado; «Usa estos 3 comandos en [herramienta] →» al pie.
SLIDES DEL MEDIO: alterna dos slides: INSTRUCCIÓN = titular arriba + captura del chat (caja negra, 85% del ancho) con el comando escrito y subrayado a mano en rojo; RESULTADO = la imagen que salió a sangre lateral con el titular arriba.
CIERRE: fondo celeste con 3 etiquetas tipo sticker (amarilla con texto negro, blanca, rosa con texto blanco) y el CTA.
ELEMENTOS GRÁFICOS: subrayado rojo hecho a mano bajo el comando · capturas REALES, nunca simuladas · firma gris muy claro al pie
EVITA: comandos que no probaste tú; tratar de «usted»; capturas simuladas.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 80 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: blanco #FFFFFF liso en instrucción y resultado; el cierre en celeste #67C1F5.
PALETA (usa SOLO estos colores): #FFFFFF = fondo · #000000 = texto · #131313 = caja de la captura del chat · #E53935 = subrayado a mano bajo el comando · #67C1F5 = fondo del cierre · #FFD33F = sticker amarillo del cierre · #F42484 = sticker rosa del cierre
TIPOGRAFÍA:
- titular: estilo Poppins (700), letra de ~3% del alto
- comando dentro de la captura: estilo JetBrains Mono (500), letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: ícono STOP rojo arriba al centro; titular de 2 líneas «Deja de publicar [lo malo] así» (8-30% del alto); 2 ejemplos malos lado a lado; «Usa estos 3 comandos en [herramienta] →» al pie.
ELEMENTOS GRÁFICOS: subrayado rojo hecho a mano bajo el comando · capturas REALES, nunca simuladas · firma gris muy claro al pie
EVITA: comandos que no probaste tú; tratar de «usted»; capturas simuladas.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: blanco #FFFFFF liso en instrucción y resultado; el cierre en celeste #67C1F5.
COMPOSICIÓN: ícono STOP rojo arriba al centro; titular de 2 líneas «Deja de publicar [lo malo] así» (8-30% del alto); 2 ejemplos malos lado a lado; «Usa estos 3 comandos en [herramienta] →» al pie.
ELEMENTOS: subrayado rojo hecho a mano bajo el comando · capturas REALES, nunca simuladas · firma gris muy claro al pie
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (blanco #FFFFFF liso en instrucción y resultado; el cierre en celeste #67C1F5.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: alterna dos slides: INSTRUCCIÓN = titular arriba + captura del chat (caja negra, 85% del ancho) con el comando escrito y subrayado a mano en rojo; RESULTADO = la imagen que salió a sangre lateral con el titular arriba.
(Si es la última slide, la composición es: fondo celeste con 3 etiquetas tipo sticker (amarilla con texto negro, blanca, rosa con texto blanco) y el CTA.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: blanco #FFFFFF liso en instrucción y resultado; el cierre en celeste #67C1F5.
PALETA (usa SOLO estos colores): #FFFFFF = fondo · #000000 = texto · #131313 = caja de la captura del chat · #E53935 = subrayado a mano bajo el comando · #67C1F5 = fondo del cierre · #FFD33F = sticker amarillo del cierre · #F42484 = sticker rosa del cierre
TIPOGRAFÍA:
- titular: estilo Poppins (700), letra de ~3% del alto
- comando dentro de la captura: estilo JetBrains Mono (500), letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: ícono STOP rojo arriba al centro; titular de 2 líneas «Deja de publicar [lo malo] así» (8-30% del alto); 2 ejemplos malos lado a lado; «Usa estos 3 comandos en [herramienta] →» al pie.
ELEMENTOS GRÁFICOS: subrayado rojo hecho a mano bajo el comando · capturas REALES, nunca simuladas · firma gris muy claro al pie
EVITA: comandos que no probaste tú; tratar de «usted»; capturas simuladas.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: blanco #FFFFFF liso en instrucción y resultado; el cierre en celeste #67C1F5.
COMPOSICIÓN: ícono STOP rojo arriba al centro; titular de 2 líneas «Deja de publicar [lo malo] así» (8-30% del alto); 2 ejemplos malos lado a lado; «Usa estos 3 comandos en [herramienta] →» al pie.
ELEMENTOS: subrayado rojo hecho a mano bajo el comando · capturas REALES, nunca simuladas · firma gris muy claro al pie
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (blanco #FFFFFF liso en instrucción y resultado; el cierre en celeste #67C1F5.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: alterna dos slides: INSTRUCCIÓN = titular arriba + captura del chat (caja negra, 85% del ancho) con el comando escrito y subrayado a mano en rojo; RESULTADO = la imagen que salió a sangre lateral con el titular arriba.
(Si es la última slide, la composición es: fondo celeste con 3 etiquetas tipo sticker (amarilla con texto negro, blanca, rosa con texto blanco) y el CTA.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## F04 · Tutorial en libreta

**Ejemplo:** @karoempowerment · https://www.instagram.com/p/DdHSQg1mJ_1/ · 977 comentarios · 5 slides

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 90 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: foto cenital de una libreta abierta sostenida por una mano (abajo a la derecha, ~15% del alto) sobre mesa de madera cálida desenfocada, con un objeto amarillo desenfocado arriba a la izquierda.
PALETA (usa SOLO estos colores): #D2C0A7 = papel crema con renglones tenues · #040000 = tinta · #DDBA41 = resaltador mostaza, franja completa · #764D29 = madera
TIPOGRAFÍA:
- título de portada: Patrick Hand 400, 54 px
- cuerpo con viñetas: Patrick Hand 400, 34 px
PORTADA: la página izquierda ocupa ~75% del ancho; título de 3-4 líneas en el tercio superior de la página con la promesa resaltada en mostaza; subtítulo entre paréntesis debajo.
SLIDES DEL MEDIO: «N. [paso]» como título (15-30% de la página), 4-6 viñetas cortas (35-70%) y un remate resaltado (72-82%); rayitas de énfasis a mano.
CIERRE: «¿Quieres [el método completo]? Comenta [PALABRA] y te lo envío por privado», con la palabra resaltada.
ELEMENTOS GRÁFICOS: mano real sosteniendo la libreta · resaltador SOLO en la promesa y en la palabra del CTA · garabatos mínimos (rayitas, corazón)
EVITA: promesas de cifras que no puedes sostener («+1 MILLÓN»); firmas o nombres que no son tuyos.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Escribe un carrusel de 5 slides "tutorial en libreta" sobre [RESULTADO DESEADO] usando [HERRAMIENTA].
Slide 1: "Cómo [lograr resultado con cifra concreta]" + en paréntesis la objeción que quitas: "(aunque [limitación de mi audiencia])". Marca con **asteriscos** la frase que va con resaltador.
Slides 2-4: "N. [Paso en 3-5 palabras]" + máx. 5 viñetas cortas + una frase final resaltada que explique por qué importa.
Slide 5: "¿Quieres [el método completo]?" + "Comenta: [PALABRA]" + "y te lo envío por privado."
Máx. 45 palabras por slide (tiene que parecer escrito a mano). Numera corrido.
Luego dame el prompt de imagen para el FONDO (sin texto): foto cenital de una libreta abierta de hojas color hueso sostenida por una mano, sobre mesa de madera cálida, luz de ventana suave, página en blanco, formato 4:5.
```

### 2 · Claude Code
```
hazme un carrusel tipo F04 (Tutorial en libreta) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 90 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: foto cenital de una libreta abierta sostenida por una mano (abajo a la derecha, ~15% del alto) sobre mesa de madera cálida desenfocada, con un objeto amarillo desenfocado arriba a la izquierda.
PALETA (usa SOLO estos colores): #D2C0A7 = papel crema con renglones tenues · #040000 = tinta · #DDBA41 = resaltador mostaza, franja completa · #764D29 = madera
TIPOGRAFÍA:
- título de portada: Patrick Hand 400, 54 px
- cuerpo con viñetas: Patrick Hand 400, 34 px
PORTADA: la página izquierda ocupa ~75% del ancho; título de 3-4 líneas en el tercio superior de la página con la promesa resaltada en mostaza; subtítulo entre paréntesis debajo.
SLIDES DEL MEDIO: «N. [paso]» como título (15-30% de la página), 4-6 viñetas cortas (35-70%) y un remate resaltado (72-82%); rayitas de énfasis a mano.
CIERRE: «¿Quieres [el método completo]? Comenta [PALABRA] y te lo envío por privado», con la palabra resaltada.
ELEMENTOS GRÁFICOS: mano real sosteniendo la libreta · resaltador SOLO en la promesa y en la palabra del CTA · garabatos mínimos (rayitas, corazón)
EVITA: promesas de cifras que no puedes sostener («+1 MILLÓN»); firmas o nombres que no son tuyos.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 90 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~8% a los lados y nada importante en el 9% de abajo.
FONDO: foto cenital de una libreta abierta sostenida por una mano (abajo a la derecha, ~15% del alto) sobre mesa de madera cálida desenfocada, con un objeto amarillo desenfocado arriba a la izquierda.
PALETA (usa SOLO estos colores): #D2C0A7 = papel crema con renglones tenues · #040000 = tinta · #DDBA41 = resaltador mostaza, franja completa · #764D29 = madera
TIPOGRAFÍA:
- título de portada: estilo Patrick Hand (400), letra de ~4% del alto
- cuerpo con viñetas: estilo Patrick Hand (400), letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: la página izquierda ocupa ~75% del ancho; título de 3-4 líneas en el tercio superior de la página con la promesa resaltada en mostaza; subtítulo entre paréntesis debajo.
ELEMENTOS GRÁFICOS: mano real sosteniendo la libreta · resaltador SOLO en la promesa y en la palabra del CTA · garabatos mínimos (rayitas, corazón)
EVITA: promesas de cifras que no puedes sostener («+1 MILLÓN»); firmas o nombres que no son tuyos.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: foto cenital de una libreta abierta sostenida por una mano (abajo a la derecha, ~15% del alto) sobre mesa de madera cálida desenfocada, con un objeto amarillo desenfocado arriba a la izquierda.
COMPOSICIÓN: la página izquierda ocupa ~75% del ancho; título de 3-4 líneas en el tercio superior de la página con la promesa resaltada en mostaza; subtítulo entre paréntesis debajo.
ELEMENTOS: mano real sosteniendo la libreta · resaltador SOLO en la promesa y en la palabra del CTA · garabatos mínimos (rayitas, corazón)
```
**C · Solo fondo, sin texto**
```
Genera SOLO EL FONDO de un slide de carrusel, imagen vertical 4:5, SIN NINGÚN TEXTO, letra, número ni logo.
Foto cenital realista de una libreta abierta de papel crema con renglones tenues, sostenida por una mano en la esquina inferior derecha, sobre mesa de madera cálida desenfocada, objeto amarillo desenfocado arriba a la izquierda, luz natural suave, página COMPLETAMENTE EN BLANCO sin letras.
Deja libre de objetos la zona donde irá el texto: la página izquierda de la libreta.
Paleta: #D2C0A7 = papel crema con renglones tenues · #040000 = tinta · #DDBA41 = resaltador mostaza, franja completa · #764D29 = madera.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: «N. [paso]» como título (15-30% de la página), 4-6 viñetas cortas (35-70%) y un remate resaltado (72-82%); rayitas de énfasis a mano.
(Si es la última slide, la composición es: «¿Quieres [el método completo]? Comenta [PALABRA] y te lo envío por privado», con la palabra resaltada.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~8% a los lados y nada importante en el 9% de abajo.
FONDO: foto cenital de una libreta abierta sostenida por una mano (abajo a la derecha, ~15% del alto) sobre mesa de madera cálida desenfocada, con un objeto amarillo desenfocado arriba a la izquierda.
PALETA (usa SOLO estos colores): #D2C0A7 = papel crema con renglones tenues · #040000 = tinta · #DDBA41 = resaltador mostaza, franja completa · #764D29 = madera
TIPOGRAFÍA:
- título de portada: estilo Patrick Hand (400), letra de ~4% del alto
- cuerpo con viñetas: estilo Patrick Hand (400), letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: la página izquierda ocupa ~75% del ancho; título de 3-4 líneas en el tercio superior de la página con la promesa resaltada en mostaza; subtítulo entre paréntesis debajo.
ELEMENTOS GRÁFICOS: mano real sosteniendo la libreta · resaltador SOLO en la promesa y en la palabra del CTA · garabatos mínimos (rayitas, corazón)
EVITA: promesas de cifras que no puedes sostener («+1 MILLÓN»); firmas o nombres que no son tuyos.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: foto cenital de una libreta abierta sostenida por una mano (abajo a la derecha, ~15% del alto) sobre mesa de madera cálida desenfocada, con un objeto amarillo desenfocado arriba a la izquierda.
COMPOSICIÓN: la página izquierda ocupa ~75% del ancho; título de 3-4 líneas en el tercio superior de la página con la promesa resaltada en mostaza; subtítulo entre paréntesis debajo.
ELEMENTOS: mano real sosteniendo la libreta · resaltador SOLO en la promesa y en la palabra del CTA · garabatos mínimos (rayitas, corazón)
```
**C · Solo fondo, sin texto**
```
Crea una imagen vertical 4:5 que sirva de FONDO para un slide. Importante: SIN texto, letras, números, logos ni marcas de agua.
Foto cenital realista de una libreta abierta de papel crema con renglones tenues, sostenida por una mano en la esquina inferior derecha, sobre mesa de madera cálida desenfocada, objeto amarillo desenfocado arriba a la izquierda, luz natural suave, página COMPLETAMENTE EN BLANCO sin letras.
Deja vacía la zona de la página izquierda de la libreta: ahí pondré el texto después.
Colores: #D2C0A7 = papel crema con renglones tenues · #040000 = tinta · #DDBA41 = resaltador mostaza, franja completa · #764D29 = madera.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: «N. [paso]» como título (15-30% de la página), 4-6 viñetas cortas (35-70%) y un remate resaltado (72-82%); rayitas de énfasis a mano.
(Si es la última slide, la composición es: «¿Quieres [el método completo]? Comenta [PALABRA] y te lo envío por privado», con la palabra resaltada.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## F05 · Hábitos 10/10 en cuadrícula editorial

**Ejemplo:** @jun_yuh · https://www.instagram.com/p/Dcd2kFKEfY3/ · 20.369 likes · 8 slides (y un 2º post: https://www.instagram.com/p/DdEqGYwESZ8/)

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 60 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: cuadrícula 2×2 de cuadrantes iguales: arriba a la izquierda tu foto; arriba a la derecha bloque negro; abajo dos imágenes metafóricas desaturadas con UN acento de color.
PALETA (usa SOLO estos colores): #000000 = bloque de texto · #FFFFFF = texto principal · #BBBBBB = itálicas del bloque
TIPOGRAFÍA:
- hábito sobre la costura: Open Sans 700, minúsculas, 42 px
- etiqueta «10/10 hábitos»: Open Sans 700, minúsculas, 26 px
- bloque negro (normal / itálica / negrita): Open Sans 400 · 600 itálica · 700, minúsculas, 30 px
PORTADA: tu foto a sangre + título centrado en 2-3 líneas («10/10 hábitos para…») y subtítulo en itálica («y casi ninguno trata de ti…»).
SLIDES DEL MEDIO: cuadrícula fija; etiqueta chica arriba del bloque negro; el hábito en blanco centrado SOBRE la costura horizontal (47-58% del alto) cruzando las dos columnas; en el bloque negro 3 renglones: normal / itálica gris / negrita.
CIERRE: tu foto a sangre + pregunta en itálica + «comenta [PALABRA] ↓».
ELEMENTOS GRÁFICOS: la costura horizontal es donde vive el titular · imágenes metafóricas en b/n o sepia con un solo color puntual
EVITA: escribir «10/10» como si fueran 10 hábitos (es una nota); fotos de banco.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Crea un carrusel "10/10 hábitos" de 8 slides para [RESULTADO que quiere mi audiencia].
Slide 1: "10/10 hábitos para [resultado]" + subtítulo en itálica que quite la barrera ("y cualquiera puede empezar hoy…").
Slides 2-7 (6 hábitos): 
- TÍTULO del hábito (máx. 7 palabras, en minúsculas).
- BLOQUE de 3 capas: 1 frase que explica · 1 frase en *itálica* que matiza · 1 **remate en negrita** citable.
- IMAGEN METAFÓRICA 1 y 2: dos prompts de imagen artística que representen el hábito sin texto (ej. "pintura al óleo de un árbol con raíces enormes").
- FOTO MÍA sugerida (qué estoy haciendo).
Slide 8: una pregunta abierta que invite a responder con su experiencia.
Reglas: tono calmado, nada de "tienes que". La cuadrícula es: foto mía arriba izquierda, imágenes metafóricas en los otros dos cuadrantes, texto en bloque negro abajo derecha.
```

### 2 · Claude Code
```
hazme un carrusel tipo F05 (Hábitos 10/10 en cuadrícula editorial) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 60 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: cuadrícula 2×2 de cuadrantes iguales: arriba a la izquierda tu foto; arriba a la derecha bloque negro; abajo dos imágenes metafóricas desaturadas con UN acento de color.
PALETA (usa SOLO estos colores): #000000 = bloque de texto · #FFFFFF = texto principal · #BBBBBB = itálicas del bloque
TIPOGRAFÍA:
- hábito sobre la costura: Open Sans 700, minúsculas, 42 px
- etiqueta «10/10 hábitos»: Open Sans 700, minúsculas, 26 px
- bloque negro (normal / itálica / negrita): Open Sans 400 · 600 itálica · 700, minúsculas, 30 px
PORTADA: tu foto a sangre + título centrado en 2-3 líneas («10/10 hábitos para…») y subtítulo en itálica («y casi ninguno trata de ti…»).
SLIDES DEL MEDIO: cuadrícula fija; etiqueta chica arriba del bloque negro; el hábito en blanco centrado SOBRE la costura horizontal (47-58% del alto) cruzando las dos columnas; en el bloque negro 3 renglones: normal / itálica gris / negrita.
CIERRE: tu foto a sangre + pregunta en itálica + «comenta [PALABRA] ↓».
ELEMENTOS GRÁFICOS: la costura horizontal es donde vive el titular · imágenes metafóricas en b/n o sepia con un solo color puntual
EVITA: escribir «10/10» como si fueran 10 hábitos (es una nota); fotos de banco.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 60 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: cuadrícula 2×2 de cuadrantes iguales: arriba a la izquierda tu foto; arriba a la derecha bloque negro; abajo dos imágenes metafóricas desaturadas con UN acento de color.
PALETA (usa SOLO estos colores): #000000 = bloque de texto · #FFFFFF = texto principal · #BBBBBB = itálicas del bloque
TIPOGRAFÍA:
- hábito sobre la costura: estilo Open Sans (700), minúsculas, letra de ~3% del alto
- etiqueta «10/10 hábitos»: estilo Open Sans (700), minúsculas, letra de ~2% del alto
- bloque negro (normal / itálica / negrita): estilo Open Sans (400 · 600 itálica · 700), minúsculas, letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: tu foto a sangre + título centrado en 2-3 líneas («10/10 hábitos para…») y subtítulo en itálica («y casi ninguno trata de ti…»).
ELEMENTOS GRÁFICOS: la costura horizontal es donde vive el titular · imágenes metafóricas en b/n o sepia con un solo color puntual
EVITA: escribir «10/10» como si fueran 10 hábitos (es una nota); fotos de banco.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: cuadrícula 2×2 de cuadrantes iguales: arriba a la izquierda tu foto; arriba a la derecha bloque negro; abajo dos imágenes metafóricas desaturadas con UN acento de color.
COMPOSICIÓN: tu foto a sangre + título centrado en 2-3 líneas («10/10 hábitos para…») y subtítulo en itálica («y casi ninguno trata de ti…»).
ELEMENTOS: la costura horizontal es donde vive el titular · imágenes metafóricas en b/n o sepia con un solo color puntual
```
**C · Solo fondo, sin texto**
```
Genera SOLO EL FONDO de un slide de carrusel, imagen vertical 4:5, SIN NINGÚN TEXTO, letra, número ni logo.
Imagen editorial metafórica de [HÁBITO: ej. una silla vacía frente a una ventana], estilo pintura/foto desaturada en blanco y negro con un único acento de color [COLOR], sin texto, cuadrada.
Deja libre de objetos la zona donde irá el texto: el bloque negro y la costura central.
Paleta: #000000 = bloque de texto · #FFFFFF = texto principal · #BBBBBB = itálicas del bloque.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: cuadrícula fija; etiqueta chica arriba del bloque negro; el hábito en blanco centrado SOBRE la costura horizontal (47-58% del alto) cruzando las dos columnas; en el bloque negro 3 renglones: normal / itálica gris / negrita.
(Si es la última slide, la composición es: tu foto a sangre + pregunta en itálica + «comenta [PALABRA] ↓».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: cuadrícula 2×2 de cuadrantes iguales: arriba a la izquierda tu foto; arriba a la derecha bloque negro; abajo dos imágenes metafóricas desaturadas con UN acento de color.
PALETA (usa SOLO estos colores): #000000 = bloque de texto · #FFFFFF = texto principal · #BBBBBB = itálicas del bloque
TIPOGRAFÍA:
- hábito sobre la costura: estilo Open Sans (700), minúsculas, letra de ~3% del alto
- etiqueta «10/10 hábitos»: estilo Open Sans (700), minúsculas, letra de ~2% del alto
- bloque negro (normal / itálica / negrita): estilo Open Sans (400 · 600 itálica · 700), minúsculas, letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: tu foto a sangre + título centrado en 2-3 líneas («10/10 hábitos para…») y subtítulo en itálica («y casi ninguno trata de ti…»).
ELEMENTOS GRÁFICOS: la costura horizontal es donde vive el titular · imágenes metafóricas en b/n o sepia con un solo color puntual
EVITA: escribir «10/10» como si fueran 10 hábitos (es una nota); fotos de banco.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: cuadrícula 2×2 de cuadrantes iguales: arriba a la izquierda tu foto; arriba a la derecha bloque negro; abajo dos imágenes metafóricas desaturadas con UN acento de color.
COMPOSICIÓN: tu foto a sangre + título centrado en 2-3 líneas («10/10 hábitos para…») y subtítulo en itálica («y casi ninguno trata de ti…»).
ELEMENTOS: la costura horizontal es donde vive el titular · imágenes metafóricas en b/n o sepia con un solo color puntual
```
**C · Solo fondo, sin texto**
```
Crea una imagen vertical 4:5 que sirva de FONDO para un slide. Importante: SIN texto, letras, números, logos ni marcas de agua.
Imagen editorial metafórica de [HÁBITO: ej. una silla vacía frente a una ventana], estilo pintura/foto desaturada en blanco y negro con un único acento de color [COLOR], sin texto, cuadrada.
Deja vacía la zona de el bloque negro y la costura central: ahí pondré el texto después.
Colores: #000000 = bloque de texto · #FFFFFF = texto principal · #BBBBBB = itálicas del bloque.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: cuadrícula fija; etiqueta chica arriba del bloque negro; el hábito en blanco centrado SOBRE la costura horizontal (47-58% del alto) cruzando las dos columnas; en el bloque negro 3 renglones: normal / itálica gris / negrita.
(Si es la última slide, la composición es: tu foto a sangre + pregunta en itálica + «comenta [PALABRA] ↓».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## F06 · Personificación en scrapbook

**Ejemplo:** @profesiondelfuturo · https://www.instagram.com/p/DdPBiLxICxV/ · 53.408 likes · 1.533 comentarios · 9 slides

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 90 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: hoja de cuaderno espiral FOTOGRAFIADA a sangre (papel gris cálido, no blanco): espiral a la izquierda, margen rojo vertical, renglones azul pálido.
PALETA (usa SOLO estos colores): #C5BAB4 = papel · #010286 = tinta azul bolígrafo · #D32F2F = subrayado a mano bajo 1 palabra
TIPOGRAFÍA:
- frase del personaje: Caveat 600, 68 px; inclinada 2-5°
- renglón chico: Caveat 600, 40 px
PORTADA: texto manuscrito en 3-4 renglones arriba (8-45% del alto): el concepto HABLA en primera persona («Soy [X] y…»); personaje 3D tipo sticker (borde blanco grueso + sombra) abajo (45-95%).
SLIDES DEL MEDIO: la misma hoja; 1 frase por slide y 1-4 personajes sticker; UNA palabra subrayada en rojo.
CIERRE: giro emocional en una frase + corazón rojo a mano.
ELEMENTOS GRÁFICOS: personajes 3D recortados con borde blanco grueso · firma vertical sobre el margen izquierdo · subrayado rojo a mano
EVITA: personajes de otras marcas o logos como cara de personaje: crea los tuyos.
```

> Cada slide lleva poco texto (máx. ~20 palabras): el modelo lo puede escribir, pero revisa tildes y eñes letra por letra antes de publicar.

### 1 · Guion (cualquier chat)
```
Crea un carrusel de 9 slides en formato "personificación" sobre [LISTA DE CONCEPTOS/HERRAMIENTAS/ERRORES de mi nicho].
Elige un PERSONAJE VIEJO (lo que la gente todavía usa) y 4 PERSONAJES NUEVOS.
Slide 1: el viejo habla en primera persona: "Soy [X], me hice viejo y me quedé atrás." + "Pero tranquilo…"
Slide 2: "Estos son los [duros/reyes/nuevos] de hoy" + los 4 nuevos juntos.
Slides 3-6: "Soy [Y]" + qué hace en 1 frase + una frase de personalidad en segunda persona ("Tú me das la idea y yo…").
Slide 7: "Y ella es [MI NOMBRE]" + qué te enseña.
Slide 8: CTA a [RECURSO].
Slide 9: despedida emotiva y graciosa al personaje viejo.
Para cada personaje dame un prompt de sticker: "personaje 3D estilo Pixar de [objeto/concepto] con [rasgo de personalidad], cuerpo completo, contorno blanco de sticker, fondo transparente".
Todo el texto va escrito a mano en azul sobre hoja de cuaderno espiral; máx. 20 palabras por slide.
```

### 2 · Claude Code
```
hazme un carrusel tipo F06 (Personificación en scrapbook) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 90 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: hoja de cuaderno espiral FOTOGRAFIADA a sangre (papel gris cálido, no blanco): espiral a la izquierda, margen rojo vertical, renglones azul pálido.
PALETA (usa SOLO estos colores): #C5BAB4 = papel · #010286 = tinta azul bolígrafo · #D32F2F = subrayado a mano bajo 1 palabra
TIPOGRAFÍA:
- frase del personaje: Caveat 600, 68 px; inclinada 2-5°
- renglón chico: Caveat 600, 40 px
PORTADA: texto manuscrito en 3-4 renglones arriba (8-45% del alto): el concepto HABLA en primera persona («Soy [X] y…»); personaje 3D tipo sticker (borde blanco grueso + sombra) abajo (45-95%).
SLIDES DEL MEDIO: la misma hoja; 1 frase por slide y 1-4 personajes sticker; UNA palabra subrayada en rojo.
CIERRE: giro emocional en una frase + corazón rojo a mano.
ELEMENTOS GRÁFICOS: personajes 3D recortados con borde blanco grueso · firma vertical sobre el margen izquierdo · subrayado rojo a mano
EVITA: personajes de otras marcas o logos como cara de personaje: crea los tuyos.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 90 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~8% a los lados y nada importante en el 9% de abajo.
FONDO: hoja de cuaderno espiral FOTOGRAFIADA a sangre (papel gris cálido, no blanco): espiral a la izquierda, margen rojo vertical, renglones azul pálido.
PALETA (usa SOLO estos colores): #C5BAB4 = papel · #010286 = tinta azul bolígrafo · #D32F2F = subrayado a mano bajo 1 palabra
TIPOGRAFÍA:
- frase del personaje: estilo Caveat (600), letra de ~5% del alto; inclinada 2-5°
- renglón chico: estilo Caveat (600), letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: texto manuscrito en 3-4 renglones arriba (8-45% del alto): el concepto HABLA en primera persona («Soy [X] y…»); personaje 3D tipo sticker (borde blanco grueso + sombra) abajo (45-95%).
ELEMENTOS GRÁFICOS: personajes 3D recortados con borde blanco grueso · firma vertical sobre el margen izquierdo · subrayado rojo a mano
EVITA: personajes de otras marcas o logos como cara de personaje: crea los tuyos.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: hoja de cuaderno espiral FOTOGRAFIADA a sangre (papel gris cálido, no blanco): espiral a la izquierda, margen rojo vertical, renglones azul pálido.
COMPOSICIÓN: texto manuscrito en 3-4 renglones arriba (8-45% del alto): el concepto HABLA en primera persona («Soy [X] y…»); personaje 3D tipo sticker (borde blanco grueso + sombra) abajo (45-95%).
ELEMENTOS: personajes 3D recortados con borde blanco grueso · firma vertical sobre el margen izquierdo · subrayado rojo a mano
```
**C · Solo fondo, sin texto**
```
Genera SOLO EL FONDO de un slide de carrusel, imagen vertical 4:5, SIN NINGÚN TEXTO, letra, número ni logo.
Personaje 3D tierno de [CONCEPTO] estilo sticker recortado con borde blanco grueso y sombra suave, colores saturados, fondo transparente o blanco, sin texto.
Deja libre de objetos la zona donde irá el texto: los renglones de arriba.
Paleta: #C5BAB4 = papel · #010286 = tinta azul bolígrafo · #D32F2F = subrayado a mano bajo 1 palabra.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: la misma hoja; 1 frase por slide y 1-4 personajes sticker; UNA palabra subrayada en rojo.
(Si es la última slide, la composición es: giro emocional en una frase + corazón rojo a mano.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~8% a los lados y nada importante en el 9% de abajo.
FONDO: hoja de cuaderno espiral FOTOGRAFIADA a sangre (papel gris cálido, no blanco): espiral a la izquierda, margen rojo vertical, renglones azul pálido.
PALETA (usa SOLO estos colores): #C5BAB4 = papel · #010286 = tinta azul bolígrafo · #D32F2F = subrayado a mano bajo 1 palabra
TIPOGRAFÍA:
- frase del personaje: estilo Caveat (600), letra de ~5% del alto; inclinada 2-5°
- renglón chico: estilo Caveat (600), letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: texto manuscrito en 3-4 renglones arriba (8-45% del alto): el concepto HABLA en primera persona («Soy [X] y…»); personaje 3D tipo sticker (borde blanco grueso + sombra) abajo (45-95%).
ELEMENTOS GRÁFICOS: personajes 3D recortados con borde blanco grueso · firma vertical sobre el margen izquierdo · subrayado rojo a mano
EVITA: personajes de otras marcas o logos como cara de personaje: crea los tuyos.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: hoja de cuaderno espiral FOTOGRAFIADA a sangre (papel gris cálido, no blanco): espiral a la izquierda, margen rojo vertical, renglones azul pálido.
COMPOSICIÓN: texto manuscrito en 3-4 renglones arriba (8-45% del alto): el concepto HABLA en primera persona («Soy [X] y…»); personaje 3D tipo sticker (borde blanco grueso + sombra) abajo (45-95%).
ELEMENTOS: personajes 3D recortados con borde blanco grueso · firma vertical sobre el margen izquierdo · subrayado rojo a mano
```
**C · Solo fondo, sin texto**
```
Crea una imagen vertical 4:5 que sirva de FONDO para un slide. Importante: SIN texto, letras, números, logos ni marcas de agua.
Personaje 3D tierno de [CONCEPTO] estilo sticker recortado con borde blanco grueso y sombra suave, colores saturados, fondo transparente o blanco, sin texto.
Deja vacía la zona de los renglones de arriba: ahí pondré el texto después.
Colores: #C5BAB4 = papel · #010286 = tinta azul bolígrafo · #D32F2F = subrayado a mano bajo 1 palabra.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: la misma hoja; 1 frase por slide y 1-4 personajes sticker; UNA palabra subrayada en rojo.
(Si es la última slide, la composición es: giro emocional en una frase + corazón rojo a mano.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## F07 · Chuleta en lapicero (2 slides)

**Ejemplo:** @profesiondelfuturo · https://www.instagram.com/p/DdMAhxsHKa6/ · 45.532 likes · 468 comentarios · 2 slides

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 70 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: hoja rayada fotografiada con espiral a la izquierda y margen rojo vertical a ~12% del ancho.
PALETA (usa SOLO estos colores): #CDC8CA = papel · #B2B4BF = renglones · #A31536 = margen y subrayados · #19115F = tinta azul marino
TIPOGRAFÍA:
- título: Kalam 700, 42 px; subrayado doble rojo
- filas de la chuleta: Kalam 400, 22 px
- frase de la slide 2: Kalam 700, 54 px
PORTADA: slide 1 DENSA: título arriba (5-12%); a la izquierda (40-58% del alto) un NODO en recuadro de doble línea; de él salen ~25-28 líneas finas en abanico hasta cada fila «dato – qué hace», filas alineadas de 15% a 97% del alto (~90 palabras).
SLIDES DEL MEDIO: no hay: son 2 slides.
CIERRE: slide 2 casi vacía: frase centrada (35-62%) con escasez honesta y remate subrayado doble en rojo pidiendo seguir.
ELEMENTOS GRÁFICOS: líneas finas del nodo a cada fila · firma vertical en el margen · subrayado doble rojo
EVITA: cerrar con una frase genérica y tratar de «usted»; verifica cada fila (una mal = comentarios corrigiéndote).
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Hazme una chuleta de 2 slides sobre [TEMA con muchos datos cortos: atajos, prompts, frases, medidas].
Slide 1: título corto subrayado + 1 concepto central en un recuadro + 20 a 30 filas con formato "[dato] — [qué hace en 1-3 palabras]", agrupadas en ramas si hay categorías. Todo tiene que caber en UNA hoja.
Slide 2: una sola frase que invite a seguirme con escasez honesta, en mis palabras, tuteando. Ej.: "Créeme: esta cuenta no te va a volver a aparecer. Sígueme."
Verifica cada dato: si no estás 100% segura de uno, quítalo. Un dato falso en una chuleta arruina el guardado.
Formato visual: letra manuscrita azul sobre hoja de cuaderno rayada con margen rojo y espiral a la izquierda.
```

### 2 · Claude Code
```
hazme un carrusel tipo F07 (Chuleta en lapicero (2 slides)) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 70 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: hoja rayada fotografiada con espiral a la izquierda y margen rojo vertical a ~12% del ancho.
PALETA (usa SOLO estos colores): #CDC8CA = papel · #B2B4BF = renglones · #A31536 = margen y subrayados · #19115F = tinta azul marino
TIPOGRAFÍA:
- título: Kalam 700, 42 px; subrayado doble rojo
- filas de la chuleta: Kalam 400, 22 px
- frase de la slide 2: Kalam 700, 54 px
PORTADA: slide 1 DENSA: título arriba (5-12%); a la izquierda (40-58% del alto) un NODO en recuadro de doble línea; de él salen ~25-28 líneas finas en abanico hasta cada fila «dato – qué hace», filas alineadas de 15% a 97% del alto (~90 palabras).
SLIDES DEL MEDIO: no hay: son 2 slides.
CIERRE: slide 2 casi vacía: frase centrada (35-62%) con escasez honesta y remate subrayado doble en rojo pidiendo seguir.
ELEMENTOS GRÁFICOS: líneas finas del nodo a cada fila · firma vertical en el margen · subrayado doble rojo
EVITA: cerrar con una frase genérica y tratar de «usted»; verifica cada fila (una mal = comentarios corrigiéndote).

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 70 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: hoja rayada fotografiada con espiral a la izquierda y margen rojo vertical a ~12% del ancho.
PALETA (usa SOLO estos colores): #CDC8CA = papel · #B2B4BF = renglones · #A31536 = margen y subrayados · #19115F = tinta azul marino
TIPOGRAFÍA:
- título: estilo Kalam (700), letra de ~3% del alto; subrayado doble rojo
- filas de la chuleta: estilo Kalam (400), letra de ~2% del alto
- frase de la slide 2: estilo Kalam (700), letra de ~4% del alto
COMPOSICIÓN DE ESTA SLIDE: slide 1 DENSA: título arriba (5-12%); a la izquierda (40-58% del alto) un NODO en recuadro de doble línea; de él salen ~25-28 líneas finas en abanico hasta cada fila «dato – qué hace», filas alineadas de 15% a 97% del alto (~90 palabras).
ELEMENTOS GRÁFICOS: líneas finas del nodo a cada fila · firma vertical en el margen · subrayado doble rojo
EVITA: cerrar con una frase genérica y tratar de «usted»; verifica cada fila (una mal = comentarios corrigiéndote).
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: hoja rayada fotografiada con espiral a la izquierda y margen rojo vertical a ~12% del ancho.
COMPOSICIÓN: slide 1 DENSA: título arriba (5-12%); a la izquierda (40-58% del alto) un NODO en recuadro de doble línea; de él salen ~25-28 líneas finas en abanico hasta cada fila «dato – qué hace», filas alineadas de 15% a 97% del alto (~90 palabras).
ELEMENTOS: líneas finas del nodo a cada fila · firma vertical en el margen · subrayado doble rojo
```
**C · Solo fondo, sin texto**
```
Genera SOLO EL FONDO de un slide de carrusel, imagen vertical 4:5, SIN NINGÚN TEXTO, letra, número ni logo.
Foto cenital realista de una hoja de cuaderno rayada con espiral a la izquierda y margen rojo, papel gris lavanda, luz suave, COMPLETAMENTE EN BLANCO sin letras.
Deja libre de objetos la zona donde irá el texto: toda la hoja.
Paleta: #CDC8CA = papel · #B2B4BF = renglones · #A31536 = margen y subrayados · #19115F = tinta azul marino.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: no hay: son 2 slides.
(Si es la última slide, la composición es: slide 2 casi vacía: frase centrada (35-62%) con escasez honesta y remate subrayado doble en rojo pidiendo seguir.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: hoja rayada fotografiada con espiral a la izquierda y margen rojo vertical a ~12% del ancho.
PALETA (usa SOLO estos colores): #CDC8CA = papel · #B2B4BF = renglones · #A31536 = margen y subrayados · #19115F = tinta azul marino
TIPOGRAFÍA:
- título: estilo Kalam (700), letra de ~3% del alto; subrayado doble rojo
- filas de la chuleta: estilo Kalam (400), letra de ~2% del alto
- frase de la slide 2: estilo Kalam (700), letra de ~4% del alto
COMPOSICIÓN DE ESTA SLIDE: slide 1 DENSA: título arriba (5-12%); a la izquierda (40-58% del alto) un NODO en recuadro de doble línea; de él salen ~25-28 líneas finas en abanico hasta cada fila «dato – qué hace», filas alineadas de 15% a 97% del alto (~90 palabras).
ELEMENTOS GRÁFICOS: líneas finas del nodo a cada fila · firma vertical en el margen · subrayado doble rojo
EVITA: cerrar con una frase genérica y tratar de «usted»; verifica cada fila (una mal = comentarios corrigiéndote).
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: hoja rayada fotografiada con espiral a la izquierda y margen rojo vertical a ~12% del ancho.
COMPOSICIÓN: slide 1 DENSA: título arriba (5-12%); a la izquierda (40-58% del alto) un NODO en recuadro de doble línea; de él salen ~25-28 líneas finas en abanico hasta cada fila «dato – qué hace», filas alineadas de 15% a 97% del alto (~90 palabras).
ELEMENTOS: líneas finas del nodo a cada fila · firma vertical en el margen · subrayado doble rojo
```
**C · Solo fondo, sin texto**
```
Crea una imagen vertical 4:5 que sirva de FONDO para un slide. Importante: SIN texto, letras, números, logos ni marcas de agua.
Foto cenital realista de una hoja de cuaderno rayada con espiral a la izquierda y margen rojo, papel gris lavanda, luz suave, COMPLETAMENTE EN BLANCO sin letras.
Deja vacía la zona de toda la hoja: ahí pondré el texto después.
Colores: #CDC8CA = papel · #B2B4BF = renglones · #A31536 = margen y subrayados · #19115F = tinta azul marino.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: no hay: son 2 slides.
(Si es la última slide, la composición es: slide 2 casi vacía: frase centrada (35-62%) con escasez honesta y remate subrayado doble en rojo pidiendo seguir.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## F08 · Consejo en agenda

**Ejemplo:** @fedecaball · https://www.instagram.com/p/Dbv24imETWE/ · 5.814 likes · 1.602 comentarios · 4 slides

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 100 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: foto real con luz natural, un poco inclinada, de una página de agenda a sangre; slides 1-2 con cabecera impresa de casillas «D · M · A» y recuadro redondeado con renglones; slides 3-4 solo renglones.
PALETA (usa SOLO estos colores): #B3B4B3 = papel gris frío con sombra · #0A0A08 = tinta · #8E8F8E = líneas impresas
TIPOGRAFÍA:
- texto a mano: Patrick Hand 400, 48 px
- slide del CTA: Patrick Hand SC 400, versalitas, 48 px
PORTADA: cabecera «D · M · A» arriba (5-20%) y 4-6 renglones escritos a mano SOBRE las líneas, alineados a la izquierda: el consejo empieza como nota privada («Adopta el hábito de…»).
SLIDES DEL MEDIO: solo renglones; el paso con una lista de ✓ escrita a mano.
CIERRE: cambia la letra a versalitas a mano: la frase-idea + «COMENTA [PALABRA] Y TE ESCRIBO».
ELEMENTOS GRÁFICOS: texto que cae sobre los renglones · sin color de acento · cambio de letra en la slide del CTA
EVITA: el voseo (tú tuteas) y firmas de calígrafo que no son tuyas.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Escribe un carrusel de 4 slides "consejo en agenda" con UNA sola acción que mi audiencia puede hacer esta semana para [RESULTADO].
Slide 1: "Adopta el hábito de [acción concreta] todos los [día] por la [momento]…" (termina en puntos suspensivos).
Slide 2: cómo se hace, en 3 frases cortas (dónde, qué poner, qué escribir literal entre comillas).
Slide 3: qué ofrecer o qué hacer después, con 3 opciones marcadas con ✓ + la frase clave de fondo.
Slide 4: el porqué en 2 frases + "Si quieres que [ayuda personal], comenta: [PALABRA] y te escribo por mensaje."
Máx. 35 palabras por slide. Tutea (nada de voseo). Tono de nota personal.
Fondo (sin texto): foto de cerca de una agenda de papel gris claro con pestañas de mes y renglones, luz natural, formato 4:5.
```

### 2 · Claude Code
```
hazme un carrusel tipo F08 (Consejo en agenda) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 100 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: foto real con luz natural, un poco inclinada, de una página de agenda a sangre; slides 1-2 con cabecera impresa de casillas «D · M · A» y recuadro redondeado con renglones; slides 3-4 solo renglones.
PALETA (usa SOLO estos colores): #B3B4B3 = papel gris frío con sombra · #0A0A08 = tinta · #8E8F8E = líneas impresas
TIPOGRAFÍA:
- texto a mano: Patrick Hand 400, 48 px
- slide del CTA: Patrick Hand SC 400, versalitas, 48 px
PORTADA: cabecera «D · M · A» arriba (5-20%) y 4-6 renglones escritos a mano SOBRE las líneas, alineados a la izquierda: el consejo empieza como nota privada («Adopta el hábito de…»).
SLIDES DEL MEDIO: solo renglones; el paso con una lista de ✓ escrita a mano.
CIERRE: cambia la letra a versalitas a mano: la frase-idea + «COMENTA [PALABRA] Y TE ESCRIBO».
ELEMENTOS GRÁFICOS: texto que cae sobre los renglones · sin color de acento · cambio de letra en la slide del CTA
EVITA: el voseo (tú tuteas) y firmas de calígrafo que no son tuyas.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 100 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~9% a los lados y nada importante en el 9% de abajo.
FONDO: foto real con luz natural, un poco inclinada, de una página de agenda a sangre; slides 1-2 con cabecera impresa de casillas «D · M · A» y recuadro redondeado con renglones; slides 3-4 solo renglones.
PALETA (usa SOLO estos colores): #B3B4B3 = papel gris frío con sombra · #0A0A08 = tinta · #8E8F8E = líneas impresas
TIPOGRAFÍA:
- texto a mano: estilo Patrick Hand (400), letra de ~4% del alto
- slide del CTA: estilo Patrick Hand SC (400), versalitas, letra de ~4% del alto
COMPOSICIÓN DE ESTA SLIDE: cabecera «D · M · A» arriba (5-20%) y 4-6 renglones escritos a mano SOBRE las líneas, alineados a la izquierda: el consejo empieza como nota privada («Adopta el hábito de…»).
ELEMENTOS GRÁFICOS: texto que cae sobre los renglones · sin color de acento · cambio de letra en la slide del CTA
EVITA: el voseo (tú tuteas) y firmas de calígrafo que no son tuyas.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: foto real con luz natural, un poco inclinada, de una página de agenda a sangre; slides 1-2 con cabecera impresa de casillas «D · M · A» y recuadro redondeado con renglones; slides 3-4 solo renglones.
COMPOSICIÓN: cabecera «D · M · A» arriba (5-20%) y 4-6 renglones escritos a mano SOBRE las líneas, alineados a la izquierda: el consejo empieza como nota privada («Adopta el hábito de…»).
ELEMENTOS: texto que cae sobre los renglones · sin color de acento · cambio de letra en la slide del CTA
```
**C · Solo fondo, sin texto**
```
Genera SOLO EL FONDO de un slide de carrusel, imagen vertical 4:5, SIN NINGÚN TEXTO, letra, número ni logo.
Foto realista con luz natural de una página de agenda gris con cabecera impresa de casillas D M A y renglones, levemente inclinada, COMPLETAMENTE EN BLANCO sin escritura.
Deja libre de objetos la zona donde irá el texto: los renglones.
Paleta: #B3B4B3 = papel gris frío con sombra · #0A0A08 = tinta · #8E8F8E = líneas impresas.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: solo renglones; el paso con una lista de ✓ escrita a mano.
(Si es la última slide, la composición es: cambia la letra a versalitas a mano: la frase-idea + «COMENTA [PALABRA] Y TE ESCRIBO».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~9% a los lados y nada importante en el 9% de abajo.
FONDO: foto real con luz natural, un poco inclinada, de una página de agenda a sangre; slides 1-2 con cabecera impresa de casillas «D · M · A» y recuadro redondeado con renglones; slides 3-4 solo renglones.
PALETA (usa SOLO estos colores): #B3B4B3 = papel gris frío con sombra · #0A0A08 = tinta · #8E8F8E = líneas impresas
TIPOGRAFÍA:
- texto a mano: estilo Patrick Hand (400), letra de ~4% del alto
- slide del CTA: estilo Patrick Hand SC (400), versalitas, letra de ~4% del alto
COMPOSICIÓN DE ESTA SLIDE: cabecera «D · M · A» arriba (5-20%) y 4-6 renglones escritos a mano SOBRE las líneas, alineados a la izquierda: el consejo empieza como nota privada («Adopta el hábito de…»).
ELEMENTOS GRÁFICOS: texto que cae sobre los renglones · sin color de acento · cambio de letra en la slide del CTA
EVITA: el voseo (tú tuteas) y firmas de calígrafo que no son tuyas.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: foto real con luz natural, un poco inclinada, de una página de agenda a sangre; slides 1-2 con cabecera impresa de casillas «D · M · A» y recuadro redondeado con renglones; slides 3-4 solo renglones.
COMPOSICIÓN: cabecera «D · M · A» arriba (5-20%) y 4-6 renglones escritos a mano SOBRE las líneas, alineados a la izquierda: el consejo empieza como nota privada («Adopta el hábito de…»).
ELEMENTOS: texto que cae sobre los renglones · sin color de acento · cambio de letra en la slide del CTA
```
**C · Solo fondo, sin texto**
```
Crea una imagen vertical 4:5 que sirva de FONDO para un slide. Importante: SIN texto, letras, números, logos ni marcas de agua.
Foto realista con luz natural de una página de agenda gris con cabecera impresa de casillas D M A y renglones, levemente inclinada, COMPLETAMENTE EN BLANCO sin escritura.
Deja vacía la zona de los renglones: ahí pondré el texto después.
Colores: #B3B4B3 = papel gris frío con sombra · #0A0A08 = tinta · #8E8F8E = líneas impresas.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: solo renglones; el paso con una lista de ✓ escrita a mano.
(Si es la última slide, la composición es: cambia la letra a versalitas a mano: la frase-idea + «COMENTA [PALABRA] Y TE ESCRIBO».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## F09 · Tu foto fija + tarjeta

**Ejemplo:** @karoempowerment · https://www.instagram.com/p/DdNER9QGI1l/ · 79 comentarios · 5 slides · ojo: es 1:1

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 70 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: la MISMA foto tuya en todas las slides (plano medio, contrapicado, mirada fuera de cámara, pared lisa), ocupando todo el lienzo.
PALETA (usa SOLO estos colores): #FEFEFE = tarjeta · #000000 = tinta · #D15771 = acento rosa: círculo del paso, chispas (o tu color de marca) · #F4E7B8 = resaltador pálido · #F7CAAC = recuadro de remate
TIPOGRAFÍA:
- título en la tarjeta: Playfair Display 600, 54 px
- cuerpo: DM Sans 400, 26 px
- 1-2 palabras script: Yellowtail 400, 56 px
PORTADA: tarjeta blanca de esquinas redondeadas anclada abajo al centro (45-98% del alto, 60-75% del ancho) que tapa el torso y NUNCA la cara; título serif con 1 palabra en script subrayada en tu color.
SLIDES DEL MEDIO: la misma foto; la tarjeta cambia: número del paso en círculo de color, título serif, cuerpo sans chico, checklist con círculos ✓, ícono de la herramienta pegado al borde.
CIERRE: tarjeta con «Comenta [PALABRA] y te envío…» y la palabra resaltada.
ELEMENTOS GRÁFICOS: chispas/rayitas a mano en tu color · ícono de la herramienta pegado a la tarjeta · una palabra resaltada por renglón
EVITA: promesas de resultados diarios («1.000 todos los días»); un acento que choque con tu marca; formato cuadrado: hazlo 4:5.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Crea un carrusel de 5 slides "foto fija + tarjeta" sobre [CÓMO LOGRAR X con Y].
Todas las slides usan la misma foto mía de fondo; solo cambia la tarjeta.
Slide 1 (tarjeta portada): "Cómo [lograr resultado con cifra]" — marca la cifra para ir en caligrafía.
Slides 2-4 (tarjeta paso): número · título de máx. 8 palabras con 2 palabras a resaltar entre **asteriscos** · 3 viñetas con ✓ (o el prompt exacto entre comillas si el paso es "pídele esto").
Slide 5 (tarjeta CTA): "Comenta [PALABRA]" + 2 líneas de qué recibe.
Máx. 40 palabras por tarjeta. Dime qué foto mía funciona mejor (mirada, encuadre, espacio libre abajo).
```

### 2 · Claude Code
```
hazme un carrusel tipo F09 (Tu foto fija + tarjeta) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 70 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: la MISMA foto tuya en todas las slides (plano medio, contrapicado, mirada fuera de cámara, pared lisa), ocupando todo el lienzo.
PALETA (usa SOLO estos colores): #FEFEFE = tarjeta · #000000 = tinta · #D15771 = acento rosa: círculo del paso, chispas (o tu color de marca) · #F4E7B8 = resaltador pálido · #F7CAAC = recuadro de remate
TIPOGRAFÍA:
- título en la tarjeta: Playfair Display 600, 54 px
- cuerpo: DM Sans 400, 26 px
- 1-2 palabras script: Yellowtail 400, 56 px
PORTADA: tarjeta blanca de esquinas redondeadas anclada abajo al centro (45-98% del alto, 60-75% del ancho) que tapa el torso y NUNCA la cara; título serif con 1 palabra en script subrayada en tu color.
SLIDES DEL MEDIO: la misma foto; la tarjeta cambia: número del paso en círculo de color, título serif, cuerpo sans chico, checklist con círculos ✓, ícono de la herramienta pegado al borde.
CIERRE: tarjeta con «Comenta [PALABRA] y te envío…» y la palabra resaltada.
ELEMENTOS GRÁFICOS: chispas/rayitas a mano en tu color · ícono de la herramienta pegado a la tarjeta · una palabra resaltada por renglón
EVITA: promesas de resultados diarios («1.000 todos los días»); un acento que choque con tu marca; formato cuadrado: hazlo 4:5.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 70 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: la MISMA foto tuya en todas las slides (plano medio, contrapicado, mirada fuera de cámara, pared lisa), ocupando todo el lienzo.
PALETA (usa SOLO estos colores): #FEFEFE = tarjeta · #000000 = tinta · #D15771 = acento rosa: círculo del paso, chispas (o tu color de marca) · #F4E7B8 = resaltador pálido · #F7CAAC = recuadro de remate
TIPOGRAFÍA:
- título en la tarjeta: estilo Playfair Display (600), letra de ~4% del alto
- cuerpo: estilo DM Sans (400), letra de ~2% del alto
- 1-2 palabras script: estilo Yellowtail (400), letra de ~4% del alto
COMPOSICIÓN DE ESTA SLIDE: tarjeta blanca de esquinas redondeadas anclada abajo al centro (45-98% del alto, 60-75% del ancho) que tapa el torso y NUNCA la cara; título serif con 1 palabra en script subrayada en tu color.
ELEMENTOS GRÁFICOS: chispas/rayitas a mano en tu color · ícono de la herramienta pegado a la tarjeta · una palabra resaltada por renglón
EVITA: promesas de resultados diarios («1.000 todos los días»); un acento que choque con tu marca; formato cuadrado: hazlo 4:5.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: la MISMA foto tuya en todas las slides (plano medio, contrapicado, mirada fuera de cámara, pared lisa), ocupando todo el lienzo.
COMPOSICIÓN: tarjeta blanca de esquinas redondeadas anclada abajo al centro (45-98% del alto, 60-75% del ancho) que tapa el torso y NUNCA la cara; título serif con 1 palabra en script subrayada en tu color.
ELEMENTOS: chispas/rayitas a mano en tu color · ícono de la herramienta pegado a la tarjeta · una palabra resaltada por renglón
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: lleva tus fotos o capturas reales (la MISMA foto tuya en todas las slides (plano medio, contrapicado, mirada fuera de cámara, pared lisa), ocupando todo el lienzo.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: la misma foto; la tarjeta cambia: número del paso en círculo de color, título serif, cuerpo sans chico, checklist con círculos ✓, ícono de la herramienta pegado al borde.
(Si es la última slide, la composición es: tarjeta con «Comenta [PALABRA] y te envío…» y la palabra resaltada.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: la MISMA foto tuya en todas las slides (plano medio, contrapicado, mirada fuera de cámara, pared lisa), ocupando todo el lienzo.
PALETA (usa SOLO estos colores): #FEFEFE = tarjeta · #000000 = tinta · #D15771 = acento rosa: círculo del paso, chispas (o tu color de marca) · #F4E7B8 = resaltador pálido · #F7CAAC = recuadro de remate
TIPOGRAFÍA:
- título en la tarjeta: estilo Playfair Display (600), letra de ~4% del alto
- cuerpo: estilo DM Sans (400), letra de ~2% del alto
- 1-2 palabras script: estilo Yellowtail (400), letra de ~4% del alto
COMPOSICIÓN DE ESTA SLIDE: tarjeta blanca de esquinas redondeadas anclada abajo al centro (45-98% del alto, 60-75% del ancho) que tapa el torso y NUNCA la cara; título serif con 1 palabra en script subrayada en tu color.
ELEMENTOS GRÁFICOS: chispas/rayitas a mano en tu color · ícono de la herramienta pegado a la tarjeta · una palabra resaltada por renglón
EVITA: promesas de resultados diarios («1.000 todos los días»); un acento que choque con tu marca; formato cuadrado: hazlo 4:5.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: la MISMA foto tuya en todas las slides (plano medio, contrapicado, mirada fuera de cámara, pared lisa), ocupando todo el lienzo.
COMPOSICIÓN: tarjeta blanca de esquinas redondeadas anclada abajo al centro (45-98% del alto, 60-75% del ancho) que tapa el torso y NUNCA la cara; título serif con 1 palabra en script subrayada en tu color.
ELEMENTOS: chispas/rayitas a mano en tu color · ícono de la herramienta pegado a la tarjeta · una palabra resaltada por renglón
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: lleva tus fotos o capturas reales (la MISMA foto tuya en todas las slides (plano medio, contrapicado, mirada fuera de cámara, pared lisa), ocupando todo el lienzo.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: la misma foto; la tarjeta cambia: número del paso en círculo de color, título serif, cuerpo sans chico, checklist con círculos ✓, ícono de la herramienta pegado al borde.
(Si es la última slide, la composición es: tarjeta con «Comenta [PALABRA] y te envío…» y la palabra resaltada.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## F10 · Anáfora sobre fotos de tu vida (marca personal)

**Ejemplo:** @jun_yuh · https://www.instagram.com/p/Dc3-q8tkRup/ · 9.144 likes · 11 slides

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: una foto distinta de tu vida real a sangre en cada slide (gimnasio, museo, oficina), luz ambiente, algo oscura.
PALETA (usa SOLO estos colores): #FBFCFB = texto, con sombra negra difusa · #2B2B2B = dominante oscuro de las fotos
TIPOGRAFÍA:
- acción grande: Open Sans 700, minúsculas, 60 px
- prefijo y remate chicos: Open Sans 700 itálica, minúsculas, 34 px
PORTADA: 4 líneas grandes centradas arriba (12-40% del alto) con 1 palabra subrayada y la última en itálica.
SLIDES DEL MEDIO: el PREFIJO que se repite chico arriba («avergüénzate…») + la acción grande al centro + el remate chico desplazado a la derecha o abajo (60-80%). Texto directo sobre la foto, sin caja.
CIERRE: «sígueme para ver qué pasa cuando sigues» sobre una foto tuya.
ELEMENTOS GRÁFICOS: itálica y subrayado como único énfasis (sin color) · sin cajas ni fondos detrás del texto
EVITA: fotos de banco y frases de portada gastadas.
```

> Cada slide lleva poco texto (máx. ~25 palabras): el modelo lo puede escribir, pero revisa tildes y eñes letra por letra antes de publicar.

### 1 · Guion (cualquier chat)
```
Crea un carrusel de 11 slides con anáfora sobre [CREENCIA que frena a mi audiencia].
Slide 1: "si aguantas [incomodidad] durante [plazo corto], puedes [cambio grande]…"
Slide 2: la tesis en 2 frases: lo que la gente cree vs. lo que de verdad le pasa.
Slides 3-8: 
- PREFIJO fijo, igual en las 6 (máx. 3 palabras + "…"): [ej. "atrévete a…"]
- FRASE grande (máx. 10 palabras), marca 1 palabra en *itálica*.
- REMATE pequeño (máx. 9 palabras) que da la vuelta.
Slides 9-10: la conclusión en 2 frases.
Slide 11: "sígueme para ver qué pasa en [el reto/plazo]".
Para cada slide sugiere una foto MÍA distinta de mi vida real (lugar + acción). Nada de fotos posadas.
```

### 2 · Claude Code
```
hazme un carrusel tipo F10 (Anáfora sobre fotos de tu vida (marca personal)) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: una foto distinta de tu vida real a sangre en cada slide (gimnasio, museo, oficina), luz ambiente, algo oscura.
PALETA (usa SOLO estos colores): #FBFCFB = texto, con sombra negra difusa · #2B2B2B = dominante oscuro de las fotos
TIPOGRAFÍA:
- acción grande: Open Sans 700, minúsculas, 60 px
- prefijo y remate chicos: Open Sans 700 itálica, minúsculas, 34 px
PORTADA: 4 líneas grandes centradas arriba (12-40% del alto) con 1 palabra subrayada y la última en itálica.
SLIDES DEL MEDIO: el PREFIJO que se repite chico arriba («avergüénzate…») + la acción grande al centro + el remate chico desplazado a la derecha o abajo (60-80%). Texto directo sobre la foto, sin caja.
CIERRE: «sígueme para ver qué pasa cuando sigues» sobre una foto tuya.
ELEMENTOS GRÁFICOS: itálica y subrayado como único énfasis (sin color) · sin cajas ni fondos detrás del texto
EVITA: fotos de banco y frases de portada gastadas.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 80 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: una foto distinta de tu vida real a sangre en cada slide (gimnasio, museo, oficina), luz ambiente, algo oscura.
PALETA (usa SOLO estos colores): #FBFCFB = texto, con sombra negra difusa · #2B2B2B = dominante oscuro de las fotos
TIPOGRAFÍA:
- acción grande: estilo Open Sans (700), minúsculas, letra de ~4% del alto
- prefijo y remate chicos: estilo Open Sans (700 itálica), minúsculas, letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: 4 líneas grandes centradas arriba (12-40% del alto) con 1 palabra subrayada y la última en itálica.
ELEMENTOS GRÁFICOS: itálica y subrayado como único énfasis (sin color) · sin cajas ni fondos detrás del texto
EVITA: fotos de banco y frases de portada gastadas.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: una foto distinta de tu vida real a sangre en cada slide (gimnasio, museo, oficina), luz ambiente, algo oscura.
COMPOSICIÓN: 4 líneas grandes centradas arriba (12-40% del alto) con 1 palabra subrayada y la última en itálica.
ELEMENTOS: itálica y subrayado como único énfasis (sin color) · sin cajas ni fondos detrás del texto
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: lleva tus fotos o capturas reales (una foto distinta de tu vida real a sangre en cada slide (gimnasio, museo, oficina), luz ambiente, algo oscura.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: el PREFIJO que se repite chico arriba («avergüénzate…») + la acción grande al centro + el remate chico desplazado a la derecha o abajo (60-80%). Texto directo sobre la foto, sin caja.
(Si es la última slide, la composición es: «sígueme para ver qué pasa cuando sigues» sobre una foto tuya.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: una foto distinta de tu vida real a sangre en cada slide (gimnasio, museo, oficina), luz ambiente, algo oscura.
PALETA (usa SOLO estos colores): #FBFCFB = texto, con sombra negra difusa · #2B2B2B = dominante oscuro de las fotos
TIPOGRAFÍA:
- acción grande: estilo Open Sans (700), minúsculas, letra de ~4% del alto
- prefijo y remate chicos: estilo Open Sans (700 itálica), minúsculas, letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: 4 líneas grandes centradas arriba (12-40% del alto) con 1 palabra subrayada y la última en itálica.
ELEMENTOS GRÁFICOS: itálica y subrayado como único énfasis (sin color) · sin cajas ni fondos detrás del texto
EVITA: fotos de banco y frases de portada gastadas.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: una foto distinta de tu vida real a sangre en cada slide (gimnasio, museo, oficina), luz ambiente, algo oscura.
COMPOSICIÓN: 4 líneas grandes centradas arriba (12-40% del alto) con 1 palabra subrayada y la última en itálica.
ELEMENTOS: itálica y subrayado como único énfasis (sin color) · sin cajas ni fondos detrás del texto
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: lleva tus fotos o capturas reales (una foto distinta de tu vida real a sangre en cada slide (gimnasio, museo, oficina), luz ambiente, algo oscura.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: el PREFIJO que se repite chico arriba («avergüénzate…») + la acción grande al centro + el remate chico desplazado a la derecha o abajo (60-80%). Texto directo sobre la foto, sin caja.
(Si es la última slide, la composición es: «sígueme para ver qué pasa cuando sigues» sobre una foto tuya.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## F11 · Historia de origen con edades

**Ejemplo:** @jun_yuh · https://www.instagram.com/p/DcV_B4eETq5/ · 9.163 likes · 149 comentarios · 14 slides

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: fotos REALES de archivo a sangre en orden cronológico: foto escolar de niña → familia → adolescente → adulta trabajando → adulta con su producto.
PALETA (usa SOLO estos colores): #FFFFFF = texto con sombra suave · #36302F = dominante cálido de las fotos de archivo
TIPOGRAFÍA:
- edad: Nunito 700, minúsculas, 34 px
- frase: Nunito 700, minúsculas, 1 palabra en itálica, 38 px
- palabra del CTA: Nunito 900, MAYÚSCULAS, 80 px
PORTADA: tu foto escolar de niña a sangre; «9 años» chico como primera línea; la frase-herida con una palabra en itálica, centrada arriba (8-35%).
SLIDES DEL MEDIO: una etapa por slide con su edad; 1-3 bloques cortos arriba, a veces uno junto a la persona (nunca sobre la cara); la frase que muta de sentido etapa a etapa.
CIERRE: el giro con el objeto físico de tu producto en la mano, y la última con «comenta [PALABRA]» gigante + urgencia real.
ELEMENTOS GRÁFICOS: la edad como ancla · el objeto físico del producto como prueba del giro
EVITA: historias o productos que no son tuyos; no inventes fotos de archivo con IA.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Convierte mi historia en un carrusel de 12-14 slides "historia de origen con edades". Mi historia en bruto: [PEGA TU HISTORIA].
1. Encuentra la FRASE MOTIVO: algo que me dijeron o me dije que me marcó (máx. 4 palabras).
2. Estructura:
- Slide 1: "[edad] años." + lo que quería o temía entonces (máx. 12 palabras, termina en "…").
- Slides 2-4: el contexto que creó la frase motivo.
- Slides 5-7: la frase motivo repetida y MUTANDO hasta volverse identidad ("[frase]" → "soy [adjetivo]").
- Slide 8: "[edad]" + el primer intento de salir (que en realidad fue otra forma de esconderme).
- Slide 9-10: el giro: qué hice distinto y cómo la frase empezó a desaparecer.
- Slide 11: hoy, con un dato concreto y verdadero.
- Slide 12: el puente: por qué creé [MI PRODUCTO] "no porque…, sino porque tú también…".
- Slide 13: CTA "comenta [PALABRA] para [qué recibe]".
Minúsculas, máx. 20 palabras por slide, 1 palabra en *itálica* por slide. Para cada slide indica qué foto mía de esa EDAD usar. No inventes hechos: si falta algo, pregúntame.
```

### 2 · Claude Code
```
hazme un carrusel tipo F11 (Historia de origen con edades) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: fotos REALES de archivo a sangre en orden cronológico: foto escolar de niña → familia → adolescente → adulta trabajando → adulta con su producto.
PALETA (usa SOLO estos colores): #FFFFFF = texto con sombra suave · #36302F = dominante cálido de las fotos de archivo
TIPOGRAFÍA:
- edad: Nunito 700, minúsculas, 34 px
- frase: Nunito 700, minúsculas, 1 palabra en itálica, 38 px
- palabra del CTA: Nunito 900, MAYÚSCULAS, 80 px
PORTADA: tu foto escolar de niña a sangre; «9 años» chico como primera línea; la frase-herida con una palabra en itálica, centrada arriba (8-35%).
SLIDES DEL MEDIO: una etapa por slide con su edad; 1-3 bloques cortos arriba, a veces uno junto a la persona (nunca sobre la cara); la frase que muta de sentido etapa a etapa.
CIERRE: el giro con el objeto físico de tu producto en la mano, y la última con «comenta [PALABRA]» gigante + urgencia real.
ELEMENTOS GRÁFICOS: la edad como ancla · el objeto físico del producto como prueba del giro
EVITA: historias o productos que no son tuyos; no inventes fotos de archivo con IA.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 80 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: fotos REALES de archivo a sangre en orden cronológico: foto escolar de niña → familia → adolescente → adulta trabajando → adulta con su producto.
PALETA (usa SOLO estos colores): #FFFFFF = texto con sombra suave · #36302F = dominante cálido de las fotos de archivo
TIPOGRAFÍA:
- edad: estilo Nunito (700), minúsculas, letra de ~3% del alto
- frase: estilo Nunito (700), minúsculas, 1 palabra en itálica, letra de ~3% del alto
- palabra del CTA: estilo Nunito (900), MAYÚSCULAS, letra de ~6% del alto
COMPOSICIÓN DE ESTA SLIDE: tu foto escolar de niña a sangre; «9 años» chico como primera línea; la frase-herida con una palabra en itálica, centrada arriba (8-35%).
ELEMENTOS GRÁFICOS: la edad como ancla · el objeto físico del producto como prueba del giro
EVITA: historias o productos que no son tuyos; no inventes fotos de archivo con IA.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: fotos REALES de archivo a sangre en orden cronológico: foto escolar de niña → familia → adolescente → adulta trabajando → adulta con su producto.
COMPOSICIÓN: tu foto escolar de niña a sangre; «9 años» chico como primera línea; la frase-herida con una palabra en itálica, centrada arriba (8-35%).
ELEMENTOS: la edad como ancla · el objeto físico del producto como prueba del giro
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: lleva tus fotos o capturas reales (fotos REALES de archivo a sangre en orden cronológico: foto escolar de niña → familia → adolescente → adulta trabajando → adulta con su producto.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: una etapa por slide con su edad; 1-3 bloques cortos arriba, a veces uno junto a la persona (nunca sobre la cara); la frase que muta de sentido etapa a etapa.
(Si es la última slide, la composición es: el giro con el objeto físico de tu producto en la mano, y la última con «comenta [PALABRA]» gigante + urgencia real.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: fotos REALES de archivo a sangre en orden cronológico: foto escolar de niña → familia → adolescente → adulta trabajando → adulta con su producto.
PALETA (usa SOLO estos colores): #FFFFFF = texto con sombra suave · #36302F = dominante cálido de las fotos de archivo
TIPOGRAFÍA:
- edad: estilo Nunito (700), minúsculas, letra de ~3% del alto
- frase: estilo Nunito (700), minúsculas, 1 palabra en itálica, letra de ~3% del alto
- palabra del CTA: estilo Nunito (900), MAYÚSCULAS, letra de ~6% del alto
COMPOSICIÓN DE ESTA SLIDE: tu foto escolar de niña a sangre; «9 años» chico como primera línea; la frase-herida con una palabra en itálica, centrada arriba (8-35%).
ELEMENTOS GRÁFICOS: la edad como ancla · el objeto físico del producto como prueba del giro
EVITA: historias o productos que no son tuyos; no inventes fotos de archivo con IA.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: fotos REALES de archivo a sangre en orden cronológico: foto escolar de niña → familia → adolescente → adulta trabajando → adulta con su producto.
COMPOSICIÓN: tu foto escolar de niña a sangre; «9 años» chico como primera línea; la frase-herida con una palabra en itálica, centrada arriba (8-35%).
ELEMENTOS: la edad como ancla · el objeto físico del producto como prueba del giro
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: lleva tus fotos o capturas reales (fotos REALES de archivo a sangre en orden cronológico: foto escolar de niña → familia → adolescente → adulta trabajando → adulta con su producto.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: una etapa por slide con su edad; 1-3 bloques cortos arriba, a veces uno junto a la persona (nunca sobre la cara); la frase que muta de sentido etapa a etapa.
(Si es la última slide, la composición es: el giro con el objeto físico de tu producto en la mano, y la última con «comenta [PALABRA]» gigante + urgencia real.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## F12 · Etiquetas de papel sobre foto

**Ejemplo:** del deck de estilos de FÓRMULA 100K: portada «Tengo 37 años y estas son TODAS las veces que empecé de nuevo», ~9 slides · falta la captura


**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 70 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: tu foto a sangre de espaldas caminando (calle, playa o campo), luz natural suave, sin que se vea la cara; ocupa el 100% del slide.
PALETA (usa SOLO estos colores): #C9A27A = tira kraft · #F4B6C2 = tira rosa · #111111 = letra · #E85C8A = garabatos rosas
TIPOGRAFÍA:
- texto en las tiras: Nunito 800, minúsculas con mayúscula inicial, 56 px
- palabras clave («37», «TODAS»): Nunito 900, MAYÚSCULAS, letra hueca (solo contorno negro de 4 px), 150 px
PORTADA: 6-8 tiras de papel rasgado (bordes irregulares, sombra suave de 6 px) apiladas en el tercio central, cada una girada entre -4° y +4° y desplazada unos 20-40 px a izquierda o derecha; tiras kraft y rosa alternadas; la edad y «TODAS» van en letra hueca gigante sobre tira rosa.
SLIDES DEL MEDIO: una foto tuya de esa etapa a sangre + 3-4 tiras con «[edad]:» en la primera y qué dejaste / qué aprendiste en las siguientes, en el tercio inferior sin tapar la cara.
CIERRE: foto tuya de hoy + 2 tiras con dónde estás + una tira rosa con la pregunta «¿cuántas veces has empezado de nuevo tú?».
ELEMENTOS GRÁFICOS: bordes rasgados irregulares, nunca rectos · 2-3 garabatos rosas mínimos (estrella, rayitas) junto a las palabras clave · sombra suave bajo cada tira para que parezca pegada
EVITA: datos personales inventados; las tiras perfectamente alineadas (el desorden leve es la firma humana).
```

> Cada slide lleva poco texto (máx. ~14 palabras): el modelo lo puede escribir, pero revisa tildes y eñes letra por letra antes de publicar.

### 1 · Guion (cualquier chat)
```
Crea un carrusel "etiquetas de papel" de 9 slides con el gancho: "Tengo [MI EDAD] años y estas son TODAS las veces que [empecé de nuevo / fracasé / cambié de rumbo]".
Slide 1: divide el gancho en 6-8 tiras cortas (1-3 palabras cada una). Marca con [GRANDE] la edad y la palabra TODAS.
Slides 2-8: una vez por slide: "[edad o año]:" + qué dejé + qué aprendí (máx. 14 palabras, repartidas en 3-4 tiras).
Slide 9: dónde estoy hoy + pregunta: "¿cuántas veces has empezado de nuevo tú?"
Para cada slide sugiere una foto mía de esa etapa (de espaldas o sin mirar a cámara si es posible).
Estilo: tiras de papel kraft y rosa rasgadas, levemente giradas, letra redondeada negra.
```

### 2 · Claude Code
```
hazme un carrusel tipo F12 (Etiquetas de papel sobre foto) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 70 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: tu foto a sangre de espaldas caminando (calle, playa o campo), luz natural suave, sin que se vea la cara; ocupa el 100% del slide.
PALETA (usa SOLO estos colores): #C9A27A = tira kraft · #F4B6C2 = tira rosa · #111111 = letra · #E85C8A = garabatos rosas
TIPOGRAFÍA:
- texto en las tiras: Nunito 800, minúsculas con mayúscula inicial, 56 px
- palabras clave («37», «TODAS»): Nunito 900, MAYÚSCULAS, letra hueca (solo contorno negro de 4 px), 150 px
PORTADA: 6-8 tiras de papel rasgado (bordes irregulares, sombra suave de 6 px) apiladas en el tercio central, cada una girada entre -4° y +4° y desplazada unos 20-40 px a izquierda o derecha; tiras kraft y rosa alternadas; la edad y «TODAS» van en letra hueca gigante sobre tira rosa.
SLIDES DEL MEDIO: una foto tuya de esa etapa a sangre + 3-4 tiras con «[edad]:» en la primera y qué dejaste / qué aprendiste en las siguientes, en el tercio inferior sin tapar la cara.
CIERRE: foto tuya de hoy + 2 tiras con dónde estás + una tira rosa con la pregunta «¿cuántas veces has empezado de nuevo tú?».
ELEMENTOS GRÁFICOS: bordes rasgados irregulares, nunca rectos · 2-3 garabatos rosas mínimos (estrella, rayitas) junto a las palabras clave · sombra suave bajo cada tira para que parezca pegada
EVITA: datos personales inventados; las tiras perfectamente alineadas (el desorden leve es la firma humana).

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 70 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: tu foto a sangre de espaldas caminando (calle, playa o campo), luz natural suave, sin que se vea la cara; ocupa el 100% del slide.
PALETA (usa SOLO estos colores): #C9A27A = tira kraft · #F4B6C2 = tira rosa · #111111 = letra · #E85C8A = garabatos rosas
TIPOGRAFÍA:
- texto en las tiras: estilo Nunito (800), minúsculas con mayúscula inicial, letra de ~4% del alto
- palabras clave («37», «TODAS»): estilo Nunito (900), MAYÚSCULAS, letra hueca (solo contorno negro de 4 px), letra de ~11% del alto
COMPOSICIÓN DE ESTA SLIDE: 6-8 tiras de papel rasgado (bordes irregulares, sombra suave de 6 px) apiladas en el tercio central, cada una girada entre -4° y +4° y desplazada unos 20-40 px a izquierda o derecha; tiras kraft y rosa alternadas; la edad y «TODAS» van en letra hueca gigante sobre tira rosa.
ELEMENTOS GRÁFICOS: bordes rasgados irregulares, nunca rectos · 2-3 garabatos rosas mínimos (estrella, rayitas) junto a las palabras clave · sombra suave bajo cada tira para que parezca pegada
EVITA: datos personales inventados; las tiras perfectamente alineadas (el desorden leve es la firma humana).
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: tu foto a sangre de espaldas caminando (calle, playa o campo), luz natural suave, sin que se vea la cara; ocupa el 100% del slide.
COMPOSICIÓN: 6-8 tiras de papel rasgado (bordes irregulares, sombra suave de 6 px) apiladas en el tercio central, cada una girada entre -4° y +4° y desplazada unos 20-40 px a izquierda o derecha; tiras kraft y rosa alternadas; la edad y «TODAS» van en letra hueca gigante sobre tira rosa.
ELEMENTOS: bordes rasgados irregulares, nunca rectos · 2-3 garabatos rosas mínimos (estrella, rayitas) junto a las palabras clave · sombra suave bajo cada tira para que parezca pegada
```
**C · Solo fondo, sin texto**
```
Genera SOLO EL FONDO de un slide de carrusel, imagen vertical 4:5, SIN NINGÚN TEXTO, letra, número ni logo.
Tiras de papel rasgado kraft y rosa, vacías, sin letras, apiladas y levemente giradas sobre una foto de una persona de espaldas caminando por una calle con luz de tarde, estilo collage hecho a mano, fotografía realista.
Deja libre de objetos la zona donde irá el texto: el tercio central (las tiras).
Paleta: #C9A27A = tira kraft · #F4B6C2 = tira rosa · #111111 = letra · #E85C8A = garabatos rosas.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: una foto tuya de esa etapa a sangre + 3-4 tiras con «[edad]:» en la primera y qué dejaste / qué aprendiste en las siguientes, en el tercio inferior sin tapar la cara.
(Si es la última slide, la composición es: foto tuya de hoy + 2 tiras con dónde estás + una tira rosa con la pregunta «¿cuántas veces has empezado de nuevo tú?».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: tu foto a sangre de espaldas caminando (calle, playa o campo), luz natural suave, sin que se vea la cara; ocupa el 100% del slide.
PALETA (usa SOLO estos colores): #C9A27A = tira kraft · #F4B6C2 = tira rosa · #111111 = letra · #E85C8A = garabatos rosas
TIPOGRAFÍA:
- texto en las tiras: estilo Nunito (800), minúsculas con mayúscula inicial, letra de ~4% del alto
- palabras clave («37», «TODAS»): estilo Nunito (900), MAYÚSCULAS, letra hueca (solo contorno negro de 4 px), letra de ~11% del alto
COMPOSICIÓN DE ESTA SLIDE: 6-8 tiras de papel rasgado (bordes irregulares, sombra suave de 6 px) apiladas en el tercio central, cada una girada entre -4° y +4° y desplazada unos 20-40 px a izquierda o derecha; tiras kraft y rosa alternadas; la edad y «TODAS» van en letra hueca gigante sobre tira rosa.
ELEMENTOS GRÁFICOS: bordes rasgados irregulares, nunca rectos · 2-3 garabatos rosas mínimos (estrella, rayitas) junto a las palabras clave · sombra suave bajo cada tira para que parezca pegada
EVITA: datos personales inventados; las tiras perfectamente alineadas (el desorden leve es la firma humana).
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: tu foto a sangre de espaldas caminando (calle, playa o campo), luz natural suave, sin que se vea la cara; ocupa el 100% del slide.
COMPOSICIÓN: 6-8 tiras de papel rasgado (bordes irregulares, sombra suave de 6 px) apiladas en el tercio central, cada una girada entre -4° y +4° y desplazada unos 20-40 px a izquierda o derecha; tiras kraft y rosa alternadas; la edad y «TODAS» van en letra hueca gigante sobre tira rosa.
ELEMENTOS: bordes rasgados irregulares, nunca rectos · 2-3 garabatos rosas mínimos (estrella, rayitas) junto a las palabras clave · sombra suave bajo cada tira para que parezca pegada
```
**C · Solo fondo, sin texto**
```
Crea una imagen vertical 4:5 que sirva de FONDO para un slide. Importante: SIN texto, letras, números, logos ni marcas de agua.
Tiras de papel rasgado kraft y rosa, vacías, sin letras, apiladas y levemente giradas sobre una foto de una persona de espaldas caminando por una calle con luz de tarde, estilo collage hecho a mano, fotografía realista.
Deja vacía la zona de el tercio central (las tiras): ahí pondré el texto después.
Colores: #C9A27A = tira kraft · #F4B6C2 = tira rosa · #111111 = letra · #E85C8A = garabatos rosas.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: una foto tuya de esa etapa a sangre + 3-4 tiras con «[edad]:» en la primera y qué dejaste / qué aprendiste en las siguientes, en el tercio inferior sin tapar la cara.
(Si es la última slide, la composición es: foto tuya de hoy + 2 tiras con dónde estás + una tira rosa con la pregunta «¿cuántas veces has empezado de nuevo tú?».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## F13 · Dibujado sobre tu foto

**Ejemplo:** del deck de estilos de FÓRMULA 100K: portada «New here? Let's get started — a lil about me» · falta la captura


**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 70 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: tu foto en plano medio, centrada, con mucho cielo o pared lisa arriba (al menos el 35% superior libre).
PALETA (usa SOLO estos colores): #FFD60A = trazo y letra amarilla · #FFFFFF = respaldo si el cielo es claro · #111111 = sombra del trazo al 25%
TIPOGRAFÍA:
- texto manuscrito: Caveat 700, minúsculas, 72 px; con sombra negra suave para que se lea sobre la foto
- palabra de bienvenida: Caveat 700, minúsculas, 120 px
PORTADA: «¿Nueva por aquí?» grande en el cielo libre, arriba a la izquierda; contorno amarillo dibujado a mano (trazo de 8 px, irregular, sin cerrar del todo) alrededor de tu silueta; 2-3 datos cortos con flecha curva que apunta a una parte tuya; flecha «→» arriba a la derecha invitando a deslizar.
SLIDES DEL MEDIO: otra foto tuya; UN dato por slide escrito en el espacio libre y conectado con flecha o círculo a algo concreto de la foto (el café, la laptop, tu mano).
CIERRE: foto tuya mirando a cámara; «si te quedas, esto vas a encontrar:» + 3 temas con flechitas + «sígueme» subrayado dos veces.
ELEMENTOS GRÁFICOS: contorno de silueta dibujado a mano · flechas curvas con punta abierta · círculos imperfectos alrededor de objetos · subrayados dobles
EVITA: texto en inglés y datos personales de terceros; nunca pongas texto encima de la cara.
```

> Cada slide lleva poco texto (máx. ~15 palabras): el modelo lo puede escribir, pero revisa tildes y eñes letra por letra antes de publicar.

### 1 · Guion (cualquier chat)
```
Crea un carrusel de 6 slides "dibujado sobre mi foto" para mi post fijado de bienvenida.
Slide 1: "¿Nueva por aquí?" + "Empecemos" + 3 datos míos cortos con flecha hacia mí (ej. "mamá de 2 →").
Slides 2-5: un dato por slide sobre quién soy, qué hago, a quién ayudo y un resultado real; cada texto debe SEÑALAR algo de la foto (una flecha al café, un círculo a la laptop).
Slide 6: "Si te quedas, esto vas a encontrar:" + 3 temas + "sígueme".
Máx. 15 palabras por slide, letra manuscrita amarilla, contorno dibujado alrededor de mi silueta.
Para cada slide dime qué foto mía necesito y DÓNDE tiene que haber espacio libre (arriba, izquierda…).
```

### 2 · Claude Code
```
hazme un carrusel tipo F13 (Dibujado sobre tu foto) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 70 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: tu foto en plano medio, centrada, con mucho cielo o pared lisa arriba (al menos el 35% superior libre).
PALETA (usa SOLO estos colores): #FFD60A = trazo y letra amarilla · #FFFFFF = respaldo si el cielo es claro · #111111 = sombra del trazo al 25%
TIPOGRAFÍA:
- texto manuscrito: Caveat 700, minúsculas, 72 px; con sombra negra suave para que se lea sobre la foto
- palabra de bienvenida: Caveat 700, minúsculas, 120 px
PORTADA: «¿Nueva por aquí?» grande en el cielo libre, arriba a la izquierda; contorno amarillo dibujado a mano (trazo de 8 px, irregular, sin cerrar del todo) alrededor de tu silueta; 2-3 datos cortos con flecha curva que apunta a una parte tuya; flecha «→» arriba a la derecha invitando a deslizar.
SLIDES DEL MEDIO: otra foto tuya; UN dato por slide escrito en el espacio libre y conectado con flecha o círculo a algo concreto de la foto (el café, la laptop, tu mano).
CIERRE: foto tuya mirando a cámara; «si te quedas, esto vas a encontrar:» + 3 temas con flechitas + «sígueme» subrayado dos veces.
ELEMENTOS GRÁFICOS: contorno de silueta dibujado a mano · flechas curvas con punta abierta · círculos imperfectos alrededor de objetos · subrayados dobles
EVITA: texto en inglés y datos personales de terceros; nunca pongas texto encima de la cara.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 70 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: tu foto en plano medio, centrada, con mucho cielo o pared lisa arriba (al menos el 35% superior libre).
PALETA (usa SOLO estos colores): #FFD60A = trazo y letra amarilla · #FFFFFF = respaldo si el cielo es claro · #111111 = sombra del trazo al 25%
TIPOGRAFÍA:
- texto manuscrito: estilo Caveat (700), minúsculas, letra de ~5% del alto; con sombra negra suave para que se lea sobre la foto
- palabra de bienvenida: estilo Caveat (700), minúsculas, letra de ~9% del alto
COMPOSICIÓN DE ESTA SLIDE: «¿Nueva por aquí?» grande en el cielo libre, arriba a la izquierda; contorno amarillo dibujado a mano (trazo de 8 px, irregular, sin cerrar del todo) alrededor de tu silueta; 2-3 datos cortos con flecha curva que apunta a una parte tuya; flecha «→» arriba a la derecha invitando a deslizar.
ELEMENTOS GRÁFICOS: contorno de silueta dibujado a mano · flechas curvas con punta abierta · círculos imperfectos alrededor de objetos · subrayados dobles
EVITA: texto en inglés y datos personales de terceros; nunca pongas texto encima de la cara.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: tu foto en plano medio, centrada, con mucho cielo o pared lisa arriba (al menos el 35% superior libre).
COMPOSICIÓN: «¿Nueva por aquí?» grande en el cielo libre, arriba a la izquierda; contorno amarillo dibujado a mano (trazo de 8 px, irregular, sin cerrar del todo) alrededor de tu silueta; 2-3 datos cortos con flecha curva que apunta a una parte tuya; flecha «→» arriba a la derecha invitando a deslizar.
ELEMENTOS: contorno de silueta dibujado a mano · flechas curvas con punta abierta · círculos imperfectos alrededor de objetos · subrayados dobles
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: lleva tus fotos o capturas reales (tu foto en plano medio, centrada, con mucho cielo o pared lisa arriba (al menos el 35% superior libre).)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: otra foto tuya; UN dato por slide escrito en el espacio libre y conectado con flecha o círculo a algo concreto de la foto (el café, la laptop, tu mano).
(Si es la última slide, la composición es: foto tuya mirando a cámara; «si te quedas, esto vas a encontrar:» + 3 temas con flechitas + «sígueme» subrayado dos veces.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: tu foto en plano medio, centrada, con mucho cielo o pared lisa arriba (al menos el 35% superior libre).
PALETA (usa SOLO estos colores): #FFD60A = trazo y letra amarilla · #FFFFFF = respaldo si el cielo es claro · #111111 = sombra del trazo al 25%
TIPOGRAFÍA:
- texto manuscrito: estilo Caveat (700), minúsculas, letra de ~5% del alto; con sombra negra suave para que se lea sobre la foto
- palabra de bienvenida: estilo Caveat (700), minúsculas, letra de ~9% del alto
COMPOSICIÓN DE ESTA SLIDE: «¿Nueva por aquí?» grande en el cielo libre, arriba a la izquierda; contorno amarillo dibujado a mano (trazo de 8 px, irregular, sin cerrar del todo) alrededor de tu silueta; 2-3 datos cortos con flecha curva que apunta a una parte tuya; flecha «→» arriba a la derecha invitando a deslizar.
ELEMENTOS GRÁFICOS: contorno de silueta dibujado a mano · flechas curvas con punta abierta · círculos imperfectos alrededor de objetos · subrayados dobles
EVITA: texto en inglés y datos personales de terceros; nunca pongas texto encima de la cara.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: tu foto en plano medio, centrada, con mucho cielo o pared lisa arriba (al menos el 35% superior libre).
COMPOSICIÓN: «¿Nueva por aquí?» grande en el cielo libre, arriba a la izquierda; contorno amarillo dibujado a mano (trazo de 8 px, irregular, sin cerrar del todo) alrededor de tu silueta; 2-3 datos cortos con flecha curva que apunta a una parte tuya; flecha «→» arriba a la derecha invitando a deslizar.
ELEMENTOS: contorno de silueta dibujado a mano · flechas curvas con punta abierta · círculos imperfectos alrededor de objetos · subrayados dobles
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: lleva tus fotos o capturas reales (tu foto en plano medio, centrada, con mucho cielo o pared lisa arriba (al menos el 35% superior libre).)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: otra foto tuya; UN dato por slide escrito en el espacio libre y conectado con flecha o círculo a algo concreto de la foto (el café, la laptop, tu mano).
(Si es la última slide, la composición es: foto tuya mirando a cámara; «si te quedas, esto vas a encontrar:» + 3 temas con flechitas + «sígueme» subrayado dos veces.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## F14 · Masterclass escenificada (hot take en rotafolio)

**Ejemplo:** del deck de estilos de FÓRMULA 100K: «Hot take: si hablas de ‘equilibrio vida-trabajo’ a los 22, te estás juntando con la gente equivocada» · falta la captura


**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: set de grabación con fondo de papel continuo morado saturado, luz de estudio suave de frente, boom de micrófono entrando por arriba a la derecha.
PALETA (usa SOLO estos colores): #6B2FD6 = fondo morado · #FFFFFF = hoja del rotafolio · #1A1A1A = marcador negro · #FFE45C = resaltador amarillo
TIPOGRAFÍA:
- «Hot take:» subrayado: Permanent Marker 400, 70 px
- opinión escrita a mano: Kalam 700, 52 px; la frase clave entre comillas con resaltador amarillo detrás
PORTADA: plano general: tú de pie a la izquierda con las manos atrás, rotafolio blanco a la derecha ocupando 45% del ancho; la hoja muestra «Hot take:» subrayado y la opinión en 4-5 líneas.
SLIDES DEL MEDIO: hojas nuevas del rotafolio con cambios de «cámara»: primer plano de la hoja (texto grande), plano medio tuyo señalando, plano cenital de la hoja arrancada.
CIERRE: plano medio tuyo mirando a cámara con la hoja «¿Estás de acuerdo o no?».
ELEMENTOS GRÁFICOS: boom de micrófono visible · hoja con leve curvatura y sombra del rotafolio · resaltador amarillo que se sale un poco de la frase
EVITA: opiniones que no son tuyas; usa tu cara real o tu personaje, nunca una persona inventada que parezca tú.
```

> Cada slide lleva poco texto (máx. ~22 palabras): el modelo lo puede escribir, pero revisa tildes y eñes letra por letra antes de publicar.

### 1 · Guion (cualquier chat)
```
Crea un carrusel de 5 slides "masterclass escenificada" con una opinión polémica sobre [TEMA DE MI NICHO].
Primero dame 3 hot takes candidatos y dime cuál genera más debate sin ser ofensivo.
Slide 1: "Opinión impopular:" + la opinión en máx. 22 palabras, con la frase clave entre comillas para resaltar en amarillo.
Slides 2-4: una hoja nueva del rotafolio por slide: el argumento, la evidencia, la excepción.
Slide 5: "¿Estás de acuerdo o no? Te leo en comentarios."
Prompt de imagen (sin texto en la hoja; el texto se pone después): "[descripción de mí], de pie con las manos atrás junto a un rotafolio blanco en un set de grabación con fondo morado saturado, luz de estudio, boom de micrófono entrando por arriba, foto realista, formato 4:5, hoja del rotafolio EN BLANCO".
```

### 2 · Claude Code
```
hazme un carrusel tipo F14 (Masterclass escenificada (hot take en rotafolio)) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: set de grabación con fondo de papel continuo morado saturado, luz de estudio suave de frente, boom de micrófono entrando por arriba a la derecha.
PALETA (usa SOLO estos colores): #6B2FD6 = fondo morado · #FFFFFF = hoja del rotafolio · #1A1A1A = marcador negro · #FFE45C = resaltador amarillo
TIPOGRAFÍA:
- «Hot take:» subrayado: Permanent Marker 400, 70 px
- opinión escrita a mano: Kalam 700, 52 px; la frase clave entre comillas con resaltador amarillo detrás
PORTADA: plano general: tú de pie a la izquierda con las manos atrás, rotafolio blanco a la derecha ocupando 45% del ancho; la hoja muestra «Hot take:» subrayado y la opinión en 4-5 líneas.
SLIDES DEL MEDIO: hojas nuevas del rotafolio con cambios de «cámara»: primer plano de la hoja (texto grande), plano medio tuyo señalando, plano cenital de la hoja arrancada.
CIERRE: plano medio tuyo mirando a cámara con la hoja «¿Estás de acuerdo o no?».
ELEMENTOS GRÁFICOS: boom de micrófono visible · hoja con leve curvatura y sombra del rotafolio · resaltador amarillo que se sale un poco de la frase
EVITA: opiniones que no son tuyas; usa tu cara real o tu personaje, nunca una persona inventada que parezca tú.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 80 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: set de grabación con fondo de papel continuo morado saturado, luz de estudio suave de frente, boom de micrófono entrando por arriba a la derecha.
PALETA (usa SOLO estos colores): #6B2FD6 = fondo morado · #FFFFFF = hoja del rotafolio · #1A1A1A = marcador negro · #FFE45C = resaltador amarillo
TIPOGRAFÍA:
- «Hot take:» subrayado: estilo Permanent Marker (400), letra de ~5% del alto
- opinión escrita a mano: estilo Kalam (700), letra de ~4% del alto; la frase clave entre comillas con resaltador amarillo detrás
COMPOSICIÓN DE ESTA SLIDE: plano general: tú de pie a la izquierda con las manos atrás, rotafolio blanco a la derecha ocupando 45% del ancho; la hoja muestra «Hot take:» subrayado y la opinión en 4-5 líneas.
ELEMENTOS GRÁFICOS: boom de micrófono visible · hoja con leve curvatura y sombra del rotafolio · resaltador amarillo que se sale un poco de la frase
EVITA: opiniones que no son tuyas; usa tu cara real o tu personaje, nunca una persona inventada que parezca tú.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: set de grabación con fondo de papel continuo morado saturado, luz de estudio suave de frente, boom de micrófono entrando por arriba a la derecha.
COMPOSICIÓN: plano general: tú de pie a la izquierda con las manos atrás, rotafolio blanco a la derecha ocupando 45% del ancho; la hoja muestra «Hot take:» subrayado y la opinión en 4-5 líneas.
ELEMENTOS: boom de micrófono visible · hoja con leve curvatura y sombra del rotafolio · resaltador amarillo que se sale un poco de la frase
```
**C · Solo fondo, sin texto**
```
Genera SOLO EL FONDO de un slide de carrusel, imagen vertical 4:5, SIN NINGÚN TEXTO, letra, número ni logo.
Mujer [DESCRÍBETE] de pie con las manos atrás junto a un rotafolio blanco en un set de grabación con fondo de papel continuo morado saturado, luz de estudio suave, boom de micrófono entrando por arriba, fotografía realista, hoja del rotafolio completamente EN BLANCO.
Deja libre de objetos la zona donde irá el texto: la hoja del rotafolio.
Paleta: #6B2FD6 = fondo morado · #FFFFFF = hoja del rotafolio · #1A1A1A = marcador negro · #FFE45C = resaltador amarillo.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: hojas nuevas del rotafolio con cambios de «cámara»: primer plano de la hoja (texto grande), plano medio tuyo señalando, plano cenital de la hoja arrancada.
(Si es la última slide, la composición es: plano medio tuyo mirando a cámara con la hoja «¿Estás de acuerdo o no?».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: set de grabación con fondo de papel continuo morado saturado, luz de estudio suave de frente, boom de micrófono entrando por arriba a la derecha.
PALETA (usa SOLO estos colores): #6B2FD6 = fondo morado · #FFFFFF = hoja del rotafolio · #1A1A1A = marcador negro · #FFE45C = resaltador amarillo
TIPOGRAFÍA:
- «Hot take:» subrayado: estilo Permanent Marker (400), letra de ~5% del alto
- opinión escrita a mano: estilo Kalam (700), letra de ~4% del alto; la frase clave entre comillas con resaltador amarillo detrás
COMPOSICIÓN DE ESTA SLIDE: plano general: tú de pie a la izquierda con las manos atrás, rotafolio blanco a la derecha ocupando 45% del ancho; la hoja muestra «Hot take:» subrayado y la opinión en 4-5 líneas.
ELEMENTOS GRÁFICOS: boom de micrófono visible · hoja con leve curvatura y sombra del rotafolio · resaltador amarillo que se sale un poco de la frase
EVITA: opiniones que no son tuyas; usa tu cara real o tu personaje, nunca una persona inventada que parezca tú.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: set de grabación con fondo de papel continuo morado saturado, luz de estudio suave de frente, boom de micrófono entrando por arriba a la derecha.
COMPOSICIÓN: plano general: tú de pie a la izquierda con las manos atrás, rotafolio blanco a la derecha ocupando 45% del ancho; la hoja muestra «Hot take:» subrayado y la opinión en 4-5 líneas.
ELEMENTOS: boom de micrófono visible · hoja con leve curvatura y sombra del rotafolio · resaltador amarillo que se sale un poco de la frase
```
**C · Solo fondo, sin texto**
```
Crea una imagen vertical 4:5 que sirva de FONDO para un slide. Importante: SIN texto, letras, números, logos ni marcas de agua.
Mujer [DESCRÍBETE] de pie con las manos atrás junto a un rotafolio blanco en un set de grabación con fondo de papel continuo morado saturado, luz de estudio suave, boom de micrófono entrando por arriba, fotografía realista, hoja del rotafolio completamente EN BLANCO.
Deja vacía la zona de la hoja del rotafolio: ahí pondré el texto después.
Colores: #6B2FD6 = fondo morado · #FFFFFF = hoja del rotafolio · #1A1A1A = marcador negro · #FFE45C = resaltador amarillo.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: hojas nuevas del rotafolio con cambios de «cámara»: primer plano de la hoja (texto grande), plano medio tuyo señalando, plano cenital de la hoja arrancada.
(Si es la última slide, la composición es: plano medio tuyo mirando a cámara con la hoja «¿Estás de acuerdo o no?».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## F15 · Tipografía gigante con degradado

**Ejemplo:** del deck de estilos de FÓRMULA 100K: @marketingharry «WHY GOOD CONTENT GETS IGNORED», 10 slides · falta la captura


**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: blanco puro #FFFFFF en portada; blanco o gris muy claro #F4F4F5 en el resto, sin texturas.
PALETA (usa SOLO estos colores): #FFFFFF = fondo · #0A0A0A = titular · #FF3D7F = inicio del degradado · #FF8A00 = fin del degradado · #71717A = contador y texto chico
TIPOGRAFÍA:
- titular: Archivo Black 400 (ya es black), MAYÚSCULAS, interlineado 0.95, 118 px
- palabra en degradado: Archivo Black 400, MAYÚSCULAS, 118 px; degradado lineal 90° rosa → naranja recortado a la letra
- texto de apoyo: Inter 500, 40 px
PORTADA: titular de 3-5 palabras en el 40% superior, alineado a la izquierda, con UNA palabra en degradado; debajo, centrado, un objeto o rostro recortado sobre blanco que traduce el titular literalmente (ocupa 45% del alto); formas 3D brillantes de color en 2 esquinas; contador «1/10» arriba a la derecha.
SLIDES DEL MEDIO: fondo claro; título de 4-6 palabras en negro ultra bold arriba, 2 líneas de explicación en Inter 40 px, y un dato o ejemplo en un bloque gris claro redondeado; contador «N/10».
CIERRE: resumen en una frase ultra bold con una palabra en degradado + «guárdalo» en gris.
ELEMENTOS GRÁFICOS: formas 3D flotantes (esfera, anillo, píldora) con brillo, cortadas por el borde · recorte fotográfico limpio sin sombra dura · contador N/10
EVITA: imágenes de bebés o personas sin permiso y texto en inglés; el degradado en más de una palabra.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Crea un carrusel de 10 slides "tipográfico con degradado" sobre [PROBLEMA de mi audiencia].
Slide 1: titular de máx. 5 palabras en mayúsculas; marca con [DEGRADADO] la ÚNICA palabra emocional. Propón un objeto o rostro recortado que traduzca el titular literalmente (con humor).
Slides 2-9: una razón por slide: título de 4-6 palabras + 2 líneas de explicación + 1 dato o ejemplo.
Slide 10: resumen en 1 frase + "guárdalo".
Estilo: fondo blanco, tipografía sans ultra bold negra, palabra clave en degradado [COLOR 1] → [COLOR 2], formas 3D flotantes de color en las esquinas, contador "N/10" arriba a la derecha.
Prompt de imagen del recorte: "[objeto/rostro] recortado sobre fondo blanco puro, foto de estudio, alto detalle, sin texto".
```

### 2 · Claude Code
```
hazme un carrusel tipo F15 (Tipografía gigante con degradado) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: blanco puro #FFFFFF en portada; blanco o gris muy claro #F4F4F5 en el resto, sin texturas.
PALETA (usa SOLO estos colores): #FFFFFF = fondo · #0A0A0A = titular · #FF3D7F = inicio del degradado · #FF8A00 = fin del degradado · #71717A = contador y texto chico
TIPOGRAFÍA:
- titular: Archivo Black 400 (ya es black), MAYÚSCULAS, interlineado 0.95, 118 px
- palabra en degradado: Archivo Black 400, MAYÚSCULAS, 118 px; degradado lineal 90° rosa → naranja recortado a la letra
- texto de apoyo: Inter 500, 40 px
PORTADA: titular de 3-5 palabras en el 40% superior, alineado a la izquierda, con UNA palabra en degradado; debajo, centrado, un objeto o rostro recortado sobre blanco que traduce el titular literalmente (ocupa 45% del alto); formas 3D brillantes de color en 2 esquinas; contador «1/10» arriba a la derecha.
SLIDES DEL MEDIO: fondo claro; título de 4-6 palabras en negro ultra bold arriba, 2 líneas de explicación en Inter 40 px, y un dato o ejemplo en un bloque gris claro redondeado; contador «N/10».
CIERRE: resumen en una frase ultra bold con una palabra en degradado + «guárdalo» en gris.
ELEMENTOS GRÁFICOS: formas 3D flotantes (esfera, anillo, píldora) con brillo, cortadas por el borde · recorte fotográfico limpio sin sombra dura · contador N/10
EVITA: imágenes de bebés o personas sin permiso y texto en inglés; el degradado en más de una palabra.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 80 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: blanco puro #FFFFFF en portada; blanco o gris muy claro #F4F4F5 en el resto, sin texturas.
PALETA (usa SOLO estos colores): #FFFFFF = fondo · #0A0A0A = titular · #FF3D7F = inicio del degradado · #FF8A00 = fin del degradado · #71717A = contador y texto chico
TIPOGRAFÍA:
- titular: estilo Archivo Black (400 (ya es black)), MAYÚSCULAS, interlineado 0.95, letra de ~9% del alto
- palabra en degradado: estilo Archivo Black (400), MAYÚSCULAS, letra de ~9% del alto; degradado lineal 90° rosa → naranja recortado a la letra
- texto de apoyo: estilo Inter (500), letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: titular de 3-5 palabras en el 40% superior, alineado a la izquierda, con UNA palabra en degradado; debajo, centrado, un objeto o rostro recortado sobre blanco que traduce el titular literalmente (ocupa 45% del alto); formas 3D brillantes de color en 2 esquinas; contador «1/10» arriba a la derecha.
ELEMENTOS GRÁFICOS: formas 3D flotantes (esfera, anillo, píldora) con brillo, cortadas por el borde · recorte fotográfico limpio sin sombra dura · contador N/10
EVITA: imágenes de bebés o personas sin permiso y texto en inglés; el degradado en más de una palabra.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: blanco puro #FFFFFF en portada; blanco o gris muy claro #F4F4F5 en el resto, sin texturas.
COMPOSICIÓN: titular de 3-5 palabras en el 40% superior, alineado a la izquierda, con UNA palabra en degradado; debajo, centrado, un objeto o rostro recortado sobre blanco que traduce el titular literalmente (ocupa 45% del alto); formas 3D brillantes de color en 2 esquinas; contador «1/10» arriba a la derecha.
ELEMENTOS: formas 3D flotantes (esfera, anillo, píldora) con brillo, cortadas por el borde · recorte fotográfico limpio sin sombra dura · contador N/10
```
**C · Solo fondo, sin texto**
```
Genera SOLO EL FONDO de un slide de carrusel, imagen vertical 4:5, SIN NINGÚN TEXTO, letra, número ni logo.
Objeto [QUE TRADUCE TU TITULAR] recortado sobre fondo blanco puro, foto de estudio de alto detalle, con 2 formas 3D brillantes rosa y naranja flotando en las esquinas, sin texto.
Deja libre de objetos la zona donde irá el texto: el 40% superior.
Paleta: #FFFFFF = fondo · #0A0A0A = titular · #FF3D7F = inicio del degradado · #FF8A00 = fin del degradado · #71717A = contador y texto chico.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: fondo claro; título de 4-6 palabras en negro ultra bold arriba, 2 líneas de explicación en Inter 40 px, y un dato o ejemplo en un bloque gris claro redondeado; contador «N/10».
(Si es la última slide, la composición es: resumen en una frase ultra bold con una palabra en degradado + «guárdalo» en gris.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: blanco puro #FFFFFF en portada; blanco o gris muy claro #F4F4F5 en el resto, sin texturas.
PALETA (usa SOLO estos colores): #FFFFFF = fondo · #0A0A0A = titular · #FF3D7F = inicio del degradado · #FF8A00 = fin del degradado · #71717A = contador y texto chico
TIPOGRAFÍA:
- titular: estilo Archivo Black (400 (ya es black)), MAYÚSCULAS, interlineado 0.95, letra de ~9% del alto
- palabra en degradado: estilo Archivo Black (400), MAYÚSCULAS, letra de ~9% del alto; degradado lineal 90° rosa → naranja recortado a la letra
- texto de apoyo: estilo Inter (500), letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: titular de 3-5 palabras en el 40% superior, alineado a la izquierda, con UNA palabra en degradado; debajo, centrado, un objeto o rostro recortado sobre blanco que traduce el titular literalmente (ocupa 45% del alto); formas 3D brillantes de color en 2 esquinas; contador «1/10» arriba a la derecha.
ELEMENTOS GRÁFICOS: formas 3D flotantes (esfera, anillo, píldora) con brillo, cortadas por el borde · recorte fotográfico limpio sin sombra dura · contador N/10
EVITA: imágenes de bebés o personas sin permiso y texto en inglés; el degradado en más de una palabra.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: blanco puro #FFFFFF en portada; blanco o gris muy claro #F4F4F5 en el resto, sin texturas.
COMPOSICIÓN: titular de 3-5 palabras en el 40% superior, alineado a la izquierda, con UNA palabra en degradado; debajo, centrado, un objeto o rostro recortado sobre blanco que traduce el titular literalmente (ocupa 45% del alto); formas 3D brillantes de color en 2 esquinas; contador «1/10» arriba a la derecha.
ELEMENTOS: formas 3D flotantes (esfera, anillo, píldora) con brillo, cortadas por el borde · recorte fotográfico limpio sin sombra dura · contador N/10
```
**C · Solo fondo, sin texto**
```
Crea una imagen vertical 4:5 que sirva de FONDO para un slide. Importante: SIN texto, letras, números, logos ni marcas de agua.
Objeto [QUE TRADUCE TU TITULAR] recortado sobre fondo blanco puro, foto de estudio de alto detalle, con 2 formas 3D brillantes rosa y naranja flotando en las esquinas, sin texto.
Deja vacía la zona de el 40% superior: ahí pondré el texto después.
Colores: #FFFFFF = fondo · #0A0A0A = titular · #FF3D7F = inicio del degradado · #FF8A00 = fin del degradado · #71717A = contador y texto chico.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: fondo claro; título de 4-6 palabras en negro ultra bold arriba, 2 líneas de explicación en Inter 40 px, y un dato o ejemplo en un bloque gris claro redondeado; contador «N/10».
(Si es la última slide, la composición es: resumen en una frase ultra bold con una palabra en degradado + «guárdalo» en gris.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## F16 · Ilustrado kawaii

**Ejemplo:** del deck de estilos de FÓRMULA 100K: «Clínica Somno — Aprende a descansar en tus días libres» · falta la captura


**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: blanco #FFFFFF con 3-4 detalles mínimos (estrellitas, nubecitas) en azul claro.
PALETA (usa SOLO estos colores): #FFFFFF = fondo · #1E2A5A = titular azul oscuro · #6E8FD8 = subtítulo azul claro · #FFD66B = amarillo del personaje y resaltados · #EEF3FF = recuadro de información
TIPOGRAFÍA:
- titular: Nunito 900, 84 px
- subtítulo con palabras resaltadas: Nunito 700, 46 px
- texto del recuadro: Nunito 600, 38 px
PORTADA: titular en 2 niveles arriba (azul oscuro + subtítulo azul claro); personaje kawaii centrado ocupando 50% del alto, exagerando la emoción del problema (ojos en espiral, gato colgando de la cabeza); logo pequeño abajo.
SLIDES DEL MEDIO: título en forma de pregunta arriba; escena del personaje haciendo el consejo en el centro (40% del alto); recuadro de esquinas redondeadas (radio 32 px, fondo #EEF3FF) abajo con máx. 25 palabras.
CIERRE: personaje feliz y descansado + CTA al servicio en un botón redondeado amarillo.
ELEMENTOS GRÁFICOS: personaje idéntico en todas las slides (misma ropa, pelo y rasgo) · trazo limpio de grosor uniforme · recuadro redondeado que separa dibujo de dato
EVITA: personajes o marcas ajenas: crea tu propio personaje con una hoja de personaje primero.
```

> Cada slide lleva poco texto (máx. ~25 palabras): el modelo lo puede escribir, pero revisa tildes y eñes letra por letra antes de publicar.

### 1 · Guion (cualquier chat)
```
Crea un carrusel ilustrado kawaii de 7 slides para [NEGOCIO] sobre [PROBLEMA COTIDIANO de su cliente].
Primero define UN personaje: aspecto, ropa, color de pelo, 1 rasgo distintivo (lo repetimos igual en todas).
Slide 1: titular educativo en 2 niveles (bold oscuro + subtítulo claro) + escena del personaje sintiendo el problema de forma exagerada y tierna.
Slides 2-6: 1 consejo por slide: título de pregunta ("¿Cómo volver a dormir?") + escena del personaje haciendo el consejo + recuadro redondeado con máx. 25 palabras.
Slide 7: cierre con el personaje feliz + CTA a [SERVICIO].
Prompt de ilustración por slide: "ilustración kawaii de [personaje], trazo limpio, colores pastel azul y amarillo, fondo blanco, sin texto".
```

### 2 · Claude Code
```
hazme un carrusel tipo F16 (Ilustrado kawaii) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: blanco #FFFFFF con 3-4 detalles mínimos (estrellitas, nubecitas) en azul claro.
PALETA (usa SOLO estos colores): #FFFFFF = fondo · #1E2A5A = titular azul oscuro · #6E8FD8 = subtítulo azul claro · #FFD66B = amarillo del personaje y resaltados · #EEF3FF = recuadro de información
TIPOGRAFÍA:
- titular: Nunito 900, 84 px
- subtítulo con palabras resaltadas: Nunito 700, 46 px
- texto del recuadro: Nunito 600, 38 px
PORTADA: titular en 2 niveles arriba (azul oscuro + subtítulo azul claro); personaje kawaii centrado ocupando 50% del alto, exagerando la emoción del problema (ojos en espiral, gato colgando de la cabeza); logo pequeño abajo.
SLIDES DEL MEDIO: título en forma de pregunta arriba; escena del personaje haciendo el consejo en el centro (40% del alto); recuadro de esquinas redondeadas (radio 32 px, fondo #EEF3FF) abajo con máx. 25 palabras.
CIERRE: personaje feliz y descansado + CTA al servicio en un botón redondeado amarillo.
ELEMENTOS GRÁFICOS: personaje idéntico en todas las slides (misma ropa, pelo y rasgo) · trazo limpio de grosor uniforme · recuadro redondeado que separa dibujo de dato
EVITA: personajes o marcas ajenas: crea tu propio personaje con una hoja de personaje primero.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 80 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: blanco #FFFFFF con 3-4 detalles mínimos (estrellitas, nubecitas) en azul claro.
PALETA (usa SOLO estos colores): #FFFFFF = fondo · #1E2A5A = titular azul oscuro · #6E8FD8 = subtítulo azul claro · #FFD66B = amarillo del personaje y resaltados · #EEF3FF = recuadro de información
TIPOGRAFÍA:
- titular: estilo Nunito (900), letra de ~6% del alto
- subtítulo con palabras resaltadas: estilo Nunito (700), letra de ~3% del alto
- texto del recuadro: estilo Nunito (600), letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: titular en 2 niveles arriba (azul oscuro + subtítulo azul claro); personaje kawaii centrado ocupando 50% del alto, exagerando la emoción del problema (ojos en espiral, gato colgando de la cabeza); logo pequeño abajo.
ELEMENTOS GRÁFICOS: personaje idéntico en todas las slides (misma ropa, pelo y rasgo) · trazo limpio de grosor uniforme · recuadro redondeado que separa dibujo de dato
EVITA: personajes o marcas ajenas: crea tu propio personaje con una hoja de personaje primero.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: blanco #FFFFFF con 3-4 detalles mínimos (estrellitas, nubecitas) en azul claro.
COMPOSICIÓN: titular en 2 niveles arriba (azul oscuro + subtítulo azul claro); personaje kawaii centrado ocupando 50% del alto, exagerando la emoción del problema (ojos en espiral, gato colgando de la cabeza); logo pequeño abajo.
ELEMENTOS: personaje idéntico en todas las slides (misma ropa, pelo y rasgo) · trazo limpio de grosor uniforme · recuadro redondeado que separa dibujo de dato
```
**C · Solo fondo, sin texto**
```
Genera SOLO EL FONDO de un slide de carrusel, imagen vertical 4:5, SIN NINGÚN TEXTO, letra, número ni logo.
Ilustración kawaii de [TU PERSONAJE: aspecto, ropa, pelo, rasgo], trazo limpio de grosor uniforme, colores pastel azul y amarillo, fondo blanco con dos estrellitas, sin texto, [ESCENA DEL CONSEJO].
Deja libre de objetos la zona donde irá el texto: el cuarto superior (titular) y el cuarto inferior (recuadro).
Paleta: #FFFFFF = fondo · #1E2A5A = titular azul oscuro · #6E8FD8 = subtítulo azul claro · #FFD66B = amarillo del personaje y resaltados · #EEF3FF = recuadro de información.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: título en forma de pregunta arriba; escena del personaje haciendo el consejo en el centro (40% del alto); recuadro de esquinas redondeadas (radio 32 px, fondo #EEF3FF) abajo con máx. 25 palabras.
(Si es la última slide, la composición es: personaje feliz y descansado + CTA al servicio en un botón redondeado amarillo.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: blanco #FFFFFF con 3-4 detalles mínimos (estrellitas, nubecitas) en azul claro.
PALETA (usa SOLO estos colores): #FFFFFF = fondo · #1E2A5A = titular azul oscuro · #6E8FD8 = subtítulo azul claro · #FFD66B = amarillo del personaje y resaltados · #EEF3FF = recuadro de información
TIPOGRAFÍA:
- titular: estilo Nunito (900), letra de ~6% del alto
- subtítulo con palabras resaltadas: estilo Nunito (700), letra de ~3% del alto
- texto del recuadro: estilo Nunito (600), letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: titular en 2 niveles arriba (azul oscuro + subtítulo azul claro); personaje kawaii centrado ocupando 50% del alto, exagerando la emoción del problema (ojos en espiral, gato colgando de la cabeza); logo pequeño abajo.
ELEMENTOS GRÁFICOS: personaje idéntico en todas las slides (misma ropa, pelo y rasgo) · trazo limpio de grosor uniforme · recuadro redondeado que separa dibujo de dato
EVITA: personajes o marcas ajenas: crea tu propio personaje con una hoja de personaje primero.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: blanco #FFFFFF con 3-4 detalles mínimos (estrellitas, nubecitas) en azul claro.
COMPOSICIÓN: titular en 2 niveles arriba (azul oscuro + subtítulo azul claro); personaje kawaii centrado ocupando 50% del alto, exagerando la emoción del problema (ojos en espiral, gato colgando de la cabeza); logo pequeño abajo.
ELEMENTOS: personaje idéntico en todas las slides (misma ropa, pelo y rasgo) · trazo limpio de grosor uniforme · recuadro redondeado que separa dibujo de dato
```
**C · Solo fondo, sin texto**
```
Crea una imagen vertical 4:5 que sirva de FONDO para un slide. Importante: SIN texto, letras, números, logos ni marcas de agua.
Ilustración kawaii de [TU PERSONAJE: aspecto, ropa, pelo, rasgo], trazo limpio de grosor uniforme, colores pastel azul y amarillo, fondo blanco con dos estrellitas, sin texto, [ESCENA DEL CONSEJO].
Deja vacía la zona de el cuarto superior (titular) y el cuarto inferior (recuadro): ahí pondré el texto después.
Colores: #FFFFFF = fondo · #1E2A5A = titular azul oscuro · #6E8FD8 = subtítulo azul claro · #FFD66B = amarillo del personaje y resaltados · #EEF3FF = recuadro de información.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: título en forma de pregunta arriba; escena del personaje haciendo el consejo en el centro (40% del alto); recuadro de esquinas redondeadas (radio 32 px, fondo #EEF3FF) abajo con máx. 25 palabras.
(Si es la última slide, la composición es: personaje feliz y descansado + CTA al servicio en un botón redondeado amarillo.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## F17 · Tier list

**Ejemplo:** @lucureau · https://www.instagram.com/p/DbMiGmbgOhX/ · 2.220 likes · 62 comentarios · 1 slide

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 40 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: gris muy claro #F3F3F3 liso.
PALETA (usa SOLO estos colores): #F3F3F3 = fondo · #E63637 = fila S · #F47D2A = fila A · #FAC430 = fila B · #73BB4F = fila C · #000000 = titular
TIPOGRAFÍA:
- titular: Inter 900, 68 px
- etiqueta de opinión: Inter 700, 26 px
- nombre de miniatura: Inter 500, 18 px
PORTADA: UNA slide: titular de 2 líneas centrado arriba (3-17%) con línea negra debajo; 4 filas iguales (~19% del alto): columna izquierda de color a sangre (23% del ancho) con la letra en cuadradito negro + etiqueta de OPINIÓN en 2-4 líneas (blanca en S/A/C, negra en B); a la derecha 3 miniaturas redondeadas con punto de su color y nombre debajo.
SLIDES DEL MEDIO: si haces versión carrusel: una fila por slide con el porqué.
CIERRE: «¿qué moverías tú?».
ELEMENTOS GRÁFICOS: líneas finas entre filas · punto de color del nivel en cada miniatura · firma centrada al pie entre líneas
EVITA: miniaturas con capturas de otras cuentas: usa capturas propias o íconos. Decide si mantienes S = rojo.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Hazme una tier list de [8-12 opciones de mi nicho: herramientas, formatos, estrategias].
Filas: S (etiqueta con opinión fuerte), A, B, C (etiqueta que provoque: "ni debería ser opción").
Pon al menos UNA opción popular en C y explica por qué en 1 línea (ahí está el debate).
Para cada opción: nombre de máx. 3 palabras + qué miniatura usar.
Si hago versión carrusel: slide 1 la tabla completa; slides 2-5 una fila por slide con el porqué de cada posición; slide 6 "¿qué moverías tú? coméntalo".
Caption: termina con una pregunta que pida su propia tier list.
```

### 2 · Claude Code
```
hazme un carrusel tipo F17 (Tier list) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 40 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: gris muy claro #F3F3F3 liso.
PALETA (usa SOLO estos colores): #F3F3F3 = fondo · #E63637 = fila S · #F47D2A = fila A · #FAC430 = fila B · #73BB4F = fila C · #000000 = titular
TIPOGRAFÍA:
- titular: Inter 900, 68 px
- etiqueta de opinión: Inter 700, 26 px
- nombre de miniatura: Inter 500, 18 px
PORTADA: UNA slide: titular de 2 líneas centrado arriba (3-17%) con línea negra debajo; 4 filas iguales (~19% del alto): columna izquierda de color a sangre (23% del ancho) con la letra en cuadradito negro + etiqueta de OPINIÓN en 2-4 líneas (blanca en S/A/C, negra en B); a la derecha 3 miniaturas redondeadas con punto de su color y nombre debajo.
SLIDES DEL MEDIO: si haces versión carrusel: una fila por slide con el porqué.
CIERRE: «¿qué moverías tú?».
ELEMENTOS GRÁFICOS: líneas finas entre filas · punto de color del nivel en cada miniatura · firma centrada al pie entre líneas
EVITA: miniaturas con capturas de otras cuentas: usa capturas propias o íconos. Decide si mantienes S = rojo.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 40 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~4% a los lados y nada importante en el 9% de abajo.
FONDO: gris muy claro #F3F3F3 liso.
PALETA (usa SOLO estos colores): #F3F3F3 = fondo · #E63637 = fila S · #F47D2A = fila A · #FAC430 = fila B · #73BB4F = fila C · #000000 = titular
TIPOGRAFÍA:
- titular: estilo Inter (900), letra de ~5% del alto
- etiqueta de opinión: estilo Inter (700), letra de ~2% del alto
- nombre de miniatura: estilo Inter (500), letra de ~1% del alto
COMPOSICIÓN DE ESTA SLIDE: UNA slide: titular de 2 líneas centrado arriba (3-17%) con línea negra debajo; 4 filas iguales (~19% del alto): columna izquierda de color a sangre (23% del ancho) con la letra en cuadradito negro + etiqueta de OPINIÓN en 2-4 líneas (blanca en S/A/C, negra en B); a la derecha 3 miniaturas redondeadas con punto de su color y nombre debajo.
ELEMENTOS GRÁFICOS: líneas finas entre filas · punto de color del nivel en cada miniatura · firma centrada al pie entre líneas
EVITA: miniaturas con capturas de otras cuentas: usa capturas propias o íconos. Decide si mantienes S = rojo.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: gris muy claro #F3F3F3 liso.
COMPOSICIÓN: UNA slide: titular de 2 líneas centrado arriba (3-17%) con línea negra debajo; 4 filas iguales (~19% del alto): columna izquierda de color a sangre (23% del ancho) con la letra en cuadradito negro + etiqueta de OPINIÓN en 2-4 líneas (blanca en S/A/C, negra en B); a la derecha 3 miniaturas redondeadas con punto de su color y nombre debajo.
ELEMENTOS: líneas finas entre filas · punto de color del nivel en cada miniatura · firma centrada al pie entre líneas
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (gris muy claro #F3F3F3 liso.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: si haces versión carrusel: una fila por slide con el porqué.
(Si es la última slide, la composición es: «¿qué moverías tú?».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~4% a los lados y nada importante en el 9% de abajo.
FONDO: gris muy claro #F3F3F3 liso.
PALETA (usa SOLO estos colores): #F3F3F3 = fondo · #E63637 = fila S · #F47D2A = fila A · #FAC430 = fila B · #73BB4F = fila C · #000000 = titular
TIPOGRAFÍA:
- titular: estilo Inter (900), letra de ~5% del alto
- etiqueta de opinión: estilo Inter (700), letra de ~2% del alto
- nombre de miniatura: estilo Inter (500), letra de ~1% del alto
COMPOSICIÓN DE ESTA SLIDE: UNA slide: titular de 2 líneas centrado arriba (3-17%) con línea negra debajo; 4 filas iguales (~19% del alto): columna izquierda de color a sangre (23% del ancho) con la letra en cuadradito negro + etiqueta de OPINIÓN en 2-4 líneas (blanca en S/A/C, negra en B); a la derecha 3 miniaturas redondeadas con punto de su color y nombre debajo.
ELEMENTOS GRÁFICOS: líneas finas entre filas · punto de color del nivel en cada miniatura · firma centrada al pie entre líneas
EVITA: miniaturas con capturas de otras cuentas: usa capturas propias o íconos. Decide si mantienes S = rojo.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: gris muy claro #F3F3F3 liso.
COMPOSICIÓN: UNA slide: titular de 2 líneas centrado arriba (3-17%) con línea negra debajo; 4 filas iguales (~19% del alto): columna izquierda de color a sangre (23% del ancho) con la letra en cuadradito negro + etiqueta de OPINIÓN en 2-4 líneas (blanca en S/A/C, negra en B); a la derecha 3 miniaturas redondeadas con punto de su color y nombre debajo.
ELEMENTOS: líneas finas entre filas · punto de color del nivel en cada miniatura · firma centrada al pie entre líneas
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (gris muy claro #F3F3F3 liso.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: si haces versión carrusel: una fila por slide con el porqué.
(Si es la última slide, la composición es: «¿qué moverías tú?».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## F18 · Comparación visual con cifras

**Ejemplo:** @estaciondemusculacion · https://www.instagram.com/p/DbeQ2lwkTkq/ · 194.210 likes · 819 comentarios · 5 slides

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 50 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: negro #000000 a sangre.
PALETA (usa SOLO estos colores): #000000 = fondo · #F1E3CD = titular crema · #C8552A = subtítulo y cifras naranja quemado · #FFFFFF = nombres y nota
TIPOGRAFÍA:
- titular: DM Serif Display 400, MAYÚSCULAS, 94 px
- subtítulo y nombres: Oswald 600, MAYÚSCULAS, 30 px
- cifra: Oswald 700, 54 px; unidad más chica
PORTADA: titular serif de 2 líneas centrado (8-26%); subtítulo naranja que rompe una creencia entre dos líneas finas (~28%); nota de unidad chica (~31%); zona de datos (35-97%): 6 columnas de elementos reales apilados de mayor a menor, cifra grande naranja encima y nombre blanco debajo.
SLIDES DEL MEDIO: el mismo molde con otra variable medible y otro subtítulo sorpresa.
CIERRE: negro tipográfico: «SÍGUEME» gigante + para más consejos de [tema] + 1 palabra en script.
ELEMENTOS GRÁFICOS: la altura de la pila ES el gráfico · dos líneas finas enmarcan el subtítulo · luz lateral dramática en los objetos
EVITA: cifras sin fuente y un cierre genérico.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Crea un carrusel de 5 slides "comparación visual con cifras" sobre [VARIABLE MEDIBLE de mi nicho: precio, tiempo, calorías, alcance, comisiones].
Slides 1-4, mismo molde:
- TITULAR: "CAMPEONES DE [X]" (o "LOS [N] MÁS [X]").
- SUBTÍTULO que rompa una creencia ("[lo que todos creen] NO ES EL GANADOR").
- NOTA de unidad ("valores aproximados por…").
- 6 elementos de mayor a menor: nombre corto + cifra + unidad.
Slide 5: "SÍGUEME para más [tema]".
Usa SOLO datos verificables y dime la fuente de cada cifra; si no hay fuente fiable, marca [VERIFICAR].
Prompt de imagen por slide (sin texto): "6 columnas de [elementos] apilados verticalmente sobre fondo negro, alturas de mayor a menor de izquierda a derecha, foto de producto de estudio, luz lateral dramática, formato 4:5". Las cifras y títulos se ponen después en HTML.
```

### 2 · Claude Code
```
hazme un carrusel tipo F18 (Comparación visual con cifras) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 50 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: negro #000000 a sangre.
PALETA (usa SOLO estos colores): #000000 = fondo · #F1E3CD = titular crema · #C8552A = subtítulo y cifras naranja quemado · #FFFFFF = nombres y nota
TIPOGRAFÍA:
- titular: DM Serif Display 400, MAYÚSCULAS, 94 px
- subtítulo y nombres: Oswald 600, MAYÚSCULAS, 30 px
- cifra: Oswald 700, 54 px; unidad más chica
PORTADA: titular serif de 2 líneas centrado (8-26%); subtítulo naranja que rompe una creencia entre dos líneas finas (~28%); nota de unidad chica (~31%); zona de datos (35-97%): 6 columnas de elementos reales apilados de mayor a menor, cifra grande naranja encima y nombre blanco debajo.
SLIDES DEL MEDIO: el mismo molde con otra variable medible y otro subtítulo sorpresa.
CIERRE: negro tipográfico: «SÍGUEME» gigante + para más consejos de [tema] + 1 palabra en script.
ELEMENTOS GRÁFICOS: la altura de la pila ES el gráfico · dos líneas finas enmarcan el subtítulo · luz lateral dramática en los objetos
EVITA: cifras sin fuente y un cierre genérico.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 50 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~5% a los lados y nada importante en el 9% de abajo.
FONDO: negro #000000 a sangre.
PALETA (usa SOLO estos colores): #000000 = fondo · #F1E3CD = titular crema · #C8552A = subtítulo y cifras naranja quemado · #FFFFFF = nombres y nota
TIPOGRAFÍA:
- titular: estilo DM Serif Display (400), MAYÚSCULAS, letra de ~7% del alto
- subtítulo y nombres: estilo Oswald (600), MAYÚSCULAS, letra de ~2% del alto
- cifra: estilo Oswald (700), letra de ~4% del alto; unidad más chica
COMPOSICIÓN DE ESTA SLIDE: titular serif de 2 líneas centrado (8-26%); subtítulo naranja que rompe una creencia entre dos líneas finas (~28%); nota de unidad chica (~31%); zona de datos (35-97%): 6 columnas de elementos reales apilados de mayor a menor, cifra grande naranja encima y nombre blanco debajo.
ELEMENTOS GRÁFICOS: la altura de la pila ES el gráfico · dos líneas finas enmarcan el subtítulo · luz lateral dramática en los objetos
EVITA: cifras sin fuente y un cierre genérico.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: negro #000000 a sangre.
COMPOSICIÓN: titular serif de 2 líneas centrado (8-26%); subtítulo naranja que rompe una creencia entre dos líneas finas (~28%); nota de unidad chica (~31%); zona de datos (35-97%): 6 columnas de elementos reales apilados de mayor a menor, cifra grande naranja encima y nombre blanco debajo.
ELEMENTOS: la altura de la pila ES el gráfico · dos líneas finas enmarcan el subtítulo · luz lateral dramática en los objetos
```
**C · Solo fondo, sin texto**
```
Genera SOLO EL FONDO de un slide de carrusel, imagen vertical 4:5, SIN NINGÚN TEXTO, letra, número ni logo.
6 columnas de [ELEMENTOS] reales apilados verticalmente sobre fondo negro puro, alturas de mayor a menor de izquierda a derecha, foto de producto de estudio con luz lateral dramática, sin texto ni números.
Deja libre de objetos la zona donde irá el texto: el 35% superior y encima de cada columna.
Paleta: #000000 = fondo · #F1E3CD = titular crema · #C8552A = subtítulo y cifras naranja quemado · #FFFFFF = nombres y nota.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: el mismo molde con otra variable medible y otro subtítulo sorpresa.
(Si es la última slide, la composición es: negro tipográfico: «SÍGUEME» gigante + para más consejos de [tema] + 1 palabra en script.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~5% a los lados y nada importante en el 9% de abajo.
FONDO: negro #000000 a sangre.
PALETA (usa SOLO estos colores): #000000 = fondo · #F1E3CD = titular crema · #C8552A = subtítulo y cifras naranja quemado · #FFFFFF = nombres y nota
TIPOGRAFÍA:
- titular: estilo DM Serif Display (400), MAYÚSCULAS, letra de ~7% del alto
- subtítulo y nombres: estilo Oswald (600), MAYÚSCULAS, letra de ~2% del alto
- cifra: estilo Oswald (700), letra de ~4% del alto; unidad más chica
COMPOSICIÓN DE ESTA SLIDE: titular serif de 2 líneas centrado (8-26%); subtítulo naranja que rompe una creencia entre dos líneas finas (~28%); nota de unidad chica (~31%); zona de datos (35-97%): 6 columnas de elementos reales apilados de mayor a menor, cifra grande naranja encima y nombre blanco debajo.
ELEMENTOS GRÁFICOS: la altura de la pila ES el gráfico · dos líneas finas enmarcan el subtítulo · luz lateral dramática en los objetos
EVITA: cifras sin fuente y un cierre genérico.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: negro #000000 a sangre.
COMPOSICIÓN: titular serif de 2 líneas centrado (8-26%); subtítulo naranja que rompe una creencia entre dos líneas finas (~28%); nota de unidad chica (~31%); zona de datos (35-97%): 6 columnas de elementos reales apilados de mayor a menor, cifra grande naranja encima y nombre blanco debajo.
ELEMENTOS: la altura de la pila ES el gráfico · dos líneas finas enmarcan el subtítulo · luz lateral dramática en los objetos
```
**C · Solo fondo, sin texto**
```
Crea una imagen vertical 4:5 que sirva de FONDO para un slide. Importante: SIN texto, letras, números, logos ni marcas de agua.
6 columnas de [ELEMENTOS] reales apilados verticalmente sobre fondo negro puro, alturas de mayor a menor de izquierda a derecha, foto de producto de estudio con luz lateral dramática, sin texto ni números.
Deja vacía la zona de el 35% superior y encima de cada columna: ahí pondré el texto después.
Colores: #000000 = fondo · #F1E3CD = titular crema · #C8552A = subtítulo y cifras naranja quemado · #FFFFFF = nombres y nota.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: el mismo molde con otra variable medible y otro subtítulo sorpresa.
(Si es la última slide, la composición es: negro tipográfico: «SÍGUEME» gigante + para más consejos de [tema] + 1 palabra en script.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## F19 · Mapa visual

**Ejemplo:** @delimonada · https://www.instagram.com/p/DPt-2VHDvFW/ · 23.305 likes · 295 comentarios · 1 slide

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 50 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: gris claro liso #E3E3E3.
PALETA (usa SOLO estos colores): #E3E3E3 = fondo · #19181A = tinta y líneas · #7A7A7A = paréntesis honestos
TIPOGRAFÍA:
- palabra central: Jost 500, 120 px
- «Hazme un»: Jost 500, 46 px
- etiquetas de las ramas: Jost 500, 24 px
- paréntesis: Jost 400, 18 px
PORTADA: UNA slide: al centro (43-55%) la frase del cliente con diminutivo («Hazme un» mediano + «Videíto» gigante); 12-14 ramas en líneas negras finas en ángulo recto hacia etiquetas repartidas alrededor (arriba 25-40%, lados 40-65%, abajo 60-80%), 2-5 palabras cada una; 1-3 aclaraciones entre paréntesis en gris.
SLIDES DEL MEDIO: no hay.
CIERRE: tu @ centrado al pie entre dos líneas (~93%).
ELEMENTOS GRÁFICOS: líneas finas en ángulo recto (no curvas) · cero color
EVITA: logos ajenos y la barra de íconos de Instagram pegada encima.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Hazme un mapa visual de 1 slide que muestre todo el trabajo invisible detrás de "[LO QUE MIS CLIENTES CREEN QUE ES FÁCIL, ej. 'hazme un logo rapidito']".
Centro: esa frase tal como la dice el cliente (con el diminutivo si aplica).
12-14 ramas: cada una un paso real del proceso en máx. 4 palabras; en 3 de ellas agrega un paréntesis honesto y con humor.
Ordena las ramas en sentido horario siguiendo el proceso real.
Estilo: fondo gris muy claro, texto negro, líneas finas en ángulo recto, centro en tipografía bold grande, mucho aire.
Caption: 2 líneas + "¿qué me faltó?".
```

### 2 · Claude Code
```
hazme un carrusel tipo F19 (Mapa visual) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 50 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: gris claro liso #E3E3E3.
PALETA (usa SOLO estos colores): #E3E3E3 = fondo · #19181A = tinta y líneas · #7A7A7A = paréntesis honestos
TIPOGRAFÍA:
- palabra central: Jost 500, 120 px
- «Hazme un»: Jost 500, 46 px
- etiquetas de las ramas: Jost 500, 24 px
- paréntesis: Jost 400, 18 px
PORTADA: UNA slide: al centro (43-55%) la frase del cliente con diminutivo («Hazme un» mediano + «Videíto» gigante); 12-14 ramas en líneas negras finas en ángulo recto hacia etiquetas repartidas alrededor (arriba 25-40%, lados 40-65%, abajo 60-80%), 2-5 palabras cada una; 1-3 aclaraciones entre paréntesis en gris.
SLIDES DEL MEDIO: no hay.
CIERRE: tu @ centrado al pie entre dos líneas (~93%).
ELEMENTOS GRÁFICOS: líneas finas en ángulo recto (no curvas) · cero color
EVITA: logos ajenos y la barra de íconos de Instagram pegada encima.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 50 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~5% a los lados y nada importante en el 9% de abajo.
FONDO: gris claro liso #E3E3E3.
PALETA (usa SOLO estos colores): #E3E3E3 = fondo · #19181A = tinta y líneas · #7A7A7A = paréntesis honestos
TIPOGRAFÍA:
- palabra central: estilo Jost (500), letra de ~9% del alto
- «Hazme un»: estilo Jost (500), letra de ~3% del alto
- etiquetas de las ramas: estilo Jost (500), letra de ~2% del alto
- paréntesis: estilo Jost (400), letra de ~1% del alto
COMPOSICIÓN DE ESTA SLIDE: UNA slide: al centro (43-55%) la frase del cliente con diminutivo («Hazme un» mediano + «Videíto» gigante); 12-14 ramas en líneas negras finas en ángulo recto hacia etiquetas repartidas alrededor (arriba 25-40%, lados 40-65%, abajo 60-80%), 2-5 palabras cada una; 1-3 aclaraciones entre paréntesis en gris.
ELEMENTOS GRÁFICOS: líneas finas en ángulo recto (no curvas) · cero color
EVITA: logos ajenos y la barra de íconos de Instagram pegada encima.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: gris claro liso #E3E3E3.
COMPOSICIÓN: UNA slide: al centro (43-55%) la frase del cliente con diminutivo («Hazme un» mediano + «Videíto» gigante); 12-14 ramas en líneas negras finas en ángulo recto hacia etiquetas repartidas alrededor (arriba 25-40%, lados 40-65%, abajo 60-80%), 2-5 palabras cada una; 1-3 aclaraciones entre paréntesis en gris.
ELEMENTOS: líneas finas en ángulo recto (no curvas) · cero color
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (gris claro liso #E3E3E3.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: no hay.
(Si es la última slide, la composición es: tu @ centrado al pie entre dos líneas (~93%).)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~5% a los lados y nada importante en el 9% de abajo.
FONDO: gris claro liso #E3E3E3.
PALETA (usa SOLO estos colores): #E3E3E3 = fondo · #19181A = tinta y líneas · #7A7A7A = paréntesis honestos
TIPOGRAFÍA:
- palabra central: estilo Jost (500), letra de ~9% del alto
- «Hazme un»: estilo Jost (500), letra de ~3% del alto
- etiquetas de las ramas: estilo Jost (500), letra de ~2% del alto
- paréntesis: estilo Jost (400), letra de ~1% del alto
COMPOSICIÓN DE ESTA SLIDE: UNA slide: al centro (43-55%) la frase del cliente con diminutivo («Hazme un» mediano + «Videíto» gigante); 12-14 ramas en líneas negras finas en ángulo recto hacia etiquetas repartidas alrededor (arriba 25-40%, lados 40-65%, abajo 60-80%), 2-5 palabras cada una; 1-3 aclaraciones entre paréntesis en gris.
ELEMENTOS GRÁFICOS: líneas finas en ángulo recto (no curvas) · cero color
EVITA: logos ajenos y la barra de íconos de Instagram pegada encima.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: gris claro liso #E3E3E3.
COMPOSICIÓN: UNA slide: al centro (43-55%) la frase del cliente con diminutivo («Hazme un» mediano + «Videíto» gigante); 12-14 ramas en líneas negras finas en ángulo recto hacia etiquetas repartidas alrededor (arriba 25-40%, lados 40-65%, abajo 60-80%), 2-5 palabras cada una; 1-3 aclaraciones entre paréntesis en gris.
ELEMENTOS: líneas finas en ángulo recto (no curvas) · cero color
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (gris claro liso #E3E3E3.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: no hay.
(Si es la última slide, la composición es: tu @ centrado al pie entre dos líneas (~93%).)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## F20 · Collage de muchas señales

**Ejemplo:** @cvcwellness · https://www.instagram.com/p/DTrVUEsjsTC/ · 27.775 likes · 696 comentarios · 4 slides (no se incluyen capturas: el contenido mezcla afirmaciones de salud peligrosas. Copia solo la forma.)


**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 40 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: slides 1 y 3 negro #000000; slide 2 blanco (el mismo sistema invertido); slide 4 póster crema #FAF1EA.
PALETA (usa SOLO estos colores): #000000 = fondo · #FFFFFF = etiquetas sobre negro · #E02424 = tachón X · #FAF1EA = póster de la oferta · #181007 = tinta café del póster
TIPOGRAFÍA:
- título: Libre Caslon Text 700, 60 px
- subtítulo: Libre Caslon Text 400 itálica, 34 px
- etiquetas de recortes: Libre Caslon Text 400, 24 px
PORTADA: título serif bold centrado arriba (2-8%) + subtítulo itálica (8-12%); 20-30 recortes sin fondo (objetos, figuras, productos) repartidos por todo el lienzo, tamaños muy distintos, algunos superpuestos, cada uno con etiqueta de 2-4 palabras pegada, sin caja; X roja gruesa sobre lo que hay que dejar.
SLIDES DEL MEDIO: otro manifiesto con el mismo sistema (puede invertirse a fondo blanco).
CIERRE: póster claro: marca arriba, titular serif grande con la pregunta de la oferta, 4 viñetas ◆, «comenta [PALABRA]», capturas de testimonios reales a los lados.
ELEMENTOS GRÁFICOS: densidad: menos de 15 recortes parece moodboard · tachones rojos · testimonios en capturas reales
EVITA: afirmaciones de salud sin respaldo, marcas registradas como recortes y testimonios que no son tuyos.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Crea un carrusel "collage de señales" de 4 slides sobre [TRANSFORMACIÓN que ofrezco].
Slides 1-3: cada una con un título tipo manifiesto ("Cómo salir de [problema]", "Tu [plan] para [año]", "La auditoría de [tema]") + subtítulo en itálica.
Para cada una, 20-25 elementos: acción de máx. 4 palabras + qué recorte visual la representa (objeto o figura reconocible). Marca con [TACHAR] lo que hay que dejar de hacer.
Slide 4: oferta en formato póster: pregunta + 4 beneficios con • + "comenta [PALABRA] y te mando info" + dónde van 2 testimonios reales.
Prompt de imagen por recorte: "[objeto] recortado, fondo transparente, estilo collage de revista vintage".
No uses marcas registradas en los recortes ni afirmaciones de salud sin respaldo.
```

### 2 · Claude Code
```
hazme un carrusel tipo F20 (Collage de muchas señales) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 40 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: slides 1 y 3 negro #000000; slide 2 blanco (el mismo sistema invertido); slide 4 póster crema #FAF1EA.
PALETA (usa SOLO estos colores): #000000 = fondo · #FFFFFF = etiquetas sobre negro · #E02424 = tachón X · #FAF1EA = póster de la oferta · #181007 = tinta café del póster
TIPOGRAFÍA:
- título: Libre Caslon Text 700, 60 px
- subtítulo: Libre Caslon Text 400 itálica, 34 px
- etiquetas de recortes: Libre Caslon Text 400, 24 px
PORTADA: título serif bold centrado arriba (2-8%) + subtítulo itálica (8-12%); 20-30 recortes sin fondo (objetos, figuras, productos) repartidos por todo el lienzo, tamaños muy distintos, algunos superpuestos, cada uno con etiqueta de 2-4 palabras pegada, sin caja; X roja gruesa sobre lo que hay que dejar.
SLIDES DEL MEDIO: otro manifiesto con el mismo sistema (puede invertirse a fondo blanco).
CIERRE: póster claro: marca arriba, titular serif grande con la pregunta de la oferta, 4 viñetas ◆, «comenta [PALABRA]», capturas de testimonios reales a los lados.
ELEMENTOS GRÁFICOS: densidad: menos de 15 recortes parece moodboard · tachones rojos · testimonios en capturas reales
EVITA: afirmaciones de salud sin respaldo, marcas registradas como recortes y testimonios que no son tuyos.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 40 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~4% a los lados y nada importante en el 9% de abajo.
FONDO: slides 1 y 3 negro #000000; slide 2 blanco (el mismo sistema invertido); slide 4 póster crema #FAF1EA.
PALETA (usa SOLO estos colores): #000000 = fondo · #FFFFFF = etiquetas sobre negro · #E02424 = tachón X · #FAF1EA = póster de la oferta · #181007 = tinta café del póster
TIPOGRAFÍA:
- título: estilo Libre Caslon Text (700), letra de ~4% del alto
- subtítulo: estilo Libre Caslon Text (400 itálica), letra de ~3% del alto
- etiquetas de recortes: estilo Libre Caslon Text (400), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: título serif bold centrado arriba (2-8%) + subtítulo itálica (8-12%); 20-30 recortes sin fondo (objetos, figuras, productos) repartidos por todo el lienzo, tamaños muy distintos, algunos superpuestos, cada uno con etiqueta de 2-4 palabras pegada, sin caja; X roja gruesa sobre lo que hay que dejar.
ELEMENTOS GRÁFICOS: densidad: menos de 15 recortes parece moodboard · tachones rojos · testimonios en capturas reales
EVITA: afirmaciones de salud sin respaldo, marcas registradas como recortes y testimonios que no son tuyos.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: slides 1 y 3 negro #000000; slide 2 blanco (el mismo sistema invertido); slide 4 póster crema #FAF1EA.
COMPOSICIÓN: título serif bold centrado arriba (2-8%) + subtítulo itálica (8-12%); 20-30 recortes sin fondo (objetos, figuras, productos) repartidos por todo el lienzo, tamaños muy distintos, algunos superpuestos, cada uno con etiqueta de 2-4 palabras pegada, sin caja; X roja gruesa sobre lo que hay que dejar.
ELEMENTOS: densidad: menos de 15 recortes parece moodboard · tachones rojos · testimonios en capturas reales
```
**C · Solo fondo, sin texto**
```
Genera SOLO EL FONDO de un slide de carrusel, imagen vertical 4:5, SIN NINGÚN TEXTO, letra, número ni logo.
[OBJETO] recortado sobre fondo transparente, estilo collage de revista vintage, sin texto.
Deja libre de objetos la zona donde irá el texto: junto a cada recorte.
Paleta: #000000 = fondo · #FFFFFF = etiquetas sobre negro · #E02424 = tachón X · #FAF1EA = póster de la oferta · #181007 = tinta café del póster.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: otro manifiesto con el mismo sistema (puede invertirse a fondo blanco).
(Si es la última slide, la composición es: póster claro: marca arriba, titular serif grande con la pregunta de la oferta, 4 viñetas ◆, «comenta [PALABRA]», capturas de testimonios reales a los lados.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~4% a los lados y nada importante en el 9% de abajo.
FONDO: slides 1 y 3 negro #000000; slide 2 blanco (el mismo sistema invertido); slide 4 póster crema #FAF1EA.
PALETA (usa SOLO estos colores): #000000 = fondo · #FFFFFF = etiquetas sobre negro · #E02424 = tachón X · #FAF1EA = póster de la oferta · #181007 = tinta café del póster
TIPOGRAFÍA:
- título: estilo Libre Caslon Text (700), letra de ~4% del alto
- subtítulo: estilo Libre Caslon Text (400 itálica), letra de ~3% del alto
- etiquetas de recortes: estilo Libre Caslon Text (400), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: título serif bold centrado arriba (2-8%) + subtítulo itálica (8-12%); 20-30 recortes sin fondo (objetos, figuras, productos) repartidos por todo el lienzo, tamaños muy distintos, algunos superpuestos, cada uno con etiqueta de 2-4 palabras pegada, sin caja; X roja gruesa sobre lo que hay que dejar.
ELEMENTOS GRÁFICOS: densidad: menos de 15 recortes parece moodboard · tachones rojos · testimonios en capturas reales
EVITA: afirmaciones de salud sin respaldo, marcas registradas como recortes y testimonios que no son tuyos.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: slides 1 y 3 negro #000000; slide 2 blanco (el mismo sistema invertido); slide 4 póster crema #FAF1EA.
COMPOSICIÓN: título serif bold centrado arriba (2-8%) + subtítulo itálica (8-12%); 20-30 recortes sin fondo (objetos, figuras, productos) repartidos por todo el lienzo, tamaños muy distintos, algunos superpuestos, cada uno con etiqueta de 2-4 palabras pegada, sin caja; X roja gruesa sobre lo que hay que dejar.
ELEMENTOS: densidad: menos de 15 recortes parece moodboard · tachones rojos · testimonios en capturas reales
```
**C · Solo fondo, sin texto**
```
Crea una imagen vertical 4:5 que sirva de FONDO para un slide. Importante: SIN texto, letras, números, logos ni marcas de agua.
[OBJETO] recortado sobre fondo transparente, estilo collage de revista vintage, sin texto.
Deja vacía la zona de junto a cada recorte: ahí pondré el texto después.
Colores: #000000 = fondo · #FFFFFF = etiquetas sobre negro · #E02424 = tachón X · #FAF1EA = póster de la oferta · #181007 = tinta café del póster.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: otro manifiesto con el mismo sistema (puede invertirse a fondo blanco).
(Si es la última slide, la composición es: póster claro: marca arriba, titular serif grande con la pregunta de la oferta, 4 viñetas ◆, «comenta [PALABRA]», capturas de testimonios reales a los lados.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## G01 · Checklist guardable

**Ejemplo:** @savingwithben · https://www.instagram.com/p/DOsxgAViKxq/ · ≈1.780 likes · 5 slides · reemplaza a la del Grimorio (muerta) (la mecánica coincide; la anatomía no: 12 tareas por slide, un checklist por tipo de persona)

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 50 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: foto oscura desenfocada con velo degradado igual en todas (gris claro arriba → casi negro abajo).
PALETA (usa SOLO estos colores): #9B9C9F = velo arriba · #12141A = velo abajo · #FCFCFB = texto · #806B43 = toques cálidos de las ilustraciones
TIPOGRAFÍA:
- titular: Chewy 400, MAYÚSCULAS, 60 px
- tareas: Nunito 600, 22 px
PORTADA: avatar circular + tu @ arriba al centro (3-10%); titular de 2 líneas «CHECKLIST SEMANAL PARA [PERSONA]» (12-28%); grilla de 3 columnas × 3 filas (30-97%): ilustración acuarela chica + tarea con verbo debajo.
SLIDES DEL MEDIO: el MISMO título cambiando solo la persona («…PARA MAMÁS QUE TRABAJAN»); cada slide es un checklist completo para otro tipo de persona.
CIERRE: el checklist general («RESET DEL DOMINGO») + «guárdalo».
ELEMENTOS GRÁFICOS: un ícono por tarea · tareas que empiezan con verbo · en español: 6-9 tareas por slide para que quepan
EVITA: ilustraciones ajenas: usa las tuyas o genera las propias.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Escribe un carrusel checklist de 8 slides para [MI NICHO] sobre lo que hay que revisar ANTES de [TAREA CONCRETA].
Slide 1: "Antes de [tarea]… revisa esto" + el miedo concreto a equivocarse (máx. 12 palabras).
Slide 2: qué pierdes si te saltas la revisión, con una consecuencia real (no "te irá mal").
Slides 3-7: un ítem por slide. Formato: verbo en imperativo + objeto concreto (máx. 8 palabras) + 1 línea de cómo comprobarlo.
Cada ítem debe poder responderse sí/no en 5 segundos.
Slide 8: el error que casi todos cometen + "Guárdalo para tu próxima [tarea]".
Tutea. Entrégalo en tabla slide | texto grande | texto chico.
```

### 2 · Claude Code
```
hazme un carrusel tipo G01 (Checklist guardable) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 50 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: foto oscura desenfocada con velo degradado igual en todas (gris claro arriba → casi negro abajo).
PALETA (usa SOLO estos colores): #9B9C9F = velo arriba · #12141A = velo abajo · #FCFCFB = texto · #806B43 = toques cálidos de las ilustraciones
TIPOGRAFÍA:
- titular: Chewy 400, MAYÚSCULAS, 60 px
- tareas: Nunito 600, 22 px
PORTADA: avatar circular + tu @ arriba al centro (3-10%); titular de 2 líneas «CHECKLIST SEMANAL PARA [PERSONA]» (12-28%); grilla de 3 columnas × 3 filas (30-97%): ilustración acuarela chica + tarea con verbo debajo.
SLIDES DEL MEDIO: el MISMO título cambiando solo la persona («…PARA MAMÁS QUE TRABAJAN»); cada slide es un checklist completo para otro tipo de persona.
CIERRE: el checklist general («RESET DEL DOMINGO») + «guárdalo».
ELEMENTOS GRÁFICOS: un ícono por tarea · tareas que empiezan con verbo · en español: 6-9 tareas por slide para que quepan
EVITA: ilustraciones ajenas: usa las tuyas o genera las propias.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 50 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~5% a los lados y nada importante en el 9% de abajo.
FONDO: foto oscura desenfocada con velo degradado igual en todas (gris claro arriba → casi negro abajo).
PALETA (usa SOLO estos colores): #9B9C9F = velo arriba · #12141A = velo abajo · #FCFCFB = texto · #806B43 = toques cálidos de las ilustraciones
TIPOGRAFÍA:
- titular: estilo Chewy (400), MAYÚSCULAS, letra de ~4% del alto
- tareas: estilo Nunito (600), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: avatar circular + tu @ arriba al centro (3-10%); titular de 2 líneas «CHECKLIST SEMANAL PARA [PERSONA]» (12-28%); grilla de 3 columnas × 3 filas (30-97%): ilustración acuarela chica + tarea con verbo debajo.
ELEMENTOS GRÁFICOS: un ícono por tarea · tareas que empiezan con verbo · en español: 6-9 tareas por slide para que quepan
EVITA: ilustraciones ajenas: usa las tuyas o genera las propias.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: foto oscura desenfocada con velo degradado igual en todas (gris claro arriba → casi negro abajo).
COMPOSICIÓN: avatar circular + tu @ arriba al centro (3-10%); titular de 2 líneas «CHECKLIST SEMANAL PARA [PERSONA]» (12-28%); grilla de 3 columnas × 3 filas (30-97%): ilustración acuarela chica + tarea con verbo debajo.
ELEMENTOS: un ícono por tarea · tareas que empiezan con verbo · en español: 6-9 tareas por slide para que quepan
```
**C · Solo fondo, sin texto**
```
Genera SOLO EL FONDO de un slide de carrusel, imagen vertical 4:5, SIN NINGÚN TEXTO, letra, número ni logo.
Fondo vertical de una foto desenfocada de un escritorio con velo degradado gris claro arriba a casi negro abajo, sin objetos nítidos ni texto.
Deja libre de objetos la zona donde irá el texto: todo.
Paleta: #9B9C9F = velo arriba · #12141A = velo abajo · #FCFCFB = texto · #806B43 = toques cálidos de las ilustraciones.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: el MISMO título cambiando solo la persona («…PARA MAMÁS QUE TRABAJAN»); cada slide es un checklist completo para otro tipo de persona.
(Si es la última slide, la composición es: el checklist general («RESET DEL DOMINGO») + «guárdalo».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~5% a los lados y nada importante en el 9% de abajo.
FONDO: foto oscura desenfocada con velo degradado igual en todas (gris claro arriba → casi negro abajo).
PALETA (usa SOLO estos colores): #9B9C9F = velo arriba · #12141A = velo abajo · #FCFCFB = texto · #806B43 = toques cálidos de las ilustraciones
TIPOGRAFÍA:
- titular: estilo Chewy (400), MAYÚSCULAS, letra de ~4% del alto
- tareas: estilo Nunito (600), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: avatar circular + tu @ arriba al centro (3-10%); titular de 2 líneas «CHECKLIST SEMANAL PARA [PERSONA]» (12-28%); grilla de 3 columnas × 3 filas (30-97%): ilustración acuarela chica + tarea con verbo debajo.
ELEMENTOS GRÁFICOS: un ícono por tarea · tareas que empiezan con verbo · en español: 6-9 tareas por slide para que quepan
EVITA: ilustraciones ajenas: usa las tuyas o genera las propias.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: foto oscura desenfocada con velo degradado igual en todas (gris claro arriba → casi negro abajo).
COMPOSICIÓN: avatar circular + tu @ arriba al centro (3-10%); titular de 2 líneas «CHECKLIST SEMANAL PARA [PERSONA]» (12-28%); grilla de 3 columnas × 3 filas (30-97%): ilustración acuarela chica + tarea con verbo debajo.
ELEMENTOS: un ícono por tarea · tareas que empiezan con verbo · en español: 6-9 tareas por slide para que quepan
```
**C · Solo fondo, sin texto**
```
Crea una imagen vertical 4:5 que sirva de FONDO para un slide. Importante: SIN texto, letras, números, logos ni marcas de agua.
Fondo vertical de una foto desenfocada de un escritorio con velo degradado gris claro arriba a casi negro abajo, sin objetos nítidos ni texto.
Deja vacía la zona de todo: ahí pondré el texto después.
Colores: #9B9C9F = velo arriba · #12141A = velo abajo · #FCFCFB = texto · #806B43 = toques cálidos de las ilustraciones.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: el MISMO título cambiando solo la persona («…PARA MAMÁS QUE TRABAJAN»); cada slide es un checklist completo para otro tipo de persona.
(Si es la última slide, la composición es: el checklist general («RESET DEL DOMINGO») + «guárdalo».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## G02 · Noticia del nicho

**Ejemplo:** @ramiro.cubria · https://www.instagram.com/p/DWkCiIHiYkz/ · 11.586 likes · 12.640 comentarios · 7 slides (la portada original no se muestra: usa la foto de una persona real humillada)

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 70 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: portada: foto editorial a sangre con degradado negro en el tercio inferior; internas: blanco con cuadrícula de puntos gris muy tenue; cierre gris claro.
PALETA (usa SOLO estos colores): #000000 = portada · #F42A2A = píldora URGENTE · #FAED0A = última línea del titular · #FFFFFF = internas · #33BC44 = CTA
TIPOGRAFÍA:
- titular de portada: Inter 700, 66 px
- titular interno: Inter 700, 34 px
- pie: Inter 500 itálica, 26 px
PORTADA: foto que se ve «de noticia» (tuya o del producto, nunca una persona real ridiculizada); píldora roja «ÚLTIMA HORA» (~66% del alto) + titular blanco de 3 líneas con la última en amarillo (70-92%) + «desliza →» chico (~96%).
SLIDES DEL MEDIO: fondo blanco con puntos; handle arriba; titular negro centrado (15-30%); visual al centro (35-80%): esquema de 2 logos unidos, captura de la app o del chat; pie en itálica con 1 frase en rojo; «desliza →» abajo.
CIERRE: gris claro: ícono de chat + pregunta + «comenta [PALABRA] y te mando el PDF» en verde.
ELEMENTOS GRÁFICOS: palabras de marca en su color · «desliza →» en todas · cuadrícula de puntos tenue
EVITA: fotos de personas reales humilladas, el voseo y «es oficial» sin fuente.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Tengo esta noticia de mi nicho: [PEGA EL LINK O EL TEXTO + FECHA].
Escribe un carrusel de 6 slides tipo portada de periódico:
Slide 1: titular de máx. 10 palabras + etiqueta "ÚLTIMA HORA" o la fecha real.
Slides 2-3: qué pasó, en frases de máx. 20 palabras, sin jerga. Cita la fuente.
Slides 4-5: "Qué cambia para ti si eres [mi cliente ideal]": 2 consecuencias prácticas.
Slide 6: mi opinión en 1 frase + "Comenta [PALABRA] si quieres que te explique cómo aplicarlo".
No inventes datos que no estén en la fuente; si falta algo, márcalo [VERIFICAR]. Tutea.
```

### 2 · Claude Code
```
hazme un carrusel tipo G02 (Noticia del nicho) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 70 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: portada: foto editorial a sangre con degradado negro en el tercio inferior; internas: blanco con cuadrícula de puntos gris muy tenue; cierre gris claro.
PALETA (usa SOLO estos colores): #000000 = portada · #F42A2A = píldora URGENTE · #FAED0A = última línea del titular · #FFFFFF = internas · #33BC44 = CTA
TIPOGRAFÍA:
- titular de portada: Inter 700, 66 px
- titular interno: Inter 700, 34 px
- pie: Inter 500 itálica, 26 px
PORTADA: foto que se ve «de noticia» (tuya o del producto, nunca una persona real ridiculizada); píldora roja «ÚLTIMA HORA» (~66% del alto) + titular blanco de 3 líneas con la última en amarillo (70-92%) + «desliza →» chico (~96%).
SLIDES DEL MEDIO: fondo blanco con puntos; handle arriba; titular negro centrado (15-30%); visual al centro (35-80%): esquema de 2 logos unidos, captura de la app o del chat; pie en itálica con 1 frase en rojo; «desliza →» abajo.
CIERRE: gris claro: ícono de chat + pregunta + «comenta [PALABRA] y te mando el PDF» en verde.
ELEMENTOS GRÁFICOS: palabras de marca en su color · «desliza →» en todas · cuadrícula de puntos tenue
EVITA: fotos de personas reales humilladas, el voseo y «es oficial» sin fuente.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 70 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: portada: foto editorial a sangre con degradado negro en el tercio inferior; internas: blanco con cuadrícula de puntos gris muy tenue; cierre gris claro.
PALETA (usa SOLO estos colores): #000000 = portada · #F42A2A = píldora URGENTE · #FAED0A = última línea del titular · #FFFFFF = internas · #33BC44 = CTA
TIPOGRAFÍA:
- titular de portada: estilo Inter (700), letra de ~5% del alto
- titular interno: estilo Inter (700), letra de ~3% del alto
- pie: estilo Inter (500 itálica), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: foto que se ve «de noticia» (tuya o del producto, nunca una persona real ridiculizada); píldora roja «ÚLTIMA HORA» (~66% del alto) + titular blanco de 3 líneas con la última en amarillo (70-92%) + «desliza →» chico (~96%).
ELEMENTOS GRÁFICOS: palabras de marca en su color · «desliza →» en todas · cuadrícula de puntos tenue
EVITA: fotos de personas reales humilladas, el voseo y «es oficial» sin fuente.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: portada: foto editorial a sangre con degradado negro en el tercio inferior; internas: blanco con cuadrícula de puntos gris muy tenue; cierre gris claro.
COMPOSICIÓN: foto que se ve «de noticia» (tuya o del producto, nunca una persona real ridiculizada); píldora roja «ÚLTIMA HORA» (~66% del alto) + titular blanco de 3 líneas con la última en amarillo (70-92%) + «desliza →» chico (~96%).
ELEMENTOS: palabras de marca en su color · «desliza →» en todas · cuadrícula de puntos tenue
```
**C · Solo fondo, sin texto**
```
Genera SOLO EL FONDO de un slide de carrusel, imagen vertical 4:5, SIN NINGÚN TEXTO, letra, número ni logo.
Foto editorial vertical dramática de [OBJETO O ESCENA DE LA NOTICIA], luz de estudio, degradado negro en el tercio inferior, sin personas reconocibles ni texto.
Deja libre de objetos la zona donde irá el texto: el tercio inferior.
Paleta: #000000 = portada · #F42A2A = píldora URGENTE · #FAED0A = última línea del titular · #FFFFFF = internas · #33BC44 = CTA.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: fondo blanco con puntos; handle arriba; titular negro centrado (15-30%); visual al centro (35-80%): esquema de 2 logos unidos, captura de la app o del chat; pie en itálica con 1 frase en rojo; «desliza →» abajo.
(Si es la última slide, la composición es: gris claro: ícono de chat + pregunta + «comenta [PALABRA] y te mando el PDF» en verde.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: portada: foto editorial a sangre con degradado negro en el tercio inferior; internas: blanco con cuadrícula de puntos gris muy tenue; cierre gris claro.
PALETA (usa SOLO estos colores): #000000 = portada · #F42A2A = píldora URGENTE · #FAED0A = última línea del titular · #FFFFFF = internas · #33BC44 = CTA
TIPOGRAFÍA:
- titular de portada: estilo Inter (700), letra de ~5% del alto
- titular interno: estilo Inter (700), letra de ~3% del alto
- pie: estilo Inter (500 itálica), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: foto que se ve «de noticia» (tuya o del producto, nunca una persona real ridiculizada); píldora roja «ÚLTIMA HORA» (~66% del alto) + titular blanco de 3 líneas con la última en amarillo (70-92%) + «desliza →» chico (~96%).
ELEMENTOS GRÁFICOS: palabras de marca en su color · «desliza →» en todas · cuadrícula de puntos tenue
EVITA: fotos de personas reales humilladas, el voseo y «es oficial» sin fuente.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: portada: foto editorial a sangre con degradado negro en el tercio inferior; internas: blanco con cuadrícula de puntos gris muy tenue; cierre gris claro.
COMPOSICIÓN: foto que se ve «de noticia» (tuya o del producto, nunca una persona real ridiculizada); píldora roja «ÚLTIMA HORA» (~66% del alto) + titular blanco de 3 líneas con la última en amarillo (70-92%) + «desliza →» chico (~96%).
ELEMENTOS: palabras de marca en su color · «desliza →» en todas · cuadrícula de puntos tenue
```
**C · Solo fondo, sin texto**
```
Crea una imagen vertical 4:5 que sirva de FONDO para un slide. Importante: SIN texto, letras, números, logos ni marcas de agua.
Foto editorial vertical dramática de [OBJETO O ESCENA DE LA NOTICIA], luz de estudio, degradado negro en el tercio inferior, sin personas reconocibles ni texto.
Deja vacía la zona de el tercio inferior: ahí pondré el texto después.
Colores: #000000 = portada · #F42A2A = píldora URGENTE · #FAED0A = última línea del titular · #FFFFFF = internas · #33BC44 = CTA.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: fondo blanco con puntos; handle arriba; titular negro centrado (15-30%); visual al centro (35-80%): esquema de 2 logos unidos, captura de la app o del chat; pie en itálica con 1 frase en rojo; «desliza →» abajo.
(Si es la última slide, la composición es: gris claro: ícono de chat + pregunta + «comenta [PALABRA] y te mando el PDF» en verde.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## G03 · ¿Qué tipo de X eres?

**Ejemplo:** @rayamarketing_ · https://www.instagram.com/p/DW-KAnFjLtC/ · 2.678 likes · 5 slides

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 60 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: gris cálido liso #F3F3F1 en todas.
PALETA (usa SOLO estos colores): #F3F3F1 = fondo · #000000 = tinta · #AE102E = rojo de marca: cursor, detalles (o tu color de marca)
TIPOGRAFÍA:
- nombre del arquetipo: Instrument Serif 400 itálica, 80 px; tracking apretado
- pregunta y palabra de identidad: Poppins 800, 66 px
- descripción: Poppins 400, 22 px
PORTADA: pregunta al centro (45-60%) con mezcla serif itálica + sans extra bold; objetos 3D recortados en las esquinas (café, audífonos, laptop) + un cursor de tu color apuntando.
SLIDES DEL MEDIO: píldora con borde «Kit de [TIPO]» (~14%); nombre del arquetipo en serif itálica grande (18-24%); collage de 5 objetos recortados numerados «1.–5.» (30-85%) que lo delatan; pie: 2 renglones + frase-firma entre comillas en serif itálica.
CIERRE: «¿Cuál eres tú?» + «escríbelo en los comentarios» + un elemento de marca tuyo.
ELEMENTOS GRÁFICOS: objetos de producto recortados a todo color · numeración 1.–5. en serif · frase-firma entre comillas por tipo
EVITA: logos, mascotas o apps ajenas como protagonistas.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Escribe un carrusel "¿Qué tipo de [ROL DE MI CLIENTE] eres?" de 6 slides.
Slide 1: la pregunta + "desliza y elige".
Slides 2-5: 4 arquetipos. Para cada uno: número + nombre con humor (2-3 palabras) + 1 emoji + 2 frases de descripción + "Te delata:" y una escena concreta y un poco vergonzosa (máx. 15 palabras).
Que ningún tipo sea "el correcto": cada uno tiene una fortaleza y un punto ciego.
Slide 6: "¿Cuál eres? Comenta el número" + "etiqueta a quien es el 3".
Tutea. Tabla slide | texto grande | texto chico.
```

### 2 · Claude Code
```
hazme un carrusel tipo G03 (¿Qué tipo de X eres?) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 60 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: gris cálido liso #F3F3F1 en todas.
PALETA (usa SOLO estos colores): #F3F3F1 = fondo · #000000 = tinta · #AE102E = rojo de marca: cursor, detalles (o tu color de marca)
TIPOGRAFÍA:
- nombre del arquetipo: Instrument Serif 400 itálica, 80 px; tracking apretado
- pregunta y palabra de identidad: Poppins 800, 66 px
- descripción: Poppins 400, 22 px
PORTADA: pregunta al centro (45-60%) con mezcla serif itálica + sans extra bold; objetos 3D recortados en las esquinas (café, audífonos, laptop) + un cursor de tu color apuntando.
SLIDES DEL MEDIO: píldora con borde «Kit de [TIPO]» (~14%); nombre del arquetipo en serif itálica grande (18-24%); collage de 5 objetos recortados numerados «1.–5.» (30-85%) que lo delatan; pie: 2 renglones + frase-firma entre comillas en serif itálica.
CIERRE: «¿Cuál eres tú?» + «escríbelo en los comentarios» + un elemento de marca tuyo.
ELEMENTOS GRÁFICOS: objetos de producto recortados a todo color · numeración 1.–5. en serif · frase-firma entre comillas por tipo
EVITA: logos, mascotas o apps ajenas como protagonistas.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 60 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: gris cálido liso #F3F3F1 en todas.
PALETA (usa SOLO estos colores): #F3F3F1 = fondo · #000000 = tinta · #AE102E = rojo de marca: cursor, detalles (o tu color de marca)
TIPOGRAFÍA:
- nombre del arquetipo: estilo Instrument Serif (400 itálica), letra de ~6% del alto; tracking apretado
- pregunta y palabra de identidad: estilo Poppins (800), letra de ~5% del alto
- descripción: estilo Poppins (400), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: pregunta al centro (45-60%) con mezcla serif itálica + sans extra bold; objetos 3D recortados en las esquinas (café, audífonos, laptop) + un cursor de tu color apuntando.
ELEMENTOS GRÁFICOS: objetos de producto recortados a todo color · numeración 1.–5. en serif · frase-firma entre comillas por tipo
EVITA: logos, mascotas o apps ajenas como protagonistas.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: gris cálido liso #F3F3F1 en todas.
COMPOSICIÓN: pregunta al centro (45-60%) con mezcla serif itálica + sans extra bold; objetos 3D recortados en las esquinas (café, audífonos, laptop) + un cursor de tu color apuntando.
ELEMENTOS: objetos de producto recortados a todo color · numeración 1.–5. en serif · frase-firma entre comillas por tipo
```
**C · Solo fondo, sin texto**
```
Genera SOLO EL FONDO de un slide de carrusel, imagen vertical 4:5, SIN NINGÚN TEXTO, letra, número ni logo.
[OBJETO QUE DELATA AL ARQUETIPO] recortado, foto de producto de estudio, fondo transparente, sin texto.
Deja libre de objetos la zona donde irá el texto: arriba y el pie.
Paleta: #F3F3F1 = fondo · #000000 = tinta · #AE102E = rojo de marca: cursor, detalles (o tu color de marca).
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: píldora con borde «Kit de [TIPO]» (~14%); nombre del arquetipo en serif itálica grande (18-24%); collage de 5 objetos recortados numerados «1.–5.» (30-85%) que lo delatan; pie: 2 renglones + frase-firma entre comillas en serif itálica.
(Si es la última slide, la composición es: «¿Cuál eres tú?» + «escríbelo en los comentarios» + un elemento de marca tuyo.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: gris cálido liso #F3F3F1 en todas.
PALETA (usa SOLO estos colores): #F3F3F1 = fondo · #000000 = tinta · #AE102E = rojo de marca: cursor, detalles (o tu color de marca)
TIPOGRAFÍA:
- nombre del arquetipo: estilo Instrument Serif (400 itálica), letra de ~6% del alto; tracking apretado
- pregunta y palabra de identidad: estilo Poppins (800), letra de ~5% del alto
- descripción: estilo Poppins (400), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: pregunta al centro (45-60%) con mezcla serif itálica + sans extra bold; objetos 3D recortados en las esquinas (café, audífonos, laptop) + un cursor de tu color apuntando.
ELEMENTOS GRÁFICOS: objetos de producto recortados a todo color · numeración 1.–5. en serif · frase-firma entre comillas por tipo
EVITA: logos, mascotas o apps ajenas como protagonistas.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: gris cálido liso #F3F3F1 en todas.
COMPOSICIÓN: pregunta al centro (45-60%) con mezcla serif itálica + sans extra bold; objetos 3D recortados en las esquinas (café, audífonos, laptop) + un cursor de tu color apuntando.
ELEMENTOS: objetos de producto recortados a todo color · numeración 1.–5. en serif · frase-firma entre comillas por tipo
```
**C · Solo fondo, sin texto**
```
Crea una imagen vertical 4:5 que sirva de FONDO para un slide. Importante: SIN texto, letras, números, logos ni marcas de agua.
[OBJETO QUE DELATA AL ARQUETIPO] recortado, foto de producto de estudio, fondo transparente, sin texto.
Deja vacía la zona de arriba y el pie: ahí pondré el texto después.
Colores: #F3F3F1 = fondo · #000000 = tinta · #AE102E = rojo de marca: cursor, detalles (o tu color de marca).
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: píldora con borde «Kit de [TIPO]» (~14%); nombre del arquetipo en serif itálica grande (18-24%); collage de 5 objetos recortados numerados «1.–5.» (30-85%) que lo delatan; pie: 2 renglones + frase-firma entre comillas en serif itálica.
(Si es la última slide, la composición es: «¿Cuál eres tú?» + «escríbelo en los comentarios» + un elemento de marca tuyo.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## G04 · Lo que nadie te dice de X (mito / realidad)

**Ejemplo:** @marinaaurorabustamante · https://www.instagram.com/p/DO6cdKjERYw/ · 514 likes · 7 slides (solo sirve de ESTILO: la referencia no trae el molde «lo que te dicen / lo que pasa»; cada slide es un consejo)

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: fotos reales tuyas con tu comunidad o en un evento, a sangre; en internas degradado de tu color de marca desde el pie hasta ~60% del alto.
PALETA (usa SOLO estos colores): #E9729C = rosa claro (o tu color de marca) · #CC2A72 = magenta del degradado · #FF63C1 = texto en arco de portada · #FFFFFF = texto · #2A1215 = bloque oscuro de «lo que te dicen»
TIPOGRAFÍA:
- título en arco: Baloo 2 800, minúsculas, blanco con contorno de color, 80 px
- «Lo que te dicen» / «Lo que pasa»: Inter 700, MAYÚSCULAS chicas, 26 px
- frase: Inter 700, 42 px
- detalle de tu experiencia: Inter 400, 34 px
PORTADA: «lo que nadie te dice» en ARCO siguiendo las cabezas de la foto + «de [tema]» en arco abajo; letras blancas con contorno de tu color.
SLIDES DEL MEDIO: sobre el degradado inferior (60-95%): etiqueta «LO QUE TE DICEN:» + la frase tachada; debajo «LO QUE PASA:» + la verdad en bold + 1-2 líneas de tu experiencia. La penúltima: la verdad más incómoda sola y grande.
CIERRE: línea de alivio («y aun así vale la pena si…») + «guárdalo».
ELEMENTOS GRÁFICOS: texto en arco en la portada · degradado de marca en el tercio inferior · tachado sobre lo que te dicen
EVITA: fotos de banco y un rosa que no sea tu marca.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Escribe un carrusel "Lo que nadie te dice de [TEMA DESEADO por mi cliente]" de 8 slides, para [QUIÉN ESTÁ POR EMPEZAR].
Slide 1: el título + a quién le hablo.
Slide 2: la frase que todos repiten, entre comillas.
Slides 3-7: 5 verdades. Cada una en 2 bloques: "Lo que te dicen:" (máx. 8 palabras) / "Lo que pasa:" (máx. 20 palabras) + un detalle real de mi experiencia: [PEGA 5 COSAS QUE TE PASARON].
Slide 8: la verdad más incómoda sola + "y aun así vale la pena si…" + "guárdalo".
No uses verdades que diría cualquiera de mi nicho. Tutea.
```

### 2 · Claude Code
```
hazme un carrusel tipo G04 (Lo que nadie te dice de X (mito / realidad)) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: fotos reales tuyas con tu comunidad o en un evento, a sangre; en internas degradado de tu color de marca desde el pie hasta ~60% del alto.
PALETA (usa SOLO estos colores): #E9729C = rosa claro (o tu color de marca) · #CC2A72 = magenta del degradado · #FF63C1 = texto en arco de portada · #FFFFFF = texto · #2A1215 = bloque oscuro de «lo que te dicen»
TIPOGRAFÍA:
- título en arco: Baloo 2 800, minúsculas, blanco con contorno de color, 80 px
- «Lo que te dicen» / «Lo que pasa»: Inter 700, MAYÚSCULAS chicas, 26 px
- frase: Inter 700, 42 px
- detalle de tu experiencia: Inter 400, 34 px
PORTADA: «lo que nadie te dice» en ARCO siguiendo las cabezas de la foto + «de [tema]» en arco abajo; letras blancas con contorno de tu color.
SLIDES DEL MEDIO: sobre el degradado inferior (60-95%): etiqueta «LO QUE TE DICEN:» + la frase tachada; debajo «LO QUE PASA:» + la verdad en bold + 1-2 líneas de tu experiencia. La penúltima: la verdad más incómoda sola y grande.
CIERRE: línea de alivio («y aun así vale la pena si…») + «guárdalo».
ELEMENTOS GRÁFICOS: texto en arco en la portada · degradado de marca en el tercio inferior · tachado sobre lo que te dicen
EVITA: fotos de banco y un rosa que no sea tu marca.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 80 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: fotos reales tuyas con tu comunidad o en un evento, a sangre; en internas degradado de tu color de marca desde el pie hasta ~60% del alto.
PALETA (usa SOLO estos colores): #E9729C = rosa claro (o tu color de marca) · #CC2A72 = magenta del degradado · #FF63C1 = texto en arco de portada · #FFFFFF = texto · #2A1215 = bloque oscuro de «lo que te dicen»
TIPOGRAFÍA:
- título en arco: estilo Baloo 2 (800), minúsculas, blanco con contorno de color, letra de ~6% del alto
- «Lo que te dicen» / «Lo que pasa»: estilo Inter (700), MAYÚSCULAS chicas, letra de ~2% del alto
- frase: estilo Inter (700), letra de ~3% del alto
- detalle de tu experiencia: estilo Inter (400), letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: «lo que nadie te dice» en ARCO siguiendo las cabezas de la foto + «de [tema]» en arco abajo; letras blancas con contorno de tu color.
ELEMENTOS GRÁFICOS: texto en arco en la portada · degradado de marca en el tercio inferior · tachado sobre lo que te dicen
EVITA: fotos de banco y un rosa que no sea tu marca.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: fotos reales tuyas con tu comunidad o en un evento, a sangre; en internas degradado de tu color de marca desde el pie hasta ~60% del alto.
COMPOSICIÓN: «lo que nadie te dice» en ARCO siguiendo las cabezas de la foto + «de [tema]» en arco abajo; letras blancas con contorno de tu color.
ELEMENTOS: texto en arco en la portada · degradado de marca en el tercio inferior · tachado sobre lo que te dicen
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: lleva tus fotos o capturas reales (fotos reales tuyas con tu comunidad o en un evento, a sangre; en internas degradado de tu color de marca desde el pie hasta ~60% del alto.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: sobre el degradado inferior (60-95%): etiqueta «LO QUE TE DICEN:» + la frase tachada; debajo «LO QUE PASA:» + la verdad en bold + 1-2 líneas de tu experiencia. La penúltima: la verdad más incómoda sola y grande.
(Si es la última slide, la composición es: línea de alivio («y aun así vale la pena si…») + «guárdalo».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: fotos reales tuyas con tu comunidad o en un evento, a sangre; en internas degradado de tu color de marca desde el pie hasta ~60% del alto.
PALETA (usa SOLO estos colores): #E9729C = rosa claro (o tu color de marca) · #CC2A72 = magenta del degradado · #FF63C1 = texto en arco de portada · #FFFFFF = texto · #2A1215 = bloque oscuro de «lo que te dicen»
TIPOGRAFÍA:
- título en arco: estilo Baloo 2 (800), minúsculas, blanco con contorno de color, letra de ~6% del alto
- «Lo que te dicen» / «Lo que pasa»: estilo Inter (700), MAYÚSCULAS chicas, letra de ~2% del alto
- frase: estilo Inter (700), letra de ~3% del alto
- detalle de tu experiencia: estilo Inter (400), letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: «lo que nadie te dice» en ARCO siguiendo las cabezas de la foto + «de [tema]» en arco abajo; letras blancas con contorno de tu color.
ELEMENTOS GRÁFICOS: texto en arco en la portada · degradado de marca en el tercio inferior · tachado sobre lo que te dicen
EVITA: fotos de banco y un rosa que no sea tu marca.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: fotos reales tuyas con tu comunidad o en un evento, a sangre; en internas degradado de tu color de marca desde el pie hasta ~60% del alto.
COMPOSICIÓN: «lo que nadie te dice» en ARCO siguiendo las cabezas de la foto + «de [tema]» en arco abajo; letras blancas con contorno de tu color.
ELEMENTOS: texto en arco en la portada · degradado de marca en el tercio inferior · tachado sobre lo que te dicen
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: lleva tus fotos o capturas reales (fotos reales tuyas con tu comunidad o en un evento, a sangre; en internas degradado de tu color de marca desde el pie hasta ~60% del alto.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: sobre el degradado inferior (60-95%): etiqueta «LO QUE TE DICEN:» + la frase tachada; debajo «LO QUE PASA:» + la verdad en bold + 1-2 líneas de tu experiencia. La penúltima: la verdad más incómoda sola y grande.
(Si es la última slide, la composición es: línea de alivio («y aun así vale la pena si…») + «guárdalo».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## G05 · Biblioteca de recursos

**Ejemplo:** @brandcrops · https://www.instagram.com/p/DRAIqFmjJMa/ · 182 likes · 47 comentarios · 7 slides (agrupa 5 herramientas por slide y no trae slide de flujo)

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: azul marino liso #001274 en todas.
PALETA (usa SOLO estos colores): #001274 = fondo · #00C182 = verde acento · #FFFFFF = texto y fichas de íconos
TIPOGRAFÍA:
- portada: Source Sans 3 300 con palabras en 700, 68 px
- título interno: Source Sans 3 700, 42 px
- nombre y uso de la herramienta: Source Sans 3 700 / 400, 24 px
PORTADA: 6 líneas centradas (22-80% del alto) mezclando peso fino blanco y bold verde, emojis 3D pegados a letras, flecha fina → abajo.
SLIDES DEL MEDIO: título alineado a la izquierda arriba «Herramientas para» + categoría en verde (12-35%); grilla de fichas blancas redondeadas con el ícono real (17% del ancho): fila de 3 + fila de 2 (40-90%), nombre + para qué en 1 línea debajo de cada una. (Si haces 1 por slide: ficha grande + «Yo la uso cuando…».)
CIERRE: píldora blanca con 3 emojis + pregunta fina + «Comenta [PALABRA]» bold verde subrayado.
ELEMENTOS GRÁFICOS: íconos reales reconocibles · solo 2 colores + fondo liso
EVITA: prometer un número que no muestras.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Escribe un carrusel de 8 slides con [N=5] herramientas/recursos que YO uso para [RESULTADO de mi nicho]. Mis herramientas: [LISTA + para qué las uso].
Slide 1: "[N] herramientas que me ahorran [TIEMPO/DINERO CONCRETO]".
Slides 2-6: una por slide → nombre + precio (gratis/pago) + "Para:" (máx. 10 palabras) + "Yo la uso cuando…" (un caso real, máx. 15 palabras). Indica la captura de pantalla que va en cada slide.
Slide 7: cómo las combino en un flujo de 3 pasos.
Slide 8: "Comenta [PALABRA] y te mando la lista con links".
No inventes precios: márcalos [VERIFICAR]. Tutea.
```

### 2 · Claude Code
```
hazme un carrusel tipo G05 (Biblioteca de recursos) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: azul marino liso #001274 en todas.
PALETA (usa SOLO estos colores): #001274 = fondo · #00C182 = verde acento · #FFFFFF = texto y fichas de íconos
TIPOGRAFÍA:
- portada: Source Sans 3 300 con palabras en 700, 68 px
- título interno: Source Sans 3 700, 42 px
- nombre y uso de la herramienta: Source Sans 3 700 / 400, 24 px
PORTADA: 6 líneas centradas (22-80% del alto) mezclando peso fino blanco y bold verde, emojis 3D pegados a letras, flecha fina → abajo.
SLIDES DEL MEDIO: título alineado a la izquierda arriba «Herramientas para» + categoría en verde (12-35%); grilla de fichas blancas redondeadas con el ícono real (17% del ancho): fila de 3 + fila de 2 (40-90%), nombre + para qué en 1 línea debajo de cada una. (Si haces 1 por slide: ficha grande + «Yo la uso cuando…».)
CIERRE: píldora blanca con 3 emojis + pregunta fina + «Comenta [PALABRA]» bold verde subrayado.
ELEMENTOS GRÁFICOS: íconos reales reconocibles · solo 2 colores + fondo liso
EVITA: prometer un número que no muestras.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 80 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: azul marino liso #001274 en todas.
PALETA (usa SOLO estos colores): #001274 = fondo · #00C182 = verde acento · #FFFFFF = texto y fichas de íconos
TIPOGRAFÍA:
- portada: estilo Source Sans 3 (300 con palabras en 700), letra de ~5% del alto
- título interno: estilo Source Sans 3 (700), letra de ~3% del alto
- nombre y uso de la herramienta: estilo Source Sans 3 (700 / 400), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: 6 líneas centradas (22-80% del alto) mezclando peso fino blanco y bold verde, emojis 3D pegados a letras, flecha fina → abajo.
ELEMENTOS GRÁFICOS: íconos reales reconocibles · solo 2 colores + fondo liso
EVITA: prometer un número que no muestras.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: azul marino liso #001274 en todas.
COMPOSICIÓN: 6 líneas centradas (22-80% del alto) mezclando peso fino blanco y bold verde, emojis 3D pegados a letras, flecha fina → abajo.
ELEMENTOS: íconos reales reconocibles · solo 2 colores + fondo liso
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (azul marino liso #001274 en todas.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: título alineado a la izquierda arriba «Herramientas para» + categoría en verde (12-35%); grilla de fichas blancas redondeadas con el ícono real (17% del ancho): fila de 3 + fila de 2 (40-90%), nombre + para qué en 1 línea debajo de cada una. (Si haces 1 por slide: ficha grande + «Yo la uso cuando…».)
(Si es la última slide, la composición es: píldora blanca con 3 emojis + pregunta fina + «Comenta [PALABRA]» bold verde subrayado.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: azul marino liso #001274 en todas.
PALETA (usa SOLO estos colores): #001274 = fondo · #00C182 = verde acento · #FFFFFF = texto y fichas de íconos
TIPOGRAFÍA:
- portada: estilo Source Sans 3 (300 con palabras en 700), letra de ~5% del alto
- título interno: estilo Source Sans 3 (700), letra de ~3% del alto
- nombre y uso de la herramienta: estilo Source Sans 3 (700 / 400), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: 6 líneas centradas (22-80% del alto) mezclando peso fino blanco y bold verde, emojis 3D pegados a letras, flecha fina → abajo.
ELEMENTOS GRÁFICOS: íconos reales reconocibles · solo 2 colores + fondo liso
EVITA: prometer un número que no muestras.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: azul marino liso #001274 en todas.
COMPOSICIÓN: 6 líneas centradas (22-80% del alto) mezclando peso fino blanco y bold verde, emojis 3D pegados a letras, flecha fina → abajo.
ELEMENTOS: íconos reales reconocibles · solo 2 colores + fondo liso
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (azul marino liso #001274 en todas.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: título alineado a la izquierda arriba «Herramientas para» + categoría en verde (12-35%); grilla de fichas blancas redondeadas con el ícono real (17% del ancho): fila de 3 + fila de 2 (40-90%), nombre + para qué en 1 línea debajo de cada una. (Si haces 1 por slide: ficha grande + «Yo la uso cuando…».)
(Si es la última slide, la composición es: píldora blanca con 3 emojis + pregunta fina + «Comenta [PALABRA]» bold verde subrayado.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## G06 · Glosario de tu nicho

**Ejemplo:** @cem.ve · https://www.instagram.com/p/DQxIMFgFKbC/ · 14 likes · 5 slides (molde visual débil (14 likes, 2 términos por slide y sin ejemplo); hay un candidato mejor sin anclar: @glorymar.negron https://www.instagram.com/p/DT0-BIUkdJs/ (13.956 likes))

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: degradado cálido que avanza por slide: amarillo → naranja claro → naranja.
PALETA (usa SOLO estos colores): #FFDD55 = portada · #FDB368 = slides 2-3 · #FFA554 = slides 4-5 · #EF9B50 = brochazo detrás del término · #D32300 = óvalo a mano · #1A1A1A = definición y ejemplo
TIPOGRAFÍA:
- título «Glosario»: Poppins 800, contorno blanco hueco, 110 px
- término: Poppins 600, MAYÚSCULAS, 56 px
- definición: Poppins 400, 32 px
- ejemplo: Poppins 400 itálica, 26 px
PORTADA: «Glosario» en contorno blanco hueco + «de [tu nicho]» bold + «(para principiantes)» fino; objetos 3D (libreta, lápiz) abajo a la derecha.
SLIDES DEL MEDIO: UN término por slide: término sobre brochazo naranja oscuro + emoji 3D (15-35%); definición en tinta oscura de 2-3 líneas con 1 palabra rodeada por un óvalo rojo a mano (40-65%); «Ejemplo:» en itálica en un recuadro blanco (70-88%); número de página abajo a la derecha.
CIERRE: «Guárdalo para cuando lo vuelvas a leer» + píldora con ♥ 💬 ✈ 🔖.
ELEMENTOS GRÁFICOS: brochazo detrás del término · óvalo rojo dibujado a mano · numeración de página
EVITA: rótulos de otras marcas y texto blanco fino sobre naranja claro (no se lee).
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Escribe un carrusel glosario de 8 slides con los 6 términos que más confunden a [PRINCIPIANTE de mi nicho].
Slide 1: "¿No entiendes qué es [término 1], [término 2] o [término 3]? Este es tu glosario".
Slides 2-7: TÉRMINO en mayúsculas + cómo se pronuncia si es en inglés + definición de máx. 15 palabras SIN usar otra palabra técnica + "Ejemplo:" de mi rubro (máx. 15 palabras).
Slide 8: "Guárdalo para cuando lo vuelvas a leer" + "¿qué palabra te falta? coméntala".
Tutea.
```

### 2 · Claude Code
```
hazme un carrusel tipo G06 (Glosario de tu nicho) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: degradado cálido que avanza por slide: amarillo → naranja claro → naranja.
PALETA (usa SOLO estos colores): #FFDD55 = portada · #FDB368 = slides 2-3 · #FFA554 = slides 4-5 · #EF9B50 = brochazo detrás del término · #D32300 = óvalo a mano · #1A1A1A = definición y ejemplo
TIPOGRAFÍA:
- título «Glosario»: Poppins 800, contorno blanco hueco, 110 px
- término: Poppins 600, MAYÚSCULAS, 56 px
- definición: Poppins 400, 32 px
- ejemplo: Poppins 400 itálica, 26 px
PORTADA: «Glosario» en contorno blanco hueco + «de [tu nicho]» bold + «(para principiantes)» fino; objetos 3D (libreta, lápiz) abajo a la derecha.
SLIDES DEL MEDIO: UN término por slide: término sobre brochazo naranja oscuro + emoji 3D (15-35%); definición en tinta oscura de 2-3 líneas con 1 palabra rodeada por un óvalo rojo a mano (40-65%); «Ejemplo:» en itálica en un recuadro blanco (70-88%); número de página abajo a la derecha.
CIERRE: «Guárdalo para cuando lo vuelvas a leer» + píldora con ♥ 💬 ✈ 🔖.
ELEMENTOS GRÁFICOS: brochazo detrás del término · óvalo rojo dibujado a mano · numeración de página
EVITA: rótulos de otras marcas y texto blanco fino sobre naranja claro (no se lee).

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 80 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: degradado cálido que avanza por slide: amarillo → naranja claro → naranja.
PALETA (usa SOLO estos colores): #FFDD55 = portada · #FDB368 = slides 2-3 · #FFA554 = slides 4-5 · #EF9B50 = brochazo detrás del término · #D32300 = óvalo a mano · #1A1A1A = definición y ejemplo
TIPOGRAFÍA:
- título «Glosario»: estilo Poppins (800), contorno blanco hueco, letra de ~8% del alto
- término: estilo Poppins (600), MAYÚSCULAS, letra de ~4% del alto
- definición: estilo Poppins (400), letra de ~2% del alto
- ejemplo: estilo Poppins (400 itálica), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: «Glosario» en contorno blanco hueco + «de [tu nicho]» bold + «(para principiantes)» fino; objetos 3D (libreta, lápiz) abajo a la derecha.
ELEMENTOS GRÁFICOS: brochazo detrás del término · óvalo rojo dibujado a mano · numeración de página
EVITA: rótulos de otras marcas y texto blanco fino sobre naranja claro (no se lee).
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: degradado cálido que avanza por slide: amarillo → naranja claro → naranja.
COMPOSICIÓN: «Glosario» en contorno blanco hueco + «de [tu nicho]» bold + «(para principiantes)» fino; objetos 3D (libreta, lápiz) abajo a la derecha.
ELEMENTOS: brochazo detrás del término · óvalo rojo dibujado a mano · numeración de página
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (degradado cálido que avanza por slide: amarillo → naranja claro → naranja.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: UN término por slide: término sobre brochazo naranja oscuro + emoji 3D (15-35%); definición en tinta oscura de 2-3 líneas con 1 palabra rodeada por un óvalo rojo a mano (40-65%); «Ejemplo:» en itálica en un recuadro blanco (70-88%); número de página abajo a la derecha.
(Si es la última slide, la composición es: «Guárdalo para cuando lo vuelvas a leer» + píldora con ♥ 💬 ✈ 🔖.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: degradado cálido que avanza por slide: amarillo → naranja claro → naranja.
PALETA (usa SOLO estos colores): #FFDD55 = portada · #FDB368 = slides 2-3 · #FFA554 = slides 4-5 · #EF9B50 = brochazo detrás del término · #D32300 = óvalo a mano · #1A1A1A = definición y ejemplo
TIPOGRAFÍA:
- título «Glosario»: estilo Poppins (800), contorno blanco hueco, letra de ~8% del alto
- término: estilo Poppins (600), MAYÚSCULAS, letra de ~4% del alto
- definición: estilo Poppins (400), letra de ~2% del alto
- ejemplo: estilo Poppins (400 itálica), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: «Glosario» en contorno blanco hueco + «de [tu nicho]» bold + «(para principiantes)» fino; objetos 3D (libreta, lápiz) abajo a la derecha.
ELEMENTOS GRÁFICOS: brochazo detrás del término · óvalo rojo dibujado a mano · numeración de página
EVITA: rótulos de otras marcas y texto blanco fino sobre naranja claro (no se lee).
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: degradado cálido que avanza por slide: amarillo → naranja claro → naranja.
COMPOSICIÓN: «Glosario» en contorno blanco hueco + «de [tu nicho]» bold + «(para principiantes)» fino; objetos 3D (libreta, lápiz) abajo a la derecha.
ELEMENTOS: brochazo detrás del término · óvalo rojo dibujado a mano · numeración de página
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (degradado cálido que avanza por slide: amarillo → naranja claro → naranja.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: UN término por slide: término sobre brochazo naranja oscuro + emoji 3D (15-35%); definición en tinta oscura de 2-3 líneas con 1 palabra rodeada por un óvalo rojo a mano (40-65%); «Ejemplo:» en itálica en un recuadro blanco (70-88%); número de página abajo a la derecha.
(Si es la última slide, la composición es: «Guárdalo para cuando lo vuelvas a leer» + píldora con ♥ 💬 ✈ 🔖.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## G07 · Mini caso de estudio

**Ejemplo:** @soldea · https://www.instagram.com/p/DWkGZMUj8fU/ · 283 likes · 7 slides

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: la MISMA escena tuya (una selfie con carácter) a sangre en todas, cada vez más oscurecida y desenfocada detrás del contenido.
PALETA (usa SOLO estos colores): #21201C = fondo oscuro metálico · #0C0C0B = sombra más densa · #FFFFFF = texto · #9D7552 = calidez de la foto
TIPOGRAFÍA:
- portada: Instrument Serif 400 + itálica, 56 px; la palabra del resultado en itálica ~95 px
- internas: Manrope 300 con frase clave en 700, 30 px
PORTADA: tú de cuerpo entero en la escena; texto disperso en 3 bloques (izq 48-56%, centro 75-78%, abajo a la derecha 88-95%) con la palabra del resultado gigante en itálica.
SLIDES DEL MEDIO: frase arriba centrada (15-25%); PRUEBA al centro (~50% del ancho): captura de tus métricas o de tu grid; explicación abajo (70-90%) con la frase clave en bold.
CIERRE: 3 párrafos centrados con la lección + ícono de guardar abajo a la derecha.
ELEMENTOS GRÁFICOS: capturas reales de tus datos como prueba · la escena oscurecida como hilo visual
EVITA: escenas de banco y citas de terceros sin verificar.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Tengo este resultado real: [DATO + PERIODO + CAPTURA DISPONIBLE] y esto fue lo que cambié: [LO QUE HICISTE].
Escribe un mini caso de estudio de 7 slides:
Slide 1: el hallazgo que contradice lo esperado (máx. 12 palabras).
Slide 2: el número grande + unidad + periodo + "captura:" (qué captura va).
Slides 3-6: una decisión por slide → qué hice (máx. 10 palabras) + por qué creo que funcionó (máx. 20) + qué NO sé todavía si aplica.
Slide 7: la lección en 1 frase que el lector puede probar esta semana + "guárdalo".
Usa SOLO mis números. Nada de promedios que no te di. Tutea.
```

### 2 · Claude Code
```
hazme un carrusel tipo G07 (Mini caso de estudio) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: la MISMA escena tuya (una selfie con carácter) a sangre en todas, cada vez más oscurecida y desenfocada detrás del contenido.
PALETA (usa SOLO estos colores): #21201C = fondo oscuro metálico · #0C0C0B = sombra más densa · #FFFFFF = texto · #9D7552 = calidez de la foto
TIPOGRAFÍA:
- portada: Instrument Serif 400 + itálica, 56 px; la palabra del resultado en itálica ~95 px
- internas: Manrope 300 con frase clave en 700, 30 px
PORTADA: tú de cuerpo entero en la escena; texto disperso en 3 bloques (izq 48-56%, centro 75-78%, abajo a la derecha 88-95%) con la palabra del resultado gigante en itálica.
SLIDES DEL MEDIO: frase arriba centrada (15-25%); PRUEBA al centro (~50% del ancho): captura de tus métricas o de tu grid; explicación abajo (70-90%) con la frase clave en bold.
CIERRE: 3 párrafos centrados con la lección + ícono de guardar abajo a la derecha.
ELEMENTOS GRÁFICOS: capturas reales de tus datos como prueba · la escena oscurecida como hilo visual
EVITA: escenas de banco y citas de terceros sin verificar.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 80 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: la MISMA escena tuya (una selfie con carácter) a sangre en todas, cada vez más oscurecida y desenfocada detrás del contenido.
PALETA (usa SOLO estos colores): #21201C = fondo oscuro metálico · #0C0C0B = sombra más densa · #FFFFFF = texto · #9D7552 = calidez de la foto
TIPOGRAFÍA:
- portada: estilo Instrument Serif (400 + itálica), letra de ~4% del alto; la palabra del resultado en itálica ~95 px
- internas: estilo Manrope (300 con frase clave en 700), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: tú de cuerpo entero en la escena; texto disperso en 3 bloques (izq 48-56%, centro 75-78%, abajo a la derecha 88-95%) con la palabra del resultado gigante en itálica.
ELEMENTOS GRÁFICOS: capturas reales de tus datos como prueba · la escena oscurecida como hilo visual
EVITA: escenas de banco y citas de terceros sin verificar.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: la MISMA escena tuya (una selfie con carácter) a sangre en todas, cada vez más oscurecida y desenfocada detrás del contenido.
COMPOSICIÓN: tú de cuerpo entero en la escena; texto disperso en 3 bloques (izq 48-56%, centro 75-78%, abajo a la derecha 88-95%) con la palabra del resultado gigante en itálica.
ELEMENTOS: capturas reales de tus datos como prueba · la escena oscurecida como hilo visual
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (la MISMA escena tuya (una selfie con carácter) a sangre en todas, cada vez más oscurecida y desenfocada detrás del contenido.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: frase arriba centrada (15-25%); PRUEBA al centro (~50% del ancho): captura de tus métricas o de tu grid; explicación abajo (70-90%) con la frase clave en bold.
(Si es la última slide, la composición es: 3 párrafos centrados con la lección + ícono de guardar abajo a la derecha.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: la MISMA escena tuya (una selfie con carácter) a sangre en todas, cada vez más oscurecida y desenfocada detrás del contenido.
PALETA (usa SOLO estos colores): #21201C = fondo oscuro metálico · #0C0C0B = sombra más densa · #FFFFFF = texto · #9D7552 = calidez de la foto
TIPOGRAFÍA:
- portada: estilo Instrument Serif (400 + itálica), letra de ~4% del alto; la palabra del resultado en itálica ~95 px
- internas: estilo Manrope (300 con frase clave en 700), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: tú de cuerpo entero en la escena; texto disperso en 3 bloques (izq 48-56%, centro 75-78%, abajo a la derecha 88-95%) con la palabra del resultado gigante en itálica.
ELEMENTOS GRÁFICOS: capturas reales de tus datos como prueba · la escena oscurecida como hilo visual
EVITA: escenas de banco y citas de terceros sin verificar.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: la MISMA escena tuya (una selfie con carácter) a sangre en todas, cada vez más oscurecida y desenfocada detrás del contenido.
COMPOSICIÓN: tú de cuerpo entero en la escena; texto disperso en 3 bloques (izq 48-56%, centro 75-78%, abajo a la derecha 88-95%) con la palabra del resultado gigante en itálica.
ELEMENTOS: capturas reales de tus datos como prueba · la escena oscurecida como hilo visual
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (la MISMA escena tuya (una selfie con carácter) a sangre en todas, cada vez más oscurecida y desenfocada detrás del contenido.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: frase arriba centrada (15-25%); PRUEBA al centro (~50% del ancho): captura de tus métricas o de tu grid; explicación abajo (70-90%) con la frase clave en bold.
(Si es la última slide, la composición es: 3 párrafos centrados con la lección + ícono de guardar abajo a la derecha.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## G08 · Molde para copiar

**Ejemplo:** @estebaneras.a · https://www.instagram.com/p/DSGer-tD5PG/ · 140 likes · 140 comentarios · 10 slides (solo sirve de ESTILO: es un tutorial con capturas, no un molde con [huecos])

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: blanco roto #FAFAFA.
PALETA (usa SOLO estos colores): #FAFAFA = fondo · #5A199C = morado de marca: bordes, frase clave (o tu color de marca) · #10061C = tinta · #FFD60A = resaltado de los [HUECOS]
TIPOGRAFÍA:
- titular: DM Serif Display 400, 56 px
- texto del molde: Montserrat 500, 30 px
- ejemplo relleno: Montserrat 400 itálica, 22 px
PORTADA: avatar + nombre arriba a la izquierda (5-12%); titular serif centrado de 2 líneas (30-43%); banda de tu color con texto blanco (~45%) «listo para copiar».
SLIDES DEL MEDIO: frase de instrucción arriba a la izquierda (20-35%) con 1 frase en tu color; al centro (40-90%) el BLOQUE DEL MOLDE en una tarjeta con borde de 2 px de tu color y esquinas redondeadas: texto fijo en negro y [HUECOS EN MAYÚSCULAS] resaltados; debajo, «Ejemplo:» relleno en itálica chica.
CIERRE: avatar grande + «Comenta [PALABRA]» en serif de tu color + «y te lo mando en texto para copiar».
ELEMENTOS GRÁFICOS: tarjeta con borde de color para cada bloque · huecos resaltados · captura del resultado en la slide 2
EVITA: personajes 3D, avatares o colores de otra marca.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Este es un mensaje/guion que uso en mi negocio y funciona: [PEGA EL TEXTO REAL + qué resultado te dio].
Conviértelo en un carrusel molde de 7 slides:
Slide 1: "[El mensaje que uso para X], listo para copiar" (máx. 12 palabras).
Slide 2: el resultado real de usarlo + qué captura va.
Slides 3-6: un bloque del molde por slide, con el texto fijo tal cual y los huecos entre [CORCHETES EN MAYÚSCULAS]. Debajo: "Ejemplo:" con ese bloque ya relleno para [cliente ficticio de mi rubro].
Slide 7: "Comenta [PALABRA] y te lo mando en texto para copiar".
No cambies mi texto salvo para quitar datos privados. Tutea.
```

### 2 · Claude Code
```
hazme un carrusel tipo G08 (Molde para copiar) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: blanco roto #FAFAFA.
PALETA (usa SOLO estos colores): #FAFAFA = fondo · #5A199C = morado de marca: bordes, frase clave (o tu color de marca) · #10061C = tinta · #FFD60A = resaltado de los [HUECOS]
TIPOGRAFÍA:
- titular: DM Serif Display 400, 56 px
- texto del molde: Montserrat 500, 30 px
- ejemplo relleno: Montserrat 400 itálica, 22 px
PORTADA: avatar + nombre arriba a la izquierda (5-12%); titular serif centrado de 2 líneas (30-43%); banda de tu color con texto blanco (~45%) «listo para copiar».
SLIDES DEL MEDIO: frase de instrucción arriba a la izquierda (20-35%) con 1 frase en tu color; al centro (40-90%) el BLOQUE DEL MOLDE en una tarjeta con borde de 2 px de tu color y esquinas redondeadas: texto fijo en negro y [HUECOS EN MAYÚSCULAS] resaltados; debajo, «Ejemplo:» relleno en itálica chica.
CIERRE: avatar grande + «Comenta [PALABRA]» en serif de tu color + «y te lo mando en texto para copiar».
ELEMENTOS GRÁFICOS: tarjeta con borde de color para cada bloque · huecos resaltados · captura del resultado en la slide 2
EVITA: personajes 3D, avatares o colores de otra marca.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 80 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: blanco roto #FAFAFA.
PALETA (usa SOLO estos colores): #FAFAFA = fondo · #5A199C = morado de marca: bordes, frase clave (o tu color de marca) · #10061C = tinta · #FFD60A = resaltado de los [HUECOS]
TIPOGRAFÍA:
- titular: estilo DM Serif Display (400), letra de ~4% del alto
- texto del molde: estilo Montserrat (500), letra de ~2% del alto
- ejemplo relleno: estilo Montserrat (400 itálica), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: avatar + nombre arriba a la izquierda (5-12%); titular serif centrado de 2 líneas (30-43%); banda de tu color con texto blanco (~45%) «listo para copiar».
ELEMENTOS GRÁFICOS: tarjeta con borde de color para cada bloque · huecos resaltados · captura del resultado en la slide 2
EVITA: personajes 3D, avatares o colores de otra marca.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: blanco roto #FAFAFA.
COMPOSICIÓN: avatar + nombre arriba a la izquierda (5-12%); titular serif centrado de 2 líneas (30-43%); banda de tu color con texto blanco (~45%) «listo para copiar».
ELEMENTOS: tarjeta con borde de color para cada bloque · huecos resaltados · captura del resultado en la slide 2
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (blanco roto #FAFAFA.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: frase de instrucción arriba a la izquierda (20-35%) con 1 frase en tu color; al centro (40-90%) el BLOQUE DEL MOLDE en una tarjeta con borde de 2 px de tu color y esquinas redondeadas: texto fijo en negro y [HUECOS EN MAYÚSCULAS] resaltados; debajo, «Ejemplo:» relleno en itálica chica.
(Si es la última slide, la composición es: avatar grande + «Comenta [PALABRA]» en serif de tu color + «y te lo mando en texto para copiar».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: blanco roto #FAFAFA.
PALETA (usa SOLO estos colores): #FAFAFA = fondo · #5A199C = morado de marca: bordes, frase clave (o tu color de marca) · #10061C = tinta · #FFD60A = resaltado de los [HUECOS]
TIPOGRAFÍA:
- titular: estilo DM Serif Display (400), letra de ~4% del alto
- texto del molde: estilo Montserrat (500), letra de ~2% del alto
- ejemplo relleno: estilo Montserrat (400 itálica), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: avatar + nombre arriba a la izquierda (5-12%); titular serif centrado de 2 líneas (30-43%); banda de tu color con texto blanco (~45%) «listo para copiar».
ELEMENTOS GRÁFICOS: tarjeta con borde de color para cada bloque · huecos resaltados · captura del resultado en la slide 2
EVITA: personajes 3D, avatares o colores de otra marca.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: blanco roto #FAFAFA.
COMPOSICIÓN: avatar + nombre arriba a la izquierda (5-12%); titular serif centrado de 2 líneas (30-43%); banda de tu color con texto blanco (~45%) «listo para copiar».
ELEMENTOS: tarjeta con borde de color para cada bloque · huecos resaltados · captura del resultado en la slide 2
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (blanco roto #FAFAFA.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: frase de instrucción arriba a la izquierda (20-35%) con 1 frase en tu color; al centro (40-90%) el BLOQUE DEL MOLDE en una tarjeta con borde de 2 px de tu color y esquinas redondeadas: texto fijo en negro y [HUECOS EN MAYÚSCULAS] resaltados; debajo, «Ejemplo:» relleno en itálica chica.
(Si es la última slide, la composición es: avatar grande + «Comenta [PALABRA]» en serif de tu color + «y te lo mando en texto para copiar».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## G09 · Frase cortada entre slides (swipe-reveal)

**Ejemplo:** @emprendeconcata · https://www.instagram.com/p/DY48PjolruI/ · 560 likes · 248 comentarios · 9 slides (solo sirve de ESTILO: la referencia es una lista de reglas, no tiene frases cortadas entre slides)

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 90 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: rosa empolvado liso #F7ECE8 en todas.
PALETA (usa SOLO estos colores): #F7ECE8 = fondo · #EDBB4C = amarillo de píldoras y corte · #000000 = tinta
TIPOGRAFÍA:
- frase: Inter Tight 800, 72 px
- «…» del corte: Inter Tight 800, 72 px; sobre píldora amarilla, siempre abajo a la derecha
- palabra clave: Instrument Serif 400, 120 px
PORTADA: frase grande alineada a la izquierda (15-60%) mezclando sans extra bold y UNA palabra en serif gigante sobre bloque amarillo redondeado; termina cortada en «…»; la continuación asoma en una píldora amarilla abajo a la derecha (85-92%).
SLIDES DEL MEDIO: abre arriba con «…» completando la anterior, en gris 60%; la nueva frase en negro; termina cortada en el MISMO lugar (píldora abajo a la derecha).
CIERRE: penúltima: la revelación completa, SIN píldora; última: «Comenta» + [PALABRA] en la píldora amarilla.
ELEMENTOS GRÁFICOS: el corte siempre en el mismo sitio · la continuación en gris al abrir cada slide · píldora amarilla como «deuda»
EVITA: frases gancho gastadas («Roba mi sistema»), miniaturas y métricas ajenas.
```

> Cada slide lleva poco texto (máx. ~25 palabras): el modelo lo puede escribir, pero revisa tildes y eñes letra por letra antes de publicar.

### 1 · Guion (cualquier chat)
```
Escribe un carrusel swipe-reveal de 7 slides para [MI NICHO] sobre [CREENCIA QUE QUIERO ROMPER].
Regla: cada slide termina con una frase CORTADA en "…" que solo se completa al abrir la siguiente, y la siguiente EMPIEZA con "…" completándola.
El corte debe caer justo antes de la palabra que cambia el sentido (nunca en "y", "pero", "además").
Slide 1: "No es [lo que creen], es…".
Slides 2-5: cada una completa + reabre (máx. 25 palabras por slide).
Slide 6: la revelación completa, SIN corte.
Slide 7: "Comenta [PALABRA] y te mando [recurso]".
Muéstrame las 7 slides seguidas para leer el hilo de corrido. Tutea.
```

### 2 · Claude Code
```
hazme un carrusel tipo G09 (Frase cortada entre slides (swipe-reveal)) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 90 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: rosa empolvado liso #F7ECE8 en todas.
PALETA (usa SOLO estos colores): #F7ECE8 = fondo · #EDBB4C = amarillo de píldoras y corte · #000000 = tinta
TIPOGRAFÍA:
- frase: Inter Tight 800, 72 px
- «…» del corte: Inter Tight 800, 72 px; sobre píldora amarilla, siempre abajo a la derecha
- palabra clave: Instrument Serif 400, 120 px
PORTADA: frase grande alineada a la izquierda (15-60%) mezclando sans extra bold y UNA palabra en serif gigante sobre bloque amarillo redondeado; termina cortada en «…»; la continuación asoma en una píldora amarilla abajo a la derecha (85-92%).
SLIDES DEL MEDIO: abre arriba con «…» completando la anterior, en gris 60%; la nueva frase en negro; termina cortada en el MISMO lugar (píldora abajo a la derecha).
CIERRE: penúltima: la revelación completa, SIN píldora; última: «Comenta» + [PALABRA] en la píldora amarilla.
ELEMENTOS GRÁFICOS: el corte siempre en el mismo sitio · la continuación en gris al abrir cada slide · píldora amarilla como «deuda»
EVITA: frases gancho gastadas («Roba mi sistema»), miniaturas y métricas ajenas.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 90 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~8% a los lados y nada importante en el 9% de abajo.
FONDO: rosa empolvado liso #F7ECE8 en todas.
PALETA (usa SOLO estos colores): #F7ECE8 = fondo · #EDBB4C = amarillo de píldoras y corte · #000000 = tinta
TIPOGRAFÍA:
- frase: estilo Inter Tight (800), letra de ~5% del alto
- «…» del corte: estilo Inter Tight (800), letra de ~5% del alto; sobre píldora amarilla, siempre abajo a la derecha
- palabra clave: estilo Instrument Serif (400), letra de ~9% del alto
COMPOSICIÓN DE ESTA SLIDE: frase grande alineada a la izquierda (15-60%) mezclando sans extra bold y UNA palabra en serif gigante sobre bloque amarillo redondeado; termina cortada en «…»; la continuación asoma en una píldora amarilla abajo a la derecha (85-92%).
ELEMENTOS GRÁFICOS: el corte siempre en el mismo sitio · la continuación en gris al abrir cada slide · píldora amarilla como «deuda»
EVITA: frases gancho gastadas («Roba mi sistema»), miniaturas y métricas ajenas.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: rosa empolvado liso #F7ECE8 en todas.
COMPOSICIÓN: frase grande alineada a la izquierda (15-60%) mezclando sans extra bold y UNA palabra en serif gigante sobre bloque amarillo redondeado; termina cortada en «…»; la continuación asoma en una píldora amarilla abajo a la derecha (85-92%).
ELEMENTOS: el corte siempre en el mismo sitio · la continuación en gris al abrir cada slide · píldora amarilla como «deuda»
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (rosa empolvado liso #F7ECE8 en todas.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: abre arriba con «…» completando la anterior, en gris 60%; la nueva frase en negro; termina cortada en el MISMO lugar (píldora abajo a la derecha).
(Si es la última slide, la composición es: penúltima: la revelación completa, SIN píldora; última: «Comenta» + [PALABRA] en la píldora amarilla.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~8% a los lados y nada importante en el 9% de abajo.
FONDO: rosa empolvado liso #F7ECE8 en todas.
PALETA (usa SOLO estos colores): #F7ECE8 = fondo · #EDBB4C = amarillo de píldoras y corte · #000000 = tinta
TIPOGRAFÍA:
- frase: estilo Inter Tight (800), letra de ~5% del alto
- «…» del corte: estilo Inter Tight (800), letra de ~5% del alto; sobre píldora amarilla, siempre abajo a la derecha
- palabra clave: estilo Instrument Serif (400), letra de ~9% del alto
COMPOSICIÓN DE ESTA SLIDE: frase grande alineada a la izquierda (15-60%) mezclando sans extra bold y UNA palabra en serif gigante sobre bloque amarillo redondeado; termina cortada en «…»; la continuación asoma en una píldora amarilla abajo a la derecha (85-92%).
ELEMENTOS GRÁFICOS: el corte siempre en el mismo sitio · la continuación en gris al abrir cada slide · píldora amarilla como «deuda»
EVITA: frases gancho gastadas («Roba mi sistema»), miniaturas y métricas ajenas.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: rosa empolvado liso #F7ECE8 en todas.
COMPOSICIÓN: frase grande alineada a la izquierda (15-60%) mezclando sans extra bold y UNA palabra en serif gigante sobre bloque amarillo redondeado; termina cortada en «…»; la continuación asoma en una píldora amarilla abajo a la derecha (85-92%).
ELEMENTOS: el corte siempre en el mismo sitio · la continuación en gris al abrir cada slide · píldora amarilla como «deuda»
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (rosa empolvado liso #F7ECE8 en todas.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: abre arriba con «…» completando la anterior, en gris 60%; la nueva frase en negro; termina cortada en el MISMO lugar (píldora abajo a la derecha).
(Si es la última slide, la composición es: penúltima: la revelación completa, SIN píldora; última: «Comenta» + [PALABRA] en la píldora amarilla.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## G10 · Frases sueltas

**Ejemplo:** sin referencia real: la referencia del Grimorio está rota (una sola imagen horizontal hecha con IA, texto ilegible); se busca un ejemplo real


**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 120 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: crema #FAF8F5 liso, mucho aire; la misma composición en todas las frases.
PALETA (usa SOLO estos colores): #FAF8F5 = fondo · #3B2F2F = texto · #C2562B = LA palabra resaltada · #8C7B6B = número y firma
TIPOGRAFÍA:
- frase: Playfair Display 500, 76 px
- palabra resaltada: Playfair Display 600 itálica, 76 px
- número «2/5»: DM Sans 500, 24 px
PORTADA: «[N] frases para cuando [momento]» centrado en el 40% central, con el momento en itálica de color; línea fina decorativa debajo.
SLIDES DEL MEDIO: UNA frase centrada vertical y horizontalmente, máx. 14 palabras, con UNA palabra en itálica de color; número «2/5» arriba a la derecha; tu @ chico abajo al centro.
CIERRE: «¿Con cuál te quedas? Comenta el número».
ELEMENTOS GRÁFICOS: mucho aire (márgenes de 120 px) · una sola palabra de color por frase · línea fina como separador
EVITA: citas de otros autores: las frases tienen que ser tuyas.
```

> Cada slide lleva poco texto (máx. ~14 palabras): el modelo lo puede escribir, pero revisa tildes y eñes letra por letra antes de publicar.

### 1 · Guion (cualquier chat)
```
Escribe 5 frases MÍAS (no citas famosas) para [MI CLIENTE] cuando [MOMENTO DIFÍCIL CONCRETO].
Básate en cosas que he dicho o vivido: [PEGA 3-5 IDEAS O FRASES TUYAS].
Cada frase: máx. 14 palabras, con una imagen concreta (no "cree en ti"), y marca con ==palabra== la ÚNICA palabra que carga el sentido.
Slide 1: "[N] frases para cuando [momento]".
Slide 7: "¿Con cuál te quedas? Comenta el número".
Tutea.
```

### 2 · Claude Code
```
hazme un carrusel tipo G10 (Frases sueltas) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 120 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: crema #FAF8F5 liso, mucho aire; la misma composición en todas las frases.
PALETA (usa SOLO estos colores): #FAF8F5 = fondo · #3B2F2F = texto · #C2562B = LA palabra resaltada · #8C7B6B = número y firma
TIPOGRAFÍA:
- frase: Playfair Display 500, 76 px
- palabra resaltada: Playfair Display 600 itálica, 76 px
- número «2/5»: DM Sans 500, 24 px
PORTADA: «[N] frases para cuando [momento]» centrado en el 40% central, con el momento en itálica de color; línea fina decorativa debajo.
SLIDES DEL MEDIO: UNA frase centrada vertical y horizontalmente, máx. 14 palabras, con UNA palabra en itálica de color; número «2/5» arriba a la derecha; tu @ chico abajo al centro.
CIERRE: «¿Con cuál te quedas? Comenta el número».
ELEMENTOS GRÁFICOS: mucho aire (márgenes de 120 px) · una sola palabra de color por frase · línea fina como separador
EVITA: citas de otros autores: las frases tienen que ser tuyas.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 120 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~11% a los lados y nada importante en el 9% de abajo.
FONDO: crema #FAF8F5 liso, mucho aire; la misma composición en todas las frases.
PALETA (usa SOLO estos colores): #FAF8F5 = fondo · #3B2F2F = texto · #C2562B = LA palabra resaltada · #8C7B6B = número y firma
TIPOGRAFÍA:
- frase: estilo Playfair Display (500), letra de ~6% del alto
- palabra resaltada: estilo Playfair Display (600 itálica), letra de ~6% del alto
- número «2/5»: estilo DM Sans (500), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: «[N] frases para cuando [momento]» centrado en el 40% central, con el momento en itálica de color; línea fina decorativa debajo.
ELEMENTOS GRÁFICOS: mucho aire (márgenes de 120 px) · una sola palabra de color por frase · línea fina como separador
EVITA: citas de otros autores: las frases tienen que ser tuyas.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: crema #FAF8F5 liso, mucho aire; la misma composición en todas las frases.
COMPOSICIÓN: «[N] frases para cuando [momento]» centrado en el 40% central, con el momento en itálica de color; línea fina decorativa debajo.
ELEMENTOS: mucho aire (márgenes de 120 px) · una sola palabra de color por frase · línea fina como separador
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (crema #FAF8F5 liso, mucho aire; la misma composición en todas las frases.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: UNA frase centrada vertical y horizontalmente, máx. 14 palabras, con UNA palabra en itálica de color; número «2/5» arriba a la derecha; tu @ chico abajo al centro.
(Si es la última slide, la composición es: «¿Con cuál te quedas? Comenta el número».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~11% a los lados y nada importante en el 9% de abajo.
FONDO: crema #FAF8F5 liso, mucho aire; la misma composición en todas las frases.
PALETA (usa SOLO estos colores): #FAF8F5 = fondo · #3B2F2F = texto · #C2562B = LA palabra resaltada · #8C7B6B = número y firma
TIPOGRAFÍA:
- frase: estilo Playfair Display (500), letra de ~6% del alto
- palabra resaltada: estilo Playfair Display (600 itálica), letra de ~6% del alto
- número «2/5»: estilo DM Sans (500), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: «[N] frases para cuando [momento]» centrado en el 40% central, con el momento en itálica de color; línea fina decorativa debajo.
ELEMENTOS GRÁFICOS: mucho aire (márgenes de 120 px) · una sola palabra de color por frase · línea fina como separador
EVITA: citas de otros autores: las frases tienen que ser tuyas.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: crema #FAF8F5 liso, mucho aire; la misma composición en todas las frases.
COMPOSICIÓN: «[N] frases para cuando [momento]» centrado en el 40% central, con el momento en itálica de color; línea fina decorativa debajo.
ELEMENTOS: mucho aire (márgenes de 120 px) · una sola palabra de color por frase · línea fina como separador
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (crema #FAF8F5 liso, mucho aire; la misma composición en todas las frases.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: UNA frase centrada vertical y horizontalmente, máx. 14 palabras, con UNA palabra en itálica de color; número «2/5» arriba a la derecha; tu @ chico abajo al centro.
(Si es la última slide, la composición es: «¿Con cuál te quedas? Comenta el número».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## G11 · Errores propios

**Ejemplo:** @tania.villalobosc · https://www.instagram.com/p/Da5tAScFtVQ/ · 113 likes · 7 slides (cazada por mecánica: el Grimorio no tenía ejemplo)

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: tu foto real a sangre, en pausa y no posada (mirando a un lado, con una taza, en tu lugar de trabajo), con degradado negro de abajo hacia arriba del 0% al 75% en la mitad inferior para que el texto se lea.
PALETA (usa SOLO estos colores): #0B0B0B = oscurecido de la foto · #FFFFFF = texto · #FEEB9D = parte clave, etiqueta y garabatos · #111111 = texto de la etiqueta
TIPOGRAFÍA:
- titular de portada: Inter 700, MAYÚSCULAS, 64 px
- confesión: Inter 700, 40 px
- nota al margen: Caveat 700, 34 px
PORTADA: foto tuya real oscurecida; titular MAYÚSCULAS arriba a la izquierda (15-30%) con la palabra «ERRORES» en amarillo pálido + un garabato «✕»; etiqueta amarilla redondeada con texto negro abajo a la izquierda (82-92%) «como [profesión]».
SLIDES DEL MEDIO: foto distinta por error; confesión en 2-3 líneas centrada arriba (10-25%) con la parte clave en amarillo; en el medio la prueba o TÚ RECORTADA con borde blanco tipo sticker; nota al margen chica en blanco con flecha a mano amarilla («uff, me replanteó todo»).
CIERRE: 3 párrafos centrados arriba con palabras en amarillo bold + corazón amarillo + tú recortada con el celular + «¿cuál te sorprendió más?».
ELEMENTOS GRÁFICOS: notas al margen a mano con tu reacción honesta · tú recortada tipo sticker con borde blanco · parte clave en amarillo pálido
EVITA: errores ajenos o genéricos; fotos de banco: tiene que ser tu cara real.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Soy [PROFESIÓN]. Estos son errores reales que cometí cuando empecé: [LISTA con año y qué pasó].
Escribe un carrusel de 7 slides:
Slide 1: "¿Qué errores cometí como [profesión] cuando empecé?".
Slides 2-5: un error por slide → año + situación concreta + qué hice. La parte clave EN MAYÚSCULAS (máx. 5 palabras). Termina con una frase de peso corta.
Slide 6: "Estos errores me dolieron, pero me hicieron mejor. Ojalá alguien me lo hubiera contado antes."
Slide 7: "¿Cuál te sorprendió más?" / "¿Qué hubieras hecho tú?".
No suavices ni conviertas el error en consejo. Máx. 35 palabras por slide. Tutea.
```

### 2 · Claude Code
```
hazme un carrusel tipo G11 (Errores propios) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: tu foto real a sangre, en pausa y no posada (mirando a un lado, con una taza, en tu lugar de trabajo), con degradado negro de abajo hacia arriba del 0% al 75% en la mitad inferior para que el texto se lea.
PALETA (usa SOLO estos colores): #0B0B0B = oscurecido de la foto · #FFFFFF = texto · #FEEB9D = parte clave, etiqueta y garabatos · #111111 = texto de la etiqueta
TIPOGRAFÍA:
- titular de portada: Inter 700, MAYÚSCULAS, 64 px
- confesión: Inter 700, 40 px
- nota al margen: Caveat 700, 34 px
PORTADA: foto tuya real oscurecida; titular MAYÚSCULAS arriba a la izquierda (15-30%) con la palabra «ERRORES» en amarillo pálido + un garabato «✕»; etiqueta amarilla redondeada con texto negro abajo a la izquierda (82-92%) «como [profesión]».
SLIDES DEL MEDIO: foto distinta por error; confesión en 2-3 líneas centrada arriba (10-25%) con la parte clave en amarillo; en el medio la prueba o TÚ RECORTADA con borde blanco tipo sticker; nota al margen chica en blanco con flecha a mano amarilla («uff, me replanteó todo»).
CIERRE: 3 párrafos centrados arriba con palabras en amarillo bold + corazón amarillo + tú recortada con el celular + «¿cuál te sorprendió más?».
ELEMENTOS GRÁFICOS: notas al margen a mano con tu reacción honesta · tú recortada tipo sticker con borde blanco · parte clave en amarillo pálido
EVITA: errores ajenos o genéricos; fotos de banco: tiene que ser tu cara real.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 80 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: tu foto real a sangre, en pausa y no posada (mirando a un lado, con una taza, en tu lugar de trabajo), con degradado negro de abajo hacia arriba del 0% al 75% en la mitad inferior para que el texto se lea.
PALETA (usa SOLO estos colores): #0B0B0B = oscurecido de la foto · #FFFFFF = texto · #FEEB9D = parte clave, etiqueta y garabatos · #111111 = texto de la etiqueta
TIPOGRAFÍA:
- titular de portada: estilo Inter (700), MAYÚSCULAS, letra de ~5% del alto
- confesión: estilo Inter (700), letra de ~3% del alto
- nota al margen: estilo Caveat (700), letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: foto tuya real oscurecida; titular MAYÚSCULAS arriba a la izquierda (15-30%) con la palabra «ERRORES» en amarillo pálido + un garabato «✕»; etiqueta amarilla redondeada con texto negro abajo a la izquierda (82-92%) «como [profesión]».
ELEMENTOS GRÁFICOS: notas al margen a mano con tu reacción honesta · tú recortada tipo sticker con borde blanco · parte clave en amarillo pálido
EVITA: errores ajenos o genéricos; fotos de banco: tiene que ser tu cara real.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: tu foto real a sangre, en pausa y no posada (mirando a un lado, con una taza, en tu lugar de trabajo), con degradado negro de abajo hacia arriba del 0% al 75% en la mitad inferior para que el texto se lea.
COMPOSICIÓN: foto tuya real oscurecida; titular MAYÚSCULAS arriba a la izquierda (15-30%) con la palabra «ERRORES» en amarillo pálido + un garabato «✕»; etiqueta amarilla redondeada con texto negro abajo a la izquierda (82-92%) «como [profesión]».
ELEMENTOS: notas al margen a mano con tu reacción honesta · tú recortada tipo sticker con borde blanco · parte clave en amarillo pálido
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: lleva tus fotos o capturas reales (tu foto real a sangre, en pausa y no posada (mirando a un lado, con una taza, en tu lugar de trabajo), con degradado negro de abajo hacia arriba del 0% al 75% en la mitad inferior para que el texto se lea.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: foto distinta por error; confesión en 2-3 líneas centrada arriba (10-25%) con la parte clave en amarillo; en el medio la prueba o TÚ RECORTADA con borde blanco tipo sticker; nota al margen chica en blanco con flecha a mano amarilla («uff, me replanteó todo»).
(Si es la última slide, la composición es: 3 párrafos centrados arriba con palabras en amarillo bold + corazón amarillo + tú recortada con el celular + «¿cuál te sorprendió más?».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: tu foto real a sangre, en pausa y no posada (mirando a un lado, con una taza, en tu lugar de trabajo), con degradado negro de abajo hacia arriba del 0% al 75% en la mitad inferior para que el texto se lea.
PALETA (usa SOLO estos colores): #0B0B0B = oscurecido de la foto · #FFFFFF = texto · #FEEB9D = parte clave, etiqueta y garabatos · #111111 = texto de la etiqueta
TIPOGRAFÍA:
- titular de portada: estilo Inter (700), MAYÚSCULAS, letra de ~5% del alto
- confesión: estilo Inter (700), letra de ~3% del alto
- nota al margen: estilo Caveat (700), letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: foto tuya real oscurecida; titular MAYÚSCULAS arriba a la izquierda (15-30%) con la palabra «ERRORES» en amarillo pálido + un garabato «✕»; etiqueta amarilla redondeada con texto negro abajo a la izquierda (82-92%) «como [profesión]».
ELEMENTOS GRÁFICOS: notas al margen a mano con tu reacción honesta · tú recortada tipo sticker con borde blanco · parte clave en amarillo pálido
EVITA: errores ajenos o genéricos; fotos de banco: tiene que ser tu cara real.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: tu foto real a sangre, en pausa y no posada (mirando a un lado, con una taza, en tu lugar de trabajo), con degradado negro de abajo hacia arriba del 0% al 75% en la mitad inferior para que el texto se lea.
COMPOSICIÓN: foto tuya real oscurecida; titular MAYÚSCULAS arriba a la izquierda (15-30%) con la palabra «ERRORES» en amarillo pálido + un garabato «✕»; etiqueta amarilla redondeada con texto negro abajo a la izquierda (82-92%) «como [profesión]».
ELEMENTOS: notas al margen a mano con tu reacción honesta · tú recortada tipo sticker con borde blanco · parte clave en amarillo pálido
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: lleva tus fotos o capturas reales (tu foto real a sangre, en pausa y no posada (mirando a un lado, con una taza, en tu lugar de trabajo), con degradado negro de abajo hacia arriba del 0% al 75% en la mitad inferior para que el texto se lea.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: foto distinta por error; confesión en 2-3 líneas centrada arriba (10-25%) con la parte clave en amarillo; en el medio la prueba o TÚ RECORTADA con borde blanco tipo sticker; nota al margen chica en blanco con flecha a mano amarilla («uff, me replanteó todo»).
(Si es la última slide, la composición es: 3 párrafos centrados arriba con palabras en amarillo bold + corazón amarillo + tú recortada con el celular + «¿cuál te sorprendió más?».)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## G12 · Confesión a partir de una pregunta

**Ejemplo:** sin referencia real: el Grimorio no tiene ejemplo público verificado; se busca uno real


**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 64 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: portada: pantalla de chat (fondo #EDE6DC, barra superior #1F2C34); slides de respuesta: nota del celular color crema #FFFDF4 con la barra amarilla de «Notas» arriba.
PALETA (usa SOLO estos colores): #EDE6DC = fondo del chat · #1F2C34 = barra del chat · #FFFFFF = burbuja de la pregunta · #FFFDF4 = hoja de nota · #1C1C1E = texto · #FFD60A = acento de la app de notas · #8E8E93 = hora y fecha
TIPOGRAFÍA:
- pregunta en burbuja: Inter 500, 54 px
- título de la nota: Inter 700, 60 px
- cuerpo de la nota: Inter 400, 44 px; interlineado 1.45, como texto escrito de corrido
PORTADA: chat con UNA burbuja blanca a la izquierda con la pregunta tal cual (54 px), hora debajo; en la barra, «[quién] · ayer»; debajo del chat, fuera de la burbuja, «y me hizo pensar…» en gris.
SLIDES DEL MEDIO: nota del celular: fecha gris arriba («ayer, 23:14»), título corto en negrita y el cuerpo en primera persona de corrido; ninguna decoración más. En la slide de aprendizaje, los 2 consejos numerados como lista de la nota.
CIERRE: nota con 3 preguntas abiertas en lista, cada una en su línea, y el cursor parpadeando al final.
ELEMENTOS GRÁFICOS: chat solo en la portada; notas en el resto · sin logos de WhatsApp ni de Apple · cursor de texto al final de la última línea
EVITA: el nombre o la foto de quien preguntó: usa su rol («mi paciente», «una alumna»).
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Ayer [QUIÉN: paciente/clienta/alumna] me preguntó: "[PREGUNTA ÍNTIMA SOBRE MI OFICIO]". La verdad es: [TU RESPUESTA HONESTA, sin pulir].
Escribe un carrusel de 7 slides:
Slide 1: la pregunta tal cual, como mensaje recibido (máx. 15 palabras) + "y me hizo pensar…".
Slides 2-4: mi respuesta honesta en primera persona, con una escena cotidiana concreta (máx. 30 palabras por slide).
Slide 5: "Y entiendo que te sientas así, porque [objeción común de mi rubro]".
Slide 6: 2 consejos numerados que salen de lo que conté.
Slide 7: 3 preguntas abiertas: "¿te ha pasado?", "¿qué le dirías a alguien así?", [una propia].
Tutea.
```

### 2 · Claude Code
```
hazme un carrusel tipo G12 (Confesión a partir de una pregunta) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 64 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: portada: pantalla de chat (fondo #EDE6DC, barra superior #1F2C34); slides de respuesta: nota del celular color crema #FFFDF4 con la barra amarilla de «Notas» arriba.
PALETA (usa SOLO estos colores): #EDE6DC = fondo del chat · #1F2C34 = barra del chat · #FFFFFF = burbuja de la pregunta · #FFFDF4 = hoja de nota · #1C1C1E = texto · #FFD60A = acento de la app de notas · #8E8E93 = hora y fecha
TIPOGRAFÍA:
- pregunta en burbuja: Inter 500, 54 px
- título de la nota: Inter 700, 60 px
- cuerpo de la nota: Inter 400, 44 px; interlineado 1.45, como texto escrito de corrido
PORTADA: chat con UNA burbuja blanca a la izquierda con la pregunta tal cual (54 px), hora debajo; en la barra, «[quién] · ayer»; debajo del chat, fuera de la burbuja, «y me hizo pensar…» en gris.
SLIDES DEL MEDIO: nota del celular: fecha gris arriba («ayer, 23:14»), título corto en negrita y el cuerpo en primera persona de corrido; ninguna decoración más. En la slide de aprendizaje, los 2 consejos numerados como lista de la nota.
CIERRE: nota con 3 preguntas abiertas en lista, cada una en su línea, y el cursor parpadeando al final.
ELEMENTOS GRÁFICOS: chat solo en la portada; notas en el resto · sin logos de WhatsApp ni de Apple · cursor de texto al final de la última línea
EVITA: el nombre o la foto de quien preguntó: usa su rol («mi paciente», «una alumna»).

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 64 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: portada: pantalla de chat (fondo #EDE6DC, barra superior #1F2C34); slides de respuesta: nota del celular color crema #FFFDF4 con la barra amarilla de «Notas» arriba.
PALETA (usa SOLO estos colores): #EDE6DC = fondo del chat · #1F2C34 = barra del chat · #FFFFFF = burbuja de la pregunta · #FFFDF4 = hoja de nota · #1C1C1E = texto · #FFD60A = acento de la app de notas · #8E8E93 = hora y fecha
TIPOGRAFÍA:
- pregunta en burbuja: estilo Inter (500), letra de ~4% del alto
- título de la nota: estilo Inter (700), letra de ~4% del alto
- cuerpo de la nota: estilo Inter (400), letra de ~3% del alto; interlineado 1.45, como texto escrito de corrido
COMPOSICIÓN DE ESTA SLIDE: chat con UNA burbuja blanca a la izquierda con la pregunta tal cual (54 px), hora debajo; en la barra, «[quién] · ayer»; debajo del chat, fuera de la burbuja, «y me hizo pensar…» en gris.
ELEMENTOS GRÁFICOS: chat solo en la portada; notas en el resto · sin logos de WhatsApp ni de Apple · cursor de texto al final de la última línea
EVITA: el nombre o la foto de quien preguntó: usa su rol («mi paciente», «una alumna»).
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: portada: pantalla de chat (fondo #EDE6DC, barra superior #1F2C34); slides de respuesta: nota del celular color crema #FFFDF4 con la barra amarilla de «Notas» arriba.
COMPOSICIÓN: chat con UNA burbuja blanca a la izquierda con la pregunta tal cual (54 px), hora debajo; en la barra, «[quién] · ayer»; debajo del chat, fuera de la burbuja, «y me hizo pensar…» en gris.
ELEMENTOS: chat solo en la portada; notas en el resto · sin logos de WhatsApp ni de Apple · cursor de texto al final de la última línea
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (portada: pantalla de chat (fondo #EDE6DC, barra superior #1F2C34); slides de respuesta: nota del celular color crema #FFFDF4 con la barra amarilla de «Notas» arriba.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: nota del celular: fecha gris arriba («ayer, 23:14»), título corto en negrita y el cuerpo en primera persona de corrido; ninguna decoración más. En la slide de aprendizaje, los 2 consejos numerados como lista de la nota.
(Si es la última slide, la composición es: nota con 3 preguntas abiertas en lista, cada una en su línea, y el cursor parpadeando al final.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: portada: pantalla de chat (fondo #EDE6DC, barra superior #1F2C34); slides de respuesta: nota del celular color crema #FFFDF4 con la barra amarilla de «Notas» arriba.
PALETA (usa SOLO estos colores): #EDE6DC = fondo del chat · #1F2C34 = barra del chat · #FFFFFF = burbuja de la pregunta · #FFFDF4 = hoja de nota · #1C1C1E = texto · #FFD60A = acento de la app de notas · #8E8E93 = hora y fecha
TIPOGRAFÍA:
- pregunta en burbuja: estilo Inter (500), letra de ~4% del alto
- título de la nota: estilo Inter (700), letra de ~4% del alto
- cuerpo de la nota: estilo Inter (400), letra de ~3% del alto; interlineado 1.45, como texto escrito de corrido
COMPOSICIÓN DE ESTA SLIDE: chat con UNA burbuja blanca a la izquierda con la pregunta tal cual (54 px), hora debajo; en la barra, «[quién] · ayer»; debajo del chat, fuera de la burbuja, «y me hizo pensar…» en gris.
ELEMENTOS GRÁFICOS: chat solo en la portada; notas en el resto · sin logos de WhatsApp ni de Apple · cursor de texto al final de la última línea
EVITA: el nombre o la foto de quien preguntó: usa su rol («mi paciente», «una alumna»).
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: portada: pantalla de chat (fondo #EDE6DC, barra superior #1F2C34); slides de respuesta: nota del celular color crema #FFFDF4 con la barra amarilla de «Notas» arriba.
COMPOSICIÓN: chat con UNA burbuja blanca a la izquierda con la pregunta tal cual (54 px), hora debajo; en la barra, «[quién] · ayer»; debajo del chat, fuera de la burbuja, «y me hizo pensar…» en gris.
ELEMENTOS: chat solo en la portada; notas en el resto · sin logos de WhatsApp ni de Apple · cursor de texto al final de la última línea
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (portada: pantalla de chat (fondo #EDE6DC, barra superior #1F2C34); slides de respuesta: nota del celular color crema #FFFDF4 con la barra amarilla de «Notas» arriba.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: nota del celular: fecha gris arriba («ayer, 23:14»), título corto en negrita y el cuerpo en primera persona de corrido; ninguna decoración más. En la slide de aprendizaje, los 2 consejos numerados como lista de la nota.
(Si es la última slide, la composición es: nota con 3 preguntas abiertas en lista, cada una en su línea, y el cursor parpadeando al final.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## G13 · De A a B con antesala

**Ejemplo:** sin referencia real: el Grimorio no tiene ejemplo público verificado; se busca uno real


**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: neutro claro #FAFAFA en todas las slides; la antesala (slides 2-4) en crema #F5F0E8 para que se note que todavía no empiezan los pasos.
PALETA (usa SOLO estos colores): #FAFAFA = fondo de los pasos · #F5F0E8 = fondo de la antesala · #18181B = texto · #6D28D9 = acento: barra, chip del paso · #E4E4E7 = barra vacía · #71717A = texto de apoyo
TIPOGRAFÍA:
- título: Inter 800, 84 px
- chip «Paso 2 de 4»: Inter 700, MAYÚSCULAS, espaciado 0.12em, 30 px
- apoyo: Inter 500, 42 px
PORTADA: arriba «De [A]» en gris y abajo «a [B]» en negro ultra bold, unidos por una línea vertical violeta con dos nodos; «una guía realista, sin hacks mágicos» chico al pie.
SLIDES DEL MEDIO: PASOS: barra de progreso de 16 px arriba a lo ancho que se llena 25% → 50% → 75% → 100% + chip violeta «PASO N DE 4»; título en el tercio superior; «cómo sabes que lo hiciste bien» en gris debajo. ANTESALA (validación, razones, a quién le sirve): fondo crema, SIN barra — la barra aparece recién en el paso 1.
CIERRE: barra al 100% + «No necesitas hacerlo perfecto» + la acción pequeña en un recuadro violeta claro + CTA de palabra clave.
ELEMENTOS GRÁFICOS: la barra NO aparece en la antesala · stepper de 4 nodos en la slide de reencuadre · un solo color de acento en todo el carrusel
EVITA: promesas de tiempo que no puedes sostener («en 30 días»).
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Escribe un carrusel "Cómo ir de [PROBLEMA FRECUENTE] a [RESULTADO DESEADO]" de 10 slides para [MI CLIENTE].
Slide 1: el título + "una guía realista, sin hacks mágicos".
Slide 2: "Esto es lo más difícil del proceso: [emoción concreta]".
Slide 3: 3 razones por las que le cuesta a la mayoría. Ninguna culpa al lector.
Slide 4: "Esta guía funciona mejor si estás en [situación inicial]". Di a quién NO le sirve.
Slides 5-8: un paso por slide → "Paso N de 4" + acción ultra específica (máx. 12 palabras) + cómo sabes que lo hiciste bien.
Slide 9: "No necesitas hacerlo perfecto: empieza con [acción pequeña] y repítela [tiempo]".
Slide 10: "Comenta [PALABRA] y te mando [recurso]".
Tutea.
```

### 2 · Claude Code
```
hazme un carrusel tipo G13 (De A a B con antesala) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: neutro claro #FAFAFA en todas las slides; la antesala (slides 2-4) en crema #F5F0E8 para que se note que todavía no empiezan los pasos.
PALETA (usa SOLO estos colores): #FAFAFA = fondo de los pasos · #F5F0E8 = fondo de la antesala · #18181B = texto · #6D28D9 = acento: barra, chip del paso · #E4E4E7 = barra vacía · #71717A = texto de apoyo
TIPOGRAFÍA:
- título: Inter 800, 84 px
- chip «Paso 2 de 4»: Inter 700, MAYÚSCULAS, espaciado 0.12em, 30 px
- apoyo: Inter 500, 42 px
PORTADA: arriba «De [A]» en gris y abajo «a [B]» en negro ultra bold, unidos por una línea vertical violeta con dos nodos; «una guía realista, sin hacks mágicos» chico al pie.
SLIDES DEL MEDIO: PASOS: barra de progreso de 16 px arriba a lo ancho que se llena 25% → 50% → 75% → 100% + chip violeta «PASO N DE 4»; título en el tercio superior; «cómo sabes que lo hiciste bien» en gris debajo. ANTESALA (validación, razones, a quién le sirve): fondo crema, SIN barra — la barra aparece recién en el paso 1.
CIERRE: barra al 100% + «No necesitas hacerlo perfecto» + la acción pequeña en un recuadro violeta claro + CTA de palabra clave.
ELEMENTOS GRÁFICOS: la barra NO aparece en la antesala · stepper de 4 nodos en la slide de reencuadre · un solo color de acento en todo el carrusel
EVITA: promesas de tiempo que no puedes sostener («en 30 días»).

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 80 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: neutro claro #FAFAFA en todas las slides; la antesala (slides 2-4) en crema #F5F0E8 para que se note que todavía no empiezan los pasos.
PALETA (usa SOLO estos colores): #FAFAFA = fondo de los pasos · #F5F0E8 = fondo de la antesala · #18181B = texto · #6D28D9 = acento: barra, chip del paso · #E4E4E7 = barra vacía · #71717A = texto de apoyo
TIPOGRAFÍA:
- título: estilo Inter (800), letra de ~6% del alto
- chip «Paso 2 de 4»: estilo Inter (700), MAYÚSCULAS, espaciado 0.12em, letra de ~2% del alto
- apoyo: estilo Inter (500), letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: arriba «De [A]» en gris y abajo «a [B]» en negro ultra bold, unidos por una línea vertical violeta con dos nodos; «una guía realista, sin hacks mágicos» chico al pie.
ELEMENTOS GRÁFICOS: la barra NO aparece en la antesala · stepper de 4 nodos en la slide de reencuadre · un solo color de acento en todo el carrusel
EVITA: promesas de tiempo que no puedes sostener («en 30 días»).
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: neutro claro #FAFAFA en todas las slides; la antesala (slides 2-4) en crema #F5F0E8 para que se note que todavía no empiezan los pasos.
COMPOSICIÓN: arriba «De [A]» en gris y abajo «a [B]» en negro ultra bold, unidos por una línea vertical violeta con dos nodos; «una guía realista, sin hacks mágicos» chico al pie.
ELEMENTOS: la barra NO aparece en la antesala · stepper de 4 nodos en la slide de reencuadre · un solo color de acento en todo el carrusel
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (neutro claro #FAFAFA en todas las slides; la antesala (slides 2-4) en crema #F5F0E8 para que se note que todavía no empiezan los pasos.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: PASOS: barra de progreso de 16 px arriba a lo ancho que se llena 25% → 50% → 75% → 100% + chip violeta «PASO N DE 4»; título en el tercio superior; «cómo sabes que lo hiciste bien» en gris debajo. ANTESALA (validación, razones, a quién le sirve): fondo crema, SIN barra — la barra aparece recién en el paso 1.
(Si es la última slide, la composición es: barra al 100% + «No necesitas hacerlo perfecto» + la acción pequeña en un recuadro violeta claro + CTA de palabra clave.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: neutro claro #FAFAFA en todas las slides; la antesala (slides 2-4) en crema #F5F0E8 para que se note que todavía no empiezan los pasos.
PALETA (usa SOLO estos colores): #FAFAFA = fondo de los pasos · #F5F0E8 = fondo de la antesala · #18181B = texto · #6D28D9 = acento: barra, chip del paso · #E4E4E7 = barra vacía · #71717A = texto de apoyo
TIPOGRAFÍA:
- título: estilo Inter (800), letra de ~6% del alto
- chip «Paso 2 de 4»: estilo Inter (700), MAYÚSCULAS, espaciado 0.12em, letra de ~2% del alto
- apoyo: estilo Inter (500), letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: arriba «De [A]» en gris y abajo «a [B]» en negro ultra bold, unidos por una línea vertical violeta con dos nodos; «una guía realista, sin hacks mágicos» chico al pie.
ELEMENTOS GRÁFICOS: la barra NO aparece en la antesala · stepper de 4 nodos en la slide de reencuadre · un solo color de acento en todo el carrusel
EVITA: promesas de tiempo que no puedes sostener («en 30 días»).
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: neutro claro #FAFAFA en todas las slides; la antesala (slides 2-4) en crema #F5F0E8 para que se note que todavía no empiezan los pasos.
COMPOSICIÓN: arriba «De [A]» en gris y abajo «a [B]» en negro ultra bold, unidos por una línea vertical violeta con dos nodos; «una guía realista, sin hacks mágicos» chico al pie.
ELEMENTOS: la barra NO aparece en la antesala · stepper de 4 nodos en la slide de reencuadre · un solo color de acento en todo el carrusel
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (neutro claro #FAFAFA en todas las slides; la antesala (slides 2-4) en crema #F5F0E8 para que se note que todavía no empiezan los pasos.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: PASOS: barra de progreso de 16 px arriba a lo ancho que se llena 25% → 50% → 75% → 100% + chip violeta «PASO N DE 4»; título en el tercio superior; «cómo sabes que lo hiciste bien» en gris debajo. ANTESALA (validación, razones, a quién le sirve): fondo crema, SIN barra — la barra aparece recién en el paso 1.
(Si es la última slide, la composición es: barra al 100% + «No necesitas hacerlo perfecto» + la acción pequeña en un recuadro violeta claro + CTA de palabra clave.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## G14 · Antes / después

**Ejemplo:** @isabellaescobar · https://www.instagram.com/p/DXXrlp5jaRw/ · ≈16.061 likes · 4 slides (alternativa de servicio: @clinicaaeon.cl https://www.instagram.com/p/DZKj2b-jqWJ/) (cazada por mecánica)

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 60 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: dos fotos REALES apiladas 50/50 a sangre que muestran LA MISMA COSA en dos momentos (cocina casera ↔ cocina industrial, bolsita con sticker ↔ empaque de marca).
PALETA (usa SOLO estos colores): #4F7A93 = píldora azul acero · #FFFFFF = texto
TIPOGRAFÍA:
- rótulo: Oswald 600, MAYÚSCULAS, 36 px
PORTADA: arriba la foto del comienzo con la píldora «PRIMERO EMPIEZAS» centrada a ~47% del alto; abajo la foto de hoy con «LUEGO MEJORAS» a ~75%.
SLIDES DEL MEDIO: el MISMO rótulo en todas; solo cambian los pares de fotos (mismo tema, dos momentos). Variante servicio: split vertical con línea blanca, «ANTES» / «DESPUÉS» en píldoras con borde abajo y etiquetas de zona con líneas guía finas.
CIERRE: el par más fuerte + pregunta («¿qué te pareció el cambio?») o CTA.
ELEMENTOS GRÁFICOS: rótulo idéntico en todas (anáfora visual) · la foto fea del inicio es la que conecta · pares con el mismo encuadre de tema
EVITA: fotos sin consentimiento escrito; en salud o estética no prometas resultados.
```

> Cada slide lleva poco texto (máx. ~6 palabras): el modelo lo puede escribir, pero revisa tildes y eñes letra por letra antes de publicar.

### 1 · Guion (cualquier chat)
```
Tengo estos pares de fotos REALES de mi negocio: [LISTA: foto del inicio → foto de hoy, del mismo tema].
Arma un carrusel antes/después de [4-6] slides:
Rótulo fijo para todas (máx. 3 palabras arriba y 3 abajo): propón 3 opciones del tipo "PRIMERO EMPIEZAS / LUEGO MEJORAS" que suenen a mí.
Slides: un par por slide, ordenados del cambio más pequeño al más impactante. Para cada uno dime qué foto va arriba y cuál abajo, y que ambas muestren LA MISMA COSA.
Si el cambio se mide (ventas, clientas, seguidores): una slide en doble paleta con ANTES [dato] / DESPUÉS [dato] + qué captura lo prueba.
Última slide: "¿qué te pareció el cambio?" o CTA a [servicio].
Usa solo fotos y datos reales. Tutea.
```

### 2 · Claude Code
```
hazme un carrusel tipo G14 (Antes / después) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 60 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: dos fotos REALES apiladas 50/50 a sangre que muestran LA MISMA COSA en dos momentos (cocina casera ↔ cocina industrial, bolsita con sticker ↔ empaque de marca).
PALETA (usa SOLO estos colores): #4F7A93 = píldora azul acero · #FFFFFF = texto
TIPOGRAFÍA:
- rótulo: Oswald 600, MAYÚSCULAS, 36 px
PORTADA: arriba la foto del comienzo con la píldora «PRIMERO EMPIEZAS» centrada a ~47% del alto; abajo la foto de hoy con «LUEGO MEJORAS» a ~75%.
SLIDES DEL MEDIO: el MISMO rótulo en todas; solo cambian los pares de fotos (mismo tema, dos momentos). Variante servicio: split vertical con línea blanca, «ANTES» / «DESPUÉS» en píldoras con borde abajo y etiquetas de zona con líneas guía finas.
CIERRE: el par más fuerte + pregunta («¿qué te pareció el cambio?») o CTA.
ELEMENTOS GRÁFICOS: rótulo idéntico en todas (anáfora visual) · la foto fea del inicio es la que conecta · pares con el mismo encuadre de tema
EVITA: fotos sin consentimiento escrito; en salud o estética no prometas resultados.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 60 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: dos fotos REALES apiladas 50/50 a sangre que muestran LA MISMA COSA en dos momentos (cocina casera ↔ cocina industrial, bolsita con sticker ↔ empaque de marca).
PALETA (usa SOLO estos colores): #4F7A93 = píldora azul acero · #FFFFFF = texto
TIPOGRAFÍA:
- rótulo: estilo Oswald (600), MAYÚSCULAS, letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: arriba la foto del comienzo con la píldora «PRIMERO EMPIEZAS» centrada a ~47% del alto; abajo la foto de hoy con «LUEGO MEJORAS» a ~75%.
ELEMENTOS GRÁFICOS: rótulo idéntico en todas (anáfora visual) · la foto fea del inicio es la que conecta · pares con el mismo encuadre de tema
EVITA: fotos sin consentimiento escrito; en salud o estética no prometas resultados.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: dos fotos REALES apiladas 50/50 a sangre que muestran LA MISMA COSA en dos momentos (cocina casera ↔ cocina industrial, bolsita con sticker ↔ empaque de marca).
COMPOSICIÓN: arriba la foto del comienzo con la píldora «PRIMERO EMPIEZAS» centrada a ~47% del alto; abajo la foto de hoy con «LUEGO MEJORAS» a ~75%.
ELEMENTOS: rótulo idéntico en todas (anáfora visual) · la foto fea del inicio es la que conecta · pares con el mismo encuadre de tema
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: lleva tus fotos o capturas reales (dos fotos REALES apiladas 50/50 a sangre que muestran LA MISMA COSA en dos momentos (cocina casera ↔ cocina industrial, bolsita con sticker ↔ empaque de marca).)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: el MISMO rótulo en todas; solo cambian los pares de fotos (mismo tema, dos momentos). Variante servicio: split vertical con línea blanca, «ANTES» / «DESPUÉS» en píldoras con borde abajo y etiquetas de zona con líneas guía finas.
(Si es la última slide, la composición es: el par más fuerte + pregunta («¿qué te pareció el cambio?») o CTA.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~6% a los lados y nada importante en el 9% de abajo.
FONDO: dos fotos REALES apiladas 50/50 a sangre que muestran LA MISMA COSA en dos momentos (cocina casera ↔ cocina industrial, bolsita con sticker ↔ empaque de marca).
PALETA (usa SOLO estos colores): #4F7A93 = píldora azul acero · #FFFFFF = texto
TIPOGRAFÍA:
- rótulo: estilo Oswald (600), MAYÚSCULAS, letra de ~3% del alto
COMPOSICIÓN DE ESTA SLIDE: arriba la foto del comienzo con la píldora «PRIMERO EMPIEZAS» centrada a ~47% del alto; abajo la foto de hoy con «LUEGO MEJORAS» a ~75%.
ELEMENTOS GRÁFICOS: rótulo idéntico en todas (anáfora visual) · la foto fea del inicio es la que conecta · pares con el mismo encuadre de tema
EVITA: fotos sin consentimiento escrito; en salud o estética no prometas resultados.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: dos fotos REALES apiladas 50/50 a sangre que muestran LA MISMA COSA en dos momentos (cocina casera ↔ cocina industrial, bolsita con sticker ↔ empaque de marca).
COMPOSICIÓN: arriba la foto del comienzo con la píldora «PRIMERO EMPIEZAS» centrada a ~47% del alto; abajo la foto de hoy con «LUEGO MEJORAS» a ~75%.
ELEMENTOS: rótulo idéntico en todas (anáfora visual) · la foto fea del inicio es la que conecta · pares con el mismo encuadre de tema
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: lleva tus fotos o capturas reales (dos fotos REALES apiladas 50/50 a sangre que muestran LA MISMA COSA en dos momentos (cocina casera ↔ cocina industrial, bolsita con sticker ↔ empaque de marca).)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: el MISMO rótulo en todas; solo cambian los pares de fotos (mismo tema, dos momentos). Variante servicio: split vertical con línea blanca, «ANTES» / «DESPUÉS» en píldoras con borde abajo y etiquetas de zona con líneas guía finas.
(Si es la última slide, la composición es: el par más fuerte + pregunta («¿qué te pareció el cambio?») o CTA.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## G15 · Preguntas frecuentes en chat

**Ejemplo:** @taboadanunez.dental · https://www.instagram.com/p/DW6k_ktEWgT/ · 6 slides · pocas métricas: molde de mecánica, no prueba de rendimiento (cazada por mecánica; usa burbuja de diálogo sobre un objeto del rubro, no una pantalla de chat)

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 56 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: pantalla de chat: fondo #EDE6DC con patrón de garabatos al 6% de opacidad, barra superior #1F2C34 con avatar y nombre.
PALETA (usa SOLO estos colores): #EDE6DC = fondo del chat · #1F2C34 = barra superior · #FFFFFF = burbuja de la clienta · #D9FDD3 = burbuja tuya (o tu color de marca al 20%) · #111111 = texto · #8696A0 = hora y vistos
TIPOGRAFÍA:
- texto de burbujas: Inter 400, 46 px
- nombre del chat: Inter 600, 40 px
- hora: Inter 400, 24 px
PORTADA: barra superior con «Preguntas antes de comprar»; una burbuja grande tuya centrada con el titular «Las 5 preguntas que me hacen antes de [comprar]» en 64 px; indicador «escribiendo…» debajo.
SLIDES DEL MEDIO: burbuja blanca a la izquierda con la pregunta tal cual (esquina superior izquierda en punta) + burbuja verde a la derecha con tu respuesta (esquina superior derecha en punta); hora abajo a la derecha de cada burbuja y ✓✓ azules en la tuya; contador «2/5» en la barra. VARIANTE: sobre papel texturizado claro, un objeto de tu rubro (portapapeles, libreta) con la pregunta en una burbuja de diálogo de tu color en MAYÚSCULAS blancas y la respuesta debajo que arranca con «No.» / «Sí.» en itálica bold.
CIERRE: burbuja tuya: «¿Tienes otra? Escríbeme [PALABRA] por DM» + campo de escribir abajo con la palabra ya escrita.
ELEMENTOS GRÁFICOS: avatar circular sin foto de terceros · hora y ✓✓ en cada mensaje · máx. 2 burbujas por slide para que se lea a 46 px · la respuesta arranca con No/Sí en itálica bold
EVITA: logos de WhatsApp o Instagram y nombres reales de clientas: usa «Clienta» o iniciales con permiso.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Estas son preguntas REALES que me llegan por DM antes de comprar [MI OFERTA]: [PEGA 5 MENSAJES tal cual].
Escribe un carrusel de 7 slides en formato chat:
Slide 1: "Las 5 preguntas que me hacen antes de [comprar/agendar]".
Slides 2-6: una por slide → burbuja cliente (la pregunta con sus palabras, máx. 20) + burbuja mía (respuesta honesta, máx. 35 palabras, sin evadir precio ni tiempos). Pon hora a cada mensaje.
Slide 7: "¿Tienes otra? Escríbeme [PALABRA] por DM".
Tutea.
```

### 2 · Claude Code
```
hazme un carrusel tipo G15 (Preguntas frecuentes en chat) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 56 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: pantalla de chat: fondo #EDE6DC con patrón de garabatos al 6% de opacidad, barra superior #1F2C34 con avatar y nombre.
PALETA (usa SOLO estos colores): #EDE6DC = fondo del chat · #1F2C34 = barra superior · #FFFFFF = burbuja de la clienta · #D9FDD3 = burbuja tuya (o tu color de marca al 20%) · #111111 = texto · #8696A0 = hora y vistos
TIPOGRAFÍA:
- texto de burbujas: Inter 400, 46 px
- nombre del chat: Inter 600, 40 px
- hora: Inter 400, 24 px
PORTADA: barra superior con «Preguntas antes de comprar»; una burbuja grande tuya centrada con el titular «Las 5 preguntas que me hacen antes de [comprar]» en 64 px; indicador «escribiendo…» debajo.
SLIDES DEL MEDIO: burbuja blanca a la izquierda con la pregunta tal cual (esquina superior izquierda en punta) + burbuja verde a la derecha con tu respuesta (esquina superior derecha en punta); hora abajo a la derecha de cada burbuja y ✓✓ azules en la tuya; contador «2/5» en la barra. VARIANTE: sobre papel texturizado claro, un objeto de tu rubro (portapapeles, libreta) con la pregunta en una burbuja de diálogo de tu color en MAYÚSCULAS blancas y la respuesta debajo que arranca con «No.» / «Sí.» en itálica bold.
CIERRE: burbuja tuya: «¿Tienes otra? Escríbeme [PALABRA] por DM» + campo de escribir abajo con la palabra ya escrita.
ELEMENTOS GRÁFICOS: avatar circular sin foto de terceros · hora y ✓✓ en cada mensaje · máx. 2 burbujas por slide para que se lea a 46 px · la respuesta arranca con No/Sí en itálica bold
EVITA: logos de WhatsApp o Instagram y nombres reales de clientas: usa «Clienta» o iniciales con permiso.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 56 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~5% a los lados y nada importante en el 9% de abajo.
FONDO: pantalla de chat: fondo #EDE6DC con patrón de garabatos al 6% de opacidad, barra superior #1F2C34 con avatar y nombre.
PALETA (usa SOLO estos colores): #EDE6DC = fondo del chat · #1F2C34 = barra superior · #FFFFFF = burbuja de la clienta · #D9FDD3 = burbuja tuya (o tu color de marca al 20%) · #111111 = texto · #8696A0 = hora y vistos
TIPOGRAFÍA:
- texto de burbujas: estilo Inter (400), letra de ~3% del alto
- nombre del chat: estilo Inter (600), letra de ~3% del alto
- hora: estilo Inter (400), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: barra superior con «Preguntas antes de comprar»; una burbuja grande tuya centrada con el titular «Las 5 preguntas que me hacen antes de [comprar]» en 64 px; indicador «escribiendo…» debajo.
ELEMENTOS GRÁFICOS: avatar circular sin foto de terceros · hora y ✓✓ en cada mensaje · máx. 2 burbujas por slide para que se lea a 46 px · la respuesta arranca con No/Sí en itálica bold
EVITA: logos de WhatsApp o Instagram y nombres reales de clientas: usa «Clienta» o iniciales con permiso.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: pantalla de chat: fondo #EDE6DC con patrón de garabatos al 6% de opacidad, barra superior #1F2C34 con avatar y nombre.
COMPOSICIÓN: barra superior con «Preguntas antes de comprar»; una burbuja grande tuya centrada con el titular «Las 5 preguntas que me hacen antes de [comprar]» en 64 px; indicador «escribiendo…» debajo.
ELEMENTOS: avatar circular sin foto de terceros · hora y ✓✓ en cada mensaje · máx. 2 burbujas por slide para que se lea a 46 px · la respuesta arranca con No/Sí en itálica bold
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (pantalla de chat: fondo #EDE6DC con patrón de garabatos al 6% de opacidad, barra superior #1F2C34 con avatar y nombre.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: burbuja blanca a la izquierda con la pregunta tal cual (esquina superior izquierda en punta) + burbuja verde a la derecha con tu respuesta (esquina superior derecha en punta); hora abajo a la derecha de cada burbuja y ✓✓ azules en la tuya; contador «2/5» en la barra. VARIANTE: sobre papel texturizado claro, un objeto de tu rubro (portapapeles, libreta) con la pregunta en una burbuja de diálogo de tu color en MAYÚSCULAS blancas y la respuesta debajo que arranca con «No.» / «Sí.» en itálica bold.
(Si es la última slide, la composición es: burbuja tuya: «¿Tienes otra? Escríbeme [PALABRA] por DM» + campo de escribir abajo con la palabra ya escrita.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~5% a los lados y nada importante en el 9% de abajo.
FONDO: pantalla de chat: fondo #EDE6DC con patrón de garabatos al 6% de opacidad, barra superior #1F2C34 con avatar y nombre.
PALETA (usa SOLO estos colores): #EDE6DC = fondo del chat · #1F2C34 = barra superior · #FFFFFF = burbuja de la clienta · #D9FDD3 = burbuja tuya (o tu color de marca al 20%) · #111111 = texto · #8696A0 = hora y vistos
TIPOGRAFÍA:
- texto de burbujas: estilo Inter (400), letra de ~3% del alto
- nombre del chat: estilo Inter (600), letra de ~3% del alto
- hora: estilo Inter (400), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: barra superior con «Preguntas antes de comprar»; una burbuja grande tuya centrada con el titular «Las 5 preguntas que me hacen antes de [comprar]» en 64 px; indicador «escribiendo…» debajo.
ELEMENTOS GRÁFICOS: avatar circular sin foto de terceros · hora y ✓✓ en cada mensaje · máx. 2 burbujas por slide para que se lea a 46 px · la respuesta arranca con No/Sí en itálica bold
EVITA: logos de WhatsApp o Instagram y nombres reales de clientas: usa «Clienta» o iniciales con permiso.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: pantalla de chat: fondo #EDE6DC con patrón de garabatos al 6% de opacidad, barra superior #1F2C34 con avatar y nombre.
COMPOSICIÓN: barra superior con «Preguntas antes de comprar»; una burbuja grande tuya centrada con el titular «Las 5 preguntas que me hacen antes de [comprar]» en 64 px; indicador «escribiendo…» debajo.
ELEMENTOS: avatar circular sin foto de terceros · hora y ✓✓ en cada mensaje · máx. 2 burbujas por slide para que se lea a 46 px · la respuesta arranca con No/Sí en itálica bold
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (pantalla de chat: fondo #EDE6DC con patrón de garabatos al 6% de opacidad, barra superior #1F2C34 con avatar y nombre.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: burbuja blanca a la izquierda con la pregunta tal cual (esquina superior izquierda en punta) + burbuja verde a la derecha con tu respuesta (esquina superior derecha en punta); hora abajo a la derecha de cada burbuja y ✓✓ azules en la tuya; contador «2/5» en la barra. VARIANTE: sobre papel texturizado claro, un objeto de tu rubro (portapapeles, libreta) con la pregunta en una burbuja de diálogo de tu color en MAYÚSCULAS blancas y la respuesta debajo que arranca con «No.» / «Sí.» en itálica bold.
(Si es la última slide, la composición es: burbuja tuya: «¿Tienes otra? Escríbeme [PALABRA] por DM» + campo de escribir abajo con la palabra ya escrita.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## G16 · Vitrina de lo que construiste (N cosas que hice)

**Ejemplo:** @nicolebrener_digital · https://www.instagram.com/p/Dcy5upWjA22/ · 18.922 likes · 23.700 comentarios · 7 slides (3 en video) (el original vosea y 3 de sus slides son grabaciones de pantalla: aquí se ve el primer cuadro)

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: azul rey plano #0E3BB2 en todas las slides del medio y en el cierre; la portada es tu foto real a sangre.
PALETA (usa SOLO estos colores): #0E3BB2 = fondo único de la serie · #F1F0C2 = titulares y texto, crema · #1C1815 = marco de la pantalla · #F49AC8 = estrellas-sticker rosas con borde crema · #FFFFFF = interior de la pantalla si la app es clara
TIPOGRAFÍA:
- titular «N. Nombre»: Bricolage Grotesque 700, interletra apretada (-4%), 78 px
- línea de qué hace: Urbanist 400, 56 px
- titular apilado de la portada: Bricolage Grotesque 700, 96 px; cada palabra o grupo en su renglón, alineaciones alternadas izquierda/derecha
PORTADA: tu foto real a sangre (celebrando con los brazos arriba o trabajando en tu escritorio); titular crema apilado en 5-6 renglones con alineación alternada que ocupa el 50% central, con la cifra y el nombre de la herramienta como los renglones más grandes; 3-4 estrellas-sticker rosas alrededor; el logo o ícono de la herramienta como sticker ladeado abajo a la izquierda; una flecha fina crema «→» que invita a deslizar.
SLIDES DEL MEDIO: fondo azul plano; arriba (8-15% del alto) «N. Nombre que dice el beneficio» en crema bold apretado, en una línea; debajo (17-27%) 1-2 renglones de qué hace en crema regular; abajo la pantalla REAL dentro de un marco tipo tablet de borde casi negro de 10 px y esquinas muy redondeadas, que ocupa del 30% al 80% del alto y se sale un poco por los dos lados (o un celular centrado si la app es móvil). La pantalla muestra la app con datos cargados. En 2-3 slides la pantalla es una grabación de 10-25 s de la app en uso.
CIERRE: fondo azul plano sin pantalla; «Comenta» en crema a la izquierda al 40% del alto con una estrella arriba a la derecha; la PALABRA entre comillas en grande entre dos estrellas al 55%; debajo, justificado a lo ancho, «Y te comparto [lo que regalas]» en crema bold.
ELEMENTOS GRÁFICOS: mismo fondo y mismo marco en TODAS las slides del medio · el número pegado al nombre del ítem, en el mismo renglón · pantallas con datos, nunca vacías · estrellas-sticker solo en portada y cierre
EVITA: maquetas o pantallas inventadas por la IA en vez de capturas reales; datos personales reales de clientas visibles en la captura; cambiar el color de fondo entre slides.
```

> Cada slide lleva poco texto (máx. ~22 palabras): el modelo lo puede escribir, pero revisa tildes y eñes letra por letra antes de publicar.

### 1 · Guion (cualquier chat)
```
Tengo estas [N] cosas REALES que construí y uso en mi negocio: [LISTA: nombre de la herramienta/app/plantilla + qué problema me resuelve + si tengo captura o grabación].
Escribe un carrusel vitrina de [N+2] slides:
Slide 1 (portada): titular apilado de máx. 12 palabras del tipo "[N] [cosas] que [dejé de pagar / uso cada día] y las hice con [herramienta]" + qué foto mía usar (celebrando o trabajando, en mi espacio).
Slides 2 a N+1: una por slide → "N. [Nombre que dice el beneficio, máx. 5 palabras]" + 1 línea de qué hace, con un dato concreto (máx. 16 palabras) + qué pantalla mostrar (con datos de ejemplo cargados, nunca vacía) y si va captura o grabación de 10-25 s.
Ordénalas de la más útil para [mi cliente ideal] a la más curiosa.
Última slide: "Comenta [PALABRA]" + qué le mandas por privado (los prompts, la plantilla o la guía para hacer la suya).
Solo cosas que construí de verdad. Tutea.
```

### 2 · Claude Code
```
hazme un carrusel tipo G16 (Vitrina de lo que construiste (N cosas que hice)) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: azul rey plano #0E3BB2 en todas las slides del medio y en el cierre; la portada es tu foto real a sangre.
PALETA (usa SOLO estos colores): #0E3BB2 = fondo único de la serie · #F1F0C2 = titulares y texto, crema · #1C1815 = marco de la pantalla · #F49AC8 = estrellas-sticker rosas con borde crema · #FFFFFF = interior de la pantalla si la app es clara
TIPOGRAFÍA:
- titular «N. Nombre»: Bricolage Grotesque 700, interletra apretada (-4%), 78 px
- línea de qué hace: Urbanist 400, 56 px
- titular apilado de la portada: Bricolage Grotesque 700, 96 px; cada palabra o grupo en su renglón, alineaciones alternadas izquierda/derecha
PORTADA: tu foto real a sangre (celebrando con los brazos arriba o trabajando en tu escritorio); titular crema apilado en 5-6 renglones con alineación alternada que ocupa el 50% central, con la cifra y el nombre de la herramienta como los renglones más grandes; 3-4 estrellas-sticker rosas alrededor; el logo o ícono de la herramienta como sticker ladeado abajo a la izquierda; una flecha fina crema «→» que invita a deslizar.
SLIDES DEL MEDIO: fondo azul plano; arriba (8-15% del alto) «N. Nombre que dice el beneficio» en crema bold apretado, en una línea; debajo (17-27%) 1-2 renglones de qué hace en crema regular; abajo la pantalla REAL dentro de un marco tipo tablet de borde casi negro de 10 px y esquinas muy redondeadas, que ocupa del 30% al 80% del alto y se sale un poco por los dos lados (o un celular centrado si la app es móvil). La pantalla muestra la app con datos cargados. En 2-3 slides la pantalla es una grabación de 10-25 s de la app en uso.
CIERRE: fondo azul plano sin pantalla; «Comenta» en crema a la izquierda al 40% del alto con una estrella arriba a la derecha; la PALABRA entre comillas en grande entre dos estrellas al 55%; debajo, justificado a lo ancho, «Y te comparto [lo que regalas]» en crema bold.
ELEMENTOS GRÁFICOS: mismo fondo y mismo marco en TODAS las slides del medio · el número pegado al nombre del ítem, en el mismo renglón · pantallas con datos, nunca vacías · estrellas-sticker solo en portada y cierre
EVITA: maquetas o pantallas inventadas por la IA en vez de capturas reales; datos personales reales de clientas visibles en la captura; cambiar el color de fondo entre slides.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 80 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: azul rey plano #0E3BB2 en todas las slides del medio y en el cierre; la portada es tu foto real a sangre.
PALETA (usa SOLO estos colores): #0E3BB2 = fondo único de la serie · #F1F0C2 = titulares y texto, crema · #1C1815 = marco de la pantalla · #F49AC8 = estrellas-sticker rosas con borde crema · #FFFFFF = interior de la pantalla si la app es clara
TIPOGRAFÍA:
- titular «N. Nombre»: estilo Bricolage Grotesque (700), interletra apretada (-4%), letra de ~6% del alto
- línea de qué hace: estilo Urbanist (400), letra de ~4% del alto
- titular apilado de la portada: estilo Bricolage Grotesque (700), letra de ~7% del alto; cada palabra o grupo en su renglón, alineaciones alternadas izquierda/derecha
COMPOSICIÓN DE ESTA SLIDE: tu foto real a sangre (celebrando con los brazos arriba o trabajando en tu escritorio); titular crema apilado en 5-6 renglones con alineación alternada que ocupa el 50% central, con la cifra y el nombre de la herramienta como los renglones más grandes; 3-4 estrellas-sticker rosas alrededor; el logo o ícono de la herramienta como sticker ladeado abajo a la izquierda; una flecha fina crema «→» que invita a deslizar.
ELEMENTOS GRÁFICOS: mismo fondo y mismo marco en TODAS las slides del medio · el número pegado al nombre del ítem, en el mismo renglón · pantallas con datos, nunca vacías · estrellas-sticker solo en portada y cierre
EVITA: maquetas o pantallas inventadas por la IA en vez de capturas reales; datos personales reales de clientas visibles en la captura; cambiar el color de fondo entre slides.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: azul rey plano #0E3BB2 en todas las slides del medio y en el cierre; la portada es tu foto real a sangre.
COMPOSICIÓN: tu foto real a sangre (celebrando con los brazos arriba o trabajando en tu escritorio); titular crema apilado en 5-6 renglones con alineación alternada que ocupa el 50% central, con la cifra y el nombre de la herramienta como los renglones más grandes; 3-4 estrellas-sticker rosas alrededor; el logo o ícono de la herramienta como sticker ladeado abajo a la izquierda; una flecha fina crema «→» que invita a deslizar.
ELEMENTOS: mismo fondo y mismo marco en TODAS las slides del medio · el número pegado al nombre del ítem, en el mismo renglón · pantallas con datos, nunca vacías · estrellas-sticker solo en portada y cierre
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: lleva tus fotos o capturas reales (azul rey plano #0E3BB2 en todas las slides del medio y en el cierre; la portada es tu foto real a sangre.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: fondo azul plano; arriba (8-15% del alto) «N. Nombre que dice el beneficio» en crema bold apretado, en una línea; debajo (17-27%) 1-2 renglones de qué hace en crema regular; abajo la pantalla REAL dentro de un marco tipo tablet de borde casi negro de 10 px y esquinas muy redondeadas, que ocupa del 30% al 80% del alto y se sale un poco por los dos lados (o un celular centrado si la app es móvil). La pantalla muestra la app con datos cargados. En 2-3 slides la pantalla es una grabación de 10-25 s de la app en uso.
(Si es la última slide, la composición es: fondo azul plano sin pantalla; «Comenta» en crema a la izquierda al 40% del alto con una estrella arriba a la derecha; la PALABRA entre comillas en grande entre dos estrellas al 55%; debajo, justificado a lo ancho, «Y te comparto [lo que regalas]» en crema bold.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: azul rey plano #0E3BB2 en todas las slides del medio y en el cierre; la portada es tu foto real a sangre.
PALETA (usa SOLO estos colores): #0E3BB2 = fondo único de la serie · #F1F0C2 = titulares y texto, crema · #1C1815 = marco de la pantalla · #F49AC8 = estrellas-sticker rosas con borde crema · #FFFFFF = interior de la pantalla si la app es clara
TIPOGRAFÍA:
- titular «N. Nombre»: estilo Bricolage Grotesque (700), interletra apretada (-4%), letra de ~6% del alto
- línea de qué hace: estilo Urbanist (400), letra de ~4% del alto
- titular apilado de la portada: estilo Bricolage Grotesque (700), letra de ~7% del alto; cada palabra o grupo en su renglón, alineaciones alternadas izquierda/derecha
COMPOSICIÓN DE ESTA SLIDE: tu foto real a sangre (celebrando con los brazos arriba o trabajando en tu escritorio); titular crema apilado en 5-6 renglones con alineación alternada que ocupa el 50% central, con la cifra y el nombre de la herramienta como los renglones más grandes; 3-4 estrellas-sticker rosas alrededor; el logo o ícono de la herramienta como sticker ladeado abajo a la izquierda; una flecha fina crema «→» que invita a deslizar.
ELEMENTOS GRÁFICOS: mismo fondo y mismo marco en TODAS las slides del medio · el número pegado al nombre del ítem, en el mismo renglón · pantallas con datos, nunca vacías · estrellas-sticker solo en portada y cierre
EVITA: maquetas o pantallas inventadas por la IA en vez de capturas reales; datos personales reales de clientas visibles en la captura; cambiar el color de fondo entre slides.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: azul rey plano #0E3BB2 en todas las slides del medio y en el cierre; la portada es tu foto real a sangre.
COMPOSICIÓN: tu foto real a sangre (celebrando con los brazos arriba o trabajando en tu escritorio); titular crema apilado en 5-6 renglones con alineación alternada que ocupa el 50% central, con la cifra y el nombre de la herramienta como los renglones más grandes; 3-4 estrellas-sticker rosas alrededor; el logo o ícono de la herramienta como sticker ladeado abajo a la izquierda; una flecha fina crema «→» que invita a deslizar.
ELEMENTOS: mismo fondo y mismo marco en TODAS las slides del medio · el número pegado al nombre del ítem, en el mismo renglón · pantallas con datos, nunca vacías · estrellas-sticker solo en portada y cierre
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: lleva tus fotos o capturas reales (azul rey plano #0E3BB2 en todas las slides del medio y en el cierre; la portada es tu foto real a sangre.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: fondo azul plano; arriba (8-15% del alto) «N. Nombre que dice el beneficio» en crema bold apretado, en una línea; debajo (17-27%) 1-2 renglones de qué hace en crema regular; abajo la pantalla REAL dentro de un marco tipo tablet de borde casi negro de 10 px y esquinas muy redondeadas, que ocupa del 30% al 80% del alto y se sale un poco por los dos lados (o un celular centrado si la app es móvil). La pantalla muestra la app con datos cargados. En 2-3 slides la pantalla es una grabación de 10-25 s de la app en uso.
(Si es la última slide, la composición es: fondo azul plano sin pantalla; «Comenta» en crema a la izquierda al 40% del alto con una estrella arriba a la derecha; la PALABRA entre comillas en grande entre dos estrellas al 55%; debajo, justificado a lo ancho, «Y te comparto [lo que regalas]» en crema bold.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Si la slide lleva foto, conserva sus colores reales: la paleta es para el texto y los elementos, no para teñir la foto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---

## G17 · Hilo de tuits: comando → resultado

**Ejemplo:** @marceloalaminoo · https://www.instagram.com/p/DdM3nuWgczR/ · 40.120 likes · 118 comentarios · 14 slides (sus comandos con barra no existen y usa fotos de famosos: se copia solo la forma del tuit)

**Visual detallado**
```
LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: blanco #FFFFFF liso en todas las slides.
PALETA (usa SOLO estos colores): #FFFFFF = fondo · #1D181E = texto · #8E8E93 = tu usuario en gris claro · #1D9BF0 = ✓ de verificado junto al avatar · #E0245E = corazón de la pausa de like
TIPOGRAFÍA:
- texto del tuit: Poppins 400, 44 px; las palabras clave y el comando en Poppins 700
- nombre: Poppins 600, 36 px
- tu usuario: Poppins 400, 28 px
PORTADA: arriba a la izquierda (5-9% del alto) avatar circular de 92 px con tu foto + ✓ azul + nombre en negro y tu usuario en gris debajo; texto del tuit alineado a la izquierda desde el 13%; el comando o prompt en bold en su propio renglón; el ANTES (foto o captura) en un marco de esquinas redondeadas 24 px, centrado, 55-65% del ancho, entre el 22% y el 45% del alto. La mitad de abajo queda en blanco a propósito.
SLIDES DEL MEDIO: mismo encabezado de tuit. RESULTADO: una línea de lo que logra con el verbo en bold + el DESPUÉS en el mismo marco y tamaño que el antes. VARIANTE lado a lado: texto a la izquierda centrado en vertical (45% del ancho) y foto vertical redondeada a la derecha. PAUSA DE LIKE: encabezado más abajo (≈45% del alto) y solo un corazón rojo seguido de la frase que pide el like, sin imagen.
CIERRE: mismo encabezado; tuit largo de 3 párrafos cortos alineado a la izquierda con frases clave en bold (a quién ayudas, qué logran, la oferta o la palabra a comentar); abajo una captura de prueba chica (60% del ancho) con sombra suave.
ELEMENTOS GRÁFICOS: el encabezado de tuit idéntico en todas las slides · el antes y el después en slides distintas, mismo marco · una sola idea en bold por tuit · slide de pausa de like a la mitad, sin imagen
EVITA: comandos con barra inventados (/algo) que no existen; fotos de famosos o de terceros; logos de X/Twitter; números falsos de me gusta o retuits.
```

> OJO: esta ficha lleva más de ~25 palabras por slide. Los modelos de imagen fallan tildes y listas largas: usa la VARIANTE C (fondo sin texto) y pon el texto con la opción HTML.

### 1 · Guion (cualquier chat)
```
Arma un carrusel tipo hilo de tuits de [8-12] slides con [3-5] trucos de [HERRAMIENTA] para [RESULTADO que quiere mi cliente ideal].
Cada truco son 2 slides:
- INSTRUCCIÓN: "[Sube/Pega] [qué] en [herramienta] y escribe:" + el prompt EXACTO que funciona (máx. 20 palabras, en bold, en su propia línea) + qué ANTES mostrar (captura o foto de partida).
- RESULTADO: "Va a [verbo en bold] [lo que logra]" (máx. 20 palabras) + qué DESPUÉS mostrar, del mismo caso.
Después del truco 2, una slide sola sin imagen: "❤️ Antes de continuar, dale like si quieres más trucos de [herramienta]".
Ordena los trucos del más fácil al más vistoso.
Última slide: tuit de 3 párrafos cortos → a quién ayudo + qué logran + mi oferta o CTA "Comenta [PALABRA]".
No inventes comandos con barra (/algo) que no existan: si es un prompt, escríbelo completo. Nada de fotos de famosos ni de terceros sin permiso. Tutea.
```

### 2 · Claude Code
```
hazme un carrusel tipo G17 (Hilo de tuits: comando → resultado) sobre [TEMA] para [MI NICHO]
```

### 3 · HTML en Claude, ChatGPT o Gemini (texto perfecto)
```
Actúa como diseñadora de carruseles de Instagram. Vas a construir el carrusel en HTML para que el texto salga perfecto (tildes, eñes y listas).

GUION:
[PEGA AQUÍ EL GUION APROBADO, SLIDE POR SLIDE, con el texto exacto de cada una]

LIENZO: 1080 × 1350 px (vertical 4:5). Márgenes de seguridad: 80 px a los lados; nada importante en los 120 px de abajo (ahí tapa la interfaz de Instagram).
FONDO: blanco #FFFFFF liso en todas las slides.
PALETA (usa SOLO estos colores): #FFFFFF = fondo · #1D181E = texto · #8E8E93 = tu usuario en gris claro · #1D9BF0 = ✓ de verificado junto al avatar · #E0245E = corazón de la pausa de like
TIPOGRAFÍA:
- texto del tuit: Poppins 400, 44 px; las palabras clave y el comando en Poppins 700
- nombre: Poppins 600, 36 px
- tu usuario: Poppins 400, 28 px
PORTADA: arriba a la izquierda (5-9% del alto) avatar circular de 92 px con tu foto + ✓ azul + nombre en negro y tu usuario en gris debajo; texto del tuit alineado a la izquierda desde el 13%; el comando o prompt en bold en su propio renglón; el ANTES (foto o captura) en un marco de esquinas redondeadas 24 px, centrado, 55-65% del ancho, entre el 22% y el 45% del alto. La mitad de abajo queda en blanco a propósito.
SLIDES DEL MEDIO: mismo encabezado de tuit. RESULTADO: una línea de lo que logra con el verbo en bold + el DESPUÉS en el mismo marco y tamaño que el antes. VARIANTE lado a lado: texto a la izquierda centrado en vertical (45% del ancho) y foto vertical redondeada a la derecha. PAUSA DE LIKE: encabezado más abajo (≈45% del alto) y solo un corazón rojo seguido de la frase que pide el like, sin imagen.
CIERRE: mismo encabezado; tuit largo de 3 párrafos cortos alineado a la izquierda con frases clave en bold (a quién ayudas, qué logran, la oferta o la palabra a comentar); abajo una captura de prueba chica (60% del ancho) con sombra suave.
ELEMENTOS GRÁFICOS: el encabezado de tuit idéntico en todas las slides · el antes y el después en slides distintas, mismo marco · una sola idea en bold por tuit · slide de pausa de like a la mitad, sin imagen
EVITA: comandos con barra inventados (/algo) que no existen; fotos de famosos o de terceros; logos de X/Twitter; números falsos de me gusta o retuits.

CÓMO LO ENTREGAS:
- UN solo archivo HTML. Cada slide es un <section class="slide"> de exactamente 1080×1350 px, uno debajo del otro, overflow hidden.
- Fuentes de Google Fonts con <link>; nunca -apple-system ni fuentes del sistema.
- Ningún texto puede salirse del slide ni quedar a menos de 80 px del borde. Si no cabe, acorta el texto: no bajes la letra por debajo de 36 px.
- Arriba de todo, un botón "Descargar PNG" que use html2canvas (https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) con scale: 2 y baje cada slide como slide-01.png, slide-02.png…
- Tutea en todo el texto.
Muéstrame el resultado en la vista previa (Canvas/Artifacts) y dime qué slide te costó más encajar.
(Para bajar los PNG: descarga el archivo .html y ábrelo con doble clic en tu navegador; dentro de la vista previa del chat el botón puede no descargar.)
```

### 4 · Gemini (Nano Banana)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Genera la PORTADA de un carrusel de Instagram.
Texto exacto, tal cual, con sus tildes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: blanco #FFFFFF liso en todas las slides.
PALETA (usa SOLO estos colores): #FFFFFF = fondo · #1D181E = texto · #8E8E93 = tu usuario en gris claro · #1D9BF0 = ✓ de verificado junto al avatar · #E0245E = corazón de la pausa de like
TIPOGRAFÍA:
- texto del tuit: estilo Poppins (400), letra de ~3% del alto; las palabras clave y el comando en Poppins 700
- nombre: estilo Poppins (600), letra de ~3% del alto
- tu usuario: estilo Poppins (400), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: arriba a la izquierda (5-9% del alto) avatar circular de 92 px con tu foto + ✓ azul + nombre en negro y tu usuario en gris debajo; texto del tuit alineado a la izquierda desde el 13%; el comando o prompt en bold en su propio renglón; el ANTES (foto o captura) en un marco de esquinas redondeadas 24 px, centrado, 55-65% del ancho, entre el 22% y el 45% del alto. La mitad de abajo queda en blanco a propósito.
ELEMENTOS GRÁFICOS: el encabezado de tuit idéntico en todas las slides · el antes y el después en slides distintas, mismo marco · una sola idea en bold por tuit · slide de pausa de like a la mitad, sin imagen
EVITA: comandos con barra inventados (/algo) que no existen; fotos de famosos o de terceros; logos de X/Twitter; números falsos de me gusta o retuits.
El texto debe verse nítido, sin letras inventadas ni palabras extra. Nada de marcas de agua.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**B · Con tu marca**
```
Genera la PORTADA de un carrusel de Instagram, imagen vertical 4:5, con MI marca en lugar de esta paleta.
Mis colores: [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex]. Mi tipografía: [nombre o "sans ultra bold" / "serif elegante" / "manuscrita"].
Texto exacto: "[TEXTO DE LA PORTADA]".
Mantén esta composición y cambia solo colores y letra:
FONDO: blanco #FFFFFF liso en todas las slides.
COMPOSICIÓN: arriba a la izquierda (5-9% del alto) avatar circular de 92 px con tu foto + ✓ azul + nombre en negro y tu usuario en gris debajo; texto del tuit alineado a la izquierda desde el 13%; el comando o prompt en bold en su propio renglón; el ANTES (foto o captura) en un marco de esquinas redondeadas 24 px, centrado, 55-65% del ancho, entre el 22% y el 45% del alto. La mitad de abajo queda en blanco a propósito.
ELEMENTOS: el encabezado de tuit idéntico en todas las slides · el antes y el después en slides distintas, mismo marco · una sola idea en bold por tuit · slide de pausa de like a la mitad, sin imagen
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (blanco #FFFFFF liso en todas las slides.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Perfecto. Ahora la slide [N] con EXACTAMENTE el mismo estilo, paleta, tipografía y márgenes que la imagen anterior. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición de esta slide: mismo encabezado de tuit. RESULTADO: una línea de lo que logra con el verbo en bold + el DESPUÉS en el mismo marco y tamaño que el antes. VARIANTE lado a lado: texto a la izquierda centrado en vertical (45% del ancho) y foto vertical redondeada a la derecha. PAUSA DE LIKE: encabezado más abajo (≈45% del alto) y solo un corazón rojo seguido de la frase que pide el like, sin imagen.
(Si es la última slide, la composición es: mismo encabezado; tuit largo de 3 párrafos cortos alineado a la izquierda con frases clave en bold (a quién ayudas, qué logran, la oferta o la palabra a comentar); abajo una captura de prueba chica (60% del ancho) con sombra suave.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
En la última imagen, corrige SOLO esta palabra: "[palabra mal escrita]" → "[palabra correcta]". No cambies nada más.
```

### 5 · ChatGPT (Imágenes)
**A · Desde la descripción (el prompt se sostiene solo: no adjuntas nada)**
```
Crea la imagen de la PORTADA de un carrusel de Instagram.
Escribe este texto EXACTO, respetando tildes y eñes: "[TEXTO DE LA PORTADA]".
FORMATO: imagen vertical 4:5. Deja un margen limpio de ~7% a los lados y nada importante en el 9% de abajo.
FONDO: blanco #FFFFFF liso en todas las slides.
PALETA (usa SOLO estos colores): #FFFFFF = fondo · #1D181E = texto · #8E8E93 = tu usuario en gris claro · #1D9BF0 = ✓ de verificado junto al avatar · #E0245E = corazón de la pausa de like
TIPOGRAFÍA:
- texto del tuit: estilo Poppins (400), letra de ~3% del alto; las palabras clave y el comando en Poppins 700
- nombre: estilo Poppins (600), letra de ~3% del alto
- tu usuario: estilo Poppins (400), letra de ~2% del alto
COMPOSICIÓN DE ESTA SLIDE: arriba a la izquierda (5-9% del alto) avatar circular de 92 px con tu foto + ✓ azul + nombre en negro y tu usuario en gris debajo; texto del tuit alineado a la izquierda desde el 13%; el comando o prompt en bold en su propio renglón; el ANTES (foto o captura) en un marco de esquinas redondeadas 24 px, centrado, 55-65% del ancho, entre el 22% y el 45% del alto. La mitad de abajo queda en blanco a propósito.
ELEMENTOS GRÁFICOS: el encabezado de tuit idéntico en todas las slides · el antes y el después en slides distintas, mismo marco · una sola idea en bold por tuit · slide de pausa de like a la mitad, sin imagen
EVITA: comandos con barra inventados (/algo) que no existen; fotos de famosos o de terceros; logos de X/Twitter; números falsos de me gusta o retuits.
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
Antes de generar, repíteme en una línea el texto que vas a escribir para confirmar que está bien.
```
**B · Con tu marca**
```
Crea la PORTADA de un carrusel de Instagram, vertical 4:5, con esta composición pero con MI identidad:
colores [FONDO #hex] · [TEXTO #hex] · [ACENTO #hex] y tipografía [descripción].
Texto exacto: "[TEXTO DE LA PORTADA]".
FONDO: blanco #FFFFFF liso en todas las slides.
COMPOSICIÓN: arriba a la izquierda (5-9% del alto) avatar circular de 92 px con tu foto + ✓ azul + nombre en negro y tu usuario en gris debajo; texto del tuit alineado a la izquierda desde el 13%; el comando o prompt en bold en su propio renglón; el ANTES (foto o captura) en un marco de esquinas redondeadas 24 px, centrado, 55-65% del ancho, entre el 22% y el 45% del alto. La mitad de abajo queda en blanco a propósito.
ELEMENTOS: el encabezado de tuit idéntico en todas las slides · el antes y el después en slides distintas, mismo marco · una sola idea en bold por tuit · slide de pausa de like a la mitad, sin imagen
```
**C · Solo fondo, sin texto**
```
Esta ficha no necesita un fondo generado con IA: el fondo es liso o tipográfico (blanco #FFFFFF liso en todas las slides.)
Usa la opción «HTML en cualquier chat» para armarla con el texto perfecto, o la variante A/B si quieres que el modelo haga la slide completa.
```
**Seguir con el slide N**
```
Ahora la slide [N]. Mismo estilo, misma paleta, misma tipografía y mismo encuadre que la imagen anterior: es una serie. Texto exacto: "[TEXTO DE LA SLIDE N]".
Composición: mismo encabezado de tuit. RESULTADO: una línea de lo que logra con el verbo en bold + el DESPUÉS en el mismo marco y tamaño que el antes. VARIANTE lado a lado: texto a la izquierda centrado en vertical (45% del ancho) y foto vertical redondeada a la derecha. PAUSA DE LIKE: encabezado más abajo (≈45% del alto) y solo un corazón rojo seguido de la frase que pide el like, sin imagen.
(Si es la última slide, la composición es: mismo encabezado; tuit largo de 3 párrafos cortos alineado a la izquierda con frases clave en bold (a quién ayudas, qué logran, la oferta o la palabra a comentar); abajo una captura de prueba chica (60% del ancho) con sombra suave.)
Lo que aparece entre «» en la descripción es solo un ejemplo de tono: no lo escribas. En la imagen va SOLO el texto exacto.
```
**Arreglar una palabra**
```
Edita la imagen anterior: cambia únicamente "[palabra mal escrita]" por "[palabra correcta]", con la misma letra y el mismo tamaño. Todo lo demás igual.
```

---
