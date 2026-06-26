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
                        console.error('API Response:', JSON.stringify(json).slice(0, 500));
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

async function main() {
    const config = {
        apiKey: process.env.BITGET_API_KEY,
        secretKey: process.env.BITGET_SECRET_KEY,
        passphrase: process.env.BITGET_PASSPHRASE,
        isSimulation: process.env.BITGET_IS_SIMULATION === 'false' ? false : true
    };

    const client = new BitgetClient(config);

    console.log('🔍 获取 BTC 和 ETH 行情...\n');
    
    // 获取 BTC 和 ETH 价格
    const btcTicker = await client.request('/spot/market/tickers?symbol=BTCUSDT', 'GET');
    const ethTicker = await client.request('/spot/market/tickers?symbol=ETHUSDT', 'GET');
    const solTicker = await client.request('/spot/market/tickers?symbol=SOLUSDT', 'GET');
    const xrpTicker = await client.request('/spot/market/tickers?symbol=XRPUSDT', 'GET');
    const bnbTicker = await client.request('/spot/market/tickers?symbol=BNBUSDT', 'GET');

    console.log('\n📊 主流币种行情:\n');
    console.log('币种          价格          24h 涨跌    24h 最高    24h 最低    波动率');
    console.log('='.repeat(75));

    const tickers = [btcTicker, ethTicker, solTicker, xrpTicker, bnbTicker].filter(t => t && !t.error);
    
    tickers.forEach(t => {
        if (Array.isArray(t)) t = t[0];
        const symbol = t.symbol.replace('USDT', '');
        const price = parseFloat(t.lastPr || 0);
        const change = parseFloat(t.chgUTC || 0);
        const high = parseFloat(t.high24h || 0);
        const low = parseFloat(t.low24h || 0);
        const volatility = ((high - low) / price * 100).toFixed(2);
        const changeStr = change >= 0 ? `+${change.toFixed(2)}%` : `${change.toFixed(2)}%`;
        const priceStr = price < 1 ? `$${price.toFixed(4)}` : `$${price.toFixed(2)}`;
        
        console.log(`${symbol.padEnd(12)} ${priceStr.padEnd(14)} ${changeStr.padEnd(10)} $${high.toFixed(2).padEnd(9)} $${low.toFixed(2).padEnd(9)} ${volatility}%`);
    });
}

main().catch(console.error);
