#!/usr/bin/env node

import WebSocket from 'ws';
import axios from 'axios';
import './dist/index.js';

// Configurações
const SYMBOLS = ['btcusdt', 'ethusdt', 'bchusdt', 'solusdt', 'adausdt', 'ltcusdt', 'linkusdt', 'etcusdt', 'trxusdt', 'zecusdt'];
const TIMEFRAMES = ['1m', '5m', '15m', '1h', '4h'];
let lastSignal = {};

// Cache de candles por símbolo/timeframe
const candleCache = {};

// Inicializar cache com dados históricos
async function initCache() {
  console.log('📦 Carregando dados históricos...');
  for (const symbol of SYMBOLS) {
    for (const tf of TIMEFRAMES) {
      const key = `${symbol}_${tf}`;
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
    }
  }
  console.log('✅ Cache inicializado');
}

// Atualizar candle com dado do WebSocket
function updateCandle(symbol, tf, candleData) {
  const key = `${symbol}_${tf}`;
  if (!candleCache[key]) candleCache[key] = [];
  
  const lastCandle = candleCache[key][candleCache[key].length - 1];
  
  // Se é um novo candle
  if (!lastCandle || lastCandle.openTime !== candleData.openTime) {
    candleCache[key].push(candleData);
    if (candleCache[key].length > 100) candleCache[key].shift();
    console.log(`🕯️ Novo candle ${symbol} ${tf} às ${new Date(candleData.openTime).toLocaleTimeString()}`);
    return true; // Novo candle
  }
  
  // Atualizar candle existente
  lastCandle.close = candleData.close;
  lastCandle.high = Math.max(lastCandle.high, candleData.high);
  lastCandle.low = Math.min(lastCandle.low, candleData.low);
  lastCandle.volume = candleData.volume;
  
  return false; // Atualização
}

// Verificar sinais
async function checkSignals(symbol, tf, isNewCandle) {
  const key = `${symbol}_${tf}`;
  const candles = candleCache[key];
  if (!candles || candles.length < 50) return;
  
  // Importar as funções do scanner
  const { calculateFinalSignal } = await import('./dist/scanner.js');
  const signal = calculateFinalSignal(symbol.toUpperCase(), tf, candles);
  
  if (signal && signal.score >= 7) {
    const signalKey = `${symbol}_${tf}_${signal.direction}`;
    const now = Date.now();
    
    // Evitar alertas duplicados no mesmo candle
    if (lastSignal[signalKey] && (now - lastSignal[signalKey] < 60000)) return;
    
    lastSignal[signalKey] = now;
    
    const arrow = signal.direction === 'BUY' ? '🟢 COMPRA ▲' : '🔴 VENDA ▼';
    console.log(`\n🚨 [${new Date().toLocaleString()}] ${symbol.toUpperCase()} ${tf} - ${arrow}`);
    console.log(`   Score: ${signal.score}/10 | PivotFlow: ${signal.pivotTrendFlow} | SMA: ${signal.smaCross} | SuperTrend: ${signal.superTrend}`);
    console.log(`   🎯 T1: ${signal.targets.t1.toFixed(4)} | Stop: ${signal.stop.toFixed(4)}`);
    
    // ⭐ AQUI VOCÊ PODE ADICIONAR EXECUÇÃO AUTOMÁTICA ⭐
    // if (signal.score >= 8 && signal.smaCross && signal.superTrend) {
    //   await executeOrder(signal);
    // }
  }
}

// Conectar WebSocket
function connectWebSocket() {
  const streams = [];
  for (const symbol of SYMBOLS) {
    for (const tf of TIMEFRAMES) {
      streams.push(`${symbol}@kline_${tf}`);
    }
  }
  
  const wsUrl = `wss://fstream.binance.com/stream?streams=${streams.join('/')}`;
  const ws = new WebSocket(wsUrl);
  
  ws.on('open', () => {
    console.log('🔌 WebSocket conectado!');
    console.log(`📡 Monitorando ${SYMBOLS.length} símbolos x ${TIMEFRAMES.length} timeframes`);
  });
  
  ws.on('message', async (data) => {
    const msg = JSON.parse(data);
    if (msg.data?.k) {
      const k = msg.data.k;
      const symbol = msg.data.s.toLowerCase();
      const tf = k.i;
      const isNewCandle = k.x; // Verdadeiro quando o candle fecha
      
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
      
      // Verificar sinal quando o candle fecha (x=true) ou a cada atualização
      if (isNewCandle) {
        await checkSignals(symbol, tf, true);
      }
    }
  });
  
  ws.on('error', (err) => {
    console.error('❌ WebSocket erro:', err.message);
  });
  
  ws.on('close', () => {
    console.log('⚠️ WebSocket desconectado. Reconectando em 5 segundos...');
    setTimeout(connectWebSocket, 5000);
  });
  
  return ws;
}

// Instalar dependência se necessário
try {
  await import('ws');
} catch {
  console.log('📦 Instalando ws...');
  const { execSync } = await import('child_process');
  execSync('npm install ws', { stdio: 'inherit' });
}

// Iniciar
console.log('🦞 APEX IA - REAL TIME SCANNER');
console.log('🎯 Detectando cruzamentos EM TEMPO REAL igual ao TradingView\n');

await initCache();
connectWebSocket();

// Keep alive
process.on('SIGINT', () => {
  console.log('\n👋 Desligando...');
  process.exit();
});
