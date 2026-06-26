#!/usr/bin/env node
'use strict';

// recall-verify-report — aggregate kind=recall_verify events from the
// memory graph jsonl into a Markdown table. Exit 0 = ship gate green
// (every asset_type has success_rate >= 0.95 and 0 mismatches), exit 2
// otherwise. Designed to be scripted into deploy.sh as a pre-publish gate.
//
// Usage:
//   node scripts/recall-verify-report.js              # all events
//   node scripts/recall-verify-report.js --since 1h   # last hour
//   node scripts/recall-verify-report.js --since 30m
//   node scripts/recall-verify-report.js --since 2026-05-16T10:00:00Z
//   node scripts/recall-verify-report.js --json       # raw JSON for piping

const { tryReadMemoryGraphEvents } = require('../src/gep/memoryGraph');

const SUCCESS_THRESHOLD = 0.95;

function parseSince(value) {
  if (!value) return null;
  // Try relative duration first (1h / 30m / 2d / 45s) — unambiguous.
  const m = String(value).match(/^(\d+)\s*(s|m|h|d)$/i);
  if (m) {
    const n = Number(m[1]);
    const unit = m[2].toLowerCase();
    const factor = unit === 's' ? 1000 : unit === 'm' ? 60000 : unit === 'h' ? 3600000 : 86400000;
    return Date.now() - (n * factor);
  }
  // Then ISO-8601. Require '-' or 'T' so we don't accept loose numeric
  // strings like "5" → year 2001.
  if (/[-T]/.test(String(value))) {
    const iso = Date.parse(value);
    if (!Number.isNaN(iso)) return iso;
  }
  return undefined;
}

function parseArgs(argv) {
  const args = { since: null, json: false };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--json') args.json = true;
    else if (a === '--since') {
      args.since = argv[++i];
    } else if (a.startsWith('--since=')) {
      args.since = a.slice('--since='.length);
    } else if (a === '--help' || a === '-h') {
      args.help = true;
    }
  }
  return args;
}

function percentile(sorted, p) {
  if (!sorted.length) return 0;
  const idx = Math.min(sorted.length - 1, Math.floor(sorted.length * p));
  return sorted[idx];
}

function aggregate(events) {
  const byType = new Map();
  for (const ev of events) {
    if (!ev || ev.kind !== 'recall_verify') continue;
    const type = (ev.asset && ev.asset.type) || 'Unknown';
    if (!byType.has(type)) {
      byType.set(type, {
        type,
        total: 0,
        ok: 0,
        missing: 0,
        mismatch: 0,
        skipped: 0,
        latencies: [],
        ages: [],
      });
    }
    const bucket = byType.get(type);
    bucket.total += 1;
    const v = ev.verification || {};
    if (v.outcome === 'roundtrip_ok') bucket.ok += 1;
    else if (v.outcome === 'roundtrip_missing') bucket.missing += 1;
    else if (v.outcome === 'roundtrip_mismatch') bucket.mismatch += 1;
    else bucket.skipped += 1;
    if (Number.isFinite(v.latency_ms)) bucket.latencies.push(v.latency_ms);
    if (Number.isFinite(v.age_at_verify_ms)) bucket.ages.push(v.age_at_verify_ms);
  }
  const rows = [];
  for (const bucket of byType.values()) {
    const denom = bucket.ok + bucket.missing + bucket.mismatch;
    bucket.success_rate = denom > 0 ? bucket.ok / denom : 0;
    bucket.latencies.sort(function (a, b) { return a - b; });
    bucket.ages.sort(function (a, b) { return a - b; });
    bucket.p50_latency_ms = percentile(bucket.latencies, 0.5);
    bucket.p95_latency_ms = percentile(bucket.latencies, 0.95);
    bucket.p99_latency_ms = percentile(bucket.latencies, 0.99);
    bucket.p50_age_ms = percentile(bucket.ages, 0.5);
    bucket.p95_age_ms = percentile(bucket.ages, 0.95);
    bucket.p99_age_ms = percentile(bucket.ages, 0.99);
    delete bucket.latencies;
    delete bucket.ages;
    rows.push(bucket);
  }
  rows.sort(function (a, b) { return a.type.localeCompare(b.type); });

  const totals = { type: 'TOTAL', total: 0, ok: 0, missing: 0, mismatch: 0, skipped: 0 };
  for (const r of rows) {
    totals.total += r.total;
    totals.ok += r.ok;
    totals.missing += r.missing;
    totals.mismatch += r.mismatch;
    totals.skipped += r.skipped;
  }
  const totalsDenom = totals.ok + totals.missing + totals.mismatch;
  totals.success_rate = totalsDenom > 0 ? totals.ok / totalsDenom : 0;

  // Gate severity is monotonic: once a row triggers a worse state, later
  // rows cannot downgrade it. Without this, AntiPattern@0% (RED) followed
  // by Capsule@90% (YELLOW) would report YELLOW — misleading dashboards
  // even though the exit code still reflects RED. (Bugbot review on PR #53.)
  // RANK is the comparison ordinal: GREEN(0) < YELLOW(1) < RED(2).
  const RANK = { GREEN: 0, YELLOW: 1, RED: 2 };
  function escalate(current, candidate) {
    return RANK[candidate] > RANK[current] ? candidate : current;
  }
  let gate = 'GREEN';
  if (rows.length === 0) gate = 'RED';
  else {
    for (const r of rows) {
      if (r.mismatch > 0) { gate = 'RED'; break; }
      if (r.success_rate < SUCCESS_THRESHOLD) {
        gate = escalate(gate, r.success_rate >= 0.85 ? 'YELLOW' : 'RED');
      }
    }
  }
  return { rows, totals, gate };
}

