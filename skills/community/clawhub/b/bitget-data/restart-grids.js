#!/usr/bin/env node
// 重启网格 - 取消旧订单 + 创建新网格

const fs = require('fs');
const crypto = require('crypto');
const http = require('http');
const https = require('https');

const CONFIG = JSON.parse(fs.readFileSync(__dirname + '/config.json'));
const SETTINGS = JSON.parse(fs.readFileSync(__dirname + '/grid_settings.json'));

function log(msg) {
    console.log(`[${new Date().toLocaleString('zh-CN')}] ${msg}`);
}

function sign(message) {
    return crypto.createHmac('sha256', CONFIG.secretKey).update(message).digest('base64');
}

function request(endpoint, method = 'GET', params = {}) {
    return new Promise((resolve) => {
        const timestamp = new Date().toISOString().split('.')[0] + '.000Z';
        const qs = method === 'GET' && Object.keys(params).length > 0 ? '?' + new URLSearchParams(params) : '';
        const fullpath = '/api/v2' + endpoint + qs;
        let body = '';
        if (method === 'POST') body = JSON.stringify(params);
        const signStr = timestamp + method + fullpath + body;
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
                    try { resolve(JSON.parse(data)); }
                    catch(e) { resolve({raw: data.substring(0,200)}); }
                });
            });
            req.on('error', e => resolve({error: e.message}));
            if(body) req.write(body);
            req.end();
        });
        proxyReq.on('error', e => resolve({error: e.message}));
        proxyReq.end();
    });
}

async function cancelAllOrders(symbol) {
    log(`📋 取消 ${symbol} 所有订单...`);
    try {
        const result = await request('/spot/trade/cancel-all-orders', 'POST', { symbol });
        if (result.code === '00000') {
            log(`   ✅ 成功取消所有订单`);
            return true;
        } else {
            log(`   ⚠️  ${result.msg || '取消失败'}`);
            return false;
        }
    } catch (e) {
        log(`   ❌ 错误：${e.message}`);
        return false;
    }
}

async function getCurrentOrders(symbol) {
    const result = await request('/spot/trade/unfilled-orders', 'GET', { symbol, limit: '100' });
    return result.data || [];
}

async function placeOrder(symbol, side, price, size) {
    const params = {
        symbol,
        side,
        force: 'limit',
        price: price.toString(),
        quantity: size.toString()
    };
    
    try {
        const result = await request('/spot/trade/place-order', 'POST', params);
        return result.code === '00000';
    } catch (e) {
        return false;
    }
}

async function createGrid(name, config) {
    const { symbol, gridNum, priceMin, priceMax, amount, maxPosition } = config;
    
    log(`\n📊 创建 ${name} 网格...`);
    log(`   区间：${priceMin} - ${priceMax}`);
    log(`   网格：${gridNum} 格`);
    log(`   每格：${amount} USDT`);
    
    const step = (priceMax - priceMin) / gridNum;
    const currentPrice = name === 'BTC' ? 67550 : 82.86;
    
    let placed = 0;
    
    // 创建买单 (当前价格以下)
    for (let i = 0; i < gridNum / 2; i++) {
        const price = (priceMin + i * step).toFixed(2);
        const size = (amount / parseFloat(price)).toFixed(6);
        
        if (parseFloat(price) < currentPrice) {
            const success = await placeOrder(symbol, 'buy', price, size);
            if (success) placed++;
        }
    }
    
    // 创建卖单 (当前价格以上)
    for (let i = Math.floor(gridNum / 2); i < gridNum; i++) {
        const price = (priceMin + i * step).toFixed(2);
        const size = (amount / parseFloat(price)).toFixed(6);
        
        if (parseFloat(price) > currentPrice) {
            const success = await placeOrder(symbol, 'sell', price, size);
            if (success) placed++;
        }
    }
    
    log(`   ✅ 成功创建 ${placed} 个订单`);
    return placed;
}

async function main() {
    log('=' .repeat(70));
    log('🔄 Bitget 网格重启 - 应用优化配置');
    log('=' .repeat(70));
    
    // 1. 取消旧订单
    log('\n📋 第一步：取消现有订单');
    log('-'.repeat(60));
    
    const btcOrders = await getCurrentOrders('BTCUSDT');
    const solOrders = await getCurrentOrders('SOLUSDT');
    
    log(`BTCUSDT: ${btcOrders.length} 个订单待取消`);
    log(`SOLUSDT: ${solOrders.length} 个订单待取消`);
    
    if (btcOrders.length > 0) await cancelAllOrders('BTCUSDT');
    if (solOrders.length > 0) await cancelAllOrders('SOLUSDT');
    
    // 等待订单取消
    log('\n⏳ 等待订单取消生效...');
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // 2. 创建新网格
    log('\n📋 第二步：创建新网格');
    log('-'.repeat(60));
    
    const btcPlaced = await createGrid('BTC', SETTINGS.btc);
    const solPlaced = await createGrid('SOL', SETTINGS.sol);
    
    // 3. 汇总
    log('\n' + '=' .repeat(70));
    log('📊 重启完成汇总');
    log('=' .repeat(70));
    log(`BTCUSDT: 创建 ${btcPlaced} 个订单`);
    log(`SOLUSDT: 创建 ${solPlaced} 个订单`);
    log(`总计：${btcPlaced + solPlaced} 个订单`);
    log('\n✅ 网格重启完成！');
    log('=' .repeat(70) + '\n');
}

main().catch(e => {
    log('❌ 错误：' + e.message);
    process.exit(1);
});
