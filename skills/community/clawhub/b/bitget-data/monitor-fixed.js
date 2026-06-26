#!/usr/bin/env node
// Bitget 监控脚本 - 修复代理版本

const fs = require('fs');
const crypto = require('crypto');
const http = require('http');
const https = require('https');

const DATA_DIR = __dirname;
const CONFIG_FILE = DATA_DIR + '/config.json';
const SETTINGS_FILE = DATA_DIR + '/grid_settings.json';
const LOG_FILE = DATA_DIR + '/grid_monitor.log';

const CONFIG = JSON.parse(fs.readFileSync(CONFIG_FILE));
const SETTINGS = JSON.parse(fs.readFileSync(SETTINGS_FILE));

function log(message) {
    const timestamp = new Date().toLocaleString('zh-CN');
    const logLine = `[${timestamp}] ${message}\n`;
    fs.appendFileSync(LOG_FILE, logLine);
    console.log(logLine.trim());
}

function sign(message) {
    return crypto.createHmac('sha256', CONFIG.secretKey).update(message).digest('base64');
}

function request(endpoint, method = 'GET', params = {}) {
    return new Promise((resolve, reject) => {
        const timestamp = new Date().toISOString().split('.')[0] + '.000Z';
        const queryString = method === 'GET' && Object.keys(params).length > 0 
            ? '?' + new URLSearchParams(params).toString() 
            : '';
        
        const fullpath = '/api/v2' + endpoint + queryString;
        let body = '';
        if (method === 'POST') body = JSON.stringify(params);
        
        const signStr = timestamp + method + fullpath + body;
        const signature = sign(signStr);
        
        // 使用代理
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
                        const result = JSON.parse(data);
                        resolve(result.code === '00000' ? result.data : { error: result.msg });
                    } catch (e) {
                        resolve({ error: 'Parse Error', raw: data.substring(0, 200) });
                    }
                });
            });
            
            req.on('error', reject);
            if (body) req.write(body);
            req.end();
        });
        
        proxyReq.on('error', (e) => {
            reject(new Error(`Proxy Error: ${e.message}`));
        });
        proxyReq.end();
    });
}

async function getTicker(symbol) {
    try {
        const result = await request('/spot/market/tickers', 'GET', { symbol });
        if (result.error || !result[0]) return null;
        return parseFloat(result[0].lastPr || 0);
    } catch (e) {
        throw e;
    }
}

async function getOrders(symbol) {
    try {
        const result = await request('/spot/trade/unfilled-orders', 'GET', { symbol, limit: '100' });
        if (result.error) return [];
        return result;
    } catch (e) {
        return [];
    }
}

async function getBalance() {
    try {
        const result = await request('/spot/account/assets', 'GET');
        if (result.error) return [];
        return result;
    } catch (e) {
        return [];
    }
}

async function checkGrid(name, gridConfig) {
    const { symbol, gridNum } = gridConfig;
    
    log(`📊 检查 ${name} (${symbol})...`);
    
    try {
        const price = await getTicker(symbol);
        const orders = await getOrders(symbol);
        
        if (price) {
            log(`   ✅ ${symbol} 价格：${price} USDT`);
            log(`   📋 订单：${orders.length} 个`);
            
            const buys = orders.filter(o => o.side === 'buy').length;
            const sells = orders.filter(o => o.side === 'sell').length;
            log(`      买单：${buys} | 卖单：${sells}`);
            
            return { status: 'ok', price, orders: orders.length };
        } else {
            log(`   ❌ 无法获取价格`);
            return { status: 'error', reason: 'no_price' };
        }
    } catch (e) {
        log(`   ❌ 错误：${e.message}`);
        return { status: 'error', reason: e.message };
    }
}

async function main() {
    log('=' .repeat(70));
    log('🔍 Bitget 多网格策略监控');
    log('=' .repeat(70));
    
    const results = {};
    
    // 检查每个网格
    for (const gridName of Object.keys(SETTINGS)) {
        const gridConfig = SETTINGS[gridName];
        const result = await checkGrid(gridName, gridConfig);
        results[gridName] = result;
    }
    
    // 汇总
    log('\n' + '=' .repeat(70));
    log('📊 监控结果汇总');
    log('=' .repeat(70));
    
    const okCount = Object.values(results).filter(r => r.status === 'ok').length;
    const totalCount = Object.keys(results).length;
    
    if (okCount === totalCount) {
        log('✅ 所有网格策略运行正常');
    } else {
        log(`⚠️  ${okCount}/${totalCount} 个网格正常`);
        
        Object.entries(results).forEach(([name, result]) => {
            if (result.status === 'error') {
                log(`   ❌ ${name}: ${result.reason}`);
            }
        });
    }
    
    log('=' .repeat(70) + '\n');
}

main().catch(e => {
    log('❌ 监控失败：' + e.message);
    process.exit(1);
});
