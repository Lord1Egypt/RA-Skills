#!/usr/bin/env node
// camscanner-cli upgrade script — checks for new versions and upgrades CLI + Skill files.
// Run by AI Agent at the start of each session. Safe to run repeatedly.
//
// Usage:
//   node scripts/upgrade.cjs
//   node scripts/upgrade.cjs --rollback
//
// Behavior:
//   - If no update needed: exits silently (exit 0)
//   - If network fails: exits silently (exit 0), does not block usage
//   - If upgrade fails: auto-rollback, then exit 1
//   - If lock conflict: exits silently (exit 0)

'use strict';

const { execSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { pipeline } = require('stream/promises');
const crypto = require('crypto');

const CDN_BASE = process.env.CAMSCANNER_CLI_CDN || 'https://data.camscanner.com/camscanner-cli';

// ── Locate paths ────────────────────────────────────────────────────────────

const SCRIPT_DIR = __dirname;
const SKILL_DIR = path.dirname(SCRIPT_DIR);
const TMP_DIR = path.join(path.dirname(SKILL_DIR), 'camscanner-temp');
const BACKUP_DIR = path.join(TMP_DIR, 'backup');
const LOCK_DIR = path.join(TMP_DIR, 'upgrade.lock.d');
let CLI_PATH = '';

// ── Helpers ─────────────────────────────────────────────────────────────────

function say(msg) { console.log(`  ${msg}`); }
function warn(msg) { console.error(`  [warn] ${msg}`); }
function err(msg) { console.error(`  [error] ${msg}`); }

function detectPlatform() {
  const platform = os.platform();
  const arch = os.arch();
  const osMap = { linux: 'linux', darwin: 'darwin', win32: 'windows' };
  const archMap = { x64: 'amd64', arm64: 'arm64' };
  return { os: osMap[platform] || '', arch: archMap[arch] || '' };
}

function versionGt(v1, v2) {
  if (!v1) return false;
  if (!v2) return true;
  if (v1 === v2) return false;
  const p1 = v1.split('.').map(Number);
  const p2 = v2.split('.').map(Number);
  for (let i = 0; i < 3; i++) {
    const a = p1[i] || 0;
    const b = p2[i] || 0;
    if (a > b) return true;
    if (a < b) return false;
  }
  return false;
}

function extractVersion(str) {
  if (!str) return '';
  const m = str.match(/(\d+\.\d+\.\d+)/);
  return m ? m[1] : '';
}

function findCli() {
  // Try PATH first
  try {
    const cmd = os.platform() === 'win32' ? 'where camscanner-cli' : 'command -v camscanner-cli';
    const result = execSync(cmd, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] }).trim().split(/\r?\n/)[0];
    if (result && fs.existsSync(result)) return result;
  } catch {}
  // Windows fallback: default install location
  if (os.platform() === 'win32') {
    const defaultPath = path.join(process.env.LOCALAPPDATA || '', 'camscanner-cli', 'camscanner-cli.exe');
    if (fs.existsSync(defaultPath)) return defaultPath;
  }
  return '';
}

function getLocalVersion() {
  if (!CLI_PATH) return '';
  try {
    const output = execSync(`"${CLI_PATH}" --version`, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] });
    return extractVersion(output);
  } catch {}
  return '';
}

function getSkillVersion() {
  const skillMd = path.join(SKILL_DIR, 'SKILL.md');
  if (!fs.existsSync(skillMd)) return '';
  const content = fs.readFileSync(skillMd, 'utf8');
  const m = content.match(/^version:\s*"?(\d+\.\d+\.\d+)"?/m);
  return m ? m[1] : '';
}

async function getRemoteVersion() {
  try {
    const resp = await fetch(`${CDN_BASE}/latest-version.txt`, { signal: AbortSignal.timeout(10000) });
    if (!resp.ok) return '';
    const text = await resp.text();
    return extractVersion(text.trim());
  } catch {}
  return '';
}

