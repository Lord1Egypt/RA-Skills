// ============================================================================
// PERSONAJE de animacion-dibujada-f100k — un personaje a partir de una FICHA (JSON), en 3 estilos.
// Se carga DESPUÉS de nucleo.js (usa clamp, lerp, ease, prog, hash2).
// ANATOMIA: estilizada — chibi de caricatura: brazos de tubo con mitón redondo, sin dedos ni nariz; la cara son puntos.
//
//   const p = crearPersonaje(ficha, { estilo: 'pixel' | 'vector' | 'papel', alto: 520 });
//   p.ancho, p.alto                                      // tamaño real en px (pixel redondea al tamaño de pixel)
//   p.zancada, p.ciclo, p.velocidad                      // px por ciclo de 2 pasos, segundos por ciclo, px/s al caminar
//   p.dibujar(ctx, x, y, { accion, t, mira = 1, escala = 1, expresion, velocidad, desdePerfil, vista, n });
//      (x, y) = el punto entre los PIES. t = segundos desde que empezó la acción (función pura de t).
//      accion: 'quieto' | 'caminar' | 'saludar' | 'señalar' | 'saltar' | 'hablar' | 'festejar' | 'pensar' | 'presentar' | 'contar'
//      mira = -1 lo voltea (mira a la izquierda).
//      expresion: 'feliz' | 'sorpresa' | 'duda' | 'triste' | 'guiño' (cejas + ojos + boca; sirve con cualquier acción)
//      velocidad: px/s a los que la escena lo mueve mientras camina. Con eso el paso se ajusta y los pies NO patinan.
//                 Sin velocidad camina a p.velocidad: mueve al personaje a esa velocidad.
//      desdePerfil: true en la acción que sigue a un «caminar» (gira de perfil a frente en 3 cuadros).
//      vista: 0 (frente) … 1 (perfil) para forzar la vista en cualquier acción.   n: hasta cuánto cuenta «contar» (1-5).
//
// La ficha la escribe Claude MIRANDO la foto o el dibujo de la persona. El código no adivina rasgos.
// Unidades internas: el personaje mide 100 (pies en y = 0, coronilla en y = -100); x = 0 al centro.
// ============================================================================

const ACCIONES_PERSONAJE = ['quieto', 'caminar', 'saludar', 'señalar', 'saltar', 'hablar', 'festejar', 'pensar', 'presentar', 'contar'];
const EXPRESIONES_PERSONAJE = ['normal', 'feliz', 'sorpresa', 'duda', 'triste', 'guiño'];
const ACCESORIOS_PERSONAJE = ['collar', 'lentes', 'aretes', 'gorro-chef', 'delantal', 'estetoscopio', 'gorra'];
const PASO = { zancada: 38, ciclo: .68, alzada: 6.5 };   // unidades por ciclo de 2 pasos, segundos por ciclo, altura del pie

function crearPersonaje(ficha, opciones = {}) {
  const estilo = opciones.estilo || 'vector';
  if (!['pixel', 'vector', 'papel'].includes(estilo)) console.warn(`[personaje] estilo «${estilo}» no existe: uso vector`);
  const F = normalizarFicha(ficha);
  const altoPedido = opciones.alto || 520;

  // ---------- pixel: se dibuja en una grilla chica y se agranda ----------
  const PIX = .44;                                     // pixeles de grilla por unidad (100 u ≈ 44 px de alto)
  const tamPixel = Math.max(2, Math.round(altoPedido / (100 * PIX)));
  const k = estilo === 'pixel' ? tamPixel * PIX : altoPedido / 100;   // px de pantalla por unidad

  const p = {
    ficha: F, estilo,
    ancho: Math.round(84 * k), alto: Math.round(100 * k), tamPixel: estilo === 'pixel' ? tamPixel : 0,
    zancada: PASO.zancada * k, ciclo: PASO.ciclo, velocidad: PASO.zancada * k / PASO.ciclo,
    dibujar(g, x, y, o = {}) {
      const accion = ACCIONES_PERSONAJE.includes(o.accion) ? o.accion : 'quieto';
      if (o.accion && !ACCIONES_PERSONAJE.includes(o.accion) && !avisado[o.accion]) { avisado[o.accion] = 1; console.warn(`[personaje] acción «${o.accion}» no existe: uso quieto`); }
      const mira = o.mira === -1 ? -1 : 1, escala = o.escala || 1;
      const t0 = Math.max(0, o.t || 0); let t = t0;
      if (estilo === 'papel') t = Math.floor(t * 12) / 12;         // recorte animado a 12 cuadros por segundo
      if (estilo === 'pixel') t = Math.floor(t * 10) / 10;         // sprite a 10 cuadros por segundo
      // stop-motion de verdad: si camina a velocidad conocida, también el AVANCE va a saltos (si no, el pie apoyado resbala)
      if (accion === 'caminar' && o.velocidad && t !== t0) x -= mira * Math.abs(o.velocidad) * (t0 - t);
      const expresion = o.expresion && o.expresion !== 'normal' ? o.expresion : null;
      if (expresion && !EXPRESIONES_PERSONAJE.includes(expresion) && !avisado['e' + expresion]) { avisado['e' + expresion] = 1; console.warn(`[personaje] expresión «${expresion}» no existe (hay: ${EXPRESIONES_PERSONAJE.join(', ')})`); }
      const P = pose(F, accion, t, { velU: o.velocidad ? Math.abs(o.velocidad) / (k * escala) : 0, n: o.n, expresion,
        desdePerfil: !!o.desdePerfil, vista: o.vista });
      if (estilo === 'pixel') return dibujarPixel(g, x, y, P, mira, escala);
      g.save(); g.translate(x, y); g.scale(mira * k * escala, k * escala);
      cuerpo(g, F, P, estilo === 'papel' ? 'papel' : 'vector', t);
      g.restore();
    },
  };
  const avisado = {};

  // sprite pixel: dibuja con formas en la grilla, cuantiza a la paleta, contorno de 1 px, cara a mano
  const GW = Math.ceil(110 * PIX), GH = Math.ceil(182 * PIX);        // lienzo de grilla (margen para saltos, gorros y brazos abiertos)
  const OX = Math.floor(GW / 2), OY = Math.round(164 * PIX);         // dónde caen los pies en la grilla
  const lienzo = document.createElement('canvas'); lienzo.width = GW; lienzo.height = GH;
  const lg = lienzo.getContext('2d', { willReadFrequently: true });
  const final = document.createElement('canvas'); final.width = GW; final.height = GH;
  const fg = final.getContext('2d');
  function dibujarPixel(g, x, y, P, mira, escala) {
    lg.setTransform(1, 0, 0, 1, 0, 0); lg.clearRect(0, 0, GW, GH);
    PALETA.clear();
    lg.save(); lg.translate(OX, OY); lg.scale(PIX, PIX);
    cuerpo(lg, F, P, 'pixel', 0);
    lg.restore();
    cuantizar(lg, GW, GH, F);
    caraPixel(lg, F, P);
    fg.clearRect(0, 0, GW, GH); fg.drawImage(lienzo, 0, 0);
    const s = tamPixel * escala;
    g.save(); g.imageSmoothingEnabled = false;
    const px = Math.round(x / tamPixel) * tamPixel, py = Math.round(y / tamPixel) * tamPixel;
    g.translate(px, py); g.scale(mira, 1);
    g.drawImage(final, -OX * s, -OY * s, GW * s, GH * s);
    g.restore();
  }
  return p;
}

// ---------------------------------------------------------------------------
// FICHA
// ---------------------------------------------------------------------------
function normalizarFicha(f) {
  f = JSON.parse(JSON.stringify(f || {}));
  const d = (v, x) => (v === undefined || v === null || v === '' ? x : v);
  f.tipo = d(f.tipo, 'humano');
  f.pelo = Object.assign({ color: '#4a2c20', largo: 'medio', estilo: 'raya-al-medio' }, f.pelo || {});
  f.piel = d(f.piel, '#e0ac88');
  f.ojos = d(f.ojos, '#2b1a14');
  f.labios = d(f.labios, mezclar(f.piel, '#b0454a', .45));
  f.ropa = Object.assign({ arriba: '#7b5cd6', tipo_arriba: 'playera', abajo: '#3b3f58', tipo_abajo: 'pantalon', zapatos: '#2a2430' }, f.ropa || {});
  f.accesorios = (f.accesorios || []).filter(a => {
    if (ACCESORIOS_PERSONAJE.includes(a)) return true;
    console.warn(`[personaje] accesorio «${a}» no existe: se ignora (hay: ${ACCESORIOS_PERSONAJE.join(', ')})`); return false;
  });
  f.criatura = Object.assign({ forma: 'gato', color: '#f2a65a', panza: null }, f.criatura || {});
  f.criatura.panza = f.criatura.panza || mezclar(f.criatura.color, '#ffffff', .55);
  f.contorno = d(f.contorno, '#221a26');
  return f;
}

// ---------------------------------------------------------------------------
// COLOR
// ---------------------------------------------------------------------------
function rgbDe(c) {
  if (Array.isArray(c)) return c;
  let h = String(c).trim().replace('#', '');
  if (h.length === 3) h = h.split('').map(x => x + x).join('');
  const n = parseInt(h.slice(0, 6), 16);
  return isNaN(n) ? [128, 128, 128] : [n >> 16 & 255, n >> 8 & 255, n & 255];
}
const hexDe = c => '#' + c.map(v => Math.round(clamp(v, 0, 255)).toString(16).padStart(2, '0')).join('');
const tono = (c, f) => hexDe(rgbDe(c).map(v => f < 1 ? v * f : v + (255 - v) * (f - 1)));   // f < 1 oscurece, f > 1 aclara
const mezclar = (a, b, k) => { const A = rgbDe(a), B = rgbDe(b); return hexDe(A.map((v, i) => v + (B[i] - v) * k)); };
const PALETA = new Set();                               // colores que usó el sprite pixel (para cuantizar)

