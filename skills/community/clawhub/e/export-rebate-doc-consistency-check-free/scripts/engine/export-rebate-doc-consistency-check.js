/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * export-rebate-doc-consistency-check.js —— 出口退税申报单证一致性核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每一票出口退税申报之前**。外贸企业（免退税）与生产企业
 * （免抵退）都要把同一票货的几张单证摆在一起逐笔对：报关单、出口发票、收汇水单、
 * 进项发票、申报表。金额与数量只要有一笔对不上，函调就会来，退税款就卡住 ——
 * 而函调要翻的单证，本来就是这张表里已经填好的东西，先自己核一遍最便宜。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   差额     = 报关金额 − 发票金额              （同一票货的两张单证应当一致，差额只是尾差）
 *   应退税额 = 计税金额（购进金额）× 退税率      （外贸企业免退税的核心算式）
 *   合计行各列 = 明细行相加
 *   同一报关单号：同一所属期里同源行重复 = 粘重；横跨两个所属期 = 重复申报
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**这一票该不该退税、该按哪个版本的出口退税率文库、免抵退的"不得免征和
 *    抵扣税额"怎么算（那属于税法与申报口径判断）：表里的报关金额、发票金额、计税金额、
 *    退税率一律**以你填的为准**，本工具只核表内勾稽，并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的条件块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '报关金额与发票金额差额复算（报关金额 − 发票金额 = 差额）',
  '应退税额复算（计税金额 × 退税率 = 应退税额）',
  '合计行逐列复核',
  '同一报关单号重复行检测',
  '空白与占位符检测',
  '金额或数量为负检测',
];

const CHECKS_WITHHELD = [
  '报关金额与发票金额不符超容差提示（两张单证本身对不上，超过尾差容差才报）',
  '收汇金额与报关金额不符提示',
  '退税率与商品编码适用税率不一致提示',
  '进项发票金额不足（小于应退税额对应进项）提示',
  '同一报关单重复申报提示（同一报关单号横跨两个所属期）',
];

const OUT_OF_SCOPE = [
  '判断这一票货该不该退税、能不能退税（出口货物是否属于退税范围、是否已申报过、是否被列入不予退税情形，属于税法判断，请咨询税务师）',
  '判断该商品编码应当适用哪个退税率（出口退税率文库的版本、商品编码归类与外购/自产口径，属于归类与税法判断）',
  '生产企业免抵退的"不得免征和抵扣税额""免抵退税额抵减额"与期末留抵的分配计算',
  '处理关税、增值税、消费税、汇率折算与免抵退税申报表的表间关系',
  '读取电子税务局 / 单一窗口 / ERP / 报关行系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  ['所属期', '报关单号', '出口发票号', '商品编码', '出口数量', '报关金额', '发票金额', '差额',
    '计税金额', '退税率', '商品编码适用退税率', '应退税额', '收汇金额', '进项发票金额'].join('\t'),
  ['2026-01', 'BG-2026-0101', 'FP-2026-0001', '8528721000', '1000', '600000.00', '600000.00', '0.00',
    '600000.00', '13%', '13%', '78000.00', '600000.00', '600000.00'].join('\t'),
  ['2026-01', 'BG-2026-0102', 'FP-2026-0002', '9013803000', '200', '300000.00', '300000.00', '0.00',
    '300000.00', '9%', '9%', '27000.00', '300000.00', '300000.00'].join('\t'),
  ['2026-02', 'BG-2026-0201', 'FP-2026-0003', '6109100021', '5000', '250000.00', '250000.00', '0.00',
    '250000.00', '13%', '13%', '32500.00', '250000.00', '250000.00'].join('\t'),
  ['2026-02', 'BG-2026-0202', 'FP-2026-0004', '8471300000', '300', '900000.00', '900000.00', '0.00',
    '900000.00', '13%', '13%', '117000.00', '900000.00', '900000.00'].join('\t'),
  ['2026-03', 'BG-2026-0301', 'FP-2026-0005', '9403600000', '150', '450000.00', '450000.00', '0.00',
    '450000.00', '9%', '9%', '40500.00', '450000.00', '450000.00'].join('\t'),
  ['2026-03', 'BG-2026-0302', 'FP-2026-0006', '3926909090', '8000', '120000.00', '120000.00', '0.00',
    '120000.00', '13%', '13%', '15600.00', '120000.00', '120000.00'].join('\t'),
  ['合计', '', '', '', '14650', '2620000.00', '2620000.00', '0.00', '2620000.00', '', '',
    '310600.00', '2620000.00', '2620000.00'].join('\t'),
].join('\n');

