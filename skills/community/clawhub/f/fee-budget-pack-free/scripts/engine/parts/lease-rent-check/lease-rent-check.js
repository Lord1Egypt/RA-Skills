#!/usr/bin/env node
/**
 * lease-rent-check.js —— 租金账单与押金结算核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**有租入场地/门店的企业每月都要核一遍出租方给的租金账单**：
 *   ① 本期应收租金 = 合同月租金 × 本期计租月数（新签合同常带免租期，月数要扣掉）
 *   ② 本期应收合计 = 本期应收租金 + 上期欠租（欠租滚存最容易漏）
 *   ③ 期末欠租     = 本期应收合计 − 本期实收
 * 免租期算错、欠租没滚进来、实收与应收对不上 —— 每一项都会变成多付或少付的钱；
 * 而且退租时还要按这套账结算押金。几十个租户，人眼核不动；这些都是**纯算术**。
 *
 * 与已有能力的区别：`utility-allocation-check` 核的是**公共费用分摊**（电费水费按面积分摊给租户），
 * **不含租金、不含欠租滚存**；本能力核的是**租金账单本身**（月租金 × 计租月数 + 欠租 − 实收）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不调用大模型；材料不足不给结论；不给法律意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '本期应收租金勾稽（合同月租金 × 本期计租月数）',
  '本期应收合计勾稽（本期应收租金 + 上期欠租）',
  '期末欠租勾稽（本期应收合计 − 本期实收）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复租户检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '合同月租金非正检测',
  '期末欠租为负检测（多收或已预收，需与预收账款核对）',
  '免租月数超出 0~12 检测',
  '本期计租月数超出 0~12 检测',
  '本期实收为负检测',
];

const OUT_OF_SCOPE = [
  '判断租赁合同条款（免租期、递增、押金）是否合法或合理',
  '处理租金递增、按面积单价计租、以及抽成租金（请先算出本期应收租金再核）',
  '处理税金（增值税/房产税）与开票口径',
  '押金的收付与退还分录（本工具只核租金账单上的算术）',
  '给出法律或税务意见；读取 .xlsx（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '租户\t合同月租金\t免租月数\t本期计租月数\t本期应收租金\t上期欠租\t本期应收合计\t本期实收\t期末欠租',
  '甲公司\t50000.00\t3\t12\t600000.00\t0.00\t600000.00\t600000.00\t0.00',
  '乙公司\t30000.00\t3\t9\t270000.00\t20000.00\t290000.00\t250000.00\t40000.00',
  '合计\t80000.00\t\t21\t870000.00\t20000.00\t890000.00\t850000.00\t40000.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  party: ['租户', '承租方', '客户名称', '商户'],
  monthly: ['合同月租金', '月租金', '月租'],
  freeMonths: ['免租月数', '免租期'],
  months: ['本期计租月数', '计租月数', '计租月份'],
  rent: ['本期应收租金', '应收租金'],
  totalDue: ['本期应收合计', '应收合计'],
  received: ['本期实收', '实收金额', '已收'],
  // ⚠️ 「期末欠租」必须排在「欠租」之前：否则 `欠租` 会把「期末欠租」先抢走，
  //    导致必需列 dueEnd 永远认不出来 ⇒ 整表被判 insufficient_input（第一版就这样）。
  dueEnd: ['期末欠租', '期末应收', '欠租余额'],
  arrears: ['上期欠租', '期初欠租', '欠租'],
};

const LABELS = {
  party: '租户', monthly: '合同月租金', freeMonths: '免租月数', months: '本期计租月数',
  rent: '本期应收租金', arrears: '上期欠租', totalDue: '本期应收合计',
  received: '本期实收', dueEnd: '期末欠租',
};

const REQUIRED = ['party', 'monthly', 'freeMonths', 'months', 'rent', 'arrears', 'totalDue', 'received', 'dueEnd'];
const SUM_ROLES = ['monthly', 'freeMonths', 'months', 'rent', 'arrears', 'totalDue', 'received', 'dueEnd'];

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
  // 「本期应收合计」必须排在「本期应收租金」之前，否则会被"应收租金"抢走
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
const who = (it) => `租户「${it.byRole.party || '(未命名)'}」`;

function checkRent(it) {
  const monthly = num(it, 'monthly');
  const months = num(it, 'months');
  const stated = num(it, 'rent');
  if (monthly === null || months === null || stated === null) return null;
  const expect = round2(monthly * months);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '本期应收租金与复算不符', line: it.line,
    message: `${who(it)}的本期应收租金是 ${stated.toFixed(2)}，`
      + `按 合同月租金 ${monthly.toFixed(2)} × 计租月数 ${months} 复算应为 ${expect.toFixed(2)}。`,
    advice: '免租期要在"计租月数"里扣掉；月租金或月数录错会直接把账单金额算歪。',
  };
}

function checkTotalDue(it) {
  const rent = num(it, 'rent');
  const arrears = num(it, 'arrears');
  const stated = num(it, 'totalDue');
  if (rent === null || arrears === null || stated === null) return null;
  const expect = round2(rent + arrears);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '本期应收合计与复算不符', line: it.line,
    message: `${who(it)}的本期应收合计是 ${stated.toFixed(2)}，`
      + `按 本期应收租金 ${rent.toFixed(2)} + 上期欠租 ${arrears.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '上期欠租最容易漏：它是滚存项，漏掉就等于少收一笔。',
  };
}

function checkDueEnd(it) {
  const totalDue = num(it, 'totalDue');
  const received = num(it, 'received');
  const stated = num(it, 'dueEnd');
  if (totalDue === null || received === null || stated === null) return null;
  const expect = round2(totalDue - received);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '期末欠租与复算不符', line: it.line,
    message: `${who(it)}的期末欠租是 ${stated.toFixed(2)}，`
      + `按 本期应收合计 ${totalDue.toFixed(2)} − 本期实收 ${received.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '期末欠租要原样滚到下期的"上期欠租"，这里错了下期也会跟着错。',
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
        advice: '要么明细行漏了租户，要么合计行没跟着更新。',
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
        level: 'P1', category: '同一租户出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一租户多个铺位是正常的；但若本表按租户汇总，重复行会让应收与欠租一起翻倍。',
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
          advice: '缺这一格这笔租金就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的租金账单/结算表（要能认出「合同月租金」「免租月数」「本期计租月数」「本期应收租金」'
      + '「上期欠租」「本期应收合计」「本期实收」「期末欠租」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从租赁台账导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个租户的明细行']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkRent(it); if (a) findings.push(a);
    const b = checkTotalDue(it); if (b) findings.push(b);
    const c = checkDueEnd(it); if (c) findings.push(c);
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
      tenants: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      rent_total: sumOf('rent'),
      total_due_total: sumOf('totalDue'),
      received_total: sumOf('received'),
      arrears_end_total: sumOf('dueEnd'),
      basis: '本期应收租金 = 合同月租金 × 本期计租月数；本期应收合计 = 本期应收租金 + 上期欠租；'
        + '期末欠租 = 本期应收合计 − 本期实收；合计行逐列复核。',
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
      + '不代表合同条款合理、也不代表押金应退多少 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
