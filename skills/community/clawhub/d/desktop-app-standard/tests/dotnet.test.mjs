import test from 'node:test';
import assert from 'node:assert/strict';
import {
  stripJsonComments, parseGlobalJson, parseTfms, tfmInfo, sdkParts,
  rollForwardReach, normalizeMetadata, analyzeDotnet,
} from '../scripts/dotnet.mjs';

test('global.json comments and test runner are parsed; strict JSON still required', () => {
  const g = parseGlobalJson(`{
    // SDK pin
    "sdk": { "version": "10.0.402", "rollForward": "latestFeature", "allowPrerelease": false },
    /* MTP */ "test": { "runner": "Microsoft.Testing.Platform" }
  }`);
  assert.equal(g.version, '10.0.402');
  assert.equal(g.rollForward, 'latestFeature');
  assert.equal(g.allowPrerelease, false);
  assert.equal(g.testRunner, 'Microsoft.Testing.Platform');
  assert.equal(stripJsonComments('{"a":"// not a comment"}').includes('// not a comment'), true);
  assert.throws(() => parseGlobalJson('{ "sdk": '));
});

test('TFM parsing: project, props, comments, old-style Framework version and unresolved properties', () => {
  assert.deepEqual(parseTfms('<PropertyGroup><TargetFramework>net10.0-windows</TargetFramework></PropertyGroup>').tfms, ['net10.0-windows']);
  assert.deepEqual(parseTfms('<TargetFrameworks> net8.0 ; net10.0 </TargetFrameworks>').tfms, ['net8.0', 'net10.0']);
  assert.deepEqual(parseTfms('<!-- <TargetFramework>net6.0</TargetFramework> --><TargetFramework>$(Tfm)</TargetFramework>'), { tfms: [], unresolved: ['$(Tfm)'] });
  assert.deepEqual(parseTfms('<TargetFrameworkVersion>v4.8</TargetFrameworkVersion>').tfms, ['net48']);
  assert.deepEqual(parseTfms('<TargetFramework>netstandard2.0</TargetFramework>').tfms, ['netstandard2.0']);
});

test('TFM classification distinguishes runtime, library, .NET Framework and unknown', () => {
  assert.deepEqual(tfmInfo('net10.0-windows'), { tfm: 'net10.0-windows', kind: 'runtime', major: 10, minor: 0, channel: '10.0', os: 'windows' });
  assert.deepEqual(tfmInfo('netcoreapp3.1'), { tfm: 'netcoreapp3.1', kind: 'runtime', major: 3, minor: 1, channel: '3.1' });
  assert.equal(tfmInfo('netstandard2.1').kind, 'library');
  assert.equal(tfmInfo('net48').kind, 'framework');
  assert.equal(tfmInfo('net472').kind, 'framework');
  assert.equal(tfmInfo('portable').kind, 'unknown');
});

test('SDK parts use feature band and patch; rollForward latest* semantics are explicit', () => {
  assert.deepEqual(sdkParts('10.0.402'), { version: '10.0.402', major: 10, minor: 0, featureBand: 4, patch: 2, prerelease: null });
  assert.equal(sdkParts('10.0.4'), null);
  assert.equal(rollForwardReach('latestFeature', '10.0.100', '10.0.402').guaranteed, true);
  assert.equal(rollForwardReach('latestPatch', '10.0.100', '10.0.402').guaranteed, false);
  assert.equal(rollForwardReach('latestPatch', '10.0.300', '10.0.302').guaranteed, true);
  assert.equal(rollForwardReach('patch', '10.0.100', '10.0.402').guaranteed, false);
  assert.equal(rollForwardReach(undefined, '10.0.100', '10.0.402').guaranteed, false);
  assert.equal(rollForwardReach('disable', '10.0.100', '10.0.402').guaranteed, false);
  assert.equal(rollForwardReach('latestMajor', '9.0.100', '10.0.402').guaranteed, true);
  assert.equal(rollForwardReach('latestFeature', '10.0.402', '10.0.402').guaranteed, true);
  assert.equal(rollForwardReach('latestFeature', '10.0.500', '10.0.402').guaranteed, false);
});

test('metadata normalization keeps support/EOL, latest SDK/runtime and SDK index', () => {
  const m = normalizeMetadata({
    'latest-sdk': '10.0.402', 'latest-release': '10.0.13', 'latest-runtime': '10.0.13',
    'support-phase': 'active', 'eol-date': '2028-11-14',
    releases: [{ sdks: [{ version: '10.0.100' }, { version: '10.0.402' }] }],
  });
  assert.equal(m.latestSdk, '10.0.402');
  assert.equal(m.latestRelease, '10.0.13');
  assert.equal(m.latestRuntime, '10.0.13');
  assert.equal(m.supportPhase, 'active');
  assert.equal(m.eolDate, '2028-11-14');
  assert.deepEqual(m.sdkVersions, ['10.0.100', '10.0.402']);
});

