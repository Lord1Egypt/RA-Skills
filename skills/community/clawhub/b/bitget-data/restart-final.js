#!/usr/bin/env node
// Bitget 网格重启 - 最终修复版 (使用正确的 API 参数)

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
                        const result = JSON.parse(data);
                        resolve(result);
                    } catch (e) {
                        resolve({raw: data.substring(0, 200)});
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

async function getOrders(symbol) {
    const result = await request('/spot/trade/unfilled-orders', 'GET', { symbol, limit: '100' });
    return result.data || [];
}

async function cancelOrder(symbol, orderId) {
    const body = { symbol, orderId };
    const result = await request('/spot/trade/cancel-order', 'POST', {}, body);
    return result.code === '00000';
}

async function placeOrder(symbol, side, price, quantity) {
    // 根据 API 文档，正确的参数名是 timeInForceValue 不是 force
    const body = {
        symbol,
        side,
        timeInForceValue: 'normal',
        orderType: 'limit',
        price: price.toString(),
        quantity: quantity.toString()
    };
    
    const result = await request('/spot/trade/place-order', 'POST', {}, body);
    return {
        success: result.code === '00000',
        orderId: result.data?.orderId,
        msg: result.msg,
        code: result.code
    };
}

async function cancelAllOrders(symbol) {
    log(`📋 取消 ${symbol} 所有订单...`);
    const orders = await getOrders(symbol);
    
    if (orders.length === 0) {
        log(`   ✅ 无订单需要取消`);
        return 0;
    }
    
    let canceled = 0;
    for (const order of orders) {
        const success = await cancelOrder(symbol, order.orderId);
        if (success) canceled++;
    }
    
    log(`   ✅ 成功取消 ${canceled}/${orders.length} 个订单`);
    return canceled;
}

async function createGrid(name, config, currentPrice) {
    const { symbol, gridNum, priceMin, priceMax, amount } = config;
    
    log(`\n📊 创建 ${name} 网格 (${symbol})...`);
    log(`   当前价：${currentPrice}`);
    log(`   区间：${priceMin} - ${priceMax}`);
    log(`   网格：${gridNum} 格`);
    log(`   每格：${amount} USDT`);
    
    const step = (priceMax - priceMin) / gridNum;
    let placed = 0;
    let errors = 0;
    
    // 创建买单 (当前价格以下)
    log(`   📈 创建买单...`);
    for (let i = 0; i < Math.floor(gridNum / 2); i++) {
        const price = priceMin + i * step;
        if (price >= currentPrice) continue;
        
        const quantity = amount / price;
        const result = await placeOrder(symbol, 'buy', price.toFixed(2), quantity.toFixed(6));
        
        if (result.success) {
            placed++;
            if (placed <= 3 || placed >= Math.floor(gridNum/2) - 1) {
                log(`      ✅ 买单：${quantity.toFixed(6)} @ ${price.toFixed(2)}`);
            }
        } else {
            errors++;
            if (errors <= 3) log(`      ❌ 失败：${result.msg}`);
        }
    }
    
    // 创建卖单 (当前价格以上)
    log(`   📉 创建卖单...`);
    const startI = Math.ceil(gridNum / 2);
    for (let i = startI; i < gridNum; i++) {
        const price = priceMin + i * step;
        if (price <= currentPrice) continue;
        
        const quantity = amount / price;
        const result = await placeOrder(symbol, 'sell', price.toFixed(2), quantity.toFixed(6));
        
        if (result.success) {
            placed++;
            if (placed - Math.floor(gridNum/2) <= 3 || i >= gridNum - 2) {
                log(`      ✅ 卖单：${quantity.toFixed(6)} @ ${price.toFixed(2)}`);
            }
        } else {
            errors++;
        }
    }
    
    log(`   ✅ 成功创建 ${placed} 个订单 (${errors} 失败)`);
    return placed;
}

async function main() {
    log('=' .repeat(70));
    log('🔄 Bitget 网格重启 - 应用优化配置');
    log('=' .repeat(70));
    
    // 获取当前价格
    const tickers = await request('/spot/market/tickers', 'GET', {});
    const btcPrice = parseFloat(tickers.data?.find(t => t.symbol === 'BTCUSDT')?.lastPr || 67550);
    const solPrice = parseFloat(tickers.data?.find(t => t.symbol === 'SOLUSDT')?.lastPr || 82.86);
    
    log(`\n💰 当前价格:`);
    log(`   BTCUSDT: ${btcPrice} USDT`);
    log(`   SOLUSDT: ${solPrice} USDT`);
    
    // 1. 取消旧订单
    log('\n📋 第一步：取消现有订单');
    log('-'.repeat(60));
    
    const btcOrders = await getOrders('BTCUSDT');
    const solOrders = await getOrders('SOLUSDT');
    
    log(`BTCUSDT: ${btcOrders.length} 个订单`);
    log(`SOLUSDT: ${solOrders.length} 个订单`);
    
    await cancelAllOrders('BTCUSDT');
    await cancelAllOrders('SOLUSDT');
    
    log('\n⏳ 等待订单取消生效 (3 秒)...');
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // 2. 创建新网格
    log('\n📋 第二步：创建新网格');
    log('-'.repeat(60));
    
    const btcPlaced = await createGrid('BTC', SETTINGS.btc, btcPrice);
    const solPlaced = await createGrid('SOL', SETTINGS.sol, solPrice);
    
    // 3. 验证
    log('\n📋 第三步：验证挂单');
    log('-'.repeat(60));
    
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const newBtcOrders = await getOrders('BTCUSDT');
    const newSolOrders = await getOrders('SOLUSDT');
    
    log(`BTCUSDT: ${newBtcOrders.length} 个订单`);
    log(`SOLUSDT: ${newSolOrders.length} 个订单`);
    
    // 4. 汇总
    log('\n' + '=' .repeat(70));
    log('📊 重启完成汇总');
    log('=' .repeat(70));
    log(`BTCUSDT: ${btcPlaced} 个订单 (验证：${newBtcOrders.length})`);
    log(`SOLUSDT: ${solPlaced} 个订单 (验证：${newSolOrders.length})`);
    log(`总计：${btcPlaced + solPlaced} 个订单`);
    
    if (newBtcOrders.length > 0 && newSolOrders.length > 0) {
        log('\n✅ 网格重启成功！');
    } else {
        log('\n⚠️  部分订单可能失败，请检查');
    }
    
    log('=' .repeat(70) + '\n');
}

main().catch(e => {
    log('❌ 错误：' + e.message);
    log(e.stack);
    process.exit(1);
});
