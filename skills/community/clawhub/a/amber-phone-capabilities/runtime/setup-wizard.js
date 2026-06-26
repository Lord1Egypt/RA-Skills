#!/usr/bin/env node
// Amber Voice Assistant — Interactive Setup Wizard
// Usage: npm run setup  (or:  node setup-wizard.js)

import { createInterface } from 'node:readline/promises';
import { stdin, stdout, env } from 'node:process';
import { existsSync, copyFileSync, writeFileSync, readFileSync } from 'node:fs';
import { access } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

// ── Colours ──────────────────────────────────────────────────────────
const c = {
  reset: '\x1b[0m',
  bold:  '\x1b[1m',
  dim:   '\x1b[2m',
  green: '\x1b[32m',
  red:   '\x1b[31m',
  yellow:'\x1b[33m',
  cyan:  '\x1b[36m',
  magenta:'\x1b[35m',
};
const ok   = (m) => console.log(`${c.green}  ✓ ${m}${c.reset}`);
const fail = (m) => console.log(`${c.red}  ✗ ${m}${c.reset}`);
const warn = (m) => console.log(`${c.yellow}  ⚠ ${m}${c.reset}`);
const info = (m) => console.log(`${c.cyan}  ℹ ${m}${c.reset}`);
const head = (m) => console.log(`\n${c.bold}${c.magenta}─── ${m} ───${c.reset}\n`);

// ── Helpers ──────────────────────────────────────────────────────────
const __dirname = dirname(fileURLToPath(import.meta.url));
const envPath   = resolve(__dirname, '.env');

let rl;
const ask = async (prompt, defaultVal) => {
  const suffix = defaultVal !== undefined ? ` ${c.dim}(${defaultVal})${c.reset}` : '';
  const answer = (await rl.question(`  ${prompt}${suffix}: `)).trim();
  return answer || (defaultVal ?? '');
};

const yesNo = async (prompt, defaultYes = true) => {
  const hint = defaultYes ? 'Y/n' : 'y/N';
  const answer = (await rl.question(`  ${prompt} ${c.dim}[${hint}]${c.reset} `)).trim().toLowerCase();
  if (!answer) return defaultYes;
  return answer.startsWith('y');
};

const spinner = (label) => {
  const frames = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏'];
  let i = 0;
  const id = setInterval(() => {
    stdout.write(`\r  ${c.cyan}${frames[i++ % frames.length]} ${label}${c.reset}`);
  }, 80);
  return { stop: (msg) => { clearInterval(id); stdout.write(`\r${' '.repeat(label.length + 10)}\r`); if (msg) console.log(msg); } };
};

// ── Validators ───────────────────────────────────────────────────────
const isE164 = (v) => /^\+[1-9]\d{6,14}$/.test(v);
const VOICES = ['alloy','echo','fable','onyx','nova','shimmer'];

async function validateTwilio(sid, token) {
  const s = spinner('Validating Twilio credentials…');
  try {
    const res = await fetch(`https://api.twilio.com/2010-04-01/Accounts/${sid}.json`, {
      headers: { Authorization: 'Basic ' + Buffer.from(`${sid}:${token}`).toString('base64') },
    });
    s.stop();
    if (res.ok) { ok('Twilio credentials verified with Twilio over HTTPS'); return true; }
    fail(`Twilio auth failed (HTTP ${res.status})`);
    return false;
  } catch (e) {
    s.stop();
    fail(`Twilio network error: ${e.message}`);
    return false;
  }
}

async function validateOpenAI(key) {
  const s = spinner('Validating OpenAI API key…');
  try {
    const res = await fetch('https://api.openai.com/v1/models', {
      headers: { Authorization: `Bearer ${key}` },
    });
    s.stop();
    if (res.ok) { ok('OpenAI API key verified with OpenAI over HTTPS'); return true; }
    fail(`OpenAI auth failed (HTTP ${res.status})`);
    return false;
  } catch (e) {
    s.stop();
    fail(`OpenAI network error: ${e.message}`);
    return false;
  }
}

async function detectNgrok() {
  const pathDirs = (env.PATH || '').split(':').filter(Boolean);
  for (const dir of pathDirs) {
    try {
      await access(resolve(dir, 'ngrok'));
      return true;
    } catch {}
  }
  return false;
}

async function getActiveNgrokTunnel() {
  try {
    const res = await fetch('http://127.0.0.1:4040/api/tunnels', { signal: AbortSignal.timeout(2000) });
    if (!res.ok) return null;
    const data = await res.json();
    const https = data.tunnels?.find(t => t.proto === 'https');
    return https?.public_url ?? data.tunnels?.[0]?.public_url ?? null;
  } catch { return null; }
}

