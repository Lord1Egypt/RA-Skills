#!/usr/bin/env bash
# Daily Market Brief — morning / midday / evening reports
# Usage: bash daily-brief.sh [morning|midday|evening]
set -euo pipefail

MODE="${1:-morning}"
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
CST_NOW=$(TZ='Asia/Shanghai' date '+%m/%d %H:%M')

case "$MODE" in
  morning)
    echo "===== ☀️ 早间简报 ====="
    echo ""
    echo "[恐慌指数]"
    bash "$SKILL_DIR/fear-greed.sh" 2>/dev/null | head -20
    echo ""
    echo "[行情速览]"
    bash "$SKILL_DIR/quotes.sh" 2>/dev/null
    echo ""
    echo "[今日关注]"
    bash "$SKILL_DIR/ecal.sh" 2>/dev/null | head -15
    ;;
  midday)
    echo "===== 🌤 午间速报 ====="
    echo ""
    bash "$SKILL_DIR/quotes.sh" 2>/dev/null
    ;;
  evening)
    echo "===== 🌙 晚间复盘 ====="
    echo ""
    echo "[美股早盘]"
    bash "$SKILL_DIR/quotes.sh" 2>/dev/null
    echo ""
    echo "[恐慌指数]"
    bash "$SKILL_DIR/fear-greed.sh" 2>/dev/null | head -20
    echo ""
    echo "[明日关注]"
    bash "$SKILL_DIR/ecal.sh" 2>/dev/null | head -15
    ;;
  *)
    echo "Usage: daily-brief.sh [morning|midday|evening]"
    ;;
esac
