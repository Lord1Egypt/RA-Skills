#!/usr/bin/env node
/**
 * Arma un carrusel desde un JSON de slides y lo exporta a PNG.
 *
 * Uso:
 *   node build.js /ruta/spec.json [carpeta-salida] [--sin-png]     plantillas propias (split, papel, datos)
 *   node build.js /ruta/carrusel.html [--sin-png]                  HTML LIBRE (estilos de la guía maestra, S17–S28)
 *
 * HTML libre: lo escribe Claude siguiendo el contrato de references/plantillas.md (cada slide es un
 * `.slide` de 1080×1350). build.js no inyecta nada: abre la página, espera fuentes e imágenes y revisa
 * lo que ninguna plantilla garantiza ahí — texto que se sale del slide, fuentes que cayeron a Times,
 * slides de otro tamaño — antes de exportar.
 *
 * spec.json: { "plantilla": "split" | "papel" | "datos", "variante": "...", "handle": "@...", "slides": [...] }
 * (ver references/plantillas.md). Las rutas de fotos relativas se resuelven desde la carpeta del spec.
 *
 * 1) inyecta el spec y _comun.js en templates/<plantilla>.html → <salida>/carrusel.html
 * 2) abre la página, espera fuentes/imágenes/autofit y lee window.__reporte (texto que no cabe, fuente o imagen que no cargó)
 * 3) exporta con el export.js de carrusel-render-formula100k → <salida>/slide-NN.png a escala 2 (2160×2700),
 *    igual que las otras skills de carrusel: IG lo baja a 1080 pero el texto queda nítido en pantallas retina.
 */

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const puppeteer = cargarPuppeteer();
// puppeteer-core vive en la skill hermana carrusel-render-formula100k (la que trae export.js)
function cargarPuppeteer() {
  const candidatos = ['puppeteer-core', path.join(__dirname, '..', 'carrusel-render-formula100k', 'node_modules', 'puppeteer-core')];
  for (const c of candidatos) { try { return require(c); } catch {} }
  console.error('Falta puppeteer-core. Instálalo una vez:\n  cd "' + __dirname + '" && npm install');
  process.exit(1);
}

const args = process.argv.slice(2).filter(a => !a.startsWith('--'));
const SIN_PNG = process.argv.includes('--sin-png');
if (!args[0]) {
  console.error('Uso: node build.js <spec.json> [carpeta-salida] [--sin-png]');
  process.exit(1);
}

const ENTRADA = path.resolve(args[0]);
const LIBRE = ENTRADA.endsWith('.html');
const SPEC_FILE = ENTRADA;
const SPEC_DIR = path.dirname(SPEC_FILE);
const OUT_DIR = path.resolve(args[1] || SPEC_DIR);
const SKILL = __dirname;
const EXPORT_JS = [path.join(SKILL, 'export.js'), path.join(SKILL, '..', 'carrusel-render-formula100k', 'export.js')].find(p => fs.existsSync(p));

const spec = LIBRE ? null : JSON.parse(fs.readFileSync(SPEC_FILE, 'utf8'));
const plantilla = spec && spec.plantilla;
const tpl = path.join(SKILL, 'templates', `${plantilla}.html`);
if (!LIBRE && !fs.existsSync(tpl)) {
  console.error(`Plantilla desconocida: "${plantilla}". Usa split, papel o datos, o pasa un .html (HTML libre).`);
  process.exit(1);
}

// Rutas locales → file:// absolutas (las URLs http y data: se dejan igual)
const aUrl = p => {
  if (typeof p !== 'string' || /^(https?:|data:|file:)/.test(p)) return p;
  const abs = path.isAbsolute(p) ? p : path.join(SPEC_DIR, p);
  if (!fs.existsSync(abs)) console.warn(`⚠ no existe la imagen: ${abs}`);
  return 'file://' + encodeURI(abs);
};
const CLAVES_IMG = new Set(['foto', 'fondo', 'src', 'img']);
function resolver(o) {
  if (Array.isArray(o)) return o.map(resolver);
  if (o && typeof o === 'object') {
    for (const k of Object.keys(o)) {
      if (CLAVES_IMG.has(k) && typeof o[k] === 'string') o[k] = aUrl(o[k]);
      else if (k === 'fotos' && Array.isArray(o[k])) o[k] = o[k].map(f => (typeof f === 'string' ? aUrl(f) : resolver(f)));
      else o[k] = resolver(o[k]);
    }
  }
  return o;
}
let HTML_OUT = ENTRADA;
if (!LIBRE) {
  resolver(spec);
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const comun = fs.readFileSync(path.join(SKILL, 'templates', '_comun.js'), 'utf8');
  const json = JSON.stringify(spec).replace(/</g, '\\u003c');
  const html = fs.readFileSync(tpl, 'utf8')
    .replace('/*__SPEC__*/null', () => json)
    .replace('/*__COMUN__*/', () => comun);
  HTML_OUT = path.join(OUT_DIR, 'carrusel.html');
  fs.writeFileSync(HTML_OUT, html);
  console.log(`✓ ${HTML_OUT}`);
}