async function download(url, dest) {
  const resp = await fetch(url, { signal: AbortSignal.timeout(120000) });
  if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${url}`);
  const fileStream = fs.createWriteStream(dest);
  await pipeline(resp.body, fileStream);
}

function sha256(filePath) {
  const data = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(data).digest('hex');
}

// ── Lock management ─────────────────────────────────────────────────────────

function acquireLock() {
  fs.mkdirSync(path.dirname(LOCK_DIR), { recursive: true });
  try {
    fs.mkdirSync(LOCK_DIR);
  } catch {
    // Lock exists, check if stale
    const pidFile = path.join(LOCK_DIR, 'pid');
    if (fs.existsSync(pidFile)) {
      const lockPid = fs.readFileSync(pidFile, 'utf8').trim();
      if (lockPid && isProcessAlive(parseInt(lockPid, 10))) {
        return false;
      }
      // Stale lock, remove and retry
      fs.rmSync(LOCK_DIR, { recursive: true, force: true });
      try {
        fs.mkdirSync(LOCK_DIR);
      } catch {
        return false;
      }
    } else {
      return false;
    }
  }
  fs.writeFileSync(path.join(LOCK_DIR, 'pid'), String(process.pid));
  return true;
}

function releaseLock() {
  try { fs.rmSync(LOCK_DIR, { recursive: true, force: true }); } catch {}
}

function isProcessAlive(pid) {
  try { process.kill(pid, 0); return true; } catch { return false; }
}

// ── Backup & Rollback ───────────────────────────────────────────────────────

function backupCurrent(currentVersion) {
  fs.mkdirSync(BACKUP_DIR, { recursive: true });
  // Backup CLI binary
  if (CLI_PATH && fs.existsSync(CLI_PATH)) {
    const ext = os.platform() === 'win32' ? '.exe.bak' : '.bak';
    fs.copyFileSync(CLI_PATH, path.join(BACKUP_DIR, `camscanner-cli${ext}`));
  }
  // Backup Skill files as tar.gz (use zip on Windows for simplicity)
  const backupName = `skill-${currentVersion}.tar.gz`;
  const backupPath = path.join(BACKUP_DIR, backupName);
  try {
    if (os.platform() === 'win32') {
      execSync(`powershell -NoProfile -Command "Compress-Archive -Path '${path.join(SKILL_DIR, 'SKILL.md')}','${path.join(SKILL_DIR, 'references')}','${path.join(SKILL_DIR, 'scripts')}' -DestinationPath '${backupPath.replace('.tar.gz', '.zip')}' -Force"`, { stdio: 'pipe' });
    } else {
      execSync(`tar -czf "${backupPath}" -C "${SKILL_DIR}" SKILL.md references/ scripts/`, { stdio: 'pipe' });
    }
  } catch {}
  fs.writeFileSync(path.join(BACKUP_DIR, 'previous-version.txt'), currentVersion);
}

function rollback(prevVersion) {
  warn(`Upgrade failed, rolling back to v${prevVersion}...`);
  // Restore CLI
  const ext = os.platform() === 'win32' ? '.exe.bak' : '.bak';
  const bakCli = path.join(BACKUP_DIR, `camscanner-cli${ext}`);
  if (fs.existsSync(bakCli) && CLI_PATH) {
    fs.copyFileSync(bakCli, CLI_PATH);
    if (os.platform() !== 'win32') {
      fs.chmodSync(CLI_PATH, 0o755);
    }
  }
  // Restore Skill
  if (os.platform() === 'win32') {
    const bakSkill = path.join(BACKUP_DIR, `skill-${prevVersion}.zip`);
    if (fs.existsSync(bakSkill)) {
      try {
        execSync(`powershell -NoProfile -Command "Expand-Archive -Path '${bakSkill}' -DestinationPath '${SKILL_DIR}' -Force"`, { stdio: 'pipe' });
      } catch {}
    }
  } else {
    const bakSkill = path.join(BACKUP_DIR, `skill-${prevVersion}.tar.gz`);
    if (fs.existsSync(bakSkill)) {
      try {
        execSync(`tar -xzf "${bakSkill}" -C "${SKILL_DIR}"`, { stdio: 'pipe' });
      } catch {}
    }
  }
  err(`Rolled back to v${prevVersion}`);
}

function doRollback() {
  const prevFile = path.join(BACKUP_DIR, 'previous-version.txt');
  if (!fs.existsSync(prevFile)) {
    err('No backup found, cannot rollback.');
    process.exit(1);
  }
  const prevVersion = fs.readFileSync(prevFile, 'utf8').trim();
  rollback(prevVersion);
  say(`Rollback to v${prevVersion} complete.`);
  process.exit(0);
}

// ── Cleanup ─────────────────────────────────────────────────────────────────

function cleanup() {
  try {
    const files = fs.readdirSync(TMP_DIR);
    for (const f of files) {
      if (f.startsWith('camscanner-cli-') || f.startsWith('camscanner-skill-') || f === 'checksums.txt') {
        fs.rmSync(path.join(TMP_DIR, f), { force: true });
      }
    }
    const skillExtract = path.join(TMP_DIR, 'skill');
    if (fs.existsSync(skillExtract)) {
      fs.rmSync(skillExtract, { recursive: true, force: true });
    }
  } catch {}
  releaseLock();
}

// ── Main ────────────────────────────────────────────────────────────────────

async function main() {
  if (typeof globalThis.fetch !== 'function') {
    err('Node.js >= 18 required (native fetch). Current: ' + process.version);
    process.exit(0);
  }

  // Handle --rollback flag
  if (process.argv.includes('--rollback')) {
    doRollback();
  }

  // Find CLI
  CLI_PATH = findCli();
  if (!CLI_PATH) {
    process.exit(0);
  }

  // Get versions
  const cliVersion = getLocalVersion();
  if (!cliVersion) {
    process.exit(0);
  }
  const skillVersion = getSkillVersion();

  // Take the lower of CLI and Skill versions
  let localVersion;
  if (skillVersion && versionGt(cliVersion, skillVersion)) {
    localVersion = skillVersion;
  } else {
    localVersion = cliVersion;
  }

  const remoteVersion = await getRemoteVersion();
  if (!remoteVersion) {
    process.exit(0);
  }

  // Compare versions
  if (!versionGt(remoteVersion, localVersion)) {
    process.exit(0);
  }

  // Acquire lock
  if (!acquireLock()) {
    process.exit(0);
  }
  process.on('exit', cleanup);
  process.on('SIGINT', () => { cleanup(); process.exit(1); });
  process.on('SIGTERM', () => { cleanup(); process.exit(1); });

  say(`Update available: v${localVersion} → v${remoteVersion}`);

  // Detect platform
  const { os: osName, arch: archName } = detectPlatform();
  if (!osName || !archName) {
    err('Unsupported platform');
    process.exit(0);
  }

  // Prepare temp directory
  fs.mkdirSync(TMP_DIR, { recursive: true });

  // Download CLI binary
  const binSuffix = osName === 'windows'
    ? `camscanner-cli-${osName}-${archName}.exe`
    : `camscanner-cli-${osName}-${archName}`;
  // CLI subpath — patched at build time for each target
  const cliSubpath = "clawhub/";

  const binUrl = `${CDN_BASE}/releases/v${remoteVersion}/${cliSubpath}${binSuffix}`;

  say('Downloading CLI binary...');
  try {
    await download(binUrl, path.join(TMP_DIR, binSuffix));
  } catch {
    warn('Download CLI failed, skipping upgrade.');
    process.exit(0);
  }

  // Download Skill ZIP
  const skillZip = `camscanner-skill-clawhub-v${remoteVersion}.zip`;
  const skillUrl = `${CDN_BASE}/releases/v${remoteVersion}/${skillZip}`;

  say('Downloading Skill package...');
  try {
    await download(skillUrl, path.join(TMP_DIR, skillZip));
  } catch {
    warn('Download Skill ZIP failed, skipping upgrade.');
    process.exit(0);
  }

  // Download and verify checksums (mandatory — abort if unavailable)
  const checksumsUrl = `${CDN_BASE}/releases/v${remoteVersion}/${cliSubpath}checksums.txt`;
  try {
    await download(checksumsUrl, path.join(TMP_DIR, 'checksums.txt'));
  } catch {
    warn('Cannot download checksums.txt, aborting upgrade for security.');
    process.exit(0);
  }

  const checksumContent = fs.readFileSync(path.join(TMP_DIR, 'checksums.txt'), 'utf8');
  const lines = checksumContent.split(/\r?\n/);

  const cliLine = lines.find(l => l.includes(binSuffix));

  if (!cliLine) {
    warn('checksums.txt missing entry for CLI binary, aborting upgrade.');
    process.exit(0);
  }

  const expectedCli = cliLine.trim().split(/\s+/)[0];
  const actualCli = sha256(path.join(TMP_DIR, binSuffix));
  if (actualCli !== expectedCli) {
    warn('CLI binary checksum mismatch, skipping upgrade.');
    process.exit(0);
  }

  // Verify downloaded CLI binary
  const binPath = path.join(TMP_DIR, binSuffix);
  if (osName !== 'windows') {
    fs.chmodSync(binPath, 0o755);
  }
  let downloadedVer = '';
  try {
    const output = execSync(`"${binPath}" --version`, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] });
    downloadedVer = extractVersion(output);
  } catch {}
  if (!downloadedVer) {
    warn('Downloaded CLI binary is not valid, skipping upgrade.');
    process.exit(0);
  }

  // Backup current version
  say('Backing up current version...');
  backupCurrent(localVersion);

  // Replace CLI binary
  say('Replacing CLI binary...');
  try {
    fs.copyFileSync(binPath, CLI_PATH);
    if (osName !== 'windows') {
      fs.chmodSync(CLI_PATH, 0o755);
    }
  } catch (e) {
    warn(`Cannot write to ${CLI_PATH}: ${e.message}`);
    rollback(localVersion);
    process.exit(1);
  }

  // Replace Skill files
  say('Replacing Skill files...');
  const skillExtractDir = path.join(TMP_DIR, 'skill');
  fs.mkdirSync(skillExtractDir, { recursive: true });

  try {
    if (osName === 'windows') {
      execSync(`powershell -NoProfile -Command "Expand-Archive -Path '${path.join(TMP_DIR, skillZip)}' -DestinationPath '${skillExtractDir}' -Force"`, { stdio: 'pipe' });
    } else {
      execSync(`unzip -qo "${path.join(TMP_DIR, skillZip)}" -d "${skillExtractDir}"`, { stdio: 'pipe' });
    }
  } catch {
    warn('Failed to extract Skill ZIP.');
    rollback(localVersion);
    process.exit(1);
  }

  // Find extracted content root
  let skillSrc = skillExtractDir;
  if (!fs.existsSync(path.join(skillSrc, 'SKILL.md'))) {
    const found = findFileRecursive(skillSrc, 'SKILL.md', 2);
    if (found) {
      skillSrc = path.dirname(found);
    } else {
      warn('Skill ZIP does not contain SKILL.md.');
      rollback(localVersion);
      process.exit(1);
    }
  }

  // Replace SKILL.md
  fs.copyFileSync(path.join(skillSrc, 'SKILL.md'), path.join(SKILL_DIR, 'SKILL.md'));

  // Replace references/
  const refsSrc = path.join(skillSrc, 'references');
  if (fs.existsSync(refsSrc)) {
    const refsDest = path.join(SKILL_DIR, 'references');
    fs.rmSync(refsDest, { recursive: true, force: true });
    copyDirSync(refsSrc, refsDest);
  }

  // Replace scripts/ (last, since this script is in it)
  const scriptsSrc = path.join(skillSrc, 'scripts');
  if (fs.existsSync(scriptsSrc)) {
    const scriptsDest = path.join(SKILL_DIR, 'scripts');
    fs.rmSync(scriptsDest, { recursive: true, force: true });
    copyDirSync(scriptsSrc, scriptsDest);
  }

  // Verify upgrade
  let newVer = '';
  try {
    const output = execSync(`"${CLI_PATH}" --version`, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] });
    newVer = extractVersion(output);
  } catch {}
  if (newVer !== remoteVersion) {
    rollback(localVersion);
    process.exit(1);
  }

  // Clean old skill backups, keep only the latest one
  try {
    const backupFiles = fs.readdirSync(BACKUP_DIR);
    const currentBackup = osName === 'windows' ? `skill-${localVersion}.zip` : `skill-${localVersion}.tar.gz`;
    for (const f of backupFiles) {
      if (f.startsWith('skill-') && (f.endsWith('.tar.gz') || f.endsWith('.zip')) && f !== currentBackup) {
        fs.rmSync(path.join(BACKUP_DIR, f), { force: true });
      }
    }
  } catch {}

  say(`Upgrade complete: v${localVersion} → v${remoteVersion}`);
}

// ── Utilities ───────────────────────────────────────────────────────────────

function findFileRecursive(dir, filename, maxDepth) {
  if (maxDepth < 0) return null;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isFile() && entry.name === filename) return full;
    if (entry.isDirectory() && maxDepth > 0) {
      const found = findFileRecursive(full, filename, maxDepth - 1);
      if (found) return found;
    }
  }
  return null;
}

function copyDirSync(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDirSync(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

main().catch(e => {
  warn(e.message);
  cleanup();
  process.exit(1);
});
