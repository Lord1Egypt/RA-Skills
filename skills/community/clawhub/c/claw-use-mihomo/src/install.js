import { getPlatform, getBinaryPath, getConfigDir } from './platform.js';
import { mkdirSync, chmodSync, existsSync, writeFileSync, statSync } from 'fs';
import { join, dirname } from 'path';
import { spawnSync } from 'child_process';
import { mkdtempSync } from 'fs';
import { tmpdir } from 'os';
import { log } from './logger.js';
import { homedir } from 'os';

const RELEASES_API = 'https://api.github.com/repos/MetaCubeX/mihomo/releases/latest';
const DOWNLOAD_TIMEOUT_MS = 120000;

async function getLatestRelease() {
  const res = await fetch(RELEASES_API, { signal: AbortSignal.timeout(30000) });
  if (!res.ok) throw new Error(`Failed to fetch releases: ${res.status}`);
  return res.json();
}

function findAsset(release, os, arch) {
  const suffix = os === 'windows' ? '.zip' : '.gz';
  const pattern = `mihomo-${os}-${arch}`;
  const asset = release.assets.find(a =>
    a.name.includes(pattern) && a.name.endsWith(suffix) && !a.name.includes('compatible')
  );
  if (!asset) throw new Error(`No binary found for ${os}-${arch}`);
  return asset;
}

async function download(url, dest) {
  const res = await fetch(url, { signal: AbortSignal.timeout(DOWNLOAD_TIMEOUT_MS) });
  if (!res.ok) throw new Error(`Download failed: ${res.status}`);
  const buffer = Buffer.from(await res.arrayBuffer());
  if (buffer.length === 0) throw new Error('Downloaded file is empty');
  writeFileSync(dest, buffer);
}

export async function install() {
  const { mihomoOS, mihomoArch, os } = getPlatform();
  const binPath = getBinaryPath();
  const configDir = getConfigDir();

  log(`Detecting platform: ${mihomoOS}/${mihomoArch}`);

  log('Fetching latest mihomo release...');
  const release = await getLatestRelease();
  const version = release.tag_name;
  const asset = findAsset(release, mihomoOS, mihomoArch);

  log(`Downloading ${asset.name} (${(asset.size / 1024 / 1024).toFixed(1)}MB)...`);

  // Use unique temp directory
  const tmpDir = mkdtempSync(join(tmpdir(), 'mihomod-'));
  const tmpFile = join(tmpDir, asset.name);
  await download(asset.browser_download_url, tmpFile);

  // Verify download size matches
  const downloadedSize = statSync(tmpFile).size;
  if (asset.size && Math.abs(downloadedSize - asset.size) > 1024) {
    throw new Error(`Download size mismatch: expected ~${asset.size}, got ${downloadedSize}`);
  }

  // Extract
  mkdirSync(dirname(binPath), { recursive: true });
  if (tmpFile.endsWith('.gz')) {
    const gunzipResult = spawnSync('gunzip', ['-f', tmpFile], { stdio: 'pipe' });
    if (gunzipResult.status !== 0) throw new Error(`gunzip failed: ${(gunzipResult.stderr || '').toString()}`);
    const extracted = tmpFile.replace('.gz', '');
    const mvResult = spawnSync('mv', [extracted, binPath], { stdio: 'pipe' });
    if (mvResult.status !== 0) throw new Error(`mv failed: ${(mvResult.stderr || '').toString()}`);
    chmodSync(binPath, 0o755);
  } else if (tmpFile.endsWith('.zip')) {
    const unzipResult = spawnSync('unzip', ['-o', tmpFile, '-d', dirname(binPath)], { stdio: 'pipe' });
    if (unzipResult.status !== 0) throw new Error(`unzip failed: ${(unzipResult.stderr || '').toString()}`);
    const extracted = join(dirname(binPath), asset.name.replace('.zip', ''));
    if (existsSync(extracted)) {
      spawnSync('mv', [extracted, binPath], { stdio: 'pipe' });
    }
  }

  // Clean up temp dir
  spawnSync('rm', ['-rf', tmpDir], { stdio: 'pipe' });

  // Create config dir
  mkdirSync(configDir, { recursive: true });

  // Install service (Linux only for now)
  let serviceInstalled = false;
  if (os === 'linux') {
    serviceInstalled = installSystemdService(binPath, configDir);
  } else if (os === 'darwin') {
    serviceInstalled = installLaunchdService(binPath, configDir);
  }

  // Verify
  try {
    const result = spawnSync(binPath, ['-v'], { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] });
    const ver = (result.stdout || '').trim();
    log(`Installed: ${ver}`);
    return { installed: true, version: ver, path: binPath, configDir, service: serviceInstalled };
  } catch {
    return { installed: true, version, path: binPath, configDir, service: serviceInstalled };
  }
}

function installSystemdService(binPath, configDir) {
  const unit = `[Unit]
Description=mihomo Daemon
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=${binPath} -d ${configDir}
Restart=on-failure
RestartSec=5
AmbientCapabilities=CAP_NET_ADMIN CAP_NET_RAW CAP_NET_BIND_SERVICE

[Install]
WantedBy=multi-user.target
`;

  try {
    // Try system-level service with sudo
    const servicePath = '/etc/systemd/system/mihomo.service';
    const result = spawnSync('sudo', ['tee', servicePath], {
      input: unit,
      stdio: ['pipe', 'pipe', 'pipe']
    });
    if (result.status === 0) {
      spawnSync('sudo', ['systemctl', 'daemon-reload'], { stdio: 'pipe' });
      spawnSync('sudo', ['systemctl', 'enable', 'mihomo'], { stdio: 'pipe' });
      return true;
    }
  } catch {}

  try {
    // Fallback to user service
    const userDir = join(homedir(), '.config', 'systemd', 'user');
    mkdirSync(userDir, { recursive: true });
    writeFileSync(join(userDir, 'mihomo.service'), unit);
    spawnSync('systemctl', ['--user', 'daemon-reload'], { stdio: 'pipe' });
    spawnSync('systemctl', ['--user', 'enable', 'mihomo'], { stdio: 'pipe' });
    return true;
  } catch {
    return false;
  }
}

function installLaunchdService(binPath, configDir) {
  try {
    const plist = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>com.mihomo.daemon</string>
    <key>ProgramArguments</key>
    <array>
        <string>${binPath}</string>
        <string>-d</string>
        <string>${configDir}</string>
    </array>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
</dict>
</plist>`;
    const agentsDir = join(homedir(), 'Library', 'LaunchAgents');
    mkdirSync(agentsDir, { recursive: true });
    const plistPath = join(agentsDir, 'com.mihomo.daemon.plist');
    writeFileSync(plistPath, plist);
    return true;
  } catch {
    return false;
  }
}
