const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');
const { getEvolverInstallRoot } = require('./gep/paths');

const MAX_EXEC_BUFFER = 10 * 1024 * 1024;

const SEMVER_NUMERIC_IDENTIFIER = '0|[1-9]\\d*';
const SEMVER_PRERELEASE_IDENTIFIER = '(?:0|[1-9]\\d*|\\d*[A-Za-z-][0-9A-Za-z-]*)';
const SEMVER_BUILD_IDENTIFIER = '[0-9A-Za-z-]+';
const CONCRETE_SEMVER_RE = new RegExp(
  '^(' + SEMVER_NUMERIC_IDENTIFIER + ')\\.(' + SEMVER_NUMERIC_IDENTIFIER + ')\\.(' +
    SEMVER_NUMERIC_IDENTIFIER + ')(?:-(' + SEMVER_PRERELEASE_IDENTIFIER +
    '(?:\\.' + SEMVER_PRERELEASE_IDENTIFIER + ')*))?(?:\\+(' +
    SEMVER_BUILD_IDENTIFIER + '(?:\\.' + SEMVER_BUILD_IDENTIFIER + ')*))?$'
);

// Sentinel returned by executeForceUpdate when the no-op short-circuit fires
// (current installed version already satisfies required_version). Distinct from
// `true` so callers can suppress phantom "success" telemetry and avoid the
// gratuitous process.exit(78) restart that follows a real upgrade. Callers
// MUST detect this with === identity comparison; do not use truthy/falsy
// checks (the sentinel IS truthy).
const FORCE_UPDATE_NOOP = Symbol('FORCE_UPDATE_NOOP');

// Sentinel returned by executeForceUpdate when a concurrent invocation is
// already running in this process. The two callers (enrich.js's evolve tick
// and a2aProtocol's heartbeat-thread trigger) can both observe a pending
// force_update directive in the same scheduler tick. Without a shared
// in-process mutex, both would call executeForceUpdate and both would fire
// reportForceUpdateOutcome, causing two atomic-rename writes to the same
// state file -- last writer wins, the first attempt's telemetry is lost.
//
// Callers MUST detect this with === identity comparison and treat it as a
// no-op (do NOT write a state file, do NOT trigger process.exit(78), do NOT
// emit failure telemetry). The in-flight invocation owns the outcome and will
// fire its own reportForceUpdateOutcome. See test/forceUpdateConcurrencyGuard.test.js.
const FORCE_UPDATE_BUSY = Symbol('FORCE_UPDATE_BUSY');

// Structured failure taxonomy. Historically every failing branch of
// _executeForceUpdateInner just `return false`, so the only thing that ever
// reached the hub (via reportForceUpdateOutcome) was the literal string
// "executeForceUpdate returned false" — degit-missing, tag-404, version
// mismatch and copy-EPERM were all indistinguishable in EvolverUpgradeAttempt.
// Each branch now returns _fail(code, detail); the reporter encodes it as
// `error = code + ': ' + detail`, so operators can GROUP BY the code prefix
// without any hub schema / DB migration. Codes are a small stable set — keep
// new ones coarse and additive so historical `error LIKE 'code%'` queries
// don't churn.
const FORCE_UPDATE_FAIL_CODES = Object.freeze({
  INSTALL_GUARD_NAME_MISMATCH: 'install_guard_name_mismatch',
  INSTALL_GUARD_UNREADABLE: 'install_guard_unreadable',
  BAD_REQUIRED_VERSION: 'bad_required_version',
  CURRENT_VERSION_UNPARSABLE: 'current_version_unparsable',
  NPX_NOT_FOUND: 'npx_not_found',
  DEGIT_TIMEOUT: 'degit_timeout',
  DEGIT_FAILED: 'degit_failed',
  DOWNLOAD_INCOMPLETE: 'download_incomplete',
  DOWNLOADED_VERSION_MISMATCH: 'downloaded_version_mismatch',
  DELETE_FAILED: 'delete_failed',
  COPY_FAILED: 'copy_failed',
  ALL_CHANNELS_EXHAUSTED: 'all_channels_exhausted',
});

