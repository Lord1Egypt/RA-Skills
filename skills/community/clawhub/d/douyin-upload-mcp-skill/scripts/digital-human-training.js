#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';

const HOME = process.env.HOME || '.';
const STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(HOME, '.openclaw', 'workspace', 'douyin-ops');
const STATE_PATH = process.env.DOUYIN_DIGITAL_HUMAN_STATE_PATH || join(STATE_DIR, 'digital-human-state.json');
const MARKETING_STATE_PATH = process.env.DOUYIN_MARKETING_STATE_PATH || join(STATE_DIR, 'automation-marketing-state.json');
const PERSONA_STATE_PATH = process.env.DOUYIN_PERSONA_STATE_PATH || join(STATE_DIR, 'persona-state.json');
const SKILL_ENV_PATH = new URL('../.env', import.meta.url).pathname;
const SKILL_LOCAL_ENV_PATH = new URL('../.env.local', import.meta.url).pathname;
const XIAOICE_ENV_PATH = process.env.XIAOICE_VIDEO_ENV_PATH || join(HOME, '自动营销', 'xiaoice-video-tool', '.env');

const DEFAULT_API_BASE_URL = 'https://openapi.xiaoice.com/vh';
const DEFAULT_COZE_API_BASE_URL = 'https://api.coze.cn';
const DEFAULT_COZE_WORKFLOW_ID = '';
const DEFAULT_DIGITAL_HUMAN_MODEL_ID = 'CVHPZJ4LCGBMNIZULS0';
const DEFAULT_AUTH_FILE_URL = 'https://livestream-data.oss-cn-beijing.aliyuncs.com/ai-marketing/WX20251031-105434%402x.png';
const CREATE_PATH = '/openapi/customize/zero/commit';
const QUALITY_PATH = '/openapi/customize/zero/get-ckq-result';
const START_TRAINING_PATH = '/openapi/customize/zero/start-training';
const TRAINING_RESULT_PATH = '/openapi/customize/zero/get-training-result';

const VOICE_IDS = {
  girl: 'VH_XIAOBING_zh-CN_new_ptts_F51421-KChhxTlJa8pJbHpV',
  female: 'MINIMAX_minimax-9e78bbb5c0fb4f829a8d17a4a5b51e7c_Rs9oxQiQ',
  matureFemale: 'MINIMAX_minimax-51d0912f08f9416085361bbe984cca43-Y5LxfQcUznK60gcF',
  boy: '211-shaoniannanyin-xin-VFQC',
  male: 'MINIMAX_minimax-f4cca1eb321b485190a11ee5953b66c9-n1gzDqUIUr3AFIvS',
  matureMale: 'VH_XIAOBING_en-US_new_ptts_M29246-PBF8BHdsNtLpD1iH',
};

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith('--')) {
      args._.push(item);
      continue;
    }
    const key = item.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) args[key] = true;
    else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

function parseFirstJsonObject(text) {
  const raw = String(text || '');
  let depth = 0;
  let start = -1;
  let inString = false;
  let escaped = false;
  for (let i = 0; i < raw.length; i += 1) {
    const ch = raw[i];
    if (inString) {
      if (escaped) escaped = false;
      else if (ch === '\\') escaped = true;
      else if (ch === '"') inString = false;
      continue;
    }
    if (ch === '"') inString = true;
    else if (ch === '{') {
      if (depth === 0) start = i;
      depth += 1;
    } else if (ch === '}') {
      depth -= 1;
      if (depth === 0 && start >= 0) return JSON.parse(raw.slice(start, i + 1));
    }
  }
  throw new Error('json_object_not_found');
}

function readJson(path, fallback) {
  try {
    if (!existsSync(path)) return fallback;
    return parseFirstJsonObject(readFileSync(path, 'utf8'));
  } catch {
    return fallback;
  }
}

function writeJson(path, value) {
  mkdirSync(dirname(path), { recursive: true });
  const tempPath = `${path}.tmp-${process.pid}-${Date.now()}`;
  writeFileSync(tempPath, `${JSON.stringify(value, null, 2)}\n`);
  renameSync(tempPath, path);
}

function loadEnvFile(path) {
  if (!existsSync(path)) return {};
  const env = {};
  for (const rawLine of readFileSync(path, 'utf8').split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#') || !line.includes('=')) continue;
    const index = line.indexOf('=');
    const key = line.slice(0, index).trim();
    let value = line.slice(index + 1).trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    if (key) env[key] = value;
  }
  return env;
}

function mergedEnv() {
  return { ...loadEnvFile(SKILL_ENV_PATH), ...loadEnvFile(SKILL_LOCAL_ENV_PATH), ...loadEnvFile(XIAOICE_ENV_PATH), ...process.env };
}

function loadState() {
  return readJson(STATE_PATH, {
    version: 2,
    status: 'idle',
    lastJob: null,
  });
}

function saveState(state) {
  writeJson(STATE_PATH, { ...state, version: 2, updatedAt: new Date().toISOString() });
}

function loadPersona() {
  return readJson(PERSONA_STATE_PATH, {});
}

function loadMarketing() {
  return readJson(MARKETING_STATE_PATH, {});
}

function saveMarketing(state) {
  writeJson(MARKETING_STATE_PATH, state);
}

function normalizeComparable(value) {
  return String(value || '').trim();
}

function currentPersonaFingerprint(persona = loadPersona()) {
  const confirmed = persona.confirmed || null;
  const fields = confirmed?.fields || persona.fields || {};
  return {
    confirmed: Boolean(confirmed),
    confirmedAt: normalizeComparable(confirmed?.confirmedAt),
    name: normalizeComparable(fields.name),
    photo: normalizeComparable(fields.photo || fields.photoUrl),
  };
}

function personaFingerprintMatches(a = {}, b = {}) {
  if (!a.confirmed || !b.confirmed) return false;
  if (a.confirmedAt && b.confirmedAt && a.confirmedAt !== b.confirmedAt) return false;
  if (a.photo && b.photo && a.photo !== b.photo) return false;
  if (a.name && b.name && a.name !== b.name) return false;
  return Boolean(a.confirmedAt || a.photo || a.name);
}

function jobMatchesCurrentPersona(job, persona = loadPersona()) {
  if (!job?.personaSnapshot?.confirmed) return false;
  return personaFingerprintMatches(job.personaSnapshot.fingerprint || {}, currentPersonaFingerprint(persona));
}

