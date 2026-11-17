/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * tax-invoice-void-check.js —— 发票作废与红冲核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月申报前**，财务、税务岗必须把发票作废与红冲过一遍 ——
 * 作废份数、红冲金额必须与申报表、账面收入对得上。红冲开错（多冲 / 少冲 / 方向反）
 * 就是少缴或多缴税，事后只能走更正申报，代价远大于当场核对。这张台账**完全能算出来对错**。
 *
 * 台账里的两条可算关系（都能手算复现）：
 *   净开票金额 = 开票金额 − 作废金额 − 红冲金额
 *   红冲金额   = 原发票金额 − 折让金额（只有发生了红冲的行才适用）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**某张发票"该不该"作废或红冲（那是税收法规与主管税务机关的口径），
 *    只核台账内部的算术与口径是否自洽 —— 结论可由第三方用同一份输入复算。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 */

const CHECKS_GIVEN = [
  '净开票金额勾稽（开票金额 − 作废金额 − 红冲金额 = 净开票金额）',
  '红冲金额勾稽（原发票金额 − 折让金额 = 红冲金额）',
  '合计行逐列复核',
  '同一发票号码重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '红冲金额超过原发票金额检测',
  '作废发票已跨月（应红冲而非作废）提示',
  '作废率超过参考上限（10%）提示（参考口径）',
  '作废或红冲发票无原因说明提示',
  '净开票金额与申报表口径不一致提示（差额超阈值）',
];

const OUT_OF_SCOPE = [
  '判断某张发票该不该作废或红冲、红冲事由是否合规（以税收法规与主管税务机关口径为准）',
  '核对增值税申报表本身的填写是否正确（只做"台账净额 vs 申报表收入"的差额提示，不认定申报是否成立）',
  '读取开票系统 / 电子税务局导出文件（需要你先导成文本贴进来）',
  '判断跨月作废是否已被税务机关受理（只提示"跨月"这一事实）',
];

const SAMPLE_TEXT = [
  '期间\t发票号码\t开票日期\t作废日期\t原发票金额\t开票金额\t作废金额\t红冲金额\t折让金额\t净开票金额\t作废份数\t是否作废\t作废或红冲原因\t申报表收入',
  '2026-01\tA0001\t2026-01-08\t\t0.00\t100000.00\t0.00\t0.00\t0.00\t100000.00\t0\t否\t\t100000.00',
  '2026-01\tA0002\t2026-01-05\t2026-01-18\t0.00\t10000.00\t10000.00\t0.00\t0.00\t0.00\t1\t是\t开票信息有误，当月作废\t0.00',
  '2026-01\tA0003\t2026-01-12\t2026-01-26\t50000.00\t50000.00\t0.00\t40000.00\t10000.00\t10000.00\t0\t否\t部分退货，按折让后金额红冲\t10000.00',
  '2026-02\tA0004\t2026-02-06\t\t0.00\t80000.00\t0.00\t0.00\t0.00\t80000.00\t0\t否\t\t80000.00',
  '合计\t\t\t\t50000.00\t240000.00\t10000.00\t40000.00\t10000.00\t190000.00\t1.00\t\t\t190000.00',
].join('\n');

/* 算术容差（元）：台账按分登记，1 分以内的四舍五入不报 */
const TOL = 0.01;
/* 参考口径：作废金额 / 开票金额，超过这个比例就提示（**参考值**，不是规定） */
const VOID_RATE_REF = 0.1;
/* 申报表口径允许的绝对差额（元）：台账净额与申报表收入相差超过它才提示 */
const DECL_TOL = 1.0;

