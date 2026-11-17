/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * cargo-insurance-claim-check.js —— 货运险投保与货损理赔核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**物流 / 外贸企业每月对账，以及每一次货损索赔时**。
 * 货运险台账是几条纯算术关系串起来的：
 *   ① 保费 = 投保金额 × 费率
 *   ② 应赔金额 = 定损金额 − 免赔额（负数按 0）
 *   ③ 理赔差额 = 应赔金额 − 实收理赔款
 *   ④ 投保比例 = 投保金额 ÷ 货值
 * 这几条关系任意一条填错，当期就少收赔款或多付保费；而**最常见的三类漏钱**是
 * **少赔**（实收低于应赔）、**漏保**（货值高于投保金额）、**重复投保**（同一票货投了两份保险）。
 *
 * 与已有能力的区别：`vehicle-insurance-amortization-check` 核的是**自有车辆的车险保费按月摊销**；
 * 本能力核的是**货运险逐票的投保与理赔台账**（保单号 / 货值 / 定损 / 实收），对象与口径都不同。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档逐单复算表内算术；完整档在此基础上做**少赔 / 漏保 / 重复投保判定**，
 * 并输出按金额排序的索赔处理清单。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**保险条款是否适用、该不该赔，也不给法律意见 —— 只核表内可算关系。
 */

const CHECKS_GIVEN = [
  '保费勾稽（保费 = 投保金额 × 费率）',
  '应赔金额勾稽（定损金额 − 免赔额，负数按 0）',
  '理赔差额勾稽（应赔金额 − 实收理赔款）',
  '投保比例与货值勾稽（投保金额 ÷ 货值）',
  '同一保单号重复检测',
  '关键字段空缺与金额负值检测',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
];

const CHECKS_WITHHELD = [
  '少赔判定（非拒赔行实收低于应赔的差额）',
  '拒赔但实际应赔判定（拒赔行的定损金额高于免赔额）',
  '同一票货重复投保判定（同一运单号在多个保单下投保）',
  '漏保判定（货值高于投保金额的未保部分）',
  '索赔处理清单（按金额从大到小排序并附行号与处理动作）',
];

const OUT_OF_SCOPE = [
  '判断保险条款是否适用、这笔损失该不该赔（条款解释与法律意见）',
  '判断免赔额、费率、投保比例是否合理（那要与保单条款和承保条件对照）',
  '处理共同海损、代位求偿、追偿时效等特殊情形',
  '读取 Excel 或保险公司系统导出的文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '运单号\t保单号\t货值\t投保金额\t投保比例\t费率\t保费\t免赔额\t货损数量\t定损金额\t应赔金额\t实收理赔款\t理赔差额\t理赔状态',
  'YD20260901\tPICC-2026-0001\t1200000.00\t1200000.00\t100.00%\t0.08%\t960.00\t5000.00\t0\t0.00\t0.00\t0.00\t0.00\t未出险',
  'YD20260902\tPICC-2026-0002\t800000.00\t800000.00\t100.00%\t0.08%\t640.00\t3000.00\t12\t50000.00\t47000.00\t47000.00\t0.00\t已赔付',
  'YD20260903\tPICC-2026-0003\t1500000.00\t1500000.00\t100.00%\t0.06%\t900.00\t4000.00\t3\t12000.00\t8000.00\t8000.00\t0.00\t已赔付',
  'YD20260904\tPICC-2026-0004\t600000.00\t600000.00\t100.00%\t0.10%\t600.00\t2000.00\t2\t1500.00\t0.00\t0.00\t0.00\t低于免赔额未赔',
  '合计\t\t4100000.00\t4100000.00\t\t\t3100.00\t14000.00\t17\t63500.00\t55000.00\t55000.00\t0.00\t',
].join('\n');