// Build the structured failure result that replaces a bare `return false`.
// Shape: { ok:false, code, detail }. Distinct from `true`, FORCE_UPDATE_NOOP
// and FORCE_UPDATE_BUSY, so the three call sites' `result === true` /
// `result === SENTINEL` checks keep classifying it as "failed" unchanged —
// this is backward compatible. Frozen so a downstream consumer cannot mutate
// the code/detail before it is reported. detail is best-effort context (an
// errno, a version delta, an entry name); it is redacted + truncated to
// ERROR_MAX by the reporter before it leaves the process.
function _fail(code, detail) {
  return Object.freeze({
    ok: false,
    code: String(code),
    detail: detail == null ? '' : String(detail),
  });
}

// Compact "CODE: message" rendering of a thrown error for the detail field.
function _errStr(e) {
  if (!e) return 'unknown';
  var code = e.code ? String(e.code) + ': ' : '';
  return code + (e.message != null ? String(e.message) : String(e));
}

// Map a Channel 1 (GitHub Release / degit) throw to a structured failure.
// `phase` records how far the try block got before throwing, so a readFileSync
// ENOENT (truncated download) is not misread as an npx ENOENT (npx missing):
//   'degit' -> the npx/degit spawn itself
//   'parse' -> degit exited 0 but the downloaded package.json is missing/invalid
//   'copy'  -> the staged tree downloaded fine but cpSync into INSTALL_ROOT failed
function _classifyChannel1Error(e, phase) {
  if (phase === 'delete') {
    var deleteEntry = e && e._evolverEntry ? String(e._evolverEntry) + ': ' : '';
    return _fail(FORCE_UPDATE_FAIL_CODES.DELETE_FAILED, deleteEntry + _errStr(e));
  }
  if (phase === 'copy') {
    var entry = e && e._evolverEntry ? String(e._evolverEntry) + ': ' : '';
    return _fail(FORCE_UPDATE_FAIL_CODES.COPY_FAILED, entry + _errStr(e));
  }
  if (phase === 'parse') {
    return _fail(FORCE_UPDATE_FAIL_CODES.DOWNLOAD_INCOMPLETE,
      'missing/invalid package.json in downloaded tree: ' + _errStr(e));
  }
  // phase === 'degit' (the spawn). ENOENT here is the npx binary itself, not a
  // file inside the download — that distinction is exactly why `phase` exists.
  if (e && e.code === 'ENOENT') {
    return _fail(FORCE_UPDATE_FAIL_CODES.NPX_NOT_FOUND, _errStr(e));
  }
  // execFileSync timeout kills the child with SIGTERM (and sets .killed); some
  // platforms surface ETIMEDOUT instead. Either way it is a 60s timeout.
  if (e && (e.killed || e.signal === 'SIGTERM' || e.code === 'ETIMEDOUT')) {
    return _fail(FORCE_UPDATE_FAIL_CODES.DEGIT_TIMEOUT,
      'degit timed out after 60s' + (e.signal ? ' (signal=' + e.signal + ')' : ''));
  }
  // Generic degit/network/tag-not-found failure. degit prints the real reason
  // ("could not find commit hash for v…", "could not resolve host") to stderr,
  // so keep a tail of it. Redact + strip control chars HERE, before the tail
  // slice: the downstream reporter redact (a2aProtocol.reportForceUpdateOutcome)
  // runs after this, so slicing first could chop a token's prefix anchor and
  // let the bare value slip past the prefix-anchored redact patterns. Stripping
  // ANSI/NUL/newlines also keeps the persisted error free of terminal-injection
  // sequences and log-line noise.
  var detail = _errStr(e);
  var stderr = '';
  if (e && e.stderr != null) {
    try {
      var redactString = require('./gep/sanitize').redactString;
      stderr = redactString(String(e.stderr)).replace(/[\x00-\x1f\x7f]/g, ' ').trim();
    } catch (_) {
      // sanitize unavailable — still strip control chars so logs stay clean.
      stderr = String(e.stderr).replace(/[\x00-\x1f\x7f]/g, ' ').trim();
    }
  }
  if (stderr) detail += ' | stderr=' + stderr.slice(-300);
  return _fail(FORCE_UPDATE_FAIL_CODES.DEGIT_FAILED, detail);
}

