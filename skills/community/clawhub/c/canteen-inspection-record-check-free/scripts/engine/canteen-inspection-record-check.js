#!/usr/bin/env node
/**
 * canteen-inspection-record-check.js —— 食堂进货查验与留样记录核对引擎（**免费档**；确定性、纯 Node 标准库）。
 *
 * 真实痛点：《食品安全法》要求食品经营者建立**进货查验记录**（供货者、许可证、批次、保质期、数量、票据）；
 *   集中用餐单位（学校 / 企业 / 机关食堂）还要**每餐次留样**（≥125g、留样 48 小时、记录留样人与时间），
 *   并做**餐具消毒记录**。食堂管理员 / 后勤每月自查（以及监管抽查时）必须把这些记录与采购台账、菜单对上：
 *   数量对不上、留样缺餐次、消毒记录断档都是**整改 / 处罚项**。记录都是表格 ⇒ 可以机械核对。
 *
 * 本文件是**免费档**：只执行下面 `CHECKS_GIVEN` 列出的六项逐行 / 逐格核对；
 * 完整档（买断版）追加的**留样保存时长、餐具消毒断档、供货者证照有效期、保质期与入库日期、
 * 分供货者 × 分品类汇总整改清单**这五类实现不在这个包里，`CHECKS_WITHHELD` 只是说明文本。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定食堂实际食品安全状况、不核留样实物与消毒工艺是否达标、不判证照真伪、
 *          不读 .xlsx/.pdf/图片原件、不联网核验；材料不足**一律不给结论**。
 *
 * ⚠️ 本免费引擎由 tools/strip_free_engine.py 从买断包引擎（canteen-inspection-record-check-full.js）摘出：
 *    完整档检查的实现与它们的辅助函数已整块摘除，这里连一个付费开关都不剩（静态与行为双重判据见免费层泄漏守卫）。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '进货数量勾稽（逐行按批次复算 入库数量 = 采购数量 − 退货数量，差额不为零即列出并给差额）',
  '进货金额勾稽（逐行复算 单价 × 入库数量 + 运费 = 金额，差额不为零即列出并给差额）',
  '留样餐次完整性（表中每个日期的 早/中/晚 三个餐次逐格点名，缺哪个日期加哪个餐次就报哪个）',
  '留样量达标（单份留样量须 ≥ 留样下限列登记的下限，低于即报并给该行原文）',
  '同一供货者 + 同一批次重复登记检测（重复出现即点名两处行号与两处原文）',
  '空白 / 占位符 / 认不出格式检测（13 个必需字段逐行点名；数值、日期与时间格式认不出即报；缺列只报材料不足，绝不给结论）',
];

const CHECKS_WITHHELD = [
  '留样保存时长核对（留样时间到销毁 / 记录时间须 ≥ 48 小时，不足即报并给两处原文）',
  '餐具消毒记录断档检测（按表中日期序列逐日比对，缺哪一天就点名哪一天）',
  '供货者证照有效期覆盖（进货日期晚于食品经营许可证到期日即报，给两处原文）',
  '保质期与入库日期核对（入库日期晚于保质期到期日即报，给两处原文）',
  '分供货者 × 分品类汇总清单（按问题数量从多到少排序，逐组给出可整改动作，并输出 consolidated_actions）',
];

const OUT_OF_SCOPE = [
  '判定食堂实际食品安全状况、是否真的发生食源性疾病 —— 那是监管抽检与现场检查的职责，本工具只核表格字面',
  '判定留样实物是否真实存在、留样冰箱温度是否达标、留样容器是否专用（要现场看，本工具看不到实物）',
  '判定餐具消毒方式是否合规（热力消毒的温度时长、化学消毒的浓度与浸泡时间是否达标）—— 本工具只核消毒记录有没有断档',
  '判定供货者证照本身真伪（是否伪造、是否已被监管注销）—— 本工具只按台账上写的到期日做日期比较',
  '读取 .xlsx / .pdf / 图片原件、联网核验证照与检验检疫证明、替代市场监管部门的检查结论',
];

// 样例：一张**干净**的食堂进货查验与留样记录核对表 —— 连续两天（2025-06-03 / 06-04）、每天早/中/晚三餐次，
// 数量勾稽、金额勾稽（含运费行）、留样量与 48 小时保存时长、证照有效期、保质期、餐具消毒逐日登记全部对得上。
// 人名与单位为编造，许可证号是自编号码，不含任何证件号码形态。
const SAMPLE_TEXT = [
  '日期\t餐次\t品名\t品类\t供货者\t许可证号\t许可证到期日\t批次\t保质期至\t采购数量\t退货数量\t入库数量\t单价\t运费\t金额\t票据号\t留样量(g)\t留样下限(g)\t留样时间\t留样人\t留样销毁时间\t餐具消毒',
  '2025-06-03\t早\t大米\t米面粮油\t兴禾粮油配送中心\tJY13201020012345\t2027-12-31\tXH20250601\t2025-12-31\t100\t0\t100\t5.20\t0.00\t520.00\tFP20250603001\t130\t125\t2025-06-03 07:20\t陈晓岚\t2025-06-05 08:00\t已消毒',
  '2025-06-03\t中\t青菜\t蔬菜\t绿源蔬菜配送有限公司\tJY13201030023456\t2027-06-30\tLY20250603A\t2025-06-08\t60\t2\t58\t3.50\t20.00\t223.00\tFP20250603002\t150\t125\t2025-06-03 11:35\t周慧敏\t2025-06-05 12:10\t已消毒',
  '2025-06-03\t晚\t鸡腿\t肉禽蛋\t康达肉禽有限公司\tJY13201040034567\t2028-03-31\tKD20250602\t2025-06-12\t80\t0\t80\t12.60\t0.00\t1008.00\tFP20250603003\t140\t125\t2025-06-03 17:40\t陈晓岚\t2025-06-05 18:00\t已消毒',
  '2025-06-04\t早\t大米\t米面粮油\t兴禾粮油配送中心\tJY13201020012345\t2027-12-31\tXH20250602\t2026-01-31\t50\t0\t50\t5.20\t0.00\t260.00\tFP20250604001\t128\t125\t2025-06-04 07:15\t李文博\t2025-06-06 07:45\t已消毒',
  '2025-06-04\t中\t土豆\t蔬菜\t绿源蔬菜配送有限公司\tJY13201030023456\t2027-06-30\tLY20250604A\t2025-06-20\t45\t0\t45\t4.20\t15.00\t204.00\tFP20250604002\t135\t125\t2025-06-04 11:50\t周慧敏\t2025-06-06 12:05\t已消毒',
  '2025-06-04\t晚\t鲈鱼\t水产\t江海水产商行\tJY13201050045678\t2027-09-30\tJH20250604\t2025-06-06\t30\t0\t30\t18.00\t0.00\t540.00\tFP20250604003\t145\t125\t2025-06-04 17:30\t李文博\t2025-06-06 18:00\t已消毒',
].join('\n');

const TOL = 0.01;

// 应留样餐次（集中用餐单位每餐次都要留样）
const MEAL_SLOTS = ['早', '中', '晚'];

// 表头级必需列（缺任何一列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = [
  'date', 'meal', 'itemName', 'supplier', 'purchaseQty', 'returnQty', 'stockQty',
  'unitPrice', 'amount', 'sampleQty', 'sampleMin', 'sampleTime', 'sampleKeeper',
];

// 单元格级必需字段（空白 / 占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['date', '日期'],
  ['meal', '餐次'],
  ['itemName', '品名'],
  ['supplier', '供货者'],
  ['purchaseQty', '采购数量'],
  ['returnQty', '退货数量'],
  ['stockQty', '入库数量'],
  ['unitPrice', '单价'],
  ['amount', '金额'],
  ['sampleQty', '留样量'],
  ['sampleMin', '留样下限'],
  ['sampleTime', '留样时间'],
  ['sampleKeeper', '留样人'],
];

// 数值列（用于「认不出格式 / 负数」判定；运费列可空，填了就必须认得出）
const NUMERIC_FIELDS = [
  ['purchaseQty', '采购数量'],
  ['returnQty', '退货数量'],
  ['stockQty', '入库数量'],
  ['unitPrice', '单价'],
  ['freight', '运费'],
  ['amount', '金额'],
  ['sampleQty', '留样量'],
  ['sampleMin', '留样下限'],
];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词会抢走更具体的列（仓库踩过 6 次，见 tools/header_map_check.py）。
//    例：「留样下限(g)」必须先于「留样量(g)」，「留样销毁时间」必须先于「留样时间」。
const ROLES = {
  date: ['进货日期', '入库日期', '验收日期', '日期'],
  meal: ['餐次', '餐别', '供餐餐次'],
  itemName: ['品名', '食材名称', '食品名称', '商品名称', '物品名称'],
  category: ['品类', '食材类别', '食品类别', '类别'],
  supplier: ['供货者', '供货商', '供应商', '供货单位'],
  licenseNo: ['许可证号', '许可证编号', '证照编号', '食品经营许可证号'],
  licenseExpiry: ['许可证到期日', '许可证有效期至', '证照有效期至', '证照到期日', '到期日'],
  batchNo: ['批次号', '生产批号', '批次', '批号'],
  shelfLife: ['保质期至', '保质期到期日', '保存期限至', '保质期'],
  purchaseQty: ['采购数量', '进货数量', '订货数量', '采购数'],
  returnQty: ['退货数量', '退回数量', '退库数量', '退货数'],
  stockQty: ['入库数量', '验收入库数量', '入库数'],
  unitPrice: ['进货单价', '采购单价', '单价', '价格'],
  freight: ['运费', '运输费', '配送费', '物流费'],
  amount: ['金额', '货款金额', '应付金额', '价款合计'],
  invoiceNo: ['票据号', '发票号', '票据编号', '单据号'],
  sampleMin: ['留样量下限', '留样下限', '留样最低量', '留样标准量', '留样标准'],
  sampleQty: ['留样量', '留样数量', '留样重量', '留样克重'],
  sampleTime: ['留样时间', '留样时刻', '留样日期'],
  destroyTime: ['留样销毁时间', '销毁时间', '留样销毁', '销毁记录时间'],
  sampleKeeper: ['留样人', '留样员', '留样人员', '留样负责人'],
  disinfection: ['餐具消毒记录', '餐具消毒', '消毒记录', '消毒情况'],
};

const LABELS = {
  date: '日期',
  meal: '餐次',
  itemName: '品名',
  category: '品类',
  supplier: '供货者',
  licenseNo: '许可证号',
  licenseExpiry: '许可证到期日',
  batchNo: '批次',
  shelfLife: '保质期至',
  purchaseQty: '采购数量',
  returnQty: '退货数量',
  stockQty: '入库数量',
  unitPrice: '单价',
  freight: '运费',
  amount: '金额',
  invoiceNo: '票据号',
  sampleMin: '留样下限',
  sampleQty: '留样量',
  sampleTime: '留样时间',
  destroyTime: '留样销毁时间',
  sampleKeeper: '留样人',
  disinfection: '餐具消毒',
};

const SUM_ROLES = ['purchaseQty', 'returnQty', 'stockQty', 'amount', 'sampleQty'];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张表补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「对得上」，也不说「对不上」。',
  };
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '');
  if (!/^-?\d+(\.\d+)?%?$/.test(t)) return null;
  const n = Number(t.replace('%', ''));
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s)
    || /^(n\/?a|无|不适用|待填|待补|待定|待核|待查|略|none)$/i.test(s);
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
}

function roleOf(header) {
  const h = String(header == null ? '' : header).replace(/[\s（）()：:]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    for (const k of keys) {
      if (h.indexOf(k) >= 0) return role;
    }
  }
  return null;
}

/** 解析成 {header, cols, items, totals, missingRoles, missingColumns, error}；行是**扁平**对象：{line, raw, 角色:值…} */
function parseTable(text) {
  const rawLines = String(text == null ? '' : text).split(/\r?\n/);
  const rows = [];
  for (let i = 0; i < rawLines.length; i++) {
    if (String(rawLines[i]).trim() === '') continue;
    rows.push({ line: i + 1, raw: String(rawLines[i]) });
  }
  if (!rows.length) {
    return {
      error: 'empty', header: [], cols: [], items: [], totals: {},
      missingRoles: REQUIRED_ROLES.slice(), missingColumns: REQUIRED_ROLES.map((r) => LABELS[r]),
    };
  }

  const header = splitRow(rows[0].raw);
  const cols = header.map((h, k) => ({ header: h, role: roleOf(h), index: k }));
  const items = [];
  for (let r = 1; r < rows.length; r++) {
    const cells = splitRow(rows[r].raw);
    const it = { line: rows[r].line, raw: rows[r].raw };
    for (const c of cols) {
      if (!c.role) continue;
      it[c.role] = cells[c.index] === undefined ? '' : cells[c.index];
    }
    items.push(it);
  }

  const missingRoles = REQUIRED_ROLES.filter((r) => !cols.some((c) => c.role === r));
  const totals = {};
  for (const role of SUM_ROLES) {
    totals[role] = round2(items.reduce((acc, it) => {
      const n = normNumber(it[role]);
      return acc + (n === null ? 0 : n);
    }, 0));
  }
  return {
    error: missingRoles.length ? 'no_header' : null,
    header,
    cols,
    items,
    totals,
    missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  };
}

