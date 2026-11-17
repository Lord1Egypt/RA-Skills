'use strict';
/**
 * audit-adjustment-check.js —— 审计调整分录核对（**免费档**；完整档实现不在本包）
 *
 * 谁在什么时候必须做这件事：**年审期间**，审计师把调整分录建议（审计调整）交给财务，
 * 财务逐条落到账上 —— 两方来回核对的就是这张**审计调整分录核对表**。
 * 这张表错一行，报表就是错的；而它错不错**完全能用算术复算出来**：
 *
 *   ① 借贷必须平衡：同一调整事项 Σ借方 = Σ贷方（借贷差额 = 借方合计 − 贷方合计，必须为 0）；
 *   ② 每一行的科目净影响 = 借方金额 − 贷方金额；
 *   ③ 合计行 = 各明细行逐列相加；
 *   ④ 同一调整事项不许有重复行、同一科目同一事项不许重复调整（完整档）；
 *   ⑤ 关键字段不许空着或用占位符，借贷两列不许出现负数（红字请单独列示）。
 *
 * 本工具只做**算术与字符串核对**：不判断会计处理是否正确、不规定重要性水平与科目方向
 * （以审计计划、企业会计准则与审计师意见为准），也不调用任何大模型、不联网。
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 *
 * 契约（所有引擎一致，别改名字）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *   CHECKS_GIVEN / CHECKS_WITHHELD     免费档执行 / 不执行的检查项（免费包据此如实列出未执行项）
 *   OUT_OF_SCOPE                       本能力根本不做的事（边界诚实）
 *   SAMPLE_TEXT                        样例输入（两档都必须 0 命中）
 *
 * ⚠️ 检查函数**形状只有一种**：统一返回「发现数组」（没问题就是空数组），
 *    绝不混用 null / undefined / 单对象 —— 调用方与测试都不用分叉。
 * ⚠️ 表的口径（写死在解析里，SAMPLE_TEXT 就是它）：
 *    · 一行 = 一条调整分录的一个科目（借方或贷方一侧）；
 *    · 「借贷差额」是**事项级**属性（= 该事项 借方合计 − 贷方合计），在同一事项的某一行填一次即可，
 *      因此它**不参与合计行逐列复核**（逐行重复填的值不能相加）；
 *      「科目净影响」是**行级**属性（= 本行 借方 − 贷方），合计行照常复核。
 * ⚠️ 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 *    **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 */

const CHECKS_GIVEN = [
  '借贷差额复算（借贷差额 = 借方合计 − 贷方合计，必须为 0）',
  '科目净影响复算（借方金额 − 贷方金额 = 科目净影响）',
  '合计行逐列复核',
  '同一调整事项重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '借贷不平超过容差提示',
  '调整事项缺说明或编号提示',
  '同一科目同一事项重复调整提示',
  '调整金额超过参考重要性水平提示（参考口径）',
  '调整后科目方向异常（资产类为负）提示',
];

const OUT_OF_SCOPE = [
  '判断调整分录的会计处理是否正确、科目使用是否符合企业会计准则（以审计师意见与准则为准）',
  '判断某笔调整是否应当调整、是否属于期后事项、是否需要披露',
  '规定重要性水平、会计政策与科目方向（以本项目审计计划与本单位会计政策为准）',
  '核对调整分录与审计底稿、报表附注之间的对应关系（需要你另外提供底稿）',
  '读取财务系统或审计软件导出的文件（需要你先导出成文本贴进来）',
];

/* 参考重要性水平（元）：只对"明显超过"做**提示**，不是口径，也不参与任何认定 */
const MATERIALITY_REF = 1000000;

const TOL = 0.01;

