---
name: conecta-tu-app-f100k
description: "Guía paso a paso para conectar una app a lo que la vuelve un negocio: base de datos (Supabase), login (Google o enlace por correo), el PORTERO (solo entran los correos de quienes pagaron, validado contra Skool, Hotmart, Kajabi, Stripe, Mercado Pago o pagos a mano, sin que estén conectadas entre sí), cobros según el país, centro de control /admin con refresco de la lista, y publicación en Vercel. Claude hace lo técnico y pide solo lo que no puede hacer (crear cuentas, copiar llaves, clics en paneles). Trae plantillas probadas y prompts para copiar y pegar. Usar cuando digan \"cómo conecto el login\", \"conecta Supabase\", \"base de datos para mi app\", \"que solo entren mis alumnos\", \"cómo valido que pagó\", \"que solo entre quien compró mi curso\", \"pasarela de pagos\", \"cómo cobro desde Colombia\", \"Stripe no está en mi país\", \"centro de control\", \"panel admin\", \"webhook de pagos\" o \"conecta mi app\". NO construye la app desde cero (constructor-miniapps-f100k, crea-tu-app-f100k) ni landings de venta."
argument-hint: "[login | base | portero | cobros | control | publicar | todo]"
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - La app tiene que estar en el workspace (`entregables/apps/<app>/`): pídele el `.zip` por Telegram o el link de su repo si conectó SU GitHub. Si no hay app todavía, deriva a `crea-tu-app-f100k`.
> - Aquí nadie mueve su cursor ni entra a sus paneles: la sección de «Claude in Chrome / uso de la computadora» no aplica. Los clics en Supabase, Google Cloud, Vercel, Stripe, Zapier o Skool los hace ella con la ruta exacta que le das; si dudas de que el panel siga igual, pídele una captura por Telegram.
> - El SQL (`plantillas/sql/01-portero.sql`) mándalo como archivo `.sql` para que lo pegue en Supabase → SQL Editor → Run. El MCP de Supabase y `claude mcp add` no existen aquí; usa la API de Supabase solo si ella conectó un token de SU cuenta y te da ✅.
> - Las llaves secretas (`sb_secret_`, `service_role`, `sk_live_`, `whsec_`) no se piden por Telegram: le das el nombre exacto de cada variable y ella las pega directo en Vercel → Settings → Environment Variables. Si alguna hace falta para probar en el servidor, avísale que queda en el historial del chat, guárdala solo en el `.env.local` del proyecto y pídele que borre el mensaje.
> - `npx tsc --noEmit` y `npm run build` sí corren en el servidor (una app a la vez). Supabase local con Docker, `stripe listen` y `vercel crons run` no: las pruebas vivas se hacen en SU despliegue de prueba.
> - **Las apps siempre se despliegan directo en Vercel** con la cuenta de la usuaria (`VERCEL_TOKEN` en el entorno): `vercel --prod --yes --token "$VERCEL_TOKEN"`, y le mandas la URL por Telegram. No hace falta pedir ✅ para desplegar. Nunca `vercel login` desde el servidor ni una cuenta que no sea suya. Si falta `VERCEL_TOKEN`, pídele que lo cree en vercel.com → Account Settings → Tokens y lo agregue al entorno del agente; el `.zip` es solo el último recurso. `vercel env add` con los nombres de variables; los valores secretos los pega ella.
> - `CONEXIONES.md` va en la raíz del proyecto y también se lo mandas por Telegram como documento, sin ningún valor secreto.
> - Para comprobar que el dominio final no redirige (trampa 1 de publicar) usa `curl -sI` o el navegador del agente sobre su URL pública: es una web propia, no una red social.

---

# Conecta tu app

Lleva a la persona desde "tengo una app" hasta "la gente paga, entra sola, y si cancela sale sola". Va **una conexión a la vez**, y cada una se prueba antes de pasar a la siguiente.

## Cómo hablarle (no opcional)

- **Tutea.** Cero jerga sin traducir: "el candado de la base" (RLS), "el aviso que manda la plataforma cuando alguien paga" (webhook), "la llave maestra" (service_role).
- **Un paso por mensaje.** Termina cada mensaje con lo único que tiene que hacer y qué debería ver al terminar. Espera su "listo".
- **Tú haces todo lo que puedas hacer.** Terminal, archivos, SQL por MCP, variables con `vercel env add`, deploy. A la persona le pides solo: crear cuentas, iniciar sesión, copiar una llave, hacer clic en un panel, pagar un plan.
- **Instrucción de clic = ruta exacta.** `Supabase → Project Settings → API Keys → botón "Reveal" junto a secret`. Si no tienes certeza de que la ruta siga así (los paneles cambian), díselo y pídele una captura.
- **Si falla, es problema → causa → arreglo**, en tres líneas. Nunca un volcado de logs.

