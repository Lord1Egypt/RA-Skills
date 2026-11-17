// .NET runtime/SDK lifecycle facts. Pure: no filesystem, network or dotnet invocation.
import { jobBlocks, stripComments } from './ci-traps.mjs';

export const DOTNET_METADATA_HOST = 'builds.dotnet.microsoft.com';
export const metadataUrl = channel =>
  `https://builds.dotnet.microsoft.com/dotnet/release-metadata/${channel}/releases.json`;

// global.json accepts // and /* */ comments (official docs); JSON.parse alone is wrong.
export function stripJsonComments(text) {
  const s = String(text ?? '');
  let out = '', quote = false, escaped = false;
  for (let i = 0; i < s.length; i++) {
    const c = s[i], n = s[i + 1];
    if (quote) {
      out += c;
      if (escaped) escaped = false;
      else if (c === '\\') escaped = true;
      else if (c === '"') quote = false;
      continue;
    }
    if (c === '"') { quote = true; out += c; continue; }
    if (c === '/' && n === '/') {
      while (i < s.length && s[i] !== '\n') i++;
      out += '\n';
      continue;
    }
    if (c === '/' && n === '*') {
      i += 2;
      while (i < s.length && !(s[i] === '*' && s[i + 1] === '/')) i++;
      i++;
      continue;
    }
    out += c;
  }
  return out;
}

export function parseGlobalJson(text) {
  const json = JSON.parse(stripJsonComments(text));
  const obj = json && typeof json === 'object' && !Array.isArray(json) ? json : {};
  const sdk = obj.sdk && typeof obj.sdk === 'object' ? obj.sdk : {};
  return {
    version: typeof sdk.version === 'string' ? sdk.version.trim() : null,
    rollForward: typeof sdk.rollForward === 'string' ? sdk.rollForward.trim() : null,
    allowPrerelease: typeof sdk.allowPrerelease === 'boolean' ? sdk.allowPrerelease : null,
    testRunner: typeof obj.test?.runner === 'string' ? obj.test.runner : null,
    msbuildSdks: obj['msbuild-sdks'] ?? null,
  };
}

export function parseTfms(text) {
  const clean = String(text ?? '').replace(/<!--[\s\S]*?-->/g, '');
  const tfms = new Set(), unresolved = new Set();
  for (const m of clean.matchAll(/<TargetFrameworks?(?:\s[^>]*)?>([\s\S]*?)<\/TargetFrameworks?>/gi)) {
    for (const raw of m[1].split(';')) {
      const v = raw.trim();
      if (!v) continue;
      if (v.includes('$(')) unresolved.add(v); else tfms.add(v);
    }
  }
  for (const m of clean.matchAll(/<TargetFrameworkVersion>\s*v?([\d.]+)\s*<\/TargetFrameworkVersion>/gi)) {
    const v = m[1].replace(/\./g, '');
    if (v) tfms.add(`net${v}`);
  }
  return { tfms: [...tfms], unresolved: [...unresolved] };
}

export function tfmInfo(tfm) {
  const v = String(tfm ?? '').trim(), lower = v.toLowerCase();
  if (/^netstandard\d+(?:\.\d+)?$/.test(lower)) return { tfm: v, kind: 'library' };
  if (/^net\d{2,3}$/.test(lower)) return { tfm: v, kind: 'framework' };
  let m = /^netcoreapp(\d+)\.(\d+)$/.exec(lower);
  if (m) {
    const major = Number(m[1]), minor = Number(m[2]);
    return { tfm: v, kind: 'runtime', major, minor, channel: `${major}.${minor}` };
  }
  m = /^net(\d+)\.(\d+)(?:-([a-z]+).*)?$/.exec(lower);
  if (m) {
    const major = Number(m[1]), minor = Number(m[2]);
    if (major < 5) return { tfm: v, kind: 'framework' };
    return { tfm: v, kind: 'runtime', major, minor, channel: `${major}.${minor}`, os: m[3] ?? null };
  }
  return { tfm: v, kind: 'unknown' };
}

