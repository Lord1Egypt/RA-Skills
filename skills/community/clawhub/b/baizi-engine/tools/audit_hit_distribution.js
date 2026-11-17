#!/usr/bin/env node
// 断语库大样本命中分布审查工具（全类别覆盖版）
// 用法：
//   node audit_hit_distribution.js                 # 默认 300 盘、固定种子 42（可复现）
//   node audit_hit_distribution.js --sample=2000   # 自定义样本数
//   node audit_hit_distribution.js --seed=random   # 换一批样本（默认固定种子，保证 CI 可复现）
//   node audit_hit_distribution.js --rules=combo_全无财星,pattern_tiaohou  # 深挖指定规则
//   node audit_hit_distribution.js --cat=性格,财运  # 只看指定类别
//
// 判定标准（2026-10-14 v1.3.16 修订，原因见下）：
//   - 命中率【100%】的规则 = 坏规则（条件过宽/字段引用错误/存在性判断代替真实判断），**失败**
//   - 命中率【≥90%】= 几乎必然无条件，**失败**
//   - 命中率【80%~90%】= 需人工复核，**仅警告，不失败**
//   - 单盘 0 命中属正常（低命中规则见"样本内 0 命中"一节，大样本仍 0 才需深挖）
//
// 【为什么把 >80% 从"失败"降级为"警告"】原实现对**点估计**硬卡 80% 就 exit 1，
//   而 n=80、随机种子时，一条真实命中率 73% 的规则（career_用神被冲 / pattern_yongshen_chong，
//   n=2000 实测 1464/2000 = 73%）有约 8% 概率在样本里显示 >80% → **门禁随机失败**。
//   CI 当时靠 `--sample=100 --seed=42` 把失败概率压到约 5%，属于"挑个能过的样本"，
//   而工具自己的注释写的是"需人工复核"（复核 ≠ 让构建失败）。现改为：
//   阈值分层（≥90% 才失败）+ 默认样本提到 300 + 默认种子固定 42（可复现，--seed=random 换样本）。
const fs = require('fs');
const path = require('path');

// ---- 参数解析 ----
const args = process.argv.slice(2);
const sampleN = (args.find(a => a.startsWith('--sample=')) || '--sample=300').split('=')[1] | 0;
const rulesArg = (args.find(a => a.startsWith('--rules=')) || '').split('=')[1];
const catsArg = (args.find(a => a.startsWith('--cat=')) || '').split('=')[1];
const watchRules = rulesArg ? rulesArg.split(',').map(s => s.trim()).filter(Boolean) : null;
const watchCats = catsArg ? catsArg.split(',').map(s => s.trim()).filter(Boolean) : null;

// ---- 从 index.html 提取 JS 并在 vm 中执行 ----
const html = fs.readFileSync(path.join(__dirname, '..', 'ui', 'index.html'), 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.error('未找到 <script> 块'); process.exit(1); }
const stub = 'var document={getElementById:()=>({value:"",innerHTML:"",style:{},classList:{add(){},remove(){}}}),querySelectorAll:()=>[]};var alert=()=>{};';
const exp = ';globalThis.paipan=paipan;globalThis.matchRules=matchRules;globalThis.RULES=RULES;globalThis.tenGod=tenGod;globalThis.GAN_WX=GAN_WX;globalThis.CANG=CANG;';
eval(stub + m[1] + exp);

// ---- 全 16 类别 ----
const ALL_CATS = ['性格','事业','财运','婚姻','健康','格局','用神喜忌','十神组合','学业','六亲','神煞','流年','合婚','五行生克','大运','流月'];
let activeCats = watchCats || ALL_CATS;

