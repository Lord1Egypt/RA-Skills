#!/usr/bin/env node
/**
 * Binance X (Twitter) Monitor - 币安 X 账号动态监控
 * 
 * 监控币安英文和中文 X 账号，检测到新推文时发送通知
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// ==================== 配置 ====================
const CONFIG = {
    // X 账号列表（使用 Jina AI Reader API）
    accounts: [
        {
            id: 'binance',
            name: 'Binance 英文',
            url: 'https://r.jina.ai/twitter/binance',
            lang: 'en'
        },
        {
            id: 'binancezh',
            name: 'Binance 中文',
            url: 'https://r.jina.ai/twitter/binancezh',
            lang: 'zh'
        }
    ],
    
    // 检查间隔（毫秒）
    checkIntervalMs: 60000, // 1 分钟检查一次（X 更新频率较低）
    
    // 目标用户（飞书 open_id）
    targetUser: 'ou_c1bac9d5fa30ac354a3705a9c87993dd',
    
    // 通知渠道
    channel: 'feishu'
};

// 文件路径
const STATE_FILE = path.join(__dirname, 'binance-x-state.json');
const NOTIFY_FILE = path.join(__dirname, 'binance-x-notify.json');

// ==================== 状态管理 ====================
function loadState() {
    try {
        if (fs.existsSync(STATE_FILE)) {
            return JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8'));
        }
    } catch (e) {
        console.error('[状态] 读取失败:', e.message);
    }
    return { seenTweets: {}, lastCheck: null };
}

function saveState(state) {
    try {
        fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2), 'utf-8');
    } catch (e) {
        console.error('[状态] 保存失败:', e.message);
    }
}

// ==================== 通知队列 ====================
function queueNotification(account, content, url) {
    const notify = {
        timestamp: new Date().toISOString(),
        channel: CONFIG.channel,
        target: `user:${CONFIG.targetUser}`,
        message: `🐦 **币安 X 动态**\n\n**${account.name}**\n\n${content}\n\n👉 [查看推文](${url})`
    };
    
    fs.writeFileSync(NOTIFY_FILE, JSON.stringify(notify, null, 2), 'utf-8');
    console.log(`[通知] 已排队：${account.name} - ${content.substring(0, 30)}...`);
}

// ==================== 获取推文 ====================
function fetchTweets(account) {
    return new Promise((resolve, reject) => {
        https.get(account.url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/plain'
            }
        }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    // Jina AI 返回的是纯文本格式，需要解析
                    const tweets = parseJinaResponse(data, account);
                    resolve(tweets);
                } catch (e) {
                    reject(new Error('解析失败：' + e.message));
                }
            });
        }).on('error', (e) => {
            reject(new Error('网络请求失败：' + e.message));
        });
    });
}

// ==================== 解析 Jina AI 响应 ====================
function parseJinaResponse(text, account) {
    const tweets = [];
    const lines = text.split('\n');
    
    let currentTweet = null;
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        
        // 跳过空行和元数据
        if (!line || line.startsWith('http') || line.startsWith('Title:') || 
            line.startsWith('URL:') || line.startsWith('Published:')) {
            continue;
        }
        
        // 检测推文开头（通常包含日期或 @）
        if (line.includes('@binance') || line.match(/^\d{1,2}\/\d{1,2}\/\d{2,4}/) || 
            line.match(/^[A-Z][a-z]+ \d{1,2}/)) {
            if (currentTweet && currentTweet.content.length > 10) {
                tweets.push(currentTweet);
            }
            currentTweet = {
                id: `${account.id}-${Date.now()}-${tweets.length}`,
                content: line,
                url: `https://twitter.com/${account.id}`,
                timestamp: new Date().toISOString()
            };
        } else if (currentTweet) {
            // 继续累积推文内容
            currentTweet.content += ' ' + line;
        }
    }
    
    // 添加最后一条推文
    if (currentTweet && currentTweet.content.length > 10) {
        tweets.push(currentTweet);
    }
    
    return tweets.slice(0, 5); // 只返回最近 5 条
}

// ==================== 主检查逻辑 ====================
async function check() {
    const state = loadState();
    const now = new Date().toISOString();
    
    console.log(`\n[${now}] 开始检查 X 账号动态...`);
    
    for (const account of CONFIG.accounts) {
        try {
            console.log(`[检查] ${account.name} (@${account.id})`);
            const tweets = await fetchTweets(account);
            let newCount = 0;
            
            for (const tweet of tweets) {
                // 用内容前 50 字符作为唯一 ID
                const tweetId = `${account.id}:${tweet.content.substring(0, 50)}`;
                
                if (!state.seenTweets[tweetId]) {
                    newCount++;
                    console.log(`[新动态] ${account.name}: ${tweet.content.substring(0, 50)}...`);
                    
                    // 写入通知队列
                    queueNotification(account, tweet.content, tweet.url);
                    
                    state.seenTweets[tweetId] = now;
                }
            }
            
            if (newCount === 0) {
                console.log(`[结果] ${account.name} 无新动态`);
            } else {
                console.log(`[结果] ${account.name} 发现 ${newCount} 条新动态`);
            }
            
        } catch (e) {
            console.error(`[错误] ${account.name}: ${e.message}`);
        }
    }
    
    // 保持最近 200 条记录
    const tweetIds = Object.keys(state.seenTweets);
    if (tweetIds.length > 200) {
        tweetIds.slice(0, tweetIds.length - 200).forEach(id => {
            delete state.seenTweets[id];
        });
    }
    
    state.lastCheck = now;
    saveState(state);
}

// ==================== 启动 ====================
console.log('🐦 Binance X Monitor');
console.log('========================');
console.log(`监控账号：${CONFIG.accounts.map(a => `@${a.id}`).join(', ')}`);
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
