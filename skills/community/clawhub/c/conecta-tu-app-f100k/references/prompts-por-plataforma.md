# Prompts por plataforma

Las versiones ARMADAS de los prompts 3 (portero) y 5 (centro de control) de `prompts-para-copiar.md`: ya traen lo que cambia según dónde cobras, así que no hay que adaptar nada. Cada uno funciona pegado solo, en una conversación nueva. Cambia lo que está entre [CORCHETES].

Si usas la skill no hacen falta: `/conecta-tu-app-f100k portero` o `/conecta-tu-app-f100k control` hace lo mismo con las plantillas probadas.

---

## El portero, según dónde cobras

### Skool

> **Termina probando:** el botón "Test" del Zap agrega un correo y aparece en la lista con origen webhook; el mismo aviso con el secreto incorrecto da 401.

```
Quiero que solo entren a mi app las personas que pagaron. Cobro en: Skool.
No programo. Hazlo tú: ejecuta comandos y edita archivos. Pídeme solo lo que no puedes hacer (crear cuentas, iniciar sesión, copiar una llave, hacer clic en un panel), dame UN paso a la vez con la ruta exacta de clics y espera mi "listo". Las llaves secretas van solo en el servidor, nunca con NEXT_PUBLIC_ y nunca en GitHub. No me digas "listo" hasta probarlo.

Antes de empezar, revisa mi carpeta: si mi app todavía no tiene base de datos (Supabase) y login, dímelo y armamos eso primero.

El portero (igual para cualquier plataforma):
- Tabla miembros_activos (email como llave, siempre en minúsculas y sin espacios; columna origen: csv/manual/webhook/pasarela/cron), tabla lotes_miembros (historial de cada cambio: origen, agregados, quitados) y tabla rebotes (quién intentó entrar y no pudo). RLS encendido y SIN políticas: solo el servidor las toca.
- Función SQL que reemplace la lista TODO O NADA: se niega si la lista nueva viene vacía y NO borra a los que agregué a mano.
- proxy.ts (o middleware.ts si mi Next es 15 o menor) que revise la lista EN CADA VISITA, no solo al iniciar sesión. Mi correo va en ADMIN_EMAILS y pasa siempre. Si la base no responde, el portero cierra.
- /api/webhooks y /api/cron NO pasan por el login (los llaman máquinas). Cada uno se protege con su propio secreto.
- Página /acceso-cerrado amable: "quizás entraste con un correo distinto al que usaste para pagar", un botón para unirme ([mi link de pago]) y "entrar con otro correo".
- Registra cada rebote.

Cómo se llena la lista desde Skool:
- Altas: en Zapier, disparador de Skool "New Paid Member" → acción "Webhooks by Zapier" (POST) a https://[mi dominio]/api/webhooks/alta con el header x-webhook-secret. Guíame clic por clic en Zapier y dime qué campo del disparador trae el correo.
- Avísame antes de empezar: la integración de Skool con Zapier pide el plan Pro de Skool, y el paso "Webhooks by Zapier" pide un plan pago de Zapier. Confirma HOY en zapier.com/apps/skool que los disparadores sigan siendo esos.
- Bajas: Skool no avisa cancelaciones y no tiene API pública. NO inventes un webhook de baja: quien cancela sale cuando subo el CSV de miembros de Skool desde /admin.
- Refresco diario: no se puede automático. Que /admin me avise en naranja cuando la lista tenga más de 1 día.

Prueba final: un correo en la lista entra; uno fuera ve /acceso-cerrado y aparece en rebotes; si lo quito, en su siguiente clic ya no entra; el botón "Test" del Zap agrega un correo y aparece en la lista con origen webhook; el mismo aviso con el secreto incorrecto da 401.
```

### Hotmart

> **Termina probando:** el evento de prueba desde el panel de Hotmart agrega el correo a la lista; un aviso sin el token correcto no toca nada.

