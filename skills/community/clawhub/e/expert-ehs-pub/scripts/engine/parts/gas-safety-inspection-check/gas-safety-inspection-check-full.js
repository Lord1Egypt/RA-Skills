#!/usr/bin/env node
/**
 * gas-safety-inspection-check-full.js —— 燃气设施安全检查与隐患整改核对引擎（**订阅版 / 买断版**；确定性、纯 Node 标准库）。
 *
 * 真实痛点：燃气用户（餐饮门店、物业、工厂与学校食堂）**每月必须做一次安全检查**
 *   （管道、阀门、软管、报警器、切断阀、通风），要留**巡检记录**、要把**隐患整改闭环**、
 *   要给**燃气报警器做年检**。软管超期、报警器失效、隐患未整改，都是**燃气公司与监管的查封项**；
 *   一旦爆燃，企业要担责。安全管理员 / 门店店长每月要核的就是四件事：
 *   ① 检查频次与检查项目齐不齐 ② 软管与报警器的有效期 ③ 隐患整改闭环
 *   ④ 供应商资质与供气合同是否覆盖核对日期 ⑤ 这个月先改哪一个点位。
 *
 * 本文件是**订阅版（买断版）**：在本包六项逐行核对之上，多出**隐患整改闭环、检查项目不齐、
 * 软管/管件超期仍在用、燃气供应商资质与合同有效期覆盖、分点位类型×分门店汇总清单与合并整改动作**
 * 这五类能力。一次性买断，没有次数上限。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定燃气设施是否真的安全、不判定隐患是否已实质消除、不代替法定检验与监管认定、
 *          不读 .xlsx/.pdf/照片原件、不联网核验资质证书与检验报告真伪；材料不足**一律不给结论**。
 *
 * ⚠️ 免费包由 `tools/strip_free_engine.py` 从本文件摘出（**形态 B**）：付费开关**只在入口里声明一次**，
 *    付费检查一律包在受该开关控制的分支里；写注释时不要复述开关那一行的源码 ——
 *    摘除工具的残渣断言是**纯字符串包含**判断，复述会被判「没删干净」。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '检查频次覆盖（按点位核对 核对日期所在月 的实际检查次数：本月一次记录都没有的点位逐个点名；最新一条是「停用」的点位不报缺检）',
  '软管/管件有效期（逐行复算 检查日期 ≤ 软管更换到期日，超期即报并给出超期天数）',
  '燃气报警器年检（逐行复算 上次年检日期 + 年检周期(月) = 下次年检日期：日期不符即报，并与核对日期比出年检超期天数）',
  '同一点位同一检查日期重复登记（同一 点位编号 + 检查日期 出现多条即点名全部行号）',
  '合计行逐列复核（数量类列：点位数按去重计数，检查项数 / 规定检查项数 / 隐患数按明细行求和，逐列复算）',
  '关键字段缺失与取值非法（空白/占位符、日期格式、数值为负或无法解析、检查结果只能是 正常/隐患/停用/已整改）',
];

const CHECKS_WITHHELD = [
  '隐患整改闭环（检查结果=隐患 但缺「整改完成日期」或晚于整改期限日 ⇒ 点名，并按超期天数降序给出 closure_rank）',
  '检查项目不齐（检查项数 < 规定检查项数 ⇒ 给差额，并对照该点位类型的应检项清单点名缺哪几项）',
  '软管/管件超期仍在用（软管更换到期日早于核对日期，且该点位最新一次检查结果不是「停用」）',
  '燃气供应商资质与供气合同有效期覆盖（按门店核对 供应商资质到期日 / 供气合同到期日 是否覆盖核对日期）',
  '分点位类型 × 分门店汇总清单与合并整改动作（by_store / by_point_type / by_store_type 按隐患数与超期数排序 + consolidated_actions）',
];

const OUT_OF_SCOPE = [
  '判定燃气设施是否真的安全、隐患是否已经实质消除（那是现场检查与复检人员的判断），本工具只核记录表里的字面与算术',
  '判定是否达到燃气公司与监管的查封、停气或处罚标准，也不代替法定检验、消防验收或第三方检测报告',
  '读取 .xlsx / .pdf / 照片原件，联网核验供应商资质证书、报警器年检报告与软管合格证的真伪',
  '给出整改工程做法与报价、代替安全管理员签字确认或代替向燃气公司报备',
];

// —— 样例：一张**干净**的燃气设施巡检与隐患整改记录表（核对月 2025-06：5 个点位、12 条明细 + 1 行合计）——
// 每个点位本月都有检查记录、软管未到期、报警器年检按周期复算与「下次年检日期」一致且未超期、
// 检查项数与规定项数一致、无隐患、供应商资质与供气合同都覆盖核对日期、合计行逐列复算相符。
const SAMPLE_HEADER = [
  '点位编号', '点位名称', '门店', '点位类型', '检查日期',
  '检查项数', '规定检查项数', '检查项目', '点位数', '检查结果',
  '隐患描述', '隐患数', '整改期限(天)', '整改完成日期', '软管更换到期日',
  '上次年检日期', '年检周期(月)', '下次年检日期', '供应商资质到期日', '供气合同到期日', '核对日期',
];

// 各点位类型的**应检项清单**（燃气巡检固定项目；订阅版用它点名「缺哪项」）
const KITCHEN_ITEMS = '管道;阀门;软管;报警器;切断阀;通风';
const DEVICE_ITEMS = '管道;阀门;软管;报警器;切断阀';
const BOILER_ITEMS = '管道;阀门;软管;报警器;切断阀;通风;烟道;安全阀';

/** 一行正常明细（检查结果=正常，隐患描述 / 整改期限 / 整改完成日期都空着） */
function sampleRow(no, name, store, type, day, items, ic, rc, hose, last, cycle, next, qual, contract, audit) {
  return [no, name, store, type, day, ic, rc, items, 1, '正常', '', 0, '', '', hose, last, cycle, next, qual, contract, audit].join('\t');
}

