#!/usr/bin/env node
/**
 * Courtroom CLI - start/stop/status commands
 */

const { spawn, exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const COURTROOM_DIR = path.join(process.env.HOME || '', '.openclaw', 'courtroom');
const PID_FILE = path.join(COURTROOM_DIR, 'daemon.pid');
const CONFIG_FILE = path.join(COURTROOM_DIR, 'config.json');

function getDaemonPath() {
  return path.join(__dirname, '..', 'daemon.js');
}

function isRunning() {
  if (!fs.existsSync(PID_FILE)) return false;
  try {
    const pid = parseInt(fs.readFileSync(PID_FILE, 'utf8'));
    // Check if process exists
    process.kill(pid, 0);
    return true;
  } catch (e) {
    return false;
  }
}

function savePid(pid) {
  fs.writeFileSync(PID_FILE, pid.toString());
}

function removePid() {
  if (fs.existsSync(PID_FILE)) {
    fs.unlinkSync(PID_FILE);
  }
}

function loadConfig() {
  if (fs.existsSync(CONFIG_FILE)) {
    try {
      return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
    } catch (e) {
      return {};
    }
  }
  return {};
}

const command = process.argv[2];

switch (command) {
  case 'start':
    if (isRunning()) {
      console.log('⚖️  Courtroom daemon is already running');
      process.exit(0);
    }
    
    console.log('🚀 Starting Courtroom daemon...');
    const daemon = spawn('node', [getDaemonPath(), 'start'], {
      detached: true,
      stdio: ['ignore', 'ignore', 'ignore']
    });
    
    savePid(daemon.pid);
    daemon.unref();
    
    console.log('✅ Daemon started (PID:', daemon.pid + ')');
    console.log('📊 Check status: courtroom-status');
    break;
    
  case 'stop':
    if (!isRunning()) {
      console.log('⏸️  Courtroom daemon is not running');
      process.exit(0);
    }
    
    console.log('🛑 Stopping Courtroom daemon...');
    
    try {
      const pid = parseInt(fs.readFileSync(PID_FILE, 'utf8'));
      process.kill(pid, 'SIGTERM');
      removePid();
      console.log('✅ Daemon stopped');
    } catch (e) {
      console.log('❌ Error stopping daemon:', e.message);
      // Force kill
      exec('pkill -f "courtroom-daemon"');
      removePid();
    }
    break;
    
  case 'status':
    const running = isRunning();
    const config = loadConfig();
    
    console.log('⚖️  ClawTrial Courtroom Status');
    console.log('');
    console.log(`   Daemon: ${running ? '🟢 Running' : '🔴 Stopped'}`);
    console.log(`   API Endpoint: ${config.apiEndpoint || 'Not configured'}`);
    console.log(`   Analysis Interval: ${config.analysisIntervalMinutes || 5} minutes`);
    console.log(`   Confidence Threshold: ${(config.confidenceThreshold || 0.6) * 100}%`);
    
    if (running) {
      // Try to get detailed status from daemon
      const http = require('http');
      const req = http.get('http://localhost:8765/status', (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const status = JSON.parse(data);
            console.log(`   Messages Tracked: ${status.messageCount}`);
            console.log(`   Cases Filed: ${status.casesFiled}`);
          } catch (e) {
            // Ignore
          }
        });
      });
      req.on('error', () => {});
    }
    break;
    
  case 'enable':
    const cfg = loadConfig();
    cfg.enabled = true;
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(cfg, null, 2));
    console.log('✅ Courtroom enabled');
    console.log('Start with: courtroom-start');
    break;
    
  case 'disable':
    const cfg2 = loadConfig();
    cfg2.enabled = false;
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(cfg2, null, 2));
    console.log('⏸️  Courtroom disabled');
    if (isRunning()) {
      console.log('Stop with: courtroom-stop');
    }
    break;
    
  default:
    console.log('⚖️  ClawTrial Courtroom');
    console.log('');
    console.log('Commands:');
    console.log('  courtroom-start    - Start the daemon');
    console.log('  courtroom-stop     - Stop the daemon');
    console.log('  courtroom-status   - Show status');
    console.log('  courtroom-enable   - Enable auto-start');
    console.log('  courtroom-disable  - Disable auto-start');
    console.log('');
    console.log('Config: ~/.openclaw/courtroom/config.json');
}
