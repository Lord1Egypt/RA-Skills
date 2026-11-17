#!/usr/bin/env node
// corto.mjs — convierte un GUION POR ESCENAS en un corto de 30-90 s: cada escena es una pieza HTML de la skill,
// se renderizan en paralelo, se unen con transiciones, se queman los subtítulos y se mezclan voz y música.
//
// Uso:  node corto.mjs guion.json salida.mp4 [--paralelo 3] [--solo 2,3] [--sin-subtitulos] [--limpiar]
//   --solo 2,3   vuelve a renderizar solo esas escenas (las demás salen de la caché .corto-tmp/ junto al guion)
//   --limpiar    borra la caché al terminar
//
// guion.json (las rutas son relativas al guion):
// {
//   "fps": 30,
//   "voz": "voz.m4a",                 // opcional. La voz GRABADA de la persona. Si dura más que las escenas, la última se sostiene quieta.
//   "musica": null,                   // opcional. Pista de fondo: se repite, entra y sale con fundido y BAJA SOLA cuando hay voz.
//   "volumen_musica": 0.18,
//   "dur_transicion": 0.4,            // segundos de cada transición (0.35-0.5 se ve pro; tinta/pagina/pixel lucen mejor con 0.5-0.6)
//   "subtitulos": {
//     "activo": true,
//     "estilo": "caja" | "contorno",
//     "posicion": "auto" | "abajo-seguro" | "arriba-seguro",   // auto = por escena, la franja más vacía
//     "sincronia": "palabra" | "largo"  // palabra = transcribe la voz (Whisper local) y enciende cada palabra cuando se dice
//   },
//   "escenas": [
//     { "pieza": "escenas/01-gancho.html",   // una pieza de la skill (draw(frame), FRAMES, FPS)
//       "dur": 4.5,                           // lo que se ve la escena. Si la pieza es más corta, su último cuadro se queda quieto;
//                                             //   si es más larga, se acelera hasta 1.8× (encajar) o se corta.
//       "transicion": "corte" | "fundido" | "barrido-izq" | "barrido-arriba" | "zoom" | "circulo"
//                   | "tinta" | "pagina" | "pixel",           // cómo ENTRA esta escena (o cualquier nombre de xfade de ffmpeg)
//       "subtitulo": "lo que se dice en esta escena, tal cual",
//       "subtitulo_posicion": "arriba-seguro",                    // opcional, pisa la del guion
//       "encajar": false,                                         // opcional. Por defecto se acelera lo justo (hasta 1.8×).
//       "inicio": 0 }                                             // opcional: segundo de la voz en que empieza. Si TODAS lo traen,
//   ]                                                             //   la duración de cada escena sale de ahí (sincronía con la voz).
// }
//
// Cómo arma el video: cada escena y cada transición se vuelven SEGMENTOS (en paralelo) y al final se concatenan.
// Las transiciones de la skill (tinta, pagina, pixel) se dibujan en canvas: una máscara + adornos (borde de tinta,
// dorso de la página, bloques de luz), así que salen con bordes suaves y en milisegundos.
// Subtítulos: se dibujan en canvas (misma letra que las piezas) y se montan con overlay. No necesita libass.
// Sincronía por palabra: usa mlx-whisper (Apple Silicon, vía uvx) o openai-whisper si están instalados.
import { createRequire } from 'node:module';
import { spawn, execFileSync, spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync, rmSync, existsSync, statSync } from 'node:fs';
import { resolve, join, dirname, basename } from 'node:path';
import { fileURLToPath } from 'node:url';

const aqui = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const [guionArg, salidaArg] = args;
const op = n => { const i = args.indexOf(n); return i < 0 ? undefined : (args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : true); };
if (!guionArg || !salidaArg) { console.error('uso: node corto.mjs guion.json salida.mp4 [--paralelo 3] [--solo 2,3] [--sin-subtitulos]'); process.exit(1); }

const t0 = Date.now();
const G = JSON.parse(readFileSync(resolve(guionArg), 'utf8'));
const base = dirname(resolve(guionArg));
const rel = p => resolve(base, p);
const FPS = G.fps || 30, TR = G.dur_transicion ?? .4;
const XFADE = { fundido: 'fade', 'barrido-izq': 'slideleft', 'barrido-arriba': 'slideup', zoom: 'zoomin', circulo: 'circleopen' };
const PROPIAS = ['tinta', 'pagina', 'pixel'];          // transiciones dibujadas en canvas
const escenas = G.escenas || [];
if (!escenas.length) { console.error('El guion no tiene escenas.'); process.exit(1); }
for (const e of escenas) if (!existsSync(rel(e.pieza))) { console.error(`No encuentro la pieza: ${e.pieza}`); process.exit(1); }

