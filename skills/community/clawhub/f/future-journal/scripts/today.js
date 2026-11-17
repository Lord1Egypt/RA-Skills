#!/usr/bin/env node
// 今天该写哪一句 —— 未来日记
// 用法:
//   node scripts/today.js 2026-09-17          以该日期为第 1 天，算到今天
//   node scripts/today.js 2026-09-17 --day 8  直接指定第几天
//   node scripts/today.js --day 8             不带起始日，仅按第几天取句
//
// 用途：不开页面也能知道今天要描哪一句 —— 适合写在实体本子上。
//
// 语言范围 / Language scope：
// 默认简体中文（zh-CN）——句库源自页面里的中文原创句库，命令行输出同为中文。
// 英文说明随包提供（skill-card.md）；这里输出的日期/天数是语言无关的，
// 用户书写内容不限语言（中英文皆可）。如需其他语言的句库可向作者提出。
// Default locale: Simplified Chinese (zh-CN). English documentation ships with the
// skill; the day/date output here is locale-independent and user entries are not
// language-restricted. Other prompt-library languages are available on request.

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
let startDate = null;
let forcedDay = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--day') { forcedDay = parseInt(args[++i], 10); }
  else if (!startDate) { startDate = args[i]; }
}

const htmlPath = path.join(__dirname, '..', 'assets', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const m = html.match(/<script id="prompt-data"[^>]*>([\s\S]*?)<\/script>/);
if (!m) { console.log('找不到引导句数据，请确认 assets/index.html 完整'); process.exit(1); }
const data = JSON.parse(m[1]);

const TOTAL = 49;

function pad(n) { return String(n).length < 2 ? '0' + n : String(n); }
function todayIso() { const d = new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
function diffDays(a, b) {
  const A = a.split('-').map(Number), B = b.split('-').map(Number);
  return Math.round((Date.UTC(B[0], B[1] - 1, B[2]) - Date.UTC(A[0], A[1] - 1, A[2])) / 86400000);
}

let day;
if (forcedDay) day = forcedDay;
else if (startDate) day = diffDays(startDate, todayIso()) + 1;
else { console.log('需要起始日期或 --day 参数。'); console.log('例: node scripts/today.js ' + todayIso()); process.exit(1); }

if (day < 1) {
  console.log('这一轮还没开始 —— 起始日是 ' + startDate + '，距今还有 ' + (1 - day) + ' 天。');
  process.exit(0);
}

if (day > TOTAL) {
  console.log('这一轮 49 天已经走完了（今天是第 ' + day + ' 天）。');
  console.log('想再来一轮，在页面的「设置」里重新开始。');
  process.exit(0);
}

const week = Math.ceil(day / 7);
const w = data.weeks[week - 1];
const text = w.prompts[(day - 1) % 7];

console.log('');
console.log('  第 ' + day + ' 天 / 49    ·    第 ' + week + ' 周 · ' + w.theme);
console.log('  这一周在练：' + w.focus);
console.log('');
console.log('  今天描这一句：');
console.log('');
console.log('    ' + text);
console.log('');
console.log('  描完再用过去时写下今天希望发生的一件事，句末带个心情。');
console.log('');
