#!/usr/bin/env bash
# 301重定向检查 - XiaoMeng AGI Service
# Usage: ./analyze.sh "your data and analysis requirements"

QUESTION="${1:-Analyze the provided data}"
SERVICE_ID="${2:-301重定向检查}"
API_BASE="${XIAOMENG_API_BASE:-https://xiaomeng-api.qisir.com}"

# Step 1: Create order
echo "Creating order..."
ORDER_RESP=$(curl -s -X POST "$API_BASE/api/createOrder" \
  -H "Content-Type: application/json" \
  -d "{\"reqData\": {\"question\": \"$QUESTION\", \"serviceId\": \"$SERVICE_ID\"}}")

echo "$ORDER_RESP" | python3 -m json.tool 2>/dev/null || echo "$ORDER_RESP"

# Extract orderNo
ORDER_NO=$(echo "$ORDER_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['resultData']['orderNo'])" 2>/dev/null)

if [ -z "$ORDER_NO" ]; then
  echo "Error: Failed to create order"
  exit 1
fi

echo ""
echo "Order created: $ORDER_NO"
echo "Price: ¥8"
echo "Please complete payment via ClawTip, then run:"
echo "  ./get_result.sh \"$ORDER_NO\" \"<credential>\" \"$QUESTION\""
