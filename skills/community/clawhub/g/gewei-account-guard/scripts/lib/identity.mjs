import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = path.resolve(__dirname, '..', '..');
const PACKAGE_PATH = path.join(SKILL_ROOT, 'package.json');
const CONFIG_PATH = path.join(SKILL_ROOT, 'config', 'posthog.json');

function readJson(file) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch {
    return null;
  }
}

function normalizeId(value, fallback) {
  const id = String(value || '').trim().toLowerCase();
  return /^[a-z0-9][a-z0-9_-]{0,63}$/.test(id) ? id : fallback;
}

function normalizeName(value, fallback) {
  const name = String(value || '').trim();
  return name ? name.slice(0, 120) : fallback;
}

const pkg = readJson(PACKAGE_PATH) || {};
const config = readJson(CONFIG_PATH) || {};
const matrix = pkg.matrix || {};
const configTrackId = normalizeId(config.trackId || matrix.track_id, 'zhini-skill-matrix');
const packagePluginId = normalizeId(pkg.name, 'unknown-plugin');

export const TRACK_ID = normalizeId(
  process.env.MATRIX_TRACK_ID || configTrackId,
  configTrackId,
);
export const PLUGIN_ID = normalizeId(
  process.env.MATRIX_PLUGIN_ID || matrix.plugin_id || packagePluginId,
  packagePluginId,
);
export const PLUGIN_NAME = normalizeName(matrix.plugin_name, PLUGIN_ID);
export const SKILL_ID = normalizeId(
  process.env.MATRIX_SKILL_ID || matrix.skill_id || PLUGIN_ID,
  PLUGIN_ID,
);
export const SKILL_NAME = normalizeName(matrix.skill_name, PLUGIN_NAME);
export const SKILL_VERSION = typeof pkg.version === 'string' ? pkg.version : '0.0.0';
export const SCHEMA_VERSION = 3;

export const EVENT_NAMES = Object.freeze({
  loaded: 'matrix_skill_loaded',
  completed: 'matrix_skill_completed',
  referralShown: 'matrix_referral_shown',
});

export const ALLOWED_EVENTS = new Set(Object.values(EVENT_NAMES));
