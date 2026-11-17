'use strict';
/**
 * construction-material-check.js —— 建筑工程材料用量与损耗核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每个分部分项完工或每月物资盘点 / 成本归集时**，项目物资员、
 * 施工员、预算员、成本会计要把「材料需用计划与实际消耗对照表」核一遍 —— 这张表是材料成本、
 * 限额领料考核、超耗扣款与物资台账的原始依据，签完再改就要走签证 / 变更流程。
 *
 * 表里有几条算式**完全能算出来对错**（手算即可复现）：
 *
 *   损耗量 = 领用量 − 实际消耗量
 *   损耗率 = 损耗量 ÷ 领用量 × 100%
 *   损耗率 ≤ 损耗率上限（用表内「损耗率上限」列；表里没有这一列时按参考上限 5.00% 提示）
 *   合计行的 需用计划量 / 领用量 / 实际消耗量 / 损耗量 = 各明细行之和
 *
 * 免费档执行 6 类检查（见 CHECKS_GIVEN）；完整档（付费）在此之上多出**一种能力**：
 * **超耗归因 + 跨分部分项 / 跨期间超耗汇总台账 + 按超耗金额从大到小的处理清单 + 跨期间损耗率漂移提示**
 * （见 CHECKS_WITHHELD）。超耗金额 = 超出「损耗率上限」的那部分损耗量 × 单价。
 *
 * 与已有能力的区别：`bom-consumption-variance-check` 核的是**制造业工单 / BOM** 的用量差异
 * （标准用量 = 单位用量 × 产出数量）；本能力核的是**建筑工程分部分项**的材料需用量 —
 * 领用量 — 实耗量三列之间的损耗勾稽，归因方向也是工地场景（限额领料、以领代耗、返工拆改、被盗流失）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不写盘、不读环境变量**。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 材料不足时**绝不给结论**（既不做"一致"的认定，也不做"不一致"的认定），也不套用默认值。
 *
 * ⚠️ 完整档（付费）的实现集中在下面那行分隔注释之后；免费包在打包时会被整块摘掉。
 *    付费开关**只声明一次**（`run()` 里的一个布尔常量），免费包里连着开关与分支一起删。
 *    ⛔ 注释里**不要**写出那个开关的字面量：摘除脚本的残渣断言是纯字符串包含判断，写了会被判"没删干净"。
 */

const CHECKS_GIVEN = [
  '损耗量复算（损耗量 = 领用量 − 实际消耗量）',
  '损耗率复算（损耗率 = 损耗量 ÷ 领用量 × 100%）',
  '损耗率与参考上限比对（表内「损耗率上限」列优先；没有这一列时按参考上限 5.00%）',
  '需用计划量与实际消耗量差异（实耗量超出需用计划量）',
  '合计行逐列复核（需用计划量 / 领用量 / 实际消耗量 / 损耗量的合计 = 各明细行之和）',
  '重复材料行与关键字段空缺检测（同一分部分项同一期间同一材料重复；必需列为空或占位符）',
];

const CHECKS_WITHHELD = [
  '超耗归因（计划偏差 / 施工损耗 / 计量口径 / 被盗或流失 / 返工）',
  '跨分部分项 / 跨期间超耗汇总台账（按分部分项 × 材料汇总加权损耗率与超耗金额）',
  '按超耗金额从大到小的处理清单（带原文行号与建议动作）',
  '跨期间损耗率漂移提示（同一材料在不同期间损耗率偏离参考中位数超过 5 个百分点）',
];

