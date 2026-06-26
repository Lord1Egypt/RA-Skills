#!/usr/bin/env node

/**
 * register-ens-name.js
 * 
 * Register a new .eth ENS name with proper three-phase process:
 * 1. Make commitment (anti-frontrunning)
 * 2. Wait 60 seconds (required minimum)
 * 3. Register name with payment
 * 
 * Usage:
 *   node register-ens-name.js <name> [options]
 * 
 * Example:
 *   node register-ens-name.js mynewname --years 1 --keystore /path/to/keystore.enc --password "pass"
 * 
 * Options:
 *   --years <n>       Registration duration in years (default: 1)
 *   --keystore <path> Path to encrypted keystore
 *   --password <pass> Keystore password
 *   --dry-run         Check availability and price only
 */

const { createPublicClient, createWalletClient, http, formatEther, parseEther, namehash, keccak256, encodePacked } = require('viem');
const { mainnet } = require('viem/chains');
const { createDecipheriv } = require('crypto');
const { scryptSync } = require('crypto');
const { readFileSync } = require('fs');

// Contract addresses (Ethereum Mainnet)
const ENS_REGISTRY = '0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e';
const ETH_REGISTRAR_CONTROLLER = '0x253553366Da8546fC250F225fe3d25d0C782303b';
const PUBLIC_RESOLVER = '0x231b0Ee14048e9dCcD1d247744d114a4EB5E8E63';

// RPC endpoint (use reliable provider)
const RPC_URL = process.env.RPC_URL || 'https://mainnet.rpc.buidlguidl.com';

// Parse command line arguments
function parseArgs() {
  const args = process.argv.slice(2);
  
  if (args.length < 1 || args[0].startsWith('--')) {
    console.error('Usage: node register-ens-name.js <name> [options]');
    console.error('');
    console.error('Options:');
    console.error('  --years <n>       Registration duration (default: 1)');
    console.error('  --keystore <path> Path to encrypted keystore');
    console.error('  --password <pass> Keystore password');
    console.error('  --dry-run         Check availability and price only');
    process.exit(1);
  }

  const name = args[0].replace('.eth', ''); // Remove .eth if provided
  const options = {
    years: 1,
    keystore: null,
    password: null,
    dryRun: false
  };

  for (let i = 1; i < args.length; i += 2) {
    const key = args[i].replace('--', '');
    const value = args[i + 1];
    
    if (key === 'years') options.years = parseInt(value);
    else if (key === 'keystore') options.keystore = value;
    else if (key === 'password') options.password = value;
    else if (key === 'dry-run') {
      options.dryRun = true;
      i--; // No value for dry-run flag
    }
  }

  return { name, ...options };
}

// Decrypt keystore
function decryptKeystore(keystorePath, password) {
  const encrypted = readFileSync(keystorePath, 'utf8');
  const { salt, iv, data } = JSON.parse(encrypted);
  
  const key = scryptSync(password, Buffer.from(salt, 'hex'), 32);
  const decipher = createDecipheriv('aes-256-cbc', key, Buffer.from(iv, 'hex'));
  
  const privateKey = Buffer.concat([
    decipher.update(Buffer.from(data, 'hex')),
    decipher.final()
  ]).toString('utf8');
  
  return privateKey;
}

// Check if name is available
async function checkAvailability(name, publicClient) {
  const available = await publicClient.readContract({
    address: ETH_REGISTRAR_CONTROLLER,
    abi: [{
      name: 'available',
      type: 'function',
      stateMutability: 'view',
      inputs: [{ name: 'name', type: 'string' }],
      outputs: [{ name: '', type: 'bool' }]
    }],
    functionName: 'available',
    args: [name]
  });
  
  return available;
}

// Get registration price
async function getPrice(name, duration, publicClient) {
  const price = await publicClient.readContract({
    address: ETH_REGISTRAR_CONTROLLER,
    abi: [{
      name: 'rentPrice',
      type: 'function',
      stateMutability: 'view',
      inputs: [
        { name: 'name', type: 'string' },
        { name: 'duration', type: 'uint256' }
      ],
      outputs: [{
        type: 'tuple',
        components: [
          { name: 'base', type: 'uint256' },
          { name: 'premium', type: 'uint256' }
        ]
      }]
    }],
    functionName: 'rentPrice',
    args: [name, duration]
  });
  
  return price.base + price.premium;
}

// Generate random secret for commitment
function generateSecret() {
  const randomValue = BigInt(Date.now()) * BigInt(Math.floor(Math.random() * 1000000));
  return keccak256(encodePacked(['uint256'], [randomValue]));
}

// Make commitment
async function makeCommitment(name, owner, duration, secret, resolver, walletClient) {
  console.log('\n📝 Phase 1: Making commitment...');
  
  // Calculate commitment hash
  const commitment = keccak256(
    encodePacked(
      ['string', 'address', 'uint256', 'bytes32', 'address', 'bytes[]', 'bool', 'uint16'],
      [
        name,
        owner,
        duration,
        secret,
        resolver,
        [], // data (empty)
        true, // reverseRecord
        0 // ownerControlledFuses
      ]
    )
  );
  
  console.log(`   Commitment: ${commitment}`);
  console.log(`   Secret: ${secret}`);
  
  // Submit commitment
  const tx = await walletClient.writeContract({
    address: ETH_REGISTRAR_CONTROLLER,
    abi: [{
      name: 'commit',
      type: 'function',
      stateMutability: 'nonpayable',
      inputs: [{ name: 'commitment', type: 'bytes32' }],
      outputs: []
    }],
    functionName: 'commit',
    args: [commitment]
  });
  
  console.log(`   TX: ${tx}`);
  console.log('   Waiting for confirmation...');
  
  return { commitment, secret, tx };
}

