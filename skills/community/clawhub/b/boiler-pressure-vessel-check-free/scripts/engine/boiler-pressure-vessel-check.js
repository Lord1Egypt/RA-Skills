#!/usr/bin/env node
/**
 * boiler-pressure-vessel-check.js —— 锅炉压力容器定期检验与台账核对引擎（**免费档**；确定性、纯 Node 标准库）。
 *
 * 真实痛点：锅炉、压力容器、压力管道都是**特种设备**，设备科/安环部**每月**都得把这本台账核一遍：
 *   定期检验（外部检验 / 内部检验 / 耐压试验）的「下次检验日期」必须覆盖核对基准日；
 *   使用登记证与作业人员证（司炉工 / 水处理工）都必须在有效期内；
 *   安全阀 / 压力表的「校验日期 + 校验周期」要能复算出下次校验日期；
 *   超期未检仍在用是**监管直接查封/处罚项**，出事故企业负责人要担刑责。
 *
 * ⚠️ 本文件是**免费档子集**：只实现下面这六项**表内逐行算术与台账勾稽**：
 *     ① 检验有效期覆盖；② 使用登记证与作业人员证覆盖；③ 安全阀压力表校验复算与超期；
 *     ④ 同一设备编号重复登记；⑤ 合计行逐列复核（设备台数 / 校验件数）；⑥ 字段合法性与空缺。
 *    **完整档（付费）的实现不在这个包里** —— 超期未检仍在用、停用报废设备仍在运行记录、
 *    运行参数越限、日常巡检记录断档、分设备类别与分使用部门的汇总清单都不在这里。
 *    `CHECKS_WITHHELD` 只是「未执行的检查项」的**说明文本**，不是实现。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定设备该不该检验、不判定检验报告结论本身是否合格、不判定隐患整改是否闭环、
 *          不读 .xlsx / .pdf 原件、不联网核验证件真伪；材料不足**一律不给结论**。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '检验有效期覆盖（核对基准日 ≤ 下次检验日期；超期逐台给出已超期天数）',
  '使用登记证与作业人员证覆盖（两证到期日都要覆盖核对基准日；缺证 / 过期逐台点名）',
  '安全阀压力表校验（校验日期 + 校验周期 = 下次校验日期 逐行复算；再以核对基准日判超期天数）',
  '同一设备编号重复登记（一本台账里设备编号唯一）',
  '合计行逐列复核（数量类列：设备台数、校验件数）',
  '空白占位符与字段合法性（关键字段缺失、日期格式非法、数值为负或周期为零、运行状态非法）',
];

const CHECKS_WITHHELD = [
  '超期未检仍在用（下次检验日期已过且运行状态=在用；按超期天数降序点名）',
  '停用报废设备仍在运行记录（跨表交叉核对：台账状态为停用/报废，却在日常运行与巡检记录里出现）',
  '运行参数越限（运行压力 / 运行温度超过设计上限，逐条报出偏差）',
  '日常巡检记录断档（按设备对运行记录日期序列逐日比对，缺哪一天就点哪一天）',
  '分设备类别与分使用部门的汇总清单（按超期天数与越限次数排序，给出可整改动作）',
];

const OUT_OF_SCOPE = [
  '判定这台设备该不该检验、该做外部检验还是内部检验或耐压试验（那是检验机构与设备类别的法定口径，本工具只核台账日期是否被覆盖）',
  '判定检验报告结论本身是否合格、安全阀整定压力是否合理（那是检验机构的判定权，本工具只核日期与周期算术）',
  '判定隐患整改是否真的闭环、现场是否已经停用或隔离（本工具只核台账与运行记录的字面一致性）',
  '读取 .xlsx / .pdf 原件、联网核验使用登记证 / 作业人员证 / 检验报告的真伪，替代特种设备安全管理员或监管部门的认定',
];

// 样例：一本**干净**的锅炉压力容器检验与核对台账 —— 三台设备（锅炉 ×2、压力容器 ×1），
// 检验有效期覆盖核对基准日、两证都在有效期内、安全阀校验周期复算一致、设备编号不重复、
// 合计行与明细一致、运行与巡检记录逐日连续且参数都没越限。**全表零命中**。
const SAMPLE_TEXT = [
  '设备编号\t设备名称\t设备类别\t使用登记证号\t登记证到期日\t上次检验日期\t检验周期(月)\t下次检验日期\t作业人员\t作业人员证号\t作业人员证到期日\t安全阀校验日期\t校验周期(月)\t下次校验日期\t运行状态\t设备台数\t校验件数\t设计压力上限(MPa)\t设计温度上限(℃)\t使用部门\t核对日期\t备注',
  'GL-2026-001\t1号蒸汽锅炉\t锅炉\t苏锅登字2026-0001\t2029-06-30\t2025-09-15\t12\t2026-09-15\t张建国\t320101********1234\t2028-05-20\t2025-09-15\t12\t2026-09-15\t在用\t1\t2\t1.6\t204\t动力车间\t2026-03-31\t外部检验合格',
  'GL-2026-002\t2号热水锅炉\t锅炉\t苏锅登字2026-0002\t2029-06-30\t2025-11-20\t12\t2026-11-20\t李秀兰\t320102********5678\t2027-11-10\t2025-11-20\t12\t2026-11-20\t在用\t1\t2\t1.25\t170\t供热车间\t2026-03-31\t外部检验合格',
  'YLR-2026-003\t3号空气储罐\t压力容器\t苏容登字2026-0003\t2030-01-31\t2025-10-08\t24\t2027-10-08\t王海涛\t320103********9012\t2029-03-15\t2025-10-08\t24\t2027-10-08\t在用\t1\t1\t1.0\t150\t动力车间\t2026-03-31\t内部检验合格',
  '合计\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t3\t5\t—\t—\t—\t—\t3 台设备、5 件安全阀压力表由明细行加总',
  '--- 日常运行与巡检记录 ---',
  '设备编号\t记录日期\t运行压力(MPa)\t运行温度(℃)',
  'GL-2026-001\t2026-03-01\t1.05\t178',
  'GL-2026-001\t2026-03-02\t1.12\t182',
  'GL-2026-001\t2026-03-03\t1.18\t186',
  'GL-2026-001\t2026-03-04\t1.10\t180',
  'GL-2026-001\t2026-03-05\t1.15\t183',
  'GL-2026-002\t2026-03-01\t0.92\t96',
  'GL-2026-002\t2026-03-02\t0.95\t98',
  'GL-2026-002\t2026-03-03\t0.90\t94',
  'YLR-2026-003\t2026-03-10\t0.75\t45',
  'YLR-2026-003\t2026-03-11\t0.78\t47',
  'YLR-2026-003\t2026-03-12\t0.72\t43',
].join('\n');

const TOL = 0.01;

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = [
  'deviceNo', 'deviceName', 'deviceCategory', 'regCertNo', 'regCertExpiry',
  'lastInspectDate', 'inspectCycleMonths', 'nextInspectDate',
  'operator', 'operatorCertExpiry',
  'valveCheckDate', 'valveCycleMonths', 'nextValveCheckDate',
  'runStatus', 'checkDate',
];

// 单元格级必需字段（空白 / 占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['deviceNo', '设备编号'],
  ['deviceName', '设备名称'],
  ['deviceCategory', '设备类别'],
  ['regCertNo', '使用登记证号'],
  ['regCertExpiry', '登记证到期日'],
  ['lastInspectDate', '上次检验日期'],
  ['inspectCycleMonths', '检验周期(月)'],
  ['nextInspectDate', '下次检验日期'],
  ['operator', '作业人员'],
  ['operatorCertExpiry', '作业人员证到期日'],
  ['valveCheckDate', '安全阀校验日期'],
  ['valveCycleMonths', '校验周期(月)'],
  ['nextValveCheckDate', '下次校验日期'],
  ['runStatus', '运行状态'],
  ['checkDate', '核对日期'],
];

// 日期列（格式非法逐格点名）
const DATE_FIELDS = [
  ['regCertExpiry', '登记证到期日'],
  ['lastInspectDate', '上次检验日期'],
  ['nextInspectDate', '下次检验日期'],
  ['operatorCertExpiry', '作业人员证到期日'],
  ['valveCheckDate', '安全阀校验日期'],
  ['nextValveCheckDate', '下次校验日期'],
  ['checkDate', '核对日期'],
];

// 数值列（为负 / 无法解析逐格点名）
const NUMBER_FIELDS = [
  ['inspectCycleMonths', '检验周期(月)'],
  ['valveCycleMonths', '校验周期(月)'],
  ['deviceCount', '设备台数'],
  ['checkCount', '校验件数'],
  ['designPressureMax', '设计压力上限'],
  ['designTempMax', '设计温度上限'],
];

// 周期类列：等于 0 也是非法（周期为零 ⇒ 等于这台设备永远不用再检）
const CYCLE_ROLES = ['inspectCycleMonths', 'valveCycleMonths'];

// 运行状态只认这四个值（特种设备台账口径）
const RUN_STATUSES = ['在用', '停用', '报废', '检修'];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词就会把更具体的列抢走（本仓库踩过多次，见 tools/header_map_check.py）。
//    本表的坑位集中在日期列上：下次检验日期 / 上次检验日期 / 下次校验日期 / 安全阀校验日期 /
//    登记证到期日 / 作业人员证到期日 / 核对日期 —— 必须按「更具体 → 更宽泛」排；
//    兜底的 '日期' 只能放在所有日期角色之后。
const ROLES = {
  deviceNo: ['设备编号', '设备代码', '设备注册代码', '设备位号'],
  deviceCategory: ['设备类别', '设备种类', '设备分类'],
  deviceName: ['设备名称', '设备名'],
  regCertExpiry: ['使用登记证到期日', '登记证到期日', '登记证有效期至', '登记证有效期'],
  regCertNo: ['使用登记证号', '登记证号', '使用登记证编号'],
  nextInspectDate: ['下次检验日期', '下次检验日', '下次检验'],
  lastInspectDate: ['上次检验日期', '上次检验日', '检验日期', '上次检验'],
  inspectCycleMonths: ['检验周期月', '检验周期'],
  operatorCertExpiry: ['作业人员证到期日', '作业人员证有效期至', '作业人员证有效期', '人员证到期日'],
  operatorCertNo: ['作业人员证号', '作业人员证件号', '人员证号'],
  operator: ['作业人员', '司炉工', '水处理工', '操作人员', '持证人员'],
  nextValveCheckDate: ['下次校验日期', '下次校验日'],
  valveCycleMonths: ['校验周期月', '校验周期'],
  valveCheckDate: ['安全阀校验日期', '安全阀校验日', '压力表校验日期', '校验日期'],
  runStatus: ['运行状态', '使用状态', '设备状态'],
  checkDate: ['核对基准日', '核对日期', '核查日期', '基准日期', '基准日'],
  designPressureMax: ['设计压力上限', '设计压力', '压力上限'],
  designTempMax: ['设计温度上限', '设计温度', '温度上限'],
  deviceCount: ['设备台数', '台数'],
  checkCount: ['校验件数', '校验数量'],
  department: ['使用部门', '所属部门', '部门', '车间'],
  recordDate: ['记录日期', '巡检日期', '运行日期', '日期'],
  runPressure: ['运行压力', '实际压力', '工作压力'],
  runTemp: ['运行温度', '实际温度', '工作温度'],
  note: ['备注', '说明'],
};

const LABELS = {
  deviceNo: '设备编号',
  deviceName: '设备名称',
  deviceCategory: '设备类别',
  regCertNo: '使用登记证号',
  regCertExpiry: '登记证到期日',
  lastInspectDate: '上次检验日期',
  inspectCycleMonths: '检验周期(月)',
  nextInspectDate: '下次检验日期',
  operator: '作业人员',
  operatorCertNo: '作业人员证号',
  operatorCertExpiry: '作业人员证到期日',
  valveCheckDate: '安全阀校验日期',
  valveCycleMonths: '校验周期(月)',
  nextValveCheckDate: '下次校验日期',
  runStatus: '运行状态',
  deviceCount: '设备台数',
  checkCount: '校验件数',
  designPressureMax: '设计压力上限',
  designTempMax: '设计温度上限',
  department: '使用部门',
  checkDate: '核对日期',
  recordDate: '记录日期',
  runPressure: '运行压力',
  runTemp: '运行温度',
  note: '备注',
};

const SUM_ROLES = ['deviceCount', 'checkCount'];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张台账补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「覆盖」，也不说「超期」。',
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

const DAY_MS = 86400000;
function dayNum(iso) {
  const p = iso.split('-').map(Number);
  return Date.UTC(p[0], p[1] - 1, p[2]) / DAY_MS;
}
/** b − a（整天数，正数表示 b 在 a 之后） */
function daysBetween(a, b) {
  return dayNum(b) - dayNum(a);
}
/** 日期 + 月数（按自然月加，目标月没有那一天就退到当月最后一天） */
function addMonths(iso, months) {
  const p = iso.split('-').map(Number);
  const total = p[0] * 12 + (p[1] - 1) + months;
  const y = Math.floor(total / 12);
  const m = (total % 12) + 1;
  const lastDay = new Date(Date.UTC(y, m, 0)).getUTCDate();
  const d = Math.min(p[2], lastDay);
  return String(y).padStart(4, '0') + '-' + String(m).padStart(2, '0') + '-' + String(d).padStart(2, '0');
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
      if (h.indexOf(k) >= 0) return role;
    }
  }
  return null;
}

