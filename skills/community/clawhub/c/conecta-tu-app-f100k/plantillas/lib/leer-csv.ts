// Lee el CSV que exportas de Skool, Hotmart, Stripe, Mercado Pago o una hoja de cálculo.
// Cada plataforma llama distinto a la columna del correo. Rechazar el archivo por el nombre
// del encabezado es la causa nº1 de "el CSV no tiene correos" cuando SÍ los tiene.
// Requiere: npm i papaparse && npm i -D @types/papaparse
import Papa from 'papaparse'
import { EMAIL_REGEX, normalizarCorreo } from './portero'

export type Fila = { email: string; nombre: string | null }

const COLUMNAS_CORREO = ['email', 'e-mail', 'mail', 'member email', 'user email', 'customer email',
  'email address', 'correo', 'correo electrónico', 'correo electronico', 'buyer email', 'e-mail do comprador']
const COLUMNAS_NOMBRE = ['nombre', 'nombre completo', 'name', 'full name', 'full_name', 'first name',
  'member name', 'customer name', 'buyer name']

function elegir(encabezados: string[], candidatos: string[]): string | null {
  const porNombre = new Map(encabezados.map((h) => [h.trim().toLowerCase(), h]))
  for (const c of candidatos) if (porNombre.has(c)) return porNombre.get(c)!
  return null
}

// Último recurso: la columna cuyos VALORES son correos, se llame como se llame.
function olfatear(filas: Record<string, string>[], encabezados: string[]): string | null {
  let mejor: { col: string; hits: number } | null = null
  for (const col of encabezados) {
    const hits = filas.filter((f) => EMAIL_REGEX.test(normalizarCorreo(f[col]))).length
    if (hits > 0 && (!mejor || hits > mejor.hits)) mejor = { col, hits }
  }
  // Al menos la mitad de las filas: una columna de notas con un correo suelto no cuenta.
  return mejor && mejor.hits * 2 >= filas.length ? mejor.col : null
}

export function leerCsv(texto: string): { filas: Fila[]; encabezados: string[]; descartadas: number } {
  const r = Papa.parse<Record<string, string>>(texto, { header: true, skipEmptyLines: true, transformHeader: (h) => h.trim() })
  const encabezados = r.meta.fields ?? []
  const datos = r.data ?? []
  const colCorreo = elegir(encabezados, COLUMNAS_CORREO) ?? olfatear(datos, encabezados)
  const colNombre = elegir(encabezados, COLUMNAS_NOMBRE)
  if (!colCorreo) return { filas: [], encabezados, descartadas: datos.length }

  const vistos = new Set<string>()
  const filas: Fila[] = []
  let descartadas = 0
  for (const d of datos) {
    const email = normalizarCorreo(d[colCorreo])
    if (!EMAIL_REGEX.test(email) || vistos.has(email)) { descartadas++; continue }
    vistos.add(email)
    filas.push({ email, nombre: colNombre ? d[colNombre]?.trim() || null : null })
  }
  return { filas, encabezados, descartadas }
}
