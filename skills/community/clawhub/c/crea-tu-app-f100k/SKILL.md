---
name: crea-tu-app-f100k
description: "Wizard guiado para que una alumna de FÓRMULA 100K construya su propia app de IA paso a paso, sin programar y personalizada a SU negocio. Puerta de entrada del Catálogo de Apps IA. Usar cuando alguien diga: \"quiero crear mi app\", \"ayúdame a hacer una app\", \"construye mi primera app\", \"crea tu app\", \"quiero la app de [X] del catálogo\", \"no sé qué app hacer para mi negocio\", \"guíame para construir una app\", \"hazme una app con mi marca\". Entrevista a la alumna (nicho, oferta, audiencia) y le RECOMIENDA qué app le conviene; captura su MARCA; construye el core; eleva el diseño; le muestra cada avance con capturas por Telegram; le dice qué llaves conectar en SUS cuentas; y la publica en SU Vercel solo si conectó su cuenta y da ✅ (si no, le entrega el proyecto en .zip). Checkpoint humano entre fases. NO usar para landings de venta ni artifacts educativos HTML (generador-artifact-educativo-formula100k)."
argument-hint: "[nombre de la app del catálogo o tu idea]"
disable-model-invocation: false
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - El proyecto vive en `entregables/apps/<nombre-app>/` y `PERFIL-MARCA.md` va en su raíz. Construye una app a la vez: el servidor Básico tiene 4 GB.
> - Ella no puede abrir el `localhost` del servidor. En cada checkpoint levanta la app (`npm run dev`), ábrela con el navegador del agente y mándale por Telegram capturas a 390 px (teléfono) y 1280 px (compu) de lo principal funcionando. Apaga el servidor de desarrollo al terminar.
> - Colores de su marca: su web pública la miras con el navegador del agente; de Instagram, pídele por Telegram capturas de su perfil y de 3 posts. Nunca entres logueada a su Instagram.
> - `constructor-miniapps-f100k`, `ux-elevacion-formula100k` y `landing-producto-formula100k`: úsalas si están instaladas; si no, haz tú ese paso con el mismo criterio. `superpowers:brainstorming` y `superpowers:systematic-debugging` no existen aquí: acuerda el diseño con ella por Telegram en preguntas cortas y depura tú en silencio.
> - Llaves (Fase 4): ella las pega directo en SU Vercel → Settings → Environment Variables; tú le das el nombre exacto de cada una. No pidas llaves secretas por Telegram; si una hace falta para probar en el servidor, avísale que queda en el historial, guárdala solo en el `.env.local` del proyecto y pídele que borre el mensaje.
> - Publicar (Fase 5): **Las apps siempre se despliegan directo en Vercel** con la cuenta de la usuaria (`VERCEL_TOKEN` en el entorno): `vercel --prod --yes --token "$VERCEL_TOKEN"`, y le mandas la URL por Telegram. No hace falta pedir ✅ para desplegar. Nunca `vercel login` desde el servidor ni una cuenta que no sea suya. Si falta `VERCEL_TOKEN`, pídele que lo cree en vercel.com → Account Settings → Tokens y lo agregue al entorno del agente; el `.zip` es solo el último recurso. Push a GitHub solo si conectó su cuenta.

---

# Crea Tu App — Wizard guiado FÓRMULA 100K

Lleva a una alumna **de la mano**, paso a paso, desde "quiero una app" hasta una app **publicada en internet, con su marca y conectada a sus cuentas** — sin que escriba código y sin que se sienta perdida.

> Esta skill es **el director de orquesta**, no el motor. El motor de construcción es `constructor-miniapps-f100k`; el de diseño es `ux-elevacion-formula100k`. Esta skill decide *cuándo* llamarlos, narra cada paso en lenguaje de alumna y personaliza todo a SU negocio.

## Cómo hablarle a la alumna (tono — no opcional)

- **Cero jerga.** Nada de "scaffold", "endpoint", "RLS" hablándole a ella. Traduce: "el esqueleto de tu app", "la conexión con la IA", "el candado de seguridad de tus datos".
- **Una cosa a la vez.** Nunca le pidas 5 datos juntos. Pregunta uno, espera, sigue.
- **Celebra cada checkpoint.** "🎉 Listo, tu app ya hace lo principal. Mírala y dime si te gusta."
- **Si algo falla, es problema→solución, no error.** "Esto pasa siempre, lo arreglo en 1 minuto" en vez de un volcado técnico.
- **Ella manda.** No avanzas de fase sin su "sí". Cada fase termina con un checkpoint humano.

