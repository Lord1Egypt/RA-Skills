# 02 · Login (que cada persona entre con SU cuenta)

El login solo contesta **quién eres**. **Si puedes entrar** lo decide otra pieza: el portero (03). Son dos cosas distintas y conviene no mezclarlas.

## Qué método elegir

| Método | Recomendado cuando | Lo que cuesta montarlo |
|---|---|---|
| **Google** | Casi siempre. Tu público ya tiene Gmail y entra con 1 clic. | 10 min en Google Cloud (una sola vez). |
| **Enlace mágico por correo** | Tu público no usa Google (empresas con Outlook, gente mayor). | Tienes que conectar un **SMTP propio** (abajo). Sin eso **no funciona** con el público. |
| Contraseña | Casi nunca. | Olvidos, reseteos y soporte. Evítala. |

Lo ideal es Google + enlace mágico. La plantilla `plantillas/app/login/page.tsx` trae los dos.

## Google, paso a paso

**En Google Cloud** (console.cloud.google.com), lo haces tú y Claude te va dictando:
1. Arriba a la izquierda: **selector de proyecto → New project** → nombre de tu app → Create.
2. Menú → **Google Auth Platform** (antes "OAuth consent screen") → **Get started**: nombre de la app, tu correo de soporte, público **External**.
3. **Clients → Create client** → tipo **Web application**.
   - **Authorized redirect URIs** → pega exactamente: `https://TU_PROJECT_REF.supabase.co/auth/v1/callback`
     (la URL exacta aparece en Supabase → Authentication → Sign In / Providers → Google, con botón de copiar).
4. Copia el **Client ID** y el **Client secret**.
5. ⚠️ **Audience → Publish app** ("In production"). Si se queda en "Testing", **solo entran los correos que agregues como testers**, y a todos los demás les sale un error de acceso bloqueado. Es la falla nº1 del login con Google y no avisa en ningún lado.

**En Supabase:**
6. **Authentication → Sign In / Providers → Google** → Enable → pega Client ID y Client secret → Save.
7. **Authentication → URL Configuration**:
   - **Site URL**: tu dominio final (`https://tuapp.com`). Mientras no tengas uno, `http://localhost:3000`, y lo cambias al publicar.
   - **Redirect URLs**: agrega `http://localhost:3000/auth/callback` **y** `https://TU-DOMINIO-FINAL/auth/callback`. Si falta una, Supabase te devuelve a la Site URL sin iniciar sesión y parece que "no hace nada".

## Enlace mágico: el correo de fábrica NO sirve para el público

Esto está verificado en la documentación de Supabase: el correo que viene incluido manda **2 mensajes por hora** y **solo entrega a los correos del equipo del proyecto**. A cualquier otra persona le responde "Email address not authorized". En tus pruebas funciona (porque tú eres del equipo) y con tu primer cliente real falla. Por eso engaña tanto.

**Solución: SMTP propio con Resend** (resend.com, plan gratis):
1. Resend → **Domains → Add domain** → agrega los registros DNS que te muestra en tu proveedor de dominio (Claude te dice cuáles, uno por uno). Espera a que diga **Verified**. Sin dominio propio no se puede, porque no se puede mandar "desde" un Gmail.
2. Resend → **API Keys → Create** → cópiala.
3. Supabase → **Authentication → Emails → SMTP Settings** → Enable custom SMTP:
   - Host `smtp.resend.com` · Port `465` · Username `resend` · Password = la API key
   - Sender email: `hola@tudominio.com` · Sender name: tu marca
4. Después sube el límite en **Authentication → Rate Limits** (emails por hora).
5. Opcional: traduce la plantilla en **Authentication → Emails → Templates → Magic Link** (viene en inglés).

## Verificación antes de seguir

- [ ] Entraste con Google desde **una cuenta que no es la tuya** (o desde una ventana de incógnito con otra cuenta).
- [ ] Si usas enlace mágico: llegó a un correo **que no es del equipo** del proyecto, y no a spam.
- [ ] Al cerrar sesión y volver a una página privada, te manda a `/login`, y al entrar te devuelve a esa misma página.
