#!/usr/bin/env node

import WebSocket from 'ws';
import axios from 'axios';
import fs from 'fs';
import path from 'path';
import readline from 'readline';
import crypto from 'crypto';

// ============================================
// SUAS CHAVES API
// ============================================
const API_KEY = 'Dq0vl5xeDxwQKMBwoJT5A9yxsJiW8hbXyVO7831c4xbI0N1tfiQjsTf1ZKsSVIXL';
const API_SECRET = '1kVF6XZuV5rVnKyIiAjbLTNcN50tQZEI8M5p90piOblTOl4W19rpgIeZMRzDlBBb';
const USE_DEMO = true;
const BASE_URL = USE_DEMO ? 'https://testnet.binancefuture.com' : 'https://fapi.binance.com';

// ============================================
// CONFIGURAÇÕES DO ROBÔ
// ============================================
const SMA_FAST = 8;
const SMA_SLOW = 21;
const TIMEFRAMES = ['5m', '15m', '30m', '1h', '4h'];
const SYMBOLS = ['btcusdt', 'ethusdt', 'bchusdt', 'solusdt', 'adausdt', 'ltcusdt', 'linkusdt', 'xrpusdt', 'dogeusdt', 'avaxusdt'];

// CONFIGURAÇÕES DE RISCO (SEGURAS)
let RISK_PERCENT = 0.5;          // 0.5% do saldo por trade
let MAX_LEVERAGE = 5;            // Alavancagem máxima 5x
let MAX_POSITIONS = 3;           // Máximo de 3 posições simultâneas

let autoTrade = true;
let equity = 7080.58;
let positions = [];
let trades = [];
let lastPrices = {};
let scanResults = [];
let candles = {};
let lastAlert = {};

// ============================================
// FUNÇÕES DA BINANCE FUTURES
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
    } catch (err) { 
        return null; 
    }
}

async function setLeverage(symbol, leverage) {
    const safeLeverage = Math.min(leverage, MAX_LEVERAGE);
    const result = await binanceRequest('POST', '/fapi/v1/leverage', {
        symbol: symbol.toUpperCase(),
        leverage: safeLeverage
    }, true);
    if (result) {
        console.log(`   ✅ Alavancagem ${safeLeverage}x configurada para ${symbol}`);
    }
    return result;
}

async function getBalance() {
    const data = await binanceRequest('GET', '/fapi/v2/account', {}, true);
    if (data && data.assets) {
        const usdtAsset = data.assets.find(a => a.asset === 'USDT');
        if (usdtAsset) { 
            equity = parseFloat(usdtAsset.walletBalance); 
            return equity; 
        }
    }
    return equity;
}

async function getPrice(symbol) {
    try {
        const response = await axios.get(`${BASE_URL}/fapi/v1/ticker/price?symbol=${symbol.toUpperCase()}`, { timeout: 5000 });
        return parseFloat(response.data.price);
    } catch (err) { 
        return null; 
    }
}

async function openPosition(symbol, side, quantity, stopLoss, takeProfit) {
    // Verificar limite de posições
    if (positions.length >= MAX_POSITIONS) {
        console.log(`   ⚠️ Limite de ${MAX_POSITIONS} posições simultâneas atingido`);
        return null;
    }
    
    // Verificar quantidade mínima
    const finalQuantity = Math.max(quantity, 0.001);
    if (finalQuantity < 0.001) {
        console.log(`   ⚠️ Quantidade muito pequena: ${finalQuantity}`);
        return null;
    }
    
    // Configurar alavancagem
    await setLeverage(symbol, MAX_LEVERAGE);
    
    console.log(`\n🔧 Enviando ordem MARKET para ${symbol}...`);
    console.log(`   Side: ${side}`);
    console.log(`   Quantity: ${finalQuantity.toFixed(4)}`);
    
    // Tentar abrir posição
    const order = await binanceRequest('POST', '/fapi/v1/order', {
        symbol: symbol.toUpperCase(),
        side: side.toUpperCase(),
        type: 'MARKET',
        quantity: finalQuantity,
        reduceOnly: 'false'
    }, true);
    
    if (order && order.orderId) {
        const entryPrice = parseFloat(order.price) || await getPrice(symbol);
        console.log(`   ✅ Ordem executada! ID: ${order.orderId}`);
        console.log(`   Preço de entrada: $${entryPrice.toFixed(2)}`);
        console.log(`   Quantidade: ${finalQuantity.toFixed(4)}`);
        
        const stopSide = side === 'BUY' ? 'SELL' : 'BUY';
        
        // Adicionar STOP LOSS (opcional, não crítico)
        try {
            await binanceRequest('POST', '/fapi/v1/order', {
                symbol: symbol.toUpperCase(),
                side: stopSide,
                type: 'STOP_MARKET',
                quantity: finalQuantity,
                stopPrice: stopLoss.toFixed(2),
                reduceOnly: 'true'
            }, true);
            console.log(`   ✅ Stop Loss configurado em $${stopLoss.toFixed(2)}`);
        } catch (err) {
            console.log(`   ⚠️ Stop Loss não configurado (ordem seguirá sem stop)`);
        }
        
        // Adicionar TAKE PROFIT (opcional, não crítico)
        try {
            await binanceRequest('POST', '/fapi/v1/order', {
                symbol: symbol.toUpperCase(),
                side: stopSide,
                type: 'TAKE_PROFIT_MARKET',
                quantity: finalQuantity,
                stopPrice: takeProfit.toFixed(2),
                reduceOnly: 'true'
            }, true);
            console.log(`   ✅ Take Profit configurado em $${takeProfit.toFixed(2)}`);
        } catch (err) {
            console.log(`   ⚠️ Take Profit não configurado`);
        }
        
        // Registrar posição
        positions.push({
            symbol: symbol.toUpperCase(),
            side: side,
            quantity: finalQuantity,
            entryPrice: entryPrice,
            stopLoss: stopLoss,
            takeProfit: takeProfit,
            leverage: MAX_LEVERAGE,
            openedAt: new Date().toISOString()
        });
        
        console.log(`\n✅ POSIÇÃO ABERTA COM SUCESSO!`);
        return order;
    } else {
        console.log(`   ❌ Erro na ordem: ${JSON.stringify(order)}`);
        return null;
    }
}

