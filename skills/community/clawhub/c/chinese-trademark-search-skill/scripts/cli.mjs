#!/usr/bin/env node

/**
 * Chinese trademark search skill CLI.
 *
 * Design goals:
 * - Public skill safe for distribution
 * - No third-party dependencies
 * - Uses platform user token only
 * - Never prints token
 * - Always returns structured JSON to stdout
 */

import { randomUUID } from 'node:crypto';

const DEFAULT_TIMEOUT_MS = 15000;
const DEFAULT_CHANNEL = 'clawhub';
/** 平台固定返回第一页前 50 条，暂不支持翻页，pageSize 不可调。 */
const FIXED_PAGE_SIZE = 50;
const MAX_RETRY_ATTEMPTS = 2;
const RETRY_DELAYS_MS = [1000, 2000];
/**
 * 可自动重试的错误码。
 *
 * 重试复用同一 X-OC-Request-Id，平台按该键去重：
 * - 上一次已扣点并成功 → 重试不重复扣点
 * - 上一次已扣点后失败并退点 → 平台会释放幂等键，重试重新正常扣点
 *
 * 刻意不含平台的 UPSTREAM_ERROR（详情上游故障）：那已经退过点了，
 * 自动重试只会连着捶上游，交给用户决定何时再试。
 * 也不含 RATE_LIMITED：限流窗口按分钟计，秒级重试没有意义，
 * 改为把 retryAfterSeconds 透传给上层。
 */
const RETRYABLE_CODES = new Set(['SERVER_ERROR', 'UPSTREAM_TIMEOUT', 'NETWORK_ERROR']);

/** 顶层异常兜底需要知道语言，main() 解析后写在这里。 */
let currentLang = 'zh';

/**
 * Bilingual error messages.
 */
