'use strict';
/**
 * chain-store-settlement-check.js —— 连锁加盟门店结算核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月跟门店/加盟商结算的时候**，总部财务要按门店逐店出一张
 * 结算核对表：门店这个月做了多少**营业额**，按合同**抽成比例**该抽多少**抽成**，
 * 又该收回多少**物料供应款**、多少**其他扣款**，扣完以后**实付**给门店多少钱
 * （另有一列**保证金**是单独挂账、按期登记结存的）。
 *
 * 为什么必须机械核：① 抽成 = 营业额 × 抽成比例，**比例填错一位**（15% 写成 1.5% 或 51%）
 * 就是几千块的差；② 实付是四个数加减出来的，**逐店勾稽**只要有一行算错，钱就打错；
 * ③ 门店一多，人眼核不动 —— 而抽成算错**直接伤加盟商关系**（少算总部吃亏，多算加盟商翻脸）。
 * 这些都是**算术**，完全能算出对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *   result.scope   = {checks, checks_not_run, rows, periods, executed_locally, network_used, …}
 *   result.summary = {rows, periods, total, p0, p1, p2, verdict, omitted}
 *
 * 核心可算关系（都能手算复现）：
 *   抽成金额 = 营业额 × 抽成比例
 *   实付金额 = 营业额 − 抽成金额 − 物料供应款 − 其他扣款      ← 表里给定的算式，别自己加项
 *   合计行   = 各门店明细行逐列之和
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**抽成比例、也不判断保证金该不该收（以加盟合同为准）：
 *    只对"偏离合同抽成比例"做**提示**，并明确标注参考口径。
 */

const CHECKS_GIVEN = [
  '抽成勾稽（营业额 × 抽成比例 = 抽成金额）',
  '实付复算（营业额 − 抽成金额 − 物料供应款 − 其他扣款 = 实付金额）',
  '合计行逐列复核（每一列的合计是否等于各门店之和）',
  '同一门店同一期重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '抽成比例偏离合同参考区间（合同抽成比例 ± 0.5 个百分点）提示',
  '实付为负（扣款超过营业额）提示',
  '扣款合计超过营业额检测',
  '营业额与门店上报不一致（差超 2%）提示',
  '同一门店同期出现两种抽成比例提示',
];

const OUT_OF_SCOPE = [
  '判断抽成比例、最低保底、返利与保证金是否符合加盟合同（合同口径以你们签的合同为准；本工具只核表内勾稽）',
  '处理阶梯抽成（按营业额分档）与年度清算（请先把本期适用档的抽成比例填进表里）',
  '把保证金并进本期实付算式：本表给定的算式是「实付 = 营业额 − 抽成 − 物料供应款 − 其他扣款」，'
  + '保证金列只参与「金额为负」与合计行复核；保证金怎么收、怎么退请看合同',
  '判断收入确认与开票口径；给出法律或税务意见',
  '读取 .xlsx 或门店 POS / 收银系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '门店\t期间\t营业额\t门店上报营业额\t抽成比例\t合同抽成比例\t抽成金额\t物料供应款\t其他扣款\t保证金\t实付金额',
  'A店\t2026-01\t200000.00\t200000.00\t15%\t15%\t30000.00\t5000.00\t1200.00\t20000.00\t163800.00',
  'B店\t2026-01\t150000.00\t150000.00\t18%\t18%\t27000.00\t3200.00\t800.00\t0.00\t119000.00',
  'C店\t2026-01\t80000.00\t80000.00\t12%\t12%\t9600.00\t1500.00\t400.00\t5000.00\t68500.00',
  '合计\t\t430000.00\t430000.00\t\t\t66600.00\t9700.00\t2400.00\t25000.00\t351300.00',
].join('\n');

