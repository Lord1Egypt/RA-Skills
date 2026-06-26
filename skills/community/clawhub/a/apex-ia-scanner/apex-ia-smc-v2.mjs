#!/usr/bin/env node

// ============================================
// SMC V2 - CORRIGIDO E EXPANDIDO
// ============================================

import WebSocket from 'ws';
import axios from 'axios';
import fs from 'fs';
import path from 'path';
import readline from 'readline';
import crypto from 'crypto';

const LOG_FILE = path.join(process.env.HOME, 'apex-ia-skill', 'operacoes-smc-v2.log');
let messageLog = [];

function addMessage(type, text) {
    const timestamp = new Date().toLocaleString('pt-BR');
    let color = '';
    switch(type) {
        case 'success': color = '\x1b[32m'; break;
        case 'error': color = '\x1b[31m'; break;
        case 'warning': color = '\x1b[33m'; break;
        default: color = '\x1b[36m'; break;
    }
    const logMessage = `[${timestamp}] ${text}`;
    messageLog.unshift(logMessage);
    if (messageLog.length > 100) messageLog.pop();
    fs.appendFileSync(LOG_FILE, logMessage + '\n');
    console.log(`${color}${logMessage}\x1b[0m`);
}

function addInfo(text) { addMessage('info', `📢 ${text}`); }
function addSuccess(text) { addMessage('success', `✅ ${text}`); }
function addWarning(text) { addMessage('warning', `⚠️ ${text}`); }
function addError(text) { addMessage('error', `❌ ${text}`); }

// ============================================
// LISTA EXPANDIDA DE PARES (sem pump & dump)
// ============================================
// Critérios de seleção:
// 1. Volume mínimo diário > $50M
// 2. Listado há mais de 6 meses
// 3. Não é meme coin recente
// 4. Correlação com BTC/ETH

const SYMBOLS = [
    // Top 10 por volume (seguros)
    'btcusdt', 'ethusdt', 'bnbusdt', 'solusdt', 'xrpusdt',
    'adausdt', 'dogeusdt', 'linkusdt', 'ltcusdt', 'avaxusdt',
    
    // Blue chips adicionais
    'maticusdt', 'atomusdt', 'dotusdt', 'uniusdt', 'aaveusdt',
    'crvusdt', 'snxusdt', 'mkrusdt', 'compusdt', 'ensusdt',
    
    // Layer 1 consolidados
    'nearusdt', 'ftmusdt', 'aptusdt', 'suiusdt', 'injxusdt',
    'seiusdt', 'taousdt', 'icpusdt', 'ethtoken', 'bchusdt',
    
    // Excluídos (pump & dump)
    // - pepusdt, flokiusdt, bonkusdt, wifusdt (meme coins recentes)
    // - trilhos, apostas, projetos novos sem histórico
];

// ============================================
// PDH/PDL MELHORADO
// ============================================
let pdhCache = {};

async function getPDHPDL(symbol) {
    const today = new Date().toDateString();
    const cacheKey = `${symbol}_${today}`;
    
    if (pdhCache[cacheKey]) return pdhCache[cacheKey];
    
    try {
        const response = await axios.get(`https://api.binance.com/api/v3/klines`, {
            params: { symbol: symbol.toUpperCase(), interval: '1d', limit: 3 }
        });
        
        const yesterday = response.data[response.data.length - 2];
        const pdh = parseFloat(yesterday[2]); // high
        const pdl = parseFloat(yesterday[3]); // low
        
        const result = { pdh, pdl };
        pdhCache[cacheKey] = result;
        return result;
    } catch (err) {
        return null;
    }
}

// ============================================
// DETECTOR DE ESTRUTURA (Choque)
// ============================================
function detectStructureBreak(candles, direction) {
    if (candles.length < 30) return false;
    
    const highs = candles.map(c => c.high);
    const lows = candles.map(c => c.low);
    
    if (direction === 'BUY') {
        // Tendência de alta: busca rompimento de topo
        const recentHighs = highs.slice(-10);
        const previousHighs = highs.slice(-25, -10);
        const recentMax = Math.max(...recentHighs);
        const previousMax = Math.max(...previousHighs);
        return recentMax > previousMax;
    } else {
        // Tendência de baixa: busca rompimento de fundo
        const recentLows = lows.slice(-10);
        const previousLows = lows.slice(-25, -10);
        const recentMin = Math.min(...recentLows);
        const previousMin = Math.min(...previousLows);
        return recentMin < previousMin;
    }
}

