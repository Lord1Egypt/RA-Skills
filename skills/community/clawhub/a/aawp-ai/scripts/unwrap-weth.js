#!/usr/bin/env node
// Unwrap all WETH in the AAWP wallet on Base
'use strict';
const path = require('path');
const { ethers } = require('ethers');

// Load skill environment
const S = process.env.AAWP_SKILL || path.resolve(__dirname, '..');
const C = process.env.AAWP_CONFIG || path.join(__dirname, '..', '.agent-config');

// Load chains config
const chains = JSON.parse(require('fs').readFileSync(path.join(S, 'config/chains.json'), 'utf8'));
const chain = chains['base'];
const p = new ethers.JsonRpcProvider(chain.rpc);

const WETH = '0x4200000000000000000000000000000000000006';
const WETH_ABI = ['function balanceOf(address) view returns (uint256)', 'function withdraw(uint256)'];

// Load the addon and signing machinery from wallet-manager
// We'll use the daemon directly via wallet-manager's signAndSend
// Instead, let's spawn wallet-manager with a batch call via raw calldata

async function main() {
  const walletAddr = process.env.AAWP_WALLET;
  if (!walletAddr) { console.error('Set AAWP_WALLET'); process.exit(1); }
  
  const weth = new ethers.Contract(WETH, WETH_ABI, p);
  const bal = await weth.balanceOf(walletAddr);
  console.log(`WETH balance: ${ethers.formatEther(bal)} WETH`);
  
  if (bal === 0n) { console.log('No WETH to unwrap'); process.exit(0); }
  
  // Encode withdraw(uint256) calldata
  const iface = new ethers.Interface(['function withdraw(uint256)']);
  const calldata = iface.encodeFunctionData('withdraw', [bal]);
  console.log('Calldata:', calldata);
  console.log(`Unwrapping ${ethers.formatEther(bal)} WETH...`);
  
  // Use wallet-manager call with raw calldata (0x prefix mode bypasses fragment bug)
  const { execSync } = require('child_process');
  const result = execSync(
    `AAWP_WALLET=${walletAddr} node ${path.join(__dirname, 'wallet-manager.js')} --chain base call ${WETH} ${calldata}`,
    { encoding: 'utf8', cwd: S }
  );
  console.log(result);
}

main().catch(e => { console.error('❌', e.message); process.exit(1); });
