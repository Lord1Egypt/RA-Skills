import { readFileSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
import yaml from 'js-yaml';

function parseEnv(content) {
  const result = {};
  for (const raw of content.split('\n')) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    const eq = line.indexOf('=');
    if (eq === -1) continue;
    const key = line.slice(0, eq).trim();
    let val = line.slice(eq + 1).trim();
    if ((val.startsWith('"') && val.endsWith('"')) ||
        (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    if (key) result[key] = val;
  }
  return result;
}

export function loadConfig(configDir) {
  const dir = configDir ?? join(homedir(), '.aurehub');
  let env = {};
  try { env = parseEnv(readFileSync(join(dir, '.env'), 'utf8')); }
  catch (e) { if (e.code !== 'ENOENT') throw e; }
  let cfg = {};
  try { cfg = yaml.load(readFileSync(join(dir, 'polymarket.yaml'), 'utf8')) ?? {}; }
  catch (e) { if (e.code !== 'ENOENT') throw e; }
  return { env, yaml: cfg, configDir: dir };
}

export function resolveRpcUrl(cfg) {
  const name = cfg.yaml?.rpc_env;
  if (!name) throw new Error(
    `rpc_env not set in ~/.aurehub/polymarket.yaml.\n` +
    `Add: rpc_env: POLYGON_RPC_URL\n` +
    `(rpc_env names the env variable that holds your Polygon RPC URL.)`,
  );
  const url = cfg.env[name] ?? process.env[name];
  if (!url) throw new Error(
    `${name} not set in ~/.aurehub/.env (referenced by rpc_env in polymarket.yaml).\n` +
    `Add: ${name}=https://polygon.drpc.org`,
  );
  return url;
}
