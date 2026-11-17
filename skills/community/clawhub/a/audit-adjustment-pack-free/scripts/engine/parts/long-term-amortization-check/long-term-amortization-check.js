/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * long-term-amortization-check.js —— 长期待摊费用摊销核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**月末结账前**，财务要把长期待摊费用（装修费、模具费、
 * 经营租入固定资产改良、开办费等）的摊销表核一遍 ——
 * 原值 / 摊销月数 / 已摊月数 / 本期摊销 / 累计摊销 / 账面余额，这几列必须自洽。
 * 摊销错了会影响当期费用与利润，**也是审计与所得税汇算的常查项**。每月必做，且完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   月摊销额   = 原值 ÷ 摊销月数
 *   本期摊销   = 月摊销额 × 本期摊销月数（通常 1）
 *   累计摊销   = 已摊月数 × 月摊销额
 *   账面余额   = 原值 − 累计摊销
 *   期末已摊月数 = 期初已摊月数 + 本期摊销月数
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**该不该资本化、摊销年限是否合理（那由准则与公司政策定），只核摊销表内部勾稽。
 */

const CHECKS_GIVEN = [
  '月摊销额勾稽（原值 ÷ 摊销月数 = 月摊销额）',
  '本期摊销勾稽（月摊销额 × 本期摊销月数）',
  '账面余额勾稽（原值 − 累计摊销 = 账面余额）',
  '累计摊销与已摊月数勾稽',
  '合计行逐列复核',
  '重复项目与空白检测',
];

const CHECKS_WITHHELD = [
  '已摊月数超过摊销月数（超期摊销）检测',
  '累计摊销超过原值检测',
  '本期摊销月数不是 1 检测（补提或漏提月）',
  '摊销月数为零或非整数检测',
  '账面余额为负或原值为负检测',
];

const OUT_OF_SCOPE = [
  '判断某项支出该不该计入长期待摊费用、摊销年限是否合理（那属于会计政策）',
  '处理摊销年限变更、提前报废或处置的账务处理',
  '核对长期待摊费用与在建工程/固定资产之间的重分类',
  '读取 ERP 或 Excel 导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '项目名称\t原值\t摊销月数\t期初已摊月数\t本期摊销月数\t月摊销额\t本期摊销\t累计摊销\t账面余额',
  '办公区装修费\t600000.00\t60\t20\t1\t10000.00\t10000.00\t210000.00\t390000.00',
  '模具费（A产品）\t180000.00\t36\t12\t1\t5000.00\t5000.00\t65000.00\t115000.00',
  '经营租入改良\t240000.00\t24\t24\t0\t10000.00\t0.00\t240000.00\t0.00',
  '合计\t1020000.00\t\t\t\t\t15000.00\t515000.00\t505000.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  item: ['项目名称', '费用项目', '资产名称', '项目'],
  cost: ['原值', '原始金额', '入账金额', '总额'],
  // ⛔ 顺序即优先级：`本期摊销月数` **也包含**「摊销月数」四个字，
  //    所以 periodMonths 必须排在 months **之前**，否则「本期摊销月数」会被 months 抢走
  //    （第 232 轮实测：结果 months 被覆盖成 1，月摊销额全报错 —— 这是同一类坑的第 6 次）。
  openMonths: ['期初已摊月数', '已摊月数（期初）', '已摊月数'],
  periodMonths: ['本期摊销月数', '本月摊销月数', '本期月数'],
  months: ['摊销月数', '摊销期限', '总月数'],
  monthly: ['月摊销额', '每月摊销额', '月摊金额'],
  periodAmt: ['本期摊销', '本期摊销额', '本月摊销'],
  accumulated: ['累计摊销', '累计摊销额'],
  balance: ['账面余额', '摊余价值', '未摊销余额', '净值'],
};

const LABELS = {
  item: '项目名称', cost: '原值', months: '摊销月数', openMonths: '期初已摊月数',
  periodMonths: '本期摊销月数', monthly: '月摊销额', periodAmt: '本期摊销',
  accumulated: '累计摊销', balance: '账面余额',
};

