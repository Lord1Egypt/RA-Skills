#!/usr/bin/env node
/**
 * 网格策略优化器 - 基于 K 线和成交量分析
 */

const https = require('https');
const fs = require('fs');

// 从 Binance 获取 K 线数据（公开 API，无需签名）
function getKline(symbol, interval = '1h', limit = 100) {
    return new Promise((resolve) => {
        const url = `https://api.binance.com/api/v3/klines?symbol=${symbol}&interval=${interval}&limit=${limit}`;
        https.get(url, {timeout: 10000}, (res) => {
            let data = '';
            res.on('data', c => data += c);
            res.on('end', () => {
                try {
                    const klines = JSON.parse(data);
                    resolve(klines.map(k => ({
                        time: k[0],
                        open: +k[1], high: +k[2], low: +k[3], close: +k[4],
                        volume: +k[5], quoteVolume: +k[7]
                    })));
                } catch(e) { resolve([]); }
            });
        }).on('error', () => resolve([]));
    });
}

// 计算移动平均
function MA(data, period) {
    if(data.length < period) return null;
    return data.slice(-period).reduce((s, c) => s + c.close, 0) / period;
}

// 计算 RSI
function RSI(data, period = 14) {
    if(data.length < period + 1) return 50;
    let gains = 0, losses = 0;
    for(let i = data.length - period; i < data.length; i++) {
        const change = data[i].close - data[i-1].close;
        if(change > 0) gains += change;
        else losses -= change;
    }
    const avgGain = gains / period;
    const avgLoss = losses / period;
    if(avgLoss === 0) return 100;
    return 100 - (100 / (1 + avgGain / avgLoss));
}