// SDK x.y.znn: z is the feature band, nn the patch.
export function sdkParts(version) {
  const raw = String(version ?? '').trim();
  const m = /^(\d+)\.(\d+)\.(\d{3})(?:-([0-9A-Za-z.-]+))?$/.exec(raw);
  if (!m) return null;
  const third = Number(m[3]);
  return { version: raw, major: Number(m[1]), minor: Number(m[2]), featureBand: Math.floor(third / 100), patch: third % 100, prerelease: m[4] ?? null };
}

const versionCompare = (a, b) =>
  (a.major - b.major) || (a.minor - b.minor) || (a.featureBand - b.featureBand) || (a.patch - b.patch);

// Only latest* policies choose the highest installed SDK. patch/feature/minor/major use the
// specified version (or the specified/next band) when it exists, so they do not guarantee a
// later patch or feature band. Default when version is set is patch (official docs).
export function rollForwardReach(policy, pin, latest) {
  const p = sdkParts(pin), l = sdkParts(latest);
  if (!p || !l) return { guaranteed: false, reason: 'SDK 版本格式无法解析（需要 x.y.znn）' };
  const pol = policy || 'patch';
  if (p.version === l.version) return { guaranteed: true, reason: 'pin 已是该通道最新 SDK' };
  if (versionCompare(l, p) < 0) return { guaranteed: false, reason: `pin ${p.version} 高于该通道最新稳定 SDK ${l.version}（可能是 preview，metadata 不能确认）` };
  if (pol === 'disable') return { guaranteed: false, reason: 'rollForward: disable 要求精确匹配' };
  if (pol === 'latestMajor') return { guaranteed: true, reason: 'latestMajor 可选到已安装的最新 SDK' };
  if (pol === 'latestMinor') {
    if (l.major === p.major) return { guaranteed: true, reason: 'latestMinor 可在同一 major 内选到最新 minor/feature/patch' };
    return { guaranteed: false, reason: `latestMinor 不跨 major（pin ${p.major}.x，latest ${l.major}.${l.minor}）` };
  }
  if (pol === 'latestFeature') {
    if (l.major === p.major && l.minor === p.minor) return { guaranteed: true, reason: 'latestFeature 可在同一 major.minor 内选到最新 feature band/patch' };
    return { guaranteed: false, reason: `latestFeature 不跨 major.minor（pin ${p.major}.${p.minor}，latest ${l.major}.${l.minor}）` };
  }
  if (pol === 'latestPatch') {
    if (l.major === p.major && l.minor === p.minor && l.featureBand === p.featureBand) return { guaranteed: true, reason: 'latestPatch 可在同一 feature band 内选到最新 patch' };
    return { guaranteed: false, reason: `latestPatch 不跨 feature band（pin ${p.featureBand}xx，latest ${l.featureBand}xx）` };
  }
  return { guaranteed: false, reason: `rollForward: ${pol} 只在精确版本/band 缺失时回退，不保证选到最新 SDK` };
}

export function normalizeMetadata(json) {
  const j = json && typeof json === 'object' && !Array.isArray(json) ? json : {};
  const releases = Array.isArray(j.releases) ? j.releases : [];
  const sdkVersions = [...new Set(releases.flatMap(r => Array.isArray(r?.sdks) ? r.sdks.map(s => s?.version).filter(v => typeof v === 'string') : []))];
  const str = v => typeof v === 'string' && v.trim() ? v.trim() : null;
  return {
    latestSdk: str(j['latest-sdk']),
    latestRelease: str(j['latest-release']),
    latestRuntime: str(j['latest-runtime']),
    supportPhase: str(j['support-phase']),
    eolDate: str(j['eol-date']),
    sdkVersions,
  };
}

const lineOf = (text, index) => (index == null ? null : String(text).slice(0, index).split('\n').length);

