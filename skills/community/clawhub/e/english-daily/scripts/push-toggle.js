#!/usr/bin/env node
/**
 * english-daily — 每日推送开关
 *
 * 用法:
 *   node push-toggle.js on <userId> [--morning HH:MM] [--channel telegram]
 *   node push-toggle.js off <userId>
 *   node push-toggle.js status <userId>
 *
 * 支持渠道：telegram / feishu / slack / discord
 */

'use strict';

const fs   = require('fs');
const path = require('path');

const USERS_DIR = path.join(__dirname, '../data/users');
const ALLOWED_CHANNELS = new Set(['telegram', 'feishu', 'slack', 'discord']);

// ── Security helpers ──────────────────────────────────────────────────────────

function sanitizeId(value, label) {
  if (typeof value !== 'string' || !/^[a-zA-Z0-9_-]{1,128}$/.test(value)) {
    console.error(`❌ 无效的 ${label}：只允许字母、数字、- 和 _，长度 1-128`);
    process.exit(1);
  }
  return value;
}

function sanitizeTime(value, label) {
  if (typeof value !== 'string' || !/^\d{1,2}:\d{2}$/.test(value)) {
    console.error(`❌ 无效的 ${label}：格式应为 HH:MM，如 08:00`);
    process.exit(1);
  }
  const [h, m] = value.split(':').map(Number);
  if (h < 0 || h > 23 || m < 0 || m > 59) {
    console.error(`❌ 无效的 ${label}：小时 0-23，分钟 0-59`);
    process.exit(1);
  }
  return { h, m };
}

function safeUserPath(userId) {
  const resolved = path.resolve(USERS_DIR, `${userId}.json`);
  if (!resolved.startsWith(path.resolve(USERS_DIR) + path.sep)) {
    console.error('❌ 非法路径');
    process.exit(1);
  }
  return resolved;
}

function loadUser(userId) {
  const f = safeUserPath(userId);
  if (!fs.existsSync(f)) return null;
  return JSON.parse(fs.readFileSync(f, 'utf8'));
}

function saveUser(userId, data) {
  fs.mkdirSync(USERS_DIR, { recursive: true });
  fs.writeFileSync(safeUserPath(userId), JSON.stringify(data, null, 2), 'utf8');
}

// ── Commands ──────────────────────────────────────────────────────────────────

function enablePush(userId, opts = {}) {
  userId = sanitizeId(userId, 'userId');

  const { h: mh, m: mm } = sanitizeTime(opts.morning || '08:00', 'morning');
  const morningDisplay   = `${String(mh).padStart(2,'0')}:${String(mm).padStart(2,'0')}`;
  const morningCron      = `${mm} ${mh} * * *`;

  const rawChannel = opts.channel || 'telegram';
  if (!ALLOWED_CHANNELS.has(rawChannel)) {
    console.error(`❌ 不支持的渠道：${rawChannel}。支持：${[...ALLOWED_CHANNELS].join(', ')}`);
    process.exit(1);
  }
  const channel = rawChannel;

  const sessionKey = `agent:main:${channel}:direct:${userId}`;

  const cronConfig = {
    name: `english-daily-morning-${userId}`,
    cronExpr: morningCron,
    tz: 'Asia/Shanghai',
    session: 'isolated',
    sessionKey,
    channel,
    to: userId,
    announce: true,
    timeoutSeconds: 120,
    message: `node ${path.join(__dirname, 'daily-push.js')} ${userId}`
  };
  console.log(`__OPENCLAW_CRON_ADD__:${JSON.stringify(cronConfig)}`);

  // Update user preferences
  const user = loadUser(userId) || {};
  if (user.preferences) {
    user.preferences.pushEnabled  = true;
    user.preferences.morningTime  = morningDisplay;
    user.preferences.channel      = channel;
  }
  user.pushEnabled   = true;
  user.morningTime   = morningDisplay;
  user.channel       = channel;
  user.pushEnabledAt = new Date().toISOString();
  saveUser(userId, user);

  console.log(`
✅ 每日英语推送已开启

⏰ 推送时间：每天 ${morningDisplay}（今日单词 + 复习）
📡 推送渠道：${channel}

关闭推送：node push-toggle.js off ${userId}
查看状态：node push-toggle.js status ${userId}`);
}

function disablePush(userId) {
  userId = sanitizeId(userId, 'userId');
  const user = loadUser(userId);
  if (!user) {
    console.log(`❌ 未找到用户 ${userId} 的推送记录`);
    return;
  }

  console.log(`__OPENCLAW_CRON_RM__:english-daily-morning-${userId}`);

  if (user.preferences) user.preferences.pushEnabled = false;
  user.pushEnabled    = false;
  user.pushDisabledAt = new Date().toISOString();
  saveUser(userId, user);

  console.log(`✅ 每日英语推送已关闭`);
}

function showStatus(userId) {
  userId = sanitizeId(userId, 'userId');
  const user = loadUser(userId);
  if (!user) {
    console.log(`❌ 未找到用户 ${userId} 的推送记录（请先注册）`);
    return;
  }

  const enabled     = user.pushEnabled || (user.preferences && user.preferences.pushEnabled) || false;
  const morningTime = user.morningTime || (user.preferences && user.preferences.morningTime) || '08:00';
  const channel     = user.channel || (user.preferences && user.preferences.channel) || 'telegram';
  const enabledAt   = user.pushEnabledAt ? user.pushEnabledAt.split('T')[0] : '未知';

  console.log(`
📡 推送状态 — ${userId}（${user.name || ''}）
━━━━━━━━━━━━━━━━━━━━━━━
状态：    ${enabled ? '✅ 开启中' : '❌ 已关闭'}
推送时间：${morningTime}
渠道：    ${channel}
${enabled ? '开启于：  ' + enabledAt : ''}
━━━━━━━━━━━━━━━━━━━━━━━`);
}

module.exports = { enablePush, disablePush, showStatus };

// ── CLI entry ─────────────────────────────────────────────────────────────────

if (require.main !== module) return;

const args    = process.argv.slice(2);
const command = args[0];
const userId  = args[1];

if (!command || !userId) {
  console.log(`用法:
  node push-toggle.js on <userId> [--morning 08:00] [--channel telegram]
  node push-toggle.js off <userId>
  node push-toggle.js status <userId>`);
  process.exit(1);
}

const opts = {};
const mi = args.indexOf('--morning');
if (mi !== -1) opts.morning = args[mi + 1];
const ci = args.indexOf('--channel');
if (ci !== -1) opts.channel = args[ci + 1];

switch (command) {
  case 'on':     enablePush(userId, opts); break;
  case 'off':    disablePush(userId);      break;
  case 'status': showStatus(userId);       break;
  default:
    console.error(`❌ 未知命令：${command}（支持 on/off/status）`);
    process.exit(1);
}
