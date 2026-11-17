/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * logistics-storage-fee-check.js —— 物流仓储与操作费核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**电商/制造的财务、供应链对账岗，每月收到第三方仓库（3PL）的
 * 仓储与操作费结算表时**，必须逐项核对后才付款 —— 仓储费、操作费、超期费、退仓费四项
 * 与**账单金额**要对得上。这张表**最容易多收**：多算天数、单价悄悄上调、同一个计费项
 * 重复计一遍、超期费比例失控。全部都是**能算出来对错**的。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   仓储费应计 = 库存体积（或托盘数）× 单价 × 库存天数
 *   账单金额   = 仓储费 + 操作费 + 超期费 + 退仓费
 *   合计行     = 各明细行逐列相加
 *
 * 免费档执行 6 项；完整档另追加 5 项（见 CHECKS_WITHHELD），付费项统一包在 paid 分支里。
 * 材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**仓库收费标准、操作费单价与超期费政策：区间与上限以合同/报价单为准，
 *    只对"明显偏离表里给出的合同区间"或"明显超出常见区间"做**提示**并明确标注是参考口径。
 */

const CHECKS_GIVEN = [
  '仓储费复算（库存体积或托盘数 × 单价 × 库存天数 = 仓储费）',
  '账单合计复算（仓储费 + 操作费 + 超期费 + 退仓费 = 账单金额）',
  '合计行逐列复核',
  '同一仓库同一期重复行检测',
  '空白与占位符检测',
  '数量或金额为负检测',
];

const CHECKS_WITHHELD = [
  '账单金额与逐项加总不符提示（差额超重要性水平才算，参考口径）',
  '单价偏离合同参考区间提示（合同单价下限 / 合同单价上限）',
  '超期费比例超过参考上限提示（参考口径）',
  '库存天数为零却有仓储费检测',
  '同一计费项在本期重复出现提示',
];

const OUT_OF_SCOPE = [
  '判断仓库收费标准、操作费单价与超期费政策是否合理（以双方合同与报价单为准，本工具只按表里的数字复算）',
  '核对出入库单、托盘流转记录、库存台账本身是否准确（需要你先导出成文本贴进来）',
  '处理税率、发票、付款账期与预付款抵扣',
  '读取 WMS / TMS / 结算系统导出的二进制文件（请先导出成文本或 JSON）',
];

/** 干净样例：合计行 = 各列之和，两档跑它都必须 0 命中。 */
const SAMPLE_TEXT = [
  '仓库\t期间\t库存体积\t托盘数\t单价\t库存天数\t仓储费\t操作费\t超期费\t退仓费\t账单金额\t合同单价下限\t合同单价上限',
  '上海仓\t2026-01\t1200\t60\t1.20\t31\t44640.00\t6800.00\t0.00\t0.00\t51440.00\t1.00\t1.50',
  '上海仓\t2026-02\t1150\t58\t1.20\t28\t38640.00\t6500.00\t1800.00\t0.00\t46940.00\t1.00\t1.50',
  '广州仓\t2026-02\t800\t40\t1.35\t28\t30240.00\t4200.00\t0.00\t600.00\t35040.00\t1.30\t1.60',
  '合计\t\t3150.00\t158.00\t\t\t113520.00\t17500.00\t1800.00\t600.00\t133420.00\t\t',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的前面
  //    （「合同单价下限」含「单价」⇒ 若 unitPrice 排在前面，这一列会被整个抢走）
  priceMin: ['合同单价下限', '单价下限', '合同价下限', '价格下限'],
  priceMax: ['合同单价上限', '单价上限', '合同价上限', '价格上限'],
  warehouse: ['仓库名称', '仓库', '库房', '仓别'],
  period: ['计费期间', '期间', '月份', '所属期', '账期'],
  volume: ['库存体积', '体积', '立方数'],
  pallets: ['托盘数', '托盘', '板数'],
  unitPrice: ['结算单价', '单价'],
  days: ['库存天数', '计费天数', '天数'],
  storageFee: ['仓储费', '仓租费', '存储费'],
  handlingFee: ['操作费', '作业费', '操作处理费'],
  lateFee: ['超期费', '逾期费', '超期仓储费'],
  returnFee: ['退仓费', '退仓手续费', '退货上架费'],
  billAmount: ['账单金额', '结算金额', '应付金额', '账单合计'],
};

const LABELS = {
  warehouse: '仓库', period: '期间', volume: '库存体积', pallets: '托盘数', unitPrice: '单价',
  days: '库存天数', storageFee: '仓储费', handlingFee: '操作费', lateFee: '超期费',
  returnFee: '退仓费', billAmount: '账单金额', priceMin: '合同单价下限', priceMax: '合同单价上限',
};

