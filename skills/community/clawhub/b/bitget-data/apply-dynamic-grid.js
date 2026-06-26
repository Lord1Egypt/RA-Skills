
const fs = require('fs');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const CONFIG = JSON.parse(fs.readFileSync('config.json'));
const ADJUSTMENTS = JSON.parse(fs.readFileSync('dynamic_adjustments.json'));

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

async function cancelOrders(symbol) {
    const pending = await api(`/api/v2/spot/trade/orders-pending?symbol=${symbol}`);
    if(pending.data && pending.data.length > 0) {
        console.log(`取消 ${symbol} ${pending.data.length} 个挂单...`);
        for(const order of pending.data) {
            await api(`/api/v2/spot/trade/cancel-order?symbol=${symbol}&orderId=${order.orderId}`, 'POST');
        }
        await new Promise(r => setTimeout(r, 500));
    }
}

async function placeOrder(symbol, side, price, amount) {
    const size = (amount / price).toFixed(6);
    const body = { symbol, side, orderType: 'limit', price: price.toFixed(2), quantity: size };
    const result = await api('/api/v2/spot/trade/place-order', 'POST', body);
    return result;
}

async function deployGrid(symbol, config) {
    console.log(`\n🚀 部署 ${symbol} 动态网格...`);
    
    await cancelOrders(symbol);
    
    console.log(`📥 部署 ${config.buyOrders} 个买单...`);
    for(const price of config.buyPrices) {
        const result = await placeOrder(symbol, 'buy', price, config.amount);
        if(result.code === '00000') {
            console.log(`   ✅ ${price.toFixed(2)}`);
        } else {
            console.log(`   ⚠️  ${price.toFixed(2)}: ${result.msg || '失败'}`);
        }
        await new Promise(r => setTimeout(r, 300));
    }
    
    console.log(`📤 部署 ${config.sellOrders} 个卖单...`);
    for(const price of config.sellPrices) {
        const result = await placeOrder(symbol, 'sell', price, config.amount);
        if(result.code === '00000') {
            console.log(`   ✅ ${price.toFixed(2)}`);
        } else {
            console.log(`   ⚠️  ${price.toFixed(2)}: ${result.msg || '失败'}`);
        }
        await new Promise(r => setTimeout(r, 300));
    }
    
    console.log(`✅ ${symbol} 部署完成！`);
}

async function main() {
    const target = process.argv[2] || 'ALL';
    const adj = ADJUSTMENTS.adjustments;
    
    console.log('🚀 应用动态网格配置\n');
    
    if(target === 'ALL' || target === 'BTC') {
        if(adj.btc) await deployGrid('BTCUSDT', adj.btc);
    }
    if(target === 'ALL' || target === 'SOL') {
        if(adj.sol) await deployGrid('SOLUSDT', adj.sol);
    }
    if(target === 'ALL' || target === 'ETH') {
        if(adj.eth) await deployGrid('ETHUSDT', adj.eth);
    }
    
    console.log('\n✅ 所有网格部署完成！\n');
}

main().catch(console.error);
