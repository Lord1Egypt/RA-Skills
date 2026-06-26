#!/usr/bin/env node
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { homedir } from 'node:os';
import { callFeishuOpenApi, sendFeishuText } from './feishu-client.js';

const STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(process.env.HOME || '.', '.openclaw', 'workspace', 'douyin-ops');
const STATE_PATH = process.env.DOUYIN_FEISHU_BITABLE_STATE || join(STATE_DIR, 'feishu-bitable-state.json');

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith('--')) continue;
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

function latestLogDays(log, fallback) {
  const latest = [...log]
    .sort((a, b) => dateValue(b, '同步时间').localeCompare(dateValue(a, '同步时间')))[0] || null;
  return Number(field(latest, '近N天')) || fallback;
}

function latestLogRecord(log) {
  return [...log]
    .sort((a, b) => dateValue(b, '同步时间').localeCompare(dateValue(a, '同步时间')))[0] || null;
}

function buildReport({ works, daily, log, days }) {
  const latestDaily = [...daily]
    .sort((a, b) => dateValue(b, '同步时间').localeCompare(dateValue(a, '同步时间')))[0] || null;
  const latestLog = [...log]
    .sort((a, b) => dateValue(b, '同步时间').localeCompare(dateValue(a, '同步时间')))[0] || null;
  const sortedWorks = [...works]
    .sort((a, b) => num(b, '播放量') - num(a, '播放量'));
  const top = sortedWorks[0] || null;
  const low = sortedWorks.at(-1) || null;
  const best5s = [...works].sort((a, b) => num(b, '5秒完播率%') - num(a, '5秒完播率%'))[0] || null;
  const highBounce = [...works].sort((a, b) => num(b, '2秒跳出率%') - num(a, '2秒跳出率%'))[0] || null;

  const totalViews = works.reduce((sum, item) => sum + num(item, '播放量'), 0);
  const totalLikes = works.reduce((sum, item) => sum + num(item, '点赞量'), 0);
  const totalComments = works.reduce((sum, item) => sum + num(item, '评论量'), 0);
  const totalShares = works.reduce((sum, item) => sum + num(item, '分享量'), 0);

  const lines = [
    `数据报告：已同步近 ${days} 天作品明细，作品 ${works.length} 条。`,
    `总播放 ${totalViews}，点赞 ${totalLikes}，评论 ${totalComments}，分享 ${totalShares}。`,
  ];
  if (latestDaily) {
    lines.push(`账号概况：抖音后台当前展示周期；昨日播放 ${field(latestDaily, '昨日播放量') || '-'}，点赞 ${field(latestDaily, '作品点赞') || '-'}，评论 ${field(latestDaily, '作品评论') || '-'}，总粉丝 ${field(latestDaily, '总粉丝量') || '-'}。`);
  }
  if (top) lines.push(`播放最高：${field(top, '标题') || field(top, '作品ID')}（${num(top, '播放量')}）。`);
  if (low && low.record_id !== top?.record_id) lines.push(`播放最低：${field(low, '标题') || field(low, '作品ID')}（${num(low, '播放量')}）。`);
  if (best5s) lines.push(`5秒完播最好：${field(best5s, '标题') || field(best5s, '作品ID')}（${num(best5s, '5秒完播率%').toFixed(2)}%）。`);
  if (highBounce) lines.push(`2秒跳出最高：${field(highBounce, '标题') || field(highBounce, '作品ID')}（${num(highBounce, '2秒跳出率%').toFixed(2)}%）。`);
  const suggestion = field(latestDaily, '建议摘要');
  if (suggestion) lines.push(`建议：${String(suggestion).split(/\n/)[0].slice(0, 90)}`);
  const latestSyncedWorks = Number(field(latestLog, '作品数'));
  if (Number.isFinite(latestSyncedWorks) && latestSyncedWorks > 0 && latestSyncedWorks !== works.length) {
    lines.push(`口径说明：多维表当前累计作品 ${works.length} 条，最近一次同步抓到 ${latestSyncedWorks} 条。`);
  }
  if (latestLog) lines.push(`最后同步：${field(latestLog, '同步时间') || '-'}。`);
  return lines.join('\n');
}

