import test from 'node:test';
import assert from 'node:assert/strict';
import { discoverApplications, workflowApplications } from '../scripts/app-context.mjs';

import { exact, compare, stableMax, minor, cargoPackages, workflowHints, usageHints, requestJson, releaseHistory, parseJson5,
  parseYarnLock, parsePnpmLock, parseBunLock, resolveFromLock, electronSupportedMajors, nodeSupportFacts, classifyNotes, changelogSections, refVersion } from '../scripts/core.mjs';
import { stripComments, runTraps, defaultContext, TRAPS, workflowCoverage } from '../scripts/ci-traps.mjs';

test('a shared Rust workspace does not turn a sibling Electron app into Tauri', () => {
  const apps = discoverApplications([{file: 'z/src-tauri/tauri.conf.json'}], [
    {name: 'electron', ecosystem: 'npm', manifest: 'a/package.json'},
    {name: 'tauri', ecosystem: 'cargo', manifest: 'Cargo.lock'},
  ], ['package.json', 'a/package.json']);
  assert.deepEqual(apps.map(app => [app.directory, app.isTauri, app.hasElectron]), [['a', false, true], ['z', true, false]]);
});

test('workflow paths prefer the closest app and run defaults do not affect actions', () => {
  const applications = [{directory: '.', isTauri: true}, {directory: 'a', isTauri: true}];
  const workflow = ['on: push', 'defaults:', '  run:', '    working-directory: a', 'jobs:', '  build:', '    steps:',
    '      - uses: tauri-apps/tauri-action@v1', '      - uses: tauri-apps/tauri-action@v1', '        with:',
    '          projectPath: a', '      - run: cargo tauri build', ''].join('\n');
  const scopes = workflowApplications('release.yml', workflow, applications);
  assert.deepEqual(scopes.map(scope => scope.application), ['.', 'a', 'a']);
  const reused = workflowApplications('release.yml', 'jobs:\n  build:\n    uses: ./.github/workflows/shared.yml\n', applications);
  assert.equal(reused[0].application, null);
  assert.match(reused[0].reason, /reusable workflow/);
});
test('stable version comparison is numeric and rejects ranges/prereleases', () => {
  assert.equal(compare('2.10.0', '2.9.9'), 1);
  assert.equal(compare('2.1.0', '2.1.0'), 0);
  assert.equal(compare('^2.1.0', '2.1.0'), null);
  for (const v of ['^1.0.0', '1.0.0-beta.1', 'v1.0.0', 'workspace:*', '02.1.0', '999999999999999999.0.0']) assert.equal(exact(v), null);
  assert.equal(stableMax(['2.9.0', '2.10.0', '3.0.0-beta.1']), '2.10.0');
  assert.equal(minor('2.10.1'), '2.10');
});
test('Cargo.lock preserves duplicates and source', () => {
  const data = cargoPackages('version = 3\n[[package]]\nname = "tauri"\nversion = "2.1.0"\nsource = "registry+https://github.com/rust-lang/crates.io-index"\n[[package]]\nname = "tauri"\nversion = "2.2.0"\n');
  assert.equal(data.length, 2); assert.equal(data[1].source, 'workspace/path');
});
test('workflow hints ignore full comments, preserve subpath and SHA', () => {
  const data = workflowHints('.github/workflows/r.yml', '# - uses: bad/bad@main\n- uses: owner/repo/sub@v2 # test\n- uses: owner/repo@' + 'a'.repeat(40) + '\n  releaseDraft: true\n', true);
  assert.equal(data.actions.length, 2); assert.equal(data.actions[0].repository, 'owner/repo');
  assert.equal(data.actions[1].immutableReference, true);
  assert.equal(data.hints, undefined);
});
test('JSON5 config: comments, unquoted keys, single quotes, trailing commas; null when unreadable', () => {
  const parsed = parseJson5("{\n  // updater\n  productName: 'My App',\n  bundle: { createUpdaterArtifacts: 'v1Compatible', targets: ['nsis','msi',], },\n}");
  assert.deepEqual(parsed, { productName: 'My App', bundle: { createUpdaterArtifacts: 'v1Compatible', targets: ['nsis','msi'] } });
  assert.equal(parseJson5('{ bundle: '), null);
  assert.equal(parseJson5(''), null);
  assert.equal(parseJson5('{ endpoint: "https://x.example/a", note: "a // b" }').endpoint, 'https://x.example/a');
  // Windows editors write a UTF-8 BOM; it is not valid JSON5 but the file is fine.
  assert.deepEqual(parseJson5('\uFEFF{ productName: "App" }'), { productName: 'App' });
});
test('usage is an unverified hint, not a semantic verdict', () => {
  const hit = usageHints([{ file: 'main.js', text: 'abc\napp.makeWindow()' }], 'New `app.makeWindow()` API.');
  assert.equal(hit.hits[0].line, 2); assert.equal(hit.applicability, 'unverified');
  assert.equal(usageHints([], 'security fix').applicability, 'unverified');
});
test('GitHub credential is not sent to npm/crates/official Electron index', async () => {
  const seen = [];
  const fetchImpl = async (u, opts) => { seen.push({ u, opts }); return { ok: true, status: 200, json: async () => ({}) }; };
  for (const url of ['https://api.github.com/repos/a/b/tags', 'https://registry.npmjs.org/electron/latest', 'https://crates.io/api/v1/crates/tauri', 'https://releases.electronjs.org/releases.json', 'https://builds.dotnet.microsoft.com/dotnet/release-metadata/10.0/releases.json', 'https://raw.githubusercontent.com/nodejs/Release/main/schedule.json']) await requestJson(url, { token: 'test-secret', fetchImpl });
  assert.equal(seen[0].opts.headers.Authorization, 'Bearer test-secret');
  for (const x of seen.slice(1)) assert.equal(x.opts.headers.Authorization, undefined);
  assert.ok(seen.every(x => x.opts.redirect === 'error'));
});
test('untrusted destinations and rate-limit responses fail explicitly', async () => {
  await assert.rejects(requestJson('https://example.com/x'), /白名单/);
  await assert.rejects(requestJson('http://api.github.com/x'), /白名单/);
  await assert.rejects(requestJson('https://api.github.com/x', { fetchImpl: async () => ({ ok: false, status: 429 }) }), /未知/);
});
test('5xx retries once', async () => {
  let count = 0;
  const x = await requestJson('https://api.github.com/x', { fetchImpl: async () => (++count === 1 ? { ok: false, status: 503 } : { ok: true, status: 200, json: async () => ({ value: 1 }) }) });
  assert.equal(count, 2); assert.equal(x.value, 1);
});
const release = v => ({ tag_name: 'v' + v, body: '`app.test` changed', html_url: 'https://github.com/test/test/releases/v' + v, published_at: '2026-01-01T00:00:00Z', prerelease: false, draft: false });
test('release pagination does not stop at an older-major backport', async () => {
  const page1 = [release('1.9.0'), ...Array.from({ length: 99 }, () => ({ ...release('9.0.0-beta.1'), prerelease: true }))];
  const page2 = [release('3.0.0'), release('2.2.0')]; let calls = 0;
  const r = await releaseHistory('test/test', /^v(\d+\.\d+\.\d+)$/, '2.1.0', 3, async () => (++calls === 1 ? page1 : page2), ['2.2.0', '3.0.0']);
  assert.equal(calls, 2); assert.equal(r.truncated, false); assert.equal(r.missingVersions.length, 0);
});
test('missing expected release is incomplete even if API is exhausted', async () => {
  const r = await releaseHistory('test/test', /^v(\d+\.\d+\.\d+)$/, '2.1.0', 2, async () => [release('2.1.0')], ['2.2.0']);
  assert.equal(r.truncated, true); assert.equal(r.exhausted, true);
});
test('page cap is reported when no authoritative version index exists', async () => {
  const r = await releaseHistory('test/test', /^v(\d+\.\d+\.\d+)$/, '2.1.0', 1, async () => Array.from({ length: 100 }, () => release('2.1.0')));
  assert.equal(r.reachedFloor, true); assert.equal(r.truncated, true);
});

