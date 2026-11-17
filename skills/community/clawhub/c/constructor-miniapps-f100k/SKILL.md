---
name: constructor-miniapps-f100k
description: "Construye mini-apps y herramientas reales sin ser programadora, con la metodología FÓRMULA 100K. Usar SIEMPRE que alguien pida: \"quiero que construyas una mini app web llamada X\", \"constrúyeme una app\", \"hazme una mini-app\", \"es mi primera app\", \"crea una herramienta\", \"una calculadora web\", \"un quiz que dé un resultado\", \"un generador de X\", \"una auditoría exprés\", \"una extensión de Chrome\", \"una app con mi API/IA\", \"un mini-SaaS\", \"clona esta web/app\", \"publícala en Vercel\", \"dame el link de mi app\". Empieza SIEMPRE por el brief de 5 preguntas y, si no hay motivo real para más, entrega una app de UN SOLO ARCHIVO HTML que funciona con doble clic, probada en el navegador del agente y enviada por Telegram — sin llaves de IA, sin base de datos, sin login. La publica en *.vercel.app solo con la cuenta de Vercel de la usuaria conectada y su ✅. NO usar para landings de venta puras ni para diseñar la estrategia del lead magnet (cazador-lead-magnets-f100k)."
argument-hint: "[tipo de app o idea]"
disable-model-invocation: false
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Camino por defecto: escribe `entregables/apps/<nombre>/index.html` y mándalo por Telegram como documento (o `.zip` si son varios archivos). Eso ya es una entrega completa: se abre con doble clic.
> - Fase 3: prueba la app abriéndola en el navegador del agente (archivo local, sin login): recorre el flujo, el camino torcido y el ancho de 390 px con screenshots. No digas que funciona sin haberla recorrido.
> - Fase 4 · publicar: **Las apps siempre se despliegan directo en Vercel** con la cuenta de la usuaria (`VERCEL_TOKEN` en el entorno): `vercel --prod --yes --token "$VERCEL_TOKEN"`, y le mandas la URL por Telegram. No hace falta pedir ✅ para desplegar. Nunca `vercel login` desde el servidor ni una cuenta que no sea suya. Si falta `VERCEL_TOKEN`, pídele que lo cree en vercel.com → Account Settings → Tokens y lo agregue al entorno del agente; el `.zip` es solo el último recurso.
> - Next.js / Supabase / Stripe: escribe el proyecto. **No corras `npm install` ni `next build` en este servidor** (es pesado para el plan): construye Vercel al desplegar. Las llaves nunca van en los archivos.
> - Clonar una web de referencia: navegador del agente, solo páginas públicas.

---

# Constructor de Mini-Apps — FÓRMULA 100K

Convierte una idea en una herramienta real, construida, probada y publicada, sin que quien la pide escriba código.

**La regla que manda sobre todas las demás:** al final de esta conversación tiene que existir una app que abre y funciona. Una app simple que abre vale infinitamente más que una app ambiciosa a medio construir. Ante cualquier duda, elige el camino que termina.

---

## Fase 0 — El brief de 5 (obligatorio, 1 minuto)

Antes de tocar código, ten estas 5 respuestas. Si la persona ya te las dio en su mensaje, no las vuelvas a preguntar: repítelas en una frase y pide confirmación.

1. **Nombre** — cómo se llama.
2. **Para quién** — una persona específica, no "todos".
3. **Qué problema le quita** — la molestia real que desaparece.
4. **Qué hace: la UNA pieza** — un solo verbo, un solo resultado.
5. **Cómo se ve** — tono + colores + un detalle visual clave.

Devuélvelo armado así antes de construir: *"[Nombre] es para [quién], que [problema]. La app [qué hace]. Se ve [cómo]."*

**Cómo preguntar sin trabar a nadie:**
- Pregunta lo que falte de una sola vez, en lenguaje normal, máximo una ronda.
- Si responde "no sé" o deja algo en blanco, **propón tú una opción concreta y sigue**. Nunca dejes la conversación parada esperando una respuesta perfecta.
- Si el punto 4 trae "y… y… y…", corta: elige la pieza más valiosa, dilo en voz alta ("empezamos por X; lo demás lo agregamos después") y construye esa.

**Lo que NO preguntas de entrada:** si usa IA, si cobra, si capta correos, si necesita base de datos. Asume que **no**, salvo que la persona lo pida explícitamente. Ese es el camino que termina.