function currentModelId() {
  const marketing = loadMarketing();
  const env = mergedEnv();
  return String(
    marketing.digitalHuman?.modelId
    || process.env.DIGITAL_HUMAN_MODEL_ID
    || process.env.VIRTUALMAN_MODEL_ID
    || process.env.VIDEO_PROVIDER_VH_BIZ_ID
    || env.VIDEO_PROVIDER_VH_BIZ_ID
    || env.VIDEO_PROVIDER_MODEL_ID
    || ''
  ).trim();
}

function defaultModelId() {
  const env = mergedEnv();
  return String(
    process.env.DOUYIN_DEFAULT_DIGITAL_HUMAN_ID
    || env.DOUYIN_DEFAULT_DIGITAL_HUMAN_ID
    || currentModelId()
    || DEFAULT_DIGITAL_HUMAN_MODEL_ID
  ).trim();
}

function useCozeWorkflow(args = {}) {
  if (args.useCoze || args.coze || args.realCoze) return true;
  if (args.skipCoze || args.defaultModel || args.useDefaultModel) return false;
  const env = mergedEnv();
  const skip = String(process.env.DIGITAL_HUMAN_SKIP_COZE || env.DIGITAL_HUMAN_SKIP_COZE || '').trim();
  if (/^(true|1|yes)$/i.test(skip)) return false;
  const use = String(process.env.DIGITAL_HUMAN_USE_COZE || env.DIGITAL_HUMAN_USE_COZE || '').trim();
  if (/^(false|0|no)$/i.test(use)) return false;
  return true;
}

function trainingConfig() {
  const env = mergedEnv();
  return {
    apiBaseUrl: String(
      process.env.DIGITAL_HUMAN_TRAINING_API_BASE_URL
      || env.DIGITAL_HUMAN_TRAINING_API_BASE_URL
      || env.XIAOICE_DIGITAL_HUMAN_API_BASE_URL
      || DEFAULT_API_BASE_URL
    ).trim().replace(/\/+$/, ''),
    apiKey: String(
      process.env.DIGITAL_HUMAN_TRAINING_API_KEY
      || env.DIGITAL_HUMAN_TRAINING_API_KEY
      || env.XIAOICE_DIGITAL_HUMAN_API_KEY
      || env.XIAOICE_SUBSCRIPTION_KEY
      || env.VIDEO_PROVIDER_API_KEY
      || ''
    ).trim(),
    authHeader: String(
      process.env.DIGITAL_HUMAN_TRAINING_AUTH_HEADER
      || env.DIGITAL_HUMAN_TRAINING_AUTH_HEADER
      || env.VIDEO_PROVIDER_AUTH_HEADER
      || 'subscription-key'
    ).trim(),
    createPath: String(process.env.DIGITAL_HUMAN_TRAINING_CREATE_PATH || env.DIGITAL_HUMAN_TRAINING_CREATE_PATH || CREATE_PATH).trim(),
    qualityPath: String(process.env.DIGITAL_HUMAN_TRAINING_QUALITY_PATH || env.DIGITAL_HUMAN_TRAINING_QUALITY_PATH || QUALITY_PATH).trim(),
    startTrainingPath: String(process.env.DIGITAL_HUMAN_TRAINING_START_PATH || env.DIGITAL_HUMAN_TRAINING_START_PATH || START_TRAINING_PATH).trim(),
    trainingResultPath: String(process.env.DIGITAL_HUMAN_TRAINING_RESULT_PATH || env.DIGITAL_HUMAN_TRAINING_RESULT_PATH || TRAINING_RESULT_PATH).trim(),
  };
}

function cozeConfig() {
  const env = mergedEnv();
  return {
    apiBaseUrl: String(
      process.env.DIGITAL_HUMAN_COZE_API_BASE_URL
      || process.env.COZE_API_BASE_URL
      || env.DIGITAL_HUMAN_COZE_API_BASE_URL
      || env.COZE_API_BASE_URL
      || DEFAULT_COZE_API_BASE_URL
    ).trim().replace(/\/+$/, ''),
    token: String(
      process.env.DIGITAL_HUMAN_COZE_TOKEN
      || process.env.COZE_API_TOKEN
      || process.env.COZE_TOKEN
      || env.DIGITAL_HUMAN_COZE_TOKEN
      || env.COZE_API_TOKEN
      || env.COZE_TOKEN
      || ''
    ).trim(),
    workflowId: String(
      process.env.DIGITAL_HUMAN_COZE_WORKFLOW_ID
      || process.env.COZE_WORKFLOW_ID
      || env.DIGITAL_HUMAN_COZE_WORKFLOW_ID
      || env.COZE_WORKFLOW_ID
      || DEFAULT_COZE_WORKFLOW_ID
    ).trim(),
  };
}

function missingConfig(config = trainingConfig()) {
  const missing = [];
  if (!config.apiBaseUrl) missing.push('DIGITAL_HUMAN_TRAINING_API_BASE_URL');
  if (!config.apiKey) missing.push('DIGITAL_HUMAN_TRAINING_API_KEY 或 VIDEO_PROVIDER_API_KEY');
  if (!config.authHeader) missing.push('DIGITAL_HUMAN_TRAINING_AUTH_HEADER');
  return missing;
}

function missingCozeConfig(config = cozeConfig()) {
  const missing = [];
  if (!config.apiBaseUrl) missing.push('COZE_API_BASE_URL');
  if (!config.token) missing.push('COZE_API_TOKEN');
  if (!config.workflowId) missing.push('COZE_WORKFLOW_ID');
  return missing;
}

function statusLabel(status) {
  if (status < 0) return 'failed';
  if (status === 0 || status === 2) return 'running';
  if (status === 1 || status === 3) return 'succeeded';
  return 'unknown';
}

function publicUrl(value) {
  return /^https?:\/\/\S+$/i.test(String(value || '').trim());
}

function normalizeVhModelType(value) {
  const raw = String(value || '').trim().toUpperCase();
  if (raw === '交互' || raw === 'INTERACTIVE') return 'INTERACTIVE';
  return 'STUDIO';
}

function parseMaybeInt(value) {
  if (value === undefined || value === null || value === '') return undefined;
  const n = Number(value);
  return Number.isFinite(n) ? n : undefined;
}

