#!/usr/bin/env node
/**
 * food-additive-usage-check-full.js —— 食品添加剂使用记录核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：食品生产企业**每一批投料**都要按 GB 2760《食品安全国家标准 食品添加剂使用标准》记录
 * 添加剂的名称、功能类别与使用量。市场监管抽检直接看两样东西：**投料记录**与**标签配料表**对不对得上。
 * 「超范围使用 / 超限量使用」是抽检不合格、召回与处罚的头号原因，而它几乎总是这样产生的：
 *   · 使用量按「批量」复算比例后越过了限量值（GB 2760 的限量单位是 g/kg，投料单上却是克）；
 *   · 同一添加剂在不同批次的台账里写了两个限量值，抄串了一个；
 *   · 标签配料表没写、或者投料记录里根本没有的那种添加剂；
 *   · 同一批次同一添加剂被记了两行（实际加了两次，或重复记录）；
 *   · 复配添加剂只记了一个总量，各单体之和与单体记录对不上；
 *   · 由配料（酱油、料酒、复合调味料）**带入**的添加剂没并进总量；
 *   · 同一功能类别下好几个品种叠加，相对量合计过了 100%；
 *   · 合计行与明细行对不上，或者关键字段根本是空的。
 * 核错一项，就是抽检不合格 + 召回 + 处罚 —— 所以每条结论都必须能拿原文复算。
 *
 * 本文件同时服务**订阅版（买断版）**与**本包**两个包：
 *   · 订阅版执行全部检查项（免费六项 + 追加五项）；
 *   · 本包只执行免费六项。追加项的实现在免费包里被 `tools/strip_free_engine.py` 整块摘除，
 *     免费包的 `CHECKS_WITHHELD` 里只剩**说明文本**，不是实现。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定这个配方该不该用这个添加剂（法规判定权在监管与检验机构）、不判定检验报告是否合格、
 *          不读 .xlsx / .pdf 原件、不联网核验 GB 2760 的现行版本与最新增补公告；
 *          **类别-允许表是本包内置的待企业确认白名单**，必须由企业按 GB 2760 现行版本与本厂产品核对后使用；
 *          材料不足**一律不给结论**。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '使用量按比例复算（使用量g ÷ 批量kg ≤ 限量值g/kg，逐行算并给出使用率与超出倍数）',
  '同一产品不同批次的限量口径不一致（同一添加剂写了两个限量值 ⇒ 点名）',
  '标签配料表与投料记录一致性（投料里有、配料表没标注 / 配料表标了、投料记录里没有）',
  '同一批次同一添加剂重复投料行',
  '合计行逐列复核（使用量合计、批量合计）',
  '字段合法性（关键字段缺失、数值为负或为零、日期格式非法）',
];

const CHECKS_WITHHELD = [
  '超范围使用（该添加剂 / 功能类别不允许用于该食品类别，按内置的类别-允许表判定并点名）',
  '复配添加剂拆分核算（复配的各单体之和 vs 记录的单体量）',
  '配料带入原则（由配料带入的添加剂量未计入总量）',
  '同一功能类别多品种叠加的相对量合计 > 100%（同一功能下的比例之和）',
  '分产品 × 分添加剂汇总清单（超出倍数降序 + 每组可整改动作）',
];

const OUT_OF_SCOPE = [
  '判定这个配方该不该用这个添加剂、用量标准对不对 —— 那是 GB 2760 与监管部门的判定权，'
    + '本工具只把台账里的使用量与台账里的限量值按比例复算，再把「类别-允许添加剂」白名单拿来点名',
  '内置的类别-允许表是**本包自带的待企业确认白名单**，不是 GB 2760 原文：'
    + '换产品、换类别、遇到市场监管总局的增补公告，必须由企业按现行版本自行核对后再用',
  '判定检验结论本身是否合格、产品实物标签是否与配料表一致（本工具只核文本字面）',
  '读取 .xlsx / .pdf 原件、联网核验配料表实物标签与添加剂生产许可证的真伪，替代企业食品安全员或监管部门的认定',
];

// 样例：一本**干净**的食品添加剂投料与使用台账 —— 3 个产品 / 5 个生产批次，
// 逐行比例复算都没超限量（且相对量合计都没过 100%）、同一添加剂的限量口径一致、
// 配料表标注与投料记录互相对得上、无重复投料行、合计行与明细一致、字段与日期都合法。
// 里面已经埋好了追加项要用的三种形态：复配添加剂（要拆分）、配料带入（酱油带入苯甲酸）、
// 白砂糖（非添加剂，不该被当成漏投料）。**全表零命中**。
const SAMPLE_TEXT = [
  '产品名称	生产批次	食品类别	添加剂名称	功能类别	使用量g	批量kg	限量值g/kg	配料表标注	投料日期	核对基准日	备注',
  '焦糖瓜子	B20260301	炒货食品	焦糖色	着色剂	1,500	1,000	2.0	焦糖色、食用香精、白砂糖	2026-03-01	2026-03-31	常规投料',
  '焦糖瓜子	B20260301	炒货食品	食用香精	增味剂	300	1,000	1.0	焦糖色、食用香精、白砂糖	2026-03-01	2026-03-31	常规投料',
  '焦糖瓜子	B20260308	炒货食品	焦糖色	着色剂	1,800	1,200	2.0	焦糖色、食用香精、白砂糖	2026-03-08	2026-03-31	常规投料',
  '焦糖瓜子	B20260308	炒货食品	食用香精	增味剂	360	1,200	1.0	焦糖色、食用香精、白砂糖	2026-03-08	2026-03-31	常规投料',
  '酱卤牛肉	B20260305	酱卤肉制品	复配防腐剂(山梨酸钾40%+脱氢乙酸钠20%)	防腐剂	500	5,000	0.5	山梨酸钾、脱氢乙酸钠、苯甲酸（酱油带入）、酱油	2026-03-05	2026-03-31	复配防腐剂：拆分核算，山梨酸钾40%＋脱氢乙酸钠20%',
  '酱卤牛肉	B20260305	酱卤肉制品	山梨酸钾	防腐剂	200	5,000	0.5	山梨酸钾、脱氢乙酸钠、苯甲酸（酱油带入）、酱油	2026-03-05	2026-03-31	单体投料：按复配产品组分表单独投料的单体',
  '酱卤牛肉	B20260305	酱卤肉制品	脱氢乙酸钠	防腐剂	100	5,000	0.3	山梨酸钾、脱氢乙酸钠、苯甲酸（酱油带入）、酱油	2026-03-05	2026-03-31	单体投料：按复配产品组分表单独投料的单体',
  '酱卤牛肉	B20260305	酱卤肉制品	苯甲酸	防腐剂	150	5,000	0.3	山梨酸钾、脱氢乙酸钠、苯甲酸（酱油带入）、酱油	2026-03-05	2026-03-31	配料带入：由酱油带入的苯甲酸，已计入本批总量',
  '卤鸡蛋	B20260312	卤蛋制品	焦糖色	着色剂	400	2,000	0.5	焦糖色、红曲红、白砂糖	2026年3月12日	2026-03-31	常规投料',
  '卤鸡蛋	B20260312	卤蛋制品	红曲红	着色剂	100	2,000	0.5	焦糖色、红曲红、白砂糖	2026-03-12	2026-03-31	常规投料',
  '合计	—	—	—	—	5,410	—	—	—	—	—	11 行明细：使用量逐行加总、批量为各批次批量之和',
].join('\n');

const TOL = 0.005;
const RATIO_TOL = 1e-6;

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = [
  'productName', 'batchNo', 'foodCategory', 'additiveName', 'functionClass',
  'usageG', 'batchKg', 'limitGkg', 'labelDeclare', 'feedDate', 'checkDate',
];

// 单元格级必需字段（空白 / 占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['productName', '产品名称'],
  ['batchNo', '生产批次'],
  ['foodCategory', '食品类别'],
  ['additiveName', '添加剂名称'],
  ['functionClass', '功能类别'],
  ['usageG', '使用量g'],
  ['batchKg', '批量kg'],
  ['limitGkg', '限量值g/kg'],
  ['labelDeclare', '配料表标注'],
  ['feedDate', '投料日期'],
];

// 日期列（格式非法逐格点名）
const DATE_FIELDS = [
  ['feedDate', '投料日期'],
  ['checkDate', '核对基准日'],
];

// 数值列（为负 / 无法解析逐格点名）
const NUMBER_FIELDS = [
  ['usageG', '使用量g'],
  ['batchKg', '批量kg'],
  ['limitGkg', '限量值g/kg'],
];

// 必须为正的列：等于 0 也不成立（使用量 0 ⇒ 这一行等于没投；批量 0 ⇒ 比例算不出来）
const POSITIVE_ROLES = ['usageG', 'batchKg', 'limitGkg'];
const ZERO_REASON = {
  usageG: '使用量为 0 等于这一行没有投料',
  batchKg: '批量为 0 时使用量的 g/kg 比例算不出来（除零）',
  limitGkg: '限量值为 0 等于这个添加剂在本类别上不允许使用',
};

// 类别-允许表：食品类别 → { 添加剂名称: 允许的直接添加限量值(g/kg) }。
// ⚠️ 这是**本包内置的待企业确认白名单**（见 OUT_OF_SCOPE）：只用于判定「超范围」与「超限量」，
//    不是 GB 2760 原文。表里**没有**的添加剂一律按「超范围使用」点名，由企业按现行版本复核。
const ALLOW_BY_CATEGORY = {
  炒货食品: { 焦糖色: 2.0, 食用香精: 1.0 },
  酱卤肉制品: { 山梨酸钾: 0.5, 脱氢乙酸钠: 0.3, 复配防腐剂: 0.5, 防腐剂: 0.5, 苯甲酸: 0.3 },
  卤蛋制品: { 焦糖色: 0.5, 红曲红: 0.5 },
  糕点: { 山梨酸钾: 0.5, 脱氢乙酸钠: 0.3, 焦糖色: 1.0 },
  饮料类: { 山梨酸钾: 0.5, 苯甲酸: 0.2, 焦糖色: 1.0 },
  酱油: { 苯甲酸: 1.0, 山梨酸钾: 1.0 },
};

// **只允许由配料带入**的添加剂：本厂不得直接投料（直接投料行 = 超范围使用）
const CARRYIN_ONLY = ['苯甲酸'];

// 复配载体标记：这类行的使用量是「复配产品总量」，不是单体量 ⇒ 比例复算用复配产品自己的限量值，
// 单体量要另行拆分核算（追加项）
const COMPOUND_MARKERS = ['复配', '复合'];

// 非添加剂配料（不该被当成「投料记录里没有这种添加剂」）
const NON_ADDITIVE_MARKERS = ['白砂糖', '食用盐', '食盐', '水', '小麦粉', '植物油', '酱油', '料酒', '淀粉', '鸡蛋', '香辛料'];

const COMPOUND_TOL = 0.02;       // 复配拆分允许的相对偏差（2%）

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词就会把更具体的列抢走（本仓库踩过多次，见 tools/header_map_check.py）。
//    本表的坑位集中在：「使用量g」必须排在「批量kg」「限量值g/kg」之前（否则被「量」抢走）、
//    「批量kg」必须排在「使用量g」之前（否则被「量」抢走）、
//    「限量值」必须排在「使用量」「批量」之前（否则被「量」抢走）；
//    兜底的 '日期' 只能放在所有日期角色之后。
const ROLES = {
  productName: ['产品名称', '品名', '产品名'],
  batchNo: ['生产批次', '批次号', '批号', '批次'],
  foodCategory: ['食品类别', '食品分类', '产品类别', '食品种类'],
  additiveName: ['添加剂名称', '复配添加剂', '添加物名称', '添加剂'],
  functionClass: ['功能类别', '功能分类', '添加剂功能'],
  limitGkg: ['限量值g/kg', '限量值', '最大使用量', '限量'],
  usageG: ['使用量g', '使用量', '添加量', '投料量', '实际用量', '用量'],
  batchKg: ['批量kg', '投料批量', '本批投料量', '批量'],
  labelDeclare: ['配料表标注', '标签配料表', '配料表', '标签标注'],
  feedDate: ['投料日期', '投料日', '使用日期'],
  checkDate: ['核对基准日', '核对日期', '核查日期', '基准日期', '基准日'],
  note: ['备注', '说明'],
};

const LABELS = {
  productName: '产品名称',
  batchNo: '生产批次',
  foodCategory: '食品类别',
  additiveName: '添加剂名称',
  functionClass: '功能类别',
  usageG: '使用量g',
  batchKg: '批量kg',
  limitGkg: '限量值g/kg',
  labelDeclare: '配料表标注',
  feedDate: '投料日期',
  checkDate: '核对基准日',
  note: '备注',
};

const SUM_ROLES = ['usageG', 'batchKg'];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张投料记录补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「没超范围」，也不说「没超限量」。',
  };
}

/** 数字归一化：认千分位（1,500）、全角数字与全角逗号、货币符号、括号负数；认不出来返回 null */
function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  let s = String(raw).trim();
  s = s.replace(/[０-９]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xFEE0))
    .replace(/[．。]/g, '.');
  s = s.replace(/[¥￥,，\s\u00a0]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '');
  if (!/^-?\d+(\.\d+)?%?$/.test(t)) return null;
  const n = Number(t.replace('%', ''));
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;
const round4 = (n) => Math.round(n * 10000) / 10000;
/** 超出倍数：使用量比例 ÷ 限量值（> 1 即超限量），保留 4 位 */
const ratioOf = (perKg, limit) => (limit > 0 ? round4(perKg / limit) : null);

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定|待核)$/i.test(s);
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
}

