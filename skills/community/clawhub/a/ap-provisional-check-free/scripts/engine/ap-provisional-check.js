#!/usr/bin/env node
'use strict';
/**
 * ap-provisional-check.js —— 应付暂估与发票未到核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**每家公司月末结账必做**的一步 —— 货到票未到先暂估入账，发票到了再冲回暂估、按票入账。
 * 台账里就三条串行关系：
 *   ① 暂估入账金额 = 数量 × 单价
 *   ② 暂估与发票差异 = 发票金额 − 暂估入账金额
 *   ③ 本期暂估余额 = 上期暂估余额 + 本期暂估 − 本期冲回
 * 算式是纯算术，但**跨月**就出事：发票到了忘了冲（已到票未冲）、没到票先冲了（已冲未到票）、
 * 差异不调整、同一合同重复暂估、暂估余额与应付账款明细对不上 —— 发票后到冲回错一次就长期挂账，
 * 暂估不准会让成本与利润一起失真。
 *
 * 与已有能力的区别：`accrual-expense-check` 核的是**费用类预提**（预提费用与到票冲销、按项目/月份口径）；
 * 本能力核的是**存货/采购类的应付暂估台账**（按暂估单 + 合同 + 数量×单价口径，核到暂估余额与应付明细勾稽）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查价目表、不调用大模型；材料不足不给结论；不给会计/审计意见。
 */

const CHECKS_GIVEN = [
  '暂估入账金额勾稽（暂估入账金额 = 数量 × 单价）',
  '冲回金额与暂估金额勾稽（本期冲回不得超过本期暂估）',
  '暂估与发票差异勾稽（差异 = 发票金额 − 暂估入账金额）',
  '暂估余额勾稽（本期暂估余额 = 上期暂估余额 + 本期暂估 − 本期冲回）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复暂估单号检测',
  '关键字段空缺与占位符检测（含已到票却缺发票金额）',
  '金额为负检测',
  '跨期标记缺失检测（已到票标记未填或认不出）',
];

const CHECKS_WITHHELD = [
  '已到票未冲判定（含自暂估所属期起的挂账月数）',
  '已冲回但无对应发票判定（已冲未到票）',
  '暂估与发票差异未调整判定（含需处理金额）',
  '同一合同同一期间重复暂估判定',
  '暂估余额与应付账款明细勾稽（不符判定）',
  '长期挂账呆滞暂估判定（未到票且挂账超过 3 期）',
];

const OUT_OF_SCOPE = [
  '判断该不该暂估、暂估单价与数量定得对不对（那是业务与合同判断）',
  '判断发票真伪、能否抵扣或税前扣除（那是发票合规与税务的事）',
  '处理暂估成本的结转与存货/成本科目分摊',
  '给出会计或审计意见；读取 .xlsx（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '暂估单号\t合同号\t暂估所属期\t数量\t单价\t暂估入账金额\t已到票\t发票金额\t到票月份\t本期冲回金额\t上期暂估余额\t本期暂估余额\t应付明细暂估余额\t暂估与发票差异',
  'ZG2026010001\tHT-2025-011\t2026-01\t100\t120.00\t12000.00\t否\t—\t—\t0.00\t0.00\t12000.00\t12000.00\t—',
  'ZG2026010002\tHT-2025-012\t2026-01\t50\t80.00\t4000.00\t是\t4000.00\t2026-01\t4000.00\t0.00\t0.00\t0.00\t0.00',
  'ZG2026010003\tHT-2025-013\t2026-01\t200\t35.50\t7100.00\t是\t7100.00\t2026-02\t7100.00\t0.00\t0.00\t0.00\t0.00',
  'ZG2026010004\tHT-2025-014\t2026-01\t40\t250.00\t10000.00\t否\t—\t—\t0.00\t0.00\t10000.00\t10000.00\t—',
  '合计\t—\t—\t390\t—\t33100.00\t—\t11100.00\t—\t11100.00\t0.00\t22000.00\t22000.00\t0.00',
].join('\n');