const MESSAGES = {
  zh: {
    envMissingBase: '缺少环境变量 CHINA_TM_PLATFORM_BASE_URL',
    envMissingToken: '缺少环境变量 CHINA_TM_USER_TOKEN',
    httpsRequired: 'CHINA_TM_PLATFORM_BASE_URL 必须使用 HTTPS（设置 ALLOW_HTTP=true 可绕过）',
    allowHttpWarning: '警告：ALLOW_HTTP=true，平台 token 将以明文发送，仅可用于本地调试。',
    unknownCommand: (cmd) => `未知命令: ${cmd}`,
    queryEmpty: 'search --query 不能为空',
    queryTooLong: 'search --query 最长 200 个字符',
    optionValueMissing: (name) => `${name} 缺少取值（若取值以 -- 开头，请写成 ${name}=<值>）`,
    tmidEmpty: '--tmid 不能为空',
    searchMissingQuery: 'search 缺少 --query 参数',
    paginationNotSupported: '暂不支持翻页：每次查询固定返回第一页前 50 条，请细化查询关键词',
    pageSizeFixed: '提示：--pageSize 已忽略，平台固定返回 50 条。',
    detailMissingTmid: 'detail 缺少 --tmid 参数',
    exportMissingQueryId: 'export 缺少 --queryId 参数',
    exportMissingTmids: 'export 缺少 --tmids 参数',
    exportTmidsEmpty: 'export 的 --tmids 不能为空',
    exportStatusMissingJobId: 'export-status 缺少 --jobId 参数',
    exportPollHint: '任务尚未完成，请稍后再次执行 export-status 查询',
    requestTimeout: (ms) => `请求超时，已超过 ${ms}ms`,
    networkError: '平台接口不可达',
    positiveInteger: (field) => `${field} 必须是正整数`,
    badRequest: '请求参数错误',
    unauthorized: '认证失败，请检查平台 token 是否有效',
    paymentRequired: '点数不足，请先充值',
    forbidden: '当前用户无权访问该平台资源',
    notFound: '请求的资源不存在',
    upstreamTimeout: '平台处理超时',
    rateLimited: '请求过于频繁，请稍后再试',
    serverError: '平台内部错误，请稍后重试',
    httpError: (status) => `请求失败，HTTP ${status}`,
    unknownError: '发生未知错误',
    invalidJson: '平台返回了无法解析的 JSON',
    helpSummary: '中国商标查询 Skill CLI',
    legalDisclaimer: '商标查询结果仅供参考，不构成法律意见。',
    noteSearch: '查询前预计消耗 1 点（固定返回前 50 条，暂不支持翻页）',
    noteDetail: '详情前预计消耗 2 点（同一商标已购不重复扣点）',
    noteExport: '导出按条数阶梯扣点（重复 tmid 会自动去重）',
    noteTrial: '新注册组织赠送 100 点体验点（90 天有效），具体以平台返回为准',
    noteBind: '未绑定时请先执行 bind-help',
    retrying: (attempt, delay) => `第 ${attempt} 次重试，等待 ${delay}ms ...`,
  },
  en: {
    envMissingBase: 'Missing environment variable CHINA_TM_PLATFORM_BASE_URL',
    envMissingToken: 'Missing environment variable CHINA_TM_USER_TOKEN',
    httpsRequired: 'CHINA_TM_PLATFORM_BASE_URL must use HTTPS (set ALLOW_HTTP=true to bypass)',
    allowHttpWarning: 'Warning: ALLOW_HTTP=true, the platform token will be sent in cleartext. Local debugging only.',
    unknownCommand: (cmd) => `Unknown command: ${cmd}`,
    queryEmpty: 'search --query must not be empty',
    queryTooLong: 'search --query must be at most 200 characters',
    optionValueMissing: (name) => `${name} requires a value (use ${name}=<value> if the value starts with --)`,
    tmidEmpty: '--tmid must not be empty',
    searchMissingQuery: 'search requires --query argument',
    paginationNotSupported: 'Pagination is not supported: every search returns the first 50 results. Please refine the query.',
    pageSizeFixed: 'Note: --pageSize is ignored, the platform always returns 50 results.',
    detailMissingTmid: 'detail requires --tmid argument',
    exportMissingQueryId: 'export requires --queryId argument',
    exportMissingTmids: 'export requires --tmids argument',
    exportTmidsEmpty: 'export --tmids must not be empty',
    exportStatusMissingJobId: 'export-status requires --jobId argument',
    exportPollHint: 'The job is still running, run export-status again later',
    requestTimeout: (ms) => `Request timed out after ${ms}ms`,
    networkError: 'Platform API is unreachable',
    positiveInteger: (field) => `${field} must be a positive integer`,
    badRequest: 'Bad request parameters',
    unauthorized: 'Authentication failed, please check your platform token',
    paymentRequired: 'Not enough points, please top up first',
    forbidden: 'Current user does not have permission to access this resource',
    notFound: 'The requested resource does not exist',
    upstreamTimeout: 'Platform processing timed out',
    rateLimited: 'Too many requests, please try again later',
    serverError: 'Platform internal error, please try again later',
    httpError: (status) => `Request failed, HTTP ${status}`,
    unknownError: 'An unknown error occurred',
    invalidJson: 'Platform returned unparsable JSON',
    helpSummary: 'Chinese Trademark Search Skill CLI',
    legalDisclaimer: 'Trademark search results are for reference only, not legal advice.',
    noteSearch: 'Search costs an estimated 1 point (first 50 results, pagination not supported)',
    noteDetail: 'Detail lookup costs an estimated 2 points (no re-charge for already purchased trademarks)',
    noteExport: 'Export costs points based on item count tiers (duplicate tmids are de-duplicated)',
    noteTrial: 'New organizations get 100 trial points (valid for 90 days); the platform response is authoritative',
    noteBind: 'If not bound, run bind-help first',
    retrying: (attempt, delay) => `Retry #${attempt}, waiting ${delay}ms ...`,
  }
};

const COMMANDS = new Set([
  'help',
  'bind-help',
  'capabilities',
  'search',
  'detail',
  'export',
  'export-status',
  'modules'
]);

/**
 * Resolve the current language.
 */
function resolveLang(args) {
  const langVal = getOptionValue(args, '--lang');
  if (langVal === 'en') return 'en';
  return 'zh';
}

/**
 * Get message bundle for current language.
 */
function msg(lang) {
  return MESSAGES[lang] || MESSAGES.zh;
}

