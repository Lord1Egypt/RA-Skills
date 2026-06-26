// Regression guard for #460: index.js must load `.env` BEFORE any
// internal module is required, so that the first time a2aProtocol /
// ATP helpers read process.env.A2A_NODE_SECRET they see the user's
// .env value (not a stale cache / fallback).
//
// This is a static test that reads index.js source and asserts that
// the `dotenv` call appears before the first `require('./src/*')`
// line. No runtime bootstrap is needed (we don't actually want to
// boot evolver from a unit test).
const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');

describe('index.js dotenv load order (regression #460)', () => {
  const indexPath = path.resolve(__dirname, '..', 'index.js');
  const source = fs.readFileSync(indexPath, 'utf8');
  const lines = source.split('\n');

  function firstMatch(regex) {
    for (let i = 0; i < lines.length; i++) {
      if (regex.test(lines[i])) return i;
    }
    return -1;
  }

  it('calls dotenv.config before requiring ./src/evolve', () => {
    const dotenvLine = firstMatch(/require\(['"]dotenv['"]\)\.config/);
    const evolveLine = firstMatch(/require\(['"]\.\/src\/evolve['"]\)/);
    assert.ok(dotenvLine >= 0, 'expected dotenv.config call in index.js');
    assert.ok(evolveLine >= 0, 'expected require("./src/evolve") in index.js');
    assert.ok(
      dotenvLine < evolveLine,
      'dotenv.config must appear BEFORE require("./src/evolve"), otherwise '
        + 'a2aProtocol reads A2A_NODE_SECRET before .env is loaded and may '
        + 'cache a stale secret (cf GitHub issue #460). '
        + `Currently: dotenv at line ${dotenvLine + 1}, evolve at line ${evolveLine + 1}.`
    );
  });

  it('calls dotenv.config before requiring any ./src/* module', () => {
    const dotenvLine = firstMatch(/require\(['"]dotenv['"]\)\.config/);
    const firstSrcRequireLine = firstMatch(/require\(['"]\.\/src\//);
    assert.ok(dotenvLine >= 0, 'expected dotenv.config call in index.js');
    assert.ok(firstSrcRequireLine >= 0, 'expected at least one require("./src/...") in index.js');
    // The only ./src/* require allowed before dotenv is ./src/gep/paths,
    // which is needed to resolve the .env file location and has zero
    // side effects on env-sensitive modules.
    const firstLine = lines[firstSrcRequireLine];
    if (dotenvLine >= firstSrcRequireLine) {
      assert.match(
        firstLine,
        /require\(['"]\.\/src\/gep\/paths['"]\)/,
        `line ${firstSrcRequireLine + 1} requires a ./src/* module before `
          + 'dotenv.config, which risks caching stale secrets (cf #460). '
          + 'Only ./src/gep/paths is allowed there (for resolving .env path).'
      );
    }
  });
});
