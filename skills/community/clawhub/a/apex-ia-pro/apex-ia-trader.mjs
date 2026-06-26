#!/usr/bin/env node

import WebSocket from 'ws';
import axios from 'axios';
import fs from 'fs';
import path from 'path';
import readline from 'readline';
import crypto from 'crypto';

// ============================================
// CONFIGURAÇÕES BINANCE DEMO
// ============================================
// Coloque suas chaves DEMO aqui:
const API_KEY = 'Dq0vl5xeDxwQKMBwoJT5A9yxsJiW8hbXyVO7831c4xbI0N1tfiQjsTf1ZKsSVIXL';
const API_SECRET = '1kVF6XZuV5rVnKyIiAjbLTNcN50tQZEI8M5p90piOblTOl4W19rpgIeZMRzDlBBb';
const USE_DEMO = true;  // true = conta demo, false = conta real

// URLs
const BASE_URL = USE_DEMO ? 'https://testnet.binancefuture.com' : 'https://fapi.binance.com';

// Limites de risco
const MAX_POSITION_SIZE_USD = 500;  // Máximo por trade
const MAX_DAILY_LOSS_USD = 200;     // Stop diário
const MAX_LEVERAGE = 10;             // Alavancagem máxima

// Estado do trader
let dailyLoss = 0;
let positions = [];
let trades = [];
let equity = 0;

// ============================================
// FUNÇÕES DA BINANCE DEMO
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
        const response = await axios({
            method,
            url,
            headers: {
                'X-MBX-APIKEY': API_KEY,
                'Content-Type': 'application/json'
            }
        });
        return response.data;
    } catch (err) {
        console.error(`❌ Erro na requisição: ${err.message}`);
        return null;
    }
}

// Obter saldo da conta
async function getBalance() {
    const data = await binanceRequest('GET', '/fapi/v2/account', {}, true);
    if (data && data.assets) {
        const usdtAsset = data.assets.find(a => a.asset === 'USDT');
        if (usdtAsset) {
            equity = parseFloat(usdtAsset.walletBalance);
            return equity;
        }
    }
    return 0;
}

// Obter preço atual
async function getPrice(symbol) {
    try {
        const response = await axios.get(`${BASE_URL}/fapi/v1/ticker/price?symbol=${symbol}`);
        return parseFloat(response.data.price);
    } catch (err) {
        return null;
    }
}

// Abrir posição
async function openPosition(symbol, side, quantity, stopLoss, takeProfit) {
    const params = {
        symbol,
        side: side.toUpperCase(),
        type: 'MARKET',
        quantity: quantity.toFixed(3)
    };
    
    const order = await binanceRequest('POST', '/fapi/v1/order', params, true);
    
    if (order && order.orderId) {
        // Adicionar stop loss e take profit
        if (stopLoss) {
            await binanceRequest('POST', '/fapi/v1/order', {
                symbol,
                side: side === 'BUY' ? 'SELL' : 'BUY',
                type: 'STOP_MARKET',
                quantity: quantity.toFixed(3),
                stopPrice: stopLoss.toFixed(2),
                price: stopLoss.toFixed(2)
            }, true);
        }
        
        if (takeProfit) {
            await binanceRequest('POST', '/fapi/v1/order', {
                symbol,
                side: side === 'BUY' ? 'SELL' : 'BUY',
                type: 'TAKE_PROFIT_MARKET',
                quantity: quantity.toFixed(3),
                stopPrice: takeProfit.toFixed(2),
                price: takeProfit.toFixed(2)
            }, true);
        }
        
        positions.push({
            symbol,
            side,
            quantity,
            entryPrice: parseFloat(order.price),
            stopLoss,
            takeProfit,
            openedAt: new Date().toISOString()
        });
        
        return order;
    }
    return null;
}

// Fechar posição
async function closePosition(symbol) {
    // Buscar posição aberta
    const position = positions.find(p => p.symbol === symbol);
    if (!position) return null;
    
    const side = position.side === 'BUY' ? 'SELL' : 'BUY';
    const order = await binanceRequest('POST', '/fapi/v1/order', {
        symbol,
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
            symbol,
            side: position.side,
            entryPrice: position.entryPrice,
            exitPrice: currentPrice,
            quantity: position.quantity,
            profit,
            closedAt: new Date().toISOString()
        });
        
        positions = positions.filter(p => p.symbol !== symbol);
        return { order, profit };
    }
    return null;
}

