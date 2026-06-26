#!/usr/bin/env node
import { existsSync, mkdirSync, openSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
const DEFAULT_TOOL_DIR = join(process.env.HOME || '.', '自动营销', 'xiaoice-video-tool');
const XIAOICE_TOOL_DIR = process.env.XIAOICE_VIDEO_TOOL_DIR || DEFAULT_TOOL_DIR;
const XIAOICE_ENV_PATH = process.env.XIAOICE_VIDEO_ENV_PATH || join(XIAOICE_TOOL_DIR, '.env');
const STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(process.env.HOME || '.', '.openclaw', 'workspace', 'douyin-ops');
const JOB_DIR = join(STATE_DIR, 'xiaoice-video-jobs');

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
  return { ...loadEnvFile(XIAOICE_ENV_PATH), ...process.env };
}

function baseUrl(env = mergedEnv()) {
  return String(env.XIAOICE_VIDEO_SERVICE_BASE_URL || `http://${env.VIDEO_TASK_SERVICE_HOST || '127.0.0.1'}:${env.VIDEO_TASK_SERVICE_PORT || '3105'}`).replace(/\/+$/, '');
}

function internalToken(env = mergedEnv()) {
  return String(env.VIDEO_SERVICE_INTERNAL_TOKEN || '').trim();
}

function providerVhBizId(env = mergedEnv()) {
  return String(
    process.env.DIGITAL_HUMAN_VH_BIZ_ID
    || process.env.DIGITAL_HUMAN_MODEL_ID
    || process.env.VIRTUALMAN_MODEL_ID
    || env.VIDEO_PROVIDER_VH_BIZ_ID
    || env.VIDEO_PROVIDER_MODEL_ID
    || ''
  ).trim();
}

function parseJsonInput(args) {
  if (args.inputJson) return JSON.parse(readFileSync(args.inputJson, 'utf8'));
  if (args.json) return JSON.parse(String(args.json));
  return {};
}

