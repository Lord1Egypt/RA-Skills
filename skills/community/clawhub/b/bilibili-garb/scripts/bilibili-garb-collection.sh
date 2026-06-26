#!/bin/bash
# Bilibili Garb Collection Query v7.5 (sanitized)
# 查询收藏集/套装详情 - 数据来源：B站官方API + 藏馆数据库回退
# 输出格式：Markdown

ID=""
while getopts "i:" opt; do
    case $opt in
        i) ID="$OPTARG" ;;
    esac
done

[ -z "$ID" ] && ID="$1"
[ -z "$ID" ] && echo "用法: $0 -i <ID>" && exit 1
[[ ! "$ID" =~ ^[0-9]+$ ]] && echo "错误：ID必须为纯数字" && exit 1

# Configurable paths (set via environment or defaults)
DB_PATH="${BILI_GARB_DB:-}"
CARD_DB="${BILI_CARD_DB:-}"
SUIT_DB="${BILI_SUIT_DB:-}"
ACCESS_KEY="${BILI_ACCESS_KEY:-}"

APPKEY="27eb53fc9058f8c3"
API_URL="https://api.bilibili.com/x/garb/v2/mall/home/search"

echo ""

# 从藏馆数据库获取基本信息（支持 biz_id 和 item_id 匹配）
get_gallery_info() {
    local ID="$1"
    [ -z "$CARD_DB" ] && return
    # 先匹配 biz_id（第4列）
    local RESULT=$(grep "|.*|.*| ${ID} |" "$CARD_DB" 2>/dev/null | head -1)
    if [ -z "$RESULT" ]; then
        # 再匹配 item_id（第5列）
        RESULT=$(awk -F'|' -v id="$ID" '{
            gsub(/^[ \t]+|[ \t]+$/, "", $5)
            if ($5 == id) print $0
        }' "$CARD_DB" 2>/dev/null | head -1)
    fi
    echo "$RESULT"
}

# 从藏馆数据库的 item_id 获取对应的 biz_id
get_biz_id_from_item_id() {
    local ITEM_ID="$1"
    [ -z "$CARD_DB" ] && return
    awk -F'|' -v item_id="$ITEM_ID" '{
        gsub(/^[ \t]+|[ \t]+$/, "", $5)
        gsub(/^[ \t]+|[ \t]+$/, "", $4)
        if ($5 == item_id && $4 != "" && $4 != "null") print $4
    }' "$CARD_DB" 2>/dev/null | head -1
}

# 从藏馆装扮数据库获取信息
get_suit_info() {
    local ID="$1"
    [ -z "$SUIT_DB" ] && return
    grep "|.*|.*| ${ID} |" "$SUIT_DB" 2>/dev/null | head -1
}

# 先检查装扮数据库（无论ID长度）
SUIT_INFO=$(get_suit_info "$ID")
if [ -n "$SUIT_INFO" ]; then
    echo "📌 检测到藏馆装扮数据库记录"
    FORCE_SUIT=1
fi

