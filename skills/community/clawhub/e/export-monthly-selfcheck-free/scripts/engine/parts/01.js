#!/usr/bin/env node
/**
 * export-rebate-check.js —— 出口退税（免抵退）核算核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**有出口业务的企业每月都要做免抵退申报**，而四道算式**串行依赖**：
 *   ① 不得免征和抵扣税额 = 出口离岸价(FOB) × 汇率 × (征税率 − 退税率)
 *   ② 免抵退税额        = FOB × 汇率 × 退税率
 *   ③ 应退税额          = min(期末留抵税额, 免抵退税额)
 *   ④ 免抵税额          = 免抵退税额 − 应退税额
 * ①②错一点，③④跟着错；而少退的是**真金白银**，多退的是**税务风险**。一个月几十票，人眼核不动。
 *
 * 与已有能力的区别：`import-duty-check` 核的是**进口**税费（关税/消费税/增值税）；
 * 本能力核的是**出口**退税（免抵退），两者是进出口的两条腿，算法完全不同。
 * `trade-doc-consistency` 只核单证一致性，不碰退税计算。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查出口退税率文库、不调用大模型；材料不足不给结论；不给税务意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '不得免征和抵扣税额勾稽（FOB × 汇率 × (征税率 − 退税率)）',
  '免抵退税额勾稽（FOB × 汇率 × 退税率）',
  '应退税额勾稽（期末留抵税额与免抵退税额取小）',
  '免抵税额勾稽（免抵退税额 − 应退税额）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复报关单号检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '退税率高于征税率检测（退税率不得高于征税率）',
  '退税率超出合理区间检测（不在 0~13%）',
  '出口离岸价或汇率为非正检测',
  '应退税额超过免抵退税额检测（超退）',
  '免抵税额为负检测',
];

const OUT_OF_SCOPE = [
  '判断出口货物该适用哪个退税率（那是海关商品码与退税文库的事）',
  '判断是否满足退税条件（单证、收汇、备案等）',
  '处理进料加工、来料加工、生产企业与外贸企业的口径差异（需按企业类型另行计算）',
  '处理跨月结转的期末留抵税额（请用当期申报表里的数字）',
  '给出税务意见；读取 .xlsx（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '报关单号\t出口离岸价\t汇率\t征税率\t退税率\t不得免征和抵扣税额\t免抵退税额\t期末留抵税额\t应退税额\t免抵税额',
  'A001\t1000000.00\t7.10\t13%\t10%\t213000.00\t710000.00\t500000.00\t500000.00\t210000.00',
  'B002\t500000.00\t7.10\t13%\t13%\t0.00\t461500.00\t200000.00\t200000.00\t261500.00',
  '合计\t1500000.00\t\t\t\t213000.00\t1171500.00\t700000.00\t700000.00\t471500.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  party: ['报关单号', '报关单', '商品', '货物', '品名', '单号'],
  fob: ['出口离岸价', '离岸价', 'FOB', '出口额', '出口金额'],
  fx: ['汇率', '记账汇率'],
  vatRate: ['征税率', '增值税率'],
  rebateRate: ['退税率'],
  notDeductible: ['不得免征和抵扣税额', '不得免征和抵扣', '不予免征和抵扣'],
  cap: ['免抵退税额', '免抵退'],
  credit: ['期末留抵税额', '留抵税额', '期末留抵'],
  refund: ['应退税额', '应退税'],
  exempt: ['免抵税额', '免抵'],
};

const LABELS = {
  party: '报关单号', fob: '出口离岸价', fx: '汇率', vatRate: '征税率', rebateRate: '退税率',
  notDeductible: '不得免征和抵扣税额', cap: '免抵退税额', credit: '期末留抵税额',
  refund: '应退税额', exempt: '免抵税额',
};

const SUM_ROLES = ['fob', 'notDeductible', 'cap', 'credit', 'refund', 'exempt'];
const REQUIRED = ['party', 'fob', 'fx', 'vatRate', 'rebateRate', 'notDeductible', 'cap', 'credit', 'refund', 'exempt'];

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
  // 「免抵退税额」必须排在「免抵税额」之前，否则会被后者抢走
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

function label(it) {
  return `报关单「${it.byRole.party || '(未命名)'}」`;
}

function baseOf(it) {
  const fob = normNumber(it.byRole.fob);
  const fx = normNumber(it.byRole.fx);
  if (fob === null || fx === null) return null;
  return fob * fx;
}

function checkNotDeductible(it) {
  const base = baseOf(it);
  const vat = normNumber(it.byRole.vatRate);
  const reb = normNumber(it.byRole.rebateRate);
  const stated = normNumber(it.byRole.notDeductible);
  if (base === null || vat === null || reb === null || stated === null) return null;
  const expect = round2(base * (vat - reb) / 100);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '不得免征和抵扣税额与复算不符', line: it.line,
    message: `${label(it)}的不得免征和抵扣税额是 ${stated.toFixed(2)}，`
      + `按 ${normNumber(it.byRole.fob).toFixed(2)} × ${normNumber(it.byRole.fx)} × (${vat}% − ${reb}%) 复算应为 ${expect.toFixed(2)}。`,
    advice: '这一项是"免抵退"的第一步，它错了后面三项会一起错。',
  };
}

function checkCap(it) {
  const base = baseOf(it);
  const reb = normNumber(it.byRole.rebateRate);
  const stated = normNumber(it.byRole.cap);
  if (base === null || reb === null || stated === null) return null;
  const expect = round2(base * reb / 100);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '免抵退税额与复算不符', line: it.line,
    message: `${label(it)}的免抵退税额是 ${stated.toFixed(2)}，`
      + `按 出口离岸价 × 汇率 × ${reb}% 复算应为 ${expect.toFixed(2)}。`,
    advice: '确认 FOB、汇率、退税率三者；退税率填错是最常见的原因。',
  };
}

function checkRefund(it) {
  const credit = normNumber(it.byRole.credit);
  const cap = normNumber(it.byRole.cap);
  const stated = normNumber(it.byRole.refund);
  if (credit === null || cap === null || stated === null) return null;
  const expect = round2(Math.min(credit, cap));
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应退税额与复算不符', line: it.line,
    message: `${label(it)}的应退税额是 ${stated.toFixed(2)}，`
      + `按「期末留抵 ${credit.toFixed(2)} 与 免抵退税额 ${cap.toFixed(2)} 取小」应为 ${expect.toFixed(2)}。`,
    advice: '应退税额取"留抵"与"免抵退税额"的较小者；取错会直接导致少退或多退。',
  };
}

function checkExempt(it) {
  const cap = normNumber(it.byRole.cap);
  const refund = normNumber(it.byRole.refund);
  const stated = normNumber(it.byRole.exempt);
  if (cap === null || refund === null || stated === null) return null;
  const expect = round2(cap - refund);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '免抵税额与复算不符', line: it.line,
    message: `${label(it)}的免抵税额是 ${stated.toFixed(2)}，按「免抵退税额 ${cap.toFixed(2)} − 应退税额 ${refund.toFixed(2)}」应为 ${expect.toFixed(2)}。`,
    advice: '免抵税额是抵减内销应纳税额的部分，它与应退税额之和必须等于免抵退税额。',
  };
}

function checkTotalRow(totals, items, role) {
  const out = [];
  for (const t of totals) {
    const stated = normNumber(t.byRole[role]);
    if (stated === null) continue;
    const sum = round2(items.reduce((s, it) => {
      const n = normNumber(it.byRole[role]);
      return s + (n === null ? 0 : n);
    }, 0));
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        level: 'P0', category: '合计行与明细之和不符', line: t.line,
        message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
        advice: '要么明细行漏了票，要么合计行没跟着更新。',
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
        level: 'P1', category: '同一报关单号出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一报关单多行商品是正常的；但若本表按报关单汇总，重复行会让退税额翻倍。',
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
          message: `${label(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这笔退税就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的出口退税（免抵退）计算表（要能认出「出口离岸价」「汇率」「征税率」「退税率」'
      + '「不得免征和抵扣税额」「免抵退税额」「期末留抵税额」「应退税额」「免抵税额」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从申报系统导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一票的明细行']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkNotDeductible(it); if (a) findings.push(a);
    const b = checkCap(it); if (b) findings.push(b);
    const c = checkRefund(it); if (c) findings.push(c);
    const d = checkExempt(it); if (d) findings.push(d);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = normNumber(it.byRole[role]);
    return s + (n === null ? 0 : n);
  }, 0));

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      fob_total: sumOf('fob'),
      cap_total: sumOf('cap'),
      refund_total: sumOf('refund'),
      exempt_total: sumOf('exempt'),
      basis: '逐票复算四步：不得免征和抵扣税额 = FOB × 汇率 ×(征税率 − 退税率)；'
        + '免抵退税额 = FOB × 汇率 × 退税率；应退税额 = min(期末留抵, 免抵退税额)；'
        + '免抵税额 = 免抵退税额 − 应退税额；合计行逐列复核。',
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
      + '不代表退税率适用正确、也不代表满足退税条件 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