const ROLES = {
  // ⚠️ 顺序即优先级：**更具体的别名必须排在更宽泛的前面**，否则列会被抢走（静默算错）。
  //    例：「净开票金额」不能被「开票金额」抢走 ⇒ netAmount 必须排在 issuedAmount 之前；
  //    「作废份数 / 作废日期 / 是否作废」不能被「作废金额」抢走 ⇒ 金额角色在前、其余随后。
  period: ['税款所属期', '所属期', '期间', '月份', '月度'],
  invoiceNo: ['发票代码及号码', '发票号码', '发票号', '票号'],
  issueDate: ['开票日期', '开具日期', '发票日期'],
  voidDate: ['作废日期', '红冲日期', '处理日期'],
  netAmount: ['净开票金额', '开票净额', '净开票额'],
  origAmount: ['被红冲原发票金额', '原发票金额', '原票金额'],
  issuedAmount: ['开票金额', '开具金额', '开票总额'],
  voidAmount: ['已作废金额', '作废金额'],
  reversalAmount: ['已红冲金额', '红冲金额', '冲红金额'],
  discountAmount: ['折扣折让金额', '折让金额', '价格折让'],
  voidCount: ['作废份数', '作废张数', '作废数量'],
  voidFlag: ['是否作废', '作废标记', '发票状态'],
  reason: ['作废或红冲原因', '作废原因', '红冲原因', '原因说明', '原因'],
  declaredRevenue: ['申报表销售额', '申报表收入', '申报销售额', '申报收入'],
};

const LABELS = {
  period: '期间', invoiceNo: '发票号码', issueDate: '开票日期', voidDate: '作废日期',
  netAmount: '净开票金额', origAmount: '原发票金额', issuedAmount: '开票金额',
  voidAmount: '作废金额', reversalAmount: '红冲金额', discountAmount: '折让金额',
  voidCount: '作废份数', voidFlag: '是否作废', reason: '作废或红冲原因',
  declaredRevenue: '申报表收入',
};

/* 必需列：少了任何一列就不给结论（**绝不用默认值替买家填**） */
const REQUIRED = ['period', 'invoiceNo', 'origAmount', 'issuedAmount', 'voidAmount',
  'reversalAmount', 'netAmount'];

/* 合计行要逐列复核的数值列 */
const SUM_ROLES = ['origAmount', 'issuedAmount', 'voidAmount', 'reversalAmount',
  'discountAmount', 'netAmount', 'voidCount', 'declaredRevenue'];

/* 金额为负检测覆盖的列 */
const AMOUNT_ROLES = ['origAmount', 'issuedAmount', 'voidAmount', 'reversalAmount',
  'discountAmount', 'netAmount'];

const TOTAL_WORDS = /^(合计|总计|小计|共计|本期合计|累计)$/;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。'
      + '把「发票作废与红冲台账」的**表头 + 明细行**一起贴进来（Tab 分隔最稳），'
      + '必需列缺一列都会在这里停下。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|暂无)$/i.test(s);
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
      if (role === 'period' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; } else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => (it && !isBlank(it.period) ? `${String(it.period).trim()} 期` : `第 ${it && it.line} 行`);
const how = (it) => `（第 ${it.line} 行，发票号码 ${isBlank(it.invoiceNo) ? '未填' : String(it.invoiceNo).trim()}）`;

/* ================================ 免费档检查项 ================================ */

/* 净开票金额 = 开票金额 − 作废金额 − 红冲金额 */
function checkNetRecompute(it) {
  const out = [];
  const issued = normNumber(it.issuedAmount);
  const voided = normNumber(it.voidAmount);
  const rev = normNumber(it.reversalAmount);
  const net = normNumber(it.netAmount);
  if (issued === null || voided === null || rev === null || net === null) return out;
  const expect = round2(issued - voided - rev);
  if (Math.abs(expect - net) <= TOL) return out;
  out.push({
    level: 'P0', category: '净开票金额勾稽不符', line: it.line,
    message: `${who(it)}${how(it)}：开票金额 ${issued.toFixed(2)} − 作废金额 ${voided.toFixed(2)} `
      + `− 红冲金额 ${rev.toFixed(2)} = ${expect.toFixed(2)}，表里净开票金额是 ${net.toFixed(2)}，`
      + `相差 ${round2(net - expect).toFixed(2)}。`,
  });
  return out;
}

