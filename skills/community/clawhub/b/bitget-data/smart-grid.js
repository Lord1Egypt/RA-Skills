#!/usr/bin/env node
// Bitget 智能网格脚本 - 基于技术指标动态调整挂单
// 策略：RSI + MACD + 布林带组合判断，留 10% 资金缓冲

const fs = require('fs');
const crypto = require('crypto');
const http = require('http');
const https = require('https');

const DATA_DIR = __dirname;
const CONFIG_FILE = DATA_DIR + '/config.json';
const SETTINGS_FILE = DATA_DIR + '/grid_settings_highfreq.json';
const LOG_FILE = DATA_DIR + '/smart_grid.log';
const STATE_FILE = DATA_DIR + '/smart_grid_state.json';

const CONFIG = JSON.parse(fs.readFileSync(CONFIG_FILE));
const SETTINGS = JSON.parse(fs.readFileSync(SETTINGS_FILE));

// 技术指标参数
const INDICATORS = {
    RSI_PERIOD: 14,
    RSI_OVERBOUGHT: 70,
    RSI_OVERSOLD: 30,
    MACD_FAST: 12,
    MACD_SLOW: 26,
    MACD_SIGNAL: 9,
    BOLLINGER_PERIOD: 20,
    BOLLINGER_STD: 2
};

// 资金管理
const CAPITAL_ALLOCATION = {
    FOLLOW_PERCENT: 0.90,  // 90% 跟随趋势
    BUFFER_PERCENT: 0.10   // 10% 缓冲
};

// 缓存 K 线数据
let klineCache = {};

function log(message) {
    const timestamp = new Date().toLocaleString('zh-CN');
    const logLine = `[${timestamp}] ${message}\n`;
    fs.appendFileSync(LOG_FILE, logLine);
    console.log(logLine.trim());
}

function sign(message) {
    return crypto.createHmac('sha256', CONFIG.secretKey).update(message).digest('base64');
}

function request(endpoint, method = 'GET', params = {}) {
    return new Promise((resolve, reject) => {
        const timestamp = new Date().toISOString().split('.')[0] + '.000Z';
        const queryString = method === 'GET' && Object.keys(params).length > 0 
            ? '?' + new URLSearchParams(params).toString() 
            : '';
        
        const fullpath = '/api/v2' + endpoint + queryString;
        let body = '';
        if (method === 'POST') body = JSON.stringify(params);
        
        const signStr = timestamp + method + fullpath + body;
        const signature = sign(signStr);
        
        // 使用代理连接 Bitget API
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
                        const result = JSON.parse(data);
                        resolve(result.code === '00000' ? result.data : { error: result.msg });
                    } catch (e) {
                        resolve({ error: 'Parse Error', raw: data.substring(0, 200) });
                    }
                });
            });
            
            req.on('error', (e) => {
                socket.destroy();
                reject(e);
            });
            if (body) req.write(body);
            req.end();
        });
        
        proxyReq.on('error', (e) => reject(e));
        proxyReq.end();
    });
}

// 获取 K 线数据
async function getKlines(symbol, interval = '1h', limit = 100) {
    const cacheKey = `${symbol}_${interval}`;
    const now = Date.now();
    
    // 缓存 5 分钟
    if (klineCache[cacheKey] && (now - klineCache[cacheKey].timestamp) < 300000) {
        return klineCache[cacheKey].data;
    }
    
    try {
        // Bitget V2 API: granularity 支持 1m,5m,15m,30m,1h,4h,6h,12h,1day,1week,1M 等
        const result = await request('/spot/market/candles', 'GET', { symbol: symbol, granularity: interval, limit: limit.toString() });
        
        log(`   📡 API 返回：${result.error ? '错误=' + result.error : (Array.isArray(result) ? result.length + '条' : '未知格式')}`);
        
        if (result.error || !Array.isArray(result) || result.length === 0) {
            log(`   ⚠️ K 线数据为空或错误`);
            return [];
        }
        
        // 解析 K 线：[时间，开盘，最高，最低，收盘，成交量，成交额...]
        const klines = result.map(k => ({
            time: parseInt(k[0]),
            open: parseFloat(k[1]),
            high: parseFloat(k[2]),
            low: parseFloat(k[3]),
            close: parseFloat(k[4]),
            volume: parseFloat(k[5])
        }));
        
        log(`   ✅ 成功获取 ${klines.length} 条 K 线`);
        klineCache[cacheKey] = { data: klines, timestamp: now };
        return klines;
    } catch (e) {
        log(`❌ 获取 K 线异常：${e.message}`);
        return [];
    }
}

