#!/usr/bin/env node
/**
 * platform-settlement-check.js —— 电商平台结算核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**任何在电商平台卖货的商家，每个月都要跟平台对一次结算单** ——
 * 平台按「销售额 − 佣金 − 技术服务费 − 运费 − 退款 = 结算金额」逐单结算，
 * 单量动辄几千上万，人眼根本核不过来；而这些**全是算术**。
 * 少算的那部分就是真金白银。
 *
 * 与已有能力的区别：本能力核**平台→商家的结算链**（佣金/服务费/运费/退款），
 * 不是银行流水对账，也不是采购三单匹配。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不调用大模型；材料不足不给结论；不判断平台费率是否合理。
 */
'use strict';

const CHECKS_GIVEN = [
  '逐单结算勾稽（销售额 − 平台佣金 − 技术服务费 − 运费 − 退款 = 结算金额）',
  '合计行复核（每一列的合计是否等于各单之和）',
  '重复订单号检测（重复计费/重复结算线索）',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '佣金率区间校验（佣金 ÷ 销售额，默认 0.5%~30%）',
  '结算金额为负检测（异常冲销）',
  '退款大于销售额检测',
  '零销售额却有费用检测（挂错单）',
];

const OUT_OF_SCOPE = [
  '判断平台费率、佣金比例定得合不合理（那是商务谈判与平台规则的事）',
  '核对平台是否真的打了款（那要拿银行流水来对）',
  '核对商品是否真的发出、退货是否真实（那要拿订单与物流记录比）',
  '给出税务或审计意见',
  '读取 .xlsx（需要你先从平台后台导出、复制成文本贴进来）',
];

const SAMPLE_TEXT = [
  '订单号\t商品销售额\t平台佣金\t技术服务费\t运费\t退款\t结算金额',
  'SO-001\t1000.00\t50.00\t10.00\t8.00\t0.00\t932.00',
  'SO-002\t2000.00\t100.00\t20.00\t0.00\t200.00\t1680.00',
  'SO-003\t500.00\t25.00\t5.00\t8.00\t0.00\t462.00',
  '合计\t3500.00\t175.00\t35.00\t16.00\t200.00\t3074.00',
].join('\n');

const RATE_MIN = 0.005;
const RATE_MAX = 0.30;
const TOL = 0.01;

const ROLE_LABELS = {
  order: '订单号', sales: '商品销售额', commission: '平台佣金',
  techFee: '技术服务费', shipping: '运费', refund: '退款', payout: '结算金额',
};
const labelOf = (r) => ROLE_LABELS[r] || r;
const SUM_ROLES = ['sales', 'commission', 'techFee', 'shipping', 'refund', 'payout'];

const COLUMN_ROLES = [
  [/订单号|单号|子订单|交易号/, 'order'],
  [/商品销售额|销售额|商品金额|成交金额|货款/, 'sales'],
  [/平台佣金|佣金|扣点/, 'commission'],
  [/技术服务费|服务费|技术费|平台服务费/, 'techFee'],
  [/运费|物流费|配送费/, 'shipping'],
  [/退款|退货|售后/, 'refund'],
  [/结算金额|实结|应结|打款金额|结算/, 'payout'],
];

const NON_AMOUNT_KWS = /备注|状态|日期|月份|店铺|商品名称|类目|买家/;

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t');
  if (line.indexOf(',') >= 0) return line.split(',');
  return line.trim().split(/\s{2,}|\s+/);
}

function roleOf(header) {
  const h = String(header || '').replace(/\s/g, '');
  if (!h) return 'skip';
  if (NON_AMOUNT_KWS.test(h)) return 'skip';
  for (const pair of COLUMN_ROLES) if (pair[0].test(h)) return pair[1];
  return 'extra';
}

function normAmount(v) {
  if (v === null || v === undefined) return null;
  let s = String(v).trim();
  if (!s) return null;
  let neg = false;
  if (/^\(.*\)$/.test(s)) { neg = true; s = s.slice(1, -1); }
  s = s.replace(/[¥￥,\s]/g, '').replace(/元$/, '');
  if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
  const n = Number(s);
  return neg ? -n : n;
}

function isBlank(v) {
  const s = String(v === null || v === undefined ? '' : v).trim();
  if (!s) return true;
  return /^(--+|\?\?+|N\/?A|na|待填|TODO|xxx|\*\*\*?)$/i.test(s);
}

