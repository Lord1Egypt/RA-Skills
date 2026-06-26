#!/usr/bin/env node
const http = require('http');
const https = require('https');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execSync } = require('child_process');
const url = require('url');

const PORT = Number(process.env.PORT || 18990);
const HOME = process.env.HOME || '/Users/bakeyzhang';
const ONE_HOUR_MS = 60 * 60 * 1000;
const MAX_WINDOW_MS = 6 * ONE_HOUR_MS;
const MIN_WINDOW_MS = 5 * 60 * 1000;
const ENTRY_CACHE_TTL_MS = 10000;
const STREAM_POLL_INTERVAL_MS = 8000;
const STREAM_PING_INTERVAL_MS = 30000;
const STREAM_MAX_TRACKED_KEYS = 1000;
const BOOTSTRAP_LOG_LIMIT_DEFAULT = 120;
const LOG_READ_MAX_BYTES_PER_FILE = clampNumber(process.env.LOG_READ_MAX_BYTES_PER_FILE, 96 * 1024, 32 * 1024, 512 * 1024);
const LOG_READ_MAX_LINES_PER_FILE = clampNumber(process.env.LOG_READ_MAX_LINES_PER_FILE, 600, 100, 3000);
const LOG_READ_MAX_ENTRIES = clampNumber(process.env.LOG_READ_MAX_ENTRIES, 350, 50, 2000);

const OPENCLAW_STATUS_CMD = process.env.OPENCLAW_STATUS_CMD || '/opt/homebrew/opt/node/bin/node /opt/homebrew/lib/node_modules/openclaw/dist/index.js gateway status --json';
const OPENCLAW_FULL_STATUS_CMD = process.env.OPENCLAW_FULL_STATUS_CMD || '/opt/homebrew/opt/node/bin/node /opt/homebrew/lib/node_modules/openclaw/dist/index.js status --json';
const USER_UID = process.getuid ? process.getuid() : Number(execSync('id -u', { encoding: 'utf8' }).trim());

const MINIMAX_REMAINS_URL = process.env.MINIMAX_REMAINS_URL || 'https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains';
const MINIMAX_CACHE_TTL_MS = clampNumber(process.env.MINIMAX_CACHE_TTL_MS, 20000, 5000, 120000);
const MINIMAX_AUTH_PROFILE_PATH = path.join(HOME, '.openclaw/agents/main/agent/auth-profiles.json');

const entryCache = new Map();
const sseClients = new Set();
const minimaxCache = {
  at: 0,
  value: null,
  inFlight: null
};

// Session usage tracking for velocity + history
const sessionTracker = {
  currentId: null,
  samples: [],      // { ts, pct, tokens }
  history: [],      // { sessionId, model, startedAt, endedAt, peakPercent, finalPercent }
  MAX_SAMPLES: 8,
  MAX_HISTORY: 10
};

function updateSessionTracking(context) {
  if (!context?.ok) return;
  const now = Date.now();
  const sid = context.sessionId || null;
  const pct = Number(context.percentUsed) || 0;
  const tokens = Number(context.totalTokens) || 0;

  const lastSample = sessionTracker.samples[sessionTracker.samples.length - 1];
  const tokensDrop = lastSample && tokens < lastSample.tokens * 0.5 && lastSample.tokens > 1000;
  const idChange = sid && sid !== sessionTracker.currentId;

  if (idChange || tokensDrop) {
    if (sessionTracker.samples.length >= 1) {
      const first = sessionTracker.samples[0];
      const last = lastSample;
      sessionTracker.history.unshift({
        sessionId: sessionTracker.currentId,
        model: context.model,
        startedAt: first.ts,
        endedAt: last.ts,
        peakPercent: Math.max(...sessionTracker.samples.map((s) => s.pct)),
        finalPercent: last.pct
      });
      if (sessionTracker.history.length > sessionTracker.MAX_HISTORY) {
        sessionTracker.history.length = sessionTracker.MAX_HISTORY;
      }
    }
    sessionTracker.currentId = sid;
    sessionTracker.samples = [];
  }

  sessionTracker.samples.push({ ts: now, pct, tokens });
  if (sessionTracker.samples.length > sessionTracker.MAX_SAMPLES) {
    sessionTracker.samples.shift();
  }
}

function sessionVelocity() {
  const s = sessionTracker.samples;
  if (s.length < 2) return null;
  const first = s[0];
  const last = s[s.length - 1];
  const dtMs = last.ts - first.ts;
  if (dtMs < 15000) return null;
  return round((last.pct - first.pct) / dtMs * 60000, 1); // %/min
}

function safeReadTail(filePath, maxBytes = LOG_READ_MAX_BYTES_PER_FILE) {
  try {
    const stat = fs.statSync(filePath);
    if (!stat.isFile()) return '';

    const size = Number(stat.size || 0);
    if (size <= 0) return '';

    const readBytes = Math.min(size, Math.max(1, Number(maxBytes) || LOG_READ_MAX_BYTES_PER_FILE));
    const start = Math.max(0, size - readBytes);
    const fd = fs.openSync(filePath, 'r');

    try {
      const buf = Buffer.allocUnsafe(readBytes);
      const bytesRead = fs.readSync(fd, buf, 0, readBytes, start);
      if (bytesRead <= 0) return '';

      let text = buf.toString('utf8', 0, bytesRead);
      if (start > 0) {
        const firstNl = text.indexOf('\n');
        if (firstNl >= 0) {
          text = text.slice(firstNl + 1);
        }
      }
      return text;
    } finally {
      fs.closeSync(fd);
    }
  } catch {
    return '';
  }
}

