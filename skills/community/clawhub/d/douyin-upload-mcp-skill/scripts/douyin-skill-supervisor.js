#!/usr/bin/env node
import { createWriteStream, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import { homedir } from 'node:os';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const stateDir = process.env.DOUYIN_MONITOR_STATE_DIR || join(homedir(), '.openclaw', 'workspace', 'douyin-ops');
const logDir = join(stateDir, 'logs');
const scheduleConfigPath = join(stateDir, 'schedule-config.json');
const daemonPort = Number(process.env.DAEMON_PORT || 40225);
const healthUrl = `http://127.0.0.1:${daemonPort}/health`;

mkdirSync(logDir, { recursive: true });

const children = new Map();
let shuttingDown = false;

function timestamp() {
  return new Date().toISOString();
}

function log(message) {
  process.stdout.write(`[${timestamp()}] ${message}\n`);
}

function childLogStream(name) {
  return createWriteStream(join(logDir, `${name}.log`), { flags: 'a' });
}

function startManaged(name, args, opts = {}) {
  if (children.has(name)) return children.get(name);
  const stdout = childLogStream(name);
  const stderr = childLogStream(name);
  const child = spawn(process.execPath, args, {
    cwd: root,
    env: process.env,
    stdio: ['ignore', 'pipe', 'pipe'],
    detached: false,
  });
  child.stdout.pipe(stdout);
  child.stderr.pipe(stderr);
  children.set(name, child);
  log(`${name} started pid=${child.pid}`);
  child.on('exit', (code, signal) => {
    children.delete(name);
    stdout.end();
    stderr.end();
    log(`${name} exited code=${code ?? ''} signal=${signal ?? ''}`);
    if (!shuttingDown && opts.restart !== false) {
      const delay = Number(opts.restartDelayMs || 3000);
      setTimeout(() => startManaged(name, args, opts), delay);
    }
  });
  return child;
}

function stopManaged(name, signal = 'SIGTERM') {
  const child = children.get(name);
  if (!child) return false;
  children.delete(name);
  try {
    child.kill(signal);
  } catch {
    // Already gone.
  }
  log(`${name} stopping signal=${signal}`);
  return true;
}

async function daemonHealthy() {
  try {
    const res = await fetch(healthUrl, { signal: AbortSignal.timeout(2500) });
    const payload = await res.json();
    return Boolean(payload?.ok);
  } catch {
    return false;
  }
}

async function ensureDaemon() {
  if (await daemonHealthy()) return;
  if (children.has('douyin-daemon')) return;
  startManaged('douyin-daemon', ['src/daemon/server.js'], {
    restart: true,
    restartDelayMs: 3000,
  });
}

function ensureWatcher() {
  if (process.env.DOUYIN_SUPERVISOR_START_WATCHER !== 'true') {
    return;
  }
  startManaged('feishu-reply-watcher', [
    'scripts/feishu-reply-watcher.js',
    'watch',
    '--since-seconds',
    process.env.DOUYIN_WATCH_SINCE_SECONDS || '1800',
    '--interval-ms',
    process.env.DOUYIN_WATCH_INTERVAL_MS || '1000',
    '--page-size',
    process.env.DOUYIN_WATCH_PAGE_SIZE || '50',
    '--max-pages',
    process.env.DOUYIN_WATCH_MAX_PAGES || '10',
  ], {
    restart: true,
    restartDelayMs: 3000,
  });
}

function ensureLocalScheduler() {
  if (process.env.DOUYIN_SUPERVISOR_START_SCHEDULER === 'false') {
    stopManaged('douyin-local-scheduler');
    return;
  }
  if (!shouldStartLocalScheduler()) {
    stopManaged('douyin-local-scheduler');
    return;
  }
  startManaged('douyin-local-scheduler', [
    'scripts/douyin-schedule-manager.js',
    'local-scheduler-loop',
  ], {
    restart: true,
    restartDelayMs: 3000,
  });
}

function shouldStartLocalScheduler() {
  if (!existsSync(scheduleConfigPath)) return true;
  try {
    const config = JSON.parse(readFileSync(scheduleConfigPath, 'utf8'));
    if (config.enabled === false) return false;
    const jobs = Object.values(config.jobs || {});
    if (jobs.length && jobs.every((job) => job?.enabled === false)) return false;
    return true;
  } catch (err) {
    log(`schedule config read failed, keeping scheduler enabled: ${err.message}`);
    return true;
  }
}

async function loop() {
  await ensureDaemon();
  ensureWatcher();
  ensureLocalScheduler();
  setInterval(async () => {
    await ensureDaemon();
    ensureWatcher();
    ensureLocalScheduler();
  }, 10_000).unref();
}

function shutdown(signal) {
  shuttingDown = true;
  log(`received ${signal}, stopping children`);
  for (const child of children.values()) {
    try {
      child.kill('SIGTERM');
    } catch {
      // Already gone.
    }
  }
  setTimeout(() => process.exit(0), 3000).unref();
}

for (const signal of ['SIGINT', 'SIGTERM', 'SIGHUP']) {
  process.on(signal, () => shutdown(signal));
}

process.on('uncaughtException', (err) => {
  log(`uncaughtException: ${err.stack || err.message}`);
});

process.on('unhandledRejection', (reason) => {
  log(`unhandledRejection: ${reason?.stack || reason}`);
});

if (!existsSync(root)) {
  log(`root missing: ${root}`);
  process.exit(1);
}

log('douyin skill supervisor starting');
loop().catch((err) => {
  log(`startup failed: ${err.stack || err.message}`);
  process.exit(1);
});
