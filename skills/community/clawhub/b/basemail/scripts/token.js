/**
 * BaseMail token store + refresh helper (shared by send.js / inbox.js / register.js)
 *
 * ~/.basemail/token.json holds { token, refresh_token, email, handle, wallet, expires_at }.
 * Tokens are JWTs valid for 24 h; when one is about to expire (or the API answers 401)
 * we exchange refresh_token at POST /api/auth/refresh — no private key needed.
 */

const fs = require('fs');
const path = require('path');

const API_BASE = 'https://api.basemail.ai';
const CONFIG_DIR = path.join(process.env.HOME, '.basemail');
const TOKEN_FILE = path.join(CONFIG_DIR, 'token.json');

/** Read the JWT expiry (the API encodes `exp` in milliseconds). */
function jwtExpiresAt(token) {
  try {
    const payload = JSON.parse(Buffer.from(token.split('.')[1], 'base64').toString('utf8'));
    if (!payload.exp) return null;
    const exp = payload.exp > 1e12 ? payload.exp : payload.exp * 1000;
    return new Date(exp).toISOString();
  } catch {
    return null;
  }
}

function readTokenFile() {
  if (!fs.existsSync(TOKEN_FILE)) return null;
  try {
    return JSON.parse(fs.readFileSync(TOKEN_FILE, 'utf8'));
  } catch {
    return null;
  }
}

function saveTokenFile(data) {
  if (!fs.existsSync(CONFIG_DIR)) fs.mkdirSync(CONFIG_DIR, { recursive: true, mode: 0o700 });
  const merged = { ...(readTokenFile() || {}), ...data, saved_at: new Date().toISOString() };
  if (merged.token && !data.expires_at) merged.expires_at = jwtExpiresAt(merged.token);
  fs.writeFileSync(TOKEN_FILE, JSON.stringify(merged, null, 2), { mode: 0o600 });
  return merged;
}

/**
 * Parse an API response into { ok, status, data }.
 * Non-JSON bodies (HTML error pages, rate-limit pages) become a readable error instead of a JSON parse crash.
 */
async function parseResponse(res) {
  const text = await res.text();
  let data;
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    data = { error: text.slice(0, 200) || res.statusText };
  }
  return { ok: res.ok, status: res.status, data, headers: res.headers };
}

/** Human-readable message for a failed API call. */
function describeError(status, data, headers) {
  const parts = [`HTTP ${status}`];
  if (data && data.error) parts.push(data.error);
  if (data && data.code) parts.push(`(${data.code})`);
  if (status === 429) {
    const retry = headers && headers.get && headers.get('retry-after');
    parts.push(retry ? `— retry after ${retry}s` : '— rate limited, retry later');
  }
  if (data && data.hint) parts.push(`\n   hint: ${data.hint}`);
  return parts.join(' ');
}

/** Exchange refresh_token for a new JWT. Returns the new token or null. */
async function refreshToken(refresh_token) {
  if (!refresh_token) return null;
  const res = await fetch(`${API_BASE}/api/auth/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token }),
  });
  const { ok, data } = await parseResponse(res);
  if (!ok || !data.token) return null;
  saveTokenFile({ token: data.token, refresh_token: data.refresh_token || refresh_token, expires_at: jwtExpiresAt(data.token) });
  return data.token;
}

/**
 * Get a usable bearer token:
 *   1. BASEMAIL_TOKEN env (or BASEMAIL_API_KEY, a long-lived bm_live_… key)
 *   2. ~/.basemail/token.json — refreshed automatically when < 30 min remain
 */
async function getToken() {
  if (process.env.BASEMAIL_API_KEY) return process.env.BASEMAIL_API_KEY;
  if (process.env.BASEMAIL_TOKEN) return process.env.BASEMAIL_TOKEN;

  const data = readTokenFile();
  if (!data || !data.token) {
    console.error('❌ 尚未註冊。請先執行 register.js');
    process.exit(1);
  }

  const expiresAt = data.expires_at || jwtExpiresAt(data.token);
  const msLeft = expiresAt ? new Date(expiresAt).getTime() - Date.now() : Infinity;
  if (msLeft < 30 * 60 * 1000) {
    const fresh = await refreshToken(data.refresh_token);
    if (fresh) {
      console.log('🔄 Token 已自動更新');
      return fresh;
    }
    console.log('⚠️ Token 已過期或即將過期且無法自動更新，請重新執行 register.js');
  }
  return data.token;
}

/**
 * Authenticated fetch with one automatic refresh-and-retry on 401.
 */
async function apiFetch(endpoint, options = {}, token) {
  const doFetch = (t) =>
    fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers: { 'Content-Type': 'application/json', ...(options.headers || {}), Authorization: `Bearer ${t}` },
    });

  let res = await doFetch(token);
  if (res.status === 401 && !process.env.BASEMAIL_TOKEN && !process.env.BASEMAIL_API_KEY) {
    const stored = readTokenFile();
    const fresh = await refreshToken(stored && stored.refresh_token);
    if (fresh) res = await doFetch(fresh);
  }
  return parseResponse(res);
}

module.exports = { API_BASE, CONFIG_DIR, TOKEN_FILE, jwtExpiresAt, readTokenFile, saveTokenFile, parseResponse, describeError, refreshToken, getToken, apiFetch };
