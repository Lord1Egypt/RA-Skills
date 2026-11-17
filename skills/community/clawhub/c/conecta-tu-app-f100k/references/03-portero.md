# 03 · El portero: solo entra quien está en tu lista

**La pregunta que lo resuelve:** "La gente me paga en una plataforma (Skool, Hotmart, Kajabi, Stripe, Mercado Pago… o por transferencia) y mi app vive en otro lado. ¿Cómo sabe mi app quién pagó, si no están conectadas?"

**La respuesta:** no hace falta conectarlas. Hace falta **una lista**. Tu app guarda en su base de datos los correos de quienes pagaron. Cada vez que alguien abre una página, el portero mira su correo: **si está en la lista, pasa. Si no, ve una pantalla amable que le dice cómo unirse.** Tu tarea es mantener esa lista al día, y eso se puede automatizar casi por completo.

```
[Plataforma donde pagan]  ──(CSV / webhook / API)──▶  [lista: miembros_activos]
                                                              │
[Persona entra con Google] ─▶ proxy.ts: ¿su correo está? ─────┤
                                    sí → entra        no → /acceso-cerrado
```

## Las piezas (todas en `plantillas/`)

| Pieza | Archivo | Qué hace |
|---|---|---|
| La lista + historial + rebotes | `sql/01-portero.sql` | 3 tablas con candado y una función que reemplaza la lista **todo o nada** |
| La regla | `lib/portero.ts` | normaliza correos, admin siempre pasa, cierra si la base no responde |
| La puerta | `proxy.ts` | revisa **en cada visita** (no solo al iniciar sesión) |
| Pantalla amable | `app/acceso-cerrado/page.tsx` | "entraste con otro correo" + botón para unirse |
| Leer el CSV | `lib/leer-csv.ts` | encuentra la columna del correo se llame como se llame |
| Altas automáticas | `app/api/webhooks/alta/route.ts` | Zapier/Make agrega a quien paga, en segundos |
| Bajas automáticas | `app/api/webhooks/baja/route.ts` | solo si tu plataforma avisa cancelaciones |
| Stripe directo | `app/api/webhooks/stripe/route.ts` | pagó → entra; canceló → sale |
| Refresco diario | `app/api/cron/refresco/route.ts` | rehace la lista cada día desde la API de cobro |
| Centro de control | `app/admin/*` + `app/api/admin/miembros` | ver ↓ `05-centro-de-control.md` |

Instalación (Claude): `npm i @supabase/ssr @supabase/supabase-js papaparse` + `npm i -D @types/papaparse` (y `stripe` si aplica). Copia los archivos respetando las carpetas, corre el SQL, agrega `ADMIN_EMAILS` y `WEBHOOK_SECRET` (que se genera con `openssl rand -hex 32`).

## ¿De dónde sale la lista? Según dónde cobras

| Cobras en… | Altas (quien paga entra) | Bajas (quien cancela sale) | Refresco diario automático |
|---|---|---|---|
| **Skool** | Zapier: trigger **"New Paid Member"** → Webhooks by Zapier (POST) → `/api/webhooks/alta` | ❌ Skool **no tiene** trigger de cancelación ni API pública. Las bajas se hacen **subiendo el CSV** de miembros. | ❌ No se puede. El centro de control te **avisa** cuando la lista tiene más de un día. Rutina: Skool → Members → Export → subir. 2 minutos. |
| **Stripe** | Webhook `checkout.session.completed` (plantilla `stripe`) | Webhook `customer.subscription.deleted` | ✅ Cron `refresco` (lee suscripciones activas) |
| **Mercado Pago** | Webhook de suscripciones → tu ruta **consulta la suscripción en la API** antes de dar acceso | Mismo webhook (estado `cancelled`) | ✅ Cron con la búsqueda de suscripciones (preapproval) `authorized` |
| **Hotmart** | Webhook (postback) de compra aprobada → `/api/webhooks/alta` vía Zapier o directo | Webhook de cancelación de suscripción → `/api/webhooks/baja` | Posible con su API. Si no, CSV. |
| **Kajabi, Teachable, Circle, Gumroad u otra** | Si tiene webhooks o Zapier → `/api/webhooks/alta` | Si avisa cancelaciones → `/api/webhooks/baja`; si no, CSV | Si tiene API, sí. Claude revisa su documentación actual. |
| **Lemon Squeezy / Polar / Paddle** | Webhook de orden o suscripción creada | Webhook de suscripción cancelada/expirada | ✅ Con su API |
| **Transferencia, efectivo, a mano** | Centro de control → "Dar acceso" | Centro de control → "Quitar acceso" | — |