// 计算 ATR
function ATR(data, period = 14) {
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

// 计算成交量均值
function VolumeMA(data, period = 20) {
    if(data.length < period) return 0;
    return data.slice(-period).reduce((s, c) => s + c.volume, 0) / period;
}

// 分析单个币种
async function analyze(symbol, name, currentConfig) {
    console.log(`\n${'='.repeat(75)}`);
    console.log(`📊 ${name} (${symbol}) 深度分析`);
    console.log('='.repeat(75));
    
    const [kline1h, kline4h, kline1d] = await Promise.all([
        getKline(symbol, '1h', 100),
        getKline(symbol, '4h', 50),
        getKline(symbol, '1d', 30)
    ]);
    
    if(kline1h.length === 0) return null;
    
    const current = kline1h[kline1h.length - 1];
    const price = current.close;
    
    // 24 小时统计
    const kline24h = kline1h.slice(-24);
    const high24h = Math.max(...kline24h.map(c => c.high));
    const low24h = Math.min(...kline24h.map(c => c.low));
    const change24h = ((price - kline24h[0].close) / kline24h[0].close * 100);
    
    console.log(`\n📈 价格分析`);
    console.log(`   当前价：${price.toFixed(2)}`);
    console.log(`   24h 涨跌：${change24h >= 0 ? '+' : ''}${change24h.toFixed(2)}%`);
    console.log(`   24h 区间：${low24h.toFixed(2)} - ${high24h.toFixed(2)}`);
    
    // 均线
    const ma5 = MA(kline1h, 5);
    const ma10 = MA(kline1h, 10);
    const ma20 = MA(kline1h, 20);
    const ma50 = MA(kline1h, 50);
    
    console.log(`\n📊 均线系统`);
    console.log(`   MA5:  ${ma5?.toFixed(2)} ${price > ma5 ? '✅' : '❌'}`);
    console.log(`   MA10: ${ma10?.toFixed(2)} ${price > ma10 ? '✅' : '❌'}`);
    console.log(`   MA20: ${ma20?.toFixed(2)} ${price > ma20 ? '✅' : '❌'}`);
    console.log(`   MA50: ${ma50?.toFixed(2)} ${price > ma50 ? '✅' : '❌'}`);
    
    const trend = price > ma20 ? '📈 上升' : price < ma20 ? '📉 下降' : '➖ 震荡';
    console.log(`   趋势：${trend}`);
    
    // RSI
    const rsi = RSI(kline1h);
    console.log(`\n📊 RSI(14): ${rsi.toFixed(2)}`);
    if(rsi > 70) console.log(`   ⚠️ 超买 (考虑减少卖单)`);
    else if(rsi < 30) console.log(`   ✅ 超卖 (考虑增加买单)`);
    else console.log(`   ➖ 中性`);
    
    // ATR 波动率
    const atr = ATR(kline1h);
    const atrPct = (atr / price * 100);
    console.log(`\n📊 波动率 (ATR)`);
    console.log(`   ATR(14): ${atr.toFixed(2)} (${atrPct.toFixed(2)}%)`);
    console.log(`   建议网格间距：${(atrPct * 0.7).toFixed(2)}% - ${(atrPct * 1.3).toFixed(2)}%`);
    
    // 成交量
    const volMA = VolumeMA(kline1h);
    const volRatio = current.volume / volMA;
    console.log(`\n📊 成交量`);
    console.log(`   当前：${current.volume.toFixed(2)}`);
    console.log(`   均量：${volMA.toFixed(2)}`);
    console.log(`   量比：${volRatio.toFixed(2)} ${volRatio > 1.5 ? '🔥 放量' : volRatio < 0.8 ? '❄️ 缩量' : '➖ 正常'}`);
    
    // 支撑/压力
    const allHighs = kline4h.map(c => c.high);
    const allLows = kline4h.map(c => c.low);
    const resistance = Math.max(...allHighs);
    const support = Math.min(...allLows);
    const range = (resistance - support) / support * 100;
    
    console.log(`\n📊 支撑/压力 (4h)`);
    console.log(`   压力位：${resistance.toFixed(2)} (+${((resistance - price) / price * 100).toFixed(2)}%)`);
    console.log(`   支撑位：${support.toFixed(2)} (-${((price - support) / price * 100).toFixed(2)}%)`);
    console.log(`   波动范围：${range.toFixed(2)}%`);
    
    // 当前配置分析
    console.log(`\n📋 当前网格配置`);
    if(currentConfig) {
        const spacing = (currentConfig.priceMax - currentConfig.priceMin) / currentConfig.gridNum / currentConfig.priceMin * 100;
        console.log(`   区间：${currentConfig.priceMin} - ${currentConfig.priceMax}`);
        console.log(`   网格数：${currentConfig.gridNum}`);
        console.log(`   间距：${spacing.toFixed(2)}%`);
        
        // 配置评估
        console.log(`\n📊 配置评估`);
        if(spacing < atrPct * 0.5) console.log(`   ⚠️ 间距过小 (建议：${(atrPct * 0.8).toFixed(2)}%)`);
        else if(spacing > atrPct * 2) console.log(`   ⚠️ 间距过大 (建议：${(atrPct * 1.2).toFixed(2)}%)`);
        else console.log(`   ✅ 间距合理`);
        
        if(currentConfig.priceMin > support * 1.1) console.log(`   ⚠️ 区间偏高 (支撑：${support.toFixed(0)})`);
        else if(currentConfig.priceMax < resistance * 0.9) console.log(`   ⚠️ 区间偏低 (压力：${resistance.toFixed(0)})`);
        else console.log(`   ✅ 区间合理`);
    }
    
    // 优化建议
    const optSpacing = atrPct;
    const optGridNum = Math.round(range / optSpacing);
    const optMin = support * 0.95;
    const optMax = resistance * 1.05;
    
    console.log(`\n💡 优化建议`);
    console.log(`   建议区间：${optMin.toFixed(0)} - ${optMax.toFixed(0)}`);
    console.log(`   建议网格数：${optGridNum}`);
    console.log(`   建议间距：${optSpacing.toFixed(2)}%`);
    console.log(`   每格金额：${currentConfig ? currentConfig.amount : 10} USDT`);
    
    // 买卖单密度建议
    console.log(`\n📥📤 挂单策略`);
    if(price > ma20) {
        console.log(`   上升趋势：增加卖单密度，减少买单`);
        console.log(`   建议：卖单 60% | 买单 40%`);
    } else if(price < ma20) {
        console.log(`   下降趋势：增加买单密度，减少卖单`);
        console.log(`   建议：买单 60% | 卖单 40%`);
    } else {
        console.log(`   震荡行情：买卖均衡`);
        console.log(`   建议：买单 50% | 卖单 50%`);
    }
    
    return {
        symbol, name, price,
        support, resistance, atrPct, rsi, volRatio,
        suggested: {
            priceMin: optMin, priceMax: optMax,
            gridNum: optGridNum, spacing: optSpacing
        }
    };
}

async function main() {
    console.log('🔍 网格策略优化器 - K 线 + 成交量分析\n');
    console.log('时间:', new Date().toLocaleString('zh-CN'));
    
    // 读取当前配置
    let gridSettings = {};
    try {
        gridSettings = JSON.parse(fs.readFileSync('grid_settings.json', 'utf-8'));
    } catch(e) { console.log('⚠️ 无法读取 grid_settings.json'); }
    
    const results = [];
    
    // 分析各币种
    results.push(await analyze('BTCUSDT', '比特币', gridSettings.btc));
    results.push(await analyze('SOLUSDT', 'Solana', gridSettings.sol));
    results.push(await analyze('ETHUSDT', '以太坊', gridSettings.eth));
    
    // 汇总优化建议
    console.log('\n' + '='.repeat(75));
    console.log('📋 网格策略优化汇总');
    console.log('='.repeat(75));
    
    const newSettings = { ...gridSettings };
    
    for(const r of results) {
        if(!r) continue;
        
        console.log(`\n${r.name}:`);
        console.log(`   当前：${r.price.toFixed(2)} | 支撑：${r.support.toFixed(0)} | 压力：${r.resistance.toFixed(0)}`);
        console.log(`   建议区间：${r.suggested.priceMin.toFixed(0)} - ${r.suggested.priceMax.toFixed(0)}`);
        console.log(`   建议网格：${r.suggested.gridNum} 格 @ ${r.suggested.spacing.toFixed(2)}%`);
        
        // 更新配置
        const key = r.symbol.replace('USDT', '').toLowerCase();
        if(gridSettings[key]) {
            newSettings[key] = {
                ...gridSettings[key],
                priceMin: Math.round(r.suggested.priceMin),
                priceMax: Math.round(r.suggested.priceMax),
                gridNum: r.suggested.gridNum,
                notes: `2026-03-09 优化：基于 ATR=${r.atrPct.toFixed(2)}%, RSI=${r.rsi.toFixed(0)}`
            };
        }
    }
    
    // 保存新配置
    console.log('\n' + '='.repeat(75));
    console.log('💾 是否保存优化配置？');
    console.log('='.repeat(75));
    console.log('运行以下命令应用优化:');
    console.log(`node save-optimized-config.js`);
    
    // 生成优化配置脚本
    fs.writeFileSync('save-optimized-config.js', `
const fs = require('fs');
const newSettings = ${JSON.stringify(newSettings, null, 2)};
fs.writeFileSync('grid_settings.json', JSON.stringify(newSettings, null, 2));
console.log('✅ 网格配置已优化并保存！');
console.log('建议重启网格监控系统：node start-simple.js');
`, 'utf-8');
    
    console.log('\n✅ 优化分析完成！\n');
}

main();
