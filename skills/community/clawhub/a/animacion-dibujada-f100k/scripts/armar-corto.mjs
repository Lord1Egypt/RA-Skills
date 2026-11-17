#!/usr/bin/env node
// armar-corto.mjs — de un PLAN de escenas a un corto listo para corto.mjs (sin tocar código).
//
// Uso:  node armar-corto.mjs plan.json <carpeta>      → deja <carpeta>/escenas/*.html, la voz y <carpeta>/guion.json
//       node corto.mjs <carpeta>/guion.json <carpeta>/corto.mp4
//
// plan.json:
// {
//   "voz": "mi-voz.m4a",            (opcional) la voz grabada de la persona, con "inicio" en cada escena.
//                                    Sin voz: se genera una VOZ DE PRUEBA con `say` para medir tiempos. Nunca se entrega.
//   "voz_prueba": "Paulina",         voz de `say` para la prueba
//   "musica": null, "subtitulos": { "activo": true, "estilo": "caja", "posicion": "auto", "sincronia": "palabra" },
//   "escenas": [
//     { "estilo": "escena-personaje",                 un estilo de estilos/
//       "cambios": { "FRASE": "si yo llevara…",       lo que cambias del bloque «LO QUE PUEDES CAMBIAR».
//                    "ACCIONES": [ … ],               Texto, número, arreglo u objeto van tal cual (JSON).
//                    "COLORES": "js:{ …código JS… }" }, Con "js:" delante, se pega como código.
//       "dice": "lo que se dice en esta escena",      para la voz de prueba y los subtítulos por palabra
//       "subtitulo": "…" | false,                     (opcional) por defecto = "dice"; false = sin subtítulo
//       "transicion": "barrido-izq",                  corte | fundido | barrido-izq | barrido-arriba | zoom | circulo | tinta | pagina | pixel
//       "encajar": true,                              (opcional) acelera la escena si no termina a tiempo
//       "inicio": 0 }                                 (solo con voz grabada) segundo de la voz donde empieza
//   ]
// }
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { dirname, join, resolve, basename } from 'node:path';
import { fileURLToPath } from 'node:url';

const aqui = dirname(fileURLToPath(import.meta.url));
const [rutaPlan, carpeta] = process.argv.slice(2);
if (!rutaPlan || !carpeta) { console.error('uso: node armar-corto.mjs plan.json <carpeta>'); process.exit(1); }
const plan = JSON.parse(readFileSync(rutaPlan, 'utf8'));
const dest = resolve(carpeta);
mkdirSync(join(dest, 'escenas'), { recursive: true });

// Reemplaza «const K = …;» respetando corchetes, llaves y comillas (valores de varias líneas)
function cambiar(src, k, valor) {
  const m = new RegExp('^const ' + k + ' = ', 'm').exec(src);   // al inicio de línea: los comentarios también dicen «const FICHA = …»
  if (!m) throw new Error(`La constante ${k} no existe en el bloque editable`);
  let i = m.index + m[0].length, j = i, prof = 0;
  for (;;) {
    const ch = src[j];
    if ('[{('.includes(ch)) prof++;
    else if (']})'.includes(ch)) prof--;
    else if (ch === ';' && prof === 0) break;
    else if (`'"\``.includes(ch)) { const q = ch; j++; while (src[j] !== q) j += src[j] === '\\' ? 2 : 1; }
    j++;
  }
  const js = typeof valor === 'string' && valor.startsWith('js:') ? valor.slice(3) : JSON.stringify(valor, null, 2);
  return src.slice(0, i) + js + src.slice(j);
}

const dur = f => parseFloat(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString());
const escenas = [];
let t = 0;
const conVoz = !!plan.voz;
if (!conVoz) mkdirSync(join(dest, 'voz'), { recursive: true });
const lista = [];

plan.escenas.forEach((e, n) => {
  const nombre = `${String(n + 1).padStart(2, '0')}-${e.estilo}`;
  const pieza = join(dest, 'escenas', nombre + '.html');
  execFileSync('node', [join(aqui, 'armar.mjs'), e.estilo, pieza], { stdio: 'pipe' });
  let src = readFileSync(pieza, 'utf8');
  for (const [k, v] of Object.entries(e.cambios || {})) src = cambiar(src, k, v);
  writeFileSync(pieza, src);

  const esc = { pieza: 'escenas/' + nombre + '.html', transicion: n === 0 ? 'corte' : (e.transicion || 'barrido-izq') };
  const sub = e.subtitulo === undefined ? e.dice : e.subtitulo;
  if (sub) esc.subtitulo = sub;
  if (e.encajar) esc.encajar = true;
  if (conVoz) { if (e.inicio !== undefined) esc.inicio = e.inicio; if (e.dur) esc.dur = e.dur; }
  else {
    // voz de PRUEBA por escena, con un respiro al principio (entra la transición) y otro al final
    const aiff = join(dest, 'voz', `${n}.aiff`), wav = join(dest, 'voz', `${n}.wav`);
    execFileSync('say', ['-v', plan.voz_prueba || 'Paulina', '-r', '195', '-o', aiff, e.dice || ' ']);
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', aiff, '-af', 'adelay=250:all=1,apad=pad_dur=0.25', '-ar', '48000', '-ac', '1', wav]);
    const d = dur(wav); lista.push(`file '${wav}'`);
    esc.inicio = +t.toFixed(3); esc.dur = +d.toFixed(3); t += d;
  }
  escenas.push(esc);
  console.log(`escena ${n + 1}: ${e.estilo}${esc.dur ? ` · ${esc.dur.toFixed(1)} s` : ''}`);
});

let voz = plan.voz ? resolve(dirname(rutaPlan), plan.voz) : null;
if (!conVoz) {
  writeFileSync(join(dest, 'voz', 'lista.txt'), lista.join('\n') + '\n');
  voz = join(dest, 'voz-de-prueba.m4a');
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', join(dest, 'voz', 'lista.txt'), '-c:a', 'aac', '-b:a', '160k', voz]);
  escenas[escenas.length - 1].dur += 1.2;          // el cierre se queda un poquito más
}
const guion = {
  fps: 30, voz: basename(voz) === basename(voz) && voz.startsWith(dest) ? voz.slice(dest.length + 1) : voz,
  dur_transicion: plan.dur_transicion ?? 0.4,
  subtitulos: plan.subtitulos ?? { activo: true, estilo: 'caja', posicion: 'auto', sincronia: 'palabra' },
  escenas,
};
if (plan.musica) guion.musica = resolve(dirname(rutaPlan), plan.musica);
writeFileSync(join(dest, 'guion.json'), JSON.stringify(guion, null, 2));
console.log(`guion.json listo en ${dest}${conVoz ? '' : ` · voz de PRUEBA de ${t.toFixed(1)} s (cámbiala por la voz grabada antes de entregar)`}`);
console.log(`siguiente: node ${join(aqui, 'hoja-corto.mjs')} ${join(dest, 'guion.json')} ${join(dest, 'hoja.jpg')}`);
