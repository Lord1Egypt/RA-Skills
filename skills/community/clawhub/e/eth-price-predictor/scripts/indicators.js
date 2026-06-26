/**
 * 技术指标计算（复用BTC版本）
 */

function calculateRSI(prices, period = 14) {
  if (prices.length < period + 1) return null;
  
  let gains = 0, losses = 0;
  for (let i = 1; i <= period; i++) {
    const change = prices[i] - prices[i - 1];
    if (change > 0) gains += change;
    else losses -= change;
  }
  
  let avgGain = gains / period, avgLoss = losses / period;
  for (let i = period + 1; i < prices.length; i++) {
    const change = prices[i] - prices[i - 1];
    if (change > 0) {
      avgGain = (avgGain * (period - 1) + change) / period;
      avgLoss = (avgLoss * (period - 1)) / period;
    } else {
      avgGain = (avgGain * (period - 1)) / period;
      avgLoss = (avgLoss * (period - 1) - change) / period;
    }
  }
  
  return avgLoss === 0 ? 100 : 100 - (100 / (1 + avgGain / avgLoss));
}

function calculateEMA(prices, period) {
  if (prices.length < period) return null;
  const multiplier = 2 / (period + 1);
  let ema = prices.slice(0, period).reduce((a, b) => a + b) / period;
  for (let i = period; i < prices.length; i++) {
    ema = (prices[i] - ema) * multiplier + ema;
  }
  return ema;
}

function calculateMACD(prices) {
  if (prices.length < 26) return null;
  
  const ema12 = [], ema26 = [], macdLine = [];
  let e12 = prices.slice(0, 12).reduce((a, b) => a + b) / 12;
  for (let i = 12; i < prices.length; i++) {
    e12 = (prices[i] - e12) * (2 / 13) + e12;
    ema12.push(e12);
  }
  
  let e26 = prices.slice(0, 26).reduce((a, b) => a + b) / 26;
  for (let i = 26; i < prices.length; i++) {
    e26 = (prices[i] - e26) * (2 / 27) + e26;
    ema26.push(e26);
  }
  
  for (let i = 0; i < ema26.length; i++) {
    macdLine.push(ema12[i + 14] - ema26[i]);
  }
  
  const signal = calculateEMA(macdLine.slice(-12), 9);
  const macd = macdLine[macdLine.length - 1];
  
  return { macd, signal, histogram: macd - signal, trend: macd > signal ? 'bullish' : 'bearish' };
}

function calculateBollingerBands(prices, period = 20, stdDev = 2) {
  if (prices.length < period) return null;
  
  const recent = prices.slice(-period);
  const sma = recent.reduce((a, b) => a + b) / period;
  const variance = recent.reduce((sum, p) => sum + Math.pow(p - sma, 2), 0) / period;
  const std = Math.sqrt(variance);
  
  return {
    upper: sma + std * stdDev,
    middle: sma,
    lower: sma - std * stdDev,
    currentPrice: prices[prices.length - 1],
    position: prices[prices.length - 1] > sma ? 'above' : 'below'
  };
}

function calculateMomentum(prices, period = 10) {
  if (prices.length < period + 1) return null;
  const current = prices[prices.length - 1];
  const previous = prices[prices.length - 1 - period];
  return { value: current - previous, percent: ((current - previous) / previous) * 100 };
}

/**
 * 综合预测
 */
function predict(klines, timeframe = 'daily') {
  const closes = klines.map(k => k.close);
  const currentPrice = closes[closes.length - 1];
  
  const rsi = calculateRSI(closes);
  const macd = calculateMACD(closes);
  const boll = calculateBollingerBands(closes);
  const momentum = calculateMomentum(closes, timeframe === 'weekly' ? 7 : 5);
  
  const recentVolume = klines.slice(-3).map(k => k.volume);
  const avgVolume = klines.slice(-10).reduce((sum, k) => sum + k.volume, 0) / 10;
  const volumeChange = ((recentVolume[2] - avgVolume) / avgVolume) * 100;
  
  let bullishScore = 0, bearishScore = 0;
  const signals = [];
  
  // RSI判断（ETH波动大，调整区间）
  if (rsi < 35) {
    bullishScore += 2;
    signals.push({ indicator: 'RSI', value: rsi.toFixed(1), signal: '超卖 → 看涨', bullish: true });
  } else if (rsi > 65) {
    bearishScore += 2;
    signals.push({ indicator: 'RSI', value: rsi.toFixed(1), signal: '超买 → 看跌', bullish: false });
  } else if (rsi > 50) {
    bullishScore += 1;
    signals.push({ indicator: 'RSI', value: rsi.toFixed(1), signal: '偏多 → 看涨', bullish: true });
  } else {
    bearishScore += 1;
    signals.push({ indicator: 'RSI', value: rsi.toFixed(1), signal: '偏空 → 看跌', bullish: false });
  }
  
  // MACD判断
  if (macd.histogram > 0) {
    bullishScore += 2;
    signals.push({ indicator: 'MACD', value: '金叉', signal: '多头动能 → 看涨', bullish: true });
  } else {
    bearishScore += 2;
    signals.push({ indicator: 'MACD', value: '死叉', signal: '空头动能 → 看跌', bullish: false });
  }
  
  // 布林带判断
  if (currentPrice < boll.lower * 1.02) {
    bullishScore += 2;
    signals.push({ indicator: 'BOLL', value: '触及下轨', signal: '反弹信号 → 看涨', bullish: true });
  } else if (currentPrice > boll.upper * 0.98) {
    bearishScore += 1;
    signals.push({ indicator: 'BOLL', value: '触及上轨', signal: '回调风险', bullish: false });
  } else {
    signals.push({ indicator: 'BOLL', value: '中轨附近', signal: '震荡', bullish: null });
  }
  
  // 成交量判断
  if (volumeChange > 15) {
    if (momentum.value > 0) {
      bullishScore += 1;
      signals.push({ indicator: 'Volume', value: `+${volumeChange.toFixed(0)}%`, signal: '放量上涨 → 看涨', bullish: true });
    } else {
      bearishScore += 1;
      signals.push({ indicator: 'Volume', value: `+${volumeChange.toFixed(0)}%`, signal: '放量下跌 → 看跌', bullish: false });
    }
  } else {
    signals.push({ indicator: 'Volume', value: `${volumeChange.toFixed(0)}%`, signal: '成交量正常', bullish: null });
  }
  
  const totalScore = bullishScore + bearishScore;
  const confidence = totalScore > 0 ? Math.max(bullishScore, bearishScore) / totalScore : 0.5;
  
  // ETH止损止盈比例（波动比BTC大）
  const stopLossPercent = timeframe === 'weekly' ? 0.04 : 0.025;
  const takeProfitPercent = timeframe === 'weekly' ? 0.08 : 0.05;
  
  return {
    direction: bullishScore > bearishScore ? 'UP' : (bearishScore > bullishScore ? 'DOWN' : 'NEUTRAL'),
    confidence: Math.min(confidence * 100, 95),
    bullishScore,
    bearishScore,
    signals,
    indicators: { rsi, macd: macd.histogram, bollinger: boll, momentum, volumeChange },
    currentPrice,
    stopLoss: bullishScore > bearishScore ? currentPrice * (1 - stopLossPercent) : currentPrice * (1 + stopLossPercent),
    takeProfit: bullishScore > bearishScore ? currentPrice * (1 + takeProfitPercent) : currentPrice * (1 - takeProfitPercent)
  };
}

module.exports = {
  calculateRSI,
  calculateEMA,
  calculateMACD,
  calculateBollingerBands,
  calculateMomentum,
  predict
};
