#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');

const CONFIG_DIR = path.join(os.homedir(), '.openclaw', 'expense-tracker');
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.enc');
const DATA_FILE = path.join(os.homedir(), 'expenses.json');

const ALGORITHM = 'aes-256-gcm';
const SALT_LENGTH = 16;
const IV_LENGTH = 12;
const TAG_LENGTH = 16;
const KEY_LENGTH = 32;
const ITERATIONS = 100000;

const COLORS = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

function log(msg, color = 'reset') {
  console.log(`${COLORS[color]}${msg}${COLORS.reset}`);
}

function ensureDir() {
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
  }
}

// Derive key from password using PBKDF2
function deriveKey(password, salt) {
  return crypto.pbkdf2Sync(password, salt, ITERATIONS, KEY_LENGTH, 'sha256');
}

// Encrypt data with password
function encrypt(data, password) {
  const salt = crypto.randomBytes(SALT_LENGTH);
  const iv = crypto.randomBytes(IV_LENGTH);
  const key = deriveKey(password, salt);
  
  const cipher = crypto.createCipheriv(ALGORITHM, key, iv);
  const encrypted = Buffer.concat([cipher.update(JSON.stringify(data), 'utf8'), cipher.final()]);
  const tag = cipher.getAuthTag();
  
  // Format: salt + iv + tag + encrypted
  return Buffer.concat([salt, iv, tag, encrypted]).toString('base64');
}

// Decrypt data with password
function decrypt(encryptedData, password) {
  try {
    const buffer = Buffer.from(encryptedData, 'base64');
    const salt = buffer.subarray(0, SALT_LENGTH);
    const iv = buffer.subarray(SALT_LENGTH, SALT_LENGTH + IV_LENGTH);
    const tag = buffer.subarray(SALT_LENGTH + IV_LENGTH, SALT_LENGTH + IV_LENGTH + TAG_LENGTH);
    const encrypted = buffer.subarray(SALT_LENGTH + IV_LENGTH + TAG_LENGTH);
    
    const key = deriveKey(password, salt);
    const decipher = crypto.createDecipheriv(ALGORITHM, key, iv);
    decipher.setAuthTag(tag);
    
    const decrypted = decipher.update(encrypted) + decipher.final('utf8');
    return JSON.parse(decrypted);
  } catch (e) {
    return null;
  }
}

let masterPassword = null;

function setPassword(password) {
  masterPassword = password;
}

function loadConfig() {
  ensureDir();
  if (!fs.existsSync(CONFIG_FILE)) {
    return { backend: 'local', local: { path: DATA_FILE } };
  }
  
  if (!masterPassword) {
    const readline = require('readline');
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    rl.question('Enter password to decrypt config: ', (password) => {
      setPassword(password);
      rl.close();
    });
    // Return default for now, will be reloaded after password
    return { backend: 'local', local: { path: DATA_FILE }, _needsPassword: true };
  }
  
  const encryptedData = fs.readFileSync(CONFIG_FILE, 'utf-8');
  const config = decrypt(encryptedData, masterPassword);
  
  if (!config) {
    log('Decryption failed. Wrong password?', 'red');
    return { backend: 'local', local: { path: DATA_FILE } };
  }
  return config;
}

function saveConfig(config) {
  ensureDir();
  
  if (!masterPassword) {
    log('No password set. Config not saved.', 'red');
    return false;
  }
  
  const encrypted = encrypt(config, masterPassword);
  fs.writeFileSync(CONFIG_FILE, encrypted);
  return true;
}

