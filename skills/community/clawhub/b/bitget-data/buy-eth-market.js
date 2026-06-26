#!/usr/bin/env node
const fs = require('fs');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const CONFIG = JSON.parse(fs.readFileSync('config.json'));

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
    log('💰 市价买入 50 USDT 的 ETH 建仓...');
    
    // 先获取价格
    const ticker = await api('/api/v2/spot/market/ticker?symbol=ETHUSDT');
    let price = 2500;
    if(ticker.data && ticker.data.last) {
        price = parseFloat(ticker.data.last);
        log(`✅ ETH 当前价格：${price} USDT`);
    }
    
    // 市价买单
    const usdtAmount = 50;
    const ethQty = (usdtAmount / price).toFixed(4);
    log(`\n📥 市价买入 ${ethQty} ETH (约 ${usdtAmount} USDT)...`);
    
    const result = await api('/api/v2/spot/trade/place-order', 'POST', {
        symbol: 'ETHUSDT',
        side: 'buy',
        force: 'FOK',
        orderType: 'market',
        size: ethQty
    });
    
    if(result.code === '00000' && result.data && result.data.orderId) {
        log(`✅ 成交！订单 ID: ${result.data.orderId}`);
        log(`   价格：${result.data.priceAvg || '市价'} | 数量：${ethQty} ETH`);
    } else {
        log(`❌ 失败：${result.msg || result.code || result.error}`);
    }
}

main();
