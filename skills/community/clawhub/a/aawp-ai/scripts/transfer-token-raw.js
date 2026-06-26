#!/usr/bin/env node
// Transfer exact raw token amount directly
'use strict';
const path = require('path');
const { ethers } = require('ethers');
const S = process.env.AAWP_SKILL || path.resolve(__dirname, '..');
const chains = JSON.parse(require('fs').readFileSync(path.join(S, 'config/chains.json'), 'utf8'));
const chain = chains['base'];
const p = new ethers.JsonRpcProvider(chain.rpc);

const TOKEN = process.argv[2];
const TO = process.argv[3];
const RAW_AMOUNT = BigInt(process.argv[4]);
const walletAddr = process.env.AAWP_WALLET;
if (!walletAddr || !TOKEN || !TO || !RAW_AMOUNT) {
  console.error('Usage: AAWP_WALLET=0x... node transfer-token-raw.js <token> <to> <rawAmount>');
  process.exit(1);
}

const ERC20_ABI = [
  'function transfer(address,uint256) returns (bool)',
  'function balanceOf(address) view returns (uint256)',
  'function symbol() view returns (string)',
];

const { execSync } = require('child_process');

async function main() {
  const tok = new ethers.Contract(TOKEN, ERC20_ABI, p);
  const [sym, bal] = await Promise.all([tok.symbol(), tok.balanceOf(walletAddr)]);
  console.log(`Token: ${sym}`);
  console.log(`Balance: ${bal.toString()}`);
  console.log(`Sending: ${RAW_AMOUNT.toString()} to ${TO}`);

  if (bal < RAW_AMOUNT) {
    console.error('❌ Insufficient balance');
    process.exit(1);
  }

  // Encode transfer calldata
  const iface = new ethers.Interface(['function transfer(address,uint256) returns (bool)']);
  const calldata = iface.encodeFunctionData('transfer', [TO, RAW_AMOUNT]);
  console.log('Calldata:', calldata.slice(0, 20) + '...');

  // Use wallet-manager call with raw calldata
  const result = execSync(
    `AAWP_WALLET=${walletAddr} node ${path.join(__dirname, 'wallet-manager.js')} --chain base call ${TOKEN} ${calldata}`,
    { encoding: 'utf8', cwd: S }
  );
  console.log(result);
}

main().catch(e => { console.error('❌', e.message); process.exit(1); });
