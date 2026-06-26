#!/usr/bin/env node

/**
 * 安装 Telegram /agents_monitor 命令
 * 
 * 用法：node install.js
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

const CONFIG_PATH = join(homedir(), '.openclaw/openclaw.json');

console.log('🔧 正在安装 Telegram /agents_monitor 命令...\n');

try {
    // 读取配置
    if (!existsSync(CONFIG_PATH)) {
        console.error('❌ 错误：找不到 OpenClaw 配置文件');
        console.error(`路径：${CONFIG_PATH}`);
        process.exit(1);
    }

    const config = JSON.parse(readFileSync(CONFIG_PATH, 'utf-8'));

    // 添加命令配置
    if (!config.commands) {
        config.commands = {};
    }

    if (!config.commands.aliases) {
        config.commands.aliases = {};
    }

    // 添加 agents_monitor 别名
    config.commands.aliases['agents_monitor'] = {
        type: 'exec',
        command: '~/.openclaw/workspace/skills/agent-status-monitor/scripts/check-agents.sh',
        description: '检查本地开发 Agent 运行状态',
        streaming: false
    };

    // 写回配置
    writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2) + '\n', 'utf-8');

    console.log('✅ 安装完成！\n');
    console.log('现在可以在 Telegram 中使用：');
    console.log('  /agents_monitor - 检查 Agent 状态\n');
    console.log('⚠️  请重启 OpenClaw Gateway 使配置生效：');
    console.log('  openclaw gateway restart\n');

} catch (error) {
    console.error('❌ 安装失败:', error.message);
    process.exit(1);
}