// ---------------------------------------------------------------------------
// POSE: cada acción es una función pura de t
// ---------------------------------------------------------------------------
function parpadeo(t) {
  const n = Math.floor(t / 3.1), tt = t - n * 3.1, cuando = .9 + hash2(n, 17) * 1.6;
  return tt > cuando && tt < cuando + .13;
}
// un pie en el ciclo de caminar: apoyo (se queda en el piso mientras el cuerpo avanza) y vuelo (arco al frente)
function piePaso(ph) {
  const S = PASO.zancada; ph = ((ph % 1) + 1) % 1;
  if (ph < .5) return [S / 4 - ph / .5 * S / 2, 0];
  const u = (ph - .5) / .5, e = u < .5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2;
  return [-S / 4 + e * S / 2, -Math.sin(u * Math.PI) * PASO.alzada];
}
function pose(F, accion, t, o = {}) {
  const P = {
    y: 0, sx: 1, sy: 1, bob: 0, lean: 0, tilt: 0, vista: 0,
    manoD: [20, -26], manoI: [-20, -26],             // dónde están los mitones (unidades, relativo a los pies)
    piernaD: 0, piernaI: 0,                            // giro de cada pierna desde la cadera (de frente)
    pieD: null, pieI: null,                            // al caminar: dónde está cada pie (x, y) respecto de la cadera
    boca: 'sonrisa', ojos: parpadeo(t) ? 'cerrados' : 'abiertos', cejas: 'normal', puntos: 0, cola: Math.sin(t * 3) * .25,
    peloLag: 0, dedos: 0, numero: 0, numeroPop: 1, palma: false,
  };
  const entra = ease(prog(t, 0, .28));                 // las poses llegan suave desde el reposo
  const hacia = (base, meta, k) => [lerp(base[0], meta[0], k), lerp(base[1], meta[1], k)];
  const reposo = [20, -26], reposoI = [-20, -26];
  switch (accion) {
    case 'quieto':
      P.bob = Math.sin(t * 2.4) * .9;
      P.manoD = [20, -26 + Math.sin(t * 2.4) * .5]; P.manoI = [-20, -26 + Math.sin(t * 2.4) * .5];
      break;
    case 'caminar': {
      // fase por distancia recorrida: si la escena dice su velocidad, el paso calza con el avance y los pies no patinan
      const ph = o.velU > 0 ? t * o.velU / PASO.zancada : t / PASO.ciclo;
      P.pieD = piePaso(ph); P.pieI = piePaso(ph + .5);
      P.bob = 1.2 * Math.cos(ph * Math.PI * 4);           // abajo al apoyar, arriba al pasar
      P.vista = ease(prog(t, 0, .1));                    // gira de frente a perfil en 3 cuadros
      P.lean = .06 * P.vista;
      const sw = Math.cos(ph * Math.PI * 2);             // brazos en contrafase con las piernas
      // de frente los brazos cuelgan a los lados; de perfil se mecen adelante y atrás
      const v = Math.sin(P.vista * Math.PI / 2);
      P.manoD = [lerp(20, 3 - sw * 13, v), -27 + Math.abs(sw) * 2 * v]; P.manoI = [lerp(-20, 3 + sw * 13, v), -27 + Math.abs(sw) * 2 * v];
      P.peloLag = Math.sin(ph * Math.PI * 4 + .8) * 1.3;   // el pelo rebota un poquito después del cuerpo
      break;
    }
    case 'saludar': {
      const ola = Math.sin(t * 10) * 5;
      P.manoD = hacia(reposo, [26 + ola, -84], back(prog(t, 0, .32))); P.manoI = reposoI;
      P.lean = -.03 * entra; P.tilt = .06 * entra; P.boca = 'abierta';
      P.bob = Math.sin(t * 3) * .6;
      break;
    }
    case 'señalar':
      P.manoD = hacia(reposo, [39, -58], back(prog(t, 0, .26)));
      P.manoI = [-20, -27]; P.lean = .04 * entra; P.tilt = .07 * entra; P.boca = 'sonrisa';
      P.bob = Math.sin(t * 2.4) * .6;
      break;
    case 'saltar': {
      const c = (t % 1.2) / 1.2;                         // agacharse (anticipación), volar, caer, asentarse con rebote
      if (c < .2) { const q = Math.sin(c / .2 * Math.PI / 2);
        P.sy = 1 - .15 * q; P.sx = 1 + .09 * q; P.manoD = hacia(reposo, [12, -19], q); P.manoI = hacia(reposoI, [-12, -19], q); P.lean = .05 * q; P.peloLag = -1.5 * q; }
      else if (c < .72) { const q = (c - .2) / .52, v = Math.cos(q * Math.PI);
        P.y = -Math.sin(q * Math.PI) * 36; P.sy = 1 + .1 * Math.max(0, v); P.sx = 1 - .06 * Math.max(0, v);
        const brazos = back(prog(q, 0, .35));
        P.manoD = hacia([12, -19], [27, -82], brazos); P.manoI = hacia([-12, -19], [-27, -82], brazos);
        P.piernaD = -.2; P.piernaI = .2; P.boca = 'abierta'; P.peloLag = v * 4.5; }
      else if (c < .86) { const q = Math.sin((c - .72) / .14 * Math.PI);
        P.sy = 1 - .14 * q; P.sx = 1 + .09 * q; P.manoD = [21, -31]; P.manoI = [-21, -31]; P.peloLag = 3.5 * q; }
      else { const q = (c - .86) / .14; P.sy = 1 + .035 * Math.sin(q * Math.PI); P.sx = 1 - .02 * Math.sin(q * Math.PI); P.peloLag = -1.2 * Math.sin(q * Math.PI); }
      break;
    }
    case 'hablar': {
      const seq = ['sonrisa', 'media', 'abierta', 'media', 'cerrada', 'abierta', 'media', 'sonrisa'];
      const n = Math.floor(t * 9);
      P.boca = seq[Math.floor(hash2(n, 3) * seq.length)];
      if (Math.floor(t * 9) % 11 === 10) P.boca = 'cerrada';
      P.manoD = hacia(reposo, [25 + Math.sin(t * 3.3) * 3, -50 + Math.sin(t * 4.1) * 5], entra);
      P.manoI = [-20, -27 + Math.sin(t * 2.2) * 1.5];
      P.tilt = Math.sin(t * 2.6) * .05; P.bob = Math.sin(t * 5.2) * .7;
      break;
    }
    case 'festejar': {
      const pre = prog(t, 0, .16);                       // anticipación: se agacha antes de brincar
      if (t < .16) { const q = Math.sin(pre * Math.PI / 2); P.sy = 1 - .12 * q; P.sx = 1 + .07 * q; P.manoD = hacia(reposo, [14, -21], q); P.manoI = hacia(reposoI, [-14, -21], q); P.ojos = 'felices'; P.boca = 'sonrisa'; break; }
      const t2 = t - .16, s7 = Math.sin(t2 * 8), h = Math.abs(s7);
      P.y = -h * 11;
      const apl = h < .3 ? 1 - h / .3 : 0;               // aplasta cada vez que toca el piso
      P.sy = 1 - .08 * apl + .05 * (h > .5 ? 1 : 0); P.sx = 1 + .06 * apl;
      const k = back(prog(t2, 0, .3));
      P.manoD = hacia([14, -21], [25, -92 + Math.sin(t2 * 16) * 3], k); P.manoI = hacia([-14, -21], [-25, -92 - Math.sin(t2 * 16) * 3], k);
      P.ojos = 'felices'; P.boca = 'abierta'; P.piernaD = h * .14; P.piernaI = -h * .14;
      P.peloLag = -Math.cos(t2 * 8) * Math.sign(s7 || 1) * 3.2;
      break;
    }
    case 'pensar':
      P.manoD = hacia(reposo, [6, -61], entra); P.manoI = hacia(reposoI, [9, -44], entra);
      P.tilt = .1 * entra; P.ojos = P.ojos === 'cerrados' ? 'cerrados' : 'arriba'; P.boca = 'cerrada';
      P.puntos = prog(t, .35, 1.6); P.bob = Math.sin(t * 1.8) * .5;
      break;
    case 'presentar': {                                  // brazo abierto hacia un lado: «mira esto»
      const k = back(prog(t, 0, .4));
      P.manoD = hacia(reposo, [41, -41 + Math.sin(t * 2.2) * 1], k); P.manoI = [-20, -26];
      P.palma = true; P.lean = -.035 * k; P.tilt = .07 * k; P.boca = 'sonrisa';
      P.bob = Math.sin(t * 2.4) * .6;
      break;
    }
    case 'contar': {                                     // levanta el mitón y cuenta 1, 2, 3…
      const n = clamp(Math.round(o.n || 3), 1, 5), PASO_C = .62;
      const i = Math.min(n, Math.floor(t / PASO_C) + 1), tt = t - (i - 1) * PASO_C;
      const pop = i === n && t > n * PASO_C ? 1 : back(prog(tt, 0, .22));
      P.manoD = hacia(reposo, [23, -76 - (1 - pop) * 3], entra); P.manoI = [-20, -26];
      P.dedos = entra > .6 ? i : 0; P.numero = P.dedos; P.numeroPop = pop;
      P.boca = tt < .2 ? 'media' : 'sonrisa'; P.tilt = .05 * entra;
      P.bob = Math.sin(t * 2.4) * .6;
      break;
    }
  }
  // vista: forzada, o el giro de perfil a frente cuando la acción sigue a un «caminar»
  if (o.vista !== undefined && o.vista !== null && accion !== 'caminar') P.vista = clamp(o.vista);
  else if (o.desdePerfil && accion !== 'caminar') P.vista = 1 - ease(prog(t, 0, .1));
  // expresión: cejas + ojos + boca, encima de cualquier acción (al hablar, la boca sigue moviéndose)
  const x = o.expresion, parpa = P.ojos === 'cerrados', habla = accion === 'hablar';
  if (x === 'feliz') { if (!parpa) P.ojos = 'felices'; P.cejas = 'arriba'; if (!habla) P.boca = accion === 'festejar' ? 'abierta' : 'sonrisaGrande'; }
  else if (x === 'sorpresa') { if (!parpa) P.ojos = 'grandes'; P.cejas = 'muyArriba'; if (!habla) P.boca = 'o'; }
  else if (x === 'duda') { if (!parpa) P.ojos = 'lado'; P.cejas = 'duda'; if (!habla) P.boca = 'ladeada'; }
  else if (x === 'triste') { P.cejas = 'triste'; if (!habla) P.boca = 'triste'; P.ojos = parpa ? 'cerrados' : 'abajo'; }
  else if (x === 'guiño') { P.ojos = 'guiño'; P.cejas = 'arriba'; if (!habla) P.boca = 'sonrisaGrande'; }
  return P;
}

