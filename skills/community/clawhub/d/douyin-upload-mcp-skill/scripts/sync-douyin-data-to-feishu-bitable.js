#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { buildFeishuScopeAuthUrl, callFeishuOpenApi, sendFeishuText } from './feishu-client.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(process.env.HOME || '.', '.openclaw', 'workspace', 'douyin-ops');
const STATE_PATH = process.env.DOUYIN_FEISHU_BITABLE_STATE || join(STATE_DIR, 'feishu-bitable-state.json');
const REPORT_DIR = join(STATE_DIR, 'reports');

const WORK_TABLE_NAME = '抖音作品明细';
const DAILY_TABLE_NAME = '抖音账号日报';
const LOG_TABLE_NAME = '抖音数据同步日志';

const FIELD_TYPES = {
  text: 1,
  number: 2,
  singleSelect: 3,
  date: 5,
};

const WORK_FIELDS = [
  ['作品ID', 'text'],
  ['标题', 'text'],
  ['发布时间', 'text'],
  ['同步时间', 'text'],
  ['统计周期', 'text'],
  ['审核状态', 'text'],
  ['可见性', 'text'],
  ['视频时长秒', 'number'],
  ['封面链接', 'text'],
  ['播放量', 'number'],
  ['点赞量', 'number'],
  ['评论量', 'number'],
  ['分享量', 'number'],
  ['收藏量', 'number'],
  ['主页访问量', 'number'],
  ['粉丝增量', 'number'],
  ['取关量', 'number'],
  ['弹幕量', 'number'],
  ['下载量', 'number'],
  ['不喜欢量', 'number'],
  ['封面展现', 'number'],
  ['平均播放秒', 'number'],
  ['平均播放占比%', 'number'],
  ['完播率%', 'number'],
  ['5秒完播率%', 'number'],
  ['2秒跳出率%', 'number'],
  ['粉丝观看占比%', 'number'],
  ['点赞率%', 'number'],
  ['评论率%', 'number'],
  ['分享率%', 'number'],
  ['收藏率%', 'number'],
  ['涨粉率%', 'number'],
  ['取关率%', 'number'],
  ['不喜欢率%', 'number'],
];

const DAILY_FIELDS = [
  ['日期', 'text'],
  ['同步时间', 'text'],
  ['统计周期', 'text'],
  ['作品数', 'number'],
  ['昨日播放量', 'text'],
  ['主页访问', 'text'],
  ['作品点赞', 'text'],
  ['作品分享', 'text'],
  ['作品评论', 'text'],
  ['净增粉丝', 'text'],
  ['总粉丝量', 'text'],
  ['周期投稿量', 'text'],
  ['条均点击率', 'text'],
  ['条均5s完播率', 'text'],
  ['条均2s跳出率', 'text'],
  ['条均播放时长', 'text'],
  ['播放量中位数', 'text'],
  ['建议摘要', 'text'],
];

const LOG_FIELDS = [
  ['同步时间', 'text'],
  ['状态', 'text'],
  ['近N天', 'number'],
  ['作品数', 'number'],
  ['新增', 'number'],
  ['更新', 'number'],
  ['信息', 'text'],
];

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
  try {
    return JSON.parse(readFileSync(STATE_PATH, 'utf8'));
  } catch {
    return {};
  }
}

function saveState(state) {
  mkdirSync(dirname(STATE_PATH), { recursive: true });
  writeFileSync(STATE_PATH, `${JSON.stringify({ ...state, updatedAt: new Date().toISOString() }, null, 2)}\n`);
}

function lastJson(text) {
  const trimmed = String(text || '').trim();
  const candidates = [];
  let depth = 0;
  let start = -1;
  let inString = false;
  let escaped = false;
  for (let i = 0; i < trimmed.length; i += 1) {
    const ch = trimmed[i];
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
      if (depth === 0 && start !== -1) {
        candidates.push(trimmed.slice(start, i + 1));
        start = -1;
      }
    }
  }
  for (let i = candidates.length - 1; i >= 0; i -= 1) {
    try {
      return JSON.parse(candidates[i]);
    } catch {
      continue;
    }
  }
  return null;
}

function compact(value) {
  if (value === null || value === undefined) return '';
  if (typeof value === 'object') return JSON.stringify(value);
  return String(value);
}

function numeric(value) {
  const num = Number(value);
  return Number.isFinite(num) ? num : undefined;
}