const OUT_OF_SCOPE = [
  '判断需用计划量定额是否合理（定额、损耗率上限以施工定额、投标文件与合同约定为准）',
  '判断现场材料是不是真的被盗 / 流失 / 返工（超耗归因只是按表内数据给出的**提示方向**，必须现场核实）',
  '判断计量口径（以领代耗、领料退库、甲供材抵扣、调拨）是否符合本单位物资管理办法',
  '处理负数（红字冲销 / 退料）行的会计处理与来源核实（请单独列示并附退料单）',
  '读取广联达 / 用友 / 物资系统导出的 Excel 文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '分部分项工程\t期间\t材料名称\t规格型号\t单位\t需用计划量\t领用量\t实际消耗量\t损耗量\t损耗率\t损耗率上限\t单价\t备注',
  '主体结构工程\t2026-03\t钢筋\tHRB400 Φ12\tt\t200.00\t200.00\t196.00\t4.00\t2.00%\t3.00%\t4200.00\t',
  '主体结构工程\t2026-03\t预拌混凝土\tC30\tm3\t500.00\t500.00\t495.00\t5.00\t1.00%\t2.00%\t480.00\t',
  '装饰装修工程\t2026-04\t瓷砖\t800×800\t㎡\t1000.00\t1000.00\t980.00\t20.00\t2.00%\t5.00%\t65.00\t',
  '装饰装修工程\t2026-04\t干混砂浆\tM7.5\tt\t50.00\t50.00\t48.00\t2.00\t4.00%\t5.00%\t380.00\t',
  '合计\t\t\t\t\t1750.00\t1750.00\t1719.00\t31.00\t\t\t\t',
].join('\n');

/** 数量允许误差（0.01 计量单位） */
const TOL = 0.01;
/** 损耗率允许误差（0.01 个百分点） */
const RATE_TOL = 0.01;
/** 表里没有「损耗率上限」列时的参考上限（%，参考口径，供"明显超限"时提示） */
const DEFAULT_CAP_PCT = 5.00;
/** 跨期间损耗率偏离参考中位数的容忍（百分点） */
const DRIFT_TOL = 5;
const TOTAL_WORDS = /^(合计|总计|小计|共计)$/;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的前面，否则会被抢走列（本仓库第 232 轮的坑）。
  //   「损耗率上限」必须由 lossCap 先认领，否则会被 lossRate 的「损耗率」抢走；
  //   「材料单价」必须由 price 先认领，否则会被 material 的「材料」抢走。
  lossCap: ['损耗率上限', '损耗上限', '允许损耗率', '定额损耗率', '损耗控制率'],
  lossRate: ['损耗率', '损耗比例'],
  loss: ['损耗量', '损耗数量', '损耗'],
  planned: ['需用计划量', '需用量', '计划用量', '计划量', '需用数量', '定额用量'],
  issued: ['领用量', '领料量', '出库量', '领料数量', '领料'],
  actual: ['实际消耗量', '实际消耗', '实际用量', '实耗量', '实耗', '消耗量'],
  price: ['材料单价', '单价', '采购单价'],
  part: ['分部分项工程', '分部分项', '工程部位', '部位', '分部工程'],
  period: ['期间', '月份', '所属期', '期次', '施工期', '计量期'],
  material: ['材料名称', '材料', '品名'],
  spec: ['规格型号', '规格', '型号'],
  unit: ['计量单位', '单位'],
  note: ['备注', '说明'],
};

const LABELS = {
  part: '分部分项工程', period: '期间', material: '材料名称', spec: '规格型号', unit: '单位',
  planned: '需用计划量', issued: '领用量', actual: '实际消耗量', loss: '损耗量',
  lossRate: '损耗率', lossCap: '损耗率上限', price: '单价', note: '备注',
};

// 少一列就核不动：这 8 列缺任何一列都直接判"材料不足"，绝不猜
const REQUIRED = ['part', 'period', 'material', 'planned', 'issued', 'actual', 'loss', 'lossRate'];
// 只有"数量"列可以合计；损耗率与单价是比率 / 单价口径，相加没有意义
const SUM_ROLES = ['planned', 'issued', 'actual', 'loss'];

function insufficient(missing, advice) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: advice || '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|待确认)$/i.test(s);
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '').replace(/%$/, '');
  if (!/^-?\d+(\.\d+)?$/.test(t)) return null;
  const n = Number(t);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

/**
 * 比率归一化成**百分点**：`2.00%` ⇒ 2；不写 % 时，绝对值小于 1 的按比率口径换算（`0.02` ⇒ 2），
 * 否则按百分数口径直接用（`3.00` ⇒ 3）。
 */
function pct(raw) {
  const s = raw === undefined || raw === null ? '' : String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n;
  if (Math.abs(n) < 1) return round2(n * 100);
  return n;
}

const round2 = (n) => Math.round(n * 100) / 100;

