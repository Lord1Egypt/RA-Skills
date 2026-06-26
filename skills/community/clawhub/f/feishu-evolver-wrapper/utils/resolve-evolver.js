const path = require('path');
const fs = require('fs');

const CANDIDATE_DIRS = [
  '../evolver-private-dev',
  '../private-evolver',
  '../evolver',
  '../capability-evolver',
];

let _resolved = null;

function resolveEvolverDir() {
  if (_resolved !== null) return _resolved;

  if (process.env.EVOLVER_DIR) {
    const envDir = path.resolve(process.env.EVOLVER_DIR);
    if (fs.existsSync(path.join(envDir, 'index.js'))) {
      _resolved = envDir;
      return _resolved;
    }
  }

  for (const d of CANDIDATE_DIRS) {
    const full = path.resolve(__dirname, '..', d);
    if (fs.existsSync(path.join(full, 'index.js'))) {
      _resolved = full;
      return _resolved;
    }
  }

  _resolved = '';
  return _resolved;
}

function requireEvolverModule(modulePath, fallback) {
  const dir = resolveEvolverDir();
  if (dir) {
    try { return require(path.join(dir, modulePath)); }
    catch (e) {}
  }
  if (fallback) {
    try { return require(fallback); }
    catch (e) {}
  }
  return null;
}

module.exports = { resolveEvolverDir, requireEvolverModule, CANDIDATE_DIRS };
