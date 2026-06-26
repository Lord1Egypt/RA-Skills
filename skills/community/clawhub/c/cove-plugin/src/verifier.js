#!/usr/bin/env node
/**
 * CoVe CLI — Chain of Verification command-line interface.
 *
 * Usage:
 *   cove-verify --response "text to verify" [--policy basic|standard|deep] [--strict] [--format text|json]
 *   echo "text" | cove-verify --stdin [--policy standard]
 *
 * Environment variables (direct API — no sidecar required):
 *   GEMINI_API_KEY       — Use Gemini directly (auto-detects provider)
 *   ANTHROPIC_API_KEY    — Use Claude directly (auto-detects provider)
 *   OPENAI_API_KEY       — Use OpenAI directly (auto-detects provider)
 *   COVE_LLM_PROVIDER    — Explicit provider override: gemini | anthropic | openai
 *   COVE_LLM_API_KEY     — Explicit API key (overrides provider-specific vars)
 *
 * Environment variables (sidecar mode):
 *   OPENCLAW_PROXY_PORT  — Sidecar proxy port (default: 8888)
 *   SIDECAR_PROXY_KEY    — Proxy auth key (if required)
 *
 * Common:
 *   COVE_MODEL           — Model to use for verification (default: gemini-2.0-flash)
 *   BRAVE_API_KEY        — Brave Search API key (for standard/deep policies)
 */

const { verifyResponse } = require('./verify_claims');

// ── Parse CLI args ──
const args = process.argv.slice(2);

function getArg(name, short) {
  for (let i = 0; i < args.length; i++) {
    if (args[i] === `--${name}` || (short && args[i] === `-${short}`)) {
      return args[i + 1] || '';
    }
  }
  return null;
}
const hasFlag = (name) => args.includes(`--${name}`);

if (hasFlag('help') || hasFlag('h')) {
  console.log(`
CoVe — Chain of Verification for OpenClaw

Usage:
  cove-verify -r "response text" [options]
  echo "response text" | cove-verify --stdin [options]

Options:
  -r, --response   Response text to verify (required unless --stdin)
  --stdin          Read response from stdin
  -p, --policy     Verification policy: basic, standard, deep (default: basic)
  --strict         Exit with error if any claim is unverifiable
  -f, --format     Output format: text, json (default: text)
  --no-correct     Report inaccuracies without auto-correcting
  --help           Show this help message

Policies:
  basic      Check against memory and workspace files
  standard   Also search the web (requires Brave API key)
  deep       Multi-step reasoning with web search and confidence scoring

Environment (direct API — no sidecar required):
  GEMINI_API_KEY        Use Gemini directly (auto-detects provider)
  ANTHROPIC_API_KEY     Use Claude directly (auto-detects provider)
  OPENAI_API_KEY        Use OpenAI directly (auto-detects provider)
  COVE_LLM_PROVIDER     Explicit provider: gemini | anthropic | openai
  COVE_LLM_API_KEY      Explicit API key (overrides provider-specific vars)

Environment (sidecar mode — used when no API key is set):
  OPENCLAW_PROXY_PORT   Sidecar port (default: 8888)
  SIDECAR_PROXY_KEY     Proxy auth key

Common:
  COVE_MODEL            LLM model for verification
  BRAVE_API_KEY         Brave Search API key
`);
  process.exit(0);
}

const policy = getArg('policy', 'p') || 'basic';
const format = getArg('format', 'f') || 'text';
const strict = hasFlag('strict');
const noCorrect = hasFlag('no-correct');
const useStdin = hasFlag('stdin');

async function main() {
  let responseText = getArg('response', 'r');

  // Read from stdin if requested
  if (useStdin || (!responseText && !process.stdin.isTTY)) {
    responseText = await new Promise((resolve) => {
      let data = '';
      process.stdin.setEncoding('utf8');
      process.stdin.on('data', (chunk) => { data += chunk; });
      process.stdin.on('end', () => resolve(data.trim()));
    });
  }

  if (!responseText) {
    console.error('Error: No response text provided. Use -r "text" or --stdin.');
    process.exit(1);
  }

  const overrides = {
    policy,
    auto_correct: !noCorrect,
  };

  const report = await verifyResponse(responseText, overrides);

  if (format === 'json') {
    console.log(JSON.stringify(report, null, 2));
  } else {
    printTextReport(report, strict);
  }

  // Exit code: 1 if inaccuracies found, 2 if strict + unverifiable
  if (report.summary.inaccurate > 0) process.exit(1);
  if (strict && report.summary.unverifiable > 0) process.exit(2);
  process.exit(0);
}

function printTextReport(report, strict) {
  console.log('');
  console.log('═══ CoVe — Chain of Verification Report ═══');
  console.log('');

  if (report.claims.length === 0) {
    console.log('✅ No specific factual claims found to verify.');
    console.log('');
    return;
  }

  for (const c of report.claims) {
    if (c.status === 'verified') {
      console.log(`  ✅ VERIFIED: "${c.claim}"`);
      if (c.source) console.log(`     Source: ${c.source}`);
    } else if (c.status === 'inaccurate') {
      console.log(`  ❌ INACCURATE: "${c.claim}"`);
      if (c.source) console.log(`     Source: ${c.source}`);
      if (c.correction) console.log(`     Correction: ${c.correction}`);
    } else {
      console.log(`  ❓ UNVERIFIABLE: "${c.claim}"`);
      if (c.evidence) console.log(`     Note: ${c.evidence}`);
    }
    console.log('');
  }

  console.log('───────────────────────────────────────────');
  console.log(`  Claims: ${report.summary.total} total`);
  console.log(`  ✅ ${report.summary.verified} verified  ❌ ${report.summary.inaccurate} inaccurate  ❓ ${report.summary.unverifiable} unverifiable`);
  console.log(`  Duration: ${report.durationMs}ms`);
  console.log('');

  if (report.correctedResponse) {
    console.log('═══ Corrected Response ═══');
    console.log('');
    console.log(report.correctedResponse);
    console.log('');
  } else if (report.summary.inaccurate === 0) {
    console.log('  ✅ Response is accurate.');
  }
  console.log('');
}

main().catch((err) => {
  console.error(`CoVe error: ${err.message}`);
  process.exit(1);
});
