// ============================================================================
// NÚCLEO de animacion-dibujada-f100k
// Cada cuadro se DIBUJA con código: sin imágenes, sin videos, sin librerías.
// Adaptado de iart-ai/javascript-animation-skills (MIT, ver scripts/LICENSE-iart-ai.txt).
//
// Contrato (render.mjs depende de él):
//   window.draw(frame)  es función PURA del número de cuadro (mismo cuadro = misma imagen)
//   window.FRAMES, window.FPS
// Nunca uses Math.random ni Date: usa rng(semilla) o hash2(a, b).
// Antes de este archivo la pieza define: W, H, FPS, DUR.
// ============================================================================
const FRAMES = Math.round(FPS * DUR);
const cv = document.getElementById('c');
cv.width = W; cv.height = H;
let ctx = cv.getContext('2d');

// Zona segura de Instagram en 9:16 (lo que no tapan la barra de arriba ni el caption de abajo)
const SEGURA = { top: 250, bottom: H - 450, left: 70, right: W - 70 };

// ---------- matemática ----------
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, t) => a + (b - a) * t;
const ease = t => { t = clamp(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const easeOut = t => 1 - Math.pow(1 - clamp(t), 3);
const back = t => { t = clamp(t); const c = 1.7; return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2); };
const prog = (t, a, b) => clamp((t - a) / (b - a));
function hash2(a, b) {
  let n = Math.imul(a | 0, 374761393) + Math.imul(b | 0, 668265263);
  n = Math.imul(n ^ (n >>> 13), 1274126177);
  return ((n ^ (n >>> 16)) >>> 0) / 4294967295;
}
function vnoise(x, y) {
  const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
  const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
  return lerp(lerp(hash2(xi, yi), hash2(xi + 1, yi), u), lerp(hash2(xi, yi + 1), hash2(xi + 1, yi + 1), u), v);
}
function rng(seed) { let a = seed | 0; return () => { a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

// ---------- trazo a mano ----------
let BOIL = 0;          // cambia cada BOIL_N cuadros: el "hervor" de la línea dibujada a mano
let WOBBLE = 1;        // 0 = línea limpia, 1 = pluma, 2+ = boceto suelto
function jit(x, y, seed, amp) {
  const s = seed * 13.37;
  return [
    x + (vnoise(x * .012 + s, y * .012) - .5) * 2 * amp + (vnoise(x * .09 + s, y * .09 + 7) - .5) * amp * .6,
    y + (vnoise(x * .012, y * .012 + s + 50) - .5) * 2 * amp + (vnoise(x * .09 + 3, y * .09 + s) - .5) * amp * .6,
  ];
}
function resample(pts, step = 9, closed = false) {
  const out = [], P = closed ? [...pts, pts[0]] : pts;
  for (let i = 0; i < P.length - 1; i++) {
    const [x0, y0] = P[i], [x1, y1] = P[i + 1], n = Math.max(1, Math.ceil(Math.hypot(x1 - x0, y1 - y0) / step));
    for (let k = 0; k < n; k++) out.push([lerp(x0, x1, k / n), lerp(y0, y1, k / n)]);
  }
  if (!closed) out.push(P[P.length - 1]);
  return out;
}
function tracePath(pts, closed) {
  ctx.beginPath();
  if (pts.length < 3) { ctx.moveTo(...pts[0]); pts.slice(1).forEach(p => ctx.lineTo(...p)); if (closed) ctx.closePath(); return; }
  const P = closed ? [...pts, pts[0], pts[1]] : pts;
  ctx.moveTo(...(closed ? [(P[0][0] + P[1][0]) / 2, (P[0][1] + P[1][1]) / 2] : P[0]));
  for (let i = 1; i < P.length - 1; i++) ctx.quadraticCurveTo(P[i][0], P[i][1], (P[i][0] + P[i + 1][0]) / 2, (P[i][1] + P[i + 1][1]) / 2);
  if (!closed) ctx.lineTo(...P[P.length - 1]); else ctx.closePath();
}
const J = (pts, seed, amp) => pts.map(([x, y]) => jit(x, y, BOIL + seed, amp * WOBBLE));
function ink(pts, o = {}) {
  const { w = 4, col = '#111', closed = false, amp = 2, seed = 0, passes = 2, alpha = 1 } = o;
  ctx.save(); ctx.lineCap = ctx.lineJoin = 'round';
  for (let p = 0; p < passes; p++) {
    ctx.globalAlpha = alpha * (p ? .45 : 1); ctx.strokeStyle = col; ctx.lineWidth = w * (p ? .55 : 1);
    tracePath(J(pts, seed + p * .41, amp * (p ? 1.4 : 1)), closed); ctx.stroke();
  }
  ctx.restore();
}
function fill(pts, col, o = {}) {
  const { amp = 1.6, seed = 0, alpha = 1 } = o;
  ctx.save(); ctx.globalAlpha = alpha; ctx.fillStyle = col;
  tracePath(J(pts, seed + .2, amp), true); ctx.fill(); ctx.restore();
}
function hatch(pts, o = {}) { // rayado paralelo recortado a una forma
  const { angle = -0.9, gap = 11, col = '#111', w = 1.6, alpha = .35, seed = 0 } = o;
  const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]);
  const cx = (Math.min(...xs) + Math.max(...xs)) / 2, cy = (Math.min(...ys) + Math.max(...ys)) / 2;
  const R = Math.hypot(Math.max(...xs) - Math.min(...xs), Math.max(...ys) - Math.min(...ys)) / 2 + 10;
  ctx.save(); tracePath(J(pts, seed, 1.5), true); ctx.clip();
  ctx.translate(cx, cy); ctx.rotate(angle);
  ctx.strokeStyle = col; ctx.lineWidth = w; ctx.globalAlpha = alpha; ctx.lineCap = 'round';
  for (let y = -R, i = 0; y < R; y += gap, i++) {
    const a = hash2(i, BOIL + seed * 7) * 4 - 2, b = hash2(i + 99, BOIL + seed * 7) * 4 - 2;
    ctx.beginPath(); ctx.moveTo(-R, y + a); ctx.quadraticCurveTo(0, y + (a + b), R, y + b); ctx.stroke();
  }
  ctx.restore();
}
function drawOn(pts, p, o = {}) { const n = Math.max(2, Math.round(pts.length * clamp(p))); if (p > 0) ink(pts.slice(0, n), o); }

// ---------- formas ----------
const circle = (cx, cy, r, ry = r, rot = 0) => {
  const n = Math.max(20, Math.round(Math.max(r, ry) * .45)), out = [];
  for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2, x = Math.cos(a) * r, y = Math.sin(a) * ry;
    out.push([cx + x * Math.cos(rot) - y * Math.sin(rot), cy + x * Math.sin(rot) + y * Math.cos(rot)]); }
  return out;
};
const rect = (x, y, w, h) => resample([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], 12, true);
const line = (x0, y0, x1, y1) => resample([[x0, y0], [x1, y1]], 10);
const arc = (cx, cy, r, a0, a1, ry = r) => { const n = Math.max(8, Math.round(Math.abs(a1 - a0) * r / 9)), o = [];
  for (let i = 0; i <= n; i++) { const a = lerp(a0, a1, i / n); o.push([cx + Math.cos(a) * r, cy + Math.sin(a) * ry]); } return o; };
