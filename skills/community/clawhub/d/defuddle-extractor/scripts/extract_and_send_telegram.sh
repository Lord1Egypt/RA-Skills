
#!/bin/bash

# 从 URL 提取内容并发送到 Telegram
# 作者：Honcy Ye

# 使用方法：bash extract_and_send_telegram.sh "https://example.com/article" <chat_id>

if [ $# -ne 2 ]; then
    echo "Usage: $0 <url> <chat_id>"
    exit 1
fi

URL="$1"
CHAT_ID="$2"

# 使用 defuddle 提取内容为 Markdown
CONTENT=$(npx defuddle parse "$URL" --markdown)

# 发送到 Telegram
openclaw message send --channel telegram --target "$CHAT_ID" --message "$CONTENT"
