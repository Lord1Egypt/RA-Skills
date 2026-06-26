#!/usr/bin/env node

import WebSocket from 'ws';
import axios from 'axios';
import fs from 'fs';
import path from 'path';
import readline from 'readline';

// ============================================
// CONFIGURAÇÕES
// ============================================
const SMA_FAST = 8;
const SMA_SLOW = 21;
const TIMEFRAMES = ['5m', '15m', '30m', '1h', '4h'];
const SYMBOLS = ['btcusdt', 'ethusdt', 'bchusdt', 'solusdt', 'adausdt', 'ltcusdt', 'linkusdt', 'xrpusdt', 'dogeusdt', 'avaxusdt'];
const SIGNALS_FILE = path.join(process.env.HOME, 'apex-ia-skill', 'sinais.json');

// Estado
let candles = {};
let lastAlert = {};
let lastPrices = {};
let currentSignals = [];
let topSetups = [];
let currentView = 'main'; // main, scanner, signals, stats
let scanResults = [];

// UI
let lastStatusTime = 0;
let spinnerFrames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
let spinnerIndex = 0;
let ws = null;
let autoScanInterval = null;
let lastScanTime = 0;

// ============================================
// FUNÇÕES DE CÁLCULO
// ============================================
function calculateSMA(data, period) {
    const result = [];
    for (let i = period - 1; i < data.length; i++) {
        const sum = data.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
        result.push(sum / period);
    }
    return result;
}

function analyzePair(symbol, timeframe, candles) {
    if (!candles || candles.length < 50) return null;
    
    const closes = candles.map(c => c.close);
    const smaFast = calculateSMA(closes, SMA_FAST);
    const smaSlow = calculateSMA(closes, SMA_SLOW);
    
    if (smaFast.length < 2 || smaSlow.length < 2) return null;
    
    const currFast = smaFast[smaFast.length - 1];
    const currSlow = smaSlow[smaSlow.length - 1];
    const prevFast = smaFast[smaFast.length - 2];
    const prevSlow = smaSlow[smaSlow.length - 2];
    const prev2Fast = smaFast[smaFast.length - 3];
    const prev2Slow = smaSlow[smaSlow.length - 3];
    
    const diffPercent = Math.abs((currFast - currSlow) / currSlow) * 100;
    const prevDiff = Math.abs((prevFast - prevSlow) / prevSlow) * 100;
    
    // Tendência
    const trend = currFast > currSlow ? 'bullish' : 'bearish';
    const trendStrength = Math.abs((currFast - currSlow) / currSlow) * 100;
    
    // Detecta se está se aproximando
    const isApproaching = prevDiff > diffPercent && diffPercent < 0.5;
    
    // Detecta toque
    const isTouching = diffPercent < 0.05;
    
    // Detecta cruzamento recente
    const isRecentCross = (prevFast <= prevSlow && currFast > currSlow) || 
                          (prevFast >= prevSlow && currFast < currSlow);
    
    // Score de oportunidade (0-100)
    let score = 0;
    let signalType = null;
    let direction = null;
    
    if (isRecentCross) {
        score = 100;
        signalType = '⚡ CRUZAMENTO';
        direction = currFast > currSlow ? 'BUY' : 'SELL';
    } else if (isTouching) {
        score = 90;
        signalType = '🎯 TOQUE';
        direction = currFast > currSlow ? 'BUY' : 'SELL';
    } else if (isApproaching) {
        score = 70 - diffPercent * 100;
        signalType = '📈 APROXIMANDO';
        direction = currFast > currSlow ? 'BUY' : 'SELL';
    }
    
    if (score > 0) {
        return {
            symbol: symbol.toUpperCase(),
            timeframe,
            direction,
            signalType,
            score: Math.min(100, Math.max(0, score)),
            diffPercent,
            trend,
            trendStrength,
            price: closes[closes.length - 1],
            smaFast: currFast,
            smaSlow: currSlow
        };
    }
    
    return null;
}

