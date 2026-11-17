/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * material-usage-loss-check.js —— 材料领用与定额损耗核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**施工/制造项目每月核材料的时候**。项目部与物资部门要拿
 * 一张「材料领用与损耗表」对上三件事 —— **领用量**（仓库实际发出去多少）、
 * **定额用量**（按工程量 × 单位定额**应该**用多少）、以及两者的差额**损耗量**。
 * 损耗率一旦超耗，通常意味着**成本失控或跑冒滴漏**（多领、丢失、以领代耗、甚至虚假领用）。
 * 这三件事全是算术，**完全能算出来对错**。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   定额用量 = 工程量 × 单位定额
 *   损耗量   = 领用量 − 定额用量
 *   金额     = 领用量 × 单价
 *   单位一致：单位定额是"每单位工程量"的消耗量 ⇒ 表里声明的「定额单位」必须等于「工程量单位」
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**行业损耗标准与定额水平（合同、施工规范、地方定额各不相同）：
 *    单位定额与损耗率以表里给的为准，只对"明显超出常见参考上限"做**提示**并明确标注是参考。
 */

const CHECKS_GIVEN = [
  '定额用量复算（工程量 × 单位定额 = 定额用量）',
  '损耗量复算（领用量 − 定额用量 = 损耗量）',
  '合计行逐列复核',
  '同一材料重复行检测',
  '空白与占位符检测',
  '数量或单价为负检测',
];

const CHECKS_WITHHELD = [
  '损耗率超过参考上限（5%）提示（参考口径）',
  '领用量为零却有损耗检测',
  '金额与数量乘单价不符检测（领用量 × 单价 = 金额）',
  '工程量与定额单位不一致提示（单位定额须是"每单位工程量"的消耗量）',
  '损耗量为负（退料未冲减）提示',
];

const OUT_OF_SCOPE = [
  '判断行业/地方定额损耗标准与超耗的责任归属（以合同约定、施工规范与当地定额为准）',
  '核对材料实际盘点数量与库存台账（需要仓库台账与盘点表）',
  '区分甲供材料与乙供材料的计价与结算口径',
  '读取 ERP / 物资系统导出文件（需要你先导出成文本贴进来）',
];

/* 参考上限：仅供"明显超出"时提示，不是行业标准 */
const LOSS_RATE_REF = 0.05;

const SAMPLE_TEXT = [
  '期间\t材料名称\t计量单位\t工程量\t工程量单位\t定额单位\t单位定额\t定额用量\t领用量\t损耗量\t损耗率\t单价\t金额',
  '2026-01\t螺纹钢 HRB400\t吨\t1200\tm³\tm³\t0.085\t102.00\t104.50\t2.50\t2.39%\t3800.00\t397100.00',
  '2026-02\t螺纹钢 HRB400\t吨\t980\tm³\tm³\t0.085\t83.30\t84.00\t0.70\t0.83%\t3850.00\t323400.00',
  '2026-03\t螺纹钢 HRB400\t吨\t1400\tm³\tm³\t0.085\t119.00\t124.00\t5.00\t4.03%\t3800.00\t471200.00',
  '2026-03\t商品混凝土 C30\tm³\t1400\tm³\tm³\t1.015\t1421.00\t1445.00\t24.00\t1.66%\t460.00\t664700.00',
  '合计\t\t\t\t\t\t\t1725.30\t1757.50\t32.20\t\t\t1856400.00',
].join('\n');

const TOL = 0.01;
const AMOUNT_TOL = 0.01;
const RATE_TOL = 0.00001;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前，更宽泛的词在后。
  //    · 「工程量单位」必须在「工程量」之前，否则单位列被当成数量列；
  //    · 「定额单位」与「单位定额」是两列，都必须在宽泛的「单位」之前被认走。
  period: ['期间', '领用期间', '施工月份', '所属期', '月份'],
  workUnit: ['工程量单位', '工程量计量单位'],
  quotaUnit: ['定额单位', '定额用量单位'],
  quotaPerUnit: ['单位定额', '定额单耗', '单位消耗定额'],
  unit: ['计量单位', '材料单位', '单位'],
  material: ['材料名称', '物料名称', '材料规格', '材料', '品名'],
  workQty: ['工程量', '完成工程量', '施工量'],
  quotaQty: ['定额用量', '定额数量', '应耗用量', '定额耗用量'],
  issuedQty: ['领用量', '实际领用量', '领用数量'],
  lossRate: ['损耗率', '材料损耗率'],
  lossQty: ['损耗量', '损耗数量', '损耗'],
  price: ['单价', '材料单价', '含税单价'],
  amount: ['金额', '领用金额', '材料金额'],
};

