#!/usr/bin/env node

// ============================================
// VERSÃO AGRESSIVA - PARA OPERAÇÕES DE ALTO RISCO
// ============================================

import WebSocket from 'ws';
import axios from 'axios';
import readline from 'readline';
import crypto from 'crypto';

// SUAS CHAVES API
const API_KEY = 'Dq0vl5xeDxwQKMBwoJT5A9yxsJiW8hbXyVO7831c4xbI0N1tfiQjsTf1ZKsSVIXL';
const API_SECRET = '1kVF6XZuV5rVnKyIiAjbLTNcN50tQZEI8M5p90piOblTOl4W19rpgIeZMRzDlBBb';
const USE_DEMO = true;
const BASE_URL = USE_DEMO ? 'https://testnet.binancefuture.com' : 'https://fapi.binance.com';

// ============================================
// CONFIGURAÇÕES AGRESSIVAS (SEU ESTILO)
// ============================================
const FIXED_ENTRY_USD = 10;           // Entrada fixa de $10 por operação
let MAX_LEVERAGE = 20;                 // Alavancagem 20x
let TAKE_PROFIT_PERCENT = 50;          // Take profit em % (50% a 400%)
let USE_STOP_LOSS = false;              // SEM STOP LOSS (seu estilo)
let STOP_LOSS_PERCENT = 0;              // Sem stop loss

const SYMBOLS = ['btcusdt', 'ethusdt', 'bchusdt', 'solusdt', 'adausdt', 'dogeusdt', 'xrpusdt'];
const TIMEFRAMES = ['5m', '15m', '30m', '1h', '4h'];

let autoTrade = true;
let equity = 0;
let positions = [];
let trades = [];
let scanResults = [];
let candles = {};
let lastAlert = {};

// ============================================
// FUNÇÕES DA BINANCE
// ============================================
function generateSignature(queryString, secret) {
    return crypto.createHmac('sha256', secret).update(queryString).digest('hex');
}

async function binanceRequest(method, endpoint, params = {}, signed = false) {
    const timestamp = Date.now();
    let queryString = `timestamp=${timestamp}`;
    if (Object.keys(params).length > 0) {
        queryString += `&${new URLSearchParams(params).toString()}`;
    }
    let signature = '';
    if (signed) {
        signature = generateSignature(queryString, API_SECRET);
        queryString += `&signature=${signature}`;
    }
    const url = `${BASE_URL}${endpoint}?${queryString}`;
    try {
        const response = await axios({ method, url, headers: { 'X-MBX-APIKEY': API_KEY }, timeout: 10000 });
        return response.data;
    } catch (err) { return null; }
}

async function setLeverage(symbol, leverage) {
    const result = await binanceRequest('POST', '/fapi/v1/leverage', {
        symbol: symbol.toUpperCase(),
        leverage: leverage
    }, true);
    if (result) console.log(`   ✅ Alavancagem ${leverage}x configurada`);
    return result;
}

async function getBalance() {
    const data = await binanceRequest('GET', '/fapi/v2/account', {}, true);
    if (data && data.assets) {
        const usdtAsset = data.assets.find(a => a.asset === 'USDT');
        if (usdtAsset) { equity = parseFloat(usdtAsset.walletBalance); return equity; }
    }
    return equity;
}

async function getPrice(symbol) {
    try {
        const response = await axios.get(`${BASE_URL}/fapi/v1/ticker/price?symbol=${symbol.toUpperCase()}`, { timeout: 5000 });
        return parseFloat(response.data.price);
    } catch (err) { return null; }
}

