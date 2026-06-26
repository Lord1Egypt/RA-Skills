#!/usr/bin/env node
// 启动 SOL 网格

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const DATA_DIR = process.env.BITGET_DATA_DIR || path.join(__dirname);
const CONFIG_FILE = path.join(DATA_DIR, 'config.json');

function loadJson(file) {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function log(message) {
    const timestamp = new Date().toLocaleString('zh-CN');
    console.log(`[${timestamp}] ${message}`);
}

function sign(message, secret) {
    return crypto.createHmac('sha256', secret).update(message).digest('base64');
}

function apiRequest(endpoint, method = 'GET', body = null) {
    return new Promise((resolve, reject) => {
        const config = loadJson(CONFIG_FILE);
        const timestamp = Date.now().toString();
        const pathWithQuery = endpoint;
        
        const signStr = timestamp + method + pathWithQuery + (body ? JSON.stringify(body) : '');
        const signature = sign(signStr, config.secretKey);

        const proxyReq = http.request({
            hostname: '127.0.0.1',
            port: 7897,
            path: `api.bitget.com:443`,
            method: 'CONNECT'
        });
        
        proxyReq.on('connect', (res, socket) => {
            const req = https.request({
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
                    'Content-Type': 'application/json'
                }
            }, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => resolve(JSON.parse(data)));
            });
            req.on('error', reject);
            if (body) req.write(JSON.stringify(body));
            req.end();
        });
        proxyReq.on('error', reject);
        proxyReq.end();
    });
}

async function placeOrder(symbol, side, price, quantity) {
    const body = {
        symbol: symbol,
        side: side,
        orderType: 'limit',
        force: 'GTC',
        price: price.toString(),
        size: quantity.toString()
    };
    
    log(`📝 下单：${side.toUpperCase()} ${symbol} @ ${price} USDT, 数量：${quantity}`);
    const result = await apiRequest('/api/v2/spot/trade/place-order', 'POST', body);
    
    if (result.code === '00000') {
        log(`✅ 订单成功！ID: ${result.data.orderId}`);
        return { success: true, orderId: result.data.orderId };
    } else {
        log(`❌ 订单失败：${result.msg}`);
        return { success: false, error: result.msg };
    }
}

async function main() {
    log('🚀 启动 SOLUSDT 网格...\n');
    
    // 获取当前价格
    const ticker = await apiRequest('/api/v2/spot/market/tickers?symbol=SOLUSDT');
    const currentPrice = parseFloat(ticker.data[0].lastPr);
    log(`📈 SOLUSDT 当前价格：${currentPrice} USDT\n`);
    
    // SOL 网格参数
    const gridNum = 30;
    const priceMin = 75;
    const priceMax = 95;
    const amountPerGrid = 12;
    const gridStep = (priceMax - priceMin) / gridNum;
    
    log(`网格数：${gridNum} | 区间：${priceMin}-${priceMax} USDT`);
    log(`网格间距：${gridStep.toFixed(2)} USDT\n`);
    
    const orders = [];
    
    // 创建买单 (当前价格下方)
    const maxBuys = Math.floor((currentPrice - priceMin) / gridStep);
    log(`📥 创建买单 (最多${Math.min(maxBuys, 5)}个)...\n`);
    
    let buyCount = 0;
    for (let i = 1; i <= maxBuys && buyCount < 5; i++) {
        const buyPrice = currentPrice - (i * gridStep);
        if (buyPrice < priceMin) break;
        
        const quantity = amountPerGrid / buyPrice;
        const result = await placeOrder('SOLUSDT', 'buy', buyPrice.toFixed(2), quantity.toFixed(4));
        
        if (result.success) {
            orders.push(result.orderId);
            buyCount++;
        }
        await new Promise(r => setTimeout(r, 500));
    }
    
    // 创建卖单 (当前价格上方)
    const maxSells = Math.floor((priceMax - currentPrice) / gridStep);
    log(`\n📤 创建卖单 (最多${Math.min(maxSells, 5)}个)...\n`);
    
    let sellCount = 0;
    for (let i = 1; i <= maxSells && sellCount < 5; i++) {
        const sellPrice = currentPrice + (i * gridStep);
        if (sellPrice > priceMax) break;
        
        const quantity = amountPerGrid / sellPrice;
        const result = await placeOrder('SOLUSDT', 'sell', sellPrice.toFixed(2), quantity.toFixed(4));
        
        if (result.success) {
            orders.push(result.orderId);
            sellCount++;
        }
        await new Promise(r => setTimeout(r, 500));
    }
    
    log(`\n✅ SOLUSDT 网格创建完成！共 ${orders.length} 个订单`);
}

main().catch(console.error);
