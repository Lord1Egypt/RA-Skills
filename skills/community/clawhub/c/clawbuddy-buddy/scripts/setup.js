#!/usr/bin/env node
/**
 * ClawBuddy Buddy — Pre-flight Setup Validator
 *
 * Checks that everything is configured correctly before running the buddy.
 * Optionally auto-creates .env from .env.example with --fix.
 *
 * Usage:
 *   node scripts/setup.js           # Validate configuration
 *   node scripts/setup.js --fix     # Auto-create .env from .env.example
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';
import { loadEnv } from './lib/env.js';
import { isLocalhostUrl } from './lib/url-utils.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SKILL_DIR = path.resolve(__dirname, '..');

const args = process.argv.slice(2);
const fixMode = args.includes('--fix');

let errors = 0;
let warnings = 0;
let detectedHermesPort = null;

function ok(msg) { console.log(`  \x1b[32m✓\x1b[0m ${msg}`); }
function warn(msg) { console.log(`  \x1b[33m⚠\x1b[0m ${msg}`); warnings++; }
function fail(msg) { console.log(`  \x1b[31m✗\x1b[0m ${msg}`); errors++; }
function info(msg) { console.log(`    ${msg}`); }

// ── .env loading is handled by lib/env.js (imported above) ──

// ── 1. Node.js version ────────────────────────────────────────────

function checkNodeVersion() {
  console.log('\n\x1b[1mNode.js Version\x1b[0m');
  const version = process.version;
  const major = parseInt(version.replace('v', '').split('.')[0]);
  if (major >= 18) {
    ok(`Node.js ${version} (>= v18 required)`);
  } else {
    fail(`Node.js ${version} — v18 or later required, got v${major}`);
    info('Upgrade: https://nodejs.org/');
  }
}

// ── 2. Required env vars ──────────────────────────────────────────

function checkRequiredVars() {
  console.log('\n\x1b[1mRequired Environment Variables\x1b[0m');

  const required = [
    { name: 'CLAWBUDDY_TOKEN', hint: 'Run: node scripts/register.js --name "My Agent"' },
    { name: 'GATEWAY_URL', hint: 'Hermes: http://127.0.0.1:8642 | OpenClaw: http://127.0.0.1:18789' },
    { name: 'GATEWAY_TOKEN', hint: 'For Hermes: copy API_SERVER_KEY from ~/.hermes/.env' },
  ];

  for (const { name, hint } of required) {
    // Check primary and fallback vars
    const fallbacks = {
      GATEWAY_URL: 'OPENCLAW_GATEWAY_URL',
      GATEWAY_TOKEN: 'OPENCLAW_GATEWAY_TOKEN',
    };
    const value = process.env[name] || (fallbacks[name] ? process.env[fallbacks[name]] : '');
    if (value) {
      ok(`${name} is set`);
    } else {
      fail(`${name} is not set`);
      info(hint);
    }
  }

  // Optional vars
  console.log('\n\x1b[1mOptional Environment Variables\x1b[0m');
  const optional = ['CLAWBUDDY_URL', 'GATEWAY_MODEL', 'HUMAN_CONSULT_TIMEOUT', 'PEARLS_DIR', 'WORKSPACE'];
  for (const name of optional) {
    if (process.env[name]) {
      ok(`${name} = ${name.includes('TOKEN') ? '***' : process.env[name]}`);
    } else {
      info(`${name} not set (using default)`);
    }
  }
}

// ── 3. Hermes config detection ────────────────────────────────────

function checkHermesConfig() {
  console.log('\n\x1b[1mHermes Configuration\x1b[0m');
  const hermesProfile = process.env.HERMES_PROFILE;
  const hermesHome = process.env.HERMES_HOME
    || (hermesProfile ? path.join(os.homedir(), '.hermes', 'profiles', hermesProfile) : path.join(os.homedir(), '.hermes'));
  const hermesConfigPath = path.join(hermesHome, 'config.yaml');

  if (!fs.existsSync(hermesConfigPath)) {
    info(`No Hermes config found at ${hermesConfigPath}`);
    info('If using a named Hermes profile, set HERMES_PROFILE before running this script.');
    return;
  }

  ok(`Found Hermes config: ${hermesConfigPath}`);

  try {
    const config = fs.readFileSync(hermesConfigPath, 'utf-8');
    const hermesEnvPath = path.join(hermesHome, '.env');
    const envContent = fs.existsSync(hermesEnvPath) ? fs.readFileSync(hermesEnvPath, 'utf-8') : '';

    // Check api_server section
    if (config.includes('api_server')) {
      ok('api_server section found');

      // Extract the api_server block (indented lines after "api_server:")
      const apiServerMatch = config.match(/api_server:\s*\n((?:\s+.*\n?)*)/);
      const apiServerBlock = apiServerMatch ? apiServerMatch[1] : '';

      // Try to extract port from the api_server block
      const portMatch = apiServerBlock.match(/port:\s*(\d+)/);
      if (portMatch) {
        detectedHermesPort = portMatch[1];
        ok(`API server port: ${portMatch[1]}`);
      } else {
        warn('Could not detect api_server port — default may be used');
      }

      // Check if enabled (only within the api_server block)
      if (/enabled:\s*false/i.test(apiServerBlock)) {
        fail('API server appears disabled (enabled: false)');
        info(`Set enabled: true in the api_server section of ${hermesConfigPath}`);
      } else {
        ok('API server appears enabled');
      }
    } else {
      if (/API_SERVER_ENABLED\s*=\s*true/i.test(envContent)) {
        ok('API_SERVER_ENABLED=true found in Hermes env');
      } else {
        warn('No api_server section in config and no API_SERVER_ENABLED=true in env');
        info('Enable the Hermes API server before starting the buddy listener');
      }
    }

    // Check for api_key
    if (envContent) {
      const envPortMatch = envContent.match(/API_SERVER_PORT\s*=\s*(\d+)/);
      if (envPortMatch) detectedHermesPort = envPortMatch[1];
      if (/API_SERVER_KEY\s*=/.test(envContent)) {
        ok(`API_SERVER_KEY found in ${hermesEnvPath}`);
      } else {
        warn(`API_SERVER_KEY not found in ${hermesEnvPath}`);
        info('Set API_SERVER_KEY in the Hermes env file for gateway auth');
      }
    } else {
      info(`No Hermes env file found at ${hermesEnvPath}`);
    }
  } catch (err) {
    warn(`Could not parse Hermes config: ${err.message}`);
  }
}

// ── 4. Gateway connectivity ───────────────────────────────────────

// isLocalhostUrl is imported from lib/url-utils.js

async function checkGatewayConnectivity() {
  console.log('\n\x1b[1mGateway Connectivity\x1b[0m');

  const gatewayUrl = process.env.GATEWAY_URL || process.env.OPENCLAW_GATEWAY_URL;
  if (!gatewayUrl) {
    fail('No GATEWAY_URL set — skipping connectivity test');
    if (detectedHermesPort) info(`For Hermes, set GATEWAY_URL=http://127.0.0.1:${detectedHermesPort}`);
    return;
  }

  if (!process.env.GATEWAY_URL && process.env.OPENCLAW_GATEWAY_URL && detectedHermesPort) {
    warn('Using OPENCLAW_GATEWAY_URL fallback while Hermes config was detected');
    info(`For a Hermes buddy, set GATEWAY_URL=http://127.0.0.1:${detectedHermesPort} and GATEWAY_TOKEN=API_SERVER_KEY`);
  }

  if (detectedHermesPort) {
    try {
      const parsedGateway = new URL(gatewayUrl);
      if (parsedGateway.hostname === '127.0.0.1' || parsedGateway.hostname === 'localhost') {
        const gatewayPort = parsedGateway.port || (parsedGateway.protocol === 'https:' ? '443' : '80');
        if (gatewayPort !== String(detectedHermesPort) && !process.env.OPENCLAW_GATEWAY_URL) {
          warn(`GATEWAY_URL port (${gatewayPort}) differs from detected Hermes API port (${detectedHermesPort})`);
        }
      }
    } catch {}
  }

  const gatewayToken = process.env.GATEWAY_TOKEN || process.env.OPENCLAW_GATEWAY_TOKEN || '';

  // Security: do not send the auth token to remote hosts
  const isLocal = isLocalhostUrl(gatewayUrl);
  let safeToken = gatewayToken;
  if (!isLocal && gatewayToken) {
    warn('GATEWAY_URL appears to be a remote host — skipping auth token for security');
    safeToken = '';
  }

  const headers = safeToken ? { 'Authorization': `Bearer ${safeToken}` } : {};

  // Try /v1/models first (standard endpoint), fall back to /v1/chat/completions probe.
  // Some gateways don't implement /v1/models but the buddy only needs /v1/chat/completions.
  const modelsUrl = new URL('/v1/models', gatewayUrl).toString();
  const completionsUrl = new URL('/v1/chat/completions', gatewayUrl).toString();

  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);

    let res;
    try {
      res = await fetch(modelsUrl, { headers, signal: controller.signal });
    } finally {
      clearTimeout(timeout);
    }

    if (res.ok) {
      ok(`Gateway responded at ${modelsUrl}`);
      try {
        const data = await res.json();
        const modelCount = data.data?.length || 0;
        info(`${modelCount} model(s) available`);
      } catch {
        // Non-critical
      }
    } else if (res.status === 404 || res.status === 405) {
      // /v1/models not available — probe /v1/chat/completions instead
      const controller2 = new AbortController();
      const timeout2 = setTimeout(() => controller2.abort(), 5000);
      // Minimal OPTIONS or GET to check the endpoint exists
      let res2;
      try {
        res2 = await fetch(completionsUrl, { headers, method: 'OPTIONS', signal: controller2.signal })
          .catch(() => null);
      } finally {
        clearTimeout(timeout2);
      }
      if (res2 && (res2.ok || res2.status === 405 || res2.status === 401)) {
        ok(`Gateway reachable (using ${completionsUrl})`);
      } else {
        warn(`/v1/models not available and /v1/chat/completions probe failed`);
        info('Gateway may not be fully compatible — buddy runtime may still work');
      }
    } else {
      fail(`Gateway returned ${res.status} ${res.statusText}`);
      if (res.status === 401) {
        info('Check GATEWAY_TOKEN — authentication failed');
      }
    }
  } catch (err) {
    if (err.name === 'AbortError') {
      fail(`Gateway at ${gatewayUrl} did not respond within 5s`);
      info('Is your gateway running?');
    } else {
      fail(`Could not reach gateway at ${gatewayUrl}: ${err.message}`);
      info('Make sure the gateway is running and the URL is correct');
    }
  }
}

// ── 5. Pearls directory ───────────────────────────────────────────

function checkPearls() {
  console.log('\n\x1b[1mPearls Directory\x1b[0m');

  const pearlsDir = process.env.PEARLS_DIR
    ? path.resolve(process.env.PEARLS_DIR)
    : path.join(SKILL_DIR, 'pearls');

  if (!fs.existsSync(pearlsDir)) {
    warn(`Pearls directory not found: ${pearlsDir}`);
    info('Run: node scripts/generate-pearls.js');
    info('Or:  node scripts/pearls.js generate --all');
    return;
  }

  const files = fs.readdirSync(pearlsDir).filter(f => f.endsWith('.md'));
  if (files.length > 0) {
    ok(`Pearls directory has ${files.length} pearl file(s)`);
  } else {
    warn('Pearls directory exists but is empty');
    info('Generate pearls: node scripts/generate-pearls.js');
  }
}

// ── --fix: Create .env from .env.example ──────────────────────────

function fixEnv() {
  console.log('\n\x1b[1m--fix: Creating .env\x1b[0m');

  const envPath = path.join(SKILL_DIR, '.env');
  const examplePath = path.join(SKILL_DIR, '.env.example');

  if (fs.existsSync(envPath)) {
    warn('.env already exists — not overwriting');
    return;
  }

  if (!fs.existsSync(examplePath)) {
    fail('.env.example not found — cannot create .env');
    return;
  }

  fs.copyFileSync(examplePath, envPath);
  ok(`Created .env from .env.example at ${envPath}`);
  info('Edit .env and fill in your values');
}

// ── Main ──────────────────────────────────────────────────────────

async function main() {
  console.log('\x1b[1m╔══════════════════════════════════════════════════╗\x1b[0m');
  console.log('\x1b[1m║  ClawBuddy Buddy — Setup Validator               ║\x1b[0m');
  console.log('\x1b[1m╚══════════════════════════════════════════════════╝\x1b[0m');

  if (fixMode) {
    fixEnv();
  }

  loadEnv();
  checkNodeVersion();
  checkRequiredVars();
  checkHermesConfig();
  await checkGatewayConnectivity();
  checkPearls();

  console.log('\n\x1b[1m──────────────────────────────────────────────────\x1b[0m');
  if (errors === 0 && warnings === 0) {
    console.log('\x1b[32mAll checks passed! Ready to run:\x1b[0m');
    console.log('  node scripts/listen.js');
  } else if (errors === 0) {
    console.log(`\x1b[33m${warnings} warning(s), 0 errors.\x1b[0m You can start but some features may not work.`);
    console.log('  node scripts/listen.js');
  } else {
    console.log(`\x1b[31m${errors} error(s), ${warnings} warning(s).\x1b[0m Fix the errors above before running.`);
    process.exitCode = 1;
  }
  console.log('');
}

main().catch(err => { console.error('Setup check failed:', err.message); process.exit(1); });
