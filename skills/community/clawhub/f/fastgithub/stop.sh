#!/bin/bash
# FastGithub 停止脚本

pkill -f fastgithub
sleep 1

if pgrep -f "fastgithub" > /dev/null; then
    echo "❌ 停止失败"
else
    echo "✅ FastGithub 已停止"
fi