const SAMPLE_TEXT = [
  '调整事项编号\t调整事项说明\t科目编码\t科目名称\t科目类别\t借方金额\t贷方金额\t借贷差额\t科目净影响\t调整依据',
  'A-01\t补记跨期销售收入\t1122\t应收账款\t资产类\t113000.00\t0.00\t0.00\t113000.00\t审计调整 A-01：收入截止性测试',
  'A-01\t补记跨期销售收入\t6001\t主营业务收入\t损益类\t0.00\t100000.00\t\t-100000.00\t审计调整 A-01：收入截止性测试',
  'A-01\t补记跨期销售收入\t2221\t应交税费\t负债类\t0.00\t13000.00\t\t-13000.00\t审计调整 A-01：收入截止性测试',
  'B-01\t补提年度审计费用\t6602\t管理费用\t损益类\t20000.00\t0.00\t0.00\t20000.00\t审计调整 B-01：未入账费用',
  'B-01\t补提年度审计费用\t2241\t其他应付款\t负债类\t0.00\t20000.00\t\t-20000.00\t审计调整 B-01：未入账费用',
  '合计\t\t\t\t\t133000.00\t133000.00\t0.00\t0.00\t',
].join('\n');

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前（「科目净影响」不能被「科目名称/科目」抢走，
  //    「科目编码」「科目类别」必须在「科目」之前）。
  itemNo: ['调整事项编号', '调整事项号', '事项编号', '分录编号', '调整编号', '编号'],
  itemDesc: ['调整事项说明', '调整事项摘要', '事项说明', '调整事由', '调整事项', '摘要'],
  accountCode: ['会计科目编码', '科目编码', '科目代码', '科目号'],
  accountType: ['科目类别', '科目类型', '科目性质'],
  netEffect: ['科目净影响', '净影响额', '净影响', '净额'],
  accountName: ['会计科目名称', '科目名称', '会计科目', '科目'],
  debit: ['借方金额', '借方发生额', '借方合计', '借方'],
  credit: ['贷方金额', '贷方发生额', '贷方合计', '贷方'],
  diff: ['借贷差额', '借贷差', '差额'],
  basis: ['调整依据', '调整理由', '调整说明', '依据', '备注'],
};

const LABELS = {
  itemNo: '调整事项编号', itemDesc: '调整事项说明', accountCode: '科目编码',
  accountName: '科目名称', accountType: '科目类别', debit: '借方金额',
  credit: '贷方金额', diff: '借贷差额', netEffect: '科目净影响', basis: '调整依据',
};

/* 必需列：缺任何一列 → 材料不足（不给结论，也不套默认值） */
const REQUIRED = ['itemNo', 'itemDesc', 'accountName', 'debit', 'credit'];
/* 合计行逐列复核的列：借贷差额是事项级属性，逐行重复填，不参与求和 */
const SUM_ROLES = ['debit', 'credit', 'netEffect'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|合计金额|合计数)$/;

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

/** 空 / 破折号 / 占位符都算"没填"（`-` 在金额列里通常就是"这一侧没有金额"） */
function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
}

