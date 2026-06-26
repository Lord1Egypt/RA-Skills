
const fs = require('fs');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const CONFIG = JSON.parse(fs.readFileSync('config.json'));
const SETTINGS = {
  "btc": {
    "symbol": "BTCUSDT",
    "gridNum": 30,
    "priceMin": 63000,
    "priceMax": 70000,
    "amount": 12,
    "maxPosition": 400,
    "notes": "2026-03-09 盈利优化：下移区间 + 加宽间距"
  },
  "sol": {
    "symbol": "SOLUSDT",
    "gridNum": 30,
    "priceMin": 75,
    "priceMax": 95,
    "amount": 15,
    "maxPosition": 400,
    "notes": "2026-03-09 盈利优化"
  },
  "eth": {
    "symbol": "ETHUSDT",
    "gridNum": 15,
    "priceMin": 1800,
    "priceMax": 2700,
    "amount": 4,
    "maxPosition": 150,
    "sellOrders": 5,
    "buyOrders": 8,
    "notes": "2026-03-09 已部署：卖单 2513-2620(5 个) | 买单 1800-2001(8 个)"
  },
  "bnb": {
    "symbol": "BNBUSDT",
    "gridNum": 10,
    "priceMin": 610,
    "priceMax": 660,
    "amount": 90,
    "maxPosition": 600,
    "sellOrders": 5,
    "buyOrders": 5,
    "notes": "2026-03-09 已调整：买单 610-625(5 个) | 卖单 640-660(5 个) | 围绕现价 630"
  },
  "optimization": {
    "date": "2026-03-09",
    "goal": "多币种分散，盈利最大化",
    "changes": [
      "新增 ETH 网格",
      "后续扩展 BNB/XRP/DOGE/AVAX"
    ]
  }
};

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

async function cancelAllOrders(symbol) {
    const orders = await api(`/api/v2/spot/trade/orders-pending?symbol=${symbol}`);
    if(orders.data && orders.data.length > 0) {
        console.log(`取消 ${symbol} ${orders.data.length} 个挂单...`);
        for(const order of orders.data) {
            await api(`/api/v2/spot/trade/cancel-order?symbol=${symbol}&orderId=${order.orderId}`, 'POST');
        }
    }
}

async function placeOrder(symbol, side, price, amount) {
    const size = (amount / price).toFixed(8);
    const body = { symbol, side, orderType: 'limit', price: price.toFixed(2), quantity: size };
    const result = await api('/api/v2/spot/trade/place-order', 'POST', body);
    return result;
}

async function deployGrid(symbol, name, buyPrices, sellPrices, amount) {
    console.log(`\n🚀 部署 ${name} 网格...`);
    
    // 取消旧订单
    await cancelAllOrders(symbol);
    
    // 部署买单
    console.log(`📥 部署 ${buyPrices.length - 1} 个买单...`);
    for(let i = 0; i < buyPrices.length - 1; i++) {
        const price = buyPrices[i];
        const result = await placeOrder(symbol, 'buy', price, amount);
        if(result.code === '00000') {
            console.log(`   ✅ 买单 ${price.toFixed(2)} OK`);
        } else {
            console.log(`   ❌ 买单 ${price.toFixed(2)} 失败：${result.msg}`);
        }
        await new Promise(r => setTimeout(r, 200));
    }
    
    // 部署卖单
    console.log(`📤 部署 ${sellPrices.length - 1} 个卖单...`);
    for(let i = 1; i < sellPrices.length; i++) {
        const price = sellPrices[i];
        const result = await placeOrder(symbol, 'sell', price, amount);
        if(result.code === '00000') {
            console.log(`   ✅ 卖单 ${price.toFixed(2)} OK`);
        } else {
            console.log(`   ❌ 卖单 ${price.toFixed(2)} 失败：${result.msg}`);
        }
        await new Promise(r => setTimeout(r, 200));
    }
    
    console.log(`✅ ${name} 网格部署完成！`);
}

async function main() {
    console.log('🚀 动态网格部署脚本\n');
    
    // 这里填入动态调整后的价格
    // 运行前请从 dynamic_adjustments.json 读取或手动填写
    
    console.log('⚠️ 请从 dynamic_adjustments.json 读取价格后手动部署');
    console.log('或联系主人确认要应用的配置');
}

main();
