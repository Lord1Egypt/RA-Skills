#!/usr/bin/env node
/**
 * ClawLink Install Script
 * 
 * IMPORTANT FOR AI AGENTS:
 * This script installs ClawLink but the skill is NOT FUNCTIONAL until you run setup.
 * You MUST run: node cli.js setup "Your Name" after this script completes.
 * Without setup, you have no identity and cannot send/receive messages.
 */

import { existsSync, readFileSync, writeFileSync, appendFileSync, mkdirSync } from 'fs';
import { homedir } from 'os';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_DIR = join(__dirname, '..');

const OPENCLAW_DIR = join(homedir(), '.openclaw');
const CLAWLINK_DATA_DIR = join(OPENCLAW_DIR, 'clawlink');
const IDENTITY_FILE = join(CLAWLINK_DATA_DIR, 'identity.json');

// Try both possible workspace locations
const CLAWD_DIR = join(homedir(), 'clawd');
const OPENCLAW_WORKSPACE = join(OPENCLAW_DIR, 'workspace');
const HEARTBEAT_CANDIDATES = [
  join(CLAWD_DIR, 'HEARTBEAT.md'),
  join(OPENCLAW_WORKSPACE, 'HEARTBEAT.md')
];

function getClawlinkSection(skillDir) {
  return `
## ClawLink
- Poll for encrypted messages: \`node ${skillDir}/heartbeat.js\`
- If output is non-empty, deliver it to the user
- Handles: messages, friend requests, acceptance notifications
`;
}

function findHeartbeatFile() {
  for (const path of HEARTBEAT_CANDIDATES) {
    if (existsSync(path)) return path;
  }
  return null;
}

async function main() {
  console.log('');
  console.log('╔════════════════════════════════════════════════════════════╗');
  console.log('║                    🔗 ClawLink Install                     ║');
  console.log('╚════════════════════════════════════════════════════════════╝');
  console.log('');

  // Step 1: Install npm dependencies
  console.log('📦 Step 1: Installing dependencies...');
  try {
    execSync('npm install --prefer-offline --no-audit --no-fund', { 
      cwd: SKILL_DIR, 
      stdio: 'inherit',
      timeout: 60000  // 60 second timeout
    });
    console.log('✓ Dependencies installed');
  } catch (e) {
    if (e.killed) {
      console.error('✗ npm install timed out after 60s');
    } else {
      console.error('✗ Failed to install dependencies:', e.message);
    }
    process.exit(1);
  }
  console.log('');

  // Step 2: Add to HEARTBEAT.md
  console.log('📋 Step 2: Configuring heartbeat...');
  const heartbeatFile = findHeartbeatFile();
  
  if (!heartbeatFile) {
    console.log('⚠ No HEARTBEAT.md found. Skipping heartbeat config.');
    console.log('  You can manually add ClawLink polling later.');
  } else {
    const content = readFileSync(heartbeatFile, 'utf8');
    if (content.includes('ClawLink') || content.includes('clawlink')) {
      console.log('✓ ClawLink already in HEARTBEAT.md');
    } else {
      appendFileSync(heartbeatFile, getClawlinkSection(SKILL_DIR));
      console.log('✓ Added ClawLink to', heartbeatFile);
    }
  }
  console.log('');

  // Step 3: Check if identity exists
  console.log('🔑 Step 3: Checking identity...');
  const hasIdentity = existsSync(IDENTITY_FILE);
  
  if (hasIdentity) {
    const identity = JSON.parse(readFileSync(IDENTITY_FILE, 'utf8'));
    console.log('✓ Identity exists');
    console.log('  Name: Check config.json for display name');
    console.log('  Public Key:', identity.publicKey?.slice(0, 20) + '...');
    console.log('');
    console.log('╔════════════════════════════════════════════════════════════╗');
    console.log('║              ✅ ClawLink is ready to use!                  ║');
    console.log('╚════════════════════════════════════════════════════════════╝');
    console.log('');
    console.log('Get your friend link: node cli.js link');
    console.log('Check messages:       node handler.js check');
    console.log('');
  } else {
    console.log('');
    console.log('╔════════════════════════════════════════════════════════════╗');
    console.log('║  ⚠️  CRITICAL: ClawLink setup required!                     ║');
    console.log('║                                                            ║');
    console.log('║  ClawLink is installed but NOT FUNCTIONAL yet.             ║');
    console.log('║  You have no identity - you cannot send or receive.        ║');
    console.log('║                                                            ║');
    console.log('║  👉 RUN THIS NOW:                                          ║');
    console.log('║                                                            ║');
    console.log('║     node cli.js setup "Your Bot Name"                      ║');
    console.log('║                                                            ║');
    console.log('║  Replace "Your Bot Name" with your actual name.            ║');
    console.log('║  This creates your keypair and identity.                   ║');
    console.log('╚════════════════════════════════════════════════════════════╝');
    console.log('');
    console.log('Example:');
    console.log('  node cli.js setup "John Wick"');
    console.log('');
    console.log('After setup, get your friend link with:');
    console.log('  node cli.js link');
    console.log('');
    
    // Return non-zero to signal incomplete setup
    process.exit(2);
  }
}

main().catch(e => {
  console.error('Install failed:', e);
  process.exit(1);
});
