// ═══════════════════════════════════════════════════════════════════
// MOTOR — Analiza tu Contenido (FÓRMULA 100K)
//
// Toda la aritmética del método vive aquí y SOLO aquí. La IA etiqueta
// y redacta; nunca calcula un número que salga en el informe.
// Sin dependencias: corre igual en Node, en el navegador o dentro de una app web.
//
// Reglas (idénticas a EL TABLERO y a la guía del Grimorio):
//   · Regla del Lote: ≥ 9 posts Y ≥ 30 días publicando.
//   · Siempre MEDIANA, nunca promedio.
//   · Línea base vs este mes. Primer mes: 20 más viejos vs 10 más nuevos.
//   · Los 5 filtros se leen EN ORDEN; el primero que cae es el tapado
//     y los de atrás no se leen. Sin dato = ni pasa ni se tapa.
//   · Filtro 1 es un «y»: vistas Y % no seguidores ≥ línea base.
//   · ORO = 25 % de arriba, CHATARRA = 25 % de abajo, redondeo hacia abajo.
//   · Una vez es suerte, dos es patrón.
// ═══════════════════════════════════════════════════════════════════

export const LOTE_MINIMO = 9
export const DIAS_MINIMOS = 30

export const FILTROS = [
  { n: 1, nombre: 'Alcance', pregunta: '¿Te vieron fuera de tu casa?',
    columna: 'pct_no_seguidores', columnaEtiqueta: '% de vistas de no seguidores',
    arreglo: 'El tema solo se entiende si ya te conocen. Tu trabajo del mes es darle entrada al desconocido: contexto en los primeros segundos y temas que no dependan de conocerte.' },
  { n: 2, nombre: 'Retención', pregunta: '¿Se quedaron viendo?',
    columna: 'retencion_3s', columnaEtiqueta: 'retención a los 3 segundos',
    arreglo: 'Si la caída es a los 3 segundos, el problema es el gancho. Si la caída es al medio, el problema es el ritmo y el desarrollo.' },
  { n: 3, nombre: 'Valor', pregunta: '¿Les sirvió tanto como para guardarlo o mandarlo?',
    columna: 'valor_1000', columnaEtiqueta: 'guardados + compartidos por cada 1.000 vistas',
    arreglo: 'Es contenido de consumo: se ve y se olvida. Tu trabajo del mes es subir un peldaño — de SAFE a REAL, de REAL a RAW, de RAW a ÚTIL.' },
  { n: 4, nombre: 'Conversión', pregunta: '¿El que llegó de afuera quiso quedarse?',
    columna: 'tasa_conv', columnaEtiqueta: 'seguidores nuevos por cada 100 vistas de no seguidores',
    arreglo: 'Llegaron y no se quedaron porque no prometiste que hay más. Tu trabajo del mes es la promesa de serie y el perfil que la sostiene.' },
  { n: 5, nombre: 'Intención', pregunta: '¿Te buscaron para lo que ofreces?',
    columna: 'intencion', columnaEtiqueta: 'visitas al perfil + toques al enlace + DMs',
    arreglo: 'El contenido funciona, la oferta no se está pidiendo. Tu trabajo del mes es el CTA y la oferta, no el contenido.' },
]

export const MEZCLAS = {
  0: { rep: 60, var_: 30, apo: 10, nota: 'Ningún filtro se tapó. La mezcla se queda en la base 60 / 30 / 10: se sostiene lo que ya funciona y se sigue midiendo.' },
  1: { rep: 40, var_: 30, apo: 30, nota: 'Filtro tapado 1 · Alcance. APOSTAR sube a 30 %: tus formatos ya no salen de tu casa y hace falta sangre nueva. VARIAR se queda en 30 %; los 20 puntos salen enteros de REPETIR.' },
  2: { rep: 60, var_: 30, apo: 10, nota: 'Filtro tapado 2 · Retención. La mezcla no se mueve, pero todo el trabajo del mes va al gancho: mismo molde, primeros 3 segundos rehechos.' },
  3: { rep: 50, var_: 40, apo: 10, nota: 'Filtro tapado 3 · Valor. VARIAR sube a 40 %: mismo formato ganador, ángulo un peldaño más útil. Ese 10 % sale de REPETIR.' },
  4: { rep: 60, var_: 40, apo: 0, nota: 'Filtro tapado 4 · Conversión. No se tocan los formatos: APOSTAR baja a 0 % y ese 10 % se va a VARIAR — mismo formato, ángulo hacia promesa y serie.' },
  5: { rep: 60, var_: 30, apo: 10, nota: 'Filtro tapado 5 · Intención. La mezcla no se mueve: el trabajo del mes es la oferta y el CTA, no el contenido.' },
}

export const PROPOSITOS = ['Experimentación', 'Crecimiento', 'Nutrición', 'Venta']

