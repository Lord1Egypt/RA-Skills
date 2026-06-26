/**
 * export_pdf.js — html-ppt-to-pdf skill
 *
 * Usage:
 *   node export_pdf.js                  # reads slides.html → slides.pdf
 *   node export_pdf.js my-deck.html     # reads my-deck.html → my-deck.pdf
 *
 * ⚠️  Do NOT use page.pdf() directly, wkhtmltopdf, pdfkit, or any other tool.
 *     This script uses Puppeteer screenshot-and-compose — the only method that
 *     preserves modern CSS layout (flexbox, grid, gradients, backdrop-filter).
 *
 * Chrome detection: tries bundled Chromium first, then falls back to system Chrome.
 * Works in sandboxed environments (Claude Code, Codex) where Chromium download is blocked.
 */

const path = require('path');
const fs   = require('fs');

// ─── Config ──────────────────────────────────────────────────────────────────
const HTML_FILE = process.argv[2] || 'slides.html';
const OUT_FILE  = HTML_FILE.replace(/\.html?$/i, '.pdf');
const W = 1440, H = 900;

/**
 * SELECTORS — one entry per output slide.
 * Leave as [] to auto-detect all <section> elements in DOM order.
 * Each entry: string selector OR array of selectors (merged into one slide).
 */
const SELECTORS = [];
// ─────────────────────────────────────────────────────────────────────────────

/** Find a usable Chrome/Chromium executable */
function findChrome() {
  // 1. Try puppeteer bundled browser
  try {
    const p = require('puppeteer');
    if (p.executablePath && typeof p.executablePath === 'function') {
      const ep = p.executablePath();
      if (ep && fs.existsSync(ep)) return { pkg: 'puppeteer', executablePath: ep };
    }
  } catch (_) {}

  // 2. Try puppeteer-core
  try {
    const pc = require('puppeteer-core');
    return { pkg: 'puppeteer-core', executablePath: undefined }; // will need system path
  } catch (_) {}

  return null;
}

/** System Chrome paths by platform */
const SYSTEM_CHROME_PATHS = {
  darwin: [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary',
  ],
  linux: [
    '/usr/bin/google-chrome',
    '/usr/bin/google-chrome-stable',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
    '/snap/bin/chromium',
  ],
  win32: [
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
  ],
};

function findSystemChrome() {
  const paths = SYSTEM_CHROME_PATHS[process.platform] || [];
  for (const p of paths) {
    if (fs.existsSync(p)) return p;
  }
  return null;
}

async function launch() {
  const chrome = findChrome();
  const systemPath = findSystemChrome();

  let puppeteer, executablePath;

  if (chrome?.pkg === 'puppeteer' && chrome.executablePath) {
    // Best case: puppeteer with bundled Chromium
    puppeteer = require('puppeteer');
    executablePath = chrome.executablePath;
    console.log('🟢 Using bundled Chromium:', executablePath);
  } else if (systemPath) {
    // Fallback: use system Chrome with puppeteer or puppeteer-core
    try { puppeteer = require('puppeteer'); } catch (_) {
      puppeteer = require('puppeteer-core');
    }
    executablePath = systemPath;
    console.log('🟡 Using system Chrome:', executablePath);
  } else {
    console.error(`
❌ No Chrome/Chromium found. Please install one of the following:

  macOS:   brew install --cask google-chrome
  Linux:   sudo apt install chromium-browser
  npm:     npm install puppeteer   (downloads bundled Chromium)
`);
    process.exit(1);
  }

  return puppeteer.launch({
    headless: true,
    executablePath,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  });
}

async function getBoundingBox(page, selectors) {
  const sels = Array.isArray(selectors) ? selectors : [selectors];
  return await page.evaluate((sels) => {
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (const s of sels) {
      const el = document.querySelector(s);
      if (!el) continue;
      const r = el.getBoundingClientRect();
      minX = Math.min(minX, r.left);  minY = Math.min(minY, r.top);
      maxX = Math.max(maxX, r.right); maxY = Math.max(maxY, r.bottom);
    }
    return minX === Infinity ? null : { x: minX, y: minY, width: maxX - minX, height: maxY - minY };
  }, sels);
}

async function autoDetectSelectors(page) {
  return await page.evaluate(() =>
    Array.from(document.querySelectorAll('section')).map((el, i) => {
      const cls = el.className ? '.' + el.className.trim().split(/\s+/)[0] : null;
      return cls || `section:nth-of-type(${i + 1})`;
    })
  );
}

