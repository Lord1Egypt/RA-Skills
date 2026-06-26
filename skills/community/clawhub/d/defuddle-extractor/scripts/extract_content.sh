
#!/bin/bash

# 从 URL 提取网页内容
# 作者：Honcy Ye

# 使用方法：bash extract_content.sh "https://example.com/article"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <url> [--markdown]"
    exit 1
fi

URL="$1"
OUTPUT_FORMAT=""

if [ "$2" == "--markdown" ]; then
    OUTPUT_FORMAT="--markdown"
fi

# 使用 defuddle 提取内容
npx defuddle parse "$URL" $OUTPUT_FORMAT
