import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { spawnSync } from 'node:child_process';
const base = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
function temp() { return fs.mkdtempSync(path.join(os.tmpdir(), 'desktop-app-standard-test-')); }
function write(root, file, data) { fs.mkdirSync(path.dirname(path.join(root, file)), { recursive: true }); fs.writeFileSync(path.join(root, file), typeof data === 'string' ? data : JSON.stringify(data)); }
const run = (script, args, options = {}) => spawnSync(process.execPath, [path.join(base, 'scripts', script), ...args], { encoding: 'utf8', ...options });

test('CLI reports WPF update caching and release source regressions alongside CI', () => {
  const root = temp();
  try {
    write(root, 'src/App.csproj', '<Project><PropertyGroup><TargetFramework>net10.0-windows</TargetFramework></PropertyGroup></Project>');
    write(root, 'src/UpdateService.cs', 'Path.Combine(UpdatesRoot, version)');
    write(root, 'scripts/release-assets.mjs', 'function verifyAssets() { return Object.keys(manifests); }\nassets.filter(a => a.digest && a.digest.startsWith("sha256:"));');
    write(root, 'tools/installer/App.iss', '[Languages]\nName: "zh"; MessagesFile: "Chinese.isl"\n');
    const result = run('audit.mjs', [root, '--dotnet', '--offline', '--json']);
    assert.equal(result.status, 2, result.stderr);
    const report = JSON.parse(result.stdout);
    for (const id of ['update-cache-architecture', 'release-manifest-inventory', 'release-digest-skipped', 'installer-ui-language']) {
      assert.ok(report.ciFindings.some(finding => finding.id === id), `missing ${id}`);
    }
  } finally { fs.rmSync(root, {recursive: true, force: true}); }
});

test('multiple Tauri apps keep updater settings, workflow steps and findings separate', () => {
  const root = temp();
  assert.equal(path.dirname(root), path.resolve(os.tmpdir()));
  try {
    write(root, 'package.json', {});
    for (const directory of ['apps/a', 'apps/z']) {
      write(root, `${directory}/package.json`, {dependencies: {'@tauri-apps/plugin-updater': '2.0.0'}});
      write(root, `${directory}/package-lock.json`, {packages: {'node_modules/@tauri-apps/plugin-updater': {version: '2.0.0'}}});
    }
    const workflow = ['name: release', 'on: push', 'jobs:', '  build:', '    runs-on: windows-latest', '    steps:',
      '      - uses: tauri-apps/tauri-action@v1', '        with:', '          projectPath: apps/a',
      '      - uses: tauri-apps/tauri-action@v1', '        with:', '          projectPath: apps/z', ''].join('\n');
    write(root, '.github/workflows/release.yml', workflow);
    for (const broken of ['apps/a', 'apps/z']) {
      for (const directory of ['apps/a', 'apps/z']) write(root, `${directory}/src-tauri/tauri.conf.json`, {
        identifier: directory, bundle: {createUpdaterArtifacts: directory !== broken, targets: ['nsis']},
      });
      const result = run('audit.mjs', [root, '--offline', '--json']);
      const report = JSON.parse(result.stdout);
      assert.equal(report.schemaVersion, 3);
      assert.equal(report.tauriConfig, undefined);
      assert.equal(report.applications.length, 2);
      const findings = report.ciFindings.filter(finding => finding.id === 'tauri-updater-manifest');
      assert.deepEqual(findings.map(finding => finding.application), [broken]);
      const expectedLine = broken === 'apps/a' ? 7 : 10;
      assert.equal(findings[0].line, expectedLine);
      assert.deepEqual(report.workflowScopes.map(scope => scope.application), ['apps/a', 'apps/z']);
      const text = run('audit.mjs', [root, '--offline']).stdout;
      assert.ok(text.includes(`[${broken}]`));
    }
    const runWorkflow = ['name: release', 'on: push', 'jobs:', '  build:', '    steps:',
      '      - run: cargo tauri build', '        working-directory: apps/a',
      '      - run: cargo tauri build', '        working-directory: apps/z', ''].join('\n');
    write(root, '.github/workflows/release.yml', runWorkflow);
    assert.equal(run('audit.mjs', [root, '--ci-only', '--json']).status, 0);
    write(root, '.github/workflows/release.yml', runWorkflow.replace('working-directory: apps/a', 'working-directory: ${{ matrix.app }}'));
    const unknown = run('audit.mjs', [root, '--ci-only', '--json']);
    assert.equal(unknown.status, 2);
    const report = JSON.parse(unknown.stdout);
    assert.equal(report.collectionComplete, false);
    assert.equal(report.workflowScopes[0].application, null);
    assert.match(report.warnings.join('\n'), /应用配置检查未完成/);
    assert.equal(report.workflowScopes[1].application, 'apps/z');
  } finally { fs.rmSync(root, {recursive: true, force: true}); }
});

test('a sibling updater and a shared Cargo lock do not enable updates in every app', () => {
  const root = temp();
  assert.equal(path.dirname(root), path.resolve(os.tmpdir()));
  try {
    write(root, 'package.json', {});
    write(root, 'Cargo.lock', '[[package]]\nname = "tauri-plugin-updater"\nversion = "2.0.0"\nsource = "registry+https://github.com/rust-lang/crates.io-index"\n');
    for (const directory of ['a', 'z']) {
      write(root, `${directory}/package.json`, {});
      write(root, `${directory}/src-tauri/tauri.conf.json`, {bundle: {createUpdaterArtifacts: false}});
      write(root, `${directory}/src-tauri/Cargo.toml`, `[dependencies]\ntauri = "2"\n${directory === 'a' ? 'tauri-plugin-updater.workspace = true\n' : ''}`);
    }
    write(root, '.github/workflows/release.yml', ['on: push', 'jobs:', '  build:', '    steps:',
      '      - uses: tauri-apps/tauri-action@v1', '        with:', '          projectPath: a',
      '      - uses: tauri-apps/tauri-action@v1', '        with:', '          projectPath: z', ''].join('\n'));
    const report = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    const findings = report.ciFindings.filter(finding => finding.id === 'tauri-updater-manifest');
    assert.deepEqual(findings.map(finding => finding.application), ['a']);
    write(root, 'z/src-tauri/Cargo.toml', '[dependencies]\ntauri = "2"\ntauri-plugin-updater.workspace = true\n');
    fs.unlinkSync(path.join(root, 'z/src-tauri/tauri.conf.json'));
    const missing = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.ok(missing.warnings.some(warning => warning.startsWith('z:') && warning.includes('没有找到 tauri.conf')));
  } finally { fs.rmSync(root, {recursive: true, force: true}); }
});

test('a shared frontend manifest supports two Tauri shells without config overwrites', () => {
  const root = temp();
  assert.equal(path.dirname(root), path.resolve(os.tmpdir()));
  try {
    write(root, 'package.json', {dependencies: {'@tauri-apps/plugin-updater': '2.0.0'}});
    write(root, 'package-lock.json', {packages: {'node_modules/@tauri-apps/plugin-updater': {version: '2.0.0'}}});
    for (const directory of ['a', 'z']) write(root, `${directory}/src-tauri/tauri.conf.json`, {bundle: {createUpdaterArtifacts: directory === 'z'}});
    write(root, '.github/workflows/release.yml', ['on: push', 'jobs:', '  build:', '    steps:',
      '      - uses: tauri-apps/tauri-action@v1', '        with:', '          projectPath: a',
      '      - uses: tauri-apps/tauri-action@v1', '        with:', '          projectPath: z', ''].join('\n'));
    const report = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.equal(report.applications.length, 2);
    assert.deepEqual(report.ciFindings.filter(finding => finding.id === 'tauri-updater-manifest').map(finding => finding.application), ['a']);
  } finally { fs.rmSync(root, {recursive: true, force: true}); }
});

