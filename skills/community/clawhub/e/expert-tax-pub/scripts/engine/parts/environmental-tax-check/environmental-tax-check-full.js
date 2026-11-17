#!/usr/bin/env node
/**
 * environmental-tax-check.js —— 环境保护税申报核对（本包 / 订阅版共用源码）
 *
 * 真实痛点：**排放应税污染物的企业每季度申报环保税前必核这张表**，而它是四条串行算式：
 *   ① 污染当量数 = 排放量 ÷ 污染当量值
 *   ② 本期应纳税额 = 污染当量数 × 适用税额
 *   ③ 本期应纳（减免后）= 本期应纳税额 − 减免税额（**负数按 0**）
 *   ④ 应补（退）= 本期应纳 − 已缴税额（正数补缴、负数可退）
 * 当量值用错档、该减免没减、监测报告/排污许可的排放量与申报数不一致，
 * 是环保税最常见的**多缴**与**少缴**来源；而污染当量值、适用税额、减免档
 * **都是地方口径**，所以本工具**一律只按你表里给的参数复算，不写死任何一省政策**。
 *
 * 与已有能力的区别：`property-tax-land-use-check` 核的是房产税/城镇土地使用税的
 * 从价从租与土地面积；本能力核的是**环保税的污染当量 — 税额 — 减免 — 已缴**这条链，
 * 参数（当量值 / 适用税额 / 减免比例）全部由输入提供。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查政策文库、不调用大模型；材料不足不给结论；**不给税务意见、不做筹划**。
 *
 * ⚠️ 付费项的写法：订阅版里有一个**布尔开关**（读入参里表示"订阅版"的那个标志），
 *    付费检查全部包进 `if (开关) { ... }`（**不要**留「订阅版才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 另外：本表有一个**列角色**也叫 `paid`（已缴税额），它和上面的开关**不是一回事**，
 *    删开关时不要连它一起动了（`strip_free_engine` 只认"开关形态"，不会碰角色名）。
 */
'use strict';

const CHECKS_GIVEN = [
  '污染当量数复算（排放量 ÷ 污染当量值）',
  '本期应纳税额复算（污染当量数 × 适用税额）',
  '本期应纳（减免后）复算（应纳税额 − 减免税额，负数按 0）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '同一污染物重复行检测',
  '关键字段空缺与负值、污染当量值缺失检测',
];

const CHECKS_WITHHELD = [
  '减免与口径判定（应减免未减、按你声明的减免比例复算减免额、应减未减的金额按档位保守估）',
  '排放量与监测报告 / 排污许可量勾稽（申报排放量低于监测或许可的差额）',
  '同一污染物在同一期间重复申报（按金额列出重复多报的部分）',
  '污染当量值与表内多数口径不一致（当量值是地方参数，取错档等于整行算错）',
  '已缴与应纳差异（多缴可退 / 少缴应补，按金额排序）',
  '申报处理清单（按金额从大到小排序，每条带原文行号 + 建议动作）',
];

const OUT_OF_SCOPE = [
  '给出税务意见或做环保税筹划（本工具只复算你表里的数，不判断该怎么报）',
  '替你认定适用哪一档污染当量值或哪一档适用税额（地方口径差异大，一律由你的输入提供）',
  '读取 .xlsx / PDF 监测报告（需要你先导出或复制成文本贴进来）',
  '判断排放数据本身的真实性（那是监测与排污许可的事，本工具只做勾稽）',
];

const SAMPLE_TEXT = [
  '所属期\t污染物名称\t排放量\t污染当量值\t污染当量数\t适用税额\t本期应纳税额\t减免税额\t本期应纳\t监测报告排放量\t排污许可允许排放量\t已缴税额\t减免情形\t减免比例',
  '2026-Q1\t一般性粉尘\t10000.00\t0.95\t10526.32\t1.20\t12631.58\t2105.68\t10525.90\t10000.00\t10000.00\t10525.90\t低于排放标准\t16.67%',
  '2026-Q1\t二氧化硫\t3000.00\t0.95\t3157.89\t1.20\t3789.47\t0.00\t3789.47\t3000.00\t3000.00\t3789.47\t\t',
  '2026-Q1\t氮氧化物\t5000.00\t0.95\t5263.16\t1.20\t6315.79\t0.00\t6315.79\t5000.00\t5000.00\t6315.79\t\t',
  '合计\t\t18000.00\t\t18947.37\t\t22736.84\t2105.68\t20631.16\t18000.00\t18000.00\t20631.16\t\t',
].join('\n');