// ---------------------------------------------------------------------------
// DIBUJO: un solo cuerpo, tres maneras de pintarlo
//   vector: relleno + trazo del mismo color más oscuro + sombra plana
//   papel:  cada parte es un recorte con borde blanco, sombra y grano
//   pixel:  relleno sólido (se cuantiza y se contornea después)
// ---------------------------------------------------------------------------
let GRANO_PAPEL = null;
function granoPapel(g) {
  if (GRANO_PAPEL) return GRANO_PAPEL;
  const c = document.createElement('canvas'); c.width = c.height = 64; const x = c.getContext('2d'), r = rng(99);
  for (let i = 0; i < 900; i++) { x.fillStyle = r() < .5 ? 'rgba(0,0,0,.18)' : 'rgba(255,255,255,.22)'; x.fillRect(r() * 64, r() * 64, 1 + r(), 1 + r()); }
  GRANO_PAPEL = g.createPattern(c, 'repeat'); return GRANO_PAPEL;
}

function cuerpo(g, F, P, modo, t) {
  const E = {
    g, modo, F, t,
    trazo: modo === 'pixel' ? 2.5 : 1.7,
    parte(id, camino, color, o = {}) {                   // pinta una forma cerrada (o.recorte: la limita a otra forma)
      if (o.recorte) { g.save(); o.recorte(g); g.clip(); const r = this.parte(id, camino, color, Object.assign({}, o, { recorte: null })); g.restore(); return r; }
      const oscuro = o.linea || tono(color, .62);
      if (modo === 'papel') {
        const j = (hash2(Math.floor(t * 12), id) - .5) * .9, j2 = (hash2(id, Math.floor(t * 12)) - .5) * .9;
        g.save(); g.translate(j, j2);
        g.save(); g.translate(1.6, 2.2); camino(g); g.fillStyle = 'rgba(40,25,20,.28)'; g.fill(); g.restore();
        camino(g); g.lineJoin = 'round'; g.lineWidth = o.borde === 0 ? 0 : 3.6; g.strokeStyle = '#fffdf6'; if (o.borde !== 0) g.stroke();
        g.fillStyle = color; g.fill();
        g.save(); camino(g); g.clip(); const pat = granoPapel(g), m = g.getTransform();   // grano a escala de pantalla, no del personaje
        pat.setTransform(new DOMMatrix([1 / Math.hypot(m.a, m.b), 0, 0, 1 / Math.hypot(m.c, m.d), 0, 0])); g.fillStyle = pat; g.globalAlpha = .3; g.fillRect(-60, -140, 120, 160); g.restore();
        g.restore(); return;
      }
      camino(g); g.fillStyle = color; g.fill();
      if (modo === 'pixel') PALETA.add(color);
      if (o.sombra !== false && o.sombraX !== undefined) {            // sombra plana del lado derecho
        const sc = tono(color, .84); if (modo === 'pixel') PALETA.add(sc);
        g.save(); camino(g); g.clip(); g.fillStyle = sc; g.fillRect(o.sombraX, -140, 80, 170); g.restore();
      }
      if (o.linea !== false) { camino(g); g.lineJoin = 'round'; g.lineWidth = this.trazo; g.strokeStyle = oscuro; g.stroke(); if (modo === 'pixel') PALETA.add(oscuro); }
    },
    tubo(id, pts, ancho, color, o = {}) {                 // brazo, pierna o cola: una línea gruesa con puntas redondas
      const camino = () => { g.beginPath(); g.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) g.lineTo(pts[i][0], pts[i][1]); };
      g.lineCap = g.lineJoin = 'round';
      if (modo === 'papel') {
        const j = (hash2(Math.floor(t * 12), id) - .5) * .9;
        g.save(); g.translate(j, j * .6);
        g.save(); g.translate(1.6, 2.2); camino(); g.lineWidth = ancho + 3.6; g.strokeStyle = 'rgba(40,25,20,.28)'; g.stroke(); g.restore();
        camino(); g.lineWidth = ancho + 3.6; g.strokeStyle = '#fffdf6'; g.stroke();
        camino(); g.lineWidth = ancho; g.strokeStyle = color; g.stroke();
        g.restore(); return;
      }
      const oscuro = o.linea || tono(color, .62);
      if (o.linea !== false) { camino(); g.lineWidth = ancho + this.trazo * 2; g.strokeStyle = oscuro; g.stroke(); if (modo === 'pixel') PALETA.add(oscuro); }
      camino(); g.lineWidth = ancho; g.strokeStyle = color; g.stroke(); if (modo === 'pixel') PALETA.add(color);
    },
  };

  // sombra en el piso (no salta con el personaje: se achica)
  if (modo !== 'pixel') {
    const alto = clamp(-P.y / 34);
    g.save(); g.fillStyle = `rgba(20,10,30,${.16 - alto * .08})`; g.beginPath(); g.ellipse(0, 1, 24 - alto * 8, 4.2, 0, 0, Math.PI * 2); g.fill(); g.restore();
  }
  g.save();
  g.translate(0, P.y); g.scale(P.sx, P.sy);
  if (F.tipo === 'criatura') criatura(E, F, P); else humano(E, F, P);
  g.restore();
}

// ---------- brazos con cinemática inversa (2 huesos): el mitón va a donde lo manda la pose ----------
function ik(sx, sy, tx, ty, L1, L2, lado) {
  let dx = tx - sx, dy = ty - sy, d = Math.hypot(dx, dy); const max = L1 + L2 - .01;
  if (d > max) { dx *= max / d; dy *= max / d; d = max; }
  d = Math.max(d, .01);
  const a = Math.atan2(dy, dx), b = Math.acos(clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1, 1));
  const ang = a - lado * b;                              // lado = 1 brazo derecho (codo hacia afuera), -1 izquierdo
  return [[sx, sy], [sx + Math.cos(ang) * L1, sy + Math.sin(ang) * L1], [sx + dx, sy + dy]];
}

// giro de la cabeza: 0 de frente, ~1,4 rad de perfil (no llega a 90°: a los 81° el ojo lejano ya se oculta)
const giroCabeza = P => P.vista * Math.PI / 2 * .9;

