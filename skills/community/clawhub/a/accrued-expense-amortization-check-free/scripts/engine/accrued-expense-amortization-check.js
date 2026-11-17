/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * accrued-expense-amortization-check.js —— 预提费用与待摊费用摊销核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月结账、对外出报表与年度审计提供底稿之前**，
 * 会计要把「预提费用」（已发生、尚未取得发票，先按估计计提）与「待摊费用」
 * （已付款但受益期跨月，按期摊入费用）的摊销明细表核一遍。
 * 审计与税务汇算盯的就是这几列能不能**逐行滚动对上**：
 *   期末未摊余额 = 期初未摊余额 − 本期实摊金额
 *   累计已摊金额 + 期末未摊余额 = 总金额
 * 这两条一旦对不上，摊销台账后面每个月的数都是错的。
 *
 * 核心可算关系（都能手算复现）：
 *   期末未摊余额 = 期初未摊余额 − 本期实摊金额
 *   累计已摊金额 + 期末未摊余额 = 总金额
 *   直线法每期金额 = 总金额 ÷ 受益月数
 *   本期实摊金额 ≤ 期初未摊余额（不能超摊）；累计已摊金额 ≤ 总金额
 *
 * 免费档执行 7 项；完整档追加 5 项（见 CHECKS_WITHHELD）；材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**该笔费用到底应当预提还是待摊、受益期与摊销方法是否恰当
 *    （那属于会计估计与会计政策判断），只核这张表**内部**的算术与口径。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不写任何文件**。
 *
 * ⚠️ 完整档的检查函数集中放在一起，并由 `run()` 里的**付费分支**统一调用；
 *    免费包由 tools/strip_free_engine.py 摘掉那个分支，再删掉因此没人引用的付费函数
 *    （所以付费函数的函数名**不要**在别处（注释/字符串）出现，否则摘不干净）。
 */

/* ⛔ 顺序即优先级：**带限定语的列必须排在裸词前面**。
   `期初未摊余额` / `期末未摊余额` 都含 `余额`，`总金额` / `本期应摊金额` / `本期实摊金额` / `累计已摊金额`
   都含 `金额`。若把 `余额`、`金额` 这类**裸词**也收成别名，它们会把上面这些列**整列抢走**
   ⇒ 必需列永远认不出来（要么全表判材料不足，要么算错却不报缺列 —— 本仓库踩过 6 次）。
   所以这里**刻意不收录任何裸词**，每个角色只收带限定语的别名；
   `tools/header_map_check.py` 会验证样例表每一列都能被识别成角色、且没有被互相覆盖。 */
const ROLES = {
  item: ['费用项目', '项目名称', '费用名称', '摊销项目', '项目'],
  type: ['费用类型', '费用类别', '摊销类型', '类型'],
  startMonth: ['受益起始月', '摊销起始月', '受益起始', '起始月'],
  months: ['受益月数', '摊销月数', '受益月份', '摊销期数', '月数'],
  total: ['总金额', '费用总额', '摊销总额', '总费用'],
  openBal: ['期初未摊余额', '期初未摊销余额', '期初未摊'],
  dueAmt: ['本期应摊金额', '本期应摊销金额', '应摊金额', '本期应摊'],
  actAmt: ['本期实摊金额', '本期实际摊销金额', '本期实际摊销', '实摊金额', '本期摊销金额', '本期摊销'],
  accAmt: ['累计已摊金额', '累计已摊销金额', '累计摊销金额', '累计已摊'],
  closeBal: ['期末未摊余额', '期末未摊销余额', '期末未摊'],
  basis: ['计提依据', '摊销依据', '计提说明', '依据', '备注', '说明'],
};

const LABELS = {
  item: '费用项目', type: '费用类型', startMonth: '受益起始月', months: '受益月数',
  total: '总金额', openBal: '期初未摊余额', dueAmt: '本期应摊金额', actAmt: '本期实摊金额',
  accAmt: '累计已摊金额', closeBal: '期末未摊余额', basis: '计提依据',
};

