// STRIPE → LISTA, en tiempo real.
// Pagó (checkout completado) → entra.  Canceló (suscripción terminada) → sale.
//
// En Stripe → Developers → Webhooks → Add endpoint:
//   URL: https://TU-DOMINIO-FINAL/api/webhooks/stripe
//   Eventos: checkout.session.completed, customer.subscription.deleted
//   Copia el "Signing secret" (whsec_…) a STRIPE_WEBHOOK_SECRET en Vercel.
// Requiere: npm i stripe
import Stripe from 'stripe'
import { clienteServidor, esAdmin, EMAIL_REGEX, normalizarCorreo } from '@/lib/portero'

// Stripe firma el cuerpo EXACTO. Hay que leerlo crudo (req.text()), nunca req.json() antes.
export const runtime = 'nodejs'

export async function POST(req: Request) {
  const firma = req.headers.get('stripe-signature')
  if (!firma) return new Response('Falta la firma de Stripe.', { status: 400 })

  const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)
  let evento: Stripe.Event
  try {
    evento = stripe.webhooks.constructEvent(await req.text(), firma, process.env.STRIPE_WEBHOOK_SECRET!)
  } catch (e) {
    // Firma inválida = no lo mandó Stripe (o el secreto no es el de ESTE endpoint).
    return new Response(`Firma inválida: ${e instanceof Error ? e.message : ''}`, { status: 400 })
  }

  const svc = clienteServidor()

  if (evento.type === 'checkout.session.completed') {
    const s = evento.data.object
    const email = normalizarCorreo(s.customer_details?.email ?? s.customer_email)
    if (!EMAIL_REGEX.test(email)) return new Response('Sin correo en el pago.', { status: 200 })
    const { data: lote, error: e1 } = await svc.from('lotes_miembros')
      .insert({ hecho_por: 'stripe', origen: 'pasarela', agregados: 1, nota: `pago: ${email}` }).select('id').single()
    if (e1 || !lote) return new Response('No pude crear el lote.', { status: 500 })
    const { error } = await svc.from('miembros_activos')
      .upsert({ email, nombre: s.customer_details?.name ?? null, lote_id: lote.id, origen: 'pasarela' })
    // 500 = Stripe reintenta solo durante días. Mejor reintento que alguien que pagó y no entra.
    if (error) return new Response(error.message, { status: 500 })
  }

  if (evento.type === 'customer.subscription.deleted') {
    const sub = evento.data.object
    const cliente = await stripe.customers.retrieve(sub.customer as string)
    const email = 'email' in cliente ? normalizarCorreo(cliente.email) : ''
    if (email && !esAdmin(email)) {
      // Tus altas MANUALES no se tocan (becas, socias, quien pagó por otro lado).
      const { error } = await svc.from('miembros_activos').delete().eq('email', email).neq('origen', 'manual')
      if (error) return new Response(error.message, { status: 500 })
      await svc.from('lotes_miembros').insert({ hecho_por: 'stripe', origen: 'pasarela', quitados: 1, nota: `canceló: ${email}` })
    }
  }

  return new Response('ok', { status: 200 })
}
