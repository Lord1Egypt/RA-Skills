import fs from 'node:fs';
import path from 'node:path';
import { decryptSecret, encryptSecret } from './crypto-store.mjs';

function stripBom(text) {
  if (typeof text !== 'string') {
    return '';
  }
  return text.charCodeAt(0) === 0xfeff ? text.slice(1) : text;
}

export function resolveConfigPath(inputPath) {
  if (!inputPath) {
    return path.resolve(process.cwd(), 'config/exchange.config.json');
  }
  return path.resolve(process.cwd(), inputPath);
}

export function loadConfig(configPath) {
  if (!fs.existsSync(configPath)) {
    throw new Error(`Config file not found: ${configPath}`);
  }

  const raw = stripBom(fs.readFileSync(configPath, 'utf8'));
  let cfg;
  try {
    cfg = JSON.parse(raw);
  } catch (err) {
    throw new Error(`Invalid JSON config: ${configPath}. ${err.message}`);
  }

  if (!cfg.exchange_url || !cfg.username) {
    throw new Error('Invalid config: exchange_url and username are required');
  }

  return cfg;
}

export function saveConfig(configPath, cfg) {
  const dir = path.dirname(configPath);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(configPath, `${JSON.stringify(cfg, null, 2)}\n`, 'utf8');
}

export function normalizeAuthMode(authMode) {
  const mode = String(authMode || 'ntlm').trim().toLowerCase();
  if (mode === 'default') {
    return 'ntlm';
  }
  if (mode === 'ntlm' || mode === 'basic') {
    return mode;
  }
  throw new Error(`Unsupported auth_mode: ${authMode}. Use ntlm or basic.`);
}

export function buildConfig({
  exchangeUrl,
  username,
  authMode,
  password,
  masterKey,
  domain,
}) {
  const mode = normalizeAuthMode(authMode);
  const secret_store = encryptSecret(password, masterKey);
  const trimmedDomain = domain ? String(domain).trim() : '';

  return {
    schema_version: 2,
    exchange_url: String(exchangeUrl).trim(),
    username: String(username).trim(),
    ...(trimmedDomain ? { domain: trimmedDomain } : {}),
    auth_mode: mode,
    secret_store,
    created_at_utc: new Date().toISOString(),
  };
}

export function readPassword({ cfg, masterKey, passwordOverride }) {
  if (passwordOverride) {
    return String(passwordOverride);
  }

  if (cfg.secret_store) {
    return decryptSecret(cfg.secret_store, masterKey);
  }

  if (cfg.password) {
    return String(cfg.password);
  }

  throw new Error('No decryptable password found in config');
}

export function maskConfig(cfg) {
  return {
    exchange_url: cfg.exchange_url,
    username: cfg.username,
    domain: cfg.domain || '',
    auth_mode: cfg.auth_mode,
    schema_version: cfg.schema_version || 1,
    created_at_utc: cfg.created_at_utc,
  };
}