async function openPosition(symbol, side, quantity, entryPrice) {
    console.log(`\n🔧 Abrindo posição ${side} em ${symbol}...`);
    console.log(`   Entrada fixa: $${FIXED_ENTRY_USD} | Alavancagem: ${MAX_LEVERAGE}x`);
    console.log(`   Quantidade: ${quantity.toFixed(6)} | Preço: $${entryPrice.toFixed(2)}`);
    
    const order = await binanceRequest('POST', '/fapi/v1/order', {
        symbol: symbol.toUpperCase(),
        side: side.toUpperCase(),
        type: 'MARKET',
        quantity: quantity,
        reduceOnly: 'false'
    }, true);
    
    if (order && order.orderId) {
        console.log(`   ✅ Ordem executada! ID: ${order.orderId}`);
        
        // SEM STOP LOSS (seu estilo)
        if (!USE_STOP_LOSS) {
            console.log(`   ⚠️ SEM STOP LOSS - risco total de perda`);
        }
        
        // Calcular take profit
        const targetPrice = side === 'BUY' 
            ? entryPrice * (1 + TAKE_PROFIT_PERCENT / 100)
            : entryPrice * (1 - TAKE_PROFIT_PERCENT / 100);
        
        console.log(`   🎯 Take Profit: ${TAKE_PROFIT_PERCENT}% → $${targetPrice.toFixed(2)}`);
        
        // Adicionar TAKE PROFIT
        const stopSide = side === 'BUY' ? 'SELL' : 'BUY';
        await binanceRequest('POST', '/fapi/v1/order', {
            symbol: symbol.toUpperCase(),
            side: stopSide,
            type: 'TAKE_PROFIT_MARKET',
            quantity: quantity,
            stopPrice: targetPrice.toFixed(2),
            reduceOnly: 'true'
        }, true);
        
        positions.push({
            symbol: symbol.toUpperCase(),
            side: side,
            quantity: quantity,
            entryPrice: entryPrice,
            targetPrice: targetPrice,
            leverage: MAX_LEVERAGE,
            targetPercent: TAKE_PROFIT_PERCENT,
            openedAt: new Date().toISOString()
        });
        
        const potentialProfit = quantity * Math.abs(targetPrice - entryPrice);
        console.log(`   💰 Lucro potencial: $${potentialProfit.toFixed(2)} (${TAKE_PROFIT_PERCENT}%)`);
        
        return order;
    }
    return null;
}

async function closePosition(symbol, reason) {
    const position = positions.find(p => p.symbol === symbol.toUpperCase());
    if (!position) return null;
    
    const currentPrice = await getPrice(symbol);
    if (!currentPrice) return null;
    
    const side = position.side === 'BUY' ? 'SELL' : 'BUY';
    const order = await binanceRequest('POST', '/fapi/v1/order', {
        symbol: symbol.toUpperCase(),
        side: side,
        type: 'MARKET',
        quantity: position.quantity,
        reduceOnly: 'true'
    }, true);
    
    if (order) {
        const profit = position.side === 'BUY' 
            ? (currentPrice - position.entryPrice) * position.quantity
            : (position.entryPrice - currentPrice) * position.quantity;
        
        const profitPercent = (profit / (position.entryPrice * position.quantity)) * 100;
        
        trades.push({
            symbol: symbol.toUpperCase(),
            side: position.side,
            entryPrice: position.entryPrice,
            exitPrice: currentPrice,
            quantity: position.quantity,
            profit: profit,
            profitPercent: profitPercent,
            leverage: position.leverage,
            reason: reason,
            closedAt: new Date().toISOString()
        });
        
        positions = positions.filter(p => p.symbol !== symbol.toUpperCase());
        console.log(`\n📊 ${reason}! ${symbol} | Lucro: ${profit >= 0 ? '+' : ''}$${profit.toFixed(2)} (${profitPercent.toFixed(2)}%)`);
        return { order, profit };
    }
    return null;
}

// ============================================
// SCANNER SMA 8/21
// ============================================
function calculateSMA(data, period) {
    const result = [];
    for (let i = period - 1; i < data.length; i++) {
        const sum = data.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
        result.push(sum / period);
    }
    return result;
}

