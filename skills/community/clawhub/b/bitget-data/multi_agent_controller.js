#!/usr/bin/env node
/**
 * Bitget 多 Agent 控制器
 * 
 * 功能：
 * 1. 网格监控 Agent - 每 30 分钟检查挂单和成交
 * 2. 技术分析 Agent - 每小时执行 RSI/MACD/布林带分析
 * 3. 网格优化 Agent - 根据成交频率自动调整参数
 * 4. 日报 Agent - 每日 20:00 生成收益报告
 * 
 * 使用方式：
 * node multi_agent_controller.js [agent-name]
 * 
 * 可用 Agent: monitor, analysis, optimizer, report, all
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const https = require('https');

// 加载配置
const CONFIG_PATH = path.join(__dirname, 'multi_agent_config.json');
const CONFIG = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));

// 日志函数
function log(msg, level = 'INFO', agent = 'controller') {
    const timestamp = new Date().toLocaleString('zh-CN');
    console.log(`[${timestamp}] [${level}] [${agent}] ${msg}`);
}

// API 请求函数
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
        const signature = crypto.createHmac('sha256', CONFIG.apiCredentials.secretKey)
            .update(signStr).digest('base64');
        
        const options = {
            hostname: 'api.bitget.com',
            port: 443,
            path: fullpath,
            method: method,
            headers: {
                'ACCESS-KEY': CONFIG.apiCredentials.apiKey,
                'ACCESS-SIGN': signature,
                'ACCESS-TIMESTAMP': timestamp,
                'ACCESS-PASSPHRASE': CONFIG.apiCredentials.passphrase,
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

// ============== Agent 实现 ==============

/**
 * 网格监控 Agent
 * 检查挂单状态、成交情况、频率统计
 */
async function gridMonitorAgent() {
    log('启动网格监控 Agent...', 'INFO', 'monitor');
    
    const results = {};
    const coins = ['sol', 'eth', 'btc'];
    
    for (const coin of coins) {
        const config = CONFIG.gridSettings.coins[coin];
        if (!config || !config.enabled) {
            log(`跳过 ${coin.toUpperCase()} - 已禁用`, 'INFO', 'monitor');
            continue;
        }
        
        const symbol = config.symbol;
        
        // 获取当前价格
        const tickerResult = await request('/spot/market/tickers', 'GET', { symbol });
        const currentPrice = parseFloat(tickerResult.data?.[0]?.lastPr || 0);
        
        // 获取挂单
        const ordersResult = await request('/spot/trade/unfilled-orders', 'GET', { 
            symbol, 
            limit: '100' 
        });
        const orders = ordersResult.data || [];
        
        // 统计买卖单
        const buyOrders = orders.filter(o => o.side === 'buy').length;
        const sellOrders = orders.filter(o => o.side === 'sell').length;
        
        results[coin] = {
            symbol,
            price: currentPrice,
            totalOrders: orders.length,
            buyOrders,
            sellOrders,
            status: 'normal'
        };
        
        log(`${symbol}: 价格=${currentPrice}, 挂单=${orders.length} (买${buyOrders}/卖${sellOrders})`, 'INFO', 'monitor');
    }
    
    // 检查成交频率
    const logPath = path.join(__dirname, 'auto_monitor.log');
    if (fs.existsSync(logPath)) {
        const logContent = fs.readFileSync(logPath, 'utf-8');
        const lines = logContent.split('\n').filter(l => l.includes('成交'));
        const recentTrades = lines.slice(-20);
        log(`最近成交记录：${recentTrades.length} 条`, 'INFO', 'monitor');
    }
    
    return results;
}

/**
 * 技术分析 Agent
 * 获取 K 线数据，计算 RSI/MACD/布林带
 */