function humano(E, F, P) {
  const { g } = E, R = F.ropa;
  const piel = F.piel;
  const sv = Math.sin(P.vista * Math.PI / 2), cv = Math.cos(P.vista * Math.PI / 2);
  const camina = !!P.pieD;
  const hb = camina ? P.bob : 0;                        // al caminar sube y baja toda la cadera; si no, solo el torso respira
  const hombroY = -55 + P.bob, cadera = -23 + hb;
  const cabeza = [0, -79 + P.bob];

  // --- pelo de atrás (detrás de todo): se va hacia la nuca al girar y rebota con retraso ---
  g.save(); g.translate(cabeza[0] - 6 * sv, cabeza[1] + P.peloLag); g.rotate(P.tilt + (camina ? P.lean * .5 : 0)); g.scale(1 - .34 * sv, 1);
  peloAtras(E, F, sv);
  g.restore();

  // --- piernas ---
  const colorPierna = R.tipo_abajo !== 'pantalon' ? piel : R.abajo;
  const zapato = (id, fx, fy, lado, lejos) => E.parte(id, gg => { gg.beginPath();
    gg.ellipse(fx + lado * 1.6 * cv + 2.8 * sv, fy - 1.3, 6.4 + 1.6 * sv, 3.8 - .4 * sv, 0, 0, Math.PI * 2); }, lejos ? tono(R.zapatos, .85) : R.zapatos, { sombraX: undefined });
  const piernaTubo = (id, pts, lado, lejos) => {
    const col = lejos ? tono(colorPierna, .88) : colorPierna;
    if (R.tipo_abajo === 'short') { E.tubo(id, pts, 8.4, lejos ? tono(piel, .88) : piel);
      E.tubo(id + 2, [pts[0], [lerp(pts[0][0], pts[1][0], .75), lerp(pts[0][1], pts[1][1], .75)]], 9.6, lejos ? tono(R.abajo, .88) : R.abajo); }
    else E.tubo(id, pts, 8.8, col);
  };
  if (camina) {                                          // perfil: cadera → rodilla (hacia adelante) → tobillo, con el pie plantado
    const pierna = (lado, pie, lejos) => {
      const hx = lado * 6.2 * cv, hy = cadera;
      const fx = pie[0] + hx * (1 - sv), fy = pie[1] - 2;
      const pts = ik(hx, hy, fx, fy, 11.2, 11.2, 1);
      piernaTubo(10 + lado, pts, lado, lejos);
      zapato(14 + lado, pts[2][0], pts[2][1] + 2, lado, lejos);
    };
    pierna(-1, P.pieI, true); pierna(1, P.pieD, false);
  } else {
    const pierna = (lado, giro) => {
      const hx = lado * 6.2 * cv, hy = cadera, L = 20;
      const px = hx + Math.sin(giro) * L, py = hy + Math.cos(giro) * L;
      piernaTubo(10 + lado, [[hx, hy], [px, py - 1.5]], lado, false);
      zapato(14 + lado, px, py, lado, false);
    };
    pierna(-1, P.piernaI); pierna(1, P.piernaD);
  }

  // --- brazos ---
  const Ls = 13.2, manga = R.tipo_arriba === 'playera' || R.tipo_arriba === 'vestido' ? 'corta' : 'larga';
  const brazo = (lado, mano, id, lejos) => {
    const sh = [lado * 13.2 * cv + 1.5 * sv, hombroY + 4.5];
    const [a, b, c] = ik(sh[0], sh[1], mano[0], mano[1] + P.bob * .6, Ls, Ls, sv > .5 ? -1 : lado);   // de perfil los dos codos doblan hacia atrás
    const osc = x => lejos ? tono(x, .86) : x;
    if (manga === 'corta') { E.tubo(id, [a, b, c], 6.6, osc(piel)); E.tubo(id + 1, [a, [lerp(a[0], b[0], .6), lerp(a[1], b[1], .6)]], 8.4, osc(R.arriba)); }
    else E.tubo(id, [a, b, c], 7.6, osc(R.arriba));
    if (lado === 1 && P.dedos > 0) dedos(E, c, P.dedos, osc(piel));
    const rm = E.modo === 'pixel' ? 5.4 : 4.6;           // en pixel el mitón es un poco más grande para que se lea como mano
    if (P.palma && lado === 1) E.parte(id + 2, gg => { gg.beginPath(); gg.ellipse(c[0], c[1], rm * 1.15, rm * .8, -.25, 0, Math.PI * 2); }, osc(piel), {});
    else E.parte(id + 2, gg => { gg.beginPath(); gg.arc(c[0], c[1], rm, 0, Math.PI * 2); }, osc(piel), {});
    return c;
  };
  const lejosPrimero = sv > .45;                        // de perfil, el brazo lejano va DETRÁS del torso

  g.save(); g.translate(0, cadera); g.rotate(P.lean); g.translate(0, -cadera);   // el torso se inclina desde la cadera
  if (lejosPrimero) brazo(-1, P.manoI, 50, true);

  // --- torso según la prenda (se angosta y se corre al frente al girar) ---
  g.save(); g.translate(2.2 * sv, 0); g.scale(1 - .3 * sv, 1);
  const tronco = gg => { gg.beginPath(); gg.moveTo(-12.5, hombroY + 1); gg.quadraticCurveTo(-15, hombroY + 1, -15, hombroY + 7);
    gg.lineTo(-14.5, cadera + 2); gg.quadraticCurveTo(0, cadera + 4.5, 14.5, cadera + 2); gg.lineTo(15, hombroY + 7); gg.quadraticCurveTo(15, hombroY + 1, 12.5, hombroY + 1); gg.closePath(); };
  if (R.tipo_abajo === 'falda' || R.tipo_arriba === 'vestido' || R.tipo_arriba === 'bata') {
    const col = R.tipo_arriba === 'vestido' || R.tipo_arriba === 'bata' ? R.arriba : R.abajo;
    const bajo = (R.tipo_arriba === 'bata' ? -7 : -11) + hb, vuelo = camina ? Math.sin(P.bob) * .8 : 0;
    E.parte(20, gg => { gg.beginPath(); gg.moveTo(-14.5, cadera - 3); gg.lineTo(-19.5 - vuelo, bajo); gg.quadraticCurveTo(0, bajo + 3.5, 19.5 + vuelo, bajo); gg.lineTo(14.5, cadera - 3); gg.closePath(); }, col, { sombraX: 7 });
  } else if (R.tipo_abajo === 'pantalon' || R.tipo_abajo === 'short') {
    E.parte(21, gg => { gg.beginPath(); gg.moveTo(-14.5, cadera - 4); gg.lineTo(-14.8, cadera + 3); gg.quadraticCurveTo(0, cadera + 6, 14.8, cadera + 3); gg.lineTo(14.5, cadera - 4); gg.closePath(); }, R.abajo, { sombraX: 7 });
  }
  E.parte(22, tronco, R.arriba, { sombraX: 7.5 });
  prendaDetalles(E, F, hombroY, cadera);
  if (F.accesorios.includes('delantal')) {
    E.parte(23, gg => { gg.beginPath(); gg.moveTo(-9, hombroY + 8); gg.lineTo(9, hombroY + 8); gg.lineTo(11, cadera + 1); gg.lineTo(12.5, -9 + hb); gg.quadraticCurveTo(0, -7 + hb, -12.5, -9 + hb); gg.lineTo(-11, cadera + 1); gg.closePath(); }, '#fbf7ef', { sombraX: 6, linea: tono('#fbf7ef', .7) });
    E.tubo(24, [[-9, hombroY + 8], [-4, hombroY + 1]], 1.6, '#fbf7ef', { linea: false }); E.tubo(25, [[9, hombroY + 8], [4, hombroY + 1]], 1.6, '#fbf7ef', { linea: false });
    E.parte(26, gg => { gg.beginPath(); gg.roundRect(-6, cadera + 5, 12, 7, 2); }, tono('#fbf7ef', .9), { linea: tono('#fbf7ef', .68) });
  }
  // cuello
  E.parte(27, gg => { gg.beginPath(); gg.roundRect(-3.6, hombroY - 4.5, 7.2, 6.5, 2); }, piel, { linea: false });
  if (F.ropa.cuello === 'alto') E.parte(28, gg => { gg.beginPath(); gg.roundRect(-5.4, hombroY - 4.2, 10.8, 6.6, 2.6); }, tono(R.arriba, .9), {});
  if (F.accesorios.includes('estetoscopio')) {
    E.tubo(29, [[-6, hombroY - 1], [-7, hombroY + 8], [-3, hombroY + 14]], 1.4, '#3b4a5c', { linea: false });
    E.tubo(30, [[6, hombroY - 1], [7, hombroY + 8], [3, hombroY + 14]], 1.4, '#3b4a5c', { linea: false });
    E.parte(31, gg => { gg.beginPath(); gg.arc(0, hombroY + 16, 2.6, 0, Math.PI * 2); }, '#c9d2dc', { linea: '#3b4a5c' });
  }
  if (F.accesorios.includes('collar')) {
    g.save(); g.lineWidth = E.modo === 'pixel' ? 2.2 : 1.1; g.strokeStyle = '#cfd3da'; g.setLineDash(E.modo === 'pixel' ? [] : [1.6, 1]);
    g.beginPath(); g.moveTo(-5.2, hombroY - .5); g.quadraticCurveTo(0, hombroY + 7.5, 5.2, hombroY - .5); g.stroke(); g.restore();
    if (E.modo === 'pixel') PALETA.add('#cfd3da');
    E.parte(32, gg => { gg.beginPath(); gg.arc(0, hombroY + 4.6, 1.9, 0, Math.PI * 2); }, '#e3e6ec', { linea: '#8b919c' });
  }
  g.restore();

  // --- cabeza ---
  g.save(); g.translate(cabeza[0], cabeza[1]); g.rotate(P.tilt);
  const RC = 21, ang = giroCabeza(P);
  const ladoX = a => RC * Math.sin(a + ang), ve = a => Math.cos(a + ang);
  E.parte(40, gg => { gg.beginPath(); gg.ellipse(0, 0, RC, RC * .96, 0, 0, Math.PI * 2); }, piel, { sombraX: 11 + sv * 14 });
  peloPerfil(E, F, sv, ang);
  if (sv > .75) {                                        // de perfil: la oreja visible y una naricita que sobresale del contorno
    const ox = ladoX(-Math.PI / 2);
    E.parte(47, gg => { gg.beginPath(); gg.ellipse(ox + 1, 3, 3.4, 4.6, 0, 0, Math.PI * 2); }, piel, {});
    const nx = RC * Math.sin(ang) + .6;
    E.parte(48, gg => { gg.beginPath(); gg.ellipse(nx, 4.5, 2.6, 2.3, 0, 0, Math.PI * 2); }, piel, {});
    E.parte(49, gg => { gg.beginPath(); gg.ellipse(nx - 2.2, 4.5, 2.6, 3.2, 0, 0, Math.PI * 2); }, piel, { linea: false, sombra: false });
  }
  if (F.accesorios.includes('aretes')) [-1, 1].forEach(l => { const a = l * Math.PI / 2; if (ve(a) < .05) return;
    E.parte(41 + (l > 0 ? 1 : 0), gg => { gg.beginPath(); gg.arc(ladoX(a) + (sv > .75 ? 1 : -l * .6), 5 + (sv > .75 ? 3.4 : 0), 1.6, 0, Math.PI * 2); }, '#e7e9ee', { linea: '#8b919c' }); });
  if (E.modo !== 'pixel') cara(E, F, P);
  peloFrente(E, F, sv, ang);
  if (F.accesorios.includes('lentes')) lentes(E, P);
  if (F.accesorios.includes('gorro-chef')) {
    g.save(); g.translate(-3 * sv, 0);
    E.parte(43, gg => { gg.beginPath(); gg.arc(-9, -24, 8.5, 0, Math.PI * 2); gg.arc(0, -28, 10, 0, Math.PI * 2); gg.arc(9, -24, 8.5, 0, Math.PI * 2); }, '#fbfbf7', { sombraX: 5, linea: '#b9b6ae' });
    E.parte(44, gg => { gg.beginPath(); gg.roundRect(-14, -21, 28, 9, 2.5); }, '#fbfbf7', { sombraX: 7, linea: '#b9b6ae' });
    g.restore();
  }
  if (F.accesorios.includes('gorra')) {
    const c = F.ropa.gorra || F.ropa.arriba;
    E.parte(45, gg => { gg.beginPath(); gg.moveTo(-20, -6); gg.quadraticCurveTo(-20, -25, 0, -25); gg.quadraticCurveTo(20, -25, 20, -6); gg.closePath(); }, c, { sombraX: 9 });
    E.parte(46, gg => { gg.beginPath(); gg.ellipse(12 + 10 * sv, -6, 15, 3.6, -.05, 0, Math.PI * 2); }, tono(c, .85), {});
  }
  g.restore();

  // --- brazos (encima del torso, para que se vean al cruzar) ---
  if (!lejosPrimero) brazo(-1, P.manoI, 50, false);
  const mano = brazo(1, P.manoD, 60, false);
  g.restore();

  if (P.numero > 0 && E.modo !== 'pixel') numeroContar(E, P, mano);
  if (P.puntos > 0 && E.modo !== 'pixel') puntosPensar(E, P, cabeza);
}