main().catch((error) => {
  writeError(normalizeUnknownError(error, currentLang));
});

/**
 * Main entry point.
 */
async function main() {
  const args = process.argv.slice(2);
  const rawCommand = args[0] || 'help';
  const command = rawCommand === '-h' || rawCommand === '--help' ? 'help' : rawCommand;
  const lang = resolveLang(args);
  currentLang = lang;
  const m = msg(lang);

  if (command === 'help') {
    return writeHelp(m, lang);
  }

  // 命令合法性先于环境变量校验：否则敲错命令只会看到“缺少环境变量”，误导排查方向。
  if (!COMMANDS.has(command)) {
    return writeError({
      code: 'UNKNOWN_COMMAND',
      message: m.unknownCommand(rawCommand)
    });
  }

  const env = readEnv(lang);

  switch (command) {
    case 'bind-help':
      return runBindHelp(env);
    case 'capabilities':
      return runCapabilities(env);
    case 'search':
      return runSearch(env, args.slice(1), lang);
    case 'detail':
      return runDetail(env, args.slice(1), lang);
    case 'export':
      return runExport(env, args.slice(1), lang);
    case 'export-status':
      return runExportStatus(env, args.slice(1), lang);
    case 'modules':
      return runModules(env);
    default:
      /* c8 ignore next */
      return writeError({ code: 'UNKNOWN_COMMAND', message: m.unknownCommand(rawCommand) });
  }
}

/**
 * Prints command help.
 */
function writeHelp(m, lang) {
  const en = lang === 'en';
  return writeJson({
    success: true,
    command: 'help',
    data: {
      summary: m.helpSummary,
      commands: [
        {
          name: 'help',
          usage: 'node scripts/cli.mjs help',
          description: en ? 'Show command help' : '输出命令帮助'
        },
        {
          name: 'bind-help',
          usage: 'node scripts/cli.mjs bind-help',
          description: en ? 'Read platform binding guide' : '读取平台绑定指引'
        },
        {
          name: 'capabilities',
          usage: 'node scripts/cli.mjs capabilities',
          description: en ? 'Read binding status, points balance, metering hints, and capabilities' : '读取绑定状态、点数余额、计费提示与能力信息'
        },
        {
          name: 'search',
          usage: 'node scripts/cli.mjs search --query "华源科技"',
          description: en ? 'Execute trademark search (always the first 50 results)' : '执行商标查询（固定返回前 50 条）'
        },
        {
          name: 'detail',
          usage: 'node scripts/cli.mjs detail --tmid "tm_20260310_0001"',
          description: en ? 'Read trademark details' : '读取指定商标详情'
        },
        {
          name: 'export',
          usage: 'node scripts/cli.mjs export --queryId "qry_001" --tmids "tm_001,tm_002"',
          description: en ? 'Create trademark export job' : '发起商标导出任务'
        },
        {
          name: 'export-status',
          usage: 'node scripts/cli.mjs export-status --jobId "exp_20260310_0003"',
          description: en ? 'Check export job status once (re-run later while still running)' : '查询一次导出任务状态（未完成时稍后重新执行）'
        },
        {
          name: 'modules',
          usage: 'node scripts/cli.mjs modules',
          description: en ? 'Read module capabilities' : '读取模块能力'
        }
      ],
      flags: [
        { name: '--lang', description: en ? 'Output language: en or zh (default zh)' : '输出语言: en 或 zh (默认 zh)', default: 'zh' }
      ],
      pagination: en
        ? 'Not supported. Every search returns the first 50 results; --page greater than 1 is rejected locally without charging.'
        : '暂不支持。每次查询固定返回第一页前 50 条；--page 大于 1 会在本地直接拒绝且不扣点。',
      environment: [
        'CHINA_TM_PLATFORM_BASE_URL',
        'CHINA_TM_USER_TOKEN',
        'CHINA_TM_TIMEOUT_MS',
        'CHINA_TM_SKILL_CHANNEL',
        'CHINA_TM_DEBUG',
        'ALLOW_HTTP'
      ],
      notes: [
        m.noteSearch,
        m.noteDetail,
        m.noteExport,
        m.noteTrial,
        m.noteBind
      ],
      legalDisclaimer: m.legalDisclaimer
    }
  });
}

