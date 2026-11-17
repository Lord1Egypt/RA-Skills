// ============================================================================
// CATALOGO_OBJETOS de animacion-dibujada-f100k — objetos y escenarios dibujados con código, por rubro.
// Se carga DESPUÉS de nucleo.js. Los kits de cada rubro viven en nucleo/kits/*.js y se registran solos.
//
//   dibujarObjeto(nombre, x, y, tam, { t, estilo, rot, anim, tinta })
//       (x, y) = centro de la base del objeto · tam = alto en px
//       t      = segundos desde que el objeto entra (lo usan 'aparece' y las animaciones propias: llama, vapor…)
//       estilo = 'vector' (plano, contorno oscuro, sombra plana, 2 tonos) | 'pixel' (mismo objeto en grilla chica)
//       anim   = null | 'aparece' | 'entra-izq' | 'entra-der' | 'cae' | 'flota' | 'late' | 'brilla'
//       sombra = true (sombra de contacto en el piso) | false
//   medidaObjeto(nombre) → { izq, der, arriba, ancho, alto } en unidades (alto típico 100), medida REAL del dibujo
//   sombraContacto(x, y, mitadAncho, { altura = 0 })   sombra de contacto de 2 capas (la usan objetos y quien quiera)
//   componerFila(nombres, { x0, x1, tam, hueco }) → [{ nombre, x, tam }] sin encimarse (usa la medida real)
//   escenario(nombre, t, { estilo, paleta })   pinta el fondo completo (1080×1920); arriba queda libre para texto.
//       registrarEscenario(nombre, fondo, vivo?) — «vivo(t, paleta)» es opcional: detalle animado sutil encima del fondo (vector).
//   KITS[rubro] · kitDe(rubro) · registrarObjeto · registrarEscenario · registrarKit · objetosDisponibles()
//
// Unidades de dibujo de cada objeto: la base está en (0, 0) y lo más alto en y = -100. Ancho típico entre -60 y 60.
// ============================================================================

const CATALOGO_OBJETOS = {}, ESCENARIOS = {}, KITS = {};
const TINTA_OBJ = '#2a2231';
function registrarObjeto(nombre, dibujo, o = {}) { CATALOGO_OBJETOS[nombre] = { dibujo, ancho: o.ancho || 46, anima: !!o.anima }; }
function registrarEscenario(nombre, fn, vivo = null) { ESCENARIOS[nombre] = fn; if (vivo) ESCENARIOS_VIVOS[nombre] = vivo; }
const ESCENARIOS_VIVOS = {};
function registrarKit(rubro, kit) { KITS[_norma(rubro)] = kit; }
function objetosDisponibles() { return Object.keys(CATALOGO_OBJETOS).sort(); }
function _norma(s) { return String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/\s+/g, '-'); }
function kitDe(rubro) {
  const k = KITS[_norma(rubro)];
  if (!k) { console.warn(`[objetos] no hay kit para «${rubro}»: uso el genérico. Hay: ${Object.keys(KITS).join(', ')}`); return KITS.generico; }
  return k;
}

