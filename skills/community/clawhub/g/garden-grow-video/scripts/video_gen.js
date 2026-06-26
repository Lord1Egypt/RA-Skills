#!/usr/bin/env node
/**
 * WeryAI 视频生成 — 通用 CLI（零 npm 依赖，需 Node.js 18+）
 *
 * 命令:
 *   wait | submit-text | submit-image | submit-multi-image | status | models
 *
 * 示例:
 *   node video_gen.js models
 *   node video_gen.js models --mode text_to_video
 *   node video_gen.js wait --json '{"model":"WERYAI_VIDEO_1_0","prompt":"...","duration":5}'
 *   node video_gen.js wait --json '...' --dry-run
 *
 * 环境变量:
 *   WERYAI_API_KEY（models / 生成 / status 必填；--dry-run 除外）— 敏感凭据，勿写入仓库；registry 元数据声明见同目录 SKILL.md。
 *   WERYAI_BASE_URL（默认 https://api.weryai.com）
 *   WERYAI_MODELS_BASE_URL（默认 https://api-growth-agent.weryai.com）
 *     仅当解析后的 hostname 为 localhost / 127.0.0.1 或 *.weryai.com 时才会采用 env 覆盖，否则忽略并使用默认官方域名。
 *   WERYAI_POLL_INTERVAL_MS / WERYAI_POLL_TIMEOUT_MS（解析后为毫秒整数并 clamp，不用于请求 URL）
 */

const DEFAULT_MODEL = 'WERYAI_VIDEO_1_0';
const DEFAULT_API_ORIGIN = 'https://api.weryai.com';
const DEFAULT_MODELS_ORIGIN = 'https://api-growth-agent.weryai.com';
const MODELS_API_PATH = '/growthai/v1/video/models';

/** Strip trailing slash. */
function normalizeOrigin(raw) {
  return String(raw).replace(/\/$/, '');
}

function isAllowedServiceHost(hostname) {
  if (hostname === 'localhost' || hostname === '127.0.0.1') return true;
  if (hostname === 'api.weryai.com' || hostname === 'api-growth-agent.weryai.com') return true;
  if (hostname.endsWith('.weryai.com')) return true;
  return false;
}

/**
 * Turn optional env URL into a fetch origin. Hostname allowlist prevents env-based open redirects / SSRF
 * to arbitrary hosts; disallowed values fall back to defaults (see SKILL.md).
 * Return value is always either a built-in default string or `URL.origin` from a validated parse.
 */
function parseTrustedOriginFromEnv(envValue, fallbackOrigin) {
  if (typeof envValue !== 'string' || !envValue.trim()) return fallbackOrigin;
  const raw = normalizeOrigin(envValue.trim());
  let u;
  try {
    u = new URL(raw.includes('://') ? raw : `https://${raw}`);
  } catch {
    return fallbackOrigin;
  }
  if (u.protocol !== 'https:' && u.protocol !== 'http:') return fallbackOrigin;
  if (u.protocol === 'http:' && u.hostname !== 'localhost' && u.hostname !== '127.0.0.1') {
    return fallbackOrigin;
  }
  if (!isAllowedServiceHost(u.hostname)) {
    process.stderr.write(
      `[weryai] Ignoring WERYAI_*_URL host "${u.hostname}" (not allowlisted); using default origin.\n`,
    );
    return fallbackOrigin;
  }
  return u.origin;
}

function apiOrigin() {
  const raw =
    typeof process.env.WERYAI_BASE_URL === 'string' ? process.env.WERYAI_BASE_URL : '';
  return parseTrustedOriginFromEnv(raw, DEFAULT_API_ORIGIN);
}

function modelsOrigin() {
  const raw =
    typeof process.env.WERYAI_MODELS_BASE_URL === 'string' ? process.env.WERYAI_MODELS_BASE_URL : '';
  return parseTrustedOriginFromEnv(raw, DEFAULT_MODELS_ORIGIN);
}