function findHeader(lines) {
  for (let i = 0; i < Math.min(lines.length, 10); i += 1) {
    const cells = splitRow(lines[i]).map((c) => c.trim());
    const roles = cells.map(roleOf);
    const known = roles.filter((r) => r !== 'skip' && r !== 'extra');
    const money = ['sales', 'payout', 'commission'].filter((r) => known.includes(r)).length;
    if (known.includes('order') && money >= 2) return { index: i, cells, roles };
  }
  return null;
}

function parseTable(text) {
  const lines = String(text).split(/\r?\n/);
  const header = findHeader(lines);
  if (!header) return { error: 'no_header' };
  const items = [];
  const totals = [];
  for (let i = header.index + 1; i < lines.length; i += 1) {
    const raw = lines[i];
    if (!raw || !raw.trim()) continue;
    const cells = splitRow(raw).map((c) => c.trim());
    const rec = { line: i + 1, raw: raw.trim(), byRole: {} };
    header.roles.forEach((role, ci) => {
      if (role === 'skip' || role === 'extra') return;
      rec.byRole[role] = cells[ci] === undefined ? '' : cells[ci];
    });
    const key = String(rec.byRole.order || '').trim();
    if (/^(合计|总计|小计|total)/i.test(key)) totals.push(rec); else items.push(rec);
  }
  return { header, items, totals, cols: header.cells };
}

function finding(level, category, line, message, evidence, advice) {
  return { level, category, line, message, evidence, advice };
}

const tag = (rec) => String(rec.byRole.order || '（无订单号）').trim();

function checkSettlement(rec) {
  const s = normAmount(rec.byRole.sales);
  const c = normAmount(rec.byRole.commission);
  const t = normAmount(rec.byRole.techFee);
  const f = normAmount(rec.byRole.shipping);
  const r = normAmount(rec.byRole.refund);
  const p = normAmount(rec.byRole.payout);
  if ([s, c, t, f, r, p].some((x) => x === null)) return null;
  const expect = Math.round((s - c - t - f - r) * 100) / 100;
  if (Math.abs(expect - p) <= TOL) return null;
  return finding('P0', '结算金额不平', rec.line,
    tag(rec) + ' 的结算金额是 ' + p.toFixed(2) + '，但「销售额 ' + s.toFixed(2) + ' − 佣金 '
      + c.toFixed(2) + ' − 技术服务费 ' + t.toFixed(2) + ' − 运费 ' + f.toFixed(2) + ' − 退款 '
      + r.toFixed(2) + '」应为 ' + expect.toFixed(2) + '（差 ' + (p - expect).toFixed(2) + '）',
    rec.raw, '先确认口径：如果有平台补贴、活动扣款、保证金扣除，请把它们也列成一列再核。');
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals.length) return out;
  const t = totals[0];
  for (const role of SUM_ROLES) {
    const claimed = normAmount(t.byRole[role]);
    if (claimed === null) continue;
    let sum = 0; let ok = true;
    for (const it of items) {
      const n = normAmount(it.byRole[role]);
      if (n === null) { ok = false; break; }
      sum += n;
    }
    if (!ok) continue;
    sum = Math.round(sum * 100) / 100;
    if (Math.abs(sum - claimed) <= TOL) continue;
    out.push(finding('P0', '合计行算错', t.line,
      '合计行的「' + labelOf(role) + '」写的是 ' + claimed.toFixed(2) + '，但各单相加是 '
        + sum.toFixed(2) + '（差 ' + (claimed - sum).toFixed(2) + '）',
      t.raw, '合计行是打款依据，对不上时通常有单被漏加或重复加。'));
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.order || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push(finding('P0', '订单号重复', it.line,
        key + ' 出现了两次（上一次在第 ' + seen.get(key) + ' 行）',
        it.raw, '同一订单号两行就是**重复结算**，必须让平台核减。'));
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  const TXT = ['order'];
  const roles = Object.keys(items[0] ? items[0].byRole : {}).filter((r) => TXT.indexOf(r) < 0);
  for (const it of items) {
    if (!String(it.byRole.order || '').trim()) {
      out.push(finding('P1', '订单号缺失', it.line, '这一行没有订单号', it.raw,
        '没有订单号无法与订单明细核对，请确认这一行是否有效。'));
    }
    for (const r of roles) {
      const v = it.byRole[r];
      if (isBlank(v)) {
        out.push(finding('P1', '该填没填', it.line,
          tag(it) + ' 的「' + labelOf(r) + '」是空的或还是占位符（' + (String(v).trim() || '空') + '）',
          it.raw, '结算单出现空列，通常是从后台导出时漏选。'));
      } else if (normAmount(v) === null) {
        out.push(finding('P1', '金额无法解析', it.line,
          tag(it) + ' 的「' + labelOf(r) + '」写作「' + String(v).trim() + '」，不是能计算的金额',
          it.raw, '请确认列是否串位。'));
      }
    }
  }
  return out;
}

