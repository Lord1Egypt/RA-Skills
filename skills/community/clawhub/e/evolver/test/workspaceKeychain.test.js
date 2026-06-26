// Tests for issue #111 Phase 1: keychain-backed workspace-id with FS
// fallback. These tests do NOT depend on `@napi-rs/keyring` being
// installed — the keychain module is treated as optional and we
// inject mock implementations through `require.cache` to exercise the
// hit / miss / migrate / force-throw branches deterministically.

const { test, describe, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { canCreateSymlinks } = require('./helpers/symlink');

// Symlink-rejection tests need to plant a real symlink before exercising
// the code under test; on Windows non-admin that fails with EPERM in
// setup. Route those tests through `symlinkTest` which becomes a no-op
// skip when symlink creation isn't available.
const symlinkTest = canCreateSymlinks() ? test : test.skip;

const PATHS_PATH = require.resolve('../src/gep/paths.js');
const KEYCHAIN_PATH = require.resolve('../src/gep/workspaceKeychain.js');

function freshRequire(modulePath) {
  delete require.cache[modulePath];
  return require(modulePath);
}

function mkTmpWorkspace(prefix) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), prefix));
  fs.mkdirSync(path.join(dir, 'workspace'), { recursive: true });
  return path.join(dir, 'workspace');
}

// Replace workspaceKeychain.js in the require cache with a mock that
// records all calls and lets each test pre-seed its own state.
function installKeychainMock({
  available = true,
  initialEntries = {},
  readReportsUnavailable = false, // simulate mid-execution unavailability (locked keyring)
  writeFails = false,             // simulate keychain write rejection
} = {}) {
  const store = new Map(Object.entries(initialEntries));
  const calls = { read: [], write: [], loadAddon: 0 };
  const mock = {
    KEYCHAIN_SERVICE: 'evomap.evolver.workspace-id',
    getMode() {
      const raw = String(process.env.EVOLVER_WORKSPACE_KEYCHAIN || 'auto').toLowerCase().trim();
      if (raw === 'force' || raw === 'off' || raw === 'auto') return raw;
      return 'auto';
    },
    loadAddon() {
      calls.loadAddon++;
      return available ? { Entry: function () {} } : null;
    },
    readFromKeychain(account) {
      calls.read.push(account);
      if (!available) return { available: false, id: null };
      if (readReportsUnavailable) return { available: false, id: null };
      const id = store.get(account) || null;
      return { available: true, id };
    },
    writeToKeychain(account, id) {
      calls.write.push({ account, id });
      if (!available) return false;
      if (writeFails) return false;
      store.set(account, id);
      return true;
    },
  };
  require.cache[KEYCHAIN_PATH] = {
    id: KEYCHAIN_PATH,
    filename: KEYCHAIN_PATH,
    loaded: true,
    exports: mock,
    children: [],
    paths: [],
  };
  return { mock, store, calls };
}

function clearKeychainMock() {
  delete require.cache[KEYCHAIN_PATH];
}

