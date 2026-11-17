#!/usr/bin/env node
// hoja-corto.mjs — hoja de contacto de un corto ANTES de renderizarlo: una fila por escena con 3 cuadros
// (al entrar, a la mitad y el último que se ve), su tiempo en el corto, la transición y el subtítulo.
// Sirve para revisar el corto entero de un vistazo en ~10 s, sin esperar el MP4.
//
// Uso:  node hoja-corto.mjs guion.json hoja.jpg          (mismo guion.json que corto.mjs)
import { createRequire } from 'node:module';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { resolve, join, dirname, basename } from 'node:path';
import { fileURLToPath } from 'node:url';

const aqui = dirname(fileURLToPath(import.meta.url));
const [guionArg, salida] = process.argv.slice(2);
if (!guionArg || !salida) { console.error('uso: node hoja-corto.mjs guion.json hoja.jpg'); process.exit(1); }
const G = JSON.parse(readFileSync(resolve(guionArg), 'utf8'));
const base = dirname(resolve(guionArg)), rel = p => resolve(base, p);
const escenas = G.escenas || [];
const conInicio = escenas.every(e => typeof e.inicio === 'number');
const TR = G.dur_transicion ?? .4, SUB = G.subtitulos || {};
let t = 0;
escenas.forEach((e, i) => { if (conInicio) e.dur = i < escenas.length - 1 ? escenas[i + 1].inicio - e.inicio : (e.dur || 3); e.empieza = t; t += e.dur; });
// cada escena se renderiza con la transición de la que sigue debajo (igual que corto.mjs)
escenas.forEach((e, i) => { const sig = escenas[i + 1]; e.clip = e.dur + (sig && (sig.transicion || 'fundido') !== 'corte' ? TR : 0); });
const Y_POS = { 'abajo-seguro': 1390, 'arriba-seguro': 330 };
const CANDIDATAS = [1390, 1300, 1210, 330, 420, 1120, 510, 1030, 600, 940, 690, 850, 780];

let chromium; for (const b of [join(aqui, '..') + '/', process.cwd() + '/']) { try { chromium = createRequire(b)('playwright-core').chromium; break; } catch {} }
if (!chromium) { console.error('Falta playwright-core: corre `npm i` en la carpeta de la skill.'); process.exit(1); }
let nav; const flags = { args: ['--allow-file-access-from-files', ...(process.platform === 'linux' ? ['--no-sandbox', '--disable-dev-shm-usage'] : [])] }   // en un servidor Linux (root) Chrome necesita --no-sandbox;
try { nav = await chromium.launch({ channel: 'chrome', ...flags }); } catch { nav = await chromium.launch(flags); }