## ¿Puede Claude mover mi cursor para mostrarme dónde hacer clic?

Pregunta frecuente. Respuesta honesta (verificada el 15-sep-2026 en support.claude.com):
- **Señalarte con TU cursor dónde hacer clic: no existe.**
- **Claude in Chrome** (extensión, planes pagos): Claude hace los clics **él mismo** en tu Chrome mientras miras (crear el proyecto de Supabase, configurar Google, etc.).
- **Uso de la computadora en Claude Desktop / Cowork** (beta, Pro y Max, macOS 15+ o Windows): Claude abre apps y hace clic por ti.
- **Lo más confiable**, y lo que usa esta skill por defecto: Claude hace casi todo por **terminal y MCP**, así quedan muy pocos clics que explicar.

Si tiene Claude in Chrome conectado, **ofrécelo** para los paneles ("¿quieres que lo haga yo en tu Chrome mientras miras?"). Aunque lo tenga, **la persona** escribe sus contraseñas, datos de tarjeta y datos bancarios, y **la persona** acepta los permisos de Google.

## Paso 0 · Diagnóstico (siempre: 4 preguntas, una por una)

1. **¿Qué hace tu app y dónde está?** Mira la carpeta tú mismo: `package.json` → versión de Next. Si es **un solo archivo HTML**, explica en 3 líneas que login y base de datos necesitan servidor, y ofrece pasarla a Next.js conservando el diseño (con `constructor-miniapps-f100k`). Si no hay app todavía, deriva a `crea-tu-app-f100k`.
2. **¿Quién debería poder entrar?** (cualquiera con cuenta / solo quien pagó / solo miembros de mi comunidad)
3. **¿Qué vendes y dónde te pagan hoy, o dónde piensas cobrar?** (curso, membresía, comunidad, servicio o la app misma · Skool, Hotmart, Kajabi, Stripe, Mercado Pago, transferencia, todavía no cobro). No asumas ninguna plataforma: la skill sirve igual para quien no tiene comunidad.
4. **¿En qué país vives** (para la pasarela) **y dónde está tu público?**

Con eso arma el **mapa** y muéstraselo antes de tocar nada:

```
Tu app: [nombre]           Conectamos, en este orden:
 ✅ 1. Base de datos       Supabase (región: São Paulo)
 ✅ 2. Login               Google
 ✅ 3. Portero             lista desde Skool: altas por Zapier + CSV para bajas
 ⬜ 4. Cobros              (ya cobras en Skool, no hace falta)
 ✅ 5. Centro de control   /admin
 ✅ 6. Publicar            Vercel + prueba en producción
Tiempo estimado: [X] · Cuentas que vas a necesitar: [lista] · Costos: [lista, "gratis" donde aplique]
```

Checkpoint: "¿Arrancamos por la 1?"

Si el argumento trae un módulo (`/conecta-tu-app-f100k portero`), haz solo las preguntas del diagnóstico que ese módulo necesita, verifica que existan las piezas previas (el portero necesita base y login) y ve directo al módulo.

## Los módulos

Lee la referencia del módulo **antes** de empezarlo. Cada una trae quién hace qué, los clics exactos, las trampas conocidas y la verificación.

| # | Módulo | Referencia | Plantillas |
|---|---|---|---|
| 1 | Base de datos | `references/01-base-de-datos.md` | `plantillas/sql/01-portero.sql` (si va portero) |
| 2 | Login | `references/02-login.md` | `plantillas/app/login`, `app/auth/callback`, `app/auth/salir`, `lib/sesion.ts` |
| 3 | **Portero** | `references/03-portero.md` | `proxy.ts`, `lib/portero.ts`, `lib/leer-csv.ts`, `app/acceso-cerrado`, `app/api/webhooks/{alta,baja,stripe}` |
| 4 | Cobros por país | `references/04-cobros-por-pais.md` | `app/api/webhooks/stripe`, `app/api/cron/refresco` |
| 5 | Centro de control | `references/05-centro-de-control.md` | `app/admin/{page,panel}.tsx`, `app/api/admin/miembros` |
| 6 | Publicar | `references/06-publicar.md` | — |
| — | Prompts armados por plataforma | `references/prompts-por-plataforma.md` | (para quien sigue sin la skill) |
| + | Varias apps, un portero | `references/07-varias-apps-un-portero.md` | (avanzado, solo si lo pide) |

