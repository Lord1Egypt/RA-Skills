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

// Fake degit: write a new-version package.json + bootstrap + code file into TMP_TARGET.
function makeSuccessfulDegitWithIndex(version, indexContent) {
  return function (_bin, args) {
    const tmpTarget = args[args.length - 1];
    fs.mkdirSync(tmpTarget, { recursive: true });
    fs.writeFileSync(
      path.join(tmpTarget, 'package.json'),
      JSON.stringify({ name: '@evomap/evolver', version }),
      'utf8',
    );
    fs.writeFileSync(path.join(tmpTarget, 'index.js'), indexContent, 'utf8');
    fs.mkdirSync(path.join(tmpTarget, 'src'), { recursive: true });
    fs.writeFileSync(path.join(tmpTarget, 'src', 'evolve.js'), '// src v' + version, 'utf8');
  };
}

function makeSuccessfulDegit(version) {
  return makeSuccessfulDegitWithIndex(version, '// v' + version);
}

function populateOldInstall(root, version) {
  fs.writeFileSync(
    path.join(root, 'package.json'),
    JSON.stringify({ name: '@evomap/evolver', version: version || '1.0.0' }),
    'utf8',
  );
  fs.writeFileSync(path.join(root, 'index.js'), '// old', 'utf8');
  fs.mkdirSync(path.join(root, 'src'), { recursive: true });
  fs.writeFileSync(path.join(root, 'src', 'evolve.js'), '// old src', 'utf8');
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
      if (path.basename(String(src)) === 'src') {
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
      if (path.basename(String(src)) === 'src') {
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
    assert.equal(fs.readFileSync(path.join(installRoot, 'src', 'evolve.js'), 'utf8'), '// src v2.0.0',
      'the new payload is in place after recovery');
    assert.equal(fs.readFileSync(path.join(installRoot, 'index.js'), 'utf8'), '// v2.0.0',
      'the downloaded bootstrap is committed on the successful retry');
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

  it('puts the recovery-capable bootstrap in place before moving old payload entries', () => {
    populateOldInstall(installRoot, '1.0.0');
    const oldIndex = fs.readFileSync(path.join(installRoot, 'index.js'), 'utf8');
    const downloadedIndex = fs.readFileSync(path.join(__dirname, '..', 'index.js'), 'utf8') +
      '\n// downloaded recovery bootstrap 2.0.0\n';
    const childScript = [
      "const fs = require('fs');",
      "const path = require('path');",
      "const childProcess = require('child_process');",
      "const installRoot = process.argv[1];",
      "const repoRoot = process.argv[2];",
      "const downloadedIndex = fs.readFileSync(path.join(repoRoot, 'index.js'), 'utf8') + '\\n// downloaded recovery bootstrap 2.0.0\\n';",
      "const pathsModPath = require.resolve(path.join(repoRoot, 'src', 'gep', 'paths.js'));",
      "require.cache[pathsModPath] = { id: pathsModPath, filename: pathsModPath, loaded: true, exports: { getEvolverInstallRoot: () => installRoot } };",
      "childProcess.execFileSync = function (_bin, args) {",
      "  const tmpTarget = args[args.length - 1];",
      "  fs.mkdirSync(tmpTarget, { recursive: true });",
      "  fs.writeFileSync(path.join(tmpTarget, 'package.json'), JSON.stringify({ name: '@evomap/evolver', version: '2.0.0' }), 'utf8');",
      "  fs.writeFileSync(path.join(tmpTarget, 'index.js'), downloadedIndex, 'utf8');",
      "  fs.mkdirSync(path.join(tmpTarget, 'src'), { recursive: true });",
      "  fs.writeFileSync(path.join(tmpTarget, 'src', 'evolve.js'), '// src v2.0.0', 'utf8');",
      "};",
      "const origRenameSync = fs.renameSync;",
      "fs.renameSync = function (src, dst) {",
      "  const dstParent = path.basename(path.dirname(String(dst)));",
      "  if (path.basename(String(src)) === 'src' && dstParent.startsWith('.evolver-force-update-backup-')) {",
      "    origRenameSync.apply(this, arguments);",
      "    process.exit(42);",
      "  }",
      "  return origRenameSync.apply(this, arguments);",
      "};",
      "const { executeForceUpdate } = require(path.join(repoRoot, 'src', 'forceUpdate.js'));",
      "const result = executeForceUpdate({ required_version: '2.0.0' });",
      "process.exit(result === true ? 0 : 1);",
    ].join('\n');

    const interrupted = childProcess.spawnSync(
      process.execPath,
      ['-e', childScript, installRoot, path.join(__dirname, '..')],
      { encoding: 'utf8' },
    );
    assert.equal(interrupted.status, 42, 'precondition: child exits immediately after moving src to backup');
    assert.ok(!fs.existsSync(path.join(installRoot, 'src')),
      'precondition: old src is no longer live after the simulated crash');
    assert.equal(fs.readFileSync(path.join(installRoot, 'index.js'), 'utf8'), downloadedIndex,
      'the live bootstrap is already the downloaded recovery-capable index.js');

    const recovered = childProcess.spawnSync(
      process.execPath,
      [path.join(installRoot, 'index.js'), 'proxy-token', '--settings', path.join(installRoot, 'missing.json')],
      { encoding: 'utf8', env: { ...process.env, EVOLVER_REPO_ROOT: installRoot } },
    );

    assert.equal(recovered.status, 1, 'proxy-token still exits with no token after bootstrap recovery');
    assert.match(recovered.stderr, /Recovered interrupted install/,
      'the early-committed bootstrap runs recovery on the next startup');
    assert.equal(fs.readFileSync(path.join(installRoot, 'index.js'), 'utf8'), oldIndex,
      'bootstrap restores the old index.js from the precommit backup, not the downloaded bootstrap');
    assert.equal(fs.readFileSync(path.join(installRoot, 'src', 'evolve.js'), 'utf8'), '// old src',
      'bootstrap restores the old src tree from the precommit backup');
    assert.equal(readPkgVersion(installRoot), '1.0.0',
      'bootstrap leaves the old package.json marker consistent with the restored old payload');
    assert.deepEqual(
      fs.readdirSync(installRoot).filter(n => n.startsWith('.evolver-force-update-backup-')),
      [],
      'bootstrap removes the consumed precommit backup',
    );
  });

  it('does not unlink live index.js before replacing it on Windows', () => {
    populateOldInstall(installRoot, '1.0.0');
    const { executeForceUpdate } = freshRequireForceUpdate(makeSuccessfulDegit('2.0.0'));
    Object.defineProperty(process, 'platform', { value: 'win32' });
    let liveIndexUnlinkAttempted = false;
    fs.rmSync = function (target, opts) {
      if (path.resolve(String(target)) === path.join(installRoot, 'index.js')) {
        liveIndexUnlinkAttempted = true;
        throw Object.assign(new Error('live index unlink would create a bootstrap gap'), { code: 'EACCES' });
      }
      return origRmSync(target, opts);
    };

    assert.equal(executeForceUpdate({ required_version: '2.0.0' }), true,
      'the update can replace index.js without deleting the live entry first');
    assert.equal(liveIndexUnlinkAttempted, false,
      'Windows index replacement must not remove the startup entry before rename');
    assert.equal(fs.readFileSync(path.join(installRoot, 'index.js'), 'utf8'), '// v2.0.0',
      'the downloaded bootstrap is still installed');
  });

  it('a delete failure restores already-removed old entries before committing the new package.json', () => {
    populateOldInstall(installRoot, '1.0.0');
    fs.writeFileSync(path.join(installRoot, 'obsolete-a.js'), '// old a', 'utf8');
    fs.writeFileSync(path.join(installRoot, 'obsolete-b.js'), '// old b', 'utf8');
    const { executeForceUpdate } = freshRequireForceUpdate(function (_bin, args) {
      const tmpTarget = args[args.length - 1];
      fs.mkdirSync(tmpTarget, { recursive: true });
      fs.writeFileSync(
        path.join(tmpTarget, 'package.json'),
        JSON.stringify({ name: '@evomap/evolver', version: '2.0.0' }),
        'utf8',
      );
      fs.writeFileSync(path.join(tmpTarget, 'index.js'), '// v2.0.0', 'utf8');
      fs.mkdirSync(path.join(tmpTarget, 'src'), { recursive: true });
      fs.writeFileSync(path.join(tmpTarget, 'src', 'evolve.js'), '// src v2.0.0', 'utf8');
      fs.writeFileSync(path.join(tmpTarget, 'new-code.js'), '// new', 'utf8');
    });
    const backupMoveNames = [];
    let lockedBackupMoveName = null;
    fs.renameSync = function (src, dst) {
      const dstParent = path.basename(path.dirname(String(dst)));
      if (dstParent.startsWith('.evolver-force-update-backup-')) {
        const moveName = path.basename(String(src));
        if (lockedBackupMoveName === null && backupMoveNames.length === 1) {
          lockedBackupMoveName = moveName;
        }
        backupMoveNames.push(moveName);
        if (moveName === lockedBackupMoveName) {
          throw Object.assign(new Error('old entry is locked'), { code: 'EBUSY' });
        }
      }
      return origRenameSync(src, dst);
    };

    const result = executeForceUpdate({ required_version: '2.0.0' });
    fs.renameSync = origRenameSync;
    assert.equal(result.ok, false, 'the update fails when an old entry cannot be deleted');
    assert.equal(result.code, 'delete_failed');
    assert.ok(new Set(backupMoveNames).size >= 2, 'one old entry was removed before the second delete failed');
    assert.ok(result.detail.includes(lockedBackupMoveName), 'the failed delete entry is named');
    assert.equal(readPkgVersion(installRoot), '1.0.0',
      'new package.json must not be committed after a delete failure');
    assert.equal(fs.readFileSync(path.join(installRoot, 'index.js'), 'utf8'), '// old',
      'old index.js is restored if it was the first removed entry');
    assert.equal(fs.readFileSync(path.join(installRoot, 'obsolete-a.js'), 'utf8'), '// old a',
      'first old non-keep file is restored after the second delete fails');
    assert.equal(fs.readFileSync(path.join(installRoot, 'obsolete-b.js'), 'utf8'), '// old b',
      'second old non-keep file remains after its delete fails');
    assert.ok(!fs.existsSync(path.join(installRoot, 'new-code.js')),
      'new-only code must not land after a delete failure');
    assert.deepEqual(
      fs.readdirSync(installRoot).filter(n => n.startsWith('.evolver-force-update-backup-')),
      [],
      'successful rollback removes the temporary backup directory',
    );

    assert.equal(executeForceUpdate({ required_version: '2.0.0' }), true,
      'the next attempt self-heals once the delete succeeds');
    assert.equal(readPkgVersion(installRoot), '2.0.0');
    assert.ok(!fs.existsSync(path.join(installRoot, 'obsolete-a.js')),
      'stale entry a is pruned on the successful retry');
    assert.ok(!fs.existsSync(path.join(installRoot, 'obsolete-b.js')),
      'stale entry b is pruned on the successful retry');
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
    const backupLeftovers = fs.readdirSync(installRoot).filter(n => n.startsWith('.evolver-force-update-backup-'));
    assert.deepEqual(backupLeftovers, [], 'no rollback backup directory remains after a successful commit');
    assert.equal(fs.readFileSync(path.join(installRoot, 'index.js'), 'utf8'), '// v2.0.0',
      'index.js is committed from the downloaded release');
  });

  it('bootstrap recovers a precommit backup before loading the missing src tree', () => {
    populateOldInstall(installRoot, '1.0.0');
    fs.copyFileSync(path.join(__dirname, '..', 'index.js'), path.join(installRoot, 'index.js'));
    const backupRoot = fs.mkdtempSync(path.join(installRoot, '.evolver-force-update-backup-'));
    fs.writeFileSync(
      path.join(backupRoot, '.evolver-force-update-journal.json'),
      JSON.stringify({ state: 'precommit', requiredVersion: '2.0.0', previousVersion: '1.0.0' }),
      'utf8',
    );
    fs.renameSync(path.join(installRoot, 'src'), path.join(backupRoot, 'src'));
    assert.ok(!fs.existsSync(path.join(installRoot, 'src')),
      'precondition: interrupted update moved src out of the live install');

    const result = childProcess.spawnSync(
      process.execPath,
      [path.join(installRoot, 'index.js'), 'proxy-token', '--settings', path.join(installRoot, 'missing.json')],
      { encoding: 'utf8', env: { ...process.env, EVOLVER_REPO_ROOT: installRoot } },
    );

    assert.equal(result.status, 1, 'proxy-token still exits with no token after bootstrap recovery');
    assert.match(result.stderr, /Recovered interrupted install/,
      'bootstrap should report that it recovered the interrupted update');
    assert.equal(fs.readFileSync(path.join(installRoot, 'src', 'evolve.js'), 'utf8'), '// old src',
      'bootstrap restores the old src tree before any normal startup require can run');
    assert.ok(!fs.existsSync(backupRoot), 'bootstrap removes the consumed backup directory');
  });

  it('bootstrap fails closed when restoring interrupted backup index.js fails', () => {
    populateOldInstall(installRoot, '1.0.0');
    fs.copyFileSync(path.join(__dirname, '..', 'index.js'), path.join(installRoot, 'index.js'));
    const liveIndex = fs.readFileSync(path.join(installRoot, 'index.js'), 'utf8');
    const backupRoot = fs.mkdtempSync(path.join(installRoot, '.evolver-force-update-backup-'));
    fs.writeFileSync(
      path.join(backupRoot, '.evolver-force-update-journal.json'),
      JSON.stringify({ state: 'precommit', requiredVersion: '2.0.0', previousVersion: '1.0.0' }),
      'utf8',
    );
    fs.writeFileSync(path.join(backupRoot, 'index.js'), '// old backup index', 'utf8');
    fs.renameSync(path.join(installRoot, 'src'), path.join(backupRoot, 'src'));
    const shimPath = path.join(installRoot, 'rename-fail-shim.js');
    fs.writeFileSync(shimPath, [
      "const fs = require('fs');",
      "const path = require('path');",
      'const origRenameSync = fs.renameSync;',
      'fs.renameSync = function (src, dst) {',
      "  if (String(src).includes('.recover-tmp') && path.basename(String(dst)) === 'index.js') {",
      "    throw Object.assign(new Error('simulated restore rename failure'), { code: 'EACCES' });",
      '  }',
      '  return origRenameSync.apply(this, arguments);',
      '};',
    ].join('\n'), 'utf8');

    const nodeOptions = ((process.env.NODE_OPTIONS || '') + ' --require=' + shimPath).trim();
    const result = childProcess.spawnSync(
      process.execPath,
      [path.join(installRoot, 'index.js'), 'proxy-token', '--settings', path.join(installRoot, 'missing.json')],
      { encoding: 'utf8', env: { ...process.env, EVOLVER_REPO_ROOT: installRoot, NODE_OPTIONS: nodeOptions } },
    );

    assert.notEqual(result.status, 0, 'bootstrap restore failure must stop startup');
    assert.match(result.stderr, /Bootstrap recovery failed/,
      'bootstrap prints a clear recovery failure');
    assert.doesNotMatch(result.stderr, /\[proxy-token\] no active proxy token/,
      'normal CLI command handling must not continue after failed recovery');
    assert.ok(fs.existsSync(backupRoot), 'failed recovery leaves the backup directory in place');
    assert.ok(fs.existsSync(path.join(backupRoot, '.evolver-force-update-journal.json')),
      'failed recovery leaves the journal in place');
    assert.equal(fs.readFileSync(path.join(installRoot, 'index.js'), 'utf8'), liveIndex,
      'failed recovery keeps the live recovery-capable bootstrap in place');
    assert.equal(fs.readFileSync(path.join(backupRoot, 'index.js'), 'utf8'), '// old backup index',
      'failed recovery leaves the backed-up bootstrap for a later cleanup');
  });

  it('bootstrap ignores stale backup when current version is newer than the journal requirement', () => {
    populateOldInstall(installRoot, '3.0.0');
    fs.writeFileSync(path.join(installRoot, 'src', 'evolve.js'), '// current src 3.0.0', 'utf8');
    fs.copyFileSync(path.join(__dirname, '..', 'index.js'), path.join(installRoot, 'index.js'));
    const backupRoot = fs.mkdtempSync(path.join(installRoot, '.evolver-force-update-backup-'));
    fs.writeFileSync(
      path.join(backupRoot, '.evolver-force-update-journal.json'),
      JSON.stringify({ state: 'precommit', requiredVersion: '2.0.0', previousVersion: '1.0.0' }),
      'utf8',
    );
    fs.mkdirSync(path.join(backupRoot, 'src'), { recursive: true });
    fs.writeFileSync(path.join(backupRoot, 'src', 'evolve.js'), '// stale src 1.0.0', 'utf8');

    const result = childProcess.spawnSync(
      process.execPath,
      [path.join(installRoot, 'index.js'), 'proxy-token', '--settings', path.join(installRoot, 'missing.json')],
      { encoding: 'utf8', env: { ...process.env, EVOLVER_REPO_ROOT: installRoot } },
    );

    assert.equal(result.status, 1, 'proxy-token still exits with no token after stale backup cleanup');
    assert.doesNotMatch(result.stderr, /Recovered interrupted install/,
      'stale backup is cleaned rather than restored');
    assert.equal(fs.readFileSync(path.join(installRoot, 'src', 'evolve.js'), 'utf8'), '// current src 3.0.0',
      'current newer payload is not overwritten by a stale backup');
    assert.ok(!fs.existsSync(backupRoot), 'stale backup directory is removed');
  });
});