async function scanAllTimeframes() {
    console.log(`\n🔍 Escaneando ${SYMBOLS.length} pares x ${TIMEFRAMES.length} timeframes...`);
    const results = [];
    
    for (const symbol of SYMBOLS) {
        for (const tf of TIMEFRAMES) {
            try {
                const cacheKey = `${symbol}_${tf}`;
                let histCandles = candles[cacheKey];
                
                if (!histCandles || histCandles.length < 50) {
                    const response = await axios.get(`https://api.binance.com/api/v3/klines`, {
                        params: { symbol: symbol.toUpperCase(), interval: tf, limit: 100 }
                    });
                    histCandles = response.data.map(k => ({ close: parseFloat(k[4]) }));
                    candles[cacheKey] = histCandles;
                    await new Promise(r => setTimeout(r, 50));
                }
                
                const analysis = analyzePair(symbol, tf, histCandles);
                if (analysis) {
                    results.push(analysis);
                }
            } catch (err) {}
        }
    }
    
    // Ordenar por score
    results.sort((a, b) => b.score - a.score);
    scanResults = results;
    lastScanTime = Date.now();
    
    return results;
}

function saveSignal(signalData) {
    let signals = [];
    if (fs.existsSync(SIGNALS_FILE)) {
        signals = JSON.parse(fs.readFileSync(SIGNALS_FILE, 'utf-8'));
    }
    
    const newSignal = {
        id: Date.now(),
        timestamp: new Date().toISOString(),
        date: new Date().toLocaleDateString('pt-BR'),
        time: new Date().toLocaleTimeString('pt-BR'),
        symbol: signalData.symbol,
        timeframe: signalData.timeframe,
        direction: signalData.direction,
        signalType: signalData.signalType,
        price: signalData.price,
        score: signalData.score,
        status: 'ativo'
    };
    
    signals.push(newSignal);
    fs.writeFileSync(SIGNALS_FILE, JSON.stringify(signals, null, 2));
    currentSignals = signals;
    return newSignal;
}

async function checkActivePositions() {
    if (!fs.existsSync(SIGNALS_FILE)) return [];
    
    const signals = JSON.parse(fs.readFileSync(SIGNALS_FILE, 'utf-8'));
    const activeSignals = signals.filter(s => s.status === 'ativo');
    let updated = false;
    
    for (const signal of activeSignals) {
        try {
            const response = await axios.get(`https://api.binance.com/api/v3/ticker/price?symbol=${signal.symbol}`);
            const currentPrice = parseFloat(response.data.price);
            const entryPrice = signal.price;
            
            const target1 = entryPrice * 1.015;
            const stopLoss = entryPrice * 0.99;
            
            if (currentPrice >= target1) {
                signal.status = 'fechado_lucro';
                signal.result = '✅ TARGET1';
                signal.finalProfit = 1.5;
                signal.closePrice = currentPrice;
                signal.closedAt = new Date().toISOString();
                updated = true;
            } else if (currentPrice <= stopLoss) {
                signal.status = 'fechado_prejuizo';
                signal.result = '❌ STOP';
                signal.finalProfit = -1.0;
                signal.closePrice = currentPrice;
                signal.closedAt = new Date().toISOString();
                updated = true;
            }
        } catch (err) {}
    }
    
    if (updated) {
        fs.writeFileSync(SIGNALS_FILE, JSON.stringify(signals, null, 2));
        currentSignals = signals;
    }
    
    return signals;
}

// ============================================
// UI - TELA PRINCIPAL
// ============================================
function drawUI() {
    console.clear();
    const now = new Date();
    
    // Header
    console.log('\x1b[36m╔════════════════════════════════════════════════════════════════════════════════╗\x1b[0m');
    console.log('\x1b[36m║\x1b[0m                    🦞 \x1b[33mAPEX IA - TRADING SOFTWARE\x1b[0m v2.0                                  \x1b[36m║\x1b[0m');
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log(`\x1b[36m║\x1b[0m  📅 ${now.toLocaleDateString('pt-BR')} | ${now.toLocaleTimeString('pt-BR')}                                                    \x1b[36m║\x1b[0m`);
    console.log(`\x1b[36m║\x1b[0m  🎯 Status: \x1b[32mATIVO\x1b[0m | Scanner: ${SYMBOLS.length} pares x ${TIMEFRAMES.length} TFs                          \x1b[36m║\x1b[0m`);
    
    if (currentView === 'scanner') {
        drawScannerView();
    } else if (currentView === 'signals') {
        drawSignalsView();
    } else if (currentView === 'stats') {
        drawStatsView();
    } else {
        drawMainView();
    }
    
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log('\x1b[36m║\x1b[0m  \x1b[33m💡 Comandos:\x1b[0m [1] Main | [2] Scanner | [3] Sinais | [4] Stats | [Q] Sair          \x1b[36m║\x1b[0m');
    console.log('\x1b[36m╚════════════════════════════════════════════════════════════════════════════════╝\x1b[0m');
}

