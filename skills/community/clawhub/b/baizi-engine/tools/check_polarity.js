#!/usr/bin/env node
// 门禁⑧（v1.3.19）：同条件断语极性冲突
//
// 为什么需要它：check_same_condition.js 只查「近重复（相似度≥0.60）」和「寒/暑互斥」，
// 对**语义相反但用词不相似**的结论完全无感。v1.3.19 实测漏了：
//   combo_财星破印  「财星破印，求财与学业名望相妨……」        （负）
//   combo_正财_正印   「财印同透，安稳生财不冒险，学养与财富并重……」 （正）
//   两者 condition 完全相同 {"组合":["正财","正印"]}，2000 盘实测 125/125 → 100% 同盘双出，
//   等于每一张「正财+正印同透」的盘都同时被告知「财印相益」和「财破印相妨」。相似度仅 0.19，前门禁看不见。
//
// 为什么不用「实测共现率」当判据：3000 盘实测 min 覆盖率 ≥95% 的规则对共 638 对，
// 绝大多数是 char_甲 × char_甲_强 这类包含关系（合法）→ 共现率当判据必然误报，只能静态判。
//
// 判定（任一命中即失败）：
//   ① 同 category + condition 完全相同 → 两条结论一正一负（极性词表，各自≥2 个命中词）
//   ② 同 category + condition 去掉"区分键"后相同 → 两半**不互斥**（可同时命中）：
//      a. 一方根本没写区分键（假拆分，照样双出）
//      b. 双方区分键取值可并存（如 财忌 / 印忌，能同时成立）
//   · REVIEWED：人工复核确认合法的同条件对，在此登记理由后放行
//   · --self-test：注入一对合成规则，必须被抓到（防"门禁永远绿"）
//   · --verbose：打印全部同条件组的极性判定明细（调词表时用）
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '..', 'ui', 'index.html'), 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.error('未找到 <script> 块'); process.exit(1); }
const stub = 'var document={getElementById:()=>({value:"",innerHTML:"",style:{},classList:{add(){},remove(){}}}),querySelectorAll:()=>[],querySelector:()=>null};var alert=()=>{};';
eval(stub + m[1] + ';globalThis.RULES=RULES;');

// ── 极性词表：判「结论方向」，不判吉凶强度 ──────────────────────────
// 只用方向明确、歧义小的词；需 ≥2 个命中词才算表态（1 个词多半是行文顺手），
// 一侧有正向词、另一侧只有负向词才算冲突（同时含正负 = 有前提的权衡型，不算冲突）。
const POS = ['安稳', '并重', '有成', '最吉', '富足', '顺遂', '显达', '聪慧', '和合', '甜美',
  '贤', '相助', '并进', '双全', '生财', '得位', '和美', '称心', '可期', '绵长'];
// 负向词只收"结论方向"词。刻意**不收** 忌/克/犯/孤/贫：这些在断语里常作前提出现
//（「枭神为忌，财制之」是正向结论），收进来会把前提当结论、令正向断语被误判成负向。
const NEG = ['破印', '坏印', '相妨', '矛盾', '受损', '受抑', '难成', '易生', '不宜',
  '分夺', '争夺', '劳苦', '损名', '相残', '反目', '受制', '有损'];

function polarity(r) {
  const t = (r.conclusion || '') + (r.suggestion || '');
  const pos = POS.filter(w => t.indexOf(w) >= 0);
  const neg = NEG.filter(w => t.indexOf(w) >= 0);
  const dir = (pos.length >= 2 && neg.length === 0) ? '正'
    : (neg.length >= 2 && pos.length === 0) ? '负'
      : '混合';
  return { dir, pos, neg };
}

// ── 区分键：能把两条同条件规则拆成互斥两半的维度 ────────────────────
// 喜忌（v1.3.19 新增）/ 旺衰（强·弱·中和）/ 性别（男·女）/ 日主（十天干）
const DISCRIM_KEYS = ['喜忌', '旺衰', '性别', '日主'];

function canon(o) {
  if (Array.isArray(o)) return o.map(canon);
  if (o && typeof o === 'object') {
    const out = {};
    Object.keys(o).sort().forEach(k => { out[k] = canon(o[k]); });
    return out;
  }
  return o;
}
const keyOf = c => JSON.stringify(canon(c));
function stripDiscrim(c) {
  const out = {};
  Object.keys(c).forEach(k => { if (DISCRIM_KEYS.indexOf(k) < 0) out[k] = c[k]; });
  return out;
}
function asArr(v) { return Array.isArray(v) ? v : [v]; }

