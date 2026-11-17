'use strict';
/**
 * autoshop-parts-labor-check.js —— 汽修配件与工时费结算核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每张维修工单交车结算时、每月与保险公司 / 大客户对账时**，
 * 服务顾问、配件库管、结算会计要把「维修工单配件与工时费明细表」核一遍 ——
 * 这张表是客户结算单、保险理赔单、门店收入与配件成本的原始依据，客户签字后再改就要走红冲 / 退料流程。
 *
 * 表里有几条算式**完全能算出来对错**（手算即可复现）：
 *
 *   配件小计 = 数量 × 配件单价
 *   工时费   = 工时 × 工时单价
 *   工单总额 = Σ配件小计 + Σ工时费 + Σ辅料费 − Σ折扣
 *
 * 免费档执行 6 类检查（见 CHECKS_GIVEN）；完整档（付费）在此之上多出**一种能力**：
 * **多收金额归因（单价 / 数量 / 工时 / 折扣口径）+ 跨门店与跨工单的多收汇总台账 +
 * 按多收金额从大到小的处理清单**（见 CHECKS_WITHHELD）。
 * 多收金额 = 表内金额 − 按上式复算的金额（负数即少收）。
 *
 * 与已有能力的区别：`piece-rate-wage-check` 核的是**计件工资**的单价与产量，
 * `logistics-fuel-card-check` 核的是油卡充值与油耗；本能力核的是**汽修工单**的
 * 「数量 × 配件单价」「工时 × 工时单价」与「工单总额 = 配件 + 工时 + 辅料 − 折扣」勾稽，
 * 多收归因方向也是门店场景（报价口径 / 派工工时 / 折扣让利 / 保险定损）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不写盘、不读环境变量**。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 材料不足时**绝不给结论**（既不做"一致"的认定，也不做"不一致"的认定），也不套用默认值。
 *
 * ⚠️ 完整档（付费）的实现集中在下面那行分隔注释之后；免费包在打包时会被整块摘掉。
 *    付费开关**只声明一次**（`run()` 里的一个布尔常量），免费包里连着开关与分支一起删。
 *    ⛔ 注释里**不要**写出那个开关的字面量：摘除脚本的残渣断言是纯字符串包含判断，写了会被判"没删干净"。
 */

const CHECKS_GIVEN = [
  '配件小计复算（配件小计 = 数量 × 配件单价）',
  '工时费复算（工时费 = 工时 × 工时单价）',
  '工单总额勾稽（工单总额 = Σ配件小计 + Σ工时费 + Σ辅料费 − Σ折扣）',
  '同一工单同一配件重复行检测（门店 + 工单号 + 配件名称 + 规格型号完全相同）',
  '配件数量 / 工时为负检测（退料 / 红字冲销行没有单独列示）',
  '关键字段空缺或占位符检测（必需列为空或写着待填 / 待补 / — / N/A）',
];

const CHECKS_WITHHELD = [
  '多收金额归因（单价口径 / 数量口径 / 工时口径 / 折扣口径）',
  '跨门店 / 跨工单多收汇总台账（按门店与按工单归集配件费、工时费、辅料费、折扣、多收金额）',
  '按多收金额从大到小的处理清单（带原文行号、归因口径与建议动作）',
];

const OUT_OF_SCOPE = [
  '判断配件单价 / 工时单价本身是否合理（原厂价、副厂价、同城工时定额、保险定损价以报价单、厂家价目表与合同为准）',
  '判断配件是否真的装到了这台车上、工时是否真的发生了（需要现场核实派工单、旧件回收与施工影像）',
  '判断折扣 / 让利 / 保险理赔口径是否符合门店与保险公司 / 大客户的结算协议',
  '处理负数（退料 / 红字冲销）行的会计处理与来源核实（本工具只把它标出来，请附退料单与红字发票）',
  '读取维修厂 DMS / ERP 导出的 Excel 文件（需要你先导出成文本贴进来）',
  '判断多收的这笔钱要不要向客户补收或退给客户（按合同与门店制度走，本工具只给金额与口径方向）',
];

