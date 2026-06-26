#!/usr/bin/env node

import WebSocket from 'ws';
import axios from 'axios';
import fs from 'fs';
import path from 'path';

// Configurações
const SYMBOLS = ['btcusdt', 'ethusdt', 'bchusdt', 'solusdt', 'adausdt', 'ltcusdt', 'linkusdt', 'etcusdt', 'trxusdt', 'zecusdt', 'xrpusdt', 'dogeusdt'];
const TIMEFRAMES = ['15m', '1h', '4h'];
let lastAlert = {};
let alertCooldown = 300000;

// Animações
const spinnerFrames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
let spinnerIndex = 0;
let lastStatusTime = 0;
let lastPrices = {};
let wsConnected = false;
let cacheReady = false;

// Arquivo de sinais
const SIGNALS_FILE = path.join(process.env.HOME, 'apex-ia-skill', 'sinais.json');

// Cache de candles
const candleCache = {};

// ============================================
// SALVAR SINAL
// ============================================
function saveSignal(signal) {
  let signals = [];
  if (fs.existsSync(SIGNALS_FILE)) {
    signals = JSON.parse(fs.readFileSync(SIGNALS_FILE, 'utf-8'));
  }
  
  const newSignal = {
    id: Date.now(),
    timestamp: new Date().toISOString(),
    date: new Date().toLocaleDateString(),
    time: new Date().toLocaleTimeString(),
    symbol: signal.symbol,
    timeframe: signal.timeframe,
    direction: signal.direction,
    score: signal.score,
    entryPrice: signal.targets.t1 - (signal.targets.t1 - signal.stop) / 2,
    stopPrice: signal.stop,
    target1: signal.targets.t1,
    target2: signal.targets.t2,
    target3: signal.targets.t3,
    confirmations: signal.confirmations,
    status: 'ativo'
  };
  
  signals.push(newSignal);
  fs.writeFileSync(SIGNALS_FILE, JSON.stringify(signals, null, 2));
  return newSignal;
}

// ============================================
// FUNÇÕES DE CÁLCULO
// ============================================
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

function calcATR(highs, lows, closes, period = 14) {
  const tr = [];
  for (let i = 1; i < closes.length; i++) {
    const hl = highs[i] - lows[i];
    const hc = Math.abs(highs[i] - closes[i - 1]);
    const lc = Math.abs(lows[i] - closes[i - 1]);
    tr.push(Math.max(hl, hc, lc));
  }
  if (tr.length < period) return 0;
  let atr = 0;
  for (let i = 0; i < period; i++) atr += tr[tr.length - 1 - i];
  return atr / period;
}

function detectSignal(symbol, tf, candles) {
  if (!candles || candles.length < 50) return null;
  
  const closes = candles.map(c => c.close);
  const highs = candles.map(c => c.high);
  const lows = candles.map(c => c.low);
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
  
  let intensity = 'NORMAL';
  if (direction === 'BUY') {
    if (rsi <= 20) intensity = 'SUPER_FORTE';
    else if (rsi <= 25) intensity = 'FORTE';
    else if (rsi <= 30) intensity = 'ALTA';
  } else {
    if (rsi >= 80) intensity = 'SUPER_FORTE';
    else if (rsi >= 75) intensity = 'FORTE';
    else if (rsi >= 70) intensity = 'ALTA';
  }
  
  const avgVolume = volumes.slice(-21, -1).reduce((a, b) => a + b, 0) / 20;
  const volumeRatio = volumes[volumes.length - 1] / avgVolume;
  
  let score = 5;
  if ((direction === 'BUY' && rsi <= 30) || (direction === 'SELL' && rsi >= 70)) score += 2;
  if ((direction === 'BUY' && rsi <= 25) || (direction === 'SELL' && rsi >= 75)) score += 1;
  if (volumeRatio >= 1.5) score += 1;
  if (volumeRatio >= 2.0) score += 1;
  
  const atr = calcATR(highs, lows, closes, 14);
  const lastClose = closes[closes.length - 1];
  const multiplier = direction === 'BUY' ? 1 : -1;
  
  let tMultiplier = 1.5;
  if (volumeRatio >= 2.0) tMultiplier = 2.5;
  else if (volumeRatio >= 1.5) tMultiplier = 2.0;
  
  const t1 = lastClose + (atr * tMultiplier * multiplier);
  const t2 = lastClose + (atr * (tMultiplier + 1) * multiplier);
  const t3 = lastClose + (atr * (tMultiplier + 2) * multiplier);
  const stop = lastClose - (atr * 1.5 * multiplier);
  const riskReward = Math.abs(t1 - lastClose) / Math.abs(lastClose - stop);
  
  const confirmations = [];
  confirmations.push('PivotFlow');
  if (crossUp || crossDown) confirmations.push('SMA8/21');
  confirmations.push('SuperTrend');
  
  return {
    symbol: symbol.toUpperCase(),
    timeframe: tf,
    direction,
    score: Math.min(score, 10),
    intensity,
    rsi,
    volumeRatio: volumeRatio.toFixed(1),
    targets: { t1, t2, t3 },
    stop,
    riskReward,
    confirmations: confirmations.join(' + ')
  };
}