// ============================================
// ESTRATÉGIA DE TRADE BASEADA NO APEX IA
// ============================================
let lastTradeTime = {};
let dailyTrades = 0;

async function executeTradeSignal(signal) {
    const now = Date.now();
    const symbol = signal.symbol;
    
    // Evitar trades repetidos no mesmo símbolo (cooldown de 5 min)
    if (lastTradeTime[symbol] && now - lastTradeTime[symbol] < 300000) {
        return { executed: false, reason: 'Cooldown ativo' };
    }
    
    // Verificar stop diário
    if (dailyLoss >= MAX_DAILY_LOSS_USD) {
        console.log(`🛑 Stop diário atingido: $${dailyLoss.toFixed(2)}`);
        return { executed: false, reason: 'Stop diário' };
    }
    
    // Verificar saldo
    const balance = await getBalance();
    if (balance < 50) {
        console.log(`❌ Saldo insuficiente: $${balance.toFixed(2)}`);
        return { executed: false, reason: 'Saldo insuficiente' };
    }
    
    // Calcular tamanho da posição (1% do capital por trade)
    const riskAmount = balance * 0.01;
    const maxRiskAmount = Math.min(riskAmount, MAX_POSITION_SIZE_USD);
    const currentPrice = await getPrice(symbol);
    const stopDistance = Math.abs(currentPrice - signal.stop) / currentPrice;
    const quantity = (maxRiskAmount / currentPrice) / (stopDistance + 0.01);
    const finalQuantity = Math.min(quantity, maxRiskAmount / currentPrice);
    
    // Verificar se o sinal está ativo ainda
    if (signal.score >= 90) {
        // Abrir posição
        const order = await openPosition(
            symbol,
            signal.direction === 'BUY' ? 'BUY' : 'SELL',
            finalQuantity,
            signal.stop,
            signal.target1
        );
        
        if (order) {
            lastTradeTime[symbol] = now;
            dailyTrades++;
            
            console.log(`\n✅ TRADE EXECUTADO!`);
            console.log(`   ${symbol} - ${signal.direction === 'BUY' ? 'COMPRA' : 'VENDA'}`);
            console.log(`   Quantidade: ${finalQuantity.toFixed(4)}`);
            console.log(`   Entrada: $${currentPrice.toFixed(2)}`);
            console.log(`   Stop: $${signal.stop.toFixed(2)}`);
            console.log(`   T1: $${signal.target1?.toFixed(2) || (currentPrice * 1.02).toFixed(2)}`);
            
            return { executed: true, order };
        }
    }
    
    return { executed: false, reason: 'Score insuficiente' };
}

// ============================================
// MONITORAMENTO DE POSIÇÕES
// ============================================
async function monitorPositions() {
    for (const position of positions) {
        const currentPrice = await getPrice(position.symbol);
        if (!currentPrice) continue;
        
        const profit = position.side === 'BUY'
            ? (currentPrice - position.entryPrice) * position.quantity
            : (position.entryPrice - currentPrice) * position.quantity;
        
        const profitPercent = (profit / (position.entryPrice * position.quantity)) * 100;
        
        // Verificar se atingiu target
        if (position.takeProfit && currentPrice >= position.takeProfit) {
            const closed = await closePosition(position.symbol);
            if (closed) {
                dailyLoss -= closed.profit;
                console.log(`🎯 TARGET ATINGIDO! ${position.symbol} - Lucro: $${closed.profit.toFixed(2)}`);
            }
        }
        // Verificar stop loss
        else if (position.stopLoss && currentPrice <= position.stopLoss) {
            const closed = await closePosition(position.symbol);
            if (closed) {
                dailyLoss += Math.abs(closed.profit);
                console.log(`🛑 STOP ATINGIDO! ${position.symbol} - Perda: $${Math.abs(closed.profit).toFixed(2)}`);
            }
        }
    }
}

// ============================================
// INTEGRAÇÃO COM O APEX IA
// ============================================
// Esta função será chamada quando o APEX IA detectar um sinal
async function onSignalDetected(signal) {
    console.log(`\n🚨 NOVO SINAL DETECTADO: ${signal.symbol} - ${signal.direction === 'BUY' ? 'COMPRA' : 'VENDA'} (Score: ${signal.score}%)`);
    
    if (signal.score >= 90) {
        const result = await executeTradeSignal(signal);
        if (result.executed) {
            console.log(`✅ Trade executado automaticamente!`);
        } else {
            console.log(`⏸️ Trade não executado: ${result.reason}`);
        }
    }
}