const roundRect = (x, y, w, h, r) => resample([
  ...arc(x + w - r, y + r, r, -Math.PI / 2, 0), ...arc(x + w - r, y + h - r, r, 0, Math.PI / 2),
  ...arc(x + r, y + h - r, r, Math.PI / 2, Math.PI), ...arc(x + r, y + r, r, Math.PI, Math.PI * 1.5)], 10, true);
function glow(x, y, r, rgb, a) {
  ctx.save(); const g = ctx.createRadialGradient(x, y, 0, x, y, r);
  g.addColorStop(0, `rgba(${rgb},${a})`); g.addColorStop(1, `rgba(${rgb},0)`);
  ctx.fillStyle = g; ctx.fillRect(x - r, y - r, 2 * r, 2 * r); ctx.restore();
}

// ---------- herramienta mágica: escribe SOLA, sin mano ni brazo ----------
// Regla de la skill: nada de anatomía dibujada en vector (manos, brazos, dedos, caras realistas): sale deforme.
// Lo que escribe flota, con brillo y chispas. Es pequeño y queda ARRIBA A LA DERECHA de la punta:
// nunca tapa lo ya escrito. Aparece y se va con un destello, no entra deslizándose desde fuera del cuadro.
//   px, py: dónde está la punta · aparece: 0→1 · se va: 0→1 · t: segundos
//   o.tipo: 'tiza' | 'plumon' · o.col: color del cuerpo · o.punta: color de la punta · o.brillo: 'r,g,b'
function herramientaMagica(px, py, t, aparece, seVa, o = {}) {
  const tipo = o.tipo || 'tiza', brillo = o.brillo || '255,236,170';
  const vis = clamp(aparece) * (1 - clamp(seVa));
  // destello al aparecer y al irse: anillo que se abre + estrellitas
  for (const [k, s] of [[aparece, 1], [seVa, 2]]) if (k > 0 && k < 1) {
    const r = 30 + k * 120; ctx.save(); ctx.globalAlpha = (1 - k) * .9; ctx.strokeStyle = `rgb(${brillo})`; ctx.lineWidth = 5 * (1 - k) + 1;
    ctx.beginPath(); ctx.arc(px + 40, py - 40, r, 0, Math.PI * 2); ctx.stroke(); ctx.restore();
    for (let i = 0; i < 8; i++) { const a = i / 8 * Math.PI * 2 + s, d = 40 + k * 150;
      estrellita(px + 40 + Math.cos(a) * d, py - 40 + Math.sin(a) * d, 14 * (1 - k) + 3, brillo, 1 - k); }
  }
  if (vis <= 0) return;
  // estela de chispas: posiciones pasadas de la punta no hacen falta; salen de la punta y suben flotando
  const f = Math.round(t * 30);
  for (let k = f - 18; k <= f; k++) { const dt = (f - k) / 30;
    for (let j = 0; j < 2; j++) { const h = hash2(k, j + 7); if (h < .45) continue;
      const x = px + (hash2(j, k) - .5) * 50 + (hash2(k, j) - .5) * 60 * dt, y = py - 10 - 90 * dt + (hash2(k + 3, j) - .5) * 30;
      estrellita(x, y, (4 + h * 7) * (1 - dt / .6), brillo, vis * (1 - dt / .6)); } }
  const flota = Math.sin(t * 5) * 4;
  ctx.save(); ctx.globalAlpha = vis; ctx.translate(px, py + flota);
  glow(0, 0, 70, brillo, .55); glow(55, -55, 110, brillo, .18);
  ctx.rotate(-Math.PI / 4);                         // cuerpo hacia arriba a la derecha, punta en el trazo
  const L = tipo === 'tiza' ? 120 : 150, A = tipo === 'tiza' ? 28 : 34;
  fill(roundRect(8, -A / 2 + 10, L, A, A / 2.4), 'rgba(0,0,0,.22)', { amp: .4, seed: 91 });   // sombra
  if (tipo === 'tiza') {
    fill(roundRect(0, -A / 2, L, A, 11), o.col || '#f4f1e8', { amp: .5, seed: 92 });
    fill(roundRect(0, -A / 2, 24, A, 10), o.punta || '#ffffff', { amp: .4, seed: 93 });
    fill(roundRect(30, -A / 2 + 4, L - 44, 6, 3), 'rgba(255,255,255,.55)', { amp: .3, seed: 94 });
  } else {
    fill(roundRect(28, -A / 2, L - 28, A, 12), o.col || '#243a7a', { amp: .5, seed: 92 });
    fill(roundRect(L - 44, -A / 2 - 3, 44, A + 6, 12), 'rgba(0,0,0,.25)', { amp: .4, seed: 95 });   // tapa trasera
    fill(resample([[4, -8], [30, -A / 2 + 3], [30, A / 2 - 3], [4, 8]], 5, true), '#1c2b59', { amp: .3, seed: 96 });
    fill(circle(2, 0, 8), o.punta || '#2f5fc4', { amp: .3, seed: 97 });
    fill(roundRect(40, -A / 2 + 5, L - 90, 6, 3), 'rgba(255,255,255,.35)', { amp: .3, seed: 94 });
  }
  ctx.restore();
}
function estrellita(x, y, r, rgb, a) {               // estrella de 4 puntas
  if (r <= 0 || a <= 0) return;
  ctx.save(); ctx.globalAlpha *= clamp(a); ctx.fillStyle = `rgb(${rgb})`; ctx.beginPath();
  for (let i = 0; i < 8; i++) { const ang = i / 8 * Math.PI * 2, d = i % 2 ? r * .28 : r; ctx.lineTo(x + Math.cos(ang) * d, y + Math.sin(ang) * d); }
  ctx.closePath(); ctx.fill(); ctx.restore();
}

