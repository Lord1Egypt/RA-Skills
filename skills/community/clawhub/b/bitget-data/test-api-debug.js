#!/usr/bin/env node
// Bitget 网格启动脚本 - 修复版

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const DATA_DIR = process.env.BITGET_DATA_DIR || path.join(__dirname);
const CONFIG_FILE = path.join(DATA_DIR, 'config.json');
const SETTINGS_FILE = path.join(DATA_DIR, 'grid_settings.json');

function loadJson(file) {
    try {
        const content = fs.readFileSync(file, 'utf8');
        console.log(`读取文件：${file}`);
        const parsed = JSON.parse(content);
        console.log(`内容：${JSON.stringify(parsed, null, 2).substring(0, 200)}...`);
        return parsed;
    } catch (e) {
        console.error(`读取 ${file} 失败：${e.message}`);
        return null;
    }
}

function log(message) {
    const timestamp = new Date().toLocaleString('zh-CN');
    console.log(`[${timestamp}] ${message}`);
}

function sign(message, secret) {
    return crypto.createHmac('sha256', secret).update(message).digest('base64');
}

function apiRequest(endpoint, method = 'GET', body = null) {
    return new Promise((resolve, reject) => {
        const config = loadJson(CONFIG_FILE);
        if (!config) {
            resolve({ error: '配置文件不存在' });
            return;
        }

        const timestamp = Date.now().toString();
        const pathWithQuery = endpoint;
        
        const signStr = timestamp + method + pathWithQuery + (body ? JSON.stringify(body) : '');
        const signature = sign(signStr, config.secretKey);

        const proxyOptions = {
            hostname: '127.0.0.1',
            port: 7897,
            path: `api.bitget.com:443`,
            method: 'CONNECT'
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
                    'Content-Type': 'application/json'
                }
            };

            const req = https.request(options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        const result = JSON.parse(data);
                        console.log(`API 响应：${endpoint} -> ${JSON.stringify(result).substring(0, 300)}`);
                        resolve(result);
                    } catch (e) {
                        resolve({ error: '解析失败', raw: data.substring(0, 500) });
                    }
                });
            });

            req.on('error', (e) => {
                console.error(`请求错误：${e.message}`);
                reject(e);
            });
            
            if (body) {
                req.write(JSON.stringify(body));
            }
            req.end();
        });

        proxyReq.on('error', reject);
        proxyReq.end();
    });
}

async function testAPI() {
    log('🔍 测试 API 连接...');
    
    // 测试余额
    const balance = await apiRequest('/api/v2/spot/account/assets', 'GET');
    log(`余额 API: ${balance.code || 'error'}`);
    
    // 测试价格
    const ticker = await apiRequest('/api/v2/spot/market/tickers?symbol=BTCUSDT', 'GET');
    log(`价格 API: ${ticker.code || 'error'}`);
    
    return true;
}

testAPI().catch(console.error);
