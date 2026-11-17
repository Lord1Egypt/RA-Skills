// BAJA AUTOMÁTICA — alguien canceló → sale de la lista.
// Úsalo SOLO si tu plataforma avisa cancelaciones de forma confiable (Stripe, Mercado Pago,
// Hotmart lo hacen). Si no (o si tienes dudas), NO lo conectes: las bajas las hace el CSV.
// Mejor que alguien que canceló tenga unos días de gracia a que alguien que pagó quede afuera.
//
// Mismo header que el alta: x-webhook-secret.  Body: { "email": "..." }
import { NextResponse } from 'next/server'
import { clienteServidor, esAdmin, EMAIL_REGEX, normalizarCorreo } from '@/lib/portero'

export async function POST(req: Request) {
  if (!process.env.WEBHOOK_SECRET || req.headers.get('x-webhook-secret') !== process.env.WEBHOOK_SECRET) {
    return NextResponse.json({ error: 'Secreto incorrecto.' }, { status: 401 })
  }
  let body: { email?: string }
  try { body = await req.json() } catch { return NextResponse.json({ error: 'El cuerpo no es JSON.' }, { status: 400 }) }

  const email = normalizarCorreo(body.email)
  if (!EMAIL_REGEX.test(email)) return NextResponse.json({ error: 'Correo inválido.' }, { status: 400 })
  if (esAdmin(email)) return NextResponse.json({ ok: true, nota: 'Es admin: no se quita.' })

  const svc = clienteServidor()
  const { count, error } = await svc.from('miembros_activos').delete({ count: 'exact' }).eq('email', email)
  if (error) return NextResponse.json({ error: 'No pude quitar el correo.' }, { status: 500 })

  await svc.from('lotes_miembros').insert({ hecho_por: 'webhook', origen: 'webhook', total: 0, agregados: 0, quitados: count ?? 0, nota: `baja: ${email}` })
  return NextResponse.json({ ok: true, email, quitado: (count ?? 0) > 0 })
}
