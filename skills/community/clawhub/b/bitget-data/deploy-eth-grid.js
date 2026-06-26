#!/usr/bin/env node
const fs = require('fs');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const CONFIG = JSON.parse(fs.readFileSync('config.json'));
const SYMBOL = 'ETHUSDT';
const GRID_NUM = 15;
const PRICE_MIN = 2300;
const PRICE_MAX = 2700;
const AMOUNT_PER_GRID = 4; // USDT

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
    log('🚀 部署 ETHUSDT 网格...');
    
    // 获取价格和持仓
    const [ticker, assets] = await Promise.all([
        api('/api/v2/spot/market/ticker?symbol=ETHUSDT'),
        api('/api/v2/spot/account/assets', 'GET')
    ]);
    
    let price = 2500;
    if(ticker.data && ticker.data.last) {
        price = parseFloat(ticker.data.last);
        log(`✅ ETH 当前价格：${price} USDT`);
    }
    
    let ethBalance = 0;
    if(assets.code === '00000' && assets.data) {
        const eth = assets.data.find(a => a.coin === 'ETH');
        if(eth) ethBalance = parseFloat(eth.available);
        log(`✅ ETH 可用余额：${ethBalance.toFixed(4)} ETH`);
    }
    
    const spacing = (PRICE_MAX - PRICE_MIN) / GRID_NUM;
    log(`\n📋 网格配置:`);
    log(`   区间：${PRICE_MIN} - ${PRICE_MAX} USDT`);
    log(`   格数：${GRID_NUM} | 间距：${spacing.toFixed(1)} USDT (${(spacing/price*100).toFixed(2)}%)`);
    log(`   每格：${AMOUNT_PER_GRID} USDT`);
    
    // 计算当前价格在哪一格
    const currentGrid = Math.floor((price - PRICE_MIN) / spacing);
    log(`   当前价位于：第 ${currentGrid} 格`);
    
    // 创建买单（价格低于当前价）
    log('\n📥 创建买单...');
    let buyCount = 0;
    for(let i = currentGrid - 1; i >= 0 && buyCount < 5; i--) {
        const p = (PRICE_MIN + i * spacing).toFixed(1);
        const q = (AMOUNT_PER_GRID / p).toFixed(4);
        log(`BUY @ ${p} = ${q} ETH`);
        
        const r = await api('/api/v2/spot/trade/place-order', 'POST', {
            symbol: SYMBOL, side: 'buy', force: 'GTC', orderType: 'limit', price: p, size: q
        });
        
        if(r.code === '00000' && r.data && r.data.orderId) {
            log(`✅ ${r.data.orderId}`);
            buyCount++;
        } else {
            log(`❌ ${r.msg || r.code || r.error}`);
        }
        await new Promise(r => setTimeout(r, 400));
    }
    
    // 创建卖单（价格高于当前价）
    log('\n📤 创建卖单...');
    let sellCount = 0;
    for(let i = currentGrid + 1; i < GRID_NUM && sellCount < 5; i++) {
        const p = (PRICE_MIN + i * spacing).toFixed(1);
        const q = (AMOUNT_PER_GRID / p).toFixed(4);
        log(`SELL @ ${p} = ${q} ETH`);
        
        const r = await api('/api/v2/spot/trade/place-order', 'POST', {
            symbol: SYMBOL, side: 'sell', force: 'GTC', orderType: 'limit', price: p, size: q
        });
        
        if(r.code === '00000' && r.data && r.data.orderId) {
            log(`✅ ${r.data.orderId}`);
            sellCount++;
        } else {
            log(`❌ ${r.msg || r.code || r.error}`);
        }
        await new Promise(r => setTimeout(r, 400));
    }
    
    log(`\n✅ ETH 网格部署完成！`);
    log(`   买单：${buyCount} 个 | 卖单：${sellCount} 个 | 总计：${buyCount + sellCount} 个订单`);
    log(`   投入：约 ${buyCount * AMOUNT_PER_GRID} USDT (买) + ${sellCount * AMOUNT_PER_GRID} USDT (卖)`);
}

main();
