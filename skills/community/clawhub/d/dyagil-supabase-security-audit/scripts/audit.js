#!/usr/bin/env node
/**
 * Supabase security audit — runs a battery of read-only checks against a
 * Supabase project and prints a human-readable report.
 *
 * USAGE:
 *   node audit.js [--cred ~/.openclaw/credentials/supabase/credentials.env]
 *                 [--pooler aws-1-eu-central-1.pooler.supabase.com:6543]
 *                 [--public-tables profiles,deals,documents,...]
 *                 [--probe-uid <uuid>]   # an existing customer-role user id
 *                 [--target-uid <uuid>]  # another customer id to test data leaks
 *                 [--site https://example.com]
 *
 * The credentials file must define:
 *   SUPABASE_URL=...
 *   SUPABASE_PROJECT_REF=...
 *   SUPABASE_ANON_KEY=...
 *   SUPABASE_SERVICE_ROLE_KEY=...
 *   SUPABASE_DB_PASSWORD=...
 *
 * The audit is READ-ONLY for everything that matters. It WILL temporarily
 * elevate `--probe-uid` to test privilege escalation; the change is reverted
 * in a transaction and rolled back regardless of outcome.
 */

'use strict';
const fs = require('fs');
const path = require('path');
const https = require('https');

// ---- pg discovery (use whatever pg the host already has) ----
let Client;
const pgCandidates = [
  '/tmp/sb-tools/node_modules/pg',
  process.env.PG_PATH,
  'pg',
].filter(Boolean);
for (const p of pgCandidates) {
  try { ({ Client } = require(p)); break; } catch {}
}
if (!Client) {
  console.error('ERR: the `pg` package is required. Install it once with:');
  console.error('     mkdir -p /tmp/sb-tools && (cd /tmp/sb-tools && npm i pg)');
  process.exit(2);
}

// ---- CLI args ----
const args = Object.fromEntries(process.argv.slice(2).reduce((acc, cur, i, arr) => {
  if (cur.startsWith('--')) acc.push([cur.slice(2), arr[i + 1] && !arr[i + 1].startsWith('--') ? arr[i + 1] : true]);
  return acc;
}, []));

const credPath = args.cred || path.join(process.env.HOME, '.openclaw/credentials/supabase/credentials.env');
const pooler   = args.pooler || 'aws-1-eu-central-1.pooler.supabase.com:6543';
const site     = args.site;
const publicTables = (args['public-tables'] || 'profiles,deals,documents,invoices,inquiries,customer_events,tax_engagements').split(',');
const probeUid  = args['probe-uid'];
const targetUid = args['target-uid'];

if (!fs.existsSync(credPath)) {
  console.error('ERR: credentials file not found:', credPath);
  process.exit(2);
}
const cred = Object.fromEntries(
  fs.readFileSync(credPath, 'utf8').split('\n')
    .filter(l => l.includes('=') && !l.trim().startsWith('#'))
    .map(l => { const i = l.indexOf('='); return [l.slice(0, i).trim(), l.slice(i + 1).trim()]; })
);

for (const k of ['SUPABASE_URL', 'SUPABASE_PROJECT_REF', 'SUPABASE_ANON_KEY', 'SUPABASE_SERVICE_ROLE_KEY', 'SUPABASE_DB_PASSWORD']) {
  if (!cred[k]) { console.error('ERR: missing', k, 'in', credPath); process.exit(2); }
}

// ---- Output helpers ----
const findings = []; // {level: ok|warn|crit, area, msg}
const C = { ok: '\x1b[32m', warn: '\x1b[33m', crit: '\x1b[31m', dim: '\x1b[2m', bold: '\x1b[1m', reset: '\x1b[0m' };
const TTY = process.stdout.isTTY;
const fmt = (color, s) => TTY ? C[color] + s + C.reset : s;
function record(level, area, msg) {
  findings.push({ level, area, msg });
  const icon = { ok: '✅', warn: '🟡', crit: '🚨' }[level];
  console.log(`${icon} ${fmt('bold', area)} — ${msg}`);
}

// ---- Tiny REST helper ----
function rest(method, url, headers) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const req = https.request({
      method, hostname: u.hostname, port: u.port || 443,
      path: u.pathname + u.search,
      headers: Object.assign({ 'Accept': 'application/json' }, headers || {}),
    }, res => {
      let buf = '';
      res.on('data', c => buf += c);
      res.on('end', () => resolve({ status: res.statusCode, headers: res.headers, body: buf }));
    });
    req.on('error', reject);
    req.end();
  });
}