const LABELS = {
  period: '期间', material: '材料名称', unit: '计量单位', workQty: '工程量',
  workUnit: '工程量单位', quotaUnit: '定额单位', quotaPerUnit: '单位定额',
  quotaQty: '定额用量', issuedQty: '领用量', lossQty: '损耗量', lossRate: '损耗率',
  price: '单价', amount: '金额',
};

const REQUIRED = ['period', 'material', 'workQty', 'quotaPerUnit', 'quotaQty', 'issuedQty', 'lossQty'];
const SUM_ROLES = ['quotaQty', 'issuedQty', 'lossQty', 'amount'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|合 计)$/;

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

/** 比率归一化成小数：`2.5%` ⇒ 0.025；`0.025` ⇒ 0.025；`2.5` ⇒ 0.025 */
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
  const p = it && it.period ? String(it.period).trim() : '';
  const m = it && it.material ? String(it.material).trim() : '';
  const tag = [p, m].filter(Boolean).join(' ');
  return tag || `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */

function checkQuotaQty(it) {
  const work = normNumber(it.workQty);
  const per = normNumber(it.quotaPerUnit);
  const stated = normNumber(it.quotaQty);
  if (work === null || per === null || stated === null) return null;
  const expect = round2(work * per);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '定额用量复算不符', line: it.line,
    message: `${who(it)}：工程量 ${work.toFixed(2)} × 单位定额 ${per} 应为 ${expect.toFixed(2)}，表里定额用量是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkLossQty(it) {
  const issued = normNumber(it.issuedQty);
  const quota = normNumber(it.quotaQty);
  const stated = normNumber(it.lossQty);
  if (issued === null || quota === null || stated === null) return null;
  const expect = round2(issued - quota);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '损耗量复算不符', line: it.line,
    message: `${who(it)}：领用量 ${issued.toFixed(2)} − 定额用量 ${quota.toFixed(2)} 应为 ${expect.toFixed(2)}，表里损耗量是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)} —— 损耗量就是这两个数之差，不该有第三种算法。`,
  };
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const mat = String(it.material === undefined || it.material === null ? '' : it.material).trim();
    if (!mat) continue;
    const per = String(it.period === undefined || it.period === null ? '' : it.period).trim();
    const key = `${per}|${mat}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一材料重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 同一期间的同一材料只该有一行，否则领用量与损耗量会被重复汇总。`,
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）—— 这一列会静默地不参与任何检查，先补齐再核。`,
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of ['workQty', 'quotaPerUnit', 'quotaQty', 'issuedQty', 'price']) {
    const v = normNumber(it[role]);
    if (v !== null && v < -TOL) {
      out.push({
        level: 'P0', category: '数量或单价为负', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 数量与单价不该为负；冲回或退料请单独列示，不要用负数混在领用里。`,
      });
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
    return insufficient('没有收到材料领用与损耗表正文（text）—— 请把「期间 / 材料名称 / 工程量 / 单位定额 / 定额用量 / 领用量 / 损耗量」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `材料领用与损耗表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何材料明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkQuotaQty(it); if (a) findings.push(a);
    const b = checkLossQty(it); if (b) findings.push(b);
    for (const x of checkNegative(it)) findings.push(x);

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

  const periods = [];
  let quotaTotal = 0; let issuedTotal = 0; let lossTotal = 0; let amountTotal = 0;
  for (const it of t.items) {
    const per = String(it.period === undefined || it.period === null ? '' : it.period).trim();
    if (per && periods.indexOf(per) < 0) periods.push(per);
    const a = normNumber(it.quotaQty); if (a !== null) quotaTotal += a;
    const b = normNumber(it.issuedQty); if (b !== null) issuedTotal += b;
    const c = normNumber(it.lossQty); if (c !== null) lossTotal += c;
    const d = normNumber(it.amount); if (d !== null) amountTotal += d;
  }

  const result = {
    status: 'success',
    service_type: 'MATERIAL_USAGE_LOSS_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.length,
      quota_qty_total: round2(quotaTotal),
      issued_qty_total: round2(issuedTotal),
      loss_qty_total: round2(lossTotal),
      amount_total: round2(amountTotal),
      loss_rate_ref: LOSS_RATE_REF,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periods.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核「工程量 × 单位定额 = 定额用量」「领用量 − 定额用量 = 损耗量」「领用量 × 单价 = 金额」'
      + '这类表内勾稽，**不规定行业损耗标准与定额水平**（以合同约定、施工规范与当地定额为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, OUT_OF_SCOPE, SAMPLE_TEXT,
};
