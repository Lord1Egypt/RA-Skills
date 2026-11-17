/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * ad-agency-rebate-check.js —— 广告代理返点与框架返点核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每季度对账时**。品牌方与代理商的季度结算里，
 * 「媒体框架返点」「代理服务费」「投放消耗」三方必须对得上；返点漏收就是白送钱，
 * 算错还会把采购口径与税务口径（返点该冲成本还是记收入）一起带偏。季度一过再追，
 * 媒体与代理多半已经不认账了。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   应收返点 = 投放消耗 × 返点比例
 *   净应付   = 投放消耗 + 代理服务费 − 应收返点
 *   合计行各列 = 明细行相加
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**框架协议里到底该给多少个点的返点、阶梯门槛怎么设（那属于商务谈判与
 *    合同判断）：表里给的框架返点比例、阶梯返点比例、框架任务量一律**以你填的为准**，
 *    本工具只核表内勾稽与档位提示，并把可疑处按原文行号列出来。
 *
 * ⚠️ 档位开关用**形态 B**：先把入参里的完整档开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 if 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时摘除脚本会走形态 A 把免费检查也整块删掉）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：摘除脚本的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚。
 */

const CHECKS_GIVEN = [
  '应收返点复算（投放消耗 × 返点比例 = 应收返点）',
  '净应付复算（投放消耗 + 代理服务费 − 应收返点 = 净应付）',
  '合计行逐列复核',
  '同一媒体同一期间重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '返点比例与框架协议不一致提示（适用比例既不等于框架返点比例、也不等于阶梯返点比例）',
  '返点超过投放消耗提示',
  '未达框架量却按高阶梯返点计算提示',
  '同一媒体重复计返点提示（媒体写法不同但实为同一媒体）',
  '服务费费率偏离参考区间（0~20%）提示',
];

const OUT_OF_SCOPE = [
  '判断框架协议里到底该给多少个点的返点、阶梯门槛与达标口径怎么定（属于媒体/代理商务谈判与合同判断，请以框架协议与商务口径为准）',
  '核对框架协议、返点确认单（Credit Note）、媒体结算单的条款本身（结算周期、是否含税、按含税还是不含税口径计提返点）',
  '处理返点的增值税与企业所得税口径（返点该冲减成本还是确认收入、跨期如何计提，请咨询税务师）',
  '判断媒体或代理给出的投放消耗、返点数据是否真实（本工具只核表内勾稽与档位提示，不评价数据来源）',
  '读取媒体后台 / DSP / 代理结算系统导出的文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t媒体名称\t框架协议号\t框架返点比例\t投放消耗\t返点比例\t应收返点\t代理服务费\t净应付\t框架任务量\t累计投放消耗\t阶梯返点比例',
  '2026-Q1\t腾讯广告\tFR-2026-001\t8%\t300000.00\t8%\t24000.00\t30000.00\t306000.00\t500000.00\t900000.00\t10%',
  '2026-Q2\t腾讯广告\tFR-2026-001\t8%\t200000.00\t8%\t16000.00\t20000.00\t204000.00\t500000.00\t900000.00\t10%',
  '2026-Q1\t巨量引擎\tFR-2026-002\t6%\t150000.00\t6%\t9000.00\t15000.00\t156000.00\t300000.00\t480000.00\t8%',
  '2026-Q2\t巨量引擎\tFR-2026-002\t6%\t130000.00\t6%\t7800.00\t13000.00\t135200.00\t300000.00\t480000.00\t8%',
  '合计\t\t\t\t780000.00\t\t56800.00\t78000.00\t801200.00\t\t\t',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;          // 比率容差：0.05 个百分点
const SERVICE_RATE_MAX = 0.2;     // 代理服务费费率的参考上限：20%
const SERVICE_RATE_TOL = 0.005;   // 费率容差：0.5 个百分点

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  //    （「累计投放消耗」不能被「投放消耗」抢走、「框架返点比例」「阶梯返点比例」不能被
  //     「返点比例」抢走、「返点比例」不能被「返点」抢走、「框架协议号」不能被「框架返点比例」抢走）
  period: ['所属期间', '会计期间', '结算期间', '所属期', '期间', '季度', '月份'],
  media: ['媒体名称', '投放媒体', '媒介名称', '媒体'],
  cumSpend: ['累计投放消耗', '本期累计消耗', '年度累计消耗', '累计消耗'],
  spend: ['投放消耗', '媒体消耗', '广告消耗', '投放金额', '消耗金额', '投放额', '消耗'],
  frameworkRate: ['框架协议返点比例', '框架返点比例', '框架返点率'],
  tierRate: ['阶梯返点比例', '高阶返点比例', '阶梯返点率', '阶梯比例'],
  rebateRate: ['适用返点比例', '本表返点比例', '返点比例', '返点率', '返点比率'],
  framework: ['框架协议编号', '框架合同编号', '框架协议号', '框架合同号', '框架协议', '协议编号'],
  rebate: ['应收返点', '应返返点', '本期返点', '返点金额', '应计返点', '返点'],
  serviceFee: ['代理服务费', '平台服务费', '服务费金额', '服务费', '代理费'],
  netPayable: ['净应付金额', '应付净额', '净应付', '净额'],
  frameworkVolume: ['框架任务量', '框架承诺量', '承诺投放量', '保底投放量', '任务量', '保底量'],
};

