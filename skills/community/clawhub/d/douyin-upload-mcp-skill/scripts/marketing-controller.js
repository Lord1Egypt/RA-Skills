#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { sendFeishuText } from './feishu-client.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(process.env.HOME || '.', '.openclaw', 'workspace', 'douyin-ops');
const STATE_PATH = process.env.DOUYIN_MARKETING_STATE_PATH || join(STATE_DIR, 'automation-marketing-state.json');
const PERSONA_STATE_PATH = process.env.DOUYIN_PERSONA_STATE_PATH || join(STATE_DIR, 'persona-state.json');
const SCHEDULE_CONFIG_PATH = join(STATE_DIR, 'schedule-config.json');
const DEFAULT_DAILY_TIME = process.env.DOUYIN_MARKETING_DAILY_TIME || '07:30';
const XIAOICE_ENV_PATH = process.env.XIAOICE_VIDEO_ENV_PATH || join(process.env.HOME || '.', '自动营销', 'xiaoice-video-tool', '.env');
const DEFAULT_DIGITAL_HUMAN_MODEL_ID = 'CVHPZJ4LCGBMNIZULS0';
const DIGITAL_HUMAN_ROUTE_TIMEOUT_MS = Number(process.env.DIGITAL_HUMAN_ROUTE_TIMEOUT_MS || 1_500_000);
const XIAOICE_VIDEO_TIMEOUT_SEC = Number(process.env.XIAOICE_VIDEO_TIMEOUT_SEC || 1800);
const IN_FLIGHT_PLAN_STALE_MS = Number(process.env.DOUYIN_IN_FLIGHT_PLAN_STALE_MS || 10 * 60 * 1000);
const IN_FLIGHT_VIDEO_STALE_MS = Number(process.env.DOUYIN_IN_FLIGHT_VIDEO_STALE_MS || 60 * 60 * 1000);

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
      if (depth === 0 && start >= 0) {
        return JSON.parse(raw.slice(start, i + 1));
      }
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

function loadState() {
  return readJson(STATE_PATH, {
    version: 1,
    enabled: false,
    publishMode: 'manual_confirm',
    confirmationMode: 'manual',
    schedule: { dailyTime: DEFAULT_DAILY_TIME },
    digitalHuman: {},
    lastRun: null,
  });
}

function marketingDailyTimeFromConfig() {
  const config = readJson(SCHEDULE_CONFIG_PATH, {});
  return String(config.jobs?.marketingDaily?.schedule?.time || '').trim();
}

function normalizeState(state = {}) {
  if (!state.confirmationMode) state.confirmationMode = state.publishMode === 'auto_confirm' ? 'auto' : 'manual';
  if (!state.publishMode) state.publishMode = confirmationMode(state) === 'auto' ? 'auto_confirm' : 'manual_confirm';
  const configuredTime = marketingDailyTimeFromConfig();
  const dailyTime = configuredTime || state.schedule?.dailyTime || DEFAULT_DAILY_TIME;
  state.schedule = { ...(state.schedule || {}), dailyTime };
  return state;
}

function saveState(state) {
  writeJson(STATE_PATH, { ...state, updatedAt: new Date().toISOString() });
}

function patchState(patch) {
  const current = loadState();
  const next = {
    ...current,
    ...patch,
    updatedAt: new Date().toISOString(),
  };
  writeJson(STATE_PATH, next);
  return next;
}