async function technicalAnalysisAgent() {
    log('启动技术分析 Agent...', 'INFO', 'analysis');
    
    const results = {};
    const coins = ['sol', 'eth'];
    
    for (const coin of coins) {
        const config = CONFIG.gridSettings.coins[coin];
        if (!config || !config.enabled) continue;
        
        const symbol = config.symbol.toUpperCase();
        
        // 获取 K 线数据 (1 小时)
        const klineResult = await request('/spot/market/candles', 'GET', {
            symbol: symbol.toLowerCase(),
            granularity: '1H',
            limit: '100'
        });
        
        if (!klineResult.data || klineResult.data.length === 0) {
            log(`${symbol} K 线数据获取失败`, 'ERROR', 'analysis');
            continue;
        }
        
        const candles = klineResult.data.map(c => ({
            time: c[0],
            open: parseFloat(c[1]),
            high: parseFloat(c[2]),
            low: parseFloat(c[3]),
            close: parseFloat(c[4]),
            volume: parseFloat(c[5])
        }));
        
        // 计算 RSI (14 周期)
        const rsi = calculateRSI(candles.map(c => c.close), 14);
        
        // 计算 MACD
        const macd = calculateMACD(candles.map(c => c.close));
        
        // 计算布林带
        const bollinger = calculateBollinger(candles.map(c => c.close));
        
        const currentPrice = candles[candles.length - 1].close;
        
        // 判断趋势
        let trend = 'NEUTRAL';
        if (rsi < 30) trend = 'OVERSOLD_BUY';
        else if (rsi > 70) trend = 'OVERBOUGHT_SELL';
        else if (macd.histogram > 0 && macd.dif > macd.dea) trend = 'BULLISH';
        else if (macd.histogram < 0 && macd.dif < macd.dea) trend = 'BEARISH';
        
        results[coin] = {
            symbol,
            price: currentPrice,
            rsi: rsi.toFixed(2),
            macd: {
                dif: macd.dif.toFixed(2),
                dea: macd.dea.toFixed(2),
                histogram: macd.histogram.toFixed(2)
            },
            bollinger: {
                upper: bollinger.upper.toFixed(2),
                middle: bollinger.middle.toFixed(2),
                lower: bollinger.lower.toFixed(2)
            },
            trend
        };
        
        log(`${symbol}: RSI=${rsi.toFixed(2)}, MACD=${macd.histogram.toFixed(2)}, 趋势=${trend}`, 'INFO', 'analysis');
    }
    
    return results;
}

/**
 * 网格优化 Agent
 * 根据成交频率自动调整网格参数
 */
async function gridOptimizerAgent() {
    log('启动网格优化 Agent...', 'INFO', 'optimizer');
    
    const settings = CONFIG.gridSettings;
    
    if (!settings.autoAdjust.enabled) {
        log('自动调整已禁用，跳过优化', 'WARN', 'optimizer');
        return { action: 'none', reason: 'autoAdjust disabled' };
    }
    
    // 读取成交频率
    const logPath = path.join(__dirname, 'auto_monitor.log');
    if (!fs.existsSync(logPath)) {
        log('日志文件不存在，无法评估频率', 'ERROR', 'optimizer');
        return { action: 'none', reason: 'no log data' };
    }
    
    const logContent = fs.readFileSync(logPath, 'utf-8');
    const frequencyMatch = logContent.match(/当前频率[:：]\s*([\d.]+)\s*笔/);
    const currentFrequency = frequencyMatch ? parseFloat(frequencyMatch[1]) : 0;
    
    const targetMin = settings.targetFrequency.min;
    const targetMax = settings.targetFrequency.max;
    
    log(`当前频率：${currentFrequency} 笔/小时，目标：${targetMin}-${targetMax} 笔/小时`, 'INFO', 'optimizer');
    
    if (currentFrequency > targetMax) {
        // 频率过高，需要降低密度
        const adjustPercent = Math.min(
            settings.autoAdjust.maxAdjustPercent,
            ((currentFrequency - targetMax) / targetMax) * 100
        );
        
        log(`频率超标 ${adjustPercent.toFixed(1)}%，建议降低网格密度`, 'WARN', 'optimizer');
        
        return {
            action: 'reduce_density',
            percent: adjustPercent,
            suggestions: [
                '减少网格数量 ' + adjustPercent.toFixed(0) + '%',
                '扩大价格区间 ' + (adjustPercent * 0.8).toFixed(0) + '%',
                '提高单笔金额 ' + (adjustPercent * 0.5).toFixed(0) + '%'
            ]
        };
    } else if (currentFrequency < targetMin) {
        // 频率过低，可以增加密度
        const adjustPercent = Math.min(
            settings.autoAdjust.maxAdjustPercent,
            ((targetMin - currentFrequency) / targetMin) * 100
        );
        
        log(`频率偏低 ${adjustPercent.toFixed(1)}%，建议增加网格密度`, 'WARN', 'optimizer');
        
        return {
            action: 'increase_density',
            percent: adjustPercent,
            suggestions: [
                '增加网格数量 ' + adjustPercent.toFixed(0) + '%',
                '缩小价格区间 ' + (adjustPercent * 0.8).toFixed(0) + '%'
            ]
        };
    } else {
        log('频率在目标范围内，无需调整', 'INFO', 'optimizer');
        return { action: 'none', reason: 'frequency optimal' };
    }
}

/**
 * 日报 Agent
 * 生成每日交易报告
 */
