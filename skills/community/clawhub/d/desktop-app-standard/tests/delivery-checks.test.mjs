import test from 'node:test';
import assert from 'node:assert/strict';
import {deliveryFindings, assertNsisEnglish} from '../scripts/delivery-checks.mjs';
import {runTraps, defaultContext} from '../scripts/ci-traps.mjs';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';

const ids = (file, text) => deliveryFindings([{file, text}]).map(item => item.id);
test('the installer gate CLI succeeds on explicit English and fails closed on a missing config', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'installer-gate-'));
  const script = fileURLToPath(new URL('../scripts/delivery-checks.mjs', import.meta.url));
  try {
    const config = path.join(root, 'electron-builder.json');
    fs.writeFileSync(config, JSON.stringify({nsis: {installerLanguages: ['en_US'], displayLanguageSelector: false}}));
    assert.equal(spawnSync(process.execPath, [script, '--installer', config]).status, 0);
    assert.notEqual(spawnSync(process.execPath, [script, '--installer', config + '.missing']).status, 0);
    fs.writeFileSync(config, JSON.stringify({nsis: {installerLanguages: ['en_US', 'zh_CN']}}));
    assert.notEqual(spawnSync(process.execPath, [script, '--installer', config]).status, 0);
    const yaml = path.join(root, 'electron-builder.yml');
    fs.writeFileSync(yaml, 'nsis: {installerLanguages: [en_US], displayLanguageSelector: false}\n');
    const unresolved = spawnSync(process.execPath, [script, '--installer', yaml], {encoding: 'utf8'});
    assert.notEqual(unresolved.status, 0);
    assert.match(unresolved.stderr, /YAML parser unavailable/);
  } finally { fs.rmSync(root, {recursive: true, force: true}); }
});
test('delivery source checks catch the application regressions and ignore test fixtures', () => {
  const oldCache = 'Path.Combine(UpdatesRoot, version)';
  assert.ok(ids('app/UpdateService.cs', oldCache).includes('update-cache-architecture'));
  assert.deepEqual(ids('app/UpdateService.cs', '// ' + oldCache), []);
  assert.deepEqual(ids('tests/UpdateService.cs', oldCache), []);
  assert.deepEqual(ids('app/UpdateService.cs', 'Path.Combine(UpdatesRoot, architecture, version)'), []);
  assert.ok(ids('scripts/release-assets.mjs', 'function verifyAssets() { return Object.keys(manifests); }').includes('release-manifest-inventory'));
  assert.ok(ids('scripts/release-assets.mjs', 'assets.filter(a => a.digest && a.digest.startsWith("sha256:"))').includes('release-digest-skipped'));
  assert.deepEqual(ids('scripts/release-assets.mjs', 'requiredManifests.map(name => manifests[name]);'), []);
  assert.ok(ids('tools/release.ps1', 'Get-ChildItem $artifacts -File | Where-Object { $_.Name -like "*.zip" }; Get-FileHash $file').includes('release-checksum-inventory'));
  assert.deepEqual(ids('tools/release.ps1', '$assets | Get-FileHash -Algorithm SHA256'), []);
  assert.ok(ids('tools/release.ps1', 'Compress-Archive -Path (Join-Path $published "*")').includes('archive-incomplete-directory'));
});

test('installer checks reject multilingual configurations and accept explicit English', () => {
  const config = {build: {win: {target: ['nsis']}, nsis: {installerLanguages: ['en_US'], displayLanguageSelector: false}}};
  assert.deepEqual(ids('desktop/package.json', JSON.stringify(config)), []);
  assertNsisEnglish('package.json', JSON.stringify(config));
  config.build.nsis.installerLanguages.push('zh_CN');
  assert.ok(ids('desktop/package.json', JSON.stringify(config)).includes('installer-ui-language'));
  assert.throws(() => assertNsisEnglish('package.json', JSON.stringify(config)), /NSIS requires/);
  for (const yaml of ['nsis: {installerLanguages: [en_US], displayLanguageSelector: false}\n',
    'nsis:\n  installerLanguages: [en_US, zh_CN]\n']) {
    const findings = deliveryFindings([{file: 'electron-builder.yml', text: yaml}]);
    assert.equal(findings.length, 1);
    assert.equal(findings[0].severity, 'notice');
    assert.equal(findings[0].confidence, 'unknown');
  }
  assert.deepEqual(ids('package.json', JSON.stringify({build:{win:{target:['portable']}}})), []);
  const inno = '[Setup]\nShowLanguageDialog=no\n[Languages]\nName: "english"; MessagesFile: "compiler:Default.isl"\n[Files]\n';
  assert.deepEqual(ids('tools/installer/App.iss', inno), []);
  assert.ok(ids('tools/installer/App.iss', inno.replace('Default.isl', 'Languages\\ChineseSimplified.isl')).includes('installer-ui-language'));
});

test('workflow checks catch incomplete archive and checksum rerun patterns', () => {
  const scan = text => runTraps([{file:'release.yml', text}], defaultContext()).map(item => item.id);
  assert.ok(scan('dotnet publish app\nCompress-Archive -Path "$published/*" -DestinationPath app.zip').includes('archive-incomplete-directory'));
  assert.equal(scan('dotnet publish app\ntar -a -c -f app.zip -C $published .').includes('archive-incomplete-directory'), false);
  assert.ok(scan('sha256sum * > SHA256SUMS').includes('checksum-self-reference'));
  assert.equal(scan("find . -type f ! -name SHA256SUMS -print0 | xargs -0 sha256sum > SHA256SUMS").includes('checksum-self-reference'), false);
});
