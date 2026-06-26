#!/usr/bin/env node

import axios from 'axios';
import fs from 'fs';
import path from 'path';

const SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'BCHUSDT', 'SOLUSDT', 'ADAUSDT', 'LTCUSDT', 'LINKUSDT'];
const SIGNALS_FILE = path.join(process.env.HOME, 'apex-ia-skill', 'sinais.json');

function saveSignal(signal) {
  let signals = [];
  if (fs.existsSync(SIGNALS_FILE)) {
    signals = JSON.parse(fs.readFileSync(SIGNALS_FILE, 'utf-8'));
  }
  signals.push({
    id: Date.now(),
    timestamp: new Date().toISOString(),
    ...signal
  });
  fs.writeFileSync(SIGNALS_FILE, JSON.stringify(signals, null, 2));
  return signals.length;
}

function calcSMA(data, length) {
  const sma = [];
  for (let i = length - 1; i < data.length; i++) {
    const sum = data.slice(i - length + 1, i + 1).reduce((a, b) => a + b, 0);
    sma.push(sum / length);
  }
  return sma;
}

function detectSignal(symbol, timeframe, candles) {
  if (!candles || candles.length < 50) return null;
  
  const closes = candles.map(c => c.close);
  const sma8 = calcSMA(closes, 8);
  const sma21 = calcSMA(closes, 21);
  
  if (sma8.length < 2 || sma21.length < 2) return null;
  
  const curr8 = sma8[sma8.length - 1];
  const curr21 = sma21[sma21.length - 1];
  const prev8 = sma8[sma8.length - 2];
  const prev21 = sma21[sma21.length - 2];
  
  const crossUp = prev8 <= prev21 && curr8 > curr21;
  const crossDown = prev8 >= prev21 && curr8 < curr21;
  
  const lastClose = closes[closes.length - 1];
  
  // Se não há cruzamento, retorna score baixo para diagnóstico
  if (!crossUp && !crossDown) {
    // Calcula tendência atual (sem cruzamento)
    const trend = curr8 > curr21 ? 'ACIMA' : 'ABAIXO';
    return { symbol, timeframe, direction: null, score: 0, trend, sma8: curr8, sma21: curr21, price: lastClose };
  }
  
  const direction = crossUp ? 'BUY' : 'SELL';
  
  // Calcular RSI
  let gains = 0, losses = 0;
  for (let i = closes.length - 14; i < closes.length; i++) {
    const diff = closes[i] - closes[i - 1];
    if (diff >= 0) gains += diff;
    else losses -= diff;
  }
  const avgGain = gains / 14;
  const avgLoss = losses / 14;
  const rsi = avgLoss === 0 ? 100 : 100 - (100 / (1 + avgGain / avgLoss));
  
  let score = 5;
  if ((direction === 'BUY' && rsi <= 30) || (direction === 'SELL' && rsi >= 70)) score += 2;
  if ((direction === 'BUY' && rsi <= 25) || (direction === 'SELL' && rsi >= 75)) score += 1;
  score = Math.min(score, 10);
  
  // ATR simplificado para alvos
  const highs = candles.map(c => c.high);
  const lows = candles.map(c => c.low);
  let tr = [];
  for (let i = 1; i < closes.length; i++) {
    const hl = highs[i] - lows[i];
    const hc = Math.abs(highs[i] - closes[i - 1]);
    const lc = Math.abs(lows[i] - closes[i - 1]);
    tr.push(Math.max(hl, hc, lc));
  }
  const atr = tr.slice(-14).reduce((a, b) => a + b, 0) / 14;
  const multiplier = direction === 'BUY' ? 1 : -1;
  
  return {
    symbol,
    timeframe,
    direction,
    score,
    rsi: Math.round(rsi),
    entryPrice: lastClose,
    stop: lastClose - (atr * 1.5 * multiplier),
    target1: lastClose + (atr * 1.5 * multiplier),
    target2: lastClose + (atr * 2.5 * multiplier),
    trend: curr8 > curr21 ? 'ACIMA' : 'ABAIXO'
  };
}

async function fetchKlines(symbol, interval) {
  try {
    const response = await axios.get(`https://api.binance.com/api/v3/klines`, {
      params: { symbol, interval, limit: 100 },
      timeout: 10000
    });
    return response.data.map(k => ({
      close: parseFloat(k[4]),
      high: parseFloat(k[2]),
      low: parseFloat(k[3]),
      volume: parseFloat(k[5])
    }));
  } catch (err) {
    return null;
  }
}

async function scan() {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`📊 [${new Date().toLocaleString()}] SCAN APEX IA`);
  console.log(`${'='.repeat(60)}`);
  
  for (const symbol of SYMBOLS) {
    const candles = await fetchKlines(symbol, '1h');
    if (candles && candles.length >= 50) {
      const signal = detectSignal(symbol, '1h', candles);
      if (signal.score >= 7 && signal.direction) {
        const count = saveSignal(signal);
        const arrow = signal.direction === 'BUY' ? '🟢 COMPRA ▲' : '🔴 VENDA ▼';
        console.log(`\n🚨 ${arrow} ${signal.symbol} (${signal.timeframe})`);
        console.log(`   Score: ${signal.score}/10 | RSI: ${signal.rsi}`);
        console.log(`   Preço: $${signal.entryPrice.toFixed(2)}`);
        console.log(`   🎯 T1: $${signal.target1.toFixed(2)} | Stop: $${signal.stop.toFixed(2)}`);
        console.log(`   💾 Sinal salvo! Total: ${count}`);
        process.stdout.write('\x07');
      } else {
        const trendIcon = signal.trend === 'ACIMA' ? '📈' : '📉';
        console.log(`${trendIcon} ${symbol}: ${signal.trend} da SMA21 | Score: ${signal.score}${signal.direction ? ' (sinal fraco)' : ''}`);
      }
    } else {
      console.log(`⚠️ ${symbol}: sem dados suficientes`);
    }
    await new Promise(r => setTimeout(r, 300));
  }
  console.log(`\n✅ Scan concluído. Próximo em 5 minutos.\n`);
}

console.clear();
console.log('\n🦞 APEX IA - REST SCANNER v2');
console.log('🎯 SMA 8/21 Cross + RSI');
console.log('⏰ Escaneia a cada 5 minutos\n');

await scan();
setInterval(async () => { await scan(); }, 5 * 60 * 1000);

process.on('SIGINT', () => {
  console.log('\n\n👋 Desligando...\n');
  process.exit();
});