const num = (it, role) => {
  const n = normNumber(it[role]);
  return n === null ? 0 : n;
};

function money(n) {
  const v = Math.abs(n) < 0.005 ? 0 : n;
  return v.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/** 数量 / 克重：整数就不带小数尾巴，免得「100.00 斤」看着别扭 */
function qtyText(n) {
  const v = round2(n);
  return Number.isInteger(v) ? String(v) : v.toFixed(2);
}

function cellText(v) {
  return String(v == null ? '' : v).trim();
}

/** 日期 → UTC 零点毫秒；认不出（含 2025-13-40 这类假日期）返回 null */
function parseDate(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/\s+/g, ' ');
  const m = /^(\d{4})[-/.年](\d{1,2})[-/.月](\d{1,2})日?$/.exec(s);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const ms = Date.UTC(y, mo - 1, d);
  const back = new Date(ms);
  if (back.getUTCFullYear() !== y || back.getUTCMonth() !== mo - 1 || back.getUTCDate() !== d) return null;
  return ms;
}

/** 日期 + 时刻 → UTC 毫秒；认不出返回 null（留样时间 / 销毁时间都用它） */
function parseDateTime(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/\s+/g, ' ');
  const m = /^(\d{4})[-/.年](\d{1,2})[-/.月](\d{1,2})日?[ T](\d{1,2}):(\d{2})(?::(\d{2}))?$/.exec(s);
  if (!m) return null;
  const day = parseDate(`${m[1]}-${m[2]}-${m[3]}`);
  if (day === null) return null;
  const hh = Number(m[4]);
  const mi = Number(m[5]);
  const ss = m[6] ? Number(m[6]) : 0;
  if (hh > 23 || mi > 59 || ss > 59) return null;
  return day + hh * 3600000 + mi * 60000 + ss * 1000;
}