```
Quiero que solo entren a mi app las personas que pagaron. Cobro en: Hotmart.
No programo. Hazlo tú: ejecuta comandos y edita archivos. Pídeme solo lo que no puedes hacer (crear cuentas, iniciar sesión, copiar una llave, hacer clic en un panel), dame UN paso a la vez con la ruta exacta de clics y espera mi "listo". Las llaves secretas van solo en el servidor, nunca con NEXT_PUBLIC_ y nunca en GitHub. No me digas "listo" hasta probarlo.

Antes de empezar, revisa mi carpeta: si mi app todavía no tiene base de datos (Supabase) y login, dímelo y armamos eso primero.

El portero (igual para cualquier plataforma):
- Tabla miembros_activos (email como llave, siempre en minúsculas y sin espacios; columna origen: csv/manual/webhook/pasarela/cron), tabla lotes_miembros (historial de cada cambio: origen, agregados, quitados) y tabla rebotes (quién intentó entrar y no pudo). RLS encendido y SIN políticas: solo el servidor las toca.
- Función SQL que reemplace la lista TODO O NADA: se niega si la lista nueva viene vacía y NO borra a los que agregué a mano.
- proxy.ts (o middleware.ts si mi Next es 15 o menor) que revise la lista EN CADA VISITA, no solo al iniciar sesión. Mi correo va en ADMIN_EMAILS y pasa siempre. Si la base no responde, el portero cierra.
- /api/webhooks y /api/cron NO pasan por el login (los llaman máquinas). Cada uno se protege con su propio secreto.
- Página /acceso-cerrado amable: "quizás entraste con un correo distinto al que usaste para pagar", un botón para unirme ([mi link de pago]) y "entrar con otro correo".
- Registra cada rebote.

Cómo se llena la lista desde Hotmart:
- Altas: el webhook (postback) de compra aprobada de Hotmart → /api/webhooks/alta.
- Bajas: el webhook de cancelación de suscripción → /api/webhooks/baja (sin tocar a los que agregué a mano).
- Antes de tocar la lista, comprueba que el aviso venga de verdad de Hotmart con su token de verificación.
- Busca en la documentación ACTUAL de Hotmart el nombre exacto de cada evento y en qué menú se configura el webhook. No lo digas de memoria.
- Refresco diario: si mi cuenta tiene acceso a la API de Hotmart, cron /api/cron/refresco (protegido con CRON_SECRET) que rehaga la lista con las suscripciones activas y NO aplique si quitaría a más del 30%. Si no, las bajas que se escapen las corrijo subiendo el CSV desde /admin.

Prueba final: un correo en la lista entra; uno fuera ve /acceso-cerrado y aparece en rebotes; si lo quito, en su siguiente clic ya no entra; el evento de prueba desde el panel de Hotmart agrega el correo a la lista; un aviso sin el token correcto no toca nada.
```

### Stripe

> **Termina probando:** compra en modo prueba con la tarjeta 4242 4242 4242 4242 → el correo aparece en la lista en menos de 1 minuto; un aviso con firma falsa da 400.

