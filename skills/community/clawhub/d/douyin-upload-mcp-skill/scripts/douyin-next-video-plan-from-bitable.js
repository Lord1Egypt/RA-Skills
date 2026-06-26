#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { homedir } from 'node:os';
import { callFeishuOpenApi, sendFeishuText } from './feishu-client.js';

const STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(process.env.HOME || '.', '.openclaw', 'workspace', 'douyin-ops');
const STATE_PATH = process.env.DOUYIN_FEISHU_BITABLE_STATE || join(STATE_DIR, 'feishu-bitable-state.json');
const PERSONA_STATE_PATH = process.env.DOUYIN_PERSONA_STATE_PATH || join(STATE_DIR, 'persona-state.json');

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

function loadState() {
  if (!existsSync(STATE_PATH)) return {};
  return JSON.parse(readFileSync(STATE_PATH, 'utf8'));
}

function readJson(path, fallback = null) {
  try {
    if (!existsSync(path)) return fallback;
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return fallback;
  }
}

function requireOk(body, action) {
  if (body.code !== 0) throw new Error(`${action} failed: ${body.msg || `code ${body.code}`}`);
  return body.data || {};
}

async function listRecords(appToken, tableId, opts = {}) {
  const items = [];
  let pageToken = '';
  for (let i = 0; i < Number(opts.maxPages || 20); i += 1) {
    const url = new URL(`https://open.feishu.cn/open-apis/bitable/v1/apps/${encodeURIComponent(appToken)}/tables/${encodeURIComponent(tableId)}/records`);
    url.searchParams.set('page_size', String(opts.pageSize || 100));
    if (pageToken) url.searchParams.set('page_token', pageToken);
    const body = await callFeishuOpenApi(url.toString(), { method: 'GET' });
    const data = requireOk(body, 'list records');
    items.push(...(data.items || []));
    if (!data.has_more || !data.page_token) break;
    pageToken = data.page_token;
  }
  return items;
}

function field(record, name) {
  const value = record?.fields?.[name];
  if (Array.isArray(value)) {
    return value.map((item) => {
      if (typeof item === 'string') return item;
      return item?.text || item?.name || item?.value || JSON.stringify(item);
    }).join('');
  }
  if (value && typeof value === 'object') return value.text || value.link || JSON.stringify(value);
  return value ?? '';
}

function num(record, name) {
  const value = Number(field(record, name));
  return Number.isFinite(value) ? value : 0;
}

function dateValue(record, name) {
  return String(field(record, name) || '');
}

function latestLogRecord(log) {
  return [...log]
    .sort((a, b) => dateValue(b, '同步时间').localeCompare(dateValue(a, '同步时间')))[0] || null;
}

function latestLogDays(log, fallback) {
  return Number(field(latestLogRecord(log), '近N天')) || fallback;
}

