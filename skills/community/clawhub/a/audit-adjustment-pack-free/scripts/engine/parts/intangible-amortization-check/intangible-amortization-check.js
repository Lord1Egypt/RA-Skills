#!/usr/bin/env node
/**
 * intangible-amortization-check.js —— 无形资产摊销与研发资本化核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**每个月的做账、每年的审计都要核一遍无形资产台账**。这张台账其实只有三条恒等式：
 *   ① 本期摊销额 =（原值 − 预计残值 − 减值准备）÷ 摊销月数 × 本期摊销月数
 *   ② 累计摊销   = 期初累计摊销 + 本期摊销额
 *   ③ 账面价值   = 原值 − 累计摊销 − 减值准备
 * 但真正出事的地方不在这三条上，而在"**看单项看不出来、必须横向比**"的那几处：
 *   摊销年限用错（10 年的专利写成 5 年）、该资本化的费用化（研发支出资本化与转无形资产对不上）、
 *   达到可使用状态却迟迟不开始摊销、已提足还在继续计提、减值后仍按原值摊销 ——
 *   这几件事都是**审计调整的高发区**，而算错的每一分钱都是要多交税或要解释的。
 *
 * 与已有能力的区别（硬要求，别写错）：
 *   · `long-term-amortization-check` 核的是**长期待摊费用**（装修费、租金、开办费）；
 *   · `mold-amortization-check` 核的是**模具与工装**的摊销；
 *   本能力核的是**无形资产**（软件、专利、商标、土地使用权、非专利技术、著作权）：
 *   原值/残值/减值/使用寿命月数与本期摊销，以及**研发支出资本化 → 转无形资产**这条线。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查税法与会计准则文库、不调用大模型；材料不足不给结论；
 *           不给会计、税务或审计意见（只把"按你填的口径算不出来的地方"指出来）。
 *
 * 说明：完整档的付费实现集中在一个开关块里，免费包由 tools/strip_free_engine.py 摘掉；
 *       开关字面量不要写进注释（守卫会把注释里的字面量也算成残留）。
 */
'use strict';

const CHECKS_GIVEN = [
  '本期摊销额勾稽复算（本期摊销额 =（原值 − 预计残值 − 减值准备）÷ 摊销月数 × 本期摊销月数）',
  '累计摊销勾稽复算（累计摊销 = 期初累计摊销 + 本期摊销额）',
  '账面价值勾稽复算（账面价值 = 原值 − 累计摊销 − 减值准备）',
  '合计行逐列复核（原值、累计摊销、减值准备、账面价值、本期摊销额等列的合计是否等于各行之和）',
  '重复资产编号检测',
  '关键字段空缺与占位符检测',
  '原值与摊销金额为负检测',
  '摊销月数非正检测',
];

const CHECKS_WITHHELD = [
  '摊销年限与类别惯例不符检测（按类别惯例区间判定，并把全部异常集中列出）',
  '已达到可使用状态却未开始摊销检测（含应补提金额）',
  '研发支出资本化金额与转无形资产金额不衔接检测',
  '已提足仍在计提检测（累计摊销超过可摊销总额的部分按多提金额计）',
  '减值后仍按原值摊销检测（应按减值后的账面价值重算本期摊销额）',
  '按金额排序的异常处理清单（每条带原文行号与建议动作）',
];

const OUT_OF_SCOPE = [
  '判断摊销年限是否符合税法或会计准则的强制规定（本工具只按你台账里的"类别惯例区间"提示异常，不下结论）',
  '判断研发支出是否满足资本化条件（那是研发费用归集与资本化条件判定的事）',
  '核对无形资产权属证书、专利年费、商标续展与评估报告等凭据',
  '处理使用寿命不确定的无形资产（不摊销、只做减值测试）与持有待售等特殊口径',
  '读取 .xlsx / ERP 导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '期间\t资产编号\t资产名称\t资产类别\t取得方式\t达到可使用状态日期\t原值\t预计残值\t摊销月数\t本期摊销月数\t期初累计摊销\t本期摊销额\t减值准备\t累计摊销\t账面价值\t研发支出资本化金额\t转无形资产金额',
  '2025-12\tWX-001\t财务软件\t软件\t外购\t2025-01-31\t600000.00\t0.00\t60\t1\t100000.00\t10000.00\t0.00\t110000.00\t490000.00\t\t',
  '2025-12\tZL-002\t发明专利权\t专利\t自研\t2025-03-31\t1200000.00\t0.00\t120\t1\t80000.00\t10000.00\t0.00\t90000.00\t1110000.00\t1500000.00\t1200000.00',
  '2025-12\tTD-003\t工业用地使用权\t土地使用权\t外购\t2023-01-01\t6000000.00\t0.00\t600\t1\t340000.00\t10000.00\t0.00\t350000.00\t5650000.00\t\t',
  '2025-12\tSB-004\t注册商标\t商标\t入股\t2025-03-31\t300000.00\t0.00\t120\t1\t20000.00\t2500.00\t0.00\t22500.00\t277500.00\t\t',
  '2025-12\tZZ-005\t软件著作权\t著作权\t自研\t2025-05-31\t480000.00\t24000.00\t60\t1\t45600.00\t7600.00\t0.00\t53200.00\t426800.00\t480000.00\t480000.00',
  '合计\t\t\t\t\t\t8580000.00\t24000.00\t\t\t585600.00\t40100.00\t0.00\t625700.00\t7954300.00\t1980000.00\t1680000.00',
].join('\n');

