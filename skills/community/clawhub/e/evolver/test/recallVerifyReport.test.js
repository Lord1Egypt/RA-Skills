'use strict';

// recall-verify-report tests — pure aggregation + parser logic + exit codes.

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execSync } = require('node:child_process');

const { aggregate, parseSince, parseArgs } = require('../scripts/recall-verify-report');

describe('recall-verify-report.parseSince', () => {
  it('parses Nh / Nm / Nd duration', () => {
    const now = Date.now();
    const oneH = parseSince('1h');
    assert.ok(oneH < now && now - oneH < 3700000);
    const tenM = parseSince('10m');
    assert.ok(tenM < now && now - tenM < 700000);
    const twoD = parseSince('2d');
    assert.ok(now - twoD > 86400000);
  });
  it('parses ISO-8601', () => {
    const ts = parseSince('2026-05-16T00:00:00Z');
    assert.equal(ts, Date.parse('2026-05-16T00:00:00Z'));
  });
  it('returns undefined sentinel for ambiguous numeric / invalid input', () => {
    assert.equal(parseSince('xyz'), undefined);
    assert.equal(parseSince('5'), undefined);
  });
});

describe('recall-verify-report.parseArgs', () => {
  it('parses --since, --json, --since=<value>', () => {
    assert.deepEqual(parseArgs(['n', 's']), { since: null, json: false });
    assert.deepEqual(parseArgs(['n', 's', '--json']), { since: null, json: true });
    assert.deepEqual(parseArgs(['n', 's', '--since', '1h']), { since: '1h', json: false });
    assert.deepEqual(parseArgs(['n', 's', '--since=30m', '--json']), { since: '30m', json: true });
  });
});

