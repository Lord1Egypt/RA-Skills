// A donde vuelve la persona después de elegir su cuenta de Google o tocar el enlace del correo.
// Esta URL exacta tiene que estar en Supabase → Authentication → URL Configuration → Redirect URLs:
//   http://localhost:3000/auth/callback   y   https://TU-DOMINIO-FINAL/auth/callback
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

export async function GET(req: Request) {
  const url = new URL(req.url)
  const code = url.searchParams.get('code')
  const next = url.searchParams.get('next') ?? '/'
  // Solo rutas internas: "//sitio-malo.com" no cuenta como ruta interna.
  const destino = next.startsWith('/') && !next.startsWith('//') ? next : '/'

  if (code) {
    const jar = await cookies()
    const supabase = createServerClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!, {
      cookies: { getAll: () => jar.getAll(), setAll: (l) => l.forEach(({ name, value, options }) => jar.set(name, value, options)) },
    })
    const { error } = await supabase.auth.exchangeCodeForSession(code)
    if (!error) return NextResponse.redirect(new URL(destino, url.origin))
  }
  return NextResponse.redirect(new URL('/login?error=enlace', url.origin))
}
