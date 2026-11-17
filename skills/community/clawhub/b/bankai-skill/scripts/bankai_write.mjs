#!/usr/bin/env node
// bankai_write.mjs — BankAI 写作脚本
// 用法:
//   node bankai_write.mjs --type <id或名称> --input <JSON或@文件路径> [--output 文件] [--key-env DEEPSEEK_API_KEY] [--base-url URL] [--model deepseek-chat] [--mock]
//   node bankai_write.mjs --list                 # 列出全部 59 种
//
// 行为: 查 scenarios.mjs 取对应公文类型 → 用其 buildUserPrompt(data) 组装 user prompt
//       → 调 DeepSeek 官方 OpenAI 兼容接口 → 输出纯文本底稿。

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const { SCENARIOS } = await import(pathToFileURL(join(__dirname, '..', 'references', 'scenarios.mjs')).href);

const DEFAULT_BASE = 'https://api.deepseek.com/chat/completions';
const DEFAULT_MODEL = 'deepseek-chat';
const TEMP = 0.7;
const MAX_TOKENS = 8192;

// ---------- 参数解析 ----------
function parseArgs(argv) {
  const a = { type: null, input: null, output: null, keyEnv: 'DEEPSEEK_API_KEY', baseUrl: null, model: DEFAULT_MODEL, mock: false, list: false };
  for (let i = 0; i < argv.length; i++) {
    const t = argv[i];
    if (t === '--type') a.type = argv[++i];
    else if (t === '--input') a.input = argv[++i];
    else if (t === '--output') a.output = argv[++i];
    else if (t === '--key-env') a.keyEnv = argv[++i];
    else if (t === '--base-url') a.baseUrl = argv[++i];
    else if (t === '--model') a.model = argv[++i];
    else if (t === '--mock') a.mock = true;
    else if (t === '--list') a.list = true;
  }
  return a;
}

function fail(msg) { console.error('[bankai] ' + msg); process.exit(1); }

// ---------- 列出 ----------
if (parseArgs(process.argv.slice(2)).list) {
  for (const s of SCENARIOS) console.log(`${s.id}\t[${s.category}]\t${s.name}`);
  process.exit(0);
}

// ---------- 主流程 ----------
const args = parseArgs(process.argv.slice(2));
if (!args.type) fail('缺少 --type（公文类型 id 或名称），可用 --list 查看');
if (!args.input) fail('缺少 --input（JSON 或 @文件路径，含各字段值）');

// 解析公文类型：仅精确 id 或精确名称（银行场景选错文档危害大，宁可报错也不猜）
function resolveScene(type) {
  const t = type.trim();
  const s = SCENARIOS.find(x => x.id === t) || SCENARIOS.find(x => x.name === t);
  if (s) return s;
  const avail = SCENARIOS.slice(0, 15).map(x => `  ${x.id}\t${x.name}`).join('\n');
  fail(`未找到公文类型: ${t}（须为精确 id 或名称）\n可用类型（前15，完整见 --list）：\n${avail}`);
}
const scen = resolveScene(args.type);

// 解析输入
let raw = args.input;
if (raw.startsWith('@')) raw = readFileSync(raw.slice(1), 'utf8');
let data;
try { data = JSON.parse(raw); }
catch { fail('--input 必须是合法 JSON（字段键值对），或 @文件路径'); }
if (typeof data !== 'object' || data === null) fail('--input JSON 必须是对象');

const userPrompt = scen.buildUserPrompt(data);
// 反编造护栏（硬性铁律，前置为最高优先级指令）：银行场景编造精确数字/文号/人名会造成实质性危害
const GUARD = '【数据真实性铁律 · 最高优先级】你正在生成一份“草稿/模板底稿”，不是已核实的真实文件。\n' +
  '1. 仅可使用用户在输入中逐字提供的真实信息；输入未给定的任何具体数值、金额、比例、人名、机构名、文号、日期，一律严禁编造。\n' +
  '2. 凡输入未提供的量化字段，必须原样写成占位符「XX」（如 XX万元、XX%、XX人、XX公司），' +
  '禁止写出看似精确的虚假数字（如 12,300.00万元、39.02%、发明专利12项、委员7人）。\n' +
  '3. 文末必须单列「需人工核实/补充项」，逐条列出所有被占位的字段及应填入的真实来源。\n' +
  '4. 若用户输入本身含具体数字，可直接使用并在其后标注「（用户提供）」。\n' +
  '5. 严禁 Markdown 格式（#、##、**、- 等符号），仅使用中文全角标点与“一、二、三”“（一）”等章节序号。\n' +
  '违反上述任一条即视为严重错误。\n\n' +
  scen.systemPrompt;
const messages = [
  { role: 'system', content: GUARD },
  { role: 'user', content: userPrompt },
];

// ---------- mock 模式（测试/离线）----------
if (args.mock) {
  const out = `【${scen.name} · 模拟输出】（mock 模式，未真实调用模型）\n\n` +
    `以下为按 ${scen.name} 格式生成的占位底稿，请接入真实 API 后替换：\n\n` +
    userPrompt.split('\n').slice(0, 3).join('\n') + '\n…（正文省略）…';
  emit(out, args.output);
  process.exit(0);
}

// ---------- 真实调用（带超时 + 限流重试）----------
const apiKey = process.env[args.keyEnv];
if (!apiKey) fail(`未找到 API Key：环境变量 ${args.keyEnv} 为空（或用 --mock 离线测试）`);

const base = args.baseUrl || DEFAULT_BASE;
const body = JSON.stringify({ model: args.model, messages, temperature: TEMP, max_tokens: MAX_TOKENS, stream: false });
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

async function callDeepSeek(attempt) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 120000); // 整体超时 120s，避免限流时永久挂起
  let resp;
  try {
    resp = await fetch(base, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${apiKey}` },
      body,
      signal: ctrl.signal,
    });
  } catch (e) {
    clearTimeout(timer);
    if (attempt < 3 && /aborted|timeout|network|ECONN|ETIMEDOUT/i.test(e.message)) {
      console.error(`[bankai] 网络异常（第${attempt}次），3s 后重试…`);
      await sleep(3000);
      return callDeepSeek(attempt + 1);
    }
    fail(`调用 DeepSeek 失败（网络/URL 错误）: ${e.message}`);
  }
  clearTimeout(timer);
  if (!resp.ok) {
    let detail = '';
    try { detail = (await resp.json())?.error?.message || ''; } catch {}
    // 429 限流 / 5xx：退避重试
    if (attempt < 3 && (resp.status === 429 || resp.status >= 500)) {
      const wait = resp.status === 429 ? 8000 : 4000;
      console.error(`[bankai] DeepSeek 返回 ${resp.status}${detail ? '：' + detail : ''}（第${attempt}次），${wait / 1000}s 后重试…`);
      await sleep(wait);
      return callDeepSeek(attempt + 1);
    }
    fail(`DeepSeek 返回 ${resp.status}${detail ? '：' + detail : ''}`);
  }
  const json = await resp.json();
  const text = json?.choices?.[0]?.message?.content;
  if (!text) fail('DeepSeek 响应中未包含内容');
  return text.trim();
}

const out = await callDeepSeek(1);
emit(out, args.output);
process.exit(0);

function emit(text, output) {
  if (output) { writeFileSync(output, text, 'utf8'); console.error(`[bankai] 已写入 ${output}`); }
  else console.log(text);
}
