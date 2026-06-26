#!/usr/bin/env node
/**
 * BaseMail Setup Script
 * Creates a new wallet for AI agents who don't have one
 * 
 * Usage: 
 *   node setup.js              # Show help
 *   node setup.js --managed    # Generate wallet (always encrypted ✅)
 * 
 * ⚠️ SECURITY: This is optional! Recommended to use existing wallet via
 *    environment variable BASEMAIL_PRIVATE_KEY instead.
 */

const { ethers } = require('ethers');
const fs = require('fs');
const path = require('path');
const readline = require('readline');
const crypto = require('crypto');

const CONFIG_DIR = path.join(process.env.HOME, '.basemail');
const KEY_FILE = path.join(CONFIG_DIR, 'private-key');
const KEY_FILE_ENCRYPTED = path.join(CONFIG_DIR, 'private-key.enc');
const WALLET_FILE = path.join(CONFIG_DIR, 'wallet.json');
const MNEMONIC_FILE = path.join(CONFIG_DIR, 'mnemonic.backup');
const AUDIT_FILE = path.join(CONFIG_DIR, 'audit.log');

function prompt(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  return new Promise(resolve => {
    rl.question(question, answer => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

function promptPassword(question) {
  return new Promise((resolve) => {
    process.stdout.write(question);
    const stdin = process.stdin;
    const wasRaw = stdin.isRaw;
    if (stdin.isTTY) {
      stdin.setRawMode(true);
    }
    stdin.resume();
    stdin.setEncoding('utf8');
    let password = '';
    const onData = (ch) => {
      if (ch === '\n' || ch === '\r' || ch === '\u0004') {
        stdin.removeListener('data', onData);
        if (stdin.isTTY) stdin.setRawMode(wasRaw);
        stdin.pause();
        process.stdout.write('\n');
        resolve(password.trim());
      } else if (ch === '\u0003') {
        process.exit();
      } else if (ch === '\u007F' || ch === '\b') {
        if (password.length > 0) {
          password = password.slice(0, -1);
          process.stdout.write('\b \b');
        }
      } else {
        password += ch;
        process.stdout.write('*');
      }
    };
    stdin.on('data', onData);
  });
}

function logAudit(action, details = {}) {
  try {
    if (!fs.existsSync(CONFIG_DIR)) return;
    const entry = {
      timestamp: new Date().toISOString(),
      action,
      wallet: details.wallet ? `${details.wallet.slice(0, 6)}...${details.wallet.slice(-4)}` : null,
      success: details.success ?? true,
    };
    fs.appendFileSync(AUDIT_FILE, JSON.stringify(entry) + '\n', { mode: 0o600 });
  } catch (e) {
    // Silently ignore audit errors
  }
}

function encryptPrivateKey(privateKey, password) {
  const salt = crypto.randomBytes(16);
  const key = crypto.scryptSync(password, salt, 32);
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  
  let encrypted = cipher.update(privateKey, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  const authTag = cipher.getAuthTag();
  
  return {
    encrypted,
    salt: salt.toString('hex'),
    iv: iv.toString('hex'),
    authTag: authTag.toString('hex'),
    algorithm: 'aes-256-gcm',
  };
}

function showHelp() {
  console.log('🦞 BaseMail Wallet Setup');
  console.log('========================\n');
  
  console.log('📌 推薦方式：使用環境變數（不需要此腳本）\n');
  console.log('   export BASEMAIL_PRIVATE_KEY="0x你的私鑰"');
  console.log('   node scripts/register.js\n');
  
  console.log('📌 或指定現有錢包路徑：\n');
  console.log('   node scripts/register.js --wallet /path/to/your/private-key\n');
  
  console.log('─'.repeat(50));
  console.log('\n⚠️  如果你沒有錢包，可以讓此 Skill 幫你生成：\n');
  console.log('   node setup.js --managed\n');
  console.log('   預設使用密碼加密，私鑰存於 ~/.basemail/private-key.enc');
  console.log('   僅建議對錢包不熟悉的用戶使用\n');
  
  console.log('   Private key is always encrypted with AES-256-GCM\n');
}

async function main() {
  const args = process.argv.slice(2);
  const isManaged = args.includes('--managed');

  // No --managed flag: show help and exit
  if (!isManaged) {
    showHelp();
    process.exit(0);
  }

  console.log('🦞 BaseMail Wallet Setup (Managed Mode)');
  console.log('=======================================\n');

  // Warning
  console.log('⚠️  Warning: About to generate a new wallet');
  console.log('   Private key will be encrypted and stored in ~/.basemail/\n');

  // Check if wallet already exists
  if (fs.existsSync(KEY_FILE) || fs.existsSync(KEY_FILE_ENCRYPTED)) {
    console.log('⚠️  錢包已存在！');
    if (fs.existsSync(KEY_FILE)) console.log(`   ${KEY_FILE}`);
    if (fs.existsSync(KEY_FILE_ENCRYPTED)) console.log(`   ${KEY_FILE_ENCRYPTED}`);
    
    const answer = await prompt('\n要覆蓋現有錢包嗎？這會永久刪除舊錢包！(yes/no): ');
    if (answer.toLowerCase() !== 'yes') {
      console.log('已取消。');
      process.exit(0);
    }
  }

  const confirm = await prompt('確定要繼續嗎？(yes/no): ');
  if (confirm.toLowerCase() !== 'yes') {
    console.log('已取消。');
    process.exit(0);
  }

  // Create config directory
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true, mode: 0o700 });
    console.log(`\n📁 建立目錄 ${CONFIG_DIR}`);
  }

  // Generate new wallet
  console.log('\n🔐 生成新錢包...\n');
  const wallet = ethers.Wallet.createRandom();

  console.log('═'.repeat(50));
  console.log('🎉 新錢包已建立');
  console.log('═'.repeat(50));
  console.log(`\n📍 地址: ${wallet.address}`);
  
  // ❌ 不輸出私鑰到終端！
  // ❌ 不輸出 mnemonic 到終端！
  
  // Always encrypt
  const password = await promptPassword('\nSet encryption password (min 8 chars, letter + number): ');
  const confirmPwd = await promptPassword('Confirm password: ');
  
  if (password !== confirmPwd) {
    console.error('❌ Passwords do not match');
    process.exit(1);
  }
  
  if (password.length < 8) {
    console.error('❌ Password must be at least 8 characters');
    process.exit(1);
  }
  
  if (!/[a-zA-Z]/.test(password) || !/[0-9]/.test(password)) {
    console.error('❌ Password must contain at least one letter and one number');
    process.exit(1);
  }
  
  const encryptedData = encryptPrivateKey(wallet.privateKey, password);
  fs.writeFileSync(KEY_FILE_ENCRYPTED, JSON.stringify(encryptedData, null, 2), { mode: 0o600 });
  console.log(`\n🔐 Encrypted private key saved to: ${KEY_FILE_ENCRYPTED}`);
  
  // Remove legacy plaintext key if exists
  if (fs.existsSync(KEY_FILE)) {
    // Overwrite before deleting for security
    fs.writeFileSync(KEY_FILE, crypto.randomBytes(64).toString('hex'), { mode: 0o600 });
    fs.unlinkSync(KEY_FILE);
    console.log('🗑️  Legacy plaintext key securely removed');
  }
  
  // Remove legacy mnemonic file if exists
  if (fs.existsSync(MNEMONIC_FILE)) {
    fs.writeFileSync(MNEMONIC_FILE, crypto.randomBytes(64).toString('hex'), { mode: 0o600 });
    fs.unlinkSync(MNEMONIC_FILE);
    console.log('🗑️  Legacy mnemonic file securely removed');
  }

  // Display mnemonic for manual backup (NOT saved to file automatically)
  console.log('\n' + '═'.repeat(50));
  console.log('📝 重要：請立即備份你的 Mnemonic（助記詞）');
  console.log('═'.repeat(50));
  console.log('\n' + wallet.mnemonic.phrase + '\n');
  console.log('═'.repeat(50));
  console.log('⚠️  這是唯一一次顯示！請抄寫或安全儲存');
  console.log('⚠️  遺失助記詞將無法恢復錢包');
  console.log('═'.repeat(50));
  
  console.log('📝 Mnemonic will NOT be saved to disk. Please back it up manually now.');
  
  // Save wallet info (public only)
  const walletInfo = {
    address: wallet.address,
    created_at: new Date().toISOString(),
    encrypted: isEncrypt,
    note: 'Private key stored separately',
  };
  fs.writeFileSync(WALLET_FILE, JSON.stringify(walletInfo, null, 2), { mode: 0o600 });

  // Audit log
  logAudit('wallet_created', { wallet: wallet.address, success: true });

  console.log('\n' + '═'.repeat(50));
  console.log('\n⚠️  重要安全提醒：');
  console.log('   1. 請立即備份 mnemonic 檔案到安全的地方');
  console.log('   2. 備份後建議刪除 mnemonic 檔案');
  console.log('   3. 永遠不要分享你的私鑰或 mnemonic');
  if (isEncrypt) {
    console.log('   4. 請牢記你的加密密碼，遺失將無法恢復');
  }

  console.log('\n📋 下一步：');
  console.log('   node scripts/register.js');
  console.log('   (選填) 到 https://www.base.org/names 取得 Basename');

  console.log('\n🦞 設定完成！');
}

main().catch(err => {
  console.error('❌ 錯誤:', err.message);
  process.exit(1);
});