// dedos para «contar»: salen del mitón hacia arriba, abiertos en abanico
function dedos(E, c, n, col) {
  for (let i = 0; i < n; i++) {
    const a = -Math.PI / 2 + (i - (n - 1) / 2) * .36, L = E.modo === 'pixel' ? 8 : 7.5;
    E.tubo(70 + i, [[c[0] + Math.cos(a) * 2, c[1] + Math.sin(a) * 2], [c[0] + Math.cos(a) * L, c[1] + Math.sin(a) * L]], E.modo === 'pixel' ? 3.2 : 2.7, col);
  }
}
// la cifra que acompaña a «contar» (solo vector y papel: en pixel sería ilegible)
function numeroContar(E, P, mano) {
  const { g } = E, s = P.numeroPop, x = mano[0] + 11, y = mano[1] - 15;
  g.save(); g.translate(x, y); g.scale(s, s);
  E.parte(75, gg => { gg.beginPath(); gg.arc(0, 0, 7, 0, Math.PI * 2); }, '#ffffff', { linea: '#2a2430' });
  g.fillStyle = '#2a2430'; g.font = `800 10px ${LETRA_LIMPIA}`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(String(P.numero), 0, .6);
  g.restore();
}

function prendaDetalles(E, F, hombroY, cadera) {
  const { g } = E, R = F.ropa, osc = tono(R.arriba, .7);
  const linea = (pts, w = 1.1, col = osc) => { g.save(); g.lineWidth = E.modo === 'pixel' ? 2.2 : w; g.strokeStyle = col; g.lineCap = 'round';
    g.beginPath(); pts.forEach(([x, y], i) => i ? g.lineTo(x, y) : g.moveTo(x, y)); g.stroke(); g.restore(); if (E.modo === 'pixel') PALETA.add(col); };
  const boton = (x, y, col = osc) => E.parte(99 + x * 3 + y, gg => { gg.beginPath(); gg.arc(x, y, 1.2, 0, Math.PI * 2); }, col, { linea: false });
  switch (R.tipo_arriba) {
    case 'sueter':
      if (E.modo !== 'pixel') { linea([[-14.6, cadera - 1.5], [14.6, cadera - 1.5]], 1.2); linea([[0, hombroY + 3], [0, cadera - 2]], .9, tono(R.arriba, .8)); }
      break;
    case 'camisa':
      E.parte(90, gg => { gg.beginPath(); gg.moveTo(-6, hombroY); gg.lineTo(0, hombroY + 6); gg.lineTo(-2, hombroY + 1); gg.closePath(); gg.moveTo(6, hombroY); gg.lineTo(0, hombroY + 6); gg.lineTo(2, hombroY + 1); gg.closePath(); }, tono(R.arriba, 1.15), {});
      if (E.modo !== 'pixel') [0, 1, 2].forEach(i => boton(0, hombroY + 10 + i * 7));
      break;
    case 'bata':
      linea([[-2, hombroY + 1], [-4, -8]], 1.2); linea([[2, hombroY + 1], [4, -8]], 1.2);
      E.parte(91, gg => { gg.beginPath(); gg.roundRect(6, hombroY + 11, 6, 5, 1); }, tono(R.arriba, .92), {});
      break;
    case 'filipina':
      [0, 1, 2].forEach(i => { boton(-4.5, hombroY + 9 + i * 7); boton(4.5, hombroY + 9 + i * 7); });
      break;
  }
}

function cara(E, F, P) {                                   // vector y papel (en pixel la cara va pixel por pixel)
  const { g } = E, RC = 21, ang = giroCabeza(P);
  const X = a => RC * Math.sin(a + ang), V = a => Math.cos(a + ang);
  const aOjo = Math.asin(8 / RC), aChapa = Math.asin(12.5 / RC);
  const oy = 2, arriba = P.ojos === 'arriba' ? -1.6 : P.ojos === 'abajo' ? 1 : 0;
  g.save(); g.lineCap = 'round';
  // chapitas
  g.fillStyle = 'rgba(240,110,120,.32)';
  [-1, 1].forEach(l => { const v = V(l * aChapa); if (v < .15) return; g.beginPath(); g.ellipse(X(l * aChapa), 8, 3.6 * Math.max(v, .45), 2.2, 0, 0, Math.PI * 2); g.fill(); });
  // ojos
  [-1, 1].forEach(l => {
    const v = V(l * aOjo); if (v < .12) return;
    const x = X(l * aOjo), sx = clamp(v, .5, 1);
    const cerrado = P.ojos === 'cerrados' || (P.ojos === 'guiño' && l === 1);
    const feliz = P.ojos === 'felices' || (P.ojos === 'guiño' && l === 1 && false);
    g.strokeStyle = F.ojos; g.fillStyle = F.ojos;
    if (P.ojos === 'guiño' && l === 1) { g.lineWidth = 1.7; g.beginPath(); g.moveTo(x - 2.6 * sx, oy + 1); g.quadraticCurveTo(x, oy - 2.4, x + 2.6 * sx, oy + 1); g.stroke(); return; }
    if (cerrado) { g.lineWidth = 1.5; g.beginPath(); g.moveTo(x - 2.4 * sx, oy + .5); g.quadraticCurveTo(x, oy + 1.8, x + 2.4 * sx, oy + .5); g.stroke(); return; }
    if (feliz) { g.lineWidth = 1.7; g.beginPath(); g.moveTo(x - 2.6 * sx, oy + 1); g.quadraticCurveTo(x, oy - 2.4, x + 2.6 * sx, oy + 1); g.stroke(); return; }
    const grande = P.ojos === 'grandes', rx = (grande ? 3 : 2.5) * sx, ry = grande ? 4 : 3.3;
    const mira = P.ojos === 'lado' ? 1 : 0;
    g.beginPath(); g.ellipse(x + mira * .6, oy + arriba, rx, ry, 0, 0, Math.PI * 2); g.fill();
    g.fillStyle = '#ffffff'; g.beginPath(); g.arc(x - .9 * sx + mira * 1.4, oy - 1.2 + arriba, grande ? 1.2 : .95, 0, Math.PI * 2); g.fill();
    if (grande) { g.beginPath(); g.arc(x + .9 * sx, oy + 1.4, .5, 0, Math.PI * 2); g.fill(); }
  });
  // cejas (del color del pelo): la expresión vive sobre todo aquí
  g.strokeStyle = tono(F.pelo.color, .8); g.lineWidth = 1.3;
  const cejaY = { normal: 0, arriba: -1.2, muyArriba: -2.8, triste: 0, duda: 0 }[P.cejas] ?? 0;
  [-1, 1].forEach(l => {
    const v = V(l * aOjo); if (v < .12) return;
    const x = X(l * aOjo), sx = clamp(v, .5, 1), yb = oy - 5.6 + cejaY + (P.ojos === 'arriba' ? -1.5 : 0);
    let dIn = 0, dOut = 0;                              // subida del extremo de adentro y del de afuera
    if (P.cejas === 'triste') { dIn = -1.6; dOut = .9; }
    if (P.cejas === 'duda') { if (l === 1) { dIn = -2.2; dOut = -2.8; } else { dIn = .6; dOut = 0; } }
    const xin = x - l * 2.8 * sx, xout = x + l * 3 * sx;
    g.beginPath(); g.moveTo(xin, yb + dIn); g.quadraticCurveTo(x, yb - 1.2 + (dIn + dOut) / 2, xout, yb + dOut); g.stroke();
  });
  // boca
  const by = 11, v0 = V(0), bx = X(0) - (v0 < .3 ? 1.2 : 0), bs = clamp(v0, .45, 1);
  g.fillStyle = tono(F.labios, .55); g.strokeStyle = tono(F.labios, .75); g.lineWidth = 1.3;
  g.save(); g.translate(bx, 0); g.scale(bs, 1);
  switch (P.boca) {
    case 'cerrada': g.beginPath(); g.moveTo(-2.2, by + .3); g.lineTo(2.2, by + .3); g.stroke(); break;
    case 'sonrisa': g.beginPath(); g.moveTo(-3.4, by - .6); g.quadraticCurveTo(0, by + 2.6, 3.4, by - .6); g.stroke(); break;
    case 'sonrisaGrande': g.beginPath(); g.moveTo(-4.2, by - 1); g.quadraticCurveTo(0, by + 4.6, 4.2, by - 1); g.closePath(); g.fill();
      g.fillStyle = '#ffffff'; g.beginPath(); g.moveTo(-3.4, by - .7); g.lineTo(3.4, by - .7); g.lineTo(2.8, by + .5); g.lineTo(-2.8, by + .5); g.closePath(); g.fill(); break;
    case 'media': g.beginPath(); g.ellipse(0, by + .5, 2.4, 1.6, 0, 0, Math.PI * 2); g.fill(); break;
    case 'o': g.beginPath(); g.ellipse(0, by + 1, 2, 2.6, 0, 0, Math.PI * 2); g.fill(); break;
    case 'ladeada': g.beginPath(); g.moveTo(-3, by + 1); g.quadraticCurveTo(0, by + 1.4, 3.2, by - .9); g.stroke(); break;
    case 'triste': g.beginPath(); g.moveTo(-3.2, by + 1.6); g.quadraticCurveTo(0, by - 1.6, 3.2, by + 1.6); g.stroke(); break;
    case 'abierta': g.beginPath(); g.moveTo(-3.6, by - .8); g.quadraticCurveTo(0, by - .2, 3.6, by - .8); g.quadraticCurveTo(0, by + 5.4, -3.6, by - .8); g.fill();
      g.fillStyle = '#e8828a'; g.beginPath(); g.ellipse(0, by + 2.4, 1.8, 1, 0, 0, Math.PI * 2); g.fill(); break;
  }
  g.restore();
  g.restore();
}

