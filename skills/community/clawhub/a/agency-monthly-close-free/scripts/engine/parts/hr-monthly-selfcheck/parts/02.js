#!/usr/bin/env node
/**
 * iit-withholding-check.js —— 工资个税「累计预扣法」核算核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**每个有员工的公司每月发薪前都要算一遍个税**，而累计预扣法是**四步串行**：
 *   ① 累计应纳税所得额 = 累计收入 − 累计减除费用 − 累计专项扣除 − 累计专项附加扣除（负则按 0）
 *   ② 累计应纳税额 = ① × 预扣率 − 速算扣除数（**七级超额累进**，按累计数落档）
 *   ③ 本期应预扣 = ② − 已预扣税额
 * 落档落错、速算扣除数抄错、减除费用少算一个月 —— 每一项都会直接体现在每个人的工资条上，
 * 而且**错了要逐月更正**。几十上百人，人眼核不动；这些都是**纯算术**。
 *
 * 与已有能力的区别：`payroll-check` 核的是**发薪总额勾稽**（应发/社保/实发），
 * `overtime-pay-check` 核加班费倍数折算；**本能力核的是个税累计预扣的四步算式**，互不重叠。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查政策文库、不调用大模型；材料不足不给结论；不给税务意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '累计应纳税所得额勾稽（累计收入 − 减除费用 − 专项扣除 − 专项附加扣除，负则按 0）',
  '累计应纳税额勾稽（按七级累计预扣率表：应纳税所得额 × 预扣率 − 速算扣除数）',
  '本期应预扣勾稽（累计应纳税额 − 已预扣税额）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复人员检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '累计减除费用勾稽（应为 5000 元/月 × 月份数，月份数由入参给出）',
  '本期应预扣为负检测（累计应纳 < 已预扣，通常是人员中途入职或前期算错）',
  '累计收入小于累计扣除项检测（收入填错或扣除项串行）',
  '累计减除费用为负或为 0 检测',
];

const OUT_OF_SCOPE = [
  '判断专项附加扣除是否真实合规（那是员工申报与税务核验的事）',
  '处理全年一次性奖金单独计税、离职补偿、外籍人员等特殊口径',
  '处理补退税与跨年更正（请用当期的累计数）',
  '给出税务意见或测算税负优化；读取 .xlsx（需要你先导出成文本贴进来）',
];

// 七级累计预扣率表（累计预扣预缴应纳税所得额上限，预扣率%，速算扣除数）
const BRACKETS = [
  [36000, 3, 0],
  [144000, 10, 2520],
  [300000, 20, 16920],
  [420000, 25, 31920],
  [660000, 30, 52920],
  [960000, 35, 85920],
  [Infinity, 45, 181920],
];

const SAMPLE_TEXT = [
  '姓名\t累计收入\t累计减除费用\t累计专项扣除\t累计专项附加扣除\t累计应纳税所得额\t累计应纳税额\t已预扣税额\t本期应预扣',
  '张三\t120000.00\t30000.00\t12000.00\t9000.00\t69000.00\t4380.00\t2100.00\t2280.00',
  '李四\t90000.00\t30000.00\t9000.00\t6000.00\t45000.00\t1980.00\t900.00\t1080.00',
  '合计\t210000.00\t60000.00\t21000.00\t15000.00\t114000.00\t6360.00\t3000.00\t3360.00',
].join('\n');

const TOL = 0.01;
const MONTHLY_DEDUCTION = 5000;

const ROLES = {
  party: ['姓名', '员工', '人员', '名字'],
  income: ['累计收入', '收入额', '累计工资'],
  deductBase: ['累计减除费用', '减除费用', '基本减除'],
  deductSpecial: ['累计专项扣除', '专项扣除'],
  deductExtra: ['累计专项附加扣除', '专项附加扣除', '附加扣除'],
  taxable: ['累计应纳税所得额', '应纳税所得额'],
  tax: ['累计应纳税额', '应纳税额'],
  withheld: ['已预扣税额', '已预扣', '累计已预扣'],
  due: ['本期应预扣', '本期应预扣预缴', '本月应预扣'],
};

const LABELS = {
  party: '姓名', income: '累计收入', deductBase: '累计减除费用', deductSpecial: '累计专项扣除',
  deductExtra: '累计专项附加扣除', taxable: '累计应纳税所得额', tax: '累计应纳税额',
  withheld: '已预扣税额', due: '本期应预扣',
};

const REQUIRED = ['party', 'income', 'deductBase', 'deductSpecial', 'deductExtra', 'taxable', 'tax', 'withheld', 'due'];
const SUM_ROLES = ['income', 'deductBase', 'deductSpecial', 'deductExtra', 'taxable', 'tax', 'withheld', 'due'];

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
  // 「累计应纳税额」必须排在「累计应纳税所得额」的规则之后，避免被"应纳税所得额"抢走
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

/** 按累计数落档：返回 {rate, quick}。 */
function bracketOf(taxable) {
  for (const [cap, rate, quick] of BRACKETS) {
    if (taxable <= cap) return { rate, quick };
  }
  const last = BRACKETS[BRACKETS.length - 1];
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

function checkTaxable(it) {
  const stated = num(it, 'taxable');
  if (stated === null) return null;
  const parts = ['income', 'deductBase', 'deductSpecial', 'deductExtra'].map((r) => num(it, r));
  if (parts.some((p) => p === null)) return null;
  const raw = round2(parts[0] - parts[1] - parts[2] - parts[3]);
  const expect = Math.max(0, raw);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '累计应纳税所得额与复算不符', line: it.line,
    message: `${who(it)}的累计应纳税所得额是 ${stated.toFixed(2)}，`
      + `按 累计收入 ${parts[0].toFixed(2)} − 减除费用 ${parts[1].toFixed(2)} − 专项扣除 ${parts[2].toFixed(2)} `
      + `− 专项附加扣除 ${parts[3].toFixed(2)} = ${raw.toFixed(2)}`
      + `${raw < 0 ? '（负值按 0 计）' : ''}，应为 ${expect.toFixed(2)}。`,
    advice: '这一格是后面两步的基数；它错了，税额与本期应预扣会一起错。',
  };
}

