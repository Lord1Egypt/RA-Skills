import { scanAll, formatSignalForDisplay } from './scanner.js';
export const tools = [
    {
        name: 'apex-scan',
        description: 'Escaneia todos os pares USDT-perp da Binance Futures em múltiplos timeframes. Retorna sinais CONFIRMADO/PIVOT/SMA ordenados por qualidade e confluência.',
        parameters: {
            type: 'object',
            properties: {
                minScore: { type: 'number', description: 'Score mínimo (0-10, padrão: 5)', default: 5 },
                includeTFs: { type: 'array', items: { type: 'string' }, default: ['15m', '1h', '4h'] },
                symbolLimit: { type: 'number', description: 'Limite de pares (padrão: 20)', default: 20 }
            }
        },
        handler: async (args) => {
            const signals = await scanAll(args);
            if (signals.length === 0) {
                return "🔍 Nenhum sinal encontrado com os critérios atuais. Tente reduzir minScore para 3 ou aguarde novos cruzamentos.";
            }
            let response = `📊 **APEX IA SCAN** - ${signals.length} sinais encontrados\n\n`;
            for (let i = 0; i < Math.min(signals.length, 10); i++) {
                response += formatSignalForDisplay(signals[i]);
                response += '\n---\n';
            }
            if (signals.length > 10) {
                response += `\n... e mais ${signals.length - 10} sinais. Use minScore maior para filtrar.`;
            }
            return response;
        }
    }
];
console.log('✅ APEX IA Skill carregado com', tools.length, 'tool');
