#!/usr/bin/env node
/**
 * BaseMail Registration Script
 * Registers an AI agent for a @basemail.ai email address
 * 
 * Usage: 
 *   node register.js [--basename yourname.base.eth] [--wallet /path/to/key]
 * 
 * Private key sources (in order of priority):
 *   1. BASEMAIL_PRIVATE_KEY environment variable (recommended ✅)
 *   2. --wallet argument specifying path to your key file
 *   3. ~/.basemail/private-key (managed by setup.js)
 * 
 * ⚠️ Security: This script does NOT auto-detect wallet locations outside
 *    ~/.basemail/ to avoid accessing unrelated credentials.
 */

const { ethers } = require('ethers');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const readline = require('readline');

const API_BASE = 'https://api.basemail.ai';
const CONFIG_DIR = path.join(process.env.HOME, '.basemail');
const TOKEN_FILE = path.join(CONFIG_DIR, 'token.json');
const AUDIT_FILE = path.join(CONFIG_DIR, 'audit.log');

function getArg(name) {
  const args = process.argv.slice(2);
  const idx = args.indexOf(name);
  if (idx !== -1 && args[idx + 1]) {
    return args[idx + 1];
  }
  return null;
}

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

function logAudit(action, details = {}) {
  try {
    if (!fs.existsSync(CONFIG_DIR)) {
      fs.mkdirSync(CONFIG_DIR, { recursive: true, mode: 0o700 });
    }
    const entry = {
      timestamp: new Date().toISOString(),
      action,
      wallet: details.wallet ? `${details.wallet.slice(0, 6)}...${details.wallet.slice(-4)}` : null,
      success: details.success ?? true,
      error: details.error,
    };
    fs.appendFileSync(AUDIT_FILE, JSON.stringify(entry) + '\n', { mode: 0o600 });
  } catch (e) {
    // Silently ignore audit errors
  }
}

