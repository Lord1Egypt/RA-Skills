/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * production-yield-scrap-check.js —— 生产投入产出与报废率核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**制造企业每天/每批（按工单、按工序）核投入产出** ——
 * 投料量（投入量）、完工量、报废量、期末在制、良率、报废率。
 * 良率掉了就是钱在漏：投进去的料去哪了必须闭环，所以这几个数**完全能算出来对错**：
 *
 *   完工量 + 报废量 = 投入量 − 期末在制     （投入的去向必须闭环）
 *   良率           = 完工量 ÷ 投入量
 *   报废率         = 报废量 ÷ 投入量
 *   上工序产出     = 下工序投入            （工序之间转序的数量要对得上）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**良率与报废率的行业合理水平（各行业差异大）：超额只做**提示**并明确标注是参考，
 *    判断口径以本厂历史水平与客户要求为准。
 */

const CHECKS_GIVEN = [
  '投入产出与报废量勾稽复算（完工量 + 报废量 = 投入量 − 期末在制）',
  '良率与完工量复算（良率 = 完工量 ÷ 投入量）',
  '合计行逐列复核',
  '同一工单同一工序重复行检测',
  '空白与占位符检测',
  '数量为负检测（投入量 / 完工量 / 期末在制）',
];

const CHECKS_WITHHELD = [
  '报废率超过参考上限（3%）提示（参考口径）',
  '良率与报废率之和不为 1 检测（期末在制为 0 的行）',
  '投入量为零却有报废检测',
  '报废量为负（返工/退料误记）提示',
  '工序间数量不匹配（上工序产出 ≠ 下工序投入）提示',
];

const OUT_OF_SCOPE = [
  '判断良率与报废率的行业合理水平（各行业差异大，请以本厂历史水平与客户要求为准）',
  '核对 BOM 用量定额、工艺损耗标准与工单领料凭据',
  '处理返工、改制、拆解与联产品/副产品的产量分摊',
  '读取 ERP / MES 导出文件（需要你先导出成文本贴进来）',
];

/* 参考上限：仅供"明显偏高"时提示，不是判定合格的标准 */
const SCRAP_RATE_REF = 0.03;

const SAMPLE_TEXT = [
  '工单号\t期间\t工序\t投入量\t完工量\t报废量\t期末在制\t良率\t报废率',
  'MO-2606-001\t2026-06-01\t下料\t1000.00\t980.00\t20.00\t0.00\t98%\t2%',
  'MO-2606-001\t2026-06-01\t机加工\t980.00\t960.40\t19.60\t0.00\t98%\t2%',
  'MO-2606-002\t2026-06-01\t装配\t500.00\t495.00\t5.00\t0.00\t99%\t1%',
  'MO-2606-003\t2026-06-02\t下料\t1200.00\t1188.00\t12.00\t0.00\t99%\t1%',
  '合计\t\t\t3680.00\t3623.40\t56.60\t0.00\t\t',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的词前面，否则列会被抢走 ⇒ 静默算错。
  //    实测坑：`报废率` 里含 `报废`，若 scrapQty 排在 scrapRate 前面，
  //    「报废率」整列会被当成报废量（率被当量、差 100 倍），而且**一列都不缺、不报错**。
  workOrder: ['工单号', '生产工单号', '生产工单', '制令单号', '派工单号', '工单'],
  period: ['期间', '月份', '所属期', '生产日期', '日期', '批次'],
  process: ['工序名称', '加工工序', '工序'],
  inputQty: ['投入数量', '投入量', '投料量', '领用量', '投入'],
  outputQty: ['完工数量', '完工量', '产出数量', '产出量', '合格数量', '合格量', '产出', '完工'],
  wipQty: ['期末在制数量', '期末在制', '在制数量', '在制量', '在产品', '在制'],
  yieldRate: ['良品率', '合格率', '产出率', '良率'],
  scrapRate: ['报废率', '废品率', '报废比例', '损耗率'],
  scrapQty: ['报废数量', '报废量', '废品数量', '废品量', '报废', '废品'],
};

const LABELS = {
  workOrder: '工单号', period: '期间', process: '工序', inputQty: '投入量', outputQty: '完工量',
  wipQty: '期末在制', yieldRate: '良率', scrapRate: '报废率', scrapQty: '报废量',
};

const REQUIRED = ['workOrder', 'period', 'process', 'inputQty', 'outputQty', 'scrapQty', 'wipQty', 'yieldRate', 'scrapRate'];
const SUM_ROLES = ['inputQty', 'outputQty', 'scrapQty', 'wipQty'];
/** 免费档的"数量为负"只管这三列；负报废量是**返工/退料误记**这一领域判断，属于完整档 */
const NEG_ROLES = ['inputQty', 'outputQty', 'wipQty'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|本月合计|总投入)$/;

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
  const h = String(header).replace(/[\s（）()【】[\]]/g, '');
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

