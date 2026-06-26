#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
INPUT="${1:-}"

if [ ! -f "$SKILL_DIR/.env" ] && [ -f "$SKILL_DIR/ENV_TEMPLATE.txt" ]; then
  cp "$SKILL_DIR/ENV_TEMPLATE.txt" "$SKILL_DIR/.env"
fi

if [ -f "$SKILL_DIR/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  source "$SKILL_DIR/.env"
  set +a
fi

if [ -z "$(printf '%s' "$INPUT" | tr -d '[:space:]')" ]; then
  python3 - <<'PY'
import json
print(json.dumps({
    "ok": False,
    "error": "缺少输入参数",
    "help": "Amazon Market Research",
    "first_run": "首次安装或更新后，请先执行：claw-update",
    "check_skill": "检查是否识别成功：openclaw skills list | grep amazon",
    "example_feishu": "/amazon-market-research 调研一下午餐盒在美国Amazon市场值不值得做",
    "example_local": "bash ~/.openclaw/workspace/skills/amazon-market-research/run.sh \"调研一下午餐盒在美国Amazon市场值不值得做\"",
    "env_file": "~/.openclaw/workspace/skills/amazon-market-research/.env",
    "env_required": [
        "MARKET_API_KEY",
        "MARKET_BASE_URL",
        "MARKET_MODEL"
    ]
}, ensure_ascii=False, indent=2))
PY
  exit 1
fi

python3 "$SKILL_DIR/skill.py" "$INPUT"