```
Quiero que solo entren a mi app las personas que pagaron. Cobro en: Stripe.
No programo. Hazlo tú: ejecuta comandos y edita archivos. Pídeme solo lo que no puedes hacer (crear cuentas, iniciar sesión, copiar una llave, hacer clic en un panel), dame UN paso a la vez con la ruta exacta de clics y espera mi "listo". Las llaves secretas van solo en el servidor, nunca con NEXT_PUBLIC_ y nunca en GitHub. No me digas "listo" hasta probarlo.

Antes de empezar, revisa mi carpeta: si mi app todavía no tiene base de datos (Supabase) y login, dímelo y armamos eso primero.

El portero (igual para cualquier plataforma):
- Tabla miembros_activos (email como llave, siempre en minúsculas y sin espacios; columna origen: csv/manual/webhook/pasarela/cron), tabla lotes_miembros (historial de cada cambio: origen, agregados, quitados) y tabla rebotes (quién intentó entrar y no pudo). RLS encendido y SIN políticas: solo el servidor las toca.
- Función SQL que reemplace la lista TODO O NADA: se niega si la lista nueva viene vacía y NO borra a los que agregué a mano.
- proxy.ts (o middleware.ts si mi Next es 15 o menor) que revise la lista EN CADA VISITA, no solo al iniciar sesión. Mi correo va en ADMIN_EMAILS y pasa siempre. Si la base no responde, el portero cierra.
- /api/webhooks y /api/cron NO pasan por el login (los llaman máquinas). Cada uno se protege con su propio secreto.
- Página /acceso-cerrado amable: "quizás entraste con un correo distinto al que usaste para pagar", un botón para unirme ([mi link de pago]) y "entrar con otro correo".
- Registra cada rebote.

Cómo se llena la lista desde Stripe:
- Uso el link de pago de Stripe (no programes un checkout).
- Webhook /api/webhooks/stripe: pago completado (checkout.session.completed) → agrega el correo; suscripción cancelada (customer.subscription.deleted) → lo quita, menos los que agregué a mano. Confirma los nombres de los eventos en la documentación actual de Stripe.
- Verifica la FIRMA de cada aviso con STRIPE_WEBHOOK_SECRET, leyendo el cuerpo en crudo. Sin firma válida, 400 y no se toca la lista.
- Cron diario /api/cron/refresco (protegido con CRON_SECRET) que rehaga la lista desde las suscripciones activas en Stripe y NO aplique si quitaría a más del 30%.
- Todo en modo prueba primero.

Prueba final: un correo en la lista entra; uno fuera ve /acceso-cerrado y aparece en rebotes; si lo quito, en su siguiente clic ya no entra; compra en modo prueba con la tarjeta 4242 4242 4242 4242 → el correo aparece en la lista en menos de 1 minuto; un aviso con firma falsa da 400.
```

### Mercado Pago

> **Termina probando:** suscripción con un usuario de prueba → el correo aparece en la lista; al cancelarla, sale; un aviso con un id inventado no agrega a nadie.

```
Quiero que solo entren a mi app las personas que pagaron. Cobro en: Mercado Pago.
No programo. Hazlo tú: ejecuta comandos y edita archivos. Pídeme solo lo que no puedes hacer (crear cuentas, iniciar sesión, copiar una llave, hacer clic en un panel), dame UN paso a la vez con la ruta exacta de clics y espera mi "listo". Las llaves secretas van solo en el servidor, nunca con NEXT_PUBLIC_ y nunca en GitHub. No me digas "listo" hasta probarlo.

Antes de empezar, revisa mi carpeta: si mi app todavía no tiene base de datos (Supabase) y login, dímelo y armamos eso primero.

El portero (igual para cualquier plataforma):
- Tabla miembros_activos (email como llave, siempre en minúsculas y sin espacios; columna origen: csv/manual/webhook/pasarela/cron), tabla lotes_miembros (historial de cada cambio: origen, agregados, quitados) y tabla rebotes (quién intentó entrar y no pudo). RLS encendido y SIN políticas: solo el servidor las toca.
- Función SQL que reemplace la lista TODO O NADA: se niega si la lista nueva viene vacía y NO borra a los que agregué a mano.
- proxy.ts (o middleware.ts si mi Next es 15 o menor) que revise la lista EN CADA VISITA, no solo al iniciar sesión. Mi correo va en ADMIN_EMAILS y pasa siempre. Si la base no responde, el portero cierra.
- /api/webhooks y /api/cron NO pasan por el login (los llaman máquinas). Cada uno se protege con su propio secreto.
- Página /acceso-cerrado amable: "quizás entraste con un correo distinto al que usaste para pagar", un botón para unirme ([mi link de pago]) y "entrar con otro correo".
- Registra cada rebote.

Cómo se llena la lista desde Mercado Pago:
- Uso el link de suscripción de Mercado Pago (no programes un checkout).
- Webhook /api/webhooks/mercadopago para las suscripciones. NUNCA le creas al aviso solo: trae un id; consulta ese id en la API de Mercado Pago con mi Access Token (solo en el servidor) y según el estado agrega el correo (autorizada) o lo quita (cancelada), menos los que agregué a mano.
- Verifica también la firma del aviso con la clave secreta del webhook.
- Busca en la documentación ACTUAL de Mercado Pago cómo se llama el tema de suscripciones y sus estados. No lo digas de memoria.
- Cron diario /api/cron/refresco (protegido con CRON_SECRET) que rehaga la lista con las suscripciones autorizadas y NO aplique si quitaría a más del 30%.
- Primero con credenciales y usuarios de prueba.

Prueba final: un correo en la lista entra; uno fuera ve /acceso-cerrado y aparece en rebotes; si lo quito, en su siguiente clic ya no entra; suscripción con un usuario de prueba → el correo aparece en la lista; al cancelarla, sale; un aviso con un id inventado no agrega a nadie.
```

