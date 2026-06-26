const { describe, it, before, after, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

// Verifies the idempotency short-circuit added to executeForceUpdate:
// when the running install is already at the required version, the function
// returns the FORCE_UPDATE_NOOP sentinel (NOT `true`) without invoking
// degit/cpSync. This prevents two distinct bugs:
//   1. transient Channel 1 failures (npx unavailable, network blip, EBUSY)
//      from overwriting a previous successful run's state file with a bogus
//      "failed" entry on the hub's repeated post-restart re-trigger.
//   2. (H2 follow-up) phantom {status:"success", from_version==to_version}
//      rows in EvolverUpgradeAttempt + gratuitous process.exit(78) restarts
//      that callers like enrich.js / a2aProtocol.js previously fired off
//      whenever executeForceUpdate returned anything truthy.

const childProcess = require('child_process');
const origExecFileSync = childProcess.execFileSync;

const forceUpdateModPath = require.resolve('../src/forceUpdate');
const pathsModPath = require.resolve('../src/gep/paths');

let installRoot;

function freshRequireForceUpdate(execFileStub) {
  delete require.cache[forceUpdateModPath];
  require.cache[pathsModPath] = {
    id: pathsModPath, filename: pathsModPath, loaded: true,
    exports: { getEvolverInstallRoot: () => installRoot },
  };
  childProcess.execFileSync = execFileStub;
  const mod = require('../src/forceUpdate');
  childProcess.execFileSync = origExecFileSync;
  return mod;
}

function writeInstallPkg(version) {
  fs.writeFileSync(
    path.join(installRoot, 'package.json'),
    JSON.stringify({ name: '@evomap/evolver', version }),
    'utf8',
  );
}

describe('executeForceUpdate: idempotency short-circuit', () => {
  before(() => {
    installRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-fu-idem-'));
  });

  after(() => {
    childProcess.execFileSync = origExecFileSync;
    delete require.cache[pathsModPath];
    delete require.cache[forceUpdateModPath];
    try { fs.rmSync(installRoot, { recursive: true, force: true }); } catch (_) {}
  });

  beforeEach(() => {
    // Reset install dir between tests so a wipe in one test doesn't bleed.
    try { fs.rmSync(installRoot, { recursive: true, force: true }); } catch (_) {}
    fs.mkdirSync(installRoot, { recursive: true });
  });

  it('exact match: returns FORCE_UPDATE_NOOP sentinel without invoking degit', () => {
    writeInstallPkg('1.88.0');
    let execFileCalls = 0;
    const stub = function () {
      execFileCalls++;
      throw new Error('degit must not be invoked when already at required version');
    };
    const { executeForceUpdate, FORCE_UPDATE_NOOP } = freshRequireForceUpdate(stub);

    const result = executeForceUpdate({ required_version: '1.88.0' });

    assert.equal(result, FORCE_UPDATE_NOOP, 'returns FORCE_UPDATE_NOOP sentinel on no-op');
    assert.notEqual(result, true,
      'must NOT return `true` — callers would misread that as a real success');
    assert.equal(typeof FORCE_UPDATE_NOOP, 'symbol',
      'sentinel must be a Symbol (===-comparable, no accidental truthy collisions)');
    assert.equal(execFileCalls, 0, 'degit (execFileSync) must NOT be called');
  });

  it('range form ">=1.88.0" with current 1.88.0: returns FORCE_UPDATE_NOOP after operator strip', () => {
    writeInstallPkg('1.88.0');
    let execFileCalls = 0;
    const stub = function () {
      execFileCalls++;
      throw new Error('degit must not be invoked when already at required version');
    };
    const { executeForceUpdate, FORCE_UPDATE_NOOP } = freshRequireForceUpdate(stub);

    const result = executeForceUpdate({ required_version: '>=1.88.0' });

    assert.equal(result, FORCE_UPDATE_NOOP, 'returns FORCE_UPDATE_NOOP after operator strip matches');
    assert.equal(execFileCalls, 0, 'degit (execFileSync) must NOT be called');
  });

  it('newer current version: returns FORCE_UPDATE_NOOP and does not downgrade', () => {
    writeInstallPkg('1.88.4');
    let execFileCalls = 0;
    const stub = function () {
      execFileCalls++;
      throw new Error('degit must not be invoked when current version is newer than required');
    };
    const { executeForceUpdate, FORCE_UPDATE_NOOP } = freshRequireForceUpdate(stub);

    const result = executeForceUpdate({ required_version: '>=1.88.3' });

    assert.equal(result, FORCE_UPDATE_NOOP, 'newer current version satisfies the force-update floor');
    assert.equal(execFileCalls, 0, 'degit (execFileSync) must NOT be called, avoiding downgrade');
  });

  it('newer current version with bare stale required version: returns FORCE_UPDATE_NOOP', () => {
    writeInstallPkg('1.88.4');
    let execFileCalls = 0;
    const stub = function () {
      execFileCalls++;
      throw new Error('degit must not be invoked when current version is newer than bare required');
    };
    const { executeForceUpdate, FORCE_UPDATE_NOOP } = freshRequireForceUpdate(stub);

    const result = executeForceUpdate({ required_version: '1.88.3' });

    assert.equal(result, FORCE_UPDATE_NOOP, 'bare stale required_version is also a minimum floor');
    assert.equal(execFileCalls, 0, 'degit (execFileSync) must NOT be called, avoiding downgrade');
  });

  it('newer current version with leading v: normalizes and does not downgrade', () => {
    writeInstallPkg('v1.88.4');
    let execFileCalls = 0;
    const stub = function () {
      execFileCalls++;
      throw new Error('degit must not be invoked when normalized current is newer than required');
    };
    const { executeForceUpdate, FORCE_UPDATE_NOOP } = freshRequireForceUpdate(stub);

    const result = executeForceUpdate({ required_version: '>=1.88.3' });

    assert.equal(result, FORCE_UPDATE_NOOP, 'leading-v current version satisfies the force-update floor');
    assert.equal(execFileCalls, 0, 'degit (execFileSync) must NOT be called, avoiding downgrade');
  });

  it('required version with leading v: normalizes and still upgrades older installs', () => {
    writeInstallPkg('1.88.2');
    let execFileCalls = 0;
    const stub = function () {
      execFileCalls++;
      throw new Error('simulated degit failure');
    };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);

    const result = executeForceUpdate({ required_version: '>=v1.88.3' });

    assert.equal(result.ok, false, 'older current version must not skip a leading-v required floor');
    assert.equal(result.code, 'degit_failed', 'degit throw classified as degit_failed');
    assert.equal(execFileCalls, 1, 'Channel 1 (degit) was attempted exactly once');
  });

  it('newer prerelease with hyphen identifier: returns FORCE_UPDATE_NOOP and does not downgrade', () => {
    writeInstallPkg('1.88.4-alpha-1');
    let execFileCalls = 0;
    const stub = function () {
      execFileCalls++;
      throw new Error('degit must not be invoked when hyphenated prerelease current is newer');
    };
    const { executeForceUpdate, FORCE_UPDATE_NOOP } = freshRequireForceUpdate(stub);

    const result = executeForceUpdate({ required_version: '>=1.88.3' });

    assert.equal(result, FORCE_UPDATE_NOOP, 'newer hyphenated prerelease satisfies the force-update floor');
    assert.equal(execFileCalls, 0, 'degit (execFileSync) must NOT be called, avoiding downgrade');
  });

  it('newer prerelease current version: compares numeric prerelease identifiers', () => {
    writeInstallPkg('1.88.0-rc.10');
    let execFileCalls = 0;
    const stub = function () {
      execFileCalls++;
      throw new Error('degit must not be invoked when prerelease current is newer than required');
    };
    const { executeForceUpdate, FORCE_UPDATE_NOOP } = freshRequireForceUpdate(stub);

    const result = executeForceUpdate({ required_version: '>=1.88.0-rc.2' });

    assert.equal(result, FORCE_UPDATE_NOOP, 'rc.10 satisfies an rc.2 force-update floor');
    assert.equal(execFileCalls, 0, 'degit (execFileSync) must NOT be called');
  });

  it('older prerelease current version: compares oversized numeric identifiers without Number precision loss', () => {
    writeInstallPkg('1.0.0-9007199254740992');
    let execFileCalls = 0;
    const stub = function () {
      execFileCalls++;
      throw new Error('simulated degit failure');
    };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);

    const result = executeForceUpdate({ required_version: '>=1.0.0-9007199254740993' });

    assert.equal(result.ok, false, 'older oversized prerelease must fall through to the upgrade path');
    assert.equal(result.code, 'degit_failed', 'degit throw classified as degit_failed');
    assert.equal(execFileCalls, 1, 'Channel 1 (degit) was attempted exactly once');
  });

  it('older current version: compares oversized major/minor/patch without Number precision loss', () => {
    const cases = [
      [
        '9007199254740992.9007199254740992.9007199254740992',
        '>=9007199254740993.9007199254740992.9007199254740992',
      ],
      [
        '9007199254740992.9007199254740992.9007199254740992',
        '>=9007199254740992.9007199254740993.9007199254740992',
      ],
      [
        '9007199254740992.9007199254740992.9007199254740992',
        '>=9007199254740992.9007199254740992.9007199254740993',
      ],
    ];

    for (const [currentVersion, requiredVersion] of cases) {
      writeInstallPkg(currentVersion);
      let execFileCalls = 0;
      const stub = function () {
        execFileCalls++;
        throw new Error('simulated degit failure');
      };
      const { executeForceUpdate } = freshRequireForceUpdate(stub);

      const result = executeForceUpdate({ required_version: requiredVersion });

      assert.equal(result.ok, false, 'older oversized core semver must fall through to the upgrade path');
      assert.equal(result.code, 'degit_failed', 'degit throw classified as degit_failed');
      assert.equal(execFileCalls, 1, 'Channel 1 (degit) was attempted exactly once');
    }
  });

  it('stable current version satisfies a prerelease floor', () => {
    writeInstallPkg('1.88.0');
    let execFileCalls = 0;
    const stub = function () {
      execFileCalls++;
      throw new Error('degit must not be invoked when stable current satisfies prerelease floor');
    };
    const { executeForceUpdate, FORCE_UPDATE_NOOP } = freshRequireForceUpdate(stub);

    const result = executeForceUpdate({ required_version: '>=1.88.0-rc.5' });

    assert.equal(result, FORCE_UPDATE_NOOP, 'stable release is newer than its prerelease');
    assert.equal(execFileCalls, 0, 'degit (execFileSync) must NOT be called');
  });

  it('version mismatch: falls through to normal upgrade path', () => {
    writeInstallPkg('1.87.5');
    let execFileCalls = 0;
    // Simulate degit failure so we can confirm the upgrade path was entered
    // without actually performing fs replacement. If the short-circuit
    // wrongly returned true, execFileCalls would remain 0 AND the result
    // would be true. If it correctly falls through, execFileCalls > 0
    // (Channel 1 attempt) and the function returns false (degit failed).
    const stub = function () {
      execFileCalls++;
      throw new Error('simulated degit failure');
    };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);

    const result = executeForceUpdate({ required_version: '1.88.0' });

    assert.equal(result.ok, false, 'no short-circuit; degit failure -> structured failure');
    assert.equal(result.code, 'degit_failed', 'degit throw classified as degit_failed');
    assert.equal(execFileCalls, 1, 'Channel 1 (degit) was attempted exactly once');
  });

  it('prerelease below stable floor: falls through to normal upgrade path', () => {
    writeInstallPkg('1.88.0-rc.5');
    let execFileCalls = 0;
    const stub = function () {
      execFileCalls++;
      throw new Error('simulated degit failure');
    };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);

    const result = executeForceUpdate({ required_version: '>=1.88.0' });

    assert.equal(result.ok, false, 'prerelease must not satisfy stable force-update floor');
    assert.equal(result.code, 'degit_failed', 'degit throw classified as degit_failed');
    assert.equal(execFileCalls, 1, 'Channel 1 (degit) was attempted exactly once');
  });

  it('malformed current version: does not satisfy a lower-looking force-update floor', () => {
    writeInstallPkg('1.88.04');
    let execFileCalls = 0;
    const stub = function () {
      execFileCalls++;
      throw new Error('simulated degit failure');
    };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);

    const result = executeForceUpdate({ required_version: '>=1.88.3' });

    assert.equal(result.ok, false, 'invalid current version must fail closed');
    assert.equal(result.code, 'current_version_unparsable',
      'unparseable installed version → current_version_unparsable (the new #213 anti-downgrade guard branch)');
    assert.equal(execFileCalls, 0, 'Channel 1 (degit) must NOT be attempted with invalid current version');
  });

  it('garbage required_version: parse failure, no short-circuit, returns false', () => {
    // If the current version happened to equal the unparsed garbage string,
    // we still must NOT short-circuit because the validator rejects it first.
    writeInstallPkg('1.88.0');
    let execFileCalls = 0;
    const stub = function () {
      execFileCalls++;
      throw new Error('degit must not be invoked when required_version is garbage');
    };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);

    const result = executeForceUpdate({ required_version: 'garbage' });

    assert.equal(result.ok, false, 'parse failure must return a structured failure');
    assert.equal(result.code, 'bad_required_version', 'garbage required_version → bad_required_version');
    assert.equal(execFileCalls, 0, 'execFileSync never reached (rejected before Channel 1)');
  });
});

