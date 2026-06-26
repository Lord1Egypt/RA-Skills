#!/usr/bin/env node
/**
 * feishu-skills cross-platform installer
 *
 * Usage:
 *   node install.js
 *   node install.js --target /custom/path/to/skills
 *
 * Auto-detects EnClaws or OpenClaw installation and installs skill directories.
 * Always outputs a JSON result so AI agents can parse success/failure and
 * report the correct target path to the user.
 */



import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
const __dirname = path.dirname(fileURLToPath(import.meta.url));

const SKILLS = [
  'feishu-quick-setup',
  'feishu-auth',
  'feishu-create-doc',
  'feishu-fetch-doc',
  'feishu-search-doc',
  'feishu-update-doc',
  'feishu-im-read',
  'feishu-chat',
  'feishu-calendar',
  'feishu-task',
  'feishu-bitable',
  'feishu-docx-download',
  'feishu-drive',
  'feishu-image-ocr',
  'feishu-search-user',
  'feishu-sheet',
  'feishu-wiki',
];

// Files/dirs to exclude when copying
const EXCLUDE = ['.tokens', 'node_modules', '.python', '__pycache__', '*.bak', '*.pyc', 'config.json'];

function shouldExclude(name) {
  return EXCLUDE.some(p => {
    if (p.startsWith('*')) return name.endsWith(p.slice(1));
    return name === p;
  });
}

// ---------------------------------------------------------------------------
// Parse --target argument
// ---------------------------------------------------------------------------
const args = process.argv.slice(2);
const targetIdx = args.indexOf('--target');
let targetDir = targetIdx !== -1 ? args[targetIdx + 1] : null;

