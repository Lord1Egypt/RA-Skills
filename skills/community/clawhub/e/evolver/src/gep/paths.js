const path = require('path');
const fs = require('fs');
const os = require('os');

let _cachedRepoRoot = null;

// Resolve the git repository that evolver should treat as its work area.
//
// Precedence:
//   1. EVOLVER_REPO_ROOT (explicit override, always wins)
//   2. Nearest ancestor of process.cwd() that has a .git
//      (user ran evolver from inside their project)
//   3. Nearest ancestor of evolver's own directory that has a .git
//      (local npm install: evolver is inside the project's node_modules)
//   4. evolver's own directory if it has a .git (dev mode fallback)
//   5. Fall back to evolver's own directory.
//
//   CWD is checked first because the user's intent is almost always to
//   evolve the project they're standing in, not evolver itself.  evolver
//   self-evolution happens naturally when CWD *is* the evolver repo.
//
//   To opt out, set EVOLVER_NO_PARENT_GIT=true.  The older
//   EVOLVER_USE_PARENT_GIT=true flag is still honored for forward
//   compatibility but is no longer required.
function getRepoRoot() {
  // Always check EVOLVER_REPO_ROOT first, even when a cached value exists.
  // .env is loaded during index.js bootstrap AFTER this function has
  // already been called at least once (for locating the .env file
  // itself). Caching the pre-dotenv result would permanently shadow any
  // EVOLVER_REPO_ROOT later populated from .env. See #526.
  if (process.env.EVOLVER_REPO_ROOT) {
    _cachedRepoRoot = process.env.EVOLVER_REPO_ROOT;
    return _cachedRepoRoot;
  }

  if (_cachedRepoRoot) return _cachedRepoRoot;

  const ownDir = path.resolve(__dirname, '..', '..');

  const noParent = String(process.env.EVOLVER_NO_PARENT_GIT || '').toLowerCase() === 'true';
  // Older flag kept for backward compatibility. Setting it to 'false'
  // explicitly is treated as an opt-out, mirroring EVOLVER_NO_PARENT_GIT.
  const legacyFlag = process.env.EVOLVER_USE_PARENT_GIT;
  const legacyOptOut = typeof legacyFlag === 'string' && legacyFlag.toLowerCase() === 'false';

  // Both upward walks below must stop at the parent of the nearest
  // `node_modules` ancestor — never escape into whatever `.git` happens
  // to live above it (issue #541). On macOS with Homebrew, the global
  // install lives at `/opt/homebrew/lib/node_modules/@evomap/evolver`
  // and `/opt/homebrew` is itself a git repo; an unbounded walk
  // therefore resolves repoRoot to `/opt/homebrew`, sending
  // workspaceRoot / memoryDir / evolutionDir to a directory that
  // doesn't belong to the user and silently producing evolution
  // proposals for the wrong codebase.
  //
  // Boundary semantics: returns the parent of the nearest `node_modules`
  // ancestor (inclusive — a `.git` at that parent IS still picked up),
  // or null if `dir` is not inside any `node_modules` (dev clone /
  // user project root). Callers stop AFTER checking the boundary path
  // itself.
  //
  // For a local install (`<project>/node_modules/@evomap/evolver`), the
  // parent of node_modules IS the user's project, so the boundary
  // includes `<project>` and `<project>/.git` is still picked up
  // correctly. For a dev clone, the boundary is null and the walk is
  // unbounded as before.
  function _nodeModulesBoundary(dir) {
    const segments = dir.split(path.sep);
    const nmIdx = segments.lastIndexOf('node_modules');
    if (nmIdx <= 0) return null;
    return segments.slice(0, nmIdx).join(path.sep) || path.sep;
  }

  function _walkForGit(start) {
    const stopAt = _nodeModulesBoundary(start);
    let dir = start;
    while (dir !== path.dirname(dir)) {
      if (fs.existsSync(path.join(dir, '.git'))) {
        if (!process.env.EVOLVER_QUIET_PARENT_GIT) {
          // Diagnostic, not data. Goes to stderr so it cannot poison
          // a child process's stdout-as-JSON contract — the Stop hook
          // emits JSON on stdout, and any caller invoking the hook via
          // `execFileSync(...).stdout` + `JSON.parse(...)` would crash
          // if this line landed there first. test/sessionEndHook.test.js
          // was failing 5/5 locally for exactly this reason.
          console.error('[evolver] Using host git repository at:', dir);
        }
        return dir;
      }
      if (stopAt !== null && dir === stopAt) break;
      dir = path.dirname(dir);
    }
    return null;
  }

  // Walk upward from process.cwd() — the project the user is standing in.
  // Bounded the same way as the ownDir walk: a user who `cd`s into the
  // global install (e.g. `cd /opt/homebrew/lib/node_modules/@evomap/evolver`
  // to debug) would otherwise hit `/opt/homebrew/.git` here BEFORE the
  // ownDir walk runs, defeating its boundary. The boundary still
  // includes the parent of node_modules, so a user `cd`'d into
  // `<their-project>/node_modules/lodash` still has `<their-project>/.git`
  // picked correctly.
  if (!noParent && !legacyOptOut) {
    const hit = _walkForGit(process.cwd());
    if (hit) {
      _cachedRepoRoot = hit;
      return _cachedRepoRoot;
    }
  }

  // Walk upward from ownDir's parent (local install inside node_modules).
  if (!noParent && !legacyOptOut) {
    const hit = _walkForGit(path.dirname(ownDir));
    if (hit) {
      _cachedRepoRoot = hit;
      return _cachedRepoRoot;
    }
  }

  // Fallback: evolver's own directory (dev mode or isolated install).
  if (fs.existsSync(path.join(ownDir, '.git'))) {
    _cachedRepoRoot = ownDir;
    return _cachedRepoRoot;
  }

  // Final fallback.
  //
  // Opt-out (EVOLVER_NO_PARENT_GIT=true / EVOLVER_USE_PARENT_GIT=false) means
  // "isolated install, treat my own dir as the root" -> ownDir.
  //
  // Otherwise: for a dev clone, ownDir IS the package root and is correct. But
  // for an npm install, ownDir is `<prefix>/node_modules/@evomap/evolver`,
  // the install dir, NOT the user's project. Falling back to it makes the
  // daemon FATAL with "Not a git repository (...\node_modules\@evomap\evolver)"
  // and tell the user to `git init` inside the global install dir, the wrong
  // place (#580 Bug 2). When ownDir is inside a node_modules, prefer
  // process.cwd(): it is where the user is standing and where they should
  // actually `git init`, so the FATAL message points at the right directory.
  // This still satisfies #541's invariant (the cwd/ownDir walks above already
  // returned nothing, so we are not escaping to any host .git).
  if (!noParent && !legacyOptOut && _nodeModulesBoundary(ownDir) !== null) {
    _cachedRepoRoot = process.cwd();
    return _cachedRepoRoot;
  }

  _cachedRepoRoot = ownDir;
  return _cachedRepoRoot;
}

