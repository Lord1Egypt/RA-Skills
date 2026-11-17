#!/usr/bin/env node
'use strict';
/**
 * CouponClaw — daily deal push subscription (no filesystem writes)
 *
 * Registers/removes a per-user cron job that runs daily-deals.js and delivers the
 * briefing via the OpenClaw runtime. Schedule state lives in the cron job itself
 * (managed by the runtime via the __OPENCLAW_CRON_ADD__/__OPENCLAW_CRON_RM__ protocol);
 * region/lang are baked into the cron message, so nothing is persisted to disk.
 *
 * Usage:
 *   node push-toggle.js on <userId> [--morning HH:MM] [--region cn|us|uk|au|sea|all] [--channel telegram|slack|feishu|discord] [--lang zh|en]
 *   node push-toggle.js off <userId>
 *   node push-toggle.js status <userId>
 */
const path = require('path');
const SKILL = 'couponclaw';
const DEFAULT_MORNING = '09:00';
const ALLOWED_CH = new Set(['telegram', 'slack', 'feishu', 'discord']);
const ALLOWED_REGION = new Set(['cn', 'us', 'uk', 'au', 'sea', 'all']);

function sanitizeId(v) {
  if (typeof v !== 'string' || !/^[a-zA-Z0-9_-]{1,128}$/.test(v)) { console.error('❌ invalid userId'); process.exit(1); }
  return v;
}
function sanitizeTime(v) {
  if (!/^\d{1,2}:\d{2}$/.test(v)) { console.error('❌ invalid --morning (HH:MM)'); process.exit(1); }
  const [h, m] = v.split(':').map(Number);
  if (h > 23 || m > 59) { console.error('❌ invalid --morning (HH:MM)'); process.exit(1); }
  return { h, m };
}

function enablePush(userId, opts) {
  userId = sanitizeId(userId);
  const mt = opts.morning || DEFAULT_MORNING;
  const { h, m } = sanitizeTime(mt);
  const ch = opts.channel || 'telegram';
  if (!ALLOWED_CH.has(ch)) { console.error('❌ unsupported channel: ' + ch); process.exit(1); }
  const region = opts.region || 'all';
  if (!ALLOWED_REGION.has(region)) { console.error('❌ unsupported region: ' + region); process.exit(1); }
  const lang = opts.lang === 'en' ? 'en' : 'zh';
  const sk = `agent:main:${ch}:direct:${userId}`;
  const msg = `node ${path.join(__dirname, 'daily-deals.js')} --region ${region} --lang ${lang}`;
  console.log('__OPENCLAW_CRON_ADD__:' + JSON.stringify({
    name: `${SKILL}-daily-${userId}`, cronExpr: `${m} ${h} * * *`, tz: 'Asia/Shanghai',
    session: 'isolated', sessionKey: sk, channel: ch, to: userId, announce: true, timeoutSeconds: 180, message: msg
  }));
  console.log(`\n✅ ${SKILL} daily deal push enabled\n⏰ ${mt}  🌍 region: ${region}  📡 ${ch}  🌐 ${lang}\n💡 Schedule is held by the cron job; note it in MEMORY.md if you like ("couponclaw push ${ch} ${mt} ${region}").\nDisable: node push-toggle.js off ${userId}`);
}

function disablePush(userId) {
  userId = sanitizeId(userId);
  console.log(`__OPENCLAW_CRON_RM__:${SKILL}-daily-${userId}`);
  console.log(`✅ ${SKILL} daily deal push disabled`);
}

function showStatus(userId) {
  userId = sanitizeId(userId);
  console.log(`\n📡 ${SKILL} — ${userId}\nPush state is held by the cron job: run \`openclaw cron list\` and look for ${SKILL}-daily-${userId}.\n`);
}

if (require.main !== module) return;
const [cmd, uid, ...rest] = process.argv.slice(2);
if (!cmd || !uid) { console.log('Usage: node push-toggle.js on|off|status <userId> [--morning HH:MM] [--region ...] [--channel ...] [--lang zh|en]'); process.exit(1); }
function flag(n) { const i = rest.indexOf(n); return i !== -1 ? rest[i + 1] : undefined; }
const opts = { morning: flag('--morning'), region: flag('--region'), channel: flag('--channel'), lang: flag('--lang') };
if (cmd === 'on') enablePush(uid, opts);
else if (cmd === 'off') disablePush(uid);
else if (cmd === 'status') showStatus(uid);
else { console.error('❌ unknown command: ' + cmd); process.exit(1); }
