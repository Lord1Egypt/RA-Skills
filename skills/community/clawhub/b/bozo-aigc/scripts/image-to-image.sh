#!/bin/bash

# ========================================
# BOZO AIGC - 图生图工具 (Image-to-Image)
# ========================================
# 使用 BizyAir GPT_IMAGE_2 I2I API 根据参考图片生成新图片
# 支持 1-8 张参考图片输入
# 用法: ./image-to-image.sh "提示词" "图片URL1" ["图片URL2" ...] [比例]
# ========================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# ========================================
# 创建pic文件夹（如果不存在）
# ========================================
mkdir -p pic

# ========================================
# 从环境变量获取API密钥
# ========================================
API_KEY="${BIZYAIR_API_KEY}"

if [ -z "$API_KEY" ]; then
    print_error "环境变量 BIZYAIR_API_KEY 未设置或为空"
    echo ""
    echo "请按以下方式设置环境变量："
    echo ""
    echo "  export BIZYAIR_API_KEY='你的API密钥'"
    echo "  # 永久设置：添加到 ~/.bashrc 或 ~/.zshrc"
    exit 1
fi

# ========================================
# 解析参数
# ========================================
# 参数格式: 提示词 图片URL1 [图片URL2...图片URL8] [比例]
# 最后一个参数如果匹配比例格式（如 16:9），则识别为比例

PROMPT="$1"
if [ -z "$PROMPT" ]; then
    print_error "缺少提示词参数"
    echo "用法: $0 \"提示词\" \"图片URL1\" [\"图片URL2\"...] [比例]"
    exit 1
fi

shift  # 移除提示词参数，剩余参数为图片URL和可能的比率

# 收集图片URL和比例
IMAGE_URLS=()
ASPECT_RATIO="9:16"  # 默认比例
VALID_RATIOS="1:1 2:3 3:2 4:5 5:4 3:4 4:3 9:16 16:9 21:9"

for arg in "$@"; do
    # 检查是否为比例参数
    if echo "$VALID_RATIOS" | grep -qw "$arg"; then
        ASPECT_RATIO="$arg"
    else
        IMAGE_URLS+=("$arg")
    fi
done

IMAGE_COUNT=${#IMAGE_URLS[@]}

if [ "$IMAGE_COUNT" -eq 0 ]; then
    print_error "缺少参考图片URL"
    echo "图生图需要至少提供 1 张参考图片 URL"
    echo "用法: $0 \"提示词\" \"图片URL1\" [\"图片URL2\"...] [比例]"
    exit 1
fi

if [ "$IMAGE_COUNT" -gt 8 ]; then
    print_error "最多支持 8 张参考图片，当前提供了 $IMAGE_COUNT 张"
    exit 1
fi

print_info "API密钥已读取: ${API_KEY:0:8}..."
print_info "提示词: $PROMPT"
print_info "参考图片数量: $IMAGE_COUNT 张"
print_info "图片比例: $ASPECT_RATIO"

for i in "${!IMAGE_URLS[@]}"; do
    print_info "图片 $((i+1)): ${IMAGE_URLS[$i]:0:60}..."
done

# ========================================
# 根据图片数量确定 web_app_id 和图片节点 ID 映射
# ========================================
# 每个图片数量对应的 web_app_id 和 LoadImage 节点 ID 列表
# 节点ID顺序来源于 BizyAir API 文档
declare -A APP_IDS
APP_IDS=(
    [1]=52418
    [2]=52420
    [3]=52423
    [4]=52343
    [5]=52431
    [6]=52435
    [7]=52437
    [8]=52442
)

declare -A NODE_IDS_STR
NODE_IDS_STR=(
    [1]="7"
    [2]="7 8"
    [3]="7 8 9"
    [4]="7 8 9 10"
    [5]="7 8 9 10 11"
    [6]="7 8 9 10 11 12"
    [7]="7 8 9 10 11 12 18"
    [8]="7 8 9 10 11 12 18 20"
)

WEB_APP_ID="${APP_IDS[$IMAGE_COUNT]}"
NODE_IDS=(${NODE_IDS_STR[$IMAGE_COUNT]})

print_info "使用 web_app_id: $WEB_APP_ID (支持 ${IMAGE_COUNT} 张参考图)"

# ========================================
# 构建请求
# ========================================
DATE=$(date +%Y%m%d_%H%M%S)

echo ""
print_info "正在创建图生图任务..."
echo "========================================"

# 构建 input_values 的 JSON
# 先构建图片输入部分
INPUT_PARTS="\"6:BizyAir_GPT_IMAGE_2_I2I_API.prompt\": \"$PROMPT\",\n    \"6:BizyAir_GPT_IMAGE_2_I2I_API.aspect_ratio\": \"$ASPECT_RATIO\""

for i in "${!IMAGE_URLS[@]}"; do
    NODE_ID="${NODE_IDS[$i]}"
    URL="${IMAGE_URLS[$i]}"
    INPUT_PARTS="$INPUT_PARTS,\n    \"${NODE_ID}:LoadImage.image\": \"$URL\""
done

# 组装完整 JSON
JSON_PAYLOAD=$(printf "{
  \"web_app_id\": $WEB_APP_ID,
  \"suppress_preview_output\": false,
  \"input_values\": {
    %s
  }
}" "$INPUT_PARTS")

