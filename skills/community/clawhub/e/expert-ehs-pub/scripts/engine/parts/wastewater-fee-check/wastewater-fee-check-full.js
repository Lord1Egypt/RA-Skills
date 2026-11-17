#!/usr/bin/env node
/**
 * wastewater-fee-check-full.js —— 污水处理费与水质数据核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：污水处理服务费按「处理水量 × 单价」结算，而这一步几乎全是跨列算术：
 *   ① 结算水量要与 进水/出水 计量勾稽（管网损耗、雨污混接、偷排都会让两边对不上）
 *   ② 服务费 = 结算水量 × 单价，还要与在线监测的水质数据对应的**档位单价**挂上
 *   ③ 超标项要按扣款标准算扣款 —— 漏算一条就是少收一笔钱
 *   ④ 同一计量点同一期间重复结算、跨期归属错位，年审与环保核查都会问到
 * 这些表都能手算复现 ⇒ 可以机械核对；而水务/环保运营企业每月对账都得做一遍。
 *
 * 本文件是**订阅版（买断版）**：在本包六项逐行核对之上，多出 阶梯/累进单价逐段复算、
 * 进水出水差额超允许损耗点名、在线监测与上报数据一致性、跨期归属检测、
 * 分计量点×分期间汇总清单与按差额金额排序的汇总整改清单（consolidated_actions）这五类能力。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定水质是否达标与超标事实本身是否成立、不核验在线监测设备是否校准、
 *          不判定单价与扣款标准是否合理合法、不读 .xlsx/.pdf 原件；材料不足**一律不给结论**。
 *
 * ⚠️ 免费包由 `tools/strip_free_engine.py` 从本文件摘出：
 *    · 付费实现集中在「订阅版才执行的检查」那一段，以及入口里的那一个付费块；
 *    · 付费开关**只在入口里声明一次**，付费检查一律包在那一个块里；
 *    · 写注释时不要复述开关那一行的源码 —— 残渣断言是**纯字符串包含**判断，复述会被判「没删干净」。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '处理水量勾稽（逐行复算 结算水量 = 出水水量 + 允许损耗，差额不为零即列出并给出差额）',
  '服务费金额勾稽（逐行复算 结算水量 × 单价 = 服务费，差额不为零即列出并给出差额）',
  '水质档位与单价一致性（按指标值查档：指标值须落在所填档位的上下限内；同一指标同一档位的上下限与档位单价跨行必须一致；'
    + '单一价行的所用单价须等于该档位的档位单价）',
  '超标扣款计算核对（超标项数 × 扣款标准 = 扣款额，漏算 / 算错 / 无法复算即报）',
  '同一计量点同一期间重复结算检测（计量点编号 或 计量点名称 + 结算期间 重复即报）',
  '空白 / 占位符 / 认不出格式检测（计量点编号、结算期间、进水水量、出水水量、结算水量、单价、服务费、水质指标、指标值、档位 缺失，'
    + '或数值无法解析、数值为负）',
];

const CHECKS_WITHHELD = [
  '阶梯 / 累进单价逐段复算（各档水量 × 各档单价 之和 = 应收服务费，且各档水量合计 = 结算水量）',
  '进水与出水水量差额超过合理损耗阈值（点名到计量点与期间，给出超出水量）',
  '在线监测数据与上报数据的一致性（同一指标同一天两处数值不一致，以及同一计量点+同一指标+同一天上报了不同的值）',
  '跨期归属检测（结算期间与水量发生日期不属于同一期）',
  '分计量点×分期间的汇总清单（按差额金额排序，给出可整改动作）与汇总整改清单 consolidated_actions',
];

const OUT_OF_SCOPE = [
  '判定水质是否达标、超标事实本身是否成立 —— 那是在线监测数据与生态环境主管部门的认定权，本工具只核上报数字与结算口径',
  '核验在线监测设备是否校准、监测数据是否造假（那是环保核查与仪器检定的职责）',
  '判定合同里的单价、档位区间、扣款标准本身是否合理合法，本工具只用你给的这些列做算术复核',
  '判定管网损耗 / 偷排的责任归属与索赔 —— 本工具只按你给的阈值把差额点出来',
  '读取 .xlsx / .pdf 原件、联网核验排污许可证与监测报告真伪、替代审计报告、法律意见或税务处理意见',
];

// 样例：一张**干净**的污水处理费结算与水质数据核对表 —— 2 个计量点 × 2 个结算期间，
// 结算水量 = 出水水量 + 允许损耗、服务费 = 结算水量 × 单价、指标值落在所填档位内、
// 同一档位的上下限与档位单价跨行一致、超标项数为 0 所以扣款额为 0、计量点+期间不重复。
const SAMPLE_TEXT = [
  '计量点名称\t计量点编号\t结算期间\t水量发生日期\t进水水量(m³)\t出水水量(m³)\t允许损耗(m³)\t结算水量(m³)\t单价(元/m³)\t服务费(元)\t第一档水量(m³)\t第一档单价(元/m³)\t第二档水量(m³)\t第二档单价(元/m³)\t第三档水量(m³)\t第三档单价(元/m³)\t水质指标\t指标值\t在线监测值\t档位下限\t档位上限\t档位\t档位单价(元/m³)\t超标项数\t扣款标准(元/次)\t扣款额(元)\t备注',
  '城东厂1#计量点\tJD-01\t2026-05\t2026-05-18\t32600\t31000\t1600\t32600\t1.20\t39120.00\t32600\t1.20\t0\t1.60\t0\t2.00\tCOD\t42.0\t42.0\t0\t50\t一级A\t1.20\t0\t5000.00\t0.00\t按月结算，抄表日期 2026-05-18',
  '城东厂1#计量点\tJD-01\t2026-06\t2026-06-15\t30100\t28700\t1400\t30100\t1.20\t36120.00\t30100\t1.20\t0\t1.60\t0\t2.00\tCOD\t46.5\t46.5\t0\t50\t一级A\t1.20\t0\t5000.00\t0.00\t按月结算，抄表日期 2026-06-15',
  '城北园区2#计量点\tJD-02\t2026-05\t2026-05-20\t45800\t43600\t2200\t45800\t1.00\t45800.00\t45800\t1.00\t0\t1.60\t0\t2.00\t氨氮\t5.6\t5.6\t5\t8\t一级B\t1.00\t0\t5000.00\t0.00\t按月结算，抄表日期 2026-05-20',
  '城北园区2#计量点\tJD-02\t2026-06\t2026-06-21\t44200\t42100\t2100\t44200\t1.20\t53040.00\t44200\t1.20\t0\t1.60\t0\t2.00\tCOD\t44.8\t44.8\t0\t50\t一级A\t1.20\t0\t5000.00\t0.00\t按月结算，抄表日期 2026-06-21',
].join('\n');

const TOL = 0.01;

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = ['meterNo', 'period', 'inflow', 'outflow', 'settled', 'price', 'fee',
  'qualityItem', 'qualityValue', 'tierBand', 'penaltyStd', 'penaltyAmt'];

// 单元格级必需字段（空白 / 占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['meterNo', '计量点编号'],
  ['period', '结算期间'],
  ['inflow', '进水水量'],
  ['outflow', '出水水量'],
  ['settled', '结算水量'],
  ['price', '单价'],
  ['fee', '服务费'],
  ['qualityItem', '水质指标'],
  ['qualityValue', '指标值'],
  ['tierBand', '档位'],
];

// 数值列（用于「无法解析 / 为负」判定；空白跳过，不当成 0）
const NUMBER_FIELDS = [
  ['inflow', '进水水量'],
  ['outflow', '出水水量'],
  ['lossAllow', '允许损耗'],
  ['settled', '结算水量'],
  ['price', '单价'],
  ['fee', '服务费'],
  ['qualityValue', '指标值'],
  ['onlineValue', '在线监测值'],
  ['penaltyStd', '扣款标准'],
  ['penaltyAmt', '扣款额'],
];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词会抢走更具体的列（本仓库已在 tools/header_map_check.py 里钉成机械判据）。
const ROLES = {
  period: ['结算期间', '账单期间', '所属期间', '账期', '期间', '月份'],
  occurDate: ['水量发生日期', '发生日期', '计量日期', '抄表日期', '日期'],
  meterName: ['计量点名称', '排口名称', '厂站名称'],
  meterNo: ['计量点编号', '计量点代码', '计量点', '排口编号', '排口'],
  inflow: ['进水水量', '进水量', '进口水量'],
  outflow: ['出水水量', '出水量', '出口水量', '排放水量'],
  lossAllow: ['允许损耗水量', '允许损耗', '合理损耗', '损耗阈值'],
  settled: ['结算水量', '计费水量', '核算水量'],
  tierQty1: ['第一档水量', '档1水量', '一档水量'],
  tierPrice1: ['第一档单价', '档1单价', '一档单价'],
  tierQty2: ['第二档水量', '档2水量', '二档水量'],
  tierPrice2: ['第二档单价', '档2单价', '二档单价'],
  tierQty3: ['第三档水量', '档3水量', '三档水量'],
  tierPrice3: ['第三档单价', '档3单价', '三档单价'],
  bandLow: ['档位下限', '档位低限', '下限'],
  bandHigh: ['档位上限', '档位高限', '上限'],
  bandPrice: ['档位单价', '档位价', '标准单价'],
  tierBand: ['档位', '水质档位', '执行档位'],
  price: ['综合单价', '结算单价', '处理单价', '单价'],
  fee: ['服务费', '污水处理费', '处理费', '应收金额'],
  qualityItem: ['水质指标', '指标名称', '监测指标', '污染物指标'],
  onlineValue: ['在线监测值', '在线监测', '在线值'],
  qualityValue: ['指标值', '指标数值', '上报值'],
  exceedQty: ['超标项数', '超标次数', '超标项', '超标水量'],
  penaltyStd: ['扣款标准', '扣款单价', '罚款标准'],
  penaltyAmt: ['扣款额', '扣款金额', '超标扣款'],
  note: ['备注', '说明', '附注'],
};

const LABELS = {
  period: '结算期间',
  occurDate: '水量发生日期',
  meterName: '计量点名称',
  meterNo: '计量点编号',
  inflow: '进水水量',
  outflow: '出水水量',
  lossAllow: '允许损耗',
  settled: '结算水量',
  tierQty1: '第一档水量',
  tierPrice1: '第一档单价',
  tierQty2: '第二档水量',
  tierPrice2: '第二档单价',
  tierQty3: '第三档水量',
  tierPrice3: '第三档单价',
  price: '单价',
  fee: '服务费',
  qualityItem: '水质指标',
  onlineValue: '在线监测值',
  qualityValue: '指标值',
  bandLow: '档位下限',
  bandHigh: '档位上限',
  bandPrice: '档位单价',
  tierBand: '档位',
  exceedQty: '超标项数',
  penaltyStd: '扣款标准',
  penaltyAmt: '扣款额',
  note: '备注',
};

const SUM_ROLES = ['inflow', 'outflow', 'lossAllow', 'settled', 'fee', 'penaltyAmt'];

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

function num(it, role) {
  const n = normNumber(it[role]);
  return n === null ? 0 : n;
}

function money(n) {
  const v = Math.abs(n) < 0.005 ? 0 : n;
  return v.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/** 水量：与金额同样按两位小数展示，单位 m³ —— 让原文数字能被第三方照着复算 */
