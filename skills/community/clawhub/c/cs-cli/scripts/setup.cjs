#!/usr/bin/env node
// camscanner-cli installer — cross-platform Node.js script.
// Requires Node.js >= 18 (uses native fetch).
//
// Usage:
//   node scripts/setup.cjs
//
// Environment variables (all optional):
//   CAMSCANNER_CLI_VERSION — version to install (default: read from SKILL.md)
//   CAMSCANNER_CLI_CDN     — CDN base URL override
//   CAMSCANNER_CLI_DIR     — install directory override

'use strict';

const { execSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { pipeline } = require('stream/promises');
const crypto = require('crypto');

const CDN_BASE = process.env.CAMSCANNER_CLI_CDN || 'https://data.camscanner.com/camscanner-cli/releases';
const BIN_NAME = 'camscanner-cli';

function say(msg) { console.log(`  ${msg}`); }
function err(msg) { console.error(`  [ERROR] ${msg}`); process.exit(1); }

function detectPlatform() {
  const platform = os.platform();
  const arch = os.arch();
  const osMap = { linux: 'linux', darwin: 'darwin', win32: 'windows' };
  const archMap = { x64: 'amd64', arm64: 'arm64' };
  const osName = osMap[platform];
  const archName = archMap[arch];
  if (!osName) err(`Unsupported OS: ${platform}`);
  if (!archName) err(`Unsupported architecture: ${arch}`);
  return { os: osName, arch: archName };
}

function defaultInstallDir(osName) {
  if (process.env.CAMSCANNER_CLI_DIR) return process.env.CAMSCANNER_CLI_DIR;
  if (osName === 'windows') {
    return path.join(process.env.LOCALAPPDATA || path.join(os.homedir(), 'AppData', 'Local'), 'camscanner-cli');
  }
  return path.join(os.homedir(), '.local', 'bin');
}

function resolveVersion() {
  if (process.env.CAMSCANNER_CLI_VERSION) return process.env.CAMSCANNER_CLI_VERSION;
  const scriptDir = __dirname;
  const candidates = [
    path.join(scriptDir, '..', 'SKILL.md'),
    path.join(scriptDir, '..', '..', 'SKILL.md'),
    path.resolve('SKILL.md'),
  ];
  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) {
      const content = fs.readFileSync(candidate, 'utf8');
      const match = content.match(/^version:\s*"?([^"\s]+)"?\s*$/m);
      if (match) return match[1];
    }
  }
  err('Cannot determine version. Set CAMSCANNER_CLI_VERSION explicitly.');
}

function compareVersions(a, b) {
  const pa = a.split('.').map(Number);
  const pb = b.split('.').map(Number);
  for (let i = 0; i < 3; i++) {
    const va = pa[i] || 0;
    const vb = pb[i] || 0;
    if (va > vb) return 1;
    if (va < vb) return -1;
  }
  return 0;
}

function checkExisting(targetVersion) {
  try {
    const existingVer = execSync(`${BIN_NAME} --version`, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] }).trim();
    const existingPath = execSync(
      os.platform() === 'win32' ? `where ${BIN_NAME}` : `command -v ${BIN_NAME}`,
      { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] }
    ).trim().split(/\r?\n/)[0];

    if (existingVer === targetVersion) {
      say(`${BIN_NAME} v${targetVersion} is already installed at ${existingPath}`);
      process.exit(0);
    }
    if (compareVersions(existingVer, targetVersion) >= 0) {
      say(`Installed ${BIN_NAME} v${existingVer} >= target v${targetVersion}, skipping.`);
      process.exit(0);
    }
    say(`Found existing ${BIN_NAME} v${existingVer} at ${existingPath}`);
    say(`Will upgrade to v${targetVersion}`);
  } catch {
    // not installed — proceed
  }
}

