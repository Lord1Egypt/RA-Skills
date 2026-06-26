#!/usr/bin/env node

/**
 * Quick test script to verify installation
 */

const path = require('path');

// Load configuration
let config;
try {
  config = require(path.join(__dirname, '../config/keys.js'));
} catch (error) {
  console.error('⚠️  config/keys.js not found. Using example config.');
  try {
    config = require(path.join(__dirname, '../config/keys.example.js'));
  } catch (fallbackError) {
    console.error('❌ No configuration files found!');
    process.exit(1);
  }
}

console.log('✓ Configuration loaded');

// Import DefiLlama client (the only platform currently implemented)
const DefiLlamaClient = require('../src/platforms/defillama');

console.log('✓ DefiLlama client imported');

// Test initialization
const defillama = new DefiLlamaClient(config);

console.log('✓ DefiLlama client initialized');
console.log('');

// Quick health check
async function runTests() {
  try {
    console.log('Testing DefiLlama API connection...');
    const tvl = await defillama.getTotalTvl();
    console.log(`✓ TVL fetched: $${(tvl.totalTvl / 1e9).toFixed(2)}B`);
    
    console.log('');
    console.log('✅ Installation verified successfully!');
    console.log('');
    console.log('You can now use the defillama-data CLI:');
    console.log('  node src/index.js --help');
    console.log('  node src/index.js defillama tvl');
    console.log('  node src/index.js defillama protocols --limit 10');
    console.log('');
  } catch (error) {
    console.error('❌ Test failed:', error.message);
    process.exit(1);
  }
}

runTests();
