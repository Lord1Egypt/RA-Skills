// REFRESCO DIARIO — cada día, la lista se rehace sola desde tu plataforma de cobro.
// Solo sirve si tu plataforma tiene API para listar suscripciones activas (Stripe, Mercado Pago,
// Hotmart…). Skool NO tiene: ahí el refresco es subir el CSV (el centro de control te avisa
// cuando la lista tiene más de un día).
//
// vercel.json:  { "crons": [{ "path": "/api/cron/refresco", "schedule": "0 9 * * *" }] }   (09:00 UTC)
// Vercel manda solo el header  Authorization: Bearer <CRON_SECRET>  si CRON_SECRET existe en tus variables.
//
// DOS TRAMPAS QUE HACEN QUE EL CRON "CORRA" SIN HACER NADA (sin ningún error visible):
//  1. Tu proxy manda /api/cron a /login → la plantilla de proxy.ts ya lo excluye.
//  2. Tu dominio redirige (sin www → con www): Vercel llama a la URL del despliegue y la
//     redirección se come la llamada. Pruébalo con:  vercel crons run  y mira  vercel logs.
//
// Esta versión lee Stripe (npm i stripe). Para otra plataforma, cambia SOLO `correosQuePagan()`.
import { NextResponse } from 'next/server'
import Stripe from 'stripe'
import { clienteServidor, diferencia, esCambioSospechoso, leerLista, normalizarCorreo } from '@/lib/portero'

export const runtime = 'nodejs'
export const maxDuration = 60

async function correosQuePagan(): Promise<{ email: string; nombre: string | null }[]> {
  const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)
  const vistos = new Map<string, string | null>()
  // 'past_due' = el cobro falló pero Stripe sigue reintentando: se le deja entrar esos días.
  for (const status of ['active', 'trialing', 'past_due'] as const) {
    for await (const sub of stripe.subscriptions.list({ status, limit: 100, expand: ['data.customer'] })) {
      const c = sub.customer as Stripe.Customer | Stripe.DeletedCustomer
      if ('email' in c && c.email) vistos.set(normalizarCorreo(c.email), c.name ?? null)
    }
  }
  return [...vistos].map(([email, nombre]) => ({ email, nombre }))
}

export async function GET(req: Request) {
  if (!process.env.CRON_SECRET || req.headers.get('authorization') !== `Bearer ${process.env.CRON_SECRET}`) {
    return NextResponse.json({ error: 'No autorizado.' }, { status: 401 })
  }
  const svc = clienteServidor()
  const filas = await correosQuePagan()
  const actuales = await leerLista(svc)

  // Los que diste de alta A MANO siguen (la función SQL no los borra): cuentan para la comparación.
  const manuales = actuales.filter((a) => a.origen === 'manual').map((a) => ({ email: a.email, nombre: null }))
  const nuevas = [...new Map([...filas, ...manuales].map((f) => [f.email, f])).values()]
  const dif = diferencia(actuales.map((a) => a.email), nuevas.map((f) => f.email))

  // Si la plataforma devuelve casi nada (caída, llave equivocada), NO vacía la lista: falla en rojo.
  if (filas.length === 0 || esCambioSospechoso(actuales.length, dif.quitados.length)) {
    console.error('[refresco] cambio sospechoso, no aplico:', { total: nuevas.length, quitados: dif.quitados.length })
    return NextResponse.json({ error: 'Cambio sospechoso: revisa a mano.', total: nuevas.length, agregados: dif.agregados.length, quitados: dif.quitados.length }, { status: 500 })
  }

  const { error } = await svc.rpc('reemplazar_miembros', {
    p_filas: nuevas, p_hecho_por: 'cron', p_archivo: null,
    p_agregados: dif.agregados.length, p_quitados: dif.quitados.length, p_origen: 'cron',
  })
  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json({ ok: true, total: nuevas.length, agregados: dif.agregados.length, quitados: dif.quitados.length })
}
