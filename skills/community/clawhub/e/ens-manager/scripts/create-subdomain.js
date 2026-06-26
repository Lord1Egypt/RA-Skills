#!/usr/bin/env node

/**
 * create-subdomain.js
 * 
 * Minimal script to create ENS subdomain WITHOUT IPFS content.
 * Fewer dependencies, simpler workflow for basic subdomain creation.
 * 
 * Usage:
 *   node create-subdomain.js <parent-name> <subdomain-label> [options]
 * 
 * Example:
 *   node create-subdomain.js clophorse.eth meetup --keystore /path/to/keystore.enc --password "pass"
 *   node create-subdomain.js clophorse.eth api --private-key-env WALLET_PRIVATE_KEY
 * 
 * Options:
 *   --keystore PATH       Path to encrypted keystore file
 *   --password PASS       Keystore password
 *   --private-key-env VAR Environment variable containing private key
 *   --private-key KEY     Private key directly (less secure)
 *   --owner ADDRESS       Owner address (defaults to signer)
 *   --resolver ADDRESS    Resolver address (defaults to PublicResolver)
 */

const { createPublicClient, createWalletClient, http, namehash, keccak256, encodePacked } = require('viem');
const { mainnet } = require('viem/chains');
const { privateKeyToAccount } = require('viem/accounts');
const { createDecipheriv, scryptSync } = require('crypto');
const { readFileSync } = require('fs');

// Contract addresses (Ethereum Mainnet)
const ENS_REGISTRY = '0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e';
const NAME_WRAPPER = '0xD4416b13d2b3a9aBae7AcD5D6C2BbDBE25686401';
const PUBLIC_RESOLVER = '0x231b0Ee14048e9dCcD1d247744d114a4EB5E8E63';

// RPC endpoint
const RPC_URL = process.env.RPC_URL || 'https://mainnet.rpc.buidlguidl.com';

// Parse arguments
function parseArgs() {
  const args = process.argv.slice(2);
  
  if (args.length < 2 || args[0].startsWith('--')) {
    console.error('Usage: node create-subdomain.js <parent-name> <subdomain-label> [options]');
    console.error('');
    console.error('Options:');
    console.error('  --keystore PATH       Encrypted keystore file');
    console.error('  --password PASS       Keystore password');
    console.error('  --private-key-env VAR Environment variable with private key');
    console.error('  --private-key KEY     Private key (0x...)');
    console.error('  --owner ADDRESS       Owner address (defaults to signer)');
    console.error('  --resolver ADDRESS    Resolver address (defaults to PublicResolver)');
    process.exit(1);
  }

  const parentName = args[0].replace('.eth', '') + '.eth';
  const label = args[1];
  
  const options = {
    keystore: null,
    password: null,
    privateKeyEnv: null,
    privateKey: null,
    owner: null,
    resolver: PUBLIC_RESOLVER
  };

  for (let i = 2; i < args.length; i += 2) {
    const key = args[i].replace('--', '');
    const value = args[i + 1];
    
    if (key === 'keystore') options.keystore = value;
    else if (key === 'password') options.password = value;
    else if (key === 'private-key-env') options.privateKeyEnv = value;
    else if (key === 'private-key') options.privateKey = value;
    else if (key === 'owner') options.owner = value;
    else if (key === 'resolver') options.resolver = value;
  }

  return { parentName, label, ...options };
}

// Decrypt keystore
function decryptKeystore(keystorePath, password) {
  const encrypted = readFileSync(keystorePath, 'utf8');
  const { salt, iv, data } = JSON.parse(encrypted);
  
  const key = scryptSync(password, Buffer.from(salt, 'hex'), 32);
  const decipher = createDecipheriv('aes-256-cbc', key, Buffer.from(iv, 'hex'));
  
  return Buffer.concat([
    decipher.update(Buffer.from(data, 'hex')),
    decipher.final()
  ]).toString('utf8');
}

// Get private key from various sources
function getPrivateKey(options) {
  if (options.keystore && options.password) {
    console.log('🔐 Decrypting keystore...');
    return decryptKeystore(options.keystore, options.password);
  }
  
  if (options.privateKeyEnv) {
    const key = process.env[options.privateKeyEnv];
    if (!key) {
      throw new Error(`Environment variable ${options.privateKeyEnv} not set`);
    }
    console.log(`🔐 Using private key from env: ${options.privateKeyEnv}`);
    return key;
  }
  
  if (options.privateKey) {
    console.log('🔐 Using provided private key');
    return options.privateKey;
  }
  
  throw new Error('No wallet credentials provided. Use --keystore + --password or --private-key-env');
}

// Check if name is wrapped
async function isWrapped(name, publicClient) {
  try {
    const owner = await publicClient.readContract({
      address: NAME_WRAPPER,
      abi: [{
        name: 'ownerOf',
        type: 'function',
        stateMutability: 'view',
        inputs: [{ name: 'id', type: 'uint256' }],
        outputs: [{ name: '', type: 'address' }]
      }],
      functionName: 'ownerOf',
      args: [BigInt(namehash(name))]
    });
    return owner !== '0x0000000000000000000000000000000000000000';
  } catch {
    return false;
  }
}

