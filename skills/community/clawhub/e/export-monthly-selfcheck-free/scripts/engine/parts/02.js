/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * export-fx-collection-check.js —— 出口报关与收汇核销核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**外贸企业每出口一票、每月做收汇核销与退税申报前**，
 * 财务都要把这票的三件事核到一起 —— **报关金额、应收外汇（扣佣后）、实际已收汇**。
 * 收汇不足会直接卡住**出口退税**与**外汇管理**（核销差额挂账、逾期未收汇要报告）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   应收外汇 = 报关金额 × (1 − 佣金率)
 *   核销差额 = 应收外汇 − 已收汇
 *   每一列的合计 = 各行之和
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**佣金率、汇率与核销差额的合法区间（各笔合同、各银行、各期不同）：
 *    只对"明显超出常见区间"做**提示**并明确标注是参考，不构成外汇/税务意见。
 */

const CHECKS_GIVEN = [
  '应收外汇勾稽（报关金额 × (1 − 佣金率) = 应收外汇）',
  '核销差额勾稽（应收外汇 − 已收汇 = 核销差额）',
  '合计行逐列复核',
  '同一报关单号重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '收汇差额率超过参考上限（5%）提示（参考口径）',
  '已收汇超过报关金额检测',
  '汇率偏离参考区间（6~8）提示（参考口径）',
  '报关金额为零却有收汇检测',
  '佣金率超出参考区间（0~10%）提示（参考口径）',
];

const OUT_OF_SCOPE = [
  '判断某笔出口是否满足退税条件（单证、备案、收汇期限等，以税务与外汇管理规定为准）',
  '判断佣金率、汇率、核销差额是否"合规"（各笔合同与银行口径不同，本工具只提示明显超区间）',
  '处理差额核销、逾期未收汇报告、远期结汇与套期保值',
  '按币种折算或多币种合并（请先在表里折成同一币种）',
  '读取 .xlsx / 银行回单 PDF（需要你先导出成文本贴进来）',
];

/* 参考区间：仅供"明显超出"时提示，不是规定 */
const DIFF_RATE_REF = 0.05;
const FX_RATE_REF = [6, 8];
const COMMISSION_RATE_REF = [0, 0.10];

const SAMPLE_TEXT = [
  '报关单号\t所属期\t报关金额\t佣金率\t应收外汇\t已收汇\t核销差额\t汇率',
  'EXP-2026-001\t2026-01\t100000.00\t2%\t98000.00\t98000.00\t0.00\t7.10',
  'EXP-2026-002\t2026-02\t250000.00\t3%\t242500.00\t242500.00\t0.00\t7.05',
  'EXP-2026-003\t2026-03\t80000.00\t1.5%\t78800.00\t78800.00\t0.00\t6.95',
  '合计\t\t430000.00\t\t419300.00\t419300.00\t0.00\t',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前，更宽泛的词在后
  //    （「应收外汇金额」不能被「收汇金额」抢走；「出口报关单号」先于「报关单号」）
  declNo: ['出口报关单号', '报关单编号', '报关单号', '核销单号', '出口单号'],
  period: ['所属期', '核销期', '出口日期', '申报日期', '所属月份', '期间', '月份'],
  declaredAmount: ['出口报关金额', '报关金额', '报关总额', '出口金额'],
  commissionRate: ['佣金费率', '佣金比例', '佣金率', '扣佣率'],
  receivableFx: ['应收外汇金额', '应收外汇额', '应收外汇', '应收货款'],
  collectedFx: ['已收汇金额', '已收汇额', '实际收汇', '收汇金额', '已收汇'],
  writeOffDiff: ['核销差额金额', '核销差额', '核销差', '差额'],
  fxRate: ['结汇汇率', '记账汇率', '折算汇率', '汇率'],
};

const LABELS = {
  declNo: '报关单号', period: '所属期', declaredAmount: '报关金额', commissionRate: '佣金率',
  receivableFx: '应收外汇', collectedFx: '已收汇', writeOffDiff: '核销差额', fxRate: '汇率',
};