function drawMainView() {
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log('\x1b[36m║\x1b[0m  \x1b[33m📈 PREÇOS EM TEMPO REAL\x1b[0m                                                         \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m                                                                        \x1b[36m║\x1b[0m');
    
    const symbolsList = ['BTCUSDT', 'ETHUSDT', 'BCHUSDT', 'SOLUSDT', 'ADAUSDT'];
    for (const symbol of symbolsList) {
        const price = lastPrices[symbol.toLowerCase()];
        if (price) {
            const priceStr = `$${price.toFixed(2)}`.padStart(12);
            console.log(`\x1b[36m║\x1b[0m    ${symbol.padEnd(8)} ${priceStr.padStart(12)}                                                    \x1b[36m║\x1b[0m`);
        }
    }
    
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log('\x1b[36m║\x1b[0m  \x1b[33m🏆 TOP SETUPS (Melhores oportunidades)\x1b[0m                                              \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m                                                                        \x1b[36m║\x1b[0m');
    
    const top3 = scanResults.slice(0, 3);
    if (top3.length === 0) {
        console.log(`\x1b[36m║\x1b[0m    Aguardando escaneamento... Pressione [2] para forçar                 \x1b[36m║\x1b[0m`);
    } else {
        for (const s of top3) {
            const arrow = s.direction === 'BUY' ? '🟢 ▲' : '🔴 ▼';
            const scoreBar = '█'.repeat(Math.floor(s.score / 10));
            console.log(`\x1b[36m║\x1b[0m    ${arrow} ${s.symbol.padEnd(8)} ${s.timeframe.padEnd(5)} | ${s.signalType.padEnd(12)} | Score: ${s.score}% ${scoreBar} \x1b[36m║\x1b[0m`);
        }
    }
    
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log('\x1b[36m║\x1b[0m  📊 ÚLTIMOS SINAIS                                                          \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m                                                                        \x1b[36m║\x1b[0m');
    
    const lastSignals = currentSignals.slice(-3).reverse();
    if (lastSignals.length === 0) {
        console.log(`\x1b[36m║\x1b[0m    Nenhum sinal ainda. Aguardando...                                   \x1b[36m║\x1b[0m`);
    } else {
        for (const s of lastSignals) {
            const statusIcon = s.status === 'fechado_lucro' ? '✅' : (s.status === 'fechado_prejuizo' ? '❌' : '⏳');
            const profit = s.finalProfit ? `${s.finalProfit > 0 ? '+' : ''}${s.finalProfit.toFixed(1)}%` : '---';
            console.log(`\x1b[36m║\x1b[0m    ${statusIcon} ${s.symbol.padEnd(8)} ${s.time} | ${s.signalType?.padEnd(12) || '---'} | ${profit.padStart(6)}        \x1b[36m║\x1b[0m`);
        }
    }
}

function drawScannerView() {
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log('\x1b[36m║\x1b[0m  \x1b[33m🔍 SCANNER AUTOMÁTICO - TODOS OS PARES E TIMEFRAMES\x1b[0m                                  \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m                                                                        \x1b[36m║\x1b[0m');
    
    if (scanResults.length === 0) {
        console.log(`\x1b[36m║\x1b[0m    Aguardando escaneamento...                                          \x1b[36m║\x1b[0m`);
    } else {
        console.log(`\x1b[36m║\x1b[0m    Total de setups encontrados: ${scanResults.length}                                          \x1b[36m║\x1b[0m`);
        console.log(`\x1b[36m║\x1b[0m    Último scan: ${new Date(lastScanTime).toLocaleTimeString('pt-BR')}                                            \x1b[36m║\x1b[0m`);
        console.log('\x1b[36m║\x1b[0m                                                                        \x1b[36m║\x1b[0m');
        
        for (let i = 0; i < Math.min(scanResults.length, 10); i++) {
            const s = scanResults[i];
            const arrow = s.direction === 'BUY' ? '🟢 ▲' : '🔴 ▼';
            const scoreBar = '█'.repeat(Math.floor(s.score / 10));
            console.log(`\x1b[36m║\x1b[0m    ${(i+1).toString().padStart(2)}. ${arrow} ${s.symbol.padEnd(8)} ${s.timeframe.padEnd(5)} | ${s.signalType.padEnd(12)} | Score: ${Math.floor(s.score)}% ${scoreBar}\x1b[36m║\x1b[0m`);
        }
    }
}

