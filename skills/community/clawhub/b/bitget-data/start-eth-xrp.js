#!/usr/bin/env node
// 启动 ETH 和 XRP 网格策略

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
        return JSON.parse(fs.readFileSync(file, 'utf8'));
    } catch (e) {
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

async function startGrid(symbol, gridNum, priceMin, priceMax, amount, maxPosition) {
    log(`🚀 启动 ${symbol} 网格策略...`);
    log(`   价格区间：${priceMin} - ${priceMax} USDT`);
    log(`   网格数量：${gridNum}`);
    log(`   单笔金额：${amount} USDT`);
    log(`   最大仓位：${maxPosition} USDT`);
    
    // 检查是否已有运行中的策略
    const current = await request('/api/v2/spot/grid/current', 'GET', { symbol, tradeType: '1' });
    
    if (current.data && current.data.length > 0) {
        log(`⚠️ ${symbol} 已有运行中的策略，跳过`);
        return false;
    }
    
    // 启动网格策略 (现货网格)
    const params = {
        symbol,
        gridNum: gridNum.toString(),
        lowerPrice: priceMin.toString(),
        upperPrice: priceMax.toString(),
        amount: amount.toString(),
        maxPosition: maxPosition.toString(),
        isBuy: '1',  // 买入模式
        tradeType: '1'  // 现货
    };
    
    const result = await request('/api/v2/spot/grid/start', 'POST', params);
    
    if (result.code === '00000') {
        log(`✅ ${symbol} 网格策略启动成功！`);
        log(`   订单 ID: ${result.data ? result.data.orderId : 'N/A'}`);
        return true;
    } else {
        log(`❌ ${symbol} 启动失败：${result.msg || JSON.stringify(result)}`);
        return false;
    }
}

async function main() {
    log('==================================================');
    log('开始启动 ETH 和 XRP 网格策略');
    log('==================================================\n');
    
    const settings = loadJson(SETTINGS_FILE);
    if (!settings) {
        log('❌ 网格配置文件不存在');
        return;
    }
    
    // 启动 ETH
    if (settings.eth) {
        await startGrid(
            settings.eth.symbol,
            settings.eth.gridNum,
            settings.eth.priceMin,
            settings.eth.priceMax,
            settings.eth.amount,
            settings.eth.maxPosition
        );
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    // 启动 XRP
    if (settings.xrp) {
        await startGrid(
            settings.xrp.symbol,
            settings.xrp.gridNum,
            settings.xrp.priceMin,
            settings.xrp.priceMax,
            settings.xrp.amount,
            settings.xrp.maxPosition
        );
    }
    
    log('\n==================================================');
    log('启动完成！');
    log('==================================================');
}

main().catch(e => {
    log(`❌ 执行出错：${e.message}`);
});