function roleOf(header) {
  const h = String(header === undefined || header === null ? '' : header).replace(/[\s（）()【】\[\]]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

function parseTable(text) {
  const raw = String(text === undefined || text === null ? '' : text)
    .split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null, cols: [], error: 'empty' };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const cols = headers.map((h, i) => ({ header: h, role: roles[i] }));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  const totals = {};
  if (missingColumns.length) return { items, totals, missingColumns, cols, error: 'no_header' };
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i] };
    let isTotal = false;
    roles.forEach((role, c) => {
      if (!role) return;
      const v = cells[c] === undefined ? '' : cells[c];
      row[role] = v;
      if (role === 'part' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; } else items.push(row);
  }
  return { items, totals, missingColumns, cols, error: null };
}

function cellOf(it, role) {
  const v = it === undefined || it === null ? undefined : it[role];
  return v === undefined || v === null ? '' : String(v).trim();
}

const who = (it) => {
  const t = [cellOf(it, 'part'), cellOf(it, 'period'), cellOf(it, 'material')].filter(Boolean).join(' ');
  return t || `第 ${it && it.line} 行`;
};
/** 每条结论都必须能指回原文行 */
const head = (it) => `${who(it)}（原文第 ${it.line} 行）`;
const basisOf = (it) => `原文第 ${it.line} 行：${it.raw}`;

function distinct(items, role) {
  const seen = new Set();
  for (const it of items) {
    const v = cellOf(it, role);
    if (v) seen.add(v);
  }
  return [...seen];
}

/* ================================ 免费档检查项 ================================ */

/** 免费档 1：损耗量 = 领用量 − 实际消耗量 */
function checkLossQty(it) {
  const issued = normNumber(it.issued);
  const actual = normNumber(it.actual);
  const stated = normNumber(it.loss);
  if (issued === null || actual === null || stated === null) return null;
  const expect = round2(issued - actual);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '损耗量复算不符', line: it.line,
    message: `${head(it)}：领用量 ${issued.toFixed(2)} − 实际消耗量 ${actual.toFixed(2)} = 损耗量应为 `
      + `${expect.toFixed(2)}，表里写的却是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '损耗量这一列是"领了多少还没用掉"的差额：先看是不是领用量抄错（把计划量抄进领用）、'
      + '实耗量漏记（还有一批料在现场没耗用），或者损耗量本身是倒挤出来的。',
    basis: basisOf(it),
  };
}

/** 免费档 2：损耗率 = 损耗量 ÷ 领用量 × 100% */
function checkLossRateValue(it) {
  const issued = normNumber(it.issued);
  const loss = normNumber(it.loss);
  const stated = pct(it.lossRate);
  if (issued === null || issued <= 0 || loss === null || stated === null) return null;
  const expect = round2((loss / issued) * 100);
  if (Math.abs(expect - stated) <= RATE_TOL) return null;
  return {
    level: 'P0', category: '损耗率与复算不符', line: it.line,
    message: `${head(it)}：损耗量 ${loss.toFixed(2)} ÷ 领用量 ${issued.toFixed(2)} × 100% = `
      + `${expect.toFixed(2)}%，表里写的却是 ${stated.toFixed(2)}%，相差 ${round2(stated - expect).toFixed(2)} 个百分点。`,
    advice: '损耗率的分母是**领用量**（不是需用计划量、也不是实耗量）：分母换了，每行的率都会不对。'
      + '不写 % 时，0~1 之间的数按比率口径认（0.02 = 2%），1 以上按百分数认（2 = 2%）。',
    basis: basisOf(it),
  };
}

/** 免费档 3：损耗率与上限比对（表内上限列优先，缺列按参考上限提示） */
function checkLossRateOverCap(it, capFromTable) {
  const issued = normNumber(it.issued);
  const loss = normNumber(it.loss);
  if (issued === null || issued <= 0 || loss === null) return null;
  const stated = pct(it.lossRate);
  const computed = round2((loss / issued) * 100);
  const used = stated === null ? computed : stated;
  const fromTable = pct(it.lossCap);
  const cap = fromTable === null ? DEFAULT_CAP_PCT : fromTable;
  if (used <= cap + RATE_TOL) return null;
  return {
    level: 'P1', category: '损耗率超出参考上限', line: it.line,
    message: `${head(it)}：损耗率 ${used.toFixed(2)}%（${stated === null ? '按损耗量复算' : '取自表内损耗率列'}）`
      + `超过上限 ${cap.toFixed(2)}%`
      + `${capFromTable && fromTable !== null ? '（表内「损耗率上限」列）' : `（表内没有可用的「损耗率上限」列，按参考上限 ${DEFAULT_CAP_PCT.toFixed(2)}% 提示）`}，`
      + `超限 ${round2(used - cap).toFixed(2)} 个百分点。`,
    advice: '先确认上限这一列是不是填成了小数比率（0.03 应写 3.00% 或 3.00）；'
      + '真超限额领料损耗率的，按本单位限额领料 / 材料承包办法走超耗分析与扣款流程。',
    basis: basisOf(it),
  };
}

/** 免费档 4：实耗量超出需用计划量 */
function checkPlannedVariance(it) {
  const planned = normNumber(it.planned);
  const actual = normNumber(it.actual);
  if (planned === null || actual === null) return null;
  const diff = round2(actual - planned);
  if (diff <= TOL) return null;
  const rate = planned > 0 ? round2((diff / planned) * 100) : null;
  return {
    level: 'P1', category: '计划量与实际消耗量差异', line: it.line,
    message: `${head(it)}：实际消耗量 ${actual.toFixed(2)} 超过需用计划量 ${planned.toFixed(2)}，`
      + `超出 ${diff.toFixed(2)}${rate === null ? '' : `（${rate.toFixed(2)}%）`}。`,
    advice: '超出需用量的部分通常只有三种来源：需用量定额本身偏低（设计变更 / 做法调整没更新计划）、'
      + '现场施工损耗偏高、或者实耗量里混进了别的部位 / 别的期间的料 —— 先分清是哪一种再补计划或走超耗分析。',
    basis: basisOf(it),
  };
}

/** 免费档 5：合计行逐列复核 */
function checkTotalRow(totals, items, role) {
  if (!totals || !totals.row) return null;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return null;
  let sum = 0;
  let n = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) { sum += v; n += 1; }
  }
  if (!n) return null;
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return null;
  return {
    level: 'P0', category: '合计行与明细之和不符', line: totals.line,
    message: `合计行（原文第 ${totals.line} 行）的「${LABELS[role]}」是 ${stated.toFixed(2)}，`
      + `${n} 条明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
    advice: '合计行必须是明细行相加：差额通常是漏了一行明细、某行被重复计入，或者合计行用了别处的数（计划表 / 上月表）。',
    basis: `原文第 ${totals.line} 行：${totals.row.raw}`,
  };
}