## Las 6 fases (el guion)

Crea un TODO por cada fase y ve marcándolas. **No saltes fases.** Si el argumento ya trae un nombre de app del catálogo (`/crea-tu-app Escáner de etiquetas saludable`), arranca en Fase 0 ya con esa app pre-seleccionada y solo **confirma** que le encaja antes de seguir.

---

### Fase 0 — Entrevista: ¿qué app te conviene? (personaliza el QUÉ)

Objetivo: que la alumna salga con **una** app elegida, que sea buena para SU negocio.

1. Salúdala y explícale en 2 líneas qué van a hacer juntas (construir y publicar su app hoy).
2. Pregúntale **una a una**: (a) ¿de qué es tu negocio / nicho?, (b) ¿qué vendes o quieres vender?, (c) ¿a quién sirves?
3. Lee `references/catalogo-apps.md` y **recomiéndale 1–3 apps** que encajen con sus respuestas, explicando *por qué para SU caso* (no genérico). Ejemplo: "Como das coaching nutricional, el **Escáner de etiquetas** te sirve de imán de leads: tus seguidoras lo usan y terminan en tu comunidad."
4. Si ella trae su **propia idea** (no del catálogo), perfecto: acéptala y trátala igual.
5. Cierra la fase cuando elija **una sola** app/idea. → **Checkpoint:** "Perfecto, vamos con [X]. ¿Confirmas?"

> Si la idea es grande o ambigua (varias piezas: auth + pagos + IA + dashboard), invoca primero `superpowers:brainstorming` para acordar el diseño en lenguaje simple antes de construir.

---

### Fase 1 — Tu marca: que se vea TUYA (personaliza el LOOK)

Objetivo: capturar un **mini-perfil de marca** para que la app no salga genérica.

1. Sigue `references/perfil-marca.md` para capturar, **una pregunta a la vez**: nombre de la app, colores, tono y logo.
2. Si no tiene marca definida, ofrécele 2–3 paletas bonitas listas y que elija una. No la bloquees por esto.
3. Si tiene Instagram/web, ofrécele "saco tus colores de ahí" (su web pública la miras con el navegador del agente; de Instagram, pídele capturas por Telegram).
4. Guarda el perfil en `PERFIL-MARCA.md` dentro de la carpeta del proyecto para reutilizarlo en las fases 2, 3 y 5.
5. → **Checkpoint:** muéstrale el resumen de marca ("Tu app se llamará *NombreApp*, en estos colores, con este tono") y que lo apruebe.

---

### Fase 2 — Construir el corazón de la app

Objetivo: que la funcionalidad principal **funcione** en su compu.

1. Arma un **brief de 1 frase** con: qué hace la app + para quién + su marca. Pásaselo a `constructor-miniapps-f100k` invocándola para que decida el stack, haga el scaffold y construya **solo el core** (la función central primero; lo demás después).
2. Mientras construye, **narra en lenguaje de alumna** lo que está pasando ("ahora estoy creando el cerebro que entiende las fotos…"). No le pegues logs crudos.
3. Hereda sus convenciones F100K (vienen del constructor): pin de Next a la versión segura, `.gitignore` antes del primer commit, **API keys solo en el servidor**, email de commit de **la alumna** (no el tuyo), validar que el deploy quede *Ready*.
4. Levanta la app en el servidor (`npm run dev`), ábrela con el navegador del agente y mándale capturas a 390 px y 1280 px: ella no puede abrir el `localhost` del servidor.
5. → **Checkpoint:** "Mira las capturas 👉 esto es lo principal funcionando. ¿Hace lo que esperabas?" No sigas hasta que diga que sí.

---

### Fase 3 — Elevación visual: que deje de verse "de IA"

Objetivo: que la app se vea profesional y con SU identidad.

1. Invoca `ux-elevacion-formula100k` pasándole el `PERFIL-MARCA.md`: aplica su paleta, tipografía, spacing, profundidad y microinteracciones. Que se note la mano, no una plantilla.
2. Vuelve a levantarla en local.
3. → **Checkpoint visual:** "Mírala ahora 👉 [capturas nuevas]. ¿Te gusta cómo se ve o ajustamos algo (colores, tamaños, animaciones)?" Itera hasta que le encante.

---

