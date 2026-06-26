#!/bin/bash
###############################################################################
# bozo-jiaodu - 获取任务结果
# 功能: 查询 BizyAir 任务状态并获取生成的图片
###############################################################################

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查环境变量
if [ -z "$BIZYAIR_API_KEY" ]; then
    echo -e "${RED}❌ 错误: 环境变量 BIZYAIR_API_KEY 未设置${NC}"
    echo "💡 请设置环境变量: export BIZYAIR_API_KEY=\"your_api_key_here\""
    exit 1
fi

# 参数检查
if [ $# -lt 1 ]; then
    echo -e "${YELLOW}用法: $0 <requestId> [轮询间隔]${NC}"
    echo ""
    echo "参数说明:"
    echo "  requestId     - 任务 ID（创建任务时返回的）"
    echo "  轮询间隔      - (可选) 查询间隔秒数，默认 5 秒"
    echo ""
    echo "示例:"
    echo "  $0 ca339473-aec3-469d-8ee6-a6657c38cd1c"
    echo "  $0 ca339473-aec3-469d-8ee6-a6657c38cd1c 10"
    exit 1
fi

# 获取参数
REQUEST_ID="$1"
POLL_INTERVAL="${2:-5}"

echo -e "${BLUE}🔍 查询任务结果...${NC}"
echo "🔖 任务 ID: ${REQUEST_ID}"
echo "⏱️ 轮询间隔: ${POLL_INTERVAL} 秒"
echo ""

# 轮询查询任务状态
while true; do
    # 获取任务状态
    RESPONSE=$(curl -s -X GET "https://api.bizyair.cn/w/v1/webapp/task/openapi/outputs?requestId=${REQUEST_ID}" \
      -H "Authorization: Bearer ${BIZYAIR_API_KEY}")

    # 解析状态 - 兼容不同的字段名和位置
    STATUS=$(echo "$RESPONSE" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)

    # 如果 data.status 存在，优先使用
    DATA_STATUS=$(echo "$RESPONSE" | grep -o '"data":\[{"[^]]*"status":"[^"]*"' | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
    if [ -n "$DATA_STATUS" ]; then
        STATUS="$DATA_STATUS"
    fi

    if [ "$STATUS" = "Success" ]; then
        echo -e "${GREEN}✅ 任务完成！${NC}"
        echo ""
        echo -e "${BLUE}📊 任务详情:${NC}"
        echo ""

        # 提取输出信息
        OUTPUT_COUNT=$(echo "$RESPONSE" | grep -o '"object_url"' | wc -l | tr -d ' ')

        if [ "$OUTPUT_COUNT" -gt 0 ]; then
            echo -e "${GREEN}### 🎨 摄像机角度调整结果${NC}"
            echo ""
            echo "> 🔖 任务 ID: \`${REQUEST_ID}\`"

            # 提取耗时信息
            COST_TIME=$(echo "$RESPONSE" | grep -o '"cost_time":[0-9]*' | head -1 | cut -d':' -f2)
            if [ -n "$COST_TIME" ]; then
                COST_SEC=$(echo "scale=1; $COST_TIME / 1000" | bc 2>/dev/null || echo "$COST_TIME")
                echo "> ⏱️ 生成耗时: ~${COST_SEC} 秒"
            fi
            echo "> 🔄 共 ${OUTPUT_COUNT} 张图片"
            echo ""

            # 生成 Markdown 表格
            echo "| 序号 | 预览 | 图片 URL |"
            echo "| --- | --- | --- |"

            INDEX=1
            echo "$RESPONSE" | grep -o '"object_url":"[^"]*"' | while read -r line; do
                URL=$(echo "$line" | cut -d'"' -f4)
                echo "| ${INDEX} | ![图片${INDEX}](${URL}) | ${URL} |"
                INDEX=$((INDEX + 1))
            done

            echo ""
            echo "> 📥 如需下载图片，请提供保存路径"
        else
            echo -e "${YELLOW}⚠️ 任务完成但没有生成图片${NC}"
            echo "API 响应: ${RESPONSE}"
        fi
        exit 0

    elif [ "$STATUS" = "Failed" ]; then
        echo -e "${RED}❌ 任务执行失败${NC}"
        echo ""
        echo "🔖 任务 ID: ${REQUEST_ID}"
        echo "API 响应: ${RESPONSE}"
        echo ""
        echo "💡 建议:"
        echo "  • 检查摄像机提示词格式是否正确"
        echo "  • 确认原始图片 URL 可访问"
        echo "  • 稍后使用相同参数重试"
        exit 1

    elif [ "$STATUS" = "Pending" ] || [ "$STATUS" = "Processing" ] || [ "$STATUS" = "Accepted" ]; then
        echo -e "${YELLOW}⏳ 任务进行中... (${STATUS})${NC}"
        echo "💡 等待 ${POLL_INTERVAL} 秒后重新查询..."
        echo ""
        sleep $POLL_INTERVAL

    elif [ -z "$STATUS" ]; then
        # 无法解析状态，可能任务不存在或 API 返回格式变化
        echo -e "${YELLOW}📡 无法解析任务状态${NC}"
        echo "API 响应: ${RESPONSE}"
        echo ""
        echo "💡 请确认任务 ID 是否正确"
        exit 1

    else
        echo -e "${YELLOW}📡 未知状态: ${STATUS}${NC}"
        echo "API 响应: ${RESPONSE}"
        echo ""
        echo "💡 等待 ${POLL_INTERVAL} 秒后重新查询..."
        echo ""
        sleep $POLL_INTERVAL
    fi
done
