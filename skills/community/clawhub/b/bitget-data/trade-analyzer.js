#!/usr/bin/env node
// 实时交易分析 + 策略总结 + 动态优化

const fs = require('fs');
const crypto = require('crypto');
const http = require('http');
const https = require('https');

const DATA_DIR = __dirname;
const CONFIG_FILE = DATA_DIR + '/config.json';
const LOG_FILE = DATA_DIR + '/trade-analysis.log';
const SUMMARY_FILE = DATA_DIR + '/strategy-summary.json';

const CONFIG = JSON.parse(fs.readFileSync(CONFIG_FILE));

function sign(message) {
    return crypto.createHmac('sha256', CONFIG.secretKey).update(message).digest('base64');
}

function request(endpoint, method = 'GET', params = {}) {
    return new Promise((resolve, reject) => {
        const timestamp = Date.now().toString();
        let body = '';
        
        if (method === 'POST') {
            body = JSON.stringify(params);
        }
        
        const signStr = timestamp + method + endpoint + body;
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
                path: endpoint + (method === 'GET' && Object.keys(params).length ? '?' + new URLSearchParams(params) : ''),
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
                        resolve({ raw: data });
                    }
                });
            });
            
            req.on('error', reject);
            if (method === 'POST' && body) req.write(body);
            req.end();
        });
        
        proxyReq.on('error', reject);
        proxyReq.end();
    });
}

function log(msg) {
    const line = `[${new Date().toLocaleString('zh-CN')}] ${msg}`;
    console.log(line);
    fs.appendFileSync(LOG_FILE, line + '\n');
}

async function getMarketData(symbol) {
    const result = await request('/api/v2/spot/market/tickers', 'GET', { symbol });
    return result.data && result.data[0] ? result.data[0] : null;
}

async function getOpenOrders(symbol) {
    const result = await request('/api/v2/spot/trade/unfilled-orders', 'GET', { symbol, limit: 100 });
    return result.data || [];
}

async function getFilledOrders(symbol, startTime) {
    const result = await request('/api/v2/spot/trade/fills', 'GET', { 
        symbol, 
        startTime: startTime.toString(),
        limit: 100 
    });
    return result.data || [];
}

async function getBalance() {
    const result = await request('/api/v2/spot/account/assets', 'GET');
    return result.data || [];
}

