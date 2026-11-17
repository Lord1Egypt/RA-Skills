#!/usr/bin/env node
/**
 * chemical-inventory-check.js —— 危险化学品出入库与领用台账核对（**免费档**；确定性、纯 Node 标准库）。
 *
 * 真实痛点：危化品（含易制爆 / 易制毒）必须建**出入库台账与领用记录**，做到「双人收发、双人记账、账物相符」，
 * 并每月与仓库盘点、领用单、MSDS / 安全标签、储存条件记录对上；对不上就是**重大隐患**（应急管理部门检查项）。
 * 财务 / 安环 / 库管每个月都要核这几件事：数量勾稽、领用与退库、账实差异、超期复检、超量储存。
 *
 * ⚠️ 本文件是 **免费档子集**：只实现下面这六项**表内逐行算术与列间勾稽**；
 *    **完整档的实现不在这个包里** —— 超量储存、复检/有效期到期、双人复核缺失、
 *    储存条件记录缺失与台账期间不连续、分品名×分仓库汇总清单都不在这里。
 *    `CHECKS_WITHHELD` 只是「未执行的检查项」的**说明文本**，不是实现。
 *    本版本**只做**表内数量与金额的复算与勾稽，**不做**实物、安全设施、储存场所与证件资质的判定。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定实物是否真的与台账相符、不判定该品种是否属于危化品/易制爆/易制毒或是否需备案、
 *          不判定储存场所与安全设施是否达标、不判定 MSDS / 安全标签的文字内容是否合规、
 *          不读 .xlsx/.pdf 原件、不联网核验许可证与备案证明真伪；材料不足**一律不给结论**。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '数量勾稽：期初库存 + 本期入库 − 本期出库 = 期末库存（逐行按 品名+规格 复算，差额不为零即列出并给差额）',
  '账实核对：期末库存（账）vs 盘点实存（实），逐行给出差额与差异率',
  '领用与退库勾稽：领用量 − 退库量 = 实际消耗（表里没有「实际消耗」列时对「本期出库」，逐行）',
  '重复登记检测：同一 品名 + 同一 批次 + 同一 日期 登记两次即点名（并点出前一行行号）',
  '合计行逐列复核：合计/小计行的每个数量列与金额列都要等于明细行之和（逐列点名差在哪一列）',
  '空白/占位符/数值格式/负数检测：必需列空白或写成占位符、数值认不出、库存/数量/金额为负',
];

const CHECKS_WITHHELD = [
  '超量储存：单一品种期末库存 > 许可/规定上限（需表里有「许可上限」列）⇒ 报出超出量',
  '复检/有效期到期：按「有效期至」列判断已过期或 30 天内到期（基准日取台账最后一条业务日期）',
  '双人复核缺失：收发人或记账人列为空、或同一人既收发又记账',
  '储存条件记录缺失（温湿度/隔离要求列）与台账期间不连续检测',
  '分品名×分仓库汇总清单（按差异量排序，给出可整改动作）',
];

const OUT_OF_SCOPE = [
  '判定实物是否真的与台账相符（盘点过程本身是否真实、实物的称量与计量误差）—— 那是现场盘点与监盘的职责，'
    + '本工具只核表内数字与列间勾稽',
  '判定该品种是否属于危险化学品 / 易制爆 / 易制毒、是否需要备案或购买许可 —— 那是应急管理与公安部门的认定权',
  '判定储存场所的消防、防爆、防泄漏、防静电等安全设施是否达标（那是安全评价与现场检查的职责）',
  '判定 MSDS / 安全标签的文字内容是否合规、是否与实际理化性质一致',
  '读取 .xlsx / .pdf 原件或扫描的领用单签字，绝不联网核验许可证与备案证明真伪，也不替代安全评价报告',
];

// 样例：一张**干净**的危化品月度出入库与领用台账 —— 4 个品种、2 个仓库 + 1 个易制爆专柜，
// 数量勾稽逐行平、账实相符、领用量减退库量等于实际消耗、合计行逐列对得上、
// 收发人与记账人是两个不同的人、储存条件与有效期都填了、期末库存都没超过许可上限、期间连续。
const SAMPLE_TEXT = [
  '品名\t规格\t批次\t单位\t期初库存\t本期入库\t本期出库\t期末库存\t盘点实存\t领用量\t退库量\t实际消耗\t入库金额\t结存金额\t日期\t仓库\t收发人\t记账人\t储存条件记录\t有效期至\t许可上限\t备注',
  '丙酮\tAR分析纯\tB20260112\tL\t120.00\t80.00\t90.00\t110.00\t110.00\t96.00\t6.00\t90.00\t5600.00\t7700.00\t2026-03-04\t甲类危化品库\t顾明远\t沈书言\t温度15-25℃ 湿度≤75% 与氧化剂隔离\t2026-11-30\t500.00\t3月领用单96L 退库6L',
  '硝酸（68%）\t工业级\tB20260206\tkg\t300.00\t200.00\t150.00\t350.00\t350.00\t150.00\t0.00\t150.00\t4200.00\t9800.00\t2026-03-09\t乙类危化品库\t顾明远\t沈书言\t温度≤30℃ 通风 与有机物隔离\t2026-09-15\t800.00\t3月领用单150kg',
  '高锰酸钾\tAR分析纯\tB20260120\tkg\t40.00\t20.00\t25.00\t35.00\t35.00\t27.00\t2.00\t25.00\t1360.00\t2380.00\t2026-03-17\t易制爆专柜\t岑亦然\t沈书言\t双人双锁 温度15-25℃ 单独存放\t2026-08-31\t200.00\t易制爆备案 双人收发 收发与记账非同一人',
  '乙醚\tAR分析纯\tB20260211\tL\t60.00\t40.00\t45.00\t55.00\t55.00\t45.00\t0.00\t45.00\t2250.00\t2750.00\t2026-03-23\t甲类危化品库\t顾明远\t沈书言\t温度≤25℃ 防静电 与氧化剂隔离\t2026-10-31\t300.00\t3月领用单45L',
  '合计\t—\t—\t—\t520.00\t340.00\t310.00\t550.00\t550.00\t318.00\t8.00\t310.00\t13410.00\t22630.00\t—\t—\t—\t—\t—\t—\t—\t合计行只参与合计行复核 不参与逐行勾稽',
].join('\n');

const TOL = 0.01;

// 表头级必需列（缺任何一列 ⇒ 材料不足，绝不给结论）
const REQUIRED_ROLES = ['name', 'spec', 'batch', 'unit', 'opening', 'inbound', 'outbound', 'closing',
  'counted', 'requisition', 'returned', 'date'];

// 单元格级必需字段（空白 / 占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['name', '品名'],
  ['spec', '规格'],
  ['batch', '批次'],
  ['unit', '单位'],
  ['opening', '期初库存'],
  ['inbound', '本期入库'],
  ['outbound', '本期出库'],
  ['closing', '期末库存'],
  ['counted', '盘点实存'],
  ['requisition', '领用量'],
  ['returned', '退库量'],
  ['date', '日期'],
];

// 数值列（用于「认不出 / 为负」判定）与各自的负数口径
const NUM_FIELDS = [
  ['opening', '期初库存'],
  ['inbound', '本期入库'],
  ['outbound', '本期出库'],
  ['closing', '期末库存'],
  ['counted', '盘点实存'],
  ['requisition', '领用量'],
  ['returned', '退库量'],
  ['consumed', '实际消耗'],
  ['amountIn', '入库金额'],
  ['amountBalance', '结存金额'],
];
const STOCK_ROLES = ['opening', 'closing', 'counted'];                              // 负数 ⇒ 负库存
const FLOW_ROLES = ['inbound', 'outbound', 'requisition', 'returned', 'consumed'];  // 负数 ⇒ 数量为负
const AMOUNT_ROLES = ['amountIn', 'amountBalance'];                                 // 负数 ⇒ 金额为负

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面（本仓库踩过六次）。
//    这里的顺序有三处是真实会踩的坑，不要"顺手整理"：
//      · 「入库金额 / 结存金额」必须排在「入库 / 期末」**前面**，否则「入库金额」会被「入库」抢走；
//      · 「有效期至」必须排在「日期」**前面**，否则「复检日期」会被「日期」抢走；
//      · 「仓库」必须排在「名称」**前面**，否则「仓库名称」会被当成品名。
const ROLES = {
  warehouse: ['仓库', '库房', '储存场所', '库位'],
  name: ['品名', '物料名称', '化学品名称', '危化品名称', '名称'],
  spec: ['规格', '型号', '牌号', '等级'],
  batch: ['批次', '批号', '生产批号'],
  unit: ['计量单位', '单位'],
  amountIn: ['本期入库金额', '入库金额', '采购金额'],
  amountBalance: ['期末结存金额', '结存金额', '库存金额', '期末金额'],
  opening: ['期初库存', '期初结存', '上月结存', '期初数量', '期初'],
  inbound: ['本期入库量', '本期入库', '入库数量', '入库'],
  outbound: ['本期出库量', '本期出库', '出库数量', '出库'],
  closing: ['期末库存', '期末结存', '期末数量', '期末'],
  counted: ['盘点实存', '盘点数量', '实盘数量', '实存数量', '盘点', '实存'],
  requisition: ['领用量', '领用数量', '领用'],
  returned: ['退库量', '退库数量', '退回数量', '退库', '退回'],
  consumed: ['实际消耗', '净领用', '消耗量', '实耗量', '实际使用量'],
  expiry: ['有效期至', '有效期止', '到期日', '复检日期', '有效期'],
  limitQty: ['许可上限', '规定上限', '储存上限', '最大储存量', '许可储存量', '核定储量', '上限', '限额'],
  storageCond: ['储存条件记录', '储存条件', '温湿度记录', '温湿度', '隔离要求', '储存要求'],
  issuer: ['收发人', '保管员', '库管员', '发料人', '入库人', '经手人'],
  bookkeeper: ['记账人', '记账员', '台账登记人', '登记人', '复核人'],
  date: ['日期', '年月', '月份'],
  note: ['备注', '说明', '附注'],
};

const LABELS = {
  warehouse: '仓库',
  name: '品名',
  spec: '规格',
  batch: '批次',
  unit: '单位',
  amountIn: '入库金额',
  amountBalance: '结存金额',
  opening: '期初库存',
  inbound: '本期入库',
  outbound: '本期出库',
  closing: '期末库存',
  counted: '盘点实存',
  requisition: '领用量',
  returned: '退库量',
  consumed: '实际消耗',
  expiry: '有效期至',
  limitQty: '许可上限',
  storageCond: '储存条件记录',
  issuer: '收发人',
  bookkeeper: '记账人',
  date: '日期',
  note: '备注',
};

const SUM_ROLES = ['opening', 'inbound', 'outbound', 'closing', 'counted', 'requisition', 'returned',
  'consumed', 'amountIn', 'amountBalance'];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张表补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「账物相符」，也不说「对不上」。',
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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定|待核|暂缺)$/i.test(s);
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

/** 「合计 / 总计 / 小计」行：只参与合计行复核，不参与逐行勾稽（否则合计会被当成一条明细再算一遍） */
function isTotalRow(it) {
  const n = String(it && it.name == null ? '' : it.name).replace(/\s/g, '');
  return /合计|总计|小计|共计/.test(n);
}

