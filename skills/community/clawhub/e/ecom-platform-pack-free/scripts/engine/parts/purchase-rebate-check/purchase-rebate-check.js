#!/usr/bin/env node
/**
 * purchase-rebate-check.js —— 采购返利与阶梯核算核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**供应商按年度（或季度）采购额给返利，企业年底必须核"返利收足了没有"**：
 *   ① 应得返利 = 年度采购额 × 适用返利率（返利率**按采购额档位**确定）
 *   ② 差额     = 应得返利 − 已收返利（**这一笔经常要等到第二年才被发现没收足**）
 * 返利率用错档、按"上年档位"算、"采购额含不含税"口径不一致 —— 每一种都会让返利少收几万块；
 * 而返利通常在合同附件里按阶梯写，几十个供应商人眼核不动。
 *
 * 与已有能力的区别：`platform-settlement-check` 核**电商平台结算**、`ota-commission-check` 核**渠道佣金**（都是"收到的"）；
 * 本能力核的是**供应商给企业的采购返利**（方向相反、且要按采购额档位定率）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查合同返利条款、不调用大模型；材料不足不给结论；不给采购/税务意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '应得返利勾稽（年度采购额 × 适用返利率）',
  '差额勾稽（应得返利 − 已收返利）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复供应商检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '适用返利率与采购额档位匹配检测（档位表由入参 brackets 给出，缺省则用引擎内置示例档）',
  '返利率超出 0~10% 检测',
  '年度采购额为负检测',
  '已收返利为负检测',
  '差额超过阈值检测（阈值由入参 tolerance 给出，默认 0.01 元；差额为正=尚未收足）',
];

const OUT_OF_SCOPE = [
  '判断返利条款是否合理、以及返利该按含税还是不含税采购额计算（那要看合同）',
  '处理季度返利、累进（超额累进）返利与封顶（请先把适用返利率算好再填）',
  '处理以货抵返利、以及返利对应的进项税转出',
  '判断收入确认时点；给出税务意见',
  '读取 .xlsx 或供应商返利对账单（需要你先导出成文本贴进来）',
];

// 内置示例档位（全额累进：采购额不超过上限时适用该档返利率）。**合同不同，应通过入参 brackets 覆盖。**
const DEFAULT_BRACKETS = [
  [1000000, 1],
  [3000000, 2],
  [5000000, 3],
  [Infinity, 4],
];

const SAMPLE_TEXT = [
  '供应商\t年度采购额\t适用返利率\t应得返利\t已收返利\t差额',
  '甲公司\t800000.00\t1%\t8000.00\t8000.00\t0.00',
  '乙公司\t2500000.00\t2%\t50000.00\t40000.00\t10000.00',
  '合计\t3300000.00\t\t58000.00\t48000.00\t10000.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  party: ['供应商', '厂商', '对方'],
  amount: ['年度采购额', '采购额', '年采购额'],
  rate: ['适用返利率', '返利率', '返利比例'],
  rebate: ['应得返利', '应得返利额', '返利金额'],
  received: ['已收返利', '已收', '实收返利'],
  diff: ['差额', '未收返利', '欠收返利'],
};

const LABELS = {
  party: '供应商', amount: '年度采购额', rate: '适用返利率', rebate: '应得返利',
  received: '已收返利', diff: '差额',
};

const REQUIRED = ['party', 'amount', 'rate', 'rebate', 'received', 'diff'];
const SUM_ROLES = ['amount', 'rebate', 'received', 'diff'];

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
  // ⚠️ 更具体的关键词必须排在更宽泛的前面（本仓库五次踩过的坑）：
  //    「适用返利率」要排在「适用返利」类之前；「应得返利」不能被「返利金额」类抢走。
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

/** 档位：返回该采购额对应的返利率（全额累进）。 */
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
const who = (it) => `供应商「${it.byRole.party || '(未命名)'}」`;

function checkRebate(it) {
  const amount = num(it, 'amount'); const rate = num(it, 'rate'); const stated = num(it, 'rebate');
  if (amount === null || rate === null || stated === null) return null;
  const expect = round2(amount * rate / 100);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应得返利与复算不符', line: it.line,
    message: `${who(it)}的应得返利是 ${stated.toFixed(2)}，按 年度采购额 ${amount.toFixed(2)} × ${rate}% 应为 ${expect.toFixed(2)}。`,
    advice: '返利率是**按采购额档位**定的；用错档（比如按上一年的档）会让返利整体偏一档。',
  };
}

function checkDiff(it) {
  const rebate = num(it, 'rebate'); const received = num(it, 'received'); const stated = num(it, 'diff');
  if (rebate === null || received === null || stated === null) return null;
  const expect = round2(rebate - received);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '差额与复算不符', line: it.line,
    message: `${who(it)}的差额是 ${stated.toFixed(2)}，按 应得返利 ${rebate.toFixed(2)} − 已收返利 ${received.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '差额 = 应得 − 已收；**为正表示还没收足**，年底要据此向供应商追。',
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
        advice: '注意：**返利率是比率，不能按行相加**（合计行里应为空）。',
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
        level: 'P1', category: '同一供应商出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一供应商分不同品类/季度分行是正常的；但若本表按供应商汇总，重复行会让采购额与返利一起翻倍。',
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
          advice: '缺这一格这笔返利就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的采购返利核对表（要能认出「年度采购额」「适用返利率」「应得返利」「已收返利」「差额」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从采购/应付台账导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个供应商的明细行']);

  const brackets = Array.isArray(payload && payload.brackets) && payload.brackets.length
    ? payload.brackets.map((b) => [Number(b[0]) === 0 ? 0 : (Number.isFinite(Number(b[0])) ? Number(b[0]) : Infinity), Number(b[1])])
    : DEFAULT_BRACKETS;
  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkRebate(it); if (a) findings.push(a);
    const b = checkDiff(it); if (b) findings.push(b);
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
      suppliers: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      amount_total: sumOf('amount'),
      rebate_total: sumOf('rebate'),
      received_total: sumOf('received'),
      diff_total: sumOf('diff'),
      brackets_used: brackets,
      basis: '应得返利 = 年度采购额 × 适用返利率（返利率按采购额档位确定）；差额 = 应得返利 − 已收返利；'
        + '合计行逐列复核（比率列不参与求和）。',
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
      + '不代表返利条款口径（含税/不含税、累进方式）判断正确 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, DEFAULT_BRACKETS,
};
