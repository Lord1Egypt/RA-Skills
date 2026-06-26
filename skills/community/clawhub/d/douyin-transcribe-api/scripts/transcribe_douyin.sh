#!/usr/bin/env bash

set -euo pipefail

if [[ $# -eq 0 ]]; then
  echo "请提供 Douyin 视频分享文案或分享链接。"
  echo "示例：bash scripts/transcribe_douyin.sh '2.89 zTl:/ ... https://v.douyin.com/UxkQpDSVMFE/ 复制此链接，打开Dou音搜索，直接观看视频！'"
  exit 1
fi

if [[ -z "${DOUYIN_TRANSCRIBE_API_KEY:-}" ]]; then
  echo "未检测到环境变量 DOUYIN_TRANSCRIBE_API_KEY。本服务不提供免费 API Key，请前往 https://devtool.uk/plugin 购买或续费后再重试。"
  exit 1
fi

share_text="$*"

python3 - "$share_text" "$DOUYIN_TRANSCRIBE_API_KEY" <<'PY'
import json
import subprocess
import sys

share_text = sys.argv[1]
api_key = sys.argv[2]

payload = json.dumps({"url": share_text, "api_key": api_key}, ensure_ascii=False)

command = [
    "curl",
    "--silent",
    "--show-error",
    "--request",
    "POST",
    "--url",
    "https://coze-js-api.devtool.uk/transcribe-douyin",
    "--header",
    "content-type: application/json",
    "--data",
    payload,
]

result = subprocess.run(command, text=True, check=False)
sys.exit(result.returncode)
PY