export const ANGULOS_QUE_PESAN = {
  Experimentación: { lista: ['Opinión', 'Curiosidad', 'Lista abierta'], por: 'Amplios a propósito: sirven para descubrir a quién le hablas.' },
  Crecimiento: { lista: ['Error común', 'Dolor concreto', 'Contraintuitivo'], por: 'Le hablan a quien todavía no te conoce.' },
  Nutrición: { lista: ['Método', 'Detrás de escena', 'Creencia'], por: 'Construyen confianza en quien ya llegó.' },
  Venta: { lista: ['Prueba / resultado', 'Objeción', 'Comparación'], por: 'Mueven de «me gusta lo que veo» a «lo quiero».' },
}

// Un ángulo se corona con la columna de SU trabajo, no con la del filtro tapado.
export const CORONA_ANGULO = {
  Crecimiento: { filtro: 1, columna: 'pct_no_seguidores', trabajo: 'salir de tu casa' },
  Nutrición: { filtro: 3, columna: 'valor_1000', trabajo: 'servirle a quien ya llegó' },
  Venta: { filtro: 5, columna: 'intencion', trabajo: 'mover a alguien hacia tu oferta' },
  Experimentación: null,
}

// ── utilidades ────────────────────────────────────────────────────
const esNum = (x) => typeof x === 'number' && Number.isFinite(x)

export function mediana(valores) {
  const v = valores.filter(esNum).sort((a, b) => a - b)
  if (v.length === 0) return null
  const m = Math.floor(v.length / 2)
  return v.length % 2 ? v[m] : (v[m - 1] + v[m]) / 2
}

export function promedio(valores) {
  const v = valores.filter(esNum)
  return v.length ? v.reduce((a, b) => a + b, 0) / v.length : null
}

const redondear = (x, dec) => (esNum(x) ? Math.round(x * 10 ** dec) / 10 ** dec : null)

// Columnas que Instagram no da y el método necesita.
export function derivar(m = {}) {
  const vistas = m.vistas
  const gc = esNum(m.guardados) || esNum(m.compartidos) ? (m.guardados || 0) + (m.compartidos || 0) : null
  const valor_1000 = esNum(vistas) && vistas > 0 && gc !== null ? redondear((gc / vistas) * 1000, 1) : null
  const vistasNoSeg = esNum(vistas) && esNum(m.pct_no_seguidores) ? (vistas * m.pct_no_seguidores) / 100 : null
  const tasa_conv = esNum(m.seguidores_nuevos) && vistasNoSeg ? redondear((m.seguidores_nuevos / vistasNoSeg) * 100, 2) : null
  const señales = [m.visitas_perfil, m.toques_enlace, m.dms]
  const intencion = señales.some(esNum) ? señales.reduce((a, b) => a + (esNum(b) ? b : 0), 0) : null
  return { valor_1000, tasa_conv, intencion }
}

// Un filtro se lee solo si cada ventana tiene su mínimo de Reels con ese dato: 5, o la mitad si la ventana es chica.
export const MIN_DATO_VENTANA = 5
export const minimoPorVentana = (n) => Math.min(MIN_DATO_VENTANA, Math.ceil(n / 2))

// Las estadísticas avanzadas solo están en la app del teléfono: se piden por captura.
export const DATOS_AVANZADOS = [
  {
    clave: 'retencion', nombre: 'Retención', columnas: ['retencion_3s', 'duracion_media'], filtro: 2,
    captura: 'En la app: el Reel → Ver estadísticas → Retención. Que se vea la gráfica, la tasa de omisión y el tiempo de visualización promedio.',
    desbloquea: 'Filtro 2 · ¿Se quedaron viendo? Dice si el problema es el gancho (caída a los 3 s) o el desarrollo (caída al medio).',
  },
  {
    clave: 'perfil', nombre: 'Actividad en el perfil', columnas: ['visitas_perfil', 'toques_enlace', 'dms'], filtro: 5,
    captura: 'En la app: el Reel → Ver estadísticas → Actividad en el perfil. Que se vean las visitas al perfil y los toques en enlaces externos. Los DMs que trajo, anótalos tú.',
    desbloquea: 'Filtro 5 · Intención. Sin esto el ángulo de venta sale «posible» (medido con conversión) y no se puede armar campaña.',
  },
]

function calidadDatos(posts) {
  const tiene = (p, cols) => cols.some((c) => esNum(p.metricas[c]))
  const basicas = ['vistas', 'pct_no_seguidores', 'guardados', 'compartidos', 'seguidores_nuevos']
  const faltanBasicas = posts.filter((p) => !basicas.every((c) => esNum(p.metricas[c]))).map((p) => p.n)
  const avanzadas = DATOS_AVANZADOS.map((d) => {
    const con = posts.filter((p) => tiene(p, d.columnas)).map((p) => p.n)
    const faltan = posts.filter((p) => !tiene(p, d.columnas)).map((p) => p.n)
    return { ...d, con: con.length, total: posts.length, faltan, estado: faltan.length === 0 ? 'completo' : con.length ? 'parcial' : 'sin-dato' }
  })
  return {
    basicas: { con: posts.length - faltanBasicas.length, total: posts.length, faltan: faltanBasicas },
    avanzadas,
    completa: faltanBasicas.length === 0 && avanzadas.every((a) => a.estado === 'completo'),
  }
}