const TOL = 0.01;        // 金额容差（分）
const TOL_EQ = 0.02;     // 污染当量数保留两位小数的容差

const ROLES = {
  // ⚠️ 关键词顺序是**本仓库踩过两次的坑**（tools/header_map_check.py 常驻守卫）：
  //    更具体的词必须排在更宽泛的前面，否则宽泛词会把具体列抢走，而且**不报错、只是算错**。
  //    本表里真实存在的抢列关系（自己数过一遍）：
  //      · 「监测报告排放量 / 排污许可允许排放量」都含 `排放量` ⇒ 必须排在 emission 之前
  //      · 「减免税额」与「减免情形 / 减免比例」共用 `减免` ⇒ 具体的两个必须排在 reduction 之前
  //      · 「污染当量数」必须排在「污染当量值」之前（"当量值"会抢走"当量数"）
  //      · 「期间」会抢走「监测…排放量」（监**期间**隔）⇒ period 排在 monitor/permit 之后
  //      · 「污染物名称」必须排在泛指「污染物」之前
  //      · 「本期应纳」是「本期应纳税额」的前缀 ⇒ tax 必须排在 payable 之前（否则税额列被抢成应纳列）
  monitor: ['监测报告排放量', '监测排放量', '监测数据排放量'],
  permit: ['排污许可允许排放量', '排污许可排放量', '许可排放量'],
  ratio: ['减免比例', '减免率', '减免幅度'],
  policy: ['减免情形', '减免类型', '减免政策'],
  reduction: ['减免税额', '减免额'],
  tax: ['本期应纳税额', '应纳税额', '应纳环保税额'],
  payable: ['本期应纳', '减免后应纳', '应纳（减免后）', '应纳(减免后)', '应纳环保税'],
  paid: ['已缴税额', '已缴金额', '已缴环保税', '本期已缴'],
  eqCount: ['污染当量数', '当量数'],
  eqValue: ['污染当量值', '当量值'],
  rate: ['适用税额', '税额标准', '单位税额'],
  period: ['所属期', '税款所属期', '申报期间', '纳税期间', '季度', '期间'],
  item: ['污染物名称', '应税污染物', '污染物', '排放口'],
  emission: ['排放量', '排放数量', '实际排放量'],
};

const LABELS = {
  period: '所属期', item: '污染物名称', emission: '排放量', eqValue: '污染当量值',
  eqCount: '污染当量数', rate: '适用税额', tax: '本期应纳税额', reduction: '减免税额',
  payable: '本期应纳', monitor: '监测报告排放量', permit: '排污许可允许排放量',
  paid: '已缴税额', policy: '减免情形', ratio: '减免比例',
};

const REQUIRED = ['period', 'item', 'emission', 'eqValue', 'eqCount', 'rate', 'tax', 'reduction', 'payable'];
const SUM_ROLES = ['emission', 'eqCount', 'tax', 'reduction', 'payable'];
// 减免档 **不是**工具写死的 —— 比例一律取自表里的「减免比例」列。
const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

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
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

const round2 = (n) => Math.round(n * 100) / 100;

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
    const first = String(cells[0] || '').trim();
    if (/^(合计|总计|小计|total)/i.test(first)) {
      row.isTotal = true; totals.push(row);
    } else {
      items.push(row);
    }
  }
  // 表头里的角色 → 原始表头文字（结论里引用"哪一列"时用）
  const headerOf = {};
  for (const c of cols) if (c.role && !headerOf[c.role]) headerOf[c.role] = c.header;
  return { cols, items, totals, headerOf };
}

