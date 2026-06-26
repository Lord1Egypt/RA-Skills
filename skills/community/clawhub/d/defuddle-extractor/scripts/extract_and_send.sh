
#!/bin/bash

# 从 URL 提取内容并发送到微信文件传输助手
# 作者：Honcy Ye

# 使用方法：bash extract_and_send.sh "https://example.com/article" "文件传输助手"

if [ $# -lt 1 ]; then
    echo "Usage: $0 <url> [contact_name]"
    exit 1
fi

URL="$1"
CONTACT="${2:-文件传输助手}"

# 使用 defuddle 提取内容为 Markdown
CONTENT=$(npx defuddle parse "$URL" --markdown)

# 发送到微信
bash "/Users/honcy/.openclaw/skills/WeChat-Send/scripts/wechat_send.sh" "$CONTACT" "$CONTENT"