async function scanAll() {
    const results = [];
    for (const symbol of SYMBOLS) {
        for (const tf of TIMEFRAMES) {
            try {
                const cacheKey = `${symbol}_${tf}`;
                if (!candles[cacheKey] || candles[cacheKey].length < 50) {
                    const response = await axios.get(`https://api.binance.com/api/v3/klines`, {
                        params: { symbol: symbol.toUpperCase(), interval: tf, limit: 100 }
                    });
                    candles[cacheKey] = response.data.map(k => ({ close: parseFloat(k[4]) }));
                    await new Promise(r => setTimeout(r, 50));
                }
                const closes = candles[cacheKey].map(c => c.close);
                const smaFast = calculateSMA(closes, 8);
                const smaSlow = calculateSMA(closes, 21);
                if (smaFast.length < 2 || smaSlow.length < 2) continue;
                
                const currFast = smaFast[smaFast.length - 1];
                const currSlow = smaSlow[smaSlow.length - 1];
                const prevFast = smaFast[smaFast.length - 2];
                const prevSlow = smaSlow[smaSlow.length - 2];
                const diffPercent = Math.abs((currFast - currSlow) / currSlow) * 100;
                const isCross = (prevFast <= prevSlow && currFast > currSlow) || (prevFast >= prevSlow && currFast < currSlow);
                const isTouch = diffPercent < 0.05;
                
                if (isCross || isTouch) {
                    const direction = currFast > currSlow ? 'BUY' : 'SELL';
                    const signalType = isCross ? 'CRUZAMENTO' : 'TOQUE';
                    const score = isCross ? 100 : 90;
                    results.push({
                        symbol: symbol.toUpperCase(),
                        timeframe: tf,
                        direction,
                        signalType,
                        score,
                        price: closes[closes.length - 1],
                        stop: closes[closes.length - 1] * 0.99,
                        target1: closes[closes.length - 1] * (1 + TAKE_PROFIT_PERCENT / 100)
                    });
                }
            } catch (err) {}
        }
    }
    results.sort((a, b) => b.score - a.score);
    scanResults = results;
    return results;
}

async function executeTrade(signal) {
    if (!autoTrade) return false;
    
    const currentPrice = await getPrice(signal.symbol);
    if (!currentPrice) return false;
    
    // Calcular quantidade baseada em ENTRADA FIXA de $10
    const positionSize = FIXED_ENTRY_USD * MAX_LEVERAGE;
    let quantity = positionSize / currentPrice;
    quantity = Math.min(quantity, 0.5); // Limite máximo de segurança
    
    console.log(`\n📊 EXECUTANDO TRADE (SEU ESTILO):`);
    console.log(`   Símbolo: ${signal.symbol}`);
    console.log(`   Direção: ${signal.direction === 'BUY' ? 'COMPRA' : 'VENDA'}`);
    console.log(`   Entrada fixa: $${FIXED_ENTRY_USD} | Alavancagem: ${MAX_LEVERAGE}x`);
    console.log(`   Posição total: $${(FIXED_ENTRY_USD * MAX_LEVERAGE).toFixed(2)}`);
    console.log(`   Quantidade: ${quantity.toFixed(6)}`);
    console.log(`   Preço: $${currentPrice.toFixed(2)}`);
    console.log(`   🎯 Target: ${TAKE_PROFIT_PERCENT}%`);
    console.log(`   🛑 Stop Loss: ${USE_STOP_LOSS ? STOP_LOSS_PERCENT + '%' : 'NENHUM (risco total)'}`);
    
    const targetPrice = signal.direction === 'BUY' 
        ? currentPrice * (1 + TAKE_PROFIT_PERCENT / 100)
        : currentPrice * (1 - TAKE_PROFIT_PERCENT / 100);
    
    const potentialProfit = quantity * Math.abs(targetPrice - currentPrice);
    console.log(`   💰 Lucro potencial: $${potentialProfit.toFixed(2)} (${TAKE_PROFIT_PERCENT}%)`);
    
    const order = await openPosition(signal.symbol, signal.direction, quantity, currentPrice);
    
    if (order) {
        console.log(`\n✅ TRADE EXECUTADO!`);
        return true;
    }
    return false;
}

