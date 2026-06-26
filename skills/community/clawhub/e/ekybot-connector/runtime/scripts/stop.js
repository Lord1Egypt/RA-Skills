#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const chalk = require('chalk');

const PID_FILE = path.join(__dirname, '..', 'service.pid');

function stopService() {
  console.log(chalk.blue('🛑 Stopping Ekybot Connector...'));

  if (!fs.existsSync(PID_FILE)) {
    console.log(chalk.yellow('⚠️  Service is not running (no PID file found)'));
    return;
  }

  try {
    const pid = parseInt(fs.readFileSync(PID_FILE, 'utf8'));

    // Try to kill the process
    process.kill(pid, 'SIGTERM');

    // Wait a moment and check if it's still running
    setTimeout(() => {
      try {
        process.kill(pid, 0); // Check if process still exists
        console.log(chalk.yellow('⚠️  Process still running, forcing termination...'));
        process.kill(pid, 'SIGKILL');
      } catch (error) {
        // Process is gone, which is what we want
      }

      // Remove PID file
      if (fs.existsSync(PID_FILE)) {
        fs.unlinkSync(PID_FILE);
      }

      console.log(chalk.green('✓ Service stopped'));
    }, 2000);
  } catch (error) {
    if (error.code === 'ESRCH') {
      // Process not found, remove stale PID file
      fs.unlinkSync(PID_FILE);
      console.log(chalk.yellow('⚠️  Process was already stopped (removed stale PID file)'));
    } else {
      console.error(chalk.red(`❌ Failed to stop service: ${error.message}`));
    }
  }
}

// Run if called directly
if (require.main === module) {
  stopService();
}

module.exports = stopService;
