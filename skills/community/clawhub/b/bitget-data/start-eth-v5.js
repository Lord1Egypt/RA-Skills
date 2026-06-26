#!/usr/bin/env node
const fs = require('fs');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const CONFIG = JSON.parse(fs.readFileSync('config.json'));
const SYMBOL = 'ETHUSDT';
const GRID_NUM = 20;
const PRICE_MIN = 2200;
const PRICE_MAX = 2700;
const AMOUNT = 10;

function log(msg) { console.log(`[${new Date().toLocaleString('zh-CN')}] ${msg}`); }

function sign(msg) {
    return crypto.createHmac('sha256', CONFIG.secretKey).update(msg).digest('base64');
}

function api(endpoint, method = 'GET', body = null) {
    return new Promise((resolve) => {
        const timestamp = Date.now().toString();
        const signStr = timestamp + method + endpoint + (body ? JSON.stringify(body) : '');
        const signature = sign(signStr);
        
        const proxy = http.request({hostname:'127.0.0.1',port:7897,path:'api.bitget.com:443',method:'CONNECT'});
        
        proxy.on('connect', (res, socket) => {
            const req = https.request({
                socket, hostname:'api.bitget.com', port:443, path:endpoint, method,
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
    
    const ticker = await api('/api/v2/spot/market/ticker?symbol=ETHUSDT');
    let price = 2500;
    if(ticker.data && ticker.data.last) {
        price = parseFloat(ticker.data.last);
        log(`✅ ETH 当前价格：${price} USDT`);
    }
    
    const spacing = (PRICE_MAX - PRICE_MIN) / GRID_NUM;
    log(`网格：${GRID_NUM}格 | ${PRICE_MIN}-${PRICE_MAX} | 间距:${spacing.toFixed(1)} USDT`);
    log(`当前价 ${price}，位于网格${((price-PRICE_MIN)/spacing).toFixed(1)}格处`);
    
    // 只创建买单（因为没有 ETH 持仓）
    log('\n📥 买单（先买入建仓）...');
    let buyCount = 0;
    const buyStart = Math.floor((price - PRICE_MIN) / spacing) - 1;
    const maxBuy = Math.min(buyStart + 1, 8); // 最多 8 个买单
    
    for(let i = buyStart; i >= 0 && buyCount < maxBuy; i--) {
        const p = (PRICE_MIN + i * spacing).toFixed(1);
        const q = (AMOUNT / p).toFixed(4);
        log(`BUY @ ${p} = ${q} ETH`);
        const r = await api('/api/v2/spot/trade/place-order', 'POST', {
            symbol: SYMBOL, side: 'buy', force: 'GTC', orderType: 'limit', price: p, size: q
        });
        if(r.code === '00000' && r.data && r.data.orderId) { log(`✅ ${r.data.orderId}`); buyCount++; }
        else log(`❌ ${r.msg||r.code||r.error}`);
        await new Promise(r=>setTimeout(r, 500));
    }
    
    log(`\n✅ ETH 完成！共 ${buyCount} 个买单`);
    log(`💡 提示：等待买单成交后，再创建卖单`);
}

main();
