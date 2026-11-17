/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * mall-concession-check.js —— 商场联营抽成与保底核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月出结算单 / 结账之前**。购物中心与百货的联营（扣点）商户，
 * 每月都要逐户把「抽成租金（销售额 × 抽成率）」与「保底租金」比一次、按**孰高**计收，
 * 再加上物业费、推广费，算出本期应收合计，然后与已收金额对账。
 * 这张表算错，方向只有两个 —— **少收租金**（抽成低于保底却按抽成计）或 **多开票 / 多收**；
 * 它是商业地产收租的核心动作，也是月报、商户对账单、审计抽样必查的一张表。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   抽成租金 = 销售额 × 抽成率
 *   应收合计 = max(抽成租金, 保底租金) + 物业费 + 推广费
 *   合计行各列 = 明细行相加
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**合同条款与销售额口径本身（抽成率阶梯、保底是否含税、免租期与装修期、
 *    退货折扣怎么冲减销售额）：表里给的抽成率、合同抽成率、保底租金、计租方式一律**以你填的为准**，
 *    本工具只核表内勾稽与档位提示，并把可疑处按原文行号列出来。
 *
 * 接口契约：run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}；
 *      roleOf(表头) 必须能认出样例表的每一列（关键词顺序即优先级，见 ROLES 注释）。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER ——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量。
 */

const CHECKS_GIVEN = [
  '抽成租金复算（销售额 × 抽成率 = 抽成租金）',
  '应收合计复算（max(抽成租金, 保底租金) + 物业费 + 推广费 = 应收合计）',
  '合计行逐列复核',
  '同一铺位同一期间重复行检测',
  '空白与占位符检测',
  '金额或比例为负检测',
];

const CHECKS_WITHHELD = [
  '已收金额超过应收合计提示',
  '抽成率与合同约定抽成率不一致提示（阶梯切换 / 临时降点未同步）',
  '保底租金未按孰高原则计收提示（抽成低于保底却按抽成计）',
  '同一铺位重复计租同一期间提示（金额不同、按行数重复计租）',
  '空置铺位仍有应收提示',
];

const OUT_OF_SCOPE = [
  '判断联营合同条款本身（抽成率阶梯、保底是否含税、免租期与装修期、扣点与保底的适用条件、空置期是否减免）是否合法或合理',
  '判断销售额口径应以哪个为准（含税 / 不含税、退货与折扣冲减、线上订单、代金券与团购、员工内购、跨店调拨）',
  '处理增值税、房产税、发票开具口径与租金收入的确认时点',
  '处理联营转租赁、租金递增、滞纳金与违约金的计算',
  '读取商场 POS / 收银系统 / ERP 导出的 Excel（需要你先导出成文本贴进来）',
  '给出法律或税务意见',
];

/**
 * 样例表：2 个铺位 × 2 个期间 + 合计行，**两档都必须 0 命中**。
 *   · 每行都满足 抽成租金 = 销售额 × 抽成率；
 *   · 每行都满足 应收合计 = max(抽成租金, 保底租金) + 物业费 + 推广费；
 *   · 计租方式都是「孰高」（其中 B-208 两期抽成低于保底，正是靠孰高按保底计）；
 *   · 已收金额都不超过应收合计；
 *   · 合计行每一列都等于 4 行明细之和。
 */