async function setupWithPassword() {
  const readline = require('readline');
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  
  // Set master password first
  rl.question('Set master password: ', (password) => {
    const confirm = rl.question('Confirm password: ');
    if (password !== confirm) {
      log('Passwords do not match', 'red');
      rl.close();
      return;
    }
    setPassword(password);
    
    // Now configure backend
    log('Select storage backend:', 'cyan');
    log('1. Local file (JSON)');
    log('2. Notion');
    log('3. Google Sheet');
    log('4. Supabase');
    
    rl.question('Choice (1-4): ', async (answer) => {
      const config = { backend: 'local', local: { path: DATA_FILE } };
      
      switch (answer) {
        case '1':
          config.backend = 'local';
          rl.question('Data file path (default ~/expenses.json): ', (pathAns) => {
            if (pathAns.trim()) config.local.path = pathAns.trim();
            if (saveConfig(config)) {
              log('Local storage configured', 'green');
            }
            rl.close();
          });
          break;
        case '2':
          config.backend = 'notion';
          rl.question('Notion API Key: ', (key) => {
            config.notion = { api_key: key.trim() };
            rl.question('Database ID: ', (dbId) => {
              config.notion.database_id = dbId.trim();
              if (saveConfig(config)) {
                log('Notion configured', 'green');
              }
              rl.close();
            });
          });
          break;
        case '3':
          config.backend = 'google_sheet';
          rl.question('Credentials file path: ', (credPath) => {
            config.google_sheet = { credentials: credPath.trim() };
            rl.question('Spreadsheet ID: ', (sheetId) => {
              config.google_sheet.spreadsheet_id = sheetId.trim();
              if (saveConfig(config)) {
                log('Google Sheet configured', 'green');
              }
              rl.close();
            });
          });
          break;
        case '4':
          config.backend = 'supabase';
          rl.question('Supabase URL: ', (url) => {
            config.supabase = { url: url.trim() };
            rl.question('Anon Key: ', (key) => {
              config.supabase.api_key = key.trim();
              if (saveConfig(config)) {
                log('Supabase configured', 'green');
              }
              rl.close();
            });
          });
          break;
        default:
          log('Invalid choice', 'red');
          rl.close();
      }
    });
  });
}

function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
}

function getLocalData(config) {
  const filePath = config.local?.path || DATA_FILE;
  if (!fs.existsSync(filePath)) {
    return [];
  }
  return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
}

function saveLocalData(config, data) {
  const filePath = config.local?.path || DATA_FILE;
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

// Notion API
async function notionAdd(config, record) {
  const { api_key, database_id } = config.notion;
  const response = await fetch(`https://api.notion.com/v1/pages`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${api_key}`,
      'Content-Type': 'application/json',
      'Notion-Version': '2022-06-28'
    },
    body: JSON.stringify({
      parent: { database_id },
      properties: {
        Type: { select: { name: record.type } },
        Amount: { number: record.amount },
        Category: { select: { name: record.category } },
        Note: { rich_text: [{ text: { content: record.note } }] },
        Date: { date: { start: record.date } }
      }
    })
  });
  return response.ok;
}

async function notionList(config) {
  const { api_key, database_id } = config.notion;
  const response = await fetch(`https://api.notion.com/v1/databases/${database_id}/query`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${api_key}`,
      'Content-Type': 'application/json',
      'Notion-Version': '2022-06-28'
    },
    body: JSON.stringify({ sorts: [{ property: 'Date', direction: 'descending' }] })
  });
  if (!response.ok) return [];
  const data = await response.json();
  return data.results.map(page => ({
    id: page.id,
    type: page.properties.Type.select?.name,
    amount: page.properties.Amount.number,
    category: page.properties.Category.select?.name,
    note: page.properties.Note.rich_text[0]?.plain_text,
    date: page.properties.Date.date?.start
  }));
}

