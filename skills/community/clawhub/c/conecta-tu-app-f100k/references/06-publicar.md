# 06 · Publicar y dejarlo funcionando solo

## Variables en Vercel

Vercel → tu proyecto → **Settings → Environment Variables**. Claude te da la lista exacta según lo que conectaste:

| Variable | Cuándo |
|---|---|
| `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` | Siempre |
| `ADMIN_EMAILS` | Portero / centro de control |
| `WEBHOOK_SECRET` | Altas y bajas por Zapier/Make |
| `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` | Stripe |
| `CRON_SECRET` | Refresco diario |

Claude las puede cargar por terminal (`vercel env add NOMBRE production`), y así tú solo pegas cada valor cuando te lo pide. **Después de cambiar variables hay que volver a desplegar**, porque las variables nuevas no llegan a un despliegue viejo.

## Las 6 trampas de publicar (todas silenciosas)

1. **El dominio final.** Si `tuapp.com` redirige a `www.tuapp.com` (o al revés), los webhooks y el cron tienen que apuntar a **la que queda en la barra del navegador**. Si apuntan a la otra, la redirección se come la llamada: Zapier o Stripe ven una respuesta 3xx, tu código nunca corre y no aparece ningún error. Claude lo comprueba con `curl -sI https://tu-dominio/api/webhooks/alta` (tiene que responder 405 o 401, **no** 307/308).
2. **Cron en plan gratis (Hobby): máximo 1 vez al día**, y corre en algún momento dentro de esa hora (±59 min). Si pones algo más frecuente, el despliegue falla.
3. **El cron que "corre" sin hacer nada.** Hay que probarlo de verdad: `vercel crons run` (o llamar la ruta con el `CRON_SECRET`) y leer `vercel logs`. Revisa que la respuesta sea `{"ok":true,...}` y no un HTML de login.
4. **Redirect URLs del login.** Al tener dominio, agrégalo en Supabase → Authentication → URL Configuration (Site URL + `/auth/callback`). Si falta, el login "no hace nada" en producción aunque funcione en localhost.
5. **Despliegue bloqueado por el autor del commit.** Si Vercel dice que GitHub "could not associate the committer", el correo de git no es el de tu cuenta de GitHub. Arreglo: `git config user.email "tu-correo-de-github"` en ese proyecto y un commit nuevo.
6. **TypeScript 7 rompe Next 16.1.** Desde 2026, `npm i typescript` instala la versión 7, y `next build` falla con un mensaje que no dice nada: *The "id" argument must be of type string. Received undefined*. Arreglo: `npm i -D typescript@5.9`.

## Prueba final en producción (no en localhost)

- [ ] Login con Google desde otra cuenta → entra.
- [ ] Correo fuera de la lista → `/acceso-cerrado`.
- [ ] Compra de prueba o test del Zap → el correo aparece en `/admin` en menos de 1 minuto.
- [ ] `vercel crons run` → `ok` en los logs (si usas refresco diario).
- [ ] `/admin` desde una cuenta que no es admin → no entra.

Cuando todo esto pase, la app funciona sola: la gente paga → entra; cancela → sale; tú miras `/admin` una vez por semana.
