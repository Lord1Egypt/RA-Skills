import fs from 'fs';
import path from 'path';
import http from 'http';
import https from 'https';
import crypto from 'crypto';
import { fileURLToPath } from 'url';
import { stateDir } from './state-dir.mjs';
import {
  ALLOWED_EVENTS,
  EVENT_NAMES,
  PLUGIN_ID,
  PLUGIN_NAME,
  SCHEMA_VERSION,
  SKILL_ID,
  SKILL_NAME,
  SKILL_VERSION,
  TRACK_ID,
} from './identity.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = path.resolve(__dirname, '..', '..');
const CONFIG_PATH = process.env.MATRIX_CONFIG
  || path.join(SKILL_ROOT, 'config', 'posthog.json');

const DEFAULT_HOST = 'https://us.i.posthog.com';
const REQUEST_TIMEOUT_MS = 1800;
const LOOPBACK_HOSTS = new Set(['localhost', '127.0.0.1', '::1']);

function readJson(file) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch {
    return null;
  }
}

function isOptOutValue(value) {
  return ['0', 'false', 'off', 'no', 'disabled'].includes(String(value).trim().toLowerCase());
}

export function isTelemetryOptedOut() {
  if (isOptOutValue(process.env.MATRIX_TELEMETRY)) return true;
  if (isOptOutValue(process.env.GEWEI_TELEMETRY)) return true;
  const dnt = String(process.env.DO_NOT_TRACK || '').trim().toLowerCase();
  return dnt === '1' || dnt === 'true';
}

// 显式 opt-in：环境变量设为 1/true/on 等价于用户明确同意发送统计。
export function isTelemetryExplicitlyEnabled() {
  return ['1', 'true', 'on', 'yes', 'enabled'].includes(
    String(process.env.MATRIX_TELEMETRY || '').trim().toLowerCase(),
  ) || ['1', 'true', 'on', 'yes', 'enabled'].includes(
    String(process.env.GEWEI_TELEMETRY || '').trim().toLowerCase(),
  );
}

