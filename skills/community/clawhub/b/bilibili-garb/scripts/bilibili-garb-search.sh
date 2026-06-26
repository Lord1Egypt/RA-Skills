#!/bin/bash
# Bilibili Garb Search v8.3 (sanitized)
# 搜索收藏集/套装 - 官方API优先，藏馆补充说明
# 输出格式：收藏集输出biz_id，套装输出item_id

API_URL="https://api.bilibili.com/x/garb/v2/mall/home/search"
APPKEY="27eb53fc9058f8c3"

# Gallery databases (optional, set these to your local data paths)
CARD_DB="${BILI_CARD_DB:-}"
SUIT_DB="${BILI_SUIT_DB:-}"

KEYWORD=$2
[ -z "$KEYWORD" ] && KEYWORD=$1
[ -z "$KEYWORD" ] && echo "用法: $0 关键词" && exit 1

echo ""
echo "## 搜索「${KEYWORD}」"
echo ""

# 用于去重的ID集合
declare -A SEEN_IDS

# 从藏馆获取补充信息（持有数、状态等）
get_gallery_hold() {
    local ID="$1"
    [ -z "$CARD_DB" ] && return
    grep "|.*|.*| ${ID} |" "$CARD_DB" 2>/dev/null | awk -F'|' '{gsub(/^[ \t]+|[ \t]+$/, "", $6); print $6}' | head -1
}

get_suit_type() {
    local ID="$1"
    [ -z "$SUIT_DB" ] && return
    grep "|.*|.*| ${ID} |" "$SUIT_DB" 2>/dev/null | awk -F'|' '{gsub(/^[ \t]+|[ \t]+$/, "", $5); print $5}' | head -1
}

# 1. 先搜索官方API（优先）
ENCODED=$(printf '%s' "$KEYWORD" | jq -sRr @uri)
RESPONSE=$(curl -s "${API_URL}?key_word=${ENCODED}&pn=1&ps=20&mobi_app=iphone&platform=ios&appkey=${APPKEY}")
TOTAL=$(echo "$RESPONSE" | jq -r '.data.list | length')

API_COUNT=0
for i in $(seq 0 $((TOTAL-1))); do
    NAME=$(echo "$RESPONSE" | jq -r ".data.list[$i].name")
    ITEM_ID=$(echo "$RESPONSE" | jq -r ".data.list[$i].item_id")
    DLC_ACT_ID=$(echo "$RESPONSE" | jq -r ".data.list[$i].properties.dlc_act_id")
    SALE=$(echo "$RESPONSE" | jq -r ".data.list[$i].sale_count_desc")
    STATUS=$(echo "$RESPONSE" | jq -r ".data.list[$i].state")
    
    # 收藏集：有dlc_act_id
    if [ "$DLC_ACT_ID" != "null" ] && [ -n "$DLC_ACT_ID" ]; then
        REAL_SALE=$(echo "$RESPONSE" | jq -r ".data.list[$i].properties.dlc_lottery_sale_quantity")
        [ "$REAL_SALE" != "null" ] && [ -n "$REAL_SALE" ] && SALE="$REAL_SALE"
        
        QUERY_ID="${DLC_ACT_ID}"
        SEEN_IDS["$QUERY_ID"]=1
        
        # 藏馆补充信息
        HOLD_INFO=$(get_gallery_hold "$QUERY_ID")
        
        STATUS_CN=""
        [ "$STATUS" = "active" ] && STATUS_CN="销售中"
        [ "$STATUS" = "ended" ] && STATUS_CN="已结束"
        [ "$STATUS" = "pending" ] && STATUS_CN="即将开售"
        
        echo "### ${NAME} \`[官方]\`"
        echo "- **类型**: 收藏集"
        echo "- **ID**: [${QUERY_ID}](https://www.bilibili.com/h5/mall/digital-card/home?act_id=${QUERY_ID})"
        [ -n "$ITEM_ID" ] && [ "$ITEM_ID" != "0" ] && [ "$ITEM_ID" != "null" ] && echo "  (商品item_id: ${ITEM_ID})"
        echo "- **销量**: ${SALE}"
        [ -n "$STATUS_CN" ] && echo "- **状态**: ${STATUS_CN}"
        [ -n "$HOLD_INFO" ] && echo "- **持有**: ${HOLD_INFO} \`[藏馆补充]\`"
        echo ""
        ((API_COUNT++))
    # 套装：有item_id且无dlc_act_id
    elif [ "$ITEM_ID" != "0" ] && [ -n "$ITEM_ID" ]; then
        TOTAL_QTY=$(echo "$RESPONSE" | jq -r ".data.list[$i].properties.sale_quantity")
        STOCK=$(echo "$RESPONSE" | jq -r ".data.list[$i].properties.item_stock_surplus")
        if [ "$TOTAL_QTY" != "null" ] && [ "$STOCK" != "null" ]; then
            SALE="$((TOTAL_QTY - STOCK)) / ${TOTAL_QTY}"
        fi
        
        QUERY_ID="${ITEM_ID}"
        SEEN_IDS["$QUERY_ID"]=1
        
        STATUS_CN=""
        [ "$STATUS" = "active" ] && STATUS_CN="销售中"
        [ "$STATUS" = "ended" ] && STATUS_CN="已结束"
        [ "$STATUS" = "pending" ] && STATUS_CN="即将开售"
        
        echo "### ${NAME} \`[官方]\`"
        echo "- **类型**: 套装"
        echo "- **ID**: [${QUERY_ID}](https://www.bilibili.com/h5/mall/suit/detail?item_id=${QUERY_ID})"
        echo "- **销量**: ${SALE}"
        [ -n "$STATUS_CN" ] && echo "- **状态**: ${STATUS_CN}"
        echo ""
        ((API_COUNT++))
    fi
