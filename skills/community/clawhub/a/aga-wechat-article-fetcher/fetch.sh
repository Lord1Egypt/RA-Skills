#!/bin/bash
# wechat-article-fetcher 主脚本

URL=$1
PORT=${2:-8080}

if [ -z "$URL" ]; then
    echo "用法: ./fetch.sh <微信文章URL> [端口]"
    echo "示例: ./fetch.sh https://mp.weixin.qq.com/s/xxxxx"
    exit 1
fi

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 运行Python脚本
python3 "$SCRIPT_DIR/fetch.py" "$URL"

# 检查HTTP服务器是否运行
if ! lsof -Pi :$PORT -sTCP:LISTEN -t > /dev/null 2>&1; then
    echo ""
    echo "启动HTTP服务器在端口 $PORT..."
    cd /root/.openclaw/workspace && python3 -m http.server $PORT > /dev/null 2>&1 &
    sleep 2
fi

echo ""
echo "✅ 完成！请在浏览器访问上述地址查看文章"