const TOTAL_LABEL = /^(合计|小计|总计|总合计|合\s*计)$/;
/** 合计行不是设备明细：逐台检查要跳过它，只有「合计行逐列复核」那一项会用到它 */
function isTotalRow(it) {
  const no = String(it.deviceNo == null ? '' : it.deviceNo).trim();
  const name = String(it.deviceName == null ? '' : it.deviceName).trim();
  return TOTAL_LABEL.test(no) || TOTAL_LABEL.test(name);
}

/**
 * 解析成 {header, cols, items, detail, totalRows, totals, missingRoles, missingColumns, error}。
 * items 是**扁平**对象：{line, raw, isTotal, 角色:值…}；遇到 `=== 段名 ===` 就停（后面是另一张表）。
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

function who(it) {
  const name = String(it.deviceName == null ? '' : it.deviceName).trim();
  const no = String(it.deviceNo == null ? '' : it.deviceNo).trim();
  return `第 ${it.line} 行「${name || no || '未命名设备'}${name && no ? ' / ' + no : ''}」`;
}

const cell = (it, role) => String(it[role] == null ? '' : it[role]).trim();

/** 每条结论都带原文依据：行号 + 设备编号 + 该行原文（截断），可被第三方用同一口径复算 */
function finding(level, category, it, diff, message, advice) {
  const f = {
    level,
    category,
    line: it.line,
    device_no: String(it.deviceNo == null ? '' : it.deviceNo).trim(),
    evidence: String(it.raw == null ? '' : it.raw).slice(0, 200),
    message,
  };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
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

/* ============================ 免费档检查（六项） ============================ */

function checkInspectionValidity(items, base) {
  // ① 检验有效期覆盖：核对基准日 ≤ 下次检验日期；不覆盖就报超期天数（逐台）
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const next = normDate(it.nextInspectDate);
    const b = baseOf(it, base);
    if (!next || !b) continue;                    // 缺字段 / 格式非法交给第 ⑥ 项点名
    const over = daysBetween(next, b);
    if (over <= 0) continue;
    const status = cell(it, 'runStatus');
    out.push(finding(status === '在用' ? 'P0' : 'P1', '检验超期', it, over,
      `${who(it)}：核对基准日 ${b} 已晚于下次检验日期 ${next}，**已超期 ${over} 天**`
      + `（设备类别 ${cell(it, 'deviceCategory') || '(未填)'}，运行状态 ${status || '(未填)'}）。`,
      '特种设备定期检验超期仍在用是监管直接查封/处罚项：先按上面天数排检验计划，'
      + '在用设备要先停用挂牌；检验合格换证后再投用。别只改台账日期。'));
  }
  return out;
}

