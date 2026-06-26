#!/usr/bin/env node
/**
 * 应用方案 A - 保守调整
 * 仅调整买卖单比例，不改变区间
 */

const fs = require('fs');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const CONFIG = JSON.parse(fs.readFileSync('config.json', 'utf-8'));

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

async function getPendingOrders(symbol) {
    const result = await api(`/api/v2/spot/trade/orders-pending?symbol=${symbol}`);
    if(result.code === '00000' && result.data) {
        return result.data;
    }
    return [];
}

async function cancelOrder(symbol, orderId) {
    const result = await api(`/api/v2/spot/trade/cancel-order?symbol=${symbol}&orderId=${orderId}`, 'POST');
    return result;
}

async function cancelAllOrders(symbol) {
    console.log(`\n📋 获取 ${symbol} 挂单...`);
    const orders = await getPendingOrders(symbol);
    
    if(orders.length === 0) {
        console.log(`   ✅ 无挂单`);
        return 0;
    }
    
    console.log(`   找到 ${orders.length} 个挂单，开始取消...`);
    let cancelled = 0;
    
    for(const order of orders) {
        const result = await cancelOrder(symbol, order.orderId);
        if(result.code === '00000') {
            cancelled++;
            console.log(`   ✅ 取消 ${order.side} ${order.price}`);
        } else {
            console.log(`   ⚠️ 取消失败：${result.msg}`);
        }
        await new Promise(r => setTimeout(r, 200));
    }
    
    return cancelled;
}

async function placeOrder(symbol, side, price, amount) {
    const size = (amount / price).toFixed(6);
    const body = {
        symbol,
        side,
        orderType: 'limit',
        price: price.toFixed(2),
        quantity: size,
        force: 'normal'
    };
    
    const result = await api('/api/v2/spot/trade/place-order', 'POST', body);
    return result;
}

async function deployGrid(symbol, name, buyConfig, sellConfig, amount) {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`🚀 部署 ${name} (${symbol}) 动态网格`);
    console.log('='.repeat(60));
    
    // 取消旧订单
    const cancelled = await cancelAllOrders(symbol);
    
    // 等待 2 秒
    console.log(`\n⏳ 等待 2 秒...`);
    await new Promise(r => setTimeout(r, 2000));
    
    // 部署买单
    console.log(`\n📥 部署 ${buyConfig.count} 个买单...`);
    let buySuccess = 0;
    for(let i = 0; i < buyConfig.prices.length; i++) {
        const price = buyConfig.prices[i];
        const result = await placeOrder(symbol, 'buy', price, amount);
        if(result.code === '00000') {
            buySuccess++;
            console.log(`   ✅ #${i+1} ${price.toFixed(2)} @ ${amount} USDT`);
        } else if(result.code === '20011' || result.msg?.includes('price precision')) {
            // 价格精度问题，调整小数位
            const adjustedPrice = parseFloat(price.toFixed(symbol.includes('BTC') ? 1 : 2));
            const result2 = await placeOrder(symbol, 'buy', adjustedPrice, amount);
            if(result2.code === '00000') {
                buySuccess++;
                console.log(`   ✅ #${i+1} ${adjustedPrice.toFixed(2)} @ ${amount} USDT (精度调整)`);
            } else {
                console.log(`   ❌ #${i+1} ${price.toFixed(2)}: ${result2.msg || result2.code}`);
            }
        } else {
            console.log(`   ❌ #${i+1} ${price.toFixed(2)}: ${result.msg || result.code}`);
        }
        await new Promise(r => setTimeout(r, 300));
    }
    
    // 部署卖单
    console.log(`\n📤 部署 ${sellConfig.count} 个卖单...`);
    let sellSuccess = 0;
    for(let i = 0; i < sellConfig.prices.length; i++) {
        const price = sellConfig.prices[i];
        const result = await placeOrder(symbol, 'sell', price, amount);
        if(result.code === '00000') {
            sellSuccess++;
            console.log(`   ✅ #${i+1} ${price.toFixed(2)} @ ${amount} USDT`);
        } else if(result.code === '20011' || result.msg?.includes('price precision')) {
            const adjustedPrice = parseFloat(price.toFixed(symbol.includes('BTC') ? 1 : 2));
            const result2 = await placeOrder(symbol, 'sell', adjustedPrice, amount);
            if(result2.code === '00000') {
                sellSuccess++;
                console.log(`   ✅ #${i+1} ${adjustedPrice.toFixed(2)} @ ${amount} USDT (精度调整)`);
            } else {
                console.log(`   ❌ #${i+1} ${price.toFixed(2)}: ${result2.msg || result2.code}`);
            }
        } else {
            console.log(`   ❌ #${i+1} ${price.toFixed(2)}: ${result.msg || result.code}`);
        }
        await new Promise(r => setTimeout(r, 300));
    }
    
    console.log(`\n${'='.repeat(60)}`);
    console.log(`✅ ${name} 部署完成！`);
    console.log(`   买单成功：${buySuccess}/${buyConfig.count}`);
    console.log(`   卖单成功：${sellSuccess}/${sellConfig.count}`);
    console.log(`   总计：${buySuccess + sellSuccess} 个订单`);
    console.log('='.repeat(60));
    
    return { buy: buySuccess, sell: sellSuccess, total: buySuccess + sellSuccess };
}