const TOL = 0.01;
/* 抽成比例允许的偏离：0.5 个百分点（合同 15% 时，14.5%~15.5% 之间不算偏离） */
const RATE_TOL = 0.005;
/* 营业额与门店上报允许的差异：2% */
const REVENUE_DIFF_TOL = 0.02;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须在前，否则宽泛的词会把更细的那一列抢走
  //    （「门店上报营业额」不能被「营业额」抢走、「合同抽成比例」不能被「抽成比例」、「门店」抢走；
  //     本仓库在这类坑上栽过多次，靠 tools/header_map_check.py 机械拦住）
  reportedRevenue: ['门店上报营业额', '门店报送营业额', '上报营业额', '门店上报'],
  revenue: ['营业额', '销售额', '营业收入'],
  store: ['门店名称', '门店', '店铺', '加盟店', '加盟商'],
  period: ['结算期间', '期间', '月份', '账期', '所属期'],
  contractRate: ['合同抽成比例', '合同扣点比例', '合同抽成率', '合同扣点', '合同比例'],
  rate: ['抽成比例', '扣点比例', '抽成率', '扣点', '佣金比例'],
  commission: ['抽成金额', '抽成额', '提成额', '抽成', '佣金'],
  material: ['物料供应款', '物料款', '物料供应', '物料结算'],
  otherDeduct: ['其他扣款', '其它扣款', '其他扣减', '其他扣项', '其他费用'],
  deposit: ['履约保证金', '保证金', '押金'],
  net: ['实付金额', '实付', '结算实付', '应付门店'],
};

const LABELS = {
  store: '门店', period: '期间', revenue: '营业额', reportedRevenue: '门店上报营业额',
  rate: '抽成比例', contractRate: '合同抽成比例', commission: '抽成金额',
  material: '物料供应款', otherDeduct: '其他扣款', deposit: '保证金', net: '实付金额',
};

/* 缺了这 8 列就没法勾稽（合同抽成比例、保证金是可选的：没有就少核一项，不硬猜） */
const REQUIRED = ['store', 'period', 'revenue', 'rate', 'commission', 'material', 'otherDeduct', 'net'];
/* 合计行要逐列复核的列（比率列不参与求和） */
const SUM_ROLES = ['revenue', 'reportedRevenue', 'commission', 'material', 'otherDeduct', 'deposit', 'net'];
/* 「金额为负」要看的列 */
const AMOUNT_ROLES = ['revenue', 'reportedRevenue', 'commission', 'material', 'otherDeduct', 'deposit', 'net'];
/* 实付算式的扣项（表里给定的算式，别自己加项） */
const DEDUCT_ROLES = ['commission', 'material', 'otherDeduct'];

const TOTAL_WORDS = /^(合计|总计|小计|共计|汇总|全店合计)$/;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()]/g, '');
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

function normNumber(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

/** 比率归一化成小数：`15%` ⇒ 0.15；`0.15` ⇒ 0.15；`15` ⇒ 0.15 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  const totals = {};
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1 };
    let isTotal = false;
    roles.forEach((role, c) => {
      if (!role) return;
      const v = cells[c] === undefined ? '' : cells[c];
      row[role] = v;
      if ((role === 'store' || role === 'period') && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const s = it && !isBlank(it.store) ? String(it.store).trim() : '';
  const p = it && !isBlank(it.period) ? String(it.period).trim() : '';
  if (s && p) return `${s}（${p}）`;
  if (s) return s;
  return `第 ${it && it.line} 行`;
};

const pct = (rate) => `${round2(rate * 100).toFixed(2)}%`;

/* 检查函数两种返回形状，**不许混用**：
 *   · 单条：`checkXxx(it)` → finding | null       → 调用处 `const x = checkXxx(it); if (x) findings.push(x);`
 *   · 多条：`checkXs(items)` → finding[]（可为空）→ 调用处 `for (const x of checkXs(...)) findings.push(x);`
 * 混用的后果是把整个数组 push 进 findings：summary 计数全错、下游按对象读字段直接崩。
 */

/* ================================ 免费档检查项 ================================ */

/** 单条：抽成 = 营业额 × 抽成比例 */
function checkCommission(it) {
  const rev = normNumber(it.revenue);
  const rate = rateValue(it.rate);
  const stated = normNumber(it.commission);
  if (rev === null || rate === null || stated === null) return null;
  const expect = round2(rev * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '抽成与营业额×比例复算不符', line: it.line,
    message: `${who(it)}：营业额 ${rev.toFixed(2)} × 抽成比例 ${pct(rate)} 应为 ${expect.toFixed(2)}，`
      + `表里抽成是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}`
      + '（比例填错一位或多算、少算一期都会这样，抽成算错直接伤加盟商关系）。',
  };
}

/** 单条：实付 = 营业额 − 抽成 − 物料供应款 − 其他扣款 */
function checkNetPay(it) {
  const rev = normNumber(it.revenue);
  const comm = normNumber(it.commission);
  const mat = normNumber(it.material);
  const other = normNumber(it.otherDeduct);
  const stated = normNumber(it.net);
  if (rev === null || comm === null || mat === null || other === null || stated === null) return null;
  const expect = round2(rev - comm - mat - other);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '实付与扣项复算不符', line: it.line,
    message: `${who(it)}：营业额 ${rev.toFixed(2)} − 抽成 ${comm.toFixed(2)} − 物料供应款 ${mat.toFixed(2)}`
      + ` − 其他扣款 ${other.toFixed(2)} = ${expect.toFixed(2)}，表里实付是 ${stated.toFixed(2)}，`
      + `相差 ${round2(stated - expect).toFixed(2)}（实付是打给门店的钱，逐店都要勾稽）。`,
  };
}