function localDateStamp(d = new Date()) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}

function buildLogFiles() {
  const now = new Date();
  const yesterday = new Date(now.getTime() - 24 * 60 * 60 * 1000);
  // Most-recent files first: today's tmp log usually has freshest data
  return [
    `/tmp/openclaw/openclaw-${localDateStamp(now)}.log`,
    path.join(HOME, '.openclaw/logs/gateway.err.log'),
    path.join(HOME, '.openclaw/logs/gateway.log'),
    `/tmp/openclaw/openclaw-${localDateStamp(yesterday)}.log`
  ];
}

function parseTime(line) {
  const m1 = line.match(/^(\d{4}-\d{2}-\d{2}T[^\s]+)/);
  if (m1) {
    const t = Date.parse(m1[1]);
    if (!Number.isNaN(t)) return t;
  }

  const m2 = line.match(/"time"\s*:\s*"([^"]+)"/);
  if (m2) {
    const t = Date.parse(m2[1]);
    if (!Number.isNaN(t)) return t;
  }

  return null;
}

function levelOf(line) {
  const s = line.toLowerCase();
  if (
    s.includes('error=') ||
    s.includes('fatal') ||
    s.includes('panic') ||
    s.includes('exception') ||
    s.includes('authentication_error') ||
    s.includes('api_error') ||
    s.includes('invalid api key') ||
    s.includes('enoent') ||
    s.includes('llm request timed out') ||
    s.includes('rate limit')
  ) return 'error';

  if (
    s.includes('warn') ||
    s.includes('warning') ||
    s.includes('security audit') ||
    s.includes('fetch fallback') ||
    s.includes('unknown entries')
  ) return 'warn';

  return 'info';
}

function signatureOf(line) {
  const s = line.toLowerCase();
  if (s.includes('error=terminated')) return 'terminated';
  if (s.includes('llm request timed out')) return 'llm_timeout';
  if (s.includes('authentication_error') || s.includes('invalid api key') || s.includes('login fail')) return 'auth_error';
  if (s.includes('rate limit')) return 'rate_limit';
  if (s.includes('enoent')) return 'file_missing';
  if (s.includes('remote bin probe timed out')) return 'remote_probe_timeout';
  if (s.includes('tools.profile') && s.includes('unknown entries')) return 'tools_profile_unknown_entries';
  if (s.includes('fetch fallback') && s.includes('ipv4first')) return 'network_fetch_fallback';
  if (s.includes('security audit')) return 'security_audit';
  if (s.includes('gateway restart failed') || s.includes('full process restart failed')) return 'gateway_restart_failed';
  return 'other';
}

function extractRunId(line) {
  const m = line.match(/runId=([a-zA-Z0-9\-]+)/);
  if (m) return m[1];
  const m2 = line.match(/"runId"\s*:\s*"([a-zA-Z0-9\-]+)"/);
  if (m2) return m2[1];
  return null;
}

function toEntry(file, line) {
  return {
    ts: parseTime(line),
    level: levelOf(line),
    signature: signatureOf(line),
    runId: extractRunId(line),
    file,
    message: line
  };
}

function dedupeKey(e) {
  if (e.runId && e.signature !== 'other') return `${e.signature}|${e.runId}`;
  const sec = e.ts ? Math.floor(e.ts / 1000) : 0;
  const norm = e.message
    .replace(/"_meta"\s*:\s*\{.*\}\s*,?/g, '')
    .replace(/\s+/g, ' ')
    .slice(0, 180);
  return `${e.signature}|${sec}|${norm}`;
}

function clampNumber(value, fallback, min, max) {
  const n = Number(value);
  if (!Number.isFinite(n)) return fallback;
  return Math.max(min, Math.min(max, n));
}

function round(value, digits = 1) {
  if (!Number.isFinite(value)) return null;
  const m = 10 ** digits;
  return Math.round(value * m) / m;
}

function runCommand(command, timeout = 2500) {
  try {
    return execSync(command, {
      encoding: 'utf8',
      timeout,
      stdio: ['ignore', 'pipe', 'ignore']
    }).trim();
  } catch {
    return '';
  }
}

let hasLsofCached = null;
function hasLsof() {
  if (hasLsofCached !== null) return hasLsofCached;
  hasLsofCached = Boolean(runCommand('command -v lsof', 800));
  return hasLsofCached;
}

function maskKey(key) {
  const s = String(key || '').trim();
  if (!s) return null;
  if (s.length <= 12) return `${s.slice(0, 2)}***${s.slice(-2)}`;
  return `${s.slice(0, 6)}***${s.slice(-4)}`;
}

