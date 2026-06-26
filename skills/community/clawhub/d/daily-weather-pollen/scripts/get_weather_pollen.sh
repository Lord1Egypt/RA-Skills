#!/bin/bash
# 获取北京天气和花粉浓度

# 天气
echo "=== 北京天气 ==="
curl -s "wttr.in/Beijing?format=%l:+%c+%t+体感温度%t+湿度%h+风速%w&lang=zh"
echo ""

# 花粉浓度需要用agent-browser访问网页获取，这里返回查询URL
echo "=== 花粉浓度查询 ==="
echo "请访问: https://richerculture.cn/hf/"
echo "或使用agent-browser: agent-browser open 'https://richerculture.cn/hf/'"