function _isRetryableFsLockError(e) {
  var code = e && e.code;
  return code === 'EPERM' || code === 'EBUSY' || code === 'EACCES' ||
    code === 'ENOTEMPTY' || code === 'EMFILE' || code === 'ENFILE';
}

function _waitForFsLockRetry() {
  var until = Date.now() + 200;
  while (Date.now() < until) { /* spin */ }
}

function _retryFsLockOperation(fn) {
  var err = null;
  for (var attempt = 0; attempt < 3; attempt++) {
    try {
      return fn();
    } catch (e) {
      err = e;
      if (!_isRetryableFsLockError(e)) break;
      if (attempt < 2) _waitForFsLockRetry();
    }
  }
  throw err;
}

function _recoverPackageCommitMarkerIfMissing(installRoot) {
  var pkgDst = path.join(installRoot, 'package.json');
  if (fs.existsSync(pkgDst)) return false;
  var entries;
  try {
    entries = fs.readdirSync(installRoot);
  } catch (_) {
    return false;
  }
  var backups = entries
    .filter(function (name) { return /^package\.json\.\d+\.evolver-old$/.test(name); })
    .sort();
  for (var i = backups.length - 1; i >= 0; i--) {
    try {
      fs.renameSync(path.join(installRoot, backups[i]), pkgDst);
      console.warn('[ForceUpdate] Recovered package.json commit marker from ' + backups[i]);
      return true;
    } catch (_) {}
  }
  return false;
}

function _restorePackageBackup(pkgBackup, pkgDst) {
  if (!fs.existsSync(pkgBackup)) return false;
  if (fs.existsSync(pkgDst)) {
    try { fs.rmSync(pkgBackup, { force: true }); } catch (_) {}
    return false;
  }
  try {
    fs.renameSync(pkgBackup, pkgDst);
    return true;
  } catch (_) {
    return false;
  }
}

function _isForceUpdateKeepEntry(name) {
  return name === 'node_modules' || name === 'memory' || name === '.git' || name === 'MEMORY.md' ||
    name === '.env' || name === '.env.local' || name === 'USER.md' || name === '.evolver';
}

// Module-level mutex: shared by every caller that requires('../forceUpdate'),
// so the heartbeat-thread trigger in a2aProtocol.js and the evolve-tick path
// in enrich/pipeline cannot run executeForceUpdate concurrently. This is a
// process-local guard only; it does not protect against two separate node
// processes upgrading the same install root simultaneously (out of scope --
// distinct processes have distinct install layouts in practice).
let _inFlight = false;

function parseConcreteSemver(version) {
  var match = CONCRETE_SEMVER_RE.exec(normalizeConcreteSemver(version));
  if (!match) return null;
  return {
    major: match[1],
    minor: match[2],
    patch: match[3],
    prerelease: match[4] ? match[4].split('.') : [],
  };
}

function normalizeConcreteSemver(version) {
  var normalized = String(version || '').replace(/^v(?=\d)/, '');
  return CONCRETE_SEMVER_RE.test(normalized) ? normalized : '';
}

function normalizeRequiredVersion(raw) {
  return normalizeConcreteSemver(String(raw || '').replace(/^[>=^~\s]+/, ''));
}

function isNumericPrereleaseIdentifier(value) {
  return /^\d+$/.test(value);
}

function compareNumericIdentifierStrings(left, right) {
  if (left.length !== right.length) return left.length - right.length;
  if (left < right) return -1;
  if (left > right) return 1;
  return 0;
}