function getWorkspaceRoot() {
  if (process.env.OPENCLAW_WORKSPACE) {
    return process.env.OPENCLAW_WORKSPACE;
  }

  const repoRoot = getRepoRoot();
  const workspaceDir = path.join(repoRoot, 'workspace');
  if (fs.existsSync(workspaceDir)) {
    return workspaceDir;
  }

  return repoRoot;
}

function getLogsDir() {
  return process.env.EVOLVER_LOGS_DIR || path.join(getWorkspaceRoot(), 'logs');
}

function getEvolverLogPath() {
  return path.join(getLogsDir(), 'evolver_loop.log');
}

function getMemoryDir() {
  return process.env.MEMORY_DIR || path.join(getWorkspaceRoot(), 'memory');
}

function getSessionScope() {
  const raw = String(process.env.EVOLVER_SESSION_SCOPE || '').trim();
  if (!raw) return null;
  const safe = raw.replace(/[^a-zA-Z0-9_\-\.]/g, '_').slice(0, 128);
  if (!safe || /^\.{1,2}$/.test(safe) || /\.\./.test(safe)) return null;
  return safe;
}

function getEvolutionDir() {
  const baseDir = process.env.EVOLUTION_DIR || path.join(getMemoryDir(), 'evolution');
  const scope = getSessionScope();
  if (scope) {
    return path.join(baseDir, 'scopes', scope);
  }
  return baseDir;
}

