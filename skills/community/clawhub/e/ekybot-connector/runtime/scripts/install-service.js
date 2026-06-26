#!/usr/bin/env node

require('dotenv').config();
const fs = require('fs');
const path = require('path');
const chalk = require('chalk');
const inquirer = require('inquirer');

async function installAsService() {
  console.log(chalk.blue.bold('🔧 Install Ekybot Connector as System Service'));
  console.log(chalk.gray('This will configure the connector to start automatically.\n'));

  const { serviceType } = await inquirer.prompt([
    {
      type: 'list',
      name: 'serviceType',
      message: 'Select service type:',
      choices: [
        { name: 'systemd (Linux)', value: 'systemd' },
        { name: 'launchd (macOS)', value: 'launchd' },
        { name: 'Manual (cross-platform)', value: 'manual' },
      ],
    },
  ]);

  switch (serviceType) {
    case 'systemd':
      await installSystemdService();
      break;
    case 'launchd':
      await installLaunchdService();
      break;
    case 'manual':
      showManualInstructions();
      break;
  }
}

// Escape a string for safe inclusion in service files (prevent injection)
function escapeServicePath(str) {
  // Reject paths with control characters or quotes that could break service files
  if (/[\x00-\x1f"'`$\\]/.test(str)) {
    throw new Error(`Unsafe path detected: "${str}". Rename directory to remove special characters.`);
  }
  return str;
}

async function installSystemdService() {
  const cwd = escapeServicePath(process.cwd());
  const execPath = escapeServicePath(process.execPath);
  const startScript = escapeServicePath(path.join(__dirname, 'start.js'));

  const serviceContent = `[Unit]
Description=Ekybot Connector
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=${cwd}
ExecStart=${execPath} ${startScript}
Restart=always
RestartSec=10
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
`;

  const servicePath = '/etc/systemd/system/ekybot-connector.service';

  try {
    console.log(chalk.blue('Creating systemd service file...'));
    console.log(chalk.gray(`Service file: ${servicePath}`));

    fs.writeFileSync(servicePath, serviceContent);

    console.log(chalk.green('✓ Service file created'));
    console.log(chalk.blue('To enable and start the service:'));
    console.log(chalk.gray('  sudo systemctl enable ekybot-connector'));
    console.log(chalk.gray('  sudo systemctl start ekybot-connector'));
  } catch (error) {
    console.error(chalk.red(`❌ Failed to create service: ${error.message}`));
    console.error(chalk.yellow('You may need to run this script with sudo'));
  }
}

async function installLaunchdService() {
  const cwd = escapeServicePath(process.cwd());
  const execPath = escapeServicePath(process.execPath);
  const startScript = escapeServicePath(path.join(__dirname, 'start.js'));

  const plistContent = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ekybot.connector</string>
    <key>ProgramArguments</key>
    <array>
        <string>${execPath}</string>
        <string>${startScript}</string>
    </array>
    <key>WorkingDirectory</key>
    <string>${cwd}</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
`;

  const plistPath = path.join(process.env.HOME, 'Library/LaunchAgents/com.ekybot.connector.plist');

  try {
    console.log(chalk.blue('Creating launchd plist file...'));
    console.log(chalk.gray(`Plist file: ${plistPath}`));

    fs.writeFileSync(plistPath, plistContent);

    console.log(chalk.green('✓ Plist file created'));
    console.log(chalk.blue('To load and start the service:'));
    console.log(chalk.gray('  launchctl load ~/Library/LaunchAgents/com.ekybot.connector.plist'));
  } catch (error) {
    console.error(chalk.red(`❌ Failed to create plist: ${error.message}`));
  }
}

function showManualInstructions() {
  console.log(chalk.blue('📋 Manual Service Setup Instructions'));
  console.log(chalk.gray('\nTo run the connector automatically:'));
  console.log(chalk.gray(''));
  console.log(chalk.gray('1. Create a startup script that runs:'));
  console.log(chalk.gray(`   cd ${process.cwd()}`));
  console.log(chalk.gray('   npm run start'));
  console.log(chalk.gray(''));
  console.log(chalk.gray('2. Add this script to your system startup:'));
  console.log(chalk.gray('   - Linux: ~/.profile or ~/.bashrc'));
  console.log(chalk.gray('   - macOS: Login Items in System Preferences'));
  console.log(chalk.gray('   - Windows: Task Scheduler or startup folder'));
  console.log(chalk.gray(''));
  console.log(chalk.gray('3. Test with:'));
  console.log(chalk.gray('   npm run start'));
}

// Run if called directly
if (require.main === module) {
  installAsService().catch((error) => {
    console.error(chalk.red(`Installation failed: ${error.message}`));
    process.exit(1);
  });
}

module.exports = installAsService;
