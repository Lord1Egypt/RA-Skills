# CATÁLOGO DE FORMATOS DE CARRUSEL · FÓRMULA 100K

> Catálogo de formatos de carrusel de FÓRMULA 100K. Lo mantiene el equipo y llega con cada actualización del paquete.
>
> Versión 2.1 · 17-sep-2026 · **37 fichas** (G16 vitrina y G17 hilo de tuits se sumaron el 17-sep). Versión 2 · 14-sep-2026 · 35 fichas: 20 F (referencias miradas el 13-sep) + 15 G (13 carruseles
> de la Guía de Formatos del Grimorio + 2 mecánicas que solo vivían en la guía maestra de 25 estilos).
> La v1 dejaba fuera 13 carruseles del Grimorio y 16 de los 25 estilos: ahora cada uno tiene su lugar
> (ver «AUDITORÍA DE COBERTURA» al final).
> Cada referencia fue MIRADA slide por slide (81 slides de 12 posts + 4 posts de los
> decks de FÓRMULA 100K). Métricas leídas de la API interna de IG el 13-sep-2026.
> Los prompts NO están probados con generación real todavía (Higgsfield sin créditos,
> sin `GEMINI_API_KEY`): son v1 razonados desde las referencias.

---

## EL SISTEMA: 3 PERILLAS

Un carrusel se decide girando tres perillas, en este orden:

1. **MECÁNICA** — qué HACE el carrusel con la atención (decide el guion).
   Se elige por el OBJETIVO: guardado, comentario, seguidor, conexión, venta.
2. **SOPORTE** — dónde VIVE el texto (decide la estética).
   Libreta, foto con tarjeta, dos fotos partidas, pizarra, tipografía pura…
3. **MOTOR** — con qué se FABRICA (decide la herramienta y el costo).
   - **A · Tus fotos + HTML** (gratis, texto perfecto): carrusel-render / clonador.
   - **B · Imagen IA** (Nano Banana / Higgsfield): soportes físicos, personajes, objetos.
   - **C · Híbrido**: la IA hace el fondo SIN texto y el texto se pone encima en HTML.

**Regla de oficio (razonada, no medida):** si una slide lleva más de ~25 palabras o
una lista, NO le pidas el texto al modelo de imagen — usa el motor C. Los modelos de
imagen se equivocan con tildes, eñes y listas largas, y un error en la slide 1 mata la
confianza en todo el carrusel.

**El error que evita este sistema:** confundir soporte con formato. "Carrusel en
libreta" no es un formato: es un soporte. Una libreta puede llevar un tutorial, una
chuleta o una frase. Lo que retiene es la mecánica; el soporte solo frena el scroll.

### Mecánicas (qué hace)

| Código | Mecánica | Objetivo principal |
|---|---|---|
| M1 | Tutorial comando → resultado | Guardado + comentario |
| M2 | Paso a paso numerado | Guardado |
| M3 | Lista con remate por ítem | Guardado + compartido |
| M4 | Anáfora (un prefijo que se repite) | Compartido + seguidor |
| M5 | Frase partida (arriba el setup, abajo el golpe) | Compartido |
| M6 | Historia de origen con edades | Conexión + venta |
| M7 | Personificación (el concepto habla) | Comentario + seguidor |
| M8 | Chuleta densa + slide de seguir | Guardado + seguidor |
| M9 | Ranking / comparación | Guardado + debate |
| M10 | Mapa (concepto central y ramas) | Guardado |
| M11 | Collage de muchas señales | Tiempo de permanencia |
| M12 | Opinión fuerte escenificada (hot take) | Comentario |
| M13 | Checklist (un ítem por slide) | Guardado |
| M14 | Noticia del nicho (qué pasó → por qué te importa) | Alcance + autoridad |
| M15 | Test de identidad (¿qué tipo de X eres?) | Comentario + etiquetas |
| M16 | Lo que te dicen vs lo que pasa (mito / realidad) | Guardado + comentario |
| M17 | Biblioteca de recursos | Guardado + comentario |
| M18 | Glosario (término + definición + ejemplo) | Guardado + compartido |
| M19 | Mini caso de estudio con tu dato | Venta + guardado |
| M20 | Molde para copiar (texto fijo + [huecos]) | Comentario + guardado |
| M21 | Frase cortada entre slides (swipe-reveal) | Tiempo de permanencia + comentario |
| M22 | Frases sueltas (una por slide) | Compartido |
| M23 | Errores propios confesados | Conexión + autoridad |
| M24 | Confesión a partir de una pregunta íntima | Comentario (historias) |
| M25 | De A a B con antesala («no es tu culpa» antes de los pasos) | Guardado + venta |
| M26 | Antes / después | Venta |
| M27 | Preguntas frecuentes en chat (objeciones respondidas) | Venta |
| M28 | Vitrina de lo que construiste (N cosas, cada una con su pantalla funcionando) | Comentario + guardado |

### Soportes (dónde vive)

| Código | Soporte | Motor natural |
|---|---|---|
| S1 | Dos fotos apiladas con frase partida | A |
| S2 | Fondo blanco + captura de pantalla | A |
| S3 | Libreta abierta sostenida con la mano | C |
| S4 | Hoja de cuaderno espiral con bolígrafo azul | C |
| S5 | Agenda / planner con letra a mano | C |
| S6 | Tu foto fija + tarjeta que cambia | A |
| S7 | Tu foto a sangre + texto con itálicas | A |
| S8 | Cuadrícula editorial de 4 cuadrantes | C |
| S9 | Etiquetas de papel rasgado sobre foto | A |
| S10 | Garabatos dibujados sobre tu foto | A |
| S11 | Pizarra / rotafolio en estudio | B o C |
| S12 | Tipografía gigante con degradado | A |
| S13 | Ilustración kawaii con tarjeta | B + A |
| S14 | Collage de recortes con etiquetas | B + A |
| S15 | Objetos reales en fila con cifras | B + A |
| S16 | Tabla tier list / mapa de ramas | A |
| S17 | Slide tipográfica plana con PIEL de la guía maestra (Bold 01 · Minimalista 02 · Dark neón 03 · Pastel emoji 05 · Glass 07 · Dato gigante 09 · Brutalist 16 · Y2K 19 · Acid 20) | A |
| S18 | Editorial revista (serif + sans en columnas) · estilo 04 | A |
| S19 | Imagen IA + bloque de texto partido · estilo 10 | C |
| S20 | Doble paleta (mito ❌ / realidad ✅ · antes / después · A│B) · estilos 12 y 15 | A |
| S21 | Casillas de checklist · estilo 13 | A |
| S22 | Chat / DM con burbujas · estilo 14 | A |
| S23 | Recibo / ticket / pase de abordar · estilo 17 | A |
| S24 | Editor de código / terminal · estilo 18 | A |
| S25 | Bento grid (tiles desiguales) · estilo 21 | A |
| S26 | Periódico / portada impresa · estilo 23 | A |
| S27 | Nota del celular / tuit · estilo 24 | A |
| S28 | Barra de progreso / stepper · estilo 25 | A |
| S29 | Fondo de color plano + pantalla en marco tipo tablet (captura o grabación) | A |

Los estilos 06 (gradiente), 08 (scrapbook), 11 (full bleed) y 22 (data-viz) ya eran soportes de la v1:
S12, S14, S7 y S16/S15. Los **prompts de cada estilo** viven en la guía maestra
(`references/estilos-guia-maestra.md`).

---

## LAS 20 FICHAS

Cada ficha: referencia real · anatomía slide por slide · por qué funciona (lo que se VE,
no lo que se supone) · error típico · prompt copiable · skill que lo fabrica.

---

### F01 · Causa y consecuencia ("¿por qué te pasó esto?")
- **Mecánica:** M5 frase partida · **Soporte:** S1 dos fotos apiladas · **Motor:** A
- **Referencia:** @kennithlee_ (74,6K seguidores) · 6.100 likes · 16 comentarios · 5 slides · https://www.instagram.com/p/Dc4PCI6nz9f/
- **Anatomía:**
  1. Slides 1-4: cada slide son 2 fotos personales apiladas. Arriba "dejé de [acción]", abajo "y [lo que pasó con la gente]". Ej.: "dejé de explicarme" / "y me malinterpretaron".
  2. Las fotos son de carrete real (casa, café, calle, playa), no de sesión.
  3. Texto blanco, fino, centrado justo en la línea de cada foto.
  4. Slide final: el REENCUADRE. Arriba "no alejaste a la gente", abajo "solo dejaste de doblarte para retenerla".
- **Por qué funciona:** el lector reconoce la consecuencia como propia ("eso me pasó") y la slide final le cambia la culpa de lugar. Portada = ya es la mecánica: no hay slide de título.
- **Error típico:** poner una portada con título ("5 señales de…"). Mata la sorpresa: la primera frase partida ES el gancho.
- **Prompt:**
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
- **Skill:** `carrusel-formatos-f100k` (plantilla split) · alternativa hoy: `clonador-carrusel-formula100k` con el link de la referencia.

---

### F02 · Pantalla dividida: casos en serie
- **Mecánica:** M5 frase partida + M4 anáfora · **Soporte:** S1 · **Motor:** A (o B para las fotos de lugares)
- **Referencia:** @businessbulls.in (1,64M seguidores) · 2.409 likes · 17 comentarios · 6 slides · https://www.instagram.com/p/Dc-MNF-im1r/
- **Anatomía:**
  1. Cada slide: foto de las personas ARRIBA, foto del resultado (logo en edificio, producto) ABAJO.
  2. Texto arriba repetido en todas: "DOS AMIGOS SE UNIERON…". Texto abajo cambia: "Y FUNDARON GOOGLE."
  3. Texto en mayúsculas bold; el de abajo en amarillo sobre degradado negro.
  4. 6 casos, sin slide de cierre; logo de la cuenta y "swipe" arriba.
