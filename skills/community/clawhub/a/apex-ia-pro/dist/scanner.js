import axios from 'axios';
// ============================================
// INDICADOR 1: PIVOT TREND FLOW (BigBeluga)
// ============================================
function calculatePivotTrendFlow(highs, lows, closes, length = 2, avgWindow = 5) {
    // Detectar pivôs
    const phArray = [];
    const plArray = [];
    for (let i = length; i < highs.length - length; i++) {
        let isPivotHigh = true;
        let isPivotLow = true;
        for (let j = 1; j <= length; j++) {
            if (highs[i] <= highs[i - j] || highs[i] <= highs[i + j])
                isPivotHigh = false;
            if (lows[i] >= lows[i - j] || lows[i] >= lows[i + j])
                isPivotLow = false;
        }
        if (isPivotHigh)
            phArray.push(highs[i]);
        if (isPivotLow)
            plArray.push(lows[i]);
        // Manter apenas as últimas avgWindow
        while (phArray.length > avgWindow)
            phArray.shift();
        while (plArray.length > avgWindow)
            plArray.shift();
    }
    const upper = phArray.length > 0 ? phArray.reduce((a, b) => a + b, 0) / phArray.length : closes[closes.length - 1];
    const lower = plArray.length > 0 ? plArray.reduce((a, b) => a + b, 0) / plArray.length : closes[closes.length - 1];
    const lastClose = closes[closes.length - 1];
    let direction = null;
    if (lastClose > upper)
        direction = 'BUY';
    else if (lastClose < lower)
        direction = 'SELL';
    return { direction, upper, lower };
}
// ============================================
// INDICADOR 2: SMA 8/21
// ============================================
function calculateSMA(data, length) {
    const sma = [];
    for (let i = length - 1; i < data.length; i++) {
        const sum = data.slice(i - length + 1, i + 1).reduce((a, b) => a + b, 0);
        sma.push(sum / length);
    }
    return sma;
}
function detectSmaCross(closes) {
    if (closes.length < 50)
        return { crossed: false, direction: null };
    const sma8 = calculateSMA(closes, 8);
    const sma21 = calculateSMA(closes, 21);
    if (sma8.length < 2 || sma21.length < 2)
        return { crossed: false, direction: null };
    const currSma8 = sma8[sma8.length - 1];
    const currSma21 = sma21[sma21.length - 1];
    const prevSma8 = sma8[sma8.length - 2];
    const prevSma21 = sma21[sma21.length - 2];
    const crossedUp = prevSma8 <= prevSma21 && currSma8 > currSma21;
    const crossedDown = prevSma8 >= prevSma21 && currSma8 < currSma21;
    if (crossedUp)
        return { crossed: true, direction: 'BUY' };
    if (crossedDown)
        return { crossed: true, direction: 'SELL' };
    return { crossed: false, direction: null };
}
// ============================================
// INDICADOR 3: PIVOT SUPERTREND
// ============================================
function calculateSuperTrend(highs, lows, closes, period = 10, multiplier = 2) {
    const atr = calculateATR(highs, lows, closes, period);
    const hl2 = highs.map((h, i) => (h + lows[i]) / 2);
    let upperBand = hl2.map(v => v + multiplier * atr);
    let lowerBand = hl2.map(v => v - multiplier * atr);
    let trend = [];
    let superTrend = [];
    for (let i = 0; i < closes.length; i++) {
        if (i === 0) {
            trend[i] = 'BUY';
            superTrend[i] = lowerBand[i];
        }
        else {
            if (trend[i - 1] === 'BUY') {
                if (closes[i] > lowerBand[i]) {
                    trend[i] = 'BUY';
                    superTrend[i] = Math.max(lowerBand[i], lowerBand[i - 1]);
                }
                else {
                    trend[i] = 'SELL';
                    superTrend[i] = upperBand[i];
                }
            }
            else {
                if (closes[i] < upperBand[i]) {
                    trend[i] = 'SELL';
                    superTrend[i] = Math.min(upperBand[i], upperBand[i - 1]);
                }
                else {
                    trend[i] = 'BUY';
                    superTrend[i] = lowerBand[i];
                }
            }
        }
    }
    return { trend: trend[trend.length - 1], band: superTrend[superTrend.length - 1] };
}
function calculateATR(highs, lows, closes, period = 14) {
    const tr = [];
    for (let i = 1; i < closes.length; i++) {
        const hl = highs[i] - lows[i];
        const hc = Math.abs(highs[i] - closes[i - 1]);
        const lc = Math.abs(lows[i] - closes[i - 1]);
        tr.push(Math.max(hl, hc, lc));
    }
    if (tr.length < period)
        return 0;
    let atr = 0;
    for (let i = 0; i < period; i++)
        atr += tr[tr.length - 1 - i];
    return atr / period;
}
function calculateFinalSignal(symbol, timeframe, candles) {
    if (candles.length < 50)
        return null;
    const closes = candles.map(c => c.close);
    const highs = candles.map(c => c.high);
    const lows = candles.map(c => c.low);
    const volumes = candles.map(c => c.volume);
    // 1. Pivot Trend Flow (BigBeluga)
    const { direction: pivotDirection } = calculatePivotTrendFlow(highs, lows, closes, 2, 5);
    // 2. SMA 8/21 Cross
    const { crossed: smaCrossed, direction: smaDirection } = detectSmaCross(closes);
    // 3. SuperTrend
    const { trend: superTrend } = calculateSuperTrend(highs, lows, closes, 10, 2);
    // SE não houver direção do Pivot, não gera sinal
    if (!pivotDirection)
        return null;
    // CONFIRMAÇÃO: Pivot Trend Flow deve estar alinhado com SMA Cross (se ocorreu)
    let direction = pivotDirection;
    let score = 5;
    // Confirmação do SMA Cross
    if (smaCrossed && smaDirection === direction) {
        score += 3;
    }
    // Confirmação do SuperTrend
    if (superTrend === direction) {
        score += 2;
    }
    // Score mínimo para gerar alerta
    if (score < 7)
        return null;
    // Volume relativo
    const avgVolume = volumes.slice(-21, -1).reduce((a, b) => a + b, 0) / 20;
    const volumeRatio = candles[candles.length - 1].volume / avgVolume;
    if (volumeRatio >= 1.3)
        score += 1;
    if (volumeRatio >= 1.8)
        score += 1;
    // RSI para intensidade
    const rsi = calculateRSI(closes, 14);
    let intensity = 'NORMAL';
    if (direction === 'BUY') {
        if (rsi <= 20)
            intensity = 'SUPER_FORTE';
        else if (rsi <= 25)
            intensity = 'FORTE';
        else if (rsi <= 30)
            intensity = 'ALTA';
    }
    else {
        if (rsi >= 80)
            intensity = 'SUPER_FORTE';
        else if (rsi >= 75)
            intensity = 'FORTE';
        else if (rsi >= 70)
            intensity = 'ALTA';
    }
    // ATR para alvos
    const atr = calculateATR(highs, lows, closes, 14);
    const lastClose = candles[candles.length - 1].close;
    const directionMultiplier = direction === 'BUY' ? 1 : -1;
    const t1 = lastClose + (atr * 1.5 * directionMultiplier);
    const t2 = lastClose + (atr * 2.5 * directionMultiplier);
    const t3 = lastClose + (atr * 4.0 * directionMultiplier);
    const stop = lastClose - (atr * 1.5 * directionMultiplier);
    const riskReward = Math.abs(t1 - lastClose) / Math.abs(lastClose - stop);
    return {
        symbol,
        timeframe,
        direction,
        pivotTrendFlow: pivotDirection,
        smaCross: smaCrossed ? smaDirection : null,
        superTrend,
        score: Math.min(score, 10),
        intensity,
        targets: { t1, t2, t3 },
        stop,
        riskReward
    };
}
function calculateRSI(closes, period = 14) {
    if (closes.length < period + 1)
        return 50;
    let gains = 0, losses = 0;
    for (let i = closes.length - period; i < closes.length; i++) {
        const diff = closes[i] - closes[i - 1];
        if (diff >= 0)
            gains += diff;
        else
            losses -= diff;
    }
    const avgGain = gains / period;
    const avgLoss = losses / period;
    if (avgLoss === 0)
        return 100;
    return 100 - (100 / (1 + avgGain / avgLoss));
}
// ============================================
// BUSCA DE DADOS REAIS DA BINANCE
// ============================================
async function fetchSymbols() {
    const response = await axios.get('https://fapi.binance.com/fapi/v1/exchangeInfo');
    const symbols = response.data.symbols
        .filter((s) => s.status === 'TRADING' &&
        s.contractType === 'PERPETUAL' &&
        s.quoteAsset === 'USDT')
        .map((s) => s.symbol);
    return symbols;
}
async function fetchKlines(symbol, interval, limit = 100) {
    const response = await axios.get('https://fapi.binance.com/fapi/v1/klines', {
        params: { symbol, interval, limit }
    });
    return response.data.map((k) => ({
        openTime: k[0],
        open: parseFloat(k[1]),
        high: parseFloat(k[2]),
        low: parseFloat(k[3]),
        close: parseFloat(k[4]),
        volume: parseFloat(k[7]),
        closeTime: k[6]
    }));
}
async function scanSymbol(symbol, timeframes) {
    const results = [];
    const intervalMap = {
        '1m': '1m', '5m': '5m', '15m': '15m', '30m': '30m',
        '1h': '1h', '4h': '4h', '1d': '1d'
    };
    for (const tf of timeframes) {
        try {
            const candles = await fetchKlines(symbol, intervalMap[tf] || '1h', 100);
            const signal = calculateFinalSignal(symbol, tf, candles);
            if (signal && signal.score >= 6) {
                results.push(signal);
            }
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        catch (error) {
            // Silencia erros individuais
        }
    }
    return results;
}
// ============================================
// FUNÇÃO PRINCIPAL scanAll
// ============================================
export async function scanAll(options = {}) {
    const { minScore = 6, includeTFs = ['15m', '1h', '4h'], symbolLimit = 30 } = options;
    console.log(`🔍 Escaneando até ${symbolLimit} pares...`);
    let symbols = await fetchSymbols();
    if (symbolLimit && symbols.length > symbolLimit) {
        symbols = symbols.slice(0, symbolLimit);
    }
    const allSignals = [];
    const batchSize = 3;
    for (let i = 0; i < symbols.length; i += batchSize) {
        const batch = symbols.slice(i, i + batchSize);
        const batchResults = await Promise.all(batch.map(symbol => scanSymbol(symbol, includeTFs)));
        allSignals.push(...batchResults.flat());
    }
    const filtered = allSignals.filter(s => s.score >= minScore);
    filtered.sort((a, b) => b.score - a.score);
    return filtered;
}
// ============================================
// FORMATAÇÃO PARA EXIBIÇÃO
// ============================================
export function formatSignalForDisplay(signal) {
    const arrow = signal.direction === 'BUY' ? '🟢 COMPRA ▲' : '🔴 VENDA ▼';
    const intensityEmoji = {
        'SUPER_FORTE': '💥',
        'FORTE': '⚡',
        'ALTA': '📈',
        'NORMAL': '📊'
    };
    const emoji = intensityEmoji[signal.intensity] || '📊';
    let confirmations = [];
    if (signal.pivotTrendFlow === signal.direction)
        confirmations.push('PivotFlow');
    if (signal.smaCross === signal.direction)
        confirmations.push('SMA8/21');
    if (signal.superTrend === signal.direction)
        confirmations.push('SuperTrend');
    return `
✅ **${signal.symbol}** - ${arrow} (${signal.timeframe})
   ${emoji} Score: ${signal.score}/10 | ${confirmations.join(' + ')}
   🎯 T1: ${signal.targets.t1.toFixed(4)} | T2: ${signal.targets.t2.toFixed(4)} | T3: ${signal.targets.t3.toFixed(4)}
   🛑 Stop: ${signal.stop.toFixed(4)} | RR: ${signal.riskReward.toFixed(2)}x`;
}