done

# 2. 藏馆独有的（官方API查不到的绝版）
GALLERY_ONLY=0
if [ -n "$CARD_DB" ] && [ -f "$CARD_DB" ]; then
    while IFS= read -r line; do
        [[ "$line" =~ ^\|.*\|$ ]] || continue
        [[ "$line" =~ ^\|[[:space:]]*# ]] && continue
        [[ "$line" =~ ^\|[-[:space:]]+\| ]] && continue
        
        NAME=$(echo "$line" | awk -F'|' '{print $3}' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        BIZ_ID=$(echo "$line" | awk -F'|' '{print $4}' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        ITEM_ID=$(echo "$line" | awk -F'|' '{print $5}' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        HOLD=$(echo "$line" | awk -F'|' '{print $6}' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        STATUS=$(echo "$line" | awk -F'|' '{print $7}' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        
        [ -z "$NAME" ] || [ -z "$BIZ_ID" ] && continue
        
        QUERY_ID="${BIZ_ID}"
        
        # 只显示官方没有的（绝版）
        if [ "${SEEN_IDS[$QUERY_ID]}" = "1" ]; then
            continue
        fi
        
        SEEN_IDS["$QUERY_ID"]=1
        
        echo "### ${NAME} \`[藏馆-绝版]\`"
        echo "- **类型**: 收藏集"
        echo "- **ID**: [${QUERY_ID}](https://www.bilibili.com/h5/mall/digital-card/home?act_id=${QUERY_ID})"
        [ -n "$ITEM_ID" ] && [ "$ITEM_ID" != "null" ] && echo "  (商品item_id: ${ITEM_ID})"
        echo "- **持有**: ${HOLD}"
        [ -n "$STATUS" ] && echo "- **状态**: ${STATUS}"
        echo ""
        ((GALLERY_ONLY++))
    done < <(grep -Fi "$KEYWORD" "$CARD_DB")
fi

# 3. 藏馆绝版装扮（官方没有的）
SUIT_ONLY=0
if [ -n "$SUIT_DB" ] && [ -f "$SUIT_DB" ]; then
    while IFS= read -r line; do
        [[ "$line" =~ ^\|.*\|$ ]] || continue
        [[ "$line" =~ ^\|[[:space:]]*# ]] && continue
        [[ "$line" =~ ^\|[-[:space:]]+\| ]] && continue
        
        NAME=$(echo "$line" | awk -F'|' '{print $3}' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        ITEM_ID=$(echo "$line" | awk -F'|' '{print $4}' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        TYPE=$(echo "$line" | awk -F'|' '{print $5}' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        
        [ -z "$NAME" ] || [ -z "$ITEM_ID" ] && continue
        
        QUERY_ID="${ITEM_ID}"
        
        # 只显示官方没有的
        if [ "${SEEN_IDS[$QUERY_ID]}" = "1" ]; then
            continue
        fi
        
        SEEN_IDS["$QUERY_ID"]=1
        
        echo "### ${NAME} \`[藏馆-绝版]\`"
        echo "- **类型**: ${TYPE}"
        echo "- **ID**: [${QUERY_ID}](https://www.bilibili.com/h5/mall/suit/detail?item_id=${QUERY_ID})"
        echo "- **状态**: 绝版"
        echo ""
        ((SUIT_ONLY++))
    done < <(grep -Fi "$KEYWORD" "$SUIT_DB")
fi

# 4. 汇总
echo "---"
echo "📊 **搜索结果**: 官方 ${API_COUNT} 个 | 藏馆绝版收藏集 ${GALLERY_ONLY} 个 | 藏馆绝版装扮 ${SUIT_ONLY} 个"
echo ""
echo "**提示**: 用查询命令查看详情"
echo "- 收藏集ID（≤6位）查询收藏集详情"
echo "- 套装ID（>6位）查询套装详情"
