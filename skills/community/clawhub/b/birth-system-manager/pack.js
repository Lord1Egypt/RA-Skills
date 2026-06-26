#!/usr/bin/env node

/**
 * OpenClaw Birth System - Pack Plugin
 * Bundle OpenClaw instance for migration with clone tracking
 */

const fs = require('fs');
const path = require('path');
const archiver = require('archiver');
const crypto = require('crypto');

// Configuration
const stateDir = path.join(process.env.HOME, '.openclaw');
const openclawRoot = path.join(process.env.HOME, '.nvm', 'versions', 'node', process.version, 'lib', 'node_modules', 'openclaw');
const timestamp = Date.now();
const outputPath = path.join(process.env.HOME, 'Desktop', `birth-pack-${timestamp}.tar.gz`);
const password = process.argv[2] || process.env.BIRTH_PACK_PASSWORD || 'default-secret-password';

console.log('📦 OpenClaw Birth System - Pack Plugin');
console.log('========================================\n');
console.log(`📂 Source: ${stateDir}`);
console.log(`📁 Output: ${outputPath}`);
console.log(`🔒 Password: ${'*'.repeat(password.length)}\n`);

/**
 * AES-256-CBC encryption with random IV
 */
function encrypt(text, password) {
  const iv = crypto.randomBytes(16);
  const key = crypto.scryptSync(password, 'salt', 32);
  const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
  
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  // Prepend IV to encrypted data
  return iv.toString('hex') + ':' + encrypted;
}

/**
 * AES-256-CBC decryption
 */
function decrypt(encryptedText, password) {
  try {
    const parts = encryptedText.split(':');
    const iv = Buffer.from(parts[0], 'hex');
    const encrypted = parts[1];
    const key = crypto.scryptSync(password, 'salt', 32);
    
    const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);
    
    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    
    return decrypted;
  } catch (error) {
    throw new Error('Decryption failed. Check password.');
  }
}

/**
 * Files and directories to exclude from archive
 */
const excludePatterns = [
  '*.log',
  '*.cache',
  'node_modules/**',
  '.DS_Store',
  '*.dSYM',
  '*.tgz',
  '*.tar.gz',
  'backup*.tar.gz',
  'tmp/**',
  'temp/**',
  '.cache/**',
  '*.sqlite',
  '*.db'
];

/**
 * Check if file should be excluded
 */
function shouldExclude(filePath) {
  return excludePatterns.some(pattern => {
    const regex = new RegExp(pattern.replace(/\*\*/g, '.*').replace(/\*/g, '[^/]*'));
    return regex.test(filePath);
  });
}

/**
 * Add directory to archive with exclusion filters
 */
function addDirectory(archive, dirPath, archivePath) {
  if (!fs.existsSync(dirPath)) {
    console.warn(`⚠️  Directory not found: ${dirPath}`);
    return;
  }

  const files = fs.readdirSync(dirPath);
  
  for (const file of files) {
    const fullPath = path.join(dirPath, file);
    const relativePath = path.join(archivePath, file);
    const stat = fs.statSync(fullPath);
    
    if (shouldExclude(relativePath)) {
      continue;
    }
    
    if (stat.isDirectory()) {
      addDirectory(archive, fullPath, relativePath);
    } else if (stat.isFile()) {
      archive.file(fullPath, { name: relativePath });
    }
  }
}

/**
 * Main packing function
 */
