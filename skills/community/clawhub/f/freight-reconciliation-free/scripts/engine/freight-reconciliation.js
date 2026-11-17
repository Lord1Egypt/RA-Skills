#!/usr/bin/env node
/**
 * freight-reconciliation.js —— 运费对账引擎（确定性、纯 Node 标准库）。
 *
 * 为什么做这个：
 *   **有发货的公司每个月都要跟物流商对一次运费**：把月结单逐单核一遍。
 *   逐单核「重量 × 单价 = 运费」「运费 + 附加费 = 小计」、合计行是不是各单之和、
 *   有没有重复运单号（重复计费）、有没有该填没填、有没有重量为 0 却有运费 ——
 *   这些**全是算术**。物流费通常排在企业成本前几位，而月结单动辄几百上千行，
 *   人眼逐单核算不现实，多算的运费基本就付掉了。
 *
 * 与已有能力的区别（不是重复品）：
 *   · `three-way-match` 核「采购订单/入库单/发票」；`bank-reconciliation` 核「银行流水/企业账面」；
 *   · 本能力核的是「**物流商月结单内部的逐单计价**」—— 重量、单价、运费、附加费、小计这条链。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约（与其它引擎一致）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *
 * 刻意不做的事：不联网、不调用大模型；材料不足不给结论；
 * **不判断物流商报价合不合理**（那是商务谈判与合同的事）。
 */
'use strict';

const CHECKS_GIVEN = [
  '逐单运费复核（重量 × 单价 = 运费）',
  '逐单小计复核（运费 + 附加费 = 小计）',
  '合计行复核（每一列的合计是否等于各单之和）',
  '重复运单号检测（重复计费线索）',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '零重量却有运费（异常计费线索）',
  '运费或小计为负（冲减方向异常）',
  '同目的地单价不一致（同一区域内单价应一致）',
  '重量缺失但有运费',
];

const OUT_OF_SCOPE = [
  '判断物流商报价是否合理、该不该换供应商（那是商务谈判与合同的事）',
  '核对包裹是否真的发出、有没有丢件（那要拿发货记录与签收记录比）',
  '核对与物流商对账单的差异（那要拿到对方的对账单；本工具只核你贴进来的这一份）',
  '给出税务或审计意见',
  '读取 .xlsx（需要你先从 Excel 复制成文本贴进来）',
];

/* 干净样例：逐单两条恒等式都吻合，合计行也对得上。
   SF001 华东 10.5 × 8.00 = 84.00，+6.00 = 90.00
   SF002 华南 20.0 × 9.00 = 180.00，+0 = 180.00
   SF003 华东  5.5 × 8.00 = 44.00， +6.00 = 50.00 */
const SAMPLE_TEXT = [
  '运单号\t目的地\t重量\t单价\t运费\t附加费\t小计',
  'SF001\t华东\t10.5\t8.00\t84.00\t6.00\t90.00',
  'SF002\t华南\t20.0\t9.00\t180.00\t0.00\t180.00',
  'SF003\t华东\t5.5\t8.00\t44.00\t6.00\t50.00',
  '合计\t\t36.0\t\t308.00\t12.00\t320.00',
].join('\n');

const ROLE_LABELS = {
  waybill: '运单号', dest: '目的地', weight: '重量', price: '单价',
  freight: '运费', surcharge: '附加费', subtotal: '小计',
};
const labelOf = (r) => ROLE_LABELS[r] || r;
const SUM_ROLES = ['weight', 'freight', 'surcharge', 'subtotal'];

const COLUMN_ROLES = [
  [/运单号|单号|快递单号|物流单号/, 'waybill'],
  [/目的地|目的站|到站|区域|线路|省份|城市/, 'dest'],
  [/重量|计费重|实重|kg|公斤/, 'weight'],
  [/单价|费率|单价\s*\(元/, 'price'],
  [/附加费|燃油费|上楼费|续重费|其他费用|杂费/, 'surcharge'],
  [/运费|运输费|干线费|配送费/, 'freight'],
  [/小计|合计金额|应付金额|金额/, 'subtotal'],
];

const NON_AMOUNT_KWS = /备注|状态|日期|月份|签收|经办|承运|发货/;

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
  s = s.replace(/[¥￥,\s]/g, '').replace(/元$/, '').replace(/kg$/i, '');
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
    const need = ['freight', 'subtotal', 'weight', 'price'].filter((r) => known.includes(r));
    if (need.length >= 3) return { index: i, cells, roles };
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
    const nm = String(rec.byRole.waybill || '').trim();
    if (/^(合计|总计|小计|total|应付)/i.test(nm)) totals.push(rec); else items.push(rec);
  }
  return { header, items, totals, cols: header.cells };
}

function finding(level, category, line, message, evidence, advice) {
  return { level, category, line, message, evidence, advice };
}

const tag = (rec) => String(rec.byRole.waybill || '（无单号）').trim();