async function analyzeAndOptimize() {
    log('\n' + '='.repeat(60));
    log('📊 实时交易分析与策略优化');
    log('='.repeat(60));
    
    const symbols = [
        { symbol: 'BTCUSDT', name: 'Bitcoin', minSize: 0.0001 },
        { symbol: 'SOLUSDT', name: 'Solana', minSize: 0.01 }
    ];
    
    const summary = {
        timestamp: Date.now(),
        strategies: []
    };
    
    for (const { symbol, name, minSize } of symbols) {
        log(`\n${'─'.repeat(60)}`);
        log(`分析 ${name} (${symbol})`);
        log('─'.repeat(60));
        
        // 1. 获取市场数据
        const market = await getMarketData(symbol);
        if (!market) continue;
        
        const currentPrice = parseFloat(market.lastPr);
        const high24h = parseFloat(market.high24h);
        const low24h = parseFloat(market.low24h);
        const change24h = parseFloat(market.change24h) * 100;
        const volatility = (high24h - low24h) / low24h * 100;
        
        log(`\n📈 市场行情:`);
        log(`   当前价：${currentPrice}`);
        log(`   24h 区间：${low24h} - ${high24h}`);
        log(`   24h 涨跌：${change24h.toFixed(2)}%`);
        log(`   波动率：${volatility.toFixed(2)}%`);
        
        // 2. 获取挂单
        const orders = await getOpenOrders(symbol);
        const buyOrders = orders.filter(o => o.side === 'buy');
        const sellOrders = orders.filter(o => o.side === 'sell');
        
        log(`\n📋 挂单分析:`);
        log(`   总挂单：${orders.length}`);
        log(`   买单：${buyOrders.length} | 卖单：${sellOrders.length}`);
        
        if (buyOrders.length > 0) {
            const buyPrices = buyOrders.map(o => parseFloat(o.price)).sort((a,b) => a-b);
            log(`   买单区间：${buyPrices[0]} - ${buyPrices[buyPrices.length-1]}`);
        }
        
        if (sellOrders.length > 0) {
            const sellPrices = sellOrders.map(o => parseFloat(o.price)).sort((a,b) => a-b);
            log(`   卖单区间：${sellPrices[0]} - ${sellPrices[sellPrices.length-1]}`);
        }
        
        // 3. 获取已成交订单（过去 24 小时）
        const startTime = Date.now() - 24 * 60 * 60 * 1000;
        const fills = await getFilledOrders(symbol, startTime);
        
        const buyFills = fills.filter(f => f.side === 'buy');
        const sellFills = fills.filter(f => f.side === 'sell');
        
        let totalBuy = 0, totalSell = 0, profit = 0;
        
        buyFills.forEach(f => {
            totalBuy += parseFloat(f.quantity) * parseFloat(f.price);
        });
        
        sellFills.forEach(f => {
            totalSell += parseFloat(f.quantity) * parseFloat(f.price);
        });
        
        // 简化利润计算
        profit = totalSell - totalBuy;
        
        log(`\n💰 24h 成交统计:`);
        log(`   成交次数：${fills.length} (买${buyFills.length} / 卖${sellFills.length})`);
        log(`   买入金额：${totalBuy.toFixed(2)} USDT`);
        log(`   卖出金额：${totalSell.toFixed(2)} USDT`);
        log(`   估算盈利：${profit.toFixed(2)} USDT`);
        
        // 4. 策略评估与优化建议
        log(`\n💡 策略评估:`);
        
        const strategy = {
            symbol,
            timestamp: Date.now(),
            metrics: {
                currentPrice,
                volatility,
                orders: orders.length,
                buyOrders: buyOrders.length,
                sellOrders: sellOrders.length,
                fills24h: fills.length,
                profit24h: profit
            },
            suggestions: []
        };
        
        // 评估 1: 挂单分布
        if (buyOrders.length < 3) {
            log(`   ⚠️ 买单过少，可能错过低吸机会`);
            strategy.suggestions.push('增加买单数量');
        } else if (sellOrders.length < 3) {
            log(`   ⚠️ 卖单过少，可能错过高抛机会`);
            strategy.suggestions.push('增加卖单数量');
        } else {
            log(`   ✅ 挂单分布合理`);
        }
        
        // 评估 2: 网格间距 vs 波动率
        if (orders.length >= 2) {
            const allPrices = orders.map(o => parseFloat(o.price)).sort((a,b) => a-b);
            const avgGridStep = (allPrices[allPrices.length-1] - allPrices[0]) / (allPrices.length - 1);
            const gridStepPercent = avgGridStep / currentPrice * 100;
            
            if (gridStepPercent < volatility / 2) {
                log(`   OK 网格密度适合当前波动 (${gridStepPercent.toFixed(2)}% < ${volatility.toFixed(2)}%)`);
            } else if (gridStepPercent > volatility * 2) {
                log(`   WARN 网格过宽，可能错过交易机会`);
                strategy.suggestions.push('缩小网格间距');
            } else {
                log(`   OK 网格间距合理 (${gridStepPercent.toFixed(2)}%)`);
            }
        }
        
        // 评估 3: 价格位置
        const pricePosition = (currentPrice - low24h) / (high24h - low24h) * 100;
        if (pricePosition < 20) {
            log(`   📍 价格在低位 (${pricePosition.toFixed(1)}%)，适合增加买单`);
            strategy.suggestions.push('当前低位，可增加买单密度');
        } else if (pricePosition > 80) {
            log(`   📍 价格在高位 (${pricePosition.toFixed(1)}%)，适合增加卖单`);
            strategy.suggestions.push('当前高位，可增加卖单密度');
        } else {
            log(`   📍 价格在中间 (${pricePosition.toFixed(1)}%)`);
        }
        
        // 评估 4: 盈利情况
        if (profit > 0) {
            log(`   ✅ 盈利中 (+${profit.toFixed(2)} USDT)`);
        } else if (profit < 0) {
            log(`   ⚠️ 暂时亏损 (${profit.toFixed(2)} USDT)，耐心等待反弹`);
        } else {
            log(`   ⏳ 暂无成交`);
        }
        
        summary.strategies.push(strategy);
    }
    
    // 5. 获取总余额
    log(`\n${'─'.repeat(60)}`);
    log('💰 账户总览:');
    
    const balance = await getBalance();
    let totalUSDT = 0;
    
    balance.forEach(asset => {
        const available = parseFloat(asset.available);
        const frozen = parseFloat(asset.frozen);
        const total = available + frozen;
        
        if (total > 0) {
            log(`   ${asset.coinName || 'UNKNOWN'}: ${available.toFixed(4)} + ${frozen.toFixed(4)} (冻结) = ${total.toFixed(4)}`);
            if (asset.coinName === 'USDT') {
                totalUSDT = total;
            }
        }
    });
    
    log(`\n📊 资金利用率：${((totalUSDT - 0.11) / totalUSDT * 100).toFixed(1)}%`);
    
    // 6. 保存总结
    fs.writeFileSync(SUMMARY_FILE, JSON.stringify(summary, null, 2));
    log(`\n📝 分析总结已保存到：${SUMMARY_FILE}`);
    
    log(`\n${'='.repeat(60)}`);
    log('✅ 分析完成！');
    log('='.repeat(60));
    
    return summary;
}

// 主循环
async function main() {
    log('🚀 启动实时交易分析系统...\n');
    
    // 立即执行一次
    await analyzeAndOptimize();
    
    // 然后每 30 分钟分析一次
    setInterval(async () => {
        await analyzeAndOptimize();
    }, 30 * 60 * 1000);
}

main().catch(e => {
    log(`❌ 错误：${e.message}`);
    process.exit(1);
});
