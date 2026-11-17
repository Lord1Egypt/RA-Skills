#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# cdp_render.sh — 本地 HTML → PDF（系统 Chrome + CDP，不依赖 Playwright 浏览器）
#
# 用法：
#   bash cdp_render.sh <in.html> <out.pdf> [waitMs=2400] [css|landscape|portrait]
#
# 方向默认 css —— 由源 HTML 的 @page{size:...} 决定，因此同一脚本既能导
# 「BII 双栏 A4 横向」也能导「classic A4 纵向」，不必分两套代码。
#
# 复用已有 Chrome：设 CDP_ENDPOINT=http://127.0.0.1:9333 即复用，不再自起自收。
#   （render.sh 先用同一个 Chrome 做图表/溢出校验，再复用导出，省一次冷启动）
#
# 依赖：系统 Chrome/Edge/Chromium + node 22（自带 WebSocket 与 fetch）
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

IN="${1:-}"; OUT="${2:-}"; WAIT="${3:-2400}"; ORIENT="${4:-css}"
[ -n "$IN" ] && [ -n "$OUT" ] || { sed -n '2,10p' "$0"; exit 2; }
[ -f "$IN" ] || { echo "[!] 找不到 HTML：$IN"; exit 1; }
IN="$(cd "$(dirname "$IN")" && pwd)/$(basename "$IN")"   # 取绝对路径，Chrome 才能 load

NODE="${BII_NODE:-}"
if [ -z "$NODE" ]; then
  for c in "$(command -v node || true)" \
           "$HOME/.workbuddy/binaries/node/versions/22.12.0/bin/node" \
           "$HOME/.workbuddy/binaries/node/versions/22.22.2-3/bin/node"; do
    [ -n "$c" ] && [ -x "$c" ] && { NODE="$c"; break; }
  done
fi
[ -n "$NODE" ] || { echo "[!] 找不到 node（CDP 导出需要）"; exit 1; }

mkdir -p "$(dirname "$OUT")"

# ── 复用模式：直接用调用方给的 CDP 端点 ──
if [ -n "${CDP_ENDPOINT:-}" ]; then
  echo "▶ 复用已运行的 Chrome：$CDP_ENDPOINT"
  "$NODE" "$HERE/cdp_pdf.js" "$CDP_ENDPOINT" "$OUT" "$WAIT" "$ORIENT"
  exit 0
fi

# ── 自起模式 ──
CHROME="${BII_CHROME:-}"
if [ -z "$CHROME" ]; then
  for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
           "/Applications/Chromium.app/Contents/MacOS/Chromium" \
           "$(command -v google-chrome || true)" \
           "$(command -v chromium || true)"; do
    [ -n "$c" ] && [ -x "$c" ] && { CHROME="$c"; break; }
  done
fi
[ -n "$CHROME" ] || { echo "[!] 找不到 Chrome/Edge/Chromium"; exit 1; }

PORT="${BII_CDP_PORT:-9333}"
PROFILE="$(mktemp -d -t cdp-render-XXXXXX)"

cleanup() {
  [ -n "${CHROME_PID:-}" ] && kill "$CHROME_PID" 2>/dev/null || true
  rm -rf "$PROFILE" 2>/dev/null || true
}
trap cleanup EXIT

# 端口自愈：残留 Chrome 蹲在 9333 会让新实例绑不上端口，请求却被老实例接走，
# 于是"导出成功"但内容是上一次的页面。先找一个没人应答的端口。
BASE_PORT="$PORT"
while curl -s --noproxy '*' "http://127.0.0.1:$PORT/json/version" >/dev/null 2>&1; do
  echo "[i] 端口 $PORT 已被其它 Chrome 占用，换端口"
  PORT=$((PORT + 1))
  if [ "$PORT" -gt "$((BASE_PORT + 20))" ]; then
    echo "[!] $BASE_PORT..$((BASE_PORT + 20)) 全被占用，先清残留 Chrome："
    echo "    pkill -f 'remote-debugging-port=$BASE_PORT'"
    exit 1
  fi
done

#   --no-sandbox / --in-process-gpu 必需：受限环境里 GPU 进程起不来会让 Chrome 直接退出
#   全新 user-data-dir 必需：否则浏览器会缓存上一次的 HTML，改了代码还看到旧页面
"$CHROME" --headless=new --no-sandbox --disable-setuid-sandbox \
  --disable-dev-shm-usage --disable-gpu --in-process-gpu \
  --no-first-run --no-default-browser-check --disable-application-cache \
  --user-data-dir="$PROFILE" --remote-debugging-port="$PORT" \
  --window-size=1400,1200 "file://$IN" > "$PROFILE/chrome.log" 2>&1 &
CHROME_PID=$!

CDP="http://127.0.0.1:$PORT"
for _ in $(seq 1 40); do
  curl -s --noproxy '*' "$CDP/json/version" >/dev/null 2>&1 && break
  sleep 0.5
done
curl -s --noproxy '*' "$CDP/json/version" >/dev/null 2>&1 \
  || { echo "[!] Chrome 未在 20s 内就绪"; tail -5 "$PROFILE/chrome.log"; exit 1; }

echo "▶ 导出 PDF：$IN"
"$NODE" "$HERE/cdp_pdf.js" "$CDP" "$OUT" "$WAIT" "$ORIENT"
