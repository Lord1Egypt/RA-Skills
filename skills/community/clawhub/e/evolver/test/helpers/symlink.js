// test/helpers/symlink.js
//
// `canCreateSymlinks()` probes the OS at module load time to determine
// whether the current process is allowed to create filesystem symlinks.
// Used by tests that exercise symlink-rejection code paths: those tests
// must first place a symlink to feed the code under test, and on Windows
// `fs.symlinkSync` requires either administrator privileges or developer
// mode (otherwise it throws `EPERM`). Without this probe, ~15 tests
// across adapters.* / workspaceKeychain.test.js / evolveCollect.test.js
// fail in setup before the assertion they actually want to make.
//
// Typical usage:
//
//   const { describe, it } = require('node:test');
//   const { canCreateSymlinks } = require('./helpers/symlink');
//   const symlinkIt = canCreateSymlinks() ? it : it.skip;
//
//   describe('thing', () => {
//     symlinkIt('refuses symlinked input', () => { ... });
//   });
//
// The result is cached per process. The probe leaves no FS artefact
// behind (it unlinks on success and ignores the unlink error path).
//
// Note: this hides a real Windows-CI gap rather than fixing it — the
// symlink-rejection code paths under test go uncovered on Windows
// non-admin runs. The right long-term answer is either (a) bake admin
// /developer-mode into the Windows CI image, or (b) mock the fs
// boundary so the rejection logic can be tested without a real
// symlink. Both are larger scope than the present "stop the publish
// gate from being non-functional" cleanup.

'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');

let _cachedSymlink;

function canCreateSymlinks() {
  if (_cachedSymlink !== undefined) return _cachedSymlink;
  const probe = path.join(os.tmpdir(), `evolver-symlink-probe-${process.pid}-${Date.now()}`);
  try {
    fs.symlinkSync('target-need-not-exist', probe);
    try { fs.unlinkSync(probe); } catch { /* best-effort cleanup */ }
    _cachedSymlink = true;
  } catch {
    _cachedSymlink = false;
  }
  return _cachedSymlink;
}

// Companion probe: `canMakeDirReadOnly()` returns true only when
// `fs.chmodSync(dir, 0o555)` actually prevents the process from
// writing into `dir`. On Windows, `chmod` mostly maps to FS attribute
// flags rather than ACL changes, so a "read-only" directory still
// accepts writes from the owning user — tests that rely on the
// POSIX-style semantics ("make this workspace read-only so the secret
// can't be persisted") silently observe the wrong behaviour. Skip
// those tests when the probe says the underlying FS won't honour the
// mode bit. Same caveat as the symlink probe: this hides a real
// platform gap in coverage; the right long-term answer is to mock
// the filesystem boundary instead of relying on chmod.
let _cachedReadOnlyDir;

function canMakeDirReadOnly() {
  if (_cachedReadOnlyDir !== undefined) return _cachedReadOnlyDir;
  let dir;
  try {
    dir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-rodir-probe-'));
    fs.chmodSync(dir, 0o555);
    try {
      fs.writeFileSync(path.join(dir, 'write-probe'), 'x');
      // Write succeeded — chmod did not actually enforce read-only.
      _cachedReadOnlyDir = false;
    } catch {
      // Write failed as expected — chmod is honoured.
      _cachedReadOnlyDir = true;
    }
  } catch {
    _cachedReadOnlyDir = false;
  } finally {
    if (dir) {
      try { fs.chmodSync(dir, 0o755); } catch {}
      try { fs.rmSync(dir, { recursive: true, force: true }); } catch {}
    }
  }
  return _cachedReadOnlyDir;
}

module.exports = { canCreateSymlinks, canMakeDirReadOnly };