function decryptPrivateKey(encryptedData, password) {
  const key = crypto.scryptSync(password, Buffer.from(encryptedData.salt, 'hex'), 32);
  const decipher = crypto.createDecipheriv(
    'aes-256-gcm',
    key,
    Buffer.from(encryptedData.iv, 'hex')
  );
  decipher.setAuthTag(Buffer.from(encryptedData.authTag, 'hex'));
  
  let decrypted = decipher.update(encryptedData.encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
}

// Get private key from various sources
async function getPrivateKey() {
  // 1. Environment variable (highest priority, most secure)
  if (process.env.BASEMAIL_PRIVATE_KEY) {
    const key = process.env.BASEMAIL_PRIVATE_KEY.trim();
    if (!/^0x[0-9a-fA-F]{64}$/.test(key)) {
      console.error('❌ BASEMAIL_PRIVATE_KEY 格式無效（必須是 0x + 64 個十六進位字元）');
      process.exit(1);
    }
    console.log('🔑 使用環境變數 BASEMAIL_PRIVATE_KEY');
    return key;
  }
  
  // 2. --wallet argument
  const walletArg = getArg('--wallet');
  if (walletArg) {
    const walletPath = path.resolve(walletArg.replace(/^~/, process.env.HOME));
    
    // Security: validate wallet path
    if (walletPath.includes('..')) {
      console.error('❌ 錢包路徑不允許包含 .. (path traversal)');
      process.exit(1);
    }
    if (!walletPath.startsWith(process.env.HOME)) {
      console.error('❌ 錢包路徑必須在 $HOME 目錄下');
      process.exit(1);
    }
    if (!fs.existsSync(walletPath)) {
      console.error(`❌ 找不到指定的錢包檔案: ${walletPath}`);
      process.exit(1);
    }
    const stat = fs.statSync(walletPath);
    if (!stat.isFile() || stat.size > 1024) {
      console.error('❌ 錢包檔案無效（必須是一般檔案且不超過 1KB）');
      process.exit(1);
    }
    
    // Validate private key format
    const keyContent = fs.readFileSync(walletPath, 'utf8').trim();
    if (!/^0x[0-9a-fA-F]{64}$/.test(keyContent)) {
      console.error('❌ 私鑰格式無效（必須是 0x + 64 個十六進位字元）');
      process.exit(1);
    }
    
    console.log(`🔑 使用指定錢包: ${walletPath}`);
    return keyContent;
  }
  
  // 3. ~/.basemail managed wallet
  const encryptedKeyFile = path.join(CONFIG_DIR, 'private-key.enc');
  const plaintextKeyFile = path.join(CONFIG_DIR, 'private-key'); // legacy support
  
  // Try encrypted wallet
  if (fs.existsSync(encryptedKeyFile)) {
    console.log(`🔐 偵測到加密錢包: ${encryptedKeyFile}`);
    const encryptedData = JSON.parse(fs.readFileSync(encryptedKeyFile, 'utf8'));
    
    const password = process.env.BASEMAIL_PASSWORD || await prompt('請輸入錢包密碼: ');
    try {
      const privateKey = decryptPrivateKey(encryptedData, password);
      logAudit('decrypt_attempt', { success: true });
      return privateKey;
    } catch (e) {
      logAudit('decrypt_attempt', { success: false, error: 'decryption failed' });
      console.error('❌ 密碼錯誤或解密失敗');
      process.exit(1);
    }
  }
  
  // Legacy: try plaintext key (from older versions)
  if (fs.existsSync(plaintextKeyFile)) {
    console.log(`⚠️  Legacy plaintext wallet found: ${plaintextKeyFile}`);
    console.log('   Consider re-running setup.js --managed to encrypt it');
    const key = fs.readFileSync(plaintextKeyFile, 'utf8').trim();
    if (!/^0x[0-9a-fA-F]{64}$/.test(key)) {
      console.error('❌ 私鑰格式無效');
      process.exit(1);
    }
    return key;
  }
  
  // Not found
  console.error('❌ 找不到錢包\n');
  console.error('請選擇一種方式：');
  console.error('  A. export BASEMAIL_PRIVATE_KEY="0x你的私鑰"');
  console.error('  B. node register.js --wallet /path/to/key');
  console.error('  C. node setup.js --managed（生成新錢包）');
  process.exit(1);
}

// Simple fetch wrapper
async function api(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  return res.json();
}

async function main() {
  // Parse args
  const basename = getArg('--basename');

  console.log('🦞 BaseMail Registration');
  console.log('========================\n');

  // Get private key
  const privateKey = await getPrivateKey();
  
  // Initialize wallet
  const wallet = new ethers.Wallet(privateKey);
  const address = wallet.address;

  console.log(`\n📍 錢包地址: ${address}`);
  if (basename) console.log(`📛 Basename: ${basename}`);

  // Step 1: Start auth
  console.log('\n1️⃣ 開始認證...');
  const startData = await api('/api/auth/start', {
    method: 'POST',
    body: JSON.stringify({ address }),
  });

  if (!startData.message) {
    console.error('❌ 認證失敗:', startData);
    logAudit('register', { wallet: address, success: false, error: 'auth_start_failed' });
    process.exit(1);
  }
  console.log('✅ 取得 SIWE 訊息');

  // Step 2: Sign message
  console.log('\n2️⃣ 簽署訊息...');
  const signature = await wallet.signMessage(startData.message);
  console.log('✅ 訊息已簽署');

  // Step 3: Verify
  console.log('\n3️⃣ 驗證簽名...');
  const verifyData = await api('/api/auth/verify', {
    method: 'POST',
    body: JSON.stringify({
      address,
      message: startData.message,
      signature,
    }),
  });

  if (!verifyData.token) {
    console.error('❌ 驗證失敗:', verifyData);
    logAudit('register', { wallet: address, success: false, error: 'verify_failed' });
    process.exit(1);
  }
  console.log('✅ 驗證成功！');

  let token = verifyData.token;
  let email = verifyData.suggested_email;
  let handle = verifyData.handle;

  // Step 4: Register if needed
  if (!verifyData.registered) {
    console.log('\n4️⃣ 註冊中...');
    const regData = await api('/api/register', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify(basename ? { basename } : {}),
    });

    if (!regData.success) {
      console.error('❌ 註冊失敗:', regData);
      logAudit('register', { wallet: address, success: false, error: 'register_failed' });
      process.exit(1);
    }

    token = regData.token || token;
    email = regData.email;
    handle = regData.handle;
    console.log('✅ 註冊成功！');
  }

  // Step 5: Upgrade if we have basename but got 0x handle
  if (basename && handle && handle.startsWith('0x')) {
    console.log('\n5️⃣ 升級至 Basename...');
    const upgradeData = await api('/api/register/upgrade', {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify({ basename }),
    });

    if (upgradeData.success) {
      token = upgradeData.token || token;
      email = upgradeData.email;
      handle = upgradeData.handle;
      console.log('✅ 升級成功！');
    } else {
      console.log('⚠️ 升級失敗:', upgradeData.error || upgradeData);
    }
  }

  // Save token
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true, mode: 0o700 });
  }
  
  const tokenData = {
    token,
    email,
    handle,
    wallet: address.toLowerCase(),
    basename: basename || null,
    saved_at: new Date().toISOString(),
    expires_hint: '24h', // Token expiry hint
  };
  
  fs.writeFileSync(TOKEN_FILE, JSON.stringify(tokenData, null, 2), { mode: 0o600 });

  // Audit log
  logAudit('register', { wallet: address, success: true });

  console.log('\n' + '═'.repeat(40));
  console.log('🎉 成功！');
  console.log('═'.repeat(40));
  console.log(`\n📧 Email: ${email}`);
  console.log(`🎫 Token 已存於: ${TOKEN_FILE}`);
  
  console.log('\n📋 下一步：');
  console.log('   node scripts/send.js someone@basemail.ai "Hi" "Hello!"');
  console.log('   node scripts/inbox.js');
}

main().catch(err => {
  console.error('❌ 錯誤:', err.message);
  process.exit(1);
});