async function download(url, dest) {
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${url}`);
  const fileStream = fs.createWriteStream(dest);
  await pipeline(resp.body, fileStream);
}

function sha256(filePath) {
  const data = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(data).digest('hex');
}

async function main() {
  if (typeof globalThis.fetch !== 'function') {
    err('Node.js >= 18 required (native fetch). Current: ' + process.version);
  }

  const { os: osName, arch } = detectPlatform();
  const version = resolveVersion();
  const installDir = defaultInstallDir(osName);

  checkExisting(version);

  // 产物命名与 Makefile 一致: camscanner-cli-{os}-{arch}[.exe]
  const binFile = osName === 'windows'
    ? `${BIN_NAME}-${osName}-${arch}.exe`
    : `${BIN_NAME}-${osName}-${arch}`;
  // CLI subpath — patched at build time for each target
  const cliSubpath = "clawhub/";

  const downloadUrl = `${CDN_BASE}/v${version}/${cliSubpath}${binFile}`;

  say(`Installing ${BIN_NAME} v${version} (${osName}/${arch})...`);
  say(`Target: ${path.join(installDir, osName === 'windows' ? `${BIN_NAME}.exe` : BIN_NAME)}`);

  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'camscanner-cli-install-'));
  try {
    const tmpFile = path.join(tmpDir, binFile);

    say(`Downloading ${binFile}...`);
    await download(downloadUrl, tmpFile);

    // Download and verify checksum
    const checksumsUrl = `${CDN_BASE}/v${version}/${cliSubpath}checksums.txt`;
    try {
      const checksumsFile = path.join(tmpDir, 'checksums.txt');
      await download(checksumsUrl, checksumsFile);
      const checksumContent = fs.readFileSync(checksumsFile, 'utf8');
      const lines = checksumContent.split(/\r?\n/);
      const matchLine = lines.find(l => l.includes(binFile));
      if (matchLine) {
        const expected = matchLine.trim().split(/\s+/)[0];
        const actual = sha256(tmpFile);
        if (actual !== expected) {
          err(`Checksum mismatch for ${binFile}. Expected: ${expected}, Got: ${actual}`);
        }
        say('[OK] Checksum verified');
      } else {
        say('[WARN] No checksum entry found for this binary, skipping verification');
      }
    } catch (e) {
      if (e.message && e.message.includes('Checksum mismatch')) throw e;
      say('[WARN] Could not download checksums.txt, skipping verification');
    }

    fs.mkdirSync(installDir, { recursive: true });
    const destBin = path.join(installDir, osName === 'windows' ? `${BIN_NAME}.exe` : BIN_NAME);
    fs.copyFileSync(tmpFile, destBin);
    if (osName !== 'windows') fs.chmodSync(destBin, 0o755);

    say(`[OK] Installed: ${destBin}`);

    const envPath = process.env.PATH || '';
    if (!envPath.split(path.delimiter).includes(installDir)) {
      say('');
      if (osName === 'windows') {
        say(`Adding ${installDir} to user PATH...`);
        try {
          execSync(
            `powershell -NoProfile -Command "[Environment]::SetEnvironmentVariable('PATH', '${installDir};' + [Environment]::GetEnvironmentVariable('PATH', 'User'), 'User')"`,
            { stdio: 'pipe' }
          );
          process.env.PATH = `${installDir}${path.delimiter}${envPath}`;
          say('[OK] PATH updated');
        } catch (e) {
          say(`[WARN] Could not update PATH automatically: ${e.message}`);
          say(`  Run manually: [Environment]::SetEnvironmentVariable("PATH", "${installDir};$env:PATH", "User")`);
        }
      } else {
        say(`${installDir} is not in your PATH.`);
        say(`  Add to ~/.bashrc or ~/.zshrc:`);
        say(`    export PATH="${installDir}:$PATH"`);
      }
    }

    say('');
    say(`${BIN_NAME} v${version} ready!`);
    say(`  PATH_HINT: ${installDir}`);
  } finally {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  }
}

main().catch(e => { err(e.message); });
