#!/usr/bin/env node

/**
 * Agents Monitor Telegram Command Handler
 * 
 * 当用户在 Telegram 中发送 /agents_monitor 命令时，
 * 执行检查脚本并返回结果。
 */

import { execSync } from 'child_process';
import { existsSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

const SCRIPT_PATH = join(homedir(), '.openclaw/workspace/skills/agent-status-monitor/scripts/check-agents.sh');

/**
 * 处理 /agents_monitor 命令
 * @param {Object} context - 命令上下文
 * @returns {Promise<string>} - 返回格式化的状态消息
 */
export async function handleAgentsMonitorCommand(context) {
    try {
        // 检查脚本是否存在
        if (!existsSync(SCRIPT_PATH)) {
            return `❌ 错误：找不到检测脚本\n\n路径：${SCRIPT_PATH}\n\n请确保已正确安装 agent-status-monitor 技能。`;
        }

        // 执行检测脚本
        const result = execSync(SCRIPT_PATH, {
            encoding: 'utf-8',
            timeout: 30000, // 30 秒超时
            env: { ...process.env, FORCE_COLOR: '0' } // 禁用颜色输出
        });

        // 格式化输出（去除 ANSI 颜色代码）
        const cleanOutput = result.replace(/\x1b\[[0-9;]*m/g, '');

        // 构建回复消息
        const message = `🤖 **Agent 状态报告**\n\n\`\`\`\n${cleanOutput}\`\`\``;

        return message;

    } catch (error) {
        let errorMessage = '❌ **执行错误**\n\n';
        
        if (error.code === 'ETIMEDOUT' || error.message.includes('timeout')) {
            errorMessage += '⏱️ 检测超时，请稍后重试。';
        } else if (error.status === 127) {
            errorMessage += '🔧 脚本无法执行，请检查权限。\n\n';
            errorMessage += '运行以下命令添加执行权限：\n';
            errorMessage += '`chmod +x ~/.openclaw/workspace/skills/agent-status-monitor/scripts/*.sh`';
        } else {
            errorMessage += `错误信息：${error.message}`;
        }

        return errorMessage;
    }
}

// 导出命令处理器
export default {
    commands: {
        agents_monitor: {
            handler: handleAgentsMonitorCommand,
            description: '检查本地开发 Agent（Claude Code、OpenCode 等）的运行状态',
            usage: '/agents_monitor'
        }
    }
};