const SAMPLE_TEXT = [
  '门店\t工单号\t配件名称\t规格型号\t数量\t配件单价\t配件小计\t工时项目\t工时\t工时单价\t工时费\t辅料费\t折扣\t工单总额\t备注',
  '城东店\tWO-20260301\t刹车片\t博世前轮\t1\t320.00\t320.00\t更换前刹车片\t1.5\t120.00\t180.00\t30.00\t20.00\t1320.00\t',
  '城东店\tWO-20260301\t刹车盘\t博世通风盘\t2\t280.00\t560.00\t更换前刹车盘\t2.0\t120.00\t240.00\t30.00\t20.00\t1320.00\t',
  '城西店\tWO-20260302\t机油\t全合成 5W-30\t4\t95.00\t380.00\t更换机油机滤\t0.8\t150.00\t120.00\t15.00\t15.00\t565.00\t',
  '城西店\tWO-20260302\t机油滤清器\t原厂\t1\t45.00\t45.00\t更换空气滤芯\t0.5\t100.00\t50.00\t0.00\t30.00\t565.00\t',
].join('\n');

/** 金额允许误差（0.01 元） */
const TOL = 0.01;
/** 复算差额的判定阈值（同 TOL，单独命名以便口径说明里引用） */
const MONEY_TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的前面，否则会被抢走列。
  //   「工单总额」必须由 total 先认领，否则会被 order 的「工单」抢走；
  //   「配件小计」「配件单价」必须排在 part 的「配件」之前；
  //   「工时项目」「工时费」「工时单价」必须都排在 hours 的「工时」之前。
  total: ['工单总额', '结算总额', '应收总额', '总额'],
  amount: ['配件小计', '配件金额', '材料小计', '小计'],
  // ⚠️ rate 必须排在 price 前面：price 的兜底别名是「单价」，排在前面会把「工时单价」抢走
  //    （表头守卫实测：工时单价 → price，工时费列算不出来，必需列 rate 永远认不出）。
  rate: ['工时单价', '工时费率', '工时价'],
  price: ['配件单价', '材料单价', '配件价', '单价'],
  laborItem: ['工时项目', '维修项目', '作业项目', '项目名称'],
  laborFee: ['工时费', '工时金额', '工时小计'],
  hours: ['工时', '小时', '用时'],
  qty: ['数量', '件数', '个数'],
  store: ['门店', '分店', '网点', '店名'],
  order: ['工单号', '工单编号', '结算单号', '单号', '工单'],
  part: ['配件名称', '配件', '件名'],
  spec: ['规格型号', '规格', '型号'],
  aux: ['辅料费', '辅料', '耗材费'],
  discount: ['折扣', '让利', '优惠'],
  note: ['备注', '说明'],
};

const LABELS = {
  store: '门店', order: '工单号', part: '配件名称', spec: '规格型号', qty: '数量',
  price: '配件单价', amount: '配件小计', laborItem: '工时项目', hours: '工时',
  rate: '工时单价', laborFee: '工时费', aux: '辅料费', discount: '折扣',
  total: '工单总额', note: '备注',
};

// 少一列就核不动：这 9 列缺任何一列都直接判"材料不足"，绝不猜
const REQUIRED = ['order', 'part', 'qty', 'price', 'amount', 'hours', 'rate', 'laborFee', 'total'];
// 只有"逐行发生额"可以按列相加；配件单价 / 工时单价是单价口径，工单总额是工单级字段（每行重复），相加没有意义
const SUM_ROLES = ['qty', 'amount', 'hours', 'laborFee', 'aux', 'discount'];

function insufficient(missing, advice) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: advice || '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|待确认)$/i.test(s);
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '').replace(/%$/, '');
  if (!/^-?\d+(\.\d+)?$/.test(t)) return null;
  const n = Number(t);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;
const fmt = (n) => (n === null || n === undefined || !Number.isFinite(Number(n)) ? '' : Number(n).toFixed(2));
const nz = (n) => (n === null || n === undefined ? 0 : n);