- **Por qué funciona:** la repetición crea ritmo y la mitad de abajo es un mini-premio en cada swipe. Es el mismo motor que F01 aplicado a negocios: la frase partida cruza nichos (desarrollo personal y negocios).
- **Error típico:** cambiar el texto de arriba en cada slide. La anáfora se rompe y ya no hay ritmo.
- **Prompt:**
```
Crea un carrusel de 6 slides en formato "pantalla dividida en serie" sobre [TEMA: ej. clientas que empezaron sin seguidores].
Frase fija de ARRIBA (igual en las 6 slides, máx. 5 palabras, termina en "…"): [ej. "EMPEZÓ CON 200 SEGUIDORES…"].
Frase de ABAJO (cambia en cada slide, empieza con "Y", máx. 6 palabras): el resultado concreto y verificable de cada caso.
Ordena los casos de menos a más impactante.
Para cada slide dime: foto de arriba (la persona o el antes) y foto de abajo (el resultado visible: producto, local, pantalla con cifra).
Estilo: mayúsculas bold, texto de abajo en [COLOR DE ACENTO] sobre degradado oscuro.
Solo casos reales que yo te dé; si falta un dato, déjalo como [FALTA DATO], no lo inventes.
```
- **Skill:** `carrusel-formatos-f100k` (plantilla split) · `carrusel-caso-exito-f100k` si son alumnas (verifica cifras).

---

### F03 · Tutorial comando → resultado
- **Mecánica:** M1 · **Soporte:** S2 fondo blanco + captura · **Motor:** A (capturas reales)
- **Referencia:** @profesiondelfuturo (4,89M seguidores) · 8.469 likes · 149 comentarios · 8 slides · https://www.instagram.com/p/DdMlaYVoA7e/
- **Anatomía:**
  1. Portada: señal de STOP + "Deja de publicar imágenes así" + 2 ejemplos feos reales + "Usa estos 3 comandos →".
  2. Slide par: "Sube la foto y escribe: /comando" + captura del chat con el comando subrayado en rojo.
  3. Slide impar: una línea de qué hace + el RESULTADO a sangre.
  4. Se repite comando → resultado 3 veces.
  5. Cierre: CTA a taller gratuito.
- **Por qué funciona:** alterna promesa y prueba cada swipe; el lector ve el resultado antes de decidir si guarda. La portada con el "antes feo" hace que se sienta aludido.
- **Error típico:** meter dos comandos en una slide o poner el resultado antes del comando. El orden instrucción → premio es la mecánica.
- **Prompt:**
```
Arma un carrusel tutorial de 8 slides "comando → resultado" para [HERRAMIENTA] y [RESULTADO que quiere mi cliente ideal].
Slide 1: "Deja de [error visible que comete mi audiencia]" + describe 2 ejemplos del error + "Usa estos 3 [prompts/comandos] →".
Slides 2, 4 y 6: "Ahora escribe:" + el prompt/comando EXACTO (cópialo tal cual, corto) + qué captura de pantalla tomar.
Slides 3, 5 y 7: una línea de lo que logra ("Crea una publicidad limpia y sin cara de IA") + qué resultado mostrar a pantalla completa.
Slide 8: CTA "Comenta [PALABRA] y te mando [recurso]".
Reglas: fondo blanco, título negro bold arriba, máximo 12 palabras por slide. Los prompts deben funcionar de verdad: si no estás segura de que existe un comando, escríbelo como prompt completo en vez de inventar un atajo.
```
- **Skill:** `capturas-tutorial-formula100k` (capturas) + `carrusel-render-formula100k` (maqueta).

---

### F04 · Tutorial en libreta
- **Mecánica:** M2 paso a paso · **Soporte:** S3 libreta sostenida · **Motor:** C
- **Referencia:** @karoempowerment (340K seguidores) · likes ocultos · **894 comentarios** · 5 slides · https://www.instagram.com/p/DdHSQg1mJ_1/
- **Anatomía:**
  1. Foto cenital de una libreta abierta sostenida por una mano, sobre madera; misma foto en todas.
  2. Portada: "Cómo pedirle a ChatGPT que muestre tu perfil a +1 MILLÓN de personas" + "(aunque tengas pocos seguidores)". La cifra con resaltador amarillo.
  3. Slides 2-4: "1. Dale contexto…" con lista de viñetas y una frase final resaltada.
  4. Cierre: "¿Quieres el MÉTODO completo…? Comenta: MÉTODO y te lo envío por privado."
- **Por qué funciona:** la letra a mano se lee como nota personal, no como anuncio; el paréntesis "(aunque tengas pocos seguidores)" quita la objeción en la portada. El CTA de palabra clave explica los 894 comentarios.
- **Error típico:** la referencia salta del paso 2 al 4. Numera siempre corrido: un salto se nota y resta confianza.
- **Prompt:**
```
Escribe un carrusel de 5 slides "tutorial en libreta" sobre [RESULTADO DESEADO] usando [HERRAMIENTA].
Slide 1: "Cómo [lograr resultado con cifra concreta]" + en paréntesis la objeción que quitas: "(aunque [limitación de mi audiencia])". Marca con **asteriscos** la frase que va con resaltador.
Slides 2-4: "N. [Paso en 3-5 palabras]" + máx. 5 viñetas cortas + una frase final resaltada que explique por qué importa.
Slide 5: "¿Quieres [el método completo]?" + "Comenta: [PALABRA]" + "y te lo envío por privado."
Máx. 45 palabras por slide (tiene que parecer escrito a mano). Numera corrido.
Luego dame el prompt de imagen para el FONDO (sin texto): foto cenital de una libreta abierta de hojas color hueso sostenida por una mano, sobre mesa de madera cálida, luz de ventana suave, página en blanco, formato 4:5.
```
- **Skill:** `carrusel-formatos-f100k` (plantilla libreta: fondo IA + fuente manuscrita HTML).

---

### F05 · Hábitos 10/10 en cuadrícula editorial
- **Mecánica:** M3 lista con remate · **Soporte:** S8 cuadrícula de 4 · **Motor:** C
- **Referencia:** @jun_yuh (5,31M seguidores) · dos posts: 20.348 likes / 99 comentarios y 5.118 likes / 311 comentarios · 8 slides cada uno · https://www.instagram.com/p/Dcd2kFKEfY3/ · https://www.instagram.com/p/DdEqGYwESZ8/
- **Anatomía:**
  1. Portada: foto personal a sangre + "10/10 hábitos para [resultado]" + subtítulo en itálica ("y literalmente cualquiera puede hacerlos…").
  2. "10/10" es una NOTA, no la cantidad: cada post trae 6 hábitos.
  3. Cada slide: 4 cuadrantes. Arriba izq. foto tuya; arriba der. imagen artística metafórica (pintura, objeto); abajo izq. otra imagen metafórica; abajo der. bloque negro con texto.
  4. Título del hábito en blanco cruzando el centro.
  5. Bloque negro en 3 capas: explicación normal · *una línea en itálica* · **remate en negrita**.
  6. Cierre: pregunta abierta ("¿qué hace a alguien inolvidable para ti?") o CTA "comenta EARN".
- **Por qué funciona:** el collage de foto real + arte hace que un consejo común se vea de revista; el remate en negrita da la frase para capturar y compartir. El cierre con pregunta sacó 311 comentarios; el que no la tenía, 99.
- **Error típico:** escribir 10 hábitos porque dice "10/10". Son 6, y cada uno necesita su slide.
- **Prompt:**
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
- **Skill:** `carrusel-formatos-f100k` (plantilla cuadrícula) + `banana` para las imágenes metafóricas.

---

### F06 · Personificación en scrapbook
- **Mecánica:** M7 · **Soporte:** S4 hoja espiral + stickers 3D · **Motor:** B + C
- **Referencia:** @profesiondelfuturo (4,89M) · 26.961 likes · 693 comentarios · 9 slides · https://www.instagram.com/p/DdPBiLxICxV/
- **Anatomía:**
  1. Hoja de cuaderno espiral, letra manuscrita en bolígrafo azul, subrayados rojos.
  2. Portada: el personaje viejo habla: "Soy ChatGPT, me hice viejo y me quedé atrás. Pero tranquilo…" (abuelito 3D con bastón).
  3. Slide 2: "Estos son los duros de hoy" + los 4 personajes en stickers.
  4. Slides 3-6: cada herramienta en primera persona: "Soy Claude, el mejor en analizar datos. Envíame los archivos…".
  5. Slide 7: "Y él es [el creador]" como personaje más, junto al abuelito.
  6. Slide 8: CTA curso gratuito. Slide 9: "Siempre lo amaremos, abuelito" (cierre emotivo y gracioso).
- **Por qué funciona:** convierte una lista de herramientas (aburrida) en un reparto de personajes con conflicto (el viejo vs. los nuevos). El creador entra como un personaje más de la historia: el CTA no se siente como corte.
- **Error típico:** personajes que solo dicen su función. Cada uno necesita una personalidad y una frase que la delate.
- **Prompt:**
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
- **Skill:** `banana` (stickers) + `carrusel-formatos-f100k` (plantilla hoja espiral).

---

### F07 · Chuleta en lapicero (2 slides)
- **Mecánica:** M8 · **Soporte:** S4 hoja rayada + bolígrafo · **Motor:** C
- **Referencia:** @profesiondelfuturo (4,89M) · **41.979 likes** · 429 comentarios · **2 slides** · https://www.instagram.com/p/DdMAhxsHKa6/
- **Anatomía:**
  1. Slide 1: título subrayado ("Atajos útiles de computadora") + un nodo central encerrado ("Ctrl") + una llave que abre ~30 filas "atajo — qué hace". Densa a propósito.
  2. Slide 2: casi vacía. "Créame, esta cuenta no le va a aparecer otra vez, así que ¡Sígala!"
- **Por qué funciona:** la slide 1 es imposible de memorizar → se guarda. La slide 2 usa escasez ("no te va a aparecer otra vez") para convertir el guardado en seguidor. Es el post con más likes de toda la lista con solo 2 slides.
- **Error típico:** repartir la chuleta en 8 slides "para que se lea mejor". La densidad es el gancho: tiene que parecer una hoja que vale la pena capturar.
- **Prompt:**
```
Hazme una chuleta de 2 slides sobre [TEMA con muchos datos cortos: atajos, prompts, frases, medidas].
Slide 1: título corto subrayado + 1 concepto central en un recuadro + 20 a 30 filas con formato "[dato] — [qué hace en 1-3 palabras]", agrupadas en ramas si hay categorías. Todo tiene que caber en UNA hoja.
Slide 2: una sola frase que invite a seguirme con escasez honesta, en mis palabras, tuteando. Ej.: "Créeme: esta cuenta no te va a volver a aparecer. Sígueme."
Verifica cada dato: si no estás 100% segura de uno, quítalo. Un dato falso en una chuleta arruina el guardado.
Formato visual: letra manuscrita azul sobre hoja de cuaderno rayada con margen rojo y espiral a la izquierda.
```
- **Skill:** `carrusel-formatos-f100k` (plantilla hoja espiral, texto en HTML: 30 filas NO se piden al modelo de imagen).

