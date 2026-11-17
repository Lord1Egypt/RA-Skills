#!/usr/bin/env node
// 引导句质量闸门 —— 未来日记
// 用法: node scripts/check-prompts.js [path/to/index.html]
// 退出码 0 = 通过, 1 = 有问题
//
// 为什么要这个脚本：
// 引导句是这套方法里唯一真正的原创资产，也是最容易写坏的地方。
// 中文没有时态标记，靠肉眼检查「是不是过去时」非常不可靠 —— 所以把
// 规则写成硬检查：禁止将来时标志词 + 必须带情绪词。改句库后跑一遍。
//
// 语言范围 / Language scope：
// 默认简体中文（zh-CN）——本脚本检查的是中文特有的时态词汇（「会」「将」「打算」
// 等将来时标志词）与中文情绪词的搭配，判定结果只对中文引导句有效。
// 英文说明随包提供（skill-card.md）；**用户书写内容不限语言**（中英文皆可），
// 该规则集只作用于句库校验，不限制用户写什么。需要其他语言的句库可向作者提出。
// Default locale: Simplified Chinese (zh-CN). The rules below validate the bundled
// Chinese prompt library only; English documentation ships with the skill and user
// entries are not language-restricted. Other prompt-library languages on request.

const fs = require('fs');
const path = require('path');

const target = process.argv[2] || path.join(__dirname, '..', 'assets', 'index.html');
const html = fs.readFileSync(target, 'utf8');

let fail = 0;
const err = (m) => { console.log('  FAIL  ' + m); fail++; };
const ok = (m) => console.log('  OK    ' + m);

const m = html.match(/<script id="prompt-data"[^>]*>([\s\S]*?)<\/script>/);
if (!m) { console.log('FAIL: 在 ' + target + ' 里找不到引导句 JSON 块'); process.exit(1); }

let data;
try { data = JSON.parse(m[1]); } catch (e) { console.log('FAIL: JSON 解析失败 — ' + e.message); process.exit(1); }

// 将来时标志词。只匹配真正的祈愿句式 ——「想要的生活」「想要的东西」是名词化
// 用法，不算将来时，早期版本把「想要」单列导致误报，别再改回去。
const FUTURE = ['但愿', '如果能', '希望能', '我希望', '我想要', '我期待', '一定要', '将会', '我会变得', '争取能'];
// 情绪词：句末要带一个表达感受的词
const EMO = ['好', '静', '满足', '暖', '得意', '亮', '喜欢', '舒服', '感谢', '踏实', '清醒', '松',
  '安心', '高兴', '满意', '有底', '开心', '稳', '惊喜', '感恩', '底气', '笃定', '感动', '满',
  '甜', '轻松', '笑', '自在', '幸福', '幸运', '痛快', '精彩', '顺', '值得'];
const MAXLEN = 30;

console.log('== 结构 ==');
if (data.weeks.length === 7) ok('7 周');
else err('周数应为 7，实际 ' + data.weeks.length);

const all = [];
data.weeks.forEach((w, i) => {
  if (w.prompts.length !== 7) err('第 ' + (i + 1) + ' 周应为 7 句，实际 ' + w.prompts.length);
  if (!w.theme) err('第 ' + (i + 1) + ' 周缺主题名');
  w.prompts.forEach((p) => all.push({ week: i + 1, text: p }));
});
if (all.length === 49) ok('共 49 句');
else err('总句数应为 49，实际 ' + all.length);

console.log('== 内容 ==');
const seen = new Map();
all.forEach((it) => {
  const key = it.text.trim();
  if (seen.has(key)) err('第 ' + it.week + ' 周重复句: ' + key);
  seen.set(key, true);
  if (seen.size === all.length) ok('无重复句');
});

const fHit = all.filter((it) => FUTURE.some((w) => it.text.includes(w)));
if (fHit.length === 0) ok('无将来时标志词（全部为过去时语感）');
else fHit.forEach((it) => err('第 ' + it.week + ' 周含将来时「' + FUTURE.find((w) => it.text.includes(w)) + '」: ' + it.text));

const eMiss = all.filter((it) => !EMO.some((w) => it.text.includes(w)));
if (eMiss.length === 0) ok('全部句末带情绪词');
else eMiss.forEach((it) => err('第 ' + it.week + ' 周缺情绪词: ' + it.text));

const lng = all.filter((it) => it.text.length > MAXLEN);
if (lng.length === 0) ok('全部单句 ≤ ' + MAXLEN + ' 字');
else lng.forEach((it) => err('第 ' + it.week + ' 周过长(' + it.text.length + '字): ' + it.text));

console.log('');
if (fail === 0) { console.log('=== 通过，句库可以发布 ==='); process.exit(0); }
console.log('=== ' + fail + ' 项需要处理 ===');
process.exit(1);