const filas = [];
for (const [i, e] of escenas.entries()) {
  if (!existsSync(rel(e.pieza))) { console.error(`No encuentro la pieza: ${e.pieza}`); process.exit(1); }
  const pag = await nav.newPage(); const errores = []; pag.on('pageerror', x => errores.push(x.message));
  await pag.goto('file://' + rel(e.pieza) + '?render');
  await pag.evaluate(() => document.fonts && document.fonts.ready);
  try { await pag.evaluate(() => window.LISTO); } catch {}
  const info = await pag.evaluate(() => ({ FRAMES: window.FRAMES, FPS: window.FPS, QUIETO: typeof window.QUIETO === 'number' ? window.QUIETO : 1.4 }));
  if (!info.FRAMES) { console.error(`La escena ${i + 1} no define draw/FRAMES:`, errores); process.exit(1); }
  // encajar (misma cuenta que renderizar.mjs): si la acción no termina 0.35 s antes del corte, se acelera hasta 1.8×
  let vel = 1, falta = 0;
  if (e.encajar !== false) { const accion = info.FRAMES / info.FPS - info.QUIETO, cabe = e.clip - .35;
    if (accion > cabe && cabe > 0) { vel = Math.min(1.8, accion / cabe); if (accion / cabe > 1.8) falta = accion / cabe; } }
  const vis = Math.round(e.dur * info.FPS) - 1, real = f => Math.min(info.FRAMES - 1, Math.round(f * vel));   // cuadro de la pieza que se ve en el corto
  const cuadros = [Math.min(vis, Math.round(.6 * info.FPS)), Math.round(vis / 2), vis].map(real);
  const fotos = [];
  for (const f of cuadros) fotos.push(await pag.evaluate(f => { window.draw(f); return document.querySelector('canvas').toDataURL('image/jpeg', .85); }, f));
  // subtítulo: ¿dónde queda y choca con algo? (densidad de bordes en la franja, en 3 cuadros de la escena)
  let sub = null;
  if (e.subtitulo && SUB.activo !== false) {
    const medidas = await pag.evaluate(([fs, C]) => { const c = document.querySelector('canvas'), peor = {};
      for (const f of fs) { window.draw(f); const x = document.createElement('canvas'); x.width = 270; x.height = 480; const g = x.getContext('2d', { willReadFrequently: true }); g.drawImage(c, 0, 0, 270, 480);
        const d = g.getImageData(0, 0, 270, 480).data, L = new Float32Array(270 * 480); for (let p = 0; p < L.length; p++) L[p] = .3 * d[p * 4] + .59 * d[p * 4 + 1] + .11 * d[p * 4 + 2];
        for (const cy of C) { const y0 = Math.round((cy - 80) / 4), y1 = Math.round((cy + 80) / 4), fila = [];   // el renglón más cargado manda
          for (let y = y0; y < y1; y++) { let b = 0; for (let xx = 23; xx < 247; xx++) { const p = y * 270 + xx; if (Math.abs(L[p] - L[p - 1]) > 18 || Math.abs(L[p] - L[p - 270]) > 18) b++; } fila.push(b / 224); }
          let max = 0; for (let k = 0; k + 3 <= fila.length; k++) max = Math.max(max, (fila[k] + fila[k + 1] + fila[k + 2]) / 3);
          peor[cy] = Math.max(peor[cy] || 0, max); } }
      return peor; }, [[Math.round(vis * .3), Math.round(vis * .65), vis].map(real), CANDIDATAS]);
    let mejor = CANDIDATAS[0], costo = 1e9; CANDIDATAS.forEach((cy, k) => { const c = medidas[cy] + k * .004; if (c < costo) { costo = c; mejor = cy; } });
    const pedida = e.subtitulo_posicion || SUB.posicion || 'abajo-seguro';
    const cy = pedida === 'auto' ? mejor : (Y_POS[pedida] ?? 1390), ocupa = medidas[cy] ?? 0;
    sub = { cy, auto: pedida === 'auto', choca: ocupa > .12, sugerida: mejor };
  }
  filas.push({ i, e, fotos, vel, falta, sostiene: e.dur * info.FPS > info.FRAMES / vel ? e.dur - info.FRAMES / info.FPS / vel : 0, sub, errores });
  await pag.close();
}

