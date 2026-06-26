#!/usr/bin/env node
// ETHUSDT 网格启动脚本

const crypto = require('crypto');
const https = require('https');
const http = require('http');

const CONFIG = {
    apiKey: process.env.BITGET_API_KEY,
    secretKey: process.env.BITGET_SECRET_KEY,
    passphrase: process.env.BITGET_PASSPHRASE
};

// 网格配置
const SYMBOL = 'ETHUSDT';
const GRID_NUM = 25;
const PRICE_MIN = 2300;
const PRICE_MAX = 2800;
const AMOUNT_PER_GRID = 8; // USDT

function log(...args) {
    console.log(`[${new Date().toLocaleString('zh-CN')}]`, ...args);
}

function sign(message) {
    return crypto.createHmac('sha256', CONFIG.secretKey).update(message).digest('base64');
}

function request(endpoint, method = 'GET', params = {}, body = null) {
    return new Promise((resolve) => {
        const now = new Date();
        const timestamp = now.toISOString().split('.')[0] + '.000Z';
        let pathStr = endpoint;
        let bodyStr = '';
        
        if (method === 'GET' && Object.keys(params).length > 0) {
            pathStr += '?' + new URLSearchParams(params).toString();
        } else if (method === 'POST' && body) {
            bodyStr = typeof body === 'string' ? body : JSON.stringify(body);
        }
        
        const fullpath = '/api/v2' + pathStr;
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
                        resolve({ status: res.statusCode, data: JSON.parse(data) });
                    } catch (e) {
                        resolve({ status: res.statusCode, raw: data.substring(0, 200) });
                    }
                    socket.destroy();
                });
            });
            
            req.on('error', (e) => {
                resolve({ error: e.message });
                socket.destroy();
            });
            
            if (bodyStr) req.write(bodyStr);
            req.end();
        });
        
        proxyReq.on('error', (e) => {
            resolve({ error: e.message });
        });
        proxyReq.end();
    });
}

async function main() {
    log('🚀 启动 ETHUSDT 网格...');
    
    // 获取当前价格
    const tickerResult = await request('/spot/market/ticker?symbol=ETHUSDT');
    let currentPrice;
    if (tickerResult.data && tickerResult.data.last) {
        currentPrice = parseFloat(tickerResult.data.last);
        log(`📈 ETHUSDT 当前价格：${currentPrice} USDT`);
    } else {
        log('❌ 无法获取价格，使用默认值 2500');
        currentPrice = 2500;
    }
    
    // 计算网格
    const gridSpacing = (PRICE_MAX - PRICE_MIN) / GRID_NUM;
    log(`网格数：${GRID_NUM} | 区间：${PRICE_MIN}-${PRICE_MAX} USDT`);
    log(`网格间距：${gridSpacing.toFixed(2)} USDT (约 ${(gridSpacing/currentPrice*100).toFixed(2)}%)`);
    
    // 计算买单和卖单
    const buyOrders = [];
    const sellOrders = [];
    
    for (let i = 0; i < GRID_NUM; i++) {
        const price = PRICE_MIN + i * gridSpacing;
        const amount = AMOUNT_PER_GRID / price; // 固定 USDT 金额
        
        if (price < currentPrice) {
            buyOrders.push({ price: price.toFixed(2), amount: amount.toFixed(4) });
        } else if (price > currentPrice) {
            sellOrders.push({ price: price.toFixed(2), amount: amount.toFixed(4) });
        }
    }
    
    log(`\n📥 创建买单 (最多${Math.min(buyOrders.length, 8)}个)...`);
    let createdBuy = 0;
    for (const order of buyOrders.slice(0, 8)) {
        log(`📝 下单：BUY ${SYMBOL} @ ${order.price} USDT, 数量：${order.amount}`);
        
        const result = await request('/spot/trade/placeOrder', 'POST', {}, {
            symbol: SYMBOL,
            side: 'buy',
            force: 'GTC',
            price: order.price,
            quantity: order.amount
        });
        
        if (result.data && result.data.orderId) {
            log(`✅ 订单成功！ID: ${result.data.orderId}`);
            createdBuy++;
        } else {
            log(`❌ 订单失败：${result.data?.msg || result.error || '未知错误'}`);
        }
        
        await new Promise(r => setTimeout(r, 500)); // 限流
    }
    
    log(`\n📤 创建卖单 (最多${Math.min(sellOrders.length, 8)}个)...`);
    let createdSell = 0;
    for (const order of sellOrders.slice(0, 8)) {
        log(`📝 下单：SELL ${SYMBOL} @ ${order.price} USDT, 数量：${order.amount}`);
        
        const result = await request('/spot/trade/placeOrder', 'POST', {}, {
            symbol: SYMBOL,
            side: 'sell',
            force: 'GTC',
            price: order.price,
            quantity: order.amount
        });
        
        if (result.data && result.data.orderId) {
            log(`✅ 订单成功！ID: ${result.data.orderId}`);
            createdSell++;
        } else {
            log(`❌ 订单失败：${result.data?.msg || result.error || '未知错误'}`);
        }
        
        await new Promise(r => setTimeout(r, 500));
    }
    
    log(`\n✅ ETHUSDT 网格创建完成！共 ${createdBuy + createdSell} 个订单`);
    log(`   买单：${createdBuy} 个 | 卖单：${createdSell} 个`);
}

main().catch(e => log('❌ 错误:', e.message));
