#!/usr/bin/env node
// 快速交易报告

const fs = require('fs');
const crypto = require('crypto');
const http = require('http');
const https = require('https');

const CONFIG = JSON.parse(fs.readFileSync(__dirname + '/config.json'));

function sign(message) {
    return crypto.createHmac('sha256', CONFIG.secretKey).update(message).digest('base64');
}

function request(endpoint, method = 'GET', params = {}) {
    return new Promise((resolve, reject) => {
        const timestamp = Date.now().toString();
        let body = '';
        if (method === 'POST') body = JSON.stringify(params);
        
        const signStr = timestamp + method + endpoint + body;
        const signature = sign(signStr);
        
        const proxyOptions = {
            hostname: '127.0.0.1',
            port: 7897,
            path: 'api.bitget.com:443',
            method: 'CONNECT'
        };
        
        const proxyReq = http.request(proxyOptions);
        
        proxyReq.on('connect', (res, socket) => {
            const options = {
                socket: socket,
                hostname: 'api.bitget.com',
                port: 443,
                path: endpoint + (method === 'GET' && Object.keys(params).length ? '?' + new URLSearchParams(params) : ''),
                method: method,
                headers: {
                    'ACCESS-KEY': CONFIG.apiKey,
                    'ACCESS-SIGN': signature,
                    'ACCESS-TIMESTAMP': timestamp,
                    'ACCESS-PASSPHRASE': CONFIG.passphrase,
                    'Content-Type': 'application/json'
                }
            };
            
            const req = https.request(options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try { resolve(JSON.parse(data)); }
                    catch (e) { resolve({ raw: data }); }
                });
            });
            
            req.on('error', reject);
            if (method === 'POST' && body) req.write(body);
            req.end();
        });
        
        proxyReq.on('error', reject);
        proxyReq.end();
    });
}

async function main() {
    console.log('\n' + '='.repeat(70));
    console.log('📊 Bitget 交易情况报告');
    console.log('时间：' + new Date().toLocaleString('zh-CN'));
    console.log('='.repeat(70));
    
    // 获取余额
    console.log('\n💰 账户余额:');
    const balance = await request('/api/v2/spot/account/assets', 'GET');
    
    if (balance.data) {
        balance.data.forEach(asset => {
            const available = parseFloat(asset.available);
            const frozen = parseFloat(asset.frozen);
            const total = available + frozen;
            if (total > 0.001) {
                console.log(`   ${asset.coinName || 'UNKNOWN'}: ${available.toFixed(4)} + ${frozen.toFixed(4)} = ${total.toFixed(4)}`);
            }
        });
    }
    
    // 获取 BTC 挂单
    console.log('\n📋 BTCUSDT 挂单:');
    const btcOrders = await request('/api/v2/spot/trade/unfilled-orders', 'GET', { symbol: 'BTCUSDT', limit: '100' });
    if (btcOrders.data) {
        const buys = btcOrders.data.filter(o => o.side === 'buy').length;
        const sells = btcOrders.data.filter(o => o.side === 'sell').length;
        console.log(`   总挂单：${btcOrders.data.length} (买单 ${buys} / 卖单 ${sells})`);
    }
    
    // 获取 SOL 挂单
    console.log('\n📋 SOLUSDT 挂单:');
    const solOrders = await request('/api/v2/spot/trade/unfilled-orders', 'GET', { symbol: 'SOLUSDT', limit: '100' });
    if (solOrders.data) {
        const buys = solOrders.data.filter(o => o.side === 'buy').length;
        const sells = solOrders.data.filter(o => o.side === 'sell').length;
        console.log(`   总挂单：${solOrders.data.length} (买单 ${buys} / 卖单 ${sells})`);
    }
    
    // 获取市场价格
    console.log('\n📈 市场价格:');
    const btcTicker = await request('/api/v2/spot/market/tickers', 'GET', { symbol: 'BTCUSDT' });
    const solTicker = await request('/api/v2/spot/market/tickers', 'GET', { symbol: 'SOLUSDT' });
    
    if (btcTicker.data && btcTicker.data[0]) {
        const b = btcTicker.data[0];
        console.log(`   BTCUSDT: ${b.lastPr} USDT (24h: ${(parseFloat(b.change24h)*100).toFixed(2)}%)`);
    }
    
    if (solTicker.data && solTicker.data[0]) {
        const s = solTicker.data[0];
        console.log(`   SOLUSDT: ${s.lastPr} USDT (24h: ${(parseFloat(s.change24h)*100).toFixed(2)}%)`);
    }
    
    console.log('\n' + '='.repeat(70));
    console.log('✅ 报告完成');
    console.log('='.repeat(70) + '\n');
}

main().catch(console.error);
