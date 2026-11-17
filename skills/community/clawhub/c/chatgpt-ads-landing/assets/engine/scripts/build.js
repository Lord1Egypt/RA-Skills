#!/usr/bin/env node
/**
 * pages/<slug>/ + page.json  ->  dist/<slug>/  (pure static, zero deps)
 *
 *   node scripts/build.js              build every page
 *   node scripts/build.js my-page     build only the listed slugs
 *
 * Each dist/<slug>/ is one self-contained site root — the hosting platform
 * serves one site per subdomain with index.html at its root. Per page it:
 *   - copies pages/<slug>/ (minus page.json) and shared/lp.js into dist/<slug>/
 *   - replaces {{PAGE_URL}} (page.json url), {{cta:<name>}} and {{link:<name>}}
 *     tokens in index.html; {{cta:x}} becomes the no-JS href (fixed country
 *     site, or fallback for geo), {{link:x}} becomes links.x.fallback
 *   - injects window.LP_CONFIG, shared/geo.js (inline) and the official OpenAI
 *     Measurement Pixel into <head>, and the <noscript> Image Tag + lp.js
 *     before </body>
 *   - writes robots.txt and sitemap.xml at the site root
 *
 * Placeholders (unset url / pixelId) only warn here; scripts/check.js is the
 * launch gate that fails on them.
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const PAGES = path.join(ROOT, 'pages');
const DIST = path.join(ROOT, 'dist');

const escAttr = (s) => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');
// Safe to embed inside <script>: no "</script>" or "<!--" can be formed.
const jsonForScript = (v) => JSON.stringify(v).replace(/</g, '\\u003c');

const warnings = [];
const warn = (msg) => { warnings.push(msg); console.warn('  ⚠ ' + msg); };

function copyDir(src, dest, skip) {
  fs.mkdirSync(dest, { recursive: true });
  for (const name of fs.readdirSync(src)) {
    if (name === '.DS_Store' || (skip && skip.includes(name))) { continue; }
    const s = path.join(src, name);
    const d = path.join(dest, name);
    if (fs.statSync(s).isDirectory()) { copyDir(s, d); } else { fs.copyFileSync(s, d); }
  }
}

function pageViewedData(page) {
  return {
    type: 'contents',
    contents: [{ id: page.contentId || page.slug, name: page.title || page.slug, content_type: 'page' }],
  };
}

function pixelHead(page) {
  if (!page.pixelId) {
    return '<!-- OpenAI Measurement Pixel: pixelId not set in page.json, pixel not installed -->';
  }
  // Official install snippet: https://developers.openai.com/ads/measurement-pixel
  return `<script>
  (function (w, d, s, u) {
    if (w.oaiq) return;
    var q = function () {
      q.q.push(arguments);
    };
    q.q = [];
    w.oaiq = q;
    var js = d.createElement(s);
    js.async = true;
    js.src = u;
    var f = d.getElementsByTagName(s)[0];
    f.parentNode.insertBefore(js, f);
  })(window, document, "script", "https://bzrcdn.openai.com/sdk/oaiq.min.js");
  // Consent must be set before init. LP_GEO comes from shared/geo.js; lp.js
  // shows the banner and sends page_viewed once the visitor accepts.
  var lpConsent = (window.LP_GEO || {}).consent;
  var lpBlocked = lpConsent === "pending" || lpConsent === "denied";
  if (lpBlocked) { oaiq("consent", false); } else if (lpConsent === "granted") { oaiq("consent", true); }
  oaiq("init", { pixelId: ${JSON.stringify(page.pixelId)} });
  if (!lpBlocked) { oaiq("measure", "page_viewed", ${jsonForScript(pageViewedData(page))}); }
</script>`;
}

function pixelNoscript(page) {
  if (!page.pixelId) { return ''; }
  // Image Tag fallback, only loads when JS is off: https://developers.openai.com/ads/image-tag
  const src = 'https://bzr.openai.com/v1/sdk/events?pid=' + encodeURIComponent(page.pixelId) +
    '&event=page_viewed&data[type]=contents';
  return `<noscript><img src="${escAttr(src)}" width="1" height="1" style="display:none" alt="" /></noscript>\n`;
}

function staticHref(page, cta) {
  const c = page.ctas && page.ctas[cta];
  if (!c) { throw new Error(`[${page.slug}] {{cta:${cta}}} used in index.html but not defined in page.json ctas`); }
  const r = page.routing || {};
  const dest = c.dest === 'geo' ? r.fallback : (r.sites || {})[c.dest];
  if (!dest) { throw new Error(`[${page.slug}] cta "${cta}" has no destination (dest=${c.dest})`); }
  return dest;
}

function staticLink(page, name) {
  const l = page.links && page.links[name];
  if (!l) { throw new Error(`[${page.slug}] {{link:${name}}} used in index.html but not defined in page.json links`); }
  if (!/^https:\/\//.test(l.fallback || '')) { throw new Error(`[${page.slug}] links.${name}.fallback must be an https URL`); }
  return l.fallback;
}

function buildPage(slug) {
  const dir = path.join(PAGES, slug);
  const page = Object.assign({ slug }, JSON.parse(fs.readFileSync(path.join(dir, 'page.json'), 'utf8')));
  const out = path.join(DIST, slug);
  console.log(`• ${slug}`);

  copyDir(dir, out, ['page.json']);
  fs.mkdirSync(path.join(out, 'assets'), { recursive: true });
  fs.copyFileSync(path.join(ROOT, 'shared', 'lp.js'), path.join(out, 'assets', 'lp.js'));

  const pageUrl = String(page.url || '').replace(/\/*$/, '/');
  if (!/^https:\/\/[^/]+\/$/.test(pageUrl)) {
    throw new Error(`[${slug}] page.json url must be the site root, e.g. https://your-site.example.com/ (got "${page.url}")`);
  }
  if (pageUrl.includes('REPLACE')) { warn(`[${slug}] page.json url not set — fill it after the first deploy`); }

  let html = fs.readFileSync(path.join(dir, 'index.html'), 'utf8')
    .replace(/\{\{PAGE_URL\}\}/g, pageUrl)
    .replace(/\{\{cta:([\w-]+)\}\}/g, (_m, cta) => escAttr(staticHref(page, cta)))
    .replace(/\{\{link:([\w-]+)\}\}/g, (_m, name) => escAttr(staticLink(page, name)));

  const leftover = html.match(/\{\{[^}]*\}\}/);
  if (leftover) { throw new Error(`[${slug}] unknown token ${leftover[0]} in index.html`); }
  if (!/<\/head>/i.test(html) || !/<\/body>/i.test(html)) {
    throw new Error(`[${slug}] index.html must contain </head> and </body>`);
  }

  if (page.consent && !(page.consent.countries || []).length) {
    throw new Error(`[${slug}] page.json consent.countries must list at least one country`);
  }
  const lpConfig = {
    slug, routing: page.routing || {}, ctas: page.ctas || {}, links: page.links || {},
    consent: page.consent || {}, pixelEvents: page.pixelEvents || {}, pageViewed: pageViewedData(page),
  };
  const geo = fs.readFileSync(path.join(ROOT, 'shared', 'geo.js'), 'utf8');
  if (/<\/script|<!--/i.test(geo)) { throw new Error('shared/geo.js must not contain "</script" or "<!--" (it is inlined)'); }
  const head = `<script>window.LP_CONFIG = ${jsonForScript(lpConfig)};</script>\n<script>\n${geo}</script>\n${pixelHead(page)}\n`;
  const tail = `${pixelNoscript(page)}<script src="assets/lp.js"></script>\n`;
  html = html.replace(/<\/head>/i, head + '</head>').replace(/<\/body>/i, tail + '</body>');
  fs.writeFileSync(path.join(out, 'index.html'), html);

  // Ads review requires OAI-AdsBot; OAI-SearchBot recommended.
  // https://help.openai.com/en/articles/20001243-advertiser-guidance-for-allowing-openai-web-crawlers
  fs.writeFileSync(path.join(out, 'robots.txt'), [
    'User-agent: OAI-AdsBot', 'Allow: /', '',
    'User-agent: OAI-SearchBot', 'Allow: /', '',
    'User-agent: GPTBot', 'Allow: /', '',
    'User-agent: *', 'Allow: /', '',
    `Sitemap: ${pageUrl}sitemap.xml`, '',
  ].join('\n'));
  const today = new Date().toISOString().slice(0, 10);
  fs.writeFileSync(path.join(out, 'sitemap.xml'),
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    `  <url><loc>${pageUrl}</loc><lastmod>${today}</lastmod></url>\n</urlset>\n`);

  if (!page.pixelId) { warn(`[${slug}] pixelId empty — Measurement Pixel not installed`); }
}

function main() {
  const all = fs.readdirSync(PAGES).filter((n) => fs.existsSync(path.join(PAGES, n, 'page.json')));
  const wanted = process.argv.slice(2);
  const slugs = wanted.length ? wanted : all;
  slugs.forEach((s) => { if (!all.includes(s)) { throw new Error(`no such page: pages/${s}/page.json`); } });

  if (!wanted.length) { fs.rmSync(DIST, { recursive: true, force: true }); }
  slugs.forEach((s) => fs.rmSync(path.join(DIST, s), { recursive: true, force: true }));
  fs.mkdirSync(DIST, { recursive: true });

  slugs.forEach(buildPage);
  console.log(`\nbuilt ${slugs.length} page(s) → dist/` + (warnings.length ? `  (${warnings.length} warning(s))` : ''));
}

try { main(); } catch (e) { console.error('✖ ' + e.message); process.exit(1); }
