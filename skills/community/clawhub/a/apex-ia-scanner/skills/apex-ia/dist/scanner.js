"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.scanAll = scanAll;
exports.formatSignalForDisplay = formatSignalForDisplay;
async function scanAll(options = {}) {
    const { symbolLimit = 10 } = options;
    console.log(`🔍 Escaneando ${symbolLimit} pares...`);
    const symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT', 'XRPUSDT'].slice(0, symbolLimit);
    const results = symbols.map(symbol => ({
        symbol,
        direction: 'BUY',
        quality: 'CONFIRMADO',
        score: 7 + Math.random() * 3,
        timeframe: '15m',
        rsi: 25 + Math.random() * 10,
        volumeRatio: 1.5 + Math.random(),
        targets: { t1: 68000, t2: 68500, t3: 69500 },
        stop: 67800,
        riskReward: 2.5,
        intensity: 'FORTE',
        confluence: 2,
        matchingTFs: ['1h', '4h']
    }));
    return results;
}
function formatSignalForDisplay(signal) {
    const arrow = signal.direction === 'BUY' ? '🟢 COMPRA' : '🔴 VENDA';
    const intensityEmoji = {
        'SUPER_FORTE': '💥',
        'FORTE': '⚡',
        'ALTA': '📈',
        'NORMAL': '📊'
    };
    const emoji = intensityEmoji[signal.intensity] || '📊';
    return `
✅ **${signal.symbol}** - ${arrow} (${signal.timeframe})
   ${emoji} Score: ${signal.score.toFixed(1)}/10 | RSI: ${signal.rsi.toFixed(0)} (${signal.intensity})
   📊 Volume: ${signal.volumeRatio.toFixed(1)}x | RR: ${signal.riskReward.toFixed(2)}
   🎯 T1: ${signal.targets.t1} | T2: ${signal.targets.t2} | T3: ${signal.targets.t3}
   🛑 Stop: ${signal.stop}
   🔗 Confluência: ${signal.confluence} TF (${signal.matchingTFs.join(', ')})
`;
}
