#!/usr/bin/env node
const fs = require('fs');
const https = require('https');
const http = require('http');
const crypto = require('crypto');

const CONFIG = JSON.parse(fs.readFileSync('config.json'));

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

async function getKline(symbol, period = '15m', limit = 100) {
    const url = `/api/v2/spot/market/candles?symbol=${symbol}&granularity=${period}&limit=${limit}`;
    const data = await api(url);
    if(data.code === '00000' && data.data) {
        return data.data.map(c => ({
            time: c[0],
            open: parseFloat(c[1]),
            high: parseFloat(c[2]),
            low: parseFloat(c[3]),
            close: parseFloat(c[4]),
            volume: parseFloat(c[5])
        }));
    }
    return [];
}

function calculateMA(data, period) {
    if(data.length < period) return null;
    const sum = data.slice(-period).reduce((s, c) => s + c.close, 0);
    return sum / period;
}

function calculateRSI(data, period = 14) {
    if(data.length < period + 1) return 50;
    let gains = 0, losses = 0;
    for(let i = data.length - period; i < data.length; i++) {
        const change = data[i].close - data[i-1].close;
        if(change > 0) gains += change;
        else losses -= change;
    }
    const rs = (gains / period) / (losses / period || 1);
    return 100 - (100 / (1 + rs));
}

function calculateATR(data, period = 14) {
    if(data.length < period + 1) return 0;
    let trSum = 0;
    for(let i = data.length - period; i < data.length; i++) {
        const tr = Math.max(
            data[i].high - data[i].low,
            Math.abs(data[i].high - data[i-1].close),
            Math.abs(data[i].low - data[i-1].close)
        );
        trSum += tr;
    }
    return trSum / period;
}

function calculateVolumeMA(data, period = 20) {
    if(data.length < period) return null;
    const sum = data.slice(-period).reduce((s, c) => s + c.volume, 0);
    return sum / period;
}

async function analyzeSymbol(symbol, name) {
    console.log(`\n${'='.repeat(70)}`);
    console.log(`📊 ${name} (${symbol}) 技术分析`);
    console.log('='.repeat(70));
    
    // 获取 15 分钟 K 线
    const kline15m = await getKline(symbol, '15m', 100);
    // 获取 1 小时 K 线
    const kline1h = await getKline(symbol, '1h', 100);
    // 获取 4 小时 K 线
    const kline4h = await getKline(symbol, '4h', 50);
    
    if(kline15m.length === 0) {
        console.log('❌ 无法获取 K 线数据');
        return null;
    }
    
    const current = kline15m[kline15m.length - 1];
    const prev24h = kline15m[kline15m.length - 96]; // 24 小时前
    
    console.log(`\n📈 当前价格：${current.close}`);
    console.log(`   24h 变化：${((current.close - prev24h.close) / prev24h.close * 100).toFixed(2)}%`);
    console.log(`   24h 最高：${Math.max(...kline15m.slice(-96).map(c => c.high))}`);
    console.log(`   24h 最低：${Math.min(...kline15m.slice(-96).map(c => c.low))}`);
    
    // 均线分析
    console.log(`\n📊 均线分析`);
    const ma5 = calculateMA(kline15m, 5);
    const ma10 = calculateMA(kline15m, 10);
    const ma20 = calculateMA(kline15m, 20);
    const ma50 = calculateMA(kline15m, 50);
    
    console.log(`   MA5:  ${ma5?.toFixed(2)} ${current.close > ma5 ? '📈' : '📉'}`);
    console.log(`   MA10: ${ma10?.toFixed(2)} ${current.close > ma10 ? '📈' : '📉'}`);
    console.log(`   MA20: ${ma20?.toFixed(2)} ${current.close > ma20 ? '📈' : '📉'}`);
    console.log(`   MA50: ${ma50?.toFixed(2)} ${current.close > ma50 ? '📈' : '📉'}`);
    
    // RSI
    const rsi = calculateRSI(kline15m);
    console.log(`\n📊 RSI(14): ${rsi.toFixed(2)}`);
    if(rsi > 70) console.log('   ⚠️ 超买区域');
    else if(rsi < 30) console.log('   ✅ 超卖区域');
    else console.log('   ➖ 中性区域');
    
    // ATR 波动率
    const atr = calculateATR(kline15m);
    const atrPercent = (atr / current.close * 100);
    console.log(`\n📊 ATR(14): ${atr.toFixed(2)} (${atrPercent.toFixed(2)}%)`);
    console.log(`   建议网格间距：${(atrPercent * 0.8).toFixed(2)}% - ${(atrPercent * 1.2).toFixed(2)}%`);
    
    // 成交量分析
    const volMA = calculateVolumeMA(kline15m);
    const currentVol = current.volume;
    const volRatio = currentVol / volMA;
    console.log(`\n📊 成交量分析`);
    console.log(`   当前成交量：${currentVol.toFixed(2)}`);
    console.log(`   20 周期均量：${volMA?.toFixed(2)}`);
    console.log(`   量比：${volRatio.toFixed(2)} ${volRatio > 1.5 ? '🔥 放量' : volRatio < 0.8 ? '❄️ 缩量' : '➖ 正常'}`);
    
    // 支撑/压力位
    const highs = kline15m.slice(-50).map(c => c.high);
    const lows = kline15m.slice(-50).map(c => c.low);
    const resistance = Math.max(...highs);
    const support = Math.min(...lows);
    
    console.log(`\n📊 支撑/压力`);
    console.log(`   压力位：${resistance.toFixed(2)} (${((resistance - current.close) / current.close * 100).toFixed(2)}% 上方)`);
    console.log(`   支撑位：${support.toFixed(2)} (${((current.close - support) / current.close * 100).toFixed(2)}% 下方)`);
    
    // 波动率分析
    const priceRange = (resistance - support) / support * 100;
    console.log(`\n📊 波动率`);
    console.log(`   50 周期波动范围：${priceRange.toFixed(2)}%`);
    console.log(`   建议网格区间：${(support * 0.98).toFixed(2)} - ${(resistance * 1.02).toFixed(2)}`);
    
    return {
        symbol, name, current: current.close,
        ma5, ma10, ma20, ma50, rsi, atr, atrPercent,
        support, resistance, volRatio,
        suggestedGridSpacing: atrPercent,
        suggestedGridRange: { min: support * 0.98, max: resistance * 1.02 }
    };
}

