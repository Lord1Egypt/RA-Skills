#!/usr/bin/env node
import { asBool, parseArgs } from '../lib/args.mjs';
import {
  loadConfig,
  normalizeAuthMode,
  readPassword,
  resolveConfigPath,
} from '../lib/config.mjs';
import { ewsGet } from '../lib/ews-client.mjs';

try {
  const args = parseArgs();

  const configPath = resolveConfigPath(args.configPath || process.env.EXCHANGE_CONFIG_PATH);
  const cfg = loadConfig(configPath);

  const masterKey = args.masterKey || process.env.EXCHANGE_SKILL_MASTER_KEY;
  const passwordOverride = args.password || process.env.EXCHANGE_PASSWORD;
  const password = readPassword({
    cfg,
    masterKey,
    passwordOverride,
  });

  const authMode = normalizeAuthMode(
    args.authMode || process.env.EXCHANGE_AUTH_MODE || cfg.auth_mode
  );
  const insecure = asBool(args.insecure ?? process.env.EXCHANGE_INSECURE);
  const domain = args.domain || process.env.EXCHANGE_DOMAIN || cfg.domain;

  const resp = await ewsGet({
    url: cfg.exchange_url,
    username: cfg.username,
    password,
    authMode,
    domain,
    insecure,
  });

  console.log(
    JSON.stringify(
      {
        ok: true,
        http_status: resp.status,
        username: cfg.username,
        domain: domain || '',
        exchange_url: cfg.exchange_url,
        auth_mode: authMode,
      },
      null,
      2
    )
  );
} catch (err) {
  console.error('verify-login failed:', err.message);
  process.exit(1);
}
