#!/usr/bin/env node

/**
 * Post-install script for ClawTrial
 * Automatically configures the skill for the detected bot
 * 
 * Handles both:
 * - NPM install: Links from npm global to bot's skills directory
 * - ClawHub install: Links from workspace/skills to skills directory
 */

const fs = require('fs');
const path = require('path');

console.log('🏛️  ClawTrial Post-Install');

// Get package paths
const packagePath = path.join(__dirname, '..');
const cliPath = path.join(packagePath, 'scripts', 'clawtrial.js');

// Detect which bot is installed
const homeDir = process.env.HOME || process.env.USERPROFILE || '';

const bots = [
  { name: 'openclaw', dir: '.openclaw', config: 'openclaw.json' },
  { name: 'moltbot', dir: '.moltbot', config: 'moltbot.json' },
  { name: 'clawdbot', dir: '.clawdbot', config: 'clawdbot.json' }
];

let detectedBot = null;

// Check which bot config exists
for (const bot of bots) {
  const configPath = path.join(homeDir, bot.dir, bot.config);
  if (fs.existsSync(configPath)) {
    detectedBot = bot;
    break;
  }
}

// Try to create /usr/bin symlink (requires sudo, may fail)
const usrBinPath = '/usr/bin/clawtrial';
if (!fs.existsSync(usrBinPath)) {
  try {
    fs.symlinkSync(cliPath, usrBinPath);
    fs.chmodSync(usrBinPath, 0o755);
    console.log('✓ Created global CLI symlink');
  } catch (err) {
    // Silent fail - will show instructions at end
  }
}

// Auto-link skill if bot detected
if (detectedBot) {
  console.log(`✓ Detected: ${detectedBot.name}`);
  
  const botDir = path.join(homeDir, detectedBot.dir);
  const skillsDir = path.join(botDir, 'skills');
  const skillLinkPath = path.join(skillsDir, 'clawtrial');
  
  // Check if we're in ClawHub workspace or npm global
  const isClawHubInstall = packagePath.includes('workspace/skills') || 
                           packagePath.includes('.openclaw/workspace');
  const isNpmInstall = packagePath.includes('node_modules');
  
  try {
    // Create skills directory if needed
    if (!fs.existsSync(skillsDir)) {
      fs.mkdirSync(skillsDir, { recursive: true });
      console.log(`✓ Created skills directory: ${skillsDir}`);
    }
    
    // Remove old link if exists
    if (fs.existsSync(skillLinkPath)) {
      try { fs.unlinkSync(skillLinkPath); } catch (e) {}
    }
    
    // Create symlink
    fs.symlinkSync(packagePath, skillLinkPath, 'dir');
    console.log(`✓ Linked skill: ${skillLinkPath}`);
    
    if (isClawHubInstall) {
      console.log('  (Installed via ClawHub)');
    } else if (isNpmInstall) {
      console.log('  (Installed via NPM)');
    }
    
    // Enable in bot config if OpenClaw
    if (detectedBot.name === 'openclaw') {
      try {
        const botConfigPath = path.join(botDir, detectedBot.config);
        if (fs.existsSync(botConfigPath)) {
          const botConfig = JSON.parse(fs.readFileSync(botConfigPath, 'utf8'));
          
          if (!botConfig.skills) botConfig.skills = {};
          if (!botConfig.skills.entries) botConfig.skills.entries = {};
          botConfig.skills.entries.clawtrial = { enabled: true };
          
          fs.writeFileSync(botConfigPath, JSON.stringify(botConfig, null, 2));
          console.log('✓ Enabled in OpenClaw config');
        }
      } catch (configErr) {
        console.log(`⚠️  Could not update config: ${configErr.message}`);
      }
    }
    
    console.log('');
    console.log('🎉 ClawTrial is ready!');
    console.log('');
    console.log('Next step:');
    console.log(`  Restart ${detectedBot.name}: killall ${detectedBot.name} && ${detectedBot.name}`);
    
  } catch (err) {
    console.log(`⚠️  Could not link skill: ${err.message}`);
  }
} else {
  console.log('ℹ️  No bot detected');
  console.log('');
  console.log('📋 Next Steps:');
  console.log('  1. Run setup:');
  console.log('     clawtrial setup');
  console.log('');
  console.log('  2. Check status:');
  console.log('     clawtrial status');
}

console.log('');
