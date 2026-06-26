#!/usr/bin/env node

/**
 * OpenClaw Birth System - Whoami Command
 * Display and verify birth information with full family tree lineage tracking
 */

const ethers = require('ethers');
const fs = require('fs');
const path = require('path');

const BIRTH_INFO_PATH = path.join(process.env.HOME, '.openclaw', 'birth-info.json');

/**
 * Verify birth signature
 */
function verifyBirthSignature(birthData) {
  try {
    const message = `BirthID:${birthData.birth_id}|Created:${birthData.created_at}|Parent:${birthData.parent_id || 'none'}`;
    const recoveredAddress = ethers.verifyMessage(message, birthData.signature);
    return recoveredAddress === birthData.wallet_address;
  } catch (error) {
    return false;
  }
}

/**
 * Format timestamp
 */
function formatTimestamp(timestamp) {
  return new Date(timestamp).toISOString();
}

/**
 * Format date for display
 */
function formatDate(timestamp) {
  const date = new Date(timestamp);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    timeZoneName: 'short'
  });
}

/**
 * Build family tree string from ancestors array
 */
function buildFamilyTree(ancestors, currentBirthId, showDetails = false) {
  if (!Array.isArray(ancestors) || ancestors.length === 0) {
    return '';
  }

  const lines = [];

  // Current instance (this clone)
  lines.push(`   📌 ${currentBirthId}`);
  lines.push(`      Type: Clone`);

  // Build ancestor chain
  ancestors.forEach((ancestor, index) => {
    const isLast = index === ancestors.length - 1;
    const prefix = isLast ? '      └─' : '      ├─';
    const suffix = ancestor.type === 'original' ? ' [Original]' : ` [Clone]`;

    lines.push(`${prefix} ${ancestor.birth_id}${suffix}`);

    if (showDetails) {
      lines.push(`        Created: ${formatDate(ancestor.created_at)}`);
    }
  });

  return lines.join('\n');
}

/**
 * Calculate age
 */
function calculateAge(createdAt) {
  const createdAtTime = typeof createdAt === 'string'
    ? new Date(createdAt).getTime()
    : createdAt;
  const ageMs = Date.now() - createdAtTime;

  const days = Math.floor(ageMs / 86400000);
  const hours = Math.floor((ageMs % 86400000) / 3600000);
  const minutes = Math.floor((ageMs % 3600000) / 60000);

  if (days > 0) return `${days} day${days > 1 ? 's' : ''}`;
  if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''}`;
  return `${minutes} minute${minutes > 1 ? 's' : ''}`;
}

/**
 * Main function
 */
function main() {
  console.log('🔮 OpenClaw Birth System - Whoami');
  console.log('=====================================\n');

  // Load birth info
  let birthData;
  try {
    const birthInfoContent = fs.readFileSync(BIRTH_INFO_PATH, 'utf8');
    birthData = JSON.parse(birthInfoContent);
  } catch (error) {
    console.error('❌ Failed to load birth info:', error.message);
    console.log('   Make sure birth-info.json exists at ~/.openclaw/birth-info.json\n');
    process.exit(1);
  }

  if (!birthData.birth_id) {
    console.log('⚠️  No Birth ID found. Run birth-system initialization first.');
    process.exit(0);
  }

  const bs = birthData;

  // Display birth ID
  console.log('🆔 Birth ID:');
  console.log(`   ${bs.birth_id}`);
  console.log('');

  // Display type
  console.log('🏷️  Type:');
  console.log(`   ${bs.type === 'clone' ? '🧬 Clone' : '🏆 Original'}`);
  console.log('');

  // Display lineage / family tree
  console.log('🧬 Lineage / Family Tree:');
  if (bs.type === 'clone' && bs.parent_id) {
    const tree = buildFamilyTree(bs.ancestors, bs.birth_id, process.argv.includes('--verbose'));
    console.log(tree);
  } else {
    console.log('   Original instance (no parent)');
  }
  console.log('');

  // Display creation time
  console.log('📅 Created:');
  console.log(`   ${formatDate(bs.created_at)}`);
  console.log('');

  // Display age
  const age = calculateAge(bs.created_at);
  console.log('⏱️  Age:');
  console.log(`   ${age}`);
  console.log('');

  // Display clone suffix if exists
  if (bs.clone_suffix) {
    console.log('🏷️  Clone Suffix:');
    console.log(`   ${bs.clone_suffix}`);
    console.log('');
  }

  // Display wallet info
  console.log('🔑 Wallet Address:');
  console.log(`   ${bs.wallet_address}`);
  console.log('');

  // Verify signature
  console.log('🔒 Signature Verification:');
  const isValid = verifyBirthSignature(bs);
  if (isValid) {
    console.log('   ✅ Valid - Birth data is authentic');
  } else {
    console.log('   ❌ Invalid - Birth data may be tampered!');
  }
  console.log('');

  // Display clone count from ancestors
  if (Array.isArray(bs.ancestors) && bs.ancestors.length > 0) {
    console.log('👨‍👩‍👧‍👦 Ancestors:');
    console.log(`   ${bs.ancestors.length} ancestor${bs.ancestors.length > 1 ? 's' : ''} in lineage`);
    console.log('');
  }

  // Summary
  console.log('📊 Summary:');
  console.log(`   Type: ${bs.type === 'clone' ? 'Clone' : 'Original'}`);
  console.log(`   Status: ${isValid ? '✅ Verified' : '⚠️  Warning'}`);

  if (bs.type === 'clone') {
    console.log(`   Generation: ${bs.ancestors ? bs.ancestors.length : 0}+`);
  }
  console.log('');

  return {
    birth_id: bs.birth_id,
    parent_id: bs.parent_id,
    type: bs.type,
    is_clone: bs.type === 'clone',
    clone_suffix: bs.clone_suffix,
    created_at: bs.created_at,
    wallet_address: bs.wallet_address,
    signature_valid: isValid,
    ancestors: bs.ancestors || [],
    ancestor_count: Array.isArray(bs.ancestors) ? bs.ancestors.length : 0
  };
}

// Run main
if (require.main === module) {
  const result = main();

  // Export result for programmatic use
  if (process.argv.includes('--json')) {
    console.log(JSON.stringify(result, null, 2));
  }
}

module.exports = { main, verifyBirthSignature, buildFamilyTree };
