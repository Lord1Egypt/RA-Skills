#!/usr/bin/env node
// Read-only fact collector for Tauri / Electron apps.
// Never installs dependencies, runs project scripts, writes into the project, commits, tags or publishes.
import fs from 'node:fs';
import { deliveryFindings } from './delivery-checks.mjs';
import path from 'node:path';
import { TOOL_VERSION, exact, compare, stableMax, walk, read, cargoPackages, workflowHints, usageHints, requestJson, releaseHistory,
  LOCKFILES, parseYarnLock, parsePnpmLock, parseBunLock, resolveFromLock, electronSupportedMajors, nodeSupportFacts, classifyNotes,
  changelogSections, refVersion, WRITE_CAPABLE_ACTIONS, macTargetsFromBuilder, macTargetsFromArgs, parseJson5 } from './core.mjs';
import { runTraps, defaultContext, stripComments, TRAPS, workflowCoverage } from './ci-traps.mjs';
import { discoverApplications, workflowApplications } from './app-context.mjs';
import { parseTfms, parseGlobalJson, normalizeMetadata, analyzeDotnet, metadataUrl, tfmInfo, sdkParts } from './dotnet.mjs';

const USAGE = `Usage: node audit.mjs <project-dir> [--offline] [--ci-only] [--dotnet] [--json] [--pages 1..10] [--out <report.json>] [--since-baseline <review.json>]
  --ci-only   CI & release checks using local stack/lockfile context, without framework release lookups
  --dotnet    .NET runtime/SDK audit (TFM support/EOL, global.json pin/rollForward) + CI checks
Read-only. --out writes only the named JSON report (refuses to overwrite). Exit: 0 complete within bounds, 2 incomplete/offline, other = failure.`;
const args = process.argv.slice(2);
if (args.includes('--help') || !args.length) { console.log(USAGE); process.exit(0); }
// User-input failures print one line, like every other CLI in this repo. A raw stack
// (absolute path + source line) reads like a crash in the audit itself.
const die = msg => { console.error(`desktop-app-standard: ${msg}`); process.exit(1); };
let root = null, offline = false, json = false, ciOnly = false, dotnet = false, out = null, baselinePath = null, pages = 3;
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === '--offline') offline = true;
  else if (a === '--json') json = true;
  else if (a === '--ci-only') ciOnly = true;
  else if (a === '--dotnet') dotnet = true;
  else if (['--out', '--since-baseline', '--pages'].includes(a)) {
    const v = args[++i]; if (!v || v.startsWith('--')) die(`缺少参数 ${a}`);
    if (a === '--out') out = path.resolve(v); else if (a === '--since-baseline') baselinePath = path.resolve(v); else pages = Number(v);
  } else if (!a.startsWith('-') && !root) root = path.resolve(a);
  else die(`未知参数: ${a}`);
}
if (!root) die('缺少 <project-dir>');
let rootStat = null;
try { rootStat = fs.statSync(root); } catch { /* reported below */ }
if (!rootStat || !rootStat.isDirectory()) die(`项目路径不是目录: ${root}`);
if (!Number.isInteger(pages) || pages < 1 || pages > 10) die('--pages 必须是 1..10 的整数');

const auditFrameworks = !ciOnly && !dotnet;
const checkedAt = new Date().toISOString();
const report = { schemaVersion: 3, toolVersion: TOOL_VERSION, checkedAt, project: root, mode: offline ? 'offline' : 'online', ciOnly, dotnetRequested: dotnet,
  collectionComplete: !offline, errors: [], warnings: [], inventory: [], packageManager: null, upstream: [], electronSupport: null,
  nodeSupport: null, nodePins: [], compatibility: [], frameworkFindings: [], changes: [], actions: [], ciFindings: [], dotnet: null,
  notes: ['此脚本只读。升级任务继续按 references/upgrade-dependencies.md 修改目标仓库并验证。P0/P1 候选需核对文件与上游证据。'] };
const incomplete = msg => { report.collectionComplete = false; if (msg) report.warnings.push(msg); };

// ---------------- scan ----------------
let scan;
try { scan = walk(root); } catch (e) { die(`无法读取项目目录: ${e.message.split('\n')[0]}`); }
report.scan = { fileCount: scan.files.length, limited: scan.limited, skipped: scan.skipped, excluded: scan.excluded, ciMethod: 'comment-stripped line heuristics, not a YAML parser' };
if (scan.limited) incomplete('扫描命中文件/深度上限，请按应用子目录分别运行。');
// A skipped directory is an unscanned subtree: symlinks are skipped to avoid loops,
// and an unreadable directory cannot be enumerated. Either way "complete" would be a
// claim the run cannot support.
if (scan.skipped.length)
  incomplete(`扫描跳过了 ${scan.skipped.length} 个目录/符号链接，这些子树未被审计：${scan.skipped.slice(0, 5).join('; ')}${scan.skipped.length > 5 ? '; …' : ''}`);
const texts = new Map();
function text(file) {
  if (!texts.has(file)) {
    try { const t = read(root, file); texts.set(file, t); if (t === null) incomplete(`${file}: 超过 4 MB，未读取`); }
    catch { texts.set(file, null); report.collectionComplete = false; report.errors.push({ scope: file, message: '文件读取失败' }); }
  }
  return texts.get(file);
}
function parseJson(file) {
  try { return JSON.parse(text(file)); }
  catch { report.collectionComplete = false; report.errors.push({ scope: file, message: 'JSON 解析失败' }); return null; }
}
const dirOf = f => path.posix.dirname(f);

// ---------------- lockfiles ----------------
const locks = new Map(); // dir -> { kind, file, data, flavor }
for (const file of scan.files.filter(f => LOCKFILES.includes(path.posix.basename(f)))) {
  const dir = dirOf(file), base = path.posix.basename(file);
  if (locks.has(dir) && base !== 'bun.lockb') report.warnings.push(`${dir}: 存在多个锁文件（${locks.get(dir).file} 与 ${file}），house style 要求单一锁文件。`);
  if (locks.has(dir)) continue;
  try {
    if (base === 'package-lock.json' || base === 'npm-shrinkwrap.json') locks.set(dir, { kind: 'npm', file, data: JSON.parse(text(file)) });
    else if (base === 'yarn.lock') { const data = parseYarnLock(text(file) ?? ''); locks.set(dir, { kind: 'yarn', file, data, flavor: data.flavor }); }
    else if (base === 'pnpm-lock.yaml') locks.set(dir, { kind: 'pnpm', file, data: parsePnpmLock(text(file) ?? '') });
    else if (base === 'bun.lock') locks.set(dir, { kind: 'bun', file, data: parseBunLock(text(file) ?? '') });
    else locks.set(dir, { kind: 'bun-binary', file, data: null });
  } catch { report.errors.push({ scope: file, message: '锁文件解析失败' }); report.collectionComplete = false; }
}
const governingLock = dir => { let d = dir; for (;;) { if (locks.has(d)) return { dir: d, ...locks.get(d) }; if (d === '.') return null; d = dirOf(d); } };
const lockfileKinds = {}; for (const l of locks.values()) lockfileKinds[l.kind === 'bun-binary' ? 'bun' : l.kind] = true;

