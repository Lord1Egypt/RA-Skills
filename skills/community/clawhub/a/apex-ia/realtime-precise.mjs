#!/usr/bin/env node

import WebSocket from 'ws';
import axios from 'axios';
import fs from 'fs';
import path from 'path';

const SYMBOLS = ['btcusdt', 'ethusdt', 'bchusdt', 'solusdt', 'adausdt'];
const SIGNALS_FILE = path.join(process.env.HOME, 'apex-ia-skill', 'sinais.json');

let lastPrices = {};
let candles = {};

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
// DETECTAR CRUZAMENTO AO VIVO
// ============================================
function detectLiveCross(symbol, tf, price, previousCandles) {
  if (!previousCandles || previousCandles.length < 50) return null;
  
  const closes = previousCandles.map(c => c.close);
  // Adicionar preço atual (ainda não fechado)
  const allCloses = [...closes, price];
  
  const sma8 = calcSMA(allCloses, 8);
  const sma21 = calcSMA(allCloses, 21);
  
  if (sma8.length < 2 || sma21.length < 2) return null;
  
  const curr8 = sma8[sma8.length - 1];
  const curr21 = sma21[sma21.length - 1];
  const prev8 = sma8[sma8.length - 2];
  const prev21 = sma21[sma21.length - 2];
  
  // DETECÇÃO PRECOCE: ainda dentro do candle
  const crossUp = prev8 <= prev21 && curr8 > curr21;
  const crossDown = prev8 >= prev21 && curr8 < curr21;
  
  if (!crossUp && !crossDown) return null;
  
  return {
    direction: crossUp ? 'BUY' : 'SELL',
    price: price,
    sma8: curr8,
    sma21: curr21,
    timestamp: Date.now()
  };
}

// ============================================
// SALVAR SINAL
// ============================================
function saveSignal(signal) {
  let signals = [];
  if (fs.existsSync(SIGNALS_FILE)) {
    signals = JSON.parse(fs.readFileSync(SIGNALS_FILE, 'utf-8'));
  }
  
  signals.push({
    id: Date.now(),
    timestamp: new Date().toISOString(),
    symbol: signal.symbol,
    timeframe: signal.timeframe,
    direction: signal.direction,
    price: signal.price,
    status: 'ativo'
  });
  
  fs.writeFileSync(SIGNALS_FILE, JSON.stringify(signals, null, 2));
  return signals.length;
}

// ============================================
// CARREGAR HISTÓRICO
// ============================================
async function loadHistory(symbol) {
  try {
    const res = await axios.get(`https://api.binance.com/api/v3/klines`, {
      params: { symbol: symbol.toUpperCase(), interval: '1h', limit: 100 }
    });
    candles[symbol] = res.data.map(k => ({
      close: parseFloat(k[4]),
      time: k[0]
    }));
  } catch (err) {
    console.error(`Erro carregando ${symbol}:`, err.message);
  }
}

// ============================================
// CONECTAR WEBSOCKET
// ============================================
async function connect() {
  // Carregar histórico primeiro
  for (const symbol of SYMBOLS) {
    await loadHistory(symbol);
    await new Promise(r => setTimeout(r, 200));
  }
  console.log(`✅ Histórico carregado para ${SYMBOLS.length} símbolos\n`);
  
  const streams = SYMBOLS.map(s => `${s}@ticker`).join('/');
  const ws = new WebSocket(`wss://fstream.binance.com/stream?streams=${streams}`);
  
  ws.on('open', () => {
    console.log('🔌 WebSocket conectado!');
    console.log('🦞 Monitorando cruzamentos SMA 8/21 EM TEMPO REAL...\n');
  });
  
  ws.on('message', (data) => {
    try {
      const msg = JSON.parse(data);
      if (msg.data?.c && msg.stream) {
        const symbol = msg.stream.split('@')[0];
        const price = parseFloat(msg.data.c);
        const timestamp = new Date().toLocaleTimeString();
        
        // Detectar cruzamento ao vivo
        const cross = detectLiveCross(symbol, '1h', price, candles[symbol]);
        
        if (cross) {
          const arrow = cross.direction === 'BUY' ? '🟢 ▲ COMPRA' : '🔴 ▼ VENDA';
          console.log(`\n${'='.repeat(60)}`);
          console.log(`🚨 [${timestamp}] ${symbol.toUpperCase()} - ${arrow}`);
          console.log(`${'='.repeat(60)}`);
          console.log(`   Preço atual: $${price.toFixed(2)}`);
          console.log(`   SMA8: $${cross.sma8.toFixed(2)}`);
          console.log(`   SMA21: $${cross.sma21.toFixed(2)}`);
          console.log(`   📊 CRUZAMENTO DETECTADO EM TEMPO REAL!`);
          console.log(`${'='.repeat(60)}\n`);
          
          // Salvar sinal
          const count = saveSignal({
            symbol: symbol.toUpperCase(),
            timeframe: '1h',
            direction: cross.direction,
            price: price,
            detectedAt: timestamp
          });
          console.log(`💾 Sinal salvo! Total: ${count}\n`);
          
          // Alerta sonoro
          process.stdout.write('\x07');
        } else {
          // Mostrar status ao vivo
          const sma8 = candles[symbol]?.length > 0 ? '...' : '---';
          process.stdout.clearLine(0);
          process.stdout.cursorTo(0);
          process.stdout.write(`🦞 ${timestamp} | ${symbol.toUpperCase()} $${price.toFixed(2)} | monitorando cruzamento...`);
        }
      }
    } catch (err) {}
  });
  
  ws.on('error', (err) => {
    console.error('❌ Erro:', err.message);
  });
  
  ws.on('close', () => {
    console.log('\n⚠️ Desconectado. Reconectando em 5s...');
    setTimeout(connect, 5000);
  });
}

console.clear();
console.log('\n🦞 APEX IA - DETECTOR PRECISO');
console.log('🎯 Detecta cruzamento SMA 8/21 ANTES do candle fechar');
console.log('💡 Baseado no TradingView - seta no momento EXATO\n');

await connect();