// ---- 随机盘生成（2026-08-19：LCG 可复现种子，--seed=N 固定样本；默认时间种子保持随机）----
let seed = (args.find(a => a.startsWith('--seed=')) || '').split('=')[1];
// 默认固定 42：门禁必须可复现（原实现用 Date.now()，同一份数据两次跑结论可能不同）。
// 需要换一批样本时用 --seed=random。
seed = (seed === 'random') ? (Date.now() >>> 0) : (seed ? (+seed >>> 0) : 42);
const seedInit = seed;   // rnd() 会不断推进 seed，报告里要打印**初始**种子才可复现
function rnd(){ seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; }
const rand = (a, b) => a + Math.floor(rnd() * (b - a + 1));
const charts = [];
for (let i = 0; i < sampleN; i++) {
  const y = rand(1950, 2005), mo = rand(1, 12), d = rand(1, 28), hh = rand(0, 23), mm = rand(0, 59);
  const c = paipan('P' + i, i % 2 ? '男' : '女', y, mo, d, hh, mm, '', 'no');
  if (c) charts.push(c);
}
const total = charts.length;
console.log(`样本: ${total} 个随机命盘 (${new Date().toISOString().slice(0, 19)})\n`);

// ---- 逐盘匹配并统计 ----
const hitCount = {};
charts.forEach(c => {
  const cats = matchRules(c);
  activeCats.forEach(cat => {
    (cats[cat] || []).forEach(r => { hitCount[r.id] = (hitCount[r.id] || 0) + 1; });
  });
});

// ---- 无 condition 的规则（始终命中）----
console.log(`== 无 condition 的规则（始终命中，${activeCats.join('/')} 内）==`);
const noCondRules = RULES.filter(r => activeCats.includes(r.category) && (!r.condition || Object.keys(r.condition).length === 0));
if (noCondRules.length === 0) console.log('✅ 无无条件命中规则');
else {
  noCondRules.forEach(r => console.log(`  ℹ️  ${r.id} [${r.category}] → ${r.conclusion.substring(0, 40)}...`));
  console.log(`共 ${noCondRules.length} 条（若为通用评语则正常，若应有条件则需补）`);
}

// ---- 100% 命中规则（坏规则候选）----
console.log(`\n== ${activeCats.join('/')} 类中命中率 100% 的规则（共 ${total} 盘）==`);
let bad = 0;
for (const id in hitCount) {
  if (hitCount[id] === total) {
    // 跳过无condition规则（已在上面报告）
    const r = RULES.find(x => x.id === id);
    if (r && (!r.condition || Object.keys(r.condition).length === 0)) continue;
    bad++;
    console.log(`⚠️  ${id} [${r ? r.category : '?'}] cond=${JSON.stringify(r ? r.condition : null)}`);
    console.log(`    → ${r ? r.conclusion : '(不存在)'}`);
  }
}
console.log(bad === 0 ? '✅ 无 100% 命中规则（排除无条件规则）' : `共 ${bad} 条需修复\n`);

// ---- 命中率分布 ----
console.log('\n== 命中率分布（≥90% 失败；80%~90% 人工复核，仅警告）==');
const hardFail = [], review = [];
for (const id in hitCount) {
  const r = RULES.find(x => x.id === id);
  if (r && (!r.condition || Object.keys(r.condition).length === 0)) continue; // 跳过无条件规则
  const rate = hitCount[id] / total;
  if (rate >= 0.9 && hitCount[id] < total) hardFail.push({ id, rate, hit: hitCount[id] });
  else if (rate >= 0.8) review.push({ id, rate, hit: hitCount[id] });
}
hardFail.sort((a, b) => b.rate - a.rate);
review.sort((a, b) => b.rate - a.rate);
const show = (list, mark) => list.forEach(({ id, rate, hit }) => {
  const r = RULES.find(x => x.id === id);
  console.log(`${mark} ${id} ${(rate * 100).toFixed(0)}% (${hit}/${total}) [${r ? r.category : '?'}] → ${r ? r.conclusion.substring(0, 50) : ''}`);
});
if (hardFail.length === 0) console.log('✅ 无 ≥90% 命中规则');
else show(hardFail, '❌');
if (review.length === 0) console.log('✅ 无 80%~90% 命中规则');
else show(review, '🔎');
if (review.length && total < 300)
  console.log(`   （本样本仅 ${total} 盘，80%~90% 区间波动大，建议 --sample=2000 复核后再判断）`);
