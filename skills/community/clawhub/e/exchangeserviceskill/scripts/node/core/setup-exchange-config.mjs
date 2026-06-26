#!/usr/bin/env node
import { parseArgs } from '../lib/args.mjs';
import {
  buildConfig,
  maskConfig,
  resolveConfigPath,
  saveConfig,
} from '../lib/config.mjs';

function usage() {
  console.error([
    'Usage:',
    '  node ./scripts/node/setup-exchange-config.mjs \\',
    '    --exchange-url https://mail.example.com/EWS/Exchange.asmx \\',
    '    --username DOMAIN\\\\user \\',
    '    [--domain DOMAIN] \\',
    '    --auth-mode ntlm \\',
    '    --password <password> \\',
    '    --master-key <masterKey> \\',
    '    [--config-path config/exchange.config.json]',
    '',
    'Env fallback:',
    '  EXCHANGE_URL, EXCHANGE_USERNAME, EXCHANGE_DOMAIN, EXCHANGE_AUTH_MODE, EXCHANGE_PASSWORD, EXCHANGE_SKILL_MASTER_KEY, EXCHANGE_CONFIG_PATH',
  ].join('\n'));
}

try {
  const args = parseArgs();

  const exchangeUrl = args.exchangeUrl || process.env.EXCHANGE_URL;
  const username = args.username || process.env.EXCHANGE_USERNAME;
  const domain = args.domain || process.env.EXCHANGE_DOMAIN;
  const authMode = args.authMode || process.env.EXCHANGE_AUTH_MODE || 'ntlm';
  const password = args.password || process.env.EXCHANGE_PASSWORD;
  const masterKey = args.masterKey || process.env.EXCHANGE_SKILL_MASTER_KEY;
  const configPath = resolveConfigPath(args.configPath || process.env.EXCHANGE_CONFIG_PATH);

  if (!exchangeUrl || !username || !password || !masterKey) {
    usage();
    process.exit(1);
  }

  const cfg = buildConfig({
    exchangeUrl,
    username,
    domain,
    authMode,
    password,
    masterKey,
  });

  saveConfig(configPath, cfg);

  console.log('Config saved:', configPath);
  console.log(JSON.stringify(maskConfig(cfg), null, 2));
  console.log('Password is encrypted with AES-256-GCM (master key required to decrypt).');
} catch (err) {
  console.error('setup-config failed:', err.message);
  process.exit(1);
}
