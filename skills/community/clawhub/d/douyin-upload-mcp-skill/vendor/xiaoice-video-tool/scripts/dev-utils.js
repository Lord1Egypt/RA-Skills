#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');
const { spawn, spawnSync } = require('node:child_process');

const REPO_ROOT = path.resolve(__dirname, '..');
const DEFAULT_PORT = 3105;
const DEFAULT_HOST = '127.0.0.1';
const DEFAULT_STATE_DIR = './data';
const DEFAULT_NGROK_BIN = 'ngrok';
const DEFAULT_NGROK_API_URL = 'http://127.0.0.1:4040';
const CALLBACK_PATH = '/v1/callbacks/provider';

class DevCommandError extends Error {
  constructor(message, options = {}) {
    const normalized = Array.isArray(options) ? { hints: options } : options;
    super(message);
    this.name = 'DevCommandError';
    this.hints = Array.isArray(normalized && normalized.hints) ? normalized.hints : [];
    if (normalized && normalized.code) {
      this.code = normalized.code;
    }
  }
}

function toTrimmedString(value, fallback = '') {
  if (value == null) {
    return fallback;
  }
  const trimmed = String(value).trim();
  return trimmed || fallback;
}

function normalizeBaseUrlOptional(value) {
  const trimmed = toTrimmedString(value);
  if (!trimmed) {
    return '';
  }
  try {
    const normalized = new URL(trimmed).toString().replace(/\/+$/, '');
    return normalized;
  } catch (error) {
    throw new DevCommandError(`Invalid URL value: ${trimmed}`, [
      'Set a full URL with protocol, for example: http://127.0.0.1:3105',
    ]);
  }
}

function parsePort(value, envName, fallback) {
  if (value == null || String(value).trim() === '') {
    return fallback;
  }
  const parsed = Number.parseInt(String(value), 10);
  if (!Number.isInteger(parsed) || parsed <= 0 || parsed > 65535) {
    throw new DevCommandError(`${envName} is invalid: ${value}`, [
      `${envName} must be an integer between 1 and 65535`,
    ]);
  }
  return parsed;
}

function parseBoolean(value, fallback = false) {
  if (value == null || String(value).trim() === '') {
    return fallback;
  }
  const lowered = String(value).trim().toLowerCase();
  if (['1', 'true', 'yes', 'on'].includes(lowered)) {
    return true;
  }
  if (['0', 'false', 'no', 'off'].includes(lowered)) {
    return false;
  }
  return fallback;
}

