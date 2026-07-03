const { describe, it, before, after, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const zlib = require('zlib');

// Strategy: forceUpdate.js destructures `execFileSync` at module load time.
// To inject a stub we must (a) mutate child_process.execFileSync before the
// first require, then (b) purge forceUpdate from cache between tests so each
// freshRequire picks up whatever stub is current.

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
  try {
    return require('../src/forceUpdate');
  } finally {
    childProcess.execFileSync = origExecFileSync;
  }
}

// Fake degit: write a new-version package.json + index.js into TMP_TARGET.
// args layout: ['-y', 'degit', 'EvoMap/evolver', <TMP_TARGET>]
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
    fs.mkdirSync(path.join(tmpTarget, 'src'), { recursive: true });
    fs.writeFileSync(path.join(tmpTarget, 'src', 'evolve.js'), '// src v' + version, 'utf8');
  };
}

function makeDegitWithLocalStateFiles(version) {
  return function (_bin, args) {
    const tmpTarget = args[args.length - 1];
    fs.mkdirSync(tmpTarget, { recursive: true });
    fs.writeFileSync(
      path.join(tmpTarget, 'package.json'),
      JSON.stringify({ name: '@evomap/evolver', version }),
      'utf8',
    );
    fs.writeFileSync(path.join(tmpTarget, 'index.js'), '// v' + version, 'utf8');
    fs.mkdirSync(path.join(tmpTarget, 'src'), { recursive: true });
    fs.writeFileSync(path.join(tmpTarget, 'src', 'evolve.js'), '// src v' + version, 'utf8');
    fs.writeFileSync(path.join(tmpTarget, '.env'), 'A2A_NODE_SECRET=from-release\n', 'utf8');
    fs.writeFileSync(path.join(tmpTarget, '.env.local'), 'DEBUG=from-release\n', 'utf8');
    fs.writeFileSync(path.join(tmpTarget, 'USER.md'), '# release user notes\n', 'utf8');
    fs.mkdirSync(path.join(tmpTarget, '.evolver'), { recursive: true });
    fs.writeFileSync(path.join(tmpTarget, '.evolver', 'config.json'), '{"workspaceId":"release"}', 'utf8');
    fs.mkdirSync(path.join(tmpTarget, 'memory'), { recursive: true });
    fs.writeFileSync(path.join(tmpTarget, 'memory', 'state.json'), '{"from":"release"}', 'utf8');
    fs.mkdirSync(path.join(tmpTarget, 'logs'), { recursive: true });
    fs.writeFileSync(path.join(tmpTarget, 'logs', 'evolver.log'), 'release log\n', 'utf8');
  };
}

function makeNpxMissingThenTarballSuccess(version) {
  return makeDegitFailureThenTarballSuccess(version, Object.assign(new Error('spawnSync npx ENOENT'), {
    code: 'ENOENT',
  }));
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
    { name: 'evolver-' + version + '/index.js', content: '// v' + version, mode: 0o755 },
    { name: 'evolver-' + version + '/src/evolve.js', content: '// tarball src v' + version },
  ].concat(extraEntries || []));
}

function makeDegitFailureThenTarballSuccess(version, degitError) {
  const calls = [];
  const stub = function (bin, args) {
    calls.push({ bin, args: Array.isArray(args) ? args.slice() : [] });
    if (bin === process.execPath) {
      const archivePath = args[3];
      fs.writeFileSync(archivePath, makeReleaseTarball(version));
      return '';
    }
    throw degitError;
  };
  stub.calls = calls;
  return stub;
}

function populateFakeInstall(root) {
  // Package identity (required by the guard at the top of executeForceUpdate)
  fs.writeFileSync(
    path.join(root, 'package.json'),
    JSON.stringify({ name: '@evomap/evolver', version: '1.0.0' }),
    'utf8',
  );
  // Old code that MUST be replaced
  fs.writeFileSync(path.join(root, 'index.js'), '// old', 'utf8');
  fs.mkdirSync(path.join(root, 'src'), { recursive: true });
  fs.writeFileSync(path.join(root, 'src', 'evolve.js'), '// old', 'utf8');
  // Classic keep-list entries (must survive)
  fs.mkdirSync(path.join(root, 'node_modules'), { recursive: true });
  fs.mkdirSync(path.join(root, 'memory'), { recursive: true });
  fs.mkdirSync(path.join(root, '.git'), { recursive: true });
  fs.writeFileSync(path.join(root, 'MEMORY.md'), '# mem\n', 'utf8');
  // New keep-list entries (must survive after this fix)
  fs.writeFileSync(path.join(root, '.env'), 'A2A_HUB_URL=https://hub.example.com\nA2A_NODE_SECRET=s3cr3t\n', 'utf8');
  fs.writeFileSync(path.join(root, '.env.local'), 'DEBUG=1\n', 'utf8');
  fs.writeFileSync(path.join(root, 'USER.md'), '# my notes\n', 'utf8');
  fs.mkdirSync(path.join(root, '.evolver'), { recursive: true });
  fs.writeFileSync(path.join(root, '.evolver', 'config.json'), '{"workspaceId":"wid_test"}', 'utf8');
  fs.mkdirSync(path.join(root, 'logs'), { recursive: true });
  fs.writeFileSync(path.join(root, 'logs', 'evolver.log'), 'local log\n', 'utf8');
}