const num = (it, role) => normNumber(it.byRole[role]);
const who = (it) => `第 ${it.line} 行「${it.byRole.period || '(未填所属期)'} / ${it.byRole.item || '(未填污染物)'}」`;

/* ============ 本包检查（这一段在免费包里保留） ============ */

function checkEqCount(it) {
  const emission = num(it, 'emission');
  const eqValue = num(it, 'eqValue');
  const stated = num(it, 'eqCount');
  if (emission === null || eqValue === null || stated === null) return null;
  if (Math.abs(eqValue) <= 1e-9) return null;
  const raw = emission / eqValue;
  const expect = round2(raw);
  if (Math.abs(expect - stated) <= TOL_EQ) return null;
  return {
    level: 'P0', category: '污染当量数与复算不符', line: it.line,
    message: `${who(it)}的污染当量数是 ${stated.toFixed(2)}，`
      + `按 排放量 ${emission.toFixed(2)} ÷ 污染当量值 ${eqValue} = ${raw.toFixed(4)}，应为 ${expect.toFixed(2)}。`,
    advice: '当量数 = 排放量 ÷ 当量值；当量值取错档或除反了，这一格就会整行错。',
  };
}

function checkTax(it) {
  const eqCount = num(it, 'eqCount');
  const rate = num(it, 'rate');
  const stated = num(it, 'tax');
  if (eqCount === null || rate === null || stated === null) return null;
  const expect = round2(eqCount * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '本期应纳税额与复算不符', line: it.line,
    message: `${who(it)}的本期应纳税额是 ${stated.toFixed(2)}，`
      + `按 污染当量数 ${eqCount.toFixed(2)} × 适用税额 ${rate} 应为 ${expect.toFixed(2)}。`,
    advice: '适用税额按你表里填的档算；档取错了这一行会整体偏大或偏小。',
  };
}

