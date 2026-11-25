// ═══════════════════════════════════════════════════════════════
//   SKILL ADAPTATION of email-scraper.js (see references/adaptation-notes.md)
//   Changes vs original are marked with "SKILL:" comments. Extraction,
//   normalization, suspicious detection, CSV columns and cache format are
//   unchanged. Removed: Facebook login/search channel + hardcoded credentials.
// ═══════════════════════════════════════════════════════════════
//   [ HUZAIFA CYBER PROXY ] — EMAIL SCRAPER ULTIMATE
//   Website → CloudFlare → FB Direct → FB Search
//   STABLE MODE | Crash-Safe | Resume | Hacker UI
//   ── v2: JSON-LD, attributes, text-node extraction, [at]/[dot],
//          email source + confidence, suspicious tracking,
//          multi-row cache restore ──
// ═══════════════════════════════════════════════════════════════

const axios         = require('axios');
const cheerio       = require('cheerio');
const fs            = require('fs');
const path          = require('path');
const { parse }     = require('csv-parse/sync');

const { stringify } = require('csv-stringify/sync');


// ─── COLORS ────────────────────────────────────────────────
const C = {
  reset:'\x1b[0m', bright:'\x1b[1m',
  red:'\x1b[31m',  green:'\x1b[32m', yellow:'\x1b[33m',
  blue:'\x1b[34m', magenta:'\x1b[35m',cyan:'\x1b[36m',
  white:'\x1b[37m',gray:'\x1b[90m',  black:'\x1b[30m',
};
// SKILL: plain (no-ANSI) output by default so agents/log files stay readable.
const ARGV  = process.argv.slice(2);
const FANCY = ARGV.includes('--fancy');
const clr = (t,...cs) => FANCY ? cs.map(c=>C[c]||'').join('')+t+C.reset : String(t);

// ─── CONFIG — STABLE MIDDLE GROUND ─────────────────────────
// Target: 1000 URLs in 3-4 hours = ~12s avg per URL
// SKILL: tiny argv reader (--key value  or  --key=value)
function argVal(name, def) {
  for (let i = 0; i < ARGV.length; i++) {
    if (ARGV[i] === name && ARGV[i+1] && !ARGV[i+1].startsWith('--')) return ARGV[i+1];
    if (ARGV[i].startsWith(name + '=')) return ARGV[i].slice(name.length + 1);
  }
  return def;
}
// SKILL: all input/cache/output files live in --workdir (default: current directory).
const WORKDIR = path.resolve(argVal('--workdir', process.cwd()));
const inW = f => path.join(WORKDIR, f);

const CONFIG = {
  INPUT_FILE:      inW(argVal('--input', 'input.csv')),
  OUTPUT_FILE:     inW('output.csv'),
  SUSPICIOUS_FILE: inW('suspicious.csv'),
  CACHE_FILE:      inW('cache.json'),

  REQUEST_TIMEOUT: 12000,   // 12s web timeout
  CONCURRENCY:     Math.max(1, Math.min(4, parseInt(argVal('--concurrency', '2'), 10) || 2)),  // SKILL: capped at 4
  RETRY_ATTEMPTS:  1,

  PRIORITY_PAGES: [
    '/contact','/contact-us','/about','/about-us',
    '/team','/reach-us','/get-in-touch','/info',
  ],
  CONTACT_KEYWORDS: ['contact','about','reach','touch','connect','enquir'],

  // Polite delays (unchanged from original website-channel values)
  DELAY_WEB:       { min: 200,  max: 500  }, // between web requests
  DELAY_BETWEEN:   { min: 500,  max: 1200 }, // between URLs

  WEB_TIMEOUT: 12000,
};

// ─── PATTERNS ──────────────────────────────────────────────
// Strict email regex — must start with a letter, not digit/symbol.
// (Still used inside the Facebook page.evaluate sandbox.)
const EMAIL_REGEX = /(?<![0-9.\-+])(?<![A-Za-z0-9._%+\-]{0,30}[0-9]{4,})[a-zA-Z][a-zA-Z0-9._%+\-]*@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/g;
// Permissive finder — captures glued junk too; normalizeEmail() cleans it afterwards.
const EMAIL_FIND  = /[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/g;
// Loose phone regex — used separately for the phone column only
const PHONE_REGEX = /(\+?1?\s?)?(\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4})/g;

