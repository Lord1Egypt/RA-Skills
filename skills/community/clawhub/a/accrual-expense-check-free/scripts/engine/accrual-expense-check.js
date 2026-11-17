/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * accrual-expense-check.js —— 预提费用与到票冲销核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**月末结账前**，财务要把预提费用核一遍 ——
 * 该属于本月的费用先按估计**计提**（记负债），下月发票到了再**冲销**预提、正式入账。
 * 这条链最容易出两种错：**只计提不冲销**（负债虚增、费用重复）与**冲销超过计提**（负债变负）。
 * 它也是**审计与所得税汇算的常查项**。每月必做，且完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   期末预提余额 = 期初预提余额 + 本期计提 − 本期到票冲销
 *   到票冲销不得超过「期初余额 + 本期计提」（没预提过就不能冲）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**预提金额是否合理（估计数与合同/预算有关），只核台账内部勾稽。
 */

const CHECKS_GIVEN = [
  '期末预提勾稽（期初 + 计提 − 到票冲销 = 期末）',
  '期末预提余额为负检测',
  '计提或冲销为负检测',
  '合计行逐列复核',
  '重复项目检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '到票冲销超过可用预提（期初 + 本期计提）检测',
  '期末余额超过本期计提（挂账超过一期）检测',
  '本期无计提却有冲销检测',
  '冲销与计提比例异常检测（冲销 ÷ 计提 > 1.5）',
  '期初余额为负检测',
];

const OUT_OF_SCOPE = [
  '判断预提金额是否合理、该不该预提（那属于会计估计与政策）',
  '处理跨年预提、汇算清缴纳税调整',
  '核对发票真伪与进项抵扣（请用进项税额认证与抵扣核对）',
  '读取 ERP 或发票系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '项目名称\t期初预提余额\t本期计提\t本期到票冲销\t期末预提余额',
  '12月水电费\t18000.00\t20000.00\t18000.00\t20000.00',
  '第四季度审计费\t60000.00\t0.00\t60000.00\t0.00',
  '年终奖金\t0.00\t120000.00\t0.00\t120000.00',
  '合计\t78000.00\t140000.00\t78000.00\t140000.00',
].join('\n');

const TOL = 0.01;
const RATIO_CAP = 1.5;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前（「期初预提余额」不能被宽泛的「余额」抢走）
  item: ['项目名称', '费用项目', '预提项目', '项目'],
  openBalance: ['期初预提余额', '期初预提', '上期预提余额'],
  accrued: ['本期计提', '计提金额', '本期预提'],
  offset: ['本期到票冲销', '到票冲销', '本期冲销', '冲销金额'],
  closeBalance: ['期末预提余额', '期末预提', '预提余额'],
};

const LABELS = {
  item: '项目名称', openBalance: '期初预提余额', accrued: '本期计提',
  offset: '本期到票冲销', closeBalance: '期末预提余额',
};

const REQUIRED = ['item', 'openBalance', 'accrued', 'offset', 'closeBalance'];
const SUM_ROLES = ['openBalance', 'accrued', 'offset', 'closeBalance'];
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
      if (role === 'item' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => (it && it.item ? String(it.item) : `第 ${it && it.line} 行`);

/* ================================ 免费档检查项 ================================ */

function checkIdentity(it) {
  const open = normNumber(it.openBalance);
  const acc = normNumber(it.accrued);
  const off = normNumber(it.offset);
  const close = normNumber(it.closeBalance);
  if ([open, acc, off, close].some((v) => v === null)) return null;
  const expect = round2(open + acc - off);
  if (Math.abs(expect - close) <= TOL) return null;
  return {
    level: 'P0', category: '期末预提勾稽不符', line: it.line,
    message: `${who(it)}：期初 ${open.toFixed(2)} + 本期计提 ${acc.toFixed(2)} − 到票冲销 ${off.toFixed(2)} 应为 ${expect.toFixed(2)}，表里期末写的是 ${close.toFixed(2)}，相差 ${round2(close - expect).toFixed(2)}。`,
  };
}

function checkNegativeClose(it) {
  const v = normNumber(it.closeBalance);
  if (v === null || v >= -TOL) return null;
  return {
    level: 'P0', category: '期末预提余额为负', line: it.line,
    message: `${who(it)}的期末预提余额是 ${v.toFixed(2)}（负数）—— 预提是负债，负数说明冲销超过了计提。`,
  };
}

function checkNegativeFlow(it) {
  const out = [];
  for (const [role, label] of [['accrued', '本期计提'], ['offset', '本期到票冲销']]) {
    const v = normNumber(it[role]);
    if (v !== null && v < -TOL) {
      out.push({
        level: 'P0', category: '计提或冲销为负', line: it.line,
        message: `${who(it)}的「${label}」是 ${v.toFixed(2)}（负数）—— 冲回建议单独列示。`,
      });
    }
  }
  return out;
}

function checkTotalRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return out;
  let sum = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) sum += v;
  }
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
    const key = String(it.item || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一项目出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 预提会被重复计算。`,
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
    return insufficient('没有收到台账正文（text）—— 请把「项目 / 期初预提余额 / 本期计提 / 本期到票冲销 / 期末预提余额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `台账缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何项目明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkIdentity(it); if (a) findings.push(a);
    const b = checkNegativeClose(it); if (b) findings.push(b);
    for (const x of checkNegativeFlow(it)) findings.push(x);

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

  let closeTotal = 0; let accruedTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.closeBalance); if (a !== null) closeTotal += a;
    const b = normNumber(it.accrued); if (b !== null) accruedTotal += b;
  }

  const result = {
    status: 'success',
    service_type: 'ACCRUAL_EXPENSE_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      items: t.items.length,
      closing_balance_total: round2(closeTotal),
      accrued_total: round2(accruedTotal),
      ratio_cap: RATIO_CAP,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      items: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核预提台账的内部勾稽（计提/到票冲销/余额），**不判断预提金额是否合理**；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
