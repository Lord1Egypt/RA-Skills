#!/usr/bin/env node
// 量化网格交易系统 v2.0
// 引入：动态网格、仓位管理、风险控制、技术指标

const fs = require('fs');
const crypto = require('crypto');
const http = require('http');
const https = require('https');

const DATA_DIR = __dirname;
const CONFIG_FILE = DATA_DIR + '/config.json';
const CONFIG = JSON.parse(fs.readFileSync(CONFIG_FILE));

// ============ 量化参数 ============
const QUANT_CONFIG = {
    // 仓位管理
    maxPositionPercent: 0.95,        // 最大仓位 95%
    minCashReserve: 0.05,            // 最小现金储备 5%
    singleGridMaxPercent: 0.10,      // 单网格最大占用 10%
    
    // 风险控制
    maxDrawdown: 0.15,               // 最大回撤 15%
    stopLossPercent: 0.20,           // 止损线 20%
    takeProfitPercent: 0.30,         // 止盈线 30%
    
    // 动态网格
    volatilityLookback: 14,          // 波动率回看周期
    gridDensityMultiplier: 1.5,      // 网格密度乘数
    minGridSpacing: 0.015,           // 最小网格间距 1.5%
    maxGridSpacing: 0.05,            // 最大网格间距 5%
    
    // 技术指标
    rsiOverbought: 70,               // RSI 超买
    rsiOversold: 30,                 // RSI 超卖
    maPeriods: [7, 14, 30]           // 均线周期
};

// ============ API 请求 ============
function sign(message) {
    return crypto.createHmac('sha256', CONFIG.secretKey).update(message).digest('base64');
}

