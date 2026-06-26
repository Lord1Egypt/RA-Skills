#!/usr/bin/env node
// name: store-rebate
// description: 搜索海外商家，查询返利比例和佣金计划，生成返利链接

import { fileURLToPath } from 'url';
import { join, dirname } from 'path';
import { existsSync } from 'fs';

// ── 加载公共库 ──
const _scriptDir = dirname(fileURLToPath(import.meta.url));
const _fxApiPath = join(_scriptDir, '../../fx-base/scripts/fx-api.mjs');
if (!existsSync(_fxApiPath)) {
  process.stderr.write(
    '{"status":"error","error_type":"missing_dependency","suggestion":"缺少 fx-base，请安装：npx skills install fangshan101-coder/fx-base"}\n'
  );
  process.exit(1);
}

const { fxCheckAuth, fxPost } = await import(_fxApiPath);

function help() {
  process.stdout.write(`用法: store-rebate --store <商家名> [选项]

必填:
  --store <商家名>                 海外商家名称（如 iHerb、Nike、Amazon）

选项:
  --format json|table              输出格式（默认 json）
  --help                           显示此帮助

示例:
  store-rebate --store "iHerb"
  store-rebate --store "Nike"
  store-rebate --store "Amazon" --format table

数据流向: 商家查询会被发送到 https://api-ai-brain.fenxianglife.com 进行搜索
`);
  process.exit(0);
}

// ── 参数解析 ──
const args = process.argv.slice(2);
let storeName = '';
let format = 'json';

for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case '--help':
    case '-h':
      help();
      break;
    case '--store':
      storeName = args[++i] || '';
      break;
    case '--format':
      format = args[++i] || 'json';
      break;
  }
}

if (!storeName) {
  process.stderr.write(
    '{"status":"error","error_type":"missing_parameter","missing":"store","suggestion":"请提供商家名称，例如 --store iHerb"}\n'
  );
  process.exit(1);
}

fxCheckAuth();

const body = { storeName };

const respText = await fxPost('skill/api/overseas/store-rebate', body, '商家查询服务暂时不可用，请稍后重试');

let resp;
try {
  resp = JSON.parse(respText);
} catch (e) {
  process.stderr.write('{"status":"error","error_type":"api_unavailable","suggestion":"响应解析失败"}\n');
  process.exit(1);
}

const data = resp.data !== undefined ? resp.data : resp;

if (resp.code === 200 && data) {
  if (format === 'table') {
    for (const [k, v] of Object.entries(data)) {
      if (v !== null && v !== '' && v !== false) {
        process.stdout.write(`${k}: ${typeof v === 'object' ? JSON.stringify(v) : v}\n`);
      }
    }
  } else {
    process.stdout.write(JSON.stringify(data, null, 2) + '\n');
  }
} else {
  const msg = resp.message || '查询失败';
  const err = (data && typeof data === 'object' && data.errorMessage) ? data.errorMessage : msg;
  process.stdout.write(
    JSON.stringify({ status: 'error', message: err, suggestion: '请检查商家名称是否正确' }, null, 2) + '\n'
  );
}
