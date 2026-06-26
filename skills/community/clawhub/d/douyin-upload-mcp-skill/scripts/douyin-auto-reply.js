#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { spawnSync } from 'node:child_process';
import { homedir } from 'node:os';
import { shouldDeferToPublish } from './browser-task-lock.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(homedir(), '.openclaw', 'workspace', 'douyin-ops');
const STATE_PATH = process.env.DOUYIN_AUTO_REPLY_STATE || join(STATE_DIR, 'auto-reply-state.json');

function usage() {
  console.error(`Usage:
  node scripts/douyin-auto-reply.js comment [--execute] [--limit 1] [--force]
  node scripts/douyin-auto-reply.js dm [--execute] [--limit 1] [--force]
  node scripts/douyin-auto-reply.js both [--execute] [--limit 1] [--force]
	  node scripts/douyin-auto-reply.js preview --kind comment --text "粉丝评论"
	
Default is dry-run. Add --execute only when real auto reply is allowed.
	  Comment auto-reply defaults to the creator-center unread/unreplied comment queue.
	  Scanning skips already replied or own messages and continues until all visible pending targets are handled or the configured cap is reached.
Reply text uses AI prompt generation by default. Deterministic rule fallback is only allowed with --allow-rules-fallback or DOUYIN_AUTO_REPLY_ALLOW_RULES_FALLBACK=true.
	`);
}

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

export function loadState() {
  if (!existsSync(STATE_PATH)) return { replied: {}, dmConversations: {} };
  try {
    const state = { replied: {}, dmConversations: {}, ...JSON.parse(readFileSync(STATE_PATH, 'utf8')) };
    for (const [key, value] of Object.entries(state.replied || {})) {
      const match = /^dm:(\d+):/.exec(key);
      if (!match || !value?.reply) continue;
      const index = match[1];
      const existing = state.dmConversations[index];
      if (!existing || String(value.at || '') > String(existing.at || '')) {
        state.dmConversations[index] = {
          at: value.at,
          lastReply: value.reply,
          lastSourceText: value.sourceText,
          migrated: true,
        };
      }
    }
    return state;
  } catch {
    return { replied: {}, dmConversations: {} };
  }
}

export function saveState(state) {
  mkdirSync(STATE_DIR, { recursive: true });
  const entries = Object.entries(state.replied || {})
    .sort((a, b) => String(b[1]?.at || '').localeCompare(String(a[1]?.at || '')))
    .slice(0, 1000);
  writeFileSync(STATE_PATH, JSON.stringify({
    ...state,
    replied: Object.fromEntries(entries),
    dmConversations: state.dmConversations || {},
    updatedAt: new Date().toISOString(),
  }, null, 2));
}

function runNode(args, timeout = 120_000) {
  const mockDir = process.env.DOUYIN_AUTO_REPLY_MOCK_DIR;
  const scriptName = String(args[0] || '').split('/').pop();
  const command = args[1];
	  if (mockDir && scriptName === 'douyin-dm-reply.js' && command === 'list') {
	    return {
	      ok: true,
	      status: 0,
	      output: readFileSync(join(mockDir, 'dm-list.json'), 'utf8'),
	    };
	  }
	  if (mockDir && scriptName === 'douyin-comment-reply.js' && command === 'list') {
	    return {
	      ok: true,
	      status: 0,
	      output: readFileSync(join(mockDir, 'comment-list.json'), 'utf8'),
	    };
	  }
	  if (mockDir && scriptName === 'douyin-comment-reply.js' && command === 'reply') {
	    const textIndex = args.indexOf('--text');
	    const indexIndex = args.indexOf('--index');
	    const reply = textIndex >= 0 ? args[textIndex + 1] : '';
	    const index = indexIndex >= 0 ? Number(args[indexIndex + 1] || 0) : 0;
	    return {
	      ok: true,
	      status: 0,
	      output: JSON.stringify({
	        ok: true,
	        action: 'comment_reply_sent_verified',
	        target: { index },
	        reply,
	        verification: { ok: true, found: true, sample: reply },
	      }, null, 2),
	    };
	  }
	  if (mockDir && scriptName === 'douyin-dm-reply.js' && command === 'reply') {
    const textIndex = args.indexOf('--text');
    const indexIndex = args.indexOf('--index');
    const reply = textIndex >= 0 ? args[textIndex + 1] : '';
    const index = indexIndex >= 0 ? Number(args[indexIndex + 1] || 0) : 0;
    return {
      ok: true,
      status: 0,
      output: JSON.stringify({
        ok: true,
        action: 'dm_reply_sent_visible',
        target: { index },
        reply,
        verification: { found: true, sample: reply },
      }, null, 2),
    };
  }

  const result = spawnSync(process.execPath, args, {
    cwd: join(__dirname, '..'),
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout,
  });
  return {
    ok: result.status === 0,
    status: result.status,
    output: `${result.stderr || ''}${result.stdout || ''}`.trim(),
  };
}

function sleepSync(ms) {
  const buffer = new SharedArrayBuffer(4);
  const view = new Int32Array(buffer);
  Atomics.wait(view, 0, 0, ms);
}

function looksTransientBrowserError(output) {
  return /Execution context was destroyed|Cannot find context with specified id|Target closed|Navigating frame was detached|Protocol error|net::ERR_ABORTED|timeout/i.test(String(output || ''));
}

