#!/usr/bin/env node
/**
 * carbon-emission-report-check-full.js —— 碳排放报告数据核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：纳入全国碳市场的重点排放单位**每年**都要提交温室气体排放报告并接受第三方核查。
 * 报告里的每一格排放量由「活动数据 × 排放因子 × 氧化率」逐项算出，再汇总到分设施 / 分范围
 * （范围一 直接排放、范围二 间接排放）；核查机构会**逐格复算**，算不平就要退回重报，
 * 甚至影响配额清缴。企业的能源 / 安环 / 财务在编制与迎检阶段必须自己先算一遍、把勾稽关系对上。
 *
 * 本文件是**订阅版（买断版）**：在本包六项逐行核对之上，多出**与上一年度报告对比、
 * 排放因子口径与官方缺省值核对、配额（分配量）与实际排放量对比、跨期/跨版本不一致检测、
 * 分设施×分范围汇总清单（consolidated_actions）**这五项。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定报告是否满足核查技术规范、不判定参数选取是否恰当、不核活动数据的真实性、
 *          不读 .xlsx/.pdf 原件、不联网取官方缺省值与配额文件；材料不足**一律不给结论**。
 *
 * ⚠️ 订阅版形态：付费开关**只在入口 run 里声明一次**，付费检查一律包在 `if (开关) { … }` 块里。
 *    写注释时不要复述那一行的源码 —— 摘除工具的残渣断言是**纯字符串包含**判断，复述会被判「没删干净」。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '单项排放量复算（逐行：活动数据 × 排放因子 × 氧化率 = 排放量，容差 0.01 tCO2e；不平即报出三处输入与差额）',
  '分设施/分范围 小计与合计 = 明细之和（逐列复核「活动数据」与「排放量（tCO2e）」两列，含合计行跨设施汇总）',
  '间接排放（范围二）单位换算勾稽（万kWh / kWh / MWh / GJ 折算 MWh，逐行复核「活动数据折算（MWh）」列）',
  '同一设施 + 同一能源品种 + 同一报告年度 的重复行检测（同一品种跨年度出现不算重复）',
  '同一能源品种（同一排放因子单位）在不同行引用不同排放因子值（报出并给两处原文）',
  '必需列与必需字段检测（空白/占位符/认不出格式；缺必需列只报「材料不足」，绝不给结论）',
];

const CHECKS_WITHHELD = [
  '与上一年度报告对比（同类设施/品种排放量变化超 ±20% 提示，并给本年度与上年度两处原文）',
  '排放因子与官方缺省值/实测值口径不一致检测（写「实测值」取值就是官方缺省值，或写「缺省值」但数值与官方缺省值不符）',
  '配额（分配量）与实际排放量对比（缺口/盈余吨数与需清缴量；同设施同年度配额填了不同值一并报出）',
  '跨期/跨版本不一致检测（同一报告年度出现多个报告版本、同一版本跨多个年度、同设施同品种数据来源跨年度不一致）',
  '分设施×分范围汇总清单（按差异吨数从大到小排序，逐条给出可整改动作 consolidated_actions）',
];

const OUT_OF_SCOPE = [
  '判定这份报告是否满足主管部门的核查技术规范、会不会被核查机构退回 —— 那是核查机构的认定权，本工具不做',
  '判定排放因子、低位发热量、碳氧化率等参数的选取是否恰当（该不该用实测值、缺省值适用条件），本工具只核报告内部的算术与口径字面一致性',
  '核查活动数据的真实性（发票、过磅单、化验单是否真实）与是否漏报了排放源，本工具只做表内复算与勾稽',
  '读取 .xlsx / .pdf 原件、联网取官方缺省值与配额分配文件、替代第三方核查报告或核查意见',
];

const TOL = 0.01;          // 排放量/合计的绝对容差（tCO2e）
const YOY_PCT = 20;        // 与上一年度对比的阈值（%）
const TOL_RATE = 1e-9;     // 大数换算的相对容差

// 样例：一张**干净**的重点排放单位排放报告明细表 —— 两个设施、两个范围、两个报告年度，
// 逐行 活动数据×因子×氧化率 = 排放量、小计/合计等于明细之和、单位换算对得上、
// 同一品种因子取值一致、配额与实际排放量刚好持平、跨年度数据来源与版本也一致。
// 企业名与设施名均为编造（示例数据），不含任何身份证号 / 统一社会信用代码。
const SAMPLE_HEADER = [
  '行类型', '设施名称', '报告年度', '范围', '能源品种', '活动数据', '活动数据单位',
  '活动数据折算（MWh）', '排放因子', '排放因子单位', '氧化率', '排放量（tCO2e）',
  '上年度排放量（tCO2e）', '因子口径', '官方缺省值', '配额分配量（tCO2e）',
  '数据来源', '报告版本', '备注',
];
const SAMPLE_ROWS = [
  ['明细', '云溪一号熟料线', '2025', '范围一', '烟煤', '12000', 't', '', '2.66', 'tCO2e/t', '0.98',
    '31281.60', '32000', '实测值', '2.60', '58656.00', '能源台账', 'V2025.1', '低位发热量实测送检（示例数据）'],
  ['明细', '云溪一号熟料线', '2025', '范围二', '电力', '4800', '万kWh', '48000', '5.703', 'tCO2e/万kWh', '1',
    '27374.40', '28000', '缺省值', '5.703', '58656.00', '能源台账', 'V2025.1', '外购电 4800 万kWh（示例数据）'],
  ['明细', '云溪二号粉磨站', '2025', '范围一', '柴油', '260', 't', '', '3.10', 'tCO2e/t', '0.99',
    '797.94', '850', '实测值', '3.02', '1787.94', '能源台账', 'V2025.1', '厂内运输柴油（示例数据）'],
  ['明细', '云溪二号粉磨站', '2025', '范围二', '热力', '9000', 'GJ', '2500', '0.11', 'tCO2e/GJ', '1',
    '990.00', '1020', '缺省值', '0.11', '1787.94', '能源台账', 'V2025.1', '外购蒸汽 9000 GJ（示例数据）'],
  ['小计', '云溪一号熟料线', '2025', '范围一', '', '12000', 't', '', '', '', '',
    '31281.60', '32000', '', '', '', '能源台账', 'V2025.1', '本设施本范围小计（示例数据）'],
  ['小计', '云溪一号熟料线', '2025', '范围二', '', '4800', '万kWh', '', '', '', '',
    '27374.40', '28000', '', '', '', '能源台账', 'V2025.1', '本设施本范围小计（示例数据）'],
  ['小计', '云溪二号粉磨站', '2025', '范围一', '', '260', 't', '', '', '', '',
    '797.94', '850', '', '', '', '能源台账', 'V2025.1', '本设施本范围小计（示例数据）'],
  ['小计', '云溪二号粉磨站', '2025', '范围二', '', '9000', 'GJ', '', '', '', '',
    '990.00', '1020', '', '', '', '能源台账', 'V2025.1', '本设施本范围小计（示例数据）'],
  ['合计', '', '2025', '范围一', '', '12260', 't', '', '', '', '',
    '32079.54', '32850', '', '', '', '', 'V2025.1', '全厂范围一合计（示例数据）'],
  ['合计', '', '2025', '范围二', '', '', '', '', '', '', '',
    '28364.40', '29020', '', '', '', '', 'V2025.1', '全厂范围二合计（明细单位不一致，故活动数据列留空）'],
  ['明细', '云溪一号熟料线', '2024', '范围一', '烟煤', '12600', 't', '', '2.66', 'tCO2e/t', '0.98',
    '32845.68', '33500', '实测值', '2.60', '60790.38', '能源台账', 'V2024.1', '上年度报告同一口径（示例数据）'],
  ['明细', '云溪一号熟料线', '2024', '范围二', '电力', '4900', '万kWh', '49000', '5.703', 'tCO2e/万kWh', '1',
    '27944.70', '28500', '缺省值', '5.703', '60790.38', '能源台账', 'V2024.1', '上年度报告同一口径（示例数据）'],
  ['明细', '云溪二号粉磨站', '2024', '范围一', '柴油', '270', 't', '', '3.10', 'tCO2e/t', '0.99',
    '828.63', '800', '实测值', '3.02', '1796.63', '能源台账', 'V2024.1', '上年度报告同一口径（示例数据）'],
  ['明细', '云溪二号粉磨站', '2024', '范围二', '热力', '8800', 'GJ', '2444.44', '0.11', 'tCO2e/GJ', '1',
    '968.00', '1000', '缺省值', '0.11', '1796.63', '能源台账', 'V2024.1', '上年度报告同一口径（示例数据）'],
];
const SAMPLE_TEXT = [SAMPLE_HEADER.join('\t')].concat(SAMPLE_ROWS.map((r) => r.join('\t'))).join('\n');

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = ['lineType', 'facility', 'scope', 'energyType', 'activityData', 'activityUnit',
  'activityMWh', 'factor', 'factorUnit', 'oxidation', 'emission'];

// 单元格级必需字段（只对明细行判；空白/占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['facility', '设施名称'],
  ['scope', '范围'],
  ['energyType', '能源品种'],
  ['activityData', '活动数据'],
  ['activityUnit', '活动数据单位'],
  ['factor', '排放因子'],
  ['factorUnit', '排放因子单位'],
  ['oxidation', '氧化率'],
  ['emission', '排放量（tCO2e）'],
];

// 数值列（用于「认不出格式 / 为负」判定）
const NUMBER_FIELDS = [
  ['activityData', '活动数据'],
  ['activityMWh', '活动数据折算（MWh）'],
  ['factor', '排放因子'],
  ['oxidation', '氧化率'],
  ['emission', '排放量（tCO2e）'],
  ['lastYearEmission', '上年度排放量（tCO2e）'],
  ['factorDefault', '官方缺省值'],
  ['quota', '配额分配量（tCO2e）'],
];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词会抢走更具体的列（本仓库踩过多次，见 tools/header_map_check.py）。
//    例：「上年度排放量」必须排在「排放量」前（否则被抢）；「因子口径」必须排在「排放因子」前；
//    「排放因子单位」必须排在通用的「单位」前；「配额分配量」不能被子串「用量」抢走。
const ROLES = {
  lineType: ['行类型', '记录类型', '数据行类型', '明细类型'],
  facility: ['设施名称', '排放设施', '主要设施', '重点设施', '设施', '厂区', '装置', '生产线'],
  lastYearEmission: ['上年度排放量', '上年度排放', '上年排放量', '上年同期排放量', '上年排放'],
  emission: ['排放量', '排放合计', '二氧化碳排放'],
  year: ['报告年度', '核算年度', '数据年度', '报告期', '年度', '年份'],
  scope: ['排放范围', '范围类别', '范围', '范畴'],
  energyType: ['能源品种', '能源种类', '燃料品种', '能源', '品种'],
  factorDefault: ['官方缺省值', '官方默认值', '缺省值', '默认因子', '缺省因子'],
  factorBasis: ['因子口径', '因子来源', '数值口径', '取值口径', '口径'],
  factorUnit: ['排放因子单位', '因子单位', '因子计量单位'],
  factor: ['排放因子', '碳排放因子', '排放系数', '因子'],
  activityMWh: ['活动数据折算', '折标活动数据', '折算活动数据'],
  activityUnit: ['活动数据单位', '活动量单位', '消耗量单位', '计量单位', '单位'],
  activityData: ['活动数据', '活动量', '消耗量', '消费量', '用量'],
  oxidation: ['氧化率', '碳氧化率', '氧化比例'],
  quota: ['配额分配量', '预分配配额', '发放配额', '分配量', '配额'],
  dataSource: ['数据来源', '数据出处', '来源'],
  reportVersion: ['报告版本', '版本号', '版本'],
  note: ['备注', '说明', '附注'],
};

const LABELS = {
  lineType: '行类型',
  facility: '设施名称',
  year: '报告年度',
  scope: '范围',
  energyType: '能源品种',
  activityData: '活动数据',
  activityUnit: '活动数据单位',
  activityMWh: '活动数据折算（MWh）',
  factor: '排放因子',
  factorUnit: '排放因子单位',
  oxidation: '氧化率',
  emission: '排放量（tCO2e）',
  lastYearEmission: '上年度排放量（tCO2e）',
  factorBasis: '因子口径',
  factorDefault: '官方缺省值',
  quota: '配额分配量（tCO2e）',
  dataSource: '数据来源',
  reportVersion: '报告版本',
  note: '备注',
};

const SUM_ROLES = ['activityData', 'emission', 'lastYearEmission'];

// 单位 → MWh 的换算表（间接排放的单位换算勾稽用；只认这几个，认不出就不给结论）
const MWH_PER_UNIT = {
  mwh: 1, 兆瓦时: 1,
  万kwh: 10, 万千瓦时: 10, 万度: 10,
  kwh: 0.001, 千瓦时: 0.001, 度: 0.001,
  gwh: 1000, 吉瓦时: 1000,
  gj: 1 / 3.6, 吉焦: 1 / 3.6,
};

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张表补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「一致」，也不说「不一致」。',
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

const txt = (v) => (v === undefined || v === null ? '' : String(v).trim());

const fmt = (n) => {
  const v = Math.abs(n) < 0.005 ? 0 : n;
  return v.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
};

/** 明细 / 小计 / 合计 —— 只有明细行参与逐行复算、因子与重复检测 */
function rowKindOf(it) {
  const k = txt(it.lineType);
  if (/合计|总计|汇总/.test(k)) return 'total';
  if (/小计|分计|subtotal/i.test(k)) return 'subtotal';
  return 'detail';
}