// Qué capturar primero: el mínimo de cada ventana; en la línea base, primero ORO y CHATARRA (son los que enseñan).
function prioridadCapturas(cd, ventanas, porN) {
  cd.avanzadas.forEach((a) => {
    if (a.estado === 'completo') { a.prioridad = []; return }
    const falta = new Set(a.faltan)
    const tomar = (ns, orden) => {
      const tienen = ns.length - ns.filter((n) => falta.has(n)).length
      const hacen = Math.max(0, minimoPorVentana(ns.length) - tienen)
      return ns.filter((n) => falta.has(n)).sort(orden).slice(0, hacen)
    }
    const peso = (n) => (['ORO', 'CHATARRA'].includes(porN.get(n)?.zona) ? 0 : 1)
    a.prioridad = [...tomar(ventanas.mes.posts, (x, y) => x - y), ...tomar(ventanas.base.posts, (x, y) => peso(x) - peso(y) || x - y)]
  })
}

function diasEntre(a, b) {
  return Math.round(Math.abs(new Date(b) - new Date(a)) / 86400000) + 1
}

// Reparte N piezas respetando porcentajes (resto mayor), sin perder ni sumar piezas.
export function repartirPiezas(total, pct) {
  const claves = Object.keys(pct)
  const exactos = claves.map((k) => ({ k, x: (total * pct[k]) / 100 }))
  const base = Object.fromEntries(exactos.map(({ k, x }) => [k, Math.floor(x)]))
  let faltan = total - Object.values(base).reduce((a, b) => a + b, 0)
  exactos
    .map(({ k, x }) => ({ k, resto: x - Math.floor(x) }))
    .sort((a, b) => b.resto - a.resto)
    .forEach(({ k }) => { if (faltan > 0 && pct[k] > 0) { base[k]++; faltan-- } })
  return base
}