const metadata = {
  '8.0': normalizeMetadata({ 'latest-sdk': '8.0.426', 'latest-release': '8.0.19', 'support-phase': 'maintenance', 'eol-date': '2026-11-10', releases: [] }),
  '9.0': normalizeMetadata({ 'latest-sdk': '9.0.319', 'latest-release': '9.0.9', 'support-phase': 'maintenance', 'eol-date': '2026-11-10', releases: [] }),
  '10.0': normalizeMetadata({ 'latest-sdk': '10.0.402', 'latest-release': '10.0.13', 'latest-runtime': '10.0.13', 'support-phase': 'active', 'eol-date': '2028-11-14', releases: [{ sdks: [{ version: '10.0.100' }, { version: '10.0.402' }] }] }),
};
const NOW = '2026-10-24T00:00:00Z';

test('active + EOL-soon + library TFM: only the expiring runtime is a finding', () => {
  const r = analyzeDotnet({
    projects: [
      { file: 'App/App.csproj', tfms: ['net10.0-windows'], globalJson: 'global.json' },
      { file: 'Legacy/Legacy.csproj', tfms: ['net8.0'], globalJson: 'global.json' },
      { file: 'Lib/Lib.csproj', tfms: ['netstandard2.0'], globalJson: null },
    ],
    globalJsons: [{ file: 'global.json', version: '10.0.100', rollForward: 'latestFeature' }],
    metadata, now: NOW,
  });
  assert.equal(r.detected, true);
  assert.deepEqual(r.channels.map(c => c.channel).sort(), ['10.0', '8.0']);
  const eolSoon = r.framework.find(f => f.id === 'dotnet-runtime-eol-soon');
  assert.equal(eolSoon.severity, 'P1');
  assert.match(eolSoon.detail, /Legacy\/Legacy\.csproj/);
  assert.equal(r.framework.some(f => f.id === 'dotnet-runtime-eol'), false);
  assert.equal(r.framework.some(f => f.id === 'dotnet-sdk-pin-behind'), false);
  assert.equal(r.globalJson[0].guaranteedLatest, true);
  assert.equal(r.globalJson[0].latestSdk, '10.0.402');
});

test('SDK pin behind latest and default patch are reported; latestFeature is not', () => {
  const base = { projects: [{ file: 'App/App.csproj', tfms: ['net10.0'], globalJson: 'global.json' }], metadata, now: NOW };
  let r = analyzeDotnet({ ...base, globalJsons: [{ file: 'global.json', version: '10.0.100', rollForward: 'patch' }] });
  const f = r.framework.find(x => x.id === 'dotnet-sdk-pin-behind');
  assert.equal(f.severity, 'P2');
  assert.match(f.detail, /10\.0\.402/);
  r = analyzeDotnet({ ...base, globalJsons: [{ file: 'global.json', version: '10.0.100', rollForward: 'latestFeature' }] });
  assert.equal(r.framework.some(x => x.id === 'dotnet-sdk-pin-behind'), false);
});

test('an SDK older than the TFM cannot target it, even when its own channel reaches latest', () => {
  const r = analyzeDotnet({
    projects: [{ file: 'App/App.csproj', tfms: ['net10.0'], globalJson: 'global.json' }],
    globalJsons: [{ file: 'global.json', version: '9.0.100', rollForward: 'latestFeature' }],
    metadata, now: NOW,
  });
  const f = r.framework.find(x => x.id === 'dotnet-sdk-cannot-target');
  assert.equal(f.severity, 'P0');
  assert.match(f.detail, /9\.0\.100/);
  assert.match(f.detail, /net10\.0/);
});

test('EOL, maintenance and offline behaviour are distinguished', () => {
  let r = analyzeDotnet({
    projects: [{ file: 'Old/Old.csproj', tfms: ['net6.0'], globalJson: null }], globalJsons: [],
    metadata: { '6.0': normalizeMetadata({ 'latest-sdk': '6.0.428', 'latest-release': '6.0.36', 'support-phase': 'maintenance', 'eol-date': '2024-11-12', releases: [] }) }, now: NOW,
  });
  assert.equal(r.framework.find(f => f.id === 'dotnet-runtime-eol').severity, 'P0');
  r = analyzeDotnet({
    projects: [{ file: 'Old/Old.csproj', tfms: ['net8.0'], globalJson: null }], globalJsons: [],
    metadata: { '8.0': { ...metadata['8.0'], eolDate: '2027-11-10' } }, now: NOW,
  });
  assert.equal(r.framework.find(f => f.id === 'dotnet-runtime-maintenance').severity, 'P2');
  r = analyzeDotnet({
    projects: [{ file: 'App/App.csproj', tfms: ['net10.0'], globalJson: 'global.json' }],
    globalJsons: [{ file: 'global.json', version: '10.0.402', rollForward: 'latestFeature' }],
    metadata: {}, now: NOW, offline: true,
  });
  assert.equal(r.framework.some(f => f.id.startsWith('dotnet-runtime-')), false);
  assert.ok(r.warnings.some(w => /offline/.test(w)));
  assert.equal(r.incomplete.length, 0);
});

