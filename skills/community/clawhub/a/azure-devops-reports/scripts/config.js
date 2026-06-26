const fs = require('fs');
const path = require('path');

const SKILL_DIR = path.resolve(__dirname, '..');
const ENV_PATH = path.join(SKILL_DIR, '.env');
const DEFAULT_OUTPUT_DIR = path.join(SKILL_DIR, 'output');

function parseEnvFile(filePath) {
  if (!fs.existsSync(filePath)) return {};
  const text = fs.readFileSync(filePath, 'utf8');
  const env = {};
  for (const rawLine of text.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) continue;
    const idx = line.indexOf('=');
    if (idx === -1) continue;
    const key = line.slice(0, idx).trim();
    let value = line.slice(idx + 1).trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    env[key] = value;
  }
  return env;
}

function resolveOutputDir(requestedOutputDir) {
  if (!requestedOutputDir) return DEFAULT_OUTPUT_DIR;
  const resolved = path.resolve(SKILL_DIR, requestedOutputDir);
  const relative = path.relative(SKILL_DIR, resolved);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    throw new Error('AZURE_DEVOPS_OUTPUT_DIR must stay within the skill directory');
  }
  return resolved;
}

function loadConfig() {
  const env = parseEnvFile(ENV_PATH);

  const config = {
    skillDir: SKILL_DIR,
    envPath: ENV_PATH,
    org: env.AZURE_DEVOPS_ORG || '',
    pat: env.AZURE_DEVOPS_PAT || '',
    defaultProject: env.AZURE_DEVOPS_DEFAULT_PROJECT || '',
    defaultTeam: env.AZURE_DEVOPS_DEFAULT_TEAM || '',
    defaultQueryId: env.AZURE_DEVOPS_DEFAULT_QUERY_ID || '',
    outputDir: resolveOutputDir(env.AZURE_DEVOPS_OUTPUT_DIR || ''),
  };

  fs.mkdirSync(config.outputDir, { recursive: true });
  return config;
}

module.exports = { loadConfig, ENV_PATH, SKILL_DIR, DEFAULT_OUTPUT_DIR };