function runNodeWithRetry(args, opts = {}) {
  const attempts = Math.max(1, Number(opts.attempts || 1));
  const timeout = Number(opts.timeout || 120_000);
  let last = null;
  for (let attempt = 1; attempt <= attempts; attempt += 1) {
    const result = runNode(args, timeout);
    if (result.ok || !looksTransientBrowserError(result.output) || attempt === attempts) {
      return {
        ...result,
        attempts: attempt,
        transientRetried: attempt > 1,
      };
    }
    last = result;
    sleepSync(1200 * attempt);
  }
  return last;
}

function parseJsonObjects(text) {
  const objects = [];
  let depth = 0;
  let start = -1;
  let inString = false;
  let escaped = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    if (inString) {
      if (escaped) escaped = false;
      else if (ch === '\\') escaped = true;
      else if (ch === '"') inString = false;
      continue;
    }
    if (ch === '"') {
      inString = true;
    } else if (ch === '{') {
      if (depth === 0) start = i;
      depth += 1;
    } else if (ch === '}') {
      depth -= 1;
      if (depth === 0 && start >= 0) {
        const raw = text.slice(start, i + 1);
        try {
          objects.push(JSON.parse(raw));
        } catch {
          // Ignore non-JSON brace spans from logs.
        }
        start = -1;
      }
    }
  }
  return objects;
}

function parseLastJson(text) {
  const objects = parseJsonObjects(text);
  return objects[objects.length - 1] || null;
}

function normalize(text) {
  return String(text || '').replace(/\s+/g, ' ').trim();
}

