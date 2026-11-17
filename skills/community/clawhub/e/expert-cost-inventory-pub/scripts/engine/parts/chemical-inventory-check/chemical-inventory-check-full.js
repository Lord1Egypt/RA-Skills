#!/usr/bin/env node
/**
 * chemical-inventory-check-full.js —— 危险化学品出入库与领用台账核对（确定性、纯 Node 标准库）。
 *
 * 真实痛点：危化品（含易制爆 / 易制毒）必须建**出入库台账与领用记录**，做到「双人收发、双人记账、账物相符」，
 * 并每月与仓库盘点、领用单、MSDS / 安全标签、储存条件记录对上；对不上就是**重大隐患**（应急管理部门检查项）。
 * 财务 / 安环 / 库管每个月都要核这几件事：数量勾稽、领用与退库、账实差异、超期复检、超量储存。
 *
 * 本文件是**订阅版（买断版）**：在本包六项逐行核对之上，多出**超量储存、复检/有效期到期、
 * 双人复核缺失、储存条件记录缺失与台账期间不连续、分品名×分仓库汇总清单**这五类能力。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定实物是否真的与台账相符、不判定该品种是否属于危化品/易制爆/易制毒或是否需备案、
 *          不判定储存场所与安全设施是否达标、不判定 MSDS / 安全标签的文字内容是否合规、
 *          不读 .xlsx/.pdf 原件、不联网核验许可证与备案证明真伪；材料不足**一律不给结论**。
 *
 * ⚠️ 付费项用**形态 B**：付费开关**只在入口 `run` 里声明一次**，付费检查一律包在 `if (开关) { … }` 块里。
 *    写注释时**不要复述**开关那一行的源码 —— 残渣断言是**纯字符串包含**判断，复述会被判「没删干净」。
 *    免费包由 `tools/strip_free_engine.py` 从本文件摘出（付费实现必须整块包在开关块里，不要另加 MARKER，
 *    两个形态同时存在时摘除工具会走另一条分支，把免费检查也一起删掉）。
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

/* ============================ 日期工具（付费项用） ============================ */

const DAY_MS = 86400000;

function parseDate(v) {
  const s = String(v == null ? '' : v).trim();
  if (!s) return null;
  const m = /^(\d{4})\s*[-/.年]\s*(\d{1,2})\s*[-/.月]\s*(\d{1,2})\s*日?/.exec(s);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  return Date.UTC(y, mo - 1, d);
}

const daysBetween = (a, b) => Math.round((b - a) / DAY_MS);

function fmtDate(ms) {
  const d = new Date(ms);
  const p = (x) => (x < 10 ? `0${x}` : String(x));
  return `${d.getUTCFullYear()}-${p(d.getUTCMonth() + 1)}-${p(d.getUTCDate())}`;
}

/**
 * 基准日：优先用调用方给的 asOf；否则取**台账里最后一条业务日期**。
 * 刻意不取「运行当天」：那会让同一张表今天报 30 天内到期、明天报已过期，结论每天都在变。
 */
function resolveBaseDate(items, p) {
  const fromPayload = parseDate(p && p.asOf);
  if (fromPayload !== null) return fromPayload;
  let max = null;
  for (const it of items) {
    if (it.isTotal) continue;
    const t = parseDate(it.date);
    if (t !== null && (max === null || t > max)) max = t;
  }
  return max;
}

/** 表里实际出现了哪些角色 —— 「列不在表里」与「这一格是空的」是两件事，要分开处理 */
function presentRoles(items) {
  const s = new Set();
  for (const it of items) for (const k of Object.keys(it)) s.add(k);
  return s;
}

/* ============================ 本包检查（六项） ============================ */

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

/* ==================== 以下只在订阅版（付费开关块）里执行 ==================== */

