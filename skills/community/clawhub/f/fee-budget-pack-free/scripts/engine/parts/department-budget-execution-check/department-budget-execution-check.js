/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * department-budget-execution-check.js —— 部门费用预算执行核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月管理会计结账 / 预算执行分析前**，都要把
 * 「部门费用预算执行表」逐部门逐科目勾一遍 —— 预算、已发生、剩余额度、执行率、超支
 * 这五个数在同一条明细行里**必须自洽**（剩余 = 预算 − 已发生；执行率 = 已发生 ÷ 预算）。
 * 只要有一处对不上，整张部门费用分析表就是错的，而超支还牵涉下月预算调整与考核。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   剩余额度 = 预算金额 − 已发生金额
 *   执行率   = 已发生金额 ÷ 预算金额
 *   合计行   = 各明细行逐列相加（预算 / 已发生 / 剩余 / 超支）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断预算额度本身定得合不合理**（那是预算编制与审批的事）：
 *    只核表内算术与勾稽；参考口径（如执行率上限 100%）只做**提示**并明确标注是参考。
 */

const CHECKS_GIVEN = [
  '剩余额度 = 预算金额 − 已发生金额 复算',
  '执行率 = 已发生金额 ÷ 预算金额 复算',
  '合计行逐列复核',
  '同一部门同一科目重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '超支金额与执行率矛盾检测',
  '执行率超过参考上限（100%）提示（参考口径）',
  '预算为零却有发生额检测',
  '已发生为负（冲销未标注）提示',
  '同一科目跨部门预算重复分配提示',
];

const OUT_OF_SCOPE = [
  '判断部门预算额度本身定得是否合理（预算编制口径与审批权限不在本工具范围）',
  '核对费用科目/部门的归属是否正确（这笔费用该记哪个部门哪个科目需人工判断）',
  '处理跨期调整、预算追加与结转（请提供调整后的执行表）',
  '读取 ERP / 费控系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '期间\t部门\t费用科目\t预算金额\t已发生金额\t剩余额度\t执行率\t超支金额',
  '2026-01\t销售部\t差旅费\t120000.00\t78000.00\t42000.00\t65%\t0.00',
  '2026-01\t销售部\t业务招待费\t80000.00\t80000.00\t0.00\t100%\t0.00',
  '2026-01\t研发部\t差旅费\t150000.00\t96000.00\t54000.00\t64%\t0.00',
  '2026-02\t销售部\t差旅费\t120000.00\t95000.00\t25000.00\t79.17%\t0.00',
  '2026-02\t研发部\t差旅费\t150000.00\t118000.00\t32000.00\t78.67%\t0.00',
  '2026-02\t研发部\t材料费\t60000.00\t21000.00\t39000.00\t35%\t0.00',
  '合计\t\t\t680000.00\t488000.00\t192000.00\t\t0.00',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;

/* ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的别名之前。
   「剩余额度 / 执行率 / 预算科目」都含「预算」二字 —— 若把「预算」放在它们前面，
   这两列会被 budget 角色抢走，于是**整列静默地不参与任何检查**（不报错、只算错）。
   同理「年度预算」会被 period 的「年度」抢走、「部门预算」会被 department 的「部门」抢走。 */
const ROLES = {
  subject: ['费用科目', '预算科目', '科目名称', '费用项目', '费用类别', '科目'],
  remaining: ['剩余额度', '剩余预算', '预算余额', '剩余可用额度', '剩余可用', '剩余'],
  rate: ['执行率', '预算执行率', '执行比例', '执行进度'],
  overspend: ['超支金额', '超预算金额', '超支额', '超支'],
  actual: ['已发生金额', '已发生额', '实际发生额', '实际发生', '已执行金额', '已发生', '实际支出'],
  budget: ['预算金额', '部门预算', '年度预算', '预算数', '预算'],
  department: ['部门名称', '费用部门', '责任部门', '归口部门', '部门', '成本中心'],
  period: ['期间', '月份', '所属期', '会计期间', '年度'],
};

const LABELS = {
  period: '期间', department: '部门', subject: '费用科目', budget: '预算金额',
  actual: '已发生金额', remaining: '剩余额度', rate: '执行率', overspend: '超支金额',
};

const REQUIRED = ['period', 'department', 'subject', 'budget', 'actual', 'remaining', 'rate', 'overspend'];
const SUM_ROLES = ['budget', 'actual', 'remaining', 'overspend'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|全年合计)$/;

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

/** 比率归一化成小数：`65%` ⇒ 0.65；`0.65` ⇒ 0.65；`65` ⇒ 0.65 */
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
      if (role === 'period' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const bits = [it && it.period, it && it.department, it && it.subject]
    .map((x) => String(x === undefined || x === null ? '' : x).trim())
    .filter(Boolean);
  return bits.length ? bits.join(' · ') : `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */

function checkRemainingRecalc(it) {
  const out = [];
  const budget = normNumber(it.budget);
  const actual = normNumber(it.actual);
  const stated = normNumber(it.remaining);
  if (budget === null || actual === null || stated === null) return out;
  const expect = round2(budget - actual);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '剩余额度与预算减已发生不符', line: it.line,
    message: `${who(it)}：预算金额 ${budget.toFixed(2)} − 已发生金额 ${actual.toFixed(2)} 应为 ${expect.toFixed(2)}，表里剩余额度是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  });
  return out;
}

