// CENTRO DE CONTROL — /admin
// De un vistazo: cuántos tienen acceso, cuándo se refrescó la lista por última vez,
// quién intentó entrar y rebotó, y el historial de cambios.
import { redirect } from 'next/navigation'
import { clienteServidor } from '@/lib/portero'
import { soloAdmin } from '@/lib/sesion'
import Panel from './panel'

export const dynamic = 'force-dynamic'

const fecha = (iso: string) => new Date(iso).toLocaleString('es', { dateStyle: 'medium', timeStyle: 'short' })

export default async function Admin() {
  if (!(await soloAdmin())) redirect('/')
  const svc = clienteServidor()

  const [{ count: activos }, { data: lotes }, { data: rebotes }] = await Promise.all([
    svc.from('miembros_activos').select('*', { count: 'exact', head: true }),
    svc.from('lotes_miembros').select('*').order('hecho_en', { ascending: false }).limit(15),
    svc.from('rebotes').select('email, intento_en').order('intento_en', { ascending: false }).limit(30),
  ])

  const ultimoCsv = lotes?.find((l) => l.origen === 'csv' || l.origen === 'cron')
  const horas = ultimoCsv ? (Date.now() - new Date(ultimoCsv.hecho_en).getTime()) / 36e5 : Infinity
  // El aviso que evita el problema de fondo: una lista que nadie refresca deja entrar a quien ya canceló.
  const vieja = horas > 26

  // Un correo que rebota varias veces casi siempre es alguien que PAGÓ con otro correo.
  const porCorreo = new Map<string, number>()
  rebotes?.forEach((r) => porCorreo.set(r.email, (porCorreo.get(r.email) ?? 0) + 1))

  const tarjeta = { padding: 16, border: '1px solid #ddd', borderRadius: 12 } as const
  return (
    <main style={{ maxWidth: 900, margin: '0 auto', padding: 24, fontFamily: 'system-ui, sans-serif' }}>
      <h1>Centro de control</h1>

      <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 12 }}>
        <div style={tarjeta}><small>Con acceso</small><p style={{ fontSize: 32, margin: 0 }}>{activos ?? '—'}</p></div>
        <div style={{ ...tarjeta, borderColor: vieja ? '#d97706' : '#ddd' }}>
          <small>Lista refrescada</small>
          <p style={{ fontSize: 18, margin: '6px 0 0' }}>{ultimoCsv ? fecha(ultimoCsv.hecho_en) : 'Nunca'}</p>
          {vieja && <p style={{ color: '#b45309', margin: '6px 0 0' }}>⚠️ Hace más de un día. Sube el CSV de hoy.</p>}
        </div>
        <div style={tarjeta}><small>Rebotes recientes</small><p style={{ fontSize: 32, margin: 0 }}>{porCorreo.size}</p></div>
      </section>

      <Panel />

      <h2>Quién intentó entrar y no pudo</h2>
      {porCorreo.size === 0 ? <p>Nadie. 🎉</p> : (
        <ul>{[...porCorreo].map(([email, veces]) => <li key={email}>{email} — {veces} {veces === 1 ? 'intento' : 'intentos'}</li>)}</ul>
      )}

      <h2>Historial de cambios</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead><tr><th align="left">Cuándo</th><th align="left">Origen</th><th align="left">Quién</th><th>+</th><th>−</th><th>Total</th></tr></thead>
        <tbody>{lotes?.map((l) => (
          <tr key={l.id} style={{ borderTop: '1px solid #eee' }}>
            <td>{fecha(l.hecho_en)}</td><td>{l.origen}</td><td>{l.nota ?? l.hecho_por}</td>
            <td align="center">{l.agregados}</td><td align="center">{l.quitados}</td><td align="center">{l.total || ''}</td>
          </tr>
        ))}</tbody>
      </table>
    </main>
  )
}