// Create subdomain (unwrapped)
async function createSubdomainUnwrapped(parentName, label, owner, resolver, walletClient) {
  console.log('\n📝 Creating subdomain (unwrapped Registry)...');
  
  const parentNode = namehash(parentName);
  const labelHash = keccak256(encodePacked(['string'], [label]));
  
  // Step 1: Set subnode owner
  console.log('   Step 1/2: Setting subnode owner...');
  const tx1 = await walletClient.writeContract({
    address: ENS_REGISTRY,
    abi: [{
      name: 'setSubnodeOwner',
      type: 'function',
      stateMutability: 'nonpayable',
      inputs: [
        { name: 'node', type: 'bytes32' },
        { name: 'label', type: 'bytes32' },
        { name: 'owner', type: 'address' }
      ],
      outputs: [{ name: '', type: 'bytes32' }]
    }],
    functionName: 'setSubnodeOwner',
    args: [parentNode, labelHash, owner]
  });
  
  console.log(`   TX: ${tx1}`);
  
  // Step 2: Set resolver
  console.log('   Step 2/2: Setting resolver...');
  const subnode = namehash(`${label}.${parentName}`);
  
  const tx2 = await walletClient.writeContract({
    address: ENS_REGISTRY,
    abi: [{
      name: 'setResolver',
      type: 'function',
      stateMutability: 'nonpayable',
      inputs: [
        { name: 'node', type: 'bytes32' },
        { name: 'resolver', type: 'address' }
      ],
      outputs: []
    }],
    functionName: 'setResolver',
    args: [subnode, resolver]
  });
  
  console.log(`   TX: ${tx2}`);
  
  return { tx1, tx2 };
}

// Create subdomain (wrapped)
async function createSubdomainWrapped(parentName, label, owner, resolver, walletClient) {
  console.log('\n📝 Creating subdomain (wrapped NameWrapper)...');
  
  const parentNode = namehash(parentName);
  
  const tx = await walletClient.writeContract({
    address: NAME_WRAPPER,
    abi: [{
      name: 'setSubnodeRecord',
      type: 'function',
      stateMutability: 'nonpayable',
      inputs: [
        { name: 'parentNode', type: 'bytes32' },
        { name: 'label', type: 'string' },
        { name: 'owner', type: 'address' },
        { name: 'resolver', type: 'address' },
        { name: 'ttl', type: 'uint64' },
        { name: 'fuses', type: 'uint32' },
        { name: 'expiry', type: 'uint64' }
      ],
      outputs: [{ name: '', type: 'bytes32' }]
    }],
    functionName: 'setSubnodeRecord',
    args: [parentNode, label, owner, resolver, 0n, 0, 0n]
  });
  
  console.log(`   TX: ${tx}`);
  
  return { tx };
}

// Main
async function main() {
  const { parentName, label, keystore, password, privateKeyEnv, privateKey, owner: customOwner, resolver } = parseArgs();
  
  console.log('🦞 ENS Subdomain Creation');
  console.log('=========================');
  console.log(`📛 Parent: ${parentName}`);
  console.log(`🏷️  Label: ${label}`);
  console.log(`🔍 Subdomain: ${label}.${parentName}`);
  console.log('');
  
  // Create clients
  const publicClient = createPublicClient({
    chain: mainnet,
    transport: http(RPC_URL)
  });
  
  // Get private key
  const privateKeyHex = getPrivateKey({ keystore, password, privateKeyEnv, privateKey });
  const account = privateKeyToAccount(privateKeyHex);
  
  const walletClient = createWalletClient({
    account,
    chain: mainnet,
    transport: http(RPC_URL)
  });
  
  const owner = customOwner || account.address;
  
  console.log(`👤 Signer: ${account.address}`);
  console.log(`👤 Owner: ${owner}`);
  console.log(`🔍 Resolver: ${resolver}`);
  console.log('');
  
  // Check if parent is wrapped
  const wrapped = await isWrapped(parentName, publicClient);
  
  if (wrapped) {
    console.log('🎁 Parent is wrapped');
    await createSubdomainWrapped(parentName, label, owner, resolver, walletClient);
  } else {
    console.log('📦 Parent is unwrapped');
    await createSubdomainUnwrapped(parentName, label, owner, resolver, walletClient);
  }
  
  console.log('\n✅ Subdomain created!');
  console.log('');
  console.log(`📛 Subdomain: ${label}.${parentName}`);
  console.log(`👤 Owner: ${owner}`);
  console.log(`🔍 Resolver: ${resolver}`);
  console.log('');
  console.log('Next steps:');
  console.log('  - Set address record: use ENS app or resolver contract');
  console.log('  - Set content hash: node ../create-subdomain-ipfs.js (if needed)');
  console.log('  - Verify: node check-ens-name.js ' + label + '.' + parentName);
}

main().catch(error => {
  console.error('\n❌ Error:', error.message);
  process.exit(1);
});
