#!/usr/bin/env bash
# awardee-kyb-pipeline.sh — pull last-week awarded contracts and KYB each awardee.
#
# Output: JSONL — {bidNtceNo, sucsfbidAmt, bizrno, corpNm, taxType, businessStatus}
#
# Requires both g2b-cli and nts-bizno-cli installed in your skills dir.
# Set NTS_BIZNO_SERVICE_KEY to enable the second hop; without it, this script
# will only emit g2b columns and skip the KYB join.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NTS_BIZNO="${NTS_BIZNO:-$(cd "$here/../nts-bizno-cli/scripts" && pwd)/status.sh}"

# Last 7 days, 500 rows. Bump --rows / paginate for higher-volume weeks.
read FROM TO < <("$here"/scripts/bid.sh --help >/dev/null 2>&1; \
  if date -v -7d +%Y%m%d >/dev/null 2>&1; then
    echo "$(date -v -7d +%Y%m%d)0000 $(date +%Y%m%d%H%M)";
  else
    echo "$(date -u -d '-7 days' +%Y%m%d)0000 $(date -u +%Y%m%d%H%M)";
  fi)

awarded=$(mktemp)
"$here"/scripts/std.sh --what awarded --from "$FROM" --to "$TO" --rows 500 > "$awarded"

if [[ ! -x "$NTS_BIZNO" ]] || [[ -z "${NTS_BIZNO_SERVICE_KEY:-}" ]]; then
  echo "warning: nts-bizno-cli or NTS_BIZNO_SERVICE_KEY not configured — emitting g2b-only rows." >&2
  jq -c '{bidNtceNo, sucsfbidAmt, bizrno, corpNm}' "$awarded"
  rm -f "$awarded"
  exit 0
fi

# Group by bizrno to avoid duplicate KYB calls.
declare -A status_cache
while IFS= read -r row; do
  brn=$(jq -r '.bizrno // empty' <<<"$row")
  [[ -z "$brn" ]] && { jq -c '{bidNtceNo, sucsfbidAmt, bizrno, corpNm, taxType: null, businessStatus: null}' <<<"$row"; continue; }

  if [[ -z "${status_cache[$brn]:-}" ]]; then
    s=$("$NTS_BIZNO" --b-no "$brn" 2>/dev/null \
        | jq -c '{taxType: .tax_type, businessStatus: .b_stt}' || echo '{"taxType":null,"businessStatus":null}')
    status_cache[$brn]="$s"
  fi

  jq -c --argjson s "${status_cache[$brn]}" '{bidNtceNo, sucsfbidAmt, bizrno, corpNm} + $s' <<<"$row"
done < "$awarded"

rm -f "$awarded"
