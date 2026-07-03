'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');

const MANAGED_BY = 'evomap-proxy';
const REUSABLE_PROXY_TOKEN_RE = /^[a-f0-9]{64}$/i;

function getHomeDir(env = process.env) {
  const home = String(env.HOME || os.homedir() || '').trim();
  return home || null;
}

function normalizeSettingsPath(value, home) {
  const raw = String(value || '').trim();
  if (!raw) return null;
  if (home && raw === '~') return path.resolve(home);
  if (home && raw.startsWith('~/')) return path.resolve(home, raw.slice(2));
  return path.resolve(raw);
}

function samePath(a, b) {
  if (!a || !b) return false;
  const left = path.resolve(a);
  const right = path.resolve(b);
  return process.platform === 'win32'
    ? left.toLowerCase() === right.toLowerCase()
    : left === right;
}

function getEnvClaudeSettingsFile(env = process.env) {
  return String(env.CLAUDE_SETTINGS_FILE || env.EVOMAP_CLAUDE_SETTINGS_FILE || '').trim();
}

function isValidReusableProxyToken(value) {
  return typeof value === 'string' && REUSABLE_PROXY_TOKEN_RE.test(value.trim());
}

function normalizeUrl(value) {
  return String(value || '').trim().replace(/\/+$/, '');
}

function parseUrl(value) {
  const raw = normalizeUrl(value);
  if (!raw) return null;
  try {
    return new URL(raw);
  } catch {
    return null;
  }
}

function isLoopbackProxyUrl(value) {
  const parsed = parseUrl(value);
  if (!parsed || parsed.protocol !== 'http:') return false;
  const host = parsed.hostname.toLowerCase();
  return host === '127.0.0.1' || host === 'localhost' || host === '[::1]' || host === '::1';
}

function safeUpstreamBaseUrl(value, opts = {}) {
  const baseUrl = normalizeUrl(value);
  if (!baseUrl) return '';
  if (baseUrl === normalizeUrl(opts.url)) return '';
  return baseUrl;
}

function safeUpstreamToken(value, proxyToken) {
  const token = typeof value === 'string' ? value.trim() : '';
  if (!token || token === proxyToken) return '';
  return token;
}

function getClaudeSettingsFile(env = process.env) {
  const home = getHomeDir(env);
  if (!home) return null;
  return path.join(home, '.claude', 'settings.json');
}

function resolveClaudeSettingsFile(opts = {}, env = process.env) {
  if (opts.file) {
    return { file: opts.file, source: 'opts' };
  }

  const defaultFile = getClaudeSettingsFile(env);
  if (!defaultFile) {
    return { file: null, reason: 'missing_settings_path' };
  }

  const envFile = getEnvClaudeSettingsFile(env);
  if (!envFile) {
    return { file: defaultFile, source: 'default' };
  }

  const home = getHomeDir(env);
  const envResolved = normalizeSettingsPath(envFile, home);
  const defaultResolved = normalizeSettingsPath(defaultFile, home);
  if (samePath(envResolved, defaultResolved)) {
    return { file: defaultFile, source: 'env_default' };
  }

  return { file: null, reason: 'unsafe_settings_path' };
}

function readJsonFile(file) {
  const result = readJsonFileResult(file);
  return result.ok ? result.value : null;
}

function readJsonFileResult(file) {
  try {
    if (!file || !fs.existsSync(file)) {
      return { exists: false, ok: true, value: null };
    }
    return { exists: true, ok: true, value: JSON.parse(fs.readFileSync(file, 'utf8')) };
  } catch (err) {
    return { exists: Boolean(file), ok: false, value: null, error: err };
  }
}

function writePrivateJsonFile(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(data, null, 2) + '\n', { encoding: 'utf8', mode: 0o600 });
  try { fs.chmodSync(file, 0o600); } catch { /* best-effort on Windows */ }
}

function isDisabled(env = process.env) {
  const raw = String(env.EVOMAP_PROXY_AUTO_INJECT || '').trim().toLowerCase();
  return raw === '0' || raw === 'false' || raw === 'off' || raw === 'none' || raw === 'no';
}

