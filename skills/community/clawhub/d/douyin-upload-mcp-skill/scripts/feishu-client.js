import { appendFileSync, readFileSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { basename, dirname, join } from 'node:path';
import { homedir } from 'node:os';
import '../src/config.js';

const FEISHU_BASE_URL = 'https://open.feishu.cn/open-apis';
const STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(homedir(), '.openclaw', 'workspace', 'douyin-ops');
const BOUND_TARGET_PATH = process.env.DOUYIN_FEISHU_BOUND_TARGET_PATH || join(STATE_DIR, 'feishu-bound-target.json');

function readJson(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}

function pickConfiguredFeishuAccount() {
  const configPath = process.env.OPENCLAW_CONFIG_PATH || join(process.env.HOME || '.', '.openclaw', 'openclaw.json');
  if (!existsSync(configPath)) return {};

  const cfg = readJson(configPath);
  const feishu = cfg.channels?.feishu;
  if (!feishu) return {};

  const accountId = process.env.FEISHU_ACCOUNT_ID || feishu.defaultAccount;
  const account = accountId ? feishu.accounts?.[accountId] : undefined;
  return {
    accountId,
    appId: account?.appId || feishu.appId,
    appSecret: account?.appSecret || feishu.appSecret,
  };
}

function pickBoundFeishuTarget() {
  try {
    if (!existsSync(BOUND_TARGET_PATH)) return {};
    const bound = readJson(BOUND_TARGET_PATH);
    return {
      receiveId: bound.receiveId,
      receiveIdType: bound.receiveIdType || 'chat_id',
    };
  } catch {
    return {};
  }
}

export function resolveFeishuConfig(overrides = {}) {
  const configured = pickConfiguredFeishuAccount();
  const bound = pickBoundFeishuTarget();
  return {
    appId: overrides.appId || configured.appId || process.env.FEISHU_APP_ID,
    appSecret: overrides.appSecret || configured.appSecret || process.env.FEISHU_APP_SECRET,
    receiveId: overrides.receiveId || bound.receiveId || process.env.DOUYIN_FEISHU_RECEIVE_ID || process.env.FEISHU_RECEIVE_ID,
    receiveIdType: overrides.receiveIdType || bound.receiveIdType || process.env.DOUYIN_FEISHU_RECEIVE_ID_TYPE || process.env.FEISHU_RECEIVE_ID_TYPE || 'open_id',
    dryRun: overrides.dryRun ?? (process.env.FEISHU_DRY_RUN === 'true'),
  };
}

export function buildFeishuScopeAuthUrl(scopes, cfg = resolveFeishuConfig()) {
  if (!cfg.appId) {
    throw new Error('Feishu appId is not configured');
  }
  const query = Array.isArray(scopes) ? scopes.join(',') : String(scopes || '');
  return `https://open.feishu.cn/app/${encodeURIComponent(cfg.appId)}/auth?q=${encodeURIComponent(query)}&op_from=openapi&token_type=tenant`;
}

function requireTarget(cfg) {
  if (!cfg.receiveId) return false;
  if (!cfg.appId || !cfg.appSecret) return false;
  return true;
}

async function feishuFetch(url, opts = {}) {
  const res = await fetch(url, opts);
  const text = await res.text();
  let body;
  try {
    body = text ? JSON.parse(text) : {};
  } catch {
    body = { raw: text };
  }
  if (!res.ok) {
    throw new Error(`Feishu HTTP ${res.status}: ${text.slice(0, 500)}`);
  }
  return body;
}

export async function callFeishuOpenApi(pathOrUrl, opts = {}, cfg = resolveFeishuConfig()) {
  const token = await getTenantAccessToken(cfg);
  const url = /^https?:\/\//.test(pathOrUrl)
    ? pathOrUrl
    : `${FEISHU_BASE_URL}${pathOrUrl.startsWith('/') ? pathOrUrl : `/${pathOrUrl}`}`;
  const headers = {
    Authorization: `Bearer ${token}`,
    ...(opts.body ? { 'Content-Type': 'application/json; charset=utf-8' } : {}),
    ...(opts.headers || {}),
  };
  return feishuFetch(url, {
    ...opts,
    headers,
    body: opts.body && typeof opts.body !== 'string' ? JSON.stringify(opts.body) : opts.body,
  });
}

async function feishuBinaryFetch(url, opts = {}) {
  const res = await fetch(url, opts);
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`Feishu HTTP ${res.status}: ${text.slice(0, 500)}`);
  }
  return Buffer.from(await res.arrayBuffer());
}