function checkPayable(it) {
  const tax = num(it, 'tax');
  const reduction = num(it, 'reduction');
  const stated = num(it, 'payable');
  if (tax === null || reduction === null || stated === null) return null;
  const raw = round2(tax - reduction);
  const expect = Math.max(0, raw);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '本期应纳（减免后）与复算不符', line: it.line,
    message: `${who(it)}的本期应纳是 ${stated.toFixed(2)}，`
      + `按 应纳税额 ${tax.toFixed(2)} − 减免税额 ${reduction.toFixed(2)} = ${raw.toFixed(2)}`
      + `${raw < 0 ? '（负值按 0 计）' : ''}，应为 ${expect.toFixed(2)}。`,
    advice: '减免额大于应纳税额时本期应纳按 0，不能填成负数；差额要落到"应退"或结转里去。',
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
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        level: 'P0', category: '合计行与明细之和不符', line: t.line,
        message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，`
          + `相差 ${round2(stated - sum).toFixed(2)}。`,
        advice: '要么明细行漏了污染物/期间，要么合计行没跟着更新。',
      });
    }
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const period = String(it.byRole.period || '').trim();
    const item = String(it.byRole.item || '').trim();
    if (!period || !item) continue;
    const key = `${period}\u0000${item}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一污染物重复出现', line: it.line,
        message: `「${period} / ${item}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一排放口同一污染物在同一所属期只该报一行；重复行会把当量数与税额一起翻倍。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

function checkBlanksAndNegatives(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这一行的税额就算不出来；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
    for (const [role, label] of [['emission', '排放量'], ['tax', '本期应纳税额'],
      ['reduction', '减免税额'], ['payable', '本期应纳'], ['eqCount', '污染当量数']]) {
      const v = num(it, role);
      if (v !== null && v < -TOL) {
        out.push({
          level: 'P0', category: `${label}为负`, line: it.line,
          message: `${who(it)}的${label}是 ${v.toFixed(2)}。`,
          advice: '这几项按申报口径都不会为负：减免额大于应纳税额时应纳按 0，差额体现在应退或结转里。',
        });
      }
    }
    const eqValue = num(it, 'eqValue');
    if (eqValue !== null && Math.abs(eqValue) <= 1e-9) {
      out.push({
        level: 'P0', category: '污染当量值为零', line: it.line,
        message: `${who(it)}的污染当量值是 ${eqValue}。`,
        advice: '当量值是除数，为 0 时当量数无法计算；按你适用的地方口径把当量值填进来（本工具不替你选档）。',
      });
    }
    const evRaw = it.byRole.eqValue;
    if ((evRaw === undefined || String(evRaw).trim() === '') && num(it, 'emission') !== null) {
      out.push({
        level: 'P0', category: '污染当量值缺失', line: it.line,
        message: `${who(it)}填了排放量，但没有填污染当量值。`,
        advice: '当量值由你适用的地方口径决定；补齐前这一行的当量数与税额都算不出来。',
      });
    }
  }
  return out;
}

/* ===== 以下为订阅版才执行的检查 ===== */

// 按你表里**自己声明**的减免比例复算减免额（工具不写死任何一省的减免档）
function checkReductionPolicy(it) {
  const out = [];
  const tax = num(it, 'tax');
  const reduction = num(it, 'reduction');
  const ratio = num(it, 'ratio');
  const policy = String(it.byRole.policy === undefined ? '' : it.byRole.policy).trim();
  if (tax === null || reduction === null) return out;
  // 只在输入**自己声明了**减免时才判定（本工具不写死任何一省的减免档）
  const saysReduce = /减|免|低于|综合|利用|优惠|不征/.test(policy) || (ratio !== null && ratio > 0);
  if (saysReduce && reduction <= TOL) {
    out.push({
      level: 'P0', category: '应减免未减', line: it.line, amount: round2(tax),
      message: `${who(it)}声明了减免情形「${policy || '(只给了减免比例)'}」，`
        + `但减免税额填的是 ${reduction.toFixed(2)}，本期应纳税额 ${tax.toFixed(2)} 被全额申报。`,
      advice: '先按你适用的减免档确认该不该减：该减未减就是多缴；确认后把减免税额补上并重算本期应纳。',
    });
  }
  if (ratio !== null && ratio > 0 && tax !== null) {
    const expect = round2(tax * ratio / 100);
    // 比例本身两位小数、税额本身两位小数 ⇒ 复算出的减免额允许 ±0.02 的舍入差，避免误报。
    if (Math.abs(expect - reduction) > TOL_EQ) {
      const diff = round2(reduction - expect);
      out.push({
        level: 'P0', category: '减免额与声明比例不符', line: it.line, amount: Math.abs(diff),
        message: `${who(it)}声明的减免比例是 ${ratio}%，`
          + `按 本期应纳税额 ${tax.toFixed(2)} × ${ratio}% 应为 ${expect.toFixed(2)}，实填 ${reduction.toFixed(2)}`
          + `（相差 ${diff.toFixed(2)}）。`,
        advice: '比例是你自己填的参数，本工具只按它复算；比例填错或减免额抄错都会在这里露出来。',
      });
    }
  }
  return out;
}

// 申报排放量 vs 监测报告 / 排污许可允许排放量
function checkEmissionVsEvidence(it) {
  const out = [];
  const emission = num(it, 'emission');
  if (emission === null) return out;
  for (const [role, label] of [['monitor', '监测报告排放量'], ['permit', '排污许可允许排放量']]) {
    const evidence = num(it, role);
    if (evidence === null) continue;
    if (evidence - emission > TOL) {
      out.push({
        level: 'P0', category: `排放量低于${label}`, line: it.line,
        amount: round2(evidence - emission),
        message: `${who(it)}申报的排放量是 ${emission.toFixed(2)}，`
          + `${label}是 ${evidence.toFixed(2)}，申报数低 ${round2(evidence - emission).toFixed(2)}。`,
        advice: `先查为什么申报数小于${label}：抄错、漏了某个排放口、还是口径不同（监测值/许可值/申报值要能对上）；确认后再定是改申报还是留说明。`,
      });
    }
  }
  const monitor = num(it, 'monitor');
  const permit = num(it, 'permit');
  if (monitor !== null && permit !== null && Math.abs(monitor - permit) > TOL) {
    out.push({
      level: 'P2', category: '监测报告与排污许可数据不一致', line: it.line,
      amount: Math.abs(round2(monitor - permit)),
      message: `${who(it)}的监测报告排放量是 ${monitor.toFixed(2)}，排污许可允许排放量是 ${permit.toFixed(2)}，`
        + `两者相差 ${round2(monitor - permit).toFixed(2)}。`,
      advice: '两份底稿对不上时，先确认以哪一份作为申报口径；差异要留说明，别只改申报表。',
    });
  }
  return out;
}

// 同一污染物在同一所属期重复申报 —— 按金额列出重复多报的部分
function checkDuplicateDeclarations(items) {
  const groups = new Map();
  for (const it of items) {
    const period = String(it.byRole.period || '').trim();
    const item = String(it.byRole.item || '').trim();
    if (!period || !item) continue;
    const key = `${period}\u0000${item}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(it);
  }
  const out = [];
  for (const rows of groups.values()) {
    if (rows.length < 2) continue;
    const lines = rows.map((r) => r.line);
    const dupTax = round2(rows.slice(1).reduce((s, r) => s + (num(r, 'tax') || 0), 0));
    const dupEmission = round2(rows.slice(1).reduce((s, r) => s + (num(r, 'emission') || 0), 0));
    for (const r of rows.slice(1)) {
      out.push({
        level: 'P1', category: '同一污染物重复申报', line: r.line,
        amount: num(r, 'tax') === null ? 0 : round2(num(r, 'tax')),
        message: `${who(r)}与第 ${lines[0]} 行是同一所属期同一污染物：`
          + `第 ${lines[0]} 行排放量 ${(num(rows[0], 'emission') || 0).toFixed(2)}、本期应纳税额 ${(num(rows[0], 'tax') || 0).toFixed(2)}，`
          + `本行排放量 ${(num(r, 'emission') || 0).toFixed(2)}、本期应纳税额 ${(num(r, 'tax') || 0).toFixed(2)}。`
          + `重复部分合计排放量 ${dupEmission.toFixed(2)}、应纳税额 ${dupTax.toFixed(2)}。`,
        advice: '确认是不是同一排放口被拆成两行、或者两张底稿被贴了两遍；重复的部分要删掉后重算合计。',
      });
    }
  }
  return out;
}

