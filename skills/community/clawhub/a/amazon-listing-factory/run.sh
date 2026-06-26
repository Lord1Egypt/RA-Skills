#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
INPUT="${1:-}"

if [ -f "$SKILL_DIR/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  source "$SKILL_DIR/.env"
  set +a
fi

if [ ! -f "$SKILL_DIR/.env" ] && [ -f "$SKILL_DIR/ENV_TEMPLATE.txt" ]; then
  cp "$SKILL_DIR/ENV_TEMPLATE.txt" "$SKILL_DIR/.env"
fi

if [ -z "$(printf '%s' "$INPUT" | tr -d '[:space:]')" ]; then
  python3 - <<'PY'
import json
print(json.dumps({
    "ok": False,
    "error": "缺少输入参数",
    "help": "Amazon Listing Factory",
    "first_run": "首次安装或更新后，请先执行：openclaw gateway restart",
    "check_skill": "检查是否识别成功：openclaw skills list | grep amazon",
    "example_feishu": "/amazon_listing_factory 生成listing：充电宝，美国站，突出便携、大容量、安全感，输出6张图",
    "example_local": "bash ~/.openclaw/workspace/skills/amazon-listing-factory/run.sh \"生成listing：充电宝，美国站，突出便携、大容量、安全感，输出6张图\"",
    "env_file": "~/.openclaw/workspace/skills/amazon-listing-factory/.env",
    "mihe": "如需自动生图，可前往米核获取 KEY：miheai.com/s/98707"
}, ensure_ascii=False, indent=2))
PY
  exit 1
fi

python3 "$SKILL_DIR/skill.py" "$INPUT"
