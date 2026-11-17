#!/usr/bin/env node
// 门禁⑤：同类别 + 同 condition 的多规则检测（近重复 / 互斥结论）
//
// 为什么需要它：现有三道门禁的盲区——
//   · audit_hit_distribution.js 只看命中率（100% / >80%），50% 命中但"每次都成对出现"的互斥规则抓不到；
//   · check_conflicts.js 只看显式反义规则对；
//   · check_dup_hits.js 只看同文案重复。
// 2026-10-11 实测就漏掉了：yongshen_寒月 与 yongshen_暑月 共用 状态:"调候"，
// 在 50.1% 的命盘上同时命中 → 每张寒/暑月盘都输出一条与自己命局相反的调候断语（v1.3.11 已修）。
//
// 判定：
//   ❌ 同组内两条结论相似度 ≥ 0.60 → 近重复（同盘必同时输出两条近似话术）
//   ❌ 同组内"寒 / 暑"（冷热）结论互斥对 → 必有一条与命局相反
//   ⚠️ 相似度 0.40~0.60 → 建议复核（不失败）
// 空 condition 的模板类规则（由 runLiuNian/runLiuYue/runLiuDay/合婚 面板按 id 触发）不参与分组。
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '..', 'ui', 'index.html'), 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.error('未找到 <script> 块'); process.exit(1); }
const stub = 'var document={getElementById:()=>({value:"",innerHTML:"",style:{},classList:{add(){},remove(){}}}),querySelectorAll:()=>[]};var alert=()=>{};';
eval(stub + m[1] + ';globalThis.RULES=RULES;');

// 字符二元组 Dice 相似度
function bigrams(s) {
  const t = s.replace(/[\s，。；：、（）()【】《》\-—]/g, '');
  const g = [];
  for (let i = 0; i < t.length - 1; i++) g.push(t.slice(i, i + 2));
  return g;
}
function dice(a, b) {
  const ga = bigrams(a), gb = bigrams(b);
  if (!ga.length || !gb.length) return 0;
  const setB = new Map();
  gb.forEach(g => setB.set(g, (setB.get(g) || 0) + 1));
  let inter = 0;
  ga.forEach(g => { const n = setB.get(g) || 0; if (n > 0) { inter++; setB.set(g, n - 1); } });
  return (2 * inter) / (ga.length + gb.length);
}

const COLD = /寒|冷|冬|湿|亥|子|丑/;
const HOT = /暑|热|夏|燥|巳|午|未/;

const groups = new Map();
RULES.forEach(r => {
  const c = r.condition || {};
  if (Object.keys(c).length === 0) return;           // 模板类，面板按 id 触发
  const sorted = {};
  Object.keys(c).sort().forEach(k => { sorted[k] = c[k]; });
  const key = r.category + ' || ' + JSON.stringify(sorted);
  if (!groups.has(key)) groups.set(key, []);
  groups.get(key).push(r);
});

let fatal = 0, warn = 0, checked = 0;
const near = [], opposite = [], soft = [];
for (const [key, rs] of groups) {
  if (rs.length < 2) continue;
  checked++;
  for (let i = 0; i < rs.length; i++) {
    for (let j = i + 1; j < rs.length; j++) {
      const a = rs[i], b = rs[j];
      const ta = (a.conclusion || '') + (a.suggestion || '');
      const tb = (b.conclusion || '') + (b.suggestion || '');
      const sim = dice(ta, tb);
      if (sim >= 0.60) { near.push({ key, a: a.id, b: b.id, sim }); fatal++; }
      else if (sim >= 0.40) { soft.push({ key, a: a.id, b: b.id, sim }); warn++; }
      const ac = COLD.test(ta), ah = HOT.test(ta), bc = COLD.test(tb), bh = HOT.test(tb);
      if ((ac && !ah && bc && !bh) || (ah && !ac && bh && !bc) || (ac && !ah && bh && !bc) || (ah && !ac && bc && !bh)) {
        // 真正互斥：一方只谈寒、另一方只谈暑（互反）
        if ((ac && !ah && bh && !bc) || (ah && !ac && bc && !bh)) {
          opposite.push({ key, a: a.id, b: b.id });
          fatal++;
        }
      }
    }
  }
}

console.log(`同条件多规则组: ${checked} 组（不含空 condition 模板类）`);
if (opposite.length) {
  console.log('\n❌ 互斥结论（同条件必然同时命中，必有一条与命局相反）:');
  opposite.forEach(o => console.log(`   [${o.key}]  ${o.a}  ×  ${o.b}`));
}
if (near.length) {
  console.log('\n❌ 近重复结论（相似度 ≥ 0.60，同盘输出两条近似话术）:');
  near.forEach(o => console.log(`   [${o.key}]  ${o.a}  ×  ${o.b}  sim=${o.sim.toFixed(2)}`));
}
if (soft.length) {
  console.log('\n⚠️  建议复核（相似度 0.40~0.60，可能是互补，也可能是重复）:');
  soft.sort((x, y) => y.sim - x.sim).forEach(o => console.log(`   [${o.key}]  ${o.a}  ×  ${o.b}  sim=${o.sim.toFixed(2)}`));
}
if (fatal === 0) console.log('\n✅ 无互斥 / 无近重复同条件规则（建议复核项 ' + warn + ' 条为信息级）');
else console.log(`\n❌ 门禁未过：互斥 ${opposite.length} 对 / 近重复 ${near.length} 对`);
process.exit(fatal === 0 ? 0 : 1);
