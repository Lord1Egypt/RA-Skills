const { describe, it, before, after, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

// Regression: a mid-copy cpSync failure must NOT permanently wedge the node.
//
// The Channel-1 install path deletes the old install in place, then copies the
// new tree on top. Historically `package.json` was deleted in that loop along
// with everything else, so a cpSync failure part-way through (ENOSPC, a Windows
// lock that outlasts the retries, a kill) left INSTALL_ROOT with NO package.json.
// The install-guard at the top of executeForceUpdate refuses on an unreadable
// package.json, so every subsequent attempt returned install-guard-refused with
// no path that ever re-copied package.json — the node was stuck forever.
//
// The fix makes package.json the install's atomic commit marker: it is kept in
// place through the whole delete+copy and swapped in last via tmp+rename. So a
// partial failure leaves the OLD package.json intact and the node self-heals on
// the next attempt. These tests pin that contract (they FAIL on the pre-fix
// code, which deletes package.json before the copy).
//
// Harness mirrors forceUpdateKeepList.test.js: forceUpdate.js destructures
// `execFileSync` at module load, so we mutate child_process.execFileSync before
// each fresh require and point getEvolverInstallRoot at a temp dir.

const childProcess = require('child_process');
const origExecFileSync = childProcess.execFileSync;
const origCpSync = fs.cpSync;
const origRmSync = fs.rmSync;
const origRenameSync = fs.renameSync;
const origPlatform = Object.getOwnPropertyDescriptor(process, 'platform');

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
  try {
    return require('../src/forceUpdate');
  } finally {
    childProcess.execFileSync = origExecFileSync;
  }
}

// Fake degit: write a new-version package.json + a code file into TMP_TARGET.
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

function populateOldInstall(root, version) {
  fs.writeFileSync(
    path.join(root, 'package.json'),
    JSON.stringify({ name: '@evomap/evolver', version: version || '1.0.0' }),
    'utf8',
  );
  fs.writeFileSync(path.join(root, 'index.js'), '// old', 'utf8');
}

function readPkgVersion(root) {
  return JSON.parse(fs.readFileSync(path.join(root, 'package.json'), 'utf8')).version;
}

function restoreGlobals() {
  childProcess.execFileSync = origExecFileSync;
  fs.cpSync = origCpSync;
  fs.rmSync = origRmSync;
  fs.renameSync = origRenameSync;
  Object.defineProperty(process, 'platform', origPlatform);
}

