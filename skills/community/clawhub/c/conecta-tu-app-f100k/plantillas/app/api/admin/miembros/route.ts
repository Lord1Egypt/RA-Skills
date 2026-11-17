// CENTRO DE CONTROL — cambiar la lista.
// POST multipart con `archivo` (CSV):
//     sin `confirmar`  → SOLO muestra qué pasaría (+nuevos / −quitados). No toca nada.
//     confirmar=si     → reemplaza la lista entera en una sola operación.
//     Si quita a más del 30%: exige además confirmar_masivo=si.
// POST JSON { accion: 'agregar' | 'quitar', email } → cambio de UN correo.
//     Los agregados a mano NO los borra la siguiente subida de CSV: salen solo si los quitas tú.
import { NextResponse } from 'next/server'
import { leerCsv } from '@/lib/leer-csv'
import { clienteServidor, diferencia, EMAIL_REGEX, esCambioSospechoso, leerLista, normalizarCorreo } from '@/lib/portero'
import { soloAdmin } from '@/lib/sesion'

export const runtime = 'nodejs'

export async function POST(req: Request) {
  const admin = await soloAdmin()
  if (!admin) return NextResponse.json({ error: 'Solo admins.' }, { status: 403 })
  const svc = clienteServidor()

  if (req.headers.get('content-type')?.includes('application/json')) {
    const { accion, email: crudo } = (await req.json()) as { accion?: string; email?: string }
    const email = normalizarCorreo(crudo)
    if (!EMAIL_REGEX.test(email)) return NextResponse.json({ error: 'Correo inválido.' }, { status: 400 })
    const agregar = accion === 'agregar'
    const { data: lote } = await svc.from('lotes_miembros')
      .insert({ hecho_por: admin, origen: 'manual', agregados: agregar ? 1 : 0, quitados: agregar ? 0 : 1, nota: email })
      .select('id').single()
    const { error } = agregar
      ? await svc.from('miembros_activos').upsert({ email, lote_id: lote!.id, origen: 'manual' })
      : await svc.from('miembros_activos').delete().eq('email', email)
    if (error) return NextResponse.json({ error: error.message }, { status: 500 })
    return NextResponse.json({ ok: true })
  }

  const form = await req.formData()
  const archivo = form.get('archivo')
  if (!(archivo instanceof File)) return NextResponse.json({ error: 'Falta el archivo CSV.' }, { status: 400 })

  const { filas, encabezados, descartadas } = leerCsv(await archivo.text())
  if (filas.length === 0) {
    return NextResponse.json({
      error: `No encontré correos en el archivo. Columnas que vi: ${encabezados.join(', ') || '(ninguna)'}.`,
    }, { status: 400 })
  }

  const lista = await leerLista(svc)
  const actuales = lista.map((m) => m.email)
  const manuales = lista.filter((m) => m.origen === 'manual').map((m) => m.email)
  const dif = diferencia(actuales, [...filas.map((f) => f.email), ...manuales])
  const sospechoso = esCambioSospechoso(actuales.length, dif.quitados.length)
  const resumen = {
    total: dif.total, descartadas, sospechoso,
    agregados: dif.agregados.length, quitados: dif.quitados.length,
    muestraAgregados: dif.agregados.slice(0, 20), muestraQuitados: dif.quitados.slice(0, 20),
  }

  if (form.get('confirmar') !== 'si') return NextResponse.json({ vistaPrevia: true, ...resumen })
  if (sospechoso && form.get('confirmar_masivo') !== 'si') {
    return NextResponse.json({ error: `Esto quitaría a ${dif.quitados.length} de ${actuales.length}. Confirma de nuevo si es correcto.`, ...resumen }, { status: 409 })
  }

  const { error } = await svc.rpc('reemplazar_miembros', {
    p_filas: filas, p_hecho_por: admin, p_archivo: archivo.name,
    p_agregados: dif.agregados.length, p_quitados: dif.quitados.length,
  })
  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json({ ok: true, ...resumen })
}
