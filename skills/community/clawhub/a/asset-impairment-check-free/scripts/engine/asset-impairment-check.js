/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * asset-impairment-check.js —— 资产减值测试核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每年年度终了（或出现减值迹象时）**，财务都要对资产做减值测试 ——
 * 拿**账面价值**与**可收回金额**比较算出**减值损失**，再确认**减值准备**的
 * 期初余额、本期计提、本期转回或处置、期末余额。这几列彼此勾稽，
 * 算错会直接影响当期利润与资产列报，而且完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   减值损失     = 账面价值 − 可收回金额（差额为负按 0，即不计提）
 *   期末减值准备 = 期初减值准备 + 本期计提 − 本期转回或处置
 *   合计行       = 各明细行逐列相加
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**折现率与资产组怎么划（行业与企业不同）：只对"明显偏离常见区间"做**提示**，
 *    并明确标注是参考 —— 取值以评估报告与管理层判断为准。
 */

const CHECKS_GIVEN = [
  '减值损失复算（账面价值 − 可收回金额，负数按 0）',
  '减值准备余额勾稽（期初 + 本期计提 − 本期转回或处置 = 期末）',
  '合计行逐列复核',
  '同一资产重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '可收回金额高于账面价值却计提减值检测',
  '计提额超过减值损失检测',
  '减值准备余额为负检测',
  '折现率偏离参考区间（5%~15%）提示（参考口径）',
  '资产组划分与账面价值合计不符提示',
];

const OUT_OF_SCOPE = [
  '判断减值迹象是否真实存在、资产组怎么划分（那是会计判断，需管理层结论）',
  '计算可收回金额（公允价值减处置费用 / 预计未来现金流量现值）与折现率取值',
  '处理商誉减值、总部资产分摊与减值相关的递延所得税影响',
  '读取评估报告或 ERP 导出文件（需要你先导出成文本贴进来）',
];

/* 参考区间：仅供"明显偏离"时提示，不替代评估结论 */
const RATE_REF = [0.05, 0.15];

const SAMPLE_TEXT = [
  '资产编号\t资产名称\t所属资产组\t期间\t账面价值\t可收回金额\t减值损失\t期初减值准备\t本期计提\t本期转回或处置\t期末减值准备\t折现率\t资产组账面价值合计',
  'A-001\t生产线A\t资产组一\t2026年度\t1000000.00\t880000.00\t120000.00\t50000.00\t120000.00\t0.00\t170000.00\t10%\t1600000.00',
  'A-002\t生产线B\t资产组一\t2026年度\t600000.00\t560000.00\t40000.00\t20000.00\t40000.00\t0.00\t60000.00\t10%\t1600000.00',
  'A-003\t厂房\t资产组二\t2026年度\t400000.00\t400000.00\t0.00\t0.00\t0.00\t0.00\t0.00\t10%\t400000.00',
  '合计\t\t\t\t2000000.00\t1840000.00\t160000.00\t70000.00\t160000.00\t0.00\t230000.00\t\t',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前。
  //    「资产组账面价值合计」必须排在「资产组」与「账面价值」**之前**，
  //    否则这一列会被抢走（表头照样解析得出，只是那一列静默地不参与检查）。
  assetCode: ['资产编号', '资产代码', '资产编码', '资产卡号'],
  assetName: ['资产名称', '资产全称', '资产名'],
  groupTotal: ['资产组账面价值合计', '资产组账面合计', '资产组账面价值', '资产组合计'],
  group: ['所属资产组', '资产组名称', '资产组', '所属组'],
  period: ['期间', '所属期', '会计期间', '年度'],
  bookValue: ['账面价值', '账面余额', '账面净值'],
  recoverable: ['可收回金额', '可回收金额', '可收回净值'],
  impairLoss: ['减值损失', '减值额', '本期减值损失'],
  openProvision: ['期初减值准备', '期初减值准备余额', '期初余额', '期初计提'],
  charge: ['本期计提', '本期计提额', '当期计提', '计提减值', '计提金额'],
  reversal: ['本期转回或处置', '本期转回', '转回或处置', '本期处置', '转回金额'],
  closeProvision: ['期末减值准备', '期末减值准备余额', '减值准备余额', '期末余额'],
  discountRate: ['折现率', '折现比率', '税前折现率'],
};

const LABELS = {
  assetCode: '资产编号', assetName: '资产名称', groupTotal: '资产组账面价值合计', group: '所属资产组',
  period: '期间', bookValue: '账面价值', recoverable: '可收回金额', impairLoss: '减值损失',
  openProvision: '期初减值准备', charge: '本期计提', reversal: '本期转回或处置',
  closeProvision: '期末减值准备', discountRate: '折现率',
};

const REQUIRED = ['assetCode', 'bookValue', 'recoverable', 'impairLoss',
  'openProvision', 'charge', 'reversal', 'closeProvision'];
