/**
 * AGIRAILS Balance Check Script
 * 
 * Quick test to verify your wallet setup is working.
 * 
 * Usage:
 *   npx ts-node test-balance.ts
 * 
 * Requires:
 *   - .actp/keystore.json OR ACTP_PRIVATE_KEY env var
 *   - @agirails/sdk installed
 */

import { ACTPClient } from '@agirails/sdk';
import { ethers } from 'ethers';

async function main() {
  console.log('🔍 AGIRAILS Balance Check\n');

  const mode = (process.env.AGIRAILS_MODE as 'mock' | 'testnet' | 'mainnet') || 'testnet';
  console.log(`Mode: ${mode}\n`);

  try {
    // SDK auto-detects wallet: .actp/keystore.json → ACTP_PRIVATE_KEY → PRIVATE_KEY
    const client = await ACTPClient.create({ mode });
    const address = await client.getAddress();
    console.log(`Address: ${address}`);

    // Get balance
    const balance = await client.getBalance(address);
    const formattedBalance = ethers.formatUnits(balance, 6);

    console.log(`💰 USDC Balance: $${formattedBalance}`);

    // Check thresholds
    const balanceNum = parseFloat(formattedBalance);
    
    if (balanceNum < 1) {
      console.log('⚠️  Balance very low - fund wallet before testing');
    } else if (balanceNum < 20) {
      console.log('⚠️  Balance below recommended minimum ($20)');
    } else if (balanceNum < 50) {
      console.log('✅ Balance OK for testing');
    } else {
      console.log('✅ Balance good');
    }

    // Get connected network
    console.log(`\n📡 Network: Base ${mode === 'mainnet' ? 'Mainnet' : 'Sepolia'}`);

  } catch (error: any) {
    console.error('❌ Error:', error.message);
    
    if (error.message.includes('private key')) {
      console.error('\nHint: Run `npx actp init` to set up your keystore, or set ACTP_PRIVATE_KEY env var');
    }
    
    process.exit(1);
  }
}

main();