# 发送API请求
# BizyAir GPT_IMAGE_2 为远程推理，生图耗时 90秒 ~ 10分钟不等
# --connect-timeout: 连接超时 30 秒
# --max-time: 总请求超时 600 秒（10 分钟），覆盖最慢情况
print_info "正在等待 API 响应（预计 90秒 ~ 10分钟）..."
RESPONSE=$(curl -s --connect-timeout 30 --max-time 600 -X POST "https://api.bizyair.cn/w/v1/webapp/task/openapi/create" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "$JSON_PAYLOAD")

echo "API响应:"
echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
echo ""

# 检查API状态
API_STATUS=$(echo "$RESPONSE" | grep -o '"status":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ "$API_STATUS" != "Success" ]; then
    print_error "API调用失败，状态: $API_STATUS"
    ERROR_MSG=$(echo "$RESPONSE" | grep -o '"message":"[^"]*"' | head -1 | cut -d'"' -f4)
    if [ -n "$ERROR_MSG" ]; then
        print_error "错误信息: $ERROR_MSG"
    fi
    exit 1
fi

print_info "API调用成功!"

# ========================================
# 下载图片
# ========================================
IMAGE_URL=$(echo "$RESPONSE" | grep -o '"object_url":"[^"]*"' | head -1 | cut -d'"' -f4)
OUTPUT_EXT=$(echo "$RESPONSE" | grep -o '"output_ext":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$IMAGE_URL" ]; then
    print_error "无法从响应中提取图片URL"
    exit 1
fi

print_info "获取到URL: $IMAGE_URL"

echo ""
print_info "正在下载..."
echo "========================================"

if [ -z "$OUTPUT_EXT" ]; then
    OUTPUT_EXT="png"
fi

# 移除可能的点号前缀
OUTPUT_EXT="${OUTPUT_EXT#.}"

OUTPUT_FILE="pic/${DATE}.${OUTPUT_EXT}"
# 图片下载超时：连接 30 秒，下载 120 秒
curl -s --connect-timeout 30 --max-time 120 -o "$OUTPUT_FILE" "$IMAGE_URL"

if [ -f "$OUTPUT_FILE" ]; then
    FILE_SIZE=$(stat -c%s "$OUTPUT_FILE" 2>/dev/null || stat -f%z "$OUTPUT_FILE" 2>/dev/null || wc -c < "$OUTPUT_FILE")
    echo ""
    echo "========================================"
    print_info "保存成功!"
    echo "========================================"
    echo "文件路径: $OUTPUT_FILE"
    echo "文件大小: $FILE_SIZE 字节"
    echo "完成时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    # macOS 自动预览
    if [[ "$OSTYPE" == "darwin"* ]]; then
        print_info "正在打开图片预览..."
        open "$OUTPUT_FILE" 2>/dev/null &
    fi
else
    print_error "图片下载失败"
    exit 1
fi
