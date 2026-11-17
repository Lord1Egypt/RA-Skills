/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * material-cost-variance-check.js —— 材料成本差异分摊核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**制造业成本会计每月结账前**。计划成本法下，
 * 「材料成本差异」科目要把当月（期初结存 + 本期收入）的差异，按**计划成本比例**
 * 在**发出材料**与**期末结存**之间分摊：
 *
 *   差异率             = 差异总额 ÷ 计划成本总额
 *   发出分摊差异额     = 发出金额 × 差异率
 *   结存分摊差异额     = 结存金额 × 差异率
 *   发出分摊 + 结存分摊 = 差异总额（差异要分完）
 *   发出金额 + 结存金额 = 计划成本总额（差异只能在这些计划成本之间分）
 *
 * 分摊率算错就是**成本与存货双错**：发出材料的成本记错 ⇒ 当期损益错；
 * 结存差异留错 ⇒ 存货与下月差异率一起错，月末结账过不去。
 * 这张表的每一格都能手算复现，所以"对不对"完全可以机械核出来。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**差异该按哪条口径分摊（那属于会计政策与职业判断）：只核表内勾稽
 *    （一个差异率、一次乘法、一次加总），口径一律以表里给的为准。
 * ⚠️ 差异额 / 分摊额**为负是正常的**（节约差异，即实际成本低于计划成本），
 *    所以"金额为负"只覆盖计划成本类的三列（计划成本总额 / 发出金额 / 结存金额）——
 *    把"差异为负"也报成错的工具会天天喊狼来了，用两次就没人信了。
 */

const CHECKS_GIVEN = [
  '差异分摊额 = 发出金额 × 差异率 复算',
  '差异率 = 差异总额 ÷ 计划成本总额 复算',
  '合计行逐列复核',
  '同一材料编码重复行检测',
  '空白与占位符检测',
  '金额为负检测（计划成本类三列）',
];

const CHECKS_WITHHELD = [
  '分摊额与差异率计算不符提示（结存分摊差异额）',
  '差异率超过参考区间（−20%~20%）提示',
  '分摊额合计与差异总额不符提示',
  '发出与结存分摊方向异常（同号）提示',
  '计划成本总额为零却有差异提示',
];

const OUT_OF_SCOPE = [
  '判断差异该按哪条口径分摊、差异率要不要分类（原材料/主要材料/全部材料）计算（那属于会计政策，请按企业会计制度与主管会计口径）',
  '核对总账「材料成本差异」科目余额与这张分摊表的期末余额是否一致、抽查记账凭证与原始单据',
  '重算计划成本单价、材料成本差异的发生额（那要读入库单、发票与计划价目录，本工具只核你贴进来的这张表）',
  '读取 ERP / 财务系统导出文件（需要你先导出成文本或 JSON 贴进来）',
];

const SAMPLE_TEXT = [
  '期间\t材料编码\t材料名称\t计划成本总额\t差异总额\t差异率\t发出金额\t发出分摊差异额\t结存金额\t结存分摊差异额',
  '2026-01\tM-1001\t冷轧钢板\t500000.00\t10000.00\t2%\t300000.00\t6000.00\t200000.00\t4000.00',
  '2026-01\tM-1002\t铝型材\t250000.00\t-5000.00\t-2%\t150000.00\t-3000.00\t100000.00\t-2000.00',
  '2026-01\tM-1003\t标准件\t125000.00\t2500.00\t2%\t75000.00\t1500.00\t50000.00\t1000.00',
  '合计\t\t\t875000.00\t7500.00\t\t525000.00\t4500.00\t350000.00\t3000.00',
].join('\n');

const TOL = 0.01;                            // 金额容差：1 分
const RATE_TOL = 0.0005;                     // 差异率容差：0.05 个百分点（写百分比时的四舍五入余量）

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前。
  //    「发出分摊差异额」不能被「发出金额」或「差异额」抢走，「结存金额」不能被「结存」抢走，
  //    「材料成本差异率」不能被「材料成本差异」抢走 —— 顺序一错就是**整列错认**（不报缺列，只算错）。
  period: ['期间', '会计期间', '月份', '月度', '所属期'],
  code: ['材料编码', '物料编码', '存货编码', '材料编号', '物料编号', '编码'],
  name: ['材料名称', '物料名称', '存货名称', '品名', '名称'],
  issuedAlloc: ['发出分摊差异额', '发出差异分摊额', '发出应分摊差异额', '发出分摊差异', '发出分摊额'],
  balanceAlloc: ['结存分摊差异额', '结存差异分摊额', '结存应分摊差异额', '期末分摊差异额', '期末结存分摊差异额', '结存分摊额'],
  issued: ['发出金额', '发出材料计划成本', '发出计划成本', '本月发出金额', '发出材料成本'],
  balance: ['结存金额', '期末结存金额', '结存计划成本', '期末结存计划成本', '结存材料成本'],
  planTotal: ['计划成本总额', '计划成本合计', '计划成本小计', '计划成本', '计划金额'],
  rate: ['材料成本差异率', '差异率', '分摊率', '差异分摊率'],
  varianceTotal: ['差异总额', '差异合计', '差异小计', '材料成本差异', '差异额', '差异金额'],
};

const LABELS = {
  period: '期间', code: '材料编码', name: '材料名称', planTotal: '计划成本总额',
  varianceTotal: '差异总额', rate: '差异率', issued: '发出金额', issuedAlloc: '发出分摊差异额',
  balance: '结存金额', balanceAlloc: '结存分摊差异额',
};

