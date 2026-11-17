# ============================================================
# 1688 Data Claw - Linux 启动浏览器
# 仅在 CDP 端口无响应时启动，否则复用已有实例
# ⚠️ 不查询任何进程信息，不关闭任何进程，只用标记文件识别实例
# ============================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/env.sh"

# 1. 确保 Xvfb 运行
if ! pgrep Xvfb > /dev/null; then
  echo ">>> 启动 Xvfb..."
  pkill -9 Xvfb 2>/dev/null || true
  rm -f /tmp/.X99-lock /tmp/.X11-unix/X99
  Xvfb "$DISPLAY" -screen 0 "$SCREEN" -ac &
  sleep 2
fi

# 2. 检查浏览器是否已在运行（仅通过标记文件识别，不查询任何进程）
if curl -s "http://127.0.0.1:$CDP_PORT/json/version" > /dev/null 2>&1; then
  if [ -f "$USER_DATA/.openclaw_browser_marker" ]; then
    echo "✅ 独立 Chromium 已在运行，直接复用 (CDP port $CDP_PORT)"
    exit 0
  fi
  # 端口被占用但标记文件不存在 → 不是我们的实例，拒绝启动
  echo "❌ CDP 端口 $CDP_PORT 被其他进程占用"
  echo "   标记文件 $USER_DATA/.openclaw_browser_marker 不存在，说明不是独立 Chromium 实例"
  echo "   请手动关闭占用该端口的进程后重试，或设置 CDP_PORT 环境变量更换端口"
  exit 1
fi

# 3. 确保 user-data-dir 目录存在
mkdir -p "$USER_DATA"

# 4. 启动浏览器新实例
echo ">>> 启动浏览器新实例..."

if [ ! -x "$CHROME" ]; then
  echo "❌ 浏览器可执行文件不存在: $CHROME"
  echo "   请先执行 setup.sh 安装依赖"
  exit 1
fi

DISPLAY="$DISPLAY" "$CHROME" \
  --no-sandbox \
  --disable-gpu \
  --disable-dev-shm-usage \
  --remote-debugging-port="$CDP_PORT" \
  --remote-allow-origins=* \
  --user-data-dir="$USER_DATA" \
  --window-size=1920,1080 \
  --no-first-run \
  --load-extension="$EXT_DIR" \
  > /tmp/chromium.log 2>&1 &

sleep 5

# 5. 验证启动
if curl -s "http://127.0.0.1:$CDP_PORT/json/version" > /dev/null 2>&1; then
  # 写入标记文件，标识这是我们的独立 Chromium 实例
  echo "$$" > "$USER_DATA/.openclaw_browser_marker"
  echo "$(date -Iseconds)" >> "$USER_DATA/.openclaw_browser_marker"
  echo "$CDP_PORT" >> "$USER_DATA/.openclaw_browser_marker"
  echo "✅ 浏览器启动成功 (CDP port $CDP_PORT)"
else
  echo "❌ 浏览器启动失败，查看日志: /tmp/chromium.log"
  exit 1
fi