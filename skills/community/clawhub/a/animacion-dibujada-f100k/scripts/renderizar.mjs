#!/usr/bin/env node
// renderizar.mjs — convierte una pieza HTML (cada cuadro dibujado en canvas) en MP4, fotos sueltas o una hoja de contacto.
//
// La pieza debe exponer: window.draw(frame), window.FRAMES, window.FPS.
// Se abre con ?render para que se salte su vista previa en vivo.
//
// Uso:
//   node renderizar.mjs pieza.html salida.mp4                 video completo (H.264, yuv420p, sin audio)
//   node renderizar.mjs pieza.html salida.mp4 --verde         igual, con fondo verde #00FF00 si la pieza lo soporta (window.VERDE)
//   node renderizar.mjs pieza.html foto --cuadros 0,2.5s,90   fotos sueltas (número de cuadro o segundos con «s»)
//   node renderizar.mjs pieza.html hoja.jpg --hoja 0.5        un cuadro cada 0.5 s en una sola imagen, con la hora estampada
//   node renderizar.mjs pieza.html salida.mp4 --dur 5.5       el video dura 5.5 s: si la pieza es más corta sostiene su último
//                                                             cuadro quieto; si es más larga, la corta (lo usa corto.mjs)
//   ... --dur 3 --encajar                                     si la animación no alcanza a terminar en 3 s, la acelera lo justo
//                                                             (hasta 1.8×) para que termine antes del corte; su «quieto final» se descuenta
//
// Necesita: Node 18+, ffmpeg y Google Chrome. `npm i` en la carpeta de la skill instala playwright-core.
import { createRequire } from 'node:module';
import { spawn, execFileSync } from 'node:child_process';
import { writeFileSync, readFileSync, mkdtempSync, rmSync } from 'node:fs';
import { resolve, join, dirname } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';

const aqui = dirname(fileURLToPath(import.meta.url));
let chromium;
for (const base of [join(aqui, '..') + '/', process.cwd() + '/']) {
  try { chromium = createRequire(base)('playwright-core').chromium; break; } catch {}
}
if (!chromium) { console.error('Falta playwright-core: corre `npm i` en la carpeta de la skill.'); process.exit(1); }

const args = process.argv.slice(2);
const [pieza, salida] = args;
const op = n => { const i = args.indexOf(n); return i < 0 ? undefined : (args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : true); };
if (!pieza || !salida) { console.error('uso: node renderizar.mjs pieza.html <salida> [--cuadros a,b] [--hoja seg] [--verde]'); process.exit(1); }

// ---------- criterio anti-deformación (antes de abrir Chrome) ----------
// La anatomía dibujada en vector (manos, brazos, dedos, caras realistas) sale deforme: bolas de piel con un palo encima.
// Si el código de la pieza pinta algo así, el render se detiene. Lo que escribe va solo y flota (herramientaMagica del núcleo).
// Excepción: personajes ESTILIZADOS donde la anatomía es una convención (cuerpo cuadrado, pixel art). Se declaran con
// una línea `// ANATOMIA: estilizada — <por qué>` en la pieza, y aun así se revisan a ojo en la hoja de contacto.
{
  const html = readFileSync(resolve(pieza), 'utf8');
  if (!/\/\/\s*ANATOMIA:\s*estilizada/.test(html)) {
    const codigo = (html.match(/<script(?![^>]*src)[^>]*>[\s\S]*?<\/script>/g) || []).join('\n').replace(/\ba mano\b/gi, '')
      // las FRASES (texto entre comillas) no dibujan nada: un guion de estética puede decir «la piel» sin frenar el render
      .replace(/'(?:[^'\\\n]|\\.)*'|"(?:[^"\\\n]|\\.)*"|`(?:[^`\\]|\\.)*`/g, "''").replace(/\/\*[\s\S]*?\*\//g, '').replace(/(^|[^:'"])\/\/.*$/gm, '$1').replace(/<!--[\s\S]*?-->/g, '');
    const hallado = [...new Set((codigo.match(/\b(manos?|brazos?|dedos?|muñecas?|codos?|hombros?|nudillos?|pulgar|piel|manga|rostro|nariz|orejas?)\b/gi) || []).map(x => x.toLowerCase()))];
    if (hallado.length) {
      console.error(`✋ Criterio anti-deformación: la pieza dibuja anatomía (${hallado.join(', ')}).\n` +
        '   Las manos y brazos en vector salen deformes. Haz que la herramienta escriba sola con herramientaMagica(...) del núcleo.\n' +
        '   Si es un personaje estilizado a propósito (cuadrito, pixel art), declara `// ANATOMIA: estilizada — <por qué>` y revísalo a ojo.');
      process.exit(1);
    }
  }
}

let nav;
// --allow-file-access-from-files: las fotos locales no «ensucian» el canvas y se puede exportar cada cuadro
const flags = { args: ['--allow-file-access-from-files', ...(process.platform === 'linux' ? ['--no-sandbox', '--disable-dev-shm-usage'] : [])] }   // en un servidor Linux (root) Chrome necesita --no-sandbox;
try { nav = await chromium.launch({ channel: 'chrome', ...flags }); } catch { nav = await chromium.launch(flags); }
const pag = await nav.newPage();
const errores = [];
pag.on('pageerror', e => errores.push(e.message));
pag.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errores.push(m.text()); });   // avisos de autoajuste y de las piezas
await pag.goto('file://' + resolve(pieza) + '?render' + (op('--verde') ? '&verde' : ''));
await pag.evaluate(() => document.fonts && document.fonts.ready);
try { await pag.evaluate(() => window.LISTO); } catch (e) { console.error('La pieza no pudo cargar sus fotos:', e.message); await nav.close(); process.exit(1); }
const info = await pag.evaluate(() => {
  const c = document.querySelector('canvas');
  return { FRAMES: window.FRAMES, FPS: window.FPS, w: c?.width, h: c?.height, ok: typeof window.draw === 'function' };
});
if (!info.ok || !info.FRAMES || !info.FPS) { console.error('La pieza debe definir window.draw(frame), window.FRAMES y window.FPS', errores); await nav.close(); process.exit(1); }

