#!/usr/bin/env node
/**
 * Qwen 方言语音识别 - 打包脚本
 * 用于将 Skill 打包为 zip 文件，供手动上传到 ClawHub
 * 
 * 使用方法：
 * node package.js
 * 
 * 生成的 package 将上传到 ClawHub（需要先运行 clawhub login）
 */

// 此脚本不包含任何硬编码的凭证信息
// 用户需要先运行 `clawhub login` 或 `clawhub login --token <your-token>` 来认证

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 检查技能目录
const skillDir = path.join(__dirname, 'skills', 'qwen-asr-skill');

if (!fs.existsSync(skillDir)) {
    console.error('❌ 错误：技能目录不存在:', skillDir);
    console.error('请确保 SKILL.md 文件存在于:', skillDir);
    process.exit(1);
}

// 检查必要的文件
const requiredFiles = ['SKILL.md', 'index.js', 'package.json'];
for (const file of requiredFiles) {
    if (!fs.existsSync(path.join(skillDir, file))) {
        console.error('❌ 错误：缺少必需文件:', file);
        process.exit(1);
    }
}

console.log('✅ 技能验证通过');
console.log('📁 技能目录:', skillDir);
console.log('\n📋 下一步操作：');
console.log('1. 运行 `clawhub login` 进行认证');
console.log('2. 运行 `clawhub sync --all` 或 `clawhub publish . --slug qwen-asr-skill`');
console.log('\nℹ️  详见 README.md 中的 "快速开始" 章节');