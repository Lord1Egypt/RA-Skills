#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/server"

# 结束可能正在运行的8765端口服务
lsof -ti:8765 | xargs kill -9 2>/dev/null
sleep 1

# 启动服务器
python3 server.py &

# SERVER_PID=$!

# # 等待服务器启动
# sleep 2

# # 检测是否在 Trae IDE 中运行
# if [ "$TRAE" = "true" ] || [ -n "$TRAE_SESSION_ID" ] || [ "$TERM_PROGRAM" = "Trae" ] || [ -n "$TRAE_PID" ]; then
#     # 使用 Trae 打开浏览器
#     /Applications/Trae\ CN.app/Contents/Resources/app/bin/trae-cn 'http://127.0.0.1:8765'
# elif command -v xdg-open &> /dev/null; then
#     xdg-open "http://127.0.0.1:8765"
# elif command -v open &> /dev/null; then
#     open "http://127.0.0.1:8765"
# fi

# # 等待服务器进程
# wait $SERVER_PID
