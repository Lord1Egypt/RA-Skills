#!/usr/bin/env node
// 门禁⑥：断语可达性（固定网格 + 极端样例盘）
//
// 为什么需要它：audit_hit_distribution.js 用的是"随机盘"，极端格局（专旺/从格）在随机样本里几乎必然 0 命中，
// 于是"库里写了、用户永远看不到"的规则没有任何门禁拦截。
// 2026-10-11 实测：pattern_专旺_水 根本不存在（而润下格恰恰是最常见的专旺形态，48 个专旺样例里 36 个是水）；
// 4 条专旺细分规则在 3.9 万盘网格中 0 命中，直到换了统计维度才暴露。
//
// 判定：主引擎可评估的规则，必须在"网格 ∪ 极端样例盘"里至少命中一次；否则失败。
//   · 空 condition 的模板类规则（大运/流年/流月/流日/合婚/六亲，由面板按 id 触发）跳过，另行统计
//   · EXTREME_WHITELIST：实测极端罕见、网格不可达但检测逻辑已人工核对的规则，在此明示豁免
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '..', 'ui', 'index.html'), 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.error('未找到 <script> 块'); process.exit(1); }
const stub = 'var document={getElementById:()=>({value:"",innerHTML:"",style:{},classList:{add(){},remove(){}}}),querySelectorAll:()=>[]};var alert=()=>{};';
eval(stub + m[1] + ';globalThis.paipan=paipan;globalThis.matchRules=matchRules;globalThis.RULES=RULES;');

// ---- 极端样例盘（v1.3.11 实测可复现，用于覆盖随机/网格样本拿不到的格局）----
const FIXTURES = [
  { label: '专旺·木（曲直格）', y: 1938, mo: 3, d: 23, hh: 21, mi: 41, sex: '男' },
  { label: '专旺·火（炎上格）', y: 1977, mo: 6, d: 18, hh: 18, mi: 41, sex: '男' },
  { label: '专旺·土（稼穑格）', y: 1979, mo: 5, d: 1, hh: 12, mi: 41, sex: '男' },
  { label: '专旺·水（润下格）', y: 1948, mo: 11, d: 23, hh: 0, mi: 17, sex: '男' },
];

// 实测：244,608 盘深搜（1930-2020 × 寅卯/巳午/申酉 × 全日期 × 8 时辰）中 0 命中；
// 检测逻辑在 build_ui.py 的 专旺格 分支（阈值 maxWx>65% 且 异行≤15% 且 主导行==日主五行）中已人工核对。
const EXTREME_WHITELIST = new Set([
  'pattern_专旺_金',   // 金专旺（从革格）：24.4 万盘深搜 0 命中，属极端罕见
  'pattern_从杀_透印', // 从杀格 + 正印：39,312 盘网格 1 命中（从格要求帮扶<18%，与"印透"高度互斥）
]);

const hits = {};
let charts = 0;
function feed(chart) {
  if (!chart) return;
  charts++;
  const cats = matchRules(chart);
  for (const cat in cats) for (const r of cats[cat]) hits[r.id] = (hits[r.id] || 0) + 1;
}

const t0 = Date.now();
// 网格：1950-2018 步长 1（含闰/平年、全月份）+ 每月 3 个日期 × 每日 3 个时辰 × 男女
for (let y = 1950; y <= 2018; y++) {
  for (let mo = 1; mo <= 12; mo++) {
    for (const d of [3, 17, 28]) {
      for (const hh of [1, 11, 21]) {
        for (const sex of ['男', '女']) {
          feed(paipan('R', sex, y, mo, d, hh, 17, '', 'no'));
        }
      }
    }
  }
}
const gridN = charts;
for (const f of FIXTURES) feed(paipan('F', f.sex, f.y, f.mo, f.d, f.hh, f.mi, '', 'no'));

console.log(`网格 ${gridN} 盘 + 极端样例 ${FIXTURES.length} 盘，用时 ${((Date.now() - t0) / 1000).toFixed(1)}s`);

const panel = [];      // 面板按 id 触发：空 condition，或 condition 含 流年/流月/流日/合婚 键
const skippedWhite = [];
const unreachable = [];
const ok = [];
// matchRules 对以下键显式置 hit=false（见 build_ui.py matchRules：时序类断语只由 runLiuNian/runLiuYue/runLiuDay/合婚面板输出）
const PANEL_KEYS = ['流年', '流月', '流日', '合婚'];
RULES.forEach(r => {
  const c = r.condition || {};
  const keys = Object.keys(c);
  if (hits[r.id]) { ok.push(r.id); return; }
  if (keys.length === 0 || keys.some(k => PANEL_KEYS.includes(k))) { panel.push(r.id); return; }
  if (EXTREME_WHITELIST.has(r.id)) { skippedWhite.push(r.id); return; }
  unreachable.push(r);
});

console.log(`全部规则 ${RULES.length} 条 → 主引擎命中 ${ok.length} / 面板触发类 ${panel.length} / 白名单豁免 ${skippedWhite.length} / 判定不可达 ${unreachable.length}`);
console.log('（面板触发类：由 runLiuNian/runLiuYue/runLiuDay/合婚 面板按 id 渲染，主引擎不输出；已由 verify_sleep_rules.js / verify_ux_e2e.js 覆盖）');
if (skippedWhite.length) console.log('（白名单豁免：' + skippedWhite.join(', ') + ' —— 极端罕见，依据见脚本内注释）');

if (unreachable.length) {
  console.log('\n❌ 判定不可达的规则（网格与极端样例盘均 0 命中）:');
  unreachable.forEach(r => console.log(`   ${r.id} [${r.category}] cond=${JSON.stringify(r.condition)} → ${(r.conclusion || '').substring(0, 60)}`));
  console.log('\n处置：① 修 condition（多半是键值写错/条件互斥）② 补极端样例盘 ③ 若确属极端罕见，加入 EXTREME_WHITELIST 并写明依据');
  process.exit(1);
}
console.log('\n✅ 全部可评估规则均可达（或已在白名单中明示豁免）');
process.exit(0);