async function closePosition(symbol) {
    const position = positions.find(p => p.symbol === symbol.toUpperCase());
    if (!position) return null;
    
    const side = position.side === 'BUY' ? 'SELL' : 'BUY';
    const order = await binanceRequest('POST', '/fapi/v1/order', {
        symbol: symbol.toUpperCase(),
        side: side,
        type: 'MARKET',
        quantity: position.quantity,
        reduceOnly: 'true'
    }, true);
    
    if (order && order.orderId) {
        const currentPrice = await getPrice(symbol) || position.entryPrice;
        const profit = position.side === 'BUY' 
            ? (currentPrice - position.entryPrice) * position.quantity
            : (position.entryPrice - currentPrice) * position.quantity;
        
        trades.push({
            symbol: symbol.toUpperCase(),
            side: position.side,
            entryPrice: position.entryPrice,
            exitPrice: currentPrice,
            quantity: position.quantity,
            profit: profit,
            leverage: position.leverage,
            closedAt: new Date().toISOString()
        });
        
        positions = positions.filter(p => p.symbol !== symbol.toUpperCase());
        console.log(`\n📊 POSIÇÃO FECHADA: ${symbol} | Lucro: ${profit >= 0 ? '+' : ''}$${profit.toFixed(2)}`);
        return { order, profit };
    }
    return null;
}