// ── núcleo ────────────────────────────────────────────────────────
export function analizar(datos) {
  const posts = [...(datos.posts || [])]
    .map((p) => {
      const m = { ...(p.metricas || {}) }
      return { ...p, metricas: { ...m, ...derivar(m) } }
    })
    .sort((a, b) => (a.fecha < b.fecha ? 1 : a.fecha > b.fecha ? -1 : a.n - b.n)) // más nuevo primero

  const fechas = posts.map((p) => p.fecha).filter(Boolean).sort()
  const diasPublicando = datos.ventana?.dias_publicando ?? (fechas.length ? diasEntre(fechas[0], fechas[fechas.length - 1]) : 0)
  const lote = {
    n: posts.length,
    dias: diasPublicando,
    valido: posts.length >= LOTE_MINIMO && diasPublicando >= DIAS_MINIMOS,
  }
  lote.motivo = lote.valido
    ? `${lote.n} posts en ${lote.dias} días: hay lote.`
    : posts.length < LOTE_MINIMO
      ? `Solo ${posts.length} posts. Con menos de ${LOTE_MINIMO} esto todavía es anécdota, no data.`
      : `Solo ${diasPublicando} días publicando. Hacen falta ${DIAS_MINIMOS}.`

  const salida = { lote, posts, generado: new Date().toISOString().slice(0, 10) }
  salida.calidadDatos = calidadDatos(posts)
  if (!lote.valido) return salida

  // Ventanas: explícitas, o primer mes partido 20/10 (proporción 2/3 – 1/3 si no son 30).
  let base, mes, modo
  if (datos.ventanas?.base?.length && datos.ventanas?.mes?.length) {
    const porN = new Map(posts.map((p) => [p.n, p]))
    base = datos.ventanas.base.map((n) => porN.get(n)).filter(Boolean)
    mes = datos.ventanas.mes.map((n) => porN.get(n)).filter(Boolean)
    modo = 'explicito'
  } else {
    const nMes = posts.length === 30 ? 10 : Math.round(posts.length / 3)
    mes = posts.slice(0, nMes)
    base = posts.slice(nMes)
    modo = 'partido'
  }
  const rango = (arr) => {
    const f = arr.map((p) => p.fecha).sort()
    return { desde: f[0], hasta: f[f.length - 1], n: arr.length, posts: arr.map((p) => p.n) }
  }
  salida.ventanas = { modo, base: rango(base), mes: rango(mes) }

  // ── Los 5 filtros ──
  const col = (arr, k) => arr.map((p) => p.metricas[k])
  const comp = (et, k, dec, unidad = '') => {
    // Con 1 o 2 capturas sueltas no hay mediana que valga: cada ventana necesita su mínimo.
    const alcanza = (arr) => col(arr, k).filter(esNum).length >= minimoPorVentana(arr.length)
    if (!alcanza(base) || !alcanza(mes)) return null
    const b = mediana(col(base, k)), mm = mediana(col(mes, k))
    if (b === null || mm === null) return null
    return { et, columna: k, base: redondear(b, dec), mes: redondear(mm, dec), unidad, ok: mm >= b }
  }
  const comps = {
    1: [comp('vistas', 'vistas', 1), comp('% de no seguidores', 'pct_no_seguidores', 2, ' %')],
    2: [comp('retención a 3 s', 'retencion_3s', 1, ' %'), comp('duración media', 'duracion_media', 1, ' s')],
    3: [comp('valor por 1.000 vistas', 'valor_1000', 1)],
    4: [comp('tasa de conversión', 'tasa_conv', 2, ' %')],
    5: [comp('visitas + enlace + DMs', 'intencion', 1)],
  }
  let tapado = 0
  salida.filtros = FILTROS.map((f) => {
    const cs = comps[f.n].filter(Boolean)
    let estado
    if (tapado > 0) estado = 'no-se-lee'
    else if (cs.length === 0) estado = 'sin-dato'
    else if (cs.some((c) => !c.ok)) { estado = 'tapado'; tapado = f.n }
    else estado = 'pasa'
    return { ...f, comps: cs, estado }
  })
  salida.tapado = tapado
  salida.tapadoInfo = tapado ? FILTROS[tapado - 1] : null

  // Referencia de la clase: mediana vs promedio de vistas (la mentira del promedio).
  const vistas = col(posts, 'vistas')
  const medV = mediana(vistas), promV = promedio(vistas)
  salida.medianaVsPromedio = {
    mediana: redondear(medV, 1),
    promedio: redondear(promV, 1),
    veces: redondear(promV / medV, 1),
    bajoPromedio: vistas.filter((v) => esNum(v) && v < promV).length,
  }

  // ── Orden por la columna del filtro tapado ──
  // Criterio de la casa: sin filtro tapado, se ordena por Valor (siempre medible en el panel).
  const filtroOrden = tapado || 3
  const columnaOrden = FILTROS[filtroOrden - 1].columna
  salida.orden = {
    filtro: filtroOrden,
    columna: columnaOrden,
    etiqueta: FILTROS[filtroOrden - 1].columnaEtiqueta,
    porDefecto: tapado === 0,
  }

  const conValor = posts.filter((p) => esNum(p.metricas[columnaOrden]))
  const porFiltro = [...conValor].sort((a, b) => b.metricas[columnaOrden] - a.metricas[columnaOrden] || a.n - b.n)
  const porVistas = [...posts].filter((p) => esNum(p.metricas.vistas)).sort((a, b) => b.metricas.vistas - a.metricas.vistas || a.n - b.n)
  const cuarto = Math.floor(porFiltro.length * 0.25)
  const zona = new Map()
  porFiltro.forEach((p, i) => zona.set(p.n, i < cuarto ? 'ORO' : i >= porFiltro.length - cuarto ? 'CHATARRA' : 'TIBIO'))
  salida.cuarto = cuarto
  salida.ranking = porFiltro.map((p, i) => ({
    n: p.n,
    posFiltro: i + 1,
    posVistas: porVistas.findIndex((q) => q.n === p.n) + 1,
    valor: p.metricas[columnaOrden],
    vistas: p.metricas.vistas,
    zona: zona.get(p.n),
  }))
  posts.forEach((p) => { p.zona = zona.get(p.n) || 'SIN DATO' })

  // Los que las vistas coronarían y el filtro manda al fondo (y al revés).
  const topVistas = porVistas.slice(0, cuarto).map((p) => p.n)
  salida.engañoVistas = {
    topVistasEnChatarra: topVistas.filter((n) => zona.get(n) === 'CHATARRA'),
    topVistasEnOro: topVistas.filter((n) => zona.get(n) === 'ORO'),
    topVistas,
  }

  // ── Veredicto por formato ──
  const grupos = (clave, filas) => {
    const g = new Map()
    filas.forEach((p) => {
      const k = p.etiquetas?.[clave]?.trim()
      if (!k) return
      if (!g.has(k)) g.set(k, [])
      g.get(k).push(p)
    })
    return g
  }
  salida.formatos = [...grupos('formato', posts)].map(([formato, ps]) => {
    const oro = ps.filter((p) => p.zona === 'ORO').length
    const chatarra = ps.filter((p) => p.zona === 'CHATARRA').length
    let veredicto
    if (oro >= 2 && chatarra >= 2) veredicto = 'EN DISPUTA'
    else if (oro >= 2) veredicto = 'REPETIR'
    else if (chatarra >= 2) veredicto = 'MATAR'
    else if (oro === 1) veredicto = 'CONFIRMAR'
    else veredicto = 'SIN VEREDICTO'
    return { formato, veces: ps.length, oro, chatarra, veredicto, posts: ps.map((p) => p.n) }
  }).sort((a, b) => b.oro - a.oro || a.chatarra - b.chatarra || b.veces - a.veces)

  // ── Coronación de ángulos, por propósito y con SU columna ──
  const porProp = grupos('proposito', posts)
  salida.angulos = PROPOSITOS.map((prop) => {
    const regla = CORONA_ANGULO[prop]
    const filas = porProp.get(prop) || []
    if (!regla) return { proposito: prop, estado: 'no-se-corona', motivo: 'Experimentación sirve para descubrir a quién le hablas, no para ganar.', filas: filas.length, coronados: [] }
    const medibles = filas.filter((p) => esNum(p.metricas[regla.columna]))
    const c = Math.floor(medibles.length * 0.25)
    if (filas.length === 0) return { proposito: prop, ...regla, estado: 'vacio', motivo: 'Ningún post con este propósito en el lote.', filas: 0, coronados: [] }
    if (medibles.length === 0) return { proposito: prop, ...regla, estado: 'sin-dato', motivo: `Falta el dato del filtro ${regla.filtro}: este mes no se puede coronar un ángulo de ${prop.toLowerCase()}.`, filas: filas.length, coronados: [] }
    if (c < 1) return { proposito: prop, ...regla, estado: 'pocas-filas', motivo: `Solo ${medibles.length} post${medibles.length === 1 ? '' : 's'} medible${medibles.length === 1 ? '' : 's'}: no alcanza para partir en cuartos.`, filas: filas.length, coronados: [] }
    const arriba = [...medibles].sort((a, b) => b.metricas[regla.columna] - a.metricas[regla.columna] || a.n - b.n).slice(0, c)
    const cuenta = new Map()
    arriba.forEach((p) => { const a = p.etiquetas?.angulo?.trim(); if (a) cuenta.set(a, (cuenta.get(a) || 0) + 1) })
    const coronados = [...cuenta].filter(([, v]) => v >= 2).map(([angulo, veces]) => ({ angulo, veces }))
    const candidatos = [...cuenta].filter(([, v]) => v === 1).map(([angulo]) => angulo)
    return {
      proposito: prop, ...regla, filas: filas.length, arriba: arriba.map((p) => p.n), coronados, candidatos,
      estado: coronados.length ? 'coronado' : 'sin-corona',
      motivo: coronados.length ? '' : 'Ningún ángulo apareció 2 veces arriba: una vez es suerte.',
    }
  })

  prioridadCapturas(salida.calidadDatos, salida.ventanas, new Map(posts.map((p) => [p.n, p])))

  // Medianas del lote entero: la meta de cada pieza del calendario.
  salida.medianas = Object.fromEntries(['vistas', 'pct_no_seguidores', 'retencion_3s', 'valor_1000', 'tasa_conv', 'intencion']
    .map((k) => [k, redondear(mediana(col(posts, k)), 2)]))

  // ── Las 3 conclusiones fijas ──
  salida.conclusionesFijas = conclusionesFijas(posts, salida, columnaOrden)

  // ── Reparto ──
  const mz = MEZCLAS[tapado]
  const piezas = datos.piezas_mes || 12
  salida.reparto = { ...mz, piezas, cubetas: repartirPiezas(piezas, { rep: mz.rep, var_: mz.var_, apo: mz.apo }) }
  const prop = datos.proposito_mes
  salida.propositoMes = prop || null
  salida.angulosQuePesan = prop ? ANGULOS_QUE_PESAN[prop] : null

  // La encuesta no sirve si el filtro tapado es 1 o 2 (quien responde ya te sigue).
  salida.encuesta = [1, 2].includes(tapado)
    ? { sirve: false, motivo: `Tu filtro tapado es el ${tapado}. Quien responde una encuesta ya te sigue: preguntarle cómo llegar a quien no te conoce es preguntarle al lugar equivocado. Este mes, sáltala.` }
    : { sirve: true, motivo: 'La encuesta desempata, no decide: la data elige el MOLDE, la encuesta elige el TEMA.' }

  return salida
}

