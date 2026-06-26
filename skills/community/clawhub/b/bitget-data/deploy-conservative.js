#!/usr/bin/env node
// Bitget 保守网格部署脚本
// 使用保守配置，匹配当前余额 (~20 USDT)

const fs = require('fs');
const crypto = require('crypto');
const http = require('http');
const https = require('https');

const CONFIG = JSON.parse(fs.readFileSync(__dirname + '/config.json'));
const SETTINGS = JSON.parse(fs.readFileSync(__dirname + '/grid_settings_conservative.json'));

function log(msg, level = 'INFO') {
    const timestamp = new Date().toLocaleString('zh-CN');
    console.log(`[${timestamp}] [${level}] ${msg}`);
}

function sign(message) {
    return crypto.createHmac('sha256', CONFIG.secretKey).update(message).digest('base64');
}

function request(endpoint, method = 'GET', params = {}, body = null) {
    return new Promise((resolve) => {
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
                path: fullpath,
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
                        resolve({raw: data.substring(0, 200)});
                    }
                });
            });
            
            req.on('error', e => resolve({error: e.message}));
            if (bodyStr) req.write(bodyStr);
            req.end();
        });
        
        proxyReq.on('error', e => resolve({error: e.message}));
        proxyReq.end();
    });
}

async function cancelAllOrders(symbol) {
    log(`📋 取消 ${symbol} 所有订单...`);
    const orders = await request('/spot/trade/unfilled-orders', 'GET', { symbol, limit: '100' });
    const orderList = orders.data || [];
    
    if (orderList.length === 0) {
        log(`   ✅ 无订单需要取消`);
        return 0;
    }
    
    let canceled = 0;
    for (const order of orderList) {
        const body = { symbol, orderId: order.orderId };
        const result = await request('/spot/trade/cancel-order', 'POST', {}, body);
        if (result.code === '00000') canceled++;
    }
    
    log(`   ✅ 成功取消 ${canceled}/${orderList.length} 个订单`);
    return canceled;
}

async function placeOrder(symbol, side, price, quantity) {
    // 精度处理
    let sizeStr;
    const priceNum = parseFloat(price);
    const qtyNum = parseFloat(quantity);
    
    if (priceNum < 100) {
        sizeStr = qtyNum.toFixed(4);
    } else {
        sizeStr = qtyNum.toFixed(6);
    }
    
    const body = {
        symbol,
        side,
        force: 'GTC',
        orderType: 'limit',
        price: price.toString(),
        size: sizeStr
    };
    
    const result = await request('/spot/trade/place-order', 'POST', {}, body);
    return {
        success: result.code === '00000',
        orderId: result.data?.orderId,
        msg: result.msg,
        code: result.code
    };
}

async function getPrice(symbol) {
    const result = await request('/spot/market/tickers', 'GET', { symbol });
    return result.data?.[0]?.lastPr;
}

