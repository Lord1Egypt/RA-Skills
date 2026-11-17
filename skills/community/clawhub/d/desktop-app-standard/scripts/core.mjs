import fs from 'node:fs';
import path from 'node:path';

export const TOOL_VERSION = '0.9.22';
export const exact = v => typeof v === 'string' && /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/.test(v) && v.split('.').every(n => Number.isSafeInteger(Number(n))) ? v : null;
export function compare(a, b) {
  if (!exact(a) || !exact(b)) return null;
  const x = a.split('.').map(Number), y = b.split('.').map(Number);
  for (let i = 0; i < 3; i++) if (x[i] !== y[i]) return Math.sign(x[i] - y[i]);
  return 0;
}
export function stableMax(values) {
  return values.filter(exact).sort((a, b) => compare(b, a))[0] ?? null;
}
export const minor = v => exact(v) ? v.split('.').slice(0, 2).join('.') : null;
export const slash = p => p.split(path.sep).join('/');
export function walk(root, maxFiles = 6000) {
  const files = [], skipped = [], excluded = new Set(['.git', 'node_modules', 'target', 'dist', 'build', '.next', 'out', 'coverage', '.venv', 'vendor']);
  let limited = false;
  function visit(dir, depth = 0) {
    if (depth > 12) { skipped.push(slash(path.relative(root, dir)) + ': depth limit'); limited = true; return; }
    // One unreadable directory — a root-owned folder, a Windows deny-ACL dir, an
    // unsynced cloud placeholder — must not abort the whole audit. Skip it and
    // keep going, so the rest of the project is still reported.
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name));
    } catch (e) {
      skipped.push(slash(path.relative(root, dir)) + ': unreadable (' + (e.code || e.message) + ')');
      return;
    }
    for (const entry of entries) {
      if (excluded.has(entry.name)) continue;
      if (files.length >= maxFiles) { limited = true; return; }
      const p = path.join(dir, entry.name);
      if (entry.isSymbolicLink()) { skipped.push(slash(path.relative(root, p)) + ': symlink'); continue; }
      if (entry.isDirectory()) visit(p, depth + 1);
      else if (entry.isFile()) files.push(slash(path.relative(root, p)));
    }
  }
  visit(root);
  return { files, limited, skipped, excluded: [...excluded] };
}
export function read(root, file, maxBytes = 4_000_000) {
  const p = path.join(root, file);
  if (fs.statSync(p).size > maxBytes) return null;
  // Windows editors write UTF-8 with a BOM, and a BOM is not valid JSON. Strip it
  // here so every consumer sees the same text the author wrote.
  return fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '');
}

// ---------------------------------------------------------------------------
// JSON5
// ---------------------------------------------------------------------------
/**
 * Minimal JSON5 reader, because Tauri v2 accepts tauri.conf.json5 and the skill ships
 * no dependencies. It handles exactly what such a config uses — comments, single-quoted
 * strings, unquoted keys, trailing commas — and returns null for anything else.
 *
 * A null result must never be read as "no problem found": the caller reports the file
 * as unreadable so the checks it would have driven stay visible instead of failing open.
 */
