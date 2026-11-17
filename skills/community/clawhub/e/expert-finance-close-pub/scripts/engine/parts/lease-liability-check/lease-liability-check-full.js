'use strict';
/**
 * lease-liability-check.js —— 租赁负债与使用权资产核对（本包 / 订阅版共用源码）
 *
 * 谁在什么时候必须做这件事：新租赁准则（CAS 21 / IFRS 16）下，承租人要把每份租赁做成一张
 * **租赁负债摊销表** —— 一边按**期初租赁负债**计提利息、按**本期付款**冲减负债，
 * 一边按**使用权资产原值**计提折旧。**每期计提利息与折旧之前**都要把这张表核一遍：
 * 利息的计提基数是期初租赁负债，折旧的计提基数是使用权资产原值，
 * 基数错一期，后面每期的费用、负债余额、资产净值会**连锁错下去**（还能算错却看起来很整洁）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   期末租赁负债   = 期初租赁负债 + 本期利息 − 本期付款
 *   使用权资产净值 = 使用权资产原值 − 累计折旧
 *   本期利息       = 期初租赁负债 × 折现率（折现率按表里给的**期口径**直接乘，订阅版）
 *
 * 本包执行 6 项；订阅版追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**折现率、租赁期这些商业条款：一律以表里给的为准；
 *    只对"明显超出常见区间"做**提示**，并明确标注那是参考口径。
 */

const CHECKS_GIVEN = [
  '期末租赁负债复算（期初 + 本期利息 − 本期付款 = 期末）',
  '使用权资产净值复算（原值 − 累计折旧 = 净值）',
  '合计行逐列复核',
  '重复期次检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '利息与折现率勾稽检测（期初租赁负债 × 折现率 = 本期利息）',
  '付款超过期初与利息之和（负债变负）检测',
  '累计折旧超过使用权资产原值检测',
  '折现率偏离常见区间提示（参考口径）',
  '租赁期与摊销期次不匹配检测',
];

const OUT_OF_SCOPE = [
  '判断租赁是否应上表（短期租赁、低价值资产租赁的简化处理）与租赁期、折现率的商业条款是否恰当',
  '核对租赁付款额本身的完整性（是否漏了续租选择权、购买选择权、担保余值）',
  '处理租赁变更、提前终止、转租与售后回租',
  '读取财务系统/租赁管理软件导出文件（需要你先导出成文本贴进来）',
];

const TOL = 0.01;

const SAMPLE_TEXT = [
  '期间\t期次\t期初租赁负债\t折现率\t本期利息\t本期付款\t期末租赁负债\t使用权资产原值\t本期折旧\t累计折旧\t使用权资产净值\t租赁期数',
  '2026-01\t1\t100000.00\t0.5%\t500.00\t8000.00\t92500.00\t120000.00\t3200.00\t3200.00\t116800.00\t3',
  '2026-02\t2\t92500.00\t0.5%\t462.50\t8000.00\t84962.50\t120000.00\t3200.00\t6400.00\t113600.00\t3',
  '2026-03\t3\t84962.50\t0.5%\t424.81\t8000.00\t77387.31\t120000.00\t3200.00\t9600.00\t110400.00\t3',
  '合计\t\t\t\t1387.31\t24000.00\t\t\t9600.00\t\t\t',
].join('\n');

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名排在前（「租赁期数」不能被「期数」抢走，
  //    「期末租赁负债」不能被更宽泛的词抢走 —— 抢走的表现是"永远不给结论"）
  period: ['摊销期间', '会计期间', '所属期', '期间', '月份'],
  termMonths: ['租赁期数', '租赁期限', '总期数', '租赁期', '租期'],
  seq: ['期次', '第几期', '序号', '期数'],
  openLiab: ['期初租赁负债', '期初负债余额', '租赁负债期初', '期初余额'],
  interest: ['本期利息', '利息费用', '利息支出', '租赁利息', '利息'],
  payment: ['本期付款', '本期支付', '租赁付款额', '付款额', '租金付款', '付款'],
  closeLiab: ['期末租赁负债', '期末负债余额', '租赁负债期末', '期末余额'],
  rate: ['月折现率', '年折现率', '折现率', '增量借款利率', '租赁内含利率', '利率'],
  rouCost: ['使用权资产原值', '使用权资产入账价值', '使用权资产原价', '资产原值'],
  depreciation: ['本期折旧', '使用权资产折旧', '当期折旧', '折旧费用', '折旧额'],
  accumDep: ['累计折旧额', '累计折旧', '已提折旧'],
  rouNet: ['使用权资产净值', '使用权资产账面净值', '使用权资产账面价值', '资产净值', '账面净值'],
};

