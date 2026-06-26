#!/usr/bin/env bash
# after-payment.sh — PostToolUse hook for fraud-filter.
#
# Evaluates payment tool responses and auto-reports post_payment_failure
# when the response is empty, null, or contains an obvious error.
# Reads tool result JSON from stdin (OpenClaw hook protocol).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVER_DIR="$SCRIPT_DIR/../server"

INPUT="$(cat)"

node --input-type=module -e "
import { queueReport } from '${SERVER_DIR}/reporter.js';

const PAYMENT_PATTERNS = [
  /pay/i, /purchase/i, /checkout/i, /buy/i, /wallet/i,
  /v402/i, /x402/i, /clawrouter/i, /stripe/i, /paypal/i,
  /payment[_-]?skill/i,
];

function isGarbage(response) {
  if (response === null || response === undefined) return true;
  const str = typeof response === 'string' ? response.trim() : JSON.stringify(response);
  if (!str || str === 'null' || str === '{}' || str === '[]' || str === '\"\"') return true;
  if (typeof response === 'object' && (response.error || response.Error)) return true;
  return false;
}

try {
  const call = JSON.parse(process.argv[1]);
  const toolName    = call.tool_name     || '';
  const toolInput   = JSON.stringify(call.tool_input || {});
  const toolResponse = call.tool_response;

  if (!PAYMENT_PATTERNS.some(p => p.test(toolName))) process.exit(0);

  const urlMatch = toolInput.match(/https?:\/\/[^\s\"\\\\]+/);
  if (!urlMatch) process.exit(0);

  const url = urlMatch[0];

  if (isGarbage(toolResponse)) {
    const result = queueReport({
      endpoint_url: url,
      outcome:      'post_payment_failure',
      amount_usd:   '0',
      reason:       'Payment tool returned empty or error response. Tool: ' + toolName,
    });
    if (result.queued) {
      const hostname = new URL(url).hostname;
      console.log('fraud-filter: auto-reported post_payment_failure for ' + hostname + ' (empty/error response).');
    }
  }

  process.exit(0);
} catch {
  process.exit(0);
}
" "$INPUT" 2>/dev/null || exit 0
