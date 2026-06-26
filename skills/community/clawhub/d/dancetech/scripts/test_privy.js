#!/usr/bin/env node
// Test Privy connectivity by creating a testnet wallet on Base Sepolia

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const WORKSPACE = path.resolve(__dirname, '..');
const ENV_PATH = path.join(WORKSPACE, '.env');

function loadEnv() {
  const content = fs.readFileSync(ENV_PATH, 'utf8');
  const env = {};
  content.split('\n').forEach(line => {
    line = line.trim();
    if (!line || line.startsWith('#')) return;
    const idx = line.indexOf('=');
    if (idx > 0) env[line.substring(0, idx).trim()] = line.substring(idx + 1).trim();
  });
  return env;
}
const env = loadEnv();
process.env.PRIVY_APP_ID = env.PRIVY_APP_ID;
process.env.PRIVY_APP_SECRET = env.PRIVY_APP_SECRET;

const fetch = globalThis.fetch;
const { Buffer } = require('buffer');

async function testPrivy() {
  const appId = process.env.PRIVY_APP_ID;
  const appSecret = process.env.PRIVY_APP_SECRET;
  if (!appId || !appSecret) {
    console.error('Missing PRIVY_APP_ID or PRIVY_APP_SECRET in .env');
    process.exit(1);
  }
  const auth = Buffer.from(`${appId}:${appSecret}`).toString('base64');

  // Create policy for testnet commerce (Base Sepolia)
  const policy = {
    version: '1.0',
    name: 'Agent testnet commerce policy',
    chain_type: 'ethereum',
    rules: [{
      name: 'Max 0.1 Sepolia ETH per transaction',
      method: 'eth_sendTransaction',
      conditions: [{ field_source: 'ethereum_transaction', field: 'value', operator: 'lte', value: '100000000000000000' }],
      action: 'ALLOW'
    }, {
      name: 'Base Sepolia only',
      method: 'eth_sendTransaction',
      conditions: [{ field_source: 'ethereum_transaction', field: 'chain_id', operator: 'eq', value: '84532' }],
      action: 'ALLOW'
    }]
  };

  console.log('Creating policy...');
  const policyRes = await fetch('https://api.privy.io/v1/policies', {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${auth}`,
      'privy-app-id': appId,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(policy)
  });
  const policyData = await policyRes.json();
  if (!policyRes.ok) {
    console.error('Policy error status:', policyRes.status);
    console.error('Response body:', JSON.stringify(policyData));
    process.exit(1);
  }
  const policyId = policyData.id;
  console.log('Policy created:', policyId);

  // Create wallet
  console.log('Creating wallet...');
  const walletRes = await fetch('https://api.privy.io/v1/wallets', {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${auth}`,
      'privy-app-id': appId,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      chain_type: 'ethereum',
      policy_ids: [policyId]
    })
  });
  const walletData = await walletRes.json();
  if (!walletRes.ok) {
    console.error('Wallet error:', JSON.stringify(walletData));
    process.exit(1);
  }
  console.log('Wallet created successfully!');
  console.log('Wallet ID:', walletData.id);
  console.log('Address:', walletData.address);
  console.log('Chain:', walletData.chain_type);
  console.log('Add PRIVY_WALLET_ADDRESS=' + walletData.address + ' to your .env for future commerce demos.');
}

testPrivy().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
