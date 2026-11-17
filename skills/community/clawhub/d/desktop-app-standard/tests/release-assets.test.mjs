import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { hashFile, recordEvidence, verifyEvidence, verifyFeed, verifyPublicRelease, verifyDraftRelease, releaseReady } from '../scripts/release-assets.mjs';

test('prepublication checks accept only drafts and enforce full feed and digest verification', async () => {
  const data = await fixture();
  try {
    const release = {tag_name: data.common.tag, draft: true, prerelease: false,
      assets: [...data.assets, {name: 'latest.json', digest: 'sha256:' + await hashFile(path.join(data.directory, 'latest.json'))}]};
    const options = {...data.common, directory: data.directory, release, requiredAssets: ['latest.json'], platforms: ['windows-x86_64']};
    assert.match(await verifyDraftRelease(options), /latest.json/);
    await assert.rejects(verifyPublicRelease(options), /public stable/);
    await assert.rejects(verifyDraftRelease({...options, release: {...release, draft: false}}), /unpublished draft/);
    await assert.rejects(verifyDraftRelease({...options, platforms: ['linux-aarch64']}), /Missing updater target/);
    fs.appendFileSync(path.join(data.directory, data.names[0]), 'tampered');
    await assert.rejects(verifyDraftRelease(options), /digest mismatch/);
  } finally { fs.rmSync(data.directory, {recursive: true, force: true}); }
});

test('public verification rejects missing whole feeds, wrong URLs, signatures and payload hashes; reruns exclude checksums', async () => {
  const data = await fixture();
  const platforms = Object.keys(data.feed.platforms);
  const feedAsset = {name: 'latest.json', digest: 'sha256:' + await hashFile(path.join(data.directory, 'latest.json'))};
  const release = {tag_name: data.common.tag, draft: false, prerelease: false, assets: [...data.assets, feedAsset, {name: 'SHA256SUMS', digest: 'sha256:' + 'b'.repeat(64)}]};
  const verify = () => verifyPublicRelease({...data.common, directory: data.directory, release, requiredAssets: ['latest.json'], platforms});
  try {
    const sums = await verify();
    assert.doesNotMatch(sums, /  SHA256SUMS\n/);
    fs.writeFileSync(path.join(data.directory, 'SHA256SUMS'), sums);
    assert.equal(await verify(), sums);
    const betaFeed = {...data.feed, version: '1.2.3-beta.1'};
    fs.writeFileSync(path.join(data.directory, 'latest.json'), JSON.stringify(betaFeed));
    feedAsset.digest = 'sha256:' + await hashFile(path.join(data.directory, 'latest.json'));
    await verifyPublicRelease({...data.common, version: betaFeed.version, tag: 'v' + betaFeed.version, directory: data.directory,
      release: {...release, tag_name: 'v' + betaFeed.version, prerelease: true}, requiredAssets: ['latest.json'], platforms});
    for (const problem of ['version', 'platform', 'signature', 'url']) {
      const feed = structuredClone(data.feed);
      if (problem === 'version') feed.version = '0.0.1';
      if (problem === 'platform') delete feed.platforms[platforms[0]];
      if (problem === 'signature') feed.platforms[platforms[0]].signature = 'changed';
      if (problem === 'url') feed.platforms[platforms[0]].url = 'https://github.com/other/app/releases/download/v1.2.3/missing.exe';
      fs.writeFileSync(path.join(data.directory, 'latest.json'), JSON.stringify(feed));
      feedAsset.digest = 'sha256:' + await hashFile(path.join(data.directory, 'latest.json'));
      await assert.rejects(verify());
    }
    fs.writeFileSync(path.join(data.directory, 'latest.json'), JSON.stringify(data.feed));
    feedAsset.digest = 'sha256:' + await hashFile(path.join(data.directory, 'latest.json'));
    fs.unlinkSync(path.join(data.directory, 'latest.json'));
    await assert.rejects(verify(), /Missing local asset/);
    fs.writeFileSync(path.join(data.directory, 'latest.json'), JSON.stringify(data.feed));
    const digest = data.assets[0].digest;
    data.assets[0].digest = null;
    await assert.rejects(verify(), /Invalid asset or digest/);
    data.assets[0].digest = digest;
    fs.appendFileSync(path.join(data.directory, data.names[0]), 'changed payload');
    await assert.rejects(verify(), /digest mismatch/);
  } finally { fs.rmSync(data.directory, {recursive: true, force: true}); }
});

test('winget readiness requires the complete inventory and completion marker from a stable public release', () => {
  const requiredAssets = ['setup.exe', 'arm64.zip', 'SHA256SUMS.txt'];
  const release = {tag_name: 'v1.2.3', draft: false, prerelease: false, assets: requiredAssets.map(name => ({name, digest: 'sha256:' + 'a'.repeat(64)}))};
  const options = {tag: 'v1.2.3', requiredAssets};
  releaseReady(release, options);
  for (const name of requiredAssets) assert.throws(() => releaseReady({...release, assets: release.assets.filter(asset => asset.name !== name)}, options), /Missing/);
  for (const field of ['draft', 'prerelease']) assert.throws(() => releaseReady({...release, [field]: true}, options), /public stable/);
  assert.throws(() => releaseReady(release, {...options, tag: 'v9.9.9'}), /public stable/);
  assert.throws(() => releaseReady({...release, assets: [{name:'setup.exe'}, ...release.assets.slice(1)]}, options), /digest/);
  assert.throws(() => releaseReady(release, {...options, requiredAssets: []}), /empty/);
});

