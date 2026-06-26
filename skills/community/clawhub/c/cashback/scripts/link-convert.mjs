#!/usr/bin/env node
// name: link-convert
// description: 海外商品链接转返利短链，返回佣金信息和推广链接

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
  process.stdout.write(`用法: link-convert --url <海外商品链接> [选项]

必填:
  --url <链接>                    海外商品链接（Amazon/Nike/iHerb/adidas 等）

选项:
  --format json|table              输出格式（默认 json）
  --help                           显示此帮助

示例:
  link-convert --url "https://www.amazon.com/dp/B0xxxxx"
  link-convert --url "https://www.nike.com/t/air-max-90-mens-shoes-xxx"
  link-convert --url "https://www.iherb.com/pr/xxx" --format table

数据流向: 商品链接会被发送到 https://api-ai-brain.fenxianglife.com 进行转链
`);
  process.exit(0);
}

// ── 参数解析 ──
const args = process.argv.slice(2);
let url = '';
let format = 'json';

for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case '--help':
    case '-h':
      help();
      break;
    case '--url':
      url = args[++i] || '';
      break;
    case '--format':
      format = args[++i] || 'json';
      break;
  }
}

if (!url) {
  process.stderr.write(
    '{"status":"error","error_type":"missing_parameter","missing":"url","suggestion":"请提供海外商品链接，例如 --url https://www.amazon.com/dp/B0xxxxx"}\n'
  );
  process.exit(1);
}

fxCheckAuth();

const body = { url };

const respText = await fxPost('skill/api/overseas/link-convert', body, '转链服务暂时不可用，请稍后重试');

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
  const msg = resp.message || '转链失败';
  const err = (data && typeof data === 'object' && data.errorMessage) ? data.errorMessage : msg;
  process.stdout.write(
    JSON.stringify({ status: 'error', message: err, suggestion: '请检查链接是否正确，确认是海外商家链接' }, null, 2) + '\n'
  );
}
