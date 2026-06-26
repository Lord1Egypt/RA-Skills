#!/usr/bin/env node
/**
 * daily-poem — weekly-digest.js
 * 每周日晚间推送本周 7 首诗词合辑
 * 由 openclaw cron 周日 20:00 触发
 *
 * 用法:
 *   node scripts/weekly-digest.js
 *   node scripts/weekly-digest.js --lang en
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = (langIdx !== -1 && args[langIdx + 1]) ? args[langIdx + 1] : 'zh';

const now = new Date();
// Calculate the Monday of this week
const monday = new Date(now);
monday.setDate(now.getDate() - ((now.getDay() + 6) % 7));
const mondayISO = `${monday.getFullYear()}-${String(monday.getMonth()+1).padStart(2,'0')}-${String(monday.getDate()).padStart(2,'0')}`;
const sundayISO = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;

// Load push log to reference this week's poems if available
const logPath = path.join(__dirname, '..', 'data', 'push-log.json');
let weekPoems = [];
if (fs.existsSync(logPath)) {
  try {
    const log = JSON.parse(fs.readFileSync(logPath, 'utf8'));
    weekPoems = log.filter(e => e.date >= mondayISO && e.date <= sundayISO);
  } catch (_) {}
}

const poemRef = weekPoems.length > 0
  ? `本周已记录推送：${weekPoems.map(p => p.title).join('、')}（可直接复用，补全未记录的）`
  : '本周推送记录不可用，请自选7首优质诗词';

if (lang === 'en') {
  console.log(`Please create this week's poetry digest (${mondayISO} to ${sundayISO}).

Reference: ${poemRef.replace(/[\u4e00-\u9fff]/g, '')}
Select 7 poems total: 3 classical Chinese, 2 modern Chinese, 2 English (public domain).
Find a common theme or thread connecting at least 4 of the 7 poems.

Output format:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 Weekly Poetry Digest · ${mondayISO} – ${sundayISO}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌟 This Week's Theme: [theme in 4-6 words]

[Repeat 7 times:]
──────────── Day N (Weekday) ────────────
📜 [Title] · [Author] · [Dynasty/Year]
[First 2-4 lines of poem]
💬 [One sentence why it fits this week]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Week in Review:
[2-3 sentences on the emotional arc of this week's selection]

See you next Monday! 🌸`);

} else {
  console.log(`请生成本周诗词合辑（${mondayISO} 至 ${sundayISO}）。

参考：${poemRef}
共选 7 首：古典诗词 3 首、现代诗 2 首、英文诗 2 首（公有领域）。
尝试找出贯穿其中 4 首以上的共同主题或情感线索。

输出格式：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 本周诗词合辑 · ${mondayISO} – ${sundayISO}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌟 本周主题：【4-6字主题词】

【重复7次：】
──────────── 第N天（周X）────────────
📜 【诗题】 · 【作者】 · 【朝代/年代】
【诗歌前2-4行】
💬 【一句话说明与本周主题的关联】

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 本周回顾：
【2-3句话，总结本周诗词的情感脉络】

下周一见！🌸`);
}
