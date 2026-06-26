import { platform, arch, homedir } from 'os';
import { join } from 'path';
import { existsSync } from 'fs';
import { execSync } from 'child_process';

export function getPlatform() {
  const os = platform();
  const a = arch();
  const mihomoArch = a === 'x64' ? 'amd64' : a === 'arm64' ? 'arm64' : a;
  let mihomoOS;
  if (os === 'linux') mihomoOS = 'linux';
  else if (os === 'darwin') mihomoOS = 'darwin';
  else if (os === 'win32') mihomoOS = 'windows';
  else mihomoOS = os;
  return { os, arch: a, mihomoOS, mihomoArch };
}

export function getBinaryPath() {
  const { os } = getPlatform();
  if (os === 'win32') {
    return join(process.env.APPDATA || join(homedir(), 'AppData', 'Roaming'), 'mihomod', 'mihomo.exe');
  }
  return join(homedir(), '.local', 'bin', 'mihomo');
}

export function getConfigDir() {
  const { os } = getPlatform();
  if (os === 'win32') {
    return join(process.env.APPDATA || join(homedir(), 'AppData', 'Roaming'), 'mihomo');
  }
  return join(homedir(), '.config', 'mihomo');
}

export function findBinary() {
  const p = getBinaryPath();
  if (existsSync(p)) return p;
  try {
    const cmd = platform() === 'win32' ? 'where mihomo' : 'which mihomo';
    return execSync(cmd, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] }).trim();
  } catch { return null; }
}
