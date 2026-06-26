#!/usr/bin/env node
// 测试 Bitget 网格 API

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const DATA_DIR = __dirname;
const CONFIG_FILE = path.join(DATA_DIR, 'config.json');

function loadJson(file) {
    try {
        return JSON.parse(fs.readFileSync(file, 'utf8'));
    } catch (e) {
        return null;
    }
}

function sign(message, secret) {
    return crypto.createHmac('sha256', secret).update(message).digest('base64');
}

function request(endpoint, method = 'GET', params = {}) {
    return new Promise((resolve, reject) => {
        const config = loadJson(CONFIG_FILE);
        if (!config) {
            resolve({ error: '配置文件不存在' });
            return;
        }

        const timestamp = Date.now().toString();
        const queryString = Object.keys(params).length > 0 ? '?' + new URLSearchParams(params).toString() : '';
        const pathWithQuery = endpoint + queryString;
        
        const signStr = timestamp + method + pathWithQuery;
        const signature = sign(signStr, config.secretKey);

        const proxyOptions = {
            hostname: '127.0.0.1',
            port: 7897,
            path: `api.bitget.com:443`,
            method: 'CONNECT',
            headers: { 'Host': 'api.bitget.com:443' }
        };

        const proxyReq = http.request(proxyOptions);
        
        proxyReq.on('connect', (res, socket, head) => {
            const options = {
                socket: socket,
                hostname: 'api.bitget.com',
                port: 443,
                path: pathWithQuery,
                method: method,
                headers: {
                    'ACCESS-KEY': config.apiKey,
                    'ACCESS-SIGN': signature,
                    'ACCESS-TIMESTAMP': timestamp,
                    'ACCESS-PASSPHRASE': config.passphrase,
                    'Content-Type': 'application/json',
                    'Host': 'api.bitget.com'
                },
                rejectUnauthorized: false
            };

            const req = https.request(options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        const result = JSON.parse(data);
                        resolve(result);
                    } catch (e) {
                        resolve({ error: '解析失败', raw: data });
                    }
                });
            });

            req.on('error', reject);
            
            if (method === 'POST' && Object.keys(params).length > 0) {
                req.write(JSON.stringify(params));
            }
            
            req.end();
        });

        proxyReq.on('error', reject);
        proxyReq.end();
    });
}

async function testEndpoints() {
    const endpoints = [
        // 现货网格
        '/api/v2/spot/grid/current?symbol=BTCUSDT&tradeType=1',
        '/api/v2/spot/grid/profit-current?symbol=BTCUSDT',
        '/api/v2/spot/grid/sub-current?symbol=BTCUSDT',
        '/api/v2/spot/trade/grid-sub-orders?symbol=BTCUSDT',
        // 策略
        '/api/v2/spot/strategy/current?symbol=BTCUSDT',
        '/api/v2/spot/plan/current?symbol=BTCUSDT',
        // 订单
        '/api/v2/spot/trade/orders-pending?symbol=BTCUSDT',
        '/api/v2/spot/trade/history?symbol=BTCUSDT&limit=3',
        // 合约网格
        '/api/v2/mix/grid/current?symbol=BTCUSDT&productType=umcbl',
        '/api/v2/mix/plan/current?symbol=BTCUSDT&productType=umcbl',
    ];
    
    console.log('测试 Bitget API 端点...\n');
    
    for (const endpoint of endpoints) {
        const result = await request(endpoint, 'GET');
        const status = result.code === '00000' ? '✅' : (result.code === '40404' ? '❌ 404' : `⚠️ ${result.code}`);
        console.log(`${status} ${endpoint}`);
        if (result.code === '00000' && result.data) {
            console.log(`   数据：${JSON.stringify(result.data).substring(0, 100)}...`);
        }
    }
}

testEndpoints().catch(e => {
    console.error('错误:', e.message);
});
