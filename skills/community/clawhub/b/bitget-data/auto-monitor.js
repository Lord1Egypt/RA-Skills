#!/usr/bin/env node
// Bitget 高频网格自动监控系统 - 真实 API 版
// 目标：每天 60-100 笔交易，自动优化网格策略

const fs = require('fs');
const crypto = require('crypto');
const http = require('http');
const https = require('https');

// 加载配置
const CONFIG = JSON.parse(fs.readFileSync(__dirname + '/config.json'));
const SETTINGS = JSON.parse(fs.readFileSync(__dirname + '/grid_settings_standard.json'));

// 监控配置
const MONITOR_CONFIG = {
    checkIntervalMs: 30 * 60 * 1000,  // 30 分钟检查一次
    targetTradesPerHour: null,        // 不设目标限制
    minTradesPerHour: null,           // 不设最低限制
    maxTradesPerHour: null,           // 不设最高限制 - 无限制模式
    autoAdjustEnabled: false,         // 禁用自动调整 (无限制模式下不需要)
    reportTime: '21:00',              // 每日报告时间
};

// 状态文件
const STATE_FILE = __dirname + '/monitor_state.json';
const DAILY_REPORT_FILE = __dirname + '/daily_report.md';
const LOG_FILE = __dirname + '/auto_monitor.log';

// 日志
function log(message, level = 'INFO') {
    const timestamp = new Date().toLocaleString('zh-CN');
    const logLine = `[${timestamp}] [${level}] ${message}`;
    console.log(logLine);
    fs.appendFileSync(LOG_FILE, logLine + '\n');
}

// API 签名
function sign(message) {
    return crypto.createHmac('sha256', CONFIG.secretKey).update(message).digest('base64');
}

// API 请求（使用代理）
function request(endpoint, method = 'GET', params = {}, body = null) {
    return new Promise((resolve) => {
        const timestamp = new Date().toISOString().split('.')[0] + '.000Z';
        let queryString = '';
        if (method === 'GET' && Object.keys(params).length > 0) {
            queryString = '?' + new URLSearchParams(params);
        }
        
        const fullpath = '/api/v2' + endpoint + queryString;
        let bodyStr = '';
        if (method === 'POST' && body) {
            bodyStr = typeof body === 'string' ? body : JSON.stringify(body);
        }
        
        const signStr = timestamp + method + fullpath + bodyStr;
        const signature = sign(signStr);
        
        const proxyOptions = {
            hostname: '127.0.0.1',
            port: 7897,
            path: 'api.bitget.com:443',
            method: 'CONNECT'
        };
        
        const proxyReq = http.request(proxyOptions);
        proxyReq.on('connect', (res, socket) => {
            const options = {
                socket: socket,
                hostname: 'api.bitget.com',
                port: 443,
                path: fullpath,
                method: method,
                headers: {
                    'ACCESS-KEY': CONFIG.apiKey,
                    'ACCESS-SIGN': signature,
                    'ACCESS-TIMESTAMP': timestamp,
                    'ACCESS-PASSPHRASE': CONFIG.passphrase,
                    'Content-Type': 'application/json'
                }
            };
            
            const req = https.request(options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        resolve(JSON.parse(data));
                    } catch (e) {
                        resolve({error: e.message, rawData: data.substring(0, 200)});
                    }
                });
            });
            
            req.on('error', e => resolve({error: e.message}));
            if (bodyStr) req.write(bodyStr);
            req.end();
        });
        
        proxyReq.on('error', e => resolve({error: e.message}));
        proxyReq.end();
    });
}

// 加载状态
function loadState() {
    if (fs.existsSync(STATE_FILE)) {
        return JSON.parse(fs.readFileSync(STATE_FILE));
    }
    return {
        lastCheck: null,
        todayTrades: 0,
        todayBuys: 0,
        todaySells: 0,
        lastCheckTrades: 0,
        lastAdjustment: null,
        startTime: new Date().toISOString(),
        coinTrades: { btc: 0, sol: 0, eth: 0, avax: 0 },
        lastCoinTradeIds: { btc: [], sol: [], eth: [], avax: [] }
    };
}

