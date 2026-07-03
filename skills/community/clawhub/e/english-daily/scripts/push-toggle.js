#!/usr/bin/env node
/**
 * english-daily — 每日推送开关（无文件写入版）
 *
 * 档案存放在原生 MEMORY.md 中，由 Agent 维护；本脚本不读写任何文件。
 * 开启推送所需的等级/每日目标由 Agent 从 MEMORY.md 读出后作为参数传入，
 * cron 任务通过 openclaw 运行时协议（__OPENCLAW_CRON_ADD__）创建，运行时负责持久化。
 *
 * 用法:
 *   node push-toggle.js on <userId> [--name <姓名>] [--level A1|A2|B1|B2] \
 *        [--goal <每日目标>] [--morning HH:MM] [--channel telegram]
 *   node push-toggle.js off <userId>
 *   node push-toggle.js status <userId>
 *
 * 支持渠道：telegram / feishu / slack / discord
 */

'use strict';

const path = require('path');

const ALLOWED_CHANNELS = new Set(['telegram', 'feishu', 'slack', 'discord']);
const VALID_LEVELS = ['A1', 'A2', 'B1', 'B2'];

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

  let level = (opts.level || 'B1').toUpperCase();
  if (!VALID_LEVELS.includes(level)) {
    console.error(`❌ 无效的等级：${level}。支持：${VALID_LEVELS.join('/')}`);
    process.exit(1);
  }

  let goal = parseInt(opts.goal, 10);
  if (isNaN(goal) || goal < 1 || goal > 20) goal = 5;

  const sessionKey = `agent:main:${channel}:direct:${userId}`;

  // cron 消息为一条 prompt：让 Agent 先从 MEMORY.md 读出该用户档案的 streak/last/points/SRS进度，
  // 再运行 daily-push.js（等级/目标已烘焙进来），最后把脚本输出的 MEMORY.md 区块回写。
  const message =
    `每日英语推送时间到。请为用户 ${userId} 生成今日学习内容：\n` +
    `1) 从 MEMORY.md 读取 <!-- english-daily:profile:${userId} --> 区块，取出 连续学习(streak)/最长(longest)/上次学习(last)/总积分(points)/SRS进度(progress JSON)。\n` +
    `2) 运行：node ${path.join(__dirname, 'daily-push.js')} ${userId} --level ${level} --goal ${goal} --progress '<SRS进度JSON>' --streak <n> --longest <n> --last <YYYY-MM-DD> --points <n>\n` +
    `3) 把复习词+新词以 ${opts.name || userId} 的母语友好地呈现，并附一句英文激励。\n` +
    `4) 用脚本输出的 MEMORY.md 区块更新原生记忆（streak/lastStudyDate 已刷新）。`;

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
    message
  };
  console.log(`__OPENCLAW_CRON_ADD__:${JSON.stringify(cronConfig)}`);

  console.log(`
✅ 每日英语推送已开启

⏰ 推送时间：每天 ${morningDisplay}（今日单词 + 复习）
📡 推送渠道：${channel}
🎯 等级：${level} · 每日目标：${goal} 个新词

💡 请在 MEMORY.md 的档案区块把「推送」记为：已开启 ${channel} ${morningDisplay}。
关闭推送：node scripts/push-toggle.js off ${userId}`);
}

function disablePush(userId) {
  userId = sanitizeId(userId, 'userId');
  // cron 名称可由 userId 推导，无需读取档案
  console.log(`__OPENCLAW_CRON_RM__:english-daily-morning-${userId}`);
  console.log(`\n✅ 每日英语推送已关闭（已请求删除 ${userId} 的定时任务）`);
  console.log(`💡 请在 MEMORY.md 的档案区块把「推送」记为：未开启。`);
}

function showStatus(userId) {
  userId = sanitizeId(userId, 'userId');
  console.log(`
📡 推送状态由 MEMORY.md 档案记录 —— 请读取 MEMORY.md 中 <!-- english-daily:profile:${userId} --> 区块的「推送」行查看开启/时间/渠道。
如需重新开启：node scripts/push-toggle.js on ${userId} --level <等级> --goal <目标> [--morning HH:MM] [--channel telegram]`);
}

module.exports = { enablePush, disablePush, showStatus };

// ── CLI entry ─────────────────────────────────────────────────────────────────

if (require.main !== module) return;

const args    = process.argv.slice(2);
const command = args[0];
const userId  = args[1];

if (!command || !userId) {
  console.log(`用法:
  node push-toggle.js on <userId> [--name <姓名>] [--level A1|A2|B1|B2] [--goal <n>] [--morning 08:00] [--channel telegram]
  node push-toggle.js off <userId>
  node push-toggle.js status <userId>

说明:
  档案存于原生 MEMORY.md，由 Agent 维护；开启推送时把等级/每日目标作为参数传入。
  推送触发时，Agent 从 MEMORY.md 读出 SRS 进度再运行 daily-push.js。`);
  process.exit(1);
}

function flag(name) {
  const i = args.indexOf(name);
  return (i !== -1 && args[i + 1] !== undefined) ? args[i + 1] : undefined;
}

const opts = {
  name:    flag('--name'),
  level:   flag('--level'),
  goal:    flag('--goal'),
  morning: flag('--morning'),
  channel: flag('--channel')
};

switch (command) {
  case 'on':     enablePush(userId, opts); break;
  case 'off':    disablePush(userId);      break;
  case 'status': showStatus(userId);       break;
  default:
    console.error(`❌ 未知命令：${command}（支持 on/off/status）`);
    process.exit(1);
}