---

### F08 · Consejo en agenda
- **Mecánica:** M2 paso a paso íntimo · **Soporte:** S5 agenda/planner · **Motor:** C
- **Referencia:** @fedecaball (1,15M seguidores) · 5.814 likes · **1.602 comentarios** · 4 slides · https://www.instagram.com/p/Dbv24imETWE/
- **Anatomía:**
  1. Foto cercana de una agenda con pestañas (D · M · A), letra de molde a mano sobre renglones.
  2. Slide 1: el hábito como instrucción: "Adopta el hábito de subir esta historia todos los domingos por la mañana…"
  3. Slides 2-3: cómo se hace (sticker "Regalo", qué escribir, qué regalar) con ✓.
  4. Slide 4: el porqué ("Las ventas empiezan en una conversación") + "Si quieres que analice tu perfil, comenta ANÁLISIS".
- **Por qué funciona:** 4 slides, una sola acción concreta para el domingo. Se siente como un secreto anotado, no como un curso. El CTA ofrece algo personal (análisis) → 1.602 comentarios.
- **Error típico:** dar 5 hábitos. La potencia está en UNA acción con día y hora.
- **Prompt:**
```
Escribe un carrusel de 4 slides "consejo en agenda" con UNA sola acción que mi audiencia puede hacer esta semana para [RESULTADO].
Slide 1: "Adopta el hábito de [acción concreta] todos los [día] por la [momento]…" (termina en puntos suspensivos).
Slide 2: cómo se hace, en 3 frases cortas (dónde, qué poner, qué escribir literal entre comillas).
Slide 3: qué ofrecer o qué hacer después, con 3 opciones marcadas con ✓ + la frase clave de fondo.
Slide 4: el porqué en 2 frases + "Si quieres que [ayuda personal], comenta: [PALABRA] y te escribo por mensaje."
Máx. 35 palabras por slide. Tutea (nada de voseo). Tono de nota personal.
Fondo (sin texto): foto de cerca de una agenda de papel gris claro con pestañas de mes y renglones, luz natural, formato 4:5.
```
- **Skill:** `carrusel-formatos-f100k` (plantilla agenda).

---

### F09 · Tu foto fija + tarjeta
- **Mecánica:** M2 paso a paso · **Soporte:** S6 · **Motor:** A
- **Referencia:** @karoempowerment (340K) · likes ocultos · 73 comentarios · 5 slides · https://www.instagram.com/p/DdNER9QGI1l/
- **Anatomía:**
  1. La MISMA selfie de fondo en las 5 slides (mirada fuera de cámara, luz cálida).
  2. Encima, una tarjeta blanca con bordes redondeados en el tercio inferior que cambia en cada slide.
  3. Tarjeta: número en círculo de color · título con palabras resaltadas en rosa · ✓ o íconos · ícono de la herramienta.
  4. Portada: "Cómo pedirle a ChatGPT atraer 1.000 seguidores todos los días a tu Instagram" con la cifra en caligrafía.
  5. Cierre: tarjeta con "Comenta SEPTIEMBRE" + descripción de la masterclass.
- **Por qué funciona:** tu cara da confianza en cada swipe sin producir 5 fotos; la tarjeta hace que el contenido se vea ordenado. Barato de fabricar: 1 foto + 5 tarjetas.
- **Error típico:** tarjeta tapándote la cara. Va en el tercio inferior o al lado de tu mirada.
- **Prompt:**
```
Crea un carrusel de 5 slides "foto fija + tarjeta" sobre [CÓMO LOGRAR X con Y].
Todas las slides usan la misma foto mía de fondo; solo cambia la tarjeta.
Slide 1 (tarjeta portada): "Cómo [lograr resultado con cifra]" — marca la cifra para ir en caligrafía.
Slides 2-4 (tarjeta paso): número · título de máx. 8 palabras con 2 palabras a resaltar entre **asteriscos** · 3 viñetas con ✓ (o el prompt exacto entre comillas si el paso es "pídele esto").
Slide 5 (tarjeta CTA): "Comenta [PALABRA]" + 2 líneas de qué recibe.
Máx. 40 palabras por tarjeta. Dime qué foto mía funciona mejor (mirada, encuadre, espacio libre abajo).
```
- **Skill:** `carrusel-organico-f100k` (foto + bloques de texto) o `carrusel-render-formula100k` (foto hero + tarjeta).

---

### F10 · Anáfora sobre fotos de tu vida (marca personal)
- **Mecánica:** M4 · **Soporte:** S7 foto a sangre · **Motor:** A
- **Referencia:** @jun_yuh (5,31M) · 9.047 likes · 105 comentarios · 11 slides · https://www.instagram.com/p/Dc3-q8tkRup/
- **Anatomía:**
  1. Portada: "si aguantas la vergüenza UN MES, puedes cambiar tu vida…" sobre selfie en el gym.
  2. Slide 2: la tesis ("a la gente no le da vergüenza ser mala en algo; le da vergüenza que la VEAN siendo mala").
  3. Slides 3-8: prefijo pequeño fijo "avergüénzate…" + frase grande con una palabra en *itálica* + remate pequeño abajo a la derecha ("todo experto tiene pruebas de haber sido principiante").
  4. Cada slide es una foto distinta de tu vida real (bolos, calle, cuaderno, noche).
  5. Slide 9-10: la conclusión. Slide 11: "sígueme para ver qué pasa si sigo" (reto de 30 días).
- **Por qué funciona:** el prefijo repetido marca el ritmo y cada foto real prueba que tú lo vives. El cierre convierte el carrusel en el capítulo 1 de un reto → seguir tiene sentido.
- **Error típico:** fotos de banco o todas en el mismo lugar. La variedad de escenas reales ES la prueba.
- **Prompt:**
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
- **Skill:** `carrusel-render-formula100k` (patrón hero background) · `clonador-carrusel-formula100k` con el link.

---

### F11 · Historia de origen con edades
- **Mecánica:** M6 · **Soporte:** S7 + collages de 3 fotos · **Motor:** A
- **Referencia:** @jun_yuh (5,31M) · 9.163 likes · 149 comentarios · 14 slides (2 son video) · https://www.instagram.com/p/DcV_B4eETq5/
- **Anatomía:**
  1. Portada: foto de infancia real + "9 años. lo único que quería era mantener la paz…"
  2. Slides 2-4: el contexto familiar con fotos viejas (traducía para su papá).
  3. Una FRASE MOTIVO que se repite y muta: "no hagas escándalo" / "no destaques" / "quédate callado" → "hasta que 'quédate callado' se volvió… 'soy callado'".
  4. Marcas de edad como capítulos: 9 · 19 ("encontré una cámara… otra forma de esconderme") · 25.
  5. Giro: "hasta que empecé a contar historias que me daban miedo" + "y poco a poco 'quédate callado' desapareció".
  6. Hoy: "el niño que pasó años sin querer ser visto… ahora le habla a millones".
  7. Puente a oferta: "por eso creé [producto]… no porque el mundo necesite más contenido, sino porque tú también necesitas recuperar tu voz". CTA "comenta MY VOICE".
- **Por qué funciona:** la frase motivo que cambia de forma es el hilo que se sigue swipe a swipe; las edades dan sensación de avance. El producto aparece como el final lógico de la historia, no como anuncio.
- **Error típico:** contar la historia sin frase motivo. Sin un hilo que mute, son 14 fotos con texto.
- **Prompt:**
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
- **Skill:** `storytelling-filosofico-f100k` / `guionizacion-humanizada` (voz) + `carrusel-render-formula100k`.

---

### F12 · Etiquetas de papel sobre foto
- **Mecánica:** M6 historia (lista de veces) · **Soporte:** S9 · **Motor:** A
- **Referencia:** del deck de estilos de FÓRMULA 100K (sin link ni métricas) · portada "Tengo 37 años y estas son TODAS las veces que empecé de nuevo" · ~9 slides.
- **Anatomía:**
  1. Foto tuya de espaldas caminando (no se ve la cara: es universal).
  2. La frase partida en tiras de papel kraft y rosa, rasgadas y un poco giradas, apiladas.
  3. Palabras clave ("37", "TODAS") en letra hueca gigante sobre tira rosa.
  4. Garabatos rosas mínimos (estrella, rayitas).
  5. Slides siguientes: una "vez que empecé de nuevo" por slide, con año/edad.
- **Por qué funciona:** la cifra de edad + "TODAS" promete una lista honesta de fracasos; el papel rasgado dice "hecho a mano, real".
- **Error típico:** tiras perfectamente alineadas. El desorden leve es lo que se ve humano.
- **Prompt:**
```
Crea un carrusel "etiquetas de papel" de 9 slides con el gancho: "Tengo [MI EDAD] años y estas son TODAS las veces que [empecé de nuevo / fracasé / cambié de rumbo]".
Slide 1: divide el gancho en 6-8 tiras cortas (1-3 palabras cada una). Marca con [GRANDE] la edad y la palabra TODAS.
Slides 2-8: una vez por slide: "[edad o año]:" + qué dejé + qué aprendí (máx. 14 palabras, repartidas en 3-4 tiras).
Slide 9: dónde estoy hoy + pregunta: "¿cuántas veces has empezado de nuevo tú?"
Para cada slide sugiere una foto mía de esa etapa (de espaldas o sin mirar a cámara si es posible).
Estilo: tiras de papel kraft y rosa rasgadas, levemente giradas, letra redondeada negra.
```
- **Skill:** `carrusel-render-formula100k` (scrapbook crema ya trae papel y washi tape).

---

### F13 · Dibujado sobre tu foto
- **Mecánica:** presentación / "conóceme" · **Soporte:** S10 · **Motor:** A
- **Referencia:** del deck de estilos de FÓRMULA 100K (sin link ni métricas) · portada "New here? Let's get started — a lil about me".
- **Anatomía:**
  1. Tu foto en plano medio, centrada, con mucho cielo o pared libre arriba.
  2. Contorno amarillo dibujado alrededor de tu silueta.
  3. Texto manuscrito amarillo en el espacio libre + flechas que apuntan a ti ("nací en 2000 → Capricornio").
  4. Flecha "→" arriba a la derecha invitando al swipe.
  5. Slides siguientes: mismo lenguaje de garabatos sobre otras fotos; el texto se relaciona con el lugar o el cuerpo.
