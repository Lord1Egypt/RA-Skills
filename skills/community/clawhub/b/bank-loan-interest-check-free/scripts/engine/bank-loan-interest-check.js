/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * bank-loan-interest-check.js —— 银行贷款利息与还款计划核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月结账前**。有银行贷款的公司，财务每个月都要
 * 计提利息、按还款计划还本付息；遇到 LPR 重定价（利率调整）还要按新的执行利率重算计划。
 * 这张表算错，方向只有两个 —— **少计财务费用**（利息提少了，利润虚高）或
 * **多付利息 / 本金还错**（还款计划与银行对账单对不上）。两条都会在月报、审计抽样
 * 和银行对账上暴露出来。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   本期利息   = 期初本金余额 × 年利率 ÷ 12 × 计息月数
 *   期末本金   = 期初本金 − 本期还本
 *   合计行各列 = 明细行相加（合同金额按合同去重，同一合同的多期明细只算一次）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**该笔贷款该按什么口径计提利息、LPR 重定价是否本期生效（那属于合同与
 *    会计判断）：表里给的合同金额、合同利率、合同期数、期初本金、年利率一律**以你填的为准**，
 *    本工具只核表内勾稽，并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '本期利息复算（期初本金 × 年利率 ÷ 12 × 计息月数 = 本期利息）',
  '期末本金滚动复算（期初本金 − 本期还本 = 期末本金）',
  '合计行逐列复核',
  '同一贷款合同同一期间重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '利息与本金×利率×期数不符提示（合同口径粗算，超容差才报）',
  '本期还本额超过期初本金检测',
  '还款计划合计与合同金额不符提示',
  '利率与合同利率不一致提示（LPR 重定价未更新）',
  '本金已还清仍计提利息提示',
];

const OUT_OF_SCOPE = [
  '判断该笔贷款该按什么口径计提利息（合同利率、LPR 加点、实际利率法、是否含复利与罚息，属于会计与合同判断，请咨询会计师）',
  '核对借款合同条款本身（提前还款、展期、罚息、复利、承诺费、手续费）对还款计划的影响',
  '判断 LPR 重定价是否应当在本期生效（重定价日与重定价周期的认定属于合同条款判断）',
  '处理外币贷款折算、增值税、印花税、财政贴息与政府补助的会计与税务处理',
  '读取网银 / 信贷系统 / ERP 导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t贷款银行\t贷款合同号\t合同金额\t合同利率\t合同期数\t期初本金\t年利率\t计息月数\t本期利息\t本期还本\t期末本金\t本期还款额',
  '2026-01\t工商银行\tHT-2026-001\t600000.00\t3.45%\t3\t600000.00\t3.45%\t1\t1725.00\t0.00\t600000.00\t1725.00',
  '2026-02\t工商银行\tHT-2026-001\t600000.00\t3.45%\t3\t600000.00\t3.45%\t1\t1725.00\t0.00\t600000.00\t1725.00',
  '2026-03\t工商银行\tHT-2026-001\t600000.00\t3.45%\t3\t600000.00\t3.45%\t1\t1725.00\t600000.00\t0.00\t601725.00',
  '2026-01\t建设银行\tHT-2026-002\t300000.00\t4.20%\t3\t300000.00\t4.20%\t1\t1050.00\t100000.00\t200000.00\t101050.00',
  '2026-02\t建设银行\tHT-2026-002\t300000.00\t4.20%\t3\t200000.00\t4.20%\t1\t700.00\t100000.00\t100000.00\t100700.00',
  '2026-03\t建设银行\tHT-2026-002\t300000.00\t4.20%\t3\t100000.00\t4.20%\t1\t350.00\t100000.00\t0.00\t100350.00',
  '合计\t\t\t900000.00\t\t\t2400000.00\t\t\t7275.00\t900000.00\t1500000.00\t907275.00',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;      // 利率容差：0.05 个百分点
const COARSE_TOL = 0.7;       // 合同口径利息粗算容差：70%（等额本息/等额本金与粗算天然有差）

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前（「期末本金」不能被「期初本金」抢走、
  //    「本期还款额」「本期还本付息」不能被「本期还本」抢走、「合同利率」不能被「利率」抢走）
  period: ['所属期间', '会计期间', '所属期', '期间', '月份', '月度'],
  bank: ['贷款银行', '放款银行', '借款银行', '开户银行', '银行名称', '银行'],
  contract: ['贷款合同编号', '借款合同编号', '贷款合同号', '借款合同号', '贷款借据号', '借据号', '合同编号', '合同号'],
  contractAmount: ['合同借款金额', '合同金额', '借款金额', '贷款金额', '授信金额', '借款本金', '合同本金'],
  contractRate: ['合同利率', '合同年利率', '合同约定利率', '约定利率', '合同执行利率'],
  contractMonths: ['合同期数', '合同月数', '借款期数', '贷款期数', '还款期数', '贷款期限'],
  principalBegin: ['期初本金余额', '期初贷款余额', '上期期末本金', '期初本金', '期初余额'],
  rate: ['年利率', '贷款年利率', '执行利率', '年化利率', '月利率', '利率'],
  months: ['计息月数', '计息期数', '本期计息月数', '计息月份', '月数'],
  interest: ['本期利息', '本期计提利息', '本期应付利息', '应付利息', '利息支出', '利息金额', '利息'],
  repayTotal: ['本期还款额', '本期还本付息', '本期应还金额', '本期还款合计', '月供', '还款额'],
  principalPay: ['本期还本', '本期还本金', '本期归还本金', '本期偿还本金', '还本金额', '归还本金', '还本'],
  principalEnd: ['期末本金余额', '期末贷款余额', '下期期初本金', '期末本金', '期末余额'],
};