// ---------- papel (se pinta UNA vez; luego se copia en cada cuadro) ----------
function hacerPapel(color, { grano = true, fibras = true, viñeta = .13, semilla = 7 } = {}) {
  const c = document.createElement('canvas'); c.width = W; c.height = H;
  const p = c.getContext('2d'), r = rng(semilla);
  p.fillStyle = color; p.fillRect(0, 0, W, H);
  if (grano) for (let i = 0; i < W * H / 14; i++) { p.fillStyle = r() < .5 ? 'rgba(90,70,50,0.05)' : 'rgba(255,255,255,0.08)'; p.fillRect(r() * W, r() * H, 1 + r() * 1.5, 1 + r() * 1.5); }
  if (fibras) { p.strokeStyle = 'rgba(120,95,70,0.06)'; p.lineWidth = 1;
    for (let i = 0; i < 480; i++) { const x = r() * W, y = r() * H, a = r() * 6.28, l = 6 + r() * 22;
      p.beginPath(); p.moveTo(x, y); p.quadraticCurveTo(x + Math.cos(a) * l / 2 + 3, y + Math.sin(a) * l / 2, x + Math.cos(a) * l, y + Math.sin(a) * l); p.stroke(); } }
  if (viñeta) { const g = p.createRadialGradient(W / 2, H / 2, Math.min(W, H) * .35, W / 2, H / 2, Math.max(W, H) * .75);
    g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, `rgba(60,40,20,${viñeta})`); p.fillStyle = g; p.fillRect(0, 0, W, H); }
  return c;
}