function checkCertificates(items, base) {
  // ② 使用登记证与作业人员证：两证的到期日都要覆盖核对基准日；缺证 / 过期逐台点名
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const b = baseOf(it, base);

    const no = cell(it, 'regCertNo');
    const exp = cell(it, 'regCertExpiry');
    if (!no || isBlank(exp)) {
      out.push(finding('P1', '使用登记证过期或缺失', it, undefined,
        `${who(it)}：${!no ? '使用登记证号是空的' : '使用登记证号 ' + no + ' 的到期日没填'}`
        + `—— 缺证就说不上"已办理使用登记"（设备编号 ${cell(it, 'deviceNo') || '(未填)'}）。`,
        '特种设备投用前必须办理使用登记证；缺证的先去登记机关补办，再把证号与有效期填回台账。'));
    } else {
      const d = normDate(exp);
      if (d && b && daysBetween(d, b) > 0) {
        const over = daysBetween(d, b);
        out.push(finding('P0', '使用登记证过期或缺失', it, over,
          `${who(it)}：使用登记证 ${no} 到期日 ${d}，早于核对基准日 ${b}，**已过期 ${over} 天**。`,
          '登记证过期等于设备处于无证使用状态：立刻办理换证，换证期间按当地要求停用或限制使用。'));
      }
    }

    const op = cell(it, 'operator');
    const oexp = cell(it, 'operatorCertExpiry');
    if (!op || isBlank(oexp)) {
      out.push(finding('P1', '作业人员证过期或缺失', it, undefined,
        `${who(it)}：${!op ? '作业人员是空的' : '作业人员 ' + op + ' 的证件到期日没填'}`
        + '—— 司炉工 / 水处理工无证上岗是直接处罚项。',
        '把持证作业人员的姓名与证件到期日逐台补进台账；证件在别处的也必须在台账里能点到。'));
    } else {
      const d = normDate(oexp);
      if (d && b && daysBetween(d, b) > 0) {
        const over = daysBetween(d, b);
        out.push(finding('P0', '作业人员证过期或缺失', it, over,
          `${who(it)}：作业人员 ${op} 的证件到期日 ${d}，早于核对基准日 ${b}，**已过期 ${over} 天**。`,
          '证件过期期间不得独立操作：先安排复审或换人，复审通过后再把这台设备交回原持证人。'));
      }
    }
  }
  return out;
}

