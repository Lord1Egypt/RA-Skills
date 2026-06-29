#!/usr/bin/env bash
# =============================================================================
#  Douyin Short Video Script Writer — CLI Entrypoint
#  Generates a complete script + storyboard from a topic and duration.
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# ── Defaults ────────────────────────────────────────────────────────────────
TOPIC=""
DURATION=15
STYLE="快节奏诱人"
AUDIENCE="通用"
PRODUCT=""
SELLING_POINTS=""
CTA=""
OUTPUT_MODE="markdown"   # markdown | json

# ── Usage ───────────────────────────────────────────────────────────────────
usage() {
    cat << 'USAGE'
douyin-script-writer — Generate a Douyin-ready short video script.

Usage:
  douyin-script-writer --topic "..." [options]

Options:
  --topic     <str>    Video topic (required)
  --duration  <int>    Target duration: 15, 30, or 60 (default: 15)
  --style     <str>    Style: 快节奏诱人 | 干货温和 | 种草真实 | 剧情搞笑 | etc.
  --audience  <str>    Target audience (default: 通用)
  --product   <str>    Product name (for e-commerce scripts)
  --points    <str>    Selling points, comma-separated
  --cta       <str>    Call-to-action text
  --json               Output as JSON instead of markdown
  --help               Show this help

First-Success Path (30 seconds):
  douyin-script-writer --topic "上海隐藏版葱油拌面" --duration 15

Examples:
  douyin-script-writer --topic "为什么你总是存不下钱" --duration 30 --style "干货温和"
  douyin-script-writer --topic "手持挂烫机" --duration 60 --product "便携手持挂烫机" --points "3秒出蒸汽,便携,不伤衣"
USAGE
}

# ── Parse Args ──────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --topic)  TOPIC="$2";   shift 2 ;;
        --duration) DURATION="$2"; shift 2 ;;
        --style)  STYLE="$2";   shift 2 ;;
        --audience) AUDIENCE="$2"; shift 2 ;;
        --product) PRODUCT="$2"; shift 2 ;;
        --points) SELLING_POINTS="$2"; shift 2 ;;
        --cta)    CTA="$2";     shift 2 ;;
        --json)   OUTPUT_MODE="json"; shift ;;
        --help|-h) usage; exit 0 ;;
        *) echo "❌ Unknown option: $1"; usage; exit 1 ;;
    esac
done

if [[ -z "$TOPIC" ]]; then
    echo "❌ --topic is required"
    usage
    exit 1
fi

# ── Validate Duration ───────────────────────────────────────────────────────
case "$DURATION" in
    15|30|60) ;;
    *) echo "❌ Duration must be 15, 30, or 60"; exit 1 ;;
esac

# ── Build prompt context (for the AI assistant) ─────────────────────────────
BUILD_PROMPT() {
    echo "请生成一个抖音短视频脚本，主题：${TOPIC}"
    echo "时长：${DURATION}秒"
    echo "风格：${STYLE}"
    echo "目标受众：${AUDIENCE}"
    if [[ -n "$PRODUCT" ]]; then
        echo "产品：${PRODUCT}"
    fi
    if [[ -n "$SELLING_POINTS" ]]; then
        echo "卖点：${SELLING_POINTS}"
    fi
    if [[ -n "$CTA" ]]; then
        echo "行动号召（CTA）：${CTA}"
    fi
    echo ""
    echo "脚本结构要求："
    case "$DURATION" in
        15)
            echo "0-3s: 钩子 → 3-8s: 展开 → 8-12s: 高潮 → 12-15s: 结尾+行动号召"
            ;;
        30)
            echo "0-3s: 钩子 → 3-12s: 展开 → 12-22s: 高潮 → 22-30s: 结尾+行动号召"
            ;;
        60)
            echo "0-3s: 钩子 → 3-15s: 痛点/问题 → 15-35s: 解决方案/产品介绍 → 35-50s: 效果展示 → 50-60s: 结尾+促单"
            ;;
    esac
    echo ""
    echo "输出要求："
    echo "1. 分镜（每段口播对应：画面描述、景别、拍摄角度）"
    echo "2. 口播稿（逐字稿）"
    echo "3. 字幕样式建议"
    echo "4. BGM 风格和建议曲目"
    echo "5. 推荐发布时间"
    echo "6. 封面文案"
}

# ── JSON Output ─────────────────────────────────────────────────────────────
OUTPUT_JSON() {
    PROMPT_CONTENT="$(BUILD_PROMPT)"
    cat << JSONEOF
{
  "tool": "douyin-script-writer",
  "version": "1.0.0",
  "input": {
    "topic": $(printf '%s' "$TOPIC" | jq -Rs .),
    "duration": $DURATION,
    "style": $(printf '%s' "$STYLE" | jq -Rs .),
    "audience": $(printf '%s' "$AUDIENCE" | jq -Rs .),
    "product": $(printf '%s' "$PRODUCT" | jq -Rs .),
    "sellingPoints": $(printf '%s' "$SELLING_POINTS" | jq -Rs .),
    "cta": $(printf '%s' "$CTA" | jq -Rs .)
  },
  "output": {
    "prompt": $(printf '%s' "$PROMPT_CONTENT" | jq -Rs .),
    "format": "script"
  }
}
JSONEOF
}

# ── Main Output ─────────────────────────────────────────────────────────────
if [[ "$OUTPUT_MODE" == "json" ]]; then
    OUTPUT_JSON
    exit 0
else
    echo "📹  Douyin Script Writer"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Topic:    $TOPIC"
    echo "  Duration: ${DURATION}s"
    echo "  Style:    $STYLE"
    echo "  Audience: $AUDIENCE"
    [[ -n "$PRODUCT" ]] && echo "  Product:  $PRODUCT"
    [[ -n "$SELLING_POINTS" ]] && echo "  Points:   $SELLING_POINTS"
    echo ""
    echo "📋  Prompt ready for AI (below):"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━"
    BUILD_PROMPT
fi

# Also save the prompt to a file for reference
PROMPT_FILE="${SKILL_DIR}/references/last-prompt.txt"
mkdir -p "$(dirname "$PROMPT_FILE")"
BUILD_PROMPT > "$PROMPT_FILE"
echo ""
echo "📎  Prompt saved to: $PROMPT_FILE"
echo ""
echo "ℹ️   Paste the prompt above into your AI assistant to generate the full script."
echo "   Or use this skill directly — the assistant will generate the script for you."
echo ""
echo "📘  First-Success Path:"
echo "   douyin-script-writer --topic \"上海隐藏版葱油拌面\" --duration 15"
echo ""
echo "✨  Happy shooting!"