const TOL = 0.01;             // 表内各列复算的容差（分）
const DOC_TOL = 1.00;         // 两张单证之间的尾差容差（元）：汇率折算与四舍五入的尾差
const RATE_TOL = 0.0005;      // 退税率容差：0.05 个百分点

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前。
  //    「商品编码适用退税率」不能被「商品编码」或「退税率」抢走、「进项发票金额」不能被
  //    「发票金额」抢走、「应退税额」不能被「退税额」抢走 —— 顺序错一列就静默不参与核对。
  period: ['申报所属期', '退税所属期', '所属期', '所属月份', '所属期间', '期间', '月份'],
  hsRate: ['商品编码适用退税率', '商品编码适用税率', '编码适用退税率', '适用退税率', '文库退税率', '退税率文库', '适用税率'],
  hsCode: ['商品编码', 'HS编码', 'hs编码', '海关编码', '税则号列', '商品编号'],
  declarationNo: ['海关报关单号', '报关单编号', '报关单号', '报关单', '核销单号'],
  invoiceNo: ['出口发票号码', '出口发票编号', '出口发票号', '外销发票号', '发票号码', '发票号'],
  qty: ['出口数量', '申报出口数量', '出口商品数量', '成交数量', '数量'],
  customsAmount: ['出口报关金额', '报关单金额', '报关金额', '海关金额', '成交总价', '报关总金额'],
  inputAmount: ['进项发票金额', '采购发票金额', '增值税专用发票金额', '进项发票计税金额', '进项金额', '进项税额'],
  invoiceAmount: ['出口发票金额', '外销发票金额', '发票总金额', '发票金额'],
  diffAmount: ['报关与发票差额', '单证差额', '金额差额', '差额', '差异额'],
  taxBase: ['出口货物计税金额', '退税计税金额', '计税金额', '购进金额', '计税价格'],
  rebateRate: ['出口退税率', '申报退税率', '退税比例', '退税率'],
  rebateAmount: ['应退税额', '可退税额', '退税金额', '退税额'],
  receiptAmount: ['已收汇金额', '外汇收汇金额', '实际收汇金额', '收汇金额', '收汇额'],
};

const LABELS = {
  period: '所属期', declarationNo: '报关单号', invoiceNo: '出口发票号', hsCode: '商品编码',
  qty: '出口数量', customsAmount: '报关金额', invoiceAmount: '发票金额', diffAmount: '差额',
  taxBase: '计税金额', rebateRate: '退税率', hsRate: '商品编码适用退税率',
  rebateAmount: '应退税额', receiptAmount: '收汇金额', inputAmount: '进项发票金额',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'declarationNo', 'invoiceNo', 'hsCode', 'qty', 'customsAmount',
  'invoiceAmount', 'diffAmount', 'taxBase', 'rebateRate', 'hsRate', 'rebateAmount',
  'receiptAmount', 'inputAmount'];
/** 合计行逐列复核的列（税率列不可加总，单号列不可加总） */
const SUM_ROLES = ['qty', 'customsAmount', 'invoiceAmount', 'diffAmount', 'taxBase',
  'rebateAmount', 'receiptAmount', 'inputAmount'];
/**
 * 免费档负值检测覆盖的列：**各单证的金额与数量**。
 * ⚠️ 刻意**不含**差额列（报关少于发票时差额天然为负）也**不含**适用税率列 ——
 *    "报关金额与发票金额不符超容差"是完整档的独立检查项（见 CHECKS_WITHHELD），
 *    免费档提前报出负差额就等于把付费结论送出去了。
 */
const NEGATIVE_ROLES = ['qty', 'customsAmount', 'invoiceAmount', 'taxBase', 'rebateRate',
  'rebateAmount', 'receiptAmount', 'inputAmount'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|合计：|汇总)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|空)$/i.test(s);
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

