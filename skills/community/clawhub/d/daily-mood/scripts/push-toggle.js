#!/usr/bin/env node
/**
 * daily-mood — push-toggle.js
 * 管理 openclaw cron 定时推送开关，支持全局或单用户级别
 *
 * 用法:
 *   node scripts/push-toggle.js on                    # 开启全局 cron（早晨+傍晚）
 *   node scripts/push-toggle.js on --userId <id>      # 仅开启某用户的推送标志
 *   node scripts/push-toggle.js off                   # 关闭全局 cron
 *   node scripts/push-toggle.js off --userId <id>     # 仅关闭某用户的推送标志
 *   node scripts/push-toggle.js status                # 查看 cron 状态
 */

const fs = require('fs');
const path = require('path');

const USERS_DIR = path.join(__dirname, '..', 'data', 'users');
const args = process.argv.slice(2);
const action = args[0];

if (!action || !['on','off','status'].includes(action)) {
  console.error('Usage: node scripts/push-toggle.js on|off|status [--userId <id>]');
  process.exit(1);
}

const userIdIdx = args.indexOf('--userId');
const userId = userIdIdx !== -1
  ? args[userIdIdx + 1].replace(/[^a-zA-Z0-9_-]/g,'').substring(0,64)
  : null;

const skillDir = path.join(__dirname, '..');
const morningCmd = `cd ${skillDir} && node scripts/morning-push.js`;
const eveningCmd = `cd ${skillDir} && node scripts/evening-push.js`;

// Per-user toggle: just update the pushEnabled flag in the profile
if (userId) {
  const fp = path.join(USERS_DIR, `${userId}.json`);
  if (!fs.existsSync(fp)) {
    console.error(`User "${userId}" not found. Register first: node scripts/register.js ${userId}`);
    process.exit(1);
  }
  const u = JSON.parse(fs.readFileSync(fp, 'utf8'));
  if (action === 'on') {
    u.pushEnabled = true;
    fs.writeFileSync(fp, JSON.stringify(u, null, 2));
    console.log(`Push ENABLED for user: ${userId}`);
  } else if (action === 'off') {
    u.pushEnabled = false;
    fs.writeFileSync(fp, JSON.stringify(u, null, 2));
    console.log(`Push DISABLED for user: ${userId}`);
  } else {
    console.log(`User ${userId}: pushEnabled = ${u.pushEnabled}`);
  }
  process.exit(0);
}

// Global cron toggle
if (action === 'on') {
  console.log(`
开启每日心情寄语推送，请在终端运行以下命令：

  openclaw cron add "0 8 * * *"  "${morningCmd}"
  openclaw cron add "0 21 * * *" "${eveningCmd}"

这将设置：
  • 每日 08:00 早晨寄语推送（推送所有已注册用户）
  • 每日 21:00 傍晚寄语推送（推送所有已注册用户）

添加后验证：
  openclaw cron list

注册用户：
  node scripts/register.js <userId> --lang zh --mood neutral

关闭推送：
  node scripts/push-toggle.js off
`);
} else if (action === 'off') {
  console.log(`
关闭每日心情寄语推送，请运行：

  openclaw cron list

找到含 "daily-mood" 的任务并记录 ID，然后：

  openclaw cron delete <morning-task-id>
  openclaw cron delete <evening-task-id>

如只想暂停某一用户（不删除 cron）：
  node scripts/push-toggle.js off --userId <userId>
`);
} else {
  // Show registered user count
  let userCount = 0;
  let enabledCount = 0;
  if (fs.existsSync(USERS_DIR)) {
    const files = fs.readdirSync(USERS_DIR).filter(f => f.endsWith('.json'));
    userCount = files.length;
    enabledCount = files.filter(f => {
      const u = JSON.parse(fs.readFileSync(path.join(USERS_DIR, f), 'utf8'));
      return u.pushEnabled !== false;
    }).length;
  }

  console.log(`
每日心情寄语推送状态
─────────────────────────────
已注册用户：${userCount}
推送已开启：${enabledCount} 人

查看 cron 任务：
  openclaw cron list
  → 查找含 "daily-mood" 的条目
  → 应有 2 条：morning-push.js (08:00) 和 evening-push.js (21:00)

如未配置 cron：
  node scripts/push-toggle.js on

查看所有用户：
  node scripts/register.js --list
`);
}
