#!/usr/bin/env node

require('../src/load-env')();
const fs = require('fs');
const path = require('path');
const os = require('os');
const chalk = require('chalk');

function resolveEnvFilePath() {
  const explicit = process.env.EKYBOT_COMPANION_ENV_FILE;
  if (explicit) {
    return path.resolve(explicit);
  }

  return path.join(process.cwd(), '.env.ekybot_companion');
}

function ensureSafePath(value, label) {
  if (/[\x00-\x1f]/.test(value)) {
    throw new Error(`Unsafe ${label}: contains control characters`);
  }
  return value;
}

function buildLaunchdPlist({ nodePath, daemonScript, workingDirectory, envFilePath }) {
  const logDir = path.join(os.homedir(), 'Library', 'Logs');
  const stdoutPath = path.join(logDir, 'ekybot-companion.log');
  const stderrPath = path.join(logDir, 'ekybot-companion.error.log');

  return `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.ekybot.companion</string>
  <key>ProgramArguments</key>
  <array>
    <string>${nodePath}</string>
    <string>${daemonScript}</string>
  </array>
  <key>WorkingDirectory</key>
  <string>${workingDirectory}</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>EKYBOT_COMPANION_ENV_FILE</key>
    <string>${envFilePath}</string>
  </dict>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>${stdoutPath}</string>
  <key>StandardErrorPath</key>
  <string>${stderrPath}</string>
</dict>
</plist>
`;
}

async function installLaunchdService() {
  const daemonScript = ensureSafePath(
    path.join(process.cwd(), 'scripts', 'companion-daemon.js'),
    'daemon script path'
  );
  const nodePath = ensureSafePath(process.execPath, 'node path');
  const workingDirectory = ensureSafePath(process.cwd(), 'working directory');
  const envFilePath = ensureSafePath(resolveEnvFilePath(), 'env file path');
  const plistPath = path.join(
    os.homedir(),
    'Library',
    'LaunchAgents',
    'com.ekybot.companion.plist'
  );

  fs.mkdirSync(path.dirname(plistPath), { recursive: true });
  fs.mkdirSync(path.join(os.homedir(), 'Library', 'Logs'), { recursive: true });

  const plistContent = buildLaunchdPlist({
    nodePath,
    daemonScript,
    workingDirectory,
    envFilePath,
  });

  fs.writeFileSync(plistPath, plistContent, 'utf8');

  console.log(chalk.green('✓ launchd plist created'));
  console.log(chalk.gray(`Plist: ${plistPath}`));
  console.log(chalk.gray(`Env file: ${envFilePath}`));
  console.log(chalk.blue('\nNext steps:'));
  console.log(chalk.gray(`  launchctl unload ${plistPath} 2>/dev/null || true`));
  console.log(chalk.gray(`  launchctl load ${plistPath}`));
  console.log(chalk.gray('  launchctl start com.ekybot.companion'));
  console.log(chalk.gray('  tail -f ~/Library/Logs/ekybot-companion.log'));
}

if (require.main === module) {
  installLaunchdService().catch((error) => {
    console.error(chalk.red(`Companion launchd install failed: ${error.message}`));
    process.exit(1);
  });
}

module.exports = installLaunchdService;