// ---------------------------------------------------------------------------
// Input validation
// ---------------------------------------------------------------------------

/**
 * Validates a search query string.
 */
function validateQuery(q, lang) {
  const m_ = msg(lang);
  if (!q || typeof q !== 'string' || q.trim().length === 0) {
    throw createSkillError('ARGUMENT_INVALID', m_.queryEmpty);
  }
  const trimmed = q.trim();
  if (trimmed.length > 200) {
    throw createSkillError('ARGUMENT_INVALID', m_.queryTooLong);
  }
  return trimmed;
}

/**
 * Validates a trademark ID.
 */
function validateTmid(id, lang) {
  const m_ = msg(lang);
  if (!id || typeof id !== 'string' || id.trim().length === 0) {
    throw createSkillError('ARGUMENT_INVALID', m_.tmidEmpty);
  }
  return id.trim();
}

// ---------------------------------------------------------------------------
// Environment
// ---------------------------------------------------------------------------

/**
 * Reads required environment values.
 */
function readEnv(lang) {
  const m_ = msg(lang);
  const baseUrl = process.env.CHINA_TM_PLATFORM_BASE_URL;
  const token = process.env.CHINA_TM_USER_TOKEN;
  const timeoutMsRaw = process.env.CHINA_TM_TIMEOUT_MS;
  const channel = process.env.CHINA_TM_SKILL_CHANNEL || DEFAULT_CHANNEL;
  const allowHttp = process.env.ALLOW_HTTP === 'true';

  if (!baseUrl) {
    throw createSkillError('ENV_MISSING', m_.envMissingBase);
  }

  if (!token) {
    throw createSkillError('ENV_MISSING', m_.envMissingToken);
  }

  const timeoutMs = parsePositiveInteger(timeoutMsRaw, DEFAULT_TIMEOUT_MS, 'CHINA_TM_TIMEOUT_MS', lang);

  const normalizedBaseUrl = baseUrl.replace(/\/+$/, '');

  if (!/^https:\/\//i.test(normalizedBaseUrl)) {
    if (!allowHttp) {
      throw createSkillError('HTTPS_REQUIRED', m_.httpsRequired);
    }
    // baseUrl 完全由使用者控制，而每个请求都会带上 Bearer token；
    // 明文降级至少要让使用者在 stderr 上看见一次。
    process.stderr.write(`${m_.allowHttpWarning}\n`);
  }

  return {
    baseUrl: normalizedBaseUrl,
    token,
    timeoutMs,
    channel,
    lang,
    // 本次 CLI 调用的稳定幂等键：同一次命令内的自动重试复用同一 ID，
    // 平台按 X-OC-Request-Id 去重扣点，网络重试不会重复计费。
    requestId: `cli_${randomUUID().replace(/-/g, '')}`
  };
}

// ---------------------------------------------------------------------------
// Command runners
// ---------------------------------------------------------------------------

async function runBindHelp(env) {
  const data = await apiRequestWithRetry(env, 'GET', '/v1/openclaw/bind/help');
  writeJson({
    success: true,
    command: 'bind-help',
    data
  });
}

async function runCapabilities(env) {
  const data = await apiRequestWithRetry(env, 'GET', '/v1/openclaw/capabilities');
  writeJson({
    success: true,
    command: 'capabilities',
    data
  });
}

async function runSearch(env, argv, lang) {
  const m_ = msg(lang);
  const queryRaw = getOptionValue(argv, '--query');
  const pageRaw = getOptionValue(argv, '--page');
  const page = parsePositiveInteger(pageRaw, 1, '--page', lang);

  if (!queryRaw) {
    throw createSkillError('ARGUMENT_INVALID', m_.searchMissingQuery);
  }

  // 平台对 page>1 返回 400 PAGINATION_NOT_SUPPORTED；本地就拦掉，省一次往返。
  if (page > 1) {
    throw createSkillError('PAGINATION_NOT_SUPPORTED', m_.paginationNotSupported);
  }

  // pageSize 由平台固定为 50，保留参数只为兼容旧调用方，不再参与请求。
  if (getOptionValue(argv, '--pageSize') !== null) {
    process.stderr.write(`${m_.pageSizeFixed}\n`);
  }

  const query = validateQuery(queryRaw, lang);

  const body = {
    query,
    page: 1,
    pageSize: FIXED_PAGE_SIZE,
    channel: env.channel
  };

  const data = await apiRequestWithRetry(env, 'POST', '/v1/openclaw/trademarks/search', body);
  writeJson({
    success: true,
    command: 'search',
    data
  });
}