// ---------- color ----------
function _rgb(hex) { const h = hex.replace('#', ''); const n = parseInt(h.length === 3 ? h.split('').map(c => c + c).join('') : h, 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
function _hex(c) { return '#' + c.map(v => Math.round(clamp(v, 0, 255)).toString(16).padStart(2, '0')).join(''); }
function oscuro(hex, k = .82) { return _hex(_rgb(hex).map(v => v * k)); }
function claro(hex, k = .35) { return _hex(_rgb(hex).map(v => v + (255 - v) * k)); }

// ---------- estado del dibujo en curso ----------
let _g = null, _lw = 5, _modo = 'vector', _pal = null, _tinta = TINTA_OBJ, _esc = 1;
function _reg(col) { if (_pal && typeof col === 'string' && col[0] === '#') _pal.add(col.toLowerCase()); return col; }

// ---------- trazos (en unidades del objeto) ----------
function pRR(x, y, w, h, r) { const p = new Path2D(); p.roundRect(x, y, w, h, r); return p; }
function pEl(cx, cy, rx, ry, rot = 0, a0 = 0, a1 = Math.PI * 2, cerrar = true) { const p = new Path2D(); p.ellipse(cx, cy, rx, ry, rot, a0, a1); if (cerrar) p.closePath(); return p; }
function pPoli(pts, cerrado = true) { const p = new Path2D(); pts.forEach(([x, y], i) => i ? p.lineTo(x, y) : p.moveTo(x, y)); if (cerrado) p.closePath(); return p; }
function pSuave(pts, cerrado = true, tension = 1) {   // curva que pasa por todos los puntos (Catmull-Rom)
  const p = new Path2D(), n = pts.length, get = i => cerrado ? pts[(i + n) % n] : pts[Math.max(0, Math.min(n - 1, i))];
  p.moveTo(pts[0][0], pts[0][1]);
  for (let i = 0; i < (cerrado ? n : n - 1); i++) {
    const a = get(i - 1), b = get(i), c = get(i + 1), d = get(i + 2), k = tension / 6;
    p.bezierCurveTo(b[0] + (c[0] - a[0]) * k, b[1] + (c[1] - a[1]) * k, c[0] - (d[0] - b[0]) * k, c[1] - (d[1] - b[1]) * k, c[0], c[1]);
  }
  if (cerrado) p.closePath(); return p;
}
function pEstrella(cx, cy, R, r, n = 5, rot = -Math.PI / 2) { const pts = []; for (let i = 0; i < n * 2; i++) { const a = rot + i * Math.PI / n, d = i % 2 ? r : R; pts.push([cx + Math.cos(a) * d, cy + Math.sin(a) * d]); } return pPoli(pts); }
function pCorazon(cx, cy, s) { const p = new Path2D(); p.moveTo(cx, cy + s * .95);
  p.bezierCurveTo(cx - s * 1.25, cy + s * .1, cx - s * 1.05, cy - s * .95, cx, cy - s * .4);
  p.bezierCurveTo(cx + s * 1.05, cy - s * .95, cx + s * 1.25, cy + s * .1, cx, cy + s * .95); p.closePath(); return p; }

// Relleno plano con contorno. sombra: número = todo lo que queda a la derecha de esa x va más oscuro;
// 'abajo:<y>' = debajo de esa y; Path2D = esa zona. brillo: [x, y, w, h] = reflejo claro redondeado.
function F(path, col, o = {}) {
  const g = _g; g.fillStyle = _reg(col); g.fill(path);
  if (o.sombra !== undefined && o.sombra !== null) {
    g.save(); g.clip(path); g.fillStyle = _reg(oscuro(col, o.k || .84));
    if (typeof o.sombra === 'number') g.fillRect(o.sombra, -2000, 4000, 4000);
    else if (typeof o.sombra === 'string') g.fillRect(-2000, parseFloat(o.sombra.split(':')[1]), 4000, 4000);
    else g.fill(o.sombra);
    g.restore();
  }
  if (o.brillo) { g.save(); g.clip(path); g.globalAlpha = _modo === 'pixel' ? 1 : .55; g.fillStyle = _reg(o.brilloCol || claro(col, .6)); g.fill(pRR(...o.brillo, Math.min(o.brillo[2], o.brillo[3]) / 2)); g.restore(); }
  if (o.linea !== false && _modo === 'vector') { g.lineJoin = g.lineCap = 'round'; g.strokeStyle = _tinta; g.lineWidth = _lw * (o.grosor || 1); g.stroke(path); }
}
// Línea de detalle (costuras, rayas, alambres). w = grosor relativo al contorno.
function L(path, col = null, w = .7) {
  const g = _g; g.lineJoin = g.lineCap = 'round'; g.strokeStyle = _reg(col || _tinta);
  g.lineWidth = _modo === 'pixel' ? Math.max(1.7 / _esc, _lw * w * .75) : _lw * w; g.stroke(path);
}
function pLinea(pts) { return pPoli(pts, false); }
// Texto dentro del objeto (el signo $ de un billete, la T del té…)
function T(txt, x, y, tam, col, peso = 800) { const g = _g; if (_modo === 'pixel' && tam * _esc < 9) return;   // en pixel, la letra diminuta es ruido
  g.fillStyle = _reg(col); g.font = `${peso} ${tam}px ${LETRA_LIMPIA}`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(txt, x, y); }

// ---------- dibujarObjeto ----------
const _cachePixel = new Map();
function dibujarObjeto(nombre, x, y, tam, o = {}) {
  const t = o.t || 0, estilo = o.estilo || 'vector', rot = o.rot || 0, anim = o.anim || null, tinta = o.tinta || TINTA_OBJ;
  let def = CATALOGO_OBJETOS[nombre];
  if (!def) { console.warn(`[objetos] no existe «${nombre}». Hay: ${objetosDisponibles().join(', ')}`); def = CATALOGO_OBJETOS['?']; }
  // animación de entrada / vida
  let s = 1, dy = 0, dx = 0, r = rot, alfa = 1, sx = 1, sy = 1;
  if (anim === 'aparece') { const k = prog(t, 0, .45); if (k <= 0) return; s = back(k); alfa = clamp(k * 3); r += (1 - easeOut(prog(t, 0, .6))) * -.25; }
  if (anim === 'entra-izq' || anim === 'entra-der') {   // entra deslizando, se frena, se inclina hacia atrás y se asienta
    const k = prog(t, 0, .55); if (k <= 0) return; const lado = anim === 'entra-izq' ? -1 : 1;
    dx = lado * (1 - easeOut(k)) * (W * .75); r += lado * (Math.sin(prog(t, .3, .85) * Math.PI) * .09 * (t < .85 ? 1 : 0) + (1 - easeOut(k)) * -.06);
  }
  if (anim === 'cae') {   // cae desde arriba, aplasta al tocar el piso y rebota
    const k = prog(t, 0, .42); if (k <= 0) return;
    dy = -(1 - k * k) * tam * 2.2;
    const golpe = prog(t, .42, .72); if (golpe > 0 && golpe < 1) { const a = Math.sin(golpe * Math.PI) * (1 - golpe); sy = 1 - .16 * a; sx = 1 + .12 * a; }
    if (t > .72) dy = -Math.abs(Math.sin(prog(t, .72, 1.02) * Math.PI)) * tam * .06;
  }
  if (anim === 'flota') dy = Math.sin(t * 2.2) * tam * .035;
  if (anim === 'late') s = 1 + .07 * Math.pow(Math.max(0, Math.sin(t * 5.5)), 6);
  const main = ctx, med = medidaObjeto(nombre);
  main.save(); main.globalAlpha *= alfa;
  // sombra de contacto en el piso (no gira ni flota con el objeto; se achica y aclara cuando el objeto sube)
  if (o.sombra !== false) sombraContacto(x + dx + (med.izq + med.der) / 2 / 100 * tam * s, y, (med.der - med.izq) / 2 / 100 * tam * s * sx, { altura: Math.max(0, -dy) / tam, tam });
  main.translate(x + dx, y + dy); main.rotate(r); main.scale(s * sx, s * sy);
  if (estilo === 'pixel') _dibujarPixel(nombre, def, tam, t, tinta);
  else { _g = main; _modo = 'vector'; _pal = null; _tinta = tinta; _esc = tam / 100; main.scale(_esc, _esc); _lw = 5.5 / _esc; def.dibujo(t); }
  main.restore();
  if (anim === 'brilla') for (let i = 0; i < 5; i++) {
    const f = (t * .9 + i / 5) % 1, a = hash2(i, 5) * Math.PI * 2, d = tam * (.35 + .25 * hash2(i, 9));
    estrellita(x + Math.cos(a) * d * .8, y - tam * .55 + Math.sin(a) * d * .6, tam * .06 * Math.sin(f * Math.PI), '255,236,150', Math.sin(f * Math.PI));
  }
}
// sombra de contacto de 2 capas: un halo ancho y suave + un núcleo oscuro y apretado justo donde el objeto toca
function sombraContacto(x, y, mitad, o = {}) {
  const alt = clamp(o.altura || 0, 0, 2), tam = o.tam || mitad * 2, k = 1 / (1 + alt * 1.6), g = ctx;
  if (mitad <= 1) return;
  g.save(); g.fillStyle = `rgba(30,20,40,${.13 * k})`; g.beginPath(); g.ellipse(x, y + tam * .012, mitad * 1.08 * (.6 + .4 * k), tam * .04 * (.6 + .4 * k), 0, 0, Math.PI * 2); g.fill();
  g.fillStyle = `rgba(30,20,40,${.2 * k * k})`; g.beginPath(); g.ellipse(x, y + tam * .006, mitad * .78 * k, tam * .018 * k, 0, 0, Math.PI * 2); g.fill(); g.restore();
}
// medida REAL de un objeto (se dibuja una vez fuera de pantalla y se mira dónde hay tinta). Unidades del objeto.
const _cacheMedida = new Map();
function medidaObjeto(nombre) {
  if (_cacheMedida.has(nombre)) return _cacheMedida.get(nombre);
  const def = CATALOGO_OBJETOS[nombre] || CATALOGO_OBJETOS['?'], E = 2, cw = 400 * E, ch = 180 * E;
  const c = document.createElement('canvas'); c.width = cw; c.height = ch; const g = c.getContext('2d', { willReadFrequently: true });
  const antes = [_g, _modo, _pal, _tinta, _esc, _lw];
  _g = g; _modo = 'vector'; _pal = null; _tinta = TINTA_OBJ; _esc = E; _lw = 5.5 / E;
  g.translate(cw / 2, 150 * E); g.scale(E, E); try { def.dibujo(1.3); } catch (e) {}
  [_g, _modo, _pal, _tinta, _esc, _lw] = antes;
  const d = g.getImageData(0, 0, cw, ch).data; let x0 = cw, x1 = 0, y0 = ch;
  for (let y = 0; y < ch; y += 2) for (let x = 0; x < cw; x += 2) if (d[(y * cw + x) * 4 + 3] > 40) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; }
  const m = x1 < x0 ? { izq: -def.ancho, der: def.ancho, arriba: -100 } : { izq: (x0 - cw / 2) / E, der: (x1 - cw / 2) / E, arriba: (y0 - 150 * E) / E };
  m.ancho = m.der - m.izq; m.alto = -m.arriba; _cacheMedida.set(nombre, m); return m;
}
// reparte objetos en una fila sin que se encimen: los achica parejo si no caben
function componerFila(nombres, o = {}) {
  const x0 = o.x0 ?? 90, x1 = o.x1 ?? W - 90, hueco = o.hueco ?? 30, tams = nombres.map((n, i) => Array.isArray(o.tam) ? o.tam[i] : (o.tam || 300));
  const anchos = nombres.map((n, i) => medidaObjeto(n).ancho / 100 * tams[i]);
  const total = anchos.reduce((a, b) => a + b, 0) + hueco * (nombres.length - 1), k = Math.min(1, (x1 - x0) / total);
  let x = (x0 + x1) / 2 - total * k / 2;
  return nombres.map((n, i) => { const m = medidaObjeto(n), w = anchos[i] * k, cx = x - m.izq / 100 * tams[i] * k; x += w + hueco * k; return { nombre: n, x: cx, tam: tams[i] * k }; });
}
// pixel: se dibuja chico, se ajustan los colores a la paleta que usó el objeto y se le pone contorno de 1 pixel
function _dibujarPixel(nombre, def, tam, t, tinta) {
  const px = Math.max(4, Math.round(tam / 38)), alto = Math.round(tam / px), ancho = Math.round(alto * 1.5);
  const cuadro = def.anima ? Math.floor(t * 8) : 0, clave = `${nombre}|${alto}|${cuadro}|${tinta}`;
  let spr = _cachePixel.get(clave);
  if (!spr) {
    spr = document.createElement('canvas'); spr.width = ancho; spr.height = alto + 2;
    const g = spr.getContext('2d', { willReadFrequently: true });
    _g = g; _modo = 'pixel'; _pal = new Set(); _tinta = tinta; _esc = alto / 108; _lw = 1 / _esc;
    g.translate(ancho / 2, alto); g.scale(_esc, _esc); def.dibujo(cuadro / 8);
    _pal.add(tinta.toLowerCase());
    _ajustarPaleta(spr, [..._pal].map(_rgb), _rgb(tinta));
    if (_cachePixel.size > 400) _cachePixel.clear();
    _cachePixel.set(clave, spr);
  }
  const m = ctx; m.imageSmoothingEnabled = false;
  m.drawImage(spr, -ancho * px / 2, -alto * px, ancho * px, (alto + 2) * px);
  m.imageSmoothingEnabled = true;
}
function _ajustarPaleta(c, pal, tinta, contorno = true) {
  const g = c.getContext('2d', { willReadFrequently: true }), W2 = c.width, H2 = c.height;
  const d = g.getImageData(0, 0, W2, H2), p = d.data, op = new Uint8Array(W2 * H2);
  for (let i = 0, j = 0; i < p.length; i += 4, j++) {
    if (p[i + 3] < 110) { p[i + 3] = 0; continue; }
    let m = 0, md = 1e9; for (let k = 0; k < pal.length; k++) { const q = pal[k], dd = (q[0] - p[i]) ** 2 + (q[1] - p[i + 1]) ** 2 + (q[2] - p[i + 2]) ** 2; if (dd < md) { md = dd; m = k; } }
    p[i] = pal[m][0]; p[i + 1] = pal[m][1]; p[i + 2] = pal[m][2]; p[i + 3] = 255; op[j] = 1;
  }
  if (contorno) for (let y = 0; y < H2; y++) for (let x = 0; x < W2; x++) {
    const j = y * W2 + x; if (op[j]) continue;
    if ((x > 0 && op[j - 1]) || (x < W2 - 1 && op[j + 1]) || (y > 0 && op[j - W2]) || (y < H2 - 1 && op[j + W2])) { const i = j * 4; p[i] = tinta[0]; p[i + 1] = tinta[1]; p[i + 2] = tinta[2]; p[i + 3] = 255; }
  }
  g.putImageData(d, 0, 0);
}

// ---------- escenario ----------
const _cacheEsc = new Map();
function escenario(nombre, t = 0, o = {}) {
  const estilo = o.estilo || 'vector';
  const fn = ESCENARIOS[nombre] || (console.warn(`[objetos] no existe el escenario «${nombre}»: uso «estudio». Hay: ${Object.keys(ESCENARIOS).join(', ')}`), ESCENARIOS.estudio);
  const paleta = Object.assign({}, KITS.generico.paleta, o.paleta || {});
  const clave = `${nombre}|${estilo}|${JSON.stringify(paleta)}`;
  let c = _cacheEsc.get(clave);
  if (!c) {
    const div = estilo === 'pixel' ? 6 : 1;
    c = document.createElement('canvas'); c.width = W / div; c.height = H / div;
    const g = c.getContext('2d', { willReadFrequently: true });
    _g = g; _modo = estilo; _pal = estilo === 'pixel' ? new Set() : null; _tinta = paleta.tinta || TINTA_OBJ; _esc = 1 / div; _lw = estilo === 'pixel' ? div : 5;
    g.scale(1 / div, 1 / div); fn(paleta);
    if (estilo !== 'pixel' && o.luz !== false) _luzYProfundidad(g);
    if (estilo === 'pixel') _ajustarPaleta(c, [..._pal].map(_rgb), _rgb(_tinta), false);
    _cacheEsc.set(clave, c);
  }
  ctx.save(); ctx.imageSmoothingEnabled = estilo !== 'pixel'; ctx.drawImage(c, 0, 0, W, H); ctx.restore();
  const vivo = ESCENARIOS_VIVOS[nombre];
  if (vivo && estilo !== 'pixel' && o.vivo !== false) { ctx.save(); _g = ctx; _modo = 'vector'; _pal = null; _tinta = paleta.tinta || TINTA_OBJ; _esc = 1; _lw = 5; vivo(t, paleta); ctx.restore(); }
}
// capa común a todos los escenarios vector: luz cálida arriba-izquierda, piso que se oscurece hacia el frente y viñeta suave
function _luzYProfundidad(g) {
  g.save(); g.setTransform(g.canvas.width / W, 0, 0, g.canvas.height / H, 0, 0);
  const luz = g.createRadialGradient(260, 520, 40, 260, 520, 1100); luz.addColorStop(0, 'rgba(255,246,225,.22)'); luz.addColorStop(1, 'rgba(255,246,225,0)');
  g.fillStyle = luz; g.fillRect(0, 0, W, H);
  const piso = g.createLinearGradient(0, PISO_Y, 0, H); piso.addColorStop(0, 'rgba(20,10,30,0)'); piso.addColorStop(1, 'rgba(20,10,30,.2)');
  g.fillStyle = piso; g.fillRect(0, PISO_Y, W, H - PISO_Y);
  const pared = g.createLinearGradient(0, PISO_Y - 260, 0, PISO_Y); pared.addColorStop(0, 'rgba(20,10,30,0)'); pared.addColorStop(1, 'rgba(20,10,30,.07)');
  g.fillStyle = pared; g.fillRect(0, PISO_Y - 260, W, 260);
  const v = g.createRadialGradient(W / 2, H * .45, H * .35, W / 2, H * .45, H * .8); v.addColorStop(0, 'rgba(20,10,30,0)'); v.addColorStop(1, 'rgba(20,10,30,.16)');
  g.fillStyle = v; g.fillRect(0, 0, W, H);
  g.restore();
}
// piso/mostrador donde se paran los objetos (todos los escenarios lo respetan)
const PISO_Y = 1330;

// ============================================================================
// ESCENARIO GENÉRICO
// ============================================================================
registrarEscenario('estudio', p => {
  const g = _g;
  g.fillStyle = _reg(p.pared); g.fillRect(0, 0, W, H);
  g.fillStyle = _reg(claro(p.pared, .35));                 // círculos grandes suaves detrás
  g.beginPath(); g.arc(160, 900, 300, 0, 7); g.fill(); g.beginPath(); g.arc(940, 620, 240, 0, 7); g.fill();
  g.fillStyle = _reg(p.piso); g.fillRect(0, PISO_Y, W, H - PISO_Y);
  g.fillStyle = _reg(oscuro(p.piso, .9)); g.fillRect(0, PISO_Y, W, 18);
  g.fillStyle = _reg(claro(p.piso, .25)); for (let i = 0; i < 6; i++) g.fillRect(0, PISO_Y + 90 + i * 110, W, 6);
}, (t, p) => {   // vivo: círculos suaves que suben muy despacio
  const g = _g; g.fillStyle = claro(p.pared, .55);
  for (let i = 0; i < 7; i++) { const f = (t * .04 + hash2(i, 3)) % 1, x = 80 + hash2(i, 7) * (W - 160) + Math.sin(t * .6 + i) * 18, y = PISO_Y - f * 700;
    g.globalAlpha = .35 * Math.sin(f * Math.PI); g.beginPath(); g.arc(x, y, 10 + hash2(i, 9) * 22, 0, 7); g.fill(); }
  g.globalAlpha = 1;
});

// ============================================================================
// CATALOGO_OBJETOS GENÉRICOS DE NEGOCIO (sirven a cualquier rubro)
// ============================================================================
registrarObjeto('?', () => {
  F(pRR(-40, -84, 80, 80, 14), '#e9e4f2', { sombra: 20 });
  T('?', 0, -44, 58, '#7b5cd6');
}, { ancho: 40 });

registrarObjeto('celular', t => {
  F(pRR(-28, -100, 56, 100, 12), '#2d2a3a', { sombra: 16 });
  F(pRR(-22, -93, 44, 84, 6), '#bfe6ff', { linea: false, sombra: 'abajo:-40', k: .93 });
  F(pRR(-8, -90, 16, 5, 2.5), '#2d2a3a', { linea: false });
  F(pRR(-16, -76, 26, 12, 5), '#ffffff', { linea: false });          // globos de chat
  F(pRR(-6, -58, 24, 12, 5), '#7b5cd6', { linea: false });
  F(pCorazon(0, -30, 9), '#ff5a6e', { linea: false });
}, { ancho: 30 });

registrarObjeto('laptop', () => {
  F(pRR(-46, -86, 92, 62, 6), '#cfd4dc', { sombra: 30 });
  F(pRR(-40, -80, 80, 50, 3), '#7fc8f8', { linea: false });
  [[-28, -44, 10, 12], [-14, -52, 10, 20], [0, -60, 10, 28], [14, -70, 10, 38]].forEach(([x, y, w, h]) => F(pRR(x, y, w, h, 2), '#ffffff', { linea: false }));
  F(pPoli([[-52, -24], [52, -24], [62, -4], [-62, -4]]), '#b7bdc7', { sombra: 34 });
  F(pRR(-14, -18, 28, 5, 2.5), '#9aa2ae', { linea: false });
}, { ancho: 58 });

registrarObjeto('calendario', () => {
  F(pRR(-44, -92, 88, 90, 10), '#ffffff', { sombra: 28 });
  const tapa = new Path2D(); tapa.roundRect(-44, -92, 88, 26, [10, 10, 0, 0]);
  F(tapa, '#ff6b6b', { sombra: 28 });
  F(pRR(-26, -100, 8, 18, 4), '#8a8fa0'); F(pRR(18, -100, 8, 18, 4), '#8a8fa0');
  for (let f = 0; f < 3; f++) for (let c = 0; c < 4; c++) {
    const x = -34 + c * 19, y = -58 + f * 17;
    F(pRR(x, y, 13, 11, 2.5), '#eef0f6', { linea: false });
    if (f * 4 + c < 6) L(pLinea([[x + 1, y + 1], [x + 12, y + 10]]), '#ff6b6b', .75), L(pLinea([[x + 12, y + 1], [x + 1, y + 10]]), '#ff6b6b', .75);
  }
  L(pEl(-34 + 2 * 19 + 6.5, -58 + 1 * 17 + 5.5, 11, 9), '#3fbf7f', .8);
}, { ancho: 46 });

registrarObjeto('bolsa-compra', () => {
  L(pEl(0, -70, 17, 20, 0, Math.PI, Math.PI * 2, false), '#b0406a', 1.6);
  F(pPoli([[-38, -72], [38, -72], [44, -2], [-44, -2]]), '#ff7aa2', { sombra: 20 });
  F(pPoli([[-38, -72], [38, -72], [39, -64], [-39, -64]]), '#ff9dbb', { linea: false });
  F(pEstrella(0, -36, 15, 7), '#ffffff', { linea: false });
}, { ancho: 46 });

registrarObjeto('billete', () => {
  _g.save(); _g.rotate(-.12);
  F(pRR(-48, -44, 96, 46, 5), '#5fae6a', { sombra: 'abajo:-10' });
  F(pRR(-54, -58, 96, 46, 5), '#7bc67b', { sombra: 'abajo:-24' });
  L(pRR(-48, -52, 84, 34, 3), '#4f9a5a', .5);
  F(pEl(-6, -35, 12, 12), '#a7dda4', { linea: false });
  T('$', -6, -35, 19, '#2f6b3a');
  _g.restore();
}, { ancho: 52 });

registrarObjeto('moneda', () => {
  F(pEl(0, -40, 40, 40), '#d9a21c');
  F(pEl(-3, -43, 37, 37), '#ffcc4d', { linea: false, brillo: [-26, -70, 18, 30] });
  L(pEl(-3, -43, 28, 28), '#d9a21c', .7);
  T('$', -3, -43, 36, '#b07d10');
}, { ancho: 40 });

registrarObjeto('estrella', () => {
  const e = pEstrella(0, -48, 50, 22);
  F(e, '#ffd23f', { sombra: 0, k: .88, grosor: 1.1 });
  F(pEl(-12, -58, 5, 9, -.4), '#fff4bf', { linea: false });
}, { ancho: 44 });

registrarObjeto('corazon', () => {
  F(pCorazon(0, -50, 46), '#ff5a6e', { sombra: 8, k: .86 });
  F(pEl(-20, -66, 7, 11, -.6), '#ffc3cb', { linea: false });
}, { ancho: 46 });

registrarObjeto('flecha', () => {
  _g.save(); _g.translate(0, -50); _g.rotate(-Math.PI / 5);
  F(pPoli([[-50, -10], [14, -10], [14, -28], [52, 0], [14, 28], [14, 10], [-50, 10]]), '#7b5cd6', { sombra: 'abajo:0', k: .85 });
  _g.restore();
}, { ancho: 44 });

registrarObjeto('check', () => {
  F(pEl(0, -46, 44, 44), '#3fbf7f', { sombra: 12, k: .88 });
  L(pLinea([[-20, -46], [-5, -30], [22, -62]]), '#ffffff', 2.2);
}, { ancho: 44 });

registrarObjeto('reloj', t => {
  F(pEl(-26, -84, 13, 11), '#ff8a5b'); F(pEl(26, -84, 13, 11), '#ff8a5b');
  F(pRR(-24, -14, 8, 14, 3), '#555a66'); F(pRR(16, -14, 8, 14, 3), '#555a66');
  F(pEl(0, -48, 40, 40), '#ff8a5b', { sombra: 14 });
  F(pEl(0, -48, 31, 31), '#ffffff', { linea: false });
  for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2; L(pLinea([[Math.cos(a) * 25, -48 + Math.sin(a) * 25], [Math.cos(a) * 28, -48 + Math.sin(a) * 28]]), '#555a66', .45); }
  const am = -Math.PI / 2 + t * 2.4, ah = -Math.PI / 2 + t * .2 + 1.1;
  L(pLinea([[0, -48], [Math.cos(ah) * 15, -48 + Math.sin(ah) * 15]]), TINTA_OBJ, 1);
  L(pLinea([[0, -48], [Math.cos(am) * 23, -48 + Math.sin(am) * 23]]), '#ff5a3c', .7);
  F(pEl(0, -48, 3.5, 3.5), TINTA_OBJ, { linea: false });
}, { ancho: 40, anima: true });