const duracion = f => Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString().trim());
const vozDur = G.voz ? duracion(rel(G.voz)) : 0;
const ffmpeg = (a, etiqueta) => new Promise((ok, mal) => {
  const p = spawn('ffmpeg', ['-y', '-loglevel', 'error', ...a], { stdio: ['ignore', 'ignore', 'pipe'] });
  let err = ''; p.stderr.on('data', d => err += d);
  p.on('close', c => c === 0 ? ok() : mal(new Error(`ffmpeg falló (${etiqueta}):\n${err}`)));
});
const pool = async (tareas, n) => { const cola = [...tareas]; await Promise.all(Array.from({ length: Math.min(n, cola.length) }, async () => { while (cola.length) await cola.shift()(); })); };

// ---------- 1. tiempos, en CUADROS (así no se acumulan redondeos) ----------
const conInicio = escenas.every(e => typeof e.inicio === 'number');
escenas.forEach((e, i) => {
  if (conInicio) e.dur = i < escenas.length - 1 ? escenas[i + 1].inicio - e.inicio : (e.dur || 3);
  if (!(e.dur > 0)) { console.error(`La escena ${i + 1} no tiene una duración válida.`); process.exit(1); }
  const nombre = i === 0 ? 'corte' : (e.transicion || 'fundido');
  e.trNombre = nombre;
  e.propia = PROPIAS.includes(nombre);
  e.xf = nombre === 'corte' ? null : (e.propia ? 'propia' : (XFADE[nombre] || nombre));   // también acepta nombres crudos de xfade
});
let acumulado = 0;
escenas.forEach(e => { e.empieza = acumulado; acumulado += e.dur; });
if (vozDur > acumulado) { const ult = escenas[escenas.length - 1]; ult.dur += vozDur - acumulado + .4; acumulado = vozDur + .4; }
const TOTAL_F = Math.round(acumulado * FPS);
escenas.forEach((e, i) => { e.iniF = Math.round(e.empieza * FPS); });
escenas.forEach((e, i) => {
  e.durF = (i < escenas.length - 1 ? escenas[i + 1].iniF : TOTAL_F) - e.iniF;
  e.trF = e.xf ? Math.max(2, Math.min(Math.round(TR * FPS), Math.floor(e.durF / 2))) : 0;
});
escenas.forEach((e, i) => { e.clipF = e.durF + (escenas[i + 1]?.trF || 0); });
const TOTAL = TOTAL_F / FPS;

// ---------- 2. render de cada escena, en paralelo ----------
const tmp = join(base, '.corto-tmp'); mkdirSync(tmp, { recursive: true });
const solo = op('--solo') ? String(op('--solo')).split(',').map(n => Number(n) - 1) : null;
const PAR = Number(op('--paralelo') || 3);
const clipDe = i => join(tmp, `escena-${String(i + 1).padStart(2, '0')}.mp4`);
console.log(`Renderizando ${escenas.length} escenas (${PAR} a la vez)…`);
await pool(escenas.map((e, i) => () => new Promise((ok, mal) => {
  const out = clipDe(i);
  if (solo && !solo.includes(i) && existsSync(out)) return ok();
  const p = spawn(process.execPath, [join(aqui, 'renderizar.mjs'), rel(e.pieza), out, '--dur', String(e.clipF / FPS), '--callado', ...(e.encajar === false ? [] : ['--encajar'])], { stdio: ['ignore', 'pipe', 'pipe'] });
  let err = '', dijo = ''; p.stderr.on('data', d => err += d); p.stdout.on('data', d => dijo += d);
  p.on('close', c => {
    if (c !== 0) return mal(new Error(`escena ${i + 1} (${e.pieza}):\n${err}`));
    const enc = (dijo.match(/encajada a [\d.]+×/) || [''])[0];
    console.log(`  escena ${i + 1}/${escenas.length} lista (${(e.clipF / FPS).toFixed(2)} s) · ${basename(e.pieza)}${enc ? ' · ' + enc : ''}`);
    if (err.includes('⚠')) console.warn('  ' + err.trim());
    ok();
  });
})), PAR);

// ---------- navegador para dibujar subtítulos, máscaras y medir las franjas ----------
let chromium; for (const b of [join(aqui, '..') + '/', process.cwd() + '/']) { try { chromium = createRequire(b)('playwright-core').chromium; break; } catch {} }
const flags = { args: ['--allow-file-access-from-files', ...(process.platform === 'linux' ? ['--no-sandbox', '--disable-dev-shm-usage'] : [])] }   // en un servidor Linux (root) Chrome necesita --no-sandbox;
let nav; try { nav = await chromium.launch({ channel: 'chrome', ...flags }); } catch { nav = await chromium.launch(flags); }
const pag = await nav.newPage();
await pag.setContent('<canvas id="c" width="1080" height="1920"></canvas><canvas id="m" width="1080" height="1920"></canvas>');
const png = (b64, ruta) => writeFileSync(ruta, Buffer.from(b64, 'base64'));

