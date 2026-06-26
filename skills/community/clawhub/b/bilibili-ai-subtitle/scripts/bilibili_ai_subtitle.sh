#!/bin/bash
# Bilibili AI字幕下载脚本 v2.0
# 专门下载B站AI自动生成字幕 - 优化版

# 显示帮助
show_help() {
    echo "Bilibili AI字幕下载器 v2.0"
    echo ""
    echo "用法: $0 [选项] <B站视频链接> [输出目录]"
    echo ""
    echo "选项:"
    echo "  -l, --lang LANG_LIST    指定AI字幕语言优先级"
    echo "                          默认: zh,en,ja,es,ar,pt,ko,de,fr"
    echo "  -h, --help              显示此帮助"
    echo ""
    echo "示例:"
    echo "  $0 \"https://www.bilibili.com/video/BVxxxxx/\""
    echo "  $0 -l en,zh \"BVxxxxx\""
    echo ""
    echo "支持的语言: zh(中文), en(英文), ja(日文), es(西班牙文),"
    echo "           ar(阿拉伯文), pt(葡萄牙文), ko(韩文), de(德文), fr(法文)"
}

# 解析参数
VIDEO_URL=""
OUTPUT_DIR=""
LANG_PRIORITY="zh,en,ja,es,ar,pt,ko,de,fr"

while [[ $# -gt 0 ]]; do
    case $1 in
        -l|--lang)
            LANG_PRIORITY="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*)
            echo "❌ 未知选项: $1"
            exit 1
            ;;
        *)
            if [ -z "$VIDEO_URL" ]; then
                VIDEO_URL="$1"
            elif [ -z "$OUTPUT_DIR" ]; then
                OUTPUT_DIR="$1"
            fi
            shift
            ;;
    esac
done

if [ -z "$VIDEO_URL" ]; then
    echo "❌ 请提供B站视频链接"
    show_help
    exit 1
fi

OUTPUT_DIR="${OUTPUT_DIR:-/home/administrator/.openclaw/workspace/Bilibili transcript}"

# 构建AI语言列表
IFS=',' read -ra LANG_ARRAY <<< "$LANG_PRIORITY"
AI_LANGS=""
for lang in "${LANG_ARRAY[@]}"; do
    AI_LANGS="$AI_LANGS ai-${lang}"
done

echo "=========================================="
echo "🎬 Bilibili AI字幕下载器 v2.0"
echo "=========================================="
echo "🌐 语言优先级: $LANG_PRIORITY"
echo ""

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# ===== 获取视频信息 =====
echo "📋 获取视频信息..."
VIDEO_INFO=$(yt-dlp --dump-json "$VIDEO_URL" 2>/dev/null)

if [ -z "$VIDEO_INFO" ]; then
    echo "❌ 无法获取视频信息"
    exit 1
fi