function checkValveCalibration(items, base) {
  // ③ 安全阀 / 压力表校验：校验日期 + 校验周期 = 下次校验日期（逐行复算），再判超期天数
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const vd = normDate(it.valveCheckDate);
    const cyc = normNumber(it.valveCycleMonths);
    const nd = normDate(it.nextValveCheckDate);

    if (vd && cyc !== null && cyc > 0) {
      const replay = addMonths(vd, cyc);
      if (nd && nd !== replay) {
        const drift = daysBetween(replay, nd);
        out.push(finding('P2', '校验周期与下次校验日期不符', it, drift,
          `${who(it)}：安全阀校验日期 ${vd} + 校验周期 ${cyc} 个月 = ${replay}，`
          + `但台账写的下次校验日期是 ${nd}，差 ${Math.abs(drift)} 天（复算值 − 台账值）。`,
          '两个字段只能有一个是对的：要么校验日期抄错，要么周期填错（锅炉安全阀一般每年至少校验一次）。'
          + '先拿校验报告上的日期与周期改正，再重跑。'));
      }
    }

    const b = baseOf(it, base);
    if (nd && b) {
      const over = daysBetween(nd, b);
      if (over > 0) {
        out.push(finding('P0', '安全阀校验超期', it, over,
          `${who(it)}：下次校验日期 ${nd}，早于核对基准日 ${b}，**已超期 ${over} 天**`
          + `（校验件数 ${cell(it, 'checkCount') || '(未填)'} 件）。`,
          '安全阀 / 压力表超期未校验等于超压保护上有空白：立即联系有资质的校验机构上门校验，'
          + '校验报告回来后同步更新校验日期与下次校验日期。'));
      }
    }
  }
  return out;
}

