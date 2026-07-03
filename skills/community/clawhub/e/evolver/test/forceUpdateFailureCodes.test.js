const { describe, it, before, after, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const zlib = require('zlib');

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

function writeStrongEvolverMarkers() {
  fs.mkdirSync(path.join(installRoot, 'src', 'gep'), { recursive: true });
  fs.writeFileSync(
    path.join(installRoot, 'src', 'forceUpdate.js'),
    'function executeForceUpdate() {}\nconst FORCE_UPDATE_FAIL_CODES = {};\n',
    'utf8',
  );
  fs.writeFileSync(
    path.join(installRoot, 'src', 'gep', 'paths.js'),
    'function getRepoRoot() {}\nfunction getEvolverInstallRoot() {}\n',
    'utf8',
  );
  fs.writeFileSync(
    path.join(installRoot, 'src', 'gep', 'a2aProtocol.js'),
    '// GEP A2A Protocol\nfunction reportForceUpdateOutcome() {}\n',
    'utf8',
  );
  fs.writeFileSync(
    path.join(installRoot, 'index.js'),
    "const evolve = require('./src/evolve');\n// proxy-token\n",
    'utf8',
  );
}

// Fake degit that "downloads" a package.json (+ a code file) of the given
// version into TMP_TARGET (the last positional arg degit receives).
function makeDegitPackage(version, name) {
  return function (bin, args) {
    if (!String(bin).includes('npx')) throw new Error('unexpected fallback call');
    const tmpTarget = args[args.length - 1];
    fs.mkdirSync(tmpTarget, { recursive: true });
    fs.writeFileSync(
      path.join(tmpTarget, 'package.json'),
      JSON.stringify({ name: name || '@evomap/evolver', version }),
      'utf8',
    );
    fs.writeFileSync(path.join(tmpTarget, 'index.js'), '// v' + version, 'utf8');
    fs.mkdirSync(path.join(tmpTarget, 'src'), { recursive: true });
    fs.writeFileSync(path.join(tmpTarget, 'src', 'evolve.js'), '// src v' + version, 'utf8');
  };
}

function makeSuccessfulDegit(version) {
  return makeDegitPackage(version, '@evomap/evolver');
}

function makeTarHeader(name, size, type, mode) {
  const header = Buffer.alloc(512);
  header.write(name, 0, Math.min(Buffer.byteLength(name), 100), 'utf8');
  header.write((mode || 0o644).toString(8).padStart(7, '0') + '\0', 100, 'ascii');
  header.write('0000000\0', 108, 'ascii');
  header.write('0000000\0', 116, 'ascii');
  header.write(size.toString(8).padStart(11, '0') + '\0', 124, 'ascii');
  header.write('00000000000\0', 136, 'ascii');
  header.fill(0x20, 148, 156);
  header.write(type || '0', 156, 'ascii');
  header.write('ustar\0', 257, 'ascii');
  header.write('00', 263, 'ascii');
  let sum = 0;
  for (const byte of header) sum += byte;
  header.write(sum.toString(8).padStart(6, '0') + '\0 ', 148, 'ascii');
  return header;
}

function makeTarGzBuffer(entries) {
  const chunks = [];
  for (const entry of entries) {
    const content = Buffer.isBuffer(entry.content)
      ? entry.content
      : Buffer.from(entry.content || '', 'utf8');
    const type = entry.type || '0';
    const size = type === '0' ? content.length : 0;
    chunks.push(makeTarHeader(entry.name, size, type, entry.mode));
    if (size > 0) {
      chunks.push(content);
      const padding = (512 - (size % 512)) % 512;
      if (padding) chunks.push(Buffer.alloc(padding));
    }
  }
  chunks.push(Buffer.alloc(1024));
  return zlib.gzipSync(Buffer.concat(chunks));
}

function makeReleaseTarball(version, extraEntries) {
  return makeTarGzBuffer([
    { name: 'evolver-' + version + '/package.json', content: JSON.stringify({ name: '@evomap/evolver', version }) },
    { name: 'evolver-' + version + '/index.js', content: '// tarball v' + version, mode: 0o755 },
    { name: 'evolver-' + version + '/src/evolve.js', content: '// tarball src v' + version },
  ].concat(extraEntries || []));
}

function makeDegitFailureThenTarballSuccess(version) {
  const calls = [];
  const stub = function (bin, args) {
    calls.push({ bin, args: Array.isArray(args) ? args.slice() : [] });
    if (bin === process.execPath) {
      fs.writeFileSync(args[3], makeReleaseTarball(version));
      return '';
    }
    throw Object.assign(new Error('degit unavailable'), {
      status: 128,
      stderr: 'fatal: could not read from remote repository\n',
    });
  };
  stub.calls = calls;
  return stub;
}

// Like makeSuccessfulDegit, but the "downloaded" package.json is parseable yet
// carries NO version field. Exercises the post-download branch where
// `tmpPkg.version` is falsy -> download_incomplete (a malformed/incomplete
// download, distinct from a present-but-wrong-version tag mismatch).
function makeVersionlessDegit() {
  return function (bin, args) {
    if (!String(bin).includes('npx')) throw new Error('unexpected fallback call');
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
    writeStrongEvolverMarkers();
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

  it('bootstrap recovery: strong evolver markers allow missing package.json to reach tarball fallback', () => {
    writeStrongEvolverMarkers();
    const execStub = makeDegitFailureThenTarballSuccess('1.88.3');
    const { executeForceUpdate } = freshRequireForceUpdate(execStub);
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r, true, 'strong markers permit bootstrap recovery through fallback');
    assert.ok(execStub.calls.some((c) => c.bin === process.execPath), 'tarball downloader was reached');
    assert.equal(execStub.calls.some((c) => c.bin === 'tar'), false,
      'tarball fallback uses the Node extractor, not system tar');
    const restoredPkg = JSON.parse(fs.readFileSync(path.join(installRoot, 'package.json'), 'utf8'));
    assert.equal(restoredPkg.name, '@evomap/evolver');
    assert.equal(restoredPkg.version, '1.88.3');
  });

  it('bootstrap recovery: strong evolver markers allow malformed package.json to be replaced', () => {
    writeStrongEvolverMarkers();
    fs.writeFileSync(path.join(installRoot, 'package.json'), '{not json', 'utf8');
    const { executeForceUpdate } = freshRequireForceUpdate(makeSuccessfulDegit('1.88.3'));
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r, true, 'strong markers permit bootstrap recovery through the install path');
    const restoredPkg = JSON.parse(fs.readFileSync(path.join(installRoot, 'package.json'), 'utf8'));
    assert.equal(restoredPkg.name, '@evomap/evolver');
    assert.equal(restoredPkg.version, '1.88.3');
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

  it('fallback download failure reports fallback terminal telemetry with primary npx context first', () => {
    writeInstallPkg('1.0.0');
    const stub = function (bin) {
      if (bin === process.execPath) throw Object.assign(new Error('fallback download failed'), { code: 'ETIMEDOUT' });
      throw Object.assign(new Error('spawnSync npx ENOENT'), { code: 'ENOENT' });
    };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'fallback_download_incomplete',
      'terminal telemetry aggregates by the terminal fallback failure');
    assert.match(r.detail, /^primary_failed=npx_not_found \| fallback_failed=download_incomplete: .*fallback download failed/,
      'detail starts with primary and fallback context before any truncation');
  });

  it('fallback download failure reports fallback terminal telemetry with primary timeout context first', () => {
    writeInstallPkg('1.0.0');
    const stub = function (bin) {
      if (bin === process.execPath) throw Object.assign(new Error('fallback download failed'), { code: 'ETIMEDOUT' });
      throw Object.assign(new Error('killed'), { killed: true, signal: 'SIGTERM' });
    };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'fallback_download_incomplete');
    assert.match(r.detail, /^primary_failed=degit_timeout \| fallback_failed=download_incomplete: .*fallback download failed/);
  });

  it('fallback download failure preserves bare ETIMEDOUT timeout telemetry', () => {
    // review #5: some platforms surface the 60s execFileSync timeout as a plain
    // ETIMEDOUT error with neither .killed nor .signal set. The classifier's
    // third disjunct (e.code === 'ETIMEDOUT') must cover this, otherwise it
    // would fall through to the generic degit_failed bucket and lose the timeout
    // signal. This pins the ETIMEDOUT-only variant the SIGTERM case above misses.
    writeInstallPkg('1.0.0');
    const stub = function (bin) {
      if (bin === process.execPath) throw Object.assign(new Error('fallback download failed'), { code: 'ETIMEDOUT' });
      throw Object.assign(new Error('etimedout'), { code: 'ETIMEDOUT' });
    };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'fallback_download_incomplete',
      'terminal telemetry aggregates by the terminal fallback failure');
    assert.match(r.detail, /^primary_failed=degit_timeout \| fallback_failed=download_incomplete: .*fallback download failed/);
  });

  it('fallback download failure reports fallback terminal telemetry with generic degit context first', () => {
    writeInstallPkg('1.0.0');
    const stub = function (bin) {
      if (bin === process.execPath) throw Object.assign(new Error('fallback download timeout'), { code: 'ETIMEDOUT' });
      throw Object.assign(new Error('Command failed'), {
        status: 128,
        stderr: 'fatal: could not read from remote repository\n',
      });
    };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'fallback_download_incomplete',
      'terminal telemetry aggregates by the terminal fallback failure');
    assert.match(r.detail, /^primary_failed=degit_failed \| fallback_failed=download_incomplete: .*fallback download timeout/,
      'fallback detail is preserved for drill-down');
  });

  it('fallback terminal failure does not return the original degit stderr', () => {
    writeInstallPkg('1.0.0');
    const SECRET = 'ghp_' + 'A'.repeat(36);
    const stderr = 'fatal: clone failed\r auth \x1b[31mtok=' + SECRET + '\x1b[0m';
    const stub = function (bin) {
      if (bin === process.execPath) throw Object.assign(new Error('fallback download failed'), { code: 'ETIMEDOUT' });
      throw Object.assign(new Error('Command failed'), { status: 128, stderr });
    };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'fallback_download_incomplete');
    assert.match(r.detail, /^primary_failed=degit_failed \| fallback_failed=download_incomplete: .*fallback download failed/);
    assert.ok(!r.detail.includes(SECRET), 'original degit stderr must not be returned after fallback fails');
  });

  it('fallback archive extraction failure reports fallback terminal telemetry', () => {
    writeInstallPkg('1.0.0');
    const stub = function (bin, args) {
      if (bin === process.execPath) {
        fs.writeFileSync(args[3], 'fake tarball bytes', 'utf8');
        return '';
      }
      throw Object.assign(new Error('Command failed'), {
        status: 128,
        stderr: 'fatal: could not read from remote repository\n',
      });
    };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'fallback_download_incomplete');
    assert.match(r.detail,
      /^primary_failed=degit_failed \| fallback_failed=download_incomplete: .*(incorrect header|gzip)/i);
  });

  // --- Channel 1: post-download branches (phase 'parse' / version check) ---

  it('download_incomplete: degit exits 0 but produced no package.json', () => {
    writeInstallPkg('1.0.0');
    // Stub returns without writing package.json into TMP_TARGET → readFileSync ENOENT.
    const stub = function () { /* no-op "successful" degit */ };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'fallback_download_incomplete',
      'fallback failure becomes the aggregation prefix');
    assert.match(r.detail, /^primary_failed=download_incomplete \| fallback_failed=download_incomplete:/);
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
    assert.equal(r.code, 'fallback_download_incomplete',
      'fallback failure becomes the aggregation prefix');
    assert.match(r.detail, /^primary_failed=download_incomplete \| fallback_failed=download_incomplete: .*unexpected fallback call/,
      'detail keeps both the malformed primary download and fallback terminal failure');
  });

  it('fallback failure reports fallback terminal telemetry with version mismatch context', () => {
    writeInstallPkg('1.0.0');
    const { executeForceUpdate } = freshRequireForceUpdate(makeSuccessfulDegit('2.0.0'));
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'fallback_download_incomplete',
      'terminal telemetry aggregates by the terminal fallback failure');
    assert.match(r.detail, /^primary_failed=downloaded_version_mismatch \| fallback_failed=download_incomplete: .*unexpected fallback call/);
  });

  it('fallback failure reports fallback terminal telemetry with package-name mismatch context', () => {
    writeInstallPkg('1.0.0');
    const { executeForceUpdate } = freshRequireForceUpdate(makeDegitPackage('1.88.3', 'some-other-package'));
    const r = executeForceUpdate({ required_version: '1.88.3' });
    assert.equal(r.ok, false);
    assert.equal(r.code, 'fallback_download_incomplete',
      'terminal telemetry aggregates by the terminal fallback failure');
    assert.match(r.detail, /^primary_failed=downloaded_package_name_mismatch \| fallback_failed=download_incomplete: .*unexpected fallback call/);
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
    assert.match(r.detail, /src|index\.js|package\.json/, 'detail names the entry that failed to copy');
  });

  it('fallback install copy failure is preserved under the primary degit telemetry', () => {
    writeInstallPkg('1.0.0');
    const stub = function (bin, args) {
      if (bin === process.execPath) {
        fs.writeFileSync(args[3], makeReleaseTarball('1.88.3'));
        return '';
      }
      throw Object.assign(new Error('Command failed'), {
        status: 128,
        stderr: 'fatal: could not read from remote repository\n',
      });
    };
    const { executeForceUpdate } = freshRequireForceUpdate(stub);
    const origCpSync = fs.cpSync;
    fs.cpSync = function (src, dst, opts) {
      if (path.basename(String(src)) === 'src') {
        throw Object.assign(new Error('no space left on device'), { code: 'ENOSPC' });
      }
      return origCpSync(src, dst, opts);
    };
    let r;
    try {
      r = executeForceUpdate({ required_version: '1.88.3' });
    } finally {
      fs.cpSync = origCpSync;
    }
    assert.equal(r.ok, false);
    assert.equal(r.code, 'fallback_copy_failed');
    assert.match(r.detail, /^primary_failed=degit_failed \| fallback_failed=copy_failed: src/);
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
      'download_incomplete', 'downloaded_package_name_mismatch', 'downloaded_version_mismatch',
      'fallback_download_incomplete', 'fallback_delete_failed', 'fallback_copy_failed',
      'fallback_downloaded_package_name_mismatch', 'fallback_downloaded_version_mismatch',
      'copy_failed', 'all_channels_exhausted',
    ]) {
      assert.ok(codes.includes(expected), 'taxonomy includes ' + expected);
    }
  });
});