test('no global.json / missing version / invalid version are reported without pretending to know latest', () => {
  let r = analyzeDotnet({ projects: [{ file: 'App/App.csproj', tfms: ['net10.0'], globalJson: null }], globalJsons: [], metadata, now: NOW });
  assert.equal(r.framework.find(f => f.id === 'dotnet-no-global-json').severity, 'notice');
  r = analyzeDotnet({ projects: [{ file: 'App/App.csproj', tfms: ['net10.0'], globalJson: 'global.json' }], globalJsons: [{ file: 'global.json', version: null }], metadata, now: NOW });
  assert.equal(r.framework.find(f => f.id === 'dotnet-sdk-version-missing').severity, 'notice');
  r = analyzeDotnet({ projects: [{ file: 'App/App.csproj', tfms: ['net10.0'], globalJson: 'global.json' }], globalJsons: [{ file: 'global.json', version: '10.0' }], metadata, now: NOW });
  assert.equal(r.framework.find(f => f.id === 'dotnet-sdk-invalid').severity, 'P2');
  r = analyzeDotnet({ projects: [{ file: 'App/App.csproj', tfms: [], unresolved: ['$(Tfm)'], globalJson: null }], globalJsons: [], metadata, now: NOW });
  assert.ok(r.incomplete.some(x => /MSBuild 属性/.test(x)));
});

test('CI SDK sources: two inputs and shadowing are P1; comments do not trigger; missing setup is P2', () => {
  const projects = [{ file: 'App/App.csproj', tfms: ['net10.0'], globalJson: 'global.json' }];
  const globals = [{ file: 'global.json', version: '10.0.402', rollForward: 'latestFeature' }];
  const run = text => analyzeDotnet({ projects, globalJsons: globals, metadata, workflows: [{ file: 'w.yml', text }], now: NOW }).ci;
  let f = run('jobs:\n  b:\n    steps:\n      - uses: actions/setup-dotnet@v6\n        with:\n          global-json-file: global.json\n          dotnet-version: 10.0.402\n');
  assert.equal(f.find(x => x.id === 'dotnet-version-two-sources').severity, 'P1');
  f = run('jobs:\n  b:\n    steps:\n      - uses: actions/setup-dotnet@v6\n        with:\n          dotnet-version: 10.0.402\n');
  assert.equal(f.find(x => x.id === 'dotnet-version-shadows-global-json').severity, 'P1');
  f = run('jobs:\n  b:\n    steps:\n      # dotnet-version: 10.0.402\n      - uses: actions/setup-dotnet@v6\n        with:\n          global-json-file: global.json\n');
  assert.equal(f.some(x => x.id.startsWith('dotnet-version-')), false);
  f = run('jobs:\n  b:\n    steps:\n      - run: dotnet test\n');
  assert.equal(f.find(x => x.id === 'dotnet-ci-setup-missing').severity, 'P2');
  f = analyzeDotnet({ projects, globalJsons: globals, metadata, workflows: [{ file: 'w.yml', text: 'jobs:\n  b:\n    steps:\n      - uses: actions/setup-dotnet@v6\n        with:\n          global-json-file: global.json\n' }], now: NOW }).ci;
  assert.equal(f.length, 0);
});

test('major roll-forward permits a newer installed SDK to build a newer TFM', () => {
  const params = { projects: [{ file: 'App.csproj', tfms: ['net10.0'], globalJson: 'global.json' }], metadata, now: NOW };
  for (const policy of ['latestMajor', 'major', 'disable', 'latestFeature']) {
    const r = analyzeDotnet({ ...params, globalJsons: [{ file: 'global.json', version: '8.0.100', rollForward: policy }] });
    assert.equal(r.framework.some(f => f.id === 'dotnet-sdk-cannot-target'), ['disable', 'latestFeature'].includes(policy), policy);
  }
});

test('SDK inputs and missing setup are scoped to their own steps and jobs', () => {
  const text = [
    'jobs:', '  first:', '    steps:', '      - uses: actions/setup-dotnet@v6',
    '        with: { global-json-file: global.json }', '      - uses: actions/setup-dotnet@v6',
    '        with: { dotnet-version: 9.0.100 }', '  second:', '    steps:', '      - run: dotnet build',
    '  web:', '    steps:', '      - run: npm ci',
  ].join('\n');
  const r = analyzeDotnet({
    projects: [{ file: 'App.csproj', tfms: ['net10.0'], globalJson: 'global.json' }],
    globalJsons: [{ file: 'global.json', version: '10.0.100' }], metadata, now: NOW,
    workflows: [{ file: 'ci.yml', text }],
  });
  assert.deepEqual(r.ci.map(f => [f.id, f.line]), [
    ['dotnet-version-shadows-global-json', 6], ['dotnet-ci-setup-missing', 8],
  ]);
});