Datos de Skool verificados el 15-sep-2026 en zapier.com/apps/skool: los únicos triggers son "New Paid Member" y "Answered Membership Questions". Además, la integración con Zapier requiere el plan **Pro** de Skool, y el paso "Webhooks by Zapier" requiere un plan **pago** de Zapier.

Con cualquier otra plataforma el patrón es el mismo. Claude busca en la documentación actual de tu plataforma (no de memoria) cómo se llaman sus eventos, porque cambian.

## Las 8 reglas del portero (cada una es una falla real que ya pasó)

1. **Revisa en cada visita, no solo al entrar.** Si solo revisas al iniciar sesión, quien canceló sigue adentro durante semanas con la sesión abierta.
2. **El correo se normaliza siempre**: minúsculas y sin espacios, en los dos lados. `Ana@Gmail.com ` y `ana@gmail.com` son la misma persona.
3. **Tu correo va en `ADMIN_EMAILS`** y pasa siempre. Si exportas el CSV sin incluirte, no te quedas afuera de tu propia app.
4. **El CSV vacío o raro no toca nada.** La función SQL se niega a vaciar la lista. Y si el cambio quita a más del 30% de la gente, pide confirmar dos veces: casi siempre es un filtro mal exportado.
5. **Primero la vista previa**: "+12 nuevos, −3 quitados". Nada se aplica sin verlo antes.
6. **Las altas automáticas sí, las bajas con cuidado.** Que alguien que pagó no pueda entrar quema la confianza al instante. Que alguien que canceló tenga un día de gracia no le hace daño a nadie. Si dudas de las bajas automáticas, que las haga el CSV.
7. **Las rutas de máquinas no pasan por el login.** `/api/webhooks` y `/api/cron` los llaman Zapier, Stripe y Vercel, que no tienen sesión. Si el proxy los manda a `/login`, el webhook "responde" con una redirección, **tu código nunca corre y nadie se entera**. Cada una se protege con su propio secreto.
8. **Registra los rebotes.** Quien intenta entrar y no puede casi siempre **pagó con otro correo**. Sin el registro esa persona se va en silencio. Con el registro la ves en el centro de control y le das acceso manual.

## Personas con dos correos

Es el caso más común de soporte: pagó con `ana.trabajo@empresa.com` y entra con su Gmail. Hay dos salidas:
- La pantalla de acceso cerrado le dice "entra con el correo con el que pagaste" y trae el botón **Entrar con otro correo**.
- Tú la agregas a mano desde el centro de control. Las altas manuales **no las borra** la siguiente subida de CSV ni el cron: salen solo cuando tú las quitas.

## Verificación (prueba viva, no "compila")

- [ ] Con un correo que **está** en la lista: entra.
- [ ] Con un correo que **no está**: ve `/acceso-cerrado`, y su intento aparece en "Quién intentó entrar".
- [ ] Quitas ese correo desde el centro de control → en su **siguiente clic** ya no entra (sin cerrar sesión).
- [ ] Test del webhook desde Zapier/Stripe → responde 200 y aparece en el historial.
- [ ] Webhook con secreto incorrecto → 401. Sin sesión, `/admin` → te manda a `/login`.
