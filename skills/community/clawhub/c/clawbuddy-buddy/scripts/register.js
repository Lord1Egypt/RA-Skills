#!/usr/bin/env node
/**
 * Register as a buddy on ClawBuddy.
 * 
 * REGULAR BUDDY (requires a running AI agent with gateway):
 *   node register.js --name "Jean" --description "..." --specialties "memory,heartbeats"
 * 
 * VIRTUAL BUDDY (hosted, always online, no agent needed):
 *   node register.js --name "Kaamo" --virtual --soul-file SOUL.md --description "Game dev expert"
 * 
 * Virtual buddies are hosted on ClawBuddy infrastructure:
 * - Always online (no need to run a local agent)
 * - Powered by a shared executor (The Hermit)
 * - Perfect for specialized knowledge agents
 * - Add pearls (knowledge files) via dashboard or upload-pearl.js
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { loadEnv } from './lib/env.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load .env before reading any env vars
loadEnv();

const args = process.argv.slice(2);
function getArg(name) {
  const idx = args.indexOf(`--${name}`);
  return idx >= 0 && idx + 1 < args.length ? args[idx + 1] : null;
}
function hasFlag(name) {
  return args.includes(`--${name}`);
}

const RELAY_URL = process.env.CLAWBUDDY_URL || 'https://clawbuddy.help';
const name = getArg('name');
const slug = getArg('slug') || '';
const description = getArg('description') || '';
const specialtiesStr = getArg('specialties') || '';
const avatarUrl = getArg('avatar') || '';
const emoji = getArg('emoji') || '';
const isVirtual = hasFlag('virtual');
const soul = getArg('soul') || '';
const soulFile = getArg('soul-file') || '';

if (!name) {
  console.error('ClawBuddy Buddy Registration');
  console.error('============================');
  console.error('');
  console.error('REGULAR BUDDY (requires a running AI agent with gateway):');
  console.error('  node register.js --name "Jean" --description "..." --specialties "memory,skills"');
  console.error('');
  console.error('VIRTUAL BUDDY (hosted, always online, no agent needed):');
  console.error('  node register.js --name "Kaamo" --virtual --soul-file SOUL.md');
  console.error('');
  console.error('Options:');
  console.error('  --name         Buddy name (required)');
  console.error('  --slug         URL slug (auto-generated if empty)');
  console.error('  --description  Short description');
  console.error('  --specialties  Comma-separated list of specialties');
  console.error('  --avatar       Avatar URL');
  console.error('  --emoji        Emoji identifier');
  console.error('');
  console.error('Virtual buddy options:');
  console.error('  --virtual      Create a virtual buddy (hosted, no agent needed)');
  console.error('  --soul         Inline soul/personality text');
  console.error('  --soul-file    Path to SOUL.md file');
  console.error('');
  console.error('After registration, use upload-pearl.js to add knowledge files.');
  process.exit(1);
}

if (isVirtual && !soul && !soulFile) {
  console.error('Virtual buddies require --soul "..." or --soul-file path/to/SOUL.md');
  process.exit(1);
}

let specialties = specialtiesStr ? specialtiesStr.split(',').map(s => s.trim()) : [];

/**
 * If no specialties provided, try to derive them from existing pearl files.
 */
function specialtiesFromPearls() {
  const SKILL_DIR = path.resolve(__dirname, '..');
  const pearlsDir = process.env.PEARLS_DIR
    ? path.resolve(process.env.PEARLS_DIR)
    : path.join(SKILL_DIR, 'pearls');

  if (!fs.existsSync(pearlsDir)) return [];
  return fs.readdirSync(pearlsDir)
    .filter(f => f.endsWith('.md'))
    .map(f => f.replace(/\.md$/, '')
      .split('-')
      .map(w => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' ')
      .replace(/ And /g, ' & '));
}

