#!/usr/bin/env node
/**
 * career-news — push-toggle.js
 * 开关用户推送 / 显示 cron 命令
 *
 * 用法:
 *   node scripts/push-toggle.js                  # 显示 cron 安装命令
 *   node scripts/push-toggle.js --userId <id>    # 切换该用户推送状态
 */

const fs = require('fs');
const path = require('path');

const USERS_DIR = path.join(__dirname, '..', 'data', 'users');
const SKILL_DIR = path.resolve(__dirname, '..');

const args = process.argv.slice(2);
const userIdx = args.indexOf('--userId');
const userId = userIdx !== -1 ? args[userIdx + 1] : null;

if (!userId) {
  // Show cron setup instructions
  console.log('Career News — Cron Setup');
  console.log('─'.repeat(50));
  console.log('Morning push (7:00 AM daily):');
  console.log(`  openclaw cron add "0 7 * * *" "cd ${SKILL_DIR} && node scripts/morning-push.js"`);
  console.log('');
  console.log('Test commands:');
  console.log(`  node scripts/morning-push.js --dry-run`);
  console.log(`  node scripts/morning-push.js --user <userId>`);
  console.log('');
  console.log('To toggle a user\'s push: node scripts/push-toggle.js --userId <id>');
  process.exit(0);
}

const safeId = userId.replace(/[^a-zA-Z0-9_-]/g, '');
const fp = path.join(USERS_DIR, `${safeId}.json`);

if (!fs.existsSync(fp)) {
  console.error(`User "${userId}" not found.`);
  process.exit(1);
}

const u = JSON.parse(fs.readFileSync(fp, 'utf8'));
u.pushEnabled = !u.pushEnabled;
u.updatedAt = new Date().toISOString();
fs.writeFileSync(fp, JSON.stringify(u, null, 2));

const status = u.pushEnabled ? '✅ enabled' : '⏸ disabled';
console.log(`Push for "${safeId}" is now ${status}.`);
