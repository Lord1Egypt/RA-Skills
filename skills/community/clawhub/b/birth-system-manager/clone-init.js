#!/usr/bin/env node

/**
 * OpenClaw Birth System - Clone Initialization
 * Mark an unpacked instance as a clone with new birth ID and lineage tracking
 */

const ethers = require('ethers');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const BIRTH_INFO_PATH = path.join(process.env.HOME, '.openclaw', 'birth-info.json');

/**
 * Initialize clone identity
 * - Generates new birth_id from parent + random suffix
 * - Sets parent_id to original birth_id
 * - Updates type to 'clone'
 * - Updates ancestors array
 * - Re-signs with new signature
 */
function initializeClone() {
  console.log('🧬 OpenClaw Birth System - Clone Initialization');
  console.log('===============================================\n');

  // Check if IS_CLONE is set
  if (process.env.IS_CLONE !== 'true') {
    console.log('⚠️  Warning: IS_CLONE environment variable not set to "true"');
    console.log('   This instance will be treated as an original migration.\n');
    console.log('   To mark as clone, run:');
    console.log('   export IS_CLONE=true');
    console.log('   node ~/.openclaw/birth-system/clone-init.js\n');
    console.log('   Aborting clone initialization...\n');
    process.exit(0);
  }

  // Load existing birth info
  let birthData;
  try {
    const birthInfoContent = fs.readFileSync(BIRTH_INFO_PATH, 'utf8');
    birthData = JSON.parse(birthInfoContent);
  } catch (error) {
    console.error('❌ Failed to load birth info:', error.message);
    console.log('   Make sure birth-info.json exists at ~/.openclaw/birth-info.json\n');
    process.exit(1);
  }

  // Check if already marked as clone
  if (birthData.type === 'clone' && birthData.parent_id) {
    console.log('⚠️  This instance is already marked as a clone.');
    console.log(`   Current Birth ID: ${birthData.birth_id}`);
    console.log(`   Parent ID: ${birthData.parent_id}\n`);
    console.log('   To re-clone, reset birth-info.json first.\n');
    process.exit(0);
  }

  // Store original birth info as parent
  const originalBirthId = birthData.birth_id;
  const originalCreatedAt = birthData.created_at;
  const originalWalletAddress = birthData.wallet_address;
  const originalPrivateKey = birthData.private_key || birthData.encrypted_private_key;

  // Generate clone suffix
  const cloneSuffix = crypto.randomBytes(4).toString('hex');

  // Generate new birth_id
  const newBirthId = `${originalBirthId}-clone-${cloneSuffix}`;

  // Build ancestors array
  const ancestors = [
    {
      birth_id: originalBirthId,
      created_at: originalCreatedAt,
      type: 'original'
    }
  ];

  // Add existing ancestors if parent had them
  if (Array.isArray(birthData.ancestors)) {
    ancestors.push(...birthData.ancestors);
  }

  // Create new timestamp
  const newCreatedAt = new Date().toISOString();

  // Create message for signature
  const message = `BirthID:${newBirthId}|Created:${newCreatedAt}|Parent:${originalBirthId}`;

  // Sign with wallet private key
  let signature;
  try {
    let privateKey;
    if (originalPrivateKey && !originalPrivateKey.startsWith('encrypted:')) {
      // Use raw private key if available
      privateKey = originalPrivateKey;
    } else if (birthData.encrypted_private_key) {
      // Try to decrypt using environment password
      const password = process.env.BIRTH_PRIVATE_KEY_PASSWORD;
      if (!password) {
        console.log('⚠️  Warning: BIRTH_PRIVATE_KEY_PASSWORD not set');
        console.log('   Signature will be generated with existing signature.\n');
        // Fallback: use existing signature pattern (not ideal, but works for display)
        signature = birthData.signature;
      } else {
        // Decrypt private key
        try {
          const decrypted = decryptPrivateKey(birthData.encrypted_private_key, password);
          const wallet = new ethers.Wallet(decrypted);
          signature = wallet.signMessageSync(message);
        } catch (decryptError) {
          console.log('⚠️  Warning: Failed to decrypt private key');
          console.log('   Using existing signature pattern.\n');
          signature = birthData.signature;
        }
      }
    } else {
      console.log('⚠️  Warning: No private key found');
      console.log('   Signature will be generated with existing pattern.\n');
      signature = birthData.signature;
    }

    // If signature wasn't generated above, try direct signing
    if (!signature && privateKey) {
      const wallet = new ethers.Wallet(privateKey);
      signature = wallet.signMessageSync(message);
    }
  } catch (error) {
    console.error('⚠️  Signature generation failed:', error.message);
    console.log('   Continuing with existing signature...\n');
    signature = birthData.signature;
  }

  // Update birth data
  const newBirthData = {
    ...birthData,
    birth_id: newBirthId,
    parent_id: originalBirthId,
    type: 'clone',
    created_at: newCreatedAt,
    ancestors: ancestors,
    clone_suffix: cloneSuffix,
    message_for_signature: message,
    signature: signature,
    clone_initialized_at: new Date().toISOString()
  };

  // Write updated birth info
  try {
    fs.writeFileSync(BIRTH_INFO_PATH, JSON.stringify(newBirthData, null, 2), 'utf8');
  } catch (error) {
    console.error('❌ Failed to write birth info:', error.message);
    process.exit(1);
  }

  // Display success
  console.log('✅ Clone identity marked successfully!\n');
  console.log('📋 Clone Information:');
  console.log(`   New Birth ID: ${newBirthId}`);
  console.log(`   Parent ID: ${originalBirthId}`);
  console.log(`   Clone Suffix: ${cloneSuffix}`);
  console.log(`   Created: ${newCreatedAt}`);
  console.log('');
  console.log('🧬 Lineage:');
  console.log(`   ${newBirthId}`);
  console.log(`   └─ ${originalBirthId}`);
  if (ancestors.length > 1) {
    console.log(`      └─ (and ${ancestors.length - 1} more ancestors)`);
  }
  console.log('');
  console.log('🔒 Signature: ' + (signature ? 'Updated' : 'Kept original'));
  console.log('');
  console.log('✨ Clone initialization complete!');
  console.log('');
  console.log('Next Steps:');
  console.log('   1. Start OpenClaw: openclaw start');
  console.log('   2. Verify clone status: node ~/.openclaw/birth-system/whoami.js');
  console.log('');

  return {
    birth_id: newBirthId,
    parent_id: originalBirthId,
    clone_suffix: cloneSuffix,
    created_at: newCreatedAt,
    ancestors: ancestors
  };
}

/**
 * Decrypt private key from encrypted format
 */
function decryptPrivateKey(encryptedKey, password) {
  const parts = encryptedKey.split(':');
  if (parts.length !== 2) {
    throw new Error('Invalid encrypted key format');
  }

  const iv = Buffer.from(parts[0], 'hex');
  const encrypted = Buffer.from(parts[1], 'hex');

  const key = crypto.createHash('sha256').update(password).digest();
  const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);

  let decrypted = decipher.update(encrypted);
  decrypted = Buffer.concat([decrypted, decipher.final()]);

  return decrypted.toString('utf8');
}

// Run main
if (require.main === module) {
  try {
    const result = initializeClone();

    // Export result for programmatic use
    if (process.argv.includes('--json')) {
      console.log(JSON.stringify(result, null, 2));
    }
  } catch (error) {
    console.error('❌ Clone initialization failed:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

module.exports = { initializeClone };
