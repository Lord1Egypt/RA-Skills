#!/usr/bin/env node
/**
 * daily-poem — query.js
 * 按需查诗：按心情/季节/主题/作者/体裁查询并呈现诗词
 *
 * 用法:
 *   node scripts/query.js <keyword>
 *   node scripts/query.js "李白"
 *   node scripts/query.js "秋天" --lang zh
 *   node scripts/query.js rain --lang en
 *   node scripts/query.js --random
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = (langIdx !== -1 && args[langIdx + 1]) ? args[langIdx + 1] : 'zh';
const isRandom = args.includes('--random');

// Sanitize keyword: strip special chars, limit length
const rawKeyword = args.filter(a => a !== '--lang' && a !== lang && a !== '--random')[0] || '';
const keyword = rawKeyword.replace(/[<>"';&|`$]/g, '').trim().substring(0, 50);

if (!keyword && !isRandom) {
  console.error('Usage: node scripts/query.js <keyword|author|theme>');
  console.error('       node scripts/query.js --random');
  console.error('Examples:');
  console.error('  node scripts/query.js 秋天');
  console.error('  node scripts/query.js 李白');
  console.error('  node scripts/query.js farewell --lang en');
  process.exit(1);
}

const now = new Date();
const dateISO = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;

if (lang === 'en') {
  const q = isRandom ? 'a random poem' : `poems about "${keyword}"`;
  console.log(`Please find and present a poem matching: ${q}
Date: ${dateISO}

Selection criteria:
- If it's an author name: choose a well-known work by that author
- If it's a theme/mood: choose the most emotionally resonant poem on that theme
- Prefer public domain works (author deceased 70+ years)
- If no exact match, choose the closest thematic fit and note the connection

Output format:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Poetry · "${isRandom ? 'random' : keyword}"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📜 [Title]
✍️  [Author] · [Year]

[Full poem — preserve line breaks]

🈶 Chinese translation:
[Full translation]

📖 Why this poem fits "${isRandom ? 'today' : keyword}":
[1-2 sentences]

💡 Key images/techniques:
• [Point 1]
• [Point 2]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 Reply "more [theme]" for similar poems`);

} else {
  const q = isRandom ? '随机一首' : `与"${keyword}"相关的诗词`;
  console.log(`请查找并呈现${q}。
日期：${dateISO}

选诗标准：
- 若为作者名：选该作者最具代表性的一首
- 若为主题/心情：选情感最贴切、意境最深远的一首
- 优先中国古典/现代诗；若关键词明显指向英文（如 rain、love），可选英文诗
- 若无精确匹配，选最接近主题的诗，并说明关联

输出格式：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 诗词查询 · "${isRandom ? '随机' : keyword}"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📜 【诗题】
✍️  作者 · 朝代/年代

【原文】

🈶 译文/注释：
【现代汉语释义】

📖 与"${isRandom ? '今日' : keyword}"的关联：
【1-2句说明选诗理由】

💡 赏析要点：
• 【要点 1】
• 【要点 2】

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 回复"更多[主题]" 获取同类诗词`);
}
