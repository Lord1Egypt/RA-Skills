#!/usr/bin/env node
/**
 * housing-fund-check-full.js —— 住房公积金汇缴与基数核对引擎（订阅版 / 本包共用源码）。
 *
 * 真实痛点：**每家公司每月发薪与汇缴时都必须核一遍住房公积金汇缴明细表**，
 * 而这张表是三条串行算式加一堆口径约束：
 *   ① 单位月缴存额 = 缴存基数 × 单位比例
 *   ② 个人月缴存额 = 缴存基数 × 个人比例
 *   ③ 缴存合计     = 单位月缴存额 + 个人月缴存额
 * 再加上：基数要落在当地上下限内、比例要取允许的整数档、新增/离职人员的缴存月份要对应、
 * 有断缴的月份影响连续性、表内的公积金口径还要与工资表应缴口径一致。
 * 基数用错、比例不合法、离职人员多缴漏缴、单位与个人合计对不上，
 * 都是**每个月都在发生的钱与合规风险**；纯算术，但人一多、月份一多，人眼极易错。
 *
 * 与已有能力的区别：`social-insurance-check` 核的是**社保**申报明细（养老/医疗/失业/工伤/生育
 * 各自的单位与个人部分）。社保与公积金是**两套独立系统**：基数上下限各自定、比例各自定、
 * 汇缴渠道也不同。本能力**只核住房公积金**，不看社保任何一个险种。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查政策文库、不调用大模型；**不给法律/合规意见**；
 * 材料不足时不给结论（绝不输出"未发现问题"）。
 *
 * ⚠️ 本文件的结构**有硬约束**（tools/strip_free_engine.py 依赖它）：
 *    下面那行「订阅版才执行的检查」MARKER 之前只放**共享件**（常量、解析、归一化、本包检查）；
 *    付费实现全部放在 MARKER 与 `function run(` 之间。
 *    共享件若被放进付费区，剥离器会先删掉它们，再连锁删掉所有引用它们的函数（实测踩过）。
 */
'use strict';

const CHECKS_GIVEN = [
  '单位月缴存额复算（缴存基数 × 单位缴存比例）',
  '个人月缴存额复算（缴存基数 × 个人缴存比例）',
  '缴存合计复算（单位月缴存额 + 个人月缴存额）',
  '合计行勾稽（合计行逐列与各明细行之和不符）',
  '同一期间重复人员检测',
  '关键字段空缺与负数检测',
  '缴存基数超出表内上下限（超上限见完整档的处理清单）',
];

const CHECKS_WITHHELD = [
  '缴存基数低于表内下限检测（并给出应调整基数与月差额）',
  '缴存比例不在允许的整数档（给出最接近的合法档）',
  '新增 / 离职人员的缴存月份与在职区间不符（应缴未缴或多缴）',
  '同一职工在缴存区间内出现断缴月份（影响连续性）',
  '单位与个人缴存比例不一致检测',
  '与工资表应缴口径差异（工资个人缴存 vs 公积金个人缴存额）',
  '按金额排序的补退处理清单（每条带原文行号与建议动作）',
];

const OUT_OF_SCOPE = [
  '给出法律或合规意见（本工具只核表内可算的算术关系与表内给定的上下限、比例）',
  '核对社保（养老 / 医疗 / 失业 / 工伤 / 生育）任何一个险种 —— 社保与公积金是两套独立系统',
  '判断当地当年真实的基数上下限与比例是否用对（请把当地公布的上下限与允许比例填进表内）',
  '判断职工身份、户籍、人才引进等是否适用某个缴存口径',
  '计算滞纳金、利息、罚款；也不做跨年度的基数调整追溯',
  '读取 .xlsx（请先从系统导出、连同表头复制成文本贴进来，Tab 分隔最稳）',
];

/* 样例：一家 7 人公司某一期的公积金汇缴明细（表头 + 明细行 + 合计行），**口径完全自洽**：
   每行的单位/个人缴存额都等于基数×比例、合计等于两者之和；
   基数全在表内上下限 [2420.00, 35283.00] 之内；
   比例取允许档 {5,6,7,8,9,10,11,12}；新增人员的入职月份、离职人员的离职月份都合法；
   工资表口径与公积金口径一致。**因此它跑出来 0 条发现**（干净样例不误报是硬要求）。 */
