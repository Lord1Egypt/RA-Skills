#!/usr/bin/env node
/**
 * Binance Announce Monitor - 币安公告监控
 * 
 * 实时监控币安官方公告，检测到新公告时写入通知队列
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// ==================== 配置 ====================
const CONFIG = {
    // 币安公告 API
    announceUrl: 'https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&pageNo=1&pageSize=5&catalogId=48',
    
    // 检查间隔（毫秒）
    checkIntervalMs: 30000,
    
    // 目标用户（飞书 open_id）
    targetUser: 'ou_c1bac9d5fa30ac354a3705a9c87993dd',
    
    // 通知渠道
    channel: 'feishu'
};

// 文件路径
const STATE_FILE = path.join(__dirname, 'binance-announce-state.json');
const NOTIFY_FILE = path.join(__dirname, 'binance-pending-notify.json');

// ==================== 状态管理 ====================
function loadState() {
    try {
        if (fs.existsSync(STATE_FILE)) {
            return JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8'));
        }
    } catch (e) {
        console.error('[状态] 读取失败:', e.message);
    }
    return { seenIds: [], lastCheck: null };
}

function saveState(state) {
    try {
        fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2), 'utf-8');
    } catch (e) {
        console.error('[状态] 保存失败:', e.message);
    }
}

// ==================== 通知队列 ====================
function queueNotification(title, summary, url) {
    const notify = {
        timestamp: new Date().toISOString(),
        channel: CONFIG.channel,
        target: `user:${CONFIG.targetUser}`,
        message: `📢 **币安新公告**\n\n**${title}**\n\n${summary}\n\n👉 [查看详情](${url})`
    };
    
    fs.writeFileSync(NOTIFY_FILE, JSON.stringify(notify, null, 2), 'utf-8');
    console.log(`[通知] 已排队：${title.substring(0, 30)}...`);
}

// ==================== 获取公告 ====================
function fetchAnnouncements() {
    return new Promise((resolve, reject) => {
        https.get(CONFIG.announceUrl, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json'
            }
        }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const json = JSON.parse(data);
                    const articles = json.data?.catalogs?.[0]?.articles || [];
                    resolve(articles);
                } catch (e) {
                    reject(new Error('JSON 解析失败：' + e.message));
                }
            });
        }).on('error', (e) => {
            reject(new Error('网络请求失败：' + e.message));
        });
    });
}

// ==================== 主检查逻辑 ====================
async function check() {
    const state = loadState();
    const now = new Date().toISOString();
    
    try {
        console.log(`\n[${now}] 开始检查...`);
        const articles = await fetchAnnouncements();
        let newCount = 0;
        
        for (const article of articles) {
            const id = article.id;
            const title = article.title;
            const summary = article.summary || '';
            const url = `https://www.binance.com/en/support/announcement/${id}`;
            
            if (!state.seenIds.includes(id)) {
                newCount++;
                console.log(`[新公告] ${title}`);
                
                // 写入通知队列
                queueNotification(title, summary, url);
                
                state.seenIds.unshift(id);
            }
        }
        
        // 保持最近 100 条记录
        state.seenIds = state.seenIds.slice(0, 100);
        state.lastCheck = now;
        saveState(state);
        
        if (newCount === 0) {
            console.log('[结果] 无新公告');
        } else {
            console.log(`[结果] 发现 ${newCount} 条新公告`);
        }
        
    } catch (e) {
        console.error(`[错误] ${e.message}`);
    }
}

// ==================== 启动 ====================
console.log('🚀 Binance Announce Monitor');
console.log('========================');
console.log(`检查间隔：${CONFIG.checkIntervalMs / 1000}秒`);
console.log(`通知渠道：${CONFIG.channel}`);
console.log(`目标用户：${CONFIG.targetUser}`);
console.log(`状态文件：${STATE_FILE}`);
console.log(`通知文件：${NOTIFY_FILE}`);
console.log('========================');
console.log('按 Ctrl+C 停止\n');

// 立即检查一次
check();

// 定时检查
setInterval(check, CONFIG.checkIntervalMs);
