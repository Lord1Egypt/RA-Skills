import { readFileSync } from 'fs';
import { join } from 'path';
import yaml from 'js-yaml';

/**
 * Parse a .env file into a plain object.
 * Skips blank lines and lines starting with #.
 * Strips surrounding single/double quotes from values.
 */
function parseEnv(content) {
  const result = {};
  for (const raw of content.split('\n')) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    const eqIndex = line.indexOf('=');
    if (eqIndex === -1) continue;
    const key = line.slice(0, eqIndex).trim();
    let value = line.slice(eqIndex + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    if (key) result[key] = value;
  }
  return result;
}

/**
 * Load config from configDir (defaults to ~/.aurehub).
 * Reads .env and hyperliquid.yaml; missing files are silently ignored.
 *
 * @param {string} [configDir]
 * @returns {{ env: object, yaml: object, configDir: string }}
 */
export function loadConfig(configDir) {
  const dir = configDir ?? join(
    process.env.HOME ?? process.env.USERPROFILE ?? '',
    '.aurehub'
  );

  let env = {};
  try {
    env = parseEnv(readFileSync(join(dir, '.env'), 'utf8'));
  } catch (err) {
    if (err.code !== 'ENOENT') throw err;
  }

  let yamlConfig = {};
  try {
    yamlConfig = yaml.load(
      readFileSync(join(dir, 'hyperliquid.yaml'), 'utf8'),
      { schema: yaml.JSON_SCHEMA }
    ) ?? {};
  } catch (err) {
    if (err.code !== 'ENOENT') throw err;
  }

  return { env, yaml: yamlConfig, configDir: dir };
}