/** 多条：金额列里出现负数 */
function checkNegativeAmounts(it) {
  const out = [];
  for (const role of AMOUNT_ROLES) {
    const v = normNumber(it[role]);
    if (v === null || v >= -TOL) continue;
    out.push({
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 冲回/红字请单独说明或单独列示，`
        + '混在结算表里会让合计与实付都算错。',
    });
  }
  return out;
}

/** 多条：合计行逐列复核 */
function checkTotalRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return out;
  let sum = 0;
  let n = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) { sum += v; n += 1; }
  }
  if (!n) return out;
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  out.push({
    level: 'P0', category: '合计行与明细之和不符', line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各门店相加是 ${sum.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

/** 多条：同一门店同一期出现多行 */
function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const s = String(isBlank(it.store) ? '' : it.store).trim();
    const p = String(isBlank(it.period) ? '' : it.period).trim();
    if (!s || !p) continue;
    const key = `${s}|${p}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一门店同一期出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经结算过一次，第 ${it.line} 行又出现一次 —— `
          + '抽成与实付会被重复计算（重复出单或把上期行复制下来最常见）。',
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/** 多条：必需列空白或占位符 */
function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）`
            + '—— 没有这一项就没法勾稽（本期没有就写 0.00，别留空）。',
        });
      }
    }
  }
  return out;
}

/* ============================ 完整档（付费）追加项 ============================ */

/** 单条：抽成比例偏离合同参考区间（合同抽成比例 ± 0.5 个百分点） */
/** 单条：实付为负（扣款超过营业额） */
/** 单条：扣款合计超过营业额 */
/** 单条：营业额与门店上报不一致（差超 2%） */
/** 多条：同一门店同期出现两种抽成比例 */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到结算表正文（text）—— 请把「门店 / 期间 / 营业额 / 抽成比例 / 抽成金额 / '
      + '物料供应款 / 其他扣款 / 实付金额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `结算表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或只有一行合计），没有任何门店明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkCommission(it); if (a) findings.push(a);
    const b = checkNetPay(it); if (b) findings.push(b);
    for (const x of checkNegativeAmounts(it)) findings.push(x);

  }
  for (const role of SUM_ROLES) {
    for (const x of checkTotalRow(t.totals, t.items, role)) findings.push(x);
  }
  for (const x of checkDuplicates(t.items)) findings.push(x);
  for (const x of checkBlanks(t.items)) findings.push(x);


  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const periods = new Set();
  let revenueTotal = 0;
  let netTotal = 0;
  for (const it of t.items) {
    if (!isBlank(it.period)) periods.add(String(it.period).trim());
    const a = normNumber(it.revenue); if (a !== null) revenueTotal += a;
    const b = normNumber(it.net); if (b !== null) netTotal += b;
  }

  const result = {
    status: 'success',
    service_type: 'CHAIN_STORE_SETTLEMENT_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.size,
      revenue_total: round2(revenueTotal),
      net_total: round2(netTotal),
      rate_diff_tolerance: RATE_TOL,
      revenue_diff_tolerance: REVENUE_DIFF_TOL,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periods.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行免费 ${CHECKS_GIVEN.length} 项：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核「营业额 × 抽成比例 = 抽成」「营业额 − 抽成 − 物料供应款 − 其他扣款 = 实付」'
      + '这类表内勾稽，**不规定抽成比例、也不判断保证金该不该收**（以加盟合同为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
