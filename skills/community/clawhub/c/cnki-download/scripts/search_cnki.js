#!/usr/bin/env node
/**
 * 知网检索 + 下载 pipeline 的 CLI 入口（Node.js port）
 *
 * 用法
 * ----
 *     # 用默认 demo config
 *     node search_cnki.js
 *
 *     # 读 JSON 配置文件
 *     node search_cnki.js my_config.json
 *
 *     # 传 JSON 字符串
 *     node search_cnki.js --json '{"keyword":"区块链","download_count":3}'
 *
 *     # 在自己代码里 import
 *     import { runPipeline } from './cnki_pipeline.js';
 *
 * 入口 URL（cnki_url）：从 scripts/user_config.json 的 "url" 字段读取，
 *                       也可以在传入的 config 里直接用 "cnki_url" 字段覆盖。
 *
 * config JSON Schema 见 cnki_pipeline.js 模块顶部。
 */

import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { runPipeline } from './cnki_pipeline.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ===================== 默认 demo config =====================
// 跑 `node search_cnki.js` 不带参数时用这个
const DEFAULT_CONFIG = {
  keyword: '区块链',
  sort: {
    field: '发表时间',
    order: 'DESC',
  },
  filters: [
    { col: '来源类别', values: ['北大核心', 'CSSCI'] },
    { col: '年度',     values: ['2024', '2025'] },
  ],
  download_count: 5,
};

/**
 * 读取 JSON 文件，自动兼容 UTF-8 BOM 前缀。
 * Node.js 的 `JSON.parse()` 不接受 BOM 字符（`\uFEFF`）开头，会抛 `Unexpected token` 错误。
 * 本 helper 手动剥除 BOM 后再 parse，避免 agent 不小心用 PowerShell 写出带 BOM 的 JSON 时崩溃。
 *
 * 兜底作用：SKILL.md 的关键约束里已经强制要求所有 JSON 无 BOM + 写完 JSON.parse 验证，
 * 这里再做一层读取兼容，给写文件侧一个安全网。
 */
async function readJsonCompat(p) {
  const buf = await fs.readFile(p, 'utf-8');
  const clean = buf.charCodeAt(0) === 0xFEFF ? buf.slice(1) : buf;
  return JSON.parse(clean);
}

/**
 * 从 JSON 文件读 config（兼容 BOM）。
 */
async function loadConfig(p) {
  return readJsonCompat(p);
}

/**
 * 简单 argv 解析：
 *   - 第一个非 -- 开头参数：JSON 文件路径
 *   - --json 后的参数：JSON 字符串
 */
function parseArgs(argv) {
  const args = argv.slice(2);
  const out = { configFile: null, json: null };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--json') {
      out.json = args[++i] ?? '';
    } else if (a.startsWith('--json=')) {
      out.json = a.slice('--json='.length);
    } else if (a === '-h' || a === '--help') {
      out.help = true;
    }  else if (!a.startsWith('--')) {
      out.configFile = a;
    }
    // 其它 flag 忽略
  }
  return out;
}

function printHelp() {
  console.log('用法:');
  console.log('  node search_cnki.js                          # 默认 demo');
  console.log('  node search_cnki.js <config.json>            # 读 JSON 配置文件');
  console.log('  node search_cnki.js --json \'{"keyword":...}\' # 传 JSON 字符串');
  console.log('');
  console.log('入口 URL：自动从 scripts/user_config.json 的 "url" 字段读取，');
  console.log('         也可以在 config 里用 "cnki_url" 字段覆盖。');
  console.log('');
  console.log('config JSON Schema 见 cnki_pipeline.js 模块顶部 README。');
}

/**
 * 从 user_config.json 读 cnki_url。
 * 返回 null 表示配置文件为空 / 不存在 / 没有 url 字段。
 */
async function loadUserConfigUrl() {
  try {
    const ucPath = path.join(__dirname, 'user_config.json');
    const uc = await readJsonCompat(ucPath);
    if (uc && typeof uc.url === 'string' && uc.url.trim() !== '') {
      return uc.url.trim();
    }
    return null;
  } catch {
    return null;
  }
}

async function main() {
  const args = parseArgs(process.argv);

  if (args.help) {
    printHelp();
    return 0;
  }

  // 加载 config
  let config;
  if (args.json != null && args.json !== '') {
    try {
      config = JSON.parse(args.json);
    } catch (e) {
      console.error(`❌ --json 解析失败: ${e.message ?? e}`);
      return 2;
    }
    console.log('📋 使用 --json 传入的 config:');
  } else if (args.configFile) {
    try {
      config = await loadConfig(args.configFile);
    } catch (e) {
      console.error(`❌ 读取 config 文件失败: ${args.configFile}: ${e.message ?? e}`);
      return 2;
    }
    console.log(`📋 读取 config 文件: ${args.configFile}`);
  } else {
    config = DEFAULT_CONFIG;
    console.log('📋 未指定 config，使用默认 demo:');
  }

  // 注入 cnki_url：先看 config 本身，再看 user_config.json
  if (!config.cnki_url) {
    const url = await loadUserConfigUrl();
    if (url) {
      config.cnki_url = url;
      console.log(`📋 从 user_config.json 读取 url: ${url}`);
    } else {
      console.error(
        '❌ 未找到 cnki_url。请在 scripts/user_config.json 中写入 {"url": "<你的知网搜索页面URL>"}，\n' +
        '   或者在传入的 config 中直接包含 "cnki_url" 字段。'
      );
      return 2;
    }
  } else {
    console.log(`📋 使用 config 中的 cnki_url: ${config.cnki_url}`);
  }

  console.log(JSON.stringify(config, null, 2));
  console.log('');

  // 跑 pipeline
  const result = await runPipeline(config);

  // 退出码：全部下载成功 → 0，否则 1
  const target = config.download_count ?? 0;
  return result.downloaded === target ? 0 : 1;
}

main().then(
  (code) => process.exit(code),
  (err) => {
    console.error('❌ 未捕获错误:', err);
    process.exit(1);
  }
);