const TOL = 0.01;   // 金额都保留两位小数，容差 0.01

// ⚠️ 表头角色映射：**更具体的词必须排在更宽泛的前面**（本仓库踩过两次的坑，见 tools/header_map_check.py）。
//    这里的顺序是刻意的，改顺序前先想清楚：
//      · monthsNow「本期摊销月数」必须排在 months「摊销月数」前（否则前者被后者抢走，月数变成 1）；
//      · openAccum「期初累计摊销」必须排在 accum「累计摊销」前；
//      · amort「本期摊销额」必须排在 monthsNow / months 之后（"本期摊销"是它们的子串）；
//      · rdTransfer「转无形资产金额」必须排在 rdCapital「研发支出资本化金额」附近但两者互不为子串。
const ROLES = {
  period: ['期间', '月份', '所属期', '账期'],
  assetId: ['资产编号', '无形资产编号', '资产编码', '卡片编号'],
  name: ['资产名称', '无形资产名称', '名称'],
  category: ['资产类别', '无形资产类别', '类别', '品名'],
  acquire: ['取得方式', '取得途径', '来源方式'],
  readyDate: ['达到可使用状态日期', '达到预定用途日期', '可使用状态日期', '转无形资产日期'],
  rdCapital: ['研发支出资本化金额', '研发资本化金额', '资本化金额'],
  rdTransfer: ['转无形资产金额', '转入无形资产金额', '转无形资产'],
  cost: ['原值', '入账价值', '账面原值'],
  residual: ['预计残值', '残余价值', '残值'],
  monthsNow: ['本期摊销月数', '本月摊销月数', '本期摊销月份数'],
  months: ['摊销月数', '摊销年限月数', '使用寿命月数', '受益期限月数'],
  openAccum: ['期初累计摊销', '上期累计摊销', '年初累计摊销', '累计摊销期初'],
  amort: ['本期摊销额', '本期摊销', '月摊销额'],
  impairment: ['减值准备', '无形资产减值准备', '减值'],
  accum: ['累计摊销', '累计摊销额'],
  bookValue: ['账面价值', '账面净值', '账面余额'],
};

const LABELS = {
  period: '期间', assetId: '资产编号', name: '资产名称', category: '资产类别', acquire: '取得方式',
  readyDate: '达到可使用状态日期', cost: '原值', residual: '预计残值', months: '摊销月数',
  monthsNow: '本期摊销月数', openAccum: '期初累计摊销', amort: '本期摊销额',
  impairment: '减值准备', accum: '累计摊销', bookValue: '账面价值',
  rdCapital: '研发支出资本化金额', rdTransfer: '转无形资产金额',
};

// 缺了这些列 ⇒ 三条恒等式一条都算不出来 ⇒ 直接"材料不足、不给结论"
const REQUIRED = ['period', 'assetId', 'name', 'category', 'cost', 'residual', 'months',
  'monthsNow', 'openAccum', 'amort', 'impairment', 'accum', 'bookValue'];

// 金额列参与"合计行逐列复核"（只有表里真出现的列才核）
const SUM_ROLES = ['cost', 'residual', 'openAccum', 'amort', 'impairment', 'accum',
  'bookValue', 'rdCapital', 'rdTransfer'];

const PLACEHOLDER = /^(待填|待补|待定|待核|xxx|xxx\.xx|\?+|tbd|n\/?a|无|—+|-+)$/i;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值（不会替你填 0）。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s);
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

