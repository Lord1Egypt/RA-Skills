#!/usr/bin/env node

import axios from 'axios';
import fs from 'fs';
import path from 'path';

const SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'BCHUSDT', 'SOLUSDT', 'ADAUSDT'];
const SIGNALS_FILE = path.join(process.env.HOME, 'apex-ia-skill', 'sinais.json');
let lastCheck = 0;

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
  
  if (!crossUp && !crossDown) return null;
  
  const direction = crossUp ? 'BUY' : 'SELL';
  
  // Calcular RSI simplificado
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
  score = Math.min(score, 10);
  
  return {
    symbol,
    timeframe,
    direction,
    score,
    rsi: Math.round(rsi),
    entryPrice: candles[candles.length - 1].close
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
      volume: parseFloat(k[5])
    }));
  } catch (err) {
    console.error(`Erro ao buscar ${symbol}:`, err.message);
    return null;
  }
}

async function scan() {
  console.log(`\n📊 [${new Date().toLocaleTimeString()}] Escaneando...`);
  
  for (const symbol of SYMBOLS) {
    const candles = await fetchKlines(symbol, '1h');
    if (candles) {
      const signal = detectSignal(symbol, '1h', candles);
      if (signal && signal.score >= 7) {
        const count = saveSignal(signal);
        const arrow = signal.direction === 'BUY' ? '🟢 COMPRA ▲' : '🔴 VENDA ▼';
        console.log(`🚨 ${signal.symbol} - ${arrow} | Score: ${signal.score}/10 | RSI: ${signal.rsi}`);
        console.log(`   💾 Sinal salvo! Total: ${count}`);
        process.stdout.write('\x07');
      } else {
        console.log(`   ${symbol}: sem sinal (score: ${signal?.score || 'n/a'})`);
      }
    }
    await new Promise(r => setTimeout(r, 500));
  }
  console.log(`✅ Scan concluído.`);
}

// Loop infinito
console.clear();
console.log('\n🦞 APEX IA - REST SCANNER (sem WebSocket)');
console.log('🎯 Usando API REST, escaneia a cada 5 minutos\n');

// Executar primeiro scan
await scan();

// Agendar scans a cada 5 minutos
setInterval(async () => {
  await scan();
}, 5 * 60 * 1000);

process.on('SIGINT', () => {
  console.log('\n\n👋 Desligando...\n');
  process.exit();
});
