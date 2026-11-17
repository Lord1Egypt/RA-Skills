'use strict';
/**
 * bid-comparison.js —— 多家报价横向比价（清标辅助）本地引擎
 *
 * 与本仓库相邻能力的区别（这是不同产品，不要混淆）：
 *   · quote-audit / batch-bid-checkup：**单家**报价自己的算术与合规；
 *   · cross-bid-collusion：找**串通**线索（联系方式一致、文本雷同…）；
 *   · 本引擎：把**多家**的报价明细**逐项摆在一起**做横向对比 ——
 *     谁缺项、谁多项、谁的单价明显离群、有没有不平衡报价的结构特征。
 *     这是评标里"清标"那一步的规则部分。
 *
 * 设计原则（与本仓库其它引擎一致）：
 *   · 自包含：只用 Node.js 标准库，**不发起任何网络请求**；
 *   · 每条结论都给出可复算的依据（具体项目名、各家数值、中位数）；
 *   · 材料不足时返回 insufficient_input 并说明缺什么，**绝不输出"未发现问题"**；
 *   · 只做AI对比，**不判断哪家该中标**（那是评标委员会的事），
 *     也**不认定串通**（那需要证据与法定程序）。
 */

const CHECKS_GIVEN = [
  '逐项对照表（按项目名对齐各家的数量 / 单价 / 合价）',
  '缺项与多项（某家有、别家没有的项目）',
  '各家合价合计与排序',
];

const CHECKS_WITHHELD = [
  '单价离群检测（某项单价与各家中位数的偏离超过阈值）',
  '不平衡报价线索（同一家内单价偏离方向不一致）',
  '合价 = 数量 × 单价 的算术核对',
  '数量在各家之间不一致的提示',
  '最高限价与各家合计的对比（需提供 maxPrice）',
];

/* ---------------------------------------------------------------- 工具 */

function finding(level, category, line, message, advice, evidence) {
  return { level, category, line, message, advice, evidence };
}

function normNumber(s) {
  const t = String(s == null ? '' : s)
    .replace(/[,，\s\u00A0]/g, '').replace(/^[¥￥$€£]/, '')
    .replace(/(元|万元|人民币|cny|rmb)$/i, '');
  if (!/^\d+(\.\d+)?$/.test(t)) return null;
  return Math.round(parseFloat(t) * 100) / 100;
}
function numOf(s) { const n = normNumber(s); return n === null ? null : n; }

