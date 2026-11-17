#!/usr/bin/env node
/**
 * bonus-pool-check.js —— 年终奖池分配与个税核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**每年年底都要做一次**，而且它有两段完全不同的算术，谁都得核：
 *   ① 分配：应发奖金 = 奖金池 × 个人绩效系数 ÷ 系数合计（**比例分摊，容易出现"分不干净"**）
 *   ② 计税（全年一次性奖金）：先把奖金 ÷ 12 找月度税率档，再 个税 = 奖金 × 税率 − 速算扣除数
 * 系数填错、池子总数没对上、税率档找错（尤其**卡在档位边界**上）—— 都会让人少拿或多扣，
 * 而且年终奖一年只有一次，错了要跨年更正。几十上百人，人眼核不动。
 *
 * 与已有能力的区别：`payroll-check` 核**月度发薪**、`iit-withholding-check` 核**累计预扣**、
 * `commission-check` 核**销售提成**；本能力核的是**年终奖池的比例分摊 + 全年一次性奖金计税**（月度税率表口径）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查政策文库、不调用大模型；材料不足不给结论；不给税务意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '应发奖金勾稽（奖金池 × 绩效系数 ÷ 系数合计）',
  '实发奖金勾稽（应发奖金 − 个税）',
  '全年一次性奖金个税勾稽（奖金 ÷ 12 落档，个税 = 奖金 × 税率 − 速算扣除数）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复人员检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '计税方式取值合法性检测（只允许「全年一次性」或「并入综合所得」）',
  '个税为负检测',
  '绩效系数非正检测',
  '个税超过应发奖金 45% 的异常检测',
];

const OUT_OF_SCOPE = [
  '判断奖金池总额与考核结果是否合理（那是薪酬委员会的事）',
  '计算「并入综合所得」情形下的个税（那要结合全年累计收入与已预扣，需用工资表另行计算）',
  '处理离职补偿、股权激励等特殊所得的计税',
  '给出税务意见或做税负优化测算；读取 .xlsx（需要你先导出成文本贴进来）',
];

// 全年一次性奖金适用的**按月换算**税率表（奖金÷12 落档）
const MONTHLY_BRACKETS = [
  [3000, 3, 0],
  [12000, 10, 210],
  [25000, 20, 1410],
  [35000, 25, 2660],
  [55000, 30, 4410],
  [80000, 35, 7160],
  [Infinity, 45, 15160],
];

const SAMPLE_TEXT = [
  '姓名\t绩效系数\t应发奖金\t计税方式\t个税\t实发奖金',
  '张三\t1.5\t60000.00\t全年一次性\t5790.00\t54210.00',
  '李四\t1.0\t40000.00\t全年一次性\t3790.00\t36210.00',
  '合计\t2.5\t100000.00\t\t9580.00\t90420.00',
].join('\n');

const TOL = 0.01;
const TAX_RATE_CAP = 0.45;

const ROLES = {
  party: ['姓名', '员工', '人员', '名字'],
  coef: ['绩效系数', '考核系数', '系数'],
  // ⚠️ 别名里**不能放裸「奖金」**：它会把「实发奖金」抢走（本仓库第四次踩这类坑，
  //    这次是发版前的 header_map_check 抓到的，没有流到线上）。
  gross: ['应发奖金', '应发金额', '奖金金额'],
  method: ['计税方式', '计税方法', '计税口径'],
  tax: ['个税', '个人所得税', '扣税'],
  net: ['实发奖金', '实发金额', '税后奖金'],
};

const LABELS = {
  party: '姓名', coef: '绩效系数', gross: '应发奖金', method: '计税方式', tax: '个税', net: '实发奖金',
};

const REQUIRED = ['party', 'coef', 'gross', 'method', 'tax', 'net'];
const SUM_ROLES = ['coef', 'gross', 'tax', 'net'];
const ANNUAL_METHOD = /全年一次性|单独计税|全年一次/;
const MERGED_METHOD = /并入|综合所得/;

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
  // ⚠️ 更具体的关键词必须排在更宽泛的前面（本仓库踩过三次的坑）：
  //    「应发奖金」不能被「实发奖金」的别名先抢走，反之亦然 —— 两者都写全，顺序按具体度排。
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

/** 按月换算的税率档：入参是"奖金 ÷ 12"。 */
function monthBracket(monthly) {
  for (const [cap, rate, quick] of MONTHLY_BRACKETS) {
    if (monthly <= cap) return { rate, quick };
  }
  const last = MONTHLY_BRACKETS[MONTHLY_BRACKETS.length - 1];
  return { rate: last[1], quick: last[2] };
}

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
const who = (it) => `「${it.byRole.party || '(未命名)'}」`;

