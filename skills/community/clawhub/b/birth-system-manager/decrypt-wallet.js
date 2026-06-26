#!/usr/bin/env node

/**
 * OpenClaw Birth System - Wallet Decrypt Script
 * Decrypt encrypted wallet backup
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// Decrypt from encrypted_private_key in birth-info.json
const birthInfoPath = process.argv[2] || path.join(process.env.HOME, '.openclaw', 'birth-info.json');
const password = process.argv[3] || process.env.BIRTH_PRIVATE_KEY_PASSWORD;

console.log('🔓 OpenClaw Birth System - Wallet Decrypt');
console.log('========================================\n');

// AES-256-CBC 解密
function decrypt(encryptedText, password) {
  try {
    const parts = encryptedText.split(':');
    const iv = Buffer.from(parts[0], 'hex');
    const encrypted = parts.slice(1).join(':');
    const key = crypto.scryptSync(password, 'openclaw-birth-salt', 32);

    const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);

    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');

    return decrypted;
  } catch (error) {
    throw new Error('Decryption failed. Check password.');
  }
}

if (!password) {
  console.error('❌ Password required.');
  console.error('Usage: node decrypt-wallet.js <birth-info-path> <password>');
  console.error('Or set BIRTH_PRIVATE_KEY_PASSWORD environment variable.');
  process.exit(1);
}

try {
  if (!fs.existsSync(birthInfoPath)) {
    console.error('❌ Birth info file not found:', birthInfoPath);
    process.exit(1);
  }

  // Read birth-info.json
  const birthInfoContent = fs.readFileSync(birthInfoPath, 'utf8');
  const birthInfo = JSON.parse(birthInfoContent);

  if (!birthInfo.encrypted_private_key) {
    console.error('❌ No encrypted_private_key found in birth-info.json');
    process.exit(1);
  }

  // Decrypt private key
  const privateKey = decrypt(birthInfo.encrypted_private_key, password);

  // Verify private key matches wallet address
  const ethers = require('ethers');
  const wallet = new ethers.Wallet(privateKey);

  if (wallet.address.toLowerCase() !== birthInfo.wallet_address.toLowerCase()) {
    console.error('❌ Private key does not match wallet address!');
    console.error(`   Expected: ${birthInfo.wallet_address}`);
    console.error(`   Got: ${wallet.address}`);
    process.exit(1);
  }

  console.log('✅ Private key decrypted successfully!');
  console.log(`📁 Birth ID: ${birthInfo.birth_id}`);
  console.log(`🔑 Wallet Address: ${wallet.address}`);
  console.log(`📅 Created: ${new Date(birthInfo.created_at).toISOString()}`);
  console.log('');

  // Option 1: Output to stdout (safe, doesn't write to disk)
  if (process.env.DECRYPT_OUTPUT_TO_FILE === 'true') {
    const outputPath = path.join(path.dirname(birthInfoPath), 'private-key-decrypted.txt');
    fs.writeFileSync(outputPath, privateKey);
    console.log(`⚠️  Private key written to: ${outputPath}`);
    console.log('   Delete this file immediately after use!\n');
  } else {
    console.log('🔐 Private Key:');
    console.log('─'.repeat(60));
    console.log(privateKey);
    console.log('─'.repeat(60));
    console.log('');
    console.log('💡 To save to file: export DECRYPT_OUTPUT_TO_FILE=true && node decrypt-wallet.js ...');
    console.log('');
  }

} catch (error) {
  console.error('❌ Decryption failed:', error.message);
  console.error('\nCommon issues:');
  console.error('  - Incorrect password');
  console.error('  - Corrupted encrypted data');
  console.error('  - Password environment variable not set');
  process.exit(1);
}