// 计算 RSI
function calculateRSI(klines, period = 14) {
    if (klines.length < period + 1) return null;
    
    const closes = klines.map(k => k.close);
    let gains = 0, losses = 0;
    
    // 计算初始平均
    for (let i = 1; i <= period; i++) {
        const change = closes[i] - closes[i - 1];
        if (change > 0) gains += change;
        else losses += Math.abs(change);
    }
    
    let avgGain = gains / period;
    let avgLoss = losses / period;
    
    // 平滑计算后续
    for (let i = period + 1; i < closes.length; i++) {
        const change = closes[i] - closes[i - 1];
        const gain = change > 0 ? change : 0;
        const loss = change < 0 ? Math.abs(change) : 0;
        
        avgGain = (avgGain * (period - 1) + gain) / period;
        avgLoss = (avgLoss * (period - 1) + loss) / period;
    }
    
    if (avgLoss === 0) return 100;
    const rs = avgGain / avgLoss;
    return 100 - (100 / (1 + rs));
}

// 计算 MACD
function calculateMACD(klines, fast = 12, slow = 26, signal = 9) {
    if (klines.length < slow + signal) return null;
    
    const closes = klines.map(k => k.close);
    
    // 计算 EMA
    const emaFast = calculateEMA(closes, fast);
    const emaSlow = calculateEMA(closes, slow);
    
    if (emaFast === null || emaSlow === null) return null;
    
    const macdLine = emaFast - emaSlow;
    
    // 计算信号线 (MACD 的 EMA)
    const macdValues = [];
    for (let i = slow - 1; i < closes.length; i++) {
        const fastEma = calculateEMA(closes.slice(0, i + 1), fast);
        const slowEma = calculateEMA(closes.slice(0, i + 1), slow);
        if (fastEma !== null && slowEma !== null) {
            macdValues.push(fastEma - slowEma);
        }
    }
    
    const signalLine = calculateEMA(macdValues, signal);
    const histogram = macdLine - (signalLine || 0);
    
    return { macdLine, signalLine, histogram };
}

function calculateEMA(values, period) {
    if (values.length < period) return null;
    
    const multiplier = 2 / (period + 1);
    let ema = values.slice(0, period).reduce((a, b) => a + b) / period;
    
    for (let i = period; i < values.length; i++) {
        ema = (values[i] - ema) * multiplier + ema;
    }
    
    return ema;
}

// 计算布林带
function calculateBollinger(klines, period = 20, stdDev = 2) {
    if (klines.length < period) return null;
    
    const closes = klines.map(k => k.close);
    const currentPrice = closes[closes.length - 1];
    
    // 计算中轨 (SMA)
    const sma = closes.slice(-period).reduce((a, b) => a + b) / period;
    
    // 计算标准差
    const variance = closes.slice(-period).reduce((sum, price) => sum + Math.pow(price - sma, 2), 0) / period;
    const std = Math.sqrt(variance);
    
    const upperBand = sma + (stdDev * std);
    const lowerBand = sma - (stdDev * std);
    
    return { upperBand, middleBand: sma, lowerBand, currentPrice, std };
}

// 综合趋势判断
function analyzeTrend(rsi, macd, bollinger) {
    const signals = {
        bullish: 0,
        bearish: 0,
        neutral: 0
    };
    
    // RSI 判断
    if (rsi < INDICATORS.RSI_OVERSOLD) signals.bullish += 2;
    else if (rsi > INDICATORS.RSI_OVERBOUGHT) signals.bearish += 2;
    else signals.neutral += 1;
    
    // MACD 判断
    if (macd) {
        if (macd.histogram > 0 && macd.macdLine > macd.signalLine) signals.bullish += 2;
        else if (macd.histogram < 0 && macd.macdLine < macd.signalLine) signals.bearish += 2;
        else signals.neutral += 1;
    }
    
    // 布林带判断
    if (bollinger) {
        const { upperBand, lowerBand, currentPrice } = bollinger;
        if (currentPrice <= lowerBand) signals.bullish += 2;
        else if (currentPrice >= upperBand) signals.bearish += 2;
        else signals.neutral += 1;
    }
    
    // 综合判断
    if (signals.bullish > signals.bearish + 1) return 'STRONG_BUY';
    if (signals.bearish > signals.bullish + 1) return 'STRONG_SELL';
    if (signals.bullish > signals.bearish) return 'WEAK_BUY';
    if (signals.bearish > signals.bullish) return 'WEAK_SELL';
    return 'NEUTRAL';
}