function urlValue(url) {
  return url ? String(url) : '';
}

function firstCoverUrl(item) {
  return item.cover?.urls?.[0] || item.cover?.url || '';
}

function buildWorkFields(item, analysis) {
  const m = item.metrics || {};
  return {
    作品ID: item.id,
    标题: item.title || '',
    发布时间: item.publishTime || '',
    同步时间: analysis.collectedAt,
    统计周期: `${analysis.days || 90}天`,
    审核状态: compact(item.reviewStatus),
    可见性: compact(item.visibility),
    视频时长秒: numeric(item.video?.durationSeconds),
    封面链接: urlValue(firstCoverUrl(item)),
    播放量: numeric(m.viewCount),
    点赞量: numeric(m.likeCount),
    评论量: numeric(m.commentCount),
    分享量: numeric(m.shareCount),
    收藏量: numeric(m.favoriteCount),
    主页访问量: numeric(m.homepageVisitCount),
    粉丝增量: numeric(m.subscribeCount),
    取关量: numeric(m.unsubscribeCount),
    弹幕量: numeric(m.danmakuCount),
    下载量: numeric(m.downloadCount),
    不喜欢量: numeric(m.dislikeCount),
    封面展现: numeric(m.coverShow),
    平均播放秒: numeric(m.avgViewSecond),
    '平均播放占比%': numeric(m.avgViewProportion),
    '完播率%': numeric(m.completionRate),
    '5秒完播率%': numeric(m.completionRate5s),
    '2秒跳出率%': numeric(m.bounceRate2s),
    '粉丝观看占比%': numeric(m.fanViewProportion),
    '点赞率%': numeric(m.likeRate),
    '评论率%': numeric(m.commentRate),
    '分享率%': numeric(m.shareRate),
    '收藏率%': numeric(m.favoriteRate),
    '涨粉率%': numeric(m.subscribeRate),
    '取关率%': numeric(m.unsubscribeRate),
    '不喜欢率%': numeric(m.dislikeRate),
  };
}

function buildDailyFields(analysis) {
  const a = analysis.analysis?.account || {};
  const c = analysis.analysis?.content || {};
  return {
    日期: new Date(analysis.collectedAt).toISOString().slice(0, 10),
    同步时间: analysis.collectedAt,
    统计周期: `${analysis.days || 90}天`,
    作品数: numeric(analysis.analysis?.items?.count),
    昨日播放量: compact(a.yesterday?.plays),
    主页访问: compact(a.yesterday?.profileVisits),
    作品点赞: compact(a.yesterday?.likes),
    作品分享: compact(a.yesterday?.shares),
    作品评论: compact(a.yesterday?.comments),
    净增粉丝: compact(a.yesterday?.netFans),
    总粉丝量: compact(a.yesterday?.totalFans),
    周期投稿量: compact(c.posts),
    条均点击率: compact(c.avgClickRate),
    条均5s完播率: compact(c.avg5sCompletionRate),
    条均2s跳出率: compact(c.avg2sBounceRate),
    条均播放时长: compact(c.avgWatchTime),
    播放量中位数: compact(c.medianPlays),
    建议摘要: (analysis.analysis?.summary || []).join('\n').slice(0, 1800),
  };
}

function stripUndefined(fields) {
  return Object.fromEntries(Object.entries(fields).filter(([, value]) => value !== undefined));
}

