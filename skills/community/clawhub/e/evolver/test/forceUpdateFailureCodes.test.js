const { describe, it, before, after, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

// Verifies the structured failure taxonomy added to executeForceUpdate.
//
// Historically every failing branch of _executeForceUpdateInner returned a
// bare `false`, so the only thing that ever reached the hub (and thus the
// EvolverUpgradeAttempt table) was the literal string "executeForceUpdate
// returned false" — degit-missing, tag-404, version mismatch and copy-EPERM
// were all indistinguishable. Each branch now returns
// { ok:false, code, detail }; this test pins each branch to its code so a
// future refactor can't silently collapse them back into one bucket.
//
// Harness mirrors forceUpdateKeepList.test.js: forceUpdate.js destructures
// `execFileSync` at module-load, so we mutate child_process.execFileSync
// before each fresh require, and we point getEvolverInstallRoot at a temp dir.

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

// Write the install-root package.json. name defaults to the real package name
// so the install-guard passes; override it to exercise the guard.
function writeInstallPkg(version, name) {
  fs.writeFileSync(
    path.join(installRoot, 'package.json'),
    JSON.stringify({ name: name || '@evomap/evolver', version }),
    'utf8',
  );
}

// Fake degit that "downloads" a package.json (+ a code file) of the given
// version into TMP_TARGET (the last positional arg degit receives).
function makeSuccessfulDegit(version) {
  return function (_bin, args) {
    const tmpTarget = args[args.length - 1];
    fs.mkdirSync(tmpTarget, { recursive: true });
    fs.writeFileSync(
      path.join(tmpTarget, 'package.json'),
      JSON.stringify({ name: '@evomap/evolver', version }),
      'utf8',
    );
    fs.writeFileSync(path.join(tmpTarget, 'index.js'), '// v' + version, 'utf8');
  };
}

// Like makeSuccessfulDegit, but the "downloaded" package.json is parseable yet
// carries NO version field. Exercises the post-download branch where
// `tmpPkg.version` is falsy -> download_incomplete (a malformed/incomplete
// download, distinct from a present-but-wrong-version tag mismatch).
function makeVersionlessDegit() {
  return function (_bin, args) {
    const tmpTarget = args[args.length - 1];
    fs.mkdirSync(tmpTarget, { recursive: true });
    fs.writeFileSync(
      path.join(tmpTarget, 'package.json'),
      JSON.stringify({ name: '@evomap/evolver' }),
      'utf8',
    );
    fs.writeFileSync(path.join(tmpTarget, 'index.js'), '// no version', 'utf8');
  };
}

describe('executeForceUpdate: structured failure taxonomy', () => {
  before(() => {
    installRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-fu-codes-'));
  });

  after(() => {
    childProcess.execFileSync = origExecFileSync;
    delete require.cache[pathsModPath];
    delete require.cache[forceUpdateModPath];
    try { fs.rmSync(installRoot, { recursive: true, force: true }); } catch (_) {}
  });

  beforeEach(() => {
    try { fs.rmSync(installRoot, { recursive: true, force: true }); } catch (_) {}
    fs.mkdirSync(installRoot, { recursive: true });
  });

  // --- guard branches (degit never reached) ---

  it('install_guard_name_mismatch: install root package.json has the wrong name', () => {
    writeInstallPkg('1.0.0', 'some-other-package');
    let execCalls = 0;
    const { executeForceUpdate } = freshRequireForceUpdate(() => { execCalls++; });
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'install_guard_name_mismatch');
    assert.match(r.detail, /some-other-package/, 'detail names the unexpected package');
    assert.equal(execCalls, 0, 'guard fires before degit');
  });

  it('install_guard_unreadable: install root package.json is missing', () => {
    // beforeEach left installRoot empty (no package.json).
    let execCalls = 0;
    const { executeForceUpdate } = freshRequireForceUpdate(() => { execCalls++; });
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'install_guard_unreadable');
    assert.equal(execCalls, 0, 'guard fires before degit');
  });

  it('bad_required_version: required_version is not a concrete semver', () => {
    writeInstallPkg('1.0.0');
    let execCalls = 0;
    const { executeForceUpdate } = freshRequireForceUpdate(() => { execCalls++; });
    const r = executeForceUpdate({ required_version: 'garbage' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'bad_required_version');
    assert.equal(execCalls, 0, 'rejected before Channel 1');
  });

  it('current_version_unparsable: installed version is not a concrete semver (#213 anti-downgrade guard)', () => {
    // Leading-zero patch ("04") is not a valid concrete semver, so the
    // anti-downgrade comparison cannot run → fail closed (do NOT proceed to a
    // download that might be a downgrade). This is the branch #213 added.
    writeInstallPkg('1.88.04');
    let execCalls = 0;
    const { executeForceUpdate } = freshRequireForceUpdate(() => { execCalls++; });
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'current_version_unparsable');
    assert.equal(execCalls, 0, 'fails closed before degit when the installed version cannot be compared');
  });

  // --- Channel 1: degit-spawn branch (phase 'degit') ---

  it('npx_not_found: degit spawn throws ENOENT (npx binary absent)', () => {
    writeInstallPkg('1.0.0');
    const stub = function () { throw Object.assign(new Error('spawnSync npx ENOENT'), { code: 'ENOENT' }); };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'npx_not_found', 'ENOENT on the spawn is npx-missing, NOT a missing download file');
  });

  it('degit_timeout: the 60s timeout kills degit with SIGTERM', () => {
    writeInstallPkg('1.0.0');
    const stub = function () { throw Object.assign(new Error('killed'), { killed: true, signal: 'SIGTERM' }); };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'degit_timeout');
  });

  it('degit_timeout: a bare ETIMEDOUT (no killed/signal) is still a timeout', () => {
    // review #5: some platforms surface the 60s execFileSync timeout as a plain
    // ETIMEDOUT error with neither .killed nor .signal set. The classifier's
    // third disjunct (e.code === 'ETIMEDOUT') must cover this, otherwise it
    // would fall through to the generic degit_failed bucket and lose the timeout
    // signal. This pins the ETIMEDOUT-only variant the SIGTERM case above misses.
    writeInstallPkg('1.0.0');
    const stub = function () { throw Object.assign(new Error('etimedout'), { code: 'ETIMEDOUT' }); };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'degit_timeout', 'ETIMEDOUT without killed/signal is a timeout, not a generic degit_failed');
  });

  it('degit_failed: generic degit failure keeps a tail of stderr in detail', () => {
    writeInstallPkg('1.0.0');
    const stub = function () {
      throw Object.assign(new Error('Command failed'), {
        status: 128,
        stderr: 'fatal: could not read from remote repository\n',
      });
    };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'degit_failed');
    assert.match(r.detail, /could not read from remote repository/, 'stderr tail preserved for drill-down');
  });

  it('degit_failed: stderr in detail is redacted of secrets and stripped of control chars', () => {
    // FIX 2+3: the degit_failed detail embeds a tail of degit's stderr, which can
    // contain a leaked credential (e.g. a token echoed in a clone URL) and raw
    // ANSI/control bytes. Before it is recorded the stderr must be (a) run through
    // redactString so secrets become [REDACTED], and (b) have control chars
    // /[\x00-\x1f\x7f]/ replaced with spaces — so neither a live token nor an
    // ESC byte reaches the hub.
    writeInstallPkg('1.0.0');
    // Secret: ghp_ + 36 alphanumerics. Matches sanitize.js REDACT_PATTERNS
    // /ghp_[A-Za-z0-9]{36,}/g (GitHub personal-access-token), so redactString
    // replaces the whole token with [REDACTED].
    const SECRET = 'ghp_' + 'A'.repeat(36);
    // Control bytes: a CR, plus an ANSI SGR colour sequence (ESC = \x1b). All of
    // ESC/CR are in /[\x00-\x1f\x7f]/ and must be scrubbed to spaces. Kept short
    // and at the tail so the detail's .slice(-300) cannot truncate it away.
    const stderr = 'fatal: clone failed\r auth \x1b[31mtok=' + SECRET + '\x1b[0m';
    const stub = function () {
      // No ENOENT / killed / SIGTERM / ETIMEDOUT -> generic degit_failed, phase='degit'.
      throw Object.assign(new Error('Command failed'), { status: 128, stderr });
    };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'degit_failed');
    // Secret never appears in plaintext; it is collapsed to the redactor marker.
    assert.ok(!r.detail.includes(SECRET), 'raw secret must not survive into detail');
    assert.match(r.detail, /\[REDACTED\]/, 'redactString replaced the leaked token with its marker');
    // No control characters survive: assert specifically the ESC byte is gone,
    // and broadly that nothing in /[\x00-\x1f\x7f]/ remains. (The SGR parameter
    // text like "[31m" is ordinary printable bytes and may remain — only the
    // ESC/control bytes are scrubbed.)
    assert.ok(!r.detail.includes('\x1b'), 'ESC byte stripped from detail');
    assert.doesNotMatch(r.detail, /[\x00-\x1f\x7f]/, 'no control characters remain in detail');
  });

  // --- Channel 1: post-download branches (phase 'parse' / version check) ---

  it('download_incomplete: degit exits 0 but produced no package.json', () => {
    writeInstallPkg('1.0.0');
    // Stub returns without writing package.json into TMP_TARGET → readFileSync ENOENT.
    const stub = function () { /* no-op "successful" degit */ };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'download_incomplete', 'a readFileSync ENOENT at phase=parse is NOT npx_not_found');
  });

  it('download_incomplete: degit exits 0 with a parseable package.json that has no version field', () => {
    // FIX 1: a falsy `tmpPkg.version` (download produced a package.json with no
    // version key) is an incomplete/malformed download, NOT a version mismatch.
    // It must be classified download_incomplete with the exact spec detail, not
    // downloaded_version_mismatch (which is for a present-but-wrong version).
    writeInstallPkg('1.0.0');
    const { executeForceUpdate } = freshRequireForceUpdate(makeVersionlessDegit());
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'download_incomplete',
      'a parseable package.json with no version is an incomplete download, not a mismatch');
    assert.match(r.detail, /no version field/, 'detail explains the package.json had no version field');
  });

  it('downloaded_version_mismatch: degit fetched a different version than requested', () => {
    writeInstallPkg('1.0.0');
    const { executeForceUpdate } = freshRequireForceUpdate(makeSuccessfulDegit('2.0.0'));
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'downloaded_version_mismatch');
    assert.match(r.detail, /2\.0\.0/, 'detail records the downloaded version');
    assert.match(r.detail, /1\.88\.3/, 'detail records the expected version');
  });

  // --- Channel 1: copy branch (phase 'copy') ---

  it('copy_failed: degit downloaded the right version but cpSync into the install root fails', () => {
    writeInstallPkg('1.0.0');
    const { executeForceUpdate } = freshRequireForceUpdate(makeSuccessfulDegit('1.88.3'));
    const origCpSync = fs.cpSync;
    // ENOSPC is not in the EPERM/EBUSY/EACCES retry set, so it breaks immediately.
    fs.cpSync = function () { throw Object.assign(new Error('no space left on device'), { code: 'ENOSPC' }); };
    let r;
    try {
      r = executeForceUpdate({ required_version: '1.88.3' });
    } finally {
      fs.cpSync = origCpSync;
    }
    assert.equal(r.ok, false);
    assert.equal(r.code, 'copy_failed');
    assert.match(r.detail, /index\.js|package\.json/, 'detail names the entry that failed to copy');
  });

  // --- contract / helper sanity ---

  it('every failure result is frozen and carries a string code + string detail', () => {
    writeInstallPkg('1.0.0');
    const stub = function () { throw new Error('boom'); };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(typeof r.code, 'string');
    assert.equal(typeof r.detail, 'string');
    assert.ok(Object.isFrozen(r), 'failure result is frozen so consumers cannot mutate the code/detail');
  });

  it('isForceUpdateFailure / FORCE_UPDATE_FAIL_CODES exports are well-formed', () => {
    const mod = freshRequireForceUpdate(() => {});
    // type guard
    assert.equal(mod.isForceUpdateFailure({ ok: false, code: 'degit_failed', detail: '' }), true);
    assert.equal(mod.isForceUpdateFailure(true), false);
    assert.equal(mod.isForceUpdateFailure(false), false);
    assert.equal(mod.isForceUpdateFailure(null), false);
    assert.equal(mod.isForceUpdateFailure(mod.FORCE_UPDATE_NOOP), false);
    assert.equal(mod.isForceUpdateFailure(mod.FORCE_UPDATE_BUSY), false);
    assert.equal(mod.isForceUpdateFailure({ ok: false }), false, 'a code is required');
    // taxonomy export
    assert.ok(Object.isFrozen(mod.FORCE_UPDATE_FAIL_CODES), 'taxonomy is frozen');
    const codes = Object.values(mod.FORCE_UPDATE_FAIL_CODES);
    for (const expected of [
      'install_guard_name_mismatch', 'install_guard_unreadable', 'bad_required_version',
      'current_version_unparsable', 'npx_not_found', 'degit_timeout', 'degit_failed',
      'download_incomplete', 'downloaded_version_mismatch', 'copy_failed', 'all_channels_exhausted',
    ]) {
      assert.ok(codes.includes(expected), 'taxonomy includes ' + expected);
    }
  });
});