const qty = (n) => `${money(n)} m³`;

const num2 = (n) => (n === null || n === undefined ? '(未填)' : String(round2(n)));

const pointOf = (it) => String(it.meterNo == null ? '' : it.meterNo).trim()
  || String(it.meterName == null ? '' : it.meterName).trim() || '未命名计量点';

const periodLabel = (it) => String(it.period == null ? '' : it.period).trim() || '(未填期间)';

function who(it) {
  const name = String(it.meterName == null ? '' : it.meterName).trim();
  const no = String(it.meterNo == null ? '' : it.meterNo).trim();
  return `第 ${it.line} 行「${name || no || '未命名计量点'} ${periodLabel(it)}」`;
}

function finding(level, category, it, diff, message, advice) {
  const f = {
    level,
    category,
    line: it.line,
    evidence: String(it.raw == null ? '' : it.raw),
    message,
  };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

/* ============================ 本包检查（六项） ============================ */

/** 1. 处理水量勾稽：结算水量 = 出水水量 + 允许损耗（逐行复算，差额不为零即列出） */
function checkWaterBalance(items) {
  const out = [];
  for (const it of items) {
    const s = normNumber(it.settled);
    const o = normNumber(it.outflow);
    if (s === null || o === null) continue;          // 缺失 / 解析不了交给「关键字段」那一项
    const l = normNumber(it.lossAllow);
    const allow = l === null ? 0 : l;
    const expect = round2(o + allow);
    const diff = round2(s - expect);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding(diff > 0 ? 'P0' : 'P1', '结算水量勾稽不符', it, diff,
      `${who(it)}：结算水量 ${qty(s)} ≠ 出水水量 ${qty(o)} + 允许损耗 ${qty(allow)} = ${qty(expect)}，差额 ${qty(diff)}。`,
      '逐行拿抄表记录核：先看出水量与允许损耗两列的抄表日期是否同一天，再确认扣减水量有没有漏登。'
      + '按进水量结算的合同就用「出水水量 + 允许损耗」做复核。本工具只列出差额，不认定是哪种原因。'));
  }
  return out;
}

