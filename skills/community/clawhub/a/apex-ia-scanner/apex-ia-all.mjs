#!/usr/bin/env node

import WebSocket from 'ws';
import axios from 'axios';
import fs from 'fs';
import path from 'path';
import readline from 'readline';
import crypto from 'crypto';

// ============================================
// CONFIGURAÇÕES - SUAS CHAVES API
// ============================================
const API_KEY = 'Dq0vl5xeDxwQKMBwoJT5A9yxsJiW8hbXyVO7831c4xbI0N1tfiQjsTf1ZKsSVIXL';
const API_SECRET = 'COLE_SEU_SECRET_AQUI';
const USE_DEMO = true;
const BASE_URL = USE_DEMO ? 'https://testnet.binancefuture.com' : 'https://fapi.binance.com';

const SMA_FAST = 8;
const SMA_SLOW = 21;
const TIMEFRAMES = ['5m', '15m', '30m', '1h', '4h'];
const SYMBOLS = ['btcusdt', 'ethusdt', 'bchusdt', 'solusdt', 'adausdt', 'ltcusdt', 'linkusdt', 'xrpusdt', 'dogeusdt', 'avaxusdt'];
const MAX_POSITION_SIZE_USD = 500;

let autoTrade = false;
let equity = 0;
let positions = [];
let trades = [];
let lastPrices = {};
let scanResults = [];
let candles = {};
let lastAlert = {};

// ============================================
// FUNÇÕES BINANCE
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
        const response = await axios({ method, url, headers: { 'X-MBX-APIKEY': API_KEY } });
        return response.data;
    } catch (err) { return null; }
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
        const response = await axios.get(`${BASE_URL}/fapi/v1/ticker/price?symbol=${symbol.toUpperCase()}`);
        return parseFloat(response.data.price);
    } catch (err) { return null; }
}

async function openPosition(symbol, side, quantity, stopLoss, takeProfit) {
    const order = await binanceRequest('POST', '/fapi/v1/order', {
        symbol: symbol.toUpperCase(),
        side: side.toUpperCase(),
        type: 'MARKET',
        quantity: quantity.toFixed(3)
    }, true);
    
    if (order && order.orderId) {
        if (stopLoss) {
            await binanceRequest('POST', '/fapi/v1/order', {
                symbol: symbol.toUpperCase(),
                side: side === 'BUY' ? 'SELL' : 'BUY',
                type: 'STOP_MARKET',
                quantity: quantity.toFixed(3),
                stopPrice: stopLoss.toFixed(2),
                price: stopLoss.toFixed(2)
            }, true);
        }
        if (takeProfit) {
            await binanceRequest('POST', '/fapi/v1/order', {
                symbol: symbol.toUpperCase(),
                side: side === 'BUY' ? 'SELL' : 'BUY',
                type: 'TAKE_PROFIT_MARKET',
                quantity: quantity.toFixed(3),
                stopPrice: takeProfit.toFixed(2),
                price: takeProfit.toFixed(2)
            }, true);
        }
        positions.push({
            symbol: symbol.toUpperCase(),
            side,
            quantity,
            entryPrice: parseFloat(order.price),
            stopLoss,
            takeProfit,
            openedAt: new Date().toISOString()
        });
        console.log(`\n✅ ORDEM EXECUTADA: ${symbol} ${side} ${quantity.toFixed(4)} @ ${order.price}`);
        return order;
    }
    return null;
}

async function closePosition(symbol) {
    const position = positions.find(p => p.symbol === symbol.toUpperCase());
    if (!position) return null;
    const side = position.side === 'BUY' ? 'SELL' : 'BUY';
    const order = await binanceRequest('POST', '/fapi/v1/order', {
        symbol: symbol.toUpperCase(),
        side,
        type: 'MARKET',
        quantity: position.quantity.toFixed(3)
    }, true);
    if (order) {
        const currentPrice = await getPrice(symbol);
        const profit = position.side === 'BUY' 
            ? (currentPrice - position.entryPrice) * position.quantity
            : (position.entryPrice - currentPrice) * position.quantity;
        trades.push({
            symbol: symbol.toUpperCase(),
            side: position.side,
            entryPrice: position.entryPrice,
            exitPrice: currentPrice,
            quantity: position.quantity,
            profit,
            closedAt: new Date().toISOString()
        });
        positions = positions.filter(p => p.symbol !== symbol.toUpperCase());
        console.log(`\n📊 POSIÇÃO FECHADA: ${symbol} | Lucro: $${profit.toFixed(2)}`);
        return { order, profit };
    }
    return null;
}