// ---------------------------------------------------------------------------
// Auto-detect target directory
// ---------------------------------------------------------------------------
function detectTarget() {
  const home = os.homedir();

  // 1. Detect by env var — EnClaws injects ENCLAWS_USER_WORKSPACE at runtime.
  //    Extract tenantId from workspace path and install to tenant-level skills dir.
  const enclawsWorkspace = process.env.ENCLAWS_USER_WORKSPACE;
  if (enclawsWorkspace) {
    const match = enclawsWorkspace.replace(/\\/g, '/').match(/tenants\/([^/]+)\//);
    if (match) {
      const tenantId = match[1];
      return { dir: path.join(home, '.enclaws', 'tenants', tenantId, 'skills'), env: 'EnClaws' };
    }
    // Fallback: env var exists but tenant path not parseable — use generic tenants dir
    return { dir: path.join(home, '.enclaws', 'tenants', 'skills'), env: 'EnClaws' };
  }

  // 2. No EnClaws env var → check OpenClaw
  const openclawBase = path.join(home, '.openclaw');
  if (fs.existsSync(openclawBase)) {
    return { dir: path.join(openclawBase, 'workspace', 'skills'), env: 'OpenClaw' };
  }

  // 3. Fallback: check EnClaws directory structure, pick first tenant
  const enclawsBase = path.join(home, '.enclaws', 'tenants');
  if (fs.existsSync(enclawsBase)) {
    const tenants = fs.readdirSync(enclawsBase).filter(f => {
      return fs.statSync(path.join(enclawsBase, f)).isDirectory();
    });
    if (tenants.length > 0) {
      return { dir: path.join(enclawsBase, tenants[0], 'skills'), env: 'EnClaws' };
    }
  }

  return null;
}

// ---------------------------------------------------------------------------
// Recursive copy (skips excluded names, preserves .tokens in existing installs)
// ---------------------------------------------------------------------------
function copyDir(src, dst) {
  fs.mkdirSync(dst, { recursive: true });
  for (const entry of fs.readdirSync(src)) {
    if (shouldExclude(entry)) continue;
    const srcPath = path.join(src, entry);
    const dstPath = path.join(dst, entry);
    if (fs.statSync(srcPath).isDirectory()) {
      copyDir(srcPath, dstPath);
    } else {
      fs.copyFileSync(srcPath, dstPath);
    }
  }
}

// Non-skill files to clean up when running in-place
const CLEANUP_FILES = [
  'install.js', 'install.sh', 'install.ps1',
  'README.md', 'README.zh.md', 'SKILL.md', 'LICENSE', '.gitignore', '.git',
];

function removeRecursive(p) {
  if (!fs.existsSync(p)) return;
  if (fs.statSync(p).isDirectory()) {
    for (const entry of fs.readdirSync(p)) removeRecursive(path.join(p, entry));
    fs.rmdirSync(p);
  } else {
    fs.unlinkSync(p);
  }
}

// ---------------------------------------------------------------------------
// Detect in-place mode: install.js is already inside a skills directory
// (e.g. AI unzipped the repo directly into skills/feishu-skills/)
// ---------------------------------------------------------------------------
const repoDir = __dirname;
const parentDir = path.dirname(repoDir);
const parentName = path.basename(parentDir).toLowerCase();
const hasSkillDirs = SKILLS.some(s => fs.existsSync(path.join(repoDir, s)));
const isInPlace = hasSkillDirs && (parentName === 'skills');

if (isInPlace && !targetDir) {
  // In-place mode: already inside skills dir, just clean up non-skill files
  const skillsFound = SKILLS.filter(s => fs.existsSync(path.join(repoDir, s)));
  for (const f of CLEANUP_FILES) {
    removeRecursive(path.join(repoDir, f));
  }
  console.log(JSON.stringify({
    success: true,
    env: 'in-place',
    target: repoDir,
    installed: skillsFound,
    updated: [],
    reply: `飞书技能安装完成！路径：${repoDir}。已安装：${skillsFound.join(', ')}。`,
  }));
  process.exit(0);
}

// ---------------------------------------------------------------------------
// Normal mode: copy skills to detected target directory
// ---------------------------------------------------------------------------
const enclawsWsEnv = process.env.ENCLAWS_USER_WORKSPACE;
if (enclawsWsEnv) {
  console.error(`[install] ENCLAWS_USER_WORKSPACE = ${enclawsWsEnv}`);
} else {
  console.error('[install] ENCLAWS_USER_WORKSPACE is not set, falling back to directory detection');
}

let detected = null;

if (!targetDir) {
  detected = detectTarget();
  if (!detected) {
    console.log(JSON.stringify({
      success: false,
      error: 'env_not_found',
      message: 'Could not detect OpenClaw or EnClaws installation.',
      hint: 'Use --target to specify the skills directory manually, e.g.: node install.js --target ~/.openclaw/workspace/skills',
    }));
    process.exit(1);
  }
  targetDir = detected.dir;
}

// Install into a feishu-skills subdirectory under the target skills dir
const installDir = path.join(targetDir, 'feishu-skills');
console.error(`[install] target directory: ${installDir} (detected env: ${detected?.env ?? 'custom'})`);

const installed = [];
const updated   = [];
const errors    = [];

for (const skill of SKILLS) {
  const src = path.join(repoDir, skill);
  const dst = path.join(installDir, skill);

  if (!fs.existsSync(src)) continue;

  try {
    const isUpdate = fs.existsSync(dst);
    copyDir(src, dst);
    (isUpdate ? updated : installed).push(skill);
  } catch (e) {
    errors.push({ skill, error: e.message });
  }
}

if (errors.length > 0) {
  console.log(JSON.stringify({
    success: false,
    error: 'copy_failed',
    target: installDir,
    env: detected?.env ?? 'custom',
    installed,
    updated,
    errors,
    message: `部分技能安装失败，目标目录：${installDir}`,
    hint: `请确认当前用户对目标目录有写入权限，然后重新执行：node install.js`,
  }));
  process.exit(1);
}

console.log(JSON.stringify({
  success: true,
  env: detected?.env ?? 'custom',
  target: installDir,
  installed,
  updated,
  reply: `飞书技能安装完成！环境：${detected?.env ?? 'custom'}，路径：${installDir}。已安装：${installed.join(', ')}${updated.length ? `；已更新：${updated.join(', ')}` : ''}。`,
}));

// Clean up: remove the cloned repo directory (including this file) after install
process.on('exit', () => {
  try { removeRecursive(repoDir); } catch (_) {}
});
