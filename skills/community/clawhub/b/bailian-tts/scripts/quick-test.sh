#!/usr/bin/env bash
set -euo pipefail

# bailian-tts quick smoke test
# Usage:
#   ./scripts/quick-test.sh
#   ./scripts/quick-test.sh "要合成的文本" "音色" "语言"

TEXT="${1:-你好，这是百炼 TTS 的快速测试。}"
VOICE="${2:-Cherry}"
LANG="${3:-Chinese}"
OUT_DIR="${OUT_DIR:-$HOME/.openclaw/media/audio}"

mkdir -p "$OUT_DIR"

echo "[1/4] 检查 @hackerpl/bailian-cli ..."
if ! npm ls -g --depth=0 @hackerpl/bailian-cli >/dev/null 2>&1; then
  echo "未检测到 @hackerpl/bailian-cli，正在安装..."
  npm i -g @hackerpl/bailian-cli
fi

echo "[2/4] 检查 BAILIAN_API_KEY ..."
if [[ -z "${BAILIAN_API_KEY:-}" ]]; then
  echo "❌ 未设置 BAILIAN_API_KEY"
  echo "请先去阿里云百炼准备 API Key: https://bailian.console.aliyun.com/"
  echo "然后执行：export BAILIAN_API_KEY='sk-xxxx'"
  exit 1
fi

echo "[3/4] 打印可用音色（可选）..."
bailian tts --list-voices || true

echo "[4/4] 生成测试语音..."
TS="$(date +%Y%m%d-%H%M%S)"
LOG_FILE="$OUT_DIR/run-$TS.log"

set +e
bailian tts -t "$TEXT" -v "$VOICE" -l "$LANG" -o url -d "$OUT_DIR" | tee "$LOG_FILE"
CODE=${PIPESTATUS[0]}
set -e

if [[ $CODE -ne 0 ]]; then
  echo "❌ 生成失败，查看日志：$LOG_FILE"
  echo "排查建议：API Key / REGION / 网络 / 音色语言拼写"
  exit $CODE
fi

echo "✅ 生成完成"
echo "输出目录：$OUT_DIR"
echo "日志文件：$LOG_FILE"
