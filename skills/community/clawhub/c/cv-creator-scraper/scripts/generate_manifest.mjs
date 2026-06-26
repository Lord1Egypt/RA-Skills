#!/usr/bin/env node
// Generate skill-manifest.json from local skill files.
//
// Usage:
//   node scripts/generate_manifest.mjs
//   node scripts/generate_manifest.mjs --version 1.7.0 --note "Improved industry mapping"
//   node scripts/generate_manifest.mjs --include scripts/new_file.mjs

import { createHash } from 'node:crypto';
import { existsSync, readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { dirname, isAbsolute, join, normalize, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const skillRoot = resolve(scriptDir, '..');
const skillMetaPath = join(skillRoot, 'skill.json');
const manifestPath = join(skillRoot, 'skill-manifest.json');
const excludedPathPrefixes = [
  '.git/',
  '.skill-backups/',
  'node_modules/',
  '__pycache__/',
];
const excludedPathNames = new Set([
  '.DS_Store',
  'Thumbs.db',
  '.env',
]);

function readJSON(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}

function writeJSON(path, data) {
  writeFileSync(path, `${JSON.stringify(data, null, 2)}\n`, 'utf8');
}

function parseArgs(argv) {
  const result = {
    includes: [],
    notes: [],
    dryRun: false,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--version') {
      result.version = argv[++index];
    } else if (arg === '--min-supported') {
      result.minSupported = argv[++index];
    } else if (arg === '--note') {
      result.notes.push(argv[++index]);
    } else if (arg === '--include') {
      result.includes.push(argv[++index]);
    } else if (arg === '--raw-base') {
      result.rawBase = argv[++index];
    } else if (arg === '--dry-run') {
      result.dryRun = true;
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }

  return result;
}

function assertSafeRelativePath(path) {
  const normalized = normalize(path).replaceAll('\\', '/');
  if (
    !normalized ||
    isAbsolute(normalized) ||
    normalized.startsWith('..') ||
    normalized.includes('/../') ||
    normalized === '.'
  ) {
    throw new Error(`Unsafe manifest file path: ${path}`);
  }
  return normalized;
}

function isExcludedPath(relativePath) {
  const normalized = assertSafeRelativePath(relativePath);
  const name = normalized.split('/').pop();
  return excludedPathNames.has(name) || excludedPathPrefixes.some((prefix) => normalized.startsWith(prefix));
}

function scanSkillFiles(root = skillRoot, prefix = '') {
  const paths = [];
  for (const entry of readdirSync(root, { withFileTypes: true })) {
    const relativePath = prefix ? `${prefix}/${entry.name}` : entry.name;
    const normalized = assertSafeRelativePath(relativePath);
    if (isExcludedPath(normalized)) {
      continue;
    }

    const fullPath = join(root, entry.name);
    if (entry.isDirectory()) {
      paths.push(...scanSkillFiles(fullPath, normalized));
    } else if (entry.isFile()) {
      paths.push(normalized);
    }
  }
  return paths.sort((left, right) => left.localeCompare(right));
}

function sha256ForTextFile(path) {
  const text = readFileSync(path, 'utf8').replace(/\r\n/g, '\n');
  return createHash('sha256').update(text).digest('hex');
}

function deriveRawBase(manifest, skillName) {
  if (process.env.CV_SKILL_MANIFEST_RAW_BASE) {
    return process.env.CV_SKILL_MANIFEST_RAW_BASE.replace(/\/$/, '');
  }

  const firstFile = Array.isArray(manifest.files) ? manifest.files.find((file) => file.url && file.path) : null;
  if (firstFile) {
    const suffix = `/${firstFile.path}`;
    if (firstFile.url.endsWith(suffix)) {
      return firstFile.url.slice(0, -suffix.length);
    }
  }

  const branch = manifest.branch || 'main';
  return `https://raw.githubusercontent.com/creativault/skills/${branch}/${skillName}`;
}

function buildManifest({ args, skillMeta, currentManifest }) {
  const version = args.version || skillMeta.version || currentManifest.latest_version;
  if (!version) {
    throw new Error('Missing version. Set skill.json version or pass --version.');
  }

  const skillName = currentManifest.name || skillMeta.name;
  const rawBase = (args.rawBase || deriveRawBase(currentManifest, skillName)).replace(/\/$/, '');
  const paths = [...new Set([...scanSkillFiles(), ...args.includes.map(assertSafeRelativePath)])].sort(
    (left, right) => left.localeCompare(right),
  );

  const files = paths.map((relativePath) => {
    const fullPath = join(skillRoot, relativePath);
    if (!existsSync(fullPath) || !statSync(fullPath).isFile()) {
      throw new Error(`Manifest file does not exist: ${relativePath}`);
    }
    const file = {
      path: relativePath,
      url: `${rawBase}/${relativePath}`,
    };
    if (relativePath !== 'skill-manifest.json') {
      file.sha256 = sha256ForTextFile(fullPath);
    }
    return file;
  });

  return {
    name: skillName,
    latest_version: version,
    min_supported_version: args.minSupported || currentManifest.min_supported_version || version,
    channel: skillMeta.channel || currentManifest.channel || 'stable',
    branch: currentManifest.branch || 'main',
    release_notes: args.notes.length > 0 ? args.notes : currentManifest.release_notes || [],
    sync: {
      mode: 'mirror',
      delete_missing: true,
      managed_roots: ['.'],
      exclude: ['.skill-backups/**'],
    },
    files,
  };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const skillMeta = readJSON(skillMetaPath);
  const currentManifest = existsSync(manifestPath) ? readJSON(manifestPath) : {};
  const manifest = buildManifest({ args, skillMeta, currentManifest });

  if (args.dryRun) {
    console.log(JSON.stringify(manifest, null, 2));
    return;
  }

  writeJSON(manifestPath, manifest);
  console.log(
    JSON.stringify(
      {
        ok: true,
        manifest: 'skill-manifest.json',
        latest_version: manifest.latest_version,
        min_supported_version: manifest.min_supported_version,
        file_count: manifest.files.length,
      },
      null,
      2,
    ),
  );
}

main();