// ---------- texto ----------
// Fuentes del sistema (cero descargas). En Mac existen todas; en Windows cae a la siguiente de la lista.
const LETRA_MANO = '"Marker Felt", "Chalkboard SE", "Segoe Print", "Comic Sans MS", cursive';
const LETRA_LIMPIA = '"Avenir Next", "Helvetica Neue", "Segoe UI", Arial, sans-serif';
function medir(texto, font) { ctx.save(); ctx.font = font; const w = ctx.measureText(texto).width; ctx.restore(); return w; }
// Parte un texto en renglones que caben en `ancho`.
// Solo corta en espacios normales: un espacio duro ( ) mantiene juntas dos palabras («10 kg»).
function renglones(texto, font, ancho) {
  const out = []; let cur = '';
  for (const pal of texto.trim().split(/[ \t\n]+/)) { const prueba = cur ? cur + ' ' + pal : pal;
    if (medir(prueba, font) > ancho && cur) { out.push(cur); cur = pal; } else cur = prueba; }
  if (cur) out.push(cur); return out;
}
// Mismos renglones, pero parejos: el ancho más angosto que no agrega renglones (evita «Nadie / enseña la / derecha»)
function parejos(texto, font, ancho, n) {
  let lo = ancho * .35, hi = ancho;
  for (let i = 0; i < 14; i++) { const m = (lo + hi) / 2; if (renglones(texto, font, m).length <= n) hi = m; else lo = m; }
  return renglones(texto, font, hi);
}
// Elige tamaño y renglones (mide alto Y ancho). Prefiere MENOS renglones: acepta uno más solo si la letra crece ≥ 20 %.
// Si ni con tamMin cabe, avisa en consola (renderizar.mjs lo muestra) y devuelve desborda: true.
function autoajuste(texto, familia, peso, ancho, maxRenglones, tamMax, tamMin = 40) {
  const mejor = {};                                      // cantidad de renglones -> tamaño más grande con esa cantidad
  for (let s = tamMax; s >= tamMin; s -= 2) {
    const font = `${peso} ${s}px ${familia}`, rs = renglones(texto, font, ancho);
    if (rs.length <= maxRenglones && rs.every(r => medir(r, font) <= ancho) && !mejor[rs.length]) mejor[rs.length] = s;
  }
  const ns = Object.keys(mejor).map(Number).sort((a, b) => a - b);
  if (!ns.length) {
    console.error(`[autoajuste] «${texto}» no cabe en ${maxRenglones} renglones ni con letra de ${tamMin}px: acorta la frase.`);
    const font = `${peso} ${tamMin}px ${familia}`; return { font, size: tamMin, rs: renglones(texto, font, ancho), desborda: true };
  }
  let n = ns[0];
  for (const k of ns.slice(1)) if (mejor[k] >= mejor[n] * 1.2) n = k;
  const size = mejor[n], font = `${peso} ${size}px ${familia}`;
  return { font, size, rs: parejos(texto, font, ancho, n) };
}

