// Copy with the release workflow to .github/scripts/release-assets.mjs.
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const safeName = name => typeof name === 'string' && name !== '.' && name !== '..' && /^[A-Za-z0-9._-]+$/.test(name);
const requireValue = (condition, message) => { if (!condition) throw new Error(message); };
const platformForTarget = target => {
  const [cpu, , os] = target.split('-');
  requireValue(['x86_64', 'aarch64'].includes(cpu) && ['windows', 'darwin', 'linux'].includes(os), 'Unsupported build target');
  return ("" + (os) + "-" + (cpu));
};
export async function hashFile(file) {
  const hash = createHash('sha256');
  for await (const chunk of fs.createReadStream(file)) hash.update(chunk);
  return hash.digest('hex');
}

// Shared by direct-release verification and central winget consumers. No network writes.
export function releaseReady(release, {tag, requiredAssets, allowPrerelease = false, expectedDraft = false}) {
  requireValue(release.tag_name === tag && release.draft === expectedDraft && (allowPrerelease || release.prerelease === false) &&
    (allowPrerelease || /^v\d+\.\d+\.\d+$/.test(tag)), expectedDraft ? 'Expected an unpublished draft release' : 'Expected the public stable release');
  requireValue(Array.isArray(requiredAssets) && requiredAssets.length > 0, 'Required asset inventory is empty');
  const assets = release.assets ?? [];
  requireValue(new Set(assets.map(asset => asset.name)).size === assets.length, 'Duplicate release asset');
  for (const name of requiredAssets) {
    requireValue(safeName(name), 'Unsafe required asset name');
    const asset = assets.find(asset => asset.name === name);
    requireValue(asset && /^sha256:[a-f0-9]{64}$/i.test(asset.digest ?? ''), ("Missing required asset or digest: " + (name)));
  }
  return assets;
}

async function verifyReleaseAssets({directory, release, requiredAssets, platforms, version, repo, tag}, expectedDraft) {
  requireValue(tag === ("v" + (version)), 'Tag and app version mismatch');
  requireValue(release.prerelease === version.includes('-'), 'Release channel mismatch');
  const assets = releaseReady(release, {tag, requiredAssets, allowPrerelease: version.includes('-'), expectedDraft});
  const payloads = assets.filter(asset => !/^SHA256SUMS(?:\.txt)?$/.test(asset.name));
  requireValue(payloads.length > 0, 'No release payloads');
  const names = new Set();
  for (const asset of payloads) {
    requireValue(safeName(asset.name) && /^sha256:[a-f0-9]{64}$/i.test(asset.digest ?? ''), ("Invalid asset or digest: " + (asset.name)));
    const local = path.join(directory, asset.name);
    requireValue(fs.existsSync(local) && fs.lstatSync(local).isFile(), ("Missing local asset: " + (asset.name)));
    requireValue(await hashFile(local) === asset.digest.slice(7).toLowerCase(), ("Release digest mismatch: " + (asset.name)));
    names.add(asset.name);
  }
  const feed = readJson(path.join(directory, 'latest.json'));
  requireValue(Array.isArray(platforms) && platforms.length > 0, 'Required updater platforms are empty');
  for (const platform of platforms) requireValue(feed.platforms?.[platform], ("Missing updater target: " + (platform)));
  const signatures = new Map([...names].filter(name => name.endsWith('.sig')).map(name => [name, fs.readFileSync(path.join(directory, name), 'utf8')]));
  verifyFeed(feed, {version, repo, tag, assets, files: names, signatures, preferNsis: true});
  // The checksum from a previous run is deliberately excluded from its replacement.
  return payloads.sort((a, b) => a.name.localeCompare(b.name, 'en')).map(asset => ("" + (asset.digest.slice(7).toLowerCase()) + "  " + (asset.name) + "\n")).join('');
}

export const verifyPublicRelease = options => verifyReleaseAssets(options, false);
export const verifyDraftRelease = options => verifyReleaseAssets(options, true);

export function resolveAsset(url, {repo, tag, assets}) {
  const parsed = new URL(url);
  requireValue(parsed.protocol === 'https:' && !parsed.port && !parsed.username && !parsed.password, 'Invalid asset URL');
  const apiPrefix = ("/repos/" + (repo) + "/releases/assets/");
  if (parsed.hostname === 'api.github.com' && parsed.pathname.startsWith(apiPrefix)) {
    const id = parsed.pathname.slice(apiPrefix.length);
    requireValue(/^\d+$/.test(id), 'Invalid asset ID');
    const found = assets.filter(asset => String(asset.id) === id);
    requireValue(found.length === 1, 'Asset ID does not belong to this draft');
    requireValue(safeName(found[0].name), 'Unsafe asset name');
    return found[0].name;
  }
  const prefix = ("/" + (repo) + "/releases/download/" + (tag) + "/");
  requireValue(parsed.hostname === 'github.com' && parsed.pathname.startsWith(prefix), 'Unexpected asset repository or tag');
  const name = decodeURIComponent(parsed.pathname.slice(prefix.length));
  requireValue(safeName(name) && assets.some(asset => asset.name === name), 'Unknown draft asset');
  return name;
}