const SAMPLE_TEXT = [
  '期间\t姓名\t证件号\t缴存基数\t单位比例\t个人比例\t单位月缴存额\t个人月缴存额\t缴存合计\t基数下限\t基数上限\t比例档位\t新增月份\t离职月份\t工资单位缴存额\t工资个人缴存额\t职工状态\t备注',
  '2026-03\t张伟\t110101********1234\t8000.00\t12%\t12%\t960.00\t960.00\t1920.00\t2420.00\t35283.00\t12%\t\t\t960.00\t960.00\t在职\t',
  '2026-03\t李娜\t110101********2345\t12000.00\t12%\t12%\t1440.00\t1440.00\t2880.00\t2420.00\t35283.00\t12%\t\t\t1440.00\t1440.00\t在职\t',
  '2026-03\t王强\t110101********3456\t6000.00\t9%\t9%\t540.00\t540.00\t1080.00\t2420.00\t35283.00\t9%\t\t\t540.00\t540.00\t在职\t',
  '2026-03\t赵敏\t110101********4567\t20000.00\t12%\t12%\t2400.00\t2400.00\t4800.00\t2420.00\t35283.00\t12%\t\t\t2400.00\t2400.00\t在职\t',
  '2026-03\t陈静\t110101********5678\t5000.00\t8%\t8%\t400.00\t400.00\t800.00\t2420.00\t35283.00\t8%\t2026-03\t\t400.00\t400.00\t新增\t本月起缴',
  '2026-03\t刘洋\t110101********6789\t9000.00\t12%\t12%\t1080.00\t1080.00\t2160.00\t2420.00\t35283.00\t12%\t\t2026-03\t1080.00\t1080.00\t离职\t缴至本月',
  '2026-03\t孙磊\t110101********7890\t7000.00\t7%\t7%\t490.00\t490.00\t980.00\t2420.00\t35283.00\t7%\t\t\t490.00\t490.00\t在职\t',
  '合计\t\t\t\t\t\t7310.00\t7310.00\t14620.00\t\t\t\t\t\t7310.00\t7310.00\t\t',
].join('\n');

/* ============================== 共享件（本包也要用） ============================== */

const TOL = 0.01;              // 金额容差（分）
const PCT_TOL = 0.02;          // 比例百分数容差（比例保留两位小数）
const AMOUNT_CENTS = (n) => Math.round(n * 100);
const round2 = (n) => Math.round(n * 100) / 100;

/** 允许的公积金缴存比例整数档（元以下不取）。表内没给「比例档位」时不判这一项。 */
const ALLOWED_RATE_STEPS = [5, 6, 7, 8, 9, 10, 11, 12];

// ⚠️ 角色别名顺序 = 判据的一部分：更具体的词必须排在更宽泛的词前面
//    （本仓库踩过两次的坑，见 tools/header_map_check.py —— 顺序一错，
//     更宽泛的关键词会把更具体的那一列**静默抢走**，算错但不报错）。
//    实测必须这样排的四处：
//      · 「基数下限」「缴存基数下限」必须排在「缴存基数」之前（否则被 base 抢走）；
//      · 「新增月份」「离职月份」必须排在「月份」之前（否则被 period 抢走）；
//      · 「工资单位缴存额」必须排在「单位月缴存额」之前，「工资个人缴存额」同理；
//      · 「比例档位」必须排在「比例」之前（本引擎没有单列「比例」的别名，但顺序要防）。
const ROLES = {
  baseMin: ['基数下限', '缴存基数下限', '下限'],
  baseMax: ['基数上限', '缴存基数上限', '上限'],
  joinMonth: ['新增月份', '入职月份', '新增日期'],
  leaveMonth: ['离职月份', '减员月份', '离职日期'],
  wageUnit: ['工资单位缴存额', '工资表单位缴存', '工资单位部分'],
  wagePerson: ['工资个人缴存额', '工资表个人缴存', '工资个人部分'],
  rateStep: ['比例档位', '缴存比例档', '允许比例', '档位'],
  totalAmt: ['缴存合计', '月缴存合计', '合计缴存额'],
  unitAmt: ['单位月缴存额', '单位缴存额', '单位部分'],
  personAmt: ['个人月缴存额', '个人缴存额', '个人部分'],
  unitRate: ['单位比例', '单位缴存比例', '公司比例'],
  personRate: ['个人比例', '个人缴存比例', '职工比例'],
  base: ['缴存基数', '缴费基数', '基数'],
  period: ['期间', '所属期', '汇缴月份', '缴存月份', '月份'],
  name: ['姓名', '职工姓名', '员工姓名', '人员'],
  idno: ['证件号', '身份证号', '身份证', '证件号码'],
  status: ['职工状态', '在职状态', '状态'],
  note: ['备注', '说明'],
};

const LABELS = {
  period: '期间', name: '姓名', idno: '证件号', base: '缴存基数',
  unitRate: '单位比例', personRate: '个人比例', unitAmt: '单位月缴存额',
  personAmt: '个人月缴存额', totalAmt: '缴存合计', baseMin: '基数下限',
  baseMax: '基数上限', rateStep: '比例档位', joinMonth: '新增月份',
  leaveMonth: '离职月份', wageUnit: '工资单位缴存额', wagePerson: '工资个人缴存额',
  status: '职工状态', note: '备注',
};

const REQUIRED = ['period', 'name', 'base', 'unitRate', 'personRate', 'unitAmt', 'personAmt', 'totalAmt'];
/* 合计行要逐列复核的列：单位、个人、缴存合计三列。
   ⚠️ 工资口径两列**不进**这个清单 —— 它们是"每人各自的工资表口径数"，
   首行那两格不是公司合计，拿它跟各人之和比会整片误报（实测踩过）。 */
