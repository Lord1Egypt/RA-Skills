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
        const now = new Date();
        const timestamp = now.toISOString().split('.')[0] + '.000Z';
        const signStr = timestamp + method + endpoint + (body ? JSON.stringify(body) : '');
        const signature = sign(signStr);
        
        const proxy = http.request({hostname:'127.0.0.1',port:7897,path:'api.bitget.com:443',method:'CONNECT'});
        
        proxy.on('connect', (res, socket) => {
            const req = https.request({socket, hostname:'api.bitget.com', port:443, path:endpoint, method,
                headers:{'ACCESS-KEY': CONFIG.apiKey, 'ACCESS-SIGN': signature, 'ACCESS-TIMESTAMP': timestamp,
                    'ACCESS-PASSPHRASE': CONFIG.passphrase, 'Content-Type': 'application/json'}});
            let data = '';
            req.on('response', res => { res.on('data', c => data += c); res.on('end', () => { try{resolve(JSON.parse(data));}catch(e){resolve({raw:data});} }); });
            req.end();
        });
        proxy.end();
    });
}

async function main() {
    log('🔧 重新部署 BNB 网格...');
    
    const ticker = await api('/api/v2/spot/market/ticker?symbol=BNBUSDT');
    let price = 630;
    if(ticker.data && ticker.data.last) {
        price = parseFloat(ticker.data.last);
        log(`✅ BNB 当前价格：${price} USDT`);
    }
    
    const assets = await api('/api/v2/spot/account/assets');
    let bnbBalance = 0;
    if(assets.code === '00000' && assets.data) {
        const bnb = assets.data.find(a => a.coin === 'BNB');
        if(bnb) {
            bnbBalance = parseFloat(bnb.available);
            log(`✅ BNB 可用余额：${bnbBalance.toFixed(4)} BNB`);
        }
    }
    
    // 新配置
    const buyPrices = [625, 620, 615, 610, 605];
    const sellPrices = [640, 645, 650, 655, 660];
    const amount = 0.15;
    
    log('\n📥 部署买单...');
    let buyCount = 0;
    for(const p of buyPrices) {
        log(`BUY @ ${p} = ${amount} BNB`);
        const r = await api('/api/v2/spot/trade/place-order', 'POST', {
            symbol: 'BNBUSDT', side: 'buy', force: 'GTC', orderType: 'limit',
            price: p.toString(), size: amount.toString()
        });
        if(r.code === '00000' && r.data && r.data.orderId) {
            log(`✅ ${r.data.orderId}`);
            buyCount++;
        } else {
            log(`❌ ${r.msg || r.code}`);
        }
        await new Promise(r => setTimeout(r, 500));
    }
    
    if(bnbBalance > 0.1) {
        log('\n📤 部署卖单...');
        let sellCount = 0;
        for(const p of sellPrices) {
            log(`SELL @ ${p} = ${amount} BNB`);
            const r = await api('/api/v2/spot/trade/place-order', 'POST', {
                symbol: 'BNBUSDT', side: 'sell', force: 'GTC', orderType: 'limit',
                price: p.toString(), size: amount.toString()
            });
            if(r.code === '00000' && r.data && r.data.orderId) {
                log(`✅ ${r.data.orderId}`);
                sellCount++;
            } else {
                log(`❌ ${r.msg || r.code}`);
            }
            await new Promise(r => setTimeout(r, 500));
        }
        log(`\n✅ BNB 完成！${buyCount}买 + ${sellCount}卖`);
    } else {
        log(`\n⏳ 已部署 ${buyCount} 个买单，等待成交后创建卖单`);
    }
}

main();