/** Bounded poll tuning; values do not flow into request URLs. */
function pollIntervalMs() {
  const n = Number(process.env.WERYAI_POLL_INTERVAL_MS);
  if (!Number.isFinite(n)) return 6000;
  return Math.min(Math.max(Math.floor(n), 1000), 120_000);
}

function pollTimeoutMs() {
  const n = Number(process.env.WERYAI_POLL_TIMEOUT_MS);
  if (!Number.isFinite(n)) return 600_000;
  return Math.min(Math.max(Math.floor(n), 10_000), 3_600_000);
}

const STATUS_MAP = {
  waiting: 'waiting',
  WAITING: 'waiting',
  pending: 'waiting',
  PENDING: 'waiting',
  processing: 'processing',
  PROCESSING: 'processing',
  succeed: 'completed',
  SUCCEED: 'completed',
  success: 'completed',
  SUCCESS: 'completed',
  failed: 'failed',
  FAILED: 'failed',
};

const ERROR_MESSAGES = {
  400: 'Bad request — check your request parameters.',
  403: 'Invalid API key or IP access denied — verify WERYAI_API_KEY is correct.',
  500: 'WeryAI server error. Please try again later.',
  1001: 'Request rate limit exceeded — slow down and retry after a moment.',
  1002: 'Parameter error — check prompt, image URLs, aspect_ratio, model key, and duration.',
  1003: 'Resource not found — the task_id may not exist or has expired.',
  1006: 'Model not supported — check the model key or try a different model.',
  1007: 'Queue full — the service is busy, please try again later.',
  1011: 'Insufficient credits — recharge at weryai.com.',
  2003: 'Content flagged by safety system — revise your prompt or input image.',
  2004: 'Image format not supported — use jpg, png, or webp.',
  6004: 'Generation failed — please try again later.',
  6010: 'Concurrent task limit reached (max 20) — wait for existing tasks to complete.',
};

function log(msg) {
  process.stderr.write(`[weryai] ${msg}\n`);
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function httpJson(method, fullUrl, body, apiKey) {
  const headers = {
    Authorization: `Bearer ${apiKey}`,
    'Content-Type': 'application/json',
  };
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 30_000);
  try {
    const res = await fetch(fullUrl, {
      method,
      headers,
      body: body != null ? JSON.stringify(body) : undefined,
      signal: controller.signal,
    });
    clearTimeout(timer);
    let data;
    try {
      data = await res.json();
    } catch {
      data = { status: res.status, msg: `Non-JSON response (HTTP ${res.status})` };
    }
    return { httpStatus: res.status, ...data };
  } catch (err) {
    clearTimeout(timer);
    if (err.name === 'AbortError') {
      throw new Error(`Request timeout: ${method} ${fullUrl}`);
    }
    throw err;
  }
}

async function apiRequest(method, path, body, apiKey) {
  return httpJson(method, apiOrigin() + path, body, apiKey);
}

async function fetchModelsRegistry(apiKey) {
  return httpJson('GET', modelsOrigin() + MODELS_API_PATH, null, apiKey);
}

function isApiSuccess(res) {
  const httpOk = res.httpStatus >= 200 && res.httpStatus < 300;
  const bodyOk = res.status === 0 || res.status === 200;
  return httpOk && bodyOk;
}

function formatApiError(res) {
  const httpStatus = res.httpStatus || 0;
  const code = res.status;
  const msg = res.msg || '';

  if (httpStatus === 403) {
    return {
      ok: false,
      phase: 'failed',
      errorCode: '403',
      errorMessage: ERROR_MESSAGES[403] + (msg ? ` (${msg})` : ''),
    };
  }
  if (httpStatus === 429) {
    return {
      ok: false,
      phase: 'failed',
      errorCode: 'RATE_LIMIT',
      errorMessage: 'Rate limited by WeryAI API. Please wait and try again.',
    };
  }
  if (httpStatus >= 500) {
    return {
      ok: false,
      phase: 'failed',
      errorCode: '500',
      errorMessage: `${ERROR_MESSAGES[500]} (HTTP ${httpStatus})`,
    };
  }
  if (httpStatus === 400) {
    return {
      ok: false,
      phase: 'failed',
      errorCode: '400',
      errorMessage: ERROR_MESSAGES[400] + (msg ? ` (${msg})` : ''),
    };
  }

  const friendly = ERROR_MESSAGES[code] || '';
  const message =
    friendly && msg
      ? `${friendly} (${msg})`
      : friendly || msg || `API error (status: ${code}, HTTP ${httpStatus})`;

  return {
    ok: false,
    phase: 'failed',
    errorCode: code != null ? String(code) : null,
    errorMessage: message,
  };
}