function resolveMiniMaxApiKey() {
  const envKey = String(process.env.MINIMAX_CP_KEY || '').trim();
  if (envKey) {
    return {
      key: envKey,
      source: 'env'
    };
  }

  try {
    const raw = fs.readFileSync(MINIMAX_AUTH_PROFILE_PATH, 'utf8');
    const data = JSON.parse(raw);
    const key = String(data?.profiles?.['minimax-portal:default']?.access || '').trim();
    if (key) {
      return {
        key,
        source: 'auth-profile'
      };
    }
  } catch {
    // ignore
  }

  return {
    key: '',
    source: null
  };
}

function fetchJson(urlString, headers = {}, timeoutMs = 6000) {
  return new Promise((resolve, reject) => {
    const u = new URL(urlString);
    const req = https.request({
      protocol: u.protocol,
      hostname: u.hostname,
      port: u.port || 443,
      path: `${u.pathname}${u.search}`,
      method: 'GET',
      headers,
      timeout: timeoutMs
    }, (res) => {
      let body = '';
      res.setEncoding('utf8');
      res.on('data', (chunk) => {
        body += chunk;
      });
      res.on('end', () => {
        if (res.statusCode < 200 || res.statusCode >= 300) {
          return reject(new Error(`HTTP ${res.statusCode}: ${body.slice(0, 220)}`));
        }
        try {
          resolve(JSON.parse(body));
        } catch (err) {
          reject(new Error(`JSON parse failed: ${err.message}`));
        }
      });
    });

    req.on('timeout', () => {
      req.destroy(new Error('request timeout'));
    });
    req.on('error', (err) => reject(err));
    req.end();
  });
}

function normalizeMiniMaxModel(item, nowTs) {
  const startTime = Number(item?.start_time);
  const endTime = Number(item?.end_time);
  const totalCount = Number(item?.current_interval_total_count);
  const usageCount = Number(item?.current_interval_usage_count);
  const remainsRaw = Number(item?.remains_time);

  const safeTotal = Number.isFinite(totalCount) && totalCount >= 0 ? totalCount : 0;
  const safeUsage = Number.isFinite(usageCount) && usageCount >= 0 ? usageCount : 0;
  const remainingCount = safeTotal ? Math.max(0, safeTotal - safeUsage) : null;
  const usagePercent = safeTotal ? round((safeUsage / safeTotal) * 100, 2) : null;

  let remainsMs = Number.isFinite(remainsRaw) ? remainsRaw : null;
  if (remainsMs === null && Number.isFinite(endTime)) {
    remainsMs = Math.max(0, endTime - nowTs);
  }

  return {
    modelName: String(item?.model_name || 'unknown'),
    totalCount: safeTotal,
    usageCount: safeUsage,
    remainingCount,
    usagePercent,
    startTime: Number.isFinite(startTime) ? startTime : null,
    endTime: Number.isFinite(endTime) ? endTime : null,
    remainsMs
  };
}

function deriveWindowHours(models) {
  for (const m of models) {
    if (Number.isFinite(m.startTime) && Number.isFinite(m.endTime) && m.endTime > m.startTime) {
      return round((m.endTime - m.startTime) / 3600000, 2);
    }
  }
  return 5;
}

async function loadMiniMaxCodingPlan(force = false) {
  const now = Date.now();

  if (!force && minimaxCache.value && now - minimaxCache.at < MINIMAX_CACHE_TTL_MS) {
    return minimaxCache.value;
  }

  if (!force && minimaxCache.inFlight) {
    return minimaxCache.inFlight;
  }

  minimaxCache.inFlight = (async () => {
    const keyInfo = resolveMiniMaxApiKey();
    const basePayload = {
      now: new Date().toISOString(),
      ok: false,
      statusMsg: 'unavailable',
      keyMasked: maskKey(keyInfo.key),
      source: keyInfo.source,
      windowHours: 5,
      models: []
    };

    if (!keyInfo.key) {
      const result = {
        ...basePayload,
        statusMsg: 'missing_api_key',
        error: 'MiniMax Coding Plan API key not found (env MINIMAX_CP_KEY / auth profile).'
      };
      minimaxCache.value = result;
      minimaxCache.at = Date.now();
      return result;
    }

    try {
      const payload = await fetchJson(MINIMAX_REMAINS_URL, {
        Authorization: `Bearer ${keyInfo.key}`,
        'Content-Type': 'application/json'
      });

      const statusCode = Number(payload?.base_resp?.status_code);
      const statusMsg = String(payload?.base_resp?.status_msg || '');
      if (!Number.isFinite(statusCode) || statusCode !== 0) {
        throw new Error(`status_code=${Number.isFinite(statusCode) ? statusCode : 'unknown'} status_msg=${statusMsg || 'unknown'}`);
      }

      const modelItems = Array.isArray(payload?.model_remains) ? payload.model_remains : [];
      const models = modelItems.map((item) => normalizeMiniMaxModel(item, now));
      const result = {
        ...basePayload,
        ok: true,
        statusMsg: statusMsg || 'success',
        windowHours: deriveWindowHours(models),
        models
      };

      minimaxCache.value = result;
      minimaxCache.at = Date.now();
      return result;
    } catch (err) {
      const result = {
        ...basePayload,
        statusMsg: 'request_failed',
        error: String(err?.message || err)
      };

      minimaxCache.value = result;
      minimaxCache.at = Date.now();
      return result;
    }
  })();

  try {
    return await minimaxCache.inFlight;
  } finally {
    minimaxCache.inFlight = null;
  }
}

