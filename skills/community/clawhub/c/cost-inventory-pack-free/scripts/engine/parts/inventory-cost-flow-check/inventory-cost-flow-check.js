/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * inventory-cost-flow-check.js —— 存货出入库与加权平均成本核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**月末成本结转前**，财务/成本会计要把存货的"数量"与"金额"
 * 两条线都对平 —— 期初 + 入库 − 出库 = 期末，而且**出库成本必须按加权平均单价结转**。
 * 这一步错了会一路错下去：毛利率错 → 利润错 → 所得税错 → 盘点对不上。
 * 这是每个月都要做、且**完全能算出来对错**的活。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   期末数量 = 期初数量 + 入库数量 − 出库数量
 *   期末金额 = 期初金额 + 入库金额 − 出库金额
 *   加权平均单价 = (期初金额 + 入库金额) ÷ (期初数量 + 入库数量)
 *   出库金额     = 出库数量 × 加权平均单价
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具按**月末一次加权平均**核对；若贵司用先进先出、移动加权或个别计价，
 *    请只把本工具当"数量与金额勾稽"用（口径写在输出里，不会假装通用）。
 */

const CHECKS_GIVEN = [
  '期末数量勾稽（期初 + 入库 − 出库 = 期末）',
  '期末金额勾稽（期初 + 入库 − 出库 = 期末）',
  '出库成本与加权平均单价复算',
  '合计行逐列复核',
  '重复存货检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '出库单价偏离加权平均单价检测（偏离率 > 1%）',
  '期末数量为负检测',
  '出库数量超过可用数量检测（期初 + 入库）',
  '数量或金额为负检测',
  '期初有数量无金额（单价为零）检测',
];

const OUT_OF_SCOPE = [
  '按先进先出（FIFO）、移动加权、个别计价法核算（本工具按**月末一次加权平均**核对）',
  '计提存货跌价准备、判断可变现净值',
  '盘点差异处理与盘盈盘亏入账',
  '读取 ERP 或进销存导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '存货名称\t期初数量\t期初金额\t入库数量\t入库金额\t出库数量\t出库金额\t期末数量\t期末金额',
  '螺纹钢HRB400\t120.00\t480000.00\t80.00\t336000.00\t150.00\t612000.00\t50.00\t204000.00',
  '水泥P.O42.5\t200.00\t90000.00\t100.00\t46000.00\t180.00\t81600.00\t120.00\t54400.00',
  '合计\t\t570000.00\t\t382000.00\t\t693600.00\t\t258400.00',
].join('\n');

const TOL = 0.01;
const UNIT_TOL = 0.02;          // 单价容忍 2 分
const DEV_CAP = 0.01;           // 出库单价偏离率 1%

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  item: ['存货名称', '物料名称', '商品名称', '品名', '存货'],
  openQty: ['期初数量', '上期结存数量', '期初数'],
  openAmt: ['期初金额', '上期结存金额', '期初额'],
  inQty: ['入库数量', '购进数量', '入库数'],
  inAmt: ['入库金额', '购进金额', '入库额'],
  outQty: ['出库数量', '发出数量', '出库数'],
  outAmt: ['出库金额', '发出金额', '结转成本', '出库额'],
  closeQty: ['期末数量', '结存数量', '期末数'],
  closeAmt: ['期末金额', '结存金额', '期末额'],
};

const LABELS = {
  item: '存货名称', openQty: '期初数量', openAmt: '期初金额', inQty: '入库数量',
  inAmt: '入库金额', outQty: '出库数量', outAmt: '出库金额', closeQty: '期末数量', closeAmt: '期末金额',
};

