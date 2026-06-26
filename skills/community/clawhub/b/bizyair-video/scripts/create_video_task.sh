#!/bin/bash
###############################################################################
# bizyair-video - 创建视频生成任务
# 功能: 调用 BizyAir 异步 API 创建视频生成任务
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

# 显示用法
show_usage() {
    echo -e "${YELLOW}用法: $0 <web_app_id> <参数JSON>${NC}"
    echo ""
    echo "📐 默认参数: width=720, height=1280 (竖屏), num_frames=81 (5秒)"
    echo ""
    echo "支持的 video modes:"
    echo "  41538  - 图生视频 KJ高速版"
    echo "  41863  - 图生视频 Wan2.2_NSFW"
    echo "  44773  - 图生视频 Wan2.2_Remix_NSFW"
    echo "  39388  - 首尾帧视频 三分钟版本"
    echo "  44750  - 首尾帧视频 Wan2.2_Remix_NSFW (1280高)"
    echo ""
    echo "🎬 帧数转换 (16帧 = 1秒):"
    echo "  17帧=1秒 | 33帧=2秒 | 49帧=3秒 | 65帧=4秒 | 81帧=5秒(默认)"
    echo "  97帧=6秒 | 113帧=7秒 | 129帧=8秒"
    echo "  公式: 帧数 = 时长(秒) × 16 + 1"
    echo ""
    echo "图生视频参数 JSON 格式:"
    echo '  {"positive_prompt": "提示词", "image_url": "图片URL", "width": 720, "height": 1280, "num_frames": 81}'
    echo ""
    echo "首尾帧视频参数 JSON 格式:"
    echo '  {"first_frame_url": "首帧URL", "last_frame_url": "尾帧URL", "width": 720, "height": 720, "num_frames": 81}'
    echo ""
    echo "💡 提示: width/height 可自定义，默认 720×1280 (9:16竖屏)"
    echo ""
    echo "示例:"
    echo "  $0 41538 '{\"positive_prompt\": \"机器人转身\", \"image_url\": \"https://example.com/img.png\"}'"
    echo "  $0 39388 '{\"first_frame_url\": \"https://example.com/frame1.png\", \"last_frame_url\": \"https://example.com/frame2.png\"}'"
    exit 1
}

# 参数检查
if [ $# -lt 2 ]; then
    show_usage
fi

# 获取参数
WEB_APP_ID="$1"
PARAMS_JSON="$2"

# 验证 web_app_id
case "$WEB_APP_ID" in
    41538|41863|44773|39388|44750)
        # 有效的 web_app_id
        ;;
    *)
        echo -e "${RED}❌ 错误: 无效的 web_app_id: ${WEB_APP_ID}${NC}"
        echo ""
        show_usage
        ;;
esac

# 解析 JSON 参数
parse_json() {
    echo "$1" | grep -o "\"$2\"\s*:\s*\"[^\"]*\"" | cut -d'"' -f4
}

parse_json_int() {
    echo "$1" | grep -o "\"$2\"\s*:\s*[0-9]*" | grep -o "[0-9]*$"
}