function comparePrereleaseIdentifiers(left, right) {
  var leftNumeric = isNumericPrereleaseIdentifier(left);
  var rightNumeric = isNumericPrereleaseIdentifier(right);
  if (leftNumeric && rightNumeric) return compareNumericIdentifierStrings(left, right);
  if (leftNumeric) return -1;
  if (rightNumeric) return 1;
  if (left < right) return -1;
  if (left > right) return 1;
  return 0;
}

function compareConcreteSemver(left, right) {
  var a = parseConcreteSemver(left);
  var b = parseConcreteSemver(right);
  if (!a || !b) return null;
  var majorCmp = compareNumericIdentifierStrings(a.major, b.major);
  if (majorCmp !== 0) return majorCmp;
  var minorCmp = compareNumericIdentifierStrings(a.minor, b.minor);
  if (minorCmp !== 0) return minorCmp;
  var patchCmp = compareNumericIdentifierStrings(a.patch, b.patch);
  if (patchCmp !== 0) return patchCmp;
  if (!a.prerelease.length && !b.prerelease.length) return 0;
  if (!a.prerelease.length) return 1;
  if (!b.prerelease.length) return -1;
  var max = Math.max(a.prerelease.length, b.prerelease.length);
  for (var i = 0; i < max; i++) {
    if (a.prerelease[i] === undefined) return -1;
    if (b.prerelease[i] === undefined) return 1;
    var cmp = comparePrereleaseIdentifiers(a.prerelease[i], b.prerelease[i]);
    if (cmp !== 0) return cmp;
  }
  return 0;
}

// Force Update: triggered by Hub when version is critically outdated.
// Extracted from src/evolve.js so both the evolve main loop and heartbeat
// thread can trigger it independently (heartbeat-only workers need this
// because they never reach the evolve run() loop that consumes the pending
// force_update directive).
//
// CRITICAL (issue #51): this function MUST operate on the evolver INSTALL
// directory, NOT getRepoRoot(). getRepoRoot() preferentially returns the
// user's surrounding project (process.cwd()'s nearest .git ancestor).
// Using it here would delete the user's project files and copy the
// evolver package on top of them. Always use getEvolverInstallRoot(),
// which resolves to the package containing this file regardless of
// install layout (global npm / local node_modules / dev clone).
function executeForceUpdate(forceUpdate) {
  // Concurrency guard: if a prior invocation is still in flight, refuse and
  // return the BUSY sentinel. The in-flight caller owns the outcome (state
  // file write, process.exit(78) on success); a second concurrent attempt
  // would (a) race the atomic-rename state-file writes and clobber the first
  // attempt's telemetry row, and (b) potentially double-exit. See
  // FORCE_UPDATE_BUSY docstring above for context.
  if (_inFlight) {
    console.log('[ForceUpdate] BUSY: another invocation already in flight, skipping');
    return FORCE_UPDATE_BUSY;
  }
  _inFlight = true;
  try {
    return _executeForceUpdateInner(forceUpdate);
  } finally {
    // Always release the mutex, even on throw. Callers may rely on retrying
    // after a failure (e.g. heartbeat cooldown), so the flag MUST NOT remain
    // set after the function returns/throws. Note: on a successful upgrade,
    // _executeForceUpdateInner returns true and the caller invokes
    // process.exit(78); the finally still runs before exit -- which is fine,
    // there is nothing else to coordinate with at that point.
    _inFlight = false;
  }
}