function stripMeta(text) {
  return normalize(text)
    .replace(/陌生人消息|白日梦想家|作者|粉丝|昨天|今天|刚刚|删除|举报|回复|查看\d+条回复|发布于\d{4}年\d{2}月\d{2}日\s*\d{2}:\d{2}/g, ' ')
    .replace(/\d+\s*(分钟前|小时前|天前)|\d{1,2}:\d{2}|\d{2}月\d{2}日|C:/g, ' ')
    .replace(/\b\d+\b/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function isOwnComment(text) {
  return /作者/.test(text) || /(^|\s)(我|本人)\s*(刚刚|今天|\d+\s*分钟前|\d{1,2}:\d{2})/.test(text);
}

function fingerprintText(text) {
  return stripMeta(text).replace(/[，。！？!?、:：\s]+/g, ' ').trim().slice(0, 200);
}

function commentFingerprint(row, text) {
  const author = fingerprintText(row?.authorName || '');
  const body = fingerprintText(text);
  return [author, body].filter(Boolean).join('|') || body;
}

function workIdentity(row = {}) {
  const raw = normalize(row.workKey || row.workText || row.workTitle || '');
  if (!raw) return '';
  const text = raw.replace(/\s+\d+$/, '').trim();
  const published = text.match(/发布于\d{4}年\d{2}月\d{2}日\s*\d{2}:\d{2}/)?.[0] || '';
  const title = text.replace(/\s*发布于.*$/, '').trim();
  return [title, published].filter(Boolean).join('|') || fingerprintText(text);
}

function sameWorkScope(currentRow = {}, previousRow = {}) {
  const current = workIdentity(currentRow);
  if (!current) return true;
  const previous = workIdentity(previousRow);
  if (!previous) return false;
  return current === previous;
}

function commentApproxAtMs(row = {}) {
  if (row.commentApproxAt) {
    const fixed = Date.parse(row.commentApproxAt);
    if (Number.isFinite(fixed)) return fixed;
  }
  const raw = normalize(row.commentTime || '');
  const now = Date.now();
  if (!raw) return null;
  if (/刚刚/.test(raw)) return now;
  let match = raw.match(/(\d+)\s*分钟前/);
  if (match) return now - Number(match[1]) * 60 * 1000;
  match = raw.match(/(\d+)\s*小时前/);
  if (match) return now - Number(match[1]) * 60 * 60 * 1000;
  match = raw.match(/(\d+)\s*天前/);
  if (match) return now - Number(match[1]) * 24 * 60 * 60 * 1000;
  match = raw.match(/^(\d{1,2}):(\d{2})$/);
  if (match) {
    const date = new Date();
    date.setHours(Number(match[1]), Number(match[2]), 0, 0);
    if (date.getTime() > now + 10 * 60 * 1000) date.setDate(date.getDate() - 1);
    return date.getTime();
  }
  match = raw.match(/(\d{1,2})月(\d{1,2})日\s*(\d{1,2}):(\d{2})?/);
  if (match) {
    const date = new Date();
    date.setMonth(Number(match[1]) - 1, Number(match[2]));
    date.setHours(Number(match[3] || 0), Number(match[4] || 0), 0, 0);
    if (date.getTime() > now + 24 * 60 * 60 * 1000) date.setFullYear(date.getFullYear() - 1);
    return date.getTime();
  }
  return null;
}

function commentOccurrenceKey(row = {}) {
  const approx = commentApproxAtMs(row);
  if (!Number.isFinite(approx)) return '';
  const bucketMs = 10 * 60 * 1000;
  return String(Math.round(approx / bucketMs));
}

export function withCommentReplyMeta(row = {}) {
  const approx = commentApproxAtMs(row);
  const workKey = workIdentity(row);
  return {
    authorName: row.authorName,
    commentTime: row.commentTime,
    commentText: row.commentText,
    commentApproxAt: Number.isFinite(approx) ? new Date(approx).toISOString() : undefined,
    workIndex: row.workIndex,
    workTitle: row.workTitle,
    workText: row.workText,
    workKey: workKey || undefined,
  };
}

function normalizeDmLatestText(text) {
  return stripMeta(text).replace(/[，。！？!?、:：\s]+/g, ' ').trim();
}

function normalizeReplyFingerprint(text) {
  return normalize(text).replace(/[，。！？!?、:：,.]/g, ' ').replace(/\s+/g, ' ').trim();
}

const DM_SELF_REPLY_FINGERPRINTS = new Set([
  '你好 请问想了解哪方面',
  '你好 宠物险方案和价格会按需求不同变化 你想了解保障内容 价格 还是投保流程',
  '你好 我在 请问想了解哪方面',
  '收到 这个问题我看到了 你可以再补充一下具体情况 我好给你更准确的回复',
  '谢谢支持',
  '收到 我看到了 请问还想了解哪方面',
]);

function dmLatestLooksOwnReply(sourceText) {
  const text = normalizeReplyFingerprint(stripMeta(sourceText));
  if (!text) return false;
  if (DM_SELF_REPLY_FINGERPRINTS.has(text)) return true;
  for (const reply of DM_SELF_REPLY_FINGERPRINTS) {
    if (text.includes(reply)) return true;
  }
  return false;
}

function dmLooksUnread(row) {
  if (row?.unread === true) return true;
  return /未读|陌生人消息/.test(String(row?.sample || ''));
}

function dmReplySourceText(row = {}) {
  return normalize(row.latestText || row.messageText || row.text || row.sample || '');
}

function generateDeterministicReply(kind, rawText) {
  const text = stripMeta(rawText);
  if (!text) return kind === 'dm' ? '你好，请问想了解哪方面？' : '感谢你的留言。';
  if (/多少钱|价格|保费|怎么买|购买|链接|投保|保险|宠物险|方案|报价/.test(text)) {
    return kind === 'dm'
      ? '你好，宠物险方案和价格会按需求不同变化。你想了解保障内容、价格，还是投保流程？'
      : '感谢关注，具体方案和价格可以私信我了解。';
  }
  if (/你好|您好|在吗|在不在|hi|hello/i.test(text)) {
    return kind === 'dm' ? '你好，我在。请问想了解哪方面？' : '你好，感谢留言。';
  }
  if (/哈哈|hhh|笑死|有意思|好玩|可爱/.test(text)) {
    return '哈哈，谢谢互动。';
  }
  if (/nb|牛|厉害|强|666|优秀/i.test(text)) {
    return '谢谢认可。';
  }
  if (/[?？]|怎么|为什么|能不能|可以吗|靠谱吗|有用吗/.test(text)) {
    return kind === 'dm'
      ? '收到，这个问题我看到了。你可以再补充一下具体情况，我好给你更准确的回复。'
      : '这个问题可以私信我，我给你更具体地说。';
  }
  if (/谢谢|感谢|支持|不错|喜欢|赞|好/.test(text)) {
    return '谢谢支持。';
  }
  return kind === 'dm' ? '收到，我看到了。请问还想了解哪方面？' : '感谢你的留言。';
}

function loadOpenClawLlmConfig() {
  const candidates = [
    process.env.OPENCLAW_MODELS_PATH,
    join(homedir(), '.openclaw', 'agents', 'main', 'agent', 'models.json'),
    process.env.OPENCLAW_CONFIG_PATH || join(homedir(), '.openclaw', 'openclaw.json'),
  ].filter(Boolean);
  for (const path of candidates) {
    if (!existsSync(path)) continue;
    try {
      const cfg = JSON.parse(readFileSync(path, 'utf8'));
      const providers = cfg.providers || cfg.models?.providers || {};
      const preferredProvider = process.env.DOUYIN_AUTO_REPLY_PROVIDER || process.env.OPENCLAW_PROVIDER || 'custom';
      const entries = [
        [preferredProvider, providers[preferredProvider]],
        ...Object.entries(providers).filter(([key]) => key !== preferredProvider),
      ].filter(([, provider]) => provider?.apiKey && provider?.baseUrl);
      for (const [providerId, provider] of entries) {
        const models = Array.isArray(provider.models) ? provider.models : [];
        const model = process.env.DOUYIN_AUTO_REPLY_MODEL
          || process.env.OPENCLAW_MODEL
          || models.find((item) => item?.id)?.id
          || provider.model
          || 'MiniMax-M2.7';
        return {
          providerId,
          api: provider.api || 'openai-chat-completions',
          apiKey: provider.apiKey,
          rawBaseUrl: provider.baseUrl,
          model,
          sourcePath: path,
        };
      }
    } catch {
      // Ignore malformed optional OpenClaw config and fall back to env.
    }
  }
  return null;
}

function resolveLlmConfig(opts = {}) {
  const mode = String(opts.llm || process.env.DOUYIN_AUTO_REPLY_LLM || 'auto').toLowerCase();
  if (['off', 'false', '0', 'none', 'rule', 'rules'].includes(mode)) {
    return { enabled: false, mode };
  }
  const openclaw = loadOpenClawLlmConfig();
  const apiKey = process.env.DOUYIN_AUTO_REPLY_API_KEY
    || openclaw?.apiKey
    || process.env.MINIMAX_API_KEY
    || process.env.OPENAI_API_KEY
    || '';
  const rawBaseUrl = opts.baseUrl
    || process.env.DOUYIN_AUTO_REPLY_BASE_URL
    || openclaw?.rawBaseUrl
    || process.env.MINIMAX_API_BASE_URL
    || process.env.OPENAI_BASE_URL
    || process.env.OPENAI_API_BASE
    || '';
  const model = opts.model
    || process.env.DOUYIN_AUTO_REPLY_MODEL
    || openclaw?.model
    || process.env.MINIMAX_MODEL
    || process.env.OPENCLAW_MODEL
    || process.env.OPENAI_MODEL
    || 'MiniMax-M2.7';
  if (!apiKey || !rawBaseUrl) {
    return { enabled: false, mode, missing: !apiKey ? 'api_key' : 'base_url' };
  }
  const baseUrl = String(rawBaseUrl).replace(/\/+$/, '');
  const api = process.env.DOUYIN_AUTO_REPLY_API || openclaw?.api || 'openai-chat-completions';
  const useOpenAiEndpoint = /minimaxi\.com\/anthropic/.test(baseUrl)
    && api !== 'anthropic-messages';
  const effectiveApi = useOpenAiEndpoint ? 'openai-chat-completions' : api;
  const endpoint = effectiveApi === 'anthropic-messages'
    ? (/\/v1\/messages$/.test(baseUrl) ? baseUrl : `${baseUrl}/v1/messages`)
    : (useOpenAiEndpoint
      ? 'https://api.minimaxi.com/v1/chat/completions'
      : (/\/chat\/completions$/.test(baseUrl) ? baseUrl : `${baseUrl}/chat/completions`));
  return {
    enabled: true,
    mode,
    api: effectiveApi,
    apiKey,
    endpoint,
    model,
    providerId: openclaw?.providerId,
    timeoutMs: Math.max(3000, Math.min(45000, Number(opts.llmTimeoutMs || process.env.DOUYIN_AUTO_REPLY_LLM_TIMEOUT_MS || 30000))),
  };
}

function autoReplySystemPrompt() {
  return [
    '你是抖音创作者账号的互动运营助手，负责给粉丝评论或私信生成一条可直接发送的中文短回复。',
    '目标：自然、真诚、轻松，尽量提升粉丝继续评论/私信的意愿。',
    '硬性要求：',
    '1. 只输出回复正文，不要解释、不要引号、不要编号。',
    '2. 8到32个中文字符左右，最多45个字符；私信可以稍长但仍要简短。',
    '3. 结合粉丝原话和作品内容，不要机械套模板。',
    '4. 可以用一个自然的问题引导继续互动，但不要每条都问。',
    '5. 不要编造渠道、价格、收益、理赔结果或具体保险结论；涉及保险/价格/投保时，只能引导对方补充情况或私信了解。',
    '6. 不要出现“AI/机器人/客服/系统/作为模型”等字样。',
    '7. 不要输出链接、手机号、微信号、诱导加群、点击下方、官方账号、小风车、直播间等内容。',
    '8. 面对质疑或负面评论，先轻微共情，不争辩。',
  ].join('\n');
}

function buildAutoReplyUserPrompt(kind, rawText, context = {}) {
  const payload = {
    interactionType: kind === 'dm' ? '私信' : '视频评论',
    workTitle: context.workTitle || '',
    fanName: context.row?.authorName || '',
    fanText: stripMeta(rawText).slice(0, 300),
    visibleText: normalize(rawText).slice(0, 500),
    desiredStyle: '像真人运营一样简短回复，增加参与感；评论区更轻松，私信更像一对一沟通。',
  };
  return `请根据以下互动生成1条回复：\n${JSON.stringify(payload, null, 2)}`;
}

function sanitizeLlmReply(raw) {
  let text = String(raw || '')
    .replace(/<think>[\s\S]*?<\/think>/gi, ' ')
    .replace(/```[\s\S]*?```/g, ' ')
    .trim();
  text = normalize(text)
    .replace(/^["'“”‘’]+|["'“”‘’]+$/g, '')
    .replace(/^(回复|评论回复|私信回复|答复)\s*[:：]\s*/i, '')
    .replace(/\s+/g, ' ')
    .trim();
  text = text.split(/\n/)[0].trim();
  if (text.includes('</think>')) text = text.split('</think>').pop().trim();
  if (text.includes('<reply>')) {
    const match = text.match(/<reply>([\s\S]*?)<\/reply>/i);
    if (match) text = match[1].trim();
  }
  text = text
    .replace(/(^|[，。！？!?\s])丝我/g, '$1私信我')
    .replace(/(^|[，。！？!?\s])戳我/g, '$1私信我')
    .replace(/私信我私信我/g, '私信我')
    .replace(/~+/g, '～')
    .trim();
  if (text.length > 45) {
    const cut = text.slice(0, 45);
    const punctuation = Math.max(cut.lastIndexOf('。'), cut.lastIndexOf('？'), cut.lastIndexOf('！'), cut.lastIndexOf('，'));
    text = (punctuation >= 12 ? cut.slice(0, punctuation + 1) : cut).trim();
  }
  return text;
}

function replyLooksUnsafe(reply, sourceText) {
  const text = normalize(reply);
  if (!text || text.length < 2) return true;
  if (/https?:\/\/|www\.|微信|VX|v信|手机号|电话|加群|链接|官方账号|下方|小风车|直播间|返现|稳赚|保证|包赔|一定赔|绝对/.test(text)) return true;
  if (/AI|机器人|模型|系统|客服|用户想要|粉丝的|这是一个|好的，?这是|我需要|我可以|回复示例|输出一句|要求[:：]|<\/?think>|<\/?reply>/.test(text)) return true;
  const source = stripMeta(sourceText);
  if (source && normalizeReplyFingerprint(text) === normalizeReplyFingerprint(source)) return true;
  return false;
}

function extractLlmContent(payload) {
  if (payload?.choices?.[0]?.message?.content) return payload.choices[0].message.content;
  if (payload?.choices?.[0]?.text) return payload.choices[0].text;
  if (Array.isArray(payload?.content)) {
    return payload.content
      .filter((item) => item?.type === 'text' && typeof item.text === 'string')
      .map((item) => item.text)
      .join('\n');
  }
  return payload?.reply || '';
}

async function generateLlmReply(kind, rawText, context = {}, opts = {}) {
  const cfg = resolveLlmConfig(opts);
  if (!cfg.enabled) {
    return { ok: false, source: 'rules', reason: cfg.missing ? `llm_missing_${cfg.missing}` : 'llm_disabled' };
  }
  const messages = [
    { role: 'system', content: autoReplySystemPrompt() },
    { role: 'user', content: buildAutoReplyUserPrompt(kind, rawText, context) },
  ];
  const body = cfg.api === 'anthropic-messages'
    ? {
      model: cfg.model,
      system: autoReplySystemPrompt(),
      messages: [{ role: 'user', content: buildAutoReplyUserPrompt(kind, rawText, context) }],
      temperature: Number(process.env.DOUYIN_AUTO_REPLY_TEMPERATURE || 0.65),
      max_tokens: Number(process.env.DOUYIN_AUTO_REPLY_MAX_TOKENS || 1000),
    }
    : {
      model: cfg.model,
      messages,
      temperature: Number(process.env.DOUYIN_AUTO_REPLY_TEMPERATURE || 0.65),
      max_tokens: Number(process.env.DOUYIN_AUTO_REPLY_MAX_TOKENS || 1000),
    };
  try {
    const res = await fetch(cfg.endpoint, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${cfg.apiKey}`,
        'x-api-key': cfg.apiKey,
        'anthropic-version': process.env.DOUYIN_AUTO_REPLY_ANTHROPIC_VERSION || '2023-06-01',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(cfg.timeoutMs),
    });
    const payload = await res.json().catch(() => ({}));
    const content = extractLlmContent(payload);
    const reply = sanitizeLlmReply(content);
    if (!res.ok || replyLooksUnsafe(reply, rawText)) {
      return {
        ok: false,
        source: 'llm',
        model: cfg.model,
        status: res.status,
        reason: !res.ok ? 'llm_http_error' : 'llm_reply_rejected',
        reply,
      };
    }
    return { ok: true, source: 'llm', model: cfg.model, reply };
  } catch (err) {
    return { ok: false, source: 'llm', model: cfg.model, reason: 'llm_request_failed', error: err.message };
  }
}

export async function generateReply(kind, rawText, context = {}, opts = {}) {
  const attempts = Math.max(1, Math.min(5, Number(opts.llmRetries || process.env.DOUYIN_AUTO_REPLY_LLM_RETRIES || 2)));
  let llm = null;
  for (let attempt = 1; attempt <= attempts; attempt += 1) {
    llm = await generateLlmReply(kind, rawText, context, opts);
    if (llm.ok) return { text: llm.reply, source: llm.source, model: llm.model, llmAttempts: attempt };
    if (/llm_disabled|llm_missing_/.test(String(llm.reason || ''))) break;
    if (attempt < attempts) sleepSync(900 * attempt);
  }
  const fallback = generateDeterministicReply(kind, rawText);
  return { text: fallback, source: 'rules', llmFallback: llm, llmAttempts: attempts };
}

export function rulesFallbackAllowed(opts = {}) {
  return Boolean(opts.allowRulesFallback)
    || process.env.DOUYIN_AUTO_REPLY_ALLOW_RULES_FALLBACK === 'true';
}

function replyGenerationRequired(opts = {}) {
  return Boolean(opts.requireLlmReply)
    || process.env.DOUYIN_AUTO_REPLY_REQUIRE_LLM !== 'false';
}

export function keyFor(kind, index, text, row = null) {
  if (kind === 'dm') return `${kind}:${normalize(text).slice(0, 240)}`;
  const occurrence = commentOccurrenceKey(row);
  const work = workIdentity(row || {});
  return `${kind}:${work ? `${work}:` : ''}${commentFingerprint(row, text)}${occurrence ? `|${occurrence}` : ''}`;
}

function replyIsRecent(value, fallbackHours = 72) {
  const at = Date.parse(value?.at || '');
  if (!Number.isFinite(at)) return false;
  const hours = Math.max(1, Number(process.env.DOUYIN_COMMENT_LOCAL_REPLY_TTL_HOURS || fallbackHours));
  return Date.now() - at <= hours * 60 * 60 * 1000;
}

function alreadyReplied(state, kind, text, row = null) {
  if (kind === 'dm') {
    return state.replied?.[keyFor(kind, 0, text, row)] || null;
  }
  const normalized = commentFingerprint(row, text);
  const legacyNormalized = fingerprintText(text);
  const hasAuthorName = Boolean(row?.authorName);
  const currentKey = keyFor(kind, 0, text, row);
  const current = state.replied?.[currentKey] || null;
  const currentApprox = commentApproxAtMs(row);
  const matched = Object.entries(state.replied || {}).find(([key, value]) => {
    if (!key.startsWith(`${kind}:`)) return false;
    if (!sameWorkScope(row || {}, value?.row || {})) return false;
    const baseMatches = commentFingerprint(value?.row, value?.sourceText) === normalized
      || key.includes(`:${normalized}|`)
      || key.endsWith(`:${normalized}`)
      || (!hasAuthorName && (
        fingerprintText(value?.sourceText) === legacyNormalized
        || key.endsWith(`:${legacyNormalized}`)
      ));
    if (!baseMatches) return false;
    const previousApprox = commentApproxAtMs(value?.row || {});
    const previousReplyAt = Date.parse(value?.at || '');
    if (Number.isFinite(currentApprox) && Number.isFinite(previousApprox)) {
      return Math.abs(currentApprox - previousApprox) <= 35 * 60 * 1000;
    }
    if (Number.isFinite(currentApprox) && Number.isFinite(previousReplyAt)) {
      return currentApprox <= previousReplyAt + 3 * 60 * 1000;
    }
    return true;
  })?.[1] || null;
  const previous = current || matched;
  if (!previous) return null;
  if (row && row.hasAuthorReply === false && row.hasReplyThread === false && process.env.DOUYIN_COMMENT_TRUST_LOCAL_STATE !== 'true') {
    return replyIsRecent(previous) ? previous : null;
  }
  return previous;
}

function summarizeResult(item, sendResult) {
  const payload = parseLastJson(sendResult.output);
  if (payload?.skipped || payload?.action === 'dm_latest_is_own_reply') {
    return {
      ...item,
      skipped: true,
      reason: payload.action || 'skipped_by_sender',
      sent: false,
      sendStatus: sendResult.status,
      sendAction: payload?.action || null,
      verified: false,
      sendPayload: payload,
    };
  }
  return {
    ...item,
    sent: sendResult.ok,
    sendStatus: sendResult.status,
    sendAction: payload?.action || null,
    verified: Boolean(payload?.verification?.ok || payload?.verification?.found),
    sendPayload: payload,
  };
}

function collectTargets(kind) {
  const script = kind === 'comment' ? 'douyin-comment-reply.js' : 'douyin-dm-reply.js';
	  const listArgs = kind === 'comment'
	    ? [
	      join(__dirname, script),
	      'list',
	      ...(process.env.DOUYIN_COMMENT_SCAN_ALL_WORKS !== 'false' ? ['--all-works'] : []),
	      '--unreplied',
	      '--author-reply-check',
	      '--pages',
	      String(process.env.DOUYIN_COMMENT_SCAN_PAGES || 8),
	      '--max-works',
	      String(process.env.DOUYIN_COMMENT_SCAN_WORKS || 20),
	      ...(process.env.DOUYIN_COMMENT_REPLY_LATEST === 'true' ? ['--latest'] : []),
	    ]
    : [join(__dirname, script), 'list'];
  const listResult = runNodeWithRetry(listArgs, {
    attempts: kind === 'dm' ? 3 : 2,
  });
  const listed = parseLastJson(listResult.output);
  const rows = kind === 'comment' ? (listed?.comments || []) : (listed?.conversations || []);
  return {
    ok: listResult.ok && Boolean(listed?.ok),
    kind,
    listResult,
    listed,
    rows,
  };
}

function sentCount(result) {
  return (result.items || []).filter((item) => item.sent && item.verified).length;
}

function commentFilterResultToAutoReply(payload, opts = {}) {
  const items = [];
  let scannedCount = 0;
  for (const work of payload?.results || []) {
    for (const attempt of work.attempts || []) {
      scannedCount += 1;
      items.push({
        kind: 'comment',
        workIndex: work.index,
        workTitle: work.title,
        sourceText: attempt.target?.commentText || '',
        reply: attempt.reply,
        replySource: attempt.replySource,
        replyModel: attempt.replyModel,
        llmFallback: attempt.llmFallback,
        llmAttempts: attempt.llmAttempts,
        mode: opts.execute ? 'execute' : 'dry-run',
        sent: Boolean(attempt.sent),
        verified: Boolean(attempt.sent && attempt.ok),
        skipped: attempt.action === 'skip_without_llm_reply',
        reason: attempt.error || attempt.action,
        sendAction: attempt.action,
        target: attempt.target,
      });
    }
  }
  return {
    ok: Boolean(payload?.ok),
    kind: 'comment',
    mode: opts.execute ? 'execute' : 'dry-run',
    scannedCount,
    actionableCount: items.filter((item) => !item.skipped).length,
    count: items.length,
    sentCount: items.filter((item) => item.sent && item.verified).length,
    skippedCount: items.filter((item) => item.skipped).length,
    items,
    source: 'reply-unreplied-by-filter',
    raw: payload,
  };
}

async function autoReplyCommentsByFilter(opts) {
  if (shouldDeferToPublish('auto-reply:comment')) {
    return {
      ok: true,
      kind: 'comment',
      mode: opts.execute ? 'execute' : 'dry-run',
      deferred: true,
      reason: 'deferred_to_publish',
      scannedCount: 0,
      actionableCount: 0,
      count: 0,
      sentCount: 0,
      skippedCount: 1,
      items: [{ kind: 'comment', skipped: true, reason: 'deferred_to_publish' }],
      source: 'reply-unreplied-by-filter',
    };
  }
  const limit = Math.min(50, Math.max(1, Number(opts.limit || process.env.DOUYIN_AUTO_REPLY_LIMIT || 50)));
  const maxWorks = Math.min(50, Math.max(1, Number(opts.maxWorks || process.env.DOUYIN_COMMENT_SCAN_WORKS || 20)));
  const args = [
    join(__dirname, 'douyin-comment-reply.js'),
    'reply-unreplied-by-filter',
    '--limit',
    String(limit),
    '--max-works',
    String(maxWorks),
  ];
  if (opts.execute) args.push('--execute');
  if (opts.allowRulesFallback) args.push('--allow-rules-fallback');
  if (opts.llmRetries) args.push('--llm-retries', String(opts.llmRetries));
  if (opts.llmTimeoutMs) args.push('--llm-timeout-ms', String(opts.llmTimeoutMs));
  if (opts.afterReplyWaitMs) args.push('--after-reply-wait-ms', String(opts.afterReplyWaitMs));
  const result = runNodeWithRetry(args, {
    attempts: 2,
    timeout: opts.execute ? 1_800_000 : 420_000,
  });
  const payload = parseLastJson(result.output);
  if (!result.ok || !payload?.ok) {
    return {
      ok: false,
      kind: 'comment',
      mode: opts.execute ? 'execute' : 'dry-run',
      error: 'reply_unreplied_by_filter_failed',
      output: result.output.slice(-3000),
      raw: payload,
    };
  }
  return commentFilterResultToAutoReply(payload, opts);
}

async function autoReplyKind(kind, opts, state) {
  if (shouldDeferToPublish(`auto-reply:${kind}`)) {
    return {
      ok: true,
      kind,
      mode: opts.execute ? 'execute' : 'dry-run',
      deferred: true,
      reason: 'deferred_to_publish',
      scannedCount: 0,
      actionableCount: 0,
      count: 0,
      sentCount: 0,
      skippedCount: 1,
      items: [{ kind, skipped: true, reason: 'deferred_to_publish' }],
    };
  }
  if (kind === 'comment' && process.env.DOUYIN_AUTO_REPLY_COMMENT_FILTER_FLOW !== 'false') {
    return autoReplyCommentsByFilter(opts);
  }
  const limit = Math.min(50, Math.max(1, Number(opts.limit || process.env.DOUYIN_AUTO_REPLY_LIMIT || 50)));
  const maxScan = Math.min(200, Math.max(limit, Number(opts.maxScan || process.env.DOUYIN_AUTO_REPLY_MAX_SCAN || (kind === 'dm' ? 100 : 100))));
  const script = kind === 'comment' ? 'douyin-comment-reply.js' : 'douyin-dm-reply.js';
  const candidates = [];
  const repliedThisRun = new Set();
  let actionableCount = 0;
  let scannedCount = 0;

  let collected = collectTargets(kind);
  if (!collected.ok) {
    return {
      ok: false,
      kind,
      error: 'list_failed',
      output: collected.listResult.output.slice(-2000),
    };
  }

  for (
    let index = 0;
    index < collected.rows.length && actionableCount < limit && scannedCount < maxScan;
    index += 1
  ) {
    scannedCount += 1;

    const row = collected.rows[index];
    if (!row) break;
    const sourceText = kind === 'comment' ? row.commentText || row.sample : row.sample;
    const dmVisibleText = kind === 'dm'
      ? [row.name, row.latestTime, row.latestText || sourceText].filter(Boolean).join(' ')
      : sourceText;
    const targetText = kind === 'dm' ? dmReplySourceText(row) : sourceText;
    const key = keyFor(kind, index, targetText, row);
    const dmKey = kind === 'dm' ? key : null;
    if (kind === 'comment' && repliedThisRun.has(key)) {
	      candidates.push({
	        kind,
	        index,
	        sourceText,
	        skipped: true,
	        reason: 'replied_this_run',
      });
      continue;
    }
	    if (kind === 'comment' && row.hasAuthorReply) {
	      candidates.push({
	        kind,
	        index,
	        sourceText,
	        skipped: true,
	        reason: 'already_has_author_reply',
	      });
	      continue;
	    }
    if (kind === 'comment' && (row.isOwn || isOwnComment(sourceText) || isOwnComment(row.sample))) {
	      candidates.push({
	        kind,
	        index,
	        sourceText,
        skipped: true,
        reason: 'own_author_comment',
      });
      continue;
    }
    const dmState = kind === 'dm'
      ? (state.dmConversations?.[dmKey] || null)
      : null;
	    if (!opts.force && kind === 'dm' && (
	      dmLatestLooksOwnReply(dmVisibleText)
	      || (dmState?.lastReply && normalizeReplyFingerprint(dmVisibleText).includes(normalizeReplyFingerprint(dmState.lastReply)))
	      || (dmState?.lastSourceText && normalizeReplyFingerprint(dmVisibleText) === normalizeReplyFingerprint(dmState.lastSourceText))
	    )) {
      candidates.push({
        kind,
        index,
        sourceText: dmVisibleText,
        skipped: true,
        reason: 'latest_dm_is_own_reply',
        previous: dmState,
      });
      continue;
    }
    const previousReply = alreadyReplied(state, kind, targetText, row);
	    if (!opts.force && previousReply) {
	      candidates.push({
	        kind,
	        index,
	        sourceText: targetText,
	        skipped: true,
	        reason: 'already_replied',
	        previous: previousReply,
	      });
	      continue;
	    }
	    if (!opts.force && kind === 'dm' && !dmLooksUnread(row) && process.env.DOUYIN_DM_REQUIRE_UNREAD === 'true') {
	      candidates.push({
	        kind,
	        index,
	        sourceText: dmVisibleText,
	        skipped: true,
	        reason: 'dm_unread_boundary',
	        stopBoundary: true,
	      });
	      break;
	    }
    const replyResult = await generateReply(kind, targetText, {
      row,
      workTitle: collected.listed?.prepare?.latest?.workTitle || '',
      listed: collected.listed,
    }, opts);
    if (replyResult.source !== 'llm' && replyGenerationRequired(opts) && !rulesFallbackAllowed(opts)) {
      candidates.push({
        kind,
        index,
        sourceText: targetText,
        skipped: true,
        reason: 'llm_reply_generation_failed',
        replySource: replyResult.source,
        llmFallback: replyResult.llmFallback,
        llmAttempts: replyResult.llmAttempts,
      });
      actionableCount += 1;
      continue;
    }
    const reply = replyResult.text;
    const item = { kind, index, sourceText: targetText, reply, replySource: replyResult.source, replyModel: replyResult.model, llmFallback: replyResult.llmFallback, llmAttempts: replyResult.llmAttempts };
    if (!opts.execute) {
      candidates.push({ ...item, mode: 'dry-run', wouldExecute: false });
      actionableCount += 1;
      continue;
    }
    const sendArgs = kind === 'comment'
	      ? [
	        join(__dirname, script),
	        'reply',
	        '--text',
	        reply,
	        '--index',
	        String(index),
	        '--unreplied',
	        '--author-reply-check',
	        '--execute',
	        ...(process.env.DOUYIN_COMMENT_SCAN_ALL_WORKS !== 'false' ? ['--all-works'] : []),
	        ...(process.env.DOUYIN_COMMENT_REPLY_LATEST === 'true' ? ['--latest'] : []),
	      ]
      : [join(__dirname, script), 'reply', '--text', reply, '--index', String(index), '--execute'];
    const sendResult = runNode(sendArgs);
    const summarized = summarizeResult(item, sendResult);
    candidates.push(summarized);
    actionableCount += 1;
	    if (summarized.sent && summarized.verified) {
	      repliedThisRun.add(key);
      if (kind === 'comment') {
        state.replied[key] = {
          at: new Date().toISOString(),
          reply,
          sourceText,
          row: withCommentReplyMeta(row),
          verified: summarized.verified,
          sendAction: summarized.sendAction,
          targetVerification: summarized.sendPayload?.verification || null,
        };
      } else {
        state.replied[key] = { at: new Date().toISOString(), reply, sourceText: targetText };
      }
	      if (kind === 'dm') {
	        state.dmConversations[dmKey] = {
	          at: new Date().toISOString(),
	          lastReply: reply,
	          lastSourceText: dmVisibleText,
	        };
	      }
	      if (kind === 'comment') {
	        collected = collectTargets(kind);
	        if (!collected.ok) {
	          candidates.push({
	            kind,
	            skipped: true,
	            reason: 'relist_failed_after_reply',
	            output: collected.listResult.output.slice(-1200),
	          });
	          break;
	        }
	        index = -1;
	      }
	    }
  }
  return {
    ok: candidates.every((item) => item.skipped || item.mode === 'dry-run' || (item.sent && item.verified)),
    kind,
    mode: opts.execute ? 'execute' : 'dry-run',
    scannedCount,
    actionableCount,
    count: candidates.length,
    sentCount: candidates.filter((item) => item.sent && item.verified).length,
    skippedCount: candidates.filter((item) => item.skipped).length,
    items: candidates,
  };
}

async function main() {
  const [kind = '', ...rest] = process.argv.slice(2);
  const opts = parseArgs(rest);
  if (kind === 'preview') {
    const previewKind = opts.kind || 'comment';
    const text = opts.text || opts._?.join(' ') || '';
    if (!text || !['comment', 'dm'].includes(previewKind)) {
      usage();
      process.exitCode = 2;
      return;
    }
    const reply = await generateReply(previewKind, text, { row: { authorName: opts.author || '' }, workTitle: opts.workTitle || '' }, opts);
    console.log(JSON.stringify({ ok: true, mode: 'preview', kind: previewKind, text, reply }, null, 2));
    return;
  }
  if (!['comment', 'dm', 'both'].includes(kind) || opts.help) {
    usage();
    process.exit(kind ? 0 : 2);
  }
  const state = loadState();
  const kinds = kind === 'both' ? ['comment', 'dm'] : [kind];
  const results = [];
  for (const item of kinds) {
    if (shouldDeferToPublish(`auto-reply:${item}`)) {
      results.push({
        ok: true,
        kind: item,
        mode: opts.execute ? 'execute' : 'dry-run',
        deferred: true,
        reason: 'deferred_to_publish',
        scannedCount: 0,
        actionableCount: 0,
        count: 0,
        sentCount: 0,
        skippedCount: 1,
        items: [{ kind: item, skipped: true, reason: 'deferred_to_publish' }],
      });
      break;
    }
    results.push(await autoReplyKind(item, opts, state));
  }
  saveState(state);
  const ok = results.every((item) => item.ok);
  console.log(JSON.stringify({
    ok,
    mode: opts.execute ? 'execute' : 'dry-run',
    ruleSet: resolveLlmConfig(opts).enabled ? 'ai-assisted-v1' : 'deterministic-v1',
    summary: {
      commentSent: sentCount(results.find((item) => item.kind === 'comment') || {}),
      dmSent: sentCount(results.find((item) => item.kind === 'dm') || {}),
    },
    results,
  }, null, 2));
  if (!ok) process.exitCode = 1;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((err) => {
    console.log(JSON.stringify({ ok: false, error: err.message, stack: err.stack }, null, 2));
    process.exit(1);
  });
}