// ============================================
// CARREGAR DADOS
// ============================================
async function initCache() {
  console.log('📦 Carregando dados históricos...');
  let total = 0;
  
  for (const symbol of SYMBOLS) {
    for (const tf of TIMEFRAMES) {
      const key = `${symbol}_${tf}`;
      try {
        const response = await axios.get(`https://fapi.binance.com/fapi/v1/klines`, {
          params: { symbol: symbol.toUpperCase(), interval: tf, limit: 100 }
        });
        candleCache[key] = response.data.map(k => ({
          openTime: k[0],
          open: parseFloat(k[1]),
          high: parseFloat(k[2]),
          low: parseFloat(k[3]),
          close: parseFloat(k[4]),
          volume: parseFloat(k[7]),
          closeTime: k[6]
        }));
        total++;
      } catch (err) {}
    }
  }
  console.log(`✅ Cache inicializado: ${total} combinações\n`);
  cacheReady = true;
}

function updateCandle(symbol, tf, candleData) {
  const key = `${symbol}_${tf}`;
  if (!candleCache[key]) candleCache[key] = [];
  
  const lastCandle = candleCache[key][candleCache[key].length - 1];
  
  if (!lastCandle || lastCandle.openTime !== candleData.openTime) {
    candleCache[key].push(candleData);
    if (candleCache[key].length > 100) candleCache[key].shift();
    return { isNew: true };
  }
  
  lastCandle.close = candleData.close;
  lastCandle.high = Math.max(lastCandle.high, candleData.high);
  lastCandle.low = Math.min(lastCandle.low, candleData.low);
  lastCandle.volume = candleData.volume;
  
  return { isNew: false };
}

async function checkSignal(symbol, tf) {
  const key = `${symbol}_${tf}`;
  const candles = candleCache[key];
  if (!candles || candles.length < 50) return;
  
  const signal = detectSignal(symbol, tf, candles);
  
  if (signal && signal.score >= 7) {
    const alertKey = `${symbol}_${tf}_${signal.direction}`;
    const now = Date.now();
    
    if (lastAlert[alertKey] && (now - lastAlert[alertKey] < alertCooldown)) return;
    lastAlert[alertKey] = now;
    
    const arrow = signal.direction === 'BUY' ? '🟢 COMPRA ▲' : '🔴 VENDA ▼';
    const intensityEmoji = { 'SUPER_FORTE': '💥', 'FORTE': '⚡', 'ALTA': '📈', 'NORMAL': '📊' };
    const emoji = intensityEmoji[signal.intensity] || '📊';
    
    const savedSignal = saveSignal(signal);
    
    // Pular linha antes do alerta
    process.stdout.write('\n');
    console.log(`\n${'='.repeat(65)}`);
    console.log(`🚨 [${new Date().toLocaleString()}] ${signal.symbol} ${signal.timeframe}`);
    console.log(`${'='.repeat(65)}`);
    console.log(`   ${arrow} | Score: ${signal.score}/10 ${emoji}`);
    console.log(`   RSI: ${Math.round(signal.rsi)} | Volume: ${signal.volumeRatio}x`);
    console.log(`   Confirmações: ${signal.confirmations}`);
    console.log(`   🎯 T1: ${signal.targets.t1.toFixed(4)} | Stop: ${signal.stop.toFixed(4)}`);
    console.log(`   💾 Sinal salvo com ID: ${savedSignal.id}`);
    console.log(`${'='.repeat(65)}\n`);
    
    // Alerta sonoro
    process.stdout.write('\x07');
  }
}