const TOL = 0.01;

// ⚠️ 更具体的关键词必须排在更宽泛的前面，否则宽泛的别名会把更具体的列抢走
//    （本仓库踩过两次：`期末欠租` 被 `欠租` 抢、`本期摊销月数` 被 `摊销月数` 抢）：
//    「到票月份」必须排在「暂估所属期/期间/月份」前；「应付明细暂估余额」必须排在「暂估余额」前；
//    「上期暂估余额」必须排在「暂估余额」前。
const ROLES = {
  doc: ['暂估单号', '暂估编号', '暂估凭证号', '单号'],
  contract: ['合同号', '合同编号', '采购合同号'],
  invoiceMonth: ['到票月份', '发票到达月份', '到票所属期', '到票期间'],
  period: ['暂估所属期', '暂估期间', '所属期', '期间', '月份'],
  invoiced: ['已到票', '到票标记', '是否到票', '发票是否到达'],
  qty: ['暂估数量', '数量'],
  price: ['暂估单价', '单价'],
  provision: ['暂估入账金额', '本期暂估金额', '暂估金额', '暂估额'],
  invoice: ['发票金额', '到票金额', '不含税发票金额'],
  reverse: ['本期冲回金额', '冲回金额', '冲销金额', '本期冲回'],
  balanceStart: ['上期暂估余额', '期初暂估余额', '上期余额', '期初余额'],
  apDetail: ['应付明细暂估余额', '应付账款明细暂估余额', '应付明细余额', '明细账余额'],
  balanceEnd: ['本期暂估余额', '期末暂估余额', '暂估余额', '本期余额', '期末余额'],
  diff: ['暂估与发票差异', '发票与暂估差异', '差异金额', '差异额', '差异'],
};

const LABELS = {
  doc: '暂估单号', contract: '合同号', invoiceMonth: '到票月份', period: '暂估所属期',
  invoiced: '已到票', qty: '数量', price: '单价', provision: '暂估入账金额',
  invoice: '发票金额', reverse: '本期冲回金额', balanceStart: '上期暂估余额',
  apDetail: '应付明细暂估余额', balanceEnd: '本期暂估余额', diff: '暂估与发票差异',
};

const REQUIRED = ['doc', 'contract', 'invoiceMonth', 'period', 'invoiced', 'qty', 'price',
  'provision', 'invoice', 'reverse', 'balanceStart', 'apDetail', 'balanceEnd', 'diff'];
// 逐格必须填的列（发票金额/到票月份/差异在"未到票"的行里本来就该空着，交给各自的语义检查）
const BLANK_ROLES = ['doc', 'period', 'qty', 'price', 'provision', 'reverse',
  'balanceStart', 'balanceEnd', 'apDetail'];
const SUM_ROLES = ['qty', 'provision', 'invoice', 'reverse', 'balanceStart', 'balanceEnd', 'apDetail', 'diff'];

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

const FLAG_TRUE = /^(是|有|y|yes|true|1|已到票|已到|已收票|已开票)$/i;
const FLAG_FALSE = /^(否|无|n|no|false|0|未到|未到票|未收票|未开票)$/i;

/** 把「已到票」列读成 true/false；空白、占位符、认不出的写法一律返回 null（**不猜**） */
function normFlag(raw) {
  const s = String(raw === undefined || raw === null ? '' : raw).trim();
  if (FLAG_TRUE.test(s)) return true;
  if (FLAG_FALSE.test(s)) return false;
  return null;
}

/** '2026-01' / '2026/1' / '2026年1月' -> 以"月"为单位的序号；认不出返回 null */
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
      row.isTotal = true;
      totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals };
}

const num = (it, role) => normNumber(it.byRole[role]);
const who = (it) => {
  const d = String(it.byRole.doc === undefined ? '' : it.byRole.doc).trim() || '(未命名单号)';
  const p = String(it.byRole.period === undefined ? '' : it.byRole.period).trim() || '(未填期间)';
  return `暂估单「${d}」（${p}）`;
};

