#!/usr/bin/env node

import fs from 'fs';
import path from 'path';

// Arquivo onde os sinais serão salvos
const SIGNALS_FILE = path.join(process.env.HOME, 'apex-ia-skill', 'sinais.json');
const RESULTS_FILE = path.join(process.env.HOME, 'apex-ia-skill', 'resultados.json');

// Carregar sinais existentes
function loadSignals() {
  if (fs.existsSync(SIGNALS_FILE)) {
    return JSON.parse(fs.readFileSync(SIGNALS_FILE, 'utf-8'));
  }
  return [];
}

// Salvar novo sinal
function saveSignal(signal) {
  const signals = loadSignals();
  
  const newSignal = {
    id: Date.now(),
    timestamp: new Date().toISOString(),
    date: new Date().toLocaleDateString(),
    time: new Date().toLocaleTimeString(),
    symbol: signal.symbol,
    timeframe: signal.timeframe,
    direction: signal.direction,
    score: signal.score,
    entryPrice: signal.targets?.t1 ? 
      (signal.direction === 'BUY' ? signal.targets.t1 - (signal.targets.t1 - signal.stop) / 2 : signal.targets.t1 + (signal.stop - signal.targets.t1) / 2) : 
      (signal.stop + (signal.targets?.t1 || 0)) / 2,
    stopPrice: signal.stop,
    target1: signal.targets?.t1,
    target2: signal.targets?.t2,
    target3: signal.targets?.t3,
    riskReward: signal.riskReward,
    confirmations: signal.confirmations,
    status: 'ativo', // ativo, acertou, errou, stopado
    result: null,
    closedAt: null,
    finalPrice: null,
    profitPercent: null
  };
  
  signals.push(newSignal);
  fs.writeFileSync(SIGNALS_FILE, JSON.stringify(signals, null, 2));
  console.log(`📝 Sinal SALVO: ${signal.symbol} ${signal.direction} (score ${signal.score})`);
  return newSignal;
}

// Verificar sinais ativos e atualizar resultados
async function checkActiveSignals() {
  const signals = loadSignals();
  const activeSignals = signals.filter(s => s.status === 'ativo');
  
  if (activeSignals.length === 0) {
    console.log('✅ Nenhum sinal ativo para verificar');
    return;
  }
  
  console.log(`\n🔍 Verificando ${activeSignals.length} sinais ativos...`);
  
  for (const signal of activeSignals) {
    try {
      // Buscar preço atual do símbolo
      const response = await fetch(`https://fapi.binance.com/fapi/v1/ticker/price?symbol=${signal.symbol}`);
      const data = await response.json();
      const currentPrice = parseFloat(data.price);
      
      let novoStatus = signal.status;
      let resultado = null;
      let profitPercent = null;
      
      if (signal.direction === 'BUY') {
        // Verificar se atingiu o stop
        if (currentPrice <= signal.stopPrice) {
          novoStatus = 'errou';
          resultado = 'stop_atingido';
          profitPercent = ((signal.stopPrice - signal.entryPrice) / signal.entryPrice) * 100;
        }
        // Verificar se atingiu T1 (lucro parcial)
        else if (currentPrice >= signal.target1) {
          novoStatus = 'acertou';
          resultado = 'target1_atingido';
          profitPercent = ((signal.target1 - signal.entryPrice) / signal.entryPrice) * 100;
        }
      } else { // SELL
        if (currentPrice >= signal.stopPrice) {
          novoStatus = 'errou';
          resultado = 'stop_atingido';
          profitPercent = ((signal.entryPrice - signal.stopPrice) / signal.entryPrice) * 100;
        }
        else if (currentPrice <= signal.target1) {
          novoStatus = 'acertou';
          resultado = 'target1_atingido';
          profitPercent = ((signal.entryPrice - signal.target1) / signal.entryPrice) * 100;
        }
      }
      
      if (novoStatus !== signal.status) {
        // Atualizar sinal
        signal.status = novoStatus;
        signal.result = resultado;
        signal.closedAt = new Date().toISOString();
        signal.finalPrice = currentPrice;
        signal.profitPercent = profitPercent;
        
        // Salvar atualização
        fs.writeFileSync(SIGNALS_FILE, JSON.stringify(signals, null, 2));
        
        const emoji = novoStatus === 'acertou' ? '✅' : '❌';
        console.log(`${emoji} SINAL ENCERRADO: ${signal.symbol} ${signal.direction} | Resultado: ${resultado} | Lucro: ${profitPercent?.toFixed(2)}%`);
      }
      
    } catch (err) {
      console.error(`Erro ao verificar ${signal.symbol}:`, err.message);
    }
  }
}

// Calcular estatísticas
function showStats() {
  const signals = loadSignals();
  const total = signals.length;
  const acertou = signals.filter(s => s.status === 'acertou').length;
  const errou = signals.filter(s => s.status === 'errou').length;
  const ativos = signals.filter(s => s.status === 'ativo').length;
  
  const taxaAcerto = total > 0 ? (acertou / (acertou + errou)) * 100 : 0;
  
  console.log('\n' + '='.repeat(50));
  console.log('📊 ESTATÍSTICAS DO SISTEMA');
  console.log('='.repeat(50));
  console.log(`📈 Total de sinais: ${total}`);
  console.log(`✅ Acertou: ${acertou}`);
  console.log(`❌ Errou: ${errou}`);
  console.log(`⏳ Ativos: ${ativos}`);
  console.log(`🎯 Taxa de acerto: ${taxaAcerto.toFixed(1)}%`);
  console.log('='.repeat(50) + '\n');
}

// Listar últimos sinais
function showLastSignals(limit = 10) {
  const signals = loadSignals();
  const lastSignals = signals.slice(-limit).reverse();
  
  console.log('\n📋 ÚLTIMOS SINAIS:');
  console.log('-'.repeat(80));
  
  for (const s of lastSignals) {
    const statusEmoji = s.status === 'acertou' ? '✅' : (s.status === 'errou' ? '❌' : '⏳');
    const profitStr = s.profitPercent ? `${s.profitPercent > 0 ? '+' : ''}${s.profitPercent.toFixed(2)}%` : '---';
    console.log(`${statusEmoji} ${s.symbol} ${s.direction} (${s.timeframe}) | Score: ${s.score} | Status: ${s.status} | Lucro: ${profitStr}`);
  }
  console.log('-'.repeat(80) + '\n');
}

// Exportar funções
export { saveSignal, checkActiveSignals, showStats, showLastSignals, loadSignals };