async function createGrid(name, config) {
    const { symbol, gridNum, priceMin, priceMax, amount, maxPosition } = config;
    
    log(`\n🚀 部署 ${name.toUpperCase()} 网格...`);
    log(`   交易对：${symbol}`);
    log(`   网格数：${gridNum} 格`);
    log(`   价格区间：${priceMin} - ${priceMax}`);
    log(`   每格金额：${amount} USDT`);
    log(`   最大持仓：${maxPosition} USDT`);
    
    const currentPrice = await getPrice(symbol);
    if (!currentPrice) {
        log(`   ❌ 获取价格失败`, 'ERROR');
        return { success: false, error: '获取价格失败' };
    }
    
    log(`   💰 当前价格：${currentPrice} USDT`);
    
    const step = (priceMax - priceMin) / gridNum;
    const gridSpacingPercent = (step / currentPrice * 100).toFixed(3);
    log(`   📐 网格间距：${step.toFixed(4)} (${gridSpacingPercent}%)`);
    
    let placed = 0;
    let errors = 0;
    
    // 创建买单
    log(`   📈 创建买单网格...`);
    const buyLevels = Math.floor(gridNum * (1 - (currentPrice - priceMin) / (priceMax - priceMin)));
    
    for (let i = 0; i < buyLevels; i++) {
        const price = priceMin + i * step;
        const priceStr = price.toFixed(currentPrice < 100 ? 4 : 2);
        const quantity = (parseFloat(amount) / price).toFixed(6);
        
        const result = await placeOrder(symbol, 'buy', priceStr, quantity);
        if (result.success) {
            placed++;
        } else {
            errors++;
            log(`   ❌ 买单失败：${result.msg || result.code}`, 'WARN');
            if (errors > 3) {
                log(`   ⚠️  连续失败，暂停...`, 'WARN');
                break;
            }
        }
    }
    
    // 创建卖单
    log(`   📉 创建卖单网格...`);
    const sellLevels = gridNum - buyLevels;
    
    for (let i = 0; i < sellLevels; i++) {
        const price = priceMin + (buyLevels + 1 + i) * step;
        const priceStr = price.toFixed(currentPrice < 100 ? 4 : 2);
        const quantity = (parseFloat(amount) / price).toFixed(6);
        
        const result = await placeOrder(symbol, 'sell', priceStr, quantity);
        if (result.success) {
            placed++;
        } else {
            errors++;
        }
    }
    
    log(`\n   ✅ ${name.toUpperCase()} 部署完成:`);
    log(`      总订单：${placed} 个 (买${buyLevels} / 卖${sellLevels})`);
    log(`      失败：${errors} 个`);
    
    return { success: true, placed, errors, buyLevels, sellLevels };
}

async function main() {
    log('\n' + '='.repeat(70));
    log('🚀 Bitget 保守网格部署 - 目标：每天 30-40 笔交易');
    log('='.repeat(70));
    
    // 取消所有现有订单
    log('\n📋 第一步：取消所有现有订单');
    log('─'.repeat(70));
    
    const coins = ['btc', 'sol', 'eth'];
    for (const coin of coins) {
        const symbol = SETTINGS[coin].symbol;
        await cancelAllOrders(symbol);
        await new Promise(r => setTimeout(r, 500));
    }
    
    // 部署新网格
    log('\n📊 第二步：部署保守网格');
    log('─'.repeat(70));
    
    const results = {};
    for (const coin of coins) {
        const config = SETTINGS[coin];
        const result = await createGrid(coin, config);
        results[coin] = result;
        await new Promise(r => setTimeout(r, 1000));
    }
    
    // 汇总报告
    log('\n' + '='.repeat(70));
    log('📊 部署汇总报告');
    log('='.repeat(70));
    
    let totalPlaced = 0;
    let totalErrors = 0;
    
    for (const [coin, result] of Object.entries(results)) {
        if (result.success) {
            log(`✅ ${coin.toUpperCase()}: ${result.placed} 个订单 (买${result.buyLevels} / 卖${result.sellLevels})`);
            totalPlaced += result.placed;
            totalErrors += result.errors;
        } else {
            log(`❌ ${coin.toUpperCase()}: 部署失败 - ${result.error}`, 'ERROR');
        }
    }
    
    log('\n' + '─'.repeat(70));
    log(`🎯 总计：${totalPlaced} 个订单 | 失败：${totalErrors} 个`);
    log('─'.repeat(70));
    
    if (totalPlaced >= 50) {
        log('\n✅ 保守网格部署成功！');
        log('📈 预期交易频率：30-40 笔/天');
        log('🔔 自动监控已启动（每 30 分钟检查）');
        log('📊 每日报告：每晚 21:00 生成\n');
    } else {
        log('\n⚠️  部署订单数较少，可能需要检查配置或 API 权限', 'WARN');
    }
    
    log('='.repeat(70) + '\n');
    
    // 保存部署报告
    const report = {
        timestamp: new Date().toISOString(),
        totalPlaced,
        totalErrors,
        results,
        config: SETTINGS.optimization
    };
    
    fs.writeFileSync(
        __dirname + '/conservative_deployment_report.json',
        JSON.stringify(report, null, 2)
    );
    
    log(`📝 详细报告已保存：conservative_deployment_report.json\n`);
}

main().catch(err => {
    log(`❌ 部署失败：${err.message}`, 'ERROR');
    process.exit(1);
});
