// ALTA AUTOMÁTICA — alguien pagó o se unió → entra a la lista en segundos.
// Lo llama Zapier/Make ("nuevo miembro en Skool", "nueva venta en Hotmart", etc.).
//
// Configuración del paso "Webhook POST" en Zapier/Make:
//   URL:      https://TU-DOMINIO-FINAL/api/webhooks/alta   ← el dominio que queda en la barra
//             del navegador DESPUÉS de cualquier redirección (con o sin www). Si apuntas al otro,
//             la redirección 308 se come el POST y nunca llega.
//   Headers:  x-webhook-secret: <el mismo valor que WEBHOOK_SECRET en Vercel>
//   Body JSON: { "email": <correo del trigger>, "nombre": <nombre del trigger> }
import { NextResponse } from 'next/server'
import { clienteServidor, EMAIL_REGEX, normalizarCorreo } from '@/lib/portero'

export async function POST(req: Request) {
  const secreto = req.headers.get('x-webhook-secret')
  if (!process.env.WEBHOOK_SECRET || secreto !== process.env.WEBHOOK_SECRET) {
    return NextResponse.json({ error: 'Secreto incorrecto.' }, { status: 401 })
  }

  let body: { email?: string; nombre?: string }
  try { body = await req.json() } catch { return NextResponse.json({ error: 'El cuerpo no es JSON.' }, { status: 400 }) }

  const email = normalizarCorreo(body.email)
  if (!EMAIL_REGEX.test(email)) return NextResponse.json({ error: `Correo inválido: "${body.email ?? ''}"` }, { status: 400 })

  const svc = clienteServidor()
  const { data: lote, error: e1 } = await svc.from('lotes_miembros')
    .insert({ hecho_por: 'webhook', origen: 'webhook', total: 0, agregados: 1, quitados: 0, nota: email })
    .select('id').single()
  if (e1 || !lote) return NextResponse.json({ error: 'No pude crear el lote.' }, { status: 500 })

  const { error: e2 } = await svc.from('miembros_activos')
    .upsert({ email, nombre: body.nombre?.trim() || null, lote_id: lote.id, origen: 'webhook' })
  if (e2) return NextResponse.json({ error: 'No pude guardar el correo.' }, { status: 500 })

  return NextResponse.json({ ok: true, email })
}
