#!/bin/bash
# AI Script Generator - 根据主题自动生成视频文案
# 调用通义千问 API 生成真实文案
set -e

# 默认参数
TOPIC=""
STYLE="vlog"
DURATION=60
OUTPUT=""
PLATFORM="general"
KEYWORDS=false

# API 配置 - 使用百炼 API
API_BASE="${DASHSCOPE_API_BASE:-https://dashscope.aliyuncs.com/compatible-mode/v1}"
API_KEY="${DASHSCOPE_API_KEY:-}"
MODEL="${DASHSCOPE_MODEL:-qwen-plus}"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }

show_help() {
    cat << EOF
📝 AI 文案自动生成器

用法:
  bash $0 --topic "主题" [选项]

选项:
  --topic <文本>      视频主题（必需）
  --style <风格>      vlog/科普/教程/带货/故事 (默认: vlog)
  --duration <秒>     目标时长 (默认: 60)
  --platform <平台>   general/tiktok/youtube/bilibili (默认: general)
  --output <文件>     输出文件路径
  --keywords          同时输出素材搜索关键词
  --help              显示帮助

EOF
    exit 0
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --topic) TOPIC="$2"; shift 2 ;;
        --style) STYLE="$2"; shift 2 ;;
        --duration) DURATION="$2"; shift 2 ;;
        --platform) PLATFORM="$2"; shift 2 ;;
        --output) OUTPUT="$2"; shift 2 ;;
        --keywords) KEYWORDS=true; shift ;;
        --help) show_help ;;
        *) print_error "未知参数：$1"; show_help ;;
    esac
done

if [[ -z "$TOPIC" ]]; then
    print_error "缺少必需参数：--topic"
    show_help
fi

if [[ -z "$API_KEY" ]]; then
    print_error "未设置 DASHSCOPE_API_KEY 环境变量"
    exit 1
fi

# 设置默认输出路径
if [[ -z "$OUTPUT" ]]; then
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    OUTPUT="$HOME/Desktop/脚本_${TIMESTAMP}.txt"
fi
mkdir -p "$(dirname "$OUTPUT")"

# 计算字数
case $PLATFORM in
    tiktok)   PLATFORM_HINT="短视频平台，节奏快，前3秒必须有钩子，竖屏"; WORD_COUNT=$((DURATION * 3)) ;;
    youtube)  PLATFORM_HINT="长视频平台，内容有深度，横屏"; WORD_COUNT=$((DURATION * 5 / 2)) ;;
    bilibili) PLATFORM_HINT="B站，喜欢干货和梗，节奏中等"; WORD_COUNT=$((DURATION * 14 / 5)) ;;
    *)        PLATFORM_HINT="通用格式，适合多平台"; WORD_COUNT=$((DURATION * 5 / 2)) ;;
esac

case $STYLE in
    vlog)   STYLE_HINT="轻松自然的Vlog风格，第一人称，像和朋友聊天" ;;
    科普)   STYLE_HINT="科普讲解风格，逻辑清晰，简单语言解释复杂概念" ;;
    教程)   STYLE_HINT="教程风格，步骤明确，每步有详细说明" ;;
    带货)   STYLE_HINT="带货风格，突出卖点，有号召力" ;;
    故事)   STYLE_HINT="故事叙述风格，有起承转合，情感丰富" ;;
    *)      STYLE_HINT="通用风格" ;;
esac

print_info "正在生成文案..."
print_info "主题：$TOPIC"
print_info "风格：$STYLE"
print_info "时长：${DURATION}秒"

# 构建 AI 提示词
KEYWORDS_INSTRUCTION=""
if [[ "$KEYWORDS" == true ]]; then
    KEYWORDS_INSTRUCTION="

最后，请输出 5-10 个适合在 Pexels/Pixabay 搜索视频素材的英文关键词，每行一个，用 KEYWORDS: 标记开头。例如：
KEYWORDS: coffee
KEYWORDS: brewing
KEYWORDS: morning"
fi

AI_PROMPT="你是一个专业的视频文案撰写者。请为以下视频生成完整的配音文案。

主题：$TOPIC
风格：$STYLE_HINT
平台：$PLATFORM_HINT
目标时长：${DURATION}秒（约 ${WORD_COUNT} 字）