function checkTax(it) {
  const taxable = num(it, 'taxable');
  const stated = num(it, 'tax');
  if (taxable === null || stated === null) return null;
  const base = Math.max(0, taxable);
  const { rate, quick } = bracketOf(base);
  const expect = round2(base * rate / 100 - quick);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '累计应纳税额与复算不符', line: it.line,
    message: `${who(it)}的累计应纳税额是 ${stated.toFixed(2)}，`
      + `按累计应纳税所得额 ${base.toFixed(2)} 落档 ${rate}%（速算扣除数 ${quick}）复算应为 ${expect.toFixed(2)}。`,
    advice: '累计预扣法是"按累计数落档"，不是按月单独算；落档或速算扣除数抄错是最常见的原因。',
  };
}

function checkDue(it) {
  const tax = num(it, 'tax');
  const withheld = num(it, 'withheld');
  const stated = num(it, 'due');
  if (tax === null || withheld === null || stated === null) return null;
  const expect = round2(tax - withheld);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '本期应预扣与复算不符', line: it.line,
    message: `${who(it)}的本期应预扣是 ${stated.toFixed(2)}，`
      + `按 累计应纳税额 ${tax.toFixed(2)} − 已预扣税额 ${withheld.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '本期应预扣 = 累计应纳税额 − 已预扣税额；差额通常是前期已预扣数抄错。',
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
        advice: '要么明细行漏了人，要么合计行没跟着更新。',
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
        advice: '同一人多笔是正常的；但若本表按人汇总，重复行会让累计数与税额一起翻倍。',
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
          advice: '缺这一格这笔个税就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的个税累计预扣计算表（要能认出「累计收入」「累计减除费用」「累计专项扣除」'
      + '「累计专项附加扣除」「累计应纳税所得额」「累计应纳税额」「已预扣税额」「本期应预扣」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从算薪系统导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一人的明细行']);

  const months = normNumber(payload && payload.months);
  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkTaxable(it); if (a) findings.push(a);
    const b = checkTax(it); if (b) findings.push(b);
    const c = checkDue(it); if (c) findings.push(c);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

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
      income_total: sumOf('income'),
      taxable_total: sumOf('taxable'),
      tax_total: sumOf('tax'),
      due_total: sumOf('due'),
      basis: '累计应纳税所得额 = 累计收入 − 累计减除费用 − 累计专项扣除 − 累计专项附加扣除（负则按 0）；'
        + '累计应纳税额 = 应纳税所得额 × 预扣率 − 速算扣除数（七级累计预扣率表）；'
        + '本期应预扣 = 累计应纳税额 − 已预扣税额；合计行逐列复核。',
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
      + '不代表专项附加扣除真实合规、也不代表适用特殊口径正确 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, bracketOf, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, BRACKETS,
};