function formatReportMessage(reportText) {
  const text = String(reportText || '数据报告已生成。').trim();
  if (text.startsWith('老板，昨日数据报告如下，请您查收～')) return text;
  return `老板，昨日数据报告如下，请您查收～\n${text}`;
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
      const preferredProvider = process.env.DOUYIN_DATA_REPORT_PROVIDER || process.env.OPENCLAW_PROVIDER || 'custom';
      const entries = [
        [preferredProvider, providers[preferredProvider]],
        ...Object.entries(providers).filter(([key]) => key !== preferredProvider),
      ].filter(([, provider]) => provider?.apiKey && provider?.baseUrl);
      for (const [providerId, provider] of entries) {
        const models = Array.isArray(provider.models) ? provider.models : [];
        const model = process.env.DOUYIN_DATA_REPORT_MODEL
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
      // Optional config may be absent or malformed; fall back to env below.
    }
  }
  return null;
}

function resolveLlmConfig() {
  const mode = String(process.env.DOUYIN_DATA_REPORT_LLM || 'auto').toLowerCase();
  if (['off', 'false', '0', 'none'].includes(mode)) return { enabled: false, reason: 'llm_disabled' };
  const openclaw = loadOpenClawLlmConfig();
  const apiKey = process.env.DOUYIN_DATA_REPORT_API_KEY
    || openclaw?.apiKey
    || process.env.MINIMAX_API_KEY
    || process.env.OPENAI_API_KEY
    || '';
  const rawBaseUrl = process.env.DOUYIN_DATA_REPORT_BASE_URL
    || openclaw?.rawBaseUrl
    || process.env.MINIMAX_API_BASE_URL
    || process.env.OPENAI_BASE_URL
    || process.env.OPENAI_API_BASE
    || '';
  const model = process.env.DOUYIN_DATA_REPORT_MODEL
    || openclaw?.model
    || process.env.MINIMAX_MODEL
    || process.env.OPENCLAW_MODEL
    || process.env.OPENAI_MODEL
    || 'MiniMax-M2.7';
  if (!apiKey || !rawBaseUrl) return { enabled: false, reason: !apiKey ? 'missing_api_key' : 'missing_base_url' };
  const baseUrl = String(rawBaseUrl).replace(/\/+$/, '');
  const api = process.env.DOUYIN_DATA_REPORT_API || openclaw?.api || 'openai-chat-completions';
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
    timeoutMs: Math.max(3000, Math.min(45000, Number(process.env.DOUYIN_DATA_REPORT_LLM_TIMEOUT_MS || 30000))),
  };
}