const pad2 = (n) => String(n).padStart(2, '0');

function fmtDay(ms) {
  const d = new Date(ms);
  return `${d.getUTCFullYear()}-${pad2(d.getUTCMonth() + 1)}-${pad2(d.getUTCDate())}`;
}

/** 餐次归一化：早餐/早饭 → 早，午餐/中餐/午饭/中午 → 中，晚餐/晚饭 → 晚；其余（夜宵、加餐）返回 null */
function mealOf(raw) {
  const s = cellText(raw).replace(/[\s（）()]/g, '');
  if (!s) return null;
  if (s.indexOf('早') >= 0) return '早';
  if (s.indexOf('中') >= 0 || s.indexOf('午') >= 0) return '中';
  if (s.indexOf('晚') >= 0) return '晚';
  return null;
}

function supOf(it) { return cellText(it.supplier); }

function batchOf(it) { return cellText(it.batchNo) || '(未填批次)'; }

function who(it) {
  const item = cellText(it.itemName) || '未填品名';
  const day = cellText(it.date) || '未填日期';
  const meal = cellText(it.meal);
  return `第 ${it.line} 行「${item}（${day}${meal ? ' ' + meal : ''}）」`;
}

function finding(level, category, it, diff, message, advice) {
  const f = { level, category, line: it.line, raw: it.raw, message };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

/* ============================ 免费档检查（六项） ============================ */

/** 1. 进货数量勾稽：入库数量 = 采购数量 − 退货数量（逐行，按批次） */
function checkQtyReconcile(items) {
  const out = [];
  for (const it of items) {
    const p = normNumber(it.purchaseQty);
    const r = normNumber(it.returnQty);
    const s = normNumber(it.stockQty);
    if (p === null || r === null || s === null) continue;      // 缺失 / 认不出交给「必需字段」那一项
    const expect = round2(p - r);
    const diff = round2(s - expect);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding('P0', '进货数量勾稽不符', it, diff,
      `${who(it)}：批次「${batchOf(it)}」采购数量 ${qtyText(p)} − 退货数量 ${qtyText(r)} = ${qtyText(expect)}，`
      + `但入库数量登记为 ${qtyText(s)}，差 ${qtyText(diff)}。原文：${it.raw}`,
      '按批次拿送货单与退货单对一遍：退货没从入库里减掉、或入库按毛重登记都会造成这个差；'
      + '本工具只列出差额，不认定是哪一种原因。'));
  }
  return out;
}