// 获取账户余额
async function getBalance() {
    try {
        const result = await request('/spot/account/assets', 'GET');
        if (result.error) return [];
        return result;
    } catch (e) {
        log(`❌ 获取余额失败：${e.message}`);
        return [];
    }
}

// 获取当前挂单
async function getOrders(symbol) {
    try {
        const result = await request('/spot/trade/unfilled-orders', 'GET', { symbol, limit: '100' });
        if (result.error) return [];
        return result;
    } catch (e) {
        return [];
    }
}

// 取消所有挂单
async function cancelAllOrders(symbol) {
    try {
        const orders = await getOrders(symbol);
        if (orders.length === 0) return 0;
        
        let cancelled = 0;
        for (const order of orders) {
            const result = await request('/spot/trade/cancel-order', 'POST', {
                symbol: symbol,
                orderId: order.orderId
            });
            if (!result.error) cancelled++;
        }
        return cancelled;
    } catch (e) {
        log(`❌ 取消订单失败：${e.message}`);
        return 0;
    }
}

// 获取交易对精度
function getPriceScale(symbol) {
    // Bitget 不同币种价格精度不同
    if (symbol.startsWith('BTC')) return 1;      // BTC: 1 位小数
    if (symbol.startsWith('ETH')) return 2;      // ETH: 2 位小数
    if (symbol.startsWith('SOL')) return 2;      // SOL: 2 位小数
    if (symbol.startsWith('AVAX')) return 2;     // AVAX: 2 位小数
    return 2;  // 默认 2 位
}

function getSizeScale(symbol) {
    // Bitget 不同币种数量精度不同
    if (symbol.startsWith('BTC')) return 5;      // BTC: 5 位小数
    if (symbol.startsWith('ETH')) return 4;      // ETH: 4 位小数
    if (symbol.startsWith('SOL')) return 4;      // SOL: 4 位小数
    if (symbol.startsWith('AVAX')) return 4;     // AVAX: 4 位小数
    return 4;  // 默认 4 位
}

// 下网格订单
async function placeGridOrders(symbol, trend, balance, currentPrice, gridConfig = null) {
    // 计算可用资金 (90% 用于网格)
    const usdtBalance = balance.find(b => b.coin === 'USDT');
    if (!usdtBalance) {
        log('❌ 未找到 USDT 余额');
        return;
    }
    
    const availableUSDT = parseFloat(usdtBalance.available) * CAPITAL_ALLOCATION.FOLLOW_PERCENT;
    log(`💰 可用资金：${availableUSDT.toFixed(2)} USDT (已留 10% 缓冲)`);
    
    // 获取精度
    const priceScale = getPriceScale(symbol);
    const sizeScale = getSizeScale(symbol);
    log(`   📏 精度要求：价格${priceScale}位，数量${sizeScale}位`);
    
    // 根据趋势决定网格方向
    let orderConfig;
    switch (trend) {
        case 'STRONG_BUY':
        case 'WEAK_BUY':
            orderConfig = createBuyGrid(symbol, currentPrice, availableUSDT, trend === 'STRONG_BUY' ? 0.85 : 0.90);
            break;
        case 'STRONG_SELL':
        case 'WEAK_SELL':
            orderConfig = await createSellGrid(symbol, currentPrice, availableUSDT, trend === 'STRONG_SELL' ? 0.85 : 0.90, gridConfig);
            break;
        case 'NEUTRAL':
        default:
            orderConfig = createNeutralGrid(symbol, currentPrice, availableUSDT);
            break;
    }
    
    // 下订单
    log(`📋 计划下单：${orderConfig.orders.length} 个`);
    
    for (const order of orderConfig.orders) {
        try {
            const priceStr = order.price.toFixed(priceScale);
            const sizeStr = order.size.toFixed(sizeScale);
            
            const result = await request('/spot/trade/place-order', 'POST', {
                symbol: symbol,
                side: order.side,
                orderType: 'limit',
                price: priceStr,
                size: sizeStr,
                force: 'GTC'  // Good Till Cancelled
            });
            
            if (result.error) {
                log(`   ❌ 下单失败：${order.side} ${priceStr} x ${sizeStr} - ${result.error}`);
            } else {
                log(`   ✅ 下单成功：${order.side} ${priceStr} x ${sizeStr}`);
            }
        } catch (e) {
            log(`   ❌ 下单异常：${e.message}`);
        }
    }
}