async function fixture() {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'release-evidence-'));
  assert.equal(path.dirname(directory), path.resolve(os.tmpdir()));
  const names = ['Demo_1.2.3_x64-setup.exe', 'Demo_1.2.3_x64-setup.exe.sig'];
  fs.writeFileSync(path.join(directory, names[0]), 'new installer bytes');
  fs.writeFileSync(path.join(directory, names[1]), 'signed fixture');
  const assets = await Promise.all(names.map(async (name, index) => ({id: index + 1, name, digest: 'sha256:' + await hashFile(path.join(directory, name))})));
  const common = {version: '1.2.3', repo: 'org/app', tag: 'v1.2.3', commit: 'a'.repeat(40), runId: '123'};
  const target = 'x86_64-pc-windows-msvc';
  const feed = {version: common.version, platforms: {'windows-x86_64': {
    url: 'https://api.github.com/repos/org/app/releases/assets/1', signature: 'signed fixture',
  }}};
  fs.writeFileSync(path.join(directory, 'latest.json'), JSON.stringify(feed));
  const evidence = await recordEvidence({...common, target, paths: names.map(name => path.join(directory, name)), assets, feed});
  return {directory, names, assets, common, target, feed, evidence};
}

test('build evidence rejects stale, missing or modified draft assets and wrong run identity', async () => {
  const data = await fixture();
  try {
    const verify = evidence => verifyEvidence({...data.common, directory: data.directory, assets: data.assets,
      targets: [data.target], evidence: evidence ?? [data.evidence]});
    await verify();
    fs.writeFileSync(path.join(data.directory, 'old-installer.exe'), 'old draft');
    await assert.rejects(verify(), /asset set differs/);
    fs.unlinkSync(path.join(data.directory, 'old-installer.exe'));
    const installer = path.join(data.directory, data.names[0]);
    fs.renameSync(installer, installer + '.bak');
    await assert.rejects(verify(), /asset set differs/);
    fs.renameSync(installer + '.bak', installer);
    fs.writeFileSync(installer, 'changed installer bytes');
    await assert.rejects(verify(), /digest mismatch/);
    fs.writeFileSync(installer, 'new installer bytes');
    for (const field of ['commit', 'runId', 'version', 'target']) {
      await assert.rejects(verify([{...data.evidence, [field]: 'different'}]), /source or version mismatch/);
    }
    await assert.rejects(verify([]), /Missing or duplicate/);
    await assert.rejects(verify([data.evidence, data.evidence]), /Missing or duplicate/);
    await verify();
  } finally { fs.rmSync(data.directory, {recursive: true, force: true}); }
});

test('feed verification checks draft ownership, platform, artifact type, version and signature', async () => {
  const data = await fixture();
  try {
    const options = {...data.common, assets: data.assets, files: new Set(data.names), signatures: new Map([[data.names[1], 'signed fixture']])};
    const verify = feed => verifyFeed(feed, options);
    verify(data.feed);
    verifyFeed(data.feed, {...options, preferNsis: true});
    const entry = data.feed.platforms['windows-x86_64'];
    verify({...data.feed, platforms: {'windows-x86_64': {...entry, url: `https://github.com/org/app/releases/download/v1.2.3/${data.names[0]}`}}});
    for (const url of ['https://api.github.com/repos/org/app/releases/assets/999',
      `https://github.com/other/app/releases/download/v1.2.3/${data.names[0]}`,
      `https://github.com/org/app/releases/download/v0.0.1/${data.names[0]}`]) {
      assert.throws(() => verify({...data.feed, platforms: {'windows-x86_64': {...entry, url}}}));
    }
    assert.throws(() => verify({...data.feed, version: '0.0.1'}), /version/);
    assert.throws(() => verify({...data.feed, platforms: {'windows-aarch64': entry}}), /architecture/);
    assert.throws(() => verify({...data.feed, platforms: {'darwin-x86_64': entry}}), /type/);
    assert.throws(() => verify({...data.feed, platforms: {'windows-x86_64': {...entry, signature: 'wrong'}}}), /signature/);
    const msi = 'Demo_1.2.3_x64.msi';
    const msiFeed = {...data.feed, platforms: {'windows-x86_64': {url: `https://github.com/org/app/releases/download/v1.2.3/${msi}`, signature: 'signed fixture'}}};
    const msiOptions = {...options, assets: [{id: 4, name: msi}], files: new Set([msi, msi + '.sig']), signatures: new Map([[msi + '.sig', 'signed fixture']])};
    verifyFeed(msiFeed, msiOptions);
    assert.throws(() => verifyFeed(msiFeed, {...msiOptions, preferNsis: true}), /must use NSIS/);
    const changed = {...data.feed, platforms: {...data.feed.platforms, 'windows-x86_64-msi': entry}};
    fs.writeFileSync(path.join(data.directory, 'latest.json'), JSON.stringify(changed));
    await assert.rejects(verifyEvidence({...data.common, directory: data.directory, assets: data.assets,
      targets: [data.target], evidence: [data.evidence]}), /platform set/);
  } finally { fs.rmSync(data.directory, {recursive: true, force: true}); }
});