// ---------- 3. posición del subtítulo: la franja más limpia de la escena ----------
// Prueba alturas desde abajo (encima de los 450 px que tapa Instagram) hasta arriba (debajo de los 250), en 3 cuadros
// de la escena, y mide la densidad de BORDES (texto y objetos tienen bordes; un fondo liso o una pantalla en blanco no).
// Gana la franja más limpia; a igualdad, las posiciones de siempre (abajo, luego arriba).
const SUB = G.subtitulos || {};
const conSubs = SUB.activo !== false && !op('--sin-subtitulos');
const Y_POS = { 'abajo-seguro': 1920 - 450 - 80, 'arriba-seguro': 250 + 80 };
const CANDIDATAS = [1390, 1300, 1210, 330, 420, 1120, 510, 1030, 600, 940, 690, 850, 780];
async function mejorAltura(i) {
  const e = escenas[i], cuadros = [Math.round(e.durF * .3), Math.round(e.durF * .65), e.durF - 1], peor = {};
  for (const f of cuadros) {
    const jpg = join(tmp, `mide-${i}-${f}.jpg`);
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', clipDe(i), '-vf', `select=eq(n\\,${f}),scale=270:480`, '-frames:v', '1', '-q:v', '3', jpg]);
    const b64 = readFileSync(jpg).toString('base64'); rmSync(jpg, { force: true });
    const m = await pag.evaluate(async ([b64, C]) => {
      const im = new Image(); im.src = 'data:image/jpeg;base64,' + b64; await im.decode();
      const c = document.createElement('canvas'); c.width = 270; c.height = 480; const x = c.getContext('2d', { willReadFrequently: true }); x.drawImage(im, 0, 0);
      const d = x.getImageData(0, 0, 270, 480).data, L = new Float32Array(270 * 480);
      for (let p = 0; p < L.length; p++) L[p] = .3 * d[p * 4] + .59 * d[p * 4 + 1] + .11 * d[p * 4 + 2];
      const out = {};
      for (const cy of C) {                       // franja de ~120 px de alto y 900 de ancho (a 1/4 de escala)
        // se mide renglón por renglón y cuenta el más cargado (un renglón de texto basta para chocar)
        const y0 = Math.round((cy - 80) / 4), y1 = Math.round((cy + 80) / 4), fila = [];
        for (let y = y0; y < y1; y++) { let b = 0; for (let xx = 23; xx < 247; xx++) { const p = y * 270 + xx;
          if (Math.abs(L[p] - L[p - 1]) > 18 || Math.abs(L[p] - L[p - 270]) > 18) b++; } fila.push(b / 224); }
        let max = 0; for (let k = 0; k + 3 <= fila.length; k++) max = Math.max(max, (fila[k] + fila[k + 1] + fila[k + 2]) / 3);
        out[cy] = max;
      }
      return out;
    }, [b64, CANDIDATAS]);
    for (const k in m) peor[k] = Math.max(peor[k] || 0, m[k]);
  }
  let mejor = null, costo = 1e9;
  CANDIDATAS.forEach((cy, k) => { const c = peor[cy] + k * .004; if (c < costo) { costo = c; mejor = cy; } });
  return { cy: mejor, ocupa: peor[mejor], abajo: peor[1390], arriba: peor[330] };
}
if (conSubs) for (const [i, e] of escenas.entries()) {
  if (!e.subtitulo) continue;
  const pedida = e.subtitulo_posicion || SUB.posicion || 'abajo-seguro';
  if (pedida !== 'auto') { e.cy = Y_POS[pedida] ?? Y_POS['abajo-seguro']; continue; }
  const r = await mejorAltura(i); e.cy = r.cy;
  const donde = r.cy === 1390 ? 'abajo' : r.cy === 330 ? 'arriba' : `a ${r.cy} px`;
  console.log(`  subtítulo escena ${i + 1}: ${donde} (bordes: abajo ${(r.abajo * 100).toFixed(0)}% · arriba ${(r.arriba * 100).toFixed(0)}% · elegida ${(r.ocupa * 100).toFixed(0)}%)${r.ocupa > .12 ? '  ⚠ no hay franja limpia: revisa ese cuadro' : ''}`);
}

// ---------- 4. subtítulos ----------
const quitaTildes = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '');
const norm = s => quitaTildes(s.toLowerCase()).replace(/[^a-z0-9ñ]/g, '');
// parte una frase en trozos parejos de ≤ 34 letras (nunca una palabra sola colgando), primero por la puntuación
function partir(txt) {
  const frases = txt.trim().split(/(?<=[.;:!?])\s+/), out = [];
  for (const f of frases) {
    const pal = f.split(/\s+/), n = Math.ceil(f.length / 34), meta = f.length / n; let cur = [];
    for (const p of pal) {
      const largo = [...cur, p].join(' ').length, quedan = pal.length - pal.indexOf(p);
      if (cur.length && largo > meta + 4 && quedan > 1 && cur.join(' ').length >= meta * .6) { out.push(cur.join(' ')); cur = []; }
      cur.push(p);
    }
    if (cur.length) out.push(cur.join(' '));
  }
  return out;
}

