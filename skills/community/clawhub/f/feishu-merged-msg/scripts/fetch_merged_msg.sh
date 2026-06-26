#!/usr/bin/env bash
# Fetch the content of a Feishu merged/forwarded message by message_id.
# Usage: fetch_merged_msg.sh <message_id> <app_id> <app_secret>
# Output: JSON array of sub-messages

set -euo pipefail

MSG_ID="${1:?Usage: fetch_merged_msg.sh <message_id> <app_id> <app_secret>}"
APP_ID="${2:?Missing app_id}"
APP_SECRET="${3:?Missing app_secret}"

# 1. Get tenant access token
TOKEN=$(curl -sf -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"${APP_ID}\",\"app_secret\":\"${APP_SECRET}\"}" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")

# 2. Fetch message and its sub-messages
curl -sf "https://open.feishu.cn/open-apis/im/v1/messages/${MSG_ID}" \
  -H "Authorization: Bearer ${TOKEN}"