const LABELS = {
  period: '期间', termMonths: '租赁期数', seq: '期次', openLiab: '期初租赁负债',
  interest: '本期利息', payment: '本期付款', closeLiab: '期末租赁负债', rate: '折现率',
  rouCost: '使用权资产原值', depreciation: '本期折旧', accumDep: '累计折旧', rouNet: '使用权资产净值',
};

/* 没有这 8 列就核不了"负债滚动 + 资产净值"这两条主线 ⇒ 直接判定材料不足 */
const REQUIRED = ['period', 'openLiab', 'interest', 'payment', 'closeLiab', 'rouCost', 'accumDep', 'rouNet'];

/* 合计行只复核**流量列**：期初/期末余额、原值、累计折旧、净值都是时点/存量数，
   纵向相加没有会计含义，硬加起来只会制造假警报 */
const SUM_ROLES = ['interest', 'payment', 'depreciation'];

/* 金额列：出现负数就要看一眼（冲回、退款、尾差调整都得单独列示） */
const AMOUNT_ROLES = ['openLiab', 'interest', 'payment', 'closeLiab', 'rouCost', 'depreciation', 'accumDep', 'rouNet'];

/* 空白检查覆盖到"有这列才查"的扩展列 —— 缺整列不算空白，留空格才算 */
const BLANK_ROLES = REQUIRED.concat(['rate', 'seq', 'termMonths']);

const TOTAL_WORDS = /^(合计|总计|小计|共计|本期合计)$/;

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

/** 比率归一化成小数：`0.5%` ⇒ 0.005；`0.005` ⇒ 0.005；`0.5` ⇒ 0.005 */
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

const who = (it) => (it && it.period ? `${String(it.period).trim()} 期` : `第 ${it && it.line} 行`);

const hasKey = (it, role) => Object.prototype.hasOwnProperty.call(it, role);

/* ================================ 本包检查项 ================================ */

function checkCloseLiability(it) {
  const open = normNumber(it.openLiab);
  const interest = normNumber(it.interest);
  const payment = normNumber(it.payment);
  const close = normNumber(it.closeLiab);
  if (open === null || interest === null || payment === null || close === null) return null;
  const expect = round2(open + interest - payment);
  if (Math.abs(expect - close) <= TOL) return null;
  return {
    level: 'P0', category: '期末租赁负债复算不符', line: it.line,
    message: `${who(it)}：期初租赁负债 ${open.toFixed(2)} + 本期利息 ${interest.toFixed(2)} − 本期付款 ${payment.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里期末写的是 ${close.toFixed(2)}，相差 ${round2(close - expect).toFixed(2)} —— 这一期的余额会带着后面每期一起错。`,
  };
}

function checkRouNet(it) {
  const cost = normNumber(it.rouCost);
  const accum = normNumber(it.accumDep);
  const net = normNumber(it.rouNet);
  if (cost === null || accum === null || net === null) return null;
  const expect = round2(cost - accum);
  if (Math.abs(expect - net) <= TOL) return null;
  return {
    level: 'P0', category: '使用权资产净值复算不符', line: it.line,
    message: `${who(it)}：使用权资产原值 ${cost.toFixed(2)} − 累计折旧 ${accum.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里净值是 ${net.toFixed(2)}，相差 ${round2(net - expect).toFixed(2)}。`,
  };
}