export async function getTenantAccessToken(cfg = resolveFeishuConfig()) {
  if (!cfg.appId || !cfg.appSecret) {
    throw new Error('Feishu appId/appSecret is not configured');
  }
  const body = await feishuFetch(`${FEISHU_BASE_URL}/auth/v3/tenant_access_token/internal`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
    body: JSON.stringify({
      app_id: cfg.appId,
      app_secret: cfg.appSecret,
    }),
  });
  if (body.code !== 0 || !body.tenant_access_token) {
    throw new Error(`Feishu token failed: ${body.msg || `code ${body.code}`}`);
  }
  return body.tenant_access_token;
}

export async function sendFeishuText(text, cfg = resolveFeishuConfig()) {
  if (!requireTarget(cfg) || cfg.dryRun) {
    if (process.env.FEISHU_DRY_RUN_LOG) {
      appendFileSync(process.env.FEISHU_DRY_RUN_LOG, `${JSON.stringify({
        ts: new Date().toISOString(),
        type: 'text',
        text,
      })}\n`);
    }
    return { ok: true, dryRun: true, type: 'text', text };
  }

  const token = await getTenantAccessToken(cfg);
  const body = await feishuFetch(`${FEISHU_BASE_URL}/im/v1/messages?receive_id_type=${encodeURIComponent(cfg.receiveIdType)}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json; charset=utf-8',
    },
    body: JSON.stringify({
      receive_id: cfg.receiveId,
      msg_type: 'text',
      content: JSON.stringify({ text }),
    }),
  });
  if (body.code !== 0) throw new Error(`Feishu text send failed: ${body.msg || `code ${body.code}`}`);
  return { ok: true, dryRun: false, type: 'text', messageId: body.data?.message_id };
}

function splitTextByLength(text, maxLength) {
  const raw = String(text || '');
  const limit = Math.max(1000, Number(maxLength || 7000));
  if (Array.from(raw).length <= limit) return [raw];
  const chunks = [];
  let rest = raw;
  while (Array.from(rest).length > limit) {
    const chars = Array.from(rest);
    const candidate = chars.slice(0, limit).join('');
    const breakpoints = [
      candidate.lastIndexOf('\n\n'),
      candidate.lastIndexOf('\n'),
      candidate.lastIndexOf('。'),
      candidate.lastIndexOf('；'),
    ].filter((idx) => idx > limit * 0.45);
    const cut = breakpoints.length ? Math.max(...breakpoints) + 1 : candidate.length;
    chunks.push(rest.slice(0, cut).trimEnd());
    rest = rest.slice(cut).trimStart();
  }
  if (rest) chunks.push(rest);
  return chunks;
}

export async function sendFeishuTextChunks(text, cfg = resolveFeishuConfig(), opts = {}) {
  const chunks = splitTextByLength(text, opts.maxLength || process.env.FEISHU_TEXT_CHUNK_MAX_CHARS || 7000);
  if (chunks.length <= 1) return sendFeishuText(text, cfg);
  const results = [];
  for (let i = 0; i < chunks.length; i += 1) {
    const prefix = `(${i + 1}/${chunks.length}) `;
    results.push(await sendFeishuText(`${prefix}${chunks[i]}`, cfg));
  }
  return { ok: results.every((item) => item.ok), type: 'text_chunks', count: chunks.length, results };
}

export async function uploadFeishuImage(filePath, cfg = resolveFeishuConfig()) {
  const token = await getTenantAccessToken(cfg);
  const buffer = readFileSync(filePath);
  const form = new FormData();
  form.append('image_type', 'message');
  form.append('image', new Blob([buffer], { type: 'image/png' }), basename(filePath));

  const body = await feishuFetch(`${FEISHU_BASE_URL}/im/v1/images`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });
  const imageKey = body.image_key || body.data?.image_key;
  if (body.code !== 0 || !imageKey) {
    throw new Error(`Feishu image upload failed: ${body.msg || `code ${body.code}`}`);
  }
  return imageKey;
}

export async function sendFeishuImage(filePath, cfg = resolveFeishuConfig()) {
  if (!requireTarget(cfg) || cfg.dryRun) {
    if (process.env.FEISHU_DRY_RUN_LOG) {
      appendFileSync(process.env.FEISHU_DRY_RUN_LOG, `${JSON.stringify({
        ts: new Date().toISOString(),
        type: 'image',
        filePath,
      })}\n`);
    }
    return { ok: true, dryRun: true, type: 'image', filePath };
  }

  const token = await getTenantAccessToken(cfg);
  const imageKey = await uploadFeishuImage(filePath, cfg);
  const body = await feishuFetch(`${FEISHU_BASE_URL}/im/v1/messages?receive_id_type=${encodeURIComponent(cfg.receiveIdType)}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json; charset=utf-8',
    },
    body: JSON.stringify({
      receive_id: cfg.receiveId,
      msg_type: 'image',
      content: JSON.stringify({ image_key: imageKey }),
    }),
  });
  if (body.code !== 0) throw new Error(`Feishu image send failed: ${body.msg || `code ${body.code}`}`);
  return { ok: true, dryRun: false, type: 'image', messageId: body.data?.message_id, imageKey };
}