function getCachedMiniMaxCodingPlan() {
  return minimaxCache.value;
}

function loadEntries(windowMs = ONE_HOUR_MS) {
  const boundedWindow = clampNumber(windowMs, ONE_HOUR_MS, MIN_WINDOW_MS, MAX_WINDOW_MS);
  const cacheKey = String(boundedWindow);
  const now = Date.now();
  const cached = entryCache.get(cacheKey);
  if (cached && now - cached.at < ENTRY_CACHE_TTL_MS) {
    return cached.items;
  }

  const from = now - boundedWindow;
  const out = [];
  const seen = new Set();

  for (const file of buildLogFiles()) {
    const text = safeReadTail(file, LOG_READ_MAX_BYTES_PER_FILE);
    if (!text) continue;

    const lines = text.split('\n');
    const startIdx = Math.max(0, lines.length - LOG_READ_MAX_LINES_PER_FILE);
    for (let idx = startIdx; idx < lines.length; idx += 1) {
      const line = lines[idx];
      if (!line || line.length < 8) continue;
      const e = toEntry(file, line);
      if (!e.ts || e.ts < from) continue;
      const key = dedupeKey(e);
      if (seen.has(key)) continue;
      seen.add(key);
      out.push(e);
      if (out.length >= LOG_READ_MAX_ENTRIES) break;
    }

    if (out.length >= LOG_READ_MAX_ENTRIES) break;
  }

  out.sort((a, b) => b.ts - a.ts);
  const limited = out.slice(0, LOG_READ_MAX_ENTRIES);
  entryCache.set(cacheKey, { at: now, items: limited });
  return limited;
}

function countBy(items, key) {
  const map = {};
  for (const i of items) {
    map[i[key]] = (map[i[key]] || 0) + 1;
  }
  return map;
}

function withTTL(loader, ttlMs) {
  let cacheAt = 0;
  let cacheValue = null;
  return () => {
    const now = Date.now();
    if (cacheValue && now - cacheAt < ttlMs) return cacheValue;
    cacheValue = loader();
    cacheAt = now;
    return cacheValue;
  };
}

function readGatewayStatus() {
  try {
    const out = execSync(OPENCLAW_STATUS_CMD, {
      encoding: 'utf8',
      timeout: 3200,
      stdio: ['ignore', 'pipe', 'ignore']
    });
    const j = JSON.parse(out);
    return {
      loaded: !!j?.service?.loaded,
      runtimeStatus: j?.service?.runtime?.status || 'unknown',
      state: j?.service?.runtime?.state || 'unknown',
      pid: j?.service?.runtime?.pid || null,
      port: j?.gateway?.port || null,
      bindHost: j?.gateway?.bindHost || null
    };
  } catch (e) {
    return {
      loaded: false,
      runtimeStatus: 'unknown',
      state: 'unknown',
      pid: null,
      port: null,
      bindHost: null,
      error: String(e.message || e)
    };
  }
}

function normalizeSession(s) {
  const pct = Number.isFinite(Number(s.percentUsed)) ? Number(s.percentUsed) : null;
  const total = Number.isFinite(Number(s.totalTokens)) ? Number(s.totalTokens) : null;
  const ctx = Number.isFinite(Number(s.contextTokens)) ? Number(s.contextTokens) : null;
  const rem = Number.isFinite(Number(s.remainingTokens)) ? Number(s.remainingTokens) : null;
  return {
    id: s.id || s.runId || null,
    percentUsed: pct,
    totalTokens: total,
    contextTokens: ctx,
    remainingTokens: rem,
    model: s.model || null,
    abortedLastRun: !!s.abortedLastRun,
    startedAt: s.startedAt || s.createdAt || null,
    lastActivityAt: s.lastActivityAt || s.updatedAt || null
  };
}

function readSessionContextStatus() {
  try {
    const out = execSync(OPENCLAW_FULL_STATUS_CMD, {
      encoding: 'utf8',
      timeout: 4200,
      stdio: ['ignore', 'pipe', 'ignore']
    });
    const j = JSON.parse(out);
    const recent = Array.isArray(j?.sessions?.recent) ? j.sessions.recent : [];
    const s = recent[0] || null;
    const sessions = recent.slice(0, 8).map(normalizeSession);

    if (!s) {
      return {
        ok: false,
        percentUsed: null,
        totalTokens: null,
        contextTokens: null,
        remainingTokens: null,
        model: null,
        abortedLastRun: null,
        sessions
      };
    }

    return {
      ok: true,
      percentUsed: Number(s.percentUsed ?? 0),
      totalTokens: Number(s.totalTokens ?? 0),
      contextTokens: Number(s.contextTokens ?? 0),
      remainingTokens: Number(s.remainingTokens ?? 0),
      model: s.model || null,
      abortedLastRun: !!s.abortedLastRun,
      sessions
    };
  } catch (e) {
    return {
      ok: false,
      percentUsed: null,
      totalTokens: null,
      contextTokens: null,
      remainingTokens: null,
      model: null,
      abortedLastRun: null,
      sessions: [],
      error: String(e.message || e)
    };
  }
}