const AMOUNT_ROLES = ['bookValue', 'recoverable', 'impairLoss', 'openProvision',
  'charge', 'reversal', 'closeProvision'];
const SUM_ROLES = AMOUNT_ROLES.slice();
const TOTAL_WORDS = /^(合计|总计|小计|共计|合计数|本年合计)$/;

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

/** 比率归一化成小数：`10%` ⇒ 0.10；`0.10` ⇒ 0.10；`10` ⇒ 0.10 */
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
    roles.forEach((role, c) => {
      if (!role) return;
      row[role] = cells[c] === undefined ? '' : cells[c];
    });
    // 合计行不参与明细逐行勾稽（它自己会被逐列复核）；任一单元格写作「合计」即认定
    const isTotal = cells.some((c) => TOTAL_WORDS.test(String(c).trim()));
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  if (!it) return '该行';
  const code = String(it.assetCode === undefined ? '' : it.assetCode).trim();
  const name = String(it.assetName === undefined ? '' : it.assetName).trim();
  const label = code || name || `第 ${it.line} 行`;
  const period = String(it.period === undefined ? '' : it.period).trim();
  return period ? `${period} ${label}` : label;
};

/* ================================ 免费档检查项 ================================ */

function checkImpairmentLoss(it) {
  const bv = normNumber(it.bookValue);
  const rec = normNumber(it.recoverable);
  const stated = normNumber(it.impairLoss);
  if (bv === null || rec === null || stated === null) return null;
  const expect = round2(Math.max(0, round2(bv - rec)));
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '减值损失复算不符', line: it.line,
    message: `${who(it)}：账面价值 ${bv.toFixed(2)} − 可收回金额 ${rec.toFixed(2)} = ${round2(bv - rec).toFixed(2)}`
      + `（差额为负按 0 计），应为 ${expect.toFixed(2)}，表里填的是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkProvisionBalance(it) {
  const open = normNumber(it.openProvision);
  const charge = normNumber(it.charge);
  const rev = normNumber(it.reversal);
  const close = normNumber(it.closeProvision);
  if (open === null || charge === null || rev === null || close === null) return null;
  const expect = round2(open + charge - rev);
  if (Math.abs(expect - close) <= TOL) return null;
  return {
    level: 'P0', category: '减值准备余额勾稽不符', line: it.line,
    message: `${who(it)}：期初 ${open.toFixed(2)} + 本期计提 ${charge.toFixed(2)} − 本期转回或处置 ${rev.toFixed(2)}`
      + ` = ${expect.toFixed(2)}，表里期末余额是 ${close.toFixed(2)}，相差 ${round2(close - expect).toFixed(2)}。`,
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const asset = String(it.assetCode === undefined ? '' : it.assetCode).trim()
      || String(it.assetName === undefined ? '' : it.assetName).trim();
    if (!asset) continue;
    const period = String(it.period === undefined ? '' : it.period).trim();
    const key = `${period}|${asset}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一资产出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经出现过，第 ${it.line} 行又出现一次 —— 减值损失与计提额会被重复计算。`,
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
  for (const role of AMOUNT_ROLES) {
    const v = normNumber(it[role]);
    if (v === null || v >= -TOL) continue;
    out.push({
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 冲回或处置请填在「本期转回或处置」列，金额列不应为负。`,
    });
  }
  return out;
}

/* ================= 完整档（付费）追加的检查：只在 paid 为真时执行 ================= */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到减值测试表正文（text）—— 请把「资产编号 / 账面价值 / 可收回金额 / 减值损失 / 减值准备」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `减值测试表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何资产明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkImpairmentLoss(it); if (a) findings.push(a);
    const b = checkProvisionBalance(it); if (b) findings.push(b);
    for (const x of checkNegatives(it)) findings.push(x);

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

  let lossTotal = 0;
  let closeTotal = 0;
  const periods = new Set();
  for (const it of t.items) {
    const a = normNumber(it.impairLoss); if (a !== null) lossTotal += a;
    const b = normNumber(it.closeProvision); if (b !== null) closeTotal += b;
    const p = String(it.period === undefined ? '' : it.period).trim();
    if (p) periods.add(p);
  }

  const result = {
    status: 'success',
    service_type: 'ASSET_IMPAIRMENT_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.size,
      impairment_loss_total: round2(lossTotal),
      provision_close_total: round2(closeTotal),
      rate_ref: RATE_REF,
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
    note: `本版本只执行 ${CHECKS_GIVEN.length} 项免费检查；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"账面价值 − 可收回金额 = 减值损失""期初 + 计提 − 转回 = 期末"这类内部勾稽，'
      + '**不规定可收回金额与折现率怎么定**（以评估报告与管理层判断为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