function fmtPct(rate) {
  return (rate * 100).toFixed(1) + '%';
}

function fmtMs(n) {
  if (!Number.isFinite(n) || n === 0) return '—';
  if (n < 1000) return Math.round(n) + 'ms';
  return (n / 1000).toFixed(1) + 's';
}

function printMarkdown(result, since) {
  const sinceStr = since ? new Date(since).toISOString() : 'all time';
  console.log('# RecallVerify Report (since ' + sinceStr + ')');
  console.log('');
  if (result.rows.length === 0) {
    console.log('_No `recall_verify` events found in memory graph._');
    console.log('');
    console.log('Ship gate: **RED** (no data — feature may be disabled or daemon has not run a publish cycle yet)');
    return;
  }
  console.log('| asset_type   | total | ok  | missing | mismatch | skipped | success_rate | p50_latency | p99_latency | p50_age | p99_age |');
  console.log('|--------------|------:|----:|--------:|---------:|--------:|-------------:|------------:|------------:|--------:|--------:|');
  for (const r of result.rows) {
    console.log('| ' + r.type.padEnd(12) +
      ' | ' + String(r.total).padStart(5) +
      ' | ' + String(r.ok).padStart(3) +
      ' | ' + String(r.missing).padStart(7) +
      ' | ' + String(r.mismatch).padStart(8) +
      ' | ' + String(r.skipped).padStart(7) +
      ' | ' + fmtPct(r.success_rate).padStart(12) +
      ' | ' + fmtMs(r.p50_latency_ms).padStart(11) +
      ' | ' + fmtMs(r.p99_latency_ms).padStart(11) +
      ' | ' + fmtMs(r.p50_age_ms).padStart(7) +
      ' | ' + fmtMs(r.p99_age_ms).padStart(7) +
      ' |');
  }
  const t = result.totals;
  console.log('| ' + 'TOTAL'.padEnd(12) +
    ' | ' + String(t.total).padStart(5) +
    ' | ' + String(t.ok).padStart(3) +
    ' | ' + String(t.missing).padStart(7) +
    ' | ' + String(t.mismatch).padStart(8) +
    ' | ' + String(t.skipped).padStart(7) +
    ' | ' + fmtPct(t.success_rate).padStart(12) +
    ' | ' + '—'.padStart(11) +
    ' | ' + '—'.padStart(11) +
    ' | ' + '—'.padStart(7) +
    ' | ' + '—'.padStart(7) +
    ' |');
  console.log('');
  console.log('Ship gate: **' + result.gate + '**' + (result.gate === 'GREEN' ? ' (exit 0)' : ' (exit 2)'));
}

function main() {
  const args = parseArgs(process.argv);
  if (args.help) {
    console.log('Usage: node scripts/recall-verify-report.js [--since <Nh|Nm|Nd|ISO>] [--json]');
    process.exit(0);
  }

  let sinceMs = null;
  if (args.since) {
    const parsed = parseSince(args.since);
    if (parsed === undefined) {
      console.error('Error: --since must be ISO-8601 or a duration like 1h / 30m / 2d (got: ' + args.since + ')');
      process.exit(1);
    }
    sinceMs = parsed;
  }

  const allEvents = tryReadMemoryGraphEvents(20000);
  const filtered = allEvents.filter(function (ev) {
    if (!ev || ev.kind !== 'recall_verify') return false;
    if (sinceMs != null && Number.isFinite(ev.ts) && ev.ts < sinceMs) return false;
    return true;
  });

  const result = aggregate(filtered);

  if (args.json) {
    console.log(JSON.stringify({
      since: sinceMs ? new Date(sinceMs).toISOString() : null,
      ...result,
    }, null, 2));
  } else {
    printMarkdown(result, sinceMs);
  }

  process.exit(result.gate === 'GREEN' ? 0 : 2);
}

if (require.main === module) {
  main();
}

module.exports = { aggregate, parseSince, parseArgs };