// 只给完整档用的日期工具（免费包用不到，会被 strip 工具当"没人引用的函数"删掉；
// 所以**不要**把它们放进 module.exports —— 见 tools/strip_free_engine.py 的导出清理规则）。
function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { error: 'empty' };
  const cols = splitRow(raw[0]).map((h) => ({ header: h, role: roleOf(h) }));
  const have = new Set(cols.map((c) => c.role).filter(Boolean));
  const missingRoles = REQUIRED.filter((r) => !have.has(r));
  if (missingRoles.length) {
    return { error: 'no_header', missingRoles: missingRoles.map((r) => LABELS[r]) };
  }
  const items = [];
  const totals = [];
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i], byRole: {} };
    cols.forEach((c, idx) => {
      if (c.role && row.byRole[c.role] === undefined) {
        row.byRole[c.role] = cells[idx] === undefined ? '' : cells[idx];
      }
    });
    const first = String(cells[0] || '').trim();
    if (/^(合计|总计|小计|total)/i.test(first)) {
      row.isTotal = true; totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals };
}

const num = (it, role) => normNumber(it.byRole[role]);
const who = (it) => `第 ${it.line} 行 资产「${String(it.byRole.assetId || '(未编号)').trim()}`
  + `${String(it.byRole.name || '').trim() ? '／' + String(it.byRole.name).trim() : ''}」`;

/** 可摊销金额 = 原值 − 预计残值 − 减值准备（三条恒等式的共同地基） */
function amortBase(it) {
  const cost = num(it, 'cost');
  const residual = num(it, 'residual');
  const imp = num(it, 'impairment');
  if (cost === null || residual === null || imp === null) return null;
  return round2(cost - residual - imp);
}

/** 月摊销额 =（原值 − 预计残值 − 减值准备）÷ 摊销月数 */
function monthlyAmount(it) {
  const base = amortBase(it);
  const months = num(it, 'months');
  if (base === null || months === null || months <= 0) return null;
  return round2(base / months);
}

const fmt = (n) => Number(n).toFixed(2);

/* ============================ 免费档：逐项复算 ============================ */

function checkAmortization(it) {
  const monthsNow = num(it, 'monthsNow');
  const stated = num(it, 'amort');
  const monthly = monthlyAmount(it);
  if (monthly === null || monthsNow === null || stated === null) return null;
  const expect = round2(monthly * monthsNow);
  if (Math.abs(expect - stated) <= TOL) return null;
  const base = amortBase(it);
  return {
    level: 'P0', category: '本期摊销额与复算不符', line: it.line,
    amount: round2(stated - expect),
    message: `${who(it)}的本期摊销额是 ${fmt(stated)}，按（原值 − 预计残值 − 减值准备）`
      + `${base === null ? '' : ' ' + fmt(base)} ÷ 摊销月数 ${num(it, 'months')} × 本期摊销月数 ${monthsNow}`
      + ` = ${fmt(expect)}，应为 ${fmt(expect)}。`,
    advice: '本期摊销额的底座是"可摊销金额 ÷ 摊销月数"；这一格错了，累计摊销与账面价值会跟着一起错。',
  };
}

function checkAccumulation(it) {
  const open = num(it, 'openAccum');
  const amort = num(it, 'amort');
  const stated = num(it, 'accum');
  if (open === null || amort === null || stated === null) return null;
  const expect = round2(open + amort);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '累计摊销与复算不符', line: it.line,
    amount: round2(stated - expect),
    message: `${who(it)}的累计摊销是 ${fmt(stated)}，按 期初累计摊销 ${fmt(open)} + 本期摊销额 `
      + `${fmt(amort)} 应为 ${fmt(expect)}。`,
    advice: '累计摊销是"期初 + 本期"滚出来的；它与本期摊销额必须能对上，否则以前期间就有断点。',
  };
}

function checkBookValue(it) {
  const cost = num(it, 'cost');
  const accum = num(it, 'accum');
  const imp = num(it, 'impairment');
  const stated = num(it, 'bookValue');
  if (cost === null || accum === null || imp === null || stated === null) return null;
  const expect = round2(cost - accum - imp);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '账面价值与复算不符', line: it.line,
    amount: round2(stated - expect),
    message: `${who(it)}的账面价值是 ${fmt(stated)}，按 原值 ${fmt(cost)} − 累计摊销 ${fmt(accum)}`
      + ` − 减值准备 ${fmt(imp)} 应为 ${fmt(expect)}。`,
    advice: '账面价值是资产负债表的取数口径；它与累计摊销、减值准备必须三处对得上。',
  };
}

