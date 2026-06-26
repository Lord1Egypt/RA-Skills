#!/usr/bin/env node
/**
 * ENS Subdomain Creator with IPFS Content Hash
 * 
 * Creates an ENS subdomain and sets its IPFS content hash in one script.
 * Handles both wrapped (NameWrapper) and unwrapped (Registry) ENS names.
 * 
 * Usage:
 *   node create-subdomain-ipfs.js <parent-name> <subdomain-label> <ipfs-cid> [options]
 * 
 * Example:
 *   node create-subdomain-ipfs.js clophorse.eth meetup QmABC123... --keystore /path/to/keystore.enc --password "pass"
 * 
 * Options:
 *   --keystore PATH    Path to encrypted keystore file
 *   --password PASS    Keystore password
 *   --rpc URL          Custom RPC endpoint (default: ethereum-rpc.publicnode.com)
 *   --dry-run          Simulate without sending transactions
 */

const { createWalletClient, createPublicClient, http, namehash, parseGwei } = require('viem');
const { mainnet } = require('viem/chains');
const { privateKeyToAccount } = require('viem/accounts');
const { readFileSync } = require('fs');
const { createDecipheriv, scryptSync } = require('crypto');
const contentHash = require('content-hash');

// ENS Contract Addresses (mainnet)
const ENS_REGISTRY = '0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e';
const NAME_WRAPPER = '0xD4416b13d2b3a9aBae7AcD5D6C2BbDBE25686401';
const PUBLIC_RESOLVER = '0x231b0Ee14048e9dCcD1d247744d114a4EB5E8E63';

// Parse command line arguments
function parseArgs() {
  const args = process.argv.slice(2);
  if (args.length < 3) {
    console.error('Usage: node create-subdomain-ipfs.js <parent-name> <label> <ipfs-cid> [options]');
    process.exit(1);
  }

  const [parentName, label, ipfsCid] = args;
  const options = {
    parentName,
    label,
    ipfsCid,
    keystorePath: null,
    password: null,
    rpcUrl: 'https://ethereum-rpc.publicnode.com',
    dryRun: false
  };

  for (let i = 3; i < args.length; i++) {
    if (args[i] === '--keystore' && args[i + 1]) {
      options.keystorePath = args[++i];
    } else if (args[i] === '--password' && args[i + 1]) {
      options.password = args[++i];
    } else if (args[i] === '--rpc' && args[i + 1]) {
      options.rpcUrl = args[++i];
    } else if (args[i] === '--dry-run') {
      options.dryRun = true;
    }
  }

  return options;
}

// Decrypt keystore
function decrypt(encrypted, password) {
  const { salt, iv, data } = JSON.parse(encrypted);
  const key = scryptSync(password, Buffer.from(salt, 'hex'), 32);
  const decipher = createDecipheriv('aes-256-cbc', key, Buffer.from(iv, 'hex'));
  return Buffer.concat([
    decipher.update(Buffer.from(data, 'hex')),
    decipher.final()
  ]).toString('utf8');
}

// Check if name is wrapped
async function isNameWrapped(parentName, publicClient) {
  const node = namehash(parentName);
  const registryOwner = await publicClient.readContract({
    address: ENS_REGISTRY,
    abi: [{
      name: 'owner',
      type: 'function',
      stateMutability: 'view',
      inputs: [{ name: 'node', type: 'bytes32' }],
      outputs: [{ name: '', type: 'address' }]
    }],
    functionName: 'owner',
    args: [node]
  });
  
  return registryOwner.toLowerCase() === NAME_WRAPPER.toLowerCase();
}