# 如果没有找到装扮，检查收藏集数据库的 item_id
if [ -z "$SUIT_INFO" ] && [ ${#ID} -gt 6 ]; then
    BIZ_ID=$(get_biz_id_from_item_id "$ID")
    if [ -n "$BIZ_ID" ]; then
        ID="$BIZ_ID"
        echo "📌 检测到收藏集 item_id，转换为 biz_id: ${ID}"
    fi
fi

# 判断类型：先检查强制套装，再按位数判断
if [ "$FORCE_SUIT" = "1" ] || [ ${#ID} -gt 6 ]; then
    # ========== 套装模式 ==========
    RESPONSE=$(curl -s "https://api.bilibili.com/x/garb/v2/mall/suit/detail?item_id=${ID}&part=suit")
    
    NAME=$(echo "$RESPONSE" | jq -r '.data.name // "未知"')
    
    # 如果官方API找不到，回退到藏馆装扮数据库
    if [ "$NAME" = "未知" ] || [ -z "$NAME" ]; then
        if [ -n "$SUIT_INFO" ]; then
            SUIT_NAME=$(echo "$SUIT_INFO" | awk -F'|' '{gsub(/^[ \t]+|[ \t]+$/, "", $3); print $3}')
            SUIT_TYPE=$(echo "$SUIT_INFO" | awk -F'|' '{gsub(/^[ \t]+|[ \t]+$/, "", $5); print $5}')
            
            echo "## ${SUIT_NAME}"
            echo ""
            echo "| 属性 | 值 |"
            echo "|------|------|"
            echo "| **装扮ID** | [${ID}](https://www.bilibili.com/h5/mall/suit/detail?item_id=${ID}) |"
            echo "| **类型** | ${SUIT_TYPE} |"
            echo "| **来源** | 藏馆数据库（官方API无数据） |"
            echo "| **状态** | 可能绝版 |"
            echo ""
            
            # 尝试从B站搜索API获取图片
            ENCODED=$(printf '%s' "$SUIT_NAME" | jq -sRr @uri)
            SEARCH_IMG=$(curl -s "${API_URL}?key_word=${ENCODED}&pn=1&ps=5&mobi_app=iphone&platform=ios&appkey=${APPKEY}" 2>/dev/null | jq -r '.data.list[0].properties.image_cover // empty' 2>/dev/null)
            
            if [ -n "$SEARCH_IMG" ]; then
                echo "**封面图**："
                echo "<qqimg>${SEARCH_IMG}</qqimg>"
            else
                echo "⚠️ 此装扮已下架，无法获取图片"
            fi
        else
            echo "❌ 未找到套装 ID: ${ID}"
            echo ""
            echo "提示：此装扮可能已下架或ID错误"
        fi
        exit 0
    fi
    
    # 所有数据来自官方API
    PRICE=$(echo "$RESPONSE" | jq -r '.data.properties.sale_bp_forever_raw // "未知"')
    TOTAL=$(echo "$RESPONSE" | jq -r '.data.properties.sale_quantity // "未知"')
    STOCK=$(echo "$RESPONSE" | jq -r '.data.properties.item_stock_surplus // "0"')
    SOLD=$((TOTAL - STOCK))
    DESC=$(echo "$RESPONSE" | jq -r '.data.properties.desc // "无描述"')
    IMAGE=$(echo "$RESPONSE" | jq -r '.data.properties.image_cover // ""')
    PORTRAIT_IMAGE=$(echo "$RESPONSE" | jq -r '.data.suit_items.space_bg[0].properties.image1_portrait // ""')
    START_TIME=$(echo "$RESPONSE" | jq -r '.data.properties.sale_time_begin // ""')
    STATUS=$(echo "$RESPONSE" | jq -r '.data.state // ""')
    
    START_DATE=""
    [ -n "$START_TIME" ] && [ "$START_TIME" != "null" ] && START_DATE=$(date -d "@$START_TIME" +"%Y-%m-%d %H:%M" 2>/dev/null)
    
    STATUS_CN=""
    [ "$STATUS" = "active" ] && STATUS_CN="销售中"
    [ "$STATUS" = "ended" ] && STATUS_CN="已结束"
    [ "$STATUS" = "pending" ] && STATUS_CN="即将开售"
    
    PRICE_YUAN="未知"
    VIP_PRICE_YUAN="未知"
    if [ "$PRICE" != "未知" ] && [ -n "$PRICE" ]; then
        PRICE_YUAN=$(awk "BEGIN {printf \"%.1f\", $PRICE/100}")
        VIP_PRICE_YUAN=$(awk "BEGIN {printf \"%.1f\", $PRICE*0.8/100}")
    fi
    
    echo "## ${NAME}"
    echo ""
    echo "| 属性 | 值 |"
    echo "|------|------|"
    echo "| **套装ID** | [${ID}](https://www.bilibili.com/h5/mall/suit/detail?item_id=${ID}) |"
    echo "| **销量** | ${SOLD} / ${TOTAL} |"
    echo "| **价格** | ${VIP_PRICE_YUAN}/${PRICE_YUAN}元 |"
    [ -n "$START_DATE" ] && echo "| **开售** | ${START_DATE} |"
    [ -n "$STATUS_CN" ] && echo "| **状态** | ${STATUS_CN} |"
    echo ""
    [ -n "$IMAGE" ] && echo "<qqimg>${IMAGE}</qqimg>"
    [ -n "$PORTRAIT_IMAGE" ] && echo "<qqimg>${PORTRAIT_IMAGE}</qqimg>"
else
    # ========== 收藏集模式 ==========
    
    FOUND=0
    KEYWORD=""
    
    # 从监控数据库获取名称
    [ -n "$DB_PATH" ] && [ -f "$DB_PATH" ] && KEYWORD=$(jq -r ".collections.\"${ID}\".name // empty" "$DB_PATH" 2>/dev/null)
    
    # 从藏馆数据库获取名称
    if [ -z "$KEYWORD" ] && [ -n "$CARD_DB" ] && [ -f "$CARD_DB" ]; then
        KEYWORD=$(grep "|.*|.*| ${ID} |" "$CARD_DB" | awk -F'|' '{gsub(/^[ \t]+|[ \t]+$/, "", $3); print $3}' | head -1)
    fi
    
    # 提取简短关键词
    if [ -n "$KEYWORD" ]; then
        KEYWORD=$(echo "$KEYWORD" | sed 's/收藏集.*//;s/·.*//;s/-.*//' | head -c 20 | sed 's/^[ \t]*//;s/[ \t]*$//')
    fi
    
    [ -z "$KEYWORD" ] && KEYWORD="$ID"
    
    # 调用搜索API
    ENCODED=$(printf '%s' "$KEYWORD" | jq -sRr @uri)
    RESPONSE=$(curl -s "${API_URL}?key_word=${ENCODED}&pn=1&ps=50&mobi_app=iphone&platform=ios&appkey=${APPKEY}")
    
    # 查找匹配ID
    for i in $(seq 0 49); do
        DLC_ACT_ID=$(echo "$RESPONSE" | jq -r ".data.list[$i].properties.dlc_act_id // empty")
        if [ "$DLC_ACT_ID" = "$ID" ]; then
            FOUND=1
            FULL_NAME=$(echo "$RESPONSE" | jq -r ".data.list[$i].name")
            SALE=$(echo "$RESPONSE" | jq -r ".data.list[$i].properties.dlc_lottery_sale_quantity")
            [ "$SALE" = "null" ] && SALE=$(echo "$RESPONSE" | jq -r ".data.list[$i].sale_count_desc")
            PRICE=$(echo "$RESPONSE" | jq -r ".data.list[$i].properties.sale_bp_forever_raw // \"未知\"")
            START_TIME=$(echo "$RESPONSE" | jq -r ".data.list[$i].properties.dlc_sale_start_time // \"\"")
            END_TIME=$(echo "$RESPONSE" | jq -r ".data.list[$i].properties.dlc_sale_end_time // \"\"")
            LOTTERY_ID=$(echo "$RESPONSE" | jq -r ".data.list[$i].properties.dlc_lottery_id // \"\"")
            IMAGE=$(echo "$RESPONSE" | jq -r ".data.list[$i].properties.image_cover // \"\"")
            STATUS=$(echo "$RESPONSE" | jq -r ".data.list[$i].state // \"\"")
            
            START_DATE=""
            END_DATE=""
            [ -n "$START_TIME" ] && [ "$START_TIME" != "null" ] && START_DATE=$(date -d "@$START_TIME" +"%Y-%m-%d %H:%M" 2>/dev/null)
            [ -n "$END_TIME" ] && [ "$END_TIME" != "null" ] && END_DATE=$(date -d "@$END_TIME" +"%Y-%m-%d" 2>/dev/null)
            
            STATUS_CN=""
            [ "$STATUS" = "active" ] && STATUS_CN="销售中"
            [ "$STATUS" = "ended" ] && STATUS_CN="已结束"
            [ "$STATUS" = "pending" ] && STATUS_CN="即将开售"
            
            PRICE_YUAN="未知"
            [ "$PRICE" != "未知" ] && [ -n "$PRICE" ] && PRICE_YUAN=$(awk "BEGIN {printf \"%.1f\", $PRICE/100}")
            
            # 获取头像框（需要 access_key）
            FRAME_IMAGE=""
            FRAME_NAME=""
            if [ -n "$LOTTERY_ID" ] && [ -n "$ACCESS_KEY" ]; then
                LOTTERY_RESPONSE=$(curl -s "https://api.bilibili.com/x/vas/dlc_act/lottery_home_detail?act_id=${ID}&lottery_id=${LOTTERY_ID}&mobi_app=iphone&platform=ios&appkey=${APPKEY}&access_key=${ACCESS_KEY}" 2>/dev/null)
                FRAME_IMAGE=$(echo "$LOTTERY_RESPONSE" | jq -r '.data.collect_list.collect_infos[] | select(.redeem_item_type==3) | .redeem_item_image' 2>/dev/null | head -1)
                FRAME_NAME=$(echo "$LOTTERY_RESPONSE" | jq -r '.data.collect_list.collect_infos[] | select(.redeem_item_type==3) | .redeem_item_name' 2>/dev/null | head -1)
            fi
            
            echo "## ${FULL_NAME}"
            echo ""
            echo "| 属性 | 值 |"
            echo "|------|------|"
            echo "| **收藏集ID** | [${ID}](https://www.bilibili.com/h5/mall/digital-card/home?act_id=${ID}) |"
            echo "| **销量** | ${SALE} |"
            echo "| **价格** | ${PRICE_YUAN}元/抽 |"
            [ -n "$START_DATE" ] && echo "| **开售** | ${START_DATE} |"
            [ -n "$END_DATE" ] && echo "| **结束** | ${END_DATE} |"
            [ -n "$STATUS_CN" ] && echo "| **状态** | ${STATUS_CN} |"
            [ -n "$FRAME_NAME" ] && echo "| **头像框** | ${FRAME_NAME} |"
            echo ""
            [ -n "$IMAGE" ] && echo "<qqimg>${IMAGE}</qqimg>"
            [ -n "$FRAME_IMAGE" ] && echo "<qqimg>${FRAME_IMAGE}</qqimg>"
            break
        fi
    done
    
    # 如果官方搜索API找不到，尝试 act/basic API
    if [ $FOUND -eq 0 ]; then
        BASIC_RESPONSE=$(curl -s "https://api.bilibili.com/x/vas/dlc_act/act/basic?act_id=${ID}&mobi_app=iphone&platform=ios&appkey=${APPKEY}" 2>/dev/null)
        ACT_TITLE=$(echo "$BASIC_RESPONSE" | jq -r '.data.act_title // empty' 2>/dev/null)
        
        if [ -n "$ACT_TITLE" ] && [ "$ACT_TITLE" != "null" ]; then
            FOUND=1
            FULL_NAME="$ACT_TITLE"
            START_TIME=$(echo "$BASIC_RESPONSE" | jq -r '.data.start_time // 0' 2>/dev/null)
            END_TIME=$(echo "$BASIC_RESPONSE" | jq -r '.data.end_time // 0' 2>/dev/null)
            PRICE=$(echo "$BASIC_RESPONSE" | jq -r '.data.lottery_list[0].price // 0' 2>/dev/null)
            SALE=$(echo "$BASIC_RESPONSE" | jq -r '.data.total_buy_cnt // 0' 2>/dev/null)
            IMAGE=$(echo "$BASIC_RESPONSE" | jq -r '.data.lottery_list[0].lottery_image // ""' 2>/dev/null)
            LOTTERY_ID=$(echo "$BASIC_RESPONSE" | jq -r '.data.lottery_list[0].lottery_id // ""' 2>/dev/null)
            STATUS="active"
            
            START_DATE=""
            END_DATE=""
            [ "$START_TIME" != "0" ] && [ -n "$START_TIME" ] && START_DATE=$(date -d "@$START_TIME" +"%Y-%m-%d %H:%M" 2>/dev/null)
            [ "$END_TIME" != "0" ] && [ -n "$END_TIME" ] && END_DATE=$(date -d "@$END_TIME" +"%Y-%m-%d" 2>/dev/null)
            
            PRICE_YUAN="未知"
            [ "$PRICE" != "0" ] && [ -n "$PRICE" ] && PRICE_YUAN=$(awk "BEGIN {printf \"%.1f\", $PRICE/1000}")
            
            # 获取头像框
            FRAME_IMAGE=""
            FRAME_NAME=""
            if [ -n "$LOTTERY_ID" ]; then
                LOTTERY_RESPONSE=$(curl -s "https://api.bilibili.com/x/vas/dlc_act/lottery_home_detail?act_id=${ID}&lottery_id=${LOTTERY_ID}&mobi_app=iphone&platform=ios&appkey=${APPKEY}" 2>/dev/null)
                FRAME_IMAGE=$(echo "$LOTTERY_RESPONSE" | jq -r '.data.collect_list.collect_infos[] | select(.redeem_item_type==3) | .redeem_item_image' 2>/dev/null | head -1)
                FRAME_NAME=$(echo "$LOTTERY_RESPONSE" | jq -r '.data.collect_list.collect_infos[] | select(.redeem_item_type==3) | .redeem_item_name' 2>/dev/null | head -1)
            fi
            
            echo "## ${FULL_NAME}"
            echo ""
            echo "| 属性 | 值 |"
            echo "|------|------|"
            echo "| **收藏集ID** | [${ID}](https://www.bilibili.com/h5/mall/digital-card/home?act_id=${ID}) |"
            echo "| **销量** | ${SALE} |"
            echo "| **价格** | ${PRICE_YUAN}元/抽 |"
            [ -n "$START_DATE" ] && echo "| **开售** | ${START_DATE} |"
            [ -n "$END_DATE" ] && echo "| **结束** | ${END_DATE} |"
            [ -n "$FRAME_NAME" ] && echo "| **头像框** | ${FRAME_NAME} |"
            echo ""
            [ -n "$IMAGE" ] && echo "<qqimg>${IMAGE}</qqimg>"
            [ -n "$FRAME_IMAGE" ] && echo "<qqimg>${FRAME_IMAGE}</qqimg>"
        fi
    fi
    
    # 如果仍然找不到，回退到藏馆数据库
    if [ $FOUND -eq 0 ] && [ -n "$CARD_DB" ] && [ -f "$CARD_DB" ]; then
        GALLERY_INFO=$(get_gallery_info "$ID")
        if [ -n "$GALLERY_INFO" ]; then
            NAME=$(echo "$GALLERY_INFO" | awk -F'|' '{print $3}' | sed 's/^[ \t]*//;s/[ \t]*$//')
            ITEM_ID=$(echo "$GALLERY_INFO" | awk -F'|' '{print $5}' | sed 's/^[ \t]*//;s/[ \t]*$//')
            HOLD=$(echo "$GALLERY_INFO" | awk -F'|' '{print $6}' | sed 's/^[ \t]*//;s/[ \t]*$//')
            STATUS=$(echo "$GALLERY_INFO" | awk -F'|' '{print $7}' | sed 's/^[ \t]*//;s/[ \t]*$//')
            
            echo "## ${NAME}"
            echo ""
            echo "| 属性 | 值 |"
            echo "|------|------|"
            echo "| **收藏集ID** | ${ID} |"
            echo "| **来源** | 藏馆数据库（官方API无数据） |"
            [ -n "$ITEM_ID" ] && [ "$ITEM_ID" != "null" ] && echo "| **商品ID** | ${ITEM_ID} |"
            [ -n "$HOLD" ] && echo "| **持有** | ${HOLD} |"
            [ -n "$STATUS" ] && echo "| **状态** | ${STATUS} |"
            echo ""
            echo "⚠️ 此收藏集可能已下架，无法获取更多信息"
        else
            echo "❌ 未找到收藏集 ID: ${ID}"
            echo ""
            echo "提示：此收藏集可能已下架或ID错误"
        fi
    fi
fi
