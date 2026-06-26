#!/usr/bin/env sh
# Auto-injected by OpenClaw Doctor — do not edit manually

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

eventType="${1:-start}"
errorMsg="${2:-}"

if command -v node >/dev/null 2>&1; then
  node "$SCRIPT_DIR/umami.js" "$eventType" "$errorMsg" >/dev/null 2>&1 || true
  exit 0
fi

escape_json() {
  printf '%s' "$1" | sed 's/"/\"/g'
}

eventTypeEsc=$(escape_json "$eventType")
errorMsgEsc=$(escape_json "$errorMsg")
errorField=''
if [ -n "$errorMsg" ]; then
  errorField=","errorMessage":"$errorMsgEsc""
fi

WEBSITE_ID='112cfe05-0cc1-48fb-a92f-65e1d66b81cf'
SKILL_ID_JSON=192
SKILL_NAME='deployment-workflow'
SKILL_VERSION_JSON="v1.1"
INSTALL_TIME='2026-04-09T13:57:00.764Z'
USER_INFO_JSON='{}'
UMAMI_ENDPOINT='https://umami.thousandrealms.win/api/send'

body=$(cat <<EOF
{"type":"event","payload":{"website":"$WEBSITE_ID","screen":"1512x982","language":"zh-CN","title":"龙虾医生","hostname":"xskillhub.com","url":"https://xskillhub.com/","referrer":"","name":"skill_exec_$eventTypeEsc","data":{"skillId":"$SKILL_ID_JSON","skillName":"$SKILL_NAME","skillVersion":"$SKILL_VERSION_JSON","installTime":"$INSTALL_TIME","eventType":"$eventTypeEsc","user":$USER_INFO_JSON,"platform":"龙虾医生"}}}
EOF
)

curl_response_file=$(mktemp)
curl_error_file=$(mktemp)
http_code=$(curl -sS -X POST "$UMAMI_ENDPOINT"   -H 'content-type: application/json'   -H 'accept: */*'   -H 'accept-language: zh-CN'   -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ????/1.2.9 Chrome/132.0.6834.210 Electron/34.5.8 Safari/537.36'   --data "$body"   -o "$curl_response_file"   -w '%{http_code}' 2>"$curl_error_file")
curl_exit=$?
curl_response=$(cat "$curl_response_file")
curl_error=$(cat "$curl_error_file")
rm -f "$curl_response_file" "$curl_error_file"

if [ "$curl_exit" -eq 0 ] && [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
  printf '[openclaw-doctor] 回执: 事件=%s, 状态=已上报(curl), HTTP=%s
' "$eventType" "$http_code" >&2
else
  printf '[openclaw-doctor] 回执: 事件=%s, 状态=上报失败(curl), 退出码=%s, HTTP=%s
' "$eventType" "$curl_exit" "$http_code" >&2
fi

