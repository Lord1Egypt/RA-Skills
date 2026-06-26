/**
 * HTTP client for fenxiang-ai-brain ContentApi.
 *
 * Zero dependencies — uses Node 18+ built-ins only (fetch / FormData / Blob).
 *
 * This file is internal to the `scripts/api/` directory. Each api script
 * imports from './_lib.mjs'. Users do not invoke it directly.
 *
 * Error contract: every function that can fail prints a single-line JSON
 * error to stderr and `process.exit(1)` on failure. Callers can assume
 * successful return values are well-formed.
 *
 * Error JSON schema:
 *   { "status": "error", "error_type": "<type>", "message": "...", "suggestion": "..." }
 *
 * Error types:
 *   - missing_api_key   FX_AI_API_KEY env var not set
 *   - invalid_argument  bad CLI args / missing required param
 *   - invalid_meta      meta.json missing required field / malformed
 *   - file_not_found    referenced file doesn't exist
 *   - api_unavailable   network / timeout / non-2xx HTTP
 *   - api_error         HTTP 200 but `code != 200` in response body
 */

import { readFile, stat } from 'node:fs/promises';
import { basename } from 'node:path';

// ----- config -----
export const API_BASE_URL = process.env.FX_AI_BASE_URL
  || 'https://api-ai-brain.fenxianglife.com/fenxiang-ai-brain';

const DEFAULT_TIMEOUT_MS = 30_000;

// ----- error helpers -----

/**
 * Print a structured error to stderr and exit with code 1.
 * Never returns.
 */
export function failWith(errorType, message, suggestion) {
  const payload = {
    status: 'error',
    error_type: errorType,
    message,
    suggestion: suggestion || '',
  };
  process.stderr.write(JSON.stringify(payload) + '\n');
  process.exit(1);
}

/**
 * Validate that FX_AI_API_KEY is set in the environment.
 * Exits with error if missing.
 */
export function requireApiKey() {
  const key = process.env.FX_AI_API_KEY;
  if (!key || !key.trim()) {
    failWith(
      'missing_api_key',
      'FX_AI_API_KEY 环境变量未设置',
      '请在 shell 中执行 `export FX_AI_API_KEY=<你的 key>`，然后重新运行。key 从 https://platform.fenxiang-ai.com/ 登录后获取。'
    );
  }
  return key.trim();
}

// ----- request core -----

function buildHeaders(apiKey, extra = {}) {
  return {
    'Fx-Ai-Api-Key': `Bearer ${apiKey}`,
    Accept: 'application/json',
    ...extra,
  };
}

async function doFetch(url, init) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS);
  try {
    return await fetch(url, { ...init, signal: controller.signal });
  } catch (e) {
    if (e.name === 'AbortError') {
      failWith(
        'api_unavailable',
        `请求超时 (${DEFAULT_TIMEOUT_MS / 1000}s): ${url}`,
        '检查网络或稍后重试。'
      );
    }
    failWith(
      'api_unavailable',
      `网络请求失败: ${e.message}`,
      '检查网络、DNS、代理设置。'
    );
  } finally {
    clearTimeout(timer);
  }
}

async function parseJsonOrFail(res, url) {
  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    failWith(
      'api_unavailable',
      `响应不是合法 JSON (HTTP ${res.status}): ${url}`,
      `服务端返回: ${text.slice(0, 200)}`
    );
  }
}

/**
 * Validate the CommonResult envelope and return `data`.
 * Exits with error if the envelope indicates failure — unless rawOnError=true,
 * in which case the full envelope is returned to the caller for custom handling.
 */
function unwrapCommonResult(body, url, rawOnError = false) {
  if (body && typeof body === 'object' && 'code' in body) {
    if (body.code === 200) return body.data;
    if (rawOnError) return body; // caller wants to inspect non-200 codes
    failWith(
      'api_error',
      `后端返回错误码 ${body.code}: ${body.message || body.errorMessage || '(no message)'}`,
      `端点: ${url}`
    );
  }
  // Some responses may be bare data; pass through
  return body;
}

/**
 * Sentinel returned by apiGet/apiPostJson when `rawOnError: true` and code != 200.
 * Callers can detect it via `result && result._isBusinessError === true`.
 */
function markBusinessError(envelope) {
  return {
    _isBusinessError: true,
    code: envelope.code,
    message: envelope.message || envelope.errorMessage || '',
    data: envelope.data ?? null,
  };
}

/**
 * True if a value returned from apiGet/apiPostJson (with rawOnError:true) is a
 * business-error sentinel. Lets callers handle specific codes like "文章不存在".
 */
export function isBusinessError(v) {
  return !!(v && typeof v === 'object' && v._isBusinessError === true);
}

// ----- public API -----

/**
 * GET a JSON endpoint. Returns the `data` field of CommonResult.
 * @param {string} path  path relative to API_BASE_URL, e.g. '/content/api/category/list'
 * @param {object} [query]  optional query params
 * @param {object} [options]
 * @param {boolean} [options.rawOnError=false]  if true, return a business-error
 *   sentinel `{ _isBusinessError, code, message, data }` instead of exit-on-error.
 */
