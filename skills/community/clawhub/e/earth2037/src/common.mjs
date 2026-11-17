import { readFileSync, statSync } from 'node:fs';
import { homedir } from 'node:os';
import { resolve } from 'node:path';
import { format } from 'node:util';

export class GatewayError extends Error {
  constructor(code, message, details = {}) { super(message); this.code = code; this.details = details; }
}
export function requireValue(value, code, message) { if (!value) throw new GatewayError(code, message); return value; }
export function checkUrl(value, protocol, allowLocal = false) {
  let url; try { url = new URL(value); } catch { throw new GatewayError('invalid_url', 'Invalid service URL'); }
  const local = ['localhost', '127.0.0.1', '[::1]'].includes(url.hostname);
  if (url.username || url.password || url.hash || !(url.protocol === protocol || (allowLocal && local && url.protocol === (protocol === 'https:' ? 'http:' : 'ws:'))))
    throw new GatewayError('insecure_url', format('Expected %s URL (loopback testing is opt-in)', String(protocol)));
  return url;
}
export function loadConfig(env = process.env) {
  // Only player-configured credentials are read: a private JSON file or the
  // named EARTH2037_* variables below. They authenticate to Account Center;
  // never log their values or include them in MCP results or action receipts.
  let secret = {};
  if (env.EARTH2037_CREDENTIAL_FILE) {
    const path = resolve(env.EARTH2037_CREDENTIAL_FILE);
    if (process.platform !== 'win32' && (statSync(path).mode & 0o077)) throw new GatewayError('credential_permissions', 'Credential file must be private (chmod 600)');
    secret = JSON.parse(readFileSync(path, 'utf8'));
  }
  return {
    accountUrl: env.EARTH2037_ACCOUNT_URL || 'https://new2037.earth2037.com/account-api',
    credentialFile: env.EARTH2037_CREDENTIAL_FILE ? resolve(env.EARTH2037_CREDENTIAL_FILE) : null,
    username: secret.username || env.EARTH2037_USERNAME,
    password: secret.password || env.EARTH2037_PASSWORD,
    newPassword: secret.new_password || env.EARTH2037_NEW_PASSWORD,
    accessToken: secret.access_token || env.EARTH2037_ACCESS_TOKEN,
    refreshToken: secret.refresh_token || env.EARTH2037_REFRESH_TOKEN,
    deviceId: secret.device_id || env.EARTH2037_DEVICE_ID || 'earth2037-agent-gateway',
    channel: secret.distribution_channel || env.EARTH2037_CHANNEL || 'direct',
    runtimePlatform: env.EARTH2037_RUNTIME_PLATFORM || (process.platform === 'darwin' ? 'macos' : process.platform === 'win32' ? 'windows' : 'web'),
    locale: env.EARTH2037_LOCALE || 'zh-CN',
    allowLocal: env.EARTH2037_ALLOW_LOOPBACK === '1',
    readOnly: env.EARTH2037_READ_ONLY !== '0',
    timeoutMs: 20000,
    stateDir: resolve(env.EARTH2037_STATE_DIR || resolve(homedir(), '.local/state/earth2037-agent')),
  };
}
export function redact(value) {
  if (Array.isArray(value)) return value.map(redact);
  if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([k,v]) =>
    [k, /^(?:(?:current_|new_)?password|pwd|md5pwd|loginKey|access_?token|refresh_?token|entry_?ticket|ticket|credential|client_secret|api_?key)$/i.test(k) ? '[redacted]' : redact(v)]));
  return value;
}
