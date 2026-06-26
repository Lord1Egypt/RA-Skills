#!/usr/bin/env node

import WebSocket from 'ws';
import axios from 'axios';
import fs from 'fs';
import path from 'path';
import readline from 'readline';
import crypto from 'crypto';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ============================================
// LOG EM ARQUIVO E MEMÓRIA
// ============================================
const LOG_FILE = path.join(process.env.HOME, 'apex-ia-skill', 'operacoes.log');
let messageLog = [];

function addMessage(type, text) {
    const timestamp = new Date().toLocaleString('pt-BR');
    let color = '';
    let reset = '\x1b[0m';
    
    switch(type) {
        case 'success': color = '\x1b[32m'; break;
        case 'error': color = '\x1b[31m'; break;
        case 'warning': color = '\x1b[33m'; break;
        case 'info': color = '\x1b[36m'; break;
        default: color = '\x1b[37m'; break;
    }
    
    const logMessage = `[${timestamp}] ${text}`;
    messageLog.unshift(logMessage);
    if (messageLog.length > 100) messageLog.pop();
    fs.appendFileSync(LOG_FILE, logMessage + '\n');
    console.log(`${color}${logMessage}${reset}`);
}

function addError(text) { addMessage('error', `❌ ${text}`); }
function addSuccess(text) { addMessage('success', `✅ ${text}`); }
function addWarning(text) { addMessage('warning', `⚠️ ${text}`); }
function addInfo(text) { addMessage('info', `📢 ${text}`); }

// ============================================
// CONVERSÃO BRL
// ============================================
const USD_BRL_RATE = 4.91;

// ============================================
// SUAS CHAVES API
// ============================================
const API_KEY = 'Dq0vl5xeDxwQKMBwoJT5A9yxsJiW8hbXyVO7831c4xbI0N1tfiQjsTf1ZKsSVIXL';
const API_SECRET = '1kVF6XZuV5rVnKyIiAjbLTNcN50tQZEI8M5p90piOblTOl4W19rpgIeZMRzDlBBb';
const USE_DEMO = true;
const BASE_URL = USE_DEMO ? 'https://testnet.binancefuture.com' : 'https://fapi.binance.com';

// ============================================
// CORREÇÃO DE TIMESTAMP
// ============================================
let serverTimeOffset = 0;

async function syncServerTime() {
    try {
        const response = await axios.get(`${BASE_URL}/fapi/v1/time`, { timeout: 5000 });
        const serverTime = response.data.serverTime;
        const localTime = Date.now();
        serverTimeOffset = serverTime - localTime;
        addSuccess(`Sincronizado com servidor (diferença: ${serverTimeOffset}ms)`);
        return serverTimeOffset;
    } catch (err) {
        addWarning(`Não foi possível sincronizar com servidor`);
        serverTimeOffset = 0;
        return 0;
    }
}

function getTimestamp() {
    return Date.now() + serverTimeOffset;
}

// ============================================
// CONFIGURAÇÕES AJUSTÁVEIS
// ============================================
const SMA_FAST = 8;
const SMA_SLOW = 21;
const TIMEFRAMES = ['5m', '15m', '30m', '1h', '4h'];
const SYMBOLS = ['btcusdt', 'ethusdt', 'bchusdt', 'solusdt', 'adausdt', 'ltcusdt', 'linkusdt', 'xrpusdt', 'dogeusdt', 'avaxusdt'];

let FIXED_ENTRY_USD = 30;
let MAX_LEVERAGE = 20;
let TAKE_PROFIT_PERCENT = 200;
let USE_STOP_LOSS = false;

let autoTrade = true;
let equity = 7080.58;
let positions = [];
let trades = [];
let lastPrices = {};
let scanResults = [];
let candles = {};
let lastAlert = {};
let processedSignals = new Set();
let wsConnected = false;
let exchangeInfo = null;
let symbolPrecisions = {};

// ============================================
// LIMITE DE POSIÇÕES - ALTERADO PARA 7
// ============================================
const MAX_POSITIONS = 7;  // Agora permite até 7 posições simultâneas

