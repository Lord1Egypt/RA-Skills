#!/bin/bash
# 阿里云百炼视频生成 - 使用 OpenAI 兼容接口
# Usage: generate-video.sh "<prompt>" --out <output.mp4>

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PROMPT=""
OUTPUT=""
MODEL="wan2.1-t2v-turbo"
DURATION=5

while [[ $# -gt 0 ]]; do
    case $1 in
        --out) OUTPUT="$2"; shift 2 ;;
        --model) MODEL="$2"; shift 2 ;;
        --duration) DURATION="$2"; shift 2 ;;
        -*) echo -e "${RED}未知选项：$1${NC}"; exit 1 ;;
        *) [[ -z "$PROMPT" ]] && PROMPT="$1"; shift ;;
    esac
done

if [[ -z "$PROMPT" ]] || [[ -z "$OUTPUT" ]]; then
    echo -e "${RED}用法：$0 \"<提示词>\" --out <输出文件.mp4>${NC}"
    exit 1
fi

API_KEY="sk-96743cd524f74354867007c0207df7b8"

echo -e "${GREEN}🎬 开始生成视频...${NC}"
echo -e "  提示词：$PROMPT"
echo -e "  模型：$MODEL"
echo -e "  时长：${DURATION}s"
echo -e "  输出：$OUTPUT"

mkdir -p "$(dirname "$OUTPUT")"

# 使用 OpenAI 兼容接口
ENDPOINT="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

echo -e "${YELLOW}📤 提交任务...${NC}"

# 先测试 API 连接
TEST_RESPONSE=$(curl -s -X POST "$ENDPOINT" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"qwen-plus","messages":[{"role":"user","content":"hi"}]}')

if echo "$TEST_RESPONSE" | grep -q "qwen-plus"; then
    echo -e "${GREEN}✅ API Key 有效${NC}"
else
    echo -e "${RED}❌ API Key 无效${NC}"
    echo "响应：$TEST_RESPONSE"
    exit 1
fi

# 视频生成需要使用异步任务 API
VIDEO_ENDPOINT="https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis"

REQUEST_DATA="{\"model\":\"$MODEL\",\"input\":{\"prompt\":\"$PROMPT\"},\"parameters\":{\"duration\":$DURATION}}"

RESPONSE=$(curl -s -X POST "$VIDEO_ENDPOINT" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -H "X-DashScope-Async: enable" \
    -d "$REQUEST_DATA")

echo "API 响应：$RESPONSE"

# 检查是否成功
if echo "$RESPONSE" | grep -q "task_id"; then
    JOB_ID=$(echo "$RESPONSE" | grep -o '"task_id"[^,]*' | head -1 | sed 's/.*"\([^"]*\)"$/\1/')
    echo -e "${GREEN}✅ 任务 ID: $JOB_ID${NC}"
    echo -e "${YELLOW}⏳ 等待生成 (约 1-5 分钟)...${NC}"
    
    # 轮询任务状态
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
                exit 0
            fi
        elif [[ "$STATUS" == "FAILED" ]]; then
            echo -e "${RED}❌ 生成失败${NC}"
            echo "$TASK_RESPONSE"
            exit 1
        else
            echo -ne "  进度：${ATTEMPT}s (状态：$STATUS)...\r"
        fi
    done
    
    echo -e "${RED}⏰ 超时${NC}"
    exit 1
else
    echo -e "${RED}❌ 任务提交失败${NC}"
    echo "响应：$RESPONSE"
    echo ""
    echo "请检查："
    echo "  1. 是否开通了视频生成服务：https://bailian.console.aliyun.com/"
    echo "  2. 模型名称是否正确"
    echo "  3. API Key 是否正确"
    exit 1
fi