describe('executeForceUpdate: mid-copy failure does not wedge the node', () => {
  before(() => {
    installRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-wedge-'));
  });

  after(() => {
    restoreGlobals();
    delete require.cache[pathsModPath];
    delete require.cache[forceUpdateModPath];
    try { fs.rmSync(installRoot, { recursive: true, force: true }); } catch (_) {}
  });

  beforeEach(() => {
    restoreGlobals();
    try { fs.rmSync(installRoot, { recursive: true, force: true }); } catch (_) {}
    fs.mkdirSync(installRoot, { recursive: true });
  });

  it('a mid-copy cpSync failure leaves the OLD package.json intact (the install-guard can still read it)', () => {
    populateOldInstall(installRoot, '1.0.0');
    const { executeForceUpdate } = freshRequireForceUpdate(makeSuccessfulDegit('2.0.0'));

    // Fail the copy of a NON-package.json entry, before the atomic commit.
    // ENOSPC is outside the EPERM/EBUSY/EACCES retry set, so it breaks at once.
    fs.cpSync = function (src, dst, opts) {
      if (String(src).endsWith('index.js')) {
        throw Object.assign(new Error('no space left on device'), { code: 'ENOSPC' });
      }
      return origCpSync(src, dst, opts);
    };

    const result = executeForceUpdate({ required_version: '2.0.0' });
    fs.cpSync = origCpSync;

    assert.equal(result.ok, false, 'the update fails');
    assert.equal(result.code, 'copy_failed', 'the failed copy is reported with the structured copy_failed code');
    // THE FIX: package.json must survive the partial copy so the next attempt's
    // install-guard reads a valid file instead of wedging on ENOENT.
    assert.ok(fs.existsSync(path.join(installRoot, 'package.json')),
      'package.json must NOT be deleted by a failed mid-copy update');
    assert.equal(readPkgVersion(installRoot), '1.0.0',
      'the surviving package.json is still the OLD version (not a partially-written new one)');
  });

  it('after a transient mid-copy failure, the very next attempt self-heals (no install_guard_unreadable wedge)', () => {
    populateOldInstall(installRoot, '1.0.0');
    const { executeForceUpdate } = freshRequireForceUpdate(makeSuccessfulDegit('2.0.0'));

    // Attempt 1: transient ENOSPC on the code file -> fails, package.json kept.
    fs.cpSync = function (src, dst, opts) {
      if (String(src).endsWith('index.js')) {
        throw Object.assign(new Error('no space left on device'), { code: 'ENOSPC' });
      }
      return origCpSync(src, dst, opts);
    };
    const result = executeForceUpdate({ required_version: '2.0.0' });
    assert.equal(result.ok, false, 'attempt 1 fails');
    assert.equal(result.code, 'copy_failed', 'attempt 1 reports the structured copy_failed code');

    // Attempt 2: disk recovered. The guard must read the preserved old
    // package.json (v1.0.0 < 2.0.0), proceed, and complete — proving the node
    // is NOT stuck. On the pre-fix code package.json is gone here and attempt 2
    // refuses with an unreadable-install guard.
    fs.cpSync = origCpSync;
    assert.equal(executeForceUpdate({ required_version: '2.0.0' }), true,
      'attempt 2 self-heals instead of wedging on install_guard_unreadable');
    assert.equal(readPkgVersion(installRoot), '2.0.0',
      'the recovered install is now at the new version');
    assert.equal(fs.readFileSync(path.join(installRoot, 'index.js'), 'utf8'), '// v2.0.0',
      'the new code is in place after recovery');
  });

  it('a Windows package.json commit failure restores the OLD package.json and retries cleanly', () => {
    populateOldInstall(installRoot, '1.0.0');
    const { executeForceUpdate } = freshRequireForceUpdate(makeSuccessfulDegit('2.0.0'));
    Object.defineProperty(process, 'platform', { value: 'win32' });
    fs.renameSync = function (src, dst) {
      if (String(src).endsWith('.evolver-tmp') && String(dst).endsWith('package.json')) {
        throw Object.assign(new Error('package.json is locked'), { code: 'EPERM' });
      }
      return origRenameSync(src, dst);
    };

    const result = executeForceUpdate({ required_version: '2.0.0' });
    assert.equal(result.ok, false, 'the package commit fails');
    assert.equal(result.code, 'copy_failed', 'the commit failure is reported as a copy-phase failure');
    assert.ok(result.detail.includes('package.json commit'), 'the failing commit marker is named');
    assert.ok(fs.existsSync(path.join(installRoot, 'package.json')),
      'old package.json must be restored after the failed Windows commit');
    assert.equal(readPkgVersion(installRoot), '1.0.0',
      'the restored package.json must still be the old version');
    const leftovers = fs.readdirSync(installRoot).filter(n => /^package\.json\..*evolver-(tmp|old)$/.test(n));
    assert.deepEqual(leftovers, [], 'failed commit restores old marker and leaves no staging marker behind');

    fs.renameSync = origRenameSync;
    assert.equal(executeForceUpdate({ required_version: '2.0.0' }), true,
      'the next attempt can self-heal after the Windows commit failure');
    assert.equal(readPkgVersion(installRoot), '2.0.0');
  });

  it('recovers an OLD package.json backup left by an interrupted Windows commit', () => {
    populateOldInstall(installRoot, '1.0.0');
    const backup = path.join(installRoot, 'package.json.12345.evolver-old');
    fs.renameSync(path.join(installRoot, 'package.json'), backup);
    assert.ok(!fs.existsSync(path.join(installRoot, 'package.json')),
      'the interrupted commit left no live package.json');

    const { executeForceUpdate } = freshRequireForceUpdate(makeSuccessfulDegit('2.0.0'));
    assert.equal(executeForceUpdate({ required_version: '2.0.0' }), true,
      'install guard recovers the old marker, then the update proceeds');
    assert.equal(readPkgVersion(installRoot), '2.0.0');
    assert.ok(!fs.existsSync(backup), 'the recovered backup marker is consumed');
  });

  it('a delete failure aborts before committing the new package.json, avoiding a mixed tree', () => {
    populateOldInstall(installRoot, '1.0.0');
    fs.writeFileSync(path.join(installRoot, 'obsolete.js'), '// stale', 'utf8');
    const { executeForceUpdate } = freshRequireForceUpdate(makeSuccessfulDegit('2.0.0'));
    fs.rmSync = function (target, opts) {
      if (path.basename(String(target)) === 'obsolete.js') {
        throw Object.assign(new Error('obsolete file is locked'), { code: 'EBUSY' });
      }
      return origRmSync(target, opts);
    };

    const result = executeForceUpdate({ required_version: '2.0.0' });
    assert.equal(result.ok, false, 'the update fails when an old entry cannot be deleted');
    assert.equal(result.code, 'delete_failed');
    assert.ok(result.detail.includes('obsolete.js'), 'the failed delete entry is named');
    assert.equal(readPkgVersion(installRoot), '1.0.0',
      'new package.json must not be committed after a delete failure');
    assert.ok(fs.existsSync(path.join(installRoot, 'obsolete.js')),
      'the stale entry remains for the next retry instead of being hidden by a committed manifest');
    const indexPath = path.join(installRoot, 'index.js');
    if (fs.existsSync(indexPath)) {
      assert.equal(fs.readFileSync(indexPath, 'utf8'), '// old',
        'new code must not be copied after a delete failure');
    }

    fs.rmSync = origRmSync;
    assert.equal(executeForceUpdate({ required_version: '2.0.0' }), true,
      'the next attempt self-heals once the delete succeeds');
    assert.equal(readPkgVersion(installRoot), '2.0.0');
    assert.ok(!fs.existsSync(path.join(installRoot, 'obsolete.js')),
      'the stale entry is pruned on the successful retry');
  });

  it('the happy path commits the new package.json atomically and leaves no temp file behind', () => {
    populateOldInstall(installRoot, '1.0.0');
    const { executeForceUpdate } = freshRequireForceUpdate(makeSuccessfulDegit('2.0.0'));

    assert.equal(executeForceUpdate({ required_version: '2.0.0' }), true, 'update succeeds');
    assert.equal(readPkgVersion(installRoot), '2.0.0', 'package.json is the new version');
    // The atomic replace writes to `package.json.<pid>.evolver-tmp` then renames;
    // a successful commit must not leave that staging file behind.
    const leftovers = fs.readdirSync(installRoot).filter(n => /^package\.json\..*evolver-(tmp|old)$/.test(n));
    assert.deepEqual(leftovers, [], 'no package.json staging temp file remains after a successful commit');
  });
});