describe('recall-verify-report.aggregate', () => {
  it('returns RED gate when no events', () => {
    const r = aggregate([]);
    assert.equal(r.gate, 'RED');
    assert.equal(r.rows.length, 0);
  });

  it('aggregates per-type counts and excludes skipped from success_rate', () => {
    const events = [
      mkEvent('Capsule', 'roundtrip_ok', 100, 5000),
      mkEvent('Capsule', 'roundtrip_ok', 200, 6000),
      mkEvent('Capsule', 'roundtrip_missing', 300, 65000),
      mkEvent('Capsule', 'verification_skipped', 0, 0, 'sample_rate'),
      mkEvent('SkillBundle', 'roundtrip_ok', 150, 4000),
    ];
    const r = aggregate(events);
    assert.equal(r.rows.length, 2);
    const cap = r.rows.find(function (x) { return x.type === 'Capsule'; });
    assert.equal(cap.total, 4);
    assert.equal(cap.ok, 2);
    assert.equal(cap.missing, 1);
    assert.equal(cap.skipped, 1);
    assert.ok(Math.abs(cap.success_rate - 2/3) < 0.001);
    const sb = r.rows.find(function (x) { return x.type === 'SkillBundle'; });
    assert.equal(sb.success_rate, 1.0);
  });

  it('sets gate=RED when any mismatch present', () => {
    const events = [
      mkEvent('Capsule', 'roundtrip_ok', 100, 5000),
      mkEvent('Capsule', 'roundtrip_mismatch', 200, 6000),
    ];
    const r = aggregate(events);
    assert.equal(r.gate, 'RED');
  });

  it('sets gate=RED when success_rate < 0.85', () => {
    const events = [
      mkEvent('Capsule', 'roundtrip_ok', 100, 5000),
      mkEvent('Capsule', 'roundtrip_missing', 200, 6000),
      mkEvent('Capsule', 'roundtrip_missing', 300, 7000),
      mkEvent('Capsule', 'roundtrip_missing', 400, 8000),
    ];
    const r = aggregate(events);
    assert.equal(r.gate, 'RED');
  });

  it('sets gate=YELLOW when 0.85 <= success_rate < 0.95', () => {
    const events = [];
    for (let i = 0; i < 9; i++) events.push(mkEvent('Capsule', 'roundtrip_ok', 100, 5000));
    events.push(mkEvent('Capsule', 'roundtrip_missing', 100, 5000));
    const r = aggregate(events);
    assert.equal(r.gate, 'YELLOW');
  });

  it('sets gate=GREEN when all rows >= 0.95 and 0 mismatches', () => {
    const events = [];
    for (let i = 0; i < 20; i++) events.push(mkEvent('Capsule', 'roundtrip_ok', 100, 5000));
    events.push(mkEvent('Capsule', 'roundtrip_missing', 100, 5000));
    const r = aggregate(events);
    assert.equal(r.gate, 'GREEN');
  });

  // Bugbot review on PR #53 caught this: gate must escalate monotonically.
  // Before the fix, iterating 'AntiPattern@0%' (RED) then 'Capsule@90%'
  // (YELLOW) would overwrite gate to YELLOW. Operators / dashboards saw
  // YELLOW even though the exit code reflected RED.
  it('does NOT downgrade gate from RED to YELLOW across rows', () => {
    const events = [];
    // AntiPattern with 0% success → RED on its own
    for (let i = 0; i < 10; i++) events.push(mkEvent('AntiPattern', 'roundtrip_missing', 100, 5000));
    // Capsule with 90% success → would be YELLOW on its own
    for (let i = 0; i < 9; i++) events.push(mkEvent('Capsule', 'roundtrip_ok', 100, 5000));
    events.push(mkEvent('Capsule', 'roundtrip_missing', 100, 5000));
    const r = aggregate(events);
    assert.equal(r.gate, 'RED', 'AntiPattern RED must not be downgraded by Capsule YELLOW');
  });

  it('does NOT downgrade gate from YELLOW to GREEN across rows', () => {
    const events = [];
    // Capsule@90% → YELLOW
    for (let i = 0; i < 9; i++) events.push(mkEvent('Capsule', 'roundtrip_ok', 100, 5000));
    events.push(mkEvent('Capsule', 'roundtrip_missing', 100, 5000));
    // Gene@100% → GREEN on its own (would clobber YELLOW pre-fix? actually
    // pre-fix logic only updated when success_rate < threshold, so a 100%
    // row didn't downgrade. Test guards against future regressions where
    // someone adds a "GREEN-on-good-row" branch.)
    for (let i = 0; i < 10; i++) events.push(mkEvent('Gene', 'roundtrip_ok', 100, 5000));
    const r = aggregate(events);
    assert.equal(r.gate, 'YELLOW');
  });

  it('mismatch in any row trumps later rows (RED is sticky)', () => {
    const events = [];
    // First a Capsule mismatch → RED
    events.push(mkEvent('Capsule', 'roundtrip_mismatch', 100, 5000));
    // Then a perfect Gene row that should NOT downgrade
    for (let i = 0; i < 20; i++) events.push(mkEvent('Gene', 'roundtrip_ok', 100, 5000));
    const r = aggregate(events);
    assert.equal(r.gate, 'RED');
  });

  it('computes p50/p95/p99 latency from sorted samples', () => {
    const events = [];
    for (let i = 1; i <= 100; i++) {
      events.push(mkEvent('Capsule', 'roundtrip_ok', i * 10, i * 100));
    }
    const r = aggregate(events);
    const cap = r.rows[0];
    assert.ok(cap.p50_latency_ms >= 500 && cap.p50_latency_ms <= 520);
    assert.ok(cap.p99_latency_ms >= 990);
  });
});