function roleOf(header) {
  const h = String(header === undefined || header === null ? '' : header).replace(/[\s（）()【】\[\]]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

function parseTable(text) {
  const raw = String(text === undefined || text === null ? '' : text)
    .split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null, cols: [], header: [], error: 'empty' };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const cols = headers.map((h, i) => ({ header: h, role: roles[i] }));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  if (missingColumns.length) return { items, totals: {}, missingColumns, cols, header: headers, error: 'no_header' };
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i] };
    roles.forEach((role, c) => {
      if (!role) return;
      row[role] = cells[c] === undefined ? '' : cells[c];
    });
    items.push(row);
  }
  return { items, totals: {}, missingColumns, cols, header: headers, error: null };
}

function cellOf(it, role) {
  const v = it === undefined || it === null ? undefined : it[role];
  return v === undefined || v === null ? '' : String(v).trim();
}

const who = (it) => {
  const t = [cellOf(it, 'store'), cellOf(it, 'order'), cellOf(it, 'part'), cellOf(it, 'spec')].filter(Boolean).join(' ');
  return t || `第 ${it && it.line} 行`;
};
/** 每条结论都必须能指回原文行 */
const head = (it) => `${who(it)}（原文第 ${it.line} 行）`;
const basisOf = (it) => `原文第 ${it.line} 行：${it.raw}`;

function distinct(items, role) {
  const seen = new Set();
  for (const it of items) {
    const v = cellOf(it, role);
    if (v) seen.add(v);
  }
  return [...seen];
}

/** 必需列全填出来的行才"核得动"；填不出来的行不给结论，也不进工单勾稽 */
function isClean(it) {
  return REQUIRED.every((r) => !isBlank(it[r]));
}

function groupByOrder(items) {
  const map = new Map();
  for (const it of items) {
    const store = cellOf(it, 'store');
    const order = cellOf(it, 'order');
    const key = `${store}|${order}`;
    if (!map.has(key)) map.set(key, { store, order, rows: [], lines: [] });
    const g = map.get(key);
    g.rows.push(it);
    g.lines.push(it.line);
  }
  return map;
}

function sumRole(items, role) {
  return round2(items.reduce((s, it) => s + nz(normNumber(it[role])), 0));
}

/** 一张工单的勾稽口径：配件费 / 工时费 / 辅料费 / 折扣 / 按式复算的总额 / 表内总额 */
function orderMathOf(group, hasAux, hasDiscount) {
  const parts = sumRole(group.rows, 'amount');
  const labor = sumRole(group.rows, 'laborFee');
  const aux = hasAux ? sumRole(group.rows, 'aux') : 0;
  const discount = hasDiscount ? sumRole(group.rows, 'discount') : 0;
  const settled = round2(parts + labor + aux - discount);
  const vals = [];
  for (const it of group.rows) {
    const n = normNumber(it.total);
    if (n === null) continue;
    const v = round2(n);
    if (!vals.some((x) => Math.abs(x - v) <= MONEY_TOL)) vals.push(v);
  }
  const billed = vals.length ? vals[0] : null;
  const consistent = vals.every((v) => Math.abs(v - vals[0]) <= MONEY_TOL);
  return { parts, labor, aux, discount, settled, billed, stated_vals: vals, consistent };
}

/**
 * 逐行"表内金额 − 按式复算金额"的差（多收为正、少收为负）。
 * 免费档用它汇总差额口径（summary.row_diff_total）；完整档的归因与处理清单也用它。
 * 任一项读不出来（空 / 占位符）时该项返回 null，不参与汇总。
 */
function rowDifferenceOf(it) {
  const qty = normNumber(it.qty);
  const price = normNumber(it.price);
  const amount = normNumber(it.amount);
  const hours = normNumber(it.hours);
  const rate = normNumber(it.rate);
  const laborFee = normNumber(it.laborFee);
  const parts = (qty === null || price === null || amount === null) ? null : round2(amount - qty * price);
  const labor = (hours === null || rate === null || laborFee === null) ? null : round2(laborFee - hours * rate);
  return { parts, labor, amount: round2(nz(parts) + nz(labor)) };
}

/* ================================ 免费档检查项 ================================ */

