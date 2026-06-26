#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

const SCRIPTS_DIR = path.join(__dirname, '..', 'scripts');
const CLI_PY = path.join(SCRIPTS_DIR, 'cli.py');

const args = process.argv.slice(2);

if (args.length === 0) {
    console.log(`
convert-markdown v1.0.3 - 多格式文档转换工具

用法:
  npx convert-markdown <command> [options]

命令:
  convert    转换文件或目录为 Markdown
  batch      批量转换目录

示例:
  npx convert-markdown convert --input document.pdf --output document.md
  npx convert-markdown batch --source ./docs --target ./markdown

运行 "npx convert-markdown <command> --help" 获取更多帮助
`);
    process.exit(0);
}

const python = process.platform === 'win32' ? 'python' : 'python3';

const child = spawn(python, [CLI_PY, ...args], {
    stdio: 'inherit',
    shell: false,
    windowsHide: true
});

child.on('error', (err) => {
    if (err.code === 'ENOENT') {
        console.error('错误：未找到 Python，请确保已安装 Python 并添加到 PATH');
    } else {
        console.error('错误：', err.message);
    }
    process.exit(1);
});

child.on('exit', (code) => {
    process.exit(code || 0);
});
