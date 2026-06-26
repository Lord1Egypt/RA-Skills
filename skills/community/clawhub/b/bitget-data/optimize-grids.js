#!/usr/bin/env node
// 优化网格策略 - 撤销旧挂单并重新挂单

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const DATA_DIR = __dirname;
const CONFIG_FILE = path.join(DATA_DIR, 'config.json');
const SETTINGS_FILE = path.join(DATA_DIR, 'grid_settings.json');

function loadJson(file) {
    try {
        return JSON.parse(fs.readFileSync(file, 'utf8'));
    } catch (e) {
        return null;
    }
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
        let body = '';
        
        if (method === 'POST') {
            body = JSON.stringify(params);
        }
        
        // GET 请求签名不包含 query string
        const signStr = timestamp + method + endpoint + body;
        const signature = sign(signStr, config.secretKey);
        
        const queryString = Object.keys(params).length > 0 && method === 'GET' ? '?' + new URLSearchParams(params).toString() : '';
        const pathWithQuery = endpoint + queryString;

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

async function getMarketData(symbol) {
    const result = await request('/api/v2/spot/market/tickers', 'GET', { symbol });
    return result.data && result.data[0] ? result.data[0] : null;
}

async function cancelAllOrders(symbol) {
    const result = await request('/api/v2/spot/trade/cancel-symbol-orders', 'POST', { symbol });
    return result;
}

async function placeOrder(symbol, side, price, quantity) {
    // SOL 需要 4 位小数精度
    const sizePrecision = symbol.includes('SOL') ? 4 : 6;
    
    const params = {
        symbol,
        side,
        orderType: 'limit',
        price: price.toFixed(side === 'buy' ? 2 : 2),
        size: quantity.toFixed(sizePrecision),
        force: 'GTC'
    };
    
    const result = await request('/api/v2/spot/trade/place-order', 'POST', params);
    return result;
}

async function optimizeGrid(symbol, currentPrice, high24h, low24h) {
    console.log(`\n${'='.repeat(50)}`);
    console.log(`优化 ${symbol} 网格策略`);
    console.log('='.repeat(50));
    console.log(`当前价：${currentPrice} | 24h: ${low24h} - ${high24h}`);
    
    // 1. 撤销所有挂单
    console.log('\n🔄 撤销所有挂单...');
    const cancelResult = await cancelAllOrders(symbol);
    if (cancelResult.code === '00000') {
        console.log('✅ 撤销成功');
    } else {
        console.log(`⚠️ 撤销结果：${cancelResult.msg}`);
    }
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 2. 计算优化后的网格参数
    const bufferPercent = 0.20; // 20% 缓冲
    const newMin = low24h * (1 - bufferPercent);
    const newMax = high24h * (1 + bufferPercent);
    const gridNum = 15; // 减少网格数，增加每个网格利润
    const gridStep = (newMax - newMin) / gridNum;
    
    console.log(`\n📐 新网格参数:`);
    console.log(`   区间：${newMin.toFixed(0)} - ${newMax.toFixed(0)}`);
    console.log(`   网格数：${gridNum}`);
    console.log(`   网格间距：${gridStep.toFixed(2)} (${(gridStep/currentPrice*100).toFixed(2)}%)`);
    
    // 3. 计算每单金额 (根据实际可用资金)
    const totalUSDT = 300; // 保守使用 300 USDT
    const perGridUSDT = totalUSDT / gridNum;
    
    console.log(`\n💰 资金分配:`);
    console.log(`   总资金：${totalUSDT} USDT`);
    console.log(`   每格：${perGridUSDT.toFixed(2)} USDT`);
    
    // 4. 放置买单 (当前价以下)
    console.log(`\n📈 放置买单...`);
    let buyCount = 0;
    for (let i = 0; i < gridNum / 2; i++) {
        const buyPrice = currentPrice - (i + 1) * gridStep;
        if (buyPrice < newMin) break;
        
        const quantity = perGridUSDT / buyPrice;
        const result = await placeOrder(symbol, 'buy', buyPrice, quantity);
        
        if (result.code === '00000') {
            console.log(`   ✅ 买单 ${i+1}: ${buyPrice.toFixed(2)} | ${quantity.toFixed(6)}`);
            buyCount++;
        } else {
            console.log(`   ❌ 买单 ${i+1}: ${result.msg}`);
        }
        
        await new Promise(resolve => setTimeout(resolve, 300));
    }
    
    // 5. 放置卖单 (当前价以上)
    console.log(`\n📉 放置卖单...`);
    let sellCount = 0;
    for (let i = 0; i < gridNum / 2; i++) {
        const sellPrice = currentPrice + (i + 1) * gridStep;
        if (sellPrice > newMax) break;
        
        const quantity = perGridUSDT / sellPrice;
        const result = await placeOrder(symbol, 'sell', sellPrice, quantity);
        
        if (result.code === '00000') {
            console.log(`   ✅ 卖单 ${i+1}: ${sellPrice.toFixed(2)} | ${quantity.toFixed(6)}`);
            sellCount++;
        } else {
            console.log(`   ❌ 卖单 ${i+1}: ${result.msg}`);
        }
        
        await new Promise(resolve => setTimeout(resolve, 300));
    }
    
    console.log(`\n✅ ${symbol} 优化完成！`);
    console.log(`   买单：${buyCount} 个 | 卖单：${sellCount} 个`);
    
    return { buyCount, sellCount };
}

async function main() {
    console.log('🚀 开始优化网格策略...\n');
    
    // 获取 BTC 数据
    const btcData = await getMarketData('BTCUSDT');
    if (btcData) {
        await optimizeGrid(
            'BTCUSDT',
            parseFloat(btcData.lastPr),
            parseFloat(btcData.high24h),
            parseFloat(btcData.low24h)
        );
    }
    
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 获取 SOL 数据
    const solData = await getMarketData('SOLUSDT');
    if (solData) {
        await optimizeGrid(
            'SOLUSDT',
            parseFloat(solData.lastPr),
            parseFloat(solData.high24h),
            parseFloat(solData.low24h)
        );
    }
    
    console.log('\n' + '='.repeat(50));
    console.log('🎉 所有优化完成！');
    console.log('='.repeat(50));
}

main().catch(e => {
    console.error('❌ 错误:', e.message);
});