// ── Las 3 conclusiones fijas ─────────────────────────────────────
// Salen en TODOS los informes, con reglas fijas:
//   1. Formato ganador   = veredicto REPETIR (si no hay, el mejor CONFIRMAR, marcado como candidato).
//   2. Ángulo que viraliza = mediana de % de no seguidores por ángulo (salir de tu casa).
//   3. Ángulo de venta   = el coronado de Venta; si no, mediana de intención; si tampoco hay, de conversión (posible).
// Un ángulo necesita 2+ Reels para competir (una vez es suerte) y ganarle a la mediana de la cuenta.
export const MIN_REELS_ANGULO = 2

export function rankingAngulos(posts, columna) {
  const medibles = posts.filter((p) => esNum(p.metricas[columna]))
  const desc = (a, b) => b.metricas[columna] - a.metricas[columna] || a.n - b.n
  const cuarto = Math.floor(medibles.length * 0.25)
  const arriba = new Set([...medibles].sort(desc).slice(0, cuarto).map((p) => p.n))
  const g = new Map()
  medibles.forEach((p) => {
    const a = p.etiquetas?.angulo?.trim()
    if (!a) return
    if (!g.has(a)) g.set(a, [])
    g.get(a).push(p)
  })
  const filas = [...g]
    .filter(([, ps]) => ps.length >= MIN_REELS_ANGULO)
    .map(([angulo, ps]) => ({
      angulo,
      veces: ps.length,
      mediana: redondear(mediana(ps.map((p) => p.metricas[columna])), 2),
      medianaVistas: redondear(mediana(ps.map((p) => p.metricas.vistas)), 0),
      arriba: ps.filter((p) => arriba.has(p.n)).length,
      posts: [...ps].sort(desc).map((p) => p.n),
    }))
    .sort((a, b) => b.mediana - a.mediana || b.arriba - a.arriba || b.veces - a.veces || a.angulo.localeCompare(b.angulo))
  return { columna, filas, medianaCuenta: redondear(mediana(medibles.map((p) => p.metricas[columna])), 2) }
}

