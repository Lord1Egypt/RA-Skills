const crypto = require('crypto');
const fs = require('fs');
const http = require('http');
const path = require('path');
const { DatabaseSync } = require('node:sqlite');

const DEFAULT_TASK_TIMEOUT_MS = 10 * 60 * 1000;
const DEFAULT_RETRY_DELAYS_MS = [2000, 5000, 10000];
const DEFAULT_RETRY_MAX = 3;
const DEFAULT_REQUEST_BODY_MAX_BYTES = 1024 * 1024;
const DEFAULT_PROVIDER_PATH = '/openapi/aivideo/create';
const DEFAULT_PROVIDER_BASE_URL = 'http://127.0.0.1:3999';
const DEFAULT_PORT = 3105;
const DEFAULT_HOST = '127.0.0.1';
const CALLBACK_PATH = '/v1/callbacks/provider';
const LEGACY_VHBIZMODE_ERROR_MESSAGE = 'vhbizmode is no longer supported; use vhBizId';
const DISALLOWED_WEAK_TOKENS = new Set([
  'video-internal-token',
  'video-admin-token',
  'video-callback-token',
  'replace-me',
]);

function ensureDirForFile(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function toInt(value, fallback) {
  const parsed = parseInt(value, 10);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function nowMs(nowFn) {
  return typeof nowFn === 'function' ? nowFn() : Date.now();
}

function hasOwn(object, key) {
  return Object.prototype.hasOwnProperty.call(object, key);
}

function toTrimmedString(value) {
  if (value == null) {
    return '';
  }
  return String(value).trim();
}

function ensureAbsolutePath(filePath) {
  return path.resolve(String(filePath));
}

function readJsonFileSafe(filePath, fallback) {
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
  ensureDirForFile(filePath);
  fs.writeFileSync(filePath, JSON.stringify(value, null, 2), 'utf8');
}

function jsonResponse(res, statusCode, payload) {
  if (res.writableEnded || res.destroyed) {
    return;
  }
  res.writeHead(statusCode, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(payload));
}

function parseJsonBody(req, maxBytes = DEFAULT_REQUEST_BODY_MAX_BYTES) {
  return new Promise((resolve, reject) => {
    let body = '';
    let size = 0;

    req.on('data', (chunk) => {
      size += chunk.length;
      if (size > maxBytes) {
        reject(new Error('PAYLOAD_TOO_LARGE'));
        req.destroy();
        return;
      }
      body += chunk.toString();
    });

    req.on('end', () => {
      if (!body) {
        resolve({});
        return;
      }
      try {
        resolve(JSON.parse(body));
      } catch (error) {
        reject(new Error('INVALID_JSON'));
      }
    });

    req.on('error', reject);
  });
}

function createTaskId() {
  if (typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID();
  }
  return `vtask-${Date.now()}-${Math.random().toString(36).slice(2, 12)}`;
}

function normalizeBaseUrl(baseUrl) {
  return String(baseUrl || '').replace(/\/+$/, '');
}

function parseRetryDelays(value) {
  const fallback = DEFAULT_RETRY_DELAYS_MS.slice();
  if (Array.isArray(value)) {
    const parsed = value
      .map((item) => toInt(item, NaN))
      .filter((item) => Number.isFinite(item) && item >= 0);
    return parsed.length > 0 ? parsed : fallback;
  }
  if (typeof value === 'string') {
    const parsed = value
      .split(',')
      .map((item) => toInt(item.trim(), NaN))
      .filter((item) => Number.isFinite(item) && item >= 0);
    return parsed.length > 0 ? parsed : fallback;
  }
  return fallback;
}

function isTerminalStatus(status) {
  return status === 'succeeded' || status === 'failed' || status === 'timeout';
}

function maskSecret(value) {
  if (!value || typeof value !== 'string') {
    return '';
  }
  if (value.length <= 6) {
    return '***';
  }
  return `${value.slice(0, 3)}***${value.slice(-3)}`;
}

function assertStrongToken(name, value) {
  const token = toTrimmedString(value);
  if (!token) {
    throw new Error(`${name} is required and must be explicitly configured`);
  }
  if (DISALLOWED_WEAK_TOKENS.has(token.toLowerCase())) {
    throw new Error(`${name} uses a weak default token and is not allowed`);
  }
  return token;
}

function resolveStatePaths(userConfig = {}) {
  const explicitDbPath = userConfig.dbPath ? ensureAbsolutePath(userConfig.dbPath) : '';
  const explicitRuntimeConfigPath = (userConfig.runtimeConfigPath || userConfig.secretsPath)
    ? ensureAbsolutePath(userConfig.runtimeConfigPath || userConfig.secretsPath)
    : '';
  const configuredStateDir = toTrimmedString(userConfig.stateDir || process.env.XIAOICE_VIDEO_STATE_DIR);
  const stateDir = configuredStateDir
    ? ensureAbsolutePath(configuredStateDir)
    : explicitDbPath
      ? path.dirname(explicitDbPath)
      : explicitRuntimeConfigPath
        ? path.dirname(explicitRuntimeConfigPath)
        : '';

  const dbPath = explicitDbPath || (stateDir ? path.join(stateDir, 'video_tasks.db') : '');
  const runtimeConfigPath = explicitRuntimeConfigPath || (stateDir ? path.join(stateDir, 'runtime-config.json') : '');

  if (!dbPath || !runtimeConfigPath) {
    throw new Error(
      'State paths are not configured. Set XIAOICE_VIDEO_STATE_DIR, or pass stateDir/dbPath/runtimeConfigPath.'
    );
  }

  return {
    stateDir,
    dbPath,
    runtimeConfigPath,
  };
}

function buildAuthHeader(config) {
  const authHeader = config.providerAuthHeader || 'X-API-Key';
  const key = config.apiKey || '';
  if (!key) {
    return null;
  }
  if (config.providerAuthScheme) {
    return [authHeader, `${config.providerAuthScheme} ${key}`];
  }
  return [authHeader, key];
}

function normalizeProviderPath(providerPath) {
  const normalized = toTrimmedString(providerPath || DEFAULT_PROVIDER_PATH);
  if (!normalized) {
    return DEFAULT_PROVIDER_PATH;
  }
  return normalized.startsWith('/') ? normalized : `/${normalized}`;
}

function extractProviderTaskId(payload) {
  if (!payload || typeof payload !== 'object') {
    return '';
  }
  if (typeof payload.data === 'string' && payload.data) {
    return payload.data.trim();
  }
  return String(
    payload.providerTaskId
      || payload.taskId
      || payload.id
      || payload.clientTaskId
      || payload.data?.providerTaskId
      || payload.data?.taskId
      || payload.result?.taskId
      || ''
  ).trim();
}

function extractVideoUrl(payload) {
  if (!payload || typeof payload !== 'object') {
    return '';
  }
  return String(
    payload.videoUrl
      || payload.url
      || payload.data?.videoUrl
      || payload.data?.url
      || payload.result?.videoUrl
      || ''
  ).trim();
}

function isFailureCallback(payload) {
  if (!payload || typeof payload !== 'object') {
    return false;
  }
  const status = String(payload.status || payload.state || '').toLowerCase();
  return payload.success === false || status === 'failed' || status === 'error';
}

function isPlainObject(value) {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

async function delay(ms) {
  await new Promise((resolve) => setTimeout(resolve, ms));
}

function createStore(dbPath) {
  ensureDirForFile(dbPath);
  const db = new DatabaseSync(dbPath);

  db.exec(`
    CREATE TABLE IF NOT EXISTS video_tasks (
      task_id TEXT PRIMARY KEY,
      provider_task_id TEXT UNIQUE,
      status TEXT NOT NULL,
      vh_biz_mode TEXT,
      request_payload TEXT,
      video_url TEXT,
      error_message TEXT,
      trace_id TEXT,
      session_id TEXT,
      created_at INTEGER NOT NULL,
      updated_at INTEGER NOT NULL,
      finished_at INTEGER
    );
  `);

  const insertStmt = db.prepare(`
    INSERT INTO video_tasks (
      task_id, provider_task_id, status, vh_biz_mode, request_payload,
      video_url, error_message, trace_id, session_id, created_at, updated_at, finished_at
    ) VALUES (
      :task_id, :provider_task_id, :status, :vh_biz_mode, :request_payload,
      :video_url, :error_message, :trace_id, :session_id, :created_at, :updated_at, :finished_at
    )
  `);

  const getByTaskIdStmt = db.prepare('SELECT * FROM video_tasks WHERE task_id = ? LIMIT 1');
  const getByProviderTaskIdStmt = db.prepare('SELECT * FROM video_tasks WHERE provider_task_id = ? LIMIT 1');

  const updateProviderStatusStmt = db.prepare(`
    UPDATE video_tasks
    SET provider_task_id = :provider_task_id,
        status = :status,
        updated_at = :updated_at,
        error_message = :error_message
    WHERE task_id = :task_id
  `);

  const updateFinalStmt = db.prepare(`
    UPDATE video_tasks
    SET status = :status,
        video_url = :video_url,
        error_message = :error_message,
        updated_at = :updated_at,
        finished_at = :finished_at
    WHERE task_id = :task_id
  `);

  const updateTimeoutStmt = db.prepare(`
    UPDATE video_tasks
    SET status = 'timeout',
        error_message = 'TASK_TIMEOUT',
        updated_at = :updated_at,
        finished_at = :finished_at
    WHERE task_id = :task_id
      AND status IN ('submitted', 'processing')
  `);

  return {
    insertTask(task) {
      insertStmt.run({
        task_id: task.taskId,
        provider_task_id: task.providerTaskId || null,
        status: task.status,
        vh_biz_mode: task.vhbizmode || null,
        request_payload: task.requestPayload ? JSON.stringify(task.requestPayload) : null,
        video_url: task.videoUrl || null,
        error_message: task.errorMessage || null,
        trace_id: task.traceId || null,
        session_id: task.sessionId || null,
        created_at: task.createdAt,
        updated_at: task.updatedAt,
        finished_at: task.finishedAt || null,
      });
    },
    getByTaskId(taskId) {
      const row = getByTaskIdStmt.get(taskId);
      if (!row) {
        return null;
      }
      if (row.request_payload) {
        try {
          row.request_payload = JSON.parse(row.request_payload);
        } catch (error) {
          row.request_payload = null;
        }
      }
      return {
        taskId: row.task_id,
        providerTaskId: row.provider_task_id || '',
        status: row.status,
        vhbizmode: row.vh_biz_mode || '',
        requestPayload: row.request_payload || null,
        videoUrl: row.video_url || '',
        errorMessage: row.error_message || '',
        traceId: row.trace_id || '',
        sessionId: row.session_id || '',
        createdAt: row.created_at,
        updatedAt: row.updated_at,
        finishedAt: row.finished_at || null,
      };
    },
    getByProviderTaskId(providerTaskId) {
      const row = getByProviderTaskIdStmt.get(providerTaskId);
      if (!row) {
        return null;
      }
      if (row.request_payload) {
        try {
          row.request_payload = JSON.parse(row.request_payload);
        } catch (error) {
          row.request_payload = null;
        }
      }
      return {
        taskId: row.task_id,
        providerTaskId: row.provider_task_id || '',
        status: row.status,
        vhbizmode: row.vh_biz_mode || '',
        requestPayload: row.request_payload || null,
        videoUrl: row.video_url || '',
        errorMessage: row.error_message || '',
        traceId: row.trace_id || '',
        sessionId: row.session_id || '',
        createdAt: row.created_at,
        updatedAt: row.updated_at,
        finishedAt: row.finished_at || null,
      };
    },
    markProcessing(taskId, providerTaskId, timestamp) {
      updateProviderStatusStmt.run({
        task_id: taskId,
        provider_task_id: providerTaskId || null,
        status: 'processing',
        updated_at: timestamp,
        error_message: null,
      });
    },
    markFailed(taskId, errorMessage, timestamp) {
      updateFinalStmt.run({
        task_id: taskId,
        status: 'failed',
        video_url: null,
        error_message: errorMessage || 'SUBMIT_FAILED',
        updated_at: timestamp,
        finished_at: timestamp,
      });
    },
    markSucceeded(taskId, videoUrl, timestamp) {
      updateFinalStmt.run({
        task_id: taskId,
        status: 'succeeded',
        video_url: videoUrl,
        error_message: null,
        updated_at: timestamp,
        finished_at: timestamp,
      });
    },
    markTimeout(taskId, timestamp) {
      updateTimeoutStmt.run({
        task_id: taskId,
        updated_at: timestamp,
        finished_at: timestamp,
      });
    },
    close() {
      db.close();
    },
  };
}

function buildProviderPayload({ runtimeConfig, task, callbackToken }) {
  const callbackBaseUrl = normalizeBaseUrl(runtimeConfig.callbackPublicBaseUrl);
  if (!callbackBaseUrl) {
    throw new Error('CALLBACK_BASE_URL_NOT_CONFIGURED');
  }

  const callbackUrl = new URL(`${callbackBaseUrl}${CALLBACK_PATH}`);
  if (callbackToken) {
    callbackUrl.searchParams.set('token', callbackToken);
  }

  const requestPayload = task.requestPayload && typeof task.requestPayload === 'object'
    ? task.requestPayload
    : {};

  const payload = {
    topic: requestPayload.topic || '',
    vhBizId: requestPayload.vhBizId || '',
    callbackUrl: callbackUrl.toString(),
  };

  const optionalProviderFields = ['title', 'content', 'materialList', 'ttsConf', 'aigcWatermark'];
  for (const field of optionalProviderFields) {
    if (hasOwn(requestPayload, field)) {
      payload[field] = requestPayload[field];
    }
  }

  if (runtimeConfig.modelId && !hasOwn(payload, 'modelId')) {
    payload.modelId = runtimeConfig.modelId;
  }

  return payload;
}

async function submitToProvider({ runtimeConfig, task, callbackToken, retryMax, retryDelaysMs, logger }) {
  const baseUrl = normalizeBaseUrl(runtimeConfig.apiBaseUrl);
  if (!baseUrl) {
    throw new Error('PROVIDER_BASE_URL_NOT_CONFIGURED');
  }

  const providerPath = normalizeProviderPath(runtimeConfig.providerPath);
  const endpoint = `${baseUrl}${providerPath}`;
  const authHeader = buildAuthHeader(runtimeConfig);
  const headers = { 'Content-Type': 'application/json' };

  if (authHeader) {
    headers[authHeader[0]] = authHeader[1];
  }

  const providerPayload = buildProviderPayload({
    runtimeConfig,
    task,
    callbackToken,
  });

  let lastError = null;
  const maxAttempts = Math.max(1, toInt(retryMax, DEFAULT_RETRY_MAX));

  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    try {
      const resp = await fetch(endpoint, {
        method: 'POST',
        headers,
        body: JSON.stringify(providerPayload),
      });

      let data = {};
      try {
        data = await resp.json();
      } catch (error) {
        data = {};
      }

      logger.info?.('[video-task-service] provider response', {
        taskId: task.taskId,
        status: resp.status,
        attempt,
      });

      if (!resp.ok) {
        const message = `PROVIDER_HTTP_${resp.status}`;
        if (resp.status >= 500 && attempt < maxAttempts) {
          lastError = new Error(message);
        } else {
          throw new Error(message);
        }
      } else {
        const providerTaskId = extractProviderTaskId(data);
        if (!providerTaskId) {
          throw new Error('PROVIDER_MISSING_TASK_ID');
        }
        return { providerTaskId, payload: data };
      }
    } catch (error) {
      lastError = error;
      if (attempt >= maxAttempts) {
        throw error;
      }
    }

    const waitMs = retryDelaysMs[Math.min(attempt - 1, retryDelaysMs.length - 1)] || 0;
    if (waitMs > 0) {
      await delay(waitMs);
    }
  }

  throw lastError || new Error('PROVIDER_SUBMIT_FAILED');
}

function createVideoTaskService(userConfig = {}) {
  const logger = userConfig.logger || console;
  const state = resolveStatePaths(userConfig);

  const config = {
    port: toInt(userConfig.port ?? process.env.VIDEO_TASK_SERVICE_PORT, DEFAULT_PORT),
    host: toTrimmedString(userConfig.host || process.env.VIDEO_TASK_SERVICE_HOST || DEFAULT_HOST),
    ...state,
    internalToken: assertStrongToken(
      'VIDEO_SERVICE_INTERNAL_TOKEN',
      userConfig.internalToken ?? process.env.VIDEO_SERVICE_INTERNAL_TOKEN
    ),
    adminToken: assertStrongToken(
      'VIDEO_SERVICE_ADMIN_TOKEN',
      userConfig.adminToken ?? process.env.VIDEO_SERVICE_ADMIN_TOKEN
    ),
    callbackToken: assertStrongToken(
      'VIDEO_SERVICE_CALLBACK_TOKEN',
      userConfig.callbackToken ?? process.env.VIDEO_SERVICE_CALLBACK_TOKEN
    ),
    taskTimeoutMs: toInt(userConfig.taskTimeoutMs ?? process.env.VIDEO_TASK_TIMEOUT_MS, DEFAULT_TASK_TIMEOUT_MS),
    providerSubmitMaxRetries: toInt(
      userConfig.providerSubmitMaxRetries ?? process.env.VIDEO_PROVIDER_SUBMIT_MAX_RETRIES,
      DEFAULT_RETRY_MAX
    ),
    providerSubmitRetryDelaysMs: parseRetryDelays(
      userConfig.providerSubmitRetryDelaysMs ?? process.env.VIDEO_PROVIDER_SUBMIT_RETRY_DELAYS_MS
    ),
    now: typeof userConfig.now === 'function' ? userConfig.now : () => Date.now(),
    requestBodyMaxBytes: toInt(
      userConfig.requestBodyMaxBytes ?? process.env.VIDEO_REQUEST_BODY_MAX_BYTES,
      DEFAULT_REQUEST_BODY_MAX_BYTES
    ),
  };

  const store = createStore(config.dbPath);
  const pendingQueue = [];
  let queueRunning = false;
  let closing = false;
  let server = null;

  const bootDefaults = {
    apiBaseUrl: toTrimmedString(
      userConfig.providerApiBaseUrl || process.env.VIDEO_PROVIDER_API_BASE_URL || DEFAULT_PROVIDER_BASE_URL
    ),
    apiKey: toTrimmedString(userConfig.providerApiKey || process.env.VIDEO_PROVIDER_API_KEY || ''),
    modelId: toTrimmedString(userConfig.providerModelId || process.env.VIDEO_PROVIDER_MODEL_ID || ''),
    vhbizmode: toTrimmedString(
      userConfig.vhBizId
      || process.env.VIDEO_PROVIDER_VH_BIZ_ID
      || ''
    ),
    callbackPublicBaseUrl: toTrimmedString(
      userConfig.callbackPublicBaseUrl || process.env.VIDEO_CALLBACK_PUBLIC_BASE_URL || ''
    ),
    providerAuthHeader: toTrimmedString(userConfig.providerAuthHeader || process.env.VIDEO_PROVIDER_AUTH_HEADER || ''),
    providerAuthScheme: toTrimmedString(userConfig.providerAuthScheme || process.env.VIDEO_PROVIDER_AUTH_SCHEME || ''),
    providerPath: normalizeProviderPath(userConfig.providerPath || process.env.VIDEO_PROVIDER_PATH || DEFAULT_PROVIDER_PATH),
  };

  const runtimeConfig = {
    ...bootDefaults,
    ...readJsonFileSafe(config.runtimeConfigPath, {}),
  };
  runtimeConfig.vhbizmode = toTrimmedString(
    runtimeConfig.vhbizmode || runtimeConfig.vhBizId || bootDefaults.vhbizmode
  );
  delete runtimeConfig.vhBizId;

  function persistRuntimeConfig() {
    writeJsonFile(config.runtimeConfigPath, runtimeConfig);
  }

  if (!fs.existsSync(config.runtimeConfigPath)) {
    persistRuntimeConfig();
  }

  function headerAuthFailed(req, headerName, expectedToken) {
    const provided = String(req.headers[headerName] || '').trim();
    return !expectedToken || provided !== expectedToken;
  }

  function callbackAuthFailed(req, expectedToken) {
    const headerToken = String(req.headers['x-callback-token'] || '').trim();
    const requestUrl = new URL(req.url, 'http://localhost');
    const queryToken = String(requestUrl.searchParams.get('token') || '').trim();
    const candidate = headerToken || queryToken;
    return !expectedToken || candidate !== expectedToken;
  }

  async function processTaskSubmission(taskId) {
    const task = store.getByTaskId(taskId);
    if (!task || isTerminalStatus(task.status)) {
      return;
    }

    try {
      const result = await submitToProvider({
        runtimeConfig,
        task,
        callbackToken: config.callbackToken,
        retryMax: config.providerSubmitMaxRetries,
        retryDelaysMs: config.providerSubmitRetryDelaysMs,
        logger,
      });
      store.markProcessing(task.taskId, result.providerTaskId, nowMs(config.now));
    } catch (error) {
      logger.error?.('[video-task-service] submit failed', {
        taskId: task.taskId,
        error: error.message,
      });
      store.markFailed(task.taskId, error.message || 'PROVIDER_SUBMIT_FAILED', nowMs(config.now));
    }
  }

  async function drainQueue() {
    if (queueRunning || closing) {
      return;
    }
    queueRunning = true;
    while (pendingQueue.length > 0 && !closing) {
      const taskId = pendingQueue.shift();
      await processTaskSubmission(taskId);
    }
    queueRunning = false;
  }

  function enqueueSubmission(taskId) {
    pendingQueue.push(taskId);
    setImmediate(() => {
      drainQueue().catch((error) => {
        logger.error?.('[video-task-service] queue error', error);
      });
    });
  }

  function materializeTimeoutIfNeeded(task) {
    if (!task || isTerminalStatus(task.status)) {
      return task;
    }
    const age = nowMs(config.now) - task.createdAt;
    if (age < config.taskTimeoutMs) {
      return task;
    }
    store.markTimeout(task.taskId, nowMs(config.now));
    return store.getByTaskId(task.taskId);
  }

  async function handleCreateTask(req, res) {
    if (headerAuthFailed(req, 'x-internal-token', config.internalToken)) {
      jsonResponse(res, 401, { error: { code: 'unauthorized', message: 'Unauthorized' } });
      return;
    }

    let payload;
    try {
      payload = await parseJsonBody(req, config.requestBodyMaxBytes);
    } catch (error) {
      if (error.message === 'PAYLOAD_TOO_LARGE') {
        jsonResponse(res, 413, { error: { code: 'payload_too_large', message: 'Payload too large' } });
        return;
      }
      jsonResponse(res, 400, { error: { code: 'invalid_json', message: 'Invalid JSON body' } });
      return;
    }

    if (!isPlainObject(payload)) {
      jsonResponse(res, 422, { error: { code: 'validation_error', message: 'request body must be an object' } });
      return;
    }

    if (hasOwn(payload, 'vhbizmode')) {
      jsonResponse(res, 422, {
        error: { code: 'validation_error', message: LEGACY_VHBIZMODE_ERROR_MESSAGE },
      });
      return;
    }

    if (hasOwn(payload, 'prompt')) {
      jsonResponse(res, 422, {
        error: { code: 'validation_error', message: 'prompt is deprecated; use topic' },
      });
      return;
    }

    if (hasOwn(payload, 'options')) {
      jsonResponse(res, 422, {
        error: { code: 'validation_error', message: 'options is deprecated; use top-level create fields' },
      });
      return;
    }

    const topic = typeof payload.topic === 'string' ? payload.topic.trim() : '';
    if (!topic) {
      jsonResponse(res, 422, { error: { code: 'validation_error', message: 'topic is required' } });
      return;
    }

    const requestVhBizId = typeof payload.vhBizId === 'string' ? payload.vhBizId.trim() : '';
    if (!requestVhBizId) {
      jsonResponse(res, 422, {
        error: { code: 'validation_error', message: 'vhBizId is required' },
      });
      return;
    }

    const sessionId = payload.sessionId == null ? '' : toTrimmedString(payload.sessionId);
    const traceId = payload.traceId == null ? '' : toTrimmedString(payload.traceId);
    if (payload.sessionId != null && !sessionId) {
      jsonResponse(res, 422, {
        error: { code: 'validation_error', message: 'sessionId must be a non-empty string when provided' },
      });
      return;
    }
    if (payload.traceId != null && !traceId) {
      jsonResponse(res, 422, {
        error: { code: 'validation_error', message: 'traceId must be a non-empty string when provided' },
      });
      return;
    }

    const title = payload.title == null ? undefined : toTrimmedString(payload.title);
    if (payload.title != null && !title) {
      jsonResponse(res, 422, {
        error: { code: 'validation_error', message: 'title must be a non-empty string when provided' },
      });
      return;
    }

    const content = payload.content == null ? undefined : toTrimmedString(payload.content);
    if (payload.content != null && !content) {
      jsonResponse(res, 422, {
        error: { code: 'validation_error', message: 'content must be a non-empty string when provided' },
      });
      return;
    }

    if (hasOwn(payload, 'materialList') && !Array.isArray(payload.materialList)) {
      jsonResponse(res, 422, {
        error: { code: 'validation_error', message: 'materialList must be an array when provided' },
      });
      return;
    }

    if (hasOwn(payload, 'ttsConf') && !isPlainObject(payload.ttsConf)) {
      jsonResponse(res, 422, {
        error: { code: 'validation_error', message: 'ttsConf must be an object when provided' },
      });
      return;
    }

    if (hasOwn(payload, 'aigcWatermark') && typeof payload.aigcWatermark !== 'boolean') {
      jsonResponse(res, 422, {
        error: { code: 'validation_error', message: 'aigcWatermark must be a boolean when provided' },
      });
      return;
    }

    const requestPayload = {
      topic,
      vhBizId: requestVhBizId,
    };
    if (title) {
      requestPayload.title = title;
    }
    if (content) {
      requestPayload.content = content;
    }
    if (hasOwn(payload, 'materialList')) {
      requestPayload.materialList = payload.materialList;
    }
    if (hasOwn(payload, 'ttsConf')) {
      requestPayload.ttsConf = payload.ttsConf;
    }
    if (hasOwn(payload, 'aigcWatermark')) {
      requestPayload.aigcWatermark = payload.aigcWatermark;
    }

    const taskId = createTaskId();
    const createdAt = nowMs(config.now);
    store.insertTask({
      taskId,
      providerTaskId: '',
      status: 'submitted',
      vhbizmode: requestVhBizId,
      requestPayload,
      videoUrl: '',
      errorMessage: '',
      traceId,
      sessionId,
      createdAt,
      updatedAt: createdAt,
      finishedAt: null,
    });

    enqueueSubmission(taskId);

    jsonResponse(res, 202, {
      data: {
        taskId,
        status: 'submitted',
        etaMinutes: 5,
      },
    });
  }

  async function handleGetTask(req, res, taskId) {
    if (headerAuthFailed(req, 'x-internal-token', config.internalToken)) {
      jsonResponse(res, 401, { error: { code: 'unauthorized', message: 'Unauthorized' } });
      return;
    }

    if (!taskId) {
      jsonResponse(res, 400, { error: { code: 'invalid_task_id', message: 'taskId is required' } });
      return;
    }

    let task = store.getByTaskId(taskId);
    task = materializeTimeoutIfNeeded(task);
    if (!task) {
      jsonResponse(res, 404, { error: { code: 'not_found', message: 'Task not found' } });
      return;
    }

    jsonResponse(res, 200, {
      data: {
        taskId: task.taskId,
        providerTaskId: task.providerTaskId || '',
        status: task.status,
        videoUrl: task.videoUrl || '',
        errorMessage: task.errorMessage || '',
        traceId: task.traceId || '',
        sessionId: task.sessionId || '',
        createdAt: task.createdAt,
        updatedAt: task.updatedAt,
        finishedAt: task.finishedAt,
      },
    });
  }

  async function handleCallback(req, res) {
    if (callbackAuthFailed(req, config.callbackToken)) {
      jsonResponse(res, 401, { error: { code: 'unauthorized', message: 'Unauthorized' } });
      return;
    }

    let payload;
    try {
      payload = await parseJsonBody(req, config.requestBodyMaxBytes);
    } catch (error) {
      if (error.message === 'PAYLOAD_TOO_LARGE') {
        jsonResponse(res, 413, { error: { code: 'payload_too_large', message: 'Payload too large' } });
        return;
      }
      jsonResponse(res, 400, { error: { code: 'invalid_json', message: 'Invalid JSON body' } });
      return;
    }

    const providerTaskId = extractProviderTaskId(payload);
    let task = providerTaskId ? store.getByProviderTaskId(providerTaskId) : null;
    if (!task && providerTaskId) {
      task = store.getByTaskId(providerTaskId);
    }
    if (!task) {
      jsonResponse(res, 404, { error: { code: 'not_found', message: 'Task not found' } });
      return;
    }

    if (!isTerminalStatus(task.status)) {
      const videoUrl = extractVideoUrl(payload);
      if (videoUrl) {
        store.markSucceeded(task.taskId, videoUrl, nowMs(config.now));
      } else if (isFailureCallback(payload)) {
        store.markFailed(task.taskId, 'PROVIDER_CALLBACK_FAILED', nowMs(config.now));
      } else if (providerTaskId && !task.providerTaskId) {
        store.markProcessing(task.taskId, providerTaskId, nowMs(config.now));
      }
    }

    jsonResponse(res, 200, {
      data: {
        acknowledged: true,
      },
    });
  }

  async function handleUpdateConfig(req, res) {
    if (headerAuthFailed(req, 'x-admin-token', config.adminToken)) {
      jsonResponse(res, 401, { error: { code: 'unauthorized', message: 'Unauthorized' } });
      return;
    }

    let payload;
    try {
      payload = await parseJsonBody(req, config.requestBodyMaxBytes);
    } catch (error) {
      if (error.message === 'PAYLOAD_TOO_LARGE') {
        jsonResponse(res, 413, { error: { code: 'payload_too_large', message: 'Payload too large' } });
        return;
      }
      jsonResponse(res, 400, { error: { code: 'invalid_json', message: 'Invalid JSON body' } });
      return;
    }

    const updatableFields = [
      'apiBaseUrl',
      'apiKey',
      'modelId',
      'callbackPublicBaseUrl',
      'providerAuthHeader',
      'providerAuthScheme',
      'providerPath',
    ];

    for (const field of updatableFields) {
      if (hasOwn(payload, field)) {
        runtimeConfig[field] = toTrimmedString(payload[field]);
      }
    }

    if (hasOwn(payload, 'vhbizmode')) {
      jsonResponse(res, 422, {
        error: { code: 'validation_error', message: LEGACY_VHBIZMODE_ERROR_MESSAGE },
      });
      return;
    }

    if (hasOwn(payload, 'vhBizId')) {
      const nextVhBizId = typeof payload.vhBizId === 'string' ? payload.vhBizId.trim() : '';
      if (!nextVhBizId) {
        jsonResponse(res, 422, {
          error: { code: 'validation_error', message: 'vhBizId must be a non-empty string when provided' },
        });
        return;
      }
      runtimeConfig.vhbizmode = nextVhBizId;
    }

    if (runtimeConfig.providerPath) {
      runtimeConfig.providerPath = normalizeProviderPath(runtimeConfig.providerPath);
    }

    persistRuntimeConfig();

    jsonResponse(res, 200, {
      data: {
        apiBaseUrl: runtimeConfig.apiBaseUrl || '',
        apiKey: maskSecret(runtimeConfig.apiKey),
        modelId: runtimeConfig.modelId || '',
        vhBizId: runtimeConfig.vhbizmode || '',
        callbackPublicBaseUrl: runtimeConfig.callbackPublicBaseUrl || '',
        providerAuthHeader: runtimeConfig.providerAuthHeader || '',
        providerAuthScheme: runtimeConfig.providerAuthScheme || '',
        providerPath: runtimeConfig.providerPath || DEFAULT_PROVIDER_PATH,
      },
    });
  }

  function createServer() {
    return http.createServer(async (req, res) => {
      try {
        const url = new URL(req.url, 'http://localhost');
        const { pathname } = url;

        if (pathname === '/health' && req.method === 'GET') {
          jsonResponse(res, 200, {
            status: 'ok',
            service: 'video-task-service',
            timestamp: nowMs(config.now),
          });
          return;
        }

        if (pathname === '/v1/tasks' && req.method === 'POST') {
          await handleCreateTask(req, res);
          return;
        }

        if (pathname.startsWith('/v1/tasks/') && req.method === 'GET') {
          const taskId = decodeURIComponent(pathname.slice('/v1/tasks/'.length));
          await handleGetTask(req, res, taskId);
          return;
        }

        if (pathname === '/v1/callbacks/provider' && req.method === 'POST') {
          await handleCallback(req, res);
          return;
        }

        if (pathname === '/v1/admin/config' && req.method === 'PUT') {
          await handleUpdateConfig(req, res);
          return;
        }

        jsonResponse(res, 404, { error: { code: 'not_found', message: 'Not found' } });
      } catch (error) {
        logger.error?.('[video-task-service] unhandled request error', error);
        jsonResponse(res, 500, {
          error: { code: 'internal_error', message: error.message || 'Internal server error' },
        });
      }
    });
  }

  return {
    async start() {
      server = createServer();
      try {
        await new Promise((resolve, reject) => {
          server.once('error', reject);
          server.listen(config.port, config.host, resolve);
        });
      } catch (error) {
        store.close();
        throw error;
      }

      const address = server.address();
      const actualPort = address && typeof address === 'object' ? address.port : config.port;
      if (!runtimeConfig.callbackPublicBaseUrl) {
        const fallbackHost = config.host === '0.0.0.0' ? '127.0.0.1' : config.host;
        runtimeConfig.callbackPublicBaseUrl = `http://${fallbackHost}:${actualPort}`;
        persistRuntimeConfig();
      }

      return {
        host: config.host,
        port: actualPort,
        async close() {
          closing = true;
          await new Promise((resolve) => {
            if (!server || !server.listening) {
              resolve();
              return;
            }
            server.close(() => resolve());
          });
          store.close();
        },
      };
    },
  };
}

async function startVideoTaskService(config = {}) {
  const service = createVideoTaskService(config);
  return service.start();
}

module.exports = {
  createVideoTaskService,
  startVideoTaskService,
};
