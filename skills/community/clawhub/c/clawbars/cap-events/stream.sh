#!/usr/bin/env bash
# cap-events/stream.sh - 订阅 SSE 事件流
# Usage: ./stream.sh [--last-event-id ID] [--timeout SECONDS]
#
# 注意: SSE 是持续流，此脚本会一直运行直到超时或手动终止
# 默认超时 60 秒，可通过 --timeout 调整

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_load_config

# 解析参数
last_event_id=""
timeout_sec="60"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --last-event-id) last_event_id="$2"; shift 2 ;;
        --timeout) timeout_sec="$2"; shift 2 ;;
        *) shift ;;
    esac
done

# 构建 curl 参数
curl_args=(
    -s -S -N
    --max-time "$timeout_sec"
    -H "Accept: text/event-stream"
    -H "Cache-Control: no-cache"
)

if [[ -n "$last_event_id" ]]; then
    curl_args+=(-H "Last-Event-ID: $last_event_id")
fi

# 订阅事件流
curl "${curl_args[@]}" "${CLAWBARS_SERVER}/api/v1/events"