export function analyzeDotnet({ projects = [], globalJsons = [], metadata = {}, workflows = [], now = new Date().toISOString(), offline = false } = {}) {
  const framework = [], ci = [], warnings = [], incomplete = [];
  const channels = new Map();
  const projectFacts = [];

  for (const p of projects) {
    const tfms = (p.tfms ?? []).map(tfmInfo);
    for (const t of tfms) {
      if (t.kind !== 'runtime' || !t.channel) continue;
      const c = channels.get(t.channel) ?? { channel: t.channel, projects: [], tfms: [] };
      if (!c.projects.includes(p.file)) c.projects.push(p.file);
      if (!c.tfms.includes(t.tfm)) c.tfms.push(t.tfm);
      channels.set(t.channel, c);
    }
    for (const t of tfms.filter(t => t.kind === 'unknown')) incomplete.push(`${p.file}: 无法识别 TFM ${t.tfm}；支持期未知。`);
    if (!tfms.length && !(p.unresolved ?? []).length) incomplete.push(`.NET 项目 ${p.file}: 未找到 TargetFramework/TargetFrameworks（旧式项目？）`);
    if ((p.unresolved ?? []).length) incomplete.push(`.NET 项目 ${p.file}: TFM 含 MSBuild 属性 ${p.unresolved.join(', ')}，静态扫描无法求值；用 \`dotnet msbuild -getProperty:TargetFramework\` 核验。`);
    projectFacts.push({ file: p.file, tfms, unresolved: p.unresolved ?? [], globalJson: p.globalJson ?? null, propsFile: p.propsFile ?? null });
  }

  for (const c of channels.values()) {
    const meta = metadata[c.channel] ?? null;
    const fact = { channel: c.channel, projects: c.projects, tfms: c.tfms, supportPhase: null, eolDate: null, latestSdk: null, latestRelease: null, latestRuntime: null, source: metadataUrl(c.channel) };
    if (!meta) {
      if (offline) warnings.push(`.NET ${c.channel}: offline，未取支持期/EOL 与最新 SDK；联网重跑。`);
      else incomplete.push(`.NET ${c.channel}: 未取得 release metadata（通道可能已停止发布或网络失败）；支持期/EOL 未知。`);
      channels.set(c.channel, fact);
      continue;
    }
    Object.assign(fact, { supportPhase: meta.supportPhase, eolDate: meta.eolDate, latestSdk: meta.latestSdk, latestRelease: meta.latestRelease, latestRuntime: meta.latestRuntime ?? meta.latestRelease });
    const eol = Date.parse(meta.eolDate), today = Date.parse(now);
    const days = Number.isFinite(eol) && Number.isFinite(today) ? Math.ceil((eol - today) / 86400000) : null;
    const where = c.projects.join(', ');
    if (days !== null && days <= 0) framework.push({ id: 'dotnet-runtime-eol', severity: 'P0', confidence: 'confirmed', file: c.projects[0], line: null,
      detail: `${c.tfms.join('/')} 对应的 .NET ${c.channel} 已于 ${meta.eolDate} 结束支持；不再接收安全补丁。项目：${where}。`,
      fix: '先选定仍受支持的 LTS/STS，再把 TargetFramework、global.json、setup-dotnet 与发布脚本一起改；EOL 运行时不因重新构建而获得补丁。', source: fact.source });
    else if (days !== null && days <= 90) framework.push({ id: 'dotnet-runtime-eol-soon', severity: 'P1', confidence: 'confirmed', file: c.projects[0], line: null,
      detail: `.NET ${c.channel} 将在 ${days} 天后（${meta.eolDate}）结束支持；项目：${where}。`, fix: '在 EOL 前完成升级计划；EOL 后不再有安全补丁。', source: fact.source });
    else if (meta.supportPhase === 'maintenance') framework.push({ id: 'dotnet-runtime-maintenance', severity: 'P2', confidence: 'confirmed', file: c.projects[0], line: null,
      detail: `.NET ${c.channel} 处于 maintenance（仅安全/关键修复），EOL ${meta.eolDate ?? '未知'}；项目：${where}。`, fix: '规划升级到当前 LTS；maintenance 期仍接收安全修复，但不再有新功能。', source: fact.source });
    else if (!meta.eolDate) warnings.push(`.NET ${c.channel}: metadata 没有 eol-date；支持期需手工核验。`);
    channels.set(c.channel, fact);
  }

  const globalFacts = [];
  for (const g of globalJsons) {
    const fact = { file: g.file, version: g.version ?? null, rollForward: g.rollForward ?? null, allowPrerelease: g.allowPrerelease ?? null,
      testRunner: g.testRunner ?? null, channel: null, latestSdk: null, latestRelease: null, guaranteedLatest: null, reason: null,
      projects: projects.filter(p => p.globalJson === g.file).map(p => p.file) };
    if (!g.version) {
      framework.push({ id: 'dotnet-sdk-version-missing', severity: 'notice', confidence: 'confirmed', file: g.file, line: null,
        detail: 'global.json 没有 sdk.version；SDK 解析为已安装的最高版本，本地与 CI 仍可能漂移。', fix: '写上完整 SDK 版本（x.y.znn），或删除 global.json 并显式依赖 setup-dotnet。' });
      globalFacts.push(fact);
      continue;
    }
    const pin = sdkParts(g.version);
    if (!pin) {
      framework.push({ id: 'dotnet-sdk-invalid', severity: 'P2', confidence: 'confirmed', file: g.file, line: null,
        detail: `global.json 的 sdk.version "${g.version}" 不是完整 SDK 版本（需要 x.y.znn，如 10.0.100）。`, fix: '改成完整版本；不要写 10、10.0 或 10.0.x。' });
      globalFacts.push(fact);
      continue;
    }
    fact.channel = `${pin.major}.${pin.minor}`;
    const meta = metadata[fact.channel] ?? null;
    if (meta) {
      fact.latestSdk = meta.latestSdk;
      fact.latestRelease = meta.latestRelease;
      if (meta.latestSdk) {
        const reach = rollForwardReach(g.rollForward, g.version, meta.latestSdk);
        fact.guaranteedLatest = reach.guaranteed;
        fact.reason = reach.reason;
        if (!reach.guaranteed) framework.push({ id: 'dotnet-sdk-pin-behind', severity: 'P2', confidence: 'confirmed', file: g.file, line: null,
          detail: `global.json 钉 ${g.version}（rollForward ${g.rollForward ?? '默认 patch'}），${fact.channel} 最新 SDK 是 ${meta.latestSdk}：${reach.reason}。`,
          fix: '要自动拿到补丁就改用 latestFeature（同一 major.minor）或 latestMajor，或抬 pin；若这是有意的下限，请记录复查条件。', source: metadataUrl(fact.channel) });
      }
      if (meta.sdkVersions.length && !meta.sdkVersions.includes(pin.version))
        warnings.push(`${g.file}: SDK ${pin.version} 不在 ${fact.channel} 的 release 索引中；可能是 preview/已下架，需在目标机器核验。`);
    } else if (offline) warnings.push(`${g.file}: offline，未取 ${fact.channel} 最新 SDK，无法判断 rollForward 能否到最新。`);
    else incomplete.push(`${g.file}: 未取得 ${fact.channel} release metadata，无法判断 SDK 是否落后/可解析。`);
    for (const p of projects.filter(x => x.globalJson === g.file)) {
      for (const t of (p.tfms ?? []).map(tfmInfo)) {
        if (t.kind !== 'runtime') continue;
        if (t.major < pin.major || (t.major === pin.major && t.minor <= pin.minor)) continue;
        const policy = (g.rollForward || 'patch').toLowerCase();
        const canCross = ['major', 'latestmajor'].includes(policy)
          || (t.major === pin.major && ['minor', 'latestminor'].includes(policy));
        if (canCross) {
          warnings.push(`${p.file}: ${g.file} 的 ${g.rollForward} 允许选择可编译 ${t.tfm} 的已安装 SDK。在构建目录运行 dotnet --version 确认。`);
        } else {
          framework.push({ id: 'dotnet-sdk-cannot-target', severity: 'P0', confidence: 'confirmed', file: p.file, line: null,
            detail: `项目 TargetFramework 是 ${t.tfm}，但最近的 ${g.file} 把 SDK 钉在 ${g.version}（${pin.major}.${pin.minor}）；旧 SDK 不能编译更新的 TFM，构建会失败或落到意外 SDK。`,
            fix: '把 global.json、TargetFramework、setup-dotnet 和发布 profile 作为一次改动同步；.NET SDK 只能 target 同一或更低的 TFM。' });
        }
      }
    }
    globalFacts.push(fact);
  }
  if (projects.length && !globalJsons.length) framework.push({ id: 'dotnet-no-global-json', severity: 'notice', confidence: 'confirmed', file: projects[0].file, line: null,
    detail: '仓库没有 global.json：本地 SDK 取已安装的最高版本，CI 取 runner 的默认 SDK；同一 TFM 可能在不同机器上用到不同 SDK。', fix: '加 global.json（GA 基线 + latestFeature，或最新补丁），CI 用 setup-dotnet 的 global-json-file；不要同时写 dotnet-version。' });

  for (const w of workflows) {
    const t = stripComments(String(w.text ?? ''));
    const jobs = jobBlocks(t);
    for (const job of jobs.length ? jobs : [{ text: t, offset: 0 }]) {
      const steps = [...job.text.matchAll(/^([ \t]*)- +(?:uses|name|id|if|run|shell|env|with|continue-on-error|timeout-minutes|working-directory):/gm)];
      let configured = false;
      for (const [i, step] of steps.entries()) {
        const block = job.text.slice(step.index, steps[i + 1]?.index);
        const setup = /\buses:\s*['"]?actions\/setup-dotnet@/.exec(block);
        if (!setup) continue;
        configured = true;
        const line = lineOf(t, job.offset + step.index + setup.index);
        const hasGlobalFile = /\bglobal-json-file\s*:/.test(block);
        const hasVersion = /\bdotnet-version\s*:/.test(block);
        const where = { confidence: 'heuristic', file: w.file, line };
        if (hasGlobalFile && hasVersion) ci.push({ ...where, id: 'dotnet-version-two-sources', severity: 'P1',
          detail: '同一 setup-dotnet 步骤同时配置 global-json-file 和 dotnet-version，action 会安装两者。',
          fix: '核对是否有意测试多个 SDK；单版本构建可保留 global-json-file。' });
        else if (hasVersion && globalJsons.length) ci.push({ ...where, id: 'dotnet-version-shadows-global-json', severity: 'P1',
          detail: 'setup-dotnet 指定安装版本，仓库另有 global.json；CLI 仍按运行目录解析 SDK。',
          fix: '在构建目录运行 dotnet --version；单版本构建可让 setup-dotnet 读取对应的 global.json。' });
        else if (!hasGlobalFile && !hasVersion) ci.push({ ...where, id: 'dotnet-setup-without-version', severity: 'P2',
          detail: 'setup-dotnet 没有指定要安装的 SDK 版本或 global.json。', fix: '核对 runner 的 SDK 来源。' });
      }
      if (!configured && globalJsons.length && projects.length && /\bdotnet\s+(?:build|test|publish|restore|pack|run|msbuild)\b/i.test(job.text))
        ci.push({ id: 'dotnet-ci-setup-missing', severity: 'P2', confidence: 'heuristic', file: w.file, line: lineOf(t, job.offset),
          detail: '该 job 调用 dotnet，未看到 setup-dotnet；SDK 可能由镜像或复用步骤提供。',
          fix: '核对该 job 的 SDK 来源与构建目录中的 dotnet --version。' });
    }
  }

  const order = { P0: 0, P1: 1, P2: 2, notice: 3 };
  framework.sort((a, b) => order[a.severity] - order[b.severity] || String(a.file).localeCompare(String(b.file)));
  ci.sort((a, b) => order[a.severity] - order[b.severity] || String(a.file).localeCompare(String(b.file)));
  return { detected: projects.length > 0, projects: projectFacts, globalJson: globalFacts, channels: [...channels.values()], framework, ci, warnings, incomplete };
}