VIDEO_TITLE=$(echo "$VIDEO_INFO" | python3 -c "import sys, json; print(json.load(sys.stdin).get('title', '未知标题'))")
VIDEO_AUTHOR=$(echo "$VIDEO_INFO" | python3 -c "import sys, json; print(json.load(sys.stdin).get('uploader', '未知作者'))")
VIDEO_DATE=$(echo "$VIDEO_INFO" | python3 -c "import sys, json; d=json.load(sys.stdin).get('upload_date', ''); print(f'{d[:4]}-{d[4:6]}-{d[6:8]}' if len(d)==8 else d)")
VIDEO_DURATION=$(echo "$VIDEO_INFO" | python3 -c "import sys, json; dur=json.load(sys.stdin).get('duration', 0); print(f'{dur//60}分{dur%60}秒' if dur else '未知')")
VIDEO_DURATION_SEC=$(echo "$VIDEO_INFO" | python3 -c "import sys, json; print(json.load(sys.stdin).get('duration', 0))")
BVID=$(echo "$VIDEO_INFO" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")

echo "   📹 标题: $VIDEO_TITLE"
echo "   👤 作者: $VIDEO_AUTHOR"
echo "   📅 时间: $VIDEO_DATE"
echo "   ⏱️ 时长: $VIDEO_DURATION"
echo ""

# 清理文件名（使用Python避免UTF-8问题）
python3 -c "
import sys
title = sys.argv[1].replace('/', '_').replace('\\\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('\"', '_').replace('<', '_').replace('>', '_').replace('|', '_')[:35]
author = sys.argv[2].replace('/', '_').replace('\\\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('\"', '_').replace('<', '_').replace('>', '_').replace('|', '_')[:15]
for char in '。？！，、；：""''（）【】《》':
    title = title.replace(char, '_')
    author = author.replace(char, '_')
print(f'{title}_{author}')
" "$VIDEO_TITLE" "$VIDEO_AUTHOR" > /tmp/safe_name_$$

SAFE_NAME=$(cat /tmp/safe_name_$$)
DATE_SHORT=$(echo "$VIDEO_DATE" | sed 's/-//g')

# 简化时长
DURATION_SIMPLE=$(echo "$VIDEO_DURATION" | sed 's/分/./g; s/秒//g')

[ -z "$SAFE_NAME" ] && SAFE_NAME="video_unknown"

# 文件名：视频标题_UP主_日期_时长_BVid.txt
FILENAME="${SAFE_NAME}_${DATE_SHORT}_${DURATION_SIMPLE}_${BVID}.txt"
OUTPUT_FILE="${OUTPUT_DIR}/${FILENAME}"

rm -f /tmp/safe_name_$$

# ===== 检测浏览器Cookie =====
echo "🔍 检测浏览器Cookie..."

COOKIE_PARAM=""
FOUND_COOKIE=false

# 1. 尝试 WSL Chromium
CHROMIUM_PATH="$HOME/snap/chromium/common/chromium"
if [ -d "$CHROMIUM_PATH" ]; then
    TEST=$(yt-dlp --list-subs --cookies-from-browser "chromium:$CHROMIUM_PATH" "$VIDEO_URL" 2>&1 | head -1)
    if echo "$TEST" | grep -q "Extracting"; then
        echo "   ✅ 使用 WSL Chromium Cookie"
        COOKIE_PARAM="--cookies-from-browser chromium:$CHROMIUM_PATH"
        FOUND_COOKIE=true
    fi
fi

# 2. 尝试 Windows Edge
if [ "$FOUND_COOKIE" = false ]; then
    WIN_USER=$(ls /mnt/c/Users/ 2>/dev/null | grep -v "Public\|Default\|All Users" | head -1)
    if [ -n "$WIN_USER" ]; then
        EDGE_PATH="/mnt/c/Users/$WIN_USER/AppData/Local/Microsoft/Edge/User Data"
        if [ -d "$EDGE_PATH" ]; then
            echo "   🔑 使用 Windows Edge Cookie"
            COOKIE_PARAM="--cookies-from-browser edge:C:/Users/$WIN_USER/AppData/Local/Microsoft/Edge/User Data"
            FOUND_COOKIE=true
        fi
    fi
fi

[ "$FOUND_COOKIE" = false ] && echo "   ℹ️ 无可用Cookie，尝试无Cookie模式"
echo ""

# ===== 检测AI字幕 =====
echo "🔍 检测AI字幕..."
echo "   🌐 语言优先级: $LANG_PRIORITY"

if [ "$FOUND_COOKIE" = true ]; then
    SUB_LIST=$(yt-dlp --list-subs --write-auto-subs $COOKIE_PARAM "$VIDEO_URL" 2>&1)
else
    SUB_LIST=$(yt-dlp --list-subs --write-auto-subs "$VIDEO_URL" 2>&1)
fi

echo "$SUB_LIST" | grep -E "(subtitle|Available|ai-)" | head -10

# 按用户指定的优先级检测AI语言
AI_LANG_FOUND=""
for lang_code in $AI_LANGS; do
    if echo "$SUB_LIST" | grep -q "$lang_code"; then
        AI_LANG_FOUND="$lang_code"
        LANG_SHORT=$(echo "$lang_code" | sed 's/ai-//')
        case "$LANG_SHORT" in
            zh) LANG_NAME="中文" ;;
            en) LANG_NAME="英文" ;;
            ja) LANG_NAME="日文" ;;
            es) LANG_NAME="西班牙文" ;;
            ar) LANG_NAME="阿拉伯文" ;;
            pt) LANG_NAME="葡萄牙文" ;;
            ko) LANG_NAME="韩文" ;;
            de) LANG_NAME="德文" ;;
            fr) LANG_NAME="法文" ;;
            *) LANG_NAME="$LANG_SHORT" ;;
        esac
        echo "   ✅ 发现AI字幕: $lang_code ($LANG_NAME)"
        break
    fi
