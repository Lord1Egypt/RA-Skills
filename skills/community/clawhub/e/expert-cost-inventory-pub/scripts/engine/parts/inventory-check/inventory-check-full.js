#!/usr/bin/env node
/**
 * inventory-check.js —— 库存账实核对引擎（确定性、纯 Node 标准库）。
 *
 * 为什么做这个：
 *   **每月（或每季）盘点后，仓管与财务必须把盘点表核一遍**：
 *   逐品「期初 + 入库 − 出库 = 账面期末」对不对、
 *   账面期末与实盘数的差异是多少、差异金额 = 数量 × 单价 对不对、
 *   合计行是不是各品之和、有没有重复品类、有没有该填没填。
 *   盘点差异直接决定盘盈盘亏的账务处理，而这些**全是算术**。
 *
 * 契约（与其它引擎一致）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *
 * 刻意不做的事：不联网、不调用大模型；材料不足不给结论；
 * 不判断"差异该不该报损"或"该按什么成本计价"（那是会计政策的事）。
 */
'use strict';

const CHECKS_GIVEN = [
  '逐品账面结存勾稽（期初 + 入库 − 出库 = 账面期末）',
  '差异数量复核（账面期末 − 实盘数量 = 差异）',
  '差异金额复核（差异数量 × 单价 = 差异金额）',
  '合计行复核（每一列的合计是否等于各品之和）',
  '重复品类检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '差异率超阈值提示（|差异金额| ÷ 账面金额，默认阈值 5%）',
  '负库存检测（账面期末或实盘为负）',
  '入库金额与数量×单价勾稽',
  '长期不动品提示（期初 = 期末且本期无出入库）',
];

const OUT_OF_SCOPE = [
  '判断盘盈盘亏该不该报损、该记什么科目（那是会计政策与审批流程的事）',
  '判断存货该按什么方法计价（先进先出 / 加权平均 / 个别计价）',
  '核对实物是否真的存在（那要人去数，本工具只核你数出来的数）',
  '给出审计或税务意见',
  '读取 .xlsx（需要你先从 Excel 复制成文本贴进来）',
];

/* 样例：三项都严丝合缝，且差异为 0（干净样例必须零发现）。
   甲：期初 100 + 入库 50 − 出库 30 = 120（账面），实盘 120 → 差异 0
   乙：期初 200 + 入库 0 − 出库 80 = 120（账面），实盘 118 → 差异 2，单价 25 → 差异金额 50
   丙：期初 0 + 入库 300 − 出库 100 = 200（账面），实盘 200 → 差异 0 */
const SAMPLE_TEXT = [
  '品类\t品名\t期初数量\t入库数量\t出库数量\t账面结存\t实盘数量\t差异数量\t单价\t差异金额',
  'A-01\t螺纹钢\t100\t50\t30\t120\t120\t0\t3800.00\t0.00',
  'A-02\t水泥\t200\t0\t80\t120\t118\t2\t25.00\t50.00',
  'A-03\t砂石\t0\t300\t100\t200\t200\t0\t120.00\t0.00',
  '合计\t\t300\t350\t210\t440\t438\t2\t\t50.00',
].join('\n');

const DIFF_RATIO_THRESHOLD = 0.05;

const ROLE_LABELS = {
  code: '品类', name: '品名', opening: '期初数量', inQty: '入库数量', outQty: '出库数量',
  bookQty: '账面结存', actualQty: '实盘数量', diffQty: '差异数量', price: '单价',
  inAmount: '入库金额', diffAmount: '差异金额',
};
const labelOf = (r) => ROLE_LABELS[r] || r;
const QTY_ROLES = ['opening', 'inQty', 'outQty', 'bookQty', 'actualQty', 'diffQty'];

const COLUMN_ROLES = [
  [/^品类|物料编码|存货编码|商品编码|物料编号/, 'code'],
  [/^品名|物料名称|存货名称|商品名称|名称/, 'name'],
  [/期初|上期结存|期初结存/, 'opening'],
  [/入库|进货|购入|收入数量/, 'inQty'],
  [/出库|销货|发出|发出数量/, 'outQty'],
  [/账面|账存|账面结存|账面数量|结存数量/, 'bookQty'],
  [/实盘|实存|盘点数|实际数量/, 'actualQty'],
  [/差异数量|盘盈盘亏数量|盈亏数量/, 'diffQty'],
  [/单价|单位成本/, 'price'],
  [/入库金额|进货金额|购入金额/, 'inAmount'],
  [/差异金额|盈亏金额|盘盈盘亏金额/, 'diffAmount'],
];

