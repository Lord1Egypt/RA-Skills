// La pantalla que ve quien NO está en la lista. Cálida, no acusatoria:
// casi siempre es alguien que pagó con otro correo, no un colado.
// Cambia los 3 textos marcados con TODO.
export default function AccesoCerrado() {
  return (
    <main style={{ minHeight: '100dvh', display: 'grid', placeItems: 'center', padding: 24, fontFamily: 'system-ui, sans-serif' }}>
      <div style={{ maxWidth: 440, textAlign: 'center' }}>
        <p style={{ fontSize: 44, margin: 0 }}>🔑</p>
        <h1 style={{ fontSize: 26, margin: '12px 0 8px' }}>Tu acceso no está activo</h1>
        <p style={{ lineHeight: 1.6, opacity: 0.8 }}>
          Esta app es para miembros de {/* TODO: nombre de tu comunidad o programa */}MI COMUNIDAD.
          Si ya eres miembro, lo más común es que hayas entrado con un correo distinto al que usaste para pagar.
        </p>
        <a href={/* TODO: link para unirse o reactivar */ 'https://TU-LINK-DE-PAGO'}
           style={{ display: 'inline-block', marginTop: 20, padding: '14px 28px', borderRadius: 10, background: '#111', color: '#fff', textDecoration: 'none', fontWeight: 700 }}>
          Unirme o reactivar
        </a>
        <p style={{ marginTop: 20, fontSize: 14, opacity: 0.75 }}>
          ¿Crees que es un error? Escríbenos a {/* TODO: tu correo o WhatsApp de soporte */}soporte@tudominio.com con el correo con el que pagaste.
        </p>
        <form action="/auth/salir" method="post" style={{ marginTop: 12 }}>
          <button style={{ background: 'none', border: 0, textDecoration: 'underline', cursor: 'pointer', opacity: 0.7 }}>Entrar con otro correo</button>
        </form>
      </div>
    </main>
  )
}
