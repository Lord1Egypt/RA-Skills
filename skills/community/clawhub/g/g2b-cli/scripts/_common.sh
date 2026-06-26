#!/usr/bin/env bash
# _common.sh — shared helpers for g2b-cli.
# Source this from each subcommand: `. "$here/_common.sh"`
#
# Wraps three 조달청 (Public Procurement Service) services on data.go.kr —
# the public APIs behind 나라장터 (g2b.go.kr):
#   - BidPublicInfoService:    current bid announcements per 업무구분.
#   - CntrctInfoService:       contract / 계약현황 per 업무구분.
#   - PubDataOpnStdService:    개방표준 (unified) bid / awarded / contract feeds.

set -euo pipefail

G2B_BID_BASE="${G2B_BID_BASE:-https://apis.data.go.kr/1230000/ad/BidPublicInfoService}"
G2B_CNTRCT_BASE="${G2B_CNTRCT_BASE:-https://apis.data.go.kr/1230000/ao/CntrctInfoService}"
G2B_STD_BASE="${G2B_STD_BASE:-https://apis.data.go.kr/1230000/ao/PubDataOpnStdService}"

require_bin() {
  for b in "$@"; do
    command -v "$b" >/dev/null 2>&1 || { echo "error: $b is required but not installed." >&2; exit 127; }
  done
}

require_key() {
  if [[ -z "${G2B_SERVICE_KEY:-}" ]]; then
    cat >&2 <<'EOF'
error: G2B_SERVICE_KEY must be set.
Register at https://www.data.go.kr/ and request approval (instant for dev tier) for:
  "조달청_나라장터 입찰공고정보서비스"   (BidPublicInfoService)
  "조달청_나라장터 계약현황정보"           (CntrctInfoService)
  "조달청_나라장터 공공데이터개방표준서비스"  (PubDataOpnStdService)
Then export the *Decoding* key (raw, not URL-encoded) as G2B_SERVICE_KEY.
EOF
    exit 78
  fi
}

# valid_bsns <thng|servc|cnstwk|frgcpt>  — 업무구분 (goods / service / construction / foreign).
valid_bsns() {
  case "$1" in
    thng|servc|cnstwk|frgcpt) ;;
    *) echo "error: --type '$1' must be one of: thng (물품) servc (용역) cnstwk (공사) frgcpt (외자)." >&2; exit 64;;
  esac
}

# valid_inqry_div <1..5>  — 조회구분.
#   1=등록일시, 2=공고게시일자, 3=공고번호, 4=공고기관코드, 5=수요기관코드
valid_inqry_div() {
  case "$1" in
    1|2|3|4|5) ;;
    *) echo "error: --inquiry-div '$1' must be 1..5 (1=등록 2=공고게시 3=공고번호 4=공고기관 5=수요기관)." >&2; exit 64;;
  esac
}

# valid_dt12 <YYYYMMDDHHMM>  — 12-digit timestamp required by data.go.kr g2b.
valid_dt12() {
  if ! [[ "$1" =~ ^[0-9]{12}$ ]]; then
    echo "error: timestamp '$1' must be YYYYMMDDHHMM (12 digits, e.g. 202604300000)." >&2
    exit 64
  fi
}

# default_window  — emits "FROM TO" for the last N days (default 7) as YYYYMMDDHHMM.
default_window() {
  local days="${1:-7}"
  local now from
  now=$(date -u +%Y%m%d%H%M)
  if date -v -1d +%Y%m%d >/dev/null 2>&1; then
    from=$(date -v -"${days}"d +%Y%m%d)0000
  else
    from=$(date -u -d "-${days} days" +%Y%m%d)0000
  fi
  printf '%s %s\n' "$from" "$now"
}

# g2b_get <base> <path> <key=val> ...
# - Adds serviceKey, type=json automatically.
# - URL-encodes values via jq -r @uri.
# - Returns body on stdout. Non-2xx, XML envelopes, or non-OK resultCode → stderr + exit 22.
g2b_get() {
  local base="$1" path="$2"; shift 2
  require_key

  local enc_key
  enc_key=$(printf '%s' "$G2B_SERVICE_KEY" | jq -sRr '@uri')
  local qs="serviceKey=${enc_key}&type=json"

  local kv k v enc_v
  for kv in "$@"; do
    [[ -z "$kv" ]] && continue
    k="${kv%%=*}"
    v="${kv#*=}"
    [[ -z "$v" ]] && continue
    enc_v=$(printf '%s' "$v" | jq -sRr '@uri')
    qs="${qs}&${k}=${enc_v}"
  done

  local out http
  out=$(mktemp)
  http=$(curl -sS -G -o "$out" -w '%{http_code}' "${base}/${path}?${qs}" || true)

  if [[ "$http" != 2* ]]; then
    echo "error: g2b returned HTTP $http for /${path}" >&2
    sed -e 's/^/  /' "$out" >&2
    rm -f "$out"
    exit 22
  fi

  # data.go.kr sometimes returns XML (with a SERVICE_KEY error envelope) even when type=json.
  if head -c 1 "$out" | grep -q '<'; then
    echo "error: g2b returned XML (likely a service-key, quota, or path error) for /${path}" >&2
    sed -e 's/^/  /' "$out" >&2
    rm -f "$out"
    exit 22
  fi

  local rc rmsg
  rc=$(jq -r '.response.header.resultCode // "?"' "$out")
  rmsg=$(jq -r '.response.header.resultMsg  // ""'  "$out")
  if [[ "$rc" != "00" ]]; then
    echo "error: g2b resultCode=$rc resultMsg=$rmsg for /${path}" >&2
    rm -f "$out"
    exit 22
  fi

  cat "$out"
  rm -f "$out"
}

# emit_items <body-json>
# Extracts response.body.items as JSONL. Handles array, single-object, and empty shapes.
emit_items() {
  jq -c '
    .response.body.items as $it
    | if   $it == null then empty
      elif ($it | type) == "array"  then $it[]
      elif ($it | type) == "object" and ($it.item != null)
        then if ($it.item | type) == "array" then $it.item[] else $it.item end
      else $it
      end
  '
}

# emit_meta <body-json>
# Prints response.body summary: totalCount, pageNo, numOfRows on a single JSON line.
emit_meta() {
  jq -c '{totalCount: (.response.body.totalCount // null), pageNo: (.response.body.pageNo // null), numOfRows: (.response.body.numOfRows // null)}'
}