const conditionalRules = Object.keys(hitCount).filter(id => {
  const r = RULES.find(x => x.id === id);
  return r && r.condition && Object.keys(r.condition).length > 0;
});
console.log(`有条件规则数: ${conditionalRules.length}（本类别内，不含无条件规则）`);

// ---- 0 命中规则（信息级：样本内未命中 ≠ 死规则；2026-08-19 增强：combo_食神制杀_印 曾 400 盘 0 命中，手动深挖才发现）----
// 排除专用触发类（流年/流月/大运/合婚：matchRules 主引擎不输出，天然 0 命中属正常）。
// 注意：<1% 低命中规则（如「日主+旺衰」组合，实测 char_甲_强 0.9%/财官印三宝 1%）在小样本（200 盘）内
// 可能 0 命中，属正常；若大样本（2000 盘）仍 0 命中才需 --rules= 深挖判定死规则。
console.log('\n== 样本内 0 命中规则（信息级：低命中属正常，大样本仍 0 才需深挖）==');
const zeroHitList = RULES.filter(r => activeCats.includes(r.category) && !['流年', '流月', '大运', '合婚'].includes(r.category) && r.condition && Object.keys(r.condition).length > 0 && !(r.id in hitCount));
if (zeroHitList.length === 0) console.log('✅ 无 0 命中规则');
else zeroHitList.forEach(r => console.log(`ℹ️  ${r.id} [${r.category}] cond=${JSON.stringify(r.condition)}`));

// ---- 每盘平均命中 ----
const per = charts.map(c => {
  let cnt = 0;
  const cats = matchRules(c);
  activeCats.forEach(cat => { cnt += (cats[cat] || []).length; });
  return cnt;
});
const avg = per.reduce((a, b) => a + b, 0) / total;
console.log(`\n${activeCats.join('/')} 平均命中/盘: ${avg.toFixed(1)} (范围 ${Math.min(...per)} - ${Math.max(...per)})`);

// ---- 深挖指定规则 ----
if (watchRules) {
  watchRules.forEach(id => {
    const r = RULES.find(x => x.id === id);
    console.log(`\n== 深挖 ${id} ==`);
    if (!r) { console.log('  (规则不存在)'); return; }
    console.log(`  condition: ${JSON.stringify(r.condition)}`);
    console.log(`  conclusion: ${r.conclusion}`);
    let hit = 0;
    charts.forEach(c => {
      const cats = matchRules(c);
      const all = Object.values(cats).flat();
      if (all.some(x => x.id === id)) {
        hit++;
        if (hit <= 3) { // 展示前 3 个命中盘的简化上下文
          console.log(`  命中盘 ${c.name}: 日主${c.dayMaster}(${c.dmWx}) 月${c.pillars[1][1]} 五行:${JSON.stringify(c.five)} 喜用:[${c.xiYong}]`);
        }
      }
    });
    console.log(`  命中率: ${hit}/${total} (${(hit / total * 100).toFixed(0)}%)`);
  });
}

// ---- 门禁退出码（2026-08-19 修复：此前恒 exit 0；2026-10-14 分层：≥90% 才失败）----
if (bad > 0 || hardFail.length > 0) {
  console.log(`\n❌ 门禁未过：100% 命中规则 ${bad} 条 / ≥90% 规则 ${hardFail.length} 条（需修复条件）`);
  if (review.length) console.log(`   （另有 ${review.length} 条落在 80%~90%，属"人工复核"级，不计入失败）`);
  process.exit(1);
}
console.log(`\n✅ 门禁通过（样本 ${total} 盘，种子 ${seedInit}）：无 100% / 无 ≥90% 命中规则`
  + (review.length ? `；${review.length} 条落在 80%~90%，建议人工复核` : ''));
process.exit(0);