/* 必需列：缺任何一列都**照常给结论**，只是如实报一条「列缺失」并停做与它有关的检查。 */
const REQUIRED = ['item', 'type', 'startMonth', 'months', 'total', 'openBal', 'dueAmt', 'actAmt', 'accAmt', 'closeBal'];
/* 合计行要逐列复核的 6 个金额列。 */
const SUM_ROLES = ['total', 'openBal', 'dueAmt', 'actAmt', 'accAmt', 'closeBal'];
const TOTAL_WORDS = /^(合计|总计|小计|共计)$/;
const TOL = 0.01;

const CHECKS_GIVEN = [
  '合计行逐列复核（总金额 / 期初未摊余额 / 本期应摊金额 / 本期实摊金额 / 累计已摊金额 / 期末未摊余额）',
  '同一「费用项目 + 受益起始月」重复行检测',
  '期末未摊余额 = 期初未摊余额 − 本期实摊金额（逐行滚动勾稽）',
  '累计已摊金额 + 期末未摊余额 = 总金额（总额勾稽）',
  '本期实摊金额为负检测',
  '本期实摊金额超过期初未摊余额（超摊）提示',
  '空白与占位符检测（含必需列缺失）',
];

const CHECKS_WITHHELD = [
  '直线法偏离检测（本期实摊金额偏离「总金额 ÷ 受益月数」超过 5%）',
  '期末未摊余额为负检测',
  '受益月数为 0 或空但本期仍在摊销检测',
  '累计已摊金额超过总金额（超摊）检测',
  '费用类型不在「预提费用 / 待摊费用」口径内的提示',
];

const OUT_OF_SCOPE = [
  '判断该笔费用应当**预提**还是**待摊**、受益期与摊销方法是否恰当（属于会计估计与会计政策判断）',
  '判断「计提依据」写的内容（合同 / 预算 / 用量估算）是否真实、充分，也不替代审计程序或出具鉴证意见',
  '核对摊销明细表与总账、明细账、报表之间的其他勾稽（本工具只核这一张表内部的逐行算术关系）',
  '读取 ERP / 财务系统导出的文件（需要你先导出成文本贴进来）',
  '处理跨年摊销、所得税税前扣除与纳税调整（属于税务判断）',
];

const SAMPLE_TEXT = [
  '费用项目\t费用类型\t受益起始月\t受益月数\t总金额\t期初未摊余额\t本期应摊金额\t本期实摊金额\t累计已摊金额\t期末未摊余额\t计提依据',
  '房租\t待摊费用\t2026-01\t12\t120000.00\t120000.00\t10000.00\t10000.00\t10000.00\t110000.00\t租赁合同，按 12 个月直线摊销',
  '水电费\t预提费用\t2026-01\t12\t24000.00\t24000.00\t2000.00\t2000.00\t2000.00\t22000.00\t按上年同期与用量预估',
  '保险费\t待摊费用\t2026-01\t12\t36000.00\t36000.00\t3000.00\t3000.00\t3000.00\t33000.00\t保单，按 12 个月直线摊销',
  '合计\t\t\t\t180000.00\t180000.00\t15000.00\t15000.00\t15000.00\t165000.00\t',
].join('\n');

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
  let s = String(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '') return null;
  let neg = false;
  if (/^\(.*\)$/.test(s)) { neg = true; s = s.slice(1, -1); }
  if (s.endsWith('%')) s = s.slice(0, -1);
  if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
  const n = Number(s);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

function who(it) {
  const name = String(it.item || '').trim();
  const type = String(it.type || '').trim();
  return name ? `${name}（${type || '未注明类型'}）` : `第 ${it.line} 行`;
}