/** 2. 进货金额勾稽：单价 × 入库数量 + 运费 = 金额（运费列空或为 0 时按 单价 × 入库数量 勾稽） */
function checkAmountReconcile(items) {
  const out = [];
  for (const it of items) {
    const price = normNumber(it.unitPrice);
    const s = normNumber(it.stockQty);
    const amount = normNumber(it.amount);
    const freight = isBlank(it.freight) ? 0 : normNumber(it.freight);
    if (price === null || s === null || amount === null || freight === null) continue;
    const expect = round2(price * s + freight);
    const diff = round2(amount - expect);
    if (Math.abs(diff) < TOL) continue;
    const formula = `${money(price)} × ${qtyText(s)}${freight ? ` + 运费 ${money(freight)}` : ''}`;
    out.push(finding(diff > 0 ? 'P1' : 'P0', '进货金额勾稽不符', it, diff,
      `${who(it)}：${formula} = ${money(expect)}，但金额登记为 ${money(amount)}，差 ${money(diff)}。原文：${it.raw}`,
      '拿发票 / 送货单复算一遍：单价被四舍五入过、运费另计一列但没加进来、或金额按毛重数量算，都会造成这个差；'
      + '确认后只改登记值，别改原始票据。'));
  }
  return out;
}

/** 3. 留样餐次完整性：应留样餐次（早/中/晚 × 表中日期）= 实际留样条数，缺哪个日期加哪个餐次就点名 */
function checkMealCompleteness(items) {
  const out = [];
  const byDay = new Map();               // 当日毫秒 → {label, meals:Set, sample:行}
  for (const it of items) {
    const ms = parseDate(it.date);
    if (ms === null) continue;           // 日期认不出由「认不出格式」那一项点名
    if (!byDay.has(ms)) byDay.set(ms, { label: fmtDay(ms), meals: new Set(), sample: it });
    const meal = mealOf(it.meal);
    if (meal) byDay.get(ms).meals.add(meal);
  }
  for (const ms of [...byDay.keys()].sort((a, b) => a - b)) {
    const day = byDay.get(ms);
    for (const slot of MEAL_SLOTS) {
      if (day.meals.has(slot)) continue;
      const have = [...day.meals].join('、') || '(一条留样餐次都没登记)';
      out.push(finding('P1', '留样餐次缺失', day.sample, undefined,
        `${day.label} 缺「${slot}」餐次的留样记录 —— 该日应留样 ${MEAL_SLOTS.join('/')} 共 ${MEAL_SLOTS.length} 个餐次，`
        + `实际登记到的是 ${have}（${day.meals.size} 个餐次）。原文：${day.sample.raw}`,
        '每餐次的留样都要当餐登记（品名、留样量、留样时间、留样人），缺餐次直接就是整改项；'
        + '补登记时按当餐实际留样时刻写，不要事后统一补写成同一个时间。'));
    }
  }
  return out;
}