function assertPrivateArchiveDownload(execStub) {
  const downloadCall = execStub.calls.find((c) => c.bin === process.execPath);
  assert.ok(downloadCall, 'fallback should download via the current node binary');

  const downloaderScript = downloadCall.args[1];
  assert.match(
    downloaderScript,
    /fs\.createWriteStream\(dest,\{flags:'wx',mode:0o600\}\)/,
    'fallback downloader should create the archive exclusively with owner-only permissions',
  );

  const archivePath = downloadCall.args[3];
  const archiveDir = path.dirname(archivePath);
  assert.equal(path.basename(archivePath), 'archive.tar.gz',
    'fallback should use a fixed archive name inside a private directory');
  assert.match(path.basename(archiveDir), /^\.evolver-update-archive-/,
    'fallback archive directory should be mkdtemp-created');
  assert.notEqual(archiveDir, os.tmpdir(),
    'fallback should not write the archive directly under os.tmpdir()');
  assert.doesNotMatch(path.basename(archivePath), /^\.evolver-update-\d+-\d+\.tar\.gz$/,
    'fallback should not use the old predictable top-level archive filename');
  assert.ok(!fs.existsSync(archiveDir), 'fallback should remove the private archive directory');
}

describe('executeForceUpdate: keep-list preserves user config files', () => {
  before(() => {
    installRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-keeplist-'));
  });

  after(() => {
    childProcess.execFileSync = origExecFileSync;
    delete require.cache[pathsModPath];
    delete require.cache[forceUpdateModPath];
    try { fs.rmSync(installRoot, { recursive: true, force: true }); } catch (_) {}
  });

  beforeEach(() => {
    childProcess.execFileSync = origExecFileSync;
    try { fs.rmSync(installRoot, { recursive: true, force: true }); } catch (_) {}
    fs.mkdirSync(installRoot, { recursive: true });
  });

  it('preserves .env, .env.local, USER.md, .evolver/ and replaces old code files', () => {
    populateFakeInstall(installRoot);

    const { executeForceUpdate } = freshRequireForceUpdate(makeSuccessfulDegit('999.999.999'));
    // Match the stub's degit-returned version exactly: the version check in
    // src/forceUpdate.js is now `===` (no range matching) to prevent a
    // compromised hub from coercing an install with a permissive range like
    // '>=0.0.1'. The earlier '>=1.0.0' form encoded the pre-tightening
    // contract.
    const result = executeForceUpdate({ required_version: '999.999.999' });

    assert.equal(result, true, 'update should succeed');

    // --- new keep-list entries ---
    assert.ok(fs.existsSync(path.join(installRoot, '.env')),
      '.env must be preserved (contains hub credentials)');
    assert.equal(
      fs.readFileSync(path.join(installRoot, '.env'), 'utf8'),
      'A2A_HUB_URL=https://hub.example.com\nA2A_NODE_SECRET=s3cr3t\n',
      '.env content must be unchanged',
    );
    assert.ok(fs.existsSync(path.join(installRoot, '.env.local')),
      '.env.local must be preserved');
    assert.ok(fs.existsSync(path.join(installRoot, 'USER.md')),
      'USER.md must be preserved');
    assert.ok(fs.existsSync(path.join(installRoot, '.evolver', 'config.json')),
      '.evolver/config.json must be preserved');
    assert.equal(fs.readFileSync(path.join(installRoot, 'logs', 'evolver.log'), 'utf8'), 'local log\n',
      'logs/ must be preserved because running processes can hold files open');

    // --- classic keep-list entries still intact ---
    assert.ok(fs.existsSync(path.join(installRoot, 'node_modules')), 'node_modules/ preserved');
    assert.ok(fs.existsSync(path.join(installRoot, 'memory')), 'memory/ preserved');
    assert.ok(fs.existsSync(path.join(installRoot, '.git')), '.git/ preserved');
    assert.ok(fs.existsSync(path.join(installRoot, 'MEMORY.md')), 'MEMORY.md preserved');

    // --- old code must be replaced by new version ---
    assert.ok(fs.existsSync(path.join(installRoot, 'index.js')), 'index.js should exist after update');
    assert.equal(
      fs.readFileSync(path.join(installRoot, 'index.js'), 'utf8'),
      '// v999.999.999',
      'index.js is atomically replaced after the new payload commits',
    );
    assert.equal(
      fs.readFileSync(path.join(installRoot, 'src', 'evolve.js'), 'utf8'),
      '// src v999.999.999',
      'src payload must have new version content',
    );
  });

  it('does NOT wipe .env when degit fails (update aborted)', () => {
    populateFakeInstall(installRoot);

    const { executeForceUpdate } = freshRequireForceUpdate(() => {
      throw new Error('simulated network failure');
    });
    // Use a version strictly NEWER than populateFakeInstall's '1.0.0' so we
    // bypass the idempotency short-circuit (which correctly returns true when
    // already at the required version) and actually exercise the degit
    // failure path that this test is asserting on.
    const result = executeForceUpdate({ required_version: '>=2.0.0' });

    assert.equal(result.ok, false, 'update should fail');
    assert.equal(result.code, 'fallback_download_incomplete',
      'terminal telemetry aggregates by the terminal fallback failure');
    assert.match(result.detail, /^primary_failed=degit_failed \| fallback_failed=download_incomplete: .*simulated network failure/,
      'primary and fallback failure context is preserved up front');
    // Deletion loop never runs when degit fails — .env must still be present
    assert.ok(fs.existsSync(path.join(installRoot, '.env')),
      '.env must survive a failed update');
    assert.ok(fs.existsSync(path.join(installRoot, 'index.js')),
      'old index.js must survive a failed update (no replacement happened)');
    assert.equal(fs.readFileSync(path.join(installRoot, 'index.js'), 'utf8'), '// old',
      'failed fallback does not leave the downloaded bootstrap behind');
  });

  it('does NOT overwrite keep-list state even if the release archive contains those paths', () => {
    populateFakeInstall(installRoot);
    fs.writeFileSync(path.join(installRoot, 'memory', 'state.json'), '{"from":"local"}', 'utf8');

    const { executeForceUpdate } = freshRequireForceUpdate(makeDegitWithLocalStateFiles('2.0.0'));
    const result = executeForceUpdate({ required_version: '2.0.0' });

    assert.equal(result, true, 'update should succeed');
    assert.equal(
      fs.readFileSync(path.join(installRoot, '.env'), 'utf8'),
      'A2A_HUB_URL=https://hub.example.com\nA2A_NODE_SECRET=s3cr3t\n',
      '.env must remain local, not release-provided',
    );
    assert.equal(fs.readFileSync(path.join(installRoot, '.env.local'), 'utf8'), 'DEBUG=1\n');
    assert.equal(fs.readFileSync(path.join(installRoot, 'USER.md'), 'utf8'), '# my notes\n');
    assert.equal(
      fs.readFileSync(path.join(installRoot, '.evolver', 'config.json'), 'utf8'),
      '{"workspaceId":"wid_test"}',
    );
    assert.equal(fs.readFileSync(path.join(installRoot, 'memory', 'state.json'), 'utf8'), '{"from":"local"}');
    assert.equal(fs.readFileSync(path.join(installRoot, 'logs', 'evolver.log'), 'utf8'), 'local log\n');
  });

  it('uses the GitHub tarball fallback when npx/degit is unavailable', () => {
    populateFakeInstall(installRoot);

    const execStub = makeNpxMissingThenTarballSuccess('3.0.0');
    const { executeForceUpdate } = freshRequireForceUpdate(execStub);
    const result = executeForceUpdate({ required_version: '3.0.0' });

    assert.equal(result, true, 'tarball fallback should complete the update');
    assert.equal(fs.readFileSync(path.join(installRoot, 'index.js'), 'utf8'), '// v3.0.0',
      'tarball fallback commits the downloaded bootstrap index.js');
    if (process.platform !== 'win32') {
      assert.notEqual(fs.statSync(path.join(installRoot, 'index.js')).mode & 0o111, 0,
        'tarball fallback preserves executable mode for the CLI bootstrap');
    }
    assert.equal(fs.readFileSync(path.join(installRoot, 'src', 'evolve.js'), 'utf8'), '// tarball src v3.0.0');
    assert.equal(fs.readFileSync(path.join(installRoot, 'logs', 'evolver.log'), 'utf8'), 'local log\n');
    assertPrivateArchiveDownload(execStub);
    assert.equal(execStub.calls.some((c) => c.bin === 'tar'), false,
      'fallback should extract without depending on the tar binary');
  });

  it('uses the GitHub tarball fallback when degit itself fails', () => {
    populateFakeInstall(installRoot);

    const execStub = makeDegitFailureThenTarballSuccess('4.0.0', Object.assign(new Error('degit failed'), {
      status: 128,
      stderr: 'fatal: could not read from remote repository\n',
    }));
    const { executeForceUpdate } = freshRequireForceUpdate(execStub);
    const result = executeForceUpdate({ required_version: '4.0.0' });

    assert.equal(result, true, 'tarball fallback should recover from generic degit failure');
    assert.equal(fs.readFileSync(path.join(installRoot, 'index.js'), 'utf8'), '// v4.0.0',
      'generic degit fallback commits the downloaded bootstrap index.js');
    assert.equal(fs.readFileSync(path.join(installRoot, 'src', 'evolve.js'), 'utf8'), '// tarball src v4.0.0');
    assert.ok(execStub.calls.some((c) => c.bin === process.execPath),
      'fallback should download via the current node binary');
    assert.equal(execStub.calls.some((c) => c.bin === 'tar'), false,
      'fallback should extract without depending on the tar binary');
  });

  it('tarball fallback skips traversal and unsupported unsafe entries while stripping the repo root', () => {
    populateFakeInstall(installRoot);
    const escapeName = 'evolver-tar-escape-' + process.pid + '-' + Date.now() + '.txt';
    const escapedPath = path.join(os.tmpdir(), escapeName);
    try { fs.rmSync(escapedPath, { force: true }); } catch (_) {}
    const calls = [];
    const execStub = function (bin, args) {
      calls.push({ bin, args: Array.isArray(args) ? args.slice() : [] });
      if (bin === process.execPath) {
        fs.writeFileSync(args[3], makeReleaseTarball('4.1.0', [
          { name: 'evolver-4.1.0/../' + escapeName, content: 'escaped' },
          { name: 'evolver-4.1.0/unsafe-link', type: '2', content: '../' + escapeName },
        ]));
        return '';
      }
      throw Object.assign(new Error('spawnSync npx ENOENT'), { code: 'ENOENT' });
    };
    execStub.calls = calls;

    const { executeForceUpdate } = freshRequireForceUpdate(execStub);
    const result = executeForceUpdate({ required_version: '4.1.0' });

    assert.equal(result, true, 'safe entries from the tarball should still install');
    assert.equal(fs.readFileSync(path.join(installRoot, 'index.js'), 'utf8'), '// v4.1.0');
    assert.equal(fs.existsSync(escapedPath), false,
      'path traversal entry must not write outside the extraction target');
    assert.equal(fs.existsSync(path.join(installRoot, 'unsafe-link')), false,
      'unsupported symlink entries are skipped conservatively');
    assert.equal(execStub.calls.some((c) => c.bin === 'tar'), false,
      'unsafe-entry coverage must exercise the Node extractor, not system tar');
  });

  it('does not move/delete legacy force-update backups or copy release-provided backups', () => {
    populateFakeInstall(installRoot);
    const legacyBackup = fs.mkdtempSync(path.join(installRoot, '.evolver-force-update-backup-'));
    fs.writeFileSync(
      path.join(legacyBackup, '.evolver-force-update-journal.json'),
      JSON.stringify({ state: 'precommit', requiredVersion: '2.0.0', previousVersion: '1.0.0' }),
      'utf8',
    );
    fs.mkdirSync(path.join(legacyBackup, 'src'), { recursive: true });
    fs.writeFileSync(path.join(legacyBackup, 'src', 'evolve.js'), '// legacy backup src', 'utf8');

    const { executeForceUpdate } = freshRequireForceUpdate(function (_bin, args) {
      const tmpTarget = args[args.length - 1];
      fs.mkdirSync(tmpTarget, { recursive: true });
      fs.writeFileSync(
        path.join(tmpTarget, 'package.json'),
        JSON.stringify({ name: '@evomap/evolver', version: '5.0.0' }),
        'utf8',
      );
      fs.writeFileSync(path.join(tmpTarget, 'index.js'), '// v5.0.0', 'utf8');
      fs.mkdirSync(path.join(tmpTarget, 'src'), { recursive: true });
      fs.writeFileSync(path.join(tmpTarget, 'src', 'evolve.js'), '// src v5.0.0', 'utf8');
      const releaseBackup = path.join(tmpTarget, '.evolver-force-update-backup-release');
      fs.mkdirSync(releaseBackup, { recursive: true });
      fs.writeFileSync(path.join(releaseBackup, 'payload.js'), '// release backup payload', 'utf8');
    });
    const result = executeForceUpdate({ required_version: '5.0.0' });

    assert.equal(result, true, 'update should succeed');
    assert.ok(fs.existsSync(legacyBackup), 'legacy backup directory is left in place for bootstrap cleanup');
    assert.equal(
      fs.readFileSync(path.join(legacyBackup, 'src', 'evolve.js'), 'utf8'),
      '// legacy backup src',
      'legacy backup payload is not nested into the new rollback backup or deleted',
    );
    assert.ok(!fs.existsSync(path.join(installRoot, '.evolver-force-update-backup-release')),
      'release-provided internal backup directories are not copied into the install root');
  });
});
