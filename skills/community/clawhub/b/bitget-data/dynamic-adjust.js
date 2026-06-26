#!/usr/bin/env node
/**
 * 动态调整策略 - 根据 RSI 自动调整买卖单密度
 */

const https = require('https');
const fs = require('fs');
const crypto = require('crypto');

const CONFIG = JSON.parse(fs.readFileSync('config.json', 'utf-8'));
const SETTINGS = JSON.parse(fs.readFileSync('grid_settings.json', 'utf-8'));

// 获取 RSI
async function getRSI(symbol, period = 14) {
    return new Promise((resolve) => {
        const url = `https://api.binance.com/api/v3/klines?symbol=${symbol}&interval=1h&limit=${period + 1}`;
        https.get(url, {timeout: 10000}, (res) => {
            let data = '';
            res.on('data', c => data += c);
            res.on('end', () => {
                try {
                    const klines = JSON.parse(data);
                    if(klines.length < period + 1) { resolve(50); return; }
                    
                    let gains = 0, losses = 0;
                    for(let i = 1; i < klines.length; i++) {
                        const change = (+klines[i][4]) - (+klines[i-1][4]);
                        if(change > 0) gains += change;
                        else losses -= change;
                    }
                    const avgGain = gains / period;
                    const avgLoss = losses / period;
                    if(avgLoss === 0) { resolve(100); return; }
                    const rsi = 100 - (100 / (1 + avgGain / avgLoss));
                    resolve(rsi);
                } catch(e) { resolve(50); }
            });
        }).on('error', () => resolve(50));
    });
}

// 获取当前价格
async function getPrice(symbol) {
    return new Promise((resolve) => {
        const url = `https://api.binance.com/api/v3/ticker/price?symbol=${symbol}`;
        https.get(url, {timeout: 5000}, (res) => {
            let data = '';
            res.on('data', c => data += c);
            res.on('end', () => {
                try {
                    const json = JSON.parse(data);
                    resolve(+json.price);
                } catch(e) { resolve(0); }
            });
        }).on('error', () => resolve(0));
    });
}

// 根据 RSI 计算买卖单比例
function getBuySellRatio(rsi) {
    if(rsi > 70) return { buy: 0.3, sell: 0.7, signal: '🔴 超买' };
    if(rsi > 60) return { buy: 0.4, sell: 0.6, signal: '🟡 偏多' };
    if(rsi > 45) return { buy: 0.5, sell: 0.5, signal: '🟢 中性' };
    if(rsi > 35) return { buy: 0.6, sell: 0.4, signal: '🟡 偏空' };
    return { buy: 0.7, sell: 0.3, signal: '🟢 超卖' };
}

// 计算网格价格
function calculateGridPrices(priceMin, priceMax, gridNum, buyRatio) {
    const spacing = (priceMax - priceMin) / gridNum;
    const prices = [];
    
    for(let i = 0; i <= gridNum; i++) {
        prices.push(priceMin + spacing * i);
    }
    
    const currentPrice = priceMin + spacing * gridNum / 2;
    const sellCount = Math.round(gridNum * (1 - buyRatio));
    const buyCount = gridNum - sellCount;
    
    // 卖单在上方，买单在下方
    const sellPrices = prices.slice(-sellCount - 1);
    const buyPrices = prices.slice(0, buyCount + 1);
    
    return { buyPrices, sellPrices, spacing };
}

async function analyzeAndAdjust(symbol, name, config) {
    console.log(`\n${'='.repeat(70)}`);
    console.log(`📊 ${name} (${symbol}) 动态调整`);
    console.log('='.repeat(70));
    
    const [price, rsi] = await Promise.all([
        getPrice(symbol),
        getRSI(symbol)
    ]);
    
    if(price === 0) {
        console.log('❌ 无法获取价格');
        return null;
    }
    
    const ratio = getBuySellRatio(rsi);
    
    console.log(`\n📈 市场状态`);
    console.log(`   当前价：${price.toFixed(2)}`);
    console.log(`   RSI(14): ${rsi.toFixed(2)} ${ratio.signal}`);
    console.log(`   建议比例：买单 ${Math.round(ratio.buy * 100)}% | 卖单 ${Math.round(ratio.sell * 100)}%`);
    
    // 计算新网格
    const grid = calculateGridPrices(config.priceMin, config.priceMax, config.gridNum, ratio.buy);
    
    console.log(`\n📋 网格配置`);
    console.log(`   区间：${config.priceMin} - ${config.priceMax}`);
    console.log(`   网格数：${config.gridNum}`);
    console.log(`   间距：${grid.spacing.toFixed(2)} (${(grid.spacing / config.priceMin * 100).toFixed(2)}%)`);
    
    console.log(`\n📥 买单 (${grid.buyPrices.length - 1}个)`);
    grid.buyPrices.forEach((p, i) => {
        if(i < grid.buyPrices.length - 1) {
            console.log(`   ${i+1}. ${p.toFixed(2)} @ ${config.amount} USDT`);
        }
    });
    
    console.log(`\n📤 卖单 (${grid.sellPrices.length - 1}个)`);
    grid.sellPrices.forEach((p, i) => {
        if(i > 0) {
            console.log(`   ${i}. ${p.toFixed(2)} @ ${config.amount} USDT`);
        }
    });
    
    // 计算总投资
    const totalBuy = (grid.buyPrices.length - 1) * config.amount;
    const totalSell = (grid.sellPrices.length - 1) * config.amount;
    
    console.log(`\n💰 资金需求`);
    console.log(`   买单总额：${totalBuy.toFixed(0)} USDT`);
    console.log(`   卖单总额：${totalSell.toFixed(0)} USDT (持仓)`);
    console.log(`   总计：${(totalBuy + totalSell).toFixed(0)} USDT`);
    
    return {
        symbol, name, price, rsi, ratio,
        buyPrices: grid.buyPrices,
        sellPrices: grid.sellPrices,
        spacing: grid.spacing,
        amount: config.amount
    };
}