function drawSignalsView() {
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log('\x1b[36m║\x1b[0m  \x1b[33m📋 HISTÓRICO DE SINAIS\x1b[0m                                                           \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m                                                                        \x1b[36m║\x1b[0m');
    
    const last20 = currentSignals.slice(-20).reverse();
    if (last20.length === 0) {
        console.log(`\x1b[36m║\x1b[0m    Nenhum sinal registrado ainda.                                        \x1b[36m║\x1b[0m`);
    } else {
        for (const s of last20.slice(0, 15)) {
            const statusIcon = s.status === 'fechado_lucro' ? '✅' : (s.status === 'fechado_prejuizo' ? '❌' : '⏳');
            const profit = s.finalProfit ? `${s.finalProfit > 0 ? '+' : ''}${s.finalProfit.toFixed(1)}%` : '---';
            console.log(`\x1b[36m║\x1b[0m    ${statusIcon} ${s.symbol.padEnd(8)} ${s.timeframe?.padEnd(5) || '15m'} | ${s.date} ${s.time} | ${profit.padStart(6)}        \x1b[36m║\x1b[0m`);
        }
    }
}

function drawStatsView() {
    const closedSignals = currentSignals.filter(s => s.status === 'fechado_lucro' || s.status === 'fechado_prejuizo');
    const profitSignals = currentSignals.filter(s => s.status === 'fechado_lucro');
    const lossSignals = currentSignals.filter(s => s.status === 'fechado_prejuizo');
    const activeSignals = currentSignals.filter(s => s.status === 'ativo');
    
    const totalClosed = closedSignals.length;
    const winRate = totalClosed > 0 ? (profitSignals.length / totalClosed) * 100 : 0;
    const totalProfit = closedSignals.reduce((sum, s) => sum + (s.finalProfit || 0), 0);
    
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log('\x1b[36m║\x1b[0m  \x1b[33m📈 ESTATÍSTICAS DO SISTEMA\x1b[0m                                                    \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m                                                                        \x1b[36m║\x1b[0m');
    console.log(`\x1b[36m║\x1b[0m    📊 Total de sinais: ${currentSignals.length}                                                 \x1b[36m║\x1b[0m`);
    console.log(`\x1b[36m║\x1b[0m    ✅ Sinais com lucro: ${profitSignals.length}                                                   \x1b[36m║\x1b[0m`);
    console.log(`\x1b[36m║\x1b[0m    ❌ Sinais com prejuízo: ${lossSignals.length}                                                 \x1b[36m║\x1b[0m`);
    console.log(`\x1b[36m║\x1b[0m    ⏳ Posições ativas: ${activeSignals.length}                                                   \x1b[36m║\x1b[0m`);
    console.log(`\x1b[36m║\x1b[0m    🎯 Taxa de acerto: ${winRate.toFixed(1)}%                                                      \x1b[36m║\x1b[0m`);
    console.log(`\x1b[36m║\x1b[0m    💰 Lucro total: ${totalProfit > 0 ? '+' : ''}${totalProfit.toFixed(2)}%                                                      \x1b[36m║\x1b[0m`);
    
    if (scanResults.length > 0) {
        console.log('\x1b[36m║\x1b[0m                                                                        \x1b[36m║\x1b[0m');
        console.log(`\x1b[36m║\x1b[0m    🔍 Melhor setup agora: ${scanResults[0]?.symbol} ${scanResults[0]?.timeframe} (Score: ${Math.floor(scanResults[0]?.score || 0)}%)          \x1b[36m║\x1b[0m`);
    }
}

