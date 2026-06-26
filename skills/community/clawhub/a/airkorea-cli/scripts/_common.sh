#!/usr/bin/env bash
# _common.sh — shared helpers for airkorea-cli.
# Source this from each subcommand: `. "$here/_common.sh"`
#
# Wraps two 한국환경공단 (Korea Environment Corp.) services on data.go.kr:
#   - ArpltnInforInqireSvc: real-time air-quality measurements + forecasts.
#   - MsrstnInfoInqireSvc:  measuring-station directory + TM-coordinate utils.

set -euo pipefail

ARPLTN_BASE="${ARPLTN_BASE:-https://apis.data.go.kr/B552584/ArpltnInforInqireSvc}"
MSRSTN_BASE="${MSRSTN_BASE:-https://apis.data.go.kr/B552584/MsrstnInfoInqireSvc}"

require_bin() {
  for b in "$@"; do
    command -v "$b" >/dev/null 2>&1 || { echo "error: $b is required but not installed." >&2; exit 127; }
  done
}

require_key() {
  if [[ -z "${AIRKOREA_SERVICE_KEY:-}" ]]; then
    cat >&2 <<'EOF'
error: AIRKOREA_SERVICE_KEY must be set.
Register at https://www.data.go.kr/ and request approval (instant) for:
  "한국환경공단_에어코리아_대기오염정보"        (real-time + forecast)
  "한국환경공단_에어코리아_측정소정보"          (station directory + TM utilities)
Then export the *Decoding* key (raw, not URL-encoded) as AIRKOREA_SERVICE_KEY.
EOF
    exit 78
  fi
}

# valid_sido <name>  — accept either Korean or English label.
valid_sido() {
  case "$1" in
    전국|서울|부산|대구|인천|광주|대전|울산|경기|강원|충북|충남|전북|전남|경북|경남|제주|세종) ;;
    *) echo "error: sidoName '$1' invalid. Use one of: 전국 서울 부산 대구 인천 광주 대전 울산 경기 강원 충북 충남 전북 전남 경북 경남 제주 세종." >&2; exit 64;;
  esac
}

# valid_yyyymmdd <YYYY-MM-DD>
valid_yyyy_mm_dd() {
  if ! [[ "$1" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    echo "error: date '$1' must be YYYY-MM-DD." >&2
    exit 64
  fi
}

# valid_period <DAILY|HOUR|MONTH|3MONTH>
valid_period() {
  case "$1" in
    DAILY|HOUR|MONTH|3MONTH) ;;
    *) echo "error: dataTerm '$1' must be one of: DAILY HOUR MONTH 3MONTH." >&2; exit 64;;
  esac
}

# airkorea_get <base> <path> <key1=val1> ...
# - Adds serviceKey, returnType=json, _returnType=json, ver=1.5 automatically.
# - URL-encodes values via jq -r @uri.
# - Returns body on stdout. Non-2xx or non-OK resultCode prints to stderr and exits 22.
airkorea_get() {
  local base="$1" path="$2"; shift 2
  require_key

  local enc_key
  enc_key=$(printf '%s' "$AIRKOREA_SERVICE_KEY" | jq -Rrn '@uri inputs')
  # ver=1.5 surfaces extra metric flags (so2Flag, coFlag, …) on the realtime endpoints; harmless on others.
  local qs="serviceKey=${enc_key}&returnType=json&_returnType=json&ver=1.5"

  local kv k v enc_v
  for kv in "$@"; do
    [[ -z "$kv" ]] && continue
    k="${kv%%=*}"
    v="${kv#*=}"
    [[ -z "$v" ]] && continue
    enc_v=$(printf '%s' "$v" | jq -Rrn '@uri inputs')
    qs="${qs}&${k}=${enc_v}"
  done

  local out http
  out=$(mktemp)
  http=$(curl -sS -G -o "$out" -w '%{http_code}' "${base}/${path}?${qs}" || true)

  if [[ "$http" != 2* ]]; then
    echo "error: AirKorea returned HTTP $http for /${path}" >&2
    sed -e 's/^/  /' "$out" >&2
    rm -f "$out"
    exit 22
  fi

  # data.go.kr sometimes returns XML (with a SERVICE_KEY error envelope) even when returnType=json.
  if head -c 1 "$out" | grep -q '<'; then
    echo "error: AirKorea returned XML (likely a service-key or quota error) for /${path}" >&2
    sed -e 's/^/  /' "$out" >&2
    rm -f "$out"
    exit 22
  fi

  # Verify the JSON envelope's resultCode == "00".
  local rc rmsg
  rc=$(jq -r '.response.header.resultCode // "?"' "$out")
  rmsg=$(jq -r '.response.header.resultMsg  // ""'  "$out")
  if [[ "$rc" != "00" ]]; then
    echo "error: AirKorea resultCode=$rc resultMsg=$rmsg for /${path}" >&2
    rm -f "$out"
    exit 22
  fi

  cat "$out"
  rm -f "$out"
}

# emit_items <body-json>
# Extracts response.body.items as JSONL. Handles both array and single-object shapes.
emit_items() {
  jq -c '
    .response.body.items as $it
    | if   $it == null then empty
      elif ($it | type) == "array"  then $it[]
      else $it
      end
  '
}
