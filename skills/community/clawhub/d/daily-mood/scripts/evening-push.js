#!/usr/bin/env node
/**
 * daily-mood — evening-push.js
 * 傍晚全量寄语推送 — 温柔收尾一天，引导好眠
 * 由 openclaw cron 21:00 每日触发
 *
 * 用法:
 *   node scripts/evening-push.js                    # 全量推送
 *   node scripts/evening-push.js --user <userId>    # 单用户测试
 *   node scripts/evening-push.js --mood <mood>      # 临时覆盖心情
 */

const fs = require('fs');
const path = require('path');

const ALLOWED_MOODS = new Set([
  'happy','sad','anxious','tired','lost','calm','grateful','angry','neutral'
]);
const USERS_DIR = path.join(__dirname, '..', 'data', 'users');

const args = process.argv.slice(2);
const userIdx = args.indexOf('--user');
const targetUser = userIdx !== -1 ? args[userIdx + 1] : null;
const moodOverrideIdx = args.indexOf('--mood');
const rawMO = moodOverrideIdx !== -1 ? args[moodOverrideIdx + 1] : null;
const moodOverride = rawMO && ALLOWED_MOODS.has(rawMO) ? rawMO : null;

const now = new Date();
const dateStr_zh = `${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日`;
const dateStr_en = now.toLocaleDateString('en-US', { weekday:'long', month:'long', day:'numeric' });

// Load users
let users = [];
if (targetUser) {
  const fp = path.join(USERS_DIR, `${targetUser.replace(/[^a-zA-Z0-9_-]/g,'')}.json`);
  if (!fs.existsSync(fp)) {
    console.error(`User "${targetUser}" not found.`);
    process.exit(1);
  }
  users = [JSON.parse(fs.readFileSync(fp, 'utf8'))];
} else {
  if (!fs.existsSync(USERS_DIR)) {
    console.log('No users registered yet.');
    process.exit(0);
  }
  users = fs.readdirSync(USERS_DIR)
    .filter(f => f.endsWith('.json'))
    .map(f => JSON.parse(fs.readFileSync(path.join(USERS_DIR, f), 'utf8')))
    .filter(u => u.pushEnabled !== false);
}

if (users.length === 0) {
  console.log('No active users to push.');
  process.exit(0);
}

users.forEach((user, i) => {
  const lang = user.language || 'zh';
  const mood = moodOverride || user.mood || 'neutral';
  const dateStr = lang === 'en' ? dateStr_en : dateStr_zh;

  if (i > 0) console.log('\n' + '─'.repeat(60) + '\n');

  if (lang === 'en') {
    const eveningTones = {
      happy:    "User had a good day. Evening tone: celebrate quietly, invite rest as a gift to tomorrow's self.",
      sad:      "User had a hard day. Evening tone: night is a small closing — tomorrow is a new page. Very gentle, no pressure.",
      anxious:  "User was anxious today. Evening tone: let today go. The body rests even when the mind doesn't — trust the night.",
      tired:    "User is exhausted. Evening tone: softest possible — you don't have to carry today into tomorrow. Just rest.",
      lost:     "User felt lost today. Evening tone: even uncertain days count. You showed up. That is enough.",
      calm:     "User was calm today. Evening tone: deepen the stillness, invite a peaceful night.",
      grateful: "User felt grateful. Evening tone: close the day in gratitude, a small blessing before sleep.",
      angry:    "User was angry today. Evening tone: let the day end, release what no longer needs to be held tonight.",
      neutral:  "User had an ordinary day. Evening tone: find the small worthwhile thing in an ordinary day."
    };
    console.log(`[Evening push to: ${user.userId} | lang: en | mood: ${mood}]

Please write an evening message to gently close this user's day.
Date: ${dateStr}
Mood context: ${eveningTones[mood]}

Requirements:
- Length: 80–120 words
- Softer and quieter than the morning message — the tone should slow down
- Do NOT give advice or tasks for tomorrow
- End with a short, calm goodnight line (≤ 15 words)

Output format:
🌙 Good Evening, ${user.userId} · ${dateStr}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Evening message — 80-120 words]

🕯️ "[A soft goodnight line — 15 words or fewer]"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);

  } else {
    const eveningTones_zh = {
      happy:    '用户今天过得很开心。傍晚基调：安静地庆祝，让开心沉淀，把今天的好留给明天的自己。',
      sad:      '用户今天情绪低落。傍晚基调：夜晚是一个小小的收束，明天是新的一页。极轻柔，不施加压力。',
      anxious:  '用户今天焦虑。傍晚基调：让今天过去。身体在睡眠中会修复焦虑——交托给夜晚。',
      tired:    '用户今天非常疲惫。傍晚基调：最温柔的一段——不需要把今天带进明天，只是休息。',
      lost:     '用户今天感到迷茫。傍晚基调：就算不确定的一天也算数。你出现了，这就够了。',
      calm:     '用户今天平静。傍晚基调：深化宁静，引导平和入睡。',
      grateful: '用户今天感恩。傍晚基调：用一点感谢收尾这一天，睡前的小小祝福。',
      angry:    '用户今天生气。傍晚基调：让这一天结束，放下今晚不再需要承载的东西。',
      neutral:  '用户今天普通平常。傍晚基调：在平凡一天里找到那件值得的小事。'
    };
    console.log(`[傍晚推送给：${user.userId} | 语言：zh | 心情：${mood}]

请为该用户写一段傍晚寄语，温柔收尾今天。
日期：${dateStr}
心情背景：${eveningTones_zh[mood]}

写作要求：
- 正文长度：80-120字
- 比早晨寄语更轻、更慢、更安静
- 不给明天的建议或任务
- 结尾一句晚安短语（不超过15字）

输出格式：
🌙 晚安，${user.userId} · ${dateStr}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[傍晚寄语 80-120字]

🕯️「[晚安短语，≤15字]」
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  }
});
