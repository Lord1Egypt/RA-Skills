#!/usr/bin/env bash
# 一键跑通示例：隔离目录，不碰你的真实数据。成功输出 ✅ 与 rc=0。
set -euo pipefail
cd "$(dirname "$0")"

DEMO="${TMPDIR:-/tmp}/ashare-demo-$$"
trap 'rm -rf "$DEMO"' EXIT
mkdir -p "$DEMO"
cp -r examples/sample_direction/. "$DEMO"/

echo "示例数据：$DEMO（临时，跑完即删）"
echo
STOCK_DATA_DIR="$DEMO" python3 scripts/validate_ledgers.py
echo
echo "✅ 示例跑通。下一步：bash init.sh 初始化你自己的数据目录。"
