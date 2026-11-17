// EL PORTERO EN LA PUERTA — corre en CADA visita, no solo al iniciar sesión.
// Así, si alguien cancela hoy y mañana se refresca la lista, en su siguiente clic ya no entra.
//
// Next.js 16+: este archivo se llama proxy.ts (en la raíz). En Next 15 o menos se llama
// middleware.ts y la función se exporta como `middleware` en vez de `proxy`.
// Requiere: npm i @supabase/ssr @supabase/supabase-js
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'
import { clienteServidor, registrarRebote, tieneAcceso } from '@/lib/portero'

// Rutas que se ven SIN iniciar sesión. Ajusta a tu app.
const PUBLICAS = ['/', '/login', '/auth', '/acceso-cerrado']

// Rutas que llaman MÁQUINAS, no personas (Zapier, tu pasarela de pago, el cron de Vercel).
// No tienen sesión: si las mandas a /login, el webhook "funciona" pero nunca llega a tu código
// y nadie se entera. Cada una se protege sola con su propio secreto (ver sus route.ts).
const DE_MAQUINAS = ['/api/webhooks', '/api/cron']

const empiezaCon = (ruta: string, lista: string[]) =>
  lista.some((p) => (p === '/' ? ruta === '/' : ruta === p || ruta.startsWith(p + '/')))

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl
  if (empiezaCon(pathname, DE_MAQUINAS)) return NextResponse.next()

  let respuesta = NextResponse.next({ request })
  const supabase = createServerClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!, {
    cookies: {
      getAll: () => request.cookies.getAll(),
      setAll(lista) {
        lista.forEach(({ name, value }) => request.cookies.set(name, value))
        respuesta = NextResponse.next({ request })
        lista.forEach(({ name, value, options }) => respuesta.cookies.set(name, value, options))
      },
    },
  })
  // IMPORTANTE: no pongas código entre createServerClient y getUser().
  const { data: { user } } = await supabase.auth.getUser()

  const redirigir = (a: string, next?: string) => {
    const url = request.nextUrl.clone()
    url.pathname = a
    url.search = next ? `?next=${encodeURIComponent(next)}` : ''
    const r = NextResponse.redirect(url)
    respuesta.cookies.getAll().forEach((c) => r.cookies.set(c.name, c.value, { path: '/', sameSite: 'lax' }))
    return r
  }

  if (!user) {
    return empiezaCon(pathname, PUBLICAS) ? respuesta : redirigir('/login', pathname + request.nextUrl.search)
  }

  // Con sesión: el portero revisa la lista (menos en la propia pantalla de "acceso cerrado",
  // o sería un bucle infinito).
  if (pathname !== '/acceso-cerrado' && !pathname.startsWith('/auth')) {
    const svc = clienteServidor()
    if (!(await tieneAcceso(svc, user.email))) {
      await registrarRebote(svc, user.email ?? '')
      return redirigir('/acceso-cerrado')
    }
  }
  return respuesta
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp|ico)$).*)'],
}