function parseTable(text) {
  const lines = String(text).split(/\r?\n/).map((l) => l.trim()).filter((l) => l !== '');
  if (!lines.length) return { items: [], totals: {}, missingColumns: [], header: [] };
  const header = splitRow(lines[0]);
  const cols = header.map((h, i) => ({ i, role: roleOf(h), raw: h }));
  const missingColumns = REQUIRED.filter((r) => !cols.some((c) => c.role === r));
  const items = [];
  const totals = {};
  for (let li = 1; li < lines.length; li += 1) {
    const cells = splitRow(lines[li]);
    const row = { line: li + 1 };
    cols.forEach((c) => { if (c.role) row[c.role] = cells[c.i] === undefined ? '' : cells[c.i]; });
    const label = (cells[0] || '').replace(/\s/g, '');
    if (TOTAL_WORDS.test(label)) { totals.line = li + 1; totals.row = row; continue; }
    items.push(row);
  }
  return { items, totals, missingColumns, header };
}

/* ================================ 免费档检查项 ================================ */

function checkTotalRow(items, totals) {
  if (!totals.row) return [];
  const out = [];
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let sum = 0;
    let n = 0;
    for (const it of items) {
      const v = normNumber(it[role]);
      if (v === null) continue;
      sum += v;
      n += 1;
    }
    sum = round2(sum);
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        line: totals.line, level: 'P1', category: '合计复核',
        message: `合计行「${LABELS[role]}」填 ${stated}，但明细逐行相加是 ${sum}，相差 ${round2(stated - sum)}`,
        evidence: `合计=${stated}；明细合计=${sum}（${n} 行）`,
      });
    }
  }
  return out;
}

function checkRollForward(it) {
  const open = normNumber(it.openBal);
  const act = normNumber(it.actAmt);
  const close = normNumber(it.closeBal);
  if (open === null || act === null || close === null) return null;
  const expect = round2(open - act);
  if (Math.abs(expect - close) <= TOL) return null;
  return {
    line: it.line, level: 'P0', category: '期末未摊余额滚动不符',
    message: `${who(it)} 期初未摊 ${open} − 本期实摊 ${act} 应为 ${expect}，但表里期末未摊填的是 ${close}，相差 ${round2(close - expect)}`,
    evidence: `期初未摊余额=${open}；本期实摊金额=${act}；应有期末未摊余额=${expect}；表内期末未摊余额=${close}`,
  };
}

function checkTotalReconcile(it) {
  const acc = normNumber(it.accAmt);
  const close = normNumber(it.closeBal);
  const total = normNumber(it.total);
  if (acc === null || close === null || total === null) return null;
  const sum = round2(acc + close);
  if (Math.abs(sum - total) <= TOL) return null;
  return {
    line: it.line, level: 'P0', category: '累计已摊加期末未摊不等于总金额',
    message: `${who(it)} 累计已摊 ${acc} + 期末未摊 ${close} = ${sum}，但总金额是 ${total}，相差 ${round2(sum - total)}`,
    evidence: `累计已摊金额=${acc}；期末未摊余额=${close}；两者合计=${sum}；总金额=${total}`,
  };
}

function checkNegativeActual(it) {
  const act = normNumber(it.actAmt);
  if (act === null || act >= -TOL) return null;
  return {
    line: it.line, level: 'P0', category: '本期实摊金额为负',
    message: `${who(it)} 本期实摊金额为 ${act}（负数）—— 摊销冲回应单独列示，不能混在本期实摊金额里`,
    evidence: `本期实摊金额=${act}`,
  };
}

function checkOverAmortize(it) {
  const act = normNumber(it.actAmt);
  const open = normNumber(it.openBal);
  if (act === null || open === null) return null;
  if (act - open <= TOL) return null;
  return {
    line: it.line, level: 'P1', category: '本期实摊超过期初未摊余额',
    message: `${who(it)} 本期实摊 ${act} 超过期初未摊余额 ${open}，超出 ${round2(act - open)}`,
    evidence: `本期实摊金额=${act}；期初未摊余额=${open}；超出=${round2(act - open)}`,
  };
}

