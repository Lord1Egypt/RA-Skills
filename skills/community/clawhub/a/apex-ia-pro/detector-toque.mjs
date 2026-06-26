#!/usr/bin/env node

import WebSocket from 'ws';
import axios from 'axios';
import fs from 'fs';
import path from 'path';

const SYMBOLS = ['bchusdt', 'btcusdt', 'ethusdt', 'solusdt', 'adausdt'];
const SIGNALS_FILE = path.join(process.env.HOME, 'apex-ia-skill', 'sinais.json');

let candles = {};
let lastAlert = {};

function calcSMA(data, length) {
  const sma = [];
  for (let i = length - 1; i < data.length; i++) {
    const sum = data.slice(i - length + 1, i + 1).reduce((a, b) => a + b, 0);
    sma.push(sum / length);
  }
  return sma;
}

// ============================================
// DETECTOR QUE CAPTURA "TOQUE" E "CRUZAMENTO"
// ============================================
function detectTouchOrCross(symbol, tf, price, history) {
  if (!history || history.length < 50) return null;
  
  const closes = history.map(c => c.close);
  const allCloses = [...closes, price];
  
  const sma8 = calcSMA(allCloses, 8);
  const sma21 = calcSMA(allCloses, 21);
  
  if (sma8.length < 3 || sma21.length < 3) return null;
  
  const curr8 = sma8[sma8.length - 1];
  const curr21 = sma21[sma21.length - 1];
  const prev8 = sma8[sma8.length - 2];
  const prev21 = sma21[sma21.length - 2];
  const prev2_8 = sma8[sma8.length - 3];
  const prev2_21 = sma21[sma21.length - 3];
  
  // 1. CRUZAMENTO REAL
  const crossingUp = prev8 <= prev21 && curr8 > curr21;
  const crossingDown = prev8 >= prev21 && curr8 < curr21;
  
  // 2. TOQUE (linhas se encostaram)
  const dist = Math.abs(curr8 - curr21);
  const prevDist = Math.abs(prev8 - prev21);
  const isTouching = dist < 0.05; // Diferença menor que 0.05%
  
  // 3. QUASE CRUZANDO (tendência de aproximação)
  const isApproaching = prevDist > dist && dist < 0.1;
  
  // Direção da tendência
  let direction = null;
  let signalType = null;
  
  if (crossingUp) {
    direction = 'BUY';
    signalType = 'CRUZAMENTO';
  } else if (crossingDown) {
    direction = 'SELL';
    signalType = 'CRUZAMENTO';
  } else if (isTouching && curr8 > curr21) {
    direction = 'BUY';
    signalType = 'TOQUE (encostou para cima)';
  } else if (isTouching && curr8 < curr21) {
    direction = 'SELL';
    signalType = 'TOQUE (encostou para baixo)';
  } else if (isApproaching && curr8 > curr21) {
    direction = 'BUY';
    signalType = 'APROXIMANDO (pré-cruzamento)';
  } else if (isApproaching && curr8 < curr21) {
    direction = 'SELL';
    signalType = 'APROXIMANDO (pré-cruzamento)';
  }
  
  if (!direction) return null;
  
  return {
    direction,
    signalType,
    price,
    sma8: curr8,
    sma21: curr21,
    distance: dist,
    timestamp: Date.now()
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
    symbol: signal.symbol,
    timeframe: signal.timeframe,
    direction: signal.direction,
    signalType: signal.signalType,
    price: signal.price,
    sma8: signal.sma8,
    sma21: signal.sma21,
    status: 'ativo'
  });
  
  fs.writeFileSync(SIGNALS_FILE, JSON.stringify(signals, null, 2));
  return signals.length;
}

async function loadHistory(symbol) {
  try {
    const res = await axios.get(`https://api.binance.com/api/v3/klines`, {
      params: { symbol: symbol.toUpperCase(), interval: '15m', limit: 100 }
    });
    candles[symbol] = res.data.map(k => ({
      close: parseFloat(k[4]),
      time: k[0]
    }));
  } catch (err) {}
}