function checkCommissionRate(rec) {
  const s = normAmount(rec.byRole.sales);
  const c = normAmount(rec.byRole.commission);
  if (s === null || c === null || s === 0) return null;
  const rate = c / s;
  if (rate >= RATE_MIN - 1e-9 && rate <= RATE_MAX + 1e-9) return null;
  return finding('P1', '佣金率超出常见区间', rec.line,
    tag(rec) + ' 的佣金率是 ' + (rate * 100).toFixed(2) + '%（佣金 ' + c.toFixed(2)
      + ' ÷ 销售额 ' + s.toFixed(2) + '），不在 0.5%~30% 之间',
    rec.raw, '可能是把佣金填成了金额以外的数，或这单适用了特殊类目费率。请对照平台费率表确认。');
}

function checkNegative(rec) {
  const p = normAmount(rec.byRole.payout);
  if (p === null || p >= 0) return null;
  return finding('P1', '结算金额为负', rec.line,
    tag(rec) + ' 的结算金额是 ' + p.toFixed(2) + '（负数）',
    rec.raw, '负数结算通常是退款/售后冲销超过当期销售额；请确认是否跨期，以及平台是否另有抵扣。');
}

function checkRefundOverSales(rec) {
  const s = normAmount(rec.byRole.sales);
  const r = normAmount(rec.byRole.refund);
  if (s === null || r === null) return null;
  if (r <= s + TOL) return null;
  return finding('P1', '退款大于销售额', rec.line,
    tag(rec) + ' 的退款 ' + r.toFixed(2) + ' 超过销售额 ' + s.toFixed(2),
    rec.raw, '可能是跨单退款被挂到了这一单，或销售额漏填。');
}

function checkZeroSales(rec) {
  const s = normAmount(rec.byRole.sales);
  if (s === null || s !== 0) return null;
  const fees = ['commission', 'techFee', 'shipping'].reduce((acc, k) => {
    const n = normAmount(rec.byRole[k]);
    return acc + (n === null ? 0 : n);
  }, 0);
  if (fees === 0) return null;
  return finding('P1', '零销售额却有费用', rec.line,
    tag(rec) + ' 的销售额是 0，但佣金/服务费/运费合计 ' + fees.toFixed(2),
    rec.raw, '可能是销售额漏填，或这一单是纯费用项被挂错位置。');
}

function insufficient(missing) {
  return { status: 'insufficient_input', missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。' };
}

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['平台结算单原文（text）']);
  const t = parseTable(text);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的结算单（要能认出「订单号」+ 至少「销售额」「结算金额」「佣金」里的两个）',
      '从平台后台导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一条订单明细行']);

  const paid = Boolean(payload && (payload.full || payload.credit || payload.token));
  const findings = [];
  const notRun = [];
  for (const it of t.items) {
    const a = checkSettlement(it); if (a) findings.push(a);
    if (paid) {
      const r = checkCommissionRate(it); if (r) findings.push(r);
      const n = checkNegative(it); if (n) findings.push(n);
      const o = checkRefundOverSales(it); if (o) findings.push(o);
      const z = checkZeroSales(it); if (z) findings.push(z);
    }
  }
  for (const f of checkTotalRow(t.totals, t.items)) findings.push(f);
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);
  if (!paid) notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => Math.round(t.items.reduce((s, it) => {
    const n = normAmount(it.byRole[role]);
    return s + (n === null ? 0 : n);
  }, 0) * 100) / 100;

  const result = {
    findings,
    summary: {
      orders: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      sales_total: sumOf('sales'),
      payout_total: sumOf('payout'),
      basis: '逐单「销售额−佣金−技术服务费−运费−退款=结算金额」比对；合计行逐列复核',
    },
    columns: t.cols,
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明这张结算单**算得对**，'
      + '不代表平台真的打了款、也不代表费率合理 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normAmount, isBlank, labelOf,
  CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT,
  ROLE_LABELS, SUM_ROLES, RATE_MIN, RATE_MAX,
};