export function parseJson5(source) {
  // A UTF-8 BOM (Windows editors) is not valid JSON5 either; drop it before parsing.
  const src = String(source ?? '').replace(/^\uFEFF/, '');
  let out = '';
  let i = 0;
  const n = src.length;
  const isIdent = c => /[A-Za-z0-9_$]/.test(c);
  const dropTrailingComma = () => {
    let k = out.length - 1;
    while (k >= 0 && /\s/.test(out[k])) k--;
    if (k >= 0 && out[k] === ',') out = out.slice(0, k) + out.slice(k + 1);
  };
  while (i < n) {
    const c = src[i];
    if (c === '/' && src[i + 1] === '/') { while (i < n && src[i] !== '\n') i++; continue; }
    if (c === '/' && src[i + 1] === '*') {
      i += 2;
      while (i < n && !(src[i] === '*' && src[i + 1] === '/')) i++;
      i += 2;
      continue;
    }
    if (c === '"' || c === "'") {
      const quote = c;
      let s = '';
      i++;
      while (i < n) {
        const ch = src[i];
        if (ch === '\\') {
          const next = src[i + 1] ?? '';
          // \' only means anything inside single quotes; in a double-quoted JSON
          // string it is an invalid escape.
          s += quote === "'" && next === "'" ? "'" : ch + next;
          i += 2;
          continue;
        }
        if (ch === quote) { i++; break; }
        s += ch;
        i++;
      }
      out += quote === "'" ? '"' + s.replace(/"/g, '\\"') + '"' : '"' + s + '"';
      continue;
    }
    if (c === '}' || c === ']') { dropTrailingComma(); out += c; i++; continue; }
    if (isIdent(c) && !/[\w$]/.test(out[out.length - 1] ?? '')) {
      let j = i;
      while (j < n && isIdent(src[j])) j++;
      let k = j;
      while (k < n && /\s/.test(src[k])) k++;
      if (src[k] === ':') { out += '"' + src.slice(i, j) + '"'; i = j; continue; }
      out += src.slice(i, j);
      i = j;
      continue;
    }
    out += c;
    i++;
  }
  try { return JSON.parse(out); } catch { return null; }
}
export function cargoPackages(text) {
  const out = [];
  for (const block of text.split(/^\[\[package\]\]\s*$/m).slice(1)) {
    const name = /^name\s*=\s*"([^"]+)"/m.exec(block)?.[1];
    const version = /^version\s*=\s*"([^"]+)"/m.exec(block)?.[1];
    const source = /^source\s*=\s*"([^"]+)"/m.exec(block)?.[1] ?? 'workspace/path';
    if (name && version) out.push({ name, version, source });
  }
  return out;
}
export function workflowHints(file, text, lockPresent) {
  const actions = [];
  text.split(/\r?\n/).forEach((line, i) => {
    if (/^\s*#/.test(line)) return;
    // A deliberately limited line scanner, NOT a YAML parser. Never assert job semantics.
    const m = /^\s*(?:-\s*)?uses:\s*["']?([\w.-]+\/[\w.-]+(?:\/[\w./-]+)?)@([^\s"'#]+)["']?/.exec(line);
    if (!m) return;
    const [, action, ref] = m;
    actions.push({ file, line: i + 1, action, repository: action.split('/').slice(0, 2).join('/'), ref,
      immutableReference: /^[a-f0-9]{40}$/i.test(ref), lockfilePresent: lockPresent });
  });
  return { actions };
}
export function usageHints(files, body) {
  // Only code-shaped tokens: no generic keyword matching, and no automatic applicability verdict.
  const tokens = [...new Set([...body.matchAll(/`([A-Za-z_$][\w$]*(?:(?:::|\.)[\w$]+)*(?:\(\))?)`/g)].map(m => m[1].replace(/\(\)$/, '')))].filter(t => t.length >= 4).slice(0, 40);
  const hits = [];
  for (const { file, text } of files) {
    for (const token of tokens) {
      const i = text.indexOf(token);
      if (i >= 0) { hits.push({ file, line: text.slice(0, i).split('\n').length, token }); break; }
    }
    if (hits.length >= 12) break;
  }
  return { tokens, hits, applicability: 'unverified' };
}
export async function requestJson(url, { token, fetchImpl = fetch, raw = false, allow404 = false } = {}) {
  const u = new URL(url);
  if (u.protocol !== 'https:' || !['api.github.com', 'registry.npmjs.org', 'crates.io', 'releases.electronjs.org', 'builds.dotnet.microsoft.com', 'raw.githubusercontent.com'].includes(u.hostname)) throw new Error('拒绝非白名单请求');
  const headers = { 'User-Agent': `desktop-app-standard/${TOOL_VERSION}`, Accept: 'application/json' };
  if (u.hostname === 'registry.npmjs.org') headers.Accept = 'application/vnd.npm.install-v1+json, application/json';
  // Never leak a GitHub token to npm, crates, release assets, or redirects.
  if (u.hostname === 'api.github.com') {
    headers.Accept = raw ? 'application/vnd.github.raw' : 'application/vnd.github+json';
    if (token) headers.Authorization = `Bearer ${token}`;
  }
  for (let attempt = 0; attempt < 2; attempt++) {
    const res = await fetchImpl(url, { headers, redirect: 'error', signal: AbortSignal.timeout(20000) });
    if (res.status >= 500 && attempt === 0) { await new Promise(r => setTimeout(r, 400)); continue; }
    if (allow404 && res.status === 404) return null;
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${u.hostname}${u.pathname}${res.status === 403 || res.status === 429 ? '（可能限流；结果未知，不是已最新）' : ''}`);
    return raw ? res.text() : res.json();
  }
}
export async function releaseHistory(repo, tagPattern, floor, maxPages, get, expectedVersions = null) {
  const releases = [];
  let reachedFloor = false, exhausted = false;
  const missing = expectedVersions === null ? null : new Set(expectedVersions);
  const visited = [];
  for (let page = 1; page <= maxPages; page++) {
    const url = `https://api.github.com/repos/${repo}/releases?per_page=100&page=${page}`;
    visited.push(url);
    const data = await get(url);
    if (!Array.isArray(data)) throw new Error('release API 未返回数组');
    for (const r of data) {
      const m = tagPattern.exec(r.tag_name ?? '');
      if (!m || !exact(m[1]) || r.draft || r.prerelease) continue;
      if (floor && m[1] === floor) reachedFloor = true;
      missing?.delete(m[1]);
      releases.push({ tag: r.tag_name, version: m[1], publishedAt: r.published_at, url: r.html_url, body: r.body ?? '' });
    }
    if (data.length < 100) { exhausted = true; break; }
    // Release order is publication time, NOT semver. Older-major backports must not stop scanning.
    if (missing !== null && missing.size === 0) break;
  }
  return { releases, visited, reachedFloor, exhausted,
    missingVersions: missing === null ? null : [...missing],
    truncated: missing !== null ? missing.size > 0 : !exhausted,
    coverage: !floor ? 'no-local-exact-version' : missing !== null ? (missing.size === 0 ? 'official-known-interval-covered' : 'official-interval-incomplete') : exhausted ? 'release-history-exhausted' : 'page-limit-without-version-index' };
}

// ---------------------------------------------------------------------------
// Lockfile readers. Deliberately small, read-only, dependency-free parsers.
// They only extract name -> resolved version; they never run a package manager.
// ---------------------------------------------------------------------------
export const LOCKFILES = ['package-lock.json', 'npm-shrinkwrap.json', 'yarn.lock', 'pnpm-lock.yaml', 'bun.lock', 'bun.lockb'];
const unquote = s => s.trim().replace(/^(['"])(.*)\1$/, '$2');
const specName = spec => { const i = spec.indexOf('@', 1); return i > 0 ? [spec.slice(0, i), spec.slice(i + 1)] : [spec, '']; };

/** yarn classic (v1) and berry (v2+) lockfiles. */
export function parseYarnLock(text) {
  const flavor = /^__metadata:/m.test(text) ? 'berry' : 'classic';
  const entries = [];
  let cur = null;
  for (const line of text.split(/\r?\n/)) {
    if (!line.trim() || line.startsWith('#')) continue;
    if (!/^\s/.test(line) && line.trimEnd().endsWith(':')) {
      const header = line.trimEnd().slice(0, -1);
      cur = { specs: header.split(/,\s*/).map(unquote), version: null };
      entries.push(cur); continue;
    }
    const m = cur && /^ {2}version:?\s+"?([^"\s]+)"?\s*$/.exec(line);
    if (m) cur.version = m[1];
  }
  const out = [];
  for (const e of entries) {
    if (!e.version || e.specs[0] === '__metadata') continue;
    for (const spec of e.specs) {
      const [name, rawRange] = specName(spec);
      if (!name || !rawRange) continue;
      const protocol = /^(npm|workspace|patch|file|link|portal|git\+?\w*|github|https?):/.exec(rawRange)?.[1] ?? (flavor === 'classic' ? 'npm' : 'unknown');
      const range = rawRange.replace(/^npm:/, '');
      out.push({ name, range, version: e.version, protocol });
    }
  }
  return { flavor, entries: out };
}

/** pnpm-lock.yaml v6-v9 importers (and the legacy single-project top-level layout). */
export function parsePnpmLock(text) {
  const importers = {};
  const hasImporters = /^importers:\s*$/m.test(text);
  const depTypes = /^(dependencies|devDependencies|optionalDependencies):$/;
  let section = null, importer = null, depType = null, dep = null;
  const keyLine = /^(?:'([^']+)'|"([^"]+)"|([^:\s][^:]*?)):\s*(.*)$/;
  const setVersion = (imp, name, raw) => {
    const version = String(raw).replace(/\(.*$/, '').trim();
    (importers[imp] ??= {})[name] = version;
  };
  for (const line of text.split(/\r?\n/)) {
    if (!line.trim() || /^\s*#/.test(line)) continue;
    const indent = line.match(/^ */)[0].length, content = line.trim();
    if (indent === 0) {
      section = content.replace(/:.*$/, ''); dep = null;
      depType = !hasImporters && depTypes.test(content) ? section : null; importer = hasImporters ? null : '.';
      continue;
    }
    const base = hasImporters ? 4 : 0;
    if (hasImporters && section !== 'importers') continue;
    if (hasImporters && indent === 2) { importer = unquote(content.replace(/:\s*$/, '')); importers[importer] ??= {}; depType = null; continue; }
    if (hasImporters && indent === 4) { depType = depTypes.test(content) ? content.slice(0, -1) : null; dep = null; continue; }
    if (!depType || importer === null) continue;
    const m = keyLine.exec(content); if (!m) continue;
    const key = m[1] ?? m[2] ?? m[3], value = m[4];
    if (indent === base + 2) { dep = key; if (value && !/^\{/.test(value)) setVersion(importer, key, unquote(value)); }
    else if (indent === base + 4 && dep && key === 'version') setVersion(importer, dep, unquote(value));
  }
  return { importers };
}

/** Text bun.lock (JSONC-like). bun.lockb is binary and reported as unreadable. */
export function parseBunLock(text) {
  const json = JSON.parse(text.replace(/,(\s*[}\]])/g, '$1'));
  const packages = {};
  for (const [key, value] of Object.entries(json.packages ?? {})) {
    const id = Array.isArray(value) ? String(value[0]) : '';
    const at = id.lastIndexOf('@');
    if (at > 0) packages[key] = id.slice(at + 1);
  }
  return { packages, workspaces: json.workspaces ?? {} };
}

/**
 * macOS packaging targets from an electron-builder config.
 * Line heuristics, NOT a YAML parser — same honesty rule as the workflow scanner.
 * Returns null when the mac block or its target list cannot be found.
 */
export function macTargetsFromBuilder(text) {
  if (!text) return null;
  const targets = [];
  let inMac = false, macIndent = 0, inTarget = false, targetIndent = 0;
  for (const line of text.split(/\r?\n/)) {
    const indent = line.length - line.trimStart().length;
    const t = line.trim();
    if (!t || t.startsWith('#')) continue;
    if (/^mac:/.test(t)) {
      // Flow style (mac: { target: [...] }) is not parsed on purpose; report null
      // rather than guess.
      inMac = !/^mac:\s*\{/.test(t);
      macIndent = indent;
      inTarget = false;
      continue;
    }
    if (!inMac) continue;
    if (indent <= macIndent) { inMac = false; inTarget = false; continue; }
    const scalar = /^target:\s*['"]?([\w-]+)['"]?$/.exec(t);
    if (scalar) { targets.push(scalar[1]); inTarget = false; continue; }
    const inline = /^target:\s*\[(.*)\]\s*$/.exec(t);
    if (inline) {
      targets.push(...inline[1].split(',').map(s => s.trim().replace(/^['"]|['"]$/g, '')).filter(Boolean));
      inTarget = false;
      continue;
    }
    if (/^target:\s*$/.test(t)) { inTarget = true; targetIndent = indent; continue; }
    if (inTarget) {
      if (indent > targetIndent && /^-\s*/.test(t)) {
        targets.push(t.replace(/^-\s*/, '').replace(/^['"]|['"]$/g, '').trim());
        continue;
      }
      if (indent <= targetIndent) inTarget = false;
    }
  }
  return targets.length ? targets : null;
}

/**
 * macOS packaging targets from a workflow's electron-builder CLI arguments.
 * `--mac dmg zip --x64` → ['dmg','zip']. Returns null when the workflow does not
 * pass --mac, or passes it without target names (then the config decides).
 */
export function macTargetsFromArgs(text) {
  if (!text) return null;
  for (const match of text.matchAll(/(?:^|[\s'"])--mac\b([^\r\n'"]*)/gm)) {
    const targets = [];
    for (const token of match[1].trim().split(/\s+/)) {
      if (!/^[\w][\w-]*$/.test(token)) break;
      targets.push(token);
    }
    if (targets.length) return targets;
  }
  return null;
}

/** Resolve one manifest dependency against a parsed lockfile. Returns {version, locator, candidates}. */
export function resolveFromLock(kind, lock, { name, declared, importerPath }) {
  if (kind === 'yarn') {
    const rows = lock.entries.filter(e => e.name === name);
    const hit = rows.find(e => e.range === declared || e.range === `npm:${declared}`);
    if (hit) return { version: hit.version, locator: `${name}@${hit.range}`, candidates: [hit.version] };
    const versions = [...new Set(rows.map(e => e.version))];
    return { version: null, locator: null, candidates: versions };
  }
  if (kind === 'pnpm') {
    const v = lock.importers[importerPath || '.']?.[name] ?? null;
    return { version: v, locator: v ? `importers.${importerPath || '.'}.${name}` : null, candidates: v ? [v] : [] };
  }
  if (kind === 'bun') {
    const key = importerPath && importerPath !== '.' && lock.packages[`${importerPath}/${name}`] ? `${importerPath}/${name}` : name;
    const v = lock.packages[key] ?? null;
    return { version: v, locator: v ? `packages.${key}` : null, candidates: v ? [v] : [] };
  }
  return { version: null, locator: null, candidates: [] };
}

// ---------------------------------------------------------------------------
// Upstream helpers
// ---------------------------------------------------------------------------
/** Electron policy: the latest three stable majors are supported. Computed from the official index. */
export function electronSupportedMajors(versions) {
  return [...new Set(versions.filter(exact).map(v => Number(v.split('.')[0])))].sort((a, b) => b - a).slice(0, 3);
}

/** Node phases from the official nodejs/Release schedule. Active LTS is the window between lts and maintenance. */
export function nodeSupportFacts(schedule, now = new Date()) {
  const today = (typeof now === 'string' ? now : now.toISOString()).slice(0, 10);
  const lines = Object.entries(schedule ?? {})
    .filter(([key, value]) => /^v\d+$/.test(key) && value && typeof value === 'object')
    .map(([key, value]) => ({ major: Number(key.slice(1)), start: value.start ?? null, lts: value.lts ?? null,
      maintenance: value.maintenance ?? null, end: value.end ?? null }))
    .sort((a, b) => b.major - a.major)
    .map(l => ({ ...l, phase: !l.end ? 'unknown' : today >= l.end ? 'eol' : l.maintenance && today >= l.maintenance ? 'maintenance'
      : l.lts && today >= l.lts ? 'active' : l.start && today >= l.start ? 'current' : 'future' }));
  const released = lines.filter(l => ['active', 'maintenance', 'current'].includes(l.phase));
  const latestLts = released.find(l => l.lts) ?? null;
  const activeLts = lines.find(l => l.phase === 'active') ?? null;
  return { today, activeLts: activeLts?.major ?? null, latestLts: latestLts?.major ?? null,
    latestLtsStart: latestLts?.lts ?? null, lines };
}

/** Classify a release body by its own headings. A hint for triage, not a verdict on this app. */
export function classifyNotes(body = '') {
  const headings = [...body.matchAll(/^#{2,4}\s*(.+)$/gm)].map(m => m[1].toLowerCase());
  const has = re => headings.some(h => re.test(h));
  const categories = [];
  if (has(/breaking|removed|deprecat|behavio(u)?r chang/) || /end of support for|BREAKING CHANGE/i.test(body) || /^[*-]\s*\w+(\([^)]*\))?!:/m.test(body)) categories.push('breaking');
  if (has(/security/) || /\b(CVE-\d{4}-\d+|GHSA-[\w-]+)\b/.test(body)) categories.push('security');
  if (has(/feature|enhancement|performance|new api|additions?/) || /^[*-]\s*(feat|perf)(\(|:)/m.test(body)) categories.push('feature');
  if (has(/fix|bug/) || /^[*-]\s*fix(\(|:)/m.test(body)) categories.push('fix');
  if (!headings.length && /^[*-]\s/m.test(body)) { // flat bullet changelogs (Tauri plugins-workspace)
    if (/\*\*breaking|\bbreaking change|\bremoved?\b|\bdeprecat/i.test(body) && !categories.includes('breaking')) categories.push('breaking');
    if (/\b(add(s|ed)?|new|support(s)? for|expose[sd]?)\b/i.test(body)) categories.push('feature');
    if (/\b(fix(es|ed)?|no longer|prevent(s|ed)?|correct(ly|ed)?)\b/i.test(body)) categories.push('fix');
  }
  const suggestedPriority = categories.includes('breaking') || categories.includes('security') ? 'P0-candidate'
    : categories.includes('feature') ? 'P1-candidate' : categories.includes('fix') ? 'P2-candidate' : 'unclassified';
  return { categories, suggestedPriority };
}

/** Split a Keep-a-Changelog style file (Tauri plugins-workspace) into version sections. */
export function changelogSections(md = '') {
  const out = [];
  const re = /^##\s*\\?\[?v?(\d+\.\d+\.\d+)\]?.*$/gm;
  const marks = [...md.matchAll(re)];
  marks.forEach((m, i) => out.push({ version: m[1], body: md.slice(m.index + m[0].length, marks[i + 1]?.index ?? md.length).trim() }));
  return out;
}

/** Extract the numeric version that a ref/tag names: v4, v4.2, action-v1.0.0, electron-builder@26.0.0. */
export function refVersion(ref = '') {
  const m = /(\d+)(?:\.(\d+))?(?:\.(\d+))?$/.exec(String(ref));
  return m ? { major: Number(m[1]), minor: m[2] === undefined ? null : Number(m[2]), patch: m[3] === undefined ? null : Number(m[3]) } : null;
}

/** Actions that create releases, upload what users install, or mint attestations: treat as write-capable. */
export const WRITE_CAPABLE_ACTIONS = new Set(['tauri-apps/tauri-action', 'softprops/action-gh-release', 'ncipollo/release-action',
  'actions/attest-build-provenance', 'actions/attest', 'actions/create-release', 'actions/upload-release-asset', 'svenstaro/upload-release-action',
  'samuelmeuli/action-electron-builder', 'vedantmgoyal9/winget-releaser', 'peter-evans/repository-dispatch', 'peter-evans/create-pull-request']);
