#!/usr/bin/env node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const ALLOWED = new Set(['title','title_sort','authors','author_sort','series','series_index','tags','publisher','pubdate','languages','comments']);
const OC_START = '<!-- OC_ANALYSIS_START -->';
const OC_END = '<!-- OC_ANALYSIS_END -->';
const WITH_LIBRARY_ENV_KEYS = ['CALIBRE_WITH_LIBRARY', 'CALIBRE_LIBRARY_URL', 'CALIBRE_CONTENT_SERVER_URL'];
const LIBRARY_ID_ENV_KEYS = ['CALIBRE_LIBRARY_ID'];
const SERVER_HOSTS_ENV_KEYS = ['CALIBRE_SERVER_HOSTS'];
const FORBIDDEN_AUTH_MODE_ARGS = ['auth-mode', 'auth_mode', 'auth-scheme', 'auth_scheme'];

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

const I18N = {
  ja: { title: 'OpenClaw解析', summary: '要約', key_points: '重要ポイント', reread: '再読ガイド', generated_at: '生成日時', file_hash: 'ファイルハッシュ', analysis_tags: '解析タグ', section: '章/節', page: 'ページ', chunk: 'チャンク' },
  en: { title: 'OpenClaw Analysis', summary: 'Summary', key_points: 'Key points', reread: 'Reread guide', generated_at: 'generated_at', file_hash: 'file_hash', analysis_tags: 'analysis_tags', section: 'section', page: 'page', chunk: 'chunk' },
};

function parseArgs(argv) {
  const out = {
    apply: false,
    lang: 'ja',
    'password-env': 'CALIBRE_PASSWORD',
    _: [],
  };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith('--')) { out._.push(a); continue; }
    const k = a.slice(2);
    if (['apply'].includes(k)) out[k] = true;
    else out[k] = argv[++i];
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

function buildSafeEnv() {
  return {
    PATH: process.env.PATH || '',
    HOME: process.env.HOME || '',
    LANG: process.env.LANG || 'C.UTF-8',
    LC_ALL: process.env.LC_ALL || '',
    LC_CTYPE: process.env.LC_CTYPE || '',
    SYSTEMROOT: process.env.SYSTEMROOT || '',
    WINDIR: process.env.WINDIR || '',
  };
}

function run(cmd) {
  const cp = spawnSync(cmd[0], cmd.slice(1), { encoding: 'utf-8', env: buildSafeEnv() });
  return { rc: cp.status || 0, out: cp.stdout || '', err: cp.stderr || '' };
}
function runOk(cmd) {
  const { rc, out, err } = run(cmd);
  if (rc !== 0) throw new Error(`calibredb failed (${rc})\nCMD: ${redactedCmd(cmd)}\nERR:\n${err.trim()}`);
  return out;
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
  if (auth.username) cmd.push('--username', String(auth.username));
  if (auth.password) cmd.push('--password', String(auth.password));
  return run(cmd);
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
  const username = args.username ? String(args.username) : (envUser || null);

  let password = args.password ? String(args.password) : '';
  const passwordEnv = args['password-env'] ? String(args['password-env']) : 'CALIBRE_PASSWORD';

  if (!password && passwordEnv) password = process.env[passwordEnv] || '';

  return { username, password, usedPasswordEnv: passwordEnv };
}

function commonArgs(args, auth) {
  const r = ['--with-library', String(args['with-library'])];
  if (auth.username) r.push('--username', String(auth.username));
  if (auth.password) r.push('--password', String(auth.password));
  return r;
}

