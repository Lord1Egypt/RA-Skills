#!/usr/bin/env bash
# bid_monitor.sh - Multi-platform bidding announcement scraper
# Usage: bash bid_monitor.sh [--platform <name>] [--fresh] [--date YYYY-MM-DD]
# Output: JSON lines to stdout, cached in bid_cache/

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CACHE_DIR="${SCRIPT_DIR}/bid_cache"
mkdir -p "$CACHE_DIR"

PLATFORM=""
FRESH=0
TARGET_DATE=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --platform) PLATFORM="$2"; shift 2;;
    --fresh) FRESH=1; shift;;
    --date) TARGET_DATE="$2"; shift 2;;
    *) echo "Unknown option: $1" >&2; exit 1;;
  esac
done

[[ -z "$TARGET_DATE" ]] && TARGET_DATE="$(date +%Y-%m-%d)"
CACHE_FILE="${CACHE_DIR}/bid_${TARGET_DATE}.jsonl"

# --- Platform adapters ---
# Each adapter function: fetch_list <date> -> JSON lines to stdout
# Format per line: {"id":"...","title":"...","source":"...","url":"...","publish_time":"..."}

# Adapter: cnooc (中海油采办业务管理与交易系统)
fetch_cnooc() {
  local date="$1"
  local base="https://bid.cnooc.com.cn"
  local api="${base}/api/v1/bid/list"
  local page=1
  local total=0
  local max_pages=10

  while [[ $page -le $max_pages ]]; do
    local resp
    resp=$(curl -sf --max-time 15 \
      -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
      -H "Accept: application/json" \
      "${api}?page=${page}&pageSize=50&type=1" 2>/dev/null) || {
      echo "WARN: cnooc page ${page} failed, retrying after cooldown..." >&2
      sleep 10
      resp=$(curl -sf --max-time 15 \
        -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
        -H "Accept: application/json" \
        "${api}?page=${page}&pageSize=50&type=1" 2>/dev/null) || break
    }

    local items
    items=$(echo "$resp" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    rows = data.get('data', {}).get('list', data.get('data', {}).get('rows', []))
    if not isinstance(rows, list): rows = []
    for r in rows:
        ct = r.get('createdTime', r.get('publishTime', ''))
        title = r.get('title', '')
        rid = str(r.get('id', ''))
        # Filter: only today's publications
        if '${date}' not in ct: continue
        # Skip non-bid types
        t = r.get('type', r.get('noticeType', ''))
        skip_words = ['结果', '中标', '成交']
        if any(w in title for w in skip_words): continue
        url = 'https://bid.cnooc.com.cn/home/#/newsAlertDetails?index=0&childrenActive=1&id=' + rid + '&type=null'
        print(json.dumps({'id': rid, 'title': title, 'source': 'cnooc', 'url': url, 'publish_time': ct}, ensure_ascii=False))
except Exception as e:
    sys.stderr.write(f'Parse error: {e}\n')
" 2>/dev/null) || break

    [[ -z "$items" ]] && break
    echo "$items"
    total=$((total + $(echo "$items" | wc -l)))
    sleep 2  # Rate limit
    page=$((page + 1))
  done

  echo "cnooc: fetched ${total} items for ${date}" >&2
}

# Adapter: cebpubservice (中国招标投标公共服务平台)
fetch_cebpubservice() {
  local date="$1"
  local api="https://ctbpsp.com/cutomNoticeApi/getNoticeList"
  local page=1
  local total=0
  local max_pages=10

  while [[ $page -le $max_pages ]]; do
    local resp
    resp=$(curl -sf --max-time 15 \
      -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
      -H "Content-Type: application/json" \
      -d "{\"pageNo\":${page},\"pageSize\":50,\"startDate\":\"${date}\",\"endDate\":\"${date}\"}" \
      "$api" 2>/dev/null) || break

    local items
    items=$(echo "$resp" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    rows = data.get('data', {}).get('list', data.get('rows', []))
    if not isinstance(rows, list): rows = []
    for r in rows:
        title = r.get('title', r.get('noticeTitle', ''))
        rid = str(r.get('id', r.get('noticeId', '')))
        ct = r.get('publishTime', r.get('createTime', ''))
        url = r.get('url', r.get('detailUrl', ''))
        if not url: url = 'https://ctbpsp.com/#/noticeDetail?id=' + rid
        print(json.dumps({'id': rid, 'title': title, 'source': 'cebpubservice', 'url': url, 'publish_time': ct}, ensure_ascii=False))
except Exception as e:
    sys.stderr.write(f'Parse error: {e}\n')
" 2>/dev/null) || break

    [[ -z "$items" ]] && break
    echo "$items"
    total=$((total + $(echo "$items" | wc -l)))
    sleep 2
    page=$((page + 1))
  done

  echo "cebpubservice: fetched ${total} items for ${date}" >&2
}

# Adapter: ccgp (中国政府采购网)
fetch_ccgp() {
  local date="$1"
  local api="http://www.ccgp.gov.cn/cggg/dfgg/index.htm"
  local total=0

  # CCGP uses HTML pages, parse with python
  local resp
  resp=$(curl -sf --max-time 15 \
    -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
    "$api" 2>/dev/null) || {
    echo "WARN: ccgp fetch failed" >&2
    return 0
  }

  echo "$resp" | python3 -c "
import sys, re, json
from html.parser import HTMLParser

html = sys.stdin.read()
# Simple regex extraction for announcement links
pattern = r'<a[^>]*href=[\"\\']([^\"\\']+)[\"\\'][^>]*>([^<]+)</a>'
matches = re.findall(pattern, html)
for url, title in matches:
    title = title.strip()
    if not title or len(title) < 5: continue
    if '通知' not in title and '公告' not in title and '招标' not in title: continue
    if not url.startswith('http'): url = 'http://www.ccgp.gov.cn' + url
    print(json.dumps({'id': url.split('/')[-1].replace('.htm',''), 'title': title, 'source': 'ccgp', 'url': url, 'publish_time': '${date}'}, ensure_ascii=False))
" 2>/dev/null || true

  echo "ccgp: fetched from ${date}" >&2
}

# --- Custom sources (A5): user-defined platforms via sources.json ---
# No adapter code needed — define endpoints in sources.json (see sources.example.json)
fetch_custom() {
  local src="${SCRIPT_DIR}/sources.json"
  [[ -f "$src" ]] || return 0
  python3 "${SCRIPT_DIR}/custom_source.py" "$src" 2>/dev/null
}

# --- Main ---
PLATFORMS=("cnooc" "cebpubservice" "ccgp")
[[ -n "$PLATFORM" ]] && PLATFORMS=("$PLATFORM")

# Cache check
if [[ $FRESH -eq 0 ]] && [[ -f "$CACHE_FILE" ]]; then
  echo "Using cached data from $CACHE_FILE" >&2
  cat "$CACHE_FILE"
  exit 0
fi

> "$CACHE_FILE"

for plat in "${PLATFORMS[@]}"; do
  echo "Fetching $plat ..." >&2
  fetch_fn="fetch_${plat}"
  if type "$fetch_fn" &>/dev/null; then
    "$fetch_fn" "$TARGET_DATE" >> "$CACHE_FILE" 2>/dev/null || echo "WARN: $plat failed" >&2
  else
    echo "WARN: no adapter for platform '$plat', skipping" >&2
  fi
done

# Custom (user-defined) sources
if [[ -f "${SCRIPT_DIR}/sources.json" ]]; then
  echo "Fetching custom sources ..." >&2
  fetch_custom >> "$CACHE_FILE" 2>/dev/null || echo "WARN: custom sources failed" >&2
fi

echo "Done. Total: $(wc -l < "$CACHE_FILE") items cached at $CACHE_FILE" >&2
cat "$CACHE_FILE"