function createBuyGrid(symbol, currentPrice, totalUSDT, aggressionFactor = 0.9) {
    const orders = [];
    const gridCount = 3; // 降低到 3 档，减少成交频率
    const priceRange = 0.08; // 扩大到 8% 价格区间，降低密度
    const MIN_ORDER_VALUE = 5; // 提高到 5 USDT，确保单笔收益
    
    // 买入网格：在当前价下方分层挂单（更宽间距）
    for (let i = 0; i < gridCount; i++) {
        const price = currentPrice * (1 - (i + 1) * (priceRange / gridCount));
        const allocation = (totalUSDT / gridCount) * (1 + (gridCount - i) * 0.1 * aggressionFactor);
        
        // 确保订单金额 ≥ 最小值
        if (allocation < MIN_ORDER_VALUE) {
            log(`   ⚠️ 买单金额 ${allocation.toFixed(2)} USDT < ${MIN_ORDER_VALUE}，跳过`);
            continue;
        }
        
        const size = allocation / price;
        orders.push({ side: 'buy', price, size });
    }
    
    // 少量卖单在上方（提高止盈位置到 3%）
    if (orders.length > 0) {
        const sellPrice = currentPrice * 1.03; // 从 2% 提高到 3%
        const sellSize = orders.reduce((sum, o) => sum + o.size, 0) * 0.3;
        const sellValue = sellPrice * sellSize;
        if (sellValue >= MIN_ORDER_VALUE) {
            orders.push({ side: 'sell', price: sellPrice, size: sellSize });
        }
    }
    
    return { orders };
}

async function createSellGrid(symbol, currentPrice, totalUSDT, aggressionFactor = 0.9, gridConfig = null) {
    const orders = [];
    const gridCount = 3; // 降低到 3 档
    const priceRange = 0.08; // 扩大到 8%
    const MIN_ORDER_VALUE = 5; // 提高到 5 USDT
    
    // 检查是否有持仓
    const hasPosition = await checkPosition(symbol);
    
    // 无持仓或持仓太少时：直接挂买单（分批建仓），不挂卖单
    if (!hasPosition || hasPosition < 1) {
        log('   💡 无持仓，执行建仓策略：分批买入（宽网格）');
        
        // 使用总资金的 20% 分批建仓
        const buildPositionUSDT = totalUSDT * 0.20;
        const allocationPerOrder = buildPositionUSDT / gridCount;
        
        for (let i = 0; i < gridCount; i++) {
            // 在当前价下方 2%-6% 分批挂买单（更宽间距）
            const price = currentPrice * (1 - (i + 1) * 0.02);
            const size = allocationPerOrder / price;
            const orderValue = price * size;
            
            if (orderValue >= MIN_ORDER_VALUE) {
                orders.push({ side: 'buy', price, size });
            }
        }
        
        log(`   📊 建仓计划：${orders.length} 个买单，总计约 ${buildPositionUSDT.toFixed(2)} USDT`);
        return { orders };
    }
    
    // 有持仓：挂卖单（止盈/网格卖出）
    const configuredAmount = gridConfig && gridConfig.amount ? parseFloat(gridConfig.amount) : null;
    const positionSize = configuredAmount || hasPosition;
    
    for (let i = 0; i < gridCount; i++) {
        const price = currentPrice * (1 + (i + 1) * (priceRange / gridCount));
        const size = positionSize / gridCount;
        const orderValue = price * size;
        
        if (orderValue < MIN_ORDER_VALUE) {
            log(`   ⚠️ 订单金额 ${orderValue.toFixed(2)} USDT < ${MIN_ORDER_VALUE}，跳过`);
            continue;
        }
        orders.push({ side: 'sell', price, size });
    }
    
    if (orders.length === 0) {
        log(`   ⚠️ 无有效卖单 (持仓不足)`);
    }
    
    return { orders };
}

