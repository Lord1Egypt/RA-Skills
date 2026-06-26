#!/usr/bin/env node
/**
 * daily-mood — morning-push.js
 * 早晨全量寄语推送 — 遍历所有已注册且 pushEnabled=true 的用户，为每人生成寄语 prompt
 * 由 openclaw cron 08:00 每日触发
 *
 * 用法:
 *   node scripts/morning-push.js                    # 全量推送
 *   node scripts/morning-push.js --user <userId>    # 单用户测试
 *   node scripts/morning-push.js --mood <mood>      # 临时覆盖心情（测试用）
 *   node scripts/morning-push.js --dry-run          # 仅输出 prompt，不记录日志
 */

const fs = require('fs');
const path = require('path');

const ALLOWED_MOODS = new Set([
  'happy','sad','anxious','tired','lost','calm','grateful','angry','neutral'
]);

const USERS_DIR = path.join(__dirname, '..', 'data', 'users');
const args = process.argv.slice(2);
const dryRun = args.includes('--dry-run');

const userIdx = args.indexOf('--user');
const targetUser = userIdx !== -1 ? args[userIdx + 1] : null;

const moodOverrideIdx = args.indexOf('--mood');
const rawMoodOverride = moodOverrideIdx !== -1 ? args[moodOverrideIdx + 1] : null;
const moodOverride = rawMoodOverride && ALLOWED_MOODS.has(rawMoodOverride) ? rawMoodOverride : null;

const now = new Date();
const dateStr_zh = `${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日`;
const dateStr_en = now.toLocaleDateString('en-US', { weekday:'long', year:'numeric', month:'long', day:'numeric' });

// Load users
let users = [];
if (targetUser) {
  const fp = path.join(USERS_DIR, `${targetUser.replace(/[^a-zA-Z0-9_-]/g,'')}.json`);
  if (!fs.existsSync(fp)) {
    console.error(`User "${targetUser}" not found. Register first: node scripts/register.js ${targetUser}`);
    process.exit(1);
  }
  users = [JSON.parse(fs.readFileSync(fp, 'utf8'))];
} else {
  if (!fs.existsSync(USERS_DIR)) {
    console.log('No users registered yet. Use: node scripts/register.js <userId>');
    process.exit(0);
  }
  users = fs.readdirSync(USERS_DIR)
    .filter(f => f.endsWith('.json'))
    .map(f => JSON.parse(fs.readFileSync(path.join(USERS_DIR, f), 'utf8')))
    .filter(u => u.pushEnabled !== false);
}

if (users.length === 0) {
  console.log('No active users to push. Register users or enable push first.');
  process.exit(0);
}

// Generate prompt for each user
users.forEach((user, i) => {
  const lang = user.language || 'zh';
  const mood = moodOverride || user.mood || 'neutral';

  const MOOD_TONE_ZH = {
    happy:    '用户今天心情开心愉悦。寄语基调：共鸣这份喜悦，引导珍惜当下，扩大感恩视角。',
    sad:      '用户今天情绪低落。寄语基调：先温柔接纳悲伤（"难过是可以的"），不急于鼓励，给予被看见的感觉，再轻轻引导向前。',
    anxious:  '用户今天焦虑。寄语基调：放慢节奏，把"未来"的巨大变成"此刻"的具体微小，给一点落脚点。不说"别担心"。',
    tired:    '用户今天很疲惫。寄语基调：允许休息，休息本身就是努力的一部分。温柔而坚定地说：你已经做得够多了。',
    lost:     '用户今天感到迷茫。寄语基调：不给"正确答案"，给方向感和陪伴感。迷茫是在生长，不是迷失。',
    calm:     '用户今天平静。寄语基调：深化这份平静，引导觉察当下细微之美，生活里的小丰盈。',
    grateful: '用户今天感恩。寄语基调：呼应感恩，从一件小事延伸到生命本身的珍贵。',
    angry:    '用户今天生气/烦躁。寄语基调：先接纳情绪（"愤怒说明你在乎"），不评判，再引导情绪流动而非压抑。',
    neutral:  '用户今天心情平常。寄语基调：一段温暖、有质感的人生寄语，既不过度激励也不无聊，像一位老朋友说的话。'
  };

  const MOOD_TONE_EN = {
    happy:    "User is feeling happy today. Tone: resonate with their joy, invite them to savour the moment and expand gratitude.",
    sad:      "User is feeling sad. Tone: first acknowledge the sadness gently ('it is okay to feel this'), don't rush to cheering up, make them feel seen, then softly point forward.",
    anxious:  "User is anxious. Tone: slow things down, shrink the overwhelming future into one small concrete present moment. Don't say 'don't worry'.",
    tired:    "User is tired. Tone: give permission to rest. Rest is not laziness — it is part of the effort. Say: you have done enough today.",
    lost:     "User feels lost. Tone: don't give 'the answer', give a sense of direction and companionship. Being lost means you are growing.",
    calm:     "User feels calm. Tone: deepen the stillness, invite noticing the small beauties in the present moment.",
    grateful: "User feels grateful. Tone: echo the gratitude, expand from one small thing to the preciousness of being alive.",
    angry:    "User is angry. Tone: first honour the anger ('anger means you care'), no judgement, then guide the emotion to flow rather than be suppressed.",
    neutral:  "User is in a neutral state. Tone: a warm, textured life message — like a trusted friend talking, not overly motivational, not bland."
  };

  const toneHint = lang === 'en' ? MOOD_TONE_EN[mood] : MOOD_TONE_ZH[mood];
  const dateStr = lang === 'en' ? dateStr_en : dateStr_zh;

  if (i > 0) console.log('\n' + '─'.repeat(60) + '\n');

  if (lang === 'en') {
    console.log(`[Push to user: ${user.userId} | lang: en | mood: ${mood}]

Please write a morning life message for this user.
Date: ${dateStr}
Mood context: ${toneHint}

Requirements:
- Length: 100–150 words of main message body
- Voice: warm, personal, non-preachy — like a thoughtful friend, not a motivational poster
- End with one short distilled line (1 sentence, ≤ 20 words) that could stand alone as a quote
- No generic phrases like "believe in yourself", "every day is a gift", "you got this"
- Grounded in real human experience, not abstract positivity

Output format:
🌅 Good Morning, ${user.userId} · ${dateStr}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Main message — 100-150 words]

✨ Today's thought:
"[The distilled one-liner]"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);

  } else {
    console.log(`[推送给用户：${user.userId} | 语言：zh | 心情：${mood}]

请为该用户写一段早晨人生寄语。
日期：${dateStr}
心情背景：${toneHint}

写作要求：
- 正文长度：100-150字
- 语气：温暖、真实、不说教 — 像一位懂你的朋友，不是励志海报
- 结尾附一句提炼语（不超过20字，可单独成句）
- 避免陈词滥调：不用"加油""相信自己""每一天都是礼物""你最棒"
- 写人真实会经历的处境，不写空洞正能量

输出格式：
🌅 早安，${user.userId} · ${dateStr}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[寄语正文 100-150字]

✨ 今日寄语：
「[提炼语，≤20字]」
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  }
});
