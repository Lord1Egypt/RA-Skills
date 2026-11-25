#!/usr/bin/env node
/**
 * Offline validator for structured notes from the read-only procedure in
 * SKILL.md. It never connects to Bilibili or changes a draft.
 */
import fs from 'node:fs';

const required = ['cover', 'title', 'description', 'category', 'assets'];
const maxRows = 100;
const labels = { cover: '封面', title: '标题', description: '简介', category: '分区', assets: '素材' };

function die(message, code = 2) {
  process.stderr.write(`检查失败：${message}\n`);
  process.exit(code);
}

function hasContent(value) {
  if (typeof value === 'string') return value.trim().length > 0 && value.trim() !== '未确认';
  if (Array.isArray(value)) return value.some(hasContent);
  if (value && typeof value === 'object') return Object.values(value).some(hasContent);
  return value !== undefined && value !== null && value !== false;
}

function isValidSource(source) {
  return source && typeof source === 'object'
    && required.includes(source.field)
    && typeof source.visible_location === 'string' && source.visible_location.trim().length > 0
    && typeof source.captured_text === 'string' && source.captured_text.trim().length > 0;
}

const inputPath = process.argv[2];
if (!inputPath) die('请提供离线页面资料 JSON 文件路径。');
let note;
try { note = JSON.parse(fs.readFileSync(inputPath, 'utf8')); } catch { die('输入不是可读取的 JSON。'); }
if (note.fixture_kind !== 'offline-page-notes') die('仅接受明确标注为 offline-page-notes 的资料；不可把样例当在线采集结果。');
if (note.owner_confirmed !== true) die('账号或稿件归属未确认，已停止。');
if (note.page_confirmed !== true) die('当前页面不是可确认的投稿草稿页，已停止。');
if (!Array.isArray(note.sources) || note.sources.length === 0) die('每个字段都需要绑定的可见来源。');
if (!note.sources.every(isValidSource)) die('来源必须绑定 field，并提供非空的 visible_location 和 captured_text。');

const fields = note.fields && typeof note.fields === 'object' && !Array.isArray(note.fields) ? note.fields : {};
let totalRows = Array.isArray(fields.assets) ? fields.assets.length : 0;
if (note.tables !== undefined) {
  if (!note.tables || typeof note.tables !== 'object' || Array.isArray(note.tables)) die('tables 必须是表名到行数组的对象。');
  for (const [name, rows] of Object.entries(note.tables)) {
    if (!Array.isArray(rows)) die(`表格 ${name} 必须是行数组。`);
    totalRows += rows.length;
  }
}
if (totalRows > maxRows) die(`素材与表格合计超过 ${maxRows} 行，请先分批。`);
const missing = [];
const present = {};
const fieldSources = {};
for (const key of required) {
  const sources = note.sources.filter((source) => source.field === key);
  if (!sources.length) die(`${labels[key]}没有绑定可见来源，不能输出已见或缺项结论。`);
  fieldSources[key] = sources.map(({ visible_location, captured_text }) => ({ visible_location, captured_text }));
  if (!hasContent(fields[key])) missing.push(key); else present[key] = fields[key];
}

const suggestions = missing.map((key) => ({ field: labels[key], advice: `补齐${labels[key]}后再进行发布前核对。` }));
if (!missing.length) suggestions.push({ field: '完整性', advice: '可进入人工复核；本工具不会保存、提交或发布稿件。' });

process.stdout.write(`${JSON.stringify({
  mode: 'offline-fixture-validation',
  status: missing.length ? 'needs-completion' : 'ready-for-human-review',
  visible_fields: present,
  missing: missing.map((key) => labels[key]),
  suggestions,
  field_sources: fieldSources
}, null, 2)}\n`);
