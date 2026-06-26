#!/usr/bin/env node

import WebSocket from 'ws';
import axios from 'axios';

// Configurações
const SYMBOLS = ['btcusdt', 'ethusdt', 'bchusdt', 'solusdt', 'adausdt', 'ltcusdt', 'linkusdt', 'etcusdt', 'trxusdt', 'zecusdt', 'xrpusdt', 'dogeusdt'];
const TIMEFRAMES = ['15m', '1h', '4h'];
let lastAlert = {};
let alertCooldown = 300000;
let lastActivity = Date.now();
let spinnerFrames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
let spinnerIndex = 0;
let lastLogTime = 0;

// Cache de candles
const candleCache = {};
const lastPrices = {};

// ============================================
// CALCULAR SMA
// ============================================
function calcSMA(data, length) {
  const sma = [];
  for (let i = length - 1; i < data.length; i++) {
    const sum = data.slice(i - length + 1, i + 1).reduce((a, b) => a + b, 0);
    sma.push(sum / length);
  }
  return sma;
}

// ============================================
// CALCULAR RSI
// ============================================
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

// ============================================
// CALCULAR ATR
// ============================================
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

// ============================================
// DETECTAR SINAL
// ============================================
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
    riskReward
  };
}

// ============================================
// CARREGAR DADOS HISTÓRICOS
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
      } catch (err) {
        // Silencia
      }
    }
  }
  console.log(`✅ Cache inicializado: ${total} combinações\n`);
}

// ============================================
// ATUALIZAR CANDLE
// ============================================
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

// ============================================
// VERIFICAR SINAIS
// ============================================
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
    
    console.log(`\n${'='.repeat(65)}`);
    console.log(`🚨 [${new Date().toLocaleString()}] ${signal.symbol} ${signal.timeframe}`);
    console.log(`${'='.repeat(65)}`);
    console.log(`   ${arrow} | Score: ${signal.score}/10 ${emoji}`);
    console.log(`   RSI: ${Math.round(signal.rsi)} | Volume: ${signal.volumeRatio}x`);
    console.log(`   🎯 T1: ${signal.targets.t1.toFixed(4)} | Stop: ${signal.stop.toFixed(4)}`);
    console.log(`   📈 T2: ${signal.targets.t2.toFixed(4)} | T3: ${signal.targets.t3.toFixed(4)}`);
    console.log(`   📊 RR: ${signal.riskReward.toFixed(2)}x`);
    console.log(`${'='.repeat(65)}\n`);
  }
}

// ============================================
// MOSTRAR STATUS ANIMADO
// ============================================
function showStatus() {
  const now = Date.now();
  
  // A cada 2 segundos, atualiza a linha de status
  if (now - lastLogTime >= 2000) {
    lastLogTime = now;
    
    // Calcular mensagens recebidas por segundo (atividade)
    const elapsed = (now - lastActivity) / 1000;
    const activityStatus = elapsed < 5 ? '🟢 ATIVO' : '🟡 AGUARDANDO';
    
    // Contar quantos símbolos têm preço
    let activeSymbols = Object.keys(lastPrices).length;
    
    // Escolher um símbolo aleatório para mostrar
    const randomSymbol = SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)].toUpperCase();
    const randomPrice = lastPrices[randomSymbol?.toLowerCase()] || '---';
    
    // Criar linha de status com spinner
    const spinner = spinnerFrames[spinnerIndex % spinnerFrames.length];
    spinnerIndex++;
    
    const statusLine = `${spinner} ${activityStatus} | ${activeSymbols} ativos | Monitorando: ${randomSymbol} $${typeof randomPrice === 'number' ? randomPrice.toFixed(2) : '---'} | ${new Date().toLocaleTimeString()}`;
    
    // Limpar linha anterior e escrever nova
    process.stdout.clearLine(0);
    process.stdout.cursorTo(0);
    process.stdout.write(statusLine);
  }
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
    // Adicionar stream de ticker para preço atual
    streams.push(`${symbol}@ticker`);
  }
  
  const wsUrl = `wss://fstream.binance.com/stream?streams=${streams.join('/')}`;
  const ws = new WebSocket(wsUrl);
  
  ws.on('open', () => {
    console.log('\x1b[32m✅ WebSocket conectado!\x1b[0m');
    console.log(`📡 Monitorando ${SYMBOLS.length} símbolos x ${TIMEFRAMES.length} timeframes`);
    console.log(`🎯 Aguardando cruzamentos SMA 8/21...\n`);
    console.log('─'.repeat(65));
  });
  
  ws.on('message', async (data) => {
    lastActivity = Date.now();
    
    try {
      const msg = JSON.parse(data);
      const stream = msg.stream;
      
      // Processar ticker (preço atual)
      if (stream && stream.includes('@ticker')) {
        const symbol = stream.split('@')[0];
        if (msg.data && msg.data.c) {
          lastPrices[symbol] = parseFloat(msg.data.c);
        }
      }
      
      // Processar klines
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
    } catch (err) {
      // Silencia
    }
  });
  
  ws.on('error', (err) => {
    console.error('\n\x1b[31m❌ WebSocket erro:', err.message, '\x1b[0m');
  });
  
  ws.on('close', () => {
    console.log('\n\x1b[33m⚠️ WebSocket desconectado. Reconectando em 5 segundos...\x1b[0m');
    setTimeout(connectWebSocket, 5000);
  });
}

// ============================================
// ANIMAÇÃO DE STATUS (roda em paralelo)
// ============================================
setInterval(() => {
  if (lastActivity > 0) {
    showStatus();
  }
}, 200);

// ============================================
// INICIAR
// ============================================
console.clear();
console.log('\n🦞 \x1b[36mAPEX IA - REAL TIME SCANNER v3\x1b[0m');
console.log('🎯 Estratégia: Pivot Flow + SMA 8/21 + SuperTrend');
console.log('💡 Baseado no indicador BigBeluga do TradingView\n');

await initCache();
connectWebSocket();

// Keep alive
process.on('SIGINT', () => {
  console.log('\n\n👋 Desligando scanner...\n');
  process.exit();
});