const REQUIRED = ['declNo', 'period', 'declaredAmount', 'commissionRate', 'receivableFx', 'collectedFx', 'writeOffDiff'];
const SUM_ROLES = ['declaredAmount', 'receivableFx', 'collectedFx', 'writeOffDiff'];
const AMOUNT_ROLES = ['declaredAmount', 'receivableFx', 'collectedFx'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|汇总|全年合计|本期合计)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|待核|未知)$/i.test(s);
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

/** 比率归一化成小数：`2%` ⇒ 0.02；`0.02` ⇒ 0.02；`2` ⇒ 0.02 */
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
    roles.forEach((role, c) => {
      if (!role) return;
      const v = cells[c] === undefined ? '' : cells[c];
      row[role] = v;
    });
    const tag = String(row.declNo || row.period || '').trim().replace(/[:：]$/, '');
    if (TOTAL_WORDS.test(tag)) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => (it && it.declNo ? `${String(it.declNo).trim()}（第 ${it.line} 行）` : `第 ${it && it.line} 行`);

/* ================================ 免费档检查项 ================================ */

function checkReceivableFx(it) {
  const declared = normNumber(it.declaredAmount);
  const rate = rateValue(it.commissionRate);
  const stated = normNumber(it.receivableFx);
  if (declared === null || rate === null || stated === null) return null;
  const expect = round2(declared * (1 - rate));
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应收外汇与复算不符', line: it.line,
    message: `${who(it)}：报关金额 ${declared.toFixed(2)} × (1 − 佣金率 ${(rate * 100).toFixed(2)}%) 应为 ${expect.toFixed(2)}，表里应收外汇是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkWriteOffDiff(it) {
  const recv = normNumber(it.receivableFx);
  const coll = normNumber(it.collectedFx);
  const stated = normNumber(it.writeOffDiff);
  if (recv === null || coll === null || stated === null) return null;
  const expect = round2(recv - coll);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '核销差额与复算不符', line: it.line,
    message: `${who(it)}：应收外汇 ${recv.toFixed(2)} − 已收汇 ${coll.toFixed(2)} = ${expect.toFixed(2)}，表里核销差额是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)} —— 差额填错会让收汇核销与退税都对不上。`,
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = String(it.declNo || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一报关单号出现多行', line: it.line,
        message: `${who(it)}：报关单号「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 收汇与退税会被重复计算。`,
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

function checkNegativeAmounts(it) {
  const out = [];
  for (const role of AMOUNT_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v < -TOL) {
      out.push({
        level: 'P0', category: '金额为负', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 冲回或红字请单独列示，不要混在报关与收汇里。`,
      });
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
    return insufficient('没有收到核销表正文（text）—— 请把「报关单号 / 所属期 / 报关金额 / 佣金率 / 应收外汇 / 已收汇 / 核销差额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `核销表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头或只剩合计行，没有任何逐票明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkReceivableFx(it); if (a) findings.push(a);
    const b = checkWriteOffDiff(it); if (b) findings.push(b);
    for (const x of checkNegativeAmounts(it)) findings.push(x);

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

  let declaredTotal = 0;
  let collectedTotal = 0;
  let diffTotal = 0;
  const periods = new Set();
  for (const it of t.items) {
    const a = normNumber(it.declaredAmount); if (a !== null) declaredTotal += a;
    const b = normNumber(it.collectedFx); if (b !== null) collectedTotal += b;
    const c = normNumber(it.writeOffDiff); if (c !== null) diffTotal += c;
    const p = String(it.period === undefined ? '' : it.period).trim();
    if (p) periods.add(p);
  }

  const result = {
    status: 'success',
    service_type: 'EXPORT_FX_COLLECTION_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      checks_executed: CHECKS_GIVEN,
      rows: t.items.length,
      periods: periods.size,
      declared_total: round2(declaredTotal),
      collected_total: round2(collectedTotal),
      write_off_diff_total: round2(diffTotal),
      diff_rate_ref: DIFF_RATE_REF,
      fx_rate_ref: FX_RATE_REF,
      commission_rate_ref: COMMISSION_RATE_REF,
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
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"报关金额 × (1 − 佣金率) = 应收外汇""应收外汇 − 已收汇 = 核销差额"这类内部勾稽，'
      + '**不规定佣金率、汇率与核销差额的合法区间**（以出口合同、结汇水单与外汇管理规定为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, rateValue, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, OUT_OF_SCOPE, SAMPLE_TEXT,
};