const SAMPLE_TEXT = [
  SAMPLE_HEADER.join('\t'),
  sampleRow('P-001', '锦绣路店后厨灶台', '锦绣路店', '厨房', '2025-05-12', KITCHEN_ITEMS, 6, 6, '2026-03-31', '2024-11-20', 12, '2025-11-20', '2026-05-31', '2026-02-28', '2025-06-30'),
  sampleRow('P-001', '锦绣路店后厨灶台', '锦绣路店', '厨房', '2025-06-10', KITCHEN_ITEMS, 6, 6, '2026-03-31', '2024-11-20', 12, '2025-11-20', '2026-05-31', '2026-02-28', '2025-06-30'),
  sampleRow('P-001', '锦绣路店后厨灶台', '锦绣路店', '厨房', '2025-06-24', KITCHEN_ITEMS, 6, 6, '2026-03-31', '2024-11-20', 12, '2025-11-20', '2026-05-31', '2026-02-28', '2025-06-30'),
  sampleRow('P-002', '锦绣路店燃气蒸箱', '锦绣路店', '用气设备', '2025-05-12', DEVICE_ITEMS, 5, 5, '2026-01-08', '2025-01-08', 12, '2026-01-08', '2026-05-31', '2026-02-28', '2025-06-30'),
  sampleRow('P-002', '锦绣路店燃气蒸箱', '锦绣路店', '用气设备', '2025-06-10', DEVICE_ITEMS, 5, 5, '2026-01-08', '2025-01-08', 12, '2026-01-08', '2026-05-31', '2026-02-28', '2025-06-30'),
  sampleRow('P-002', '锦绣路店燃气蒸箱', '锦绣路店', '用气设备', '2025-06-24', DEVICE_ITEMS, 5, 5, '2026-01-08', '2025-01-08', 12, '2026-01-08', '2026-05-31', '2026-02-28', '2025-06-30'),
  sampleRow('P-003', '云谷工业园食堂管道阀门', '云谷工业园食堂', '厨房', '2025-06-05', KITCHEN_ITEMS, 6, 6, '2026-06-30', '2025-02-18', 12, '2026-02-18', '2026-08-31', '2026-03-31', '2025-06-30'),
  sampleRow('P-003', '云谷工业园食堂管道阀门', '云谷工业园食堂', '厨房', '2025-06-19', KITCHEN_ITEMS, 6, 6, '2026-06-30', '2025-02-18', 12, '2026-02-18', '2026-08-31', '2026-03-31', '2025-06-30'),
  sampleRow('P-004', '云谷工业园食堂燃气锅炉', '云谷工业园食堂', '用气设备', '2025-06-05', DEVICE_ITEMS, 5, 5, '2025-12-31', '2024-12-05', 12, '2025-12-05', '2026-08-31', '2026-03-31', '2025-06-30'),
  sampleRow('P-004', '云谷工业园食堂燃气锅炉', '云谷工业园食堂', '用气设备', '2025-06-19', DEVICE_ITEMS, 5, 5, '2025-12-31', '2024-12-05', 12, '2025-12-05', '2026-08-31', '2026-03-31', '2025-06-30'),
  sampleRow('P-005', '城南物业锅炉房调压柜', '城南物业', '锅炉房', '2025-06-08', BOILER_ITEMS, 8, 8, '2026-09-30', '2025-03-15', 12, '2026-03-15', '2026-10-31', '2026-04-30', '2025-06-30'),
  sampleRow('P-005', '城南物业锅炉房调压柜', '城南物业', '锅炉房', '2025-06-22', BOILER_ITEMS, 8, 8, '2026-09-30', '2025-03-15', 12, '2026-03-15', '2026-10-31', '2026-04-30', '2025-06-30'),
  ['合计', '', '', '', '', 71, 71, '', 5, '', '', 0, '', '', '', '', '', '', '', '', '2025-06-30'].join('\t'),
].join('\n');

const TOL = 0.01;

// 检查结果只允许这四个取值（别的一律点名）
const STATUS_VALUES = ['正常', '隐患', '停用', '已整改'];

// 合计行 / 小计行：点位编号或点位名称里带这些字
const TOTAL_RE = /合计|总计|小计/;

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词会把更具体的列抢走（本仓库踩过多次，见 tools/header_map_check.py）。
//    「检查日期 / 上次年检日期 / 下次年检日期 / 软管更换到期日 / 供应商资质到期日 / 核对日期」
//    就是靠这套顺序 +「不写裸词」的写法错开的：
//    · 规定检查项数 排在 检查项数 之前（否则「规定检查项数」被「检查项数」抢走）；
//    · 下次年检日期 排在 上次年检日期 之前（否则「下次年检日期」被「年检日期」抢走）；
//    · 隐患数 排在 隐患描述 之前，且这两条都不含会让对方命中的裸词。
const ROLES = {
  pointType: ['点位类型', '设备类型', '场所类型', '用气设备类型', '类型'],
  requiredItemCount: ['规定检查项数', '应检项数', '规定项数', '标准项数'],
  itemCount: ['检查项数', '检查项目数', '实检项数', '项数'],
  checkItems: ['检查项目', '已检项目', '巡检项目', '检查项'],
  pointNo: ['点位编号', '点位代码', '点位编码', '设备编号', '编号'],
  pointName: ['点位名称', '设备名称', '点位名', '名称'],
  store: ['门店名称', '门店', '使用单位', '场所名称', '场所'],
  checkDate: ['检查日期', '巡检日期', '检查时间', '检查日'],
  result: ['检查结果', '检查结论', '巡检结果', '结论', '状态'],
  hazardCount: ['隐患数', '隐患数量', '隐患条数'],
  hazardDesc: ['隐患描述', '隐患情况', '问题描述', '隐患', '描述'],
  pointCount: ['点位数', '点位数量', '点位总数'],
  fixDays: ['整改期限', '整改天数', '整改时限', '期限'],
  fixDoneDate: ['整改完成日期', '整改完成时间', '完成日期', '整改日期'],
  hoseDueDate: ['软管更换到期日', '软管到期日', '软管更换日期', '软管'],
  nextAlarmDate: ['下次年检日期', '下次年检时间', '下次年检'],
  lastAlarmDate: ['上次年检日期', '上次年检时间', '上次年检', '年检日期', '上次检验日期'],
  alarmCycle: ['年检周期', '检验周期', '周期'],
  supplierQualExpiry: ['供应商资质到期日', '资质到期日', '资质有效期', '资质'],
  supplierContractExpiry: ['供气合同到期日', '合同到期日', '供气合同有效期', '合同到期'],
  auditDate: ['核对日期', '核对时间', '核对日'],
  note: ['备注', '说明'],
};