- **Por qué funciona:** los garabatos que apuntan a ti crean "diálogo visual": el ojo sigue la flecha hasta tu cara. Ideal para post fijado de bienvenida.
- **Error típico:** foto sin espacio libre. Si el texto va encima de la cara o de un fondo cargado, no se lee.
- **Prompt:**
```
Crea un carrusel de 6 slides "dibujado sobre mi foto" para mi post fijado de bienvenida.
Slide 1: "¿Nueva por aquí?" + "Empecemos" + 3 datos míos cortos con flecha hacia mí (ej. "mamá de 2 →").
Slides 2-5: un dato por slide sobre quién soy, qué hago, a quién ayudo y un resultado real; cada texto debe SEÑALAR algo de la foto (una flecha al café, un círculo a la laptop).
Slide 6: "Si te quedas, esto vas a encontrar:" + 3 temas + "sígueme".
Máx. 15 palabras por slide, letra manuscrita amarilla, contorno dibujado alrededor de mi silueta.
Para cada slide dime qué foto mía necesito y DÓNDE tiene que haber espacio libre (arriba, izquierda…).
```
- **Skill:** `carrusel-formatos-f100k` (`templates/garabato.html`: notas manuscritas, flechas, círculos, subrayados y contorno suelto con coordenadas sobre tu foto) · `clonador-carrusel-formula100k` si tienes la captura de la referencia.

---

### F14 · Masterclass escenificada (hot take en rotafolio)
- **Mecánica:** M12 · **Soporte:** S11 · **Motor:** B (o foto real en estudio)
- **Referencia:** del deck de estilos de FÓRMULA 100K (sin link ni métricas) · "Hot take: si hablas de 'equilibrio vida-trabajo' a los 22, te estás juntando con la gente equivocada".
- **Anatomía:**
  1. Foto de estudio: tú de pie junto a un rotafolio blanco, fondo de color saturado (morado), luz de set, boom de micrófono.
  2. En el rotafolio: "Hot take:" subrayado + la opinión escrita a mano, con la frase clave resaltada en amarillo y entre comillas.
  3. Slides siguientes: más hojas del rotafolio, primeros planos del texto, ángulos distintos "de cámara".
- **Por qué funciona:** el set de estudio da autoridad de clase; la letra a mano en la pizarra hace la opinión personal. La opinión polémica pide comentario.
- **Error típico:** una "opinión fuerte" que todos comparten. Si nadie la discutiría, no es hot take.
- **Prompt:**
```
Crea un carrusel de 5 slides "masterclass escenificada" con una opinión polémica sobre [TEMA DE MI NICHO].
Primero dame 3 hot takes candidatos y dime cuál genera más debate sin ser ofensivo.
Slide 1: "Opinión impopular:" + la opinión en máx. 22 palabras, con la frase clave entre comillas para resaltar en amarillo.
Slides 2-4: una hoja nueva del rotafolio por slide: el argumento, la evidencia, la excepción.
Slide 5: "¿Estás de acuerdo o no? Te leo en comentarios."
Prompt de imagen (sin texto en la hoja; el texto se pone después): "[descripción de mí], de pie con las manos atrás junto a un rotafolio blanco en un set de grabación con fondo morado saturado, luz de estudio, boom de micrófono entrando por arriba, foto realista, formato 4:5, hoja del rotafolio EN BLANCO".
```
- **Skill:** `higgsfield-carrusel-generador` (foto con tu cara) + texto en HTML · o foto real + `carrusel-render-formula100k`.

---

### F15 · Tipografía gigante con degradado
- **Mecánica:** M3 lista / M9 · **Soporte:** S12 · **Motor:** A (+ B para el objeto recortado)
- **Referencia:** del deck de estilos de FÓRMULA 100K · @marketingharry "WHY GOOD CONTENT GETS IGNORED" (sin métricas) · 10 slides.
- **Anatomía:**
  1. Portada: fondo blanco limpio; titular ultra bold en mayúsculas, negro sólido + UNA palabra en degradado brillante (rosa → naranja).
  2. Debajo, un objeto o rostro recortado provocador (bebé bostezando = contenido que aburre).
  3. Formas 3D flotantes de color en las esquinas + contador "1/10".
  4. Slides intermedias: fondo blanco o gris muy claro, bloques tipográficos jerárquicos, sin ruido.
- **Por qué funciona:** la palabra en degradado es lo único de color → es lo que se lee primero; la foto literal (bebé bostezando) traduce el concepto en medio segundo.
- **Error típico:** degradado en todo el titular. Solo UNA palabra, la emocional.
- **Prompt:**
```
Crea un carrusel de 10 slides "tipográfico con degradado" sobre [PROBLEMA de mi audiencia].
Slide 1: titular de máx. 5 palabras en mayúsculas; marca con [DEGRADADO] la ÚNICA palabra emocional. Propón un objeto o rostro recortado que traduzca el titular literalmente (con humor).
Slides 2-9: una razón por slide: título de 4-6 palabras + 2 líneas de explicación + 1 dato o ejemplo.
Slide 10: resumen en 1 frase + "guárdalo".
Estilo: fondo blanco, tipografía sans ultra bold negra, palabra clave en degradado [COLOR 1] → [COLOR 2], formas 3D flotantes de color en las esquinas, contador "N/10" arriba a la derecha.
Prompt de imagen del recorte: "[objeto/rostro] recortado sobre fondo blanco puro, foto de estudio, alto detalle, sin texto".
```
- **Skill:** `carrusel-render-formula100k` o `clonador-carrusel-formula100k` · `banana` para el recorte.

---

### F16 · Ilustrado kawaii
- **Mecánica:** M2 / M3 educativo · **Soporte:** S13 · **Motor:** B + A
- **Referencia:** del deck de estilos de FÓRMULA 100K · "Clínica Somno — Aprende a descansar en tus días libres" (sin métricas).
- **Anatomía:**
  1. Portada: personaje tierno ilustrado en el centro (con la emoción del problema: ojos en espiral, gato colgando).
  2. Fondo blanco con detalles mínimos; titular bold azul oscuro + subtítulo azul claro con palabras resaltadas.
  3. Slides intermedias: 1 consejo por slide, una escena del personaje + recuadro de bordes redondeados con la información.
- **Por qué funciona:** el personaje exagera la emoción del lector (agotamiento) sin mostrar a una persona real; el recuadro redondeado separa "dibujo" de "dato".
- **Error típico:** cambiar el diseño del personaje entre slides. Genera primero una hoja de personaje y úsala de referencia.
- **Prompt:**
```
Crea un carrusel ilustrado kawaii de 7 slides para [NEGOCIO] sobre [PROBLEMA COTIDIANO de su cliente].
Primero define UN personaje: aspecto, ropa, color de pelo, 1 rasgo distintivo (lo repetimos igual en todas).
Slide 1: titular educativo en 2 niveles (bold oscuro + subtítulo claro) + escena del personaje sintiendo el problema de forma exagerada y tierna.
Slides 2-6: 1 consejo por slide: título de pregunta ("¿Cómo volver a dormir?") + escena del personaje haciendo el consejo + recuadro redondeado con máx. 25 palabras.
Slide 7: cierre con el personaje feliz + CTA a [SERVICIO].
Prompt de ilustración por slide: "ilustración kawaii de [personaje], trazo limpio, colores pastel azul y amarillo, fondo blanco, sin texto".
```
- **Skill:** `carrusel-ilustrado-formula100k` (hoy hace Xiaohei blanco y negro: adaptar el estilo al pedirlo) · `banana`.

---

### F17 · Tier list
- **Mecánica:** M9 ranking · **Soporte:** S16 tabla por niveles · **Motor:** A
- **Referencia:** @lucureau (426K seguidores) · 2.220 likes · 62 comentarios · **1 slide** · https://www.instagram.com/p/DbMiGmbgOhX/
- **Anatomía:**
  1. Título "Tier List de formatos de contenido".
  2. 4 filas S · A · B · C con colores rojo → verde y una etiqueta con opinión ("Viraliza 90% de las veces", "Ni debería ser opción").
  3. En cada fila, 3 miniaturas con nombre corto debajo.
  4. Caption: "¿Tú cambiarías algo?".
- **Por qué funciona:** todos tienen opinión sobre un ranking → debate en comentarios. Se entiende de un vistazo.
- **Error típico:** un ranking "diplomático" donde todo sale bien. La fila C polémica es la que trae comentarios.
- **Prompt:**
```
Hazme una tier list de [8-12 opciones de mi nicho: herramientas, formatos, estrategias].
Filas: S (etiqueta con opinión fuerte), A, B, C (etiqueta que provoque: "ni debería ser opción").
Pon al menos UNA opción popular en C y explica por qué en 1 línea (ahí está el debate).
Para cada opción: nombre de máx. 3 palabras + qué miniatura usar.
Si hago versión carrusel: slide 1 la tabla completa; slides 2-5 una fila por slide con el porqué de cada posición; slide 6 "¿qué moverías tú? coméntalo".
Caption: termina con una pregunta que pida su propia tier list.
```
- **Skill:** gap → `carrusel-formatos-f100k` (plantilla tabla) · hoy: `carrusel-render-formula100k` a mano.

---

### F18 · Comparación visual con cifras
- **Mecánica:** M9 · **Soporte:** S15 objetos en fila · **Motor:** B + A
- **Referencia:** @estaciondemusculacion (5,75M seguidores) · **194.212 likes** · 819 comentarios · 5 slides · https://www.instagram.com/p/DbeQ2lwkTkq/
- **Anatomía:**
  1. Fondo negro. Titular serif crema "CAMPEONES DE PROTEÍNA" + subtítulo en naranja que rompe una creencia ("NO SE NECESITA POLVO") + "Valores aproximados por 100 g".
  2. 6 alimentos reales apilados en columnas, ordenados de mayor a menor, con la cifra grande arriba (31 g, 29 g…) y el nombre abajo.
  3. Slides 2-4: el mismo molde con otro nutriente ("LA NARANJA NO ES LA GANADORA").
  4. Slide 5: "SÍGUEME para más consejos de…".
- **Por qué funciona:** la altura de las columnas ES el gráfico: se entiende sin leer. El subtítulo que contradice una creencia ("la naranja no gana") da la sorpresa. Con 4 tablas iguales se guarda como referencia.
- **Error típico:** cifras inventadas o sin unidad. Un dato falso en una comparación la vuelve polémica por la razón equivocada.
- **Prompt:**
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
- **Skill:** `banana` (fondos) + `carrusel-formatos-f100k` (capa de cifras) · `infografia-reel-formula100k` para versión video.

---

