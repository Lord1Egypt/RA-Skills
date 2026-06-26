#!/usr/bin/env node
const fs = require('fs');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const CONFIG = JSON.parse(fs.readFileSync('config.json'));
const SYMBOL = 'ETHUSDT';

// 调整：买单价格上限 2036 USDT
const BUY_PRICE_MAX = 2030;
const BUY_PRICE_MIN = 1800;
const BUY_NUM = 8;
const AMOUNT = 4;

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
    log('📥 部署 ETH 买单（低价区）...');
    
    const ticker = await api('/api/v2/spot/market/ticker?symbol=ETHUSDT');
    let price = 2500;
    if(ticker.data && ticker.data.last) {
        price = parseFloat(ticker.data.last);
        log(`✅ 当前价格：${price} USDT`);
    }
    
    const spacing = (BUY_PRICE_MAX - BUY_PRICE_MIN) / BUY_NUM;
    log(`区间：${BUY_PRICE_MIN} - ${BUY_PRICE_MAX} | 间距：${spacing.toFixed(1)} USDT`);
    
    let count = 0;
    for(let i = BUY_NUM - 1; i >= 0; i--) {
        const p = (BUY_PRICE_MIN + i * spacing).toFixed(1);
        const q = (AMOUNT / p).toFixed(4);
        log(`BUY @ ${p} = ${q} ETH`);
        
        const r = await api('/api/v2/spot/trade/place-order', 'POST', {
            symbol: SYMBOL, side: 'buy', force: 'GTC', orderType: 'limit', price: p, size: q
        });
        
        if(r.code === '00000' && r.data && r.data.orderId) {
            log(`✅ ${r.data.orderId}`);
            count++;
        } else {
            log(`❌ ${r.msg || r.code}`);
        }
        await new Promise(r => setTimeout(r, 400));
    }
    
    log(`\n✅ 完成！共 ${count} 个买单`);
}

main();