// ---------------- lockfiles ----------------
test('yarn classic lock: multi-spec headers resolve the declared range', () => {
  const lock = parseYarnLock('# yarn lockfile v1\n\n"electron@^2.0.0", electron@~2.0.1:\n  version "2.0.4"\n  resolved "https://x"\n\nelectron@^3.0.0:\n  version "3.0.1"\n');
  assert.equal(lock.flavor, 'classic');
  assert.equal(resolveFromLock('yarn', lock, { name: 'electron', declared: '^2.0.0' }).version, '2.0.4');
  const amb = resolveFromLock('yarn', lock, { name: 'electron', declared: '^9' });
  assert.equal(amb.version, null); assert.deepEqual(amb.candidates.sort(), ['2.0.4', '3.0.1']);
});
test('yarn berry lock: npm: protocol, scoped names, __metadata skipped', () => {
  const lock = parseYarnLock('__metadata:\n  version: 8\n\n"@tauri-apps/api@npm:^2.1.0":\n  version: 2.1.3\n  resolution: "@tauri-apps/api@npm:2.1.3"\n\n"app@workspace:.":\n  version: 0.0.0-use.local\n');
  assert.equal(lock.flavor, 'berry');
  const r = resolveFromLock('yarn', lock, { name: '@tauri-apps/api', declared: '^2.1.0' });
  assert.equal(r.version, '2.1.3');
  assert.equal(lock.entries.some(e => e.name === '__metadata'), false);
});
test('pnpm v9 importers are per workspace and strip peer suffixes', () => {
  const lock = parsePnpmLock("lockfileVersion: '9.0'\n\nimporters:\n\n  .:\n    devDependencies:\n      electron:\n        specifier: ^2.0.0\n        version: 2.0.9\n\n  apps/desktop:\n    dependencies:\n      '@tauri-apps/api':\n        specifier: ^2.1.0\n        version: 2.1.1(typescript@5.0.0)\n\npackages:\n\n  electron@2.0.9:\n    resolution: {integrity: x}\n");
  assert.equal(resolveFromLock('pnpm', lock, { name: 'electron', importerPath: '.' }).version, '2.0.9');
  assert.equal(resolveFromLock('pnpm', lock, { name: '@tauri-apps/api', importerPath: 'apps/desktop' }).version, '2.1.1');
  assert.equal(resolveFromLock('pnpm', lock, { name: 'electron', importerPath: 'apps/desktop' }).version, null);
});
test('bun.lock text format with trailing commas', () => {
  const lock = parseBunLock('{\n  "lockfileVersion": 1,\n  "workspaces": { "": { "name": "app" } },\n  "packages": {\n    "electron": ["electron@2.0.3", "", {}, "sha512-x"],\n  },\n}\n');
  assert.equal(resolveFromLock('bun', lock, { name: 'electron' }).version, '2.0.3');
});

