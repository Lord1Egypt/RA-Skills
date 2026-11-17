// Cerrar sesión (lo usa el botón "Entrar con otro correo").
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

export async function POST(req: Request) {
  const jar = await cookies()
  const supabase = createServerClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!, {
    cookies: { getAll: () => jar.getAll(), setAll: (l) => l.forEach(({ name, value, options }) => jar.set(name, value, options)) },
  })
  await supabase.auth.signOut()
  return NextResponse.redirect(new URL('/login', req.url), 303)
}
