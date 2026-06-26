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
    run.mjs convert "<链接>"                    # 转链（含比价+历史价）
    run.mjs convert "https://click.meituan.com/t?..."  # 美团转链
    run.mjs compare-price "<链接>"              # 仅比价

  标准调用:
    run.mjs call <接口名> [参数...]              # 调用指定接口
    run.mjs call convert --help                 # 查看接口帮助

  辅助:
    run.mjs list                                # 列出所有可用接口
    run.mjs show <接口名>                       # 查看接口源码

数据流向: 商品链接会被发送到 https://api-ai-brain.fenxianglife.com 进行解析
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

  // 快捷命令：run.mjs convert "<链接>" → call convert --tpwd "<链接>"
  case 'convert': {
    const link = args[1] || '';
    if (!link) {
      process.stderr.write('错误: 请提供商品链接，例如 run.mjs convert "https://e.tb.cn/h.xxx"\n');
      process.exit(1);
    }
    const convertScript = join(_scriptDir, 'convert.mjs');
    await runScript(convertScript, ['--tpwd', link, ...args.slice(2)]);
    break;
  }

  // 快捷命令：run.mjs compare-price "<链接>" → call compare-price --productIdentifier "<链接>"
  case 'compare-price': {
    const link = args[1] || '';
    if (!link) {
      process.stderr.write('错误: 请提供商品链接，例如 run.mjs compare-price "https://e.tb.cn/h.xxx"\n');
      process.exit(1);
    }
    const cmpScript = join(_scriptDir, 'compare-price.mjs');
    await runScript(cmpScript, ['--productIdentifier', link, ...args.slice(2)]);
    break;
  }

  default:
    usage();
    break;
}
