#!/usr/bin/env node

/**
 * Test Dropbox Connection
 * 
 * Verifies that the OAuth token works by fetching account info and listing root folder.
 */

const fs = require('fs');
const path = require('path');

const TOKEN_PATH = path.join(__dirname, 'token.json');

if (!fs.existsSync(TOKEN_PATH)) {
  console.error('❌ token.json not found! Run setup-oauth.js first.');
  process.exit(1);
}

const tokenData = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
const accessToken = tokenData.access_token;

async function testConnection() {
  console.log('🧪 Testing Dropbox connection...\n');
  
  try {
    // Get account info
    console.log('1️⃣ Fetching account info...');
    const accountResponse = await fetch('https://api.dropboxapi.com/2/users/get_current_account', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(null),
    });
    
    if (!accountResponse.ok) {
      const error = await accountResponse.text();
      throw new Error(`Failed to get account info: ${error}`);
    }
    
    const accountInfo = await accountResponse.json();
    console.log(`   ✅ Connected as: ${accountInfo.name.display_name}`);
    console.log(`   📧 Email: ${accountInfo.email}`);
    console.log(`   🆔 Account ID: ${accountInfo.account_id}\n`);
    
    // List root folder
    console.log('2️⃣ Listing root folder...');
    const listResponse = await fetch('https://api.dropboxapi.com/2/files/list_folder', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        path: '',
        limit: 10,
      }),
    });
    
    if (!listResponse.ok) {
      const error = await listResponse.text();
      throw new Error(`Failed to list folder: ${error}`);
    }
    
    const listData = await listResponse.json();
    console.log(`   ✅ Found ${listData.entries.length} items (showing first 10):\n`);
    
    listData.entries.forEach(entry => {
      const icon = entry['.tag'] === 'folder' ? '📁' : '📄';
      const size = entry.size ? ` (${formatBytes(entry.size)})` : '';
      console.log(`   ${icon} ${entry.name}${size}`);
    });
    
    if (listData.has_more) {
      console.log(`   ... and ${listData.entries.length} more items`);
    }
    
    console.log('\n✅ Connection test successful!');
    
  } catch (error) {
    console.error('\n❌ Connection test failed:', error.message);
    process.exit(1);
  }
}

function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${(bytes / Math.pow(k, i)).toFixed(1)} ${sizes[i]}`;
}

testConnection();
