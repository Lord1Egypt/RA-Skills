/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * travel-standard-check.js —— 差旅费标准与报销核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每家公司每个月报销差旅费时**，财务要把每个员工的
 * 差旅报销单对照**公司自己的内部标准**核一遍：住宿费、交通费、伙食补助都有**上限标准**，
 * 超标要么当场扣减、要么走审批。逐单核对最费人，而且**每一条都能用手算复现**：
 *
 *   报销合计     = 住宿费 + 交通费 + 伙食补助 + 其他
 *   超标金额     = 实际金额 − 标准上限        （正数 = 超标，负数 = 未超）
 *   伙食补助上限 = 出差天数 × 每日伙食补助标准
 *   出差天数     = 出差起止日期算出来的天数（含首尾）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * ⚠️ 本工具**不规定**标准：住宿/交通/伙食的上限一律**以表里给的为准**，
 *    只做"实际 vs 上限"的算术核对与内部勾稽，不替你判断标准定得合不合理。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 */

const CHECKS_GIVEN = [
  '报销合计勾稽（住宿费 + 交通费 + 伙食补助 + 其他 = 报销合计）',
  '超标金额勾稽（实际金额 − 标准上限 = 超标金额，正数=超标）',
  '合计行逐列复核',
  '同一人同一行程重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '住宿费超标准提示（含超出金额）',
  '交通费超标准提示（含超出金额）',
  '伙食补助按天数 × 标准勾稽',
  '出差天数与起止日期不一致检测',
  '超标但无审批标记提示',
];

const OUT_OF_SCOPE = [
  '判断住宿费/交通费/伙食补助的内部标准定得合不合理（标准以各公司制度与表里给出的为准）',
  '代替审批流程：本工具只提示"超标且未见审批标记"，不判断该不该批',
  '核对发票真伪、票据合规性与税务扣除口径',
  '读取 OA / 报销系统里的单据（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '姓名\t行程\t出差起止日期\t出差天数\t住宿费\t住宿费标准上限\t交通费\t交通费标准上限\t伙食补助\t伙食补助日标准\t其他费用\t报销合计\t超标金额\t审批',
  '张伟\t北京-上海\t2026-03-02 至 2026-03-06\t5\t2000.00\t2500.00\t1200.00\t1500.00\t500.00\t100.00\t300.00\t4000.00\t0.00\t已审批',
  '李娜\t广州-深圳\t2026-03-10 至 2026-03-13\t4\t1200.00\t1500.00\t600.00\t800.00\t400.00\t100.00\t0.00\t2200.00\t0.00\t已审批',
  '合计\t\t\t9\t3200.00\t4000.00\t1800.00\t2300.00\t900.00\t\t300.00\t6200.00\t0.00\t',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：**带「标准 / 上限」的别名必须排在「实际」别名前面**，
  //    否则「住宿费标准上限」会被更宽泛的「住宿费」抢走 ⇒ 实际金额列读到标准值（静默算错）。
  period: ['所属期', '期间', '月份'],
  person: ['姓名', '员工', '出差人', '报销人'],
  trip: ['行程', '出差事由', '出差地点'],
  dates: ['出差起止日期', '起止日期', '出差日期'],
  days: ['出差天数', '天数'],
  lodgingStd: ['住宿费标准上限', '住宿标准上限', '住宿费标准', '住宿标准'],
  lodgingActual: ['住宿费', '住宿'],
  transportStd: ['交通费标准上限', '交通标准上限', '交通费标准', '交通标准'],
  transportActual: ['交通费', '交通'],
  mealDaily: ['伙食补助日标准', '伙食日标准', '每日伙食补助', '日伙食补助标准'],
  mealActual: ['伙食补助', '伙食费', '餐补', '伙食'],
  otherStd: ['其他费用标准', '其他标准'],
  otherActual: ['其他费用', '其他'],
  total: ['报销合计', '报销总额', '合计金额', '报销金额'],
  over: ['超标金额', '超出金额', '超标'],
  approval: ['审批', '审批标记', '审批状态', '是否审批'],
};

const LABELS = {
  period: '所属期', person: '姓名', trip: '行程', dates: '出差起止日期', days: '出差天数',
  lodgingActual: '住宿费', lodgingStd: '住宿费标准上限', transportActual: '交通费',
  transportStd: '交通费标准上限', mealActual: '伙食补助', mealDaily: '伙食补助日标准',
  otherActual: '其他费用', otherStd: '其他费用标准', total: '报销合计', over: '超标金额',
  approval: '审批',
};

const REQUIRED = ['person', 'trip', 'total'];
/* 合计行逐列复核的金额列 */
const SUM_ROLES = ['lodgingActual', 'lodgingStd', 'transportActual', 'transportStd',
  'mealActual', 'otherActual', 'total', 'over'];
/* "金额为负"只看这些列 */
const AMOUNT_ROLES = ['lodgingActual', 'transportActual', 'mealActual', 'otherActual',
  'total', 'over'];
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

/** 日期归一化成 {y,m,d}；认 2026-03-02 / 2026/3/2 / 2026.3.2 / 2026年3月2日 */
const DAY_MS = 24 * 60 * 60 * 1000;
const dateMs = (o) => Date.UTC(o.y, o.m - 1, o.d);

/** 出差起止日期 → 天数（含首尾：3-02 到 3-06 = 5 天）；认不出来返回 null */
/** 审批标记：空 / 未审批 / 待审批 / 否 → 视为"没有审批标记" */
function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null, headers: [] };
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
    // 身份列（姓名 / 行程 / 所属期）被写成「合计」的行才是合计行
    if (!isTotal && ['person', 'trip', 'period'].some(
      (r) => row[r] !== undefined && TOTAL_WORDS.test(String(row[r]).trim()))) isTotal = true;
    if (isTotal) { totals.row = row; totals.line = i + 1; } else items.push(row);
  }
  return { items, totals, missingColumns, headers };
}

