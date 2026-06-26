#!/usr/bin/env bash
# Poll/retrieve results for an existing crawl job
# Usage: poll.sh <job-id> [--raw] [--status completed|queued|errored]
set -euo pipefail

if [[ -f ~/.clawdbot/secrets/cloudflare-crawl.env ]]; then
  source ~/.clawdbot/secrets/cloudflare-crawl.env
fi
: "${CF_ACCOUNT_ID:?Set CF_ACCOUNT_ID}"
: "${CF_CRAWL_API_TOKEN:?Set CF_CRAWL_API_TOKEN}"

BASE="https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/browser-rendering/crawl"
JOB_ID="${1:?Usage: poll.sh <job-id>}"
shift
RAW=false
STATUS_FILTER=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --raw) RAW=true; shift;;
    --status) STATUS_FILTER="$2"; shift 2;;
    *) shift;;
  esac
done

QUERY=""
[[ -n "$STATUS_FILTER" ]] && QUERY="?status=$STATUS_FILTER"

RESULT=$(curl -s "$BASE/$JOB_ID$QUERY" \
  -H "Authorization: Bearer $CF_CRAWL_API_TOKEN")

if [[ "$RAW" == "true" ]]; then
  echo "$RESULT" | jq .
else
  echo "$RESULT" | jq '{
    job_id: .result.id,
    status: .result.status,
    browser_seconds: .result.browserSecondsUsed,
    total: .result.total,
    finished: .result.finished,
    pages: [.result.records[]? | {
      url: .url,
      title: .metadata.title,
      status: .status,
      content_length: ((.markdown // .html // "") | length)
    }]
  }'
fi
