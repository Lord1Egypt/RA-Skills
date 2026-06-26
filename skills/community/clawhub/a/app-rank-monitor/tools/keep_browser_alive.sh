#!/bin/bash
# 点点数据浏览器保持常开脚本

USER_DATA_DIR="/Users/cfans/.openclaw/workspace/skills/app-rank-monitor/.browser_data/diandian"

echo "🚀 启动点点数据浏览器（后台运行）..."

# 使用 nohup 后台运行 Chrome
nohup /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
    --user-data-dir="$USER_DATA_DIR" \
    --remote-debugging-port=9222 \
    --window-size=1920,1080 \
    --no-first-run \
    --disable-features=TranslateUI \
    > /tmp/diandian_browser.log 2>&1 &

BROWSER_PID=$!
echo $BROWSER_PID > /tmp/diandian_browser.pid

echo "✅ 浏览器已启动（PID: $BROWSER_PID）"
echo "💡 浏览器在后台运行，不会关闭"
echo "📍 用户数据目录：$USER_DATA_DIR"
echo ""
echo "查看浏览器日志：tail -f /tmp/diandian_browser.log"
echo "关闭浏览器：kill $BROWSER_PID"
