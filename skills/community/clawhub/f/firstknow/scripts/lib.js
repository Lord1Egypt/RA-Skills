/**
 * Shared utilities for FirstKnow skill scripts.
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

export const DATA_DIR = join(homedir(), '.firstknow');
export const CONFIG_PATH = join(DATA_DIR, 'config.json');
export const PORTFOLIO_PATH = join(DATA_DIR, 'portfolio.json');
export const ENV_PATH = join(DATA_DIR, '.env');

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
export const SKILL_DIR = dirname(__dirname);

export const DEFAULT_API_BASE = 'https://firstknow-backend.yuchen-9cf.workers.dev';

export function ensureDataDir() {
  if (!existsSync(DATA_DIR)) {
    mkdirSync(DATA_DIR, { recursive: true });
  }
}

export function loadConfig() {
  if (!existsSync(CONFIG_PATH)) return null;
  return JSON.parse(readFileSync(CONFIG_PATH, 'utf-8'));
}

export function saveConfig(config) {
  ensureDataDir();
  writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2) + '\n');
}

export function loadPortfolio() {
  if (!existsSync(PORTFOLIO_PATH)) return null;
  return JSON.parse(readFileSync(PORTFOLIO_PATH, 'utf-8'));
}

export function savePortfolio(portfolio) {
  ensureDataDir();
  writeFileSync(PORTFOLIO_PATH, JSON.stringify(portfolio, null, 2) + '\n');
}

export function getApiBase() {
  const config = loadConfig();
  return config?.api_base_url || DEFAULT_API_BASE;
}

export function getChatId() {
  const config = loadConfig();
  return config?.delivery?.chatId || null;
}

export function getBotToken() {
  const config = loadConfig();
  return config?.delivery?.botToken || null;
}

export function log(context, message) {
  console.error(`[${new Date().toISOString()}] [${context}] ${message}`);
}

export async function apiCall(method, path, body = null) {
  const base = getApiBase();
  const url = `${base}${path}`;
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (body) opts.body = JSON.stringify(body);

  const resp = await fetch(url, opts);
  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`API ${method} ${path} returned ${resp.status}: ${text}`);
  }
  return resp.json();
}
