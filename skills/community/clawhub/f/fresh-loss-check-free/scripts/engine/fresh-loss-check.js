/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * fresh-loss-check.js —— 生鲜损耗与盘点差异核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**超市 / 生鲜门店每天或每周盘点时**，店长与财务要拿
 * 「生鲜损耗与盘点表」核一遍。某品类的损耗率突然变高，往往意味着**陈列方式不对、
 * 报损没及时登记、称重有偏差或内盗** —— 这些直接吃掉毛利，而且**表里的数字是能自己算出来的**：
 *
 *   损耗量 = 进货量 + 期初库存 − 销售量 − 期末库存
 *   损耗率 = 损耗量 ÷ 进货量
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**损耗率多少算正常（品类、门店、季节差异都很大），
 *    只对"明显超出常见参考上限"做**提示**，并在结论里明确标注那是参考口径。
 */

const CHECKS_GIVEN = [
  '损耗量勾稽复算（进货量 + 期初库存 − 销售量 − 期末库存 = 损耗量）',
  '损耗率复算（损耗量 ÷ 进货量 = 损耗率）',
  '合计行逐列复核',
  '同一品类同一期间重复行检测',
  '空白与占位符检测',
  '数量为负检测',
];

const CHECKS_WITHHELD = [
  '损耗率超过参考上限（15%）提示（参考口径）',
  '期末库存为负检测',
  '销售量为零却有损耗提示',
  '进货金额与进货量不符（单价异常）检测',
  '损耗率与损耗量方向矛盾检测',
];

const OUT_OF_SCOPE = [
  '判定损耗率是否属于正常范围、报损是否合规、该不该计提报废损失（品类与门店差异大，请以本单位盘点与报损制度为准）',
  '区分陈列损耗、报损、称重误差与内盗（需要现场盘点、监控与称重记录，本工具只核对表内数字）',
  '核对生鲜成本结转与毛利额（需要进销存系统与成本核算资料）',
  '读取 POS / 进销存系统导出文件（需要你先导出成文本贴进来）',
];

/* 参考口径：仅供"明显超出"时提示，不是行业标准 */
const LOSS_RATE_REF = 0.15;              // 损耗率参考上限 15%
const UNIT_PRICE_REF = [0.2, 2000];      // 进货单价宽区间（元/单位）
const PRICE_DEVIATION_REF = 0.5;         // 同品类单价偏离中位数超过 50% ⇒ 提示
const TOL = 0.01;
const RATE_TOL = 0.02;                   // 损耗率按百分点比较，容忍两位小数四舍五入

const SAMPLE_TEXT = [
  '期间\t品类\t进货量\t进货金额\t期初库存\t销售量\t期末库存\t损耗量\t损耗率',
  '2026-06-01\t叶菜类\t1200.00\t3600.00\t150.00\t980.00\t210.00\t160.00\t13.33%',
  '2026-06-01\t水果类\t1000.00\t6000.00\t180.00\t820.00\t240.00\t120.00\t12.00%',
  '2026-06-02\t叶菜类\t1100.00\t3300.00\t210.00\t930.00\t250.00\t130.00\t11.82%',
  '2026-06-02\t水果类\t900.00\t5400.00\t240.00\t800.00\t240.00\t100.00\t11.11%',
  '合计\t\t4200.00\t18300.00\t780.00\t3530.00\t940.00\t510.00\t',
].join('\n');

const ROLES = {
  // ⚠️ 顺序即优先级：**更具体的词必须排在更宽泛的词前面**
  //    （「损耗率」不能被「损耗量」这类同族词抢走，「期末库存」不能被「期初」抢走）
  period: ['期间', '盘点日期', '营业日', '日期', '所属期', '月份', '周次'],
  category: ['品类', '类别', '品名', '商品名称', '商品'],
  purchaseQty: ['进货量', '进货数量', '采购量', '到货量', '入库量'],
  purchaseAmt: ['进货金额', '采购金额', '进货额', '金额'],
  openingQty: ['期初库存', '期初结存', '期初数量', '期初'],
  salesQty: ['销售量', '销售数量', '销量', '销售'],
  closingQty: ['期末库存', '期末结存', '期末数量', '期末'],
  lossRate: ['损耗率', '报损率', '损耗比例'],
  lossQty: ['损耗量', '损耗数量', '报损量', '损耗'],
};

const LABELS = {
  period: '期间', category: '品类', purchaseQty: '进货量', purchaseAmt: '进货金额',
  openingQty: '期初库存', salesQty: '销售量', closingQty: '期末库存',
  lossQty: '损耗量', lossRate: '损耗率',
};

const REQUIRED = ['period', 'category', 'purchaseQty', 'openingQty', 'salesQty',
  'closingQty', 'lossQty', 'lossRate'];
const SUM_ROLES = ['purchaseQty', 'purchaseAmt', 'openingQty', 'salesQty', 'closingQty', 'lossQty'];
const NEGATIVE_ROLES = ['purchaseQty', 'openingQty', 'salesQty', 'lossQty'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|全月合计)$/;

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