/** 比率归一化成小数：`2%` ⇒ 0.02；`0.02` ⇒ 0.02；`2` ⇒ 0.02 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
}

const round2 = (n) => Math.round(n * 100) / 100;
const num2 = (n) => n.toFixed(2);

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
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
      if ((role === 'workOrder' || role === 'period') && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; } else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const wo = !isBlank(it && it.workOrder) ? String(it.workOrder).trim() : `第 ${it && it.line} 行`;
  const pr = !isBlank(it && it.process) ? String(it.process).trim() : '';
  const pd = !isBlank(it && it.period) ? String(it.period).trim() : '';
  return `${wo}${pr ? ' · ' + pr : ''}${pd ? '（' + pd + '）' : ''}`;
};

/* ================================ 免费档检查项 ================================ */
/* 约定：**返回对象的**在调用处写 `const x = f(it); if (x) findings.push(x)`；
 *       **返回数组的**一律写 `for (const x of f(it)) findings.push(x)` ——
 *       两者混用会让空数组 `[]`（真值）被当成一条发现（上一轮真实踩到）。 */

function checkInputOutputBalance(it) {
  const inp = normNumber(it.inputQty);
  const out = normNumber(it.outputQty);
  const scrap = normNumber(it.scrapQty);
  const wip = normNumber(it.wipQty);
  if (inp === null || out === null || scrap === null || wip === null) return null;
  const left = round2(out + scrap);
  const right = round2(inp - wip);
  if (Math.abs(left - right) <= TOL) return null;
  return {
    level: 'P0', category: '投入产出勾稽不符', line: it.line,
    message: `${who(it)}：完工量 ${num2(out)} + 报废量 ${num2(scrap)} = ${num2(left)}，`
      + `投入量 ${num2(inp)} − 期末在制 ${num2(wip)} = ${num2(right)}，相差 ${num2(round2(left - right))} —— `
      + '投进去的料只有三个去向：完工、报废、留在在制，必须闭环。',
  };
}

function checkYieldRate(it) {
  const inp = normNumber(it.inputQty);
  const out = normNumber(it.outputQty);
  const stated = rateValue(it.yieldRate);
  if (inp === null || out === null || stated === null) return null;
  if (Math.abs(inp) <= TOL) return null;   // 投入为 0 ⇒ 良率无从算起（由完整档的"投入为零"提示处理）
  const expect = out / inp;
  if (Math.abs(expect - stated) <= RATE_TOL) return null;
  return {
    level: 'P0', category: '良率复算不符', line: it.line,
    message: `${who(it)}：完工量 ${num2(out)} ÷ 投入量 ${num2(inp)} = ${(expect * 100).toFixed(2)}%，`
      + `表里良率是 ${(stated * 100).toFixed(2)}%，相差 ${((stated - expect) * 100).toFixed(2)} 个百分点 —— `
      + '良率是钱的漏斗，写错会直接看漏损失。',
  };
}

function checkTotalRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return out;
  let sum = 0;
  let n = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) { sum += v; n += 1; }
  }
  if (!n) return out;
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  out.push({
    level: 'P0', category: '合计行与明细之和不符', line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${num2(stated)}，各工单工序行相加是 ${num2(sum)}，相差 ${num2(round2(stated - sum))}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const wo = String(it.workOrder === undefined ? '' : it.workOrder).trim();
    if (!wo) continue;
    const key = wo + '\u0000' + String(it.process === undefined ? '' : it.process).trim();
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一工单同一工序重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现过，第 ${it.line} 行又出现一次 —— `
          + '同工单同工序的数量会被重复统计（跨工序的多行是正常转序，不算重复）。',
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
        });
      }
    }
  }
  return out;
}

function checkNegatives(it) {
  const out = [];
  for (const role of NEG_ROLES) {
    const v = normNumber(it[role]);
    if (v !== null && v < -TOL) {
      out.push({
        level: 'P0', category: '数量为负', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${num2(v)}（负数）—— 投入/完工/在制都不能为负，`
          + '冲回、退料、返工请单独列示，否则良率会被算成虚高。',
      });
    }
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到生产投入产出与报废表正文（text）—— 请把「工单号 / 期间 / 工序 / 投入量 / 完工量 / 报废量 / 期末在制 / 良率 / 报废率」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `生产投入产出与报废表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何工单工序明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkInputOutputBalance(it); if (a) findings.push(a);
    const b = checkYieldRate(it); if (b) findings.push(b);

  }
  for (const role of SUM_ROLES) {
    for (const x of checkTotalRow(t.totals, t.items, role)) findings.push(x);
  }
  for (const x of checkDuplicates(t.items)) findings.push(x);
  for (const x of checkBlanks(t.items)) findings.push(x);
  for (const it of t.items) {
    for (const x of checkNegatives(it)) findings.push(x);
  }


  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let inputTotal = 0; let outputTotal = 0; let scrapTotal = 0;
  const periods = new Set();
  for (const it of t.items) {
    const a = normNumber(it.inputQty); if (a !== null) inputTotal += a;
    const b = normNumber(it.outputQty); if (b !== null) outputTotal += b;
    const c = normNumber(it.scrapQty); if (c !== null) scrapTotal += c;
    const p = !isBlank(it.period) ? String(it.period).trim() : '';
    if (p) periods.add(p);
  }

  const result = {
    status: 'success',
    service_type: 'PRODUCTION_YIELD_SCRAP_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.size,
      input_total: round2(inputTotal),
      output_total: round2(outputTotal),
      scrap_total: round2(scrapTotal),
      scrap_rate_ref: SCRAP_RATE_REF,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periods.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"完工量 + 报废量 = 投入量 − 期末在制""良率 = 完工量 ÷ 投入量""上工序产出 = 下工序投入"'
      + '这类内部勾稽，**不规定良率与报废率的行业合理水平**（以本厂历史水平与客户要求为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, rateValue, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
