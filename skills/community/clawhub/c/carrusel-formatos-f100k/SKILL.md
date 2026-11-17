---
name: carrusel-formatos-f100k
description: "Router del catálogo de 35 formatos de carrusel de FÓRMULA 100K (20 fichas F con referencia mirada + 15 fichas G de la guía maestra de 25 estilos). Elige el formato por objetivo, escribe el guion con el prompt de la ficha, fija el visual y la referencia, y lo entrega como prompts listos para Gemini, ChatGPT o cualquier chat (3 variantes: desde la descripción, con su marca, solo fondo) o como HTML. Usar cuando se diga \"qué formato de carrusel uso\", \"catálogo de formatos de carrusel\", \"hazme un carrusel tipo [ficha]\", \"carrusel en libreta\", \"carrusel frase partida\", \"carrusel tier list\", \"chuleta en lapicero\", \"carrusel checklist\", \"carrusel de noticias\", \"lo que nadie te dice\", \"carrusel antes y después\", \"carrusel tipo chat\", \"dame el prompt para hacerlo en Gemini/ChatGPT\", \"carrusel estilo bento/recibo/periódico/terminal\"."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - El render a PNG (`build.js` + `export.js`) está hecho para una Mac con Chrome. En el servidor, por defecto entrega el camino **«prompts por plataforma»**: el prompt listo para Gemini o ChatGPT de la ficha elegida, con las 3 variantes.
> - Si la usuaria tiene `GEMINI_API_KEY` o un modelo de imagen en OpenRouter, puedes generar las imágenes tú: costo estimado → ✅ → generar → mandar por Telegram.
> - `build.js` y `export.js` buscan Chrome en `CHROME_PATH`, `/usr/bin/google-chrome-stable` o `/usr/bin/chromium` y lanzan con `--no-sandbox`. Úsalos si `node` y `puppeteer-core` están instalados; si fallan, vuelve a los prompts sin insistir.
> - Las fotos de la usuaria están en `cerebro/fotos/`. Skills que menciona y no vienen en este paquete (render, clonador, ilustrado con tu cara): ofrece el prompt equivalente.

---

## 🧭 ANCLAJE DE RUBRO (leer PRIMERO — manda sobre cualquier ejemplo de esta skill)

Esta skill enseña un **método**. El método es agnóstico de industria: sirve igual para
formulación cosmética, nutrición, repostería, fisioterapia, finanzas o jabonería.
Los ejemplos escritos aquí abajo son ilustraciones **del método**, nunca del tema.

**Antes de escribir nada:**

1. Identifica el **RUBRO real** de la persona (léelo de su Segundo Cerebro, de su perfil o
   pregúntaselo en una línea si no está claro). Decláralo: *"Rubro: ___"*.
2. Todos los ejemplos, analogías, comparaciones, objeciones, métricas y vocabulario salen
   de **ESE** rubro.
3. Si el rubro **no** es marketing, redes sociales, creación de contenido, ventas online o
   negocios digitales → queda **PROHIBIDO** el vocabulario de ese mundo (reels, algoritmo,
   embudo, lead magnet, engagement, "publicar sin vender", "clientes de alto ticket",
   "escalar tu negocio", "posicionarte como referente"), salvo que la persona lo escriba primero.
4. Si el rubro es **técnico, científico o de oficio**: NO borres el tecnicismo para
   "simplificar". Úsalo y **tradúcelo en su primera mención**. El término preciso ES la
   autoridad de esa creadora; quitarlo borra justo lo que la diferencia.
5. Si no tienes datos suficientes del negocio, dilo y usa marcadores explícitos
   (`[TU OFERTA]`, `[TU RESULTADO]`). **Nunca asumas que el rubro es marketing.**

**El método viaja, el rubro no.** El mismo molde, vestido con rubros distintos:

| Rubro | El mismo molde |
|---|---|
| Cocina | "Así es mi cena favorita para no dormir con el azúcar alta." |
| Relaciones | "5 señales de que estás forzando una relación que ya no funciona." |
| Finanzas | "La principal causa de un divorcio no es una infidelidad." |
| Formulación cosmética | "El conservante decide si tu crema dura tres meses o te da una infección. No el aceite." |
| Jabonería | "Si tu jabón se pone blando a los dos días, no fue el aceite. Fue la sosa." |
| Fisioterapia | "Ese dolor de rodilla al bajar escaleras casi nunca nace en la rodilla." |
| Repostería | "Tu bizcocho se hunde en el centro por la temperatura, no por la harina." |
| Jardinería | "Tu planta no se está muriendo de sed. Se está ahogando." |

Mismo molde en todos; ninguno menciona reels ni embudos. Haz exactamente eso.

---

