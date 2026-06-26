#!/usr/bin/env node
// 简单测试 K 线数据

const http = require('http');
const https = require('https');

function getKlines() {
    return new Promise((resolve, reject) => {
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
                path: '/api/v2/spot/market/candles?symbol=BTCUSDT&granularity=15min&limit=50',
                method: 'GET'
            };
            
            const req = https.request(options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    const result = JSON.parse(data);
                    console.log('Code:', result.code);
                    console.log('Data length:', result.data ? result.data.length : 0);
                    if (result.data && result.data.length > 0) {
                        console.log('First candle:', result.data[0]);
                        const closes = result.data.map(k => parseFloat(k[4]));
                        console.log('Close prices:', closes.slice(0, 5));
                    }
                });
            });
            
            req.on('error', reject);
            req.end();
        });
        
        proxyReq.on('error', reject);
        proxyReq.end();
    });
}

getKlines().catch(console.error);