const foto = (f, marca) => pag.evaluate(([f, marca, fps]) => {
  window.draw(f);
  const src = document.querySelector('canvas');
  if (!marca) return src.toDataURL('image/jpeg', .93).split(',')[1];
  const c = document.createElement('canvas'); c.width = src.width; c.height = src.height;
  const x = c.getContext('2d'); x.drawImage(src, 0, 0);
  const s = Math.round(src.width / 14); x.fillStyle = 'rgba(0,0,0,.7)'; x.fillRect(0, 0, s * 3.2, s * 1.3);
  x.fillStyle = '#fff'; x.font = `700 ${Math.round(s * .8)}px monospace`; x.textBaseline = 'middle'; x.fillText((f / fps).toFixed(1) + 's', s * .25, s * .66);
  return c.toDataURL('image/jpeg', .9).split(',')[1];
}, [f, marca, info.FPS]).then(b => Buffer.from(b, 'base64'));

if (op('--cuadros')) {
  for (const v of String(op('--cuadros')).split(',').map(s => s.trim())) {
    const f = Math.min(info.FRAMES - 1, v.endsWith('s') ? Math.round(parseFloat(v) * info.FPS) : Number(v));
    const archivo = `${salida}-${String(f).padStart(4, '0')}.jpg`; writeFileSync(archivo, await foto(f)); console.log(archivo);
  }
} else if (op('--hoja')) {
  const cada = op('--hoja') === true ? 1 : Number(op('--hoja'));
  const cuadros = []; for (let t = cada / 2; t * info.FPS < info.FRAMES; t += cada) cuadros.push(Math.round(t * info.FPS));
  cuadros.push(info.FRAMES - 1);
  const dir = mkdtempSync(join(tmpdir(), 'hoja-'));
  for (let i = 0; i < cuadros.length; i++) writeFileSync(join(dir, `f${String(i).padStart(4, '0')}.jpg`), await foto(cuadros[i], true));
  const cols = Math.min(6, cuadros.length), filas = Math.ceil(cuadros.length / cols);
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', join(dir, 'f%04d.jpg'), '-vf', `scale=270:-2,tile=${cols}x${filas}`, '-frames:v', '1', salida]);
  rmSync(dir, { recursive: true });
  console.log(`hoja de contacto: ${cuadros.length} cuadros (cada ${cada}s) -> ${salida}`);
} else {
  if (info.w % 2 || info.h % 2) { console.error(`El lienzo mide ${info.w}x${info.h}: H.264 pide ancho y alto pares.`); await nav.close(); process.exit(1); }
  const out = /\.\w+$/.test(salida) ? salida : salida + '.mp4';
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(info.FPS), '-c:v', 'mjpeg', '-i', '-',
    // los JPEG llegan en rango completo (yuvj420p): se pasan a rango TV para que Instagram y el editor no los vean lavados
    '-vf', 'scale=in_range=full:out_range=tv,format=yuv420p', '-color_range', 'tv',
    '-c:v', 'libx264', '-crf', '18', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const TOTAL = op('--dur') ? Math.max(1, Math.round(Number(op('--dur')) * info.FPS)) : info.FRAMES;
  // encajar: la acción de la pieza (sin su quieto final, window.QUIETO o 1.4 s) tiene que terminar 0.35 s antes del corte
  let vel = 1;
  if (op('--dur') && op('--encajar')) {
    const quieto = await pag.evaluate(() => typeof window.QUIETO === 'number' ? window.QUIETO : 1.4);
    const accion = info.FRAMES / info.FPS - quieto, cabe = Number(op('--dur')) - .35;
    if (accion > cabe && cabe > 0) { vel = Math.min(1.8, accion / cabe); if (accion / cabe > 1.8) console.warn(`⚠ la escena necesita ${(accion / cabe).toFixed(2)}× y el tope es 1.8×: se corta antes de terminar. Dale más tiempo o acorta el texto.`); }
    if (vel > 1) console.log(`encajada a ${vel.toFixed(2)}×`);
  }
  let cerrado = false, codigo = null; const fin = new Promise(r => ff.on('close', c => { cerrado = true; codigo = c; r(); }));
  ff.on('error', e => { console.error('No arrancó ffmpeg:', e.message); process.exit(1); });
  ff.stdin.on('error', () => {});
  const t0 = Date.now();
  let ultimo = null;
  for (let f = 0; f < TOTAL && !cerrado; f++) {
    const fp = Math.round(f * vel);
    const img = fp < info.FRAMES ? (ultimo = await foto(fp)) : (ultimo ||= await foto(info.FRAMES - 1));   // pasado el final: el último cuadro, quieto
    if (!ff.stdin.write(img)) await Promise.race([new Promise(r => ff.stdin.once('drain', r)), fin]);
    if (f % (info.FPS * 2) === 0 && !op('--callado')) console.log(`cuadro ${f}/${TOTAL}`);
  }
  ff.stdin.end(); await fin;
  if (codigo !== 0) { console.error(`ffmpeg terminó con código ${codigo}; ${out} quedó incompleto`); await nav.close(); process.exit(1); }
  console.log(`listo: ${TOTAL} cuadros @ ${info.FPS}fps (${info.w}x${info.h}) en ${((Date.now() - t0) / 1000).toFixed(1)} s -> ${out}`);
}
if (errores.length) console.warn('errores de la página:', errores);
await nav.close();
