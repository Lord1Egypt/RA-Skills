// ---------------------------------------------------------------------------
// OAuth device-flow login (RFC 8628) for the published `evolver` CLI.
//
// `evolver login` runs the device authorization grant against the hub
// (gh-auth-login style): print a user code + verification URL, poll until the
// user approves in the browser, then store the token at ~/.evomap/oauth_token.json.
//
// The resulting access token is consumed by a2aProtocol.buildHubHeaders() for
// user-scoped Hub APIs. Node-scoped A2A endpoints use node_secret via
// buildNodeScopedHubHeaders().
// ---------------------------------------------------------------------------
'use strict';

const fs = require('fs');
const path = require('path');
const { getEvomapDir } = require('./paths');
const { resolveHubUrl: resolveDefaultHubUrl } = require('../config');
const { enforceHubScheme, hubFetch } = require('./hubFetch');

const CLIENT_ID = 'evolver-cli';
const DEVICE_GRANT = 'urn:ietf:params:oauth:grant-type:device_code';
const DEFAULT_SCOPES = 'a2a recipe:read recipe:write recipe:publish gene:read reuse:query';
const OAUTH_TIMEOUT_MS = 30000;
// Refresh slightly early so a token in active use does not expire mid-request.
const EXPIRY_SKEW_MS = 60 * 1000;

function tokenFile() { return path.join(getEvomapDir(), 'oauth_token.json'); }

/** @returns {{access_token:string, refresh_token?:string, expires_at:number, scope?:string}|null} */
function loadOAuthToken() {
  try {
    const raw = fs.readFileSync(tokenFile(), 'utf8');
    const t = JSON.parse(raw);
    if (t && typeof t.access_token === 'string' && t.access_token) return t;
  } catch {}
  return null;
}

/** Sync: the current access token if present and not (nearly) expired, else null. */
function loadValidAccessToken() {
  const t = loadOAuthToken();
  if (!t) return null;
  if (typeof t.expires_at === 'number' && t.expires_at - EXPIRY_SKEW_MS <= Date.now()) return null;
  return t.access_token;
}

function saveOAuthToken(tok) {
  const dir = getEvomapDir();
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
  fs.writeFileSync(tokenFile(), JSON.stringify(tok, null, 2), { encoding: 'utf8', mode: 0o600 });
}

function clearOAuthToken() {
  try { fs.unlinkSync(tokenFile()); return true; } catch { return false; }
}

function resolveHubUrl(explicit) {
  const u = explicit
    ? String(explicit).replace(/\/+$/, '')
    : resolveDefaultHubUrl().replace(/\/+$/, '');
  enforceHubScheme(u);
  return u;
}

async function postJson(url, body) {
  const res = await hubFetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(OAUTH_TIMEOUT_MS),
  });
  let json = {};
  try { json = await res.json(); } catch {}
  return { status: res.status, json };
}

function toStored(json, prev) {
  return {
    access_token: json.access_token,
    refresh_token: json.refresh_token || (prev && prev.refresh_token) || undefined,
    expires_at: Date.now() + (Number(json.expires_in) > 0 ? json.expires_in * 1000 : 3600 * 1000),
    scope: json.scope,
  };
}

/**
 * Run the full device flow and persist the token. `onCode` is invoked once with
 * { userCode, verificationUri } so the caller can show the user where to go.
 * @returns {Promise<{access_token:string, expires_at:number, scope?:string}>}
 */
async function deviceLogin(opts = {}) {
  const hubUrl = resolveHubUrl(opts.hubUrl);
  const scope = opts.scope || DEFAULT_SCOPES;
  const onCode = opts.onCode || (() => {});
  const sleep = opts.sleep || ((ms) => new Promise((r) => setTimeout(r, ms)));
  const now = opts.now || (() => Date.now());

  const start = await postJson(`${hubUrl}/oauth/device_authorization`, { client_id: CLIENT_ID, scope });
  const s = start.json || {};
  if (start.status >= 400 || !s.device_code || !s.user_code) {
    throw new Error(`device_authorization failed (HTTP ${start.status}): ${s.error || 'no device_code'}`);
  }
  onCode({ userCode: s.user_code, verificationUri: s.verification_uri_complete || s.verification_uri || `${hubUrl}/device` });

  const deadline = now() + (opts.maxWaitMs || 15 * 60 * 1000);
  let intervalMs = (Number(s.interval) > 0 ? s.interval : 5) * 1000;
  for (;;) {
    await sleep(intervalMs);
    const poll = await postJson(`${hubUrl}/oauth/token`, { grant_type: DEVICE_GRANT, device_code: s.device_code, client_id: CLIENT_ID });
    const p = poll.json || {};
    if (p.access_token) {
      const tok = toStored(p, null);
      saveOAuthToken(tok);
      return tok;
    }
    if (p.error === 'authorization_pending') { /* keep waiting */ }
    else if (p.error === 'slow_down') { intervalMs += 5000; }
    else throw new Error(`device login failed (HTTP ${poll.status}): ${p.error || 'unknown'}`);
    if (now() >= deadline) throw new Error('device_flow_timeout');
  }
}

/** Refresh the stored token via the refresh_token grant. Returns the new access token, or null if not possible. */
async function refreshOAuthToken(opts = {}) {
  const t = loadOAuthToken();
  if (!t || !t.refresh_token) return null;
  const hubUrl = resolveHubUrl(opts.hubUrl);
  const res = await postJson(`${hubUrl}/oauth/token`, { grant_type: 'refresh_token', refresh_token: t.refresh_token, client_id: CLIENT_ID });
  const p = res.json || {};
  if (!p.access_token) return null;
  const tok = toStored(p, t);
  saveOAuthToken(tok);
  return tok.access_token;
}

/**
 * Background auto-refresh for long-running processes (`evolver run`): schedule a
 * refresh ~2min before the current token expires, then reschedule after each
 * refresh. No-op when there is no refresh token (e.g. node_secret-only nodes).
 * The timer is unref'd so it never blocks process exit. Returns a stop() fn.
 * `now`/`setTimer`/`clearTimer` are injectable for tests.
 */
function startTokenAutoRefresh(opts = {}) {
  const now = opts.now || (() => Date.now());
  const setTimer = opts.setTimer || ((fn, ms) => setTimeout(fn, ms));
  const clearTimer = opts.clearTimer || ((h) => clearTimeout(h));
  const MIN_DELAY_MS = 15 * 1000;
  const SKEW_MS = 2 * 60 * 1000;
  let handle = null;
  let stopped = false;

  function scheduleNext() {
    if (stopped) return;
    const t = loadOAuthToken();
    // Only auto-refresh when we actually have a refresh token to use.
    if (!t || !t.refresh_token || typeof t.expires_at !== 'number') return;
    const delay = Math.max(MIN_DELAY_MS, t.expires_at - now() - SKEW_MS);
    handle = setTimer(async () => {
      try { await refreshOAuthToken(opts); } catch {}
      scheduleNext();
    }, delay);
    if (handle && typeof handle.unref === 'function') handle.unref();
  }

  scheduleNext();
  return function stop() { stopped = true; if (handle) clearTimer(handle); };
}

module.exports = {
  tokenFile,
  loadOAuthToken,
  loadValidAccessToken,
  saveOAuthToken,
  clearOAuthToken,
  resolveHubUrl,
  deviceLogin,
  refreshOAuthToken,
  startTokenAutoRefresh,
  CLIENT_ID,
  DEFAULT_SCOPES,
};
