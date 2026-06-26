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
const LOG_FILE = path.join(process.env.HOME, 'apex-ia-skill', 'operacoes-smc.log');
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
// CONFIGURAÇÕES SMC
// ============================================
const SYMBOLS = ['btcusdt', 'ethusdt', 'bchusdt', 'solusdt', 'adausdt', 'ltcusdt', 'linkusdt', 'xrpusdt', 'dogeusdt', 'avaxusdt'];

let FIXED_ENTRY_USD = 30;
let MAX_LEVERAGE = 20;
let RISK_REWARD_RATIO = 2;  // Alvo = 2x risco (RR 1:2)
let USE_STOP_LOSS = true;    // SMC usa stop loss!

let autoTrade = true;
let equity = 7080.58;
let positions = [];
let trades = [];
let lastPrices = {};
let scanResults = [];
let candles = {};
let dailyCandles = {};
let lastAlert = {};
let processedSignals = new Set();
let wsConnected = false;
let exchangeInfo = null;
let symbolPrecisions = {};

// ============================================
// LIMITE DE POSIÇÕES
// ============================================
const MAX_POSITIONS = 7;

// ============================================
// ESTRUTURAS SMC
// ============================================
let pdhPdlCache = {};

async function getDailyPDHPDL(symbol) {
    const today = new Date().toDateString();
    const cacheKey = `${symbol}_${today}`;
    
    if (pdhPdlCache[cacheKey]) {
        return pdhPdlCache[cacheKey];
    }
    
    try {
        // Buscar candles diários
        const response = await axios.get(`https://api.binance.com/api/v3/klines`, {
            params: { symbol: symbol.toUpperCase(), interval: '1d', limit: 2 }
        });
        
        const yesterday = response.data[0];
        const pdh = parseFloat(yesterday[2]); // high do dia anterior
        const pdl = parseFloat(yesterday[3]); // low do dia anterior
        
        const result = { pdh, pdl, date: today };
        pdhPdlCache[cacheKey] = result;
        
        addInfo(`📊 ${symbol}: PDH=$${pdh.toFixed(4)} | PDL=$${pdl.toFixed(4)}`);
        return result;
    } catch (err) {
        addError(`Erro ao buscar PDH/PDL para ${symbol}`);
        return null;
    }
}

// ============================================
// DETECTOR DE CHOQUE (Change of Character)
// ============================================
function detectChoque(candles, direction) {
    if (candles.length < 20) return false;
    
    const closes = candles.map(c => c.close);
    const highs = candles.map(c => c.high);
    const lows = candles.map(c => c.low);
    
    if (direction === 'BUY') {
        // Tendência de alta: precisa romper o último fundo válido
        let lastValidLow = Infinity;
        for (let i = candles.length - 10; i < candles.length; i++) {
            if (lows[i] < lastValidLow) {
                lastValidLow = lows[i];
            }
        }
        const currentLow = lows[lows.length - 1];
        return currentLow < lastValidLow;
    } else {
        // Tendência de baixa: precisa romper o último topo válido
        let lastValidHigh = -Infinity;
        for (let i = candles.length - 10; i < candles.length; i++) {
            if (highs[i] > lastValidHigh) {
                lastValidHigh = highs[i];
            }
        }
        const currentHigh = highs[highs.length - 1];
        return currentHigh > lastValidHigh;
    }
}

