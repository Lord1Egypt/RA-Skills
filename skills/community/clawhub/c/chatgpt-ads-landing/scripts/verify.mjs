#!/usr/bin/env node
/**
 * End-to-end verification of a deployed (or locally served) landing page.
 *
 *   node verify.mjs <url> [--dist <dist/slug dir>] [--proxy <url>|--no-proxy] [--only http,pixel,geo,consent]
 *
 *   <url>      https://your-site.example.com/  or  http://localhost:4123/  (the page root)
 *   --dist     compare the live files byte-for-byte with this build output
 *              (sitemap.xml <lastmod> is ignored: it is the build date, not content)
 *              (answers "is the new zip actually deployed?")
 *   --proxy    proxy for every request (default: $https_proxy). The OpenAI SDK
 *              and policy pages refuse mainland-China IPs, so pixel checks
 *              need an overseas exit.
 *   --only     run a subset of the groups
 *
 * Groups
 *   http    – OpenAI crawlers get 200, robots/sitemap/canonical point at <url>,
 *             no placeholders, live == --dist
 *   pixel   – real browser, real SDK: every configured event is POSTed to
 *             bzr.openai.com, gets 2xx and carries oppref
 *   geo     – per routing.sites country (time zone, IP lookup blocked): geo
 *             CTAs and data-link footer links point at that country; an
 *             unmatched visitor gets routing.fallback; with routing.ipLookup,
 *             the proxy's exit IP decides
 *   consent – per consent.countries: banner shows, nothing is sent before
 *             Accept, Accept replays page_viewed + held events, Decline sends
 *             nothing, the choice persists
 *
 * Exit code 1 if any check fails.
 */