function cleanUrlFromMatch(value) {
  return String(value || '')
    .trim()
    .replace(/[，。；;、)）\]}】]+$/g, '')
    .replace(/^["'“”‘’]+|["'“”‘’]+$/g, '');
}

function matchLabeledUrl(text, labels) {
  const label = labels.map((item) => item.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|');
  const pattern = new RegExp(`(?:${label})\\s*[:：=]?\\s*(https?:\\/\\/[^\\s"'<>]+)`, 'i');
  const match = String(text || '').match(pattern);
  return cleanUrlFromMatch(match?.[1] || '');
}

function matchTextField(text, labels, maxLen = 80) {
  const escaped = labels.map((item) => item.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  const pattern = new RegExp(`^\\s*(?:${escaped.join('|')})\\s*(?:[:：=]|是)\\s*([^\\n，,；;]{1,${maxLen}})\\s*$`, 'i');
  for (const line of String(text || '').split(/\r?\n|[；;]/)) {
    const match = line.match(pattern);
    if (match) return String(match[1] || '').trim().replace(/^["'“”‘’]+|["'“”‘’]+$/g, '');
  }
  return '';
}

function parseTrainingRequestFromText(text) {
  const raw = String(text || '').trim();
  const trainingVideoUrl = matchLabeledUrl(raw, ['训练视频地址', '训练视频链接', '训练视频', 'trainingVideoUrl', 'training_video_url']);
  const photoUrl = matchLabeledUrl(raw, ['照片链接', '本人照片', '形象照片', '头像照片', '头像', '照片', 'photoUrl', 'photo', 'image']);
  const authVideoUrl = matchLabeledUrl(raw, ['授权视频地址', '授权视频链接', '授权视频', 'authVideoUrl', 'auth_video_url']);
  const authFileUrl = matchLabeledUrl(raw, ['授权文件地址', '授权文件链接', '授权文件', '授权书', 'authFileUrl', 'auth_file_url']);
  const name = matchTextField(raw, ['数字人名称', '形象名称', '训练名称', '名字', 'name'], 16);
  const sex = matchTextField(raw, ['性别', 'sex'], 8);
  const age = matchTextField(raw, ['年龄', 'age'], 8);
  const vhModelTypeRaw = matchTextField(raw, ['数字人工作场景', '工作场景', '场景', 'vhModelType'], 16);
  const languageTypeRaw = matchTextField(raw, ['语言类型', 'languageType'], 16);
  const voiceBizId = matchTextField(raw, ['声音bizId', '声音ID', 'voiceBizId'], 80);
  const request = {
    vhModelType: normalizeVhModelType(vhModelTypeRaw),
    trainingVideoUrl,
    photoUrl,
    authVideoUrl,
    authFileUrl,
    name,
    sex,
    age,
    voiceBizId,
    languageType: /multi|多语言/i.test(languageTypeRaw) ? 'MULTI' : (/chinese|普通话|中文/i.test(languageTypeRaw) ? 'CHINESE' : ''),
    voiceTemplateVersion: parseMaybeInt(matchTextField(raw, ['voiceTemplateVersion', '声音模板版本'], 4)),
    reduceNoise: parseMaybeInt(matchTextField(raw, ['reduceNoise', '降噪'], 4)),
  };
  if (!request.voiceTemplateVersion && /全程讲话|10\s*(?:秒|s).*(?:30\s*min|30\s*分钟)/i.test(raw)) {
    request.voiceTemplateVersion = 1;
  }
  return request;
}

function requestFromArgs(args = {}) {
  return {
    vhModelType: normalizeVhModelType(args.vhModelType || args.modelType || 'STUDIO'),
    trainingVideoUrl: String(args.trainingVideoUrl || args.trainingVideo || '').trim(),
    photoUrl: String(args.photoUrl || args.photo || args.image || '').trim(),
    authVideoUrl: String(args.authVideoUrl || args.authVideo || '').trim(),
    authFileUrl: String(args.authFileUrl || args.authFile || '').trim(),
    name: String(args.name || args.humanName || args.digitalHumanName || '').trim(),
    sex: String(args.sex || '').trim(),
    age: String(args.age || '').trim(),
    voiceBizId: String(args.voiceBizId || '').trim(),
    languageType: String(args.languageType || '').trim(),
    voiceTemplateVersion: parseMaybeInt(args.voiceTemplateVersion),
    reduceNoise: parseMaybeInt(args.reduceNoise),
  };
}

function mergeRequest(primary, fallback) {
  const out = { ...fallback };
  for (const [key, value] of Object.entries(primary || {})) {
    if (value !== '' && value !== undefined && value !== null) out[key] = value;
  }
  return out;
}

function validateCreateRequest(request) {
  const missing = [];
  if (!publicUrl(request.trainingVideoUrl)) missing.push('训练视频链接');
  return missing;
}

function validateStartTrainingRequest(request) {
  const missing = [];
  if (!request.name || request.name.length > 16) missing.push('数字人名称（16字以内）');
  return missing;
}

function collectMessage(missing = []) {
  const need = missing.length ? `还缺：${missing.join('、')}。\n` : '';
  return `${need}请先完成人设确认，并发送本人正面清晰照片链接。\n可直接这样回：照片：https://example.com/photo.jpg`;
}

function safeConfig(config = trainingConfig()) {
  return {
    apiBaseUrl: config.apiBaseUrl,
    authHeader: config.authHeader,
    createPath: config.createPath,
    qualityPath: config.qualityPath,
    startTrainingPath: config.startTrainingPath,
    trainingResultPath: config.trainingResultPath,
    hasApiKey: Boolean(config.apiKey),
  };
}

function safeCozeConfig(config = cozeConfig()) {
  return {
    apiBaseUrl: config.apiBaseUrl,
    workflowId: config.workflowId,
    hasToken: Boolean(config.token),
  };
}

function endpoint(config, path) {
  const base = config.apiBaseUrl.replace(/\/+$/, '');
  const cleanPath = String(path || '').startsWith('/') ? String(path) : `/${path}`;
  return `${base}${cleanPath}`;
}

async function requestJson(path, options = {}) {
  const config = trainingConfig();
  const method = options.method || 'GET';
  let url = endpoint(config, path);
  const headers = {
    [config.authHeader]: config.apiKey,
    'Content-Type': 'application/json',
  };
  let body;
  if (method === 'GET' && options.query) {
    const params = new URLSearchParams(options.query);
    url = `${url}${url.includes('?') ? '&' : '?'}${params.toString()}`;
  } else if (options.body) {
    body = JSON.stringify(options.body);
  }
  const response = await fetch(url, {
    method,
    headers,
    body,
    signal: AbortSignal.timeout(Number(options.timeoutMs || 60000)),
  });
  const text = await response.text();
  let payload = {};
  try {
    payload = text ? JSON.parse(text) : {};
  } catch {
    payload = { rawText: text };
  }
  if (!response.ok || Number(payload.code) !== 200) {
    const err = new Error(payload.message || payload.rawText || `HTTP ${response.status}`);
    err.status = response.status;
    err.payload = payload;
    throw err;
  }
  return payload;
}

function tryParseJson(text) {
  const raw = String(text || '').trim();
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    try {
      return parseFirstJsonObject(raw);
    } catch {
      return null;
    }
  }
}

function parseCozeStream(text) {
  const events = [];
  let currentEvent = null;
  let currentData = [];
  const flush = () => {
    if (!currentData.length) {
      currentEvent = null;
      return;
    }
    const data = currentData.join('\n').trim();
    currentData = [];
    if (!data || data === '[DONE]') {
      currentEvent = null;
      return;
    }
    const parsed = tryParseJson(data);
    if (parsed) events.push(parsed);
    else if (currentEvent && currentEvent !== 'PING') events.push({ event: currentEvent, rawText: data });
    currentEvent = null;
  };
  for (const rawLine of String(text || '').split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line) {
      flush();
      continue;
    }
    if (line.startsWith('event:')) {
      currentEvent = line.slice(6).trim();
      continue;
    }
    if (line.startsWith('data:')) {
      currentData.push(line.slice(5).trim());
      continue;
    }
    if (line.startsWith('id:') || line.startsWith('retry:')) continue;
    const parsed = tryParseJson(line);
    if (parsed) events.push(parsed);
  }
  flush();
  const whole = tryParseJson(text);
  if (whole) events.push(whole);
  return events;
}

function walkValues(value, visitor, path = []) {
  if (Array.isArray(value)) {
    value.forEach((item, index) => walkValues(item, visitor, [...path, String(index)]));
    return;
  }
  if (value && typeof value === 'object') {
    for (const [key, item] of Object.entries(value)) walkValues(item, visitor, [...path, key]);
    return;
  }
  visitor(value, path);
}

function extractUrlsFromText(text) {
  return [...String(text || '').matchAll(/https?:\/\/[^\s"'<>\\]+/gi)]
    .map((match) => cleanUrlFromMatch(match[0]))
    .filter(Boolean);
}

function extractCozeOutput(text, events = []) {
  const urls = [];
  const keyed = {};
  const candidates = [...events];
  for (const event of events) {
    for (const key of ['data', 'content', 'message', 'output']) {
      const nested = typeof event?.[key] === 'string' ? tryParseJson(event[key]) : null;
      if (nested) candidates.push(nested);
    }
  }
  for (const candidate of candidates) {
    walkValues(candidate, (value, path) => {
      if (typeof value !== 'string') return;
      for (const url of extractUrlsFromText(value)) {
        urls.push(url);
        const keyPath = path.join('.').toLowerCase();
        if (/video|训练|training/.test(keyPath)) keyed.trainingVideoUrl ||= url;
        if (/avatar|head|头像/.test(keyPath)) keyed.avatarUrl ||= url;
        if (/口播|mouth|poster|cover|photo|image|照片|图片/.test(keyPath)) keyed.mouthPhotoUrl ||= url;
      }
    });
  }
  for (const url of extractUrlsFromText(text)) urls.push(url);
  const uniqueUrls = [...new Set(urls)];
  const videoUrl = keyed.trainingVideoUrl
    || uniqueUrls.find((url) => /\.(mp4|mov|webm|m4v)(?:[?#].*)?$/i.test(url))
    || uniqueUrls.find((url) => /video|\.mp4|\.mov|\.webm/i.test(url))
    || '';
  const imageUrls = uniqueUrls.filter((url) => /\.(jpg|jpeg|png|webp)(?:[?#].*)?$/i.test(url) || /image|photo|img|byteimg/i.test(url));
  return {
    trainingVideoUrl: videoUrl,
    avatarUrl: keyed.avatarUrl || imageUrls[0] || '',
    mouthPhotoUrl: keyed.mouthPhotoUrl || imageUrls[1] || keyed.avatarUrl || imageUrls[0] || '',
    urls: uniqueUrls,
    rawEvents: events.slice(-5),
  };
}

function findCozeError(events = []) {
  for (const event of events) {
    const code = event?.error_code || event?.code;
    const message = String(event?.error_message || event?.message || event?.error || '').trim();
    if (code || message) {
      return {
        code,
        message,
        debugUrl: event?.debug_url || '',
      };
    }
  }
  return null;
}

async function runCozeWorkflow(input, args = {}) {
  const config = cozeConfig();
  const missing = missingCozeConfig(config);
  if (missing.length && !args.dryRun) {
    return {
      ok: false,
      action: 'digital_human_coze_missing_config',
      missing,
      config: safeCozeConfig(config),
      customerMessage: '形象视频生成接口还没配置好，请先检查 Coze token 和工作流 ID。',
    };
  }
  if (args.dryRun) {
    const stamp = Date.now();
    return {
      ok: true,
      dryRun: true,
      action: 'digital_human_coze_succeeded',
      output: {
        trainingVideoUrl: `https://example.com/coze-training-${stamp}.mp4`,
        avatarUrl: input.photo,
        mouthPhotoUrl: input.photo,
        urls: [`https://example.com/coze-training-${stamp}.mp4`, input.photo].filter(Boolean),
      },
    };
  }
  const response = await fetch(`${config.apiBaseUrl}/v1/workflow/stream_run`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${config.token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      workflow_id: config.workflowId,
      parameters: input,
    }),
    signal: AbortSignal.timeout(Number(args.cozeTimeoutMs || process.env.DIGITAL_HUMAN_COZE_TIMEOUT_MS || 300000)),
  });
  const text = await response.text();
  const events = parseCozeStream(text);
  const output = extractCozeOutput(text, events);
  const cozeError = findCozeError(events);
  if (!response.ok) {
    const err = new Error(`coze_http_${response.status}`);
    err.payload = { status: response.status, sample: text.slice(0, 500) };
    throw err;
  }
  if (cozeError) {
    const isRateLimit = /RPM|rate|limit|频率|限流|too many/i.test(cozeError.message);
    const err = new Error(isRateLimit ? 'coze_rate_limited' : 'coze_workflow_error');
    err.payload = { error: cozeError, urls: output.urls };
    err.customerMessage = isRateLimit
      ? '形象视频生成接口当前触发了 Coze 调用频率限制，请稍后重试，或让管理员提高工作流/API限额。'
      : `形象视频生成工作流执行失败：${cozeError.message || cozeError.code || '请管理员检查 Coze 工作流执行日志'}`;
    throw err;
  }
  if (!publicUrl(output.trainingVideoUrl)) {
    const err = new Error('coze_training_video_url_not_found');
    err.payload = { events: events.slice(-3), urls: output.urls };
    err.customerMessage = '形象视频生成流程已执行，但 Coze 工作流没有返回训练视频链接。请联系管理员检查工作流输出节点/字段名，确认会输出 video 或 trainingVideoUrl。';
    throw err;
  }
  return { ok: true, action: 'digital_human_coze_succeeded', output };
}

function bindMarketingModel(modelId, patch = {}) {
  const clean = String(modelId || '').trim();
  if (!clean) return null;
  const state = loadMarketing();
  const persona = loadPersona();
  const fingerprint = patch.personaFingerprint || currentPersonaFingerprint(persona);
  const personaConfirmedAt = patch.personaConfirmedAt || fingerprint.confirmedAt || '';
  const next = {
    ...state,
    digitalHuman: {
      ...(state.digitalHuman || {}),
      modelId: clean,
      source: patch.source || 'trained',
      trainingTaskBizId: patch.trainingTaskBizId || state.digitalHuman?.trainingTaskBizId || '',
      personaConfirmedAt,
      personaFingerprint: fingerprint,
      personaName: fingerprint.name || '',
      personaPhoto: fingerprint.photo || '',
      boundAt: new Date().toISOString(),
      confirmedAt: new Date().toISOString(),
    },
    updatedAt: new Date().toISOString(),
  };
  saveMarketing(next);
  return next.digitalHuman;
}

function defaultModelJob(request, snapshot, args = {}) {
  const modelId = defaultModelId();
  const bizId = `default-model-${Date.now()}`;
  const job = {
    ...newJob(bizId, request, 'succeeded'),
    personaSnapshot: snapshot,
    quality: { status: 1, progress: 100, message: null, skipped: true },
    training: { status: 1, progress: 100, message: null, bizId: modelId, skipped: true },
    digitalHumanBizId: modelId,
    skippedCoze: true,
    skippedProviderTraining: true,
    source: args.dryRun ? 'default_dry_run' : 'default_model',
  };
  saveState({ ...loadState(), status: 'succeeded', lastJob: job });
  bindMarketingModel(modelId, {
    source: args.dryRun ? 'default_dry_run' : 'default',
    trainingTaskBizId: bizId,
    personaFingerprint: snapshot.fingerprint,
    personaConfirmedAt: snapshot.fingerprint?.confirmedAt || '',
  });
  return {
    ok: true,
    dryRun: Boolean(args.dryRun),
    action: 'digital_human_training_succeeded',
    job,
    customerMessage: '数字人生成完成，ID已绑定。当前使用默认数字人ID降级测试，没有调用 Coze 工作流。现在可以回复：开启自动化营销',
  };
}

function textFromSection(value) {
  if (!value) return '';
  if (typeof value === 'string') return value.trim();
  if (Array.isArray(value)) return value.map(textFromSection).filter(Boolean).join('\n');
  if (typeof value === 'object') {
    return Object.entries(value)
      .map(([key, item]) => {
        const text = textFromSection(item);
        return text ? `${key}：${text}` : '';
      })
      .filter(Boolean)
      .join('\n');
  }
  return String(value).trim();
}

function personaSnapshot(persona = loadPersona()) {
  const confirmed = persona.confirmed || null;
  const fields = confirmed?.fields || persona.fields || {};
  const output = [
    confirmed?.strategy,
    confirmed?.marketing,
    confirmed?.customerPersona ? `精准用户画像：\n${textFromSection(confirmed.customerPersona)}` : '',
    confirmed?.accountProfile ? `账号资料：\n${textFromSection(confirmed.accountProfile)}` : '',
  ].filter(Boolean).join('\n\n');
  return {
    confirmed: Boolean(confirmed),
    confirmedAt: confirmed?.confirmedAt || '',
    fields,
    summary: confirmed?.summary || null,
    fingerprint: currentPersonaFingerprint(persona),
    output: output || textFromSection(confirmed || persona.draft || fields),
  };
}

function recommendVoice(fields = {}, personaText = '') {
  const sex = String(fields.sex || '').trim();
  const age = Number(String(fields.age || '').match(/\d{1,3}/)?.[0] || 0);
  const combined = `${personaText}\n${fields.trials || ''}\n${fields.bissiness || ''}`;
  const mature = age >= 40 || /成熟|阅历|专家|老板|企业|管理|资深|深耕|年/.test(combined);
  const young = age > 0 && age <= 20;
  if (/女|female/i.test(sex)) return young ? VOICE_IDS.girl : (mature ? VOICE_IDS.matureFemale : VOICE_IDS.female);
  if (/男|male/i.test(sex)) return young ? VOICE_IDS.boy : (mature ? VOICE_IDS.matureMale : VOICE_IDS.male);
  return mature ? VOICE_IDS.matureMale : VOICE_IDS.male;
}

function buildPersonaDrivenRequest(partial = {}) {
  const snapshot = personaSnapshot();
  const fields = snapshot.fields || {};
  const photoUrl = partial.photoUrl || fields.photo || fields.photoUrl || '';
  const name = partial.name || fields.name || '数字人';
  const sex = partial.sex || fields.sex || '';
  const age = partial.age || fields.age || '';
  const voiceBizId = partial.voiceBizId || recommendVoice({ ...fields, sex, age }, snapshot.output);
  return {
    request: {
      vhModelType: partial.vhModelType || 'STUDIO',
      trainingVideoUrl: partial.trainingVideoUrl || '',
      photoUrl,
      authFileUrl: partial.authFileUrl || DEFAULT_AUTH_FILE_URL,
      authVideoUrl: partial.authVideoUrl || '',
      name: String(name).trim().slice(0, 16) || '数字人',
      sex,
      age,
      voiceBizId,
      languageType: partial.languageType || 'CHINESE',
      voiceTemplateVersion: partial.voiceTemplateVersion ?? 1,
      reduceNoise: partial.reduceNoise,
    },
    personaSnapshot: snapshot,
  };
}

function validatePersonaDrivenRequest(request, snapshot) {
  const missing = [];
  if (!snapshot.confirmed) missing.push('已确认人设');
  if (!publicUrl(request.photoUrl)) missing.push('本人照片链接');
  if (!request.name || request.name.length > 16) missing.push('数字人名称（16字以内）');
  return missing;
}

function normalizeCreatePayload(request) {
  const body = {
    vhModelType: request.vhModelType || 'STUDIO',
    trainingVideoUrl: request.trainingVideoUrl,
    authFileUrl: request.authFileUrl || DEFAULT_AUTH_FILE_URL,
    skipVoiceCheck: request.skipVoiceCheck === undefined ? 1 : Number(request.skipVoiceCheck),
    voiceTemplateVersion: request.voiceTemplateVersion === undefined ? 1 : Number(request.voiceTemplateVersion),
  };
  if (request.authVideoUrl) body.authVideoUrl = request.authVideoUrl;
  return body;
}

function normalizeStartPayload(bizId, request) {
  const body = {
    bizId,
    name: request.name,
  };
  if (request.voiceBizId) body.voiceBizId = request.voiceBizId;
  if (request.languageType) body.languageType = request.languageType;
  if (request.reduceNoise !== undefined) body.reduceNoise = Number(request.reduceNoise);
  return body;
}

function newJob(bizId, request, status = 'quality_running') {
  return {
    bizId,
    status,
    request,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };
}

async function createFromPersona(args = {}, partial = {}) {
  const { request, personaSnapshot: snapshot } = buildPersonaDrivenRequest(mergeRequest(requestFromArgs(args), partial));
  const missing = validatePersonaDrivenRequest(request, snapshot);
  if (missing.length) {
    return {
      ok: true,
      action: 'digital_human_training_collect_needed',
      missing,
      customerMessage: collectMessage(missing),
    };
  }
  if (!useCozeWorkflow(args)) return defaultModelJob(request, snapshot, args);
  const cozeJob = {
    ...newJob(`coze-${Date.now()}`, request, 'coze_running'),
    personaSnapshot: snapshot,
  };
  saveState({ ...loadState(), status: 'coze_running', lastJob: cozeJob });
  const coze = await runCozeWorkflow({
    persona: JSON.stringify({ output: snapshot.output }),
    photo: request.photoUrl,
    sex: request.sex || snapshot.fields?.sex || '',
  }, args);
  if (coze.ok === false) return coze;
  const trainingVideoUrl = coze.output.trainingVideoUrl;
  const createRequest = {
    ...request,
    trainingVideoUrl,
    cozeOutput: {
      trainingVideoUrl,
      avatarUrl: coze.output.avatarUrl || '',
      mouthPhotoUrl: coze.output.mouthPhotoUrl || '',
      urls: coze.output.urls || [],
    },
  };
  if (args.cozeOnly) {
    const job = {
      ...newJob(`coze-only-${Date.now()}`, createRequest, 'coze_succeeded'),
      personaSnapshot: snapshot,
      coze: coze.output,
      dryRun: Boolean(args.dryRun),
    };
    saveState({ ...loadState(), status: 'coze_succeeded', lastJob: job });
    return {
      ok: true,
      action: 'digital_human_coze_succeeded',
      job,
      customerMessage: '形象训练视频已生成。继续训练请回复：训练数字人',
    };
  }
  return createTask(createRequest, {
    ...args,
    personaSnapshot: snapshot,
    cozeOutput: coze.output,
  });
}

async function createTask(request, args = {}) {
  const missing = validateCreateRequest(request);
  if (missing.length) {
    return {
      ok: true,
      action: 'digital_human_training_collect_needed',
      missing,
      customerMessage: collectMessage(missing),
    };
  }
  const nameMissing = validateStartTrainingRequest(request);
  if (nameMissing.length) {
    return {
      ok: true,
      action: 'digital_human_training_collect_needed',
      missing: nameMissing,
      customerMessage: collectMessage(nameMissing),
    };
  }
  const configMissing = missingConfig();
  if (configMissing.length && !args.dryRun) {
    return {
      ok: false,
      action: 'digital_human_training_missing_config',
      missing: configMissing,
      config: safeConfig(),
      customerMessage: '数字人训练接口还没配置好，请先检查小冰 subscription-key 和接口地址。',
    };
  }
  if (args.dryRun) {
    const bizId = `dry-customize-${Date.now()}`;
    const modelId = `dry-vh-${Date.now()}`;
    const job = {
      ...newJob(bizId, request, 'succeeded'),
      personaSnapshot: args.personaSnapshot || null,
      coze: args.cozeOutput || request.cozeOutput || null,
      quality: { status: 1, progress: 100, message: null },
      training: { status: 1, progress: 100, message: null, bizId: modelId },
      digitalHumanBizId: modelId,
      dryRun: true,
    };
    saveState({ ...loadState(), status: 'succeeded', lastJob: job });
    bindMarketingModel(modelId, {
      source: 'trained_dry_run',
      trainingTaskBizId: bizId,
      personaFingerprint: job.personaSnapshot?.fingerprint,
      personaConfirmedAt: job.personaSnapshot?.fingerprint?.confirmedAt || '',
    });
    return {
      ok: true,
      dryRun: true,
      action: 'digital_human_training_succeeded',
      job,
      customerMessage: '数字人生成完成，ID已绑定。现在可以回复：开启自动化营销',
    };
  }
  const payload = await requestJson(trainingConfig().createPath, {
    method: 'POST',
    body: normalizeCreatePayload(request),
  });
  const bizId = String(payload.data || '').trim();
  if (!bizId) throw new Error('create_task_missing_biz_id');
  const job = newJob(bizId, request, 'quality_running');
  if (args.personaSnapshot) job.personaSnapshot = args.personaSnapshot;
  if (args.cozeOutput || request.cozeOutput) job.coze = args.cozeOutput || request.cozeOutput;
  saveState({ ...loadState(), status: 'quality_running', lastJob: job });
  return {
    ok: true,
    action: 'digital_human_training_created',
    job,
    provider: { code: payload.code, traceId: payload.traceId || '' },
    customerMessage: '数字人定制任务已创建，正在质检。稍后回复：查看数字人训练',
  };
}

async function checkQuality(job, args = {}) {
  if (args.dryRun || job.dryRun) {
    const next = {
      ...job,
      status: 'quality_passed',
      quality: { status: 1, progress: 100, message: null },
      updatedAt: new Date().toISOString(),
    };
    saveState({ ...loadState(), status: next.status, lastJob: next });
    return { ok: true, action: 'digital_human_quality_passed', job: next, customerMessage: '质检通过，准备启动训练。' };
  }
  const payload = await requestJson(trainingConfig().qualityPath, {
    method: 'GET',
    query: { bizId: job.bizId },
  });
  const data = payload.data || {};
  const label = statusLabel(Number(data.status));
  const next = {
    ...job,
    status: label === 'succeeded' ? 'quality_passed' : (label === 'failed' ? 'failed' : 'quality_running'),
    quality: {
      status: Number(data.status),
      progress: Number(data.progress || 0),
      message: data.message || payload.message || null,
    },
    updatedAt: new Date().toISOString(),
  };
  saveState({ ...loadState(), status: next.status, lastJob: next });
  if (next.status === 'failed') {
    return {
      ok: false,
      action: 'digital_human_quality_failed',
      job: next,
      customerMessage: `数字人质检未通过：${next.quality.message || '请重新上传符合要求的视频'}`,
    };
  }
  if (next.status === 'quality_passed') {
    return { ok: true, action: 'digital_human_quality_passed', job: next, customerMessage: '质检通过，准备启动训练。' };
  }
  return {
    ok: true,
    action: 'digital_human_quality_running',
    job: next,
    customerMessage: `数字人质检中：${next.quality.progress || 0}%。稍后回复：查看数字人训练`,
  };
}

async function startTraining(job, args = {}) {
  const missing = validateStartTrainingRequest(job.request || {});
  if (missing.length) {
    return {
      ok: true,
      action: 'digital_human_training_collect_needed',
      missing,
      customerMessage: collectMessage(missing),
    };
  }
  if (args.dryRun || job.dryRun) {
    const next = {
      ...job,
      status: 'training_running',
      trainingStart: { result: true, estimateMinutes: 10 },
      updatedAt: new Date().toISOString(),
    };
    saveState({ ...loadState(), status: next.status, lastJob: next });
    return { ok: true, action: 'digital_human_training_started', job: next, customerMessage: '数字人训练已启动，预计 10 分钟。稍后回复：查看数字人训练' };
  }
  const payload = await requestJson(trainingConfig().startTrainingPath, {
    method: 'POST',
    body: normalizeStartPayload(job.bizId, job.request || {}),
  });
  const data = payload.data || {};
  if (data.result !== true) throw new Error(payload.message || 'start_training_failed');
  const next = {
    ...job,
    status: 'training_running',
    trainingStart: {
      result: Boolean(data.result),
      estimateMinutes: Number(data.estimateMinutes || 0),
    },
    updatedAt: new Date().toISOString(),
  };
  saveState({ ...loadState(), status: next.status, lastJob: next });
  return {
    ok: true,
    action: 'digital_human_training_started',
    job: next,
    provider: { code: payload.code, traceId: payload.traceId || '' },
    customerMessage: `数字人训练已启动，预计 ${next.trainingStart.estimateMinutes || 10} 分钟。稍后回复：查看数字人训练`,
  };
}

async function checkTraining(job, args = {}) {
  if (args.dryRun || job.dryRun) {
    const modelId = job.digitalHumanBizId || `dry-vh-${Date.now()}`;
    const next = {
      ...job,
      status: 'succeeded',
      training: { status: 1, progress: 100, message: null, bizId: modelId },
      digitalHumanBizId: modelId,
      updatedAt: new Date().toISOString(),
    };
    saveState({ ...loadState(), status: next.status, lastJob: next });
    bindMarketingModel(modelId, {
      source: 'trained_dry_run',
      trainingTaskBizId: job.bizId,
      personaFingerprint: next.personaSnapshot?.fingerprint,
      personaConfirmedAt: next.personaSnapshot?.fingerprint?.confirmedAt || '',
    });
    return { ok: true, action: 'digital_human_training_succeeded', job: next, customerMessage: '数字人生成完成，ID已绑定。现在可以回复：开启自动化营销' };
  }
  const payload = await requestJson(trainingConfig().trainingResultPath, {
    method: 'POST',
    body: { bizId: job.bizId },
  });
  const data = payload.data || {};
  const label = statusLabel(Number(data.status));
  const modelId = String(data.bizId || '').trim();
  const next = {
    ...job,
    status: label === 'succeeded' ? 'succeeded' : (label === 'failed' ? 'failed' : 'training_running'),
    training: {
      status: Number(data.status),
      progress: Number(data.progress || 0),
      message: data.message || payload.message || null,
      bizId: modelId || null,
    },
    digitalHumanBizId: modelId || job.digitalHumanBizId || '',
    updatedAt: new Date().toISOString(),
  };
  saveState({ ...loadState(), status: next.status, lastJob: next });
  if (next.status === 'failed') {
    return {
      ok: false,
      action: 'digital_human_training_failed',
      job: next,
      customerMessage: `数字人训练失败：${next.training.message || '请重新发送清晰照片后重试'}`,
    };
  }
  if (next.status === 'succeeded') {
    bindMarketingModel(next.digitalHumanBizId, {
      source: 'trained',
      trainingTaskBizId: job.bizId,
      personaFingerprint: next.personaSnapshot?.fingerprint,
      personaConfirmedAt: next.personaSnapshot?.fingerprint?.confirmedAt || '',
    });
    return {
      ok: true,
      action: 'digital_human_training_succeeded',
      job: next,
      provider: { code: payload.code, traceId: payload.traceId || '' },
      customerMessage: '数字人生成完成，ID已绑定。现在可以回复：开启自动化营销',
    };
  }
  return {
    ok: true,
    action: 'digital_human_training_running',
    job: next,
    customerMessage: `数字人训练中：${next.training.progress || 0}%。稍后回复：查看数字人训练`,
  };
}

async function advance(args = {}) {
  const state = loadState();
  const job = state.lastJob;
  if (!job?.bizId) {
    return {
      ok: true,
      action: 'digital_human_training_collect_needed',
      customerMessage: collectMessage(),
    };
  }
  if (job.status === 'quality_running' || job.status === 'created') {
    const quality = await checkQuality(job, args);
    if (quality.job?.status === 'quality_passed') return startTraining(quality.job, args);
    return quality;
  }
  if (job.status === 'quality_passed') return startTraining(job, args);
  if (job.status === 'training_running' || job.status === 'training_started') return checkTraining(job, args);
  if (job.status === 'succeeded') {
    if (!jobMatchesCurrentPersona(job)) {
      return createFromPersona(args);
    }
    if (job.digitalHumanBizId) {
      bindMarketingModel(job.digitalHumanBizId, {
        source: job.dryRun ? 'trained_dry_run' : 'trained',
        trainingTaskBizId: job.bizId,
        personaFingerprint: job.personaSnapshot?.fingerprint,
        personaConfirmedAt: job.personaSnapshot?.fingerprint?.confirmedAt || '',
      });
    }
    return {
      ok: true,
      action: 'digital_human_training_already_succeeded',
      job,
      customerMessage: '数字人已生成并绑定。现在可以回复：开启自动化营销',
    };
  }
  return {
    ok: false,
    action: 'digital_human_training_failed',
    job,
    customerMessage: `上一次数字人训练失败：${job.quality?.message || job.training?.message || '请重新发送清晰照片后重试'}`,
  };
}

function status() {
  const state = loadState();
  const persona = loadPersona();
  const config = trainingConfig();
  const missing = missingConfig(config);
  const modelId = currentModelId();
  const job = state.lastJob;
  const lines = [
    `形象训练接口：${missing.length ? '未完整配置' : '已配置'}`,
    `形象视频接口：${missingCozeConfig().length ? '未完整配置' : '已配置'}`,
    `人设：${persona.confirmed ? '已确认' : '未完成'}`,
    `数字人ID：${modelId ? '已绑定' : '未绑定'}`,
  ];
  if (job?.status === 'coze_running') lines.push('当前任务：正在生成形象训练视频');
  else if (job?.status === 'quality_running') lines.push(`当前任务：质检中 ${job.quality?.progress || 0}%`);
  else if (job?.status === 'training_running') lines.push(`当前任务：训练中 ${job.training?.progress || 0}%`);
  else if (job?.status === 'succeeded') lines.push('当前任务：已完成');
  else if (job?.status === 'failed') lines.push('当前任务：失败，可重新提交');
  if (!modelId) lines.push('请先确认人设并发送照片，再回复：训练数字人；已有ID可回复：绑定数字人ID xxxxx');
  return {
    ok: true,
    action: 'digital_human_training_status',
    statePath: STATE_PATH,
    configured: missing.length === 0,
    missing,
    config: safeConfig(config),
    cozeConfig: safeCozeConfig(),
    modelIdConfigured: Boolean(modelId),
    state,
    customerMessage: lines.join('\n'),
  };
}

async function createFromArgs(args = {}) {
  const request = requestFromArgs(args);
  return createTask(request, args);
}

async function routeText(text, args = {}) {
  const raw = String(text || '').trim();
  if (/^(形象状态|数字人状态|查看形象定制|数字人训练状态)$/.test(raw)) return status();
  if (/^(查看数字人训练|检查数字人训练|训练进度|质检结果|训练结果|继续训练)$/.test(raw)) return advance(args);
  const parsed = parseTrainingRequestFromText(raw);
  if (/^(训练数字人|生成数字人形象|上传照片训练|上传视频训练|形象定制)$/.test(raw) || parsed.photoUrl) {
    const current = loadState();
    if (!parsed.photoUrl && current.lastJob?.bizId && ['created', 'quality_running', 'quality_passed', 'training_running', 'training_started'].includes(String(current.lastJob.status || ''))) {
      return advance(args);
    }
    if (!parsed.photoUrl && current.lastJob?.status === 'succeeded') {
      return advance(args);
    }
    return createFromPersona(args, parsed);
  }
  if (parsed.trainingVideoUrl || parsed.authVideoUrl || parsed.authFileUrl) {
    return createTask(parsed, args);
  }
  return {
    ok: true,
    action: 'digital_human_training_usage',
    customerMessage: '支持：训练数字人、查看数字人训练、数字人状态。已有数字人ID也可以回复：绑定数字人ID xxxxx',
  };
}

async function main() {
  const [command = 'status', ...rest] = process.argv.slice(2);
  const args = parseArgs(rest);
  let output;
  if (command === 'status') output = status();
  else if (command === 'create') output = await createFromArgs(args);
  else if (command === 'create-from-persona') output = await createFromPersona(args);
  else if (command === 'advance') output = await advance(args);
  else if (command === 'route-text') {
    const textRequest = parseTrainingRequestFromText(args.text || args._.join(' '));
    const argRequest = requestFromArgs(args);
    const merged = mergeRequest(argRequest, textRequest);
    if (merged.photoUrl && !merged.trainingVideoUrl) {
      output = await createFromPersona(args, merged);
    } else if (merged.trainingVideoUrl || merged.authVideoUrl || merged.authFileUrl) {
      output = await createTask(merged, args);
    } else {
      output = await routeText(args.text || args._.join(' '), args);
    }
  } else {
    output = {
      ok: false,
      error: 'unknown_command',
      usage: 'digital-human-training.js status|create|advance|route-text',
    };
  }
  console.log(JSON.stringify(output, null, 2));
  if (output.ok === false) process.exitCode = 1;
}

main().catch((err) => {
  console.log(JSON.stringify({
    ok: false,
    error: err.message,
    payload: err.payload || null,
    customerMessage: err.customerMessage || '数字人训练接口调用失败，请检查人设、照片链接或稍后重试。',
  }, null, 2));
  process.exit(1);
});