const TOL = 0.01;
const PCT_TOL = 0.02;   // 投保比例保留两位小数，容差 0.02 个百分点

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的前面（见 tools/header_map_check.py）
  waybill: ['运单号', '提单号', '票号', '货物批次'],
  policy: ['保单号', '保单编号', '投保单号'],
  insuredAmount: ['投保金额', '保险金额', '投保价', '保额'],
  cargoValue: ['货值', '货物价值', '发票货值', '报关货值'],
  insuredRatio: ['投保比例', '投保率'],
  rate: ['费率', '保险费率'],
  premium: ['保费', '保险费'],
  deductible: ['免赔额', '免配额'],
  lossQty: ['货损数量', '受损数量', '货损件数'],
  lossAmount: ['定损金额', '定损额', '核定损失金额', '核定损失'],
  payable: ['应赔金额', '应赔付金额', '应赔'],
  received: ['实收理赔款', '实收赔款', '已收赔款', '理赔到账'],
  gap: ['理赔差额', '差额'],
  claimStatus: ['理赔状态', '赔付状态', '理赔进展'],
};

const LABELS = {
  waybill: '运单号', policy: '保单号', insuredAmount: '投保金额', cargoValue: '货值',
  insuredRatio: '投保比例', rate: '费率', premium: '保费', deductible: '免赔额',
  lossQty: '货损数量', lossAmount: '定损金额', payable: '应赔金额', received: '实收理赔款',
  gap: '理赔差额', claimStatus: '理赔状态',
};

const REQUIRED = ['waybill', 'policy', 'cargoValue', 'insuredAmount', 'insuredRatio',
  'rate', 'premium', 'deductible', 'lossAmount', 'payable', 'received', 'gap'];
const SUM_ROLES = ['cargoValue', 'insuredAmount', 'premium', 'deductible', 'lossQty',
  'lossAmount', 'payable', 'received', 'gap'];
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
      if (role === 'waybill' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const wb = String((it && it.waybill) === undefined ? '' : (it && it.waybill) || '').trim();
  return wb ? `运单「${wb}」` : `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */

function checkPremium(it) {
  const amount = normNumber(it.insuredAmount);
  const rate = normNumber(it.rate);
  const stated = normNumber(it.premium);
  if (amount === null || rate === null || stated === null) return null;
  const expect = round2(amount * rate / 100);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '保费与复算不符', line: it.line,
    message: `${who(it)}的保费是 ${stated.toFixed(2)}，按 投保金额 ${amount.toFixed(2)} × 费率 ${rate}% 应为 ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '费率按保单约定的百分数填；投保金额改了保费要跟着改，别直接沿用上期的保费。',
  };
}

function checkPayable(it) {
  const loss = normNumber(it.lossAmount);
  const ded = normNumber(it.deductible);
  const stated = normNumber(it.payable);
  if (loss === null || ded === null || stated === null) return null;
  const raw = round2(loss - ded);
  const expect = Math.max(0, raw);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应赔金额与复算不符', line: it.line,
    message: `${who(it)}的应赔金额是 ${stated.toFixed(2)}，按 定损金额 ${loss.toFixed(2)} − 免赔额 ${ded.toFixed(2)} = ${raw.toFixed(2)}${raw < 0 ? '（负值按 0 计）' : ''}，应为 ${expect.toFixed(2)}。`,
    advice: '定损金额没超过免赔额时应赔是 0，不是负数；把负数原样填进台账会把理赔差额一起算错。',
  };
}

function checkGap(it) {
  const payable = normNumber(it.payable);
  const received = normNumber(it.received);
  const stated = normNumber(it.gap);
  if (payable === null || received === null || stated === null) return null;
  const expect = round2(payable - received);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '理赔差额与复算不符', line: it.line,
    message: `${who(it)}的理赔差额是 ${stated.toFixed(2)}，按 应赔金额 ${payable.toFixed(2)} − 实收理赔款 ${received.toFixed(2)} = ${expect.toFixed(2)}，对不上。`,
    advice: '赔款分次到账时按累计实收填；只填最后一笔，差额会凭空变小。',
  };
}