registrarObjeto('megafono', () => {
  F(pRR(-26, -44, 14, 34, 5), '#555a66', { sombra: 'abajo:-22' });          // agarradera
  F(pPoli([[-44, -70], [22, -96], [22, -26], [-44, -52]]), '#ff5a5a', { sombra: 'abajo:-58', k: .85 });
  F(pEl(22, -61, 12, 35), '#ffd7d7');
  F(pEl(24, -61, 6, 24), '#c93c3c', { linea: false });
  F(pRR(-54, -72, 14, 22, 5), '#ffffff');
  [0, 1, 2].forEach(i => L(pEl(34, -61, 18 + i * 12, 30 + i * 12, 0, -.6, .6, false), '#ff5a5a', .6));
}, { ancho: 44 });

registrarObjeto('lupa', () => {
  _g.save(); _g.translate(0, 0); _g.rotate(.6);
  F(pRR(-9, -46, 18, 50, 8), '#8a5a3b', { sombra: 0 });
  _g.restore();
  F(pEl(-10, -66, 34, 34), '#5d6b7a', { sombra: 8 });
  F(pEl(-10, -66, 25, 25), '#cfeeff', { linea: false });
  F(pEl(-20, -76, 7, 11, -.6), '#ffffff', { linea: false });
}, { ancho: 40 });

