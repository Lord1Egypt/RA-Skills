#!/usr/bin/env node

import WebSocket from 'ws';
import axios from 'axios';
import fs from 'fs';
import path from 'path';

// ============================================
// PARÂMETROS IGUAIS AO TRADINGVIEW
// ============================================
const SMA_FAST = 8;
const SMA_SLOW = 21;
const TIMEFRAME = '15m';
const DISTANCE_THRESHOLD = 0.05;

const SYMBOLS = ['bchusdt', 'btcusdt', 'ethusdt', 'solusdt', 'adausdt', 'ltcusdt', 'linkusdt'];
const SIGNALS_FILE = path.join(process.env.HOME, 'apex-ia-skill', 'sinais.json');

let candles = {};
let lastAlert = {};
let lastPrices = {};

// Spinner para animação
const spinnerFrames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
let spinnerIndex = 0;
let lastStatusTime = 0;

function calculateSMA(data, period) {
    const result = [];
    for (let i = period - 1; i < data.length; i++) {
        const sum = data.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
        result.push(sum / period);
    }
    return result;
}

function detectSignal(symbol, currentPrice, history) {
    if (!history || history.length < 50) return null;
    
    const closes = history.map(c => c.close);
    const allCloses = [...closes, currentPrice];
    
    const smaFast = calculateSMA(allCloses, SMA_FAST);
    const smaSlow = calculateSMA(allCloses, SMA_SLOW);
    
    if (smaFast.length < 2 || smaSlow.length < 2) return null;
    
    const currFast = smaFast[smaFast.length - 1];
    const currSlow = smaSlow[smaSlow.length - 1];
    const prevFast = smaFast[smaFast.length - 2];
    const prevSlow = smaSlow[smaSlow.length - 2];
    
    const diffPercent = Math.abs((currFast - currSlow) / currSlow) * 100;
    
    const isCrossingUp = prevFast <= prevSlow && currFast > currSlow;
    const isCrossingDown = prevFast >= prevSlow && currFast < currSlow;
    const isTouchingUp = !isCrossingUp && currFast > currSlow && diffPercent < DISTANCE_THRESHOLD;
    const isTouchingDown = !isCrossingDown && currFast < currSlow && diffPercent < DISTANCE_THRESHOLD;
    
    let signal = null;
    let signalType = null;
    
    if (isCrossingUp) {
        signal = 'BUY';
        signalType = '⚡ CRUZAMENTO CONFIRMADO';
    } else if (isCrossingDown) {
        signal = 'SELL';
        signalType = '⚡ CRUZAMENTO CONFIRMADO';
    } else if (isTouchingUp) {
        signal = 'BUY';
        signalType = '🎯 TOQUE - IGUAL TRADINGVIEW';
    } else if (isTouchingDown) {
        signal = 'SELL';
        signalType = '🎯 TOQUE';
    }
    
    if (signal) {
        return {
            direction: signal,
            type: signalType,
            price: currentPrice,
            smaFast: currFast,
            smaSlow: currSlow,
            diffPercent: diffPercent,
            timestamp: Date.now()
        };
    }
    return null;
}

function saveSignal(signal) {
    let signals = [];
    if (fs.existsSync(SIGNALS_FILE)) {
        signals = JSON.parse(fs.readFileSync(SIGNALS_FILE, 'utf-8'));
    }
    
    signals.push({
        id: Date.now(),
        timestamp: new Date().toISOString(),
        date: new Date().toLocaleDateString(),
        time: new Date().toLocaleTimeString(),
        symbol: signal.symbol,
        timeframe: TIMEFRAME,
        direction: signal.direction,
        signalType: signal.type,
        price: signal.price,
        sma8: signal.smaFast,
        sma21: signal.smaSlow,
        diffPercent: signal.diffPercent,
        status: 'ativo'
    });
    
    fs.writeFileSync(SIGNALS_FILE, JSON.stringify(signals, null, 2));
    return signals.length;
}

async function loadHistory(symbol) {
    try {
        const response = await axios.get(`https://api.binance.com/api/v3/klines`, {
            params: { symbol: symbol.toUpperCase(), interval: TIMEFRAME, limit: 100 }
        });
        candles[symbol] = response.data.map(k => ({
            close: parseFloat(k[4]),
            time: k[0]
        }));
        return true;
    } catch (err) {
        return false;
    }
}

async function init() {
    console.log(`📊 Carregando histórico (${TIMEFRAME}) para ${SYMBOLS.length} símbolos...`);
    let loaded = 0;
    for (const symbol of SYMBOLS) {
        if (await loadHistory(symbol)) loaded++;
        await new Promise(r => setTimeout(r, 200));
    }
    console.log(`✅ ${loaded} símbolos carregados\n`);
}