/* ================= 免费档检查（逐行复算 + 合计 + 重复 + 空缺/负值/跨期标记） ================= */

function checkProvisionAmount(it) {
  const qty = num(it, 'qty');
  const price = num(it, 'price');
  const stated = num(it, 'provision');
  if (qty === null || price === null || stated === null) return null;
  const expect = round2(qty * price);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '暂估金额与复算不符', line: it.line,
    message: `${who(it)}的暂估入账金额是 ${stated.toFixed(2)}，`
      + `按 数量 ${qty} × 单价 ${price.toFixed(2)} 应为 ${expect.toFixed(2)}（相差 ${round2(stated - expect).toFixed(2)}）。`,
    advice: '暂估金额必须等于数量 × 暂估单价（合同价/采购单口径）；单价用错或漏摊运费都反映在这里。',
  };
}

function checkReverseOver(it) {
  const provision = num(it, 'provision');
  const reverse = num(it, 'reverse');
  if (provision === null || reverse === null) return null;
  if (reverse <= provision + TOL) return null;
  return {
    level: 'P0', category: '冲回金额超过暂估金额', line: it.line,
    message: `${who(it)}的本期冲回金额是 ${reverse.toFixed(2)}，大于本期暂估入账金额 ${provision.toFixed(2)}，`
      + `多冲了 ${round2(reverse - provision).toFixed(2)}。`,
    advice: '一笔暂估最多被冲回一次；冲回超过暂估通常是重复冲回，或把别的单冲到了这一行。',
  };
}

function checkDiff(it) {
  const invoice = num(it, 'invoice');
  const provision = num(it, 'provision');
  const stated = num(it, 'diff');
  if (invoice === null || provision === null || stated === null) return null;
  const expect = round2(invoice - provision);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P1', category: '差异与复算不符', line: it.line,
    message: `${who(it)}的暂估与发票差异填的是 ${stated.toFixed(2)}，`
      + `按 发票金额 ${invoice.toFixed(2)} − 暂估入账金额 ${provision.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '差异＝发票金额−暂估金额（同口径，都按不含税）；差异填错会让后续调整金额跟着错。',
  };
}

function checkRollforward(it) {
  const start = num(it, 'balanceStart');
  const provision = num(it, 'provision');
  const reverse = num(it, 'reverse');
  const stated = num(it, 'balanceEnd');
  if (start === null || provision === null || reverse === null || stated === null) return null;
  const expect = round2(start + provision - reverse);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '暂估余额与复算不符', line: it.line,
    message: `${who(it)}的本期暂估余额是 ${stated.toFixed(2)}，`
      + `按 上期暂估余额 ${start.toFixed(2)} + 本期暂估 ${provision.toFixed(2)} − 本期冲回 ${reverse.toFixed(2)} `
      + `应为 ${expect.toFixed(2)}（相差 ${round2(stated - expect).toFixed(2)}）。`,
    advice: '余额＝上期余额＋本期暂估−本期冲回；这条链断了，暂估余额会一直挂着、与总账长期差口。',
  };
}

function checkNegative(it) {
  const out = [];
  for (const role of ['provision', 'invoice', 'reverse', 'balanceStart', 'balanceEnd', 'apDetail']) {
    const v = num(it, role);
    if (v !== null && v < -TOL) {
      out.push({
        level: 'P0', category: '金额为负', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}。`,
        advice: '这几列按口径都不该是负数（红字冲回请在备注说明）；负数多半是方向填反或把借贷写混。',
      });
    }
  }
  return out;
}