test('Tauri core and JS API pairing stays within each application', () => {
  const root = temp();
  assert.equal(path.dirname(root), path.resolve(os.tmpdir()));
  try {
    write(root, 'package.json', {});
    for (const [directory, version] of [['a', '2.1.0'], ['z', '2.5.0']]) {
      write(root, `${directory}/package.json`, {dependencies: {'@tauri-apps/api': version}});
      write(root, `${directory}/package-lock.json`, {packages: {'node_modules/@tauri-apps/api': {version}}});
      write(root, `${directory}/src-tauri/tauri.conf.json`, {});
      write(root, `${directory}/src-tauri/Cargo.lock`, `[[package]]\nname = "tauri"\nversion = "${version}"\nsource = "registry+https://github.com/rust-lang/crates.io-index"\n`);
    }
    const report = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.equal(report.frameworkFindings.some(finding => finding.id === 'tauri-api-core-minor-skew'), false);
    assert.deepEqual(report.compatibility.filter(pair => pair.rule === 'tauri-api-same-minor').map(pair => [pair.application, pair.status]), [['a', 'ok'], ['z', 'ok']]);
  } finally { fs.rmSync(root, {recursive: true, force: true}); }
});

test('Electron mac targets and run defaults belong to their own application', () => {
  const root = temp();
  assert.equal(path.dirname(root), path.resolve(os.tmpdir()));
  try {
    write(root, 'package.json', {});
    for (const directory of ['apps/a', 'apps/z']) {
      write(root, `${directory}/package.json`, {dependencies: {'electron-updater': '6.0.0'}, devDependencies: {electron: '45.0.0'}});
      write(root, `${directory}/package-lock.json`, {packages: {
        'node_modules/electron-updater': {version: '6.0.0'}, 'node_modules/electron': {version: '45.0.0'},
      }});
      write(root, `${directory}/electron-builder.yml`, `mac:\n  target: [dmg${directory === 'apps/z' ? ', zip' : ''}]\n`);
    }
    const workflow = ['name: release', 'on: push', 'jobs:', '  a:', '    defaults:', '      run:',
      '        working-directory: apps/a', '    steps:', '      - run: npx electron-builder --mac dmg --publish never',
      '  z:', '    steps:', '      - run: npx electron-builder --mac dmg zip --publish never',
      '        working-directory: apps/z', ''].join('\n');
    write(root, '.github/workflows/release.yml', workflow);
    let report = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.deepEqual(report.workflowScopes.map(scope => scope.application), ['apps/a', 'apps/z']);
    let findings = report.ciFindings.filter(finding => finding.id === 'mac-update-needs-zip');
    assert.deepEqual(findings.map(finding => finding.application), ['apps/a']);
    assert.equal(findings[0].line, 9);
    fs.unlinkSync(path.join(root, '.github/workflows/release.yml'));
    report = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    findings = report.ciFindings.filter(finding => finding.id === 'mac-update-needs-zip');
    assert.deepEqual(findings.map(finding => finding.file), ['apps/a/electron-builder.yml']);
  } finally { fs.rmSync(root, {recursive: true, force: true}); }
});

