#!/usr/bin/env node
/**
 * Convert llms-latest.json → Feishu Bitable batch_create / batch_update payloads.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CACHE_DIR =
  process.env.AA_MODELS_CACHE ||
  path.join(process.env.HOME || '/tmp', '.openclaw', 'cache', 'artificial-analysis');

/** Bitable 列名（与 SKILL 中建表字段一致） */
export const BITABLE_FIELDS = [
  '模型ID',
  '模型名称',
  'Slug',
  '厂商',
  '智能指数',
  '编程指数',
  '数学指数',
  'MMLU Pro(%)',
  'GPQA(%)',
  'HLE(%)',
  'LiveCodeBench(%)',
  'SciCode(%)',
  'MATH-500(%)',
  'AIME(%)',
  '综合价格($/1M)',
  '输入价格($/1M)',
  '输出价格($/1M)',
  '输出速度(tok/s)',
  '首Token延迟(s)',
  '数据来源',
  '更新时间',
];

function pctOrDash(v) {
  return v == null ? '' : `${v}%`;
}

function numOrEmpty(v) {
  return v == null ? '' : v;
}

export function modelToBitableFields(m) {
  return {
    模型ID: m.id,
    模型名称: m.name,
    Slug: m.slug || '',
    厂商: m.creator_name || '',
    智能指数: numOrEmpty(m.intelligence_index),
    编程指数: numOrEmpty(m.coding_index),
    数学指数: numOrEmpty(m.math_index),
    'MMLU Pro(%)': pctOrDash(m.mmlu_pro),
    'GPQA(%)': pctOrDash(m.gpqa),
    'HLE(%)': pctOrDash(m.hle),
    'LiveCodeBench(%)': pctOrDash(m.livecodebench),
    'SciCode(%)': pctOrDash(m.scicode),
    'MATH-500(%)': pctOrDash(m.math_500),
    'AIME(%)': pctOrDash(m.aime),
    '综合价格($/1M)': numOrEmpty(m.price_blended_3_1),
    '输入价格($/1M)': numOrEmpty(m.price_input_1m),
    '输出价格($/1M)': numOrEmpty(m.price_output_1m),
    '输出速度(tok/s)': numOrEmpty(m.output_tps),
    '首Token延迟(s)': numOrEmpty(m.ttft_seconds),
    数据来源: m.source || 'artificialanalysis.ai',
    更新时间: m.fetched_at || new Date().toISOString(),
  };
}

export function buildTableFieldDefs() {
  return [
    { field_name: '模型ID', type: 1 },
    { field_name: '模型名称', type: 1 },
    { field_name: 'Slug', type: 1 },
    { field_name: '厂商', type: 1 },
    { field_name: '智能指数', type: 2 },
    { field_name: '编程指数', type: 2 },
    { field_name: '数学指数', type: 2 },
    { field_name: 'MMLU Pro(%)', type: 1 },
    { field_name: 'GPQA(%)', type: 1 },
    { field_name: 'HLE(%)', type: 1 },
    { field_name: 'LiveCodeBench(%)', type: 1 },
    { field_name: 'SciCode(%)', type: 1 },
    { field_name: 'MATH-500(%)', type: 1 },
    { field_name: 'AIME(%)', type: 1 },
    { field_name: '综合价格($/1M)', type: 2 },
    { field_name: '输入价格($/1M)', type: 2 },
    { field_name: '输出价格($/1M)', type: 2 },
    { field_name: '输出速度(tok/s)', type: 2 },
    { field_name: '首Token延迟(s)', type: 2 },
    { field_name: '数据来源', type: 1 },
    { field_name: '更新时间', type: 1 },
  ];
}

function main() {
  const input = process.argv[2] || path.join(CACHE_DIR, 'llms-latest.json');
  if (!fs.existsSync(input)) {
    console.error(`找不到 ${input}，请先运行 fetch-llms.mjs`);
    process.exit(1);
  }
  const { models } = JSON.parse(fs.readFileSync(input, 'utf8'));
  const records = models.map((m) => ({ fields: modelToBitableFields(m) }));

  const outDir = path.dirname(input);
  const recordsPath = path.join(outDir, 'bitable-records.json');
  const fieldsPath = path.join(outDir, 'bitable-field-defs.json');

  fs.writeFileSync(recordsPath, JSON.stringify({ count: records.length, records }, null, 2));
  fs.writeFileSync(fieldsPath, JSON.stringify(buildTableFieldDefs(), null, 2));

  console.log(`✅ ${records.length} 条记录 → ${recordsPath}`);
  console.log(`FIELD_DEFS:${fieldsPath}`);
  console.log(`RECORDS:${recordsPath}`);
}

if (process.argv[1]?.endsWith('build-bitable-records.mjs')) {
  main();
}
