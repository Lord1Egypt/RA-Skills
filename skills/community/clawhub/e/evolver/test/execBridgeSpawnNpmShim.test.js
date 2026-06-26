'use strict';

// CVE-2024-27980: Node >= 18.20.2 / 20.12.2 / 21.7.3 refuses to spawn
// .cmd / .bat targets without `shell: true` (throws EINVAL). evolver's
// engines field requires Node >= 22.12, so any Windows code path that
// hands a .cmd to spawn() without shell:true is dead.
//
// _resolveNpmCmdShim addresses this for npm-cli-generated Windows shims
// (anthropic-ai/openai/sst-style packages installed via `npm install -g`)
// by parsing the shim's well-known last line ("%dp0%\<entry>" %*) and
// rewriting (bin, args) into (process.execPath, [<entry>, ...args]).
// spawn(node.exe, ...) sidesteps the .cmd EINVAL entirely.
//
// These tests drive the helper against synthetic shim files in a tmpdir,
// so they pass on any host (POSIX too) and do not require the resolver's
// real PATH lookup. process.platform is overridden via Object.defineProperty
// to exercise the Windows branch on a POSIX test box.

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const execBridge = require('../src/gep/execBridge');
const { __test } = execBridge;

const _realPlatform = Object.getOwnPropertyDescriptor(process, 'platform');
function setPlatform(value) {
  Object.defineProperty(process, 'platform', { value: value, configurable: true });
}
function restorePlatform() {
  if (_realPlatform) Object.defineProperty(process, 'platform', _realPlatform);
}

// Real npm-cli Windows shim format (verbatim from anthropic-ai-sdk.cmd).
// The parser only cares about the trailing exec line; the header is here so
// the fixture is byte-equivalent to what `npm install -g` actually writes.
function realNpmShim(relEntry) {
  return [
    '@ECHO off',
    'GOTO start',
    ':find_dp0',
    'SET dp0=%~dp0',
    'EXIT /b',
    ':start',
    'SETLOCAL',
    'CALL :find_dp0',
    '',
    'IF EXIST "%dp0%\\node.exe" (',
    '  SET "_prog=%dp0%\\node.exe"',
    ') ELSE (',
    '  SET "_prog=node"',
    '  SET PATHEXT=%PATHEXT:;.JS;=;%',
    ')',
    '',
    'endLocal & goto #_undefined_# 2>NUL || title %COMSPEC% & "%_prog%"  "%dp0%\\' + relEntry + '" %*',
    '',
  ].join('\r\n');
}

let tmpRoot;
beforeEach(function () {
  tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'execbridge-npm-shim-'));
});
afterEach(function () {
  try { fs.rmSync(tmpRoot, { recursive: true, force: true }); } catch (_) {}
  restorePlatform();
});

describe('_resolveNpmCmdShim — platform gating', function () {
  it('returns null on POSIX even when bin ends .cmd (a file literally named X.cmd on Linux must spawn directly)', function () {
    setPlatform('linux');
    const shim = path.join(tmpRoot, 'claude.cmd');
    fs.writeFileSync(shim, realNpmShim('node_modules\\@anthropic-ai\\claude-code\\cli.js'));
    fs.mkdirSync(path.join(tmpRoot, 'node_modules', '@anthropic-ai', 'claude-code'), { recursive: true });
    fs.writeFileSync(path.join(tmpRoot, 'node_modules', '@anthropic-ai', 'claude-code', 'cli.js'), '');
    assert.equal(__test.resolveNpmCmdShim(shim, []), null);
  });

  it('returns null on Windows for non-.cmd targets', function () {
    setPlatform('win32');
    assert.equal(__test.resolveNpmCmdShim('C:\\nodejs\\node.exe', []), null);
    assert.equal(__test.resolveNpmCmdShim('claude', []), null);
    assert.equal(__test.resolveNpmCmdShim('script.bat', []), null,
      '.bat shims are not the npm-cli format and the parser anchors on the .cmd suffix');
  });

  it('returns null for null / undefined / empty bin', function () {
    setPlatform('win32');
    assert.equal(__test.resolveNpmCmdShim(null, []), null);
    assert.equal(__test.resolveNpmCmdShim(undefined, []), null);
    assert.equal(__test.resolveNpmCmdShim('', []), null);
  });
});