test('record and verify CLI use local built bytes and preserve existing evidence on failure', async () => {
  const data = await fixture();
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'release-command-'));
  assert.equal(path.dirname(temporary), path.resolve(os.tmpdir()));
  try {
    fs.renameSync(data.directory, path.join(temporary, 'dist'));
    const dist = path.join(temporary, 'dist');
    fs.writeFileSync(path.join(temporary, 'draft-assets.json'), JSON.stringify([data.assets]));
    fs.writeFileSync(path.join(temporary, 'build-feed.json'), JSON.stringify(data.feed));
    const env = {...process.env, RUNNER_TEMP: temporary, APP_VERSION: data.common.version, TAG: data.common.tag,
      SOURCE_COMMIT: data.common.commit, REPO: data.common.repo, GITHUB_RUN_ID: data.common.runId,
      TARGET: data.target, TARGETS: data.target, ARTIFACT_PATHS: JSON.stringify(data.names.map(name => path.join(dist, name)))};
    const script = fileURLToPath(new URL('../scripts/release-assets.mjs', import.meta.url));
    const run = (mode, changes = {}) => spawnSync(process.execPath, [script, mode], {cwd: temporary, encoding: 'utf8', env: {...env, ...changes}});
    assert.equal(run('record').status, 0);
    fs.writeFileSync(path.join(dist, 'SHA256SUMS'), 'checksum from a previous attempt');
    assert.equal(run('verify').status, 0);
    assert.equal(fs.existsSync(path.join(dist, 'SHA256SUMS')), false, 'verification discards only its regenerated checksum output');
    const proof = path.join(temporary, 'release-evidence', data.target + '.json');
    const original = fs.readFileSync(proof, 'utf8');
    assert.notEqual(run('record', {TAG: 'v9.9.9'}).status, 0);
    assert.equal(fs.readFileSync(proof, 'utf8'), original);
    fs.writeFileSync(path.join(dist, 'stale.zip'), 'previous run');
    assert.notEqual(run('verify').status, 0);
  } finally { fs.rmSync(temporary, {recursive: true, force: true}); }
});

test('Windows, macOS app directories and Linux evidence merge into one complete feed', async () => {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'release-platforms-'));
  assert.equal(path.dirname(temporary), path.resolve(os.tmpdir()));
  try {
    const directory = path.join(temporary, 'dist');
    fs.mkdirSync(directory);
    const common = {version: '1.2.3', tag: 'v1.2.3', repo: 'org/app', commit: 'a'.repeat(40), runId: '123'};
    const targets = ['x86_64-pc-windows-msvc', 'aarch64-apple-darwin', 'aarch64-unknown-linux-gnu'];
    const names = ['Demo_1.2.3_x64-setup.exe', 'Demo_1.2.3_aarch64.app.tar.gz', 'Demo_1.2.3_arm64.AppImage'];
    const keys = ['windows-x86_64', 'darwin-aarch64', 'linux-aarch64'];
    const assets = [], platforms = {}, paths = [];
    for (const [index, name] of names.entries()) {
      const local = path.join(temporary, name);
      const signature = `signature-${index}`;
      fs.writeFileSync(local, `payload-${index}`);
      fs.writeFileSync(local + '.sig', signature);
      for (const file of [local, local + '.sig']) {
        const name = path.basename(file);
        fs.copyFileSync(file, path.join(directory, name));
        assets.push({id: assets.length + 1, name, digest: 'sha256:' + await hashFile(file)});
      }
      platforms[keys[index]] = {url: `https://github.com/org/app/releases/download/v1.2.3/${name}`, signature};
      if (index === 1) {
        fs.mkdirSync(local.slice(0, -7)); // artifactPaths can contain the .app directory.
        paths.push([local.slice(0, -7), local + '.sig']);
      } else paths.push([local, local + '.sig']);
    }
    const feed = {version: common.version, platforms};
    fs.writeFileSync(path.join(directory, 'latest.json'), JSON.stringify(feed));
    const evidence = [];
    for (const [index, target] of targets.entries()) evidence.push(await recordEvidence({...common, target, assets, feed, paths: paths[index]}));
    await verifyEvidence({...common, targets, assets, evidence, directory});
    await assert.rejects(verifyEvidence({...common, targets, assets, evidence: evidence.slice(1), directory}), /Missing/);
  } finally { fs.rmSync(temporary, {recursive: true, force: true}); }
});