async function runDetail(env, argv, lang) {
  const m_ = msg(lang);
  const tmidRaw = getOptionValue(argv, '--tmid');

  if (!tmidRaw) {
    throw createSkillError('ARGUMENT_INVALID', m_.detailMissingTmid);
  }

  const tmid = validateTmid(tmidRaw, lang);

  const data = await apiRequestWithRetry(
    env,
    'GET',
    `/v1/openclaw/trademarks/${encodeURIComponent(tmid)}`
  );

  writeJson({
    success: true,
    command: 'detail',
    data
  });
}

async function runExport(env, argv, lang) {
  const m_ = msg(lang);
  const queryId = getOptionValue(argv, '--queryId');
  const tmidsRaw = getOptionValue(argv, '--tmids');

  if (!queryId) {
    throw createSkillError('ARGUMENT_INVALID', m_.exportMissingQueryId);
  }

  if (!tmidsRaw) {
    throw createSkillError('ARGUMENT_INVALID', m_.exportMissingTmids);
  }

  // 去重：导出按条数阶梯计价，重复 tmid 会把用户推进更贵的档。
  const selectedTmids = Array.from(
    new Set(
      tmidsRaw
        .split(',')
        .map((item) => item.trim())
        .filter(Boolean)
    )
  );

  if (selectedTmids.length === 0) {
    throw createSkillError('ARGUMENT_INVALID', m_.exportTmidsEmpty);
  }

  const body = {
    queryId,
    selectedTmids,
    channel: env.channel
  };

  const data = await apiRequestWithRetry(env, 'POST', '/v1/openclaw/trademarks/export', body);
  writeJson({
    success: true,
    command: 'export',
    data
  });
}

/**
 * Reads export job status once.
 *
 * 刻意不在 CLI 内轮询：每次调用是一次独立进程，长轮询会把 agent 卡住，
 * 未完成时由调用方稍后重新执行本命令（SKILL.md 的工作流即如此描述）。
 */
async function runExportStatus(env, argv, lang) {
  const m_ = msg(lang);
  const exportJobId = getOptionValue(argv, '--jobId');

  if (!exportJobId) {
    throw createSkillError('ARGUMENT_INVALID', m_.exportStatusMissingJobId);
  }

  const data = await apiRequestWithRetry(
    env,
    'GET',
    `/v1/openclaw/exports/${encodeURIComponent(exportJobId)}`
  );

  const pending = data && (data.status === 'processing' || data.status === 'queued');

  writeJson({
    success: true,
    command: 'export-status',
    data,
    ...(pending ? { pending: true, hint: m_.exportPollHint } : {})
  });
}

async function runModules(env) {
  const data = await apiRequestWithRetry(env, 'GET', '/v1/openclaw/modules');
  writeJson({
    success: true,
    command: 'modules',
    data
  });
}

// ---------------------------------------------------------------------------
// API request with retry
// ---------------------------------------------------------------------------

/**
 * Wraps apiRequest with backoff for retryable errors.
 */
async function apiRequestWithRetry(env, method, path, body) {
  let lastError;

  for (let attempt = 0; attempt <= MAX_RETRY_ATTEMPTS; attempt++) {
    try {
      return await apiRequest(env, method, path, body);
    } catch (error) {
      lastError = error;

      if (attempt < MAX_RETRY_ATTEMPTS && error && RETRYABLE_CODES.has(error.code)) {
        const delay = RETRY_DELAYS_MS[attempt];
        const m_ = msg(env.lang || 'zh');
        process.stderr.write(`${m_.retrying(attempt + 1, delay)}\n`);
        await sleep(delay);
        continue;
      }

      throw error;
    }
  }

  /* c8 ignore next */
  throw lastError;
}