// 检查是否有持仓
async function checkPosition(symbol) {
    try {
        const baseCoin = symbol.replace('USDT', '');
        const balance = await request('/spot/account/assets', 'GET');
        if (balance.error) return 0;
        
        const asset = balance.find(b => b.coin === baseCoin);
        if (!asset) return 0;
        
        const available = parseFloat(asset.available || 0);
        const locked = parseFloat(asset.frozen || 0);
        return available + locked;
    } catch (e) {
        return 0;
    }
}

function createNeutralGrid(symbol, currentPrice, totalUSDT) {
    const orders = [];
    const gridCount = 3;
    const priceRange = 0.08; // 扩大到 8%
    const MIN_ORDER_VALUE = 5; // 提高到 5 USDT
    
    // 中性策略：上下对称挂单（宽网格）
    for (let i = 0; i < gridCount; i++) {
        const buyPrice = currentPrice * (1 - (i + 1) * (priceRange / gridCount));
        const sellPrice = currentPrice * (1 + (i + 1) * (priceRange / gridCount));
        const allocation = totalUSDT / 2 / gridCount;
        
        // 确保订单金额 ≥ 最小值
        if (allocation >= MIN_ORDER_VALUE) {
            const size = allocation / buyPrice;
            orders.push({ side: 'buy', price: buyPrice, size });
            orders.push({ side: 'sell', price: sellPrice, size });
        }
    }
    
    return { orders };
}

// 保存状态
function saveState(state) {
    fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

// 主函数
async function main() {
    log('=' .repeat(70));
    log('🤖 Bitget 智能网格 - 技术指标驱动');
    log('=' .repeat(70));
    
    const state = {
        timestamp: new Date().toISOString(),
        grids: []
    };
    
    // 处理每个网格配置
    for (const gridName of Object.keys(SETTINGS)) {
        const gridConfig = SETTINGS[gridName];
        if (!gridConfig.symbol) continue;
        
        const { symbol } = gridConfig;
        
        // 检查是否启用
        if (gridConfig.enabled === false) {
            log(`\n⏭️  跳过 ${gridName} (${symbol}) - 已禁用`);
            continue;
        }
        log(`\n📊 分析 ${gridName} (${symbol})...`);
        
        // 获取 K 线数据
        const klines = await getKlines(symbol, '1h', 100);
        if (klines.length === 0) {
            log('   ❌ 无法获取 K 线数据');
            continue;
        }
        
        // 计算技术指标
        const rsi = calculateRSI(klines, INDICATORS.RSI_PERIOD);
        const macd = calculateMACD(klines, INDICATORS.MACD_FAST, INDICATORS.MACD_SLOW, INDICATORS.MACD_SIGNAL);
        const bollinger = calculateBollinger(klines, INDICATORS.BOLLINGER_PERIOD, INDICATORS.BOLLINGER_STD);
        
        const currentPrice = klines[klines.length - 1].close;
        log(`   💰 当前价格：${currentPrice}`);
        log(`   📈 RSI: ${rsi ? rsi.toFixed(2) : 'N/A'}`);
        log(`   📊 MACD: ${macd ? `DIF=${macd.macdLine.toFixed(4)}, DEA=${macd.signalLine?.toFixed(4)}, Histogram=${macd.histogram.toFixed(4)}` : 'N/A'}`);
        log(`   📉 布林带：${bollinger ? `上=${bollinger.upperBand.toFixed(2)}, 中=${bollinger.middleBand.toFixed(2)}, 下=${bollinger.lowerBand.toFixed(2)}` : 'N/A'}`);
        
        // 趋势判断
        const trend = analyzeTrend(rsi, macd, bollinger);
        log(`   🎯 趋势判断：${trend}`);
        
        // 获取余额
        const balance = await getBalance();
        
        // 取消旧订单并下新订单
        log('   🔄 调整挂单...');
        const cancelled = await cancelAllOrders(symbol);
        log(`   ✅ 已取消 ${cancelled} 个旧订单`);
        
        await placeGridOrders(symbol, trend, balance, currentPrice, gridConfig);
        
        state.grids.push({
            name: gridName,
            symbol,
            trend,
            rsi,
            macd: macd ? { ...macd } : null,
            bollinger: bollinger ? { ...bollinger } : null,
            price: currentPrice
        });
    }
    
    saveState(state);
    
    log('\n' + '=' .repeat(70));
    log('✅ 智能网格调整完成');
    log('=' .repeat(70) + '\n');
}

main().catch(e => {
    log('❌ 智能网格执行失败：' + e.message);
    process.exit(1);
});
