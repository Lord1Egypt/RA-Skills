#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import { existsSync, readFileSync, statSync } from 'node:fs';
import { basename, join } from 'node:path';
import os from 'node:os';

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const k = a.slice(2);
      const v = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
      out[k] = v;
    } else {
      out._.push(a);
    }
  }
  return out;
}

const WITH_LIBRARY_ENV_KEYS = ['CALIBRE_WITH_LIBRARY', 'CALIBRE_LIBRARY_URL', 'CALIBRE_CONTENT_SERVER_URL'];
const LIBRARY_ID_ENV_KEYS = ['CALIBRE_LIBRARY_ID'];
const SERVER_HOSTS_ENV_KEYS = ['CALIBRE_SERVER_HOSTS'];
const FORBIDDEN_AUTH_MODE_ARGS = ['auth-mode', 'auth_mode', 'auth-scheme', 'auth_scheme'];

function assertDigestAuthModeFixed(args) {
  const provided = FORBIDDEN_AUTH_MODE_ARGS.find((k) => Object.prototype.hasOwnProperty.call(args, k));
  if (!provided) return;
  throw new Error(
    `unsupported --${provided}: auth scheme is fixed to Digest for non-SSL Content server usage. Remove auth mode arguments.`,
  );
}

function parseDotEnvValue(raw) {
  const s = String(raw || '').trim();
  if (!s) return '';
  if ((s.startsWith('"') && s.endsWith('"')) || (s.startsWith("'") && s.endsWith("'"))) {
    return s.slice(1, -1);
  }
  return s;
}

function loadDotEnvFile(envPath) {
  if (!existsSync(envPath)) return;
  const txt = readFileSync(envPath, 'utf8');
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
    join(process.cwd(), '.env'),
    join(os.homedir(), '.openclaw', '.env'),
  ];
  const seen = new Set();
  for (const p of candidates) {
    if (seen.has(p)) continue;
    seen.add(p);
    loadDotEnvFile(p);
  }
}

hydrateEnvFromDotEnv();


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
    if (existsSync(rc)) {
      const txt = readFileSync(rc, 'utf8');
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
  if (s.startsWith('~/')) return join(os.homedir(), s.slice(2));
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
  if (!existsSync(v)) return `local library path not found: ${v}`;
  const st = statSync(v);
  if (st.isFile() && basename(v).toLowerCase() === 'metadata.db') return null;
  if (st.isDirectory() && existsSync(join(v, 'metadata.db'))) return null;
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
    throw new Error('missing --with-library (or set CALIBRE_WITH_LIBRARY / CALIBRE_LIBRARY_URL / CALIBRE_CONTENT_SERVER_URL). Check TOOLS.md for the value.');
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

function probeRemoteLibrary(withLibrary, auth) {
  const cmd = ['calibredb', 'list', '--for-machine', '--fields', 'id', '--limit', '1', '--with-library', withLibrary];
  if (auth.username) cmd.push('--username', auth.username);
  if (auth.password) cmd.push('--password', auth.password);
  const cp = spawnSync(cmd[0], cmd.slice(1), { encoding: 'utf8' });
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

function resolveAuth(args) {
  const envUser = (process.env.CALIBRE_USERNAME || '').trim();
  const username = args.username ? String(args.username) : (envUser || '');

  let password = args.password ? String(args.password) : '';
  const passwordEnv = args['password-env'] ? String(args['password-env']) : 'CALIBRE_PASSWORD';

  if (!password && passwordEnv) password = process.env[passwordEnv] || '';

  return { username, password };
}

function commonArgs(args) {
  const r = ['--with-library', String(args['with-library'] || '')];
  const auth = args.__resolved_auth || resolveAuth(args);
  if (auth.username) r.push('--username', auth.username);
  if (auth.password) r.push('--password', auth.password);
  return r;
}

function run(cmd) {
  const cp = spawnSync(cmd[0], cmd.slice(1), { encoding: 'utf8' });
  if (cp.status !== 0) {
    throw new Error(`calibredb failed (${cp.status})\nCMD: ${cmd.map(x => JSON.stringify(x)).join(' ')}\nERR:\n${(cp.stderr || '').trim()}`);
  }
  return cp.stdout || '';
}

function toJson(text) {
  return JSON.parse(text);
}

function requireArg(args, key, hint = '') {
  if (!args[key]) {
    throw new Error(`missing --${key}${hint ? ` (${hint})` : ''}`);
  }
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const cmd = args._[0];

  if (!cmd || !['list', 'search', 'id'].includes(cmd)) {
    const bad = String(cmd || '').trim();
    const guidance = bad
      ? `unsupported command: ${bad}. calibredb_read.mjs is read-only (list/search/id). For metadata edits use: node skills/calibre-metadata-apply/scripts/calibredb_apply.mjs`
      : 'usage: calibredb_read.mjs <list|search|id> [--with-library <url#lib>] [--username u] [--password p|--password-env ENV] [--fields f] [--limit n] [--query q] [--book-id id]';
    console.log(JSON.stringify({
      ok: false,
      error: guidance
    }, null, 2));
    process.exit(1);
  }

  try {
    assertDigestAuthModeFixed(args);
    const auth = resolveAuth(args);
    args['with-library'] = resolveWithLibrary(args, auth);
    args.__resolved_auth = auth;
    const fieldsDefault = 'id,title,authors,series,series_index,tags,formats,publisher,pubdate,languages,last_modified';
    const fields = String(args.fields || (cmd === 'id'
      ? `${fieldsDefault},comments`
      : fieldsDefault));
    const limit = Number(args.limit || 100);

    if (cmd === 'list') {
      const out = run([
        'calibredb', 'list', '--for-machine', '--fields', fields, '--limit', String(limit),
        ...commonArgs(args),
      ]);
      console.log(JSON.stringify({ ok: true, mode: 'list', fields, items: toJson(out) }, null, 2));
      return;
    }

    if (cmd === 'search') {
      requireArg(args, 'query');
      const query = String(args.query);
      const out = run([
        'calibredb', 'list', '--for-machine', '--fields', fields,
        '--search', query, '--limit', String(limit),
        ...commonArgs(args),
      ]);
      console.log(JSON.stringify({ ok: true, mode: 'search', query, fields, items: toJson(out) }, null, 2));
      return;
    }

    // id
    requireArg(args, 'book-id');
    const bookId = String(args['book-id']);
    const out = run([
      'calibredb', 'list', '--for-machine', '--fields', fields,
      '--search', `id:${bookId}`, '--limit', '5',
      ...commonArgs(args),
    ]);
    const rows = toJson(out);
    const item = rows.find(r => String(r?.id) === bookId) || null;
    console.log(JSON.stringify({ ok: true, mode: 'id', book_id: bookId, item }, null, 2));
  } catch (e) {
    console.log(JSON.stringify({ ok: false, error: String(e?.message || e) }, null, 2));
    process.exit(1);
  }
}

main();