// Whisper local: tiempos de cada palabra de la voz. Caché por tamaño+fecha del audio.
function transcribir(voz) {
  const st = statSync(voz), cache = join(tmp, `palabras-${st.size}-${Math.round(st.mtimeMs)}.json`);
  if (existsSync(cache)) return JSON.parse(readFileSync(cache, 'utf8'));
  const dir = join(tmp, 'whisper'); mkdirSync(dir, { recursive: true });
  const intentos = [
    ['uvx', ['--offline', '--from', 'mlx-whisper', 'mlx_whisper', voz, '--model', 'mlx-community/whisper-large-v3-turbo']],
    ['uvx', ['--from', 'mlx-whisper', 'mlx_whisper', voz, '--model', 'mlx-community/whisper-large-v3-turbo']],
    ['whisper', [voz, '--model', 'small']],
  ];
  const comun = ['--language', 'es', '--word_timestamps', 'True', '--output_format', 'json', '--output_dir', dir, '--condition_on_previous_text', 'False', '--temperature', '0'];
  for (const [cmd, a] of intentos) {
    const extra = cmd === 'uvx' ? comun.map(s => s.startsWith('--') ? s.replace(/_/g, '-') : s) : comun;
    const r = spawnSync(cmd, [...a, ...extra], { encoding: 'utf8', timeout: 600000 });
    const j = join(dir, basename(voz).replace(/\.[^.]+$/, '') + '.json');
    if (r.status === 0 && existsSync(j)) {
      const d = JSON.parse(readFileSync(j, 'utf8'));
      const pal = d.segments.flatMap(s => s.words || []).map(w => ({ w: w.word.trim(), a: w.start, b: w.end }));
      if (pal.length) { writeFileSync(cache, JSON.stringify(pal)); console.log(`  voz transcrita con ${cmd === 'uvx' ? 'mlx-whisper' : 'openai-whisper'}: ${pal.length} palabras`); return pal; }
    }
  }
  return null;
}
// Alinea las palabras del guion (texto correcto) con las de Whisper (tiempos correctos): alineación global con huecos.
function alinear(guion, voz) {
  const n = guion.length, m = voz.length, S = Array.from({ length: n + 1 }, () => new Float32Array(m + 1)), P = Array.from({ length: n + 1 }, () => new Uint8Array(m + 1));
  const parecido = (a, b) => { if (a === b) return 2; if (!a || !b) return -1; if (a.length > 3 && (a.startsWith(b) || b.startsWith(a))) return 1.2;
    let comun = 0; for (let k = 0; k < Math.min(a.length, b.length); k++) if (a[k] === b[k]) comun++; return comun / Math.max(a.length, b.length) > .6 ? .8 : -1; };
  for (let i = 1; i <= n; i++) { S[i][0] = -i * .6; P[i][0] = 1; }
  for (let j = 1; j <= m; j++) { S[0][j] = -j * .3; P[0][j] = 2; }        // saltarse palabras de la voz cuesta poco (la voz dice más que el subtítulo)
  for (let i = 1; i <= n; i++) for (let j = 1; j <= m; j++) {
    const d = S[i - 1][j - 1] + parecido(guion[i - 1].k, voz[j - 1].k), u = S[i - 1][j] - .6, l = S[i][j - 1] - .3;
    if (d >= u && d >= l) { S[i][j] = d; P[i][j] = 0; } else if (u >= l) { S[i][j] = u; P[i][j] = 1; } else { S[i][j] = l; P[i][j] = 2; }
  }
  // el subtítulo es un tramo de la voz: se permite empezar y terminar en cualquier palabra de la voz
  let j = 0, mejor = -1e9; for (let jj = 0; jj <= m; jj++) if (S[n][jj] > mejor) { mejor = S[n][jj]; j = jj; }
  let i = n; const par = new Array(n).fill(-1);
  while (i > 0 && j > 0) { if (P[i][j] === 0) { if (guion[i - 1].k && voz[j - 1].k && (guion[i - 1].k === voz[j - 1].k || S[i][j] - S[i - 1][j - 1] > 0)) par[i - 1] = j - 1; i--; j--; } else if (P[i][j] === 1) i--; else j--; }
  return par;
}
const trozos = [];                                   // { texto, activa, desde, hasta, pos }
let modoPalabra = conSubs && SUB.sincronia === 'palabra' && G.voz;
let vozPal = null;
if (modoPalabra) { vozPal = transcribir(rel(G.voz)); if (!vozPal) { console.warn('  ⚠ no encontré Whisper (mlx-whisper o openai-whisper): subtítulos repartidos por largo. Ver cortos/LEEME.md'); modoPalabra = false; } }
if (conSubs) for (const e of escenas) {
  if (!e.subtitulo) continue;
  const ini = e.iniF / FPS + (e.trF ? e.trF / FPS * .5 : 0), fin = (e.iniF + e.durF) / FPS - .05;
  const pos = e.cy ?? Y_POS[e.subtitulo_posicion || SUB.posicion] ?? Y_POS['abajo-seguro'];
  if (!modoPalabra) {
    const partes = partir(e.subtitulo), total = partes.reduce((a, p) => a + p.length + 6, 0); let t = ini;
    partes.forEach(p => { const d = (fin - ini) * (p.length + 6) / total; trozos.push({ palabras: p.split(' '), activa: -1, desde: t, hasta: t + d, pos }); t += d; });
    continue;
  }
  // --- por palabra: tiempos reales de la voz, texto del guion ---
  const g = e.subtitulo.trim().split(/\s+/).map(w => ({ w, k: norm(w) }));
  const ventana = vozPal.filter(p => p.a >= e.empieza - .6 && p.a <= e.empieza + e.dur + .3).map(p => ({ ...p, k: norm(p.w) }));
  const par = alinear(g, ventana);
  g.forEach((x, k) => { if (par[k] >= 0) { x.a = ventana[par[k]].a; x.b = ventana[par[k]].b; } });
  // las que no casaron: repartidas entre sus vecinas que sí
  const conT = g.map((x, k) => x.a != null ? k : -1).filter(k => k >= 0);
  if (!conT.length) { g.forEach((x, k) => { x.a = ini + (fin - ini) * k / g.length; x.b = x.a + (fin - ini) / g.length; }); }
  else g.forEach((x, k) => {
    if (x.a != null) return;
    const antes = conT.filter(c => c < k).pop(), despues = conT.find(c => c > k);
    const ta = antes != null ? g[antes].b : ini, tb = despues != null ? g[despues].a : Math.min(fin, ta + .35 * (g.length - k));
    const huecos = (despues ?? g.length) - (antes ?? -1);
    x.a = ta + (tb - ta) * (k - (antes ?? -1) - 1) / Math.max(1, huecos - 1); x.b = x.a + .2;
  });
  // grupos de 2-5 palabras (≤ 24 letras), cortando después de la puntuación, sin dejar una sola al final
  const grupos = []; let cur = [];
  g.forEach((x, k) => {
    cur.push(x);
    const largo = cur.map(y => y.w).join(' ').length, sig = g[k + 1];
    const cierra = /[.,;:!?»]$/.test(x.w) && cur.length >= 2, lleno = cur.length >= 5 || (sig && largo + sig.w.length + 1 > 24);
    const quedan = g.length - k - 1;
    if ((cierra || lleno) && quedan !== 1) { grupos.push(cur); cur = []; }
  });
  if (cur.length) grupos.push(cur);
  grupos.forEach((gr, q) => {
    const desdeG = Math.max(ini, gr[0].a - .08), hastaG = q < grupos.length - 1 ? Math.max(desdeG + .25, grupos[q + 1][0].a - .08) : Math.min(fin, gr[gr.length - 1].b + .45);
    gr.forEach((x, k) => {
      const d = k ? Math.max(desdeG, x.a - .03) : desdeG, h = k < gr.length - 1 ? Math.max(d + .06, gr[k + 1].a - .03) : hastaG;
      if (h > d) trozos.push({ palabras: gr.map(y => y.w), activa: k, desde: d, hasta: Math.min(h, fin), pos });
    });
  });
}
for (let i = 0; i < trozos.length; i++) {
  const b64 = await pag.evaluate(([pal, activa, estilo, pos]) => {
    const c = document.getElementById('c'), x = c.getContext('2d'); x.clearRect(0, 0, 1080, 1920);
    const fam = '"Avenir Next", "Helvetica Neue", "Segoe UI", Arial, sans-serif', txt = pal.join(' ');
    let tam = activa >= 0 ? 70 : 62; x.font = `800 ${tam}px ${fam}`; while (x.measureText(txt).width > 900 && tam > 40) { tam -= 2; x.font = `800 ${tam}px ${fam}`; }
    const esp = x.measureText(' ').width, anchos = pal.map(p => x.measureText(p).width), w = anchos.reduce((a, b) => a + b, 0) + esp * (pal.length - 1);
    const cy = pos;
    x.textBaseline = 'middle'; x.textAlign = 'left'; x.lineJoin = 'round';
    if (estilo !== 'contorno') {
      const pw = w + 60, ph = tam * 1.55;
      x.fillStyle = 'rgba(18,16,22,.86)'; x.beginPath(); x.roundRect(540 - pw / 2, cy - ph / 2, pw, ph, 24); x.fill();
    }
    let px = 540 - w / 2;
    pal.forEach((p, k) => {
      const on = k === activa;
      if (on && estilo !== 'contorno') { x.fillStyle = '#ffd84d'; x.beginPath(); x.roundRect(px - 10, cy - tam * .62, anchos[k] + 20, tam * 1.24, 12); x.fill(); }
      if (estilo === 'contorno') { x.lineWidth = 14; x.strokeStyle = 'rgba(0,0,0,.92)'; x.strokeText(p, px, cy + 2); }
      x.fillStyle = on ? (estilo === 'contorno' ? '#ffd84d' : '#15131a') : '#ffffff';
      x.fillText(p, px, cy + 3);
      px += anchos[k] + esp;
    });
    return c.toDataURL('image/png').split(',')[1];
  }, [trozos[i].palabras, trozos[i].activa, SUB.estilo || 'caja', trozos[i].pos]);
  trozos[i].png = join(tmp, `sub-${String(i).padStart(3, '0')}.png`); png(b64, trozos[i].png);
}