export async function apiGet(path, query, options = {}) {
  const apiKey = requireApiKey();
  const url = new URL(API_BASE_URL + path);
  if (query) {
    for (const [k, v] of Object.entries(query)) {
      if (v != null) url.searchParams.set(k, String(v));
    }
  }
  const res = await doFetch(url.toString(), {
    method: 'GET',
    headers: buildHeaders(apiKey),
  });
  if (!res.ok) {
    failWith(
      'api_unavailable',
      `HTTP ${res.status} ${res.statusText}: GET ${url}`,
      '检查端点是否存在，或 API Key 是否有权限。'
    );
  }
  const body = await parseJsonOrFail(res, url.toString());
  const unwrapped = unwrapCommonResult(body, url.toString(), options.rawOnError === true);
  if (options.rawOnError && body && body.code !== 200) {
    return markBusinessError(body);
  }
  return unwrapped;
}

/**
 * POST a JSON body. Returns the `data` field of CommonResult.
 * @param {string} path  path relative to API_BASE_URL
 * @param {object} [body]  request body, will be JSON.stringify'd
 */
export async function apiPostJson(path, body) {
  const apiKey = requireApiKey();
  const url = API_BASE_URL + path;
  const res = await doFetch(url, {
    method: 'POST',
    headers: buildHeaders(apiKey, { 'Content-Type': 'application/json' }),
    body: body == null ? undefined : JSON.stringify(body),
  });
  if (!res.ok) {
    failWith(
      'api_unavailable',
      `HTTP ${res.status} ${res.statusText}: POST ${url}`,
      '检查请求体 / 端点 / 权限。'
    );
  }
  const parsed = await parseJsonOrFail(res, url);
  return unwrapCommonResult(parsed, url);
}

/**
 * POST a single file as multipart/form-data. Returns `data` field.
 * Used by the /content/api/upload endpoint.
 * @param {string} path     api path
 * @param {string} filePath absolute local file path
 * @param {string} [fieldName='file']  multipart form field name
 */
export async function apiPostMultipart(path, filePath, fieldName = 'file') {
  const apiKey = requireApiKey();
  const url = API_BASE_URL + path;

  try {
    await stat(filePath);
  } catch {
    failWith(
      'file_not_found',
      `上传文件不存在: ${filePath}`,
      '检查路径拼写，或先跑 image-localize.mjs 将图片拷贝到 posts/<slug>/images/。'
    );
  }

  const fileBuf = await readFile(filePath);
  const blob = new Blob([fileBuf]);
  const form = new FormData();
  form.append(fieldName, blob, basename(filePath));

  // NOTE: do NOT set Content-Type manually — fetch will add the correct
  // multipart boundary when body is FormData.
  const res = await doFetch(url, {
    method: 'POST',
    headers: buildHeaders(apiKey),
    body: form,
  });
  if (!res.ok) {
    failWith(
      'api_unavailable',
      `HTTP ${res.status} ${res.statusText}: POST ${url} (upload ${basename(filePath)})`,
      '检查文件大小 / 后端是否可用。'
    );
  }
  const parsed = await parseJsonOrFail(res, url);
  return unwrapCommonResult(parsed, url);
}

// ----- CLI helpers (shared by all api scripts) -----

/**
 * Parse `--flag value` style CLI arguments into an object.
 * Bare `--flag` (no value) becomes `true`.
 * Unknown args are collected as positional.
 */
export function parseCliArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--help' || a === '-h') { args.help = true; continue; }
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) {
        args[key] = true;
      } else {
        args[key] = next;
        i++;
      }
    } else {
      args._.push(a);
    }
  }
  return args;
}

/**
 * Print a JSON object to stdout. Used for successful return values.
 */
export function printJson(obj) {
  process.stdout.write(JSON.stringify(obj, null, 2) + '\n');
}

/**
 * Load and parse posts/<slug>/meta.json, with meta.json schema validation
 * that matters to the api layer. Exits with invalid_meta on failure.
 */
export async function loadMeta(postDir) {
  const path = postDir + '/meta.json';
  try {
    const text = await readFile(path, 'utf8');
    return JSON.parse(text);
  } catch (e) {
    if (e.code === 'ENOENT') {
      failWith(
        'file_not_found',
        `meta.json 不存在: ${path}`,
        '先用 new-post.mjs 创建文章骨架。'
      );
    }
    failWith(
      'invalid_meta',
      `meta.json 解析失败: ${e.message}`,
      '检查 meta.json 是否是合法的 JSON。'
    );
  }
}

/**
 * Save an updated meta.json back to disk.
 */
export async function saveMeta(postDir, meta) {
  const { writeFile } = await import('node:fs/promises');
  await writeFile(postDir + '/meta.json', JSON.stringify(meta, null, 2) + '\n', 'utf8');
}
