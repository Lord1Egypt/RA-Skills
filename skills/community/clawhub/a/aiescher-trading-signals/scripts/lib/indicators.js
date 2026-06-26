function calculateSMA(periods, length) {
  if (periods.length < length) return null;
  const closes = periods.slice(0, length).map(p => p.close);
  const sum = closes.reduce((a, b) => a + b, 0);
  return sum / length;
}

function calculateRSI(periods, length = 14) {
  if (periods.length < length + 1) return null;
  
  let gains = 0;
  let losses = 0;
  
  for (let i = 0; i < length; i++) {
    const change = periods[i].close - periods[i + 1].close;
    if (change > 0) gains += change;
    else losses -= change;
  }
  
  const avgGain = gains / length;
  const avgLoss = losses / length;
  
  if (avgLoss === 0) return 100;
  const rs = avgGain / avgLoss;
  return 100 - (100 / (1 + rs));
}

function calculateEMA(periods, length) {
  if (periods.length < length) return null;
  const multiplier = 2 / (length + 1);
  let ema = periods.slice(0, length).reduce((sum, p) => sum + p.close, 0) / length;
  
  for (let i = length - 1; i >= 0; i--) {
    ema = (periods[i].close * multiplier) + (ema * (1 - multiplier));
  }
  
  return ema;
}

function calculateMACD(periods) {
  const ema12 = calculateEMA(periods, 12);
  const ema26 = calculateEMA(periods, 26);
  
  if (!ema12 || !ema26) return null;
  
  const macdLine = ema12 - ema26;
  // Signal line is EMA9 of MACD - simplified
  return {
    macd: macdLine,
    signal: macdLine * 0.9, // Simplified approximation
    histogram: macdLine * 0.1
  };
}

function calculateBollingerBands(periods, length = 20, stdDev = 2) {
  const sma = calculateSMA(periods, length);
  if (!sma) return null;
  
  const closes = periods.slice(0, length).map(p => p.close);
  const variance = closes.reduce((sum, close) => sum + Math.pow(close - sma, 2), 0) / length;
  const std = Math.sqrt(variance);
  
  return {
    middle: sma,
    upper: sma + (stdDev * std),
    lower: sma - (stdDev * std)
  };
}

function generateSignals(data, config = {}) {
  const signals = [];
  const { rsiOversold = 30, rsiOverbought = 70 } = config;
  
  // RSI signals
  if (data.rsi !== null) {
    if (data.rsi < rsiOversold) {
      signals.push({ type: 'BUY', reason: `RSI überverkauft (${data.rsi.toFixed(1)})`, strength: 'strong' });
    } else if (data.rsi > rsiOverbought) {
      signals.push({ type: 'SELL', reason: `RSI überkauft (${data.rsi.toFixed(1)})`, strength: 'strong' });
    }
  }
  
  // Moving Average Crossover
  if (data.sma20 !== null && data.sma50 !== null) {
    if (data.sma20 > data.sma50 && data.price > data.sma20) {
      signals.push({ type: 'BUY', reason: 'Golden Cross (SMA20 > SMA50)', strength: 'medium' });
    } else if (data.sma20 < data.sma50 && data.price < data.sma20) {
      signals.push({ type: 'SELL', reason: 'Death Cross (SMA20 < SMA50)', strength: 'medium' });
    }
  }
  
  // Bollinger Bands
  if (data.bollingerBands !== null) {
    if (data.price < data.bollingerBands.lower) {
      signals.push({ type: 'BUY', reason: 'Preis unter unterer Bollinger Band', strength: 'medium' });
    } else if (data.price > data.bollingerBands.upper) {
      signals.push({ type: 'SELL', reason: 'Preis über oberer Bollinger Band', strength: 'medium' });
    }
  }
  
  // Price near SMA20
  if (data.sma20 !== null) {
    const distFromSMA20 = Math.abs(data.price - data.sma20) / data.sma20 * 100;
    if (distFromSMA20 < 1 && data.price > data.sma20) {
      signals.push({ type: 'BUY', reason: 'Preis nahe SMA20 (Bounce)', strength: 'weak' });
    } else if (distFromSMA20 < 1 && data.price < data.sma20) {
      signals.push({ type: 'SELL', reason: 'Preis nahe SMA20 (Abweisung)', strength: 'weak' });
    }
  }
  
  return signals;
}

function analyzeData(rawData, config = {}) {
  const periods = rawData.periods;
  
  return {
    ...rawData,
    sma20: calculateSMA(periods, 20),
    sma50: calculateSMA(periods, 50),
    rsi: calculateRSI(periods, 14),
    macd: calculateMACD(periods),
    bollingerBands: calculateBollingerBands(periods, 20, 2),
    signals: generateSignals({
      ...rawData,
      sma20: calculateSMA(periods, 20),
      sma50: calculateSMA(periods, 50),
      rsi: calculateRSI(periods, 14),
      bollingerBands: calculateBollingerBands(periods, 20, 2)
    }, config)
  };
}

module.exports = {
  calculateSMA,
  calculateRSI,
  calculateEMA,
  calculateMACD,
  calculateBollingerBands,
  generateSignals,
  analyzeData
};