/** 付费项 1：超量储存 —— 单一品种期末库存 > 许可/规定上限 */
function checkStorageLimit(it, present) {
  const out = [];
  if (!present.has('limitQty')) return out;
  const limit = normNumber(it.limitQty);
  const close = normNumber(it.closing);
  if (limit === null) {
    out.push(finding('P1', '超量储存', it, undefined,
      `${who(it)}：「${LABELS.limitQty}」是空的或认不出（原文「${rawOf(it, 'limitQty')}」）—— `
      + `本行是否超量无法判定（原文第 ${it.line} 行：${it.raw}）。`,
      '把该品种批文 / 备案上的许可储存量填到「许可上限」列（单位要与库存一致）；'
      + '上限是判定超量的唯一依据，本工具不会替你套一个默认上限。'));
    return out;
  }
  if (close === null) return out;                       // 期末库存缺失交给「关键字段缺失」
  if (close <= limit + TOL) return out;
  const over = round2(close - limit);
  out.push(finding('P0', '超量储存', it, over,
    `${who(it)}：期末库存 ${qn(it, close)} 超过许可/规定上限 ${qn(it, limit)}，超出 ${qn(it, over)}`
    + `（原文第 ${it.line} 行：${it.raw}）。`,
    '超量储存是检查项也是重大隐患：先按领用 / 调拨把库存降到限额以内，再核对「许可上限」是不是该品种'
    + '现行批文上的储存量（单位、混存与隔离要求一起看）。'));
  return out;
}

/** 付费项 2：复检 / 有效期到期 —— 已过期或 30 天内到期 */
function checkExpiry(it, baseDate, present) {
  const out = [];
  if (!present.has('expiry')) return out;
  const raw = rawOf(it, 'expiry');
  const exp = parseDate(it.expiry);
  if (exp === null) {
    out.push(finding('P1', '复检有效期到期', it, undefined,
      `${who(it)}：「${LABELS.expiry}」是空的或认不出（原文「${raw}」）—— 这一批是否已过期、是否需要复检`
      + `无法判定（原文第 ${it.line} 行：${it.raw}）。`,
      '填上批次的有效期至（或复检日期）：化学品过期与超期未复检都是检查项，没有这一列就无法判断。'));
    return out;
  }
  if (baseDate === null) return out;                    // 基准日取不到 ⇒ 本项不做（run 里会如实记进 checks_notes）
  const left = daysBetween(baseDate, exp);
  if (left < 0) {
    out.push(finding('P0', '复检有效期到期', it, left,
      `${who(it)}：${LABELS.expiry} ${fmtDate(exp)} 已过期 ${qty(-left)} 天`
      + `（基准日 ${fmtDate(baseDate)}，取台账最后一条业务日期）（原文第 ${it.line} 行：${it.raw}）。`,
      '过期的化学品要立即隔离并按危废 / 报废流程处置，台账上标明处置单据号；'
      + '处置前不得再领用，也不得与合格批次混放。'));
  } else if (left <= 30) {
    out.push(finding('P1', '复检有效期到期', it, left,
      `${who(it)}：${LABELS.expiry} ${fmtDate(exp)}，距基准日 ${fmtDate(baseDate)} 只剩 ${left} 天 —— `
      + `30 天内到期，要安排复检或先行处置（原文第 ${it.line} 行：${it.raw}）。`,
      '列入本月待办：能复检的安排复检并更新有效期，不能复检的在到期前完成退库 / 处置，别等过期了再补记录。'));
  }
  return out;
}

/** 付费项 3：双人复核缺失 —— 收发人 / 记账人为空，或同一人既收发又记账 */
function checkDualSignOff(it, present) {
  const out = [];
  const hasIssuer = present.has('issuer');
  const hasBook = present.has('bookkeeper');
  if (!hasIssuer && !hasBook) return out;
  const issuer = String(it.issuer == null ? '' : it.issuer).trim();
  const book = String(it.bookkeeper == null ? '' : it.bookkeeper).trim();
  const miss = [];
  if (hasIssuer && isBlank(issuer)) miss.push(LABELS.issuer);
  if (hasBook && isBlank(book)) miss.push(LABELS.bookkeeper);
  if (miss.length) {
    out.push(finding('P1', '双人复核缺失', it, undefined,
      `${who(it)}：${miss.join('、')}一栏是空的（原文第 ${it.line} 行：${it.raw}）—— `
      + '危化品出入库与领用要求「双人收发、双人记账」，缺一个签字人这条记录就不成立。',
      '按双人收发 / 双人记账补齐两个签字人（收发人与记账人必须是两个人），'
      + '并在领用单、出库单上留同一对签名；本工具只核表里的姓名列，不核实物签字。'));
    return out;
  }
  if (hasIssuer && hasBook && issuer === book) {
    out.push(finding('P0', '双人复核缺失', it, undefined,
      `${who(it)}：收发人与记账人是同一个人（「${issuer}」）—— 双人复核在这条记录上不成立`
      + `（原文第 ${it.line} 行：${it.raw}）。`,
      '换一个人记账或复核；同一个人既收发又记账，检查时按「双人复核缺失」认定，等于这条台账没有复核。'));
  }
  return out;
}

