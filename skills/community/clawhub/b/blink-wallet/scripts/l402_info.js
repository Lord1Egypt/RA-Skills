#!/usr/bin/env node
/**
 * Blink Wallet — L402 Service Info
 *
 * Usage:
 *   node l402_info.js <service_id> [options]
 *
 * Get full details for an L402 service from l402.directory.
 * Optionally fetch a paid health report (10 sats via L402).
 *
 * Arguments:
 *   service_id      - Required. Service ID from l402.directory (hex string).
 *   --report        - Optional. Fetch paid health report (10 sats, L402-gated).
 *
 * The --report flag triggers an L402 payment. It is subject to the budget
 * controls and the domain allowlist (domain: l402.directory), both of which
 * must be configured or the payment is refused. --force only forces a fresh
 * payment instead of reusing a cached token; it never bypasses either control.
 *
 * No API key required for the free detail endpoint.
 * Write scope required for --report (L402 payment).
 *
 * Output: JSON to stdout. Status messages to stderr.
 * Dependencies: None (Node.js 22+ built-in fetch).
 */

'use strict';

const { strictParseArgs } = require('./_blink_client');

// ── URLs ─────────────────────────────────────────────────────────────────────

const DIRECTORY_BASE = 'https://l402.directory/api';

// ── Arg parsing ──────────────────────────────────────────────────────────────

// Every option this script accepts (strict; exported for the CLI-forwarding guard).
const ARG_OPTIONS = {
  report: { type: 'boolean', default: false },
  force: { type: 'boolean', default: false },
  help: { type: 'boolean', short: 'h', default: false },
};

function parseCliArgs(argv) {
  // Strict (PR #28 review): conflicting repeats and extra positionals are
  // refused, and errors never echo argument values.
  const { values, positionals } = strictParseArgs(argv, ARG_OPTIONS, { positionals: [0, 1] });

  if (values.help) {
    console.error(
      [
        'Usage: blink l402-info <service_id> [--report] [--force]',
        '',
        'Options:',
        '  --report   Fetch paid health report (10 sats via L402)',
        '  --force    Pay fresh instead of reusing a cached token (never bypasses',
        '             the budget or domain allowlist)',
        '  --help     Show this help',
      ].join('\n'),
    );
    process.exit(0);
  }

  const serviceId = positionals[0];
  if (!serviceId) {
    throw new Error('Missing required argument: service_id. Run with --help for usage.');
  }

  return {
    serviceId,
    report: values.report,
    force: values.force,
  };
}

// ── Free detail endpoint ─────────────────────────────────────────────────────

async function fetchServiceDetail(serviceId) {
  const url = `${DIRECTORY_BASE}/services/${serviceId}`;
  console.error(`Fetching service detail from l402.directory...`);

  const res = await fetch(url, {
    headers: { Accept: 'application/json' },
    signal: AbortSignal.timeout(15_000),
  });

  if (res.status === 404) {
    throw new Error(`Service not found: ${serviceId}`);
  }
  if (!res.ok) {
    throw new Error(`l402.directory returned HTTP ${res.status}`);
  }

  return res.json();
}

// ── Paid report endpoint (L402) ──────────────────────────────────────────────

async function fetchServiceReport(serviceId, { force }) {
  // Delegate to l402-pay for the L402 payment flow. Budget and domain
  // enforcement is handled inside l402_pay (fail closed at the point of
  // payment) — no duplicate pre-checks here.
  const reportUrl = `${DIRECTORY_BASE}/report/${serviceId}`;

  // Use l402_pay's main logic by setting up argv and calling it
  const origArgv = process.argv;
  process.argv = ['node', 'blink', reportUrl];
  if (force) process.argv.push('--force');

  try {
    const { main: l402PayMain } = require('./l402_pay');
    await l402PayMain();
  } finally {
    process.argv = origArgv;
  }
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const args = parseCliArgs(process.argv.slice(2));

  if (args.report) {
    await fetchServiceReport(args.serviceId, { force: args.force });
  } else {
    const detail = await fetchServiceDetail(args.serviceId);
    console.log(JSON.stringify(detail, null, 2));
  }
}

if (require.main === module) {
  main()
    .then(async () => {
      // --report delegates to l402_pay, which may load the Spark SDK (open
      // event-loop handles) and reports failures via process.exitCode, not a
      // hard exit. Drain stdout, then exit with that code — the same tail as
      // l402_pay's own direct entrypoint (PR #25 review).
      await new Promise((resolve) => {
        if (process.stdout.writableLength === 0) return resolve();
        process.stdout.write('', () => resolve());
      });
      process.exit(process.exitCode || 0);
    })
    .catch((e) => {
      console.error('Error:', e.message);
      process.exit(1);
    });
}

module.exports = { main, parseCliArgs, fetchServiceDetail, DIRECTORY_BASE, ARG_OPTIONS };