const LABELS = {
  period: '所属期间', bank: '贷款银行', contract: '贷款合同号', contractAmount: '合同金额',
  contractRate: '合同利率', contractMonths: '合同期数', principalBegin: '期初本金', rate: '年利率',
  months: '计息月数', interest: '本期利息', principalPay: '本期还本', principalEnd: '期末本金',
  repayTotal: '本期还款额',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'contract', 'contractAmount', 'principalBegin', 'rate', 'months',
  'interest', 'principalPay', 'principalEnd'];
/** 合计行逐列复核的列 */
const SUM_ROLES = ['contractAmount', 'principalBegin', 'interest', 'principalPay', 'principalEnd', 'repayTotal'];
/** 这几列是**按合同**的口径（同一合同的多期明细里，合同金额只算一次，否则会被重复加总） */
const PER_CONTRACT_ROLES = ['contractAmount'];
/**
 * 免费档负值检测覆盖的列：**还款侧**的金额与利率。
 * ⚠️ 刻意**不含**期末本金 —— "还本额超过期初本金"是完整档的独立检查项（见 CHECKS_WITHHELD），
 *    免费档提前报出期末本金为负就等于把付费结论送出去了。
 */
const NEGATIVE_ROLES = ['contractAmount', 'principalBegin', 'interest', 'principalPay', 'repayTotal', 'rate'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|合计：|汇总)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|空)$/i.test(s);
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

/** 利率归一化成小数：`4.35%` ⇒ 0.0435；`0.0435` ⇒ 0.0435；`4.35` ⇒ 0.0435 */
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
  const p = it && it.period !== undefined && String(it.period).trim() !== ''
    ? String(it.period).trim() : `第 ${it && it.line} 行`;
  const n = [it && it.bank, it && it.contract]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

const contractKeyOf = (it) => {
  const c = it && it.contract !== undefined ? String(it.contract).trim() : '';
  return c || `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkInterestRecompute(it) {
  const out = [];
  const principal = normNumber(it.principalBegin);
  const rate = rateValue(it.rate);
  const months = normNumber(it.months);
  const stated = normNumber(it.interest);
  if (principal === null || rate === null || months === null || stated === null) return out;
  if (months <= 0) return out;                 // 计息月数填 0 或负：算不出本期利息（负值由负值检测报）
  const expect = round2(principal * rate / 12 * months);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '本期利息复算不符', line: it.line,
    message: `${who(it)}：期初本金 ${principal.toFixed(2)} × 年利率 ${(rate * 100).toFixed(4)}% ÷ 12 × 计息月数 ${months} = ${expect.toFixed(2)}，`
      + `表里「本期利息」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '每月利息就是"期初本金 × 年利率 ÷ 12 × 计息月数"，提少了就是少计财务费用，提多了就是多计费用。',
  });
  return out;
}