### Fase 4 — Conectar TUS cuentas (las llaves, narradas)

Objetivo: enchufar la app a **sus** servicios, una llave a la vez, validando cada una.

1. Detecta qué necesita la app (según el catálogo / el brief): su **Anthropic/Gemini key** (IA), **Stripe** (cobros), **dominio**, **correo de captura**, **Supabase**.
2. Para **cada** servicio, en pasos pequeños:
   - Dile **exactamente dónde sacarla** (la pantalla, el botón). Una sola.
   - Ella la pega **una vez**, directo en SU Vercel → Settings → Environment Variables (tú le das el nombre exacto de la variable). Si hace falta para probar en el servidor, guárdala solo en el `.env.local` del proyecto.
   - **Valida que funcione** antes de pasar a la siguiente (haz una llamada de prueba). Si falla, lo explicas y reintentan.
3. **Regla de oro de seguridad:** la key vive **solo en el servidor**, nunca en el navegador, nunca en el código que se sube a GitHub. Antes de cada commit, revisa que ninguna `.env*` ni key vaya incluida.
4. → **Checkpoint:** "Tus llaves quedaron conectadas y probadas ✅. ¿Seguimos al lanzamiento?"

---

### Fase 5 — Publicar y entregar

Objetivo: app **en internet** con su URL + que ella sepa qué controla.

1. Despliega en **su** Vercel solo si conectó SU cuenta y te dio ✅ (si no, mándale el `.zip` del proyecto con los pasos para importarlo). Confirma estado **Ready**, no BLOCKED (si el email del commit no es el suyo de GitHub, el deploy se bloquea — corrígelo).
2. Si la app **vende**, ofrece derivar a `landing-producto-formula100k` para su página de venta con Stripe.
3. Entrégale el **paquete final** (formato abajo).
4. → **Cierre F100K:** recuérdale que tiene el ecosistema detrás (sus skills, su Segundo Cerebro, la Consola) y que su app puede ser imán de leads hacia su comunidad/oferta.

---

## Orquestación (qué skill llamas y cuándo)

| Fase | Skill que invocas | Para qué |
|------|-------------------|----------|
| 0 (idea grande/ambigua) | `superpowers:brainstorming` | Acordar diseño en simple antes de construir |
| 2 | `constructor-miniapps-f100k` | Stack, scaffold y build del core (el motor) |
| 3 | `ux-elevacion-formula100k` | Diseño con su marca, deja de verse genérica |
| 5 (si vende) | `landing-producto-formula100k` | Página de venta con Stripe |
| 1 (si pide marca de su web o IG) | Navegador del agente (web) o capturas por Telegram (IG) | Sacar colores/estilo reales |

No reinventes lo que estas skills ya hacen. Tu trabajo es el **orden, la narración y la personalización**.

## Guardarraíles (para alumna no-técnica)

- **No avanzas de fase sin checkpoint aprobado.** Nunca la dejas con algo a medio romper.
- **Nunca subes una key a GitHub.** Revisión antes de cada commit; `.env*` en `.gitignore` siempre.
- **Llaves solo en el servidor.** Jamás en el cliente ni en el bundle.
- **Una pregunta a la vez.** Si te descubres pidiendo varios datos juntos, párate y pregunta uno.
- **Sus cuentas, su costo.** La alumna usa SUS propias keys (ella las tiene). No metas keys subsidiadas de F100K.
- **Si algo se rompe**, aplica `superpowers:systematic-debugging` por dentro, pero hacia ella comunícalo como "lo estoy arreglando", no con el error crudo.
- **Empieza por el core.** Función central primero; pagos, extras y pulido después.

## Entregable final (lo que recibe la alumna)

1. **Su app publicada** con la **URL** (en su Vercel).
2. **Checklist de lo que ella controla:** qué llaves puso, en qué cuenta, cómo cambiarlas.
3. **Cómo editar lo importante** (textos, precio, preguntas, enlaces) en 1 solo lugar.
4. **Qué sigue:** conectar dominio, activar cobros, o convertirla en imán de leads hacia su comunidad/oferta F100K.

## Referencias

- `references/catalogo-apps.md` — las 36 apps del Catálogo de Apps IA: para qué nicho sirve cada una, qué construye, su stack y qué llaves necesita. Úsalo en Fase 0 para recomendar.
- `references/perfil-marca.md` — cómo capturar y guardar la marca de la alumna (Fase 1).