function loadPersona() {
  return readJson(PERSONA_STATE_PATH, {});
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

function digitalHumanMatchesCurrentPersona(digitalHuman = {}, persona = loadPersona()) {
  if (!digitalHuman?.modelId) return false;
  const expected = currentPersonaFingerprint(persona);
  const actual = digitalHuman.personaFingerprint || {
    confirmed: Boolean(digitalHuman.personaConfirmedAt || digitalHuman.personaName || digitalHuman.personaPhoto),
    confirmedAt: normalizeComparable(digitalHuman.personaConfirmedAt),
    name: normalizeComparable(digitalHuman.personaName),
    photo: normalizeComparable(digitalHuman.personaPhoto),
  };
  if (digitalHuman.source === 'customer' && !actual.confirmed) return true;
  if (digitalHuman.source === 'customer') return personaFingerprintMatches(actual, expected);
  return personaFingerprintMatches(actual, expected);
}

function compactText(value, maxLength = 220) {
  if (!value) return '';
  let text = '';
  if (typeof value === 'string') text = value;
  else if (Array.isArray(value)) text = value.map((item) => compactText(item, maxLength)).filter(Boolean).join('；');
  else if (typeof value === 'object') {
    text = Object.entries(value)
      .map(([key, item]) => {
        const child = compactText(item, maxLength);
        return child ? `${key}：${child}` : '';
      })
      .filter(Boolean)
      .join('；');
  } else {
    text = String(value);
  }
  return cleanTrailingPunctuation(text.replace(/\s+/g, ' ').trim().slice(0, maxLength));
}

function shortPhrase(value, maxLength = 32) {
  const text = compactText(value, maxLength * 2);
  const first = text.split(/[、，,。；;！!？?\n]/).map((item) => item.trim()).find(Boolean) || text;
  return cleanTrailingPunctuation(first.slice(0, maxLength).trim());
}

function cleanTrailingPunctuation(value) {
  return String(value || '').replace(/[、，,；;：:\s]+$/u, '').trim();
}

function revisionFeedbackFromText(value, prefixes = ['不通过', '不满意', '重新生成视频', '重做视频', '重新成片']) {
  const raw = String(value || '').trim();
  if (!raw) return '';
  const escaped = prefixes.map((item) => item.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|');
  return raw.replace(new RegExp(`^(${escaped})\\s*[，,。:：-]?\\s*`, 'u'), '').trim();
}

function explicitForbiddenTitlePrefixes(feedback = '', fields = {}) {
  const text = String(feedback || '').trim();
  if (!text) return [];
  const values = [];
  for (const pattern of [
    /标题[^，。；;！!？?\n]{0,20}(?:不要|别|去掉|删掉|不写|不能写|不要写)[^，。；;！!？?\n]{0,8}["“”']?([^"“”'，。；;！!？?\n]{1,16}[：:])["“”']?/u,
    /(?:不要|别|去掉|删掉|不写|不能写|不要写)[^，。；;！!？?\n]{0,8}["“”']?([^"“”'，。；;！!？?\n]{1,16}[：:])["“”']?/u,
  ]) {
    const match = text.match(pattern)?.[1];
    if (match) values.push(match);
  }
  const name = shortPhrase(fields.name || '', 10);
  if (name && (
    new RegExp(`(?:不要|别|去掉|删掉|不写|不能写|不要写)[\\s\\S]{0,12}${name}[：:]`, 'u').test(text)
    || new RegExp(`(?:不要|别|去掉|删掉|不写|不能写|不要写)[\\s\\S]{0,12}${name}`, 'u').test(text)
  )) {
    values.push(`${name}：`, `${name}:`);
  }
  return [...new Set(values.map((item) => String(item || '').trim()).filter(Boolean))];
}

function applyTitleRevisionFeedback(title, feedback = '', fields = {}) {
  let next = String(title || '').trim();
  const prefixes = explicitForbiddenTitlePrefixes(feedback, fields);
  for (const prefix of prefixes) {
    if (next.startsWith(prefix)) next = next.slice(prefix.length).trim();
  }
  if (/(标题|文案).*(?:不要|别|去掉|删掉|不写|不能写|不要写).*(姓名|名字|人名)/u.test(feedback)) {
    const name = shortPhrase(fields.name || '', 10);
    if (name) next = next.replace(new RegExp(`^${name}[：:]\\s*`, 'u'), '').trim();
  }
  return cleanTrailingPunctuation(next || title);
}

function sentenceLimit(value, maxLength = 26) {
  const text = cleanTrailingPunctuation(compactText(value, maxLength * 2));
  if (!text) return '';
  const chars = Array.from(text);
  if (chars.length <= maxLength) return text;
  const head = chars.slice(0, maxLength).join('');
  const softIndex = Math.max(
    head.lastIndexOf('，'),
    head.lastIndexOf(','),
    head.lastIndexOf('、'),
    head.lastIndexOf('；'),
    head.lastIndexOf(';'),
  );
  if (softIndex >= 10) return cleanTrailingPunctuation(head.slice(0, softIndex));
  return cleanTrailingPunctuation(head);
}

function businessKeyword(value, maxLength = 16) {
  const raw = compactText(value, maxLength * 3)
    .replace(/^面向[^，,。；;、]{1,12}提供/u, '')
    .replace(/^(主营|主要做|提供|从事|经营)/u, '')
    .replace(/解决[^，,。；;、]{0,40}$/u, '')
    .trim();
  return shortPhrase(raw || value, maxLength);
}

function audienceLabel(value, fallback = '客户') {
  const text = compactText(value, 120);
  if (!text) return fallback;
  const segments = text
    .split(/[，,。；;！!？?\n]/)
    .map((item) => item
      .replace(/^.*?(?:等地区的|等地的|地区的)/u, '')
      .replace(/^(遇到|需要|想要|希望).*/u, '')
      .trim())
    .filter(Boolean);
  const direct = segments.find((item) => /种植户|客户|用户|商家|企业主|创业者|老板|车主|宠物主|养宠人|家长|学生|宝妈|家庭/u.test(item));
  const raw = direct || segments[0] || text;
  return shortPhrase(raw, 14) || fallback;
}

function problemLabel(value, fallback = '') {
  const text = compactText(value, 140);
  const match = text.match(/(?:遇到|解决|改善|处理)([^，。；;！!？?\n]{2,40})/u);
  const source = match?.[1] || text;
  const pieces = source
    .replace(/等问题.*$/u, '')
    .replace(/^受/u, '')
    .replace(/困扰$/u, '')
    .split(/[、，,和及]/)
    .map((item) => item.replace(/问题$/u, '').trim())
    .filter((item) => item && !/^(大棚)?种植(农户|户)$|^客户$|^用户$/.test(item))
    .slice(0, 2);
  return pieces.length ? pieces.join('、') : fallback;
}

function stripTitleDecorations(value) {
  return String(value || '')
    .replace(/^[^：:\n]{1,10}[：:]/u, '')
    .replace(/[#"'“”‘’《》【】（）()\[\]]/g, '')
    .replace(/\s+/g, '')
    .trim();
}

function safeVisualTitle(value, fallback = '今日重点') {
  const raw = stripTitleDecorations(value)
    .replace(/怎么少踩坑|如何少踩坑|怎样少踩坑|怎么避坑|如何避坑|怎样避坑/gu, '避坑')
    .replace(/避坑指南$/u, '避坑');
  const chars = Array.from(raw);
  if (!chars.length) return fallback;
  if (chars.length >= 4 && chars.length <= 8) return raw;
  const keywordPatterns = [
    /散光膜/u,
    /棚膜/u,
    /农膜/u,
    /宠物险/u,
    /宠物保险/u,
    /保险/u,
    /自动回复/u,
    /数据分析/u,
    /自动营销/u,
    /数字人/u,
  ];
  for (const pattern of keywordPatterns) {
    const match = raw.match(pattern)?.[0];
    if (match) {
      const suffix = /坑|踩坑|避坑/u.test(raw) ? '避坑' : (/指南|技巧|方案/u.test(raw) ? '指南' : '重点');
      const title = `${match}${suffix}`;
      if (Array.from(title).length <= 8) return title;
      if (Array.from(match).length >= 4 && Array.from(match).length <= 8) return match;
    }
  }
  const preferred = [
    /[^，。！？!?、：:\s]{2,6}(?:避坑|指南|技巧|重点|方案|提醒)/u,
    /(?:少踩坑|别踩坑|避坑|选对方案|实用建议)/u,
  ];
  for (const pattern of preferred) {
    const match = raw.match(pattern)?.[0];
    if (match && Array.from(match).length <= 8) return match;
  }
  const compact = raw
    .replace(/高温|强光|专用|专业|核心|主营|服务|顾问|怎么|如何|怎样|什么|哪些|哪个|为什么/gu, '')
    .replace(/[？?！!。]/g, '');
  const compactChars = Array.from(compact);
  if (compactChars.length >= 2) {
    const head = compactChars.slice(0, Math.min(6, compactChars.length)).join('');
    const withSuffix = `${head}${/坑/u.test(raw) ? '避坑' : ''}`;
    if (Array.from(withSuffix).length >= 4 && Array.from(withSuffix).length <= 8) return withSuffix;
    if (Array.from(head).length >= 4 && Array.from(head).length <= 8) return head;
  }
  return chars.slice(0, 8).join('');
}

function safeCoverText(value, fallback = '今日重点') {
  const title = safeVisualTitle(value, fallback);
  if (/指南|避坑|技巧|重点|方案/u.test(title)) return title;
  const withGuide = `${title}指南`;
  return Array.from(withGuide).length <= 12 ? withGuide : title;
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

function runNode(args, opts = {}) {
  const result = spawnSync(process.execPath, args, {
    cwd: ROOT,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: Number(opts.timeout || 180000),
    env: { ...process.env, ...(opts.env || {}) },
  });
  const output = `${result.stderr || ''}${result.stdout || ''}`.trim();
  return {
    ok: result.status === 0,
    status: result.status,
    signal: result.signal,
    output,
    payload: parseLastJson(output),
  };
}

function parseJsonObjects(text) {
  const objects = [];
  let depth = 0;
  let start = -1;
  let inString = false;
  let escaped = false;
  const raw = String(text || '');
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
      if (depth === 0 && start >= 0) {
        try {
          objects.push(JSON.parse(raw.slice(start, i + 1)));
        } catch {
          // Ignore logs.
        }
        start = -1;
      }
    }
  }
  return objects;
}

function parseLastJson(text) {
  return parseJsonObjects(text).at(-1) || null;
}

function currentModelId(state = loadState()) {
  const xiaoiceEnv = loadEnvFile(XIAOICE_ENV_PATH);
  return String(
    state.digitalHuman?.modelId
    || process.env.DIGITAL_HUMAN_MODEL_ID
    || process.env.VIRTUALMAN_MODEL_ID
    || process.env.VIDEO_PROVIDER_VH_BIZ_ID
    || xiaoiceEnv.VIDEO_PROVIDER_VH_BIZ_ID
    || xiaoiceEnv.VIDEO_PROVIDER_MODEL_ID
    || ''
  ).trim();
}

function stateBoundModelId(state = loadState()) {
  return String(state.digitalHuman?.modelId || '').trim();
}

function digitalHumanTrainingState() {
  return readJson(join(STATE_DIR, 'digital-human-state.json'), {});
}

function digitalHumanReady(state = loadState()) {
  const modelId = currentModelId(state);
  if (!modelId) return { ok: false, modelId: '', reason: 'missing_model_id' };
  if (digitalHumanMatchesCurrentPersona(state.digitalHuman)) {
    return { ok: true, modelId, source: state.digitalHuman?.source || 'confirmed' };
  }
  const training = digitalHumanTrainingState();
  if (
    training.lastJob?.status === 'succeeded'
    && training.lastJob?.digitalHumanBizId
    && personaFingerprintMatches(training.lastJob.personaSnapshot?.fingerprint || {}, currentPersonaFingerprint())
  ) {
    return { ok: true, modelId, source: 'trained' };
  }
  if (process.env.DOUYIN_ALLOW_UNCONFIRMED_DEFAULT_DIGITAL_HUMAN === 'true' && state.digitalHuman?.source === 'default') {
    return { ok: true, modelId, source: 'default' };
  }
  return { ok: false, modelId, reason: 'not_confirmed' };
}

function ensureDefaultModelId(state = loadState()) {
  const modelId = currentModelId(state);
  if (modelId) {
    if (!state.digitalHuman?.modelId) {
      state.digitalHuman = {
        ...(state.digitalHuman || {}),
        modelId,
        source: 'default',
        boundAt: new Date().toISOString(),
      };
      return { state, modelId, changed: true };
    }
    return { state, modelId, changed: false };
  }
  const fallback = process.env.DOUYIN_DEFAULT_DIGITAL_HUMAN_ID || DEFAULT_DIGITAL_HUMAN_MODEL_ID;
  state.digitalHuman = {
    ...(state.digitalHuman || {}),
    modelId: fallback,
    source: 'default',
    boundAt: new Date().toISOString(),
  };
  return { state, modelId: fallback, changed: true };
}

function ensureModelIdForLegacyAction(state = loadState()) {
  return ensureDefaultModelId(state);
}

function prerequisites(state = loadState()) {
  const persona = loadPersona();
  const missing = [];
  if (!persona.confirmed) {
    missing.push({
      key: 'persona',
      message: persona.draft
        ? '已有待确认人设，请回复：确认人设；如需调整，请直接说明修改方向。'
        : '请先发送：生成人设，并补充姓名、照片、性别、从业年限、主营业务、核心优势、目标客户、个人特质、案例、IP诉求、禁忌偏好。',
    });
  }
  const human = digitalHumanReady(state);
  if (!human.ok) {
    missing.push({
      key: 'digitalHuman',
      message: persona.confirmed
        ? '人设已确认，但数字人还未就绪。确认人设后系统会自动启动数字人生成；如上次中断，可回复：训练数字人 重试，或回复：绑定数字人ID xxxxx。'
        : '人设确认后会自动进入数字人生成；已有数字人可回复：绑定数字人ID xxxxx。',
    });
  }
  return {
    ok: missing.length === 0,
    missing,
    persona: persona.confirmed || null,
    modelId: stateBoundModelId(state),
    digitalHuman: human,
  };
}

function confirmationMode(state = loadState()) {
  return state.confirmationMode === 'auto' ? 'auto' : 'manual';
}

function confirmationModeLabel(state = loadState()) {
  return confirmationMode(state) === 'auto'
    ? '自动确认（自动生成方案、成片并进入发布；登录/验证码/风控仍会暂停提醒）'
    : '流程自动推进，审核节点人工确认（人设、视频方案和最终视频按文档等待确认）';
}

function statusText(state = loadState()) {
  state = normalizeState(state);
  const pre = prerequisites(state);
  const lines = [
    `自动化营销：${state.enabled ? '已开启' : '未开启'}`,
    `默认时间：每天 ${state.schedule?.dailyTime || DEFAULT_DAILY_TIME}`,
    `确认模式：${confirmationModeLabel(state)}`,
    `人设：${pre.persona ? '已确认' : '未完成'}`,
    `数字人：${pre.digitalHuman?.ok ? `已就绪（${pre.digitalHuman.source}）` : '未就绪'}`,
  ];
  if (state.pendingEnable?.status === 'waiting_confirm') {
    lines.push('待确认开启：请回复“确认开启”，或先修改定时任务/确认模式。');
  }
  if (state.inFlightPlan?.status === 'running') {
    lines.push('视频方案：正在生成中，请稍等；完成后会进入待确认状态。');
  }
  if (state.pendingPlan?.plan) {
    lines.push('待确认方案：已生成，回复“确认方案”生成视频，回复“不满意”重新生成方案。');
  }
  if (state.inFlightVideo?.status === 'running') {
    lines.push('视频：正在生成中，请稍等；完成后回复“确认发布”或“不满意”。');
  }
  if (state.pendingReview?.publishText) {
    lines.push('待确认视频：已生成，回复“确认发布”进入发布流程，回复“不满意”重新生成。');
  }
  if (state.lastRun?.status) lines.push(`最近执行：${state.lastRun.status}（${state.lastRun.finishedAt || state.lastRun.startedAt || '-'}）`);
  if (!pre.ok) lines.push(`缺少：${pre.missing.map((item) => item.key).join('、')}`);
  return lines.join('\n');
}

function enableReviewText(state, pre) {
  const persona = pre.persona?.summary?.coreIdentity || '已确认';
  const time = state.schedule?.dailyTime || DEFAULT_DAILY_TIME;
  const mode = confirmationMode(state);
  return [
    '开启前请核对：',
    `人设：${persona}`,
    `定时：每天 ${time}`,
    `确认模式：${confirmationModeLabel(state)}`,
    '确认开启请回复：确认开启',
    `调整时间可回复：修改定时任务 自动化营销 ${time}`,
    mode === 'auto'
      ? '如需恢复审核节点人工确认，请回复：关闭自动确认'
      : '如需跳过视频方案/最终视频审核，请回复：开启自动确认',
  ].join('\n');
}

function requestEnable(args = {}) {
  let state = normalizeState(loadState());
  if (args.modelId) state.digitalHuman = { ...(state.digitalHuman || {}), modelId: String(args.modelId).trim() };
  if (args.time) state.schedule = { ...(state.schedule || {}), dailyTime: String(args.time).trim() };
  const pre = prerequisites(state);
  if (!pre.ok) {
    state.enabled = false;
    saveState(state);
    return {
      ok: false,
      action: 'marketing_enable_missing_prerequisites',
      missing: pre.missing,
      statePath: STATE_PATH,
      customerMessage: [
        '自动化营销暂未开启。',
        pre.missing[0].message,
        '生成人设并确认后，我会按文档流程继续推进形象定制、视频生成和投放配置。',
      ].join('\n'),
    };
  }
  if (state.enabled) {
    saveState(state);
    return {
      ok: true,
      action: 'marketing_already_enabled',
      statePath: STATE_PATH,
      customerMessage: [
        '自动化营销已开启。',
        `每天 ${state.schedule?.dailyTime || DEFAULT_DAILY_TIME} 自动生成视频，待你回复【确认发布】后发布。`,
        '每 30 分钟自动回复新评论和未读私信。',
      ].join('\n'),
    };
  }
  state.pendingEnable = {
    status: 'waiting_confirm',
    dailyTime: state.schedule?.dailyTime || DEFAULT_DAILY_TIME,
    confirmationMode: confirmationMode(state),
    requestedAt: new Date().toISOString(),
  };
  saveState(state);
  return {
    ok: true,
    action: 'marketing_enable_review_required',
    statePath: STATE_PATH,
    customerMessage: enableReviewText(state, pre),
  };
}

function confirmEnable(args = {}) {
  let state = normalizeState(loadState());
  if (args.time) state.schedule = { ...(state.schedule || {}), dailyTime: String(args.time).trim() };
  const pre = prerequisites(state);
  if (!pre.ok) {
    state.enabled = false;
    saveState(state);
    return {
      ok: false,
      action: 'marketing_enable_missing_prerequisites',
      missing: pre.missing,
      statePath: STATE_PATH,
      customerMessage: `自动化营销暂未开启。\n${pre.missing[0].message}`,
    };
  }
  if (!args.force && state.pendingEnable?.status !== 'waiting_confirm') {
    state.pendingEnable = {
      status: 'waiting_confirm',
      dailyTime: state.schedule?.dailyTime || DEFAULT_DAILY_TIME,
      confirmationMode: confirmationMode(state),
      requestedAt: new Date().toISOString(),
    };
    saveState(state);
    return {
      ok: true,
      action: 'marketing_enable_review_required',
      statePath: STATE_PATH,
      customerMessage: enableReviewText(state, pre),
    };
  }
  state.enabled = true;
  state.enabledAt = new Date().toISOString();
  state.schedule = { ...(state.schedule || {}), dailyTime: args.time || state.schedule?.dailyTime || DEFAULT_DAILY_TIME };
  state.confirmationMode = 'manual';
  state.publishMode = 'manual_confirm';
  state.pendingEnable = null;
  const schedule = updateMarketingSchedule(true, state.schedule.dailyTime);
  saveState(state);
  return {
    ok: true,
    action: 'marketing_enabled',
    statePath: STATE_PATH,
    schedule,
    customerMessage: [
      '自动化营销已开启。',
      `每天 ${state.schedule.dailyTime} 自动生成视频，待你回复【确认发布】后发布。`,
      '每 30 分钟自动回复新评论和未读私信。',
    ].join('\n'),
  };
}

function disable() {
  const state = normalizeState(loadState());
  state.enabled = false;
  state.pendingEnable = null;
  state.disabledAt = new Date().toISOString();
  const schedule = updateMarketingSchedule(false, state.schedule?.dailyTime || DEFAULT_DAILY_TIME);
  saveState(state);
  return { ok: true, action: 'marketing_disabled', statePath: STATE_PATH, schedule, customerMessage: '自动化营销已暂停。' };
}

function setConfirmationMode(mode) {
  const state = normalizeState(loadState());
  const normalized = mode === 'auto' ? 'auto' : 'manual';
  state.confirmationMode = normalized;
  state.publishMode = normalized === 'auto' ? 'auto_confirm' : 'manual_confirm';
  if (state.pendingEnable?.status === 'waiting_confirm') {
    state.pendingEnable = {
      ...state.pendingEnable,
      confirmationMode: normalized,
      updatedAt: new Date().toISOString(),
    };
  }
  saveState(state);
  return {
    ok: true,
    action: normalized === 'auto' ? 'confirmation_mode_auto' : 'confirmation_mode_manual',
    statePath: STATE_PATH,
    customerMessage: normalized === 'auto'
      ? '已开启自动确认模式。后续定时任务会自动生成方案、成片并进入发布；登录/验证码/风控仍会暂停提醒。回复“关闭自动确认”可恢复人工确认。'
      : '已切回审核节点人工确认模式。后续视频方案和最终视频都需要你确认后再进入下一步。',
  };
}

function usageMessage() {
  return [
    '支持：开启自动化营销、确认开启、生成视频方案、确认方案、确认发布、自动化营销状态。',
    '可选：开启自动确认、关闭自动确认、绑定数字人ID xxxxx。',
  ].join('\n');
}

function pendingPlanExists(state = loadState()) {
  return Boolean(state.pendingPlan?.plan);
}

function isFreshRunning(record, staleMs) {
  if (record?.status !== 'running') return false;
  const started = Date.parse(record.startedAt || '');
  if (!Number.isFinite(started)) return true;
  return Date.now() - started < staleMs;
}

function inFlightPlanExists(state = loadState()) {
  return isFreshRunning(state.inFlightPlan, IN_FLIGHT_PLAN_STALE_MS);
}

function pendingReviewExists(state = loadState()) {
  return Boolean(state.pendingReview?.publishText || state.pendingReview?.videoUrl);
}

function inFlightVideoExists(state = loadState()) {
  return isFreshRunning(state.inFlightVideo, IN_FLIGHT_VIDEO_STALE_MS);
}

function pendingPlanReuseResponse(state = loadState()) {
  return {
    ok: true,
    action: 'marketing_plan_already_pending',
    statePath: STATE_PATH,
    customerMessage: [
      '已有待确认视频方案，不再重复生成。',
      planSummaryText(state.pendingPlan),
    ].join('\n'),
    pendingPlan: state.pendingPlan,
  };
}

function inFlightPlanReuseResponse(state = loadState()) {
  return {
    ok: true,
    action: 'marketing_plan_already_running',
    statePath: STATE_PATH,
    customerMessage: '视频方案正在生成中，不再重复生成。请稍等；完成后我会进入待确认方案状态。',
    inFlightPlan: state.inFlightPlan || null,
  };
}

function pendingVideoReuseResponse(state = loadState()) {
  return {
    ok: true,
    action: 'marketing_video_already_pending',
    statePath: STATE_PATH,
    customerMessage: '视频已在生成中或已有待确认视频，请稍等；生成完成后回复“确认发布”，需要重做再回复“不满意”。',
    pendingReview: state.pendingReview || null,
    inFlightVideo: state.inFlightVideo || null,
  };
}

function bindModelId(modelId) {
  const clean = String(modelId || '').trim();
  if (!clean || clean.length < 6) {
    return { ok: false, action: 'bind_model_id_failed', customerMessage: '数字人ID格式不正确，请重新发送。' };
  }
  const state = loadState();
  const fingerprint = currentPersonaFingerprint();
  state.digitalHuman = {
    ...(state.digitalHuman || {}),
    modelId: clean,
    source: 'customer',
    personaConfirmedAt: fingerprint.confirmedAt || '',
    personaFingerprint: fingerprint,
    personaName: fingerprint.name || '',
    personaPhoto: fingerprint.photo || '',
    boundAt: new Date().toISOString(),
    confirmedAt: new Date().toISOString(),
  };
  saveState(state);
  return { ok: true, action: 'bind_model_id', statePath: STATE_PATH, customerMessage: '数字人ID已绑定，后续成片会使用这个ID。' };
}

function updateMarketingSchedule(enabled, time = DEFAULT_DAILY_TIME) {
  const current = readJson(SCHEDULE_CONFIG_PATH, { version: 1, enabled: true, jobs: {} });
  const next = {
    ...current,
    enabled: true,
    jobs: {
      ...(current.jobs || {}),
      autoReply: {
        enabled: Boolean(enabled),
        schedule: current.jobs?.autoReply?.schedule || { kind: 'every', every: '30m' },
      },
      dailyReport: {
        enabled: false,
        schedule: current.jobs?.dailyReport?.schedule || { kind: 'daily', time: '07:30', tz: process.env.DOUYIN_SCHEDULE_TZ || 'Asia/Shanghai' },
      },
      marketingDaily: {
        enabled: Boolean(enabled),
        schedule: { kind: 'daily', time, tz: process.env.DOUYIN_SCHEDULE_TZ || 'Asia/Shanghai' },
      },
    },
  };
  writeJson(SCHEDULE_CONFIG_PATH, next);
  return { ok: true, configPath: SCHEDULE_CONFIG_PATH, enabled: Boolean(enabled), time };
}

function enableMarketingScheduleAfterFirstPublish(time = DEFAULT_DAILY_TIME) {
  return updateMarketingSchedule(true, time);
}

function buildDigitalHumanInput(planPayload, state) {
  const plan = planPayload?.plan || {};
  const digitalHumanInput = { ...(plan.digitalHumanInput || {}) };
  const modelId = currentModelId(state);
  if (modelId) digitalHumanInput.modelId = modelId;
  if (!digitalHumanInput.title && plan.title) digitalHumanInput.title = plan.title;
  if (!digitalHumanInput.publishTitle && plan.title) digitalHumanInput.publishTitle = plan.title;
  if (!digitalHumanInput.videoTitle && (plan.videoTitle || plan.visualTitle || plan.coverText)) digitalHumanInput.videoTitle = plan.videoTitle || plan.visualTitle || plan.coverText;
  if (!digitalHumanInput.visualTitle && (plan.visualTitle || plan.videoTitle || plan.coverText)) digitalHumanInput.visualTitle = plan.visualTitle || plan.videoTitle || plan.coverText;
  if (!digitalHumanInput.scriptText && Array.isArray(plan.script)) digitalHumanInput.scriptText = plan.script.join('\n');
  const scriptOpts = planPayload?.source === 'persona_first_video'
    ? { maxLines: 7, maxLineLength: 24 }
    : {};
  digitalHumanInput.scriptText = normalizeScriptText(digitalHumanInput.scriptText || plan.script || '', scriptOpts);
  if (!digitalHumanInput.coverText && plan.coverText) digitalHumanInput.coverText = plan.coverText;
  const visual = safeVisualTitle(
    digitalHumanInput.visualTitle
    || digitalHumanInput.videoTitle
    || digitalHumanInput.coverText
    || digitalHumanInput.publishTitle
    || digitalHumanInput.title,
  );
  digitalHumanInput.videoTitle = visual;
  digitalHumanInput.visualTitle = visual;
  digitalHumanInput.coverText = safeCoverText(digitalHumanInput.coverText || visual);
  if (!digitalHumanInput.tags && plan.tags) digitalHumanInput.tags = plan.tags;
  return digitalHumanInput;
}

function normalizeScriptLines(value, opts = {}) {
  const maxLines = Number(opts.maxLines || 4);
  const maxLineLength = Number(opts.maxLineLength || 26);
  const raw = Array.isArray(value) ? value.join('\n') : String(value || '');
  const pieces = raw
    .split(/[\n。！？!?]+/)
    .flatMap((line) => line.split(/[；;]+/))
    .map((line) => sentenceLimit(line, maxLineLength))
    .filter(Boolean);
  return pieces.slice(0, maxLines);
}

function normalizeScriptText(value, opts = {}) {
  return normalizeScriptLines(value, opts).join('\n');
}

function fitScriptBudget(lines, opts = {}) {
  const maxLines = Number(opts.maxLines || 4);
  const maxLineLength = Number(opts.maxLineLength || 24);
  const maxTotalLength = Number(opts.maxTotalLength || 78);
  const out = [];
  let total = 0;
  for (const raw of lines || []) {
    const line = sentenceLimit(raw, maxLineLength);
    const len = Array.from(line).length;
    if (!line || total + len > maxTotalLength) continue;
    out.push(line);
    total += len;
    if (out.length >= maxLines) break;
  }
  return out;
}

function fitScriptWithRequiredLines(lines, requiredLines, opts = {}) {
  const maxLines = Number(opts.maxLines || 4);
  const maxLineLength = Number(opts.maxLineLength || 24);
  const maxTotalLength = Number(opts.maxTotalLength || 78);
  const required = (requiredLines || [])
    .map((line) => sentenceLimit(line, maxLineLength))
    .filter(Boolean)
    .slice(0, maxLines);
  const out = [];
  let total = 0;
  for (const raw of lines || []) {
    const line = sentenceLimit(raw, maxLineLength);
    if (!line || required.includes(line) || out.includes(line)) continue;
    const remainingSlots = maxLines - out.length;
    if (remainingSlots <= required.length) break;
    const requiredLen = required.reduce((sum, item) => sum + Array.from(item).length, 0);
    const len = Array.from(line).length;
    if (total + len + requiredLen > maxTotalLength) continue;
    out.push(line);
    total += len;
  }
  for (const line of required) {
    const len = Array.from(line).length;
    if (out.length < maxLines && total + len <= maxTotalLength) {
      out.push(line);
      total += len;
    }
  }
  return out;
}

function planFromPayload(planPayload) {
  return planPayload?.plan || {};
}

function normalizePublishTitle(value, maxLength = 30) {
  const raw = String(value || '')
    .replace(/#[^\s#，。,;；!！?？)）(（]+/g, '')
    .replace(/\s+/g, ' ')
    .replace(/[，,、；;：:|｜\\/-]+$/g, '')
    .trim();
  if (!raw) return '';
  const chars = Array.from(raw);
  if (chars.length <= maxLength) return raw;
  const head = chars.slice(0, maxLength).join('');
  const punctuationIndex = Math.max(
    head.lastIndexOf('？'),
    head.lastIndexOf('?'),
    head.lastIndexOf('！'),
    head.lastIndexOf('!'),
    head.lastIndexOf('。'),
  );
  if (punctuationIndex >= 8) return head.slice(0, punctuationIndex + 1);
  const softIndex = Math.max(head.lastIndexOf('、'), head.lastIndexOf('，'), head.lastIndexOf(','), head.lastIndexOf(' '));
  if (softIndex >= 8) return cleanTrailingPunctuation(head.slice(0, softIndex));
  return cleanTrailingPunctuation(head.replace(/(怎么|如何|为什么|哪些|哪个|怎样)$/u, '')) || head;
}

function publishTitleFromPlan(planPayload) {
  const plan = planFromPayload(planPayload);
  return normalizePublishTitle(plan.publishFields?.title || plan.digitalHumanInput?.publishTitle || plan.title || '自动化营销视频');
}

function planSummaryText(planPayload) {
  const plan = planFromPayload(planPayload);
  const tags = Array.isArray(plan.tags) ? plan.tags.join('') : String(plan.tags || '');
  const script = Array.isArray(plan.script)
    ? plan.script.join(' ')
    : String(plan.script || plan.digitalHumanInput?.scriptText || '');
  return [
    '老板，您的视频方案已生成，请您审核：',
    `标题：${publishTitleFromPlan(planPayload)}`,
    plan.coverText ? `封面：${plan.coverText}` : '',
    tags ? `标签：${tags}` : '',
    script ? `口播：${script.slice(0, 120)}` : '',
    '回复【通过】或【不通过】，若不通过，请指出修改建议～',
  ].filter(Boolean).join('\n');
}

function publishTextFromVideo(videoPayload, planPayload) {
  const task = videoPayload?.task || videoPayload?.wait?.task || {};
  const plan = planPayload?.plan || {};
  const tags = Array.isArray(plan.tags) ? plan.tags.join('') : String(plan.tags || '');
  const coverImageUrl = String(
    task.coverImageUrl
    || videoPayload?.coverImageUrl
    || videoPayload?.wait?.providerDetail?.coverImageUrl
    || plan.coverImageUrl
    || plan.coverUrl
    || ''
  ).trim();
  const videoUrl = String(task.videoUrl || videoPayload?.videoUrl || '').trim();
  const title = publishTitleFromPlan(planPayload) || normalizePublishTitle(task.title || '数字人成片');
  return [
    tags ? `tags:${tags}` : '',
    coverImageUrl ? `"封面图片": "${coverImageUrl}"` : '',
    `标题："${title}"`,
    `"视频地址": "${videoUrl}"`,
  ].filter(Boolean).join('\n');
}

function modelReviewText(state = loadState()) {
  const modelId = currentModelId(state) || process.env.DOUYIN_DEFAULT_DIGITAL_HUMAN_ID || 'CVHPZJ4LCGBMNIZULS0';
  const source = state.digitalHuman?.source === 'customer' ? '客户数字人' : '默认数字人';
  return [
    `当前使用${source}。`,
    `数字人ID：${modelId}`,
    '确认请回复：确认形象',
    '客户已有自己的数字人时，可回复：绑定数字人ID xxxxx',
  ].join('\n');
}

function generatedVideoTask(videoPayload) {
  return videoPayload?.task || videoPayload?.wait?.task || null;
}

function generatedVideoUrl(videoPayload) {
  return String(generatedVideoTask(videoPayload)?.videoUrl || videoPayload?.videoUrl || '').trim();
}

function reportSummaryText(reportPayload) {
  const text = String(reportPayload?.reportText || reportPayload?.basicReportText || '').trim();
  if (!text) return '';
  const firstLines = text
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean)
    .slice(0, 8)
    .join('\n');
  return firstLines;
}

function bitableUrlFromSync(syncPayload) {
  const appToken = syncPayload?.appToken;
  const tableId = syncPayload?.tables?.workTableId || syncPayload?.tables?.worksTableId;
  if (!appToken || !tableId) return '';
  return `https://feishu.cn/base/${encodeURIComponent(appToken)}?table=${encodeURIComponent(tableId)}`;
}

function mergeDailyReportMessage(reportPayload, nextMessage, syncPayload = null) {
  return dailyReportMessages(reportPayload, nextMessage, syncPayload).join('\n\n');
}

function dailyReportMessages(reportPayload, nextMessage, syncPayload = null) {
  const report = reportSummaryText(reportPayload);
  const link = bitableUrlFromSync(syncPayload);
  const reportMessage = [
    '老板，昨日数据报告如下，请您查收～',
    report || '数据报告已生成。',
    link ? `多维表：${link}` : '',
  ].filter(Boolean).join('\n');
  return [
    reportMessage,
    nextMessage || '下一条视频已进入生成流程。',
  ].filter(Boolean);
}

function clearPendingReviewPatch(extra = {}) {
  return patchState({ pendingReview: null, ...extra });
}

function clearPendingPlanPatch(extra = {}) {
  return patchState({ pendingPlan: null, ...extra });
}

function lightPlanPayload() {
  const plan = {
    topic: '自动化营销链路稳定性测试',
    title: '自动化营销链路测试',
    coverText: '链路测试',
    tags: ['#自动化营销', '#数字人'],
    hook: '这是一条验证数字人自动化营销链路是否稳定的测试内容。',
    script: [
      '这是一条数字人自动化营销链路测试。',
      '它会验证人设、方案生成、一键成片桥接和抖音发布入口是否能稳定串起来。',
      '如果你看到这条方案，说明编排流程已经正常工作。',
    ],
    publishFields: {
      title: '自动化营销链路测试',
      description: '这是一条自动化营销链路测试。 #自动化营销 #数字人',
      tags: ['#自动化营销', '#数字人'],
    },
    digitalHumanInput: {
      modelId: '',
      title: '自动化营销链路测试',
      publishTitle: '自动化营销链路测试',
      videoTitle: '链路测试',
      visualTitle: '链路测试',
      scriptText: '这是一条数字人自动化营销链路测试。它会验证人设、方案生成、一键成片桥接和抖音发布入口是否能稳定串起来。',
      coverText: '链路测试',
      tags: ['#自动化营销', '#数字人'],
      suggestedDurationSeconds: 15,
    },
  };
  return {
    ok: true,
    source: 'light_test',
    days: 0,
    counts: { works: 0, daily: 0, log: 0 },
    model: null,
    generator: { ok: true, source: 'light_test' },
    context: {},
    plan,
    planText: '下一条视频方案：自动化营销链路测试',
  };
}

function firstPersonaVideoPlanPayload(state = loadState()) {
  const personaState = loadPersona();
  const confirmed = personaState.confirmed || {};
  const fields = confirmed.fields || {};
  const summary = confirmed.summary || {};
  const account = confirmed.accountProfile || {};
  const customer = confirmed.customerPersona || {};
  const rules = confirmed.contentRules || {};
  const name = shortPhrase(fields.name || account.accountName || '客户', 10);
  const business = businessKeyword(fields.bissiness || fields.business || summary.coreIdentity || '专业服务', 16);
  const audience = audienceLabel(fields.segment || summary.audience || customer.coreLabel || customer.attributes || '', '客户');
  const problem = problemLabel(fields.segment || fields.bissiness || customer.painPoints || customer.needs || '', '实际问题');
  const value = shortPhrase(summary.value || fields.advantage || customer.needs || '专业建议', 18);
  const tone = shortPhrase(summary.tone || fields.trials || rules.interactionTone || '专业、真诚、清晰', 32);
  const compliance = String(fields.taboos || compactText(rules.compliance, 100) || '表达合规，不夸大、不承诺不可控结果').trim();
  const videoRevisionFeedback = compactText(state.videoRevisionFeedback || '', 80);
  const baseTitle = `${name}：${business}怎么少踩坑？`;
  const title = applyTitleRevisionFeedback(baseTitle, videoRevisionFeedback, fields);
  const visualTitle = safeVisualTitle(summary.slogan || `${business}避坑`, `${business.slice(0, 4) || '专业'}避坑`);
  const coverText = safeCoverText(summary.slogan || `${business}避坑指南`, visualTitle);
  const tags = Array.isArray(account.hashtags) && account.hashtags.length
    ? account.hashtags.slice(0, 4).map((tag) => String(tag).startsWith('#') ? String(tag) : `#${tag}`)
    : ['#个人IP', '#专业服务', '#避坑指南'];
  const baseScript = [
    `大家好，我是${name}`,
    `做${business}这行${fields.work_year || '多年'}了`,
    `主要帮${audience}选对方案`,
    problem ? `不少人卡在${problem}` : '',
    `我会用大白话讲清楚`,
    '如果你也遇到这些问题，关注我',
    '只讲真实场景，不夸大效果',
  ];
  const scriptSource = videoRevisionFeedback
    ? [
      baseScript[0],
      /更自然|自然|通顺|短句|多段/u.test(videoRevisionFeedback) ? '我用几句实在话讲清楚' : '',
      /痛点|问题|困扰/u.test(videoRevisionFeedback) ? `先说${audience}最常见的痛点` : '',
      ...baseScript.slice(1),
    ]
    : baseScript;
  const script = videoRevisionFeedback
    ? fitScriptWithRequiredLines(scriptSource, ['如果你也遇到这些问题，关注我'], { maxLines: 7, maxLineLength: 24, maxTotalLength: 112 })
    : fitScriptBudget(scriptSource, { maxLines: 7, maxLineLength: 24, maxTotalLength: 112 });
  const plan = {
    topic: '首条人设介绍视频',
    title,
    videoTitle: visualTitle,
    visualTitle,
    coverText,
    tags,
    hook: script[0],
    script,
    publishFields: {
      title,
      description: `${script.join(' ')} ${tags.join(' ')}`,
      tags,
    },
    digitalHumanInput: {
      modelId: currentModelId(state),
      title,
      publishTitle: title,
      videoTitle: visualTitle,
      visualTitle,
      scriptText: normalizeScriptText(script, { maxLines: 7, maxLineLength: 24, maxTotalLength: 112 }),
      coverText,
      tags,
      tone,
      compliance,
      suggestedDurationSeconds: 22,
    },
  };
  return {
    ok: true,
    source: 'persona_first_video',
    days: 0,
    counts: { works: 0, daily: 0, log: 0 },
    personaUsed: true,
    videoRevisionFeedback,
    personaSummary: summary,
    model: null,
    generator: { ok: true, source: 'persona_first_video' },
    context: { persona: { fields, summary, accountProfile: account, customerPersona: customer, contentRules: rules } },
    plan,
    planText: `首条视频方案：${title}`,
  };
}

function routePublishText(text, opts = {}) {
  if (opts.dryRun) {
    return { ok: true, dryRun: true, action: 'publish_route_dry_run', text };
  }
  return runNode([
    'scripts/feishu-reply-watcher.js',
    'route-text',
    '--text',
    text,
    ...(opts.receiveId ? ['--receive-id', opts.receiveId, '--receive-id-type', opts.receiveIdType || 'chat_id'] : []),
  ], {
    timeout: 900000,
    env: {
      DOUYIN_SUPPRESS_PUBLISH_START: 'true',
      DOUYIN_INTERNAL_CONFIRMED_MARKETING_PUBLISH: 'true',
    },
  });
}

function publishSubmittedMessage(ok) {
  return ok ? '' : '发布流程启动失败，请稍后重试。';
}

function publishStartedByRoute(payload) {
  const action = String(payload?.result?.action || payload?.action || '');
  return Boolean(
    payload?.ok === true
    && /upstream_task_waiting_login_|publish_upstream_task_|publish_video_from_feishu|publish_current_draft/.test(action)
  );
}

function reviewDefaultModel(args = {}) {
  let state = loadState();
  state = ensureDefaultModelId(state).state;
  patchState({
    digitalHuman: state.digitalHuman,
    pendingModelReview: {
      modelId: currentModelId(state),
      status: 'pending',
      createdAt: new Date().toISOString(),
    },
  });
  return {
    ok: true,
    action: 'digital_human_default_model_review',
    statePath: STATE_PATH,
    modelId: currentModelId(state),
    customerMessage: modelReviewText(state),
  };
}

function confirmDefaultModel() {
  let state = loadState();
  state = ensureDefaultModelId(state).state;
  state.pendingModelReview = null;
  state.digitalHuman = {
    ...(state.digitalHuman || {}),
    confirmedAt: new Date().toISOString(),
  };
  saveState(state);
  return {
    ok: true,
    action: 'digital_human_default_model_confirmed',
    statePath: STATE_PATH,
    modelId: currentModelId(state),
    customerMessage: '数字人ID已确认。',
  };
}

async function generatePlan(args = {}) {
  const state = normalizeState(loadState());
  if (!isFreshRunning(state.inFlightPlan, IN_FLIGHT_PLAN_STALE_MS) && state.inFlightPlan?.status === 'running') {
    state.inFlightPlan = null;
  }
  if (!isFreshRunning(state.inFlightVideo, IN_FLIGHT_VIDEO_STALE_MS) && state.inFlightVideo?.status === 'running') {
    state.inFlightVideo = null;
  }
  saveState(state);
  if (!args.force && pendingPlanExists(state)) return pendingPlanReuseResponse(state);
  if (!args.force && inFlightPlanExists(state)) return inFlightPlanReuseResponse(state);
  if (!args.force && (pendingReviewExists(state) || inFlightVideoExists(state))) return pendingVideoReuseResponse(state);
  const pre = prerequisites(state);
  if (!pre.ok && !args.allowMissingPersona) {
    return {
      ok: false,
      action: 'generate_plan_missing_prerequisites',
      missing: pre.missing,
      customerMessage: `视频方案暂未开始。\n${pre.missing[0].message}`,
    };
  }
  const runId = `plan-${Date.now()}`;
  const outputPath = join(STATE_DIR, 'reports', `${runId}-next-video-plan.json`);
  patchState({
    inFlightPlan: {
      runId,
      status: 'running',
      outputPath,
      startedAt: new Date().toISOString(),
    },
  });
  const lightMode = args.lightTest || process.env.DOUYIN_ROUTE_LIGHT_TEST === 'true';
  const plan = lightMode
    ? { ok: true, payload: lightPlanPayload() }
    : (args.inputJson
      ? { ok: true, payload: JSON.parse(readFileSync(args.inputJson, 'utf8')) }
      : runNode([
        'scripts/douyin-next-video-plan-from-bitable.js',
        '--days',
        String(args.days || 90),
        '--persona-state',
        PERSONA_STATE_PATH,
        '--output',
        outputPath,
      ], { timeout: 240000 }));
  const planPayload = plan.payload;
  if (!plan.ok || !planPayload?.ok) {
    patchState({
      inFlightPlan: null,
      lastRun: {
        status: 'failed',
        stage: 'next_video_plan_failed',
        runId,
        finishedAt: new Date().toISOString(),
      },
    });
    return { ok: false, action: 'next_video_plan_failed', plan, customerMessage: '视频方案生成失败，请先发送：更新数据' };
  }
  patchState({
    inFlightPlan: null,
    pendingPlan: {
      runId,
      plan: planPayload,
      createdAt: new Date().toISOString(),
    },
    pendingReview: null,
    lastPlan: {
      runId,
      title: publishTitleFromPlan(planPayload),
      createdAt: new Date().toISOString(),
    },
  });
  return {
    ok: true,
    action: 'marketing_plan_generated',
    runId,
    plan: planPayload,
    customerMessage: planSummaryText(planPayload),
  };
}

async function generateVideo(args = {}) {
  const state = normalizeState(loadState());
  if (!isFreshRunning(state.inFlightPlan, IN_FLIGHT_PLAN_STALE_MS) && state.inFlightPlan?.status === 'running') {
    state.inFlightPlan = null;
  }
  if (!isFreshRunning(state.inFlightVideo, IN_FLIGHT_VIDEO_STALE_MS) && state.inFlightVideo?.status === 'running') {
    state.inFlightVideo = null;
  }
  saveState(state);
  if (!args.force && (pendingReviewExists(state) || inFlightVideoExists(state))) return pendingVideoReuseResponse(state);
  const pre = prerequisites(state);
  if (!pre.ok && !args.allowMissingPersona) {
    return {
      ok: false,
      action: 'generate_video_missing_prerequisites',
      missing: pre.missing,
      customerMessage: `视频生成暂未开始。\n${pre.missing[0].message}`,
    };
  }

  const runId = `marketing-${Date.now()}`;
  let planPayload = args.firstPersonaVideo ? null : (args.planPayload || state.pendingPlan?.plan || null);
  if (!planPayload) {
    if (args.firstPersonaVideo) {
      planPayload = firstPersonaVideoPlanPayload(state);
    } else if (args.requirePlanConfirmation) {
      return {
        ok: false,
        action: 'generate_video_requires_plan_confirmation',
        customerMessage: '请先发送：生成视频方案。确认方案后我再生成最终视频。',
      };
    } else {
      const generatedPlan = await generatePlan(args);
      if (!generatedPlan.ok) return generatedPlan;
      planPayload = generatedPlan.plan;
    }
  }

  const digitalHumanInput = {
    ...buildDigitalHumanInput(planPayload, state),
    ...(args.title ? { title: args.title } : {}),
    ...(args.scriptText ? { scriptText: args.scriptText } : {}),
  };
  const videoInputPath = join(STATE_DIR, 'reports', `${runId}-xiaoice-input.json`);
  mkdirSync(dirname(videoInputPath), { recursive: true });
  writeJson(videoInputPath, {
    ...digitalHumanInput,
    digitalHumanInput,
    title: digitalHumanInput.title,
    publishTitle: digitalHumanInput.publishTitle || digitalHumanInput.title,
    videoTitle: digitalHumanInput.videoTitle || digitalHumanInput.visualTitle || digitalHumanInput.coverText,
    visualTitle: digitalHumanInput.visualTitle || digitalHumanInput.videoTitle || digitalHumanInput.coverText,
    scriptText: digitalHumanInput.scriptText,
    tags: digitalHumanInput.tags,
  });
  patchState({
    inFlightVideo: {
      runId,
      status: 'running',
      inputPath: videoInputPath,
      startedAt: new Date().toISOString(),
      title: digitalHumanInput.publishTitle || digitalHumanInput.title || '',
    },
  });
  const video = runNode([
    'scripts/xiaoice-video-produce.js',
    args.dryRun ? 'create-and-wait' : 'create-and-wait',
    '--input-json',
    videoInputPath,
    ...(args.dryRun ? ['--dry-run'] : []),
    '--timeout-sec',
    String(args.timeoutSec || XIAOICE_VIDEO_TIMEOUT_SEC),
    '--interval-sec',
    String(args.intervalSec || 5),
  ], {
    timeout: Math.max(60_000, Number(args.timeoutSec || XIAOICE_VIDEO_TIMEOUT_SEC) * 1000 + 60_000),
    env: currentModelId(state) ? { DIGITAL_HUMAN_MODEL_ID: currentModelId(state) } : {},
  });
  if (!video.ok || !video.payload?.ok) {
    patchState({
      inFlightVideo: null,
      lastRun: {
        status: 'failed',
        stage: 'xiaoice_video_failed',
        runId,
        finishedAt: new Date().toISOString(),
      },
    });
    return { ok: false, action: 'xiaoice_video_failed', plan: planPayload, video, customerMessage: '视频生成失败，请稍后重试。' };
  }
  const publishText = publishTextFromVideo(video.payload, planPayload);
  const output = {
    ok: true,
    action: 'marketing_video_generated',
    runId,
    plan: planPayload,
    video: video.payload,
    publishText,
    customerMessage: args.autoPublish
      ? ''
      : videoReviewText(video.payload, planPayload),
  };
  patchState({
    lastGenerated: {
      runId,
      planSource: planPayload.source || '',
      title: publishTitleFromPlan(planPayload),
      publishText,
      video: generatedVideoTask(video.payload),
      generatedAt: new Date().toISOString(),
    },
    pendingReview: args.autoPublish ? null : {
      runId,
      planSource: planPayload.source || '',
      publishText,
      videoUrl: generatedVideoUrl(video.payload),
      planTitle: planPayload?.plan?.title || '',
      createdAt: new Date().toISOString(),
    },
    pendingPlan: args.keepPendingPlan ? state.pendingPlan || null : null,
    inFlightVideo: null,
  });
  return output;
}

function videoReviewText(videoPayload, planPayload) {
  const plan = planFromPayload(planPayload);
  const task = generatedVideoTask(videoPayload) || {};
  const title = publishTitleFromPlan(planPayload);
  const tags = Array.isArray(plan.tags) ? plan.tags.join('') : String(plan.tags || '');
  const description = String(plan.publishFields?.description || plan.description || plan.digitalHumanInput?.description || '').trim();
  const videoUrl = String(task.videoUrl || videoPayload?.videoUrl || '').trim();
  const coverUrl = String(
    task.coverImageUrl
    || videoPayload?.coverImageUrl
    || videoPayload?.wait?.providerDetail?.coverImageUrl
    || plan.coverImageUrl
    || plan.coverUrl
    || ''
  ).trim();
  const lines = [
    '老板，您的视频制作完成！请您审核：',
    `视频标题：${title}`,
    description ? `视频描述：${description}` : '',
    tags ? `视频标签：${tags}` : '',
    videoUrl ? `视频地址：${videoUrl}` : '',
    coverUrl ? `封面地址：${coverUrl}` : '',
  ].filter(Boolean);
  return `${lines.join('\n')}\n\n回复【确认发布】或【不通过】，若不通过，请指出修改建议～`;
}

async function generateAndPublish(args = {}) {
  const startedAt = new Date().toISOString();
  patchState({ lastRun: { status: 'running', startedAt, stage: 'generate_video' } });
  const generated = await generateVideo({ ...args, autoPublish: true });
  if (!generated.ok) {
    patchState({ lastRun: { status: 'failed', startedAt, finishedAt: new Date().toISOString(), stage: generated.action, customerMessage: generated.customerMessage } });
    return generated;
  }
  const publish = routePublishText(generated.publishText, args);
  const publishPayload = publish.payload;
  const ok = Boolean(args.dryRun || publish.ok && publishPayload?.ok === true);
  patchState({ lastRun: {
    status: ok ? 'submitted' : 'failed',
    startedAt,
    finishedAt: new Date().toISOString(),
    stage: 'publish',
    publishText: generated.publishText,
    publishPayload,
  } });
  return {
    ok,
    action: args.dryRun ? 'marketing_generate_and_publish_dry_run' : 'marketing_generate_and_publish',
    generated,
    publish,
    customerMessage: publishSubmittedMessage(ok),
  };
}

function publishPendingReview(args = {}) {
  const state = loadState();
  const pending = state.pendingReview;
  if (!pending?.publishText) {
    return {
      ok: false,
      action: 'publish_pending_review_missing',
      customerMessage: '当前没有待确认视频。请先发送：生成数字人视频',
    };
  }
  const publish = routePublishText(pending.publishText, args);
  const publishPayload = publish.payload;
  const ok = Boolean(args.dryRun || publish.ok && publishPayload?.ok === true);
  const publishStarted = Boolean(args.dryRun || publishStartedByRoute(publishPayload));
  patchState({
    pendingReview: publishStarted ? null : pending,
    lastRun: {
      status: publishStarted ? 'submitted' : 'failed',
      startedAt: pending.createdAt || new Date().toISOString(),
      finishedAt: new Date().toISOString(),
      stage: 'publish_confirmed_video',
      publishText: pending.publishText,
      publishPayload,
    },
  });
  return {
    ok,
    action: args.dryRun ? 'publish_pending_review_dry_run' : 'publish_pending_review',
    publish,
    pending,
    customerMessage: publishSubmittedMessage(publishStarted),
  };
}

async function regeneratePendingReview(args = {}) {
  const pending = loadState().pendingReview || {};
  const feedback = revisionFeedbackFromText(args.text || args.rawText || '');
  clearPendingReviewPatch(feedback ? {
    videoRevisionFeedback: feedback,
    lastVideoRevisionRequestedAt: new Date().toISOString(),
  } : {});
  return generateVideo({
    ...args,
    firstPersonaVideo: pending.planSource === 'persona_first_video' || args.firstPersonaVideo,
  });
}

async function confirmPendingPlan(args = {}) {
  const state = loadState();
  const pending = state.pendingPlan;
  if (!pending?.plan) {
    return {
      ok: false,
      action: 'confirm_pending_plan_missing',
      customerMessage: '当前没有待确认视频方案。请先发送：生成视频方案',
    };
  }
  return generateVideo({ ...args, planPayload: pending.plan });
}

async function rejectPendingPlan(args = {}) {
  clearPendingPlanPatch({ pendingReview: null, inFlightPlan: null, inFlightVideo: null });
  return generatePlan(args);
}

function digitalHumanTrainingUnavailable(args = {}) {
  const routeArgs = [
    'scripts/digital-human-training.js',
    'route-text',
    '--text',
    '训练数字人',
  ];
  if (args.dryRun) routeArgs.push('--dry-run');
  if (args.skipCoze || args.defaultModel || args.useDefaultModel) routeArgs.push('--use-default-model');
  const result = runNode(routeArgs, { timeout: DIGITAL_HUMAN_ROUTE_TIMEOUT_MS });
  return result.payload || {
    ok: false,
    action: 'digital_human_training_failed_to_start',
    result,
    customerMessage: result.timedOut
      ? '数字人训练启动仍在等待形象视频生成，请稍后回复：查看数字人训练'
      : '数字人训练入口启动失败，请稍后重试。',
  };
}

function digitalHumanTrainingRoute(text, args = {}) {
  const routeArgs = [
    'scripts/digital-human-training.js',
    'route-text',
    '--text',
    text,
  ];
  if (args.dryRun) routeArgs.push('--dry-run');
  if (args.skipCoze || args.defaultModel || args.useDefaultModel) routeArgs.push('--use-default-model');
  const result = runNode(routeArgs, { timeout: DIGITAL_HUMAN_ROUTE_TIMEOUT_MS });
  if (result.payload) return {
    ...result.payload,
    customerMessage: result.payload.customerMessage || (result.payload.error === 'coze_training_video_url_not_found'
      ? '形象视频生成流程已执行，但 Coze 工作流没有返回训练视频链接。请联系管理员检查工作流输出节点/字段名。'
      : '数字人训练处理失败，请检查材料后重试。'),
  };
  return {
    ok: false,
    action: 'digital_human_training_route_failed',
    result,
    customerMessage: result.timedOut
      ? '数字人训练处理时间较长，请稍后回复：查看数字人训练'
      : '数字人训练处理失败，请检查材料后重试。',
  };
}

async function dailyRun(args = {}) {
  const startedAt = new Date().toISOString();
  const state = normalizeState(loadState());
  saveState(state);
  if (!state.enabled && !args.force) {
    return { ok: false, action: 'marketing_daily_skipped_disabled', customerMessage: '自动化营销未开启。' };
  }
  const pre = prerequisites(state);
  if (!pre.ok) {
    return { ok: false, action: 'marketing_daily_missing_prerequisites', missing: pre.missing, customerMessage: `今日自动化营销中断：${pre.missing[0].message}` };
  }
  const sync = args.dryRun
    ? { ok: true, dryRun: true, payload: { ok: true, skipped: true, reason: 'dry_run' } }
    : runNode(['scripts/sync-douyin-data-to-feishu-bitable.js', '--days', String(args.days || 90)], { timeout: 600000 });
  if (!sync.ok || sync.payload?.ok === false) {
    return { ok: false, action: 'marketing_daily_sync_failed', sync, customerMessage: '今日自动化营销中断：数据更新失败。' };
  }
  const report = args.dryRun
    ? { ok: true, dryRun: true, payload: { ok: true, reportText: '数据报告：dry-run 已跳过真实多维表读取。' } }
    : runNode(['scripts/douyin-data-report-from-bitable.js', '--days', String(args.days || 90)], { timeout: 240000 });
  if (!report.ok || report.payload?.ok === false) {
    return { ok: false, action: 'marketing_daily_report_failed', sync, report, customerMessage: '今日自动化营销中断：数据报告生成失败。' };
  }
  if (confirmationMode(state) === 'manual' && !args.autoConfirm) {
    patchState({ lastRun: { status: 'running', startedAt, stage: 'generate_video_manual_publish_confirm' } });
    const generated = await generateVideo({ ...args, autoPublish: false });
    patchState({
      lastRun: {
        status: generated.ok ? 'waiting_publish_confirm' : 'failed',
        startedAt,
        finishedAt: new Date().toISOString(),
        stage: generated.action,
        customerMessage: generated.customerMessage,
        report: report.payload,
      },
    });
    return {
      ...generated,
      action: generated.ok ? 'marketing_daily_waiting_publish_confirm' : generated.action,
      sync,
      report,
      customerMessages: generated.ok
        ? dailyReportMessages(report.payload, generated.customerMessage, sync.payload)
        : undefined,
      customerMessage: generated.ok
        ? mergeDailyReportMessage(report.payload, generated.customerMessage, sync.payload)
        : generated.customerMessage,
    };
  }
  const result = await generateAndPublish(args);
  return {
    ...result,
    action: result.ok ? 'marketing_daily_run_started_publish' : result.action,
    sync,
    report,
    customerMessages: result.ok
      ? dailyReportMessages(report.payload, result.customerMessage || '新视频已生成并进入发布流程。', sync.payload)
      : undefined,
    customerMessage: result.ok
      ? mergeDailyReportMessage(report.payload, result.customerMessage || '新视频已生成并进入发布流程。', sync.payload)
      : result.customerMessage,
  };
}

async function routeText(text, args = {}) {
  const raw = String(text || '').trim();
  if (/^(自动化营销状态|营销状态|当前状态|任务进度)$/.test(raw)) {
    const state = loadState();
    return { ok: true, action: 'marketing_status', statePath: STATE_PATH, customerMessage: statusText(state), state };
  }
  if (/^(查看数字人训练|检查数字人训练|数字人训练状态|数字人状态|训练进度|质检结果|训练结果|继续训练)$/.test(raw)
    || /训练视频|授权视频|授权文件|trainingVideoUrl|authVideoUrl|authFileUrl|照片链接|本人照片|形象照片|头像照片|照片\s*[:：]|photoUrl|photo\s*[:：]/i.test(raw)) {
    return digitalHumanTrainingRoute(raw, args);
  }
  if (/^(关闭自动化营销|暂停自动发布|暂停自动化营销|关闭营销|停止营销|停止自动化营销|关闭自动营销)$/.test(raw)) return disable();
  if (/^(查看形象|形象审核|审核形象|确认默认形象|默认数字人|查看数字人形象)$/.test(raw)) return reviewDefaultModel(args);
  if (/^(确认形象|采用形象|采用默认形象)$/.test(raw)) return confirmDefaultModel();
  if (/^(训练数字人|生成数字人形象|上传照片训练|上传视频训练|形象定制)$/.test(raw)) return digitalHumanTrainingUnavailable(args);
  if (/^(绑定数字人ID|设置modelId|设置模型ID|数字人ID是|数字人ID)\s*[:：]?\s*$/i.test(raw)) {
    return {
      ok: false,
      action: 'bind_model_id_missing',
      customerMessage: '请发送：绑定数字人ID xxxxx',
    };
  }
  const bind = raw.match(/(?:绑定数字人ID|设置modelId|设置模型ID|数字人ID是|数字人ID)\s*[:：]?\s*([A-Za-z0-9_-]{6,})/i);
  if (bind) return bindModelId(bind[1]);
  if (/^(开启自动确认|开启自动发布模式|自动确认|自动发布模式|跳过确认|以后自动确认)$/.test(raw)) return setConfirmationMode('auto');
  if (/^(关闭自动确认|关闭自动发布模式|人工确认|手动确认|手动确认模式|人工确认模式)$/.test(raw)) return setConfirmationMode('manual');
  if (/^(确认开启|确认启动|确认开启自动化营销|确认启动自动化营销)$/.test(raw)) return confirmEnable(args);
  if (/^(开启自动化营销|启动自动化营销|我要做自动化营销|开启营销|启动营销|开通自动化营销|开启自动营销|启动自动营销|我要自动营销)$/.test(raw)) return requestEnable(args);
  if (/^(生成视频方案|生成内容方案|生成选题方案|生成模板|生成标题模板|生成方案|生成内容|视频文案|口播文案|立即生成视频|马上生成视频|现在生成视频|开始生成视频)$/.test(raw)) return generatePlan(args);
  if (/^(确认方案|确认模板|采用方案|采用这个方案)$/.test(raw)) return confirmPendingPlan(args);
  if (/^(初次生成数字人视频|直接生成数字人视频|立即生成数字人视频)$/.test(raw)) return generateVideo({ ...args, firstPersonaVideo: true });
  if (/^(生成数字人视频|一键成片|生成视频)$/.test(raw)) return stateHasPendingPlan() ? confirmPendingPlan(args) : generateVideo({ ...args, requirePlanConfirmation: true });
  if (/^(确认发布|发布这个视频|确认发布视频|发布生成的视频)$/.test(raw)) return publishPendingReview(args);
  if (/^(不通过|不满意|重新生成视频|重做视频|重新成片)(?:[\s\S]*)$/.test(raw)) {
    return loadState().pendingPlan?.plan
      ? rejectPendingPlan({ ...args, text: raw })
      : regeneratePendingReview({ ...args, text: raw });
  }
  if (/^(生成并发布|生成并发布视频|自动生成并发布|执行自动化营销)$/.test(raw)) return generateAndPublish(args);
  if (/^(每日自动化营销|今日自动化营销|运行自动化营销)$/.test(raw)) return dailyRun({ ...args, force: true });
  return { ok: false, action: 'marketing_usage', customerMessage: usageMessage() };
}

function stateHasPendingPlan() {
  return Boolean(loadState().pendingPlan?.plan);
}

async function main() {
  const [command = 'status', ...rest] = process.argv.slice(2);
  const args = parseArgs(rest);
  let output;
  if (command === 'status') {
    const state = loadState();
    output = { ok: true, action: 'marketing_status', statePath: STATE_PATH, customerMessage: statusText(state), state };
  } else if (command === 'enable') output = confirmEnable({ ...args, force: true });
  else if (command === 'request-enable') output = requestEnable(args);
  else if (command === 'confirm-enable') output = confirmEnable(args);
  else if (command === 'set-confirmation-mode') output = setConfirmationMode(args.mode || args._[0]);
  else if (command === 'disable') output = disable();
  else if (command === 'bind-model') output = bindModelId(args.modelId || args._[0]);
  else if (command === 'generate-plan') output = await generatePlan(args);
  else if (command === 'generate-video') output = await generateVideo(args);
  else if (command === 'confirm-plan') output = await confirmPendingPlan(args);
  else if (command === 'generate-and-publish') output = await generateAndPublish(args);
  else if (command === 'publish-pending') output = publishPendingReview(args);
  else if (command === 'regenerate-pending') output = await regeneratePendingReview(args);
  else if (command === 'daily-run') output = await dailyRun(args);
  else if (command === 'route-text') output = await routeText(args.text || args._.join(' '), args);
  else {
    output = { ok: false, error: 'unknown_command', usage: 'marketing-controller.js status|request-enable|confirm-enable|enable|disable|bind-model|generate-plan|confirm-plan|generate-video|generate-and-publish|daily-run|route-text' };
  }
  if (args.notify && output.customerMessage) output.notify = await sendFeishuText(output.customerMessage);
  console.log(JSON.stringify(output, null, 2));
  if (output.ok === false) process.exitCode = 1;
}

main().catch((err) => {
  console.log(JSON.stringify({ ok: false, error: err.message, stack: err.stack }, null, 2));
  process.exit(1);
});
