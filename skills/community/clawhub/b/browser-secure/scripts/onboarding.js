#!/usr/bin/env node

/**
 * Browser-Secure Onboarding (Smoothed)
 * 
 * Flow:
 * 1. Check prerequisites
 * 2. Auto-install missing dependencies (with permission)
 * 3. Build and link
 * 4. Configure
 */

import { execSync, spawn } from 'child_process';
import fs from 'fs';
import path from 'path';
import os from 'os';
import readline from 'readline';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function ask(question) {
  return new Promise(resolve => {
    rl.question(question, answer => resolve(answer.trim()));
  });
}

function isMac() {
  return process.platform === 'darwin';
}

function isLinux() {
  return process.platform === 'linux';
}

function hasBrew() {
  try {
    execSync('which brew', { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

function getNodeVersion() {
  try {
    const version = process.version.slice(1);
    const major = parseInt(version.split('.')[0]);
    return major;
  } catch {
    return 0;
  }
}

// Check functions
const checks = {
  node: {
    name: 'Node.js 18+',
    check: () => getNodeVersion() >= 18,
    required: true,
    autoFixable: false,
    fixHint: 'Install from https://nodejs.org/ or use: nvm install 18'
  },
  npm: {
    name: 'npm',
    check: () => {
      try {
        execSync('which npm', { stdio: 'ignore' });
        return true;
      } catch {
        return false;
      }
    },
    required: true,
    autoFixable: false,
    fixHint: 'Install Node.js (includes npm)'
  },
  chrome: {
    name: 'Google Chrome',
    check: () => {
      try {
        const chromePaths = [
          '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
          '/usr/bin/google-chrome',
          '/usr/bin/chromium',
          '/usr/bin/chromium-browser',
          'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
          'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
        ];
        for (const p of chromePaths) {
          if (fs.existsSync(p)) return true;
        }
        execSync('which google-chrome', { stdio: 'ignore' });
        return true;
      } catch {
        return false;
      }
    },
    required: true,
    autoFixable: false,
    fixHint: 'Install from https://google.com/chrome'
  },
  playwrightDeps: {
    name: 'Playwright browser deps',
    check: () => {
      try {
        // Check if playwright is installed
        const result = execSync('npx playwright --version', { 
          stdio: ['pipe', 'pipe', 'ignore'],
          encoding: 'utf8'
        });
        return result.includes('Version');
      } catch {
        return false;
      }
    },
    required: true,
    autoFixable: true,
    installCmd: () => 'npx playwright install chromium'
  },
  bitwarden: {
    name: 'Bitwarden CLI',
    check: () => {
      try {
        execSync('which bw', { stdio: 'ignore' });
        return true;
      } catch {
        return false;
      }
    },
    required: false,
    autoFixable: hasBrew(),
    installCmd: () => isMac() ? 'brew install bitwarden-cli' : 'npm install -g @bitwarden/cli'
  },
  onepassword: {
    name: '1Password CLI',
    check: () => {
      try {
        execSync('which op', { stdio: 'ignore' });
        return true;
      } catch {
        return false;
      }
    },
    required: false,
    autoFixable: hasBrew(),
    installCmd: () => isMac() ? 'brew install 1password-cli' : null
  }
};

async function checkPrerequisites() {
  console.log('\n🔍 Checking prerequisites...\n');
  
  const results = [];
  const missing = [];
  const optionalMissing = [];
  
  for (const [key, check] of Object.entries(checks)) {
    const passed = check.check();
    const status = passed ? '✅' : check.required ? '❌' : '⚠️';
    const label = check.required ? '(required)' : '(optional)';
    
    console.log(`   ${status} ${check.name} ${label}`);
    
    if (!passed) {
      if (check.autoFixable) {
        console.log(`      → Can auto-install`);
        missing.push({ key, ...check });
      } else if (check.required) {
        console.log(`      → ${check.fixHint}`);
        missing.push({ key, ...check });
      } else {
        optionalMissing.push({ key, ...check });
      }
    }
    
    results.push({ key, passed, required: check.required });
  }
  
  return { results, missing, optionalMissing };
}

async function installMissing(missing) {
  if (missing.length === 0) return true;
  
  const autoFixable = missing.filter(m => m.autoFixable);
  const manualFix = missing.filter(m => !m.autoFixable && m.required);
  
  // Fail fast on manual-fix required items
  if (manualFix.length > 0) {
    console.log('\n❌ Missing required prerequisites that need manual installation:\n');
    for (const item of manualFix) {
      console.log(`   ❌ ${item.name}: ${item.fixHint}`);
    }
    console.log('\nPlease install these and run setup again.');
    return false;
  }
  
  // Offer to auto-install
  if (autoFixable.length > 0) {
    console.log('\n📦 The following can be auto-installed:\n');
    for (const item of autoFixable) {
      console.log(`   • ${item.name}`);
    }
    
    const shouldInstall = await ask('\n🚀 Install these now? [Y/n]: ');
    
    if (shouldInstall.toLowerCase() === 'n') {
      console.log('\n⚠️ Skipping auto-install. Setup may not work correctly.');
      return false;
    }
    
    console.log('\n📦 Installing dependencies...\n');
    
    for (const item of autoFixable) {
      const cmd = item.installCmd();
      if (!cmd) continue;
      
      console.log(`   Installing ${item.name}...`);
      try {
        execSync(cmd, { stdio: 'inherit' });
        console.log(`   ✅ ${item.name} installed\n`);
      } catch (err) {
        console.log(`   ⚠️ Failed to install ${item.name}, continuing...\n`);
      }
    }
  }
  
  return true;
}

async function buildAndLink() {
  console.log('\n🔨 Building browser-secure...\n');
  
  const steps = [
    { name: 'Installing npm dependencies', cmd: 'npm install' },
    { name: 'Building TypeScript', cmd: 'npm run build' },
    { name: 'Linking CLI globally', cmd: 'npm link' }
  ];
  
  for (const step of steps) {
    console.log(`   ${step.name}...`);
    try {
      execSync(step.cmd, { stdio: 'inherit' });
      console.log(`   ✅ ${step.name}\n`);
    } catch (err) {
      console.error(`   ❌ ${step.name} failed`);
      throw err;
    }
  }
}

async function setupConfig() {
  const configDir = path.join(os.homedir(), '.browser-secure');
  const isReinstall = fs.existsSync(configDir);
  
  // Backup if reinstalling
  if (isReinstall) {
    const backupDir = `${configDir}.backup.${Date.now()}`;
    fs.cpSync(configDir, backupDir, { recursive: true });
    console.log(`📁 Backed up existing config to: ${backupDir}`);
    fs.rmSync(configDir, { recursive: true, force: true });
  }
  
  // Create fresh config directory
  fs.mkdirSync(configDir, { recursive: true });
  fs.mkdirSync(path.join(configDir, 'audit'), { recursive: true });
  
  // Copy default config
  const defaultConfig = path.join(process.cwd(), 'config', 'default.yaml');
  const userConfig = path.join(configDir, 'config.yaml');
  
  if (fs.existsSync(defaultConfig)) {
    fs.copyFileSync(defaultConfig, userConfig);
  } else {
    // Create minimal default config
    const defaultYaml = `vault:
  provider: bitwarden  # Options: bitwarden, 1password, keychain, env
  
  # Site-specific credential mappings
  sites: {}
    # Example:
    # nytimes:
    #   vault: "My Vault"
    #   item: "NYT Account"
    #   usernameField: "email"
    #   passwordField: "password"

security:
  sessionTimeoutMinutes: 30
  requireApprovalFor:
    - fill_password
    - submit_login
  blockLocalhost: true
  auditScreenshots: true
`;
    fs.writeFileSync(userConfig, defaultYaml);
  }
  
  console.log('📝 Created config at ~/.browser-secure/config.yaml');
}

async function runOnboarding() {
  console.log('╔════════════════════════════════════════════════════════════╗');
  console.log('║          🔒 Browser-Secure Installation                    ║');
  console.log('║     Secure browser automation with vault integration       ║');
  console.log('╚════════════════════════════════════════════════════════════╝');
  
  const configDir = path.join(os.homedir(), '.browser-secure');
  const isReinstall = fs.existsSync(configDir);
  
  if (isReinstall) {
    console.log('\n⚠️  Browser-Secure is already installed.');
    const reinstall = await ask('Reinstall/reset? [y/N]: ');
    if (reinstall.toLowerCase() !== 'y') {
      console.log('\n✅ Keeping existing installation.');
      rl.close();
      return;
    }
  }
  
  // Phase 1: Check prerequisites
  const { results, missing, optionalMissing } = await checkPrerequisites();
  
  // Phase 2: Install missing deps
  const canProceed = await installMissing(missing);
  if (!canProceed) {
    rl.close();
    process.exit(1);
  }
  
  // Phase 3: Show summary and get final permission
  console.log('\n────────────────────────────────────────────────────────────');
  console.log('\n📋 Installation Summary:\n');
  console.log('   • browser-secure CLI (globally available)');
  console.log('   • Config directory: ~/.browser-secure/');
  console.log('   • Audit logs for session tracking');
  console.log('   • 30-minute session timeouts');
  console.log('   • Vault-backed credentials (Bitwarden default)');
  
  if (optionalMissing.length > 0) {
    console.log('\n⚠️  Optional (install later if needed):');
    for (const item of optionalMissing) {
      console.log(`      • ${item.name}`);
    }
  }
  
  const confirm = await ask('\n🚀 Proceed? [Y/n]: ');
  if (confirm.toLowerCase() === 'n') {
    console.log('\n❌ Installation cancelled.');
    rl.close();
    process.exit(0);
  }
  
  // Phase 4: Build and install
  try {
    await buildAndLink();
    await setupConfig();
    
    // Update setup.json
    const setupJsonPath = path.join(process.cwd(), 'setup.json');
    if (fs.existsSync(setupJsonPath)) {
      const setupJson = JSON.parse(fs.readFileSync(setupJsonPath, 'utf8'));
      setupJson.setupComplete = true;
      setupJson.onboardingRequired = false;
      setupJson.installedAt = new Date().toISOString();
      fs.writeFileSync(setupJsonPath, JSON.stringify(setupJson, null, 2));
    }
    
    // Success message
    console.log('\n╔════════════════════════════════════════════════════════════╗');
    console.log('║              ✅ Installation Complete!                     ║');
    console.log('╚════════════════════════════════════════════════════════════╝');
    console.log('\nQuick start:\n');
    console.log('   browser-secure --version');
    console.log('   browser-secure navigate https://example.com');
    console.log('   browser-secure navigate https://github.com --profile select');
    console.log('\nConfigure vault:\n');
    console.log('   bw login                    # Bitwarden');
    console.log('   export BW_SESSION=$(bw unlock --raw)');
    console.log('   browser-secure config --edit');
    console.log('');
    
  } catch (error) {
    console.error('\n❌ Installation failed:', error.message);
    rl.close();
    process.exit(1);
  }
  
  rl.close();
}

runOnboarding();
