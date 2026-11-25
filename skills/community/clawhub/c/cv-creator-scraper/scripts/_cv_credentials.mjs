// Cache + lazy-fetch CV API credentials for Navos desktop users.
//
// Flow
// ----
//   1. Navos users always prefer Navos identity + env-scoped cache.
//      CV_API_KEY is ignored for Navos unless CV_ALLOW_ENV_API_KEY=true.
//   2. Non-Navos/dev path may use CV_API_KEY as an explicit override.
//   3. Otherwise read Navos identity from env or local identity file.
//   4. If an env-scoped cache entry exists, validate the local Navos uid/token
//      through CV's partner-user validate endpoint, then return cached api_key.
//   5. If no cache exists, call CV ensure endpoint, cache, then return.
//
// Cache schema:
//   {
//     "<partner_code>:<skill_channel>@<cv_host>:<uid>": {
//       "api_key":     "cv_live_navos_xxx",
//       "key_prefix":  "cv_live_n",
//       "user_id":     "<cv-user-uuid>",
//       "issued_at":   "2026-06-23T10:00:00Z",
//       "navos_email": "user@navos.local",
//       "cv_user_identity": "cn_user@navos.local",
//       "navos_token_hash": "<sha256>",
//       "navos_validated_at": "2026-07-01T10:00:00Z",
//       "navos_region": "cn",
//       "skill_channel": "stable",
//       "cv_base": "https://creativault-business.creativault.ai"
//     }
//   }
//
// Cache invalidation: when Navos uid/token validation fails, only the current
// env+uid cache entry is removed. CV OpenAPI auth failures (40101/40102/40103)
// remain authoritative and must not trigger client-side re-issuing.

import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { createHash, randomBytes } from 'node:crypto';

import { loadNavosIdentity } from './_navos_identity.mjs';

const DEFAULT_PARTNER_CODE = process.env.CV_PARTNER_CODE || 'navos';
const DEFAULT_CV_BASE = (process.env.CV_API_BASE_URL || '').replace(/\/+$/, '');
const SKILL_CHANNEL = loadDefaultSkillChannel();

const CACHE_DIR = process.env.CV_CREDENTIALS_DIR
  || join(homedir(), '.creativault');
const CACHE_FILE = join(CACHE_DIR, 'skill-credentials.json');

function loadDefaultSkillChannel() {
  const explicit = (process.env.CV_SKILL_CHANNEL || '').trim();
  if (explicit) return explicit;
  try {
    const meta = JSON.parse(readFileSync(new URL('../skill.json', import.meta.url), 'utf8'));
    return meta?.channel || 'stable';
  } catch {
    return 'stable';
  }
}

// ---------------------------------------------------------------------------
// Cache I/O
// ---------------------------------------------------------------------------

function readCache() {
  if (!existsSync(CACHE_FILE)) return {};
  try {
    return JSON.parse(readFileSync(CACHE_FILE, 'utf8')) || {};
  } catch {
    return {};
  }
}

function writeCache(cache) {
  if (!existsSync(CACHE_DIR)) {
    mkdirSync(CACHE_DIR, { recursive: true });
  }
  // Best-effort write; failure to cache should not break the call path.
  try {
    writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2), { encoding: 'utf8' });
  } catch (err) {
    process.stderr.write(
      `[cv-credentials] warning: failed to write cache (${err.code || err.name}); will re-ensure next run\n`,
    );
  }
}

function normalizeCachePart(value) {
  return String(value || 'unknown')
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9._-]+/g, '_')
    .replace(/^_+|_+$/g, '')
    || 'unknown';
}

function cacheEnv(cvBase = DEFAULT_CV_BASE, skillChannel = SKILL_CHANNEL, navosRegion = '') {
  let host = '';
  try {
    host = new URL(cvBase).host;
  } catch {
    host = cvBase || 'default';
  }
  const regionPart = navosRegion ? `:${normalizeCachePart(navosRegion)}` : '';
  return `${normalizeCachePart(skillChannel)}${regionPart}@${normalizeCachePart(host)}`;
}

function legacyCacheKey(partnerCode, uid) {
  return `${partnerCode}:${uid}`;
}

function cacheKey(partnerCode, uid, env = cacheEnv()) {
  return `${partnerCode}:${env}:${uid}`;
}

function tokenHash(token) {
  return createHash('sha256').update(String(token || ''), 'utf8').digest('hex');
}

function isTruthyEnv(value) {
  return ['1', 'true', 'yes', 'on'].includes(String(value || '').trim().toLowerCase());
}