done

if [ -z "$AI_LANG_FOUND" ]; then
    echo ""
    echo "❌ 该视频没有AI字幕（指定语言: $LANG_PRIORITY）"
    echo "💡 提示：只有部分视频有B站AI自动字幕"
    exit 1
fi

# ===== 下载AI字幕 =====
echo ""
echo "⬇️  下载AI字幕 ($AI_LANG_FOUND)..."

TEMP_FILE="${OUTPUT_DIR}/temp_ai_sub_$$"

if [ "$FOUND_COOKIE" = true ]; then
    yt-dlp --skip-download --write-subs --write-auto-subs $COOKIE_PARAM \
        --sub-langs "$AI_LANG_FOUND" --convert-subs srt \
        -o "${TEMP_FILE}.%(ext)s" "$VIDEO_URL" 2>&1 | tail -5
else
    yt-dlp --skip-download --write-subs --write-auto-srt \
        --sub-langs "$AI_LANG_FOUND" --convert-subs srt \
        -o "${TEMP_FILE}.%(ext)s" "$VIDEO_URL" 2>&1 | tail -5
fi

# 查找下载的字幕文件
SUB_FILE=$(find "$OUTPUT_DIR" -name "temp_ai_sub_$$*.srt" -type f 2>/dev/null | head -1)

if [ -z "$SUB_FILE" ] || [ ! -s "$SUB_FILE" ]; then
    echo ""
    echo "❌ AI字幕下载失败"
    echo "💡 可能原因：Cookie已过期或网络问题"
    exit 1
fi

echo "   ✅ AI字幕下载成功！"

# ===== 生成文档 =====
echo ""
echo "📝 生成文档..."

CURRENT_TIME=$(date "+%Y-%m-%d %H:%M")

# 提取纯文本
TRANSCRIPT_TEXT=$(sed '/^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]/d' "$SUB_FILE" | sed '/^[0-9]*$/d' | sed '/^$/d')

# 生成简短摘要（前10行）
SUMMARY_LINES=$(echo "$TRANSCRIPT_TEXT" | head -10 | tr '\\n' ' ')

cat > "$OUTPUT_FILE" << EOF
================================================================================
第一部分：视频信息
================================================================================

视频标题：${VIDEO_TITLE}
B站链接：${VIDEO_URL}
作者：${VIDEO_AUTHOR}
发布时间：${VIDEO_DATE}
视频时长：${VIDEO_DURATION}
原视频语言：${LANG_NAME}
转录来源：B站AI字幕 (${LANG_NAME})
转录时间：${CURRENT_TIME}

================================================================================
第二部分：视频摘要
================================================================================

本视频由UP主${VIDEO_AUTHOR}发布。视频主要内容包括：${SUMMARY_LINES}...
（以上为视频开头部分内容预览，完整内容请查看第三部分）

================================================================================
第三部分：完整原文
================================================================================

${TRANSCRIPT_TEXT}

================================================================================
文件结束
================================================================================
EOF

# 清理临时文件
rm -f "$SUB_FILE"

# 统计字数
WORD_COUNT=$(wc -m < "$OUTPUT_FILE")

# 生成Discord预览摘要
DISCORD_PREVIEW=$(echo "$TRANSCRIPT_TEXT" | head -5 | tr '\\n' ' ' | cut -c1-200)

echo ""
echo "=========================================="
echo "✅ AI字幕下载成功！"
echo "=========================================="
echo ""
echo "📄 文件：$FILENAME"
echo "📍 位置：$OUTPUT_FILE"
echo "📝 字数：约$WORD_COUNT字"
echo "🌐 语言：$LANG_NAME"
echo ""
echo "📋 视频摘要："
echo "📹 $VIDEO_TITLE"
echo "👤 $VIDEO_AUTHOR | 📅 $VIDEO_DATE"
echo ""
echo "💡 内容预览："
echo "$DISCORD_PREVIEW..."
echo ""
echo "📎 完整内容请查看附件TXT文件"