function checkFreight(rec) {
  const w = normAmount(rec.byRole.weight);
  const p = normAmount(rec.byRole.price);
  const f = normAmount(rec.byRole.freight);
  if (w === null || p === null || f === null) return null;
  const expect = Math.round(w * p * 100) / 100;
  if (Math.abs(expect - f) <= 0.01) return null;
  return finding('P0', '运费不等于重量×单价', rec.line,
    tag(rec) + ' 的运费是 ' + f.toFixed(2) + '，但「重量 ' + w + ' × 单价 ' + p.toFixed(2)
      + '」应为 ' + expect.toFixed(2) + '（差 ' + (f - expect).toFixed(2) + '）',
    rec.raw, '若物流商用的是阶梯价或首重续重，请把计价后的运费与单价口径对齐，或按他们的价目表核对。');
}

function checkSubtotal(rec) {
  const f = normAmount(rec.byRole.freight);
  const s = normAmount(rec.byRole.surcharge);
  const t = normAmount(rec.byRole.subtotal);
  if (f === null || s === null || t === null) return null;
  const expect = Math.round((f + s) * 100) / 100;
  if (Math.abs(expect - t) <= 0.01) return null;
  return finding('P0', '小计不等于运费+附加费', rec.line,
    tag(rec) + ' 的小计是 ' + t.toFixed(2) + '，但「运费 ' + f.toFixed(2) + ' + 附加费 '
      + s.toFixed(2) + '」应为 ' + expect.toFixed(2) + '（差 ' + (t - expect).toFixed(2) + '）',
    rec.raw, '小计是结算金额，算错会直接多付或少付运费。');
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals.length) return out;
  const t = totals[0];
  for (const role of SUM_ROLES) {
    const claimed = normAmount(t.byRole[role]);
    if (claimed === null) continue;
    let sum = 0;
    let ok = true;
    for (const it of items) {
      const n = normAmount(it.byRole[role]);
      if (n === null) { ok = false; break; }
      sum += n;
    }
    if (!ok) continue;
    sum = Math.round(sum * 100) / 100;
    if (Math.abs(sum - claimed) <= 0.01) continue;
    out.push(finding('P0', '合计行算错', t.line,
      '合计行的「' + labelOf(role) + '」写的是 ' + claimed + '，但各单相加是 ' + sum
        + '（差 ' + Math.round((claimed - sum) * 100) / 100 + '）',
      t.raw, '合计行是结算总额，对不上时通常有单被漏加或重复加。'));
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.waybill || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push(finding('P0', '运单号重复', it.line,
        key + ' 出现了两次（上一次在第 ' + seen.get(key) + ' 行）',
        it.raw, '同一运单号出现两次就是**重复计费**，必须让物流商核减；这是最常见的多付运费原因。'));
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  // 只校验**金额/数量**角色；运单号与目的地是文本，拿去 normAmount 必然解析失败 ——
  // 第一版漏了这个过滤，干净样例直接报 3 条「数值无法解析」的假问题。
  const TXT_ROLES = ['waybill', 'dest'];
  const roles = Object.keys(items[0] ? items[0].byRole : {}).filter((r) => TXT_ROLES.indexOf(r) < 0);
  for (const it of items) {
    if (!String(it.byRole.waybill || '').trim()) {
      out.push(finding('P1', '运单号缺失', it.line, '这一行没有运单号', it.raw,
        '没有单号就无法与发货记录核对，请确认这一行是否有效。'));
    }
    for (const r of roles) {
      const v = it.byRole[r];
      if (isBlank(v)) {
        out.push(finding('P1', '该填没填', it.line,
          tag(it) + ' 的「' + labelOf(r) + '」是空的或还是占位符（' + (String(v).trim() || '空') + '）',
          it.raw, '月结单出现空列，通常是从系统导出时漏选，或模板没替换。'));
      } else if (normAmount(v) === null) {
        out.push(finding('P1', '数值无法解析', it.line,
          tag(it) + ' 的「' + labelOf(r) + '」写作「' + String(v).trim() + '」，不是能计算的数值',
          it.raw, '请确认列是否串位。'));
      }
    }
  }
  return out;
}

/** 同目的地单价不一致：同一区域同一条线路，单价应一致（跨行比对）。 */
function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。',
  };
}

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['运费月结单原文（text）']);
  const t = parseTable(text);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的月结单（要能认出「运单号」和「重量」「单价」「运费」「小计」里的至少三个）',
      '从物流商给的 Excel/系统导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一条运单明细行']);

  const findings = [];
  const notRun = [];
  for (const it of t.items) {
    const a = checkFreight(it); if (a) findings.push(a);
    const b = checkSubtotal(it); if (b) findings.push(b);

  }
  for (const f of checkTotalRow(t.totals, t.items)) findings.push(f);
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => Math.round(t.items.reduce((s, it) => {
    const n = normAmount(it.byRole[role]);
    return s + (n === null ? 0 : n);
  }, 0) * 100) / 100;

  const result = {
    findings,
    summary: {
      waybills: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      freight_total: sumOf('freight'),
      surcharge_total: sumOf('surcharge'),
      payable_total: sumOf('subtotal'),
      basis: '逐单「重量 × 单价 = 运费」「运费 + 附加费 = 小计」比对；合计行逐列复核',
    },
    columns: t.cols,
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明这张月结单**算得对**，'
      + '不代表包裹真的都发出了、也不代表报价合理 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normAmount, isBlank, labelOf, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, ROLE_LABELS, SUM_ROLES,
};