// ============================================
// DETECTOR DE FVG MELHORADO
// ============================================
function detectFVG(candles) {
    if (candles.length < 4) return null;
    
    const last3 = candles.slice(-3);
    const candle1 = last3[0];
    const candle2 = last3[1];
    const candle3 = last3[2];
    
    // FVG de ALTA (bullish) - gap para cima
    if (candle1.high < candle3.low) {
        return {
            type: 'BULLISH',
            entryPrice: candle1.high,
            stopPrice: candle2.low,
            direction: 'BUY'
        };
    }
    
    // FVG de BAIXA (bearish) - gap para baixo
    if (candle1.low > candle3.high) {
        return {
            type: 'BEARISH',
            entryPrice: candle1.low,
            stopPrice: candle2.high,
            direction: 'SELL'
        };
    }
    
    return null;
}

// ============================================
// FILTRO DE ATIVOS (evitar pump & dump)
// ============================================
async function isSafeSymbol(symbol) {
    try {
        // Verificar volume 24h
        const ticker = await axios.get(`https://api.binance.com/api/v3/ticker/24hr?symbol=${symbol.toUpperCase()}`);
        const volume = parseFloat(ticker.data.quoteVolume);
        
        // Rejeitar se volume < $10M (pouco líquido)
        if (volume < 10_000_000) {
            return false;
        }
        
        // Verificar volatilidade anormal (pump)
        const change = parseFloat(ticker.data.priceChangePercent);
        if (Math.abs(change) > 20) {
            addWarning(`${symbol.toUpperCase()} volátil demais (${change.toFixed(1)}%), ignorando`);
            return false;
        }
        
        return true;
    } catch (err) {
        return false;
    }
}

// ============================================
// SCANNER SMC MELHORADO
// ============================================
async function scanSMC() {
    const results = [];
    const safeSymbols = [];
    
    addInfo(`🔍 Filtrando ${SYMBOLS.length} pares...`);
    
    for (const symbol of SYMBOLS) {
        const isSafe = await isSafeSymbol(symbol);
        if (isSafe) safeSymbols.push(symbol);
    }
    
    addInfo(`✅ ${safeSymbols.length} pares seguros encontrados`);
    
    for (const symbol of safeSymbols.slice(0, 20)) { // Limite de 20 por scan
        try {
            // 1. Buscar PDH/PDL
            const pdhPdl = await getPDHPDL(symbol);
            if (!pdhPdl) continue;
            
            // 2. Buscar candles recentes
            const response = await axios.get(`https://api.binance.com/api/v3/klines`, {
                params: { symbol: symbol.toUpperCase(), interval: '15m', limit: 50 }
            });
            
            const currentPrice = parseFloat(response.data[response.data.length - 1][4]);
            const candles = response.data.map(k => ({
                high: parseFloat(k[2]),
                low: parseFloat(k[3]),
                close: parseFloat(k[4])
            }));
            
            // Distância para PDH/PDL (2% de tolerância)
            const distToPDH = Math.abs(currentPrice - pdhPdl.pdh) / pdhPdl.pdh * 100;
            const distToPDL = Math.abs(currentPrice - pdhPdl.pdl) / pdhPdl.pdl * 100;
            
            const nearPDH = distToPDH < 2.0;
            const nearPDL = distToPDL < 2.0;
            
            if (!nearPDH && !nearPDL) continue;
            
            // 3. Detectar choque
            const choqueBuy = detectStructureBreak(candles, 'BUY');
            const choqueSell = detectStructureBreak(candles, 'SELL');
            
            // 4. Detectar FVG
            const fvg = detectFVG(candles);
            
            // 5. Verificar alinhamento
            let signal = null;
            
            // Sinal de VENDA: perto do PDH + choque de baixa + FVG de baixa
            if (nearPDH && choqueSell && fvg && fvg.direction === 'SELL') {
                signal = {
                    symbol: symbol.toUpperCase(),
                    direction: 'SELL',
                    entryPrice: fvg.entryPrice,
                    stopPrice: fvg.stopPrice,
                    targetPrice: fvg.entryPrice - (fvg.stopPrice - fvg.entryPrice) * 2,
                    score: 95,
                    signalType: 'SMC_COMPLETO'
                };
            }
            
            // Sinal de COMPRA: perto do PDL + choque de alta + FVG de alta
            if (nearPDL && choqueBuy && fvg && fvg.direction === 'BUY') {
                signal = {
                    symbol: symbol.toUpperCase(),
                    direction: 'BUY',
                    entryPrice: fvg.entryPrice,
                    stopPrice: fvg.stopPrice,
                    targetPrice: fvg.entryPrice + (fvg.entryPrice - fvg.stopPrice) * 2,
                    score: 95,
                    signalType: 'SMC_COMPLETO'
                };
            }
            
            if (signal) {
                addSuccess(`🎯 SINAL SMC ENCONTRADO: ${signal.symbol} ${signal.direction} | RR 1:2`);
                results.push(signal);
            }
            
        } catch (err) {
            // Silencia erros
        }
    }
    
    return results;
}

