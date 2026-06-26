#!/bin/bash
# 启动 Chrome 调试实例（用于 gui 模式）
# 用法: ./start-chrome-debug.sh

DISPLAY=:0

# 检查是否已经在运行
if curl -s --max-time 2 http://localhost:9222/json/version > /dev/null 2>&1; then
  echo "Chrome 调试实例已在运行 (PID: $(pgrep -f 'chrome.*remote-debugging' | head -1))"
  exit 0
fi

# 使用用户默认 profile 启动 Chrome（复用已登录状态）
google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=$HOME/.config/google-chrome/Default \
  --new-window \
  --no-sandbox \
  > /tmp/chrome-debug.log 2>&1 &

CHROME_PID=$!
echo "Chrome 调试实例已启动 (PID: $CHROME_PID)"

# 等待启动完成
for i in {1..10}; do
  if curl -s --max-time 2 http://localhost:9222/json/version > /dev/null 2>&1; then
    echo "Chrome 调试端口已就绪 (http://localhost:9222)"
    exit 0
  fi
  sleep 1
done

echo "警告: Chrome 启动可能失败，查看 /tmp/chrome-debug.log"