// 两条规则在某个区分键上是否**必然互斥**（不可能同时成立）
function exclusiveOn(a, b, key) {
  const ca = a.condition || {}, cb = b.condition || {};
  if (!(key in ca) || !(key in cb)) return false;
  const va = ca[key], vb = cb[key];
  if (key === '喜忌') {
    // 喜忌元素形如 {十神|五行, 为:'喜'|'忌'}；同一主体一喜一忌 → 互斥
    const subj = o => o['十神'] || o['五行'] || '';
    const pol = o => o['为'] || o['状态'] || '';
    for (const x of asArr(va)) for (const y of asArr(vb)) {
      if (x && y && subj(x) && subj(x) === subj(y) && pol(x) && pol(y) && pol(x) !== pol(y)) return true;
    }
    return false;
  }
  // 标量型区分键：取值集合无交集 → 互斥
  const sa = new Set(asArr(va).map(v => JSON.stringify(v)));
  return asArr(vb).every(v => !sa.has(JSON.stringify(v)));
}
function mutuallyExclusive(a, b) {
  return DISCRIM_KEYS.some(k => exclusiveOn(a, b, k));
}

// 人工复核后放行的同条件对：key 用 "idA × idB"（升序），值写放行理由
const REVIEWED = {
  'kin_手足_正财 × kin_祖上_正财': '同条件但六亲主体不同（年干正财→祖上/手足两种取象），非极性冲突',
  'kin_手足_比肩 × kin_祖上_比肩': '同上：年干比肩→手足/祖上两种取象',
  'marriage_rz_m_偏财 × marriage_nanpiancai': '同为男命日支偏财，一为配偶性情、一为感情形态，互补而非相反',
};

function analyze(rules, verbose) {
  const groups = new Map();
  rules.forEach(r => {
    const c = r.condition || {};
    if (Object.keys(c).length === 0) return;              // 面板按 id 触发的模板类不参与
    const whole = r.category + ' || ' + keyOf(c);
    if (!groups.has(whole)) groups.set(whole, []);
    groups.get(whole).push(r);
  });
  const conflicts = [], splits = [], pairsChecked = [], reviewHits = [];
  for (const [key, rs] of groups) {
    if (rs.length < 2) continue;
    for (let i = 0; i < rs.length; i++) for (let j = i + 1; j < rs.length; j++) {
      const a = rs[i], b = rs[j], pa = polarity(a), pb = polarity(b);
      pairsChecked.push({ key, a: a.id, b: b.id, da: pa.dir, db: pb.dir, pa, pb });
      const pairId = [a.id, b.id].sort().join(' × ');
      if (pa.dir !== '混合' && pb.dir !== '混合' && pa.dir !== pb.dir) {
        if (REVIEWED[pairId]) reviewHits.push(pairId); else conflicts.push({ key, a: a.id, b: b.id, da: pa.dir, db: pb.dir });
      }
    }
  }
  // ② 按"区分键"分组：去掉某个区分键后同条件，且**结论一正一负** → 必须在该键上真互斥
  //    只查结论相反的对：通用规则 + 分日主/分旺衰变体这类合法共现（结论同向）不进本检查，
  //    否则 1000 条库里会报出 200+ 对噪声，把真问题埋掉。
  for (const K of DISCRIM_KEYS) {
    const stripped = new Map();
    rules.forEach(r => {
      const c = r.condition || {};
      if (Object.keys(c).length === 0) return;
      if (!(K in c)) return;                               // 只统计"写了这个区分键"的规则
      const s = {};
      Object.keys(c).forEach(k => { if (k !== K) s[k] = c[k]; });
      const k = r.category + ' || ' + keyOf(s);
      if (!stripped.has(k)) stripped.set(k, []);
      stripped.get(k).push(r);
    });
    for (const [key, rs] of stripped) {
      if (rs.length < 2) continue;
      for (let i = 0; i < rs.length; i++) for (let j = i + 1; j < rs.length; j++) {
        const a = rs[i], b = rs[j];
        const pa = polarity(a), pb = polarity(b);
        if (pa.dir === '混合' || pb.dir === '混合' || pa.dir === pb.dir) continue; // 结论同向，允许共存
        const pairId = [a.id, b.id].sort().join(' × ');
        if (REVIEWED[pairId]) continue;
        if (!exclusiveOn(a, b, K)) splits.push({ key: `${K}: ${key}`, a: a.id, b: b.id, ca: a.condition, cb: b.condition });
      }
    }
  }
  if (verbose) {
    pairsChecked.sort((x, y) => (x.da === '混合' ? 1 : 0) - (y.da === '混合' ? 1 : 0));
    pairsChecked.forEach(p => console.log(
      `   ${p.da}/${p.db}  ${p.a} × ${p.b}  [正:${p.pa.pos.join(',') || '—'}] [负:${p.pa.neg.join(',') || '—'}] | [正:${p.pb.pos.join(',') || '—'}] [负:${p.pb.neg.join(',') || '—'}]`));
  }
  return { groups: [...groups.values()].filter(g => g.length > 1).length, pairs: pairsChecked.length, conflicts, splits, reviewHits };
}