const EMAIL_BLACKLIST = [
  'example.com','test.com','domain.com','email.com','youremail.com',
  'sentry.io','wixpress.com','schema.org','facebook.com','fb.com',
  'instagram.com','twitter.com','linkedin.com','tiktok.com',
  'wordpress','jquery','bootstrap','google','apple','microsoft',
  'png','jpg','jpeg','gif','svg','webp','css','js','woff','ttf',
];
const FB_SOCIAL = /facebook\.com\/(?!share|sharer|dialog|login|help|policies|groups\/|events\/|marketplace|watch|gaming|ads|pages\/create)([^/?#"'\s]+)/i;

// Known typo TLDs / provider domains — FLAGGED as suspicious, never auto-corrected.
const SUSPICIOUS_TLDS = new Set([
  'con','cmo','vom','comm','ocm','xom','coom','cim','clm','coon','nte','ogr','orgg',
]);
const SUSPICIOUS_DOMAINS = new Set([
  'gmial.com','gmai.com','gmil.com','gmail.co','gmail.con','gmaill.com',
  'hotmial.com','hotmai.com','hotmal.com','yaho.com','yahooo.com','outlok.com',
]);

// ─── STATS ─────────────────────────────────────────────────
const STATS = {
  total:0, processed:0, found:0,
  fromWeb:0,
  notFound:0, errors:0, blocked:0, suspicious:0, startTime: Date.now(),
};

// ─── UTILS ─────────────────────────────────────────────────
const rInt   = (a,b) => Math.floor(Math.random()*(b-a+1))+a;
const sleep  = ms => new Promise(r=>setTimeout(r,ms));
const rSleep = r => sleep(rInt(r.min,r.max));
const confRank = c => ({ high:3, medium:2, low:1 })[c] || 0;

function normalizeUrl(url) {
  url = url.trim();
  if (!url.startsWith('http')) url = 'https://'+url;
  return url.replace(/\/$/,'');
}
function getBusinessName(url) {
  try {
    return new URL(url).hostname.replace('www.','').split('.')[0]
      .replace(/[-_]/g,' ')
      .replace(/\b(inc|llc|ltd|co|corp|group)\b/gi,'')
      .trim();
  } catch { return url; }
}

// ─── ENTITY / ESCAPE DECODER ───────────────────────────────
// Fixes the "u003e…" prefix bug: sites encode ">" as \u003e; when the
// backslash is lost upstream you get a literal "u003e" glued to the email.
function decodeEntities(s) {
  if (!s) return '';
  return String(s)
    // \u003e style escapes (backslash still present)
    .replace(/\\u([0-9a-fA-F]{4})/g, (_, h) => String.fromCharCode(parseInt(h, 16)))
    // leftover escapes whose backslash was stripped: u003e, u0040 …
    .replace(/u00([0-9a-fA-F]{2})/g, (_, h) => String.fromCharCode(parseInt(h, 16)))
    // numeric HTML entities: &#64;  &#x40;
    .replace(/&#x([0-9a-fA-F]+);?/g, (_, h) => String.fromCharCode(parseInt(h, 16)))
    .replace(/&#(\d+);?/g,           (_, d) => String.fromCharCode(parseInt(d, 10)))
    // named entities that show up around emails
    .replace(/&gt;/gi, '>').replace(/&lt;/gi, '<')
    .replace(/&amp;/gi, '&').replace(/&quot;/gi, '"').replace(/&nbsp;/gi, ' ');
}

// ─── DE-OBFUSCATOR — turns "name [at] domain [dot] com" into an email ───
function deobfuscateText(text) {
  let t = String(text);
  // bracketed forms: (at) [at] {at} <at>  /  (dot) [dot] {dot} <dot>
  t = t.replace(/\s*[\[\](){}<>]\s*at\s*[\[\](){}<>]\s*/gi, '@');
  t = t.replace(/\s*[\[\](){}<>]\s*dot\s*[\[\](){}<>]\s*/gi, '.');
  // spelled-out unbracketed form, only when it forms a full email
  t = t.replace(/([a-z0-9._%+\-]+)\s+at\s+([a-z0-9.\-]+)\s+dot\s+([a-z]{2,})/gi, '$1@$2.$3');
  return t;
}

// ─── EMAIL NORMALIZER ──────────────────────────────────────
// Returns { email, suspicious, reason } or null.
//   • conservative "u003e" decode              (repaired, kept)
//   • conservative phone-prefix strip          (repaired, kept)
//   • TLD/domain typos (.con etc.)             (FLAGGED suspicious, NOT changed)
function normalizeEmail(raw) {
  if (!raw) return null;
  const original = String(raw).trim();

  let e = decodeEntities(original).trim();
  e = e.replace(/^mailto:/i, '').split('?')[0].trim();
  if (!e.includes('@')) return null;

  // drop trailing glued words (Opens, PHONE, TEL, …)
  e = e.replace(/(Opens|PHONE|TEL|FAX|MOB|MOBILE|CALL|CONTACT|EMAIL|GMAIL|HOTMAIL)\s*$/i, '').trim();

  // grab the maximal local@domain candidate (digits allowed so a glued phone
  // is captured whole, then cleaned below)
  const m = e.match(/[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/);
  if (!m) return null;

  let [local, domain] = m[0].split('@');
  if (!local || !domain) return null;

  const reasons = [];
  if (/^u00[0-9a-fA-F]{2}/i.test(original)) reasons.push('decoded-escape');

  // strip a phone number glued to the FRONT of the local part:
  //   usa2527283899info → info      |      il773.276.8888hello → hello
  const beforePhone = local;
  local = local.replace(/^[a-z]{0,4}\+?\d[\d.\-\s]{7,}\d(?=[a-z])/i, '');
  if (/\d{5,}/.test(local)) {
    const tail = local.replace(/^.*\d{4,}/, '');
    if (/^[a-z][a-z0-9._%+\-]*$/i.test(tail)) local = tail;
  }
  if (local !== beforePhone) reasons.push('stripped-phone-prefix');

  local = local.replace(/^[._%+\-]+/, '').replace(/[._%+\-]+$/, '');
  if (!/^[a-zA-Z]/.test(local)) return null;
  if (local.length < 1 || local.length > 64) return null;

  // domain validation — DO NOT auto-repair typos, only flag them
  domain = domain.toLowerCase().replace(/^\.+|\.+$/g, '');
  if (!domain.includes('.')) return null;
  const tld = domain.split('.').pop();
  if (tld.length < 2 || tld.length > 10) return null;
  if (/^\d+$/.test(domain.replace(/\./g, ''))) return null;

  let suspicious = false;
  if (SUSPICIOUS_TLDS.has(tld))       { suspicious = true; reasons.push('suspicious-tld:.'+tld); }
  if (SUSPICIOUS_DOMAINS.has(domain)) { suspicious = true; reasons.push('suspicious-domain:'+domain); }

  return {
    email: (local + '@' + domain).toLowerCase(),
    suspicious,
    reason: reasons.join('; '),
  };
}

// ─── CANDIDATE REFINER — normalize, blacklist, dedupe, split suspicious ───
// Input:  [{ raw, source, confidence, page }]
// Output: { clean:[cand], suspicious:[cand] }   (cand has email/source/confidence/suspicious/reason/page)
function refineCandidates(cands) {
  const best = new Map(); // email -> chosen candidate (highest confidence wins)
  for (const c of cands) {
    const n = normalizeEmail(c.raw);
    if (!n) continue;
    if (EMAIL_BLACKLIST.some(b => n.email.includes(b))) continue;

    const cand = {
      email:      n.email,
      source:     c.source || '',
      confidence: c.confidence || 'low',
      suspicious: n.suspicious,
      reason:     n.reason,
      page:       c.page || '',
    };
    const prev = best.get(n.email);
    if (!prev || confRank(cand.confidence) > confRank(prev.confidence)) best.set(n.email, cand);
  }
  const all = [...best.values()];
  return {
    clean:      all.filter(c => !c.suspicious),
    suspicious: all.filter(c =>  c.suspicious),
  };
}

function filterPhones(arr) {
  return [...new Set(arr.filter(p => {
    const d = String(p).replace(/\D/g,'');
    return d.length >= 10 && d.length <= 15;
  }))];
}

function eta() {
  const elapsed = (Date.now() - STATS.startTime) / 1000;
  const rate    = STATS.processed / elapsed;
  const rem     = STATS.total - STATS.processed;
  const etaSec  = rate > 0 ? rem / rate : 0;
  const h = Math.floor(etaSec/3600);
  const m = Math.floor((etaSec%3600)/60);
  return `${h}h ${m}m`;
}

// ─── CRASH SAFE ────────────────────────────────────────────
function loadCache() {
  if (!fs.existsSync(CONFIG.CACHE_FILE)) return {};
  try { return JSON.parse(fs.readFileSync(CONFIG.CACHE_FILE,'utf8')); }
  catch { return {}; }
}
function saveCache(cache) {
  try {
    const t = CONFIG.CACHE_FILE+'.tmp';
    fs.writeFileSync(t, JSON.stringify(cache,null,2));
    fs.renameSync(t, CONFIG.CACHE_FILE);
  } catch { try { fs.writeFileSync(CONFIG.CACHE_FILE, JSON.stringify(cache,null,2)); } catch {} }
}
function saveOutput(results) {
  try {
    const t = CONFIG.OUTPUT_FILE+'.tmp';
    fs.writeFileSync(t, stringify(results,{header:true}));
    fs.renameSync(t, CONFIG.OUTPUT_FILE);
  } catch { try { fs.writeFileSync(CONFIG.OUTPUT_FILE, stringify(results,{header:true})); } catch {} }
}

// ─── SUSPICIOUS STORE (saved separately) ───────────────────
const suspiciousResults = [];
function loadSuspicious() {
  if (!fs.existsSync(CONFIG.SUSPICIOUS_FILE)) return;
  try {
    const rows = parse(fs.readFileSync(CONFIG.SUSPICIOUS_FILE,'utf8'),
      { columns:true, skip_empty_lines:true, trim:true });
    suspiciousResults.push(...rows);
  } catch {}
}
function saveSuspicious() {
  if (!suspiciousResults.length) return;
  try {
    const t = CONFIG.SUSPICIOUS_FILE+'.tmp';
    fs.writeFileSync(t, stringify(suspiciousResults,{header:true}));
    fs.renameSync(t, CONFIG.SUSPICIOUS_FILE);
  } catch { try { fs.writeFileSync(CONFIG.SUSPICIOUS_FILE, stringify(suspiciousResults,{header:true})); } catch {} }
}
function recordSuspicious(url, biz, list, channel) {
  if (!list || !list.length) return;
  const now = new Date().toISOString();
  const seen = new Set(suspiciousResults.map(r => r.url + '|' + r.email));
  for (const c of list) {
    const key = url + '|' + c.email;
    if (seen.has(key)) continue;
    seen.add(key);
    suspiciousResults.push({
      url,
      business_name: biz,
      email:         c.email,
      email_source:  c.source,
      confidence:    c.confidence,
      reason:        c.reason,
      source_page:   c.page || '',
      channel,
      scraped_at:    now,
    });
    STATS.suspicious++;
  }
  saveSuspicious();
}

// ══════════════════════════════════════════════════════════
//  HACKER ASCII UI
// ══════════════════════════════════════════════════════════
const MX = '01アイウエオカキクケコ@#$%<>[]{}?!';
const mx  = n => Array.from({length:n},()=>MX[Math.floor(Math.random()*MX.length)]).join('');

// Mini Cicada butterfly — cycles line by line in the status bar
const _B = '\x1b[38;2;80;140;255m';   // blue
const _W = '\x1b[38;2;200;220;255m';  // white-blue
const _C = '\x1b[38;2;100;200;255m';  // cyan
const _D = '\x1b[2m';                  // dim
const _R = '\x1b[0m';                  // reset
const HACKER_LINES = [
  `${_D}${_W}  ·  ✦  ·  ✦  ·  ${_R}`,
  `${_W} ▄▀▀▄${_B}╬${_W}▄▀▀▄ ${_R}`,
  `${_W}▓${_B}░▄███▄░${_W}▓${_R}`,
  `${_B}▓╬${_W}◈${_B}╬╬╬${_W}◈${_B}╬▓${_R}`,
  `${_B} ▀╬╬╬╬╬╬╬▀ ${_R}`,
  `${_B}  ▄${_W}█████${_B}▄  ${_R}`,
  `${_B} ▓╬${_W}▀███▀${_B}╬▓ ${_R}`,
  `${_B}  ╬╬╬╬╬╬╬  ${_R}`,
  `${_B} ▄╬╬╬╬╬╬╬▄ ${_R}`,
  `${_W}▀▄${_B}╬╬╬╬╬${_W}▄▀${_R}`,
  `${_D}${_W}▀▀▄▄▄▄▄▀▀ ${_R}`,
  `${_C}  ≡ CICADA ≡  ${_R}`,
];

let cyberInt   = null;
let hackerLine = 0;
let frameCount = 0;

function drawCyberPanel() {
  frameCount++;
  const pct  = STATS.total > 0 ? Math.round((STATS.processed/STATS.total)*100) : 0;


  const name = clr('[ HUZAIFA CYBER PROXY ]', 'green','bright');
  const proc = clr(`${STATS.processed}/${STATS.total}`, 'cyan','bright');
  const pctS = clr(`${pct}%`, 'yellow','bright');
  const fnd  = clr(`✔${STATS.found}`, 'green','bright');
  const nf   = clr(`✘${STATS.notFound}`, 'red');
  const etaS = clr(`ETA:${eta()}`, 'gray');

  // Hacker figure line (cycle through)
  const fig  = clr(HACKER_LINES[hackerLine % HACKER_LINES.length], 'green');
  if (frameCount % 3 === 0) hackerLine++;

  process.stdout.write(
    `\r  ${name}  ${proc} ${pctS} ${fnd} ${nf} ${etaS}  ${fig}  `
  );
}

function startCyberUI() {
  cyberInt = setInterval(drawCyberPanel, 180);
}
function stopCyberUI() {
  if (cyberInt) clearInterval(cyberInt);
  console.log('');
}

// Per URL header
function urlHeader(url, idx) {
  const t   = clr(new Date().toLocaleTimeString(), 'gray');
  const hcp = clr('HCP>>', 'green','bright');
  const idS = clr(`[${idx}/${STATS.total}]`, 'cyan');

  const u   = clr(url.length > 55 ? url.slice(0,55)+'...' : url, 'white','bright');
  console.log(`\n ${idS} ${hcp} ${u} ${t}`);
}

// Per URL result
function urlResult(biz, emails, source, elapsed) {
  const hcp = clr('[HUZAIFA CYBER PROXY]', 'green','bright');
  const e   = clr(`${elapsed}s`, 'gray');
  if (emails.length > 0) {
    console.log(` ${clr('>','green','bright')} ${hcp} ${clr('FOUND:','green','bright')} ${clr(emails.join(' | '),'green','bright')} ${clr('['+source+']','gray')} ${e}`);
  } else {
    console.log(` ${clr('>','red')} ${hcp} ${clr('NOT FOUND','red')} ${clr('['+biz+']','gray')} ${e}`);
  }
}

// Simple log
function log(msg, type='INFO') {
  if (['SKIP','HUMAN'].includes(type)) return;
  const t = clr(new Date().toLocaleTimeString(), 'gray');
  const map = {
    INFO:'white', OK:'green', ERROR:'red', WARN:'yellow',
    FOUND:'green', FB:'blue', WEB:'cyan', CF:'magenta',
  };
  console.log(` ${t}  ${clr(msg, map[type]||'white')}`);
}

// ─── BANNER ────────────────────────────────────────────────
function printBanner() {
  // 24-bit ANSI color helpers
  const rgb  = (r,g,b) => `\x1b[38;2;${r};${g};${b}m`;
  const bgRgb= (r,g,b) => `\x1b[48;2;${r};${g};${b}m`;
  const RST  = '\x1b[0m';
  const BOLD = '\x1b[1m';
  const DIM  = '\x1b[2m';

  // Palette
  const W    = rgb(220,230,255);          // bright white-blue
  const B1   = rgb(80,140,255);           // bright blue
  const B2   = rgb(40,90,200);            // mid blue
  const B3   = rgb(20,50,140);            // dark blue
  const CY   = rgb(100,200,255);          // cyan accent
  const GR   = rgb(130,150,180);          // gray-blue
  const DGR  = rgb(60,70,100);            // dark gray

  const w = (process.stdout.columns || 100);
  const pad = (s, total) => {
    const visLen = s.replace(/\x1b\[[^m]*m/g,'').length;
    const left   = Math.max(0, Math.floor((total - visLen) / 2));
    return ' '.repeat(left) + s;
  };
  const ln = (s) => console.log(pad(s, w));

  console.clear();
  console.log('');

  // ── OUTER BORDER TOP ──
  ln(`${B2}╔${'═'.repeat(91)}╗${RST}`);
  ln(`${B2}║${' '.repeat(91)}║${RST}`);

  // ── BINARY SIDES + BUTTERFLY ROWS ──
  const BIN = [
    ['00100010 01000110 01100101','01101100 01101110 01101111'],
    ['01100001 01110010 01101110','00100000 01010031 01100031'],
    ['01101111 01110100 00101100','01110010 01100001 01110030'],
    ['00100000 01001000 01100101','01100101 01110010 00101110'],
  ];

  const BUTTERFLY = [
    `${DIM}${W}          ·  ·  ✦  ·  ✦  ·  ✦  ·  ·          ${RST}`,
    `${W}      ░▒▓ ▄▀▀▀▀▀▄ ░${B1}✦${W}░ ▄▀▀▀▀▀▄ ▓▒░      ${RST}`,
    `${W}    ▒▓█ ▄█▀░░▄▄░░▀█▄${B1}╬${W}▄█▀░░▄▄░░▀█▄ █▓▒    ${RST}`,
    `${W}   ▓██▄▀█▓░${CY}▄███▄${W}░▓${B1}╬╬${W}▓░${CY}▄███▄${W}░▓█▀▄██▓   ${RST}`,
    `${W}  ▓███▀░▓░${CY}█${B1}◈◈◈${CY}█${W}░▓${B1}╬╬╬${W}▓░${CY}█${B1}◈◈◈${CY}█${W}░▓░▀███▓  ${RST}`,
    `${W}  ███▓░░▓${CY}▄█████▄${W}▓${B1}╬╬╬╬${W}▓${CY}▄█████▄${W}▓░░▓███  ${RST}`,
    `${B1}  ▓██░▒▓${W}▀▀▀█▀▀▀${B1}▓╬╬╬╬╬▓${W}▀▀▀█▀▀▀${B1}▓▒░██▓  ${RST}`,
    `${B1}  ░██▄▒${W}░▄▄▄▄▄▄▄${B1}▓╬╬╬╬╬╬▓${W}▄▄▄▄▄▄▄${B1}░▒▄██░  ${RST}`,
    `${B1}   ▀███${W}▄${B1}▓▓▓▓▓▓▓╬╬╬╬╬╬╬╬▓▓▓▓▓▓▓${W}▄${B1}███▀   ${RST}`,
    `${B2}    ▀▀██${B1}▓╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬▓${B2}██▀▀    ${RST}`,
    `${B2}     ${B1}▀▓╬╬╬╬${W}░░▄${B1}╬╬╬╬╬╬╬${W}▄░░${B1}╬╬╬╬▓${B2}▀     ${RST}`,
    `${B3}      ${B2}▓╬╬╬${B1}╬╬╬${W}▄▄▀${B1}╬╬╬╬╬${W}▀▄▄${B1}╬╬╬${B2}╬╬╬▓${B3}      ${RST}`,
    `${B3}       ${B2}░${B1}╬╬╬╬╬${W}▄▄▄${B1}╬╬╬╬╬${W}▄▄▄${B1}╬╬╬╬╬${B2}░${B3}       ${RST}`,
    `${B3}        ${B1}▓╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬▓${B3}        ${RST}`,
    `${B3}         ${B2}▀▓${B1}╬╬╬╬╬╬╬${W}▄▀▄${B1}╬╬╬╬╬╬╬${B2}▓▀${B3}         ${RST}`,
    `${B3}          ${B2}░▓${B1}╬╬╬╬╬${W}█████${B1}╬╬╬╬╬${B2}▓░${B3}          ${RST}`,
    `${B3}           ${B2}▒${B1}╬╬╬╬╬${W}▀███▀${B1}╬╬╬╬╬${B2}▒${B3}           ${RST}`,
    `${B3}            ${B1}▄╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬▄${B3}            ${RST}`,
    `${B2}           ${B1}▓╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬▓${B2}           ${RST}`,
    `${B2}          ${W}▄${B1}╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬${W}▄${B2}          ${RST}`,
    `${B2}         ${W}▄▀${B1}╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬${W}▀▄${B2}         ${RST}`,
    `${B1}        ${W}▄▀▀${B1}╬╬╬╬╬${W}░░${B1}╬╬╬╬╬╬╬${W}░░${B1}╬╬╬╬╬${W}▀▀▄${B1}        ${RST}`,
    `${B1}       ${W}▄▀░░▀${B1}▄╬╬╬${W}░░${B1}╬╬╬╬╬╬╬${W}░░${B1}╬╬╬${W}▄▀░░▀▄${B1}       ${RST}`,
    `${W}      ▄▀░▒▒░░▀▄${B1}╬╬╬╬╬╬╬╬╬╬╬${W}▄▀░▒▒░░▀▄      ${RST}`,
    `${W}     ▀░░▒▒▒▒░░░▀▄▄${B1}╬╬╬╬╬${W}▄▄▀░░▒▒▒▒░░░▀     ${RST}`,
    `${GR}    ▀▄░░▒▒▒▒▒░▄▀  ▀${B1}╬╬╬${GR}▀  ▀▄░▒▒▒▒▒░░▄▀    ${RST}`,
    `${GR}      ▀▀▄▄▄▄▀▀      ${B1}▓▓▓      ${GR}▀▀▄▄▄▄▀▀      ${RST}`,
    `${DIM}${GR}                   ▄█▄                          ${RST}`,
    `${DIM}${GR}                  █████                         ${RST}`,
    `${DIM}${GR}                   ▀█▀                          ${RST}`,
  ];

  // Print butterfly rows with binary flanking (first 4 rows)
  for (let i = 0; i < BUTTERFLY.length; i++) {
    const bf  = BUTTERFLY[i];
    if (i < BIN.length) {
      const binL = `${DIM}${B2}${BIN[i][0]}${RST}`;
      const binR = `${DIM}${B2}${BIN[i][1]}${RST}`;
      ln(`${B2}║${RST}  ${binL}   ${bf}   ${binR}  ${B2}║${RST}`);
    } else {
      ln(`${B2}║${RST}  ${' '.repeat(25)} ${bf} ${' '.repeat(25)}  ${B2}║${RST}`);
    }
  }

  ln(`${B2}║${' '.repeat(91)}║${RST}`);

  // ── CICADA 3301 TITLE ──
  const T = BOLD+B1;
  const TD= BOLD+rgb(30,70,180);
  const titleLines = [
    `${T}  ██████╗ ██╗ ██████╗ █████╗ ██████╗  █████╗     ██████╗ ██████╗  ██████╗  ██╗  ${RST}`,
    `${T} ██╔════╝ ██║██╔════╝██╔══██╗██╔══██╗██╔══██╗   ╚════██╗╚════██╗██╔═══██╗███║  ${RST}`,
    `${T} ██║      ██║██║     ███████║██║  ██║███████║    █████╔╝  █████╔╝██║   ██║╚██║  ${RST}`,
    `${T} ██║      ██║██║     ██╔══██║██║  ██║██╔══██║    ╚═══██╗ ╚═══██╗██║   ██║ ██║  ${RST}`,
    `${T} ╚██████╗ ██║╚██████╗██║  ██║██████╔╝██║  ██║   ██████╔╝ ██████╔╝╚██████╔╝ ██║  ${RST}`,
    `${TD} ╚═════╝ ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═════╝  ╚═════╝  ╚═════╝  ╚═╝  ${RST}`,
  ];
  for (const tl of titleLines) {
    ln(`${B2}║${RST}${tl}${B2}║${RST}`);
  }

  ln(`${B2}║${' '.repeat(91)}║${RST}`);

  // ── BEGIN ENCRYPTED TRANSMISSION ──
  const subT = `${BOLD}${W}[ ${CY}B E G I N   E N C R Y P T E D   T R A N S M I S S I O N${W} ]${RST}`;
  ln(`${B2}║${RST}${pad(subT, 91)}${B2}║${RST}`);

  ln(`${B2}║${' '.repeat(91)}║${RST}`);

  // ── MESSAGE BOX ──
  const boxW = 55;
  const boxL = `${B1}╔${'═'.repeat(boxW-2)}╗${RST}`;
  const boxB = `${B1}╚${'═'.repeat(boxW-2)}╝${RST}`;
  const boxLine = (txt, color) => {
    const vis = txt.replace(/\x1b\[[^m]*m/g,'').length;
    const pad2 = Math.max(0, Math.floor((boxW - 2 - vis) / 2));
    const padR = Math.max(0, boxW - 2 - vis - pad2);
    return `${B1}║${RST}${' '.repeat(pad2)}${color}${txt}${RST}${' '.repeat(padR)}${B1}║${RST}`;
  };

  const msgLine1 = boxLine('Hello.',       W+BOLD);
  const msgLine2 = boxLine('Your scraper has begun.', W+BOLD);
  const msgLine3 = boxLine('Good luck.',   W+BOLD);
  const msgLine4 = boxLine('WE ARE EVERYWHERE', CY+BOLD);

  ln(`${B2}║${RST}  ${boxL}  ${B2}║${RST}`);
  ln(`${B2}║${RST}  ${msgLine1}  ${B2}║${RST}`);
  ln(`${B2}║${RST}  ${msgLine2}  ${B2}║${RST}`);
  ln(`${B2}║${RST}  ${msgLine3}  ${B2}║${RST}`);
  ln(`${B2}║${RST}  ${boxLine('─'.repeat(boxW-12), DGR)}  ${B2}║${RST}`);
  ln(`${B2}║${RST}  ${msgLine4}  ${B2}║${RST}`);
  ln(`${B2}║${RST}  ${boxB}  ${B2}║${RST}`);

  ln(`${B2}║${' '.repeat(91)}║${RST}`);

  // ── BORDER BOTTOM ──
  ln(`${B2}╚${'═'.repeat(91)}╝${RST}`);

  console.log('');

  // ── COLOR GUIDE ──
  const G = `${BOLD}${W}`;
  console.log(pad(`${G}COLOR GUIDE:${RST}`, w));
  console.log('');
  console.log(pad(`  ${BOLD}${W}✔ WHITE/BLUE${RST}  ${W}= Email FOUND (website ya FB se)${RST}`, w));
  console.log(pad(`  ${BOLD}${rgb(255,60,60)}✘ RED       ${RST}  ${W}= NOT FOUND${RST}`, w));
  console.log(pad(`  ${BOLD}${B1}● BLUE      ${RST}  ${W}= Facebook action (search/login/direct)${RST}`, w));
  console.log(pad(`  ${BOLD}${rgb(255,80,255)}● MAGENTA   ${RST}  ${W}= CloudFlare email decode${RST}`, w));
  console.log(pad(`  ${BOLD}${CY}● CYAN      ${RST}  ${W}= Website crawling${RST}`, w));
  console.log(pad(`  ${BOLD}${rgb(255,220,50)}● YELLOW    ${RST}  ${W}= Warning / phone number${RST}`, w));
  console.log('');
}

// ══════════════════════════════════════════════════════════
//  CLOUDFLARE DECODE
// ══════════════════════════════════════════════════════════
function decodeCfEmail(hex) {
  try {
    hex = hex.replace(/[^0-9a-fA-F]/g,'');
    const key = parseInt(hex.substring(0,2),16);
    let email = '';
    for (let i=2; i<hex.length; i+=2)
      email += String.fromCharCode(parseInt(hex.substring(i,i+2),16) ^ key);
    return email.includes('@') ? email : null;
  } catch { return null; }
}

function extractCfEmails($, html) {
  const out = [];
  $('[data-cfemail]').each((_,el) => {
    const d = decodeCfEmail($(el).attr('data-cfemail'));
    if (d) out.push(d);
  });
  $('a[href*="email-protection"]').each((_,el) => {
    const m = ($(el).attr('href')||'').match(/#([0-9a-fA-F]+)/);
    if (m) { const d = decodeCfEmail(m[1]); if (d) out.push(d); }
  });
  (html.match(/(?:data-cfemail|email-protection#)([0-9a-fA-F]+)/g)||[]).forEach(m => {
    const hex = m.split(/[#"]/)[1];
    if (hex) { const d = decodeCfEmail(hex); if (d) out.push(d); }
  });
  return out;
}

// ══════════════════════════════════════════════════════════
//  STRUCTURED EXTRACTORS
// ══════════════════════════════════════════════════════════

// JSON-LD — pull email + telephone from any nested schema.org object
function walkJsonLd(node, emails, phones) {
  if (!node || typeof node !== 'object') return;
  if (Array.isArray(node)) { node.forEach(n => walkJsonLd(n, emails, phones)); return; }
  for (const [k, v] of Object.entries(node)) {
    const key = k.toLowerCase();
    if (typeof v === 'string') {
      if (key === 'email' || key.endsWith('email')) emails.push(v.replace(/^mailto:/i,'').trim());
      if (key === 'telephone' || key === 'phone' || key.endsWith('phone')) phones.push(v.trim());
    } else if (v && typeof v === 'object') {
      walkJsonLd(v, emails, phones);
    }
  }
}
function extractJsonLd($) {
  const emails = [], phones = [];
  $('script[type]').each((_,el) => {
    const type = ($(el).attr('type')||'').toLowerCase();
    if (!type.includes('ld+json')) return;
    const txt = $(el).contents().text() || $(el).text() || '';
    let data;
    try { data = JSON.parse(txt); }
    catch {
      // some sites concatenate multiple JSON-LD blocks — try a lenient split
      try { data = JSON.parse('[' + txt.replace(/}\s*{/g, '},{') + ']'); } catch { return; }
    }
    walkJsonLd(data, emails, phones);
  });
  return { emails, phones };
}

// data-email / data-mail (high), plus aria-label / content / title / alt / value (medium)
function extractAttrCandidates($) {
  const out = [];
  const MED_ATTRS = ['aria-label','content','title','alt','value','data-original-title'];
  $('*').each((_,el) => {
    const a = el.attribs;
    if (!a) return;
    for (const name of ['data-email','data-mail']) {
      if (a[name] && a[name].includes('@')) out.push({ raw:a[name], source:name, confidence:'high' });
    }
    for (const name of MED_ATTRS) {
      if (a[name] && a[name].includes('@')) out.push({ raw:a[name], source:'attr-'+name, confidence:'medium' });
    }
  });
  return out;
}

// Visible text via SEPARATE text nodes joined with spaces (prevents phone/email glue).
// Assumes script/style/template/noscript already removed from $.
function extractTextWithSpaces($) {
  const parts = [];
  const scope = $('body').length ? $('body') : $.root();
  scope.find('*').addBack().contents().each((_, node) => {
    if (node.type === 'text') {
      const t = (node.data || '').replace(/\s+/g,' ').trim();
      if (t) parts.push(t);
    }
  });
  return parts.join(' ');
}

// ══════════════════════════════════════════════════════════
//  WEBSITE SCRAPER
// ══════════════════════════════════════════════════════════
// SKILL: rate-limit / block awareness. A 429/403/503 from a host stops further
// requests to that host for this run and drops global concurrency to 1.
const blockedHosts = new Set();
const hostOf = u => { try { return new URL(u).host; } catch { return ''; } };
function noteBlock(url, status) {
  const h = hostOf(url);
  if (h && !blockedHosts.has(h)) {
    blockedHosts.add(h);
    log(`HTTP ${status} from ${h} — not retrying this site; reducing concurrency`, 'WARN');
  }
  if (CONFIG.CONCURRENCY > 1) CONFIG.CONCURRENCY = 1;
}

async function fetchHtml(url) {
  const res = await axios.get(url, {
    timeout: CONFIG.WEB_TIMEOUT,
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5',
    },
    maxRedirects: 5,
  });
  return res.data;
}

// parsePage → { cands:[{raw,source,confidence,page}], phones, fbLinks, contLinks }
function parsePage(html, pageUrl, baseUrl) {
  const $ = cheerio.load(html);
  const cands = [], phones = [], fbLinks = [], contLinks = [];
  const push = (raw, source, confidence) => {
    if (raw && String(raw).includes('@')) cands.push({ raw, source, confidence, page: pageUrl });
  };

  // 1. mailto: links — most reliable
  $('a[href^="mailto:"]').each((_,el) => {
    const e = ($(el).attr('href')||'').replace(/^mailto:/i,'').split('?')[0].trim();
    if (e) push(e, 'mailto', 'high');
  });

  // 2. JSON-LD email + telephone (high) — must run BEFORE scripts are stripped
  const ld = extractJsonLd($);
  ld.emails.forEach(e => push(e, 'json-ld', 'high'));
  phones.push(...ld.phones);

  // 3. attributes: data-email/data-mail (high), aria-label/content/… (medium)
  for (const a of extractAttrCandidates($)) push(a.raw, a.source, a.confidence);

  // 4. CloudFlare decoded (high)
  const cf = extractCfEmails($, html);
  if (cf.length) { log(`CF decoded: ${cf.join(', ')}`, 'CF'); cf.forEach(e => push(e, 'cloudflare', 'high')); }

  // 5. raw HTML matches (LOW confidence)
  (html.match(EMAIL_FIND) || []).forEach(e => push(e, 'html', 'low'));

  // ─── PHONES (kept separate from email extraction) ───
  $('a[href^="tel:"]').each((_,el) => {
    phones.push(($(el).attr('href')||'').replace(/^tel:/i,'').trim());
  });

  // ─── FACEBOOK LINKS ───
  $('a[href*="facebook.com"]').each((_,el) => {
    const href = ($(el).attr('href')||'').split('?')[0].replace(/\/$/,'');
    const m    = href.match(FB_SOCIAL);
    if (m && m[1]) fbLinks.push(`https://www.facebook.com/${m[1]}`);
  });

  // ─── CONTACT PAGE LINKS ───
  try {
    const origin = new URL(baseUrl).origin;
    $('a[href]').each((_,el) => {
      const href = $(el).attr('href')||'';
      const text = ($(el).text()||'').toLowerCase();
      const full = href.startsWith('http') ? href : href.startsWith('/') ? origin+href : null;
      if (!full || !full.startsWith(origin)) return;
      if (CONFIG.CONTACT_KEYWORDS.some(kw => full.toLowerCase().includes(kw) || text.includes(kw)))
        contLinks.push(full.split('?')[0]);
    });
  } catch {}

  // ─── VISIBLE TEXT (medium) — strip non-visible content first ───
  $('script, style, template, noscript, svg').remove();
  const vis = extractTextWithSpaces($);
  (vis.match(EMAIL_FIND) || []).forEach(e => push(e, 'text', 'medium'));

  // ─── DE-OBFUSCATED [at]/[dot] emails (medium) ───
  const deob = deobfuscateText(vis);
  (deob.match(EMAIL_FIND) || []).forEach(e => push(e, 'deobfuscated', 'medium'));

  // phones from visible text (not raw html — avoids markup noise)
  phones.push(...(vis.match(PHONE_REGEX) || []));

  const refined = refineCandidates(cands);
  log(`  🔍 ${pageUrl.slice(0,50)} → ${refined.clean.length} email(s), ${refined.suspicious.length} suspicious, ${filterPhones(phones).length} phone(s)`, 'WEB');

  return {
    cands,
    phones:    filterPhones(phones),
    fbLinks:   [...new Set(fbLinks)],
    contLinks: [...new Set(contLinks)].slice(0,5),
  };
}

async function scrapeWebsite(baseUrl) {
  const cands = [], allPhones = [], allFb = [];
  const visited = new Set();
  let mainParsed = null;
  let mainStatus = 0;   // SKILL: HTTP status if the main page was refused

  async function doPage(url) {
    const clean = url.split('?')[0].replace(/\/$/,'');
    if (visited.has(clean)) return null;
    visited.add(clean);
    if (blockedHosts.has(hostOf(url))) return null;   // SKILL: do not hammer a blocking site
    try {
      await sleep(rInt(CONFIG.DELAY_WEB.min, CONFIG.DELAY_WEB.max));
      const html   = await fetchHtml(url);
      const parsed = parsePage(html, url, baseUrl);
      cands.push(...parsed.cands);
      allPhones.push(...parsed.phones);
      allFb.push(...parsed.fbLinks);
      return parsed;
    } catch (err) {
      const st = err && err.response && err.response.status;
      if (st === 429 || st === 403 || st === 503) { noteBlock(url, st); if (url.split('?')[0].replace(/\/$/,'') === baseUrl) mainStatus = st; }
      return null;
    }
  }

  // "strong" = at least one high/medium confidence CLEAN email
  const hasStrong = () => refineCandidates(cands).clean.some(c => c.confidence === 'high' || c.confidence === 'medium');

  mainParsed = await doPage(baseUrl);

  // Sub-pages — crawl if we don't yet have a strong email
  if (!hasStrong()) {
    await Promise.allSettled(CONFIG.PRIORITY_PAGES.map(s => doPage(baseUrl+s)));
  }

  // Contact links — KEEP crawling when we only have low-confidence (or no) emails
  if (!hasStrong() && mainParsed?.contLinks?.length > 0) {
    for (const link of mainParsed.contLinks) {
      await doPage(link);
      if (hasStrong()) break;
    }
  }

  const refined = refineCandidates(cands);
  return {
    emails:     refined.clean,       // [{email,source,confidence,suspicious:false,reason,page}]
    suspicious: refined.suspicious,  // [{...suspicious:true}]
    phones:     filterPhones(allPhones),
    fbLinks:    [...new Set(allFb)],
    blockedStatus: blockedHosts.has(hostOf(baseUrl)) ? (mainStatus || 429) : 0,
  };
}

// ══════════════════════════════════════════════════════════
//  COMBINED FLOW
// ══════════════════════════════════════════════════════════
// ─── BUILD ROWS — one row per email ───────────────────────
// emailObjs: [{email,source,confidence,suspicious,reason,page}]
// Returns an ARRAY of rows (one per email, or one no-email row)
function buildRows(url, biz, emailObjs, phones, fbUrl, status, channel='', error='') {
  const now = new Date().toISOString();
  const phonesStr = (phones||[]).join(' | ');

  if (!emailObjs || emailObjs.length === 0) {
    return [{
      url, business_name: biz,
      email: '',
      phone: phonesStr,
      email_count: 0,
      email_source: '',
      confidence: '',
      suspicious: false,
      notes: '',
      source_page: '',
      fb_page_url: fbUrl,
      channel,
      status, error,
      scraped_at: now,
    }];
  }

  return emailObjs.map(o => ({
    url, business_name: biz,
    email: o.email,
    phone: phonesStr,
    email_count: emailObjs.length,
    email_source: o.source || '',
    confidence: o.confidence || '',
    suspicious: !!o.suspicious,
    notes: o.reason || '',
    source_page: o.page || '',
    fb_page_url: fbUrl,
    channel,
    status, error,
    scraped_at: now,
  }));
}

async function processUrl(url, idx) {
  const norm  = normalizeUrl(url);
  const biz   = getBusinessName(norm);
  const start = Date.now();

  urlHeader(norm, idx);

  // STEP 1: Website (the only channel in the skill version)
  let web = { emails:[], suspicious:[], phones:[], fbLinks:[], blockedStatus:0 };
  try { web = await scrapeWebsite(norm); } catch {}

  if (web.suspicious?.length) recordSuspicious(norm, biz, web.suspicious, 'website');

  log(`  📧 Emails: ${web.emails.length} | 🚩 Suspicious: ${web.suspicious.length} | 📞 Phones: ${web.phones.length}`, 'INFO');

  if (web.emails.length > 0) {
    const el = ((Date.now()-start)/1000).toFixed(1);
    urlResult(biz, web.emails.map(e=>e.email), 'website', el);
    STATS.found++; STATS.fromWeb++;
    return buildRows(norm, biz, web.emails, web.phones, '', 'found', 'website');
  }

  const el = ((Date.now()-start)/1000).toFixed(1);
  urlResult(biz, [], '', el);

  // SKILL: site refused us (429/403/503) -> record as 'blocked' with the reason, never retry.
  if (web.blockedStatus) {
    STATS.blocked++;
    return buildRows(norm, biz, [], web.phones, web.fbLinks[0] || '', 'blocked', '', `HTTP ${web.blockedStatus} - site blocked or rate-limited requests; not retried`);
  }

  STATS.notFound++;
  // SKILL: a Facebook link the site itself publishes is kept as a lead hint (no Facebook access is attempted).
  return buildRows(norm, biz, [], web.phones, web.fbLinks[0] || '', 'not_found', '');
}

// SKILL: --fresh archives any previous run files instead of deleting them.
function archivePreviousRun() {
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const moved = [];
  for (const f of [CONFIG.CACHE_FILE, CONFIG.OUTPUT_FILE, CONFIG.SUSPICIOUS_FILE]) {
    if (!fs.existsSync(f)) continue;
    const dest = f.replace(/(\.[^.]+)$/, `_archived_${stamp}$1`);
    fs.renameSync(f, dest);
    moved.push(path.basename(dest));
  }
  if (moved.length) console.log(clr(`  --fresh: archived previous run files → ${moved.join(', ')}`, 'yellow'));
}

// SKILL: clean exit codes for agents: 2 = bad/missing input.
function inputError(msg) {
  console.error(clr('  ERROR: ' + msg, 'red', 'bright'));
  process.exit(2);
}

// ─── MAIN ──────────────────────────────────────────────────
async function main() {
  if (FANCY) printBanner();
  fs.mkdirSync(WORKDIR, { recursive: true });

  if (ARGV.includes('--fresh')) archivePreviousRun();

  if (!fs.existsSync(CONFIG.INPUT_FILE)) {
    inputError(`input file not found: ${CONFIG.INPUT_FILE}`);
  }

  let rows;
  try {
    rows = parse(fs.readFileSync(CONFIG.INPUT_FILE,'utf8'),
      { columns:true, skip_empty_lines:true, trim:true, bom:true }
    );
  } catch (e) { inputError('input CSV could not be parsed: ' + e.message); }
  if (!rows.length) inputError('input CSV has a header but no rows');

  const col = Object.keys(rows[0]).find(k =>
    ['url','website','link','domain','site'].includes(k.toLowerCase())
  );
  if (!col) {
    inputError('no url column found. Header must be one of: url, website, link, domain, site');
  }

  const urls  = rows.map(r=>r[col]).filter(Boolean);
  if (!urls.length) inputError(`column "${col}" has no values`);
  STATS.total = urls.length;

  loadSuspicious();
  const cache   = loadCache();
  const results = [];

  // ─── RESUME — restore ALL email rows per URL (not just the first) ───
  let processedUrls = 0;
  for (const u of urls) {
    const key = u.trim();
    if (!cache[key]) continue;
    let arr = cache[key];
    if (!Array.isArray(arr)) arr = [arr];   // backward-compat with old single-row cache
    results.push(...arr);
    processedUrls++;
    const rep = arr[0] || {};
    if (rep.status === 'found') {
      STATS.found++;
      if (rep.channel === 'website') STATS.fromWeb++;
    } else if (rep.status === 'error') {
      STATS.errors++;
    } else if (rep.status === 'blocked') {
      STATS.blocked++;
    } else {
      STATS.notFound++;
    }
  }
  STATS.processed = processedUrls;

  console.log(clr(`  Workdir      : ${WORKDIR}`, 'gray'));
  console.log(clr(`  Total URLs   : ${urls.length}`, 'cyan','bright'));
  console.log(clr(`  Resume from  : ${STATS.processed} already done`, 'gray'));
  console.log(clr(`  New to scrape: ${urls.length - STATS.processed}`, 'yellow'));
  console.log(clr(`  Concurrency  : ${CONFIG.CONCURRENCY} parallel`, 'green'));
  console.log('');

  const queue = urls.filter(u => !cache[u.trim()]);
  console.log('');
  if (FANCY) startCyberUI();

  let running = 0;
  let idx     = STATS.processed;
  let stopping = false;

  // SKILL: Ctrl+C / SIGTERM → stop queueing, let in-flight URLs finish (cache is saved per URL).
  const onStop = () => {
    if (stopping) process.exit(130);
    stopping = true;
    console.log('\n  Stop requested — finishing in-flight URLs. Re-run the same command to resume.');
  };
  process.on('SIGINT', onStop);
  process.on('SIGTERM', onStop);

  async function runOne(url) {
    running++;
    idx++;
    const trimmed = url.trim();
    let builtRows;
    try {
      builtRows = await processUrl(trimmed, idx);
    } catch(e) {
      STATS.errors++;
      builtRows = buildRows(normalizeUrl(trimmed), getBusinessName(trimmed), [], [], '', 'error', '', e.message);
    }
    // Cache: store the FULL array of rows so resume restores every email row
    cache[trimmed] = builtRows;
    results.push(...builtRows);
    saveCache(cache);
    saveOutput(results);
    STATS.processed++;
    if (!FANCY) console.log(`PROGRESS ${STATS.processed}/${STATS.total} found=${STATS.found} not_found=${STATS.notFound} blocked=${STATS.blocked} errors=${STATS.errors}`);
    running--;
  }

  for (let i=0; i<queue.length; i++) {
    if (stopping) break;
    while (running >= CONFIG.CONCURRENCY) await sleep(150);
    if (stopping) break;
    runOne(queue[i]);
    await sleep(rInt(CONFIG.DELAY_BETWEEN.min, CONFIG.DELAY_BETWEEN.max));
  }
  while (running > 0) await sleep(200);

  if (FANCY) stopCyberUI();

  // ─── FINAL ────────────────────────────────────────────
  const totalTime = ((Date.now()-STATS.startTime)/60000).toFixed(1);
  const complete = STATS.processed >= STATS.total;
  console.log('');
  console.log(clr('  ══════════════════════════════════════════════════════', 'green','bright'));
  console.log(clr(complete ? '  RUN COMPLETE' : '  RUN STOPPED EARLY (resume by re-running the same command)', 'green','bright'));
  console.log(clr('  ══════════════════════════════════════════════════════', 'green','bright'));
  console.log(clr(`  Processed       : ${STATS.processed}/${STATS.total}`, 'white','bright'));
  console.log(clr(`  Total Rows      : ${results.length}`, 'white','bright'));
  console.log(clr(`  Emails Found    : ${STATS.found}`, 'green','bright'));
  console.log(clr(`  Website         : ${STATS.fromWeb}`, 'cyan'));
  console.log(clr(`  Suspicious      : ${STATS.suspicious}`, 'yellow'));
  console.log(clr(`  Not Found       : ${STATS.notFound}`, 'red'));
  console.log(clr(`  Blocked         : ${STATS.blocked}`, 'yellow'));
  console.log(clr(`  Errors          : ${STATS.errors}`, 'yellow'));
  console.log(clr(`  Total Time      : ${totalTime} min`, 'gray'));
  console.log(clr(`  Output File     : ${CONFIG.OUTPUT_FILE}`, 'gray'));
  console.log(clr(`  Suspicious File : ${CONFIG.SUSPICIOUS_FILE}`, 'gray'));
  console.log(clr('  ══════════════════════════════════════════════════════', 'green','bright'));
  console.log('');
}

// ─── SELF-TEST (pure functions only) — run: node email-scraper.js --selftest ───
function runSelfTest() {
  const cases = [
    ['u003einfo@bakedbyael.com',            'info@bakedbyael.com', false],
    ['u003emealplans@udel.edu',             'mealplans@udel.edu',  false],
    ['usa2527283899info@beaugro.com',       'info@beaugro.com',    false],
    ['il773.276.8888hello@bangbangpie.con', 'hello@bangbangpie.con', true ], // typo kept + flagged
    ['john2024@gmail.com',                  'john2024@gmail.com',  false],
    ['contact@sansoxygen.com',              'contact@sansoxygen.com', false],
    ['&#105;nfo&#64;example.org',           null,                  false],  // blacklisted domain → null
    ['sales@gmial.com',                     'sales@gmial.com',     true ],  // provider typo flagged
  ];
  let pass = 0;
  for (const [raw, expEmail, expSusp] of cases) {
    const n = normalizeEmail(raw);
    const gotEmail = n ? n.email : null;
    const blacklisted = n && EMAIL_BLACKLIST.some(b => n.email.includes(b));
    const finalEmail = blacklisted ? null : gotEmail;
    const ok = finalEmail === expEmail && (finalEmail === null || n.suspicious === expSusp);
    if (ok) pass++;
    console.log(`${ok?'✔':'✘'} ${raw.padEnd(38)} → ${finalEmail}  susp=${n?n.suspicious:'-'}${n&&n.reason?('  ('+n.reason+')'):''}`);
  }
  // de-obfuscation
  const deob = deobfuscateText('reach us: sales (at) foocorp (dot) com or bob at bar dot io');
  console.log('deobfuscate →', deob.match(EMAIL_FIND));
  console.log(`\n${pass}/${cases.length} normalizeEmail cases passed`);
}

if (process.argv.includes('--selftest')) {
  runSelfTest();
} else {
  main().catch(async err => {
    if (FANCY) stopCyberUI();
    console.error(clr('\n  FATAL: '+err.message, 'red','bright'));
    process.exit(1);
  });
}