function peloAtras(E, F, sv = 0) {
  const L = F.pelo.largo, c = tono(F.pelo.color, .82);
  if (L === 'sin' || L === 'corto') return;
  if (F.pelo.estilo === 'cola') {                        // la cola cuelga del lado de la nuca (de perfil, atrás)
    const l = sv > .3 ? -1 : 1;
    E.parte(1, gg => { gg.beginPath(); gg.moveTo(l * 15, -12); gg.quadraticCurveTo(l * 34, -6, l * 27, 22); gg.quadraticCurveTo(l * 24, 30, l * 21, 20); gg.quadraticCurveTo(l * 26, 2, l * 12, -6); gg.closePath(); }, c, {});
    return;
  }
  if (F.pelo.estilo === 'chongo') return;
  const bajo = L === 'largo' ? 50 : 22;
  if (F.pelo.estilo === 'rizado') {
    E.parte(2, gg => { gg.beginPath(); for (let i = 0; i < 11; i++) { const a = Math.PI * (.05 + i * .09); gg.moveTo(0, 0); gg.arc(Math.cos(a) * 21 * (i % 2 ? 1.05 : 1), -4 + Math.sin(a) * (bajo * .55 + 6), 8, 0, Math.PI * 2); } gg.ellipse(0, bajo * .35, 24, bajo * .5, 0, 0, Math.PI * 2); }, c, {});
    return;
  }
  // arranca por dentro de la cabeza (queda tapado) y cae siguiendo su curva: sin esquinas que asomen
  E.parte(3, gg => { gg.beginPath(); gg.moveTo(-15, -16); gg.bezierCurveTo(-26, -8, -26, bajo * .5, -21, bajo); gg.quadraticCurveTo(0, bajo + 6, 21, bajo); gg.bezierCurveTo(26, bajo * .5, 26, -8, 15, -16); gg.closePath(); }, c, {});
}

// de perfil el pelo tapa la parte de atrás de la cabeza, desde la coronilla hasta la oreja
function peloPerfil(E, F, sv, ang) {
  if (sv < .05 || F.pelo.largo === 'sin') return;
  const RC = 21, c = F.pelo.color, largo = F.pelo.largo === 'largo' || F.pelo.largo === 'medio';
  const borde = lerp(-RC - 3, -3.5, sv), top = RC * Math.sin(ang) * .3;
  E.parte(9, gg => {
    gg.beginPath(); gg.moveTo(top, -RC - 3);
    gg.bezierCurveTo(borde + 6, -RC * .7, borde - 2, -8, borde + 1, 2);
    if (largo) gg.lineTo(borde + 2, RC + 3); else gg.quadraticCurveTo(borde - 2, 10, borde - 6, 12);
    gg.lineTo(-RC - 6, RC + 6); gg.lineTo(-RC - 6, -RC - 6); gg.closePath();
  }, tono(c, .92), { linea: false, sombra: false, recorte: gg => { gg.beginPath(); gg.ellipse(0, 0, RC + .8, RC * .96 + .8, 0, 0, Math.PI * 2); } });
}

function peloFrente(E, F, sv = 0, ang = 0) {
  const L = F.pelo.largo, est = F.pelo.estilo, c = F.pelo.color;
  if (L === 'sin') return;
  const RC = 21;
  const brillo = F.pelo.brillo || tono(c, 1.28);
  const g = E.g;
  g.save(); g.translate(RC * Math.sin(ang) * .28, 0); g.scale(1 - .12 * sv, 1);   // el frente del pelo acompaña el giro
  if (est === 'rizado') {
    E.parte(4, gg => { gg.beginPath(); for (let i = 0; i < 9; i++) { const a = Math.PI * (1.02 + i * .12); gg.moveTo(Math.cos(a) * 20 + 7, Math.sin(a) * 19); gg.arc(Math.cos(a) * 20, Math.sin(a) * 19, 7, 0, Math.PI * 2); } }, c, {});
    g.restore(); return;
  }
  if (est === 'flequillo') {
    E.parte(5, gg => { gg.beginPath(); gg.moveTo(-RC - 1.5, 4); gg.bezierCurveTo(-RC - 3, -27, RC + 3, -27, RC + 1.5, 4);
      gg.lineTo(RC - 3, -3); for (let i = 0; i <= 6; i++) gg.lineTo(RC - 5 - i * 5.5, i % 2 ? -3.5 : -6.5); gg.lineTo(-RC + 3, -3); gg.closePath(); }, c, { sombraX: 12 });
  } else {                                               // raya al medio / cola / chongo: dos cortinas que abren en la frente
    const lados = L === 'corto' || est === 'cola' || est === 'chongo' ? 4 : 13;
    const cortina = lado => gg => { gg.beginPath(); gg.moveTo(0, -20.5);
      gg.bezierCurveTo(lado * 13, -24, lado * (RC + 4), -14, lado * (RC + 2.2), 2);
      gg.lineTo(lado * (RC + 1.5), lados); gg.quadraticCurveTo(lado * (RC - 3), lados - 2, lado * (RC - 4.5), 0);
      gg.bezierCurveTo(lado * (RC - 6), -9, lado * 7, -13, lado * .6, -17.5); gg.closePath(); };
    E.parte(6, cortina(-1), c, {}); if (sv < .6) E.parte(7, cortina(1), tono(c, .9), {});
    else E.parte(7, gg => { gg.beginPath(); gg.moveTo(0, -20.5); gg.bezierCurveTo(9, -23, RC + 1, -15, RC + 1, -6); gg.quadraticCurveTo(12, -12, 1, -14); gg.closePath(); }, tono(c, .9), {});
    if (E.modo !== 'papel') { g.save(); g.strokeStyle = brillo; g.lineWidth = E.modo === 'pixel' ? 2.4 : 1.6; g.lineCap = 'round';
      g.beginPath(); g.moveTo(-6, -18); g.quadraticCurveTo(-13, -16, -16, -9); g.stroke(); g.restore(); if (E.modo === 'pixel') PALETA.add(brillo); }
  }
  if (est === 'chongo') E.parte(8, gg => { gg.beginPath(); gg.arc(-7 * sv, -25, 8.5, 0, Math.PI * 2); }, c, { sombraX: 3 });
  g.restore();
}

function lentes(E, P) {
  const { g } = E, RC = 21, ang = giroCabeza(P), aOjo = Math.asin(8 / RC);
  const X = a => RC * Math.sin(a + ang), V = a => Math.cos(a + ang);
  g.save(); g.strokeStyle = '#2a2430'; g.lineWidth = E.modo === 'pixel' ? 2.2 : 1.3;
  const vis = [-1, 1].filter(l => V(l * aOjo) >= .12);
  g.beginPath();
  vis.forEach(l => { const x = X(l * aOjo), sx = clamp(V(l * aOjo), .45, 1); g.moveTo(x + 5 * sx, 2); g.ellipse(x, 2, 5 * sx, 5, 0, 0, Math.PI * 2); });
  if (vis.length === 2) { g.moveTo(X(-aOjo) + 5 * clamp(V(-aOjo), .45, 1), 1.2); g.quadraticCurveTo(X(0), -.4, X(aOjo) - 5 * clamp(V(aOjo), .45, 1), 1.2); }
  else if (vis.length === 1) { const x = X(vis[0] * aOjo); g.moveTo(x - 5 * clamp(V(vis[0] * aOjo), .45, 1), 1.5); g.lineTo(X(-Math.PI / 2) + 2, 2.5); }   // patita hacia la oreja
  g.stroke(); g.restore();
  if (E.modo === 'pixel') PALETA.add('#2a2430');
}

