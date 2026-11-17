/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * ap-aging-plan-check.js —— 应付账款账龄与付款计划核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月资金计划会之前**，财务要把应付账款的账龄与付款计划核一遍 ——
 * 哪些逾期了、逾多久、这个月计划付多少、实际付了多少。这张表直接决定**资金安排与供应商关系**：
 * 逾期金额算错会误判资金缺口；计划付款超过应付余额会排错预算。每月必做，且完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   逾期金额 ≤ 应付余额（逾期的部分不可能超过欠款总额）
 *   付款计划 ≤ 应付余额（不能安排超过欠款的付款）
 *   计划付款 − 本期实付 = 待付差额
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**该不该付款、账龄口径是否合理，只核表内勾稽与常见阈值。
 */

const CHECKS_GIVEN = [
  '逾期金额超过应付余额检测',
  '本期实付超过计划付款检测',
  '应付余额为负检测',
  '合计行逐列复核',
  '重复供应商检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '逾期天数超过 90 天提示（长账龄）',
  '实付与计划差异超阈值（10%）检测',
  '逾期金额与逾期天数矛盾检测',
  '应付余额为零却有付款检测',
  '计划付款超过应付余额检测',
];

const OUT_OF_SCOPE = [
  '判断该不该付款、付款优先级与供应商信用政策',
  '计算应付账款周转率、现金折扣与融资成本',
  '核对采购合同、入库单与发票的三单匹配（请用三单匹配核对）',
  '读取 ERP 或资金系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '供应商\t应付余额\t其中逾期金额\t逾期天数\t计划付款金额\t本期实付',
  '豫州建材有限公司\t380000.00\t0.00\t0\t300000.00\t300000.00',
  '中岳设备租赁有限公司\t120000.00\t120000.00\t45\t60000.00\t60000.00',
  '豫通物流有限公司\t45000.00\t0.00\t0\t45000.00\t45000.00',
  '合计\t545000.00\t120000.00\t\t405000.00\t405000.00',
].join('\n');

const TOL = 0.01;
const LONG_DAYS = 90;            // 长账龄提示阈值
const PAY_DIFF_CAP = 0.10;       // 实付与计划差异阈值 10%

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前（「其中逾期金额」不能被「应付余额」抢走）
  supplier: ['供应商', '往来单位', '收款单位', '单位名称'],
  balance: ['应付余额', '应付账款余额', '欠款余额'],
  overdueAmt: ['其中逾期金额', '逾期金额', '逾期应付'],
  overdueDays: ['逾期天数', '账龄天数', '最长逾期天数'],
  plannedPay: ['计划付款金额', '计划付款', '本月计划付款'],
  actualPay: ['本期实付', '实际付款', '已付金额'],
};

const LABELS = {
  supplier: '供应商', balance: '应付余额', overdueAmt: '其中逾期金额',
  overdueDays: '逾期天数', plannedPay: '计划付款金额', actualPay: '本期实付',
};

const REQUIRED = ['supplier', 'balance', 'overdueAmt', 'plannedPay', 'actualPay'];
const SUM_ROLES = ['balance', 'overdueAmt', 'plannedPay', 'actualPay'];
const TOTAL_WORDS = /^(合计|总计|小计|共计)$/;

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
      if (role === 'supplier' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => (it && it.supplier ? String(it.supplier) : `第 ${it && it.line} 行`);

/* ================================ 免费档检查项 ================================ */

function checkOverdueOverBalance(it) {
  const bal = normNumber(it.balance);
  const od = normNumber(it.overdueAmt);
  if (bal === null || od === null) return null;
  if (od <= bal + TOL) return null;
  return {
    level: 'P0', category: '逾期金额超过应付余额', line: it.line,
    message: `${who(it)}的逾期金额 ${od.toFixed(2)} 超过应付余额 ${bal.toFixed(2)} —— 逾期的部分不可能超过欠款总额。`,
  };
}

function checkPayOverPlan(it) {
  const plan = normNumber(it.plannedPay);
  const act = normNumber(it.actualPay);
  if (plan === null || act === null) return null;
  if (act <= plan + TOL) return null;
  return {
    level: 'P0', category: '本期实付超过计划付款', line: it.line,
    message: `${who(it)}本期计划付 ${plan.toFixed(2)}，实际付了 ${act.toFixed(2)}，超出 ${round2(act - plan).toFixed(2)} —— 超计划付款要有审批依据。`,
  };
}

function checkNegativeBalance(it) {
  const v = normNumber(it.balance);
  if (v === null || v >= -TOL) return null;
  return {
    level: 'P0', category: '应付余额为负', line: it.line,
    message: `${who(it)}的应付余额是 ${v.toFixed(2)}（负数）—— 预付或退款建议单独列示。`,
  };
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
    const key = String(it.supplier || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一供应商出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 请合并或按合同分行并注明。`,
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

/* ============================ 完整档（付费）检查项 ============================ */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到台账正文（text）—— 请把「供应商 / 应付余额 / 逾期金额 / 逾期天数 / 计划付款 / 本期实付」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `台账缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何供应商明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkOverdueOverBalance(it); if (a) findings.push(a);
    const b = checkPayOverPlan(it); if (b) findings.push(b);
    const c = checkNegativeBalance(it); if (c) findings.push(c);

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

  let balTotal = 0; let odTotal = 0; let plannedTotal = 0; let paidTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.balance); if (a !== null) balTotal += a;
    const b = normNumber(it.overdueAmt); if (b !== null) odTotal += b;
    const c = normNumber(it.plannedPay); if (c !== null) plannedTotal += c;
    const d = normNumber(it.actualPay); if (d !== null) paidTotal += d;
  }

  const result = {
    status: 'success',
    service_type: 'AP_AGING_PLAN_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      suppliers: t.items.length,
      balance_total: round2(balTotal),
      overdue_total: round2(odTotal),
      planned_total: round2(plannedTotal),
      paid_total: round2(paidTotal),
      unpaid_plan_total: round2(plannedTotal - paidTotal),
      long_aging_days: LONG_DAYS,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      suppliers: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核账龄与付款计划的表内勾稽，**不判断该不该付款**；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
