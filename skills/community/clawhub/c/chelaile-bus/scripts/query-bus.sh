#!/usr/bin/env bash
# chelaile-bus helper: 一句话查公交实时
# 用法:
#   query-bus.sh <线路号> [目标站名]
#   query-bus.sh 311 展春园西路北口
#   query-bus.sh 311  # 不指定站 → 列出线路详情+在线车辆
# kimiclaw 适配（2026-09-22）: 逻辑已迁至 query-bus.py（MCP stdio 直连，无 mcporter 依赖），本文件为兼容包装
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/query-bus.py" "$@"