export function verifyFeed(feed, {version, repo, tag, assets, files, signatures, preferNsis = false}) {
  requireValue(feed.version === version && feed.platforms && typeof feed.platforms === 'object' && Object.keys(feed.platforms).length > 0, 'Updater version or platforms mismatch');
  for (const [platform, entry] of Object.entries(feed.platforms)) {
    const match = /^(windows|darwin|linux)-(x86_64|aarch64)(?:-(nsis|msi|app|appimage|deb|rpm))?$/.exec(platform);
    requireValue(match, ("Unknown updater platform " + (platform)));
    const name = resolveAsset(entry.url, {repo, tag, assets});
    requireValue(files.has(name), ("" + (platform) + " references an unbuilt asset " + (name)));
    const arch = match[2] === 'aarch64' ? /(^|[-_.])(arm64|aarch64)([-_.]|$)/i : /(^|[-_.])(amd64|x64|x86_64)([-_.]|$)/i;
    requireValue(arch.test(name), ("" + (platform) + " architecture mismatch"));
    const types = {windows: /(?:[-_]setup\.exe|\.nsis\.zip|\.msi(?:\.zip)?)$/i,
      darwin: /\.app\.tar\.gz$/i, linux: /\.AppImage(?:\.tar\.gz)?$/i};
    const bundles = {nsis: /(?:[-_]setup\.exe|\.nsis\.zip)$/i, msi: /\.msi(?:\.zip)?$/i,
      app: /\.app\.tar\.gz$/i, appimage: /\.AppImage(?:\.tar\.gz)?$/i, deb: /\.deb$/i, rpm: /\.rpm$/i};
    requireValue((match[3] ? bundles[match[3]] : types[match[1]]).test(name), ("" + (platform) + " artifact type mismatch"));
    if (preferNsis && match[1] === 'windows' && !match[3]) requireValue(bundles.nsis.test(name), ("" + (platform) + " must use NSIS"));
    requireValue(!match[3] || ({windows: ['nsis', 'msi'], darwin: ['app'], linux: ['appimage', 'deb', 'rpm']})[match[1]].includes(match[3]), ("" + (platform) + " bundle mismatch"));
    requireValue(files.has(name + '.sig') && typeof entry.signature === 'string' && entry.signature.trim() &&
      signatures.get(name + '.sig')?.trim() === entry.signature.trim(), ("" + (platform) + " signature mismatch"));
  }
}

export async function recordEvidence({paths, assets, feed, version, repo, tag, commit, runId, target, preferNsis = false}) {
  requireValue(tag === ("v" + (version)), 'Tag and built app version mismatch');
  const files = [];
  const signatures = new Map();
  const localPaths = new Set(paths.map(file => fs.statSync(file).isDirectory() && file.endsWith('.app') ? file + '.tar.gz' : file));
  for (const file of localPaths) {
    requireValue(fs.statSync(file).isFile(), ("Artifact is not a file: " + (file)));
    const sha256 = await hashFile(file);
    const matches = assets.filter(asset => asset.digest === ("sha256:" + (sha256)));
    requireValue(matches.length === 1 && safeName(matches[0].name), ("Built artifact has no unique matching draft digest: " + (file)));
    const name = matches[0].name;
    requireValue(!files.some(entry => entry.name === name), ("Duplicate artifact " + (name)));
    files.push({name, sha256});
    if (name.endsWith('.sig')) signatures.set(name, fs.readFileSync(file, 'utf8'));
  }
  requireValue(files.length > 0, 'No build artifacts');
  const names = new Set(files.map(file => file.name));
  const platforms = Object.fromEntries(Object.entries(feed.platforms ?? {}).filter(([, entry]) => names.has(resolveAsset(entry.url, {repo, tag, assets}))));
  verifyFeed({...feed, platforms}, {version, repo, tag, assets, files: names, signatures, preferNsis});
  const platform = platformForTarget(target);
  requireValue(platforms[platform], ("Build evidence missing " + (platform)));
  return {version, tag, repo, commit, runId, target, files, platforms};
}

