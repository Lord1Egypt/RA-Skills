#!/bin/bash
###############################################################################
# AI内容收集脚本
# 用法: ./collect.sh [日期，格式YYYY-MM-DD，默认为今天]
###############################################################################

set -e

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIPELINE_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$PIPELINE_DIR/config/sources.json"

# 日期处理
DATE="${1:-$(date +%Y-%m-%d)}"
TIME_24H_AGO=$(($(date +%s) - 86400))

# 输出目录
OUTPUT_DIR="$PIPELINE_DIR/collected/$DATE"
mkdir -p "$OUTPUT_DIR"

# 日志文件
LOG_FILE="$OUTPUT_DIR/collection.log"
RAW_FILE="$OUTPUT_DIR/raw-content.json"
MARKDOWN_FILE="$OUTPUT_DIR/raw-content.md"

# 初始化日志
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "========== AI内容收集开始 =========="
log "日期: $DATE"
log "输出目录: $OUTPUT_DIR"
log "24小时前时间戳: $TIME_24H_AGO"

# 初始化JSON文件
echo '{"date": "'$DATE'", "collection_time": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'", "sources": []}' > "$RAW_FILE"

# 初始化Markdown文件
cat > "$MARKDOWN_FILE" << EOF
# AI内容收集报告 - $DATE

> 收集时间: $(date '+%Y-%m-%d %H:%M:%S')
> 数据来源: Hacker News, Reddit

---

EOF

###############################################################################
# 函数: 收集Hacker News内容
###############################################################################
collect_hackernews() {
    log "[Hacker News] 开始收集AI相关内容..."
    
    local TEMP_FILE=$(mktemp)
    local API_URL="https://hn.algolia.com/api/v1/search?query=AI+OR+artificial+intelligence+OR+LLM+OR+GPT+OR+Claude&tags=story&numericFilters=created_at_i>${TIME_24H_AGO}&hitsPerPage=20"
    
    log "[Hacker News] API URL: $API_URL"
    
    # 调用API
    if curl -s --max-time 30 "$API_URL" -o "$TEMP_FILE"; then
        # 检查是否有效JSON
        if jq -e '.hits' "$TEMP_FILE" > /dev/null 2>&1; then
            local COUNT=$(jq '.hits | length' "$TEMP_FILE")
            log "[Hacker News] 成功获取 $COUNT 条内容"
            
            # 保存到主JSON
            local SOURCE_JSON=$(jq -n \
                --arg name "Hacker News" \
                --arg id "hn-ai" \
                --arg count "$COUNT" \
                '{name: $name, id: $id, count: ($count | tonumber), items: []}')
            
            # 处理每条内容
            local ITEMS=$(jq '.hits[] | select(.title != null) | {
                title: .title,
                url: .url,
                author: .author,
                points: .points,
                comments: .num_comments,
                created_at: .created_at,
                objectID: .objectID,
                hn_url: ("https://news.ycombinator.com/item?id=" + .objectID)
            }' "$TEMP_FILE" | jq -s '.')
            
            SOURCE_JSON=$(echo "$SOURCE_JSON" | jq --argjson items "$ITEMS" '.items = $items')
            
            # 添加到主JSON
            jq --argjson source "$SOURCE_JSON" '.sources += [$source]' "$RAW_FILE" > "${RAW_FILE}.tmp" && mv "${RAW_FILE}.tmp" "$RAW_FILE"
            
            # 写入Markdown
            {
                echo "## 🔥 Hacker News - AI相关内容"
                echo ""
                echo "共 $COUNT 条"
                echo ""
                
                echo "$ITEMS" | jq -r '.[] | 
                    "### \(.title)" + "\n" +
                    "- **热度**: ⬆️ \(.points) points, 💬 \(.comments) comments" + "\n" +
                    "- **作者**: @\(.author)" + "\n" +
                    "- **原文链接**: \(.url // "N/A")" + "\n" +
                    "- **HN讨论**: \(.hn_url)" + "\n" +
                    "- **收录时间**: \(.created_at)" + "\n"
                '
                
                echo "---"
                echo ""
            } >> "$MARKDOWN_FILE"
            
            log "[Hacker News] 处理完成"
        else
            log "[Hacker News] ❌ 返回数据无效"
        fi
    else
        log "[Hacker News] ❌ 请求失败"
    fi
    
    rm -f "$TEMP_FILE"
}

