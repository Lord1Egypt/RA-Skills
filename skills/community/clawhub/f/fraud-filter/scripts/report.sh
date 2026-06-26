#!/usr/bin/env bash
# report.sh — Queue an anonymous report for an endpoint.
#
# Usage:
#   report.sh <url> <outcome> [amount_usd] [--skill <skill_name>] [--reason <text>]
#
# Outcomes: success, post_payment_failure, pre_payment_failure
#
# Examples:
#   report.sh https://api.example.com/data post_payment_failure 0.05 --reason "Needed AAPL price. Got HTTP 200 with empty data array."
#   report.sh https://api.example.com/data post_payment_failure 0.05 --skill stock-research --reason "Paid for structured stock data. Received garbled JSON."
#   report.sh https://api.example.com/data success 0.03 --reason "Needed current AAPL price. Advertised real-time quotes. Got price, volume, and 52-week range in clean JSON."

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVER_DIR="$SCRIPT_DIR/../server"

if [ $# -lt 2 ]; then
  echo "Usage: report.sh <endpoint-url> <outcome> [amount_usd] [--skill <skill_name>]" >&2
  echo "Outcomes: success, post_payment_failure, pre_payment_failure" >&2
  exit 1
fi

URL="$1"
OUTCOME="$2"
AMOUNT="${3:-0}"
SKILL=""
REASON=""

shift 3 2>/dev/null || shift $#
while [ $# -gt 0 ]; do
  case "$1" in
    --skill) SKILL="$2"; shift 2 ;;
    --reason) REASON="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

node --input-type=module -e "
  import { queueReport } from '${SERVER_DIR}/reporter.js';

  const url      = process.argv[1];
  const outcome  = process.argv[2];
  const amount   = process.argv[3];
  const skill    = process.argv[4] || null;
  const reason   = process.argv[5] || null;

  const validOutcomes = ['success', 'post_payment_failure', 'pre_payment_failure'];
  if (!validOutcomes.includes(outcome)) {
    console.error('Invalid outcome: ' + outcome);
    console.error('Valid outcomes: ' + validOutcomes.join(', '));
    process.exit(1);
  }

  const result = queueReport({ endpoint_url: url, outcome, amount_usd: amount, skill_name: skill, reason });
  console.log(JSON.stringify(result, null, 2));
" "$URL" "$OUTCOME" "$AMOUNT" "$SKILL" "$REASON"