# Carrusel por formatos · FÓRMULA 100K

Convierte un tema en un carrusel terminado eligiendo **una ficha** y girando 3 perillas:
**MECÁNICA** (qué hace con la atención) → **SOPORTE** (dónde vive el texto) → **MOTOR** (con qué se fabrica).

## Fuentes (léelas, no las copies en esta skill)
| Archivo | Qué trae |
|---|---|
| `references/catalogo.md` | Las **37 fichas**: F01–F20 (referencias miradas) y G01–G17. Mecánicas M1–M28, soportes S1–S29, anatomía, error típico, **prompt de guion**, quién lo fabrica, y la auditoría de cobertura. |
| `references/prompts-por-plataforma.md` | Por ficha: **referencia** (link al post real), **visual detallado** (paleta hex, tipografía, composición por slide) y prompts para Claude Code · HTML en cualquier chat · Gemini · ChatGPT, con variantes A/B/C. GENERADO desde `visual.json`. |
| `references/grimorio-carruseles.md` | Anatomía completa de los 17 carruseles del Grimorio (G01–G13 + 4 alias). GENERADO por `scripts/sincronizar-grimorio.mjs`. |
| `references/estilos-guia-maestra.md` | Los 25 estilos visuales con su prompt HTML (pieles y soportes S17–S28). |
| `references/plantillas.md` | Formato de `spec.json` de las plantillas y contrato del HTML libre. |

Los archivos de `references/` los mantiene el equipo de FÓRMULA 100K y llegan con cada actualización del paquete: no los edites.

**Voz:** tuteo siempre (tú, tienes, sube, comenta). Nunca voseo, tampoco en los textos de las slides.

---

## Flujo

### 1. Formato
- Si piden una ficha ("tier list", "F07", "tipo chat") → esa ficha.
- Si NO dicen formato → pregunta UNA cosa: **¿qué quieres que haga este carrusel?** y propón **3 fichas** con 1 línea de por qué y su referencia.

| Objetivo | Primero se proponen | También |
|---|---|---|
| Guardado | F07 chuleta · G01 checklist · G05 recursos | F18, F04, G06 glosario, G13 de A a B, G17 hilo de tuits |
| Comentario | F17 tier list · G03 qué tipo eres · G16 vitrina de lo que construiste | F08, F14, G08 molde, G12 confesión, G10 frases |
| Compartido | F01 causa y consecuencia · G10 frases · G06 glosario | F19 mapa |
| Tiempo de permanencia | G09 swipe-reveal · F20 collage | G04 lo que nadie te dice |
| Seguidor | F07 (slide de seguir) · F10 anáfora · F13 garabatos (post fijado) | F06 |
| Conexión | F11 historia con edades · G11 errores propios · G12 confesión | F12 |
| Venta | G07 caso de estudio · G14 antes/después · G15 FAQ en chat | F11, F20, F09 |
| Autoridad / actualidad | G02 noticia · G04 lo que nadie te dice | F14 hot take |

### 2. Guion
Usa el **prompt de guion** de la ficha (catálogo) con el tema, el nicho y la voz. Respeta la anatomía y evita el error típico.
Si falta un dato real (cifra, caso, historia, pregunta de DM) → pregúntalo. No inventes cifras, casos ni testimonios.
Entrega el guion como tabla slide por slide y **espera el OK** antes de producir.

### 3. ¿Dónde lo va a fabricar?
Pregunta solo si no está claro. Si el usuario trabaja en Claude Code → paso 4. Si la persona trabaja en otra herramienta, o pide "el prompt":
entrégale de `prompts-por-plataforma.md` la sección de esa ficha para **su** herramienta:
- **HTML en cualquier chat** (Claude, ChatGPT o Gemini con Canvas): texto perfecto, gratis. Recomiéndalo si hay más de ~25 palabras por slide.
- **Gemini (Nano Banana)** o **ChatGPT (Imágenes)**: variante **A** desde la descripción (el prompt se sostiene solo: no se adjuntan capturas ni se nombra la cuenta del ejemplo), **B** con su marca, **C** solo fondo sin texto (el texto va después en HTML). Más los prompts «seguir» (slide N) y «arreglar» (una palabra mal escrita).
Rellena tú los corchetes que ya conozcas (texto de la portada, colores de su marca). Si quiere ver el formato funcionando, pásale el link del ejemplo aparte, nunca dentro del prompt.

### 4. Motor en Claude Code
- **A · Fotos + HTML** (gratis, texto perfecto) · **B · Imagen IA** · **C · Híbrido** (fondo IA sin texto + texto en HTML).
- **Regla:** más de ~25 palabras o una lista en una slide → el texto NO se le pide al modelo de imagen → motor C.
- Antes de gastar créditos (B o C) di cuántas imágenes son y pide confirmación.