// 当量值是地方参数：偏离表内多数口径的行，整行都值得复核
function checkEqValueConsistency(items) {
  const freq = new Map();
  for (const it of items) {
    const v = num(it, 'eqValue');
    if (v === null) continue;
    const k = String(v);
    freq.set(k, (freq.get(k) || 0) + 1);
  }
  if (freq.size < 2) return [];
  let major = null; let best = -1;
  for (const [k, n] of freq.entries()) {
    if (n > best) { major = Number(k); best = n; }
  }
  const out = [];
  for (const it of items) {
    const v = num(it, 'eqValue');
    if (v === null) continue;
    if (Math.abs(v - major) <= 1e-9) continue;
    const eqCount = num(it, 'eqCount');
    const tax = num(it, 'tax');
    out.push({
      level: 'P1', category: '污染当量值与表内多数口径不一致', line: it.line,
      amount: tax === null ? 0 : round2(Math.abs(tax)),
      message: `${who(it)}的污染当量值是 ${v}，而本表多数行用的是 ${major}（${best} 行）。`
        + `${eqCount === null ? '' : `该行污染当量数 ${eqCount.toFixed(2)}、`}`
        + `${tax === null ? '' : `本期应纳税额 ${tax.toFixed(2)}`}。`,
      advice: `当量值按污染物分档（本表多数行取 ${major}）；若这一行确实适用别的档，请在表里注明依据，否则整行的当量数与税额都要重算。`,
    });
  }
  return out;
}