// la hoja: cada fila = 3 miniaturas + ficha de la escena
const pag = await nav.newPage();
await pag.setContent('<canvas id="h"></canvas>');
const b64 = await pag.evaluate(async filas => {
  const TW = 216, TH = 384, PAD = 16, FICHA = 640, FW = PAD + 3 * (TW + PAD) + FICHA, FH = filas.length * (TH + PAD) + PAD;
  const c = document.getElementById('h'); c.width = FW; c.height = FH; const x = c.getContext('2d');
  x.fillStyle = '#16141b'; x.fillRect(0, 0, FW, FH);
  const carga = s => new Promise(ok => { const im = new Image(); im.onload = () => ok(im); im.src = s; });
  const fam = '"Avenir Next", "Helvetica Neue", Arial, sans-serif';
  const envolver = (txt, ancho) => { const out = []; let cur = ''; for (const p of txt.split(' ')) { const pr = cur ? cur + ' ' + p : p; if (x.measureText(pr).width > ancho && cur) { out.push(cur); cur = p; } else cur = pr; } if (cur) out.push(cur); return out; };
  for (const [k, f] of filas.entries()) {
    const y = PAD + k * (TH + PAD);
    for (const [j, s] of f.fotos.entries()) { const im = await carga(s); x.drawImage(im, PAD + j * (TW + PAD), y, TW, TH);
      if (f.sub) { x.save(); x.setLineDash([6, 4]); x.lineWidth = 2; x.strokeStyle = f.sub.choca ? '#ff6a52' : '#ffd84d';    // dónde va el subtítulo
        x.strokeRect(PAD + j * (TW + PAD) + 10, y + TH * (f.sub.cy - 62) / 1920, TW - 20, TH * 124 / 1920); x.restore(); }
      // zona segura de Instagram (lo que tapa la interfaz), en rayas
      x.fillStyle = 'rgba(255,60,60,.22)'; x.fillRect(PAD + j * (TW + PAD), y, TW, TH * 250 / 1920); x.fillRect(PAD + j * (TW + PAD), y + TH * (1 - 450 / 1920), TW, TH * 450 / 1920); }
    const fx = PAD + 3 * (TW + PAD) + 8; let fy = y + 34;
    x.fillStyle = '#ffd84d'; x.font = `800 30px ${fam}`; x.fillText(`${k + 1} · ${f.e.empieza.toFixed(1)}–${(f.e.empieza + f.e.dur).toFixed(1)} s`, fx, fy); fy += 36;
    x.fillStyle = '#edeaf3'; x.font = `600 22px ${fam}`; x.fillText(f.e.pieza.split('/').pop(), fx, fy); fy += 30;
    x.fillStyle = '#a7a1b4'; x.font = `500 20px ${fam}`;
    x.fillText(`entra con: ${k ? (f.e.transicion || 'fundido') : '—'}   ·   dura ${f.e.dur.toFixed(1)} s`, fx, fy); fy += 28;
    if (f.sostiene > .05) { x.fillStyle = '#8fd3ff'; x.fillText(`último cuadro quieto ${f.sostiene.toFixed(1)} s`, fx, fy); fy += 28; }
    if (f.vel > 1.005 && !f.falta) { x.fillStyle = '#8fd3ff'; x.fillText(`encajada a ${f.vel.toFixed(2)}×: termina a tiempo`, fx, fy); fy += 28; }
    if (f.falta) { x.fillStyle = '#ff9f6b'; x.fillText(`necesita ${f.falta.toFixed(2)}× (tope 1.8×): se corta. Dale más tiempo`, fx, fy); fy += 28; }
    if (f.sub) { const donde = cy => cy === 1390 ? 'abajo' : cy === 330 ? 'arriba' : `a ${cy} px`;
      x.fillStyle = f.sub.choca ? '#ff6a52' : '#ffd84d';
      const msj = !f.sub.choca ? `subtítulo ${donde(f.sub.cy)}${f.sub.auto ? ' (auto)' : ''}: libre`
        : f.sub.sugerida !== f.sub.cy ? `subtítulo ${donde(f.sub.cy)} CHOCA → usa "auto" (iría ${donde(f.sub.sugerida)})`
        : `subtítulo ${donde(f.sub.cy)}: no hay franja libre en esta escena`;
      x.fillText(msj, fx, fy); fy += 28;
      if (f.sub.choca && f.sub.sugerida === f.sub.cy) { x.fillStyle = '#a7a1b4'; x.fillText('  → quita el subtítulo aquí o deja aire en la pieza', fx, fy); fy += 28; } }
    if (f.errores.length) { x.fillStyle = '#ff6a52'; x.fillText('errores: ' + f.errores[0].slice(0, 44), fx, fy); fy += 28; }
    if (f.e.subtitulo) { fy += 8; x.fillStyle = '#edeaf3'; x.font = `italic 500 20px ${fam}`;
      for (const r of envolver('«' + f.e.subtitulo + '»', FICHA - 30).slice(0, 7)) { x.fillText(r, fx, fy); fy += 26; } }
  }
  return c.toDataURL('image/jpeg', .88).split(',')[1];
}, filas.map(f => ({ ...f, e: { pieza: f.e.pieza, empieza: f.e.empieza, dur: f.e.dur, transicion: f.e.transicion, subtitulo: f.e.subtitulo } })));
writeFileSync(resolve(salida), Buffer.from(b64, 'base64'));
await nav.close();
console.log(`hoja del corto: ${escenas.length} escenas, ${t.toFixed(1)} s en total -> ${salida}`);