// ---------------- npm inventory ----------------
const npmMatch = n => /^(electron|electron-builder|electron-updater)$/.test(n) || n.startsWith('@electron-forge/') || /^@tauri-apps\/(?:api|cli|plugin-[\w-]+)$/.test(n);
let enginesNode = null;
const rootPkg = scan.files.includes('package.json') ? parseJson('package.json') : null;
if (rootPkg?.packageManager) report.packageManager = rootPkg.packageManager;
// electron-builder copies the app manifest into the packaged output
// (<out>/<platform>-unpacked/resources/app/package.json). That copy is a build
// artifact, not a source manifest: it resolves against the root lockfile, so it
// only ever duplicates an inventory row — and if it names a dependency the
// lockfile cannot resolve, it would mark the whole collection incomplete
// (exit code 2) for a file nobody edits.
const builderManifestTargets = new Map();
const npmManifests = new Map();
const isPackagedAppManifest = f => /(^|\/)resources\/app\/package\.json$/.test(f);
for (const file of scan.files.filter(f => /(^|\/)package\.json$/.test(f) && !isPackagedAppManifest(f))) {
  const data = file === 'package.json' ? rootPkg : parseJson(file); if (!data) continue;
  npmManifests.set(file, data);
  const macTarget = data.build?.mac?.target;
  if (macTarget) {
    const targets = [macTarget].flat().map(entry => typeof entry === 'string' ? entry : entry?.target).filter(Boolean);
    if (targets.length) builderManifestTargets.set(file, targets);
  }
  if (!enginesNode && data.engines?.node) enginesNode = data.engines.node;
  const dir = dirOf(file);
  for (const [name, declared] of Object.entries({ ...data.dependencies, ...data.devDependencies, ...data.optionalDependencies })) {
    if (!npmMatch(name)) continue;
    const lock = governingLock(dir);
    let res = { version: null, locator: null, candidates: [] };
    if (lock?.kind === 'npm') {
      const rel = lock.dir === '.' ? dir : path.posix.relative(lock.dir, dir);
      const parts = rel === '.' ? [] : rel.split('/').filter(Boolean), keys = [];
      for (let n = parts.length; n >= 0; n--) keys.push((n ? parts.slice(0, n).join('/') + '/' : '') + 'node_modules/' + name);
      const key = keys.find(k => lock.data?.packages?.[k]?.version);
      const v = key ? lock.data.packages[key].version : (!parts.length ? lock.data?.dependencies?.[name]?.version : null);
      res = { version: v ?? null, locator: key ?? (v ? `dependencies.${name}` : null), candidates: v ? [v] : [] };
    } else if (lock && lock.kind !== 'bun-binary') {
      res = resolveFromLock(lock.kind, lock.data, { name, declared, importerPath: lock.dir === dir ? '.' : path.posix.relative(lock.dir, dir) });
    }
    const resolved = exact(res.version);
    report.inventory.push({ ecosystem: 'npm', name, manifest: file, declared, resolved, lockfile: lock?.file ?? null, lockKind: lock?.kind ?? null,
      locator: res.locator, candidates: res.candidates, status: resolved ? 'lock-resolved' : 'unresolved' });
    if (!resolved && auditFrameworks) incomplete(lock?.kind === 'bun-binary' ? `${file}: ${name} 由二进制 bun.lockb 锁定，脚本无法读取；运行 \`bun pm ls\` 或迁移到文本 bun.lock。`
      : !lock ? `${file}: ${name} 没有锁文件；声明范围 ${declared} 不是已安装版本。`
      : `${file}: ${name} 未能从 ${lock.file} 唯一解析（候选: ${res.candidates.join(', ') || '无'}）；用 \`npm ls ${name}\` / \`yarn why ${name}\` / \`pnpm why ${name}\` 等原生只读命令核验。`);
  }
}
const yarnLock = [...locks.values()].find(l => l.kind === 'yarn');
const yarnFlavor = yarnLock?.flavor ?? (/^yarn@(\d+)/.exec(report.packageManager ?? '')?.[1] ? (Number(/^yarn@(\d+)/.exec(report.packageManager)[1]) >= 2 ? 'berry' : 'classic') : null);
report.packageManagerDetected = { lockfiles: [...locks.values()].map(l => l.file), yarnFlavor, packageManagerField: report.packageManager };
if (yarnFlavor === 'berry' && !report.packageManager) report.warnings.push('yarn berry 锁文件存在，但 package.json 没有 `packageManager` 字段；CI 中 corepack 无法确定 yarn 版本。');

// ---------------- cargo inventory ----------------
const cargoMatch = n => ['tauri', 'tauri-build', 'tauri-cli'].includes(n) || n.startsWith('tauri-plugin-');
for (const file of scan.files.filter(f => /(^|\/)Cargo\.lock$/.test(f)))
  for (const item of cargoPackages(text(file) ?? '')) if (cargoMatch(item.name))
    report.inventory.push({ ecosystem: 'cargo', name: item.name, manifest: file, declared: null, resolved: item.version, lockfile: file, lockKind: 'cargo',
      locator: item.source, candidates: [item.version], status: 'lock-resolved', registry: /crates\.io-index|index\.crates\.io/.test(item.source) });
for (const file of scan.files.filter(f => /(^|\/)Cargo\.toml$/.test(f))) {
  for (const m of (text(file) ?? '').matchAll(/^\s*(tauri(?:-build|-cli|-plugin-[\w-]+)?)\s*=\s*(.+)$/gm)) {
    const covered = report.inventory.some(x => x.ecosystem === 'cargo' && x.name === m[1] && (dirOf(x.manifest) === '.' || dirOf(file) === dirOf(x.manifest) || dirOf(file).startsWith(dirOf(x.manifest) + '/')));
    if (!covered) { report.inventory.push({ ecosystem: 'cargo', name: m[1], manifest: file, declared: m[2].trim(), resolved: null, status: 'unresolved', registry: false });
      if (auditFrameworks) incomplete(`${file}: ${m[1]} 仅发现 TOML 声明；可能由父工作区锁定、重命名或 git/path，需 \`cargo metadata\` 核验。`); }
  }
}

// ---------------- app config facts ----------------
const has = n => report.inventory.some(x => x.name === n || (n.endsWith('*') && x.name.startsWith(n.slice(0, -1))));
const isTauri = has('tauri') || has('@tauri-apps/cli') || scan.files.some(f => /tauri\.conf\.json5?$/.test(f));
const hasElectron = has('electron');
const usesTauriUpdater = has('tauri-plugin-updater') || has('@tauri-apps/plugin-updater');
const tauriConfigs = [];
for (const file of scan.files.filter(f => /(^|\/)tauri\.conf\.json5?$/.test(f))) {
  const raw = text(file) ?? '';
  let conf = null;
  try { conf = JSON.parse(raw); } catch { conf = parseJson5(raw); }
  if (!conf) {
    incomplete(`${file}: 配置读不出来（不是合法 JSON，也不是可读的 JSON5），createUpdaterArtifacts 与 targets 未核验`);
    tauriConfigs.push({ file, unreadable: true });
    continue;
  }
  tauriConfigs.push({ file, createUpdaterArtifacts: conf.bundle?.createUpdaterArtifacts ?? null,
    targets: conf.bundle?.targets ?? 'all', identifier: conf.identifier ?? null });
}
const applications = discoverApplications(tauriConfigs, report.inventory, [...npmManifests.keys()],
  scan.files.filter(file => /(^|\/)Cargo\.toml$/.test(file)).map(file => ({file, text: text(file) ?? ''})));
const multiApplication = applications.length > 1;
const artifactsEnabled = config => config && !config.unreadable
  ? config.createUpdaterArtifacts === true || config.createUpdaterArtifacts === 'v1Compatible' : null;
const bothBundles = config => config?.targets === 'all' ||
  (Array.isArray(config?.targets) && config.targets.includes('msi') && config.targets.includes('nsis'));
// Preserve the existing single-config field. Multiple configs live in applications.
if (tauriConfigs.length === 1 && !tauriConfigs[0].unreadable) report.tauriConfig = tauriConfigs[0];
const tauriCreateUpdaterArtifacts = tauriConfigs.length === 1 ? artifactsEnabled(tauriConfigs[0]) : null;
const tauriBothWindowsBundles = tauriConfigs.length === 1 && bothBundles(tauriConfigs[0]);
report.applications = applications.map(app => ({ directory: app.directory,
  frameworks: [app.isTauri && 'tauri', app.hasElectron && 'electron'].filter(Boolean),
  manifests: [...new Set(app.inventory.map(item => item.manifest))], tauriConfigs: app.tauriConfigs }));
