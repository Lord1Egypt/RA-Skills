#!/usr/bin/env node
// Bitget 多网格策略启动脚本
// 启动 BTC/ETH/SOL/XRP 四个币种的网格策略

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const DATA_DIR = process.env.BITGET_DATA_DIR || path.join(__dirname);
const CONFIG_FILE = path.join(DATA_DIR, 'config.json');
const SETTINGS_FILE = path.join(DATA_DIR, 'grid_settings.json');
const LOG_FILE = path.join(DATA_DIR, 'start-grids.log');

function loadJson(file) {
    try {
        return JSON.parse(fs.readFileSync(file, 'utf8'));
    } catch (e) {
        return null;
    }
}

function log(message, level = 'INFO') {
    const timestamp = new Date().toLocaleString('zh-CN');
    const logLine = `[${timestamp}] [${level}] ${message}\n`;
    console.log(logLine.trim());
    fs.appendFileSync(LOG_FILE, logLine);
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

        // 使用 HTTP CONNECT 隧道通过代理访问 HTTPS
        const proxyOptions = {
            hostname: '127.0.0.1',
            port: 7897,
            path: `api.bitget.com:443`,
            method: 'CONNECT',
            headers: {
                'Host': 'api.bitget.com:443'
            }
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

async function startGridStrategy(symbol, gridNum, priceMin, priceMax, amount, maxPosition) {
    log(`🚀 启动 ${symbol} 网格策略...`);
    
    // 1. 先检查是否有运行中的策略
    const runningStrategies = await request('/api/v2/spot/grid/trade-current', 'GET', { symbol });
    
    if (runningStrategies.data && runningStrategies.data.length > 0) {
        log(`⚠️ ${symbol} 已有运行中的策略，跳过`);
        return;
    }
    
    // 2. 计算网格参数
    const priceRange = priceMax - priceMin;
    const gridStep = priceRange / gridNum;
    
    // 3. 启动网格策略
    const strategyParams = {
        symbol,
        gridNum: gridNum.toString(),
        priceMin: priceMin.toString(),
        priceMax: priceMax.toString(),
        amount: amount.toString(),
        maxPosition: maxPosition.toString(),
        strategyType: '1', // 等差网格
        runType: '1' // 手动启动
    };
    
    const result = await request('/api/v2/spot/grid/trade-start', 'POST', strategyParams);
    
    if (result.code === '00000') {
        log(`✅ ${symbol} 网格策略启动成功！`);
        log(`   网格数：${gridNum} | 价格区间：${priceMin}-${priceMax}`);
        log(`   单笔金额：${amount} USDT | 最大仓位：${maxPosition} USDT`);
        return true;
    } else {
        log(`❌ ${symbol} 网格策略启动失败：${result.msg || JSON.stringify(result)}`);
        return false;
    }
}

async function main() {
    log('==================================================');
    log('开始启动 Bitget 多网格策略');
    log('==================================================');
    
    const settings = loadJson(SETTINGS_FILE);
    if (!settings) {
        log('❌ 网格配置文件不存在', 'ERROR');
        return;
    }
    
    const results = [];
    
    // 启动各个币种的网格
    for (const [key, config] of Object.entries(settings)) {
        log(`\n处理 ${config.symbol}...`);
        const success = await startGridStrategy(
            config.symbol,
            config.gridNum,
            config.priceMin,
            config.priceMax,
            config.amount,
            config.maxPosition
        );
        results.push({ symbol: config.symbol, success });
        
        // 每个策略之间间隔 1 秒
        if (Object.keys(settings).indexOf(key) < Object.keys(settings).length - 1) {
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }
    
    log('\n==================================================');
    log('启动完成汇总：');
    results.forEach(r => {
        log(`  ${r.success ? '✅' : '❌'} ${r.symbol}`);
    });
    log('==================================================');
}

main().catch(e => {
    log(`❌ 执行出错：${e.message}`, 'ERROR');
});