async function main() {
    console.log('🔍 K 线及成交量深度分析 - 网格策略优化\n');
    console.log('时间:', new Date().toLocaleString('zh-CN'));
    
    const results = [];
    
    // 分析 BTC
    results.push(await analyzeSymbol('BTCUSDT', '比特币'));
    
    // 分析 SOL
    results.push(await analyzeSymbol('SOLUSDT', 'Solana'));
    
    // 分析 ETH
    results.push(await analyzeSymbol('ETHUSDT', '以太坊'));
    
    // 生成优化建议
    console.log('\n' + '='.repeat(70));
    console.log('💡 网格策略优化建议');
    console.log('='.repeat(70));
    
    for(const r of results) {
        if(!r) continue;
        
        console.log(`\n${r.name} (${r.symbol}):`);
        console.log('-'.repeat(50));
        
        // 当前网格配置（从 grid_settings.json 读取）
        const gridSettings = JSON.parse(fs.readFileSync('grid_settings.json', 'utf-8'));
        const config = gridSettings[r.symbol.replace('USDT', '').toLowerCase()];
        
        if(config) {
            console.log(`当前配置:`);
            console.log(`  区间：${config.priceMin} - ${config.priceMax}`);
            console.log(`  网格数：${config.gridNum}`);
            console.log(`  间距：${((config.priceMax - config.priceMin) / config.gridNum / config.priceMin * 100).toFixed(2)}%`);
        }
        
        console.log(`\n优化建议:`);
        console.log(`  建议区间：${r.suggestedGridRange.min.toFixed(0)} - ${r.suggestedGridRange.max.toFixed(0)}`);
        console.log(`  建议间距：${(r.suggestedGridSpacing * 0.8).toFixed(2)}% - ${(r.suggestedGridSpacing * 1.2).toFixed(2)}%`);
        console.log(`  建议网格数：${Math.round((r.suggestedGridRange.max - r.suggestedGridRange.min) / (r.suggestedGridRange.min * r.suggestedGridSpacing / 100))}`);
        
        // 趋势判断
        const trend = r.current > r.ma20 ? '📈 上升趋势' : r.current < r.ma20 ? '📉 下降趋势' : '➖ 震荡';
        console.log(`  趋势：${trend}`);
        
        // 操作建议
        if(r.rsi > 70) {
            console.log(`  ⚠️ RSI 超买，考虑减少卖单密度`);
        } else if(r.rsi < 30) {
            console.log(`  ✅ RSI 超卖，考虑增加买单密度`);
        }
        
        if(r.volRatio > 1.5) {
            console.log(`  🔥 放量中，可加宽网格间距`);
        } else if(r.volRatio < 0.8) {
            console.log(`  ❄️ 缩量中，可收窄网格间距`);
        }
    }
    
    console.log('\n' + '='.repeat(70));
}

main();
