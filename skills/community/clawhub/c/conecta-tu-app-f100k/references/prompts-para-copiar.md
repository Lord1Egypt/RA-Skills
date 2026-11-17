# Prompts para copiar y pegar

Para quien **no** tiene la skill instalada. Funcionan en Claude Code (Claude hace los pasos en tu compu) y en claude.ai o Claude Desktop (Claude te da cada paso para que lo copies). Pégalos **en orden** y en la carpeta de tu app. Cada uno termina con una prueba, y no conviene pasar al siguiente hasta que esa prueba funcione.

Cambia lo que está entre [CORCHETES].

¿Cobras en una plataforma concreta? Los prompts 3 (portero) y 5 (centro de control) están **ya armados para cada una** (Skool, Hotmart, Stripe, Mercado Pago, Polar/Lemon Squeezy, otra, o pagos a mano) en `prompts-por-plataforma.md`, junto con un prompt por cada pieza del panel.

---

## 0 · Modo guía (pégalo primero, una sola vez)

> **Qué hace:** hace que Claude te lleve paso a paso, sin volcarte 40 instrucciones juntas.

```
Voy a conectar mi app (login, base de datos, lista de acceso y cobros). No programo.
Reglas para toda esta conversación:
1. Dame UN paso a la vez y espera a que te diga "listo" antes de seguir.
2. Si puedes ejecutar comandos o editar archivos en mi computadora, hazlo tú. Pídeme solo lo que no puedes hacer: crear cuentas, iniciar sesión, copiar una llave de un panel o hacer clic en un botón de un sitio.
3. Cuando me pidas hacer algo en un panel web, dime la ruta exacta de clics (Menú → Sección → Botón) y qué debo ver al terminar.
4. Las llaves secretas nunca van en código que vea el navegador, nunca llevan el prefijo NEXT_PUBLIC_ y nunca se suben a GitHub. Revisa .gitignore antes de cualquier commit.
5. No me digas "listo" hasta que hayamos PROBADO que funciona, y dime cómo lo probamos.
6. Si algo falla, muéstrame el error real en una línea y cómo lo arreglamos. No adivines.
Mi app: [qué hace, en una frase]. Está hecha con: [Next.js / un solo archivo HTML / no sé].
```

---

## 1 · Base de datos (Supabase)

> **Qué hace:** crea el cuaderno donde tu app guarda cosas que tienen que seguir ahí mañana, con candado para que nadie las lea desde afuera.

```
Conecta mi app a Supabase, paso a paso.
- Si mi app es un solo archivo HTML, primero explícame en 3 líneas por qué para login y base de datos necesito pasarla a Next.js, y hazlo tú conservando cómo se ve.
- Guíame para crear el proyecto (región más cercana a mi público: [país]).
- Dime dónde copio las 3 llaves (URL, anon/publishable y service_role/secret) y guárdalas en .env.local. La service_role SOLO se usa en el servidor.
- Cada tabla con RLS encendido. Las que solo toca el servidor van SIN políticas (y avísame que desde el navegador van a devolver vacío sin error). Las de cada usuario van con la política auth.uid() = user_id.
- Prueba final: una consulta real desde el servidor que responda sin error, y revisión de Advisors → Security.
```

---

## 2 · Login con Google

> **Qué hace:** cada persona entra con su cuenta de Google. Solo contesta "quién eres". Si puede entrar, lo decide el paso 3.

```
Agrega login con Google usando Supabase Auth (@supabase/ssr) a mi app Next.js.
- Guíame en Google Cloud: crear el cliente OAuth tipo "Web application", con redirect URI https://[mi-project-ref].supabase.co/auth/v1/callback.
- IMPORTANTE: recuérdame publicar la app en Google Auth Platform → Audience → "In production". Si queda en Testing, solo entran los testers.
- En Supabase: activar Google y configurar Site URL y Redirect URLs (localhost:3000/auth/callback y mi dominio final /auth/callback).
- Crea /login, /auth/callback (que solo acepte rutas internas en ?next=) y un botón de cerrar sesión.
- Si además quiero enlace mágico por correo: avísame que el correo de fábrica de Supabase solo manda 2 por hora y SOLO a correos del equipo del proyecto, y guíame para conectar SMTP propio con Resend (necesito un dominio).
- Prueba final: entrar con una cuenta de Google que NO sea la mía.
```

---

## 3 · El portero: solo entra quien pagó

> **Versión armada para tu plataforma:** `prompts-por-plataforma.md` → «El portero, según dónde cobras».

> **Qué hace:** tu app guarda una lista de correos. Si el correo de quien entra no está en la lista, no pasa y ve una pantalla amable. Así tu app valida contra Skool, Hotmart, Kajabi, Stripe o donde cobres (incluso si te pagan por transferencia), **sin que las plataformas estén conectadas entre sí**.

