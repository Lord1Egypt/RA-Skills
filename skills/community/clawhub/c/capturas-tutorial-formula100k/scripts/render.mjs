#!/usr/bin/env node
/**
 * capturas-tutorial-formula100k — render
 *
 * Modos:
 *   1) MANIFEST     node render.mjs --manifest <ruta.yml> --out <carpeta>
 *   2) Single       node render.mjs --type <tipo> --out <archivo.png> --data '<json>'
 *
 * Tipos soportados: step, terminal, callout, screenshot, keys, link, comparison, list
 *
 * Flags:
 *   --width <px>     (default 1920) — canvas inicial, NO el tamaño del PNG final.
 *   --height <px>    (default 1080) — canvas inicial.
 *   --bg <cream|cream-soft|transparent>   (default transparent)
 *   --scale <n>      (deviceScaleFactor, default 1) — 1 garantiza que el PNG final coincida con (width,height).
 *   --no-trim        Desactiva el auto-trim del bbox de alpha (por default: ON sobre fondo transparente).
 *   --pad <px>       Padding alrededor del bbox tras trim (default 40).
 *
 * Post-procesado automático:
 *   - Si bg=transparent: trim al bbox de alpha + extend(pad).
 *   - Si bg=cream: no trim, se garantiza output (width,height).
 */

import fs from 'node:fs/promises';
import path from 'node:path';
import url from 'node:url';
import { existsSync } from 'node:fs';
import sharp from 'sharp';

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));
const TEMPLATES_DIR = path.resolve(__dirname, '..', 'templates');

const VALID_TYPES = ['step', 'terminal', 'callout', 'screenshot', 'keys', 'link', 'comparison', 'list', 'claude-input'];

// ---------- arg parsing ----------
function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) { args[key] = true; }
      else { args[key] = next; i++; }
    }
  }
  return args;
}

// ---------- placeholder substitution ----------
function fillTemplate(tpl, data) {
  // {{key}} substitution. If key missing, replace with empty string.
  // Also handles {{key_hidden}} -> "hidden" or "" depending on whether `key` is present.
  return tpl.replace(/\{\{(\w+)\}\}/g, (_, key) => {
    if (key.endsWith('_hidden')) {
      const base = key.slice(0, -'_hidden'.length);
      const v = data[base];
      const isEmpty = v === undefined || v === null || v === '';
      return isEmpty ? 'hidden' : '';
    }
    const v = data[key];
    return v === undefined || v === null ? '' : String(v);
  });
}

