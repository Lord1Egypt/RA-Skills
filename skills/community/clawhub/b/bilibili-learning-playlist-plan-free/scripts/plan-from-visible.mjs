#!/usr/bin/env node
import fs from 'node:fs';

const [inputPath, outputPath] = process.argv.slice(2);
if (!inputPath || !outputPath) throw new Error('用法: node scripts/plan-from-visible.mjs 输入.json 输出.md');
const input = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
if (!input.goal?.trim() || !Number.isFinite(input.dailyMinutes) || input.dailyMinutes <= 0 || !Array.isArray(input.items)) {
  throw new Error('需要 goal、正数 dailyMinutes 和 items 数组');
}
if (input.collectionAccess === 'unauthorized' || input.authorization === 'unauthorized') {
  throw new Error('私人收藏夹未授权：停止读取，未生成学习顺序或日程');
}
if (input.items.length > 100) throw new Error('单批最多 100 条；请分批处理');
if (input.learningDays !== undefined && (!Number.isInteger(input.learningDays) || input.learningDays <= 0)) {
  throw new Error('learningDays 如提供，必须是正整数');
}

function parseVisibleDuration(value) {
  if (typeof value !== 'string') return null;
  const parts = value.trim().split(':');
  if (parts.length !== 2 && parts.length !== 3 || parts.some(part => !/^\d{1,2}$/.test(part))) return null;
  const numbers = parts.map(Number);
  if (numbers.slice(1).some(part => part >= 60)) return null;
  const seconds = parts.length === 2
    ? numbers[0] * 60 + numbers[1]
    : numbers[0] * 3600 + numbers[1] * 60 + numbers[2];
  return seconds > 0 ? seconds / 60 : null;
}

function markdownCell(value) {
  return String(value ?? '未知').replace(/\\/g, '\\\\').replace(/\|/g, '\\|').replace(/[\r\n]+/g, '<br>');
}

function formatMinutes(minutes) {
  return Number.isInteger(minutes) ? String(minutes) : minutes.toFixed(2).replace(/\.00$/, '');
}

const terms = input.goal.toLowerCase().split(/[\s,，、/]+/).filter(Boolean);
const rows = input.items.map((item, index) => {
  if (!item.title || !item.source) throw new Error(`第 ${index + 1} 条缺少 title 或 source`);
  if (Object.hasOwn(item, 'visibleMinutes') && Object.hasOwn(item, 'visibleDuration')) {
    throw new Error(`第 ${index + 1} 条的 visibleMinutes 与 visibleDuration 只能二选一`);
  }
  const text = `${item.title} ${item.description || ''}`.toLowerCase();
  const hits = terms.filter(term => text.includes(term));
  // visibleMinutes is explicitly minutes. For browser-visible clock text use visibleDuration.
  const minutes = Number.isFinite(item.visibleMinutes) && item.visibleMinutes > 0
    ? item.visibleMinutes
    : parseVisibleDuration(item.visibleDuration);
  return { ...item, minutes, hits, original: index };
}).sort((a, b) => b.hits.length - a.hits.length || a.original - b.original);
let day = 1, used = 0;
for (const row of rows) {
  if (!row.minutes) { row.day = '未知时长，不计入预算'; continue; }
  if (row.minutes > input.dailyMinutes) { row.day = '超过单日预算，未排期'; continue; }
  if (used && used + row.minutes > input.dailyMinutes) { day++; used = 0; }
  if (input.learningDays && day > input.learningDays) { row.day = `超出 ${input.learningDays} 天范围，未排期`; continue; }
  row.day = day;
  used += row.minutes;
}
const out = [
  '# B站合集学习顺序单（可见资料草稿）',
  '',
  `- 学习目标：${markdownCell(input.goal)}`,
  `- 每日预算：${input.dailyMinutes} 分钟`,
  ...(input.learningDays ? [`- 可选学习天数：${input.learningDays} 天（超出范围的条目不排期）`] : []),
  '- 说明：排序仅匹配标题与可见简介；不代表内容已验证。',
  '',
  '| 顺序 | 日程 | 标题 | 可见简介 | 可见时长 | 匹配理由 | 来源 | 缺项 |',
  '|---:|---|---|---|---|---|---|---|',
  ...rows.map((r, i) => {
    const unscheduled = typeof r.day === 'string' && r.day !== '未知时长，不计入预算';
    const missingItems = [];
    if (!r.description?.trim()) missingItems.push('简介不可见');
    if (!r.minutes) missingItems.push('时长不可见');
    if (unscheduled) missingItems.push(r.day);
    const missing = missingItems.length ? missingItems.join('；') : '无';
    return `| ${i + 1} | ${markdownCell(r.day)} | ${markdownCell(r.title)} | ${markdownCell(r.description || '未知')} | ${r.minutes ? `${formatMinutes(r.minutes)} 分钟` : '未知'} | ${markdownCell(r.hits.length ? `标题/简介含：${r.hits.join('、')}` : '未匹配目标词，按原页面顺序')} | ${markdownCell(r.source)} | ${markdownCell(missing)} |`;
  }),
  '',
  '## 缺项与暂停条件',
  '',
  '- 私人收藏夹未授权、登录/验证码/风控：停止读取，不尝试绕过。',
  '- 时长不可见：标为未知，不计入每日分钟预算。',
  '- 单条时长超过每日预算或超出可选学习天数：保留在清单中但不排入日程。'
].join('\n');
fs.writeFileSync(outputPath, `${out}\n`);
