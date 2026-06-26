#!/bin/bash
# Resolve (close) comments on a Feishu docx document
# Usage: resolve_comments.sh <doc_token> <comment_id1,comment_id2,...>
# Or:    resolve_comments.sh <doc_token> --orphaned   (auto-resolve all orphaned comments)

set -euo pipefail

DOC_TOKEN="${1:?Usage: resolve_comments.sh <doc_token> <comment_id1,...|--orphaned>}"
TARGET="${2:?Usage: resolve_comments.sh <doc_token> <comment_id1,...|--orphaned>}"

# Read credentials from openclaw config
CONFIG_FILE="$HOME/.openclaw/openclaw.json"
APP_ID=$(grep -m1 '"appId"' "$CONFIG_FILE" | head -1 | sed 's/.*: *"\(.*\)".*/\1/')
APP_SECRET=$(grep -m1 '"appSecret"' "$CONFIG_FILE" | head -1 | sed 's/.*: *"\(.*\)".*/\1/')

# Detect domain
DOMAIN=$(grep -m1 '"domain"' "$CONFIG_FILE" | head -1 | sed 's/.*: *"\(.*\)".*/\1/' || echo "feishu")
if [ "$DOMAIN" = "lark" ]; then
  API_BASE="https://open.larksuite.com"
else
  API_BASE="https://open.feishu.cn"
fi

# Get tenant_access_token
TENANT_TOKEN=$(curl -s -X POST "${API_BASE}/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"${APP_ID}\",\"app_secret\":\"${APP_SECRET}\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['tenant_access_token'])" 2>/dev/null)

if [ -z "$TENANT_TOKEN" ]; then
  echo "Error: Failed to get tenant_access_token"
  exit 1
fi

# If --orphaned, find orphaned comment IDs automatically
if [ "$TARGET" = "--orphaned" ]; then
  # Get doc content
  DOC_CONTENT=$(curl -s -X GET \
    "${API_BASE}/open-apis/docx/v1/documents/${DOC_TOKEN}/raw_content" \
    -H "Authorization: Bearer ${TENANT_TOKEN}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('data', {}).get('content', ''))
" 2>/dev/null || echo "")

  # List all comments
  ALL_COMMENTS=$(curl -s -X GET \
    "${API_BASE}/open-apis/drive/v1/files/${DOC_TOKEN}/comments?file_type=docx&user_id_type=open_id" \
    -H "Authorization: Bearer ${TENANT_TOKEN}")

  COMMENT_IDS_STR=$(echo "$ALL_COMMENTS" | python3 -c "
import sys, json
data = json.load(sys.stdin)
items = data.get('data', {}).get('items', [])
ids = [item['comment_id'] for item in items]
print(','.join(ids))
" 2>/dev/null)

  if [ -z "$COMMENT_IDS_STR" ] || [ "$COMMENT_IDS_STR" = "" ]; then
    echo "No comments found."
    exit 0
  fi

  # Batch query for details
  IDS_JSON=$(echo "$COMMENT_IDS_STR" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read().strip().split(',')))")
  DETAIL=$(curl -s -X POST \
    "${API_BASE}/open-apis/drive/v1/files/${DOC_TOKEN}/comments/batch_query?file_type=docx&user_id_type=open_id" \
    -H "Authorization: Bearer ${TENANT_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"comment_ids\": ${IDS_JSON}}")

  # Find orphaned (open + anchor text gone)
  TARGET=$(echo "$DETAIL" | DOC_CONTENT="$DOC_CONTENT" python3 -c "
import sys, json, os
data = json.load(sys.stdin)
doc_content = os.environ.get('DOC_CONTENT', '')
items = data.get('data', {}).get('items', [])
orphaned = []
for item in items:
    if item.get('is_solved', False):
        continue
    quote = item.get('quote', '')[:50]
    if quote and quote not in doc_content:
        orphaned.append(item['comment_id'])
if orphaned:
    print(','.join(orphaned))
else:
    print('')
" 2>/dev/null)

  if [ -z "$TARGET" ]; then
    echo "No orphaned comments found."
    exit 0
  fi
  echo "Found orphaned comments: $TARGET"
fi

# Resolve each comment
IFS=',' read -ra IDS <<< "$TARGET"
for cid in "${IDS[@]}"; do
  RESP=$(curl -s -X PATCH \
    "${API_BASE}/open-apis/drive/v1/files/${DOC_TOKEN}/comments/${cid}?file_type=docx" \
    -H "Authorization: Bearer ${TENANT_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{"is_solved": true}')
  
  CODE=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('code', -1))" 2>/dev/null)
  if [ "$CODE" = "0" ]; then
    echo "✅ Resolved: ${cid}"
  else
    echo "❌ Failed: ${cid} — $(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('msg', 'unknown error'))" 2>/dev/null)"
  fi
done
