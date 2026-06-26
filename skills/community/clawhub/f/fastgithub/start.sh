#!/bin/bash
# FastGithub 启动脚本

cd /workspace/skills/fastgithub/publish

if pgrep -f "fastgithub" > /dev/null; then
    echo "FastGithub 已在运行"
    exit 0
fi

nohup ./fastgithub > /workspace/fastgithub.log 2>&1 &
sleep 2

if pgrep -f "fastgithub" > /dev/null; then
    echo "✅ FastGithub 已启动，代理地址: http://127.0.0.1:38457"
else
    echo "❌ 启动失败"
fi