const SUM_ROLES = ['unitAmt', 'personAmt', 'totalAmt'];

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值、更不会输出"未发现问题"。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
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
  const n = Number(String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/%$/, ''));
  return Number.isFinite(n) ? n : null;
}

/** 期间归一：'2026-3' / '2026/3' / '2026年3月' -> '2026-03'；认不出返回 null */
function normMonth(raw) {
  if (isBlank(raw)) return null;
  const m = String(raw).trim().match(/^(\d{4})\s*[-/年.]\s*(\d{1,2})/);
  if (!m) return null;
  const mm = Number(m[2]);
  if (!(mm >= 1 && mm <= 12)) return null;
  return `${m[1]}-${String(mm).padStart(2, '0')}`;
}

/** 比例归一：'12%' -> 12；'0.12' -> 12；认不出返回 null */
function normRate(raw) {
  const n = normNumber(raw);
  if (n === null) return null;
  return n > 0 && n <= 1 && String(raw).indexOf('%') < 0 ? round2(n * 100) : n;
}

/** 月序号（用于比较先后）：'2026-03' -> 2026*12+2；认不出返回 null */
function monthIndex(mon) {
  if (!mon) return null;
  const [y, m] = String(mon).split('-').map(Number);
  if (!y || !m) return null;
  return y * 12 + (m - 1);
}

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { error: 'empty' };
  const cols = splitRow(raw[0]).map((h) => ({ header: h, role: roleOf(h) }));
  const have = new Set(cols.map((c) => c.role).filter(Boolean));
  const missingRoles = REQUIRED.filter((r) => !have.has(r));
  if (missingRoles.length) {
    return { error: 'no_header', missingRoles: missingRoles.map((r) => LABELS[r]) };
  }
  const items = [];
  const totals = [];
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i], byRole: {} };
    cols.forEach((c, idx) => {
      if (c.role && row.byRole[c.role] === undefined) {
        row.byRole[c.role] = cells[idx] === undefined ? '' : cells[idx];
      }
    });
    const marks = [row.byRole.name, row.byRole.period, cells[0]];
    if (marks.some((v) => /^(合计|总计|小计|total)/i.test(String(v || '').trim()))) {
      row.isTotal = true;
      totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals, missingColumns: [] };
}

const num = (it, role) => normNumber(it.byRole[role]);
const who = (it) => `第 ${it.line} 行「${String(it.byRole.name || '(未署名)').trim() || '(未署名)'}」`;
const tag = (it) => {
  const n = String(it.byRole.name || '').trim() || '(未署名)';
  const p = String(it.byRole.period || '').trim() || '(未填期间)';
  return `${p} ${n}`;
};
const keyOf = (it) => {
  const id = String(it.byRole.idno || '').trim();
  return id || String(it.byRole.name || '').trim();
};

/* ============================== 本包检查（7 项） ============================== */

function checkUnitAmount(it) {
  const base = num(it, 'base');
  const rate = normRate(it.byRole.unitRate);
  const stated = num(it, 'unitAmt');
  if (base === null || rate === null || stated === null) return null;
  const expect = round2(base * rate / 100);
  if (AMOUNT_CENTS(expect) === AMOUNT_CENTS(stated)) return null;
  return {
    level: 'P0', category: '单位月缴存额与复算不符', line: it.line,
    subject: tag(it), amount: round2(stated - expect), person: String(it.byRole.name || '').trim(),
    message: `${who(it)}的单位月缴存额是 ${stated.toFixed(2)}，`
      + `按 缴存基数 ${base.toFixed(2)} × 单位比例 ${rate}% = ${expect.toFixed(2)}，应为 ${expect.toFixed(2)}`
      + `（相差 ${round2(stated - expect).toFixed(2)}）。`,
    advice: '单位月缴存额只由「缴存基数 × 单位比例」决定；对不上说明基数、比例或金额三者之一填错了。',
  };
}

function checkPersonAmount(it) {
  const base = num(it, 'base');
  const rate = normRate(it.byRole.personRate);
  const stated = num(it, 'personAmt');
  if (base === null || rate === null || stated === null) return null;
  const expect = round2(base * rate / 100);
  if (AMOUNT_CENTS(expect) === AMOUNT_CENTS(stated)) return null;
  return {
    level: 'P0', category: '个人月缴存额与复算不符', line: it.line,
    subject: tag(it), amount: round2(stated - expect), person: String(it.byRole.name || '').trim(),
    message: `${who(it)}的个人月缴存额是 ${stated.toFixed(2)}，`
      + `按 缴存基数 ${base.toFixed(2)} × 个人比例 ${rate}% = ${expect.toFixed(2)}，应为 ${expect.toFixed(2)}`
      + `（相差 ${round2(stated - expect).toFixed(2)}）。`,
    advice: '个人月缴存额是从工资里代扣的那一笔；算错会同时影响工资表代扣与公积金汇缴两个口径。',
  };
}