function redactedCmd(cmd) {
  const out = [];
  let maskNext = false;
  for (const t of cmd) {
    if (maskNext) { out.push('********'); maskNext = false; continue; }
    out.push(t);
    if (t === '--password') maskNext = true;
  }
  return out.map(x => (/[\s'"\\]/.test(x) ? JSON.stringify(x) : x)).join(' ');
}

function toFieldValue(v) { return Array.isArray(v) ? v.map(String).join(',') : String(v); }

function splitMulti(v) {
  if (v == null) return [];
  const raw = Array.isArray(v) ? v.map(String) : String(v).split(/[,;\n]/);
  const out = [];
  const seen = new Set();
  for (const x of raw) {
    const t = String(x).trim();
    if (!t) continue;
    const k = t.toLowerCase();
    if (seen.has(k)) continue;
    seen.add(k); out.push(t);
  }
  return out;
}

function fetchBook(args, auth, bookId, fields) {
  const cmd = ['calibredb','list','--for-machine','--fields',fields,'--search',`id:${bookId}`,'--limit','5', ...commonArgs(args, auth)];
  const rows = JSON.parse(runOk(cmd));
  return rows.find(r => String(r?.id) === String(bookId)) || null;
}

function renderAnalysisHtml(bookId, analysis, defaultLang='ja') {
  const summary = String(analysis?.summary || '').trim();
  const highlights = splitMulti(analysis?.highlights || []);
  const tags = splitMulti(analysis?.tags || []);
  const reread = Array.isArray(analysis?.reread) ? analysis.reread : [];
  const generatedAt = String(analysis?.generated_at || '').trim() || new Date().toISOString();
  const sourceHash = String(analysis?.file_hash || '').trim();
  let lang = String(analysis?.lang || defaultLang).toLowerCase();
  if (!I18N[lang]) lang = I18N[defaultLang] ? defaultLang : 'en';
  const tr = I18N[lang];

  const lines = [OC_START, '<div class="openclaw-analysis">', `<h3>${tr.title}</h3>`];
  if (summary) lines.push(`<p><strong>${tr.summary}:</strong> ${summary}</p>`);
  if (highlights.length) {
    lines.push(`<h4>${tr.key_points}</h4><ul>`);
    for (const h of highlights) lines.push(`<li>${h}</li>`);
    lines.push('</ul>');
  }
  if (reread.length) {
    lines.push(`<h4>${tr.reread}</h4><ul>`);
    for (const item of reread) {
      if (!item || typeof item !== 'object') continue;
      const section = String(item.section || '').trim();
      const page = String(item.page || '').trim();
      const chunk = String(item.chunk_id || '').trim();
      const reason = String(item.reason || '').trim();
      const parts = [section ? `${tr.section}: ${section}` : '', page ? `${tr.page}: ${page}` : '', chunk ? `${tr.chunk}: ${chunk}` : '', reason].filter(Boolean);
      if (parts.length) lines.push(`<li>${parts.join(' | ')}</li>`);
    }
    lines.push('</ul>');
  }
  const meta = [`${tr.generated_at}: ${generatedAt}`];
  if (sourceHash) meta.push(`${tr.file_hash}: ${sourceHash}`);
  if (tags.length) meta.push(`${tr.analysis_tags}: ${tags.join(', ')}`);
  lines.push(`<p><em>${meta.join(' / ')}</em></p>`);
  lines.push('</div>', OC_END);
  return lines.join('\n');
}

function upsertOcBlock(existingHtml, blockHtml) {
  const existing = String(existingHtml || '');
  const re = new RegExp(OC_START.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '[\\s\\S]*?' + OC_END.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  if (re.test(existing)) return existing.replace(re, blockHtml);
  if (existing.trim()) return existing.replace(/\s+$/, '') + '\n\n' + blockHtml;
  return blockHtml;
}

function buildFields(args, auth, rec) {
  const r = { ...rec };
  const bid = String(r.id || '').trim();
  if (!bid) throw new Error('missing id');

  if (r.analysis && typeof r.analysis === 'object') {
    r.comments_html = renderAnalysisHtml(bid, r.analysis, args.lang || 'ja');
    if (!r.analysis_tags) r.analysis_tags = r.analysis.tags || [];
  }

  if (r.comments_html) {
    const current = fetchBook(args, auth, bid, 'id,comments') || {};
    r.comments = upsertOcBlock(String(current.comments || ''), String(r.comments_html));
  }

  if (r.tags !== undefined || r.analysis_tags !== undefined || r.tags_remove !== undefined) {
    const incoming = splitMulti(r.tags);
    const extra = splitMulti(r.analysis_tags);
    const removeSet = new Set(splitMulti(r.tags_remove).map(x => x.toLowerCase()));
    const mergeExisting = r.tags_merge !== false;
    let existingTags = [];
    if (mergeExisting) {
      const current = fetchBook(args, auth, bid, 'id,tags') || {};
      existingTags = splitMulti(current.tags || []);
    }
    let merged = splitMulti([...existingTags, ...incoming, ...extra]);
    if (removeSet.size) merged = merged.filter(t => !removeSet.has(t.toLowerCase()));
    r.tags = merged;
  }

  const fields = [];
  for (const [k, v] of Object.entries(r)) {
    if (k === 'id') continue;
    if (!ALLOWED.has(k)) continue;
    if (v == null) continue;
    fields.push([k, toFieldValue(v)]);
  }
  if (!fields.length) throw new Error('no updatable fields');
  return fields;
}

function buildCmd(args, auth, rec) {
  const bid = String(rec.id || '').trim();
  if (!bid) throw new Error('missing id');
  const fields = buildFields(args, auth, rec);
  const cmd = ['calibredb','set_metadata',bid];
  for (const [k, v] of fields) cmd.push('--field', `${k}:${v}`);
  cmd.push(...commonArgs(args, auth));
  return cmd;
}

async function readStdinLines() {
  const chunks = [];
  for await (const c of process.stdin) chunks.push(c);
  return Buffer.concat(chunks).toString('utf-8').split(/\r?\n/).map(s => s.trim()).filter(Boolean);
}

async function main() {
  const args = parseArgs(process.argv);
  assertDigestAuthModeFixed(args);
  if (!['ja','en'].includes(String(args.lang || 'ja'))) throw new Error('--lang must be ja|en');
  const auth = resolveAuth(args);
  args['with-library'] = resolveWithLibrary(args, auth);

  const lines = await readStdinLines();
  if (!lines.length) {
    console.log(JSON.stringify({ ok: true, summary: { total: 0, planned: 0, applied: 0, failed: 0 }, results: [] }, null, 2));
    return;
  }

  const results = [];
  let planned = 0, applied = 0, failed = 0;

  for (let i = 0; i < lines.length; i++) {
    const ln = lines[i];
    try {
      const rec = JSON.parse(ln);
      const cmd = buildCmd(args, auth, rec);
      planned++;
      if (!args.apply) {
        results.push({ line: i + 1, id: rec.id, action: 'planned', cmd: redactedCmd(cmd) });
        continue;
      }
      const { rc, out, err } = run(cmd);
      if (rc === 0) {
        applied++;
        results.push({ line: i + 1, id: rec.id, action: 'applied', stdout: out.trim() });
      } else {
        failed++;
        results.push({ line: i + 1, id: rec.id, action: 'failed', stderr: err.trim(), rc });
      }
    } catch (e) {
      failed++;
      results.push({ line: i + 1, action: 'error', error: String(e?.message || e) });
    }
  }

  const ok = failed === 0;
  console.log(JSON.stringify({ ok, mode: args.apply ? 'apply' : 'dry-run', summary: { total: lines.length, planned, applied, failed }, results }, null, 2));
  if (!ok) process.exit(1);
}

main().catch(e => { console.error(String(e?.stack || e)); process.exit(1); });
