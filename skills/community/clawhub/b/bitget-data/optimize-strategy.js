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
    const client = new BitgetClient({
        apiKey: process.env.BITGET_API_KEY,
        secretKey: process.env.BITGET_SECRET_KEY,
        passphrase: process.env.BITGET_PASSPHRASE,
        isSimulation: process.env.BITGET_IS_SIMULATION === 'false' ? false : true
    });

    console.log('🔧 策略优化：挂出 XRP 和 SOL 卖单\n');
    
    // 获取余额
    const balance = await client.request('/spot/account/assets', 'GET');
    const xrpData = balance.find(a => a.coin === 'XRP');
    const solData = balance.find(a => a.coin === 'SOL');
    
    const xrpaAvailable = parseFloat(xrpData?.available || 0);
    const solAvailable = parseFloat(solData?.available || 0);
    
    console.log(`XRP 可用：${xrpaAvailable}`);
    console.log(`SOL 可用：${solAvailable}\n`);
    
    // 获取当前价格
    const btcTicker = await client.request('/spot/market/tickers', 'GET', { symbol: 'BTCUSDT' });
    const ethTicker = await client.request('/spot/market/tickers', 'GET', { symbol: 'ETHUSDT' });
    const solTicker = await client.request('/spot/market/tickers', 'GET', { symbol: 'SOLUSDT' });
    const xrpTicker = await client.request('/spot/market/tickers', 'GET', { symbol: 'XRPUSDT' });
    
    const prices = {
        BTC: parseFloat(btcTicker[0]?.lastPr || 0),
        ETH: parseFloat(ethTicker[0]?.lastPr || 0),
        SOL: parseFloat(solTicker[0]?.lastPr || 0),
        XRP: parseFloat(xrpTicker[0]?.lastPr || 0)
    };
    
    console.log('当前价格:');
    console.log(`  BTC: $${prices.BTC.toFixed(2)}`);
    console.log(`  ETH: $${prices.ETH.toFixed(2)}`);
    console.log(`  SOL: $${prices.SOL.toFixed(2)}`);
    console.log(`  XRP: $${prices.XRP.toFixed(4)}\n`);
    
    let sold = 0;
    
    // XRP 卖单 - 当前价格上方 1%
    if (xrpaAvailable > 0.1) {
        const sellPrice = prices.XRP * 1.01; // 1% 利润
        const result = await client.request('/spot/trade/place-order', 'POST', {
            symbol: 'XRPUSDT',
            side: 'sell',
            force: 'GTC',
            orderType: 'limit',
            price: sellPrice.toFixed(4),
            size: xrpaAvailable.toFixed(2)
        });
        
        if (result && !result.error) {
            console.log(`✅ XRP 卖单：${xrpaAvailable.toFixed(2)} @ $${sellPrice.toFixed(4)} (+1%)`);
            sold++;
        } else {
            console.log(`❌ XRP 卖单失败：${result?.error || '未知'}`);
        }
        await sleep(200);
    }
    
    // SOL 卖单 - 当前价格上方 0.5%
    if (solAvailable > 0.01) {
        const sellPrice = prices.SOL * 1.005; // 0.5% 利润
        const result = await client.request('/spot/trade/place-order', 'POST', {
            symbol: 'SOLUSDT',
            side: 'sell',
            force: 'GTC',
            orderType: 'limit',
            price: sellPrice.toFixed(2),
            size: solAvailable.toFixed(4)
        });
        
        if (result && !result.error) {
            console.log(`✅ SOL 卖单：${solAvailable.toFixed(4)} @ $${sellPrice.toFixed(2)} (+0.5%)`);
            sold++;
        } else {
            console.log(`❌ SOL 卖单失败：${result?.error || '未知'}`);
        }
        await sleep(200);
    }
    
    console.log(`\n总计：挂出 ${sold} 个卖单`);
    console.log('\n💡 策略建议:');
    console.log('  1. 降低 BTC 仓位至 250 USDT (释放 50)');
    console.log('  2. 降低 SOL 仓位至 180 USDT (释放 20)');
    console.log('  3. 降低 XRP 仓位至 120 USDT (释放 30)');
    console.log('  4. 部署 ETH 网格 150 USDT');
    console.log('  5. 保留 100 USDT 备用金');
}

main().catch(console.error);
