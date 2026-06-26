---
name: apex-ia
description: APEX IA - Scanner profissional multi-timeframe para Binance Futures. Detecta cruzamentos SMA 8x21 com confirmação de Pivot SuperTrend, RSI, volume e confluência
version: 0.1.0
author: marcusfranca12
tags:
  - binance
  - futures
  - scanner
  - sma
  - trading
  - apex
---

# APEX IA Scanner

## Descrição

O APEX IA é um scanner profissional para **Binance Futures** que varre todos os pares USDT-perp em múltiplos timeframes (1m, 5m, 15m, 30m, 1h, 4h, 1d).

### Algoritmo de Detecção

O motor utiliza uma combinação de indicadores testados em mercado:

1. **SMA 8x21** - Cruzamento rápido/lento com filtro anti-ruído (separação mínima de 0.05%)
2. **Pivot Point SuperTrend** - Confirmação de direção (parâmetros prd=2, factor=2, atr=10)
3. **RSI (14)** - Mede intensidade do movimento (4 níveis: NORMAL, ALTA, FORTE, SUPER_FORTE)
4. **Volume Relativo** - Compara volume atual com média de 20 barras
5. **Alvos Dinâmicos** - Baseados no ATR(14) multiplicado pelo volume ratio
6. **Confluência Multi-TF** - Sinais alinhados em múltiplos timeframes sobem no ranking

### Classificação de Qualidade

| Classificação | Critério | Significado |
|-------------|----------|-------------|
| CONFIRMADO | cross + ST flip + score ≥ 8 | Sinal mais forte possível |
| PIVOT | cross + ST alinhado (sem flip) + score ≥ 7 | Sinal forte com confirmação |
| SMA | apenas cross, score ≥ 5 | Sinal base - requer confirmação manual |

### Score (0-10)

O score combina 3 fatores com pesos diferentes:

- **RSI (peso 4)**: Quanto mais extremo, maior o score
- **Volume (peso 3)**: Volume explosivo aumenta confiança
- **SuperTrend (peso 3)**: Flip recente confirma direção

## Tools

| Tool | Descrição |
|------|-----------|
| `apex-scan` | Escaneia todos os pares e retorna os melhores setups ordenados por qualidade (CONFIRMADO > PIVOT > SMA) e score |

## Parâmetros do Scan

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| minScore | number | 5 | Score mínimo para filtrar sinais (0-10) |
| includeTFs | array | [1m,5m,15m,1h,4h] | Timeframes para escanear |
| symbolLimit | number | 30 | Limite de pares (evita rate limit) |

## Installation

```bash
clawhub install apex-ia
```

## Exemplos de Uso

```
"Me mostre os melhores setups agora na Binance Futures"
"Escaneia apenas pares com score mínimo 7"
"Quais sinais CONFIRMADO temos no BTC?"
```

## Exemplo de Saída

```
✅ **BTCUSDT** - 🟢 COMPRA (15m)
   ⚡ Score: 8.5/10 | RSI: 29 (FORTE)
   📊 Volume: 1.8x | RR: 2.50
   🎯 T1: 68420 | T2: 68920 | T3: 69800
   🛑 Stop: 68100
   🔗 Confluência: 3 TF (15m, 1h, 4h)
```

## Configuração

Adicione ao seu arquivo `.env` do OpenClaw:

```bash
APEX_MIN_SCORE=5
APEX_SYMBOL_LIMIT=50
APEX_TFS=1m,5m,15m,1h,4h
```

## Requisitos

- OpenClaw instalado e configurado
- Conexão com internet (acesso à API da Binance)

## Aviso de Risco

> ⚠️ **Este skill é uma ferramenta de análise. Não é consultoria financeira.** Sempre faça sua própria análise antes de operar. Futuros na Binance envolvem alto risco de perda. Comece na testnet.

## Licença

MIT

---

**Desenvolvido por @marcusfranca12 para a comunidade OpenClaw**
