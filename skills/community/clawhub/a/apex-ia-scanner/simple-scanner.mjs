#!/usr/bin/env node

import WebSocket from 'ws';
import axios from 'axios';
import fs from 'fs';
import path from 'path';

const SYMBOLS = ['btcusdt', 'ethusdt', 'bchusdt', 'solusdt', 'adausdt'];
const SIGNALS_FILE = path.join(process.env.HOME, 'apex-ia-skill', 'sinais.json');

let lastPrices = {};
let lastStatusTime = 0;
const spinnerFrames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
let spinnerIndex = 0;

// Cache de candles
const candleCache = {};

function calcSMA(data, length) {
  const sma = [];
  for (let i = length - 1; i < data.length; i++) {
    const sum = data.slice(i - length + 1, i + 1).reduce((a, b) => a + b, 0);
    sma.push(sum / length);
  }
  return sma;
}

function calcRSI(closes, period = 14) {
  if (closes.length < period + 1) return 50;
  let gains = 0, losses = 0;
  for (let i = closes.length - period; i < closes.length; i++) {
    const diff = closes[i] - closes[i - 1];
    if (diff >= 0) gains += diff;
    else losses -= diff;
  }
  const avgGain = gains / period;
  const avgLoss = losses / period;
  if (avgLoss === 0) return 100;
  return 100 - (100 / (1 + avgGain / avgLoss));
}

function detectSignal(symbol, tf, candles) {
  if (!candles || candles.length < 50) return null;
  
  const closes = candles.map(c => c.close);
  const volumes = candles.map(c => c.volume);
  
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
  const rsi = calcRSI(closes, 14);
  
  const avgVolume = volumes.slice(-21, -1).reduce((a, b) => a + b, 0) / 20;
  const volumeRatio = volumes[volumes.length - 1] / avgVolume;
  
  let score = 5;
  if ((direction === 'BUY' && rsi <= 30) || (direction === 'SELL' && rsi >= 70)) score += 2;
  if (volumeRatio >= 1.5) score += 1;
  score = Math.min(score, 10);
  
  return {
    symbol: symbol.toUpperCase(),
    timeframe: tf,
    direction,
    score,
    entryPrice: candles[candles.length - 1].close,
    rsi: Math.round(rsi),
    volumeRatio: volumeRatio.toFixed(1)
  };
}

function saveSignal(signal) {
  let signals = [];
  if (fs.existsSync(SIGNALS_FILE)) {
    signals = JSON.parse(fs.readFileSync(SIGNALS_FILE, 'utf-8'));
  }
  
  signals.push({
    id: Date.now(),
    timestamp: new Date().toISOString(),
    ...signal,
    status: 'ativo'
  });
  
  fs.writeFileSync(SIGNALS_FILE, JSON.stringify(signals, null, 2));
  return signals.length;
}

async function fetchHistory(symbol) {
  for (const tf of ['15m', '1h']) {
    const key = `${symbol}_${tf}`;
    try {
      const res = await axios.get(`https://fapi.binance.com/fapi/v1/klines`, {
        params: { symbol: symbol.toUpperCase(), interval: tf, limit: 100 }
      });
      candleCache[key] = res.data.map(k => ({
        close: parseFloat(k[4]),
        volume: parseFloat(k[7])
      }));
    } catch (err) {}
  }
}

async function init() {
  console.log('📦 Carregando histórico...');
  for (const symbol of SYMBOLS) {
    await fetchHistory(symbol);
    await new Promise(r => setTimeout(r, 200));
  }
  console.log('✅ Pronto!\n');
}

function showStatus() {
  const now = Date.now();
  if (now - lastStatusTime < 1000) return;
  lastStatusTime = now;
  
  const spinner = spinnerFrames[spinnerIndex % spinnerFrames.length];
  spinnerIndex++;
  
  const btcPrice = lastPrices.btcusdt ? `$${lastPrices.btcusdt.toFixed(2)}` : '$---';
  const activeCount = Object.keys(lastPrices).length;
  
  const line = `${spinner} 🟢 ATIVO | ${activeCount} ativos | BTC ${btcPrice} | ${new Date().toLocaleTimeString()}`;
  process.stdout.clearLine(0);
  process.stdout.cursorTo(0);
  process.stdout.write(line);
}

function connectWebSocket() {
  // Streams separados por símbolo (mais estável)
  const ws = new WebSocket('wss://fstream.binance.com/ws');
  
  ws.on('open', () => {
    // Subscrever tickers e klines
    const subscribe = {
      method: 'SUBSCRIBE',
      params: [],
      id: 1
    };
    
    for (const symbol of SYMBOLS) {
      subscribe.params.push(`${symbol}@ticker`);
      subscribe.params.push(`${symbol}@kline_15m`);
    }
    
    ws.send(JSON.stringify(subscribe));
    console.log('\n✅ WebSocket conectado e inscrito!\n');
  });
  
  ws.on('message', async (data) => {
    try {
      const msg = JSON.parse(data);
      
      // Atualizar preços
      if (msg.stream?.includes('@ticker') && msg.data?.c) {
        const symbol = msg.stream.split('@')[0];
        lastPrices[symbol] = parseFloat(msg.data.c);
      }
      
      // Verificar klines
      if (msg.stream?.includes('@kline') && msg.data?.k) {
        const k = msg.data.k;
        const symbol = msg.stream.split('@')[0];
        const tf = k.i;
        const isNewCandle = k.x;
        
        if (isNewCandle) {
          const key = `${symbol}_${tf}`;
          const candles = candleCache[key];
          if (candles) {
            const signal = detectSignal(symbol, tf, candles);
            if (signal && signal.score >= 7) {
              const count = saveSignal(signal);
              const arrow = signal.direction === 'BUY' ? '🟢 COMPRA ▲' : '🔴 VENDA ▼';
              console.log(`\n🚨 ${signal.symbol} ${signal.timeframe} - ${arrow} | Score: ${signal.score}/10 | RSI: ${signal.rsi}`);
              console.log(`   💾 Sinal salvo! Total: ${count}\n`);
              process.stdout.write('\x07');
            }
          }
        }
      }
    } catch (err) {}
  });
  
  ws.on('error', (err) => {
    console.error('\n❌ Erro:', err.message);
  });
  
  ws.on('close', () => {
    console.log('\n⚠️ Desconectado. Reconectando em 5s...');
    setTimeout(connectWebSocket, 5000);
  });
}

console.clear();
console.log('\n🦞 APEX IA SCANNER SIMPLIFICADO\n');
await init();
connectWebSocket();

setInterval(() => showStatus(), 200);

process.on('SIGINT', () => {
  console.log('\n\n👋 Desligando...\n');
  process.exit();
});