test('offline npm lock is resolved; script does not run project lifecycle scripts', () => {
  const root = temp();
  try {
    write(root, 'package.json', { devDependencies: { electron: '^2.0.0' }, scripts: { postinstall: 'do-not-execute', test: 'do-not-execute' } });
    write(root, 'package-lock.json', { lockfileVersion: 3, packages: { 'node_modules/electron': { version: '2.1.0' } } });
    const before = fs.readdirSync(root).sort();
    const r = run('audit.mjs', [root, '--offline', '--json']); assert.equal(r.status, 2, r.stderr);
    const out = JSON.parse(r.stdout); assert.equal(out.inventory[0].resolved, '2.1.0'); assert.equal(out.collectionComplete, false);
    assert.deepEqual(fs.readdirSync(root).sort(), before);
  } finally { fs.rmSync(root, { recursive: true }); }
});
test('pnpm lock resolves through importers; an empty pnpm lock stays unknown (never the range)', () => {
  const root = temp(); try {
    write(root, 'package.json', { devDependencies: { electron: '^2.0.0' } });
    write(root, 'pnpm-lock.yaml', "lockfileVersion: '9.0'\nimporters:\n  .:\n    devDependencies:\n      electron:\n        specifier: ^2.0.0\n        version: 2.0.5\n");
    let out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.equal(out.inventory[0].resolved, '2.0.5');
    write(root, 'pnpm-lock.yaml', 'lockfileVersion: 9');
    out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.equal(out.inventory[0].resolved, null); assert.equal(out.inventory[0].declared, '^2.0.0');
  } finally { fs.rmSync(root, { recursive: true }); }
});
test('yarn classic project: resolved from yarn.lock, CI traps in a separate bucket, --ci-only skips inventory', () => {
  const root = temp(); try {
    write(root, 'package.json', { devDependencies: { electron: '^2.0.0', 'electron-builder': '^1.0.0' }, dependencies: { 'electron-updater': '^1.0.0' } });
    write(root, 'yarn.lock', '# yarn lockfile v1\n\nelectron@^2.0.0:\n  version "2.0.8"\n\nelectron-builder@^1.0.0:\n  version "1.0.0"\n\nelectron-updater@^1.0.0:\n  version "1.0.0"\n');
    write(root, '.github/workflows/release.yml', 'on:\n  push:\n    tags: [v*]\njobs:\n  b:\n    runs-on: windows-latest\n    steps:\n      - run: yarn install\n      - run: yarn electron-builder --win portable --publish always\n');
    let out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.equal(out.schemaVersion, 3); assert.equal(out.inventory.find(x => x.name === 'electron').resolved, '2.0.8');
    const ids = out.ciFindings.map(f => f.id);
    for (const id of ['yarn-install-not-frozen', 'electron-updater-windows-target', 'release-permissions', 'platform-coverage', 'yarn-classic']) assert.ok(ids.includes(id), id);
    assert.equal(out.frameworkFindings.some(f => f.id.startsWith('yarn')), false);
    assert.equal(out.ciFindings.find(f => f.id === 'yarn-classic').severity, 'notice');
    out = JSON.parse(run('audit.mjs', [root, '--offline', '--ci-only', '--json']).stdout);
    assert.ok(out.ciFindings.length);
  } finally { fs.rmSync(root, { recursive: true }); }
});
test('documented platform deviation narrows coverage; undocumented one is reported as drift', () => {
  const root = temp(); try {
    write(root, 'package.json', { devDependencies: { electron: '^2.0.0' } });
    write(root, '.github/workflows/release.yml', 'on:\n  push:\n    tags: [v*]\njobs:\n  b:\n    runs-on: windows-latest\n    steps:\n      - run: yarn electron-builder --win nsis --publish never\n      - run: gh release upload v1 x\n');
    const example = fs.readFileSync(path.join(base, 'templates/desktop-policy.example.json'), 'utf8');
    write(root, '.desktop-policy.json', example);
    const defaults = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.ok(defaults.ciFindings.some(f => f.id === 'platform-coverage' && !f.accepted));
    assert.equal(defaults.summary.ciAccepted, 0);
    write(root, '.desktop-policy.json', { deviations: [{ rule: 'platforms', value: ['windows-x64'], reason: 'pilot', revisitWhen: '2027-01-01' }] });
    let ids = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout).ciFindings.map(f => f.id);
    assert.equal(ids.includes('platform-coverage'), false);
    write(root, '.desktop-policy.json', { deviations: [{ rule: 'platforms', value: ['windows-x64'] }] });
    ids = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout).ciFindings.map(f => f.id);
    assert.ok(ids.includes('platform-coverage')); assert.ok(ids.includes('policy-deviation-undocumented'));
    // A bare platforms array that narrows the matrix is drift too, even without a
    // deviations entry to hang the finding on.
    write(root, '.desktop-policy.json', { platforms: ['windows-x64'] });
    ids = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout).ciFindings.map(f => f.id);
    assert.ok(ids.includes('policy-deviation-undocumented'), 'a bare narrowed platforms array must be reported as drift');
      assert.ok(ids.includes('platform-coverage'), 'an undocumented platform list must not suppress coverage checks');
  } finally { fs.rmSync(root, { recursive: true }); }
});
test('policy deviation naming a finding id accepts it (with reason + revisitWhen) and keeps it out of the P counts', () => {
  const root = temp(); try {
    write(root, 'package.json', { devDependencies: { electron: '^2.0.0' } });
    write(root, 'package-lock.json', { lockfileVersion: 3, packages: { 'node_modules/electron': { version: '2.0.0' } } });
    write(root, '.github/workflows/release.yml', 'on:\n  push:\n    tags: [v*]\npermissions:\n  contents: write\njobs:\n  b:\n    runs-on: windows-latest\n    steps:\n      - run: npm test\n      - run: npm pkg set version=${GITHUB_REF_NAME#v}\n      - run: npx electron-builder --win nsis --mac --linux --publish never\n      - run: gh release view v1 || gh release create v1 dist/*\n');
    let out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    const p1 = out.summary.ci.P1; assert.ok(out.ciFindings.find(f => f.id === 'windows-unsigned' && !f.accepted));
    write(root, '.desktop-policy.json', { deviations: [{ rule: 'windows-unsigned', reason: 'cert pending', revisitWhen: '2027-01-01' }] });
    out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    const f = out.ciFindings.find(x => x.id === 'windows-unsigned'); assert.deepEqual(f.accepted, { reason: 'cert pending', revisitWhen: '2027-01-01' });
    assert.equal(out.summary.ci.P1, p1 - 1); assert.equal(out.summary.ciAccepted, 1);
    assert.match(run('audit.mjs', [root, '--offline']).stdout, /已接受的偏离/);
    write(root, '.desktop-policy.json', { deviations: [{ rule: 'windows-unsigned' }] });
    out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.equal(out.ciFindings.find(x => x.id === 'windows-unsigned').accepted, undefined);
    assert.ok(out.ciFindings.some(x => x.id === 'policy-deviation-undocumented'));
  } finally { fs.rmSync(root, { recursive: true }); }
});
test('--dotnet audits TFM/global.json offline without asking for Tauri/Electron', () => {
  const root = temp(); try {
    write(root, 'App/App.csproj', '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net10.0-windows</TargetFramework></PropertyGroup></Project>');
    write(root, 'global.json', '{\n  // team pin\n  "sdk": { "version": "10.0.402", "rollForward": "latestFeature" }\n}');
    write(root, '.github/workflows/ci.yml', 'on: [push]\njobs:\n  test:\n    runs-on: windows-latest\n    steps:\n      - uses: actions/setup-dotnet@v6\n        with:\n          global-json-file: global.json\n      - run: dotnet test\n');
    const r = run('audit.mjs', [root, '--dotnet', '--offline', '--json']);
    assert.equal(r.status, 2, r.stderr);
    const out = JSON.parse(r.stdout);
    assert.equal(out.dotnetRequested, true); assert.equal(out.collectionComplete, false);
    assert.equal(out.dotnet.detected, true); assert.equal(out.dotnet.projects[0].file, 'App/App.csproj');
    assert.deepEqual(out.dotnet.projects[0].tfms.map(t => t.tfm), ['net10.0-windows']);
    assert.equal(out.dotnet.globalJson[0].version, '10.0.402'); assert.equal(out.dotnet.globalJson[0].rollForward, 'latestFeature');
    assert.equal(out.warnings.some(w => /Tauri\/Electron/.test(w)), false);
    assert.equal(out.frameworkFindings.some(f => f.id === 'dotnet-runtime-eol'), false);
  } finally { fs.rmSync(root, { recursive: true }); }
});
test('--dotnet online: official metadata drives support/EOL and latest SDK without GitHub calls', () => {
  const root = temp(); try {
    write(root, 'App/App.csproj', '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net8.0</TargetFramework></PropertyGroup></Project>');
    write(root, 'global.json', { sdk: { version: '8.0.100', rollForward: 'latestFeature' } });
    write(root, '.github/workflows/ci.yml', 'on: [push]\njobs:\n  test:\n    runs-on: windows-latest\n    steps:\n      - run: dotnet test\n');
    write(root, 'mock.mjs', `globalThis.fetch = async (u) => {
      if (u.includes('builds.dotnet.microsoft.com/dotnet/release-metadata/8.0/releases.json')) return { ok: true, status: 200, json: async () => ({
        'latest-sdk': '8.0.426', 'latest-release': '8.0.19', 'support-phase': 'maintenance', 'eol-date': '2020-01-01',
        releases: [{ sdks: [{ version: '8.0.100' }, { version: '8.0.426' }] }]
      })};
      throw Error('Unexpected test URL ' + u);
    };`);
    const r = spawnSync(process.execPath, ['--import', pathToFileURL(path.join(root, 'mock.mjs')).href, path.join(base, 'scripts/audit.mjs'), root, '--dotnet', '--json'], { encoding: 'utf8' });
    assert.equal(r.status, 0, r.stderr);
    const out = JSON.parse(r.stdout);
    assert.equal(out.collectionComplete, true); assert.equal(out.dotnet.channels[0].supportPhase, 'maintenance');
    assert.equal(out.dotnet.channels[0].latestSdk, '8.0.426'); assert.equal(out.dotnet.globalJson[0].guaranteedLatest, true);
    const eol = out.frameworkFindings.find(f => f.id === 'dotnet-runtime-eol');
    assert.equal(eol.severity, 'P0'); assert.match(eol.detail, /2020-01-01/);
    assert.ok(out.ciFindings.some(f => f.id === 'dotnet-ci-setup-missing'));
  } finally { fs.rmSync(root, { recursive: true }); }
});
test('--dotnet online fetches the SDK pin channel too, so an older TFM built by a newer SDK is complete', () => {
  const root = temp(); try {
    write(root, 'App/App.csproj', '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net8.0</TargetFramework></PropertyGroup></Project>');
    write(root, 'global.json', { sdk: { version: '10.0.402', rollForward: 'latestFeature' } });
    write(root, '.github/workflows/ci.yml', 'on: [push]\njobs:\n  test:\n    runs-on: windows-latest\n    steps:\n      - uses: actions/setup-dotnet@v6\n        with:\n          global-json-file: global.json\n');
    write(root, 'mock.mjs', `globalThis.fetch = async (u) => {
      if (u.includes('builds.dotnet.microsoft.com/dotnet/release-metadata/8.0/releases.json')) return { ok: true, status: 200, json: async () => ({
        'latest-sdk': '8.0.426', 'latest-release': '8.0.19', 'support-phase': 'active', 'eol-date': '2028-11-10', releases: []
      })};
      if (u.includes('builds.dotnet.microsoft.com/dotnet/release-metadata/10.0/releases.json')) return { ok: true, status: 200, json: async () => ({
        'latest-sdk': '10.0.402', 'latest-release': '10.0.13', 'support-phase': 'active', 'eol-date': '2028-11-14', releases: [{ sdks: [{ version: '10.0.402' }] }]
      })};
      if (u.includes('/repos/actions/setup-dotnet/releases/latest')) return { ok: true, status: 200, json: async () => ({ tag_name: 'v6.0.0' }) };
      if (u.includes('/repos/actions/setup-dotnet/tags')) return { ok: true, status: 200, json: async () => [{ name: 'v6', commit: { sha: 'a'.repeat(40) } }] };
      throw Error('Unexpected test URL ' + u);
    };`);
    const r = spawnSync(process.execPath, ['--import', pathToFileURL(path.join(root, 'mock.mjs')).href, path.join(base, 'scripts/audit.mjs'), root, '--dotnet', '--json'], { encoding: 'utf8' });
    assert.equal(r.status, 0, r.stderr);
    const out = JSON.parse(r.stdout);
    assert.equal(out.collectionComplete, true);
    assert.equal(out.warnings.some(w => /10\.0.*未取得|未取得 10\.0/.test(w)), false, out.warnings.join('\n'));
    assert.equal(out.dotnet.globalJson[0].guaranteedLatest, true);
  } finally { fs.rmSync(root, { recursive: true }); }
});
test('policy deviation accepts a .NET framework finding, not only CI findings', () => {
  const root = temp(); try {
    write(root, 'App/App.csproj', '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net10.0</TargetFramework></PropertyGroup></Project>');
    write(root, '.desktop-policy.json', { deviations: [{ rule: 'dotnet-no-global-json', reason: 'SDK arrives with the base image', revisitWhen: '2027-01-01' }] });
    const r = run('audit.mjs', [root, '--dotnet', '--offline', '--json']); assert.equal(r.status, 2);
    const out = JSON.parse(r.stdout);
    const f = out.frameworkFindings.find(x => x.id === 'dotnet-no-global-json');
    assert.deepEqual(f.accepted, { reason: 'SDK arrives with the base image', revisitWhen: '2027-01-01' });
    assert.equal(out.summary.frameworkAccepted, 1); assert.equal(out.summary.frameworkFindings, 0);
    assert.match(run('audit.mjs', [root, '--dotnet', '--offline']).stdout, /已接受的偏离[\s\S]*dotnet-no-global-json/);
  } finally { fs.rmSync(root, { recursive: true }); }
});
test('--dotnet without .NET projects is incomplete, not a clean pass', () => {
  const root = temp(); try {
    write(root, 'README.md', 'not a dotnet repo');
    const r = run('audit.mjs', [root, '--dotnet', '--offline', '--json']);
    assert.equal(r.status, 2);
    const out = JSON.parse(r.stdout);
    assert.equal(out.dotnet.detected, false);
    assert.ok(out.warnings.some(w => /未发现 \.NET 项目/.test(w)));
  } finally { fs.rmSync(root, { recursive: true }); }
});
test('workspace app resolves hoisted npm dependency', () => {
  const root = temp(); try {
    write(root, 'apps/desktop/package.json', { devDependencies: { electron: '~2.0.0' } });
    write(root, 'package-lock.json', { lockfileVersion: 3, packages: { 'node_modules/electron': { version: '2.0.7' } } });
    const out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.equal(out.inventory[0].manifest, 'apps/desktop/package.json'); assert.equal(out.inventory[0].resolved, '2.0.7');
  } finally { fs.rmSync(root, { recursive: true }); }
});
test('a skipped directory/symlink makes the run incomplete and appears in the text report', () => {
  const root = temp();
  try {
    write(root, 'package.json', {});
    fs.mkdirSync(path.join(root, 'real'), { recursive: true });
    fs.writeFileSync(path.join(root, 'real', 'x.txt'), 'x');
    fs.symlinkSync(path.join(root, 'real'), path.join(root, 'linked'), 'junction');
    const r = run('audit.mjs', [root, '--offline', '--ci-only', '--json']);
    assert.equal(r.status, 2, r.stderr);
    const out = JSON.parse(r.stdout);
    assert.equal(out.collectionComplete, false);
    assert.ok(out.warnings.some(w => /跳过了/.test(w)), out.warnings.join('\n'));
    const text = run('audit.mjs', [root, '--offline', '--ci-only']);
    assert.match(text.stdout, /skipped: linked/);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('Cargo workspace lock avoids a false unresolved sibling declaration', () => {
  const root = temp(); try {
    write(root, 'Cargo.lock', 'version = 3\n[[package]]\nname = "tauri"\nversion = "2.0.7"\nsource = "registry+https://github.com/rust-lang/crates.io-index"\n');
    write(root, 'apps/desktop/Cargo.toml', '[dependencies]\ntauri = { workspace = true }\n');
    const out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.equal(out.inventory.filter(x => x.name === 'tauri').length, 1); assert.equal(out.inventory[0].resolved, '2.0.7');
  } finally { fs.rmSync(root, { recursive: true }); }
});
test('report refuses overwriting existing file', () => {
  const root = temp(); try {
    write(root, 'package.json', {}); write(root, 'keep.json', 'KEEP');
    const r = run('audit.mjs', [root, '--offline', '--out', path.join(root, 'keep.json')]);
    assert.notEqual(r.status, 0); assert.equal(fs.readFileSync(path.join(root, 'keep.json'), 'utf8'), 'KEEP');
  } finally { fs.rmSync(root, { recursive: true }); }
});
test('review baseline rejects offline/incomplete report and missing confirmation', () => {
  const root = temp(); try {
    write(root, 'audit.json', { schemaVersion: 2, collectionComplete: false, mode: 'offline', changes: [] });
    const out = path.join(root, 'review.json');
    assert.notEqual(run('review-baseline.mjs', [path.join(root, 'audit.json'), out, '--confirm-reviewed']).status, 0);
    assert.notEqual(run('review-baseline.mjs', [path.join(root, 'audit.json'), out]).status, 0);
    assert.equal(fs.existsSync(out), false);
  } finally { fs.rmSync(root, { recursive: true }); }
});
test('baseline records reviewed IDs, not fixed versions, and cannot overwrite', () => {
  const root = temp(); try {
    const input = path.join(root, 'audit.json'), output = path.join(root, 'review.json');
    write(root, 'audit.json', { schemaVersion: 3, collectionComplete: true, mode: 'online', project: root, checkedAt: 'fixture', errors: [], changes: [{ framework: 'electron', tag: 'v2.1.0' }] });
    assert.equal(run('review-baseline.mjs', [input, output, '--confirm-reviewed']).status, 0);
    const b = JSON.parse(fs.readFileSync(output)); assert.deepEqual(b.reviewedChangeIds, ['electron:v2.1.0']); assert.equal(b.fixed, undefined);
    assert.notEqual(run('review-baseline.mjs', [input, output, '--confirm-reviewed']).status, 0);
  } finally { fs.rmSync(root, { recursive: true }); }
});
test('checksum output is deterministic LF SHA256 of final file', () => {
  const root = temp(); try {
    write(root, 'b.bin', 'abc'); write(root, 'a.bin', '');
    const r = run('checksums.mjs', [path.join(root, 'b.bin'), path.join(root, 'a.bin')]); assert.equal(r.status, 0, r.stderr);
    assert.ok(r.stdout.startsWith('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  a.bin\n'));
    assert.ok(r.stdout.includes('ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad  b.bin\n'));
    assert.equal(r.stdout.includes('\r'), false);
  } finally { fs.rmSync(root, { recursive: true }); }
});
test('Node toolchain pins are checked against the official schedule (EOL, maintenance, local file advisory)', () => {
  const root = temp(); try {
    write(root, 'package.json', { engines: { node: '>=20' } });
    const schedule = {
      v20: { start: '2019-01-01', lts: '2019-01-01', maintenance: '2020-01-01', end: '2020-12-31' },
      v24: { start: '2019-01-01', lts: '2019-01-01', maintenance: '2020-01-01', end: '2099-12-31' },
      v26: { start: '2019-01-01', lts: '2020-01-01', maintenance: '2099-01-01', end: '2099-12-31' },
    };
    const workflow = v => `on: [push]\njobs:\n  t:\n    runs-on: ubuntu-latest\n    env: { node-version: ${v} }\n`;
    write(root, '.github/workflows/ci.yml', workflow(20));
    write(root, 'mock.mjs', `globalThis.fetch = async (u) => {
      if (u.includes('nodejs/Release/main/schedule.json')) return { ok: true, status: 200, json: async () => (${JSON.stringify(schedule)}) };
      throw Error('Unexpected test URL ' + u);
    };`);
    const exec = () => spawnSync(process.execPath, ['--import', pathToFileURL(path.join(root, 'mock.mjs')).href, path.join(base, 'scripts/audit.mjs'), root, '--ci-only', '--json'], { encoding: 'utf8' });
    let r = exec(); assert.equal(r.status, 0, r.stderr); let out = JSON.parse(r.stdout);
    assert.equal(out.nodeSupport.latestLts, 26);
    assert.equal(out.ciFindings.find(f => f.id === 'node-version-eol').severity, 'P1');
    write(root, '.github/workflows/ci.yml', 'on: [push]\njobs:\n  t:\n    runs-on: ubuntu-latest\n    env:\n      node-version: 20\n');
    r = exec(); out = JSON.parse(r.stdout);
    assert.equal(out.ciFindings.find(f => f.id === 'node-version-eol').severity, 'P1');
    write(root, '.github/workflows/ci.yml', workflow(24));
    r = exec(); out = JSON.parse(r.stdout);
    assert.equal(out.ciFindings.find(f => f.id === 'node-version-maintenance').severity, 'P2');
    write(root, '.github/workflows/ci.yml', workflow(26));
    write(root, '.nvmrc', '24\n');
    r = exec(); out = JSON.parse(r.stdout);
    assert.equal(out.ciFindings.some(f => f.id.startsWith('node-version-')), false);
    assert.equal(out.ciFindings.some(f => f.id === 'node-version-source-mismatch'), false);
    assert.equal(out.summary.ci.P2, 0);
    assert.ok(out.nodePins.some(p => p.kind === 'file' && p.major === 24));
    assert.ok(out.warnings.some(w => /\.nvmrc.*maintenance/.test(w)), out.warnings.join('\n'));
    write(root, '.nvmrc', '26\n');
    write(root, '.github/workflows/ci.yml', 'on: [push]\njobs:\n  t:\n    runs-on: ubuntu-latest\n    env:\n      node-version-file: .nvmrc\n');
    r = exec(); out = JSON.parse(r.stdout);
    assert.equal(out.ciFindings.some(f => f.id.startsWith('node-version-')), false);
    assert.ok(out.nodePins.some(p => p.kind === 'workflow-file' && p.major === 26));
    assert.equal(out.warnings.some(w => /\.nvmrc.*maintenance/.test(w)), false);
    r = run('audit.mjs', [root, '--offline', '--ci-only', '--json']); out = JSON.parse(r.stdout);
    assert.equal(r.status, 2); assert.equal(out.nodeSupport, null);
    assert.ok(out.warnings.some(w => /离线模式未核验/.test(w)));
  } finally { fs.rmSync(root, { recursive: true }); }
});
test('online end-to-end with synthetic registry/release responses; since-baseline keeps inventory and CI', () => {
  const root = temp(); try {
    write(root, 'package.json', { devDependencies: { electron: '^45.0.0' } });
    write(root, 'package-lock.json', { packages: { 'node_modules/electron': { version: '45.0.0' } } });
    write(root, 'main.js', 'app.makeWindow()');
    write(root, '.github/workflows/release.yml', 'jobs:\n  build:\n    steps:\n      - uses: actions/checkout@v1\n      - uses: softprops/action-gh-release@v1\n      - uses: dtolnay/rust-toolchain@stable\n');
    const mock = path.join(root, 'mock.mjs');
    write(root, 'mock.mjs', `globalThis.fetch = async (u) => {
      let data;
      if (u.includes('registry.npmjs.org')) data = { 'dist-tags': { latest: '46.0.0' }, versions: { '45.0.0': {}, '45.1.0': {}, '46.0.0': {} } };
      else if (u.includes('releases.electronjs.org')) data = [{ version:'45.0.0' }, { version:'45.1.0' }, { version:'46.0.0' }];
      else if (u.includes('/releases/latest')) data = { tag_name: 'v4.0.0' };
      else if (u.includes('/releases?')) data = [{ tag_name:'v45.1.0', prerelease:false, draft:false, body:'## Features\\n- New \\x60app.makeWindow\\x60 feature', html_url:'https://github.com/electron/electron/releases/tag/v45.1.0' }];
      else if (u.includes('/tags?')) data = [{ name:'v4.0.0', commit:{sha:'b'.repeat(40)} }, { name:'v1', commit:{sha:'a'.repeat(40)} }];
      else throw Error('Unexpected test URL');
      return {ok:true, status:200, json:async()=>data};
    };`);
    const audit = path.join(root, 'snapshot.json');
    let r = spawnSync(process.execPath, ['--import', pathToFileURL(mock).href, path.join(base, 'scripts/audit.mjs'), root, '--json', '--out', audit], { encoding: 'utf8' });
    assert.equal(r.status, 0, r.stderr); let data = JSON.parse(r.stdout);
    assert.equal(data.changes.length, 1); assert.equal(data.changes[0].hits[0].file, 'main.js');
    assert.equal(data.changes[0].suggestedPriority, 'P1-candidate'); assert.equal(data.schemaVersion, 3);
    const behind = data.ciFindings.find(f => f.id === 'action-major-behind'); assert.ok(behind);
    assert.equal(data.actions[0].suggestedPin, 'actions/checkout@v4');
    const rt = data.actions.find(x => x.repository === 'dtolnay/rust-toolchain'); assert.equal(rt.toolchainRef, true); assert.equal(rt.suggestedPin, 'dtolnay/rust-toolchain@stable');
    assert.equal(data.ciFindings.filter(f => f.id === 'action-major-behind').length, 2);
    // house style 钉大版本标签，所以只读 Action 的可移动 ref 不是发现；
    // 能写产物的那几个才是另一类风险。
    const moving = data.ciFindings.filter(f => f.id === 'action-moving-ref');
    assert.equal(moving.length, 1);
    // 符合 house style：notice，不计入 P2
    assert.equal(moving[0].severity, 'notice'); assert.equal(data.summary.ci.notice, 1);
    assert.ok(String(moving[0].detail).includes('softprops/action-gh-release'));
    // 只读 Action 的大版本标签不该触发“SHA 未在 tag 中找到”的警告（0.5.0 的回归）
    assert.equal(data.warnings.some(w => /SHA/.test(w)), false, data.warnings.join('\n'));
    const review = path.join(root, 'review.json'); assert.equal(run('review-baseline.mjs', [audit, review, '--confirm-reviewed']).status, 0);
    r = spawnSync(process.execPath, ['--import', pathToFileURL(mock).href, path.join(base, 'scripts/audit.mjs'), root, '--json', '--since-baseline', review], { encoding: 'utf8' });
    assert.equal(r.status, 0, r.stderr); data = JSON.parse(r.stdout);
    assert.equal(data.changes[0].reviewed, true); assert.ok(data.inventory.length); assert.ok(data.ciFindings.length);
    assert.ok(data.changes[0].hits.every(hit => hit.file !== 'snapshot.json'));
  } finally { fs.rmSync(root, { recursive: true }); }
});

test('macOS updater needs a zip target: dmg-only is P1, a zip target clears it, CLI args win over the config', () => {
  const root = temp();
  try {
    write(root, 'package.json', { dependencies: { 'electron-updater': '^6.0.0' }, devDependencies: { electron: '^44.0.0' } });
    write(root, 'package-lock.json', { lockfileVersion: 3, packages: { 'node_modules/electron': { version: '44.9.0' }, 'node_modules/electron-updater': { version: '6.8.9' } } });
    const builder = (targets) => ['appId: com.x', 'mac:', '  target:', ...targets.map(t => '    - ' + t), 'linux:', '  target:', '    - AppImage', ''].join('\n');
    // dmg only: the manifest points at a .dmg and the Mac updater throws
    // ERR_UPDATER_ZIP_FILE_NOT_FOUND — silent, because the build is green.
    write(root, 'electron-builder.yml', builder(['dmg']));
    let out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    let finding = out.ciFindings.find(f => f.id === 'mac-update-needs-zip');
    assert.ok(finding, 'dmg-only mac target must be reported');
    assert.equal(finding.severity, 'P1');
    assert.equal(finding.file, 'electron-builder.yml');
    // a zip target clears it
    write(root, 'electron-builder.yml', builder(['dmg', 'zip']));
    out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.equal(out.ciFindings.find(f => f.id === 'mac-update-needs-zip'), undefined);
    // CLI args override the config, so --mac dmg wins over mac.target: [dmg, zip]
    write(root, '.github/workflows/release.yml', 'name: release\non:\n  push:\n    tags: ["v*"]\njobs:\n  build:\n    steps:\n      - run: npx electron-builder --mac dmg --x64\n');
    out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    finding = out.ciFindings.find(f => f.id === 'mac-update-needs-zip');
    assert.ok(finding, 'CLI --mac dmg without zip must be reported');
    assert.equal(finding.file, '.github/workflows/release.yml');
    // A comment mentioning a zip command is not a command: it must not mask the
    // dmg-only build (comments are stripped, same rule as the CI traps).
    write(root, '.github/workflows/release.yml', 'name: release\non:\n  push:\n    tags: ["v*"]\njobs:\n  build:\n    steps:\n      # later: npx electron-builder --mac dmg zip\n      - run: npx electron-builder --mac dmg --x64\n');
    out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.ok(out.ciFindings.find(f => f.id === 'mac-update-needs-zip'), 'a comment must not suppress the dmg-only finding');
    // An inline comment in the builder config behaves the same way.
    write(root, '.github/workflows/release.yml', 'name: noop\non: [push]\njobs:\n  b:\n    steps:\n      - run: echo ok\n');
    write(root, 'electron-builder.yml', 'appId: com.x\nmac:\n  target: [dmg] # zip later\n');
    out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.ok(out.ciFindings.find(f => f.id === 'mac-update-needs-zip'), 'an inline builder comment must not suppress the finding');
  } finally { fs.rmSync(root, { recursive: true }); }
});

test('the packaged app manifest copy is not an inventory source', () => {
  const root = temp();
  try {
    write(root, 'package.json', { dependencies: { 'electron-updater': '^6.8.9' } });
    write(root, 'package-lock.json', { lockfileVersion: 3, packages: { 'node_modules/electron-updater': { version: '6.8.9' } } });
    // electron-builder copies the manifest into the packaged output; it is a
    // build artifact, not a source manifest.
    write(root, 'release/win-unpacked/resources/app/package.json', { dependencies: { 'electron-updater': '^6.8.9' } });
    const out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    const rows = out.inventory.filter(i => i.name === 'electron-updater');
    assert.equal(rows.length, 1, JSON.stringify(rows));
    assert.equal(rows[0].manifest, 'package.json');
  } finally { fs.rmSync(root, { recursive: true }); }
});

test('CSC_LINK taken straight from a secret is reported: a missing secret renders as an empty string', () => {  const root = temp();
  try {
    write(root, 'package.json', { devDependencies: { electron: '^44.0.0' } });
    write(root, 'package-lock.json', { lockfileVersion: 3, packages: { 'node_modules/electron': { version: '44.9.0' } } });
    const wf = (env) => ['name: release', 'on:', '  push:', '    tags: ["v*"]', 'jobs:', '  build:', '    steps:', '      - run: npx electron-builder --mac dmg', '        env:', ...env].join('\n') + '\n';
    // A missing secret renders as an empty string, and electron-builder reads an
    // empty CSC_LINK as "the certificate is this path" → it signs the working
    // directory and the macOS leg dies with "<repo> not a file".
    write(root, '.github/workflows/release.yml', wf(['          CSC_LINK: ${{ runner.os == \'macOS\' && secrets.MAC_CSC_LINK || \'\' }}']));
    let out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    let finding = out.ciFindings.find(f => f.id === 'electron-builder-empty-csc-link');
    assert.ok(finding, 'an empty-able CSC_LINK must be reported');
    assert.equal(finding.severity, 'P1');
    assert.equal(finding.file, '.github/workflows/release.yml');
    // A literal path is a deliberate choice, not the bug.
    write(root, '.github/workflows/release.yml', wf(['          CSC_LINK: ./cert.p12']));
    out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.equal(out.ciFindings.find(f => f.id === 'electron-builder-empty-csc-link'), undefined);
    // The guarded form (secret under another name, exported only when present) is fine.
    write(root, '.github/workflows/release.yml', wf(['          MAC_CSC_LINK: ${{ secrets.MAC_CSC_LINK }}']));
    out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.equal(out.ciFindings.find(f => f.id === 'electron-builder-empty-csc-link'), undefined);
  } finally { fs.rmSync(root, { recursive: true }); }
});

test('a bash script on a Windows runner without shell: bash is reported', () => {
  const root = temp();
  try {
    write(root, 'package.json', { devDependencies: { electron: '^44.0.0' } });
    write(root, 'package-lock.json', { lockfileVersion: 3, packages: { 'node_modules/electron': { version: '44.9.0' } } });
    const wf = (extra) => ['name: release', 'on:', '  push:', '    tags: ["v*"]', 'jobs:', '  build:', '    runs-on: windows-latest', '    steps:', '      - run: |', '          set -euo pipefail', '          if [ -n "$X" ]; then', '            export Y=1', '          fi', ...extra].join('\n') + '\n';
    // Windows' default shell is PowerShell: a bash script there is a ParserError
    // while macOS/Linux pass — looks like a platform problem, is a shell problem.
    write(root, '.github/workflows/release.yml', wf([]));
    let out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    let finding = out.ciFindings.find(f => f.id === 'bash-script-on-windows-runner');
    assert.ok(finding, 'a bash script on a Windows runner must be reported');
    assert.equal(finding.severity, 'P1');
    // Declaring the shell fixes it.
    write(root, '.github/workflows/release.yml', wf(['        shell: bash']));
    out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.equal(out.ciFindings.find(f => f.id === 'bash-script-on-windows-runner'), undefined);
    // No Windows runner → nothing to report.
    write(root, '.github/workflows/release.yml', wf([]).replace('windows-latest', 'ubuntu-latest'));
    out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.equal(out.ciFindings.find(f => f.id === 'bash-script-on-windows-runner'), undefined);
    // A Windows job next to a Linux-only job that holds the bash script: the
    // script never runs on Windows, so this must NOT be reported.
    write(root, '.github/workflows/release.yml', [
      'name: mixed', 'on:', '  push:', '    tags: ["v*"]', 'jobs:',
      '  build:', '    runs-on: windows-latest', '    steps:', '      - run: npm ci',
      '  publish:', '    runs-on: ubuntu-latest', '    steps:', '      - run: |',
      '          set -euo pipefail', '          echo hi > notes.md', '',
    ].join('\n'));
    out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.equal(out.ciFindings.find(f => f.id === 'bash-script-on-windows-runner'), undefined, 'bash only in a Linux job must not be reported');
  } finally { fs.rmSync(root, { recursive: true }); }
});

test('tauri.conf.json5 drives the updater P0; an unreadable config is not a clean run', () => {
  const root = temp();
  try {
    write(root, 'package.json', { devDependencies: { '@tauri-apps/cli': '^2.0.0' }, dependencies: { '@tauri-apps/plugin-updater': '^2.0.0' } });
    write(root, 'package-lock.json', { lockfileVersion: 3, packages: {
      'node_modules/@tauri-apps/cli': { version: '2.1.0' },
      'node_modules/@tauri-apps/plugin-updater': { version: '2.1.0' } } });
    write(root, '.github/workflows/release.yml', 'on:\n  push:\n    tags: [v*]\npermissions:\n  contents: write\njobs:\n  b:\n    steps:\n      - uses: tauri-apps/tauri-action@v1\n');
    write(root, 'src-tauri/tauri.conf.json5', '{\n  // no updater artifacts\n  bundle: { createUpdaterArtifacts: false, targets: ["nsis"], },\n}\n');
    let out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.equal(out.tauriConfig.file, 'src-tauri/tauri.conf.json5');
    assert.equal(out.tauriConfig.createUpdaterArtifacts, false);
    assert.ok(out.ciFindings.some(f => f.id === 'tauri-updater-manifest'), 'JSON5 config must reach the updater P0 check');
    assert.equal(out.warnings.some(w => /配置读不出来/.test(w)), false);
    // A config the parser cannot read must not look like "no P0 found".
    write(root, 'src-tauri/tauri.conf.json5', '{ bundle: ');
    out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.equal(out.tauriConfig, undefined);
    assert.ok(out.warnings.some(w => /配置读不出来/.test(w)));
    // A UTF-8 BOM (Windows editors) is not valid JSON, but the file is fine: the
    // config must still be read and the P0 must still fire.
    write(root, 'src-tauri/tauri.conf.json5', '\uFEFF{\n  bundle: { createUpdaterArtifacts: false, targets: ["nsis"], },\n}\n');
    write(root, 'package.json', '\uFEFF' + JSON.stringify({ devDependencies: { '@tauri-apps/cli': '^2.0.0' }, dependencies: { '@tauri-apps/plugin-updater': '^2.0.0' } }));
    out = JSON.parse(run('audit.mjs', [root, '--offline', '--json']).stdout);
    assert.equal(out.tauriConfig.createUpdaterArtifacts, false);
    assert.ok(out.ciFindings.some(f => f.id === 'tauri-updater-manifest'), 'a BOM must not disable the updater P0 check');
    assert.equal(out.errors.some(e => /JSON 解析失败/.test(e.message)), false);
    assert.equal(out.warnings.some(w => /配置读不出来/.test(w)), false);
    // No config file at all is the same fail-open: with the updater in use, the
    // run must say the artifact setting was never verified.
    fs.rmSync(path.join(root, 'src-tauri/tauri.conf.json5'));
    const noConf = run('audit.mjs', [root, '--ci-only', '--json']);
    assert.equal(noConf.status, 2, noConf.stderr);
    const noConfOut = JSON.parse(noConf.stdout);
    assert.ok(noConfOut.warnings.some(w => /tauri\.conf/.test(w)), noConfOut.warnings.join('\n'));
  } finally { fs.rmSync(root, { recursive: true }); }
});

test('an unreadable tauri.conf.json5 makes an online run incomplete, not just warned about', () => {
  const root = temp(); try {
    write(root, 'package.json', { name: 'fx', version: '1.0.0' });
    write(root, 'src-tauri/tauri.conf.json5', '{ bundle: ');
    // Online mode: the report starts complete, so the config branch is the only
    // thing that can make it incomplete — that is the behaviour under test.
    const r = run('audit.mjs', [root, '--json']);
    assert.equal(r.status, 2, r.stderr);
    const out = JSON.parse(r.stdout);
    assert.equal(out.collectionComplete, false);
    assert.ok(out.warnings.some(w => /配置读不出来/.test(w)));
  } finally { fs.rmSync(root, { recursive: true }); }
});

test('CLI usage errors print one line, not a stack', () => {
  const root = temp();
  try {
    for (const args of [[root, '--pages', '99'], [root, '--bogus'], [path.join(root, 'missing')]]) {
      const r = run('audit.mjs', args);
      assert.notEqual(r.status, 0);
      assert.match(r.stderr, /^desktop-app-standard: /m);
      assert.doesNotMatch(r.stderr, /\n\s+at /);
    }
  } finally { fs.rmSync(root, { recursive: true }); }
});

test('skill major selects the newest published stable target even after upstream moves to the next major', () => {
  const root = temp();
  try {
    write(root, 'package.json', { devDependencies: { 'electron-builder': '26.18.0' }, dependencies: { 'electron-updater': '6.8.9' } });
    write(root, 'package-lock.json', { packages: {
      'node_modules/electron-builder': { version: '26.18.0' },
      'node_modules/electron-updater': { version: '6.8.9' },
    } });
    const mock = path.join(root, 'registry.mjs');
    write(root, 'registry.mjs', `globalThis.fetch = async url => {
      const data = {
        'https://registry.npmjs.org/electron-builder': { 'dist-tags': { latest: '27.0.0' }, versions: { '26.18.0': {}, '26.18.1': {}, '26.18.2': { deprecated: 'withdrawn' }, '27.0.0': {} } },
        'https://registry.npmjs.org/electron-updater': { 'dist-tags': { latest: '7.0.0', next: '6.8.20' }, versions: { '6.8.9': {}, '6.8.10': {}, '6.8.20': {}, '6.8.12-beta.1': {}, '7.0.0': {} } },
      }[url];
      if (data) return { ok: true, json: async () => data };
      if (url.startsWith('https://api.github.com/repos/electron-userland/electron-builder/releases?')) return { ok: true, json: async () => [] };
      throw new Error('unexpected request ' + url);
    };`);
    const r = spawnSync(process.execPath, ['--import', pathToFileURL(mock).href,
      path.join(base, 'scripts/audit.mjs'), root, '--json'], { encoding: 'utf8' });
    const out = JSON.parse(r.stdout);
    assert.equal(r.status, 0, JSON.stringify(out.errors));
    const versions = out.upstream.map(p => [p.name, p.latestStable, p.targetMajor, p.targetStable]).sort();
    assert.deepEqual(versions, [['electron-builder', '27.0.0', 26, '26.18.1'], ['electron-updater', '7.0.0', 6, '6.8.10']]);
  } finally { fs.rmSync(root, { recursive: true }); }
});

test('Tauri major selection excludes yanked crates and reports an unavailable target without substituting a newer major', () => {
  const root = temp();
  try {
    write(root, 'Cargo.lock', 'version = 3\n[[package]]\nname = "tauri-build"\nversion = "1.0.0"\nsource = "registry+https://github.com/rust-lang/crates.io-index"\n');
    write(root, 'package.json', { devDependencies: { '@tauri-apps/cli': '1.0.0' } });
    write(root, 'package-lock.json', { packages: { 'node_modules/@tauri-apps/cli': { version: '1.0.0' } } });
    const mock = path.join(root, 'registry.mjs');
    write(root, 'registry.mjs', `globalThis.fetch = async url => {
      const data = {
        'https://registry.npmjs.org/%40tauri-apps%2Fcli': { 'dist-tags': { latest: '3.0.0' }, versions: { '3.0.0': {}, '2.1.0-rc.1': {} } },
        'https://crates.io/api/v1/crates/tauri-build': { versions: [{num:'3.0.0'}, {num:'2.10.0',yanked:true}, {num:'2.9.2'}] },
      }[url];
      if (!data) throw new Error('unexpected request ' + url);
      return { ok: true, json: async () => data };
    };`);
    const r = spawnSync(process.execPath, ['--import', pathToFileURL(mock).href,
      path.join(base, 'scripts/audit.mjs'), root, '--json'], { encoding: 'utf8' });
    const out = JSON.parse(r.stdout);
    assert.equal(r.status, 2);
    assert.deepEqual(out.errors, []);
    assert.equal(out.upstream.find(p => p.name === 'tauri-build').targetStable, '2.9.2');
    assert.equal(out.upstream.find(p => p.name === '@tauri-apps/cli').targetStable, null);
    assert.ok(out.warnings.some(message => message.includes('@tauri-apps/cli') && message.includes('2.x')));
  } finally { fs.rmSync(root, { recursive: true }); }
});

test('specialized modes keep CI context without collecting unrelated framework releases', () => {
  const root = temp();
  try {
    write(root, 'ui/package.json', {
      dependencies: { electron: '^1.0.0', 'electron-updater': '^1.0.0' },
      build: { mac: { target: [{ target: 'dmg' }] } },
    });
    write(root, 'App.csproj', '<Project><PropertyGroup><TargetFramework>net10.0</TargetFramework></PropertyGroup></Project>');
    const mock = path.join(root, 'metadata.mjs');
    write(root, 'metadata.mjs', [
      'globalThis.fetch = async url => {',
      "  if (!url.endsWith('/10.0/releases.json')) throw new Error('unexpected request ' + url);",
      "  return { ok: true, json: async () => ({ 'latest-sdk': '10.0.100', 'support-phase': 'active', 'eol-date': '2099-01-01' }) };",
      '};',
    ].join('\n'));
    for (const mode of ['--ci-only', '--dotnet']) {
      const r = spawnSync(process.execPath, ['--import', pathToFileURL(mock).href,
        path.join(base, 'scripts/audit.mjs'), root, mode, '--json'], { encoding: 'utf8' });
      const out = JSON.parse(r.stdout);
      assert.equal(r.status, 0, JSON.stringify(out.errors));
      assert.deepEqual(out.upstream, []);
      assert.ok(out.ciFindings.some(f => f.file === 'ui/package.json' && f.id === 'mac-update-needs-zip'));
      if (mode === '--dotnet') assert.equal(out.dotnet.channels[0].latestSdk, '10.0.100');
    }
  } finally { fs.rmSync(root, { recursive: true }); }
});

test('explicit MSBuild expressions keep their uncertainty over inherited defaults', () => {
  const root = temp();
  try {
    write(root, 'Directory.Build.props', '<Project><PropertyGroup><TargetFramework>net10.0</TargetFramework></PropertyGroup></Project>');
    write(root, 'App.csproj', '<Project><PropertyGroup><TargetFramework>$(AppTfm)</TargetFramework></PropertyGroup></Project>');
    const r = run('audit.mjs', [root, '--dotnet', '--json']);
    const out = JSON.parse(r.stdout);
    assert.equal(r.status, 2);
    assert.deepEqual(out.dotnet.projects[0].unresolved, ['$(AppTfm)']);
    assert.deepEqual(out.dotnet.channels, []);
  } finally { fs.rmSync(root, { recursive: true }); }
});

test('a failed checksum run emits no partial manifest', () => {
  const root = temp();
  try {
    write(root, 'a.zip', 'valid first asset');
    const r = run('checksums.mjs', [path.join(root, 'a.zip'), path.join(root, 'z.zip')]);
    assert.notEqual(r.status, 0);
    assert.equal(r.stdout, '');
    write(root, 'SHA256SUMS', 'old checksum');
    const self = run('checksums.mjs', [path.join(root, 'a.zip'), path.join(root, 'SHA256SUMS')]);
    assert.notEqual(self.status, 0);
    assert.equal(self.stdout, '');
    assert.match(self.stderr, /不能包含自身/);
  } finally { fs.rmSync(root, { recursive: true }); }
});

test('PR-only repositories report the absent release path without claiming offline verification', () => {
  const root = temp();
  try {
    write(root, 'package.json', {name: 'coverage', version: '1.0.0', devDependencies: {electron: '45.0.0'}});
    write(root, '.github/workflows/ci.yml', 'on: [pull_request]\njobs:\n  test:\n    steps:\n      - run: npm test\n');
    const result = run('audit.mjs', [root, '--ci-only', '--offline', '--json']);
    const report = JSON.parse(result.stdout);
    assert.equal(result.status, 2);
    assert.deepEqual(report.workflowCoverage.pullRequest, ['.github/workflows/ci.yml']);
    assert.ok(report.ciFindings.some(f => f.id === 'workflow-release-missing'));
    assert.ok(!report.ciFindings.some(f => f.id === 'workflow-pull-request-missing'));
  } finally { fs.rmSync(root, {recursive: true, force: true}); }
});