---

## Fase 1 — Elegir el camino (por defecto, el corto)

**Camino por defecto — UN archivo HTML.** React + Tailwind por CDN en un solo `.html`. Abre con doble clic, sin instalar nada, sin servidor, sin llaves. Sirve para casi todo lo que la gente pide de verdad: quiz, test, calculadora, auditoría con puntaje, recomendador, cotizador, checklist, contador, generador de textos por plantilla, planificador.

Toma este camino **salvo que exista una razón concreta para no hacerlo**. "Se vería más profesional" no es una razón.

**Sube de camino solo si aparece una de estas necesidades reales:**

| Necesidad real | Camino | Notas |
|---|---|---|
| Guardar datos que se vean desde otro dispositivo | Next.js + Supabase | Antes prueba `localStorage`: casi siempre alcanza. |
| Llamar a un modelo de IA con una llave | Next.js + route handler | La llave va SIEMPRE en variable de entorno del servidor. |
| Scrapear o transcribir | Next.js + MCP (Apify / Supadata) en el server | Nunca desde el cliente. |
| Cobrar o suscripción | Next.js + Supabase (auth + RLS) + Stripe | El más complejo: acuerda el diseño antes de construir. |
| Vivir dentro del navegador sobre otras webs | Extensión Chrome (Manifest V3) | Sin servidor. README de instalación en 3 pasos. |
| Landing de venta con pago | → delega en `landing-producto-formula100k` | Esta skill no la construye. |

Si la idea junta varias piezas grandes a la vez (login + pagos + IA + panel), usa antes `superpowers:brainstorming` para acordar el diseño; con lógica delicada apóyate en `superpowers:test-driven-development`.

---

## Fase 2 — Construir

Con el camino corto (un archivo HTML), estas son las reglas:

- **Una sola pantalla o un solo flujo**, con un principio y un final visible. El final siempre muestra un resultado que la persona quiere leer.
- **El "cerebro" es lógica normal**: cálculos, condiciones y textos ya escritos. Nada de llamadas a servicios externos.
- **Marca de quien la pide**: sus colores, su nombre, su tono. Si no dio colores, propón una paleta y muéstrala.
- **Responsive de verdad**: pruébala mentalmente en 390px de ancho. Los botones se tocan con el pulgar.
- **Todo el contenido editable arriba**: preguntas, textos de resultado, enlaces y colores en constantes al principio del archivo, con un comentario que diga qué cambiar.
- **CTA final**: un botón grande al terminar el flujo, que lleve a **la oferta, el DM o el WhatsApp de quien construye la app** — nunca a un destino que no sea suyo. Déjalo como constante `MI_LINK` arriba, con un valor de ejemplo, y al entregar recuérdale cambiarlo.
- **Los estados que faltan siempre**: qué se ve al abrir (vacío), mientras responde, al terminar, y si se equivoca o no contesta algo. Ninguno puede quedar en blanco.
- Escribe en español neutro, trato de "tú", salvo que pidan otra cosa.

Con Next.js, además, estas convenciones vienen de errores reales y evitan que el deploy falle:

- **Pin de Next.js a `16.1.7`.** Next `16.2.0` rompe el build en Vercel (`TypeError path undefined` en modifyConfig); local pasa, Vercel no. No uses `latest`.
- **`eslint: "^9"`** en devDependencies.
- **`.gitignore` ANTES del primer commit** (`node_modules`, `.next`, `.env*`).
- **Email de commit correcto para Vercel:** usa el noreply de TU cuenta de GitHub (`<id>+<usuario>@users.noreply.github.com`, lo ves en Settings → Emails). Un email no asociado al usuario de GitHub deja el deploy en estado BLOCKED.
- **API keys SIEMPRE en variables de entorno del servidor**, jamás en el cliente ni en el bundle.
- **Supabase + RLS:** toda tabla que se mute necesita una policy permisiva o el insert **falla en silencio**. Define las policies en el mismo `schema.sql`.
- **Docs actualizados:** con librerías que cambian rápido (Stripe, Supabase, Next), trae la doc real con **Context7 MCP** antes de programar.
- **next.config mínimo**, sin opciones experimentales.

---

## Fase 3 — Probarla ANTES de entregarla

No digas que está lista sin haberla recorrido. Con un archivo HTML, ábrelo y haz el camino completo como si fueras la persona que la va a usar:

1. Abre la app. ¿Se entiende qué es y qué hacer, sin que nadie lo explique?
2. Recorre el flujo entero hasta el resultado final.
3. Prueba el camino torcido: sin responder nada, con todo respondido igual, con el valor extremo.
4. Mira si el CTA final está y a dónde apunta.
5. Revísala angosta (celular).

Si algo se rompe, arréglalo antes de mostrarla. Si quieres una revisión más dura, pásala por `auditor-ux-app-f100k`; si se ve genérica o "hecha por IA", por `ux-elevacion-formula100k`.

---

## Fase 4 — Publicarla

El objetivo es una dirección `*.vercel.app` que se pueda mandar por WhatsApp.

Hay tres caminos. **Empieza siempre por el primero: publícala tú, desde esta misma conversación.** Publicar es donde más gente abandona, y es justo lo que tú puedes hacer por ella.

### Camino A — la publicas tú (el que hay que intentar primero)

Es gratis y no pide tarjeta. Pide permiso antes de correr comandos y di en una línea qué hace cada uno; no la dejes mirando una terminal sin entender qué pasa.

1. **¿Está la CLI?** `vercel --version`. Si no está: `npm i -g vercel`. Si `npm` tampoco existe en esa máquina, cámbiate al Camino B — no te pongas a instalar Node en vivo.
2. **¿Hay sesión?** `vercel whoami`. Si no hay, corre `vercel login` y **avísale antes**: se le va a abrir el navegador y tiene que confirmar ahí, con el mismo correo con el que quiera su cuenta. El comando se queda esperando hasta que lo haga; no es que se colgó.
3. **Prepara la carpeta.** Si es un solo archivo HTML, tiene que llamarse `index.html` y estar **dentro de una carpeta** (Vercel publica carpetas, no archivos sueltos). Si se llama distinto, renómbralo antes.
4. **Publica:** desde la carpeta del proyecto, `vercel --prod --yes`. Si existe la skill `/vercel:deploy`, úsala en lugar de este paso.
5. **Compruébalo tú.** Abre la URL que devolvió y verifica que carga y que el flujo funciona. Tiene que quedar en estado **Ready**, nunca BLOCKED. Una URL que no abriste no es una entrega.
6. **Entrégala sola y copiable**, en su propia línea, y dile que ya la puede mandar por WhatsApp.

Si la app usa variables de entorno, configúralas en Vercel **antes** de dar por lista la app.

### Camino B — sin terminal, arrastrando

Cuando no hay `npm`, o cuando la persona prefiere hacerlo con sus manos: entra a `vercel.com`, crea la cuenta gratis, y arrastra la carpeta del proyecto a la pantalla de nuevo proyecto. Vercel la publica y devuelve la URL. Guíala paso a paso y pídele que te pegue la URL para comprobarla tú.

### Camino C — si falla

Ver abajo. Nunca dejes el intento fallido como estado final.

### Camino C — si publicar falla

No se pierde el día. La app ya existe y funciona en el computador. Entrega el archivo, di exactamente dónde quedó guardado, explica que se abre con doble clic, y deja escrito el paso a paso para publicarla después. Después dedícate al error de publicación con calma. Nunca termines la conversación sin que exista algo que abre.

---

## Entregable final

1. La app construida, **probada por ti** y **publicada por ti**, con su URL abierta y verificada.
2. **Dónde quedó el archivo** (ruta exacta) y cómo volver a abrirlo.
3. **Qué cambiar y dónde**: la línea del `MI_LINK`, los colores, las preguntas y los textos de resultado, señalados por nombre.
4. Si quedó pendiente publicar o configurar algo, una lista corta y concreta de lo que falta.
5. Para extensiones: README de instalación en 3 pasos.

---

## Skills que se combinan

- **`cazador-lead-magnets-f100k`** — define QUÉ app conviene construir; esta skill construye el CÓMO.
- **`auditor-ux-app-f100k`** — revisa el brief antes de construir y la app ya construida.
- **`ux-elevacion-formula100k`** — sube el nivel visual cuando la app ya funciona.
- **`landing-producto-formula100k`** — la landing de venta con pago.
- **Navegador del agente (sin login)** — para clonar una web de referencia pública inspeccionando su estructura y estilo.
- **MCPs:** Context7 (docs actualizados), Apify (datos públicos), Supadata (transcripción), Higgsfield (si la app genera imágenes o video).
