#!/bin/bash
# 阿里云万相视频生成脚本
# Usage: wanx-video.sh "<prompt>" --out <output.mp4> [--model wan2.6-t2v] [--duration 5]

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PROMPT=""
OUTPUT=""
MODEL="wan2.1-t2v-turbo"
DURATION=5
RESOLUTION="720p"
NEGATIVE_PROMPT=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --out) OUTPUT="$2"; shift 2 ;;
        --model) MODEL="$2"; shift 2 ;;
        --duration) DURATION="$2"; shift 2 ;;
        --resolution) RESOLUTION="$2"; shift 2 ;;
        --negative-prompt) NEGATIVE_PROMPT="$2"; shift 2 ;;
        -*) echo -e "${RED}未知选项：$1${NC}"; exit 1 ;;
        *) [[ -z "$PROMPT" ]] && PROMPT="$1"; shift ;;
    esac
done

if [[ -z "$PROMPT" ]] || [[ -z "$OUTPUT" ]]; then
    echo -e "${RED}用法：$0 \"<提示词>\" --out <输出文件.mp4>${NC}"
    exit 1
fi

API_KEY="${DASHSCOPE_API_KEY:-sk-96743cd524f74354867007c0207df7b8}"

echo -e "${GREEN}🎬 开始生成视频...${NC}"
echo -e "  提示词：$PROMPT"
echo -e "  模型：$MODEL"
echo -e "  时长：${DURATION}s"
echo -e "  输出：$OUTPUT"

mkdir -p "$(dirname "$OUTPUT")"

ENDPOINT="https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-generation"

if [[ -n "$NEGATIVE_PROMPT" ]]; then
    REQUEST_DATA="{\"model\":\"$MODEL\",\"input\":{\"prompt\":\"$PROMPT\",\"negative_prompt\":\"$NEGATIVE_PROMPT\"},\"parameters\":{\"duration\":$DURATION}}"
else
    REQUEST_DATA="{\"model\":\"$MODEL\",\"input\":{\"prompt\":\"$PROMPT\"},\"parameters\":{\"duration\":$DURATION}}"
fi

echo -e "${YELLOW}📤 提交任务...${NC}"

RESPONSE=$(curl -s -X POST "$ENDPOINT" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -H "X-DashScope-Async: enable" \
    -d "$REQUEST_DATA")

echo "API 响应：$RESPONSE"

JOB_ID=$(echo "$RESPONSE" | grep -o '"task_id"[^,]*' | head -1 | sed 's/.*"\([^"]*\)"$/\1/')

if [[ -z "$JOB_ID" ]]; then
    echo -e "${RED}❌ 任务提交失败${NC}"
    echo "请检查："
    echo "  1. API Key 是否正确"
    echo "  2. 是否开通了视频生成服务：https://bailian.console.aliyun.com/"
    echo "  3. 模型名称是否正确"
    echo "响应：$RESPONSE"
    exit 1
fi

echo -e "${GREEN}✅ 任务 ID: $JOB_ID${NC}"
echo -e "${YELLOW}⏳ 等待生成 (约 1-5 分钟)...${NC}"

TASK_ENDPOINT="https://dashscope.aliyuncs.com/api/v1/tasks/$JOB_ID"
MAX_ATTEMPTS=60
ATTEMPT=0

while [[ $ATTEMPT -lt $MAX_ATTEMPTS ]]; do
    sleep 5
    ATTEMPT=$((ATTEMPT + 1))
    
    TASK_RESPONSE=$(curl -s -X GET "$TASK_ENDPOINT" -H "Authorization: Bearer $API_KEY")
    STATUS=$(echo "$TASK_RESPONSE" | grep -o '"status"[^,]*' | head -1 | sed 's/.*"\([^"]*\)"$/\1/')
    
    if [[ "$STATUS" == "SUCCEEDED" ]]; then
        echo -e "${GREEN}✅ 生成完成!${NC}"
        VIDEO_URL=$(echo "$TASK_RESPONSE" | grep -o '"video_url"[^,]*' | head -1 | sed 's/.*"\([^"]*\)"$/\1/')
        
        if [[ -n "$VIDEO_URL" ]]; then
            echo -e "${YELLOW}📥 下载视频...${NC}"
            curl -s -o "$OUTPUT" "$VIDEO_URL"
            echo -e "${GREEN}✅ 视频已保存：$OUTPUT${NC}"
            ls -lh "$OUTPUT"
        fi
        break
    elif [[ "$STATUS" == "FAILED" ]]; then
        echo -e "${RED}❌ 生成失败${NC}"
        echo "$TASK_RESPONSE"
        exit 1
    else
        echo -ne "  进度：${ATTEMPT}s (状态：$STATUS)...\r"
    fi
done

[[ $ATTEMPT -ge $MAX_ATTEMPTS ]] && echo -e "${RED}⏰ 超时${NC}" && exit 1
echo -e "${GREEN}🎉 完成!${NC}"
