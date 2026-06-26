#!/usr/bin/env node
/**
 * Binance Notify Sender - 币安通知发送器
 * 
 * 轮询通知队列，输出通知内容供外部系统调用 message 工具发送
 * 
 * 使用方式：
 * 1. 独立运行，捕获 stdout 中的 NOTIFY: 前缀
 * 2. 或集成到 OpenClaw 子 agent 中自动发送
 */

const fs = require('fs');
const path = require('path');

// 文件路径
const NOTIFY_FILE = path.join(__dirname, 'binance-pending-notify.json');
const SENT_FILE = path.join(__dirname, 'binance-sent-ids.json');

// ==================== 已发送记录 ====================
function loadSentIds() {
    try {
        if (fs.existsSync(SENT_FILE)) {
            return JSON.parse(fs.readFileSync(SENT_FILE, 'utf-8'));
        }
    } catch (e) {}
    return [];
}

function saveSentIds(ids) {
    try {
        fs.writeFileSync(SENT_FILE, JSON.stringify(ids, null, 2), 'utf-8');
    } catch (e) {}
}

// ==================== 处理通知 ====================
function processNotify() {
    try {
        if (!fs.existsSync(NOTIFY_FILE)) {
            return;
        }
        
        const content = fs.readFileSync(NOTIFY_FILE, 'utf-8').trim();
        if (!content) {
            return;
        }
        
        const notify = JSON.parse(content);
        
        // 生成唯一 ID（用时间戳 + 标题前缀）
        const id = notify.timestamp + ':' + notify.message.substring(0, 30);
        
        const sentIds = loadSentIds();
        if (sentIds.includes(id)) {
            return; // 已发送，跳过
        }
        
        // 输出通知（格式：NOTIFY:<JSON>）
        // 外部系统可以捕获这个输出并调用 message 工具
        console.log('NOTIFY:' + JSON.stringify({
            action: 'send',
            channel: notify.channel,
            target: notify.target,
            message: notify.message
        }));
        
        // 标记为已发送
        sentIds.push(id);
        saveSentIds(sentIds.slice(-100));
        
        // 清空通知文件
        fs.writeFileSync(NOTIFY_FILE, '', 'utf-8');
        
        console.log(`[发送] ${notify.message.substring(0, 50)}...`);
        
    } catch (e) {
        console.error('[错误] 处理通知失败:', e.message);
    }
}

// ==================== 启动 ====================
console.log('📨 Binance Notify Sender');
console.log('========================');
console.log(`监听文件：${NOTIFY_FILE}`);
console.log(`记录文件：${SENT_FILE}`);
console.log('========================');
console.log('按 Ctrl+C 停止\n');

// 立即处理一次
processNotify();

// 每 3 秒检查一次
setInterval(processNotify, 3000);
