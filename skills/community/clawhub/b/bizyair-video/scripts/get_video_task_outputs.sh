#!/bin/bash
###############################################################################
# bizyair-video - 获取视频任务结果
# 功能: 查询 BizyAir 视频生成任务状态并获取结果
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
    echo -e "${YELLOW}用法: $0 <requestId> [轮询间隔秒数]${NC}"
    echo ""
    echo "参数说明:"
    echo "  requestId    - 视频生成任务 ID"
    echo "  轮询间隔     - (可选) 每次查询间隔秒数，默认 5 秒"
    echo ""
    echo "示例:"
    echo "  $0 ca339473-aec3-469d-8ee6-a6657c38cd1c"
    echo "  $0 ca339473-aec3-469d-8ee6-a6657c38cd1c 10"
    exit 1
fi

# 获取参数
REQUEST_ID="$1"
POLL_INTERVAL="${2:-5}"

# 发送查询请求
query_task() {
    curl -s -X GET "https://api.bizyair.cn/w/v1/webapp/task/openapi/outputs?requestId=${REQUEST_ID}" \
      -H "Authorization: Bearer ${BIZYAIR_API_KEY}"
}

# 格式化毫秒为秒
format_duration() {
    local ms=$1
    local sec=$(echo "scale=1; $ms / 1000" | bc 2>/dev/null || echo "$ms")
    echo "~${sec}秒"
}

# 解析响应并显示结果
parse_and_show_result() {
    local response=$1

    # 检查是否包含错误
    if echo "$response" | grep -q '"code":[^0]'; then
        local error_msg=$(echo "$response" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
        echo -e "${RED}❌ API 返回错误${NC}"
        echo ""
        echo "错误信息: ${error_msg}"
        return 1
    fi

    # 提取状态
    local status=$(echo "$response" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)

    case "$status" in
        "Success")
            # 任务成功
            local request_id=$(echo "$response" | grep -o '"request_id":"[^"]*"' | cut -d'"' -f4)
            local cost_time=$(echo "$response" | grep -o '"cost_time":[0-9]*' | grep -o '[0-9]*$' | head -1)

            echo -e "${GREEN}✅ 视频生成完成！${NC}"
            echo ""
            echo -e "${BLUE}📊 任务详情:${NC}"
            echo ""
            echo "> 🔖 任务 ID: \`${request_id}\`"

            if [ -n "$cost_time" ]; then
                echo "> ⏱️ 生成耗时: $(format_duration $cost_time)"
            fi

            # 提取输出数量
            local output_count=$(echo "$response" | grep -o '"object_url"' | wc -l | tr -d ' ')
            echo "> 🔄 共 ${output_count} 个视频"
            echo ""

            # 生成 Markdown 表格
            echo "| 序号 | 视频 URL | 格式 |"
            echo "| --- | --- | --- |"

            local index=1
            echo "$response" | grep -o '"object_url":"[^"]*"' | while read -r line; do
                local url=$(echo "$line" | cut -d'"' -f4)
                local ext=$(echo "$response" | grep -o '"output_ext":"[^"]*"' | head -1 | cut -d'"' -f4)
                echo "| ${index} | [视频${index}](${url}) | ${ext} |"
                index=$((index + 1))
            done

            echo ""
            echo "> 📥 视频预览和下载链接已生成"
            return 0
            ;;

        "Processing"|"Pending"|"Running")
            # 任务进行中
            echo -e "${YELLOW}⏳ 任务状态: ${status}${NC}"
            echo -e "${YELLOW}💡 视频正在生成中，请稍后再次查询...${NC}"
            return 2
            ;;

        "Failed"|"Error")
            # 任务失败
            local error_msg=$(echo "$response" | grep -o '"error_message":"[^"]*"' | cut -d'"' -f4)
            if [ -z "$error_msg" ]; then
                error_msg=$(echo "$response" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
            fi

            echo -e "${RED}❌ 视频生成任务失败${NC}"
            echo ""
            echo "🔖 任务 ID: ${REQUEST_ID}"
            if [ -n "$error_msg" ]; then
                echo "❌ 错误信息: ${error_msg}"
            fi
            echo ""
            echo "💡 可能的原因:"
            echo "  • 提示词包含敏感内容"
            echo "  • 图片 URL 无法访问"
            echo "  • 参数配置错误"
            echo "  • 服务端临时异常"
            echo ""
            echo "建议:"
            echo "  1. 检查提示词内容"
            echo "  2. 确认图片 URL 可访问"
            echo "  3. 稍后重试"
            return 1
            ;;

        *)
            # 未知状态
            echo -e "${RED}❌ 未知任务状态: ${status}${NC}"
            echo ""
            echo "API 响应: ${response}"
            return 1
            ;;
    esac
}

# 主流程
echo -e "${BLUE}🔍 查询视频任务结果...${NC}"
echo "🔖 任务 ID: ${REQUEST_ID}"
echo "⏱️ 轮询间隔: ${POLL_INTERVAL} 秒"
echo ""

# 首次查询
RESPONSE=$(query_task)
parse_and_show_result "$RESPONSE"
result=$?

# 如果任务进行中，进入轮询模式
if [ $result -eq 2 ]; then
    echo ""
    echo -e "${YELLOW}💡 将自动轮询任务状态... (Ctrl+C 退出)${NC}"
    echo ""

    while true; do
        sleep "$POLL_INTERVAL"

        RESPONSE=$(query_task)
        parse_and_show_result "$RESPONSE"
        result=$?

        # 如果任务完成或失败，退出轮询
        if [ $result -eq 0 ] || [ $result -eq 1 ]; then
            exit $result
        fi
    done
fi

exit $result