function detectMode(params) {
  if (Array.isArray(params.images) && params.images.length > 0) return 'multi_image';
  if (typeof params.image === 'string' && params.image) return 'image';
  return 'text';
}

function coerceBool(v, defaultVal = false) {
  if (v == null) return defaultVal;
  if (typeof v === 'boolean') return v;
  return String(v).toLowerCase() === 'true';
}

function buildRequestBody(params) {
  const model = params.model || DEFAULT_MODEL;
  const body = {
    prompt: params.prompt,
    model,
    duration: Number(params.duration) || 5,
  };
  if (params.aspect_ratio) body.aspect_ratio = params.aspect_ratio;
  if (params.resolution) body.resolution = params.resolution;
  if (params.generate_audio != null) body.generate_audio = coerceBool(params.generate_audio, false);
  if (params.negative_prompt) body.negative_prompt = params.negative_prompt;
  if (params.image) body.image = params.image;
  if (params.images) body.images = params.images.slice(0, 3);
  return body;
}

async function submitTask(params, apiKey) {
  const mode = detectMode(params);
  const pathMap = {
    text: '/v1/generation/text-to-video',
    image: '/v1/generation/image-to-video',
    multi_image: '/v1/generation/multi-image-to-video',
  };
  const body = buildRequestBody(params);
  let res;
  try {
    res = await apiRequest('POST', pathMap[mode], body, apiKey);
  } catch (err) {
    return {
      ok: false,
      phase: 'failed',
      errorCode: 'NETWORK_ERROR',
      errorMessage: err.message || String(err),
    };
  }

  if (!isApiSuccess(res)) return formatApiError(res);

  const data = res.data || {};
  const taskIds = data.task_ids ?? (data.task_id ? [data.task_id] : []);
  return {
    ok: true,
    phase: 'submitted',
    batchId: data.batch_id ?? null,
    taskIds,
    taskId: taskIds[0] ?? null,
    taskStatus: null,
    videos: null,
    errorCode: null,
    errorMessage: null,
  };
}

function extractVideos(taskData) {
  const tr = taskData.task_result || {};
  const raw = tr.videos || taskData.videos || [];
  return raw.map((v) => {
    if (typeof v === 'string') {
      return { url: v, cover_url: '' };
    }
    return {
      url: v?.url || v?.video_url || '',
      cover_url: v?.cover_image_url || v?.cover_url || '',
    };
  });
}