### F19 · Mapa visual
- **Mecánica:** M10 · **Soporte:** S16 concepto central + ramas · **Motor:** A
- **Referencia:** @delimonada (77,5K seguidores) · **23.306 likes** · 295 comentarios · **1 slide** · https://www.instagram.com/p/DPt-2VHDvFW/
- **Anatomía:**
  1. Fondo gris claro, minimalista. En el centro, grande: "Hazme un Videíto".
  2. Líneas finas en ángulo recto a ~13 ramas: planeación, guion visual, grabación "(y mil tomas fallidas)", corrección de color, subida con copy…
  3. Handle abajo entre líneas. Caption: "me faltaron agregar más puntos 😅".
- **Por qué funciona:** revela el trabajo invisible detrás de algo que parece simple ("un videíto") → se comparte a clientes que regatean. Con 77K seguidores sacó 23K likes: sale de tu audiencia.
- **Error típico:** ramas sin humor ni detalle. Los paréntesis honestos ("y mil tomas fallidas") son los que se comparten.
- **Prompt:**
```
Hazme un mapa visual de 1 slide que muestre todo el trabajo invisible detrás de "[LO QUE MIS CLIENTES CREEN QUE ES FÁCIL, ej. 'hazme un logo rapidito']".
Centro: esa frase tal como la dice el cliente (con el diminutivo si aplica).
12-14 ramas: cada una un paso real del proceso en máx. 4 palabras; en 3 de ellas agrega un paréntesis honesto y con humor.
Ordena las ramas en sentido horario siguiendo el proceso real.
Estilo: fondo gris muy claro, texto negro, líneas finas en ángulo recto, centro en tipografía bold grande, mucho aire.
Caption: 2 líneas + "¿qué me faltó?".
```
- **Skill:** gap → `carrusel-formatos-f100k` (plantilla mapa) · alternativa: `excalidraw-diagram`.

---

### F20 · Collage de muchas señales
- **Mecánica:** M11 · **Soporte:** S14 recortes con etiquetas · **Motor:** B + A
- **Referencia:** @cvcwellness (370K seguidores) · **27.777 likes** · 696 comentarios · 4 slides · https://www.instagram.com/p/DTrVUEsjsTC/
- **Anatomía:**
  1. Slides 1-3: fondo negro, título serif ("How to Exit the Matrix") + subtítulo en itálica.
  2. 25-30 recortes (objetos, personas, estatuas, productos) con una etiqueta blanca de 2-4 palabras cada uno ("bloquea la luz azul", "cultiva tu comida"); tachones rojos en lo que hay que dejar.
  3. Slide 4: cambia a lienzo claro tipo póster con la oferta ("DM o comenta REWILD") + testimonios en capturas.
- **Por qué funciona:** el cerebro intenta identificar cada recorte uno por uno → tiempo de permanencia alto; se siente "mucha información". La oferta llega cuando el lector ya invirtió atención.
- **Error típico:** menos de 15 elementos. La densidad es el gancho; con pocos parece un moodboard.
- **Prompt:**
```
Crea un carrusel "collage de señales" de 4 slides sobre [TRANSFORMACIÓN que ofrezco].
Slides 1-3: cada una con un título tipo manifiesto ("Cómo salir de [problema]", "Tu [plan] para [año]", "La auditoría de [tema]") + subtítulo en itálica.
Para cada una, 20-25 elementos: acción de máx. 4 palabras + qué recorte visual la representa (objeto o figura reconocible). Marca con [TACHAR] lo que hay que dejar de hacer.
Slide 4: oferta en formato póster: pregunta + 4 beneficios con • + "comenta [PALABRA] y te mando info" + dónde van 2 testimonios reales.
Prompt de imagen por recorte: "[objeto] recortado, fondo transparente, estilo collage de revista vintage".
No uses marcas registradas en los recortes ni afirmaciones de salud sin respaldo.
```
- **Skill:** `banana` (recortes) + `carrusel-formatos-f100k` (composición) · hoy: `carrusel-render-formula100k` (scrapbook).

---

## LAS 17 FICHAS G (lo que la v1 dejó fuera + 2 sumadas el 17-sep)

G01–G13 vienen de la **Guía de Formatos del Grimorio** (carruseles con `soporte: 'carrusel'`); su
anatomía completa vive en `references/grimorio-carruseles.md`, que se regenera con
`scripts/sincronizar-grimorio.mjs` y FALLA si el Grimorio suma un carrusel que aquí no está mapeado.
G14 y G15 son mecánicas que solo vivían dentro de la guía maestra de 25 estilos (estilos 15 y 14).
G16 y G17 se sumaron el 17-sep-2026 desde dos carruseles reales: mirados slide por slide y convertidos en ficha.
El VISUAL detallado y los prompts por plataforma (Claude · Gemini · ChatGPT · HTML en cualquier chat)
de las 37 fichas están en `references/prompts-por-plataforma.md`.

Cuatro carruseles del Grimorio NO son ficha nueva porque su mecánica ya estaba:
`carrusel-paso-a-paso` → M2 (F04, F08, F09) · `carrusel-comparativo` → M9 (F18, con maqueta A│B en S20) ·
`carrusel-storytelling` → M6 (F11, F12) · `infografia-ia` → M10 (F19).

---

### G01 · Checklist guardable
- **Mecánica:** M13 · **Soporte:** S21 casillas (alternativa S4 hoja espiral con `check`) · **Motor:** A
- **Grimorio:** `carrusel-checklist` · **Referencia:** @savingwithben · ≈1.780 likes · https://www.instagram.com/p/DOsxgAViKxq/ (la del Grimorio, @serinformarketing DKMXMKotQef, está MUERTA: «Media not found» el 14-sep) · ojo: trae 12 tareas por slide, un checklist por tipo de persona
- **Anatomía:** 1) promesa de revisión + miedo a equivocarte ("Antes de publicar… revisa todo esto") · 2) qué te juegas si lo saltas · 3-7) un ítem por slide con su casilla · penúltima: el error que casi todos cometen · cierre: "guárdalo para tu próxima [tarea]".
- **Por qué funciona:** se guarda como herramienta que vas a volver a usar; cada ítem que el lector NO hace es un impulso de guardar.
- **Error típico:** ítems vagos ("revisa la calidad"). Cada casilla tiene que poder marcarse sí/no en 5 segundos.
- **Prompt de guion:**
```
Escribe un carrusel checklist de 8 slides para [MI NICHO] sobre lo que hay que revisar ANTES de [TAREA CONCRETA].
Slide 1: "Antes de [tarea]… revisa esto" + el miedo concreto a equivocarse (máx. 12 palabras).
Slide 2: qué pierdes si te saltas la revisión, con una consecuencia real (no "te irá mal").
Slides 3-7: un ítem por slide. Formato: verbo en imperativo + objeto concreto (máx. 8 palabras) + 1 línea de cómo comprobarlo.
Cada ítem debe poder responderse sí/no en 5 segundos.
Slide 8: el error que casi todos cometen + "Guárdalo para tu próxima [tarea]".
Tutea. Entrégalo en tabla slide | texto grande | texto chico.
```
- **Fabrica:** `carrusel-formatos-f100k` (papel.html `check` o HTML S21).

---

### G02 · Noticia del nicho
- **Mecánica:** M14 · **Soporte:** S26 periódico (alternativa S17 dark neón) · **Motor:** A
- **Grimorio:** `carrusel-noticias` · **Referencia:** @ramiro.cubria · 11.586 likes · 12.640 comentarios · https://www.instagram.com/p/DWkCiIHiYkz/ · ojo: la bajada práctica es un paso a paso y el CTA pide comentar para recibir un PDF
- **Anatomía:** 1) titular + etiqueta "ÚLTIMA HORA" o fecha · 2-3) qué pasó en lenguaje simple · 4-5) por qué te importa a ti · cierre: tu opinión + CTA.
- **Por qué funciona:** la actualidad da urgencia y te vuelve la fuente del nicho.
- **Error típico:** contar la noticia y no bajarla a la vida del lector. Sin slides 4-5 es un resumen de prensa.
- **Prompt de guion:**
```
Tengo esta noticia de mi nicho: [PEGA EL LINK O EL TEXTO + FECHA].
Escribe un carrusel de 6 slides tipo portada de periódico:
Slide 1: titular de máx. 10 palabras + etiqueta "ÚLTIMA HORA" o la fecha real.
Slides 2-3: qué pasó, en frases de máx. 20 palabras, sin jerga. Cita la fuente.
Slides 4-5: "Qué cambia para ti si eres [mi cliente ideal]": 2 consecuencias prácticas.
Slide 6: mi opinión en 1 frase + "Comenta [PALABRA] si quieres que te explique cómo aplicarlo".
No inventes datos que no estén en la fuente; si falta algo, márcalo [VERIFICAR]. Tutea.
```
- **Fabrica:** `carrusel-formatos-f100k` (HTML S26).

---

### G03 · ¿Qué tipo de X eres?
- **Mecánica:** M15 · **Soporte:** S17 piel pastel emoji (alternativa S13 ilustrado, un personaje por tipo) · **Motor:** A (o B + A)
- **Grimorio:** `que-tipo-eres` · **Referencia:** @rayamarketing_ · 2.678 likes · https://www.instagram.com/p/DW-KAnFjLtC/ · cada tipo se muestra como «kit» de 5 objetos
- **Anatomía:** 1) la pregunta · 2-N) un arquetipo por slide: nombre + descripción + rasgo reconocible · cierre: "comenta cuál eres / etiqueta al tipo 3".
- **Por qué funciona:** todo el mundo quiere saber "cuál soy" y etiquetar a alguien.
- **Error típico:** arquetipos genéricos (el "organizado", el "creativo"). El rasgo tiene que ser una escena que da vergüenza reconocer.
- **Prompt de guion:**
```
Escribe un carrusel "¿Qué tipo de [ROL DE MI CLIENTE] eres?" de 6 slides.
Slide 1: la pregunta + "desliza y elige".
Slides 2-5: 4 arquetipos. Para cada uno: número + nombre con humor (2-3 palabras) + 1 emoji + 2 frases de descripción + "Te delata:" y una escena concreta y un poco vergonzosa (máx. 15 palabras).
Que ningún tipo sea "el correcto": cada uno tiene una fortaleza y un punto ciego.
Slide 6: "¿Cuál eres? Comenta el número" + "etiqueta a quien es el 3".
Tutea. Tabla slide | texto grande | texto chico.
```
- **Fabrica:** `carrusel-formatos-f100k` (HTML S17) · `carrusel-ilustrado-formula100k` si va con personajes.

