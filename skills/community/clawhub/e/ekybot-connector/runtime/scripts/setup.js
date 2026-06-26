#!/usr/bin/env node

require('dotenv').config();
const chalk = require('chalk');
const inquirer = require('inquirer');
const OpenClawConfigManager = require('../src/config-manager');

async function setupIntegration() {
  console.log(chalk.blue.bold('⚙️  Ekybot Integration Setup'));
  console.log(chalk.gray('Configuring OpenClaw integration settings...\n'));

  const configManager = new OpenClawConfigManager();

  // Validate OpenClaw installation
  const validation = configManager.validateOpenClawInstallation();

  if (!validation.configExists) {
    console.error(chalk.red('❌ OpenClaw configuration not found'));
    console.error(chalk.red(`Expected at: ${configManager.configPath}`));
    process.exit(1);
  }

  // Check if Ekybot is already configured
  if (!configManager.isEkybotConfigured()) {
    console.error(chalk.red('❌ Ekybot integration not configured'));
    console.error(chalk.yellow('Run "npm run register" first to connect your workspace'));
    process.exit(1);
  }

  const currentConfig = configManager.getEkybotConfig();

  console.log(chalk.green('✓ Current configuration found:'));
  console.log(chalk.gray(`  Workspace ID: ${currentConfig.workspace_id}`));
  console.log(
    chalk.gray(`  Telemetry: ${currentConfig.telemetry_enabled ? 'Enabled' : 'Disabled'}`)
  );
  console.log(chalk.gray(`  Interval: ${currentConfig.telemetry_interval || 60000}ms\n`));

  // Configuration options
  const answers = await inquirer.prompt([
    {
      type: 'confirm',
      name: 'enableTelemetry',
      message: 'Enable telemetry streaming?',
      default: currentConfig.telemetry_enabled,
    },
    {
      type: 'number',
      name: 'telemetryInterval',
      message: 'Telemetry interval (milliseconds):',
      default: currentConfig.telemetry_interval || 60000,
      when: (answers) => answers.enableTelemetry,
      validate: (input) => {
        if (input < 10000) {
          return 'Interval must be at least 10 seconds (10000ms)';
        }
        if (input > 600000) {
          return 'Interval cannot exceed 10 minutes (600000ms)';
        }
        return true;
      },
    },
    {
      type: 'input',
      name: 'apiUrl',
      message: 'API endpoint URL:',
      default: currentConfig.endpoints?.api || 'https://api.ekybot.com',
      validate: (input) => {
        try {
          new URL(input);
          return true;
        } catch {
          return 'Please enter a valid URL';
        }
      },
    },
    {
      type: 'input',
      name: 'wsUrl',
      message: 'WebSocket endpoint URL:',
      default: currentConfig.endpoints?.websocket || 'wss://api.ekybot.com/ws',
      validate: (input) => {
        if (!input.startsWith('ws://') && !input.startsWith('wss://')) {
          return 'WebSocket URL must start with ws:// or wss://';
        }
        return true;
      },
    },
  ]);

  try {
    // Update configuration
    const config = configManager.readConfig();

    config.integrations.ekybot = {
      ...config.integrations.ekybot,
      telemetry_enabled: answers.enableTelemetry,
      telemetry_interval: answers.telemetryInterval || 60000,
      endpoints: {
        api: answers.apiUrl,
        websocket: answers.wsUrl,
      },
      updated_at: new Date().toISOString(),
    };

    configManager.writeConfig(config);

    console.log(chalk.green('\n✅ Configuration updated successfully!'));
    console.log(chalk.gray('\nNew settings:'));
    console.log(chalk.gray(`  Telemetry: ${answers.enableTelemetry ? 'Enabled' : 'Disabled'}`));

    if (answers.enableTelemetry) {
      console.log(chalk.gray(`  Interval: ${answers.telemetryInterval}ms`));
    }

    console.log(chalk.gray(`  API URL: ${answers.apiUrl}`));
    console.log(chalk.gray(`  WebSocket URL: ${answers.wsUrl}`));

    // Restart recommendation
    console.log(chalk.blue('\n💡 Recommendations:'));
    console.log(chalk.blue('• Run "npm run test-connection" to verify settings'));
    console.log(chalk.blue('• Restart the service with "npm run restart" to apply changes'));
    console.log(chalk.blue('• Use "npm run health" to monitor the integration'));
  } catch (error) {
    console.error(chalk.red(`\n❌ Failed to update configuration: ${error.message}`));
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  setupIntegration().catch((error) => {
    console.error(chalk.red(`Setup failed: ${error.message}`));
    process.exit(1);
  });
}

module.exports = setupIntegration;
