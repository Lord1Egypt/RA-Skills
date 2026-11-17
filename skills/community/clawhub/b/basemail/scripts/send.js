#!/usr/bin/env node
/**
 * BaseMail Send Email Script
 * 
 * Usage: node send.js <to> <subject> <body>
 * Example: node send.js alice@basemail.ai "Hello" "How are you?"
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
      to: details.to ? `${details.to.split('@')[0].slice(0, 4)}...@${details.to.split('@')[1]}` : null,
      success: details.success ?? true,
      error: details.error,
    };
    fs.appendFileSync(AUDIT_FILE, JSON.stringify(entry) + '\n', { mode: 0o600 });
  } catch (e) {
    // Silently ignore audit errors
  }
}


async function main() {
  const [to, subject, ...bodyParts] = process.argv.slice(2);
  const body = bodyParts.join(' ');

  if (!to || !subject) {
    console.log('📬 BaseMail - 發送郵件\n');
    console.log('用法: node send.js <收件人> <主旨> <內文>');
    console.log('範例: node send.js alice@basemail.ai "Hello" "How are you?"');
    process.exit(1);
  }

  const token = await getToken();

  console.log('📧 發送郵件中...');
  console.log(`   收件人: ${to}`);
  console.log(`   主旨: ${subject}`);

  const { ok, status, data, headers } = await apiFetch('/api/send', {
    method: 'POST',
    body: JSON.stringify({ to, subject, body: body || '' }),
  }, token);

  if (ok && data.success) {
    console.log('\n✅ 發送成功！');
    console.log(`   寄件人: ${data.from}`);
    console.log(`   郵件 ID: ${data.email_id}`);
    logAudit('send_email', { to, success: true });
  } else {
    console.error('\n❌ 發送失敗:', describeError(status, data, headers));
    logAudit('send_email', { to, success: false, error: data.error || `http_${status}` });
    process.exit(1);
  }
}

main().catch(err => {
  console.error('❌ 錯誤:', err.message);
  process.exit(1);
});