function _executeForceUpdateInner(forceUpdate) {
  const INSTALL_ROOT = getEvolverInstallRoot();

  // Defense in depth: if a future refactor breaks path resolution and
  // INSTALL_ROOT no longer points at the evolver package (no package.json
  // / wrong package name), refuse the update rather than risk
  // overwriting an unrelated directory. This is the last guard between
  // the deletion loop and the user's data.
  try {
    const pkg = JSON.parse(fs.readFileSync(path.join(INSTALL_ROOT, 'package.json'), 'utf8'));
    if (!pkg || (pkg.name !== '@evomap/evolver' && pkg.name !== 'evolver')) {
      console.warn('[ForceUpdate] Refusing — ' + INSTALL_ROOT +
        '/package.json has name="' + (pkg && pkg.name) +
        '", expected "@evomap/evolver". Aborting to avoid data loss.');
      return _fail(FORCE_UPDATE_FAIL_CODES.INSTALL_GUARD_NAME_MISMATCH,
        'install root package.json name="' + (pkg && pkg.name) + '", expected "@evomap/evolver"');
    }
  } catch (e) {
    if (_recoverPackageCommitMarkerIfMissing(INSTALL_ROOT)) {
      try {
        const recoveredPkg = JSON.parse(fs.readFileSync(path.join(INSTALL_ROOT, 'package.json'), 'utf8'));
        if (!recoveredPkg || (recoveredPkg.name !== '@evomap/evolver' && recoveredPkg.name !== 'evolver')) {
          console.warn('[ForceUpdate] Refusing — recovered ' + INSTALL_ROOT +
            '/package.json has name="' + (recoveredPkg && recoveredPkg.name) +
            '", expected "@evomap/evolver". Aborting to avoid data loss.');
          return _fail(FORCE_UPDATE_FAIL_CODES.INSTALL_GUARD_NAME_MISMATCH,
            'recovered install root package.json name="' + (recoveredPkg && recoveredPkg.name) +
            '", expected "@evomap/evolver"');
        }
      } catch (recoverReadErr) {
        console.warn('[ForceUpdate] Refusing — cannot read recovered ' + INSTALL_ROOT +
          '/package.json: ' + (recoverReadErr && recoverReadErr.message || recoverReadErr));
        return _fail(FORCE_UPDATE_FAIL_CODES.INSTALL_GUARD_UNREADABLE,
          'cannot read recovered install root package.json: ' + _errStr(recoverReadErr));
      }
    } else {
      console.warn('[ForceUpdate] Refusing — cannot read ' + INSTALL_ROOT +
        '/package.json: ' + (e && e.message || e));
      return _fail(FORCE_UPDATE_FAIL_CODES.INSTALL_GUARD_UNREADABLE,
        'cannot read install root package.json: ' + _errStr(e));
    }
  }

  const requiredVersion = normalizeRequiredVersion(forceUpdate.required_version);
  if (!requiredVersion) {
    console.warn('[ForceUpdate] Refusing — required_version "' +
      String(forceUpdate.required_version || '').replace(/^[>=^~\s]+/, '') +
      '" is not a concrete semver (ranges not accepted).');
    return _fail(FORCE_UPDATE_FAIL_CODES.BAD_REQUIRED_VERSION,
      'required_version=' + JSON.stringify(forceUpdate && forceUpdate.required_version) + ' is not a concrete semver');
  }

  function getCurrentVersion() {
    try {
      var pkg = JSON.parse(fs.readFileSync(path.join(INSTALL_ROOT, 'package.json'), 'utf8'));
      return pkg.version || '0.0.0';
    } catch (_) { return '0.0.0'; }
  }

  // Idempotency / anti-downgrade short-circuit: the hub keeps re-issuing the
  // same force_update directive until the node reports success. After a
  // successful upgrade + restart (process.exit(78)), the next heartbeat may
  // still carry the same directive. Without this early return, a transient
  // Channel 1 failure (npx unavailable, network blip, EBUSY) would cause
  // executeForceUpdate to return false and overwrite the previous successful
  // run's state file with a bogus "failed" -- even though we are already at or
  // above the target version.
  //
  // Compare the ACTUAL current running version (which reflects the new
  // version post-restart) against the parsed requiredVersion. Force-update is
  // a minimum-version floor, not an exact-version pin: a node running 1.88.4
  // must not be downgraded to satisfy a 1.88.3 floor. Only reached after the
  // strip+validate above, so a garbage / unparseable required_version will NOT
  // short-circuit -- it falls into the validation failure branch above and
  // returns false safely.
  var currentVersion = getCurrentVersion();
  var versionCmp = compareConcreteSemver(currentVersion, requiredVersion);
  if (versionCmp === null) {
    console.warn('[ForceUpdate] Refusing — current installed version "' +
      currentVersion + '" is not a concrete semver.');
    return _fail(FORCE_UPDATE_FAIL_CODES.CURRENT_VERSION_UNPARSABLE,
      'current installed version "' + currentVersion + '" is not a concrete semver');
  }
  if (versionCmp >= 0) {
    console.log('[ForceUpdate] already satisfies required version, no-op (current=' +
      currentVersion + ', required=' + requiredVersion + ')');
    // Return the dedicated sentinel rather than `true`. Callers use this to
    // (a) emit status="skipped" telemetry instead of a phantom "success"
    // row in EvolverUpgradeAttempt with from_version == to_version, and
    // (b) skip the process.exit(78) restart — there is nothing to restart
    // for when the binary didn't change.
    return FORCE_UPDATE_NOOP;
  }

  console.log('[ForceUpdate] Starting update (target: ' + requiredVersion +
    ', install root: ' + INSTALL_ROOT + ')');

  // Use os.tmpdir() for staging — INSTALL_ROOT's parent (e.g.
  // /usr/lib/node_modules/@evomap when globally installed) is often not
  // writable, unlike the previous user-project parent.
  // mkdtempSync produces a random suffix, preventing predictable-path pre-population.
  const TMP_TARGET = fs.mkdtempSync(path.join(os.tmpdir(), '.evolver-update-tmp-'));

  // Channel 1: GitHub Release (via degit pinned to exact version tag)
  //
  // channel1Failure captures the structured reason this channel failed, so the
  // terminal `return` can surface it instead of a bare `false`. `phase` tracks
  // how far we got before any throw, so _classifyChannel1Error can tell a
  // degit-spawn failure (phase 'degit') from a truncated download (phase
  // 'parse') from a delete/copy-into-INSTALL_ROOT failure.
  var channel1Failure = null;
  var phase = 'degit';
  try {
    console.log('[ForceUpdate] Channel 1: GitHub Release download (v' + requiredVersion + ')...');
    var npxBin = process.platform === 'win32' ? 'npx.cmd' : 'npx';
    // Pin to exact git tag so we download a specific published release, not
    // whatever is currently at HEAD (which could be a different, unreviewed commit).
    // --force: mkdtempSync pre-creates TMP_TARGET; some degit versions refuse a pre-existing dest.
    execFileSync(npxBin, ['-y', 'degit', '--force', 'EvoMap/evolver#v' + requiredVersion, TMP_TARGET], {
      encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'],
      timeout: 60000, windowsHide: true, maxBuffer: MAX_EXEC_BUFFER,
    });
    phase = 'parse';
    var tmpPkg = JSON.parse(fs.readFileSync(path.join(TMP_TARGET, 'package.json'), 'utf8'));
    // Require exact version match — a ">=" check would allow a compromised hub to
    // request version "0.0.1" and install any version including unreleased HEAD code.
    if (tmpPkg.version && tmpPkg.version === requiredVersion) {
      var entries = fs.readdirSync(INSTALL_ROOT, { withFileTypes: true });
      for (var ei = 0; ei < entries.length; ei++) {
        var eName = entries[ei].name;
        // package.json is the install's commit marker: keep the OLD one in
        // place through the entire delete+copy below and swap in the new one
        // atomically at the very end (see "commit marker" block). If it were
        // deleted here and any later cpSync threw (ENOSPC, a Windows lock that
        // outlasts the retries, a kill), the install root would be left with
        // no package.json — and the install-guard at the top of this function
        // refuses on an unreadable package.json, wedging the node in
        // install_guard_unreadable on every subsequent attempt with no path
        // that ever re-copies it. Deferring it keeps the install self-healing.
        if (_isForceUpdateKeepEntry(eName) || eName === 'package.json') continue;
        try {
          (function (entryName) {
            phase = 'delete';
            _retryFsLockOperation(function () {
              fs.rmSync(path.join(INSTALL_ROOT, entryName), {
                recursive: true, force: true, maxRetries: 3, retryDelay: 200,
              });
            });
          })(eName);
        } catch (rmErr) {
          console.warn('[ForceUpdate] rmSync failed for ' + eName + ': ' + (rmErr.message || rmErr));
          try { rmErr._evolverEntry = eName; } catch (_) {}
          throw rmErr;
        }
      }
      phase = 'copy';
      var newEntries = fs.readdirSync(TMP_TARGET, { withFileTypes: true });
      for (var ni = 0; ni < newEntries.length; ni++) {
        // Deferred: package.json is the commit marker, written last after every
        // other entry has copied successfully (see below). Keep-list entries are
        // local state and must not be overwritten by the downloaded release.
        if (newEntries[ni].name === 'package.json' || _isForceUpdateKeepEntry(newEntries[ni].name)) continue;
        var src = path.join(TMP_TARGET, newEntries[ni].name);
        var dst = path.join(INSTALL_ROOT, newEntries[ni].name);
        try {
          (function (copySrc, copyDst) {
            _retryFsLockOperation(function () {
              fs.cpSync(copySrc, copyDst, { recursive: true });
            });
          })(src, dst);
        } catch (copyErr) {
          console.warn('[ForceUpdate] cpSync failed for ' + newEntries[ni].name + ': ' + (copyErr.message || copyErr));
          // Tag the failing entry so _classifyChannel1Error can name it in the
          // copy_failed detail. phase is already 'copy' here.
          try { copyErr._evolverEntry = newEntries[ni].name; } catch (_) {}
          throw copyErr;
        }
      }
      // Commit marker: every other entry copied successfully, so swap in the
      // new package.json LAST. POSIX gets an atomic rename-over-existing. Windows
      // cannot rename over an existing destination, so it first renames the old
      // package.json to a recoverable same-directory backup; the install guard
      // restores that backup on the next tick if the process dies mid-commit.
      var pkgSrc = path.join(TMP_TARGET, 'package.json');
      var pkgDst = path.join(INSTALL_ROOT, 'package.json');
      var pkgTmp = pkgDst + '.' + process.pid + '.evolver-tmp';
      var pkgBackup = pkgDst + '.' + process.pid + '.evolver-old';
      try {
        _retryFsLockOperation(function () {
          try { fs.rmSync(pkgTmp, { force: true }); } catch (_) {}
          fs.cpSync(pkgSrc, pkgTmp);
          if (process.platform === 'win32') {
            if (!fs.existsSync(pkgDst)) _recoverPackageCommitMarkerIfMissing(INSTALL_ROOT);
            try { fs.rmSync(pkgBackup, { force: true }); } catch (_) {}
            fs.renameSync(pkgDst, pkgBackup);
            try {
              fs.renameSync(pkgTmp, pkgDst);
            } catch (commitErr) {
              _restorePackageBackup(pkgBackup, pkgDst);
              throw commitErr;
            }
            try { fs.rmSync(pkgBackup, { force: true }); } catch (_) {}
          } else {
            fs.renameSync(pkgTmp, pkgDst);
          }
        });
      } catch (pkgErr) {
        _restorePackageBackup(pkgBackup, pkgDst);
        try { fs.rmSync(pkgTmp, { force: true }); } catch (_) {}
        console.warn('[ForceUpdate] package.json commit (atomic replace) failed: ' + (pkgErr.message || pkgErr));
        try { pkgErr._evolverEntry = 'package.json commit'; } catch (_) {}
        throw pkgErr;
      }
      try { fs.rmSync(TMP_TARGET, { recursive: true, force: true }); } catch (_) {}
      console.log('[ForceUpdate] GitHub Release update successful: ' + tmpPkg.version);
      return true;
    }
    // degit succeeded and produced a parseable package.json, but it did not
    // satisfy the exact-version check above. Two distinct causes, two codes:
    if (!tmpPkg.version) {
      // degit produced a parseable package.json with no version field — a
      // malformed/incomplete download, not a stale/tampered tag mismatch.
      channel1Failure = _fail(FORCE_UPDATE_FAIL_CODES.DOWNLOAD_INCOMPLETE,
        'downloaded package.json has no version field');
    } else {
      // version present but not the exact tag we asked for (stale tag, mirror
      // lag, or a tampered/redirected tag). Refuse and record the delta.
      channel1Failure = _fail(FORCE_UPDATE_FAIL_CODES.DOWNLOADED_VERSION_MISMATCH,
        'downloaded version=' + JSON.stringify(tmpPkg.version) + ', expected ' + requiredVersion);
    }
    try { fs.rmSync(TMP_TARGET, { recursive: true, force: true }); } catch (_) {}
  } catch (e) {
    channel1Failure = _classifyChannel1Error(e, phase);
    console.warn('[ForceUpdate] GitHub Release failed (' + channel1Failure.code + '):', e && e.message || e);
    try { fs.rmSync(TMP_TARGET, { recursive: true, force: true }); } catch (_) {}
    // Fall through to Channel 2 (manual download URL hint) instead of
    // returning. A Channel 1 error (degit missing, network down, tag not
    // found) still leaves the user a path forward via the release_url.
  }

  // Channel 2: GitHub release (manual download URL only)
  try {
    var releaseUrl = forceUpdate.release_url;
    if (releaseUrl) {
      console.log('[ForceUpdate] Channel 2: GitHub release -- manual download required');
      console.log('[ForceUpdate] Visit: ' + releaseUrl);
    }
  } catch (_) {}

  console.warn('[ForceUpdate] All automatic channels exhausted. Current version: ' + getCurrentVersion());
  // Surface the concrete Channel 1 failure when we have one (the common case:
  // degit/network/copy/version-mismatch). channel1Failure is null only when
  // Channel 1 was never entered, which cannot happen here — but fall back to a
  // terminal code so the reporter never lands on the legacy "returned false".
  return channel1Failure || _fail(FORCE_UPDATE_FAIL_CODES.ALL_CHANNELS_EXHAUSTED,
    'no automatic channel succeeded; current=' + getCurrentVersion() + ' target=' + requiredVersion);
}

