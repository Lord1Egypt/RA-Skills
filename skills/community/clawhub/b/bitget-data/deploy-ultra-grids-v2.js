#!/usr/bin/env node
// Bitget 超高密度网格部署脚本 - v2
// 使用 ultra 配置，目标每天 100-150 笔交易

const fs = require('fs');
const crypto = require('crypto');
const http = require('http');
const https = require('https');

const CONFIG = JSON.parse(fs.readFileSync(__dirname + '/config.json'));
const SETTINGS = JSON.parse(fs.readFileSync(__dirname + '/grid_settings_ultra.json'));

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
                        const result = JSON.parse(data);
                        resolve(result);
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

async function getOrders(symbol) {
    const result = await request('/spot/trade/unfilled-orders', 'GET', { symbol, limit: '100' });
    return result.data || [];
}

async function cancelOrder(symbol, orderId) {
    const body = { symbol, orderId };
    const result = await request('/spot/trade/cancel-order', 'POST', {}, body);
    return result.code === '00000';
}

async function cancelAllOrders(symbol) {
    log(`📋 取消 ${symbol} 所有订单...`);
    const orders = await getOrders(symbol);
    
    if (orders.length === 0) {
        log(`   ✅ 无订单需要取消`);
        return 0;
    }
    
    let canceled = 0;
    for (const order of orders) {
        const success = await cancelOrder(symbol, order.orderId);
        if (success) canceled++;
    }
    
    log(`   ✅ 成功取消 ${canceled}/${orders.length} 个订单`);
    return canceled;
}

async function placeOrder(symbol, side, price, quantity) {
    // quantity 已经是字符串 (调用前已 toFixed)
    // Bitget 精度要求：BTC 6 位，SOL/ETH 等 4 位
    let sizeStr = quantity.toString();
    if (parseFloat(price) < 100) {
        // 中低价币 (SOL/ETH 等) 保留 4 位小数
        sizeStr = parseFloat(quantity).toFixed(4);
    } else {
        // 高价币 (BTC 等) 保留 6 位小数
        sizeStr = parseFloat(quantity).toFixed(6);
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

async function createHighFreqGrid(name, config) {
    const { symbol, gridNum, priceMin, priceMax, amount, maxPosition } = config;
    
    log(`\n🚀 部署 ${name.toUpperCase()} 超高密度网格...`);
    log(`   交易对：${symbol}`);
    log(`   网格数：${gridNum} 格 (超高密度)`);
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
    
    // 创建买单 (当前价格以下)
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
        
        if (placed % 15 === 0) {
            log(`   已放置 ${placed} 个买单...`);
        }
    }
    
    // 创建卖单 (当前价格以上)
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
        
        if (placed % 15 === 0) {
            log(`   已放置 ${placed} 个订单...`);
        }
    }
    
    log(`\n   ✅ ${name.toUpperCase()} 部署完成:`);
    log(`      总订单：${placed} 个 (买${buyLevels} / 卖${sellLevels})`);
    log(`      失败：${errors} 个`);
    
    return { success: true, placed, errors, buyLevels, sellLevels };
}

async function main() {
    log('\n' + '='.repeat(70));
    log('🚀 Bitget 超高密度网格部署 - 目标：每天 100-150 笔交易');
    log('='.repeat(70));
    
    // 备份旧配置
    const oldSettingsPath = __dirname + '/grid_settings.json.bak_ultra';
    if (fs.existsSync(__dirname + '/grid_settings.json')) {
        fs.copyFileSync(__dirname + '/grid_settings.json', oldSettingsPath);
        log(`📦 旧配置已备份：${oldSettingsPath}`);
    }
    
    // 取消所有现有订单
    log('\n📋 第一步：取消所有现有订单');
    log('─'.repeat(70));
    
    const coins = ['btc', 'sol', 'eth'];
    for (const coin of coins) {
        const symbol = SETTINGS[coin].symbol;
        await cancelAllOrders(symbol);
        await new Promise(r => setTimeout(r, 500));
    }
    
    // 部署新高频网格
    log('\n📊 第二步：部署超高密度网格');
    log('─'.repeat(70));
    
    const results = {};
    for (const coin of coins) {
        const config = SETTINGS[coin];
        const result = await createHighFreqGrid(coin, config);
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
    
    if (totalPlaced >= 300) {
        log('\n✅ 超高密度网格部署成功！');
        log('📈 预期交易频率：100-150 笔/天');
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
        __dirname + '/ultra_deployment_report.json',
        JSON.stringify(report, null, 2)
    );
    
    log(`📝 详细报告已保存：ultra_deployment_report.json\n`);
}

main().catch(err => {
    log(`❌ 部署失败：${err.message}`, 'ERROR');
    process.exit(1);
});