### Cómo usar las plantillas

Las plantillas están **compiladas y probadas de punta a punta** (15-sep-2026: Next 16.1.7 + Supabase local real con 3 usuarios: el que no está en la lista rebota y queda registrado; el admin pasa; CSV con vista previa que no toca nada; alta por webhook; alta manual que sobrevive a otro CSV; quitado de la lista que pierde el acceso en el siguiente clic sin cerrar sesión; freno del 30%; CSV sin correos rechazado; webhook de Stripe con firma real). Úsalas como base, no reescribas desde cero:
1. Copia respetando carpetas (`plantillas/lib/portero.ts` → `lib/portero.ts`). Si el proyecto no usa el alias `@/`, ajusta los imports.
2. **Next 15 o menor:** `proxy.ts` → `middleware.ts` y `export async function proxy` → `export async function middleware`.
3. **Si ya existe un `proxy.ts`/`middleware.ts`,** fusiona. No lo pises. Conserva sus rutas públicas y agrégales `/api/webhooks`, `/api/cron` y `/acceso-cerrado`.
4. Adapta a su app: rutas públicas en `PUBLICAS`, textos TODO de `/acceso-cerrado`, estilo del `/admin` con su marca si tiene `PERFIL-MARCA.md` o `DESIGN.md`.
5. Corre `npx tsc --noEmit` y `npm run build` antes de decir que está.

## Checkpoints (no se salta ninguno)

Al cerrar cada módulo:
1. Corre la **verificación** de su referencia. Tiene que ser prueba **viva** (entrar, llamar al webhook, mirar la tabla), no "compila".
2. Díselo en una línea con evidencia: "✅ Login: entraste con tu segunda cuenta de Google y te devolvió a /admin".
3. Actualiza el mapa (✅) y pregunta si seguimos con el próximo.

Nunca dejes un módulo a medias. Si hay que parar, deja todo funcionando y anota en `CONEXIONES.md` en qué paso quedó.

## Guardarraíles

- **Llaves:** la maestra solo en el servidor, nunca con `NEXT_PUBLIC_`, nunca en `'use client'`. `.env*` en `.gitignore` **antes** del primer commit (compruébalo con `git check-ignore .env.local`). Antes de cada commit: `git diff --cached | grep -nE "sb_secret_|eyJhbGciOi|sk_live_|sk_test_|whsec_"` tiene que salir vacío.
- **Sus cuentas, su costo.** Todo va a nombre de la persona. Nunca uses llaves ni cuentas tuyas.
- **Nada de datos de pago en tus manos.** Nunca le pidas el número de tarjeta, los datos bancarios ni la contraseña. Los escribe la persona en el sitio oficial.
- **Datos de países y pasarelas:** usa `04-cobros-por-pais.md`. Si su fecha tiene más de 3 meses o el país no está, verifica en la fuente oficial antes de recomendar. **Nunca de memoria.**
- **Eventos de plataformas** (nombres de triggers y webhooks): verifica en la documentación actual. Si no puedes verificar, dilo.
- **Modo prueba antes que real** en cualquier cobro.
- **No borres su lista ni sus tablas** para "empezar limpio" sin preguntar y sin exportar antes.
- Si algo se rompe, aplica `superpowers:systematic-debugging` por dentro y a la persona háblale en simple.

## Entregable final

1. App publicada con la URL, y cada módulo del mapa en ✅ con su prueba viva.
2. **`CONEXIONES.md`** en la raíz del proyecto (sin valores secretos):
   - Qué conectaste, en qué cuenta y dónde se cambia cada cosa (ruta de clics).
   - Nombres de las variables de entorno (sin sus valores) y en qué panel está cada una.
   - URLs de webhooks y cron con el dominio final.
   - **La rutina**: "Cada [día], exporta el CSV de [plataforma] y súbelo en /admin" (si la plataforma no tiene API).
   - Qué hacer si alguien dice "pagué y no puedo entrar": mirar rebotes → dar acceso manual.
3. Si prefiere seguir por su cuenta o compartirlo con alguien de su equipo: `references/prompts-para-copiar.md` tiene los mismos pasos como prompts sueltos, y `references/prompts-por-plataforma.md` trae el portero y el centro de control ya armados para su plataforma (dale el de la suya, no el genérico).