function checkPrincipalRolling(it) {
  const out = [];
  const begin = normNumber(it.principalBegin);
  const pay = normNumber(it.principalPay);
  const stated = normNumber(it.principalEnd);
  if (begin === null || pay === null || stated === null) return out;
  const expect = round2(begin - pay);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '期末本金滚动复算不符', line: it.line,
    message: `${who(it)}：期初本金 ${begin.toFixed(2)} − 本期还本 ${pay.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「期末本金」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '本金余额滚不动，后面每一期的利息都会跟着错（利息是按本金余额算的）。',
  });
  return out;
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals || !totals.row) return out;
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let expect = null;
    let how = '';
    if (PER_CONTRACT_ROLES.indexOf(role) >= 0) {
      const first = new Map();
      for (const it of items) {
        const v = normNumber(it[role]);
        if (v !== null && !first.has(contractKeyOf(it))) first.set(contractKeyOf(it), v);
      }
      if (!first.size) continue;
      expect = round2(Array.from(first.values()).reduce((a, b) => a + b, 0));
      how = `按合同去重后 ${first.size} 笔合同的「${LABELS[role]}」相加`;
    } else {
      let sum = 0;
      let n = 0;
      for (const it of items) {
        const v = normNumber(it[role]);
        if (v !== null) { sum += v; n += 1; }
      }
      if (!n) continue;
      expect = round2(sum);
      how = `本表 ${n} 行明细的「${LABELS[role]}」相加`;
    }
    if (Math.abs(stated - expect) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，${how}是 ${expect.toFixed(2)}，`
        + `相差 ${round2(stated - expect).toFixed(2)}。合计行就是月报与银行对账单的取数口径，对不上说明有一边错。`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined ? String(it.period).trim() : '';
    const c = it.contract !== undefined ? String(it.contract).trim() : '';
    if (!p || !c) continue;
    const key = `${p}|${c}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一贷款合同重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一期间、同一合同再次出现 —— `
          + '要么是重复粘贴了一行，要么是同一笔贷款被拆成两行（比如分次提款各建一行），'
          + '多出来的那一行会把利息与还本都重复计一遍。',
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`
            + '这一列缺失时对应的复算做不了：缺哪一列就补哪一列，别让空值静默跳过检查。',
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = role === 'rate' ? rateValue(it[role]) : normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    const shown = role === 'rate' ? `${(v * 100).toFixed(4)}%` : v.toFixed(2);
    out.push({
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${shown}（负数）—— 合同金额、本金余额、利息与还本都不该为负，`
        + '冲回 / 红字应单独列示并在备注里说明。',
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
    return insufficient('没有收到银行贷款利息与还款计划核对表正文（text）—— 请把「所属期间 / 贷款银行 / 贷款合同号 / 合同金额 / 合同利率 / 合同期数 / 期初本金 / 年利率 / 计息月数 / 本期利息 / 本期还本 / 期末本金」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `银行贷款利息与还款计划核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何贷款明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkInterestRecompute(it));
    findings.push(...checkPrincipalRolling(it));
    findings.push(...checkNegative(it));

  }

  findings.push(...checkTotalRow(t.totals, t.items));
  findings.push(...checkDuplicates(t.items));
  findings.push(...checkBlanks(t.items));

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let interestTotal = 0;
  let principalPayTotal = 0;
  for (const it of t.items) {
    const i = normNumber(it.interest);
    if (i !== null) interestTotal += i;
    const p = normNumber(it.principalPay);
    if (p !== null) principalPayTotal += p;
  }

  const result = {
    status: 'success',
    service_type: 'BANK_LOAN_INTEREST_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      interest_total: round2(interestTotal),
      principal_repaid_total: round2(principalPayTotal),
      tolerance: TOL,
      rate_tolerance: RATE_TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: groups.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"期初本金 × 年利率 ÷ 12 × 计息月数 = 本期利息"与"期初本金 − 本期还本 = 期末本金"这类**表内勾稽**与档位提示，'
      + '**不判断该笔贷款该按什么口径计提利息、LPR 重定价是否本期生效**（以借款合同与会计师口径为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
