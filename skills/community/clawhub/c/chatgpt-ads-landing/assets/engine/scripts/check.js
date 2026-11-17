#!/usr/bin/env node
/**
 * Launch gate for dist/ (run after build). Exit code 1 if any check fails.
 *
 *   node scripts/check.js              check every page in dist/
 *   node scripts/check.js my-page     check only the listed slugs
 *
 * Hard rules come from OpenAI's ads docs (OAI-AdsBot must be able to fetch
 * the page; no CAPTCHA / JS challenge / geo redirect in front of it) plus our
 * own "body readable with JS off" rule, so we never depend on whether the
 * crawler executes JS.
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DIST = path.join(ROOT, 'dist');

// Hosting-platform upload rules:
// files outside the extension whitelist are silently skipped, total must be ≤ 50MB.
const PLATFORM_EXTENSIONS = new Set(['html', 'htm', 'css', 'js', 'mjs', 'json', 'map', 'png', 'jpg', 'jpeg',
  'gif', 'svg', 'webp', 'ico', 'bmp', 'woff', 'woff2', 'ttf', 'eot', 'otf', 'mp4', 'webm', 'mp3', 'wav',
  'txt', 'xml', 'pdf']);
const PLATFORM_MAX_BYTES = 50 * 1024 * 1024;

const PLACEHOLDERS = [/REPLACE_WITH_[A-Z]+/, /__PIXEL_ID__/, /example\.com/, /\{\{[^}]*\}\}/, /to be confirmed/i, /\bTBD\b/, /填【/];
const MIN_WORDS = 300;
const MAX_IMAGE_KB = 800;

const decode = (s) => s.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
  .replace(/&quot;/g, '"').replace(/&#39;|&rsquo;|&lsquo;/g, "'").replace(/&ndash;|&mdash;/g, '-');
const norm = (s) => decode(s).replace(/[‐-―]/g, '-').replace(/[‘’]/g, "'").replace(/\s+/g, ' ').trim().toLowerCase();

// What a crawler that does NOT run JS sees.
function visibleText(html) {
  return decode(html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<noscript[\s\S]*?<\/noscript>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
}

function robotsAllows(robots, agent) {
  const groups = robots.split(/\n\s*\n/);
  const g = groups.find((b) => new RegExp(`^\\s*User-agent:\\s*${agent}\\s*$`, 'im').test(b));
  if (!g) { return false; }
  return /^\s*Allow:\s*\/\s*$/im.test(g) && !/^\s*Disallow:\s*\/\s*$/im.test(g);
}

function listFiles(dir, base = dir) {
  return fs.readdirSync(dir).flatMap((name) => {
    const p = path.join(dir, name);
    return fs.statSync(p).isDirectory() ? listFiles(p, base) : [path.relative(base, p)];
  });
}

function checkPage(slug) {
  const dir = path.join(DIST, slug);
  const read = (f) => (fs.existsSync(path.join(dir, f)) ? fs.readFileSync(path.join(dir, f), 'utf8') : '');
  const html = read('index.html');
  const robots = read('robots.txt');
  const sitemap = read('sitemap.xml');
  const text = visibleText(html);
  const page = JSON.parse(fs.readFileSync(path.join(ROOT, 'pages', slug, 'page.json'), 'utf8'));
  const pageUrl = String(page.url || '').replace(/\/*$/, '/');
  const results = [];
  const check = (group, name, ok, detail) => results.push({ group, name, ok: !!ok, detail: ok ? '' : (detail || '') });
  const warn = (group, name, detail) => results.push({ group, name, ok: true, warn: true, detail });

  // ① crawlable
  check('①可抓取', '站点根目录有 robots.txt / sitemap.xml', robots && sitemap);
  check('①可抓取', 'robots 放行 OAI-AdsBot(广告审核必需)', robotsAllows(robots, 'OAI-AdsBot'));
  check('①可抓取', 'robots 放行 OAI-SearchBot', robotsAllows(robots, 'OAI-SearchBot'));
  check('①可抓取', 'sitemap 收录本页', sitemap.includes(`<loc>${pageUrl}</loc>`), pageUrl);
  const scripts = [html].concat(
    fs.readdirSync(path.join(dir, 'assets')).filter((f) => f.endsWith('.js'))
      .map((f) => fs.readFileSync(path.join(dir, 'assets', f), 'utf8')));
  const redirects = /http-equiv=["']?refresh/i.test(html) ||
    scripts.some((s) => /location\s*\.\s*(replace|assign)\s*\(|location(\.href)?\s*=[^=]/.test(s));
  check('①可抓取', '页面本身不跳转(无 meta refresh / location 跳转)', !redirects);
  const words = text.split(/\s+/).filter((w) => /[A-Za-z0-9一-鿿]/.test(w)).length;
  check('①可抓取', `关 JS 正文仍在(≥${MIN_WORDS} 词)`, words >= MIN_WORDS, `仅 ${words} 词`);

  // ② semantic structure
  const h1 = (html.match(/<h1[\s>]/gi) || []).length;
  check('②语义结构', '唯一 h1', h1 === 1, `h1 × ${h1}`);
  check('②语义结构', '有 h2 分节', /<h2[\s>]/i.test(html));
  check('②语义结构', '<html lang> 已设置', /<html[^>]*\slang=["'][\w-]+["']/i.test(html));

  // ③④ structured data matches visible content
  const blocks = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/gi)].map((m) => m[1]);
  let parsed = [];
  let jsonOk = blocks.length > 0;
  for (const b of blocks) { try { parsed.push(JSON.parse(b)); } catch (e) { jsonOk = false; } }
  check('④可信度', 'JSON-LD 存在且合法', jsonOk, blocks.length ? 'JSON 解析失败' : '无 JSON-LD');
  const nodes = parsed.flatMap((p) => (p['@graph'] ? p['@graph'] : [p]));
  const faq = nodes.find((n) => n['@type'] === 'FAQPage');
  if (faq) {
    const qs = (faq.mainEntity || []).map((q) => q.name);
    const visible = norm(text);
    const missing = qs.filter((q) => !visible.includes(norm(q)));
    check('③意图匹配', 'FAQPage ≥3 问', qs.length >= 3, `仅 ${qs.length} 问`);
    check('③意图匹配', 'FAQPage 问题与可见 FAQ 一致', !missing.length, '页面上找不到: ' + missing.join(' | '));
  } else {
    warn('③意图匹配', '无 FAQPage', '建议加 FAQ + FAQPage schema');
  }

  // ⑤ conversion path
  const ctas = [...html.matchAll(/<a\b[^>]*data-cta="([\w-]+)"[^>]*>/gi)];
  const badHref = ctas.filter((m) => !/href="https:\/\//.test(m[0])).map((m) => m[1]);
  check('⑤转化路径', '有 CTA(data-cta)', ctas.length > 0);
  check('⑤转化路径', 'CTA 关 JS 也能跳(href 为 https 绝对地址)', ctas.length && !badHref.length, badHref.join(', '));
  const firstH2 = html.search(/<h2[\s>]/i);
  check('⑤转化路径', '首屏(第一个 h2 之前)有主 CTA', ctas.length && ctas[0].index < firstH2);

  // ⑥ technical / launch readiness
  check('⑥技术体验', 'viewport', /<meta[^>]+name="viewport"/i.test(html));
  const canon = (html.match(/<link rel="canonical" href="([^"]+)"/i) || [])[1];
  check('⑥技术体验', 'canonical = 本页 https 地址', canon === pageUrl, `canonical=${canon}`);
  const hits = PLACEHOLDERS.filter((re) => re.test(html)).map((re) => (html.match(re) || [])[0]);
  check('⑥技术体验', '无占位符(访问地址 / Pixel / 待确认文案)', !hits.length, '命中: ' + [...new Set(hits)].join(', '));
  const pixel = (html.match(/oaiq\("init",\s*\{\s*pixelId:\s*"([^"]*)"/) || [])[1];
  check('⑥技术体验', 'OpenAI Pixel 已安装(oaiq init + pixelId)', !!pixel, 'page.json pixelId 为空');
  check('⑥技术体验', 'Pixel noscript Image Tag 兜底', /<noscript>[\s\S]*bzr\.openai\.com\/v1\/sdk\/events/i.test(html));
  const lpConfigJson = (html.match(/window\.LP_CONFIG = (\{.*?\});<\/script>/) || [])[1];
  const consentCountries = lpConfigJson ? ((JSON.parse(lpConfigJson).consent || {}).countries || []) : [];
  if (consentCountries.length) {
    check('⑥技术体验', `consent 国家(${consentCountries.join('/')})在 Pixel init 前关闭 consent`,
      /oaiq\("consent", false\)[\s\S]*oaiq\("init"/.test(html) && /window\.LP_GEO = /.test(html));
  }
  const legal = [...html.matchAll(/<a\b[^>]*data-link="([\w-]+)"[^>]*>/gi)];
  const badLink = legal.filter((m) => !/href="https:\/\//.test(m[0])).map((m) => m[1]);
  if (legal.length) {
    check('⑥技术体验', '页脚链接关 JS 也能打开(href 为 https 绝对地址)', !badLink.length, badLink.join(', '));
  }

  const refs = [...html.matchAll(/(?:src|href)="([^"#:]+)"/gi)].map((m) => m[1]).filter((u) => !u.startsWith('//'));
  const missingAssets = refs.filter((u) => !fs.existsSync(path.join(dir, u.split('?')[0])));
  // url() inside CSS resolves relative to the CSS file; a leading "/" means the site root,
  // which on the deploy platform is dist/<slug>/ itself (not /<slug>/ as in local preview).
  for (const css of listFiles(dir).filter((f) => f.endsWith('.css'))) {
    const cssDir = path.dirname(path.join(dir, css));
    for (const m of fs.readFileSync(path.join(dir, css), 'utf8').matchAll(/url\(\s*["']?([^"')]+)["']?\s*\)/g)) {
      const u = m[1].split(/[?#]/)[0];
      if (/^(data:|https?:|\/\/)/.test(u)) { continue; }
      if (!fs.existsSync(u.startsWith('/') ? path.join(dir, u) : path.join(cssDir, u))) { missingAssets.push(`${css} → ${m[1]}`); }
    }
  }
  check('⑥技术体验', '引用的本地资源都存在(含 CSS 里的图片)', !missingAssets.length, missingAssets.join(', '));
  const big = fs.readdirSync(path.join(dir, 'assets'))
    .filter((f) => /\.(jpe?g|png|webp|gif)$/i.test(f))
    .map((f) => [f, Math.round(fs.statSync(path.join(dir, 'assets', f)).size / 1024)])
    .filter(([, kb]) => kb > MAX_IMAGE_KB);
  if (big.length) { warn('⑥技术体验', `图片 >${MAX_IMAGE_KB}KB`, big.map(([f, kb]) => `${f} ${kb}KB`).join(', ')); }
  // ⑦ deploy platform constraints
  const files = listFiles(dir);
  const rejected = files.filter((f) => !PLATFORM_EXTENSIONS.has(path.extname(f).slice(1).toLowerCase()));
  const junk = files.filter((f) => f.split(path.sep).some((seg) => seg.startsWith('.') || seg === '__MACOSX'));
  const total = files.reduce((n, f) => n + fs.statSync(path.join(dir, f)).size, 0);
  check('⑦部署平台', '文件类型都在平台白名单内', !rejected.length, '会被平台跳过: ' + rejected.join(', '));
  check('⑦部署平台', '无隐藏文件 / __MACOSX', !junk.length, junk.join(', '));
  check('⑦部署平台', '总大小 ≤ 50MB', total <= PLATFORM_MAX_BYTES, `${(total / 1048576).toFixed(1)}MB`);

  if (!/privacy/i.test(html)) { warn('⑥技术体验', '无隐私政策链接', '建议页脚加品牌方 Privacy Policy 链接'); }

  return results;
}

function main() {
  if (!fs.existsSync(DIST)) { console.error('✖ dist/ not found — run `node scripts/build.js` first'); process.exit(1); }
  const all = fs.readdirSync(DIST).filter((n) => fs.existsSync(path.join(DIST, n, 'index.html')));
  const slugs = process.argv.slice(2).length ? process.argv.slice(2) : all;

  let failed = 0;
  for (const slug of slugs) {
    const results = checkPage(slug);
    const hard = results.filter((r) => !r.warn);
    const pass = hard.filter((r) => r.ok).length;
    console.log(`\n■ ${slug}   ${pass}/${hard.length} 通过`);
    for (const r of results) {
      const mark = r.warn ? '⚠' : (r.ok ? '✅' : '❌');
      console.log(`  ${mark} ${r.group}  ${r.name}${r.detail ? '  — ' + r.detail : ''}`);
    }
    failed += hard.length - pass;
  }
  console.log(failed ? `\n✖ ${failed} 项未通过,不可上线` : '\n✔ 全部通过');
  process.exit(failed ? 1 : 0);
}

main();