function checkTotalAmount(it) {
  const u = num(it, 'unitAmt');
  const p = num(it, 'personAmt');
  const stated = num(it, 'totalAmt');
  if (u === null || p === null || stated === null) return null;
  const expect = round2(u + p);
  if (AMOUNT_CENTS(expect) === AMOUNT_CENTS(stated)) return null;
  return {
    level: 'P0', category: '缴存合计与复算不符', line: it.line,
    subject: tag(it), amount: round2(stated - expect), person: String(it.byRole.name || '').trim(),
    message: `${who(it)}的缴存合计是 ${stated.toFixed(2)}，`
      + `按 单位月缴存额 ${u.toFixed(2)} + 个人月缴存额 ${p.toFixed(2)} = ${expect.toFixed(2)}`
      + `（相差 ${round2(stated - expect).toFixed(2)}）。`,
    advice: '缴存合计是单位与个人两笔之和；这一格错了，单位合计与个人合计的勾稽也会跟着错。',
  };
}

function checkTotalRow(totals, items, role) {
  const out = [];
  for (const t of totals) {
    const stated = num(t, role);
    if (stated === null) continue;
    const sum = round2(items.reduce((s, it) => {
      const n = num(it, role);
      return s + (n === null ? 0 : n);
    }, 0));
    if (AMOUNT_CENTS(sum) === AMOUNT_CENTS(stated)) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: t.line,
      subject: `合计行「${LABELS[role]}」`, amount: round2(stated - sum), role,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，`
        + `各明细行（共 ${items.length} 人）相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
      advice: '要么明细行漏了人（新增人员没进表），要么合计行没跟着更新；'
        + '单位合计与个人合计要分别核，两列之和还要等于缴存合计列之和。',
    });
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = keyOf(it);
    if (!key) continue;
    const mon = normMonth(it.byRole.period) || String(it.byRole.period || '').trim();
    const merged = `${mon}|${key}`;
    if (seen.has(merged)) {
      out.push({
        level: 'P1', category: '同一期间重复人员', line: it.line,
        subject: tag(it), amount: null, person: String(it.byRole.name || '').trim(),
        message: `${who(it)}与第 ${seen.get(merged)} 行是同一期间（${mon}）的同一职工（${key}）：`
          + '一个人头出现两次，单位与个人两侧都会按两倍汇缴。',
        advice: '同一个月内一个人只能有一行；分档缴存的请分列并注明，不要让同一人头重复出现。',
      });
    } else {
      seen.set(merged, it.line);
    }
  }
  return out;
}

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          subject: `${tag(it)}「${LABELS[role]}」`, amount: null, role,
          person: String(it.byRole.name || '').trim(),
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这笔缴存额就算不出来；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
  }
  return out;
}

function checkNegatives(items) {
  const out = [];
  for (const it of items) {
    for (const role of ['base', 'unitAmt', 'personAmt', 'totalAmt', 'unitRate', 'personRate']) {
      const isRate = role === 'unitRate' || role === 'personRate';
      const v = isRate ? normRate(it.byRole[role]) : num(it, role);
      if (v !== null && v < 0) {
        out.push({
          level: 'P0', category: '关键字段为负数', line: it.line,
          subject: `${tag(it)}「${LABELS[role]}」`, amount: null, role,
          person: String(it.byRole.name || '').trim(),
          message: `${who(it)}的「${LABELS[role]}」是 ${v}。`,
          advice: '基数、比例、缴存额都不会是负数；出现负值通常是粘贴时带进了减号，或把冲销行混进了本期。',
        });
      }
    }
  }
  return out;
}

function checkBaseRange(items) {
  const out = [];
  for (const it of items) {
    const base = num(it, 'base');
    const max = num(it, 'baseMax');
    if (base === null || max === null) continue;
    if (base > max + TOL) {
      out.push({
        level: 'P1', category: '缴存基数超出表内上下限', line: it.line,
        subject: tag(it), amount: round2(base - max), person: String(it.byRole.name || '').trim(),
        message: `${who(it)}的缴存基数是 ${base.toFixed(2)}，高于表内给定的基数上限 ${max.toFixed(2)}。`,
        advice: '本档只判"超出表内上下限"这件事本身；应调整到多少、月差额多少，见完整档的补退处理清单。',
      });
    }
  }
  return out;
}

/* ===== 以下为订阅版才执行的检查 ===== */

/** 订阅版独有的结论类别（本包一条都不会出现） */
const PAID_CATEGORIES = [
  '缴存基数低于下限',
  '缴存基数超过上限',
  '缴存比例不在允许档',
  '缴存比例与表内档位不符',
  '单位与个人缴存比例不一致',
  '新增 / 离职月份应在职区间不符',
  '区间内存在断缴月份',
  '与工资表应缴口径差异（个人部分）',
  '与工资表应缴口径差异（单位部分）',
];