---

### G04 · Lo que nadie te dice de X (mito / realidad)
- **Mecánica:** M16 · **Soporte:** S20 doble paleta · **Motor:** A
- **Grimorio:** `carrusel-secreto` · también estilo 12 «Mitos vs realidad» de la guía maestra · **Referencia:** @marinaaurorabustamante · 514 likes · https://www.instagram.com/p/DO6cdKjERYw/ · **solo estilo**: la referencia NO trae el molde «lo que te dicen / lo que pasa» (cada slide es un consejo); falta un ejemplo que muestre la mecánica
- **Anatomía:** 1) "Lo que nadie te dice de [tema]" + a quién le hablas · 2) lo que SÍ te dicen todos, entre comillas · 3-7) una verdad por slide: "Lo que te dicen:" arriba / "Lo que pasa:" abajo + un detalle de tu experiencia · penúltima: la verdad más incómoda, sola y grande · cierre: una línea de alivio + guardar.
- **Por qué funciona:** el vacío de información da curiosidad y la honestidad te separa del mar de tips.
- **Error típico:** "verdades" que todo el mundo ya dice. Si tu competencia la publicaría igual, no es secreto.
- **Prompt de guion:**
```
Escribe un carrusel "Lo que nadie te dice de [TEMA DESEADO por mi cliente]" de 8 slides, para [QUIÉN ESTÁ POR EMPEZAR].
Slide 1: el título + a quién le hablo.
Slide 2: la frase que todos repiten, entre comillas.
Slides 3-7: 5 verdades. Cada una en 2 bloques: "Lo que te dicen:" (máx. 8 palabras) / "Lo que pasa:" (máx. 20 palabras) + un detalle real de mi experiencia: [PEGA 5 COSAS QUE TE PASARON].
Slide 8: la verdad más incómoda sola + "y aun así vale la pena si…" + "guárdalo".
No uses verdades que diría cualquiera de mi nicho. Tutea.
```
- **Fabrica:** `carrusel-formatos-f100k` (HTML S20).

---

### G05 · Biblioteca de recursos
- **Mecánica:** M17 · **Soporte:** S25 bento (alternativa S2 fondo blanco + captura) · **Motor:** A
- **Grimorio:** `carrusel-recursos` · **Referencia:** @brandcrops · 182 likes · 47 comentarios · https://www.instagram.com/p/DRAIqFmjJMa/ · ojo: agrupa 5 herramientas por slide, sin slide de flujo
- **Anatomía:** 1) "Herramientas que nos salvan en el día a día" · 2-6) una por slide: nombre + para qué sirve + caso de uso · penúltima: cómo combinarlas · cierre: "comenta [palabra] y te mando la lista completa".
- **Por qué funciona:** nadie memoriza 6 herramientas: las archiva. El "comenta y te mando" multiplica comentarios.
- **Error típico:** listar herramientas que no usas. Sin un caso de uso tuyo por herramienta es una lista de Google.
- **Prompt de guion:**
```
Escribe un carrusel de 8 slides con [N=5] herramientas/recursos que YO uso para [RESULTADO de mi nicho]. Mis herramientas: [LISTA + para qué las uso].
Slide 1: "[N] herramientas que me ahorran [TIEMPO/DINERO CONCRETO]".
Slides 2-6: una por slide → nombre + precio (gratis/pago) + "Para:" (máx. 10 palabras) + "Yo la uso cuando…" (un caso real, máx. 15 palabras). Indica la captura de pantalla que va en cada slide.
Slide 7: cómo las combino en un flujo de 3 pasos.
Slide 8: "Comenta [PALABRA] y te mando la lista con links".
No inventes precios: márcalos [VERIFICAR]. Tutea.
```
- **Fabrica:** `carrusel-formatos-f100k` (HTML S25) + `capturas-tutorial-formula100k` para las capturas.

---

### G06 · Glosario de tu nicho
- **Mecánica:** M18 · **Soporte:** S18 editorial revista (alternativa S4 hoja espiral) · **Motor:** A
- **Grimorio:** `carrusel-glosario` · **Referencia:** @cem.ve · 14 likes · https://www.instagram.com/p/DQxIMFgFKbC/ · **solo estilo** (2 términos por slide, sin ejemplo) · candidato mejor sin anclar: @glorymar.negron · 13.956 likes · https://www.instagram.com/p/DT0-BIUkdJs/
- **Anatomía:** 1) la jerga que confunde, nombrada · 2-7) un término por slide: término grande + definición en una frase + mini-ejemplo de tu rubro en letra chica · cierre: "guárdalo" + seguir.
- **Por qué funciona:** quita la sensación de estar perdido y se comparte a principiantes.
- **Error típico:** definir con otra palabra técnica. La definición sin ejemplo no se entiende.
- **Prompt de guion:**
```
Escribe un carrusel glosario de 8 slides con los 6 términos que más confunden a [PRINCIPIANTE de mi nicho].
Slide 1: "¿No entiendes qué es [término 1], [término 2] o [término 3]? Este es tu glosario".
Slides 2-7: TÉRMINO en mayúsculas + cómo se pronuncia si es en inglés + definición de máx. 15 palabras SIN usar otra palabra técnica + "Ejemplo:" de mi rubro (máx. 15 palabras).
Slide 8: "Guárdalo para cuando lo vuelvas a leer" + "¿qué palabra te falta? coméntala".
Tutea.
```
- **Fabrica:** `carrusel-formatos-f100k` (HTML S18 o papel.html).

---

### G07 · Mini caso de estudio
- **Mecánica:** M19 · **Soporte:** S17 piel dato gigante (09) + capturas reales (S2) · **Motor:** A
- **Grimorio:** `carrusel-caso-estudio` · **Referencia:** @soldea · 283 likes · https://www.instagram.com/p/DWkGZMUj8fU/
- **Anatomía:** 1) gancho con el hallazgo ("mis mejores resultados no vienen de…") · 2) el dato concreto · 3-6) qué hiciste distinto + por qué funcionó · cierre: la lección replicable + guardar.
- **Por qué funciona:** tu dato propio da la credibilidad que el consejo genérico no tiene.
- **Error típico:** el dato sin captura. Si no se ve la prueba, se lee como humo.
- **Prompt de guion:**
```
Tengo este resultado real: [DATO + PERIODO + CAPTURA DISPONIBLE] y esto fue lo que cambié: [LO QUE HICISTE].
Escribe un mini caso de estudio de 7 slides:
Slide 1: el hallazgo que contradice lo esperado (máx. 12 palabras).
Slide 2: el número grande + unidad + periodo + "captura:" (qué captura va).
Slides 3-6: una decisión por slide → qué hice (máx. 10 palabras) + por qué creo que funcionó (máx. 20) + qué NO sé todavía si aplica.
Slide 7: la lección en 1 frase que el lector puede probar esta semana + "guárdalo".
Usa SOLO mis números. Nada de promedios que no te di. Tutea.
```
- **Fabrica:** `carrusel-caso-exito-f100k` (cifras verificadas) o `carrusel-formatos-f100k` (HTML S17-09).

---

### G08 · Molde para copiar
- **Mecánica:** M20 · **Soporte:** S27 nota del celular (mensajes) o S24 terminal (prompts) · **Motor:** A
- **Grimorio:** `carrusel-plantilla` · **Referencia:** @estebaneras.a · 140 comentarios · https://www.instagram.com/p/DSGer-tD5PG/ · **solo estilo**: es un tutorial con capturas, no un molde con [huecos]; falta un ejemplo que muestre la mecánica
- **Anatomía:** 1) la promesa del molde y lo que ahorra · 2) el resultado de usarlo (captura o número) · 3-6) un bloque del molde por slide, texto fijo escrito y [huecos] resaltados + ejemplo relleno en letra chica · cierre: CTA de palabra clave para recibirlo en texto.
- **Por qué funciona:** el lector se lleva un activo que usa esa semana; el "comenta y te lo mando" llena comentarios.
- **Error típico:** huecos sin ejemplo. "[tu propuesta de valor]" sin un ejemplo relleno no lo completa nadie.
- **Prompt de guion:**
```
Este es un mensaje/guion que uso en mi negocio y funciona: [PEGA EL TEXTO REAL + qué resultado te dio].
Conviértelo en un carrusel molde de 7 slides:
Slide 1: "[El mensaje que uso para X], listo para copiar" (máx. 12 palabras).
Slide 2: el resultado real de usarlo + qué captura va.
Slides 3-6: un bloque del molde por slide, con el texto fijo tal cual y los huecos entre [CORCHETES EN MAYÚSCULAS]. Debajo: "Ejemplo:" con ese bloque ya relleno para [cliente ficticio de mi rubro].
Slide 7: "Comenta [PALABRA] y te lo mando en texto para copiar".
No cambies mi texto salvo para quitar datos privados. Tutea.
```
- **Fabrica:** `carrusel-formatos-f100k` (HTML S27 o S24).

---

### G09 · Frase cortada entre slides (swipe-reveal)
- **Mecánica:** M21 · **Soporte:** S17 piel bold (01) con el corte SIEMPRE abajo a la derecha · **Motor:** A
- **Grimorio:** `carrusel-swipe-embudo` · **Referencia:** @emprendeconcata · 560 likes · 248 comentarios · https://www.instagram.com/p/DY48PjolruI/ · **solo estilo**: es una lista de reglas, NO tiene frases cortadas entre slides; falta un ejemplo que muestre la mecánica
- **Anatomía:** 1) afirmación que reencuadra y termina cortada ("El problema no es tu precio, es…") · cada slide abre completando la anterior y cierra con otra cortada · el corte en el mismo lugar · penúltima: la revelación completa, la única que no termina cortada · cierre: CTA que cobra la tensión.
- **Por qué funciona:** cada swipe paga una deuda pequeña → deslizamiento completo (tiempo de permanencia).
- **Error típico:** que el corte no genere pregunta ("y además…"). Sin frases partidas es una lista.
- **Prompt de guion:**
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
- **Fabrica:** `carrusel-formatos-f100k` (HTML S17-01).

---

