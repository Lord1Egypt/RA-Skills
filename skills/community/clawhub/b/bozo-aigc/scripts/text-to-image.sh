#!/bin/bash

# ========================================
# BOZO AIGC - 文生图工具 (Text-to-Image)
# ========================================
# 使用 BizyAir GPT_IMAGE_2 T2I API 将文本描述转换为图片
# 用法: ./text-to-image.sh "提示词" [比例]
# 比例选项: 1:1 2:3 3:2 4:5 5:4 3:4 4:3 9:16 16:9 21:9
# ========================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印带颜色的消息
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

# 检查API密钥是否设置
if [ -z "$API_KEY" ]; then
    print_error "环境变量 BIZYAIR_API_KEY 未设置或为空"
    echo ""
    echo "请按以下方式设置环境变量："
    echo ""
    echo "【Git Bash / WSL】"
    echo "  export BIZYAIR_API_KEY='你的API密钥'"
    echo ""
    echo "【macOS / Linux】"
    echo "  export BIZYAIR_API_KEY='你的API密钥'"
    echo "  # 永久设置：添加到 ~/.bashrc 或 ~/.zshrc"
    echo ""
    echo "【Windows 系统环境变量】（需重启终端生效）"
    echo "  setx BIZYAIR_API_KEY \"你的API密钥\""
    exit 1
fi

# 获取提示词参数
PROMPT="$1"

# 如果没有传入参数，使用默认提示词
if [ -z "$PROMPT" ]; then
    print_warning "未提供提示词，使用默认示例"
    PROMPT="一张美丽的风景画，蓝天白云，青山绿水"
fi

print_info "API密钥已读取: ${API_KEY:0:8}..."
print_info "提示词: $PROMPT"

# ========================================
# 获取当前日期作为文件名
# ========================================
DATE=$(date +%Y%m%d_%H%M%S)
print_info "当前时间: $DATE"

# ========================================
# 第一步：创建任务
# ========================================
echo ""
print_info "正在创建生成任务..."
echo "========================================"

# 解析比例参数（第二个参数），默认 9:16
ASPECT_RATIO="${2:-9:16}"

# 验证比例是否合法
VALID_RATIOS="1:1 2:3 3:2 4:5 5:4 3:4 4:3 9:16 16:9 21:9"
if ! echo "$VALID_RATIOS" | grep -qw "$ASPECT_RATIO"; then
    print_warning "不支持的图片比例: $ASPECT_RATIO，使用默认 9:16"
    ASPECT_RATIO="9:16"
fi

print_info "图片比例: $ASPECT_RATIO"

# 构建JSON请求体 - 使用 BizyAir GPT_IMAGE_2 T2I API (web_app_id: 52416)
JSON_PAYLOAD=$(cat <<EOF
{
  "web_app_id": 52416,
  "suppress_preview_output": false,
  "input_values": {
    "4:BizyAir_GPT_IMAGE_2_T2I_API.prompt": "$PROMPT",
    "4:BizyAir_GPT_IMAGE_2_T2I_API.aspect_ratio": "$ASPECT_RATIO"
  }
}
EOF
)

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
    echo ""
    print_warning "请检查API密钥是否有效"
    exit 1
fi

print_info "API调用成功!"

# 从outputs数组提取图片URL和文件扩展名
IMAGE_URL=$(echo "$RESPONSE" | grep -o '"object_url":"[^"]*"' | head -1 | cut -d'"' -f4)
OUTPUT_EXT=$(echo "$RESPONSE" | grep -o '"output_ext":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$IMAGE_URL" ]; then
    print_error "无法从outputs数组提取URL"
    exit 1
fi

print_info "获取到URL: $IMAGE_URL"

# ========================================
# 第二步：下载图片并保存到pic文件夹
# ========================================
echo ""
print_info "正在下载..."
echo "========================================"

# 确定文件扩展名，默认为.jpg
if [ -z "$OUTPUT_EXT" ]; then
    OUTPUT_EXT="jpg"
fi

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
    # 尝试在macOS上预览图片
    if [[ "$OSTYPE" == "darwin"* ]]; then
        print_info "正在打开图片预览..."
        open "$OUTPUT_FILE" 2>/dev/null &
    fi
else
    print_error "图片下载失败"
    exit 1
fi