function puntosPensar(E, P, cabeza) {
  [0, 1, 2].forEach(i => {
    const k = clamp(P.puntos * 3 - i); if (k <= 0) return;
    const r = (1.6 + i * 1.1) * back(k);
    E.parte(80 + i, gg => { gg.beginPath(); gg.arc(cabeza[0] + 16 + i * 6, cabeza[1] - 24 - i * 7, r, 0, Math.PI * 2); }, '#ffffff', { linea: '#8a8494' });
  });
}

// ---------- criaturas: gato, perro, blob, robot ----------
function criatura(E, F, P) {
  const { g } = E, C = F.criatura, col = C.color, panza = C.panza, forma = C.forma;
  const robot = forma === 'robot', blob = forma === 'blob';
  const cab = [0, -70 + P.bob];
  const metal = '#8d95a3', metalOsc = '#5d6472';
  // cola: curva en S que se mece (sale de atrás del cuerpo)
  if (forma === 'gato' || forma === 'perro') {
    const w = P.cola, gato = forma === 'gato';
    const pts = gato ? [[11, -14], [21, -15 + w * 3], [28, -24 + w * 6], [28, -35 + w * 10], [24, -42 + w * 12]]
                     : [[12, -16], [21, -20 + w * 5], [26, -29 + w * 10]];
    E.tubo(1, pts, gato ? 5 : 7, col);
    if (!gato) E.parte(2, gg => { gg.beginPath(); gg.arc(pts[2][0], pts[2][1], 4, 0, Math.PI * 2); }, col, {});
  }
  // patitas (al caminar se levantan por turnos, de frente)
  const pata = (lado, giro, pie) => {
    const hx = lado * (blob ? 9 : 8), hy = -12, lift = pie ? -pie[1] * .8 : 0, dx = pie ? pie[0] * .25 : 0;
    const px = hx + Math.sin(giro) * 11 + dx, py = hy + Math.cos(giro) * 11 - lift;
    E.tubo(10 + lado, [[hx, hy], [px, py - 1.5]], robot ? 6.5 : 7.5, robot ? metal : col);
    E.parte(12 + lado, gg => { gg.beginPath(); gg.ellipse(px, py - 1.5, 5.4, 3.4, 0, 0, Math.PI * 2); }, robot ? metalOsc : tono(col, .9), {}); };
  pata(-1, P.piernaI, P.pieI); pata(1, P.piernaD, P.pieD);
  // cuerpo
  if (robot) {
    E.parte(19, gg => { gg.beginPath(); gg.roundRect(-5, -58 + P.bob, 10, 14, 2); }, metalOsc, {});   // cuello
    E.parte(20, gg => { gg.beginPath(); gg.roundRect(-16, -46 + P.bob, 32, 34, 6); }, col, { sombraX: 8 });
    E.parte(21, gg => { gg.beginPath(); gg.roundRect(-9, -38 + P.bob, 18, 14, 3); }, '#1f2733', { linea: false });
    E.parte(22, gg => { gg.beginPath(); gg.arc(-4, -31 + P.bob, 2, 0, Math.PI * 2); }, '#6fe3ff', { linea: false });
    E.parte(23, gg => { gg.beginPath(); gg.arc(4, -31 + P.bob, 2, 0, Math.PI * 2); }, '#ffd84d', { linea: false });
  } else if (!blob) {
    E.parte(20, gg => { gg.beginPath(); gg.ellipse(0, -30 + P.bob * .5, 18, 20, 0, 0, Math.PI * 2); }, col, { sombraX: 9 });
    E.parte(21, gg => { gg.beginPath(); gg.ellipse(0, -26 + P.bob * .5, 10, 12, 0, 0, Math.PI * 2); }, panza, { linea: false });
  }
  // cabeza (el blob es cabeza y cuerpo en uno)
  const ang = giroCabeza(P) * (robot ? .25 : .55);
  g.save(); g.translate(cab[0], cab[1]); g.rotate(P.tilt);
  if (forma === 'gato') {
    E.parte(30, gg => { gg.beginPath(); gg.moveTo(-19, -8); gg.lineTo(-17, -29); gg.lineTo(-6, -17); gg.closePath(); gg.moveTo(19, -8); gg.lineTo(17, -29); gg.lineTo(6, -17); gg.closePath(); }, col, {});
    E.parte(31, gg => { gg.beginPath(); gg.moveTo(-16, -12); gg.lineTo(-15.5, -24); gg.lineTo(-9, -17); gg.closePath(); gg.moveTo(16, -12); gg.lineTo(15.5, -24); gg.lineTo(9, -17); gg.closePath(); }, '#f4a7b3', { linea: false });
  }
  if (forma === 'perro') E.parte(30, gg => { gg.beginPath(); gg.ellipse(-20, 2, 6.5, 13, .3, 0, Math.PI * 2); gg.ellipse(20, 2, 6.5, 13, -.3, 0, Math.PI * 2); }, tono(col, .72), {});
  if (robot) {
    E.tubo(32, [[0, -20], [0, -29]], 1.8, metalOsc);
    E.parte(33, gg => { gg.beginPath(); gg.arc(0, -30, 3, 0, Math.PI * 2); }, '#ff5a5f', {});
    E.parte(34, gg => { gg.beginPath(); gg.roundRect(-21, -20, 42, 36, 8); }, col, { sombraX: 10 });
    E.parte(35, gg => { gg.beginPath(); gg.roundRect(-16, -13, 32, 20, 6); }, '#1f2733', { linea: false });
    E.parte(36, gg => { gg.beginPath(); gg.roundRect(-24, -6, 4, 10, 2); gg.roundRect(20, -6, 4, 10, 2); }, metalOsc, {});   // tuercas de las orejas
  } else if (blob) {
    E.parte(34, gg => { gg.beginPath(); gg.moveTo(0, -24); gg.bezierCurveTo(22, -24, 27, 8, 26, 32); gg.bezierCurveTo(25, 60, -25, 60, -26, 32); gg.bezierCurveTo(-27, 8, -22, -24, 0, -24); gg.closePath(); }, col, { sombraX: 13 });
    E.parte(37, gg => { gg.beginPath(); gg.ellipse(0, 40, 14, 11, 0, 0, Math.PI * 2); }, panza, { linea: false });
    E.parte(38, gg => { gg.beginPath(); gg.ellipse(-12, -12, 4, 6, -.5, 0, Math.PI * 2); }, tono(col, 1.35), { linea: false, sombra: false });   // brillo de gomita
  } else E.parte(34, gg => { gg.beginPath(); gg.ellipse(0, 0, 21, 18.5, 0, 0, Math.PI * 2); }, col, { sombraX: 11 });
  if (forma === 'gato' || forma === 'perro') {
    const hx = 21 * Math.sin(ang) * .7;
    E.parte(39, gg => { gg.beginPath(); gg.ellipse(hx, forma === 'perro' ? 8.5 : 6.5, forma === 'perro' ? 9.5 : 8.5, forma === 'perro' ? 6.4 : 5.8, 0, 0, Math.PI * 2); }, panza, { linea: forma === 'perro' ? undefined : false });
    if (forma === 'perro') E.parte(40, gg => { gg.beginPath(); gg.ellipse(hx, 4.4, 3.6, 2.5, 0, 0, Math.PI * 2); }, '#2a1f24', { linea: false });   // la nariz
  }
  if (E.modo !== 'pixel') {
    const Fc = Object.assign({}, F, { ojos: robot ? '#6fe3ff' : F.ojos, labios: '#8a3a44', pelo: { color: tono(col, .6) } });
    const Pc = Object.assign({}, P, { vista: P.vista * (robot ? .25 : .55) });
    g.save(); if (robot) g.translate(0, -3); if (blob) g.translate(0, 6);
    if (forma === 'perro') { g.save(); g.translate(0, -3.6); cara(E, Fc, Pc); g.restore(); } else cara(E, Fc, Pc);   // perro: ojos arriba del hocico
    g.restore();
    if (forma === 'gato') { g.save(); g.strokeStyle = tono(col, .45); g.lineWidth = .9; g.beginPath(); const hx = 21 * Math.sin(ang) * .7;
      [[-9, 7, -19, 5], [-9, 9, -19, 10], [9, 7, 19, 5], [9, 9, 19, 10]].forEach(([a, b, c2, d]) => { g.moveTo(a + hx, b); g.lineTo(c2 + hx, d); }); g.stroke();
      g.fillStyle = '#e07a8a'; g.beginPath(); g.moveTo(-1.6 + hx, 6.4); g.lineTo(1.6 + hx, 6.4); g.lineTo(hx, 8.2); g.closePath(); g.fill(); g.restore(); }
  }
  g.restore();
  // bracitos: el mitón es del color del cuerpo (o metálico en el robot), no un aro gris
  const brazo = (lado, mano, id) => { const sh = [lado * (blob ? 22 : 14), (blob ? -44 : -40) + P.bob];
    if (P.pieD) mano = [lado * 20, -26 - (lado > 0 ? P.pieI : P.pieD)[1] * .9];   // al caminar de frente, el brazo sube con la pierna contraria
    const m = [mano[0] * (blob ? 1.05 : .95), mano[1] * .8 - 1];                    // en reposo el brazo cuelga (nada de manos en la cintura)
    const pts = ik(sh[0], sh[1], m[0], m[1], 9.5, 9.5, lado);
    E.tubo(id, pts, 6, robot ? metal : col);
    if (lado === 1 && P.dedos > 0) dedos(E, pts[2], P.dedos, robot ? metal : col);
    E.parte(id + 1, gg => { gg.beginPath(); gg.arc(pts[2][0], pts[2][1], E.modo === 'pixel' ? 5 : 4.4, 0, Math.PI * 2); }, robot ? metalOsc : tono(col, 1.06), {});
    return pts[2]; };
  brazo(-1, P.manoI, 50); const mano = brazo(1, P.manoD, 60);
  if (P.numero > 0 && E.modo !== 'pixel') numeroContar(E, P, mano);
  if (P.puntos > 0 && E.modo !== 'pixel') puntosPensar(E, P, [cab[0], cab[1] + 6]);
}