// ---------- 5. transiciones propias: máscara (dónde se ve la escena nueva) + adornos, dibujados en canvas ----------
async function framesTransicion(nombre, n, dir, semilla) {
  mkdirSync(dir, { recursive: true });
  for (let f = 0; f < n; f++) {
    const [m, d] = await pag.evaluate(([nombre, p, semilla]) => {
      const W = 1080, H = 1920, mc = document.getElementById('m'), mx = mc.getContext('2d'), dc = document.getElementById('c'), dx = dc.getContext('2d');
      mx.fillStyle = '#000'; mx.fillRect(0, 0, W, H); dx.clearRect(0, 0, W, H); mx.fillStyle = '#fff';
      const e = p * p * (3 - 2 * p);                                  // suavizado
      const hash = (a, b) => { const s = Math.sin(a * 12.9898 + b * 78.233 + semilla * 3.1) * 43758.5453; return s - Math.floor(s); };
      if (nombre === 'tinta') {
        // una mancha grande que crece desde abajo del centro + gotas que se adelantan; borde de tinta oscuro
        const manchas = [[.5, .56, 1, 0], [.22, .27, .42, .08], [.8, .8, .36, .14], [.83, .2, .2, .22], [.14, .86, .18, .26]];
        const forma = (cx, cy, r, sem) => { const pts = []; for (let k = 0; k <= 90; k++) { const a = k / 90 * Math.PI * 2;
          const rr = r * (1 + .12 * Math.sin(7 * a + sem) + .06 * Math.sin(13 * a - sem * 2) + .04 * Math.sin(3 * a + sem * 5)); pts.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr]); } return pts; };
        const trazar = (c, pts) => { c.beginPath(); pts.forEach(([x, y], k) => k ? c.lineTo(x, y) : c.moveTo(x, y)); c.closePath(); };
        const formas = manchas.map(([u, v, esc, ret], k) => { const q = Math.max(0, (e - ret) / (1 - ret)); return forma(u * W, v * H, q * esc * 1420, semilla + k); }).filter(f => f.length);
        for (const f of formas) { trazar(mx, f); mx.fill(); }
        dx.strokeStyle = 'rgba(24,20,30,.95)'; dx.lineWidth = 30; dx.lineJoin = 'round';
        for (const f of formas) { trazar(dx, f); dx.stroke(); }
        // el borde queda solo POR FUERA de la unión de manchas: se borra la unión en UN solo trazado
        // (borrar mancha por mancha deja restos del suavizado donde se cruzan los bordes)
        dx.globalCompositeOperation = 'destination-out'; dx.fillStyle = '#000'; dx.beginPath();   // relleno opaco: borra el 100 %
        for (const f of formas) { f.forEach(([x, y], k) => k ? dx.lineTo(x, y) : dx.moveTo(x, y)); dx.closePath(); }
        dx.fill('nonzero'); dx.globalCompositeOperation = 'source-over';
        // salpicaduras chicas alrededor del frente
        dx.fillStyle = 'rgba(24,20,30,.95)';
        if (e > .05 && e < .9) for (let k = 0; k < 26; k++) { const a = hash(k, 1) * Math.PI * 2, r = e * 1420 * (1.05 + hash(k, 2) * .25), rad = 6 + hash(k, 3) * 16;
          const x = W * .5 + Math.cos(a) * r, y = H * .56 + Math.sin(a) * r; dx.beginPath(); dx.arc(x, y, rad * (1 - e), 0, 7); dx.fill(); }
      } else if (nombre === 'pixel') {
        // bloques de 60 px que se encienden en blanco y dejan ver la escena nueva, con barrido de arriba hacia abajo
        const B = 60, cols = W / B, filas = H / B;
        for (let by = 0; by < filas; by++) for (let bx = 0; bx < cols; bx++) {
          const clave = hash(bx, by) * .6 + by / filas * .4, umbral = e * 1.12;
          if (clave < umbral - .08) mx.fillRect(bx * B, by * B, B, B);
          else if (clave < umbral) { dx.fillStyle = 'rgba(255,255,255,.95)'; dx.fillRect(bx * B, by * B, B, B); dx.fillStyle = 'rgba(0,0,0,.12)'; dx.fillRect(bx * B + B - 6, by * B, 6, B); dx.fillRect(bx * B, by * B + B - 6, B, 6); }
        }
      } else if (nombre === 'pagina') {
        // se da vuelta la página desde el borde derecho: el doblez (línea inclinada) corre hacia la izquierda.
        // A la derecha del doblez ya se ve la escena nueva (con la sombra del papel); a la izquierda, el dorso de la hoja
        // que se levantó cae encima de la vieja.
        const X = y => W * (1.32 - 1.9 * e) - (y - H / 2) * .32;
        const pts = []; for (let y = -40; y <= H + 40; y += 40) pts.push([X(y), y]);
        const ancho = y => Math.min(Math.max(0, W - X(y)), 300) * (1 - Math.max(0, e - .8) * 2);   // cuánto dorso se ve
        // máscara: a la derecha del doblez, la escena nueva
        mx.beginPath(); mx.moveTo(W + 400, -40); pts.forEach(([x, y]) => mx.lineTo(x, y)); mx.lineTo(W + 400, H + 40); mx.closePath(); mx.fill();
        // sombra del papel sobre la escena nueva, pegada al doblez
        const gN = dx.createLinearGradient(X(H / 2), 0, X(H / 2) + 150, 0); gN.addColorStop(0, 'rgba(0,0,0,.42)'); gN.addColorStop(1, 'rgba(0,0,0,0)');
        dx.fillStyle = gN; dx.beginPath(); pts.forEach(([x, y], k) => k ? dx.lineTo(x, y) : dx.moveTo(x, y)); for (let k = pts.length - 1; k >= 0; k--) dx.lineTo(pts[k][0] + 150, pts[k][1]); dx.closePath(); dx.fill();
        // sombra que el dorso proyecta sobre la vieja
        const gV = dx.createLinearGradient(X(H / 2) - ancho(H / 2) - 70, 0, X(H / 2) - ancho(H / 2), 0); gV.addColorStop(0, 'rgba(0,0,0,0)'); gV.addColorStop(1, 'rgba(0,0,0,.30)');
        dx.fillStyle = gV; dx.beginPath(); pts.forEach(([x, y], k) => { const xx = x - ancho(y); k ? dx.lineTo(xx, y) : dx.moveTo(xx, y); }); for (let k = pts.length - 1; k >= 0; k--) dx.lineTo(pts[k][0] - ancho(pts[k][1]) - 70, pts[k][1]); dx.closePath(); dx.fill();
        // el dorso: papel con brillo en la curva
        const gD = dx.createLinearGradient(X(H / 2) - ancho(H / 2), 0, X(H / 2), 0); gD.addColorStop(0, '#efe9dd'); gD.addColorStop(.6, '#fdfbf6'); gD.addColorStop(.9, '#e2dbcc'); gD.addColorStop(1, '#cfc6b4');
        dx.fillStyle = gD; dx.beginPath(); pts.forEach(([x, y], k) => { const xx = x - ancho(y); k ? dx.lineTo(xx, y) : dx.moveTo(xx, y); }); for (let k = pts.length - 1; k >= 0; k--) dx.lineTo(pts[k][0], pts[k][1]); dx.closePath(); dx.fill();
        dx.strokeStyle = 'rgba(60,50,40,.25)'; dx.lineWidth = 3; dx.beginPath(); pts.forEach(([x, y], k) => k ? dx.lineTo(x, y) : dx.moveTo(x, y)); dx.stroke();
      }
      return [mc.toDataURL('image/png').split(',')[1], dc.toDataURL('image/png').split(',')[1]];
    }, [nombre, (f + .5) / n, semilla]);
    png(m, join(dir, `m${String(f).padStart(3, '0')}.png`)); png(d, join(dir, `d${String(f).padStart(3, '0')}.png`));
  }
}

