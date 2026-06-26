#!/usr/bin/env node
/**
 * bootstrap-token.mjs — Multi-client Figma MCP token bootstrap
 *
 * Scans known MCP client credential stores for a valid Figma OAuth token,
 * optionally refreshes it, then writes it into OpenClaw config.
 *
 * Credential reading is delegated to token-scanner.mjs (pure file I/O).
 * This file handles only network (token refresh) and config writing.
 *
 * Usage:
 *   node scripts/bootstrap-token.mjs [--dry-run] [--refresh]
 *
 * This is a TEMPORARY workaround. Once Figma opens DCR for custom clients
 * or OpenClaw becomes an approved MCP client, direct auth will replace this.
 */

import { writeFileSync } from 'fs';
import { scanForFigmaToken, readOpenClawConfig } from './token-scanner.mjs';

const DRY_RUN = process.argv.includes('--dry-run');
const REFRESH = process.argv.includes('--refresh');

// --- Token refresh (network only) ---

async function refreshToken(source) {
  if (!source.refreshToken || !source.clientId) {
    console.error('⚠️  No refresh token or client ID — cannot refresh.');
    return null;
  }

  const metaRes = await fetch('https://api.figma.com/v1/oauth/token');
  if (!metaRes.ok) {
    console.error(`⚠️  Failed to fetch OAuth metadata: ${metaRes.status}`);
    return null;
  }
  const meta = await metaRes.json().catch(() => null);
  const tokenEndpoint = meta?.token_endpoint || 'https://api.figma.com/v1/oauth/token';

  const body = new URLSearchParams({
    grant_type: 'refresh_token',
    refresh_token: source.refreshToken,
    client_id: source.clientId,
  });
  if (source.clientSecret) body.set('client_secret', source.clientSecret);

  const tokenRes = await fetch(tokenEndpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });

  if (!tokenRes.ok) {
    const text = await tokenRes.text().catch(() => '');
    console.error(`⚠️  Token refresh failed: ${tokenRes.status} — ${text.slice(0, 200)}`);
    return null;
  }

  const tokens = await tokenRes.json();
  return {
    accessToken: tokens.access_token,
    refreshToken: tokens.refresh_token || source.refreshToken,
    expiresAt: tokens.expires_in ? Date.now() + tokens.expires_in * 1000 : null,
  };
}

// --- OpenClaw config writer ---

function writeToOpenClaw(token) {
  const found = readOpenClawConfig();
  if (!found) { console.error('❌ openclaw.json not found.'); return false; }
  let { config, configPath } = found;

  config.mcp = config.mcp || {};
  config.mcp.servers = config.mcp.servers || {};
  config.mcp.servers.figma = config.mcp.servers.figma || {};
  config.mcp.servers.figma.url = 'https://mcp.figma.com/mcp';
  config.mcp.servers.figma.headers = { Authorization: `Bearer ${token}` };

  if (DRY_RUN) {
    console.log(`🔍 DRY RUN — would write to: ${configPath}`);
    console.log(`   mcp.servers.figma.headers.Authorization = Bearer ${token.slice(0, 8)}...`);
    return true;
  }

  writeFileSync(configPath, JSON.stringify(config, null, 2));
  console.log(`✅ Token written to ${configPath}`);
  return true;
}

// --- Main ---

console.log('🔎 Scanning for Figma MCP tokens...\n');

const source = scanForFigmaToken();

if (!source) {
  console.error('❌ No Figma MCP token found. Connect Figma via a supported client first:');
  console.error('   Claude Code: claude plugin install figma');
  console.error('   Cursor, VS Code, Codex: add Figma in MCP settings');
  process.exit(1);
}

console.log(`✅ Found token from ${source.source}`);
console.log(`   File: ${source.file}`);
if (source.key) console.log(`   Key: ${source.key}`);
if (source.expiresAt) {
  const exp = new Date(source.expiresAt);
  const expired = exp < new Date();
  console.log(`   Expires: ${exp.toISOString()} ${expired ? '⚠️ EXPIRED' : '✅'}`);
}
if (source.refreshToken) console.log('   Refresh token: available');

let token = source.token;

if (REFRESH && source.refreshToken) {
  console.log('\n🔄 Refreshing token...');
  const refreshed = await refreshToken(source);
  if (refreshed) {
    token = refreshed.accessToken;
    if (refreshed.expiresAt) {
      console.log(`✅ Token refreshed.\n   New expiry: ${new Date(refreshed.expiresAt).toISOString()}`);
    } else {
      console.log('✅ Token refreshed.');
    }
  } else {
    console.error('⚠️  Refresh failed — using existing token (may be expired).');
  }
}

console.log('');
writeToOpenClaw(token);

if (!DRY_RUN) {
  console.log('\n💡 Restart the OpenClaw gateway to apply:');
  console.log('   openclaw gateway restart');
}
