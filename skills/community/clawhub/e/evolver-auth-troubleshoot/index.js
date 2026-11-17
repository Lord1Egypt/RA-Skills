#!/usr/bin/env node
/**
 * evolver-auth-troubleshoot — diagnose EvoMap Evolver Hub auth failures.
 * Usage: node index.js   (reads .env + ~/.evomap, prints diagnosis & fixes)
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');

function hash(str) {
  return crypto.createHash('md5').update(String(str || '')).digest('hex').slice(0, 8);
}

function readEnv(file) {
  const out = {};
  try {
    for (const line of fs.readFileSync(file, 'utf-8').split('\n')) {
      const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
      if (m) out[m[1]] = m[2].trim();
    }
  } catch (_) {}
  return out;
}

function main() {
  const home = os.homedir();
  const envCandidates = [
    path.join(process.cwd(), '.env'),
    path.join(home, '.openclaw', 'workspace', '.env'),
  ];
  const envFile = envCandidates.find((f) => fs.existsSync(f));
  const env = envFile ? readEnv(envFile) : {};

  const evomapDir = path.join(home, '.evomap');
  const nodeIdFile = path.join(evomapDir, 'node_id');
  const secretFile = path.join(evomapDir, 'node_secret');
  const oauthFile = path.join(evomapDir, 'oauth_token.json');

  const localId = fs.existsSync(nodeIdFile) ? fs.readFileSync(nodeIdFile, 'utf-8').trim() : null;
  const localSecret = fs.existsSync(secretFile) ? fs.readFileSync(secretFile, 'utf-8').trim() : null;

  const envId = env.A2A_NODE_ID || null;
  const idMatch = envId === localId;
  const secretMatch = hash(env.A2A_NODE_SECRET) === hash(localSecret);

  console.log('=== Evolver Hub Auth Diagnosis ===');
  console.log(`env file   : ${envFile || '(not found)'}`);
  console.log(`env node id: ${envId || '(unset)'}`);
  console.log(`local id   : ${localId || '(unset)'}`);
  console.log(`id match   : ${idMatch ? 'YES' : 'NO  <-- stale node id'}`);
  console.log(`secret     : env=${hash(env.A2A_NODE_SECRET)} local=${hash(localSecret)} -> ${secretMatch ? 'MATCH' : 'MISMATCH <-- stale secret'}`);

  let oauthOk = false;
  let oauthExp = 'n/a';
  try {
    const t = JSON.parse(fs.readFileSync(oauthFile, 'utf-8'));
    const exp = t.expires_at ? new Date(t.expires_at) : null;
    oauthExp = exp ? exp.toISOString() : 'n/a';
    oauthOk = exp ? exp.getTime() > Date.now() : false;
  } catch (_) {}
  console.log(`oauth token: ${oauthExp} ${oauthOk ? '(valid)' : '(EXPIRED / missing - re-login needed)'}`);

  const hubConfigured = !!(env.A2A_HUB_URL || envId);
  console.log(`hub config : ${hubConfigured ? 'CONNECTED MODE (solidify requires Hub auth)' : 'OFFLINE MODE (solidify works locally)'}`);

  console.log('\n=== Fixes ===');
  if (!idMatch || !secretMatch) {
    console.log('1. Sync .env credentials to ~/.evomap values (node_id / node_secret), then re-verify.');
  }
  if (!oauthOk) {
    console.log('2. Re-authorize: run `evolver login`, open the printed https://evomap.ai/device?user_code=XXX in a browser, enter the code.');
  }
  if (hubConfigured) {
    console.log('3. Optional offline mode: comment out A2A_HUB_URL / A2A_NODE_ID / A2A_NODE_SECRET in .env (solidify then runs locally without Hub).');
  }
  console.log('4. Verify: evolver solidify --dry-run');
  process.exit(0);
}

main();
