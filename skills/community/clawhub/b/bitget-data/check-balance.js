#!/usr/bin/env node
// 查询 Bitget 账户余额

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const DATA_DIR = process.env.BITGET_DATA_DIR || path.join(__dirname);
const CONFIG_FILE = path.join(DATA_DIR, 'config.json');

function loadJson(file) {
    try {
        return JSON.parse(fs.readFileSync(file, 'utf8'));
    } catch (e) {
        return null;
    }
}

function sign(message, secret) {
    return crypto.createHmac('sha256', secret).update(message).digest('hex');
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

async function main() {
    console.log('查询 Bitget 账户余额...\n');
    
    // 查询现货账户资产
    const result = await request('/api/v2/spot/account/assets', 'GET');
    
    console.log('API 响应:', JSON.stringify(result, null, 2));
    
    if (result.code === '00000' && result.data) {
        console.log('\n💰 账户资产：');
        result.data.forEach(asset => {
            if (parseFloat(asset.available) > 0 || parseFloat(asset.frozen) > 0) {
                console.log(`  ${asset.coinName}: 可用 ${asset.available} | 冻结 ${asset.frozen}`);
            }
        });
    } else {
        console.log('\n❌ 查询失败:', result.msg || result.error);
    }
}

main().catch(e => {
    console.error('错误:', e.message);
});