const NON_AMOUNT_KWS = /备注|状态|日期|月份|仓库|库位|经办|盘点人|类别/;

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
    const hasKey = known.includes('code') || known.includes('name');
    const qty = QTY_ROLES.filter((r) => known.includes(r)).length;
    if (hasKey && qty >= 3) return { index: i, cells, roles };
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
    const nm = String(rec.byRole.code || rec.byRole.name || '').trim();
    if (/^(合计|总计|小计|total)/i.test(nm)) totals.push(rec); else items.push(rec);
  }
  return { header, items, totals, cols: header.cells };
}

function finding(level, category, line, message, evidence, advice) {
  return { level, category, line, message, evidence, advice };
}

function tag(rec) {
  const c = String(rec.byRole.code || '').trim();
  const n = String(rec.byRole.name || '').trim();
  return c && n ? c + ' ' + n : (c || n || '（未命名品类）');
}

function checkBook(rec) {
  const o = normAmount(rec.byRole.opening);
  const i = normAmount(rec.byRole.inQty);
  const u = normAmount(rec.byRole.outQty);
  const b = normAmount(rec.byRole.bookQty);
  if (o === null || i === null || u === null || b === null) return null;
  const expect = Math.round((o + i - u) * 100) / 100;
  if (Math.abs(expect - b) <= 0.005) return null;
  return finding('P0', '账面结存不平', rec.line,
    tag(rec) + ' 的账面结存是 ' + b + '，但「期初 ' + o + ' + 入库 ' + i + ' − 出库 ' + u
      + '」应为 ' + expect + '（差 ' + (b - expect) + '）',
    rec.raw, '先确认口径：如果有调拨、退货、报损，请把它们也列成一列再核。');
}

function checkDiffQty(rec) {
  const b = normAmount(rec.byRole.bookQty);
  const a = normAmount(rec.byRole.actualQty);
  const d = normAmount(rec.byRole.diffQty);
  if (b === null || a === null || d === null) return null;
  const expect = Math.round((b - a) * 100) / 100;
  if (Math.abs(expect - d) <= 0.005) return null;
  return finding('P0', '差异数量算错', rec.line,
    tag(rec) + ' 的差异数量是 ' + d + '，但「账面结存 ' + b + ' − 实盘 ' + a + '」应为 '
      + expect + '（差 ' + (d - expect) + '）',
    rec.raw, '差异数量是盘盈盘亏的原始依据，算错会直接带错账务处理。');
}

function checkDiffAmount(rec) {
  const d = normAmount(rec.byRole.diffQty);
  const p = normAmount(rec.byRole.price);
  const amt = normAmount(rec.byRole.diffAmount);
  if (d === null || p === null || amt === null) return null;
  const expect = Math.round(d * p * 100) / 100;
  if (Math.abs(expect - amt) <= 0.01) return null;
  return finding('P0', '差异金额不等于差异数量×单价', rec.line,
    tag(rec) + ' 的差异金额是 ' + amt.toFixed(2) + '，但「差异数量 ' + d + ' × 单价 '
      + p.toFixed(2) + '」应为 ' + expect.toFixed(2) + '（差 ' + (amt - expect).toFixed(2) + '）',
    rec.raw, '差异金额决定盘盈盘亏的入账金额，必须与数量、单价对得上。');
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals.length) return out;
  const t = totals[0];
  for (const role of QTY_ROLES.concat(['diffAmount'])) {
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
      '合计行的「' + labelOf(role) + '」写的是 ' + claimed + '，但各品类相加是 ' + sum
        + '（差 ' + Math.round((claimed - sum) * 100) / 100 + '）',
      t.raw, '合计行常是从系统导出后手工改过，改了一处忘了另一处。'));
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.code || it.byRole.name || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push(finding('P0', '同一品类出现两行', it.line,
        key + ' 出现了两次（上一次在第 ' + seen.get(key) + ' 行）',
        it.raw, '同一品类两行会让盘点差异重复计算，请先合并。'));
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  const roles = Object.keys(items[0] ? items[0].byRole : {})
    .filter((r) => r !== 'name' && r !== 'code');
  for (const it of items) {
    if (!String(it.byRole.code || it.byRole.name || '').trim()) {
      out.push(finding('P0', '品类无编码也无名称', it.line, '这一行认不出是哪个品类', it.raw,
        '请确认这一行是否有效。'));
      continue;
    }
    for (const r of roles) {
      const v = it.byRole[r];
      if (isBlank(v)) {
        out.push(finding('P1', '该填没填', it.line,
          tag(it) + ' 的「' + labelOf(r) + '」是空的或还是占位符（' + (String(v).trim() || '空') + '）',
          it.raw, '盘点表出现空列，通常是从系统导出时漏选，或模板没替换。'));
      } else if (normAmount(v) === null) {
        out.push(finding('P1', '数值无法解析', it.line,
          tag(it) + ' 的「' + labelOf(r) + '」写作「' + String(v).trim() + '」，不是能计算的数值',
          it.raw, '请确认列是否串位。'));
      }
    }
  }
  return out;
}