async function monitorPositions() {
    for (const position of positions) {
        const currentPrice = await getPrice(position.symbol);
        if (!currentPrice) continue;
        if (position.takeProfit && currentPrice >= position.takeProfit) {
            await closePosition(position.symbol);
        } else if (position.stopLoss && currentPrice <= position.stopLoss) {
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
    if (!autoTrade) return false;
    const balance = await getBalance();
    if (balance < 50) return false;
    const riskAmount = balance * 0.01;
    const currentPrice = await getPrice(signal.symbol);
    if (!currentPrice) return false;
    const stopDistance = Math.abs(currentPrice - signal.stop) / currentPrice;
    const quantity = (riskAmount / currentPrice) / (stopDistance + 0.01);
    const finalQuantity = Math.min(quantity, MAX_POSITION_SIZE_USD / currentPrice);
    const order = await openPosition(signal.symbol, signal.direction, finalQuantity, signal.stop, signal.target1);
    return !!order;
}

// ============================================
// WEBSOCKET
// ============================================
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

// ============================================
// UI
// ============================================
function drawUI() {
    console.clear();
    const now = new Date();
    console.log('╔════════════════════════════════════════════════════════════════════╗');
    console.log('║                 🦞 APEX IA - SISTEMA COMPLETO v3.0                 ║');
    console.log('╠════════════════════════════════════════════════════════════════════╣');
    console.log(`║  📅 ${now.toLocaleDateString('pt-BR')} | ${now.toLocaleTimeString('pt-BR')}                                         ║`);
    console.log(`║  💰 Saldo Demo: $${equity.toFixed(2)} | 🤖 Modo: ${autoTrade ? 'AUTOMATICO' : 'MANUAL'}                    ║`);
    console.log('╠════════════════════════════════════════════════════════════════════╣');
    console.log('║  🏆 TOP SETUPS                                                   ║');
    const top3 = scanResults.slice(0, 3);
    if (top3.length === 0) {
        console.log('║    Aguardando scan...                                              ║');
    } else {
        for (const s of top3) {
            const arrow = s.direction === 'BUY' ? '🟢 ▲' : '🔴 ▼';
            console.log(`║    ${arrow} ${s.symbol.padEnd(8)} ${s.timeframe.padEnd(5)} | ${s.signalType.padEnd(12)} | Score: ${s.score}% ║`);
        }
    }
    console.log('╠════════════════════════════════════════════════════════════════════╣');
    console.log('║  📊 POSICOES ABERTAS                                              ║');
    if (positions.length === 0) {
        console.log('║    Nenhuma posicao aberta                                           ║');
    } else {
        for (const p of positions) {
            console.log(`║    ${p.symbol} ${p.side === 'BUY' ? '🟢 COMPRA' : '🔴 VENDA'} | Entrada: $${p.entryPrice.toFixed(2)}     ║`);
        }
    }
    console.log('╠════════════════════════════════════════════════════════════════════╣');
    console.log('║  📋 ULTIMOS TRADES                                                ║');
    const lastTrades = trades.slice(-3).reverse();
    if (lastTrades.length === 0) {
        console.log('║    Nenhum trade ainda                                                ║');
    } else {
        for (const t of lastTrades) {
            const profitIcon = t.profit >= 0 ? '✅' : '❌';
            console.log(`║    ${profitIcon} ${t.symbol} | Lucro: ${t.profit >= 0 ? '+' : ''}$${t.profit.toFixed(2)}                            ║`);
        }
    }
    console.log('╚════════════════════════════════════════════════════════════════════╝');
    console.log('\n💡 [A] Automatico | [M] Manual | [Q] Sair\n');
}

// ============================================
// LOOP PRINCIPAL
// ============================================
async function mainLoop() {
    const results = await scanAll();
    for (const signal of results.slice(0, 5)) {
        if (signal.score >= 90) {
            const alertKey = `${signal.symbol}_${signal.timeframe}`;
            const now = Date.now();
            if (!lastAlert[alertKey] || now - lastAlert[alertKey] > 300000) {
                lastAlert[alertKey] = now;
                console.log(`\n🚨 SINAL DETECTADO! ${signal.symbol} ${signal.timeframe} - ${signal.direction === 'BUY' ? 'COMPRA' : 'VENDA'} (${signal.signalType})`);
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
// TECLAS
// ============================================
readline.emitKeypressEvents(process.stdin);
process.stdin.setRawMode(true);
process.stdin.on('keypress', (str, key) => {
    if (key.name === 'q') { console.clear(); console.log('\n👋 Encerrando...\n'); process.exit(); }
    if (key.name === 'a') { autoTrade = true; console.log('\n🤖 MODO AUTOMATICO ATIVADO!\n'); }
    if (key.name === 'm') { autoTrade = false; console.log('\n📋 MODO MANUAL ATIVADO.\n'); }
});

// ============================================
// INICIAR
// ============================================
console.clear();
console.log('\n🦞 APEX IA - SISTEMA COMPLETO v3.0\n');
await getBalance();
connectWebSocket();
setInterval(mainLoop, 30000);
setInterval(drawUI, 1000);
drawUI();