### Polar · Lemon Squeezy

> **Termina probando:** compra en modo prueba → el correo aparece en la lista en menos de 1 minuto; un aviso con firma falsa no toca nada.

```
Quiero que solo entren a mi app las personas que pagaron. Cobro en: [Polar / Lemon Squeezy].
No programo. Hazlo tú: ejecuta comandos y edita archivos. Pídeme solo lo que no puedes hacer (crear cuentas, iniciar sesión, copiar una llave, hacer clic en un panel), dame UN paso a la vez con la ruta exacta de clics y espera mi "listo". Las llaves secretas van solo en el servidor, nunca con NEXT_PUBLIC_ y nunca en GitHub. No me digas "listo" hasta probarlo.

Antes de empezar, revisa mi carpeta: si mi app todavía no tiene base de datos (Supabase) y login, dímelo y armamos eso primero.

El portero (igual para cualquier plataforma):
- Tabla miembros_activos (email como llave, siempre en minúsculas y sin espacios; columna origen: csv/manual/webhook/pasarela/cron), tabla lotes_miembros (historial de cada cambio: origen, agregados, quitados) y tabla rebotes (quién intentó entrar y no pudo). RLS encendido y SIN políticas: solo el servidor las toca.
- Función SQL que reemplace la lista TODO O NADA: se niega si la lista nueva viene vacía y NO borra a los que agregué a mano.
- proxy.ts (o middleware.ts si mi Next es 15 o menor) que revise la lista EN CADA VISITA, no solo al iniciar sesión. Mi correo va en ADMIN_EMAILS y pasa siempre. Si la base no responde, el portero cierra.
- /api/webhooks y /api/cron NO pasan por el login (los llaman máquinas). Cada uno se protege con su propio secreto.
- Página /acceso-cerrado amable: "quizás entraste con un correo distinto al que usaste para pagar", un botón para unirme ([mi link de pago]) y "entrar con otro correo".
- Registra cada rebote.

Cómo se llena la lista desde [Polar / Lemon Squeezy]:
- Uso el link de pago de la plataforma (no programes un checkout).
- Webhook: orden o suscripción creada/activa → agrega el correo. Suscripción terminada → lo quita, menos los que agregué a mano.
- OJO con "cancelada": en estas plataformas quien cancela suele seguir activo hasta el fin del período que pagó. Quítalo cuando termine ese período, no el día que cancela. Revisa en la documentación ACTUAL qué evento marca el final.
- Verifica la firma de cada aviso con el secreto del webhook.
- Cron diario /api/cron/refresco (protegido con CRON_SECRET) que rehaga la lista desde su API y NO aplique si quitaría a más del 30%.
- Todo en modo prueba primero.

Prueba final: un correo en la lista entra; uno fuera ve /acceso-cerrado y aparece en rebotes; si lo quito, en su siguiente clic ya no entra; compra en modo prueba → el correo aparece en la lista en menos de 1 minuto; un aviso con firma falsa no toca nada.
```

### Kajabi, Teachable, Circle, Gumroad u otra

> **Termina probando:** un evento o compra de prueba agrega el correo a la lista; el webhook con el secreto incorrecto da 401.

