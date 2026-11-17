import { execFile } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import { resolve, isAbsolute, join } from 'node:path';
import { BridgeError } from './bridge.mjs';
const stop = code => { throw new BridgeError(code); };
// Strict allowlist: unrelated credentials, NODE_OPTIONS, and BW_SESSION never reach Keychain.
export function childEnv(env = process.env) {
  return Object.fromEntries(['PATH','HOME','USER','TMPDIR','LANG','SSL_CERT_FILE','NODE_EXTRA_CA_CERTS','BITWARDENCLI_APPDATA_DIR'].filter(k => env[k]).map(k => [k, env[k]]));
}
export function captured(file, args, env, timeout = 15000) {
  return new Promise((yes, no) => execFile(file, args, { env, timeout, maxBuffer: 16 * 1024 * 1024, encoding: 'utf8' }, (error, stdout) => error ? no(new BridgeError(error.killed ? 'SUBPROCESS_TIMEOUT' : 'SUBPROCESS_FAILED')) : yes(stdout)));
}
export function createVault({ profile = {}, platform = process.platform, env = process.env, run = captured, now = Date.now, sleep = ms => new Promise(r => setTimeout(r, ms)) } = {}) {
  const base = childEnv(env); let session = env.BW_SESSION || '';
  const bw = async args => run('bw', args, { ...base, ...(session ? { BW_SESSION: session } : {}) });
  return {
    status: async () => JSON.parse(await bw(['status'])),
    unlock: async () => {
      if (platform !== 'darwin' || !profile.keychainAccount || !profile.keychainService) stop('UNLOCK_PROVIDER_MISSING');
      const password = (await run('/usr/bin/security', ['find-generic-password','-a',profile.keychainAccount,'-s',profile.keychainService,'-w'], base)).replace(/\r?\n$/, '');
      if (!password) stop('KEYCHAIN_EMPTY');
      session = (await run('bw', ['unlock','--raw','--passwordenv','BW_PASSWORD'], { ...base, BW_PASSWORD: password })).trim();
      if (!session) stop('UNLOCK_FAILED');
    },
    items: async () => JSON.parse(await bw(['list','items'])),
    totp: async item => {
      // Need a known period, not an assumed 30s for an arbitrary URI.
      const seed = item.login?.totp; let period = 30;
      if (typeof seed !== 'string' || !seed) stop('MISSING_TOTP');
      if (seed.startsWith('otpauth://')) {
        let u; try { u = new URL(seed); } catch { stop('UNSUPPORTED_TOTP'); }
        if (u.hostname !== 'totp') stop('UNSUPPORTED_TOTP');
        if (u.searchParams.has('period')) period = Number(u.searchParams.get('period'));
      } else if (!/^[A-Z2-7 =]+$/i.test(seed)) stop('UNSUPPORTED_TOTP');
      if (!Number.isInteger(period) || period < 15 || period > 120) stop('UNSUPPORTED_TOTP');
      let remaining = () => period * 1000 - now() % (period * 1000);
      if (remaining() < 12000) await sleep(remaining() + 100);
      const tick = Math.floor(now() / (period * 1000));
      const code = (await bw(['get','totp',item.id])).trim();
      if (Math.floor(now() / (period * 1000)) !== tick || remaining() < 10000) stop('TOTP_TOO_OLD');
      return { code, expiresAt: (tick + 1) * period * 1000 };
    },
  };
}
// Fixed, nonsecret inspector. Never returns values, prose, labels, or arbitrary DOM text.
export function inspectionExpression(selector) {
  return '(' + inspectPage.toString() + ')(' + JSON.stringify(selector) + ')';
}
function inspectPage(selector) {
  const nodes = document.querySelectorAll(selector);
  const e = nodes[0];
  const result = { url: location.origin, top: window === window.top, count: nodes.length };
  // Credential-bearing location URL must be rejected even though origin hides userinfo.
  if (new URL(location.href).username || new URL(location.href).password) result.url = 'invalid';
  if (nodes.length !== 1) return result;
  const s = getComputedStyle(e), r = e.getBoundingClientRect();
  const actions = [];
  if (e.form) {
    actions.push(e.form.action);
    for (const b of e.form.elements) if (b.hasAttribute('formaction')) actions.push(b.formAction);
    if (e.form.target && !['_self',''].includes(e.form.target)) actions.push('invalid');
    for (const b of e.form.elements) if (b.hasAttribute('formtarget') && b.formTarget !== '_self') actions.push('invalid');
  }
  return { ...result, tag: e.tagName, type: e.type, disabled: e.matches(':disabled'), readOnly: !!e.readOnly,
    visible: !e.hidden && !e.closest('[hidden],[inert]') && s.display !== 'none' && s.visibility === 'visible' && Number(s.opacity) > 0 && r.width > 0 && r.height > 0 && e.getClientRects().length > 0,
    actions };
}
export async function createBrowser({ runtimePath, configPath, userId, sessionKey, read = readFile } = {}) {
  if (!runtimePath || !isAbsolute(runtimePath) || !configPath || !isAbsolute(configPath) || !userId || !sessionKey) stop('RUNTIME_REQUIRED');
  let manifest;
  try { manifest = JSON.parse(await read(resolve(runtimePath, 'package.json'), 'utf8')); } catch { stop('UNSUPPORTED_CAMOFOX_BUILD'); }
  if (manifest.name !== '@askjo/camofox-browser' || manifest.version !== '1.18.1') stop('UNSUPPORTED_CAMOFOX_BUILD');
  // Explicit trusted installed package root only: no caller-supplied JS source or adapter expression.
  const [{ runTool }, { loadConfig }] = await Promise.all([
    import(pathToFileURL(resolve(runtimePath, 'mcp/lib/tool-contracts.mjs')).href),
    import(pathToFileURL(resolve(runtimePath, 'lib/config.js')).href),
  ]);
  if (typeof runTool !== 'function' || typeof loadConfig !== 'function') stop('UNSUPPORTED_CAMOFOX_BUILD');
  const root = JSON.parse(await read(configPath, 'utf8'));
  const settings = root.plugins?.entries?.['camofox-browser']?.config;
  if (!settings) stop('CAMOFOX_CONFIG_MISSING');
  const baseUrl = settings.url || (settings.port ? 'http://localhost:' + settings.port : null);
  if (!baseUrl) stop('CAMOFOX_URL_MISSING');
  const u = new URL(baseUrl);
  if (!['127.0.0.1','localhost','[::1]'].includes(u.hostname) || !['http:','https:'].includes(u.protocol) || u.username || u.password || u.pathname !== '/' || u.search || u.hash) stop('UNSAFE_CAMOFOX_ENDPOINT');
  const cfg = loadConfig();
  return browserFromContract({ runTool, ctx: { userId, sessionKey }, baseUrl: u.origin, cfg });
}
// Dependency injection seam for synthetic tests; never available through CLI request JSON.
export function browserFromContract({ runTool, ctx, baseUrl, cfg = {}, timeoutMs = 15000 }) {
  const call = async (name, args) => {
    // Contract has no AbortSignal: a timeout means outcome unknown, never retry automatically.
    let timer;
    try { return (await Promise.race([runTool(name, args, ctx, baseUrl, cfg), new Promise((_, reject) => { timer = setTimeout(() => reject(new BridgeError('BROWSER_TIMEOUT')), timeoutMs); })])).payload; }
    finally { clearTimeout(timer); }
  };
  return {
    inspect: async (tabId, selector) => {
      const p = await call('camofox_evaluate', { tabId, expression: inspectionExpression(selector) });
      if (p?.ok !== true || !p.result || typeof p.result !== 'object') stop('BROWSER_INSPECTION_FAILED');
      return p.result;
    },
    type: async (tabId, selector, text) => {
      const p = await call('camofox_type', { tabId, selector, text, pressEnter: false });
      if (p?.ok !== true) stop('BROWSER_FILL_FAILED');
      // No raw response or request object escapes this function.
    },
  };
}