export async function verifyEvidence({directory, evidence, targets, version, repo, tag, commit, runId, assets, preferNsis = false}) {
  requireValue(evidence.length === targets.length && new Set(evidence.map(item => item.target)).size === targets.length, 'Missing or duplicate target evidence');
  const expected = new Map();
  const platforms = {};
  for (const item of evidence) {
    requireValue(targets.includes(item.target) && item.version === version && item.tag === tag && item.repo === repo &&
      item.commit === commit && String(item.runId) === String(runId), 'Evidence source or version mismatch');
    requireValue(item.files.length > 0 && item.platforms[platformForTarget(item.target)], 'Incomplete target evidence');
    for (const file of item.files) {
      requireValue(safeName(file.name) && /^[a-f0-9]{64}$/.test(file.sha256), 'Invalid evidence file');
      requireValue(!expected.has(file.name), ("Duplicate build asset " + (file.name)));
      expected.set(file.name, file.sha256);
    }
    for (const [key, entry] of Object.entries(item.platforms)) {
      requireValue(!platforms[key], ("Duplicate updater platform " + (key)));
      platforms[key] = entry;
    }
  }
  const actual = fs.readdirSync(directory).sort();
  requireValue(JSON.stringify(actual) === JSON.stringify([...expected.keys(), 'latest.json'].sort()), 'Draft asset set differs from this build');
  for (const [name, sha256] of expected) requireValue(await hashFile(path.join(directory, name)) === sha256, ("Draft digest mismatch: " + (name)));
  const feed = readJson(path.join(directory, 'latest.json'));
  requireValue(JSON.stringify(Object.keys(feed.platforms).sort()) === JSON.stringify(Object.keys(platforms).sort()), 'Updater platform set differs from build evidence');
  for (const [key, entry] of Object.entries(platforms)) requireValue(JSON.stringify(feed.platforms[key]) === JSON.stringify(entry), ("Updater entry changed: " + (key)));
  const signatures = new Map([...expected.keys()].filter(name => name.endsWith('.sig')).map(name => [name, fs.readFileSync(path.join(directory, name), 'utf8')]));
  verifyFeed(feed, {version, repo, tag, assets, files: new Set(expected.keys()), signatures, preferNsis});
}

async function main() {
  const env = process.env;
  if (process.argv[2] === 'ready') {
    const contract = readJson(process.argv[4]);
    releaseReady(readJson(process.argv[3]), {tag: contract.tag, requiredAssets: contract.requiredAssets});
    return;
  }
  if (['verify-release', 'verify-draft'].includes(process.argv[2])) {
    const verify = process.argv[2] === 'verify-draft' ? verifyDraftRelease : verifyPublicRelease;
    const checksums = await verify({directory: 'dist', release: readJson(path.join(env.RUNNER_TEMP, 'release.json')),
      requiredAssets: ['latest.json'], platforms: env.PLATFORMS?.split(' '), version: env.APP_VERSION, repo: env.REPO, tag: env.TAG});
    fs.writeFileSync('dist/SHA256SUMS', checksums);
    return;
  }
  const common = {version: env.APP_VERSION, tag: env.TAG, repo: env.REPO, commit: env.SOURCE_COMMIT, runId: env.GITHUB_RUN_ID, preferNsis: env.PREFER_NSIS === 'true'};
  requireValue(/^[a-f0-9]{40}$/i.test(common.commit ?? '') && /^\d+$/.test(common.runId ?? ''), 'Missing build source identity');
  const assets = readJson(path.join(env.RUNNER_TEMP, 'draft-assets.json')).flat();
  if (process.argv[2] === 'record') {
    const evidence = await recordEvidence({...common, assets, paths: [...JSON.parse(env.ARTIFACT_PATHS), ...JSON.parse(env.EXTRA_ARTIFACTS || '[]')],
      target: env.TARGET, feed: readJson(path.join(env.RUNNER_TEMP, 'build-feed.json'))});
    requireValue(safeName(env.TARGET), 'Invalid target');
    fs.mkdirSync('release-evidence', {recursive: true});
    fs.writeFileSync(path.join('release-evidence', env.TARGET + '.json'), JSON.stringify(evidence) + '\n');
  } else if (process.argv[2] === 'verify') {
    // SHA256SUMS is regenerated after verification; it is not a build payload.
    fs.rmSync(path.join('dist', 'SHA256SUMS'), {force: true});
    const evidence = fs.readdirSync('release-evidence').filter(file => file.endsWith('.json')).map(file => readJson(path.join('release-evidence', file)));
    await verifyEvidence({...common, assets, directory: 'dist', evidence, targets: env.TARGETS.split(' ')});
  } else throw new Error('Usage: release-assets.mjs record|verify');
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch(error => { console.error(("release-assets: " + (error.message))); process.exitCode = 1; });
}