// ---------------- upstream helpers ----------------
test('Electron supported majors = latest three stable majors, prereleases ignored', () => {
  assert.deepEqual(electronSupportedMajors(['3.0.0', '4.1.0', '5.0.0', '6.0.0-beta.1', '2.9.9', '5.0.1']), [5, 4, 3]);
});
test('Node phases follow the official schedule, including the maintenance window before the next LTS', () => {
  const schedule = {
    v24: { start: '2025-05-06', lts: '2025-10-28', maintenance: '2026-10-20', end: '2028-04-30' },
    v25: { start: '2025-10-15', maintenance: '2026-04-01', end: '2026-06-01' },
    v26: { start: '2026-05-05', lts: '2026-10-28', maintenance: '2027-10-20', end: '2029-04-30' },
    v27: { start: '2027-04-22', lts: '2027-10-20', end: '2030-04-30' },
  };
  const before = nodeSupportFacts(schedule, '2026-10-27');
  assert.equal(before.activeLts, null);
  assert.equal(before.latestLts, 26);
  assert.equal(before.lines.find(l => l.major === 24).phase, 'maintenance');
  assert.equal(before.lines.find(l => l.major === 25).phase, 'eol');
  assert.equal(before.lines.find(l => l.major === 26).phase, 'current');
  assert.equal(before.lines.find(l => l.major === 27).phase, 'future');
  const ltsDay = nodeSupportFacts(schedule, '2026-10-28');
  assert.equal(ltsDay.activeLts, 26);
  assert.equal(ltsDay.lines.find(l => l.major === 26).phase, 'active');
  const later = nodeSupportFacts(schedule, '2028-05-01');
  assert.equal(later.lines.find(l => l.major === 24).phase, 'eol');
  assert.equal(later.activeLts, 27);
  assert.equal(later.latestLts, 27);
});
test('classifyNotes: headings, conventional commits and flat plugin bullets', () => {
  assert.equal(classifyNotes('## Breaking Changes\n- removed x').suggestedPriority, 'P0-candidate');
  assert.equal(classifyNotes('- feat!: drop node 18').suggestedPriority, 'P0-candidate');
  assert.equal(classifyNotes('## Fixes\n- GHSA-abcd-efgh-ijkl patched').suggestedPriority, 'P0-candidate');
  assert.equal(classifyNotes('- Added `foo` option to the dialog.').suggestedPriority, 'P1-candidate');
  assert.equal(classifyNotes('- Fixed a crash when closing.').suggestedPriority, 'P2-candidate');
  assert.equal(classifyNotes('').suggestedPriority, 'unclassified');
});
test('changelogSections splits Keep-a-Changelog files; refVersion reads action/package tags', () => {
  const s = changelogSections('# Changelog\n\n## \\[2.3.0]\n\n- Added a\n\n## \\[2.2.1]\n\n- Fixed b\n');
  assert.deepEqual(s.map(x => x.version), ['2.3.0', '2.2.1']); assert.match(s[1].body, /Fixed b/);
  assert.deepEqual(refVersion('action-v1.0.0'), { major: 1, minor: 0, patch: 0 });
  assert.deepEqual(refVersion('v4'), { major: 4, minor: null, patch: null });
  assert.equal(refVersion('electron-builder@26.1.2').major, 26);
  assert.equal(refVersion('main'), null);
});