function readCurrentModel() {
  const log = safeReadTail(path.join(HOME, '.openclaw/logs/gateway.log'), 256 * 1024);
  const lines = log.split('\n').reverse();
  for (const line of lines) {
    const m = line.match(/agent model:\s*([^\s]+)/i);
    if (m) return m[1];
  }
  return 'unknown';
}

const gatewayStatus = withTTL(readGatewayStatus, 10000);
const sessionContextStatus = withTTL(readSessionContextStatus, 20000);
const currentModel = withTTL(readCurrentModel, 25000);

function launchAgentStatus(label) {
  const target = `gui/${USER_UID}/${label}`;
  try {
    const out = execSync(`launchctl print ${target}`, { encoding: 'utf8', timeout: 2500 });
    const pick = (re) => {
      const m = out.match(re);
      return m ? m[1].trim() : null;
    };

    return {
      label,
      target,
      exists: true,
      state: pick(/(?:^|\n)\s*state = ([^\n]+)/),
      jobState: pick(/(?:^|\n)\s*job state = ([^\n]+)/),
      pid: Number(pick(/(?:^|\n)\s*pid = (\d+)/) || 0) || null,
      runs: Number(pick(/(?:^|\n)\s*runs = (\d+)/) || 0),
      lastExitCode: Number(pick(/(?:^|\n)\s*last exit code = (-?\d+)/) || 0)
    };
  } catch (e) {
    return {
      label,
      target,
      exists: false,
      state: 'not loaded',
      jobState: 'unknown',
      pid: null,
      runs: 0,
      lastExitCode: null,
      error: String(e.message || e)
    };
  }
}

function readProcessMetrics(pid) {
  if (!pid) {
    return {
      cpuPercent: null,
      memoryMB: null,
      virtualMB: null,
      uptime: null
    };
  }

  const out = runCommand(`ps -p ${Number(pid)} -o %cpu=,rss=,vsz=,etime=`, 1800);
  const tokens = out.split(/\s+/).filter(Boolean);
  if (tokens.length < 4) {
    return {
      cpuPercent: null,
      memoryMB: null,
      virtualMB: null,
      uptime: null
    };
  }

  const [cpuRaw, rssRaw, vszRaw, ...etimeParts] = tokens;
  return {
    cpuPercent: round(Number(cpuRaw), 1),
    memoryMB: round(Number(rssRaw) / 1024, 1),
    virtualMB: round(Number(vszRaw) / 1024, 1),
    uptime: etimeParts.join(' ') || null
  };
}

function countLsofRows(output) {
  if (!output) return 0;
  const lines = output
    .split('\n')
    .map((s) => s.trim())
    .filter(Boolean);
  return lines.length > 1 ? lines.length - 1 : 0;
}

function readTcpConnections(port) {
  const p = Number(port);
  if (!Number.isFinite(p) || p <= 0) {
    return {
      established: null,
      listenSockets: 0,
      listening: false
    };
  }

  if (!hasLsof()) {
    return {
      established: null,
      listenSockets: null,
      listening: null
    };
  }

  const out = runCommand(`lsof -nP -iTCP:${p}`, 1800);
  let established = 0;
  let listenSockets = 0;
  for (const line of out.split('\n').slice(1)) {
    if (line.includes('(ESTABLISHED)')) established += 1;
    else if (line.includes('(LISTEN)')) listenSockets += 1;
  }

  return {
    established,
    listenSockets,
    listening: listenSockets > 0
  };
}

function hostMetrics() {
  const safeCall = (fn, fallback = null) => {
    try {
      return fn();
    } catch {
      return fallback;
    }
  };

  const totalBytes = safeCall(() => os.totalmem(), 0);
  const freeBytes = safeCall(() => os.freemem(), 0);
  const totalMB = totalBytes ? totalBytes / 1024 / 1024 : 0;
  const freeMB = freeBytes ? freeBytes / 1024 / 1024 : 0;
  const usedMB = Math.max(0, totalMB - freeMB);
  const load = safeCall(() => os.loadavg(), [null, null, null]);
  const uptimeSec = safeCall(() => Math.floor(os.uptime()), null);

  return {
    cpuLoad1: round(load[0], 2),
    cpuLoad5: round(load[1], 2),
    cpuLoad15: round(load[2], 2),
    memoryTotalMB: round(totalMB, 1),
    memoryUsedMB: round(usedMB, 1),
    memoryUsedPercent: totalMB ? round((usedMB / totalMB) * 100, 1) : null,
    uptimeSec
  };
}

function buildMetrics(gateway) {
  const processMetrics = readProcessMetrics(gateway?.pid);
  const conn = readTcpConnections(gateway?.port);

  return {
    gateway: {
      cpuPercent: processMetrics.cpuPercent,
      memoryMB: processMetrics.memoryMB,
      virtualMB: processMetrics.virtualMB,
      uptime: processMetrics.uptime,
      connections: conn.established,
      listening: conn.listening,
      listenSockets: conn.listenSockets
    },
    host: hostMetrics()
  };
}