function checkRatio(it) {
  const amount = normNumber(it.insuredAmount);
  const value = normNumber(it.cargoValue);
  const stated = normNumber(it.insuredRatio);
  if (amount === null || value === null || stated === null) return null;
  if (Math.abs(value) <= 1e-9) return null;
  const expect = round2(amount / value * 100);
  if (Math.abs(expect - stated) <= PCT_TOL) return null;
  return {
    level: 'P1', category: '投保比例与货值勾稽不符', line: it.line,
    message: `${who(it)}的投保比例是 ${stated}%，按 投保金额 ${amount.toFixed(2)} ÷ 货值 ${value.toFixed(2)} 应为 ${expect}%。`,
    advice: '投保比例这一列是给货值勾稽用的；填了比例就等于声明"这一票保了多少"，货值或投保金额动过它必须跟着动。',
  };
}

function checkNegative(it) {
  const out = [];
  const watch = [['cargoValue', '货值'], ['insuredAmount', '投保金额'], ['premium', '保费'],
    ['deductible', '免赔额'], ['lossAmount', '定损金额'], ['received', '实收理赔款']];
  for (const [role, label] of watch) {
    const v = normNumber(it[role]);
    if (v !== null && v < -TOL) {
      out.push({
        level: 'P0', category: '金额出现负值', line: it.line,
        message: `${who(it)}的「${label}」是 ${v.toFixed(2)}（负数）。`,
        advice: '这几列按台账口径都不会为负：负数要么是公式写反了，要么是把红字冲销混进了金额列。',
      });
    }
  }
  return out;
}

function checkDuplicatePolicy(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = String(it.policy === undefined ? '' : it.policy).trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一保单号出现多行', line: it.line,
        message: `保单号「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '一张保单保多票货是正常的，但要把它们列成保单明细并注明；整行重复会让保费合计翻倍。',
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
          level: 'P0', category: '关键字段空缺或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这一票就算不出来；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
    const loss = normNumber(it.lossAmount);
    if (loss !== null && loss > TOL && isBlank(it.lossQty)) {
      out.push({
        level: 'P1', category: '有定损金额却没填货损数量', line: it.line,
        message: `${who(it)}的定损金额是 ${loss.toFixed(2)}，但「货损数量」是空的。`,
        advice: '索赔要能对上"坏了多少件、定损多少钱"；数量空着，复核时会被打回。',
      });
    }
  }
  return out;
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
    advice: '要么明细行漏了一票，要么合计行没跟着更新。',
  });
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
    return insufficient('没有收到台账正文（text）—— 请把「运单号 / 保单号 / 货值 / 投保金额 / 投保比例 / 费率 / 保费 / 免赔额 / 货损数量 / 定损金额 / 应赔金额 / 实收理赔款 / 理赔差额 / 理赔状态」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `台账缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何运单明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkPremium(it); if (a) findings.push(a);
    const b = checkPayable(it); if (b) findings.push(b);
    const c = checkGap(it); if (c) findings.push(c);
    const d = checkRatio(it); if (d) findings.push(d);
    for (const x of checkNegative(it)) findings.push(x);

  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicatePolicy(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);


  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const sumOf = (role) => {
    let s = 0;
    for (const it of t.items) {
      const v = normNumber(it[role]);
      if (v !== null) s += v;
    }
    return round2(s);
  };

  const result = {
    status: 'success',
    service_type: 'CARGO_INSURANCE_CLAIM_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      cargo_value_total: sumOf('cargoValue'),
      insured_amount_total: sumOf('insuredAmount'),
      premium_total: sumOf('premium'),
      payable_total: sumOf('payable'),
      paid_in_total: sumOf('received'),
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      items: t.items.length,
      rows: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只做表内复算（${CHECKS_GIVEN.length} 项）；少赔、漏保、重复投保判定与索赔处理清单见 scope.checks_not_run（未执行）。`,
    disclaimer: '只核货运险台账内部可算的算术与勾稽（保费 / 应赔 / 差额 / 投保比例，'
      + '以及本次实际执行、已在 scope.checks 里列明的那些判定）；'
      + '**不判断保险条款是否适用、这笔损失该不该赔**，也不给法律意见。结论可由第三方用同一份输入复算。',
  };



  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT,
};
