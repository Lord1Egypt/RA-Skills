#!/usr/bin/env node
/**
 * ccproxy-ensure.js v6
 * 
 * Ensures the claude-cli-proxy is running on the configured port
 * and the persistent acpx session exists.
 * Called from HEARTBEAT.md and startup.
 * 
 * Respects same env vars as claude-cli-proxy.js:
 *   CCPROXY_PORT, CCPROXY_SESSION_NAME, CCPROXY_CWD / OPENCLAW_WORKSPACE
 */
const { execSync, spawn } = require('child_process');
const http = require('http');
const path = require('path');
const os = require('os');
const fs = require('fs');

const PORT = parseInt(process.env.CCPROXY_PORT || '8081', 10);
const SESSION_NAME = process.env.CCPROXY_SESSION_NAME || 'dexter-proxy';
const CWD = process.env.CCPROXY_CWD || process.env.OPENCLAW_WORKSPACE ||
  path.join(os.homedir(), '.openclaw', 'workspace');
const ENV = { ...process.env, ANTHROPIC_API_KEY: '' };
const PROXY_SCRIPT = path.join(CWD, 'claude-cli-proxy.js');

function isAlive() {
  return new Promise((resolve) => {
    const req = http.get(`http://127.0.0.1:${PORT}/health`, { timeout: 3000 }, (res) => {
      let data = '';
      res.on('data', (d) => data += d);
      res.on('end', () => {
        try { resolve(JSON.parse(data).status === 'ok'); }
        catch { resolve(false); }
      });
    });
    req.on('error', () => resolve(false));
    req.on('timeout', () => { req.destroy(); resolve(false); });
  });
}

function ensureSession() {
  try {
    const out = execSync('acpx claude sessions list 2>&1', {
      cwd: CWD, timeout: 10000, encoding: 'utf8', env: ENV,
    });
    if (!out.includes(SESSION_NAME)) {
      console.log(`Creating session "${SESSION_NAME}"...`);
      execSync(`acpx claude sessions new --name ${SESSION_NAME}`, {
        cwd: CWD, timeout: 10000, encoding: 'utf8', env: ENV,
      });
    }
  } catch (e) {
    console.error('Session check error:', e.message);
  }
}

function warmup() {
  try {
    console.log('Warming up session...');
    execSync(`acpx claude prompt -s ${SESSION_NAME} "warmup"`, {
      cwd: CWD, timeout: 30000, encoding: 'utf8', env: ENV,
    });
    console.log('Session warm.');
  } catch (e) {
    console.error('Warmup error:', e.message);
  }
}

(async () => {
  ensureSession();

  if (await isAlive()) {
    console.log('claude-cli-proxy: alive');
    return;
  }

  if (!fs.existsSync(PROXY_SCRIPT)) {
    console.error(`claude-cli-proxy: script not found at ${PROXY_SCRIPT}`);
    process.exit(1);
  }

  console.log('claude-cli-proxy: dead, starting...');
  const logPath = path.join(os.tmpdir(), 'claude-cli-proxy.log');
  const child = spawn('node', [PROXY_SCRIPT], {
    detached: true,
    stdio: ['ignore',
      fs.openSync(logPath, 'a'),
      fs.openSync(logPath, 'a')
    ],
    env: ENV,
  });
  child.unref();
  console.log(`claude-cli-proxy started (PID=${child.pid})`);

  await new Promise(r => setTimeout(r, 2000));
  warmup();
})();