const isDetail = (it) => rowKindOf(it) === 'detail';

const isIndirect = (it) => /间接|范围二|范围2|scope\s*2/i.test(txt(it.scope));

function who(it) {
  const kind = rowKindOf(it);
  const tag = kind === 'detail' ? '' : (kind === 'total' ? '（合计行）' : '（小计行）');
  const fac = txt(it.facility) || '(未填设施)';
  const et = txt(it.energyType);
  return `第 ${it.line} 行「${fac}${tag}${et ? ' · ' + et : ''}」`;
}

const cite = (it) => `原文（第 ${it.line} 行）：「${it.raw}」`;

function finding(level, category, it, diff, message, advice) {
  const f = { level, category, line: it.line, message };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

const unitKey = (u) => txt(u).toLowerCase().replace(/[\s（）()]/g, '');

/* ============================ 本包检查（六项） ============================ */

/** 1. 单项排放量复算：活动数据 × 排放因子 × 氧化率 = 排放量（逐行） */
function checkRecompute(items) {
  const out = [];
  for (const it of items) {
    if (!isDetail(it)) continue;
    const a = normNumber(it.activityData);
    const f = normNumber(it.factor);
    const o = normNumber(it.oxidation);
    const e = normNumber(it.emission);
    if (a === null || f === null || o === null || e === null) continue;   // 缺失/认不出交给「必需字段」那一项
    const expected = round2(a * f * o);
    const diff = round2(e - expected);
    const tol = Math.max(TOL, Math.abs(expected) * TOL_RATE);
    if (Math.abs(diff) < tol) continue;
    out.push(finding('P0', '单项排放量复算不平', it, diff,
      `${who(it)}：活动数据 ${fmt(a)} × 排放因子 ${fmt(f)} × 氧化率 ${fmt(o)} = ${fmt(expected)} tCO2e，`
      + `但报告里「排放量（tCO2e）」写的是 ${fmt(e)}，差 ${fmt(diff)} tCO2e。`
      + `（本行原文：${cite(it)}）`,
      '按这一行的活动数据来源单（过磅单 / 电费单 / 化验单）与因子出处逐格复算；差额必须落回某一个输入上，别只改结果数。'));
  }
  return out;
}

/** 2. 分设施/分范围 小计与合计 = 明细之和（逐列复核 活动数据 与 排放量 两列） */
function checkSubtotalColumn(items) {
  const out = [];
  const details = items.filter(isDetail);
  for (const it of items) {
    const kind = rowKindOf(it);
    if (kind === 'detail') continue;
    const fac = txt(it.facility);
    const sc = txt(it.scope);
    const yr = txt(it.year);
    // 小计行按「同设施」；合计行（设施留空）按全表同范围汇总
    const group = details.filter((d) => {
      if (kind === 'subtotal' && fac && txt(d.facility) !== fac) return false;
      if (sc && txt(d.scope) !== sc) return false;
      if (yr && txt(d.year) !== yr) return false;
      return true;
    });
    if (!group.length) continue;                       // 找不到对应明细 ⇒ 不下结论（不猜）

    const declaredE = normNumber(it.emission);
    if (declaredE !== null) {
      const sumE = round2(group.reduce((acc, d) => acc + num(d, 'emission'), 0));
      const diffE = round2(declaredE - sumE);
      const tolE = Math.max(TOL, Math.abs(sumE) * TOL_RATE);
      if (Math.abs(diffE) >= tolE) {
        out.push(finding('P0', '小计或合计与明细之和不符', it, diffE,
          `${who(it)}：「排放量（tCO2e）」写的是 ${fmt(declaredE)}，但该组 ${group.length} 条明细之和是 ${fmt(sumE)}`
          + `（${group.map((d) => `第 ${d.line} 行 ${fmt(num(d, 'emission'))}`).join('、')}），差 ${fmt(diffE)} tCO2e。`,
          '小计/合计行要用明细逐行重算；改过明细就必须重刷小计 —— 核查机构正是按明细逐格复算再对小计的。'));
      }
    }

    const declaredA = normNumber(it.activityData);
    const units = new Set(group.map((d) => txt(d.activityUnit)).filter((u) => u !== ''));
    if (declaredA !== null && units.size <= 1) {       // 明细单位不一致时这一列不给结论
      const sumA = round2(group.reduce((acc, d) => acc + num(d, 'activityData'), 0));
      const diffA = round2(declaredA - sumA);
      const tolA = Math.max(TOL, Math.abs(sumA) * TOL_RATE);
      if (Math.abs(diffA) >= tolA) {
        out.push(finding('P0', '小计或合计与明细之和不符', it, diffA,
          `${who(it)}：「活动数据」写的是 ${fmt(declaredA)}，但该组 ${group.length} 条明细之和是 ${fmt(sumA)}`
          + `（${group.map((d) => `第 ${d.line} 行 ${fmt(num(d, 'activityData'))}`).join('、')}），差 ${fmt(diffA)}。`,
          '活动数据列的小计要与明细逐行对上；单位不统一时请先把单位统一到同一口径（本工具在该组明细单位不一致时不对这一列下结论）。'));
      }
    }
  }
  return out;
}

/** 3. 间接排放（范围二）单位换算勾稽：活动数据 × 换算系数 = 活动数据折算（MWh） */
function checkUnitConversion(items) {
  const out = [];
  for (const it of items) {
    if (!isDetail(it) || !isIndirect(it)) continue;
    const mwh = normNumber(it.activityMWh);
    if (mwh === null) continue;                        // 没填折算值 ⇒ 这一项没有材料，不给结论
    const a = normNumber(it.activityData);
    const unit = txt(it.activityUnit);
    const k = MWH_PER_UNIT[unitKey(unit)];
    if (k === undefined) {
      out.push(finding('P1', '间接排放单位无法换算', it, undefined,
        `${who(it)}：范围二的活动数据单位「${unit}」不在本工具的换算表内（只认 万kWh / kWh / MWh / GWh / GJ），`
        + '因此这一行的间接排放单位换算勾稽做不了 —— 不给结论。',
        '把单位写成 万kWh / kWh / MWh / GWh / GJ 之一（或在其后注明换算关系）再重跑。'));
      continue;
    }
    if (a === null) continue;
    const expected = round2(a * k);
    const diff = round2(mwh - expected);
    const tol = Math.max(TOL, Math.abs(expected) * TOL_RATE);
    if (Math.abs(diff) < tol) continue;
    out.push(finding('P0', '间接排放单位换算勾稽不符', it, diff,
      `${who(it)}：范围二的活动数据 ${fmt(a)} ${unit}，按 1 ${unit} = ${k} MWh 应折算 ${fmt(expected)} MWh，`
      + `但「活动数据折算（MWh）」列写的是 ${fmt(mwh)}，差 ${fmt(diff)} MWh。`
      + `（本行原文：${cite(it)}）`,
      'MWh ↔ 万kWh ↔ kWh ↔ GJ 的换算最容易差 10 倍或 3.6 倍；先把「活动数据折算（MWh）」按同一口径重算，再重出间接排放量。'));
  }
  return out;
}

/** 4. 同一设施 + 同一能源品种 + 同一报告年度 的重复行 */
function checkDuplicateRows(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    if (!isDetail(it)) continue;
    const fac = txt(it.facility);
    const et = txt(it.energyType);
    const yr = txt(it.year);
    if (!fac || !et) continue;
    const key = `${fac}|${et}|${yr}`;
    if (!seen.has(key)) { seen.set(key, it); continue; }
    const first = seen.get(key);
    out.push(finding('P1', '同一设施同一年度能源品种重复行', it, undefined,
      `${who(it)}：设施「${fac}」+ 能源品种「${et}」+ 报告年度 ${yr || '(未填)'} 在第 ${first.line} 行已经出现过一次`
      + `（第 ${first.line} 行：活动数据 ${txt(first.activityData)}、排放量 ${txt(first.emission)}；`
      + `第 ${it.line} 行：活动数据 ${txt(it.activityData)}、排放量 ${txt(it.emission)}）—— 同一设施同一年度同一品种只应有一行。`,
      '同一年度里同一设施同一品种出现两行，多数是一条是重复粘贴、另一条才是修正稿；确认后删掉作废的那一行。'
      + '（同一品种跨年度出现是**正常的**：本项只按「同一报告年度」判重复。）'));
  }
  return out;
}

