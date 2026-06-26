#!/usr/bin/env node
/**
 * daily-poem — morning-push.js
 * 每日早晨诗词推送 prompt 生成器
 * 由 openclaw cron 08:00 触发
 *
 * 用法:
 *   node scripts/morning-push.js
 *   node scripts/morning-push.js --lang en
 *   node scripts/morning-push.js --theme 离别
 */

const fs = require('fs');
const path = require('path');

const ALLOWED_THEMES = new Set([
  '离别','思乡','爱情','友情','豪情','悲秋','咏春','励志','禅意','月亮',
  '山水','战争','田园','咏物','闺怨','送别','饮酒','怀古',
  'love','autumn','spring','farewell','courage','moon','nature','friendship'
]);

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = (langIdx !== -1 && args[langIdx + 1]) ? args[langIdx + 1] : 'zh';
const themeIdx = args.indexOf('--theme');
const rawTheme = themeIdx !== -1 ? args[themeIdx + 1] : null;
const theme = rawTheme && ALLOWED_THEMES.has(rawTheme) ? rawTheme : null;

const now = new Date();
const day = now.getDay(); // 0=Sun,1=Mon,...6=Sat
const dateISO = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;

// Rotation: Mon/Wed/Fri = classical, Tue/Thu = modern, Sat/Sun = English
const poetryType = (lang === 'en')
  ? 'english'
  : ([1,3,5].includes(day) ? 'classical' : [2,4].includes(day) ? 'modern' : 'english');

// Load push log to avoid repeats
const logPath = path.join(__dirname, '..', 'data', 'push-log.json');
let recentPoems = [];
if (fs.existsSync(logPath)) {
  try {
    const log = JSON.parse(fs.readFileSync(logPath, 'utf8'));
    const cutoff = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
    recentPoems = log
      .filter(e => new Date(e.date) > cutoff)
      .map(e => e.title);
  } catch (_) {}
}

const avoidNote = recentPoems.length
  ? `\n避免重复：近7天已推过以下诗（请勿重选）：${recentPoems.join('、')}`
  : '';

if (lang === 'en') {
  const WEEKDAYS = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  const dateStr = `${WEEKDAYS[day]}, ${MONTHS[now.getMonth()]} ${now.getDate()}, ${now.getFullYear()}`;
  const typeNote = theme ? `Theme: ${theme}` : 'Poetry type: English (public domain)';

  console.log(`Please deliver today's Daily Poem. Date: ${dateStr}
${typeNote}${avoidNote ? avoidNote.replace(/[^\x00-\x7F]/g, '') : ''}

Choose one outstanding English poem (author must have been deceased 70+ years, public domain). ${theme ? `Theme: ${theme}.` : ''}

Output format:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌸 Daily Poem · ${dateStr}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📜 [Title]
✍️  [Author] · [Year/Collection]

[Full poem text — preserve line breaks]

🈶 Chinese Translation:
[Full translation]

📖 Background:
[2-3 sentences on the poet's life context when writing this]

💡 Analysis (2-3 points):
• [Image/technique 1]
• [Image/technique 2]
• [Optional: metre or sound device]

🎙 Recitation note:
[1 sentence on stress pattern or reading pace]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 Reply "more like this" · "query [theme]" · "weekly digest on Sunday"`);

} else {
  const WEEKDAYS_ZH = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
  const dateStr = `${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日 ${WEEKDAYS_ZH[day]}`;

  const typeMap = { classical:'中国古典诗词（唐诗/宋词/元曲）', modern:'中国现代诗（1919年后）', english:'英文诗（公有领域）' };
  const typeHint = theme ? `主题：${theme}` : `今日类型：${typeMap[poetryType]}`;

  console.log(`请为今日推送精选诗词。日期：${dateStr}
${typeHint}${avoidNote}

选择一首符合今日类型的出色诗作，按以下格式完整呈现：

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌸 每日诗词 · ${dateStr}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📜 【诗题】
✍️  作者 · 朝代/年代

【原文】（保留原始格式和换行）

${poetryType === 'classical' ? '🎵 平仄标注：\n【标注版本，用 ○ 标平声，● 标仄声，◎ 标韵脚】\n' : ''}🈶 译文/注释：
【现代汉语释义或英译（若为英文诗则附中译）】

📖 背景故事：
【诗人创作此诗的生平背景，2-3句】

💡 赏析要点（2-3处）：
• 【意象/手法 1】
• 【意象/手法 2】
• 【可选：音韵/结构特点】

🎙 朗读节奏：
【一句话说明朗读节奏或情感基调】

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 回复"再来一首" · "查 [主题/作者]" · 周日晚见合辑`);
}