if (!applications.length && isTauri && usesTauriUpdater) incomplete('使用了 Tauri updater，但没有找到 tauri.conf.json/json5；createUpdaterArtifacts 未核验');
for (const app of applications) {
  if (app.isTauri && app.usesTauriUpdater && !app.tauriConfigs.length)
    incomplete(`${app.directory}: 使用了 Tauri updater，但没有找到 tauri.conf.json/json5；createUpdaterArtifacts 未核验`);
  if (app.tauriConfigs.length > 1)
    incomplete(`${app.directory}: 多个 Tauri 基础配置，无法确定实际生效文件；按应用子目录和实际配置核验`);
}
const electronMajor = (() => { const v = report.inventory.find(x => x.name === 'electron' && x.resolved)?.resolved; return v ? Number(v.split('.')[0]) : null; })();
let platforms = ['windows', 'macos', 'linux'];
const policyNotes = [], acceptedRules = new Map();
const osOf = list => [...new Set(list.map(p => String(p).split('-')[0].replace(/^win$/, 'windows').replace(/^mac$|^darwin$/, 'macos')))];
if (scan.files.includes('.desktop-policy.json')) {
  const pol = parseJson('.desktop-policy.json');
  // House style is the default; only a documented deviation (reason + revisitWhen) narrows it.
  const dev = Array.isArray(pol?.deviations) ? pol.deviations.find(d => d?.rule === 'platforms' && Array.isArray(d.value)) : null;
  const documented = d => [d.reason, d.revisitWhen].every(v => typeof v === 'string' && v.trim().length > 0);
  if (dev && documented(dev)) { platforms = osOf(dev.value); report.policyPlatforms = dev.value; report.policyDeviation = { reason: dev.reason, revisitWhen: dev.revisitWhen }; }
  else if (dev) policyNotes.push({ id: 'policy-deviation-undocumented', severity: 'P2', file: '.desktop-policy.json', line: null, confidence: 'confirmed',
    detail: '`.desktop-policy.json` 缩小了平台范围，但缺少 reason 或 revisitWhen；按 house style 仍以 Windows/macOS/Linux 全平台为准。', fix: '补齐 reason 与 revisitWhen（日期或触发条件），或删除该偏离。' });
  else if (Array.isArray(pol?.platforms)) {
    const requestedPlatforms = osOf(pol.platforms);
    report.policyPlatforms = pol.platforms;
    const missing = ['windows', 'macos', 'linux'].filter(p => !requestedPlatforms.includes(p));
    if (missing.length)
      policyNotes.push({ id: 'policy-deviation-undocumented', severity: 'P2', file: '.desktop-policy.json', line: null, confidence: 'confirmed',
        detail: `\`.desktop-policy.json\` 的 platforms 缩小到 ${requestedPlatforms.join('/')}（缺少 ${missing.join('/')}），但没有 \`deviations\` 里带 reason/revisitWhen 的 platforms 条目；仍按 Windows/macOS/Linux 全平台审计。`,
        fix: '在 deviations 中加 { "rule": "platforms", "value": [...], "reason": "...", "revisitWhen": "..." }，或恢复全平台。' });
  }
  // Any other deviation names a finding id: documented ones turn that finding into "accepted", undocumented ones are drift.
  for (const d of Array.isArray(pol?.deviations) ? pol.deviations : []) {
    if (!d?.rule || d.rule === 'platforms') continue;
    if (documented(d)) acceptedRules.set(d.rule, { reason: d.reason, revisitWhen: d.revisitWhen });
    else policyNotes.push({ id: 'policy-deviation-undocumented', severity: 'P2', file: '.desktop-policy.json', line: null, confidence: 'confirmed',
      detail: `\`.desktop-policy.json\` 偏离 \`${d.rule}\` 缺少 reason 或 revisitWhen，不予接受；该发现照常报告。`, fix: '补齐 reason 与 revisitWhen（日期或触发条件），或删除该偏离。' });
  }
}
// ---------------- workflows ----------------
const workflowFiles = scan.files.filter(f => /^\.github\/workflows\/[^/]+\.ya?ml$/.test(f));
const actionsLock = scan.files.includes('.github/workflows/actions.lock');
for (const file of workflowFiles) report.actions.push(...workflowHints(file, text(file) ?? '', actionsLock).actions);
const ctx = defaultContext({ isTauri, hasElectron, hasElectronUpdater: has('electron-updater'), usesTauriUpdater, tauriCreateUpdaterArtifacts,
  tauriBothWindowsBundles, electronMajor, lockfiles: lockfileKinds, packageManager: report.packageManager ?? (yarnFlavor ? `yarn (${yarnFlavor})` : null), yarnFlavor, enginesNode, platforms });
const trapError = ({ file, id, error }) => incomplete(`${file}: 陷阱 ${id} 执行失败（${error?.message ?? error}）；该检查未完成`);
const applicationRuleIds = new Set(['tauri-updater-manifest', 'updater-json-prefer-nsis', 'electron-updater-manifest',
  'electron-updater-windows-target', 'electron-runtime-download', 'electron-builder-empty-csc-link',
  'electron-mac-multiarch-split', 'electron-publish-never', 'cache-lockfile-mismatch', 'npm-ci-without-lockfile',
  'npm-install-not-ci', 'yarn-install-not-frozen', 'yarn-berry-corepack', 'node-version-vs-engines',
  'rust-cache-workspace', 'tauri-linux-deps', 'tauri-macos-rust-targets']);
const workflowScopes = multiApplication ? workflowFiles.flatMap(file => workflowApplications(file, text(file) ?? '', applications, scan.files)) : [];
for (const file of workflowFiles) {
  const scoped = multiApplication && workflowScopes.some(scope => scope.file === file);
  report.ciFindings.push(...runTraps([{file, text: text(file) ?? ''}], ctx, trapError,
    scoped ? TRAPS.filter(rule => !applicationRuleIds.has(rule.id)) : TRAPS));
}
if (multiApplication) {
  report.workflowScopes = workflowScopes.map(({ text, ...scope }) => scope);
  for (const scope of workflowScopes) {
    if (scope.reason) { incomplete(`${scope.file}:${scope.line} (${scope.job}): ${scope.reason}，应用配置检查未完成；按应用子目录重跑并人工核对 workflow`); continue; }
    const app = applications.find(app => app.directory === scope.application);
    const localLock = governingLock(app.directory);
    const localPkgFile = path.posix.join(app.directory, 'package.json');
    const localPkg = scan.files.includes(localPkgFile) ? parseJson(localPkgFile) : null;
    const config = app.tauriConfigs.length === 1 ? app.tauriConfigs[0] : null;
    const context = defaultContext({ ...ctx, ...app, tauriCreateUpdaterArtifacts: artifactsEnabled(config),
      tauriBothWindowsBundles: bothBundles(config),
      electronMajor: Number(app.inventory.find(item => item.name === 'electron' && item.resolved)?.resolved?.split('.')[0]) || null,
      lockfiles: localLock ? { [localLock.kind]: true } : {}, packageManager: localPkg?.packageManager ?? null,
      yarnFlavor: localLock?.flavor ?? null, enginesNode: localPkg?.engines?.node ?? null });
    const findings = runTraps([{ file: scope.file, text: scope.text }], context, trapError,
      TRAPS.filter(rule => applicationRuleIds.has(rule.id)));
    for (const finding of findings) {
      if (!report.ciFindings.some(existing => existing.id === finding.id && existing.file === finding.file &&
          existing.line === finding.line && existing.application === app.directory))
        report.ciFindings.push({ ...finding, application: app.directory });
    }
  }
}
if (!workflowFiles.length) report.warnings.push('没有 .github/workflows；新项目可从 templates/ 生成 ci/release。');
report.workflowCoverage = workflowCoverage(workflowFiles.map(file => ({file, text: text(file) ?? ''})));
if (isTauri || hasElectron || dotnet) {
  const coverage = report.workflowCoverage;
  if (coverage.delegated.length) report.warnings.push('存在 reusable workflow 或发布脚本委托；追踪其实现、权限与发布路径后再确认覆盖范围。');
  for (const [kind, evidence] of [['pull-request', coverage.pullRequest], ['release', coverage.release]]) {
    if (evidence.length || coverage.delegated.length || (kind === 'release' && coverage.manual.length)) continue;
    report.ciFindings.push({id: `workflow-${kind}-missing`, severity: 'P2', confidence: 'heuristic',
      file: '.github/workflows', line: null,
      detail: kind === 'release' ? '未发现 GitHub Release 构建或上传入口；需确认项目的实际分发渠道。' : '未发现 pull_request 检查入口。',
      fix: kind === 'release' ? 'GitHub Releases 项目适配对应栈的发布模板；商店、内部或手动渠道记录现有交付方法和验收证据。' : '按现有构建与测试命令配置 PR 检查，并核对受保护分支的 required checks。'});
  }
}
report.ciFindings.push(...policyNotes);
report.ciFindings.push(...deliveryFindings(scan.files
  .filter(file => /\.cs$|\.iss$|(?:release|publish)[^/]*\.(?:[cm]?js|ps1)$|(?:^|\/)package\.json$|electron-builder\.(?:json5?|ya?ml)$/.test(file))
  .map(file => ({file, text: text(file) ?? ''}))));