/** 免费档 1：配件小计 = 数量 × 配件单价 */
function partsSubtotalIssue(it) {
  const qty = normNumber(it.qty);
  const price = normNumber(it.price);
  const stated = normNumber(it.amount);
  if (qty === null || price === null || stated === null) return null;
  const expect = round2(qty * price);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '配件小计与数量×单价不符', line: it.line,
    diff: round2(stated - expect), expect, stated,
    message: `${head(it)}：数量 ${fmt(qty)} × 配件单价 ${fmt(price)} = 配件小计应为 ${fmt(expect)}，`
      + `表里写的却是 ${fmt(stated)}，相差 ${fmt(stated - expect)}。`,
    advice: '配件小计这一列是"数量 × 配件单价"的结果：先看是不是数量抄错（把 1 件写成 2 件）、'
      + '单价被改过（报价 320 填成 350），或者小计是按上一版报价倒挤出来的。',
    basis: basisOf(it),
  };
}

/** 免费档 2：工时费 = 工时 × 工时单价 */
function laborFeeIssue(it) {
  const hours = normNumber(it.hours);
  const rate = normNumber(it.rate);
  const stated = normNumber(it.laborFee);
  if (hours === null || rate === null || stated === null) return null;
  const expect = round2(hours * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '工时费与工时×工时单价不符', line: it.line,
    diff: round2(stated - expect), expect, stated,
    message: `${head(it)}：工时 ${fmt(hours)} × 工时单价 ${fmt(rate)} = 工时费应为 ${fmt(expect)}，`
      + `表里写的却是 ${fmt(stated)}，相差 ${fmt(stated - expect)}。`,
    advice: '工时费的分母是**工时**（不是工时定额、也不是套餐价）：'
      + '实数工时按 0.5 小时进位、或者把"标准工时"直接当成计费工时，都会让这一行对不上。'
      + '同一张工单里共用的一个工时项目，只在其中一行计费，其余行应写 0.00。',
    basis: basisOf(it),
  };
}

/** 免费档 3：工单总额 = Σ配件小计 + Σ工时费 + Σ辅料费 − Σ折扣（按工单聚合） */
function orderTotalIssue(group, hasAux, hasDiscount) {
  const m = orderMathOf(group, hasAux, hasDiscount);
  if (m.billed === null) return null;
  const diff = round2(m.billed - m.settled);
  if (Math.abs(diff) <= MONEY_TOL && m.consistent) return null;
  const first = group.rows[0];
  const extra = m.consistent ? ''
    : `；同一工单各行填的工单总额不一致（${m.stated_vals.map(fmt).join(' / ')}）`;
  return {
    level: 'P0', category: '工单总额与明细加总不符', line: first.line,
    diff, expect: m.settled, stated: m.billed,
    message: `${head(first)}：工单 ${group.order || '(未填工单号)'} 的明细加总 = 配件小计 ${fmt(m.parts)} `
      + `+ 工时费 ${fmt(m.labor)} + 辅料费 ${fmt(m.aux)} − 折扣 ${fmt(m.discount)} = ${fmt(m.settled)}，`
      + `表里写的工单总额是 ${fmt(m.billed)}，相差 ${fmt(diff)}${extra}。`,
    advice: '工单总额必须等于本工单所有明细行的"配件小计 + 工时费 + 辅料费 − 折扣"：'
      + '差额通常是漏了一行明细、某行被重复计入、折扣没从总额里扣，或者总额是从报价单 / 保险定损单抄过来的。',
    basis: basisOf(first),
  };
}

