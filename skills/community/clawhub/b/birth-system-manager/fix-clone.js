#!/usr/bin/env node

/**
 * OpenClaw Birth System - Fix Clone Identity
 * Manually mark an instance as clone by specifying parent_id
 * Use this when clone-init was not run after unpacking
 */

const ethers = require('ethers');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const BIRTH_INFO_PATH = path.join(process.env.HOME, '.openclaw', 'birth-info.json');

/**
 * Fix clone identity by manually specifying parent_id
 */
function fixCloneIdentity(parentBirthId, options = {}) {
  console.log('🔧 OpenClaw Birth System - Fix Clone Identity');
  console.log('==============================================\n');

  if (!parentBirthId) {
    console.error('❌ Missing required argument: parent_birth_id');
    console.log('\nUsage:');
    console.log('  node fix-clone.js <parent_birth_id> [--force]');
    console.log('\nOptions:');
    console.log('  --force    Skip confirmation if already a clone');
    console.log('\nExample:');
    console.log('  node fix-clone.js did:ethr:0xF80042413226cf4a5F1b7de458Cf0EEd19237662');
    console.log('\nTo find parent_id from a package:');
    console.log('  tar -xzf birth-pack-xxx.tar.gz ./.openclaw/birth-info.json');
    console.log('  cat .openclaw/birth-info.json | grep birth_id\n');
    process.exit(1);
  }

  // Load current birth info
  let birthData;
  try {
    const birthInfoContent = fs.readFileSync(BIRTH_INFO_PATH, 'utf8');
    birthData = JSON.parse(birthInfoContent);
  } catch (error) {
    console.error('❌ Failed to load birth info:', error.message);
    process.exit(1);
  }

  // Check if already a clone
  if (birthData.type === 'clone' && !options.force) {
    console.log('⚠️  This instance is already marked as a clone.');
    console.log(`   Current Birth ID: ${birthData.birth_id}`);
    console.log(`   Current Parent ID: ${birthData.parent_id}`);
    console.log(`   New Parent ID: ${parentBirthId}`);
    console.log('');
    console.log('   To proceed anyway, use --force flag.\n');
    process.exit(0);
  }

  // Store original info
  const originalBirthId = birthData.birth_id;
  const originalCreatedAt = birthData.created_at;
  const originalWalletAddress = birthData.wallet_address;
  const originalPrivateKey = birthData.private_key || birthData.encrypted_private_key;

  // Confirm if not already a clone
  if (birthData.type !== 'clone' && !options.force && !options.auto) {
    console.log('⚠️  You are about to mark this instance as a clone.');
    console.log(`   Current Birth ID: ${originalBirthId}`);
    console.log(`   New Parent ID: ${parentBirthId}`);
    console.log('');
    console.log('   This will generate a new Birth ID and update the type to "clone".');
    console.log('');
    console.log('   Press Enter to continue, or Ctrl+C to cancel...');
    
    // Simple prompt for node CLI
    if (process.stdin.isTTY) {
      const readline = require('readline');
      const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
      rl.question('', () => {
        rl.close();
        proceedWithFix();
      });
    } else {
      proceedWithFix();
    }
  } else {
    proceedWithFix();
  }

  function proceedWithFix() {
    // Generate clone suffix
    const cloneSuffix = crypto.randomBytes(4).toString('hex');

    // Generate new birth_id
    const newBirthId = `${originalBirthId}-clone-${cloneSuffix}`;

    // Build ancestors array
    const ancestors = [
      {
        birth_id: parentBirthId,
        created_at: new Date(originalCreatedAt || Date.now()).toISOString(),
        type: 'clone'  // Parent might be a clone itself
      }
    ];

    // Try to extract parent type from parentBirthId
    if (parentBirthId.includes('-clone-')) {
      ancestors[0].type = 'clone';
    } else {
      ancestors[0].type = 'original';
    }

    // Add original parent's ancestors if this was a failed clone attempt
    if (Array.isArray(birthData.ancestors) && birthData.ancestors.length > 0) {
      ancestors.push(...birthData.ancestors);
    }

    // Create new timestamp
    const newCreatedAt = new Date().toISOString();

    // Create message for signature
    const message = `BirthID:${newBirthId}|Created:${newCreatedAt}|Parent:${parentBirthId}`;

    // Sign with wallet private key
    let signature;
    try {
      let privateKey;
      if (originalPrivateKey && !originalPrivateKey.startsWith('encrypted:')) {
        privateKey = originalPrivateKey;
      } else if (birthData.encrypted_private_key) {
        const password = process.env.BIRTH_PRIVATE_KEY_PASSWORD;
        if (!password) {
          console.log('⚠️  Warning: BIRTH_PRIVATE_KEY_PASSWORD not set');
          console.log('   Signature will be kept from original.\n');
          signature = birthData.signature;
        } else {
          try {
            const decrypted = decryptPrivateKey(birthData.encrypted_private_key, password);
            const wallet = new ethers.Wallet(decrypted);
            signature = wallet.signMessageSync(message);
          } catch (decryptError) {
            console.log('⚠️  Warning: Failed to decrypt private key');
            console.log('   Using original signature.\n');
            signature = birthData.signature;
          }
        }
      } else {
        signature = birthData.signature;
      }

      if (!signature && privateKey) {
        const wallet = new ethers.Wallet(privateKey);
        signature = wallet.signMessageSync(message);
      }
    } catch (error) {
      console.log('⚠️  Signature generation failed:', error.message);
      signature = birthData.signature;
    }

    // Update birth data
    const newBirthData = {
      ...birthData,
      birth_id: newBirthId,
      parent_id: parentBirthId,
      type: 'clone',
      created_at: newCreatedAt,
      ancestors: ancestors,
      clone_suffix: cloneSuffix,
      message_for_signature: message,
      signature: signature,
      clone_fixed_at: new Date().toISOString(),
      original_birth_id: originalBirthId,
      original_created_at: originalCreatedAt
    };

    // Write updated birth info
    try {
      fs.writeFileSync(BIRTH_INFO_PATH, JSON.stringify(newBirthData, null, 2), 'utf8');
    } catch (error) {
      console.error('❌ Failed to write birth info:', error.message);
      process.exit(1);
    }

    // Display success
    console.log('✅ Clone identity fixed successfully!\n');
    console.log('📋 Updated Information:');
    console.log(`   New Birth ID: ${newBirthId}`);
    console.log(`   Original Birth ID: ${originalBirthId}`);
    console.log(`   Parent ID: ${parentBirthId}`);
    console.log(`   Clone Suffix: ${cloneSuffix}`);
    console.log(`   Fixed At: ${newBirthData.clone_fixed_at}`);
    console.log('');
    console.log('🧬 Lineage:');
    console.log(`   ${newBirthId}`);
    console.log(`   └─ ${parentBirthId}`);
    if (ancestors.length > 1) {
      console.log(`      └─ (and ${ancestors.length - 1} more ancestors)`);
    }
    console.log('');
    console.log('✨ Fix complete!');
    console.log('');
    console.log('Next Steps:');
    console.log('   1. Verify clone status: node ~/.openclaw/birth-system/whoami.js');
    console.log('   2. Start OpenClaw: openclaw start');
    console.log('');

    return {
      birth_id: newBirthId,
      parent_id: parentBirthId,
      clone_suffix: cloneSuffix,
      original_birth_id: originalBirthId,
      ancestors: ancestors
    };
  }
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

// Parse command line arguments
const args = process.argv.slice(2);
const parentBirthId = args[0];
const force = args.includes('--force');
const auto = args.includes('--auto');

// Run main
if (require.main === module) {
  try {
    const result = fixCloneIdentity(parentBirthId, { force, auto });

    // Export result for programmatic use
    if (process.argv.includes('--json')) {
      console.log(JSON.stringify(result, null, 2));
    }
  } catch (error) {
    console.error('❌ Fix failed:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

module.exports = { fixCloneIdentity };