function checkTotalRow(totals, items, role) {
  const out = [];
  for (const t of totals) {
    const stated = num(t, role);
    if (stated === null) continue;
    const sum = round2(items.reduce((s, it) => {
      const n = num(it, role);
      return s + (n === null ? 0 : n);
    }, 0));
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        level: 'P0', category: '合计行与明细之和不符', line: t.line,
        amount: round2(stated - sum),
        message: `第 ${t.line} 行 合计行的「${LABELS[role]}」是 ${fmt(stated)}，各明细行相加是 `
          + `${fmt(sum)}，相差 ${fmt(round2(stated - sum))}。`,
        advice: '要么明细行漏了资产，要么合计行没跟着更新 —— 合计行正是给管理层和审计看的那一行。',
      });
    }
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.assetId || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '重复资产编号', line: it.line,
        message: `${who(it)}的资产编号「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一张台账里一个资产只应有一行；重复行会让原值、摊销额与合计一起翻倍。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这一项就算不出来；补齐前本工具不会用 0 或默认值替你填（没有残值也要写 0.00）。',
        });
      }
    }
  }
  return out;
}

function checkNegatives(items) {
  const out = [];
  const roles = ['cost', 'residual', 'openAccum', 'amort', 'impairment', 'accum', 'bookValue'];
  for (const it of items) {
    for (const role of roles) {
      const v = num(it, role);
      if (v !== null && v < -TOL) {
        out.push({
          level: 'P0', category: '原值与摊销金额为负', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是 ${fmt(v)}（负数）。`,
          advice: '这几列按口径都不会为负：为负通常是录入了冲销行、或把"贷方余额"直接抄成了负数，请拆行说明。',
        });
      }
    }
  }
  return out;
}

function checkMonths(items) {
  const out = [];
  for (const it of items) {
    const months = num(it, 'months');
    const monthsNow = num(it, 'monthsNow');
    if (months !== null && months <= 0) {
      out.push({
        level: 'P0', category: '摊销月数非正', line: it.line,
        message: `${who(it)}的摊销月数是 ${months}（应为正数，单位是"月"）。`,
        advice: '摊销月数=0 会让月摊销额无穷大；想表达"使用寿命不确定"请单独说明，不要填 0。',
      });
    }
    if (monthsNow !== null && monthsNow < 0) {
      out.push({
        level: 'P0', category: '摊销月数非正', line: it.line,
        message: `${who(it)}的本期摊销月数是 ${monthsNow}（不能为负）。`,
        advice: '本期摊销月数填 0 表示本期不摊销（例如尚未达到可使用状态），但不能填负数。',
      });
    }
  }
  return out;
}

/* ============================ 入口 ============================ */

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的无形资产台账（要能认出「期间」「资产编号」「资产名称」「资产类别」「原值」'
      + '「预计残值」「摊销月数」「本期摊销月数」「期初累计摊销」「本期摊销额」「减值准备」'
      + '「累计摊销」「账面价值」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从无形资产台账导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一行无形资产明细行（合计行不算明细）']);




  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkAmortization(it); if (a) findings.push(a);
    const b = checkAccumulation(it); if (b) findings.push(b);
    const c = checkBookValue(it); if (c) findings.push(c);
  }
  const totalRoles = SUM_ROLES.filter((r) => t.cols.some((c) => c.role === r));
  for (const role of totalRoles) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);
  for (const f of checkNegatives(t.items)) findings.push(f);
  for (const f of checkMonths(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));

  const costTotal = sumOf('cost');
  const accumTotal = sumOf('accum');
  const impairmentTotal = sumOf('impairment');
  const bookValueTotal = sumOf('bookValue');
  const amortTotal = sumOf('amort');

  const scope = {
    rows: t.items.length,
    period: t.items.length ? String(t.items[0].byRole.period || '').trim() : '',
    checks: CHECKS_GIVEN,
    withheld: CHECKS_WITHHELD,
    checks_not_run: notRun,
    cost_total: costTotal,
    accum_total: accumTotal,
    book_value_total: bookValueTotal,
    amort_total: amortTotal,
    paid_in_total: amortTotal,
    outstanding_total: 0,
  };

  const result = {
    findings,
    action_list: [],
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      cost_total: costTotal,
      accum_total: accumTotal,
      impairment_total: impairmentTotal,
      book_value_total: bookValueTotal,
      amort_total: amortTotal,
      rd_capital_total: sumOf('rdCapital'),
      rd_transfer_total: sumOf('rdTransfer'),
      paid_in_total: amortTotal,
      outstanding_total: 0,
      basis: '本期摊销额 =（原值 − 预计残值 − 减值准备）÷ 摊销月数 × 本期摊销月数；'
        + '累计摊销 = 期初累计摊销 + 本期摊销额；账面价值 = 原值 − 累计摊销 − 减值准备；合计行逐列复核。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
    scope,
  };



  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得对**，'
      + '不代表摊销年限符合税法规定、也不代表研发支出资本化本身合规 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, REQUIRED, amortBase, monthlyAmount,
};
