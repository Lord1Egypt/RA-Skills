#!/usr/bin/env node
/**
 * ENS Name Checker
 * 
 * Checks ENS name ownership, resolver, and content hash status.
 * 
 * Usage:
 *   node check-ens-name.js <ens-name> [--rpc URL]
 * 
 * Example:
 *   node check-ens-name.js clophorse.eth
 *   node check-ens-name.js meetup.clophorse.eth
 */

const { createPublicClient, http, namehash } = require('viem');
const { mainnet } = require('viem/chains');
const contentHash = require('content-hash');

const ENS_REGISTRY = '0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e';
const NAME_WRAPPER = '0xD4416b13d2b3a9aBae7AcD5D6C2BbDBE25686401';

function parseArgs() {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.error('Usage: node check-ens-name.js <ens-name> [--rpc URL]');
    process.exit(1);
  }

  const ensName = args[0];
  let rpcUrl = 'https://ethereum-rpc.publicnode.com';

  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--rpc' && args[i + 1]) {
      rpcUrl = args[++i];
    }
  }

  return { ensName, rpcUrl };
}

async function main() {
  const { ensName, rpcUrl } = parseArgs();

  console.log('🔍 ENS Name Checker');
  console.log('═'.repeat(50));
  console.log(`Name: ${ensName}\n`);

  const publicClient = createPublicClient({
    chain: mainnet,
    transport: http(rpcUrl, { timeout: 30_000 })
  });

  const node = namehash(ensName);

  // Check registry owner
  console.log('📋 Registry Information:');
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

  console.log(`   Owner: ${registryOwner}`);
  
  const isWrapped = registryOwner.toLowerCase() === NAME_WRAPPER.toLowerCase();
  console.log(`   Status: ${isWrapped ? '🎁 Wrapped (NameWrapper)' : '📦 Unwrapped (Registry)'}`);

  // If wrapped, check NameWrapper owner
  if (isWrapped) {
    const wrapperOwner = await publicClient.readContract({
      address: NAME_WRAPPER,
      abi: [{
        name: 'ownerOf',
        type: 'function',
        stateMutability: 'view',
        inputs: [{ name: 'id', type: 'uint256' }],
        outputs: [{ name: '', type: 'address' }]
      }],
      functionName: 'ownerOf',
      args: [BigInt(node)]
    });
    console.log(`   NameWrapper Owner: ${wrapperOwner}`);
  }

  // Check resolver
  console.log('\n🔧 Resolver Information:');
  const resolver = await publicClient.readContract({
    address: ENS_REGISTRY,
    abi: [{
      name: 'resolver',
      type: 'function',
      stateMutability: 'view',
      inputs: [{ name: 'node', type: 'bytes32' }],
      outputs: [{ name: '', type: 'address' }]
    }],
    functionName: 'resolver',
    args: [node]
  });

  console.log(`   Resolver: ${resolver}`);

  if (resolver === '0x0000000000000000000000000000000000000000') {
    console.log('   ⚠️  No resolver set');
  } else {
    // Try to get content hash
    try {
      const contenthash = await publicClient.readContract({
        address: resolver,
        abi: [{
          name: 'contenthash',
          type: 'function',
          stateMutability: 'view',
          inputs: [{ name: 'node', type: 'bytes32' }],
          outputs: [{ name: '', type: 'bytes' }]
        }],
        functionName: 'contenthash',
        args: [node]
      });

      if (contenthash && contenthash !== '0x') {
        const decoded = contentHash.decode(contenthash);
        console.log(`\n📦 Content Hash:`);
        console.log(`   ${decoded}`);
        console.log(`\n🌐 Access at:`);
        console.log(`   https://${ensName}.limo`);
        console.log(`   https://${ensName}.link`);
        console.log(`\n📦 IPFS Gateway:`);
        console.log(`   https://ipfs.io/ipfs/${decoded}`);
      } else {
        console.log('   📭 No content hash set');
      }
    } catch (e) {
      console.log('   ⚠️  Could not read content hash');
    }

    // Try to get address
    try {
      const address = await publicClient.readContract({
        address: resolver,
        abi: [{
          name: 'addr',
          type: 'function',
          stateMutability: 'view',
          inputs: [{ name: 'node', type: 'bytes32' }],
          outputs: [{ name: '', type: 'address' }]
        }],
        functionName: 'addr',
        args: [node]
      });

      if (address && address !== '0x0000000000000000000000000000000000000000') {
        console.log(`\n💼 ETH Address:`);
        console.log(`   ${address}`);
      }
    } catch (e) {
      // Resolver doesn't support addr
    }
  }

  console.log();
}

main().catch(error => {
  console.error('\n❌ Error:', error.message);
  process.exit(1);
});
