"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.tools = void 0;
const scanner_js_1 = require("./scanner.js");
exports.tools = [
    {
        name: 'apex-scan',
        description: 'Escaneia todos os pares USDT-perp da Binance Futures em múltiplos timeframes. Retorna sinais CONFIRMADO/PIVOT/SMA ordenados por qualidade e confluência.',
        parameters: {
            type: 'object',
            properties: {
                minScore: { type: 'number', description: 'Score mínimo (0-10, padrão: 5)', default: 5 },
                includeTFs: { type: 'array', items: { type: 'string' }, default: ['1m', '5m', '15m', '1h', '4h'] },
                symbolLimit: { type: 'number', description: 'Limite de pares (padrão: 30)', default: 30 }
            }
        },
        handler: async (args) => {
            const signals = await (0, scanner_js_1.scanAll)(args);
            if (signals.length === 0) {
                return "🔍 Nenhum sinal encontrado com os critérios atuais.";
            }
            let response = `📊 **APEX IA SCAN** - ${signals.length} sinais encontrados\n\n`;
            for (let i = 0; i < Math.min(signals.length, 5); i++) {
                response += (0, scanner_js_1.formatSignalForDisplay)(signals[i]);
                response += '\n---\n';
            }
            if (signals.length > 5) {
                response += `\n... e mais ${signals.length - 5} sinais. Use minScore maior para filtrar.`;
            }
            return response;
        }
    }
];
console.log('✅ APEX IA Skill carregado com', exports.tools.length, 'tool');