function requireOk(body, action) {
  if (body.code !== 0) {
    throw new Error(`${action} failed: ${body.msg || `code ${body.code}`}`);
  }
  return body.data || {};
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function isRetryableFeishuError(err) {
  return /1254607|Data not ready|please try again later|HTTP 429|HTTP 5\d\d/i.test(err.message || '');
}

async function withFeishuRetry(action, fn, attempts = 5) {
  let lastError = null;
  for (let attempt = 1; attempt <= attempts; attempt += 1) {
    try {
      return await fn();
    } catch (err) {
      lastError = err;
      if (!isRetryableFeishuError(err) || attempt === attempts) break;
      await sleep(800 * attempt * attempt);
    }
  }
  throw lastError;
}

async function createBitable(name) {
  const body = await callFeishuOpenApi('/bitable/v1/apps', {
    method: 'POST',
    body: { name },
  });
  const data = requireOk(body, 'create bitable');
  return data.app?.app_token || data.app_token;
}

async function listTables(appToken) {
  const body = await callFeishuOpenApi(`/bitable/v1/apps/${encodeURIComponent(appToken)}/tables?page_size=100`, {
    method: 'GET',
  });
  return requireOk(body, 'list tables').items || [];
}

async function ensureTable(appToken, name, fieldsSpec, stateKey, state) {
  const tables = await listTables(appToken);
  const existing = tables.find((table) => table.name === name || table.table_id === state[stateKey]);
  if (existing) {
    state[stateKey] = existing.table_id;
    return existing.table_id;
  }

  const fields = fieldsSpec.map(([fieldName, type]) => ({
    field_name: fieldName,
    type: FIELD_TYPES[type] || FIELD_TYPES.text,
  }));
  const body = await callFeishuOpenApi(`/bitable/v1/apps/${encodeURIComponent(appToken)}/tables`, {
    method: 'POST',
    body: {
      table: {
        name,
        default_view_name: '默认视图',
        fields,
      },
    },
  });
  const data = requireOk(body, `create table ${name}`);
  const tableId = data.table_id || data.table?.table_id;
  if (!tableId) throw new Error(`create table ${name} did not return table_id`);
  state[stateKey] = tableId;
  return tableId;
}

async function searchRecords(appToken, tableId, fieldName, value) {
  const body = await withFeishuRetry(`search ${fieldName}`, () => callFeishuOpenApi(`/bitable/v1/apps/${encodeURIComponent(appToken)}/tables/${encodeURIComponent(tableId)}/records/search?page_size=20`, {
    method: 'POST',
    body: {
      filter: {
        conjunction: 'and',
        conditions: [{
          field_name: fieldName,
          operator: 'is',
          value: [String(value)],
        }],
      },
    },
  }));
  return requireOk(body, `search ${fieldName}`).items || [];
}

async function createRecord(appToken, tableId, fields) {
  const body = await withFeishuRetry('create record', () => callFeishuOpenApi(`/bitable/v1/apps/${encodeURIComponent(appToken)}/tables/${encodeURIComponent(tableId)}/records`, {
    method: 'POST',
    body: { fields: stripUndefined(fields) },
  }));
  return requireOk(body, 'create record').record;
}

async function updateRecord(appToken, tableId, recordId, fields) {
  const body = await withFeishuRetry('update record', () => callFeishuOpenApi(`/bitable/v1/apps/${encodeURIComponent(appToken)}/tables/${encodeURIComponent(tableId)}/records/${encodeURIComponent(recordId)}`, {
    method: 'PUT',
    body: { fields: stripUndefined(fields) },
  }));
  return requireOk(body, 'update record').record;
}

async function upsertRecord(appToken, tableId, keyField, fields) {
  const value = fields[keyField];
  const found = await searchRecords(appToken, tableId, keyField, value);
  if (found[0]?.record_id) {
    await updateRecord(appToken, tableId, found[0].record_id, fields);
    return { action: 'updated', recordId: found[0].record_id };
  }
  const record = await createRecord(appToken, tableId, fields);
  return { action: 'created', recordId: record?.record_id };
}

function runAnalysis(days, output) {
  const result = spawnSync(process.execPath, [
    join(__dirname, 'douyin-data-analysis.js'),
    '--days',
    String(days),
    '--output',
    output,
  ], {
    cwd: join(__dirname, '..'),
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: 180000,
  });
  const text = `${result.stderr || ''}${result.stdout || ''}`.trim();
  const payload = existsSync(output) ? JSON.parse(readFileSync(output, 'utf8')) : lastJson(text);
  if (result.status !== 0 || !payload?.ok) {
    throw new Error(`data analysis failed: ${payload?.error || text.slice(0, 600) || result.status}`);
  }
  return payload;
}

function summarizeForFeishu(analysis, worksResult) {
  const top = [...(analysis.analysis?.items?.details || [])]
    .sort((a, b) => (b.metrics?.viewCount || 0) - (a.metrics?.viewCount || 0))[0];
  const lines = [
    `数据已更新：近 ${analysis.days || 90} 天，作品 ${analysis.analysis?.items?.count || 0} 条。`,
  ];
  if (worksResult) lines.push(`新增 ${worksResult.created} 条，更新 ${worksResult.updated} 条。`);
  if (top) lines.push(`播放最高：${top.title || top.id}（${top.metrics?.viewCount ?? '-'}）。`);
  return lines.join('\n');
}

function bitableUrl(appToken, tableId) {
  return `https://feishu.cn/base/${encodeURIComponent(appToken)}?table=${encodeURIComponent(tableId)}`;
}

function buildNotifyText(result) {
  return [
    result.feishuText,
    `多维表：${bitableUrl(result.appToken, result.tables.workTableId)}`,
  ].join('\n');
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const days = Math.max(1, Math.min(365, Number(args.days || 90)));
  mkdirSync(REPORT_DIR, { recursive: true });
  const output = args.input || args.output || join(REPORT_DIR, `douyin-data-sync-${Date.now()}.json`);
  const analysis = args.input ? JSON.parse(readFileSync(args.input, 'utf8')) : runAnalysis(days, output);
  const state = loadState();
  const appToken = args.appToken || process.env.FEISHU_BITABLE_APP_TOKEN || state.appToken || await createBitable(`抖音数据看板-${new Date().toISOString().slice(0, 10)}`);
  state.appToken = appToken;

  const workTableId = args.worksTableId || process.env.FEISHU_BITABLE_WORKS_TABLE_ID || await ensureTable(appToken, WORK_TABLE_NAME, WORK_FIELDS, 'worksTableId', state);
  const dailyTableId = args.dailyTableId || process.env.FEISHU_BITABLE_DAILY_TABLE_ID || await ensureTable(appToken, DAILY_TABLE_NAME, DAILY_FIELDS, 'dailyTableId', state);
  const logTableId = args.logTableId || process.env.FEISHU_BITABLE_LOG_TABLE_ID || await ensureTable(appToken, LOG_TABLE_NAME, LOG_FIELDS, 'logTableId', state);
  state.worksTableId = workTableId;
  state.dailyTableId = dailyTableId;
  state.logTableId = logTableId;
  saveState(state);

  const works = analysis.analysis?.items?.details || [];
  const worksResult = { created: 0, updated: 0, records: [] };
  for (const item of works) {
    if (!item.id) continue;
    const record = await upsertRecord(appToken, workTableId, '作品ID', buildWorkFields(item, analysis));
    worksResult[record.action === 'created' ? 'created' : 'updated'] += 1;
    worksResult.records.push({ id: item.id, ...record });
  }

  const dailyFields = buildDailyFields(analysis);
  const daily = await upsertRecord(appToken, dailyTableId, '日期', dailyFields);
  await createRecord(appToken, logTableId, {
    同步时间: analysis.collectedAt,
    状态: '成功',
    近N天: analysis.days || days,
    作品数: works.length,
    新增: worksResult.created,
    更新: worksResult.updated,
    信息: summarizeForFeishu(analysis, worksResult),
  });

  const result = {
    ok: true,
    appToken,
    tables: { workTableId, dailyTableId, logTableId },
    days: analysis.days || days,
    itemCount: works.length,
    works: worksResult,
    daily,
    reportPath: output,
    feishuText: summarizeForFeishu(analysis, worksResult),
  };
  result.notifyText = buildNotifyText(result);
  if (args.notify) {
    result.notify = await sendFeishuText(result.notifyText);
  }
  console.log(JSON.stringify(result, null, 2));
}

main().catch(async (err) => {
  const missingBitableScope = /99991672|bitable:app|base:app:create/.test(err.message || '');
  const authUrl = missingBitableScope
    ? buildFeishuScopeAuthUrl(['bitable:app', 'base:app:create'])
    : undefined;
  const payload = {
    ok: false,
    error: err.message,
    actionRequired: missingBitableScope
      ? '飞书应用缺少多维表权限。请打开 authUrl 授权 bitable:app 或 base:app:create；如果使用已有多维表，还需把 FEISHU_BITABLE_APP_TOKEN 配到 .env。'
      : undefined,
    authUrl,
    notified: false,
    stack: err.stack,
  };
  if (process.argv.includes('--notify')) {
    const notify = await sendFeishuText(missingBitableScope
      ? `数据更新失败：需要开通飞书多维表权限。\n请点击授权：${authUrl}`
      : `数据更新失败：${err.message.slice(0, 180)}`);
    payload.notified = Boolean(notify?.ok);
    payload.notify = notify;
  }
  console.log(JSON.stringify(payload, null, 2));
  process.exit(1);
});