// ---------- per-type data normalization ----------
function buildItemHtml(type, data, globalBg) {
  const bg = data.bg || globalBg || 'transparent';
  const ctx = { ...data, bg };

  if (type === 'terminal') {
    ctx.title = ctx.title || 'Terminal — bash';
    ctx.command = (ctx.command || '').replace(/^\$\s*/, '');
    if (ctx.copy === false) ctx.copy = ''; // triggers _hidden
    else ctx.copy = '1';
  }

  if (type === 'callout') {
    ctx.variant = ctx.variant || 'info';
    if (!ctx.icon) {
      const defaultIcons = { info: 'ℹ️', warning: '⚠️', success: '✓', note: '📝', error: '✕' };
      ctx.icon = defaultIcons[ctx.variant] || 'ℹ️';
    }
    // body puede traer **bold** y `code` en markdown light → convertir
    ctx.body = mdLite(ctx.body || '');
  }

  if (type === 'step') {
    ctx.body = mdLite(ctx.body || '');
  }

  if (type === 'screenshot') {
    ctx.frame = ctx.frame || 'mac';
    // image puede ser ruta absoluta o file:// — convertir a file://
    if (ctx.image && !ctx.image.startsWith('file://') && !ctx.image.startsWith('http')) {
      ctx.image = 'file://' + path.resolve(ctx.image);
    }
    // ocultar el url-bar si frame != browser, ocultar title si frame == browser
    if (ctx.frame === 'browser') {
      ctx.title = '';
      ctx.url = ctx.url || '';
    } else {
      ctx.url = '';
      ctx.title = ctx.title || '';
    }
    ctx.caption = ctx.caption || '';
  }

  if (type === 'keys') {
    const keys = Array.isArray(ctx.keys) ? ctx.keys : (ctx.keys || '').split('+').map(s => s.trim()).filter(Boolean);
    const parts = [];
    keys.forEach((k, i) => {
      const wide = k.length >= 3 ? ' wide' : '';
      parts.push(`<div class="key${wide}">${escapeHtml(k)}</div>`);
      if (i < keys.length - 1) parts.push('<span class="plus">+</span>');
    });
    ctx.keys_html = parts.join('');
    ctx.label = ctx.label || '';
  }

  if (type === 'link') {
    ctx.label = ctx.label || '';
  }

  if (type === 'comparison') {
    ctx.no_title = ctx.no_title || ctx.bad_title || '';
    ctx.no_body = mdLite(ctx.no_body || ctx.bad_body || '');
    ctx.yes_title = ctx.yes_title || ctx.good_title || '';
    ctx.yes_body = mdLite(ctx.yes_body || ctx.good_body || '');
  }

  if (type === 'claude-input') {
    ctx.popup_header = ctx.popup_header || 'Skills disponibles';
    ctx.icon_active  = ctx.icon_active  || '📝';
    ctx.name_active  = ctx.name_active  || 'guionizacion-formula100k';
    ctx.desc_active  = ctx.desc_active  || 'Crea guiones virales con tu voz y estrategia.';
    ctx.icon_2       = ctx.icon_2       || '🎬';
    ctx.name_2       = ctx.name_2       || 'carrusel-viral-formula100k';
    ctx.icon_3       = ctx.icon_3       || '🎯';
    ctx.name_3       = ctx.name_3       || 'optimizador-cta-formula100k';
    ctx.typed        = ctx.typed        || ctx.name_active;
  }

  if (type === 'list') {
    const items = Array.isArray(ctx.items) ? ctx.items : [];
    ctx.items_html = items.map((it, i) => {
      const content = mdLite(typeof it === 'string' ? it : (it.text || ''));
      const numberOrCheck = ctx.numbered ? (i + 1) : '✓';
      return `<div class="list-item"><div class="check">${numberOrCheck}</div><div>${content}</div></div>`;
    }).join('');
    ctx.title = ctx.title || '';
  }

  return ctx;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
}

// markdown-light: **bold**, `code`. Resto se escapa.
function mdLite(s) {
  let out = escapeHtml(s);
  out = out.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  out = out.replace(/`(.+?)`/g, '<code>$1</code>');
  return out;
}

// ---------- render with puppeteer ----------
async function loadPuppeteer() {
  try {
    return (await import('puppeteer')).default;
  } catch (e) {
    console.error('\nFalta puppeteer. Corre primero: bash ' + path.resolve(__dirname, 'install.sh') + '\n');
    process.exit(2);
  }
}

async function renderOne(browser, { type, data, outPath, width, height, bg, scale, trim, pad }) {
  if (!VALID_TYPES.includes(type)) throw new Error('Tipo inválido: ' + type);
  const tplPath = path.join(TEMPLATES_DIR, type + '.html');
  let tpl = await fs.readFile(tplPath, 'utf8');
  const ctx = buildItemHtml(type, data, bg);
  let html = fillTemplate(tpl, ctx);

  // Inline el CSS de tokens (Puppeteer le da igual el link relativo si baseURI está bien, pero para evitar problemas con file:// y headers, lo inlineamos)
  const tokens = await fs.readFile(path.join(TEMPLATES_DIR, '_tokens.css'), 'utf8');
  html = html.replace('<link rel="stylesheet" href="_tokens.css">', `<style>${tokens}</style>`);

  const page = await browser.newPage();
  await page.setViewport({ width, height, deviceScaleFactor: scale });
  // base URL = templates dir para que las imágenes relativas y futuras refs funcionen
  await page.goto('data:text/html;charset=utf-8,' + encodeURIComponent(html), { waitUntil: 'networkidle0' });

  // esperar a que las fuentes carguen
  await page.evaluate(() => document.fonts.ready);

  // si bg es transparente, forzar omitBackground
  const omitBg = (ctx.bg === 'transparent');

  // Screenshot a buffer (no a disco todavía — vamos a post-procesar)
  const rawBuf = await page.screenshot({ type: 'png', omitBackground: omitBg, fullPage: false });
  await page.close();

  await fs.mkdir(path.dirname(outPath), { recursive: true });

  // Post-procesado:
  //   - Sobre fondo transparente, recortar al bbox de alpha + padding (BUG 2)
  //   - Si scale > 1, sharp redimensiona al canvas pedido (width, height) ANTES de trim
  //     para garantizar que el PNG final no excede 1x el viewport (BUG 1).
  let img = sharp(rawBuf);
  const meta = await img.metadata();
  if (meta.width !== width || meta.height !== height) {
    img = sharp(await img.resize(width, height, { fit: 'fill' }).png().toBuffer());
  }
  if (trim && omitBg) {
    img = img.trim({ threshold: 1 }).extend({
      top: pad, bottom: pad, left: pad, right: pad,
      background: { r: 0, g: 0, b: 0, alpha: 0 }
    });
  }
  await img.png().toFile(outPath);
  return outPath;
}