function cleanTitle(title) {
  return String(title || '')
    .replace(/#[^\s#，。,;；!！?？)）(（]+/g, '')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, 40);
}

function safeVisualTitle(title, fallback = '今日重点') {
  const clean = cleanTitle(title).replace(/\s+/g, '');
  const chars = [...clean];
  if (!chars.length) return fallback;
  if (chars.length <= 8) return clean;
  const preferred = [
    /[^，。！？!?、：:\s]{2,8}(?:避坑|方案|技巧|重点|指南|提醒|真相|秘诀|测试|服务)/,
    /(?:宠物保险|宠物险|自动营销|数字人|一键成片|数据复盘)/,
  ];
  for (const pattern of preferred) {
    const match = clean.match(pattern);
    if (match?.[0] && [...match[0]].length <= 8) return match[0];
  }
  return chars.slice(0, 8).join('');
}

function extractTags(text) {
  return [...String(text || '').matchAll(/#[^\s#，。,;；!！?？)）(（]+/g)]
    .map((match) => match[0].trim())
    .filter(Boolean)
    .slice(0, 8);
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function keywordFromText(text, maxLength = 6) {
  const compact = String(text || '')
    .replace(/https?:\/\/\S+/g, '')
    .replace(/[^\u4e00-\u9fa5A-Za-z0-9]/g, '')
    .trim();
  if (!compact) return '';
  const preferred = [
    '高温强光',
    '散光膜',
    '大棚膜',
    '瓜果增甜',
    '育苗',
    '棚膜',
    '种植',
  ].find((item) => compact.includes(item));
  return (preferred || compact).slice(0, maxLength);
}

function personaTags(persona = {}) {
  const fields = persona.fields || {};
  const summary = persona.summary || {};
  return unique([
    keywordFromText(fields.bissiness || summary.value || '', 6),
    keywordFromText(fields.segment || summary.audience || '', 6),
    '避坑指南',
    '专业服务',
  ].filter(Boolean).map((item) => item.startsWith('#') ? item : `#${item}`)).slice(0, 3);
}

function shortenClause(text, maxLength = 18) {
  const clean = String(text || '')
    .replace(/\s+/g, '')
    .replace(/[，。！？!?、:：；;].*$/u, '')
    .trim();
  return [...clean].slice(0, maxLength).join('');
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

function loadPersonaContext(path = PERSONA_STATE_PATH) {
  const state = readJson(path, {});
  const persona = state.confirmed || null;
  if (!persona) return null;
  const fields = persona.fields || {};
  const summary = persona.summary || {};
  return {
    confirmedAt: persona.confirmedAt || '',
    fields,
    summary: {
      personaId: summary.personaId || '',
      coreIdentity: summary.coreIdentity || '',
      audience: summary.audience || fields.segment || '',
      tone: summary.tone || fields.trials || '',
      value: summary.value || fields.advantage || '',
      primaryPlatform: summary.primaryPlatform || '抖音',
      slogan: summary.slogan || '',
    },
    customerPersona: persona.customerPersona || null,
    accountProfile: persona.accountProfile || null,
    contentRules: persona.contentRules || null,
    platformPlan: persona.platformPlan || null,
    strategyExcerpt: textFromSection(persona.strategy).slice(0, 1200),
    marketingExcerpt: textFromSection(persona.marketing).slice(0, 1200),
  };
}

function workSummary(record) {
  const title = String(field(record, '标题') || field(record, '作品ID') || '').slice(0, 100);
  return {
    title,
    coreTitle: cleanTitle(title),
    tags: extractTags(title),
    views: num(record, '播放量'),
    likes: num(record, '点赞量'),
    comments: num(record, '评论量'),
    shares: num(record, '分享量'),
    avgWatchSeconds: num(record, '平均播放秒'),
    fiveSecondCompletionRate: num(record, '5秒完播率%'),
    twoSecondBounceRate: num(record, '2秒跳出率%'),
    likeRate: num(record, '点赞率%'),
    commentRate: num(record, '评论率%'),
    shareRate: num(record, '分享率%'),
  };
}

function median(numbers) {
  const sorted = numbers.filter((item) => Number.isFinite(item)).sort((a, b) => a - b);
  if (!sorted.length) return 0;
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
}

function buildContext({ works, daily, log, days }) {
  const sorted = [...works].sort((a, b) => num(b, '播放量') - num(a, '播放量'));
  const latestDaily = [...daily]
    .sort((a, b) => dateValue(b, '同步时间').localeCompare(dateValue(a, '同步时间')))[0] || null;
  const latestLog = latestLogRecord(log);
  const topWorks = sorted.slice(0, 5).map(workSummary);
  const weakWorks = [...works].sort((a, b) => num(a, '播放量') - num(b, '播放量')).slice(0, 5).map(workSummary);
  const retentionRisks = [...works]
    .sort((a, b) => num(b, '2秒跳出率%') - num(a, '2秒跳出率%'))
    .slice(0, 5)
    .map(workSummary);
  const tagCounts = new Map();
  for (const item of works) {
    for (const tag of extractTags(field(item, '标题'))) {
      tagCounts.set(tag, (tagCounts.get(tag) || 0) + Math.max(1, num(item, '播放量')));
    }
  }
  const candidateTags = [...tagCounts.entries()]
    .sort((a, b) => b[1] - a[1])
    .map(([tag]) => tag)
    .slice(0, 6);
  return {
    days,
    scope: {
      bitableWorks: works.length,
      latestSyncedWorks: Number(field(latestLog, '作品数')) || works.length,
      latestSyncAt: field(latestLog, '同步时间') || '',
    },
    account: latestDaily ? {
      totalFans: field(latestDaily, '总粉丝量'),
      yesterdayPlays: field(latestDaily, '昨日播放量'),
      periodPosts: field(latestDaily, '周期投稿量'),
      avgClickRate: field(latestDaily, '条均点击率'),
      avg5sCompletionRate: field(latestDaily, '条均5s完播率'),
      avg2sBounceRate: field(latestDaily, '条均2s跳出率'),
      avgWatchTime: field(latestDaily, '条均播放时长'),
      medianPlays: field(latestDaily, '播放量中位数') || String(Math.round(median(works.map((item) => num(item, '播放量'))))),
      sourceSuggestion: field(latestDaily, '建议摘要'),
    } : {
      medianPlays: String(Math.round(median(works.map((item) => num(item, '播放量'))))),
    },
    candidateTags,
    topWorks,
    weakWorks,
    retentionRisks,
  };
}

function withPersona(context, persona) {
  if (!persona) return context;
  return {
    ...context,
    persona,
  };
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
      const preferredProvider = process.env.DOUYIN_NEXT_VIDEO_PLAN_PROVIDER
        || process.env.DOUYIN_DATA_REPORT_PROVIDER
        || process.env.OPENCLAW_PROVIDER
        || 'custom';
      const entries = [
        [preferredProvider, providers[preferredProvider]],
        ...Object.entries(providers).filter(([key]) => key !== preferredProvider),
      ].filter(([, provider]) => provider?.apiKey && provider?.baseUrl);
      for (const [providerId, provider] of entries) {
        const models = Array.isArray(provider.models) ? provider.models : [];
        const model = process.env.DOUYIN_NEXT_VIDEO_PLAN_MODEL
          || process.env.DOUYIN_DATA_REPORT_MODEL
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
      // Optional config may be absent or malformed.
    }
  }
  return null;
}

function resolveLlmConfig() {
  const mode = String(process.env.DOUYIN_NEXT_VIDEO_PLAN_LLM || process.env.DOUYIN_DATA_REPORT_LLM || 'auto').toLowerCase();
  if (['off', 'false', '0', 'none'].includes(mode)) return { enabled: false, reason: 'llm_disabled' };
  const openclaw = loadOpenClawLlmConfig();
  const apiKey = process.env.DOUYIN_NEXT_VIDEO_PLAN_API_KEY
    || process.env.DOUYIN_DATA_REPORT_API_KEY
    || openclaw?.apiKey
    || process.env.MINIMAX_API_KEY
    || process.env.OPENAI_API_KEY
    || '';
  const rawBaseUrl = process.env.DOUYIN_NEXT_VIDEO_PLAN_BASE_URL
    || process.env.DOUYIN_DATA_REPORT_BASE_URL
    || openclaw?.rawBaseUrl
    || process.env.MINIMAX_API_BASE_URL
    || process.env.OPENAI_BASE_URL
    || process.env.OPENAI_API_BASE
    || '';
  const model = process.env.DOUYIN_NEXT_VIDEO_PLAN_MODEL
    || process.env.DOUYIN_DATA_REPORT_MODEL
    || openclaw?.model
    || process.env.MINIMAX_MODEL
    || process.env.OPENCLAW_MODEL
    || process.env.OPENAI_MODEL
    || 'MiniMax-M2.7';
  if (!apiKey || !rawBaseUrl) return { enabled: false, reason: !apiKey ? 'missing_api_key' : 'missing_base_url' };
  const baseUrl = String(rawBaseUrl).replace(/\/+$/, '');
  const api = process.env.DOUYIN_NEXT_VIDEO_PLAN_API || process.env.DOUYIN_DATA_REPORT_API || openclaw?.api || 'openai-chat-completions';
  const effectiveApi = /minimaxi\.com\/anthropic/.test(baseUrl) && api !== 'anthropic-messages'
    ? 'openai-chat-completions'
    : api;
  const endpoint = effectiveApi === 'anthropic-messages'
    ? (/\/v1\/messages$/.test(baseUrl) ? baseUrl : `${baseUrl}/v1/messages`)
    : (/\/chat\/completions$/.test(baseUrl) ? baseUrl : `${baseUrl}/chat/completions`);
  return {
    enabled: true,
    api: effectiveApi,
    apiKey,
    endpoint,
    model,
    providerId: openclaw?.providerId,
    timeoutMs: Math.max(3000, Math.min(180000, Number(process.env.DOUYIN_NEXT_VIDEO_PLAN_LLM_TIMEOUT_MS || 120000))),
  };
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

function parseJsonFromText(text) {
  const raw = String(text || '').trim().replace(/^```(?:json)?/i, '').replace(/```$/i, '').trim();
  try {
    return JSON.parse(raw);
  } catch {
    // Continue with brace extraction.
  }
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
        try {
          return JSON.parse(raw.slice(start, i + 1));
        } catch {
          return null;
        }
      }
    }
  }
  return null;
}

function fallbackPlan(context) {
  const top = context.topWorks?.[0] || {};
  const risk = context.retentionRisks?.[0] || context.weakWorks?.[0] || {};
  const persona = context.persona || {};
  const summary = persona.summary || {};
  const fields = persona.fields || {};
  const business = shortenClause(fields.bissiness || summary.value || '核心业务', 16);
  const audience = shortenClause(summary.audience || fields.segment || '目标客户', 14);
  const tone = summary.tone || fields.trials || '专业、直接';
  const subject = top.coreTitle || risk.coreTitle || business || '下一条内容';
  const safeTags = personaTags(persona);
  const title = normalizeTitle(`${audience}选${keywordFromText(business, 6) || business}别只看价格`, 30);
  const visualTitle = safeVisualTitle(title);
  const hook = `很多${audience}选${business}只看价格，其实更要看适不适合棚里的光照问题。`;
  return {
    topic: `结合账号人设“${summary.coreIdentity || business}”，延续高播放作品《${subject}》的结构，讲清${audience}最容易忽略的决策误区。`,
    title,
    videoTitle: visualTitle,
    visualTitle,
    coverText: safeVisualTitle(`${keywordFromText(business, 6) || business}避坑`),
    tags: safeTags,
    hook,
    script: [
      `开头：${hook}`,
      `展开：用${tone}的表达方式，先说${audience}最常见的误区。`,
      `转折：结合${fields.cases || '实际经验'}提醒大家不要只看表面条件。`,
      `收束：给出一个合规、可执行的判断标准，引导有类似情况的人继续咨询。`,
    ],
    shotList: [
      { time: '0-3s', visual: '数字人正面近景，字幕突出冲突词。', narration: hook },
      { time: '3-12s', visual: '切换 2-3 个关键词卡片。', narration: `先讲${audience}常见误区，再给出判断线索。` },
      { time: '12-24s', visual: '数字人强调结论，屏幕保留一句总结。', narration: '把避坑点讲透，并给出下一步互动问题。' },
    ],
    publishFields: {
      title,
      description: `${hook}\n${safeTags.join(' ')}`,
      tags: safeTags,
    },
    digitalHumanInput: {
      modelId: process.env.DIGITAL_HUMAN_MODEL_ID || process.env.VIRTUALMAN_MODEL_ID || '',
      title,
      publishTitle: title,
      videoTitle: visualTitle,
      visualTitle,
      scriptText: [
        hook,
        `先别急着下结论。对${audience}来说，棚膜不是越便宜越稳，也不是功能越多越好。`,
        `把${business}里的关键条件拆开看，很多坑其实能提前避开。`,
        '如果你也有类似情况，可以在评论区告诉我。',
      ].join('\n'),
      coverText: safeVisualTitle(`${keywordFromText(business, 6) || business}避坑`),
      tags: safeTags,
      suggestedDurationSeconds: 25,
    },
  };
}

function normalizeTitle(value, maxLength = 30) {
  const chars = [...cleanTitle(value)
    .replace(/\s+/g, '')
    .replace(/[，,、；;：:|｜\\/-]+$/g, '')
    .trim()];
  return chars.slice(0, maxLength).join('');
}

function tagLooksPersonaRelated(tag, context) {
  const text = String(tag || '').replace(/^#/, '');
  if (!text) return false;
  const persona = context.persona || {};
  const fields = persona.fields || {};
  const haystack = [
    fields.bissiness,
    fields.segment,
    fields.advantage,
    fields.cases,
    persona.summary?.audience,
    persona.summary?.value,
    '避坑指南',
    '专业服务',
  ].filter(Boolean).join('\n');
  return haystack.includes(text) || text.includes('避坑') || text.includes('专业');
}

function normalizePlan(plan, context) {
  const fallback = fallbackPlan(context);
  const tagsRaw = unique(
    (Array.isArray(plan?.tags) ? plan.tags : String(plan?.tags || '').split(/[,\s，、]+/))
      .map((tag) => String(tag || '').trim())
      .filter(Boolean)
      .map((tag) => tag.startsWith('#') ? tag : `#${tag}`)
  ).filter((tag) => tagLooksPersonaRelated(tag, context)).slice(0, 5);
  const tags = tagsRaw.length ? tagsRaw : fallback.tags;
  const title = normalizeTitle(plan?.title || fallback.title, 30);
  const visualTitle = safeVisualTitle(plan?.videoTitle || plan?.visualTitle || plan?.digitalHumanInput?.videoTitle || plan?.digitalHumanInput?.visualTitle || title);
  const coverText = String(plan?.coverText || plan?.cover || fallback.coverText).trim().slice(0, 16);
  const splitScriptText = (value) => {
    const raw = String(value || '').trim();
    if (!raw) return [];
    const lines = raw.split(/\n+/).map((line) => line.trim()).filter(Boolean);
    if (lines.length > 1) return lines;
    return raw
      .split(/(?<=[。！？!?])\s*/)
      .map((line) => line.trim())
      .filter(Boolean);
  };
  const script = Array.isArray(plan?.script)
    ? plan.script.map((line) => String(line || '').trim()).filter(Boolean).slice(0, 8)
    : splitScriptText(plan?.script).slice(0, 8);
  const shotList = Array.isArray(plan?.shotList) && plan.shotList.length
    ? plan.shotList.slice(0, 6).map((item) => ({
      time: String(item?.time || '').slice(0, 20),
      visual: String(item?.visual || '').slice(0, 100),
      narration: String(item?.narration || '').slice(0, 160),
    }))
    : fallback.shotList;
  const next = {
    topic: String(plan?.topic || fallback.topic).trim().slice(0, 120),
    title,
    videoTitle: visualTitle,
    visualTitle,
    coverText,
    tags: tags.length ? tags : fallback.tags,
    hook: String(plan?.hook || fallback.hook).trim().slice(0, 180),
    script: script.length ? script : fallback.script,
    shotList,
  };
  next.publishFields = {
    title,
    description: String(plan?.publishFields?.description || `${next.hook}\n${next.tags.join(' ')}`).trim().slice(0, 500),
    tags: next.tags,
  };
  next.digitalHumanInput = {
    modelId: process.env.DIGITAL_HUMAN_MODEL_ID || process.env.VIRTUALMAN_MODEL_ID || String(plan?.digitalHumanInput?.modelId || ''),
    title,
    publishTitle: title,
    videoTitle: visualTitle,
    visualTitle,
    scriptText: String(plan?.digitalHumanInput?.scriptText || next.script.join('\n')).trim().slice(0, 2000),
    coverText,
    tags: next.tags,
    suggestedDurationSeconds: Number(plan?.digitalHumanInput?.suggestedDurationSeconds || 25),
  };
  return next;
}

function planText(plan, meta = {}) {
  const scriptLines = plan.script.map((line, index) => `${index + 1}. ${line}`).join('\n');
  const shotLines = plan.shotList.map((item) => `${item.time || '-'}：${item.visual || ''}`).join('\n');
  const digitalHumanInput = JSON.stringify(plan.digitalHumanInput || {}, null, 2);
  return [
    '下一条视频方案：',
    `标题：${plan.title}`,
    `封面文案：${plan.coverText}`,
    `tags：${plan.tags.join(' ')}`,
    `选题：${plan.topic}`,
    '口播脚本：',
    scriptLines,
    '画面建议：',
    shotLines,
    '数字人成片参数 digitalHumanInput：',
    digitalHumanInput,
    meta.model ? `生成模型：${meta.model}` : '',
    '成片完成后发送“视频地址/封面图片/标题/tags”即可自动发布。',
  ].filter(Boolean).join('\n');
}

async function generateWithLlm(context) {
  const cfg = resolveLlmConfig();
  if (!cfg.enabled) return { ok: false, source: 'rules', reason: cfg.reason };
  const system = [
    '你是抖音短视频增长编导，只基于给定账号数据生成下一条可拍摄的视频方案。',
    '如果 context.persona 存在，必须优先遵循已确认人设：核心身份、目标客户、沟通调性、核心价值、禁忌偏好和账号内容规范。',
    '生成的标题、选题、口播、画面建议必须体现该人设，不要脱离主营业务和目标客户去追泛流量。',
    '不要编造数据，不要引用外部事实，不要承诺收益、投保结果、医疗或法律效果。',
    '输出必须是 JSON，不要 Markdown，不要解释。',
    'JSON 字段：topic,title,videoTitle,coverText,tags,hook,script,shotList,publishFields,digitalHumanInput。',
    'title 是抖音发布标题，可到 30 个中文字符；videoTitle 是视频画面主标题，必须 4-8 个中文字符，不能越界；coverText 不超过 12 个中文字符；tags 2-5 个且带 #。',
    'script 是 4-7 句中文口播，适合数字人口播，前 2 秒必须有冲突/反转/利益点。',
    'shotList 每项含 time, visual, narration；digitalHumanInput 含 title, publishTitle, videoTitle, scriptText, coverText, tags, suggestedDurationSeconds；如果配置了 modelId 必须放入 digitalHumanInput.modelId。',
  ].join('\n');
  const user = `请根据这些抖音数据生成下一条视频完整方案：\n${JSON.stringify(context, null, 2)}`;
  const body = cfg.api === 'anthropic-messages'
    ? {
      model: cfg.model,
      system,
      messages: [{ role: 'user', content: user }],
      temperature: Number(process.env.DOUYIN_NEXT_VIDEO_PLAN_TEMPERATURE || 0.55),
      max_tokens: Number(process.env.DOUYIN_NEXT_VIDEO_PLAN_MAX_TOKENS || 1800),
    }
    : {
      model: cfg.model,
      messages: [
        { role: 'system', content: system },
        { role: 'user', content: user },
      ],
      temperature: Number(process.env.DOUYIN_NEXT_VIDEO_PLAN_TEMPERATURE || 0.55),
      max_tokens: Number(process.env.DOUYIN_NEXT_VIDEO_PLAN_MAX_TOKENS || 1800),
    };
  try {
    const res = await fetch(cfg.endpoint, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${cfg.apiKey}`,
        'x-api-key': cfg.apiKey,
        'anthropic-version': process.env.DOUYIN_NEXT_VIDEO_PLAN_ANTHROPIC_VERSION || '2023-06-01',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(cfg.timeoutMs),
    });
    const payload = await res.json().catch(() => ({}));
    const text = extractLlmContent(payload);
    const parsed = parseJsonFromText(text);
    if (!res.ok || !parsed) {
      return { ok: false, source: 'llm', model: cfg.model, status: res.status, reason: 'llm_failed_or_invalid_json' };
    }
    return { ok: true, source: 'llm', model: cfg.model, plan: parsed };
  } catch (err) {
    return { ok: false, source: 'llm', model: cfg.model, reason: 'llm_request_failed', error: err.message };
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  let works;
  let daily;
  let log;
  if (args.fixtureJson) {
    const fixture = readJson(args.fixtureJson, {});
    works = Array.isArray(fixture.works) ? fixture.works : [];
    daily = Array.isArray(fixture.daily) ? fixture.daily : [];
    log = Array.isArray(fixture.log) ? fixture.log : [];
  } else {
    const state = loadState();
    const appToken = args.appToken || process.env.FEISHU_BITABLE_APP_TOKEN || state.appToken;
    const worksTableId = args.worksTableId || process.env.FEISHU_BITABLE_WORKS_TABLE_ID || state.worksTableId;
    const dailyTableId = args.dailyTableId || process.env.FEISHU_BITABLE_DAILY_TABLE_ID || state.dailyTableId;
    const logTableId = args.logTableId || process.env.FEISHU_BITABLE_LOG_TABLE_ID || state.logTableId;
    if (!appToken || !worksTableId || !dailyTableId || !logTableId) {
      throw new Error('Feishu bitable state is missing. Run sync-douyin-data-to-feishu-bitable.js first.');
    }
    [works, daily, log] = await Promise.all([
      listRecords(appToken, worksTableId),
      listRecords(appToken, dailyTableId),
      listRecords(appToken, logTableId),
    ]);
  }
  const days = Number(args.days || latestLogDays(log, 90));
  const persona = args.personaState === 'off' ? null : loadPersonaContext(args.personaState || PERSONA_STATE_PATH);
  const context = withPersona(buildContext({ works, daily, log, days }), persona);
  const generated = await generateWithLlm(context);
  const plan = normalizePlan(generated.ok ? generated.plan : fallbackPlan(context), context);
  const text = planText(plan, { model: generated.ok ? generated.model : 'rules-fallback' });
  const result = {
    ok: true,
    source: 'feishu_bitable',
    days,
    counts: { works: works.length, daily: daily.length, log: log.length },
    personaUsed: Boolean(persona),
    personaSummary: persona?.summary || null,
    model: generated.ok ? generated.model : null,
    generator: generated,
    context,
    plan,
    planText: text,
  };
  if (args.output) {
    mkdirSync(join(String(args.output), '..'), { recursive: true });
    writeFileSync(args.output, `${JSON.stringify(result, null, 2)}\n`);
    result.output = args.output;
  }
  if (args.notify) result.notify = await sendFeishuText(text);
  console.log(JSON.stringify(result, null, 2));
}

main().catch(async (err) => {
  const payload = { ok: false, error: err.message, stack: err.stack };
  if (process.argv.includes('--notify')) {
    payload.notify = await sendFeishuText(`下一条视频方案生成失败：${err.message.slice(0, 120)}`);
  }
  console.log(JSON.stringify(payload, null, 2));
  process.exit(1);
});
