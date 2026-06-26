#!/usr/bin/env bash
# std.sh — PubDataOpnStdService: 공공데이터개방표준 (unified, schema-stable feeds).
#
# One subcommand for all three open-standard data sets:
#   bid       → getDataSetOpnStdBidPblancInfo  (입찰공고 표준)
#   awarded   → getDataSetOpnStdScsbidInfo     (낙찰 표준)
#   contract  → getDataSetOpnStdCntrctInfo     (계약 표준)
#
# Why "std"?
#   The non-std endpoints (BidPublicInfoService, CntrctInfoService) have separate
#   shapes per 업무구분 (thng/servc/cnstwk/frgcpt). The 개방표준 service collapses
#   all four 업무구분 into a single canonical schema — easier for warehouses + dashboards.
#
# Usage:
#   std.sh --what bid                         # last 7 days, 100 rows
#   std.sh --what awarded --from 202604010000 --to 202604300000 --rows 500
#   std.sh --what contract --bid-no 20240412345-00 --meta
#
# Output: JSONL — one row per record. Use --meta for the response summary instead.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

what="" from="" to="" rows="100" page="1" bid_no="" instt_cd="" dminstt_cd="" meta=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --what)          what="$2";        shift 2;;
    --from)          from="$2";        shift 2;;
    --to)            to="$2";          shift 2;;
    --rows)          rows="$2";        shift 2;;
    --page)          page="$2";        shift 2;;
    --bid-no)        bid_no="$2";      shift 2;;
    --instt-cd)      instt_cd="$2";    shift 2;;
    --dminstt-cd)    dminstt_cd="$2";  shift 2;;
    --meta)          meta=1;           shift;;
    -h|--help)
      sed -n '2,21p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

require_bin curl jq

case "$what" in
  bid)      op="getDataSetOpnStdBidPblancInfo";;
  awarded)  op="getDataSetOpnStdScsbidInfo";;
  contract) op="getDataSetOpnStdCntrctInfo";;
  *) echo "error: --what must be one of: bid awarded contract." >&2; exit 64;;
esac

if [[ -z "$bid_no" && ( -z "$from" || -z "$to" ) ]]; then
  read from to < <(default_window 7)
fi
[[ -n "$from" ]] && valid_dt12 "$from"
[[ -n "$to"   ]] && valid_dt12 "$to"

declare -a params=( "numOfRows=$rows" "pageNo=$page" )

# The std service uses different begin/end-date param names per dataset.
# All accept bidNtceBgnDt/bidNtceEndDt as the canonical filter window.
if [[ -n "$bid_no" ]]; then
  params+=( "bidNtceNo=$bid_no" )
else
  params+=( "bidNtceBgnDt=$from" "bidNtceEndDt=$to" )
fi
[[ -n "$instt_cd"   ]] && params+=( "ntceInsttCd=$instt_cd" )
[[ -n "$dminstt_cd" ]] && params+=( "dminsttCd=$dminstt_cd" )

resp=$(g2b_get "$G2B_STD_BASE" "$op" "${params[@]}")

if (( meta )); then
  echo "$resp" | emit_meta
else
  echo "$resp" | emit_items
fi