async function main() {
    console.log('🔄 方案 A - 保守调整（动态买卖比例）\n');
    console.log('时间:', new Date().toLocaleString('zh-CN'));
    console.log('策略：根据 RSI 调整买卖单密度，不改变区间\n');
    
    const results = {
        time: new Date().toISOString(),
        scheme: 'A',
        deployments: {}
    };
    
    // BTC 配置
    console.log('\n' + '='.repeat(60));
    console.log('📊 BTCUSDT - 比特币');
    console.log('='.repeat(60));
    console.log('RSI: ~65 偏多 | 比例：40% 买 : 60% 卖');
    const btcResult = await deployGrid(
        'BTCUSDT',
        '比特币',
        {
            count: 12,
            prices: [65000, 65500, 66000, 66500, 67000, 67500, 68000, 68500, 69000, 69200, 69400, 69600]
        },
        {
            count: 18,
            prices: [69800, 70000, 70200, 70400, 70600, 70800, 71000, 71200, 71400, 71600, 71800, 72000, 72200, 72400, 72600, 72800, 73000, 73200]
        },
        12
    );
    results.deployments.btc = btcResult;
    
    // SOL 配置
    console.log('\n' + '='.repeat(60));
    console.log('📊 SOLUSDT - Solana');
    console.log('='.repeat(60));
    console.log('RSI: ~68 偏多 | 比例：40% 买 : 60% 卖');
    const solResult = await deployGrid(
        'SOLUSDT',
        'Solana',
        {
            count: 12,
            prices: [80, 81, 82, 83, 84, 84.5, 85, 85.2, 85.4, 85.6, 85.8, 86]
        },
        {
            count: 18,
            prices: [86.2, 86.5, 87, 87.5, 88, 88.5, 89, 89.5, 90, 90.5, 91, 91.5, 92, 92.5, 93, 93.5, 94, 94.5]
        },
        15
    );
    results.deployments.sol = solResult;
    
    // ETH 配置
    console.log('\n' + '='.repeat(60));
    console.log('📊 ETHUSDT - 以太坊');
    console.log('='.repeat(60));
    console.log('RSI: ~58 中性 | 比例：50% 买 : 50% 卖');
    const ethResult = await deployGrid(
        'ETHUSDT',
        '以太坊',
        {
            count: 10,
            prices: [1900, 1920, 1940, 1960, 1980, 2000, 2010, 2015, 2020, 2025]
        },
        {
            count: 10,
            prices: [2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100, 2120, 2140]
        },
        5
    );
    results.deployments.eth = ethResult;
    
    // 汇总
    console.log('\n' + '='.repeat(60));
    console.log('📋 部署汇总');
    console.log('='.repeat(60));
    
    const totalOrders = btcResult.total + solResult.total + ethResult.total;
    console.log(`\nBTC: ${btcResult.buy}买 + ${btcResult.sell}卖 = ${btcResult.total}个`);
    console.log(`SOL: ${solResult.buy}买 + ${solResult.sell}卖 = ${solResult.total}个`);
    console.log(`ETH: ${ethResult.buy} + ${ethResult.sell}卖 = ${ethResult.total}个`);
    console.log(`\n总计：${totalOrders} 个订单`);
    
    // 保存结果
    results.totalOrders = totalOrders;
    fs.writeFileSync('scheme_a_result.json', JSON.stringify(results, null, 2), 'utf-8');
    
    console.log('\n' + '='.repeat(60));
    console.log('✅ 方案 A 执行完成！');
    console.log('='.repeat(60));
    console.log('\n💡 下一步:');
    console.log('1. 检查订单状态：node check-orders.js');
    console.log('2. 查看监控日志：tail -f grid_monitor.log');
    console.log('3. 结果已保存：scheme_a_result.json');
    console.log('\n🎉 祝主人网格大赚！💰\n');
}

main().catch(err => {
    console.error('❌ 执行错误:', err);
    process.exit(1);
});
