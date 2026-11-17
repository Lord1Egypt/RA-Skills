'use client'
// Subir el CSV (con vista previa antes de cambiar nada) y agregar/quitar un correo suelto.
import { useRouter } from 'next/navigation'
import { useState } from 'react'

type Resumen = { total: number; agregados: number; quitados: number; descartadas: number; sospechoso: boolean;
  muestraAgregados: string[]; muestraQuitados: string[]; error?: string; ok?: boolean }

export default function Panel() {
  const router = useRouter()
  const [archivo, setArchivo] = useState<File | null>(null)
  const [previa, setPrevia] = useState<Resumen | null>(null)
  const [msg, setMsg] = useState('')
  const [correo, setCorreo] = useState('')

  async function enviar(confirmar: boolean, masivo = false) {
    if (!archivo) return
    const fd = new FormData()
    fd.set('archivo', archivo)
    if (confirmar) fd.set('confirmar', 'si')
    if (masivo) fd.set('confirmar_masivo', 'si')
    setMsg('Leyendo…')
    const r: Resumen = await fetch('/api/admin/miembros', { method: 'POST', body: fd }).then((x) => x.json())
    if (r.error && !r.sospechoso) { setMsg(r.error); return }
    setPrevia(r)
    if (r.ok) { setMsg(`✅ Lista actualizada: ${r.total} con acceso.`); setPrevia(null); setArchivo(null); router.refresh() }
    else setMsg('')
  }

  async function uno(accion: 'agregar' | 'quitar') {
    const r = await fetch('/api/admin/miembros', { method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ accion, email: correo }) }).then((x) => x.json())
    setMsg(r.error ?? `✅ ${correo} ${accion === 'agregar' ? 'agregado' : 'quitado'}. Se queda aunque subas otro CSV, hasta que lo quites.`)
    if (!r.error) { setCorreo(''); router.refresh() }
  }

  return (
    <section style={{ marginTop: 24, display: 'grid', gap: 20 }}>
      <div style={{ padding: 16, border: '1px solid #ddd', borderRadius: 12 }}>
        <h2 style={{ marginTop: 0 }}>Refrescar la lista</h2>
        <p>Exporta los miembros activos de tu plataforma (CSV) y súbelo aquí. Primero te muestro qué cambia.</p>
        <input type="file" accept=".csv,text/csv" onChange={(e) => { setArchivo(e.target.files?.[0] ?? null); setPrevia(null) }} />
        <button disabled={!archivo} onClick={() => enviar(false)} style={{ marginLeft: 8 }}>Ver qué cambia</button>

        {previa && !previa.ok && (
          <div style={{ marginTop: 12 }}>
            <p><b>+{previa.agregados}</b> nuevos · <b>−{previa.quitados}</b> quitados · <b>{previa.total}</b> en total
              {previa.descartadas > 0 && ` · ${previa.descartadas} filas sin correo válido o repetidas`}</p>
            {previa.muestraQuitados.length > 0 && <details><summary>Ver quitados</summary><p>{previa.muestraQuitados.join(', ')}</p></details>}
            {previa.sospechoso ? (
              <>
                <p style={{ color: '#b45309' }}>⚠️ Esto quita a mucha gente de golpe. ¿Exportaste la lista completa y no un filtro?</p>
                <button onClick={() => enviar(true, true)}>Sí, la lista está completa: aplicar</button>
              </>
            ) : <button onClick={() => enviar(true)}>Aplicar cambios</button>}
          </div>
        )}
      </div>

      <div style={{ padding: 16, border: '1px solid #ddd', borderRadius: 12 }}>
        <h2 style={{ marginTop: 0 }}>Un correo suelto</h2>
        <p>Para quien pagó con otro correo o necesita entrar ya.</p>
        <input type="email" value={correo} onChange={(e) => setCorreo(e.target.value)} placeholder="correo@ejemplo.com" aria-label="Correo" />
        <button onClick={() => uno('agregar')} disabled={!correo} style={{ marginLeft: 8 }}>Dar acceso</button>
        <button onClick={() => uno('quitar')} disabled={!correo} style={{ marginLeft: 8 }}>Quitar acceso</button>
      </div>

      {msg && <p role="status">{msg}</p>}
    </section>
  )
}