// ---------------- CI traps ----------------
const scan = (yml, over = {}) => runTraps([{ file: 'w.yml', text: yml }], defaultContext(over)).map(f => f.id);
test('stripComments keeps line numbers and ignores # inside quotes', () => {
  const t = stripComments("a: 1 # gh release create\nb: 'x # y'\n# whole line");
  assert.equal(t.split('\n').length, 3); assert.equal(t.includes('gh release create'), false); assert.match(t, /'x # y'/);
});
test('a comment explaining a step is not the step', () => {
  const yml = "on:\n  push:\n    tags: [v*]\njobs:\n  a:\n    steps:\n      # releaseDraft: true would never be published\n      - run: echo hi\n";
  assert.equal(scan(yml).includes('draft-never-published'), false);
});
test('draft created but never published is P0', () => {
  const yml = "on:\n  push:\n    tags: [v*]\npermissions:\n  contents: write\njobs:\n  b:\n    steps:\n      - uses: tauri-apps/tauri-action@x\n        with:\n          releaseDraft: true\n";
  const ids = scan(yml, { isTauri: true }); assert.ok(ids.includes('draft-never-published'));
  const f = runTraps([{ file: 'w.yml', text: yml }], defaultContext({ isTauri: true })).find(x => x.id === 'draft-never-published');
  assert.equal(f.severity, 'P0'); assert.equal(f.line, 11); assert.equal(f.confidence, 'heuristic');
});

