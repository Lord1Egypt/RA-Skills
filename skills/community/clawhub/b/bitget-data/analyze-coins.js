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

            const fullpath = '/api/v2' + pathStr;
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

async function main() {
    const config = {
        apiKey: process.env.BITGET_API_KEY,
        secretKey: process.env.BITGET_SECRET_KEY,
        passphrase: process.env.BITGET_PASSPHRASE,
        isSimulation: process.env.BITGET_IS_SIMULATION === 'false' ? false : true
    };

    const client = new BitgetClient(config);

    console.log('🔍 获取热门币种行情...\n');
    
    // 获取所有 USDT 交易对
    const tickers = await client.request('/spot/market/tickers', 'GET');
    
    if (tickers.error) {
        console.log('❌ 获取失败:', tickers.error);
        return;
    }

    // 筛选 USDT 交易对，按 24h 成交量排序
    const usdtPairs = tickers
        .filter(t => t.symbol && t.symbol.endsWith('USDT'))
        .map(t => ({
            symbol: t.symbol,
            price: parseFloat(t.lastPr || 0),
            change24h: parseFloat(t.chgUTC || 0),
            volume24h: parseFloat(t.quoteVol || 0),
            high24h: parseFloat(t.high24h || 0),
            low24h: parseFloat(t.low24h || 0)
        }))
        .filter(t => t.price > 0 && t.volume24h > 1000000) // 成交量 > 100 万 USDT
        .sort((a, b) => b.volume24h - a.volume24h);

    console.log('📊 热门币种 (按 24h 成交量排序)\n');
    console.log('币种          价格          24h 涨跌    24h 成交量 (USDT)    波动率');
    console.log('='.repeat(75));

    for (let i = 0; i < Math.min(20, usdtPairs.length); i++) {
        const t = usdtPairs[i];
        const volatility = ((t.high24h - t.low24h) / t.price * 100).toFixed(2);
        const changeStr = t.change24h >= 0 ? `+${t.change24h.toFixed(2)}%` : `${t.change24h.toFixed(2)}%`;
        const volumeStr = (t.volume24h / 1000000).toFixed(1) + 'M';
        const priceStr = t.price < 1 ? `$${t.price.toFixed(6)}` : `$${t.price.toFixed(2)}`;
        
        console.log(`${t.symbol.replace('USDT', '').padEnd(12)} ${priceStr.padEnd(14)} ${changeStr.padEnd(10)} ${volumeStr.padEnd(18)} ${volatility}%`);
    }

    console.log('\n\n💡 网格交易推荐 (高波动 + 高成交量):\n');
    
    // 推荐标准：高波动率 (>5%) + 适中价格 (0.1-100) + 高成交量
    const recommendations = usdtPairs
        .filter(t => {
            const volatility = (t.high24h - t.low24h) / t.price;
            return volatility > 0.05 && t.price > 0.1 && t.price < 100 && t.volume24h > 5000000;
        })
        .slice(0, 10);

    recommendations.forEach((t, i) => {
        const volatility = ((t.high24h - t.low24h) / t.price * 100).toFixed(2);
        console.log(`${i+1}. ${t.symbol} - 波动率 ${volatility}%, 价格 $${t.price.toFixed(4)}, 24h 涨跌 ${t.change24h >= 0 ? '+' : ''}${t.change24h.toFixed(2)}%`);
    });
}

main().catch(console.error);
