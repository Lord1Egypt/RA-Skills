#!/usr/bin/env node
// preparar-foto.mjs — deja lista una foto (o un dibujo) para animarla: la achica, la recorta del fondo
// y busca la cara. Todo local y gratis (sips + Vision de macOS 14+).
//
// Uso: node preparar-foto.mjs <foto> <carpeta-salida> [--sin-recorte]
// Deja en la carpeta:
//   <nombre>-recorte.png   la persona/objeto con fondo transparente (o la foto achicada si no hubo sujeto)
//   <nombre>-cara.json     cara, ojos y boca en pixeles del recorte (cara: null si no hay cara)
// --sin-recorte: para un PNG que YA viene transparente (un personaje de marca, un dibujo): solo busca la cara.
//
// Si Vision no le encuentra cara (pasa con mascotas y dibujos), escribe tú los ojos y la boca en el JSON:
//   { "ojoIzq": [x, y], "ojoDer": [x, y], "ojoAncho": 30, "boca": [x, y], "bocaAncho": 40, "bocaAlto": 14, "piel": "#f3c9a0" }
import { execFileSync } from 'node:child_process';
import { mkdirSync, writeFileSync, copyFileSync, existsSync, mkdtempSync, rmSync } from 'node:fs';
import { basename, extname, join, resolve, dirname } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';

const aqui = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const [foto, salida] = args.filter(a => !a.startsWith('--'));
const sinRecorte = args.includes('--sin-recorte');
if (!foto || !salida) { console.error('uso: node preparar-foto.mjs <foto> <carpeta-salida> [--sin-recorte]'); process.exit(1); }
if (!existsSync(foto)) { console.error('No existe la foto: ' + foto); process.exit(1); }
mkdirSync(salida, { recursive: true });
const nombre = basename(foto, extname(foto)).replace(/[^\w-]+/g, '-');
const tmp = mkdtempSync(join(tmpdir(), 'foto-'));
const chica = join(tmp, nombre + (sinRecorte ? '.png' : '.jpg'));
const recorte = resolve(salida, nombre + '-recorte.png');
const caraJson = resolve(salida, nombre + '-cara.json');
const swift = (script, ...a) => execFileSync('swift', [join(aqui, script), ...a], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();

// 1. achicar (1600 px del lado largo: sobra para 1080x1920 y Vision va más rápido)
const medida = execFileSync('sips', ['-g', 'pixelWidth', '-g', 'pixelHeight', foto], { encoding: 'utf8' }).match(/\d+/g).slice(-2).map(Number);
if (Math.max(...medida) > 1600) execFileSync('sips', ['-Z', '1600', foto, '--out', chica], { stdio: 'ignore' });   // sips -Z también agranda: solo si sobra
else execFileSync('sips', ['-s', 'format', sinRecorte ? 'png' : 'jpeg', foto, '--out', chica], { stdio: 'ignore' });

// 2. recortar del fondo
let hayRecorte = false;
if (sinRecorte) { execFileSync('sips', ['-s', 'format', 'png', chica, '--out', recorte], { stdio: 'ignore' }); hayRecorte = true; }
else {
  try { console.log(swift('recortar.swift', chica, recorte)); hayRecorte = true; }
  catch (e) {
    console.warn('⚠ No hubo recorte: ' + ((e.stdout || '') + (e.stderr || '')).trim().split('\n').pop());
    console.warn('  Sigo con la foto entera (sin fondo transparente).');
    execFileSync('sips', ['-s', 'format', 'png', chica, '--out', recorte], { stdio: 'ignore' });
  }
}

// 3. cara, ojos y boca sobre el recorte
let cara = null;
try {
  const salidaSwift = swift('cara.swift', recorte).split('\n').filter(l => l.startsWith('{')).pop();
  cara = JSON.parse(salidaSwift);
} catch (e) { console.warn('⚠ No pude buscar la cara: ' + ((e.stderr || e.message) + '').trim().split('\n').pop()); }
if (!cara) cara = { cara: null };
if (!cara.cara) console.warn('⚠ No encontré una cara. Si es un personaje o un dibujo, escribe a mano ojoIzq, ojoDer, boca… en ' + caraJson);
writeFileSync(caraJson, JSON.stringify(cara, (k, v) => typeof v === 'number' ? Math.round(v * 10) / 10 : v));
rmSync(tmp, { recursive: true, force: true });
console.log(`listo: ${hayRecorte ? 'recorte' : 'foto'} -> ${recorte}`);
console.log(`      cara  -> ${caraJson}${cara.cara ? '' : ' (sin cara)'}`);
