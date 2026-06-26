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

async function main() {
    const config = {
        apiKey: process.env.BITGET_API_KEY,
        secretKey: process.env.BITGET_SECRET_KEY,
        passphrase: process.env.BITGET_PASSPHRASE,
        isSimulation: process.env.BITGET_IS_SIMULATION === 'false' ? false : true
    };

    const client = new BitgetClient(config);

    console.log('📊 手动部署 ETH 网格...\n');
    
    const symbol = 'ETHUSDT';
    const currentPrice = 1990.58;
    const priceMin = 1900;
    const priceMax = 2100;
    const gridNum = 30;
    const amount = 10;
    
    const gridStep = (priceMax - priceMin) / gridNum;
    console.log(`当前价格：${currentPrice}`);
    console.log(`网格间距：${gridStep.toFixed(4)}`);
    console.log(`\n计算买单价格:\n`);
    
    let placed = 0;
    for (let i = gridNum; i >= 0; i--) {
        const price = priceMin + (gridStep * i);
        if (price >= currentPrice) {
            console.log(`${price.toFixed(2)} >= ${currentPrice} - 跳过`);
            continue;
        }
        
        const buyAmount = amount / price;
        console.log(`${price.toFixed(2)} < ${currentPrice} - 应该下单 ${buyAmount.toFixed(6)}`);
        
        if (placed >= 15) {
            console.log('  达到限制，停止\n');
            break;
        }
        
        const result = await client.request('/spot/trade/place-order', 'POST', {
            symbol: symbol,
            side: 'buy',
            force: 'GTC',
            orderType: 'limit',
            price: price.toFixed(2),
            size: buyAmount.toFixed(6)
        });
        
        if (result && !result.error) {
            console.log(`  ✅ 下单成功\n`);
            placed++;
        } else {
            console.log(`  ❌ 下单失败：${result?.error || '未知错误'}\n`);
        }
        
        await sleep(200);
    }
    
    console.log(`\n总计：${placed} 个订单`);
}

main().catch(console.error);