registrarObjeto('foco', t => {
  for (let i = 0; i < 7; i++) { const a = -Math.PI / 2 + (i - 3) * .42; L(pLinea([[Math.cos(a) * 46, -66 + Math.sin(a) * 46], [Math.cos(a) * 56, -66 + Math.sin(a) * 56]]), '#ffc93c', .9); }
  F(pSuave([[0, -104], [30, -92], [36, -66], [22, -40], [16, -26], [-16, -26], [-22, -40], [-36, -66], [-30, -92]]), '#ffe680', { sombra: 8, k: .9, brillo: [-24, -94, 12, 26] });
  L(pSuave([[-8, -30], [-8, -52], [0, -60], [8, -52], [8, -30]], false), '#e0a800', .5);
  F(pRR(-17, -26, 34, 22, 4), '#a8aebb', { sombra: 6 });
  L(pLinea([[-17, -19], [17, -19]]), '#6e7482', .5); L(pLinea([[-17, -12], [17, -12]]), '#6e7482', .5);
  F(pRR(-8, -5, 16, 5, 2), '#555a66');
}, { ancho: 30 });

registrarObjeto('regalo', () => {
  F(pEl(-15, -76, 16, 11, -.5), '#ffd23f'); F(pEl(15, -76, 16, 11, .5), '#ffd23f');
  F(pRR(-44, -60, 88, 58, 5), '#7b5cd6', { sombra: 16 });
  F(pRR(-50, -72, 100, 16, 5), '#9278e6', { sombra: 16 });
  F(pRR(-7, -72, 14, 70, 2), '#ffd23f', { linea: false }); L(pRR(-7, -72, 14, 70, 2), null, .5);
  F(pEl(0, -74, 7, 6), '#f0b800');
}, { ancho: 50 });