function parseEnvFileLine(rawLine) {
  const line = rawLine.trim();
  if (!line || line.startsWith('#')) {
    return null;
  }
  const withoutExport = line.startsWith('export ') ? line.slice('export '.length).trim() : line;
  const eqIndex = withoutExport.indexOf('=');
  if (eqIndex <= 0) {
    return null;
  }
  const key = withoutExport.slice(0, eqIndex).trim();
  if (!key) {
    return null;
  }
  let value = withoutExport.slice(eqIndex + 1);
  const isDoubleQuoted = value.startsWith('"') && value.endsWith('"');
  const isSingleQuoted = value.startsWith("'") && value.endsWith("'");
  if (isDoubleQuoted || isSingleQuoted) {
    value = value.slice(1, -1);
  } else {
    value = value.replace(/\s+#.*$/, '').trim();
  }
  return { key, value };
}

function loadDotEnv({ envPath = path.join(REPO_ROOT, '.env') } = {}) {
  if (!fs.existsSync(envPath)) {
    return [];
  }
  const raw = fs.readFileSync(envPath, 'utf8');
  const loadedKeys = [];
  for (const line of raw.split(/\r?\n/)) {
    const parsed = parseEnvFileLine(line);
    if (!parsed) {
      continue;
    }
    if (process.env[parsed.key] == null) {
      process.env[parsed.key] = parsed.value;
      loadedKeys.push(parsed.key);
    }
  }
  return loadedKeys;
}

function resolveStateDir(input, repoRoot = REPO_ROOT) {
  const raw = toTrimmedString(input, DEFAULT_STATE_DIR);
  if (path.isAbsolute(raw)) {
    return path.resolve(raw);
  }
  return path.resolve(repoRoot, raw);
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function ensureParentDir(filePath) {
  ensureDir(path.dirname(filePath));
}

function ensureRuntimeDir(context) {
  ensureDir(context.runtimeDir);
}

function getRuntimePaths(stateDir) {
  const runtimeDir = path.join(stateDir, 'runtime');
  return {
    runtimeDir,
    servicePidFile: path.join(runtimeDir, 'video-service.pid'),
    serviceLogFile: path.join(runtimeDir, 'video-service.log'),
    ngrokPidFile: path.join(runtimeDir, 'ngrok.pid'),
    ngrokLogFile: path.join(runtimeDir, 'ngrok.log'),
    ngrokUrlFile: path.join(runtimeDir, 'ngrok-url.txt'),
    bootstrapLastFile: path.join(runtimeDir, 'bootstrap.last.json'),
    runtimeConfigFile: path.join(stateDir, 'runtime-config.json'),
  };
}

function createContext({ env = process.env } = {}) {
  loadDotEnv();

  const serviceHost = toTrimmedString(env.VIDEO_TASK_SERVICE_HOST, DEFAULT_HOST);
  const servicePort = parsePort(env.VIDEO_TASK_SERVICE_PORT, 'VIDEO_TASK_SERVICE_PORT', DEFAULT_PORT);
  const requestHost = serviceHost === '0.0.0.0' ? DEFAULT_HOST : serviceHost;
  const stateDir = resolveStateDir(env.XIAOICE_VIDEO_STATE_DIR);
  const runtimePaths = getRuntimePaths(stateDir);
  const callbackFromEnv = normalizeBaseUrlOptional(env.VIDEO_CALLBACK_PUBLIC_BASE_URL);

  return {
    repoRoot: REPO_ROOT,
    stateDir,
    runtimeDir: runtimePaths.runtimeDir,
    paths: runtimePaths,
    service: {
      host: serviceHost,
      requestHost,
      port: servicePort,
      baseUrl: `http://${requestHost}:${servicePort}`,
      healthUrl: `http://${requestHost}:${servicePort}/health`,
    },
    ngrok: {
      enabled: parseBoolean(env.VIDEO_USE_NGROK, false),
      bin: toTrimmedString(env.NGROK_BIN, DEFAULT_NGROK_BIN),
      apiUrl: normalizeBaseUrlOptional(env.NGROK_API_URL || DEFAULT_NGROK_API_URL),
      authtoken: toTrimmedString(env.NGROK_AUTHTOKEN),
      domain: toTrimmedString(env.NGROK_DOMAIN),
      region: toTrimmedString(env.NGROK_REGION),
    },
    tokens: {
      admin: toTrimmedString(env.VIDEO_SERVICE_ADMIN_TOKEN),
      internal: toTrimmedString(env.VIDEO_SERVICE_INTERNAL_TOKEN),
      callback: toTrimmedString(env.VIDEO_SERVICE_CALLBACK_TOKEN),
    },
    callbackPublicBaseUrlFromEnv: callbackFromEnv,
  };
}

function readTextFileSafe(filePath, fallback = '') {
  try {
    return fs.existsSync(filePath) ? fs.readFileSync(filePath, 'utf8') : fallback;
  } catch (error) {
    return fallback;
  }
}

function writeTextFile(filePath, content) {
  ensureParentDir(filePath);
  fs.writeFileSync(filePath, content, 'utf8');
}

function readJsonFileSafe(filePath, fallback = null) {
  try {
    if (!fs.existsSync(filePath)) {
      return fallback;
    }
    const raw = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(raw);
  } catch (error) {
    return fallback;
  }
}

function writeJsonFile(filePath, value) {
  writeTextFile(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

function readPidFile(pidFilePath) {
  const raw = readTextFileSafe(pidFilePath, '').trim();
  if (!raw) {
    return null;
  }
  const parsed = Number.parseInt(raw, 10);
  return Number.isInteger(parsed) && parsed > 0 ? parsed : null;
}

function writePidFile(pidFilePath, pid) {
  writeTextFile(pidFilePath, `${pid}\n`);
}

function removeFileIfExists(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
    }
  } catch (error) {
    // Ignore cleanup failures in helper paths.
    void error;
  }
}

function isProcessRunning(pid) {
  if (!Number.isInteger(pid) || pid <= 0) {
    return false;
  }
  try {
    process.kill(pid, 0);
    return true;
  } catch (error) {
    if (error && error.code === 'EPERM') {
      return true;
    }
    return false;
  }
}

function killProcess(pid, signal = 'SIGTERM') {
  if (!Number.isInteger(pid) || pid <= 0) {
    return false;
  }
  try {
    process.kill(pid, signal);
    return true;
  } catch (error) {
    return false;
  }
}

async function spawnDetachedProcess({ command, args, logFilePath, env = process.env, cwd = REPO_ROOT }) {
  ensureParentDir(logFilePath);
  const stdoutFd = fs.openSync(logFilePath, 'a');

  try {
    const pid = await new Promise((resolve, reject) => {
      const child = spawn(command, args, {
        cwd,
        env,
        detached: true,
        stdio: ['ignore', stdoutFd, stdoutFd],
      });

      let settled = false;

      child.once('error', (error) => {
        if (settled) {
          return;
        }
        settled = true;
        reject(error);
      });

      child.once('spawn', () => {
        if (settled) {
          return;
        }
        settled = true;
        child.unref();
        resolve(child.pid);
      });

      setTimeout(() => {
        if (settled) {
          return;
        }
        settled = true;
        if (child.pid) {
          child.unref();
          resolve(child.pid);
        } else {
          reject(new Error(`Failed to spawn command: ${command}`));
        }
      }, 120);
    });

    return pid;
  } finally {
    fs.closeSync(stdoutFd);
  }
}

function verifyCommandAvailable(command, args = ['version']) {
  const result = spawnSync(command, args, { encoding: 'utf8' });
  if (result.error) {
    if (result.error.code === 'ENOENT') {
      throw new DevCommandError(`Command not found: ${command}`, [
        `Install ${command} and ensure it is available in PATH`,
      ]);
    }
    throw new DevCommandError(`Failed to execute ${command}: ${result.error.message}`, [
      `Run "${command} ${args.join(' ')}" manually to inspect local setup`,
    ]);
  }
  if (result.status !== 0) {
    throw new DevCommandError(`${command} is not ready (exit ${result.status})`, [
      `Run "${command} ${args.join(' ')}" manually to inspect the error`,
    ]);
  }
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function fetchWithTimeout(url, options = {}) {
  const timeoutMs = Number.isInteger(options.timeoutMs) ? options.timeoutMs : 5000;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    return await fetch(url, {
      ...options,
      signal: controller.signal,
    });
  } finally {
    clearTimeout(timer);
  }
}

async function requestJson(url, { method = 'GET', headers = {}, body, timeoutMs = 5000 } = {}) {
  const requestInit = {
    method,
    headers: { ...headers },
    timeoutMs,
  };

  if (body !== undefined) {
    requestInit.body = JSON.stringify(body);
    if (!Object.keys(requestInit.headers).some((name) => name.toLowerCase() === 'content-type')) {
      requestInit.headers['Content-Type'] = 'application/json';
    }
  }

  const response = await fetchWithTimeout(url, requestInit);
  let rawText = '';
  let data = null;

  if (typeof response.text === 'function') {
    rawText = await response.text();
    if (rawText) {
      try {
        data = JSON.parse(rawText);
      } catch (error) {
        data = null;
      }
    }
  } else if (typeof response.json === 'function') {
    try {
      data = await response.json();
      rawText = data == null ? '' : JSON.stringify(data);
    } catch (error) {
      data = null;
      rawText = '';
    }
  }

  return {
    ok: response.ok,
    status: response.status,
    statusText: response.statusText,
    data,
    rawText,
  };
}

async function waitFor(predicate, { timeoutMs = 20000, intervalMs = 500, errorMessage, hints = [] } = {}) {
  const startedAt = Date.now();
  let lastError = null;

  while (Date.now() - startedAt <= timeoutMs) {
    try {
      const result = await predicate();
      if (result) {
        return result;
      }
    } catch (error) {
      lastError = error;
    }
    await sleep(intervalMs);
  }

  if (lastError instanceof DevCommandError) {
    throw lastError;
  }

  if (lastError) {
    throw new DevCommandError(errorMessage || lastError.message, hints);
  }

  throw new DevCommandError(errorMessage || `Timed out after ${timeoutMs}ms`, hints);
}

async function getServiceHealth(context, { timeoutMs = 1500 } = {}) {
  try {
    const response = await requestJson(context.service.healthUrl, {
      method: 'GET',
      timeoutMs,
    });
    const isHealthy = response.ok && response.data && response.data.status === 'ok';
    return {
      ok: isHealthy,
      status: response.status,
      data: response.data,
    };
  } catch (error) {
    return {
      ok: false,
      status: 0,
      error,
    };
  }
}

async function waitForServiceHealth(context, { timeoutMs = 20000 } = {}) {
  return waitFor(
    async () => {
      const health = await getServiceHealth(context, { timeoutMs: 1500 });
      return health.ok ? health : null;
    },
    {
      timeoutMs,
      intervalMs: 500,
      errorMessage: `Service health check did not pass at ${context.service.healthUrl}`,
      hints: [
        `Check logs at ${context.paths.serviceLogFile}`,
        'Verify VIDEO_SERVICE_INTERNAL_TOKEN / VIDEO_SERVICE_ADMIN_TOKEN / VIDEO_SERVICE_CALLBACK_TOKEN in .env',
      ],
    }
  );
}

function buildCallbackEndpoint(baseUrl) {
  const normalized = normalizeBaseUrlOptional(baseUrl);
  if (!normalized) {
    throw new DevCommandError('callbackPublicBaseUrl is empty', [
      'Set VIDEO_CALLBACK_PUBLIC_BASE_URL in .env, or run npm run dev:ngrok first',
    ]);
  }
  return `${normalized}${CALLBACK_PATH}`;
}

function extractPortFromAddr(addr) {
  const raw = toTrimmedString(addr);
  if (!raw) {
    return null;
  }
  if (/^\d+$/.test(raw)) {
    return Number.parseInt(raw, 10);
  }

  try {
    const normalized = /^[a-z]+:\/\//i.test(raw) ? raw : `http://${raw}`;
    const parsed = new URL(normalized);
    if (parsed.port) {
      return Number.parseInt(parsed.port, 10);
    }
    if (parsed.protocol === 'http:') {
      return 80;
    }
    if (parsed.protocol === 'https:') {
      return 443;
    }
  } catch (error) {
    const match = raw.match(/:(\d+)(?:$|\/)/);
    if (match) {
      return Number.parseInt(match[1], 10);
    }
  }

  return null;
}

function parseHostFromAddr(addr) {
  const raw = toTrimmedString(addr);
  if (!raw) {
    return '';
  }
  try {
    const normalized = /^[a-z]+:\/\//i.test(raw) ? raw : `http://${raw}`;
    return new URL(normalized).hostname.toLowerCase();
  } catch (error) {
    const stripped = raw.replace(/^[a-z]+:\/\//i, '');
    const host = stripped.split('/')[0].split(':')[0];
    return host.toLowerCase();
  }
}

function isLocalHost(hostname) {
  return ['127.0.0.1', 'localhost', '0.0.0.0', '::1', '[::1]'].includes(String(hostname).toLowerCase());
}

function isHttpsPublicUrl(value) {
  return /^https:\/\//i.test(toTrimmedString(value));
}

function tunnelMatchesLocalPort(tunnel, servicePort) {
  const addr = toTrimmedString(tunnel && tunnel.config && tunnel.config.addr);
  if (!addr) {
    return false;
  }
  const parsedPort = extractPortFromAddr(addr);
  if (parsedPort !== servicePort) {
    return false;
  }
  const host = parseHostFromAddr(addr);
  return isLocalHost(host);
}

function pickBestNgrokTunnel(tunnels, servicePort) {
  const list = Array.isArray(tunnels) ? tunnels : [];
  const httpsTunnels = list.filter((tunnel) => isHttpsPublicUrl(tunnel && tunnel.public_url));
  const exactMatches = httpsTunnels.filter((tunnel) => tunnelMatchesLocalPort(tunnel, servicePort));
  const warnings = [];

  if (exactMatches.length > 1) {
    warnings.push(`Found ${exactMatches.length} HTTPS tunnels matching local port ${servicePort}; using the first.`);
  }

  if (exactMatches.length > 0) {
    return {
      tunnel: exactMatches[0],
      warnings,
    };
  }

  if (httpsTunnels.length > 0) {
    warnings.push(
      `No exact local tunnel match for port ${servicePort}; using first HTTPS tunnel ${httpsTunnels[0].public_url}.`
    );
    return {
      tunnel: httpsTunnels[0],
      warnings,
    };
  }

  return {
    tunnel: null,
    warnings,
  };
}

async function fetchNgrokTunnels(context, { timeoutMs = 5000 } = {}) {
  const endpoint = `${context.ngrok.apiUrl}/api/tunnels`;
  let response;
  try {
    response = await requestJson(endpoint, { method: 'GET', timeoutMs });
  } catch (error) {
    throw new DevCommandError(`Cannot reach ngrok API at ${endpoint}`, [
      `Run npm run dev:ngrok to start a tunnel`,
      `Verify NGROK_API_URL in .env (current: ${context.ngrok.apiUrl})`,
    ]);
  }

  if (!response.ok) {
    throw new DevCommandError(`ngrok API returned HTTP ${response.status}`, [
      'Confirm ngrok process is running and local API is enabled',
      `Inspect logs at ${context.paths.ngrokLogFile}`,
    ]);
  }

  if (!response.data || !Array.isArray(response.data.tunnels)) {
    throw new DevCommandError('ngrok API returned malformed tunnels payload', [
      'Check ngrok version compatibility (ngrok v3 is expected)',
      `Inspect ${context.ngrok.apiUrl}/api/tunnels manually`,
    ]);
  }

  return response.data.tunnels;
}

function getNgrokTunnelInfo(tunnels, servicePort) {
  const picked = pickBestNgrokTunnel(tunnels, servicePort);
  if (!picked.tunnel) {
    throw new DevCommandError(`No HTTPS ngrok tunnel found for local port ${servicePort}`, [
      'Run npm run dev:ngrok to create the tunnel',
      'Ensure ngrok is forwarding to VIDEO_TASK_SERVICE_PORT',
    ]);
  }
  const publicUrl = normalizeBaseUrlOptional(picked.tunnel.public_url);
  if (!isHttpsPublicUrl(publicUrl)) {
    throw new DevCommandError(`ngrok public URL is not HTTPS: ${picked.tunnel.public_url}`, [
      'Use ngrok HTTPS tunnel for provider callbacks',
    ]);
  }
  return {
    publicUrl,
    localAddr: toTrimmedString(picked.tunnel.config && picked.tunnel.config.addr),
    warnings: picked.warnings,
    tunnel: picked.tunnel,
  };
}

function selectNgrokTunnel(tunnels, servicePort) {
  const info = getNgrokTunnelInfo(tunnels, servicePort);
  return {
    publicUrl: info.publicUrl,
    localAddr: info.localAddr,
    addrPort: extractPortFromAddr(info.localAddr),
    warnings: info.warnings,
  };
}

function assertToken(name, value) {
  const token = toTrimmedString(value);
  if (!token) {
    throw new DevCommandError(`${name} is required`, [
      `Set ${name} in .env`,
    ]);
  }
  return token;
}

function validateServiceTokens(context, { requireAdmin = true, requireInternal = true, requireCallback = true } = {}) {
  if (requireAdmin) {
    assertToken('VIDEO_SERVICE_ADMIN_TOKEN', context.tokens.admin);
  }
  if (requireInternal) {
    assertToken('VIDEO_SERVICE_INTERNAL_TOKEN', context.tokens.internal);
  }
  if (requireCallback) {
    assertToken('VIDEO_SERVICE_CALLBACK_TOKEN', context.tokens.callback);
  }
}

function logResolvedStateDir(commandName, context) {
  console.log(`[${commandName}] state directory: ${context.stateDir}`);
}

function saveBootstrapState(context, payload) {
  writeJsonFile(context.paths.bootstrapLastFile, {
    updatedAt: new Date().toISOString(),
    ...payload,
  });
}

function formatErrorMessage(error) {
  if (!error) {
    return 'Unknown error';
  }
  if (error instanceof DevCommandError) {
    return error.message;
  }
  if (error.name === 'AbortError') {
    return 'Request timed out';
  }
  return error.message || String(error);
}

function getHints(error) {
  if (error instanceof DevCommandError && Array.isArray(error.hints)) {
    return error.hints;
  }
  return [];
}

function exitWithError(error, commandName) {
  const label = commandName || 'dev';
  console.error(`[${label}] ERROR: ${formatErrorMessage(error)}`);
  for (const hint of getHints(error)) {
    console.error(`[${label}] fix: ${hint}`);
  }
  process.exitCode = 1;
}

module.exports = {
  CALLBACK_PATH,
  DevCommandError,
  REPO_ROOT,
  assertToken,
  buildCallbackEndpoint,
  createContext,
  ensureRuntimeDir,
  exitWithError,
  fetchNgrokTunnels,
  formatErrorMessage,
  getHints,
  getNgrokTunnelInfo,
  getServiceHealth,
  isHttpsPublicUrl,
  isProcessRunning,
  killProcess,
  loadDotEnv,
  logResolvedStateDir,
  normalizeBaseUrlOptional,
  pickBestNgrokTunnel,
  readJsonFileSafe,
  readPidFile,
  readTextFileSafe,
  removeFileIfExists,
  requestJson,
  saveBootstrapState,
  selectNgrokTunnel,
  spawnDetachedProcess,
  toTrimmedString,
  resolveStateDir,
  validateServiceTokens,
  verifyCommandAvailable,
  waitFor,
  waitForServiceHealth,
  writeJsonFile,
  writePidFile,
  writeTextFile,
};