// ---------------------------------------------------------------------------
// H2 follow-up: no-op MUST persist status="skipped" (not "success"), MUST omit
// from_version (so EvolverUpgradeAttempt does not record a phantom
// from_version == to_version row), and MUST NOT trigger process.exit(78).
//
// Verified end-to-end via the heartbeat-trigger path because that is where the
// bug manifests in production: heartbeat -> _maybeTriggerForceUpdateFromHeartbeat
// -> executeForceUpdate -> reportForceUpdateOutcome -> (maybe) exit(78).
// ---------------------------------------------------------------------------

describe('executeForceUpdate no-op: telemetry + exit-suppression', () => {
  // Defer require()s until inside the test so we can swap forceUpdate first.
  const forceUpdatePath = require.resolve('../src/forceUpdate');
  const a2aProtocolPath = require.resolve('../src/gep/a2aProtocol');

  var tmpDir;
  var evomapHomeDir;
  var origHubUrl;
  var origLogsDir;
  var origEvolverHome;
  var origInsecure;
  var origFetch;
  var origExit;

  // executeForceUpdate spy controls + recorded calls.
  var execReturn;
  var execCalls;

  function loadProtocolWithSpy() {
    // Rig the require cache so a2aProtocol picks up our spy executeForceUpdate
    // instead of the real one. Mirrors the approach used in
    // forceUpdateLastUpdateReport.test.js (see top-of-file cache rig there).
    delete require.cache[a2aProtocolPath];
    const realFU = require('../src/forceUpdate');
    require.cache[forceUpdatePath] = {
      id: forceUpdatePath,
      filename: forceUpdatePath,
      loaded: true,
      exports: {
        executeForceUpdate: function (fu) {
          execCalls.push(fu);
          // For no-op tests, return realFU.FORCE_UPDATE_NOOP — that's what the
          // real implementation would return when current === required.
          if (execReturn === '__NOOP__') return realFU.FORCE_UPDATE_NOOP;
          return execReturn;
        },
        FORCE_UPDATE_NOOP: realFU.FORCE_UPDATE_NOOP,
      },
    };
    return require('../src/gep/a2aProtocol');
  }

  before(() => {
    if (!process.env.A2A_NODE_SECRET) process.env.A2A_NODE_SECRET = 'a'.repeat(64);
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-fu-noop-'));
    evomapHomeDir = path.join(tmpDir, 'evomap-home');
    fs.mkdirSync(evomapHomeDir, { recursive: true });

    origHubUrl = process.env.A2A_HUB_URL;
    origLogsDir = process.env.EVOLVER_LOGS_DIR;
    origEvolverHome = process.env.EVOLVER_HOME;
    origInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    process.env.A2A_HUB_URL = 'http://localhost:19998';
    process.env.EVOLVER_LOGS_DIR = tmpDir;
    process.env.EVOLVER_HOME = evomapHomeDir;
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';

    origFetch = global.fetch;
    origExit = process.exit;
  });

  after(() => {
    global.fetch = origFetch;
    process.exit = origExit;
    if (origHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = origHubUrl;
    if (origLogsDir === undefined) delete process.env.EVOLVER_LOGS_DIR;
    else process.env.EVOLVER_LOGS_DIR = origLogsDir;
    if (origEvolverHome === undefined) delete process.env.EVOLVER_HOME;
    else process.env.EVOLVER_HOME = origEvolverHome;
    if (origInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = origInsecure;
    delete require.cache[a2aProtocolPath];
    delete require.cache[forceUpdatePath];
    try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
  });

  beforeEach(() => {
    execCalls = [];
    execReturn = '__NOOP__';
    process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS = '0';
  });

  it('reportForceUpdateOutcome(noop:true) writes status="skipped" with no from_version', () => {
    const a2a = loadProtocolWithSpy();
    const statePath = a2a._testing._getLastUpdateStatePathForTesting();
    a2a._testing._resetLastUpdateStateForTesting();
    try { fs.unlinkSync(statePath); } catch (_) {}

    a2a.reportForceUpdateOutcome(
      { required_version: '>=1.88.0', directive_id: 'd-noop' },
      { updated: false, noop: true, fromVersion: '1.88.0' }
    );

    assert.ok(fs.existsSync(statePath), 'state file persisted for no-op');
    const payload = JSON.parse(fs.readFileSync(statePath, 'utf8'));
    assert.equal(payload.status, 'skipped',
      'no-op MUST be persisted as "skipped" (hub schema enum), NOT "success"');
    assert.equal(payload.to_version, '1.88.0', 'to_version still required by hub schema');
    assert.equal(payload.from_version, undefined,
      'from_version OMITTED for no-op (avoids phantom from_version == to_version row)');
    assert.equal(payload.error, undefined, 'no error on no-op');
    assert.equal(payload.directive_id, 'd-noop');
    assert.equal(typeof payload.finished_at, 'number');
  });

  it('reportForceUpdateOutcome: noop wins over updated (defensive)', () => {
    // If both flags are accidentally set (regression in caller logic), the
    // status must still be "skipped" — we never want a phantom "success" row.
    const a2a = loadProtocolWithSpy();
    const statePath = a2a._testing._getLastUpdateStatePathForTesting();
    a2a._testing._resetLastUpdateStateForTesting();
    try { fs.unlinkSync(statePath); } catch (_) {}

    a2a.reportForceUpdateOutcome(
      { required_version: '>=1.88.0' },
      { updated: true, noop: true, fromVersion: '1.88.0' }
    );

    const payload = JSON.parse(fs.readFileSync(statePath, 'utf8'));
    assert.equal(payload.status, 'skipped', 'noop overrides updated to prevent phantom success');
    assert.equal(payload.from_version, undefined, 'still omits from_version');
  });

  it('reportForceUpdateOutcome(updated:true) still writes status="success" with from_version (regression guard)', () => {
    const a2a = loadProtocolWithSpy();
    const statePath = a2a._testing._getLastUpdateStatePathForTesting();
    a2a._testing._resetLastUpdateStateForTesting();
    try { fs.unlinkSync(statePath); } catch (_) {}

    a2a.reportForceUpdateOutcome(
      { required_version: '>=1.88.0', directive_id: 'd-ok' },
      { updated: true, fromVersion: '1.87.0' }
    );

    const payload = JSON.parse(fs.readFileSync(statePath, 'utf8'));
    assert.equal(payload.status, 'success');
    assert.equal(payload.to_version, '1.88.0');
    assert.equal(payload.from_version, '1.87.0',
      'real upgrade keeps from_version so hub can render the transition');
  });

  it('heartbeat-trigger: no-op short-circuit persists "skipped" and does NOT call process.exit(78)', async () => {
    execReturn = '__NOOP__';
    const a2a = loadProtocolWithSpy();
    // Touch getNodeId BEFORE reading statePath: _shortNodeIdForStatePath uses
    // the cached node_id once it exists, and sendHeartbeat creates the
    // node_id file. Without this, the pre-heartbeat statePath uses 'anon'
    // while the post-heartbeat persist writes to a hex-suffixed path,
    // making the existsSync check look at the wrong file.
    a2a.getNodeId();
    const statePath = a2a._testing._getLastUpdateStatePathForTesting();
    a2a._testing._resetLastUpdateStateForTesting();
    a2a._testing._resetForceUpdateStateForTesting();
    try { fs.unlinkSync(statePath); } catch (_) {}

    const exitCalls = [];
    process.exit = function (code) { exitCalls.push(code); };
    global.fetch = async function (_url, opts) {
      // First call: heartbeat. Hand back a force_update directive so
      // _maybeTriggerForceUpdateFromHeartbeat fires.
      return {
        ok: true,
        status: 200,
        json: async () => ({
          status: 'ok',
          force_update: {
            required_version: '>=1.88.0',
            directive_id: 'd-noop-hb',
            reason: 'test',
          },
        }),
        text: async () => '',
      };
    };

    await a2a.sendHeartbeat();
    // Drain the microtask the trigger schedules (Promise.resolve().then(...)).
    await new Promise(r => setImmediate(r));

    assert.equal(execCalls.length, 1, 'executeForceUpdate invoked exactly once');
    assert.equal(exitCalls.length, 0,
      'process.exit(78) MUST NOT be called for a no-op — nothing to restart for');
    assert.ok(fs.existsSync(statePath), 'no-op still writes telemetry');
    const payload = JSON.parse(fs.readFileSync(statePath, 'utf8'));
    assert.equal(payload.status, 'skipped');
    assert.equal(payload.from_version, undefined);
  });

  it('heartbeat-trigger: real success (true) still calls process.exit(78) (regression guard)', async () => {
    execReturn = true;
    const a2a = loadProtocolWithSpy();
    a2a.getNodeId();
    const statePath = a2a._testing._getLastUpdateStatePathForTesting();
    a2a._testing._resetLastUpdateStateForTesting();
    a2a._testing._resetForceUpdateStateForTesting();
    try { fs.unlinkSync(statePath); } catch (_) {}

    const exitCalls = [];
    process.exit = function (code) { exitCalls.push(code); };
    global.fetch = async function () {
      return {
        ok: true,
        status: 200,
        json: async () => ({
          status: 'ok',
          force_update: { required_version: '>=1.88.0', directive_id: 'd-ok-hb', reason: 'test' },
        }),
        text: async () => '',
      };
    };

    await a2a.sendHeartbeat();
    await new Promise(r => setImmediate(r));

    assert.equal(exitCalls.length, 1, 'real success still triggers restart');
    assert.equal(exitCalls[0], 78);
    const payload = JSON.parse(fs.readFileSync(statePath, 'utf8'));
    assert.equal(payload.status, 'success');
  });
});
