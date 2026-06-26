#!/usr/bin/env bash
# 列出当前用户可「快捷记一笔」的指标预设（与 App 芯片列表一致）
# 用法: bash list-system-presets.sh
# 依赖: 同目录 api-call.sh（OAuth 用户 token）

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec "$SCRIPT_DIR/api-call.sh" GET /api/indicators/system-presets