function checkDuplicate(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const name = String(it.item || '').trim();
    const start = String(it.startMonth || '').trim();
    const key = `${name}|${start}`;
    if (!name && !start) continue;
    if (seen.has(key)) {
      out.push({
        line: it.line, level: 'P1', category: '重复行',
        message: `${who(it)} 与第 ${seen.get(key)} 行的「费用项目 + 受益起始月」完全相同 —— 摊销可能被重复计入`,
        evidence: `费用项目=${name}；受益起始月=${start}；与第 ${seen.get(key)} 行重复`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBlanks(header, items, missingColumns) {
  const out = [];
  if (missingColumns.length) {
    out.push({
      line: 1, level: 'P1', category: '列缺失',
      message: `表头缺少必需列：${missingColumns.map((r) => LABELS[r]).join('、')}（共 ${missingColumns.length} 列）—— 与这些列有关的检查本次无法执行`,
      evidence: `表头=${header.join('|')}；缺少=${missingColumns.join('、')}`,
    });
  }
  for (const it of items) {
    for (const role of REQUIRED) {
      if (missingColumns.indexOf(role) >= 0) continue;
      if (isBlank(it[role])) {
        out.push({
          line: it.line, level: 'P1', category: '空白或占位符',
          message: `${who(it)} 的「${LABELS[role]}」是空白或占位符（第 ${it.line} 行）—— 这一行无法核对`,
          evidence: `${LABELS[role]}=${it[role] === undefined ? '(空)' : it[role]}`,
        });
      }
    }
  }
  return out;
}

/* ============================== 完整档（付费）检查项 ============================== */

/* ================================== 主流程 ================================== */

function run(payload) {
  const p = payload || {};
  const text = p.text === undefined || p.text === null ? '' : String(p.text);
  if (text.trim() === '') return insufficient(['材料文本为空：请把预提待摊明细表（含表头）贴进来']);

  const { items, totals, missingColumns, header } = parseTable(text);
  if (!header.some((h) => roleOf(h))) {
    return insufficient(['认不出表头：第一行必须是列名（费用项目 / 费用类型 / 受益起始月 / 受益月数 / 总金额 / 期初未摊余额 / 本期应摊金额 / 本期实摊金额 / 累计已摊金额 / 期末未摊余额），Tab 分隔最稳']);
  }
  if (!items.length) {
    return insufficient(['认不出任何明细行：第一行必须是表头，且至少有一行明细（合计行可留）']);
  }

  const findings = [];
  for (const f of checkTotalRow(items, totals)) findings.push(f);
  for (const it of items) {
    const one = [checkRollForward(it), checkTotalReconcile(it), checkNegativeActual(it), checkOverAmortize(it)];
    for (const f of one) if (f) findings.push(f);
  }
  for (const f of checkDuplicate(items)) findings.push(f);
  for (const f of checkBlanks(header, items, missingColumns)) findings.push(f);



  findings.sort((a, b) => (a.line - b.line) || String(a.category).localeCompare(String(b.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;
  const checkList = CHECKS_GIVEN;
  const notRun = CHECKS_WITHHELD;

  return {
    status: 'success',
    result: {
      findings,
      summary: {
        rows: items.length,
        total: findings.length,
        p0, p1, p2,
        verdict: findings.length === 0 ? 'NO_ISSUE_FOUND' : (p0 > 0 ? 'P0_ISSUES' : 'ISSUES'),
        omitted: 0,
      },
      scope: {
        checks: checkList,
        checks_not_run: notRun,
        rows: items.length,
        act_total: round2(items.reduce((n, it) => n + (normNumber(it.actAmt) || 0), 0)),
        close_total: round2(items.reduce((n, it) => n + (normNumber(it.closeBal) || 0), 0)),
        tolerance: TOL,
        executed_locally: true,
        network_used: false,
      },
    },
  };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