/** 日期归一化成 YYYY-MM-DD；认不出来返回 null（认不出来绝不当成今天） */
function normDate(raw) {
  if (raw === undefined || raw === null) return null;
  let s = String(raw).trim();
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  s = s.replace(/[０-９]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xFEE0));
  s = s.replace(/[年月]/g, '-').replace(/日/g, '').replace(/[.／/]/g, '-').replace(/\s+/g, '');
  if (/^\d{8}$/.test(s)) s = s.slice(0, 4) + '-' + s.slice(4, 6) + '-' + s.slice(6, 8);
  const m = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(s);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const dt = new Date(Date.UTC(y, mo - 1, d));
  if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== mo - 1 || dt.getUTCDate() !== d) return null;
  return m[1] + '-' + String(mo).padStart(2, '0') + '-' + String(d).padStart(2, '0');
}

const SECTION_RE = /^\s*-{2,}\s*(.+?)\s*-{2,}\s*$/;
function isSectionMarker(line) {
  return SECTION_RE.test(String(line == null ? '' : line));
}

function roleOf(header) {
  const h = String(header == null ? '' : header).replace(/[\s（）()：:]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    for (const k of keys) {
      if (h.indexOf(k.replace(/[\s（）()：:]/g, '')) >= 0) return role;
    }
  }
  return null;
}