function elegirAngulo(rk, extra) {
  const [g, segundo] = rk.filas
  if (!g) return { estado: 'sin-dato', columna: rk.columna, motivo: `Ningún ángulo tiene ${MIN_REELS_ANGULO} Reels con este dato: una vez es suerte.`, tabla: [], ...extra }
  if (!(g.mediana > rk.medianaCuenta)) return { estado: 'sin-ganador', columna: rk.columna, medianaCuenta: rk.medianaCuenta, motivo: 'Ningún ángulo le gana a la mediana de tu cuenta: todavía no hay uno que haga la diferencia.', tabla: rk.filas.slice(0, 5), ...extra }
  return {
    estado: 'ganador', columna: rk.columna, medianaCuenta: rk.medianaCuenta,
    angulo: g.angulo, veces: g.veces, mediana: g.mediana, medianaVistas: g.medianaVistas, arriba: g.arriba,
    fuerza: g.arriba >= 2 ? 'patron' : 'pista',
    referencias: g.posts.slice(0, 3),
    segundo: segundo ? { angulo: segundo.angulo, mediana: segundo.mediana, veces: segundo.veces } : null,
    tabla: rk.filas.slice(0, 5),
    ...extra,
  }
}

function conclusionesFijas(posts, salida, columnaOrden) {
  const valorDe = (n) => posts.find((p) => p.n === n)?.metricas[columnaOrden] ?? -Infinity
  const conDatos = (f) => {
    const ps = posts.filter((p) => f.posts.includes(p.n))
    return {
      formato: f.formato, veredicto: f.veredicto, veces: f.veces, oro: f.oro, chatarra: f.chatarra, posts: f.posts,
      referencias: ps.filter((p) => p.zona === 'ORO').sort((a, b) => valorDe(b.n) - valorDe(a.n)).map((p) => p.n),
      mediana: redondear(mediana(ps.map((p) => p.metricas[columnaOrden])), 2),
      medianaVistas: redondear(mediana(ps.map((p) => p.metricas.vistas)), 0),
    }
  }

  // 1 · Formato ganador
  const repetir = salida.formatos.filter((f) => f.veredicto === 'REPETIR')
  const confirmar = salida.formatos.filter((f) => f.veredicto === 'CONFIRMAR')
    .sort((a, b) => a.chatarra - b.chatarra || Math.max(...b.posts.map(valorDe)) - Math.max(...a.posts.map(valorDe)))
  const formato = repetir.length
    ? { estado: 'repetir', ganadores: repetir.map(conDatos) }
    : confirmar.length
      ? { estado: 'candidato', ganadores: [conDatos(confirmar[0])], motivo: 'Ningún formato fue 2 veces a ORO. Este es el mejor candidato: fue 1 vez y hay que confirmarlo.' }
      : { estado: 'sin-ganador', ganadores: [], motivo: 'Ningún formato llegó a ORO: etiqueta con más cuidado o sigue publicando.' }
  formato.columna = columnaOrden
  formato.matar = salida.formatos.filter((f) => f.veredicto === 'MATAR').map((f) => f.formato)

  // 2 · Ángulo que más te ayuda a viralizar = el que más sale de tu casa
  const anguloViral = elegirAngulo(rankingAngulos(posts, 'pct_no_seguidores'), { fuente: 'Filtro 1 · % de vistas de no seguidores' })

  // 3 · Posible mejor ángulo de venta
  const ventaCoronada = salida.angulos.find((a) => a.proposito === 'Venta' && a.estado === 'coronado')
  let anguloVenta
  if (ventaCoronada) {
    const rk = rankingAngulos(posts.filter((p) => p.etiquetas?.proposito === 'Venta'), 'intencion')
    const fila = rk.filas.find((f) => f.angulo === ventaCoronada.coronados[0].angulo)
    anguloVenta = {
      estado: 'ganador', seguridad: 'coronado', columna: 'intencion', fuente: 'Filtro 5 · Intención, coronado en tus piezas de Venta',
      angulo: ventaCoronada.coronados[0].angulo, veces: fila?.veces ?? ventaCoronada.coronados[0].veces,
      mediana: fila?.mediana ?? null, medianaVistas: fila?.medianaVistas ?? null, medianaCuenta: rk.medianaCuenta,
      arriba: ventaCoronada.coronados[0].veces, fuerza: 'patron',
      referencias: fila ? fila.posts.slice(0, 3) : ventaCoronada.arriba, tabla: rk.filas.slice(0, 5), segundo: null,
    }
  } else {
    const rkInt = rankingAngulos(posts, 'intencion')
    anguloVenta = rkInt.filas.length
      ? elegirAngulo(rkInt, { seguridad: 'medido', fuente: 'Filtro 5 · Intención (visitas + enlace + DMs)' })
      : elegirAngulo(rankingAngulos(posts, 'tasa_conv'), { seguridad: 'proxy', fuente: 'Filtro 4 · Conversión: no hay dato de intención' })
  }

  return { formato, anguloViral, anguloVenta }
}