async function main() {
  const options = parseArgs();
  
  console.log('🏷️  ENS Subdomain Creator with IPFS');
  console.log('═'.repeat(50));
  console.log(`Parent: ${options.parentName}`);
  console.log(`Label: ${options.label}`);
  console.log(`Subdomain: ${options.label}.${options.parentName}`);
  console.log(`IPFS CID: ${options.ipfsCid}`);
  console.log();

  // Load wallet
  if (!options.keystorePath || !options.password) {
    console.error('❌ Error: --keystore and --password required');
    process.exit(1);
  }

  const encrypted = readFileSync(options.keystorePath, 'utf8');
  const privateKey = decrypt(encrypted, options.password);
  const account = privateKeyToAccount(privateKey);
  console.log(`📍 Wallet: ${account.address}`);

  // Setup clients
  const publicClient = createPublicClient({
    chain: mainnet,
    transport: http(options.rpcUrl, { timeout: 60_000, batch: false })
  });

  const walletClient = createWalletClient({
    account,
    chain: mainnet,
    transport: http(options.rpcUrl, { timeout: 60_000, batch: false })
  });

  // Check if parent is wrapped
  console.log('\n🔍 Checking parent name...');
  const isWrapped = await isNameWrapped(options.parentName, publicClient);
  console.log(`   ${isWrapped ? 'Wrapped (NameWrapper)' : 'Unwrapped (Registry)'}`);

  // Get gas price
  const block = await publicClient.getBlock({ blockTag: 'latest' });
  const maxFeePerGas = block.baseFeePerGas * 2n;
  const maxPriorityFeePerGas = parseGwei('0.1');
  console.log(`   Base fee: ${Number(block.baseFeePerGas) / 1e9} gwei`);

  const parentNode = namehash(options.parentName);
  const subnode = namehash(`${options.label}.${options.parentName}`);

  // Step 1: Create subdomain
  console.log('\n📝 Step 1/2: Creating subdomain...');
  
  if (options.dryRun) {
    console.log('   [DRY RUN] Would create subdomain');
  } else {
    if (isWrapped) {
      // Use NameWrapper.setSubnodeRecord
      const tx1 = await walletClient.writeContract({
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
        args: [parentNode, options.label, account.address, PUBLIC_RESOLVER, 0n, 0, 0n],
        maxFeePerGas,
        maxPriorityFeePerGas,
        gas: 200000n
      });
      
      console.log(`   TX: ${tx1}`);
      console.log(`   https://etherscan.io/tx/${tx1}`);
    } else {
      // Use Registry.setSubnodeOwner + setResolver
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
        args: [parentNode, keccak256(encodePacked(['string'], [options.label])), account.address],
        maxFeePerGas,
        maxPriorityFeePerGas,
        gas: 100000n
      });
      
      console.log(`   TX: ${tx1}`);
      console.log(`   https://etherscan.io/tx/${tx1}`);
      
      console.log('   Waiting 20s for confirmation...');
      await new Promise(r => setTimeout(r, 20000));
      
      // Set resolver
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
        args: [subnode, PUBLIC_RESOLVER],
        maxFeePerGas,
        maxPriorityFeePerGas,
        gas: 100000n
      });
      
      console.log(`   TX: ${tx2}`);
      console.log(`   https://etherscan.io/tx/${tx2}`);
    }
  }

  console.log('   Waiting 30s for TX to be mined...');
  await new Promise(r => setTimeout(r, 30000));

  // Step 2: Set IPFS content hash
  console.log('\n📝 Step 2/2: Setting IPFS content hash...');
  
  const encodedHash = '0x' + contentHash.encode('ipfs-ns', options.ipfsCid);
  console.log(`   Encoded: ${encodedHash.slice(0, 20)}...`);

  if (options.dryRun) {
    console.log('   [DRY RUN] Would set content hash');
  } else {
    const tx3 = await walletClient.writeContract({
      address: PUBLIC_RESOLVER,
      abi: [{
        name: 'setContenthash',
        type: 'function',
        stateMutability: 'nonpayable',
        inputs: [
          { name: 'node', type: 'bytes32' },
          { name: 'hash', type: 'bytes' }
        ],
        outputs: []
      }],
      functionName: 'setContenthash',
      args: [subnode, encodedHash],
      maxFeePerGas,
      maxPriorityFeePerGas,
      gas: 100000n
    });
    
    console.log(`   TX: ${tx3}`);
    console.log(`   https://etherscan.io/tx/${tx3}`);
  }

  console.log('\n✅ Done! Subdomain created and IPFS content hash set.');
  console.log('\n🌐 Access at:');
  console.log(`   https://${options.label}.${options.parentName}.limo`);
  console.log(`   https://${options.label}.${options.parentName}.link`);
  console.log(`\n📦 IPFS gateways:`);
  console.log(`   https://ipfs.io/ipfs/${options.ipfsCid}`);
  console.log(`   https://${options.ipfsCid}.ipfs.dweb.link/`);
}

main().catch(error => {
  console.error('\n❌ Error:', error.shortMessage || error.message);
  process.exit(1);
});
