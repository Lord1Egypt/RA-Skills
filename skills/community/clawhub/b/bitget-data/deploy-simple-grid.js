#!/usr/bin/env node
/**
 * Bitget 简易网格部署脚本
 * 直接部署买单 + 卖单，不依赖代理
 */

const fs = require('fs');
const crypto = require('crypto');
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
        
        const options = {
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
                    resolve({ raw: data.substring(0, 200) });
                }
            });
        });
        
        req.on('error', e => resolve({ error: e.message }));
        if (bodyStr) req.write(bodyStr);
        req.end();
    });
}

async function deployGrid(coin) {
    const config = SETTINGS[coin];
    if (!config || !config.enabled) {
        log(`⏭️ 跳过 ${coin} - 未启用`, 'INFO');
        return;
    }
    
    const symbol = config.symbol;
    log(`\n🚀 部署 ${symbol} 网格...`, 'INFO');
    log(`   网格数：${config.gridNum} 格`, 'INFO');
    log(`   价格区间：${config.priceMin} - ${config.priceMax}`, 'INFO');
    log(`   每格金额：${config.amount} USDT`, 'INFO');
    
    // 获取当前价格
    const tickerResult = await request('/spot/market/tickers', 'GET', { symbol });
    const currentPrice = parseFloat(tickerResult.data?.[0]?.lastPr || 0);
    
    if (!currentPrice || currentPrice === 0) {
        log(`   ❌ 无法获取价格`, 'ERROR');
        return;
    }
    
    log(`   💰 当前价格：${currentPrice} USDT`, 'INFO');
    
    // 计算网格
    const priceRange = config.priceMax - config.priceMin;
    const gridSpacing = priceRange / config.gridNum;
    log(`   📐 网格间距：${gridSpacing.toFixed(4)} (${(gridSpacing/currentPrice*100).toFixed(2)}%)`, 'INFO');
    
    // 获取精度
    const priceScale = coin === 'eth' ? 2 : 2;
    const sizeScale = coin === 'eth' ? 4 : 2;
    
    // 创建买单（当前价下方）
    log(`\n   📈 创建买单网格...`, 'INFO');
    const buyLevels = Math.floor(config.gridNum / 2);
    let placedBuy = 0;
    
    for (let i = 0; i < buyLevels; i++) {
        const price = currentPrice * (1 - (i + 1) * (gridSpacing / currentPrice));
        if (price < config.priceMin) break;
        
        const size = config.amount / price;
        const priceStr = price.toFixed(priceScale);
        const sizeStr = size.toFixed(sizeScale);
        
        // 检查最小订单金额
        const orderValue = price * size;
        if (orderValue < (config.minOrderValue || 1)) {
            log(`   ⚠️ 订单金额 ${orderValue.toFixed(2)} < ${config.minOrderValue || 1}，跳过`, 'WARN');
            continue;
        }
        
        const result = await request('/spot/trade/place-order', 'POST', {}, {
            symbol: symbol,
            side: 'buy',
            orderType: 'limit',
            price: priceStr,
            size: sizeStr,
            force: 'GTC'
        });
        
        if (result.code === '00000' || result.msg === 'success') {
            placedBuy++;
            log(`   ✅ 买单 #${i+1}: ${priceStr} x ${sizeStr}`, 'INFO');
        } else {
            log(`   ❌ 买单失败：${result.msg || result.error}`, 'WARN');
        }
        
        // 避免限流
        await sleep(200);
    }
    
    // 创建卖单（当前价上方）
    log(`\n   📉 创建卖单网格...`, 'INFO');
    const sellLevels = config.gridNum - buyLevels;
    let placedSell = 0;
    
    // 注意：卖单需要持仓，这里先尝试挂单
    for (let i = 0; i < sellLevels; i++) {
        const price = currentPrice * (1 + (i + 1) * (gridSpacing / currentPrice));
        if (price > config.priceMax) break;
        
        const size = config.amount / price;
        const priceStr = price.toFixed(priceScale);
        const sizeStr = size.toFixed(sizeScale);
        
        const orderValue = price * size;
        if (orderValue < (config.minOrderValue || 1)) continue;
        
        const result = await request('/spot/trade/place-order', 'POST', {}, {
            symbol: symbol,
            side: 'sell',
            orderType: 'limit',
            price: priceStr,
            size: sizeStr,
            force: 'GTC'
        });
        
        if (result.code === '00000' || result.msg === 'success') {
            placedSell++;
            log(`   ✅ 卖单 #${i+1}: ${priceStr} x ${sizeStr}`, 'INFO');
        } else {
            log(`   ❌ 卖单失败：${result.msg || result.error}`, 'WARN');
        }
        
        await sleep(200);
    }
    
    log(`\n   ✅ ${symbol} 部署完成：`, 'INFO');
    log(`      总订单：${placedBuy + placedSell} 个 (买${placedBuy} / 卖${placedSell})`, 'INFO');
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function main() {
    log('='.repeat(60), 'INFO');
    log('🚀 Bitget 简易网格部署', 'INFO');
    log('='.repeat(60), 'INFO');
    
    try {
        await deployGrid('sol');
        await deployGrid('eth');
        
        log('\n' + '='.repeat(60), 'INFO');
        log('✅ 部署完成！', 'INFO');
        log('='.repeat(60), 'INFO');
    } catch (error) {
        log(`❌ 部署异常：${error.message}`, 'ERROR');
    }
}

main();