async function main() {
    console.log('🔄 动态调整策略 - 基于 RSI 自动调整买卖密度\n');
    console.log('时间:', new Date().toLocaleString('zh-CN'));
    console.log('策略：RSI>70 减少买单，RSI<30 增加买单\n');
    
    const results = [];
    
    // 分析各币种
    if(SETTINGS.btc) {
        results.push(await analyzeAndAdjust('BTCUSDT', '比特币', SETTINGS.btc));
    }
    if(SETTINGS.sol) {
        results.push(await analyzeAndAdjust('SOLUSDT', 'Solana', SETTINGS.sol));
    }
    if(SETTINGS.eth) {
        results.push(await analyzeAndAdjust('ETHUSDT', '以太坊', SETTINGS.eth));
    }
    
    // 生成调整报告
    console.log('\n' + '='.repeat(70));
    console.log('📋 动态调整汇总');
    console.log('='.repeat(70));
    
    const summary = {
        time: new Date().toISOString(),
        adjustments: []
    };
    
    for(const r of results) {
        if(!r) continue;
        
        console.log(`\n${r.name}:`);
        console.log(`   RSI: ${r.rsi.toFixed(2)} ${r.ratio.signal}`);
        console.log(`   买单：${r.buyPrices.length - 1}个 @ ${r.amount} USDT`);
        console.log(`   卖单：${r.sellPrices.length - 1}个 @ ${r.amount} USDT`);
        
        summary.adjustments.push({
            symbol: r.symbol,
            rsi: r.rsi.toFixed(2),
            signal: r.ratio.signal,
            buyCount: r.buyPrices.length - 1,
            sellCount: r.sellPrices.length - 1,
            ratio: `${Math.round(r.ratio.buy * 100)}:${Math.round(r.ratio.sell * 100)}`
        });
    }
    
    // 保存调整记录
    fs.writeFileSync('dynamic_adjustments.json', JSON.stringify(summary, null, 2), 'utf-8');
    
    console.log('\n' + '='.repeat(70));
    console.log('✅ 动态调整分析完成！');
    console.log('='.repeat(70));
    console.log('\n💡 下一步操作:');
    console.log('1. 查看调整建议（上方）');
    console.log('2. 运行 node deploy-dynamic-grid.js 应用新配置');
    console.log('3. 或手动调整各币种网格');
    
    // 生成部署脚本
    const deployScript = `
const fs = require('fs');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const CONFIG = JSON.parse(fs.readFileSync('config.json'));
const SETTINGS = ${JSON.stringify(SETTINGS, null, 2)};

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

async function cancelAllOrders(symbol) {
    const orders = await api(\`/api/v2/spot/trade/orders-pending?symbol=\${symbol}\`);
    if(orders.data && orders.data.length > 0) {
        console.log(\`取消 \${symbol} \${orders.data.length} 个挂单...\`);
        for(const order of orders.data) {
            await api(\`/api/v2/spot/trade/cancel-order?symbol=\${symbol}&orderId=\${order.orderId}\`, 'POST');
        }
    }
}

async function placeOrder(symbol, side, price, amount) {
    const size = (amount / price).toFixed(8);
    const body = { symbol, side, orderType: 'limit', price: price.toFixed(2), quantity: size };
    const result = await api('/api/v2/spot/trade/place-order', 'POST', body);
    return result;
}

async function deployGrid(symbol, name, buyPrices, sellPrices, amount) {
    console.log(\`\\n🚀 部署 \${name} 网格...\`);
    
    // 取消旧订单
    await cancelAllOrders(symbol);
    
    // 部署买单
    console.log(\`📥 部署 \${buyPrices.length - 1} 个买单...\`);
    for(let i = 0; i < buyPrices.length - 1; i++) {
        const price = buyPrices[i];
        const result = await placeOrder(symbol, 'buy', price, amount);
        if(result.code === '00000') {
            console.log(\`   ✅ 买单 \${price.toFixed(2)} OK\`);
        } else {
            console.log(\`   ❌ 买单 \${price.toFixed(2)} 失败：\${result.msg}\`);
        }
        await new Promise(r => setTimeout(r, 200));
    }
    
    // 部署卖单
    console.log(\`📤 部署 \${sellPrices.length - 1} 个卖单...\`);
    for(let i = 1; i < sellPrices.length; i++) {
        const price = sellPrices[i];
        const result = await placeOrder(symbol, 'sell', price, amount);
        if(result.code === '00000') {
            console.log(\`   ✅ 卖单 \${price.toFixed(2)} OK\`);
        } else {
            console.log(\`   ❌ 卖单 \${price.toFixed(2)} 失败：\${result.msg}\`);
        }
        await new Promise(r => setTimeout(r, 200));
    }
    
    console.log(\`✅ \${name} 网格部署完成！\`);
}

async function main() {
    console.log('🚀 动态网格部署脚本\\n');
    
    // 这里填入动态调整后的价格
    // 运行前请从 dynamic_adjustments.json 读取或手动填写
    
    console.log('⚠️ 请从 dynamic_adjustments.json 读取价格后手动部署');
    console.log('或联系主人确认要应用的配置');
}

main();
`;
    
    fs.writeFileSync('deploy-dynamic-grid.js', deployScript, 'utf-8');
    console.log('\n✅ 部署脚本已生成：deploy-dynamic-grid.js\n');
}

main();