function filterEntries(entries, filters) {
  const signature = String(filters.signature || '').trim();
  const level = String(filters.level || '').trim();
  const keyword = String(filters.keyword || '').trim().toLowerCase();

  // Support comma-separated levels (e.g., "error,warn")
  const levelSet = level ? new Set(level.split(',').map(l => l.trim()).filter(Boolean)) : null;

  return entries.filter((e) => {
    if (signature && e.signature !== signature) return false;
    if (levelSet && !levelSet.has(e.level)) return false;
    if (keyword && !e.message.toLowerCase().includes(keyword)) return false;
    return true;
  });
}

function buildAlerts(entries, gateway, metrics, context) {
  const now = Date.now();
  const fiveMinAgo = now - 5 * 60 * 1000;
  const tenMinAgo = now - 10 * 60 * 1000;

  let errorsLast5m = 0;
  let errorsPrev5m = 0;
  let terminatedLast5m = 0;

  for (const e of entries) {
    if (!e.ts) continue;
    if (e.ts >= fiveMinAgo) {
      if (e.level === 'error') errorsLast5m += 1;
      if (e.signature === 'terminated') terminatedLast5m += 1;
    } else if (e.ts >= tenMinAgo && e.level === 'error') {
      errorsPrev5m += 1;
    }
  }

  const items = [];
  const gatewayRunning = gateway.loaded && gateway.runtimeStatus === 'running';
  const errorSpike = errorsLast5m >= 6 && (errorsPrev5m === 0 ? errorsLast5m >= 6 : errorsLast5m >= errorsPrev5m * 2);
  const terminatedSpike = terminatedLast5m >= 3;
  const highCpu = Number.isFinite(metrics.gateway.cpuPercent) && metrics.gateway.cpuPercent >= 85;
  const highMem = Number.isFinite(metrics.gateway.memoryMB) && metrics.gateway.memoryMB >= 1024;
  const contextHot = Number.isFinite(context?.percentUsed) && context.percentUsed >= 85;

  if (!gatewayRunning) {
    items.push({
      id: 'gateway_down',
      level: 'critical',
      title: 'Gateway 非运行状态',
      detail: `runtime=${gateway.runtimeStatus} loaded=${gateway.loaded}`
    });
  }

  if (errorSpike) {
    items.push({
      id: 'error_spike',
      level: 'critical',
      title: '错误突增',
      detail: `最近5分钟 error=${errorsLast5m}，前5分钟=${errorsPrev5m}`
    });
  }

  if (terminatedSpike) {
    items.push({
      id: 'terminated_spike',
      level: 'high',
      title: 'terminated 频率升高',
      detail: `最近5分钟 terminated=${terminatedLast5m}`
    });
  }

  if (highCpu) {
    items.push({
      id: 'gateway_cpu_hot',
      level: 'high',
      title: 'Gateway CPU 偏高',
      detail: `当前 CPU=${metrics.gateway.cpuPercent}%`
    });
  }

  if (highMem) {
    items.push({
      id: 'gateway_mem_hot',
      level: 'medium',
      title: 'Gateway 内存偏高',
      detail: `当前 RSS=${metrics.gateway.memoryMB} MB`
    });
  }

  if (contextHot) {
    items.push({
      id: 'context_hot',
      level: 'medium',
      title: '会话上下文接近上限',
      detail: `context used=${context.percentUsed}%`
    });
  }

  const primarySession = Array.isArray(context?.sessions) ? context.sessions[0] : null;
  if (primarySession?.abortedLastRun) {
    items.push({
      id: 'session_aborted',
      level: 'high',
      title: '会话异常中断',
      detail: `最近会话 abortedLastRun=true | model=${primarySession.model || 'unknown'}`
    });
  }

  return {
    active: items.length > 0,
    items,
    stats: {
      errorsLast5m,
      errorsPrev5m,
      terminatedLast5m
    }
  };
}

function buildSummarySnapshot() {
  const entries = loadEntries(ONE_HOUR_MS);
  const gateway = gatewayStatus();
  const context = sessionContextStatus();
  const metrics = buildMetrics(gateway);
  const bySignature = countBy(entries, 'signature');
  const totals = {
    logs: entries.length,
    error: entries.filter((e) => e.level === 'error').length,
    warn: entries.filter((e) => e.level === 'warn').length,
    terminated: bySignature.terminated || 0
  };

  return {
    window: '1h',
    now: new Date().toISOString(),
    gateway,
    model: currentModel(),
    context,
    metrics,
    totals,
    bySignature,
    alerts: buildAlerts(entries, gateway, metrics, context),
    minimax: getCachedMiniMaxCodingPlan()
  };
}

function buildLaunchdAgents() {
  return {
    gateway: launchAgentStatus('ai.openclaw.gateway'),
    watchdog: launchAgentStatus('ai.openclaw.gateway-watchdog'),
    monitor: launchAgentStatus('ai.openclaw.gateway-monitor')
  };
}

const summarySnapshotCached = withTTL(buildSummarySnapshot, 10000);
const launchdAgentsCached = withTTL(buildLaunchdAgents, 15000);

function buildBootstrapSnapshot() {
  const summary = summarySnapshotCached();
  const entries = loadEntries(ONE_HOUR_MS).slice(0, BOOTSTRAP_LOG_LIMIT_DEFAULT);

  return {
    now: new Date().toISOString(),
    summary,
    agents: launchdAgentsCached(),
    logs: {
      count: summary?.totals?.logs ?? entries.length,
      limit: BOOTSTRAP_LOG_LIMIT_DEFAULT,
      items: entries
    }
  };
}