const REQUIRED = ['item', 'cost', 'months', 'monthly', 'periodAmt', 'accumulated', 'balance'];
const SUM_ROLES = ['cost', 'periodAmt', 'accumulated', 'balance'];
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
const round6 = (n) => Math.round(n * 1e6) / 1e6;

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

function checkMonthly(it) {
  const cost = normNumber(it.cost);
  const months = normNumber(it.months);
  const stated = normNumber(it.monthly);
  if (cost === null || months === null || stated === null || months <= 0) return null;
  const expect = round6(cost / months);
  if (Math.abs(expect - stated) <= 0.02) return null;
  return {
    level: 'P0', category: '月摊销额与复算不符', line: it.line,
    message: `${who(it)}：原值 ${cost.toFixed(2)} ÷ 摊销月数 ${months} 应为 ${expect.toFixed(2)}，表里月摊销额是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkPeriodAmount(it) {
  const monthly = normNumber(it.monthly);
  const pm = normNumber(it.periodMonths);
  const stated = normNumber(it.periodAmt);
  if (monthly === null || pm === null || stated === null) return null;
  const expect = round2(monthly * pm);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '本期摊销与复算不符', line: it.line,
    message: `${who(it)}：月摊销额 ${monthly.toFixed(2)} × 本期摊销月数 ${pm} 应为 ${expect.toFixed(2)}，表里本期摊销是 ${stated.toFixed(2)}。`,
  };
}

function checkBalance(it) {
  const cost = normNumber(it.cost);
  const acc = normNumber(it.accumulated);
  const stated = normNumber(it.balance);
  if (cost === null || acc === null || stated === null) return null;
  const expect = round2(cost - acc);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '账面余额与复算不符', line: it.line,
    message: `${who(it)}：原值 ${cost.toFixed(2)} − 累计摊销 ${acc.toFixed(2)} 应为 ${expect.toFixed(2)}，表里账面余额是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkAccumulated(it) {
  const monthly = normNumber(it.monthly);
  const openM = normNumber(it.openMonths);
  const pm = normNumber(it.periodMonths);
  const stated = normNumber(it.accumulated);
  if (monthly === null || openM === null || pm === null || stated === null) return null;
  const expect = round2(monthly * (openM + pm));
  if (Math.abs(expect - stated) <= 0.02) return null;
  return {
    level: 'P0', category: '累计摊销与已摊月数不符', line: it.line,
    message: `${who(it)}：按（期初已摊 ${openM} + 本期 ${pm}）个月 × 月摊销额 ${monthly.toFixed(2)} 应为 ${expect.toFixed(2)}，表里累计摊销是 ${stated.toFixed(2)}。`,
  };
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
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 摊销会被重复计算。`,
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
    return insufficient('没有收到摊销表正文（text）—— 请把「项目 / 原值 / 摊销月数 / 月摊销额 / 本期摊销 / 累计摊销 / 账面余额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `摊销表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何项目明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkMonthly(it); if (a) findings.push(a);
    const b = checkPeriodAmount(it); if (b) findings.push(b);
    const c = checkBalance(it); if (c) findings.push(c);
    const d = checkAccumulated(it); if (d) findings.push(d);

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

  let costTotal = 0; let balanceTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.cost); if (a !== null) costTotal += a;
    const b = normNumber(it.balance); if (b !== null) balanceTotal += b;
  }

  const result = {
    status: 'success',
    service_type: 'LONG_TERM_AMORTIZATION_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      items: t.items.length,
      cost_total: round2(costTotal),
      balance_total: round2(balanceTotal),
      amortized_total: round2(costTotal - balanceTotal),
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
    disclaimer: '只核摊销表内部勾稽（原值/月数/月摊销额/累计/余额），'
      + '**不判断该不该资本化或年限是否合理**；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, round6, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
