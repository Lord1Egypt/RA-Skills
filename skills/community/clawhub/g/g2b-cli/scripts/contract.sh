#!/usr/bin/env bash
# contract.sh — CntrctInfoService: 나라장터 계약현황 (signed contracts per 업무구분).
#
# Wraps four 업무구분 endpoints under one flag (--type):
#   thng    → getCntrctInfoListThng     (물품)
#   servc   → getCntrctInfoListServc    (용역)
#   cnstwk  → getCntrctInfoListCnstwk   (공사)
#   frgcpt  → getCntrctInfoListFrgcpt   (외자)
#
# Usage:
#   contract.sh --type thng                          # 물품 last 7 days
#   contract.sh --type servc --from 202604010000 --to 202604300000
#   contract.sh --type cnstwk --inquiry-div 4 --instt-cd 6110000
#   contract.sh --type thng --cntrct-no 2026000123 --meta
#
# Output: JSONL — one row per 계약. Use --meta for the response summary instead.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

bsns="thng" inquiry_div="" from="" to="" rows="100" page="1" cntrct_no="" instt_cd="" dminstt_cd="" meta=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --type)          bsns="$2";        shift 2;;
    --inquiry-div)   inquiry_div="$2"; shift 2;;
    --from)          from="$2";        shift 2;;
    --to)            to="$2";          shift 2;;
    --rows)          rows="$2";        shift 2;;
    --page)          page="$2";        shift 2;;
    --cntrct-no)     cntrct_no="$2";   shift 2;;
    --instt-cd)      instt_cd="$2";    shift 2;;
    --dminstt-cd)    dminstt_cd="$2";  shift 2;;
    --meta)          meta=1;           shift;;
    -h|--help)
      sed -n '2,18p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

require_bin curl jq
valid_bsns "$bsns"

case "$bsns" in
  thng)   op="getCntrctInfoListThng";;
  servc)  op="getCntrctInfoListServc";;
  cnstwk) op="getCntrctInfoListCnstwk";;
  frgcpt) op="getCntrctInfoListFrgcpt";;
esac

if [[ -z "$cntrct_no" && ( -z "$from" || -z "$to" ) ]]; then
  read from to < <(default_window 7)
fi
[[ -n "$from" ]] && valid_dt12 "$from"
[[ -n "$to"   ]] && valid_dt12 "$to"
[[ -n "$inquiry_div" ]] && valid_inqry_div "$inquiry_div"

declare -a params=( "numOfRows=$rows" "pageNo=$page" )

if [[ -n "$cntrct_no" ]]; then
  # 계약번호 단건 조회 (inqryDiv=2)
  params+=( "inqryDiv=2" "cntrctNo=$cntrct_no" )
elif [[ -n "$dminstt_cd" ]]; then
  params+=( "inqryDiv=${inquiry_div:-3}" "dminsttCd=$dminstt_cd" "inqryBgnDt=$from" "inqryEndDt=$to" )
elif [[ -n "$instt_cd" ]]; then
  params+=( "inqryDiv=${inquiry_div:-4}" "ntceInsttCd=$instt_cd" "inqryBgnDt=$from" "inqryEndDt=$to" )
else
  params+=( "inqryDiv=${inquiry_div:-1}" "inqryBgnDt=$from" "inqryEndDt=$to" )
fi

resp=$(g2b_get "$G2B_CNTRCT_BASE" "$op" "${params[@]}")

if (( meta )); then
  echo "$resp" | emit_meta
else
  echo "$resp" | emit_items
fi