// ============================================
// DETECTOR DE FVG (Fair Value Gap)
// ============================================
function detectFVG(candles) {
    if (candles.length < 3) return null;
    
    const last3 = candles.slice(-3);
    const candle1 = last3[0];
    const candle2 = last3[1];
    const candle3 = last3[2];
    
    // FVG de BAIXA (gap para baixo) - sinal de VENDA
    if (candle1.low > candle3.high) {
        return {
            type: 'BEARISH_FVG',
            entryLow: candle3.high,
            entryHigh: candle1.low,
            stopPrice: candle2.high,
            direction: 'SELL'
        };
    }
    
    // FVG de ALTA (gap para cima) - sinal de COMPRA
    if (candle1.high < candle3.low) {
        return {
            type: 'BULLISH_FVG',
            entryLow: candle1.high,
            entryHigh: candle3.low,
            stopPrice: candle2.low,
            direction: 'BUY'
        };
    }
    
    return null;
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

function getQuantityPrecision(symbol) {
    if (!exchangeInfo) return 3;
    const symbolInfo = exchangeInfo.symbols.find(s => s.symbol === symbol.toUpperCase());
    if (!symbolInfo) return 3;
    const lotSizeFilter = symbolInfo.filters.find(f => f.filterType === 'LOT_SIZE');
    if (lotSizeFilter) {
        const stepSize = parseFloat(lotSizeFilter.stepSize);
        return stepSize.toString().split('.')[1]?.length || 3;
    }
    return 3;
}

function formatQuantity(quantity, symbol) {
    const precision = getQuantityPrecision(symbol);
    return parseFloat(quantity.toFixed(precision));
}

async function getExchangeInfo() {
    if (exchangeInfo) return exchangeInfo;
    try {
        const response = await axios.get(`${BASE_URL}/fapi/v1/exchangeInfo`);
        exchangeInfo = response.data;
        addSuccess(`Informações de mercado carregadas`);
        return exchangeInfo;
    } catch (err) {
        addError(`Erro ao carregar informações: ${err.message}`);
        return null;
    }
}

async function openPosition(symbol, side, quantity, entryPrice, stopPrice, targetPrice) {
    if (positions.length >= MAX_POSITIONS) {
        addWarning(`Limite de ${MAX_POSITIONS} posições atingido.`);
        return null;
    }
    
    const existingPosition = positions.find(p => p.symbol === symbol.toUpperCase());
    if (existingPosition) {
        addWarning(`Posição já existe para ${symbol}`);
        return null;
    }
    
    await setLeverage(symbol, MAX_LEVERAGE);
    
    const adjustedQuantity = formatQuantity(quantity, symbol);
    
    addInfo(`📊 SMC: Abrindo ${side} em ${symbol}`);
    addInfo(`   Entrada: $${entryPrice.toFixed(4)} | Quantidade: ${adjustedQuantity}`);
    addInfo(`   Stop: $${stopPrice.toFixed(4)} | Target: $${targetPrice.toFixed(4)}`);
    addInfo(`   Risco: $${(positionValue * 0.01).toFixed(2)} | Retorno: $${(positionValue * 0.02).toFixed(2)}`);
    
    const order = await binanceRequest('POST', '/fapi/v1/order', {
        symbol: symbol.toUpperCase(),
        side: side.toUpperCase(),
        type: 'MARKET',
        quantity: adjustedQuantity
    }, true);
    
    if (order && !order.error && order.orderId) {
        // Stop Loss
        const stopSide = side === 'BUY' ? 'SELL' : 'BUY';
        await binanceRequest('POST', '/fapi/v1/order', {
            symbol: symbol.toUpperCase(),
            side: stopSide,
            type: 'STOP_MARKET',
            quantity: adjustedQuantity,
            stopPrice: stopPrice.toFixed(2),
            reduceOnly: 'true'
        }, true);
        
        // Take Profit
        await binanceRequest('POST', '/fapi/v1/order', {
            symbol: symbol.toUpperCase(),
            side: stopSide,
            type: 'TAKE_PROFIT_MARKET',
            quantity: adjustedQuantity,
            stopPrice: targetPrice.toFixed(2),
            reduceOnly: 'true'
        }, true);
        
        const positionValue = FIXED_ENTRY_USD * MAX_LEVERAGE;
        
        positions.push({
            symbol: symbol.toUpperCase(),
            side: side,
            quantity: adjustedQuantity,
            entryPrice: entryPrice,
            stopPrice: stopPrice,
            targetPrice: targetPrice,
            leverage: MAX_LEVERAGE,
            investedUSD: FIXED_ENTRY_USD,
            positionValue: positionValue,
            openedAt: new Date().toISOString()
        });
        
        addSuccess(`${symbol} ${side === 'BUY' ? 'COMPRA' : 'VENDA'} SMC aberta!`);
        addInfo(`   Posições atuais: ${positions.length}/${MAX_POSITIONS}`);
        
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
            investedUSD: position.investedUSD,
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
        return { order, profit: profitUSD };
    }
    return null;
}

async function monitorPositions() {
    for (const position of positions) {
        const currentPrice = await getPrice(position.symbol);
        if (!currentPrice) continue;
        
        if (position.side === 'BUY' && currentPrice >= position.targetPrice) {
            await closePosition(position.symbol, '🎯 TARGET SMC');
        } else if (position.side === 'SELL' && currentPrice <= position.targetPrice) {
            await closePosition(position.symbol, '🎯 TARGET SMC');
        }
    }
}

// ============================================
// SCANNER SMC
// ============================================
async function scanSMC() {
    const results = [];
    
    for (const symbol of SYMBOLS) {
        try {
            // 1. Buscar PDH/PDL
            const pdhPdl = await getDailyPDHPDL(symbol);
            if (!pdhPdl) continue;
            
            // 2. Buscar candles de 15m para análise
            const response = await axios.get(`https://api.binance.com/api/v3/klines`, {
                params: { symbol: symbol.toUpperCase(), interval: '15m', limit: 100 }
            });
            
            const candles15m = response.data.map(k => ({
                open: parseFloat(k[1]),
                high: parseFloat(k[2]),
                low: parseFloat(k[3]),
                close: parseFloat(k[4]),
                time: k[0]
            }));
            
            const currentPrice = candles15m[candles15m.length - 1].close;
            const nearPDH = Math.abs(currentPrice - pdhPdl.pdh) / pdhPdl.pdh < 0.01;
            const nearPDL = Math.abs(currentPrice - pdhPdl.pdl) / pdhPdl.pdl < 0.01;
            
            if (!nearPDH && !nearPDL) continue;
            
            // 3. Detecta CHOQUE
            const choqueBuy = detectChoque(candles15m, 'BUY');
            const choqueSell = detectChoque(candles15m, 'SELL');
            
            if (!choqueBuy && !choqueSell) continue;
            
            // 4. Detecta FVG
            const fvg = detectFVG(candles15m);
            if (!fvg) continue;
            
            // 5. Verifica alinhamento
            let direction = null;
            if (nearPDL && choqueBuy && fvg.direction === 'BUY') {
                direction = 'BUY';
            } else if (nearPDH && choqueSell && fvg.direction === 'SELL') {
                direction = 'SELL';
            }
            
            if (!direction) continue;
            
            // 6. Calcular entrada, stop e target
            const entryPrice = fvg.entryHigh;
            const stopPrice = fvg.stopPrice;
            const riskAmount = Math.abs(entryPrice - stopPrice);
            const targetPrice = direction === 'BUY' 
                ? entryPrice + (riskAmount * RISK_REWARD_RATIO)
                : entryPrice - (riskAmount * RISK_REWARD_RATIO);
            
            results.push({
                symbol: symbol.toUpperCase(),
                direction,
                entryPrice,
                stopPrice,
                targetPrice,
                riskReward: RISK_REWARD_RATIO,
                score: 95,
                signalType: 'SMC',
                signalId: `${symbol}_smc_${Date.now()}`
            });
            
        } catch (err) {
            // Silencia erros
        }
    }
    
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
    
    const positionSize = FIXED_ENTRY_USD * MAX_LEVERAGE;
    let quantity = positionSize / signal.entryPrice;
    const adjustedQuantity = formatQuantity(quantity, signal.symbol);
    
    addInfo(`🚨 SINAL SMC DETECTADO: ${signal.symbol} ${signal.direction === 'BUY' ? 'COMPRA' : 'VENDA'}`);
    addInfo(`   Entrada: $${signal.entryPrice.toFixed(4)} | Stop: $${signal.stopPrice.toFixed(4)}`);
    addInfo(`   Target: $${signal.targetPrice.toFixed(4)} | RR: 1:${signal.riskReward}`);
    addInfo(`   Investimento: $${FIXED_ENTRY_USD} | Alavancagem: ${MAX_LEVERAGE}x | Posição: $${positionSize.toFixed(2)}`);
    
    const order = await openPosition(
        signal.symbol, 
        signal.direction, 
        quantity, 
        signal.entryPrice, 
        signal.stopPrice, 
        signal.targetPrice
    );
    
    if (order) {
        processedSignals.add(signal.signalId);
        addSuccess(`✅ TRADE SMC ${signal.symbol} EXECUTADO!`);
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
    console.log('\x1b[36m║\x1b[0m                              🦞 \x1b[33mAPEX IA - ESTRATÉGIA SMC (PDH/PDL + CHOQUE + FVG)\x1b[0m                           \x1b[36m║\x1b[0m');
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log(`\x1b[36m║\x1b[0m  📅 ${now.toLocaleDateString('pt-BR')} | ${now.toLocaleTimeString('pt-BR')}                                                                        \x1b[36m║\x1b[0m`);
    console.log(`\x1b[36m║\x1b[0m  💰 Entrada: \x1b[33m$${FIXED_ENTRY_USD}\x1b[0m | ⚡ Alavancagem: ${MAX_LEVERAGE}x | 🎯 RR: 1:${RISK_REWARD_RATIO} | 🛑 Stop: ON | 🤖: ${autoTrade ? 'AUTOMÁTICO' : 'MANUAL'} | 🔌 WS: ${wsConnected ? '✅' : '❌'} \x1b[36m║\x1b[0m`);
    console.log(`\x1b[36m║\x1b[0m  📊 Posições: ${positions.length}/${MAX_POSITIONS} | 💰 Saldo: $${equity.toFixed(2)}                                                                 \x1b[36m║\x1b[0m`);
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log('\x1b[36m║\x1b[0m  \x1b[33m🏆 SINAIS SMC DETECTADOS\x1b[0m                                                                                              \x1b[36m║\x1b[0m');
    const top3 = scanResults.slice(0, 4);
    if (top3.length === 0) {
        console.log('\x1b[36m║\x1b[0m    Aguardando sinais SMC... (PDH/PDL + Choque + FVG)                                                                  \x1b[36m║\x1b[0m');
    } else {
        for (const s of top3) {
            const arrow = s.direction === 'BUY' ? '🟢 ▲ COMPRA SMC' : '🔴 ▼ VENDA SMC';
            const jaTem = positions.some(p => p.symbol === s.symbol);
            const status = jaTem ? '⚠️ IGNORAR' : '✅ LIVRE';
            console.log(`\x1b[36m║\x1b[0m    ${arrow.padEnd(16)} ${s.symbol.padEnd(8)} | Entrada: $${s.entryPrice.toFixed(4)} | Stop: $${s.stopPrice.toFixed(4)} | Target: $${s.targetPrice.toFixed(4)} | ${status.padEnd(10)} \x1b[36m║\x1b[0m`);
        }
    }
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log('\x1b[36m║\x1b[0m  \x1b[33m📊 POSIÇÕES ABERTAS (SMC)\x1b[0m                                                                                           \x1b[36m║\x1b[0m');
    if (positions.length === 0) {
        console.log('\x1b[36m║\x1b[0m    Nenhuma posição aberta                                                                                          \x1b[36m║\x1b[0m');
    } else {
        for (const p of positions) {
            const sideIcon = p.side === 'BUY' ? '🟢 COMPRA' : '🔴 VENDA';
            const riskAmount = Math.abs(p.entryPrice - p.stopPrice);
            const targetProfit = p.positionValue * (RISK_REWARD_RATIO * 0.01);
            console.log(`\x1b[36m║\x1b[0m    ${p.symbol.padEnd(8)} ${sideIcon.padEnd(10)} | Entrada: $${p.entryPrice.toFixed(4)} | Stop: $${p.stopPrice.toFixed(4)} | Target: $${p.targetPrice.toFixed(4)} | Alvo: +$${targetProfit.toFixed(2)} \x1b[36m║\x1b[0m`);
        }
    }
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log('\x1b[36m║\x1b[0m  \x1b[33m📋 HISTÓRICO DE TRADES SMC\x1b[0m                                                                                       \x1b[36m║\x1b[0m');
    const lastTrades = trades.slice(-5).reverse();
    if (lastTrades.length === 0) {
        console.log('\x1b[36m║\x1b[0m    Nenhum trade finalizado                                                                                         \x1b[36m║\x1b[0m');
    } else {
        for (const t of lastTrades) {
            const profitIcon = t.profitUSD >= 0 ? '✅' : '❌';
            console.log(`\x1b[36m║\x1b[0m    ${profitIcon} ${t.symbol.padEnd(8)} | ${t.side === 'BUY' ? 'COMPRA' : 'VENDA'} | ${t.profitPercent.toFixed(2)}% | Lucro: $${t.profitUSD.toFixed(2)} | R$${t.profitBRL.toFixed(2)} \x1b[36m║\x1b[0m`);
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
    console.log('\x1b[36m║\x1b[0m  \x1b[33m💡 COMANDOS SMC:\x1b[0m                                                                                                  \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m     [A] Auto  |  [M] Manual  |  [Q] Sair                                                                             \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m     [U] +Entry  |  [D] -Entry  |  [↑] +Leve  |  [↓] -Leve  |  [→] +RR  |  [←] -RR                                    \x1b[36m║\x1b[0m');
    console.log('\x1b[36m╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝\x1b[0m');
}

async function mainLoop() {
    const results = await scanSMC();
    for (const signal of results) {
        const alertKey = `${signal.symbol}_smc`;
        const now = Date.now();
        if (!lastAlert[alertKey] || now - lastAlert[alertKey] > 300000) {
            lastAlert[alertKey] = now;
            const hasPosition = positions.some(p => p.symbol === signal.symbol);
            if (!hasPosition && autoTrade) {
                addInfo(`🚨 SINAL SMC: ${signal.symbol} - ${signal.direction === 'BUY' ? 'COMPRA' : 'VENDA'} (PDH/PDL + Choque + FVG)`);
                await executeTrade(signal);
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
    if (key.name === 'a') { autoTrade = true; addSuccess('MODO AUTOMÁTICO SMC'); }
    if (key.name === 'm') { autoTrade = false; addWarning('MODO MANUAL SMC'); }
    
    if (key.name === 'u') { FIXED_ENTRY_USD = Math.min(FIXED_ENTRY_USD + 10, 500); addSuccess(`💰 Entrada: $${FIXED_ENTRY_USD}`); }
    if (key.name === 'd') { FIXED_ENTRY_USD = Math.max(FIXED_ENTRY_USD - 10, 10); addSuccess(`💰 Entrada: $${FIXED_ENTRY_USD}`); }
    
    if (key.name === 'up') { MAX_LEVERAGE = Math.min(MAX_LEVERAGE + 1, 20); addSuccess(`⚡ Alavancagem: ${MAX_LEVERAGE}x`); }
    if (key.name === 'down') { MAX_LEVERAGE = Math.max(MAX_LEVERAGE - 1, 1); addSuccess(`⚡ Alavancagem: ${MAX_LEVERAGE}x`); }
    
    if (key.name === 'right') { RISK_REWARD_RATIO = Math.min(RISK_REWARD_RATIO + 0.5, 5); addSuccess(`🎯 Risk/Reward: 1:${RISK_REWARD_RATIO}`); }
    if (key.name === 'left') { RISK_REWARD_RATIO = Math.max(RISK_REWARD_RATIO - 0.5, 1); addSuccess(`🎯 Risk/Reward: 1:${RISK_REWARD_RATIO}`); }
});

// ============================================
// INICIAR
// ============================================
addInfo('🦞 APEX IA - ESTRATÉGIA SMC INICIADA');
addInfo('📊 Estratégia: PDH/PDL + Choque + FVG');
await syncServerTime();
await getExchangeInfo();
await getBalance();
connectWebSocket();
setInterval(mainLoop, 60000); // SMC escaneia a cada minuto
setInterval(drawUI, 1000);
drawUI();
