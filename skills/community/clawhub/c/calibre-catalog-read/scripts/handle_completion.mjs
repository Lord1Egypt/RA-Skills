#!/usr/bin/env node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const SCRIPT_DIR = path.dirname(new URL(import.meta.url).pathname);
const DEFAULT_STATE_PATH = path.resolve(SCRIPT_DIR, '..', 'state', 'runs.json');
const WITH_LIBRARY_ENV_KEYS = ['CALIBRE_WITH_LIBRARY', 'CALIBRE_LIBRARY_URL', 'CALIBRE_CONTENT_SERVER_URL'];
const LIBRARY_ID_ENV_KEYS = ['CALIBRE_LIBRARY_ID'];
const SERVER_HOSTS_ENV_KEYS = ['CALIBRE_SERVER_HOSTS'];
const FORBIDDEN_AUTH_MODE_ARGS = ['auth-mode', 'auth_mode', 'auth-scheme', 'auth_scheme'];
const PIPELINE_PY = path.resolve(SCRIPT_DIR, 'run_analysis_pipeline.py');

function parseDotEnvValue(raw) {
  const s = String(raw || '').trim();
  if (!s) return '';
  if ((s.startsWith('"') && s.endsWith('"')) || (s.startsWith("'") && s.endsWith("'"))) {
    return s.slice(1, -1);
  }
  return s;
}

function loadDotEnvFile(envPath) {
  if (!fs.existsSync(envPath)) return;
  const txt = fs.readFileSync(envPath, 'utf-8');
  for (const line of txt.split(/\r?\n/)) {
    const t = line.trim();
    if (!t || t.startsWith('#')) continue;
    const m = t.match(/^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$/);
    if (!m) continue;
    const key = m[1];
    if (process.env[key] != null && String(process.env[key]).trim() !== '') continue;
    process.env[key] = parseDotEnvValue(m[2]);
  }
}

function hydrateEnvFromDotEnv() {
  const candidates = [
    path.resolve(process.cwd(), '.env'),
    path.join(os.homedir(), '.openclaw', '.env'),
  ];
  const seen = new Set();
  for (const p of candidates) {
    const n = path.normalize(p);
    if (seen.has(n)) continue;
    seen.add(n);
    loadDotEnvFile(n);
  }
}

hydrateEnvFromDotEnv();

function nowIso() { return new Date().toISOString(); }

function parseArgs(argv) {
  const out = {};
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const k = a.slice(2);
      const v = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
      out[k] = v;
    }
  }
  return out;
}

function assertDigestAuthModeFixed(args) {
  const provided = FORBIDDEN_AUTH_MODE_ARGS.find((k) => Object.prototype.hasOwnProperty.call(args, k));
  if (!provided) return;
  throw new Error(
    `unsupported --${provided}: auth scheme is fixed to Digest for non-SSL Content server usage. Remove auth mode arguments.`,
  );
}

function splitList(v) {
  if (v == null) return [];
  if (Array.isArray(v)) return v.map(x => String(x || '').trim()).filter(Boolean);
  return String(v)
    .split(/[,\n;]/)
    .map(x => x.trim())
    .filter(Boolean);
}

function pickFirstNonEmpty(values) {
  for (const v of values) {
    const t = String(v || '').trim();
    if (t) return t;
  }
  return '';
}

function isHttpUrl(v) {
  return /^https?:\/\//i.test(String(v || '').trim());
}