function showStatus() {
    const now = Date.now();
    if (now - lastStatusTime < 1000) return;
    lastStatusTime = now;
    
    const spinner = spinnerFrames[spinnerIndex % spinnerFrames.length];
    spinnerIndex++;
    
    const currentDate = new Date().toLocaleString('pt-BR');
    
    // Contar símbolos com preço
    const activeCount = Object.keys(lastPrices).length;
    
    // Escolher um símbolo aleatório para mostrar
    const symbolsList = Object.keys(lastPrices);
    const randomSymbol = symbolsList.length > 0 ? symbolsList[Math.floor(Math.random() * symbolsList.length)].toUpperCase() : '---';
    const randomPrice = lastPrices[randomSymbol.toLowerCase()] ? `$${lastPrices[randomSymbol.toLowerCase()].toFixed(2)}` : '---';
    
    const line = `${spinner} 🟢 ATIVO | ${currentDate} | ${activeCount} ativos | ${randomSymbol} ${randomPrice} | SMA ${SMA_FAST}/${SMA_SLOW} ${TIMEFRAME}`;
    
    process.stdout.clearLine(0);
    process.stdout.cursorTo(0);
    process.stdout.write(line);
}

function connectWebSocket() {
    const streams = SYMBOLS.map(s => `${s}@ticker`).join('/');
    const ws = new WebSocket(`wss://fstream.binance.com/stream?streams=${streams}`);
    
    ws.on('open', () => {
        console.log('\n✅ WebSocket conectado!');
        console.log(`🦞 Monitorando SMA ${SMA_FAST}/${SMA_SLOW} em ${TIMEFRAME}`);
        console.log('🎯 Aguardando TOQUE ou CRUZAMENTO...\n');
    });
    
    ws.on('message', (data) => {
        try {
            const msg = JSON.parse(data);
            if (msg.data?.c && msg.stream) {
                const symbol = msg.stream.split('@')[0];
                const price = parseFloat(msg.data.c);
                lastPrices[symbol] = price;
                
                const signal = detectSignal(symbol, price, candles[symbol]);
                
                if (signal) {
                    const alertKey = `${symbol}_${signal.direction}`;
                    if (lastAlert[alertKey] && Date.now() - lastAlert[alertKey] < 300000) return;
                    lastAlert[alertKey] = Date.now();
                    
                    const arrow = signal.direction === 'BUY' ? '🟢 ▲ COMPRA' : '🔴 ▼ VENDA';
                    const now = new Date();
                    const dateTime = now.toLocaleString('pt-BR');
                    
                    // Pular linha para mostrar o alerta
                    process.stdout.write('\n');
                    console.log(`\n${'='.repeat(70)}`);
                    console.log(`🚨 [${dateTime}] ${symbol.toUpperCase()} - ${arrow}`);
                    console.log(`${'='.repeat(70)}`);
                    console.log(`   📊 ${signal.type}`);
                    console.log(`   💰 Preço: $${price.toFixed(4)}`);
                    console.log(`   📈 SMA${SMA_FAST}: $${signal.smaFast.toFixed(4)}`);
                    console.log(`   📉 SMA${SMA_SLOW}: $${signal.smaSlow.toFixed(4)}`);
                    console.log(`   📏 Diferença: ${signal.diffPercent.toFixed(4)}%`);
                    console.log(`${'='.repeat(70)}\n`);
                    
                    const count = saveSignal({
                        symbol: symbol.toUpperCase(),
                        direction: signal.direction,
                        type: signal.type,
                        price: price,
                        smaFast: signal.smaFast,
                        smaSlow: signal.smaSlow,
                        diffPercent: signal.diffPercent
                    });
                    
                    console.log(`💾 Sinal salvo! Total: ${count}`);
                    console.log(`📅 ${new Date().toLocaleString('pt-BR')}\n`);
                    process.stdout.write('\x07');
                }
            }
        } catch (err) {}
    });
    
    ws.on('close', () => {
        console.log('\n⚠️ WebSocket desconectado. Reconectando em 5s...');
        setTimeout(connectWebSocket, 5000);
    });
    
    ws.on('error', (err) => {
        console.error('\n❌ WebSocket erro:', err.message);
    });
}

// Atualizar status a cada 500ms
setInterval(() => {
    showStatus();
}, 500);

console.clear();
console.log('\n🦞 APEX IA - DETECTOR FINAL');
console.log(`🎯 SMA ${SMA_FAST}/${SMA_SLOW} - Timeframe ${TIMEFRAME}`);
console.log('💡 Detecta: CRUZAMENTO + TOQUE');
console.log('✅ Exatamente igual à sua configuração do TradingView\n');

await init();
connectWebSocket();

process.on('SIGINT', () => {
    console.log('\n\n📊 Estatísticas finais:');
    if (fs.existsSync(SIGNALS_FILE)) {
        const signals = JSON.parse(fs.readFileSync(SIGNALS_FILE, 'utf-8'));
        console.log(`   Total de sinais salvos: ${signals.length}`);
    }
    console.log('\n👋 Desligando...\n');
    process.exit();
});