###############################################################################
# 函数: 收集Reddit内容
###############################################################################
collect_reddit() {
    local SUBREDDIT="$1"
    local LIMIT="$2"
    local DISPLAY_NAME="$3"
    
    log "[Reddit r/$SUBREDDIT] 开始收集..."
    
    local TEMP_FILE=$(mktemp)
    local API_URL="https://www.reddit.com/r/${SUBREDDIT}/hot.json?limit=${LIMIT}"
    
    log "[Reddit r/$SUBREDDIT] API URL: $API_URL"
    
    # 调用API
    if curl -s --max-time 30 \
        -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
        "$API_URL" -o "$TEMP_FILE"; then
        
        # 检查是否有效JSON
        if jq -e '.data.children' "$TEMP_FILE" > /dev/null 2>&1; then
            local COUNT=$(jq '[.data.children[] | select(.data.stickied != true)] | length' "$TEMP_FILE")
            log "[Reddit r/$SUBREDDIT] 成功获取 $COUNT 条内容"
            
            # 保存到主JSON
            local SOURCE_JSON=$(jq -n \
                --arg name "$DISPLAY_NAME" \
                --arg id "reddit-$SUBREDDIT" \
                --arg count "$COUNT" \
                '{name: $name, id: $id, count: ($count | tonumber), items: []}')
            
            # 处理每条内容
            local ITEMS=$(jq '.data.children[] | select(.data.stickied != true) | {
                title: .data.title,
                url: .data.url,
                permalink: ("https://reddit.com" + .data.permalink),
                author: .data.author,
                upvotes: .data.ups,
                upvote_ratio: .data.upvote_ratio,
                comments: .data.num_comments,
                created_utc: .data.created_utc,
                is_video: .data.is_video,
                domain: .data.domain
            }' "$TEMP_FILE" | jq -s '.')
            
            SOURCE_JSON=$(echo "$SOURCE_JSON" | jq --argjson items "$ITEMS" '.items = $items')
            
            # 添加到主JSON
            jq --argjson source "$SOURCE_JSON" '.sources += [$source]' "$RAW_FILE" > "${RAW_FILE}.tmp" && mv "${RAW_FILE}.tmp" "$RAW_FILE"
            
            # 写入Markdown
            {
                echo "## 🤖 Reddit r/$SUBREDDIT"
                echo ""
                echo "共 $COUNT 条"
                echo ""
                
                echo "$ITEMS" | jq -r '.[] | 
                    "### \(.title)" + "\n" +
                    "- **热度**: ⬆️ \(.upvotes) upvotes (\(.upvote_ratio * 100)%), 💬 \(.comments) comments" + "\n" +
                    "- **作者**: u/\(.author)" + "\n" +
                    "- **来源**: \(.domain)" + "\n" +
                    "- **链接**: [原文](\(.url)) | [Reddit讨论](\(.permalink))" + "\n"
                '
                
                echo "---"
                echo ""
            } >> "$MARKDOWN_FILE"
            
            log "[Reddit r/$SUBREDDIT] 处理完成"
        else
            log "[Reddit r/$SUBREDDIT] ❌ 返回数据无效"
            log "[Reddit r/$SUBREDDIT] 响应内容: $(head -c 200 "$TEMP_FILE")"
        fi
    else
        log "[Reddit r/$SUBREDDIT] ❌ 请求失败"
    fi
    
    rm -f "$TEMP_FILE"
}

###############################################################################
# 主执行流程
###############################################################################

# 1. 收集Hacker News
collect_hackernews

# 2. 收集Reddit AI版块
collect_reddit "ArtificialIntelligence" 15 "Reddit - AI"

# 3. 收集Reddit机器学习版块
collect_reddit "machinelearning" 10 "Reddit - Machine Learning"

# 4. 生成统计信息
TOTAL_ITEMS=$(jq '[.sources[].items | length] | add' "$RAW_FILE")
SOURCE_COUNT=$(jq '.sources | length' "$RAW_FILE")

log "========== 收集完成 =========="
log "数据源: $SOURCE_COUNT 个"
log "总条目: $TOTAL_ITEMS 条"
log "原始数据: $RAW_FILE"
log "Markdown报告: $MARKDOWN_FILE"
log "日志: $LOG_FILE"

# 更新Markdown头部统计
sed -i.bak "s/收集时间:.*/收集时间: $(date '+%Y-%m-%d %H:%M:%S')/" "$MARKDOWN_FILE"
sed -i.bak "s/数据来源:.*/数据来源: Hacker News, Reddit | 共 $TOTAL_ITEMS 条/" "$MARKDOWN_FILE"
rm -f "$MARKDOWN_FILE.bak"

echo ""
echo "✅ 收集完成!"
echo "📁 输出目录: $OUTPUT_DIR"
echo "📊 共 $TOTAL_ITEMS 条内容"
echo "📄 Markdown报告: $MARKDOWN_FILE"
