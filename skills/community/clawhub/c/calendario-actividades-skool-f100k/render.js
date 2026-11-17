#!/usr/bin/env node
/**
 * Renderiza un calendario de actividades de Skool a PNG (estilo FÓRMULA 100K).
 *
 * Uso:
 *   node render.js <config.json> [--mes 5] [--anio 2026] [--tema alquimista-f100k]
 *                                [--out /ruta/salida.png] [--scale 2]
 *
 * - <config.json>: rutina semanal + horarios + eventos (ver plantillas/).
 * - --mes/--anio: si no se pasan, los toma del config (campo "mes"/"anio").
 * - --tema: carpeta dentro de themes/ (default: el campo "tema" del config o "alquimista-f100k").
 * - --out: ruta del PNG (default: entregables/calendarios-actividades/AAAA-MM_comunidad.png, relativo a donde corres el comando).
 *
 * Genera junto al PNG el .html editable usado para el render.
 */

const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');
const os = require('os');

// ---------- args ----------
const args = process.argv.slice(2);
if (args.length === 0 || args[0].startsWith('--')) {
  console.error('Uso: node render.js <config.json> [--mes N] [--anio N] [--tema NOMBRE] [--out RUTA] [--scale N]');
  process.exit(1);
}
const CONFIG_FILE = path.resolve(args[0]);
function getArg(name, def) { const i = args.indexOf(name); return i > -1 && args[i+1] ? args[i+1] : def; }

if (!fs.existsSync(CONFIG_FILE)) { console.error(`No existe el config: ${CONFIG_FILE}`); process.exit(1); }
const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));

const MES   = Number(getArg('--mes',  config.mes));
const ANIO  = Number(getArg('--anio', config.anio));
const TEMA  = getArg('--tema', config.tema || 'alquimista-f100k');
const SCALE = Number(getArg('--scale', 2));

if (!MES || !ANIO) { console.error('Falta --mes y/o --anio (o los campos "mes"/"anio" en el config).'); process.exit(1); }

const SKILL_DIR = __dirname;
const THEME_DIR = path.join(SKILL_DIR, 'themes', TEMA);
if (!fs.existsSync(THEME_DIR)) { console.error(`No existe el tema: ${TEMA} (en themes/)`); process.exit(1); }

// ---------- tema ----------
const theme = JSON.parse(fs.readFileSync(path.join(THEME_DIR, 'theme.json'), 'utf8'));
let bgDataUri = '';
if (theme.fondo) {
  const fondoPath = path.join(THEME_DIR, theme.fondo);
  if (fs.existsSync(fondoPath)) {
    const ext = path.extname(fondoPath).slice(1).toLowerCase();
    const mime = ext === 'png' ? 'image/png' : ext === 'webp' ? 'image/webp' : 'image/jpeg';
    bgDataUri = `data:${mime};base64,${fs.readFileSync(fondoPath).toString('base64')}`;
  } else {
    console.warn(`⚠ Fondo no encontrado (${theme.fondo}); se usa el fondo CSS del tema.`);
  }
}

// ---------- logo a dataURI (si el config trae ruta local) ----------
if (config.logo && !/^data:|^https?:/.test(config.logo)) {
  const logoPath = path.isAbsolute(config.logo) ? config.logo : path.join(path.dirname(CONFIG_FILE), config.logo);
  if (fs.existsSync(logoPath)) {
    const ext = path.extname(logoPath).slice(1).toLowerCase();
    const mime = ext === 'png' ? 'image/png' : ext === 'svg' ? 'image/svg+xml' : 'image/jpeg';
    config.logo = `data:${mime};base64,${fs.readFileSync(logoPath).toString('base64')}`;
  } else {
    console.warn(`⚠ Logo no encontrado (${config.logo}); se usa el fallback de iniciales.`);
    config.logo = '';
  }
}

// ---------- normalizar rutina: aplicar catálogo de tipos a cada sesión ----------
const CATALOGO = config.catalogoTipos || {};
function expandSesiones(arr) {
  return (arr || []).map(item => {
    if (typeof item === 'string') return { s: item, t: {} };
    const t = item.t || (item.tipo && CATALOGO[item.tipo]) || {};
    return { s: item.s || item.sesion, ic: item.ic || item.icono, t };
  });
}
const rutina = {};
Object.entries(config.rutinaSemanal || {}).forEach(([dow, arr]) => { rutina[dow] = expandSesiones(arr); });

const DATA = {
  month: MES, year: ANIO, bg: bgDataUri, theme,
  config: { ...config, rutinaSemanal: rutina }
};

// ---------- construir HTML ----------
const template = fs.readFileSync(path.join(SKILL_DIR, 'template.html'), 'utf8');
const inject = `<script>window.__DATA__ = ${JSON.stringify(DATA)};</script>`;
const html = template.replace('</head>', `${inject}\n</head>`);

// ---------- salida ----------
const comuSlug = (config.comunidad || 'comunidad').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const defOutDir = path.join(process.cwd(), 'entregables', 'calendarios-actividades');
const OUT = path.resolve(getArg('--out', path.join(defOutDir, `${ANIO}-${String(MES).padStart(2,'0')}_${comuSlug}.png`)));
fs.mkdirSync(path.dirname(OUT), { recursive: true });
const HTML_OUT = OUT.replace(/\.png$/i, '.html');
fs.writeFileSync(HTML_OUT, html);

// ---------- chrome ----------
const CHROME_CANDIDATES = [
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
  '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  process.env.CHROME_PATH,
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
  '/usr/bin/google-chrome',
].filter(Boolean);
const CHROME_PATH = CHROME_CANDIDATES.find(p => fs.existsSync(p));
if (!CHROME_PATH) { console.error('No se encontró Chrome/Chromium/Brave/Edge. Instala Google Chrome o define CHROME_PATH.'); process.exit(1); }

(async () => {
  console.log(`Tema: ${TEMA}  ·  Mes: ${MES}/${ANIO}  ·  Navegador: ${path.basename(CHROME_PATH)}`);
  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
    defaultViewport: { width: 2000, height: 1143, deviceScaleFactor: SCALE },
  });
  const page = await browser.newPage();
  await page.goto('file://' + HTML_OUT, { waitUntil: 'networkidle0' });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 1200));

  const el = await page.$('#cal');
  await el.screenshot({ path: OUT });
  await browser.close();

  console.log(`\n✅ PNG:  ${OUT}`);
  console.log(`📝 HTML: ${HTML_OUT}  (editable y re-renderizable)`);
})().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
