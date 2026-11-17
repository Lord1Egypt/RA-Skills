#!/bin/sh
# 一键「网页下载助手」：启动本机 serve + 全局剪贴板监听 + 打开 Web UI
# 用法：sh scripts/pan_web.sh [port=17890]
set -e
cd "$(dirname "$0")/.."
PORT="${1:-17890}"
PY="${PYTHON:-python3}"

# 常驻下载服务（后台）
if ! curl -s "http://127.0.0.1:$PORT/api/status" >/dev/null 2>&1; then
  echo "[pan_web] 启动本机下载服务 :$PORT"
  nohup "$PY" scripts/pan.py serve --port "$PORT" > /tmp/pan_web_serve.log 2>&1 &
  sleep 1
fi

# 全局剪贴板监听（后台）
echo "[pan_web] 启动全局剪贴板监听（ctrl+C 本窗口退出不影响后台服务）"
nohup "$PY" scripts/clipboard_monitor.py --port "$PORT" --once > /dev/null 2>&1 &   # 预热一次，投递当前剪贴板里的链接
"$PY" scripts/clipboard_monitor.py --port "$PORT" --interval 2 &
CLIP_PID=$!

# 打开网页
URL="http://127.0.0.1:$PORT/"
if command -v open >/dev/null 2>&1; then open "$URL"; fi
echo "[pan_web] Web 首页：$URL"
echo "[pan_web] 实时进度：http://127.0.0.1:$PORT/live"
echo "[pan_web] 剪贴板监听运行中（PID $CLIP_PID）。停止：kill $CLIP_PID"
wait $CLIP_PID