function checkNegative(rec) {
  const out = [];
  for (const pair of [['bookQty', '账面结存'], ['actualQty', '实盘数量']]) {
    const n = normAmount(rec.byRole[pair[0]]);
    if (n === null || n >= 0) continue;
    out.push(finding('P0', '数量为负', rec.line,
      tag(rec) + ' 的' + pair[1] + '是 ' + n + '（负数）',
      rec.raw, '库存数量不可能为负；通常是出入库方向录反了，或期初本身是错的。'));
  }
  return out;
}

function checkInboundAmount(rec) {
  const i = normAmount(rec.byRole.inQty);
  const p = normAmount(rec.byRole.price);
  if (i === null || p === null) return null;
  // 只有同时给了「入库金额」列时才核；这里用差异金额反推不成立，故仅在存在该列时检查
  const amt = normAmount(rec.byRole.inAmount);
  if (amt === null) return null;
  const expect = Math.round(i * p * 100) / 100;
  if (Math.abs(expect - amt) <= 0.01) return null;
  return finding('P1', '入库金额不等于入库数量×单价', rec.line,
    tag(rec) + ' 的入库金额是 ' + amt.toFixed(2) + '，但「入库数量 ' + i + ' × 单价 ' + p.toFixed(2)
      + '」应为 ' + expect.toFixed(2),
    rec.raw, '请确认是否用了不同批次的成本价。');
}

function checkStagnant(rec) {
  const o = normAmount(rec.byRole.opening);
  const b = normAmount(rec.byRole.bookQty);
  const i = normAmount(rec.byRole.inQty);
  const u = normAmount(rec.byRole.outQty);
  if (o === null || b === null || i === null || u === null) return null;
  if (i !== 0 || u !== 0) return null;
  if (o <= 0) return null;
  return finding('P1', '本期无出入库（长期挂账存货）', rec.line,
    tag(rec) + ' 期初 ' + o + '、期末 ' + b + '，本期入库与出库都是 0',
    rec.raw, '长期不动的存货可能已减值或已报废，值得单独看一次。');
}

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。',
  };
}

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['盘点表原文（text）']);
  const t = parseTable(text);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的盘点表（要能认出「品类/品名」+ 至少三个数量列，例如「期初」「入库」「出库」「账面结存」）',
      '从系统导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个品类的明细行']);

  const paid = Boolean(payload && (payload.full || payload.credit || payload.token));
  const threshold = payload && typeof payload.diffRatio === 'number' ? payload.diffRatio : DIFF_RATIO_THRESHOLD;

  const findings = [];
  const notRun = [];
  for (const it of t.items) {
    const a = checkBook(it); if (a) findings.push(a);
    const b = checkDiffQty(it); if (b) findings.push(b);
    const c = checkDiffAmount(it); if (c) findings.push(c);
    if (paid) {
      for (const f of checkNegative(it)) findings.push(f);
      const ia = checkInboundAmount(it); if (ia) findings.push(ia);
      const st = checkStagnant(it); if (st) findings.push(st);
    }
  }
  for (const f of checkTotalRow(t.totals, t.items)) findings.push(f);
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const sumOf = (role) => Math.round(t.items.reduce((s, it) => {
    const n = normAmount(it.byRole[role]);
    return s + (n === null ? 0 : n);
  }, 0) * 100) / 100;
  const bookAmt = t.items.reduce((s, it) => {
    const b = normAmount(it.byRole.bookQty);
    const p = normAmount(it.byRole.price);
    return s + ((b === null || p === null) ? 0 : b * p);
  }, 0);
  const diffAmt = sumOf('diffAmount');
  const ratio = bookAmt > 0 ? Math.abs(diffAmt) / bookAmt : 0;

  if (paid && ratio > threshold + 1e-9) {
    findings.push(finding('P1', '盘点差异率超阈值', 0,
      '差异金额合计 ' + diffAmt.toFixed(2) + '，占账面金额 ' + bookAmt.toFixed(2) + ' 的 '
        + (ratio * 100).toFixed(2) + '%，超过阈值 ' + (threshold * 100).toFixed(0) + '%',
      '', '这是提示不是错误；差异率偏高通常说明收发存流程或账务处理有问题，值得查一次原因。'));
  }
  if (!paid) notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));

  const result = {
    findings,
    summary: {
      items: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      diff_amount_total: diffAmt,
      diff_ratio: Math.round(ratio * 10000) / 10000,
      basis: '逐品「期初+入库−出库=账面结存」「账面−实盘=差异数量」「差异数量×单价=差异金额」比对',
    },
    columns: t.cols,
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明这张表**算得对**，'
      + '不代表实物真的数对了、也不代表差异该不该报损 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normAmount, isBlank, labelOf,
  CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT,
  ROLE_LABELS, QTY_ROLES, DIFF_RATIO_THRESHOLD,
};
