#!/usr/bin/env node

const assert = require('assert');
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const expectedRepo = 'https://github.com/harrylabsj/changebrief';

function run(command, args, options = {}) {
  execFileSync(command, args, {
    cwd: root,
    stdio: options.capture ? 'pipe' : 'inherit',
    encoding: 'utf8',
  });
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));
}

function readText(file) {
  return fs.readFileSync(path.join(root, file), 'utf8');
}

function assertNoStaleRepoLinks(text, file) {
  assert(
    !text.includes('openclaw-skill-changebrief'),
    `${file} still references the old repository slug`,
  );
}

function main() {
  console.log('[verify] checking JavaScript syntax');
  run('node', ['--check', 'src/index.js']);
  run('node', ['--check', 'bin/cli.js']);
  run('node', ['--check', 'test/test.js']);

  console.log('[verify] running unit tests');
  run('npm', ['test']);

  console.log('[verify] running CLI smoke test');
  const cliOutput = execFileSync('node', [
    'bin/cli.js',
    'brief',
    '--before-text',
    '计划 4 月上线，暂时不需要法务审批。',
    '--after-text',
    '计划改为 5 月上线，需要先完成法务审批。',
  ], { cwd: root, encoding: 'utf8' });
  assert(cliOutput.includes('哪些旧结论可能失效'), 'CLI brief missing stale-conclusion section');
  assert(cliOutput.includes('最值得立刻行动的 3 个变化'), 'CLI brief missing priority section');

  console.log('[verify] checking metadata');
  const pkg = readJson('package.json');
  const clawhub = readJson('clawhub.json');
  const skill = readText('SKILL.md');
  const readme = readText('README.md');

  assert.strictEqual(clawhub.version, pkg.version, 'clawhub.json version must match package.json');
  assert(skill.includes(`version: ${pkg.version}`), 'SKILL.md frontmatter version must match package.json');
  assert.strictEqual(pkg.repository.url, expectedRepo, 'package repository URL is stale');
  assert.strictEqual(clawhub.repository, expectedRepo, 'clawhub repository URL is stale');

  for (const file of ['package.json', 'clawhub.json', 'README.md', 'SKILL.md']) {
    assertNoStaleRepoLinks(readText(file), file);
  }

  assert(readme.includes('npm run verify'), 'README should document the verification command');
  console.log('[verify] ok');
}

main();