const REQUIRED = ['item', 'openQty', 'openAmt', 'inQty', 'inAmt', 'outQty', 'outAmt', 'closeQty', 'closeAmt'];
const SUM_ROLES = ['openQty', 'openAmt', 'inQty', 'inAmt', 'outQty', 'outAmt', 'closeQty', 'closeAmt'];
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
const round4 = (n) => Math.round(n * 1e4) / 1e4;

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
      if (role === 'item' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => (it && it.item ? String(it.item) : `第 ${it && it.line} 行`);

/** 加权平均单价（可用数量为 0 时返回 null） */
function avgUnitPrice(it) {
  const oq = normNumber(it.openQty); const oa = normNumber(it.openAmt);
  const iq = normNumber(it.inQty); const ia = normNumber(it.inAmt);
  if ([oq, oa, iq, ia].some((v) => v === null)) return null;
  const qty = oq + iq;
  if (qty <= 0) return null;
  return { unit: (oa + ia) / qty, qty, amt: oa + ia };
}

/* ================================ 免费档检查项 ================================ */

function checkQtyIdentity(it) {
  const oq = normNumber(it.openQty); const iq = normNumber(it.inQty);
  const uq = normNumber(it.outQty); const cq = normNumber(it.closeQty);
  if ([oq, iq, uq, cq].some((v) => v === null)) return null;
  const expect = round4(oq + iq - uq);
  if (Math.abs(expect - cq) <= TOL) return null;
  return {
    level: 'P0', category: '期末数量勾稽不符', line: it.line,
    message: `${who(it)}：期初 ${oq} + 入库 ${iq} − 出库 ${uq} 应为 ${expect}，表里期末写的是 ${cq}，相差 ${round4(cq - expect)}。`,
  };
}

function checkAmtIdentity(it) {
  const oa = normNumber(it.openAmt); const ia = normNumber(it.inAmt);
  const ua = normNumber(it.outAmt); const ca = normNumber(it.closeAmt);
  if ([oa, ia, ua, ca].some((v) => v === null)) return null;
  const expect = round2(oa + ia - ua);
  if (Math.abs(expect - ca) <= TOL) return null;
  return {
    level: 'P0', category: '期末金额勾稽不符', line: it.line,
    message: `${who(it)}：期初金额 ${oa.toFixed(2)} + 入库 ${ia.toFixed(2)} − 出库 ${ua.toFixed(2)} 应为 ${expect.toFixed(2)}，表里期末写的是 ${ca.toFixed(2)}，相差 ${round2(ca - expect).toFixed(2)}。`,
  };
}

function checkOutCost(it) {
  const uq = normNumber(it.outQty);
  const ua = normNumber(it.outAmt);
  if (uq === null || ua === null || uq <= 0) return null;
  const avg = avgUnitPrice(it);
  if (!avg) return null;
  const unit = ua / uq;
  if (Math.abs(unit - avg.unit) <= UNIT_TOL) return null;
  const expect = round2(uq * avg.unit);
  return {
    level: 'P0', category: '出库成本与加权平均不符', line: it.line,
    message: `${who(it)}：出库 ${uq} 按加权平均单价 ${round4(avg.unit)} 结转应为 ${expect.toFixed(2)}，表里出库金额是 ${ua.toFixed(2)}（折合单价 ${round4(unit)}），相差 ${round2(ua - expect).toFixed(2)}。`,
  };
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
    message: `合计行的「${LABELS[role]}」是 ${stated}，各明细行相加是 ${sum}，相差 ${round2(stated - sum)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = String(it.item || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一存货出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 请合并，否则成本会被重复结转。`,
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
        });
      }
    }
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
    return insufficient('没有收到存货表正文（text）—— 请把「存货名称 / 期初 / 入库 / 出库 / 期末」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `存货表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何存货明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkQtyIdentity(it); if (a) findings.push(a);
    const b = checkAmtIdentity(it); if (b) findings.push(b);
    const c = checkOutCost(it); if (c) findings.push(c);

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

  let closeAmtTotal = 0;
  for (const it of t.items) {
    const v = normNumber(it.closeAmt); if (v !== null) closeAmtTotal += v;
  }

  const result = {
    status: 'success',
    service_type: 'INVENTORY_COST_FLOW_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      items: t.items.length,
      closing_amount_total: round2(closeAmtTotal),
      costing_method: '月末一次加权平均（若贵司用 FIFO/移动加权，请只当数量与金额勾稽用）',
      unit_tolerance: UNIT_TOL,
      deviation_cap: DEV_CAP,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      items: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '按**月末一次加权平均**核数量与金额勾稽，不对其他计价方法下结论；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, avgUnitPrice, round2, round4, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