### 5. ¿Quién lo fabrica?
| Ficha | Se fabrica con |
|---|---|
| F01, F02, F05 | esta skill · `templates/split.html` |
| F04, F06, F07, F08 · G01 (variante papel) · G06 (variante papel) | esta skill · `templates/papel.html` (F06: stickers con `banana`) |
| F13 | esta skill · `templates/garabato.html` |
| F17, F18, F19 | esta skill · `templates/datos.html` (F18 con fondo: `banana`) |
| G01–G06, G08, G09, G10, G12–G15 | esta skill · **HTML libre** con el estilo de su soporte (S17–S28) y el visual de la ficha |
| G07 · G14 con clienta | `carrusel-caso-exito-f100k` (cifras verificadas) |
| G11 · G10 sobre tus fotos | `carrusel-render-formula100k` |
| F03 · G05 (capturas) | `capturas-tutorial-formula100k` + esta skill o `carrusel-render-formula100k` |
| G16 · G17 | `capturas-tutorial-formula100k` (capturas o grabaciones reales) + esta skill · **HTML libre** S29 (fondo plano + pantalla en marco) o S27 (tuit) |
| F09 | `carrusel-organico-f100k` o `carrusel-render-formula100k` |
| F10, F11, F12, F15 | `carrusel-render-formula100k` (o `clonador-carrusel-formula100k` con el link) |
| F14 | `higgsfield-carrusel-generador` (foto con tu cara) + texto en HTML |
| F16 · G03 con personajes | `carrusel-ilustrado-formula100k` (adaptando el estilo) |
| F20 | `banana` (recortes) + `carrusel-render-formula100k` |

Si deriva a otra skill: pásale el guion aprobado + el **visual detallado** + la **referencia anclada** de la ficha, e invócala.

### 6. Render
**Plantillas propias:**
1. Escribe `spec.json` en la carpeta de la pieza (por defecto `entregables/carruseles/<fecha>_<slug>/`). Formato en `references/plantillas.md`; ejemplos en `ejemplos/`.
2. Fotos del usuario: pregúntale la carpeta la primera vez (por ejemplo `cerebro/fotos`) y usa rutas absolutas o relativas al `spec.json`. Mira las fotos recortadas a 4:5 antes de elegir y de poner coordenadas: la cara nunca va debajo del texto.
3. `node skills/carrusel-formatos-f100k/build.js <carpeta>/spec.json`

**HTML libre** (fichas G y estilos de la guía maestra):
1. Lee el prompt del estilo del soporte en `estilos-guia-maestra.md` y el visual de la ficha en `prompts-por-plataforma.md`. Abre el link de la referencia para ver el post.
2. Escribe `<carpeta>/carrusel.html` con el contrato de `plantillas.md`.
3. `node skills/carrusel-formatos-f100k/build.js <carpeta>/carrusel.html`

Avisos: `⚠ no-cabe` / `⚠ letra-chica` → acorta el texto (no achiques la plantilla). `⚠ fuente` / `⚠ imagen` → no entregues hasta resolverlo.
Salen PNG a 2160×2700 (escala 2).

### 7. MIRA los PNG antes de entregar
Abre cada `slide-NN.png` con Read. Revisa: texto cortado, tildes y eñes, cara tapada, líneas cruzando textos, contraste, que se parezca a la referencia.
Los avisos de `build.js` no reemplazan mirar.
Entrega: rutas de los PNG + caption con el CTA de la ficha.

---


## Gotchas conocidos
- **Fuentes:** nunca `-apple-system` (en Chrome headless cae a Times). Las plantillas esperan `document.fonts.ready`. Requiere internet (Google Fonts).
- **Autofit** mide cajas, no `scrollHeight`, y borra `style.fontSize` para medir la base: el tamaño inicial de un texto con `data-fit` va en CSS (o en una variable), nunca inline en `font-size`, o cae a 16 px.
- **Chequeo de fuentes** del HTML libre usa el peso y la itálica reales: una familia cargada solo en 900 no se pregunta en 400.
- `export.js` viene dentro de esta skill. La primera vez: `cd` a la carpeta de esta skill y corre `npm install` (instala `puppeteer-core`; usa tu Google Chrome).
- F05 necesita 2 imágenes metafóricas por slide: sin créditos de imagen, usa fotos distintas y avisa que es provisional.
- F18 sin fondo IA dibuja barras: sirve para publicar, pero la referencia usa objetos reales apilados.
- F13: el `contorno` es un óvalo suelto, no un recorte de la silueta.
- Los prompts de Gemini y ChatGPT no están probados con generación real todavía.