/** 2. 服务费金额勾稽：结算水量 × 单价 = 服务费（逐行复算） */
function checkFeeAmount(items) {
  const out = [];
  for (const it of items) {
    const s = normNumber(it.settled);
    const p = normNumber(it.price);
    const f = normNumber(it.fee);
    if (s === null || p === null || f === null) continue;
    const expect = round2(s * p);
    const diff = round2(f - expect);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding(diff < 0 ? 'P0' : 'P1', '服务费金额勾稽不符', it, diff,
      `${who(it)}：结算水量 ${qty(s)} × 单价 ${p.toFixed(2)} 元/m³ = ${money(expect)} 元，`
      + `但服务费写的是 ${money(f)} 元，差额 ${money(diff)} 元（${diff < 0 ? '少收' : '多收'}）。`,
      '先确认单价有没有用错档位（见「水质档位与单价」那一条），再确认服务费里是不是把扣款、上期调整或分成并进来了 —— '
      + '本工具只按你给的这两列复算。'));
  }
  return out;
}

/** 3. 水质档位与单价一致性：按指标值查档，档位与所用单价不符即报 */
function checkQualityBand(items) {
  const out = [];
  const catalog = new Map();     // `指标|档位` -> {low, high, price, line}
  for (const it of items) {
    const name = String(it.tierBand == null ? '' : it.tierBand).trim();
    const item = String(it.qualityItem == null ? '' : it.qualityItem).trim();
    const low = normNumber(it.bandLow);
    const high = normNumber(it.bandHigh);
    const bandPrice = normNumber(it.bandPrice);
    const value = normNumber(it.qualityValue);

    // (3a) 指标值必须落在本行所填档位的区间内
    if (value !== null && low !== null && high !== null && (value < low - TOL || value > high + TOL)) {
      out.push(finding('P1', '水质档位与单价不一致', it, undefined,
        `${who(it)}：${item || '水质指标'} 的指标值 ${num2(value)} 不在所填档位「${name || '(未填)'}」的区间 `
        + `[${num2(low)}, ${num2(high)}] 内 —— 档位与指标值不符。`,
        '按合同附件的水质档位表重新查档：指标值落在哪一档就用哪一档的单价，不要沿用上月档位。'));
    }

    // (3b) 同一指标同一档位名，跨行的上下限与档位单价必须一致
    if (name) {
      const key = `${item}|${name}`;
      const prev = catalog.get(key);
      if (!prev) {
        catalog.set(key, { low, high, price: bandPrice, line: it.line });
      } else {
        const bad = (low !== null && prev.low !== null && Math.abs(low - prev.low) >= TOL)
          || (high !== null && prev.high !== null && Math.abs(high - prev.high) >= TOL)
          || (bandPrice !== null && prev.price !== null && Math.abs(bandPrice - prev.price) >= TOL);
        if (bad) {
          out.push(finding('P1', '水质档位与单价不一致', it, undefined,
            `${who(it)}：档位「${name}」（${item || '水质指标'}）在第 ${prev.line} 行对应 `
            + `[${num2(prev.low)}, ${num2(prev.high)}]、档位单价 ${num2(prev.price)}，本行却写成 `
            + `[${num2(low)}, ${num2(high)}]、档位单价 ${num2(bandPrice)} —— 同一档位的上下限或单价不一致。`,
            '同一档位在所有行必须对应同一组上下限与同一个档位单价；先确认是不是把两个计量点或两份合同的档位表混在一张表里了。'));
        }
      }
    }

    // (3c) 单一价行：所用单价必须等于该档位的档位单价（累进计价行由订阅版的逐段复算负责）
    const applied = normNumber(it.price);
    const q2 = normNumber(it.tierQty2);
    const q3 = normNumber(it.tierQty3);
    const flat = (q2 === null || Math.abs(q2) < TOL) && (q3 === null || Math.abs(q3) < TOL);
    if (flat && applied !== null && bandPrice !== null && Math.abs(applied - bandPrice) >= TOL) {
      out.push(finding('P1', '水质档位与单价不一致', it, round2(applied - bandPrice),
        `${who(it)}：本行按单一价结算，所用单价 ${applied.toFixed(2)} 元/m³，`
        + `但档位「${name || '(未填)'}」的档位单价是 ${bandPrice.toFixed(2)} 元/m³，`
        + `差 ${money(round2(applied - bandPrice))} 元/m³ —— 档位与所用单价不符。`,
        '档位决定了适用单价：先确认指标值对应的档位，再把单价换成该档位的合同单价；改完服务费要按新单价重算。'));
    }
  }
  return out;
}