/** 4. 留样量达标：单份留样量 ≥ 该行登记的下限，低于即报（附原文） */
function checkSampleWeight(items) {
  const out = [];
  for (const it of items) {
    const w = normNumber(it.sampleQty);
    const min = normNumber(it.sampleMin);
    if (w === null || min === null) continue;
    if (w >= min - TOL) continue;
    out.push(finding('P0', '留样量低于下限', it, round2(w - min),
      `${who(it)}：留样量登记 ${qtyText(w)}g，低于该行登记的留样下限 ${qtyText(min)}g，少 ${qtyText(round2(min - w))}g。`
      + `原文：${it.raw}`,
      '留样量不足 125g 的样品在需要送检时分量不够，属于当场就能改的项：留样时用带刻度的容器按份称重，'
      + '不足的当餐重新留足并如实登记。'));
  }
  return out;
}

/** 5. 同一供货者 + 同一批次重复登记检测（重复出现即点名两处） */
function checkSupplierBatchDuplicate(items) {
  const out = [];
  const first = new Map();
  const reported = new Set();
  for (const it of items) {
    const sup = supOf(it);
    const batch = cellText(it.batchNo);
    if (!sup || !batch) continue;
    const key = `${sup}|${batch}`;
    if (first.has(key) && !reported.has(it.line)) {
      reported.add(it.line);
      const prev = first.get(key);
      out.push(finding('P1', '供货者批次重复登记', it, undefined,
        `${who(it)}：供货者「${sup}」+ 批次「${batch}」在第 ${prev.line} 行已经登记过（原文：${prev.raw}），`
        + `本行又登记了一次（原文：${it.raw}）—— 同一供货者同一批次出现两行。`,
        '同一批次只应有一条进货查验记录：拆行登记会把数量与金额重复计入月度合计，'
        + '先确认是抄重了还是同一批次分两次到货（分两次到货应补新的批次号或写明到货日期）。'));
    }
    if (!first.has(key)) first.set(key, it);
  }
  return out;
}