describe('recall-verify-report CLI exit codes', () => {
  let tmpDir, evoDir;
  let savedEnv = {};

  beforeEach(() => {
    savedEnv.MEMORY_DIR = process.env.MEMORY_DIR;
    savedEnv.EVOLUTION_DIR = process.env.EVOLUTION_DIR;
    savedEnv.EVOLVER_REPO_ROOT = process.env.EVOLVER_REPO_ROOT;
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'rvr-cli-'));
    evoDir = path.join(tmpDir, 'evolution');
    fs.mkdirSync(evoDir, { recursive: true });
    fs.mkdirSync(path.join(tmpDir, 'memory'), { recursive: true });
    process.env.EVOLUTION_DIR = evoDir;
    process.env.MEMORY_DIR = path.join(tmpDir, 'memory');
    process.env.EVOLVER_REPO_ROOT = tmpDir;
  });

  afterEach(() => {
    try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
    for (const k of ['MEMORY_DIR', 'EVOLUTION_DIR', 'EVOLVER_REPO_ROOT']) {
      if (savedEnv[k] === undefined) delete process.env[k];
      else process.env[k] = savedEnv[k];
    }
  });

  function writeEvents(events) {
    const file = path.join(evoDir, 'memory_graph.jsonl');
    fs.writeFileSync(file, events.map(JSON.stringify).join('\n') + '\n', 'utf8');
  }

  function runReport(extraArgs) {
    const args = (extraArgs || []).join(' ');
    const cmd = 'node ' + path.join(__dirname, '..', 'scripts', 'recall-verify-report.js') + ' ' + args;
    try {
      const out = execSync(cmd, { env: process.env, encoding: 'utf8' });
      return { code: 0, out };
    } catch (err) {
      return { code: err.status, out: err.stdout || '', err: err.stderr || '' };
    }
  }

  it('exits 0 when ship gate is GREEN', () => {
    const events = [];
    for (let i = 0; i < 20; i++) events.push(mkEvent('Capsule', 'roundtrip_ok', 100, 5000));
    writeEvents(events);
    const r = runReport(['--json']);
    assert.equal(r.code, 0);
    const parsed = JSON.parse(r.out);
    assert.equal(parsed.gate, 'GREEN');
  });

  it('exits 2 when ship gate is RED (mismatch)', () => {
    writeEvents([
      mkEvent('Capsule', 'roundtrip_ok', 100, 5000),
      mkEvent('Capsule', 'roundtrip_mismatch', 100, 5000),
    ]);
    const r = runReport(['--json']);
    assert.equal(r.code, 2);
  });

  it('exits 2 when no events found', () => {
    writeEvents([]);
    const r = runReport(['--json']);
    assert.equal(r.code, 2);
  });

  it('--since filters by ts', () => {
    const oldTs = Date.now() - 7200000;
    const newTs = Date.now() - 60000;
    writeEvents([
      mkEventWithTs('Capsule', 'roundtrip_missing', 100, 5000, oldTs),
      mkEventWithTs('Capsule', 'roundtrip_ok', 100, 5000, newTs),
    ]);
    const r = runReport(['--since', '1h', '--json']);
    const parsed = JSON.parse(r.out);
    assert.equal(parsed.totals.total, 1, 'only the recent event counted');
    assert.equal(parsed.totals.ok, 1);
  });
});

function mkEvent(type, outcome, latency_ms, age_at_verify_ms, reason) {
  return mkEventWithTs(type, outcome, latency_ms, age_at_verify_ms, Date.now(), reason);
}

function mkEventWithTs(type, outcome, latency_ms, age_at_verify_ms, ts, reason) {
  return {
    type: 'MemoryGraphEvent',
    kind: 'recall_verify',
    id: 'mge_' + ts + '_' + Math.random().toString(36).slice(2, 8),
    ts,
    asset: { type, id: 'sha256:dummy' + Math.random().toString(36).slice(2, 8) },
    verification: {
      outcome,
      reason: reason || null,
      attempts: 1,
      latency_ms,
      age_at_verify_ms,
      recalled_hash: outcome === 'roundtrip_ok' ? 'sha256:dummy' : null,
    },
    signal: { signals: [] },
  };
}