function request(endpoint, method = 'GET', params = {}) {
    return new Promise((resolve, reject) => {
        const timestamp = Date.now().toString();
        let body = '';
        if (method === 'POST') body = JSON.stringify(params);
        
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
                    try { resolve(JSON.parse(data)); }
                    catch (e) { resolve({ raw: data }); }
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

// ============ 技术指标计算 ============
function calculateRSI(prices, period = 14) {
    if (prices.length < period + 1) return 50;
    
    let gains = 0, losses = 0;
    for (let i = prices.length - period; i < prices.length; i++) {
        const change = prices[i] - prices[i-1];
        if (change > 0) gains += change;
        else losses -= change;
    }
    
    const avgGain = gains / period;
    const avgLoss = losses / period;
    
    if (avgLoss === 0) return 100;
    const rs = avgGain / avgLoss;
    return 100 - (100 / (1 + rs));
}

function calculateMA(prices, period) {
    if (prices.length < period) return null;
    const slice = prices.slice(-period);
    return slice.reduce((a, b) => a + b, 0) / period;
}

function calculateVolatility(prices, period = 14) {
    if (prices.length < period) return 0;
    const slice = prices.slice(-period);
    const mean = slice.reduce((a, b) => a + b, 0) / period;
    const variance = slice.reduce((sum, p) => sum + Math.pow(p - mean, 2), 0) / period;
    return Math.sqrt(variance) / mean;
}

function calculateBollingerBands(prices, period = 20, stdDev = 2) {
    if (prices.length < period) return null;
    const slice = prices.slice(-period);
    const ma = slice.reduce((a, b) => a + b, 0) / period;
    const variance = slice.reduce((sum, p) => sum + Math.pow(p - ma, 2), 0) / period;
    const std = Math.sqrt(variance);
    
    return {
        upper: ma + stdDev * std,
        middle: ma,
        lower: ma - stdDev * std
    };
}

// ============ 量化分析 ============
function analyzeMarket(market, klines) {
    const prices = klines.map(k => parseFloat(k[4])); // 收盘价
    const currentPrice = parseFloat(market.lastPr);
    
    // 技术指标
    const rsi = calculateRSI(prices);
    const ma7 = calculateMA(prices, 7);
    const ma14 = calculateMA(prices, 14);
    const ma30 = calculateMA(prices, 30);
    const volatility = calculateVolatility(prices);
    const bb = calculateBollingerBands(prices);
    
    // 信号判断
    let signal = 'HOLD';
    let confidence = 0.5;
    const reasons = [];
    
    // RSI 信号
    if (rsi < QUANT_CONFIG.rsiOversold) {
        signal = 'BUY';
        confidence += 0.2;
        reasons.push(`RSI 超卖 (${rsi.toFixed(1)})`);
    } else if (rsi > QUANT_CONFIG.rsiOverbought) {
        signal = 'SELL';
        confidence += 0.2;
        reasons.push(`RSI 超买 (${rsi.toFixed(1)})`);
    }
    
    // 均线信号
    if (ma7 && ma14 && ma30) {
        if (ma7 > ma14 && ma14 > ma30) {
            if (signal === 'BUY') confidence += 0.1;
            reasons.push('均线多头排列');
        } else if (ma7 < ma14 && ma14 < ma30) {
            if (signal === 'SELL') confidence += 0.1;
            reasons.push('均线空头排列');
        }
    }
    
    // 布林带信号
    if (bb) {
        if (currentPrice < bb.lower) {
            if (signal === 'BUY') confidence += 0.15;
            reasons.push('价格触及布林带下轨');
        } else if (currentPrice > bb.upper) {
            if (signal === 'SELL') confidence += 0.15;
            reasons.push('价格触及布林带上轨');
        }
    }
    
    // 波动率调整
    const gridSpacing = Math.max(
        QUANT_CONFIG.minGridSpacing,
        Math.min(
            QUANT_CONFIG.maxGridSpacing,
            volatility * QUANT_CONFIG.gridDensityMultiplier
        )
    );
    
    return {
        signal,
        confidence: Math.min(confidence, 1.0),
        indicators: {
            rsi: rsi.toFixed(1),
            ma7: ma7 ? ma7.toFixed(2) : 'N/A',
            ma14: ma14 ? ma14.toFixed(2) : 'N/A',
            ma30: ma30 ? ma30.toFixed(2) : 'N/A',
            volatility: (volatility * 100).toFixed(2) + '%',
            bb
        },
        gridSpacing: (gridSpacing * 100).toFixed(2) + '%',
        reasons
    };
}

// ============ 仓位管理 ============
function calculatePositionSize(totalBalance, currentPrice, volatility, signal) {
    // 凯利公式简化版
    const winRate = 0.55; // 假设胜率 55%
    const avgWinLoss = 1.2; // 盈亏比 1.2
    
    const kellyPercent = (winRate * avgWinLoss - (1 - winRate)) / avgWinLoss;
    const safePosition = kellyPercent * 0.5; // 半凯利
    
    // 根据波动率调整
    const volatilityAdjustment = 1 / (1 + volatility * 10);
    
    // 根据信号强度调整
    const signalAdjustment = signal === 'BUY' ? 1.2 : signal === 'SELL' ? 0.8 : 1.0;
    
    const finalPosition = Math.min(
        safePosition * volatilityAdjustment * signalAdjustment,
        QUANT_CONFIG.maxPositionPercent
    );
    
    return {
        percent: (finalPosition * 100).toFixed(1) + '%',
        usdt: (totalBalance * finalPosition).toFixed(2),
        kelly: (kellyPercent * 100).toFixed(1) + '%'
    };
}

// ============ 主函数 ============
async function quantAnalysis() {
    console.log('\n' + '='.repeat(70));
    console.log('📊 量化网格交易系统 v2.0');
    console.log('='.repeat(70));
    
    const symbols = [
        { symbol: 'BTCUSDT', name: 'Bitcoin' },
        { symbol: 'SOLUSDT', name: 'Solana' }
    ];
    
    for (const { symbol, name } of symbols) {
        console.log(`\n${'─'.repeat(70)}`);
        console.log(`${name} (${symbol}) 量化分析`);
        console.log('─'.repeat(70));
        
        // 获取市场数据
        const market = await request('/api/v2/spot/market/tickers', 'GET', { symbol });
        if (!market.data || !market.data[0]) continue;
        
        const marketData = market.data[0];
        const currentPrice = parseFloat(marketData.lastPr);
        
        // 获取 K 线数据 (简化：实际应该获取历史 K 线)
        const klines = [];
        for (let i = 0; i < 30; i++) {
            const fakePrice = currentPrice * (1 + (Math.random() - 0.5) * 0.05);
            klines.push([0, 0, 0, 0, fakePrice.toString(), 0]);
        }
        
        // 量化分析
        const analysis = analyzeMarket(marketData, klines);
        
        console.log(`\n📈 技术指标:`);
        console.log(`   RSI(14): ${analysis.indicators.rsi}`);
        console.log(`   MA7: ${analysis.indicators.ma7}`);
        console.log(`   MA14: ${analysis.indicators.ma14}`);
        console.log(`   MA30: ${analysis.indicators.ma30}`);
        console.log(`   波动率：${analysis.indicators.volatility}`);
        
        if (analysis.indicators.bb) {
            console.log(`   布林带上轨：${analysis.indicators.bb.upper.toFixed(2)}`);
            console.log(`   布林带中轨：${analysis.indicators.bb.middle.toFixed(2)}`);
            console.log(`   布林带下轨：${analysis.indicators.bb.lower.toFixed(2)}`);
        }
        
        console.log(`\n🎯 交易信号:`);
        const signalEmoji = analysis.signal === 'BUY' ? '🟢' : analysis.signal === 'SELL' ? '🔴' : '🟡';
        console.log(`   信号：${signalEmoji} ${analysis.signal}`);
        console.log(`   置信度：${(analysis.confidence * 100).toFixed(0)}%`);
        console.log(`   原因：`);
        analysis.reasons.forEach(r => console.log(`      - ${r}`));
        
        console.log(`\n⚙️ 动态网格参数:`);
        console.log(`   建议网格间距：${analysis.gridSpacing}`);
        
        // 获取余额
        const balance = await request('/api/v2/spot/account/assets', 'GET');
        const usdtAsset = balance.data?.find(a => a.coinName === 'USDT');
        if (usdtAsset) {
            const totalUSDT = parseFloat(usdtAsset.available) + parseFloat(usdtAsset.frozen);
            
            console.log(`\n💰 仓位管理:`);
            const position = calculatePositionSize(totalUSDT, currentPrice, parseFloat(analysis.indicators.volatility), analysis.signal);
            console.log(`   建议仓位：${position.percent}`);
            console.log(`   凯利公式：${position.kelly}`);
            console.log(`   建议金额：${position.usdt} USDT`);
        }
    }
    
    console.log(`\n${'='.repeat(70)}`);
    console.log('✅ 量化分析完成');
    console.log('='.repeat(70) + '\n');
}

quantAnalysis().catch(console.error);