```
Quiero que solo entren a mi app las personas que pagaron. Vendo: [curso / membresía / comunidad / servicio / la app misma]. Cobro en: [Skool / Hotmart / Kajabi / Stripe / Mercado Pago / Polar / Lemon Squeezy / transferencia o efectivo / otra].
Construye un "portero" así:
1. Tabla miembros_activos (email como llave, siempre en minúsculas y sin espacios), tabla lotes_miembros (historial de cada cambio: origen csv/manual/webhook/pasarela/cron, agregados, quitados) y tabla rebotes (quién intentó entrar y no pudo). RLS encendido y sin políticas: solo el servidor las toca.
2. Función SQL que reemplace la lista TODO O NADA. Tiene que negarse si la lista nueva viene vacía y NO borrar a los que agregué a mano.
3. proxy.ts (o middleware.ts si mi Next es 15 o menor) que revise la lista EN CADA VISITA, no solo al iniciar sesión. Mi correo va en ADMIN_EMAILS y pasa siempre. Si la base no responde, el portero cierra.
4. /api/webhooks y /api/cron NO pasan por el login (los llaman máquinas). Cada uno se protege con su propio secreto.
5. Página /acceso-cerrado amable: "quizás entraste con otro correo distinto al que usaste para pagar", un botón para unirme ([mi link de pago]) y "entrar con otro correo".
6. Webhook /api/webhooks/alta con header x-webhook-secret para que [Zapier / mi plataforma] agregue a quien paga. Si me pagan por transferencia o efectivo, no hace falta webhook: doy acceso a mano desde el panel. Busca en la documentación ACTUAL de mi plataforma cómo se llaman sus eventos de pago y de cancelación; no lo digas de memoria. Si mi plataforma no avisa cancelaciones (Skool no lo hace), las bajas se hacen subiendo el CSV de miembros.
7. Registra cada rebote.
Prueba final: un correo en la lista entra; uno fuera ve /acceso-cerrado y aparece en rebotes; si lo quito, en su siguiente clic ya no entra; el webhook con el secreto incorrecto da 401.
```

---

## 4 · Cobrar según mi país

> **Qué hace:** elige la pasarela que sí funciona donde vives y la conecta a la lista del paso 3.

```
Vivo en [país] y quiero cobrar [suscripción mensual / pago único] de [precio y moneda] a gente de [países].
1. Revisa HOY en las páginas oficiales qué pasarelas me aceptan (stripe.com/global, la documentación de Mercado Pago, y la lista de países de Polar, Lemon Squeezy y Paddle). Dame una tabla con 2 o 3 opciones: comisión, si cobran por mí (merchant of record) y a dónde me pagan. Recomiéndame UNA.
2. Usa el link de pago de la plataforma (no programes un checkout).
3. Conecta su webhook de pago → agrega el correo a miembros_activos; y el de cancelación → lo quita (menos los que agregué a mano). Verifica la firma del aviso; si la plataforma solo manda un id, consulta ese id en su API antes de dar acceso.
4. Si la plataforma tiene API, agrega un cron diario (/api/cron/refresco, protegido con CRON_SECRET) que rehaga la lista desde las suscripciones activas y que NO aplique cambios si quitaría a más del 30%.
Prueba final en modo prueba: compra con tarjeta de prueba → el correo aparece en la lista en menos de 1 minuto.
```

---

## 5 · Centro de control

> **Versión armada para tu plataforma, o una sola pieza del panel:** `prompts-por-plataforma.md`.

> **Qué hace:** tu panel /admin para manejar la lista sin tocar código.

```
Crea /admin (solo para ADMIN_EMAILS, verificado en el servidor en cada página y ruta):
- Cuántas personas tienen acceso y cuándo se refrescó la lista (en naranja si pasó más de 1 día).
- Subir el CSV exportado de mi plataforma. Que encuentre la columna del correo aunque se llame "Email", "Correo electrónico" o "Customer Email", o por su contenido. PRIMERO muestra "+nuevos / −quitados" con la lista de quitados, y solo aplica si confirmo. Si quita a más del 30%, que pida una segunda confirmación.
- Dar o quitar acceso a un correo suelto (las altas manuales se quedan aunque suba otro CSV).
- Quién intentó entrar y no pudo, agrupado por correo.
- Historial de cambios.
- Ojo: Supabase devuelve máximo 1000 filas por consulta; pagina al leer la lista completa.
Prueba final: sube un CSV de prueba, mira la vista previa, aplícalo y revisa que el historial lo muestre.
```

---

## 6 · Publicar y probar en producción

> **Qué hace:** sube la app a internet y comprueba que todo funcione sin ti.

```
Publica mi app en Vercel y verifica todo EN PRODUCCIÓN, no en localhost:
- Carga las variables de entorno (dime cuáles faltan) y vuelve a desplegar.
- Averigua cuál es mi dominio FINAL (con o sin www, el que queda después de las redirecciones) y usa ese en los webhooks, en el cron y en las Redirect URLs de Supabase. Compruébalo con curl -sI: la ruta del webhook tiene que responder 401 o 405, no 307/308.
- Si hay cron: recuerda que en el plan gratis corre máximo 1 vez al día. Ejecútalo a mano y lee los logs; la respuesta tiene que ser ok, no un HTML de login.
- Si next build falla con 'The "id" argument must be of type string', instala typescript@5.9.
Prueba final: login con otra cuenta, correo fuera de la lista → acceso cerrado, compra o test de webhook → aparece en /admin.
```

---

## 7 · Me trabé

```
Esto no funciona: [qué esperaba que pasara y qué pasó].
El error exacto es: [pégalo, o describe la captura].
Antes de cambiar código: dime la causa más probable y cómo la comprobamos con UN comando o UNA mirada al panel. Revisa primero lo típico: una variable de entorno que falta en Vercel, un redirect de dominio que se come el webhook, RLS devolviendo vacío desde el navegador, la app de Google en "Testing", o la Redirect URL que falta en Supabase.
```
