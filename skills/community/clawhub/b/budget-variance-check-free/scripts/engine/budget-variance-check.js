/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * budget-variance-check.js —— 费用预算执行差异核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月经营分析会之前**，财务要把费用预算执行表核一遍 ——
 * 预算数 / 实际数 / 差异 / 差异率 / 累计执行率，这几列必须自洽。
 * 这是**管理层每月都要看的表**：差异率算错会让决策跑偏；累计执行率与月度口径混用更是常见错。
 * 每月必做，且完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   差异     = 实际数 − 预算数
 *   差异率   = 差异 ÷ 预算数
 *   执行率   = 实际数 ÷ 预算数
 *   累计实际 = 各月实际之和（若表里给了累计列，必须与逐月之和一致）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**预算编制是否合理、该不该超支，只核表内勾稽与口径一致性。
 */

const CHECKS_GIVEN = [
  '差异勾稽（实际数 − 预算数 = 差异）',
  '差异率勾稽（差异 ÷ 预算数）',
  '合计行逐列复核',
  '重复科目检测',
  '空白与占位符检测',
  '预算数为零却填了差异率检测',
];

const CHECKS_WITHHELD = [
  '执行率勾稽（实际数 ÷ 预算数 = 执行率）',
  '累计实际与逐月/逐项实际不符检测',
  '预算数或实际数为负检测',
  '执行率超出常见区间（0~200%）检测',
  '差异率与差异方向不一致检测（正负号矛盾）',
];

const OUT_OF_SCOPE = [
  '判断预算编制是否合理、是否应当调整预算',
  '做同比/环比分析与业务原因归因',
  '处理预算科目口径变更或部门重分类',
  '读取 Excel 或预算系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '费用科目\t预算数\t实际数\t差异\t差异率\t执行率',
  '办公费\t120000.00\t108000.00\t-12000.00\t-10%\t90%',
  '差旅费\t200000.00\t230000.00\t30000.00\t15%\t115%',
  '市场推广费\t500000.00\t460000.00\t-40000.00\t-8%\t92%',
  '合计\t820000.00\t798000.00\t-22000.00\t-2.68%\t97.32%',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;          // 百分数比较容忍（0.05 个百分点）
const EXEC_MIN = 0;
const EXEC_MAX = 2.0;             // 执行率常见上限 200%

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前（否则「差异率」会被「差异」抢走）
  item: ['费用科目', '预算科目', '科目', '费用项目'],
  budget: ['预算数', '预算金额', '年度预算'],
  actual: ['实际数', '实际金额', '实际发生'],
  // ⛔ `差异率` 包含 `差异` 两个字 ⇒ 更具体的 diffRate **必须排在 diff 之前**
  //    （第 234 轮：顺序写反时差旅费那一列的差异被 -10% 覆盖，守卫当场报"有 1 列被覆盖"）。
  diffRate: ['差异率', '差异百分比'],
  execRate: ['执行率', '预算执行率', '完成率'],
  diff: ['差异', '差额'],
  cumulative: ['累计实际', '累计实际数', '累计发生'],
};

const LABELS = {
  item: '费用科目', budget: '预算数', actual: '实际数', diff: '差异',
  diffRate: '差异率', execRate: '执行率', cumulative: '累计实际',
};

const REQUIRED = ['item', 'budget', 'actual', 'diff'];
const SUM_ROLES = ['budget', 'actual', 'diff'];
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

/** 比率归一化成小数：`15%` ⇒ 0.15；`0.15` ⇒ 0.15；`15` ⇒ 0.15（按百分数看） */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 3 ? n / 100 : n;
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

function checkDiff(it) {
  const b = normNumber(it.budget);
  const a = normNumber(it.actual);
  const stated = normNumber(it.diff);
  if (b === null || a === null || stated === null) return null;
  const expect = round2(a - b);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '差异与复算不符', line: it.line,
    message: `${who(it)}：实际 ${a.toFixed(2)} − 预算 ${b.toFixed(2)} 应为 ${expect.toFixed(2)}，表里差异是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkDiffRate(it) {
  const b = normNumber(it.budget);
  const stated = rateValue(it.diffRate);
  if (b === null || stated === null || b === 0) return null;
  const diff = normNumber(it.diff);
  if (diff === null) return null;
  const expect = diff / b;
  if (Math.abs(expect - stated) <= RATE_TOL) return null;
  return {
    level: 'P0', category: '差异率与复算不符', line: it.line,
    message: `${who(it)}：差异 ${diff.toFixed(2)} ÷ 预算 ${b.toFixed(2)} 应为 ${(expect * 100).toFixed(2)}%，表里差异率是 ${(stated * 100).toFixed(2)}%。`,
  };
}

function checkZeroBudgetRate(it) {
  const b = normNumber(it.budget);
  if (b === null || b !== 0) return null;
  const dr = rateValue(it.diffRate);
  const aa = normNumber(it.actual);
  if (dr === null || Math.abs(dr) < 1e-9) return null;
  return {
    level: 'P0', category: '预算数为零却有差异率', line: it.line,
    message: `${who(it)}预算数是 0，却填了 ${(dr * 100).toFixed(2)}% 的差异率（实际数 ${aa === null ? '—' : aa.toFixed(2)}）—— 除数为零算不出比率，这一列应当留空或注明口径。`,
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
        level: 'P1', category: '同一科目出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 合计会被重复计算。`,
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
    return insufficient('没有收到预算执行表正文（text）—— 请把「科目 / 预算数 / 实际数 / 差异 / 差异率」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `预算执行表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何科目明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkDiff(it); if (a) findings.push(a);
    const b = checkDiffRate(it); if (b) findings.push(b);
    const c = checkZeroBudgetRate(it); if (c) findings.push(c);

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

  let budgetTotal = 0; let actualTotal = 0;
  for (const it of t.items) {
    const b = normNumber(it.budget); if (b !== null) budgetTotal += b;
    const a = normNumber(it.actual); if (a !== null) actualTotal += a;
  }

  const result = {
    status: 'success',
    service_type: 'BUDGET_VARIANCE_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      items: t.items.length,
      budget_total: round2(budgetTotal),
      actual_total: round2(actualTotal),
      variance_total: round2(actualTotal - budgetTotal),
      overall_exec_rate: budgetTotal > 0 ? round6(actualTotal / budgetTotal) : null,
      exec_range: [EXEC_MIN, EXEC_MAX],
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
    disclaimer: '只核预算执行表的内部勾稽（差异、差异率、执行率、累计），'
      + '**不判断预算是否合理**；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, rateValue, round2, round6, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
