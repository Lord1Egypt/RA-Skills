/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * asset-disposal-check.js —— 固定资产处置损益核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**处置固定资产当期**（报废、出售、转让），财务必须把处置表核一遍 ——
 * 原值 / 累计折旧 / 账面净值 / 处置收入 / 清理费用 / 处置损益这几列必须自洽。
 * 处置损益直接进当期利润，**也是所得税与审计常查项**：算错要么多缴税、要么被调整。
 * 完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   账面净值   = 原值 − 累计折旧
 *   处置损益   = 处置收入 − 清理费用 − 账面净值
 *                （正数=处置收益，负数=处置损失）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**折旧年限、减值与税务口径，只核处置表内部勾稽。
 */

const CHECKS_GIVEN = [
  '账面净值勾稽（原值 − 累计折旧 = 账面净值）',
  '处置损益勾稽（收入 − 清理费用 − 账面净值 = 处置损益）',
  '累计折旧超过原值检测',
  '合计行逐列复核',
  '重复资产检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '处置收入或清理费用为负检测',
  '账面净值为负检测',
  '原值为零或为负检测',
  '清理费用超过处置收入检测（净支出处置）',
  '无处置收入却记了处置损益检测',
];

const OUT_OF_SCOPE = [
  '判断折旧年限、残值率、减值准备是否合理（那属于会计政策与减值测试）',
  '计算处置的增值税与所得税影响',
  '处理资产组处置、非货币性资产交换、债务重组',
  '读取固定资产卡片或 ERP 导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '资产名称\t原值\t累计折旧\t账面净值\t处置收入\t清理费用\t处置损益',
  '办公大楼A座-电梯\t480000.00\t380000.00\t100000.00\t120000.00\t5000.00\t15000.00',
  '生产设备-3号线\t1200000.00\t1200000.00\t0.00\t30000.00\t8000.00\t22000.00',
  '公务车-豫A12345\t260000.00\t230000.00\t30000.00\t25000.00\t1000.00\t-6000.00',
  '合计\t1940000.00\t1810000.00\t130000.00\t175000.00\t14000.00\t31000.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  item: ['资产名称', '固定资产名称', '设备名称', '资产'],
  cost: ['原值', '原价', '入账价值'],
  accumulated: ['累计折旧', '已提折旧'],
  netValue: ['账面净值', '折余价值', '净值'],
  income: ['处置收入', '变卖收入', '处置价款', '出售收入'],
  expense: ['清理费用', '处置费用', '清理支出'],
  gain: ['处置损益', '处置净损益', '处置盈亏'],
};

const LABELS = {
  item: '资产名称', cost: '原值', accumulated: '累计折旧', netValue: '账面净值',
  income: '处置收入', expense: '清理费用', gain: '处置损益',
};

const REQUIRED = ['item', 'cost', 'accumulated', 'netValue', 'income', 'gain'];
const SUM_ROLES = ['cost', 'accumulated', 'netValue', 'income', 'expense', 'gain'];
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
      if (role === 'item' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => (it && it.item ? String(it.item) : `第 ${it && it.line} 行`);

/* ================================ 免费档检查项 ================================ */

function checkNetValue(it) {
  const cost = normNumber(it.cost);
  const acc = normNumber(it.accumulated);
  const stated = normNumber(it.netValue);
  if (cost === null || acc === null || stated === null) return null;
  const expect = round2(cost - acc);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '账面净值与复算不符', line: it.line,
    message: `${who(it)}：原值 ${cost.toFixed(2)} − 累计折旧 ${acc.toFixed(2)} 应为 ${expect.toFixed(2)}，表里账面净值是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkGain(it) {
  const net = normNumber(it.netValue);
  const inc = normNumber(it.income);
  const exp = normNumber(it.expense);
  const stated = normNumber(it.gain);
  if (net === null || inc === null || stated === null) return null;
  const exp2 = exp === null ? 0 : exp;
  const expect = round2(inc - exp2 - net);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '处置损益与复算不符', line: it.line,
    message: `${who(it)}：处置收入 ${inc.toFixed(2)} − 清理费用 ${exp2.toFixed(2)} − 账面净值 ${net.toFixed(2)} 应为 ${expect.toFixed(2)}，表里处置损益是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkAccOverCost(it) {
  const cost = normNumber(it.cost);
  const acc = normNumber(it.accumulated);
  if (cost === null || acc === null || cost <= 0) return null;
  if (acc <= cost + TOL) return null;
  return {
    level: 'P0', category: '累计折旧超过原值', line: it.line,
    message: `${who(it)}累计折旧 ${acc.toFixed(2)} 超过原值 ${cost.toFixed(2)} —— 折旧总额不可能超过原值（除非有重估，请注明）。`,
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
    const key = String(it.item || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一资产出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 处置损益会被重复计算。`,
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
    return insufficient('没有收到处置表正文（text）—— 请把「资产 / 原值 / 累计折旧 / 账面净值 / 处置收入 / 清理费用 / 处置损益」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `处置表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何资产明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkNetValue(it); if (a) findings.push(a);
    const b = checkGain(it); if (b) findings.push(b);
    const c = checkAccOverCost(it); if (c) findings.push(c);

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

  let gainTotal = 0; let incomeTotal = 0;
  for (const it of t.items) {
    const g = normNumber(it.gain); if (g !== null) gainTotal += g;
    const i = normNumber(it.income); if (i !== null) incomeTotal += i;
  }

  const result = {
    status: 'success',
    service_type: 'ASSET_DISPOSAL_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      assets: t.items.length,
      income_total: round2(incomeTotal),
      gain_total: round2(gainTotal),
      gain_direction: gainTotal > 0 ? '净收益' : (gainTotal < 0 ? '净损失' : '持平'),
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      assets: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核处置表内部勾稽（净值 / 收入 / 清理费用 / 损益），'
      + '**不判断折旧与减值口径**；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
