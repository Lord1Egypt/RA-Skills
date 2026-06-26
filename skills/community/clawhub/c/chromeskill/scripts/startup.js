#!/usr/bin/env node

/**
 * Chrome AI Action — Skill Startup Script
 *
 * Responsibilities:
 *   1. Check if npm package "chrome-ai-action" is installed globally
 *   2. If not, install it via npm install -g
 *   3. Check if bridge is already running on target port
 *   4. If not running, launch the bridge
 *   5. Wait for bridge to be ready, then return status
 *
 * The bridge will auto-launch Chrome if not already running with CDP.
 *
 * Usage: node scripts/startup.js
 */

const http = require('http');
const { execSync, spawn } = require('child_process');
const path = require('path');
const os = require('os');

const BRIDGE_PORT = Math.max(1, parseInt(process.env.CAA_BRIDGE_PORT || '9876', 10) || 9876);
const STARTUP_TIMEOUT = Math.max(5000, parseInt(process.env.CAA_STARTUP_TIMEOUT || '60000', 10) || 60000);
const isWindows = os.platform() === 'win32';

function log(msg) {
  console.error(`[chrome-ai-action-skill] ${msg}`);
}

function isBridgeRunning() {
  return new Promise((resolve) => {
    const req = http.get(`http://127.0.0.1:${BRIDGE_PORT}/health`, (res) => {
      let data = '';
      res.setTimeout(2000, () => { req.destroy(); resolve(false); });
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const j = JSON.parse(data.trim());
          resolve(j.status === 'ok' && j.bridgePort === BRIDGE_PORT);
        } catch {
          resolve(false);
        }
      });
    });
    req.on('error', () => resolve(false));
    req.setTimeout(2000, () => { req.destroy(); resolve(false); });
  });
}

function ensurePackageInstalled() {
  try {
    execSync('npm list -g chrome-ai-action --depth=0', { stdio: 'pipe' });
    const command = isWindows ? 'where chrome-ai-action.cmd' : 'which chrome-ai-action';
    execSync(command, { stdio: 'pipe' });
    return true;
  } catch {
    return false;
  }
}

function getGlobalNodeModulesPath() {
  try {
    return execSync('npm root -g', { encoding: 'utf-8', stdio: 'pipe' }).trim();
  } catch {
    return 'unknown';
  }
}

function installPackage() {
  log('Installing chrome-ai-action globally...');
  try {
    execSync('npm install -g chrome-ai-action', { stdio: 'inherit' });
    const pkgPath = path.join(getGlobalNodeModulesPath(), 'chrome-ai-action');
    log(`Installation complete at: ${pkgPath}`);
  } catch (err) {
    log(`Failed to install: ${err.message}`);
    process.exit(1);
  }
}

function launchBridge() {
  const command = isWindows ? 'chrome-ai-action.cmd' : 'chrome-ai-action';
  log(`Starting bridge on port ${BRIDGE_PORT}...`);
  const child = spawn(command, ['--port', String(BRIDGE_PORT)], {
    stdio: 'inherit',
    detached: false,
  });
  child.on('error', (err) => {
    log(`Failed to start bridge: ${err.message}`);
    process.exit(1);
  });
  child.on('exit', (code) => {
    if (code !== null && code !== 0) {
      log(`Bridge exited with code ${code}`);
    }
  });
  return child;
}

function waitForBridge(timeoutMs) {
  return new Promise((resolve, reject) => {
    const start = Date.now();
    const poll = () => {
      isBridgeRunning().then((running) => {
        if (running) {
          resolve(true);
          return;
        }
        if (Date.now() - start > timeoutMs) {
          reject(new Error(`Bridge did not become ready within ${timeoutMs}ms`));
          return;
        }
        setTimeout(poll, 500);
      }).catch(() => setTimeout(poll, 500));
    };
    poll();
  });
}

async function main() {
  log('Chrome AI Action — Skill Startup');
  log(`Bridge port: ${BRIDGE_PORT}`);

  const alreadyRunning = await isBridgeRunning();
  if (alreadyRunning) {
    log(`Bridge already running on port ${BRIDGE_PORT}. Skipping startup.`);
    console.log(JSON.stringify({
      status: 'already_running',
      port: BRIDGE_PORT,
      action: 'skip',
    }));
    return;
  }

  if (!ensurePackageInstalled()) {
    installPackage();
  } else {
    const pkgPath = path.join(getGlobalNodeModulesPath(), 'chrome-ai-action');
    log(`chrome-ai-action already installed at: ${pkgPath}`);
  }

  launchBridge();

  try {
    await waitForBridge(STARTUP_TIMEOUT);
    log('Bridge is ready.');
    console.log(JSON.stringify({
      status: 'started',
      port: BRIDGE_PORT,
      action: 'launch',
    }));
  } catch (err) {
    log(`Error: ${err.message}`);
    console.log(JSON.stringify({
      status: 'error',
      port: BRIDGE_PORT,
      error: err.message,
    }));
    process.exit(1);
  }
}

main();