function getGepAssetsDir() {
  const baseDir = process.env.GEP_ASSETS_DIR || path.join(getWorkspaceRoot(), '.evolver', 'gep');
  const scope = getSessionScope();
  if (scope) {
    return path.join(baseDir, 'scopes', scope);
  }
  return baseDir;
}

function getBundledGepAssetsDir() {
  return path.join(getEvolverInstallRoot(), 'assets', 'gep');
}

function getSkillsDir() {
  return process.env.SKILLS_DIR || path.join(getWorkspaceRoot(), 'skills');
}

// Resolve the OpenClaw `sessions` directory for the agent that actually
// matches the current EVOLVER_SESSION_SCOPE (fixes #371).
//
// Precedence:
//   1. AGENT_SESSIONS_DIR         explicit override
//   2. EVOLVER_SESSION_SCOPE with a `workspace-<agent>` prefix =>
//      ~/.openclaw/agents/<agent>/sessions
//   3. AGENT_NAME (defaults to "main")   pre-#371 behavior
function getAgentSessionsDir() {
  if (process.env.AGENT_SESSIONS_DIR) return process.env.AGENT_SESSIONS_DIR;

  const scope = getSessionScope();
  let agentName = null;
  if (scope) {
    const match = /^workspace-(.+)$/.exec(scope);
    if (match) agentName = match[1];
  }
  if (!agentName) agentName = process.env.AGENT_NAME || 'main';

  // Honor an explicit HOME override (used by tests to redirect to a fake
  // home) before falling back to os.homedir(). On POSIX, os.homedir() also
  // reads $HOME first, so this is a no-op in practice on macOS/Linux. On
  // Windows, os.homedir() reads %USERPROFILE% and ignores HOME -- without
  // this fallback, test/paths.test.js cannot inject a fake home and the
  // tests fail with C:\Users\... vs the test's \tmp\home\... expectation.
  // Same pattern as the reset-local-secret fix in eb423dc.
  const home = process.env.HOME || os.homedir();
  return path.join(home, '.openclaw', 'agents', agentName, 'sessions');
}

// Read the first `maxBytes` of a session .jsonl file and extract the `cwd`
// field from its header record (fixes #371, bug 2). The pre-fix matcher
// tailed the file, so it never saw the header. This helper is O(1) on file
// size. Returns null on any read/parse failure.
function readSessionCwdFromHead(sessionFilePath, maxBytes) {
  const cap = typeof maxBytes === 'number' && maxBytes > 0 ? maxBytes : 800;
  try {
    if (!fs.existsSync(sessionFilePath)) return null;
    const fd = fs.openSync(sessionFilePath, 'r');
    try {
      const stat = fs.fstatSync(fd);
      const readSize = Math.min(cap, stat.size);
      if (readSize <= 0) return null;
      const buf = Buffer.alloc(readSize);
      fs.readSync(fd, buf, 0, readSize, 0);
      const newline = buf.indexOf('\n');
      const slice = newline >= 0 ? buf.slice(0, newline) : buf;
      const record = JSON.parse(slice.toString('utf8'));
      if (record && typeof record.cwd === 'string') return record.cwd;
      return null;
    } finally {
      fs.closeSync(fd);
    }
  } catch (_err) {
    return null;
  }
}

