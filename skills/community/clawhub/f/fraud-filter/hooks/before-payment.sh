#!/usr/bin/env bash
# before-payment.sh — PreToolUse hook for fraud-filter.
#
# Intercepts payment tool calls and checks the endpoint before allowing.
# Reads tool call JSON from stdin (OpenClaw hook protocol).
# Exit 0: allow  |  Exit 2: block (stdout message shown to agent)
#
# Config (via dashboard or API):
#   on_block:   "block" (default) | "warn"
#   on_caution: "warn"  (default) | "block" | "allow"

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVER_DIR="$SCRIPT_DIR/../server"

INPUT="$(cat)"

node --input-type=module -e "
import { checkEndpoint, loadConfig } from '${SERVER_DIR}/trust-db.js';

const PAYMENT_PATTERNS = [
  /pay/i, /purchase/i, /checkout/i, /buy/i, /wallet/i,
  /v402/i, /x402/i, /clawrouter/i, /stripe/i, /paypal/i,
  /payment[_-]?skill/i,
];

try {
  const call = JSON.parse(process.argv[1]);
  const toolName = call.tool_name || '';
  const toolInput = JSON.stringify(call.tool_input || {});

  // Only act on payment-looking tool calls
  if (!PAYMENT_PATTERNS.some(p => p.test(toolName))) process.exit(0);

  // Extract endpoint URL from tool arguments
  const urlMatch = toolInput.match(/https?:\/\/[^\s\"\\\\]+/);
  if (!urlMatch) process.exit(0);

  const url = urlMatch[0];
  const assessment = checkEndpoint(url);
  const config = loadConfig();

  const onBlock   = config.on_block   || 'block';
  const onCaution = config.on_caution || 'warn';

  if (assessment.recommendation === 'block') {
    const reason = assessment.hotlisted ? 'hotlisted' : 'satisfaction score: ' + assessment.score;
    if (onBlock === 'block') {
      console.log('fraud-filter: blocked payment to ' + url + ' (' + reason + ')');
      process.exit(2);
    }
    console.log('fraud-filter: warning — ' + url + ' has block recommendation (' + reason + '). Proceeding per settings.');

  } else if (assessment.recommendation === 'caution') {
    if (onCaution === 'block') {
      console.log('fraud-filter: blocked payment to ' + url + ' (caution, score: ' + assessment.score + ')');
      process.exit(2);
    } else if (onCaution === 'warn') {
      console.log('fraud-filter: caution — ' + url + ' (score: ' + assessment.score + '). Proceeding.');
    }
  }

  process.exit(0);
} catch {
  process.exit(0); // fail open — never block due to an internal error
}
" "$INPUT" 2>/dev/null || exit 0