// Test-only hook: re-implements the EXACT same operator-strip + semver
// validation as the runtime force_update check. Exists
// so test/forceUpdateLastUpdateReport.test.js can build a parity sweep
// proving that _extractTargetVersion's (a2aProtocol.js) verdict matches
// forceUpdate.js's verdict byte-for-byte on any input -- the comment at
// a2aProtocol.js:823-833 claims this invariant but a hand-maintained
// regex copy can silently drift. Anything that changes this function
// MUST also update _extractTargetVersion (and vice versa) or the
// parity test breaks.
function _isAcceptedRequiredVersionForTesting(raw) {
  if (typeof raw !== 'string') return false;
  return normalizeRequiredVersion(raw) !== '';
}

// Type guard: is `result` a structured failure (vs true / NOOP / BUSY)?
// Call sites use this to decide whether to forward result as opts.failure to
// reportForceUpdateOutcome. Kept tiny and dependency-free so all three
// duplicated triggers (a2aProtocol heartbeat, proxy manager, enrich tick) can
// share one definition.
function isForceUpdateFailure(result) {
  return !!result && typeof result === 'object' && result.ok === false && typeof result.code === 'string';
}

module.exports = {
  executeForceUpdate,
  FORCE_UPDATE_NOOP,
  FORCE_UPDATE_BUSY,
  FORCE_UPDATE_FAIL_CODES,
  isForceUpdateFailure,
  // Test-only hook: reset the in-flight mutex so unit tests do not leak state
  // across cases. Production callers must NOT touch this -- the mutex is the
  // load-bearing invariant that prevents concurrent state-file writes.
  _resetInFlightForTesting: function () { _inFlight = false; },
  _isAcceptedRequiredVersionForTesting: _isAcceptedRequiredVersionForTesting,
};