// ---- PG connection ----
const [host, port] = pooler.split(':');
const pg = new Client({
  host, port: Number(port || 6543),
  user: `postgres.${cred.SUPABASE_PROJECT_REF}`,
  password: cred.SUPABASE_DB_PASSWORD,
  database: 'postgres',
  ssl: { rejectUnauthorized: false },
  connectionTimeoutMillis: 15000,
});

// ============================================================
async function checkRlsCoverage() {
  console.log(fmt('bold', '\n=== 1. RLS coverage ==='));
  const r = await pg.query(`
    select tablename, rowsecurity
      from pg_tables
     where schemaname='public' and tablename not like 'pg_%'
     order by rowsecurity, tablename
  `);
  const off = r.rows.filter(x => !x.rowsecurity);
  if (off.length === 0) record('ok', 'RLS', `all ${r.rows.length} public tables have RLS enabled`);
  else record('crit', 'RLS', `${off.length} tables without RLS: ${off.map(x => x.tablename).join(', ')}`);
}

// ============================================================
async function checkAnonExposure() {
  console.log(fmt('bold', '\n=== 2. Anonymous reads ==='));
  for (const tbl of publicTables) {
    try {
      const r = await rest('GET', `${cred.SUPABASE_URL}/rest/v1/${tbl}?select=count`, {
        apikey: cred.SUPABASE_ANON_KEY,
        Authorization: 'Bearer ' + cred.SUPABASE_ANON_KEY,
        Prefer: 'count=exact',
      });
      const m = (r.headers['content-range'] || '').match(/\/(\d+)/);
      const n = m ? Number(m[1]) : null;
      if (n === null || n === 0) record('ok', 'anon:' + tbl, 'anonymous sees 0 rows');
      else                       record('crit', 'anon:' + tbl, `anonymous sees ${n} rows`);
    } catch (e) {
      record('warn', 'anon:' + tbl, 'check failed: ' + e.message);
    }
  }
}

// ============================================================
async function checkUpdatePolicies() {
  console.log(fmt('bold', '\n=== 3. UPDATE policies on profiles-like tables ==='));
  // Find every public table that has a column literally called `role` and an
  // UPDATE policy whose `with_check` is null/empty (= privilege escalation vector).
  const r = await pg.query(`
    select c.table_name,
           p.policyname,
           p.qual,
           p.with_check
      from information_schema.columns c
      join pg_policies p
        on p.schemaname = c.table_schema and p.tablename = c.table_name
     where c.table_schema = 'public'
       and c.column_name in ('role', 'email')
       and p.cmd = 'UPDATE'
  `);
  let found = false;
  for (const row of r.rows) {
    const wc = row.with_check;
    if (!wc || (!wc.includes('role') && !wc.includes('is_staff'))) {
      record('crit', `policy:${row.table_name}.${row.policyname}`,
        `UPDATE policy lacks WITH CHECK on role/email — privilege escalation risk`);
      found = true;
    }
  }
  if (!found) record('ok', 'update-policies', 'no privilege escalation surface found on UPDATE policies');
}

// ============================================================
async function checkPrivilegeEscalationLive() {
  if (!probeUid) {
    record('warn', 'priv-escalation', 'skipped — no --probe-uid provided');
    return;
  }
  console.log(fmt('bold', '\n=== 4. Live privilege escalation attempt ==='));
  // Each probe gets its own savepoint, so a deliberate failure in one doesn't
  // poison the next probe with "transaction is aborted".
  const probes = [
    {
      name: 'priv-set-admin',
      sql: `update public.profiles set role='admin' where id = $1 returning role`,
      msg: r => `PRIVILEGE ESCALATION: role became '${r.rows[0].role}'`,
    },
    {
      name: 'priv-set-email',
      sql: `update public.profiles set email='attacker@evil.test' where id = $1 returning email`,
      msg: () => `email mutation allowed`,
    },
  ];
  await pg.query('begin');
  try {
    await pg.query('set local role authenticated');
    await pg.query(`set local request.jwt.claims to '{"sub":"${probeUid}","role":"authenticated"}'`);
    for (const p of probes) {
      await pg.query('savepoint sp');
      const r = await pg.query(p.sql, [probeUid]).catch(e => ({ error: e.message }));
      if (r.error) {
        record('ok', p.name, 'blocked: ' + r.error.slice(0, 80));
        await pg.query('rollback to savepoint sp');
      } else if (r.rows.length === 0) {
        record('ok', p.name, 'blocked silently (0 rows)');
        await pg.query('release savepoint sp');
      } else {
        record('crit', p.name, p.msg(r));
        await pg.query('rollback to savepoint sp');
      }
    }
  } finally {
    await pg.query('rollback');
  }
}

