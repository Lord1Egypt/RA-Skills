'use strict';

// Verifies the per-run token-usage rollup over the proxy trace log: plaintext
// rows, real encrypted round-trip (encryptTraceEvent -> decrypt in the reader),
// time-window filtering, and graceful unmeasured fallbacks.

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const { sumRunUsage } = require('../src/proxy/trace/usage');
const extractor = require('../src/proxy/trace/extractor');

const SECRET = 'a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90'; // 64-hex
const ENV = ['EVOMAP_PROXY_TRACE_FILE', 'A2A_NODE_SECRET', 'EVOLVER_HOME', 'EVOMAP_PROXY_TRACE_ENCRYPTION'];

const SINCE = '2026-06-07T10:00:00.000Z';
const IN_WINDOW = '2026-06-07T10:00:05.000Z';
const BEFORE_WINDOW = '2026-06-07T09:59:00.000Z';

describe('proxy trace usage rollup (sumRunUsage)', () => {
  let tmp, file, saved;

  beforeEach(() => {
    tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'trace-usage-'));
    file = path.join(tmp, 'proxy-traces.jsonl');
    saved = {};
    for (const k of ENV) { saved[k] = process.env[k]; delete process.env[k]; }
    process.env.EVOMAP_PROXY_TRACE_FILE = file;
    process.env.EVOLVER_HOME = tmp; // isolate node-secret/state lookups from the host
  });

  afterEach(() => {
    for (const k of ENV) { if (saved[k] === undefined) delete process.env[k]; else process.env[k] = saved[k]; }
    fs.rmSync(tmp, { recursive: true, force: true });
  });

  function writeLines(rows) {
    fs.writeFileSync(file, rows.map(r => JSON.stringify(r)).join('\n') + '\n', 'utf8');
  }

  it('reports unmeasured when sinceIso is missing (cannot correlate)', () => {
    const r = sumRunUsage({});
    assert.equal(r.measured, false);
    assert.equal(r.total_tokens, 0);
  });

  it('reports unmeasured when the trace file does not exist', () => {
    const r = sumRunUsage({ sinceIso: SINCE });
    assert.equal(r.measured, false);
  });

  it('sums plaintext rows in-window and ignores out-of-window rows', () => {
    writeLines([
      { timestamp: IN_WINDOW, input_tokens: 1000, output_tokens: 200 },
      { timestamp: IN_WINDOW, input_tokens: 500, output_tokens: 100 },
      { timestamp: BEFORE_WINDOW, input_tokens: 9999, output_tokens: 9999 }, // excluded
    ]);
    const r = sumRunUsage({ sinceIso: SINCE });
    assert.equal(r.measured, true);
    assert.equal(r.input_tokens, 1500);
    assert.equal(r.output_tokens, 300);
    assert.equal(r.total_tokens, 1800);
    assert.equal(r.calls, 2);
  });

  it('decrypts encrypted rows with the node secret and sums them', () => {
    process.env.A2A_NODE_SECRET = SECRET;
    const env1 = extractor.encryptTraceEvent({ timestamp: IN_WINDOW, input_tokens: 2000, output_tokens: 400 });
    const env2 = extractor.encryptTraceEvent({ timestamp: IN_WINDOW, input_tokens: 100, output_tokens: 50 });
    assert.equal(env1.encrypted, true, 'sanity: produced an encrypted envelope');
    writeLines([env1, env2]);
    const r = sumRunUsage({ sinceIso: SINCE });
    assert.equal(r.measured, true);
    assert.equal(r.total_tokens, 2550);
    assert.equal(r.calls, 2);
  });

  it('cannot read encrypted rows without the secret -> unmeasured', () => {
    process.env.A2A_NODE_SECRET = SECRET;
    const enc = extractor.encryptTraceEvent({ timestamp: IN_WINDOW, input_tokens: 2000, output_tokens: 400 });
    writeLines([enc]);
    delete process.env.A2A_NODE_SECRET; // reader has no key now
    const r = sumRunUsage({ sinceIso: SINCE });
    assert.equal(r.measured, false);
    assert.equal(r.total_tokens, 0);
  });

  it('treats rows with no usage as unobserved (measured:false)', () => {
    writeLines([{ timestamp: IN_WINDOW, input_tokens: null, output_tokens: null }]);
    const r = sumRunUsage({ sinceIso: SINCE });
    assert.equal(r.measured, false);
  });

  it('tolerates corrupt lines without throwing', () => {
    fs.writeFileSync(
      file,
      'not-json\n' + JSON.stringify({ timestamp: IN_WINDOW, input_tokens: 700, output_tokens: 0 }) + '\n',
      'utf8'
    );
    const r = sumRunUsage({ sinceIso: SINCE });
    assert.equal(r.measured, true);
    assert.equal(r.input_tokens, 700);
    assert.equal(r.calls, 1);
  });
});