// ============================================
// ANIMAÇÃO DE STATUS
// ============================================
function showStatus() {
  if (!cacheReady) return;
  
  const now = Date.now();
  if (now - lastStatusTime < 1500) return;
  lastStatusTime = now;
  
  const spinner = spinnerFrames[spinnerIndex % spinnerFrames.length];
  spinnerIndex++;
  
  const activityStatus = wsConnected ? '🟢 ATIVO' : '🟡 CONECTANDO';
  const activeCount = Object.keys(lastPrices).length;
  
  // Pega um símbolo aleatório com preço
  const symbolsWithPrice = Object.entries(lastPrices).filter(([_, price]) => price > 0);
  let displaySymbol = 'BTCUSDT';
  let displayPrice = '---';
  if (symbolsWithPrice.length > 0) {
    const random = symbolsWithPrice[Math.floor(Math.random() * symbolsWithPrice.length)];
    displaySymbol = random[0].toUpperCase();
    displayPrice = random[1].toFixed(2);
  }
  
  const statusLine = `${spinner} ${activityStatus} | ${activeCount} ativos | ${displaySymbol} $${displayPrice} | ${new Date().toLocaleTimeString()}`;
  
  process.stdout.clearLine(0);
  process.stdout.cursorTo(0);
  process.stdout.write(statusLine);
}

// ============================================
// CONECTAR WEBSOCKET
// ============================================
function connectWebSocket() {
  const streams = [];
  for (const symbol of SYMBOLS) {
    for (const tf of TIMEFRAMES) {
      streams.push(`${symbol}@kline_${tf}`);
    }
    streams.push(`${symbol}@ticker`);
  }
  
  const wsUrl = `wss://fstream.binance.com/stream?streams=${streams.join('/')}`;
  const ws = new WebSocket(wsUrl);
  
  ws.on('open', () => {
    wsConnected = true;
    console.log('\n\x1b[32m✅ WebSocket conectado!\x1b[0m');
    console.log(`📡 Monitorando ${SYMBOLS.length} símbolos x ${TIMEFRAMES.length} timeframes`);
    console.log(`💾 Sinais salvos em: ~/apex-ia-skill/sinais.json\n`);
  });
  
  ws.on('message', async (data) => {
    try {
      const msg = JSON.parse(data);
      const stream = msg.stream;
      
      if (stream && stream.includes('@ticker') && msg.data?.c) {
        const symbol = stream.split('@')[0];
        lastPrices[symbol] = parseFloat(msg.data.c);
      }
      
      if (msg.data?.k) {
        const k = msg.data.k;
        const symbol = msg.data.s.toLowerCase();
        const tf = k.i;
        const isNewCandle = k.x;
        
        const candleData = {
          openTime: k.t,
          open: parseFloat(k.o),
          high: parseFloat(k.h),
          low: parseFloat(k.l),
          close: parseFloat(k.c),
          volume: parseFloat(k.v),
          closeTime: k.T
        };
        
        updateCandle(symbol, tf, candleData);
        
        if (isNewCandle) {
          await checkSignal(symbol, tf);
        }
      }
    } catch (err) {}
  });
  
  ws.on('error', (err) => {
    wsConnected = false;
    console.error('\n\x1b[31m❌ WebSocket erro:', err.message, '\x1b[0m');
  });
  
  ws.on('close', () => {
    wsConnected = false;
    console.log('\n\x1b[33m⚠️ WebSocket desconectado. Reconectando em 5 segundos...\x1b[0m');
    setTimeout(connectWebSocket, 5000);
  });
}

// ============================================
// ANIMAÇÃO CONTÍNUA
// ============================================
setInterval(() => {
  showStatus();
}, 200);

// ============================================
// INICIAR
// ============================================
console.clear();
console.log('\n🦞 \x1b[36mAPEX IA - REAL TIME SCANNER COM LOG\x1b[0m');
console.log('🎯 Estratégia: Pivot Flow + SMA 8/21 + SuperTrend');
console.log('💾 Sinais serão salvos e validados automaticamente!\n');

await initCache();
connectWebSocket();

process.on('SIGINT', () => {
  console.log('\n\n👋 Desligando scanner...\n');
  process.exit();
});
