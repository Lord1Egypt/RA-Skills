#!/usr/bin/env bash
# ai-rfp-digest.sh — daily AI-related 용역 RFP digest.
# Pipe the output into Slack, email, or a tistory/velog post.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

today=$(date +%Y-%m-%d)
out=$(mktemp)

# Pull AI-keyworded 용역 RFPs from the last 24h.
"$here"/scripts/bid.sh --keyword "인공지능" --rows 100 \
  | jq -c "select(.bidNtceDt >= \"$today\")" \
  > "$out"

count=$(wc -l < "$out" | tr -d ' ')

cat <<EOF
# 🤖 AI 입찰 다이제스트 — $today

총 ${count}건의 인공지능 관련 신규 입찰공고가 게시되었습니다.

EOF

jq -r '"## \(.bidNtceNm)\n\n- 공고번호: \(.bidNtceNo)\n- 공고기관: \(.ntceInsttNm)\n- 수요기관: \(.dminsttNm)\n- 추정가격: ₩\(.presmptPrce)\n- 입찰개시: \(.bidBeginDt)\n- 개찰일시: \(.opengDt)\n"' "$out"

rm -f "$out"