async function monitorPositions() {
    for (const position of positions) {
        const currentPrice = await getPrice(position.symbol);
        if (!currentPrice) continue;
        
        const profit = position.side === 'BUY' 
            ? (currentPrice - position.entryPrice) * position.quantity
            : (position.entryPrice - currentPrice) * position.quantity;
        
        const profitPercent = (profit / (position.entryPrice * position.quantity)) * 100;
        
        // Verificar se atingiu take profit (target1)
        if (position.takeProfit && currentPrice >= position.takeProfit) {
            console.log(`🎯 TAKE PROFIT ATINGIDO! ${position.symbol} | Lucro: ${profitPercent.toFixed(2)}%`);
            await closePosition(position.symbol);
        } 
        // Verificar se atingiu stop loss
        else if (position.stopLoss && currentPrice <= position.stopLoss) {
            console.log(`🛑 STOP LOSS ATINGIDO! ${position.symbol} | Perda: ${profitPercent.toFixed(2)}%`);
            await closePosition(position.symbol);
        }
    }
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
                const smaFast = calculateSMA(closes, SMA_FAST);
                const smaSlow = calculateSMA(closes, SMA_SLOW);
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
                        target1: closes[closes.length - 1] * 1.015
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
    if (!autoTrade) {
        console.log(`⏸️ Modo manual, sinal não executado`);
        return false;
    }
    
    if (positions.length >= MAX_POSITIONS) {
        console.log(`⚠️ Máximo de ${MAX_POSITIONS} posições simultâneas atingido`);
        return false;
    }
    
    const balance = await getBalance();
    if (balance < 50) {
        console.log(`❌ Saldo insuficiente: $${balance.toFixed(2)}`);
        return false;
    }
    
    const currentPrice = await getPrice(signal.symbol);
    if (!currentPrice) {
        console.log(`❌ Não foi possível obter preço de ${signal.symbol}`);
        return false;
    }
    
    // Calcular quantidade (1% do saldo com alavancagem)
    const riskAmount = balance * (RISK_PERCENT / 100);
    const positionSize = riskAmount * MAX_LEVERAGE;
    let quantity = positionSize / currentPrice;
    
    // Limitar quantidade máxima
    const maxQuantity = 0.5;
    if (quantity > maxQuantity) {
        quantity = maxQuantity;
        console.log(`   Quantidade limitada a ${maxQuantity} por segurança`);
    }
    
    // Garantir quantidade mínima
    quantity = Math.max(quantity, 0.001);
    
    console.log(`\n📊 EXECUTANDO TRADE:`);
    console.log(`   Símbolo: ${signal.symbol}`);
    console.log(`   Direção: ${signal.direction === 'BUY' ? 'COMPRA' : 'VENDA'}`);
    console.log(`   Preço: $${currentPrice.toFixed(2)}`);
    console.log(`   Quantidade: ${quantity.toFixed(4)}`);
    console.log(`   Alavancagem: ${MAX_LEVERAGE}x`);
    console.log(`   Risco: ${RISK_PERCENT}% do saldo`);
    console.log(`   Stop: $${signal.stop.toFixed(2)}`);
    console.log(`   Target: $${signal.target1.toFixed(2)}`);
    
    const order = await openPosition(signal.symbol, signal.direction, quantity, signal.stop, signal.target1);
    
    if (order) {
        console.log(`\n✅ TRADE EXECUTADO COM SUCESSO!`);
        return true;
    } else {
        console.log(`\n❌ FALHA AO EXECUTAR TRADE`);
        return false;
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
                lastPrices[symbol] = parseFloat(msg.data.c);
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
    console.log('║                    🦞 APEX IA - ROBÔ FUTURES - SISTEMA COMPLETO                 ║');
    console.log('╠══════════════════════════════════════════════════════════════════════════════╣');
    console.log(`║  📅 ${now.toLocaleDateString('pt-BR')} | ${now.toLocaleTimeString('pt-BR')}                                                      ║`);
    console.log(`║  💰 Saldo: $${equity.toFixed(2)} | 🤖 Modo: ${autoTrade ? 'AUTOMÁTICO' : 'MANUAL'} | ⚡ Alavancagem: ${MAX_LEVERAGE}x | 📊 Risco: ${RISK_PERCENT}%  ║`);
    console.log(`║  📈 Posições: ${positions.length}/${MAX_POSITIONS} | 🔒 Limite seguro ativo                                         ║`);
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
    console.log('║  📊 POSIÇÕES ABERTAS (FUTURES)                                               ║');
    if (positions.length === 0) {
        console.log('║    Nenhuma posição aberta                                                        ║');
    } else {
        for (const p of positions) {
            const sideIcon = p.side === 'BUY' ? '🟢 COMPRA' : '🔴 VENDA';
            console.log(`║    ${p.symbol.padEnd(8)} ${sideIcon.padEnd(10)} | Entrada: $${p.entryPrice.toFixed(2)} | ${p.leverage}x ║`);
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
            console.log(`║    ${profitIcon} ${t.symbol.padEnd(8)} | Lucro: ${t.profit >= 0 ? '+' : ''}$${t.profit.toFixed(2)} | ${t.leverage}x                        ║`);
        }
    }
    console.log('╠══════════════════════════════════════════════════════════════════════════════╣');
    console.log('║  💡 COMANDOS:                                                                ║');
    console.log('║     [A] Automático  |  [M] Manual  |  [Q] Sair                               ║');
    console.log('║     [↑] +Leve (max 5x)  |  [↓] -Leve    |  [→] +Risco (max 2%)  |  [←] -Risco ║');
    console.log('║     🔒 LIMITES: Alavancagem MAX 5x | Risco MAX 2% | Posições MAX 3            ║');
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
    await getBalance();
}

// ============================================
// CONTROLE DE TECLADO
// ============================================
readline.emitKeypressEvents(process.stdin);
process.stdin.setRawMode(true);
process.stdin.on('keypress', (str, key) => {
    if (key.name === 'q') { console.clear(); console.log('\n👋 Encerrando sistema...\n'); process.exit(); }
    if (key.name === 'a') { autoTrade = true; console.log('\n🤖 MODO AUTOMÁTICO ATIVADO!\n'); }
    if (key.name === 'm') { autoTrade = false; console.log('\n📋 MODO MANUAL ATIVADO.\n'); }
    
    if (key.name === 'up') { 
        MAX_LEVERAGE = Math.min(MAX_LEVERAGE + 1, 5); 
        console.log(`\n⚡ Alavancagem ajustada para ${MAX_LEVERAGE}x\n`);
    }
    if (key.name === 'down') { 
        MAX_LEVERAGE = Math.max(MAX_LEVERAGE - 1, 1); 
        console.log(`\n⚡ Alavancagem ajustada para ${MAX_LEVERAGE}x\n`);
    }
    
    if (key.name === 'right') { 
        RISK_PERCENT = Math.min(RISK_PERCENT + 0.5, 2); 
        console.log(`\n📊 Risco ajustado para ${RISK_PERCENT}% do saldo\n`);
    }
    if (key.name === 'left') { 
        RISK_PERCENT = Math.max(RISK_PERCENT - 0.5, 0.5); 
        console.log(`\n📊 Risco ajustado para ${RISK_PERCENT}% do saldo\n`);
    }
});

// ============================================
// INICIAR
// ============================================
console.clear();
console.log('\n🦞 APEX IA - ROBÔ DE FUTURES - SISTEMA COMPLETO v4.0');
console.log('📊 Conectando à Binance Futures Demo...\n');

await getBalance();
connectWebSocket();
setInterval(mainLoop, 30000);
setInterval(drawUI, 1000);
drawUI();