function getNarrativePath() {
  return path.join(getEvolutionDir(), 'evolution_narrative.md');
}

function getEvolutionPrinciplesPath() {
  const repoRoot = getRepoRoot();
  const custom = path.join(repoRoot, 'EVOLUTION_PRINCIPLES.md');
  if (fs.existsSync(custom)) return custom;
  return path.join(repoRoot, 'assets', 'gep', 'EVOLUTION_PRINCIPLES.md');
}

function getReflectionLogPath() {
  return path.join(getEvolutionDir(), 'reflection_log.jsonl');
}

// Resolve the evolver INSTALLATION directory (the package containing this file),
// independent of any host git repo or process.cwd().
//
// Use this — never getRepoRoot() — for any operation that mutates evolver's
// own files (force-update, self-PR, integrity rewrites, etc.). getRepoRoot()
// preferentially returns the user's surrounding project so that evolution
// signals are scoped to *their* code; using it for self-mutation will
// overwrite the user's project with evolver's package contents (issue #51).
//
// path.resolve(__dirname, '..', '..') is stable across all install modes:
//   - global npm: /usr/lib/node_modules/@evomap/evolver/src/gep/paths.js
//                 → /usr/lib/node_modules/@evomap/evolver
//   - local install: <project>/node_modules/@evomap/evolver/src/gep/paths.js
//                 → <project>/node_modules/@evomap/evolver
//   - dev clone: /home/user/evolver/src/gep/paths.js → /home/user/evolver
function getEvolverInstallRoot() {
  return path.resolve(__dirname, '..', '..');
}

// Resolve the per-user `~/.evomap` directory, with `EVOLVER_HOME` env var
// override. Lazy (function call, not a module-level `const`) so tests can
// flip `EVOLVER_HOME` per case without monkey-patching `os.homedir`.
//
// Existing call sites used to duplicate `path.join(os.homedir(), '.evomap')`
// across ~9 modules; about two thirds silently ignored `EVOLVER_HOME` (it
// worked for stake bootstrap and claim nudge but not for node-id, device-id,
// feature flags, etc.). #114 consolidates onto this helper so the override
// is uniform and tests don't need to monkey-patch the global homedir
// function (which doesn't compose with `node --test` parallel execution).
function getEvomapDir() {
  return process.env.EVOLVER_HOME || path.join(os.homedir(), '.evomap');
}

// Join sub-segments under `~/.evomap`. Just a convenience wrapper so call
// sites don't have to `path.join(getEvomapDir(), 'mailbox', 'state.json')`
// in two pieces.
function getEvomapPath(...segments) {
  return path.join(getEvomapDir(), ...segments);
}

// Per-workspace random secret used to attest that a memory_graph.jsonl
// entry was written by the same workspace that's now reading it. Stored
// at <workspace>/.evolver/workspace-id with mode 0600 and lazily created
// on first call. Returns null on read/write errors so callers can fall
// back to legacy cwd-tag matching.
//
// Why this exists: when memory_graph.jsonl lives at the user-level path
// (~/.evolver/memory/evolution/memory_graph.jsonl, used by npm-global
// installs), it's shared across every workspace under the same uid. The
// PR #108 cwd-tag layer scopes reads to the current cwd, but `cwd` is a
// plain-text self-report — any process writing the shared file can
// claim a different workspace. workspace-id replaces that self-report
// with a secret that only the legitimate workspace's evolver knows
// (Bugbot PR #108 round-3 Agentic Security Review MEDIUM).
//
// Issue #111 Phase 1: optionally backs the secret with the OS keychain
// (`@napi-rs/keyring` optional dep) to close the same-uid readability
// gap. Mode is controlled by `EVOLVER_WORKSPACE_KEYCHAIN` (auto/force/
// off, default `auto`). FS file is RETAINED on successful keychain
// migration so bun-compiled binaries (which can't `require()` the
// addon yet — Phase 2) still see the same id when handing off to a
// node-CLI session in the same workspace.

