#!/bin/bash
# 费曼虾 — 启动 Web 面板
# 从任意位置运行均可，脚本会自动定位到 web 目录
# 示例：bash ~/.openclaw/skills/feynman-lobster/scripts/start-panel.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WEB_DIR="$SCRIPT_DIR/../web"
PORT=19380
API_HOST="127.0.0.1"
API_PORT=18790
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw}"
PANEL_URL="http://localhost:$PORT"
API_LOG="/tmp/feynman-api.log"
PANEL_LOG="/tmp/feynman-panel.log"
DETACHED=0
AUTO_OPEN=0

for arg in "$@"; do
  case "$arg" in
    --detached) DETACHED=1 ;;
    --open) AUTO_OPEN=1 ;;
    --no-open) AUTO_OPEN=0 ;;
  esac
done

if [ ! -d "$WEB_DIR" ]; then
  echo "❌ 未找到 web 目录：$WEB_DIR"
  exit 1
fi

is_ready() {
  curl -fsS "$1" >/dev/null 2>&1
}

open_browser() {
  if [ "$AUTO_OPEN" -ne 1 ]; then
    return 0
  fi
  if command -v open >/dev/null 2>&1; then
    open "$PANEL_URL" >/dev/null 2>&1 || true
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$PANEL_URL" >/dev/null 2>&1 || true
  fi
}

start_local_api_if_needed() {
  if is_ready "http://localhost:18789/api/feynman/contracts"; then
    return 0
  fi
  if is_ready "http://$API_HOST:$API_PORT/api/feynman/contracts"; then
    return 0
  fi
  echo "   启动本地真实数据桥接器：http://$API_HOST:$API_PORT"
  nohup python3 "$SCRIPT_DIR/feynman_api.py" --host "$API_HOST" --port "$API_PORT" --workspace "$WORKSPACE" >"$API_LOG" 2>&1 &
  sleep 0.5
}

start_panel_if_needed_detached() {
  if is_ready "$PANEL_URL/"; then
    return 0
  fi
  nohup python3 -m http.server "$PORT" --bind 127.0.0.1 --directory "$WEB_DIR" >"$PANEL_LOG" 2>&1 &
  sleep 0.5
}

echo "🦞 费曼虾面板启动中..."
echo "   地址：http://localhost:$PORT"
echo "   数据源优先级：Gateway(18789) -> 本地桥接器($API_PORT)"
if [ "$DETACHED" -eq 1 ]; then
  echo "   模式：后台常驻"
else
  echo "   模式：前台运行（按 Ctrl+C 停止）"
fi
echo ""

start_local_api_if_needed

if [ "$DETACHED" -eq 1 ]; then
  start_panel_if_needed_detached
  open_browser
  if is_ready "$PANEL_URL/"; then
    echo "✅ 面板已就绪：$PANEL_URL"
  else
    echo "⚠️ 面板启动失败，请查看日志：$PANEL_LOG"
    exit 1
  fi
  exit 0
fi

if is_ready "$PANEL_URL/"; then
  open_browser
  echo "✅ 检测到面板已在运行：$PANEL_URL"
  exit 0
fi

open_browser
exec python3 -m http.server "$PORT" --bind 127.0.0.1 --directory "$WEB_DIR"