// ============================================
// MONITORAMENTO DE TAKE PROFIT
// ============================================
async function monitorPositions() {
    for (const position of positions) {
        const currentPrice = await getPrice(position.symbol);
        if (!currentPrice) continue;
        
        // Verificar se atingiu o target
        if (position.side === 'BUY' && currentPrice >= position.targetPrice) {
            await closePosition(position.symbol, '🎯 TARGET ATINGIDO');
        } else if (position.side === 'SELL' && currentPrice <= position.targetPrice) {
            await closePosition(position.symbol, '🎯 TARGET ATINGIDO');
        }
    }
}

function connectWebSocket() {
    const streams = SYMBOLS.map(s => `${s}@ticker`).join('/');
    const ws = new WebSocket(`wss://fstream.binance.com/stream?streams=${streams}`);
    ws.on('message', (data) => {
        try {
            const msg = JSON.parse(data);
            if (msg.data?.c && msg.stream) {
                const symbol = msg.stream.split('@')[0];
            }
        } catch (err) {}
    });
    ws.on('close', () => setTimeout(connectWebSocket, 5000));
    return ws;
}

function drawUI() {
    console.clear();
    const now = new Date();
    console.log('╔══════════════════════════════════════════════════════════════════════════════╗');
    console.log('║              🦞 APEX IA - MODO AGRESSIVO (SEU ESTILO)                          ║');
    console.log('╠══════════════════════════════════════════════════════════════════════════════╣');
    console.log(`║  📅 ${now.toLocaleDateString('pt-BR')} | ${now.toLocaleTimeString('pt-BR')}                                                      ║`);
    console.log(`║  💰 Entrada: $${FIXED_ENTRY_USD} | ⚡ Alavancagem: ${MAX_LEVERAGE}x | 🎯 Target: ${TAKE_PROFIT_PERCENT}%     ║`);
    console.log(`║  🛑 Stop Loss: ${USE_STOP_LOSS ? `${STOP_LOSS_PERCENT}%` : 'NENHUM (risco total)'} | 🤖 Modo: ${autoTrade ? 'AUTOMÁTICO' : 'MANUAL'}          ║`);
    console.log('╠══════════════════════════════════════════════════════════════════════════════╣');
    console.log('║  🏆 TOP SETUPS (SMA 8/21)                                                   ║');
    const top3 = scanResults.slice(0, 4);
    if (top3.length === 0) {
        console.log('║    Aguardando scan...                                                           ║');
    } else {
        for (const s of top3) {
            const arrow = s.direction === 'BUY' ? '🟢 ▲ COMPRA' : '🔴 ▼ VENDA';
            console.log(`║    ${arrow.padEnd(12)} ${s.symbol.padEnd(8)} ${s.timeframe.padEnd(5)} | ${s.signalType.padEnd(10)} | Score: ${s.score}% ║`);
        }
    }
    console.log('╠══════════════════════════════════════════════════════════════════════════════╣');
    console.log('║  📊 POSIÇÕES ABERTAS                                                         ║');
    if (positions.length === 0) {
        console.log('║    Nenhuma posição aberta                                                        ║');
    } else {
        for (const p of positions) {
            const sideIcon = p.side === 'BUY' ? '🟢 COMPRA' : '🔴 VENDA';
            const targetProfit = p.quantity * Math.abs(p.targetPrice - p.entryPrice);
            console.log(`║    ${p.symbol.padEnd(8)} ${sideIcon.padEnd(10)} | Entrada: $${p.entryPrice.toFixed(2)} | Alvo: ${TAKE_PROFIT_PERCENT}% | Lucro pot: $${targetProfit.toFixed(2)} ║`);
        }
    }
    console.log('╠══════════════════════════════════════════════════════════════════════════════╣');
    console.log('║  📋 ÚLTIMOS TRADES                                                           ║');
    const lastTrades = trades.slice(-3).reverse();
    if (lastTrades.length === 0) {
        console.log('║    Nenhum trade ainda                                                           ║');
    } else {
        for (const t of lastTrades) {
            const profitIcon = t.profit >= 0 ? '✅' : '❌';
            console.log(`║    ${profitIcon} ${t.symbol.padEnd(8)} | Lucro: ${t.profit >= 0 ? '+' : ''}$${t.profit.toFixed(2)} (${t.profitPercent.toFixed(1)}%) | ${t.reason} ║`);
        }
    }
    console.log('╠══════════════════════════════════════════════════════════════════════════════╣');
    console.log('║  💡 COMANDOS:                                                                ║');
    console.log('║     [A] Automático  |  [M] Manual  |  [Q] Sair                               ║');
    console.log('║     [↑] +Leve     [↓] -Leve     [→] +Target%     [←] -Target%                 ║');
    console.log('║     [S] Ligar/Desligar Stop Loss                                              ║');
    console.log('╚══════════════════════════════════════════════════════════════════════════════╝');
}