### G10 · Frases sueltas
- **Mecánica:** M22 · **Soporte:** S17 piel minimalista (02) o S7 tu foto a sangre · **Motor:** A
- **Grimorio:** `carrusel-frases` · **Referencia:** sin referencia válida · la del Grimorio (@impulsanegocios.es DTZv391Dh2E) está ROTA: es una sola imagen horizontal hecha con IA con texto ilegible, no un carrusel
- **Anatomía:** 1) "5 frases que te impulsan a…" · 2-6) una frase por slide, grande, mucho aire, misma tipografía; UNA palabra resaltada en color · cierre: "¿con cuál te quedas? coméntalo".
- **Por qué funciona:** se reenvían como identidad y el "cuál te quedas" da comentarios de bajo esfuerzo.
- **Error típico:** frases de Pinterest. Si no suenan a ti, nadie las asocia a tu cuenta.
- **Prompt de guion:**
```
Escribe 5 frases MÍAS (no citas famosas) para [MI CLIENTE] cuando [MOMENTO DIFÍCIL CONCRETO].
Básate en cosas que he dicho o vivido: [PEGA 3-5 IDEAS O FRASES TUYAS].
Cada frase: máx. 14 palabras, con una imagen concreta (no "cree en ti"), y marca con ==palabra== la ÚNICA palabra que carga el sentido.
Slide 1: "[N] frases para cuando [momento]".
Slide 7: "¿Con cuál te quedas? Comenta el número".
Tutea.
```
- **Fabrica:** `carrusel-formatos-f100k` (HTML S17-02) · `carrusel-render-formula100k` si va sobre tus fotos.

---

### G11 · Errores propios
- **Mecánica:** M23 · **Soporte:** S7 tu foto a sangre + MAYÚSCULAS en la parte clave · **Motor:** A
- **Grimorio:** `carrusel-errores-propios` · **Referencia:** @tania.villalobosc · 113 likes · https://www.instagram.com/p/Da5tAScFtVQ/ (cazada por mecánica el 14-sep; el Grimorio no tenía)
- **Anatomía:** 1) "¿Qué errores cometí como [profesión] cuando empecé?" + foto tuya real, no posada · 2-N) una confesión por slide: fecha, situación, qué hiciste; la parte clave en MAYÚSCULAS; cierre de peso · reflexión: "me dolieron, pero me hicieron mejor" · cierre: "¿cuál te sorprendió más?".
- **Por qué funciona:** contar un error con fecha compra más autoridad que un acierto: solo lo cuenta quien ya lo superó.
- **Error típico:** errores del espectador disfrazados de propios ("no publicaba seguido"). Tiene que dar un poco de vergüenza.
- **Prompt de guion:**
```
Soy [PROFESIÓN]. Estos son errores reales que cometí cuando empecé: [LISTA con año y qué pasó].
Escribe un carrusel de 7 slides:
Slide 1: "¿Qué errores cometí como [profesión] cuando empecé?".
Slides 2-5: un error por slide → año + situación concreta + qué hice. La parte clave EN MAYÚSCULAS (máx. 5 palabras). Termina con una frase de peso corta.
Slide 6: "Estos errores me dolieron, pero me hicieron mejor. Ojalá alguien me lo hubiera contado antes."
Slide 7: "¿Cuál te sorprendió más?" / "¿Qué hubieras hecho tú?".
No suavices ni conviertas el error en consejo. Máx. 35 palabras por slide. Tutea.
```
- **Fabrica:** `carrusel-render-formula100k` (tu foto + texto) · `carrusel-formatos-f100k` (split.html portada).

---

### G12 · Confesión a partir de una pregunta
- **Mecánica:** M24 · **Soporte:** S22 chat (la pregunta en burbuja) → S27 nota del celular para la respuesta · **Motor:** A
- **Grimorio:** `carrusel-confesion-personal` · **Referencia:** sin ejemplo público verificado todavía
- **Anatomía:** 1) la conversación + la pregunta íntima (el gancho es la pregunta) · 2-4) la situación cotidiana que contrasta con lo que esperan de ti · valida la objeción del lector · aprendizaje: 2 consejos numerados · cierre: VARIAS preguntas abiertas.
- **Por qué funciona:** la pregunta ajena da permiso para hablar de lo personal, y el cierre con varias preguntas llena los comentarios de historias.
- **Error típico:** una pregunta cómoda. Si no te da pudor contestarla, el formato no sirve.
- **Prompt de guion:**
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
- **Fabrica:** `carrusel-formatos-f100k` (HTML S22 + S27).

---

### G13 · De A a B con antesala
- **Mecánica:** M25 · **Soporte:** S28 barra de progreso (la barra NO avanza en la antesala: arranca en el primer paso) · **Motor:** A
- **Grimorio:** `carrusel-de-a-a-b` · **Referencia:** sin ejemplo público verificado todavía
- **Anatomía:** 1) "Cómo ir de [problema] a [resultado]" + "guía realista, sin hacks" · 2-3) validación emocional + 3 razones por las que cuesta, ninguna culpa al lector · 4) "funciona mejor si estás en [situación]" · pasos, uno por slide · reencuadre: "no necesitas hacerlo perfecto" · cierre: recurso con palabra clave.
- **Por qué funciona:** quien está en A no falla por falta de pasos, falla porque cree que el problema es suyo; la antesala le quita la culpa.
- **Error típico:** saltarse la antesala. Sin las slides 2-4 es un paso a paso más.
- **Prompt de guion:**
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
- **Fabrica:** `carrusel-formatos-f100k` (HTML S28).

---

### G14 · Antes / después
- **Mecánica:** M26 · **Soporte:** S1 dos fotos reales apiladas con rótulo fijo (o S20 doble paleta si el cambio es un número) · **Motor:** A
- **Origen:** estilo 15 «Antes / después dramático» de la guía maestra (no estaba en las 20 ni en el Grimorio como carrusel) · **Referencia:** @isabellaescobar · ≈16.061 likes · https://www.instagram.com/p/DXXrlp5jaRw/ (cazada por mecánica) · alternativa de servicio: @clinicaaeon.cl · https://www.instagram.com/p/DZKj2b-jqWJ/
- **Anatomía:** 1) par de fotos reales del MISMO tema: arriba el comienzo, abajo hoy, con el rótulo fijo («PRIMERO EMPIEZAS» / «LUEGO MEJORAS») · 2-N) otro par (cocina ↔ cocina, empaque ↔ empaque, puesto ↔ local) con el MISMO rótulo · variante con datos: split ANTES/DESPUÉS en doble paleta fría → cálida con la cifra y su prueba · cierre: pregunta («¿qué te pareció el cambio?») o CTA.
- **Por qué funciona:** el rótulo que no cambia hace que el ojo solo compare las fotos, y la foto fea del inicio es la que conecta (la referencia, con el mismo texto en las 4 slides, pasa de 16K likes).
- **Error típico:** un "después" sin prueba o con fotos que no son del mismo caso. Nunca inventes el resultado.
- **Prompt de guion:**
```
Tengo estos pares de fotos REALES de mi negocio: [LISTA: foto del inicio → foto de hoy, del mismo tema].
Arma un carrusel antes/después de [4-6] slides:
Rótulo fijo para todas (máx. 3 palabras arriba y 3 abajo): propón 3 opciones del tipo "PRIMERO EMPIEZAS / LUEGO MEJORAS" que suenen a mí.
Slides: un par por slide, ordenados del cambio más pequeño al más impactante. Para cada uno dime qué foto va arriba y cuál abajo, y que ambas muestren LA MISMA COSA.
Si el cambio se mide (ventas, clientas, seguidores): una slide en doble paleta con ANTES [dato] / DESPUÉS [dato] + qué captura lo prueba.
Última slide: "¿qué te pareció el cambio?" o CTA a [servicio].
Usa solo fotos y datos reales. Tutea.
```
- **Fabrica:** `carrusel-formatos-f100k` (HTML S20) · `carrusel-caso-exito-f100k` si es caso de clienta.

---

### G15 · Preguntas frecuentes en chat
- **Mecánica:** M27 · **Soporte:** S22 chat / DM con burbujas · **Motor:** A
- **Origen:** estilo 14 «FAQ tipo chat» de la guía maestra · **Referencia:** @taboadanunez.dental · https://www.instagram.com/p/DW6k_ktEWgT/ (cazada por mecánica; pocas métricas, usa burbuja de diálogo sobre un objeto del rubro, no pantalla de chat)
- **Anatomía:** 1) "Las [N] preguntas que me hacen antes de comprar [oferta]" · 2-N) una pregunta por slide en burbuja gris (lado del cliente) + tu respuesta en burbuja de color (tu lado), con hora y "visto" · cierre: "¿tienes otra? escríbeme [PALABRA] por DM".
- **Por qué funciona:** responde objeciones de venta en el formato donde de verdad se hacen (el DM) y se lee como conversación, no como anuncio.
- **Error típico:** preguntas inventadas y cómodas. Copia las que te llegan de verdad, con sus palabras.
- **Prompt de guion:**
```
Estas son preguntas REALES que me llegan por DM antes de comprar [MI OFERTA]: [PEGA 5 MENSAJES tal cual].
Escribe un carrusel de 7 slides en formato chat:
Slide 1: "Las 5 preguntas que me hacen antes de [comprar/agendar]".
Slides 2-6: una por slide → burbuja cliente (la pregunta con sus palabras, máx. 20) + burbuja mía (respuesta honesta, máx. 35 palabras, sin evadir precio ni tiempos). Pon hora a cada mensaje.
Slide 7: "¿Tienes otra? Escríbeme [PALABRA] por DM".
Tutea.
```
- **Fabrica:** `carrusel-formatos-f100k` (HTML S22).

---

