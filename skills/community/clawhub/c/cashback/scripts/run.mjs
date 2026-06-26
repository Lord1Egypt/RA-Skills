#!/usr/bin/env node
// 统一执行引擎：调度脚本，支持快捷命令和标准调用

import { fileURLToPath } from 'url';
import { join, dirname } from 'path';
import { readdirSync, readFileSync, existsSync } from 'fs';
import { spawn } from 'child_process';

const _scriptDir = dirname(fileURLToPath(import.meta.url));

function usage() {
  process.stdout.write(`用法:
  快捷命令（推荐）:
    run.mjs convert "<海外商品链接>"          # 链接转返利短链
    run.mjs store "<商家名>"                 # 查商家返利
    run.mjs orders                           # 查返利订单（默认30天）
    run.mjs orders --days 7                  # 查最近7天订单

  标准调用:
    run.mjs call <接口名> [参数...]            # 调用指定接口
    run.mjs call link-convert --help          # 查看接口帮助

  辅助:
    run.mjs list                              # 列出所有可用接口
    run.mjs show <接口名>                     # 查看接口源码

数据流向: 链接和查询会被发送到 https://api-ai-brain.fenxianglife.com 进行处理
`);
}

function runScript(scriptPath, args) {
  return new Promise((_resolve, reject) => {
    const child = spawn(process.execPath, [scriptPath, ...args], {
      stdio: 'inherit',
      env: process.env,
    });
    child.on('close', (code) => {
      process.exit(code ?? 0);
    });
    child.on('error', reject);
  });
}

const args = process.argv.slice(2);
const cmd = args[0] || '';

switch (cmd) {
  case '--help':
  case '-h':
    usage();
    break;

  case 'list': {
    process.stdout.write('可用接口：\n');
    const files = readdirSync(_scriptDir)
      .filter(f => f.endsWith('.mjs') && f !== 'run.mjs')
      .sort();
    if (files.length === 0) {
      process.stdout.write('  (暂无接口)\n');
      break;
    }
    const rows = files.map(f => {
      const name = f.replace(/\.mjs$/, '');
      let desc = '';
      const content = readFileSync(join(_scriptDir, f), 'utf8');
      const m = content.match(/^\/\/\s*description:\s*(.+)/m);
      if (m) desc = m[1].trim();
      return [name, desc];
    });
    const w0 = Math.max(...rows.map(r => r[0].length));
    for (const [name, desc] of rows) {
      process.stdout.write(`  ${name.padEnd(w0)}  ${desc}\n`);
    }
    break;
  }

  case 'show': {
    const name = args[1] || '';
    if (!name) {
      process.stderr.write('错误: 请指定接口名\n');
      process.exit(1);
    }
    const mjsFile = join(_scriptDir, `${name}.mjs`);
    if (!existsSync(mjsFile)) {
      process.stderr.write(`错误: 接口 '${name}' 不存在\n`);
      process.exit(1);
    }
    process.stdout.write(readFileSync(mjsFile, 'utf8'));
    break;
  }

  case 'call': {
    const name = args[1] || '';
    if (!name) {
      process.stderr.write('错误: 请指定接口名\n');
      process.exit(1);
    }
    const mjsFile = join(_scriptDir, `${name}.mjs`);
    if (!existsSync(mjsFile)) {
      process.stderr.write(`错误: 接口 '${name}' 不存在，运行 'node run.mjs list' 查看可用接口\n`);
      process.exit(1);
    }
    await runScript(mjsFile, args.slice(2));
    break;
  }

  // 快捷命令：run.mjs convert "<链接>" → call link-convert --url "<链接>"
  case 'convert': {
    const url = args[1] || '';
    if (!url) {
      process.stderr.write('错误: 请提供海外商品链接，例如 run.mjs convert "https://www.amazon.com/dp/B0xxxxx"\n');
      process.exit(1);
    }
    const script = join(_scriptDir, 'link-convert.mjs');
    await runScript(script, ['--url', url, ...args.slice(2)]);
    break;
  }

  // 快捷命令：run.mjs store "<商家名>" → call store-rebate --store "<商家名>"
  case 'store': {
    const store = args[1] || '';
    if (!store) {
      process.stderr.write('错误: 请提供商家名称，例如 run.mjs store "iHerb"\n');
      process.exit(1);
    }
    const script = join(_scriptDir, 'store-rebate.mjs');
    await runScript(script, ['--store', store, ...args.slice(2)]);
    break;
  }

  // 快捷命令：run.mjs orders [--days N] → call order-query [--days N]
  case 'orders': {
    const script = join(_scriptDir, 'order-query.mjs');
    await runScript(script, args.slice(1));
    break;
  }

  default:
    usage();
    break;
}