/** 4. 超标扣款计算核对：超标项数 × 扣款标准 = 扣款额 */
function checkPenalty(items) {
  const out = [];
  for (const it of items) {
    const q = normNumber(it.exceedQty);
    const std = normNumber(it.penaltyStd);
    const amtRaw = normNumber(it.penaltyAmt);
    const amt = amtRaw === null ? 0 : amtRaw;
    const qNum = q === null ? 0 : q;

    // 有超标项却没有标准 ⇒ 疑似漏算（这一条直接是钱）
    if (q !== null && q > TOL && (std === null || std <= TOL)) {
      out.push(finding('P0', '超标扣款计算不符', it, undefined,
        `${who(it)}：本行有 ${num2(q)} 项超标，却没有填扣款标准（或标准为 0），扣款额是 ${num2(amtRaw)} —— 疑似漏算扣款。`,
        '超标必须按合同附件的水质扣款标准逐项计扣；先把扣款标准补上再重跑，让扣款额能被复算出来。'));
      continue;
    }
    // 有扣款额、但既没有超标项数也没有标准 ⇒ 无法复算
    if (std === null && q === null && Math.abs(amt) >= TOL) {
      out.push(finding('P1', '超标扣款计算不符', it, undefined,
        `${who(it)}：本行扣款额写了 ${money(amt)} 元，但没有超标项数也没有扣款标准 —— 这笔扣款无法复算。`,
        '扣款额必须能被「超标项数 × 扣款标准」复算出来：把这两列补上，或者在备注里写明这笔扣款的计算口径。'));
      continue;
    }
    if (std === null) continue;
    const expect = round2(qNum * std);
    const diff = round2(amt - expect);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding('P1', '超标扣款计算不符', it, diff,
      `${who(it)}：超标项数 ${num2(qNum)} × 扣款标准 ${money(std)} 元 = ${money(expect)} 元，`
      + `但扣款额写的是 ${money(amt)} 元，差额 ${money(diff)} 元。`,
      '按合同的分项扣款标准逐项复算（超标项数 × 标准）：漏算就补扣、算错就改数。'
      + '本工具只复算这一行的算术，不判断超标事实本身是否成立。'));
  }
  return out;
}