function splitTags(value) {
  if (Array.isArray(value)) return value.map((item) => String(item || '').trim()).filter(Boolean);
  return String(value || '')
    .split(/(?=#)|[\s,，、]+/)
    .map((item) => item.trim())
    .filter(Boolean)
    .map((item) => item.startsWith('#') ? item : `#${item}`);
}

function stripTitleDecorations(value) {
  return String(value || '')
    .replace(/^[^：:\n]{1,10}[：:]/u, '')
    .replace(/[#"'“”‘’《》【】（）()]/g, '')
    .replace(/\s+/g, '')
    .trim();
}

function textUnits(value) {
  return [...stripTitleDecorations(value)];
}

function safeVisualTitle(value, fallback = '今日重点') {
  const normalized = stripTitleDecorations(value)
    .replace(/怎么少踩坑|如何少踩坑|怎样少踩坑|怎么避坑|如何避坑|怎样避坑/gu, '避坑')
    .replace(/避坑指南$/u, '避坑');
  const units = textUnits(normalized);
  if (!units.length) return fallback;
  if (units.length <= 8) return units.join('');
  const raw = units.join('');
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
      if (textUnits(title).length <= 8) return title;
      if (textUnits(match).length >= 4 && textUnits(match).length <= 8) return match;
    }
  }
  const preferred = [
    /[^，。！？!?、：:\s]{2,8}(?:测试|避坑|方案|技巧|重点|服务|指南|提醒|真相|秘诀)/,
    /(?:稳定性测试|一键成片|接口测试|数据复盘|宠物保险|宠物险|自动营销|数字人)/,
  ];
  for (const pattern of preferred) {
    const match = raw.match(pattern);
    if (match?.[0] && textUnits(match[0]).length <= 8) return match[0];
  }
  return units.slice(0, 8).join('');
}

function cleanTrailingPunctuation(value) {
  return String(value || '').replace(/[、，,；;：:\s]+$/u, '').trim();
}

function sentenceLimit(value, maxLength = 26) {
  const text = String(value || '').replace(/\s+/g, ' ').trim();
  if (!text) return '';
  const chars = Array.from(text);
  if (chars.length <= maxLength) return cleanTrailingPunctuation(text);
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

function normalizeScriptText(value, opts = {}) {
  const maxLines = Number(opts.maxLines || 6);
  const maxLineLength = Number(opts.maxLineLength || 26);
  const maxTotalLength = Number(opts.maxTotalLength || 96);
  let total = 0;
  const lines = [];
  for (const line of String(value || '')
    .split(/[\n。！？!?]+/)
    .flatMap((item) => item.split(/[；;]+/))) {
    const limited = sentenceLimit(line, maxLineLength);
    const len = Array.from(limited).length;
    if (!limited || total + len > maxTotalLength) continue;
    lines.push(limited);
    total += len;
    if (lines.length >= maxLines) break;
  }
  return lines.join('\n');
}

function publishTitleFrom(input, args, digitalHumanInput) {
  return String(
    args.publishTitle
    || input.publishTitle
    || input.publishFields?.title
    || input.metadata?.title
    || input['发布标题']
    || args.title
    || input.title
    || digitalHumanInput.publishTitle
    || digitalHumanInput.title
    || ''
  ).trim();
}

function buildTopic(input, args) {
  const publishTitle = publishTitleFrom(input, args, input.digitalHumanInput || {});
  const title = safeVisualTitle(
    args.visualTitle
    || args.videoTitle
    || input.visualTitle
    || input.videoTitle
    || input.digitalHumanInput?.visualTitle
    || input.digitalHumanInput?.videoTitle
    || input.digitalHumanInput?.coverText
    || input.coverText
    || publishTitle
  );
  const scriptText = normalizeScriptText(args.scriptText || input.scriptText || input.digitalHumanInput?.scriptText || input.content || '');
  const coverText = String(args.coverText || input.coverText || input.digitalHumanInput?.coverText || '').trim();
  const tags = splitTags(args.tags || input.tags || input.digitalHumanInput?.tags);
  return String(args.topic || input.topic || [
    title ? `画面标题：${title}` : '',
    coverText ? `封面文案：${coverText}` : '',
    scriptText ? `口播脚本：${scriptText}` : '',
    tags.length ? `标签：${tags.join(' ')}` : '',
  ].filter(Boolean).join('\n')).trim();
}

function buildCreateBody(input, args) {
  const env = mergedEnv();
  const digitalHumanInput = input.digitalHumanInput && typeof input.digitalHumanInput === 'object'
    ? input.digitalHumanInput
    : {};
  const publishTitle = publishTitleFrom(input, args, digitalHumanInput);
  const title = safeVisualTitle(
    args.visualTitle
    || args.videoTitle
    || input.visualTitle
    || input.videoTitle
    || digitalHumanInput.visualTitle
    || digitalHumanInput.videoTitle
    || digitalHumanInput.coverText
    || input.coverText
    || publishTitle
  );
  const scriptText = normalizeScriptText(args.scriptText || input.scriptText || digitalHumanInput.scriptText || input.content || '');
  const tags = splitTags(args.tags || input.tags || digitalHumanInput.tags);
  const body = {
    topic: buildTopic(input, args),
    vhBizId: String(args.vhBizId || args.modelId || input.vhBizId || input.modelId || digitalHumanInput.vhBizId || digitalHumanInput.modelId || providerVhBizId(env)).trim(),
  };
  if (args.sessionId || input.sessionId) body.sessionId = String(args.sessionId || input.sessionId);
  if (args.traceId || input.traceId) body.traceId = String(args.traceId || input.traceId);
  if (title) body.title = title;
  if (scriptText) body.content = scriptText;
  if (Array.isArray(input.materialList)) body.materialList = input.materialList;
  if (input.ttsConf && typeof input.ttsConf === 'object') body.ttsConf = input.ttsConf;
  if (input.aigcWatermark != null) body.aigcWatermark = Boolean(input.aigcWatermark);
  if (tags.length) body.tags = tags;
  return body;
}

function validateCreateBody(body) {
  const missing = [];
  if (!body.topic) missing.push('topic');
  if (!body.vhBizId) missing.push('vhBizId');
  return missing;
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    signal: AbortSignal.timeout(Number(options.timeoutMs || 30000)),
  });
  const text = await response.text();
  let payload = {};
  if (text) {
    try {
      payload = JSON.parse(text);
    } catch {
      payload = { rawText: text };
    }
  }
  return { ok: response.ok, status: response.status, payload };
}

async function health() {
  try {
    const result = await fetchJson(`${baseUrl()}/health`, { timeoutMs: 3000 });
    return { ok: result.ok, status: result.status, payload: result.payload };
  } catch (err) {
    return { ok: false, error: err.message };
  }
}

function startService() {
  if (!existsSync(join(XIAOICE_TOOL_DIR, 'src', 'service', 'cli.js'))) {
    return { ok: false, error: 'xiaoice_video_tool_missing', toolDir: XIAOICE_TOOL_DIR };
  }
  mkdirSync(join(STATE_DIR, 'logs'), { recursive: true });
  const logPath = join(STATE_DIR, 'logs', `xiaoice-video-service-${Date.now()}.log`);
  const logFd = openSync(logPath, 'a');
  const child = spawn(process.execPath, ['src/service/cli.js'], {
    cwd: XIAOICE_TOOL_DIR,
    detached: true,
    stdio: ['ignore', logFd, logFd],
    env: {
      ...process.env,
      ...loadEnvFile(XIAOICE_ENV_PATH),
      PATH: `${dirname(process.execPath)}:${process.env.PATH || ''}`,
    },
  });
  child.unref();
  return { ok: true, pid: child.pid, logPath };
}

async function ensureService(opts = {}) {
  const current = await health();
  if (current.ok) return { ok: true, alreadyRunning: true, health: current };
  if (opts.noStart) return { ok: false, health: current, error: 'service_not_running' };
  const started = startService();
  if (!started.ok) return { ok: false, started, health: current };
  let next = current;
  for (let i = 0; i < 20; i += 1) {
    await new Promise((resolve) => setTimeout(resolve, 500));
    next = await health();
    if (next.ok) return { ok: true, alreadyRunning: false, started, health: next };
  }
  return { ok: false, started, health: next, error: 'service_start_timeout' };
}

async function serviceRequest(path, options = {}) {
  const token = internalToken();
  if (!token) throw new Error('VIDEO_SERVICE_INTERNAL_TOKEN is missing');
  const result = await fetchJson(`${baseUrl()}${path}`, {
    method: options.method || 'GET',
    headers: {
      'Content-Type': 'application/json',
      'X-Internal-Token': token,
    },
    body: options.body == null ? undefined : JSON.stringify(options.body),
    timeoutMs: options.timeoutMs || 60000,
  });
  if (!result.ok) {
    const message = result.payload?.error?.message || result.payload?.message || `HTTP ${result.status}`;
    const err = new Error(message);
    err.status = result.status;
    err.payload = result.payload;
    throw err;
  }
  return result.payload?.data || result.payload;
}

function normalizeTask(record) {
  return {
    taskId: String(record?.taskId || ''),
    providerTaskId: String(record?.providerTaskId || ''),
    status: String(record?.status || ''),
    videoUrl: String(record?.videoUrl || ''),
    coverImageUrl: String(record?.coverImageUrl || record?.previewImageUrl || record?.coverUrl || ''),
    errorMessage: String(record?.errorMessage || ''),
    traceId: String(record?.traceId || ''),
    sessionId: String(record?.sessionId || ''),
    createdAt: record?.createdAt ?? null,
    updatedAt: record?.updatedAt ?? null,
    finishedAt: record?.finishedAt ?? null,
  };
}

async function createTask(body) {
  const data = await serviceRequest('/v1/tasks', { method: 'POST', body, timeoutMs: 60000 });
  return normalizeTask(data);
}

async function getTask(taskId) {
  const data = await serviceRequest(`/v1/tasks/${encodeURIComponent(taskId)}`, { timeoutMs: 30000 });
  return normalizeTask(data);
}

function deepFindVideoUrl(value) {
  if (!value) return '';
  if (typeof value === 'string') {
    return /^https?:\/\/.+\.(mp4|mov|m4v|webm)(\?|$)/i.test(value) ? value : '';
  }
  if (Array.isArray(value)) {
    for (const item of value) {
      const found = deepFindVideoUrl(item);
      if (found) return found;
    }
    return '';
  }
  if (typeof value === 'object') {
    for (const key of ['videoUrl', 'video_url', 'url', 'outputUrl', 'outputURL']) {
      const found = deepFindVideoUrl(value[key]);
      if (found) return found;
    }
    for (const item of Object.values(value)) {
      const found = deepFindVideoUrl(item);
      if (found) return found;
    }
  }
  return '';
}

function deepFindImageUrl(value) {
  if (!value) return '';
  if (typeof value === 'string') {
    return /^https?:\/\/.+\.(png|jpe?g|webp)(\?|$)/i.test(value) ? value : '';
  }
  if (Array.isArray(value)) {
    for (const item of value) {
      const found = deepFindImageUrl(item);
      if (found) return found;
    }
    return '';
  }
  if (typeof value === 'object') {
    for (const key of ['previewImageUrl', 'preview_image_url', 'coverImageUrl', 'coverUrl', 'imageUrl', 'image_url', 'posterUrl', 'poster']) {
      const found = deepFindImageUrl(value[key]);
      if (found) return found;
    }
    for (const item of Object.values(value)) {
      const found = deepFindImageUrl(item);
      if (found) return found;
    }
  }
  return '';
}

async function providerDetail(providerTaskId) {
  const env = mergedEnv();
  const apiBase = String(env.VIDEO_PROVIDER_API_BASE_URL || '').replace(/\/+$/, '');
  const apiKey = String(env.VIDEO_PROVIDER_API_KEY || '').trim();
  if (!apiBase || !apiKey || !providerTaskId) return { ok: false, skipped: true, reason: 'provider_detail_not_configured' };
  const headerName = String(env.VIDEO_PROVIDER_AUTH_HEADER || 'X-API-Key').trim();
  const url = `${apiBase}/openapi/aivideo/detail/${encodeURIComponent(providerTaskId)}`;
  try {
    const result = await fetchJson(url, {
      headers: { [headerName]: apiKey },
      timeoutMs: 30000,
    });
    const videoUrl = deepFindVideoUrl(result.payload);
    const coverImageUrl = deepFindImageUrl(result.payload);
    return {
      ok: result.ok,
      status: result.status,
      providerStatus: result.payload?.data?.status || result.payload?.status || '',
      videoUrl,
      coverImageUrl,
      payload: result.payload,
    };
  } catch (err) {
    return { ok: false, error: err.message };
  }
}

function isTerminal(task) {
  return ['succeeded', 'failed', 'timeout'].includes(String(task?.status || '').toLowerCase());
}

function providerLooksRunning(detail) {
  const status = String(detail?.providerStatus || detail?.payload?.data?.status || detail?.payload?.data?.displayStatus || '').trim().toUpperCase();
  if (!status) return false;
  if (detail?.videoUrl) return false;
  const err = String(detail?.payload?.data?.errMsg || detail?.payload?.error?.message || detail?.payload?.message || '').trim();
  if (err && err !== '成功') return false;
  return status.includes('ING') || status.includes('RUNNING') || status.includes('PROCESS');
}

async function waitTask(taskId, opts = {}) {
  const startedAt = Date.now();
  const timeoutMs = Math.max(10_000, Number(opts.timeoutSec || 900) * 1000);
  const intervalMs = Math.max(1000, Number(opts.intervalSec || 5) * 1000);
  let last = null;
  let lastProvider = null;
  while (Date.now() - startedAt < timeoutMs) {
    last = await getTask(taskId);
    if (last.providerTaskId) {
      lastProvider = await providerDetail(last.providerTaskId);
      if (lastProvider.videoUrl) {
        last = { ...last, status: 'succeeded', videoUrl: lastProvider.videoUrl, coverImageUrl: last.coverImageUrl || lastProvider.coverImageUrl || '' };
        break;
      }
      if (lastProvider.coverImageUrl && !last.coverImageUrl) last = { ...last, coverImageUrl: lastProvider.coverImageUrl };
      if (String(last.status || '').toLowerCase() === 'timeout' && providerLooksRunning(lastProvider)) {
        last = { ...last, status: 'processing', errorMessage: '' };
      }
    }
    if (last.videoUrl || isTerminal(last)) break;
    await new Promise((resolve) => setTimeout(resolve, intervalMs));
  }
  if (last?.providerTaskId) {
    lastProvider = await providerDetail(last.providerTaskId);
    if (lastProvider.coverImageUrl) last = { ...last, coverImageUrl: lastProvider.coverImageUrl };
    if (!last.videoUrl && lastProvider.videoUrl) last = { ...last, status: 'succeeded', videoUrl: lastProvider.videoUrl };
    if (!last.videoUrl && String(last.status || '').toLowerCase() === 'timeout' && providerLooksRunning(lastProvider)) {
      last = { ...last, status: 'processing', errorMessage: '' };
    }
  }
  return {
    ok: Boolean(last?.videoUrl || last?.status === 'succeeded'),
    timedOut: !(last?.videoUrl || isTerminal(last)) && Date.now() - startedAt >= timeoutMs,
    elapsedMs: Date.now() - startedAt,
    task: last,
    providerDetail: lastProvider,
  };
}

function publishText(task, input = {}, args = {}) {
  const title = publishTitleFrom(input, args, input.digitalHumanInput || {}) || '数字人成片测试';
  const tags = splitTags(args.publishTags || args.tags || input.publishFields?.tags || input.tags || input.digitalHumanInput?.tags).join('');
  const cover = String(args.coverImage || args.coverUrl || input['封面图片'] || input.coverImage || input.coverUrl || input.publishFields?.coverImage || task.coverImageUrl || '').trim();
  const lines = [
    tags ? `tags:${tags}` : '',
    cover ? `"封面图片": "${cover}"` : '',
    `标题："${title}"`,
    `"视频地址": "${task.videoUrl}"`,
  ].filter(Boolean);
  return lines.join('\n');
}

async function main() {
  const [command = 'health', ...rest] = process.argv.slice(2);
  const args = parseArgs(rest);
  const input = parseJsonInput(args);

  if (command === 'health') {
    const ensured = await ensureService({ noStart: args.noStart });
    console.log(JSON.stringify({ ok: ensured.ok, action: 'health', service: ensured }, null, 2));
    if (!ensured.ok) process.exitCode = 1;
    return;
  }

  const service = await ensureService({ noStart: args.noStart });
  if (!service.ok) {
    console.log(JSON.stringify({ ok: false, action: command, error: service.error || 'service_unavailable', service }, null, 2));
    process.exit(1);
  }

  if (command === 'create' || command === 'create-and-wait') {
    const body = buildCreateBody(input, args);
    const missing = validateCreateBody(body);
    if (args.dryRun) {
      const task = {
        taskId: `dry-${Date.now()}`,
        providerTaskId: 'dry-provider-task',
        status: 'succeeded',
        videoUrl: args.fakeVideoUrl || 'https://example.com/dry-run.mp4',
        coverImageUrl: args.fakeCoverImageUrl || '',
      };
      const result = {
        ok: true,
        dryRun: true,
        action: command,
        request: { ...body, vhBizId: body.vhBizId ? '<configured>' : '' },
        task,
        publishText: publishText(task, input, args),
      };
      console.log(JSON.stringify(result, null, 2));
      return;
    }
    if (missing.length) {
      console.log(JSON.stringify({ ok: false, action: command, error: 'missing_required_fields', missing }, null, 2));
      process.exit(1);
      return;
    }
    const task = await createTask(body);
    const wait = command === 'create-and-wait'
      ? await waitTask(task.taskId, args)
      : null;
    const finalTask = wait?.task || task;
    const result = {
      ok: command === 'create' ? Boolean(task.taskId) : Boolean(wait?.ok),
      action: command,
      task: finalTask,
      wait,
      publishText: finalTask?.videoUrl ? publishText(finalTask, input, args) : '',
    };
    if (result.wait?.providerDetail?.coverImageUrl && result.task && !result.task.coverImageUrl) {
      result.task.coverImageUrl = result.wait.providerDetail.coverImageUrl;
      result.publishText = result.task.videoUrl ? publishText(result.task, input, args) : '';
    }
    mkdirSync(JOB_DIR, { recursive: true });
    writeFileSync(join(JOB_DIR, `${task.taskId}.json`), `${JSON.stringify(result, null, 2)}\n`);
    console.log(JSON.stringify(result, null, 2));
    if (!result.ok) process.exitCode = 1;
    return;
  }

  if (command === 'get' || command === 'wait') {
    const taskId = String(args.taskId || input.taskId || args._[0] || '').trim();
    if (!taskId) throw new Error('taskId is required');
    const result = command === 'wait'
      ? await waitTask(taskId, args)
      : { ok: true, task: await getTask(taskId) };
    if (result.task?.providerTaskId && !result.task.coverImageUrl) {
      const detail = await providerDetail(result.task.providerTaskId);
      result.providerDetail = result.providerDetail || detail;
      if (detail.coverImageUrl || detail.videoUrl) {
        result.task = {
          ...result.task,
          coverImageUrl: result.task.coverImageUrl || detail.coverImageUrl || '',
          videoUrl: result.task.videoUrl || detail.videoUrl || '',
        };
      }
    }
    result.publishText = result.task?.videoUrl ? publishText(result.task, input, args) : '';
    console.log(JSON.stringify(result, null, 2));
    if (!result.ok) process.exitCode = 1;
    return;
  }

  console.error('Usage: node scripts/xiaoice-video-produce.js health|create|wait|get|create-and-wait [--input-json file] [--title ...] [--script-text ...]');
  process.exit(2);
}

main().catch((err) => {
  console.log(JSON.stringify({ ok: false, error: err.message, stack: err.stack }, null, 2));
  process.exit(1);
});