// ---------------- Node toolchain pins ----------------
const nodePins = [], nodePinSeen = new Set();
const lineAt = (t, i) => t.slice(0, i).split('\n').length;
const addNodePin = p => { const k = `${p.kind}:${p.file}:${p.line}:${p.major}`; if (!nodePinSeen.has(k)) { nodePinSeen.add(k); nodePins.push(p); } };
const majorOf = t => /^\s*v?(\d+)/m.exec(t ?? '')?.[1] ?? null;
for (const file of workflowFiles) {
  const t = stripComments(text(file) ?? '');
  for (const m of t.matchAll(/(?:^[\t ]*|[{,]\s*)node-version:\s*['"]?(\d+)/gm))
    addNodePin({ file, line: lineAt(t, m.index), major: Number(m[1]), kind: 'workflow' });
  for (const m of t.matchAll(/(?:^[\t ]*|[{,]\s*)node-version-file:\s*['"]?([^\s'"}]+)/gm)) {
    const ref = m[1].replace(/^\.\//, '');
    if (!scan.files.includes(ref)) { report.warnings.push(`${file}:${lineAt(t, m.index)} node-version-file 指向 ${ref}，扫描中不存在；该 pin 未核验。`); continue; }
    const major = majorOf(text(ref));
    if (major) addNodePin({ file, line: lineAt(t, m.index), major: Number(major), kind: 'workflow-file', versionFile: ref });
    else report.warnings.push(`${file}:${lineAt(t, m.index)} node-version-file ${ref} 无法解析出 Node major；该 pin 未核验。`);
  }
  const dynamic = [...new Set([...t.matchAll(/(?:^[\t ]*|[{,]\s*)node-version:\s*([^\s,}\n]+)/gm)].map(m => m[1].replace(/^['"]|['"]$/g, '')).filter(v => !/^\d+$/.test(v)))];
  if (dynamic.length) report.warnings.push(`${file}: node-version ${dynamic.join('/')} 不是可解析的数字（矩阵或表达式？）；该 pin 未核验。`);
}
for (const file of ['.nvmrc', '.node-version'].filter(f => scan.files.includes(f))) {
  const major = majorOf(text(file));
  if (major) addNodePin({ file, line: 1, major: Number(major), kind: 'file' });
  else if ((text(file) ?? '').trim()) report.warnings.push(`${file} 无法解析出 Node major（可能是 lts/*）；该 pin 未核验。`);
}
report.nodePins = nodePins;

// ---------------- macOS updater artifact (Electron) ----------------
// The macOS updater needs a **zip** artifact. electron-updater's MacUpdater only
// accepts a zip: findFile(files, "zip", ["pkg","dmg"]) treats pkg/dmg as an
// EXCLUSION list, not a fallback, so a dmg-only build makes the manifest point at
// a .dmg and every "check for update" throws ERR_UPDATER_ZIP_FILE_NOT_FOUND.
// Nothing else notices: the build is green, the manifest exists, the release
// looks fine — and the app's update button is dead on every Mac.
for (const app of applications.filter(app => app.hasElectron && app.hasElectronUpdater)) {
  const builderFile = scan.files.find(file => /(^|\/)electron-builder\.ya?ml$/.test(file) && (!multiApplication || dirOf(file) === app.directory));
  const builderText = builderFile ? stripComments(text(builderFile) ?? '') : '';
  const manifestTargets = [...builderManifestTargets].filter(([file]) => !multiApplication || dirOf(file) === app.directory);
  const configTargets = macTargetsFromBuilder(builderText);
  const fallback = configTargets ? { targets: configTargets, file: builderFile, line: lineAt(builderText, /^\s*target:/m.exec(builderText)?.index ?? 0) }
    : manifestTargets.length === 1 ? { targets: manifestTargets[0][1], file: manifestTargets[0][0], line: null } : null;
  const scopes = multiApplication ? workflowScopes.filter(scope => scope.application === app.directory)
    : workflowFiles.map(file => ({file, text: stripComments(text(file) ?? '')}));
  const overrides = scopes.map(scope => ({ targets: macTargetsFromArgs(scope.text), file: scope.file,
    line: lineAt(scope.text, /--mac\b/.exec(scope.text)?.index ?? 0) }));
  const checks = multiApplication ? (overrides.length ? overrides.map(override => override.targets?.length ? override : fallback) : [fallback])
    : [overrides.find(override => override.targets?.length) ?? fallback];
  for (const check of checks.filter(Boolean)) {
    if (!check.targets.some(target => /^(dmg|pkg)$/i.test(target)) || check.targets.some(target => /^zip$/i.test(target))) continue;
    if (report.ciFindings.some(finding => finding.id === 'mac-update-needs-zip' && finding.file === check.file && finding.line === check.line && finding.application === app.directory)) continue;
    report.ciFindings.push({ id: 'mac-update-needs-zip', severity: 'P1', confidence: 'heuristic', file: check.file, line: check.line,
      ...(multiApplication ? { application: app.directory } : {}),
      detail: `macOS 的打包目标是 ${check.targets.join('/')}，没有 zip。electron-updater 的 MacUpdater 只在更新清单里找 zip（findFile(files,"zip",["pkg","dmg"]) 里的 pkg/dmg 是**排除表**，不是兜底），所以清单会指向 .dmg，检查更新直接抛 ERR_UPDATER_ZIP_FILE_NOT_FOUND——Mac 上「检查更新」必失败。构建全绿、清单也在，只有用户点得到。`,
      fix: 'mac 的 target 里加 zip（electron-builder.yml 的 mac.target，或工作流里的 `--mac dmg zip`），并在发布流水线里校验 latest-mac.yml 指向 .zip。' });
  }
}

if (yarnFlavor === 'classic') report.ciFindings.push({ id: 'yarn-classic', severity: 'notice', file: 'yarn.lock', line: null, confidence: 'confirmed',
  detail: '项目使用 Yarn 1（classic，仅维护）。house style 默认 npm，但存量 Yarn 项目不强迁：按自己的锁文件走，CI 必须 `--frozen-lockfile`（违反时另报 yarn-install-not-frozen）。',
  fix: '不需要动作。真要迁移时单独一个 PR（迁 npm：删 yarn.lock、`npm install` 生成 package-lock.json、CI 改 `cache: npm` + `npm ci`），不要与框架升级混在一起。' });
if (auditFrameworks && !report.inventory.length) incomplete('未发现 Tauri/Electron 依赖；bootstrap 请按 references/bootstrap.md 选择框架。其他栈请用 --ci-only 或 --dotnet。');

// ---------------- .NET projects / SDK pin (--dotnet) ----------------
let dotnetProjects = [], dotnetGlobals = [];
if (dotnet) {
  const projectFiles = scan.files.filter(f => /\.(?:csproj|fsproj|vbproj)$/.test(f) && !/(^|\/)(?:bin|obj)\//.test(f));
  const globalFiles = scan.files.filter(f => /(^|\/)global\.json$/.test(f) && !/(^|\/)(?:bin|obj)\//.test(f));
  const propsFiles = scan.files.filter(f => /(^|\/)Directory\.Build\.props$/.test(f));
  const targetsFiles = scan.files.filter(f => /(^|\/)Directory\.Build\.targets$/.test(f));
  const nearest = (dir, files) => { for (let d = dir;; d = dirOf(d)) { const hit = files.find(f => dirOf(f) === d); if (hit) return hit; if (d === '.') return null; } };
  for (const file of projectFiles) {
    const parsed = parseTfms(text(file) ?? '');
    let { tfms, unresolved } = parsed, propsFile = null;
    if (!tfms.length && !unresolved.length) {
      for (const props of [nearest(dirOf(file), propsFiles), nearest(dirOf(file), targetsFiles)]) {
        if (!props) continue;
        const p = parseTfms(text(props) ?? '');
        if (p.tfms.length || p.unresolved.length) { tfms = p.tfms; unresolved = p.unresolved; propsFile = props; break; }
      }
    }
    dotnetProjects.push({ file, tfms, unresolved, globalJson: nearest(dirOf(file), globalFiles), propsFile });
  }
  for (const file of globalFiles) {
    try { dotnetGlobals.push({ file, ...parseGlobalJson(text(file) ?? '') }); }
    catch (e) { report.collectionComplete = false; report.errors.push({ scope: file, message: 'global.json 解析失败: ' + String(e.message).split('\n')[0] }); }
  }
  if (!dotnetProjects.length) incomplete('--dotnet 未发现 .NET 项目（.csproj/.fsproj/.vbproj）；确认路径或去掉该模式。');
}
report.scan.configFiles = scan.files.filter(f => /tauri\.conf\.|capabilities\/|electron-builder|forge\.config|rust-toolchain|\.node-version|\.nvmrc|dependabot|renovate|\.desktop-policy|\.(?:csproj|fsproj|vbproj)$|global\.json$|Directory\.Build\.(?:props|targets)$|Directory\.Packages\.props$/.test(f));

// ---------------- online upstream ----------------
let sourceFiles = null;
// Read lazily: only the online, non-ci-only path uses usage hints, so --offline and
// --ci-only must not pay for a full source-tree read (and must not hold it in memory).
const sourceFileTexts = () => {
  if (sourceFiles) return sourceFiles;
  const candidates = scan.files.filter(f => /\.(?:[cm]?[jt]sx?|rs|json|toml|ya?ml|vue|svelte)$/.test(f) && !/(?:lock|shrinkwrap)/.test(f));
  sourceFiles = [];
  for (const file of candidates.slice(0, 1500)) {
    const raw = text(file);
    if (raw === null) continue;
    // An earlier --out report quotes upstream notes and the very tokens we search for.
    if (file.endsWith('.json') && raw.includes('"schemaVersion"')) {
      let data;
      try { data = JSON.parse(raw); } catch { /* other JSON dialects may still contain usage */ }
      if (Array.isArray(data?.inventory) && Array.isArray(data?.changes) && data?.toolVersion) continue;
    }
    sourceFiles.push({ file, text: raw });
  }
  if (candidates.length > 1500) report.warnings.push('API 使用提示仅扫描前 1500 个候选源文件；无匹配不代表不受影响。');
  return sourceFiles;
};
const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN;
if (!token && !offline) report.warnings.push('未设置 GITHUB_TOKEN/GH_TOKEN：GitHub API 每小时仅 60 次，插件或 Action 较多时可能限流（结果标为未知）。可用 `GH_TOKEN=$(gh auth token)`。');
const cache = new Map();
const get = (url, opts = {}) => { const k = url + (opts.raw ? '#raw' : ''); if (!cache.has(k)) cache.set(k, requestJson(url, { token, ...opts })); return cache.get(k); };
async function collect(scope, job) { try { return await job(); } catch (e) { report.collectionComplete = false; report.errors.push({ scope, message: e.message }); return null; } }
const lowest = name => report.inventory.filter(x => x.name === name).map(x => x.resolved).filter(exact).sort(compare)[0] ?? null;

// ---------------- Node toolchain support (online, also for --ci-only) ----------------
let nodeFacts = null;
if (nodePins.length && !offline) await collect('node:schedule', async () => {
  const schedule = await get('https://raw.githubusercontent.com/nodejs/Release/main/schedule.json');
  if (!schedule || typeof schedule !== 'object' || Array.isArray(schedule)) throw new Error('Node release schedule 格式未知');
  nodeFacts = nodeSupportFacts(schedule, checkedAt);
  report.nodeSupport = { ...nodeFacts, source: 'https://raw.githubusercontent.com/nodejs/Release/main/schedule.json', checkedAt };
});
if (nodePins.length && offline) report.warnings.push('发现了 Node 工具链 pin，但离线模式未核验 Active LTS/EOL；联网重跑。');
if (nodeFacts) {
  const byMajor = new Map(nodeFacts.lines.map(l => [l.major, l]));
  const ltsLabel = nodeFacts.latestLts ? `Node ${nodeFacts.latestLts}${nodeFacts.latestLtsStart ? `（LTS ${nodeFacts.latestLtsStart}）` : ''}` : '当前 LTS';
  // P-level findings are for the build toolchain only. `.nvmrc` is an optional
  // local convenience (house-style), so a stale one is a heads-up, not a release finding.
  const ciPins = nodePins.filter(p => p.kind !== 'file'), localPins = nodePins.filter(p => p.kind === 'file');
  const pinsByMajor = new Map();
  for (const p of ciPins) { if (!pinsByMajor.has(p.major)) pinsByMajor.set(p.major, []); pinsByMajor.get(p.major).push(p); }
  for (const [major, pins] of pinsByMajor) {
    const line = byMajor.get(major);
    const where = pins.map(p => `${p.file}${p.line ? ':' + p.line : ''}`).join(', '), extra = pins.length > 1 ? `；位置：${where}` : '';
    if (!line) { report.warnings.push(`Node ${major}: 不在官方 release schedule 中，无法判断支持阶段（${where}）。`); continue; }
    const common = { confidence: 'heuristic', file: pins[0].file, line: pins[0].line ?? null, source: report.nodeSupport.source };
    if (line.phase === 'eol') report.ciFindings.push({ ...common, id: 'node-version-eol', severity: 'P1',
      detail: `Node ${major} 于 ${line.end} 结束支持（EOL），CI 构建工具链不再获得安全补丁。Node 只用于构建，不是应用运行时。${extra}`,
      fix: `把 CI 的 node-version 升到 ${ltsLabel}；engines 下限按工具链约束单独核算，不要照抄 CI major；.nvmrc 可选。` });
    else if (line.phase === 'maintenance' && nodeFacts.latestLts && nodeFacts.latestLts > major) report.ciFindings.push({ ...common, id: 'node-version-maintenance', severity: 'P2',
      detail: `Node ${major} 处于 maintenance（仅安全修复，EOL ${line.end}）；最新 LTS 线是 ${ltsLabel}。${extra}`,
      fix: `计划把 CI 构建线升级到 ${ltsLabel}；house style 要求 CI 为 Active LTS。` });
    else if (!line.lts) report.ciFindings.push({ ...common, id: 'node-version-not-lts', severity: 'P2',
      detail: `Node ${major} 不是 LTS 线（没有 LTS 计划），不适合作为 CI 构建工具链。${extra}`,
      fix: `把 CI 构建线改用 ${ltsLabel}；house style 要求 CI 为 LTS。` });
  }
  const ciMajors = new Set(ciPins.map(p => p.major));
  for (const p of localPins) {
    if (ciMajors.has(p.major)) continue;
    const line = byMajor.get(p.major);
    if (!line) { report.warnings.push(`${p.file}: Node ${p.major} 不在官方 schedule 中；本地版本文件未核验。`); continue; }
    const stale = line.phase === 'eol' ? `已于 ${line.end} EOL` : line.phase === 'maintenance' ? `处于 maintenance（EOL ${line.end}）` : !line.lts ? '不是 LTS 线' : null;
    if (stale) report.warnings.push(`${p.file}: Node ${p.major} ${stale}；它是可选的本地版本文件，不影响 CI。需要时改成 ${ltsLabel}。`);
  }
  report.notes.push('Node 工具链按 nodejs/Release 官方 schedule 判定 active/maintenance/EOL；P 级只针对 CI 的 node-version / node-version-file；.nvmrc/.node-version 是可选本地文件，过期只作 Heads-up。Node 是构建工具，应用运行时使用 Electron 内置 Node 或系统 WebView。');
}
const pushChange = (framework, rel, sourceUrl) => report.changes.push({ framework, tag: rel.tag, version: rel.version, url: rel.url ?? sourceUrl, publishedAt: rel.publishedAt ?? null,
  ...classifyNotes(rel.body), ...usageHints(sourceFileTexts(), rel.body), reviewed: false });

const targetMajors = JSON.parse(fs.readFileSync(new URL('../references/version-targets.json', import.meta.url), 'utf8'));

if (auditFrameworks) {
  for (const item of report.inventory) item.targetMajor = targetMajors[item.ecosystem]?.[item.name] ?? null;
}

if (!offline && auditFrameworks) {
  const knownVersions = new Map();
  for (const key of [...new Set(report.inventory.map(x => `${x.ecosystem}:${x.name}`))]) {
    const [ecosystem, ...rest] = key.split(':'), name = rest.join(':');
    await collect(key, async () => {
      const targetMajor = targetMajors[ecosystem]?.[name] ?? null;
      const npm = ecosystem === 'npm';
      const source = npm ? `https://registry.npmjs.org/${encodeURIComponent(name)}${targetMajor ? '' : '/latest'}` : `https://crates.io/api/v1/crates/${encodeURIComponent(name)}`;
      const data = await get(source);
      let versions, latestStable, engines = null, rustVersion = null;
      if (npm && targetMajor) {
        const tags = data['dist-tags'] ?? {};
        const stableTags = new Set(), previewTags = new Set();
        for (const [tag, version] of Object.entries(tags)) {
          const preview = /^(next|alpha|beta|rc|canary|nightly|dev|preview|experimental)(?:[-.\d]|$)/i.test(tag);
          (preview ? previewTags : stableTags).add(version);
        }
        versions = Object.keys(data.versions ?? {}).filter(v => exact(v) && !data.versions[v].deprecated
          && (!previewTags.has(v) || stableTags.has(v)));
        latestStable = exact(tags.latest) ?? stableMax(versions);
      } else if (npm) {
        latestStable = exact(data.version);
        versions = latestStable ? [latestStable] : [];
        engines = data.engines ?? null;
      } else {
        versions = (data.versions ?? []).filter(v => !v.yanked).map(v => v.num).filter(exact);
        knownVersions.set(name, versions);
        latestStable = stableMax(versions);
      }
      if (!latestStable) throw new Error('包源中未找到可核验的稳定版本');
      const targetStable = targetMajor ? stableMax(versions.filter(v => Number(v.split('.')[0]) === targetMajor)) : latestStable;
      if (!targetStable) incomplete(`${name}: 包源中没有可用的 ${targetMajor}.x 稳定版，无法落实技能目标`);
      if (npm && targetMajor) engines = data.versions?.[targetStable]?.engines ?? null;
      if (!npm) rustVersion = data.versions?.find(v => v.num === targetStable)?.rust_version ?? null;
      report.upstream.push({ ecosystem, name, latestStable, targetMajor, targetStable, checkedAt, source, engines, rustVersion });
    });
  }
  const targetOf = name => report.upstream.find(x => x.name === name)?.targetStable ?? null;
  // Framework release notes over the exact (resolved, latest] interval.
  const frameworks = [];
  if (hasElectron) frameworks.push({ name: 'electron', repo: 'electron/electron', pattern: /^v(\d+\.\d+\.\d+)$/ });
  if (report.inventory.some(x => x.name === 'tauri' && x.ecosystem === 'cargo')) frameworks.push({ name: 'tauri', repo: 'tauri-apps/tauri', pattern: /^tauri-v(\d+\.\d+\.\d+)$/ });
  for (const fw of frameworks) await collect(`releases:${fw.name}`, async () => {
    const floor = lowest(fw.name), target = targetOf(fw.name);
    if (fw.name === 'electron') {
      const index = await get('https://releases.electronjs.org/releases.json');
      if (!Array.isArray(index)) throw new Error('Electron 官方版本索引格式未知');
      const all = index.map(r => String(r.version).replace(/^v/, '')).filter(exact); knownVersions.set('electron', all);
      const supported = electronSupportedMajors(all);
      if (!supported.length) throw new Error('Electron 版本索引缺少稳定版本，无法判断支持窗口');
      report.electronSupport = { supportedMajors: supported, policy: '最新三个稳定 major 受支持，且每条线只维护最新 minor', source: 'https://releases.electronjs.org/releases.json', schedule: 'https://releases.electronjs.org/schedule' };
      if (!supported.includes(targetMajors.npm.electron)) report.frameworkFindings.push({ id: 'electron-target-unsupported', severity: 'P0', confidence: 'confirmed',
        detail: `技能指定的 Electron ${targetMajors.npm.electron}.x 已不在上游支持窗口`, fix: '标明目标线的支持期冲突并复核技能版本策略。', source: report.electronSupport.schedule });
      for (const x of report.inventory.filter(i => i.name === 'electron' && i.resolved)) {
        const major = Number(x.resolved.split('.')[0]);
        if (!supported.includes(major)) report.frameworkFindings.push({ id: 'electron-unsupported-major', severity: 'P0', confidence: 'confirmed', file: x.manifest,
          detail: `Electron ${x.resolved} 的 major ${major} 已不在受支持的 ${supported.join('/')} 内，不再获得安全补丁（含 Chromium）。`, fix: `核对技能目标 Electron ${targetMajors.npm.electron}.x 的支持期，在目标线上迁移并验证。`, source: report.electronSupport.schedule });
        else if (major === Math.min(...supported)) report.frameworkFindings.push({ id: 'electron-oldest-supported-major', severity: 'P1', confidence: 'confirmed', file: x.manifest,
          detail: `Electron ${major} 是当前最老的受支持 major，下一个 major 发布时即停止支持。`, fix: '在 schedule 的下个稳定版日期前完成升级计划。', source: report.electronSupport.schedule });
      }
    }
    if (!target) return;
    const known = knownVersions.get(fw.name);
    const expected = floor && target && known?.includes(floor) && known.includes(target) ? [...new Set(known.filter(v => compare(v, floor) > 0 && compare(v, target) <= 0))] : null;
    const history = await releaseHistory(fw.repo, fw.pattern, floor, pages, get, expected);
    report[`${fw.name}History`] = { coverage: history.coverage, truncated: history.truncated, missingVersions: history.missingVersions, visited: history.visited.length, expectedReleaseCount: expected?.length ?? null };
    if (history.truncated || !floor || expected === null) incomplete(`${fw.name}: release 覆盖 ${history.coverage}，迁移清单不完整；加大 --pages 或查阅官方 breaking-changes。`);
    for (const rel of history.releases.filter(r => (!floor || compare(r.version, floor) > 0) && (!target || compare(r.version, target) <= 0))) pushChange(fw.name, rel);
  });
  // Official Tauri plugins: JS and Rust halves must move together; changelog lives in plugins-workspace (branch v2).
  const plugins = new Set(report.inventory.map(x => /^(?:tauri-plugin-|@tauri-apps\/plugin-)([\w-]+)$/.exec(x.name)?.[1]).filter(Boolean));
  for (const p of plugins) await collect(`plugin:${p}`, async () => {
    const rustName = `tauri-plugin-${p}`, jsName = `@tauri-apps/plugin-${p}`;
    const local = lowest(rustName) ?? lowest(jsName), target = targetOf(rustName) ?? targetOf(jsName);
    for (const app of multiApplication ? applications : [{directory: null, inventory: report.inventory}]) {
      const rust = app.inventory.filter(x => x.name === rustName), js = app.inventory.filter(x => x.name === jsName);
      if (!rust.length && !js.length) continue;
      if (multiApplication && new Set(rust.map(item => item.resolved)).size > 1) {
        incomplete(`${app.directory}: 插件 ${p} 的 Cargo 锁文件含多个版本，无法确认直接依赖；用 cargo metadata 核验`); continue;
      }
      const location = multiApplication ? {application: app.directory} : {};
      const pairOk = rust.length && js.length ? rust.every(r => js.every(j => r.resolved && r.resolved === j.resolved)) : null;
      report.compatibility.push({ ...location, rule: 'official-plugin-exact-pair', plugin: p, status: pairOk === false ? 'mismatch' : pairOk ? 'ok' : 'one-side-only',
        rust: rust.map(x => ({ version: x.resolved, file: x.manifest })), js: js.map(x => ({ version: x.resolved, file: x.manifest })), source: 'https://v2.tauri.app/develop/updating-dependencies' });
      if (pairOk === false) report.frameworkFindings.push({ ...location, id: 'tauri-plugin-skew', severity: 'P0', confidence: 'confirmed', file: rust[0].manifest,
        detail: `插件 ${p} 的 Rust(${rust.map(x => x.resolved).join('/')}) 与 JS(${js.map(x => x.resolved).join('/')}) 版本不一致；不会在构建时失败，而是运行时缺命令/行为错位。`, fix: '同一提交中把两侧升级到同一完整版本。' });
    }
    if (!local || !target || compare(local, target) >= 0) return;
    const url = `https://api.github.com/repos/tauri-apps/plugins-workspace/contents/plugins/${p}/CHANGELOG.md?ref=v2`;
    const md = await get(url, { raw: true, allow404: true });
    if (md === null) { report.warnings.push(`插件 ${p}: plugins-workspace 中没有 CHANGELOG（第三方插件？），需到其自身仓库核验。`); return; }
    const web = `https://github.com/tauri-apps/plugins-workspace/blob/v2/plugins/${p}/CHANGELOG.md`;
    for (const s of changelogSections(md).filter(s => compare(s.version, local) > 0 && compare(s.version, target) <= 0))
      pushChange(`tauri-plugin-${p}`, { tag: `v${s.version}`, version: s.version, body: s.body.replace(/^###/gm, '##') }, web);
  });
  // Packagers ship independently of Electron; read their own release notes for the local->latest interval.
  for (const pkg of ['electron-builder', 'electron-updater'].filter(n => has(n))) await collect(`releases:${pkg}`, async () => {
    const floor = lowest(pkg), target = targetOf(pkg); if (!floor || !target || compare(floor, target) >= 0) return;
    const history = await releaseHistory('electron-userland/electron-builder', new RegExp(`^${pkg}@(\\d+\\.\\d+\\.\\d+)$`), floor, pages, get, null);
    const ghLatest = stableMax(history.releases.map(r => r.version));
    if (ghLatest && ghLatest.split('.')[0] === target.split('.')[0] && compare(ghLatest, target) > 0) report.warnings.push(`${pkg}: GitHub 已有 ${ghLatest} release，本次核实的 npm 稳定目标是 ${target}。核实较新版本是否已发布到项目配置的包源并属于目标大版本的稳定线，符合时安装精确版本并验证。`);
    if (!history.reachedFloor && !history.exhausted) incomplete(`${pkg}: 未在 ${pages} 页内找到本地版本 ${floor} 的 release，变更区间可能不完整。`);
    for (const rel of history.releases.filter(r => compare(r.version, floor) > 0 && compare(r.version, target) <= 0)) pushChange(pkg, rel);
  });
}
// Tauri API/core minor pairing (offline-safe).
for (const app of multiApplication ? applications : [{directory: null, inventory: report.inventory}]) {
  const tauriCore = app.inventory.filter(x => x.name === 'tauri' && x.ecosystem === 'cargo'), tauriApi = app.inventory.filter(x => x.name === '@tauri-apps/api');
  if (auditFrameworks && tauriCore.length && tauriApi.length) {
    if (multiApplication && new Set(tauriCore.map(item => item.resolved)).size > 1) {
      incomplete(`${app.directory}: Tauri core 的 Cargo 锁文件含多个版本，无法确认直接依赖；用 cargo metadata 核验`); continue;
    }
    const location = multiApplication ? {application: app.directory} : {};
    const mm = v => v?.split('.').slice(0, 2).join('.');
    const ok = tauriCore.every(c => tauriApi.every(a => c.resolved && a.resolved && mm(c.resolved) === mm(a.resolved)));
    report.compatibility.push({ ...location, rule: 'tauri-api-same-minor', status: ok ? 'ok' : 'review', rust: tauriCore.map(x => x.resolved), js: tauriApi.map(x => x.resolved), source: 'https://v2.tauri.app/develop/updating-dependencies',
      note: 'CLI/build/macros 独立发版，不要求全部版本号相等。' });
    if (!ok) report.frameworkFindings.push({ ...location, id: 'tauri-api-core-minor-skew', severity: 'P1', confidence: 'heuristic', file: tauriApi[0].manifest,
      detail: `@tauri-apps/api(${tauriApi.map(x => x.resolved).join('/')}) 与 tauri(${tauriCore.map(x => x.resolved).join('/')}) 的 major.minor 不一致（monorepo 请逐应用配对）。`, fix: '把二者调整到同一 major.minor。' });
  }
}
// Action pins: latest release and major gap. House style pins major tags, so suggestedPin is `@v<latest major>`.
if (!offline) for (const repository of [...new Set(report.actions.map(a => a.repository))]) await collect(`action:${repository}`, async () => {
  const latest = await get(`https://api.github.com/repos/${repository}/releases/latest`, { allow404: true });
  const tags = await get(`https://api.github.com/repos/${repository}/tags?per_page=100`);
  const latestTag = latest?.tag_name ?? null, latestVer = refVersion(latestTag ?? '');
  const majorTags = tags.filter(t => /^v\d+$/.test(t.name)).map(t => Number(t.name.slice(1)));
  const latestMajor = latestVer?.major ?? (majorTags.length ? Math.max(...majorTags) : null);
  for (const a of report.actions.filter(x => x.repository === repository)) {
    const shaTags = a.immutableReference ? tags.filter(t => t.commit.sha === a.ref).map(t => t.name) : [];
    // dtolnay/rust-toolchain@stable / @1.89.0 names a Rust toolchain, not an action version.
    const toolchainRef = repository === 'dtolnay/rust-toolchain' && /^(stable|beta|nightly|\d+\.\d+(\.\d+)?)$/.test(a.ref);
    const cur = toolchainRef ? null : a.immutableReference ? refVersion(shaTags.find(n => /\d+\.\d+\.\d+$/.test(n)) ?? shaTags[0] ?? '') : refVersion(a.ref);
    Object.assign(a, { latestReleaseTag: latestTag, latestMajor, currentRefTags: shaTags, currentMajor: cur?.major ?? null, toolchainRef,
      writeCapable: WRITE_CAPABLE_ACTIONS.has(repository), suggestedPin: toolchainRef ? `${a.action}@${a.ref}` : latestMajor !== null ? `${a.action}@v${latestMajor}` : null, tagListingTruncated: tags.length === 100 });
    if (cur && latestMajor !== null && cur.major < latestMajor) report.ciFindings.push({ id: 'action-major-behind', severity: 'P1', confidence: 'confirmed', file: a.file, line: a.line,
      detail: `${a.action}@${a.ref} 落后：当前 major ${cur.major}，最新 release ${latestTag}。\`@v${cur.major}\` 永远不会自动升到新 major。`, fix: `阅读该 Action 的 release notes 后单独升到大版本标签 \`@v${latestMajor}\`（house style：钉大版本标签，不钉 SHA）。` });
    // house style 钉的就是大版本标签，所以只读 Action 的可移动 ref 不是问题。
    // 能写产物的那几个是另一类风险：被接管时受影响的正是用户下载到的东西。
    // 符合 house style，所以是 notice（不计入 P0/P1/P2），只为让人单独看一眼。
    if (!a.immutableReference && a.writeCapable) report.ciFindings.push({ id: 'action-moving-ref', severity: 'notice', confidence: 'confirmed', file: a.file, line: a.line,
      detail: `${a.action}@${a.ref} 是可移动 ref，而这个 Action 能创建/上传用户安装的产物或证明——被接管时受影响的正是用户下载到的东西。`, fix: `符合 house style（大版本标签），无需动作；要收紧就钉精确版本${latestTag ? `（\`@${latestTag}\`）` : ''}，不钉 SHA。` });
    else if (a.immutableReference && !shaTags.length) report.warnings.push(`${a.file}:${a.line} ${a.action} 钉的 SHA 未在前 100 个 tag 中找到对应版本（当前版本未知，不等于最新）。`);
  }
});
if (actionsLock) report.warnings.push('存在 .github/workflows/actions.lock：确认它覆盖每个 workflow 且由官方工具生成；脚本不验证锁内容。');

// ---------------- .NET runtime/SDK metadata + analysis (--dotnet) ----------------
if (dotnet) {
  const dotnetMetadata = {};
  if (!offline && dotnetProjects.length) {
    const channels = [...new Set(dotnetProjects.flatMap(p => p.tfms.map(tfmInfo).filter(t => t.kind === 'runtime').map(t => t.channel)))];
    // A global.json may pin a newer SDK than the TFM (e.g. net8.0 built by SDK 10).
    // Fetch that channel too, or analyzeDotnet has no metadata for the pin and marks
    // a perfectly normal setup as an incomplete collection.
    for (const g of dotnetGlobals) {
      const pin = sdkParts(g.version);
      if (pin && !channels.includes(`${pin.major}.${pin.minor}`)) channels.push(`${pin.major}.${pin.minor}`);
    }
    for (const channel of channels) {
      const meta = await collect(`dotnet:${channel}`, async () => {
        const json = await get(metadataUrl(channel), { allow404: true });
        if (!json) { report.warnings.push(`.NET ${channel}: release metadata 404；通道可能已停止发布，EOL/最新 SDK 未知。`); return null; }
        return normalizeMetadata(json);
      });
      if (meta) dotnetMetadata[channel] = meta;
    }
  }
  const d = analyzeDotnet({ projects: dotnetProjects, globalJsons: dotnetGlobals, metadata: dotnetMetadata,
    workflows: workflowFiles.map(file => ({ file, text: text(file) ?? '' })), now: checkedAt, offline });
  report.dotnet = { detected: d.detected, projects: d.projects, globalJson: d.globalJson, channels: d.channels };
  report.frameworkFindings.push(...d.framework);
  report.ciFindings.push(...d.ci);
  report.warnings.push(...d.warnings);
  for (const msg of d.incomplete) incomplete(msg);
  report.notes.push('.NET 模式：TFM 支持期/EOL 取自官方 release metadata；global.json 的 rollForward 语义按官方文档；未执行 dotnet/MSBuild，SDK pin 能否在目标机器/CI 解析需实测。');
}

// ---------------- baseline ----------------
if (baselinePath) {
  let baseline;
  try { baseline = JSON.parse(fs.readFileSync(baselinePath, 'utf8')); }
  catch (e) { die(`无法读取基线 ${baselinePath}: ${e.message.split('\n')[0]}`); }
  if (![2, 3].includes(baseline.schemaVersion) || baseline.project !== root || !Array.isArray(baseline.reviewedChangeIds)) die('基线格式或项目路径不匹配');
  const ids = new Set(baseline.reviewedChangeIds);
  report.changes.forEach(c => { c.reviewed = ids.has(`${c.framework}:${c.tag}`); });
  report.baseline = { path: baselinePath, reviewedAt: baseline.reviewedAt, note: '仅标记已审阅 release；风险、兼容性与 CI 仍完整展示。' };
}
report.warnings = [...new Set(report.warnings)];
for (const f of [...report.ciFindings, ...report.frameworkFindings]) { const acc = acceptedRules.get(f.id); if (acc) f.accepted = acc; }
const order = { P0: 0, P1: 1, P2: 2, notice: 3 };
report.ciFindings.sort((a, b) => order[a.severity] - order[b.severity] || String(a.file).localeCompare(String(b.file)) || (a.line ?? 0) - (b.line ?? 0));
report.summary = {
  framework: Object.fromEntries(['P0-candidate', 'P1-candidate', 'P2-candidate', 'unclassified'].map(k => [k, report.changes.filter(c => c.suggestedPriority === k && !c.reviewed).length])),
  frameworkFindings: report.frameworkFindings.filter(f => !f.accepted).length,
  frameworkAccepted: report.frameworkFindings.filter(f => f.accepted).length,
  ci: Object.fromEntries(['P0', 'P1', 'P2', 'notice'].map(k => [k, report.ciFindings.filter(f => f.severity === k && !f.accepted).length])),
  ciAccepted: report.ciFindings.filter(f => f.accepted).length,
};

// ---------------- output ----------------
if (out) {
  if (fs.existsSync(out)) die('--out 已存在；拒绝覆盖');
  try { fs.writeFileSync(out, JSON.stringify(report, null, 2) + '\n', { flag: 'wx' }); }
  catch (e) { die(`无法写入报告: ${e.message.split('\n')[0]}`); }
}
if (json) console.log(JSON.stringify(report, null, 2));
else {
  const L = [];
  L.push(`# Desktop App Standard ${TOOL_VERSION}`, `Checked: ${checkedAt} · Mode: ${report.mode}${ciOnly ? ' (ci-only)' : ''}${dotnet ? ' · dotnet' : ''} · Collection: ${report.collectionComplete ? 'complete within declared bounds' : 'INCOMPLETE'} (not a release verdict)`);
  if (auditFrameworks) {
    L.push('', '## 版本矩阵');
    for (const x of report.inventory) { const u = report.upstream.find(y => y.name === x.name && y.ecosystem === x.ecosystem);
      L.push(`- ${x.ecosystem} ${x.name}: local=${x.resolved ?? 'UNKNOWN'} (${x.lockfile ?? 'no lock'}) · declared=${typeof x.declared === 'string' ? x.declared : '—'} · upstream=${u?.latestStable ?? 'UNKNOWN'} · targetMajor=${x.targetMajor ?? 'auto'} · target=${u?.targetStable ?? 'UNKNOWN'} · ${x.manifest}`); }
    if (report.electronSupport) L.push(`- Electron 受支持 major: ${report.electronSupport.supportedMajors.join(', ')}（按官方政策计算；日期以 schedule 为准）`);
    if (nodePins.length) {
      const pins = nodePins.map(p => `${p.file}${p.line ? ':' + p.line : ''}=${p.major}${p.kind === 'file' ? ' (local)' : ''}`).join(' · ');
      const support = report.nodeSupport
        ? `latest LTS ${report.nodeSupport.latestLts ?? 'UNKNOWN'}${report.nodeSupport.latestLtsStart ? `（LTS ${report.nodeSupport.latestLtsStart}）` : ''}${report.nodeSupport.activeLts ? ` · active ${report.nodeSupport.activeLts}` : ''}`
        : offline ? 'offline，未核验' : '未核验（网络/schedule 失败）';
      L.push(`- Node 工具链: ${pins} · ${support}`);
    }
    const fw = report.frameworkFindings.filter(f => !f.accepted);
    L.push('', '## 框架 P0/P1（已确认）', ...(fw.length ? fw.map(f => `- [${f.severity}] ${f.id} · ${f.file}: ${f.detail} → ${f.fix}`) : ['- 无']));
    const s = report.summary.framework;
    L.push('', `## 上游变更候选（未审阅）: P0候选 ${s['P0-candidate']} · P1候选 ${s['P1-candidate']} · P2候选 ${s['P2-candidate']} · 未分类 ${s.unclassified}`);
    for (const c of report.changes.filter(c => !c.reviewed && c.suggestedPriority === 'P0-candidate').slice(0, 20))
      L.push(`- ${c.framework} ${c.tag} [${c.categories.join('/')}] ${c.url}${c.hits.length ? ' · touches ' + c.hits.map(h => `${h.file}:${h.line} (${h.token})`).join(', ') : ' · 未匹配到用法（不等于不受影响）'}`);
  }
  if (dotnet) {
    L.push('', '## .NET 运行时与 SDK');
    if (!report.dotnet?.detected) L.push('- 未发现 .csproj/.fsproj/.vbproj');
    for (const p of report.dotnet?.projects ?? []) {
      const tfms = p.tfms.length ? p.tfms.map(t => `${t.tfm}${t.kind === 'runtime' ? ` (${t.channel})` : ` (${t.kind})`}`).join(', ') : 'UNRESOLVED';
      L.push(`- ${p.file}: ${tfms}${p.globalJson ? ` · ${p.globalJson}` : ''}${p.propsFile ? ` · TFM from ${p.propsFile}` : ''}${p.unresolved.length ? ` · unresolved: ${p.unresolved.join(', ')}` : ''}`);
    }
    for (const g of report.dotnet?.globalJson ?? []) {
      const reach = g.guaranteedLatest === null ? 'latest unknown' : g.guaranteedLatest ? 'rolls to latest' : g.reason;
      L.push(`- ${g.file}: SDK ${g.version ?? 'UNPINNED'} · rollForward ${g.rollForward ?? '(default) patch'}${g.latestSdk ? ` · latest ${g.latestSdk} (${reach})` : ''}${g.latestRelease ? ` · latest runtime ${g.latestRelease}` : ''}${g.testRunner ? ` · test runner ${g.testRunner}` : ''}`);
    }
    for (const c of report.dotnet?.channels ?? [])
      L.push(`- .NET ${c.channel}: ${c.supportPhase ?? 'UNKNOWN'}${c.eolDate ? ` · EOL ${c.eolDate}` : ''}${c.latestSdk ? ` · latest SDK ${c.latestSdk}` : ''}${c.latestRuntime ? ` · runtime ${c.latestRuntime}` : ''} · ${c.projects.join(', ')}`);
    const dn = report.frameworkFindings.filter(f => f.id.startsWith('dotnet-') && !f.accepted);
    L.push('', '## .NET 发现（P0/P1/P2 / notice）', ...(dn.length ? dn.map(f => `- [${f.severity}] ${f.id} · ${f.file ?? '?'}: ${f.detail} → ${f.fix}`) : ['- 未发现']));
  }
  L.push('', '## CI & Release（与框架风险分开处理）');
  for (const [kind, files] of Object.entries(report.workflowCoverage)) L.push(`- ${kind}: ${files.join(', ') || '未发现静态证据'}`);
  const where = f => `${f.file}${f.line ? ':' + f.line : ''}${f.application ? ` [${f.application}]` : ''}`;
  for (const sev of ['P0', 'P1', 'P2']) { const list = report.ciFindings.filter(f => f.severity === sev && !f.accepted); if (!list.length) continue;
    L.push(`### ${sev}`); for (const f of list) L.push(`- ${where(f)} ${f.id}: ${f.detail} → ${f.fix}`); }
  if (!report.ciFindings.some(f => f.severity !== 'notice' && !f.accepted)) L.push('- 未发现 P0/P1/P2 候选（启发式，不等于发布链已验证）');
  const notices = report.ciFindings.filter(f => f.severity === 'notice' && !f.accepted), accepted = [...report.ciFindings, ...report.frameworkFindings].filter(f => f.accepted);
  if (notices.length) { L.push('### 提示（符合 house style，不计入 P0/P1/P2）'); for (const f of notices) L.push(`- ${where(f)} ${f.id}: ${f.detail}`); }
  if (accepted.length) { L.push('### 已接受的偏离（.desktop-policy.json，不计入 P0/P1/P2）'); for (const f of accepted) L.push(`- [${f.severity}] ${where(f)} ${f.id} · reason: ${f.accepted.reason} · revisitWhen: ${f.accepted.revisitWhen}`); }
  L.push('', '## Heads-up', ...report.warnings.map(x => '- ' + x), ...report.scan.skipped.map(x => '- skipped: ' + x), ...report.errors.map(e => `- ERROR ${e.scope}: ${e.message}`));
  L.push('', 'No code was executed; no dependencies, files, baselines or releases were changed. Use --json/--out for raw notes and evidence.');
  console.log(L.join('\n'));
}
process.exitCode = report.collectionComplete ? 0 : 2;
