#!/usr/bin/env node
// 动态网格调仓系统 - 根据量化指标自动调整

const fs = require('fs');
const crypto = require('crypto');
const http = require('http');
const https = require('https');

const DATA_DIR = __dirname;
const CONFIG_FILE = DATA_DIR + '/config.json';
const SETTINGS_FILE = DATA_DIR + '/grid_settings.json';
const CONFIG = JSON.parse(fs.readFileSync(CONFIG_FILE));

function sign(message) {
    return crypto.createHmac('sha256', CONFIG.secretKey).update(message).digest('base64');
}

function request(endpoint, method = 'GET', params = {}) {
    return new Promise((resolve, reject) => {
        const timestamp = Date.now().toString();
        let body = '';
        if (method === 'POST') body = JSON.stringify(params);
        
        const signStr = timestamp + method + endpoint + body;
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
                path: endpoint + (method === 'GET' && Object.keys(params).length ? '?' + new URLSearchParams(params) : ''),
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
                    try { resolve(JSON.parse(data)); }
                    catch (e) { resolve({ raw: data }); }
                });
            });
            
            req.on('error', reject);
            if (method === 'POST' && body) req.write(body);
            req.end();
        });
        
        proxyReq.on('error', reject);
        proxyReq.end();
    });
}

// 计算 RSI
function calculateRSI(prices, period = 14) {
    if (prices.length < period + 1) return 50;
    
    let gains = 0, losses = 0;
    for (let i = prices.length - period; i < prices.length; i++) {
        const change = prices[i] - prices[i-1];
        if (change > 0) gains += change;
        else losses -= change;
    }
    
    const avgGain = gains / period;
    const avgLoss = losses / period;
    
    if (avgLoss === 0) return 100;
    const rs = avgGain / avgLoss;
    return 100 - (100 / (1 + rs));
}

// 获取 K 线数据
async function getKlines(symbol, granularity = '15min', limit = 100) {
    const result = await request('/api/v2/spot/market/candles', 'GET', {
        symbol,
        granularity,
        limit: limit.toString()
    });
    return result.data || [];
}

// 获取当前挂单
async function getOpenOrders(symbol) {
    const result = await request('/api/v2/spot/trade/unfilled-orders', 'GET', {
        symbol,
        limit: '100'
    });
    return result.data || [];
}

// 撤销所有挂单
async function cancelAllOrders(symbol) {
    const result = await request('/api/v2/spot/trade/cancel-symbol-orders', 'POST', { symbol });
    return result;
}

// 下单
async function placeOrder(symbol, side, price, size) {
    const params = {
        symbol,
        side,
        orderType: 'limit',
        price: price.toFixed(side === 'buy' ? 1 : 2),
        size: size.toFixed(6),
        force: 'GTC'
    };
    
    const result = await request('/api/v2/spot/trade/place-order', 'POST', params);
    return result;
}

