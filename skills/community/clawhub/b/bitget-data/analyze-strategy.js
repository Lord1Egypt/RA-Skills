#!/usr/bin/env node
// 分析当前网格策略并优化

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const DATA_DIR = __dirname;
const CONFIG_FILE = path.join(DATA_DIR, 'config.json');
const SETTINGS_FILE = path.join(DATA_DIR, 'grid_settings.json');

function loadJson(file) {
    try {
        return JSON.parse(fs.readFileSync(file, 'utf8'));
    } catch (e) {
        return null;
    }
}

function sign(message, secret) {
    return crypto.createHmac('sha256', secret).update(message).digest('base64');
}

function request(endpoint, method = 'GET', params = {}) {
    return new Promise((resolve, reject) => {
        const config = loadJson(CONFIG_FILE);
        if (!config) {
            resolve({ error: '配置文件不存在' });
            return;
        }

        const timestamp = Date.now().toString();
        const queryString = Object.keys(params).length > 0 ? '?' + new URLSearchParams(params).toString() : '';
        const pathWithQuery = endpoint + queryString;
        
        const signStr = timestamp + method + pathWithQuery;
        const signature = sign(signStr, config.secretKey);

        const proxyOptions = {
            hostname: '127.0.0.1',
            port: 7897,
            path: `api.bitget.com:443`,
            method: 'CONNECT',
            headers: { 'Host': 'api.bitget.com:443' }
        };

        const proxyReq = http.request(proxyOptions);
        
        proxyReq.on('connect', (res, socket, head) => {
            const options = {
                socket: socket,
                hostname: 'api.bitget.com',
                port: 443,
                path: pathWithQuery,
                method: method,
                headers: {
                    'ACCESS-KEY': config.apiKey,
                    'ACCESS-SIGN': signature,
                    'ACCESS-TIMESTAMP': timestamp,
                    'ACCESS-PASSPHRASE': config.passphrase,
                    'Content-Type': 'application/json',
                    'Host': 'api.bitget.com'
                },
                rejectUnauthorized: false
            };

            const req = https.request(options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        const result = JSON.parse(data);
                        resolve(result);
                    } catch (e) {
                        resolve({ error: '解析失败', raw: data });
                    }
                });
            });

            req.on('error', reject);
            
            if (method === 'POST' && Object.keys(params).length > 0) {
                req.write(JSON.stringify(params));
            }
            
            req.end();
        });

        proxyReq.on('error', reject);
        proxyReq.end();
    });
}

async function getMarketData(symbol) {
    const result = await request('/api/v2/spot/market/tickers', 'GET', { symbol });
    if (result.data && result.data[0]) {
        return result.data[0];
    }
    return null;
}

async function getOpenOrders(symbol) {
    const result = await request('/api/v2/spot/trade/unfilled-orders', 'GET', { symbol, limit: 100 });
    if (result.data) {
        return result.data;
    }
    return [];
}

async function cancelOrders(symbol) {
    const result = await request('/api/v2/spot/trade/cancel-symbol-orders', 'POST', { symbol });
    return result;
}

async function analyzeAndOptimize() {
    console.log('📊 分析网格策略并优化...\n');
    
    const settings = loadJson(SETTINGS_FILE);
    if (!settings) {
        console.log('❌ 配置文件不存在');
        return;
    }
    
    for (const [key, config] of Object.entries(settings)) {
        console.log(`\n${'='.repeat(50)}`);
        console.log(`分析 ${config.symbol}...`);
        console.log('='.repeat(50));
        
        // 获取市场数据
        const market = await getMarketData(config.symbol);
        if (!market) {
            console.log('❌ 无法获取市场数据');
            continue;
        }
        
        const currentPrice = parseFloat(market.lastPr);
        const high24h = parseFloat(market.high24h);
        const low24h = parseFloat(market.low24h);
        const change24h = parseFloat(market.change24h) * 100;
        
        console.log(`\n📈 市场数据:`);
        console.log(`   当前价：${currentPrice}`);
        console.log(`   24h 最高：${high24h}`);
        console.log(`   24h 最低：${low24h}`);
        console.log(`   24h 涨跌：${change24h.toFixed(2)}%`);
        
        // 当前网格配置
        console.log(`\n⚙️ 当前网格:`);
        console.log(`   区间：${config.priceMin} - ${config.priceMax}`);
        console.log(`   网格数：${config.gridNum}`);
        console.log(`   网格间距：${((config.priceMax - config.priceMin) / config.gridNum).toFixed(2)}`);
        
        // 分析价格位置
        const rangePercent = ((currentPrice - config.priceMin) / (config.priceMax - config.priceMin) * 100).toFixed(1);
        console.log(`\n📍 价格位置：${rangePercent}% (从区间底部计算)`);
        
        // 获取挂单
        const orders = await getOpenOrders(config.symbol);
        const buyOrders = orders.filter(o => o.side === 'buy');
        const sellOrders = orders.filter(o => o.side === 'sell');
        
        console.log(`\n📋 挂单情况:`);
        console.log(`   总挂单：${orders.length}`);
        console.log(`   买单：${buyOrders.length}`);
        console.log(`   卖单：${sellOrders.length}`);
        
        // 优化建议
        console.log(`\n💡 优化建议:`);
        
        // 检查区间是否合理
        const bufferPercent = 0.15; // 15% 缓冲
        const suggestedMin = low24h * (1 - bufferPercent);
        const suggestedMax = high24h * (1 + bufferPercent);
        
        if (config.priceMin > suggestedMin || config.priceMax < suggestedMax) {
            console.log(`   ⚠️ 区间可能过窄`);
            console.log(`      建议：${suggestedMin.toFixed(0)} - ${suggestedMax.toFixed(0)}`);
        } else {
            console.log(`   ✅ 区间合理`);
        }
        
        // 检查网格密度
        const gridStep = (config.priceMax - config.priceMin) / config.gridNum;
        const volatility = (high24h - low24h) / low24h * 100;
        
        if (gridStep < volatility) {
            console.log(`   ✅ 网格密度适合当前波动 (${volatility.toFixed(1)}%)`);
        } else {
            console.log(`   ⚠️ 网格可能过密，考虑减少网格数`);
        }
        
        // 检查挂单分布
        if (buyOrders.length < 5) {
            console.log(`   ⚠️ 买单较少，可能错过低吸机会`);
        }
        if (sellOrders.length < 5) {
            console.log(`   ⚠️ 卖单较少，可能错过高抛机会`);
        }
        
        if (buyOrders.length >= 5 && sellOrders.length >= 5) {
            console.log(`   ✅ 挂单分布良好`);
        }
    }
    
    console.log(`\n${'='.repeat(50)}`);
    console.log('分析完成！');
    console.log('='.repeat(50));
}

analyzeAndOptimize().catch(e => {
    console.error('错误:', e.message);
});