function parseHttpUrlParts(v) {
  const m = String(v || '').trim().match(/^(https?:\/\/)(\[[^\]]+\]|[^\/:#]+)(:\d+)?(.*)$/i);
  if (!m) return null;
  return { proto: m[1], host: m[2], port: m[3] || '', tail: m[4] || '' };
}

function normalizeHostToken(h) {
  const t = String(h || '').trim();
  if (!t) return '';
  if (t.startsWith('[') && t.endsWith(']')) return t.slice(1, -1);
  return t;
}

function formatHostForUrl(h) {
  const t = normalizeHostToken(h);
  if (!t) return '';
  if (t.includes(':')) return `[${t}]`;
  return t;
}

function replaceHttpHost(v, host) {
  const p = parseHttpUrlParts(v);
  if (!p) return String(v || '').trim();
  const f = formatHostForUrl(host);
  if (!f) return String(v || '').trim();
  return `${p.proto}${f}${p.port}${p.tail}`;
}

function discoverWslHostCandidates() {
  const out = [];
  try {
    const rc = '/etc/resolv.conf';
    if (fs.existsSync(rc)) {
      const txt = fs.readFileSync(rc, 'utf-8');
      for (const line of txt.split(/\r?\n/)) {
        const m = line.match(/^\s*nameserver\s+([0-9a-fA-F:.]+)\s*$/);
        if (m && m[1]) out.push(m[1]);
      }
    }
  } catch {}
  return out;
}

function expandHome(v) {
  const s = String(v || '').trim();
  if (!s.startsWith('~')) return s;
  if (s === '~') return os.homedir();
  if (s.startsWith('~/')) return path.join(os.homedir(), s.slice(2));
  return s;
}

function normalizeWithLibrary(value, libraryId) {
  const raw = String(value || '').trim();
  if (!raw) return '';
  if (!isHttpUrl(raw)) return expandHome(raw);
  if (/#.+/.test(raw)) return raw;
  const lid = String(libraryId || '').trim();
  if (!lid) return raw;
  return `${raw}#${lid}`;
}

function validateWithLibrary(value) {
  const v = String(value || '').trim();
  if (!v) return 'empty';
  if (isHttpUrl(v)) {
    if (!/#.+/.test(v)) return 'content server URL must include #LIBRARY_ID';
    return null;
  }
  if (!fs.existsSync(v)) return `local library path not found: ${v}`;
  const st = fs.statSync(v);
  if (st.isFile() && path.basename(v).toLowerCase() === 'metadata.db') return null;
  if (st.isDirectory() && fs.existsSync(path.join(v, 'metadata.db'))) return null;
  return `local path exists but metadata.db is missing: ${v}`;
}

function buildWithLibraryCandidates(args) {
  const libraryId = pickFirstNonEmpty([
    args['library-id'],
    ...LIBRARY_ID_ENV_KEYS.map(k => process.env[k]),
  ]);

  const baseCandidates = [];
  if (args['with-library']) baseCandidates.push({ source: '--with-library', value: String(args['with-library']) });
  for (const k of WITH_LIBRARY_ENV_KEYS) {
    if (process.env[k]) baseCandidates.push({ source: `env:${k}`, value: String(process.env[k]) });
  }

  const extraHosts = [
    ...splitList(args['server-hosts']),
    ...SERVER_HOSTS_ENV_KEYS.flatMap(k => splitList(process.env[k])),
    ...discoverWslHostCandidates(),
    'host.docker.internal',
  ]
    .map(normalizeHostToken)
    .filter(Boolean);

  if (!baseCandidates.length) {
    throw new Error('missing --with-library (or set CALIBRE_WITH_LIBRARY / CALIBRE_LIBRARY_URL / CALIBRE_CONTENT_SERVER_URL)');
  }

  const expanded = [];
  for (const c of baseCandidates) {
    const normalized = normalizeWithLibrary(c.value, libraryId);
    expanded.push({ source: c.source, value: normalized });
    if (!isHttpUrl(normalized)) continue;
    const p = parseHttpUrlParts(normalized);
    if (!p) continue;
    const curHost = normalizeHostToken(p.host);
    for (const h of extraHosts) {
      if (!h || h === curHost) continue;
      expanded.push({ source: `${c.source}:host=${h}`, value: replaceHttpHost(normalized, h) });
    }
  }

  const dedup = [];
  const seen = new Set();
  for (const c of expanded) {
    const key = String(c.value || '').trim();
    if (!key || seen.has(key)) continue;
    seen.add(key);
    dedup.push(c);
  }
  return dedup;
}

function isConnectionLikeError(msg) {
  const s = String(msg || '').toLowerCase();
  return (
    s.includes('connection refused') ||
    s.includes('connectionrefusederror') ||
    s.includes('timed out') ||
    s.includes('no route to host') ||
    s.includes('name or service not known') ||
    s.includes('temporary failure in name resolution') ||
    s.includes('urlopen error [errno 111]') ||
    s.includes('urlopen error [errno 113]') ||
    s.includes('[errno 111]') ||
    s.includes('[errno 113]') ||
    s.includes('operation not permitted')
  );
}

function isNotFoundLikeError(msg) {
  const s = String(msg || '').trim().toLowerCase();
  return (
    s.includes('not found') ||
    s.includes('404') ||
    s.includes('http error 404') ||
    s.includes('no library with id') ||
    s.includes('library id')
  );
}

function shortErr(msg) {
  const s = String(msg || '').trim().replace(/\s+/g, ' ');
  return s.length > 240 ? `${s.slice(0, 237)}...` : s;
}

function resolveProbeAuth(args) {
  const username = String(args.username || process.env.CALIBRE_USERNAME || '').trim();
  let password = String(args.password || '').trim();
  const penv = String(args['password-env'] || 'CALIBRE_PASSWORD');
  if (!password && penv) password = String(process.env[penv] || '').trim();
  return { username, password };
}

function probeRemoteLibrary(withLibrary, auth) {
  const cmd = ['calibredb', 'list', '--for-machine', '--fields', 'id', '--limit', '1', '--with-library', withLibrary];
  if (auth.username) cmd.push('--username', String(auth.username));
  if (auth.password) cmd.push('--password', String(auth.password));
  const cp = spawnSync(cmd[0], cmd.slice(1), { encoding: 'utf-8' });
  return { rc: cp.status || 0, out: cp.stdout || '', err: cp.stderr || '' };
}

function resolveWithLibrary(args, auth) {
  const candidates = buildWithLibraryCandidates(args);
  const errors = [];
  for (const c of candidates) {
    const value = String(c.value || '').trim();
    const err = validateWithLibrary(value);
    if (err) {
      errors.push(`${c.source}: ${err}`);
      continue;
    }
    if (!isHttpUrl(value)) return value;
    const pr = probeRemoteLibrary(value, auth);
    if (pr.rc === 0) return value;
    const raw = String(pr.err || pr.out || '');
    if (isConnectionLikeError(raw)) {
      errors.push(`${c.source}: connection probe failed (${shortErr(raw)})`);
      continue;
    }
    if (isNotFoundLikeError(raw)) {
      errors.push(`${c.source}: target not found (${shortErr(raw)})`);
      continue;
    }
    const e = shortErr(raw);
    throw new Error(`with-library probe failed at ${c.source}: ${e}`);
  }

  throw new Error(`unable to resolve usable --with-library\n${errors.map(e => `- ${e}`).join('\n')}\nHint: set CALIBRE_SERVER_HOSTS (comma-separated) for host failover.`);
}

function loadState(p) {
  if (!fs.existsSync(p)) return { runs: {} };
  const txt = fs.readFileSync(p, 'utf-8').trim();
  if (!txt) return { runs: {} };
  try {
    const d = JSON.parse(txt);
    if (!d.runs || typeof d.runs !== 'object') d.runs = {};
    return d;
  } catch {
    return { runs: {} };
  }
}

function saveState(p, d) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(d, null, 2), 'utf-8');
}

function markFailed(p, runId, error) {
  const d = loadState(p);
  const e = d.runs?.[runId];
  if (!e) return;
  e.status = 'failed';
  e.error = error;
  e.updated_at = nowIso();
  saveState(p, d);
}

function removeRun(p, runId) {
  const d = loadState(p);
  const existed = !!d.runs?.[runId];
  if (d.runs) delete d.runs[runId];
  saveState(p, d);
  return existed;
}

function runApply(args, bookId) {
  const cmd = ['uv', 'run', 'python', PIPELINE_PY, '--with-library', args['with-library'], '--book-id', String(bookId), '--lang', String(args.lang || 'ja'), '--analysis-json', String(args['analysis-json'])];
  if (args.username) cmd.push('--username', String(args.username));
  if (args['password-env']) cmd.push('--password-env', String(args['password-env']));

  const safeEnv = {
    PATH: process.env.PATH || '',
    HOME: process.env.HOME || '',
    LANG: process.env.LANG || 'C.UTF-8',
    LC_ALL: process.env.LC_ALL || '',
    LC_CTYPE: process.env.LC_CTYPE || '',
    CALIBRE_USERNAME: process.env.CALIBRE_USERNAME || '',
  };
  const penv = String(args['password-env'] || '');
  if (penv && process.env[penv]) safeEnv[penv] = process.env[penv];

  return spawnSync(cmd[0], cmd.slice(1), { encoding: 'utf-8', env: safeEnv });
}

function main() {
  const a = parseArgs(process.argv);
  assertDigestAuthModeFixed(a);
  const statePath = String(a.state || DEFAULT_STATE_PATH);
  const runId = String(a['run-id'] || '');
  const analysisJson = String(a['analysis-json'] || '');
  if (!runId || !analysisJson) throw new Error('required: --run-id --analysis-json');
  const probeAuth = resolveProbeAuth(a);
  a['with-library'] = resolveWithLibrary(a, probeAuth);

  const d = loadState(statePath);
  const run = d.runs?.[runId];
  if (!run) {
    console.log(JSON.stringify({ ok: true, status: 'stale_or_duplicate', runId }));
    return;
  }

  const bookId = Number(run.book_id);
  if (!fs.existsSync(analysisJson)) {
    const err = `analysis_json_not_found: ${analysisJson}`;
    markFailed(statePath, runId, err);
    console.log(JSON.stringify({ ok: false, status: 'failed', runId, error: err }));
    process.exit(1);
  }

  const cp = runApply(a, bookId);
  if (cp.status !== 0) {
    const err = `apply_failed (exit=${cp.status})`;
    markFailed(statePath, runId, err);
    console.log(JSON.stringify({ ok: false, status: 'failed', runId, book_id: bookId, error: err, stdout: cp.stdout, stderr: cp.stderr }));
    process.exit(cp.status || 1);
  }

  removeRun(statePath, runId);
  console.log(JSON.stringify({ ok: true, status: 'applied_and_removed', runId, book_id: bookId, stdout: cp.stdout }));
}

try { main(); } catch (e) { console.error(String(e?.stack || e)); process.exit(1); }
