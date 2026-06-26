#!/usr/bin/env node
/**
 * Post-install script - auto-starts the courtroom daemon
 */

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const COURTROOM_DIR = path.join(process.env.HOME || '', '.openclaw', 'courtroom');
const CONFIG_FILE = path.join(COURTROOM_DIR, 'config.json');

function ensureDir() {
  if (!fs.existsSync(COURTROOM_DIR)) {
    fs.mkdirSync(COURTROOM_DIR, { recursive: true });
  }
}

function loadConfig() {
  ensureDir();
  if (fs.existsSync(CONFIG_FILE)) {
    try {
      return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
    } catch (e) {
      return {};
    }
  }
  return {};
}

function saveConfig(config) {
  ensureDir();
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
}

console.log('⚖️  ClawTrial Courtroom - Post Install');
console.log('');

// Initialize config if not exists
const config = loadConfig();
if (!config.apiEndpoint) {
  config.apiEndpoint = 'https://api.clawtrial.com/cases';
  config.analysisIntervalMinutes = 5;
  config.confidenceThreshold = 0.6;
  config.enabled = true;
  config.autoStart = true;
  saveConfig(config);
  console.log('✅ Default configuration created');
}

// Auto-start if enabled
if (config.autoStart !== false) {
  console.log('🚀 Auto-starting daemon...');
  
  const daemonPath = path.join(__dirname, '..', 'daemon.js');
  const daemon = spawn('node', [daemonPath, 'start'], {
    detached: true,
    stdio: 'ignore'
  });
  
  daemon.unref();
  
  console.log('✅ Daemon started in background');
  console.log('');
  console.log('To check status: courtroom-status');
  console.log('To stop: courtroom-stop');
  console.log('To configure: edit ~/.openclaw/courtroom/config.json');
} else {
  console.log('⏸️  Auto-start disabled');
  console.log('To start manually: courtroom-start');
}
