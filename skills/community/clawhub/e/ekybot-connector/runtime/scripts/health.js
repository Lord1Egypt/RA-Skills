#!/usr/bin/env node

require('dotenv').config();
const fs = require('fs');
const path = require('path');
const chalk = require('chalk');
const EkybotApiClient = require('../src/api-client');
const OpenClawConfigManager = require('../src/config-manager');

const PID_FILE = path.join(__dirname, '..', 'service.pid');

async function checkHealth() {
  console.log(chalk.blue.bold('🔍 Ekybot Connector Health Check\n'));

  const results = {
    service: { status: 'unknown', details: '' },
    openclaw: { status: 'unknown', details: '' },
    ekybot_config: { status: 'unknown', details: '' },
    api_connection: { status: 'unknown', details: '' },
  };

  // 1. Check service status
  console.log(chalk.blue('📋 Checking service status...'));
  try {
    if (!fs.existsSync(PID_FILE)) {
      results.service = { status: 'stopped', details: 'No PID file found' };
      console.log(chalk.yellow('  ⚠️  Service is not running'));
    } else {
      const pid = parseInt(fs.readFileSync(PID_FILE, 'utf8'));
      try {
        process.kill(pid, 0); // Check if process exists
        results.service = { status: 'running', details: `PID: ${pid}` };
        console.log(chalk.green(`  ✓ Service is running (PID: ${pid})`));
      } catch (error) {
        results.service = { status: 'stopped', details: 'Stale PID file' };
        console.log(chalk.red('  ❌ Service appears stopped (stale PID file)'));
      }
    }
  } catch (error) {
    results.service = { status: 'error', details: error.message };
    console.log(chalk.red(`  ❌ Error checking service: ${error.message}`));
  }

  // 2. Check OpenClaw installation
  console.log(chalk.blue('\n🔧 Checking OpenClaw installation...'));
  try {
    const configManager = new OpenClawConfigManager();
    const validation = configManager.validateOpenClawInstallation();

    if (validation.configExists && validation.configValid) {
      results.openclaw = { status: 'ok', details: `Config at ${configManager.configPath}` };
      console.log(chalk.green('  ✓ OpenClaw installation is valid'));
      console.log(chalk.gray(`    Config: ${configManager.configPath}`));
      console.log(chalk.gray(`    Agents dir: ${validation.agentsDir ? 'Found' : 'Not found'}`));
    } else {
      const issues = [];
      if (!validation.configExists) issues.push('Config missing');
      if (!validation.configValid) issues.push('Config invalid');
      if (!validation.agentsDir) issues.push('Agents directory missing');

      results.openclaw = { status: 'error', details: issues.join(', ') };
      console.log(chalk.red(`  ❌ OpenClaw issues: ${issues.join(', ')}`));
    }
  } catch (error) {
    results.openclaw = { status: 'error', details: error.message };
    console.log(chalk.red(`  ❌ Error checking OpenClaw: ${error.message}`));
  }

  // 3. Check Ekybot configuration
  console.log(chalk.blue('\n⚙️  Checking Ekybot configuration...'));
  try {
    const configManager = new OpenClawConfigManager();

    if (configManager.isEkybotConfigured()) {
      const config = configManager.getEkybotConfig();
      results.ekybot_config = {
        status: 'ok',
        details: `Workspace: ${config.workspace_id}`,
      };
      console.log(chalk.green('  ✓ Ekybot integration is configured'));
      console.log(chalk.gray(`    Workspace ID: ${config.workspace_id}`));
      console.log(
        chalk.gray(`    Telemetry: ${config.telemetry_enabled ? 'Enabled' : 'Disabled'}`)
      );
      console.log(chalk.gray(`    Interval: ${config.telemetry_interval}ms`));
    } else {
      results.ekybot_config = { status: 'missing', details: 'Not configured' };
      console.log(chalk.yellow('  ⚠️  Ekybot integration not configured'));
      console.log(chalk.gray('    Run "npm run register" to configure'));
    }
  } catch (error) {
    results.ekybot_config = { status: 'error', details: error.message };
    console.log(chalk.red(`  ❌ Error checking configuration: ${error.message}`));
  }

  // 4. Check API connection
  console.log(chalk.blue('\n🌐 Checking API connection...'));
  try {
    const configManager = new OpenClawConfigManager();

    if (configManager.isEkybotConfigured()) {
      const config = configManager.getEkybotConfig();
      const apiClient = new EkybotApiClient(config.api_key, config.endpoints?.api);

      const startTime = Date.now();
      const response = await apiClient.healthCheck();
      const responseTime = Date.now() - startTime;

      if (response.status === 'ok' || response.status === 'healthy') {
        results.api_connection = {
          status: 'ok',
          details: `Response time: ${responseTime}ms`,
        };
        console.log(chalk.green(`  ✓ API connection is healthy (${responseTime}ms)`));
      } else {
        results.api_connection = { status: 'degraded', details: response.status };
        console.log(chalk.yellow(`  ⚠️  API response: ${response.status}`));
      }
    } else {
      results.api_connection = { status: 'skipped', details: 'No configuration' };
      console.log(chalk.gray('  ⏭  Skipped (no configuration)'));
    }
  } catch (error) {
    results.api_connection = { status: 'error', details: error.message };
    console.log(chalk.red(`  ❌ API connection failed: ${error.message}`));
  }

  // Summary
  console.log(chalk.blue.bold('\n📊 Health Check Summary:'));

  const statusColors = {
    ok: chalk.green,
    running: chalk.green,
    stopped: chalk.yellow,
    missing: chalk.yellow,
    skipped: chalk.gray,
    degraded: chalk.yellow,
    error: chalk.red,
    unknown: chalk.red,
  };

  Object.entries(results).forEach(([component, result]) => {
    const colorFn = statusColors[result.status] || chalk.red;
    console.log(
      `  ${component.padEnd(15)}: ${colorFn(result.status)} ${chalk.gray(result.details)}`
    );
  });

  // Overall status
  const hasErrors = Object.values(results).some((r) => r.status === 'error');
  const hasWarnings = Object.values(results).some(
    (r) => r.status === 'stopped' || r.status === 'missing'
  );

  if (hasErrors) {
    console.log(chalk.red('\n❌ Health check failed - errors detected'));
    process.exit(1);
  } else if (hasWarnings) {
    console.log(chalk.yellow('\n⚠️  Health check completed with warnings'));
    process.exit(0);
  } else {
    console.log(chalk.green('\n✅ All systems healthy'));
    process.exit(0);
  }
}

// Run if called directly
if (require.main === module) {
  checkHealth().catch((error) => {
    console.error(chalk.red(`Health check failed: ${error.message}`));
    process.exit(1);
  });
}

module.exports = checkHealth;