registrarObjeto('grafica', () => {
  F(pRR(-50, -96, 100, 94, 8), '#ffffff', { sombra: 34 });
  [[-38, -26, '#c9c2ec'], [-18, -42, '#b0a4e8'], [2, -58, '#9278e6'], [22, -78, '#7b5cd6']].forEach(([x, y, c]) => F(pRR(x, y, 15, -8 - y, 3), c, { linea: false }));
  L(pLinea([[-42, -12], [44, -12]]), '#a0a4b4', .5);
  L(pLinea([[-34, -36], [-12, -50], [8, -64], [36, -88]]), '#ff5a6e', .9);
  F(pPoli([[40, -92], [26, -90], [36, -80]]), '#ff5a6e', { linea: false });
}, { ancho: 50 });

registrarKit('generico', {
  nombre: 'Genérico de negocio',
  paleta: { fondo: '#eef0ff', pared: '#e3e6fb', piso: '#d6d9f2', acento: '#7b5cd6', acento2: '#ffb547', tinta: '#232033' },
  escenario: 'estudio',
  objetos: ['celular', 'laptop', 'calendario', 'bolsa-compra', 'billete', 'moneda', 'estrella', 'corazon', 'flecha', 'check', 'reloj', 'megafono', 'lupa', 'foco', 'regalo', 'grafica'],
});