/** 5. 同一计量点同一期间重复结算（计量点编号 或 计量点名称 + 结算期间） */
function checkDuplicateSettlement(items) {
  const out = [];
  const reported = new Set();
  const byNo = new Map();
  const byName = new Map();
  for (const it of items) {
    const no = String(it.meterNo == null ? '' : it.meterNo).trim();
    const name = String(it.meterName == null ? '' : it.meterName).trim();
    const pd = String(it.period == null ? '' : it.period).trim();
    if (!pd) continue;

    const noKey = `${no}|${pd}`;
    if (no && byNo.has(noKey) && !reported.has(it.line)) {
      reported.add(it.line);
      out.push(finding('P0', '同一计量点同一期间重复结算', it, undefined,
        `${who(it)}：计量点编号「${no}」在结算期间 ${pd} 里第 ${byNo.get(noKey)} 行已经结算过一次 —— `
        + '同一计量点同一期间重复结算。',
        '一个计量点在一个结算期间里只应有一条结算记录：分次抄表请用「本期水量 / 累计水量」两列，不要新增行，否则会重复计费。'));
    }
    if (no && !byNo.has(noKey)) byNo.set(noKey, it.line);

    const nameKey = `${name}|${pd}`;
    if (name && byName.has(nameKey) && !reported.has(it.line)) {
      reported.add(it.line);
      out.push(finding('P0', '同一计量点同一期间重复结算', it, undefined,
        `${who(it)}：计量点「${name}」在结算期间 ${pd} 里第 ${byName.get(nameKey)} 行已经结算过一次 —— `
        + '同一计量点同一期间重复结算。',
        '先确认是不是两个计量点用了同一个名称，或者把同一笔结算抄了两遍；确认后删掉重复的那一行。'));
    }
    if (name && !byName.has(nameKey)) byName.set(nameKey, it.line);
  }
  return out;
}

/** 6. 空白 / 占位符 / 认不出格式（关键字段缺失、数值无法解析、数值为负） */
function checkFieldIntegrity(items) {
  const out = [];
  for (const it of items) {
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        `${who(it)}：这些关键字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的字段会让对应的核对整项做不了；补全后重跑。本工具不会替你猜一个默认值。'));
    }
    for (const [role, label] of NUMBER_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        out.push(finding('P1', '数值无法解析', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的数值（只认数字、千分位、¥、括号负数）。`,
          '把这一格改成纯数字形态（如 32600 或 1.20）再跑；本工具不会把看不懂的值当成 0。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '数值为负', it, n,
          `${who(it)}：「${label}」是负数（${num2(n)}）—— 水量、单价、服务费、扣款这些列出现负数，`
          + '通常是填反了方向或者写成了红字冲销。',
          '确认是红字冲销还是填错了方向；确属冲销的请写在「备注」里并保留原值，不要直接改成正数。'));
      }
    }
  }
  return out;
}

/* ===== 以下检查只有订阅版才执行 ===== */

/** 付费：期间归一化 —— 2026-05 / 2026年5月 / 202605 → 2026-05；认不出返回 null */
function normPeriod(raw) {
  const s = String(raw == null ? '' : raw).trim();
  if (!s) return null;
  let m = /^(\d{4})\s*[-/.年]\s*(\d{1,2})\s*月?$/.exec(s);
  if (m) return `${m[1]}-${String(Number(m[2])).padStart(2, '0')}`;
  m = /^(\d{4})(\d{2})$/.exec(s);
  if (m) return `${m[1]}-${m[2]}`;
  return null;
}

/** 付费：日期归一化到所属期间 —— 2026-05-18 / 2026年5月18日 / 20260518 → 2026-05；认不出返回 null */
function periodOfDate(raw) {
  const s = String(raw == null ? '' : raw).trim();
  if (!s) return null;
  let m = /^(\d{4})\s*[-/.年]\s*(\d{1,2})\s*[-/.月]\s*(\d{1,2})\s*日?$/.exec(s);
  if (m) return `${m[1]}-${String(Number(m[2])).padStart(2, '0')}`;
  m = /^(\d{4})(\d{2})(\d{2})$/.exec(s);
  if (m) return `${m[1]}-${m[2]}`;
  return normPeriod(s);
}

