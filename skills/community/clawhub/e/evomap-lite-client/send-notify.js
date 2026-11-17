#!/usr/bin/env node
/**
 * EvoMap 任务执行结果 - 飞书通知脚本
 * 用法：node send-notify.js <状态> [任务 ID] [标题] [内容] [时间戳]
 */

const { execSync } = require('child_process');
const path = require('path');

const [,, STATUS, TASK_ID, TITLE, CONTENT, TIMESTAMP] = process.argv;

// 配置
const CONFIG_FILE = path.join(__dirname, 'config.json');
let config = { feishu: { target_user: '' } };

try {
    config = require(CONFIG_FILE);
} catch (e) {
    // 配置文件不存在，使用默认值
}

// 构建消息内容
const messages = {
    'NO_TASKS': {
        emoji: '⏳',
        text: 'EvoMap 定时检查完成，当前没有可用任务。'
    },
    'SUCCESS': {
        emoji: '✅',
        text: `任务 ID: ${TASK_ID}\n已成功处理并完成任务！`
    },
    'CLAIM_FAILED': {
        emoji: '❌',
        text: `任务 ID: ${TASK_ID}\n认领任务时出错。`
    },
    'PUBLISH_FAILED': {
        emoji: '❌',
        text: `任务 ID: ${TASK_ID}\n发布解决方案时出错。`
    },
    'COMPLETE_FAILED': {
        emoji: '❌',
        text: `任务 ID: ${TASK_ID}\n完成任务时出错。`
    },
    'ERROR': {
        emoji: '⚠️',
        text: `执行过程中发生错误：${CONTENT}`
    }
};

const msg = messages[STATUS] || { emoji: '📋', text: `状态：${STATUS}` };

// 构建飞书消息
const title = `${msg.emoji} ${TITLE || STATUS}`;
const message = `${msg.text}\n\n执行时间：${TIMESTAMP || new Date().toLocaleString('zh-CN')}`;

// 构建 openclaw message 命令
const targetUser = config.feishu?.target_user;
let cmd = `openclaw message send --channel feishu --account team --message "${title}\\n\\n${message}"`;

if (targetUser) {
    // 判断 ID 格式，chat_ 开头用 chat:，ou_ 开头用 user:
    const prefix = targetUser.startsWith('cli_') ? 'chat:' : 'user:';
    cmd += ` --target "${prefix}${targetUser}"`;
}

console.log(`📤 发送飞书通知：${STATUS}`);
console.log(`📝 消息内容：${title}`);

try {
    execSync(cmd, { stdio: 'inherit' });
    console.log('✅ 通知发送成功');
} catch (error) {
    console.error('❌ 通知发送失败:', error.message);
    process.exit(1);
}
