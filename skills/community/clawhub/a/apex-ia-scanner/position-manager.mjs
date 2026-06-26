#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import axios from 'axios';

const SIGNALS_FILE = path.join(process.env.HOME, 'apex-ia-skill', 'sinais.json');
const RESULTS_FILE = path.join(process.env.HOME, 'apex-ia-skill', 'resultados.json');

// ============================================
// CARREGAR SINAIS ATIVOS
// ============================================
function loadSignals() {
    if (fs.existsSync(SIGNALS_FILE)) {
        return JSON.parse(fs.readFileSync(SIGNALS_FILE, 'utf-8'));
    }
    return [];
}

function saveSignals(signals) {
    fs.writeFileSync(SIGNALS_FILE, JSON.stringify(signals, null, 2));
}

// ============================================
// VERIFICAR POSIÇÕES ATIVAS
// ============================================
async function checkActivePositions() {
    const signals = loadSignals();
    const activeSignals = signals.filter(s => s.status === 'ativo' && s.direction === 'BUY');
    
    if (activeSignals.length === 0) {
        console.log(`📊 Nenhuma posição ativa no momento`);
        return;
    }
    
    console.log(`\n${'='.repeat(70)}`);
    console.log(`📊 VERIFICANDO ${activeSignals.length} POSIÇÕES ATIVAS`);
    console.log(`${'='.repeat(70)}`);
    
    for (const signal of activeSignals) {
        try {
            // Buscar preço atual
            const response = await axios.get(`https://api.binance.com/api/v3/ticker/price?symbol=${signal.symbol}`);
            const currentPrice = parseFloat(response.data.price);
            
            // Calcular resultado
            const entryPrice = signal.price;
            const currentProfit = ((currentPrice - entryPrice) / entryPrice) * 100;
            
            // Definir targets e stop (se não tiver, usar valores padrão)
            const target1 = signal.target1 || entryPrice * 1.015; // 1.5% de lucro
            const stopLoss = signal.stop || entryPrice * 0.99;    // 1% de perda
            
            let newStatus = signal.status;
            let result = null;
            let finalProfit = null;
            
            // Verificar se atingiu alvo ou stop
            if (currentPrice >= target1) {
                newStatus = 'fechado_lucro';
                result = '✅ TARGET1 ATINGIDO';
                finalProfit = ((target1 - entryPrice) / entryPrice) * 100;
            } else if (currentPrice <= stopLoss) {
                newStatus = 'fechado_prejuizo';
                result = '❌ STOP ATINGIDO';
                finalProfit = ((stopLoss - entryPrice) / entryPrice) * 100;
            }
            
            // Atualizar status
            if (newStatus !== signal.status) {
                signal.status = newStatus;
                signal.result = result;
                signal.finalProfit = finalProfit;
                signal.closedAt = new Date().toISOString();
                signal.closePrice = currentPrice;
                
                console.log(`\n📌 ${signal.symbol} - Sinal de ${new Date(signal.timestamp).toLocaleString()}`);
                console.log(`   Entrada: $${entryPrice.toFixed(2)}`);
                console.log(`   Saída: $${currentPrice.toFixed(2)}`);
                console.log(`   Resultado: ${result} (${finalProfit > 0 ? '+' : ''}${finalProfit.toFixed(2)}%)`);
            } else {
                // Mostrar status atual
                const profitColor = currentProfit > 0 ? '🟢' : (currentProfit < 0 ? '🔴' : '⚪');
                console.log(`${profitColor} ${signal.symbol} | Entrada: $${entryPrice.toFixed(2)} | Atual: $${currentPrice.toFixed(2)} | ${currentProfit > 0 ? '+' : ''}${currentProfit.toFixed(2)}%`);
            }
        } catch (err) {
            console.error(`Erro ao verificar ${signal.symbol}:`, err.message);
        }
    }
    
    saveSignals(signals);
    
    // Mostrar estatísticas
    showStats();
}

// ============================================
// ESTATÍSTICAS DO SISTEMA
// ============================================
function showStats() {
    const signals = loadSignals();
    const closedSignals = signals.filter(s => s.status === 'fechado_lucro' || s.status === 'fechado_prejuizo');
    const profitSignals = signals.filter(s => s.status === 'fechado_lucro');
    const lossSignals = signals.filter(s => s.status === 'fechado_prejuizo');
    const activeSignals = signals.filter(s => s.status === 'ativo');
    
    const totalClosed = closedSignals.length;
    const winRate = totalClosed > 0 ? (profitSignals.length / totalClosed) * 100 : 0;
    
    console.log(`\n${'='.repeat(70)}`);
    console.log(`📈 ESTATÍSTICAS DO SISTEMA`);
    console.log(`${'='.repeat(70)}`);
    console.log(`📊 Total de sinais: ${signals.length}`);
    console.log(`✅ Sinais com lucro: ${profitSignals.length}`);
    console.log(`❌ Sinais com prejuízo: ${lossSignals.length}`);
    console.log(`⏳ Posições ativas: ${activeSignals.length}`);
    console.log(`🎯 Taxa de acerto: ${winRate.toFixed(1)}%`);
    console.log(`${'='.repeat(70)}\n`);
}

// ============================================
// MOSTRAR ÚLTIMOS RESULTADOS
// ============================================
function showLastResults() {
    const signals = loadSignals();
    const lastSignals = signals.slice(-10).reverse();
    
    console.log(`\n📋 ÚLTIMOS 10 SINAIS:`);
    console.log(`${'='.repeat(70)}`);
    
    for (const s of lastSignals) {
        const date = new Date(s.timestamp).toLocaleString();
        const statusIcon = s.status === 'fechado_lucro' ? '✅' : (s.status === 'fechado_prejuizo' ? '❌' : '⏳');
        const profit = s.finalProfit ? `${s.finalProfit > 0 ? '+' : ''}${s.finalProfit.toFixed(2)}%` : '---';
        console.log(`${statusIcon} ${s.symbol} (${date}) | ${s.direction} | Score: ${s.score || '-'} | ${profit}`);
    }
    console.log(`${'='.repeat(70)}\n`);
}

// ============================================
// EXECUTAR
// ============================================
console.clear();
console.log('\n🦞 APEX IA - GERENCIADOR DE POSIÇÕES');
console.log('📊 Monitorando resultados dos sinais\n');

// Verificar posições agora
await checkActivePositions();
showLastResults();

// Continuar verificando a cada 5 minutos
console.log('⏳ Verificando automaticamente a cada 5 minutos...\n');

setInterval(async () => {
    console.log(`\n🔍 [${new Date().toLocaleString()}] Verificando posições...`);
    await checkActivePositions();
    showLastResults();
}, 5 * 60 * 1000);

process.on('SIGINT', () => {
    console.log('\n\n👋 Desligando...\n');
    process.exit();
});
