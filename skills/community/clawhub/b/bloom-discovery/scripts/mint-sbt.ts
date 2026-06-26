#!/usr/bin/env ts-node
import 'dotenv/config';
import { mintIdentitySbt } from '../src/blockchain/identity-sbt';

async function main() {
  const walletAddress = process.argv[2];
  if (!walletAddress) {
    console.error('Usage: ts-node scripts/mint-sbt.ts <walletAddress>');
    process.exit(1);
  }

  const contractAddress = process.env.SBT_CONTRACT_ADDRESS as `0x${string}` | undefined;
  if (!contractAddress) {
    console.error('Missing SBT_CONTRACT_ADDRESS');
    process.exit(1);
  }

  const privateKey = process.env.DEPLOYER_PRIVATE_KEY;
  if (!privateKey) {
    console.error('Missing DEPLOYER_PRIVATE_KEY in .env');
    process.exit(1);
  }
  const key = (privateKey.startsWith('0x') ? privateKey : `0x${privateKey}`) as `0x${string}`;

  const network = (process.env.NETWORK || 'base-sepolia') as 'base-mainnet' | 'base-sepolia';

  const tokenUri = `data:application/json;base64,${Buffer.from(JSON.stringify({
    name: 'Bloom Identity (Demo)',
    description: 'Demo SBT mint for Bloom Identity',
    attributes: [{ trait_type: 'walletAddress', value: walletAddress }],
  })).toString('base64')}`;

  const txHash = await mintIdentitySbt({
    contractAddress,
    to: walletAddress as `0x${string}`,
    tokenUri,
    network,
    privateKey: key,
  });

  console.log('Minted:', txHash);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
