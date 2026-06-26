#!/bin/bash
set -e

# ==========================
# 自动安装逻辑（第一次运行）
# ==========================
if ! command -v edge-tts &> /dev/null; then
  echo "正在自动安装 edge-tts..."
  sudo apt update
  sudo apt install -y pipx jq
  pipx ensurepath
  source ~/.bashrc
  pipx install edge-tts
  echo "edge-tts 安装完成！"
fi

# ==========================
# 执行文本转语音
# ==========================
TEXT=$(echo "$1" | jq -r '.text')
OUTPUT=$(echo "$1" | jq -r '.output_path')

edge-tts --text "$TEXT" \
         --voice zh-CN-XiaoxiaoNeural \
         --write-media "$OUTPUT"

echo "{\"success\":true,\"file\":\"$OUTPUT\"}"