// Read the FS-backed workspace-id at <workspace>/.evolver/workspace-id.
// Returns the id on a clean read, null on any error or missing file.
// Symlink rejection matches the pre-keychain hardening from PR #109.
function _readWorkspaceIdFromFs(file) {
  const dir = path.dirname(file);
  try {
    const dirStat = fs.lstatSync(dir, { throwIfNoEntry: false });
    if (dirStat && dirStat.isSymbolicLink()) return null;
    const fileStat = fs.lstatSync(file, { throwIfNoEntry: false });
    if (!fileStat) return null;
    if (fileStat.isSymbolicLink() || !fileStat.isFile()) return null;
    const raw = fs.readFileSync(file, 'utf8').trim();
    if (raw && /^[a-f0-9]{32,}$/i.test(raw)) return raw;
    return null;
  } catch {
    return null;
  }
}

// Atomically create <workspace>/.evolver/workspace-id with the given id
// (or generate one if `id` is null). Returns the id that ended up on
// disk, or null on any unrecoverable error. EEXIST races re-read.
function _writeWorkspaceIdToFs(file, id) {
  const dir = path.dirname(file);
  try {
    // Refuse to write if `.evolver` is a symlink. mkdirSync({recursive:true})
    // happily traverses an existing symlinked directory and the subsequent
    // open() lands the secret file in the attacker-controlled target —
    // O_NOFOLLOW only guards the FINAL path component, not intermediate
    // directories. The pre-refactor monolithic getWorkspaceId() returned
    // null on a symlinked dir before reaching the write; preserve that
    // here (Bugbot PR #121 round-1 HIGH; original guard PR #109 round-2 HIGH).
    const dirStat = fs.lstatSync(dir, { throwIfNoEntry: false });
    if (dirStat && dirStat.isSymbolicLink()) return null;
    fs.mkdirSync(dir, { recursive: true });
    const payload = id || require('crypto').randomBytes(16).toString('hex');
    // Atomic create-and-fail-if-exists so we never overwrite an
    // attacker-pre-placed file (TOCTOU between lstat and writeFileSync
    // could otherwise race a symlink in). O_NOFOLLOW also refuses to
    // follow a symlink that appears between the lstat and open. Both
    // flags exist on Linux/macOS; on Windows O_NOFOLLOW is silently
    // ignored, but Windows has no symlink-by-default risk.
    // NOTE(windows): mode 0o600 passed to openSync is silently ignored on
    // Windows. The workspace-id file will NOT be restricted to owner-read-only.
    // Only Windows user-profile directory ACLs provide isolation. To get
    // proper per-user encryption on Windows, install @napi-rs/keyring — the
    // keychain path above will store the id in Credential Manager (DPAPI)
    // instead of this plaintext file.
    const flags = fs.constants.O_WRONLY | fs.constants.O_CREAT | fs.constants.O_EXCL |
      (fs.constants.O_NOFOLLOW || 0);
    let fd;
    try {
      fd = fs.openSync(file, flags, 0o600);
    } catch (e) {
      if (e && e.code === 'EEXIST') {
        // Another process beat us — re-read with the same symlink guards.
        return _readWorkspaceIdFromFs(file);
      }
      // ELOOP / EMLINK from O_NOFOLLOW hitting a symlink — refuse.
      return null;
    }
    try {
      fs.writeSync(fd, payload + '\n', 0, 'utf8');
    } finally {
      fs.closeSync(fd);
    }
    // Best-effort chmod: silently ignored on Windows (no equivalent ACL API).
    try { fs.chmodSync(file, 0o600); } catch { /* best-effort; no-op on Windows */ }
    return payload;
  } catch {
    return null;
  }
}