/** 付费：把逐段复算写成一行可复算的算式 */
function segments(q, p) {
  return `${qty(q[0])}×${p[0].toFixed(2)} + ${qty(q[1])}×${p[1].toFixed(2)} + ${qty(q[2])}×${p[2].toFixed(2)}`;
}

/** 付费：阶梯 / 累进单价逐段复算（各档水量 × 各档单价 之和 = 应收服务费） */
function checkTierSegments(it) {
  const out = [];
  const q = [normNumber(it.tierQty1), normNumber(it.tierQty2), normNumber(it.tierQty3)]
    .map((n) => (n === null ? 0 : n));
  const p = [normNumber(it.tierPrice1), normNumber(it.tierPrice2), normNumber(it.tierPrice3)]
    .map((n) => (n === null ? 0 : n));
  const settled = normNumber(it.settled);
  const fee = normNumber(it.fee);
  const qtySum = round2(q[0] + q[1] + q[2]);
  const amtSum = round2(q[0] * p[0] + q[1] * p[1] + q[2] * p[2]);

  if (qtySum <= TOL && amtSum <= TOL) {
    if (fee !== null && fee > TOL) {
      out.push(finding('P2', '阶梯单价逐段复算不符', it, undefined,
        `${who(it)}：本行没有分档水量与分档单价明细，服务费 ${money(fee)} 元无法逐段复算 —— `
        + '累进计价合同必须给出各档水量与各档单价。',
        '按合同的分档计价表把「第一/二/三档水量」与「各档单价」补上，本工具会逐段复算到分。'));
    }
    return out;
  }
  if (settled !== null && Math.abs(qtySum - settled) >= TOL) {
    out.push(finding('P1', '阶梯单价逐段复算不符', it, round2(qtySum - settled),
      `${who(it)}：各档水量合计 ${qty(qtySum)} ≠ 结算水量 ${qty(settled)}，差 ${qty(round2(qtySum - settled))} —— 分档没把结算水量分完。`,
      '各档水量必须刚好把结算水量分完：先看是不是漏填了某一档的水量，或者把「本档水量」填成了「累计到本档的水量」。'));
  }
  if (fee !== null && Math.abs(amtSum - fee) >= TOL) {
    out.push(finding('P0', '阶梯单价逐段复算不符', it, round2(amtSum - fee),
      `${who(it)}：逐段复算 ${segments(q, p)} = ${money(amtSum)} 元，但服务费写的是 ${money(fee)} 元，`
      + `差 ${money(round2(amtSum - fee))} 元 —— 累进计价没有按档切开。`,
      '按合同的分档单价逐段重算（各档水量 × 各档单价再求和）：跨档的水量必须按档切开，不能用综合单价一把算。'));
  }
  return out;
}

/** 付费：进水与出水水量差额超过合理损耗阈值（点名到计量点与期间） */
function checkLossThreshold(it) {
  const out = [];
  const i = normNumber(it.inflow);
  const o = normNumber(it.outflow);
  if (i === null || o === null) return out;
  const allowRaw = normNumber(it.lossAllow);
  const allow = allowRaw === null ? 0 : allowRaw;
  const lost = round2(i - o);
  if (lost <= allow + TOL) return out;
  const over = round2(lost - allow);
  out.push(finding('P1', '进水出水差额超允许损耗', it, over,
    `${who(it)}：进水水量 ${qty(i)} − 出水水量 ${qty(o)} = ${qty(lost)}，超过允许损耗 ${qty(allow)}，`
    + `超出 ${qty(over)} —— 计量点「${pointOf(it)}」、期间「${periodLabel(it)}」的水量差额需要解释。`,
    '管网破损、雨污混接、偷排、计量表失准都会造成这个差额：先核对两个计量表的表号与抄表日期，再让运维出具差额说明；'
    + '差额水量要不要计费按合同口径定，本工具只按你给的阈值把差额点出来。'));
  return out;
}

/** 付费：在线监测数据与上报数据的一致性（同一行两处数值不一致） */
function checkOnlineVsReported(it) {
  const out = [];
  const v = normNumber(it.qualityValue);
  const on = normNumber(it.onlineValue);
  if (v === null || on === null) return out;
  const diff = round2(v - on);
  if (Math.abs(diff) < TOL) return out;
  const item = String(it.qualityItem == null ? '' : it.qualityItem).trim() || '水质指标';
  out.push(finding('P1', '在线监测与上报数据不一致', it, undefined,
    `${who(it)}：${item} 的上报指标值 ${num2(v)} 与在线监测值 ${num2(on)} 不一致（差 ${num2(diff)}）。`,
    '把在线监测平台的原始小时均值调出来对一遍：同一天同一指标只能有一个数，两处不一致要先定哪一个作准，再改台账。'));
  return out;
}

