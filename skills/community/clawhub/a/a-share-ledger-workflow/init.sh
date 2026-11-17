#!/usr/bin/env bash
# 初始化 $STOCK_DATA_DIR 目录骨架（已存在的文件不覆盖）。
set -euo pipefail
cd "$(dirname "$0")"

DIR="${STOCK_DATA_DIR:-$HOME/stock_data}"
mkdir -p "$DIR/股票台账/候选" "$DIR/股票台账/持仓中" "$DIR/股票台账/模板" \
         "$DIR/方向记录/数据" "$DIR/reports"

put() { [ -e "$2" ] || cp "$1" "$2"; }   # 不覆盖已有文件（跨平台，不用 cp -n）

put templates/ledger_template.md          "$DIR/股票台账/模板/单股跟踪台账_模板.md"
put templates/status_table_template.md    "$DIR/股票台账/流程状态表.md"
put templates/direction_template.md       "$DIR/方向记录/方向档案_模板.md"
put templates/bench.example.json          "$DIR/bench.json"

echo "已初始化：$DIR"
echo
echo "下一步："
echo "  1. 编辑 $DIR/bench.json —— 按你的标的填 7 项门槛字段（模板顶部有注释）"
echo "  2. export STOCK_DATA_DIR=\"$DIR\""
echo "  3. python3 scripts/validate_ledgers.py"
