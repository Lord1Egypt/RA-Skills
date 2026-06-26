#!/usr/bin/env node
// Check and update this skill from a remote manifest.
//
// Usage:
//   node scripts/skill_update.mjs --check
//   node scripts/skill_update.mjs --yes
//   node scripts/skill_update.mjs --sync
//
// Required:
//   CV_SKILL_UPDATE_MANIFEST_URL=https://.../creator-scraper-cv.manifest.json
//
// Manifest shape:
// {
//   "name": "creator-scraper-cv",
//   "latest_version": "0.9.1",
//   "min_supported_version": "0.8.0",
//   "release_notes": ["..."],
//   "files": [
//     {"path": "SKILL.md", "url": "https://...", "sha256": "..."}
//   ]
// }

import { createHash } from 'node:crypto';
import {
  existsSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  renameSync,
  rmdirSync,
  rmSync,
  statSync,
  writeFileSync,
} from 'node:fs';
import { dirname, isAbsolute, join, normalize, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const skillRoot = resolve(scriptDir, '..');
const skillMetaPath = join(skillRoot, 'skill.json');
const skillMdPath = join(skillRoot, 'SKILL.md');
const defaultManifestUrl = 'https://raw.githubusercontent.com/creativault/skills/main/creator-scraper-cv/skill-manifest.json';

function readJSON(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}

function readSkillVersionFromMarkdown() {
  try {
    const skillMd = readFileSync(skillMdPath, 'utf8');
    const versionMatch = skillMd.match(/version:\s*"?([^"\n]+)"?/);
    return versionMatch?.[1]?.trim() || 'unknown';
  } catch {
    return 'unknown';
  }
}

function readSkillMeta() {
  if (existsSync(skillMetaPath)) {
    return readJSON(skillMetaPath);
  }
  return {
    name: 'creator-scraper-cv',
    version: readSkillVersionFromMarkdown(),
    channel: 'stable',
    update: {
      manifest_url: defaultManifestUrl,
      manifest_url_env: 'CV_SKILL_UPDATE_MANIFEST_URL',
      auto_update_env: 'CV_SKILL_AUTO_UPDATE',
    },
  };
}

function compareVersion(a, b) {
  const left = String(a || '0').split('.').map((part) => Number.parseInt(part, 10) || 0);
  const right = String(b || '0').split('.').map((part) => Number.parseInt(part, 10) || 0);
  const length = Math.max(left.length, right.length);
  for (let index = 0; index < length; index += 1) {
    const diff = (left[index] || 0) - (right[index] || 0);
    if (diff !== 0) return diff > 0 ? 1 : -1;
  }
  return 0;
}

function sha256(text) {
  return createHash('sha256').update(text).digest('hex');
}

function sha256LocalFile(path) {
  return sha256(readFileSync(path, 'utf8').replace(/\r\n/g, '\n'));
}

function assertSafeRelativePath(path) {
  const normalized = normalize(path).replaceAll('\\', '/');
  if (
    !normalized ||
    isAbsolute(normalized) ||
    normalized.startsWith('..') ||
    normalized.includes('../') ||
    normalized.includes('/../') ||
    normalized === '.' ||
    resolve(skillRoot, normalized) === skillRoot
  ) {
    throw new Error(`Unsafe manifest file path: ${path}`);
  }
  return normalized;
}

function isSyncExcluded(relativePath) {
  const normalized = assertSafeRelativePath(relativePath);
  return (
    normalized.startsWith('.skill-backups/')
    || normalized.startsWith('.git/')
    || normalized.startsWith('node_modules/')
    || normalized.includes('/__pycache__/')
    || normalized.endsWith('/.DS_Store')
    || normalized.endsWith('/Thumbs.db')
    || normalized === '.env'
    || normalized.endsWith('/.env')
  );
}

function listLocalFiles(root, prefix = '') {
  if (!existsSync(root)) {
    return [];
  }

  const paths = [];
  for (const entry of readdirSync(root, { withFileTypes: true })) {
    const relativePath = prefix ? `${prefix}/${entry.name}` : entry.name;
    const normalized = assertSafeRelativePath(relativePath);
    if (isSyncExcluded(normalized)) {
      continue;
    }

    const fullPath = join(root, entry.name);
    if (entry.isDirectory()) {
      paths.push(...listLocalFiles(fullPath, normalized));
    } else if (entry.isFile()) {
      paths.push(normalized);
    }
  }
  return paths;
}

function getManagedRoots(manifest) {
  const roots = manifest.sync?.managed_roots;
  if (!Array.isArray(roots) || roots.length === 0) {
    return [];
  }
  return roots.map((root) => {
    if (root === '.') {
      return '.';
    }
    return assertSafeRelativePath(root);
  });
}

function listMissingLocalFiles(manifestFiles, managedRoots) {
  if (managedRoots.length === 0) {
    return [];
  }

  const remotePaths = new Set(manifestFiles);
  const localPaths = [];
  for (const root of managedRoots) {
    const fullRoot = root === '.' ? skillRoot : join(skillRoot, root);
    const prefix = root === '.' ? '' : root;
    localPaths.push(...listLocalFiles(fullRoot, prefix));
  }

  return [...new Set(localPaths)]
    .filter((path) => !remotePaths.has(path))
    .filter((path) => !isSyncExcluded(path))
    .sort((left, right) => left.localeCompare(right));
}

function backupAndRemoveFile(relativePath, backupRoot) {
  const target = join(skillRoot, relativePath);
  if (!existsSync(target) || !statSync(target).isFile()) {
    return false;
  }

  const backup = join(backupRoot, relativePath);
  mkdirSync(dirname(backup), { recursive: true });
  renameSync(target, backup);
  return true;
}