// 动态调整策略
async function rebalance(symbol, settings) {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`🔄 动态调仓：${symbol}`);
    console.log('='.repeat(60));
    
    // 1. 获取市场数据
    const market = await request('/api/v2/spot/market/tickers', 'GET', { symbol });
    if (!market.data || !market.data[0]) {
        console.log('❌ 无法获取市场数据');
        return;
    }
    
    const currentPrice = parseFloat(market.data[0].lastPr);
    console.log(`\n📊 当前价格：${currentPrice}`);
    
    // 2. 获取 K 线并计算指标
    const klines = await getKlines(symbol, '15m', 50);
    if (klines.length < 20) {
        console.log('⚠️ K 线数据不足');
        return;
    }
    
    const closes = klines.map(k => parseFloat(k[4])).reverse();
    const rsi = calculateRSI(closes, 14);
    
    console.log(`\n📈 技术指标:`);
    console.log(`   RSI(14): ${rsi.toFixed(1)}`);
    
    // 3. 根据 RSI 调整策略
    let adjustmentFactor = 1.0;
    let strategy = '标准网格';
    
    if (rsi < 30) {
        adjustmentFactor = 1.5; // 增加买单
        strategy = '激进买入 (RSI 超卖)';
    } else if (rsi > 70) {
        adjustmentFactor = 0.7; // 减少买单，增加卖单
        strategy = '保守卖出 (RSI 超买)';
    } else if (rsi < 40) {
        adjustmentFactor = 1.2;
        strategy = '偏多网格';
    } else if (rsi > 60) {
        adjustmentFactor = 0.85;
        strategy = '偏空网格';
    }
    
    console.log(`\n🎯 调整策略：${strategy}`);
    console.log(`   调整系数：${adjustmentFactor.toFixed(2)}`);
    
    // 4. 获取当前挂单
    const orders = await getOpenOrders(symbol);
    const buyOrders = orders.filter(o => o.side === 'buy');
    const sellOrders = orders.filter(o => o.side === 'sell');
    
    console.log(`\n📋 当前挂单:`);
    console.log(`   买单：${buyOrders.length} | 卖单：${sellOrders.length}`);
    
    // 5. 判断是否需要调整
    const targetBuyRatio = rsi < 50 ? 0.6 : 0.4;
    const currentBuyRatio = buyOrders.length / (orders.length || 1);
    const ratioDiff = Math.abs(currentBuyRatio - targetBuyRatio);
    
    console.log(`\n📊 挂单比例:`);
    console.log(`   当前买单比例：${(currentBuyRatio * 100).toFixed(0)}%`);
    console.log(`   目标买单比例：${(targetBuyRatio * 100).toFixed(0)}%`);
    
    if (ratioDiff < 0.15) {
        console.log(`\n✅ 挂单比例合理，无需调整`);
        return;
    }
    
    // 6. 执行调整
    console.log(`\n🔄 开始调整挂单...`);
    
    // 撤销所有挂单
    const cancelResult = await cancelAllOrders(symbol);
    if (cancelResult.code !== '00000') {
        console.log(`⚠️ 撤销结果：${cancelResult.msg}`);
    } else {
        console.log(`   ✅ 已撤销所有挂单`);
    }
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 重新挂单
    const { priceMin, priceMax, gridNum, totalUSDT } = settings;
    const gridStep = (priceMax - priceMin) / gridNum;
    const perGridUSDT = totalUSDT / gridNum;
    
    let placedBuy = 0, placedSell = 0;
    
    // 放置买单
    for (let i = 0; i < gridNum / 2; i++) {
        const buyPrice = currentPrice - (i + 1) * gridStep;
        if (buyPrice < priceMin) break;
        
        const quantity = (perGridUSDT * adjustmentFactor) / buyPrice;
        const result = await placeOrder(symbol, 'buy', buyPrice, quantity);
        
        if (result.code === '00000') {
            console.log(`   ✅ 买单 ${i+1}: ${buyPrice.toFixed(2)} | ${quantity.toFixed(6)}`);
            placedBuy++;
        }
        
        await new Promise(resolve => setTimeout(resolve, 200));
    }
    
    // 放置卖单
    const sellAdjustment = rsi > 70 ? 1.3 : 1.0; // RSI 超买时增加卖单
    
    for (let i = 0; i < gridNum / 2; i++) {
        const sellPrice = currentPrice + (i + 1) * gridStep;
        if (sellPrice > priceMax) break;
        
        const quantity = (perGridUSDT * sellAdjustment) / sellPrice;
        const result = await placeOrder(symbol, 'sell', sellPrice, quantity);
        
        if (result.code === '00000') {
            console.log(`   ✅ 卖单 ${i+1}: ${sellPrice.toFixed(2)} | ${quantity.toFixed(6)}`);
            placedSell++;
        }
        
        await new Promise(resolve => setTimeout(resolve, 200));
    }
    
    console.log(`\n✅ 调仓完成！`);
    console.log(`   新买单：${placedBuy} 个`);
    console.log(`   新卖单：${placedSell} 个`);
}

// 主函数
async function main() {
    console.log('\n' + '='.repeat(60));
    console.log('🤖 动态网格调仓系统');
    console.log('='.repeat(60));
    
    const settings = JSON.parse(fs.readFileSync(SETTINGS_FILE));
    
    // 只处理 BTC 和 SOL
    const activeSymbols = {
        btc: settings.btc,
        sol: settings.sol
    };
    
    for (const [key, config] of Object.entries(activeSymbols)) {
        try {
            await rebalance(config.symbol, {
                priceMin: config.priceMin,
                priceMax: config.priceMax,
                gridNum: config.gridNum,
                totalUSDT: config.maxInvestment
            });
            
            await new Promise(resolve => setTimeout(resolve, 3000));
        } catch (e) {
            console.log(`\n❌ ${config.symbol} 调仓失败：${e.message}`);
        }
    }
    
    console.log('\n' + '='.repeat(60));
    console.log('✅ 所有调仓完成');
    console.log('='.repeat(60) + '\n');
}

main().catch(console.error);