function hasManagedProxyMarker(settings) {
  return settings && settings._evomap_proxy_client_env?.managed_by === MANAGED_BY;
}

function isManagedProxyBaseUrl(settings, cfg, value, opts = {}) {
  const baseUrl = normalizeUrl(value);
  if (!isLoopbackProxyUrl(baseUrl)) return false;
  if (baseUrl === normalizeUrl(opts.url)) return true;
  if (hasManagedProxyMarker(settings)) return true;
  if (String(cfg && cfg.EVOMAP_PROXY_AUTO_INJECTED || '') === '1') return true;

  const proxyUrl = normalizeUrl(cfg && cfg.EVOMAP_PROXY_URL);
  return Boolean(proxyUrl && isLoopbackProxyUrl(proxyUrl) && proxyUrl === baseUrl);
}

function isManagedProxyClientSettings(settings, cfg, opts = {}) {
  return isManagedProxyBaseUrl(settings, cfg, cfg && cfg.ANTHROPIC_BASE_URL, opts);
}

function isManagedProxyUpstreamResidual(settings, cfg, baseValue, tokenValue, apiKeyValue) {
  const baseUrl = normalizeUrl(baseValue);
  const token = typeof tokenValue === 'string' ? tokenValue.trim() : '';
  const apiKey = typeof apiKeyValue === 'string' ? apiKeyValue.trim() : '';
  if (!isLoopbackProxyUrl(baseUrl)
    || (!isValidReusableProxyToken(token) && !isValidReusableProxyToken(apiKey))) {
    return false;
  }
  return hasManagedProxyMarker(settings) || String(cfg && cfg.EVOMAP_PROXY_AUTO_INJECTED || '') === '1';
}

function safeStoredUpstreamBaseUrl(settings, cfg, value, opts = {}) {
  const baseUrl = normalizeUrl(value);
  if (!baseUrl) return '';
  if (baseUrl === normalizeUrl(opts.url)) return '';
  const proxyUrl = normalizeUrl(cfg && cfg.EVOMAP_PROXY_URL);
  if (proxyUrl && baseUrl === proxyUrl) return '';
  if (baseUrl === normalizeUrl(cfg && cfg.ANTHROPIC_BASE_URL)
    && isManagedProxyBaseUrl(settings, cfg, cfg && cfg.ANTHROPIC_BASE_URL, opts)) {
    return '';
  }
  return safeUpstreamBaseUrl(value, opts);
}

function readReusableClientProxyToken(opts = {}) {
  const env = opts.env || process.env;
  if (isDisabled(env)) return null;

  const resolved = resolveClaudeSettingsFile(opts, env);
  const file = resolved.file;
  if (!file) return null;
  const settings = readJsonFile(file);
  const cfg = settings && settings.env;
  if (!cfg || typeof cfg !== 'object') return null;

  const baseUrl = normalizeUrl(cfg.ANTHROPIC_BASE_URL);
  const token = typeof cfg.ANTHROPIC_AUTH_TOKEN === 'string'
    ? cfg.ANTHROPIC_AUTH_TOKEN.trim()
    : '';
  if (!isValidReusableProxyToken(token)
    || !isManagedProxyClientSettings(settings, cfg, opts)
    || !isLoopbackProxyUrl(baseUrl)) {
    return null;
  }
  return token;
}

function backupExistingFile(file) {
  try {
    if (!file || !fs.existsSync(file)) return null;
    const stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d{3}Z$/, 'Z');
    const backupDir = path.join(path.dirname(file), 'backups');
    fs.mkdirSync(backupDir, { recursive: true });
    for (let i = 0; i < 10; i++) {
      const suffix = i === 0 ? '' : `-${i}`;
      const backupFile = path.join(backupDir, `settings.json.pre-evomap-proxy-sync-${stamp}${suffix}`);
      try {
        fs.copyFileSync(file, backupFile, fs.constants.COPYFILE_EXCL);
        try { fs.chmodSync(backupFile, 0o600); } catch { /* best-effort */ }
        return backupFile;
      } catch (err) {
        if (!err || err.code !== 'EEXIST') return null;
      }
    }
    return null;
  } catch {
    return null;
  }
}