describe('_resolveNpmCmdShim — npm shim parsing', function () {
  it('rewrites a real npm-cli shim into (node.exe, [<entry>, ...args])', function () {
    setPlatform('win32');
    const rel = path.join('node_modules', '@anthropic-ai', 'claude-code', 'cli.js');
    const shim = path.join(tmpRoot, 'claude.cmd');
    fs.writeFileSync(shim, realNpmShim(rel));
    fs.mkdirSync(path.dirname(path.join(tmpRoot, rel)), { recursive: true });
    fs.writeFileSync(path.join(tmpRoot, rel), '');

    const out = __test.resolveNpmCmdShim(shim, ['-p', 'hello']);
    assert.ok(out, 'parser must recognize a real npm-cli shim');
    assert.equal(out.bin, process.execPath, 'bin must be the running node executable');
    assert.equal(out.args[0], path.resolve(tmpRoot, rel),
      'first arg must be the absolute JS entry path');
    assert.deepEqual(out.args.slice(1), ['-p', 'hello'],
      'remaining args must be forwarded verbatim');
  });

  it('handles entries without a .js extension (npm-cli omits it; Node resolves it)', function () {
    setPlatform('win32');
    const rel = path.join('node_modules', '@anthropic-ai', 'sdk', 'bin', 'cli');
    const shim = path.join(tmpRoot, 'anthropic-ai-sdk.cmd');
    fs.writeFileSync(shim, realNpmShim(rel));
    fs.mkdirSync(path.dirname(path.join(tmpRoot, rel)), { recursive: true });
    fs.writeFileSync(path.join(tmpRoot, rel + '.js'), ''); // entry exists as .js

    const out = __test.resolveNpmCmdShim(shim, []);
    assert.ok(out, 'must accept entries that exist only as <name>.js (npm omits .js in the shim)');
    assert.equal(out.args[0], path.resolve(tmpRoot, rel));
  });

  it('returns null when the shim does not match the npm-cli format (custom wrapper, hand-rolled .cmd)', function () {
    setPlatform('win32');
    const shim = path.join(tmpRoot, 'custom.cmd');
    fs.writeFileSync(shim, '@echo off\r\nrem custom one-off wrapper\r\nnode "C:\\my\\script.js" %*\r\n');
    const out = __test.resolveNpmCmdShim(shim, []);
    assert.equal(out, null,
      'parser must fall through to null so the caller can either spawn-direct (broken on Node 22) or hit a different code path; mis-parsing a hand-rolled .cmd would be worse than not handling it');
  });

  it('returns null when the resolved entry does not exist on disk (broken install)', function () {
    setPlatform('win32');
    const rel = path.join('node_modules', 'missing-pkg', 'cli.js');
    const shim = path.join(tmpRoot, 'orphan.cmd');
    fs.writeFileSync(shim, realNpmShim(rel));
    // intentionally do NOT create the entry file

    const out = __test.resolveNpmCmdShim(shim, []);
    assert.equal(out, null,
      'we must not blindly hand Node a path that does not exist; surfacing as ENOENT mid-spawn is worse than falling back to original bin/args');
  });

  it('returns null when the shim file cannot be read (permission / race)', function () {
    setPlatform('win32');
    const missing = path.join(tmpRoot, 'does-not-exist.cmd');
    const out = __test.resolveNpmCmdShim(missing, []);
    assert.equal(out, null);
  });

  it('handles empty / missing args defensively', function () {
    setPlatform('win32');
    const rel = path.join('node_modules', '@evomap', 'evolver', 'index.js');
    const shim = path.join(tmpRoot, 'evolver.cmd');
    fs.writeFileSync(shim, realNpmShim(rel));
    fs.mkdirSync(path.dirname(path.join(tmpRoot, rel)), { recursive: true });
    fs.writeFileSync(path.join(tmpRoot, rel), '');

    const a = __test.resolveNpmCmdShim(shim, []);
    assert.deepEqual(a.args.slice(1), []);

    const b = __test.resolveNpmCmdShim(shim, undefined);
    assert.deepEqual(b.args.slice(1), [],
      'undefined args must be treated as empty, not blow up at args.slice / spread');

    const c = __test.resolveNpmCmdShim(shim, null);
    assert.deepEqual(c.args.slice(1), []);
  });

  it('preserves the scope segment in scoped package names (@anthropic-ai / @openai / ...)', function () {
    setPlatform('win32');
    const rel = path.join('node_modules', '@openai', 'codex', 'dist', 'cli.js');
    const shim = path.join(tmpRoot, 'codex.cmd');
    fs.writeFileSync(shim, realNpmShim(rel));
    fs.mkdirSync(path.dirname(path.join(tmpRoot, rel)), { recursive: true });
    fs.writeFileSync(path.join(tmpRoot, rel), '');

    const out = __test.resolveNpmCmdShim(shim, []);
    assert.ok(out);
    assert.ok(out.args[0].endsWith(path.join('@openai', 'codex', 'dist', 'cli.js')),
      'scope @ segment must survive the parse — got ' + out.args[0]);
  });
});