### G16 · Vitrina de lo que construiste (N cosas que hice)
- **Mecánica:** M28 · **Soporte:** S29 fondo de color plano + pantalla en marco (captura o grabación) · **Motor:** A (capturas o grabaciones reales)
- **Origen:** carrusel sumado al recetario el 17-sep-2026 · **Referencia:** @nicolebrener_digital · 18.922 likes · **23.700 comentarios** · 7 slides (3 son video) · https://www.instagram.com/p/Dcy5upWjA22/ · ojo: el original vosea («metés», «registrás») y en la slide 3 los montos no cuadran; copia la forma, no el texto
- **Anatomía:** 1) portada con TU foto real (celebrando, en tu espacio de trabajo) + titular apilado «5 apps que [dejé de pagar] y las hice con [herramienta]» + stickers + el logo de la herramienta · 2-6) un ítem por slide sobre el MISMO fondo de color: «N. [Nombre que dice el beneficio]» + 1 línea de qué hace + la pantalla real en un marco tipo tablet que se sale por los lados (en 2 o 3 slides, la grabación de la pantalla usándose) · cierre: «Comenta [PALABRA]» entre stickers + qué te llevas («y te comparto una guía para crear las tuyas»).
- **Por qué funciona:** cada slide es PRUEBA, no promesa: la pantalla funcionando convence de que tú también puedes, y el CTA regala justo lo que falta para hacerlo (los prompts). Por eso 23.700 comentarios con 18.900 likes: la gente comenta más de lo que da like. Los nombres venden el ahorro («sin suscripción») y el fondo único hace que el ojo solo mire la pantalla.
- **Error típico:** mostrar maquetas bonitas que no usas o capturas vacías (sin datos): se nota y el CTA pierde fuerza. Otro: cambiar el fondo o el marco en cada slide; la serie tiene que verse como UNA colección.
- **Prompt de guion:**
```
Tengo estas [N] cosas REALES que construí y uso en mi negocio: [LISTA: nombre de la herramienta/app/plantilla + qué problema me resuelve + si tengo captura o grabación].
Escribe un carrusel vitrina de [N+2] slides:
Slide 1 (portada): titular apilado de máx. 12 palabras del tipo "[N] [cosas] que [dejé de pagar / uso cada día] y las hice con [herramienta]" + qué foto mía usar (celebrando o trabajando, en mi espacio).
Slides 2 a N+1: una por slide → "N. [Nombre que dice el beneficio, máx. 5 palabras]" + 1 línea de qué hace, con un dato concreto (máx. 16 palabras) + qué pantalla mostrar (con datos de ejemplo cargados, nunca vacía) y si va captura o grabación de 10-25 s.
Ordénalas de la más útil para [mi cliente ideal] a la más curiosa.
Última slide: "Comenta [PALABRA]" + qué le mandas por privado (los prompts, la plantilla o la guía para hacer la suya).
Solo cosas que construí de verdad. Tutea.
```
- **Fabrica:** `capturas-tutorial-formula100k` (capturas y grabaciones) + `carrusel-formatos-f100k` (HTML S29) · `portada-video-carrusel-formula100k` si una slide va en video.

---

### G17 · Hilo de tuits: comando → resultado
- **Mecánica:** M1 + pausa de like a mitad · **Soporte:** S27 tuit sobre fondo blanco (avatar + nombre + ✓) · **Motor:** A (capturas reales)
- **Origen:** carrusel sumado al recetario el 17-sep-2026 · **Referencia:** @marceloalaminoo · 40.120 likes · 118 comentarios · 14 slides · https://www.instagram.com/p/DdM3nuWgczR/ · ojo: sus «comandos» (/together, /skinpro, /deblur…) NO existen en ChatGPT y usa fotos de famosos; copia la forma, nunca eso
- **Anatomía:** 1) tuit-instrucción: «Envía [tu foto/tu texto] a [herramienta] y escribe:» + el comando o prompt en bold en su propia línea + el ANTES (la foto o el texto de partida) · 2) tuit-resultado: «Va a [lo que logra]» con el verbo en bold + el DESPUÉS en el mismo marco redondeado · 3-6) otro par instrucción → resultado; a veces van lado a lado (texto a la izquierda, foto vertical a la derecha) · cada 5-6 slides (en la referencia, la 7): pausa de like sin imagen «❤️ Antes de continuar, dale like si te gusta este tipo de contenido» · penúltima: el truco más vistoso (una cuadrícula de versiones) · cierre: tuit largo con tu oferta en 3 párrafos + captura de prueba.
- **Por qué funciona:** el tuit con avatar se lee como consejo de una persona, no como anuncio, y cada par da la recompensa en el siguiente swipe. La pausa de like a mitad pide la acción cuando el lector ya recibió valor: por eso esta referencia tiene 40.000 likes y apenas 118 comentarios (pidió like, no comentario).
- **Error típico:** inventar atajos que no existen («escribe /skinpro»): la alumna lo prueba, no pasa nada y pierdes confianza. Escribe el prompt completo que SÍ funciona. Otro: poner el antes y el después en la misma slide (se pierde el swipe).
- **Prompt de guion:**
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
- **Fabrica:** `capturas-tutorial-formula100k` (capturas) + `carrusel-formatos-f100k` (HTML S27).

---

## MAPA DE SKILLS

| Qué necesitas | Skill que ya existe | Cubre fichas |
|---|---|---|
| Escribir el guion de cualquier carrusel | `carrusel-viral-formula100k` | todas |
| Clonar el estilo de un link o captura | `clonador-carrusel-formula100k` | F01, F02, F10, F13, F15 (hoy es el conector universal) |
| Maquetar con tus fotos (scrapbook / editorial oscuro) | `carrusel-render-formula100k` | F09, F10, F11, F12, F15 |
| Tu foto + bloques de texto | `carrusel-organico-f100k` | F09 |
| Ilustraciones consistentes | `carrusel-ilustrado-formula100k` | F16 (adaptando estilo) |
| Fotos IA con tu cara | `higgsfield-carrusel-generador` | F14 |
| Imágenes sueltas (recortes, fondos, stickers) | `banana` | F05, F06, F18, F20 |
| Capturas de pantalla limpias | `capturas-tutorial-formula100k` | F03 |
| Caso de éxito con cifras verificadas | `carrusel-caso-exito-f100k` | F02 |
| Portada que se mueve | `portada-video-carrusel-formula100k` | cualquiera |

**Huecos que tenía la v1 y cómo quedaron (14-sep):**
1. Soportes de papel con texto fiel (F04, F06, F07, F08) → `papel.html`, y ahora el texto cae sobre los renglones.
2. Composiciones partidas y en cuadrícula (F01, F02, F05) → `split.html` (F05 sigue provisional sin arte IA).
3. Datos visuales (F17, F18, F19) → `datos.html` (F18 con fondo IA sin probar).
4. Garabatos sobre tu foto (F13) → `garabato.html`.
5. Router → `carrusel-formatos-f100k`, que ahora cubre las 35 fichas y entrega prompts para Gemini, ChatGPT y cualquier chat.
6. Fichas G y estilos de la guía maestra → HTML libre revisado por `build.js`.

| Qué necesitas | Skill |
|---|---|
| Cualquier ficha G en HTML | `carrusel-formatos-f100k` (HTML libre + estilo del soporte) |
| Hacerlo fuera de Claude Code | `prompts-por-plataforma.md` (Gemini · ChatGPT · HTML en cualquier chat) |

## CONEXIONES CON EL ECOSISTEMA
- **Grimorio** `lib/formatos-catalogo.ts` categoría `carruseles`: hoy 11 fichas por mecánica y 0 por soporte. Las 20 de aquí pueden entrar como lote nuevo (con embed real).
- **Challengerz**: la auditoría del 13-sep encontró 5 piezas de carrusel apuntando a anatomía de REEL; estas fichas son la anatomía de carrusel que les falta.
- **Guía maestra** `references/estilos-guia-maestra.md` (25 estilos): son SOPORTES y pieles; cada uno quedó mapeado a S1–S28 (ver auditoría). Se pasó a tuteo el 14-sep (solo el `.md`: el `.html` y el `.docx` siguen con voseo).

---

## AUDITORÍA DE COBERTURA (14-sep-2026)

La v1 decía cubrir «todos los formatos» pero solo enrutaba las 20 fichas F. Revisadas las 4 fuentes:

| Fuente | Formatos de carrusel | En la v1 | En la v2 |
|---|---|---|---|
| Fichas F (links + deck, miradas el 13-sep) | 20 | 20 | 20 |
| Guía de Formatos del Grimorio (`soporte: 'carrusel'`, origin/main) | 17 | 0 enrutados (solo «se pueden meter como lote») | 13 fichas G + 4 alias de una F |
| Guía maestra de 25 estilos | 25 | 9 coincidían con un soporte; 16 fuera | 25 mapeados (S1–S28) + 2 mecánicas nuevas (G14, G15) |
| Radar de formatos (`formatos.json`) | 0 (son reels) | — | — |

### Grimorio → catálogo
| Grimorio | Queda como |
|---|---|
| `carrusel-checklist` | G01 |
| `carrusel-noticias` | G02 |
| `que-tipo-eres` | G03 |
| `carrusel-secreto` | G04 |
| `carrusel-recursos` | G05 |
| `carrusel-glosario` | G06 |
| `carrusel-caso-estudio` | G07 |
| `carrusel-plantilla` | G08 |
| `carrusel-swipe-embudo` | G09 |
| `carrusel-frases` | G10 |
| `carrusel-errores-propios` | G11 |
| `carrusel-confesion-personal` | G12 |
| `carrusel-de-a-a-b` | G13 |
| `carrusel-paso-a-paso` | alias M2 → F04 / F08 / F09 |
| `carrusel-comparativo` | alias M9 → F18, con maqueta A│B en S20 |
| `carrusel-storytelling` | alias M6 → F11 / F12 |
| `infografia-ia` | alias M10 → F19 |

### Guía maestra → soportes
| Estilo | Soporte | Lo usan |
|---|---|---|
| 01 Bold statement | S17 (piel) | G09 |
| 02 Minimalista limpio | S17 (piel) | G10 |
| 03 Dark neón tech | S17 (piel) | G02 (alternativa) |
| 04 Editorial revista | S18 | G06 |
| 05 Pastel & emoji | S17 (piel) | G03 |
| 06 Gradiente fluido | S12 | F15 |
| 07 Glassmorphism | S17 (piel) | cualquier ficha tipográfica |
| 08 Scrapbook humano | S14 | F20, F06 |
| 09 Dato gigante | S17 (piel) | G07 |
| 10 Split imagen IA + texto | S19 | F16, F14 (alternativa) |
| 11 Full bleed atmosférico | S7 | F10, F11, G11 |
| 12 Mitos vs realidad | S20 | G04 |
| 13 Checklist | S21 | G01 |
| 14 FAQ tipo chat | S22 | G15, G12 |
| 15 Antes / después | S20 | G14 |
| 16 Brutalist / swiss | S17 (piel) | F14 (versión tipográfica), G04 (alternativa) |
| 17 Recibo / ticket | S23 | G05 (versión «la cuenta»), ofertas |
| 18 Code editor / terminal | S24 | G08 (prompts), F03 (alternativa) |
| 19 Y2K chrome | S17 (piel) | G03 (audiencia joven) |
| 20 Acid maximalista | S17 (piel) | G09 (nichos creativos) |
| 21 Bento grid | S25 | G05 |
| 22 Data-viz | S16 / S15 | F17, F18, F19 |
| 23 Newspaper | S26 | G02 |
| 24 Notes-app / tweet | S27 | G08, G12 |
| 25 Progress bar | S28 | G13, F04 (alternativa) |