/** 5. 同一能源品种（同一排放因子单位）在不同行引用不同排放因子值 */
function checkFactorConsistency(items) {
  const out = [];
  const firstByKey = new Map();
  for (const it of items) {
    if (!isDetail(it)) continue;
    const et = txt(it.energyType);
    const fu = txt(it.factorUnit);
    if (!et || isBlank(it.factor)) continue;
    const f = normNumber(it.factor);
    if (f === null) continue;                          // 认不出的格式交给「数值无法解析」
    const key = `${et}|${fu}`;
    if (!firstByKey.has(key)) { firstByKey.set(key, it); continue; }
    const first = firstByKey.get(key);
    const f0 = normNumber(first.factor);
    if (f0 === null) continue;
    const diff = round2(f - f0);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding('P0', '同一能源品种排放因子不一致', it, diff,
      `同一能源品种「${et}」（排放因子单位 ${fu || '(未填)'}）在不同行用了两个排放因子值：`
      + `第 ${first.line} 行取 ${fmt(f0)}，第 ${it.line} 行取 ${fmt(f)}，差 ${fmt(diff)}。`
      + `两处原文：${cite(first)}；${cite(it)}`,
      '同一品种同一口径的因子取值应当一致；请确认哪一行是当年度正式取值，另一行（上年度口径 / 试算稿）须删掉或注明来源。'));
  }
  return out;
}