// 已缴 vs 应纳：多缴可退 / 少缴补缴
function checkPaidVsPayable(it) {
  const payable = num(it, 'payable');
  const paid = num(it, 'paid');
  if (payable === null || paid === null) return [];
  const diff = round2(payable - paid);
  if (Math.abs(diff) <= TOL) return [];
  const over = diff < 0;
  return [{
    level: over ? 'P1' : 'P0', category: over ? '已缴多于应纳（可退）' : '已缴少于应纳（应补）',
    line: it.line, amount: Math.abs(diff),
    message: `${who(it)}的本期应纳是 ${payable.toFixed(2)}，已缴税额是 ${paid.toFixed(2)}，`
      + `相差 ${Math.abs(diff).toFixed(2)}（${over ? '多缴' : '少缴'}）。`,
    advice: over
      ? '多缴的部分按你适用的申报口径确认能否退（抵）税及申请期限；本工具只算差额，不给税务意见。'
      : '少缴要在申报期内补上，避免滞纳金；先核对是不是漏了某个污染物或减免算错。',
  }];
}

// 其他值得进处理清单的项（材料口径不一致、缺证据）
function checkEvidenceGaps(it) {
  const out = [];
  const emission = num(it, 'emission');
  const monitorBlank = isBlank(it.byRole.monitor);
  const permitBlank = isBlank(it.byRole.permit);
  if (emission !== null && monitorBlank && permitBlank) {
    out.push({
      level: 'P2', category: '缺监测报告与排污许可数据', line: it.line, amount: 0,
      message: `${who(it)}只有申报排放量 ${emission.toFixed(2)}，监测报告排放量与排污许可允许排放量都没填。`,
      advice: '把监测报告和排污许可里的排放量一起贴进来，才能做勾稽；在那之前这一行的排放量无法被第三方复算。',
    });
  }
  const ratio = num(it, 'ratio');
  if (ratio !== null && (ratio < 0 || ratio > 100)) {
    out.push({
      level: 'P2', category: '减免比例不在 0~100% 之间', line: it.line, amount: 0,
      message: `${who(it)}的减免比例是 ${ratio}%。`,
      advice: '减免比例是百分数；大于 100 或为负多半是填错（比如把 0.5 当成 50% 填了）。',
    });
  }
  return out;
}

// 申报处理清单：按金额从大到小，每条带原文行号 + 建议动作
// （订阅版独有；免费包里这个函数因为没人引用会被 strip_free_engine 一并摘掉）
function buildDeclarationItems(declarationItems) {
  const rank = { P0: 0, P1: 1, P2: 2 };
  return declarationItems.slice().sort((a, b) => {
    const d = (b.amount || 0) - (a.amount || 0);
    if (Math.abs(d) > 1e-9) return d;
    return (rank[a.level] - rank[b.level]) || (a.line - b.line);
  });
}

