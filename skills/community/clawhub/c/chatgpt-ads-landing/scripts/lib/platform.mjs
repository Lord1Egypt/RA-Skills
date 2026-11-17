/**
 * Hosting-platform client for the skill's optional publish script — zero deps, Node ≥ 22.
 *
 *   auth      device-code login → api-key, stored in ~/.config/chatgpt-ads-landing/credentials.json (0600)
 *   api       JSON calls with the `api-key` header; unwraps BaseResponse {errId, errCode, errMsg, data}
 *   cos       PUT one object to Tencent COS with the STS credential from site/deploy-credential
 *
 * Backend facts this relies on (the hosting platform's backend):
 *   - UnifiedAuthMiddleware accepts `api-key` on every route, so the same endpoints the
 *     the platform's site-hosting and landing-page audit pages call work from here.
 *   - /v1/open-api/device/code and /device/token are on the auth skip list.
 *   - errId 0 = success, 2 = partial success; device polling returns errCode
 *     AUTHORIZATION_PENDING until the user approves.
 */
import { createHash, createHmac } from 'node:crypto';
import { chmodSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join } from 'node:path';

// No default: set BV_API_BASE (or --api-base) to the API address of your hosting platform.
export const DEFAULT_API_BASE = '';
const CRED_FILE = process.env.BV_CREDENTIALS || join(homedir(), '.config', 'chatgpt-ads-landing', 'credentials.json');

export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ---------- credentials ----------

export function readCredentials() {
  const fromFile = existsSync(CRED_FILE) ? JSON.parse(readFileSync(CRED_FILE, 'utf8')) : {};
  return {
    apiBase: (process.env.BV_API_BASE || fromFile.apiBase || DEFAULT_API_BASE).replace(/\/+$/, ''),
    appId: process.env.BV_APP_ID || fromFile.appId || '',
    apiKey: process.env.BV_API_KEY || fromFile.apiKey || '',
    expireTime: fromFile.expireTime || '',
    file: CRED_FILE,
  };
}

function saveCredentials(cred) {
  mkdirSync(dirname(CRED_FILE), { recursive: true, mode: 0o700 });
  const { apiBase, appId, apiKey, expireTime } = cred;
  writeFileSync(CRED_FILE, JSON.stringify({ apiBase, appId, apiKey, expireTime }, null, 2) + '\n', { mode: 0o600 });
  chmodSync(CRED_FILE, 0o600);
}

export function clearCredentials() {
  if (existsSync(CRED_FILE)) { rmSync(CRED_FILE); }
}

// ---------- api ----------

export class ApiError extends Error {
  constructor(message, { status, errCode } = {}) {
    super(message);
    this.status = status;
    this.errCode = errCode;
  }
}

/** One JSON call. `query` goes to the URL for GET/DELETE, `body` is sent as JSON otherwise. */
export async function api(cred, method, path, { query, body, auth = true } = {}) {
  const url = new URL(cred.apiBase + path);
  for (const [k, v] of Object.entries(query || {})) {
    if (v !== undefined && v !== null && v !== '') { url.searchParams.set(k, String(v)); }
  }
  const headers = { 'content-type': 'application/json' };
  if (auth) {
    if (!cred.apiKey) { throw new ApiError('未登录：先运行 publish.mjs login', { errCode: 'NOT_LOGGED_IN' }); }
    headers['api-key'] = cred.apiKey;
  }
  let res;
  try {
    res = await fetch(url, { method, headers, body: body === undefined ? undefined : JSON.stringify(body) });
  } catch (e) {
    throw new ApiError(`连不上 ${cred.apiBase}（${e.cause?.code || e.message}）。api 地址用 --api-base 或环境变量 BV_API_BASE 指定；内网平台需要先连上对应网络`);
  }
  if (res.status === 401) {
    throw new ApiError('api-key 无效或已过期：重新运行 publish.mjs login', { status: 401, errCode: 'UNAUTHORIZED' });
  }
  const text = await res.text();
  let json;
  try { json = JSON.parse(text); } catch (e) {
    throw new ApiError(`${method} ${path} → HTTP ${res.status}，返回的不是 JSON：${text.slice(0, 200)}`, { status: res.status });
  }
  if (json.errId !== 0 && json.errId !== 2) {
    throw new ApiError(`${method} ${path} → ${json.errMsg || json.message || 'unknown error'}${json.errCode ? ` (${json.errCode})` : ''}`,
      { status: res.status, errCode: json.errCode || json.reason });
  }
  return json.data;
}

