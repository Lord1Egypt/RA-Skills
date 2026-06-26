#!/bin/bash
# 调用提槽服务，为MCP工具调用填充参数
# 环境变量:
#   SLOT_SERVICE_URL   - 提槽服务完整 URL（如 http://host:port/path）
#   SLOT_SERVICE_TOKEN - Bearer token（使用真实服务时必填）
#   SLOT_INDEX_NAME    - indexName 参数（默认 financial_assistant_data_version_b）
#   SLOT_SCENE         - scene 参数（默认 基金）
#   SLOT_THRESHOLD     - 相似度阈值（默认 0.8）
#   MOCK_MODE          - 设为 "true" 时返回mock数据，不调用真实服务
# 参数: --query <改写后的query> --tools <工具列表JSON>

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
[ -f "${SCRIPT_DIR}/services.conf" ] && . "${SCRIPT_DIR}/services.conf"

QUERY=""
TOOLS=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --query)
      QUERY="$2"
      shift 2
      ;;
    --tools)
      TOOLS="$2"
      shift 2
      ;;
    *)
      echo "Unknown parameter: $1" >&2
      exit 1
      ;;
  esac
done

if [ -z "$QUERY" ]; then
  echo "Error: --query parameter is required" >&2
  exit 1
fi

if [ -z "$TOOLS" ]; then
  echo "Error: --tools parameter is required" >&2
  exit 1
fi

# Mock模式：模拟提槽，将产品名替换为基金代码，相对时间替换为绝对日期
if [ "${MOCK_MODE:-}" = "true" ]; then
  echo "[mock] Slot filling called with query: $QUERY" >&2
  TODAY=$(date +%Y-%m-%d)
  # 为每个工具填充模拟参数
  echo "$TOOLS" | jq --arg today "$TODAY" '
    [.[] | (if type == "string" then {"tool": .} else . end) + {
      "filled_params": {
        "fund_code": "001048",
        "fund_name": "富国新兴产业股票型证券投资基金",
        "date": $today,
        "period": "近一年"
      }
    }]
  '
  exit 0
fi

if [ -z "${SLOT_SERVICE_URL:-}" ]; then
  echo "Warning: SLOT_SERVICE_URL not set, returning tools with empty slots" >&2
  echo "$TOOLS"
  exit 0
fi

PAYLOAD=$(jq -n \
  --arg trace "slot_$$_$(date +%s)" \
  --arg query "$QUERY" \
  --arg index "${SLOT_INDEX_NAME:-financial_assistant_data_version_b}" \
  --arg scene "${SLOT_SCENE:-基金}" \
  --argjson threshold "${SLOT_THRESHOLD:-0.8}" \
  '{traceId: $trace, query: $query, indexName: $index, scene: $scene, vectorStoreType: "es", threshold: $threshold}')

RESPONSE=$(curl -s -X POST "${SLOT_SERVICE_URL}" \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "authorization: Bearer ${SLOT_SERVICE_TOKEN:-}" \
  -d "$PAYLOAD" \
  --connect-timeout 10 \
  --max-time 30)

if [ $? -ne 0 ] || [ -z "$RESPONSE" ]; then
  echo "Warning: Slot filling service call failed, returning original tools" >&2
  echo "$TOOLS"
  exit 0
fi

# 校验返回结果是有效JSON
if ! echo "$RESPONSE" | jq empty 2>/dev/null; then
  echo "Warning: Invalid slot filling response, returning original tools" >&2
  echo "$TOOLS"
  exit 0
fi

# 校验服务状态
if [ "$(echo "$RESPONSE" | jq -r '.status // empty')" != "success" ]; then
  echo "Warning: Slot filling service returned non-success status, returning original tools" >&2
  echo "$TOOLS"
  exit 0
fi

# 校验实体结果不为空
SCORES_COUNT=$(echo "$RESPONSE" | jq '.strictCodeWithScores | length')
if [ "${SCORES_COUNT:-0}" -eq 0 ]; then
  echo "Warning: Slot filling returned empty strictCodeWithScores, returning original tools" >&2
  echo "$TOOLS"
  exit 0
fi

# 按 span 分组，取 score 最高的候选项
ENTITY_MAP=$(echo "$RESPONSE" | jq '
  .strictCodeWithScores
  | group_by(.span)
  | map(
      sort_by(-.score) | first
      | {key: .span, value: {entity_name: .entity, entity_code: .code, entity_type: .type, score: .score}}
    )
  | from_entries
')

echo "$TOOLS" | jq --argjson entities "$ENTITY_MAP" \
  '[.[] | (if type == "string" then {"tool": .} else . end) + {"filled_params": {"entities": $entities}}]'
