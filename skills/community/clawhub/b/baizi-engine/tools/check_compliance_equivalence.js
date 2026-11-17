/**
 * 合规软化版等价性门禁（v1.3.13 新增）
 *
 * 背景：`tools/compliance_soften.py` 用"全局文本替换"产出 C 端合规版 engine.compliance.js。
 * 历史事故（2026-10-13 第八轮扫描发现）：
 *   ① 引擎代码里的比较字面量 `k==='流年'` 被替换成 `k==='年度'`
 *      → matchRules 中"流年/流月/流日条件不参与主匹配"的守卫失效
 *      → 每张命盘凭空多出近 30 条流年断语，且类别名从 [流年] 变成 [年度]；
 *   ② 规则 id `liunian_流年XXX` 被替换 → 面板按 id 查规则全部查不到；
 *   ③ `category` 被替换 38 处、`source`（古籍出处）被替换 1 处。
 *
 * 本门禁的判据：**软化只允许改"给人看的文案"，不允许改任何"机器读的标识"**。
 *   - 逐规则：id 集合必须相同；category / condition / source / confidence 必须逐字节相同；
 *     conclusion / suggestion 允许不同（这正是软化的目的）。
 *   - 逐命盘：matchRules 的类别集合与每类规则 id 序列必须完全一致。
 *   - findRule：所有 id 在两侧都必须能查到。
 *   - 反向哨兵：若两侧文案完全相同，说明软化根本没生效（门禁失效），同样报错。
 *
 * 用法：node tools/check_compliance_equivalence.js
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const DIST = path.join(ROOT, 'engine', 'engine.dist.js');
const COMP = path.join(ROOT, 'engine', 'engine.compliance.js');
const SAMPLE = 200;

let fails = 0, warns = 0;
function check(name, ok, extra){ console.log((ok ? '  ✅ ' : '  ❌ ') + name + (extra ? '  [' + extra + ']' : '')); if (!ok) fails++; }

if (!fs.existsSync(COMP)) {
  console.error('❌ 未找到 engine/engine.compliance.js');
  console.error('   生成：cp engine/engine.dist.js engine/engine.compliance.js && python tools/compliance_soften.py engine/engine.compliance.js');
  process.exit(1);
}
const D = require(DIST);
const C = require(COMP);

console.log('=== 1. 规则元数据：机器读的标识必须逐字节相同 ===');
const md = new Map(D.RULES.map(r => [r.id, r]));
const mc = new Map(C.RULES.map(r => [r.id, r]));
const onlyDist = [...md.keys()].filter(k => !mc.has(k));
const onlyComp = [...mc.keys()].filter(k => !md.has(k));
check('规则条数一致', D.RULES.length === C.RULES.length, `dist=${D.RULES.length} compliance=${C.RULES.length}`);
check('规则 id 集合一致', onlyDist.length === 0 && onlyComp.length === 0,
  onlyDist.length + onlyComp.length ? 'dist独有 ' + onlyDist.slice(0, 5) + ' / comp独有 ' + onlyComp.slice(0, 5) : '');

const FIELDS = ['category', 'condition', 'source', 'confidence'];
for (const f of FIELDS) {
  const bad = [];
  for (const [id, r] of md) {
    const q = mc.get(id);
    if (!q) continue;
    const a = typeof r[f] === 'object' ? JSON.stringify(r[f]) : String(r[f]);
    const b = typeof q[f] === 'object' ? JSON.stringify(q[f]) : String(q[f]);
    if (a !== b) bad.push(id + ': [' + a.slice(0, 40) + '] → [' + b.slice(0, 40) + ']');
  }
  check(`字段 ${f} 未被软化改动`, bad.length === 0, bad.length ? bad.length + ' 条，例：' + bad[0] : '');
}
const catNames = new Set(D.RULES.map(r => r.category));
const catBad = [...catNames].filter(c => !C.RULES.some(r => r.category === c));
check('类别名集合未被改名', catBad.length === 0, catBad.length ? '缺少 ' + catBad.join(',') : '');

console.log('\n=== 2. 软化必须真的生效（反向哨兵）===');
let textChanged = 0, condChanged = 0;
for (const [id, r] of md) {
  const q = mc.get(id); if (!q) continue;
  if (r.conclusion !== q.conclusion) textChanged++;
  if (r.suggestion !== q.suggestion) condChanged++;
}
check('存在被软化的文案（否则门禁本身失效）', textChanged > 0, `conclusion 改动 ${textChanged} 条 / suggestion 改动 ${condChanged} 条`);

console.log('\n=== 3. 行为等价：matchRules 逐盘对比 ===');
const diffs = [];
let charts = 0;
for (let i = 0; i < SAMPLE; i++) {
  const y = 1940 + (i * 7) % 160, mo = 1 + (i * 5) % 12, d = 1 + (i * 11) % 28, hh = i % 24, mi = (i * 13) % 60;
  const ctx = D.paipan('T', i % 2 ? '男' : '女', y, mo, d, hh, mi, '北京市', 'no');
  if (!ctx) continue;
  charts++;
  const a = D.matchRules(ctx), b = C.matchRules(ctx);
  const ka = Object.keys(a), kb = Object.keys(b);
  if (ka.join('|') !== kb.join('|')) {
    const extra = kb.filter(k => !ka.includes(k)), missing = ka.filter(k => !kb.includes(k));
    diffs.push(`盘${i}: 类别不一致（comp 多出 [${extra.join(',')}]，缺失 [${missing.join(',')}]）`);
    continue;
  }
  for (const k of ka) {
    const ia = a[k].map(r => r.id).join(',');
    const ib = b[k].map(r => r.id).join(',');
    if (ia !== ib) { diffs.push(`盘${i}: 类别[${k}] 命中规则不一致`); break; }
  }
}
check(`matchRules 在 ${charts} 盘上类别与命中规则完全一致`, diffs.length === 0,
  diffs.length ? diffs.length + ' 盘不一致，例：' + diffs[0] : '');

console.log('\n=== 4. findRule 全 id 可查 ===');
let findBad = [];
for (const id of md.keys()) {
  const q = C.findRule(id);
  if (!q || q.id !== id) { findBad.push(id); }
}
check('所有规则 id 在 compliance 版仍可 findRule', findBad.length === 0,
  findBad.length ? findBad.length + ' 个查不到，例：' + findBad.slice(0, 5).join(',') : '');

console.log('\n=== 5. 面板触发类规则不得泄漏进主匹配 ===');
// 流年/流月/流日/合婚 条件键的规则：主引擎必须 0 命中（两侧都要）
const PANEL_KEYS = ['流年', '流月', '流日', '合婚'];
const panelIds = new Set(D.RULES.filter(r => Object.keys(r.condition || {}).some(k => PANEL_KEYS.includes(k))).map(r => r.id));
let leakD = 0, leakC = 0;
for (let i = 0; i < 40; i++) {
  const ctx = D.paipan('L', '男', 1960 + i, 1 + i % 12, 1 + i % 28, 10, 0, '北京市', 'no');
  if (!ctx) continue;
  for (const r of Object.values(D.matchRules(ctx)).flat()) if (panelIds.has(r.id)) leakD++;
  for (const r of Object.values(C.matchRules(ctx)).flat()) if (panelIds.has(r.id)) leakC++;
}
check('dist 主匹配无面板类泄漏', leakD === 0, 'dist 泄漏 ' + leakD + ' 次');
check('compliance 主匹配无面板类泄漏', leakC === 0, 'compliance 泄漏 ' + leakC + ' 次');

console.log('\n' + (fails === 0
  ? '✅ 合规软化版与 dist 行为等价（仅文案不同）'
  : `❌ 合规软化版与 dist 存在 ${fails} 项不一致 —— 软化越界改到了"机器读的标识"`));
process.exit(fails === 0 ? 0 : 1);