async function connect() {
  for (const symbol of SYMBOLS) {
    await loadHistory(symbol);
    await new Promise(r => setTimeout(r, 200));
  }
  console.log(`✅ Histórico 15m carregado para ${SYMBOLS.length} símbolos\n`);
  
  const streams = SYMBOLS.map(s => `${s}@ticker`).join('/');
  const ws = new WebSocket(`wss://fstream.binance.com/stream?streams=${streams}`);
  
  ws.on('open', () => {
    console.log('🔌 WebSocket conectado!');
    console.log('🦞 Detectando: CRUZAMENTOS + TOQUES + APROXIMAÇÕES SMA 8/21\n');
  });
  
  ws.on('message', (data) => {
    try {
      const msg = JSON.parse(data);
      if (msg.data?.c && msg.stream) {
        const symbol = msg.stream.split('@')[0];
        const price = parseFloat(msg.data.c);
        const timestamp = new Date().toLocaleTimeString();
        
        const signal = detectTouchOrCross(symbol, '15m', price, candles[symbol]);
        
        if (signal) {
          const alertKey = `${symbol}_${signal.direction}`;
          const now = Date.now();
          if (lastAlert[alertKey] && now - lastAlert[alertKey] < 300000) return;
          lastAlert[alertKey] = now;
          
          const arrow = signal.direction === 'BUY' ? '🟢 ▲ COMPRA' : '🔴 ▼ VENDA';
          const typeEmoji = signal.signalType === 'CRUZAMENTO' ? '⚡' : (signal.signalType === 'TOQUE' ? '🎯' : '📈');
          
          console.log(`\n${'='.repeat(65)}`);
          console.log(`🚨 [${timestamp}] ${symbol.toUpperCase()} - ${arrow} ${typeEmoji}`);
          console.log(`${'='.repeat(65)}`);
          console.log(`   📊 SINAL: ${signal.signalType}`);
          console.log(`   💰 Preço: $${price.toFixed(2)}`);
          console.log(`   📈 SMA8: $${signal.sma8.toFixed(2)}`);
          console.log(`   📉 SMA21: $${signal.sma21.toFixed(2)}`);
          console.log(`   📏 Distância: ${signal.distance.toFixed(4)}%`);
          console.log(`${'='.repeat(65)}\n`);
          
          const count = saveSignal({
            symbol: symbol.toUpperCase(),
            timeframe: '15m',
            direction: signal.direction,
            signalType: signal.signalType,
            price: price,
            sma8: signal.sma8,
            sma21: signal.sma21
          });
          
          console.log(`💾 Sinal salvo! Total: ${count}`);
          process.stdout.write('\x07');
        } else {
          // Status ao vivo com distância entre SMAs
          const hist = candles[symbol];
          if (hist && hist.length > 0) {
            const closes = hist.map(c => c.close);
            const allCloses = [...closes, price];
            const sma8 = calcSMA(allCloses, 8);
            const sma21 = calcSMA(allCloses, 21);
            if (sma8.length > 0 && sma21.length > 0) {
              const curr8 = sma8[sma8.length - 1];
              const curr21 = sma21[sma21.length - 1];
              const dist = Math.abs(curr8 - curr21);
              const trend = curr8 > curr21 ? '📈' : '📉';
              process.stdout.clearLine(0);
              process.stdout.cursorTo(0);
              process.stdout.write(`${trend} ${timestamp} | ${symbol.toUpperCase()} $${price.toFixed(2)} | SMA8/21 dist: ${dist.toFixed(4)} | ${curr8 > curr21 ? '8 acima' : '21 acima'}`);
            }
          }
        }
      }
    } catch (err) {}
  });
  
  ws.on('close', () => {
    console.log('\n⚠️ Desconectado. Reconectando em 5s...');
    setTimeout(connect, 5000);
  });
}

console.clear();
console.log('\n🦞 APEX IA - DETECTOR DE TOQUE E CRUZAMENTO');
console.log('🎯 Detecta: Cruzamento REAL + TOQUE + APROXIMAÇÃO');
console.log('📊 Timeframe: 15 minutos (igual sua imagem)\n');

await connect();