function buildDiagnosticsSnapshot() {
  const summary = summarySnapshotCached();
  return {
    now: new Date().toISOString(),
    summary,
    launchd: launchdAgentsCached()
  };
}

function json(res, obj, code = 200) {
  const body = JSON.stringify(obj);
  res.writeHead(code, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff'
  });
  res.end(body);
}

let indexHtmlCache = null;
function serveIndex(res) {
  if (!indexHtmlCache) {
    const p = path.join(__dirname, 'public/index.html');
    try {
      indexHtmlCache = fs.readFileSync(p, 'utf8');
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end(`Failed to load index.html: ${e.message}`);
      return;
    }
  }
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(indexHtmlCache);
}

function writeSSE(res, event, payload) {
  res.write(`event: ${event}\n`);
  res.write(`data: ${JSON.stringify(payload)}\n\n`);
}

function streamKeyOf(entry) {
  const msg = String(entry.message || '').slice(0, 160);
  return `${entry.ts || 0}|${entry.signature}|${entry.file}|${entry.runId || ''}|${msg}`;
}

function markStreamSeen(client, key) {
  if (client.seenSet.has(key)) return false;

  client.seenSet.add(key);
  client.seenQueue.push(key);

  if (client.seenQueue.length > STREAM_MAX_TRACKED_KEYS) {
    const old = client.seenQueue.shift();
    if (old) client.seenSet.delete(old);
  }

  return true;
}

// entries are desc-sorted; iterate backwards (asc) to avoid spread+reverse allocation
function pushStreamLogs(client, entries, initial = false) {
  const { signature, levelSet, keyword } = client.filters;
  const fresh = [];

  for (let i = entries.length - 1; i >= 0; i--) {
    const e = entries[i];
    if (!e.ts || e.ts < client.sinceTs) continue;
    if (signature && e.signature !== signature) continue;
    if (levelSet && !levelSet.has(e.level)) continue;
    if (keyword && !e.message.toLowerCase().includes(keyword)) continue;
    const key = streamKeyOf(e);
    if (!markStreamSeen(client, key)) continue;
    fresh.push(e);
  }

  if (!fresh.length) return;

  const payloadItems = initial && fresh.length > 80 ? fresh.slice(-80) : fresh;
  const last = payloadItems[payloadItems.length - 1];
  if (last?.ts) client.sinceTs = last.ts + 1;

  writeSSE(client.res, 'logs', {
    count: payloadItems.length,
    items: payloadItems
  });
}

function handleLogStream(req, res, query) {
  const sinceTs = Number(query.sinceTs);
  const level = String(query.level || '').trim();
  const filters = {
    signature: String(query.signature || '').trim(),
    level,
    keyword: String(query.keyword || '').trim().toLowerCase(),
    levelSet: level ? new Set(level.split(',').map((l) => l.trim()).filter(Boolean)) : null
  };

  res.writeHead(200, {
    'Content-Type': 'text/event-stream; charset=utf-8',
    'Cache-Control': 'no-cache, no-transform',
    Connection: 'keep-alive'
  });

  const client = {
    res,
    filters,
    sinceTs: Number.isFinite(sinceTs) && sinceTs > 0 ? sinceTs : Date.now() - 2 * 60 * 1000,
    lastPingAt: Date.now(),
    seenSet: new Set(),
    seenQueue: []
  };

  sseClients.add(client);
  writeSSE(res, 'ready', {
    now: new Date().toISOString(),
    filters: { signature: filters.signature, level: filters.level, keyword: filters.keyword }
  });

  pushStreamLogs(client, loadEntries(ONE_HOUR_MS), true);

  req.on('close', () => {
    sseClients.delete(client);
  });
}

let streamPumpBusy = false;
setInterval(() => {
  if (!sseClients.size) return;
  if (streamPumpBusy) return;
  streamPumpBusy = true;

  try {
    const now = Date.now();
    const entries = loadEntries(ONE_HOUR_MS);

    for (const client of Array.from(sseClients)) {
      try {
        pushStreamLogs(client, entries, false);
        if (now - client.lastPingAt >= STREAM_PING_INTERVAL_MS) {
          writeSSE(client.res, 'ping', { now: new Date(now).toISOString() });
          client.lastPingAt = now;
        }
      } catch (err) {
        try {
          client.res.end();
        } catch {
          // ignore
        }
        sseClients.delete(client);
        if (process.env.DEBUG_SSE) console.error('[sse] client error, removed:', err?.message || err);
      }
    }
  } finally {
    streamPumpBusy = false;
  }
}, STREAM_POLL_INTERVAL_MS);