/** 比率归一化成**百分点数值**：`13.33%` ⇒ 13.33；`0.1333` ⇒ 13.33；`13.33` ⇒ 13.33 */
function ratePct(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n;
  return Math.abs(n) <= 1 ? n * 100 : n;
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
  const p = it && it.period ? `${String(it.period).trim()}` : `第 ${it && it.line} 行`;
  const c = it && it.category ? ` ${String(it.category).trim()}` : '';
  return `${p}${c}`;
};

/* ================================ 免费档检查项 ================================ */

function checkLossFormula(it) {
  const qty = normNumber(it.purchaseQty);
  const open = normNumber(it.openingQty);
  const sale = normNumber(it.salesQty);
  const close = normNumber(it.closingQty);
  const loss = normNumber(it.lossQty);
  if (qty === null || open === null || sale === null || close === null || loss === null) return null;
  const expect = round2(qty + open - sale - close);
  if (Math.abs(expect - loss) <= TOL) return null;
  return {
    level: 'P0', category: '损耗量复算不符', line: it.line,
    message: `${who(it)}：进货量 ${qty.toFixed(2)} + 期初库存 ${open.toFixed(2)} − 销售量 ${sale.toFixed(2)} `
      + `− 期末库存 ${close.toFixed(2)} = ${expect.toFixed(2)}，但表里损耗量是 ${loss.toFixed(2)}，`
      + `相差 ${round2(loss - expect).toFixed(2)} —— 这一行说明盘点的进销存没有闭合。`,
  };
}

function checkLossRate(it) {
  const qty = normNumber(it.purchaseQty);
  const loss = normNumber(it.lossQty);
  const rate = ratePct(it.lossRate);
  if (qty === null || loss === null || rate === null || qty <= TOL) return null;
  const expect = round2((loss / qty) * 100);
  if (Math.abs(expect - rate) <= RATE_TOL) return null;
  return {
    level: 'P0', category: '损耗率复算不符', line: it.line,
    message: `${who(it)}：损耗量 ${loss.toFixed(2)} ÷ 进货量 ${qty.toFixed(2)} = ${expect.toFixed(2)}%，`
      + `但表里损耗率写的是 ${rate.toFixed(2)}%，相差 ${round2(rate - expect).toFixed(2)} 个百分点。`,
  };
}

function checkNegativeQty(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = normNumber(it[role]);
    if (v === null || v >= -TOL) continue;
    out.push({
      level: 'P0', category: '数量为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 生鲜损耗表里的数量为负，`
        + '通常意味着盘点方向填反了（或把退货冲销混进了这张表），请先对回实物。',
    });
  }
  return out;
}

function checkTotalRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return out;
  let sum = 0;
  let n = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) { sum += v; n += 1; }
  }
  if (!n) return out;
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  out.push({
    level: 'P0', category: '合计行与明细之和不符', line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各行相加是 ${sum.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)} —— 合计列对不上，后面所有比率都会被带偏。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const period = String(it.period === undefined ? '' : it.period).trim();
    const cat = String(it.category === undefined ? '' : it.category).trim();
    if (!period || !cat) continue;
    const key = `${period}|${cat}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一品类同一期间出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经出现过，第 ${it.line} 行又来一行 —— `
          + '同一品类同一期间的损耗会被重复计入，损耗率会被算高。',
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）—— `
            + '缺一列这两条勾稽就都算不出来，请先补齐。',
        });
      }
    }
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** 同品类单价的**中位数**（≥3 行才算；少于 3 行中位数不稳健，宁可不判） */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到盘点表正文（text）—— 请把「期间 / 品类 / 进货量 / 期初库存 / 销售量 / 期末库存 / 损耗量 / 损耗率」'
      + '这张表（含表头，Tab 分隔最稳）贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `盘点表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何盘点明细行（期间 + 品类的具体数字）');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkLossFormula(it); if (a) findings.push(a);
    const b = checkLossRate(it); if (b) findings.push(b);
    for (const c of checkNegativeQty(it)) findings.push(c);
  }

  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let purchaseTotal = 0;
  let lossTotal = 0;
  const periods = new Set();
  for (const it of t.items) {
    const a = normNumber(it.purchaseQty); if (a !== null) purchaseTotal += a;
    const b = normNumber(it.lossQty); if (b !== null) lossTotal += b;
    const p = String(it.period === undefined ? '' : it.period).trim();
    if (p) periods.add(p);
  }

  const result = {
    status: 'success',
    service_type: 'FRESH_LOSS_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.size,
      purchase_qty_total: round2(purchaseTotal),
      loss_qty_total: round2(lossTotal),
      loss_rate_ref: LOSS_RATE_REF,
      unit_price_ref: UNIT_PRICE_REF,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periods.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核「进货量 + 期初库存 − 销售量 − 期末库存 = 损耗量」「损耗量 ÷ 进货量 = 损耗率」这类'
      + '**表内可复算的勾稽**，以及合计、重复、空缺、负数；**不判定损耗多少算正常，也不区分陈列损耗、报损、称重误差与内盗**'
      + '（那要现场盘点、监控与称重记录）；15% 只是**参考上限提示**，不是行业标准。结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, ratePct, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT,
};