/** 6. 空白 / 占位符 / 认不出格式（必需字段、数值形态、日期与时间格式） */
function checkFieldIntegrity(items) {
  const out = [];
  for (const it of items) {
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        `${who(it)}：这些必需字段是空的或占位符 —— ${miss.join('、')}。原文：${it.raw}`,
        '空着的字段会让对应的核对整项做不了；补全后重跑，本工具不会替你猜一个默认值。'));
    }
    for (const [role, label] of NUMERIC_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        out.push(finding('P1', '数值无法解析', it, undefined,
          `${who(it)}：「${label}」的值「${cellText(raw)}」不是可识别的数值（只认数字、千分位、¥、括号负数）。原文：${it.raw}`,
          '把数量与金额改成纯数字形态（如 100、520.00）再跑；本工具不会把看不懂的值当成 0。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '数值为负', it, n,
          `${who(it)}：「${label}」是负数（${qtyText(n)}）—— 进货与留样类记录里出现负数通常是填反了方向或写成了红字冲销。原文：${it.raw}`,
          '确认是红字冲销还是填错方向；确属冲销的请写在备注列并保留原值，别直接改成正数。'));
      }
    }
    if (!isBlank(it.date) && parseDate(it.date) === null) {
      out.push(finding('P1', '日期时间格式无法识别', it, undefined,
        `${who(it)}：「日期」的值「${cellText(it.date)}」认不出（支持 2025-06-03 / 2025/6/3 / 2025年6月3日）。原文：${it.raw}`,
        '统一写成 2025-06-03 这种形态：日期认不出来的行不参与餐次完整性与消毒断档比对。'));
    }
    if (!isBlank(it.sampleTime) && parseDateTime(it.sampleTime) === null) {
      out.push(finding('P1', '日期时间格式无法识别', it, undefined,
        `${who(it)}：「留样时间」的值「${cellText(it.sampleTime)}」认不出（要写到分钟，如 2025-06-03 07:20）。原文：${it.raw}`,
        '留样时间必须写到分钟：只写日期没法核 48 小时保存时长；补全后再重跑。'));
    }
  }
  return out;
}

