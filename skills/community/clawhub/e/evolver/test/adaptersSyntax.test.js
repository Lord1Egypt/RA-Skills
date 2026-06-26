// test/adaptersSyntax.test.js
//
// Parser-syntax guard for entry-point scripts shipped to end users (#542).
//
// `evolver setup-hooks --platform=codex` copies `src/adapters/scripts/*.js`
// verbatim into the user's `.codex/hooks/` directory; the CLI entry
// `index.js` is referenced by `package.json#bin`. A SyntaxError in either
// blocks the user before any code can run, with no workaround.
//
// PR #110 introduced a duplicate `const path = require('path')` in
// evolver-session-end.js, and v1.85.1 / v1.85.2 shipped that to npm —
// fresh installs hit `SyntaxError: Identifier 'path' has already been
// declared` the first time the Stop hook fired. The existing test suite
// never loaded those scripts (they spawn their own node process), so the
// regression made it through pre-publish. `node --check` is parse-only,
// cheap, and runs on every entry-point file unconditionally.
//
// Structure note: this file is loaded by both `node --test` (npm test)
// and `npx vitest run` (pre_publish_check.js). Vitest's node:test
// compat layer can't statically discover `it()` calls registered inside
// a `for` loop — it executes them but the suite-level report shows
// "0 test / No test suite found" and exits non-zero, which trips up
// pre_publish_check (catch branch can't find "# fail 0" pattern and
// blocks publish). The fix is to keep the test count STATIC: each
// runner sees one `it()` per top-level concern, and the dynamic file
// list is iterated INSIDE the test body. Failure messages list every
// failing file so debugging stays just as cheap.

'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const REPO_ROOT = path.resolve(__dirname, '..');

function nodeCheck(absPath) {
  const res = spawnSync(process.execPath, ['--check', absPath], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  return { status: res.status, stderr: res.stderr || '' };
}

function listJsFiles(dirRel) {
  const dirAbs = path.join(REPO_ROOT, dirRel);
  if (!fs.existsSync(dirAbs)) return [];
  return fs.readdirSync(dirAbs)
    .filter((name) => name.endsWith('.js'))
    .map((name) => ({ rel: path.posix.join(dirRel, name), abs: path.join(dirAbs, name) }));
}

describe('entry-point scripts parse without SyntaxError (#542)', () => {
  it('every adapter script in src/adapters/scripts/ passes node --check', () => {
    const targets = listJsFiles('src/adapters/scripts');
    assert.ok(targets.length > 0,
      'expected at least one adapter script to guard — directory empty or missing');

    const failures = [];
    for (const t of targets) {
      const r = nodeCheck(t.abs);
      if (r.status !== 0) {
        failures.push(`  ${t.rel}: ${r.stderr.trim()}`);
      }
    }
    assert.equal(failures.length, 0,
      `node --check failed for ${failures.length} adapter script(s):\n${failures.join('\n')}`);
  });

  it('CLI entry index.js passes node --check', () => {
    const indexJs = path.join(REPO_ROOT, 'index.js');
    if (!fs.existsSync(indexJs)) return; // dist-only builds may omit
    const r = nodeCheck(indexJs);
    assert.equal(r.status, 0, `node --check failed for index.js:\n${r.stderr}`);
  });
});