/**
 * Sleeps for given milliseconds.
 */
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// ---------------------------------------------------------------------------
// Core API request
// ---------------------------------------------------------------------------

/**
 * Sends a request to the hosted platform API.
 */
async function apiRequest(env, method, path, body) {
  const m_ = msg(env.lang || 'zh');
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), env.timeoutMs);

  const headers = {
    'Accept': 'application/json',
    'Authorization': `Bearer ${env.token}`,
    'X-OC-Request-Id': env.requestId
  };

  if (body !== undefined) {
    headers['Content-Type'] = 'application/json';
  }

  const requestInit = {
    method,
    headers,
    signal: controller.signal
  };

  if (body !== undefined) {
    requestInit.body = JSON.stringify(body);
  }

  let response;
  let payload;
  try {
    response = await fetch(`${env.baseUrl}${path}`, requestInit);
    // 读 body 必须留在计时器里：先 clearTimeout 再读，响应体挂住就永远不超时。
    payload = await safeReadJson(response, env.lang);
  } catch (error) {
    if (error && (error.name === 'AbortError' || error.name === 'TimeoutError')) {
      throw createSkillError('UPSTREAM_TIMEOUT', m_.requestTimeout(env.timeoutMs));
    }

    throw createSkillError('NETWORK_ERROR', m_.networkError);
  } finally {
    clearTimeout(timeoutId);
  }

  if (response.ok) {
    return payload;
  }

  throw mapHttpError(response, payload, env.lang);
}

// ---------------------------------------------------------------------------
// Utility functions
// ---------------------------------------------------------------------------

/**
 * Parses a positive integer with fallback.
 */
function parsePositiveInteger(rawValue, fallbackValue, fieldName, lang) {
  if (rawValue === undefined || rawValue === null || rawValue === '') {
    return fallbackValue;
  }

  const m_ = msg(lang || 'zh');
  const value = Number(rawValue);
  if (!Number.isInteger(value) || value <= 0) {
    throw createSkillError('ARGUMENT_INVALID', m_.positiveInteger(fieldName));
  }
  return value;
}

/**
 * Gets a CLI option value: `--query abc` or `--query=abc`.
 *
 * 取值以 `--` 开头时视为“漏了取值”而不是取值本身 —— 早先 `search --query --page 1`
 * 会真的拿 "--page" 当关键词查询并扣掉 1 点。确需以 -- 开头的取值请用 `--query=--x`。
 */
function getOptionValue(argv, optionName) {
  for (let index = 0; index < argv.length; index++) {
    const token = argv[index];

    if (token === optionName) {
      const next = argv[index + 1];
      if (next === undefined || /^--[A-Za-z]/.test(next)) return null;
      return next;
    }

    if (typeof token === 'string' && token.startsWith(`${optionName}=`)) {
      return token.slice(optionName.length + 1);
    }
  }
  return null;
}

/**
 * Reads JSON safely. Falls back to text if needed.
 */
async function safeReadJson(response, lang) {
  const m_ = msg(lang || 'zh');
  const contentType = response.headers.get('content-type') || '';
  const text = await response.text();

  if (!text) {
    return {};
  }

  if (contentType.includes('application/json')) {
    try {
      return JSON.parse(text);
    } catch {
      return {
        success: false,
        error: {
          code: 'INVALID_JSON',
          message: m_.invalidJson
        },
        raw: text
      };
    }
  }

  // Fallback: some platforms may return JSON without correct content-type; try parsing.
  // If that fails, wrap the raw text as a message to ensure the host always gets a structured object.
  try {
    return JSON.parse(text);
  } catch {
    return {
      message: text
    };
  }
}

/**
 * Maps HTTP status and platform payload into a structured error.
 *
 * 平台在错误体里带的附加字段（402 的 rechargeUrl、失败退点的 refundedPoints 等）
 * 必须一路透传到 stdout：SKILL.md 要求 agent 直接把 rechargeUrl 给用户，
 * 早先只取 code/message，这些字段全被吞掉了。
 */
