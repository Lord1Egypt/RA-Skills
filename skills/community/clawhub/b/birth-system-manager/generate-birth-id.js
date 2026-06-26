#!/usr/bin/env node

/**
 * OpenClaw Birth System
 * Global Unique Birth ID System for OpenClaw Instances
 */

const ethers = require('ethers');
const fs = require('fs');
const path = require('path');

// Configuration
const BIRTH_INFO_PATH = process.env.OPENCLAW_CONFIG_PATH || path.join(process.env.HOME, '.openclaw', 'birth-info.json');
const IS_CLONE = process.env.IS_CLONE === 'true';

/**
 * Generate a Birth ID using Ethereum-based DID
 * @param {boolean} isClone - Whether this instance is a clone
 * @param {string|null} parentId - Parent birth ID if this is a clone
 * @returns {Object} Birth system data
 */
async function generateBirthId(isClone = false, parentId = null) {
  // Generate wallet
  const wallet = ethers.Wallet.createRandom();
  const did = `did:ethr:${wallet.address}`;
  
  const now = Date.now();
  let fullId = did;
  let cloneSuffix = null;
  
  if (isClone) {
    cloneSuffix = `-clone-${now}`;
    fullId += cloneSuffix;
  }
  
  // Create signature to prevent tampering
  const message = `BirthID:${fullId}|Created:${now}|Parent:${parentId || 'none'}`;
  const signature = await wallet.signMessage(message);
  
  return {
    birth_id: fullId,
    parent_id: parentId,
    clone_suffix: cloneSuffix,
    created_at: now,
    signature: signature,
    wallet_address: wallet.address,
    public_key: wallet.publicKey,
    // Store private key for verification (in production, this should be encrypted)
    private_key: wallet.privateKey
  };
}

/**
 * Load birth info
 */
function loadBirthInfo() {
  try {
    const birthInfoContent = fs.readFileSync(BIRTH_INFO_PATH, 'utf8');
    return JSON.parse(birthInfoContent);
  } catch (error) {
    throw new Error(`Failed to load birth info from ${BIRTH_INFO_PATH}: ${error.message}`);
  }
}

/**
 * Save birth info
 */
function saveBirthInfo(birthData) {
  fs.writeFileSync(BIRTH_INFO_PATH, JSON.stringify(birthData, null, 2));
}

/**
 * Verify birth signature
 */
function verifyBirthSignature(birthData) {
  try {
    const message = `BirthID:${birthData.birth_id}|Created:${birthData.created_at}|Parent:${birthData.parent_id || 'none'}`;
    const recoveredAddress = ethers.verifyMessage(message, birthData.signature);
    return recoveredAddress === birthData.wallet_address;
  } catch (error) {
    console.error('Signature verification failed:', error.message);
    return false;
  }
}

/**
 * Main function
 */
async function main() {
  console.log('🔮 OpenClaw Birth System');
  console.log('=================================\n');

  // Load birth info
  console.log(`📂 Loading birth info from: ${BIRTH_INFO_PATH}`);
  let birthData = loadBirthInfo();

  // Check if birth_id already exists
  if (!birthData.birth_id) {
    // New instance - generate birth ID
    console.log('🌱 New instance detected. Generating Birth ID...');
    const newBirthData = await generateBirthId(false, null);
    saveBirthInfo(newBirthData);

    console.log(`✅ Birth ID generated: ${newBirthData.birth_id}`);
    console.log(`   Wallet: ${newBirthData.wallet_address}`);
    console.log(`   Created: ${new Date(newBirthData.created_at).toISOString()}`);
  } else {
    console.log(`🔍 Existing Birth ID found: ${birthData.birth_id}`);

    // Verify signature
    const isValid = verifyBirthSignature(birthData);
    if (!isValid) {
      console.error('❌ WARNING: Birth signature is invalid! Data may be tampered.');
      process.exit(1);
    }
    console.log('✅ Birth signature verified.');

    // Check if clone
    if (IS_CLONE) {
      console.log('🧬 Clone detected. Generating new Birth ID...');
      const originalId = birthData.birth_id;
      const newBirthData = await generateBirthId(true, originalId);
      saveBirthInfo(newBirthData);

      console.log(`✅ Clone Birth ID generated: ${newBirthData.birth_id}`);
      console.log(`   Cloned from: ${originalId}`);
      console.log(`   Wallet: ${newBirthData.wallet_address}`);
    } else {
      console.log(`🔑 Parent ID: ${birthData.parent_id || 'None (original instance)'}`);
      console.log(`   Wallet: ${birthData.wallet_address}`);
    }
  }
  
  // Update SOUL.md
  try {
    const soulPath = path.join(process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw', 'workspace'), 'SOUL.md');
    if (fs.existsSync(soulPath)) {
      const soulContent = fs.readFileSync(soulPath, 'utf8');
      if (!soulContent.includes('Birth System:')) {
        fs.appendFileSync(soulPath, '\n\nBirth System: Initialized\n');
        console.log(`✅ Updated ${soulPath}`);
      }
    }
  } catch (error) {
    console.warn(`⚠️  Could not update SOUL.md: ${error.message}`);
  }
  
  console.log('\n✨ Birth System setup complete!');
}

// Run main
if (require.main === module) {
  main().catch(error => {
    console.error('❌ Error:', error.message);
    process.exit(1);
  });
}

module.exports = {
  generateBirthId,
  verifyBirthSignature,
  loadBirthInfo,
  saveBirthInfo
};