const TOTAL_LABEL = /^(合计|小计|总计|总合计|合\s*计)$/;
/** 合计行不是投料明细：逐行检查要跳过它，只有「合计行逐列复核」那一项会用到它 */
function isTotalRow(it) {
  const name = String(it.productName == null ? '' : it.productName).trim();
  const batch = String(it.batchNo == null ? '' : it.batchNo).trim();
  return TOTAL_LABEL.test(name) || TOTAL_LABEL.test(batch);
}

/**
 * 解析成 {header, cols, items, detail, totalRows, totals, missingRoles, missingColumns, error}。
 * items 是**扁平**对象：{line, raw, isTotal, 角色:值…}；遇到 `--- 段名 ---` 就停（后面是另一张表）。
 */
function parseTable(text) {
  const rawLines = String(text == null ? '' : text).split(/\r?\n/);
  const rows = [];
  for (let i = 0; i < rawLines.length; i++) {
    if (isSectionMarker(rawLines[i])) break;
    if (String(rawLines[i]).trim() === '') continue;
    rows.push({ line: i + 1, raw: String(rawLines[i]) });
  }
  if (!rows.length) {
    return {
      error: 'empty', header: [], cols: [], items: [], detail: [], totalRows: [], totals: {},
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
  const detail = items.filter((it) => !it.isTotal);
  const totalRows = items.filter((it) => it.isTotal);
  const totals = {};
  for (const role of SUM_ROLES) {
    totals[role] = round2(detail.reduce((acc, it) => {
      const n = normNumber(it[role]);
      return acc + (n === null ? 0 : n);
    }, 0));
  }
  return {
    error: missingRoles.length ? 'no_header' : null,
    header,
    cols,
    items,
    detail,
    totalRows,
    totals,
    missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  };
}

const cell = (it, role) => String(it[role] == null ? '' : it[role]).trim();

function who(it) {
  const p = cell(it, 'productName');
  const b = cell(it, 'batchNo');
  const a = cell(it, 'additiveName');
  const parts = [];
  if (p) parts.push(p);
  if (b) parts.push('批次 ' + b);
  if (a) parts.push(a);
  return `第 ${it.line} 行「${parts.join(' / ') || '未填产品与添加剂'}」`;
}

/** 每条结论都带原文依据：行号 + 产品 / 批次 / 添加剂 + 该行原文（截断），可被第三方用同一口径复算 */
function finding(level, category, it, diff, message, advice) {
  const f = {
    level,
    category,
    line: it.line,
    product_name: cell(it, 'productName'),
    batch_no: cell(it, 'batchNo'),
    additive_name: cell(it, 'additiveName'),
    evidence: String(it.raw == null ? '' : it.raw).slice(0, 200),
    message,
  };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

/** 使用量比例与超出倍数一并挂在结论上（可复算） */
function withRatio(f, usageG, batchKg, limit) {
  const perKg = round4(usageG / batchKg);
  f.usage_g = round2(usageG);
  f.batch_kg = round2(batchKg);
  f.limit_g_kg = round2(limit);
  f.per_kg = perKg;
  f.usage_ratio = ratioOf(perKg, limit);
  return f;
}

/** 台账里第一个能认出来的核对基准日（逐行没填时兜底；逐行填了就以逐行为准） */
function baseDateOf(items) {
  for (const it of items) {
    const d = normDate(it.checkDate);
    if (d) return d;
  }
  return null;
}
const baseOf = (it, base) => normDate(it.checkDate) || base;

/** 配料表标注拆成成分名清单 */
function parseLabel(text) {
  return String(text == null ? '' : text)
    .split(/[、,，;；/／|｜+＋&和\u3000\s]+/)
    .map((s) => s.replace(/[（）()]/g, '').trim())
    .filter(Boolean);
}

/** 某一行是不是复配添加剂（名称或备注里有「复配 / 复合」） */
function isCompound(it) {
  // ⚠️ 只看**添加剂名称**，不看备注：备注里写「按复配产品组分表单独投料的单体」的是**单体行**，
  //    把它当成复配行会凭空多报「拆分核算未执行」。复配产品的名字里才带「复配 / 复合」。
  const name = cell(it, 'additiveName');
  return COMPOUND_MARKERS.some((k) => name.indexOf(k) >= 0);
}

/** 复配添加剂名称的基名：去掉 "(…)" 与「复配/复合」前缀，用于在允许表里找限量 */
function compoundBaseName(name) {
  const raw = String(name == null ? '' : name).trim();
  const noParen = raw.replace(/\([^)]*\)/g, '').replace(/（[^）]*）/g, '');
  let s = noParen;
  for (const k of COMPOUND_MARKERS) s = s.split(k).join('');
  s = s.trim();
  return s || noParen.trim() || raw;
}

/**
 * 从复配添加剂的名称或备注里拆出各单体与占比：认「山梨酸钾40%」与
 * 「山梨酸钾40%＋脱氢乙酸钠20%」这两种真实写法；拆不出来返回 []（⇒ 追加项如实记"没有执行"）。
 */
function parseCompoundMembers(it) {
  const src = cell(it, 'additiveName') + ' ' + cell(it, 'note');
  const out = [];
  const seen = new Set();
  const re = /([\u4e00-\u9fa5A-Za-z][\u4e00-\u9fa5A-Za-z0-9]*?)\s*[:：]?\s*(\d+(?:\.\d+)?)\s*%/g;
  let m;
  while ((m = re.exec(src)) !== null) {
    const name = m[1].replace(/^.*[+＋、，,;；/／]/, '').trim();
    const pct = Number(m[2]);
    if (!name || seen.has(name)) continue;
    if (!Number.isFinite(pct) || pct <= 0 || pct > 100) continue;
    if (/^(合计|拆分|核算|总量|复配|复合|防腐剂|投料|常规|备注)$/.test(name)) continue;
    seen.add(name);
    out.push({ name, pct });
  }
  return out;
}

/** 备注里是不是**声明了**「由配料带入」——注意别被「没写带入来源」这种否定说法骗了。
 *  这是真实踩过的缺陷：备注写「直接投料，没写带入来源」时，早先的实现因为正则里有裸的「带入」
 *  而把它当成"已声明带入"，于是**漏报了整条带入项**（第 ⑨ 项最要命的场景反而放过）。
 *  判据：必须出现「配料带入 / 由配料带入 / 带入量」这类**声明**，且前面不能是「没/未/无」，
 *  也不能是「没写带入 / 未标带入 / 无需带入」这类**否认**写法。 */
function isCarryIn(it) {
  const s = cell(it, 'note');
  if (!s) return false;
  if (/[没未无][^，。；,;]{0,4}(写|标|填|需|有)?[^，。；,;]{0,2}带入/.test(s)) return false;
  return /(由)?配料带入|带入量|由[^，。；,;]{0,6}带入/.test(s);
}

/** 同一批次的批量（从该批次第一行取，用于把单体记录换算成比例） */
function batchKgOf(batch, detail) {
  for (const it of detail) {
    if (cell(it, 'batchNo') !== batch) continue;
    const n = normNumber(it.batchKg);
    if (n !== null && n > 0) return n;
  }
  return null;
}

/** 同批次某一行添加剂的记录（单体记录） */
function rowsOfAdditive(batch, additive, detail) {
  return detail.filter((it) => cell(it, 'batchNo') === batch && cell(it, 'additiveName') === additive);
}

/* ============================ 本包检查（六项） ============================ */

function checkUsageRatio(items, base) {
  // ① 使用量按比例复算：使用量g ÷ 批量kg ≤ 限量值g/kg，逐行算并给超出倍数
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const usage = normNumber(it.usageG);
    const batch = normNumber(it.batchKg);
    const limit = normNumber(it.limitGkg);
    if (usage === null || batch === null || limit === null) continue;  // 缺失 / 非法交给第 ⑥ 项
    if (usage <= 0 || batch <= 0 || limit <= 0) continue;
    const perKg = usage / batch;
    const ratio = perKg / limit;
    if (ratio <= 1 + RATIO_TOL) continue;
    const over = round2(usage - limit * batch);
    const f = finding(ratio >= 1.2 ? 'P0' : 'P1', '超限量使用', it, over,
      `${who(it)}：使用量 ${usage} g ÷ 批量 ${batch} kg = **${round4(perKg)} g/kg**，`
      + `台账限量值 ${limit} g/kg ⇒ 使用率 ${round4(ratio)}（**超出 ${round4(ratio - 1)}，即超限量 ${over} g**）。`
      + `（产品 ${cell(it, 'productName') || '(未填)'}，功能类别 ${cell(it, 'functionClass') || '(未填)'}。）`,
      'GB 2760 的限量单位是 g/kg，投料单上却是克 —— 这是超限量最常见的来源：'
      + '先按上面的差额调低投料量或扩大批量，再把「使用量」与「批量」两列的真实数填回去重跑。'
      + '超限量使用是抽检不合格与召回的直接原因，别只改台账数字。');
    out.push(withRatio(f, usage, batch, limit));
  }
  return out;
}

function checkLimitConsistency(items) {
  // ② 同一产品不同批次的限量口径不一致：同一添加剂写了两个限量值 ⇒ 点名
  const out = [];
  const groups = new Map();
  for (const it of items) {
    if (it.isTotal) continue;
    const p = cell(it, 'productName');
    const a = cell(it, 'additiveName');
    const limit = normNumber(it.limitGkg);
    if (!p || !a || limit === null) continue;
    const key = p + '||' + a;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push({ it, limit });
  }
  for (const list of groups.values()) {
    const values = [...new Set(list.map((x) => x.limit))];
    if (values.length < 2) continue;
    for (const x of list) {
      const others = list.filter((y) => y.it.line !== x.it.line && y.limit !== x.limit);
      if (!others.length) continue;
      const o = others[0];
      out.push(finding('P1', '限量口径不一致', x.it, round2(x.limit - o.limit),
        `${who(x.it)}：同一产品同一添加剂的限量值，第 ${x.it.line} 行写 ${x.limit} g/kg，`
        + `第 ${o.it.line} 行写 ${o.limit} g/kg —— **同一添加剂两个限量口径**（差 ${round2(Math.abs(x.limit - o.limit))} g/kg）。`
        + `本次涉及 ${values.length} 个不同的限量值：${values.join(' / ')}。`,
        '限量值只能有一个口径：要么某个批次抄错了，要么把「复配产品限量」与「单体限量」写混了。'
        + '拿 GB 2760 里这个食品类别对应的最大使用量核对后统一，再重跑 —— '
        + '口径不一致时，超限量的判定会随批次不同而得出不同结论。'));
    }
  }
  return out;
}

function checkLabelConsistency(items) {
  // ③ 标签配料表与投料记录一致性：投料里有、配料表没标注 / 配料表标了、投料记录里没有
  const out = [];
  const byProduct = new Map();
  for (const it of items) {
    if (it.isTotal) continue;
    const p = cell(it, 'productName');
    if (!p) continue;
    if (!byProduct.has(p)) byProduct.set(p, { items: [], parts: [] });
    const g = byProduct.get(p);
    g.items.push(it);
    const declared = cell(it, 'labelDeclare');
    if (isBlank(declared)) continue;
    for (const part of parseLabel(declared)) {
      if (!g.parts.some((x) => x.name === part)) g.parts.push({ name: part, line: it.line });
    }
  }
  for (const [product, g] of byProduct.entries()) {
    const names = [...new Set(g.items.map((it) => cell(it, 'additiveName')).filter(Boolean))];
    const hay = g.parts.map((x) => x.name).join('|');
    // 方向一：投料里有这种添加剂，配料表标注里找不到它（含复配拆分后的单体名）
    for (const it of g.items) {
      const a = cell(it, 'additiveName');
      if (!a) continue;
      const declared = cell(it, 'labelDeclare');
      if (isBlank(declared)) continue;
      const base = compoundBaseName(a);
      const members = parseCompoundMembers(it).map((m) => m.name);
      const candidates = [a, base].concat(members).filter(Boolean);
      const hit = candidates.some((c) => hay.indexOf(c) >= 0)
        || (base && hay.indexOf(base) >= 0 && members.length > 0 && members.every((m) => hay.indexOf(m) >= 0));
      if (hit) continue;
      out.push(finding('P0', '配料表与投料记录不一致', it, undefined,
        `${who(it)}：投料记录里有「${a}」（功能类别 ${cell(it, 'functionClass') || '(未填)'}），`
        + `但产品「${product}」第 ${it.line} 行的配料表标注是「${declared}」—— **配料表里找不到它**。`,
        '市场监管抽检直接比对投料记录与标签配料表：投料了却没标注，属于标签不合格（GB 7718 要求'
        + '配料表按加入量递减列出、食品添加剂要用标准名称标注）。先核实标签实物，'
        + '再决定是改标签还是改投料记录 —— 两个文本必须对得上。'));
    }
    // 方向二：配料表标注里列了这种添加剂，投料记录里却没有对应行
    for (const part of g.parts) {
      const pn = part.name;
      if (NON_ADDITIVE_MARKERS.some((k) => pn.indexOf(k) >= 0)) continue;
      const hit = names.some((a) => {
        const base = compoundBaseName(a);
        const members = parseCompoundMembers({ additiveName: a, note: '' }).map((m) => m.name);
        return pn.indexOf(a) >= 0 || a.indexOf(pn) >= 0
          || (base && (pn.indexOf(base) >= 0 || base.indexOf(pn) >= 0))
          || members.some((m) => pn.indexOf(m) >= 0 || m.indexOf(pn) >= 0);
      });
      if (hit) continue;
      const src = g.items[0];
      out.push(finding('P2', '配料表与投料记录不一致', src, undefined,
        `产品「${product}」：配料表标注里列了「${pn}」（原文第 ${src.line} 行「配料表标注」列），`
        + `但投料记录里没有叫这个名字的添加剂行 —— 要么漏记投料（配料表里的东西不可能凭空出现），`
        + `要么它是经配料带入的（那就该在备注里写明带入来源）。`,
        '配料表与投料记录是一对镜像：配料表能列出来的添加剂，投料记录里必须能找到它的来路'
        + '（直接投料或由配料带入）。补一行投料记录，或在备注里写明带入来源。'));
    }
  }
  return out;
}

function checkDuplicateRows(items) {
  // ④ 同一批次同一添加剂重复投料行
  const out = [];
  const first = new Map();
  for (const it of items) {
    if (it.isTotal) continue;
    const batch = cell(it, 'batchNo');
    const a = cell(it, 'additiveName');
    if (!batch || !a) continue;
    const key = batch + '||' + a;
    if (first.has(key)) {
      const before = first.get(key);
      out.push(finding('P1', '重复投料行', it, undefined,
        `${who(it)}：批次 ${batch} 的「${a}」在第 ${before.line} 行已经记过一次 —— `
        + `**同一批次同一添加剂重复投料行**（本次这行功能类别 ${cell(it, 'functionClass') || '(未填)'}，`
        + `使用量 ${cell(it, 'usageG') || '(未填)'} g）。`,
        '重复行会让「合计使用量」翻倍，也会让超限量判定失真：先确认是**真的投了两次**'
        + '（那就是超限量风险，按并表后的使用量复算）还是**重复记录**（删掉多记的一行，保留原始凭证）。'));
    } else {
      first.set(key, it);
    }
  }
  return out;
}

function checkTotals(items, cols) {
  // ⑤ 合计行逐列复核：使用量合计、批量合计必须等于明细行加总
  const out = [];
  const detail = items.filter((it) => !it.isTotal);
  const totalRows = items.filter((it) => it.isTotal);
  for (const tr of totalRows) {
    for (const role of SUM_ROLES) {
      if (!cols.some((c) => c.role === role)) continue;
      const raw = tr[role];
      if (isBlank(raw)) continue;
      const declared = normNumber(raw);
      if (declared === null) {
        out.push(finding('P1', '合计行不符', tr, undefined,
          `第 ${tr.line} 行合计行的「${LABELS[role]}」值是「${String(raw).trim()}」，不是可识别的数字。`,
          '合计行只能写数字；请核对是否把单位（g / kg）写进了单元格里。'));
        continue;
      }
      const actual = round2(detail.reduce((acc, it) => {
        const n = normNumber(it[role]);
        return acc + (n === null ? 0 : n);
      }, 0));
      const diff = round2(declared - actual);
      if (Math.abs(diff) < TOL) continue;
      out.push(finding('P1', '合计行不符', tr, diff,
        `第 ${tr.line} 行合计行的「${LABELS[role]}」写着 ${declared}，但上面 ${detail.length} 行明细逐行加总是 ${actual}，`
        + `差 ${diff}（合计 − 明细）。`,
        '合计行必须等于明细行逐列加总：先看有没有明细行被隐藏 / 筛选掉了，再看合计公式有没有漏行或重复计数。'
        + '投料量的合计直接决定这一批的添加剂总量，合计错了超限量就判不出来。'
        + '（本工具只核这一个合计行，不替你去别的表里找补。）'));
    }
  }
  return out;
}

function checkFieldIntegrity(items) {
  // ⑥ 字段合法性：关键字段缺失、日期格式非法、数值为负或为零
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        `${who(it)}：这些关键字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的字段会让对应的核对整项做不了（例如批量空着就复算不出 g/kg 的比例）；'
        + '补全后重跑，本工具不会替你猜一个默认值。'));
    }

    for (const [role, label] of DATE_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      if (normDate(raw) === null) {
        out.push(finding('P1', '日期格式非法', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的日期`
          + '（只认 2026-03-31 / 2026/3/31 / 2026年3月31日 / 20260331 这几种形态）。',
          '把日期改成 2026-03-31 这种形态再跑；投料日期认不出来时就没法把这一批归到哪一天投的料。'));
      }
    }

    for (const [role, label] of NUMBER_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        out.push(finding('P1', '数值为负或为零', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的数字。`,
          '使用量 / 批量 / 限量值都必须是纯数字（如 1,500 / 1000 / 2.0）；'
          + '写成「约一千五百克」这类形态本工具一律不给结论。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '数值为负或为零', it, n,
          `${who(it)}：「${label}」是负数（${n}）—— 投料台账里的量出现负数，通常是填反了或写成了红字。`,
          '确认是红字冲销还是填错方向；确属冲销的请写在备注里并保留原值，别直接改成正数。'));
      } else if (n === 0 && POSITIVE_ROLES.indexOf(role) >= 0) {
        out.push(finding('P1', '数值为负或为零', it, n,
          `${who(it)}：「${label}」是 0 —— ${ZERO_REASON[role] || '台账口径上不成立'}。`,
          '按真实的投料单填数：批量填这一批的投料总量（kg），使用量填这一批实际加了多少这种添加剂（g）；'
          + '限量值为 0 时应走「超范围使用」的判定，而不是把 0 写进限量列。'));
      }
    }
  }
  return out;
}

/* ============================ 订阅版检查（追加五项） ============================ */

function checkOutOfScope(it) {
  // 付费 ①：超范围使用 —— 该添加剂 / 功能类别不允许用于该食品类别（按内置的类别-允许表判定）
  if (it.isTotal) return [];
  const category = cell(it, 'foodCategory');
  const additive = cell(it, 'additiveName');
  if (!category || !additive) return [];
  const table = ALLOW_BY_CATEGORY[category];
  const isCompoundRow = isCompound(it);
  const probe = isCompoundRow ? compoundBaseName(additive) : additive;
  const carryOnly = CARRYIN_ONLY.some((k) => additive.indexOf(k) >= 0);

  if (!table) {
    return [finding('P1', '超范围使用', it, undefined,
      `${who(it)}：食品类别「${category}」不在内置的**类别-允许表**里 —— `
      + `这张表没有这个类别，所以「${additive}」能不能用在本类别上，本工具**判不了**（不是判它合规）。`,
      '这是本包内置的待企业确认白名单，不是 GB 2760 原文：请按 GB 2760 现行版本把本厂真实用到的'
      + '食品类别与允许添加剂补进白名单，再重跑；补之前，这一个类别的超范围使用一律按「没有执行」处理。')];
  }
  // ⚠️ 判「只允许由配料带入」要**排在允许清单命中之前**：允许清单里可能也列着它（那个量是带入量的上限），
  //    但直接投料照样超范围。顺序一错就漏判。
  if (carryOnly && !isCarryIn(it)) {
    return [finding('P0', '超范围使用', it, undefined,
      `${who(it)}：食品类别「${category}」**只允许「${additive}」由配料带入**，`
      + `但第 ${it.line} 行是**直接投料**（备注：${cell(it, 'note') || '(空)'}）—— 属于超范围使用。`,
      '由配料带入的添加剂不能当本厂直接添加用：把这一行改成配料带入（备注写明带入来源与配料的用量），'
      + '或者从配方里去掉这项直接投料。超范围使用是抽检不合格与处罚的头号原因。')];
  }
  if (Object.prototype.hasOwnProperty.call(table, probe) || Object.prototype.hasOwnProperty.call(table, additive)) {
    // 名称在允许清单里 ⇒ 还要比**限量值**：允许清单是数值列（不是字符串键名），
    // 必须比数字 —— 写成 `table[recorded]` 会因为键是 number 而永远 undefined（本包踩过）。
    const allowed = normNumber(table[probe] !== undefined ? table[probe] : table[additive]);
    const recorded = normNumber(it.limitGkg);
    if (allowed === null || recorded === null || Math.abs(allowed - recorded) < 1e-9) return [];
    return [finding('P0', '超范围使用', it, round2(recorded - allowed),
      `${who(it)}：食品类别「${category}」里「${probe}」的允许最大使用量是 ${allowed} g/kg，`
      + `但第 ${it.line} 行的限量值写的是 ${recorded} g/kg（差 ${round2(recorded - allowed)} g/kg）`
      + ' —— 台账写的限量口径与允许清单不一致，照它判就会把超限量放过去。',
      '限量值必须用 GB 2760 里这个食品类别对应的最大使用量、且全表只有一个口径：'
      + '把限量值改成允许清单里的数（或把允许清单按现行 GB 2760 补齐）后重跑，'
      + '**不要为了让它通过而把限量值放大** —— 放大限量值等于把超限量藏起来。')];
  }
  return [finding('P0', '超范围使用', it, undefined,
    `${who(it)}：食品类别「${category}」的允许清单里**没有**「${additive}」`
    + `（该类别允许的直接添加限量：${Object.keys(table).join('、') || '(空)'}）—— 属于超范围使用。`,
    '先拿 GB 2760 核对这个食品类别能不能用这种添加剂：确实不能用就立刻停用并改配方；'
    + '能用但名字写法不同（复配产品名 / 商品名 / 简称）就把允许清单里的名称补全，'
    + '**不要为了让它通过而把类别改掉**。')];
}

function checkCompoundSplit(it, ctx) {
  // 付费 ②：复配添加剂拆分核算 —— 复配的各单体之和 vs 记录的单体量
  if (it.isTotal) return [];
  if (!isCompound(it)) return [];
  const batch = cell(it, 'batchNo');
  const usage = normNumber(it.usageG);
  if (!batch || usage === null || usage <= 0) return [];
  const members = parseCompoundMembers(it);
  if (!members.length) {
    return [finding('P1', '复配拆分未核算', it, undefined,
      `${who(it)}：这一行是复配添加剂（使用量 ${usage} g），但名称与备注里**拆不出各单体与占比**`
      + '（认「山梨酸钾40%＋脱氢乙酸钠20%」这种写法）—— 拆分核算本次**没有执行**。',
      '复配添加剂的各单体都要单独核：把复配产品的组分表写进备注（单体名 + 占比），'
      + '再把每个单体的实际投料量单独记一行；本工具会把「复配量 × 占比」与单体记录逐项对照。')];
  }
  const out = [];
  for (const m of members) {
    const expect = round2(usage * m.pct / 100);
    const rows = rowsOfAdditive(batch, m.name, ctx.detail);
    if (!rows.length) continue;
    const actual = round2(rows.reduce((acc, r) => {
      const n = normNumber(r.usageG);
      return acc + (n === null ? 0 : n);
    }, 0));
    const diff = round2(actual - expect);
    if (Math.abs(diff) <= Math.max(COMPOUND_TOL * expect, 1)) continue;
    out.push(finding('P1', '复配拆分不符', it, diff,
      `${who(it)}：复配添加剂使用量 ${usage} g，其中「${m.name}」占 ${m.pct}% ⇒ 应为 ${expect} g，`
      + `但同批次「${m.name}」的单体记录（第 ${rows.map((r) => r.line).join('、')} 行）合计是 ${actual} g，`
      + `差 ${diff} g。`,
      '复配添加剂的组分表与实际投料必须对得上：要么复配产品的组分占比抄错了，'
      + '要么单体记录漏了一行或写错了量。按复配产品包装上的组分表核对后改正，再重跑。'));
  }
  return out;
}

function checkCarryIn(it, ctx) {
  // 付费 ③：配料带入原则 —— 由配料带入的添加剂量未计入总量
  if (it.isTotal) return [];
  const additive = cell(it, 'additiveName');
  const batch = cell(it, 'batchNo');
  if (!additive) return [];
  const usage = normNumber(it.usageG);
  const limit = normNumber(it.limitGkg);
  const marked = isCarryIn(it);
  const carryOnly = CARRYIN_ONLY.some((k) => additive.indexOf(k) >= 0);
  if (marked) {
    // 已声明带入：带入量必须并进总量再与限量比对
    if (usage === null || limit === null) return [];
    const kg = normNumber(it.batchKg) || batchKgOf(batch, ctx.detail);
    if (kg === null || kg <= 0) return [];
    const perKg = usage / kg;
    if (perKg <= limit + RATIO_TOL) return [];
    return [finding('P1', '带入量未计入总量', it, round2(usage - limit * kg),
      `${who(it)}：备注已写明「配料带入」，但带入量按比例复算是 ${round4(perKg)} g/kg，`
      + `**已越过限量值 ${limit} g/kg**（超 ${round2(usage - limit * kg)} g）—— 带入的也得算进总量。`,
      'GB 2760 的带入原则不是免死金牌：由配料带入的添加剂连同本厂直接添加的量**合并后**仍不得超过'
      + '该类别该添加剂的最大使用量。把配料用量与配料本身的添加剂含量都算进来，'
      + '要么换一种不含该添加剂的配料，要么调低本厂直接添加的量。')];
  }
  if (!carryOnly) return [];
  return [finding('P0', '带入量未计入总量', it, undefined,
    `${who(it)}：食品类别「${cell(it, 'foodCategory') || '(未填)'}」只允许「${additive}」由配料带入，`
    + `第 ${it.line} 行却按直接投料记录（使用量 ${cell(it, 'usageG') || '(未填)'} g），备注里也没有带入来源`
    + ' —— **配料带入原则没有被执行，带入量也没有并进总量**。',
    '两件事一起做：① 把这一行改成配料带入（备注写明是哪种配料、用了多少）；'
    + '② 把该配料按自身含量换算出来的添加剂量并进本批总量，再与限量值比对。'
    + '直接投料且不并入总量，等于既超范围又超限量。')];
}

function checkFunctionClassSum(items, ctx) {
  // 付费 ④：同一功能类别多品种叠加的相对量合计 > 100%（同一功能下的比例之和）
  const out = [];
  const groups = new Map();
  const seen = new Set();
  for (const it of items) {
    if (it.isTotal) continue;
    const fc = cell(it, 'functionClass');
    const batch = cell(it, 'batchNo');
    const a = cell(it, 'additiveName');
    const usage = normNumber(it.usageG);
    const kg = normNumber(it.batchKg) || batchKgOf(batch, ctx.detail);
    const limit = normNumber(it.limitGkg);
    if (!fc || !batch || !a || usage === null || limit === null || kg === null || kg <= 0 || limit <= 0) continue;
    // ⚠️ 必须按「产品 × 批次 × 功能类别 × 添加剂」去重：台账里同一添加剂重复记了两行时，
    //    不能把同一个品种算两遍（重复行由第 ④ 项单独点名），否则叠加相对量会被凭空放大。
    const dedupKey = cell(it, 'productName') + '||' + batch + '||' + fc + '||' + a;
    if (seen.has(dedupKey)) continue;
    seen.add(dedupKey);
    const key = batch + '||' + fc;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push({ it, fc, batch, usage, kg, limit, share: usage / kg / limit });
  }
  for (const list of groups.values()) {
    if (list.length < 2) continue;
    const sum = list.reduce((acc, x) => acc + x.share, 0);
    if (sum <= 1 + RATIO_TOL) continue;
    const parts = list.map((x) => `${cell(x.it, 'additiveName')} ${round4(x.share)}`).join(' + ');
    for (const x of list) {
      out.push(finding('P1', '同功能相对量合计超 100%', x.it, round2(sum * 100 - 100),
        `${who(x.it)}：批次 ${x.batch} 的「${x.fc}」下各品种相对量合计 = ${parts} = **${round4(sum)}**`
        + `（> 100%，超出 ${round4((sum - 1) * 100)}%）。单一品种都没超限量，叠加起来超了。`,
        'GB 2760 对同一功能的多种添加剂有「相对量合计不得超过 1」的口径：'
        + '先按上面的比例把其中最不必要的一种减下来（或换功能类别不同的替代品），'
        + '让合计回到 100% 以内，再把各行的使用量填回去重跑。'));
    }
  }
  return out;
}

function groupActionFor(v) {
  // 付费 ⑤：每一组给一条可整改动作（先解决最要命的：超限量 / 超范围）
  if (v.out_of_scope_count > 0) {
    return `本组有 ${v.out_of_scope_count} 行超范围使用：按 GB 2760 拿掉不允许用于该类别的添加剂，改配方并留变更记录`;
  }
  if (v.rows_over > 0) {
    return `本组 ${v.rows_over} 行超限量（最高使用率 ${v.ratio_max}）：按差额调低投料量或扩大批量，改完重算合计`;
  }
  if (v.relative_over > 0) {
    return `本组同功能相对量合计超 100%：减少其中最不必要的一个品种，把合计压回 100% 以内`;
  }
  if (v.compound_diff > 0) {
    return `本组复配添加剂拆分对不上：按复配产品组分表核对各单体占比与单体记录`;
  }
  if (v.carryin_missing > 0) {
    return `本组有 ${v.carryin_missing} 行配料带入未处理：写明带入来源并把带入量并进总量`;
  }
  if (v.duplicate > 0) {
    return `本组有 ${v.duplicate} 行重复投料：确认真投两次还是重复记录，合并后重算合计`;
  }
  return '本组未发现超限量 / 超范围 / 叠加超 100% 的问题，保持现有投料记录口径即可';
}

function buildRollup(agg) {
  // 付费 ⑤：分产品 × 分添加剂的汇总清单（超出倍数降序 + 每组可整改动作）
  const blank = () => ({
    rows: 0, usage_g_total: 0, batch_kg_total: 0,
    rows_over: 0, ratio_max: 0, over_g_total: 0,
    out_of_scope_count: 0, relative_over: 0, compound_diff: 0,
    carryin_missing: 0, duplicate: 0,
  });
  const add = (bk, a) => {
    bk.rows += a.rows;
    bk.usage_g_total = round2(bk.usage_g_total + a.usage_g_total);
    bk.batch_kg_total = round2(bk.batch_kg_total + a.batch_kg_total);
    bk.rows_over += a.rows_over;
    bk.ratio_max = Math.max(bk.ratio_max, a.ratio_max);
    bk.over_g_total = round2(bk.over_g_total + a.over_g_total);
    bk.out_of_scope_count += a.out_of_scope_count;
    bk.relative_over += a.relative_over;
    bk.compound_diff += a.compound_diff;
    bk.carryin_missing += a.carryin_missing;
    bk.duplicate += a.duplicate;
    return bk;
  };
  const byProduct = new Map();
  const byAdditive = new Map();
  const byProductAdditive = new Map();
  for (const a of agg) {
    const kp = a.product_name || '(未填产品)';
    const ka = a.additive_name || '(未填添加剂)';
    const kpa = kp + ' × ' + ka;
    if (!byProduct.has(kp)) byProduct.set(kp, blank());
    if (!byAdditive.has(ka)) byAdditive.set(ka, blank());
    if (!byProductAdditive.has(kpa)) byProductAdditive.set(kpa, blank());
    add(byProduct.get(kp), a);
    add(byAdditive.get(ka), a);
    add(byProductAdditive.get(kpa), a);
  }
  const toRows = (map, keyName) => [...map.entries()]
    .map(([k, v]) => Object.assign({ [keyName]: k, action: groupActionFor(v) }, v))
    .sort((x, y) => (y.ratio_max - x.ratio_max)
      || (y.over_g_total - x.over_g_total)
      || String(x[keyName]).localeCompare(String(y[keyName])));
  return {
    by_product: toRows(byProduct, 'product_name'),
    by_additive: toRows(byAdditive, 'additive_name'),
    by_product_additive: toRows(byProductAdditive, 'product_additive'),
    total: agg.reduce((acc, a) => add(acc, a), blank()),
    basis: '按「产品」「添加剂」「产品 × 添加剂」三档分组：每组给出明细行数、使用量合计(g)、批量合计(kg)、'
      + '超限量的行数、最高使用率（使用量比例 ÷ 限量值）、超限量合计(g)、超范围行数、'
      + '同功能相对量合计超 100% 的次数、复配拆分不符次数、配料带入未处理行数与重复投料行数；'
      + '排序按「最高使用率 → 超限量合计」降序，每组附一条可整改动作。',
  };
}

function buildConsolidatedActions(agg) {
  // 付费 ⑤：把每一行的添加剂问题合并成一张整改清单（超出倍数降序 → 行号）
  const rows = [];
  for (const a of agg) {
    const issues = [];
    if (a.out_of_scope_count > 0) issues.push(`超范围使用 ${a.out_of_scope_count} 处`);
    if (a.rows_over > 0) issues.push(`超限量 ${a.rows_over} 行（最高使用率 ${a.ratio_max}，超 ${a.over_g_total} g）`);
    if (a.relative_over > 0) issues.push(`同功能相对量合计超 100%（${a.relative_over} 次）`);
    if (a.compound_diff > 0) issues.push(`复配拆分不符 ${a.compound_diff} 处`);
    if (a.carryin_missing > 0) issues.push(`配料带入未处理 ${a.carryin_missing} 行`);
    if (a.duplicate > 0) issues.push(`重复投料行 ${a.duplicate} 行`);
    if (!issues.length) continue;
    let action;
    if (a.out_of_scope_count > 0) action = '按 GB 2760 核对本类别允许清单 → 停用不允许的添加剂 → 改配方并留变更记录';
    else if (a.rows_over > 0) action = '按超出量调低投料量或扩大批量 → 修正使用量/批量两列 → 重算合计行';
    else if (a.relative_over > 0) action = '减少同功能中最不必要的一个品种 → 使相对量合计 ≤ 100% → 重跑';
    else if (a.compound_diff > 0) action = '对照复配产品组分表 → 改正占比或补单体记录 → 重新拆分核算';
    else if (a.carryin_missing > 0) action = '备注写明带入来源 → 把带入量并进本批总量 → 与限量值重新比对';
    else action = '确认真投两次还是重复记录 → 合并或删除重复行 → 修平合计行';
    rows.push({
      product_name: a.product_name,
      additive_name: a.additive_name,
      function_class: a.function_class,
      line: a.line,
      batch_no: a.batch_no,
      level: (a.out_of_scope_count > 0 || a.ratio_max > 1.2) ? 'P0' : 'P1',
      ratio_max: a.ratio_max,
      over_g_total: a.over_g_total,
      issue: issues.join('；'),
      action,
    });
  }
  rows.sort((x, y) => (y.ratio_max - x.ratio_max) || (y.over_g_total - x.over_g_total) || (x.line - y.line));
  return rows.map((r, i) => Object.assign({ seq: i + 1 }, r));
}

function buildRowAggregates(items, ctx) {
  // 付费 ⑤ 的取数：逐行算使用率、超限量、超范围、叠加、复配、带入、重复
  const seen = new Map();
  const dupLines = new Set();
  for (const it of items) {
    if (it.isTotal) continue;
    const batch = cell(it, 'batchNo');
    const a = cell(it, 'additiveName');
    if (!batch || !a) continue;
    const key = batch + '||' + a;
    if (seen.has(key)) dupLines.add(it.line); else seen.set(key, it.line);
  }
  const overFLines = new Set();
  const outFLines = new Set();
  const relFLines = new Set();
  const compFLines = new Set();
  const carryFLines = new Set();
  for (const f of ctx.extra) {
    if (f.category === '超限量使用') overFLines.add(f.line);
    if (f.category === '超范围使用') outFLines.add(f.line);
    if (f.category === '同功能相对量合计超 100%') relFLines.add(f.line);
    if (f.category === '复配拆分不符') compFLines.add(f.line);
    if (f.category === '带入量未计入总量') carryFLines.add(f.line);
  }
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const usage = normNumber(it.usageG);
    const kg = normNumber(it.batchKg);
    const limit = normNumber(it.limitGkg);
    let ratio = 0;
    let overG = 0;
    if (usage !== null && kg !== null && limit !== null && kg > 0 && limit > 0) {
      ratio = round4(usage / kg / limit);
      if (ratio > 1 + RATIO_TOL) overG = round2(usage - limit * kg);
    }
    out.push({
      product_name: cell(it, 'productName'),
      batch_no: cell(it, 'batchNo'),
      additive_name: cell(it, 'additiveName'),
      function_class: cell(it, 'functionClass'),
      line: it.line,
      rows: 1,
      usage_g_total: usage === null ? 0 : round2(usage),
      batch_kg_total: kg === null ? 0 : round2(kg),
      rows_over: ratio > 1 + RATIO_TOL ? 1 : 0,
      ratio_max: ratio,
      over_g_total: overG,
      out_of_scope_count: outFLines.has(it.line) ? 1 : 0,
      relative_over: relFLines.has(it.line) ? 1 : 0,
      compound_diff: compFLines.has(it.line) ? 1 : 0,
      carryin_missing: carryFLines.has(it.line) ? 1 : 0,
      duplicate: dupLines.has(it.line) ? 1 : 0,
    });
  }
  return out;
}

/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的食品添加剂投料与使用台账']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的食品添加剂投料与使用台账']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的食品添加剂投料与使用台账（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.detail.length) {
    return insufficient(['至少一行投料明细（现在只有表头或只有合计行，没有可核对的添加剂投料）']);
  }

  const paid = Boolean(p.full || p.credit || p.token);
  const base = baseDateOf(t.items);
  const findings = [];
  const notRun = [];
  const dataNotes = [];
  let rollup = null;
  let consolidated = null;

  for (const f of checkUsageRatio(t.items, base)) findings.push(f);
  for (const f of checkLimitConsistency(t.items)) findings.push(f);
  for (const f of checkLabelConsistency(t.items)) findings.push(f);
  for (const f of checkDuplicateRows(t.items)) findings.push(f);
  for (const f of checkTotals(t.items, t.cols)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

  if (paid) {
    const ctx = { base, detail: t.detail, extra: [] };
    for (const it of t.items) {
      for (const f of checkOutOfScope(it)) { findings.push(f); ctx.extra.push(f); }
      for (const f of checkCompoundSplit(it, ctx)) { findings.push(f); ctx.extra.push(f); }
      for (const f of checkCarryIn(it, ctx)) { findings.push(f); ctx.extra.push(f); }
    }
    for (const f of checkFunctionClassSum(t.items, ctx)) { findings.push(f); ctx.extra.push(f); }

    const compoundRows = t.detail.filter((it) => isCompound(it));
    const noMember = compoundRows.filter((it) => !parseCompoundMembers(it).length);
    if (noMember.length) {
      dataNotes.push('有 ' + noMember.length + ' 行复配添加剂（原文第 '
        + noMember.map((it) => it.line).slice(0, 5).join('、') + ' 行）名称与备注里拆不出各单体与占比：'
        + '这几行的**拆分核算本次没有执行** —— 不等于它们对得上。');
    }
    const unknownCats = [...new Set(t.detail.map((it) => cell(it, 'foodCategory'))
      .filter((c) => c && !ALLOW_BY_CATEGORY[c]))];
    if (unknownCats.length) {
      dataNotes.push('这些食品类别不在内置的**类别-允许表**里：' + unknownCats.join('、')
        + ' —— 它们的**超范围使用本次没有执行**（判不了），不等于它们合规；'
        + '请按 GB 2760 现行版本把类别与允许添加剂补进白名单。');
    }

    const agg = buildRowAggregates(t.items, ctx);
    rollup = buildRollup(agg);
    consolidated = buildConsolidatedActions(agg);
  } else {
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  }

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const overRows = findings.filter((f) => f.category === '超限量使用');
  const ratioMax = overRows.reduce((m, f) => Math.max(m, f.usage_ratio || 0), 0);

  const result = {
    findings,
    summary: {
      rows: t.detail.length,
      total_rows: t.totalRows.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      usage_g_total: t.totals.usageG,
      batch_kg_total: t.totals.batchKg,
      rows_over_limit: overRows.length,
      ratio_max: ratioMax,
      check_date: base,
      basis: '使用量按比例复算：使用量g ÷ 批量kg ≤ 限量值g/kg 才算没超限量（超出倍数 = 比例 ÷ 限量值）；'
        + '同一产品同一添加剂的限量值只能有一个口径，出现两个即点名；'
        + '标签配料表标注与投料记录里的添加剂必须互相能对上（含复配拆分后的单体名）；'
        + '同一批次同一添加剂只允许一行；'
        + '合计行（使用量合计、批量合计）必须等于明细行逐列加总；'
        + '使用量 / 批量 / 限量值都必须为正数，日期只认 2026-03-31 这几种形态。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这本投料台账按上面写明的口径算得对、'
      + '限量口径一致、配料表标注与投料记录能对上**，不代表 GB 2760 的现行允许清单已经由监管确认、'
      + '不代表标签实物与配料表一致、也不代表检验报告合格 —— 那些不在本工具范围内。'
      + (dataNotes.length ? '（注意：' + dataNotes.join('；') + '）' : '');
  }

  const scope = {
    checks: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.detail.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    usage_g_total: t.totals.usageG,
    batch_kg_total: t.totals.batchKg,
    check_date: base,
  };
  result.scope = scope;
  if (dataNotes.length) result.data_notes = dataNotes;

  if (paid) {
    result.rollup = rollup;
    result.consolidated_actions = consolidated;
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, normDate, round2, round4, isBlank, splitRow,
  parseLabel, parseCompoundMembers, isCompound, ALLOW_BY_CATEGORY, CARRYIN_ONLY,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
  CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
