#!/usr/bin/env node
// Bitget 超高密度网格部署脚本
// 使用 auto-monitor.js 的签名方式 (base64 + ISO 时间戳)

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const DATA_DIR = __dirname;
const CONFIG_FILE = path.join(DATA_DIR, 'config.json');
const SETTINGS_FILE = path.join(DATA_DIR, 'grid_settings_ultra.json');
const LOG_FILE = path.join(DATA_DIR, 'deploy-ultra.log');

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

// API 签名 - base64 格式
function sign(message, secret) {
    return crypto.createHmac('sha256', secret).update(message).digest('base64');
}

// API 请求 - 使用 auto-monitor.js 的方式
function request(endpoint, method = 'GET', params = {}, body = null) {
    return new Promise((resolve) => {
        const config = loadJson(CONFIG_FILE);
        if (!config) {
            resolve({ error: '配置文件不存在' });
            return;
        }

        const timestamp = new Date().toISOString().split('.')[0] + '.000Z';
        let queryString = '';
        if (method === 'GET' && Object.keys(params).length > 0) {
            queryString = '?' + new URLSearchParams(params);
        }
        
        const fullpath = '/api/v2' + endpoint + queryString;
        let bodyStr = '';
        if (method === 'POST' && body) {
            bodyStr = typeof body === 'string' ? body : JSON.stringify(body);
        }
        
        const signStr = timestamp + method + fullpath + bodyStr;
        const signature = sign(signStr, config.secretKey);

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
                        resolve({ error: '解析失败', raw: data });
                    }
                });
            });

            req.on('error', (e) => resolve({ error: e.message }));
            
            if (bodyStr) {
                req.write(bodyStr);
            }
            
            req.end();
        });

        proxyReq.on('error', (e) => resolve({ error: e.message }));
        proxyReq.end();
    });
}

// 取消所有现有订单
async function cancelAllOrders(symbol) {
    log(`🗑️ 取消 ${symbol} 所有订单...`);
    
    const result = await request('/spot/trade/cancel-all-orders', 'POST', {}, { symbol });
    
    if (result.code === '00000') {
        const cancelled = result.data?.cancelledCount || 0;
        log(`   ✅ 成功取消 ${cancelled} 个订单`);
        return cancelled;
    } else {
        log(`   ⚠️ 取消失败：${result.code} - ${result.msg}`, 'WARN');
        return 0;
    }
}

// 启动网格策略
async function startGridStrategy(symbol, gridNum, priceMin, priceMax, amount) {
    log(`🚀 启动 ${symbol} 网格策略...`);
    log(`   网格数：${gridNum}, 区间：${priceMin}-${priceMax}, 金额：${amount} USDT`);
    
    // 构建策略参数
    const strategyParams = {
        symbol: symbol,
        gridNum: gridNum.toString(),
        priceMin: priceMin.toString(),
        priceMax: priceMax.toString(),
        amount: amount.toString(),
        isInfinity: 'false',
        gridType: 'arithmetic',
        buyType: 'size',
        sellType: 'size'
    };
    
    log(`   发送策略参数...`);
    const result = await request('/spot/grid/trade-start', 'POST', {}, strategyParams);
    
    if (result.code === '00000') {
        const strategyId = result.data?.strategyId || 'unknown';
        log(`   ✅ 策略启动成功！策略 ID: ${strategyId}`);
        return { success: true, strategyId };
    } else {
        log(`   ❌ 策略启动失败：${result.code} - ${result.msg}`, 'ERROR');
        return { success: false, error: result.msg };
    }
}

// 检查网格状态
async function checkGridStatus(symbol) {
    const result = await request('/spot/grid/trade-current', 'GET', { symbol });
    
    if (result.code === '00000' && result.data && result.data.length > 0) {
        return {
            active: true,
            strategyId: result.data[0].strategyId,
            gridNum: result.data[0].gridNum
        };
    }
    return { active: false };
}

// 主函数
async function main() {
    log('\n' + '='.repeat(70));
    log('🚀 Bitget 超高密度网格部署开始');
    log('='.repeat(70));
    
    const config = loadJson(CONFIG_FILE);
    const settings = loadJson(SETTINGS_FILE);
    
    if (!config) {
        log('❌ 配置文件不存在', 'ERROR');
        return;
    }
    
    if (!settings) {
        log('❌ 网格配置文件不存在', 'ERROR');
        return;
    }
    
    const coins = ['btc', 'sol', 'eth'];
    const results = [];
    
    for (const coin of coins) {
        const s = settings[coin];
        if (!s) continue;
        
        log('\n' + '-'.repeat(70));
        log(`📊 处理 ${coin.toUpperCase()} (${s.symbol})`);
        log('-'.repeat(70));
        
        // 1. 检查现有网格
        const status = await checkGridStatus(s.symbol);
        if (status.active) {
            log(`   ⚠️ 发现运行中的网格 (ID: ${status.strategyId})，先取消...`);
            await cancelAllOrders(s.symbol);
            await new Promise(resolve => setTimeout(resolve, 2000));
        }
        
        // 2. 取消现有订单
        await cancelAllOrders(s.symbol);
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // 3. 启动新网格
        const result = await startGridStrategy(
            s.symbol,
            s.gridNum,
            s.priceMin,
            s.priceMax,
            s.amount
        );
        
        results.push({ coin, symbol: s.symbol, ...result });
        
        // 等待 3 秒再处理下一个
        await new Promise(resolve => setTimeout(resolve, 3000));
    }
    
    // 汇总结果
    log('\n' + '='.repeat(70));
    log('📊 部署结果汇总');
    log('='.repeat(70));
    
    results.forEach(r => {
        const status = r.success ? '✅' : '❌';
        log(`${status} ${r.symbol}: ${r.success ? '成功 (ID: ' + r.strategyId + ')' : '失败 (' + r.error + ')'}`);
    });
    
    const successCount = results.filter(r => r.success).length;
    log(`\n总计：${successCount}/${coins.length} 个策略部署成功`);
    
    if (successCount === coins.length) {
        log('\n🎉 所有网格策略部署完成！');
    } else {
        log('\n⚠️ 部分策略部署失败，请检查日志', 'WARN');
    }
    
    log('\n' + '='.repeat(70));
}

// 运行
main().catch(err => {
    log(`❌ 错误：${err.message}`, 'ERROR');
    process.exit(1);
});