// ---------- YAML loader (lazy) ----------
async function loadYaml(filepath) {
  let yaml;
  try { yaml = (await import('js-yaml')).default; }
  catch (e) {
    console.error('Falta js-yaml. Corre: bash ' + path.resolve(__dirname, 'install.sh'));
    process.exit(2);
  }
  const raw = await fs.readFile(filepath, 'utf8');
  return yaml.load(raw);
}

// ---------- main ----------
async function main() {
  const args = parseArgs(process.argv.slice(2));
  const width  = parseInt(args.width  || '1920', 10);
  const height = parseInt(args.height || '1080', 10);
  const bg     = args.bg || 'transparent';
  const scale  = parseFloat(args.scale || '1');
  const trim   = !args['no-trim'];
  const pad    = parseInt(args.pad || '40', 10);

  const puppeteer = await loadPuppeteer();
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });

  try {
    if (args.manifest) {
      const manifest = await loadYaml(args.manifest);
      const outDir = path.resolve(args.out || path.join(path.dirname(args.manifest), 'USER'));
      const items = manifest.recursos || manifest.items || [];
      if (!items.length) { console.error('Manifest vacío.'); process.exit(1); }

      console.log(`Renderizando ${items.length} items → ${outDir}`);
      for (const it of items) {
        const type = it.tipo || it.type;
        const id   = it.id || Math.random().toString(36).slice(2, 8);
        const data = it.data || {};
        const itemBg = it.bg || bg;
        const itemW = parseInt(it.width  || width, 10);
        const itemH = parseInt(it.height || height, 10);
        const slug  = (data.slug || id).replace(/[^a-z0-9_-]/gi, '_').toLowerCase();
        const outPath = path.join(outDir, `${id}_${type}_${slug}.png`);
        await renderOne(browser, { type, data, outPath, width: itemW, height: itemH, bg: itemBg, scale, trim, pad });
        console.log(`  ✓ ${path.basename(outPath)}`);
      }
    } else if (args.type) {
      const data = args.data ? JSON.parse(args.data) : {};
      const outPath = path.resolve(args.out || `./${args.type}.png`);
      await renderOne(browser, { type: args.type, data, outPath, width, height, bg, scale, trim, pad });
      console.log(`✓ ${outPath}`);
    } else {
      console.log(`
Usage:
  render.mjs --manifest <ruta.yml> [--out <carpeta>]
  render.mjs --type <tipo> --out <archivo.png> --data '<json>'

Tipos: ${VALID_TYPES.join(', ')}

Flags globales:
  --width <px>    default 1920 (canvas inicial; el PNG final se recorta al bbox)
  --height <px>   default 1080 (canvas inicial)
  --bg <cream|cream-soft|transparent>   default transparent
  --scale <n>     default 1  (mantén 1 — el PNG final coincide con el canvas; 2x rompe Remotion)
  --no-trim       desactiva el auto-trim al bbox (default: ON sobre transparente)
  --pad <px>      padding alrededor del bbox tras trim (default 40)

Ejemplos:
  # un comando terminal solo
  render.mjs --type terminal --out term.png \\
    --data '{"command":"curl -fsSL https://claude.ai/install.sh | bash"}'

  # un paso numerado
  render.mjs --type step --out step2.png \\
    --data '{"number":2,"title":"Pega el comando","body":"Copia y pega con **Cmd+V**."}'

  # batch desde manifest
  render.mjs --manifest /ruta/MANIFEST_UI.yml --out /ruta/UI/
      `);
      process.exit(0);
    }
  } finally {
    await browser.close();
  }
}

main().catch(e => { console.error(e); process.exit(1); });
