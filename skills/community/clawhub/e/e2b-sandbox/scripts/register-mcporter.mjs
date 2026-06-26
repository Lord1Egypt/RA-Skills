#!/usr/bin/env node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SKILL_DIR = path.resolve(__dirname, '..');
const SERVER_PATH = path.join(SKILL_DIR, 'scripts', 'e2b-mcp-server.mjs');
const PACKAGE_JSON = path.join(SKILL_DIR, 'package.json');
const PACKAGE_LOCK = path.join(SKILL_DIR, 'package-lock.json');

const CONFIG_PATH = path.join(os.homedir(), '.openclaw', 'workspace', 'config', 'mcporter.json');
const SERVER_NAME = 'e2b-sandbox';

function ensureParent(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function readConfig() {
  try {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  } catch {
    return { mcpServers: {}, imports: [] };
  }
}

function writeConfig(config) {
  ensureParent(CONFIG_PATH);
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
}

const config = readConfig();
config.mcpServers ||= {};
config.imports ||= [];
config.mcpServers[SERVER_NAME] = {
  command: `node ${SERVER_PATH}`,
  env: {
    E2B_API_KEY: '${E2B_API_KEY}'
  }
};
writeConfig(config);

console.log(JSON.stringify({
  ok: true,
  serverName: SERVER_NAME,
  configPath: CONFIG_PATH,
  command: config.mcpServers[SERVER_NAME].command,
  files: [PACKAGE_JSON, PACKAGE_LOCK, SERVER_PATH]
}, null, 2));