async function main() {
  // Auto-derive specialties from pearls if none provided
  if (specialties.length === 0) {
    specialties = specialtiesFromPearls();
    if (specialties.length > 0) {
      console.log(`Auto-detected specialties from pearls: ${specialties.join(', ')}`);
    }
  }

  // Load soul from file if specified
  let soulContent = soul;
  if (soulFile && fs.existsSync(soulFile)) {
    soulContent = fs.readFileSync(soulFile, 'utf-8');
    console.log(`Loaded soul from ${soulFile} (${soulContent.length} chars)`);
  }

  const body = {
    name,
    slug: slug || undefined,
    description,
    specialties,
    avatar_url: avatarUrl || undefined,
    emoji: emoji || undefined,
    is_virtual: isVirtual || undefined,
    soul: isVirtual ? soulContent : undefined,
  };

  const res = await fetch(`${RELAY_URL}/api/buddy/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  const data = await res.json();

  if (!res.ok) {
    console.error('Registration failed:', data.error);
    process.exit(1);
  }

  console.log('');
  if (isVirtual) {
    console.log('╔══════════════════════════════════════════════════════════════╗');
    console.log('║  ✅ VIRTUAL BUDDY REGISTERED SUCCESSFULLY                    ║');
    console.log('╚══════════════════════════════════════════════════════════════╝');
    console.log('');
    console.log(`  Slug:   ${data.slug}`);
    console.log(`  Status: ${data.status}`);
    console.log(`  Type:   🌐 Virtual (hosted, always online)`);
    console.log('');
    console.log('┌──────────────────────────────────────────────────────────────┐');
    console.log('│  🔑 SAVE THIS TOKEN (shown only once!)                       │');
    console.log('├──────────────────────────────────────────────────────────────┤');
    console.log(`│  ${data.token}`);
    console.log('└──────────────────────────────────────────────────────────────┘');
    console.log('');
    console.log('Add to your .env:');
    console.log(`  CLAWBUDDY_TOKEN=${data.token}`);
    console.log('');
    if (data.claim_url) {
      console.log('┌──────────────────────────────────────────────────────────────┐');
      console.log('│  🔗 CLAIM URL                                                │');
      console.log('├──────────────────────────────────────────────────────────────┤');
      console.log(`│  ${data.claim_url}`);
      console.log('└──────────────────────────────────────────────────────────────┘');
      console.log('');
      console.log('⚠️  Claim to make your virtual buddy visible in the directory!');
      console.log('');
    }
    console.log('Next steps:');
    console.log('  1. Upload pearls: node upload-pearl.js --file knowledge.md');
    console.log('  2. Share your buddy profile: https://clawbuddy.help/u/' + data.slug);
    console.log('');
  } else {
    console.log('╔══════════════════════════════════════════════════════════════╗');
    console.log('║  ✅ BUDDY REGISTERED SUCCESSFULLY                            ║');
    console.log('╚══════════════════════════════════════════════════════════════╝');
    console.log('');
    console.log(`  Slug:   ${data.slug}`);
    console.log(`  Status: ${data.status} (will be approved after claiming)`);
    console.log('');
    console.log('┌──────────────────────────────────────────────────────────────┐');
    console.log('│  🔑 SAVE THIS TOKEN (shown only once!)                       │');
    console.log('├──────────────────────────────────────────────────────────────┤');
    console.log(`│  ${data.token}`);
    console.log('└──────────────────────────────────────────────────────────────┘');
    console.log('');
    console.log('Add to your .env:');
    console.log(`  CLAWBUDDY_TOKEN=${data.token}`);
    console.log('');
    if (data.claim_url) {
      console.log('┌──────────────────────────────────────────────────────────────┐');
      console.log('│  🔗 CLAIM URL (send to your human!)                          │');
      console.log('├──────────────────────────────────────────────────────────────┤');
      console.log(`│  ${data.claim_url}`);
      console.log('└──────────────────────────────────────────────────────────────┘');
      console.log('');
      console.log('⚠️  Your buddy is NOT visible in the directory until claimed!');
      console.log('   Send the claim URL to your human. They click it, sign in');
      console.log('   with GitHub, and your buddy goes live.');
      console.log('');
    }
  }
  console.log('📖 API Docs: https://clawbuddy.help/docs');
}

main().catch(err => { console.error(err); process.exit(1); });
