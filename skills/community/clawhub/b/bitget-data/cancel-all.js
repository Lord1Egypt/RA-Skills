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

async function cancelAll(symbol) {
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

    console.log('🔄 取消所有订单...\n');
    
    const symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT'];
    let total = 0;
    
    for (const symbol of symbols) {
        const cancelled = await cancelAll(symbol);
        console.log(`${symbol}: 取消 ${cancelled} 个订单`);
        total += cancelled;
    }
    
    console.log(`\n✅ 总计：取消 ${total} 个订单`);
    
    console.log('\n⏳ 等待资金释放 (5 秒)...');
    await sleep(5000);
    
    const balance = await client.request('/spot/account/assets', 'GET');
    const usdt = balance.find(a => a.coin === 'USDT');
    console.log(`\n💰 USDT 余额：${usdt ? usdt.available : 0} (冻结：${usdt ? usdt.frozen : 0})`);
}

main().catch(console.error);