async function pollUntilDone(taskId, batchId, taskIds, apiKey) {
  const start = Date.now();
  while (true) {
    const elapsed = (Date.now() - start) / 1000;
    if (elapsed * 1000 >= pollTimeoutMs()) {
      return {
        ok: false,
        phase: 'failed',
        errorCode: 'TIMEOUT',
        errorMessage: `Poll timeout after ${Math.floor(elapsed)}s.`,
        batchId,
        taskIds,
        taskId,
        taskStatus: 'unknown',
        videos: null,
      };
    }

    await sleep(pollIntervalMs());

    let res;
    try {
      res = await apiRequest('GET', `/v1/generation/${taskId}/status`, null, apiKey);
    } catch (err) {
      log(`Warning: poll failed (${err.message}), retrying...`);
      continue;
    }

    if (!isApiSuccess(res)) {
      log('Warning: poll returned non-success status, retrying...');
      continue;
    }

    const taskData = res.data || {};
    const rawStatus = taskData.task_status || '';
    const normalized = STATUS_MAP[rawStatus] || 'unknown';
    const elapsedSec = Math.floor((Date.now() - start) / 1000);
    log(`Polling ${taskId}... status: ${rawStatus} (${elapsedSec}s elapsed)`);

    if (normalized === 'completed') {
      const videos = extractVideos(taskData);
      return {
        ok: true,
        phase: 'completed',
        batchId,
        taskIds,
        taskId,
        taskStatus: rawStatus,
        videos: videos.length ? videos : null,
        errorCode: null,
        errorMessage: null,
      };
    }

    if (normalized === 'failed') {
      const tr = taskData.task_result || {};
      const errMsg = tr.message || taskData.msg || 'Task failed';
      return {
        ok: false,
        phase: 'failed',
        batchId,
        taskIds,
        taskId,
        taskStatus: rawStatus,
        videos: null,
        errorCode: 'TASK_FAILED',
        errorMessage: errMsg,
      };
    }
  }
}

async function cmdWait(params, apiKey) {
  const submitResult = await submitTask(params, apiKey);
  if (!submitResult.ok) return submitResult;
  const taskId = submitResult.taskId;
  const batchId = submitResult.batchId;
  const taskIds = submitResult.taskIds || [taskId];
  log(`Submitted task ${taskId}. Polling for completion...`);
  return pollUntilDone(taskId, batchId, taskIds, apiKey);
}

async function cmdStatus(taskId, apiKey) {
  let res;
  try {
    res = await apiRequest('GET', `/v1/generation/${taskId}/status`, null, apiKey);
  } catch (err) {
    return {
      ok: false,
      phase: 'failed',
      errorCode: 'NETWORK_ERROR',
      errorMessage: err.message || String(err),
    };
  }

  if (!isApiSuccess(res)) return formatApiError(res);

  const taskData = res.data || {};
  const rawStatus = taskData.task_status || '';
  const normalized = STATUS_MAP[rawStatus] || 'unknown';
  const videos = extractVideos(taskData);
  const phase =
    normalized === 'completed' ? 'completed' : normalized === 'failed' ? 'failed' : 'running';
  const tr = taskData.task_result || {};
  return {
    ok: phase !== 'failed',
    phase,
    batchId: null,
    taskIds: [taskId],
    taskId,
    taskStatus: rawStatus,
    videos: videos.length ? videos : null,
    errorCode: phase === 'failed' ? 'TASK_FAILED' : null,
    errorMessage: phase === 'failed' ? tr.message || taskData.msg || null : null,
  };
}

const VALID_MODEL_MODES = ['text_to_video', 'image_to_video', 'multi_image_to_video'];

async function cmdModels(modeFilter, apiKey) {
  let res;
  try {
    res = await fetchModelsRegistry(apiKey);
  } catch (err) {
    return {
      ok: false,
      phase: 'failed',
      errorCode: 'NETWORK_ERROR',
      errorMessage: err.message || String(err),
    };
  }

  if (!isApiSuccess(res)) return formatApiError(res);

  const data = res.data || {};
  const out = { ok: true, phase: 'completed' };

  if (modeFilter) {
    if (!VALID_MODEL_MODES.includes(modeFilter)) {
      return {
        ok: false,
        phase: 'failed',
        errorCode: 'VALIDATION',
        errorMessage: `Invalid --mode. Use: ${VALID_MODEL_MODES.join(', ')}`,
      };
    }
    out[modeFilter] = data[modeFilter] || [];
  } else {
    out.text_to_video = data.text_to_video || [];
    out.image_to_video = data.image_to_video || [];
    out.multi_image_to_video = data.multi_image_to_video || [];
  }

  return out;
}

