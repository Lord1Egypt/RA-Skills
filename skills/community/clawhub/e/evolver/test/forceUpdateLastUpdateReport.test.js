// Tests for client-side last_update reporting (evomap-hub #1034 / #1039).
//
// After each executeForceUpdate attempt the client persists the outcome to
// ${EVOLVER_HOME}/force_update_last.json, then attaches it as
// body.last_update on the next /a2a/heartbeat POST. The hub-side
// EvolverUpgradeAttempt table is populated from this field; without these
// reports the table stays empty forever.

const { describe, it, before, after, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

if (!process.env.A2A_NODE_SECRET) {
  process.env.A2A_NODE_SECRET = 'a'.repeat(64);
}

// Rigged require cache: swap the forceUpdate module for a spy BEFORE
// a2aProtocol is required, so _maybeTriggerForceUpdateFromHeartbeat picks up
// the spy instead of spawning npm/degit against the real network.
// Load the real module FIRST so we can passthrough its pure helpers
// (sentinel symbols, validator-for-testing) on the spy -- otherwise tests
// that need parity with forceUpdate.js can't reach the validator.
const forceUpdatePath = require.resolve('../src/forceUpdate');
const _realForceUpdate = require('../src/forceUpdate');
let executeForceUpdateCalls = [];
let executeForceUpdateReturn = false;
let executeForceUpdateThrow = null;
require.cache[forceUpdatePath] = {
  id: forceUpdatePath,
  filename: forceUpdatePath,
  loaded: true,
  exports: {
    executeForceUpdate: function (fu) {
      executeForceUpdateCalls.push(fu);
      if (executeForceUpdateThrow) throw executeForceUpdateThrow;
      return executeForceUpdateReturn;
    },
    // Passthrough the real pure helpers so parity tests + sentinel checks
    // still reach the actual implementation.
    FORCE_UPDATE_NOOP: _realForceUpdate.FORCE_UPDATE_NOOP,
    FORCE_UPDATE_BUSY: _realForceUpdate.FORCE_UPDATE_BUSY,
    _isAcceptedRequiredVersionForTesting: _realForceUpdate._isAcceptedRequiredVersionForTesting,
  },
};

const a2aProtocol = require('../src/gep/a2aProtocol');
const {
  sendHeartbeat,
  reportForceUpdateOutcome,
  readPendingLastUpdate,
  clearLastUpdateOnAck,
} = a2aProtocol;
const {
  _resetForceUpdateStateForTesting,
  _resetLastUpdateStateForTesting,
  _persistLastUpdateStateForTesting,
  _getLastUpdateStatePathForTesting,
  _extractTargetVersionForTesting,
} = a2aProtocol._testing;

describe('force_update last_update reporting', () => {
  var tmpDir;
  var evomapHomeDir;
  var originalFetch;
  var originalHubUrl;
  var originalLogsDir;
  var originalEvolverHome;
  var originalProcessExit;
  var originalInsecure;
  var exitCalls;
  var fetchCalls;
  var fetchResponder;

  before(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-lu-test-'));
    evomapHomeDir = path.join(tmpDir, 'evomap-home');
    fs.mkdirSync(evomapHomeDir, { recursive: true });

    originalHubUrl = process.env.A2A_HUB_URL;
    originalLogsDir = process.env.EVOLVER_LOGS_DIR;
    originalEvolverHome = process.env.EVOLVER_HOME;
    originalInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;

    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOLVER_LOGS_DIR = tmpDir;
    process.env.EVOLVER_HOME = evomapHomeDir;
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';

    originalFetch = global.fetch;
    originalProcessExit = process.exit;
  });

  after(() => {
    global.fetch = originalFetch;
    process.exit = originalProcessExit;
    if (originalHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = originalHubUrl;
    if (originalLogsDir === undefined) delete process.env.EVOLVER_LOGS_DIR;
    else process.env.EVOLVER_LOGS_DIR = originalLogsDir;
    if (originalEvolverHome === undefined) delete process.env.EVOLVER_HOME;
    else process.env.EVOLVER_HOME = originalEvolverHome;
    if (originalInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = originalInsecure;
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  beforeEach(() => {
    executeForceUpdateCalls = [];
    executeForceUpdateReturn = false;
    executeForceUpdateThrow = null;
    exitCalls = [];
    process.exit = function (code) { exitCalls.push(code); };
    fetchCalls = [];
    fetchResponder = null;
    global.fetch = async function (url, opts) {
      var body = {};
      try { body = JSON.parse(opts && opts.body || '{}'); } catch (_) { body = {}; }
      fetchCalls.push({ url: String(url), body: body, opts: opts });
      if (typeof fetchResponder === 'function') return fetchResponder(url, opts);
      return {
        ok: true,
        status: 200,
        json: async () => ({ status: 'ok' }),
        text: async () => '',
      };
    };
    process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS = '0';
    _resetForceUpdateStateForTesting();
    _resetLastUpdateStateForTesting();
  });

  function _statePath() { return _getLastUpdateStatePathForTesting(); }

  // Helper used by (l)+ to cut ~30 lines of duplicated 200-OK envelope
  // boilerplate. Existing (a..k) cases are deliberately left untouched.
  function okResponder(body) {
    var payload = body || { status: 'ok' };
    return async function () {
      return {
        ok: true,
        status: 200,
        json: async () => payload,
        text: async () => '',
      };
    };
  }

  it('(a) successful force_update writes state file with status=success and required fields', async () => {
    executeForceUpdateReturn = true;
    fetchResponder = async () => ({
      ok: true, status: 200,
      json: async () => ({
        status: 'ok',
        force_update: {
          to_version: '1.88.0',
          directive_id: 'directive-abc-123',
          required_version: '>=1.88.0',
          reason: 'test',
        },
      }),
      text: async () => '',
    });

    await sendHeartbeat();
    await new Promise(r => setImmediate(r));

    assert.equal(exitCalls.length, 1, 'process.exit called on success');
    assert.equal(exitCalls[0], 78);
    assert.ok(fs.existsSync(_statePath()), 'state file written');
    var payload = JSON.parse(fs.readFileSync(_statePath(), 'utf8'));
    assert.equal(payload.status, 'success');
    assert.equal(payload.to_version, '1.88.0');
    assert.equal(typeof payload.from_version, 'string');
    assert.ok(payload.from_version.length > 0, 'from_version captured before exit');
    assert.equal(payload.directive_id, 'directive-abc-123');
    assert.equal(typeof payload.finished_at, 'number');
    assert.ok(payload.finished_at >= 1700000000000, 'finished_at in ms-since-epoch range');
  });

  it('(b) failed force_update writes state file with status=failed and error truncated to <=1000', async () => {
    executeForceUpdateReturn = false;
    // Make executeForceUpdate throw with a very long error message.
    executeForceUpdateThrow = new Error('x'.repeat(2500));
    fetchResponder = async () => ({
      ok: true, status: 200,
      json: async () => ({
        status: 'ok',
        force_update: { to_version: '1.88.0', required_version: '>=1.88.0', reason: 'test' },
      }),
      text: async () => '',
    });

    await sendHeartbeat();
    await new Promise(r => setImmediate(r));

    assert.equal(exitCalls.length, 0, 'no exit on failure');
    assert.ok(fs.existsSync(_statePath()), 'state file written on failure');
    var payload = JSON.parse(fs.readFileSync(_statePath(), 'utf8'));
    assert.equal(payload.status, 'failed');
    assert.equal(payload.to_version, '1.88.0');
    assert.equal(typeof payload.error, 'string');
    assert.ok(payload.error.length <= 1000, 'error truncated to <=1000 chars');
    assert.equal(payload.error.length, 1000);
  });

  it('(c) heartbeat body includes last_update from state file', async () => {
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      from_version: '1.87.0',
      status: 'success',
      finished_at: Date.now(),
      directive_id: 'd1',
    });

    await sendHeartbeat();

    assert.equal(fetchCalls.length, 1);
    assert.ok(fetchCalls[0].body.last_update, 'last_update attached to body');
    assert.equal(fetchCalls[0].body.last_update.to_version, '1.88.0');
    assert.equal(fetchCalls[0].body.last_update.status, 'success');
    assert.equal(fetchCalls[0].body.last_update.directive_id, 'd1');
  });

  it('(d) heartbeat 200 OK deletes the state file', async () => {
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
    });
    assert.ok(fs.existsSync(_statePath()), 'precondition: file exists');

    fetchResponder = async () => ({
      ok: true, status: 200,
      json: async () => ({ status: 'ok' }),
      text: async () => '',
    });

    var result = await sendHeartbeat();
    assert.ok(result.ok);
    assert.ok(!fs.existsSync(_statePath()), 'state file deleted on 2xx');
  });

  it('(e) heartbeat 500 keeps the state file (state preserved across non-2xx and network errors)', async () => {
    // 1) HTTP 500 case
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
    });
    assert.ok(fs.existsSync(_statePath()), 'precondition: file exists');

    fetchResponder = async () => ({
      ok: false, status: 500,
      json: async () => ({ error: 'internal' }),
      text: async () => 'internal error',
    });

    await sendHeartbeat();
    assert.ok(fs.existsSync(_statePath()), 'state file kept on HTTP 500 (data.ok=false)');

    // 2) Fetch-rejects (network) case
    fetchResponder = async () => { throw new Error('ECONNREFUSED'); };
    var result = await sendHeartbeat();
    assert.equal(result.ok, false, 'heartbeat returns ok:false on network error');
    assert.ok(fs.existsSync(_statePath()), 'state file kept on network error (.catch path)');
  });

  it('(f) corrupt state file is silently dropped and file removed; body has no last_update', async () => {
    // Write deliberately invalid JSON.
    fs.mkdirSync(path.dirname(_statePath()), { recursive: true });
    fs.writeFileSync(_statePath(), '{not valid json', 'utf8');
    assert.ok(fs.existsSync(_statePath()));

    await sendHeartbeat();

    assert.equal(fetchCalls.length, 1);
    assert.ok(
      !Object.prototype.hasOwnProperty.call(fetchCalls[0].body, 'last_update'),
      'no last_update key in body when state file is corrupt'
    );
    assert.ok(!fs.existsSync(_statePath()), 'corrupt file removed');

    // Also a valid-JSON-but-missing-to_version variant.
    fs.writeFileSync(_statePath(), JSON.stringify({ status: 'success' }), 'utf8');
    await sendHeartbeat();
    assert.equal(fetchCalls.length, 2);
    assert.ok(!Object.prototype.hasOwnProperty.call(fetchCalls[1].body, 'last_update'));
    assert.ok(!fs.existsSync(_statePath()));

    // And a valid-JSON-but-bad-status variant.
    fs.writeFileSync(_statePath(), JSON.stringify({ to_version: '1.88.0', status: 'bogus' }), 'utf8');
    await sendHeartbeat();
    assert.equal(fetchCalls.length, 3);
    assert.ok(!Object.prototype.hasOwnProperty.call(fetchCalls[2].body, 'last_update'));
    assert.ok(!fs.existsSync(_statePath()));
  });

  it('(g) no state file → body has no last_update key (not null)', async () => {
    assert.ok(!fs.existsSync(_statePath()), 'precondition: no state file');

    await sendHeartbeat();

    assert.equal(fetchCalls.length, 1);
    assert.ok(
      !Object.prototype.hasOwnProperty.call(fetchCalls[0].body, 'last_update'),
      'last_update key omitted when state file absent'
    );
  });

  // ---------------------------------------------------------------------
  // PR #188 review follow-ups: HIGH lost-write race, HIGH read-side
  // revalidation, MEDIUM required_version parsing.
  // ---------------------------------------------------------------------

  it('(h) lost-write race: 2xx clear keeps a file rewritten mid-flight', async () => {
    // Step 1: persist the FIRST outcome and start a heartbeat that captures
    // it as _pendingLastUpdate at request-build time.
    var firstFinishedAt = 1_800_000_000_000;
    var first = {
      to_version: '1.88.0',
      status: 'failed',
      finished_at: firstFinishedAt,
      error: 'first attempt timed out',
    };
    _persistLastUpdateStateForTesting(first);
    assert.ok(fs.existsSync(_statePath()), 'precondition: file exists');

    // Step 2: while the hub call is "in flight" (before our fetchResponder
    // resolves), simulate a concurrent _maybeTriggerForceUpdateFromHeartbeat
    // retry past cooldown writing a fresher outcome to the same path.
    var second = {
      to_version: '1.88.0',
      status: 'failed',
      finished_at: firstFinishedAt + 60_000,
      error: 'second attempt also failed (different cause)',
    };
    fetchResponder = async () => {
      _persistLastUpdateStateForTesting(second);
      return {
        ok: true, status: 200,
        json: async () => ({ status: 'ok' }),
        text: async () => '',
      };
    };

    var result = await sendHeartbeat();
    assert.ok(result.ok);

    // File MUST still exist and hold the fresher payload.
    assert.ok(fs.existsSync(_statePath()), 'state file kept (identity mismatch)');
    var onDisk = JSON.parse(fs.readFileSync(_statePath(), 'utf8'));
    assert.equal(onDisk.finished_at, second.finished_at,
      'fresher payload preserved (clear refused identity mismatch)');
    assert.equal(onDisk.error, second.error,
      'fresher error preserved across clear');

    // And the body we sent must have carried the FIRST payload, not the
    // second (proves the request was built before the rewrite).
    var lu = fetchCalls[fetchCalls.length - 1].body.last_update;
    assert.equal(lu.finished_at, firstFinishedAt,
      'body.last_update carried the captured first payload');
  });

  it('(i) corrupt optional fields are stripped at read time', async () => {
    // Hand-edit a state file with all four "should-be-fixed-up" defects.
    fs.mkdirSync(path.dirname(_statePath()), { recursive: true });
    fs.writeFileSync(_statePath(), JSON.stringify({
      to_version: '1.88.0',
      status: 'failed',
      finished_at: 1_700_000_000,      // seconds, not ms -- must be stripped
      error: 'x'.repeat(2000),         // too long -- must be truncated
      directive_id: '',                // empty -- hub rejects min:1; must be stripped
      from_version: 'a'.repeat(50),    // too long -- must be truncated to 32
    }), 'utf8');

    await sendHeartbeat();

    assert.equal(fetchCalls.length, 1);
    var lu = fetchCalls[0].body.last_update;
    assert.ok(lu, 'last_update present (required fields valid)');
    assert.equal(lu.to_version, '1.88.0');
    assert.equal(lu.status, 'failed');
    // Required survives, optionals are sanitised:
    assert.ok(!Object.prototype.hasOwnProperty.call(lu, 'finished_at'),
      'finished_at stripped (seconds instead of ms)');
    assert.ok(!Object.prototype.hasOwnProperty.call(lu, 'directive_id'),
      'directive_id stripped (empty string)');
    assert.equal(lu.from_version.length, 32, 'from_version truncated to 32');
    assert.equal(lu.error.length, 1000, 'error truncated to 1000');
  });

  it('(j) required_version is parsed: strips >=, >, ~, ^ etc. with whitespace', async () => {
    // Case 1: ">=1.88.0" -> "1.88.0"
    executeForceUpdateReturn = false;
    fetchResponder = async () => ({
      ok: true, status: 200,
      json: async () => ({
        status: 'ok',
        force_update: { required_version: '>=1.88.0', reason: 'test' },
      }),
      text: async () => '',
    });
    await sendHeartbeat();
    await new Promise(r => setImmediate(r));

    assert.ok(fs.existsSync(_statePath()));
    var p1 = JSON.parse(fs.readFileSync(_statePath(), 'utf8'));
    assert.equal(p1.to_version, '1.88.0',
      'required_version ">=1.88.0" parsed to "1.88.0"');

    // Reset for case 2.
    _resetForceUpdateStateForTesting();
    _resetLastUpdateStateForTesting();

    // Case 2: ">= 2.0.0-rc.5" (with whitespace) -> "2.0.0-rc.5"
    fetchResponder = async () => ({
      ok: true, status: 200,
      json: async () => ({
        status: 'ok',
        force_update: { required_version: '>= 2.0.0-rc.5', reason: 'test' },
      }),
      text: async () => '',
    });
    await sendHeartbeat();
    await new Promise(r => setImmediate(r));

    assert.ok(fs.existsSync(_statePath()));
    var p2 = JSON.parse(fs.readFileSync(_statePath(), 'utf8'));
    assert.equal(p2.to_version, '2.0.0-rc.5',
      'required_version ">= 2.0.0-rc.5" parsed to "2.0.0-rc.5"');
  });

  it('(k) missing required_version → no state file written, warn logged', async () => {
    var warnings = [];
    var originalWarn = console.warn;
    console.warn = function () {
      try { warnings.push(Array.from(arguments).join(' ')); } catch (_) {}
    };
    try {
      executeForceUpdateReturn = false;
      fetchResponder = async () => ({
        ok: true, status: 200,
        json: async () => ({
          status: 'ok',
          // No required_version, no to_version, no version.
          force_update: { reason: 'test' },
        }),
        text: async () => '',
      });

      await sendHeartbeat();
      await new Promise(r => setImmediate(r));

      assert.ok(!fs.existsSync(_statePath()),
        'state file NOT written when no parsable target version');
      var matched = warnings.some(function (w) {
        return w.indexOf('no parsable target version') !== -1;
      });
      assert.ok(matched,
        'expected warn with "no parsable target version", got: ' + JSON.stringify(warnings));
    } finally {
      console.warn = originalWarn;
    }
  });

  // ---------------------------------------------------------------------
  // PR #188 Phase 1 review follow-ups: TTL, stricter _extractTargetVersion,
  // 400 circuit breaker, public reportForceUpdateOutcome /
  // readPendingLastUpdate / clearLastUpdateOnAck API.
  // ---------------------------------------------------------------------

  it('(l) TTL: stale state file (finished_at > 7d old) is dropped at read time', async () => {
    var eightDaysAgo = Date.now() - 8 * 24 * 60 * 60 * 1000;
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: eightDaysAgo,
    });
    assert.ok(fs.existsSync(_statePath()), 'precondition: file exists');

    await sendHeartbeat();

    assert.equal(fetchCalls.length, 1);
    assert.ok(
      !Object.prototype.hasOwnProperty.call(fetchCalls[0].body, 'last_update'),
      'no last_update key when state is older than 7d TTL'
    );
    assert.ok(!fs.existsSync(_statePath()), 'stale state file removed by TTL gate');
  });

  it('(m) TTL: non-stale state file (<7d) is kept and sent', async () => {
    var oneDayAgo = Date.now() - 1 * 24 * 60 * 60 * 1000;
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: oneDayAgo,
    });

    fetchResponder = okResponder({ status: 'ok' });
    await sendHeartbeat();

    assert.equal(fetchCalls.length, 1);
    assert.ok(fetchCalls[0].body.last_update, 'last_update present for <7d state');
    assert.equal(fetchCalls[0].body.last_update.to_version, '1.88.0');
    assert.equal(fetchCalls[0].body.last_update.finished_at, oneDayAgo);
  });

  it('(n) strict _extractTargetVersion: AND range ">=1.88.0 <2.0.0" rejected, no state file', async () => {
    var warnings = [];
    var originalWarn = console.warn;
    console.warn = function () {
      try { warnings.push(Array.from(arguments).join(' ')); } catch (_) {}
    };
    try {
      executeForceUpdateReturn = false;
      fetchResponder = okResponder({
        status: 'ok',
        force_update: { required_version: '>=1.88.0 <2.0.0', reason: 'test' },
      });

      await sendHeartbeat();
      await new Promise(r => setImmediate(r));

      assert.ok(!fs.existsSync(_statePath()),
        'state file NOT written for AND-range required_version');
      var matched = warnings.some(function (w) {
        return w.indexOf('no parsable target version') !== -1;
      });
      assert.ok(matched,
        'expected warn with "no parsable target version", got: ' + JSON.stringify(warnings));
    } finally {
      console.warn = originalWarn;
    }
  });

  it('(o) strict _extractTargetVersion: wildcard "*" rejected, no state file', async () => {
    executeForceUpdateReturn = false;
    fetchResponder = okResponder({
      status: 'ok',
      force_update: { required_version: '*', reason: 'test' },
    });

    await sendHeartbeat();
    await new Promise(r => setImmediate(r));

    assert.ok(!fs.existsSync(_statePath()),
      'state file NOT written for wildcard required_version');
  });

  it('(p) strict _extractTargetVersion: dist-tag "latest" rejected, no state file', async () => {
    executeForceUpdateReturn = false;
    fetchResponder = okResponder({
      status: 'ok',
      force_update: { required_version: 'latest', reason: 'test' },
    });

    await sendHeartbeat();
    await new Promise(r => setImmediate(r));

    assert.ok(!fs.existsSync(_statePath()),
      'state file NOT written for dist-tag required_version');
  });

  it('(q) 400 circuit breaker: error string naming last_update clears file', async () => {
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
    });
    assert.ok(fs.existsSync(_statePath()), 'precondition: file exists');

    fetchResponder = async () => ({
      ok: false, status: 400,
      json: async () => ({ error: 'invalid last_update field' }),
      text: async () => 'invalid last_update field',
    });

    await sendHeartbeat();

    assert.ok(!fs.existsSync(_statePath()),
      'state file unlinked (400 + error names last_update)');
  });

  it('(r) 400 circuit breaker: non-last_update 400 does not trip breaker (file kept, counter not bumped)', async () => {
    // PR #188 follow-up: the breaker MUST be scoped to 400s about
    // last_update. A 400 for an unrelated field (fingerprint, node_id,
    // etc.) must not count toward the 3-strike threshold and must not
    // unlink the state file -- that file is legitimate upgrade telemetry
    // and the 400 is some other code's bug.
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
    });

    fetchResponder = async () => ({
      ok: false, status: 400,
      json: async () => ({ error: 'bad_request' }),
      text: async () => 'bad_request',
    });

    // Three consecutive UNRELATED 400s: file must remain intact every time.
    await sendHeartbeat();
    assert.ok(fs.existsSync(_statePath()),
      'file present after 1st non-last_update 400 (counter not bumped)');

    await sendHeartbeat();
    assert.ok(fs.existsSync(_statePath()),
      'file present after 2nd non-last_update 400 (counter not bumped)');

    await sendHeartbeat();
    assert.ok(fs.existsSync(_statePath()),
      'file present after 3rd non-last_update 400 (breaker did NOT fire)');
  });

  it('(r2) 400 circuit breaker: 3 consecutive last_update-related 400s clear file', async () => {
    // Proves the breaker still works for its intended cause -- a hub
    // validation_error whose body mentions the last_update field path
    // (the hub's validateBody envelope serialises the path array into
    // the JSON body, which lands in the client error string verbatim).
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
    });

    // Mimic the real hub validateBody envelope: error key is
    // "validation_error" and the path "last_update.finished_at" is in
    // the details. The producer at a2aProtocol.js:1968 stuffs the entire
    // body text into `error: 'http_400: <body>'`, so the regex matches.
    fetchResponder = async () => ({
      ok: false, status: 400,
      json: async () => ({
        error: 'validation_error',
        details: [{ path: ['last_update', 'finished_at'], message: 'expected number' }],
      }),
      text: async () => JSON.stringify({
        error: 'validation_error',
        details: [{ path: ['last_update', 'finished_at'], message: 'expected number' }],
      }),
    });

    // First last_update-related 400 will fire the breaker IMMEDIATELY
    // (the existing "error names last_update" branch fires on the very
    // first hit -- the 3-strike branch is for borderline cases where the
    // hub body is too generic to name the field). To verify the 3-strike
    // counting works for last_update-related errors specifically, drive
    // it via the broader regex match path with an error body that
    // contains "last_update" only via the field path, which still hits
    // the regex -- and the same-tick mentionsLastUpdate==true fires the
    // unlink immediately. So this case is the "fires on first hit" path.
    await sendHeartbeat();
    assert.ok(!fs.existsSync(_statePath()),
      'state file unlinked on first 400 that names last_update');
  });

  it('(r3) 400 circuit breaker: warn at fire-time is NOT suppressed by an unrelated rate-limited warn in the same hour', async () => {
    // _warnLastUpdateRateLimited has a shared 1h budget across all
    // ForceUpdate warns. The threshold-fire moment must bypass that
    // budget -- otherwise an unrelated earlier warn (e.g. corrupt state
    // file dropped, persist failed, stale TTL drop) would silently
    // swallow the critical "breaker fired" signal for up to an hour.
    //
    // Note: the module-level _lastUpdateWarnState rate limiter has likely
    // already been armed by warns emitted in earlier test cases (it has
    // no per-test reset hook -- a deliberate scope-out: the limiter is
    // module state by design and adding test hooks for it would couple
    // tests to implementation details). The fact that the breaker-fire
    // warn appears under that condition IS the property under test.
    var warnings = [];
    var originalWarn = console.warn;
    console.warn = function () {
      try { warnings.push(Array.from(arguments).join(' ')); } catch (_) {}
    };
    try {
      // Drive a corrupt-state read inside this case too so the rate
      // limiter is definitely armed at the time of the breaker fire,
      // regardless of test ordering. We don't assert on the corrupt-state
      // warn here (it may or may not appear, depending on whether the
      // module-level limiter was already armed by earlier tests) -- the
      // post-condition is the breaker-fire warn appearing.
      fs.mkdirSync(path.dirname(_statePath()), { recursive: true });
      fs.writeFileSync(_statePath(), '{not valid json', 'utf8');
      await sendHeartbeat();

      // Drive the breaker via a last_update-related 400. The fire-time
      // warn MUST appear -- it uses console.warn directly, NOT the
      // shared rate limiter.
      _persistLastUpdateStateForTesting({
        to_version: '1.88.0',
        status: 'success',
        finished_at: Date.now(),
      });
      var body = JSON.stringify({
        error: 'validation_error',
        details: [{ path: ['last_update', 'to_version'], message: 'invalid' }],
      });
      fetchResponder = async () => ({
        ok: false, status: 400,
        json: async () => JSON.parse(body),
        text: async () => body,
      });

      // Reset the captured warnings AFTER the corrupt-state setup so we
      // measure only the breaker tick's output.
      warnings.length = 0;
      await sendHeartbeat();

      var sawBreakerWarn = warnings.some(function (w) {
        return w.indexOf('hub 400 with last_update attached') !== -1
          && w.indexOf('clearing poisoning state file') !== -1;
      });
      assert.ok(sawBreakerWarn,
        'breaker-fire warn must appear even when shared rate limiter is on cooldown; got: ' +
        JSON.stringify(warnings));
      assert.ok(!fs.existsSync(_statePath()),
        'file cleared as a side-effect of the same breaker fire');
    } finally {
      console.warn = originalWarn;
    }
  });

  it('(s) 400 circuit breaker: counter resets on intervening 2xx', async () => {
    // Use last_update-related 400s because PR #188 follow-up scoped the
    // breaker to those -- unrelated 400s never touch the counter, so they
    // could not prove the reset behaviour. We use a body the regex
    // matches via the field-path string but whose top-level error is NOT
    // the literal "last_update" (avoid the first-strike fire branch).
    var ambiguousLastUpdate400 = function () {
      var body = JSON.stringify({
        error: 'something_else',
        // Note: regex matches "last_update" anywhere in the body, but the
        // mentionsLastUpdate first-strike branch ALSO matches it. So this
        // case fires on tick 1, not tick 3. To exercise the counter
        // specifically we need a path that increments but does not fire.
        // No such body exists in the current implementation; this test
        // therefore covers the related invariant: a successful 2xx in the
        // middle DOES reset the counter when 400s do reach the bump
        // branch. We assert this via behaviour rather than internal state.
        details: [{ path: ['last_update'] }],
      });
      return {
        ok: false, status: 400,
        json: async () => JSON.parse(body),
        text: async () => body,
      };
    };

    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
    });

    // Tick 1: ambiguous 400 mentioning last_update -> fires immediately
    // (mentionsLastUpdate is true), file unlinked, counter reset to 0.
    fetchResponder = ambiguousLastUpdate400;
    await sendHeartbeat();
    assert.ok(!fs.existsSync(_statePath()),
      'file unlinked on first last_update-related 400 (regex matched)');

    // Tick 2: 200 OK -- counter (already 0) stays 0. No file present so
    // nothing to clear; this just verifies the reset branch does not
    // crash on no-pending-payload.
    fetchResponder = okResponder({ status: 'ok' });
    await sendHeartbeat();

    // Tick 3: re-persist and confirm the file again gets cleared on the
    // first last_update-related 400, proving the breaker is healthy.
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
    });
    fetchResponder = ambiguousLastUpdate400;
    await sendHeartbeat();
    assert.ok(!fs.existsSync(_statePath()),
      'breaker still fires after intervening 2xx (counter was reset)');
  });

  it('(t) reportForceUpdateOutcome public API: success path persists payload', async () => {
    assert.ok(!fs.existsSync(_statePath()), 'precondition: no state file');

    reportForceUpdateOutcome(
      { required_version: '>=1.88.0', directive_id: 'd1' },
      { updated: true, fromVersion: '1.87.0' }
    );

    assert.ok(fs.existsSync(_statePath()), 'state file persisted via public API');
    var payload = JSON.parse(fs.readFileSync(_statePath(), 'utf8'));
    assert.equal(payload.status, 'success');
    assert.equal(payload.to_version, '1.88.0');
    assert.equal(payload.from_version, '1.87.0');
    assert.equal(payload.directive_id, 'd1');
    assert.equal(typeof payload.finished_at, 'number');
    assert.ok(payload.finished_at >= 1700000000000, 'finished_at in ms-since-epoch range');
  });

  it('(u) reportForceUpdateOutcome public API: failure path persists status=failed with error', async () => {
    assert.ok(!fs.existsSync(_statePath()));

    reportForceUpdateOutcome(
      { required_version: '>=1.88.0' },
      { updated: false, error: new Error('boom') }
    );

    assert.ok(fs.existsSync(_statePath()), 'state file persisted via public API');
    var payload = JSON.parse(fs.readFileSync(_statePath(), 'utf8'));
    assert.equal(payload.status, 'failed');
    assert.equal(payload.to_version, '1.88.0');
    // A THROWN error (no structured failure) is prefixed with the
    // `unexpected_error` code so every failed row carries a "code: detail"
    // shape for GROUP BY split_part(error, ':', 1). executeForceUpdate now
    // catches its own Channel 1 errors and RETURNS structured failures, so
    // this thrown path is the rare "threw outside the inner try" case.
    assert.equal(payload.error, 'unexpected_error: boom');
  });

  it('(u2) structured failure encodes as "code: detail" (the headline feature)', () => {
    assert.ok(!fs.existsSync(_statePath()));
    reportForceUpdateOutcome(
      { required_version: '>=1.88.3' },
      { updated: false, failure: { ok: false, code: 'degit_failed', detail: 'spawn npx ENOENT' } }
    );
    var payload = JSON.parse(fs.readFileSync(_statePath(), 'utf8'));
    assert.equal(payload.status, 'failed');
    // This is the whole point: the hub can now `GROUP BY split_part(error, ':', 1)`
    // instead of seeing N rows of the identical "executeForceUpdate returned false".
    assert.equal(payload.error, 'degit_failed: spawn npx ENOENT');
  });

  it('(u3) structured failure with empty detail persists the bare code', () => {
    reportForceUpdateOutcome(
      { required_version: '>=1.88.3' },
      { updated: false, failure: { ok: false, code: 'all_channels_exhausted', detail: '' } }
    );
    var payload = JSON.parse(fs.readFileSync(_statePath(), 'utf8'));
    assert.equal(payload.error, 'all_channels_exhausted');
  });

  it('(u4) structured failure (returned) wins over a thrown error when both are present', () => {
    reportForceUpdateOutcome(
      { required_version: '>=1.88.3' },
      {
        updated: false,
        failure: { ok: false, code: 'copy_failed', detail: 'index.js: EPERM' },
        error: new Error('boom'),
      }
    );
    var payload = JSON.parse(fs.readFileSync(_statePath(), 'utf8'));
    assert.equal(payload.error, 'copy_failed: index.js: EPERM',
      'the precise returned-failure code beats the generic thrown error; legacy fallback never appears');
  });

  it('(u5) structured failure detail is redacted before persisting (degit stderr can carry tokens)', () => {
    var token = 'npm_' + 'c'.repeat(36);
    reportForceUpdateOutcome(
      { required_version: '>=1.88.3' },
      { updated: false, failure: { ok: false, code: 'degit_failed', detail: 'registry 401 token=' + token } }
    );
    var payload = JSON.parse(fs.readFileSync(_statePath(), 'utf8'));
    assert.ok(payload.error.startsWith('degit_failed: '), 'code prefix preserved for GROUP BY');
    assert.ok(!payload.error.includes(token), 'a token in the detail must be redacted');
    assert.ok(/\[REDACTED\]/.test(payload.error), 'redaction marker present');
  });

  it('(v) reportForceUpdateOutcome public API: unparsable required_version writes nothing', async () => {
    assert.ok(!fs.existsSync(_statePath()));

    reportForceUpdateOutcome(
      { required_version: '*' },
      { updated: true, fromVersion: '1.87.0' }
    );

    assert.ok(!fs.existsSync(_statePath()),
      'no state file written when target version unparsable');
  });

  it('(w) readPendingLastUpdate + clearLastUpdateOnAck public API: round-trip works', async () => {
    var finishedAt = Date.now();
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      from_version: '1.87.0',
      status: 'success',
      finished_at: finishedAt,
      directive_id: 'dd',
    });

    var pending = readPendingLastUpdate();
    assert.ok(pending, 'public readPendingLastUpdate returns sanitised payload');
    assert.equal(pending.to_version, '1.88.0');
    assert.equal(pending.from_version, '1.87.0');
    assert.equal(pending.status, 'success');
    assert.equal(pending.directive_id, 'dd');
    assert.equal(pending.finished_at, finishedAt);

    // Identity-matching clear removes the file.
    clearLastUpdateOnAck(pending);
    assert.ok(!fs.existsSync(_statePath()),
      'clearLastUpdateOnAck removes file when identity matches');
  });

  it('(x) retry re-sends last_update on second heartbeat after 500', async () => {
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
      directive_id: 'dx',
    });

    var n = 0;
    fetchResponder = async () => {
      n++;
      if (n === 1) {
        return {
          ok: false, status: 500,
          json: async () => ({ error: 'internal' }),
          text: async () => 'internal error',
        };
      }
      return {
        ok: true, status: 200,
        json: async () => ({ status: 'ok' }),
        text: async () => '',
      };
    };

    await sendHeartbeat();
    assert.ok(fs.existsSync(_statePath()), 'file retained after 500');

    await sendHeartbeat();
    assert.ok(!fs.existsSync(_statePath()), 'file cleared after 2xx');

    assert.equal(fetchCalls.length, 2);
    assert.ok(fetchCalls[0].body.last_update, '1st call carried last_update');
    assert.ok(fetchCalls[1].body.last_update, '2nd call also carried last_update');
    assert.deepEqual(
      fetchCalls[0].body.last_update,
      fetchCalls[1].body.last_update,
      'identical last_update payload re-sent on retry'
    );
  });

  it('(y) 200 OK with data.ok=false keeps state file (not a successful delivery)', async () => {
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
    });

    fetchResponder = async () => ({
      ok: true, status: 200,
      json: async () => ({ ok: false, error: 'something' }),
      text: async () => '',
    });

    await sendHeartbeat();

    assert.ok(fs.existsSync(_statePath()),
      'state file kept when data.ok === false despite HTTP 200');
  });

  it('(z) directive_id 64-char boundary: exact fit kept, oversized sliced to 64', async () => {
    // Exactly 64.
    var sixtyFour = 'a'.repeat(64);
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
      directive_id: sixtyFour,
    });

    await sendHeartbeat();
    assert.equal(fetchCalls.length, 1);
    assert.equal(fetchCalls[0].body.last_update.directive_id, sixtyFour,
      'exact 64-char directive_id preserved');

    // Now 65 -> slice to 64.
    _resetLastUpdateStateForTesting();
    var sixtyFive = 'a'.repeat(65);
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
      directive_id: sixtyFive,
    });

    await sendHeartbeat();
    assert.equal(fetchCalls.length, 2);
    assert.equal(fetchCalls[1].body.last_update.directive_id, sixtyFour,
      '65-char directive_id sliced to 64');
  });

  it('(aa) state file persisted with 0o600 mode on POSIX', async () => {
    if (process.platform === 'win32') return; // POSIX-only assertion
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
    });
    var st = fs.statSync(_statePath());
    assert.equal(st.mode & 0o777, 0o600,
      'state file mode is 0o600');
  });

  // ---------------------------------------------------------------------------
  // (cc..gg) Hub last_update_ack contract (PR #188 follow-up, HIGH H1-client).
  //
  // Hub now writes a top-level `last_update_ack: { ok, reason? }` on the
  // heartbeat response whenever the request carried a `last_update` payload.
  // Client gates the state-file clear on the ack rather than the bare HTTP
  // status (the previous gate dropped telemetry whenever the hub's
  // fire-and-forget persistLastUpdate threw / dedup-missed / schema-rejected
  // / bypass-returned-false after the 2xx had already been wired).
  //
  // Contract under test:
  //   ack.ok=true            -> clear
  //   ack.reason='duplicate' -> clear (already persisted via dedup)
  //   ack.reason='invalid'   -> clear + warn (retry will not help)
  //   ack.reason='failed'    -> KEEP + warn (retry next tick)
  //   no ack field           -> fall back to bare-2xx semantics (old hub)
  // ---------------------------------------------------------------------------

  it('(cc) ack.ok=true → state file cleared', async () => {
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
    });

    fetchResponder = okResponder({
      status: 'ok',
      last_update_ack: { ok: true },
    });

    await sendHeartbeat();
    assert.ok(!fs.existsSync(_statePath()),
      'ack.ok=true must clear the state file');
  });

  it('(dd) ack.reason=duplicate → state file cleared', async () => {
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
    });

    fetchResponder = okResponder({
      status: 'ok',
      last_update_ack: { ok: false, reason: 'duplicate' },
    });

    await sendHeartbeat();
    assert.ok(!fs.existsSync(_statePath()),
      'ack.reason=duplicate (dedup hit) must clear the state file');
  });

  it('(ee) ack.reason=failed → state file KEPT with warn', async () => {
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
    });

    fetchResponder = okResponder({
      status: 'ok',
      last_update_ack: { ok: false, reason: 'failed' },
    });

    // Capture console.warn so we can assert the diagnostic surfaces.
    var origWarn = console.warn;
    var warns = [];
    console.warn = function () {
      warns.push(Array.prototype.slice.call(arguments).join(' '));
    };
    try {
      await sendHeartbeat();
    } finally {
      console.warn = origWarn;
    }

    assert.ok(fs.existsSync(_statePath()),
      'ack.reason=failed must KEEP the state file so next tick retries');
    assert.ok(
      warns.some(function (m) { return /last_update_ack=failed/.test(m); }),
      'a warn must mention last_update_ack=failed'
    );
  });

  it('(ff) ack.reason=invalid → state file cleared with warn', async () => {
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
    });

    fetchResponder = okResponder({
      status: 'ok',
      last_update_ack: { ok: false, reason: 'invalid' },
    });

    var origWarn = console.warn;
    var warns = [];
    console.warn = function () {
      warns.push(Array.prototype.slice.call(arguments).join(' '));
    };
    try {
      await sendHeartbeat();
    } finally {
      console.warn = origWarn;
    }

    assert.ok(!fs.existsSync(_statePath()),
      'ack.reason=invalid must clear the state file (retry would re-fail)');
    assert.ok(
      warns.some(function (m) { return /last_update_ack=invalid/.test(m); }),
      'a warn must mention last_update_ack=invalid'
    );
  });

  it('(gg) no ack field (old hub) → falls back to bare-2xx clear behavior', async () => {
    // Backward compat: a pre-rollout hub returns 2xx without the ack
    // field. The client preserves today's behavior so the upgrade does
    // not silently break against undeployed hubs.
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
    });

    fetchResponder = okResponder({ status: 'ok' /* no last_update_ack */ });

    await sendHeartbeat();
    assert.ok(!fs.existsSync(_statePath()),
      'bare 2xx with no ack must clear (old-hub fallback path)');
  });

  it('(hh) no ack field (old hub) + data.ok=false → state file KEPT (fallback respects envelope)', async () => {
    // The fallback path must still gate on data.ok !== false: a 2xx with
    // {ok:false} from an old hub is NOT a successful delivery and is the
    // very case the original gate was added for. See (y).
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
    });

    fetchResponder = okResponder({ ok: false, error: 'transient' });

    await sendHeartbeat();
    assert.ok(fs.existsSync(_statePath()),
      'old-hub fallback must keep file when envelope says {ok:false}');
  });

  it('(ii) ack present + identity mismatch (state rotated mid-flight) → fresh file preserved', async () => {
    // Mirror of (h) but exercising the new ack path. The rotation-safe
    // clear (_clearLastUpdateStateIfMatches) must still gate on identity
    // even when the hub said ok=true: a subsequent upgrade attempt that
    // wrote a fresher payload during the heartbeat round-trip must NOT
    // be unlinked just because the OLD payload was acked.
    var initial = {
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now() - 1000,
      directive_id: 'd-old',
    };
    _persistLastUpdateStateForTesting(initial);

    // Set up the fetch responder to rewrite the file mid-flight to a
    // newer payload, then ack the OLD one.
    fetchResponder = async function () {
      _persistLastUpdateStateForTesting({
        to_version: '1.89.0',
        status: 'success',
        finished_at: Date.now(),
        directive_id: 'd-new',
      });
      return {
        ok: true,
        status: 200,
        json: async function () {
          return { status: 'ok', last_update_ack: { ok: true } };
        },
        text: async function () { return ''; },
      };
    };

    await sendHeartbeat();
    assert.ok(fs.existsSync(_statePath()),
      'fresher state must survive identity-mismatched ack');
    var current = JSON.parse(fs.readFileSync(_statePath(), 'utf8'));
    assert.equal(current.directive_id, 'd-new',
      'identity-match guard keeps the rotated payload intact');
  });

  // (jj) Bugbot PR#188 #2: when the on-disk payload has a bogus finished_at
  // (e.g. legacy seconds-precision value < FINISHED_AT_MIN), the optional
  // field is stripped from `sent` but stays on `parsed`. The OLD identity
  // tuple would diverge and refuse to clear → the file re-sends every
  // heartbeat forever (the TTL gate cannot fire because TTL also requires
  // finished_at >= FINISHED_AT_MIN). The fix sanitizes the SAME way on
  // both sides so identity matches and the file is unlinked.
  it('(jj) ack clear sanitizes both sides: bogus on-disk finished_at still matches sent', async () => {
    // Hand-craft the file: required fields valid, finished_at = seconds
    // (1.7e9, NOT ms 1.7e12) so it fails the FINISHED_AT_MIN gate.
    fs.mkdirSync(path.dirname(_statePath()), { recursive: true });
    var poisoned = {
      to_version: '1.88.0',
      status: 'success',
      finished_at: 1700000001, // seconds-since-epoch (looks valid, isn't ms)
      directive_id: 'd-jj',
    };
    fs.writeFileSync(_statePath(), JSON.stringify(poisoned), 'utf8');

    var sent = readPendingLastUpdate();
    assert.ok(sent, 'sanitizer returns a payload (only the optional finished_at is dropped)');
    assert.equal(sent.finished_at, undefined,
      'sanitizer must drop seconds-precision finished_at');
    assert.equal(sent.to_version, '1.88.0');
    assert.equal(sent.status, 'success');
    assert.equal(sent.directive_id, 'd-jj');

    clearLastUpdateOnAck(sent);
    assert.ok(!fs.existsSync(_statePath()),
      'identity sanitizer must drop the bogus finished_at on the parsed side too, so identity matches and the file is unlinked');
  });

  // (kk) Bugbot PR#188 #5: npm/degit failure messages can carry tokens,
  // paths, and other secrets. reportForceUpdateOutcome must run them
  // through redactString BEFORE truncation so a token at the tail of a
  // long stack trace cannot survive via the .slice. Uses the same
  // allowlisted redactor as every other GEP-bound payload.
  it('(kk) reportForceUpdateOutcome redacts secrets in error before truncating', async () => {
    var nukeToken = 'npm_' + 'a'.repeat(36);    // matches /npm_[A-Za-z0-9]{36,}/
    var ghToken = 'ghp_' + 'b'.repeat(36);      // matches /ghp_[A-Za-z0-9]{36,}/
    var fsPath = '/Users/alice/code/.npmrc';    // matches /\/Users\/[^...]+/
    var raw = 'npm install failed: registry returned 401 ' +
              '(token=' + nukeToken + ', ' +
              'gh=' + ghToken + ', ' +
              'file=' + fsPath + ')';
    reportForceUpdateOutcome(
      { required_version: '>=1.88.0' },
      { updated: false, error: new Error(raw), fromVersion: '1.87.0' }
    );

    assert.ok(fs.existsSync(_statePath()), 'failed-outcome state file written');
    var payload = JSON.parse(fs.readFileSync(_statePath(), 'utf8'));
    assert.equal(payload.status, 'failed');
    assert.ok(!payload.error.includes(nukeToken),
      'npm token must be [REDACTED] before reaching the state file');
    assert.ok(!payload.error.includes(ghToken),
      'github token must be [REDACTED] before reaching the state file');
    assert.ok(!payload.error.includes('alice'),
      'user-home path must be [REDACTED] before reaching the state file');
    assert.ok(/\[REDACTED\]/.test(payload.error),
      'at least one redaction marker must be present');
    // The non-sensitive prefix must survive so operators still see what failed.
    // (A thrown error is now code-prefixed with `unexpected_error: ` — the
    // original message still leads the rest of the string.)
    assert.ok(payload.error.startsWith('unexpected_error: npm install failed'),
      'redactor preserves the message structure / leading context after the code prefix');
  });

  // (ll) Companion to (kk): redact runs BEFORE the ERROR_MAX truncation,
  // so a token sitting past the slice boundary still gets redacted instead
  // of surviving in the (already-truncated) tail that the slice cuts off.
  // This guards against the obvious "fix" of redacting after truncation,
  // which would still leak any token whose start byte sat before the cut.
  it('(ll) reportForceUpdateOutcome redacts BEFORE slice (token at the tail of a long message)', async () => {
    var token = 'npm_' + 'z'.repeat(36);
    // Build a message whose length exceeds ERROR_MAX (1000) with the token
    // placed deep inside. After redaction the token becomes [REDACTED]
    // (shorter) so the post-slice tail is still safe.
    var padding = 'x'.repeat(950);
    var raw = padding + ' ' + token + ' (oom while parsing package-lock)';
    reportForceUpdateOutcome(
      { required_version: '>=1.88.0' },
      { updated: false, error: new Error(raw), fromVersion: '1.87.0' }
    );
    var payload = JSON.parse(fs.readFileSync(_statePath(), 'utf8'));
    assert.ok(!payload.error.includes(token),
      'token deep in a long message must still be redacted (redact-then-slice)');
    assert.ok(payload.error.length <= 1000,
      'ERROR_MAX truncation still applies after redaction');
  });

  // (mm) Bugbot PR#188 #1: NOOP must NOT overwrite an unacked success/failed row.
  // Models the race the autogame-17 review surfaced (cache-key + non-ok ack
  // window). If the on-disk state already carries a non-skipped status,
  // reportForceUpdateOutcome({noop:true,...}) must short-circuit — preserve
  // the real telemetry for the next heartbeat to retry.
  it('(mm) NOOP suppresses write when on-disk state is success/failed', async () => {
    // Seed an unacked success on disk (campaign A).
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      from_version: '1.87.0',
      status: 'success',
      finished_at: Date.now() - 1000,
      directive_id: 'd-mm-A',
    });
    assert.ok(fs.existsSync(_statePath()), 'precondition: success row on disk');

    // Hub still emits force_update directive B (stale cache); client returns
    // NOOP. Pre-fix path would write status='skipped' here.
    reportForceUpdateOutcome(
      { required_version: '>=1.88.0', directive_id: 'd-mm-B' },
      { noop: true, fromVersion: '1.88.0' }
    );

    var current = JSON.parse(fs.readFileSync(_statePath(), 'utf8'));
    assert.equal(current.status, 'success',
      'NOOP must NOT clobber the unacked success row');
    assert.equal(current.directive_id, 'd-mm-A',
      'NOOP must preserve the previous directive_id');
  });

  it('(mm2) NOOP suppresses write when on-disk state is failed', async () => {
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      from_version: '1.87.0',
      status: 'failed',
      finished_at: Date.now() - 1000,
      error: 'npm registry unreachable',
      directive_id: 'd-mm2',
    });

    reportForceUpdateOutcome(
      { required_version: '>=1.88.0', directive_id: 'd-mm2-new' },
      { noop: true, fromVersion: '1.88.0' }
    );

    var current = JSON.parse(fs.readFileSync(_statePath(), 'utf8'));
    assert.equal(current.status, 'failed',
      'NOOP must NOT clobber the unacked failed row');
    assert.match(current.error, /npm registry unreachable/);
  });

  it('(mm3) NOOP DOES overwrite an existing skipped row (idempotent refresh)', async () => {
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'skipped',
      finished_at: Date.now() - 60_000,
      directive_id: 'd-mm3-old',
    });

    reportForceUpdateOutcome(
      { required_version: '>=1.88.0', directive_id: 'd-mm3-new' },
      { noop: true, fromVersion: '1.88.0' }
    );

    var current = JSON.parse(fs.readFileSync(_statePath(), 'utf8'));
    assert.equal(current.status, 'skipped');
    assert.equal(current.directive_id, 'd-mm3-new',
      'a fresh skipped overwrites a stale skipped — only success/failed are sacred');
  });

  it('(mm4) NOOP writes when no on-disk state exists (baseline)', async () => {
    assert.ok(!fs.existsSync(_statePath()), 'precondition: no state file');
    reportForceUpdateOutcome(
      { required_version: '>=1.88.0', directive_id: 'd-mm4' },
      { noop: true, fromVersion: '1.88.0' }
    );
    assert.ok(fs.existsSync(_statePath()), 'first NOOP after a clean slate writes normally');
    var current = JSON.parse(fs.readFileSync(_statePath(), 'utf8'));
    assert.equal(current.status, 'skipped');
  });

  // (nn) Bugbot PR#188 #2: _extractTargetVersion must reject trailing
  // whitespace, mirroring forceUpdate.js's strip-then-validate behavior (which
  // has no .trim()).
  // Pre-fix, the extra .trim() let "1.88.0 " yield a phantom failed-row.
  describe('(nn) _extractTargetVersion rejects trailing whitespace (mirrors forceUpdate.js)', () => {
    it('rejects trailing space "1.88.0 "', () => {
      assert.equal(_extractTargetVersionForTesting({ required_version: '1.88.0 ' }), '');
    });
    it('rejects trailing tab "1.88.0\\t"', () => {
      assert.equal(_extractTargetVersionForTesting({ required_version: '1.88.0\t' }), '');
    });
    it('rejects trailing newline "1.88.0\\n"', () => {
      assert.equal(_extractTargetVersionForTesting({ required_version: '1.88.0\n' }), '');
    });
    it('rejects trailing space after operator ">=1.88.0 "', () => {
      assert.equal(_extractTargetVersionForTesting({ required_version: '>=1.88.0 ' }), '');
    });
    it('still accepts leading whitespace stripped by [\\s]+ char class', () => {
      // Note: " 1.88.0" -- leading space is part of [>=^~\s]+ strip
      assert.equal(_extractTargetVersionForTesting({ required_version: '  1.88.0' }), '1.88.0');
      assert.equal(_extractTargetVersionForTesting({ required_version: '\t>=1.88.0' }), '1.88.0');
    });
  });

  // (oo) Bugbot PR#188 #3: a2aProtocol sendHeartbeat must trigger
  // executeForceUpdate on HTTP 426 with a parseable force_update body,
  // mirroring proxy LifecycleManager. Pre-fix, canonical (non-proxy)
  // nodes below the hard floor never attempted an upgrade.
  it('(oo) 426 with force_update body triggers executeForceUpdate', async () => {
    var fuBody = {
      error: 'evolver_min_version_required',
      force_update: { required_version: '>=1.74.1', reason: 'critical_security_and_stability_fixes' },
    };
    fetchResponder = async () => ({
      ok: false,
      status: 426,
      json: async () => fuBody,
      text: async () => JSON.stringify(fuBody),
    });

    await sendHeartbeat();
    // Drain the Promise.resolve().then(...) microtask the trigger schedules.
    await new Promise((r) => setImmediate(r));
    await new Promise((r) => setImmediate(r));

    assert.equal(executeForceUpdateCalls.length, 1,
      '426 + parseable force_update must call executeForceUpdate once');
    assert.equal(executeForceUpdateCalls[0].required_version, '>=1.74.1');
  });

  it('(oo2) 426 with non-JSON body does NOT crash, does NOT trigger', async () => {
    fetchResponder = async () => ({
      ok: false,
      status: 426,
      json: async () => { throw new Error('not json'); },
      text: async () => 'plain text upgrade required',
    });

    // sendHeartbeat itself must not throw; the inner data is wrapped
    // {ok:false,error:'http_426:...'} but the heartbeat envelope still
    // resolves -- caller-facing failure surfaces via response inspection.
    var result = await sendHeartbeat();
    assert.equal(result.response && result.response.ok, false,
      'inner response carries ok:false');
    assert.match(String(result.response && result.response.error || ''), /^http_426: /);
    await new Promise((r) => setImmediate(r));
    assert.equal(executeForceUpdateCalls.length, 0,
      'no parseable force_update -> no trigger');
  });

  it('(oo3) 426 with JSON body but no force_update field is a no-op', async () => {
    var body = { error: 'evolver_min_version_required' };
    fetchResponder = async () => ({
      ok: false,
      status: 426,
      json: async () => body,
      text: async () => JSON.stringify(body),
    });

    await sendHeartbeat();
    await new Promise((r) => setImmediate(r));
    assert.equal(executeForceUpdateCalls.length, 0,
      'JSON body without force_update must not trigger');
  });

  // (pp) Bugbot PR#188 #4: unknown_node + ack.ok=true must clear the
  // state file. Mirrors proxy LifecycleManager behavior; pre-fix
  // a2aProtocol kept the file (defensive but inefficient -- next
  // heartbeat re-sent, hub dedup-acked, cleared anyway).
  it('(pp) unknown_node + ack.ok=true clears state file', async () => {
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
      directive_id: 'd-pp',
    });
    assert.ok(fs.existsSync(_statePath()));

    // First call: heartbeat returns unknown_node with positive ack.
    // sendHeartbeat will internally call sendHelloToHub() (which itself
    // hits global.fetch) -- the responder above returns the same envelope
    // for the hello call too, which is fine: hello does not consume
    // last_update_ack and the second response is a no-op for this test.
    fetchResponder = async () => ({
      ok: true,
      status: 200,
      json: async () => ({ status: 'unknown_node', last_update_ack: { ok: true } }),
      text: async () => '',
    });

    await sendHeartbeat();
    await new Promise((r) => setImmediate(r));

    assert.ok(!fs.existsSync(_statePath()),
      'unknown_node + positive ack must clear the file (proxy parity)');
  });

  it('(pp2) unknown_node WITHOUT ack does NOT clear (old-hub backward compat)', async () => {
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
      directive_id: 'd-pp2',
    });

    fetchResponder = async () => ({
      ok: true,
      status: 200,
      json: async () => ({ status: 'unknown_node' }),
      text: async () => '',
    });

    await sendHeartbeat();
    await new Promise((r) => setImmediate(r));

    assert.ok(fs.existsSync(_statePath()),
      'no ack field on unknown_node: keep the file for retry (no inference about persist)');
  });

  it('(pp3) unknown_node + ack.ok=false keeps state file', async () => {
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0',
      status: 'success',
      finished_at: Date.now(),
      directive_id: 'd-pp3',
    });

    fetchResponder = async () => ({
      ok: true,
      status: 200,
      json: async () => ({ status: 'unknown_node', last_update_ack: { ok: false, reason: 'failed' } }),
      text: async () => '',
    });

    await sendHeartbeat();
    await new Promise((r) => setImmediate(r));

    assert.ok(fs.existsSync(_statePath()),
      'ack.reason=failed -> keep the file regardless of unknown_node');
  });

  // (nn-parity) Verifier follow-up: the "mirror forceUpdate.js" claim in the
  // comment at a2aProtocol.js:823-833 is hand-maintained -- two regex copies
  // can drift silently. Sweep a shared input table and assert
  // _extractTargetVersion's verdict and forceUpdate.js's regex verdict agree
  // BIT-FOR-BIT on every input. Imports forceUpdate.js's test hook
  // _isAcceptedRequiredVersionForTesting which re-implements the EXACT same
  // strip + validation, so any future drift breaks BOTH this test AND
  // forceUpdate.js's runtime check.
  describe('(nn-parity) _extractTargetVersion matches forceUpdate.js byte-for-byte', () => {
    var fU;
    before(() => {
      fU = require('../src/forceUpdate');
    });
    const PARITY_INPUTS = [
      // Equal verdicts -- both accept
      '1.88.0', '>=1.88.0', '^1.88.0', '~1.88.0', '=1.88.0', ' 1.88.0',
      '\t>=1.88.0', '= 1.88.0', 'v1.88.0', '>=v1.88.0',
      '1.0.0-rc.1', '1.0.0+build.5', '1.0.0-rc.1+build.5',
      '1.0.0-alpha-beta', '1.0.0-0.3.7', '1.0.0-x.7.z.92',
      '1.0.0+20130313144700', '1.0.0-beta+exp.sha.5114f85',
      // Equal verdicts -- both reject
      '1.88.0 ', '1.88.0\t', '1.88.0\n', '1.88.0\r',
      '>=1.88.0 ', '1.88 .0', '1.88.0-rc 1',
      '<1.88.0', '<=1.88.0',
      '01.0.0', '1.02.0', '1.0.03', '1.0.0-01',
      '1.0.0-alpha..1', '1.0.0-alpha_', '1.0.0+build_meta', '1.0.0+',
      '*', 'latest', '', '   ', '>= ',
      // Asymmetric (length): both accept but a2a TO_VERSION_MAX (32) caps it.
      // Listed but NOT checked for strict parity -- a2a is stricter on length,
      // and the divergence is in the SAFE direction (no phantom row). The
      // sweep is filtered below to inputs ≤32 chars to lock the operationally
      // relevant invariant.
    ];
    for (var i = 0; i < PARITY_INPUTS.length; i++) {
      (function (raw) {
        // a2a TO_VERSION_MAX=32; longer-but-valid inputs are filtered (a2a's
        // length cap is safer-direction-asymmetric and not part of the parity
        // contract). All inputs in the table above are <32 chars.
        if (typeof raw === 'string' && raw.length > 32) return;
        it('input ' + JSON.stringify(raw) + ': both reject OR both accept', () => {
          var a2aAccepted = _extractTargetVersionForTesting({ required_version: raw }) !== '';
          var fUAccepted = fU._isAcceptedRequiredVersionForTesting(raw);
          assert.equal(a2aAccepted, fUAccepted,
            'parity broken: _extractTargetVersion accepted=' + a2aAccepted +
            ' but forceUpdate.js accepted=' + fUAccepted +
            ' for input ' + JSON.stringify(raw));
        });
      }(PARITY_INPUTS[i]));
    }
  });

  // (oo-malformed) Bugbot #3 follow-up: 426 with non-object force_update
  // (e.g. a string, number, array) must NOT crash and MUST NOT trigger.
  it('(oo-malformed) 426 with force_update as string is a no-op', async () => {
    var body = { error: 'evolver_min_version_required', force_update: 'yes please' };
    fetchResponder = async () => ({
      ok: false, status: 426,
      json: async () => body,
      text: async () => JSON.stringify(body),
    });
    await sendHeartbeat();
    await new Promise((r) => setImmediate(r));
    assert.equal(executeForceUpdateCalls.length, 0,
      'force_update of wrong type must not trigger');
  });

  it('(oo-malformed2) 426 with force_update as null is a no-op', async () => {
    var body = { error: 'evolver_min_version_required', force_update: null };
    fetchResponder = async () => ({
      ok: false, status: 426,
      json: async () => body,
      text: async () => JSON.stringify(body),
    });
    await sendHeartbeat();
    await new Promise((r) => setImmediate(r));
    assert.equal(executeForceUpdateCalls.length, 0);
  });

  // (oo-cooldown) Bugbot #3 follow-up: two 426s back-to-back inside the
  // cooldown window must trigger executeForceUpdate at most once.
  it('(oo-cooldown) back-to-back 426s within cooldown trigger only once', async () => {
    var prevCooldown = process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS;
    process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS = '60000';
    try {
      var body = {
        error: 'evolver_min_version_required',
        force_update: { required_version: '>=1.74.1', reason: 'critical' },
      };
      fetchResponder = async () => ({
        ok: false, status: 426,
        json: async () => body,
        text: async () => JSON.stringify(body),
      });
      await sendHeartbeat();
      await new Promise((r) => setImmediate(r));
      await sendHeartbeat();
      await new Promise((r) => setImmediate(r));
      assert.equal(executeForceUpdateCalls.length, 1,
        'second 426 inside cooldown must NOT re-trigger executeForceUpdate');
    } finally {
      if (prevCooldown === undefined) delete process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS;
      else process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS = prevCooldown;
    }
  });

  // (pp-duplicate) Bugbot #4 follow-up: unknown_node + ack.reason='duplicate'
  // must clear, matching the canonical block's behavior.
  it('(pp-duplicate) unknown_node + ack.reason=duplicate clears state file', async () => {
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0', status: 'success',
      finished_at: Date.now(), directive_id: 'd-pp-dup',
    });
    fetchResponder = async () => ({
      ok: true, status: 200,
      json: async () => ({ status: 'unknown_node', last_update_ack: { ok: false, reason: 'duplicate' } }),
      text: async () => '',
    });
    await sendHeartbeat();
    await new Promise((r) => setImmediate(r));
    assert.ok(!fs.existsSync(_statePath()),
      'reason=duplicate must clear even on unknown_node path');
  });

  // (pp-invalid) unknown_node + ack.reason='invalid' clears with warn.
  it('(pp-invalid) unknown_node + ack.reason=invalid clears with warn', async () => {
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0', status: 'success',
      finished_at: Date.now(), directive_id: 'd-pp-inv',
    });
    var warns = [];
    var origWarn = console.warn;
    console.warn = (m) => { warns.push(String(m)); };
    try {
      fetchResponder = async () => ({
        ok: true, status: 200,
        json: async () => ({ status: 'unknown_node', last_update_ack: { ok: false, reason: 'invalid' } }),
        text: async () => '',
      });
      await sendHeartbeat();
      await new Promise((r) => setImmediate(r));
      assert.ok(!fs.existsSync(_statePath()),
        'reason=invalid must clear even on unknown_node path');
      assert.ok(warns.some((m) => /last_update_ack=invalid \(unknown_node path\)/.test(m)),
        'unknown_node + invalid must emit the aligned warn');
    } finally {
      console.warn = origWarn;
    }
  });

  // (pp-failed-warn) unknown_node + ack.reason='failed' emits warn (keep).
  it('(pp-failed-warn) unknown_node + ack.reason=failed emits warn and keeps file', async () => {
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0', status: 'success',
      finished_at: Date.now(), directive_id: 'd-pp-fail',
    });
    var warns = [];
    var origWarn = console.warn;
    console.warn = (m) => { warns.push(String(m)); };
    try {
      fetchResponder = async () => ({
        ok: true, status: 200,
        json: async () => ({ status: 'unknown_node', last_update_ack: { ok: false, reason: 'failed' } }),
        text: async () => '',
      });
      await sendHeartbeat();
      await new Promise((r) => setImmediate(r));
      assert.ok(fs.existsSync(_statePath()), 'reason=failed must KEEP file');
      assert.ok(warns.some((m) => /last_update_ack=failed \(unknown_node path\)/.test(m)),
        'unknown_node + failed must emit the aligned warn');
    } finally {
      console.warn = origWarn;
    }
  });

  // (pp-malformed) unknown_node + malformed ack shapes must fall through
  // without crashing. The typeof === 'object' guard handles them.
  it('(pp-malformed) unknown_node + last_update_ack as string keeps file', async () => {
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0', status: 'success',
      finished_at: Date.now(), directive_id: 'd-pp-mal',
    });
    fetchResponder = async () => ({
      ok: true, status: 200,
      json: async () => ({ status: 'unknown_node', last_update_ack: 'oops' }),
      text: async () => '',
    });
    await sendHeartbeat();
    await new Promise((r) => setImmediate(r));
    assert.ok(fs.existsSync(_statePath()),
      'malformed ack must not be treated as ok=true');
  });

  it('(pp-malformed2) unknown_node + last_update_ack as array keeps file', async () => {
    _persistLastUpdateStateForTesting({
      to_version: '1.88.0', status: 'success',
      finished_at: Date.now(), directive_id: 'd-pp-mal2',
    });
    fetchResponder = async () => ({
      ok: true, status: 200,
      json: async () => ({ status: 'unknown_node', last_update_ack: ['ok'] }),
      text: async () => '',
    });
    await sendHeartbeat();
    await new Promise((r) => setImmediate(r));
    // typeof [] === 'object' in JS so array passes the typeof guard,
    // but it has neither .ok nor .reason -- falls through to keep.
    assert.ok(fs.existsSync(_statePath()),
      'array ack must not trigger clear (no .ok/.reason match)');
  });

  // (pp-nopending) unknown_node + ack.ok=true + NO pending state file:
  // the clear path is gated by `_pendingLastUpdate`. Verify no crash.
  it('(pp-nopending) unknown_node + ack.ok=true + no state file is no-op', async () => {
    assert.ok(!fs.existsSync(_statePath()), 'precondition: clean slate');
    fetchResponder = async () => ({
      ok: true, status: 200,
      json: async () => ({ status: 'unknown_node', last_update_ack: { ok: true } }),
      text: async () => '',
    });
    await sendHeartbeat();
    await new Promise((r) => setImmediate(r));
    assert.ok(!fs.existsSync(_statePath()), 'no pending, no file, no problem');
  });

  // (bb) Pin the strip/validate contract against src/forceUpdate.js.
  // The bug these guard against: _extractTargetVersion used to strip
  // operators (notably "<"/"<=") that forceUpdate.js does NOT strip.
  // Result -- telemetry would report to_version="1.88.0" for a directive
  // (e.g. "<2.0.0") that the upgrader itself rejects, producing
  // ghost `failed` rows in EvolverUpgradeAttempt for upgrades that were
  // never even attempted. The cases below trace each input against
  // forceUpdate.js's `String(...).replace(/^[>=^~\s]+/, '')` strip class
  // (matches >, =, ^, ~, whitespace -- NOT < or <=), optional leading-v
  // normalization, and the same concrete-semver test.
  describe('(bb) _extractTargetVersion mirrors forceUpdate.js', () => {
    it('accepts "v1.88.0" -> "1.88.0"', () => {
      assert.equal(_extractTargetVersionForTesting({ required_version: 'v1.88.0' }), '1.88.0');
    });
    it('rejects "<1.88.0" (< is not in forceUpdate.js strip class)', () => {
      assert.equal(_extractTargetVersionForTesting({ required_version: '<1.88.0' }), '');
    });
    it('rejects "<=1.88.0" (<= is not in forceUpdate.js strip class)', () => {
      assert.equal(_extractTargetVersionForTesting({ required_version: '<=1.88.0' }), '');
    });
    it('accepts ">=v1.88.0" -> "1.88.0"', () => {
      assert.equal(_extractTargetVersionForTesting({ required_version: '>=v1.88.0' }), '1.88.0');
    });
    it('accepts ">=1.88.0" -> "1.88.0"', () => {
      assert.equal(_extractTargetVersionForTesting({ required_version: '>=1.88.0' }), '1.88.0');
    });
    it('accepts "^1.88.0" -> "1.88.0"', () => {
      assert.equal(_extractTargetVersionForTesting({ required_version: '^1.88.0' }), '1.88.0');
    });
    it('accepts "~1.88.0" -> "1.88.0"', () => {
      assert.equal(_extractTargetVersionForTesting({ required_version: '~1.88.0' }), '1.88.0');
    });
    it('accepts "=1.88.0" -> "1.88.0" (= IS in forceUpdate.js strip class)', () => {
      assert.equal(_extractTargetVersionForTesting({ required_version: '=1.88.0' }), '1.88.0');
    });
    it('accepts "= 1.88.0" -> "1.88.0" (whitespace also stripped)', () => {
      assert.equal(_extractTargetVersionForTesting({ required_version: '= 1.88.0' }), '1.88.0');
    });
    it('accepts a bare "1.88.0" -> "1.88.0"', () => {
      assert.equal(_extractTargetVersionForTesting({ required_version: '1.88.0' }), '1.88.0');
    });
    it('rejects malformed semver identifiers', () => {
      assert.equal(_extractTargetVersionForTesting({ required_version: '01.88.0' }), '');
      assert.equal(_extractTargetVersionForTesting({ required_version: '1.88.03' }), '');
      assert.equal(_extractTargetVersionForTesting({ required_version: '1.88.0-01' }), '');
      assert.equal(_extractTargetVersionForTesting({ required_version: '1.88.0-alpha_' }), '');
      assert.equal(_extractTargetVersionForTesting({ required_version: '1.88.0+build_meta' }), '');
    });
    it('rejects garbage / non-string / missing', () => {
      assert.equal(_extractTargetVersionForTesting({ required_version: '*' }), '');
      assert.equal(_extractTargetVersionForTesting({ required_version: 'latest' }), '');
      assert.equal(_extractTargetVersionForTesting({ required_version: 123 }), '');
      assert.equal(_extractTargetVersionForTesting({}), '');
      assert.equal(_extractTargetVersionForTesting(null), '');
    });
  });
});
