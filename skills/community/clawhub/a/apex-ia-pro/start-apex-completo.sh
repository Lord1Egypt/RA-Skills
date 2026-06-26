#!/bin/bash

echo "🦞 APEX IA - SISTEMA COMPLETO"
echo "=============================="
echo ""
echo "Iniciando APEX IA Scanner e Trader Automático..."
echo ""

# Limpar sinais anteriores
rm -f bridge-signals.json

# Criar arquivo de ponte vazio
echo '{"lastSignal": null, "timestamp": null, "updated": false}' > bridge-signals.json

# Iniciar o trader em background
node apex-ia-trader.mjs &
TRADER_PID=$!

# Aguardar 2 segundos
sleep 2

# Iniciar o scanner
node apex-ia-software.mjs

# Quando o scanner fechar, matar o trader
kill $TRADER_PID 2>/dev/null