// ── Validador de la parte que escribe la IA ──────────────────────
// Rechaza lo que contradiga al motor: posts inexistentes, formatos
// muertos en REPETIR, cubetas con otro número de piezas, etc.
export function validarLectura(resultado, lectura, opciones = {}) {
  const errores = []
  const ns = new Set(resultado.posts.map((p) => p.n))
  const porN = new Map(resultado.posts.map((p) => [p.n, p]))
  const usados = new Set(resultado.posts.map((p) => p.etiquetas?.formato?.trim()).filter(Boolean))
  const biblioteca = opciones.biblioteca ? new Set(opciones.biblioteca) : null
  const refs = (arr, donde) => (arr || []).forEach((n) => { if (!ns.has(n)) errores.push(`${donde}: el post ${n} no existe en el lote`) })

  ;(lectura.preguntas || []).forEach((q, i) => refs(q.evidencia, `pregunta ${i + 1}`))
  ;(lectura.conclusiones || []).forEach((c, i) => refs(c.evidencia, `conclusión ${i + 1}`))

  const cal = lectura.aplicacion?.calendario || []
  if (resultado.reparto && cal.length) {
    const cuenta = { REPETIR: 0, VARIAR: 0, APOSTAR: 0 }
    cal.forEach((f) => { if (f.de_donde_sale in cuenta) cuenta[f.de_donde_sale]++ })
    const esperado = resultado.reparto.cubetas
    if (cal.length !== resultado.reparto.piezas) errores.push(`calendario: ${cal.length} piezas, el reparto pide ${resultado.reparto.piezas}`)
    if (cuenta.REPETIR !== esperado.rep) errores.push(`calendario: ${cuenta.REPETIR} en REPETIR, el reparto pide ${esperado.rep}`)
    if (cuenta.VARIAR !== esperado.var_) errores.push(`calendario: ${cuenta.VARIAR} en VARIAR, el reparto pide ${esperado.var_}`)
    if (cuenta.APOSTAR !== esperado.apo) errores.push(`calendario: ${cuenta.APOSTAR} en APOSTAR, el reparto pide ${esperado.apo}`)
    const muertos = new Set(resultado.formatos.filter((f) => f.veredicto === 'MATAR').map((f) => f.formato))
    const ganadores = new Set(resultado.formatos.filter((f) => f.veredicto === 'REPETIR').map((f) => f.formato))
    cal.forEach((f, i) => {
      if (muertos.has(f.formato)) errores.push(`calendario fila ${i + 1}: «${f.formato}» tiene veredicto MATAR`)
      if (f.de_donde_sale === 'REPETIR' && ganadores.size && !ganadores.has(f.formato)) errores.push(`calendario fila ${i + 1}: REPETIR con «${f.formato}», que no tiene veredicto REPETIR`)
      refs(f.evidencia, `calendario fila ${i + 1}`)

      // El detalle que hace grabable cada fila.
      const donde = `calendario fila ${i + 1}`
      const vacio = (x) => typeof x !== 'string' || !x.trim()
      if (vacio(f.angulo)) errores.push(`${donde}: falta el ángulo`)
      if (vacio(f.angulo_exacto)) errores.push(`${donde}: falta angulo_exacto (la frase del ángulo aplicada a este tema)`)
      if (vacio(f.gancho)) errores.push(`${donde}: falta el gancho (la primera frase literal)`)
      if (!Array.isArray(f.estructura) || f.estructura.length < 3) errores.push(`${donde}: la estructura necesita 3 pasos o más`)
      if (vacio(f.cta)) errores.push(`${donde}: falta el CTA`)
      const ref = f.referencia
      if (!ref || (ref.post == null && vacio(ref.biblioteca))) {
        errores.push(`${donde}: falta la referencia (un Reel tuyo o, en APOSTAR, la ficha de la Biblioteca)`)
      } else {
        if (ref.post != null && !ns.has(ref.post)) errores.push(`${donde}: la referencia #${ref.post} no existe en el lote`)
        if (ref.post != null && vacio(ref.que_copiar)) errores.push(`${donde}: la referencia #${ref.post} no dice qué se copia de ella`)
        if (f.de_donde_sale === 'REPETIR' && ref.post != null && ns.has(ref.post) && porN.get(ref.post).etiquetas?.formato?.trim() !== f.formato) {
          errores.push(`${donde}: REPETIR copia el molde, pero la referencia #${ref.post} está hecha con otro formato`)
        }
      }
      if (f.de_donde_sale === 'APOSTAR') {
        if (usados.has(f.formato)) errores.push(`${donde}: APOSTAR con «${f.formato}», que ya usaste en el lote`)
        if (biblioteca && !biblioteca.has(f.formato)) errores.push(`${donde}: APOSTAR con «${f.formato}», que no está en la Biblioteca de formatos`)
      }
    })

    // Los ángulos de las conclusiones fijas tienen que estar en el calendario.
    const cf = resultado.conclusionesFijas
    const angulosCal = new Set(cal.map((f) => f.angulo?.trim()))
    if (cf?.anguloViral?.estado === 'ganador' && !angulosCal.has(cf.anguloViral.angulo)) {
      errores.push(`calendario: ninguna pieza usa tu ángulo que viraliza («${cf.anguloViral.angulo}»)`)
    }
    if (cf?.anguloVenta?.estado === 'ganador' && !angulosCal.has(cf.anguloVenta.angulo)) {
      errores.push(`calendario: ninguna pieza usa tu posible ángulo de venta («${cf.anguloVenta.angulo}»)`)
    }
  }

  // Si falta data avanzada, conseguirla es una acción de la semana, no una nota al pie.
  const incompletas = (resultado.calidadDatos?.avanzadas || []).filter((a) => a.estado !== 'completo')
  if (resultado.reparto && incompletas.length) {
    const es = lectura.aplicacion?.esta_semana || []
    if (!es.some((x) => /captur/i.test(x))) {
      errores.push(`esta_semana: falta la acción de capturar ${incompletas.map((a) => a.nombre).join(' y ')} (sin eso, los filtros ${incompletas.map((a) => a.filtro).join(' y ')} siguen sin dato)`)
    }
  }

  // Las 3 conclusiones fijas: el motor elige, la IA solo explica el porqué.
  const cfL = lectura.conclusiones_fijas
  const cfR = resultado.conclusionesFijas
  if (cfR && resultado.reparto) {
    if (!cfL) errores.push('conclusiones_fijas: falta el porqué de las 3 (formato, angulo_viral, angulo_venta)')
    else {
      ;['formato', 'angulo_viral', 'angulo_venta'].forEach((k) => {
        if (!cfL[k] || typeof cfL[k].texto !== 'string' || !cfL[k].texto.trim()) errores.push(`conclusiones_fijas.${k}: falta el texto`)
        else refs(cfL[k].evidencia, `conclusiones_fijas.${k}`)
      })
      // El ángulo no se entrega como categoría suelta: se aterriza al tema de SUS Reels.
      const sinTildes = (t) => String(t || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
      ;[['angulo_viral', cfR.anguloViral], ['angulo_venta', cfR.anguloVenta]].forEach(([k, a]) => {
        if (a?.estado !== 'ganador' || !cfL[k]) return
        const esp = cfL[k].angulo_especifico
        const raiz = sinTildes(a.angulo).split(/[\s/]+/)[0]
        if (typeof esp !== 'string' || !esp.trim()) errores.push(`conclusiones_fijas.${k}: falta angulo_especifico («${a.angulo} de …», aterrizado al tema de sus Reels)`)
        else if (!sinTildes(esp).includes(raiz)) errores.push(`conclusiones_fijas.${k}: angulo_especifico tiene que partir de «${a.angulo}», que es el que eligió el motor`)
        else if (sinTildes(esp).trim().length < sinTildes(a.angulo).length + 12) errores.push(`conclusiones_fijas.${k}: angulo_especifico repite la categoría; di de QUÉ tema («${a.angulo} de cómo…»)`)
        else if (esp.length > 110) errores.push(`conclusiones_fijas.${k}: angulo_especifico pasa de 110 caracteres; tiene que caber como titular`)
      })
    }
  }
  if (lectura.aplicacion?.campana && !resultado.angulos?.find((a) => a.proposito === 'Venta' && a.estado === 'coronado')) {
    errores.push('campaña: no hay ángulo de Venta coronado; una campaña sin ángulo probado es un anuncio con prisa')
  }
  return errores
}