/** 付费项 4a：储存条件记录缺失（温湿度 / 隔离要求列） */
function checkStorageCondition(it, present) {
  const out = [];
  if (!present.has('storageCond')) return out;
  if (!isBlank(it.storageCond)) return out;
  out.push(finding('P1', '储存条件记录缺失', it, undefined,
    `${who(it)}：「${LABELS.storageCond}」一栏是空的（原文第 ${it.line} 行：${it.raw}）—— `
    + '温湿度、通风、隔离要求是要留痕的检查项，没有记录就无法证明按 MSDS / 安全标签的条件储存。',
    '按该品种的 MSDS / 安全标签写清温度湿度范围与隔离要求，并把本月的温湿度记录编号填进来；'
    + '条件不达标的要写明整改措施，不要留空。'));
  return out;
}

/** 付费项 4b：台账期间不连续 —— 相邻业务日期之间隔了超过 31 天 */
function checkPeriodContinuity(items) {
  const out = [];
  const rows = items
    .filter((it) => !it.isTotal)
    .map((it) => ({ it, t: parseDate(it.date) }))
    .filter((x) => x.t !== null);
  const uniq = [...new Set(rows.map((x) => x.t))].sort((a, b) => a - b);
  for (let i = 1; i < uniq.length; i++) {
    const gap = daysBetween(uniq[i - 1], uniq[i]);
    if (gap <= 31) continue;
    const prev = rows.find((x) => x.t === uniq[i - 1]);
    const cur = rows.find((x) => x.t === uniq[i]);
    out.push(finding('P1', '台账期间不连续', cur.it, gap,
      `${fmtDate(uniq[i - 1])}（第 ${prev.it.line} 行）到 ${fmtDate(uniq[i])}（第 ${cur.it.line} 行）`
      + `之间隔了 ${gap} 天，这 ${gap} 天里没有任何出入库 / 领用记录（原文第 ${cur.it.line} 行：${cur.it.raw}）。`,
      '要么这期间确实没有业务（请在备注里写明停用 / 停产期间），要么是漏记了整段台账；'
      + '漏记的期间要凭原始出入库单与领用单补记，别把「记录连续」当成「已经核对过」。'));
  }
  return out;
}

/** 付费项 5：分品名 × 分仓库汇总（按差异量排序） */
function bucketOf(it) {
  const name = String(it.name == null ? '' : it.name).trim() || '(未填品名)';
  const spec = String(it.spec == null ? '' : it.spec).trim() || '(未填规格)';
  const wh = String(it.warehouse == null ? '' : it.warehouse).trim() || '(未填仓库)';
  return { name, spec, warehouse: wh, key: `${name}|${spec}|${wh}` };
}