const REQUIRED = ['warehouse', 'period', 'days', 'storageFee', 'billAmount'];
const SUM_ROLES = ['volume', 'pallets', 'storageFee', 'handlingFee', 'lateFee', 'returnFee', 'billAmount'];
const NEG_ROLES = ['volume', 'pallets', 'unitPrice', 'days', 'storageFee', 'handlingFee', 'lateFee', 'returnFee', 'billAmount'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|汇总|合计金额)$/;

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
      if ((role === 'warehouse' || role === 'period') && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const cell = (it, role) => String((it && it[role]) === undefined ? '' : it[role]).trim();

const who = (it) => {
  const w = cell(it, 'warehouse');
  const p = cell(it, 'period');
  if (w && p) return `${w} ${p}`;
  if (w) return w;
  if (p) return p;
  return `第 ${it && it.line} 行`;
};

const dupKey = (it) => {
  const w = cell(it, 'warehouse');
  const p = cell(it, 'period');
  if (!w || !p) return '';
  return `${w}|${p}`;
};

/* ================================ 免费档检查项 ================================ */

function checkStorageRecompute(it) {
  const stated = normNumber(it.storageFee);
  const days = normNumber(it.days);
  const price = normNumber(it.unitPrice);
  if (stated === null || days === null || price === null) return null;
  const bases = [];
  const vol = normNumber(it.volume);
  const pal = normNumber(it.pallets);
  if (vol !== null && vol !== 0) bases.push(['库存体积', vol]);
  if (pal !== null && pal !== 0) bases.push(['托盘数', pal]);
  if (!bases.length) return null;
  const exp = bases.map(([name, qty]) => ({ name, qty, expect: round2(qty * price * days) }));
  if (exp.some((e) => Math.abs(e.expect - stated) <= TOL)) return null;
  const detail = exp
    .map((e) => `按${e.name} ${e.qty} × 单价 ${price.toFixed(2)} × ${days} 天 = ${e.expect.toFixed(2)}`)
    .join('；');
  return {
    level: 'P0', category: '仓储费复算不符', line: it.line,
    message: `${who(it)}：${detail}，但表里的仓储费是 ${stated.toFixed(2)}，`
      + `相差 ${round2(stated - exp[0].expect).toFixed(2)} —— 仓储费就是这三个数乘出来的，差额通常是多算天数或单价被调过。`,
  };
}

function checkBillSum(it) {
  const bill = normNumber(it.billAmount);
  const storage = normNumber(it.storageFee);
  if (bill === null || storage === null) return null;
  const handling = normNumber(it.handlingFee) || 0;
  const late = normNumber(it.lateFee) || 0;
  const back = normNumber(it.returnFee) || 0;
  const sum = round2(storage + handling + late + back);
  if (Math.abs(bill - sum) <= TOL) return null;
  return {
    level: 'P0', category: '账单合计与四项费用之和不符', line: it.line,
    message: `${who(it)}：仓储费 ${storage.toFixed(2)} + 操作费 ${handling.toFixed(2)} + 超期费 ${late.toFixed(2)}`
      + ` + 退仓费 ${back.toFixed(2)} = ${sum.toFixed(2)}，但账单金额写的是 ${bill.toFixed(2)}，`
      + `相差 ${round2(bill - sum).toFixed(2)}。`,
  };
}

function checkNegatives(it) {
  const out = [];
  for (const role of NEG_ROLES) {
    const v = normNumber(it[role]);
    if (v === null || v >= -TOL) continue;
    out.push({
      level: 'P0', category: '数量或金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 红字冲回应当单独列一行并注明原因，`
        + '否则会与正常费用混在一起，合计看着正常但明细多扣了钱。',
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)} —— 合计行被改过，或者有明细行没列进来。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = dupKey(it);
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一仓库同一期出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经出现过，第 ${it.line} 行又出现一次 —— `
          + '同一仓库同一期正常只该有一行，请确认不是把同一张账单贴了两遍。',
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
        const s = cell(it, role);
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）—— 缺了它这条明细就无法复算。`,
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
    return insufficient('没有收到结算表正文（text）—— 请把「仓库 / 期间 / 库存体积或托盘数 / 单价 / 库存天数 / 仓储费 / 操作费 / 超期费 / 退仓费 / 账单金额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `结算表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何仓库明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkStorageRecompute(it); if (a) findings.push(a);
    const b = checkBillSum(it); if (b) findings.push(b);
    for (const x of checkNegatives(it)) findings.push(x);

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

  let billTotal = 0; let storageTotal = 0;
  const periodSet = new Set();
  for (const it of t.items) {
    const a = normNumber(it.billAmount); if (a !== null) billTotal += a;
    const b = normNumber(it.storageFee); if (b !== null) storageTotal += b;
    const p = cell(it, 'period'); if (p) periodSet.add(p);
  }
  const rows = t.items.length;
  const periods = periodSet.size;

  const result = {
    status: 'success',
    service_type: 'LOGISTICS_STORAGE_FEE_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows,
      periods,
      executed_locally: true,
      network_used: false,
      bill_total: round2(billTotal),
      storage_fee_total: round2(storageTotal),
      tolerance: TOL,
    },
    findings,
    summary: {
      rows,
      periods,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"库存体积（或托盘数）× 单价 × 库存天数 = 仓储费""仓储费 + 操作费 + 超期费 + 退仓费 = 账单金额"'
      + '这类内部勾稽；**不规定仓库收费标准、操作费单价与超期费政策**（以合同与报价单为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
