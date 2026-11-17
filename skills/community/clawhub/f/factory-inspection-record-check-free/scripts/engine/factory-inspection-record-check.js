#!/usr/bin/env node
/**
 * factory-inspection-record-check-full.js —— 食品出厂检验与留样记录核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：食品生产企业**每批产品出厂前必须检验**（检验项目按产品标准执行）、**每批留样**
 * 并保存到保质期后（一般不少于保质期），监管抽查与第三方审核最常见的整改项就是：
 *   ① 出厂检验缺项 / 缺批次（某批没过检就发货，或标准要求 5 个项目只做了 3 个）
 *   ② 留样数量不足、或留样提前销毁（销毁日期早于「留样日期 + 留样期限」）
 *   ③ 检验数据与出厂检验报告不一致（记录写「合格」，报告结论却是「待复检」）
 *   ④ 不合格品没有处置闭环（判了不合格，处置结论/处置日期/复核人三项缺一项都说不清）
 *   ⑤ 同一批次跨生产线 / 跨班次生产（防混批：同批号出现在两条线上就无法追溯）
 * 品控 / 质量部每月必须把这张台账核一遍：批次覆盖、项目齐全、留样与销毁期限、
 * 不合格处置闭环、记录与报告一致 —— 每一项都要能追溯到原文。
 *
 * 本文件同时是**免费档**的来源：`tools/strip_free_engine.py` 从本文件摘出免费档子集
 * （摘掉完整档整块实现与那一个付费开关）；`CHECKS_WITHHELD` 是"未执行的检查项"的说明文本，
 * 不是实现。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定检验项目本身是否适用于该产品（那要按产品执行标准判定）、不判定检验方法与
 *          检验结果本身是否科学准确（那是检验机构与检验员的职责）、不判定留样是否被真实动用、
 *          不读 .xlsx/.pdf 原件、不联网核验报告真伪；材料不足**一律不给结论**。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '批次检验覆盖（逐批核对是否检验：检验日期缺失、检验结果缺失或日期不可解析的批次逐批点名）',
  '检验项目齐全性（检验项目数 ≥ 规定检验项目数，不足报出差额；有清单与规定项目两列时点名缺哪项）',
  '留样期限（留样日期 + 留样期限(天) = 应销毁日期；基准日早于应销毁日期即报出，并报销毁日期早于该日期的行）',
  '同一生产批次 + 同一检验项目重复登记检测（同批同项目出现两次以上即点名）',
  '合计行逐列复核（批次数、留样数量、检验项目数三类合计列与逐行加总比对，差额不为零即列出）',
  '空白与占位符、日期格式、数值为负或无法解析、状态值非法（合格/不合格/待检/复检之外的值逐处点名）',
];

const CHECKS_WITHHELD = [
  '不合格品处置闭环（检验结果=不合格 但缺处置结论/处置日期/复核人 ⇒ 点名并按超期天数排序）',
  '检验数据与报告一致性（报告结论与检验记录结论不一致时把两处原文都列出来）',
  '留样数量达标（单批留样数量 < 规定留样数量，报出差额）',
  '同批产品跨生产线/跨班次（同一批次出现在多条生产线或多个班次，防混批点名）',
  '分产品×分班次汇总清单（按不合格数与缺检批次排序，给出可整改动作）',
];

const OUT_OF_SCOPE = [
  '判定出厂检验项目本身是否适用于该产品（那要按产品执行标准与生产许可审查细则认定），本工具只核台账字面',
  '判定检验方法与检验结果是否科学准确、是否合格（那是检验机构与检验员的职责），本工具只核记录内部一致性',
  '判定留样是否被真实动用、留样样品是否真实存在（那是现场检查与留样实物核对的职责）',
  '读取 .xlsx/.pdf 原件、联网核验检验报告真伪、替代监管部门抽检结论或第三方审核意见',
];

// 检验结果 / 报告结论允许出现的状态值（其余值一律点名）
const RESULT_STATUS = ['合格', '不合格', '待检', '复检'];
// 不合格处置结论里应该看得到"处置动作"痕迹（空白/占位符另有检查，这里只点"写了但不含动作"的）
const DISPOSAL_HINT = /(已|报废|销毁|退货|召回|返工|降级|让步|隔离|处置|处理|封存|转料)/;

const DAY = 86400000;
const DATE_RE = /^(\d{4})[-/.年](\d{1,2})[-/.月](\d{1,2})日?$/;

const CHECKS_OUT_OF_SCOPE = OUT_OF_SCOPE;

// 样例：一张**干净**的食品出厂检验与留样台账 —— 四个批次、两个班次、两条生产线，
// 检验项目数 = 规定项目数、留样数量达标、销毁日期 = 留样日期 + 留样期限(天) 且都在基准日之后、
// 报告结论与检验结果一致、没有同一批次跨线/跨班次，合计行与逐行加总一致。
const SAMPLE_TEXT = [
  '生产批次\t产品名称\t规格\t生产日期\t保质期至\t检验日期\t检验项目数\t规定检验项目数\t检验结果\t留样日期\t留样数量\t规定留样数量\t留样期限(天)\t销毁日期\t不合格处置\t处置日期\t复核人\t报告结论\t生产线\t班次\t核对日期\t备注',
  'P2026-0413-01\t老面馒头\t500g/袋\t2026-04-13\t2027-04-13\t2026-04-14\t5\t5\t合格\t2026-04-14\t3\t2\t180\t2026-10-11\t无需处置\t\t\t合格\t一号线\t早班\t2026-06-30\t当日检验当日留样',
  'P2026-0420-02\t原味豆奶\t250mL/盒\t2026-04-20\t2026-10-17\t2026-04-21\t6\t6\t合格\t2026-04-21\t4\t2\t180\t2026-10-18\t无需处置\t\t\t合格\t一号线\t早班\t2026-06-30\t商业无菌项目外送检验',
  'P2026-0506-03\t五香酱牛肉\t200g/袋\t2026-05-06\t2026-08-04\t2026-05-07\t5\t5\t合格\t2026-05-08\t2\t2\t90\t2026-08-06\t无需处置\t\t\t合格\t二号线\t中班\t2026-06-30\t留样冷库 A 区',
  'P2026-0518-04\t速冻荠菜水饺\t1kg/袋\t2026-05-18\t2027-05-18\t2026-05-19\t7\t7\t合格\t2026-05-21\t3\t3\t90\t2026-08-19\t无需处置\t\t\t合格\t二号线\t中班\t2026-06-30\t速冻库 -18℃',
  '合计\t\t\t\t\t\t23\t23\t\t\t12\t9\t\t\t\t\t\t\t\t\t\t4 个批次',
].join('\n');

const TOL = 0.01;

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = [
  'batchNo', 'productName', 'spec', 'prodDate', 'shelfLifeEnd', 'inspectDate', 'itemCount',
  'reqItemCount', 'inspectResult', 'retainDate', 'retainQty', 'retainDays', 'destroyDate',
  'disposal', 'checkDate',
];

// 日期角色（格式 / 先后关系都要核）
const DATE_LABELS = [
  ['prodDate', '生产日期'],
  ['shelfLifeEnd', '保质期至'],
  ['inspectDate', '检验日期'],
  ['retainDate', '留样日期'],
  ['destroyDate', '销毁日期'],
  ['disposalDate', '处置日期'],
  ['checkDate', '核对日期'],
];

// 数值角色（空白 ⇒ 缺失；为负或无法解析 ⇒ 逐处点名）
const NUMBER_LABELS = [
  ['itemCount', '检验项目数'],
  ['reqItemCount', '规定检验项目数'],
  ['retainQty', '留样数量'],
  ['reqRetainQty', '规定留样数量'],
  ['retainDays', '留样期限(天)'],
];

// 单元格级必需文本字段（空白 / 占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['batchNo', '生产批次'],
  ['productName', '产品名称'],
  ['inspectDate', '检验日期'],
  ['inspectResult', '检验结果'],
];

// 状态值的两处（只接受 合格 / 不合格 / 待检 / 复检）
const STATUS_FIELDS = [
  ['inspectResult', '检验结果'],
  ['reportResult', '报告结论'],
];

// 合计行要逐列复核的数量类列
const SUM_ROLES = ['itemCount', 'reqItemCount', 'retainQty', 'reqRetainQty', 'retainDays'];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词会抢走更具体的列（本仓库踩过六次，见 tools/header_map_check.py）。
//    ⚠️ 铁律：**要两遍扫描**。第一遍只跑"具体别名"，第二遍才跑"兜底别名" ——
//    因为角色是按对象键顺序整体遍历的，只要有一个角色的兜底别名（如「批次」「项目数」「处置」）
//    排在另一个角色的具体别名前面，就会把更具体的列抢走（`规定检验项目数` 被 `检验项目数` 抢、
//    `规定留样数量` 被 `留样数量` 抢、`处置日期` 被 `处置` 抢、`生产日期` 被 `生产批次` 抢）。
//    实测这四种抢列都不会报缺列，只会静默算错（本仓库同类坑踩过六次）。
const ROLES_SPECIFIC = {
  batchNo: ['生产批次', '生产批号', '产品批号'],
  productName: ['产品名称', '品名'],
  spec: ['规格型号', '规格'],
  prodDate: ['生产日期', '生产时间'],
  shelfLifeEnd: ['保质期至', '保质期到', '保质期止', '保存期限至', '货架期至'],
  inspectDate: ['检验日期', '检测日期', '检验时间'],
  itemCount: ['检验项目数', '检测项目数'],
  reqItemCount: ['规定检验项目数', '应检项目数', '标准检验项目数', '规定项目数'],
  inspectItemList: ['检验项目清单', '检测项目清单', '检验项目名称'],
  requiredItemList: ['规定检验项目', '应检项目', '标准检验项目', '规定项目'],
  inspectResult: ['检验结果', '检验结论', '检测结果', '判定结果'],
  reportResult: ['报告结论', '报告判定', '检验报告结论'],
  retainDate: ['留样日期', '留样时间'],
  retainQty: ['留样数量', '留样件数'],
  reqRetainQty: ['规定留样数量', '留样数量规定', '应留样数量'],
  retainDays: ['留样期限(天)', '留样期限（天）', '留样期限', '留样天数'],
  destroyDate: ['销毁日期', '留样销毁日期'],
  disposal: ['不合格处置', '不合格品处置', '处置结论', '处置方式', '处置措施'],
  disposalDate: ['处置日期', '处置时间'],
  reviewer: ['复核人', '审核人', '批准人'],
  // ⛔ 角色名不能叫 `line`：行的行号字段就叫 `line`，会被解析覆盖（实测结论带的行号变成「一号线」）。
  prodLine: ['生产线', '产线', '线别'],
  shift: ['班次', '排班'],
  checkDate: ['核对日期', '核查日期', '核对时间'],
  note: ['备注', '附注'],
};

//    ⚠️ 第二遍才跑的兜底别名：宽泛词一律放这里（顺序仍按具体度从高到低）。
const ROLES_FALLBACK = {
  batchNo: ['批号', '批次'],
  productName: ['产品'],
  shelfLifeEnd: ['保质期'],
  itemCount: ['项目数'],
  inspectItemList: ['检验项目'],
  disposal: ['处置'],
  reviewer: ['复核'],
  note: ['说明'],
};

// 对外暴露的合并视图（保留原键顺序：具体别名在前、兜底在后）
const ROLES = (() => {
  const out = {};
  for (const k of Object.keys(ROLES_SPECIFIC)) {
    out[k] = ROLES_SPECIFIC[k].concat(ROLES_FALLBACK[k] || []);
  }
  return out;
})();

const LABELS = {
  batchNo: '生产批次',
  productName: '产品名称',
  spec: '规格',
  prodDate: '生产日期',
  shelfLifeEnd: '保质期至',
  inspectDate: '检验日期',
  itemCount: '检验项目数',
  reqItemCount: '规定检验项目数',
  inspectItemList: '检验项目清单',
  requiredItemList: '规定检验项目',
  inspectResult: '检验结果',
  reportResult: '报告结论',
  retainDate: '留样日期',
  retainQty: '留样数量',
  reqRetainQty: '规定留样数量',
  retainDays: '留样期限(天)',
  destroyDate: '销毁日期',
  disposal: '不合格处置',
  disposalDate: '处置日期',
  reviewer: '复核人',
  prodLine: '生产线',
  shift: '班次',
  checkDate: '核对日期',
  note: '备注',
};

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张台账补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说"批次齐全/记录一致"，也不说"有问题"。',
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

function round2(n) {
  return Math.round(n * 100) / 100;
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定|待核)$/i.test(s);
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
}

function roleOf(header) {
  const h = String(header == null ? '' : header).replace(/[\s（）()：:]/g, '');
  if (!h) return null;
  // 第一遍：具体别名；第二遍：兜底别名。
  // 每一遍里都**先长后短**：长别名天然更具体（`规定检验项目数` 比 `检验项目数` 长 ⇒ 先匹配它），
  // 这样兜底词与容器词就都抢不走更具体的列（本仓库同类坑踩过六次）。
  for (const table of [ROLES_SPECIFIC, ROLES_FALLBACK]) {
    const rules = [];
    for (const [role, keys] of Object.entries(table)) {
      for (const k of keys) {
        const kk = String(k).replace(/[\s（）()：:]/g, '');
        if (kk) rules.push([kk, role]);
      }
    }
    rules.sort((a, b) => (b[0].length - a[0].length) || a[1].localeCompare(b[1]));
    for (const [k, role] of rules) {
      if (h.indexOf(k) >= 0) return role;
    }
  }
  return null;
}

/** 标准日期串 YYYY-MM-DD，解析不出来返回 null（"没填"与"填错了"由调用方用 isBlank 区分） */
function normDate(raw) {
  if (raw === undefined || raw === null) return null;
  const m = DATE_RE.exec(String(raw).trim());
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const dt = new Date(Date.UTC(y, mo - 1, d));
  if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== mo - 1 || dt.getUTCDate() !== d) return null;
  return `${m[1]}-${String(mo).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
}

const toMs = (iso) => Date.UTC(Number(iso.slice(0, 4)), Number(iso.slice(5, 7)) - 1, Number(iso.slice(8, 10)));

/** 日期加减天数（只认 normDate 过了的串） */
function addDays(iso, n) {
  const dt = new Date(toMs(iso) + n * DAY);
  return `${dt.getUTCFullYear()}-${String(dt.getUTCMonth() + 1).padStart(2, '0')}-${String(dt.getUTCDate()).padStart(2, '0')}`;
}

/** b − a 的天数（都是标准串） */
function diffDays(a, b) {
  return Math.round((toMs(b) - toMs(a)) / DAY);
}

/** 把「留样期限(天)」变成非负整数天；解析不了 / 为负 / 带小数返回 null */
function retainTermDays(raw) {
  const n = normNumber(raw);
  if (n === null) return null;
  const v = Math.trunc(n);
  if (v < 0 || Math.abs(n - v) > 0.0001) return null;
  return v;
}

/** 这一行是不是合计 / 汇总行（合计行不参与逐行检查，单独做逐列复核） */
function isSummaryRow(it) {
  const b = String(it.batchNo == null ? '' : it.batchNo).trim();
  if (/^(合计|总计|小计|汇总|总共)/.test(b)) return true;
  return /^(合计|总计|小计|汇总)/.test(String(it.productName == null ? '' : it.productName).trim());
}

/** 解析成 {header, cols, items, summary, totals, missingRoles, missingColumns, error}；行是**扁平**对象：{line, raw, 角色:值…} */
function parseTable(text) {
  const rawLines = String(text == null ? '' : text).split(/\r?\n/);
  const rows = [];
  for (let i = 0; i < rawLines.length; i++) {
    if (String(rawLines[i]).trim() === '') continue;
    rows.push({ line: i + 1, raw: String(rawLines[i]) });
  }
  if (!rows.length) {
    return {
      error: 'empty', header: [], lines: 0, cols: [], items: [], summary: null, itemCount: 0,
      totals: {}, missingRoles: REQUIRED_ROLES.slice(),
      missingColumns: REQUIRED_ROLES.map((r) => LABELS[r]),
    };
  }

  const header = splitRow(rows[0].raw);
  const cols = header.map((h, k) => ({ header: h, role: roleOf(h), index: k }));
  const all = [];
  for (let r = 1; r < rows.length; r++) {
    const cells = splitRow(rows[r].raw);
    const it = { line: Number(rows[r].line), raw: rows[r].raw };
    for (const c of cols) {
      if (!c.role) continue;
      it[c.role] = cells[c.index] === undefined ? '' : cells[c.index];
    }
    all.push(it);
  }

  let summary = null;
  const items = [];
  for (const it of all) {
    if (!summary && isSummaryRow(it)) { summary = it; continue; }
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
    lines: rows.length,
    cols,
    items,
    summary,
    itemCount: items.length,
    totals,
    missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  };
}

const num = (it, role) => {
  const n = normNumber(it[role]);
  return n === null ? 0 : n;
};

function fmtNum(n) {
  return String(round2(Math.abs(n) < 0.005 ? 0 : n));
}

function txt(it, role) {
  return String(it[role] == null ? '' : it[role]).trim();
}

function who(it) {
  const b = txt(it, 'batchNo');
  const name = txt(it, 'productName');
  if (b && name) return `第 ${it.line} 行「批次 ${b} / ${name}」`;
  if (b) return `第 ${it.line} 行「批次 ${b}」`;
  if (name) return `第 ${it.line} 行「${name}」`;
  return `第 ${it.line} 行「未填批次」`;
}

/** 行内定位标签：批次 + 检验日期 / 留样日期等 */
function tag(it, extra) {
  const parts = [];
  const b = txt(it, 'batchNo');
  const name = txt(it, 'productName');
  const idate = txt(it, 'inspectDate');
  const rdate = txt(it, 'retainDate');
  if (b) parts.push(`批次 ${b}`);
  if (name) parts.push(name);
  if (idate) parts.push(`检验日期 ${idate}`);
  if (rdate) parts.push(`留样日期 ${rdate}`);
  if (extra) parts.push(extra);
  return parts.join('，');
}

function finding(level, category, line, message, advice, diff) {
  const f = { level, category, line, message };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

/** "清单"型单元格 → 去重后的条目数组（分号/逗号/顿号/斜杠分隔） */
function listCells(v) {
  const out = [];
  for (const s of String(v == null ? '' : v).split(/[;；,，、/|]+/)) {
    const x = s.trim();
    if (x === '' || isBlank(x)) continue;
    if (out.indexOf(x) < 0) out.push(x);
  }
  return out;
}

/** 有清单列时用它数项目数，没有就用声明的「检验项目数」列 */
function listedItemCount(it) {
  const list = listCells(it.inspectItemList);
  if (list.length) return list.length;
  return normNumber(it.itemCount);
}

/* ============================ 免费档检查（六项） ============================ */

/** 1. 批次检验覆盖：逐批核对"是否检验"（检验日期缺失 / 结论缺失 / 日期不可解析都算缺检） */
function checkBatchCoverage(items) {
  const out = [];
  for (const it of items) {
    const rawDate = txt(it, 'inspectDate');
    const rawRes = txt(it, 'inspectResult');
    const badDate = rawDate !== '' && normDate(rawDate) === null;
    const missDate = rawDate === '' || badDate;
    const missRes = isBlank(rawRes);
    if (!missDate && !missRes) continue;
    const lack = [];
    if (rawDate === '') lack.push('检验日期为空');
    else if (badDate) lack.push(`检验日期「${rawDate}」不是可识别的日期`);
    if (missRes) lack.push('检验结果为空（说明不了这一批到底检没检）');
    out.push(finding('P0', '批次未检验', it.line,
      `${who(it)}：${tag(it)} —— 这一批没有可核对的出厂检验记录（${lack.join('；')}）。`
      + '出厂检验应当逐批做、逐批留记录，缺批次的批号无法证明出厂前检验过。',
      '把这一批的检验原始记录与出厂检验报告找出来；确实没做的要在不合格品/异常台账里说明去向'
      + '（返工、降级、报废），不能留空白。'));
  }
  return out;
}

/** 2. 检验项目齐全性：项目数 ≥ 规定项目数；有清单时点名缺哪一项 */
function checkItemCompleteness(items) {
  const out = [];
  for (const it of items) {
    const req = normNumber(it.reqItemCount);
    const have = listedItemCount(it);
    if (req === null || have === null) continue;                 // 缺列 / 空值交给别的检查项
    if (req < 0 || have < 0) continue;
    if (have + TOL >= req) continue;
    const list = listCells(it.inspectItemList);
    const required = listCells(it.requiredItemList);
    let detail;
    if (list.length) {
      const missed = required.filter((r) => !list.some((x) => x === r || x.indexOf(r) >= 0 || r.indexOf(x) >= 0));
      detail = `本行检验项目清单共 ${list.length} 项（${list.join('、')}）`
        + (required.length
          ? (missed.length
            ? `；按规定项目清单点名缺：${missed.join('、')}`
            : '；规定项目清单里没有整项缺失（差额可能来自项目重复登记）')
          : '；本行没有「规定检验项目」清单列，只能报出差额');
    } else {
      detail = `本行只填了 ${fmtNum(have)} 个检验项目（没有「检验项目清单」列，无法点名缺哪一项）`;
    }
    out.push(finding('P0', '检验项目缺项', it.line,
      `${who(it)}：${tag(it)} —— 规定检验项目数 ${fmtNum(req)}，实际 ${fmtNum(have)}，`
      + `差 ${fmtNum(req - have)} 项。${detail}。`,
      '按该产品的执行标准与生产许可审查细则把缺的项目补做，并在原始记录里留下数据；'
      + '缺项批次的出厂检验报告不能算齐全。', req - have));
  }
  return out;
}

/** 3. 留样期限：留样日期 + 留样期限(天) = 应销毁日期；基准日 < 应销毁日期 即报出 */
function checkRetainTerm(items) {
  const out = [];
  for (const it of items) {
    const rdate = normDate(it.retainDate);
    const days = retainTermDays(it.retainDays);
    if (rdate === null || days === null) continue;
    if (days <= 0) {
      out.push(finding('P0', '留样期限非法', it.line,
        `${who(it)}：${tag(it)} —— 留样期限填的是「${txt(it, 'retainDays')}」天；留样期限必须是正数天数`
        + '（一般口径：留样保存到保质期后，常用 保质期天数 或 保质期 + 6 个月）。',
        '按该产品保质期重新算留样期限并重算应销毁日期，别用 0 天或空值糊过去。'));
      continue;
    }
    const due = addDays(rdate, days);
    const rawDestroy = txt(it, 'destroyDate');
    const destroy = normDate(it.destroyDate);
    const basis = normDate(it.checkDate);

    if (rawDestroy !== '' && destroy === null) continue;         // 日期格式非法另有检查项
    if (destroy !== null) {
      if (diffDays(rdate, destroy) < 0) {
        out.push(finding('P0', '留样期限', it.line,
          `${who(it)}：${tag(it)} —— 销毁日期 ${destroy} 早于留样日期 ${rdate}（负数保存期），记录自相矛盾。`,
          '核对留样台账与销毁记录：销毁日期不可能早于留样日期，先确认是哪一处写错。'));
        continue;
      }
      if (diffDays(due, destroy) < 0) {
        const d = diffDays(destroy, due);
        out.push(finding('P0', '留样期限', it.line,
          `${who(it)}：${tag(it)} —— 留样日期 ${rdate} + 留样期限 ${days} 天 = 应销毁日期 ${due}，`
          + `但记录的销毁日期是 ${destroy}，提前销毁 ${d} 天。留样保存到保质期后是硬要求，提前销毁属整改项。`,
          '把留样实物与销毁审批单一起核：确属提前销毁的要有审批与原因，并评估该批次留样的可追溯性；'
          + '还没销毁的请把销毁日期清空（未销毁不要预填日期）。', -d));
      }
      continue;
    }

    if (basis !== null && diffDays(basis, due) < 0) {
      const d = diffDays(due, basis);
      out.push(finding('P1', '留样期限', it.line,
        `${who(it)}：${tag(it)} —— 留样日期 ${rdate} + 留样期限 ${days} 天 = 应销毁日期 ${due}，`
        + `但核对日期 ${basis} 已经到/过了应销毁日期 ${d} 天，销毁日期一栏仍是空的。`
        + '留样到期未处理（没销毁也没办延期）在审核里会被问"留样还在不在、保存期够不够"。',
        '清点该批留样实物：已销毁的补填销毁日期与审批单，仍需保存的办延期并在备注里写明原因。', d));
    }
  }
  return out;
}

/** 4. 同一生产批次 + 同一检验项目重复登记检测 */
function checkDuplicateEntry(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const batch = txt(it, 'batchNo');
    if (!batch) continue;
    const item = txt(it, 'inspectItemList') || '(未填检验项目)';
    const key = `${batch}|${item}`;
    if (!seen.has(key)) { seen.set(key, it); continue; }
    const first = seen.get(key);
    out.push(finding('P1', '同批同项重复登记', it.line,
      `${who(it)}：批次「${batch}」+ 检验项目「${item}」在第 ${first.line} 行已经登记过一次，`
      + `这里是第 ${it.line} 行又登记了一遍（原文：第 ${first.line} 行 `
      + `${txt(first, 'inspectDate') || '(无检验日期)'}，第 ${it.line} 行 ${txt(it, 'inspectDate') || '(无检验日期)'}）。`,
      '同一批同一项目只应有一条检验登记（复检请把状态写成「复检」并把两次数据分开列）；'
      + '重复行会让检验项目数与留样数量被重复计入合计。'));
  }
  return out;
}

/** 5. 合计行逐列复核（数量类列：批次数、留样数量、检验项目数） */
function checkSummaryRow(t) {
  const out = [];
  const s = t.summary;
  if (!s) return out;
  for (const role of SUM_ROLES) {
    const declared = normNumber(s[role]);
    if (declared === null) continue;                              // 合计列没填不在这里报（必需列另有把关）
    const actual = t.totals[role];
    const diff = round2(declared - actual);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding('P0', '合计行不符', s.line,
      `合计行（第 ${s.line} 行）「${LABELS[role]}」写的是 ${fmtNum(declared)}，`
      + `逐行加总（${t.itemCount} 行明细）是 ${fmtNum(actual)}，差 ${fmtNum(diff)}`
      + `（${diff > 0 ? '合计多' : '合计少'}）。原文：${s.raw}`,
      '合计列按明细重算一遍再报出；改过明细行却没重算合计是最常见的原因。', diff));
  }
  return out;
}

/** 6. 空白 / 占位符 / 日期格式 / 数值为负或无法解析 / 状态值非法 */
function checkFieldIntegrity(items) {
  const out = [];
  for (const it of items) {
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '空白与占位符', it.line,
        `${who(it)}：这些必需字段是空的或占位符 —— ${miss.join('、')}。（原文：${it.raw}）`,
        '空着的字段会让对应的核对整项做不了；补全后重跑，本工具不会替你猜一个默认值。'));
    }
    for (const [role, label] of DATE_LABELS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      if (normDate(raw) === null) {
        out.push(finding('P1', '日期格式非法', it.line,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的日期`
          + '（只认 2026-06-30 / 2026/6/30 / 2026年6月30日 这类真实存在的日期）。',
          '把日期改成标准形态（如 2026-06-30）再跑；本工具不会把看不懂的日期当成今天。'));
      }
    }
    for (const [role, label] of NUMBER_LABELS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        out.push(finding('P1', '非数值或负数', it.line,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的数字（只认数字、千分位、括号负数）。`,
          '把数量改成纯数字形态（如 3）再跑；本工具不会把看不懂的值当成 0。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '非数值或负数', it.line,
          `${who(it)}：「${label}」是负数（${fmtNum(n)}）—— 批次数、留样数量、检验项目数都不可能为负，`
          + '通常是填反了方向，或把红字冲销写进了数量列。',
          '确认是笔误还是冲销记录；确属冲销的请写在「备注」里并保留原值，别直接改成正数。', n));
      }
    }
    for (const [role, label] of STATUS_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const v = String(raw).trim();
      if (RESULT_STATUS.indexOf(v) >= 0) continue;
      out.push(finding('P1', '状态值非法', it.line,
        `${who(it)}：「${label}」填的是「${v}」，不在允许的取值里（只认 ${RESULT_STATUS.join(' / ')}）。`,
        '把状态改成这四个值之一；自造状态（如"已检""OK""通过"）会让批次覆盖与处置闭环两项失去判据。'));
    }
  }
  return out;
}

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的食品出厂检验与留样台账（含 生产批次/检验日期/留样日期 等列）']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的食品出厂检验与留样台账（含 生产批次/检验日期/留样日期 等列）']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的食品出厂检验与留样台账（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行批次明细（现在只有表头，没有可核对的批次行）']);
  }

  const findings = [];
  const notRun = [];

  for (const f of checkBatchCoverage(t.items)) findings.push(f);
  for (const f of checkItemCompleteness(t.items)) findings.push(f);
  for (const f of checkRetainTerm(t.items)) findings.push(f);
  for (const f of checkDuplicateEntry(t.items)) findings.push(f);
  for (const f of checkSummaryRow(t)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

  let consolidated = null;
  let lines = [];
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const allBasis = t.items.map((it) => normDate(it.checkDate)).filter((x) => x !== null).sort();
  const basisDate = allBasis.length ? allBasis[allBasis.length - 1] : null;
  const batches = t.items.filter((it) => txt(it, 'batchNo') !== '').length;
  const notInspected = findings.filter((f) => f.category === '批次未检验').length;
  const nonconforming = t.items.filter((it) => txt(it, 'inspectResult') === '不合格').length;

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      batches,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      not_inspected_batches: notInspected,
      nonconforming_batches: nonconforming,
      item_count_total: t.totals.itemCount,
      req_item_count_total: t.totals.reqItemCount,
      retain_qty_total: t.totals.retainQty,
      basis_date: basisDate,
      summary_row: t.summary ? t.summary.line : null,
      basis: '逐批核对是否检验（检验日期与检验结果都要有）；检验项目数须不小于规定检验项目数（有清单时点名缺项）；'
        + '留样日期 + 留样期限(天) = 应销毁日期，核对基准日早于应销毁日期即报出，销毁日期早于该日期也算提前销毁；'
        + '同一生产批次 + 同一检验项目只能登记一次；合计行的批次数 / 留样数量 / 检验项目数须等于逐行加总；'
        + '状态值只认 合格 / 不合格 / 待检 / 复检。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得对、该点的批次与项目都点到了**，'
      + '不代表检验项目本身适用于该产品、检验结果科学准确、留样实物真实存在或没被提前动用 —— 那些不在本工具范围内。';
  }

  result.scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.items.length,
    batches,
    columns_recognized: t.cols.filter((c) => c.role).length,
    lines,
    basis_date: basisDate,
    not_inspected_batches: notInspected,
    nonconforming_batches: nonconforming,
    item_count_total: t.totals.itemCount,
    req_item_count_total: t.totals.reqItemCount,
    retain_qty_total: t.totals.retainQty,
  };



  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