// Revisión del HTML libre: corre DENTRO de la página. Mide cajas, no scrollHeight (ver _comun.js).
async function revisarLibre() {
  await document.fonts.ready;
  await Promise.all([...document.images].map(img => img.complete ? null : new Promise(r => { img.onload = img.onerror = r; })));
  const rep = [];
  const slides = [...document.querySelectorAll('.slide')];
  if (!slides.length) rep.push({ tipo: 'no-cabe', detalle: 'no hay ningún elemento .slide' });
  [...document.images].forEach(img => { if (!img.naturalWidth) rep.push({ tipo: 'imagen', detalle: `no cargó ${decodeURI(img.src).slice(-80)}` }); });
  // Una familia pedida en CSS que no está cargada cae a otra: con -apple-system en Chrome headless cae a Times.
  // Se revisa con el peso y la itálica REALES de cada texto: una familia cargada solo en 900 da
  // "no cargó" si se pregunta por 400.
  const pedidas = new Map();
  document.querySelectorAll('.slide, .slide *').forEach(el => {
    if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return;
    const cs = getComputedStyle(el);
    const f = cs.fontFamily.split(',')[0].trim().replace(/["']/g, '');
    if (f) pedidas.set(`${cs.fontStyle} ${cs.fontWeight} 40px "${f}"`, f);
  });
  const genericas = new Set(['serif', 'sans-serif', 'monospace', 'cursive', 'system-ui', 'fantasy']);
  const avisadas = new Set();
  pedidas.forEach((f, fuente) => {
    if (avisadas.has(f)) return;
    if (/apple-system|BlinkMacSystemFont/i.test(f)) { avisadas.add(f); rep.push({ tipo: 'fuente', detalle: `${f} cae a Times en Chrome headless: usa una Google Font` }); }
    else if (!genericas.has(f) && !document.fonts.check(fuente)) { avisadas.add(f); rep.push({ tipo: 'fuente', detalle: `no cargó la fuente ${fuente}` }); }
  });
  slides.forEach((s, i) => {
    const r = s.getBoundingClientRect();
    if (Math.round(r.width) !== 1080 || Math.round(r.height) !== 1350) rep.push({ tipo: 'no-cabe', slide: i + 1, detalle: `el slide mide ${Math.round(r.width)}×${Math.round(r.height)}, no 1080×1350` });
    s.querySelectorAll('*').forEach(el => {
      if (!el.textContent.trim() || getComputedStyle(el).visibility === 'hidden') return;
      if (el.closest('[data-sangra]')) return; // decoración que sale del borde a propósito
      const q = el.getBoundingClientRect();
      if (!q.width || !q.height) return;
      const tieneTexto = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
      if (!tieneTexto) return;
      if (q.left < r.left - 1 || q.right > r.right + 1 || q.top < r.top - 1 || q.bottom > r.bottom + 1)
        rep.push({ tipo: 'no-cabe', slide: i + 1, detalle: `se sale del slide: ${el.textContent.trim().slice(0, 50)}` });
      else if (el.clientWidth > 0 && el.scrollWidth > el.clientWidth + 1 && getComputedStyle(el).overflow !== 'visible')
        rep.push({ tipo: 'no-cabe', slide: i + 1, detalle: `texto cortado: ${el.textContent.trim().slice(0, 50)}` });
    });
  });
  // Un mismo aviso repetido por padre e hijo solo ensucia
  const vistos = new Set();
  return rep.filter(x => { const k = x.tipo + x.slide + x.detalle; if (vistos.has(k)) return false; vistos.add(k); return true; });
}

const CHROME = [
  process.env.CHROME_PATH,
  '/usr/bin/google-chrome-stable',
  '/usr/bin/chromium',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
  '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
].find(p => fs.existsSync(p));

(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox', '--disable-dev-shm-usage'], defaultViewport: { width: 1080, height: 1350 } });
  const page = await browser.newPage();
  const errores = [];
  page.on('pageerror', e => errores.push(e.message));
  await page.goto('file://' + HTML_OUT, { waitUntil: 'networkidle0' });
  let reporte = [];
  if (LIBRE) {
    reporte = await page.evaluate(revisarLibre);
  } else {
    try {
      await page.waitForFunction('window.__listo === true', { timeout: 20000 });
    } catch {
      errores.push('la plantilla no terminó de pintar (window.__listo nunca llegó)');
    }
    reporte = await page.evaluate(() => window.__reporte || []);
  }
  await browser.close();

  errores.forEach(e => console.error(`✗ error en la página: ${e}`));
  reporte.forEach(r => console.warn(`⚠ ${r.tipo}${r.slide ? ` (slide ${r.slide})` : ''}: ${r.detalle}`));
  if (!reporte.length && !errores.length) console.log('✓ todo cabe, fuentes e imágenes cargadas');
  if (errores.length) process.exit(1);

  if (SIN_PNG) return;
  // Borra PNGs viejos para que no se mezclen slides de otra corrida
  const PNG_DIR = path.dirname(HTML_OUT);
  fs.readdirSync(PNG_DIR).filter(f => /^slide-\d+\.png$/.test(f)).forEach(f => fs.unlinkSync(path.join(PNG_DIR, f)));
  const r = spawnSync('node', [EXPORT_JS, HTML_OUT, '--width', '1080', '--height', '1350', '--scale', '2'], { stdio: 'inherit' });
  if (r.status !== 0) process.exit(r.status || 1);
  if (reporte.some(x => x.tipo === 'no-cabe' || x.tipo === 'fuente' || x.tipo === 'imagen')) {
    console.warn('\n⚠ Hay avisos arriba: MIRA esos PNG antes de entregar.');
  }
})().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