function checkNegativeAmounts(it) {
  const out = [];
  for (const role of AMOUNT_ROLES) {
    const v = normNumber(it[role]);
    if (v === null || v >= -TOL) continue;
    out.push({
      level: 'P1', category: '金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 冲回、退款、尾差调整请单独列示，不要直接抵在摊销表里。`,
    });
  }
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各期相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const byPeriod = new Map();
  const bySeq = new Map();
  for (const it of items) {
    const key = String(it.period || '').trim();
    if (key) {
      if (byPeriod.has(key)) {
        out.push({
          level: 'P1', category: '期次重复', line: it.line,
          message: `${who(it)}在第 ${byPeriod.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 利息与折旧会被重复计提。`,
        });
      } else byPeriod.set(key, it.line);
    }
    const seq = String(it.seq === undefined ? '' : it.seq).trim();
    if (seq) {
      if (bySeq.has(seq)) {
        out.push({
          level: 'P1', category: '期次重复', line: it.line,
          message: `第 ${seq} 期在第 ${bySeq.get(seq)} 行已出现，第 ${it.line} 行再次出现 —— 同一期次只能有一行。`,
        });
      } else bySeq.set(seq, it.line);
    }
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of BLANK_ROLES) {
      if (!hasKey(it, role)) continue;
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

/* ============================ 订阅版检查项 ============================ */

function checkInterestRate(it) {
  const open = normNumber(it.openLiab);
  const rate = rateValue(it.rate);
  const stated = normNumber(it.interest);
  if (open === null || rate === null || stated === null) return null;
  const expect = round2(open * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '利息与折现率勾稽不符', line: it.line,
    message: `${who(it)}：期初租赁负债 ${open.toFixed(2)} × 折现率 ${(rate * 100).toFixed(4)}% 应为 ${expect.toFixed(2)}，`
      + `表里本期利息是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)} —— 利息的计提基数就是期初余额。`,
  };
}

function checkPaymentExceeds(it) {
  const open = normNumber(it.openLiab);
  const interest = normNumber(it.interest);
  const payment = normNumber(it.payment);
  if (open === null || interest === null || payment === null) return null;
  const limit = round2(open + interest);
  if (payment <= limit + TOL) return null;
  return {
    level: 'P0', category: '付款超过期初与利息之和', line: it.line,
    message: `${who(it)}：本期付款 ${payment.toFixed(2)} 超过「期初 ${open.toFixed(2)} + 本期利息 ${interest.toFixed(2)} = ${limit.toFixed(2)}」，`
      + `按此付款期末租赁负债会变成 ${round2(limit - payment).toFixed(2)}（负数）—— 租赁负债不该被付成负数。`,
  };
}

function checkAccumOverCost(it) {
  const cost = normNumber(it.rouCost);
  const accum = normNumber(it.accumDep);
  if (cost === null || accum === null) return null;
  if (accum <= cost + TOL) return null;
  return {
    level: 'P0', category: '累计折旧超过使用权资产原值', line: it.line,
    message: `${who(it)}：累计折旧 ${accum.toFixed(2)} 已超过使用权资产原值 ${cost.toFixed(2)}，超出 ${round2(accum - cost).toFixed(2)} —— 折旧提过头了。`,
  };
}

function checkRateRef(it) {
  const rate = rateValue(it.rate);
  if (rate === null) return null;
  /* 参考区间：**期利率** 0.2%~2.0%（约对应月折现率 0.2%~2%）。
     年折现率与月折现率相互混填，正是这条提示要抓的写法。 */
  const REF = [0.002, 0.02];
  if (rate >= REF[0] && rate <= REF[1]) return null;
  return {
    level: 'P2', category: '折现率偏离常见区间（参考）', line: it.line,
    message: `${who(it)}的折现率是 ${(rate * 100).toFixed(4)}%，超出本工具参考的期利率区间 `
      + `${(REF[0] * 100).toFixed(1)}%~${(REF[1] * 100).toFixed(1)}%`
      + '（**参考口径，不是规定**：请确认是年折现率还是月折现率，两者不能混填，最终以租赁合同与增量借款利率口径为准）。',
  };
}

function checkTermMatch(items) {
  const out = [];
  if (!items.length) return out;
  let hasTerm = false;
  const terms = new Set();
  for (const it of items) {
    if (!hasKey(it, 'termMonths')) continue;
    hasTerm = true;
    const v = normNumber(it.termMonths);
    if (v !== null) terms.add(v);
  }
  if (!hasTerm) return out;

  let hasSeq = false;
  const seqs = [];
  for (const it of items) {
    if (!hasKey(it, 'seq')) continue;
    hasSeq = true;
    const v = normNumber(it.seq);
    if (v !== null) seqs.push(v);
  }

  const declared = terms.size === 1 ? Array.from(terms)[0] : null;
  if (terms.size > 1) {
    out.push({
      level: 'P1', category: '租赁期与摊销期次不匹配', line: items[0].line,
      message: `表里「租赁期数」出现了 ${terms.size} 个不同的值（${Array.from(terms).join('、')}）—— 同一份摊销表的租赁期只能有一个口径。`,
    });
  }
  const count = hasSeq ? seqs.length : items.length;
  if (declared !== null && count !== declared) {
    out.push({
      level: 'P1', category: '租赁期与摊销期次不匹配', line: items[0].line,
      message: `表里列了 ${count} 期摊销，但「租赁期数」声明的是 ${declared} 期，相差 ${round2(count - declared)} 期`
        + ' —— 若这里只是整份摊销表的一部分，请把剩余期次补齐，或把租赁期数改成表内实际期数。',
    });
  } else if (declared !== null && hasSeq && seqs.length) {
    seqs.sort((a, b) => a - b);
    if (seqs[0] !== 1 || seqs[seqs.length - 1] !== seqs.length) {
      out.push({
        level: 'P1', category: '租赁期与摊销期次不匹配', line: items[0].line,
        message: `期次不是从 1 开始的连续编号（读到 ${seqs.join('、')}，而租赁期数是 ${declared} 期）—— 有期次被漏掉或重复编号。`,
      });
    }
  }
  return out;
}

/* ================================== 主入口 ================================== */

function run(payload) {
  const paid = Boolean(payload && (payload.full || payload.credit || payload.token));
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到摊销表正文（text）—— 请把「期间 / 期初租赁负债 / 本期利息 / 本期付款 / 期末租赁负债 / 使用权资产原值 / 累计折旧 / 使用权资产净值」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `摊销表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何期间明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkCloseLiability(it); if (a) findings.push(a);
    const b = checkRouNet(it); if (b) findings.push(b);
    for (const x of checkNegativeAmounts(it)) findings.push(x);
    if (paid) {
      const p1 = checkInterestRate(it); if (p1) findings.push(p1);
      const p2 = checkPaymentExceeds(it); if (p2) findings.push(p2);
      const p3 = checkAccumOverCost(it); if (p3) findings.push(p3);
      const p4 = checkRateRef(it); if (p4) findings.push(p4);
    }
  }
  if (paid) {
    for (const x of checkTermMatch(t.items)) findings.push(x);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const notRun = [];
  if (!paid) notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const totalsOf = (role) => {
    let s = 0;
    for (const it of t.items) {
      const v = normNumber(it[role]);
      if (v !== null) s += v;
    }
    return round2(s);
  };

  const result = {
    status: 'success',
    service_type: 'LEASE_LIABILITY_CHECK',
    scope: {
      checks: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      periods: t.items.length,
      interest_total: totalsOf('interest'),
      payment_total: totalsOf('payment'),
      depreciation_total: totalsOf('depreciation'),
      close_liability_total: totalsOf('closeLiab'),
      rou_net_total: totalsOf('rouNet'),
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: paid ? '完整档执行全部检查项。' : `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核摊销表内部的算术勾稽（期末 = 期初 + 利息 − 付款、净值 = 原值 − 累计折旧、利息 = 期初 × 折现率），'
      + '**不规定**折现率与租赁期这些商业条款（以租赁合同与增量借款利率口径为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, rateValue, round2,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
