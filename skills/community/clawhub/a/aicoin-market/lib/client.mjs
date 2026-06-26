#!/usr/bin/env node
// AiCoin Open Data v3 API client — HMAC-SHA1 signed, header auth.
// One unified envelope {ok, data, error, meta}; see catalog for all endpoints.
import { createHmac, randomBytes } from 'node:crypto';
import { readFileSync, existsSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ── .env auto-load (OpenClaw exec may not inject env into child processes) ──
const ENV_FILES = [
  resolve(process.cwd(), '.env'),
  resolve(process.env.HOME || '', '.openclaw', 'workspace', '.env'),
  resolve(process.env.HOME || '', '.openclaw', '.env'),
];
for (const file of ENV_FILES) {
  if (!existsSync(file)) continue;
  try {
    for (const line of readFileSync(file, 'utf-8').split('\n')) {
      const t = line.trim();
      if (!t || t.startsWith('#')) continue;
      const eq = t.indexOf('=');
      if (eq < 1) continue;
      const k = t.slice(0, eq).trim();
      let v = t.slice(eq + 1).trim();
      if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) v = v.slice(1, -1);
      if (!process.env[k]) process.env[k] = v;
    }
  } catch { /* ignore unreadable .env */ }
}

const defaults = JSON.parse(readFileSync(resolve(__dirname, 'defaults.json'), 'utf-8'));
export const BASE = process.env.AICOIN_BASE_URL || 'https://open.aicoin.com';
export const KEY = process.env.AICOIN_ACCESS_KEY_ID || defaults.accessKeyId;
const SECRET = process.env.AICOIN_ACCESS_SECRET || defaults.accessSecret;
export const USING_OWN_KEY = !!(process.env.AICOIN_ACCESS_KEY_ID && process.env.AICOIN_ACCESS_SECRET);

// HMAC-SHA1(signStr, secret) → hex → base64. The 4 values ride in X-Aic-* headers.
function authHeaders(keyId = KEY, secret = SECRET) {
  const nonce = randomBytes(8).toString('hex');
  const ts = Math.floor(Date.now() / 1000).toString();
  const signStr = `AccessKeyId=${keyId}&SignatureNonce=${nonce}&Timestamp=${ts}`;
  const hex = createHmac('sha1', secret).update(signStr).digest('hex');
  return {
    'X-Aic-AccessKey-Id': keyId,
    'X-Aic-Signature-Nonce': nonce,
    'X-Aic-Timestamp': ts,
    'X-Aic-Signature': Buffer.from(hex).toString('base64'),
  };
}

// Normalize a user-supplied endpoint to a full /api/v3/... path.
//   "market/ticker" / "/market/ticker" / "/api/v3/market/ticker"  → "/api/v3/market/ticker"
export function normalizePath(ep) {
  let p = String(ep || '').trim().replace(/^https?:\/\/[^/]+/, '');
  if (p.startsWith('/api/v3/') || p === '/api/v3') return p;
  p = p.replace(/^\/?(api\/v3\/?)?/, '');
  return '/api/v3/' + p;
}

// endpoints.json — a bundled catalog snapshot. Drives GET/POST selection and
// offline `catalog`. Live catalog is still the source of truth (see fetchCatalog).
let _snapshot = null;
export function snapshotEndpoints() {
  if (_snapshot) return _snapshot;
  try {
    const j = JSON.parse(readFileSync(resolve(__dirname, 'endpoints.json'), 'utf-8'));
    _snapshot = j.endpoints || [];
  } catch { _snapshot = []; }
  return _snapshot;
}

// Pull the live catalog. Falls back to the bundled snapshot when offline.
export async function fetchCatalog() {
  try {
    const { httpStatus, body } = await request('GET', '/api/v3/_catalog');
    if (httpStatus === 200 && body?.data?.endpoints) return { endpoints: body.data.endpoints, live: true };
  } catch { /* fall through to snapshot */ }
  return { endpoints: snapshotEndpoints(), live: false };
}

// Core request. Returns { httpStatus, body }; body is the parsed envelope.
export async function request(method, path, params = {}) {
  const full = normalizePath(path);
  const m = (method || 'GET').toUpperCase();
  const headers = authHeaders();
  let url = `${BASE}${full}`;
  const init = { method: m, headers, signal: AbortSignal.timeout(30000) };
  if (m === 'GET' || m === 'DELETE') {
    const qs = new URLSearchParams();
    for (const [k, v] of Object.entries(params || {})) {
      if (v === undefined || v === null || v === '') continue;
      qs.set(k, Array.isArray(v) ? v.join(',') : String(v));
    }
    const s = qs.toString();
    if (s) url += `?${s}`;
  } else {
    headers['Content-Type'] = 'application/json';
    init.body = JSON.stringify(params || {});
  }
  const res = await fetch(url, init);
  const text = await res.text();
  let body;
  try { body = JSON.parse(text); } catch { body = { ok: false, error: { code: 'bad_response', message: text.slice(0, 300) } }; }
  // v3 business endpoints answer with {ok,...}. Auth / quota errors from the
  // gateway are still legacy-shaped ({success:false,errorCode,error}); fold them
  // into the same envelope so callers only ever branch on `ok`.
  if (body && typeof body === 'object' && typeof body.ok !== 'boolean' && (res.status >= 400 || body.success === false)) {
    body = {
      ok: false,
      data: null,
      error: {
        code: body.errorCode != null ? String(body.errorCode) : String(res.status),
        message: body.error || body.message || body.msg || `HTTP ${res.status}`,
      },
      meta: {},
    };
  }
  return { httpStatus: res.status, body };
}

// Resolve which HTTP method an endpoint uses, from snapshot then live catalog.
export async function resolveMethod(path) {
  const full = normalizePath(path);
  let hit = snapshotEndpoints().find(e => e.path === full);
  if (!hit) {
    const { endpoints } = await fetchCatalog();
    hit = endpoints.find(e => e.path === full);
  }
  return hit ? { method: hit.method, spec: hit } : null;
}

// Persist a new key pair to the workspace .env (validates before writing).
export async function saveKey(keyId, secret) {
  const headers = authHeaders(keyId, secret);
  const res = await fetch(`${BASE}/api/v3/coins/tickers?coin_key=bitcoin`, { headers, signal: AbortSignal.timeout(15000) });
  if (res.status === 401 || res.status === 403) return { ok: false, error: `key 验证失败 (HTTP ${res.status})` };
  if (!res.ok) return { ok: false, error: `验证请求失败 (HTTP ${res.status})` };
  const target = ENV_FILES.find(existsSync) || ENV_FILES[0];
  let lines = existsSync(target) ? readFileSync(target, 'utf-8').split('\n') : [];
  const set = (k, v) => {
    const i = lines.findIndex(l => l.trim().startsWith(k + '='));
    if (i >= 0) lines[i] = `${k}=${v}`; else lines.push(`${k}=${v}`);
  };
  set('AICOIN_ACCESS_KEY_ID', keyId);
  set('AICOIN_ACCESS_SECRET', secret);
  writeFileSync(target, lines.join('\n'));
  return { ok: true, file: target };
}