function buildRollup(items, present) {
  const detail = items.filter((it) => !it.isTotal);
  const fresh = () => ({
    rows: 0, opening: 0, inbound: 0, outbound: 0, closing: 0, counted: 0,
    requisition: 0, returned: 0, consumed: 0, amount_in: 0, amount_balance: 0,
    count_diff: 0, over_limit: 0,
  });
  const add = (b, it) => {
    b.rows += 1;
    b.opening = round2(b.opening + num(it, 'opening'));
    b.inbound = round2(b.inbound + num(it, 'inbound'));
    b.outbound = round2(b.outbound + num(it, 'outbound'));
    b.closing = round2(b.closing + num(it, 'closing'));
    b.counted = round2(b.counted + num(it, 'counted'));
    b.requisition = round2(b.requisition + num(it, 'requisition'));
    b.returned = round2(b.returned + num(it, 'returned'));
    b.consumed = round2(b.consumed + num(it, 'consumed'));
    b.amount_in = round2(b.amount_in + num(it, 'amountIn'));
    b.amount_balance = round2(b.amount_balance + num(it, 'amountBalance'));
    const limit = normNumber(it.limitQty);
    const close = normNumber(it.closing);
    if (limit !== null && close !== null && close > limit + TOL) b.over_limit = round2(b.over_limit + (close - limit));
    b.count_diff = round2(b.counted - b.closing);      // 差异量 = 盘点实存 − 期末库存
    return b;
  };
  const byBucket = new Map();
  const byName = new Map();
  const byWarehouse = new Map();
  for (const it of detail) {
    const b = bucketOf(it);
    if (!byBucket.has(b.key)) {
      byBucket.set(b.key, Object.assign({ name: b.name, spec: b.spec, warehouse: b.warehouse }, fresh()));
    }
    if (!byName.has(b.name)) byName.set(b.name, fresh());
    if (!byWarehouse.has(b.warehouse)) byWarehouse.set(b.warehouse, fresh());
    add(byBucket.get(b.key), it);
    add(byName.get(b.name), it);
    add(byWarehouse.get(b.warehouse), it);
  }
  const toRows = (map, keyName) => [...map.entries()]
    .sort((a, b) => (Math.abs(b[1].count_diff) - Math.abs(a[1].count_diff))
      || String(a[0]).localeCompare(String(b[0])))
    .map(([k, v]) => Object.assign({ [keyName]: k }, v));
  const total = detail.reduce((acc, it) => add(acc, it), fresh());
  return {
    by_name_warehouse: toRows(byBucket, 'bucket'),
    by_name: toRows(byName, 'name'),
    by_warehouse: toRows(byWarehouse, 'warehouse'),
    total,
    basis: '分品名 × 分仓库汇总，按差异量（盘点实存 − 期末库存）的绝对值从大到小排；'
      + '超量合计取各明细行「期末库存 − 许可上限」的正值之和'
      + (present.has('warehouse') ? '。' : '（本表没有「仓库」列，一律归到「(未填仓库)」）。'),
  };
}

/** 付费项 5：可整改清单 —— 同一 品名+规格+仓库 的问题合并成一条，按差异量从大到小排队 */
function buildConsolidatedActions(items, findings) {
  const rowByLine = new Map();
  for (const it of items) if (!it.isTotal) rowByLine.set(it.line, it);
  const buckets = new Map();
  for (const f of findings) {
    const it = rowByLine.get(f.line);
    if (!it) continue;                                  // 只汇总到得了明细行的结论（合计行的问题不归到某个品种）
    const b = bucketOf(it);
    if (!buckets.has(b.key)) {
      buckets.set(b.key, {
        bucket: b.key, name: b.name, spec: b.spec, warehouse: b.warehouse,
        lines: [], categories: [], count_diff: 0, over_limit: 0, abs_diff: 0, actions: [],
      });
    }
    const acc = buckets.get(b.key);
    if (acc.lines.indexOf(it.line) < 0) acc.lines.push(it.line);
    if (acc.categories.indexOf(f.category) < 0) acc.categories.push(f.category);
    if (f.category === '账实不符' && typeof f.diff === 'number') acc.count_diff = round2(acc.count_diff + f.diff);
    if (f.category === '超量储存' && typeof f.diff === 'number') acc.over_limit = round2(acc.over_limit + f.diff);
    if (f.advice && acc.actions.indexOf(f.advice) < 0) acc.actions.push(f.advice);
  }
  const list = [...buckets.values()];
  for (const b of list) {
    b.lines.sort((x, y) => x - y);
    b.abs_diff = round2(Math.max(Math.abs(b.count_diff), b.over_limit));
    b.action = `【${b.name} / ${b.spec} / ${b.warehouse}】涉及第 ${b.lines.join('、')} 行，`
      + `问题类型：${b.categories.join('、')}；`
      + (Math.abs(b.count_diff) >= TOL ? `账实差异合计 ${qty(b.count_diff)}，` : '')
      + (b.over_limit >= TOL ? `超出许可上限合计 ${qty(b.over_limit)}，` : '')
      + b.actions.join(' ');
  }
  return list
    .sort((a, b) => (b.abs_diff - a.abs_diff) || (a.lines[0] - b.lines[0]) || a.bucket.localeCompare(b.bucket))
    .map((b, i) => Object.assign({ seq: i + 1 }, b));
}

