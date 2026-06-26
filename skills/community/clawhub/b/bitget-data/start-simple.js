#!/usr/bin/env node
// Bitget 网格启动脚本 - 简化版
// 直接使用现货下单 API 创建网格订单

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
                        resolve(JSON.parse(data));
                    } catch (e) {
                        resolve({ error: '解析失败', raw: data });
                    }
                });
            });

            req.on('error', reject);
            
            if (body) {
                req.write(JSON.stringify(body));
            }
            req.end();
        });

        proxyReq.on('error', reject);
        proxyReq.end();
    });
}

async function checkBalance() {
    log('📊 检查账户余额...');
    const result = await apiRequest('/api/v2/spot/account/assets', 'GET');
    
    if (result.code === '00000' && result.data) {
        const usdt = result.data.find(a => a.coin === 'USDT');
        if (usdt) {
            log(`✅ USDT 可用余额：${usdt.available} USDT`);
            return parseFloat(usdt.available);
        }
    }
    log('⚠️ 无法获取余额');
    return 0;
}

async function getCurrentPrice(symbol) {
    log(`📈 获取 ${symbol} 当前价格...`);
    const result = await apiRequest(`/api/v2/spot/market/tickers?symbol=${symbol}`, 'GET');
    
    if (result.code === '00000' && result.data && result.data[0]) {
        const price = parseFloat(result.data[0].lastPr);
        log(`✅ ${symbol} 当前价格：${price} USDT`);
        return price;
    }
    log('⚠️ 无法获取价格');
    return null;
}

async function placeOrder(symbol, side, price, quantity) {
    const body = {
        symbol: symbol,
        side: side,
        orderType: 'limit',
        force: 'GTC',
        price: price.toString(),
        size: quantity.toString()
    };
    
    log(`📝 下单：${side.toUpperCase()} ${symbol} @ ${price} USDT, 数量：${quantity}`);
    
    const result = await apiRequest('/api/v2/spot/trade/place-order', 'POST', body);
    
    if (result.code === '00000') {
        log(`✅ 订单成功！ID: ${result.data.orderId}`);
        return { success: true, orderId: result.data.orderId };
    } else {
        log(`❌ 订单失败：${result.msg || JSON.stringify(result)}`);
        return { success: false, error: result.msg };
    }
}

async function createGrid(symbol, gridNum, priceMin, priceMax, amountPerGrid) {
    log(`\n🚀 创建 ${symbol} 网格策略...`);
    log(`   网格数：${gridNum} | 区间：${priceMin}-${priceMax} USDT`);
    
    const currentPrice = await getCurrentPrice(symbol);
    if (!currentPrice) {
        log('⚠️ 跳过，无法获取价格');
        return;
    }
    
    const gridStep = (priceMax - priceMin) / gridNum;
    log(`   网格间距：${gridStep.toFixed(2)} USDT`);
    
    const orders = [];
    
    // 在当前位置下方创建买单
    let buyPrice = currentPrice;
    let buyCount = 0;
    const maxBuys = Math.floor((currentPrice - priceMin) / gridStep);
    
    log(`\n📥 创建买单 (最多${maxBuys}个)...`);
    for (let i = 1; i <= maxBuys && buyCount < 5; i++) {
        buyPrice = currentPrice - (i * gridStep);
        if (buyPrice < priceMin) break;
        
        // 修复：数量固定 4 位小数，向下取整确保不超额
        const quantity = Math.floor((amountPerGrid / buyPrice) * 10000) / 10000;
        const result = await placeOrder(symbol, 'buy', buyPrice.toFixed(2), quantity.toFixed(4));
        
        if (result.success) {
            orders.push(result.orderId);
            buyCount++;
            await new Promise(r => setTimeout(r, 500)); // 限速
        }
    }
    
    // 在当前位置上方创建卖单
    let sellPrice = currentPrice;
    let sellCount = 0;
    const maxSells = Math.floor((priceMax - currentPrice) / gridStep);
    
    log(`\n📤 创建卖单 (最多${maxSells}个)...`);
    for (let i = 1; i <= maxSells && sellCount < 5; i++) {
        sellPrice = currentPrice + (i * gridStep);
        if (sellPrice > priceMax) break;
        
        // 修复：数量固定 4 位小数，向下取整确保不超额
        const quantity = Math.floor((amountPerGrid / sellPrice) * 10000) / 10000;
        const result = await placeOrder(symbol, 'sell', sellPrice.toFixed(2), quantity.toFixed(4));
        
        if (result.success) {
            orders.push(result.orderId);
            sellCount++;
            await new Promise(r => setTimeout(r, 500)); // 限速
        }
    }
    
    log(`\n✅ ${symbol} 网格创建完成！共 ${orders.length} 个订单`);
    return orders;
}

async function main() {
    log('==================================================');
    log('Bitget 自动网格交易系统启动');
    log('==================================================\n');
    
    const balance = await checkBalance();
    if (balance < 100) {
        log('❌ 余额不足，需要至少 100 USDT');
        return;
    }
    
    const settings = loadJson(SETTINGS_FILE);
    if (!settings) {
        log('❌ 配置文件不存在');
        return;
    }
    
    const allOrders = [];
    
    for (const [key, config] of Object.entries(settings)) {
        // 跳过非网格配置（如 optimization）
        if (!config.symbol) {
            log(`⏭️ 跳过 ${key}（非网格配置）`);
            continue;
        }
        
        const orders = await createGrid(
            config.symbol,
            config.gridNum,
            config.priceMin,
            config.priceMax,
            config.amount
        );
        
        if (orders && orders.length > 0) {
            allOrders.push(...orders);
        }
        
        await new Promise(r => setTimeout(r, 2000));
    }
    
    log('\n==================================================');
    log(`启动完成！共创建 ${allOrders.length} 个订单`);
    log('==================================================');
}

main().catch(e => {
    log(`❌ 错误：${e.message}`);
    console.error(e);
});