/** 6. 必需字段缺失 / 认不出格式 / 为负 / 氧化率越界 */
function checkFieldIntegrity(items) {
  const out = [];
  for (const it of items) {
    if (!isDetail(it)) continue;
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        `${who(it)}：这些必需字段是空的或占位符 —— ${miss.join('、')}。`,
        '必需字段空着，对应的复算就整项做不了；补全后重跑。本工具不会替你猜默认值，也不会因此给出「一致」的结论。'));
    }
    for (const [role, label] of NUMBER_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        out.push(finding('P1', '数值无法解析', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的数值（只认数字、千分位、括号负数、百分数）。`,
          '把这一格改成纯数字形态（如 31281.60）再跑；本工具不会把看不懂的值当成 0，也不会跳过它。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '数值为负', it, n,
          `${who(it)}：「${label}」是负数（${fmt(n)}）—— 活动数据与排放量出现负数，通常是填反了方向、写成了红字冲销，或把减少量直接写成负排放。`,
          '核对原始台账的方向；确属冲销的请保留原值并在「备注」里写明，别直接改成正数。'));
      }
    }
    const o = normNumber(it.oxidation);
    if (o !== null && (o <= 0 || o > 1)) {
      out.push(finding('P1', '氧化率超出合理范围', it, undefined,
        `${who(it)}：「氧化率」是 ${fmt(o)}，不在 (0, 1] 区间内 —— 氧化率是碳氧化比例，必须落在 0 到 1 之间（多数燃料为 0.98~1）。`,
        '核对是不是把百分数直接填成了 98（应为 0.98），或者漏了小数点。'));
    }
  }
  return out;
}

/* ===== 以下为订阅版才执行的检查 ===== */

/** 付费：与上一年度报告对比（同类设施/品种变化超 ±20%） */
function checkYearOverYear(it) {
  if (!isDetail(it)) return [];
  const cur = normNumber(it.emission);
  const prev = normNumber(it.lastYearEmission);
  if (cur === null || prev === null || Math.abs(prev) < TOL) return [];
  const diff = round2(cur - prev);
  const pct = round2((diff / Math.abs(prev)) * 100);
  if (Math.abs(pct) <= YOY_PCT) return [];
  return [finding(Math.abs(pct) >= 50 ? 'P0' : 'P1', '与上一年度报告对比异常（±20%）', it, diff,
    `${who(it)}：本年度报告这一格 ${fmt(cur)} tCO2e，上一年度报告中同一设施同一品种是 ${fmt(prev)} tCO2e，`
    + `变化 ${fmt(diff)} tCO2e（${pct > 0 ? '+' : ''}${fmt(pct)}%），超过 ±${YOY_PCT}% 阈值。`
    + `两处原文：本年度「排放量（tCO2e）」= ${fmt(cur)}；上年度「上年度排放量（tCO2e）」= ${fmt(prev)}。`
    + `（本行原文：${cite(it)}）`,
    '先分清是**真实变化**（产量、燃料结构、开工天数）还是**口径变化**（因子、边界、数据来源变了）；'
    + '超阈值项核查机构会要求单独说明，说明材料必须能对上这两处数值。')];
}

/** 付费：排放因子与官方缺省值 / 实测值口径是否自洽 */
function checkFactorBasis(it) {
  if (!isDetail(it)) return [];
  const basis = txt(it.factorBasis);
  const f = normNumber(it.factor);
  const def = normNumber(it.factorDefault);
  if (!basis || f === null || def === null) return [];
  const out = [];
  const measured = /实测|送检|检测|化验/.test(basis);
  const declared = /缺省|默认|官方/.test(basis);
  const diff = round2(f - def);
  if (measured && Math.abs(diff) < TOL) {
    out.push(finding('P1', '排放因子口径与官方缺省值不符', it, diff,
      `${who(it)}：「因子口径」写的是「${basis}」（实测/送检），但「排放因子」取值 ${fmt(f)} 与「官方缺省值」${fmt(def)} 完全相同 —— 口径写实测、数值就是官方缺省值。`
      + `两处原文：第 ${it.line} 行「因子口径」= ${basis}、「排放因子」= ${fmt(f)}、「官方缺省值」= ${fmt(def)}。`,
      '要么补上实测报告（低位发热量 / 单位热值含碳量 / 碳氧化率的检测结果）并让数值体现出来，要么把口径改成「缺省值」；'
      + '口径与数值不一致是核查最常退件的一类。'));
  }
  if (declared && Math.abs(diff) >= TOL) {
    out.push(finding('P0', '排放因子口径与官方缺省值不符', it, diff,
      `${who(it)}：「因子口径」写的是「${basis}」，但「排放因子」取值 ${fmt(f)} 与「官方缺省值」${fmt(def)} 不等（差 ${fmt(diff)}）—— 口径写缺省值、数值却不是官方缺省值。`
      + `两处原文：第 ${it.line} 行「排放因子」= ${fmt(f)}、「官方缺省值」= ${fmt(def)}。`,
      '核对「官方缺省值」一栏是否抄错、单位是否与「排放因子」一致；若当年发布了新缺省值，请更新这一列并注明出处文号。'));
  }
  return out;
}

/** 付费：同一报告年度出现多个报告版本 / 同一版本跨多个年度 / 同设施同品种数据来源跨年度不一致 */
function buildPeriodContext(items) {
  const byYear = new Map();       // 年度 → (版本 → 首次出现行号)
  const byVersion = new Map();    // 版本 → { 年度集合, 行号 }
  const byFacType = new Map();    // 设施|品种 → [{ line, year, source, raw }]
  for (const it of items) {
    if (!isDetail(it)) continue;
    const yr = txt(it.year);
    const ver = txt(it.reportVersion);
    const src = txt(it.dataSource);
    if (yr && ver) {
      if (!byYear.has(yr)) byYear.set(yr, new Map());
      const m = byYear.get(yr);
      if (!m.has(ver)) m.set(ver, it.line);
    }
    if (ver) {
      if (!byVersion.has(ver)) byVersion.set(ver, { years: new Map(), lines: [] });
      const v = byVersion.get(ver);
      if (yr && !v.years.has(yr)) v.years.set(yr, it.line);
      v.lines.push(it.line);
    }
    const fac = txt(it.facility);
    const et = txt(it.energyType);
    if (fac && et) {
      const key = `${fac}|${et}`;
      if (!byFacType.has(key)) byFacType.set(key, []);
      byFacType.get(key).push({ line: it.line, year: yr, source: src, raw: it.raw });
    }
  }
  return { byYear, byVersion, byFacType };
}

function checkCrossPeriodVersion(it, ctx) {
  if (!isDetail(it)) return [];
  const out = [];
  const yr = txt(it.year);
  const ver = txt(it.reportVersion);
  const src = txt(it.dataSource);

  if (yr && ver && ctx.byYear.has(yr)) {
    const m = ctx.byYear.get(yr);
    if (m.size > 1) {
      const firstVer = [...m.keys()][0];
      if (ver !== firstVer) {
        out.push(finding('P1', '跨期/跨版本或数据来源不一致', it, undefined,
          `${who(it)}：报告年度 ${yr} 里出现了两个「报告版本」—— 第 ${m.get(firstVer)} 行用「${firstVer}」，第 ${it.line} 行用「${ver}」。`
          + '同一份年度报告的版本号应当唯一。',
          '确认哪一版是报出的正式版本；同一轮编制里的过程稿不要和正式稿留在同一张表里，否则核查对不上版本。'));
      }
    }
  }

  if (ver && ctx.byVersion.has(ver)) {
    const v = ctx.byVersion.get(ver);
    if (v.years.size > 1 && it.line === Math.max(...v.lines)) {
      const list = [...v.years.entries()].map(([y, l]) => `${y} 年（第 ${l} 行）`).join('、');
      out.push(finding('P1', '跨期/跨版本或数据来源不一致', it, undefined,
        `${who(it)}：报告版本「${ver}」被用在 ${v.years.size} 个不同报告年度上（${list}）—— 一个版本号不应覆盖多个年度。`,
        '按年度分别编号（如 V2024.1 / V2025.1）；跨年度沿用同一版本号，会让核查分不清哪一版对应哪一年。'));
    }
  }

  const fac = txt(it.facility);
  const et = txt(it.energyType);
  if (fac && et && yr && src) {
    const list = ctx.byFacType.get(`${fac}|${et}`) || [];
    const other = list.find((x) => x.year && x.year !== yr && x.source && x.source !== src);
    if (other) {
      out.push(finding('P1', '跨期/跨版本或数据来源不一致', it, undefined,
        `${who(it)}：同一设施同一能源品种的数据来源跨年度不一致 —— 第 ${other.line} 行（${other.year} 年）用「${other.source}」，第 ${it.line} 行（${yr} 年）用「${src}」。`
        + `两处原文：${cite({ line: other.line, raw: other.raw })}；${cite(it)}`,
        '换了数据来源（台账系统更换、发票换成化验单）要在报告里写明变更原因并保留前后可比性说明，否则会被要求解释跨年口径。'));
    }
  }
  return out;
}

/** 付费：配额（分配量）与实际排放量对比 —— 缺口 / 盈余 / 需清缴量 */
function buildQuotaFindings(items) {
  const out = [];
  const groups = new Map();
  for (const it of items) {
    if (!isDetail(it)) continue;
    const fac = txt(it.facility);
    if (!fac) continue;
    const key = `${fac}|${txt(it.year)}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(it);
  }
  for (const [, list] of groups) {
    const quotaRows = list.filter((it) => !isBlank(it.quota));
    if (!quotaRows.length) continue;                   // 没填配额 ⇒ 这一项没有材料，不给结论
    const vals = quotaRows.map((it) => normNumber(it.quota)).filter((n) => n !== null);
    if (!vals.length) continue;
    const last = list[list.length - 1];
    const fac = txt(last.facility);
    const yr = txt(last.year) || '(未填年度)';
    if (vals.some((v) => Math.abs(v - vals[0]) >= TOL)) {
      out.push(finding('P1', '同一设施同一年度配额分配量不一致', quotaRows[0], round2(Math.max(...vals) - Math.min(...vals)),
        `设施「${fac}」${yr} 年的「配额分配量（tCO2e）」在 ${quotaRows.length} 行上填了不同值（${vals.map((v) => fmt(v)).join('、')}）`
        + '—— 配额是按设施按年度分配的，同一年度应当是同一个数。',
        '把该设施该年度的配额分配量（来自配额分配方案 / 预分配通知）统一填在同一列上，不要按范围拆开填不同数值。'));
    }
    const quota = vals[0];
    const emission = round2(list.reduce((acc, it) => acc + num(it, 'emission'), 0));
    const gap = round2(emission - quota);
    if (Math.abs(gap) < TOL) continue;
    out.push(finding(gap > 0 ? 'P0' : 'P2', '配额与实际排放量对比（缺口/盈余与需清缴量）', last, gap,
      `设施「${fac}」${yr} 年：实际排放量合计 ${fmt(emission)} tCO2e（${list.length} 条明细之和），配额分配量 ${fmt(quota)} tCO2e —— `
      + (gap > 0
        ? `**缺口 ${fmt(gap)} tCO2e**，需清缴量为 ${fmt(gap)} tCO2e（要靠市场购买或结余配额补足）。`
        : `**盈余 ${fmt(-gap)} tCO2e**（配额多于实际排放，可按当年度规则结转或出售）。`),
      gap > 0
        ? '先核对该设施该年度的活动数据与排放源是否已全部归集（漏算会低估排放）；缺口确认后要预留清缴成本与购买时间。'
        : '盈余不等于可以不管：先核有没有漏报的排放源、边界是否写全，确认后再考虑结转或出售。'));
  }
  return out;
}

/** 付费：分设施×分范围汇总清单（按差异吨数排序） */
function buildFacilityScopeSummary(items, findings) {
  const groups = new Map();
  for (const it of items) {
    if (!isDetail(it)) continue;
    const key = `${txt(it.facility)}|${txt(it.scope)}`;
    if (!groups.has(key)) {
      groups.set(key, {
        facility: txt(it.facility) || '(未填设施)', scope: txt(it.scope) || '(未填范围)',
        lines: [], emission: 0, lastYear: 0,
      });
    }
    const g = groups.get(key);
    g.lines.push(it.line);
    g.emission = round2(g.emission + num(it, 'emission'));
    g.lastYear = round2(g.lastYear + num(it, 'lastYearEmission'));
  }
  const out = [];
  for (const [, g] of groups) {
    const diff = round2(g.emission - g.lastYear);
    const pct = Math.abs(g.lastYear) < TOL ? null : round2((diff / Math.abs(g.lastYear)) * 100);
    const related = findings.filter((f) => g.lines.indexOf(f.line) >= 0);
    const worst = related.slice().sort((a, b) => Math.abs(b.diff || 0) - Math.abs(a.diff || 0))[0];
    out.push({
      facility: g.facility,
      scope: g.scope,
      rows: g.lines.length,
      lines: g.lines,
      emission: g.emission,
      last_year_emission: g.lastYear,
      diff_tco2e: diff,
      pct: pct,
      findings: related.length,
      top_category: worst ? worst.category : '',
      action: worst ? (worst.advice || '按列出的差异逐条核对原始单据。')
        : '本分组按同一口径复算平；把活动数据来源单与因子出处留档备查即可。',
    });
  }
  out.sort((a, b) => (Math.abs(b.diff_tco2e) - Math.abs(a.diff_tco2e))
    || String(a.facility).localeCompare(String(b.facility))
    || String(a.scope).localeCompare(String(b.scope)));
  return out;
}

/** 付费：汇总整改清单（按差异吨数从大到小排序，逐条给出可整改动作） */
function buildConsolidatedActions(findings, summary, items) {
  const info = new Map();
  for (const it of (items || [])) info.set(it.line, { facility: txt(it.facility), scope: txt(it.scope) });
  const rows = findings
    .filter((f) => typeof f.diff === 'number' && Number.isFinite(f.diff) && Math.abs(f.diff) >= TOL)
    .map((f) => Object.assign(
      { facility: '', scope: '' },
      info.get(f.line) || {},
      {
        level: f.level,
        line: f.line,
        category: f.category,
        diff: f.diff,
        abs_diff: round2(Math.abs(f.diff)),
        action: f.advice || '按列出的差异逐条核对原始单据。',
      }));
  const covered = new Set(rows.map((r) => r.line));
  const extra = (summary || [])
    .filter((s) => Math.abs(s.diff_tco2e) >= TOL && !(s.lines || []).some((ln) => covered.has(ln)))
    .map((s) => ({
      facility: s.facility, scope: s.scope, level: 'P2', line: 0,
      category: '分设施×分范围汇总差异', diff: s.diff_tco2e,
      abs_diff: round2(Math.abs(s.diff_tco2e)), action: s.action,
    }));
  const all = rows.concat(extra);
  all.sort((a, b) => (b.abs_diff - a.abs_diff)
    || ((a.line || 0) - (b.line || 0))
    || String(a.category).localeCompare(String(b.category)));
  return all.map((a, i) => Object.assign({ seq: i + 1 }, a));
}

/** 付费：跨年度 / 跨范围汇总台账（含配额缺口与需清缴量） */
function buildRollup(items) {
  const details = items.filter(isDetail);
  const blank = () => ({ rows: 0, emission: 0, last_year_emission: 0, activity: 0 });
  const add = (b, it) => {
    b.rows += 1;
    b.emission = round2(b.emission + num(it, 'emission'));
    b.last_year_emission = round2(b.last_year_emission + num(it, 'lastYearEmission'));
    b.activity = round2(b.activity + num(it, 'activityData'));
    return b;
  };
  const byYear = new Map();
  const byScope = new Map();
  for (const it of details) {
    const yr = txt(it.year) || '(未填年度)';
    const sc = txt(it.scope) || '(未填范围)';
    if (!byYear.has(yr)) byYear.set(yr, blank());
    if (!byScope.has(sc)) byScope.set(sc, blank());
    add(byYear.get(yr), it);
    add(byScope.get(sc), it);
  }
  const toRows = (map, key) => [...map.entries()]
    .sort((a, b) => String(a[0]).localeCompare(String(b[0])))
    .map(([k, v]) => Object.assign({ [key]: k }, v, { diff: round2(v.emission - v.last_year_emission) }));

  const qGroups = new Map();
  for (const it of details) {
    const fac = txt(it.facility);
    if (!fac) continue;
    const key = `${fac}|${txt(it.year)}`;
    if (!qGroups.has(key)) qGroups.set(key, []);
    qGroups.get(key).push(it);
  }
  const quotaRows = [];
  for (const [, list] of qGroups) {
    const withQuota = list.filter((it) => normNumber(it.quota) !== null);
    const emission = round2(list.reduce((acc, it) => acc + num(it, 'emission'), 0));
    if (!withQuota.length) {
      quotaRows.push({ facility: txt(list[0].facility), year: txt(list[0].year), rows: list.length, emission, quota: null, gap: null, surrender: null, surplus: null });
      continue;
    }
    const quota = normNumber(withQuota[0].quota);
    const gap = round2(emission - quota);
    quotaRows.push({
      facility: txt(list[0].facility), year: txt(list[0].year), rows: list.length, emission, quota, gap,
      surrender: gap > 0 ? gap : 0,
      surplus: gap < 0 ? round2(-gap) : 0,
    });
  }
  quotaRows.sort((a, b) => String(a.facility).localeCompare(String(b.facility)) || String(a.year).localeCompare(String(b.year)));
  const qTotal = quotaRows.reduce((acc, r) => {
    if (r.quota !== null) acc.quota = round2(acc.quota + r.quota);
    acc.surrender = round2(acc.surrender + (r.surrender || 0));
    acc.surplus = round2(acc.surplus + (r.surplus || 0));
    return acc;
  }, { quota: 0, surrender: 0, surplus: 0 });

  return {
    by_year: toRows(byYear, 'year'),
    by_scope: toRows(byScope, 'scope'),
    quota_by_facility_year: quotaRows,
    quota_total: qTotal.quota,
    surrender_total: qTotal.surrender,
    surplus_total: qTotal.surplus,
    total: details.reduce((acc, it) => add(acc, it), blank()),
  };
}

/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的排放报告明细表（至少要有 行类型 / 设施名称 / 范围 / 能源品种 / 活动数据 / 单位 / 排放因子 / 氧化率 / 排放量）']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的排放报告明细表（至少要有 行类型 / 设施名称 / 范围 / 能源品种 / 活动数据 / 单位 / 排放因子 / 氧化率 / 排放量）']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的排放报告明细表（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行排放明细（现在只有表头，没有可核对的明细行）']);
  }

  const paid = Boolean(p && (p.full || p.credit || p.token));
  const items = t.items;
  const findings = [];
  const notRun = [];

  for (const f of checkRecompute(items)) findings.push(f);
  for (const f of checkSubtotalColumn(items)) findings.push(f);
  for (const f of checkUnitConversion(items)) findings.push(f);
  for (const f of checkDuplicateRows(items)) findings.push(f);
  for (const f of checkFactorConsistency(items)) findings.push(f);
  for (const f of checkFieldIntegrity(items)) findings.push(f);

  let summaryTable = null;
  let rollup = null;

  if (paid) {
    const ctx = buildPeriodContext(items);
    for (const it of items) {
      for (const f of checkYearOverYear(it)) findings.push(f);
      for (const f of checkFactorBasis(it)) findings.push(f);
      for (const f of checkCrossPeriodVersion(it, ctx)) findings.push(f);
    }
    for (const f of buildQuotaFindings(items)) findings.push(f);

    // 付费项依赖的列没给 ⇒ 这一项如实标成「未执行」，绝不拿默认值凑结论
    const paidRequires = [
      ['与上一年度报告对比（±20%）', ['lastYearEmission']],
      ['排放因子与官方缺省值/实测值口径核对', ['factorBasis', 'factorDefault']],
      ['配额（分配量）与实际排放量对比', ['quota']],
      ['跨期/跨版本不一致检测', ['year', 'reportVersion', 'dataSource']],
    ];
    for (const [label, roles] of paidRequires) {
      const miss = roles.filter((r) => !t.cols.some((c) => c.role === r));
      if (miss.length) notRun.push(`${label}（缺列：${miss.map((r) => LABELS[r]).join('、')} —— 本项未执行，不给结论）`);
    }

    summaryTable = buildFacilityScopeSummary(items, findings);
    rollup = buildRollup(items);
  } else {
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  }

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const details = items.filter(isDetail);
  const result = {
    findings,
    summary: {
      rows: items.length,
      detail_rows: details.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      activity_total: t.totals.activityData,
      emission_total: t.totals.emission,
      last_year_emission_total: t.totals.lastYearEmission,
      basis: '逐行：活动数据 × 排放因子 × 氧化率 = 排放量（tCO2e，容差 0.01）；小计/合计行必须等于其对应明细之和（活动数据列仅在该组明细单位一致时复核）；'
        + '范围二的活动数据按 万kWh=10MWh、kWh=0.001MWh、GJ=1/3.6MWh 折算后要与「活动数据折算（MWh）」列一致；'
        + '同一设施 + 同一能源品种 + 同一报告年度只应有一行；同一能源品种（同一排放因子单位）的因子取值应当一致。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的口径算得平、勾稽对得上**，'
      + '不代表报告一定符合核查技术规范、参数选取一定恰当、活动数据一定真实 —— 那些不在本工具范围内。';
  }

  result.scope = {
    checks: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: items.length,
    detail_rows: details.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    activity_total: t.totals.activityData,
    emission_total: t.totals.emission,
    last_year_emission_total: t.totals.lastYearEmission,
  };

  if (paid) {
    result.rollup = rollup;
    result.facility_scope_summary = summaryTable;
    result.consolidated_actions = buildConsolidatedActions(findings, summaryTable, items);
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
  CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