/** 一条结论对应一条整改动作（补退处理清单用） */
const ACTION_BY_CATEGORY = {
  缴存基数低于下限: '按表内下限调整基数并补缴差额（补缴月份见备注）',
  缴存基数超过上限: '把基数压回上限，多缴部分办理退缴或冲抵下期',
  缴存基数超出表内上下限: '按表内上下限调整基数后重新复算',
  缴存比例不在允许档: '改用允许的整数档重算，并同步更新单位与个人两栏',
  缴存比例与表内档位不符: '让比例与表内档位一致（两者只能有一个是对的）',
  单位与个人缴存比例不一致: '确认当地是否允许两者不同档；不允许则改成同档',
  '新增 / 离职月份应在职区间不符': '删除本期多列的行，或改列为补缴/退缴月份行',
  区间内存在断缴月份: '确认漏缴月份并办理补缴，或在表内补记离职月份',
  与工资表应缴口径差异: '把工资表代扣数同步到与基数、比例一致的口径',
};

const ACTION_LEVELS = new Set(['P0', 'P1']);

/** 超出上下限的基准值：低于下限取下限，高于上限取上限，否则取原值 */
function clampedBase(it) {
  const base = num(it, 'base');
  const min = num(it, 'baseMin');
  const max = num(it, 'baseMax');
  if (base === null) return null;
  let v = base;
  if (min !== null && base < min - TOL) v = min;
  if (max !== null && base > max + TOL) v = max;
  return round2(v);
}

/** 按调整后的基数与原有比例，复算出单位/个人应缴额，并给出月差额（正=应补缴，负=多缴） */
function adjustByBase(it, fixed) {
  const u = num(it, 'unitAmt');
  const p = num(it, 'personAmt');
  const uRate = normRate(it.byRole.unitRate);
  const pRate = normRate(it.byRole.personRate);
  const calc = (amount, rate) => (amount === null || rate === null ? null : round2(fixed * rate / 100));
  const uExpect = calc(u, uRate);
  const pExpect = calc(p, pRate);
  const diff = (u === null || uExpect === null ? 0 : round2(uExpect - u))
    + (p === null || pExpect === null ? 0 : round2(pExpect - p));
  return { u, p, uRate, pRate, uExpect, pExpect, diff: round2(diff) };
}

function checkBaseBelowMin(it) {
  const base = num(it, 'base');
  const min = num(it, 'baseMin');
  if (base === null || min === null) return null;
  if (!(base < min - TOL)) return null;
  const fixed = round2(min);
  const a = adjustByBase(it, fixed);
  return {
    level: 'P0', category: '缴存基数低于下限', line: it.line,
    subject: tag(it), person: String(it.byRole.name || '').trim(),
    base, base_limit: fixed, adjust_base: fixed, amount: a.diff, rate: a.uRate,
    unit_amount: a.u, unit_expected: a.uExpect, person_amount: a.p, person_expected: a.pExpect,
    message: `${who(it)}的缴存基数是 ${base.toFixed(2)}，低于表内给定的基数下限 ${min.toFixed(2)}；`
      + `应调整基数为 ${fixed.toFixed(2)}：按原比例复算 单位 ${a.uExpect === null ? '(比例或金额缺失，算不出)' : a.uExpect.toFixed(2)}`
      + ` / 个人 ${a.pExpect === null ? '(比例或金额缺失，算不出)' : a.pExpect.toFixed(2)}；`
      + `与原缴存额相比，月差额合计 ${a.diff.toFixed(2)}（正数=应补缴，负数=多缴）。`,
    advice: '基数低于下限属于少缴：把基数抬到下限（或补足差额）后重新汇缴，并确认补缴的月份范围。',
  };
}

function checkBaseAboveMax(it) {
  const base = num(it, 'base');
  const max = num(it, 'baseMax');
  if (base === null || max === null) return null;
  if (!(base > max + TOL)) return null;
  const fixed = round2(max);
  const a = adjustByBase(it, fixed);
  return {
    level: 'P0', category: '缴存基数超过上限', line: it.line,
    subject: tag(it), person: String(it.byRole.name || '').trim(),
    base, base_limit: fixed, adjust_base: fixed, amount: a.diff, rate: a.uRate,
    unit_amount: a.u, unit_expected: a.uExpect, person_amount: a.p, person_expected: a.pExpect,
    message: `${who(it)}的缴存基数是 ${base.toFixed(2)}，高于表内给定的基数上限 ${max.toFixed(2)}；`
      + `应调整基数为 ${fixed.toFixed(2)}：按原比例复算 单位 ${a.uExpect === null ? '(比例或金额缺失，算不出)' : a.uExpect.toFixed(2)}`
      + ` / 个人 ${a.pExpect === null ? '(比例或金额缺失，算不出)' : a.pExpect.toFixed(2)}；`
      + `与原缴存额相比，月差额合计 ${a.diff.toFixed(2)}（负数=多缴，应退或冲抵下期）。`,
    advice: '基数超过上限属于多缴：把基数压回上限，多缴部分按规定办理退缴或冲抵下期汇缴。',
  };
}

