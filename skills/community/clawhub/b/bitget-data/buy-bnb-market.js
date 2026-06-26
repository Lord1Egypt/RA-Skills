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
    log('💰 市价买入 100 USDT 的 BNB 建仓...');
    
    const ticker = await api('/api/v2/spot/market/ticker?symbol=BNBUSDT');
    let price = 380;
    if(ticker.data && ticker.data.last) {
        price = parseFloat(ticker.data.last);
        log(`✅ BNB 当前价格：${price} USDT`);
    }
    
    // 计算数量
    const usdtAmount = 100;
    const bnbQty = (usdtAmount / price).toFixed(3);
    log(`\n📥 市价买入 ${bnbQty} BNB (约 ${usdtAmount} USDT)...`);
    
    // 尝试用 size 参数（BNB 数量）
    const result = await api('/api/v2/spot/trade/place-order', 'POST', {
        symbol: 'BNBUSDT',
        side: 'buy',
        force: 'FOK',
        orderType: 'market',
        size: bnbQty
    });
    
    if(result.code === '00000' && result.data && result.data.orderId) {
        log(`✅ 成交！订单 ID: ${result.data.orderId}`);
        log(`   成交均价：${result.data.priceAvg || '市价'} | 数量：${bnbQty} BNB`);
    } else {
        log(`❌ 失败：${result.msg || result.code || result.error}`);
        log('💡 尝试用 quoteSize (USDT 金额)...');
        
        // 尝试用 quoteSize
        const result2 = await api('/api/v2/spot/trade/place-order', 'POST', {
            symbol: 'BNBUSDT',
            side: 'buy',
            force: 'FOK',
            orderType: 'market',
            quoteSize: usdtAmount.toString()
        });
        
        if(result2.code === '00000' && result2.data && result2.data.orderId) {
            log(`✅ 成交！订单 ID: ${result2.data.orderId}`);
        } else {
            log(`❌ 再次失败：${result2.msg || result2.code}`);
        }
    }
}

main();
