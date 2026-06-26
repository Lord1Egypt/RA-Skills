#!/usr/bin/env node
/**
 * 动态调整策略 V2 - 使用 Bitget 公开 API
 */

const https = require('https');
const fs = require('fs');

const SETTINGS = JSON.parse(fs.readFileSync('grid_settings.json', 'utf-8'));

// 从 Bitget 获取价格和 K 线（公开 API）
function getBitget(url) {
    return new Promise((resolve) => {
        const req = https.get(`https://api.bitget.com${url}`, {timeout: 10000}, (res) => {
            let data = '';
            res.on('data', c => data += c);
            res.on('end', () => {
                try { resolve(JSON.parse(data)); } catch(e) { resolve(null); }
            });
        });
        req.on('error', () => resolve(null));
    });
}

async function getPrice(symbol) {
    const data = await getBitget(`/api/v2/spot/market/ticker?symbol=${symbol}`);
    if(data && data.code === '00000' && data.data) {
        return +data.data.last;
    }
    return 0;
}

async function getKline(symbol, limit = 20) {
    const data = await getBitget(`/api/v2/spot/market/candles?symbol=${symbol}&granularity=1h&limit=${limit}`);
    if(data && data.code === '00000' && data.data) {
        return data.data.map(k => ({
            open: +k[1], high: +k[2], low: +k[3], close: +k[4], volume: +k[5]
        }));
    }
    return [];
}

// 计算 RSI
function calculateRSI(klines, period = 14) {
    if(klines.length < period + 1) return 50;
    let gains = 0, losses = 0;
    for(let i = klines.length - period; i < klines.length; i++) {
        const change = klines[i].close - klines[i-1].close;
        if(change > 0) gains += change;
        else losses -= change;
    }
    const avgGain = gains / period;
    const avgLoss = losses / period;
    if(avgLoss === 0) return 100;
    return 100 - (100 / (1 + avgGain / avgLoss));
}

// 根据 RSI 计算买卖单比例
function getRatio(rsi) {
    if(rsi > 70) return { buy: 0.3, sell: 0.7, signal: '🔴 超买', advice: '减少买单，增加卖单' };
    if(rsi > 60) return { buy: 0.4, sell: 0.6, signal: '🟡 偏多', advice: '适度减少买单' };
    if(rsi > 45) return { buy: 0.5, sell: 0.5, signal: '🟢 中性', advice: '买卖均衡' };
    if(rsi > 35) return { buy: 0.6, sell: 0.4, signal: '🟡 偏空', advice: '适度增加买单' };
    return { buy: 0.7, sell: 0.3, signal: '🟢 超卖', advice: '大幅增加买单' };
}