/** 明确写着"还没填"的字样 —— 这种要**响亮地**报出来，不能被当成 0 静默算过去 */
function isPlaceholder(v) {
  if (v === undefined || v === null) return false;
  return /^(n\/?a|无|待填|待补|待定|未知|不详)$/i.test(String(v).trim());
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

const round2 = (n) => Math.round(n * 100) / 100;
const money = (n) => round2(n).toFixed(2);

/** 事项分组键：有编号按编号，没有编号的行各自算一个事项（绝不把不同事项混成一组） */
function groupKey(it) {
  const no = it.itemNo === undefined || it.itemNo === null ? '' : String(it.itemNo).trim();
  return no || `\u0000第${it.line}行`;
}

/** 科目键：优先科目编码，没有编码就用科目名称 */
function accountKey(it) {
  const code = it.accountCode === undefined || it.accountCode === null ? '' : String(it.accountCode).trim();
  if (code) return code;
  const name = it.accountName === undefined || it.accountName === null ? '' : String(it.accountName).trim();
  return name;
}

function groupByItems(items) {
  const m = new Map();
  for (const it of items) {
    const k = groupKey(it);
    if (!m.has(k)) m.set(k, []);
    m.get(k).push(it);
  }
  return m;
}

const who = (it) => {
  const no = it.itemNo === undefined || it.itemNo === null ? '' : String(it.itemNo).trim();
  const name = it.accountName === undefined || it.accountName === null ? '' : String(it.accountName).trim();
  const tag = no ? `${no} 事项` : `第 ${it.line} 行`;
  return name ? `${tag}（${name}）` : tag;
};

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null, headers: [] };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const known = roles.filter(Boolean);
  const missingColumns = REQUIRED.filter((r) => known.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  const totals = {};
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i] };
    let isTotal = false;
    roles.forEach((role, c) => {
      if (!role) return;
      const v = cells[c] === undefined ? '' : cells[c];
      row[role] = v;
      if ((role === 'itemNo' || role === 'accountName') && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns, headers };
}

/* ================================ 免费档检查项 ================================ */
/* 约定：每条检查函数都返回**发现数组**（没有发现就是空数组） */

/** ① 借贷差额复算：表里填的「借贷差额」必须等于 借方合计 − 贷方合计（事项级，每个事项只报一次） */
function checkEntryDiff(group) {
  const carriers = group.filter((r) => normNumber(r.diff) !== null);
  if (!carriers.length) return [];
  let d = 0;
  let c = 0;
  for (const r of group) {
    const a = normNumber(r.debit); if (a !== null) d += a;
    const b = normNumber(r.credit); if (b !== null) c += b;
  }
  d = round2(d); c = round2(c);
  const expect = round2(d - c);
  const bad = carriers.filter((r) => Math.abs(normNumber(r.diff) - expect) > TOL);
  if (!bad.length) return [];
  const stated = normNumber(bad[0].diff);
  return [{
    level: 'P0', category: '借贷差额与复算不符', line: bad[0].line,
    message: `${who(bad[0])}：表里「借贷差额」填的是 ${money(stated)}（共 ${bad.length} 行这样填），`
      + `按本事项各行复算 借方合计 ${money(d)} − 贷方合计 ${money(c)} = ${money(expect)}，`
      + `相差 ${money(stated - expect)}。`,
  }];
}

/** ② 科目净影响复算：每一行 借方金额 − 贷方金额 = 科目净影响 */
function checkNetEffect(it) {
  const d = normNumber(it.debit);
  const c = normNumber(it.credit);
  const net = normNumber(it.netEffect);
  if (d === null || c === null || net === null) return [];
  const expect = round2(d - c);
  if (Math.abs(net - expect) <= TOL) return [];
  return [{
    level: 'P0', category: '科目净影响与复算不符', line: it.line,
    message: `${who(it)}：借方 ${money(d)} − 贷方 ${money(c)} 应为 ${money(expect)}，`
      + `表里「科目净影响」填的是 ${money(net)}，相差 ${money(net - expect)}。`,
  }];
}

/** ⑥ 金额为负：借方/贷方列出现负数（红字冲销请单独列示，别与正常分录混在一起） */
function checkNegativeAmount(it) {
  const out = [];
  const d = normNumber(it.debit);
  const c = normNumber(it.credit);
  if (d !== null && d < -TOL) {
    out.push({
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「借方金额」是 ${money(d)}（负数）—— 红字冲销请单独列示，避免与正常分录混在一起。`,
    });
  }
  if (c !== null && c < -TOL) {
    out.push({
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「贷方金额」是 ${money(c)}（负数）—— 红字冲销请单独列示，避免与正常分录混在一起。`,
    });
  }
  return out;
}

/** ⑤ 空白与占位符：编号/科目名称空着，或借贷两列都没填，或金额列写着"待填"之类 */
function checkBlankCells(it) {
  const out = [];
  const push = (role, why) => {
    const raw = it[role] === undefined || it[role] === null ? '' : String(it[role]).trim();
    out.push({
      level: 'P0', category: '关键字段缺失或占位符', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」${why}（当前值：${raw === '' ? '空' : raw}）`
        + ' —— 空着或占位符会让这条分录核不了，请回到原始表补齐。',
    });
  };
  if (it.itemNo !== undefined && isBlank(it.itemNo)) push('itemNo', '是空的或占位符');
  if (it.accountName !== undefined && isBlank(it.accountName)) push('accountName', '是空的或占位符');
  if (isBlank(it.debit) && isBlank(it.credit)) push('debit', '和「贷方金额」两列都没填（一条分录不可能借贷两侧都没有金额）');
  for (const role of ['debit', 'credit', 'diff', 'netEffect']) {
    if (it[role] !== undefined && isPlaceholder(it[role])) push(role, '是占位符（还没填）');
  }
  return out;
}

/** ③ 合计行逐列复核：合计行 = 各明细行逐列相加（借贷差额是事项级属性，不参与） */
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
    message: `合计行的「${LABELS[role]}」是 ${money(stated)}，各明细行相加是 ${money(sum)}`
      + `（共 ${n} 行），相差 ${money(stated - sum)}。`,
  });
  return out;
}

/** ④ 同一调整事项重复行：事项、科目、借贷金额、净影响完全一样的两行 = 重复录入 */
function checkDuplicateRows(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = [
      groupKey(it), accountKey(it), normNumber(it.debit), normNumber(it.credit),
      normNumber(it.netEffect), String(it.itemDesc === undefined ? '' : it.itemDesc).trim(),
    ].join('|');
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一调整事项重复行', line: it.line,
        message: `${who(it)}与第 ${seen.get(key)} 行**完全相同**（事项、科目、借贷金额、净影响都一致）`
          + ' —— 分录被重复录入，调整会被算两次。',
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** 借贷不平超过容差：同一调整事项 借方合计 与 贷方合计 不相等（不平衡的分录不能过账） */
/** 调整事项缺说明或编号：说明是"影响科目与金额必须与调整事项一致"的唯一依据 */
/** 同一科目同一事项重复调整：同一事项下同一科目被调整了多次（金额不同也要先确认） */
/** 调整金额超过参考重要性水平：只做**提示**，参考值不是口径 */
/** 调整后科目方向异常（资产类为负）：除备抵科目外，资产类科目调整后不应为贷方净影响 */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text
    : (payload && typeof payload.content === 'string' ? payload.content : '');
  if (text.trim().length < 5) {
    return insufficient('没有收到核对表正文（text）—— 请把「调整事项编号 / 调整事项说明 / 科目名称 / 借方金额 / 贷方金额」'
      + '这张表连同表头一起贴进来（Tab 分隔最稳）');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${(t.headers || []).join(' / ') || '(读不出表头)'}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或只有合计行），没有任何调整分录明细行');
  }

  const groups = groupByItems(t.items);
  const findings = [];
  for (const it of t.items) {
    const g = groups.get(groupKey(it)) || [it];
    if (g[0] === it) {
      for (const f of checkEntryDiff(g)) findings.push(f);
    }
    for (const f of checkNetEffect(it)) findings.push(f);
    for (const f of checkNegativeAmount(it)) findings.push(f);
    for (const f of checkBlankCells(it)) findings.push(f);

  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicateRows(t.items)) findings.push(f);


  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let debitTotal = 0;
  let creditTotal = 0;
  let netTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.debit); if (a !== null) debitTotal += a;
    const b = normNumber(it.credit); if (b !== null) creditTotal += b;
    const n = normNumber(it.netEffect); if (n !== null) netTotal += n;
  }

  const absent = ['accountCode', 'accountType', 'diff', 'netEffect', 'basis']
    .filter((r) => !t.items.some((it) => it[r] !== undefined)).map((r) => LABELS[r]);

  const result = {
    status: 'success',
    service_type: 'AUDIT_ADJUSTMENT_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      debit_total: round2(debitTotal),
      credit_total: round2(creditTotal),
      net_effect_total: round2(netTotal),
      columns_absent: absent,
      materiality_ref: MATERIALITY_REF,
      tolerance: TOL,
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
    disclaimer: '只核"借贷差额 = 借方合计 − 贷方合计""借方 − 贷方 = 科目净影响""合计行 = 各明细行之和"'
      + '这类**内部勾稽**，以及重复、空白、负数；**不判断会计处理是否正确，也不规定重要性水平与科目方向**'
      + '（以审计计划、企业会计准则与审计师意见为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
