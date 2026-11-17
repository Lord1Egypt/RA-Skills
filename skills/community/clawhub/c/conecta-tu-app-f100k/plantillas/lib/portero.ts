// EL PORTERO — decide si un correo entra o no.
// Todo el que lee o escribe la lista pasa por aquí, así la regla vive en un solo lugar.
import { createClient, type SupabaseClient } from '@supabase/supabase-js'

export const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

// "  Ana@Gmail.COM " y "ana@gmail.com" tienen que ser la MISMA persona.
// También quita el BOM invisible que a veces trae la primera celda de un CSV.
export function normalizarCorreo(correo: string | null | undefined): string {
  return (correo ?? '').replace(/^﻿/, '').trim().toLowerCase()
}

// ADMIN_EMAILS="tu@correo.com,socia@correo.com"
// El admin entra SIEMPRE, esté o no en la lista: si exportas el CSV sin incluirte,
// no te quedas afuera de tu propia app.
export function esAdmin(correo: string | null | undefined, adminEmails = process.env.ADMIN_EMAILS): boolean {
  const c = normalizarCorreo(correo)
  if (!c || !adminEmails) return false
  return adminEmails.split(',').map(normalizarCorreo).includes(c)
}

// Cliente con la llave maestra. SOLO en el servidor. Nunca en un archivo con 'use client'
// ni en una variable NEXT_PUBLIC_.
export function clienteServidor(): SupabaseClient {
  return createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!, {
    auth: { persistSession: false, autoRefreshToken: false },
  })
}

export async function tieneAcceso(svc: SupabaseClient, correo: string | null | undefined): Promise<boolean> {
  const c = normalizarCorreo(correo)
  if (!c) return false
  if (esAdmin(c)) return true
  const { data, error } = await svc.from('miembros_activos').select('email').eq('email', c).maybeSingle()
  // Si la base no responde, el portero CIERRA (no deja pasar a ciegas) y lo deja escrito en los logs.
  if (error) {
    console.error('[portero] no pude leer la lista:', error.message)
    return false
  }
  return !!data
}

// Nunca lanza: registrar el rebote no puede tumbar la página.
export async function registrarRebote(svc: SupabaseClient, correo: string): Promise<void> {
  try {
    await svc.from('rebotes').insert({ email: normalizarCorreo(correo) })
  } catch (e) {
    console.error('[portero] no pude registrar el rebote:', e)
  }
}

// Toda la lista. Supabase devuelve máximo 1000 filas por consulta: sin paginar,
// con 1.200 miembros la comparación "quitaría" a 200 que siguen pagando.
export async function leerLista(svc: SupabaseClient): Promise<{ email: string; origen: string }[]> {
  const todos: { email: string; origen: string }[] = []
  for (let desde = 0; ; desde += 1000) {
    const { data, error } = await svc.from('miembros_activos').select('email, origen').order('email').range(desde, desde + 999)
    if (error) throw new Error(error.message)
    todos.push(...(data ?? []))
    if (!data || data.length < 1000) return todos
  }
}

// Compara la lista actual con la nueva ANTES de tocar nada: "+12 nuevos, −3 quitados".
export function diferencia(actuales: string[], nuevos: string[]) {
  const a = new Set(actuales.map(normalizarCorreo))
  const n = new Set(nuevos.map(normalizarCorreo))
  return {
    agregados: [...n].filter((e) => !a.has(e)),
    quitados: [...a].filter((e) => !n.has(e)),
    total: n.size,
  }
}

// Freno de mano: si la lista nueva quita a más del 30% de la gente, algo raro pasó
// (exportaste un filtro, el archivo equivocado, solo una página). Se pide confirmar dos veces.
export function esCambioSospechoso(totalActual: number, quitados: number): boolean {
  return totalActual >= 10 && quitados / totalActual > 0.3
}
