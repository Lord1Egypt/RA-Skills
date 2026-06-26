#!/usr/bin/env node
// name: order-query
// description: 查询海外返利订单列表和金额汇总

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
  process.stdout.write(`用法: order-query [选项]

选项:
  --days <天数>                    查询最近几天的订单（默认 30）
  --format json|table              输出格式（默认 json）
  --help                           显示此帮助

示例:
  order-query                      # 查询最近30天订单
  order-query --days 7             # 查询最近7天订单
  order-query --days 90 --format table

数据流向: 订单查询会被发送到 https://api-ai-brain.fenxianglife.com 进行查询
`);
  process.exit(0);
}

// ── 参数解析 ──
const args = process.argv.slice(2);
let days = 30;
let format = 'json';

for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case '--help':
    case '-h':
      help();
      break;
    case '--days':
      days = parseInt(args[++i] || '30', 10) || 30;
      break;
    case '--format':
      format = args[++i] || 'json';
      break;
  }
}

fxCheckAuth();

const body = { days };

const respText = await fxPost('skill/api/overseas/order-query', body, '订单查询服务暂时不可用，请稍后重试');

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
    // 汇总信息
    if (data.summary) {
      process.stdout.write('--- 汇总 ---\n');
      for (const [k, v] of Object.entries(data.summary)) {
        process.stdout.write(`${k}: ${v}\n`);
      }
      process.stdout.write('\n');
    }
    // 订单列表
    if (data.orders && data.orders.length > 0) {
      process.stdout.write('--- 订单列表 ---\n');
      for (const order of data.orders) {
        for (const [k, v] of Object.entries(order)) {
          if (v !== null && v !== '' && v !== false) {
            process.stdout.write(`${k}: ${v}\n`);
          }
        }
        process.stdout.write('---\n');
      }
    }
  } else {
    process.stdout.write(JSON.stringify(data, null, 2) + '\n');
  }
} else {
  const msg = resp.message || '查询失败';
  const err = (data && typeof data === 'object' && data.errorMessage) ? data.errorMessage : msg;
  process.stdout.write(
    JSON.stringify({ status: 'error', message: err, suggestion: '订单查询失败，请稍后重试' }, null, 2) + '\n'
  );
}