async function packBirthSystem() {
  console.log('Step 1: Preparing pack...\n');
  
  // Create temp directory for generated files
  const tempDir = `/tmp/birth-pack-${timestamp}`;
  fs.mkdirSync(tempDir, { recursive: true });
  
  // Read current birth info
  console.log('Step 2: Reading birth configuration...');
  let birthData;
  try {
    const birthInfoPath = path.join(stateDir, 'birth-info.json');
    const birthInfoContent = fs.readFileSync(birthInfoPath, 'utf8');
    birthData = JSON.parse(birthInfoContent);
  } catch (error) {
    console.error('❌ Failed to read birth info:', error.message);
    process.exit(1);
  }

  const birthId = birthData?.birth_id || 'unknown';
  const walletAddress = birthData?.wallet_address || 'unknown';
  console.log(`✅ Birth ID: ${birthId}`);
  console.log(`✅ Wallet: ${walletAddress}\n`);
  
  // Create clone marker
  console.log('Step 3: Creating clone marker...');
  const marker = {
    original_birth_id: birthId,
    original_wallet: walletAddress,
    pack_time: timestamp,
    pack_version: '1.0.0',
    is_for_clone: true,
    metadata: {
      hostname: require('os').hostname(),
      platform: process.platform,
      arch: process.arch,
      node_version: process.version
    }
  };
  
  const markerPath = path.join(tempDir, 'clone-marker.json');
  fs.writeFileSync(markerPath, JSON.stringify(marker, null, 2));
  console.log(`✅ Clone marker created\n`);
  
  // Create encrypted wallet backup
  console.log('Step 4: Encrypting sensitive data...');
  if (birthData?.private_key) {
    const walletData = JSON.stringify({
      birth_id: birthId,
      wallet_address: walletAddress,
      private_key: birthData.private_key,
      public_key: birthData.public_key,
      signature: birthData.signature,
      created_at: birthData.created_at
    }, null, 2);
    
    const encryptedWallet = encrypt(walletData, password);
    const encryptedPath = path.join(tempDir, 'wallet-backup.encrypted');
    fs.writeFileSync(encryptedPath, encryptedWallet);
    console.log(`✅ Wallet backup encrypted\n`);
  } else {
    console.warn('⚠️  No wallet data found to encrypt\n');
  }
  
  // Create migration instructions
  console.log('Step 5: Creating migration instructions...');
  const instructions = `# OpenClaw Birth System - Migration Instructions

## Overview
This package contains a complete OpenClaw instance with birth system tracking.
Pack created: ${new Date(timestamp).toISOString()}
Original Birth ID: ${birthId}

## Prerequisites
- Node.js 22+
- Extracted password: ${password}

## Migration Steps

### 1. Extract Package
\`\`\`bash
# Extract to home directory
tar -xzf birth-pack-${timestamp}.tar.gz -C ~/
\`\`\`

### 2. Setup Environment
\`\`\`bash
# Set clone flag
export IS_CLONE=true

# Optional: Set custom state directory
export OPENCLAW_STATE_DIR=\\$HOME/.openclaw
\`\`\`

### 3. Verify Birth System
\`\`\`bash
# Check birth information
node ~/.openclaw/birth-system/whoami.js

# Expected output: Clone detected with parent ID matching original
\`\`\`

### 4. Decrypt Wallet (if needed)
\`\`\`bash
# Using decryption script (if available)
node ~/.openclaw/birth-system/decrypt-wallet.js ${password}
\`\`\`

### 5. Start OpenClaw
\`\`\`bash
# Start gateway
openclaw gateway start

# Or run directly
openclaw dashboard
\`\`\`

## Verification

After migration, verify the following:
- [ ] Birth ID shows clone status
- [ ] Parent ID matches original: ${birthId}
- [ ] Signature is valid
- [ ] All channels and integrations work

## Troubleshooting

### "No Birth ID found"
Run birth system initialization:
\`\`\`bash
node ~/.openclaw/birth-system/generate-birth-id.js
\`\`\`

### "Signature verification failed"
Restore from backup and re-migrate.

### "Clone marker not found"
Check that clone-marker.json exists in the package.

## Rollback

If migration fails, restore original instance:
\`\`\`bash
tar -xzf ~/Desktop/openclaw-backup-*.tar.gz -C ~/
\`\`\`

## Support

For issues and questions, refer to:
- Birth System README: ~/.openclaw/birth-system/README.md
- OpenClaw Documentation: https://docs.openclaw.ai

---
Generated by OpenClaw Birth Pack Plugin v1.0.0
`;

  const instructionsPath = path.join(tempDir, 'MIGRATION.md');
  fs.writeFileSync(instructionsPath, instructions);
  console.log(`✅ Migration instructions created\n`);
  
  // Create archive
  console.log('Step 6: Creating archive...');
  const archive = archiver('tar', { gzip: true });
  const output = fs.createWriteStream(outputPath);
  
  archive.pipe(output);
  
  // Add clone marker
  archive.file(markerPath, { name: 'clone-marker.json' });
  
  // Add encrypted wallet
  if (fs.existsSync(path.join(tempDir, 'wallet-backup.encrypted'))) {
    archive.file(path.join(tempDir, 'wallet-backup.encrypted'), { name: 'wallet-backup.encrypted' });
  }
  
  // Add migration instructions
  archive.file(instructionsPath, { name: 'MIGRATION.md' });
  
  // Add birth system files
  const birthSystemDir = path.join(stateDir, 'birth-system');
  if (fs.existsSync(birthSystemDir)) {
    addDirectory(archive, birthSystemDir, '.openclaw/birth-system');
  }
  
  // Add openclaw.json (exclude sensitive data)
  const safeConfig = { ...birthData };
  if (safeConfig?.private_key) {
    safeConfig.private_key = '[ENCRYPTED - see wallet-backup.encrypted]';
  }
  const safeConfigPath = path.join(tempDir, 'birth-info.json');
  fs.writeFileSync(safeConfigPath, JSON.stringify(safeConfig, null, 2));
  archive.file(safeConfigPath, { name: '.openclaw/birth-info.json' });
  
  // Add DID dependencies
  console.log('Step 7: Adding DID dependencies...');
  const openclawNodeModules = path.join(openclawRoot, 'node_modules');
  
  const didLibPath = path.join(openclawNodeModules, '@digitalbazaar');
  if (fs.existsSync(didLibPath)) {
    addDirectory(archive, didLibPath, 'node_modules/@digitalbazaar');
    console.log('✅ Added @digitalbazaar/did-io');
  }
  
  const ethersPath = path.join(openclawNodeModules, 'ethers');
  if (fs.existsSync(ethersPath)) {
    addDirectory(archive, ethersPath, 'node_modules/ethers');
    console.log('✅ Added ethers');
  }
  
  // Add workspace (if exists)
  const workspaceDir = process.env.OPENCLAW_WORKSPACE || path.join(stateDir, 'workspace');
  if (fs.existsSync(workspaceDir)) {
    addDirectory(archive, workspaceDir, '.openclaw/workspace');
    console.log('✅ Added workspace');
  }
  
  // Add skills (if exists)
  const skillsDir = path.join(workspaceDir, 'skills');
  if (fs.existsSync(skillsDir)) {
    addDirectory(archive, skillsDir, '.openclaw/workspace/skills');
    console.log('✅ Added skills');
  }
  
  // Add memory (if exists)
  const memoryDir = path.join(workspaceDir, 'memory');
  if (fs.existsSync(memoryDir)) {
    addDirectory(archive, memoryDir, '.openclaw/workspace/memory');
    console.log('✅ Added memory');
  }
  
  console.log('');
  
  // Finalize archive
  console.log('Step 8: Finalizing archive...');
  await new Promise((resolve, reject) => {
    output.on('close', resolve);
    output.on('error', reject);
    archive.finalize();
  });
  
  const stats = fs.statSync(outputPath);
  console.log(`✅ Archive created: ${(stats.size / 1024 / 1024).toFixed(2)} MB\n`);
  
  // Cleanup temp files
  console.log('Step 9: Cleanup...');
  fs.rmSync(tempDir, { recursive: true, force: true });
  console.log('✅ Cleanup complete\n');
  
  // Display summary
  console.log('✨ Pack completed successfully!\n');
  console.log('Summary:');
  console.log(`  📦 Package: ${outputPath}`);
  console.log(`  🆔 Birth ID: ${birthId}`);
  console.log(`  🔐 Password: ${password}`);
  console.log(`  📊 Size: ${(stats.size / 1024 / 1024).toFixed(2)} MB`);
  console.log('');
  console.log('Next Steps:');
  console.log('  1. Transfer package to target machine');
  console.log('  2. Extract and follow MIGRATION.md instructions');
  console.log('  3. Verify clone status with: node ~/.openclaw/birth-system/whoami.js');
  console.log('');
  console.log('📋 To verify pack contents:');
  console.log(`  tar -tzf "${outputPath}"`);
  console.log('');
}

// Run pack
packBirthSystem().catch(error => {
  console.error('❌ Error:', error.message);
  console.error(error.stack);
  process.exit(1);
});

module.exports = { encrypt, decrypt };
