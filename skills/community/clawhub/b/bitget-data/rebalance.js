#!/usr/bin/env node

const crypto = require('crypto');
const https = require('https');

let HttpsProxyAgent = null;
try {
    HttpsProxyAgent = require('https-proxy-agent').HttpsProxyAgent;
} catch (e) {}

class BitgetClient {
    constructor(config = {}) {
        this.apiKey = config.apiKey || process.env.BITGET_API_KEY;
        this.secretKey = config.secretKey || process.env.BITGET_SECRET_KEY;
        this.passphrase = config.passphrase || process.env.BITGET_PASSPHRASE;
        const isSim = config.isSimulation !== undefined ? config.isSimulation : process.env.BITGET_IS_SIMULATION;
        this.isSimulation = isSim === true || isSim === 'true';
        
        const proxyUrl = process.env.HTTPS_PROXY || process.env.https_proxy;
        if (HttpsProxyAgent && proxyUrl) {
            this.agent = new HttpsProxyAgent(proxyUrl);
        } else {
            this.agent = null;
        }
    }

    request(endpoint, method = 'GET', params = '') {
        return new Promise((resolve, reject) => {
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
                agent: this.agent,
                headers: {
                    'ACCESS-KEY': this.apiKey,
                    'ACCESS-SIGN': signature,
                    'ACCESS-TIMESTAMP': timestamp,
                    'ACCESS-PASSPHRASE': this.passphrase,
                    'x-bitget-simulated-trading': this.isSimulation ? '1' : '0',
                    'Content-Type': 'application/json'
                }
            };

            const req = https.request(options, res => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        const json = JSON.parse(data);
                        if (json.code === '00000') resolve(json.data);
                        else resolve({ error: json.msg || json.message, code: json.code });
                    } catch (e) {
                        resolve({ error: 'JSON Parse Error', raw: data });
                    }
                });
            });

            req.on('error', (e) => reject(e));
            if (body) req.write(typeof body === 'string' ? body : JSON.stringify(body));
            req.end();
        });
    }
}

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function cancelAllOrders(symbol) {
    const orders = await client.request('/spot/trade/unfilled-orders', 'GET', { symbol });
    if (orders.error || !Array.isArray(orders)) return 0;
    
    let cancelled = 0;
    for (const order of orders) {
        const result = await client.request('/spot/trade/cancel-order', 'POST', {
            symbol: symbol,
            orderId: order.orderId
        });
        if (result && !result.error) cancelled++;
        await sleep(100);
    }
    return cancelled;
}

async function main() {
    global.client = new BitgetClient({
        apiKey: process.env.BITGET_API_KEY,
        secretKey: process.env.BITGET_SECRET_KEY,
        passphrase: process.env.BITGET_PASSPHRASE,
        isSimulation: process.env.BITGET_IS_SIMULATION === 'false' ? false : true
    });

    console.log('🔄 资金重新分配 - 优化策略\n');
    console.log('⚠️  警告：此操作将取消所有订单并释放资金！\n');
    
    // 获取当前余额
    const balance = await client.request('/spot/account/assets', 'GET');
    const usdt = balance.find(a => a.coin === 'USDT');
    const btc = balance.find(a => a.coin === 'BTC');
    const sol = balance.find(a => a.coin === 'SOL');
    const xrp = balance.find(a => a.coin === 'XRP');
    
    console.log('📊 当前余额:');
    console.log(`  USDT: ${usdt ? parseFloat(usdt.available).toFixed(2) : 0} (冻结：${usdt ? parseFloat(usdt.frozen).toFixed(2) : 0})`);
    console.log(`  BTC: ${btc ? parseFloat(btc.available).toFixed(6) : 0}`);
    console.log(`  SOL: ${sol ? parseFloat(sol.available).toFixed(6) : 0}`);
    console.log(`  XRP: ${xrp ? parseFloat(xrp.available).toFixed(6) : 0}`);
    console.log('');
    
    console.log('🎯 优化目标:');
    console.log('  BTC: 250 USDT (当前 ~300)');
    console.log('  SOL: 150 USDT (当前 ~200)');
    console.log('  XRP: 100 USDT (当前 ~120)');
    console.log('  ETH: 150 USDT (新增)');
    console.log('  备用：150 USDT (当前 ~14)');
    console.log('');
    
    console.log('⚡ 执行步骤:');
    console.log('  1. 取消所有订单');
    console.log('  2. 等待资金释放');
    console.log('  3. 按新配置部署网格');
    console.log('');
    
    const confirm = process.argv.includes('--confirm');
    if (!confirm) {
        console.log('💡 使用 --confirm 参数执行此操作');
        console.log('   node rebalance.js --confirm\n');
        return;
    }
    
    // 取消所有订单
    console.log('📤 取消订单中...\n');
    
    const symbols = ['BTCUSDT', 'SOLUSDT', 'XRPUSDT', 'ETHUSDT'];
    let totalCancelled = 0;
    
    for (const symbol of symbols) {
        const cancelled = await cancelAllOrders(symbol);
        console.log(`  ${symbol}: 取消 ${cancelled} 个订单`);
        totalCancelled += cancelled;
        await sleep(200);
    }
    
    console.log(`\n✅ 总计：取消 ${totalCancelled} 个订单`);
    
    console.log('\n⏳ 等待资金释放 (10 秒)...');
    await sleep(10000);
    
    // 获取新余额
    const newBalance = await client.request('/spot/account/assets', 'GET');
    const newUsdt = newBalance.find(a => a.coin === 'USDT');
    
    console.log('\n💰 新余额:');
    console.log(`  USDT: ${newUsdt ? parseFloat(newUsdt.available).toFixed(2) : 0} (冻结：${newUsdt ? parseFloat(newUsdt.frozen).toFixed(2) : 0})`);
    
    console.log('\n✅ 资金重新分配完成！');
    console.log('\n📋 下一步:');
    console.log('  1. 更新 grid_settings.json');
    console.log('  2. 运行 multi-grid-bot.js 部署新网格');
    console.log('  3. 运行 report.js 验证');
}

main().catch(console.error);
