import { asBool } from './args.mjs';
import {
  loadConfig,
  normalizeAuthMode,
  readPassword,
  resolveConfigPath,
} from './config.mjs';

export function loadConnectionFromArgs(args) {
  const configPath = resolveConfigPath(args.configPath || process.env.EXCHANGE_CONFIG_PATH);
  const cfg = loadConfig(configPath);

  const masterKey = args.masterKey || process.env.EXCHANGE_SKILL_MASTER_KEY;
  const password = readPassword({
    cfg,
    masterKey,
    passwordOverride: args.password || process.env.EXCHANGE_PASSWORD,
  });

  return {
    configPath,
    cfg,
    url: cfg.exchange_url,
    username: cfg.username,
    password,
    authMode: normalizeAuthMode(args.authMode || process.env.EXCHANGE_AUTH_MODE || cfg.auth_mode),
    domain: args.domain || process.env.EXCHANGE_DOMAIN || cfg.domain,
    insecure: asBool(args.insecure ?? process.env.EXCHANGE_INSECURE),
    serverVersion: args.serverVersion || process.env.EXCHANGE_SERVER_VERSION || 'Exchange2013_SP1',
  };
}