# 构建请求数据
build_request_data() {
    local web_app_id=$1
    local params=$2

    case "$web_app_id" in
        41538)
            # 图生视频 - KJ高速版
            local positive_prompt=$(parse_json "$params" "positive_prompt")
            local image_url=$(parse_json "$params" "image_url")
            local width=$(parse_json_int "$params" "width")
            local height=$(parse_json_int "$params" "height")
            local num_frames=$(parse_json_int "$params" "num_frames")

            # 设置默认值
            width=${width:-720}
            height=${height:-1280}
            num_frames=${num_frames:-81}

            cat <<EOF
{
  "web_app_id": ${web_app_id},
  "suppress_preview_output": false,
  "input_values": {
    "16:WanVideoTextEncode.positive_prompt": "${positive_prompt}",
    "67:LoadImage.image": "${image_url}",
    "68:ImageResizeKJv2.width": ${width},
    "68:ImageResizeKJv2.height": ${height},
    "89:WanVideoImageToVideoEncode.num_frames": ${num_frames}
  }
}
EOF
            ;;
        41863)
            # 图生视频 - Wan2.2_NSFW
            local image_url=$(parse_json "$params" "image_url")
            local text=$(parse_json "$params" "text")
            local width=$(parse_json_int "$params" "width")
            local height=$(parse_json_int "$params" "height")
            local length=$(parse_json_int "$params" "length")

            # 设置默认值
            width=${width:-720}
            height=${height:-1280}
            length=${length:-81}

            cat <<EOF
{
  "web_app_id": ${web_app_id},
  "suppress_preview_output": false,
  "input_values": {
    "106:LoadImage.image": "${image_url}",
    "6:CLIPTextEncode.text": "${text}",
    "107:WanImageToVideo.width": ${width},
    "107:WanImageToVideo.height": ${height},
    "107:WanImageToVideo.length": ${length}
  }
}
EOF
            ;;
        44773)
            # 图生视频 - Wan2.2_Remix_NSFW
            local image_url=$(parse_json "$params" "image_url")
            local positive_prompt=$(parse_json "$params" "positive_prompt")
            local width=$(parse_json_int "$params" "width")
            local height=$(parse_json_int "$params" "height")
            local num_frames=$(parse_json_int "$params" "num_frames")

            # 设置默认值
            width=${width:-720}
            height=${height:-1280}
            num_frames=${num_frames:-81}

            cat <<EOF
{
  "web_app_id": ${web_app_id},
  "suppress_preview_output": false,
  "input_values": {
    "67:LoadImage.image": "${image_url}",
    "89:WanVideoImageToVideoEncode.num_frames": ${num_frames},
    "16:WanVideoTextEncode.positive_prompt": "${positive_prompt}",
    "68:ImageResizeKJv2.width": ${width},
    "68:ImageResizeKJv2.height": ${height}
  }
}
EOF
            ;;
        39388)
            # 首尾帧视频 - 三分钟版本
            local first_frame_url=$(parse_json "$params" "first_frame_url")
            local last_frame_url=$(parse_json "$params" "last_frame_url")
            local width=$(parse_json_int "$params" "width")
            local height=$(parse_json_int "$params" "height")
            local num_frames=$(parse_json_int "$params" "num_frames")

            # 设置默认值
            width=${width:-720}
            height=${height:-720}
            num_frames=${num_frames:-81}

            cat <<EOF
{
  "web_app_id": ${web_app_id},
  "suppress_preview_output": false,
  "input_values": {
    "67:LoadImage.image": "${first_frame_url}",
    "99:LoadImage.image": "${last_frame_url}",
    "100:easy int.value": ${width},
    "101:easy int.value": ${height},
    "89:WanVideoImageToVideoEncode.num_frames": ${num_frames}
  }
}
EOF
            ;;
        44750)
            # 首尾帧视频 - Wan2.2_Remix_NSFW (1280高)
            local first_frame_url=$(parse_json "$params" "first_frame_url")
            local last_frame_url=$(parse_json "$params" "last_frame_url")
            local positive_prompt=$(parse_json "$params" "positive_prompt")
            local num_frames=$(parse_json_int "$params" "num_frames")

            # 设置默认值
            num_frames=${num_frames:-81}
            positive_prompt=${positive_prompt:-""}

            cat <<EOF
{
  "web_app_id": ${web_app_id},
  "suppress_preview_output": false,
  "input_values": {
    "52:LoadImage.image": "${first_frame_url}",
    "53:LoadImage.image": "${last_frame_url}",
    "26:JWInteger.value": ${num_frames},
    "30:WanVideoTextEncode.positive_prompt": "${positive_prompt}"
  }
}
EOF
            ;;
    esac
}

# 获取视频模式名称
get_mode_name() {
    case "$1" in
        41538) echo "图生视频 - KJ高速版" ;;
        41863) echo "图生视频 - Wan2.2_NSFW" ;;
        44773) echo "图生视频 - Wan2.2_Remix_NSFW" ;;
        39388) echo "首尾帧视频 - 三分钟版本" ;;
        44750) echo "首尾帧视频 - Wan2.2_Remix_NSFW" ;;
        *) echo "未知模式" ;;
    esac
}

# 构建请求数据
REQUEST_DATA=$(build_request_data "$WEB_APP_ID" "$PARAMS_JSON")

# 发送 API 请求
echo -e "${GREEN}📤 正在创建视频生成任务...${NC}"
echo "🎬 视频模式: $(get_mode_name $WEB_APP_ID)"
echo "🔧 工作流 ID: ${WEB_APP_ID}"
echo ""

RESPONSE=$(curl -s -X POST "https://api.bizyair.cn/w/v1/webapp/task/openapi/create" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${BIZYAIR_API_KEY}" \
  -H "X-Bizyair-Task-Async: enable" \
  -d "$REQUEST_DATA")

# 解析响应
if echo "$RESPONSE" | grep -q '"requestId"\|"request_id"'; then
    REQUEST_ID=$(echo "$RESPONSE" | grep -o '"requestId":"[^"]*"' | cut -d'"' -f4)
    if [ -z "$REQUEST_ID" ]; then
        REQUEST_ID=$(echo "$RESPONSE" | grep -o '"request_id":"[^"]*"' | cut -d'"' -f4)
    fi

    if [ -n "$REQUEST_ID" ]; then
        echo -e "${GREEN}✅ 视频生成任务已提交！${NC}"
        echo ""
        echo "🔖 任务 ID: ${REQUEST_ID}"
        echo ""
        echo -e "${YELLOW}⏳ 视频正在后台生成中...${NC}"
        echo ""
        echo "💡 使用以下命令查询结果:"
        echo "   bash scripts/get_video_task_outputs.sh ${REQUEST_ID}"
        exit 0
    fi
fi

# 错误处理
echo -e "${RED}❌ 任务创建失败${NC}"
echo ""
echo "API 响应: ${RESPONSE}"
echo ""
echo "💡 可能原因:"
echo "  • BIZYAIR_API_KEY 无效或已过期"
echo "  • 图片 URL 无法访问"
echo "  • 请求参数格式错误"
echo ""
echo "建议:"
echo "  1. 检查环境变量 BIZYAIR_API_KEY 是否正确设置"
echo "  2. 确认图片 URL 可访问"
echo "  3. 稍后重试"
exit 1