// Trusted local NONSECRET profile; never return it to caller output.
export async function loadProfile({ env = process.env, read = readFile } = {}) {
  const home = env.HOME;
  const configHome = env.XDG_CONFIG_HOME || (home && join(home, '.config'));
  const path = env.CAMOFOX_VAULT_CONFIG || (configHome && join(configHome, 'camofox-vault-login', 'config.json'));
  if (!path || !isAbsolute(path)) stop('PROFILE_PATH_REQUIRED');
  let profile;
  try { profile = JSON.parse(await read(path, 'utf8')); } catch { stop('PROFILE_UNAVAILABLE'); }
  if (!profile || typeof profile !== 'object' || Array.isArray(profile)) stop('PROFILE_INVALID');
  const allowed = ['expectedVaultServerUrl','expectedVaultEmail','keychainService','keychainAccount','camofoxRuntimePath','openclawConfigPath'];
  if (Object.keys(profile).some(k => !allowed.includes(k)) || Object.values(profile).some(v => typeof v !== 'string' || !v || /[\r\n\0]/.test(v))) stop('PROFILE_INVALID');
  if (!profile.expectedVaultServerUrl || !profile.expectedVaultEmail) stop('VAULT_IDENTITY_REQUIRED');
  let u; try { u = new URL(profile.expectedVaultServerUrl); } catch { stop('PROFILE_INVALID'); }
  if (u.protocol !== 'https:' || u.username || u.password || u.search || u.hash || u.pathname !== '/') stop('PROFILE_INVALID');
  if (!!profile.keychainAccount !== !!profile.keychainService) stop('PROFILE_INVALID');
  const stateDir = env.OPENCLAW_STATE_DIR || (home && join(home, '.openclaw'));
  const runtimePath = profile.camofoxRuntimePath || (stateDir && join(stateDir, 'extensions', 'camofox-browser'));
  const configPath = profile.openclawConfigPath || (stateDir && join(stateDir, 'openclaw.json'));
  if (!runtimePath || !configPath || !isAbsolute(runtimePath) || !isAbsolute(configPath)) stop('PROFILE_PATH_REQUIRED');
  return { ...profile, runtimePath, configPath };
}