function checkDuplicateDevice(items) {
  // ④ 同一设备编号重复登记：一本台账里设备编号唯一
  const out = [];
  const first = new Map();
  for (const it of items) {
    if (it.isTotal) continue;
    const no = cell(it, 'deviceNo');
    if (!no) continue;
    if (first.has(no)) {
      out.push(finding('P0', '设备重复登记', it, undefined,
        `${who(it)}：设备编号「${no}」在第 ${first.get(no)} 行已经出现过 —— 同一台设备重复登记。`
        + `本次这行名称是「${cell(it, 'deviceName') || '(未填)'}」。`,
        '一台设备在一本台账里只应有一行：重复登记会让检验有效期与校验日期各算一套，'
        + '极容易出现"其中一行超期了却没人发现"。合并成一行，历史记录写进备注。'));
    } else {
      first.set(no, it.line);
    }
  }
  return out;
}

function checkTotals(items, cols) {
  // ⑤ 合计行逐列复核：数量类列（设备台数、校验件数）的合计行必须等于明细行加总
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
          '合计行只能写数字；请核对是否把单位（台 / 件）写进了单元格里。'));
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
        + '（本工具只核这一个合计行，不替你去别的表里找补。）'));
    }
  }
  return out;
}

function checkFieldIntegrity(items) {
  // ⑥ 空白 / 占位符 / 日期格式 / 数值为负或周期为零 / 运行状态非法
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        `${who(it)}：这些关键字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的字段会让对应的核对整项做不了（例如下次检验日期空着就判不了检验覆盖）；'
        + '补全后重跑，本工具不会替你猜一个默认值。'));
    }

    for (const [role, label] of DATE_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      if (normDate(raw) === null) {
        out.push(finding('P1', '日期格式非法', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的日期`
          + '（只认 2026-03-31 / 2026/3/31 / 2026年3月31日 / 20260331 这几种形态）。',
          '把日期改成 2026-03-31 这种形态再跑；日期认不出来时本工具不会拿它去算超期天数。'));
      }
    }

    for (const [role, label] of NUMBER_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        out.push(finding('P1', '数值为负或非法', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的数字。`,
          '数量与周期都必须是纯数字（如 1 / 12）；写成「十二个月」「壹」这类形态本工具一律不给结论。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '数值为负或非法', it, n,
          `${who(it)}：「${label}」是负数（${n}）—— 台账里的台数 / 件数 / 周期出现负数，通常是填反了或写成了红字。`,
          '确认是红字冲销还是填错方向；确属冲销的请写在备注里并保留原值，别直接改成正数。'));
      } else if (n === 0 && CYCLE_ROLES.indexOf(role) >= 0) {
        out.push(finding('P1', '数值为负或非法', it, n,
          `${who(it)}：「${label}」是 0 —— 周期为零等于这台设备永远不用再检验 / 再校验，台账口径上不成立。`,
          '按设备类别填真实的检验周期（锅炉一般 12 个月）；确实不需要再检的应走报废流程，而不是把周期写 0。'));
      }
    }

    const status = cell(it, 'runStatus');
    if (status && RUN_STATUSES.indexOf(status) < 0) {
      out.push(finding('P1', '运行状态非法', it, undefined,
        `${who(it)}：运行状态写的是「${status}」，不在允许的四个值里（${RUN_STATUSES.join(' / ')}）。`,
        '运行状态会直接决定"超期未检仍在用"这类结论：按实际状态改成 在用 / 停用 / 报废 / 检修 之一。'));
    }
  }
  return out;
}

/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的锅炉 / 压力容器 / 压力管道定期检验与台账核对表']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的锅炉 / 压力容器 / 压力管道定期检验与台账核对表']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的定期检验与台账核对表（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.detail.length) {
    return insufficient(['至少一行设备明细（现在只有表头或只有合计行，没有可核对的设备）']);
  }

  const base = baseDateOf(t.items);
  const findings = [];
  const notRun = [];

  for (const f of checkInspectionValidity(t.items, base)) findings.push(f);
  for (const f of checkCertificates(t.items, base)) findings.push(f);
  for (const f of checkValveCalibration(t.items, base)) findings.push(f);
  for (const f of checkDuplicateDevice(t.items)) findings.push(f);
  for (const f of checkTotals(t.items, t.cols)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

  // 免费档：完整档追加的那五项检查一项都不执行，这里如实记下来（只记「没做」，绝不伪造结论）
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const deviceTotal = t.totals.deviceCount;
  const checkTotal = t.totals.checkCount;
  const overdueRows = findings.filter((f) => f.category === '检验超期');
  const overdueMax = overdueRows.reduce((m, f) => Math.max(m, f.diff || 0), 0);

  const result = {
    findings,
    summary: {
      rows: t.detail.length,
      total_rows: t.totalRows.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      device_count_total: deviceTotal,
      check_count_total: checkTotal,
      overdue_devices: overdueRows.length,
      overdue_days_max: overdueMax,
      check_date: base,
      basis: '核对基准日（表内「核对日期」，逐行为准、缺行用表内第一个）≤ 下次检验日期才算检验有效期被覆盖；'
        + '使用登记证到期日与作业人员证到期日都要覆盖核对基准日；'
        + '安全阀 / 压力表按「校验日期 + 校验周期(月)」复算下次校验日期，并与台账值逐行比对、与核对基准日判超期；'
        + '同一设备编号在一本台账里唯一；合计行（设备台数、校验件数）必须等于明细行逐列加总；'
        + '运行状态只认 在用 / 停用 / 报废 / 检修 四个值。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这本台账按上面写明的口径算得对、'
      + '两证与校验日期都覆盖了核对基准日**，不代表定期检验结论本身合格、'
      + '不代表现场隐患已经整改闭环、也不代表登记证与作业人员证的真伪已经核验 —— 那些不在本工具范围内。';
  }

  const scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.detail.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    device_count_total: deviceTotal,
    check_count_total: checkTotal,
    check_date: base,
  };
  result.scope = scope;

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, normDate, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