function syncClaudeProxySettings(info = {}) {
  const env = info.env || process.env;
  if (isDisabled(env)) {
    return { synced: false, reason: 'disabled' };
  }

  const url = normalizeUrl(info.url);
  const token = typeof info.token === 'string' ? info.token.trim() : '';
  if (!url || !isValidReusableProxyToken(token)) {
    return { synced: false, reason: 'missing_proxy_settings' };
  }

  const resolved = resolveClaudeSettingsFile(info, env);
  const file = resolved.file;
  if (!file) {
    return { synced: false, changed: false, reason: resolved.reason || 'missing_settings_path' };
  }

  const currentResult = readJsonFileResult(file);
  if (currentResult.exists && !currentResult.ok) {
    const backupFile = info.backup === false ? null : backupExistingFile(file);
    return {
      synced: false,
      changed: false,
      reason: 'invalid_settings_json',
      file,
      backupFile,
    };
  }
  const current = currentResult.value;
  const settings = current && typeof current === 'object' && !Array.isArray(current)
    ? current
    : {};
  const cfg = settings.env && typeof settings.env === 'object' && !Array.isArray(settings.env)
    ? { ...settings.env }
    : {};

  const existingBase = normalizeUrl(cfg.ANTHROPIC_BASE_URL);
  const existingToken = typeof cfg.ANTHROPIC_AUTH_TOKEN === 'string'
    ? cfg.ANTHROPIC_AUTH_TOKEN.trim()
    : '';
  const existingApiKey = typeof cfg.ANTHROPIC_API_KEY === 'string'
    ? cfg.ANTHROPIC_API_KEY.trim()
    : '';
  const existingStoredUpstreamBase = normalizeUrl(cfg.EVOMAP_ANTHROPIC_BASE_URL);
  const existingStoredUpstreamAuthToken = typeof cfg.EVOMAP_ANTHROPIC_AUTH_TOKEN === 'string'
    ? cfg.EVOMAP_ANTHROPIC_AUTH_TOKEN.trim()
    : '';
  const existingUpstreamApiKey = typeof cfg.EVOMAP_ANTHROPIC_API_KEY === 'string'
    ? cfg.EVOMAP_ANTHROPIC_API_KEY.trim()
    : '';
  const existingBaseIsProxy = isManagedProxyBaseUrl(settings, cfg, existingBase, info);
  const runtimeEnv = info.runtimeEnv && typeof info.runtimeEnv === 'object'
    ? info.runtimeEnv
    : null;

  let changed = false;
  let runtimeChanged = false;
  let runtimeUpstreamChanged = false;
  const setIfChanged = (key, value) => {
    if (cfg[key] === value) return;
    cfg[key] = value;
    changed = true;
  };
  const deleteIfPresent = (key) => {
    if (!Object.prototype.hasOwnProperty.call(cfg, key)) return;
    delete cfg[key];
    changed = true;
  };
  const setRuntimeIfMissing = (key, value) => {
    if (!runtimeEnv || !value) return false;
    if (String(runtimeEnv[key] || '').trim()) return false;
    runtimeEnv[key] = value;
    runtimeChanged = true;
    runtimeUpstreamChanged = true;
    return true;
  };
  const setRuntimeAutoInjected = () => {
    if (!runtimeEnv || !runtimeUpstreamChanged || runtimeEnv.EVOMAP_PROXY_AUTO_INJECTED === '1') return;
    runtimeEnv.EVOMAP_PROXY_AUTO_INJECTED = '1';
    runtimeChanged = true;
  };
  const setRuntimeUpstreamApiKey = (value) => {
    const upstreamApiKey = safeUpstreamToken(value, token);
    if (!upstreamApiKey || upstreamApiKey === existingToken) return;
    setRuntimeIfMissing('EVOMAP_ANTHROPIC_API_KEY', upstreamApiKey);
  };

  if (isManagedProxyUpstreamResidual(
    settings,
    cfg,
    existingStoredUpstreamBase,
    existingStoredUpstreamAuthToken,
    existingUpstreamApiKey
  )) {
    deleteIfPresent('EVOMAP_ANTHROPIC_BASE_URL');
    deleteIfPresent('EVOMAP_ANTHROPIC_AUTH_TOKEN');
    deleteIfPresent('EVOMAP_ANTHROPIC_API_KEY');
  }

  const migratedBaseUrl = existingBaseIsProxy ? '' : safeUpstreamBaseUrl(existingBase, info);
  if (migratedBaseUrl && !existingBaseIsProxy && !cfg.EVOMAP_ANTHROPIC_BASE_URL) {
    setIfChanged('EVOMAP_ANTHROPIC_BASE_URL', migratedBaseUrl);
  }
  const migratedAuthToken = existingBaseIsProxy ? '' : safeUpstreamToken(existingToken, token);
  if (migratedAuthToken && !cfg.EVOMAP_ANTHROPIC_AUTH_TOKEN) {
    setIfChanged('EVOMAP_ANTHROPIC_AUTH_TOKEN', migratedAuthToken);
  }
  if (existingApiKey && existingApiKey !== token && existingApiKey !== existingToken && !cfg.EVOMAP_ANTHROPIC_API_KEY) {
    setIfChanged('EVOMAP_ANTHROPIC_API_KEY', existingApiKey);
  }
  const runtimeHadUpstreamBase = Boolean(runtimeEnv && String(runtimeEnv.EVOMAP_ANTHROPIC_BASE_URL || '').trim());
  const runtimeBaseSyncedFromSettings = setRuntimeIfMissing(
    'EVOMAP_ANTHROPIC_BASE_URL',
    safeStoredUpstreamBaseUrl(settings, cfg, cfg.EVOMAP_ANTHROPIC_BASE_URL, info)
  );
  const canSyncSettingsCredentialToRuntime = !runtimeHadUpstreamBase || runtimeBaseSyncedFromSettings;
  if (canSyncSettingsCredentialToRuntime) {
    const upstreamAuthToken = safeUpstreamToken(cfg.EVOMAP_ANTHROPIC_AUTH_TOKEN, token);
    if (!(existingBaseIsProxy && upstreamAuthToken === existingToken)) {
      setRuntimeIfMissing('EVOMAP_ANTHROPIC_AUTH_TOKEN', upstreamAuthToken);
    }
    setRuntimeUpstreamApiKey(cfg.EVOMAP_ANTHROPIC_API_KEY);
  }
  setRuntimeAutoInjected();

  setIfChanged('ANTHROPIC_BASE_URL', url);
  setIfChanged('ANTHROPIC_AUTH_TOKEN', token);
  deleteIfPresent('ANTHROPIC_API_KEY');
  setIfChanged('CUSTOM_API_KEY', token);
  setIfChanged('EVOMAP_PROXY_URL', url);
  setIfChanged('EVOMAP_PROXY_AUTO_INJECTED', '1');

  const marker = settings._evomap_proxy_client_env || {};
  if (marker.managed_by !== MANAGED_BY) {
    settings._evomap_proxy_client_env = { managed_by: MANAGED_BY };
    changed = true;
  }

  if (!changed) {
    return {
      synced: true,
      changed: false,
      runtimeChanged,
      file,
      vars: [
        'ANTHROPIC_BASE_URL',
        'ANTHROPIC_AUTH_TOKEN',
        'CUSTOM_API_KEY',
        'EVOMAP_PROXY_URL',
      ],
    };
  }

  settings.env = cfg;
  settings._evomap_proxy_client_env = {
    managed_by: MANAGED_BY,
    updated_at: new Date().toISOString(),
  };

  const backupFile = info.backup === false ? null : backupExistingFile(file);
  writePrivateJsonFile(file, settings);

  return {
    synced: true,
    changed: true,
    runtimeChanged,
    file,
    backupFile,
    vars: [
      'ANTHROPIC_BASE_URL',
      'ANTHROPIC_AUTH_TOKEN',
      'CUSTOM_API_KEY',
      'EVOMAP_PROXY_URL',
    ],
  };
}

module.exports = {
  getClaudeSettingsFile,
  isLoopbackProxyUrl,
  isValidReusableProxyToken,
  readReusableClientProxyToken,
  syncClaudeProxySettings,
};