// ============================================================
async function checkCustomerDataLeak() {
  if (!probeUid || !targetUid) {
    record('warn', 'data-leak', 'skipped — provide both --probe-uid and --target-uid');
    return;
  }
  console.log(fmt('bold', '\n=== 5. Customer-to-customer data isolation ==='));
  await pg.query('begin');
  try {
    await pg.query('set local role authenticated');
    await pg.query(`set local request.jwt.claims to '{"sub":"${probeUid}","role":"authenticated"}'`);
    const probes = [
      ['profiles', 'id'],
      ['deals', 'customer_id'],
      ['tax_engagements', 'customer_id'],
      ['customer_events', 'customer_id'],
      ['inquiries', 'user_id'],
      ['documents', 'user_id'],
      ['invoices', 'user_id'],
    ];
    let leaks = 0;
    for (const [tbl, col] of probes) {
      await pg.query('savepoint sp');
      const r = await pg.query(
        `select count(*)::int n from public.${tbl} where ${col} = $1`,
        [targetUid]
      ).catch(e => ({ error: e.message }));
      if (r.error) {
        record('warn', 'leak:' + tbl, 'query failed: ' + r.error.slice(0, 60));
        await pg.query('rollback to savepoint sp');
      } else if (r.rows[0].n === 0) {
        record('ok',   'leak:' + tbl, '0 rows visible (good)');
        await pg.query('release savepoint sp');
      } else {
        record('crit', 'leak:' + tbl, `${r.rows[0].n} rows of target leaked`);
        leaks++;
        await pg.query('release savepoint sp');
      }
    }
    if (leaks === 0) record('ok', 'data-isolation', 'no cross-customer leaks detected');
  } finally {
    await pg.query('rollback');
  }
}

// ============================================================
async function checkSecurityHeaders() {
  if (!site) {
    record('warn', 'headers', 'skipped — no --site provided');
    return;
  }
  console.log(fmt('bold', '\n=== 6. HTTP security headers on ' + site + ' ==='));
  const r = await rest('HEAD', site, {});
  const required = {
    'strict-transport-security': 'HSTS',
    'x-content-type-options':    'X-Content-Type-Options',
    'x-frame-options':           'X-Frame-Options',
    'referrer-policy':           'Referrer-Policy',
    'permissions-policy':        'Permissions-Policy',
  };
  for (const [h, label] of Object.entries(required)) {
    const v = r.headers[h];
    if (v) record('ok',   'header:' + label, String(v).slice(0, 80));
    else   record('warn', 'header:' + label, 'missing');
  }
}

// ============================================================
async function main() {
  console.log(fmt('bold', `🔐 Supabase Security Audit · ${new Date().toISOString()}\n`));
  await pg.connect();
  await pg.query('reset role').catch(() => {});
  try {
    await checkRlsCoverage();
    await checkAnonExposure();
    await checkUpdatePolicies();
    await checkPrivilegeEscalationLive();
    await checkCustomerDataLeak();
    await checkSecurityHeaders();
  } finally {
    await pg.end();
  }

  // Summary
  const sum = { ok: 0, warn: 0, crit: 0 };
  for (const f of findings) sum[f.level]++;
  console.log(fmt('bold', '\n=== Summary ==='));
  console.log(`  ${fmt('ok',   '✅ pass')} : ${sum.ok}`);
  console.log(`  ${fmt('warn', '🟡 warn')} : ${sum.warn}`);
  console.log(`  ${fmt('crit', '🚨 crit')} : ${sum.crit}`);
  process.exit(sum.crit > 0 ? 1 : 0);
}

main().catch(e => { console.error('FATAL:', e); process.exit(2); });