```
Quiero que solo entren a mi app las personas que pagaron. Cobro en: [Kajabi / Teachable / Circle / Gumroad / escribe cuál].
No programo. Hazlo tú: ejecuta comandos y edita archivos. Pídeme solo lo que no puedes hacer (crear cuentas, iniciar sesión, copiar una llave, hacer clic en un panel), dame UN paso a la vez con la ruta exacta de clics y espera mi "listo". Las llaves secretas van solo en el servidor, nunca con NEXT_PUBLIC_ y nunca en GitHub. No me digas "listo" hasta probarlo.

Antes de empezar, revisa mi carpeta: si mi app todavía no tiene base de datos (Supabase) y login, dímelo y armamos eso primero.

El portero (igual para cualquier plataforma):
- Tabla miembros_activos (email como llave, siempre en minúsculas y sin espacios; columna origen: csv/manual/webhook/pasarela/cron), tabla lotes_miembros (historial de cada cambio: origen, agregados, quitados) y tabla rebotes (quién intentó entrar y no pudo). RLS encendido y SIN políticas: solo el servidor las toca.
- Función SQL que reemplace la lista TODO O NADA: se niega si la lista nueva viene vacía y NO borra a los que agregué a mano.
- proxy.ts (o middleware.ts si mi Next es 15 o menor) que revise la lista EN CADA VISITA, no solo al iniciar sesión. Mi correo va en ADMIN_EMAILS y pasa siempre. Si la base no responde, el portero cierra.
- /api/webhooks y /api/cron NO pasan por el login (los llaman máquinas). Cada uno se protege con su propio secreto.
- Página /acceso-cerrado amable: "quizás entraste con un correo distinto al que usaste para pagar", un botón para unirme ([mi link de pago]) y "entrar con otro correo".
- Registra cada rebote.

Cómo se llena la lista desde [Kajabi / Teachable / Circle / Gumroad / escribe cuál]:
- Primero busca en la documentación ACTUAL de mi plataforma si tiene webhooks, integración con Zapier o Make, y API. Dime en 3 líneas qué se puede automatizar y qué no. No lo digas de memoria.
- Si avisa cuando alguien paga: → /api/webhooks/alta con el header x-webhook-secret (directo o por Zapier).
- Si avisa cuando alguien cancela: → /api/webhooks/baja. Si NO avisa, no inventes nada: las bajas entran cuando subo el CSV de miembros desde /admin.
- Si tiene API: cron diario /api/cron/refresco (protegido con CRON_SECRET) que NO aplique si quitaría a más del 30%.

Prueba final: un correo en la lista entra; uno fuera ve /acceso-cerrado y aparece en rebotes; si lo quito, en su siguiente clic ya no entra; un evento o compra de prueba agrega el correo a la lista; el webhook con el secreto incorrecto da 401.
```

### Transferencia, efectivo o WhatsApp

> **Termina probando:** doy acceso a un correo desde /admin y entra; se lo quito y en su siguiente clic ya no entra.

```
Quiero que solo entren a mi app las personas que pagaron. Cobro en: transferencia, efectivo o WhatsApp (sin plataforma).
No programo. Hazlo tú: ejecuta comandos y edita archivos. Pídeme solo lo que no puedes hacer (crear cuentas, iniciar sesión, copiar una llave, hacer clic en un panel), dame UN paso a la vez con la ruta exacta de clics y espera mi "listo". Las llaves secretas van solo en el servidor, nunca con NEXT_PUBLIC_ y nunca en GitHub. No me digas "listo" hasta probarlo.

Antes de empezar, revisa mi carpeta: si mi app todavía no tiene base de datos (Supabase) y login, dímelo y armamos eso primero.

El portero (igual para cualquier plataforma):
- Tabla miembros_activos (email como llave, siempre en minúsculas y sin espacios; columna origen: csv/manual/webhook/pasarela/cron), tabla lotes_miembros (historial de cada cambio: origen, agregados, quitados) y tabla rebotes (quién intentó entrar y no pudo). RLS encendido y SIN políticas: solo el servidor las toca.
- Función SQL que reemplace la lista TODO O NADA: se niega si la lista nueva viene vacía y NO borra a los que agregué a mano.
- proxy.ts (o middleware.ts si mi Next es 15 o menor) que revise la lista EN CADA VISITA, no solo al iniciar sesión. Mi correo va en ADMIN_EMAILS y pasa siempre. Si la base no responde, el portero cierra.
- /api/webhooks y /api/cron NO pasan por el login (los llaman máquinas). Cada uno se protege con su propio secreto.
- Página /acceso-cerrado amable: "quizás entraste con un correo distinto al que usaste para pagar", un botón para unirme ([mi link de pago]) y "entrar con otro correo".
- Registra cada rebote.

Cómo se llena la lista desde transferencia, efectivo o WhatsApp (sin plataforma):
- No hay plataforma que avise: NO hagas webhooks ni cron.
- Las altas y bajas las hago yo desde /admin con "Dar acceso" y "Quitar acceso". Arma al menos esa parte del centro de control.
- Cada alta y baja queda en el historial con origen manual.
- En /acceso-cerrado, en lugar del link de pago, pon cómo pagarme: [mi WhatsApp o mis datos de pago].

Prueba final: un correo en la lista entra; uno fuera ve /acceso-cerrado y aparece en rebotes; si lo quito, en su siguiente clic ya no entra; doy acceso a un correo desde /admin y entra; se lo quito y en su siguiente clic ya no entra.
```