/** 少一列就算不出勾稽 ⇒ 材料不足（`name` 只是叫法，缺了不影响算术，所以不算必需列） */
const REQUIRED = ['code', 'planTotal', 'varianceTotal', 'rate', 'issued', 'issuedAlloc', 'balance', 'balanceAlloc'];
/** 合计行逐列复核覆盖的列（差异率是比例，不求和） */
const SUM_ROLES = ['planTotal', 'varianceTotal', 'issued', 'issuedAlloc', 'balance', 'balanceAlloc'];
/** 金额为负检测覆盖的列：**只有计划成本类三列**（差异/分摊为负 = 节约差异，是正常方向） */
const NON_NEGATIVE_ROLES = ['planTotal', 'issued', 'balance'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|全年合计)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|xx|\?+)$/i.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()【】\[\]]/g, '');
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

/** 比率归一化成小数：`2%` ⇒ 0.02；`0.02` ⇒ 0.02；`2` ⇒ 0.02；`-2%` ⇒ -0.02 */
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
      if ((role === 'period' || role === 'code' || role === 'name')
        && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const p = it && it.period !== undefined && String(it.period).trim() !== ''
    ? String(it.period).trim() : `第 ${it && it.line} 行`;
  const c = it && it.code !== undefined && String(it.code).trim() !== '' ? String(it.code).trim() : '';
  const n = it && it.name !== undefined && String(it.name).trim() !== '' ? String(it.name).trim() : '';
  const label = c && n ? `${c}「${n}」` : (c || (n ? `「${n}」` : ''));
  return label ? `${p} ${label}` : p;
};

/** 同一材料编码的判重口径是**同一期间内**；表里没有期间列时，整张表算一个期间 */
const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || '（未填期间）';
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkIssuedAllocRecompute(it) {
  const out = [];
  const issued = normNumber(it.issued);
  const rate = rateValue(it.rate);
  const stated = normNumber(it.issuedAlloc);
  if (issued === null || rate === null || stated === null) return out;
  const expect = round2(issued * rate);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '发出分摊额与复算不符', line: it.line,
    message: `${who(it)}：发出金额 ${issued.toFixed(2)} × 差异率 ${(rate * 100).toFixed(4)}% = ${expect.toFixed(2)}，`
      + `表里「发出分摊差异额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)} —— `
      + '发出材料应负担的差异就是这一笔乘法，算错直接进当期成本。',
  });
  return out;
}

function checkRateRecompute(it) {
  const out = [];
  const stated = rateValue(it.rate);
  const plan = normNumber(it.planTotal);
  const variance = normNumber(it.varianceTotal);
  if (stated === null || plan === null || variance === null) return out;
  if (Math.abs(plan) <= TOL) return out;      // 计划成本为零：差异率无从算起（完整档单独提示）
  const expect = variance / plan;
  if (Math.abs(stated - expect) <= RATE_TOL) return out;
  out.push({
    level: 'P0', category: '差异率与复算不符', line: it.line,
    message: `${who(it)}：差异总额 ${variance.toFixed(2)} ÷ 计划成本总额 ${plan.toFixed(2)} = ${(expect * 100).toFixed(4)}%，`
      + `表里「差异率」是 ${(stated * 100).toFixed(4)}%，差 ${(Math.abs(stated - expect) * 100).toFixed(4)} 个百分点`
      + `（容差 ${(RATE_TOL * 100).toFixed(2)} 个百分点）—— 整列分摊额都是照这个率算的，率错则全错。`,
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
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，本表 ${n} 行明细相加是 ${expect.toFixed(2)}，`
        + `相差 ${round2(stated - expect).toFixed(2)} —— 合计行就是各明细之和，两者必须相等。`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const c = it.code !== undefined ? String(it.code).trim() : '';
    if (!c) continue;
    const key = `${periodKeyOf(it)}|${c}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一材料编码出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— `
          + '同一期间同一材料编码只能有一行，重复行会让这笔差异被分摊两次（发出与结存都虚增）。',
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）—— `
            + '分摊勾稽缺任何一格都算不出结果，不能用"没填"当 0。',
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NON_NEGATIVE_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    out.push({
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 计划成本类的金额不该为负；`
        + '节约差异应记在差异列，冲回应单独列示。',
    });
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
    return insufficient('没有收到材料成本差异分摊核对表正文（text）—— 请把「期间 / 材料编码 / 材料名称 / 计划成本总额 / 差异总额 / 差异率 / 发出金额 / 发出分摊差异额 / 结存金额 / 结存分摊差异额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `材料成本差异分摊核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何材料明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkIssuedAllocRecompute(it));
    findings.push(...checkRateRecompute(it));
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

  let planTotal = 0;
  let varianceTotal = 0;
  let issuedAllocTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.planTotal);
    const b = normNumber(it.varianceTotal);
    const c = normNumber(it.issuedAlloc);
    if (a !== null) planTotal += a;
    if (b !== null) varianceTotal += b;
    if (c !== null) issuedAllocTotal += c;
  }

  const result = {
    status: 'success',
    service_type: 'MATERIAL_COST_VARIANCE_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      plan_cost_total: round2(planTotal),
      variance_total: round2(varianceTotal),
      issued_alloc_total: round2(issuedAllocTotal),
      tolerance: TOL,
      rate_tolerance: RATE_TOL,
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
    disclaimer: '只核"差异率 = 差异总额 ÷ 计划成本总额""发出分摊 = 发出金额 × 差异率"这类**表内勾稽**与档位提示，'
      + '**不判断差异该按哪条口径分摊**（以企业会计政策与主管会计口径为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT,
};