(async () => {
  const browser = await launch();

  const page = await browser.newPage();
  await page.setViewport({ width: W, height: H, deviceScaleFactor: 2 });
  const filePath = path.resolve(process.cwd(), HTML_FILE);
  await page.goto(`file://${filePath}`, { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 1500));

  const selectors = SELECTORS.length > 0 ? SELECTORS : await autoDetectSelectors(page);
  if (selectors.length === 0) {
    console.error('❌ No <section> elements found. Check your HTML file.');
    await browser.close(); process.exit(1);
  }
  console.log(`📐 ${selectors.length} slides detected`);

  const overlayPage = await browser.newPage();
  await overlayPage.setViewport({ width: W, height: H, deviceScaleFactor: 2 });

  const imgDir = path.resolve(process.cwd(), '_pdf_pages');
  if (fs.existsSync(imgDir)) fs.rmSync(imgDir, { recursive: true });
  fs.mkdirSync(imgDir);

  for (let i = 0; i < selectors.length; i++) {
    const sel = selectors[i];
    const selStr = Array.isArray(sel) ? sel.join('+') : sel;
    try {
      const box = await getBoundingBox(page, sel);
      if (!box) { console.log(`⚠️  skip (not found): ${selStr}`); continue; }

      const scale = Math.min(W / box.width, H / box.height);
      const scaledW = Math.round(box.width * scale);
      const scaledH = Math.round(box.height * scale);

      const rawPath = path.join(imgDir, `raw_${String(i+1).padStart(2,'0')}.png`);
      await page.screenshot({ path: rawPath, clip: { x: box.x, y: box.y, width: box.width, height: box.height } });

      const slidePath = path.join(imgDir, `slide_${String(i+1).padStart(2,'0')}.html`);
      fs.writeFileSync(slidePath,
        `<!DOCTYPE html><html><head><style>*{margin:0;padding:0}` +
        `body{width:${W}px;height:${H}px;background:#000;display:flex;align-items:center;justify-content:center;overflow:hidden}` +
        `img{width:${scaledW}px;height:${scaledH}px;display:block}</style></head>` +
        `<body><img src="${rawPath}"></body></html>`
      );

      await overlayPage.goto(`file://${slidePath}`, { waitUntil: 'networkidle0' });
      const imgPath = path.join(imgDir, `page_${String(i+1).padStart(2,'0')}.png`);
      await overlayPage.screenshot({ path: imgPath, clip: { x: 0, y: 0, width: W, height: H } });

      fs.unlinkSync(rawPath); fs.unlinkSync(slidePath);
      console.log(`✅ Slide ${i+1}: ${selStr} (${Math.round(box.width)}×${Math.round(box.height)}, scale=${scale.toFixed(2)})`);
    } catch (e) { console.log(`❌ ${selStr}: ${e.message}`); }
  }

  const imgs = fs.readdirSync(imgDir).filter(f => f.startsWith('page_') && f.endsWith('.png')).sort();
  const slides = imgs.map(img =>
    `<div style="width:${W}px;height:${H}px;page-break-after:always;overflow:hidden">` +
    `<img src="${path.join(imgDir, img)}" style="width:${W}px;height:${H}px;display:block"></div>`
  ).join('\n');

  const tmpHtml = path.resolve(process.cwd(), '_slides.html');
  fs.writeFileSync(tmpHtml,
    `<!DOCTYPE html><html><head><meta charset="utf-8"><style>` +
    `*{margin:0;padding:0;box-sizing:border-box}body{background:#000}` +
    `@media print{@page{size:${W}px ${H}px;margin:0}body{-webkit-print-color-adjust:exact;print-color-adjust:exact}}` +
    `</style></head><body>${slides}</body></html>`
  );

  await overlayPage.goto(`file://${tmpHtml}`, { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 800));
  await overlayPage.pdf({
    path: path.resolve(process.cwd(), OUT_FILE),
    width: `${W}px`, height: `${H}px`,
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 }
  });

  await browser.close();
  fs.rmSync(imgDir, { recursive: true });
  fs.unlinkSync(tmpHtml);
  console.log(`\n🎉 Done: ${OUT_FILE}  (${imgs.length} slides)`);
})();
