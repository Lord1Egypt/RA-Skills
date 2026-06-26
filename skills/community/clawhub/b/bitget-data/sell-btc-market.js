#!/usr/bin/env node

const fs = require('fs');
const crypto = require('crypto');
const http = require('http');
const https = require('https');

// 加载配置
const configPath = require('path').join(__dirname, 'config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

function request(endpoint, method = 'GET', params = {}) {
    return new Promise((resolve, reject) => {
        const timestamp = new Date().toISOString().split('.')[0] + '.000Z';
        const queryString = method === 'GET' && Object.keys(params).length > 0 
            ? '?' + new URLSearchParams(params).toString() 
            : '';
        
        const fullpath = '/api/v2' + endpoint + queryString;
        let body = '';
        if (method === 'POST') body = JSON.stringify(params);
        
        const signStr = timestamp + method + fullpath + body;
        const signature = crypto.createHmac('sha256', config.secretKey).update(signStr).digest('base64');
        
        const proxyReq = http.request({
            hostname: '127.0.0.1',
            port: 7897,
            path: 'api.bitget.com:443',
            method: 'CONNECT'
        });
        
        proxyReq.on('connect', (res, socket) => {
            const options = {
                socket: socket,
                hostname: 'api.bitget.com',
                port: 443,
                path: fullpath,
                method: method,
                headers: {
                    'ACCESS-KEY': config.apiKey,
                    'ACCESS-SIGN': signature,
                    'ACCESS-TIMESTAMP': timestamp,
                    'ACCESS-PASSPHRASE': config.passphrase,
                    'Content-Type': 'application/json'
                }
            };
            
            const req = https.request(options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        const result = JSON.parse(data);
                        resolve(result);
                    } catch (e) {
                        resolve({ error: 'Parse Error', raw: data.substring(0, 200) });
                    }
                });
            });
            
            req.on('error', reject);
            if (body) req.write(body);
            req.end();
        });
        
        proxyReq.on('error', (e) => reject(new Error(`Proxy Error: ${e.message}`)));
        proxyReq.end();
    });
}

async function getBTCBalance() {
    const result = await request('/spot/account/assets', 'GET');
    if (result.error || !result.data) {
        throw new Error(result.error || 'No data');
    }
    return result.data;
}

async function getTicker(symbol) {
    const result = await request('/spot/market/tickers', 'GET', { symbol: symbol });
    if (result.error || !result.data) {
        return { error: result.error || 'No data' };
    }
    return result.data;
}

async function sellMarket(symbol, size) {
    // 市价单：orderType=market
    const result = await request('/spot/trade/place-order', 'POST', {
        symbol: symbol,
        side: 'sell',
        force: 'normal',
        orderType: 'market',
        size: size.toString()
    });
    return result;
}

async function main() {
    console.log('========================================');
    console.log('💰 市价卖出 BTC');
    console.log('========================================');
    
    try {
        // 获取 BTC 余额
        console.log('\n📋 查询 BTC 余额...');
        const balance = await getBTCBalance();
        
        const btcAsset = balance.find(b => b.coin === 'BTC');
        if (!btcAsset) {
            console.log('❌ 未找到 BTC 资产');
            return;
        }
        
        const available = parseFloat(btcAsset.available || 0);
        const frozen = parseFloat(btcAsset.frozen || 0);
        const total = available + frozen;
        
        console.log(`   BTC 总额：${total}`);
        console.log(`   可用：${available}`);
        console.log(`   冻结：${frozen}`);
        
        if (available <= 0.0001) {
            console.log('\n⚠️ 没有可用的 BTC 余额');
            return;
        }
        
        // 获取当前价格
        console.log('\n📊 获取当前价格...');
        const tickerResult = await getTicker('BTCUSDT');
        if (!tickerResult.error && tickerResult.length > 0) {
            const currentPrice = parseFloat(tickerResult[0].close);
            console.log(`   当前价格：$${currentPrice}`);
            console.log(`   预计可得：$${(available * currentPrice).toFixed(2)} USDT`);
        }
        
        // 执行卖出（保留 6 位小数）
        console.log('\n🔄 执行市价卖出...');
        const sellSize = available.toFixed(6);
        console.log(`   卖出数量：${sellSize} BTC`);
        const sellResult = await sellMarket('BTCUSDT', sellSize);
        
        console.log('\n📋 API 返回:', JSON.stringify(sellResult, null, 2));
        
        if (!sellResult.error && sellResult.orderId) {
            console.log('\n✅ 市价卖出成功！');
            console.log(`   订单 ID: ${sellResult.orderId}`);
            console.log(`   卖出数量：${available} BTC`);
        } else if (sellResult.code === '00000' || sellResult.code === 0) {
            console.log('\n✅ 市价卖出成功！');
            console.log(`   订单 ID: ${sellResult.orderId || sellResult.data?.orderId}`);
            console.log(`   卖出数量：${sellSize} BTC`);
        } else {
            console.log('\n❌ 卖出失败:', sellResult.error || sellResult.msg || sellResult);
        }
        
    } catch (e) {
        console.log('❌ 错误:', e.message);
    }
    
    console.log('\n========================================');
}

main().catch(console.error);