// ============================================
// INTERFACE DO TRADER
// ============================================
function drawTraderUI() {
    console.clear();
    console.log('\x1b[36m╔════════════════════════════════════════════════════════════════════╗\x1b[0m');
    console.log('\x1b[36m║\x1b[0m                    🦞 APEX IA - TRADER AUTOMÁTICO                      \x1b[36m║\x1b[0m');
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════╣\x1b[0m');
    console.log(`\x1b[36m║\x1b[0m  📊 Conta: ${USE_DEMO ? 'DEMO (Testnet)' : 'REAL'}                                     \x1b[36m║\x1b[0m`);
    console.log(`\x1b[36m║\x1b[0m  💰 Saldo: $${equity.toFixed(2)}                                                    \x1b[36m║\x1b[0m`);
    console.log(`\x1b[36m║\x1b[0m  📈 Trades hoje: ${dailyTrades} | Perda diária: $${dailyLoss.toFixed(2)}                               \x1b[36m║\x1b[0m`);
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════╣\x1b[0m');
    
    // Posições abertas
    console.log('\x1b[36m║\x1b[0m  \x1b[33m📊 POSIÇÕES ABERTAS\x1b[0m                                                \x1b[36m║\x1b[0m');
    if (positions.length === 0) {
        console.log(`\x1b[36m║\x1b[0m    Nenhuma posição aberta                                             \x1b[36m║\x1b[0m`);
    } else {
        for (const p of positions) {
            console.log(`\x1b[36m║\x1b[0m    ${p.symbol} ${p.side === 'BUY' ? '🟢 COMPRA' : '🔴 VENDA'} | Entrada: $${p.entryPrice.toFixed(2)}       \x1b[36m║\x1b[0m`);
        }
    }
    
    console.log('\x1b[36m╠════════════════════════════════════════════════════════════════════╣\x1b[0m');
    
    // Últimos trades
    console.log('\x1b[36m║\x1b[0m  \x1b[33m📋 ÚLTIMOS TRADES\x1b[0m                                                  \x1b[36m║\x1b[0m');
    const lastTrades = trades.slice(-5).reverse();
    if (lastTrades.length === 0) {
        console.log(`\x1b[36m║\x1b[0m    Nenhum trade ainda                                                  \x1b[36m║\x1b[0m`);
    } else {
        for (const t of lastTrades) {
            const profitIcon = t.profit >= 0 ? '✅' : '❌';
            console.log(`\x1b[36m║\x1b[0m    ${profitIcon} ${t.symbol} | Lucro: ${t.profit >= 0 ? '+' : ''}$${t.profit.toFixed(2)}                                  \x1b[36m║\x1b[0m`);
        }
    }
    
    console.log('\x1b[36m╚════════════════════════════════════════════════════════════════════╝\x1b[0m');
    console.log('\n\x1b[33m💡 [Q] Sair | [R] Reiniciar | [M] Modo Manual | [A] Automático\x1b[0m\n');
}

// ============================================
// LOOP PRINCIPAL
// ============================================
let autoMode = true;

setInterval(async () => {
    if (autoMode) {
        await getBalance();
        await monitorPositions();
        drawTraderUI();
    }
}, 2000);

// ============================================
// INICIAR
// ============================================
console.clear();
console.log('\n🦞 APEX IA - TRADER AUTOMÁTICO');
console.log('📊 Conectando à Binance Demo...\n');

await getBalance();
drawTraderUI();

// Keyboard input
readline.emitKeypressEvents(process.stdin);
process.stdin.setRawMode(true);
process.stdin.on('keypress', (str, key) => {
    if (key.name === 'q') {
        console.clear();
        console.log('\n👋 Encerrando trader...\n');
        process.exit();
    } else if (key.name === 'm') {
        autoMode = false;
        console.log('\n📋 Modo manual ativado. Pressione [A] para automático.\n');
    } else if (key.name === 'a') {
        autoMode = true;
        console.log('\n🤖 Modo automático ativado.\n');
    }
});

// Exportar função para integração com APEX IA
export { onSignalDetected, executeTradeSignal };