function getWorkspaceId() {
  if (process.env.EVOLVER_WORKSPACE_ID) return String(process.env.EVOLVER_WORKSPACE_ID);
  const workspaceRoot = getWorkspaceRoot();
  const dir = path.join(workspaceRoot, '.evolver');
  const file = path.join(dir, 'workspace-id');

  let mode = 'off';
  let keychain = null;
  try {
    keychain = require('./workspaceKeychain');
    mode = keychain.getMode();
  } catch {
    // workspaceKeychain.js missing — degrade silently to FS-only.
    mode = 'off';
  }

  if (mode !== 'off' && keychain) {
    const addonAvailable = keychain.loadAddon() !== null;
    if (mode === 'force' && !addonAvailable) {
      throw new Error(
        'EVOLVER_WORKSPACE_KEYCHAIN=force but @napi-rs/keyring is not installed. ' +
        'Install it (`npm i @napi-rs/keyring`) or set EVOLVER_WORKSPACE_KEYCHAIN=auto/off.'
      );
    }
    if (addonAvailable) {
      const hit = keychain.readFromKeychain(workspaceRoot);
      if (hit.available && hit.id) return hit.id;

      // `force` must NEVER fall back to FS read/write — that would
      // silently re-introduce same-uid plaintext exposure of the
      // workspace secret, which is exactly what `force` exists to
      // prevent (Bugbot PR #121 round-2 MEDIUM Agentic Security).
      // Generate a fresh id and write it ONLY to the keychain; if
      // that write fails, throw rather than mirror to FS.
      if (mode === 'force') {
        if (hit.available) {
          // Keychain reachable but empty — mint and write keychain-only.
          const newId = require('crypto').randomBytes(16).toString('hex');
          if (!keychain.writeToKeychain(workspaceRoot, newId)) {
            throw new Error(
              'EVOLVER_WORKSPACE_KEYCHAIN=force: keychain write failed; ' +
              'refusing to fall back to filesystem secret.'
            );
          }
          return newId;
        }
        // Addon loaded but read claims unavailable (e.g. locked
        // keyring on Linux, no D-Bus session). Refuse rather than
        // silently degrade.
        throw new Error(
          'EVOLVER_WORKSPACE_KEYCHAIN=force: keychain reports unavailable ' +
          '(locked keyring / no session?); refusing to fall back to filesystem.'
        );
      }

      // mode === 'auto', keychain miss — try to migrate an existing
      // FS secret in.
      const fsId = _readWorkspaceIdFromFs(file);
      if (fsId) {
        keychain.writeToKeychain(workspaceRoot, fsId); // best-effort
        return fsId;
      }

      // No secret anywhere — generate, write FS atomically, then
      // mirror to keychain. FS write is the source of truth for the
      // value (race-resistant via O_EXCL); keychain is the upgrade.
      const newId = _writeWorkspaceIdToFs(file, null);
      if (!newId) return null;
      keychain.writeToKeychain(workspaceRoot, newId); // best-effort
      return newId;
    }
    // mode === 'auto' && addon unavailable → fall through to FS.
  }

  // FS-only path (mode === 'off' or auto-fallback). Identical to the
  // pre-#111 implementation in observable behavior.
  const existing = _readWorkspaceIdFromFs(file);
  if (existing) return existing;
  return _writeWorkspaceIdToFs(file, null);
}

module.exports = {
  getRepoRoot,
  getEvolverInstallRoot,
  getWorkspaceRoot,
  getLogsDir,
  getEvolverLogPath,
  getMemoryDir,
  getEvolutionDir,
  getGepAssetsDir,
  getBundledGepAssetsDir,
  getSkillsDir,
  getSessionScope,
  getAgentSessionsDir,
  getWorkspaceId,
  readSessionCwdFromHead,
  getNarrativePath,
  getEvolutionPrinciplesPath,
  getReflectionLogPath,
  getEvomapDir,
  getEvomapPath,
};