function checkMarkerMissing(it) {
  const raw = it.byRole.invoiced;
  if (normFlag(raw) !== null) return null;
  const shown = isBlank(raw) ? '空' : String(raw).trim();
  return {
    level: 'P1', category: '已到票标记缺失', line: it.line,
    message: `${who(it)}的「已到票」是${shown}，认不出"已到票 / 未到票"，这一行的跨期状态无法判断。`,
    advice: '这一列只填 是 / 否；填不出时本工具不会替你猜（猜错会把跨期结论带偏）。',
  };
}

function checkInvoiceAmountMissing(it) {
  const flag = normFlag(it.byRole.invoiced);
  if (flag !== true) return null;
  if (num(it, 'invoice') !== null) return null;
  return {
    level: 'P0', category: '已到票但发票金额空缺', line: it.line,
    message: `${who(it)}标了已到票，但「发票金额」是空的 —— 冲回金额和差异都算不出来。`,
    advice: '把发票上的不含税金额补上；缺这一格时本工具不会用 0 或默认值替你填。',
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
        advice: '要么明细行漏了一笔暂估单，要么合计行没跟着更新。',
      });
    }
  }
  return out;
}

function checkDuplicateDoc(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.doc === undefined ? '' : it.byRole.doc).trim();
    if (!key || isBlank(key)) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '暂估单号重复出现', line: it.line,
        message: `暂估单号「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行又出现一次。`,
        advice: '同一张暂估单只能入账一次；若你要在两张表里分别登记暂估与冲回，请用「-冲」后缀区分单号。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd)$/i;

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of BLANK_ROLES) {
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (isBlank(s) || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这笔暂估就算不出来；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
  }
  return out;
}

/* ======== 以下只由付费档（paid 开关块）调用的检查：跨期与呆滞判定 + 结账前处理清单 ======== */

/** 结账前处理清单：把带金额的判定按金额从大到小排（每条带行号与建议动作） */
function run(payload) {
  const p = payload || {};
  const text = p.text || p.content || '';
  if (!String(text).trim()) {
    return insufficient(['原文（text）：把应付暂估台账的表头和数据行一起粘进来']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：把应付暂估台账的表头和数据行一起粘进来']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的应付暂估台账（要能认出「暂估单号」「合同号」「暂估所属期」「数量」「单价」'
      + '「暂估入账金额」「已到票」「发票金额」「到票月份」「本期冲回金额」「上期暂估余额」'
      + '「本期暂估余额」「应付明细暂估余额」「暂估与发票差异」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从台账或 Excel 导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行暂估明细（只有合计行算不出任何东西）']);
  }

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkProvisionAmount(it); if (a) findings.push(a);
    const b = checkReverseOver(it); if (b) findings.push(b);
    const c = checkDiff(it); if (c) findings.push(c);
    const d = checkRollforward(it); if (d) findings.push(d);
    for (const f of checkNegative(it)) findings.push(f);
    const g = checkMarkerMissing(it); if (g) findings.push(g);
    const h = checkInvoiceAmountMissing(it); if (h) findings.push(h);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicateDoc(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));
  const checksExecuted = CHECKS_GIVEN;

  const result = {
    findings,
    actions: [],
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      provisional_total: sumOf('provision'),
      invoice_total: sumOf('invoice'),
      reverse_total: sumOf('reverse'),
      outstanding_total: sumOf('balanceEnd'),
      basis: '暂估入账金额 = 数量 × 单价；暂估与发票差异 = 发票金额 − 暂估入账金额；'
        + '本期暂估余额 = 上期暂估余额 + 本期暂估 − 本期冲回；合计行逐列复核。',
    },
    scope: {
      rows: t.items.length,
      checks_executed: checksExecuted,
      checks_not_run: notRun,
      provisional_total: sumOf('provision'),
      outstanding_total: sumOf('balanceEnd'),
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_executed: checksExecuted,
    checks_withheld: CHECKS_WITHHELD,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的口径算得对**，'
      + '不代表这些暂估该不该做、单价数量定得对不对 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, normFlag, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, ROLES, REQUIRED, BLANK_ROLES, SUM_ROLES,
};