const who = (it) => {
  const p = it && it.person ? String(it.person).trim() : '';
  const tr = it && it.trip ? String(it.trip).trim() : '';
  const id = [p, tr].filter(Boolean).join(' / ');
  return id ? `${id}（第 ${it.line} 行）` : `第 ${it && it.line} 行`;
};
const money = (n) => Number(n).toFixed(2);

/* ================================ 免费档检查项 ================================ */

/** ① 报销合计 = 住宿费 + 交通费 + 伙食补助 + 其他 */
function checkTripTotal(it) {
  const lodging = normNumber(it.lodgingActual);
  const transport = normNumber(it.transportActual);
  const meal = normNumber(it.mealActual);
  const other = normNumber(it.otherActual);
  const stated = normNumber(it.total);
  if (stated === null) return null;
  if (lodging === null && transport === null && meal === null && other === null) return null;
  const parts = [
    ['住宿费', lodging], ['交通费', transport], ['伙食补助', meal], ['其他费用', other],
  ].filter((x) => x[1] !== null).map((x) => `${x[0]} ${money(x[1])}`).join(' + ');
  const sum = round2((lodging || 0) + (transport || 0) + (meal || 0) + (other || 0));
  if (Math.abs(sum - stated) <= TOL) return null;
  return {
    level: 'P0', category: '报销合计勾稽不符', line: it.line,
    message: `${who(it)}：${parts} = ${money(sum)}，但报销合计填的是 ${money(stated)}，相差 ${money(round2(stated - sum))}。`,
  };
}

/** ② 超标金额 = 实际金额 − 标准上限（正数=超标）
 *  ⚠️ 参与复算的只有「实际 + 上限」成对给出的列；**伙食补助的上限 = 出差天数 × 日标准**，
 *     不是表里某列直给，所以它由完整档的第 ⑨ 项单独勾稽，不混进这里。 */
function checkOverStandard(it) {
  const pairs = [
    ['住宿费', it.lodgingActual, it.lodgingStd],
    ['交通费', it.transportActual, it.transportStd],
    ['其他费用', it.otherActual, it.otherStd],
  ];
  const stated = normNumber(it.over);
  if (stated === null) return null;
  const rows = pairs.map(([label, a, s]) => {
    const actual = normNumber(a);
    const std = normNumber(s);
    if (actual === null || std === null) return null;
    return { label, actual, std, over: round2(actual - std) };
  }).filter(Boolean);
  if (!rows.length) return null;
  const expect = round2(rows.reduce((acc, x) => acc + Math.max(0, x.over), 0));
  if (Math.abs(expect - stated) <= TOL) return null;
  const detail = rows.map((x) => `${x.label} ${money(x.actual)}−${money(x.std)}=${money(x.over)}`).join('；');
  return {
    level: 'P0', category: '超标金额与（实际−上限）不符', line: it.line,
    message: `${who(it)}：逐项 ${detail}，超标部分相加应为 ${money(expect)}，但超标金额填的是 ${money(stated)}，相差 ${money(round2(stated - expect))}。`,
  };
}

/** ③ 合计行逐列复核：每个金额列的合计 = 各明细行相加 */
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
    message: `合计行的「${LABELS[role]}」是 ${money(stated)}，各明细行相加是 ${money(sum)}，相差 ${money(round2(stated - sum))}。`,
  });
  return out;
}

/** ④ 同一人同一行程重复行检测 */
function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const person = String(it.person || '').trim();
    const trip = String(it.trip || '').trim();
    if (!person || !trip) continue;
    const key = `${person}|${trip}|${String(it.dates || '').trim()}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一人同一行程出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 要么重复报销，要么行程需要拆开写。`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/** ⑤ 空白与占位符检测（姓名 / 行程 / 报销合计） */
function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）—— 这一列没法参与核对。`,
        });
      }
    }
  }
  return out;
}

/** ⑥ 金额为负检测 */
function checkNegativeAmounts(it) {
  const out = [];
  for (const role of AMOUNT_ROLES) {
    const v = normNumber(it[role]);
    if (v !== null && v < -TOL) {
      out.push({
        level: 'P0', category: '金额为负', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${money(v)}（负数）—— 冲回/退款请单独列示，别混进报销金额。`,
      });
    }
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** ⑦ 住宿费超标准提示（含超出金额） */
/** ⑧ 交通费超标准提示（含超出金额） */
/** ⑨ 伙食补助按 出差天数 × 每日标准 勾稽 */
/** ⑩ 出差天数与起止日期不一致检测 */
/** ⑪ 超标但无审批标记提示（伙食补助上限同样按 天数 × 日标准 算） */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到差旅报销表正文（text）—— 请把「姓名 / 行程 / 起止日期 / 天数 / 住宿费 / 交通费 / 伙食补助 / 报销合计」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `差旅报销表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${t.headers.join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或只有合计行），没有任何一张报销单明细');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkTripTotal(it); if (a) findings.push(a);
    const b = checkOverStandard(it); if (b) findings.push(b);
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

  let total = 0;
  let days = 0;
  for (const it of t.items) {
    const v = normNumber(it.total); if (v !== null) total += v;
    const w = normNumber(it.days); if (w !== null) days += w;
  }

  const result = {
    status: 'success',
    service_type: 'TRAVEL_STANDARD_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      periods: t.items.length,
      total_amount: round2(total),
      trip_days: round2(days),
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
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"报销合计 = 各项相加""超标金额 = 实际 − 上限""伙食补助 = 天数 × 标准"这类内部勾稽，'
      + '**不规定住宿/交通/伙食标准**（以各公司制度与表里给出的为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
