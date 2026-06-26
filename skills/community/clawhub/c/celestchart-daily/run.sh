#!/bin/bash
# ============================================================
# CelestChart 运势与本命盘 API 调用脚本
# 使用前请配置以下环境变量（见 README.md）
# ============================================================

ACTION="${1:-daily}"

API_KEY="${CELESTCHART_API_KEY}"
BASE_URL="https://xp.broad-intelli.com"

# 出生信息（从环境变量读取）
BIRTH_YEAR="${CELESTCHART_BIRTH_YEAR}"
BIRTH_MONTH="${CELESTCHART_BIRTH_MONTH}"
BIRTH_DAY="${CELESTCHART_BIRTH_DAY}"
BIRTH_HOUR="${CELESTCHART_BIRTH_HOUR:-12}"
BIRTH_MINUTE="${CELESTCHART_BIRTH_MINUTE:-0}"
BIRTH_LON="${CELESTCHART_BIRTH_LON:-116.4}"
BIRTH_LAT="${CELESTCHART_BIRTH_LAT:-39.9}"
BIRTH_TZ="${CELESTCHART_BIRTH_TZ:-8}"

# ── 参数校验 ──────────────────────────────────────────────
if [ "$ACTION" = "daily" ]; then
  if [ -z "$API_KEY" ]; then
    echo '{"error": "未配置 CELESTCHART_API_KEY，请先设置环境变量。前往CelestChart官网 https://xp.broad-intelli.com 用户中心生成 API Key。"}'
    exit 1
  fi
fi

if [ -z "$BIRTH_YEAR" ] || [ -z "$BIRTH_MONTH" ] || [ -z "$BIRTH_DAY" ]; then
  echo '{"error": "未配置出生信息，请设置 CELESTCHART_BIRTH_YEAR / BIRTH_MONTH / BIRTH_DAY 环境变量。"}'
  exit 1
fi

# ── 数字格式校验（防止命令注入）──────────────────────────
_validate_number() {
  local name="$1" val="$2"
  if ! echo "$val" | grep -qE '^-?[0-9]+(\.[0-9]+)?$'; then
    echo "{\"error\": \"参数 ${name} 格式无效，必须为数字。\"}"
    exit 1
  fi
}
_validate_number BIRTH_YEAR    "$BIRTH_YEAR"
_validate_number BIRTH_MONTH   "$BIRTH_MONTH"
_validate_number BIRTH_DAY     "$BIRTH_DAY"
_validate_number BIRTH_HOUR    "$BIRTH_HOUR"
_validate_number BIRTH_MINUTE  "$BIRTH_MINUTE"
_validate_number BIRTH_LON     "$BIRTH_LON"
_validate_number BIRTH_LAT     "$BIRTH_LAT"
_validate_number BIRTH_TZ      "$BIRTH_TZ"

# ── 调用 API ──────────────────────────────────────────────
if [ "$ACTION" = "birthchart" ]; then
  RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
    "${BASE_URL}/api/v1/birth-chart" \
    -H "Content-Type: application/json" \
    -d "{
      \"year\": ${BIRTH_YEAR},
      \"month\": ${BIRTH_MONTH},
      \"day\": ${BIRTH_DAY},
      \"hour\": ${BIRTH_HOUR},
      \"minute\": ${BIRTH_MINUTE},
      \"longitude\": ${BIRTH_LON},
      \"latitude\": ${BIRTH_LAT},
      \"timezone\": ${BIRTH_TZ},
      \"house_system\": \"P\"
    }")
else
  RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
    "${BASE_URL}/api/v1/public/daily-forecast" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: ${API_KEY}" \
    -d "{
      \"birth_year\": ${BIRTH_YEAR},
      \"birth_month\": ${BIRTH_MONTH},
      \"birth_day\": ${BIRTH_DAY},
      \"birth_hour\": ${BIRTH_HOUR},
      \"birth_minute\": ${BIRTH_MINUTE},
      \"birth_longitude\": ${BIRTH_LON},
      \"birth_latitude\": ${BIRTH_LAT},
      \"birth_timezone\": ${BIRTH_TZ},
      \"house_system\": \"W\"
    }")
fi

# 分离响应体和状态码（兼容 macOS / Linux）
HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)
HTTP_BODY=$(echo "$RESPONSE" | sed '$d')

# ── 错误处理 ──────────────────────────────────────────────
if [ "$HTTP_CODE" = "401" ]; then
  echo '{"error": "API Key 无效或已失效，请前往CelestChart官网 https://xp.broad-intelli.com 用户中心检查。"}'
  exit 1
elif [ "$HTTP_CODE" = "403" ]; then
  echo '{"error": "VIP 已过期或无权限，请前往CelestChart官网 https://xp.broad-intelli.com 续费 VIP 后重试。"}'
  exit 1
elif [ "$HTTP_CODE" != "200" ]; then
  echo "{\"error\": \"API 请求失败（HTTP ${HTTP_CODE}）\", \"detail\": ${HTTP_BODY}}"
  exit 1
fi

# ── 输出结果 ──────────────────────────────────────────────
echo "$HTTP_BODY"