// 订阅版独有的收尾：一份**申报处理清单**（按金额从大到小排序，每条带原文行号 + 建议动作）。
// 本包**结构上做不到**，所以这段付费实现会被 strip_free_engine 整块摘掉。
// ⚠️ 这里写成 `checkXxx(it) { push }` 段落，是因为 strip_free_engine 只按"整行 `if (付费开关) {`"
//    识别形态；而且它还会迭代删掉"没人引用"的顶层函数 —— 所以收尾逻辑**不能**包进辅助函数里。
function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的环境保护税申报明细表（要能认出「所属期」「污染物名称」「排放量」「污染当量值」'
      + '「污染当量数」「适用税额」「本期应纳税额」「减免税额」「本期应纳」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从申报底稿导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个污染物的明细行']);

  const paid = Boolean(payload && (payload.full || payload.credit || payload.token));
  const findings = [];
  // 本包：如实记下"本次没有执行的检查项"（这是说明文本，不是实现）。
  const notRun = CHECKS_WITHHELD.slice();

  for (const it of t.items) {
    const a = checkEqCount(it); if (a) findings.push(a);
    const b = checkTax(it); if (b) findings.push(b);
    const c = checkPayable(it); if (c) findings.push(c);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanksAndNegatives(t.items)) findings.push(f);

  // 订阅版独有的 5 项口径判定（申报处理清单就从这些结论里来）。本包这一段会被整块摘掉，
  // 因为免费包里 `if (付费开关)` 这个条件成立不了 —— 摘掉后本包只剩上面那 6 项。
  if (paid) {
    for (const it of t.items) {
      for (const f of checkReductionPolicy(it)) findings.push(f);
      for (const f of checkEmissionVsEvidence(it)) findings.push(f);
      for (const f of checkPaidVsPayable(it)) findings.push(f);
      for (const f of checkEvidenceGaps(it)) findings.push(f);
    }
    for (const f of checkDuplicateDeclarations(t.items)) findings.push(f);
    for (const f of checkEqValueConsistency(t.items)) findings.push(f);
  }

  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));

  const result = {
    findings,
    summary: {
      periods: new Set(t.items.map((it) => String(it.byRole.period || '').trim()).filter(Boolean)).size,
      pollutants: new Set(t.items.map((it) => String(it.byRole.item || '').trim()).filter(Boolean)).size,
      rows: t.items.length,
      emission_total: sumOf('emission'),
      eqcount_total: sumOf('eqCount'),
      tax_total: sumOf('tax'),
      reduction_total: sumOf('reduction'),
      payable_total: sumOf('payable'),
      basis: '污染当量数 = 排放量 ÷ 污染当量值；本期应纳税额 = 污染当量数 × 适用税额；'
        + '本期应纳（减免后）= 本期应纳税额 − 减免税额（负数按 0）；合计行逐列复核；'
        + '污染当量值 / 适用税额 / 减免比例一律取自输入，本工具不写死任何地方政策。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_out_of_scope: OUT_OF_SCOPE,
  };

  // 收尾：订阅版与本包在"结果结构"上的差别只在这里。
  if (paid) {
    // 订阅版独有：把每一条结论折算成"表内金额差"，产出**申报处理清单**
    //（按金额从大到小排序，每条带原文行号 + 建议动作）。
    const actionItems = buildDeclarationItems(findings);
    // 结论计数必须在订阅版的检查跑完之后再算（本包那 6 项之外还有 5 项口径判定）
    result.summary.total = findings.length;
    result.summary.p0 = findings.filter((f) => f.level === 'P0').length;
    result.summary.p1 = findings.filter((f) => f.level === 'P1').length;
    result.summary.p2 = findings.filter((f) => f.level === 'P2').length;
    result.findings = findings.slice().sort((x, y) => (x.line - y.line)
      || String(x.category).localeCompare(String(y.category)));
    result.checks_executed = CHECKS_GIVEN.concat(CHECKS_WITHHELD);
    result.declaration_items = actionItems;
    result.scope = {
      checks_executed: CHECKS_GIVEN.length + CHECKS_WITHHELD.length,
      declaration_items_total: actionItems.length,
      declaration_amount_total: round2(actionItems.reduce((s, f) => s + (f.amount || 0), 0)),
    };
    result.note = '以上是**申报处理清单**（按金额从大到小排列），每条都带原文行号与建议动作；'
      + '金额是"这一条涉及的表内金额差"，不是最终应退应补税额 —— 本工具不给税务意见，也不做筹划。';
  } else {
    result.findings = findings.slice().sort((x, y) => (x.line - y.line)
      || String(x.category).localeCompare(String(y.category)));
    result.summary.total = result.findings.length;
    result.summary.p0 = result.findings.filter((f) => f.level === 'P0').length;
    result.summary.p1 = result.findings.filter((f) => f.level === 'P1').length;
    result.summary.p2 = result.findings.filter((f) => f.level === 'P2').length;
    result.checks_executed = CHECKS_GIVEN;
    result.checks_not_run = notRun;
    result.scope = { checks_executed: CHECKS_GIVEN.length, checks_withheld: CHECKS_WITHHELD.length };
  }

  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的口径算得对**，'
      + '不代表减免档适用正确、也不代表排放数据真实 —— 那些按范围声明不在本工具内（本工具不替你选档）。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2,
  CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT,
  LABELS, SUM_ROLES,
};
