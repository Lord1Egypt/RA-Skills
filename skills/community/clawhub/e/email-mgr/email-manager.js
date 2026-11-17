#!/usr/bin/env node
/**
 * Email Manager — Read, search, compose, and manage email
 * 
 * Modes:
 *   --inbox [count]                    → Show inbox (default: last 10)
 *   --inbox --unread                   → Show only unread
 *   --inbox --read <id>                → Mark as read
 *   --inbox --delete <id>              → Delete email
 *   --search <query>                   → Search emails
 *   --compose <to> <subject> [body]    → Compose email
 *   --compose --send <to> <subject>    → Send immediately
 *   --thread <id>                      → Show email thread
 *   --status                           → Email status overview
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = (() => {
  if (process.env.EMAIL_DIR) return process.env.EMAIL_DIR;
  let dir = __dirname;
  for (let i = 0; i < 10; i++) {
    if (fs.existsSync(path.join(dir, 'MEMORY.md'))) return dir;
    dir = path.resolve(dir, '..');
  }
  return path.resolve(__dirname, '..', '..');
})();

const DATA_DIR = path.join(WORKSPACE, 'memory', 'email');
const EMAILS_FILE = path.join(DATA_DIR, 'emails.json');
const SETTINGS_FILE = path.join(DATA_DIR, 'settings.json');

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function loadJSON(file, fallback) {
  try {
    const data = fs.readFileSync(file, 'utf8');
    return JSON.parse(data);
  } catch { return fallback || {}; }
}

function saveJSON(file, data) {
  ensureDir(path.dirname(file));
  fs.writeFileSync(file, JSON.stringify(data, null, 2), 'utf8');
}

function getToday() {
  return new Date().toISOString().split('T')[0];
}

function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substring(2, 8);
}

// ─── INBOX ─────────────────────────────────────────────────────────────────

function getInbox(count = 10, unreadOnly = false) {
  const emails = loadJSON(EMAILS_FILE, []);
  let filtered = emails.sort((a, b) => new Date(b.date) - new Date(a.date));
  
  if (unreadOnly) {
    filtered = filtered.filter(e => !e.read);
  }
  
  return filtered.slice(0, count);
}

function showInbox(count = 10, unreadOnly = false) {
  const emails = getInbox(count, unreadOnly);
  
  if (emails.length === 0) {
    console.log('[email-manager] ' + (unreadOnly ? 'No unread emails.' : 'Inbox is empty.'));
    return;
  }
  
  const label = unreadOnly ? 'Unread' : 'Inbox';
  console.log(`[email-manager] ${label} (${emails.length}):\n`);
  
  for (const email of emails) {
    const icon = email.read ? '📧' : '🔔';
    const date = new Date(email.date).toLocaleString();
    const preview = (email.body || '').substring(0, 80).replace(/\n/g, ' ');
    console.log(`  ${icon} ${email.from}`);
    console.log(`     ${email.subject}`);
    console.log(`     ${date}`);
    console.log(`     ${preview}...`);
    console.log(`     ID: ${email.id}`);
    console.log('');
  }
}

// ─── SEARCH ────────────────────────────────────────────────────────────────

function searchEmails(query) {
  const emails = loadJSON(EMAILS_FILE, []);
  const queryLower = query.toLowerCase();
  
  const results = emails.filter(e => {
    const searchable = `${e.from} ${e.to} ${e.subject} ${e.body || ''}`.toLowerCase();
    return searchable.includes(queryLower);
  });
  
  console.log(`[email-manager] Found ${results.length} results for "${query}":\n`);
  for (const email of results.slice(0, 20)) {
    const date = new Date(email.date).toLocaleString();
    console.log(`  📧 ${email.from} — ${email.subject}`);
    console.log(`     ${date}`);
    console.log('');
  }
}

// ─── COMPOSE ───────────────────────────────────────────────────────────────

function composeEmail(to, subject, body = '', send = false) {
  const emails = loadJSON(EMAILS_FILE, []);
  
  const email = {
    id: generateId(),
    from: '', // Configured in settings
    to,
    subject,
    body,
    date: new Date().toISOString(),
    read: true,
    sent: send,
    folder: send ? 'sent' : 'drafts'
  };
  
  // Get configured sender
  const settings = loadJSON(SETTINGS_FILE, {});
  email.from = settings.sender || 'configured@domain.com';
  
  if (send) {
    // In production, would send via SMTP/API
    console.log(`[email-manager] Would send email:`);
    console.log(`  To: ${email.to}`);
    console.log(`  Subject: ${email.subject}`);
    console.log(`  Body: ${email.body.substring(0, 100)}...`);
  } else {
    emails.push(email);
    saveJSON(EMAILS_FILE, emails);
    console.log(`[email-manager] Draft saved: ${email.id}`);
  }
  
  return email;
}

// ─── THREAD ────────────────────────────────────────────────────────────────

function showThread(id) {
  const emails = loadJSON(EMAILS_FILE, []);
  const thread = emails.filter(e => e.threadId === id || e.id === id);
  
  if (thread.length === 0) {
    console.log(`[email-manager] No thread found for: ${id}`);
    return;
  }
  
  console.log(`[email-manager] Thread (${thread.length} messages):\n`);
  for (const email of thread.sort((a, b) => new Date(a.date) - new Date(b.date))) {
    const date = new Date(email.date).toLocaleString();
    const icon = email.read ? '📧' : '🔔';
    console.log(`  ${icon} ${email.from}`);
    console.log(`     ${email.subject}`);
    console.log(`     ${date}`);
    console.log(`     ${(email.body || '').substring(0, 100)}...`);
    console.log('');
  }
}

// ─── MARK READ ─────────────────────────────────────────────────────────────

function markAsRead(id) {
  const emails = loadJSON(EMAILS_FILE, []);
  const email = emails.find(e => e.id === id);
  if (email) {
    email.read = true;
    saveJSON(EMAILS_FILE, emails);
    console.log(`[email-manager] Marked as read: ${email.subject}`);
  } else {
    console.log(`[email-manager] Not found: ${id}`);
  }
}

// ─── DELETE ────────────────────────────────────────────────────────────────

function deleteEmail(id) {
  let emails = loadJSON(EMAILS_FILE, []);
  const idx = emails.findIndex(e => e.id === id);
  if (idx >= 0) {
    const email = emails[idx];
    emails.splice(idx, 1);
    saveJSON(EMAILS_FILE, emails);
    console.log(`[email-manager] Deleted: ${email.subject}`);
  } else {
    console.log(`[email-manager] Not found: ${id}`);
  }
}

// ─── STATUS ────────────────────────────────────────────────────────────────

function showStatus() {
  const emails = loadJSON(EMAILS_FILE, []);
  const unread = emails.filter(e => !e.read).length;
  const drafts = emails.filter(e => e.folder === 'drafts').length;
  const sent = emails.filter(e => e.folder === 'sent').length;
  
  console.log('[email-manager] Status:\n');
  console.log(`  Total emails: ${emails.length}`);
  console.log(`  Unread: ${unread}`);
  console.log(`  Drafts: ${drafts}`);
  console.log(`  Sent: ${sent}`);
  
  if (unread > 0) {
    console.log(`\n  ⚠️ You have ${unread} unread emails.`);
  }
}

// ─── CLI ───────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
let mode = 'status';
let searchQuery = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--inbox') mode = 'inbox';
  if (args[i] === '--search') mode = 'search';
  if (args[i] === '--compose') mode = 'compose';
  if (args[i] === '--thread') mode = 'thread';
  if (args[i] === '--status') mode = 'status';
  if (args[i] === '--unread') searchQuery = 'unread';
  if (args[i] === '--read') searchQuery = 'read';
  if (args[i] === '--delete') searchQuery = 'delete';
  if (args[i] === '--send') searchQuery = 'send';
  if (args[i] === '--dir' && i + 1 < args.length) process.env.EMAIL_DIR = args[i + 1];
}

(async () => {
  switch (mode) {
    case 'inbox': {
      const count = parseInt(args[1]) || 10;
      showInbox(count, searchQuery === 'unread');
      break;
    }
    case 'search': {
      const query = args[1];
      if (!query) {
        console.log('Usage: email-manager.js --search <query>');
      } else {
        searchEmails(query);
      }
      break;
    }
    case 'compose': {
      const to = args[1];
      const subject = args[2];
      const body = args[3] || '';
      if (!to || !subject) {
        console.log('Usage: email-manager.js --compose <to> <subject> [body]');
      } else {
        composeEmail(to, subject, body, searchQuery === 'send');
      }
      break;
    }
    case 'thread':
      showThread(args[1]);
      break;
    case 'status':
      showStatus();
      break;
    default:
      showStatus();
      break;
  }
})();