const SAMPLE_TEXT = [
  '所属期间\t铺位号\t商户名称\t铺位状态\t销售额\t抽成率\t合同抽成率\t抽成租金\t保底租金\t物业费\t推广费\t应收合计\t已收金额\t计租方式',
  '2026-01\tA-101\t星巴克\t在营\t1000000.00\t10.00%\t10.00%\t100000.00\t80000.00\t12000.00\t5000.00\t117000.00\t117000.00\t孰高',
  '2026-02\tA-101\t星巴克\t在营\t1200000.00\t10.00%\t10.00%\t120000.00\t80000.00\t12000.00\t5000.00\t137000.00\t130000.00\t孰高',
  '2026-01\tB-208\t优衣库\t在营\t500000.00\t8.00%\t8.00%\t40000.00\t60000.00\t9000.00\t3000.00\t72000.00\t72000.00\t孰高',
  '2026-02\tB-208\t优衣库\t在营\t450000.00\t8.00%\t8.00%\t36000.00\t60000.00\t9000.00\t3000.00\t72000.00\t70000.00\t孰高',
  '合计\t\t\t\t3150000.00\t\t\t296000.00\t280000.00\t42000.00\t16000.00\t398000.00\t389000.00\t',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;      // 抽成率容差：0.05 个百分点

const ROLES = {
  // ⚠️ 顺序即优先级：roleOf 从上往下取**第一个**命中的角色，
  //    所以更具体的角色必须排在更宽泛的角色前面，否则列会被抢走（算错但不报缺列）。
  period: ['所属期间', '会计期间', '结算期间', '计费期间', '所属期', '结算期', '期间', '月份', '月度'],
  // 「铺位状态」必须排在「铺位号」之前：否则 `铺位` 会把状态列抢走
  status: ['铺位状态', '商铺状态', '经营状态', '营业状态', '租赁状态', '租户状态', '空置状态', '铺位情况', '状态'],
  unit: ['铺位编号', '铺位号', '商铺编号', '商铺号', '柜台编号', '柜台号', '房号', '铺号', '铺位', '商铺', '柜台'],
  tenant: ['商户名称', '商户全称', '租户名称', '品牌名称', '客户名称', '商户', '租户', '品牌'],
  // 「销售额」必须排在任何带「金额」的角色之前，否则「销售金额」会被抢走
  sales: ['月销售额', '销售额', '销售金额', '销售净额', '净销售额', '营业额', '销售流水', '销售'],
  // 「合同抽成率」必须排在「抽成率」之前
  contractRate: ['合同抽成率', '合同约定抽成率', '约定抽成率', '合同扣点率', '合同扣率', '合同佣金率', '合同抽成比例'],
  rate: ['抽成率', '扣点率', '扣率', '提成率', '佣金率', '抽成比例', '扣点'],
  // 「抽成租金」「保底租金」都必须排在兜底的「租金」之前
  commission: ['抽成租金', '抽成租金金额', '抽成额', '按抽成计租', '抽成部分'],
  baseRent: ['保底租金', '保底租金金额', '最低租金', '保底金额', '保底额', '固定租金'],
  propertyFee: ['物业费', '物业管理费', '物业服务费', '物业费金额', '物管费'],
  promoFee: ['推广费', '市场推广费', '广告推广费', '推广服务费', '营销费', '企划费'],
  receivable: ['应收合计', '应收租金合计', '本期应收合计', '应收金额合计', '应收总额', '本期应收'],
  received: ['已收金额', '实收金额', '收款金额', '已收租金', '已收合计', '本期已收', '已收'],
  basis: ['计租方式', '计租口径', '计租原则', '计租依据', '租金取数', '取数方式', '租金方式'],
  rentGeneric: ['租金'],      // 兜底：只写了「租金」的列（排在 抽成租金 / 保底租金 之后，否则会把它们抢走）
  amountGeneric: ['金额'],    // 兜底：只写了「金额」的列（排在 销售额 / 已收金额 之后）
};

const LABELS = {
  period: '所属期间', unit: '铺位号', tenant: '商户名称', status: '铺位状态', sales: '销售额',
  contractRate: '合同抽成率', rate: '抽成率', commission: '抽成租金', baseRent: '保底租金',
  propertyFee: '物业费', promoFee: '推广费', receivable: '应收合计', received: '已收金额',
  basis: '计租方式',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'unit', 'sales', 'rate', 'commission', 'baseRent',
  'propertyFee', 'promoFee', 'receivable'];
/** 合计行逐列复核的列（抽成率是比率，不做纵向加总） */
const SUM_ROLES = ['sales', 'commission', 'baseRent', 'propertyFee', 'promoFee', 'receivable', 'received'];
/** 逐行空白/占位符检测覆盖的列（= 必需列：这些格空着，对应的复算就被静默跳过了） */
const BLANK_ROLES = REQUIRED;
/**
 * 免费档负值检测覆盖的列：金额与比例。
 * ⚠️ 只报"这一格本身是负数"，**不**顺手推断"空置却收了租金""保底没按孰高计" ——
 *    那两项是完整档的独立检查项（见 CHECKS_WITHHELD）。
 */
const NEGATIVE_ROLES = ['sales', 'rate', 'contractRate', 'commission', 'baseRent',
  'propertyFee', 'promoFee', 'receivable', 'received'];
/** 完全重复行的指纹列（含这一行的全部业务字段，不含行号） */
const FINGERPRINT_ROLES = ['period', 'unit', 'tenant', 'status', 'sales', 'rate', 'contractRate',
  'commission', 'baseRent', 'propertyFee', 'promoFee', 'receivable', 'received', 'basis'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：|总计：)$/;

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

/** 比例归一化成小数：`10.00%` ⇒ 0.10；`0.10` ⇒ 0.10；`10` ⇒ 0.10 */
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
  const n = [it && it.unit, it && it.tenant]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

/** 一行的业务字段指纹：整行**逐字相同**才算"重复粘贴了一行" */
function rowFingerprint(it) {
  return FINGERPRINT_ROLES
    .map((r) => (it && it[r] !== undefined && it[r] !== null ? String(it[r]).trim() : ''))
    .join('|');
}

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkCommissionRent(it) {
  const out = [];
  const sales = normNumber(it.sales);
  const rate = rateValue(it.rate);
  const stated = normNumber(it.commission);
  if (sales === null || rate === null || stated === null) return out;
  const expect = round2(sales * rate);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '抽成租金复算不符', line: it.line,
    message: `${who(it)}：销售额 ${sales.toFixed(2)} × 抽成率 ${(rate * 100).toFixed(4)}% = ${expect.toFixed(2)}，`
      + `表里「抽成租金」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '抽成租金就是"销售额 × 抽成率"这一格：填少了就是少收租金，填多了就是多开票，'
      + '商户拿着自己的 POS 流水一乘就能对出来。',
  });
  return out;
}

function checkReceivableTotal(it) {
  const out = [];
  const comm = normNumber(it.commission);
  const base = normNumber(it.baseRent);
  const prop = normNumber(it.propertyFee);
  const promo = normNumber(it.promoFee);
  const stated = normNumber(it.receivable);
  if (comm === null || base === null || prop === null || promo === null || stated === null) return out;
  const higher = Math.max(comm, base);
  const expect = round2(higher + prop + promo);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '应收合计复算不符', line: it.line,
    message: `${who(it)}：max(抽成租金 ${comm.toFixed(2)}, 保底租金 ${base.toFixed(2)}) = ${higher.toFixed(2)}，`
      + `+ 物业费 ${prop.toFixed(2)} + 推广费 ${promo.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「应收合计」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + `⚠️ 只取了抽成（${comm.toFixed(2)}）或只取了保底（${base.toFixed(2)}）是这张表最常见的错：`
      + '联营合同是**抽成与保底孰高**，取低了就少收租金；'
      + '「应收合计」是给商户出结算单、开票、催收的取数口径，对不上两边都不可信。',
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
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，本表 ${n} 行明细的「${LABELS[role]}」相加是 ${expect.toFixed(2)}，`
        + `相差 ${round2(stated - expect).toFixed(2)}。合计行就是月报与商户对账单的取数口径，`
        + '对不上说明有一边错（明细改了合计没跟着改，或者合计是手打的）。',
    });
  }
  return out;
}

function checkDuplicateRows(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined ? String(it.period).trim() : '';
    const u = it.unit !== undefined ? String(it.unit).trim() : '';
    if (!p || !u) continue;
    const key = `${p}|${u}|${rowFingerprint(it)}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一铺位同一期间重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已整行出现过，第 ${it.line} 行逐字重复 —— `
          + '要么是结算表重复粘贴了一行，要么是同一个铺位同一期间被开了两张单（中途换约、拆铺各建一行）。'
          + '重复的那一行会把销售额、抽成租金、应收合计全部重复计一遍。',
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBlanks(it) {
  const out = [];
  for (const role of BLANK_ROLES) {
    if (isBlank(it[role])) {
      const s = String(it[role] === undefined ? '' : it[role]).trim();
      out.push({
        level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`
          + '这一列缺失时对应的复算做不了（空值会被静默跳过，看起来"没报错"）：'
          + '缺哪一列就补哪一列；本期确实不发生的那一项请填 0.00，不要留空。',
      });
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const isRate = role === 'rate' || role === 'contractRate';
    const v = isRate ? rateValue(it[role]) : normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    const shown = isRate ? `${(v * 100).toFixed(4)}%` : v.toFixed(2);
    out.push({
      level: 'P0', category: '金额或比例为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${shown}（负数）—— 销售额、抽成率、租金、物业费、推广费`
        + '与应收合计都不该为负；红字冲销、退货冲减请单独列示并在备注里说明，'
        + '直接填负数会让"孰高"与合计行双双算错。',
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
    return insufficient('没有收到商场联营抽成与保底核对表正文（text）—— 请把「所属期间 / 铺位号 / 商户名称 / 铺位状态 / 销售额 / 抽成率 / 合同抽成率 / 抽成租金 / 保底租金 / 物业费 / 推广费 / 应收合计 / 已收金额 / 计租方式」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `商场联营抽成与保底核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何联营商户明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkCommissionRent(it));
    findings.push(...checkReceivableTotal(it));
    findings.push(...checkNegative(it));
    findings.push(...checkBlanks(it));

  }

  findings.push(...checkTotalRow(t.totals, t.items));
  findings.push(...checkDuplicateRows(t.items));

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let salesTotal = 0;
  let receivableTotal = 0;
  for (const it of t.items) {
    const s = normNumber(it.sales);
    if (s !== null) salesTotal += s;
    const r = normNumber(it.receivable);
    if (r !== null) receivableTotal += r;
  }

  const result = {
    status: 'success',
    service_type: 'MALL_CONCESSION_RENT_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      sales_total: round2(salesTotal),
      receivable_total: round2(receivableTotal),
      tolerance: TOL,
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
    disclaimer: '只核"销售额 × 抽成率 = 抽成租金"与"max(抽成租金, 保底租金) + 物业费 + 推广费 = 应收合计"'
      + '这类**表内勾稽**与档位提示，**不判断合同条款与销售额口径本身**（抽成率阶梯、保底是否含税、'
      + '免租期、退货折扣怎么冲减，一律以合同与你的口径为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