// ---------- 6. segmentos: escena (sin lo que se come la transición) y transición, en paralelo ----------
const venc = ['-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-an'];
const segmentos = [], tareas = [];
for (const [i, e] of escenas.entries()) {
  if (e.trF) {
    const prev = escenas[i - 1], out = join(tmp, `tr-${String(i + 1).padStart(2, '0')}.mp4`), a = prev.durF, T = e.trF;
    const cortes = `[0:v]trim=start_frame=${a}:end_frame=${a + T},setpts=PTS-STARTPTS,format=yuv420p[a];[1:v]trim=end_frame=${T},setpts=PTS-STARTPTS,format=yuv420p[b]`;
    if (e.propia) {
      const dir = join(tmp, `tr-${String(i + 1).padStart(2, '0')}`);
      await framesTransicion(e.trNombre, T, dir, i * 1.7);
      tareas.push(() => ffmpeg(['-i', clipDe(i - 1), '-i', clipDe(i), '-framerate', String(FPS), '-i', join(dir, 'm%03d.png'), '-framerate', String(FPS), '-i', join(dir, 'd%03d.png'),
        '-filter_complex', `${cortes};[2:v]format=gray[m];[b]format=yuva420p[bb];[bb][m]alphamerge[bm];[a][bm]overlay=format=auto[x];[x][3:v]overlay=format=auto,format=yuv420p[v]`,
        '-map', '[v]', '-frames:v', String(T), ...venc, out], `transición ${i + 1}`));
    } else {
      tareas.push(() => ffmpeg(['-i', clipDe(i - 1), '-i', clipDe(i), '-filter_complex', `${cortes};[a][b]xfade=transition=${e.xf}:duration=${(T / FPS).toFixed(4)}:offset=0,format=yuv420p[v]`,
        '-map', '[v]', '-frames:v', String(T), ...venc, out], `transición ${i + 1}`));
    }
    segmentos.push(out);
  }
  const out = join(tmp, `seg-${String(i + 1).padStart(2, '0')}.mp4`), desde = e.trF, hasta = e.durF;
  tareas.push(() => ffmpeg(['-i', clipDe(i), '-vf', `trim=start_frame=${desde}:end_frame=${hasta},setpts=PTS-STARTPTS,format=yuv420p`, '-frames:v', String(hasta - desde), ...venc, out], `escena ${i + 1}`));
  segmentos.push(out);
}
await nav.close();
console.log(`Armando ${segmentos.length} segmentos…`);
await pool(tareas, 4);
writeFileSync(join(tmp, 'segmentos.txt'), segmentos.map(s => `file '${s}'`).join('\n'));

