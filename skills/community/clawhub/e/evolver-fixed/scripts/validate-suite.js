// Usage: node scripts/validate-suite.js [test-glob-pattern]
// Runs the project's test suite (node --test) and fails if any test fails.
// When called without arguments, runs all tests in test/.
// When called with a glob pattern, runs only matching tests.
//
// This script is intended to be used as a Gene validation command.

const { execFileSync } = require('child_process');
const path = require('path');
const fs = require('fs');

function findTestFiles(cwd) {
  const files = [];
  function walk(dir) {
    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const full = path.join(dir, entry.name);
        if (entry.isDirectory()) walk(full);
        else if (entry.isFile() && entry.name.endsWith('.test.js')) files.push(full);
      }
    } catch (e) {}
  }
  walk(path.join(cwd, 'test'));
  return files;
}

const repoRoot = process.cwd();
const testFiles = findTestFiles(repoRoot).sort();

if (testFiles.length === 0) {
  console.error('FAIL: no tests found');
  process.exit(1);
}

try {
  execFileSync(process.execPath, ['--test', ...testFiles], {
    cwd: repoRoot,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: 120000,
    env: Object.assign({}, process.env, {
      NODE_ENV: 'test',
      EVOLVER_REPO_ROOT: repoRoot,
      GEP_ASSETS_DIR: path.join(repoRoot, 'assets', 'gep'),
    }),
    maxBuffer: 50 * 1024 * 1024,
  });
  process.exit(0);
} catch (e) {
  const stdout = e.stdout ? e.stdout.toString('utf8') : '';
  const stderr = e.stderr ? e.stderr.toString('utf8') : '';
  if (stdout) console.error(stdout.slice(-500));
  if (stderr) console.error(stderr.slice(-500));
  console.error('FAIL: test suite exited with code ' + (e.status || 'unknown'));
  process.exit(1);
}
