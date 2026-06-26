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
    log('💰 限价买入 100 USDT 的 BNB...');
    
    const ticker = await api('/api/v2/spot/market/ticker?symbol=BNBUSDT');
    let price = 380;
    if(ticker.data && ticker.data.last) {
        price = parseFloat(ticker.data.last);
        log(`✅ BNB 当前价格：${price} USDT`);
    }
    
    // 限价单：略高于市价确保成交
    const buyPrice = (price * 1.005).toFixed(1); // 高 0.5%
    const bnbQty = (100 / buyPrice).toFixed(3);
    
    log(`\n📥 限价买入 @ ${buyPrice} USDT = ${bnbQty} BNB`);
    
    const result = await api('/api/v2/spot/trade/place-order', 'POST', {
        symbol: 'BNBUSDT',
        side: 'buy',
        force: 'GTC',
        orderType: 'limit',
        price: buyPrice,
        size: bnbQty
    });
    
    if(result.code === '00000' && result.data && result.data.orderId) {
        log(`✅ 订单成功！ID: ${result.data.orderId}`);
        log(`   等待成交...`);
        
        // 等待 2 秒检查是否成交
        await new Promise(r => setTimeout(r, 2000));
        
        const orders = await api('/api/v2/spot/trade/unfilled-orders?symbol=BNBUSDT');
        if(orders.code === '00000' && orders.data && orders.data.length > 0) {
            log('⏳ 订单尚未完全成交');
        } else {
            log('✅ 订单已成交！');
        }
    } else {
        log(`❌ 失败：${result.msg || result.code}`);
    }
}

main();