const LABELS = {
  pointNo: '点位编号',
  pointName: '点位名称',
  store: '门店',
  pointType: '点位类型',
  checkDate: '检查日期',
  itemCount: '检查项数',
  requiredItemCount: '规定检查项数',
  checkItems: '检查项目',
  pointCount: '点位数',
  result: '检查结果',
  hazardDesc: '隐患描述',
  hazardCount: '隐患数',
  fixDays: '整改期限(天)',
  fixDoneDate: '整改完成日期',
  hoseDueDate: '软管更换到期日',
  lastAlarmDate: '上次年检日期',
  alarmCycle: '年检周期(月)',
  nextAlarmDate: '下次年检日期',
  supplierQualExpiry: '供应商资质到期日',
  supplierContractExpiry: '供气合同到期日',
  auditDate: '核对日期',
  note: '备注',
};

// 表头级必需列（缺列 ⇒ 材料不足，**绝不给结论**）
const REQUIRED_ROLES = [
  'pointNo', 'pointName', 'pointType', 'checkDate', 'itemCount', 'requiredItemCount', 'result',
  'hazardDesc', 'fixDays', 'fixDoneDate', 'hoseDueDate', 'lastAlarmDate', 'alarmCycle',
  'nextAlarmDate', 'auditDate',
];

// 单元格级必需字段（空白 / 占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['pointNo', '点位编号'],
  ['pointName', '点位名称'],
  ['pointType', '点位类型'],
  ['checkDate', '检查日期'],
  ['itemCount', '检查项数'],
  ['requiredItemCount', '规定检查项数'],
  ['result', '检查结果'],
  ['hoseDueDate', '软管更换到期日'],
  ['lastAlarmDate', '上次年检日期'],
  ['alarmCycle', '年检周期(月)'],
  ['nextAlarmDate', '下次年检日期'],
  ['auditDate', '核对日期'],
];

// 数值列（为负 / 无法解析 ⇒ 点名；空白交给「关键字段缺失」或按需跳过）
const NUM_FIELDS = [
  ['itemCount', '检查项数'],
  ['requiredItemCount', '规定检查项数'],
  ['pointCount', '点位数'],
  ['hazardCount', '隐患数'],
  ['fixDays', '整改期限(天)'],
  ['alarmCycle', '年检周期(月)'],
];

// 日期列（第三个值 = 是否每个明细行都必须填）
const DATE_FIELDS = [
  ['checkDate', '检查日期', true],
  ['fixDoneDate', '整改完成日期', false],
  ['hoseDueDate', '软管更换到期日', true],
  ['lastAlarmDate', '上次年检日期', true],
  ['nextAlarmDate', '下次年检日期', true],
  ['auditDate', '核对日期', true],
];

// 数量类列：点位数按**去重计数**，其余按明细行求和
const SUM_ROLES = ['itemCount', 'requiredItemCount', 'hazardCount'];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张表补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「检查已覆盖」，也不说「有隐患」，'
      + '更不会输出「未发现问题」。',
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
    || /^(n\/?a|无|不适用|待填|待补|待定|待核|未检|未查)$/i.test(s);
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

function str(v) {
  return v === undefined || v === null ? '' : String(v).trim();
}

function isTotalRow(it) {
  return TOTAL_RE.test(str(it.pointNo) + str(it.pointName));
}

function totalKind(it) {
  const s = str(it.pointNo) + str(it.pointName);
  if (/小计/.test(s) && !/合计|总计/.test(s)) return 'subtotal';
  return 'total';
}

function detailRows(items) {
  return items.filter((it) => !isTotalRow(it));
}

function pointKey(it) {
  return str(it.pointNo) || str(it.pointName);
}