// ============================================
// INTERFACE (simplificada)
// ============================================
function drawUI() {
    console.clear();
    const now = new Date();
    console.log('\x1b[36m╔════════════════════════════════════════════════════════════════════════════════════════════════════════╗\x1b[0m');
    console.log('\x1b[36m║\x1b[0m                    🦞 \x1b[33mAPEX IA - SMC V2 (PDH/PDL + CHOQUE + FVG)\x1b[0m                               \x1b[36m║\x1b[0m');
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log(`\x1b[36m║\x1b[0m  📅 ${now.toLocaleDateString('pt-BR')} | ${now.toLocaleTimeString('pt-BR')}                                                               \x1b[36m║\x1b[0m`);
    console.log(`\x1b[36m║\x1b[0m  📊 Buscando em ${SYMBOLS.length} pares | Filtro anti-pump: ✅                                         \x1b[36m║\x1b[0m`);
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log('\x1b[36m║\x1b[0m  \x1b[33m🔍 STATUS DO SMC V2\x1b[0m                                                                                 \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m    ✅ PDH/PDL: Buscando máxima/mínima do dia anterior                                             \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m    ✅ Choque: Detectando rompimento de estrutura                                               \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m    ✅ FVG: Identificando Fair Value Gaps                                                       \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m    ✅ Filtro anti-pump: Volume > $10M, volatilidade < 20%                                       \x1b[36m║\x1b[0m');
    console.log('\x1b[36m╚════════════════════════════════════════════════════════════════════════════════════════════════════════╝\x1b[0m');
    console.log('\n💡 [Q] Sair | [R] Forçar scan | Sistema aguardando sinais...\n');
}

// ============================================
// LOOP PRINCIPAL
// ============================================
let scanResults = [];

async function mainLoop() {
    addInfo(`🔍 Escaneando ${SYMBOLS.length} pares com filtro anti-pump...`);
    const results = await scanSMC();
    scanResults = results;
    
    if (results.length > 0) {
        addSuccess(`🎉 ${results.length} sinais SMC encontrados!`);
    } else {
        addInfo(`Nenhum sinal SMC no momento. Aguardando condições ideais...`);
    }
    
    drawUI();
}

// ============================================
// CONTROLE DE TECLADO
// ============================================
readline.emitKeypressEvents(process.stdin);
process.stdin.setRawMode(true);
process.stdin.on('keypress', (str, key) => {
    if (key.name === 'q') { console.clear(); process.exit(); }
    if (key.name === 'r') { mainLoop(); }
});

// ============================================
// INICIAR
// ============================================
console.clear();
addInfo('🦞 APEX IA - SMC V2 INICIADO');
addInfo(`📊 Buscando em ${SYMBOLS.length} pares`);
addInfo('✅ Filtro anti-pump & dump ativado');
addInfo('⏳ Aguardando condições SMC ideais...\n');

drawUI();
setInterval(mainLoop, 60000); // Scan a cada minuto
