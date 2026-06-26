#!/usr/bin/env node

/**
 * ClawCap Setup Script
 *
 * What this script does:
 *   1. Reads your existing ~/.openclaw/openclaw.json config
 *   2. Creates a backup at ~/.openclaw/openclaw.json.backup (if one doesn't exist)
 *   3. Changes each provider's baseUrl to your ClawCap proxy URL
 *   4. Saves the updated config
 *
 * What this script does NOT do:
 *   - It does NOT read, store, or transmit your API keys
 *   - It does NOT modify any files outside ~/.openclaw/
 *   - It does NOT install any packages or download anything
 *   - It does NOT run any network requests
 *
 * To undo: run the uninstall script, or copy your .backup file back manually.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { exec } = require('child_process');
const readline = require('readline');

const CLAWCAP_BASE = 'https://clawcap.co/proxy';

// Only allow writing within ~/.openclaw/
const ALLOWED_DIR = path.join(os.homedir(), '.openclaw');

function getConfigPath() {
  return path.join(ALLOWED_DIR, 'openclaw.json');
}

function validatePath(filePath) {
  const resolved = path.resolve(filePath);
  if (!resolved.startsWith(ALLOWED_DIR)) {
    console.error('Error: Refusing to write outside ~/.openclaw/ directory.');
    process.exit(1);
  }
  return resolved;
}

function readConfig(configPath) {
  const safePath = validatePath(configPath);
  if (!fs.existsSync(safePath)) {
    console.error(`Error: OpenClaw config not found at ${safePath}`);
    console.error('Make sure OpenClaw is installed and has been run at least once.');
    process.exit(1);
  }
  try {
    const raw = fs.readFileSync(safePath, 'utf8');
    return JSON.parse(raw);
  } catch (err) {
    console.error(`Error: Could not parse ${safePath} — ${err.message}`);
    process.exit(1);
  }
}

function backupConfig(configPath) {
  const safePath = validatePath(configPath);
  const backupPath = validatePath(configPath + '.backup');
  if (!fs.existsSync(backupPath)) {
    fs.copyFileSync(safePath, backupPath);
    console.log(`Backed up config to ${backupPath}`);
  } else {
    console.log('Backup already exists, skipping backup.');
  }
}

function getToken() {
  const token = (process.env.CLAWCAP_TOKEN || '').trim();
  if (token && /^cc_live_[a-f0-9]{32}$/.test(token)) {
    return token;
  }
  return null;
}

function openBrowser(url) {
  const platform = process.platform;
  const cmd = platform === 'win32' ? `start "" "${url}"`
    : platform === 'darwin' ? `open "${url}"`
    : `xdg-open "${url}"`;
  exec(cmd, () => {}); // fire-and-forget, ignore errors
}

function askForToken() {
  return new Promise((resolve) => {
    const signupUrl = 'https://clawcap.co';
    console.log('');
    console.log('You need a ClawCap token to continue.');
    console.log('Opening clawcap.co in your browser to sign up and get your token...');
    console.log('');
    openBrowser(signupUrl);

    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    rl.question('Paste your ClawCap token here (cc_live_...): ', (answer) => {
      rl.close();
      const token = answer.trim();
      if (!/^cc_live_[a-f0-9]{32}$/.test(token)) {
        console.error('Error: Invalid token format. Must be cc_live_ followed by 32 hex characters.');
        console.error('Sign up at https://clawcap.co to get your token.');
        process.exit(1);
      }
      resolve(token);
    });
  });
}

function patchProviders(config, proxyUrl) {
  let patched = 0;

  if (config.models && config.models.providers && typeof config.models.providers === 'object') {
    const providers = config.models.providers;

    if (Array.isArray(providers)) {
      for (const provider of providers) {
        if (provider.baseUrl && !provider.baseUrl.includes('clawcap.co')) {
          provider._originalBaseUrl = provider.baseUrl;
          provider.baseUrl = proxyUrl;
          patched++;
          console.log(`  Patched provider: ${provider.name || 'unnamed'}`);
        }
      }
    } else {
      for (const [name, provider] of Object.entries(providers)) {
        if (provider && typeof provider === 'object' && provider.baseUrl && !provider.baseUrl.includes('clawcap.co')) {
          provider._originalBaseUrl = provider.baseUrl;
          provider.baseUrl = proxyUrl;
          patched++;
          console.log(`  Patched provider: ${name}`);
        }
      }
    }
  }

  if (config.providers && Array.isArray(config.providers)) {
    for (const provider of config.providers) {
      if (provider.baseUrl && !provider.baseUrl.includes('clawcap.co')) {
        provider._originalBaseUrl = provider.baseUrl;
        provider.baseUrl = proxyUrl;
        patched++;
        console.log(`  Patched provider: ${provider.name || 'unnamed'}`);
      }
    }
  }

  return patched;
}

async function main() {
  console.log('');
  console.log('ClawCap Setup');
  console.log('=============');
  console.log('');

  let token = getToken();
  if (!token) {
    console.log('No CLAWCAP_TOKEN environment variable found.');
    token = await askForToken();
  } else {
    console.log('Using token from CLAWCAP_TOKEN environment variable.');
  }

  const proxyUrl = `${CLAWCAP_BASE}/${token}`;

  const configPath = getConfigPath();
  console.log(`Reading config from ${configPath}`);
  const config = readConfig(configPath);

  backupConfig(configPath);

  console.log('');
  console.log('Patching providers...');
  const patched = patchProviders(config, proxyUrl);

  if (patched === 0) {
    console.log('');
    console.log('No providers found to patch. Either:');
    console.log('  - Your config has no providers with baseUrl set');
    console.log('  - Providers are already routed through ClawCap');
    console.log('');
    console.log('You can manually set baseUrl to:');
    console.log(`  ${proxyUrl}`);
    console.log('');
    process.exit(0);
  }

  // Write updated config (only to validated path within ~/.openclaw/)
  const safePath = validatePath(configPath);
  fs.writeFileSync(safePath, JSON.stringify(config, null, 2) + '\n', 'utf8');

  console.log('');
  console.log(`Done! ${patched} provider(s) now route through ClawCap.`);
  console.log('');
  console.log('Your proxy URL:');
  console.log(`  ${proxyUrl}`);
  console.log('');
  console.log('Check your spend anytime:');
  console.log(`  curl ${proxyUrl}/status`);
  console.log('');
  console.log('To undo, run: node skills/clawcap/scripts/uninstall.js');
  console.log('');
}

main().catch((err) => {
  console.error('Setup failed:', err.message);
  process.exit(1);
});
