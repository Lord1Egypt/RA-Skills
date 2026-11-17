#!/usr/bin/env node

const { spawnSync } = require('child_process');
const path = require('path');

// 获取脚本目录
const scriptDir = path.resolve(__dirname);
const pythonScript = path.join(scriptDir, 'bilibili_skill.py');

// 构建命令参数
const args = process.argv.slice(2);
const pythonArgs = [pythonScript, ...args];

// 执行 Python 脚本
const result = spawnSync('python3', pythonArgs, {
  encoding: 'utf8',
  stdio: ['pipe', 'pipe', 'pipe']
});

// 输出结果
if (result.stdout) {
  process.stdout.write(result.stdout);
}

if (result.stderr) {
  process.stderr.write(result.stderr);
}

// 退出码
process.exit(result.status || 0);
