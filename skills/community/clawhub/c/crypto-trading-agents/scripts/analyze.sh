#!/usr/bin/env bash
# ─────────────────────────────────────────────
# Crypto Trading Agents - 快速分析脚本
# 用法：bash scripts/analyze.sh BTC/USDT
# ─────────────────────────────────────────────

SYMBOL="${1:-BTC/USDT}"
DATE="${2:-}"

echo "🔍 分析 $SYMBOL ..."

source .venv/bin/activate

if [ -z "$DATE" ]; then
    python -m tradingagents.crypto_trading --symbol "$SYMBOL" --action analyze
else
    python -m tradingagents.crypto_trading --symbol "$SYMBOL" --action analyze --date "$DATE"
fi