function checkRateRecalc(it) {
  const out = [];
  const budget = normNumber(it.budget);
  const actual = normNumber(it.actual);
  const rate = rateValue(it.rate);
  if (budget === null || actual === null || rate === null) return out;
  if (Math.abs(budget) <= TOL) return out;   // 预算为零：除法无定义，交由完整档的「预算为零却有发生额」检查
  const expect = actual / budget;
  if (Math.abs(expect - rate) <= RATE_TOL) return out;
  out.push({
    level: 'P0', category: '执行率与已发生除以预算不符', line: it.line,
    message: `${who(it)}：已发生金额 ${actual.toFixed(2)} ÷ 预算金额 ${budget.toFixed(2)} = ${(expect * 100).toFixed(2)}%，表里执行率是 ${(rate * 100).toFixed(2)}%，相差 ${round2((rate - expect) * 100).toFixed(2)} 个百分点。`,
  });
  return out;
}

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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = [it.period, it.department, it.subject]
      .map((x) => String(x === undefined || x === null ? '' : x).trim()).join('|');
    if (key === '||') continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一部门同一科目重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 同一期间、同一部门、同一科目重复登记，预算与已发生都会被重复计算。`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
        });
      }
    }
  }
  return out;
}

function checkNegativeAmount(it) {
  const out = [];
  for (const role of ['budget', 'actual', 'remaining', 'overspend']) {
    const v = normNumber(it[role]);
    if (v === null || v >= -TOL) continue;
    out.push({
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 冲销/红字与超支要单独列示并标注，否则会被当成正常金额参与勾稽。`,
    });
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到执行表正文（text）—— 请把「期间 / 部门 / 费用科目 / 预算金额 / 已发生金额 / 剩余额度 / 执行率 / 超支金额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `执行表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或只有合计行），没有任何明细行');
  }

  const findings = [];
  for (const it of t.items) {
    for (const a of checkRemainingRecalc(it)) findings.push(a);
    for (const b of checkRateRecalc(it)) findings.push(b);
    for (const c of checkNegativeAmount(it)) findings.push(c);

  }

  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const rows = t.items.length;
  const periodKeys = new Set();
  let budgetTotal = 0; let actualTotal = 0; let remainingTotal = 0; let overspendTotal = 0;
  for (const it of t.items) {
    const p = String(it.period === undefined || it.period === null ? '' : it.period).trim();
    if (p) periodKeys.add(p);
    const a = normNumber(it.budget); if (a !== null) budgetTotal += a;
    const b = normNumber(it.actual); if (b !== null) actualTotal += b;
    const c = normNumber(it.remaining); if (c !== null) remainingTotal += c;
    const d = normNumber(it.overspend); if (d !== null) overspendTotal += d;
  }
  const periods = periodKeys.size;

  const result = {
    status: 'success',
    service_type: 'DEPARTMENT_BUDGET_EXECUTION_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: rows,
      periods: periods,
      budget_total: round2(budgetTotal),
      actual_total: round2(actualTotal),
      remaining_total: round2(remainingTotal),
      overspend_total: round2(overspendTotal),
      rate_ref_cap: 1,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: rows,
      periods: periods,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"剩余额度 = 预算金额 − 已发生金额""执行率 = 已发生金额 ÷ 预算金额""合计 = 明细逐列相加"'
      + '这类表内勾稽，**不判断预算额度定得合不合理**（以预算编制与审批口径为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, rateValue, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