// 只允许 https 主机；http 仅放行本机回环地址（本地测试用），
// 其余 http 主机返回 null，事件不允许明文外发。
function normalizeHost(raw) {
  let host = String(raw || '').trim().replace(/\/+$/, '');
  if (!host) return DEFAULT_HOST;
  if (!/^https?:\/\//i.test(host)) host = `https://${host}`;
  let url;
  try {
    url = new URL(host);
  } catch {
    return null;
  }
  if (url.protocol !== 'https:' && url.protocol !== 'http:') return null;
  if (url.protocol === 'http:' && !LOOPBACK_HOSTS.has(url.hostname)) return null;
  if (/^https:\/\/(us\.posthog\.com|app\.posthog\.com)$/i.test(host)) return 'https://us.i.posthog.com';
  if (/^https:\/\/eu\.posthog\.com$/i.test(host)) return 'https://eu.i.posthog.com';
  return host;
}

function loadConfig() {
  const file = readJson(CONFIG_PATH) || {};
  const token = String(
    process.env.MATRIX_POSTHOG_KEY
      || process.env.GEWEI_POSTHOG_KEY
      || process.env.POSTHOG_PROJECT_TOKEN
      || file.projectToken
      || '',
  ).trim();
  const host = normalizeHost(
    process.env.MATRIX_POSTHOG_HOST
      || process.env.GEWEI_POSTHOG_HOST
      || process.env.POSTHOG_HOST
      || file.host
      || DEFAULT_HOST,
  );
  const tokenLooksReal = token.length >= 12 && !/^phc_(replace|your|placeholder|test)/i.test(token);
  const optedOut = isTelemetryOptedOut();
  const explicitlyEnabled = isTelemetryExplicitlyEnabled();
  const configEnabled = file.enabled === true;
  const reason = optedOut
    ? 'opted_out'
    : !tokenLooksReal
      ? 'not_configured'
      : !host
        ? 'insecure_host'
        : !(explicitlyEnabled || configEnabled)
          ? 'disabled_by_config'
          : null;
  const enabled = reason === null;
  return { enabled, token, host: host || '', configPath: CONFIG_PATH, reason };
}

export function normalizeChannel(value) {
  const channel = String(
    value || process.env.MATRIX_CHANNEL || process.env.GEWEI_CHANNEL || 'unknown',
  ).trim().toLowerCase();
  return /^[a-z0-9][a-z0-9_-]{0,39}$/.test(channel) ? channel : 'unknown';
}

export function normalizeSurface(value, fallback = 'agent-skill') {
  const surface = String(value || fallback).trim().toLowerCase();
  return /^[a-z0-9][a-z0-9_-]{0,39}$/.test(surface) ? surface : fallback;
}

export function normalizeAgent(value) {
  const agent = String(
    value || process.env.MATRIX_AGENT || process.env.GEWEI_AGENT || 'unknown',
  ).trim().toLowerCase();
  return /^[a-z0-9][a-z0-9_-]{0,39}$/.test(agent) ? agent : 'unknown';
}

function anonymousIdPath() {
  return path.join(stateDir(), 'posthog-id');
}

function randomId() {
  if (typeof crypto.randomUUID === 'function') return crypto.randomUUID();
  const bytes = crypto.randomBytes(16).toString('hex');
  return `${bytes.slice(0, 8)}-${bytes.slice(8, 12)}-${bytes.slice(12, 16)}-${bytes.slice(16, 20)}-${bytes.slice(20)}`;
}

// 从事件身份稳定派生 UUID：同一逻辑事件的重试（含超时后重试）复用同一个
// uuid，PostHog 侧据此幂等去重；不同事件即使其他字段相同也不会碰撞。
export function stableEventUuid(...parts) {
  const hash = crypto.createHash('sha256')
    .update(parts.join('\u0000'))
    .digest('hex')
    .slice(0, 32);
  return `${hash.slice(0, 8)}-${hash.slice(8, 12)}-${hash.slice(12, 16)}-${hash.slice(16, 20)}-${hash.slice(20)}`;
}

function readExistingAnonymousId() {
  try {
    const id = fs.readFileSync(anonymousIdPath(), 'utf8').trim();
    return /^anon_[0-9a-f-]{36}$/i.test(id) ? id : null;
  } catch {
    return null;
  }
}

let anonymousIdCache = null;

function readOrCreateAnonymousId() {
  if (anonymousIdCache) return anonymousIdCache;
  const file = anonymousIdPath();
  const existing = readExistingAnonymousId();
  if (existing) {
    anonymousIdCache = { id: existing, firstRun: false, file };
    return anonymousIdCache;
  }

  const id = `anon_${randomId()}`;
  try {
    fs.mkdirSync(stateDir(), { recursive: true, mode: 0o700 });
    fs.writeFileSync(file, `${id}\n`, { mode: 0o600 });
    try {
      fs.chmodSync(file, 0o600);
    } catch {
      // Windows 上可能不支持 chmod，忽略。
    }
    anonymousIdCache = { id, firstRun: true, file };
    return anonymousIdCache;
  } catch {
    anonymousIdCache = { id, firstRun: true, file: null };
    return anonymousIdCache;
  }
}

function safeValue(value) {
  if (Array.isArray(value)) {
    return value.slice(0, 8).map((item) => String(item).slice(0, 40));
  }
  if (typeof value === 'boolean' || typeof value === 'number') return value;
  if (value === null || value === undefined) return undefined;
  return String(value).slice(0, 120);
}

function safeProperties(properties) {
  const out = {};
  for (const [key, value] of Object.entries(properties || {})) {
    if (key.startsWith('$')) continue;
    if (!/^[a-z][a-z0-9_]{0,39}$/i.test(key)) continue;
    const safe = safeValue(value);
    if (safe !== undefined) out[key] = safe;
  }
  return out;
}

function postJson(url, payload) {
  return new Promise((resolve) => {
    let target;
    try {
      target = new URL(url);
    } catch {
      resolve({ ok: false, error: 'invalid_host' });
      return;
    }

    const transport = target.protocol === 'http:' ? http : https;
    const body = JSON.stringify(payload);
    let settled = false;
    const finish = (result) => {
      if (settled) return;
      settled = true;
      resolve(result);
    };

    let req;
    try {
      req = transport.request(target, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(body),
          'User-Agent': `${PLUGIN_ID}-skill/${SKILL_VERSION}`,
        },
        timeout: REQUEST_TIMEOUT_MS,
      }, (res) => {
        let text = '';
        res.setEncoding('utf8');
        res.on('data', (chunk) => {
          if (text.length < 4096) text += chunk;
        });
        res.on('end', () => {
          finish({
            ok: res.statusCode >= 200 && res.statusCode < 300,
            status: res.statusCode,
            body: text.slice(0, 500),
          });
        });
      });
    } catch {
      finish({ ok: false, error: 'request_failed' });
      return;
    }

    req.on('timeout', () => {
      req.destroy();
      finish({ ok: false, error: 'timeout' });
    });
    req.on('error', () => finish({ ok: false, error: 'network_error' }));
    req.write(body);
    req.end();
  });
}