/** 解析成 {header, cols, items, totals, missingRoles, missingColumns, error}；行是**扁平**对象：{line, raw, isTotal, 角色:值…} */
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
    it.isTotal = isTotalRow(it);
    items.push(it);
  }

  const missingRoles = REQUIRED_ROLES.filter((r) => !cols.some((c) => c.role === r));
  const totals = {};
  for (const role of SUM_ROLES) {
    totals[role] = round2(items.reduce((acc, it) => {
      if (it.isTotal) return acc;                      // 明细行之和，不要把合计行再加一遍
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

/** 数量：整数不拖两位小数，带千分位 */
function qty(n) {
  const v = Math.abs(n) < 0.005 ? 0 : round2(n);
  return v.toFixed(2).replace(/\.00$/, '').replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

function money(n) {
  const v = Math.abs(n) < 0.005 ? 0 : n;
  return v.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

const fmtByRole = (role, n) => (AMOUNT_ROLES.indexOf(role) >= 0 ? money(n) : qty(n));

function unitOf(it) {
  const u = String(it.unit == null ? '' : it.unit).trim();
  return isBlank(u) ? '' : u;
}

function qn(it, n) {
  const u = unitOf(it);
  return u ? `${qty(n)} ${u}` : qty(n);
}

function rawOf(it, role) {
  const v = it[role];
  if (v === undefined || v === null) return '(该列不存在)';
  const s = String(v).trim();
  return s === '' ? '(空)' : s;
}

function who(it) {
  const name = String(it.name == null ? '' : it.name).trim();
  const spec = String(it.spec == null ? '' : it.spec).trim();
  const batch = String(it.batch == null ? '' : it.batch).trim();
  const tag = [name, spec, batch].filter((x) => x && !isBlank(x)).join(' / ');
  return `第 ${it.line} 行「${tag || '未填品名'}」`;
}

function finding(level, category, it, diff, message, advice) {
  const f = { level, category, line: it.line, message };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

/** 表里实际出现了哪些角色 —— 「列不在表里」与「这一格是空的」是两件事，要分开处理 */
function presentRoles(items) {
  const s = new Set();
  for (const it of items) for (const k of Object.keys(it)) s.add(k);
  return s;
}

/* ============================ 免费档检查（六项） ============================ */

/** 1. 数量勾稽：期初库存 + 本期入库 − 本期出库 = 期末库存（逐行按 品名+规格 复算） */
function checkQuantityIdentity(items) {
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const o = normNumber(it.opening);
    const i = normNumber(it.inbound);
    const ou = normNumber(it.outbound);
    const c = normNumber(it.closing);
    if (o === null || i === null || ou === null || c === null) continue;   // 缺失 / 认不出交给第 6 项
    const expect = round2(o + i - ou);
    const diff = round2(c - expect);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding('P0', '数量勾稽不平', it, diff,
      `${who(it)}：期初库存 ${qn(it, o)} + 本期入库 ${qn(it, i)} − 本期出库 ${qn(it, ou)} = ${qn(it, expect)}，`
      + `台账「期末库存」写的是 ${qn(it, c)}，差 ${qn(it, diff)}（原文第 ${it.line} 行：${it.raw}）。`,
      '先查是不是漏记了一次出入库（单据在、台账没记），再查期末库存是不是抄错；'
      + '这条式子是账内外平衡的唯一算术依据，不要用「盘点实存」去倒推期末库存。'));
  }
  return out;
}

/** 2. 账实核对：期末库存（账）vs 盘点实存（实），给出差额与差异率 */
function checkBookVsCount(items) {
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const c = normNumber(it.closing);
    const k = normNumber(it.counted);
    if (c === null || k === null) continue;
    const diff = round2(k - c);                        // 盘盈为正、盘亏为负
    if (Math.abs(diff) < TOL) continue;
    const rate = c === 0 ? null : round2((diff / c) * 100);
    const f = finding('P0', '账实不符', it, diff,
      `${who(it)}：期末库存（账）${qn(it, c)}，盘点实存（实）${qn(it, k)}，`
      + `差异 ${qn(it, diff)}${diff > 0 ? '（盘盈）' : '（盘亏）'}，`
      + `差异率 ${rate === null ? '无法计算（账面为 0）' : `${rate}%`}（原文第 ${it.line} 行：${it.raw}）。`,
      '账实不符是检查项也是重大隐患：先复称实物、再逐张核对本期出入库单据与领用单；'
      + '盘盈盘亏要按制度走审批并留痕，不要直接把账面改成实盘数把差异抹平。');
    f.diff_rate = rate;
    out.push(f);
  }
  return out;
}

/** 3. 领用与退库勾稽：领用量 − 退库量 = 实际消耗（没有该列时对「本期出库」） */
function checkRequisitionReturn(items) {
  const out = [];
  const hasConsumed = items.some((it) => !it.isTotal && it.consumed !== undefined);
  const targetName = hasConsumed ? '实际消耗' : '本期出库';
  for (const it of items) {
    if (it.isTotal) continue;
    const req = normNumber(it.requisition);
    const ret = normNumber(it.returned);
    if (req === null || ret === null) continue;
    const net = round2(req - ret);
    const target = hasConsumed ? normNumber(it.consumed) : normNumber(it.outbound);
    if (target === null) continue;
    const diff = round2(net - target);
    if (Math.abs(diff) < TOL) continue;
    const over = net < 0;
    out.push(finding(over ? 'P0' : 'P1', '领用退库与消耗不符', it, diff,
      `${who(it)}：领用量 ${qn(it, req)} − 退库量 ${qn(it, ret)} = ${qn(it, net)}，`
      + (over
        ? `退库量比领用量还多 ${qn(it, -net)} —— 同一行里领用与退库在算术上就不成立；`
        : `台账上「${targetName}」写的是 ${qn(it, target)}，差 ${qn(it, diff)}；`)
      + `（原文第 ${it.line} 行：${it.raw}）。`,
      `领用单与退库单要逐张对：领用量减退库量才是实际消耗，退库应冲减消耗而不是当成新的入库；`
      + `先查是不是有一张退库单没登记，或「${targetName}」那一列串行抄错。`));
  }
  return out;
}

/** 4. 重复登记：同一 品名 + 同一 批次 + 同一 日期 出现两次 */
function checkDuplicateEntry(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    if (it.isTotal) continue;
    const name = String(it.name == null ? '' : it.name).trim();
    const batch = String(it.batch == null ? '' : it.batch).trim();
    const date = String(it.date == null ? '' : it.date).trim();
    if (!name || isBlank(batch) || isBlank(date)) continue;   // 缺字段交给第 6 项，不在这里瞎猜
    const key = `${name}|${batch}|${date}`;
    if (seen.has(key)) {
      out.push(finding('P0', '重复登记', it, undefined,
        `${who(it)}：品名「${name}」+ 批次「${batch}」+ 日期「${date}」在第 ${seen.get(key)} 行已经登记过一次 —— `
        + `同一天同一批次重复登记（原文第 ${it.line} 行：${it.raw}）。`,
        '同一天同一批次的出入库应合并成一行，或分行但用单据号区分并在备注里写明；'
        + '重复登记会把数量勾稽、账实合计与领用合计全都多算一遍。'));
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

/** 5. 合计行逐列复核：数量列与金额列都要等于明细行之和 */
function checkTotalRows(items) {
  const out = [];
  const totalRows = items.filter((it) => it.isTotal);
  if (!totalRows.length) return out;
  const detail = items.filter((it) => !it.isTotal);
  const present = presentRoles(detail);
  const roles = SUM_ROLES.filter((r) => present.has(r));
  for (const tr of totalRows) {
    for (const role of roles) {
      const label = LABELS[role] || role;
      const expected = round2(detail.reduce((acc, it) => {
        const n = normNumber(it[role]);
        return acc + (n === null ? 0 : n);
      }, 0));
      const actual = normNumber(tr[role]);
      if (actual === null) {
        if (isBlank(tr[role]) && Math.abs(expected) < TOL) continue;   // 明细全为 0、合计行留空 ⇒ 不算错
        out.push(finding('P1', '合计行不平', tr, undefined,
          `第 ${tr.line} 行「合计」的「${label}」是空的或认不出（原文「${rawOf(tr, role)}」），`
          + `明细行之和应是 ${fmtByRole(role, expected)}（原文第 ${tr.line} 行：${tr.raw}）。`,
          '合计行每个数量列与金额列都要写数：留空或写「—」时本工具无法复核合计，只能如实报出来。'));
        continue;
      }
      const diff = round2(actual - expected);
      if (Math.abs(diff) < TOL) continue;
      out.push(finding('P1', '合计行不平', tr, diff,
        `第 ${tr.line} 行「合计」的「${label}」写的是 ${fmtByRole(role, actual)}，`
        + `明细行之和是 ${fmtByRole(role, expected)}，差 ${fmtByRole(role, diff)}（原文第 ${tr.line} 行：${tr.raw}）。`,
        '合计行要按明细行重算：漏一行、多一行、或把「盘点实存」混进「期末库存」都会在这里露出来；'
        + '数量列与金额列都要对。'));
    }
  }
  return out;
}

/** 6. 空白 / 占位符 / 数值格式 / 负数 */
function checkFieldIntegrity(items) {
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        `${who(it)}：这些必需列是空的或写成了占位符 —— ${miss.join('、')}（原文第 ${it.line} 行：${it.raw}）。`,
        '空着的列会让对应的核对整项做不了（数量勾稽、账实核对、领用退库、重复登记都依赖它们）；'
        + '补全后重跑，本工具不会替你猜一个默认值。'));
    }
    for (const [role, label] of NUM_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        out.push(finding('P1', '数值无法解析', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的数值（只认数字、千分位、`
          + `货币符号、括号负数与结尾的 %）（原文第 ${it.line} 行：${it.raw}）。`,
          '把这一格改成纯数字形态（如 120 或 120.00）再跑；本工具不会把看不懂的值当成 0。'));
        continue;
      }
      if (n < 0) {
        const cat = STOCK_ROLES.indexOf(role) >= 0 ? '负库存'
          : (FLOW_ROLES.indexOf(role) >= 0 ? '数量为负' : '金额为负');
        out.push(finding('P0', cat, it, n,
          `${who(it)}：「${label}」是负数（${fmtByRole(role, n)}）—— 危化品台账里出现负数，通常是填反了方向、`
          + `写成红字冲销，或把退库记成了负入库（原文第 ${it.line} 行：${it.raw}）。`,
          '确属红字冲销的请在备注里写明并保留原值；数量与库存列正常不应为负，先查这一格是不是抄串了行。'));
      }
    }
  }
  return out;
}

/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的危险化学品出入库与领用台账（含仓库盘点与领用记录）']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的危险化学品出入库与领用台账（含仓库盘点与领用记录）']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的危险化学品出入库与领用台账（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行台账明细（现在只有表头，没有可核对的明细行）']);
  }

  const findings = [];
  const notRun = [];

  for (const f of checkQuantityIdentity(t.items)) findings.push(f);
  for (const f of checkBookVsCount(t.items)) findings.push(f);
  for (const f of checkRequisitionReturn(t.items)) findings.push(f);
  for (const f of checkDuplicateEntry(t.items)) findings.push(f);
  for (const f of checkTotalRows(t.items)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

  // 免费档：完整档那五类检查一项都不执行，这里如实记下来（只记「没做」，不会伪造结论）
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const detail = t.items.filter((it) => !it.isTotal);
  const totals = t.totals;
  const countDiff = round2(totals.counted - totals.closing);

  const result = {
    findings,
    summary: {
      rows: detail.length,
      total_rows: t.items.length - detail.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      opening_total: totals.opening,
      inbound_total: totals.inbound,
      outbound_total: totals.outbound,
      closing_total: totals.closing,
      counted_total: totals.counted,
      requisition_total: totals.requisition,
      returned_total: totals.returned,
      consumed_total: totals.consumed,
      amount_in_total: totals.amountIn,
      amount_balance_total: totals.amountBalance,
      count_diff_total: countDiff,
      basis: '期初库存 + 本期入库 − 本期出库 = 期末库存（逐行复算）；期末库存应与盘点实存对上'
        + '（差异 = 盘点实存 − 期末库存，差异率 = 差异 ÷ 期末库存）；领用量 − 退库量 = 实际消耗'
        + '（表里没有「实际消耗」列时对「本期出库」）；同一 品名+批次+日期 只能登记一次；'
        + '合计 / 小计行的数量列与金额列必须等于明细行之和；必需列空白、写成占位符、认不出的数值或负数都逐行点名。'
        + '「合计」行只参与合计行复核，不参与逐行勾稽。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得对、必需列都填了、'
      + '合计行复算一致**，不代表实物与台账真的相符、也不代表安全设施、储存场所、MSDS 与安全标签内容已经过关 —— '
      + '那些不在本工具范围内。';
  }

  const scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: detail.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    closing_total: totals.closing,
    counted_total: totals.counted,
    count_diff_total: countDiff,
    requisition_total: totals.requisition,
    returned_total: totals.returned,
    consumed_total: totals.consumed,
  };
  result.scope = scope;

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
  CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