// ---------- pixel: de formas suavizadas a pixel art de verdad ----------
function cuantizar(g, GW, GH, F) {
  const d = g.getImageData(0, 0, GW, GH), px = d.data;
  const pal = [...PALETA].map(rgbDe);
  const n = GW * GH, opaco = new Uint8Array(n);
  for (let i = 0, j = 0; j < n; i += 4, j++) {
    if (px[i + 3] < 110) { px[i + 3] = 0; continue; }
    // deshace el semitransparente del borde antes de buscar el color más parecido
    const a = px[i + 3] / 255, r = px[i] / a, gg = px[i + 1] / a, b = px[i + 2] / a;
    let m = pal[0], md = 1e9;
    for (const c of pal) { const dd = (c[0] - r) ** 2 + (c[1] - gg) ** 2 + (c[2] - b) ** 2; if (dd < md) { md = dd; m = c; } }
    px[i] = m[0]; px[i + 1] = m[1]; px[i + 2] = m[2]; px[i + 3] = 255; opaco[j] = 1;
  }
  const co = rgbDe(F.contorno);
  const o = new Uint8ClampedArray(px);
  for (let y = 0; y < GH; y++) for (let x = 0; x < GW; x++) {
    const j = y * GW + x; if (opaco[j]) continue;
    const vec = (x > 0 && opaco[j - 1]) || (x < GW - 1 && opaco[j + 1]) || (y > 0 && opaco[j - GW]) || (y < GH - 1 && opaco[j + GW]);
    if (vec) { const i = j * 4; o[i] = co[0]; o[i + 1] = co[1]; o[i + 2] = co[2]; o[i + 3] = 255; }
  }
  d.data.set(o); g.putImageData(d, 0, 0);
}

function caraPixel(g, F, P) {
  // la cara va a mano, pixel por pixel: a este tamaño una forma suavizada se perdería
  const PIX = .44, OX = Math.floor(Math.ceil(110 * PIX) / 2), OY = Math.round(164 * PIX);   // igual que en crearPersonaje
  const cria = F.tipo === 'criatura', forma = F.criatura.forma;
  // centro de la cara con las mismas transformaciones del cuerpo: inclinación desde la cadera, aplastado y salto
  const camina = !!P.pieD, hb = camina && !cria ? P.bob : 0;
  const rel = (cria ? -70 : -79) + P.bob + (cria && forma === 'blob' ? 12 : 2) + (cria && forma === 'robot' ? -3 : 0) - (cria ? 0 : -23 + hb);
  const lean = cria ? 0 : P.lean;
  const ux = -rel * Math.sin(lean), uy = rel * Math.cos(lean) + (cria ? 0 : -23 + hb);
  const hx = OX + ux * P.sx * PIX, hy = OY + (uy * P.sy + P.y) * PIX;
  // rasgos sobre la «esfera» de la cabeza: giran con la vista y rotan con la inclinación de la cabeza
  const RCg = (cria && forma === 'blob' ? 24 : 21) * PIX, ang = giroCabeza(P) * (cria ? (forma === 'robot' ? .25 : .55) : 1);   // el visor del robot es plano: gira poco
  const rot = P.tilt + lean, cr = Math.cos(rot), sr = Math.sin(rot);
  const pt = (a, dy) => { const dx = RCg * Math.sin(a + ang); return [Math.floor(hx + dx * cr - dy * sr), Math.floor(hy + dx * sr + dy * cr)]; };
  const ve = a => Math.cos(a + ang);
  const set = (col, x, y, w = 1, h = 1) => { g.fillStyle = col; g.fillRect(Math.floor(x), Math.floor(y), w, h); };
  const ojo = cria && forma === 'robot' ? '#6fe3ff' : F.ojos;
  const aO = Math.asin((cria && forma === 'blob' ? 5 : 4) / RCg), dyO = P.ojos === 'arriba' ? -2 : P.ojos === 'abajo' ? 0 : -1;
  const ceja = tono(cria ? tono(F.criatura.color, .6) : F.pelo.color, .8);
  [-1, 1].forEach(l => {
    if (ve(l * aO) < .15) return;
    const [x0, y0] = pt(l * aO, dyO), x = x0 - (l < 0 ? 1 : 0);
    const cerrado = P.ojos === 'cerrados', guino = P.ojos === 'guiño' && l === 1;
    if (cerrado) set(ojo, x, y0 + 1, 2, 1);
    else if (P.ojos === 'felices' || guino) { set(ojo, x, y0, 2, 1); set(ojo, x - 1, y0 + 1); set(ojo, x + 2, y0 + 1); }
    else if (P.ojos === 'grandes') { set(ojo, x, y0 - 1, 2, 3); set('#ffffff', x, y0 - 1); }
    else { set(ojo, x, y0, 2, 2); set('#ffffff', P.ojos === 'lado' ? x + 1 : x, y0); }
    // cejas: solo cuando la expresión las necesita (a este tamaño, de más ensucian)
    const yb = y0 - 3;
    if (P.cejas === 'muyArriba') set(ceja, x, yb - 1, 2, 1);
    else if (P.cejas === 'triste') { set(ceja, l < 0 ? x + 1 : x, yb - 1); set(ceja, l < 0 ? x : x + 1, yb); }
    else if (P.cejas === 'duda') { if (l === 1) set(ceja, x, yb - 1, 2, 1); else set(ceja, x, yb, 2, 1); }
  });
  if (!(cria && forma === 'robot')) [-1, 1].forEach(l => { const a = l * Math.asin(Math.min(.95, 6 / RCg)); if (ve(a) < .25) return; const [x, y] = pt(a, 2); set('#f08c96', x - (l < 0 ? 1 : 0), y, 2, 1); });
  const bocaC = cria ? '#6b2a34' : tono(F.labios, .5);
  const [mx0, by] = pt(0, 3), mx = mx0 - (ve(0) < .35 ? 1 : 0);
  switch (P.boca) {
    case 'cerrada': set(bocaC, mx - 1, by, 2, 1); break;
    case 'sonrisa': set(bocaC, mx - 2, by); set(bocaC, mx - 1, by + 1, 2, 1); set(bocaC, mx + 1, by); break;
    case 'sonrisaGrande': set(bocaC, mx - 2, by, 4, 1); set(bocaC, mx - 1, by + 1, 2, 1); set('#ffffff', mx - 1, by, 2, 1); break;
    case 'media': set(bocaC, mx - 1, by, 2, 1); set(bocaC, mx - 1, by + 1, 2, 1); break;
    case 'o': set(bocaC, mx - 1, by, 2, 2); break;
    case 'ladeada': set(bocaC, mx - 1, by + 1); set(bocaC, mx, by + 1); set(bocaC, mx + 1, by); break;
    case 'triste': set(bocaC, mx - 1, by, 2, 1); set(bocaC, mx - 2, by + 1); set(bocaC, mx + 1, by + 1); break;
    case 'abierta': set(bocaC, mx - 2, by, 4, 1); set(bocaC, mx - 1, by + 1, 2, 1); set('#e8828a', mx - 1, by + 1); break;
  }
  // globitos de pensar: círculos pixel de verdad, con contorno de 1 px (sin esquinas)
  if (P.puntos > 0) [[9, -9, 1.1], [12, -13, 1.6], [16, -18, 2.4]].forEach(([dx, dy, r], i) => {
    const k = clamp(P.puntos * 3 - i); if (k <= 0) return;
    circuloPixel(g, hx + dx, hy + dy, r * (k < 1 ? .6 + .4 * k : 1), '#ffffff', F.contorno);
  });
}
function circuloPixel(g, cx, cy, r, relleno, borde) {
  const dentro = (x, y) => (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r + .35;
  const x0 = Math.floor(cx - r - 2), y0 = Math.floor(cy - r - 2), n = Math.ceil(2 * r + 4);
  for (let y = y0; y < y0 + n; y++) for (let x = x0; x < x0 + n; x++) {
    if (dentro(x, y)) { g.fillStyle = relleno; g.fillRect(x, y, 1, 1); }
    else if (dentro(x + 1, y) || dentro(x - 1, y) || dentro(x, y + 1) || dentro(x, y - 1)) { g.fillStyle = borde; g.fillRect(x, y, 1, 1); }
  }
}