---

## Centro de control completo

El panel entero. Lo único que cambia según la plataforma es cómo se actualiza la lista; aquí va la versión de Skool, y abajo la línea para las demás.

```
Crea el centro de control /admin de mi app. Cobro en: Skool.
No programo. Hazlo tú: ejecuta comandos y edita archivos. Pídeme solo lo que no puedes hacer (crear cuentas, iniciar sesión, copiar una llave, hacer clic en un panel), dame UN paso a la vez con la ruta exacta de clics y espera mi "listo". Las llaves secretas van solo en el servidor, nunca con NEXT_PUBLIC_ y nunca en GitHub. No me digas "listo" hasta probarlo.

Antes de empezar, revisa que mi app ya tenga el portero (tablas miembros_activos, lotes_miembros y rebotes). Si no está, dímelo y lo armamos primero.

Seguridad: solo entran los correos de ADMIN_EMAILS, verificado EN EL SERVIDOR en cada página y en cada ruta /api/admin. Esconder el botón no cuenta.

Lo que lleva el panel:
1. Arriba, 3 tarjetas: cuántas personas tienen acceso, hace cuánto se refrescó la lista (en naranja si pasó más de 1 día) y cuántos rebotes hubo.
2. Refrescar la lista con un CSV: encuentra la columna del correo aunque se llame "Email", "Correo electrónico" o "Customer Email", o por su contenido. PRIMERO muestra "+nuevos / −quitados" con la lista de quitados y no toca nada; aplica solo cuando confirmo. Si quitaría a más del 30%, pide una segunda confirmación. Un CSV sin correos se rechaza sin tocar la lista.
3. Dar o quitar acceso a un correo suelto. Las altas manuales se quedan aunque suba otro CSV o corra el cron; salen solo cuando yo las quito.
4. Quién intentó entrar y no pudo, agrupado por correo con el número de intentos, y un botón "Dar acceso" al lado de cada uno.
5. Historial de cambios: fecha, origen, cuántos entraron y cuántos salieron.

Cómo se actualiza la lista: Exporto el CSV de miembros desde Skool. Como Skool no avisa cancelaciones, esta subida es la que saca a quien canceló: hazla lo más cómoda posible.
Ojo: Supabase devuelve máximo 1000 filas por consulta; pagina al leer la lista completa.

Prueba final: entra con un correo que no es admin a /admin y a /api/admin → no pasa; sube un CSV de prueba, mira la vista previa sin que cambie nada, aplícalo y revisa que el historial lo muestre; da acceso a un correo suelto y comprueba que sigue ahí después de subir otro CSV.
```

Si no cobras en Skool, cambia la línea «Cómo se actualiza la lista» y la de «Cobro en» por la de tu caso:

- **Hotmart:** Exporto el CSV de compradores o suscriptores activos de Hotmart cuando quiero corregir la lista a mano.
- **Stripe:** La lista se rehace sola con el cron. El CSV queda de respaldo, y el panel muestra cuándo corrió el cron por última vez y si falló.
- **Mercado Pago:** La lista se rehace sola con el cron. El CSV queda de respaldo, y el panel muestra cuándo corrió el cron por última vez y si falló.
- **Polar · Lemon Squeezy:** La lista se rehace sola con el cron. El CSV queda de respaldo, y el panel muestra cuándo corrió el cron por última vez y si falló.
- **Kajabi, Teachable, Circle, Gumroad u otra:** Exporto el CSV de miembros de mi plataforma. Si mi plataforma no avisa cancelaciones, esta subida es la que saca a quien canceló.
- **Transferencia, efectivo o WhatsApp:** No uso CSV para el día a día: lo importante es dar y quitar acceso. Deja la subida de CSV solo para cargar mi lista inicial.

---

## Una sola pieza del centro de control

Para quien ya tiene el panel y le falta una parte.

### 1 · Arriba: 3 tarjetas de estado

```
En el centro de control /admin de mi app agrega solo esto: Arriba, 3 tarjetas: cuántas personas tienen acceso, hace cuánto se refrescó la lista (en naranja si pasó más de 1 día) y cuántos rebotes hubo.
Verifica en el servidor que solo lo usen los correos de ADMIN_EMAILS. No cambies nada más. No programo. Hazlo tú: ejecuta comandos y edita archivos. Pídeme solo lo que no puedes hacer (crear cuentas, iniciar sesión, copiar una llave, hacer clic en un panel), dame UN paso a la vez con la ruta exacta de clics y espera mi "listo". Las llaves secretas van solo en el servidor, nunca con NEXT_PUBLIC_ y nunca en GitHub. No me digas "listo" hasta probarlo.
```

### 2 · Refrescar la lista con un CSV

```
En el centro de control /admin de mi app agrega solo esto: Refrescar la lista con un CSV: encuentra la columna del correo aunque se llame "Email", "Correo electrónico" o "Customer Email", o por su contenido. PRIMERO muestra "+nuevos / −quitados" con la lista de quitados y no toca nada; aplica solo cuando confirmo. Si quitaría a más del 30%, pide una segunda confirmación. Un CSV sin correos se rechaza sin tocar la lista.
Verifica en el servidor que solo lo usen los correos de ADMIN_EMAILS. No cambies nada más. No programo. Hazlo tú: ejecuta comandos y edita archivos. Pídeme solo lo que no puedes hacer (crear cuentas, iniciar sesión, copiar una llave, hacer clic en un panel), dame UN paso a la vez con la ruta exacta de clics y espera mi "listo". Las llaves secretas van solo en el servidor, nunca con NEXT_PUBLIC_ y nunca en GitHub. No me digas "listo" hasta probarlo.
```

### 3 · Un correo suelto

```
En el centro de control /admin de mi app agrega solo esto: Dar o quitar acceso a un correo suelto. Las altas manuales se quedan aunque suba otro CSV o corra el cron; salen solo cuando yo las quito.
Verifica en el servidor que solo lo usen los correos de ADMIN_EMAILS. No cambies nada más. No programo. Hazlo tú: ejecuta comandos y edita archivos. Pídeme solo lo que no puedes hacer (crear cuentas, iniciar sesión, copiar una llave, hacer clic en un panel), dame UN paso a la vez con la ruta exacta de clics y espera mi "listo". Las llaves secretas van solo en el servidor, nunca con NEXT_PUBLIC_ y nunca en GitHub. No me digas "listo" hasta probarlo.
```

### 4 · Quién intentó entrar

```
En el centro de control /admin de mi app agrega solo esto: Quién intentó entrar y no pudo, agrupado por correo con el número de intentos, y un botón "Dar acceso" al lado de cada uno.
Verifica en el servidor que solo lo usen los correos de ADMIN_EMAILS. No cambies nada más. No programo. Hazlo tú: ejecuta comandos y edita archivos. Pídeme solo lo que no puedes hacer (crear cuentas, iniciar sesión, copiar una llave, hacer clic en un panel), dame UN paso a la vez con la ruta exacta de clics y espera mi "listo". Las llaves secretas van solo en el servidor, nunca con NEXT_PUBLIC_ y nunca en GitHub. No me digas "listo" hasta probarlo.
```