/** 退税率归一化成小数：`13%` ⇒ 0.13；`0.13` ⇒ 0.13；`13` ⇒ 0.13 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
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
      if (role === 'period' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const p = it && it.period !== undefined && String(it.period).trim() !== ''
    ? String(it.period).trim() : `第 ${it && it.line} 行`;
  const n = [it && it.declarationNo, it && it.invoiceNo]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

const declarationKeyOf = (it) => {
  const d = it && it.declarationNo !== undefined ? String(it.declarationNo).trim() : '';
  return d || `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkDiffRecompute(it) {
  const out = [];
  const customs = normNumber(it.customsAmount);
  const invoice = normNumber(it.invoiceAmount);
  const stated = normNumber(it.diffAmount);
  if (customs === null || invoice === null || stated === null) return out;
  const expect = round2(customs - invoice);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '差额复算不符', line: it.line,
    message: `${who(it)}：报关金额 ${customs.toFixed(2)} − 发票金额 ${invoice.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「差额」填的是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '差额列是"报关单与出口发票对不对得上"的第一行证据：这一格填错，'
      + '函调时两张单证摆在一起就说不清差额是怎么来的。',
  });
  return out;
}

function checkRebateRecompute(it) {
  const out = [];
  const base = normNumber(it.taxBase);
  const rate = rateValue(it.rebateRate);
  const stated = normNumber(it.rebateAmount);
  if (base === null || rate === null || stated === null) return out;
  const expect = round2(base * rate);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '应退税额复算不符', line: it.line,
    message: `${who(it)}：计税金额 ${base.toFixed(2)} × 退税率 ${(rate * 100).toFixed(2)}% = ${expect.toFixed(2)}，`
      + `表里「应退税额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '外贸企业免退税就是"购进（计税）金额 × 退税率"：算多了会被追回并加收滞纳金，'
      + '算少了是自己的钱没拿回来。',
  });
  return out;
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals || !totals.row) return out;
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let sum = 0;
    let n = 0;
    for (const it of items) {
      const v = normNumber(it[role]);
      if (v !== null) { sum += v; n += 1; }
    }
    if (!n) continue;
    const expect = round2(sum);
    if (Math.abs(stated - expect) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，本表 ${n} 行明细的`
        + `「${LABELS[role]}」相加是 ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
        + '申报表的取数口径就是这张表的合计行：合计是手打或从别处粘来的，明细改了它没跟着改，'
        + '报上去的表与附送单证就对不上。',
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined ? String(it.period).trim() : '';
    const d = it.declarationNo !== undefined ? String(it.declarationNo).trim() : '';
    const v = it.invoiceNo !== undefined ? String(it.invoiceNo).trim() : '';
    if (!p || !d) continue;
    const key = `${p}|${d}|${v}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一报关单重复行', line: it.line,
        message: `${who(it)}与第 ${seen.get(key)} 行完全同源（同一所属期、同一报关单号、同一出口发票号）—— `
          + '要么是重复粘贴了一行，要么是同一票货被拆成两行登记。'
          + '多出来的那一行会把报关金额、应退税额与收汇都重复计一遍，退税额当场虚增。',
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
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`
            + '这一列缺失时对应的复算做不了：缺哪一列就补哪一列，别让空值静默跳过检查。',
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = role === 'rebateRate' ? rateValue(it[role]) : normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    const shown = role === 'rebateRate' ? `${(v * 100).toFixed(4)}%` : v.toFixed(2);
    out.push({
      level: 'P0', category: '金额或数量为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${shown}（负数）—— 出口数量、报关金额、发票金额、`
        + '计税金额、应退税额、收汇金额与进项发票金额都不该为负；'
        + '红字冲回或退货应单独列示并在备注里说明，不要与正数行混在一张表里。',
    });
  }
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
    return insufficient('没有收到出口退税申报单证一致性核对表正文（text）—— 请把「所属期 / 报关单号 / 出口发票号 / 商品编码 / 出口数量 / 报关金额 / 发票金额 / 差额 / 计税金额 / 退税率 / 商品编码适用退税率 / 应退税额 / 收汇金额 / 进项发票金额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `出口退税申报单证一致性核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何单证明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkDiffRecompute(it));
    findings.push(...checkRebateRecompute(it));
    findings.push(...checkNegative(it));

  }

  findings.push(...checkTotalRow(t.totals, t.items));
  findings.push(...checkDuplicates(t.items));
  findings.push(...checkBlanks(t.items));

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let customsTotal = 0;
  let rebateTotal = 0;
  let receiptTotal = 0;
  const declarations = new Set();
  for (const it of t.items) {
    const c = normNumber(it.customsAmount);
    if (c !== null) customsTotal += c;
    const r = normNumber(it.rebateAmount);
    if (r !== null) rebateTotal += r;
    const v = normNumber(it.receiptAmount);
    if (v !== null) receiptTotal += v;
    const d = it.declarationNo === undefined ? '' : String(it.declarationNo).trim();
    if (d) declarations.add(d);
  }

  const result = {
    status: 'success',
    service_type: 'EXPORT_REBATE_DOC_CONSISTENCY_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      declarations: declarations.size,
      totals_row: Boolean(t.totals && t.totals.row),
      customs_total: round2(customsTotal),
      rebate_total: round2(rebateTotal),
      receipt_total: round2(receiptTotal),
      tolerance: TOL,
      doc_tolerance: DOC_TOL,
      rate_tolerance: RATE_TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: groups.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"报关金额 − 发票金额 = 差额""计税金额 × 退税率 = 应退税额"与"合计行 = 明细之和"'
      + '这类**表内勾稽**与档位提示，**不判断这一票该不该退税、适用退税率文库的版本、'
      + '免抵退的不得免征和抵扣税额怎么算**（以税法与主管税务机关口径为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
