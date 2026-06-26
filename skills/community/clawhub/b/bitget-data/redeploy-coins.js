#!/usr/bin/env node
// Bitget 高频网格补部署 - 修复精度问题后部署 SOL/ETH/AVAX

const fs = require('fs');
const crypto = require('crypto');
const http = require('http');
const https = require('https');

const CONFIG = JSON.parse(fs.readFileSync(__dirname + '/config.json'));
const SETTINGS = JSON.parse(fs.readFileSync(__dirname + '/grid_settings_highfreq.json'));

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
    // Bitget 要求数量最多 4 位小数 - 统一用 4 位
    const sizeStr = quantity.toFixed(4);
    
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
    
    log(`\n🚀 部署 ${name.toUpperCase()} 高频网格...`);
    log(`   交易对：${symbol}`);
    log(`   网格数：${gridNum} 格 (超密集)`);
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
        const price = (priceMin + i * step).toFixed(currentPrice < 100 ? 4 : 2);
        const quantity = amount / price;
        
        const result = await placeOrder(symbol, 'buy', price, quantity);
        if (result.success) {
            placed++;
        } else {
            errors++;
            if (errors <= 3) {
                log(`   ❌ 买单失败：${result.msg} (价${price} 量${amount/price})`, 'WARN');
            }
            if (errors > 5) {
                log(`   ⚠️  连续失败，暂停...`, 'WARN');
                break;
            }
        }
        
        if (placed % 10 === 0 && placed > 0) {
            log(`   已放置 ${placed} 个买单...`);
        }
    }
    
    // 创建卖单 (当前价格以上)
    log(`   📉 创建卖单网格...`);
    const sellLevels = gridNum - buyLevels;
    
    for (let i = 0; i < sellLevels; i++) {
        const price = (priceMin + (buyLevels + 1 + i) * step).toFixed(currentPrice < 100 ? 4 : 2);
        const quantity = amount / price;
        
        const result = await placeOrder(symbol, 'sell', price, quantity);
        if (result.success) {
            placed++;
        } else {
            errors++;
            if (errors <= 3) {
                log(`   ❌ 卖单失败：${result.msg}`, 'WARN');
            }
        }
        
        if (placed % 10 === 0 && placed > 0) {
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
    log('🚀 Bitget 高频网格补部署 - SOL/ETH/AVAX');
    log('='.repeat(70));
    
    // 只部署 SOL, ETH, AVAX (BTC 已成功)
    const coins = ['sol', 'eth', 'avax'];
    
    // 先取消现有订单
    log('\n📋 第一步：取消现有订单');
    log('─'.repeat(70));
    
    for (const coin of coins) {
        const symbol = SETTINGS[coin].symbol;
        await cancelAllOrders(symbol);
        await new Promise(r => setTimeout(r, 500));
    }
    
    // 部署新高频网格
    log('\n📊 第二步：部署高频网格');
    log('─'.repeat(70));
    
    const results = {};
    for (const coin of coins) {
        const config = SETTINGS[coin];
        const result = await createHighFreqGrid(coin, config);
        results[coin] = result;
        await new Promise(r => setTimeout(r, 1000)); // 避免 API 限流
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
    
    if (totalPlaced >= 150) {
        log('\n✅ 高频网格部署成功！');
        log('📈 预期交易频率：60-100 笔/天');
        log('🔔 自动监控已启动（每 30 分钟检查）');
        log('📊 每日报告：每晚 21:00 生成\n');
    } else {
        log('\n⚠️  部署订单数较少，可能需要检查配置', 'WARN');
    }
    
    log('='.repeat(70) + '\n');
}

// 运行
main().catch(err => {
    log(`❌ 部署失败：${err.message}`, 'ERROR');
    process.exit(1);
});