function pruneEmptyDirectories(startDir) {
  if (!existsSync(startDir) || startDir === skillRoot) {
    return;
  }

  let current = startDir;
  while (current !== skillRoot && existsSync(current)) {
    const entries = readdirSync(current);
    if (entries.length > 0) {
      break;
    }
    rmdirSync(current);
    current = dirname(current);
  }
}

async function fetchJSON(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch manifest: HTTP ${response.status} ${response.statusText}`);
  }
  return response.json();
}

async function fetchText(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch file: HTTP ${response.status} ${response.statusText} (${url})`);
  }
  return response.text();
}

function getManifestUrl(meta) {
  const envName = meta.update?.manifest_url_env || 'CV_SKILL_UPDATE_MANIFEST_URL';
  return process.env[envName] || meta.update?.manifest_url || defaultManifestUrl;
}

function shouldUpdate(meta, manifest) {
  return compareVersion(meta.version, manifest.latest_version) < 0;
}

function printResult(result) {
  console.log(JSON.stringify(result, null, 2));
}

async function check() {
  const meta = readSkillMeta();
  const manifestUrl = getManifestUrl(meta);
  if (!manifestUrl) {
    return {
      ok: false,
      error: 'Missing update manifest URL',
      hint: `Set ${meta.update?.manifest_url_env || 'CV_SKILL_UPDATE_MANIFEST_URL'} to your published skill manifest URL.`,
      current_version: meta.version,
    };
  }

  const manifest = await fetchJSON(manifestUrl);
  if (manifest.name && manifest.name !== meta.name) {
    throw new Error(`Manifest skill name mismatch: expected ${meta.name}, got ${manifest.name}`);
  }

  const updateAvailable = shouldUpdate(meta, manifest);
  const updateRequired = manifest.min_supported_version
    ? compareVersion(meta.version, manifest.min_supported_version) < 0
    : false;

  return {
    ok: true,
    skill: meta.name,
    current_version: meta.version,
    latest_version: manifest.latest_version,
    min_supported_version: manifest.min_supported_version || null,
    update_available: updateAvailable,
    update_required: updateRequired,
    release_notes: manifest.release_notes || [],
    manifest_url: manifestUrl,
    manifest,
  };
}

async function update({ dryRun = false, force = false } = {}) {
  const result = await check();
  if (!result.ok) return result;
  if (!result.update_available && !force) return result;

  const { manifest } = result;
  if (!Array.isArray(manifest.files) || manifest.files.length === 0) {
    throw new Error('Manifest must include a non-empty files array for automatic update.');
  }

  const staged = [];
  const manifestPaths = [];
  const skippedFiles = [];
  for (const file of manifest.files) {
    const relativePath = assertSafeRelativePath(file.path);
    manifestPaths.push(relativePath);
    const target = join(skillRoot, relativePath);
    if (file.sha256 && existsSync(target) && statSync(target).isFile() && sha256LocalFile(target) === file.sha256) {
      skippedFiles.push(relativePath);
      continue;
    }

    const text = await fetchText(file.url);
    const normalizedText = text.replace(/\r\n/g, '\n');
    if (file.sha256 && sha256(normalizedText) !== file.sha256) {
      throw new Error(`Checksum mismatch for ${relativePath}`);
    }
    staged.push({ relativePath, text: normalizedText });
  }

  const managedRoots = manifest.sync?.delete_missing ? getManagedRoots(manifest) : [];
  const staleFiles = listMissingLocalFiles(manifestPaths, managedRoots);

  if (dryRun) {
    return {
      ...result,
      dry_run: true,
      sync_forced: force,
      file_count: staged.length,
      skipped_file_count: skippedFiles.length,
      stale_file_count: staleFiles.length,
      stale_files: staleFiles,
    };
  }

  const backupRoot = join(skillRoot, '.skill-backups', new Date().toISOString().replace(/[:.]/g, '-'));
  for (const item of staged) {
    const target = join(skillRoot, item.relativePath);
    const backup = join(backupRoot, item.relativePath);
    mkdirSync(dirname(target), { recursive: true });
    if (existsSync(target)) {
      mkdirSync(dirname(backup), { recursive: true });
      renameSync(target, backup);
    }
    writeFileSync(target, item.text, 'utf8');
  }
  let deletedFileCount = 0;
  for (const relativePath of staleFiles) {
    if (backupAndRemoveFile(relativePath, backupRoot)) {
      deletedFileCount += 1;
      pruneEmptyDirectories(dirname(join(skillRoot, relativePath)));
    }
  }

  return {
    ...result,
    updated: true,
    sync_forced: force,
    file_count: staged.length,
    skipped_file_count: skippedFiles.length,
    deleted_file_count: deletedFileCount,
    backup_dir: relative(skillRoot, backupRoot),
  };
}

async function main() {
  const args = new Set(process.argv.slice(2));
  const yes = args.has('--yes') || process.env.CV_SKILL_AUTO_UPDATE === 'true';
  const forceSync = args.has('--sync');
  const dryRun = args.has('--dry-run');
  const checkOnly = args.has('--check') || (!yes && !dryRun && !forceSync);

  const result = checkOnly ? await check() : await update({ dryRun, force: forceSync });
  printResult(result);

  if (result.ok && result.update_required && !yes) {
    process.exitCode = 2;
  }
}

main().catch((error) => {
  console.error(JSON.stringify({ ok: false, error: error.message }, null, 2));
  process.exit(1);
});
