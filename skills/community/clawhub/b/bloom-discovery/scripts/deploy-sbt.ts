#!/usr/bin/env ts-node
/**
 * Deploy BloomTasteCard SBT contract to Base Sepolia (or mainnet).
 *
 * Usage:
 *   npx ts-node scripts/deploy-sbt.ts
 *
 * Requires:
 *   - DEPLOYER_PRIVATE_KEY in .env
 *
 * After deploy, add the printed address to .env as SBT_CONTRACT_ADDRESS.
 */
import 'dotenv/config';
import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';
import {
  createPublicClient,
  createWalletClient,
  http,
} from 'viem';
import { base, baseSepolia } from 'viem/chains';
import { privateKeyToAccount } from 'viem/accounts';

// ---------------------------------------------------------------------------
// 1. Compile contract with solc (npx solc = solcjs wrapper)
// ---------------------------------------------------------------------------
function compile(): { abi: any[]; bytecode: `0x${string}` } {
  const projectRoot = path.resolve(__dirname, '..');
  const contractPath = path.resolve(projectRoot, 'contracts/BloomTasteCard.sol');
  const outDir = path.resolve(projectRoot, '.solc-output');

  console.log('Compiling BloomTasteCard.sol ...');

  // Clean previous output
  fs.rmSync(outDir, { recursive: true, force: true });
  fs.mkdirSync(outDir, { recursive: true });

  // Compile with solcjs via npx
  execSync(
    `npx solc --bin --abi --optimize --optimize-runs 200 ` +
    `--base-path "${projectRoot}" ` +
    `--include-path "${path.join(projectRoot, 'node_modules')}" ` +
    `-o "${outDir}" ` +
    `"${contractPath}"`,
    { encoding: 'utf-8', maxBuffer: 10 * 1024 * 1024 },
  );

  // Read compiled artifacts (solcjs uses flattened filenames)
  const abiFile = path.join(outDir, 'contracts_BloomTasteCard_sol_BloomTasteCard.abi');
  const binFile = path.join(outDir, 'contracts_BloomTasteCard_sol_BloomTasteCard.bin');

  if (!fs.existsSync(abiFile) || !fs.existsSync(binFile)) {
    throw new Error('Compilation output not found — check solc errors above');
  }

  const abi = JSON.parse(fs.readFileSync(abiFile, 'utf-8'));
  const bin = fs.readFileSync(binFile, 'utf-8').trim();

  if (!bin) {
    throw new Error('Empty bytecode — contract may be abstract');
  }

  console.log('Compilation successful.');
  return { abi, bytecode: `0x${bin}` as `0x${string}` };
}

// ---------------------------------------------------------------------------
// 2. Resolve deployer private key
// ---------------------------------------------------------------------------
function getDeployerKey(): `0x${string}` {
  const key = process.env.DEPLOYER_PRIVATE_KEY;
  if (!key) {
    throw new Error('Missing DEPLOYER_PRIVATE_KEY in .env');
  }
  return (key.startsWith('0x') ? key : `0x${key}`) as `0x${string}`;
}

// ---------------------------------------------------------------------------
// 3. Deploy
// ---------------------------------------------------------------------------
async function main() {
  const network = (process.env.NETWORK as string) || 'base-sepolia';
  const chain = network === 'base-mainnet' ? base : baseSepolia;

  console.log(`\nTarget network: ${chain.name} (${chain.id})`);

  const { abi, bytecode } = compile();
  const privateKey = getDeployerKey();
  const account = privateKeyToAccount(privateKey);

  console.log(`Deployer: ${account.address}`);

  const publicClient = createPublicClient({
    chain,
    transport: http(chain.rpcUrls.default.http[0]),
  });

  const walletClient = createWalletClient({
    account,
    chain,
    transport: http(chain.rpcUrls.default.http[0]),
  });

  console.log('Deploying BloomTasteCard ...');

  const hash = await walletClient.deployContract({
    abi,
    bytecode,
    args: [],
  });

  console.log(`Tx submitted: ${hash}`);
  console.log('Waiting for confirmation ...');

  const receipt = await publicClient.waitForTransactionReceipt({ hash });

  if (!receipt.contractAddress) {
    throw new Error('Deploy failed — no contract address in receipt');
  }

  const explorerBase = network === 'base-mainnet'
    ? 'https://basescan.org'
    : 'https://sepolia.basescan.org';

  console.log('\n========================================');
  console.log(`Contract deployed!`);
  console.log(`  Address : ${receipt.contractAddress}`);
  console.log(`  Tx Hash : ${hash}`);
  console.log(`  Network : ${chain.name}`);
  console.log(`  Explorer: ${explorerBase}/address/${receipt.contractAddress}`);
  console.log('========================================');
  console.log(`\nAdd to .env:`);
  console.log(`  SBT_CONTRACT_ADDRESS=${receipt.contractAddress}`);
}

main().catch(err => {
  console.error('\nDeploy failed:', err.message || err);
  process.exit(1);
});