export function getAnalyticsStatus() {
  const config = loadConfig();
  return {
    enabled: config.enabled,
    disabled_reason: config.reason,
    host: config.host,
    token_configured: Boolean(config.token),
    opted_out: isTelemetryOptedOut(),
    config_path: config.configPath,
    anonymous_id_present: Boolean(readExistingAnonymousId()),
    anonymous_id_file: anonymousIdPath(),
    track_id: TRACK_ID,
    plugin_id: PLUGIN_ID,
    plugin_name: PLUGIN_NAME,
    skill_id: SKILL_ID,
    skill_name: SKILL_NAME,
    skill_version: SKILL_VERSION,
    schema_version: SCHEMA_VERSION,
    events: EVENT_NAMES,
  };
}

export async function trackEvent(event, properties = {}, options = {}) {
  const config = loadConfig();
  if (!config.enabled) {
    return {
      ok: false,
      skipped: true,
      reason: config.reason || 'disabled',
    };
  }
  if (!ALLOWED_EVENTS.has(event)) {
    return { ok: false, skipped: true, reason: 'invalid_event' };
  }

  const identity = readOrCreateAnonymousId();
  const runId = String(options.runId || '').trim().toLowerCase();
  const eventUuid = String(options.eventUuid || '').trim().toLowerCase();
  const payloadProperties = {
    ...safeProperties(properties),
    schema_version: SCHEMA_VERSION,
    track_id: TRACK_ID,
    plugin_id: PLUGIN_ID,
    plugin_name: PLUGIN_NAME,
    skill_id: SKILL_ID,
    skill_name: SKILL_NAME,
    skill_version: SKILL_VERSION,
    channel: normalizeChannel(options.channel),
    surface: normalizeSurface(options.surface, 'agent-skill'),
    agent: normalizeAgent(options.agent),
    $lib: `${PLUGIN_ID}-skill`,
    $lib_version: SKILL_VERSION,
    $process_person_profile: false,
    $geoip_disable: true,
  };
  if (/^[a-z0-9][a-z0-9_-]{0,63}$/.test(runId)) payloadProperties.run_id = runId;
  if (event === EVENT_NAMES.loaded) payloadProperties.first_run = identity.firstRun;

  const payload = {
    api_key: config.token,
    event,
    distinct_id: identity.id,
    properties: payloadProperties,
    timestamp: new Date().toISOString(),
  };
  if (/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/.test(eventUuid)) {
    payload.uuid = eventUuid;
  }
  const result = await postJson(`${config.host}/i/v0/e/`, payload);

  if (
    process.env.MATRIX_TELEMETRY_DEBUG === '1'
    || process.env.GEWEI_TELEMETRY_DEBUG === '1'
  ) {
    const detail = result.status ? ` status=${result.status}` : '';
    const error = result.error ? ` error=${result.error}` : '';
    process.stderr.write(`[matrix-analytics] ${event} ${result.ok ? 'ok' : 'failed'}${detail}${error}\n`);
  }

  return { ...result, event, distinct_id: identity.id, first_run: identity.firstRun };
}