const LABELS = {
  period: '所属期间', media: '媒体名称', framework: '框架协议号', frameworkRate: '框架返点比例',
  spend: '投放消耗', rebateRate: '返点比例', rebate: '应收返点', serviceFee: '代理服务费',
  netPayable: '净应付', frameworkVolume: '框架任务量', cumSpend: '累计投放消耗', tierRate: '阶梯返点比例',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'media', 'spend', 'rebateRate', 'rebate', 'serviceFee', 'netPayable'];
/** 完整档额外需要的列：缺了就只报材料不足，绝不用默认值替买家判断 */
const FULL_REQUIRED = ['framework', 'frameworkRate', 'tierRate', 'frameworkVolume', 'cumSpend'];
/** 合计行逐列复核的列（框架任务量与累计消耗是"按框架的存量口径"，不做加总） */
const SUM_ROLES = ['spend', 'rebate', 'serviceFee', 'netPayable'];
/**
 * 免费档负值检测覆盖的列。
 * ⚠️ 刻意**不含净应付** —— 净应付为负的根因是"返点超过投放消耗"，
 *    那是完整档的独立检查项（见 CHECKS_WITHHELD），
 *    免费档提前报出净应付为负就等于把付费结论送出去了。
 */
const NEGATIVE_ROLES = ['spend', 'rebate', 'serviceFee', 'frameworkVolume', 'cumSpend'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|合计：|汇总)$/;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|空)$/i.test(s);
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
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

