#!/usr/bin/env node
// validate-input.js — inspect and clean a URL list BEFORE scraping.
//
// Usage:
//   node scripts/validate-input.js <file.csv|file.txt> [--write-clean <out.csv>] [--force] [--allow-local]
//
// - .csv: needs a header column named url / website / link / domain / site
// - .txt: one URL or domain per line
// - Bare domains get "https://" prepended in the cleaned output (the scraper
//   itself only checks startsWith('http'), so "httpbin.org" would be mishandled).
// - Rejects: invalid hosts, non-http(s) schemes, localhost / private / link-local
//   addresses (unless --allow-local, used only by the test-suite), duplicates.
// - Never overwrites an existing --write-clean target unless --force is given.
// Exit codes: 0 = at least one valid URL, 2 = nothing usable / bad input.

const fs = require('fs');
const path = require('path');
const { parse } = require('csv-parse/sync');
const { stringify } = require('csv-stringify/sync');

const argv = process.argv.slice(2);
const file = argv.find(a => !a.startsWith('--') && argv[argv.indexOf(a) - 1] !== '--write-clean');
const flag = n => argv.includes(n);
const val  = n => { const i = argv.indexOf(n); return i >= 0 ? argv[i + 1] : undefined; };
const OUT = val('--write-clean');
const ALLOW_LOCAL = flag('--allow-local');

if (!file) { console.error('Usage: node scripts/validate-input.js <file.csv|file.txt> [--write-clean out.csv] [--force]'); process.exit(2); }
if (!fs.existsSync(file)) { console.error(`ERROR: file not found: ${file}`); process.exit(2); }

const URL_COLS = ['url', 'website', 'link', 'domain', 'site'];
const SOCIAL = ['facebook.com', 'instagram.com', 'twitter.com', 'x.com', 'linkedin.com', 'tiktok.com', 'youtube.com'];

function isPrivateHost(h) {
  h = h.toLowerCase().replace(/^\[|\]$/g, '');
  if (h === 'localhost' || h.endsWith('.localhost') || h.endsWith('.local') || h.endsWith('.internal')) return true;
  if (/^\d+\.\d+\.\d+\.\d+$/.test(h)) {
    const [a, b] = h.split('.').map(Number);
    return a === 10 || a === 127 || a === 0 || (a === 169 && b === 254) ||
           (a === 172 && b >= 16 && b <= 31) || (a === 192 && b === 168);
  }
  if (h.includes(':')) return h === '::1' || h.startsWith('fc') || h.startsWith('fd') || h.startsWith('fe80');
  return false;
}

function check(raw) {
  let s = String(raw || '').trim();
  if (!s) return { ok: false, reason: 'empty' };
  if (/^[a-z][a-z0-9+.-]*:/i.test(s) && !/^https?:\/\//i.test(s) && !/^[^/]+:\d+/.test(s))
    return { ok: false, reason: 'unsupported scheme (only http/https)' };
  const withScheme = /^https?:\/\//i.test(s) ? s : 'https://' + s;
  let u;
  try { u = new URL(withScheme); } catch { return { ok: false, reason: 'not a valid URL' }; }
  const host = u.hostname;
  if (!host.includes('.') && !host.includes(':') && host !== 'localhost') return { ok: false, reason: 'host has no dot (not a public domain)' };
  if (!ALLOW_LOCAL && isPrivateHost(host)) return { ok: false, reason: 'private/local address — not a public website' };
  const clean = withScheme.replace(/\/+$/, '');
  const social = SOCIAL.some(d => host === d || host.endsWith('.' + d));
  return { ok: true, clean, host, social, addedScheme: withScheme !== s };
}

// ---- read ----
const text = fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
let rawValues = [], column = '(one URL per line)';
if (/\.csv$/i.test(file)) {
  let rows;
  try { rows = parse(text, { columns: true, skip_empty_lines: true, trim: true }); }
  catch (e) { console.error('ERROR: CSV could not be parsed: ' + e.message); process.exit(2); }
  if (!rows.length) { console.error('ERROR: CSV has no data rows'); process.exit(2); }
  column = Object.keys(rows[0]).find(k => URL_COLS.includes(k.toLowerCase()));
  if (!column) { console.error(`ERROR: no URL column. Header is [${Object.keys(rows[0]).join(', ')}]; need one of: ${URL_COLS.join(', ')}`); process.exit(2); }
  rawValues = rows.map(r => r[column]);
} else {
  rawValues = text.split(/\r?\n/).map(l => l.trim()).filter(l => l && !l.startsWith('#'));
}

// ---- classify ----
const seen = new Set(), valid = [], invalid = [], dups = [], social = [], addedScheme = [];
rawValues.forEach((raw, i) => {
  if (raw === undefined || String(raw).trim() === '') return;       // blank cells are ignored, not errors
  const r = check(raw);
  if (!r.ok) { invalid.push({ line: i + 1, value: raw, reason: r.reason }); return; }
  const key = r.clean.toLowerCase();
  if (seen.has(key)) { dups.push({ line: i + 1, value: raw }); return; }
  seen.add(key);
  valid.push(r.clean);
  if (r.social) social.push(r.clean);
  if (r.addedScheme) addedScheme.push(r.clean);
});

const total = rawValues.filter(v => v !== undefined && String(v).trim() !== '').length;
console.log(`Input file      : ${path.resolve(file)}`);
console.log(`URL column      : ${column}`);
console.log(`Non-empty rows  : ${total}`);
console.log(`Valid (unique)  : ${valid.length}`);
console.log(`Duplicates      : ${dups.length}`);
console.log(`Invalid         : ${invalid.length}`);
invalid.slice(0, 20).forEach(x => console.log(`  - row ${x.line}: "${x.value}" → ${x.reason}`));
if (invalid.length > 20) console.log(`  … and ${invalid.length - 20} more`);
if (addedScheme.length) console.log(`Note            : ${addedScheme.length} bare domain(s) will get https:// in the cleaned file`);
if (social.length) console.log(`Warning         : ${social.length} social-media URL(s) (e.g. ${social[0]}) — these are not business websites; the scraper only reads public HTML and will usually find nothing`);
if (valid.length > 500) console.log(`Warning         : ${valid.length} URLs ≈ ${(valid.length * 12 / 3600).toFixed(1)}+ hours at ~12s/URL. Consider running in batches.`);

if (OUT) {
  if (fs.existsSync(OUT) && !flag('--force')) {
    console.error(`ERROR: ${OUT} already exists — refusing to overwrite (pass --force, or choose another path)`);
    process.exit(2);
  }
  if (!valid.length) { console.error('ERROR: nothing valid to write'); process.exit(2); }
  fs.mkdirSync(path.dirname(path.resolve(OUT)), { recursive: true });
  fs.writeFileSync(OUT, stringify(valid.map(u => ({ url: u })), { header: true }));
  console.log(`Cleaned CSV     : ${path.resolve(OUT)} (${valid.length} URLs)`);
}

if (!valid.length) { console.error('RESULT: no usable URLs'); process.exit(2); }
console.log('RESULT: OK');
