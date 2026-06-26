#!/usr/bin/env node

/**
 * 安装脚本 - 在用户安装skill时自动执行
 */

const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');

console.log(chalk.bold.blue('🧠 安装 Claw Memory Guardian...'));

// 获取安装路径
const skillPath = __dirname;
const workspacePath = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw/workspace');
const skillsPath = path.join(workspacePath, 'skills');

// 确保skills目录存在
fs.ensureDirSync(skillsPath);

// 复制skill文件
const targetPath = path.join(skillsPath, 'claw-memory-guardian');
if (fs.existsSync(targetPath)) {
  console.log(chalk.yellow('⚠️  检测到已安装，正在更新...'));
  fs.removeSync(targetPath);
}

fs.copySync(skillPath, targetPath);

// 创建符号链接到可执行文件
const binPath = path.join(workspacePath, 'bin');
fs.ensureDirSync(binPath);

const executablePath = path.join(binPath, 'memory-guardian');
if (fs.existsSync(executablePath)) {
  fs.removeSync(executablePath);
}

// 创建可执行脚本
const scriptContent = `#!/bin/bash
node "${path.join(targetPath, 'index.js')}" "$@"
`;

fs.writeFileSync(executablePath, scriptContent);
fs.chmodSync(executablePath, '755');

console.log(chalk.green('✅ 安装完成！'));
console.log(chalk.cyan('\n🚀 开始使用:'));
console.log('1. memory-guardian init    # 初始化记忆系统');
console.log('2. memory-guardian status  # 检查系统状态');
console.log('3. memory-guardian search  # 搜索记忆内容');
console.log('4. memory-guardian backup  # 创建完整备份');

console.log(chalk.yellow('\n📖 详细文档:'));
console.log('查看 ' + path.join(targetPath, 'SKILL.md'));

console.log(chalk.bold.green('\n🎉 记忆守护者已准备就绪！'));
console.log(chalk.gray('基于亲身教训的防丢失记忆系统，保护你的工作不被遗忘。'));