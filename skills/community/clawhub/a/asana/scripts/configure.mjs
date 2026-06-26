#!/usr/bin/env node
/**
 * Configure local-only Asana auth for the OpenClaw Asana skill.
 *
 * Recommended: PAT mode
 * Optional: OAuth client credentials for oauth_oob.mjs flows
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

function die(msg) {
  console.error(msg);
  process.exit(1);
}

function asanaDir() {
  return path.join(os.homedir(), '.openclaw', 'asana');
}

function configPath() {
  return path.join(asanaDir(), 'config.json');
}

function credentialsPath() {
  return path.join(asanaDir(), 'credentials.json');
}

function loadJsonIfExists(p, fallback = {}) {
  if (!fs.existsSync(p)) return fallback;
  try {
    return JSON.parse(fs.readFileSync(p, 'utf-8'));
  } catch {
    return fallback;
  }
}

function saveJson(p, data) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(data, null, 2));
}

function parseArgs(argv) {
  const flags = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const k = a.slice(2);
      const v = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
      flags[k] = v;
    }
  }
  return flags;
}

const flags = parseArgs(process.argv.slice(2));
const mode = String(flags.mode || 'pat').toLowerCase();

if (mode === 'pat') {
  const pat = flags.pat || process.env.ASANA_PAT;
  if (!pat) die('PAT mode requires --pat <asana_pat> or ASANA_PAT env var');
  const current = loadJsonIfExists(configPath(), {});
  saveJson(configPath(), { ...current, pat: String(pat) });
  console.log(`Saved Asana PAT to: ${configPath()}`);
  process.exit(0);
}

if (mode === 'oauth') {
  const clientId = flags['client-id'] || process.env.ASANA_CLIENT_ID;
  const clientSecret = flags['client-secret'] || process.env.ASANA_CLIENT_SECRET;
  if (!clientId || !clientSecret) {
    die('OAuth mode requires --client-id and --client-secret (or ASANA_CLIENT_ID / ASANA_CLIENT_SECRET)');
  }
  saveJson(credentialsPath(), {
    client_id: String(clientId),
    client_secret: String(clientSecret),
  });
  console.log(`Saved Asana OAuth credentials to: ${credentialsPath()}`);
  process.exit(0);
}

die('Unknown mode. Use --mode pat or --mode oauth');
