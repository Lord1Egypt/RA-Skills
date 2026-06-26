#!/bin/bash
# API Translator - 翻譯 API 文檔為繁體中文

URL="$1"

if [ -z "$URL" ]; then
    echo "用法: api-translator <URL>"
    echo "範例: api-translator https://api.example.com/docs"
    exit 1
fi

echo "正在抓取 API 文檔: $URL"
echo "..."

# 抓取網頁內容
CONTENT=$(web_fetch --url "$URL" --maxChars 50000 2>/dev/null)

if [ -z "$CONTENT" ]; then
    echo "錯誤：無法抓取網頁內容"
    exit 1
fi

# 發送給 LLM 翻譯
TRANSLATED=$(cat << 'EOF' | tail -n +2
請將以下 API 文檔翻譯成繁體中文（台灣用語），保持 Markdown 格式和程式碼不變，只翻譯說明文字：

EOF
echo "$CONTENT"
)

# 這裡用 echo 讓 LLM 自動處理翻譯
echo "正在翻譯..."
echo "$TRANSLATED"
