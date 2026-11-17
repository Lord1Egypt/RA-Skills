#!/usr/bin/env node
/**
 * sync.js — Sync local Evolver assets with Evomap Hub
 * Uses correct A2A API endpoints (GET /a2a/assets instead of deprecated POST /a2a/assets/purchased)
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const crypto = require('crypto');

const HOME = process.env.HOME || process.env.USERPROFILE || process.cwd();
const NODE_SECRET = fs.readFileSync(path.join(HOME, '.evomap', 'node_secret'), 'utf-8').trim();
const NODE_ID = fs.readFileSync(path.join(HOME, '.evomap', 'node_id'), 'utf-8').trim();
const HUB_URL = process.env.HUB_URL || 'https://hub.evomap.ai';

// Prefer OAuth token (token.json) over node_secret when present
function getAuthToken() {
  try {
    const tokenFile = path.join(HOME, '.evomap', 'token.json');
    const t = JSON.parse(fs.readFileSync(tokenFile, 'utf-8'));
    if (t.token) return t.token;
  } catch (e) { /* fall through */ }
  return NODE_SECRET;
}
const AUTH_TOKEN = getAuthToken();

function a2aEnvelope(messageType, payload = {}) {
  return {
    protocol: 'gep-a2a',
    protocol_version: '1.0.0',
    message_type: messageType,
    message_id: `msg_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`,
    sender_id: NODE_ID,
    timestamp: new Date().toISOString(),
    payload
  };
}

function httpsGet(urlPath) {
  return new Promise((resolve, reject) => {
    const url = new URL(HUB_URL + urlPath);
    const options = {
      hostname: url.hostname,
      path: url.pathname + url.search,
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${AUTH_TOKEN}`
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(data) });
        } catch (e) {
          resolve({ status: res.statusCode, data: { raw: data } });
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

function httpsPost(urlPath, body) {
  return new Promise((resolve, reject) => {
    const url = new URL(HUB_URL + urlPath);
    const bodyStr = JSON.stringify(body);
    const options = {
      hostname: url.hostname,
      path: url.pathname,
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${AUTH_TOKEN}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(bodyStr)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(data) });
        } catch (e) {
          resolve({ status: res.statusCode, data: { raw: data } });
        }
      });
    });

    req.on('error', reject);
    req.write(bodyStr);
    req.end();
  });
}

async function syncAssets() {
  console.log(`[sync] Node: ${NODE_ID}`);
  console.log('[sync] Fetching assets from Hub...');

  // Use GET /a2a/assets (correct endpoint)
  const result = await httpsGet('/a2a/assets?status=all&limit=50');
  
  if (result.status === 200 && result.data.assets) {
    console.log(`[sync] Fetched ${result.data.count} asset(s)`);
    for (const asset of result.data.assets.slice(0, 5)) {
      console.log(`  - [${asset.asset_type}] ${asset.short_title || asset.asset_id.slice(0, 20)}... (${asset.status})`);
    }
    if (result.data.count > 5) {
      console.log(`  ... and ${result.data.count - 5} more`);
    }
    return result.data;
  } else {
    console.error('[sync] Error:', result.data.error || result.data);
    return null;
  }
}

async function getNodeInfo() {
  console.log(`[node-info] Node: ${NODE_ID}`);
  const result = await httpsGet(`/a2a/nodes/${NODE_ID}`);
  
  if (result.status === 200) {
    console.log('[node-info] Node info:', JSON.stringify(result.data, null, 2));
    return result.data;
  } else {
    console.error('[node-info] Error:', result.data.error || result.data);
    return null;
  }
}

async function publishAssets(assets) {
  console.log(`[publish] Publishing ${assets.length} asset(s)...`);
  const envelope = a2aEnvelope('publish', { assets });
  const result = await httpsPost('/a2a/publish', envelope);
  
  console.log('[publish] Result:', JSON.stringify(result.data, null, 2));
  return result.data;
}

// CLI
if (require.main === module) {
  const cmd = process.argv[2];
  if (cmd === 'sync') {
    syncAssets().catch(console.error);
  } else if (cmd === 'node-info') {
    getNodeInfo().catch(console.error);
  } else if (cmd === 'publish') {
    const assetsFile = process.argv[3];
    if (!assetsFile) {
      console.error('Usage: node sync.js publish <assets.json>');
      process.exit(1);
    }
    const assets = JSON.parse(fs.readFileSync(assetsFile, 'utf-8'));
    publishAssets(assets).catch(console.error);
  } else {
    console.log('Usage: node sync.js <sync|node-info|publish>');
    process.exit(1);
  }
}
