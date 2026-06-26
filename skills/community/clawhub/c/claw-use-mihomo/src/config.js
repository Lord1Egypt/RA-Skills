import { readFileSync, existsSync, mkdirSync, writeFileSync } from 'fs';
import { dirname, join } from 'path';
import { homedir } from 'os';

const DEFAULT_CONFIG_DIR = join(process.env.XDG_CONFIG_HOME || join(homedir(), '.config'), 'mihomod');
const DEFAULT_CONFIG_FILE = join(DEFAULT_CONFIG_DIR, 'config.json');

const DEFAULT_CONFIG = {
  mihomo: {
    api: 'http://127.0.0.1:9090',
    secret: '',
    configPath: join(homedir(), '.config', 'mihomo', 'config.yaml'),
    binaryPath: ''
  },
  watchdog: {
    endpoints: [
      { url: 'https://www.gstatic.com/generate_204', expect: 204 }
    ],
    checkInterval: 30,
    failThreshold: 2,
    cooldown: 60,
    maxDelay: 3000,
    nodePriority: ['US', '美国', 'SG', '新加坡', 'JP', '日本', 'HK', '香港']
  },
  selector: '🚀节点选择'
};

function deepMerge(target, source) {
  const result = { ...target };
  for (const key of Object.keys(source)) {
    if (
      source[key] !== null &&
      typeof source[key] === 'object' &&
      !Array.isArray(source[key]) &&
      typeof target[key] === 'object' &&
      !Array.isArray(target[key]) &&
      target[key] !== null
    ) {
      result[key] = deepMerge(target[key], source[key]);
    } else {
      result[key] = source[key];
    }
  }
  return result;
}

export function loadConfig(overridePath) {
  const configPath = overridePath || DEFAULT_CONFIG_FILE;
  if (!existsSync(configPath)) {
    mkdirSync(DEFAULT_CONFIG_DIR, { recursive: true });
    writeFileSync(configPath, JSON.stringify(DEFAULT_CONFIG, null, 2));
    return structuredClone(DEFAULT_CONFIG);
  }
  const raw = readFileSync(configPath, 'utf8');
  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch (e) {
    throw new Error(`Failed to parse config ${configPath}: ${e.message}`);
  }
  return deepMerge(DEFAULT_CONFIG, parsed);
}

export function saveConfig(config, overridePath) {
  const configPath = overridePath || DEFAULT_CONFIG_FILE;
  mkdirSync(dirname(configPath), { recursive: true });
  writeFileSync(configPath, JSON.stringify(config, null, 2));
}

export { DEFAULT_CONFIG_FILE };