/* ===== 完整档（买断版）追加的检查实现 ===== */

/** 完整档①：留样保存时长 —— 留样时间到销毁 / 记录时间须 ≥ 48 小时 */
/** 完整档②：餐具消毒记录断档 —— 按表中日期序列（最早到最晚逐日）比对，缺哪一天点名哪一天 */
/** 完整档③：供货者证照有效期覆盖 —— 进货日期晚于许可证到期日即报（给两处原文） */
/** 完整档④：保质期与入库日期 —— 入库日期晚于保质期到期日即报（给两处原文） */
/** 完整档⑤：分供货者 × 分品类汇总清单（按问题数量从多到少排序，逐组给出可整改动作） */
/** 完整档⑤配套：跨供货者 / 跨品类的汇总台账 */
/** 完整档⑤配套：汇总整改清单（P0 在前，逐条给动作） */
/** 完整档补充：哪些行的付费检查因为原始信息没登记而没能核（如实列出，不静默放过） */
/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的食堂进货查验与留样记录核对表']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的食堂进货查验与留样记录核对表']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的食堂进货查验与留样记录核对表（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行记录明细（现在只有表头，没有可核对的明细行）']);
  }

  const findings = [];
  const notRun = [];

  for (const f of checkQtyReconcile(t.items)) findings.push(f);
  for (const f of checkAmountReconcile(t.items)) findings.push(f);
  const mealMissing = checkMealCompleteness(t.items);
  for (const f of mealMissing) findings.push(f);
  for (const f of checkSampleWeight(t.items)) findings.push(f);
  for (const f of checkSupplierBatchDuplicate(t.items)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const sampleRows = t.items.filter((it) => mealOf(it.meal) !== null).length;
  const dayCount = new Set(t.items.map((it) => parseDate(it.date)).filter((ms) => ms !== null)).size;

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      days: dayCount,
      sample_rows: sampleRows,
      sample_slots_expected: dayCount * MEAL_SLOTS.length,
      sample_slots_missing: mealMissing.length,
      purchase_total: t.totals.purchaseQty,
      return_total: t.totals.returnQty,
      stock_total: t.totals.stockQty,
      amount_total: t.totals.amount,
      sample_weight_total: t.totals.sampleQty,
      basis: '入库数量 = 采购数量 − 退货数量（逐行按批次）；单价 × 入库数量 + 运费 = 金额；'
        + '应留样餐次 = 表中日期 × 早/中/晚，每个餐次都要有留样记录；单份留样量须 ≥ 留样下限列登记的下限；'
        + '同一供货者 + 同一批次只应登记一次；13 个必需列缺一列即材料不足、不给结论。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的口径算得对、餐次与日期点到的都在**，'
      + '不代表食堂实际操作合规、留样实物真实存在、消毒工艺达标，也不代表监管检查已经过关 —— 那些不在本工具范围内。';
  }

  const scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.items.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    days: dayCount,
    sample_slots_expected: dayCount * MEAL_SLOTS.length,
    sample_slots_missing: mealMissing.length,
    qty_diff_rows: findings.filter((f) => f.category === '进货数量勾稽不符').length,
    amount_diff_rows: findings.filter((f) => f.category === '进货金额勾稽不符').length,
    amount_total: t.totals.amount,
    stock_total: t.totals.stockQty,
    sample_weight_total: t.totals.sampleQty,
  };
  result.scope = scope;



  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