async function analyze(symbol, name, config) {
    console.log(`\n${'='.repeat(70)}`);
    console.log(`📊 ${name} (${symbol}) 动态调整分析`);
    console.log('='.repeat(70));
    
    const [price, klines] = await Promise.all([
        getPrice(symbol),
        getKline(symbol, 20)
    ]);
    
    if(price === 0) {
        console.log('❌ 无法获取价格数据');
        return null;
    }
    
    const rsi = calculateRSI(klines);
    const ratio = getRatio(rsi);
    
    // 计算网格
    const spacing = (config.priceMax - config.priceMin) / config.gridNum;
    const totalOrders = config.gridNum;
    const sellCount = Math.round(totalOrders * ratio.sell);
    const buyCount = totalOrders - sellCount;
    
    // 生成价格
    const prices = [];
    for(let i = 0; i <= config.gridNum; i++) {
        prices.push(config.priceMin + spacing * i);
    }
    
    // 找到中间价
    const midIndex = Math.floor(prices.length / 2);
    const midPrice = prices[midIndex];
    
    // 卖单在现价上方，买单在下方
    const sellPrices = prices.filter(p => p >= midPrice);
    const buyPrices = prices.filter(p => p <= midPrice);
    
    // 根据 RSI 调整
    const adjustedBuyCount = Math.round(buyCount * (ratio.buy / 0.5));
    const adjustedSellCount = Math.round(sellCount * (ratio.sell / 0.5));
    
    console.log(`\n📈 市场状态`);
    console.log(`   当前价：${price.toFixed(2)} USDT`);
    console.log(`   RSI(14): ${rsi.toFixed(2)} ${ratio.signal}`);
    console.log(`   24h 趋势：${klines.length > 1 ? ((klines[klines.length-1].close - klines[0].close) / klines[0].close * 100).toFixed(2) + '%' : 'N/A'}`);
    
    console.log(`\n📊 动态比例`);
    console.log(`   建议：买单 ${Math.round(ratio.buy * 100)}% | 卖单 ${Math.round(ratio.sell * 100)}%`);
    console.log(`   策略：${ratio.advice}`);
    
    console.log(`\n📋 网格配置`);
    console.log(`   区间：${config.priceMin.toLocaleString()} - ${config.priceMax.toLocaleString()} USDT`);
    console.log(`   网格数：${config.gridNum}`);
    console.log(`   间距：${spacing.toFixed(2)} (${(spacing / config.priceMin * 100).toFixed(2)}%)`);
    
    console.log(`\n📥 买单建议 (${adjustedBuyCount}个)`);
    const finalBuyPrices = prices.slice(0, adjustedBuyCount + 1);
    finalBuyPrices.forEach((p, i) => {
        if(i < finalBuyPrices.length - 1) {
            console.log(`   ${i+1}. ${p.toFixed(2)} @ ${config.amount} USDT`);
        }
    });
    
    console.log(`\n📤 卖单建议 (${adjustedSellCount}个)`);
    const finalSellPrices = prices.slice(-adjustedSellCount - 1);
    finalSellPrices.forEach((p, i) => {
        if(i > 0) {
            console.log(`   ${i}. ${p.toFixed(2)} @ ${config.amount} USDT`);
        }
    });
    
    // 资金计算
    const buyTotal = adjustedBuyCount * config.amount;
    const sellTotal = adjustedSellCount * config.amount;
    
    console.log(`\n💰 资金需求`);
    console.log(`   买单：${buyTotal} USDT`);
    console.log(`   卖单：${sellTotal} USDT (需持仓)`);
    console.log(`   总计：${buyTotal + sellTotal} USDT`);
    
    // 生成新配置
    const newConfig = {
        ...config,
        buyOrders: adjustedBuyCount,
        sellOrders: adjustedSellCount,
        buyPrices: finalBuyPrices.slice(0, -1),
        sellPrices: finalSellPrices.slice(1),
        rsi: rsi.toFixed(2),
        ratio: ratio.signal,
        adjustedAt: new Date().toISOString()
    };
    
    return newConfig;
}

