#!/usr/bin/env node

/**
 * Context Preserver CLI
 * 上下文保持器命令行工具
 */

const ctxp = require('../src/index.js');

// 当通过 bin/cli.js 执行时，需要手动调用 parseArgs
// 但由于 parseArgs 不是导出函数，我们直接执行命令行解析
const { spawn } = require('child_process');
const path = require('path');

// 转发参数到 src/index.js
const args = process.argv.slice(2);
const child = spawn('node', [path.join(__dirname, '../src/index.js'), ...args], {
  stdio: 'inherit'
});

child.on('error', (err) => {
  console.error('执行失败:', err.message);
  process.exit(1);
});

child.on('close', (code) => {
  process.exit(code);
});