/** 比率归一化成小数：`8%` ⇒ 0.08；`0.08` ⇒ 0.08；`8` ⇒ 0.08 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null, missingFull: [] };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const missingFull = FULL_REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  const totals = {};
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1 };
    let isTotal = false;
    roles.forEach((role, c) => {
      if (!role) return;
      const v = cells[c] === undefined ? '' : cells[c];
      row[role] = v;
      if (role === 'period' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns, missingFull };
}

const who = (it) => {
  const p = it && it.period !== undefined && String(it.period).trim() !== ''
    ? String(it.period).trim() : `第 ${it && it.line} 行`;
  const n = [it && it.media, it && it.framework]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkRebateRecompute(it) {
  const out = [];
  const spend = normNumber(it.spend);
  const rate = rateValue(it.rebateRate);
  const stated = normNumber(it.rebate);
  if (spend === null || rate === null || stated === null) return out;
  const expect = round2(spend * rate);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '应收返点复算不符', line: it.line,
    message: `${who(it)}：投放消耗 ${spend.toFixed(2)} × 返点比例 ${(rate * 100).toFixed(4)}% = ${expect.toFixed(2)}，`
      + `表里「应收返点」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '返点就是"投放消耗 × 返点比例"：算少了的那部分就是白送给媒体的钱，季度一过基本追不回来。',
  });
  return out;
}

function checkNetPayableRecompute(it) {
  const out = [];
  const spend = normNumber(it.spend);
  const fee = normNumber(it.serviceFee);
  const rebate = normNumber(it.rebate);
  const stated = normNumber(it.netPayable);
  if (spend === null || fee === null || rebate === null || stated === null) return out;
  const expect = round2(spend + fee - rebate);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '净应付复算不符', line: it.line,
    message: `${who(it)}：投放消耗 ${spend.toFixed(2)} + 代理服务费 ${fee.toFixed(2)} − 应收返点 ${rebate.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「净应付」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '净应付是付款与请款的口径：这里错了，要么多付给媒体、要么返点没被真正扣下来。',
  });
  return out;
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals || !totals.row) return out;
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let sum = 0;
    let n = 0;
    for (const it of items) {
      const v = normNumber(it[role]);
      if (v !== null) { sum += v; n += 1; }
    }
    if (!n) continue;
    const expect = round2(sum);
    if (Math.abs(stated - expect) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，本表 ${n} 行明细的「${LABELS[role]}」相加是 ${expect.toFixed(2)}，`
        + `相差 ${round2(stated - expect).toFixed(2)}。合计行就是季度对账与请款的取数口径，对不上说明有一边错。`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined ? String(it.period).trim() : '';
    const m = it.media !== undefined ? String(it.media).trim() : '';
    if (!p || !m) continue;
    const key = `${p}|${m}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一媒体同一期间重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一期间、同一媒体再次出现 —— `
          + '要么是重复粘贴了一行，要么是同一笔投放被拆成两行（比如按投放位各建一行）。'
          + '多出来的那一行会把投放消耗与返点都重复计一遍。',
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`
            + '这一列缺失时对应的复算做不了：缺哪一列就补哪一列，别让空值静默跳过检查。',
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    out.push({
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 投放消耗、返点、服务费与框架任务量都不该为负，`
        + '冲回 / 红字应单独列示并在备注里说明。',
    });
  }
  return out;
}

/* ---------- 完整档（付费）追加的检查项 ---------- */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到广告代理返点与框架返点核对表正文（text）—— 请把「所属期间 / 媒体名称 / 框架协议号 / 框架返点比例 / 投放消耗 / 返点比例 / 应收返点 / 代理服务费 / 净应付 / 框架任务量 / 累计投放消耗 / 阶梯返点比例」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `广告代理返点与框架返点核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }

  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何返点明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkRebateRecompute(it));
    findings.push(...checkNetPayableRecompute(it));
    findings.push(...checkNegative(it));

  }

  findings.push(...checkTotalRow(t.totals, t.items));
  findings.push(...checkDuplicates(t.items));
  findings.push(...checkBlanks(t.items));

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let spendTotal = 0;
  let rebateTotal = 0;
  let feeTotal = 0;
  let netTotal = 0;
  for (const it of t.items) {
    const s = normNumber(it.spend);
    if (s !== null) spendTotal += s;
    const rb = normNumber(it.rebate);
    if (rb !== null) rebateTotal += rb;
    const f = normNumber(it.serviceFee);
    if (f !== null) feeTotal += f;
    const np = normNumber(it.netPayable);
    if (np !== null) netTotal += np;
  }

  const result = {
    status: 'success',
    service_type: 'AD_AGENCY_REBATE_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      spend_total: round2(spendTotal),
      rebate_total: round2(rebateTotal),
      service_fee_total: round2(feeTotal),
      net_payable_total: round2(netTotal),
      tolerance: TOL,
      rate_tolerance: RATE_TOL,
      service_rate_max: SERVICE_RATE_MAX,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: groups.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"投放消耗 × 返点比例 = 应收返点"与"投放消耗 + 代理服务费 − 应收返点 = 净应付"这类**表内勾稽**与档位提示，'
      + '**不判断框架协议里到底该给多少个点的返点、阶梯门槛怎么定**（以框架协议与商务口径为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
