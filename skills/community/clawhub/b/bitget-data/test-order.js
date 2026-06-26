#!/usr/bin/env node
// 测试下单 API

const fs = require('fs');
const crypto = require('crypto');
const http = require('http');
const https = require('https');

const CONFIG = JSON.parse(fs.readFileSync(__dirname + '/config.json'));

function sign(message) {
    return crypto.createHmac('sha256', CONFIG.secretKey).update(message).digest('base64');
}

function apiRequest(endpoint, method = 'GET', params = {}) {
    return new Promise((resolve, reject) => {
        const timestamp = Date.now().toString();
        let body = '';
        
        if (method === 'POST') {
            body = JSON.stringify(params);
        }
        
        const signStr = timestamp + method + endpoint + body;
        const signature = sign(signStr);
        
        console.log('Sign String:', signStr);
        console.log('Signature:', signature);
        
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
                path: endpoint,
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
                    try {
                        resolve(JSON.parse(data));
                    } catch (e) {
                        resolve({ raw: data });
                    }
                });
            });
            
            req.on('error', reject);
            if (method === 'POST' && body) {
                req.write(body);
            }
            req.end();
        });
        
        proxyReq.on('error', reject);
        proxyReq.end();
    });
}

async function main() {
    console.log('测试 Bitget API...\n');
    
    // 测试 1: 查询余额
    console.log('1️⃣ 查询余额...');
    const balance = await apiRequest('/api/v2/spot/account/assets', 'GET');
    console.log('Result:', balance.code, balance.msg);
    if (balance.data) {
        balance.data.forEach(a => {
            if (parseFloat(a.available) > 0) {
                console.log(`   ${a.coinName}: ${a.available}`);
            }
        });
    }
    
    // 测试 2: 查询挂单
    console.log('\n2️⃣ 查询 BTC 挂单...');
    const orders = await apiRequest('/api/v2/spot/trade/unfilled-orders?symbol=BTCUSDT&limit=5', 'GET');
    console.log('Result:', orders.code, orders.msg);
    if (orders.data && orders.data.length > 0) {
        console.log(`   找到 ${orders.data.length} 个挂单`);
        orders.data.slice(0, 3).forEach(o => {
            console.log(`   ${o.side} ${o.price} ${o.quantity}`);
        });
    }
    
    // 测试 3: 尝试下小单 (0.0001 BTC)
    console.log('\n3️⃣ 测试下单...');
    const testOrder = await apiRequest('/api/v2/spot/trade/place-order', 'POST', {
        symbol: 'BTCUSDT',
        side: 'buy',
        orderType: 'limit',
        price: '60000',
        quantity: '0.0001'
    });
    console.log('Result:', testOrder.code, testOrder.msg);
    if (testOrder.data) {
        console.log('Order ID:', testOrder.data.orderId);
    }
}

main().catch(console.error);
