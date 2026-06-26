#!/bin/bash
# FastGithub 重启脚本

pkill -f fastgithub
sleep 1

cd /workspace/skills/fastgithub/publish
nohup ./fastgithub > /workspace/fastgithub.log 2>&1 &
sleep 2

if pgrep -f "fastgithub" > /dev/null; then
    echo "✅ FastGithub 已重启，代理地址: http://127.0.0.1:38457"
else
    echo "❌ 重启失败"
fi