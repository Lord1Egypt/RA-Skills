#!/usr/bin/env node
const fs = require('fs');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const CONFIG = JSON.parse(fs.readFileSync('config.json'));
const SYMBOL = 'ETHUSDT';
const GRID_NUM = 25;
const PRICE_MIN = 2300;
const PRICE_MAX = 2800;
const AMOUNT = 8;

function log(msg) { console.log(`[${new Date().toLocaleString('zh-CN')}] ${msg}`); }

function sign(msg) {
    return crypto.createHmac('sha256', CONFIG.secretKey).update(msg).digest('base64');
}

function api(endpoint, method = 'GET', body = null) {
    return new Promise((resolve) => {
        const timestamp = Date.now().toString();
        const pathStr = endpoint;
        const signStr = timestamp + method + pathStr + (body ? JSON.stringify(body) : '');
        const signature = sign(signStr);
        
        const proxy = http.request({hostname:'127.0.0.1',port:7897,path:'api.bitget.com:443',method:'CONNECT'});
        
        proxy.on('connect', (res, socket) => {
            const req = https.request({
                socket, hostname:'api.bitget.com', port:443, path:pathStr, method,
                headers:{
                    'ACCESS-KEY': CONFIG.apiKey,
                    'ACCESS-SIGN': signature,
                    'ACCESS-TIMESTAMP': timestamp,
                    'ACCESS-PASSPHRASE': CONFIG.passphrase,
                    'Content-Type': 'application/json'
                }
            }, (res) => {
                let data = '';
                res.on('data', c => data += c);
                res.on('end', () => {
                    try { resolve(JSON.parse(data)); }
                    catch(e) { resolve({raw:data}); }
                });
            });
            req.on('error', e => resolve({error:e.message}));
            if(body) req.write(JSON.stringify(body));
            req.end();
        });
        proxy.on('error', e => resolve({error:e.message}));
        proxy.end();
    });
}

async function main() {
    log('🚀 启动 ETHUSDT 网格...');
    
    // 获取价格
    const ticker = await api('/api/v2/spot/market/ticker?symbol=ETHUSDT');
    let price = 2500;
    if(ticker.data && ticker.data.last) {
        price = parseFloat(ticker.data.last);
        log(`✅ ETH 当前价格：${price} USDT`);
    } else {
        log(`⚠️ 无法获取价格，使用 ${price}`);
    }
    
    const spacing = (PRICE_MAX - PRICE_MIN) / GRID_NUM;
    log(`网格：${GRID_NUM}格 | ${PRICE_MIN}-${PRICE_MAX} | 间距:${spacing.toFixed(1)} USDT`);
    
    // 创建买单
    log('\n📥 买单...');
    let buyCount = 0;
    for(let i = Math.floor((price - PRICE_MIN) / spacing) - 1; i >= 0 && buyCount < 6; i--) {
        const p = (PRICE_MIN + i * spacing).toFixed(1);
        const q = (AMOUNT / p).toFixed(4);
        log(`BUY @ ${p} = ${q} ETH`);
        const r = await api('/api/v2/spot/trade/placeOrder', 'POST', {
            symbol: SYMBOL, side: 'buy', force: 'GTC', price: p, quantity: q
        });
        if(r.data && r.data.orderId) { log(`✅ ${r.data.orderId}`); buyCount++; }
        else log(`❌ ${r.msg||r.error}`);
        await new Promise(r=>setTimeout(r, 400));
    }
    
    // 创建卖单
    log('\n📤 卖单...');
    let sellCount = 0;
    const startI = Math.floor((price - PRICE_MIN) / spacing) + 1;
    for(let i = startI; i < GRID_NUM && sellCount < 6; i++) {
        const p = (PRICE_MIN + i * spacing).toFixed(1);
        const q = (AMOUNT / p).toFixed(4);
        log(`SELL @ ${p} = ${q} ETH`);
        const r = await api('/api/v2/spot/trade/placeOrder', 'POST', {
            symbol: SYMBOL, side: 'sell', force: 'GTC', price: p, quantity: q
        });
        if(r.data && r.data.orderId) { log(`✅ ${r.data.orderId}`); sellCount++; }
        else log(`❌ ${r.msg||r.error}`);
        await new Promise(r=>setTimeout(r, 400));
    }
    
    log(`\n✅ ETH 完成！${buyCount}买 + ${sellCount}卖 = ${buyCount+sellCount}单`);
}

main();