const server = http.createServer((req, res) => {
  const parsed = url.parse(req.url, true);
  const pathname = parsed.pathname;

  if (pathname === '/') return serveIndex(res);

  if (pathname === '/api/logs/stream') {
    return handleLogStream(req, res, parsed.query || {});
  }

  if (pathname === '/api/minimax-coding-plan') {
    const force = String(parsed.query.force || '').trim() === '1';
    loadMiniMaxCodingPlan(force)
      .then((payload) => json(res, payload))
      .catch((err) => json(res, {
        now: new Date().toISOString(),
        ok: false,
        statusMsg: 'request_failed',
        keyMasked: null,
        source: null,
        windowHours: 5,
        models: [],
        error: String(err?.message || err)
      }, 500));
    return;
  }

  if (pathname === '/api/gateway-status') {
    const gateway = gatewayStatus();
    return json(res, {
      now: new Date().toISOString(),
      gateway,
      model: currentModel(),
      context: sessionContextStatus(),
      metrics: buildMetrics(gateway)
    });
  }

  if (pathname === '/api/context-status') {
    return json(res, {
      now: new Date().toISOString(),
      context: sessionContextStatus()
    });
  }

  if (pathname === '/api/sessions') {
    const ctx = sessionContextStatus();
    return json(res, {
      now: new Date().toISOString(),
      ok: ctx.ok,
      primary: ctx.ok ? {
        percentUsed: ctx.percentUsed,
        totalTokens: ctx.totalTokens,
        contextTokens: ctx.contextTokens,
        remainingTokens: ctx.remainingTokens,
        model: ctx.model,
        abortedLastRun: ctx.abortedLastRun
      } : null,
      sessions: ctx.sessions || [],
      error: ctx.error || null
    });
  }

  if (pathname === '/api/launchd-status') {
    return json(res, {
      now: new Date().toISOString(),
      agents: launchdAgentsCached()
    });
  }

  if (pathname === '/api/summary') {
    return json(res, summarySnapshotCached());
  }

  if (pathname === '/api/bootstrap') {
    return json(res, buildBootstrapSnapshot());
  }

  if (pathname === '/api/logs') {
    const levelFilter = parsed.query.level || 'error,warn';
    const entries = filterEntries(loadEntries(ONE_HOUR_MS), {
      signature: parsed.query.signature,
      level: levelFilter,
      keyword: parsed.query.keyword
    });

    return json(res, {
      now: new Date().toISOString(),
      count: entries.length,
      items: entries.slice(0, 150)
    });
  }

  if (pathname === '/api/diagnostics') {
    return json(res, buildDiagnosticsSnapshot());
  }

  if (pathname === '/api/restore-config') {
    // 只允许 GET 请求
    if (req.method !== 'GET') {
      res.writeHead(405, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ error: 'Method not allowed', allowed: ['GET'] }));
    }
    
    const confirm = String(parsed.query.confirm || '').trim();
    if (confirm !== 'true') {
      return json(res, {
        ok: false,
        error: 'Confirmation required',
        message: 'Add ?confirm=true to confirm restore of latest backup'
      }, 400);
    }
    
    try {
      const configBackupDir = path.join(HOME, '.openclaw/config-backups');
      const openclawJsonPath = path.join(HOME, '.openclaw/openclaw.json');
      
      // 查找最新的备份文件（按修改时间排序）
      const backupFiles = fs.readdirSync(configBackupDir)
        .filter(f => f.startsWith('openclaw.json.bak.'))
        .map(f => {
          const p = path.join(configBackupDir, f);
          return { name: f, path: p, mtime: fs.statSync(p).mtimeMs };
        })
        .sort((a, b) => b.mtime - a.mtime);
      
      if (backupFiles.length === 0) {
        return json(res, {
          ok: false,
          error: 'No backup files found',
          configBackupDir
        }, 404);
      }
      
      const latestBackup = backupFiles[0].name;
      const backupPath = backupFiles[0].path;
      
      // 复制备份到配置文件
      fs.copyFileSync(backupPath, openclawJsonPath);
      
      // 验证 JSON 格式
      const content = fs.readFileSync(openclawJsonPath, 'utf8');
      JSON.parse(content); // 如果无效会抛出异常
      
      return json(res, {
        ok: true,
        restored: latestBackup,
        backupPath,
        configPath: openclawJsonPath,
        message: 'Configuration restored successfully. Gateway restart may be required.'
      });
      
    } catch (err) {
      return json(res, {
        ok: false,
        error: 'Restore failed',
        message: err.message,
        stack: process.env.NODE_ENV === 'development' ? err.stack : undefined
      }, 500);
    }
  }

  res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('Not Found');
});

function prewarmFastCaches() {
  try {
    gatewayStatus();
    sessionContextStatus();
    currentModel();
    launchdAgentsCached();
    summarySnapshotCached();
  } catch {
    // ignore
  }
}

prewarmFastCaches();

function shutdown(signal) {
  console.log(`[gateway-monitor] received ${signal}, shutting down…`);
  for (const client of sseClients) {
    try { client.res.end(); } catch { /* ignore */ }
  }
  sseClients.clear();
  server.close(() => {
    console.log('[gateway-monitor] server closed.');
    process.exit(0);
  });
  setTimeout(() => process.exit(1), 5000).unref();
}

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Gateway monitor running: http://127.0.0.1:${PORT}`);


  setTimeout(() => {
    loadMiniMaxCodingPlan(false).catch(() => {
      // ignore
    });
  }, 1000);
  setInterval(() => {
    loadMiniMaxCodingPlan(false).catch(() => {
      // keep best-effort
    });
  }, Math.max(20000, MINIMAX_CACHE_TTL_MS));
});
