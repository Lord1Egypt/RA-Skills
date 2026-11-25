#!/usr/bin/env node
// summarize-run.js — report completed / failed / pending URLs for a run directory.
// Usage: node scripts/summarize-run.js [--workdir <dir>] [--input <file>] [--json]
// Reads input.csv, cache.json, output.csv and suspicious.csv (read-only; writes nothing).

const fs = require('fs');
const path = require('path');
const { parse } = require('csv-parse/sync');

const argv = process.argv.slice(2);
const val = n => { const i = argv.indexOf(n); return i >= 0 ? argv[i + 1] : undefined; };
const WORKDIR = path.resolve(val('--workdir') || process.cwd());
const INPUT = path.resolve(val('--input') ? val('--input') : path.join(WORKDIR, 'input.csv'));
const f = n => path.join(WORKDIR, n);

if (!fs.existsSync(INPUT)) { console.error('ERROR: input file not found: ' + INPUT); process.exit(2); }
const rows = parse(fs.readFileSync(INPUT, 'utf8'), { columns: true, skip_empty_lines: true, trim: true, bom: true });
const col = rows.length ? Object.keys(rows[0]).find(k => ['url', 'website', 'link', 'domain', 'site'].includes(k.toLowerCase())) : null;
if (!col) { console.error('ERROR: no url column in input'); process.exit(2); }
const urls = rows.map(r => r[col]).filter(Boolean).map(u => u.trim());

let cache = {};
try { if (fs.existsSync(f('cache.json'))) cache = JSON.parse(fs.readFileSync(f('cache.json'), 'utf8')); } catch (e) { console.error('WARN: cache.json unreadable: ' + e.message); }

const buckets = { found: [], not_found: [], blocked: [], error: [], pending: [] };
let emailRows = 0; const emails = new Set();
for (const u of urls) {
  const arr = cache[u] ? (Array.isArray(cache[u]) ? cache[u] : [cache[u]]) : null;
  if (!arr) { buckets.pending.push({ url: u }); continue; }
  const rep = arr[0] || {};
  const st = ['found', 'not_found', 'blocked', 'error'].includes(rep.status) ? rep.status : 'not_found';
  buckets[st].push({ url: u, error: rep.error || '' });
  for (const r of arr) if (r.email) { emailRows++; emails.add(String(r.email).toLowerCase()); }
}
let suspicious = 0;
if (fs.existsSync(f('suspicious.csv'))) {
  try { suspicious = parse(fs.readFileSync(f('suspicious.csv'), 'utf8'), { columns: true, skip_empty_lines: true }).length; } catch {}
}

const summary = {
  workdir: WORKDIR,
  input_urls: urls.length,
  completed: urls.length - buckets.pending.length,
  found: buckets.found.length,
  not_found: buckets.not_found.length,
  blocked: buckets.blocked.length,
  errors: buckets.error.length,
  pending_not_yet_processed: buckets.pending.length,
  email_rows: emailRows,
  unique_emails: emails.size,
  suspicious_rows: suspicious,
  output_csv: fs.existsSync(f('output.csv')) ? f('output.csv') : null,
  suspicious_csv: fs.existsSync(f('suspicious.csv')) ? f('suspicious.csv') : null,
  can_resume: buckets.pending.length > 0 && Object.keys(cache).length > 0,
};

if (argv.includes('--json')) {
  console.log(JSON.stringify({ summary, blocked: buckets.blocked, errors: buckets.error, pending: buckets.pending.slice(0, 50) }, null, 2));
} else {
  console.log(`Run directory   : ${summary.workdir}`);
  console.log(`Input URLs      : ${summary.input_urls}`);
  console.log(`Completed       : ${summary.completed}  (found ${summary.found}, not found ${summary.not_found}, blocked ${summary.blocked}, errors ${summary.errors})`);
  console.log(`Pending         : ${summary.pending_not_yet_processed}${summary.can_resume ? '  → re-run the same scrape command to resume' : ''}`);
  console.log(`Emails          : ${summary.unique_emails} unique (${summary.email_rows} rows), ${summary.suspicious_rows} suspicious`);
  if (buckets.blocked.length) { console.log('Blocked / rate-limited:'); buckets.blocked.forEach(x => console.log(`  - ${x.url}  ${x.error}`)); }
  if (buckets.error.length)   { console.log('Errors:'); buckets.error.forEach(x => console.log(`  - ${x.url}  ${x.error}`)); }
  console.log(`output.csv      : ${summary.output_csv || '(not created yet)'}`);
  console.log(`suspicious.csv  : ${summary.suspicious_csv || '(none)'}`);
}