// ---------- fotos reales (scrapbook, polaroid) ----------
// cargarFotos(['fotos/a.jpg', ...]) → promesa con las imágenes, en orden. Rutas relativas a la pieza.
// El render espera a window.LISTO antes del primer cuadro, así que nunca sale un cuadro sin foto.
function cargarFotos(rutas) {
  const p = Promise.all(rutas.map(src => new Promise((ok, mal) => {
    const im = new Image(); im.onload = () => ok(im); im.onerror = () => mal(new Error('No encontré la foto: ' + src)); im.src = src;
  })));
  window.LISTO = p; return p;
}
// cargarJSON('mi-ficha.json') → promesa con el objeto. Usa XHR porque fetch() no abre archivos locales (file://).
function cargarJSON(ruta) {
  return new Promise((ok, mal) => { const x = new XMLHttpRequest(); x.open('GET', ruta);
    x.onload = () => { try { ok(JSON.parse(x.responseText)); } catch (e) { mal(new Error('El JSON está mal escrito: ' + ruta)); } };
    x.onerror = () => mal(new Error('No encontré el archivo: ' + ruta)); x.send(); });
}
// Pinta una foto recortada tipo «cover» dentro de un rectángulo (sin deformarla). fx, fy = foco 0..1
function fotoCover(im, x, y, w, h, fx = .5, fy = .4) {
  const e = Math.max(w / im.width, h / im.height), sw = w / e, sh = h / e;
  ctx.drawImage(im, (im.width - sw) * fx, (im.height - sh) * fy, sw, sh, x, y, w, h);
}

// ---------- arranque ----------
window.FRAMES = FRAMES; window.FPS = FPS;
function arrancar(draw) {
  window.draw = draw;
  // vista previa en vivo al abrir con doble clic (render.mjs abre con ?render y se la salta)
  if (!new URLSearchParams(location.search).has('render')) (window.LISTO || Promise.resolve()).then(() => {
    const start = performance.now();
    const loop = () => { draw(Math.floor((performance.now() - start) / 1000 * FPS) % FRAMES); requestAnimationFrame(loop); };
    loop();
  });
}
