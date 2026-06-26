#!/bin/bash
###############################################################################
# bozo-jiaodu - 创建摄像机角度调整任务
# 功能: 调用 BizyAir API 创建图片角度调整任务（支持同步/异步返回）
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
if [ $# -lt 2 ]; then
    echo -e "${YELLOW}用法: $0 <图片URL> <摄像机提示词> [web_app_id]${NC}"
    echo ""
    echo "参数说明:"
    echo "  图片URL        - 要调整角度的原始图片URL"
    echo "  摄像机提示词   - 以 <sks> 开头的96个标准摄像机位置提示词之一"
    echo "  web_app_id     - (可选) BizyAir 工作流ID，默认 43531"
    echo ""
    echo "示例:"
    echo "  $0 \"https://example.com/image.png\" \"<sks> left side view low-angle shot close-up\""
    echo "  $0 \"https://example.com/image.png\" \"<sks> front view eye-level shot medium shot\" 43531"
    exit 1
fi

# 获取参数
IMAGE_URL="$1"
CAMERA_PROMPT="$2"
WEB_APP_ID="${3:-43531}"

# 验证摄像机提示词格式
if [[ ! "$CAMERA_PROMPT" =~ ^\<sks\>\ .+ ]]; then
    echo -e "${RED}❌ 错误: 摄像机提示词必须以 <sks> 开头${NC}"
    echo "💡 正确格式示例: <sks> left side view low-angle shot close-up"
    exit 1
fi

# 构建请求数据
REQUEST_DATA=$(cat <<EOF
{
  "web_app_id": ${WEB_APP_ID},
  "suppress_preview_output": false,
  "input_values": {
    "41:LoadImage.image": "${IMAGE_URL}",
    "112:TextEncodeQwenImageEditPlus.prompt": "${CAMERA_PROMPT}\n"
  }
}
EOF
)

# 发送 API 请求
echo -e "${GREEN}📤 正在创建摄像机角度调整任务...${NC}"
echo "📷 图片 URL: ${IMAGE_URL}"
echo "🎬 摄像机提示词: ${CAMERA_PROMPT}"
echo ""

RESPONSE=$(curl -s -X POST "https://api.bizyair.cn/w/v1/webapp/task/openapi/create" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${BIZYAIR_API_KEY}" \
  -d "$REQUEST_DATA")

# 检查响应是否包含 outputs（同步返回，任务已完成）
if echo "$RESPONSE" | grep -q '"outputs"'; then
    # 同步返回 - 任务已完成
    echo -e "${GREEN}✅ 角度调整完成！${NC}"
    echo ""
    echo -e "${BLUE}📊 任务详情:${NC}"
    echo ""

    # 提取 request_id
    REQUEST_ID=$(echo "$RESPONSE" | grep -o '"request_id":"[^"]*"' | cut -d'"' -f4)
    if [ -n "$REQUEST_ID" ]; then
        echo "> 🔖 任务 ID: \`${REQUEST_ID}\`"
    fi

    # 提取耗时
    COST_TIME=$(echo "$RESPONSE" | grep -o '"total_cost_time":[0-9]*' | cut -d':' -f2)
    if [ -n "$COST_TIME" ]; then
        COST_SEC=$(echo "scale=1; $COST_TIME / 1000" | bc 2>/dev/null || echo "$COST_TIME")
        echo "> ⏱️ 处理耗时: ~${COST_SEC} 秒"
    fi

    # 提取输出数量
    OUTPUT_COUNT=$(echo "$RESPONSE" | grep -o '"object_url"' | wc -l | tr -d ' ')
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

# 检查响应是否包含 requestId/request_id（异步返回，任务进行中）
elif echo "$RESPONSE" | grep -q '"requestId"\|"request_id"'; then
    # 异步返回 - 需要查询结果
    REQUEST_ID=$(echo "$RESPONSE" | grep -o '"requestId":"[^"]*"' | cut -d'"' -f4)
    if [ -z "$REQUEST_ID" ]; then
        REQUEST_ID=$(echo "$RESPONSE" | grep -o '"request_id":"[^"]*"' | cut -d'"' -f4)
    fi

    echo -e "${GREEN}✅ 任务创建成功！${NC}"
    echo ""
    echo "🔖 任务 ID: ${REQUEST_ID}"
    echo ""
    echo -e "${YELLOW}⏳ 图片正在后台处理中...${NC}"
    echo "💡 使用以下命令查询结果:"
    echo "   bash scripts/get_task_outputs.sh ${REQUEST_ID}"

# 检查是否包含错误信息
elif echo "$RESPONSE" | grep -q '"error"\|"message"' && ! echo "$RESPONSE" | grep -q '"status":"Success"'; then
    echo -e "${RED}❌ API 返回错误${NC}"
    echo ""
    echo "API 响应: ${RESPONSE}"
    echo ""
    echo "💡 可能原因:"
    echo "  • BIZYAIR_API_KEY 无效或已过期"
    echo "  • 图片 URL 无法访问"
    echo "  • 请求参数格式错误"

else
    echo -e "${RED}❌ 未知响应格式${NC}"
    echo ""
    echo "API 响应: ${RESPONSE}"
    echo ""
    echo "💡 可能原因:"
    echo "  • API 返回格式发生变化"
    echo "  • 网络连接不稳定"
fi