/** 订阅版的「这一项为什么没做」说明（材料里缺哪一列就如实说，绝不用默认值假装核过） */
function paidNotesOf(items, present) {
  const notes = [];
  const detail = items.filter((it) => !it.isTotal);
  if (!present.has('limitQty')) {
    notes.push('本表没有「许可上限 / 规定上限」列：超量储存这一项没有执行 —— 不会替你套一个默认上限假装核过。');
  }
  if (!present.has('expiry')) {
    notes.push('本表没有「有效期至 / 到期日」列：复检有效期到期这一项没有执行。');
  } else if (resolveBaseDate(items, null) === null) {
    notes.push('本表取不到基准日（业务日期都认不出）：复检有效期到期这一项没有执行 —— '
      + '不会拿运行当天当基准日，那会让结论每天都变。');
  }
  if (!present.has('issuer') && !present.has('bookkeeper')) {
    notes.push('本表没有「收发人 / 记账人」列：双人复核缺失这一项没有执行。');
  }
  if (!present.has('storageCond')) {
    notes.push('本表没有「储存条件记录 / 温湿度」列：储存条件记录缺失这一项没有执行。');
  }
  if (!present.has('warehouse')) {
    notes.push('本表没有「仓库」列：分品名×分仓库汇总里的仓库一律归到「(未填仓库)」。');
  }
  if (!present.has('amountIn') && !present.has('amountBalance')) {
    notes.push('本表没有金额列：合计行复核只覆盖数量列。');
  }
  const dates = [...new Set(detail.map((it) => parseDate(it.date)).filter((x) => x !== null))];
  if (dates.length <= 1) {
    notes.push(`本表只有 ${dates.length} 个可识别的业务日期：台账期间连续性无法判断，这一项没有执行。`);
  }
  return notes;
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

  const paid = Boolean(p.full || p.credit || p.token);
  const findings = [];
  const notRun = [];

  for (const f of checkQuantityIdentity(t.items)) findings.push(f);
  for (const f of checkBookVsCount(t.items)) findings.push(f);
  for (const f of checkRequisitionReturn(t.items)) findings.push(f);
  for (const f of checkDuplicateEntry(t.items)) findings.push(f);
  for (const f of checkTotalRows(t.items)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

  if (paid) {
    const present = presentRoles(t.items);
    const baseDate = resolveBaseDate(t.items, p);
    for (const it of t.items) {
      if (it.isTotal) continue;                        // 合计行不是一条业务，逐行项都不看它
      for (const f of checkStorageLimit(it, present)) findings.push(f);
      for (const f of checkExpiry(it, baseDate, present)) findings.push(f);
      for (const f of checkDualSignOff(it, present)) findings.push(f);
      for (const f of checkStorageCondition(it, present)) findings.push(f);
    }
    for (const f of checkPeriodContinuity(t.items)) findings.push(f);
  } else {
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  }

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
    checks_executed: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得对、必需列都填了、'
      + '合计行复算一致**，不代表实物与台账真的相符、也不代表安全设施、储存场所、MSDS 与安全标签内容已经过关 —— '
      + '那些不在本工具范围内。';
  }

  const scope = {
    checks: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
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

  if (paid) {
    const present = presentRoles(t.items);
    const notes = paidNotesOf(t.items, present);
    result.rollup = buildRollup(t.items, present);
    result.consolidated_actions = buildConsolidatedActions(t.items, findings);
    if (notes.length) result.checks_notes = notes;
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
  CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