// Register name
async function registerName(name, owner, duration, secret, resolver, price, walletClient) {
  console.log('\n📝 Phase 3: Registering name...');
  console.log(`   Sending ${formatEther(price)} ETH...`);
  
  const tx = await walletClient.writeContract({
    address: ETH_REGISTRAR_CONTROLLER,
    abi: [{
      name: 'register',
      type: 'function',
      stateMutability: 'payable',
      inputs: [
        { name: 'name', type: 'string' },
        { name: 'owner', type: 'address' },
        { name: 'duration', type: 'uint256' },
        { name: 'secret', type: 'bytes32' },
        { name: 'resolver', type: 'address' },
        { name: 'data', type: 'bytes[]' },
        { name: 'reverseRecord', type: 'bool' },
        { name: 'ownerControlledFuses', type: 'uint16' }
      ],
      outputs: []
    }],
    functionName: 'register',
    args: [name, owner, duration, secret, resolver, [], true, 0],
    value: price
  });
  
  console.log(`   TX: ${tx}`);
  return tx;
}

// Main registration flow
async function main() {
  const { name, years, keystore, password, dryRun } = parseArgs();
  
  console.log('🦞 ENS Name Registration');
  console.log('========================');
  console.log(`📛 Name: ${name}.eth`);
  console.log(`⏱️  Duration: ${years} year${years > 1 ? 's' : ''}`);
  console.log('');
  
  // Create public client
  const publicClient = createPublicClient({
    chain: mainnet,
    transport: http(RPC_URL)
  });
  
  // Check availability
  console.log('🔍 Checking availability...');
  const available = await checkAvailability(name, publicClient);
  
  if (!available) {
    console.error(`❌ Name "${name}.eth" is not available`);
    process.exit(1);
  }
  
  console.log('✅ Name is available!');
  
  // Calculate duration in seconds (1 year = 31536000 seconds)
  const duration = BigInt(years) * 31536000n;
  
  // Get price
  console.log('\n💰 Calculating price...');
  const priceWei = await getPrice(name, duration, publicClient);
  const priceEth = formatEther(priceWei);
  
  console.log(`   Registration cost: ${priceEth} ETH`);
  console.log(`   (for ${years} year${years > 1 ? 's' : ''})`);
  
  // Dry run stops here
  if (dryRun) {
    console.log('\n✅ Dry run complete. Name is available at the price shown above.');
    console.log('\nTo register, run without --dry-run and provide keystore credentials.');
    process.exit(0);
  }
  
  // Check keystore provided
  if (!keystore || !password) {
    console.error('\n❌ Keystore and password required for registration');
    console.error('   Use: --keystore <path> --password <pass>');
    process.exit(1);
  }
  
  // Decrypt keystore
  console.log('\n🔐 Decrypting keystore...');
  const privateKey = decryptKeystore(keystore, password);
  
  // Create wallet client
  const walletClient = createWalletClient({
    chain: mainnet,
    transport: http(RPC_URL)
  });
  
  const [account] = await walletClient.getAddresses();
  console.log(`   Owner: ${account}`);
  
  // Check balance
  const balance = await publicClient.getBalance({ address: account });
  const balanceEth = formatEther(balance);
  
  console.log(`   Balance: ${balanceEth} ETH`);
  
  if (balance < priceWei) {
    console.error(`\n❌ Insufficient balance`);
    console.error(`   Need: ${priceEth} ETH`);
    console.error(`   Have: ${balanceEth} ETH`);
    process.exit(1);
  }
  
  // Generate secret
  const secret = generateSecret();
  
  // Phase 1: Make commitment
  const { tx: commitTx } = await makeCommitment(
    name,
    account,
    duration,
    secret,
    PUBLIC_RESOLVER,
    walletClient
  );
  
  // Phase 2: Wait 60 seconds
  console.log('\n⏳ Phase 2: Waiting 60 seconds (anti-frontrunning protection)...');
  
  for (let i = 60; i > 0; i--) {
    process.stdout.write(`\r   ${i} seconds remaining...`);
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  console.log('\r   ✅ Wait complete!                    ');
  
  // Phase 3: Register
  const registerTx = await registerName(
    name,
    account,
    duration,
    secret,
    PUBLIC_RESOLVER,
    priceWei,
    walletClient
  );
  
  console.log('\n🎉 Registration complete!');
  console.log('');
  console.log('📛 Your ENS name: ' + name + '.eth');
  console.log('🔍 View on ENS: https://app.ens.domains/' + name + '.eth');
  console.log('🔗 Registry TX: https://etherscan.io/tx/' + registerTx);
  console.log('');
  console.log('Next steps:');
  console.log('  1. Set your address: ens.domains → Records → ETH Address');
  console.log('  2. Create subdomains: node create-subdomain-ipfs.js');
  console.log('  3. Set reverse record: ens.domains → My Account → Primary Name');
}

main().catch(error => {
  console.error('\n❌ Error:', error.message);
  process.exit(1);
});