describe('workspace-id keychain integration (issue #111 Phase 1)', () => {
  let savedEnv;
  let workspace;

  beforeEach(() => {
    savedEnv = {
      EVOLVER_WORKSPACE_ID: process.env.EVOLVER_WORKSPACE_ID,
      EVOLVER_WORKSPACE_KEYCHAIN: process.env.EVOLVER_WORKSPACE_KEYCHAIN,
      OPENCLAW_WORKSPACE: process.env.OPENCLAW_WORKSPACE,
    };
    delete process.env.EVOLVER_WORKSPACE_ID;
    delete process.env.EVOLVER_WORKSPACE_KEYCHAIN;
    workspace = mkTmpWorkspace('evolver-111-');
    process.env.OPENCLAW_WORKSPACE = workspace;
    delete require.cache[PATHS_PATH];
    clearKeychainMock();
  });

  afterEach(() => {
    for (const [k, v] of Object.entries(savedEnv)) {
      if (v === undefined) delete process.env[k];
      else process.env[k] = v;
    }
    try { fs.rmSync(path.dirname(workspace), { recursive: true, force: true }); } catch { /* */ }
    delete require.cache[PATHS_PATH];
    clearKeychainMock();
  });

  test('EVOLVER_WORKSPACE_ID env always wins, regardless of mode', () => {
    process.env.EVOLVER_WORKSPACE_ID = 'overridden-by-env';
    process.env.EVOLVER_WORKSPACE_KEYCHAIN = 'force';
    installKeychainMock({ available: false });
    const paths = freshRequire(PATHS_PATH);
    assert.equal(paths.getWorkspaceId(), 'overridden-by-env');
  });

  test('mode=off bypasses keychain entirely (FS only)', () => {
    process.env.EVOLVER_WORKSPACE_KEYCHAIN = 'off';
    const { calls } = installKeychainMock({ available: true });
    const paths = freshRequire(PATHS_PATH);
    const id = paths.getWorkspaceId();
    assert.match(id, /^[a-f0-9]{32}$/);
    assert.equal(calls.read.length, 0, 'mode=off must not read keychain');
    assert.equal(calls.write.length, 0, 'mode=off must not write keychain');
    assert.ok(fs.existsSync(path.join(workspace, '.evolver', 'workspace-id')));
  });

  test('mode=auto with addon unavailable falls back to FS silently', () => {
    process.env.EVOLVER_WORKSPACE_KEYCHAIN = 'auto';
    const { calls } = installKeychainMock({ available: false });
    const paths = freshRequire(PATHS_PATH);
    const id = paths.getWorkspaceId();
    assert.match(id, /^[a-f0-9]{32}$/);
    assert.equal(calls.read.length, 0, 'unavailable addon must short-circuit before read');
    const onDisk = fs.readFileSync(path.join(workspace, '.evolver', 'workspace-id'), 'utf8').trim();
    assert.equal(onDisk, id, 'FS must hold the same id when addon is unavailable');
  });

  test('mode=force throws when addon is unavailable', () => {
    process.env.EVOLVER_WORKSPACE_KEYCHAIN = 'force';
    installKeychainMock({ available: false });
    const paths = freshRequire(PATHS_PATH);
    assert.throws(() => paths.getWorkspaceId(), /EVOLVER_WORKSPACE_KEYCHAIN=force/);
  });

  test('mode=auto with addon hit returns keychain value without touching FS', () => {
    process.env.EVOLVER_WORKSPACE_KEYCHAIN = 'auto';
    const seeded = '0123456789abcdef0123456789abcdef';
    const { calls } = installKeychainMock({
      available: true,
      initialEntries: { [workspace]: seeded },
    });
    const paths = freshRequire(PATHS_PATH);
    const id = paths.getWorkspaceId();
    assert.equal(id, seeded);
    assert.equal(calls.read.length, 1);
    assert.equal(calls.write.length, 0, 'a clean keychain hit must not re-write');
    assert.ok(!fs.existsSync(path.join(workspace, '.evolver', 'workspace-id')),
      'a keychain hit must not lazily create the FS file');
  });

  test('mode=auto with FS-only secret migrates into keychain and KEEPS FS file', () => {
    process.env.EVOLVER_WORKSPACE_KEYCHAIN = 'auto';
    const fsId = 'fedcba9876543210fedcba9876543210';
    fs.mkdirSync(path.join(workspace, '.evolver'), { recursive: true });
    fs.writeFileSync(path.join(workspace, '.evolver', 'workspace-id'), fsId + '\n', { mode: 0o600 });

    const { calls, store } = installKeychainMock({ available: true });
    const paths = freshRequire(PATHS_PATH);
    const id = paths.getWorkspaceId();

    assert.equal(id, fsId, 'returned id must match the pre-existing FS secret');
    assert.equal(calls.read.length, 1, 'keychain miss path triggers one read');
    assert.equal(calls.write.length, 1, 'FS-only secret must be migrated into keychain');
    assert.equal(store.get(workspace), fsId);
    assert.ok(fs.existsSync(path.join(workspace, '.evolver', 'workspace-id')),
      'FS file MUST be retained after migration so bun-compiled binaries (which can\'t require the addon yet — Phase 2) still see the same id');
  });

  test('mode=auto with empty keychain + empty FS generates id, writes both', () => {
    process.env.EVOLVER_WORKSPACE_KEYCHAIN = 'auto';
    const { calls, store } = installKeychainMock({ available: true });
    const paths = freshRequire(PATHS_PATH);
    const id = paths.getWorkspaceId();
    assert.match(id, /^[a-f0-9]{32}$/);
    assert.equal(store.get(workspace), id, 'new id must be mirrored to keychain');
    const fsContent = fs.readFileSync(path.join(workspace, '.evolver', 'workspace-id'), 'utf8').trim();
    assert.equal(fsContent, id, 'new id must also land on FS for cross-binary handoff');
    assert.equal(calls.write.length, 1);
  });

  test('writer + reader resolve the same id when only keychain is populated', () => {
    process.env.EVOLVER_WORKSPACE_KEYCHAIN = 'auto';
    installKeychainMock({ available: true });
    const paths = freshRequire(PATHS_PATH);
    const writerId = paths.getWorkspaceId();
    const readerId = paths.getWorkspaceId();
    assert.equal(writerId, readerId);
    assert.match(writerId, /^[a-f0-9]{32}$/);
  });

  test('default mode (no env set) is auto', () => {
    // No EVOLVER_WORKSPACE_KEYCHAIN set.
    delete process.env.EVOLVER_WORKSPACE_KEYCHAIN;
    const keychain = freshRequire(KEYCHAIN_PATH);
    assert.equal(keychain.getMode(), 'auto');
  });

  test('unknown EVOLVER_WORKSPACE_KEYCHAIN value normalizes to auto', () => {
    process.env.EVOLVER_WORKSPACE_KEYCHAIN = 'YOLO';
    const keychain = freshRequire(KEYCHAIN_PATH);
    assert.equal(keychain.getMode(), 'auto');
  });

  test('auto/force/off mode names are case-insensitive', () => {
    process.env.EVOLVER_WORKSPACE_KEYCHAIN = 'FORCE';
    const k1 = freshRequire(KEYCHAIN_PATH);
    assert.equal(k1.getMode(), 'force');
    process.env.EVOLVER_WORKSPACE_KEYCHAIN = ' Off ';
    const k2 = freshRequire(KEYCHAIN_PATH);
    assert.equal(k2.getMode(), 'off');
  });

  // Regression test for Bugbot PR #121 round-1 HIGH: the refactor split
  // the original monolithic getWorkspaceId() into _readWorkspaceIdFromFs
  // and _writeWorkspaceIdToFs. The read helper retained the directory-
  // symlink guard but the write helper called mkdirSync({recursive:true})
  // through a symlinked `.evolver`, dropping the secret outside the
  // workspace. PR #109 round-2 HIGH originally hardened against this and
  // we must not regress.
  symlinkTest('refuses to write through a symlinked .evolver dir (Bugbot PR#121 round-1 HIGH; original PR#109 round-2 HIGH)', () => {
    process.env.EVOLVER_WORKSPACE_KEYCHAIN = 'off'; // exercise write path directly
    // Pre-place .evolver as a symlink to an attacker-controlled dir.
    const attackerDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-111-attacker-'));
    fs.symlinkSync(attackerDir, path.join(workspace, '.evolver'));

    const paths = freshRequire(PATHS_PATH);
    const id = paths.getWorkspaceId();
    assert.equal(id, null, 'symlinked .evolver must yield null, never a write through the link');

    // Critically: NO secret file in the attacker-controlled target.
    assert.ok(!fs.existsSync(path.join(attackerDir, 'workspace-id')),
      'mkdirSync({recursive:true}) must not be allowed to traverse a symlinked .evolver and drop the secret outside the workspace');
    try { fs.rmSync(attackerDir, { recursive: true, force: true }); } catch { /* */ }
  });

  symlinkTest('mode=auto with addon-hit MISS still refuses symlinked .evolver write', () => {
    process.env.EVOLVER_WORKSPACE_KEYCHAIN = 'auto';
    const attackerDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-111-attacker2-'));
    fs.symlinkSync(attackerDir, path.join(workspace, '.evolver'));

    installKeychainMock({ available: true }); // keychain miss → falls into write path
    const paths = freshRequire(PATHS_PATH);
    const id = paths.getWorkspaceId();
    assert.equal(id, null);
    assert.ok(!fs.existsSync(path.join(attackerDir, 'workspace-id')),
      'keychain auto path must not write the secret through a symlinked .evolver either');
    try { fs.rmSync(attackerDir, { recursive: true, force: true }); } catch { /* */ }
  });

  // Bugbot PR #121 round-2 MEDIUM (Agentic Security): `force` mode
  // must NOT silently fall back to FS read/write — that would defeat
  // the entire purpose of opting into keychain-only handling.
  test('mode=force on a fresh workspace mints + writes keychain-only, NEVER touches FS', () => {
    process.env.EVOLVER_WORKSPACE_KEYCHAIN = 'force';
    const { calls, store } = installKeychainMock({ available: true });
    const paths = freshRequire(PATHS_PATH);
    const id = paths.getWorkspaceId();
    assert.match(id, /^[a-f0-9]{32}$/);
    assert.equal(store.get(workspace), id, 'force mode must persist via keychain');
    assert.ok(!fs.existsSync(path.join(workspace, '.evolver', 'workspace-id')),
      'force mode must NEVER create the FS file (would re-introduce same-uid plaintext exposure)');
    assert.equal(calls.write.length, 1);
  });

  test('mode=force throws when keychain read reports unavailable mid-call (locked keyring)', () => {
    process.env.EVOLVER_WORKSPACE_KEYCHAIN = 'force';
    installKeychainMock({ available: true, readReportsUnavailable: true });
    const paths = freshRequire(PATHS_PATH);
    assert.throws(() => paths.getWorkspaceId(), /keychain reports unavailable/);
    assert.ok(!fs.existsSync(path.join(workspace, '.evolver', 'workspace-id')),
      'force + locked keyring must NOT silently degrade to FS write');
  });

  test('mode=force throws when keychain write fails (read empty + write rejected)', () => {
    process.env.EVOLVER_WORKSPACE_KEYCHAIN = 'force';
    installKeychainMock({ available: true, writeFails: true });
    const paths = freshRequire(PATHS_PATH);
    assert.throws(() => paths.getWorkspaceId(), /keychain write failed/);
    assert.ok(!fs.existsSync(path.join(workspace, '.evolver', 'workspace-id')),
      'force + keychain-write-failure must throw, never mirror to FS');
  });

  test('mode=auto with keychain reporting unavailable (locked keyring) DOES fall back to FS', () => {
    process.env.EVOLVER_WORKSPACE_KEYCHAIN = 'auto';
    installKeychainMock({ available: true, readReportsUnavailable: true });
    const paths = freshRequire(PATHS_PATH);
    const id = paths.getWorkspaceId();
    // auto mode degrades gracefully — locked keyring should NOT block
    // the user from getting a workspace-id at all.
    assert.match(id, /^[a-f0-9]{32}$/);
    assert.ok(fs.existsSync(path.join(workspace, '.evolver', 'workspace-id')),
      'auto mode + locked keyring must fall back to FS (it is the documented escape hatch)');
  });

  test('mode=force does NOT migrate a pre-existing FS secret (refuses to read it)', () => {
    process.env.EVOLVER_WORKSPACE_KEYCHAIN = 'force';
    const fsId = 'aaaabbbbccccdddd0000111122223333';
    fs.mkdirSync(path.join(workspace, '.evolver'), { recursive: true });
    fs.writeFileSync(path.join(workspace, '.evolver', 'workspace-id'), fsId + '\n', { mode: 0o600 });

    const { store } = installKeychainMock({ available: true });
    const paths = freshRequire(PATHS_PATH);
    const id = paths.getWorkspaceId();
    // force mode generates a fresh id keychain-side, ignoring the FS file.
    assert.match(id, /^[a-f0-9]{32}$/);
    assert.notEqual(id, fsId, 'force mode must not read the FS secret (would defeat keychain-only enforcement)');
    assert.equal(store.get(workspace), id);
  });
});

