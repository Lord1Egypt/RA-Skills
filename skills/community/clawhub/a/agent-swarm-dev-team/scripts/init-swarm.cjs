#!/usr/bin/env node

/**
 * Agent Swarm Dev Team - 初始化脚本
 * 
 * 功能：
 * 1. 创建必要的目录结构
 * 2. 生成脚本文件
 * 3. 设置权限
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SKILL_DIR = '/Users/xufan65/.openclaw/workspace/skills/agent-swarm-dev-team';
const CLAWDBOT_DIR = path.join(SKILL_DIR, '.clawdbot');

console.log('🤖 Agent Swarm Dev Team - 初始化\n');
console.log('========================================\n');

// 1. 创建目录结构
console.log('📁 创建目录结构...');
const dirs = [
    path.join(CLAWDBOT_DIR, 'worktrees'),
    path.join(CLAWDBOT_DIR, 'logs')
];

dirs.forEach(dir => {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
        console.log(`  ✅ ${path.relative(SKILL_DIR, dir)}`);
    } else {
        console.log(`  ⏭️  ${path.relative(SKILL_DIR, dir)} (已存在)`);
    }
});

// 2. 设置脚本权限
console.log('\n🔐 设置脚本权限...');
const scripts = [
    path.join(CLAWDBOT_DIR, 'run-agent.sh'),
    path.join(CLAWDBOT_DIR, 'check-agents.sh')
];

scripts.forEach(script => {
    if (fs.existsSync(script)) {
        fs.chmodSync(script, '755');
        console.log(`  ✅ ${path.basename(script)}`);
    } else {
        console.log(`  ⚠️  ${path.basename(script)} (不存在)`);
    }
});

// 3. 检查依赖
console.log('\n🔍 检查依赖...');
const dependencies = [
    { name: 'git', command: 'git --version' },
    { name: 'tmux', command: 'tmux -V' },
    { name: 'gh CLI', command: 'gh --version' },
    { name: 'jq', command: 'jq --version' }
];

dependencies.forEach(dep => {
    try {
        execSync(dep.command, { stdio: 'ignore' });
        console.log(`  ✅ ${dep.name}`);
    } catch (e) {
        console.log(`  ❌ ${dep.name} (未安装)`);
    }
});

// 4. 创建 README
console.log('\n📝 创建 README...');
const readme = `# Agent Swarm Dev Team

## 快速开始

### 1. 启动 Codex Agent
\`\`\`bash
./.clawdbot/run-agent.sh codex feat-custom-templates gpt-5.3-codex "Implement custom email templates"
\`\`\`

### 2. 启动 Claude Code Agent
\`\`\`bash
./.clawdbot/run-agent.sh claude fix-billing-bug claude-opus-4.5 "Fix the billing calculation bug"
\`\`\`

### 3. 监控 Agent 状态
\`\`\`bash
./.clawdbot/check-agents.sh
\`\`\`

### 4. 发送指令
\`\`\`bash
tmux send-keys -t codex-feat-custom-templates "Stop. Focus on the API layer first." Enter
\`\`\`

## Definition of Done

- ✅ PR 已创建
- ✅ 分支已同步 main
- ✅ CI 通过
- ✅ Codex Review 通过
- ✅ Claude Code Review 通过
- ✅ Gemini Review 通过
- ✅ UI 变更包含截图
`;

const readmePath = path.join(CLAWDBOT_DIR, 'README.md');
fs.writeFileSync(readmePath, readme);
console.log(`  ✅ README.md`);

console.log('\n========================================');
console.log('✅ 初始化完成！\n');
console.log('下一步:');
console.log('  1. cd /Users/xufan65/.openclaw/workspace/skills/agent-swarm-dev-team');
console.log('  2. ./.clawdbot/run-agent.sh codex <task-id> gpt-5.3-codex "<prompt>"');
console.log('');