function pointLabel(it) {
  return str(it.pointName) || str(it.pointNo) || '未命名点位';
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
  // ⚠️ 合计/小计行**不计入** totals（否则会把合计行自身的数字再加一遍）
  const details = items.filter((it) => !isTotalRow(it));
  const totals = {};
  for (const role of SUM_ROLES) {
    totals[role] = round2(details.reduce((acc, it) => {
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

function who(it) {
  return `第 ${it.line} 行「${pointLabel(it)}」`;
}

function docList(v) {
  return String(v == null ? '' : v).split(/[;；,，、/|]+/).map((s) => s.trim()).filter((s) => s !== '');
}

function finding(level, category, it, diff, message, advice) {
  const f = { level, category, line: it.line, message };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

function sumRole(items, role) {
  return round2(items.reduce((acc, it) => acc + num(it, role), 0));
}

/* ---- 日期：一律换算成「自 1970-01-01 起的天数」做整数比较，不依赖本机时钟 ---- */

function makeDay(y, m, d) {
  if (!(y >= 1900 && y <= 2999) || !(m >= 1 && m <= 12) || !(d >= 1 && d <= 31)) return null;
  const dt = new Date(Date.UTC(y, m - 1, d));
  if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== m - 1 || dt.getUTCDate() !== d) return null;
  return Math.round(dt.getTime() / 86400000);
}

/** 只认 2025-06-30 / 2025/6/30 / 2025.6.30 / 2025年6月30日 这类形态；别的一律 null */
function normDate(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/^["']|["']$/g, '');
  if (!s) return null;
  const m = /^(\d{4})[-/.年](\d{1,2})[-/.月](\d{1,2})日?$/.exec(s);
  if (!m) return null;
  return makeDay(Number(m[1]), Number(m[2]), Number(m[3]));
}

function fmtDay(n) {
  if (n === null || n === undefined) return '(未填)';
  const d = new Date(n * 86400000);
  const mm = String(d.getUTCMonth() + 1).padStart(2, '0');
  const dd = String(d.getUTCDate()).padStart(2, '0');
  return `${d.getUTCFullYear()}-${mm}-${dd}`;
}

/** 加 N 个月（按自然月对齐，月末不足时取该月最后一天）—— 报警器年检到期日就靠它复算 */
function addMonths(dayNum, months) {
  const d = new Date(dayNum * 86400000);
  const y = d.getUTCFullYear();
  const m = d.getUTCMonth();
  const dom = d.getUTCDate();
  const t = new Date(Date.UTC(y, m + months, 1));
  const ty = t.getUTCFullYear();
  const tm = t.getUTCMonth();
  const lastDom = new Date(Date.UTC(ty, tm + 1, 0)).getUTCDate();
  return makeDay(ty, tm + 1, Math.min(dom, lastDom));
}

function monthOf(dayNum) {
  return fmtDay(dayNum).slice(0, 7);
}

function monthLabel(monthKey) {
  return monthKey ? `${monthKey}（${Number(monthKey.slice(5, 7))} 月）` : '(核对日期未填)';
}

/** 核对日期：取明细行里第一条能解析出来的「核对日期」；一条都解析不出来就返回 null（交给「日期无法解析」那项） */
function refDayOf(details) {
  for (const it of details) {
    const d = normDate(it.auditDate);
    if (d !== null) return d;
  }
  return null;
}

/* ============================ 本包检查（六项） ============================ */

/** 1. 检查频次覆盖：核对日期所在月里，每个点位至少要有 1 条检查记录 */
function checkMonthlyCoverage(items) {
  const out = [];
  const details = detailRows(items);
  const refDay = refDayOf(details);
  if (refDay === null) return out;              // 核对日期都填不出来 ⇒ 交给「日期无法解析」，不在这里猜
  const monthKey = monthOf(refDay);
  const byPoint = new Map();
  for (const it of details) {
    const k = pointKey(it);
    if (!k) continue;
    if (!byPoint.has(k)) byPoint.set(k, { key: k, lines: [], month: [], latest: null });
    const g = byPoint.get(k);
    g.lines.push(it);
    const cd = normDate(it.checkDate);
    if (cd === null) continue;
    if (monthOf(cd) === monthKey) g.month.push(it);
    if (cd <= refDay && (g.latest === null || cd > g.latest.day)) g.latest = { day: cd, result: str(it.result) };
  }
  for (const [, g] of byPoint) {
    if (g.month.length) continue;
    if (g.latest && g.latest.result === '停用') continue;   // 停用点位不要求月检
    const anchor = g.lines[0];
    out.push(finding('P1', '本月未按频次检查', anchor, undefined,
      `${who(anchor)}：点位「${pointLabel(anchor)}」在核对日期 ${fmtDay(refDay)} 所在的 ${monthLabel(monthKey)} 里`
      + '一条检查记录都没有 —— 燃气设施每月至少检查 1 次，这个点位本月缺检。',
      '补一次现场检查（管道、阀门、软管、报警器、切断阀、通风）并把记录补进表里；'
      + '确实停用的点位请把「检查结果」写成「停用」，本工具对最新一条为停用的点位不报缺检。'));
  }
  return out;
}

/** 2. 软管/管件有效期：检查日期 ≤ 软管更换到期日 */
function checkHoseValidity(items) {
  const out = [];
  for (const it of detailRows(items)) {
    const cd = normDate(it.checkDate);
    const hd = normDate(it.hoseDueDate);
    if (cd === null || hd === null) continue;
    if (cd <= hd) continue;
    const diff = cd - hd;
    out.push(finding('P0', '软管超期仍在检查使用', it, diff,
      `${who(it)}：检查日期 ${fmtDay(cd)} 晚于「软管更换到期日」${fmtDay(hd)}，这次检查时软管已经超期 ${diff} 天。`,
      '先换管（或停用该点位）再检查；超期软管是燃气公司与监管的查封项，记录里出现超期检查本身就是证据。'));
  }
  return out;
}

/** 3. 燃气报警器年检：上次年检日期 + 年检周期(月) = 下次年检日期，并与核对日期比出超期天数 */
function checkAlarmYearly(items) {
  const out = [];
  const details = detailRows(items);
  const refDay = refDayOf(details);
  for (const it of details) {
    const last = normDate(it.lastAlarmDate);
    const cyc = normNumber(it.alarmCycle);
    if (last === null || cyc === null || cyc <= 0) continue;
    const months = Math.round(cyc);
    const expect = addMonths(last, months);
    const declared = normDate(it.nextAlarmDate);
    if (declared !== null && declared !== expect) {
      const diff = declared - expect;
      out.push(finding('P1', '下次年检日期与周期不符', it, diff,
        `${who(it)}：「上次年检日期」${fmtDay(last)} + 年检周期 ${months} 个月 = ${fmtDay(expect)}，`
        + `但表里「下次年检日期」填的是 ${fmtDay(declared)}，差 ${Math.abs(diff)} 天。`,
        '两边对齐：要么改「年检周期(月)」，要么改「下次年检日期」；年检到期日算错，报警器年检就会漏做。'));
    }
    if (refDay !== null && refDay > expect) {
      const diff = refDay - expect;
      out.push(finding('P0', '燃气报警器年检超期', it, diff,
        `${who(it)}：按「上次年检日期」${fmtDay(last)} + 年检周期 ${months} 个月复算，年检到期日是 ${fmtDay(expect)}，`
        + `核对日期 ${fmtDay(refDay)} 已经超期 ${diff} 天。`,
        '立刻约年检并留报告；报警器失效期间不报警、不联动切断阀，是燃气公司与监管的查封项。'
        + '超期天数按**复算值**算，不认表里填的「下次年检日期」。'));
    }
  }
  return out;
}

/** 4. 同一点位同一检查日期重复登记 */
function checkDuplicateChecks(items) {
  const out = [];
  const seen = new Map();
  for (const it of detailRows(items)) {
    const k = pointKey(it);
    const cd = normDate(it.checkDate);
    if (!k || cd === null) continue;
    const key = `${k}|${cd}`;
    if (!seen.has(key)) { seen.set(key, { lines: [it.line] }); continue; }
    const g = seen.get(key);
    g.lines.push(it.line);
    out.push(finding('P1', '同一点位同一检查日期重复登记', it, undefined,
      `${who(it)}：点位「${pointLabel(it)}」在 ${fmtDay(cd)} 有 ${g.lines.length} 条检查记录`
      + `（第 ${g.lines.join('、')} 行）—— 同一天同一点位重复登记。`,
      '同一天同一点位只应留一条巡检记录；分次巡检请把检查日期分开写，重复行会让「检查频次」虚高。'));
  }
  return out;
}

/** 5. 合计行逐列复核：点位数按去重计数，检查项数/规定检查项数/隐患数按明细行求和 */
function checkTotalRows(items) {
  const out = [];
  const details = detailRows(items);
  for (const it of items) {
    if (!isTotalRow(it)) continue;
    const kind = totalKind(it);
    let scope = details;
    const scopeLabel = [];
    if (kind === 'subtotal') {
      const st = str(it.store);
      const tp = str(it.pointType);
      if (st) { scope = details.filter((d) => str(d.store) === st); scopeLabel.push(`门店 ${st}`); }
      else if (tp) { scope = details.filter((d) => str(d.pointType) === tp); scopeLabel.push(`点位类型 ${tp}`); }
    }
    const truth = {
      pointCount: new Set(scope.map((d) => pointKey(d)).filter((k) => k)).size,
      itemCount: sumRole(scope, 'itemCount'),
      requiredItemCount: sumRole(scope, 'requiredItemCount'),
      hazardCount: scope.filter((d) => str(d.result) === '隐患').length,
    };
    for (const role of ['pointCount', 'itemCount', 'requiredItemCount', 'hazardCount']) {
      const raw = it[role];
      if (isBlank(raw)) continue;                 // 空着的合计单元格不在这里猜
      const declared = normNumber(raw);
      if (declared === null) continue;            // 交给「数值为负或无法解析」
      const diff = round2(declared - truth[role]);
      if (Math.abs(diff) < TOL) continue;
      out.push(finding('P1', '合计行复算不符', it, diff,
        `${who(it)}：「${LABELS[role]}」这一列填的是 ${declared}，按${scopeLabel.length ? scopeLabel.join('、') + '的' : '全部'}明细行复算应为 `
        + `${truth[role]}，差 ${diff > 0 ? '+' : ''}${diff}。`
        + (role === 'pointCount' ? '「点位数」是**去重计数**（同一点位本月查了两次仍只算 1 个点位），不是明细行数。' : ''),
        '把合计行改成复算值，或把漏填/多填的明细行补齐 —— 合计行与明细对不上，这张巡检台账就不可信。'));
    }
  }
  return out;
}

/** 6. 关键字段缺失与取值非法（空白/占位符、日期格式、数值为负或无法解析、检查结果取值） */
function checkFieldIntegrity(items) {
  const out = [];
  for (const it of detailRows(items)) {
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        `${who(it)}：这些关键字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的字段会让对应的核对整项做不了；补全后重跑，本工具不会替你猜一个默认值。'));
    }

    const numBad = [];
    for (const [role, label] of NUM_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) { numBad.push(`「${label}」的值「${str(raw)}」不是可识别的数值`); continue; }
      if (n < 0) numBad.push(`「${label}」是负数（${n}）`);
    }
    if (numBad.length) {
      out.push(finding('P1', '数值为负或无法解析', it, undefined,
        `${who(it)}：${numBad.join('；')}。`,
        '项数与天数只能是不小于 0 的数值（只认数字、千分位、英文括号负数）；看不懂的值本工具不会当成 0。'));
    }

    const dateBad = [];
    for (const [role, label, required] of DATE_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) {
        if (required && miss.indexOf(label) < 0) dateBad.push(`「${label}」是空的`);
        continue;
      }
      if (normDate(raw) === null) dateBad.push(`「${label}」的值「${str(raw)}」不是可识别的日期`);
    }
    if (dateBad.length) {
      out.push(finding('P1', '日期无法解析', it, undefined,
        `${who(it)}：${dateBad.join('；')}。`,
        '日期请写成 2025-06-30 或 2025/6/30 这种形态；日期写不清楚，软管超期与报警器年检超期就都算不出来。'));
    }

    const rv = str(it.result);
    if (rv && STATUS_VALUES.indexOf(rv) < 0) {
      out.push(finding('P1', '检查结果取值非法', it, undefined,
        `${who(it)}：「检查结果」填的是「${rv}」，不在允许的取值里（只能是 ${STATUS_VALUES.join(' / ')}）。`,
        '按 正常 / 隐患 / 停用 / 已整改 四选一填写；「已通知」「整改中」「已报修」这类写法会让整改闭环与停用判定都失效。'));
    }
  }
  return out;
}

/* ===== 以下函数只在订阅版执行（形态 B：由入口里那一个开关控制；免费包会把它们整块摘掉） ===== */

/** 付费①：隐患整改闭环 —— 检查结果=隐患 但缺整改完成日期 或 晚于整改期限日 */
function checkHazardClosure(items) {
  const out = [];
  const details = detailRows(items);
  const refDay = refDayOf(details);
  for (const it of details) {
    if (str(it.result) !== '隐患') continue;
    const cd = normDate(it.checkDate);
    const days = normNumber(it.fixDays);
    const done = normDate(it.fixDoneDate);
    if (cd === null || days === null || days < 0) {
      out.push(finding('P1', '隐患未整改闭环', it, undefined,
        `${who(it)}：检查结果=隐患（${str(it.hazardDesc) || '未填隐患描述'}），但「检查日期」或「整改期限(天)」填不出来 —— 复算不了超期天数。`,
        '补上检查日期与整改期限（天）再跑；本工具不会把缺的期限猜成 0，也不会替你判定「应该算没超期」。'));
      continue;
    }
    const deadline = cd + Math.round(days);
    let overdue = 0;
    let reason = '';
    if (done === null) {
      reason = '缺「整改完成日期」，隐患还没闭环';
      if (refDay !== null && refDay > deadline) overdue = refDay - deadline;
    } else if (done > deadline) {
      overdue = done - deadline;
      reason = `整改完成日期 ${fmtDay(done)} 晚于整改期限日 ${fmtDay(deadline)}`;
    } else {
      continue;                                  // 已按期闭环
    }
    out.push(finding(overdue > 0 ? 'P0' : 'P1', '隐患未整改闭环', it, overdue > 0 ? overdue : undefined,
      `${who(it)}：${reason}（检查日期 ${fmtDay(cd)} + 整改期限 ${Math.round(days)} 天 = 期限日 ${fmtDay(deadline)}`
      + (overdue > 0 ? `，超期 ${overdue} 天）` : '）') + '。',
      '能当场整改的立刻整改并填「整改完成日期」、结果改成「已整改」；要停用的先停用并书面报燃气公司。'
      + '隐患未整改是燃气公司与监管的查封项，别只写「已通知」。'));
  }
  return out;
}

/** 该点位类型的**应检项清单**（订阅版用它点名缺哪项） */
function standardItems(type) {
  const STD = {
    '厨房': ['管道', '阀门', '软管', '报警器', '切断阀', '通风'],
    '锅炉房': ['管道', '阀门', '软管', '报警器', '切断阀', '通风', '烟道', '安全阀'],
    '用气设备': ['管道', '阀门', '软管', '报警器', '切断阀'],
  };
  return STD[str(type)] || ['管道', '阀门', '软管', '报警器', '切断阀', '通风'];
}

/** 付费②：检查项目不齐（检查项数 < 规定检查项数） */
function checkItemGap(items) {
  const out = [];
  for (const it of detailRows(items)) {
    const ic = normNumber(it.itemCount);
    const rc = normNumber(it.requiredItemCount);
    if (ic === null || rc === null) continue;
    if (ic >= rc) continue;
    const listed = docList(it.checkItems);
    const std = standardItems(it.pointType);
    const missing = std.filter((x) => !listed.some((h) => h.indexOf(x) >= 0));
    const diff = round2(rc - ic);
    out.push(finding('P1', '检查项目不齐', it, diff,
      `${who(it)}：检查项数 ${ic} < 规定检查项数 ${rc}（${str(it.pointType) || '点位类型未填'}应检 ${std.join('、')}），差 ${diff} 项。`
      + (listed.length ? `「检查项目」列写的是：${listed.join('、')}；` : '「检查项目」列没填，点不了名；')
      + (listed.length && missing.length ? `按台账**没有点到**的项：${missing.join('、')}。` : '')
      + (listed.length && !missing.length ? '它列的项本身就不齐（数量与应检清单对不上）。' : ''),
      '按该点位类型的应检项清单逐项补检，并在「检查项目」里逐项写出来；漏检的往往正是软管、报警器、切断阀'
      + '这些燃气公司与监管的查封项。'));
  }
  return out;
}

/** 付费③：软管/管件超期仍在用（到期日早于核对日期，且该点位最新一条检查结果不是停用） */
function checkHoseOverdueInUse(items) {
  const out = [];
  const details = detailRows(items);
  const refDay = refDayOf(details);
  if (refDay === null) return out;
  const byPoint = new Map();
  for (const it of details) {
    const k = pointKey(it);
    if (!k) continue;
    const cd = normDate(it.checkDate);
    if (cd === null || cd > refDay) continue;
    const g = byPoint.get(k);
    if (!g || cd > g.day) byPoint.set(k, { day: cd, it: it });
  }
  for (const [, g] of byPoint) {
    const it = g.it;
    if (str(it.result) === '停用') continue;
    const hd = normDate(it.hoseDueDate);
    if (hd === null || hd >= refDay) continue;
    const diff = refDay - hd;
    out.push(finding('P0', '软管超期仍在使用', it, diff,
      `${who(it)}：软管更换到期日 ${fmtDay(hd)} 已经早于核对日期 ${fmtDay(refDay)}，超期 ${diff} 天；`
      + `而该点位最新一次检查（${fmtDay(g.day)}）的检查结果是「${str(it.result) || '未填'}」，不是「停用」—— 超期软管还在用。`,
      '先停用该点位或换管，再复检并留新管的合格证；超期软管是燃气公司与监管的查封项，别只写「下次换」。'));
  }
  return out;
}

/** 付费④：燃气供应商资质与供气合同有效期覆盖（按门店核对是否覆盖核对日期） */
function checkSupplierValidity(items) {
  const out = [];
  const details = detailRows(items);
  const refDay = refDayOf(details);
  if (refDay === null) return out;
  const byStore = new Map();
  for (const it of details) {
    const k = str(it.store) || pointKey(it);
    if (!k) continue;
    const cd = normDate(it.checkDate);
    const g = byStore.get(k);
    if (!g) { byStore.set(k, { key: k, day: cd === null ? -1 : cd, it: it }); continue; }
    if (cd !== null && cd > g.day) { g.day = cd; g.it = it; }
  }
  const checks = [
    ['supplierQualExpiry', '供应商资质到期日', '燃气供应商资质'],
    ['supplierContractExpiry', '供气合同到期日', '供气合同'],
  ];
  for (const [, g] of byStore) {
    for (const pair of checks) {
      const role = pair[0];
      const label = pair[1];
      const what = pair[2];
      const raw = g.it[role];
      if (isBlank(raw)) {
        out.push(finding('P1', '供应商资质与合同未覆盖', g.it, undefined,
          `${who(g.it)}：门店「${g.key}」没有登记「${label}」—— 核对日期 ${fmtDay(refDay)} 是否被${what}覆盖，核不了。`,
          `把${what}的到期日填进「${label}」列；空着不等于有效，本工具不会替你当作已覆盖。`));
        continue;
      }
      const d = normDate(raw);
      if (d === null || d >= refDay) continue;
      const diff = refDay - d;
      out.push(finding('P0', '供应商资质与合同未覆盖', g.it, diff,
        `${who(g.it)}：门店「${g.key}」的「${label}」是 ${fmtDay(d)}（原文：${str(raw)}），`
        + `早于核对日期 ${fmtDay(refDay)}，已经过期 ${diff} 天 —— 用气期间${what}没有覆盖。`,
        `向供气方索取有效的${what}并归档后再续用；资质/合同过期期间用气，一旦出事责任在企业。`));
    }
  }
  return out;
}

/** 逐行超期计数（订阅版汇总排序用）：超期软管 + 报警器年检超期 + 隐患超期未闭环 */
function overdueFlags(it, refDay) {
  const out = { hose: 0, alarm: 0, closure: 0 };
  const cd = normDate(it.checkDate);
  const hd = normDate(it.hoseDueDate);
  if (cd !== null && hd !== null && cd > hd) out.hose = 1;
  const last = normDate(it.lastAlarmDate);
  const cyc = normNumber(it.alarmCycle);
  if (last !== null && cyc !== null && cyc > 0 && refDay !== null && refDay > addMonths(last, Math.round(cyc))) out.alarm = 1;
  if (str(it.result) === '隐患') {
    const days = normNumber(it.fixDays);
    const done = normDate(it.fixDoneDate);
    if (cd !== null && days !== null && days >= 0) {
      const deadline = cd + Math.round(days);
      if (done === null) { if (refDay !== null && refDay > deadline) out.closure = 1; }
      else if (done > deadline) out.closure = 1;
    } else {
      out.closure = 1;
    }
  }
  return out;
}

/** 付费①的降序清单：按超期天数从大到小（findings 本身保持行号序，便于对照原文） */
function buildClosureRank(findings) {
  return findings
    .filter((f) => f.category === '隐患未整改闭环')
    .slice()
    .sort((a, b) => ((b.diff || 0) - (a.diff || 0)) || (a.line - b.line))
    .map((f, i) => ({ seq: i + 1, line: f.line, days: f.diff || 0, level: f.level, message: f.message }));
}

/** 付费⑤：分门店 / 分点位类型 / 分门店×点位类型 的汇总清单（按隐患数与超期数排序） */
function buildStoreRollup(items, refDay) {
  const details = detailRows(items);
  const mk = () => ({ rows: 0, points: new Set(), item_count: 0, required_item_count: 0, hazards: 0, overdue: 0 });
  const add = (b, it) => {
    b.rows += 1;
    const k = pointKey(it);
    if (k) b.points.add(k);
    b.item_count = round2(b.item_count + num(it, 'itemCount'));
    b.required_item_count = round2(b.required_item_count + num(it, 'requiredItemCount'));
    if (str(it.result) === '隐患') b.hazards += 1;
    const fl = overdueFlags(it, refDay);
    b.overdue += fl.hose + fl.alarm + fl.closure;
    return b;
  };
  const byStore = new Map();
  const byType = new Map();
  const byStoreType = new Map();
  for (const it of details) {
    const s = str(it.store) || '(未填门店)';
    const tp = str(it.pointType) || '(未填类型)';
    const key = `${s}|${tp}`;
    if (!byStore.has(s)) byStore.set(s, mk());
    if (!byType.has(tp)) byType.set(tp, mk());
    if (!byStoreType.has(key)) byStoreType.set(key, mk());
    add(byStore.get(s), it);
    add(byType.get(tp), it);
    add(byStoreType.get(key), it);
  }
  const toRows = (map, keys) => [...map.entries()].map(([k, v]) => {
    const parts = String(k).split('|');
    const row = {
      points: v.points.size,
      rows: v.rows,
      item_count: v.item_count,
      required_item_count: v.required_item_count,
      hazards: v.hazards,
      overdue: v.overdue,
    };
    keys.forEach((name, i) => { row[name] = parts[i]; });
    return row;
  }).sort((a, b) => (b.hazards - a.hazards) || (b.overdue - a.overdue)
    || String(keys.map((n) => a[n]).join('|')).localeCompare(String(keys.map((n) => b[n]).join('|'))));
  const total = details.reduce((acc, it) => add(acc, it), mk());
  return {
    by_store: toRows(byStore, ['store']),
    by_point_type: toRows(byType, ['point_type']),
    by_store_type: toRows(byStoreType, ['store', 'point_type']),
    total: {
      points: total.points.size,
      rows: total.rows,
      item_count: total.item_count,
      required_item_count: total.required_item_count,
      hazards: total.hazards,
      overdue: total.overdue,
    },
  };
}

/** 付费⑤：合并整改动作（按 隐患数 → 超期数 排序，给出可整改动作） */
function buildConsolidatedActions(rollup) {
  const out = [];
  for (const row of (rollup && rollup.by_store_type) || []) {
    if (!row.hazards && !row.overdue) continue;
    const parts = [];
    if (row.hazards) parts.push(`先闭环 ${row.hazards} 条隐患（填「整改完成日期」/ 按整改期限整改后改成「已整改」）`);
    if (row.overdue) parts.push(`再处理 ${row.overdue} 处超期（超期软管换管、报警器补年检、超期隐患收口）`);
    out.push({
      level: row.hazards ? 'P0' : 'P1',
      store: row.store,
      point_type: row.point_type,
      points: row.points,
      rows: row.rows,
      hazards: row.hazards,
      overdue: row.overdue,
      action: `${parts.join('；')}（涉及 ${row.points} 个点位 / ${row.rows} 条检查记录）`,
    });
  }
  out.sort((a, b) => (b.hazards - a.hazards) || (b.overdue - a.overdue)
    || str(a.store).localeCompare(str(b.store)) || str(a.point_type).localeCompare(str(b.point_type)));
  out.forEach((x, i) => { x.seq = i + 1; });
  return out;
}

/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  const WHAT = '原文（text）：一张含表头的燃气设施安全检查与隐患整改记录表'
    + '（点位编号/点位名称/点位类型/检查日期/检查项数/规定检查项数/检查结果/隐患描述/整改期限(天)/整改完成日期/'
    + '软管更换到期日/上次年检日期/年检周期(月)/下次年检日期/核对日期）';
  if (!String(text).trim()) return insufficient([WHAT]);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient([WHAT]);
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的燃气设施安全检查与隐患整改记录表（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行点位检查明细（现在只有表头，没有可核对的明细行）']);
  }

  const paid = Boolean(p && (p.full || p.credit || p.token));
  const details = detailRows(t.items);
  const refDay = refDayOf(details);
  const findings = [];
  const notRun = [];
  let closureRank = [];
  let storeRollup = null;
  let consolidatedActions = [];
  let overdueCount = 0;

  for (const f of checkMonthlyCoverage(t.items)) findings.push(f);
  for (const f of checkHoseValidity(t.items)) findings.push(f);
  for (const f of checkAlarmYearly(t.items)) findings.push(f);
  for (const f of checkDuplicateChecks(t.items)) findings.push(f);
  for (const f of checkTotalRows(t.items)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

  if (paid) {
    for (const f of checkHazardClosure(t.items)) findings.push(f);
    for (const f of checkItemGap(t.items)) findings.push(f);
    for (const f of checkHoseOverdueInUse(t.items)) findings.push(f);
    for (const f of checkSupplierValidity(t.items)) findings.push(f);
    closureRank = buildClosureRank(findings);
    storeRollup = buildStoreRollup(t.items, refDay);
    consolidatedActions = buildConsolidatedActions(storeRollup);
    overdueCount = details.reduce((acc, it) => {
      const fl = overdueFlags(it, refDay);
      return acc + fl.hose + fl.alarm + fl.closure;
    }, 0);
  } else {
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  }

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const hazardCount = details.filter((it) => str(it.result) === '隐患').length;
  const pointCount = new Set(details.map((it) => pointKey(it)).filter((k) => k)).size;

  const summary = {
    rows: t.items.length,
    detail_rows: details.length,
    total_rows: t.items.length - details.length,
    total: findings.length,
    p0: findings.filter((f) => f.level === 'P0').length,
    p1: findings.filter((f) => f.level === 'P1').length,
    p2: findings.filter((f) => f.level === 'P2').length,
    point_count: pointCount,
    item_count_total: t.totals.itemCount,
    required_item_count_total: t.totals.requiredItemCount,
    hazard_count: hazardCount,
    audit_date: refDay === null ? '' : fmtDay(refDay),
    audit_month: refDay === null ? '' : monthOf(refDay),
    basis: '检查频次按月核对（每个点位每月至少 1 次；最新一条为「停用」的点位不算缺检）；'
      + '软管按 检查日期 ≤ 软管更换到期日 复算；报警器年检按 上次年检日期 + 年检周期(月) = 下次年检日期 复算，'
      + '超期天数一律按复算值算；同一 点位编号 + 检查日期 只允许一条记录；'
      + '合计行的点位数按去重计数，检查项数/规定检查项数/隐患数按明细行求和。',
  };

  const result = {
    findings,
    summary,
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张巡检/整改记录表按上面写明的口径算得对、该填的都填了**，'
      + '不代表燃气设施本身安全、隐患已经实质消除，也不代表已经通过燃气公司或监管的检查 —— 那些不在本工具范围内。';
  }

  const scope = {
    checks: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.items.length,
    detail_rows: details.length,
    total_rows: t.items.length - details.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    point_count: pointCount,
    item_count_total: t.totals.itemCount,
    required_item_count_total: t.totals.requiredItemCount,
    hazard_count: hazardCount,
    audit_date: refDay === null ? '' : fmtDay(refDay),
    audit_month: refDay === null ? '' : monthOf(refDay),
    missing_fields: details.length
      ? REQUIRED_FIELDS.filter(([role]) => details.some((it) => isBlank(it[role]))).map(([, label]) => label)
      : [],
  };
  result.scope = scope;

  if (paid) {
    summary.overdue_count = overdueCount;
    scope.overdue_count = overdueCount;
    result.closure_rank = closureRank;
    result.store_rollup = storeRollup;
    result.consolidated_actions = consolidatedActions;
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
  CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
  normDate, fmtDay, addMonths,
};