// ============================================
// CARREGAR HISTÓRICO INICIAL
// ============================================
async function loadInitialHistory() {
    console.log(`📊 Carregando histórico inicial para ${SYMBOLS.length} símbolos x ${TIMEFRAMES.length} TFs...`);
    let loaded = 0;
    for (const symbol of SYMBOLS) {
        for (const tf of TIMEFRAMES) {
            const cacheKey = `${symbol}_${tf}`;
            try {
                const response = await axios.get(`https://api.binance.com/api/v3/klines`, {
                    params: { symbol: symbol.toUpperCase(), interval: tf, limit: 100 }
                });
                candles[cacheKey] = response.data.map(k => ({ close: parseFloat(k[4]) }));
                loaded++;
                await new Promise(r => setTimeout(r, 50));
            } catch (err) {}
        }
    }
    console.log(`✅ Histórico carregado: ${loaded} combinações\n`);
}

// ============================================
// CONECTAR WEBSOCKET
// ============================================
function connectWebSocket() {
    if (ws) ws.close();
    
    const streams = SYMBOLS.map(s => `${s}@ticker`).join('/');
    ws = new WebSocket(`wss://fstream.binance.com/stream?streams=${streams}`);
    
    ws.on('message', async (data) => {
        try {
            const msg = JSON.parse(data);
            if (msg.data?.c && msg.stream) {
                const symbol = msg.stream.split('@')[0];
                const price = parseFloat(msg.data.c);
                lastPrices[symbol] = price;
            }
        } catch (err) {}
    });
    
    ws.on('close', () => {
        setTimeout(connectWebSocket, 5000);
    });
}

// ============================================
// AUTO SCAN PERIÓDICO
// ============================================
function startAutoScan() {
    autoScanInterval = setInterval(async () => {
        const results = await scanAllTimeframes();
        if (results.length > 0) {
            // Verificar se algum setup é novo e tem score alto
            for (const setup of results.slice(0, 5)) {
                if (setup.score >= 85) {
                    const alertKey = `${setup.symbol}_${setup.timeframe}`;
                    if (!lastAlert[alertKey] || Date.now() - lastAlert[alertKey] > 300000) {
                        lastAlert[alertKey] = Date.now();
                        const newSignal = saveSignal(setup);
                        console.log(`\x07`);
                        console.log(`\n\x1b[32m🚨 NOVO SINAL! ${setup.symbol} ${setup.timeframe} - ${setup.direction === 'BUY' ? 'COMPRA' : 'VENDA'} (${setup.signalType}) Score: ${setup.score}%\x1b[0m\n`);
                        setTimeout(() => drawUI(), 1000);
                    }
                }
            }
        }
        drawUI();
    }, 60000); // A cada 1 minuto
    
    // Primeiro scan imediato
    setTimeout(async () => {
        await scanAllTimeframes();
        drawUI();
    }, 2000);
}

// ============================================
// INICIAR SOFTWARE
// ============================================
async function init() {
    await loadInitialHistory();
    await checkActivePositions();
    connectWebSocket();
    startAutoScan();
}

// ============================================
// INPUT DO USUÁRIO
// ============================================
readline.emitKeypressEvents(process.stdin);
process.stdin.setRawMode(true);
process.stdin.on('keypress', (str, key) => {
    if (key.ctrl && key.name === 'c') {
        console.log('\n\n👋 Encerrando APEX IA...\n');
        if (ws) ws.close();
        if (autoScanInterval) clearInterval(autoScanInterval);
        process.exit();
    } else if (key.name === 'q') {
        console.log('\n\n👋 Encerrando APEX IA...\n');
        if (ws) ws.close();
        if (autoScanInterval) clearInterval(autoScanInterval);
        process.exit();
    } else if (key.name === '1') {
        currentView = 'main';
        drawUI();
    } else if (key.name === '2') {
        currentView = 'scanner';
        scanAllTimeframes().then(() => drawUI());
    } else if (key.name === '3') {
        currentView = 'signals';
        drawUI();
    } else if (key.name === '4') {
        currentView = 'stats';
        drawUI();
    }
});

console.clear();
console.log('\x1b[36m════════════════════════════════════════════════════════════════════════════════╗\x1b[0m');
console.log('\x1b[36m                    🦞 APEX IA - INICIANDO SCANNER INTELIGENTE...\x1b[0m                    ');
console.log('\x1b[36m════════════════════════════════════════════════════════════════════════════════╝\x1b[0m\n');

await init();
drawUI();
