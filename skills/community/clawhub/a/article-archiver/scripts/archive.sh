#!/bin/bash
# Article Archiver - Main Script
# Usage: bash archive.sh <URL>

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/config.sh"

URL="$1"

if [ -z "$URL" ]; then
    log_error "Usage: bash archive.sh <URL>"
    exit 1
fi

log "开始归档文章: $URL"

# 检查是否已归档
if [ -f "$ARCHIVED_URLS_FILE" ] && grep -Fxq "$URL" "$ARCHIVED_URLS_FILE"; then
    log "文章已归档，跳过"
    exit 0
fi

# 抓取文章内容
log "抓取文章内容..."
CONTENT=$(web_fetch --url "$URL" --extractMode markdown 2>&1)

if [ $? -ne 0 ]; then
    log_error "抓取失败: $CONTENT"
    exit 1
fi

# 提取标题（第一个 # 标题）
TITLE=$(echo "$CONTENT" | grep -m 1 '^#' | sed 's/^#* *//')

if [ -z "$TITLE" ]; then
    TITLE="未命名文章_$(date +%Y%m%d%H%M%S)"
    log "未找到标题，使用默认: $TITLE"
fi

log "文章标题: $TITLE"

# 获取当前月份
MONTH=$(date +%Y-%m)

# 准备文档内容
ARCHIVE_TIME=$(date '+%Y-%m-%d %H:%M:%S')
DOMAIN=$(echo "$URL" | awk -F/ '{print $3}')

DOC_CONTENT="> **原始链接**：$URL
> 
> **归档时间**：$ARCHIVE_TIME
> 
> **来源**：$DOMAIN

---

$CONTENT"

log "准备上传到飞书..."

# 这里需要调用 OpenClaw 的工具来完成飞书操作
# 由于是 bash 脚本，我们输出一个 JSON 指令，让主 agent 执行
cat <<EOF
{
  "action": "archive_to_feishu",
  "url": "$URL",
  "title": "$TITLE",
  "month": "$MONTH",
  "content": $(echo "$DOC_CONTENT" | jq -Rs .)
}
EOF