function mapHttpError(response, payload, lang) {
  const m_ = msg(lang || 'zh');
  const status = response.status;
  const platformError = payload && typeof payload === 'object' ? payload.error : null;
  const platformCode = platformError && typeof platformError.code === 'string' ? platformError.code : null;
  const platformMessage = platformError && typeof platformError.message === 'string' ? platformError.message : null;

  const details = { httpStatus: status };

  if (platformError && typeof platformError === 'object') {
    for (const [key, value] of Object.entries(platformError)) {
      if (key !== 'code' && key !== 'message') details[key] = value;
    }
  }

  // 自动退点的金额在响应体顶层，不在 error 内。
  if (payload && typeof payload === 'object' && payload.refundedPoints !== undefined) {
    details.refundedPoints = payload.refundedPoints;
  }

  if (status === 429) {
    const retryAfter = response.headers.get('retry-after');
    if (retryAfter) details.retryAfterSeconds = Number(retryAfter) || retryAfter;
  }

  if (platformCode && platformMessage) {
    return createSkillError(platformCode, platformMessage, details);
  }

  switch (status) {
    case 400:
      return createSkillError('BAD_REQUEST', readMessage(payload, m_.badRequest), details);
    case 401:
      return createSkillError('UNAUTHORIZED', m_.unauthorized, details);
    case 402:
      return createSkillError('POINTS_NOT_ENOUGH', readMessage(payload, m_.paymentRequired), details);
    case 403:
      return createSkillError('FORBIDDEN', m_.forbidden, details);
    case 404:
      return createSkillError('NOT_FOUND', m_.notFound, details);
    case 408:
      return createSkillError('UPSTREAM_TIMEOUT', m_.upstreamTimeout, details);
    case 429:
      return createSkillError('RATE_LIMITED', m_.rateLimited, details);
    case 500:
    case 502:
    case 503:
    case 504:
      return createSkillError('SERVER_ERROR', readMessage(payload, m_.serverError), details);
    default:
      return createSkillError('HTTP_ERROR', readMessage(payload, m_.httpError(status)), details);
  }
}

/**
 * Reads a human message from payload.
 */
function readMessage(payload, fallback) {
  if (!payload || typeof payload !== 'object') return fallback;
  if (typeof payload.message === 'string' && payload.message.trim()) return payload.message;
  if (payload.error && typeof payload.error.message === 'string' && payload.error.message.trim()) {
    return payload.error.message;
  }
  return fallback;
}

/**
 * Creates a known skill error.
 */
function createSkillError(code, message, details) {
  const error = new Error(message);
  error.code = code;
  if (details && Object.keys(details).length > 0) {
    error.details = details;
  }
  return error;
}

/**
 * Converts unknown exceptions into skill error objects.
 *
 * 已知的 skill error 原样透出；未知异常（真 bug）保留 message，
 * 并在 CHINA_TM_DEBUG=true 时附带 stack —— 否则线上只剩一个无信息的 UNKNOWN_ERROR。
 */
function normalizeUnknownError(error, lang) {
  const m_ = msg(lang || 'zh');

  if (error && typeof error === 'object' && typeof error.code === 'string' && typeof error.message === 'string') {
    return {
      code: error.code,
      message: error.message,
      details: error.details
    };
  }

  const details = {};
  if (error && typeof error.message === 'string' && error.message.trim()) {
    details.reason = error.message;
  }
  if (process.env.CHINA_TM_DEBUG === 'true' && error && typeof error.stack === 'string') {
    details.stack = error.stack;
  }

  return {
    code: 'UNKNOWN_ERROR',
    message: m_.unknownError,
    details: Object.keys(details).length > 0 ? details : undefined
  };
}

/**
 * Prints a successful JSON result.
 */
function writeJson(payload) {
  process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`);
}

/**
 * Prints a structured error JSON result.
 */
function writeError(error) {
  process.stdout.write(
    `${JSON.stringify(
      {
        success: false,
        error: {
          code: error.code,
          message: error.message,
          ...(error.details ?? {})
        }
      },
      null,
      2
    )}\n`
  );
  process.exitCode = 1;
}