import { execFileSync } from 'node:child_process';
import { readFileSync, existsSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { launch, navigate, sleep } from './lib/cdp.mjs';

// ---------- args ----------
const argv = process.argv.slice(2);
const opt = (name) => { const i = argv.indexOf(name); return i === -1 ? undefined : argv[i + 1]; };
const pageUrl = argv.find((a) => /^(https?|file):\/\//.test(a));
if (!pageUrl) { console.error('usage: node verify.mjs <url> [--dist dir] [--proxy url|--no-proxy] [--only http,pixel,geo,consent]'); process.exit(1); }
const base = pageUrl.replace(/[?#].*$/, '');
const dist = opt('--dist');
const proxy = argv.includes('--no-proxy') ? null : (opt('--proxy') || process.env.https_proxy || process.env.HTTPS_PROXY || null);
const only = (opt('--only') || 'http,pixel,geo,consent').split(',');
const isHttp = /^https?:/.test(base);

const COUNTRY_TZ = {
  US: 'America/New_York', CA: 'America/Toronto', GB: 'Europe/London', IE: 'Europe/Dublin', AU: 'Australia/Sydney',
  NZ: 'Pacific/Auckland', SG: 'Asia/Singapore', JP: 'Asia/Tokyo', KR: 'Asia/Seoul', HK: 'Asia/Hong_Kong',
  TW: 'Asia/Taipei', MO: 'Asia/Macau', CN: 'Asia/Shanghai', TH: 'Asia/Bangkok', MY: 'Asia/Kuala_Lumpur',
  FR: 'Europe/Paris', DE: 'Europe/Berlin', ES: 'Europe/Madrid', IT: 'Europe/Rome', NL: 'Europe/Amsterdam',
};
const NOWHERE_TZ = 'Pacific/Fiji'; // maps to no country in geo.js
const IP_LOOKUP_URLS = ['*cdn-cgi/trace*', '*country.is*'];
const BOT_UAS = {
  'OAI-AdsBot': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-AdsBot/1.0; +https://openai.com/adsbot',
  'OAI-SearchBot': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot',
  'ChatGPT-User': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot',
  'GPTBot': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.1; +https://openai.com/gptbot',
};

// ---------- report ----------
const results = [];
const report = (group, ok, item, detail = '') => {
  const mark = ok === true ? '✅' : ok === 'warn' ? '⚠️ ' : ok === 'info' ? 'ℹ️ ' : '❌';
  results.push({ ok, group, item });
  console.log(`  ${mark} ${item}${detail ? '  — ' + detail : ''}`);
};

function curl(url, { ua = 'Mozilla/5.0 (Macintosh) Chrome/141 Safari/537.36' } = {}) {
  const args = ['-s', '-L', '-m', '25', '-A', ua, '-H', 'Cache-Control: no-cache', '-w', '\n%{http_code}', url];
  if (proxy) { args.unshift('-x', proxy); }
  try {
    const out = execFileSync('curl', args, { encoding: 'latin1', maxBuffer: 50 * 1024 * 1024 });
    const i = out.lastIndexOf('\n');
    return { status: Number(out.slice(i + 1)), body: Buffer.from(out.slice(0, i), 'latin1') };
  } catch (e) { return { status: 0, body: Buffer.alloc(0) }; }
}
// robots.txt groups: the group naming the bot wins, else "*"; blocked if it has "Disallow: /".
function robotsAllows(text, bot) {
  const groups = [];
  let cur = null;
  text.split(/\r?\n/).forEach((raw) => {
    const line = raw.replace(/#.*/, '').trim();
    const m = /^([A-Za-z-]+)\s*:\s*(.*)$/.exec(line);
    if (!m) { return; }
    const key = m[1].toLowerCase();
    if (key === 'user-agent') {
      if (!cur || cur.rules.length) { cur = { agents: [], rules: [] }; groups.push(cur); }
      cur.agents.push(m[2].toLowerCase());
    } else if (cur && (key === 'allow' || key === 'disallow')) { cur.rules.push([key, m[2]]); }
  });
  const g = groups.find((x) => x.agents.includes(bot.toLowerCase())) || groups.find((x) => x.agents.includes('*'));
  return !!g && !g.rules.some(([k, v]) => k === 'disallow' && v === '/');
}
const bust = (u) => u + (u.includes('?') ? '&' : '?') + 'lpverify=' + Date.now();

// ---------- http ----------
async function groupHttp() {
  console.log('\n■ http — crawlability & deployed version');
  if (!isHttp) { report('http', 'info', 'skipped (not an http(s) URL)'); return; }
  for (const [name, ua] of Object.entries(BOT_UAS)) {
    const r = curl(base, { ua });
    report('http', r.status === 200 && r.body.length > 1000, `${name} gets the page`, `HTTP ${r.status}, ${r.body.length}B`);
  }
  const html = curl(bust(base)).body.toString('utf8');
  const robots = curl(bust(new URL('robots.txt', base).href));
  const sitemap = curl(bust(new URL('sitemap.xml', base).href));
  const robotsText = robots.body.toString('utf8');
  const allows = (bot) => robotsAllows(robotsText, bot);
  report('http', robots.status === 200 && allows('OAI-AdsBot'), 'robots.txt allows OAI-AdsBot (required for ad review)');
  report('http', robots.status === 200 && allows('OAI-SearchBot'), 'robots.txt allows OAI-SearchBot (recommended)');
  const canon = (html.match(/<link rel="canonical" href="([^"]+)"/i) || [])[1];
  report('http', canon === base, 'canonical = this URL', `canonical=${canon}`);
  const smUrl = (robotsText.match(/^Sitemap:\s*(\S+)/m) || [])[1];
  report('http', smUrl === new URL('sitemap.xml', base).href, 'robots Sitemap line = this site', `${smUrl}`);
  report('http', sitemap.status === 200 && sitemap.body.toString().includes(`<loc>${base}</loc>`), 'sitemap lists this URL');
  const ph = [html, robotsText, sitemap.body.toString()].join('\n').match(/REPLACE_WITH_[A-Z]+|填【|\{\{[^}]*\}\}|example\.com/);
  report('http', !ph, 'no placeholders in live html/robots/sitemap', ph ? `found ${ph[0]}` : '');
  report('http', !/<meta[^>]+http-equiv=["']refresh|location\.(replace|assign)\(|location\.href\s*=/i.test(html), 'page never redirects itself');

  if (dist) {
    const files = ['index.html', 'robots.txt', 'sitemap.xml', 'assets/lp.js'].filter((f) => existsSync(join(dist, f)));
    // sitemap <lastmod> is the build date, so a rebuild with no content change would look "not deployed".
    const norm = (f, buf) => (f === 'sitemap.xml' ? Buffer.from(buf.toString('utf8').replace(/<lastmod>[^<]*<\/lastmod>/g, '')) : buf);
    const diff = files.filter((f) => !norm(f, curl(bust(new URL(f, base).href)).body).equals(norm(f, readFileSync(join(dist, f)))));
    report('http', !diff.length, `live == ${dist}`, diff.length ? `differs: ${diff.join(', ')} → the new zip is not deployed yet` : files.join(', '));
  }
}

// ---------- browser helpers ----------
async function openPage({ tz, lang = 'en', viaProxy = true, blockIpLookup = false, profile, keepProfile = false } = {}) {
  const page = await launch({ proxy: viaProxy ? proxy : null, lang, profile, keepProfile });
  const events = [];
  const reqs = new Map();
  page.on((method, p) => {
    if (method === 'Network.requestWillBeSent' && /bzr\.openai\.com\/v1\/sdk\/events/.test(p.request.url)) {
      let body = null;
      try { body = p.request.postData ? JSON.parse(p.request.postData) : null; } catch { body = null; }
      const list = body ? body.events.map((e) => ({ name: e.custom_event_name || e.type, oppref: body.oppref, status: null }))
        : [{ name: new URL(p.request.url).searchParams.get('event') || '(image tag)', oppref: null, status: null }];
      reqs.set(p.requestId, list);
      events.push(...list);
    }
    if (method === 'Network.responseReceived' && reqs.has(p.requestId)) { reqs.get(p.requestId).forEach((e) => { e.status = p.response.status; }); }
  });
  await page.send('Network.enable');
  if (blockIpLookup) { await page.send('Network.setBlockedURLs', { urls: IP_LOOKUP_URLS }); }
  if (tz) { await page.send('Emulation.setTimezoneOverride', { timezoneId: tz }); }
  return { page, events };
}
const measurement = (events) => events.filter((e) => !/^(openai|oai)::/.test(e.name));
const cfgOf = (page) => page.evaluate('JSON.stringify(window.LP_CONFIG || null)').then((s) => JSON.parse(s));

const INTERACT = (selectors) => `(async () => {
  document.documentElement.style.scrollBehavior = 'auto';
  for (const s of ${JSON.stringify(selectors)}) { const el = document.querySelector(s); if (el) { el.scrollIntoView({ block: 'center' }); await new Promise(r => setTimeout(r, 1200)); } }
  window.scrollTo(0, document.documentElement.scrollHeight); await new Promise(r => setTimeout(r, 1200));
  const a = document.querySelector('[data-cta]');
  if (a) { a.addEventListener('click', e => e.preventDefault(), { once: true }); a.click(); }
})()`;

// ---------- pixel ----------
async function groupPixel(cfg) {
  console.log('\n■ pixel — real SDK, real requests' + (proxy ? ` (via ${proxy})` : ' (direct)'));
  const consentCountries = (cfg.consent && cfg.consent.countries) || [];
  const country = Object.keys(cfg.routing.sites || {}).find((c) => !consentCountries.includes(c) && COUNTRY_TZ[c]);
  const pe = cfg.pixelEvents || {};
  const expected = ['page_viewed'];
  if (pe.click) { expected.push(pe.click); }
  (pe.engagement || []).forEach((e) => expected.push(e.event));
  const waitSec = Math.max(0, ...(pe.engagement || []).map((e) => e.seconds || 0));
  const oppref = 'lpverify' + Date.now();
  const { page, events } = await openPage({ tz: country ? COUNTRY_TZ[country] : 'America/New_York' });
  try {
    await navigate(page, `${base}?oppref=${oppref}&utm_source=lpverify`, 6000);
    // The install stub queues calls in oaiq.q; the real SDK drains it on load.
    const sdk = await page.evaluate('typeof window.oaiq !== "function" ? "missing" : (!window.oaiq.q || window.oaiq.q.length === 0) ? "loaded" : "still queued (" + window.oaiq.q.length + " calls)"');
    report('pixel', sdk === 'loaded', `SDK loaded as ${country || 'US'} visitor`, sdk === 'loaded' ? '' : `${sdk} — SDK blocked? From mainland China pass --proxy`);
    await page.evaluate(INTERACT((pe.engagement || []).filter((e) => e.visible).map((e) => e.visible)));
    console.log(`  … waiting ${waitSec + 4}s for time-based events`);
    await sleep((waitSec + 4) * 1000);
    for (const name of expected) {
      const hit = events.filter((e) => e.name === name);
      const ok = hit.some((e) => e.status >= 200 && e.status < 300);
      report('pixel', ok, `event ${name}`, hit.length ? `HTTP ${hit.map((e) => e.status ?? 'pending').join('/')}${hit.some((e) => e.oppref === oppref) ? ', oppref ✓' : ', oppref MISSING'}` : 'not sent');
      if (ok && !hit.some((e) => e.oppref === oppref)) { report('pixel', false, `event ${name} carries oppref`); }
    }
    const extra = [...new Set(measurement(events).map((e) => e.name))].filter((n) => !expected.includes(n));
    if (extra.length) { report('pixel', 'info', 'other events seen', extra.join(', ')); }
  } finally { await page.close(); }
}

// ---------- geo ----------
async function geoState(page) {
  return JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const cfg = window.LP_CONFIG, ctas = cfg.ctas || {};
    const geo = [...document.querySelectorAll('[data-cta]')].filter(a => (ctas[a.dataset.cta] || {}).dest === 'geo').map(a => a.href);
    const links = Object.fromEntries([...document.querySelectorAll('[data-link]')].map(a => [a.dataset.link, a.href]));
    return { tzCountry: (window.LP_GEO || {}).country || '', country: (window.LP || {}).country || '', ipCountry: (window.LP || {}).ipCountry || '', geo, links };
  })())`));
}
// href was built from base + forwarded params: same origin/path and every base param kept.
const pointsAt = (href, target) => {
  try {
    const h = new URL(href), t = new URL(target);
    return h.origin === t.origin && h.pathname === t.pathname && [...t.searchParams].every(([k, v]) => h.searchParams.get(k) === v);
  } catch { return false; }
};

async function groupGeo(cfg) {
  console.log('\n■ geo — CTA and footer-link routing');
  const sites = cfg.routing.sites || {};
  const links = cfg.links || {};
  const geoCtas = Object.entries(cfg.ctas || {}).filter(([, c]) => c.dest === 'geo').map(([k]) => k);
  if (!geoCtas.length && !Object.keys(links).length) { report('geo', 'info', 'no geo CTAs or data-link links configured'); return; }
  const cases = Object.keys(sites).map((c) => [c, COUNTRY_TZ[c]]).concat([['(none)', NOWHERE_TZ]]);
  for (const [c, tz] of cases) {
    if (!tz) { report('geo', 'warn', `${c}: no test time zone known — add it to COUNTRY_TZ in verify.mjs`); continue; }
    const { page } = await openPage({ tz, viaProxy: !!proxy, blockIpLookup: true });
    try {
      await navigate(page, base, 2500);
      const s = await geoState(page);
      const wantCta = c === '(none)' ? cfg.routing.fallback : sites[c];
      const ctaOk = s.geo.every((h) => pointsAt(h, wantCta));
      const badLinks = Object.entries(links).filter(([n, l]) => s.links[n] && s.links[n] !== (l[c] || l.fallback)).map(([n]) => n);
      report('geo', ctaOk && !badLinks.length, `${c.padEnd(6)} (${tz})`, `detected=${s.country || '(none)'} → ${s.geo[0] ? new URL(s.geo[0]).host : '-'}${badLinks.length ? `, wrong links: ${badLinks.join(',')}` : ''}`);
    } finally { await page.close(); }
  }
  if (cfg.routing.ipLookup) {
    const { page } = await openPage({ tz: NOWHERE_TZ, viaProxy: !!proxy });
    try {
      await navigate(page, base, 5000);
      const s = await geoState(page);
      if (!s.ipCountry) { report('geo', 'warn', 'IP lookup', 'no answer (both endpoints blocked/unreachable) — time-zone result kept'); }
      else {
        const want = sites[s.ipCountry] || cfg.routing.fallback;
        report('geo', s.geo.every((h) => pointsAt(h, want)), `IP lookup (exit IP = ${s.ipCountry}${proxy ? ', via proxy' : ', direct'})`,
          sites[s.ipCountry] ? `→ ${new URL(want).host}` : `not a target country → fallback ${new URL(want).host}`);
      }
    } finally { await page.close(); }
  }
}

// ---------- consent ----------
async function groupConsent(cfg) {
  const countries = (cfg.consent && cfg.consent.countries) || [];
  console.log('\n■ consent — cookie banner flow');
  if (!countries.length) { report('consent', 'info', 'no consent.countries configured'); return; }
  const acceptText = cfg.consent.accept || 'Accept';
  const declineText = cfg.consent.decline || 'Decline';
  const pe = cfg.pixelEvents || {};
  const visible = (pe.engagement || []).filter((e) => e.visible).map((e) => e.visible);
  const clickBtn = (t) => `(() => { const b = [...document.querySelectorAll('.lp-consent button')].find(x => x.textContent.trim() === ${JSON.stringify(t)}); if (b) b.click(); return !!b; })()`;
  const state = `JSON.stringify({ banner: !!document.querySelector('.lp-consent:not([hidden])'), consent: window.LP && LP.consent(), cookies: document.cookie.split('; ').filter(c => /^__o[pb]ref=/.test(c)).length })`;
  for (const c of countries) {
    const tz = COUNTRY_TZ[c];
    if (!tz) { report('consent', 'warn', `${c}: no test time zone known`); continue; }

    // 1. first visit: banner, nothing before a choice, Accept replays held events
    let { page, events } = await openPage({ tz, keepProfile: true });
    const profile = page.profile;
    try {
      await navigate(page, `${base}?oppref=lpverify`, 5000);
      report('consent', JSON.parse(await page.evaluate(state)).banner, `${c}: banner shown on first visit`);
      await page.evaluate(INTERACT(visible)); await sleep(2500);
      const before = measurement(events).length;
      const cookiesBefore = JSON.parse(await page.evaluate(state)).cookies;
      report('consent', before === 0 && cookiesBefore === 0, `${c}: nothing sent / stored before a choice`, `${before} events, ${cookiesBefore} pixel cookies`);
      report('consent', await page.evaluate(clickBtn(acceptText)), `${c}: "${acceptText}" button works`);
      await sleep(4000);
      if (net.sdkOk) {
        const after = measurement(events).slice(before).map((e) => e.name);
        report('consent', after.includes('page_viewed'), `${c}: Accept replays held events`, after.join(', ') || 'nothing sent');
        if (isHttp) { report('consent', JSON.parse(await page.evaluate(state)).cookies > 0, `${c}: pixel cookie set after Accept`); }
      } else {
        report('consent', 'warn', `${c}: Accept replay / cookie checks skipped — SDK unreachable`);
      }
    } finally { await page.close(); }
    await sleep(800);

    // 2. revisit with the same profile: the choice is remembered
    ({ page, events } = await openPage({ tz, profile }));
    try {
      await navigate(page, base, 5000);
      const s = JSON.parse(await page.evaluate(state));
      report('consent', !s.banner && s.consent === 'granted', `${c}: choice remembered on revisit`, `consent=${s.consent}`);
    } finally { await page.close(); rmSync(profile, { recursive: true, force: true }); }

    // 3. fresh visitor declines: nothing is sent or stored
    ({ page, events } = await openPage({ tz }));
    try {
      await navigate(page, base, 5000);
      await page.evaluate(clickBtn(declineText));
      await page.evaluate(INTERACT(visible)); await sleep(3000);
      const s = JSON.parse(await page.evaluate(state));
      report('consent', measurement(events).length === 0 && s.cookies === 0, `${c}: Decline sends nothing`, `${measurement(events).length} events, ${s.cookies} cookies`);
    } finally { await page.close(); }
  }
}

// ---------- preflight: can this network reach the OpenAI SDK at all? ----------
// OpenAI blocks mainland-China IPs; without an overseas exit every pixel check
// would "fail" for reasons that have nothing to do with the page.
function preflight() {
  const trace = curl('https://www.cloudflare.com/cdn-cgi/trace').body.toString();
  const exit = (trace.match(/^loc=([A-Z]{2})$/m) || [])[1] || '?';
  const sdk = curl('https://bzrcdn.openai.com/sdk/oaiq.min.js').status;
  console.log(`exit IP country: ${exit}${proxy ? ` (via ${proxy})` : ' (direct)'} · OpenAI SDK: HTTP ${sdk}`);
  return { exit, sdkOk: sdk === 200 };
}

// ---------- main ----------
console.log(`verify ${base}${proxy ? `  (proxy ${proxy})` : '  (direct)'}`);
const net = preflight();
if (!net.sdkOk) {
  console.log('  ⚠️  OpenAI SDK unreachable from this exit — pixel checks and consent "Accept" checks are skipped.\n' +
    '     Switch the proxy/VPN to an overseas node (US/UK/SG…) and rerun to verify real event delivery.');
}
if (only.includes('http')) { await groupHttp(); }
const needBrowser = only.some((g) => ['pixel', 'geo', 'consent'].includes(g));
if (needBrowser) {
  const { page } = await openPage({ tz: 'America/New_York' });
  let cfg;
  try { await navigate(page, base, 2500); cfg = await cfgOf(page); } finally { await page.close(); }
  if (!cfg) { report('browser', false, 'window.LP_CONFIG not found — is this a page built by scripts/build.js?'); }
  else {
    if (only.includes('pixel')) {
      if (net.sdkOk) { await groupPixel(cfg); } else { console.log('\n■ pixel'); report('pixel', 'warn', 'skipped — OpenAI SDK unreachable from this network'); }
    }
    if (only.includes('geo')) { await groupGeo(cfg); }
    if (only.includes('consent')) { await groupConsent(cfg); }
  }
}
const failed = results.filter((r) => r.ok === false);
console.log(`\n${failed.length ? '✖' : '✔'} ${results.filter((r) => r.ok === true).length} passed, ${failed.length} failed, ${results.filter((r) => r.ok === 'warn').length} warnings`);
process.exit(failed.length ? 1 : 0);