/* 红冲金额 = 原发票金额 − 折让金额（只对发生了红冲的行适用） */
function checkReversalRecompute(it) {
  const out = [];
  const orig = normNumber(it.origAmount);
  const disc = normNumber(it.discountAmount);
  const rev = normNumber(it.reversalAmount);
  if (orig === null || disc === null || rev === null) return out;
  if (Math.abs(rev) <= TOL) return out;
  const expect = round2(orig - disc);
  if (Math.abs(expect - rev) <= TOL) return out;
  out.push({
    level: 'P0', category: '红冲金额勾稽不符', line: it.line,
    message: `${who(it)}${how(it)}：原发票金额 ${orig.toFixed(2)} − 折让金额 ${disc.toFixed(2)} `
      + `= ${expect.toFixed(2)}，表里红冲金额是 ${rev.toFixed(2)}，相差 ${round2(rev - expect).toFixed(2)}`
      + ' —— 红冲方向或多冲少冲会直接影响当期申报收入。',
  });
  return out;
}

/* 金额为负（本表的金额一律按正数绝对值登记，红冲填进「红冲金额」列） */
function checkNegativeAmount(it) {
  const out = [];
  for (const role of AMOUNT_ROLES) {
    const v = normNumber(it[role]);
    if (v === null || v >= -TOL) continue;
    out.push({
      level: 'P1', category: '金额为负', line: it.line,
      message: `${who(it)}${how(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）`
        + ' —— 本表按正数登记发生额；红冲请填在「红冲金额」列，不要用负号表达。',
    });
  }
  return out;
}

/* 合计行逐列复核 */
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，明细行相加是 ${sum.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

/* 同一发票号码出现多行（作废/红冲金额会被重复计算） */
function checkDuplicateInvoice(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = String(it.invoiceNo === undefined || it.invoiceNo === null ? '' : it.invoiceNo).trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一发票号码出现多行', line: it.line,
        message: `${who(it)}的发票号码 ${key} 已在第 ${seen.get(key)} 行出现，第 ${it.line} 行再次出现`
          + ' —— 若两行是同一张票，作废份数与红冲金额会被重复计算；若是不同票请分开编号。',
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/* 必需列的空白与占位符 */
function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}${how(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）`
            + ' —— 缺了它这条勾稽就不成立，本工具不替它套默认值。',
        });
      }
    }
  }
  return out;
}

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到台账正文（text）—— 请把「发票作废与红冲台账」的'
      + '「期间 / 发票号码 / 原发票金额 / 开票金额 / 作废金额 / 红冲金额 / 净开票金额」这些列表头连同明细行一起贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `台账缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何发票明细行');
  }

  const findings = [];
  for (const it of t.items) {
    for (const f of checkNetRecompute(it)) findings.push(f);
    for (const f of checkReversalRecompute(it)) findings.push(f);
    for (const f of checkNegativeAmount(it)) findings.push(f);

  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicateInvoice(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);


  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const periodSet = new Set();
  let netTotal = 0;
  for (const it of t.items) {
    periodSet.add(isBlank(it.period) ? '(未填期间)' : String(it.period).trim());
    const a = normNumber(it.netAmount);
    if (a !== null) netTotal += a;
  }

  const result = {
    status: 'success',
    service_type: 'TAX_INVOICE_VOID_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periodSet.size,
      net_issued_total: round2(netTotal),
      void_rate_ref: VOID_RATE_REF,
      declared_tolerance: DECL_TOL,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periodSet.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核台账内部的算术与口径勾稽（净开票金额 = 开票金额 − 作废金额 − 红冲金额、'
      + '红冲金额 = 原发票金额 − 折让金额、合计勾稽、申报表口径差额），'
      + '**不判断**某张发票该不该作废或红冲（以税收法规与主管税务机关口径为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
