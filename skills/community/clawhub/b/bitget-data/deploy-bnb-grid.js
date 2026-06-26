#!/usr/bin/env node
const fs = require('fs');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const CONFIG = JSON.parse(fs.readFileSync('config.json'));
const SYMBOL = 'BNBUSDT';

// BNB 网格配置 - 参考 ETH 策略
// 假设当前价 ~380，买单挂在 350-375，卖单挂在 385-410
const BUY_PRICE_MAX = 375;
const BUY_PRICE_MIN = 350;
const BUY_NUM = 5;
const SELL_PRICE_MIN = 385;
const SELL_PRICE_MAX = 410;
const SELL_NUM = 5;
const AMOUNT = 20; // USDT per grid

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
    log('🚀 部署 BNBUSDT 网格...');
    
    // 检查持仓
    const assets = await api('/api/v2/spot/account/assets', 'GET');
    let bnbBalance = 0;
    if(assets.code === '00000' && assets.data) {
        const bnb = assets.data.find(a => a.coin === 'BNB');
        if(bnb) bnbBalance = parseFloat(bnb.available);
        log(`BNB 可用余额：${bnbBalance.toFixed(4)} BNB`);
    }
    
    // 创建买单
    log('\n📥 创建买单...');
    const buySpacing = (BUY_PRICE_MAX - BUY_PRICE_MIN) / BUY_NUM;
    let buyCount = 0;
    
    for(let i = BUY_NUM - 1; i >= 0; i--) {
        const p = (BUY_PRICE_MIN + i * buySpacing).toFixed(1);
        const q = (AMOUNT / p).toFixed(3);
        log(`BUY @ ${p} = ${q} BNB`);
        
        const r = await api('/api/v2/spot/trade/place-order', 'POST', {
            symbol: SYMBOL, side: 'buy', force: 'GTC', orderType: 'limit', price: p, size: q
        });
        
        if(r.code === '00000' && r.data && r.data.orderId) {
            log(`✅ ${r.data.orderId}`);
            buyCount++;
        } else {
            log(`❌ ${r.msg || r.code}`);
        }
        await new Promise(r => setTimeout(r, 400));
    }
    
    // 如果有持仓，创建卖单
    if(bnbBalance > 0.01) {
        log('\n📤 创建卖单...');
        const sellSpacing = (SELL_PRICE_MAX - SELL_PRICE_MIN) / SELL_NUM;
        let sellCount = 0;
        
        for(let i = 0; i < SELL_NUM; i++) {
            const p = (SELL_PRICE_MIN + i * sellSpacing).toFixed(1);
            const q = (AMOUNT / p).toFixed(3);
            log(`SELL @ ${p} = ${q} BNB`);
            
            const r = await api('/api/v2/spot/trade/place-order', 'POST', {
                symbol: SYMBOL, side: 'sell', force: 'GTC', orderType: 'limit', price: p, size: q
            });
            
            if(r.code === '00000' && r.data && r.data.orderId) {
                log(`✅ ${r.data.orderId}`);
                sellCount++;
            } else {
                log(`❌ ${r.msg || r.code}`);
            }
            await new Promise(r => setTimeout(r, 400));
        }
        
        log(`\n✅ BNB 网格完成！${buyCount}买 + ${sellCount}卖`);
    } else {
        log(`\n⏳ BNB 买单已部署，等待成交后自动创建卖单`);
        log(`💡 当前无 BNB 持仓，只创建了 ${buyCount} 个买单`);
    }
}

main();