/** 付费：同一计量点 + 同一指标 + 同一天，上报了不同的值 */
function checkSameDayReport(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const v = normNumber(it.qualityValue);
    const point = String(it.meterNo == null ? '' : it.meterNo).trim()
      || String(it.meterName == null ? '' : it.meterName).trim();
    const item = String(it.qualityItem == null ? '' : it.qualityItem).trim();
    const date = String(it.occurDate == null ? '' : it.occurDate).trim();
    if (v === null || !point || !item || !date) continue;
    const key = `${point}|${item}|${date}`;
    const prev = seen.get(key);
    if (!prev) {
      seen.set(key, { value: v, line: it.line });
      continue;
    }
    if (Math.abs(prev.value - v) < TOL) continue;
    out.push(finding('P1', '同一指标同一天上报值不一致', it, undefined,
      `${who(it)}：计量点「${point}」在 ${date} 的 ${item} 上报了两次、数值还不同 —— `
      + `第 ${prev.line} 行是 ${num2(prev.value)}，本行是 ${num2(v)}。`,
      '同一天同一计量点同一指标只能有一条上报值：先确认哪一条是在线平台的原始值、哪一条被人工改过，删掉不对的那条。'));
  }
  return out;
}

/** 付费：跨期归属（结算期间与水量发生日期不属于同一期） */
function checkCrossPeriod(it) {
  const out = [];
  const p = normPeriod(it.period);
  const d = periodOfDate(it.occurDate);
  if (!p || !d || p === d) return out;
  out.push(finding('P2', '跨期归属', it, undefined,
    `${who(it)}：结算期间「${String(it.period == null ? '' : it.period).trim()}」与水量发生日期 `
    + `「${String(it.occurDate == null ? '' : it.occurDate).trim()}」不属于同一期（日期属于 ${d}，结算期间是 ${p}）—— `
    + '水量被记到了别的期间。',
    '按水量实际发生的月份改结算期间，或者台账里补一列「归属期间」；跨期水量要单独挂账，否则相邻两个月的服务费都会对不上。'));
  return out;
}

function emptyBucket() {
  return { rows: 0, inflow: 0, outflow: 0, settled: 0, fee: 0, penalty: 0, issues: 0, diff_amount: 0 };
}

function addItemToBucket(b, it) {
  b.rows += 1;
  b.inflow = round2(b.inflow + num(it, 'inflow'));
  b.outflow = round2(b.outflow + num(it, 'outflow'));
  b.settled = round2(b.settled + num(it, 'settled'));
  b.fee = round2(b.fee + num(it, 'fee'));
  b.penalty = round2(b.penalty + num(it, 'penaltyAmt'));
  return b;
}

function mergeBucket(acc, b) {
  acc.rows += b.rows;
  acc.inflow = round2(acc.inflow + b.inflow);
  acc.outflow = round2(acc.outflow + b.outflow);
  acc.settled = round2(acc.settled + b.settled);
  acc.fee = round2(acc.fee + b.fee);
  acc.penalty = round2(acc.penalty + b.penalty);
  acc.issues += b.issues;
  acc.diff_amount = round2(acc.diff_amount + b.diff_amount);
  return acc;
}

function groupBuckets(pairs, keyName, keyOf) {
  const map = new Map();
  for (const p of pairs) {
    const k = keyOf(p);
    if (!map.has(k)) map.set(k, Object.assign({ [keyName]: k }, emptyBucket()));
    mergeBucket(map.get(k), p);
  }
  return [...map.values()].sort((a, b) => (b.diff_amount - a.diff_amount)
    || String(a[keyName]).localeCompare(String(b[keyName])));
}

/** 付费：分计量点×分期间的汇总清单（按差额金额从大到小） */
function buildRollup(items, findings) {
  const pairs = new Map();
  const linePair = new Map();
  for (const it of items) {
    const key = `${pointOf(it)}|${periodLabel(it)}`;
    if (!pairs.has(key)) {
      pairs.set(key, Object.assign({ key, meter_point: pointOf(it), period: periodLabel(it) }, emptyBucket()));
    }
    addItemToBucket(pairs.get(key), it);
    linePair.set(it.line, key);
  }
  for (const f of findings) {
    const key = linePair.get(f.line);
    if (!key || !pairs.has(key)) continue;
    const b = pairs.get(key);
    b.issues += 1;
    b.diff_amount = round2(b.diff_amount + Math.abs(typeof f.diff === 'number' ? f.diff : 0));
  }
  const list = [...pairs.values()].sort((a, b) => (b.diff_amount - a.diff_amount)
    || String(a.key).localeCompare(String(b.key)));
  const total = list.reduce((acc, p) => mergeBucket(acc, p), emptyBucket());
  return {
    by_meter_point: groupBuckets(list, 'meter_point', (p) => p.meter_point),
    by_period: groupBuckets(list, 'period', (p) => p.period),
    by_meter_period: list,
    total,
  };
}

