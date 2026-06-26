#!/usr/bin/env node
// name: compare-price
// description: 跨平台比价，输入商品链接/淘口令，返回全网最低价 TOP3
// tags: 比价,省钱,全网最低

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
  process.stdout.write(`用法: compare-price --productIdentifier <链接> [选项]

必填:
  --productIdentifier <链接>   商品链接或淘口令

选项:
  --shopType <平台>            指定平台筛选（如 淘宝、京东）
  --format json|table          输出格式（默认 json）
  --help                       显示此帮助

示例:
  compare-price --productIdentifier "https://e.tb.cn/h.xxx"
  compare-price --productIdentifier "https://u.jd.com/xxx" --format table

数据流向: 商品链接会被发送到 https://api-ai-brain.fenxianglife.com 进行解析
`);
  process.exit(0);
}

// ── 参数解析 ──
const args = process.argv.slice(2);
let productIdentifier = '';
let shopType = '';
let format = 'json';

for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case '--help':
    case '-h':
      help();
      break;
    case '--productIdentifier':
      productIdentifier = args[++i] || '';
      break;
    case '--shopType':
      shopType = args[++i] || '';
      break;
    case '--format':
      format = args[++i] || 'json';
      break;
  }
}

if (!productIdentifier) {
  process.stderr.write(
    '{"status":"error","error_type":"missing_parameter","missing":"productIdentifier","suggestion":"请提供商品链接或淘口令，例如 --productIdentifier https://u.jd.com/xxx"}\n'
  );
  process.exit(1);
}

fxCheckAuth();

const body = { productIdentifier };
if (shopType) body.shopType = shopType;

const respText = await fxPost('skill/api/compare-price', body, '比价服务暂时不可用，请稍后重试');

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
    const total = data.totalCount || 0;
    process.stdout.write(`比价商品总数: ${total}\n`);
    const items = data.topLowestItems || [];
    if (items.length > 0) {
      process.stdout.write(`全网最低价 TOP${items.length}:\n`);
      process.stdout.write(`${'平台'.padEnd(8)} ${'店铺'.padEnd(20)} ${'价格'.padEnd(10)} 标签\n`);
      process.stdout.write('─'.repeat(60) + '\n');
      for (const item of items) {
        const shop = (item.shopName || '').slice(0, 18).padEnd(20);
        const price = String(item.price || '-').padEnd(9);
        const badge = item.badge || '';
        const shopType = (item.shopType || '').padEnd(8);
        process.stdout.write(`${shopType} ${shop} ¥${price} ${badge}\n`);
      }
    } else {
      process.stdout.write('暂无跨平台比价数据\n');
    }
  } else {
    process.stdout.write(JSON.stringify(data, null, 2) + '\n');
  }
} else {
  process.stdout.write(
    JSON.stringify({ status: 'error', message: resp.message || '比价失败' }, null, 2) + '\n'
  );
}
