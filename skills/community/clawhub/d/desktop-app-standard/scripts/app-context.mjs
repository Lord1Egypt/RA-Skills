import path from 'node:path';
import { jobBlocks, stripComments } from './ci-traps.mjs';

const dirOf = file => path.posix.dirname(file);
export const within = (file, directory) => directory === '.' || file === directory || file.startsWith(directory + '/');
export const tauriDirectory = file => path.posix.basename(dirOf(file)) === 'src-tauri' ? dirOf(dirOf(file)) : dirOf(file);

// Shared workspace manifests can supply dependencies to child applications.
// A sibling application's manifest can never supply them.
export function applicationInventory(directory, inventory, manifests) {
  const nearest = manifests.filter(file => within(directory, dirOf(file)))
    .sort((a, b) => (dirOf(b) === '.' ? 0 : dirOf(b).length) - (dirOf(a) === '.' ? 0 : dirOf(a).length))[0];
  return inventory.filter(item => item.ecosystem === 'npm' ? dirOf(item.manifest) === dirOf(nearest ?? '')
    : within(directory, dirOf(item.manifest)) || dirOf(item.manifest) === directory || dirOf(item.manifest) === path.posix.join(directory, 'src-tauri'));
}

export function discoverApplications(configs, inventory, manifests = [], cargoSources = []) {
  const directories = new Set(configs.map(config => tauriDirectory(config.file)));
  for (const item of inventory.filter(item => item.ecosystem === 'npm')) {
    const directory = dirOf(item.manifest);
    if (item.name === 'electron' || item.name === 'electron-updater') directories.add(directory);
    if (item.name.startsWith('@tauri-apps/') && ![...directories].some(child => within(child, directory))) directories.add(directory);
  }
  for (const item of inventory.filter(item => item.ecosystem === 'cargo' && item.manifest.endsWith('Cargo.toml'))) {
    directories.add(tauriDirectory(item.manifest));
  }
  for (const source of cargoSources) {
    if (/^\s*tauri(?:\.workspace)?\s*=/m.test(stripComments(source.text)) && (!/\[workspace/.test(source.text) || /\[package\]/.test(source.text)))
      directories.add(tauriDirectory(source.file));
  }
  return [...directories].sort().map(directory => {
    const local = applicationInventory(directory, inventory, manifests);
    const has = name => local.some(item => item.name === name);
    const tauriConfigs = configs.filter(config => tauriDirectory(config.file) === directory);
    const cargo = cargoSources.filter(source => [directory, path.posix.join(directory, 'src-tauri')].includes(dirOf(source.file)));
    const rustUpdater = cargo.length ? cargo.some(source => /^\s*tauri-plugin-updater(?:\.workspace)?\s*=|package\s*=\s*["']tauri-plugin-updater["']|^\s*\[[^\]\n]*dependencies\.tauri-plugin-updater\]/m.test(stripComments(source.text)))
      : local.some(item => item.name === 'tauri-plugin-updater' && within(item.manifest, directory));
    const rustApp = cargo.some(source => /^\s*tauri(?:\.workspace)?\s*=/m.test(stripComments(source.text))) ||
      local.some(item => item.name === 'tauri' && within(item.manifest, directory));
    return { directory, inventory: local, tauriConfigs,
      isTauri: tauriConfigs.length > 0 || rustApp || has('@tauri-apps/cli'),
      hasElectron: has('electron'), hasElectronUpdater: has('electron-updater'),
      usesTauriUpdater: rustUpdater || has('@tauri-apps/plugin-updater') };
  });
}

function scalar(text, key) {
  const match = new RegExp(`^[ \\t]*(?:- +)?${key}:[ \\t]*(.+)$`, 'm').exec(text);
  if (!match) return null;
  return match[1].trim().replace(/^(['"])(.*)\1$/, '$2');
}

function defaultDirectory(text) {
  const defaults = /^( *)defaults:\s*\n((?:\1 +[^\n]*\n?)*)/m.exec(text);
  return defaults ? scalar(defaults[2], 'working-directory') : null;
}

function buildKind(text) {
  if (/tauri-apps\/tauri-action|\b(?:cargo +)?tauri +(build|dev)|(?:yarn|pnpm|npm run) +(?:build:tauri|tauri)\b/.test(text)) return 'tauri';
  if (/electron-builder|electron-forge|electron:build/.test(text)) return 'electron';
  if (/gh release (create|upload)|action-gh-release|ncipollo\/release-action/.test(text)) return 'release';
  return null;
}

// Recognizes literal paths in standard block-style GitHub workflows. Expressions,
// custom checkout layouts and unsupported step layouts remain explicit unknowns.
export function workflowApplications(file, source, applications, files = []) {
  const text = stripComments(source);
  const jobs = jobBlocks(text);
  const header = text.slice(0, jobs[0]?.offset ?? text.length);
  const workflowDirectory = defaultDirectory(header);
  const scopes = [];
  for (const job of jobs) {
    const stepsAt = /^( *)steps:[ \t]*$/m.exec(job.text);
    if (!stepsAt) {
      if (/^[ \t]*uses:/m.test(job.text)) scopes.push({file, job: job.name, line: text.slice(0, job.offset).split('\n').length,
        directory: null, application: null, reason: 'reusable workflow 的应用归属需要人工核对', text: ''});
      continue;
    }
    const heads = [...job.text.matchAll(/^( *)- +[^\n]+/gm)]
      .filter(match => match.index > stepsAt.index && [stepsAt[1].length, stepsAt[1].length + 2].includes(match[1].length));
    const steps = heads.map((match, index) => ({ start: match.index, end: heads[index + 1]?.index ?? job.text.length,
      text: job.text.slice(match.index, heads[index + 1]?.index ?? job.text.length) }));
    const builds = steps.filter(step => buildKind(step.text));
    for (const step of builds) {
      const kind = buildKind(step.text);
      const action = /uses:\s*tauri-apps\/tauri-action@/.test(step.text);
      const actionStep = /uses:/.test(step.text);
      const cd = /(?:^|[\n;&|])\s*cd\s+([^\n;&|]+)/.exec(step.text)?.[1]?.trim();
      let directory = action ? scalar(step.text, 'projectPath') : actionStep ? null
        : scalar(step.text, 'working-directory') ?? defaultDirectory(job.text.slice(0, stepsAt.index)) ?? workflowDirectory;
      const explicit = directory !== null || cd !== undefined;
      directory ??= '.';
      if (cd) directory = path.posix.join(directory, cd.replace(/^(['"])(.*)\1$/, '$2'));
      const normalized = path.posix.normalize(directory.replace(/\\/g, '/')).replace(/\/$/, '') || '.';
      let reason = null;
      if (action && /projectPath:/.test(step.text) && scalar(step.text, 'projectPath') === null) reason = '无法解析 projectPath 写法';
      if (/--prefix\b|--cwd\b|(?:^|\s)-C\s|--config\b|TAURI_CONFIG/.test(step.text)) reason = '构建使用了目录或配置覆盖参数，需要人工核对';
      if ([...step.text.matchAll(/(?:^|[\n;&|])\s*cd\s+/g)].length > 1) reason = '构建步骤包含多次目录切换';
      if (/[$`{}*]|\s/.test(normalized) || path.posix.isAbsolute(normalized) || /^[A-Za-z]:/.test(normalized) || normalized === '..' || normalized.startsWith('../')) reason = '构建路径为动态表达式或不支持的路径';
      if (/uses:\s*actions\/checkout@[^\n]+[\s\S]*?\n +path:/.test(job.text)) reason = '自定义 checkout 路径需要人工核对';
      const candidates = applications.filter(app => (kind === 'tauri' ? app.isTauri : kind === 'electron' ? app.hasElectron : true) && within(normalized, app.directory))
        .sort((a, b) => (b.directory === '.' ? 0 : b.directory.length) - (a.directory === '.' ? 0 : a.directory.length));
      let app = candidates[0];
      if (!explicit && applications.length === 1) app = applications[0];
      if (!app) reason ??= '构建路径无法唯一关联到已发现的应用';
      if (explicit && files.length && !files.some(file => within(file, normalized))) reason ??= '构建目录在扫描范围内不存在';
      // Keep shared setup and job headers, mask other build steps at their original
      // offsets so rule locations still refer to the original workflow.
      let scoped = text.slice(0, job.offset).replace(/[^\n]/g, ' ') + job.text;
      for (const other of builds.filter(other => other !== step)) {
        const start = job.offset + other.start, end = job.offset + other.end;
        scoped = scoped.slice(0, start) + scoped.slice(start, end).replace(/[^\n]/g, ' ') + scoped.slice(end);
      }
      scopes.push({ file, job: job.name, line: text.slice(0, job.offset + step.start).split('\n').length,
        directory: normalized, application: reason ? null : app.directory, reason, text: scoped });
    }
    if (!builds.length && buildKind(job.text)) {
      scopes.push({ file, job: job.name, line: text.slice(0, job.offset).split('\n').length,
        directory: null, application: null, reason: '无法解析构建步骤布局', text: '' });
    }
  }
  if (!scopes.length && buildKind(text)) scopes.push({ file, job: null, line: 1, directory: null,
    application: null, reason: '无法解析构建 job 或步骤布局', text: '' });
  return scopes;
}
