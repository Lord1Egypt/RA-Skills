import { spawnSync, spawn } from 'child_process';
import { platform } from 'os';
import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { getBinaryPath, getConfigDir } from './platform.js';
import { log } from './logger.js';
import { homedir } from 'os';

const PID_FILE = join(process.env.XDG_CONFIG_HOME || join(homedir(), '.config'), 'mihomod', 'mihomo.pid');

function savePid(pid) {
  mkdirSync(dirname(PID_FILE), { recursive: true });
  writeFileSync(PID_FILE, String(pid));
}

function loadPid() {
  try {
    const pid = parseInt(readFileSync(PID_FILE, 'utf8').trim());
    if (!Number.isFinite(pid) || pid <= 0) return null;
    // Check if process is alive
    try { process.kill(pid, 0); return pid; } catch { return null; }
  } catch { return null; }
}

function clearPid() {
  try { writeFileSync(PID_FILE, ''); } catch {}
}

export async function startMihomo(config) {
  const os = platform();
  const binPath = config?.mihomo?.binaryPath || getBinaryPath();
  const configDir = config?.mihomo?.configPath ? dirname(config.mihomo.configPath) : getConfigDir();

  if (!existsSync(binPath)) {
    throw new Error(`mihomo not found at ${binPath}. Run 'mihomod install' first.`);
  }

  if (os === 'linux') {
    // Check if already running via systemd
    const isActive = spawnSync('systemctl', ['is-active', 'mihomo'], { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] });
    if (isActive.stdout?.trim() === 'active') {
      return { started: true, method: 'systemd', note: 'already running' };
    }

    // Try system systemd
    const sysResult = spawnSync('sudo', ['systemctl', 'start', 'mihomo'], { stdio: 'pipe' });
    if (sysResult.status === 0) return { started: true, method: 'systemd' };

    // Try user systemd
    const userActive = spawnSync('systemctl', ['--user', 'is-active', 'mihomo'], { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] });
    if (userActive.stdout?.trim() === 'active') {
      return { started: true, method: 'systemd-user', note: 'already running' };
    }

    const userResult = spawnSync('systemctl', ['--user', 'start', 'mihomo'], { stdio: 'pipe' });
    if (userResult.status === 0) return { started: true, method: 'systemd-user' };
  }

  if (os === 'darwin') {
    const result = spawnSync('launchctl', ['load', join(homedir(), 'Library', 'LaunchAgents', 'com.mihomo.daemon.plist')], { stdio: 'pipe' });
    if (result.status === 0) return { started: true, method: 'launchd' };
  }

  // Fallback: direct execution
  const child = spawn(binPath, ['-d', configDir], {
    detached: true,
    stdio: 'ignore'
  });
  child.unref();
  savePid(child.pid);

  // Wait a moment and verify it's still running
  await new Promise(r => setTimeout(r, 2000));
  const stillAlive = loadPid();
  if (!stillAlive) {
    throw new Error('mihomo started but exited immediately. Check config with: mihomo -t -d ' + configDir);
  }

  return { started: true, method: 'direct', pid: child.pid };
}

export async function stopMihomo(config) {
  const os = platform();

  if (os === 'linux') {
    const sysResult = spawnSync('sudo', ['systemctl', 'stop', 'mihomo'], { stdio: 'pipe' });
    if (sysResult.status === 0) return { stopped: true, method: 'systemd' };

    const userResult = spawnSync('systemctl', ['--user', 'stop', 'mihomo'], { stdio: 'pipe' });
    if (userResult.status === 0) return { stopped: true, method: 'systemd-user' };
  }

  if (os === 'darwin') {
    const result = spawnSync('launchctl', ['unload', join(homedir(), 'Library', 'LaunchAgents', 'com.mihomo.daemon.plist')], { stdio: 'pipe' });
    if (result.status === 0) return { stopped: true, method: 'launchd' };
  }

  // Try saved PID
  const pid = loadPid();
  if (pid) {
    try {
      process.kill(pid, 'SIGTERM');
      clearPid();
      return { stopped: true, method: 'pid', pid };
    } catch {}
  }

  // Last resort: pkill with exact binary name
  const result = spawnSync('pkill', ['-x', 'mihomo'], { stdio: 'pipe' });
  if (result.status === 0) {
    clearPid();
    return { stopped: true, method: 'pkill' };
  }

  return { stopped: false, error: 'Could not stop mihomo (not running?)' };
}