/** 付费：汇总整改清单（按差额金额从大到小，每条给出可整改动作） */
function buildActions(findings, items) {
  const lineBucket = new Map();
  const linePoint = new Map();
  for (const it of items) {
    lineBucket.set(it.line, `${pointOf(it)}|${periodLabel(it)}`);
    linePoint.set(it.line, { meter_point: pointOf(it), period: periodLabel(it) });
  }
  return findings
    .slice()
    .sort((a, b) => (Math.abs(b.diff || 0) - Math.abs(a.diff || 0)) || (a.line - b.line)
      || String(a.category).localeCompare(String(b.category)))
    .map((f, i) => {
      const at = linePoint.get(f.line) || { meter_point: '', period: '' };
      return {
        seq: i + 1,
        level: f.level,
        line: f.line,
        bucket: lineBucket.get(f.line) || `${at.meter_point}|${at.period}`,
        meter_point: at.meter_point,
        period: at.period,
        category: f.category,
        diff: typeof f.diff === 'number' ? f.diff : 0,
        abs_diff: round2(Math.abs(typeof f.diff === 'number' ? f.diff : 0)),
        action: f.advice || '按上面列出的差额逐条核对原始抄表记录与结算单。',
      };
    });
}

/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的污水处理费结算与水质数据核对表']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的污水处理费结算与水质数据核对表']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的污水处理费结算与水质数据核对表（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行结算明细（现在只有表头，没有可核对的明细行）']);
  }

  const paid = Boolean(p.full || p.credit || p.token);
  const findings = [];
  const notRun = [];

  for (const f of (checkWaterBalance(t.items) || [])) findings.push(f);
  for (const f of (checkFeeAmount(t.items) || [])) findings.push(f);
  for (const f of (checkQualityBand(t.items) || [])) findings.push(f);
  for (const f of (checkPenalty(t.items) || [])) findings.push(f);
  for (const f of (checkDuplicateSettlement(t.items) || [])) findings.push(f);
  for (const f of (checkFieldIntegrity(t.items) || [])) findings.push(f);

  if (paid) {
    for (const it of t.items) {
      for (const f of (checkTierSegments(it) || [])) findings.push(f);
      for (const f of (checkLossThreshold(it) || [])) findings.push(f);
      for (const f of (checkOnlineVsReported(it) || [])) findings.push(f);
      for (const f of (checkCrossPeriod(it) || [])) findings.push(f);
    }
    for (const f of (checkSameDayReport(t.items) || [])) findings.push(f);
  } else {
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  }

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const inflowTotal = t.totals.inflow;
  const outflowTotal = t.totals.outflow;
  const lossTotal = t.totals.lossAllow;
  const settledTotal = t.totals.settled;
  const feeTotal = t.totals.fee;
  const penaltyTotal = t.totals.penaltyAmt;
  const measuredLoss = round2(inflowTotal - outflowTotal);
  const lossRate = inflowTotal > 0 ? round2((measuredLoss / inflowTotal) * 100) : null;

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      inflow_total: inflowTotal,
      outflow_total: outflowTotal,
      measured_loss: measuredLoss,
      allowed_loss_total: lossTotal,
      loss_rate_pct: lossRate,
      settled_total: settledTotal,
      fee_total: feeTotal,
      penalty_total: penaltyTotal,
      payable_total: round2(feeTotal - penaltyTotal),
      basis: '结算水量应等于 出水水量 + 允许损耗（差额逐行列出）；服务费应等于 结算水量 × 单价；'
        + '水质指标值须落在所填档位的上下限内，同一指标同一档位的上下限与档位单价跨行必须一致，单一价行的所用单价须等于档位单价；'
        + '扣款额应等于 超标项数 × 扣款标准；同一计量点同一结算期间只应有一条结算记录。'
        + '完整档另按 各档水量 × 各档单价 逐段复算服务费，并把 进水−出水 超允许损耗、在线与上报不一致、跨期归属逐条点名。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的口径算得对**，'
      + '不代表水质达标、超标事实不成立、在线监测设备已校准，也不代表单价与扣款标准本身合规 —— 那些不在本工具范围内。';
  }

  const scope = {
    checks: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.items.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    inflow_total: inflowTotal,
    outflow_total: outflowTotal,
    measured_loss: measuredLoss,
    settled_total: settledTotal,
    fee_total: feeTotal,
    penalty_total: penaltyTotal,
    payable_total: round2(feeTotal - penaltyTotal),
  };
  result.scope = scope;

  if (paid) {
    result.rollup = buildRollup(t.items, findings);
    result.actions = buildActions(findings, t.items);
    result.consolidated_actions = result.actions;
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
  CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
