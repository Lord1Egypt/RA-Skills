'use client'
// Login con Google (recomendado) y, opcional, enlace mágico por correo.
// El enlace por correo NO funciona para el público hasta conectar un SMTP propio
// (ver references/02-login.md). Si no lo tienes, borra el formulario de correo.
import { createBrowserClient } from '@supabase/ssr'
import { useState } from 'react'

const supabase = createBrowserClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!)

export default function Login() {
  const [correo, setCorreo] = useState('')
  const [estado, setEstado] = useState<'' | 'enviando' | 'enviado' | string>('')
  const next = typeof window !== 'undefined' ? new URLSearchParams(location.search).get('next') ?? '/' : '/'
  const volver = () => `${location.origin}/auth/callback?next=${encodeURIComponent(next)}`

  async function conGoogle() {
    await supabase.auth.signInWithOAuth({ provider: 'google', options: { redirectTo: volver() } })
  }
  async function conCorreo(e: React.FormEvent) {
    e.preventDefault()
    setEstado('enviando')
    const { error } = await supabase.auth.signInWithOtp({ email: correo.trim().toLowerCase(), options: { emailRedirectTo: volver() } })
    // Muestra el error REAL: "Email rate limit exceeded" es el SMTP de prueba de Supabase, no un bug tuyo.
    setEstado(error ? `No se pudo enviar: ${error.message}` : 'enviado')
  }

  return (
    <main style={{ minHeight: '100dvh', display: 'grid', placeItems: 'center', padding: 24, fontFamily: 'system-ui, sans-serif' }}>
      <div style={{ width: '100%', maxWidth: 360 }}>
        <h1 style={{ fontSize: 26, marginBottom: 20 }}>Entrar</h1>
        <button onClick={conGoogle} style={{ width: '100%', padding: 14, borderRadius: 10, border: '1px solid #ccc', fontWeight: 600, cursor: 'pointer' }}>
          Continuar con Google
        </button>
        <form onSubmit={conCorreo} style={{ marginTop: 24, display: 'grid', gap: 10 }}>
          <label htmlFor="correo" style={{ fontSize: 14 }}>O recibe un enlace en tu correo</label>
          <input id="correo" type="email" required autoComplete="email" value={correo} onChange={(e) => setCorreo(e.target.value)}
                 placeholder="el correo con el que pagaste" style={{ padding: 12, borderRadius: 10, border: '1px solid #ccc' }} />
          <button disabled={estado === 'enviando'} style={{ padding: 12, borderRadius: 10, background: '#111', color: '#fff', border: 0, cursor: 'pointer' }}>
            {estado === 'enviando' ? 'Enviando…' : 'Enviarme el enlace'}
          </button>
          {estado === 'enviado' && <p role="status">Listo: revisa tu correo (y la carpeta de spam).</p>}
          {estado.startsWith('No se pudo') && <p role="alert" style={{ color: '#b00020' }}>{estado}</p>}
        </form>
      </div>
    </main>
  )
}
