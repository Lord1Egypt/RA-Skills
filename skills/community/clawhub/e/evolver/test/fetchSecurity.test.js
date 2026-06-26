'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');

describe('fetch command hardening (GHSA-r466-rxw4-3j9j)', () => {
  const indexSrc = fs.readFileSync(path.join(__dirname, '..', 'index.js'), 'utf8');

  it('validates --out= path stays inside cwd', () => {
    // The fix wraps the raw --out= value with path.resolve + path.relative and
    // rejects paths that escape the cwd. Guard against regressions that go
    // back to the raw outFlag.slice() pattern without a cwd check.
    assert.ok(/outFlag\.slice\('--out='\.length\)/.test(indexSrc),
      'fetch still parses --out= flag');
    assert.ok(/path\.resolve\(process\.cwd\(\),\s*rawOut\)/.test(indexSrc),
      'fetch must resolve --out= against process.cwd()');
    assert.ok(/rel\.startsWith\('\.\.'\)/.test(indexSrc) || /startsWith\('\.\.'\)/.test(indexSrc),
      'fetch must reject paths escaping cwd via path.relative check');
  });

  it('does not allow the raw --out= value to flow directly into mkdirSync', () => {
    // Source-level check: `fs.mkdirSync(outDir, ...)` in the fetch branch must
    // be preceded by the path.resolve+path.relative containment guard we
    // introduced for GHSA-r466-rxw4-3j9j. We scope the check to the block
    // immediately after the --out= slice so other unrelated outDir vars in
    // index.js do not trigger false positives.
    const sliceIdx = indexSrc.indexOf("outFlag.slice('--out='.length)");
    assert.ok(sliceIdx !== -1, 'fetch still parses --out= flag');
    const window = indexSrc.slice(sliceIdx, sliceIdx + 2000);
    assert.ok(/path\.resolve\(process\.cwd\(\),\s*rawOut\)/.test(window),
      'the --out= slice result must feed into path.resolve(process.cwd(), rawOut) before mkdirSync');
    assert.ok(/rel\.startsWith\('\.\.'\)/.test(window),
      'the --out= branch must reject paths that escape cwd via path.relative check');
  });
});

describe('fetch default-branch containment (GHSA-cfcj-hqpf-hccf)', () => {
  const indexSrc = fs.readFileSync(path.join(__dirname, '..', 'index.js'), 'utf8');

  it('rejects safeId values that collapse to cwd or escape skills/', () => {
    // The fix rejects safeId === '.' / '..' / '' / contains '/' or '\\' or
    // NUL so `path.join('.', 'skills', safeId)` cannot collapse back to cwd
    // and overwrite top-level project files (index.js, package.json).
    assert.ok(/safeId === '\.\.'/.test(indexSrc),
      'fetch must reject safeId === ".."');
    assert.ok(/safeId === '\.'/.test(indexSrc),
      'fetch must reject safeId === "."');
    assert.ok(/safeId === ''/.test(indexSrc),
      'fetch must reject empty safeId');
    assert.ok(/safeId\.includes\('\\\\'\)/.test(indexSrc) || /safeId\.includes\("\\\\\\\\"\)/.test(indexSrc),
      'fetch must reject safeId containing backslash');
  });

  it('applies a traversal check to the default skills/ output branch', () => {
    // In the non --out= branch, the resolved candidate path must be confirmed
    // to live strictly under skills/. Guard against regressions that drop
    // this second relative-path check.
    const marker = "outDir = path.join('.', 'skills', safeId)";
    const legacyIdx = indexSrc.indexOf(marker);
    assert.equal(legacyIdx, -1,
      'fetch default branch must no longer do unchecked path.join("./skills", safeId); use path.resolve + path.relative guard');
    assert.ok(/path\.resolve\(process\.cwd\(\),\s*'skills',\s*safeId\)/.test(indexSrc),
      'fetch default branch must resolve skills/safeId explicitly before containment check');
    assert.ok(/path\.relative\(skillsRoot,\s*candidate\)/.test(indexSrc),
      'fetch default branch must path.relative against skillsRoot to reject traversal');
  });

  it('guards bundled_files writes so no file lands in cwd or escapes outDir', () => {
    // Per-file destination must resolve under outDir, and never equal cwd.
    assert.ok(/path\.resolve\(resolvedOutDir,\s*safeName\)/.test(indexSrc),
      'bundled_files must compute destPath via path.resolve(resolvedOutDir, safeName)');
    assert.ok(/path\.relative\(resolvedOutDir,\s*destPath\)/.test(indexSrc),
      'bundled_files must run path.relative(resolvedOutDir, destPath) containment check');
    assert.ok(/path\.dirname\(destPath\)\s*===\s*resolvedCwd/.test(indexSrc),
      'bundled_files must refuse writes whose parent equals cwd');
  });
});