/** 免费档 6-a：重复材料行 */
function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = [cellOf(it, 'part'), cellOf(it, 'period'), cellOf(it, 'material'), cellOf(it, 'spec')].join('|');
    if (/^\|+$/.test(key) || key.replace(/\|/g, '') === '') continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '重复材料行', line: it.line,
        message: `${head(it)}与原文第 ${seen.get(key)} 行是同一条材料（分部分项 + 期间 + 材料名称 + 规格型号完全相同），`
          + '却被拆成了两行 —— 用量与损耗会被重复汇总。',
        advice: '同一分部分项、同一期间、同一材料（含规格）应合并成一行；'
          + '确实是分批领料的，在备注里写清批次，不要再开一行。',
        basis: basisOf(it),
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/** 免费档 6-b：必需列为空或占位符 */
function checkBlanks(items, required) {
  const out = [];
  for (const it of items) {
    const miss = required.filter((r) => isBlank(it[r]));
    if (!miss.length) continue;
    out.push({
      level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
      message: `${head(it)}有 ${miss.length} 个关键字段是空的或占位符：`
        + `${miss.map((r) => `${LABELS[r]}（${cellOf(it, r) || '空'}）`).join('、')} —— 这一行的损耗勾稽核不动，`
        + '所以本工具对它**不给结论**。',
      advice: '必需列一个都不能空：填不上就先写 0.00 并在备注里说明，别用「—」「待填」「无」「N/A」代替。',
      basis: basisOf(it),
    });
  }
  return out;
}

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`,
      '入参请写成 {"text": "（含表头的材料需用计划与实际消耗对照表）"}，或先用 --sample 看看需要什么格式。');
  }
  const p = payload && typeof payload === 'object' ? payload : {};
  const text = typeof p.text === 'string' ? p.text : (typeof p.content === 'string' ? p.content : '');
  if (text.trim().length < 5) {
    return insufficient(['材料需用计划与实际消耗对照表正文（text）'],
      '请把这张表连**表头**一起贴进来（Tab 分隔最稳）：分部分项工程 / 期间 / 材料名称 / 规格型号 / 单位 / '
      + '需用计划量 / 领用量 / 实际消耗量 / 损耗量 / 损耗率 / 损耗率上限 / 单价。'
      + '可用 {"text": "…"}，或先跑 --sample 看格式。');
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['材料需用计划与实际消耗对照表正文（text）'],
      '入参里没有任何可读的行；请把这张表连表头一起贴进来。');
  }
  if (t.error === 'no_header') {
    return insufficient([
      `对照表缺少必需列：${t.missingColumns.join('、')}`,
      `必需列清单：${REQUIRED.map((r) => LABELS[r]).join('、')}`,
      `本次认出来的表头：${t.cols.map((c) => c.header).join(' / ') || '(一行都没认出来)'}`,
    ], '从物资 / 成本系统导出后，把表头与数据行一起复制成文本贴进来（Tab 分隔最稳）；'
      + '缺列就核不动，本工具不会靠猜补列。');
  }
  if (!t.items.length) {
    return insufficient(['至少一行材料明细（分部分项工程 + 期间 + 材料名称 + 四个数量列）'],
      '只认到表头，没有明细行；请把数据行一起贴进来。');
  }

  const hasCap = t.cols.some((c) => c.role === 'lossCap');
  const findings = [];
  let executed = CHECKS_GIVEN.slice();

  for (const it of t.items) {
    const a = checkLossQty(it); if (a) findings.push(a);
    const b = checkLossRateValue(it); if (b) findings.push(b);
    const c = checkLossRateOverCap(it, hasCap); if (c) findings.push(c);
    const d = checkPlannedVariance(it); if (d) findings.push(d);
  }
  for (const role of SUM_ROLES) {
    const f = checkTotalRow(t.totals, t.items, role); if (f) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items, REQUIRED)) findings.push(f);

  let overuseLedger = [];
  let actionPlan = [];


  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));

  const parts = distinct(t.items, 'part');
  const periods = distinct(t.items, 'period');
  const materials = distinct(t.items, 'material');
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = normNumber(it[role]);
    return s + (n === null ? 0 : n);
  }, 0));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const result = {
    status: 'success',
    service_type: 'CONSTRUCTION_MATERIAL_CHECK',
    basis: '损耗量 = 领用量 − 实际消耗量；损耗率 = 损耗量 ÷ 领用量 × 100%；'
      + '损耗率不超过「损耗率上限」（表内没有这一列时按参考上限 5.00%）；'
      + '合计行的需用计划量 / 领用量 / 实际消耗量 / 损耗量 = 各明细行之和；'
      + '超耗金额 = 超出「损耗率上限」的那部分损耗量 × 单价。',
    findings,
    summary: {
      rows: t.items.length,
      parts: parts.length,
      periods: periods.length,
      materials: materials.length,
      total: findings.length,
      p0, p1, p2,
      planned_total: sumOf('planned'),
      issued_total: sumOf('issued'),
      actual_total: sumOf('actual'),
      loss_total: sumOf('loss'),
      over_amount_total: round2(actionPlan.reduce((s, x) => s + x.amount, 0)),
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    scope: {
      checks: executed,
      checks_not_run: CHECKS_WITHHELD.slice(),
      rows: t.items.length,
      parts: parts.length,
      periods: periods.length,
      materials: materials.length,
      loss_rate_cap: hasCap ? '表内「损耗率上限」列' : `参考上限 ${DEFAULT_CAP_PCT.toFixed(2)}%`,
      tolerance: TOL,
      rate_tolerance: RATE_TOL,
      executed_locally: true,
      network_used: false,
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: executed,
    checks_out_of_scope: OUT_OF_SCOPE,
  };



  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