/** 奖金池与系数合计：优先取"合计行"，没有合计行就用各行之和。 */
function poolOf(items, totals) {
  const sum = (role) => round2(items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));
  const t = totals[0];
  const pool = t && num(t, 'gross') !== null ? num(t, 'gross') : sum('gross');
  const coefSum = t && num(t, 'coef') !== null ? num(t, 'coef') : sum('coef');
  return { pool, coefSum };
}

function checkGross(it, pool, coefSum) {
  const coef = num(it, 'coef');
  const stated = num(it, 'gross');
  if (coef === null || stated === null || !Number.isFinite(pool) || !Number.isFinite(coefSum) || coefSum === 0) return null;
  const expect = round2(pool * coef / coefSum);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应发奖金与分摊复算不符', line: it.line,
    message: `${who(it)}的应发奖金是 ${stated.toFixed(2)}，`
      + `按 奖金池 ${pool.toFixed(2)} × 系数 ${coef} ÷ 系数合计 ${coefSum} 应为 ${expect.toFixed(2)}。`,
    advice: '比例分摊容易出现"分不干净"（合计与池子差几毛）；差额要有明确处理方式（如计入某一人或留池）。',
  };
}

function checkNet(it) {
  const gross = num(it, 'gross');
  const tax = num(it, 'tax');
  const stated = num(it, 'net');
  if (gross === null || tax === null || stated === null) return null;
  const expect = round2(gross - tax);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '实发奖金与复算不符', line: it.line,
    message: `${who(it)}的实发奖金是 ${stated.toFixed(2)}，按 应发奖金 ${gross.toFixed(2)} − 个税 ${tax.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '实发 = 应发 − 个税；若还有其他扣款（如借款、罚款），应在本表显式列示。',
  };
}

function checkTax(it) {
  const gross = num(it, 'gross');
  const stated = num(it, 'tax');
  const method = String(it.byRole.method || '').trim();
  if (gross === null || stated === null) return null;
  if (!ANNUAL_METHOD.test(method)) return null;          // 并入综合所得的税额需另行计算，本表不判
  const monthly = gross / 12;
  const { rate, quick } = monthBracket(monthly);
  const expect = round2(gross * rate / 100 - quick);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '全年一次性奖金个税与复算不符', line: it.line,
    message: `${who(it)}的个税是 ${stated.toFixed(2)}，`
      + `按 奖金 ${gross.toFixed(2)} ÷ 12 = ${round2(monthly).toFixed(2)} 落档 ${rate}%（速算扣除数 ${quick}）`
      + `复算应为 ${expect.toFixed(2)}。`,
    advice: '全年一次性奖金是"**先除以 12 找档、再用全额算税**"；档位边界（3000/12000/25000…）最容易错一档。',
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
        message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
        advice: '要么明细行漏了人，要么合计行没跟着更新（合计行的应发奖金通常就是"奖金池"）。',
      });
    }
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.party || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一人员出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一人多笔奖金是正常的；但若本表按人汇总，重复行会让池子分摊与个税一起翻倍。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这笔奖金就算不出来；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
  }
  return out;
}

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的年终奖分配表（要能认出「绩效系数」「应发奖金」「计税方式」「个税」「实发奖金」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从算薪系统导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一人的明细行']);

  const { pool, coefSum } = poolOf(t.items, t.totals);
  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkGross(it, pool, coefSum); if (a) findings.push(a);
    const b = checkNet(it); if (b) findings.push(b);
    const c = checkTax(it); if (c) findings.push(c);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const mergedRows = t.items.filter((it) => MERGED_METHOD.test(String(it.byRole.method || '')));
  if (mergedRows.length) notRun.push('并入综合所得情形的个税（需结合全年累计收入，另行计算）');

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));

  const result = {
    findings,
    summary: {
      people: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      pool: Number.isFinite(pool) ? pool : null,
      coef_sum: Number.isFinite(coefSum) ? coefSum : null,
      gross_total: sumOf('gross'),
      tax_total: sumOf('tax'),
      net_total: sumOf('net'),
      allocation_gap: Number.isFinite(pool) ? round2(pool - sumOf('gross')) : null,
      basis: '应发奖金 = 奖金池 × 绩效系数 ÷ 系数合计（池子与系数合计取合计行，无合计行则取各行之和）；'
        + '实发奖金 = 应发奖金 − 个税；全年一次性奖金个税 = 奖金 × 税率 − 速算扣除数（**先按 奖金 ÷ 12 落档**）；合计行逐列复核。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的口径算得对**，'
      + '不代表考核结果与池子总额合理、也不代表并入综合所得情形下的税额正确 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, monthBracket, poolOf, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, MONTHLY_BRACKETS,
};