function workSummary(record) {
  return {
    title: String(field(record, '标题') || field(record, '作品ID') || '').slice(0, 80),
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

function buildEnhancedContext({ works, daily, log, days, basicReport }) {
  const latestDaily = [...daily]
    .sort((a, b) => dateValue(b, '同步时间').localeCompare(dateValue(a, '同步时间')))[0] || null;
  const latestLog = latestLogRecord(log);
  const sorted = [...works].sort((a, b) => num(b, '播放量') - num(a, '播放量'));
  return {
    days,
    basicReport,
    scope: {
      bitableWorks: works.length,
      latestSyncedWorks: Number(field(latestLog, '作品数')) || works.length,
      latestSyncAt: field(latestLog, '同步时间') || '',
      reportingInstruction: Number(field(latestLog, '作品数')) && Number(field(latestLog, '作品数')) !== works.length
        ? '必须明确区分：基础报告和作品排行使用多维表累计作品数；最近一次同步作品数只用于说明最新采集范围。禁止写“本次报告基于最近一次同步作品”。'
        : '',
    },
    account: latestDaily ? {
      yesterdayPlays: field(latestDaily, '昨日播放量'),
      profileVisits: field(latestDaily, '主页访问'),
      likes: field(latestDaily, '作品点赞'),
      shares: field(latestDaily, '作品分享'),
      comments: field(latestDaily, '作品评论'),
      netFans: field(latestDaily, '净增粉丝'),
      totalFans: field(latestDaily, '总粉丝量'),
      periodPosts: field(latestDaily, '周期投稿量'),
      avgClickRate: field(latestDaily, '条均点击率'),
      avg5sCompletionRate: field(latestDaily, '条均5s完播率'),
      avg2sBounceRate: field(latestDaily, '条均2s跳出率'),
      avgWatchTime: field(latestDaily, '条均播放时长'),
      medianPlays: field(latestDaily, '播放量中位数'),
      sourceSuggestion: field(latestDaily, '建议摘要'),
    } : {},
    topWorks: sorted.slice(0, 5).map(workSummary),
    weakWorks: [...works].sort((a, b) => num(a, '播放量') - num(b, '播放量')).slice(0, 3).map(workSummary),
    retentionRisks: [...works]
      .sort((a, b) => num(b, '2秒跳出率%') - num(a, '2秒跳出率%'))
      .slice(0, 3)
      .map(workSummary),
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

function sanitizeReport(text) {
  return String(text || '')
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/^\s*(增强版数据分析|数据分析报告|报告)[:：]\s*/i, '')
    .replace(/\*\*/g, '')
    .replace(/^#{1,6}\s*/gm, '')
    .replace(/^[-–—]{3,}$/gm, '')
    .replace(/^[⚠️!！\s]*/gm, '')
    .trim()
    .split(/\n+/)
    .map((line) => line.trim().replace(/^[-*]\s+/, ''))
    .filter((line) => line && !/^(关键结论|原因判断|下一步动作|下一条视频实验假设|数据口径说明)[:：]?$/.test(line))
    .slice(0, 8)
    .join('\n')
    .slice(0, 1800);
}

function reportLooksInconsistent(text, context) {
  const latest = Number(context?.scope?.latestSyncedWorks || 0);
  const bitable = Number(context?.scope?.bitableWorks || 0);
  if (!latest || !bitable || latest === bitable) return false;
  const compact = String(text || '').replace(/\s+/g, '');
  return new RegExp(`报告[^，。；\\n]{0,20}基于[^，。；\\n]{0,12}${latest}条`).test(compact)
    || new RegExp(`基于[^，。；\\n]{0,12}${latest}条有效作品`).test(compact);
}

function deterministicEnhancedReport(context) {
  const top = context.topWorks?.[0];
  const weak = context.weakWorks?.[0];
  const risk = context.retentionRisks?.[0];
  const median = context.account?.medianPlays || '-';
  const avg5s = context.account?.avg5sCompletionRate || '-';
  const avgBounce = context.account?.avg2sBounceRate || '-';
  const lines = [
    `数据口径：多维表累计作品 ${context.scope?.bitableWorks || '-'} 条；最近一次同步抓到 ${context.scope?.latestSyncedWorks || '-'} 条，用于判断最新采集范围。`,
    `关键结论：播放主要集中在《${top?.title || '-'}》，播放 ${top?.views ?? '-'}；非头部作品仍需要继续验证稳定流量。`,
    `原因判断：当前条均 5 秒完播 ${avg5s}、2 秒跳出 ${avgBounce}、播放中位数 ${median}，优先排查前 2 秒钩子和封面标题点击。`,
    `风险作品：${risk?.title || weak?.title || '-'} 的 2 秒跳出率 ${risk?.twoSecondBounceRate ?? '-'}%，需要更快给出冲突或结果。`,
    '下一步动作：标题减少泛标签堆叠，封面突出单一卖点，前 3 秒先给结果或反转点。',
    '下一条视频实验假设：延续高播放作品的“反转/悬念”结构，目标播放超过非头部中位数，5 秒完播率不低于 40%。',
  ];
  return lines.join('\n').slice(0, 1800);
}

async function generateEnhancedReport(context) {
  const cfg = resolveLlmConfig();
  if (!cfg.enabled) return { ok: false, source: 'rules', reason: cfg.reason };
  const system = [
    '你是抖音创作者数据分析助手，只基于给定数据做中文短报告。',
    '不要编造数据，不要引入外部事实，不要泛泛而谈。',
    '输出 5-7 行，每行一句：口径、关键结论、原因判断、下一步动作、下一条视频实验假设。',
    '如果多维表累计作品数和最近一次同步作品数不同，必须把两者分别说明，不能混成一个口径。',
    '保留关键数字；如果样本少，明确低置信度。',
  ].join('\n');
  const user = `请生成增强版数据分析：\n${JSON.stringify(context, null, 2)}`;
  const body = cfg.api === 'anthropic-messages'
    ? {
      model: cfg.model,
      system,
      messages: [{ role: 'user', content: user }],
      temperature: Number(process.env.DOUYIN_DATA_REPORT_TEMPERATURE || 0.4),
      max_tokens: Number(process.env.DOUYIN_DATA_REPORT_MAX_TOKENS || 1200),
    }
    : {
      model: cfg.model,
      messages: [
        { role: 'system', content: system },
        { role: 'user', content: user },
      ],
      temperature: Number(process.env.DOUYIN_DATA_REPORT_TEMPERATURE || 0.4),
      max_tokens: Number(process.env.DOUYIN_DATA_REPORT_MAX_TOKENS || 1200),
    };
  try {
    const res = await fetch(cfg.endpoint, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${cfg.apiKey}`,
        'x-api-key': cfg.apiKey,
        'anthropic-version': process.env.DOUYIN_DATA_REPORT_ANTHROPIC_VERSION || '2023-06-01',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(cfg.timeoutMs),
    });
    const payload = await res.json().catch(() => ({}));
    const text = sanitizeReport(extractLlmContent(payload));
    if (!res.ok || !text) {
      return { ok: false, source: 'llm', model: cfg.model, status: res.status, reason: 'llm_failed' };
    }
    if (reportLooksInconsistent(text, context)) {
      return {
        ok: true,
        source: 'rules',
        model: cfg.model,
        reason: 'llm_report_inconsistent_scope',
        text: deterministicEnhancedReport(context),
      };
    }
    return { ok: true, source: 'llm', model: cfg.model, text };
  } catch (err) {
    return { ok: false, source: 'llm', model: cfg.model, reason: 'llm_request_failed', error: err.message };
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const state = loadState();
  const appToken = args.appToken || process.env.FEISHU_BITABLE_APP_TOKEN || state.appToken;
  const worksTableId = args.worksTableId || process.env.FEISHU_BITABLE_WORKS_TABLE_ID || state.worksTableId;
  const dailyTableId = args.dailyTableId || process.env.FEISHU_BITABLE_DAILY_TABLE_ID || state.dailyTableId;
  const logTableId = args.logTableId || process.env.FEISHU_BITABLE_LOG_TABLE_ID || state.logTableId;
  if (!appToken || !worksTableId || !dailyTableId || !logTableId) {
    throw new Error('Feishu bitable state is missing. Run sync-douyin-data-to-feishu-bitable.js first.');
  }
  const [works, daily, log] = await Promise.all([
    listRecords(appToken, worksTableId),
    listRecords(appToken, dailyTableId),
    listRecords(appToken, logTableId),
  ]);
  const days = Number(args.days || latestLogDays(log, 90));
  const basicReportText = buildReport({ works, daily, log, days });
  let reportText = basicReportText;
  let enhanced = null;
  const enhancedEnabled = !['false', '0', 'off', 'no'].includes(String(args.enhanced ?? process.env.DOUYIN_DATA_REPORT_ENHANCED ?? 'true').toLowerCase());
  if (enhancedEnabled) {
    enhanced = await generateEnhancedReport(buildEnhancedContext({
      works,
      daily,
      log,
      days,
      basicReport: basicReportText,
    }));
    if (enhanced.ok) {
      reportText = `${basicReportText}\n\n增强分析（${enhanced.model}）：\n${enhanced.text}`;
    }
  }
  const result = {
    ok: true,
    source: 'feishu_bitable',
    appToken,
    tables: { worksTableId, dailyTableId, logTableId },
    counts: { works: works.length, daily: daily.length, log: log.length },
    basicReportText,
    enhanced,
    reportText,
  };
  if (args.notify) result.notify = await sendFeishuText(formatReportMessage(reportText));
  console.log(JSON.stringify(result, null, 2));
}

main().catch(async (err) => {
  const payload = { ok: false, error: err.message, stack: err.stack };
  if (process.argv.includes('--notify')) {
    payload.notify = await sendFeishuText(`数据报告生成失败：${err.message.slice(0, 180)}`);
  }
  console.log(JSON.stringify(payload, null, 2));
  process.exit(1);
});