function checkRateStep(it) {
  const out = [];
  for (const [role, label2] of [['unitRate', '单位比例'], ['personRate', '个人比例']]) {
    const r = normRate(it.byRole[role]);
    if (r === null) continue;
    if (ALLOWED_RATE_STEPS.some((s) => Math.abs(s - r) <= PCT_TOL)) continue;
    const nearest = ALLOWED_RATE_STEPS.reduce((a, b) => (Math.abs(b - r) < Math.abs(a - r) ? b : a));
    out.push({
      level: 'P0', category: '缴存比例不在允许档', line: it.line,
      subject: `${tag(it)}「${label2}」`, person: String(it.byRole.name || '').trim(),
      amount: null, rate: r, nearest_step: nearest,
      message: `${who(it)}的「${label2}」是 ${r}%，不在允许的整数档`
        + `（${ALLOWED_RATE_STEPS.join(' / ')}%，以表内给定口径为准）之内；最接近的合法档是 ${nearest}%。`,
      advice: '比例只能取政策允许的整数档；比例一走偏，单位、个人、合计三笔金额都会跟着走偏。',
    });
  }
  return out;
}

function checkRateMatchesStep(it) {
  const stated = normRate(it.byRole.rateStep);
  if (stated === null) return null;
  for (const [role, label2] of [['unitRate', '单位比例'], ['personRate', '个人比例']]) {
    const r = normRate(it.byRole[role]);
    if (r === null) continue;
    if (Math.abs(r - stated) <= PCT_TOL) continue;
    return {
      level: 'P1', category: '缴存比例与表内档位不符', line: it.line,
      subject: `${tag(it)}「${label2}」`, person: String(it.byRole.name || '').trim(),
      amount: null, rate: r, rate_step: stated,
      message: `${who(it)}的「${label2}」是 ${r}%，与表内给出的比例档位 ${stated}% 不符。`,
      advice: '比例档位是这张表的表内口径；要么档位填错、要么比例用错档，两列一致才谈得上"按档执行"。',
    };
  }
  return null;
}

function checkRateParity(it) {
  const u = normRate(it.byRole.unitRate);
  const p = normRate(it.byRole.personRate);
  if (u === null || p === null) return null;
  if (Math.abs(u - p) <= PCT_TOL) return null;
  return {
    level: 'P1', category: '单位与个人缴存比例不一致', line: it.line,
    subject: tag(it), person: String(it.byRole.name || '').trim(),
    amount: null, unit_rate: u, person_rate: p,
    message: `${who(it)}的单位比例是 ${u}%、个人比例是 ${p}%：两者不一致（本口径下两栏应当同档同值）。`,
    advice: '若当地确实允许两者取不同档，请在备注里写明依据；否则请改成同一档。',
  };
}

function wageGap(it, wageRole, actualRole, label2) {
  const wage = num(it, wageRole);
  const actual = num(it, actualRole);
  if (wage === null || actual === null) return null;
  if (AMOUNT_CENTS(wage) === AMOUNT_CENTS(actual)) return null;
  const diff = round2(actual - wage);
  return {
    level: 'P1', category: `与工资表应缴口径差异（${label2}）`, line: it.line,
    subject: tag(it), person: String(it.byRole.name || '').trim(),
    amount: diff, wage_amount: wage, fund_amount: actual,
    message: `${who(it)}的${label2}：工资表口径是 ${wage.toFixed(2)}，公积金汇缴口径是 ${actual.toFixed(2)}，`
      + `相差 ${diff.toFixed(2)}（正数=公积金侧多列）。`,
    advice: '两个口径必须同源：要么工资表代扣数没跟着基数/比例更新，要么公积金表改了而工资表没同步。',
  };
}

const checkWagePersonDiff = (it) => wageGap(it, 'wagePerson', 'personAmt', '个人部分');
const checkWageUnitDiff = (it) => wageGap(it, 'wageUnit', 'unitAmt', '单位部分');

