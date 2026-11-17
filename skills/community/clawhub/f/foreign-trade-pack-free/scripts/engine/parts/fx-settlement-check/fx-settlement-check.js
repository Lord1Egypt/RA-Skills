#!/usr/bin/env node
/**
 * fx-settlement-check.js —— 外币结算与汇兑损益核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**有外币业务的企业，每笔收付都要按两个汇率过一遍**：
 *   ① 记账本位币 = 外币金额 × 记账汇率（确认收入/应收时用）
 *   ② 结算本位币 = 外币金额 × 结算汇率（实际收款日汇率）
 *   ③ 汇兑损益   = 结算本位币 − 记账本位币
 *   ④ 已收本位币应等于结算本位币（差一分都要查）
 * 汇率用错、日期串了、损益方向反了 —— 每一项都会进损益表，而且**月结时几十上百笔**，人眼核不动。
 *
 * 与已有能力的区别：`import-duty-check` / `export-rebate-check` 核的是**进出口税费与退税**；
 * `trade-doc-consistency` 核的是**单证之间的一致性**；本能力核的是**外币折算与汇兑损益**，互不重叠。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查当日汇率、不调用大模型；材料不足不给结论；不给会计/税务意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '记账本位币勾稽（外币金额 × 记账汇率）',
  '结算本位币勾稽（外币金额 × 结算汇率）',
  '汇兑损益勾稽（结算本位币 − 记账本位币）',
  '已收本位币与结算本位币一致性勾稽',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复单据号检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '汇率为非正检测',
  '外币金额非正检测',
  '汇兑损益与「已收本位币 − 记账本位币」口径不符检测',
  '汇兑损益绝对额超过记账本位币 10% 的异常波动检测',
  '已收本位币为负检测',
];

const OUT_OF_SCOPE = [
  '判断记账汇率是否符合准则要求（那是会计政策的事）',
  '处理外币货币性项目期末调汇、以及资本化处理',
  '处理远期结售汇、期权等套期会计',
  '判断汇兑损益的税前扣除口径；给出税务意见',
  '读取 .xlsx 或银行水单文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '单据号\t外币金额\t记账汇率\t记账本位币\t结算汇率\t结算本位币\t汇兑损益\t已收本位币',
  'INV-001\t10000.00\t7.1000\t71000.00\t7.1500\t71500.00\t500.00\t71500.00',
  'INV-002\t5000.00\t7.1000\t35500.00\t7.0500\t35250.00\t-250.00\t35250.00',
  '合计\t15000.00\t\t106500.00\t\t106750.00\t250.00\t106750.00',
].join('\n');

const TOL = 0.01;
const FX_MOVE_CAP = 0.10;      // 汇兑损益绝对额占记账本位币的比例上限（异常波动）

const ROLES = {
  party: ['单据号', '单号', '发票号', '凭证号'],
  amount: ['外币金额', '原币金额', '外币'],
  bookRate: ['记账汇率', '记账日汇率', '月初汇率'],
  bookBase: ['记账本位币', '记账金额', '本位币金额'],
  settleRate: ['结算汇率', '收款汇率', '实际汇率'],
  settleBase: ['结算本位币', '结算金额'],
  fxGain: ['汇兑损益', '汇兑差额', '汇兑收益'],
  received: ['已收本位币', '实收本位币', '已收金额'],
};

const LABELS = {
  party: '单据号', amount: '外币金额', bookRate: '记账汇率', bookBase: '记账本位币',
  settleRate: '结算汇率', settleBase: '结算本位币', fxGain: '汇兑损益', received: '已收本位币',
};

const REQUIRED = ['party', 'amount', 'bookRate', 'bookBase', 'settleRate', 'settleBase', 'fxGain', 'received'];
const SUM_ROLES = ['amount', 'bookBase', 'settleBase', 'fxGain', 'received'];

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
  // ⚠️ 更具体的关键词必须排在更宽泛的前面（本仓库踩过三次的坑，见 tools/header_map_check.py）：
  //    「记账汇率」必须排在「记账本位币」之前，否则「记账」类宽泛词会互相抢；
  //    「结算汇率」同理要排在「结算本位币」之前。
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

const num = (it, role) => normNumber(it.byRole[role]);
const who = (it) => `单据「${it.byRole.party || '(未命名)'}」`;

function checkBookBase(it) {
  const amount = num(it, 'amount');
  const rate = num(it, 'bookRate');
  const stated = num(it, 'bookBase');
  if (amount === null || rate === null || stated === null) return null;
  const expect = round2(amount * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '记账本位币与复算不符', line: it.line,
    message: `${who(it)}的记账本位币是 ${stated.toFixed(2)}，按 外币金额 ${amount.toFixed(2)} × 记账汇率 ${rate} 应为 ${expect.toFixed(2)}。`,
    advice: '记账汇率是确认收入/应收时的汇率；用成结算日汇率会让汇兑损益凭空消失。',
  };
}

function checkSettleBase(it) {
  const amount = num(it, 'amount');
  const rate = num(it, 'settleRate');
  const stated = num(it, 'settleBase');
  if (amount === null || rate === null || stated === null) return null;
  const expect = round2(amount * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '结算本位币与复算不符', line: it.line,
    message: `${who(it)}的结算本位币是 ${stated.toFixed(2)}，按 外币金额 ${amount.toFixed(2)} × 结算汇率 ${rate} 应为 ${expect.toFixed(2)}。`,
    advice: '结算汇率应取**实际收款日**的汇率；两个汇率取同日就等于没有汇兑损益。',
  };
}

function checkFxGain(it) {
  const book = num(it, 'bookBase');
  const settle = num(it, 'settleBase');
  const stated = num(it, 'fxGain');
  if (book === null || settle === null || stated === null) return null;
  const expect = round2(settle - book);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '汇兑损益与复算不符', line: it.line,
    message: `${who(it)}的汇兑损益是 ${stated.toFixed(2)}，`
      + `按 结算本位币 ${settle.toFixed(2)} − 记账本位币 ${book.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '方向最容易写反：**结算汇率高于记账汇率 ⇒ 收益（正）**；表里符号错了会让损益表反向。',
  };
}

function checkReceived(it) {
  const settle = num(it, 'settleBase');
  const stated = num(it, 'received');
  if (settle === null || stated === null) return null;
  if (Math.abs(settle - stated) <= TOL) return null;
  return {
    level: 'P0', category: '已收本位币与结算本位币不符', line: it.line,
    message: `${who(it)}的已收本位币是 ${stated.toFixed(2)}，与结算本位币 ${settle.toFixed(2)} 相差 ${round2(stated - settle).toFixed(2)}。`,
    advice: '已收 = 结算（同一笔款）；不一致通常是银行扣了电报费/手续费，或汇率取错 —— 请查明后单列。',
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
        advice: '要么明细行漏了单据，要么合计行没跟着更新。',
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
        level: 'P1', category: '同一单据号出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一单据分次收款是正常的；但若本表按单据汇总，重复行会让金额与损益一起翻倍。',
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
          advice: '缺这一格这笔折算就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的外币结算核对表（要能认出「外币金额」「记账汇率」「记账本位币」'
      + '「结算汇率」「结算本位币」「汇兑损益」「已收本位币」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从外币台账导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一笔的明细行']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkBookBase(it); if (a) findings.push(a);
    const b = checkSettleBase(it); if (b) findings.push(b);
    const c = checkFxGain(it); if (c) findings.push(c);
    const d = checkReceived(it); if (d) findings.push(d);
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
      notes: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      amount_total: sumOf('amount'),
      book_base_total: sumOf('bookBase'),
      settle_base_total: sumOf('settleBase'),
      fx_gain_total: sumOf('fxGain'),
      received_total: sumOf('received'),
      basis: '记账本位币 = 外币金额 × 记账汇率；结算本位币 = 外币金额 × 结算汇率；'
        + '汇兑损益 = 结算本位币 − 记账本位币；已收本位币应与结算本位币一致；合计行逐列复核。',
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
      + '不代表记账汇率符合准则、也不代表套期等特殊处理正确 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