// ── --self-test：注入合成冲突对，必须被抓到 ─────────────────────────
function selfTest() {
  const base = { category: '十神组合', condition: { '组合': ['甲测试', '乙测试'] } };
  const pos = Object.assign({}, base, { id: '__ST_POS', conclusion: '测试正向：安稳有成，财路绵长可期。', suggestion: '测试' });
  const neg = Object.assign({}, base, { id: '__ST_NEG', conclusion: '测试负向：相妨矛盾，受损难成。', suggestion: '测试' });
  const r1 = analyze(RULES.concat([pos, neg]));
  const caughtA = r1.conflicts.some(c => [c.a, c.b].sort().join(' × ') === '__ST_NEG × __ST_POS');
  // 假拆分：写了 喜忌 但两半可并存（印喜 / 财忌 与 印喜 / 财忌 同向不可并存判不了 → 用可并存组合）
  const s1 = Object.assign({}, base, { id: '__ST_S1', condition: { '组合': ['甲测试', '乙测试'], '喜忌': { '十神': '偏印', '为': '忌' } }, conclusion: '同上正向文案，安稳有成可期。', suggestion: '测试' });
  const s2 = Object.assign({}, base, { id: '__ST_S2', condition: { '组合': ['甲测试', '乙测试'], '喜忌': { '十神': '正印', '为': '忌' } }, conclusion: '同上负向文案，相妨矛盾受损。', suggestion: '测试' });
  const r2 = analyze(RULES.concat([s1, s2]));
  const caughtB = r2.splits.some(s => [s.a, s.b].sort().join(' × ') === '__ST_S1 × __ST_S2');
  // 对照组：真互斥的拆分（偏印忌 / 偏印喜）不得报错
  const s3 = Object.assign({}, s1, { id: '__ST_S3', condition: { '组合': ['甲测试', '乙测试'], '喜忌': { '十神': '偏印', '为': '喜' } } });
  const r3 = analyze(RULES.concat([s1, s3]));
  const falsePositive = r3.splits.some(s => [s.a, s.b].some(id => id.indexOf('__ST_S') === 0));

  console.log('门禁自检（注入合成故障，必须被抓到）：');
  console.log(`  ${caughtA ? '✅' : '❌'} 自检①：同条件 + 一正一负结论 → ${caughtA ? '已抓出' : '漏检'}`);
  console.log(`  ${caughtB ? '✅' : '❌'} 自检②：假拆分（喜忌写错成可并存）→ ${caughtB ? '已抓出' : '漏检'}`);
  console.log(`  ${falsePositive ? '❌' : '✅'} 对照③：真互斥拆分（偏印忌/偏印喜）→ ${falsePositive ? '误报' : '未误报'}`);
  return caughtA && caughtB && !falsePositive ? 0 : 1;
}

const verbose = process.argv.includes('--verbose');
const r = analyze(RULES, verbose);
console.log(`同条件组: ${r.groups} 组（≥2 条）/ 逐对检查 ${r.pairs} 对（不含空 condition 模板类）`);

if (r.conflicts.length) {
  console.log('\n❌ 同条件极性冲突（完全相同的 condition，结论一正一负 → 同盘必然双出、必有一条与命局相反）:');
  r.conflicts.forEach(c => console.log(`   [${c.key}]\n      ${c.a}(${c.da})  ×  ${c.b}(${c.db})`));
}
if (r.splits.length) {
  console.log('\n❌ 假拆分 / 拆分后仍可并存（写了区分键但两半能同时命中）:');
  r.splits.forEach(s => console.log(`   [${s.key}]  ${s.a} ${JSON.stringify(s.ca)}\n      ×  ${s.b} ${JSON.stringify(s.cb)}`));
}
if (r.reviewHits.length) console.log('\nℹ️  已在 REVIEWED 登记的合法同条件对: ' + r.reviewHits.join(', '));

if (process.argv.includes('--self-test')) process.exit(selfTest());

const fatal = r.conflicts.length + r.splits.length;
if (fatal === 0) console.log('\n✅ 无同条件极性冲突 / 无假拆分');
else console.log(`\n❌ 门禁未过：极性冲突 ${r.conflicts.length} 对 / 假拆分 ${r.splits.length} 对`);
process.exit(fatal === 0 ? 0 : 1);