function checkJoinLeaveMonths(it) {
  const out = [];
  const pIdx = monthIndex(normMonth(it.byRole.period));
  if (pIdx === null) return out;
  const joinIdx = monthIndex(normMonth(it.byRole.joinMonth));
  const leaveIdx = monthIndex(normMonth(it.byRole.leaveMonth));
  const amt = num(it, 'totalAmt');
  const person = String(it.byRole.name || '').trim();
  const fmt = (idx) => `${Math.floor(idx / 12)}-${String((idx % 12) + 1).padStart(2, '0')}`;
  const periodTxt = normMonth(it.byRole.period);
  if (joinIdx !== null && joinIdx > pIdx) {
    out.push({
      level: 'P0', category: '新增 / 离职月份应在职区间不符', line: it.line,
      subject: tag(it), person, amount: amt, kind: '早缴', period: periodTxt,
      message: `${who(it)}标为新增，但新增月份是 ${fmt(joinIdx)}，晚于本期 ${periodTxt}：`
        + `本期本不应缴（已列缴存合计 ${amt === null ? '(缺失)' : amt.toFixed(2)}）。`,
      advice: '新增人员从入职当月起缴（各地口径不同，请以表内区间为准）：本期多列的这笔要么删行、要么改列为补缴月份行。',
    });
  }
  if (leaveIdx !== null && leaveIdx < pIdx) {
    out.push({
      level: 'P0', category: '新增 / 离职月份应在职区间不符', line: it.line,
      subject: tag(it), person, amount: amt, kind: '多缴', period: periodTxt,
      message: `${who(it)}标为离职，但离职月份是 ${fmt(leaveIdx)}，早于本期 ${periodTxt}：`
        + `本期本不应缴（已列缴存合计 ${amt === null ? '(缺失)' : amt.toFixed(2)}）。`,
      advice: '离职人员应在离职当月缴足后停止汇缴：本期这一行属于离职后多缴，应办理退缴或冲抵。',
    });
  }
  return out;
}

/** 断缴：把每个人的缴存月份与表内整体区间对比，缺的月份就是断缴月 */
function checkGapMonths(items) {
  const all = new Set();
  for (const it of items) {
    const m = normMonth(it.byRole.period);
    if (m) all.add(m);
  }
  const sorted = [...all].sort();
  if (sorted.length < 2) return [];
  const lo = monthIndex(sorted[0]);
  const hi = monthIndex(sorted[sorted.length - 1]);
  const perPerson = new Map();
  for (const it of items) {
    const key = keyOf(it);
    const m = normMonth(it.byRole.period);
    if (!key || !m) continue;
    if (!perPerson.has(key)) perPerson.set(key, { months: new Set(), lines: [] });
    const rec = perPerson.get(key);
    rec.months.add(m);
    rec.lines.push(it.line);
  }
  const out = [];
  for (const [key, rec] of perPerson) {
    const missing = [];
    for (let i = lo; i <= hi; i += 1) {
      const mon = `${Math.floor(i / 12)}-${String((i % 12) + 1).padStart(2, '0')}`;
      if (!rec.months.has(mon)) missing.push(mon);
    }
    if (!missing.length) continue;
    out.push({
      level: 'P1', category: '区间内存在断缴月份', line: rec.lines[0],
      subject: String(key), person: String(key), amount: null, months: missing,
      message: `${key}出现在第 ${rec.lines.join('、')} 行，缴存月份为 ${[...rec.months].sort().join('、')}；`
        + `表内整体区间是 ${sorted[0]} ~ ${sorted[sorted.length - 1]}，其中 ${missing.join('、')} 没有缴存记录（断缴）。`,
      advice: '断缴影响连续性：确认是当月漏缴（应补缴）还是离职后停缴（应在表内补记离职月份）。',
    });
  }
  return out;
}

function actionOf(category) {
  if (ACTION_BY_CATEGORY[category]) return ACTION_BY_CATEGORY[category];
  if (category.indexOf('与工资表应缴口径差异') === 0) return ACTION_BY_CATEGORY['与工资表应缴口径差异'];
  return '按表内口径重新复算这一行';
}

/** 补退处理清单：按金额（绝对值）从大到小排，金额待定的排最后；每条带原文行号与建议动作 */
function buildActions(findings) {
  const rows = findings.filter((f) => ACTION_LEVELS.has(f.level)
    && (ACTION_BY_CATEGORY[f.category] || f.category.indexOf('与工资表应缴口径差异') === 0));
  const pick = (o, k) => (o[k] === undefined ? null : o[k]);
  return rows.map((f) => ({
    level: f.level,
    category: f.category,
    line: f.line,
    subject: f.subject,
    person: f.person,
    period: pick(f, 'period'),
    months: pick(f, 'months'),
    amount: pick(f, 'amount'),
    adjust_base: pick(f, 'adjust_base'),
    base: pick(f, 'base'),
    base_limit: pick(f, 'base_limit'),
    unit_amount: pick(f, 'unit_amount'),
    unit_expected: pick(f, 'unit_expected'),
    person_amount: pick(f, 'person_amount'),
    person_expected: pick(f, 'person_expected'),
    rate: pick(f, 'rate'),
    nearest_step: pick(f, 'nearest_step'),
    message: f.message,
    action: actionOf(f.category),
  })).sort((a, b) => {
    const an = a.amount === null ? null : Math.abs(a.amount);
    const bn = b.amount === null ? null : Math.abs(b.amount);
    if (an === null && bn === null) return a.line - b.line;
    if (an === null) return 1;
    if (bn === null) return -1;
    if (bn !== an) return bn - an;
    return a.line - b.line;
  });
}