/** 免费档 4：同一工单同一配件重复行 */
function duplicateIssue(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    if (isBlank(it.order) || isBlank(it.part)) continue;
    const key = [cellOf(it, 'store'), cellOf(it, 'order'), cellOf(it, 'part'), cellOf(it, 'spec')].join('|');
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '重复配件行', line: it.line,
        message: `${head(it)}与原文第 ${seen.get(key)} 行是同一个配件（门店 + 工单号 + 配件名称 + 规格型号完全相同），`
          + '却被拆成了两行 —— 配件费与工时费会被重复汇总。',
        advice: '同一工单、同一配件（含规格）应合并成一行；'
          + '确实是分两次领料 / 换两个位置的，请在规格或备注里写清区别，不要再开一行。',
        basis: basisOf(it),
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/** 免费档 5：配件数量 / 工时为负（退料、红字行没有单独列示） */
function negativeIssue(it) {
  const qty = normNumber(it.qty);
  const hours = normNumber(it.hours);
  const bad = [];
  if (qty !== null && qty < 0) bad.push(`数量 ${fmt(qty)}`);
  if (hours !== null && hours < 0) bad.push(`工时 ${fmt(hours)}`);
  if (!bad.length) return null;
  return {
    level: 'P1', category: '配件数量或工时为负', line: it.line,
    message: `${head(it)}的${bad.join('、')}是负数 —— 负数行是退料 / 红字冲销，`
      + '这一行的配件费与工时费会把本工单的加总冲减掉。',
    advice: '退料 / 红冲要单独开一张红字工单或在备注里写明原因并附退料单；'
      + '混在正常结算明细里，客户与对账方都看不出来这笔钱为什么少了。',
    basis: basisOf(it),
  };
}

/** 免费档 6：必需列为空或占位符 */
function blankIssue(items, required) {
  const out = [];
  for (const it of items) {
    const miss = required.filter((r) => isBlank(it[r]));
    if (!miss.length) continue;
    out.push({
      level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
      message: `${head(it)}有 ${miss.length} 个关键字段是空的或占位符：`
        + `${miss.map((r) => `${LABELS[r]}（${cellOf(it, r) || '空'}）`).join('、')} —— `
        + '这一行的配件 / 工时勾稽核不动，本工具对它**不给结论**，这张工单的总额勾稽也一并跳过。',
      advice: '必需列一个都不能空：该是 0 就写 0.00 并在备注里说明，'
        + '别用「—」「待填」「待补」「无」「N/A」代替。',
      basis: basisOf(it),
    });
  }
  return out;
}

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`,
      '入参请写成 {"text": "（含表头的维修工单配件与工时费明细表）"}，或先用 --sample 看看需要什么格式。');
  }
  const p = payload && typeof payload === 'object' ? payload : {};
  const text = typeof p.text === 'string' ? p.text : (typeof p.content === 'string' ? p.content : '');
  if (text.trim().length < 5) {
    return insufficient(['维修工单配件与工时费明细表正文（text）'],
      '请把这张表连**表头**一起贴进来（Tab 分隔最稳）：门店 / 工单号 / 配件名称 / 规格型号 / 数量 / '
      + '配件单价 / 配件小计 / 工时项目 / 工时 / 工时单价 / 工时费 / 辅料费 / 折扣 / 工单总额。'
      + '可用 {"text": "…"}，或先跑 --sample 看格式。');
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['维修工单配件与工时费明细表正文（text）'],
      '入参里没有任何可读的行；请把这张表连表头一起贴进来。');
  }
  if (t.error === 'no_header') {
    return insufficient([
      `明细表缺少必需列：${t.missingColumns.join('、')}`,
      `必需列清单：${REQUIRED.map((r) => LABELS[r]).join('、')}`,
      `本次认出来的表头：${t.cols.map((c) => c.header).join(' / ') || '(一行都没认出来)'}`,
    ], '从 DMS / Excel 导出后，把表头与数据行一起复制成文本贴进来（Tab 分隔最稳）；'
      + '缺列就核不动，本工具不会靠猜补列。');
  }
  if (!t.items.length) {
    return insufficient(['至少一行配件 / 工时明细（工单号 + 配件名称 + 数量 + 配件单价 + 配件小计 + 工时 + 工时单价 + 工时费 + 工单总额）'],
      '只认到表头，没有明细行；请把数据行一起贴进来。');
  }
  if (!t.items.some(isClean)) {
    const first = t.items[0];
    const miss = REQUIRED.filter((r) => isBlank(first[r])).map((r) => `${LABELS[r]}（${cellOf(first, r) || '空'}）`);
    return insufficient([
      `至少一行**完整**的明细行（${REQUIRED.map((r) => LABELS[r]).join('、')} 都要能读出来）`,
      `本次认出的明细行：${t.items.length} 行，其中必需列填全的 0 行`,
      `原文第 ${first.line} 行的空白 / 占位符：${miss.join('、') || '(无)'}`,
    ], '把每一行的必需列都填出来（该是 0 就写 0.00，别用「—」「待填」「无」代替）；'
      + '一行都读不出来时本工具不给结论，也不套用默认值。');
  }

  const hasAux = t.cols.some((c) => c.role === 'aux');
  const hasDiscount = t.cols.some((c) => c.role === 'discount');
  const byOrder = groupByOrder(t.items);
  const ctx = { rows: t.items, byOrder, hasAux, hasDiscount };
  const findings = [];
  let executed = CHECKS_GIVEN.slice();
  let ledger = null;
  let actionPlan = [];

  for (const it of t.items) {
    const a = partsSubtotalIssue(it); if (a) findings.push(a);
    const b = laborFeeIssue(it); if (b) findings.push(b);
  }
  for (const g of byOrder.values()) {
    if (g.rows.some((it) => !isClean(it))) continue;   // 有填不出来的行 ⇒ 这张工单的总额勾稽不给结论
    const c = orderTotalIssue(g, hasAux, hasDiscount); if (c) findings.push(c);
  }
  for (const f of duplicateIssue(t.items)) findings.push(f);
  for (const it of t.items) { const g = negativeIssue(it); if (g) findings.push(g); }
  for (const f of blankIssue(t.items, REQUIRED)) findings.push(f);



  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));

  const stores = distinct(t.items, 'store');
  const orders = distinct(t.items, 'order');
  const parts = distinct(t.items, 'part');
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;
  const columnTotals = {};
  for (const role of SUM_ROLES) columnTotals[role] = sumRole(t.items, role);

  let settledTotal = 0;
  let billedTotal = 0;
  let rowDiffTotal = 0;
  let orderDiffTotal = 0;
  for (const g of byOrder.values()) {
    const clean = !g.rows.some((it) => !isClean(it));
    const m = clean
      ? orderMathOf(g, hasAux, hasDiscount)
      : { parts: 0, labor: 0, aux: 0, discount: 0, settled: 0, billed: null };
    if (clean && m.billed !== null) {
      settledTotal = round2(settledTotal + m.settled);
      billedTotal = round2(billedTotal + m.billed);
      if (Math.abs(m.billed - m.settled) > MONEY_TOL) orderDiffTotal = round2(orderDiffTotal + (m.billed - m.settled));
    }
    for (const it of g.rows) {
      const d = rowDifferenceOf(it).amount;
      if (Math.abs(d) > MONEY_TOL) rowDiffTotal = round2(rowDiffTotal + d);
    }
  }

  const result = {
    status: 'success',
    service_type: 'AUTOSHOP_PARTS_LABOR_CHECK',
    basis: '配件小计 = 数量 × 配件单价；工时费 = 工时 × 工时单价；'
      + '工单总额 = Σ配件小计 + Σ工时费 + Σ辅料费 − Σ折扣（辅料费 / 折扣按各明细行相加；'
      + '表内没有这两列时按 0 计，并在 scope 里标注口径来源）；'
      + '多收金额 = 表内金额 − 按上式复算的金额（负数即少收）。',
    findings,
    summary: {
      rows: t.items.length,
      stores: stores.length,
      orders: orders.length,
      parts: parts.length,
      total: findings.length,
      p0, p1, p2,
      column_totals: columnTotals,
      parts_amount_total: sumRole(t.items, 'amount'),
      labor_fee_total: sumRole(t.items, 'laborFee'),
      aux_fee_total: hasAux ? sumRole(t.items, 'aux') : 0,
      discount_total: hasDiscount ? sumRole(t.items, 'discount') : 0,
      settled_total: settledTotal,
      billed_total: billedTotal,
      row_diff_total: rowDiffTotal,
      order_diff_total: orderDiffTotal,
      discrepancy_total: round2(rowDiffTotal + orderDiffTotal),
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    scope: {
      checks: executed,
      checks_not_run: CHECKS_WITHHELD.slice(),
      rows: t.items.length,
      clean_rows: t.items.filter(isClean).length,
      stores: stores.length,
      orders: orders.length,
      aux_basis: hasAux ? '表内「辅料费」列，按明细行相加' : '表内没有「辅料费」列，按 0 计',
      discount_basis: hasDiscount ? '表内「折扣」列，按明细行相加并从工单总额中扣减' : '表内没有「折扣」列，按 0 计',
      tolerance: MONEY_TOL,
      executed_locally: true,
      network_used: false,
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: executed,
    checks_out_of_scope: OUT_OF_SCOPE,
  };



  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