// 保存状态
function saveState(state) {
    fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

// 获取成交数据（最近 100 笔，过滤出 startTime 之后的）
async function getFilledOrders(symbol, startTime) {
    const result = await request('/spot/trade/fills', 'GET', { 
        symbol, 
        limit: '100'
    });
    
    if (result.code !== '00000' || !result.data) {
        log(`   API 返回错误：${result.code} - ${result.msg}`, 'WARN');
        return [];
    }
    
    const startTimeMs = new Date(startTime).getTime();
    const filtered = result.data.filter(fill => {
        const fillTime = Number(fill.cTime);
        return fillTime >= startTimeMs;
    });
    
    log(`   ${symbol}: API 返回${result.data.length}笔，过滤后${filtered.length}笔`);
    return filtered;
}

// 检查成交情况
async function checkTrades(state) {
    log('🔍 检查成交情况...');
    
    const coins = ['btc', 'sol', 'eth']; // AVAX 已取消
    const results = {};
    let totalTrades = 0;
    
    // 获取上次各币种成交 ID 用于去重
    const lastCoinTradeIds = state.lastCoinTradeIds || { btc: [], sol: [], eth: [], avax: [] };
    const newCoinTradeIds = { btc: [], sol: [], eth: [], avax: [] };
    
    for (const coin of coins) {
        // 检查是否启用
        if (SETTINGS[coin].enabled === false) {
            log(`   ⏭️  跳过 ${coin.toUpperCase()} - 已禁用`);
            results[coin] = { trades: 0, buys: 0, sells: 0 };
            continue;
        }
        
        const symbol = SETTINGS[coin].symbol;
        const fills = await getFilledOrders(symbol, state.startTime);
        
        // 过滤出新成交（不在上次记录中的）
        const newFills = fills.filter(f => !lastCoinTradeIds[coin].includes(f.tradeId));
        
        const buys = newFills.filter(f => f.side === 'buy').length;
        const sells = newFills.filter(f => f.side === 'sell').length;
        const trades = buys + sells;
        
        // 保存最近的成交 ID（最多 50 个）
        newCoinTradeIds[coin] = fills.slice(0, 50).map(f => f.tradeId);
        
        results[coin] = { trades, buys, sells };
        totalTrades += trades;
        
        log(`   ${coin.toUpperCase()}: ${trades} 笔 (买${buys}/卖${sells})`);
    }
    
    log(`📊 本次检查新增成交：${totalTrades} 笔`);
    
    // 更新状态
    state.lastCoinTradeIds = newCoinTradeIds;
    
    return { coins: results, total: totalTrades };
}

// 评估是否需要调整
function evaluatePerformance(state, checkResult) {
    const now = new Date();
    const startTime = new Date(state.startTime);
    const hoursElapsed = (now - startTime) / (1000 * 60 * 60);
    
    // 计算本次检查的增量成交
    const incrementTrades = checkResult.total; // 这是本次检查新增的成交
    
    // 计算平均小时成交率（基于总运行时间）
    const totalTrades = state.todayTrades + incrementTrades;
    const avgTradesPerHour = totalTrades / hoursElapsed;
    
    // 计算本次检查间隔的成交率（如果有多次检查）
    let intervalTradesPerHour = avgTradesPerHour;
    if (state.lastCheck) {
        const lastCheckTime = new Date(state.lastCheck);
        const intervalHours = (now - lastCheckTime) / (1000 * 60 * 60);
        if (intervalHours > 0) {
            intervalTradesPerHour = incrementTrades / intervalHours;
        }
    }
    
    log(`📈 性能评估:`);
    log(`   运行时长：${hoursElapsed.toFixed(1)} 小时`);
    log(`   本次新增：${incrementTrades} 笔`);
    log(`   累计成交：${totalTrades} 笔`);
    log(`   平均频率：${avgTradesPerHour.toFixed(2)} 笔/小时`);
    
    if (hoursElapsed < 0.5) {
        log('⏳ 运行时间不足 30 分钟，暂不评估');
        return { needsAdjustment: false, reason: '运行时间短' };
    }
    
    // 基于平均频率评估 (无限制模式下跳过)
    if (MONITOR_CONFIG.minTradesPerHour === null || MONITOR_CONFIG.maxTradesPerHour === null) {
        log(`✅ 无限制模式 - 当前频率：${avgTradesPerHour.toFixed(1)} 笔/小时 (不自动调整)`);
        return { needsAdjustment: false, reason: '无限制模式' };
    }
    
    if (avgTradesPerHour < MONITOR_CONFIG.minTradesPerHour) {
        log(`⚠️  成交过少 (${avgTradesPerHour.toFixed(1)} < ${MONITOR_CONFIG.minTradesPerHour})，需要加密网格`);
        return { needsAdjustment: true, action: 'increase_density', reason: '成交不足' };
    } else if (avgTradesPerHour > MONITOR_CONFIG.maxTradesPerHour) {
        log(`⚠️  成交过多 (${avgTradesPerHour.toFixed(1)} > ${MONITOR_CONFIG.maxTradesPerHour})，需要降低密度`);
        return { needsAdjustment: true, action: 'decrease_density', reason: '成交过多' };
    } else {
        log(`✅ 成交频率正常 (${avgTradesPerHour.toFixed(1)} 笔/小时)`);
        return { needsAdjustment: false, reason: '正常范围' };
    }
}

// 主循环
async function main() {
    log('\n' + '='.repeat(70));
    log('🤖 Bitget 高频网格自动监控系统启动');
    log('='.repeat(70));
    
    const state = loadState();
    log(`📁 加载状态：今日成交 ${state.todayTrades} 笔，启动时间 ${state.startTime}`);
    
    // 检查成交
    const checkResult = await checkTrades(state);
    
    // 评估性能
    const evaluation = evaluatePerformance(state, checkResult);
    
    // 更新状态
    state.lastCheck = new Date().toISOString();
    state.todayTrades += checkResult.total; // 累加增量成交
    state.coinTrades = checkResult.coins;
    
    if (evaluation.needsAdjustment && MONITOR_CONFIG.autoAdjustEnabled) {
        log(`\n🔧 需要调整：${evaluation.action} - ${evaluation.reason}`);
        state.lastAdjustment = new Date().toISOString();
        // 这里可以调用调整脚本
    } else {
        log(`\n✅ 无需调整：${evaluation.reason}`);
    }
    
    saveState(state);
    log(`💾 状态已保存 (累计成交：${state.todayTrades} 笔)`);
    
    log('\n' + '='.repeat(70));
    log('✅ 监控检查完成');
    log('='.repeat(70) + '\n');
}

// 运行
main().catch(err => {
    log(`❌ 错误：${err.message}`, 'ERROR');
    process.exit(1);
});
