#!/usr/bin/env node
import { existsSync, mkdirSync, openSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn, spawnSync } from 'node:child_process';
import { homedir } from 'node:os';
import config from '../src/config.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
const STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(homedir(), '.openclaw', 'workspace', 'douyin-ops');
const LOG_DIR = join(STATE_DIR, 'logs');
const PID_PATH = join(STATE_DIR, 'douyin-daemon.lab.pid');
const LOG_PATH = join(LOG_DIR, 'douyin-daemon.lab.log');
const PORT = String(config.daemonPort);

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function stopOldProcess() {
  if (!existsSync(PID_PATH)) return null;
  const pid = Number(readFileSync(PID_PATH, 'utf8').trim());
  if (!Number.isInteger(pid) || pid <= 0 || pid === process.pid) return null;
  try {
    process.kill(pid, 'SIGTERM');
    return pid;
  } catch {
    return null;
  }
}

function hasCommand(command) {
  const result = spawnSync('bash', ['-lc', `command -v ${command} >/dev/null 2>&1`], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  return result.status === 0;
}

function spawnDaemonProcess(stdoutFd, stderrFd) {
  const hasDisplay = Boolean(process.env.DISPLAY || process.env.WAYLAND_DISPLAY);
  if (!hasDisplay && hasCommand('xvfb-run')) {
    return {
      mode: 'xvfb-run',
      child: spawn('xvfb-run', [
        '-a',
        '--server-args=-screen 0 1440x1000x24',
        process.execPath,
        'src/daemon/server.js',
      ], {
        cwd: ROOT,
        env: { ...process.env, BROWSER_HEADLESS: 'false', DOUYIN_USE_XVFB: 'true' },
        detached: true,
        stdio: ['ignore', stdoutFd, stderrFd],
      }),
    };
  }
  return {
    mode: hasDisplay ? 'display' : 'plain-no-display',
    child: spawn(process.execPath, ['src/daemon/server.js'], {
      cwd: ROOT,
      env: process.env,
      detached: true,
      stdio: ['ignore', stdoutFd, stderrFd],
    }),
  };
}

async function waitHealth(timeoutMs = 30_000) {
  const deadline = Date.now() + timeoutMs;
  let last = null;
  while (Date.now() < deadline) {
    try {
      const res = await fetch(`http://127.0.0.1:${PORT}/health`, { signal: AbortSignal.timeout(2000) });
      const payload = await res.json();
      last = { status: res.status, payload };
      if (res.ok && (payload.ok || payload.status === 'ok')) return { ok: true, ...last };
    } catch (err) {
      last = { error: err.message };
    }
    await sleep(1000);
  }
  return { ok: false, last };
}

async function main() {
  mkdirSync(LOG_DIR, { recursive: true });
  const stoppedPid = stopOldProcess();
  await sleep(stoppedPid ? 1000 : 0);

  const stdoutFd = openSync(LOG_PATH, 'a');
  const stderrFd = openSync(LOG_PATH, 'a');
  const { child, mode } = spawnDaemonProcess(stdoutFd, stderrFd);
  child.unref();
  writeFileSync(PID_PATH, `${child.pid}\n`);

  const health = await waitHealth();
  console.log(JSON.stringify({
    ok: health.ok,
    action: 'start_lab_daemon',
    stoppedPid,
    pid: child.pid,
    mode,
    port: PORT,
    logPath: LOG_PATH,
    health,
  }, null, 2));
  if (!health.ok) process.exit(1);
}

main().catch((err) => {
  console.log(JSON.stringify({ ok: false, action: 'start_lab_daemon', error: err.message, stack: err.stack }, null, 2));
  process.exit(1);
});