async function main() {
    console.log('🔄 动态调整策略 V2 - 基于 RSI 自动调整\n');
    console.log('时间:', new Date().toLocaleString('zh-CN'));
    console.log('策略规则:');
    console.log('  RSI > 70: 买单 30% | 卖单 70% (超买，多卖)');
    console.log('  RSI 60-70: 买单 40% | 卖单 60% (偏多)');
    console.log('  RSI 45-60: 买单 50% | 卖单 50% (中性)');
    console.log('  RSI 35-45: 买单 60% | 卖单 40% (偏空)');
    console.log('  RSI < 35: 买单 70% | 卖单 30% (超卖，多买)');
    console.log('\n' + '='.repeat(70));
    
    const results = {};
    
    if(SETTINGS.btc) {
        results.btc = await analyze('BTCUSDT', '比特币', SETTINGS.btc);
    }
    if(SETTINGS.sol) {
        results.sol = await analyze('SOLUSDT', 'Solana', SETTINGS.sol);
    }
    if(SETTINGS.eth) {
        results.eth = await analyze('ETHUSDT', '以太坊', SETTINGS.eth);
    }
    
    // 保存调整建议
    const report = {
        time: new Date().toISOString(),
        strategy: 'dynamic-rsi',
        adjustments: results
    };
    
    fs.writeFileSync('dynamic_adjustments.json', JSON.stringify(report, null, 2), 'utf-8');
    
    console.log('\n' + '='.repeat(70));
    console.log('📋 动态调整汇总');
    console.log('='.repeat(70));
    
    for(const [key, r] of Object.entries(results)) {
        if(!r) continue;
        const name = key.toUpperCase();
        console.log(`\n${name}:`);
        console.log(`   RSI: ${r.rsi} ${r.ratio}`);
        console.log(`   买单：${r.buyOrders}个 | 卖单：${r.sellOrders}个`);
        console.log(`   比例：${Math.round(r.buyOrders / (r.buyOrders + r.sellOrders) * 100)}% : ${Math.round(r.sellOrders / (r.buyOrders + r.sellOrders) * 100)}%`);
    }
    
    console.log('\n' + '='.repeat(70));
    console.log('✅ 动态调整分析完成！');
    console.log('='.repeat(70));
    console.log('\n💾 调整建议已保存到：dynamic_adjustments.json');
    console.log('\n🚀 下一步:');
    console.log('1. 查看上方建议');
    console.log('2. 确认要应用的配置');
    console.log('3. 运行：node apply-dynamic-grid.js BTC|SOL|ETH (应用指定币种)');
    console.log('4. 或运行：node apply-dynamic-grid.js ALL (应用所有币种)');
    
    // 生成应用脚本
    const applyScript = `
const fs = require('fs');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const CONFIG = JSON.parse(fs.readFileSync('config.json'));
const ADJUSTMENTS = JSON.parse(fs.readFileSync('dynamic_adjustments.json'));

function sign(msg) {
    return crypto.createHmac('sha256', CONFIG.secretKey).update(msg).digest('base64');
}

function api(endpoint, method = 'GET', body = null) {
    return new Promise((resolve) => {
        const now = new Date();
        const timestamp = now.toISOString().split('.')[0] + '.000Z';
        const signStr = timestamp + method + endpoint + (body ? JSON.stringify(body) : '');
        const signature = sign(signStr);
        
        const proxy = http.request({hostname:'127.0.0.1',port:7897,path:'api.bitget.com:443',method:'CONNECT'});
        proxy.on('connect', (res, socket) => {
            const req = https.request({socket, hostname:'api.bitget.com', port:443, path:endpoint, method,
                headers:{'ACCESS-KEY': CONFIG.apiKey, 'ACCESS-SIGN': signature, 'ACCESS-TIMESTAMP': timestamp,
                    'ACCESS-PASSPHRASE': CONFIG.passphrase, 'Content-Type': 'application/json'}});
            let data = '';
            req.on('response', res => { res.on('data', c => data += c); res.on('end', () => { try{resolve(JSON.parse(data));}catch(e){resolve({raw:data});} }); });
            req.end();
        });
        proxy.end();
    });
}

async function cancelOrders(symbol) {
    const pending = await api(\`/api/v2/spot/trade/orders-pending?symbol=\${symbol}\`);
    if(pending.data && pending.data.length > 0) {
        console.log(\`取消 \${symbol} \${pending.data.length} 个挂单...\`);
        for(const order of pending.data) {
            await api(\`/api/v2/spot/trade/cancel-order?symbol=\${symbol}&orderId=\${order.orderId}\`, 'POST');
        }
        await new Promise(r => setTimeout(r, 500));
    }
}

async function placeOrder(symbol, side, price, amount) {
    const size = (amount / price).toFixed(6);
    const body = { symbol, side, orderType: 'limit', price: price.toFixed(2), quantity: size };
    const result = await api('/api/v2/spot/trade/place-order', 'POST', body);
    return result;
}

async function deployGrid(symbol, config) {
    console.log(\`\\n🚀 部署 \${symbol} 动态网格...\`);
    
    await cancelOrders(symbol);
    
    console.log(\`📥 部署 \${config.buyOrders} 个买单...\`);
    for(const price of config.buyPrices) {
        const result = await placeOrder(symbol, 'buy', price, config.amount);
        if(result.code === '00000') {
            console.log(\`   ✅ \${price.toFixed(2)}\`);
        } else {
            console.log(\`   ⚠️  \${price.toFixed(2)}: \${result.msg || '失败'}\`);
        }
        await new Promise(r => setTimeout(r, 300));
    }
    
    console.log(\`📤 部署 \${config.sellOrders} 个卖单...\`);
    for(const price of config.sellPrices) {
        const result = await placeOrder(symbol, 'sell', price, config.amount);
        if(result.code === '00000') {
            console.log(\`   ✅ \${price.toFixed(2)}\`);
        } else {
            console.log(\`   ⚠️  \${price.toFixed(2)}: \${result.msg || '失败'}\`);
        }
        await new Promise(r => setTimeout(r, 300));
    }
    
    console.log(\`✅ \${symbol} 部署完成！\`);
}

async function main() {
    const target = process.argv[2] || 'ALL';
    const adj = ADJUSTMENTS.adjustments;
    
    console.log('🚀 应用动态网格配置\\n');
    
    if(target === 'ALL' || target === 'BTC') {
        if(adj.btc) await deployGrid('BTCUSDT', adj.btc);
    }
    if(target === 'ALL' || target === 'SOL') {
        if(adj.sol) await deployGrid('SOLUSDT', adj.sol);
    }
    if(target === 'ALL' || target === 'ETH') {
        if(adj.eth) await deployGrid('ETHUSDT', adj.eth);
    }
    
    console.log('\\n✅ 所有网格部署完成！\\n');
}

main().catch(console.error);
`;
    
    fs.writeFileSync('apply-dynamic-grid.js', applyScript, 'utf-8');
    console.log('\n✅ 应用脚本已生成：apply-dynamic-grid.js\n');
}

main();
