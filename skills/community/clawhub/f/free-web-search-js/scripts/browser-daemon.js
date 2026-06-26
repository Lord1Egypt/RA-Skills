#!/usr/bin/env node
/**
 * browser-daemon.js — 持久化 Chromium 守护进程
 *
 * 用 Playwright launchServer() 启动常驻浏览器，
 * search.js / fetch.js 通过 CDP 复用，省去每次 1.5s+ 的 launch 开销。
 *
 * 自动退出：空闲超过 IDLE_TIMEOUT_MS（默认 10 分钟）daemon 自动 close + exit。
 *   客户端每次连接前会 touch 心跳文件 .browser-heartbeat，daemon 每 60s 检查一次。
 *
 * 用法：
 *   启动: node scripts/browser-daemon.js          (前台运行，建议 `&` 后台跑或交给 launcher)
 *   停止: node scripts/browser-daemon.js --stop
 *   状态: node scripts/browser-daemon.js --status
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { launchBrowserServer } from './playwright-support.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillRoot = path.resolve(__dirname, '..');
const ENDPOINT_FILE = path.join(skillRoot, '.browser-endpoint');
const HEARTBEAT_FILE = path.join(skillRoot, '.browser-heartbeat');

const IDLE_TIMEOUT_MS = parseInt(process.env.BROWSER_DAEMON_IDLE_MS || '600000', 10); // 10 min
const CHECK_INTERVAL_MS = 60_000; // 1 min

function readInfo() {
  try { return JSON.parse(fs.readFileSync(ENDPOINT_FILE, 'utf-8')); } catch { return null; }
}

function isAlive() {
  const info = readInfo();
  if (!info) return false;
  try { process.kill(info.pid, 0); return true; } catch {
    try { fs.unlinkSync(ENDPOINT_FILE); } catch {}
    try { fs.unlinkSync(HEARTBEAT_FILE); } catch {}
    return false;
  }
}

function readHeartbeat() {
  try {
    const raw = fs.readFileSync(HEARTBEAT_FILE, 'utf-8').trim();
    const ts = parseInt(raw, 10);
    return Number.isFinite(ts) ? ts : 0;
  } catch { return 0; }
}

function writeHeartbeat(ts) {
  try { fs.writeFileSync(HEARTBEAT_FILE, String(ts)); } catch {}
}

async function startDaemon() {
  if (isAlive()) {
    const info = readInfo();
    const uptime = ((Date.now() - info.startedAt) / 1000).toFixed(0);
    console.log(`[daemon] Already running  PID: ${info.pid}  Uptime: ${uptime}s`);
    console.log(`  WS: ${info.wsEndpoint}`);
    return;
  }

  const server = await launchBrowserServer({ headless: true });
  const wsEndpoint = server.wsEndpoint();
  const startedAt = Date.now();

  // 初始心跳：避免启动后立刻被判定空闲
  writeHeartbeat(startedAt);

  const info = {
    pid: process.pid,
    wsEndpoint,
    startedAt,
    idleTimeoutMs: IDLE_TIMEOUT_MS,
  };
  fs.writeFileSync(ENDPOINT_FILE, JSON.stringify(info, null, 2));

  console.log(`[daemon] Chromium started  PID: ${info.pid}`);
  console.log(`[daemon] WS: ${wsEndpoint}`);
  console.log(`[daemon] Idle exit after ${(IDLE_TIMEOUT_MS / 60000).toFixed(0)} min of inactivity`);

  let stopping = false;
  async function shutdown(reason) {
    if (stopping) return;
    stopping = true;
    console.log(`[daemon] Stopping (${reason})...`);
    try { await server.close(); } catch {}
    try { fs.unlinkSync(ENDPOINT_FILE); } catch {}
    try { fs.unlinkSync(HEARTBEAT_FILE); } catch {}
    process.exit(0);
  }

  // 空闲检查
  setInterval(() => {
    const last = readHeartbeat();
    const idleFor = Date.now() - last;
    if (idleFor > IDLE_TIMEOUT_MS) {
      shutdown(`idle ${(idleFor / 60000).toFixed(1)}min > ${(IDLE_TIMEOUT_MS / 60000).toFixed(0)}min`);
    }
  }, CHECK_INTERVAL_MS).unref?.();

  process.on('SIGINT', () => shutdown('SIGINT'));
  process.on('SIGTERM', () => shutdown('SIGTERM'));
}

function stopDaemon() {
  const info = readInfo();
  if (!info) { console.log('[daemon] Not running'); return; }
  try {
    process.kill(info.pid, 'SIGTERM');
    console.log(`[daemon] Stopped  PID: ${info.pid}`);
  } catch {
    console.log('[daemon] Process already exited');
  }
  try { fs.unlinkSync(ENDPOINT_FILE); } catch {}
  try { fs.unlinkSync(HEARTBEAT_FILE); } catch {}
}

function showStatus() {
  if (!isAlive()) { console.log('[daemon] Not running'); return; }
  const info = readInfo();
  const uptime = ((Date.now() - info.startedAt) / 1000).toFixed(0);
  const last = readHeartbeat();
  const idleSec = last ? ((Date.now() - last) / 1000).toFixed(0) : '?';
  console.log(`[daemon] Running  PID: ${info.pid}  Uptime: ${uptime}s  Idle: ${idleSec}s`);
  console.log(`  WS: ${info.wsEndpoint}`);
  console.log(`  Idle timeout: ${((info.idleTimeoutMs ?? IDLE_TIMEOUT_MS) / 60000).toFixed(0)} min`);
}

const arg = process.argv[2];
if (arg === '--stop') stopDaemon();
else if (arg === '--status') showStatus();
else startDaemon();