test('an explicit manual release mode keeps a verified draft for human publication', () => {
  const workflow = "env:\n  DESKTOP_RELEASE_MODE: manual\njobs:\n  build:\n    steps:\n      - uses: tauri-apps/tauri-action@v1\n        with:\n          releaseDraft: true\n";
  assert.equal(scan(workflow).includes('draft-never-published'), false);
  assert.equal(scan(workflow.replace('DESKTOP_RELEASE_MODE: manual', 'DESKTOP_RELEASE_MODE: automatic')).includes('draft-never-published'), true);
});
test('a throwing trap is reported through onError instead of looking clean', () => {
  const trap = { id: 'test-throw', severity: 'P1', applies: () => true, test: () => { throw new Error('boom'); } };
  TRAPS.push(trap);
  try {
    const errors = [];
    const findings = runTraps([{ file: 'w.yml', text: 'jobs:\n  a:\n    steps: []\n' }], defaultContext({}), (e) => errors.push(e));
    assert.deepEqual(findings, []);
    assert.equal(errors.length, 1); assert.equal(errors[0].id, 'test-throw');
  } finally { TRAPS.pop(); }
});
test('yarn install flags: classic needs --frozen-lockfile, berry needs --immutable + corepack', () => {
  const classic = "jobs:\n  a:\n    steps:\n      - run: yarn install\n";
  assert.ok(scan(classic, { lockfiles: { yarn: 'yarn.lock' }, yarnFlavor: 'classic' }).includes('yarn-install-not-frozen'));
  assert.equal(scan("jobs:\n  a:\n    steps:\n      - run: yarn install --frozen-lockfile\n", { lockfiles: { yarn: 'yarn.lock' }, yarnFlavor: 'classic' }).includes('yarn-install-not-frozen'), false);
  const berry = scan("jobs:\n  a:\n    steps:\n      - run: yarn install --immutable\n", { lockfiles: { yarn: 'yarn.lock' }, yarnFlavor: 'berry' });
  assert.equal(berry.includes('yarn-install-not-frozen'), false); assert.ok(berry.includes('yarn-berry-corepack'));
});
test('npm: bare `npm install` in CI is flagged; npm ci, global tools, named packages and comments are not', () => {
  const ctx = { lockfiles: { npm: 'package-lock.json' } };
  const job = run => `jobs:\n  a:\n    steps:\n      - run: ${run}\n`;
  assert.ok(scan(job('npm install'), ctx).includes('npm-install-not-ci'));
  assert.ok(scan(job('npm i --no-audit && npm test'), ctx).includes('npm-install-not-ci'));
  assert.ok(scan("jobs:\n  a:\n    steps:\n      - run: |\n          npm install\n          npm test\n", ctx).includes('npm-install-not-ci'));
  for (const ok of ['npm ci', 'npm install -g @tauri-apps/cli', 'npm i --global pnpm', 'npm install left-pad', 'npm init -y', 'echo hi # npm install'])
    assert.equal(scan(job(ok), ctx).includes('npm-install-not-ci'), false, ok);
  assert.equal(scan("jobs:\n  a:\n    steps:\n      - name: npm install\n        run: npm ci\n", ctx).includes('npm-install-not-ci'), false);
  assert.equal(scan(job('npm ci'), ctx).includes('npm-ci-without-lockfile'), false);
});
test('Electron >= 42 runtime download: npm uses the installed Electron script; local bins remain recognized', () => {
  const yml = "jobs:\n  a:\n    steps:\n      - run: npm ci\n      - run: npx electron-builder --win nsis --publish never\n";
  const f = runTraps([{ file: 'w.yml', text: yml }], defaultContext({ electronMajor: 45, lockfiles: { npm: 'package-lock.json' } })).find(x => x.id === 'electron-runtime-download');
  assert.ok(f); assert.match(f.fix, /node node_modules\/electron\/install\.js/);
  assert.equal(scan(yml.replace('      - run: npx electron', '      - run: npx install-electron\n      - run: npx electron'), { electronMajor: 45 }).includes('electron-runtime-download'), false);
  for (const command of [
    'node node_modules/electron/install.js',
    'node ./node_modules/electron/install.js',
    'node "node_modules/electron/install.js"',
    'node .\\node_modules\\electron\\install.js',
  ]) {
    const fixed = yml.replace('      - run: npx electron', `      - run: ${command}\n      - run: npx electron`);
    assert.equal(scan(fixed, { electronMajor: 45 }).includes('electron-runtime-download'), false, command);
  }
  assert.ok(scan(yml + '      # node node_modules/electron/install.js\n', { electronMajor: 45 }).includes('electron-runtime-download'));
  assert.ok(scan(yml.replace('      - run: npm ci', '      - run: npm ci\n      - run: node node_modules/electron/not-install.js'), { electronMajor: 45 }).includes('electron-runtime-download'));
});
test('winget must follow publish; release:published is flagged (GITHUB_TOKEN does not trigger it)', () => {
  const ok = "jobs:\n  publish:\n    steps:\n      - run: gh api -X PATCH x -F draft=false -f make_latest=true\n  winget:\n    needs: publish\n    steps:\n      - uses: vedantmgoyal9/winget-releaser@x\n";
  assert.equal(scan(ok).includes('winget-before-publish'), false);
  const bad = "on:\n  release:\n    types: [published]\njobs:\n  w:\n    steps:\n      - run: komac update X --submit\n";
  const ids = scan(bad); assert.ok(ids.includes('winget-before-publish')); assert.ok(ids.includes('release-event-github-token'));
});
test('platform coverage uses house-style default (all three OS) and the bundled templates are clean', async () => {
  const fs = await import('node:fs'); const path = await import('node:path'); const { fileURLToPath } = await import('node:url');
  const dir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../templates/workflows');
  assert.ok(scan("on:\n  push:\n    tags: [v*]\njobs:\n  a:\n    runs-on: windows-latest\n    steps:\n      - uses: tauri-apps/tauri-action@x\n", { isTauri: true }).includes('platform-coverage'));
  const tauri = fs.readFileSync(path.join(dir, 'release-tauri.yml'), 'utf8'), electron = fs.readFileSync(path.join(dir, 'release-electron.yml'), 'utf8');
  const npmLock = { npm: 'package-lock.json' };
  assert.deepEqual(runTraps([{ file: 't', text: tauri }], defaultContext({ isTauri: true, usesTauriUpdater: true, tauriBothWindowsBundles: true, lockfiles: npmLock })), []);
  assert.deepEqual(runTraps([{ file: 'e', text: electron }], defaultContext({ hasElectron: true, hasElectronUpdater: true, electronMajor: 45, lockfiles: npmLock, enginesNode: '>=22' })), []);
  const ci = fs.readFileSync(path.join(dir, 'ci.yml'), 'utf8');
  assert.deepEqual(runTraps([{ file: 'c', text: ci }], defaultContext({ isTauri: true, lockfiles: npmLock })), []);
  // npm templates copied into a Yarn repo without converting the install line: caught, not silently green.
  const yarnRepo = runTraps([{ file: 'c', text: ci }], defaultContext({ isTauri: true, lockfiles: { yarn: 'yarn.lock' }, yarnFlavor: 'classic' })).map(f => f.id);
  assert.ok(yarnRepo.includes('npm-ci-without-lockfile')); assert.ok(yarnRepo.includes('cache-lockfile-mismatch'));
  for (const f of fs.readdirSync(dir)) for (const m of fs.readFileSync(path.join(dir, f), 'utf8').matchAll(/uses:\s*([^\s@]+)@(\S+)/g))
    // house style: 大版本标签（补丁随标签自动到手）。不钉 SHA——每次升级手改哈希，
    // 实际就永远不动了；分支引用（stable）只给 rust-toolchain 这类官方用法。
    assert.match(m[2], /^(v\d+|stable)$/, `${f}: ${m[1]} must be pinned to a major tag, got ${m[2]}`);
});
test('tauri-linux-deps is scoped to the Ubuntu job that actually builds Tauri', () => {
  const yml = "on:\n  push:\n    tags: [v*]\npermissions:\n  contents: write\njobs:\n  security:\n    runs-on: ubuntu-latest\n    steps:\n      - run: cargo audit --file src-tauri/Cargo.lock\n  release:\n    runs-on: windows-latest\n    steps:\n      - uses: tauri-apps/tauri-action@v1\n";
  assert.equal(scan(yml, { isTauri: true }).includes('tauri-linux-deps'), false);
  const bad = "on:\n  push:\n    tags: [v*]\npermissions:\n  contents: write\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: tauri-apps/tauri-action@v1\n";
  assert.ok(scan(bad, { isTauri: true }).includes('tauri-linux-deps'));
  const good = bad.replace('    steps:\n', '    steps:\n      - run: sudo apt-get install -y libwebkit2gtk-4.1-dev\n');
  assert.equal(scan(good, { isTauri: true }).includes('tauri-linux-deps'), false);
});
test('tag/version traps require a recognizable versionAsserted marker', () => {
  const base = "on:\n  push:\n    tags: [v*]\npermissions:\n  contents: write\njobs:\n  release:\n    if: github.ref_type == 'tag'\n    steps:\n      - uses: tauri-apps/tauri-action@v1\n        with:\n          tagName: ${{ github.ref_name }}\n";
  assert.equal(scan(base, { isTauri: true }).includes('tagname-from-ref-unasserted'), false);
  assert.equal(scan(base, { isTauri: true }).includes('version-single-source'), false);
  const noMarker = base.replace("    if: github.ref_type == 'tag'\n", '') + '      - run: echo "tag checked"\n';
  assert.ok(scan(noMarker, { isTauri: true }).includes('tagname-from-ref-unasserted'));
  assert.ok(scan(noMarker, { isTauri: true }).includes('version-single-source'));
});
test('tagName from ref is judged in its own job, not by a marker elsewhere', () => {
  const yml = "on:\n  push:\n    tags: [v*]\npermissions:\n  contents: write\njobs:\n  validate:\n    if: github.ref_type == 'tag'\n    steps:\n      - run: echo ok\n  build:\n    steps:\n      - uses: tauri-apps/tauri-action@v1\n        with:\n          tagName: ${{ github.ref_name }}\n";
  assert.ok(scan(yml, { isTauri: true }).includes('tagname-from-ref-unasserted'));
});
test('every trap has a unique id and P0/P1/P2 severity', () => {
  const ids = TRAPS.map(t => t.id); assert.equal(new Set(ids).size, ids.length);
  for (const t of TRAPS) assert.match(t.severity, /^P[012]$/);
  // the documented table in references/ci-traps.md lists every trap id
  return import('node:fs').then(fs => { const doc = fs.readFileSync(new URL('../references/ci-traps.md', import.meta.url), 'utf8');
    for (const id of ids) assert.ok(doc.includes('`' + id + '`'), `ci-traps.md is missing ${id}`);
    assert.equal(/\$\{(c|m)\.|\| 未知 \|/.test(doc), false, 'ci-traps.md contains unrendered template text'); });
});


test('Yarn does not resolve an unmatched declaration from a unique candidate', () => {
  const lock = parseYarnLock('electron@^40.0.0:\n  version "40.0.1"');
  const resolved = resolveFromLock('yarn', lock, { name: 'electron', declared: '^41.0.0' });
  assert.equal(resolved.version, null);
  assert.deepEqual(resolved.candidates, ['40.0.1']);
});

test('release permissions belong to the uploading job and job maps replace inherited permissions', () => {
  const workflow = ['permissions:', '  contents: read', 'jobs:', '  other:', '    permissions: { contents: write }',
    '    steps:', '      - run: echo ok', '  upload:', '    steps:', '      - uses: softprops/action-gh-release@v3', ''].join('\n');
  assert.ok(scan(workflow).includes('release-permissions'));
  assert.ok(!scan(workflow.replace('  upload:', '  upload:\n    permissions: { contents: write }')).includes('release-permissions'));
  assert.ok(!scan(workflow.replace('  upload:', '  upload:\n    permissions: { contents: "write" }')).includes('release-permissions'));
  const inherited = workflow.replace('  contents: read', '  contents: write');
  assert.ok(!scan(inherited).includes('release-permissions'));
  assert.ok(scan(inherited.replace('  upload:', '  upload:\n    permissions: { actions: read }')).includes('release-permissions'));
  const token = workflow + '        with:\n          token: ${{ secrets.RELEASE_TOKEN }}\n';
  assert.ok(!scan(token).includes('release-permissions'));
});

test('latest status does not publish a draft', () => {
  const workflow = 'jobs:\n  upload:\n    steps:\n      - uses: softprops/action-gh-release@v3\n        with:\n          draft: true\n          make_latest: false\n';
  assert.ok(scan(workflow).includes('draft-never-published'));
  assert.ok(!scan(workflow + '      - run: gh release edit v1.0.0 --draft=false\n').includes('draft-never-published'));
  assert.ok(!scan(workflow + '  publish:\n    steps:\n      - uses: softprops/action-gh-release@v3\n        with:\n          draft: false\n').includes('draft-never-published'));
});

test('workflow coverage distinguishes checks, publishers, manual mode and delegation', () => {
  const files = [
    {file: 'ci.yml', text: 'on: [pull_request]\njobs:\n  test:\n    steps:\n      - run: npm test'},
    {file: 'tag.yml', text: 'on:\n  push:\n    tags: [v*]\njobs:\n  test:\n    steps:\n      - run: npm test'},
  ];
  assert.deepEqual(workflowCoverage(files), {pullRequest: ['ci.yml'], release: [], delegated: [], manual: []});
  files.push({file: 'release.yml', text: 'env:\n  DESKTOP_RELEASE_MODE: manual\njobs:\n  build:\n    steps:\n      - run: gh release upload v1.0.0 app.exe'});
  files.push({file: 'reuse.yml', text: 'jobs:\n  release:\n    uses: owner/repo/.github/workflows/release.yml@v1'});
  assert.deepEqual(workflowCoverage(files), {pullRequest: ['ci.yml'], release: ['release.yml'], delegated: ['reuse.yml'], manual: ['release.yml']});
});

test('a build-only Tauri action does not claim release coverage or need a write token', () => {
  const text = 'on: push\njobs:\n  build:\n    steps:\n      - uses: tauri-apps/tauri-action@v1\n      - run: echo pull_request\n';
  assert.deepEqual(workflowCoverage([{file: 'ci.yml', text}]), {pullRequest: [], release: [], delegated: [], manual: []});
  assert.ok(!scan(text).includes('release-permissions'));
  const publish = text.replace('      - run: echo pull_request', '        with:\n          tagName: v1.0.0');
  assert.deepEqual(workflowCoverage([{file: 'ci.yml', text: publish}]).release, ['ci.yml']);
  assert.ok(scan(publish).includes('release-permissions'));
});

test('a custom release uploader is delegated evidence requiring script inspection', () => {
  const text = 'on: push\njobs:\n  upload:\n    permissions:\n      contents: write\n    steps:\n      - run: node scripts/release-draft.mjs dist\n';
  const coverage = workflowCoverage([{file: 'release.yml', text}]);
  assert.deepEqual(coverage.release, []);
  assert.deepEqual(coverage.delegated, ['release.yml']);
  assert.deepEqual(workflowCoverage([{file: 'ci.yml', text: text.replace('      contents: write', '      contents: read')}]).delegated, []);
});