function isCnRegion(value) {
  const region = String(value || '').trim().toLowerCase();
  return region === 'cn' || region === 'china' || region === 'mainland' || region === 'navos-cn';
}

function isNavosPartnerCode(value) {
  return ['navos', 'navos-cn', 'navos-global'].includes(normalizeCachePart(value));
}

function buildCvUserIdentity(email, navosRegion) {
  const identity = String(email || '').trim();
  if (!identity || !isCnRegion(navosRegion) || identity.startsWith('cn_')) {
    return identity;
  }
  return `cn_${identity}`;
}

function shouldUseEnvApiKey({ partnerCode }) {
  if (!isNavosPartnerCode(partnerCode)) return true;

  // Navos 专用版必须默认走 Navos uid/token + 本地环境化缓存，避免用户机器上
  // 残留的 CV 平台 API Key 覆盖 Navos 授权链路。仅调试时显式开启。
  if (isTruthyEnv(process.env.CV_ALLOW_ENV_API_KEY)) {
    return true;
  }

  // beta/dev 也默认不吃 CV_API_KEY，保持与 stable 一致。
  return false;
}

export function invalidateCachedApiKey(partnerCode = DEFAULT_PARTNER_CODE, uid = null, env = cacheEnv()) {
  const cache = readCache();
  if (!uid) {
    // No uid known: drop everything for this partner_code.
    let mutated = false;
    for (const key of Object.keys(cache)) {
      if (key.startsWith(`${partnerCode}:`)) {
        delete cache[key];
        mutated = true;
      }
    }
    if (mutated) writeCache(cache);
    return;
  }
  const key = cacheKey(partnerCode, uid, env);
  const legacyKey = legacyCacheKey(partnerCode, uid);
  let mutated = false;
  for (const candidate of [key, legacyKey]) {
    if (cache[candidate]) {
      delete cache[candidate];
      mutated = true;
    }
  }
  if (mutated) {
    writeCache(cache);
  }
}

// ---------------------------------------------------------------------------
// CV ensure call
// ---------------------------------------------------------------------------

function buildPartnerHeaders(partnerCode, opts = {}) {
  const headers = {
    'Content-Type': 'application/json',
    'X-Partner-Code': partnerCode,
    'X-Timestamp': Math.floor(Date.now() / 1000).toString(),
    'X-Nonce': randomBytes(16).toString('hex'),
  };
  if (opts.navosRegion) {
    headers['X-Navos-Region'] = String(opts.navosRegion);
  }
  if (opts.navosValidateBaseUrl) {
    headers['X-Navos-Validate-Base-Url'] = String(opts.navosValidateBaseUrl);
  }
  if (opts.navosCallbackBaseUrl) {
    headers['X-Navos-Callback-Base-Url'] = String(opts.navosCallbackBaseUrl);
  }
  return headers;
}

/**
 * Call CV `/internal/partners/{partner_code}/users/validate`.
 *
 * This endpoint validates the local Navos uid/token only. It does not issue or
 * return a CV API Key.
 *
 * @param {object} args
 * @param {string} args.cvBase
 * @param {string} args.partnerCode
 * @param {string} args.uid
 * @param {string} args.token
 * @returns {Promise<boolean>}
 */
async function callPartnerUserValidate({
  cvBase,
  partnerCode,
  uid,
  token,
  navosRegion = '',
  navosValidateBaseUrl = '',
  navosCallbackBaseUrl = '',
}) {
  const url = `${cvBase}/internal/partners/${encodeURIComponent(partnerCode)}/users/validate`;
  const body = {
    uid,
    token,
    ...(navosRegion && { navos_region: navosRegion }),
    ...(navosValidateBaseUrl && { navos_validate_base_url: navosValidateBaseUrl }),
    ...(navosCallbackBaseUrl && { navos_callback_base_url: navosCallbackBaseUrl }),
  };

  let resp;
  try {
    resp = await fetch(url, {
      method: 'POST',
      headers: buildPartnerHeaders(partnerCode, {
        navosRegion,
        navosValidateBaseUrl,
        navosCallbackBaseUrl,
      }),
      body: JSON.stringify(body),
    });
  } catch (err) {
    const e = new Error(`CV partner user validation request failed: ${err.message}`);
    e.cause = err;
    throw e;
  }

  let payload = null;
  try {
    payload = await resp.json();
  } catch {
    // Keep payload null; non-JSON error handling below will include HTTP status.
  }

  if (resp.status === 401) {
    const reason = payload?.detail || payload?.en_message || payload?.zh_message || 'HTTP 401';
    const err = new Error(`CV partner user validation rejected: ${reason}`);
    err.status = resp.status;
    err.payload = payload;

    if (reason === 'Partner user validation failed') {
      return false;
    }
    throw err;
  }

  if (!resp.ok || payload?.code !== 200) {
    const reason = payload?.en_message || payload?.zh_message || `HTTP ${resp.status}`;
    const err = new Error(`CV partner user validation failed: ${reason}`);
    err.status = resp.status;
    err.payload = payload;
    throw err;
  }

  return payload?.data?.valid === true;
}