// Direct unit tests for the readFromKeychain NoEntry/PlatformFailure
// discrimination (Bugbot PR #121 round-3 MEDIUM). The mock used in the
// suite above shortcuts loadAddon — these tests exercise the REAL
// readFromKeychain against a fake `@napi-rs/keyring` addon shape and
// prove the `available: false` branch is reachable, not dead code.
describe('readFromKeychain error-class discrimination (real impl)', () => {
  const ADDON_PATH = '@napi-rs/keyring';
  let savedCache;

  function installFakeAddon(getPasswordImpl) {
    const fake = {
      Entry: function (service, account) {
        this.service = service;
        this.account = account;
      },
    };
    fake.Entry.prototype.getPassword = getPasswordImpl;
    fake.Entry.prototype.setPassword = function () { /* no-op */ };
    // Hijack Module._cache so `require('@napi-rs/keyring')` resolves
    // to our fake even when the real package isn't installed.
    const Module = require('module');
    const fakeId = '__fake_napi_keyring__';
    require.cache[fakeId] = {
      id: fakeId, filename: fakeId, loaded: true, exports: fake,
      children: [], paths: [],
    };
    const orig = Module._resolveFilename;
    savedCache = { orig, fakeId };
    Module._resolveFilename = function (req, ...rest) {
      if (req === ADDON_PATH) return fakeId;
      return orig.call(this, req, ...rest);
    };
  }

  function uninstallFakeAddon() {
    if (savedCache) {
      const Module = require('module');
      Module._resolveFilename = savedCache.orig;
      delete require.cache[savedCache.fakeId];
      savedCache = null;
    }
  }

  afterEach(() => {
    uninstallFakeAddon();
    delete require.cache[KEYCHAIN_PATH];
  });

  test('libsecret-style "No matching entry" → available:true, id:null (clean miss)', () => {
    installFakeAddon(function () {
      throw new Error('No matching entry found in secure storage');
    });
    const keychain = freshRequire(KEYCHAIN_PATH);
    const r = keychain.readFromKeychain('/some/workspace');
    assert.deepEqual(r, { available: true, id: null });
  });

  test('macOS-style "could not be found" → available:true, id:null (clean miss)', () => {
    installFakeAddon(function () {
      throw new Error('The specified item could not be found in the keychain');
    });
    const keychain = freshRequire(KEYCHAIN_PATH);
    const r = keychain.readFromKeychain('/some/workspace');
    assert.deepEqual(r, { available: true, id: null });
  });

  test('Windows-style "Element not found" → available:true, id:null (clean miss)', () => {
    installFakeAddon(function () {
      throw new Error('Element not found.');
    });
    const keychain = freshRequire(KEYCHAIN_PATH);
    const r = keychain.readFromKeychain('/some/workspace');
    assert.deepEqual(r, { available: true, id: null });
  });

  test('locked-keyring failure → available:FALSE (proves force-unavailable path is REACHABLE)', () => {
    installFakeAddon(function () {
      throw new Error('Keyring is locked, cannot read');
    });
    const keychain = freshRequire(KEYCHAIN_PATH);
    const r = keychain.readFromKeychain('/some/workspace');
    assert.deepEqual(r, { available: false, id: null },
      'a locked keyring must surface as unavailable, not silently masquerade as a clean miss');
  });

  test('platform-binding failure → available:FALSE', () => {
    installFakeAddon(function () {
      throw new Error('Platform credential storage failure: D-Bus session not available');
    });
    const keychain = freshRequire(KEYCHAIN_PATH);
    const r = keychain.readFromKeychain('/some/workspace');
    assert.deepEqual(r, { available: false, id: null });
  });

  test('_isNoEntryError correctly classifies the documented platform messages', () => {
    const keychain = freshRequire(KEYCHAIN_PATH);
    assert.equal(keychain._isNoEntryError(new Error('No matching entry found in secure storage')), true);
    assert.equal(keychain._isNoEntryError(new Error('The specified item could not be found in the keychain')), true);
    assert.equal(keychain._isNoEntryError(new Error('Element not found.')), true);
    assert.equal(keychain._isNoEntryError(new Error('NoEntry')), true);
    assert.equal(keychain._isNoEntryError(new Error('Keyring locked')), false);
    assert.equal(keychain._isNoEntryError(new Error('D-Bus session unavailable')), false);
    assert.equal(keychain._isNoEntryError(new Error('Ambiguous credential')), false);
    assert.equal(keychain._isNoEntryError(null), false);
    assert.equal(keychain._isNoEntryError(undefined), false);
  });
});