要求：
1. 直接输出可用于 TTS 配音的纯文本
2. 按段落分隔（每段对应一个视频片段）
3. **每段最多 1-2 句话，不超过 40 个字**（这非常重要！）
4. 生成 8-15 个短段落
5. 开场要有吸引力
6. 语言口语化，适合朗读
7. 结尾有总结
8. 不要输出任何标记、编号、时间码、画面描述，只要纯文案文本
9. 段落之间用一个空行分隔
${KEYWORDS_INSTRUCTION}

请直接开始输出文案："

# 调用通义千问 API
RESPONSE=$(curl -s --max-time 60 "${API_BASE}/chat/completions" \
    -H "Authorization: Bearer ${API_KEY}" \
    -H "Content-Type: application/json" \
    -d "$(jq -n \
        --arg model "$MODEL" \
        --arg prompt "$AI_PROMPT" \
        '{
            model: $model,
            messages: [
                {role: "system", content: "你是一个专业的视频文案撰写者，只输出纯文案文本，不要任何标记或格式。"},
                {role: "user", content: $prompt}
            ],
            temperature: 0.8,
            max_tokens: 2000
        }'
    )")

# 检查 API 返回
if [[ -z "$RESPONSE" ]]; then
    print_error "API 调用失败：无响应"
    exit 1
fi

# 提取文案内容
SCRIPT_CONTENT=$(echo "$RESPONSE" | jq -r '.choices[0].message.content // empty' 2>/dev/null)

if [[ -z "$SCRIPT_CONTENT" ]]; then
    ERROR_MSG=$(echo "$RESPONSE" | jq -r '.error.message // .message // "未知错误"' 2>/dev/null)
    print_error "AI 生成失败：$ERROR_MSG"
    echo "API 返回：$RESPONSE" >&2
    exit 1
fi

# 提取关键词（如果有）
KEYWORDS_LIST=""
if [[ "$KEYWORDS" == true ]]; then
    KEYWORDS_LIST=$(echo "$SCRIPT_CONTENT" | grep "^KEYWORDS:" | sed 's/^KEYWORDS: *//')
    # 从文案中移除关键词行
    SCRIPT_CONTENT=$(echo "$SCRIPT_CONTENT" | grep -v "^KEYWORDS:")
fi

# 清理文案：去除可能的 markdown 标记
SCRIPT_CONTENT=$(echo "$SCRIPT_CONTENT" | sed 's/^##* *//g' | sed 's/^\*\*.*\*\*$//g' | sed '/^---$/d' | sed '/^```/d')
# 去除开头和结尾的空行 (macOS 兼容)
SCRIPT_CONTENT=$(echo "$SCRIPT_CONTENT" | awk 'NF{p=1} p' | awk '{lines[NR]=$0} END{for(i=NR;i>=1;i--){if(lines[i]!=""){last=i;break}} for(i=1;i<=last;i++) print lines[i]}')

# 写入输出文件
echo "$SCRIPT_CONTENT" > "$OUTPUT"

# 统计段落数
PARAGRAPH_COUNT=$(echo "$SCRIPT_CONTENT" | awk 'BEGIN{n=0} /^$/{if(p)n++; p=0; next} {p=1} END{if(p)n++; print n}')
CHAR_COUNT=$(echo "$SCRIPT_CONTENT" | wc -c | tr -d ' ')

print_success "文案已生成：$OUTPUT"
print_info "段落数：$PARAGRAPH_COUNT"
print_info "字数：~$CHAR_COUNT"

# 输出关键词
if [[ -n "$KEYWORDS_LIST" ]]; then
    KEYWORDS_FILE="${OUTPUT%.txt}_keywords.txt"
    echo "$KEYWORDS_LIST" > "$KEYWORDS_FILE"
    print_info "素材关键词：$KEYWORDS_FILE"
    echo ""
    echo "推荐素材关键词："
    echo "$KEYWORDS_LIST"
fi

# 显示文案预览
echo ""
echo "━━━ 文案预览 ━━━"
echo "$SCRIPT_CONTENT" | head -20
if [[ $(echo "$SCRIPT_CONTENT" | wc -l) -gt 20 ]]; then
    echo "... (更多内容见输出文件)"
fi
echo "━━━━━━━━━━━━━━━"

echo ""
echo "$OUTPUT"