// Supabase API
async function supabaseAdd(config, record) {
  const { url, api_key } = config.supabase;
  const response = await fetch(`${url}/rest/v1/expenses`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${api_key}`,
      'Content-Type': 'application/json',
      'apikey': api_key
    },
    body: JSON.stringify(record)
  });
  return response.ok;
}

async function supabaseList(config) {
  const { url, api_key } = config.supabase;
  const response = await fetch(`${url}/rest/v1/expenses?order=date.desc`, {
    headers: {
      'Authorization': `Bearer ${api_key}`,
      'apikey': api_key
    }
  });
  if (!response.ok) return [];
  return await response.json();
}

// Google Sheet
async function googleSheetAdd(config, record) {
  log('Google Sheet: not implemented', 'yellow');
  return false;
}

async function googleSheetList(config) {
  log('Google Sheet: not implemented', 'yellow');
  return [];
}

// Commands
async function addRecord(amount, note, category) {
  const config = loadConfig();
  
  if (config._needsPassword) {
    log('Please enter password first', 'red');
    return;
  }
  
  const record = {
    id: generateId(),
    type: amount < 0 ? 'expense' : 'income',
    amount: parseFloat(amount),
    category: category || 'other',
    note: note || '',
    date: new Date().toISOString().split('T')[0],
    created_at: new Date().toISOString()
  };
  
  let success = false;
  
  switch (config.backend) {
    case 'local':
      const data = getLocalData(config);
      data.push(record);
      saveLocalData(config, data);
      success = true;
      break;
    case 'notion':
      success = await notionAdd(config, record);
      break;
    case 'supabase':
      success = await supabaseAdd(config, record);
      break;
    case 'google_sheet':
      success = await googleSheetAdd(config, record);
      break;
  }
  
  if (success) {
    log(`Recorded: ${record.type} | ${record.amount} | ${record.category} | ${record.note}`, 'green');
  } else {
    log('Failed to record', 'red');
  }
}

async function listRecords(options = {}) {
  const config = loadConfig();
  
  if (config._needsPassword) {
    log('Please enter password first', 'red');
    return;
  }
  
  let records = [];
  
  switch (config.backend) {
    case 'local':
      records = getLocalData(config);
      break;
    case 'notion':
      records = await notionList(config);
      break;
    case 'supabase':
      records = await supabaseList(config);
      break;
    case 'google_sheet':
      records = await googleSheetList(config);
      break;
  }
  
  if (options.month) {
    const now = new Date();
    const targetMonth = options.month ? now.getMonth() - options.month : now.getMonth();
    const targetYear = options.month ? now.getFullYear() : now.getFullYear();
    records = records.filter(r => {
      const d = new Date(r.date);
      return d.getMonth() === targetMonth && d.getFullYear() === targetYear;
    });
  }
  
  records.sort((a, b) => new Date(b.date) - new Date(a.date));
  
  if (options.category) {
    const grouped = {};
    records.forEach(r => {
      grouped[r.category] = (grouped[r.category] || 0) + r.amount;
    });
    log('By category:', 'cyan');
    Object.entries(grouped).forEach(([cat, amt]) => {
      log(`  ${cat}: ${amt}`, amt < 0 ? 'red' : 'green');
    });
    return;
  }
  
  log(`Total ${records.length} records:`, 'cyan');
  records.slice(0, 10).forEach(r => {
    const color = r.amount < 0 ? 'red' : 'green';
    log(`  ${r.date} | ${r.type} | ${r.amount} | ${r.category} | ${r.note}`, color);
  });
}

async function stats(monthOffset = 0) {
  const config = loadConfig();
  
  if (config._needsPassword) {
    log('Please enter password first', 'red');
    return;
  }
  
  let records = [];
  
  switch (config.backend) {
    case 'local':
      records = getLocalData(config);
      break;
    case 'notion':
      records = await notionList(config);
      break;
    case 'supabase':
      records = await supabaseList(config);
      break;
    case 'google_sheet':
      records = await googleSheetList(config);
      break;
  }
  
  const now = new Date();
  const targetMonth = now.getMonth() - monthOffset;
  const targetYear = now.getFullYear() + (targetMonth < 0 ? -1 : 0);
  const adjustedMonth = targetMonth < 0 ? 12 + targetMonth : targetMonth;
  
  records = records.filter(r => {
    const d = new Date(r.date);
    return d.getMonth() === adjustedMonth && d.getFullYear() === targetYear;
  });
  
  const income = records.filter(r => r.amount > 0).reduce((sum, r) => sum + r.amount, 0);
  const expense = records.filter(r => r.amount < 0).reduce((sum, r) => sum + r.amount, 0);
  
  log(`=== ${targetYear}-${adjustedMonth + 1} Stats ===`, 'cyan');
  log(`Income: ${income}`, 'green');
  log(`Expense: ${expense}`, 'red');
  log(`Balance: ${income + expense}`, income + expense >= 0 ? 'green' : 'red');
}

// CLI
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case 'setup':
    setupWithPassword();
    break;
  case 'pass':
    if (args[1]) {
      setPassword(args[1]);
      log('Password set', 'green');
    } else {
      log('Usage: expense-tracker pass <password>', 'yellow');
    }
    break;
  case 'add':
    addRecord(args[1], args[2], args[3]);
    break;
  case 'list':
    const listOpts = {};
    if (args.includes('--month')) listOpts.month = 0;
    if (args.includes('--category')) listOpts.category = true;
    listRecords(listOpts);
    break;
  case 'stats':
    const monthIdx = args.indexOf('-m');
    const monthOffset = monthIdx >= 0 ? parseInt(args[monthIdx + 1]) || 0 : 0;
    stats(monthOffset);
    break;
  default:
    log('Usage:', 'cyan');
    log('  expense-tracker setup              # Set password & configure backend');
    log('  expense-tracker pass <password>    # Set password (for API operations)');
    log('  expense-tracker add <amount> <note> <category>  # Add record');
    log('  expense-tracker list               # View records');
    log('  expense-tracker list --month       # This month');
    log('  expense-tracker list --category    # By category');
    log('  expense-tracker stats              # Monthly stats');
    log('  expense-tracker stats -m 1         # Last month');
}