export async function uploadFeishuFile(filePath, cfg = resolveFeishuConfig()) {
  const token = await getTenantAccessToken(cfg);
  const buffer = readFileSync(filePath);
  const fileName = basename(filePath);
  const form = new FormData();
  form.append('file_type', 'stream');
  form.append('file_name', fileName);
  form.append('file', new Blob([buffer], { type: 'application/octet-stream' }), fileName);

  const body = await feishuFetch(`${FEISHU_BASE_URL}/im/v1/files`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });
  const fileKey = body.file_key || body.data?.file_key;
  if (body.code !== 0 || !fileKey) {
    throw new Error(`Feishu file upload failed: ${body.msg || `code ${body.code}`}`);
  }
  return fileKey;
}

export async function sendFeishuFile(filePath, cfg = resolveFeishuConfig()) {
  if (!requireTarget(cfg) || cfg.dryRun) {
    if (process.env.FEISHU_DRY_RUN_LOG) {
      appendFileSync(process.env.FEISHU_DRY_RUN_LOG, `${JSON.stringify({
        ts: new Date().toISOString(),
        type: 'file',
        filePath,
      })}\n`);
    }
    return { ok: true, dryRun: true, type: 'file', filePath };
  }

  const token = await getTenantAccessToken(cfg);
  const fileKey = await uploadFeishuFile(filePath, cfg);
  const body = await feishuFetch(`${FEISHU_BASE_URL}/im/v1/messages?receive_id_type=${encodeURIComponent(cfg.receiveIdType)}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json; charset=utf-8',
    },
    body: JSON.stringify({
      receive_id: cfg.receiveId,
      msg_type: 'file',
      content: JSON.stringify({ file_key: fileKey }),
    }),
  });
  if (body.code !== 0) throw new Error(`Feishu file send failed: ${body.msg || `code ${body.code}`}`);
  return { ok: true, dryRun: false, type: 'file', messageId: body.data?.message_id, fileKey };
}

export async function listFeishuMessages(opts = {}, cfg = resolveFeishuConfig()) {
  if (!requireTarget(cfg)) {
    throw new Error('Feishu receive target is not configured');
  }
  const token = await getTenantAccessToken(cfg);
  const end = opts.endTime || Math.floor(Date.now() / 1000);
  const start = opts.startTime || end - Number(opts.sinceSeconds || 300);
  const url = new URL(`${FEISHU_BASE_URL}/im/v1/messages`);
  url.searchParams.set('container_id_type', 'chat');
  url.searchParams.set('container_id', cfg.receiveId);
  url.searchParams.set('start_time', String(start));
  url.searchParams.set('end_time', String(end));
  url.searchParams.set('page_size', String(opts.pageSize || 50));
  if (opts.pageToken) url.searchParams.set('page_token', opts.pageToken);

  const body = await feishuFetch(url, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (body.code !== 0) throw new Error(`Feishu message list failed: ${body.msg || `code ${body.code}`}`);
  return body.data || { items: [] };
}

export async function getFeishuMessage(messageId, cfg = resolveFeishuConfig()) {
  const token = await getTenantAccessToken(cfg);
  const body = await feishuFetch(`${FEISHU_BASE_URL}/im/v1/messages/${encodeURIComponent(messageId)}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (body.code !== 0) throw new Error(`Feishu message get failed: ${body.msg || `code ${body.code}`}`);
  return body.data?.items?.[0] || null;
}

export async function downloadFeishuMessageResource(messageId, fileKey, opts = {}, cfg = resolveFeishuConfig()) {
  if (!messageId || !fileKey) {
    throw new Error('messageId and fileKey are required');
  }
  if (!opts.outputPath) {
    throw new Error('outputPath is required');
  }
  const token = await getTenantAccessToken(cfg);
  const type = opts.type || 'file';
  const url = new URL(`${FEISHU_BASE_URL}/im/v1/messages/${encodeURIComponent(messageId)}/resources/${encodeURIComponent(fileKey)}`);
  url.searchParams.set('type', type);
  const buffer = await feishuBinaryFetch(url, {
    headers: { Authorization: `Bearer ${token}` },
  });
  mkdirSync(dirname(opts.outputPath), { recursive: true });
  writeFileSync(opts.outputPath, buffer);
  return {
    ok: true,
    messageId,
    fileKey,
    type,
    outputPath: opts.outputPath,
    bytes: buffer.length,
  };
}
