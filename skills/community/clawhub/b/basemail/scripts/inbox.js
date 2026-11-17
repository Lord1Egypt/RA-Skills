#!/usr/bin/env node
/**
 * BaseMail Inbox Script
 * 
 * Usage: 
 *   node inbox.js              # List inbox
 *   node inbox.js <email_id>   # Read specific email
 */

const fs = require('fs');
const path = require('path');

const { API_BASE, CONFIG_DIR, getToken, apiFetch, describeError } = require('./token');
const AUDIT_FILE = path.join(CONFIG_DIR, 'audit.log');

function logAudit(action, details = {}) {
  try {
    if (!fs.existsSync(CONFIG_DIR)) return;
    const entry = {
      timestamp: new Date().toISOString(),
      action,
      success: details.success ?? true,
    };
    fs.appendFileSync(AUDIT_FILE, JSON.stringify(entry) + '\n', { mode: 0o600 });
  } catch (e) {
    // Silently ignore audit errors
  }
}


async function listInbox(token) {
  const { ok, status, data, headers } = await apiFetch('/api/inbox', {}, token);

  if (!ok || data.error) {
    console.error('❌ 錯誤:', describeError(status, data, headers));
    logAudit('inbox_list', { success: false });
    process.exit(1);
  }

  console.log(`📬 收件箱 (${data.unread} 未讀 / ${data.total} 總計)`);
  console.log('═'.repeat(60));

  if (data.emails.length === 0) {
    console.log('沒有郵件。');
    return;
  }

  for (const email of data.emails) {
    const unread = email.read ? ' ' : '●';
    const date = new Date(email.created_at * 1000).toLocaleString();
    console.log(`${unread} [${email.id}]`);
    console.log(`  寄件人: ${email.from_addr}`);
    console.log(`  主旨: ${email.subject}`);
    console.log(`  時間: ${date}`);
    console.log(`  預覽: ${email.snippet?.slice(0, 80)}...`);
    console.log('');
  }
  
  logAudit('inbox_list', { success: true });
}

async function readEmail(token, emailId) {
  const { ok, status, data, headers } = await apiFetch(`/api/inbox/${encodeURIComponent(emailId)}`, {}, token);

  if (!ok || data.error) {
    console.error('❌ 錯誤:', describeError(status, data, headers));
    logAudit('inbox_read', { success: false });
    process.exit(1);
  }

  console.log('📧 郵件內容');
  console.log('═'.repeat(60));
  console.log(`寄件人: ${data.from_addr}`);
  console.log(`收件人: ${data.to_addr}`);
  console.log(`主旨: ${data.subject}`);
  console.log(`時間: ${new Date(data.created_at * 1000).toLocaleString()}`);
  console.log('═'.repeat(60));
  console.log(data.body);
  
  logAudit('inbox_read', { success: true });
}

async function main() {
  const emailId = process.argv[2];
  const token = await getToken();

  if (emailId) {
    await readEmail(token, emailId);
  } else {
    await listInbox(token);
  }
}

main().catch(err => {
  console.error('❌ 錯誤:', err.message);
  process.exit(1);
});
