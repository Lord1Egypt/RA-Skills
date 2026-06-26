#!/usr/bin/env bash
# bid.sh — BidPublicInfoService: 나라장터 입찰공고 (current bidding announcements).
#
# Wraps four 업무구분 endpoints under one flag (--type):
#   thng    → getBidPblancListInfoThng     (물품)
#   servc   → getBidPblancListInfoServc    (용역)
#   cnstwk  → getBidPblancListInfoCnstwk   (공사)
#   frgcpt  → getBidPblancListInfoFrgcpt   (외자)
# Plus a keyword-search variant under --keyword (uses getBidPblancListInfoServcPPSSrch
# for 용역 — the only 업무구분 with a documented PPS keyword endpoint).
#
# Usage:
#   bid.sh --type thng                          # 물품 last 7 days
#   bid.sh --type servc --from 202604010000 --to 202604300000
#   bid.sh --type cnstwk --inquiry-div 5 --dminstt-cd 6110000
#   bid.sh --type thng --bid-no 20240412345-00
#   bid.sh --keyword 인공지능 --rows 50           # PPS 검색 (servc only)
#   bid.sh --type thng --meta                   # totalCount / pageNo / numOfRows only
#
# Output: JSONL — one row per 입찰공고. Use --meta for the response summary instead.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

bsns="thng" inquiry_div="" from="" to="" rows="100" page="1" bid_no="" instt_cd="" dminstt_cd="" keyword="" meta=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --type)          bsns="$2";        shift 2;;
    --inquiry-div)   inquiry_div="$2"; shift 2;;
    --from)          from="$2";        shift 2;;
    --to)            to="$2";          shift 2;;
    --rows)          rows="$2";        shift 2;;
    --page)          page="$2";        shift 2;;
    --bid-no)        bid_no="$2";      shift 2;;
    --instt-cd)      instt_cd="$2";    shift 2;;
    --dminstt-cd)    dminstt_cd="$2";  shift 2;;
    --keyword)       keyword="$2";     shift 2;;
    --meta)          meta=1;           shift;;
    -h|--help)
      sed -n '2,21p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

require_bin curl jq

# Resolve the operation name + applicable params.
if [[ -n "$keyword" ]]; then
  op="getBidPblancListInfoServcPPSSrch"  # PPS 키워드 검색 — servc only
else
  valid_bsns "$bsns"
  case "$bsns" in
    thng)   op="getBidPblancListInfoThng";;
    servc)  op="getBidPblancListInfoServc";;
    cnstwk) op="getBidPblancListInfoCnstwk";;
    frgcpt) op="getBidPblancListInfoFrgcpt";;
  esac
fi

# Default 7-day window unless explicit --from/--to or --bid-no was given.
if [[ -z "$bid_no" && ( -z "$from" || -z "$to" ) ]]; then
  read from to < <(default_window 7)
fi
[[ -n "$from" ]] && valid_dt12 "$from"
[[ -n "$to"   ]] && valid_dt12 "$to"
[[ -n "$inquiry_div" ]] && valid_inqry_div "$inquiry_div"

# 공고번호 단건 조회는 inqryDiv=3 + bidNtceNo만 보내면 충분 (날짜창 미필요).
declare -a params=( "numOfRows=$rows" "pageNo=$page" )

if [[ -n "$bid_no" ]]; then
  params+=( "inqryDiv=3" "bidNtceNo=$bid_no" )
elif [[ -n "$dminstt_cd" ]]; then
  params+=( "inqryDiv=${inquiry_div:-5}" "dminsttCd=$dminstt_cd" "inqryBgnDt=$from" "inqryEndDt=$to" )
elif [[ -n "$instt_cd" ]]; then
  params+=( "inqryDiv=${inquiry_div:-4}" "ntceInsttCd=$instt_cd" "inqryBgnDt=$from" "inqryEndDt=$to" )
else
  # Default to inqryDiv=1 (등록일시 기준) when only the date window is given.
  params+=( "inqryDiv=${inquiry_div:-1}" "inqryBgnDt=$from" "inqryEndDt=$to" )
fi

[[ -n "$keyword" ]] && params+=( "bidNtceNm=$keyword" )

resp=$(g2b_get "$G2B_BID_BASE" "$op" "${params[@]}")

if (( meta )); then
  echo "$resp" | emit_meta
else
  echo "$resp" | emit_items
fi