// ---------- device-code login ----------

export async function deviceLogin({ apiBase, appId, onCode }) {
  const cred = { ...readCredentials(), apiBase: (apiBase || readCredentials().apiBase).replace(/\/+$/, '') };
  cred.appId = appId || cred.appId;
  if (!cred.appId) { throw new ApiError('缺少 app_id：用 --app-id 或环境变量 BV_APP_ID 指定开发者应用'); }

  const code = await api(cred, 'POST', '/v1/open-api/device/code', { body: { app_id: cred.appId }, auth: false });
  onCode(code);
  const interval = Math.max(2, code.interval || 5) * 1000;
  const deadline = Date.now() + (code.expires_in || 600) * 1000;
  while (Date.now() < deadline) {
    await sleep(interval);
    try {
      const tok = await api(cred, 'POST', '/v1/open-api/device/token',
        { body: { device_code: code.device_code, app_id: cred.appId }, auth: false });
      if (tok?.access_token) {
        saveCredentials({ ...cred, apiKey: tok.access_token, expireTime: tok.expire_time || '' });
        return { ...cred, apiKey: tok.access_token, expireTime: tok.expire_time || '' };
      }
    } catch (e) {
      if (e.errCode === 'AUTHORIZATION_PENDING') { continue; }
      throw e;
    }
  }
  throw new ApiError('授权超时：设备码已过期，重新运行 login');
}

// ---------- COS ----------

const sha1 = (s) => createHash('sha1').update(s).digest('hex');
const hmac = (key, s) => createHmac('sha1', key).update(s).digest('hex');
const enc = (s) => encodeURIComponent(s).replace(/[!'()*]/g, (c) => '%' + c.charCodeAt(0).toString(16).toUpperCase());

/** COS v5 request signature (https://cloud.tencent.com/document/product/436/7778), signing only `host`. */
export function cosAuthorization({ secretId, secretKey, method, path, host, expire, now = Math.floor(Date.now() / 1000) - 60 }) {
  const keyTime = `${now};${Math.max(now + 120, expire)}`;
  const httpString = `${method.toLowerCase()}\n${path}\n\nhost=${enc(host)}\n`;
  const stringToSign = `sha1\n${keyTime}\n${sha1(httpString)}\n`;
  const signature = hmac(hmac(secretKey, keyTime), stringToSign);
  return `q-sign-algorithm=sha1&q-ak=${secretId}&q-sign-time=${keyTime}&q-key-time=${keyTime}`
    + `&q-header-list=host&q-url-param-list=&q-signature=${signature}`;
}

/** PUT one object. `credential` is the data of GET /v1/site-hosting/site/deploy-credential. */
export async function cosPut(credential, key, body, contentType) {
  const host = `${credential.bucket}.cos.${credential.region}.myqcloud.com`;
  const path = '/' + key.replace(/^\/+/, '');
  const authorization = cosAuthorization({
    secretId: credential.tmp_secret_id, secretKey: credential.tmp_secret_key,
    method: 'PUT', path, host, expire: Number(credential.expire),
  });
  // BV_COS_ENDPOINT points uploads at a stand-in server for tests; the signature still names the real host.
  const endpoint = process.env.BV_COS_ENDPOINT || `https://${host}`;
  const res = await fetch(`${endpoint}${path.split('/').map(enc).join('/')}`, {
    method: 'PUT',
    headers: {
      authorization,
      'x-cos-security-token': credential.session_token,
      'content-type': contentType,
      'content-length': String(body.length),
    },
    body,
  });
  if (!res.ok) {
    const text = await res.text();
    const code = /<Code>([^<]+)<\/Code>/.exec(text)?.[1] || '';
    throw new Error(`COS PUT ${key} → HTTP ${res.status} ${code}`);
  }
}
