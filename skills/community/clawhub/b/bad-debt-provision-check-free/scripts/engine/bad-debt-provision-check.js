/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * bad-debt-provision-check.js —— 应收账款坏账准备计提核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**月末/季末结账与审计前**，财务要把坏账准备计提表核一遍 ——
 * 计提额是按**账龄区间**对应的比例算出来的（账龄越长比例越高），
 * 算错了直接影响利润、也直接影响审计调整与所得税。这是每个有应收账款的公司在做的活，
 * 且**完全能算出来对错**。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   应计提金额 = 应收余额 × 计提比例
 *   计提率     = 计提合计 ÷ 应收余额合计
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**各账龄该用多少比例：比例以表里给的为准，
 *    只对"比例与账龄是否自相矛盾"做**提示性**判断（并明确标注是参考口径）。
 */

const CHECKS_GIVEN = [
  '计提额勾稽（应收余额 × 计提比例 = 已计提金额）',
  '计提比例超出 0~100% 检测',
  '已计提金额为负检测',
  '合计行逐列复核',
  '重复客户与账龄区间检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '同一客户跨区间比例须随账龄递增检测',
  '计提额超过应收余额检测',
  '应收余额为负检测',
  '账龄区间与计提比例是否匹配（参考口径提示）',
  '整体计提率异常检测（<0.5% 或 >50%）',
];

const OUT_OF_SCOPE = [
  '判断各账龄区间该用多少计提比例（那取决于公司会计政策与预期信用损失模型）',
  '测算预期信用损失率、做减值测试（本工具只核"比例 × 余额 = 计提额"这件事）',
  '核对应收账款明细账与总账是否一致',
  '读取 Excel 或 ERP 导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '客户名称\t账龄区间\t应收余额\t计提比例\t已计提金额',
  '豫州建材有限公司\t1年以内\t800000.00\t5%\t40000.00',
  '中岳设备租赁有限公司\t1-2年\t300000.00\t10%\t30000.00',
  '豫通物流有限公司\t2-3年\t120000.00\t30%\t36000.00',
  '合计\t\t1220000.00\t\t106000.00',
].join('\n');

const TOL = 0.01;
const RATE_MIN = 0.005;          // 整体计提率下限（参考）
const RATE_MAX = 0.50;           // 整体计提率上限（参考）

/* 参考口径（仅用于"比例与账龄是否自相矛盾"的**提示**，不是公司政策）：
 * 账龄越长，计提比例的常见下沿越高。 */
const AGE_ORDER = [
  [/1年以内|一年以内|1年内|0-1年/, 1],
  [/1-2年|1至2年|一年至两年/, 2],
  [/2-3年|2至3年|两年至三年/, 3],
  [/3年以上|3-5年|三年以上|5年以上/, 4],
];
const AGE_FLOOR = { 1: 0.0, 2: 0.10, 3: 0.30, 4: 0.50 };   // 各账龄常见**下沿**（参考）

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  customer: ['客户名称', '客户', '单位名称', '往来单位'],
  ageBucket: ['账龄区间', '账龄', '区间', '账期'],
  balance: ['应收余额', '期末余额', '应收账款余额', '余额'],
  rate: ['计提比例', '计提率', '比例'],
  provision: ['已计提金额', '计提金额', '已计提', '坏账准备'],
};

const LABELS = {
  customer: '客户名称', ageBucket: '账龄区间', balance: '应收余额',
  rate: '计提比例', provision: '已计提金额',
};

const REQUIRED = ['customer', 'ageBucket', 'balance', 'rate', 'provision'];
const SUM_ROLES = ['balance', 'provision'];
const TOTAL_WORDS = /^(合计|总计|小计|共计)$/;

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
const round6 = (n) => Math.round(n * 1e6) / 1e6;

/** 比例归一化成小数：`5` / `5%` ⇒ 0.05；`0.05` ⇒ 0.05 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return n > 1 ? n / 100 : n;
}

/** 账龄区间 -> 序号（认不出来返回 null） */
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
      if (role === 'customer' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const c = it && it.customer ? String(it.customer).trim() : `第 ${it && it.line} 行`;
  const a = it && it.ageBucket ? String(it.ageBucket).trim() : '';
  return a ? `${c}（${a}）` : c;
};

/* ================================ 免费档检查项 ================================ */

function checkProvision(it) {
  const bal = normNumber(it.balance);
  const rate = rateValue(it.rate);
  const stated = normNumber(it.provision);
  if (bal === null || rate === null || stated === null) return null;
  const expect = round2(bal * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '计提额与复算不符', line: it.line,
    message: `${who(it)}：应收余额 ${bal.toFixed(2)} × 计提比例 ${(rate * 100).toFixed(2)}% 应为 ${expect.toFixed(2)}，表里写的是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkRateRange(it) {
  const rate = rateValue(it.rate);
  if (rate === null) return null;
  if (rate >= 0 && rate <= 1) return null;
  return {
    level: 'P0', category: '计提比例超出 0~100%', line: it.line,
    message: `${who(it)}的计提比例是 ${(rate * 100).toFixed(3)}%，超出 0~100% —— 比例不可能大于 100%，也不该为负。`,
  };
}

function checkNegativeProvision(it) {
  const v = normNumber(it.provision);
  if (v === null || v >= -TOL) return null;
  return {
    level: 'P0', category: '已计提金额为负', line: it.line,
    message: `${who(it)}的已计提金额是 ${v.toFixed(2)}（负数）—— 冲回应当单独列示，不要用负数混进计提表。`,
  };
}

function checkTotalRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return out;
  let sum = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) sum += v;
  }
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  out.push({
    level: 'P0', category: '合计行与明细之和不符', line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const c = String(it.customer || '').trim();
    if (!c) continue;
    const key = `${c}|${String(it.ageBucket || '').trim()}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一客户同一账龄区间出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 计提基数会被重复计算，请合并。`,
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

/* ============================ 完整档（付费）检查项 ============================ */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到计提表正文（text）—— 请把「客户 / 账龄区间 / 应收余额 / 计提比例 / 已计提金额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `计提表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何客户明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkProvision(it); if (a) findings.push(a);
    const b = checkRateRange(it); if (b) findings.push(b);
    const c = checkNegativeProvision(it); if (c) findings.push(c);

  }

  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let balTotal = 0; let provTotal = 0;
  for (const it of t.items) {
    const b = normNumber(it.balance); if (b !== null) balTotal += b;
    const p = normNumber(it.provision); if (p !== null) provTotal += p;
  }

  const result = {
    status: 'success',
    service_type: 'BAD_DEBT_PROVISION_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      balance_total: round2(balTotal),
      provision_total: round2(provTotal),
      overall_rate: balTotal > 0 ? round6(provTotal / balTotal) : null,
      rate_cap: RATE_MAX,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"余额 × 比例 = 计提额"与比例的自洽性，**不规定各账龄该用多少比例**'
      + '（那取决于公司会计政策与预期信用损失模型）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, rateValue, round2, round6, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
