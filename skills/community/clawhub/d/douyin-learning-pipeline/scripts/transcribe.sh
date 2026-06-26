#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <audio_file> [model]" >&2
    echo "  model: teleai (default) | sensevoice" >&2
    exit 1
fi

AUDIO_FILE="$1"
MODEL="${2:-teleai}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$SKILL_DIR/local/config.json"
BASE_URL="https://api.siliconflow.cn/v1"
API_KEY="${SILICONFLOW_API_KEY:-}"

if [[ -z "$API_KEY" && -f "$CONFIG_FILE" ]]; then
    API_KEY=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('siliconflow_api_key',''))" 2>/dev/null || true)
    CONF_BASE=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('siliconflow_base_url',''))" 2>/dev/null || true)
    if [[ -n "$CONF_BASE" ]]; then
        BASE_URL="$CONF_BASE"
    fi
fi

if [[ -z "$API_KEY" ]]; then
    echo "错误: 未配置 SiliconFlow API Key" >&2
    echo "请设置环境变量: export SILICONFLOW_API_KEY='your-key'" >&2
    echo "或运行配置脚本: python3 scripts/setup_config.py" >&2
    exit 1
fi

case "$MODEL" in
    teleai) MODEL_NAME="TeleAI/TeleSpeechASR" ;;
    sensevoice) MODEL_NAME="FunAudioLLM/SenseVoiceSmall" ;;
    *) echo "错误: 未知模型 $MODEL" >&2; exit 1 ;;
esac

echo "使用模型: $MODEL_NAME"
echo "音频文件: $AUDIO_FILE"
echo ""

RESPONSE=$(curl -sS --request POST \
    --url "$BASE_URL/audio/transcriptions" \
    -H "Authorization: Bearer $API_KEY" \
    -F "file=@$AUDIO_FILE" \
    -F "model=$MODEL_NAME")

TEXT=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('text','').strip())" 2>/dev/null || echo "$RESPONSE")

echo "转写结果:"
echo "$TEXT"
echo ""

OUTPUT_FILE="${AUDIO_FILE%.*}.transcript.txt"
echo "$TEXT" > "$OUTPUT_FILE"
echo "已保存到: $OUTPUT_FILE"
