#!/usr/bin/env node
/**
 * daily-mood — mood-response.js
 * 用户报告当下心情后，即时返回匹配寄语 prompt
 *
 * 用法:
 *   node scripts/mood-response.js <mood> [--lang zh|en] [--userId <id>]
 *   node scripts/mood-response.js anxious
 *   node scripts/mood-response.js happy --lang en
 *   node scripts/mood-response.js tired --userId alice
 *
 * mood 可以是英文关键词，也可以传入中文（会自动映射）：
 *   开心/高兴/快乐 → happy
 *   低落/难过/伤心/不开心 → sad
 *   焦虑/紧张/担心/害怕 → anxious
 *   疲惫/累/很累/累了 → tired
 *   迷茫/不知道/困惑 → lost
 *   平静/还好/一般 → calm
 *   感恩/感谢/开心感激 → grateful
 *   生气/愤怒/烦/烦躁 → angry
 */

const fs = require('fs');
const path = require('path');

const MOOD_MAP_ZH = {
  '开心':'happy','高兴':'happy','快乐':'happy','很好':'happy',
  '低落':'sad','难过':'sad','伤心':'sad','不开心':'sad','哭':'sad',
  '焦虑':'anxious','紧张':'anxious','担心':'anxious','害怕':'anxious','慌':'anxious',
  '疲惫':'tired','累':'tired','很累':'tired','累了':'tired','没劲':'tired',
  '迷茫':'lost','不知道':'lost','困惑':'lost','不确定':'lost',
  '平静':'calm','还好':'calm','一般':'calm','平和':'calm',
  '感恩':'grateful','感谢':'grateful','感激':'grateful',
  '生气':'angry','愤怒':'angry','烦':'angry','烦躁':'angry','火':'angry'
};

const ALLOWED_MOODS_EN = new Set([
  'happy','sad','anxious','tired','lost','calm','grateful','angry','neutral'
]);

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const langArg = langIdx !== -1 ? args[langIdx + 1] : null;
const userIdIdx = args.indexOf('--userId');
const userId = userIdIdx !== -1 ? args[userIdIdx + 1] : null;

const rawMood = args.filter(a => !a.startsWith('--') && a !== langArg && a !== userId)[0] || '';
if (!rawMood) {
  console.error('Usage: node scripts/mood-response.js <mood> [--lang zh|en] [--userId <id>]');
  console.error('');
  console.error('English moods: happy, sad, anxious, tired, lost, calm, grateful, angry, neutral');
  console.error('Chinese moods: 开心, 低落, 焦虑, 疲惫, 迷茫, 平静, 感恩, 生气, 还好 ...');
  process.exit(1);
}

// Resolve mood
let mood = MOOD_MAP_ZH[rawMood] || (ALLOWED_MOODS_EN.has(rawMood) ? rawMood : null);
if (!mood) {
  // Fuzzy: check if rawMood contains any zh key
  for (const [key, val] of Object.entries(MOOD_MAP_ZH)) {
    if (rawMood.includes(key)) { mood = val; break; }
  }
}
if (!mood) mood = 'neutral';

// Determine language
let lang = 'zh';
if (langArg === 'en') {
  lang = 'en';
} else if (userId) {
  const USERS_DIR = path.join(__dirname, '..', 'data', 'users');
  const fp = path.join(USERS_DIR, `${userId.replace(/[^a-zA-Z0-9_-]/g,'')}.json`);
  if (fs.existsSync(fp)) {
    const u = JSON.parse(fs.readFileSync(fp, 'utf8'));
    lang = u.language || 'zh';
    // Update user's mood in profile
    u.mood = mood;
    u.updatedAt = new Date().toISOString();
    fs.writeFileSync(fp, JSON.stringify(u, null, 2));
  }
}

const now = new Date();
const dateStr = lang === 'en'
  ? now.toLocaleDateString('en-US', { weekday:'long', month:'long', day:'numeric' })
  : `${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日`;

const MOOD_CONTEXT_ZH = {
  happy:    '用户此刻开心愉悦。寄语：共鸣这份喜悦，引导珍惜，不过度煽情。',
  sad:      '用户此刻情绪低落。先温柔承接悲伤，让他/她感到被看见，再轻轻引向光。',
  anxious:  '用户此刻焦虑。把"未来"化为"此刻"，提供一个小小落脚点。不说"别担心"。',
  tired:    '用户此刻疲惫。允许休息，此刻不需要解决任何问题，只是稍作停歇。',
  lost:     '用户此刻迷茫。给陪伴和方向感，不给"正确答案"。迷茫本身是在生长。',
  calm:     '用户此刻平静。深化这份宁静，引导觉察身边细微之美。',
  grateful: '用户此刻感恩。呼应感恩，从一件小事扩展到生命本身的丰盈。',
  angry:    '用户此刻生气/烦躁。先接纳情绪，不评判，再引导情绪流动。',
  neutral:  '用户此刻心情普通。一段有质感的人生寄语，温暖而真实。'
};

const MOOD_CONTEXT_EN = {
  happy:    "User is feeling happy right now. Resonate with the joy, invite savoring, don't over-sentimentalize.",
  sad:      "User is feeling sad. First hold the sadness gently, make them feel seen, then softly point toward light.",
  anxious:  "User is anxious right now. Bring the overwhelming future into one small present moment. Don't say 'don't worry'.",
  tired:    "User is exhausted. Give permission to stop. Nothing needs solving right now — just a brief rest.",
  lost:     "User feels lost. Offer companionship and a sense of direction, not 'the answer'. Being lost is growth.",
  calm:     "User is calm. Deepen the stillness, invite noticing small present-moment beauty.",
  grateful: "User feels grateful. Echo the gratitude, expand from one thing to the richness of being alive.",
  angry:    "User is angry. First honour the emotion, no judgement, then guide it to flow.",
  neutral:  "User is in a neutral state. A textured, warm life message — real, not bland."
};

const ctx = lang === 'en' ? MOOD_CONTEXT_EN[mood] : MOOD_CONTEXT_ZH[mood];
const userName = userId || (lang === 'en' ? 'you' : '你');

if (lang === 'en') {
  console.log(`[Mood response | user: ${userName} | mood: ${mood} | lang: en | ${dateStr}]

Please write an immediate mood-response message.
Mood context: ${ctx}

Requirements:
- Length: 100–150 words
- Voice: like a wise, warm friend who truly gets it — not a therapist, not a coach
- One specific, concrete image or metaphor (not abstract platitudes)
- End with one distilled line (≤ 20 words)
- Do NOT use: "believe in yourself", "you got this", "everything happens for a reason"

Output format:
💬 Hey ${userName} · ${dateStr}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Message body — 100-150 words]

✨ "[Distilled line — 20 words or fewer]"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);

} else {
  console.log(`[心情响应 | 用户：${userName} | 心情：${mood} | 语言：zh | ${dateStr}]

请写一段即时心情响应寄语。
心情背景：${ctx}

写作要求：
- 正文长度：100-150字
- 语气：像一个真正懂你的朋友——不是心理咨询师，不是励志导师
- 包含一个具体、真实的意象或比喻（不要空洞抽象）
- 结尾一句提炼语（不超过20字）
- 禁止使用：加油、相信自己、你最棒、一切都会好的、这都是天意

输出格式：
💬 ${userName} · ${dateStr}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[寄语正文 100-150字]

✨「[提炼语，≤20字]」
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
}
