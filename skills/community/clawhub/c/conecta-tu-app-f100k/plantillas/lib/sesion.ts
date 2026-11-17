// Quién está usando la app ahora mismo (desde el servidor).
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'
import { esAdmin } from './portero'

export async function usuarioActual() {
  const jar = await cookies()
  const supabase = createServerClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!, {
    cookies: {
      getAll: () => jar.getAll(),
      setAll: (lista) => { try { lista.forEach(({ name, value, options }) => jar.set(name, value, options)) } catch { /* en Server Components no se puede escribir: el proxy ya refresca la sesión */ } },
    },
  })
  const { data: { user } } = await supabase.auth.getUser()
  return user
}

// Úsalo al inicio de CADA página y ruta de /admin. Esconder el botón no es seguridad.
export async function soloAdmin(): Promise<string | null> {
  const user = await usuarioActual()
  return user?.email && esAdmin(user.email) ? user.email : null
}