/** 项目名归一：用于跨家对齐（去空白、标点、大小写、单位后缀差异） */
function normItemName(s) {
  return String(s == null ? '' : s)
    .replace(/[\s\u00A0]+/g, '')
    .replace(/[。．.,，;；:：、"“”‘’()（）]/g, '')
    .replace(/(m3|m2|m³|m²|t|kg|项|个|台|套|米|吨)$/i, '')
    .toUpperCase();
}

/**
 * 解析文本形式的报价明细。
 * 支持行形如：「序号 项目名称 单位 数量 单价 合价」，分隔符 Tab / 竖线 / 逗号 / 多空格。
 * 返回 [{name, unit, qty, price, amount, line}]。
 */
function parseItemsFromText(text) {
  const out = [];
  String(text == null ? '' : text).split(/\r?\n/).forEach((raw, idx) => {
    const line = raw.trim();
    if (!line) return;
    if (/^\|?\s*[-:|\s]+$/.test(line)) return;                 // 表格分隔行
    // 分隔符：Tab / 竖线 / 逗号 / 分号 / **任意空白**（单空格也算 —— 从 Excel 或网页复制常是单空格）
    const tokens = line.split(/[\t|,，;；]+|\s+/).map((c) => c.trim()).filter(Boolean);
    if (tokens.length < 3) return;
    if (/^(序号|项目名称|名称|unit|qty|price|amount)$/i.test(tokens[0])) return;   // 表头
    // 找出所有「数字」token，取最后 2~3 个当数量/单价/合价
    const numericIdx = tokens.map((c, i) => ({ i, v: numOf(c) })).filter((x) => x.v !== null);
    if (numericIdx.length < 2) return;
    const tail = numericIdx.slice(-3);
    let qty = null, price = null, amount = null, firstNum = tail[0].i;
    if (tail.length >= 3) { qty = tail[0].v; price = tail[1].v; amount = tail[2].v; }
    else { price = tail[0].v; amount = tail[1].v; }
    // 项目名 = 第一个数字之前的所有 token（这样「C30 混凝土」这类含数字的名字尽量保留）
    let nameEnd = firstNum;
    if (tail.length >= 3 && firstNum > 0 && numOf(tokens[firstNum - 1]) === null) nameEnd = firstNum;
    let nameTokens = tokens.slice(0, Math.max(1, nameEnd));
    // 行首的纯序号（「1」「1.」「1、」「(1)」）不是项目名的一部分，去掉
    if (nameTokens.length > 1 && /^\(?\d+[.、)]?$/.test(nameTokens[0])) nameTokens = nameTokens.slice(1);
    const name = nameTokens.join(' ').trim();
    if (!name) return;
    out.push({ name: name.slice(0, 40), unit: null, qty, price, amount, line: idx + 1, raw: line });
  });
  return out;
}

/** 收集材料：bidders 数组（推荐）或 text（空行分隔各家） */
function collectBidders(payload) {
  const p = payload && typeof payload === 'object' ? payload : {};
  const out = [];
  if (Array.isArray(p.bidders)) {
    p.bidders.forEach((b, i) => {
      if (!b) return;
      const name = String(b.name || b.bidder || ('投标人 ' + (i + 1))).slice(0, 40);
      let items = Array.isArray(b.items) ? b.items
        .filter((it) => it && (it.name || it.item))
        .map((it) => ({
          name: String(it.name || it.item).slice(0, 40),
          unit: it.unit ? String(it.unit).slice(0, 8) : null,
          qty: numOf(it.qty != null ? it.qty : it.quantity),
          price: numOf(it.price != null ? it.price : it.unitPrice),
          amount: numOf(it.amount != null ? it.amount : it.total),
          line: 0, raw: `${it.name || it.item} ${it.qty || ''} ${it.price || ''} ${it.amount || ''}`.trim(),
        })) : [];
      const text = typeof b.text === 'string' ? b.text : (typeof b === 'string' ? b : '');
      if (!items.length && text.trim()) items = parseItemsFromText(text);
      if (!items.length) return;
      const total = numOf(b.total != null ? b.total : b.totalAmount);
      out.push({ name, items, total });
    });
  } else if (typeof p.text === 'string' && p.text.trim()) {
    const blocks = p.text.split(/\n[ \t]*\n+/).map((x) => x.trim()).filter(Boolean);
    blocks.forEach((b, i) => {
      const first = (b.split('\n')[0] || '').trim().slice(0, 40);
      const items = parseItemsFromText(b);
      if (items.length) out.push({ name: first || ('投标人 ' + (i + 1)), items, total: null });
    });
  }
  return out;
}

/* ------------------------------------------------------------ 各项检查 */

function median(arr) {
  if (!arr.length) return null;
  const s = arr.slice().sort((a, b) => a - b);
  const mid = Math.floor(s.length / 2);
  return s.length % 2 ? s[mid] : (s[mid - 1] + s[mid]) / 2;
}
function fmt(n) { return n === null || n === undefined ? '—' : n.toFixed(2); }

/** 构建逐项对照表 */
function buildMatrix(bidders) {
  const rows = new Map();     // normName → { display, byBidder: {bidderName: {qty, price, amount, raw}} }
  bidders.forEach((b) => {
    b.items.forEach((it) => {
      const k = normItemName(it.name);
      if (!k) return;
      if (!rows.has(k)) rows.set(k, { display: it.name, byBidder: {} });
      const row = rows.get(k);
      if (!row.byBidder[b.name]) row.byBidder[b.name] = it;
    });
  });
  return rows;
}

/** 1. 缺项与多项 */
function checkMissingItems(bidders, rows) {
  const out = [];
  const names = bidders.map((b) => b.name);
  rows.forEach((row) => {
    const have = names.filter((n) => row.byBidder[n]);
    if (have.length === names.length) return;
    const missing = names.filter((n) => !row.byBidder[n]);
    out.push(finding('P1', '缺项', 0,
      `项目「${row.display}」只有 ${have.length}/${names.length} 家报了：缺的是 ${missing.join('、')}。`,
      '清标时要逐项确认：是真的没报，还是项目名称写法不同导致对不上。',
      have.map((n) => `${n}: ${row.byBidder[n].raw}`).slice(0, 4)));
  });
  return out;
}











/* -------------------------------------------------------------- 主流程 */

function analyze(bidders, opts) {
  const rows = buildMatrix(bidders);
  const findings = [
    ...checkMissingItems(bidders, rows),
  ];
  const summary = { p0: 0, p1: 0, p2: 0 };
  const byCategory = {};
  findings.forEach((f) => {
    const k = f.level === 'P0' ? 'p0' : (f.level === 'P1' ? 'p1' : 'p2');
    summary[k]++;
    byCategory[f.category] = (byCategory[f.category] || 0) + 1;
  });
  summary.total = findings.length;
  summary.by_category = byCategory;
  summary.verdict = summary.p0 > 0
    ? '发现必须处理的硬错误（P0）'
    : (summary.p1 > 0 ? '没有 P0，但有需要人工核对的项（P1）'
      : (summary.p2 > 0 ? '只有提示性预警（P2），没有硬错误'
        : '在上述检查项范围内没有发现问题 —— 这不等于没有问题'));

  // 逐项对照表 + 各家合计与排序（这是本产品的主产出，不只是一堆问题）
  const table = [...rows.values()].map((row) => ({
    item: row.display,
    prices: Object.fromEntries(Object.entries(row.byBidder).map(([n, it]) => [n, it.price])),
    qty: Object.fromEntries(Object.entries(row.byBidder).map(([n, it]) => [n, it.qty])),
    median_price: median(Object.values(row.byBidder).map((it) => it.price).filter((x) => x !== null && x > 0)),
  }));
  const totals = bidders.map((b) => ({
    name: b.name,
    total: b.total !== null && b.total !== undefined
      ? b.total
      : Math.round(b.items.reduce((n, it) => n + (it.amount || 0), 0) * 100) / 100,
    items: b.items.length,
  })).sort((a, b) => a.total - b.total);
  totals.forEach((t, i) => { t.rank = i + 1; });

  return { findings, summary, comparison: table, totals, bidderCount: bidders.length, itemCount: rows.size };
}

function insufficient(missing, advice) {
  return { status: 'insufficient_input', missing: [].concat(missing), advice };
}

/**
 * @param {Object} payload { bidders:[{name,items:[{name,qty,price,amount}]}], maxPrice?, outlierPct? } 或 { text }
 */
function run(payload) {
  const bidders = collectBidders(payload);
  if (bidders.length < 2) {
    return insufficient(
      [bidders.length === 0 ? '没有收到任何报价明细' : `只收到 ${bidders.length} 家报价`],
      '横向比价至少需要两家。请用 bidders 数组提供各家的 items（形如 {"name":"甲","items":[{"name":"钢筋","qty":100,"price":10,"amount":1000}]}），'
      + '或用 text、各家之间空一行、行格式为「项目名称 数量 单价 合价」。');
  }
  const itemCount = bidders.reduce((n, b) => n + b.items.length, 0);
  if (itemCount < 2) {
    return insufficient([`解析到的报价明细只有 ${itemCount} 条`],
      '请确认每家的明细里至少有「项目名称 + 至少两个数字（数量/单价/合价）」，例如「钢筋 100 10 1000」。');
  }
  const opts = {
    outlierPct: payload && Number.isFinite(payload.outlierPct) ? payload.outlierPct : undefined,
    maxPrice: payload && Number.isFinite(payload.maxPrice) ? payload.maxPrice : undefined,
    minBiddersForOutlier: payload && Number.isFinite(payload.minBiddersForOutlier) ? payload.minBiddersForOutlier : undefined,
  };
  const result = analyze(bidders, opts);
  result.scope = { given: CHECKS_GIVEN.slice(), withheld: CHECKS_WITHHELD.slice() };
  result.bidders = bidders.map((b) => ({ name: b.name, items: b.items.length }));
  return { status: 'success', result: result };
}

module.exports = {
  run,
  analyze,
  collectBidders,
  parseItemsFromText,
  buildMatrix,
  normItemName,
  normNumber,
  CHECKS_GIVEN,
  CHECKS_WITHHELD,
  SAMPLE_BIDDERS: [
    { name: '河南甲建设有限公司', items: [
      { name: '土方开挖', qty: 100, price: 25, amount: 2500 },
      { name: '路基填筑', qty: 200, price: 38, amount: 7600 },
      { name: '沥青面层', qty: 500, price: 120, amount: 60000 },
      { name: '排水管道', qty: 300, price: 85, amount: 25500 },
    ] },
    { name: '河南乙工程有限公司', items: [
      { name: '土方开挖', qty: 100, price: 26, amount: 2600 },
      { name: '路基填筑', qty: 200, price: 39, amount: 7800 },
      { name: '沥青面层', qty: 500, price: 122, amount: 61000 },
    ] },
  ],
};