/* ============================== 入口 ============================== */

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的住房公积金汇缴明细表（要能认出「期间」「姓名」「缴存基数」'
      + '「单位比例（单位缴存比例）」「个人比例（个人缴存比例）」「单位月缴存额」「个人月缴存额」「缴存合计」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从公积金系统或工资表导出后，连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一行的职工缴存明细（只有表头或只有合计行时不做任何认定）']);

  const paid = Boolean(payload && (payload.full || payload.credit || payload.token));
  const findings = [];
  const notRun = [];

  /* 本包：逐人复算 + 合计勾稽 + 重复 / 空缺 / 负数 / 超上下限 */
  for (const it of t.items) {
    const a = checkUnitAmount(it); if (a) findings.push(a);
    const b = checkPersonAmount(it); if (b) findings.push(b);
    const c = checkTotalAmount(it); if (c) findings.push(c);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);
  for (const f of checkNegatives(t.items)) findings.push(f);
  for (const f of checkBaseRange(t.items)) findings.push(f);

  let actions = [];
  if (paid) {
    /* 订阅版多出来的一种能力：**合规判定 + 补退处理清单** */
    for (const it of t.items) {
      const a = checkBaseBelowMin(it); if (a) findings.push(a);
      const b = checkBaseAboveMax(it); if (b) findings.push(b);
      for (const f of checkRateStep(it)) findings.push(f);
      const d = checkRateMatchesStep(it); if (d) findings.push(d);
      const e = checkRateParity(it); if (e) findings.push(e);
      for (const f of checkJoinLeaveMonths(it)) findings.push(f);
      const g = checkWagePersonDiff(it); if (g) findings.push(g);
      const h = checkWageUnitDiff(it); if (h) findings.push(h);
    }
    for (const f of checkGapMonths(t.items)) findings.push(f);
    actions = buildActions(findings);
  } else {
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  }

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));
  const bases = t.items.map((it) => num(it, 'base')).filter((v) => v !== null);
  const periods = [...new Set(t.items.map((it) => normMonth(it.byRole.period)).filter(Boolean))].sort();
  /* 本包没有"调整基数"这类结论 ⇒ 这个计数天然是 0，不是漏算 */
  const adjustable = findings.filter((f) => f.adjust_base !== undefined && f.adjust_base !== null);
  /* 补退处理清单只有订阅版才产出；本包如实为 null（"这类交付物本档没有"，不是 0 条）。
     ⚠️ 这里必须写成**带大括号的付费分支**，不要写多行三元：剥离器只认大括号分支与单行三元。 */
  let actionScope = null;
  let baseAdjustAmount = null;
  if (paid) {
    actionScope = {
      count: actions.length,
      amount_total: round2(actions.reduce((s, a) => s + (a.amount === null ? 0 : a.amount), 0)),
      unknown_amount_count: actions.filter((a) => a.amount === null).length,
    };
    baseAdjustAmount = round2(adjustable.reduce((s, f) => s + (f.amount || 0), 0));
  }

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      unit_total: sumOf('unitAmt'),
      person_total: sumOf('personAmt'),
      grand_total: sumOf('totalAmt'),
      base_min: bases.length ? Math.min.apply(null, bases) : null,
      base_max: bases.length ? Math.max.apply(null, bases) : null,
      basis: '单位月缴存额 = 缴存基数 × 单位比例；个人月缴存额 = 缴存基数 × 个人比例；'
        + '缴存合计 = 单位月缴存额 + 个人月缴存额；合计行逐列与各明细行复核；'
        + '基数与比例的一致性以**表内给定的**上下限与比例档位为准。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
    scope: {
      rows: t.items.length,
      periods,
      total_rows: t.totals.length,
      checks: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
      checks_not_run: paid ? [] : CHECKS_WITHHELD.slice(),
      base_limit_column: t.cols.some((c) => c.role === 'baseMin') && t.cols.some((c) => c.role === 'baseMax'),
      rate_step_column: t.cols.some((c) => c.role === 'rateStep'),
      wage_column: t.cols.some((c) => c.role === 'wageUnit' || c.role === 'wagePerson'),
      allowed_rate_steps: ALLOWED_RATE_STEPS.slice(),
      unit_total: sumOf('unitAmt'),
      person_total: sumOf('personAmt'),
      grand_total: sumOf('totalAmt'),
      base_adjusted_rows: adjustable.length,
      base_adjust_amount: baseAdjustAmount,
      actions: actionScope,
    },
  };
  if (actions.length) result.actions = actions;
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的口径算得对、'
      + '且基数与比例落在表内给定的上下限与档位内**；不代表当地当年真实政策口径就是这样，'
      + '也不代表社保、个税口径已经核对 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, normMonth, normRate, monthIndex, isBlank, round2,
  CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT,
  LABELS, ROLES, REQUIRED, SUM_ROLES, ALLOWED_RATE_STEPS, PAID_CATEGORIES,
};
