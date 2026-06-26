#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SINGLE="$SCRIPT_DIR/claim-verify.sh"

die() { echo "ERROR: $*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || die "missing dependency: $1"; }

need jq
need sed
need tr

[[ -x "$SINGLE" ]] || die "claim-verify.sh is not executable"

usage() {
  cat <<'EOF'
Claim Verifier batch helper

Usage:
  claim-verify-batch.sh --text-file draft.txt [--max-claims 25] [--out claim_verification_report.json]
  claim-verify-batch.sh --text "Draft text..." [--max-claims 25] [--out claim_verification_report.json]

Notes:
  - This is an MVP orchestrator over claim-verify.sh (single-claim API helper).
  - Claims are extracted by sentence splitting heuristics.
  - Status/confidence are heuristic and conservative in this MVP.
  - This helper does not assign `verified` from search-result counts alone.
EOF
}

text=""
text_file=""
max_claims=25
out_file="claim_verification_report.json"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --text) shift; text="${1:-}" ;;
    --text-file) shift; text_file="${1:-}" ;;
    --max-claims) shift; max_claims="${1:-25}" ;;
    --out) shift; out_file="${1:-claim_verification_report.json}" ;;
    --help|-h) usage; exit 0 ;;
    *) die "unknown arg: $1" ;;
  esac
  shift
done

if [[ -n "$text_file" ]]; then
  [[ -f "$text_file" ]] || die "text file not found: $text_file"
  text="$(cat "$text_file")"
fi

[[ -n "$text" ]] || { usage; die "provide --text or --text-file"; }

# Basic claim extraction heuristic: split by sentence separators, trim, dedupe, keep non-trivial lines.
mapfile -t claims < <(
  echo "$text" \
  | tr '\n' ' ' \
  | sed 's/[!?]/./g' \
  | tr '.' '\n' \
  | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' \
  | awk 'length($0) > 20' \
  | awk '!seen[$0]++' \
  | head -n "$max_claims"
)

timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
tmp_items="$(mktemp)"
echo "[]" > "$tmp_items"

run_failure_code="null"

for claim in "${claims[@]}"; do
  raw=""
  if ! raw="$("$SINGLE" --raw --claim "$claim" 2>/tmp/claim_verify_err.$$)"; then
    err="$(cat /tmp/claim_verify_err.$$ 2>/dev/null || true)"
    status="not_found"
    confidence="0.20"
    evidence='[]'
    notes="single-claim verify failed: ${err:-unknown}"
    failure_code="PRISMFY_UNAVAILABLE"
    run_failure_code='"PRISMFY_UNAVAILABLE"'
  else
    results_count="$(echo "$raw" | jq '.results | length')"
    evidence="$(echo "$raw" | jq '[.results[]?.url] | unique | .[:5]')"
    if [[ "$results_count" -ge 3 ]]; then
      status="weak"; confidence="0.60"; failure_code=""; notes="multiple search hits found; manual source review still required"
    elif [[ "$results_count" -ge 1 ]]; then
      status="weak"; confidence="0.45"; failure_code=""; notes="preliminary evidence found; manual review advised"
    else
      status="not_found"; confidence="0.20"; failure_code="NO_PRIMARY_SOURCE"; notes="no usable evidence found"
    fi
  fi

  if [[ -z "$failure_code" ]]; then
    failure_json="null"
  else
    failure_json="\"$failure_code\""
  fi

  jq --arg claim "$claim" \
     --arg status "$status" \
     --argjson confidence "$confidence" \
     --argjson evidence_urls "$evidence" \
     --argjson failure_code "$failure_json" \
     --arg notes "$notes" \
     '. + [{
       claim: $claim,
       status: $status,
       confidence: $confidence,
       evidence_urls: $evidence_urls,
       failure_code: $failure_code,
       notes: $notes
     }]' "$tmp_items" > "${tmp_items}.new"
  mv "${tmp_items}.new" "$tmp_items"
done

summary="$(jq -r '
  {
    verified: (map(select(.status=="verified"))|length),
    weak: (map(select(.status=="weak"))|length),
    conflicting: (map(select(.status=="conflicting"))|length),
    not_found: (map(select(.status=="not_found"))|length)
  } | "verified=\(.verified), weak=\(.weak), conflicting=\(.conflicting), not_found=\(.not_found)"
' "$tmp_items")"

jq -n \
  --arg timestamp_utc "$timestamp" \
  --arg skill_version "1.0.0" \
  --arg summary "$summary" \
  --argjson run_failure_code "$run_failure_code" \
  --argjson items "$(cat "$tmp_items")" \
  '{
    timestamp_utc: $timestamp_utc,
    skill_version: $skill_version,
    summary: $summary,
    run_failure_code: $run_failure_code,
    items: $items
  }' > "$out_file"

rm -f "$tmp_items" /tmp/claim_verify_err.$$
echo "Wrote $out_file"