function parseArgs(argv) {
  const cmd = argv[0];
  let jsonStr = null;
  let taskId = null;
  let dryRun = false;
  let modelsMode = null;
  for (let i = 1; i < argv.length; i++) {
    if (argv[i] === '--json') jsonStr = argv[++i];
    else if (argv[i] === '--task-id') taskId = argv[++i];
    else if (argv[i] === '--dry-run') dryRun = true;
    else if (argv[i] === '--mode') modelsMode = argv[++i];
  }
  return { command: cmd, jsonStr, taskId, dryRun, modelsMode };
}

function printJson(obj) {
  process.stdout.write(`${JSON.stringify(obj, null, 2)}\n`);
}

async function main() {
  const argv = process.argv.slice(2);
  const valid = new Set([
    'wait',
    'submit-text',
    'submit-image',
    'submit-multi-image',
    'status',
    'models',
  ]);
  const { command, jsonStr, taskId: cliTaskId, dryRun, modelsMode } = parseArgs(argv);

  if (!command || !valid.has(command)) {
    printJson({
      ok: false,
      phase: 'failed',
      errorCode: 'USAGE',
      errorMessage:
        'Usage: node video_gen.js <wait|submit-text|submit-image|submit-multi-image|status|models> [--json \'...\'] [--task-id id] [--dry-run] [--mode text_to_video|image_to_video|multi_image_to_video]',
    });
    process.exit(1);
  }

  let params = {};
  if (jsonStr) {
    try {
      params = JSON.parse(jsonStr);
    } catch (e) {
      printJson({
        ok: false,
        phase: 'failed',
        errorCode: 'INVALID_JSON',
        errorMessage: `Invalid JSON: ${e.message}`,
      });
      process.exit(1);
    }
  }

  if (command === 'models') {
    const apiKey = (process.env.WERYAI_API_KEY || '').trim();
    if (!apiKey) {
      printJson({
        ok: false,
        phase: 'failed',
        errorCode: 'NO_API_KEY',
        errorMessage: 'Missing WERYAI_API_KEY environment variable.',
      });
      process.exit(1);
    }
    const result = await cmdModels(modelsMode, apiKey);
    printJson(result);
    process.exit(result.ok ? 0 : 1);
  }

  if (dryRun) {
    const mode = detectMode(params);
    const pathMap = {
      text: '/v1/generation/text-to-video',
      image: '/v1/generation/image-to-video',
      multi_image: '/v1/generation/multi-image-to-video',
    };
    const body = 'prompt' in params ? buildRequestBody(params) : {};
    printJson({
      ok: true,
      phase: 'dry-run',
      dryRun: true,
      requestBody: body,
      requestUrl: apiOrigin() + (pathMap[mode] || pathMap.text),
    });
    process.exit(0);
  }

  const apiKey = (process.env.WERYAI_API_KEY || '').trim();
  if (!apiKey) {
    printJson({
      ok: false,
      phase: 'failed',
      errorCode: 'NO_API_KEY',
      errorMessage: 'Missing WERYAI_API_KEY environment variable.',
    });
    process.exit(1);
  }

  let result;
  if (command === 'status') {
    const tid = cliTaskId || params.task_id || params.taskId;
    if (!tid) {
      printJson({
        ok: false,
        phase: 'failed',
        errorCode: 'MISSING_PARAM',
        errorMessage: 'status command requires --task-id <id>',
      });
      process.exit(1);
    }
    result = await cmdStatus(tid, apiKey);
  } else {
    if (!params.prompt) {
      printJson({
        ok: false,
        phase: 'failed',
        errorCode: 'MISSING_PARAM',
        errorMessage: "'prompt' is required in JSON parameters.",
      });
      process.exit(1);
    }
    result = command === 'wait' ? await cmdWait(params, apiKey) : await submitTask(params, apiKey);
  }

  printJson(result);
  process.exit(result.ok ? 0 : 1);
}

main().catch((err) => {
  printJson({
    ok: false,
    phase: 'failed',
    errorCode: 'FATAL',
    errorMessage: err.message || String(err),
  });
  process.exit(1);
});