async function dailyReportAgent() {
    log('启动日报 Agent...', 'INFO', 'report');
    
    const report = {
        date: new Date().toLocaleDateString('zh-CN'),
        generated: new Date().toLocaleString('zh-CN'),
        summary: {},
        coins: {},
        recommendations: []
    };
    
    // 读取日志统计
    const logPath = path.join(__dirname, 'auto_monitor.log');
    if (fs.existsSync(logPath)) {
        const logContent = fs.readFileSync(logPath, 'utf-8');
        
        // 提取统计数据
        const totalMatch = logContent.match(/累计成交[:：]\s*(\d+)\s*笔/);
        const frequencyMatch = logContent.match(/当前频率[:：]\s*([\d.]+)\s*笔/);
        
        report.summary = {
            totalTrades: totalMatch ? parseInt(totalMatch[1]) : 0,
            avgFrequency: frequencyMatch ? parseFloat(frequencyMatch[1]) : 0,
            targetFrequency: CONFIG.gridSettings.targetFrequency
        };
    }
    
    // 各币种详情
    for (const [coin, config] of Object.entries(CONFIG.gridSettings.coins)) {
        if (!config.enabled) continue;
        
        report.coins[coin] = {
            symbol: config.symbol,
            gridNum: config.gridNum,
            priceRange: `${config.priceMin}-${config.priceMax}`,
            amount: config.amount,
            maxPosition: config.maxPosition
        };
    }
    
    // 生成建议
    if (report.summary.avgFrequency > CONFIG.gridSettings.targetFrequency.max) {
        report.recommendations.push('⚠️ 成交频率偏高，建议降低网格密度');
    } else if (report.summary.avgFrequency < CONFIG.gridSettings.targetFrequency.min) {
        report.recommendations.push('💡 成交频率偏低，可增加网格密度提高收益');
    } else {
        report.recommendations.push('✅ 成交频率正常，保持当前策略');
    }
    
    return report;
}

// ============== 技术指标计算 ==============

function calculateRSI(prices, period = 14) {
    if (prices.length < period + 1) return 50;
    
    let gains = 0, losses = 0;
    for (let i = prices.length - period; i < prices.length; i++) {
        const change = prices[i] - prices[i - 1];
        if (change > 0) gains += change;
        else losses -= change;
    }
    
    const rs = losses === 0 ? 100 : gains / losses;
    return 100 - (100 / (1 + rs));
}

function calculateMACD(prices, fast = 12, slow = 26, signal = 9) {
    const emaFast = calculateEMA(prices, fast);
    const emaSlow = calculateEMA(prices, slow);
    const dif = emaFast - emaSlow;
    
    // 简化版：假设 DEA 是 DIF 的 EMA
    const dea = dif * 0.8; // 简化计算
    const histogram = dif - dea;
    
    return { dif, dea, histogram };
}

function calculateEMA(prices, period) {
    if (prices.length === 0) return 0;
    const multiplier = 2 / (period + 1);
    let ema = prices[0];
    for (let i = 1; i < prices.length; i++) {
        ema = (prices[i] - ema) * multiplier + ema;
    }
    return ema;
}

function calculateBollinger(prices, period = 20, stdDev = 2) {
    if (prices.length < period) {
        return { upper: 0, middle: 0, lower: 0 };
    }
    
    const slice = prices.slice(-period);
    const middle = slice.reduce((a, b) => a + b, 0) / period;
    
    const variance = slice.reduce((sum, price) => sum + Math.pow(price - middle, 2), 0) / period;
    const std = Math.sqrt(variance);
    
    return {
        upper: middle + stdDev * std,
        middle,
        lower: middle - stdDev * std
    };
}

// ============== 主函数 ==============

async function runAgent(agentName) {
    log(`=== 启动 Agent: ${agentName} ===`, 'INFO');
    
    try {
        let result;
        
        switch (agentName) {
            case 'monitor':
                result = await gridMonitorAgent();
                break;
            case 'analysis':
                result = await technicalAnalysisAgent();
                break;
            case 'optimizer':
                result = await gridOptimizerAgent();
                break;
            case 'report':
                result = await dailyReportAgent();
                break;
            case 'all':
                log('执行所有 Agent...', 'INFO');
                result = {
                    monitor: await gridMonitorAgent(),
                    analysis: await technicalAnalysisAgent(),
                    optimizer: await gridOptimizerAgent(),
                    report: await dailyReportAgent()
                };
                break;
            default:
                log(`未知 Agent: ${agentName}`, 'ERROR');
                console.log('可用 Agent: monitor, analysis, optimizer, report, all');
                process.exit(1);
        }
        
        log('Agent 执行完成', 'INFO');
        console.log('\n=== 执行结果 ===');
        console.log(JSON.stringify(result, null, 2));
        
    } catch (error) {
        log(`Agent 执行失败：${error.message}`, 'ERROR');
        process.exit(1);
    }
}

// 命令行参数
const agentName = process.argv[2] || 'all';
runAgent(agentName);