// ---------- 7. montaje final: segmentos + subtítulos + voz y música ----------
const entradas = ['-f', 'concat', '-safe', '0', '-i', join(tmp, 'segmentos.txt')], filtro = [];
let prev = '0:v', nIn = 1;
trozos.forEach((s, k) => {
  entradas.push('-i', s.png);
  filtro.push(`[${prev}][${nIn}:v]overlay=0:0:enable='between(t,${s.desde.toFixed(3)},${(s.hasta - .001).toFixed(3)})'[s${k}]`);
  prev = `s${k}`; nIn++;
});
filtro.push(`[${prev}]trim=duration=${TOTAL.toFixed(3)},setpts=PTS-STARTPTS[vout]`);
const mapa = ['-map', '[vout]'];
if (G.voz || G.musica) {
  const a = [];
  if (G.voz) { entradas.push('-i', rel(G.voz)); a.push(`[${nIn}:a]aresample=48000,pan=stereo|c0=c0|c1=c0,apad[voz0]`)   /* mono → estéreo sin perder 3 dB */; nIn++; }
  if (G.musica) {
    entradas.push('-stream_loop', '-1', '-i', rel(G.musica));
    a.push(`[${nIn}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=duration=${TOTAL.toFixed(3)},volume=${G.volumen_musica ?? .18},afade=t=in:d=1.2,afade=t=out:st=${Math.max(0, TOTAL - 1.2).toFixed(3)}:d=1.2[mus0]`); nIn++;
  }
  if (G.voz && G.musica) a.push('[voz0]asplit=2[voz][vozsc]', '[mus0][vozsc]sidechaincompress=threshold=0.06:ratio=5:attack=20:release=260:makeup=1[mus]', '[voz][mus]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[aout]');
  else a.push(`[${G.voz ? 'voz0' : 'mus0'}]anull[aout]`);
  filtro.push(...a); mapa.push('-map', '[aout]', '-c:a', 'aac', '-b:a', '192k');
}
const salida = resolve(salidaArg);
writeFileSync(join(tmp, 'filtro.txt'), filtro.join(';\n'));
console.log(`Uniendo ${escenas.length} escenas, ${trozos.length} subtítulos${G.voz ? ', la voz' : ''}${G.musica ? ' y la música' : ''}…`);
try {
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', ...entradas, '-filter_complex_script', join(tmp, 'filtro.txt'), ...mapa,
    '-t', TOTAL.toFixed(3), '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-color_range', 'tv', '-movflags', '+faststart', salida], { stdio: 'inherit' });
} catch { console.error(`ffmpeg falló. El filtro quedó en ${join(tmp, 'filtro.txt')}`); process.exit(1); }
if (op('--limpiar')) rmSync(tmp, { recursive: true, force: true });   // si no, queda de caché para --solo
console.log(`listo: ${salida}\n  duración ${duracion(salida).toFixed(2)} s · ${escenas.length} escenas · ${trozos.length} subtítulos${modoPalabra ? ' (por palabra)' : ''} · render ${((Date.now() - t0) / 1000).toFixed(1)} s`);
