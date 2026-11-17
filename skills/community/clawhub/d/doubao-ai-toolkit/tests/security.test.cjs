const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const skill = fs.readFileSync(path.join(root, 'SKILL.md'), 'utf8');
const pkg = JSON.parse(fs.readFileSync(path.join(root, 'package.json'), 'utf8'));
const lock = JSON.parse(fs.readFileSync(path.join(root, 'package-lock.json'), 'utf8'));
const npmrc = fs.readFileSync(path.join(root, '.npmrc'), 'utf8');

assert.equal(pkg.dependencies['coze-coding-dev-sdk'], '0.7.32');
assert.equal(pkg.dependencies['seedream-ark'], '0.1.7');
assert.equal(lock.packages[''].dependencies['coze-coding-dev-sdk'], '0.7.32');
assert.equal(lock.packages[''].dependencies['seedream-ark'], '0.1.7');
assert.match(npmrc, /^ignore-scripts=true$/m);
assert(!skill.includes(['npm', 'install', '-g'].join(' ')));
assert(!skill.includes(['--', 'api-key'].join('')));
assert(!skill.includes('Authorization' + ': Bearer'));
assert(!skill.includes('HIGHEST' + ' PRIORITY'));
console.log('doubao-ai-toolkit security checks passed');
