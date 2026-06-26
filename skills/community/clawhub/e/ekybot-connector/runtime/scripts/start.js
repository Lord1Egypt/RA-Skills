#!/usr/bin/env node

require('dotenv').config();
const fs = require('fs');
const path = require('path');
const chalk = require('chalk');
const TelemetryCollector = require('../src/telemetry');
const OpenClawConfigManager = require('../src/config-manager');

// PID file for service management
const PID_FILE = path.join(__dirname, '..', 'service.pid');

function writePidFile() {
  fs.writeFileSync(PID_FILE, process.pid.toString());
}

function removePidFile() {
  if (fs.existsSync(PID_FILE)) {
    fs.unlinkSync(PID_FILE);
  }
}

function isServiceRunning() {
  if (!fs.existsSync(PID_FILE)) {
    return false;
  }

  try {
    const pid = parseInt(fs.readFileSync(PID_FILE, 'utf8'));
    process.kill(pid, 0); // Check if process exists
    return true;
  } catch (error) {
    // Process doesn't exist, remove stale PID file
    removePidFile();
    return false;
  }
}

async function startTelemetryService() {
  console.log(chalk.blue.bold('🚀 Starting Ekybot Connector'));

  // Check if already running
  if (isServiceRunning()) {
    console.log(chalk.yellow('⚠️  Service is already running'));
    console.log(chalk.gray('Use "npm run stop" to stop the service first'));
    process.exit(1);
  }

  // Load configuration
  const configManager = new OpenClawConfigManager();

  if (!configManager.isEkybotConfigured()) {
    console.error(chalk.red('❌ Ekybot integration not configured'));
    console.error(chalk.yellow('Run "npm run register" first to set up the connection'));
    process.exit(1);
  }

  const config = configManager.getEkybotConfig();

  if (!config.workspace_id || !config.api_key) {
    console.error(chalk.red('❌ Invalid Ekybot configuration'));
    console.error(chalk.yellow('Run "npm run register" to reconfigure'));
    process.exit(1);
  }

  try {
    // Initialize telemetry collector
    const telemetry = new TelemetryCollector(config.api_key, config.workspace_id, {
      interval: config.telemetry_interval || 60000,
      wsUrl: config.endpoints?.websocket,
    });

    // Write PID file
    writePidFile();
    console.log(chalk.green(`✓ Service started (PID: ${process.pid})`));

    // Setup graceful shutdown
    process.on('SIGINT', shutdown);
    process.on('SIGTERM', shutdown);
    process.on('exit', removePidFile);

    let isShuttingDown = false;

    function shutdown() {
      if (isShuttingDown) return;
      isShuttingDown = true;

      console.log(chalk.yellow('\n📋 Shutting down...'));

      telemetry.stop();
      removePidFile();

      console.log(chalk.green('✓ Service stopped gracefully'));
      process.exit(0);
    }

    // Start telemetry collection
    await telemetry.start();

    console.log(chalk.green('✅ Ekybot Connector is now running'));
    console.log(chalk.gray(`Workspace ID: ${config.workspace_id}`));
    console.log(chalk.gray(`Telemetry interval: ${config.telemetry_interval || 60000}ms`));
    console.log(chalk.gray('View your dashboard at: https://ekybot.com'));
    console.log(chalk.gray('\nPress Ctrl+C to stop\n'));

    // Keep process alive and show periodic status
    setInterval(
      () => {
        const status = telemetry.getStatus();
        const timestamp = new Date().toISOString();

        console.log(
          chalk.blue(
            `[${timestamp}] Status: ${status.running ? 'Running' : 'Stopped'} | ` +
              `WebSocket: ${status.websocket_connected ? 'Connected' : 'Disconnected'} | ` +
              `Buffered: ${status.buffered_entries}`
          )
        );
      },
      5 * 60 * 1000
    ); // Status update every 5 minutes
  } catch (error) {
    console.error(chalk.red(`❌ Failed to start service: ${error.message}`));
    removePidFile();
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  startTelemetryService().catch((error) => {
    console.error(chalk.red(`Fatal error: ${error.message}`));
    removePidFile();
    process.exit(1);
  });
}

module.exports = startTelemetryService;
