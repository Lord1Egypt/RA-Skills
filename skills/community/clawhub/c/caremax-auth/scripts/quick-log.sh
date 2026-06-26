#!/usr/bin/env bash
# 快捷记一笔：按 preset_key 写入单条数值（与 App 「快捷记一笔」一致）
# 用法:
#   bash quick-log.sh <preset_key> <value>
#   bash quick-log.sh <preset_key> <value> --unit kg --date 2026-03-29 --member <family_member_uuid>
#
# 先运行 list-system-presets.sh 查看合法的 preset_key 与默认单位。

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

usage() {
  echo "Usage: quick-log.sh <preset_key> <value> [--unit UNIT] [--date YYYY-MM-DD] [--member MEMBER_UUID]" >&2
  exit 1
}

[[ $# -ge 2 ]] || usage
PRESET_KEY="$1"
VALUE="$2"
shift 2

UNIT=""
TEST_DATE=""
MEMBER_ID=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --unit)
      [[ $# -ge 2 ]] || usage
      UNIT="$2"
      shift 2
      ;;
    --date)
      [[ $# -ge 2 ]] || usage
      TEST_DATE="$2"
      shift 2
      ;;
    --member)
      [[ $# -ge 2 ]] || usage
      MEMBER_ID="$2"
      shift 2
      ;;
    *)
      usage
      ;;
  esac
done

BODY="$(
  CM_PRESET_KEY="$PRESET_KEY" \
  CM_VALUE="$VALUE" \
  CM_UNIT="$UNIT" \
  CM_TEST_DATE="$TEST_DATE" \
  CM_MEMBER_ID="$MEMBER_ID" \
  python3 -c 'import json, os
d = {"preset_key": os.environ["CM_PRESET_KEY"], "value": os.environ["CM_VALUE"]}
if os.environ.get("CM_UNIT", "").strip():
    d["unit"] = os.environ["CM_UNIT"].strip()
if os.environ.get("CM_TEST_DATE", "").strip():
    d["test_date"] = os.environ["CM_TEST_DATE"].strip()
if os.environ.get("CM_MEMBER_ID", "").strip():
    d["member_id"] = os.environ["CM_MEMBER_ID"].strip()
print(json.dumps(d, ensure_ascii=False))
')"

exec "$SCRIPT_DIR/api-call.sh" POST /api/indicators/quick-log "$BODY"