// ============================================
// BUSCAR INFORMAÇÕES DOS SÍMBOLOS
// ============================================
async function getExchangeInfo() {
    if (exchangeInfo) return exchangeInfo;
    try {
        const response = await axios.get(`${BASE_URL}/fapi/v1/exchangeInfo`);
        exchangeInfo = response.data;
        
        for (const symbol of exchangeInfo.symbols) {
            const lotSizeFilter = symbol.filters.find(f => f.filterType === 'LOT_SIZE');
            if (lotSizeFilter) {
                const stepSize = parseFloat(lotSizeFilter.stepSize);
                const precision = stepSize.toString().split('.')[1]?.length || 0;
                symbolPrecisions[symbol.symbol] = precision;
            }
        }
        
        addSuccess(`Informações de mercado carregadas`);
        return exchangeInfo;
    } catch (err) {
        addError(`Erro ao carregar informações: ${err.message}`);
        return null;
    }
}

function getQuantityPrecision(symbol) {
    const upperSymbol = symbol.toUpperCase();
    if (symbolPrecisions[upperSymbol] !== undefined) {
        return symbolPrecisions[upperSymbol];
    }
    return 3;
}

function getMinQuantity(symbol) {
    if (!exchangeInfo) return 0.001;
    const symbolInfo = exchangeInfo.symbols.find(s => s.symbol === symbol.toUpperCase());
    if (!symbolInfo) return 0.001;
    const lotSizeFilter = symbolInfo.filters.find(f => f.filterType === 'LOT_SIZE');
    if (lotSizeFilter) return parseFloat(lotSizeFilter.minQty);
    return 0.001;
}

function formatQuantity(quantity, symbol) {
    const precision = getQuantityPrecision(symbol);
    return parseFloat(quantity.toFixed(precision));
}

// ============================================
// FUNÇÕES DA BINANCE
// ============================================
function generateSignature(queryString, secret) {
    return crypto.createHmac('sha256', secret).update(queryString).digest('hex');
}

async function binanceRequest(method, endpoint, params = {}, signed = false) {
    const timestamp = getTimestamp();
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
        if (err.response && err.response.data) {
            if (err.response.data.code === -1021) {
                addWarning(`Erro de timestamp, sincronizando...`);
                await syncServerTime();
            }
            addError(`Binance: ${JSON.stringify(err.response.data)}`);
            return { error: true, code: err.response.data.code, msg: err.response.data.msg };
        }
        return { error: true, msg: err.message };
    }
}

async function setLeverage(symbol, leverage) {
    const result = await binanceRequest('POST', '/fapi/v1/leverage', {
        symbol: symbol.toUpperCase(),
        leverage: leverage
    }, true);
    if (result && !result.error) {
        addSuccess(`Alavancagem ${leverage}x configurada`);
        return true;
    }
    return false;
}