async function startNgrok(port) {
  info(`Open a second terminal and run: ngrok http ${String(port)}`);
  info('Then paste the HTTPS forwarding URL below.');
  return null;
}

// ── Main ─────────────────────────────────────────────────────────────
async function main() {
  rl = createInterface({ input: stdin, output: stdout });

  console.log(`
${c.bold}${c.cyan}╔══════════════════════════════════════════════╗
║   ☎️  Amber Voice Assistant — Setup Wizard    ║
╚══════════════════════════════════════════════╝${c.reset}
`);
  info('This wizard will walk you through configuration and generate a .env file.');
  warn('Amber is a sensitive communications system: calls may be handled by AI providers and logged locally.');
  warn('Secrets and operator contact details entered here are written to runtime/.env; keep that file private and out of published packages.');
  info('Credential validation calls only the relevant provider APIs over HTTPS (Twilio/OpenAI) and does not send secrets to Amber or ClawHub.');
  info('Press Enter to accept defaults shown in parentheses.\n');

  const cfg = {};

  // ── Twilio ─────────────────────────────────────────────────────────
  head('Twilio Configuration');
  info('Get credentials at https://console.twilio.com');

  while (true) {
    cfg.TWILIO_ACCOUNT_SID = await ask('Account SID (starts with AC)');
    if (!cfg.TWILIO_ACCOUNT_SID.startsWith('AC') || cfg.TWILIO_ACCOUNT_SID.length < 34) {
      fail('Account SID must start with "AC" and be 34 characters'); continue;
    }
    cfg.TWILIO_AUTH_TOKEN = await ask('Auth Token');
    if (!cfg.TWILIO_AUTH_TOKEN) { fail('Auth Token is required'); continue; }
    if (await validateTwilio(cfg.TWILIO_ACCOUNT_SID, cfg.TWILIO_AUTH_TOKEN)) break;
    if (!(await yesNo('Try again?'))) break;
  }

  while (true) {
    cfg.TWILIO_CALLER_ID = await ask('Twilio phone number (E.164, e.g. +15555551234)');
    if (isE164(cfg.TWILIO_CALLER_ID)) { ok('Phone number format valid'); break; }
    fail('Must be E.164 format: +<country><number>');
  }

  // ── OpenAI ─────────────────────────────────────────────────────────
  head('OpenAI Configuration');
  info('Get your API key at https://platform.openai.com/api-keys');

  while (true) {
    cfg.OPENAI_API_KEY = await ask('API Key (starts with sk-)');
    if (!cfg.OPENAI_API_KEY.startsWith('sk-')) { fail('API key should start with "sk-"'); continue; }
    if (await validateOpenAI(cfg.OPENAI_API_KEY)) break;
    if (!(await yesNo('Try again?'))) break;
  }

  while (true) {
    cfg.OPENAI_PROJECT_ID = await ask('Project ID (starts with proj_)');
    if (!cfg.OPENAI_PROJECT_ID) {
      warn('Project ID is required');
      continue;
    }
    if (!cfg.OPENAI_PROJECT_ID.startsWith('proj_')) {
      warn('Project ID usually starts with "proj_" — using as-is');
    }
    break;
  }

  while (true) {
    cfg.OPENAI_WEBHOOK_SECRET = await ask('Webhook Secret (starts with whsec_)');
    if (!cfg.OPENAI_WEBHOOK_SECRET) {
      warn('Webhook Secret is required');
      continue;
    }
    if (!cfg.OPENAI_WEBHOOK_SECRET.startsWith('whsec_')) {
      warn('Webhook secret usually starts with "whsec_" — using as-is');
    }
    break;
  }

  while (true) {
    cfg.OPENAI_VOICE = (await ask('Voice', 'alloy')).toLowerCase();
    if (VOICES.includes(cfg.OPENAI_VOICE)) { ok(`Voice: ${cfg.OPENAI_VOICE}`); break; }
    fail(`Must be one of: ${VOICES.join(', ')}`);
  }

  // ── Server ─────────────────────────────────────────────────────────
  head('Server Configuration');

  cfg.PORT = await ask('Port', '8000');

  // ngrok detection
  const ngrokInstalled = await detectNgrok();
  let publicUrl = null;

  if (ngrokInstalled) {
    ok('ngrok binary detected locally');
    const tunnel = await getActiveNgrokTunnel();
    if (tunnel) {
      ok(`Active local ngrok tunnel detected: ${tunnel}`);
      if (await yesNo(`Use ${tunnel} as PUBLIC_BASE_URL?`)) publicUrl = tunnel;
    } else {
      info('No active ngrok tunnel found.');
      if (await yesNo(`Show ngrok command for port ${cfg.PORT}?`)) {
        await startNgrok(cfg.PORT);
      }
    }
  } else {
    info('ngrok not detected. You\'ll need a public URL for webhooks.');
  }

  if (!publicUrl) {
    cfg.PUBLIC_BASE_URL = await ask('Public base URL (e.g. https://your-domain.com)');
  } else {
    cfg.PUBLIC_BASE_URL = publicUrl;
  }

  head('Outbound Calls (optional)');
  info('Outbound calling is enabled by default for the full Amber experience. You can disable it later.');
  cfg.AMBER_ENABLE_OUTBOUND_CALLS = await yesNo('Enable outbound calling?', true) ? 'true' : 'false';

  // ── Optional: OpenClaw ─────────────────────────────────────────────
  head('OpenClaw Gateway (optional)');
  info('If you have an OpenClaw gateway, the assistant can consult it during calls.');

  if (await yesNo('Configure OpenClaw integration?', false)) {
    cfg.OPENCLAW_GATEWAY_URL = await ask('Gateway URL', 'http://127.0.0.1:18789');
    cfg.OPENCLAW_GATEWAY_TOKEN = await ask('Gateway Token', '');
  }

  // ── Optional: Personalization ──────────────────────────────────────
  head('Personalization (optional)');

  if (await yesNo('Customize assistant identity?', false)) {
    cfg.ASSISTANT_NAME = await ask('Assistant name', 'Amber');
    cfg.OPERATOR_NAME  = await ask('Operator name (person being assisted)', '');
    cfg.OPERATOR_PHONE = await ask('Operator phone (E.164)', '');
    if (cfg.OPERATOR_PHONE && !isE164(cfg.OPERATOR_PHONE)) warn('Not a valid E.164 number');
    cfg.OPERATOR_EMAIL = await ask('Operator email', '');
    cfg.ORG_NAME       = await ask('Organization name', '');
    cfg.DEFAULT_CALENDAR = await ask('Default calendar name', '');
  }

  // ── Optional: Call Screening ───────────────────────────────────────
  head('Call Screening (optional)');

  if (await yesNo('Configure GenZ-style call screening numbers?', false)) {
    cfg.GENZ_CALLER_NUMBERS = await ask('Comma-separated E.164 numbers', '');
  }

  // ── Generate .env ──────────────────────────────────────────────────
  head('Generating .env');
  warn('Writing secrets, phone numbers, and optional operator identity fields to runtime/.env. Protect this file and rotate credentials if it is exposed.');

  if (existsSync(envPath)) {
    const ts = new Date().toISOString().replace(/[:.]/g, '-');
    const backup = `${envPath}.backup.${ts}`;
    copyFileSync(envPath, backup);
    ok(`Backed up existing .env → ${backup}`);
  }

  const lines = [
    '# Amber Voice Assistant - Generated by setup wizard',
    `# ${new Date().toISOString()}`,
    '',
    '# === Telephony Provider ===',
    'VOICE_PROVIDER=twilio',
    '',
    '# === Twilio ===',
    `TWILIO_ACCOUNT_SID=${cfg.TWILIO_ACCOUNT_SID}`,
    `TWILIO_AUTH_TOKEN=${cfg.TWILIO_AUTH_TOKEN}`,
    `TWILIO_CALLER_ID=${cfg.TWILIO_CALLER_ID}`,
    '',
    '# === OpenAI ===',
    `OPENAI_API_KEY=${cfg.OPENAI_API_KEY}`,
    `OPENAI_PROJECT_ID=${cfg.OPENAI_PROJECT_ID || ''}`,
    `OPENAI_WEBHOOK_SECRET=${cfg.OPENAI_WEBHOOK_SECRET || ''}`,
    `OPENAI_VOICE=${cfg.OPENAI_VOICE}`,
    '',
    '# === Server ===',
    `PORT=${cfg.PORT}`,
    `PUBLIC_BASE_URL=${cfg.PUBLIC_BASE_URL}`,
    '',
    '# === Safety ===',
    '# Outbound calling defaults to enabled. Set false to disable the outbound call endpoint.',
    `AMBER_ENABLE_OUTBOUND_CALLS=${cfg.AMBER_ENABLE_OUTBOUND_CALLS}`,
  ];

  if (cfg.OPENCLAW_GATEWAY_URL) {
    lines.push('', '# === OpenClaw Gateway ===',
      `OPENCLAW_GATEWAY_URL=${cfg.OPENCLAW_GATEWAY_URL}`,
      `OPENCLAW_GATEWAY_TOKEN=${cfg.OPENCLAW_GATEWAY_TOKEN || ''}`);
  }

  if (cfg.ASSISTANT_NAME || cfg.OPERATOR_NAME) {
    lines.push('', '# === Personalization ===');
    for (const k of ['ASSISTANT_NAME','OPERATOR_NAME','OPERATOR_PHONE','OPERATOR_EMAIL','ORG_NAME','DEFAULT_CALENDAR']) {
      if (cfg[k]) lines.push(`${k}=${cfg[k]}`);
    }
  }

  if (cfg.GENZ_CALLER_NUMBERS) {
    lines.push('', '# === Call Screening ===', `GENZ_CALLER_NUMBERS=${cfg.GENZ_CALLER_NUMBERS}`);
  }

  lines.push('');
  writeFileSync(envPath, lines.join('\n'));
  ok(`.env written to ${envPath}`);

  // ── Post-setup ─────────────────────────────────────────────────────
  head('Post-Setup');
  info('Configuration is complete. To keep this wizard safe and transparent, it does not run install/build commands itself.');
  info('Run these commands next from the runtime directory:');
  info('  npm install');
  info('  npm run build');

  if (process.platform === 'darwin') {
    head('Native Tools (macOS)');
    info('Amber can use native macOS helpers for Calendar and Contacts access.');
    info('If you need Calendar support, compile the helper after setup:');
    info('  mkdir -p ../tools');
    info('  swiftc src/ical-query.swift -o ../tools/ical-query -framework EventKit -O');
    info('Then trigger the macOS permission dialog with:');
    info('  ../tools/ical-query today');
  }

  head('Claude Desktop / Cowork Plugin (optional)');
  let isCowork = false;
  if (await yesNo('Are you setting up for Claude Desktop / Cowork?', false)) {
    isCowork = true;
    info('To sync Apple Contacts after setup, run:');
    info('  npm run sync-contacts');
    info('The cache stays local at runtime/contacts-cache.json.');
  }

  // ── Summary ────────────────────────────────────────────────────────
  head('All Done! 🎉');

  const webhookUrl = `${cfg.PUBLIC_BASE_URL}/twilio/inbound`;
  const hasNativeTools = process.platform === 'darwin' &&
    existsSync(resolve(__dirname, '..', 'tools', 'ical-query'));
  const hasContactsCache = isCowork && existsSync(resolve(__dirname, 'contacts-cache.json'));

  console.log(`
${c.bold}Next steps:${c.reset}

  1. ${c.cyan}Configure Twilio webhook:${c.reset}
     Go to ${c.bold}https://console.twilio.com${c.reset} → Phone Numbers → ${cfg.TWILIO_CALLER_ID}
     Set Voice webhook (HTTP POST) to:
     ${c.green}${c.bold}${webhookUrl}${c.reset}

  2. ${c.cyan}Start the server:${c.reset}
     ${c.bold}npm start${c.reset}

  3. ${c.cyan}Test it:${c.reset}
     Call ${c.bold}${cfg.TWILIO_CALLER_ID}${c.reset} — your voice assistant should answer!
${hasNativeTools ? `
  4. ${c.cyan}Calendar access:${c.reset}
     ical-query compiled and configured.
     If permission was denied, grant it in:
     ${c.bold}System Settings → Privacy & Security → Calendar${c.reset}
` : ''}${hasContactsCache ? `
  ${hasNativeTools ? '5' : '4'}. ${c.cyan}Contacts:${c.reset}
     Apple Contacts synced to local cache.
     To refresh: ${c.bold}npm run sync-contacts${c.reset}
` : ''}
${c.dim}Config saved to: ${envPath}${c.reset}
`);

  rl.close();
}

main().catch((err) => {
  if (err.code === 'ERR_USE_AFTER_CLOSE' || err.message?.includes('readline was closed')) {
    // user hit Ctrl+C
    console.log(`\n${c.yellow}Setup cancelled.${c.reset}`);
  } else {
    console.error(`\n${c.red}Setup error: ${err.message}${c.reset}`);
  }
  process.exit(1);
});