async function mainLoop() {
    const results = await scanAll();
    for (const signal of results.slice(0, 5)) {
        if (signal.score >= 90) {
            const alertKey = `${signal.symbol}_${signal.timeframe}`;
            const now = Date.now();
            if (!lastAlert[alertKey] || now - lastAlert[alertKey] > 300000) {
                lastAlert[alertKey] = now;
                console.log(`\n🚨 SINAL DETECTADO! ${signal.symbol} ${signal.timeframe} - ${signal.direction === 'BUY' ? 'COMPRA' : 'VENDA'} (${signal.signalType} Score: ${signal.score})`);
                if (autoTrade) {
                    await executeTrade(signal);
                }
            }
        }
    }
    await monitorPositions();
}

// ============================================
// CONTROLE DE TECLADO
// ============================================
readline.emitKeypressEvents(process.stdin);
process.stdin.setRawMode(true);
process.stdin.on('keypress', (str, key) => {
    if (key.name === 'q') { console.clear(); console.log('\n👋 Encerrando...\n'); process.exit(); }
    if (key.name === 'a') { autoTrade = true; console.log('\n🤖 MODO AUTOMÁTICO ATIVADO!\n'); }
    if (key.name === 'm') { autoTrade = false; console.log('\n📋 MODO MANUAL ATIVADO.\n'); }
    
    if (key.name === 'up') { MAX_LEVERAGE = Math.min(MAX_LEVERAGE + 1, 20); console.log(`\n⚡ Alavancagem: ${MAX_LEVERAGE}x\n`); }
    if (key.name === 'down') { MAX_LEVERAGE = Math.max(MAX_LEVERAGE - 1, 1); console.log(`\n⚡ Alavancagem: ${MAX_LEVERAGE}x\n`); }
    
    if (key.name === 'right') { TAKE_PROFIT_PERCENT = Math.min(TAKE_PROFIT_PERCENT + 10, 400); console.log(`\n🎯 Take Profit: ${TAKE_PROFIT_PERCENT}%\n`); }
    if (key.name === 'left') { TAKE_PROFIT_PERCENT = Math.max(TAKE_PROFIT_PERCENT - 10, 50); console.log(`\n🎯 Take Profit: ${TAKE_PROFIT_PERCENT}%\n`); }
    
    if (key.name === 's') { USE_STOP_LOSS = !USE_STOP_LOSS; console.log(`\n🛑 Stop Loss: ${USE_STOP_LOSS ? 'ATIVADO' : 'DESLIGADO (risco total)'}\n`); }
});

// ============================================
// INICIAR
// ============================================
console.clear();
console.log('\n🦞 APEX IA - MODO AGRESSIVO (SEU ESTILO)');
console.log('📊 Conectando à Binance Futures Demo...\n');

await getBalance();
connectWebSocket();
setInterval(mainLoop, 30000);
setInterval(drawUI, 1000);
drawUI();