async function getBalance() {
    const data = await binanceRequest('GET', '/fapi/v2/account', {}, true);
    if (data && !data.error && data.assets) {
        const usdtAsset = data.assets.find(a => a.asset === 'USDT');
        if (usdtAsset) { equity = parseFloat(usdtAsset.walletBalance); }
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
    // Verificar limite de posições
    if (positions.length >= MAX_POSITIONS) {
        addWarning(`Limite de ${MAX_POSITIONS} posições atingido. Não é possível abrir nova posição.`);
        return null;
    }
    
    await getExchangeInfo();
    
    const adjustedQuantity = formatQuantity(quantity, symbol);
    const minQty = getMinQuantity(symbol);
    
    if (adjustedQuantity < minQty) {
        const minEntry = (minQty * entryPrice / MAX_LEVERAGE).toFixed(2);
        addError(`Quantidade mínima para ${symbol}: ${minQty}. Entrada mínima sugerida: $${minEntry}`);
        return null;
    }
    
    const existingPosition = positions.find(p => p.symbol === symbol.toUpperCase());
    if (existingPosition) {
        addWarning(`Posição já existe para ${symbol}`);
        return null;
    }
    
    await setLeverage(symbol, MAX_LEVERAGE);
    
    addInfo(`Enviando ordem: ${symbol} ${side} ${adjustedQuantity.toFixed(getQuantityPrecision(symbol))} @ ~$${entryPrice.toFixed(4)}`);
    
    const order = await binanceRequest('POST', '/fapi/v1/order', {
        symbol: symbol.toUpperCase(),
        side: side.toUpperCase(),
        type: 'MARKET',
        quantity: adjustedQuantity
    }, true);
    
    if (order && !order.error && order.orderId) {
        const targetPrice = side === 'BUY' 
            ? entryPrice * (1 + TAKE_PROFIT_PERCENT / 100)
            : entryPrice * (1 - TAKE_PROFIT_PERCENT / 100);
        
        const stopSide = side === 'BUY' ? 'SELL' : 'BUY';
        await binanceRequest('POST', '/fapi/v1/order', {
            symbol: symbol.toUpperCase(),
            side: stopSide,
            type: 'TAKE_PROFIT_MARKET',
            quantity: adjustedQuantity,
            stopPrice: targetPrice.toFixed(2),
            reduceOnly: 'true'
        }, true);
        
        const positionValue = FIXED_ENTRY_USD * MAX_LEVERAGE;
        const potentialProfitUSD = positionValue * (TAKE_PROFIT_PERCENT / 100);
        
        positions.push({
            symbol: symbol.toUpperCase(),
            side: side,
            quantity: adjustedQuantity,
            entryPrice: entryPrice,
            targetPrice: targetPrice,
            leverage: MAX_LEVERAGE,
            targetPercent: TAKE_PROFIT_PERCENT,
            investedUSD: FIXED_ENTRY_USD,
            positionValue: positionValue,
            openedAt: new Date().toISOString()
        });
        
        addSuccess(`${symbol} ${side === 'BUY' ? 'COMPRA' : 'VENDA'} aberta!`);
        addInfo(`   Quantidade: ${adjustedQuantity.toFixed(getQuantityPrecision(symbol))} | Entrada: $${entryPrice.toFixed(4)}`);
        addInfo(`   Investido: $${FIXED_ENTRY_USD} | Posição: $${positionValue.toFixed(2)} | Alvo: +$${potentialProfitUSD.toFixed(2)}`);
        addInfo(`   Posições atuais: ${positions.length}/${MAX_POSITIONS}`);
        
        return order;
    } else if (order && order.error) {
        addError(`Erro na ordem: ${order.msg}`);
        return null;
    }
    return null;
}

async function closePosition(symbol, reason) {
    const position = positions.find(p => p.symbol === symbol.toUpperCase());
    if (!position) return null;
    
    const currentPrice = await getPrice(symbol);
    if (!currentPrice) return null;
    
    const side = position.side === 'BUY' ? 'SELL' : 'BUY';
    const adjustedQuantity = formatQuantity(position.quantity, symbol);
    
    const order = await binanceRequest('POST', '/fapi/v1/order', {
        symbol: symbol.toUpperCase(),
        side: side,
        type: 'MARKET',
        quantity: adjustedQuantity,
        reduceOnly: 'true'
    }, true);
    
    if (order && !order.error) {
        const priceMovePercent = position.side === 'BUY' 
            ? ((currentPrice - position.entryPrice) / position.entryPrice) * 100
            : ((position.entryPrice - currentPrice) / position.entryPrice) * 100;
        
        const profitPercent = priceMovePercent * position.leverage;
        const profitUSD = position.investedUSD * (profitPercent / 100);
        const profitBRL = profitUSD * USD_BRL_RATE;
        
        trades.push({
            symbol: symbol.toUpperCase(),
            side: position.side,
            entryPrice: position.entryPrice,
            exitPrice: currentPrice,
            quantity: adjustedQuantity,
            investedUSD: position.investedUSD,
            positionValue: position.positionValue,
            priceMovePercent: priceMovePercent,
            profitPercent: profitPercent,
            profitUSD: profitUSD,
            profitBRL: profitBRL,
            leverage: position.leverage,
            reason: reason,
            closedAt: new Date().toISOString()
        });
        
        positions = positions.filter(p => p.symbol !== symbol.toUpperCase());
        
        const profitIcon = profitUSD >= 0 ? '✅' : '❌';
        addSuccess(`${profitIcon} ${reason}! ${symbol} | Lucro: $${profitUSD.toFixed(2)} (${profitPercent.toFixed(2)}%) | R$${profitBRL.toFixed(2)}`);
        addInfo(`   Posições restantes: ${positions.length}/${MAX_POSITIONS}`);
        return { order, profit: profitUSD };
    }
    return null;
}

async function monitorPositions() {
    for (const position of positions) {
        const currentPrice = await getPrice(position.symbol);
        if (!currentPrice) continue;
        
        if (position.side === 'BUY' && currentPrice >= position.targetPrice) {
            await closePosition(position.symbol, '🎯 TARGET');
        } else if (position.side === 'SELL' && currentPrice <= position.targetPrice) {
            await closePosition(position.symbol, '🎯 TARGET');
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
                        signalId: `${symbol}_${tf}_${Date.now()}`
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
    if (processedSignals.has(signal.signalId)) return false;
    
    const existingPosition = positions.find(p => p.symbol === signal.symbol);
    if (existingPosition) {
        addWarning(`${signal.symbol} já tem posição, ignorando`);
        return false;
    }
    
    const currentPrice = await getPrice(signal.symbol);
    if (!currentPrice) return false;
    
    const positionSize = FIXED_ENTRY_USD * MAX_LEVERAGE;
    let quantity = positionSize / currentPrice;
    const adjustedQuantity = formatQuantity(quantity, signal.symbol);
    
    addInfo(`🚨 SINAL: ${signal.symbol} ${signal.direction === 'BUY' ? 'COMPRA' : 'VENDA'} (${signal.signalType} ${signal.score}%)`);
    addInfo(`   Investimento: $${FIXED_ENTRY_USD} | Alavancagem: ${MAX_LEVERAGE}x | Posição: $${positionSize.toFixed(2)}`);
    addInfo(`   Quantidade: ${adjustedQuantity.toFixed(getQuantityPrecision(signal.symbol))} | Preço: $${currentPrice.toFixed(4)}`);
    
    const order = await openPosition(signal.symbol, signal.direction, quantity, currentPrice);
    
    if (order) {
        processedSignals.add(signal.signalId);
        addSuccess(`✅ TRADE ${signal.symbol} EXECUTADO!`);
        return true;
    }
    return false;
}

function connectWebSocket() {
    const streams = SYMBOLS.map(s => `${s}@ticker`).join('/');
    const ws = new WebSocket(`wss://fstream.binance.com/stream?streams=${streams}`);
    ws.on('open', () => { wsConnected = true; addSuccess(`WebSocket conectado`); });
    ws.on('message', (data) => {
        try {
            const msg = JSON.parse(data);
            if (msg.data?.c && msg.stream) {
                const symbol = msg.stream.split('@')[0];
                lastPrices[symbol] = parseFloat(msg.data.c);
            }
        } catch (err) {}
    });
    ws.on('error', (err) => { addError(`WebSocket: ${err.message}`); wsConnected = false; });
    ws.on('close', () => { wsConnected = false; setTimeout(connectWebSocket, 5000); });
    return ws;
}

function drawUI() {
    console.clear();
    const now = new Date();
    
    console.log('\x1b[36m╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗\x1b[0m');
    console.log('\x1b[36m║\x1b[0m                              🦞 \x1b[33mAPEX IA - MODO AGRESSIVO (ENTRADA AJUSTÁVEL)\x1b[0m                                      \x1b[36m║\x1b[0m');
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log(`\x1b[36m║\x1b[0m  📅 ${now.toLocaleDateString('pt-BR')} | ${now.toLocaleTimeString('pt-BR')}                                                                        \x1b[36m║\x1b[0m`);
    console.log(`\x1b[36m║\x1b[0m  💰 Entrada: \x1b[33m$${FIXED_ENTRY_USD}\x1b[0m | ⚡ Alavancagem: ${MAX_LEVERAGE}x | 🎯 Target: ${TAKE_PROFIT_PERCENT}% | 🛑 Stop: ${USE_STOP_LOSS ? 'ON' : 'OFF'} | 🤖: ${autoTrade ? 'AUTOMÁTICO' : 'MANUAL'} | 🔌 WS: ${wsConnected ? '✅' : '❌'} \x1b[36m║\x1b[0m`);
    console.log(`\x1b[36m║\x1b[0m  📊 Posições: ${positions.length}/${MAX_POSITIONS} | 💰 Saldo: $${equity.toFixed(2)}                                                                 \x1b[36m║\x1b[0m`);
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log('\x1b[36m║\x1b[0m  \x1b[33m🏆 TOP SETUPS (SMA 8/21)\x1b[0m                                                                                              \x1b[36m║\x1b[0m');
    const top3 = scanResults.slice(0, 4);
    if (top3.length === 0) {
        console.log('\x1b[36m║\x1b[0m    Aguardando scan...                                                                                              \x1b[36m║\x1b[0m');
    } else {
        for (const s of top3) {
            const arrow = s.direction === 'BUY' ? '🟢 ▲ COMPRA' : '🔴 ▼ VENDA';
            const jaTem = positions.some(p => p.symbol === s.symbol);
            const status = jaTem ? '⚠️ IGNORAR' : '✅ LIVRE';
            console.log(`\x1b[36m║\x1b[0m    ${arrow.padEnd(12)} ${s.symbol.padEnd(8)} ${s.timeframe.padEnd(5)} | ${s.signalType.padEnd(10)} | Score: ${s.score}% | ${status.padEnd(10)}                         \x1b[36m║\x1b[0m`);
        }
    }
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log('\x1b[36m║\x1b[0m  \x1b[33m📊 POSIÇÕES ABERTAS (${positions.length}/${MAX_POSITIONS})\x1b[0m                                                                                        \x1b[36m║\x1b[0m');
    if (positions.length === 0) {
        console.log('\x1b[36m║\x1b[0m    Nenhuma posição aberta                                                                                          \x1b[36m║\x1b[0m');
    } else {
        for (const p of positions) {
            const sideIcon = p.side === 'BUY' ? '🟢 COMPRA' : '🔴 VENDA';
            const targetProfit = p.positionValue * (TAKE_PROFIT_PERCENT / 100);
            console.log(`\x1b[36m║\x1b[0m    ${p.symbol.padEnd(8)} ${sideIcon.padEnd(10)} | Entrada: $${p.entryPrice.toFixed(4)} | Investido: $${p.investedUSD} | Posição: $${p.positionValue.toFixed(2)} | Alvo: +$${targetProfit.toFixed(2)} \x1b[36m║\x1b[0m`);
        }
    }
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log('\x1b[36m║\x1b[0m  \x1b[33m📋 HISTÓRICO DE TRADES (Lucro Real)\x1b[0m                                                                                 \x1b[36m║\x1b[0m');
    const lastTrades = trades.slice(-5).reverse();
    if (lastTrades.length === 0) {
        console.log('\x1b[36m║\x1b[0m    Nenhum trade finalizado                                                                                         \x1b[36m║\x1b[0m');
    } else {
        for (const t of lastTrades) {
            const profitIcon = t.profitUSD >= 0 ? '✅' : '❌';
            console.log(`\x1b[36m║\x1b[0m    ${profitIcon} ${t.symbol.padEnd(8)} | ${t.side === 'BUY' ? 'COMPRA' : 'VENDA'} | Entrada: $${t.entryPrice.toFixed(4)} | Saída: $${t.exitPrice.toFixed(4)} | ${t.profitPercent.toFixed(2)}% | Lucro: $${t.profitUSD.toFixed(2)} | R$${t.profitBRL.toFixed(2)} \x1b[36m║\x1b[0m`);
        }
    }
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log('\x1b[36m║\x1b[0m  \x1b[33m📋 MENSAGENS (últimas 4)\x1b[0m                                                                                           \x1b[36m║\x1b[0m');
    const lastMessages = messageLog.slice(0, 4);
    for (const msg of lastMessages) {
        const shortMsg = msg.length > 85 ? msg.substring(0, 82) + '...' : msg;
        console.log(`\x1b[36m║\x1b[0m    ${shortMsg.padEnd(90)} \x1b[36m║\x1b[0m`);
    }
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log('\x1b[36m║\x1b[0m  \x1b[33m💡 COMANDOS:\x1b[0m                                                                                                      \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m     [A] Auto  |  [M] Manual  |  [Q] Sair                                                                             \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m     [U] +Entry  |  [D] -Entry  |  [↑] +Leve  |  [↓] -Leve  |  [→] +Target  |  [←] -Target  |  [S] Stop Loss        \x1b[36m║\x1b[0m');
    console.log('\x1b[36m╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝\x1b[0m');
}

async function mainLoop() {
    const results = await scanAll();
    for (const signal of results.slice(0, 5)) {
        if (signal.score >= 90) {
            const alertKey = `${signal.symbol}_${signal.timeframe}`;
            const now = Date.now();
            if (!lastAlert[alertKey] || now - lastAlert[alertKey] > 300000) {
                lastAlert[alertKey] = now;
                const hasPosition = positions.some(p => p.symbol === signal.symbol);
                if (!hasPosition && autoTrade) {
                    addInfo(`🚨 SINAL: ${signal.symbol} ${signal.timeframe} - ${signal.direction === 'BUY' ? 'COMPRA' : 'VENDA'} (${signal.signalType})`);
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
    if (key.name === 'q') { addInfo('Encerrando...'); process.exit(); }
    if (key.name === 'a') { autoTrade = true; addSuccess('MODO AUTOMÁTICO'); }
    if (key.name === 'm') { autoTrade = false; addWarning('MODO MANUAL'); }
    
    if (key.name === 'u') { FIXED_ENTRY_USD = Math.min(FIXED_ENTRY_USD + 10, 500); addSuccess(`💰 Entrada: $${FIXED_ENTRY_USD}`); }
    if (key.name === 'd') { FIXED_ENTRY_USD = Math.max(FIXED_ENTRY_USD - 10, 10); addSuccess(`💰 Entrada: $${FIXED_ENTRY_USD}`); }
    
    if (key.name === 'up') { MAX_LEVERAGE = Math.min(MAX_LEVERAGE + 1, 20); addSuccess(`⚡ Alavancagem: ${MAX_LEVERAGE}x`); }
    if (key.name === 'down') { MAX_LEVERAGE = Math.max(MAX_LEVERAGE - 1, 1); addSuccess(`⚡ Alavancagem: ${MAX_LEVERAGE}x`); }
    
    if (key.name === 'right') { TAKE_PROFIT_PERCENT = Math.min(TAKE_PROFIT_PERCENT + 50, 400); addSuccess(`🎯 Target: ${TAKE_PROFIT_PERCENT}%`); }
    if (key.name === 'left') { TAKE_PROFIT_PERCENT = Math.max(TAKE_PROFIT_PERCENT - 50, 50); addSuccess(`🎯 Target: ${TAKE_PROFIT_PERCENT}%`); }
    
    if (key.name === 's') { USE_STOP_LOSS = !USE_STOP_LOSS; addWarning(`Stop Loss: ${USE_STOP_LOSS ? 'ON' : 'OFF'}`); }
});

// ============================================
// INICIAR
// ============================================
addInfo('🦞 APEX IA - MODO AGRESSIVO INICIADO');
await syncServerTime();
await getExchangeInfo();
await getBalance();
connectWebSocket();
setInterval(mainLoop, 30000);
setInterval(drawUI, 1000);
drawUI();