/**
 * Call CV `/internal/partners/{partner_code}/api-keys/ensure`.
 *
 * @param {object} args
 * @param {string} args.cvBase       e.g. https://api.creativault.vip/skill/creativault
 * @param {string} args.partnerCode  e.g. "navos"
 * @param {string} args.uid
 * @param {string} args.token
 * @param {string} args.email
 * @param {string} args.navosEmail
 * @param {string} args.clientVersion
 * @returns {Promise<{api_key: string, key_prefix: string, user_id: string, is_new: boolean}>}
 */
async function callEnsure({
  cvBase,
  partnerCode,
  uid,
  token,
  email,
  navosEmail = '',
  clientVersion,
  navosRegion = '',
  navosValidateBaseUrl = '',
  navosCallbackBaseUrl = '',
}) {
  const url = `${cvBase}/internal/partners/${encodeURIComponent(partnerCode)}/api-keys/ensure`;

  const body = {
    uid,
    token,
    email,
    ...(navosEmail && { navos_email: navosEmail }),
    client_version: clientVersion || '',
    ...(navosRegion && { navos_region: navosRegion }),
    ...(navosValidateBaseUrl && { navos_validate_base_url: navosValidateBaseUrl }),
    ...(navosCallbackBaseUrl && { navos_callback_base_url: navosCallbackBaseUrl }),
  };

  let resp;
  try {
    resp = await fetch(url, {
      method: 'POST',
      headers: buildPartnerHeaders(partnerCode, {
        navosRegion,
        navosValidateBaseUrl,
        navosCallbackBaseUrl,
      }),
      body: JSON.stringify(body),
    });
  } catch (err) {
    const e = new Error(`CV ensure request failed: ${err.message}`);
    e.cause = err;
    throw e;
  }

  let payload;
  try {
    payload = await resp.json();
  } catch {
    throw new Error(`CV ensure returned non-JSON (HTTP ${resp.status})`);
  }

  if (!resp.ok || payload?.code !== 200) {
    // payload may be {code, en_message, zh_message, data}
    const reason = payload?.en_message || payload?.zh_message || `HTTP ${resp.status}`;
    const err = new Error(`CV ensure rejected: ${reason}`);
    err.status = resp.status;
    err.payload = payload;
    throw err;
  }

  const data = payload?.data || {};
  if (!data.api_key) {
    throw new Error('CV ensure returned no api_key. Response shape unexpected.');
  }
  return data;
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Resolve the CV API key for the current Navos desktop session.
 *
 * Caching strategy:
 *   - Navos partner users prefer Navos identity and env-scoped cache.
 *   - CV_API_KEY is only honored for Navos when CV_ALLOW_ENV_API_KEY=true.
 *   - Else read Navos identity, look up cache by (partner_code, uid).
 *   - On miss / forceRefresh: call ensure and persist.
 *
 * @param {object} [opts]
 * @param {boolean} [opts.forceRefresh=false]
 * @param {string}  [opts.partnerCode]
 * @param {string}  [opts.cvBase]
 * @param {string}  [opts.skillChannel]
 * @returns {Promise<{
 *   apiKey: string,
 *   userIdentity: string,
 *   partnerCode: string,
 *   uid: string,
 *   userId: string | null,
 *   isNew: boolean,
 *   source: 'env' | 'cache' | 'ensure',
 * }>}
 */
export async function resolveCvCredentials(opts = {}) {
  const partnerCode = (opts.partnerCode || DEFAULT_PARTNER_CODE).trim();
  const cvBase = (opts.cvBase || DEFAULT_CV_BASE).replace(/\/+$/, '');
  const skillChannel = (opts.skillChannel || SKILL_CHANNEL).trim();
  const navosRegion = (opts.navosRegion || process.env.NAVOS_REGION || '').trim();
  const navosValidateBaseUrl = (opts.navosValidateBaseUrl || process.env.NAVOS_VALIDATE_BASE_URL || '').replace(/\/+$/, '');
  const navosCallbackBaseUrl = (opts.navosCallbackBaseUrl || process.env.NAVOS_CALLBACK_BASE_URL || '').replace(/\/+$/, '');
  const forceRefresh = Boolean(opts.forceRefresh);
  const env = cacheEnv(cvBase, skillChannel, navosRegion);

  // 1) Manual override via env var only wins for non-Navos, or explicit Navos debug.
  const explicitKey = (process.env.CV_API_KEY || '').trim();
  if (explicitKey && !forceRefresh && shouldUseEnvApiKey({ partnerCode })) {
    const userIdentity = (process.env.CV_USER_IDENTITY || '').trim();
    return {
      apiKey: explicitKey,
      userIdentity,
      partnerCode,
      uid: '',
      userId: null,
      isNew: false,
      source: 'env',
      cacheEnv: env,
    };
  }
  if (explicitKey && !forceRefresh) {
    process.stderr.write(
      `[cv-credentials] warning: CV_API_KEY env var ignored for partner=${partnerCode} channel=${skillChannel}; `
      + 'using Navos credentials cache instead. Set CV_ALLOW_ENV_API_KEY=true only for debugging.\n',
    );
  }

  // 2) Need Navos identity from here on.
  const identity = loadNavosIdentity();
  const cvUserIdentity = buildCvUserIdentity(identity.email, navosRegion);

  // 3) Cache lookup
  const cache = readCache();
  const key = cacheKey(partnerCode, identity.uid, env);
  if (!forceRefresh && cache[key]?.api_key) {
    if (!cvBase) {
      throw new Error(
        'CV_API_BASE_URL is not configured. Set CV_API_BASE_URL or pass {cvBase} to resolveCvCredentials.',
      );
    }

    const isValidNavosSession = await callPartnerUserValidate({
      cvBase,
      partnerCode,
      uid: identity.uid,
      token: identity.token,
      navosRegion,
      navosValidateBaseUrl,
      navosCallbackBaseUrl,
    });

    if (!isValidNavosSession) {
      delete cache[key];
      writeCache(cache);
      const err = new Error(
        'Navos session validation failed. Local CV API Key cache was cleared; please re-login to Navos and retry.',
      );
      err.status = 401;
      err.code = 'NAVOS_SESSION_INVALID';
      throw err;
    }

    cache[key] = {
      ...cache[key],
      navos_email: identity.email,
      cv_user_identity: cvUserIdentity,
      navos_token_hash: tokenHash(identity.token),
      navos_validated_at: new Date().toISOString(),
      navos_region: navosRegion || null,
      navos_validate_base_url: navosValidateBaseUrl || null,
      navos_callback_base_url: navosCallbackBaseUrl || null,
      skill_channel: skillChannel,
      cv_base: cvBase,
    };
    writeCache(cache);

    return {
      apiKey: cache[key].api_key,
      userIdentity: cache[key].cv_user_identity || cvUserIdentity || cache[key].navos_email || identity.email,
      partnerCode,
      uid: identity.uid,
      userId: cache[key].user_id || null,
      isNew: false,
      source: 'cache',
      cacheEnv: env,
    };
  }

  // 4) Need to call ensure; require cvBase configured.
  if (!cvBase) {
    throw new Error(
      'CV_API_BASE_URL is not configured. Set CV_API_BASE_URL or pass {cvBase} to resolveCvCredentials.',
    );
  }

  const data = await callEnsure({
    cvBase,
    partnerCode,
    uid: identity.uid,
    token: identity.token,
    email: cvUserIdentity,
    navosEmail: identity.email,
    clientVersion: skillChannel,
    navosRegion,
    navosValidateBaseUrl,
    navosCallbackBaseUrl,
  });

  cache[key] = {
    api_key: data.api_key,
    key_prefix: data.key_prefix,
    user_id: data.user_id,
    issued_at: new Date().toISOString(),
    navos_email: identity.email,
    cv_user_identity: cvUserIdentity,
    navos_token_hash: tokenHash(identity.token),
    navos_validated_at: new Date().toISOString(),
    navos_region: navosRegion || null,
    navos_validate_base_url: navosValidateBaseUrl || null,
    navos_callback_base_url: navosCallbackBaseUrl || null,
    skill_channel: skillChannel,
    cv_base: cvBase,
  };
  writeCache(cache);

  return {
    apiKey: data.api_key,
    userIdentity: cvUserIdentity,
    partnerCode,
    uid: identity.uid,
    userId: data.user_id || null,
    isNew: Boolean(data.is_new),
    source: 'ensure',
    cacheEnv: env,
  };
}
