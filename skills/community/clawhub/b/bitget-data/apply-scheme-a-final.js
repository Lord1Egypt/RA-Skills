#!/usr/bin/env node
/**
 * 方案 A - 保守调整 FINAL V2
 * 使用正确的 API 格式 (基于 cancel-all.js)
 */

const fs = require('fs');
const https = require('https');
const crypto = require('crypto');

const CONFIG = JSON.parse(fs.readFileSync('config.json', 'utf-8'));

class BitgetClient {
    constructor(config) {
        this.apiKey = config.apiKey;
        this.secretKey = config.secretKey;
        this.passphrase = config.passphrase;
    }

    request(endpoint, method = 'GET', params = '') {
        return new Promise((resolve) => {
            const now = new Date();
            const timestamp = now.toISOString().split('.')[0] + '.000Z';
            let pathStr = endpoint;
            let body = '';

            if (method === 'GET' && typeof params === 'object' && Object.keys(params).length > 0) {
                pathStr += '?' + new URLSearchParams(params).toString();
            } else if (method === 'POST') {
                body = typeof params === 'string' ? params : JSON.stringify(params);
            }

            const fullpath = pathStr.startsWith('/api') ? pathStr : '/api/v2' + pathStr;
            const signStr = timestamp + method + fullpath + body;
            const signature = crypto.createHmac('sha256', this.secretKey).update(signStr).digest('base64');

            const options = {
                hostname: 'api.bitget.com',
                port: 443,
                path: fullpath,
                method: method,
                headers: {
                    'ACCESS-KEY': this.apiKey,
                    'ACCESS-SIGN': signature,
                    'ACCESS-TIMESTAMP': timestamp,
                    'ACCESS-PASSPHRASE': this.passphrase,
                    'Content-Type': 'application/json'
                }
            };

            const req = https.request(options, res => {
                let data = '';
                res.on('data', c => data += c);
                res.on('end', () => {
                    try { resolve(JSON.parse(data)); }
                    catch(e) { resolve({raw: data}); }
                });
            });
            req.on('error', e => resolve({error: e.message}));
            if (body) req.write(body);
            req.end();
        });
    }
}

const client = new BitgetClient(CONFIG);

async function getPrice(symbol) {
    const result = await client.request('/spot/market/tickers', 'GET', { symbol });
    if(result.code === '00000' && result.data) {
        return parseFloat(result.data.last);
    }
    return 0;
}

async function getPendingOrders(symbol) {
    const result = await client.request('/spot/trade/unfilled-orders', 'GET', { symbol });
    if(result.code === '00000' && result.data) {
        return result.data;
    }
    return [];
}

async function cancelOrder(symbol, orderId) {
    const result = await client.request('/spot/trade/cancel-order', 'POST', {
        symbol,
        orderId
    });
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
            console.log(`   ⚠️ 取消失败：${result.msg || result.code}`);
        }
        await new Promise(r => setTimeout(r, 300));
    }
    
    return cancelled;
}

async function placeOrder(symbol, side, price, amount) {
    const size = (amount / price).toFixed(6);
    const result = await client.request('/spot/trade/place-order', 'POST', {
        symbol,
        side,
        orderType: 'limit',
        price: price.toFixed(2),
        size,
        force: 'GTC'
    });
    return result;
}

async function deployGrid(symbol, name, buyConfig, sellConfig, amount) {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`🚀 部署 ${name} (${symbol}) 动态网格`);
    console.log('='.repeat(60));
    
    // 获取当前价格
    const price = await getPrice(symbol);
    if(price > 0) {
        console.log(`📈 当前价格：${price.toFixed(2)} USDT`);
    }
    
    // 取消旧订单
    const cancelled = await cancelAllOrders(symbol);
    
    // 等待 2 秒
    console.log(`\n⏳ 等待 2 秒...`);
    await new Promise(r => setTimeout(r, 2000));
    
    // 部署买单
    console.log(`\n📥 部署 ${buyConfig.count} 个买单...`);
    let buySuccess = 0;
    for(let i = 0; i < buyConfig.prices.length; i++) {
        const p = buyConfig.prices[i];
        const result = await placeOrder(symbol, 'buy', p, amount);
        if(result.code === '00000' && result.data) {
            buySuccess++;
            console.log(`   ✅ #${i+1} ${p.toFixed(2)} @ ${amount} USDT [${result.data.orderId}]`);
        } else if(result.code === '20011' || (result.msg && result.msg.includes('price precision'))) {
            // 价格精度问题
            const decimals = symbol.includes('BTC') || symbol.includes('ETH') ? 0 : 2;
            const adjustedPrice = parseFloat(p.toFixed(decimals));
            const result2 = await placeOrder(symbol, 'buy', adjustedPrice, amount);
            if(result2.code === '00000' && result2.data) {
                buySuccess++;
                console.log(`   ✅ #${i+1} ${adjustedPrice.toFixed(2)} @ ${amount} USDT (精度调整) [${result2.data.orderId}]`);
            } else {
                console.log(`   ❌ #${i+1} ${p.toFixed(2)}: ${result2.msg || result2.code}`);
            }
        } else {
            console.log(`   ❌ #${i+1} ${p.toFixed(2)}: ${result.msg || result.code || '未知错误'}`);
        }
        await new Promise(r => setTimeout(r, 400));
    }
    
    // 部署卖单
    console.log(`\n📤 部署 ${sellConfig.count} 个卖单...`);
    let sellSuccess = 0;
    for(let i = 0; i < sellConfig.prices.length; i++) {
        const p = sellConfig.prices[i];
        const result = await placeOrder(symbol, 'sell', p, amount);
        if(result.code === '00000' && result.data) {
            sellSuccess++;
            console.log(`   ✅ #${i+1} ${p.toFixed(2)} @ ${amount} USDT [${result.data.orderId}]`);
        } else if(result.code === '20011' || (result.msg && result.msg.includes('price precision'))) {
            const decimals = symbol.includes('BTC') || symbol.includes('ETH') ? 0 : 2;
            const adjustedPrice = parseFloat(p.toFixed(decimals));
            const result2 = await placeOrder(symbol, 'sell', adjustedPrice, amount);
            if(result2.code === '00000' && result2.data) {
                sellSuccess++;
                console.log(`   ✅ #${i+1} ${adjustedPrice.toFixed(2)} @ ${amount} USDT (精度调整) [${result2.data.orderId}]`);
            } else {
                console.log(`   ❌ #${i+1} ${p.toFixed(2)}: ${result2.msg || result2.code}`);
            }
        } else {
            console.log(`   ❌ #${i+1} ${p.toFixed(2)}: ${result.msg || result.code || '未知错误'}`);
        }
        await new Promise(r => setTimeout(r, 400));
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
    console.log('🔄 方案 A - 保守调整（动态买卖比例）FINAL V2\n');
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
    console.log(`ETH: ${ethResult.buy}买 + ${ethResult.sell}卖 = ${ethResult.total}个`);
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
