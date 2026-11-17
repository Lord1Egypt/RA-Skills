'use strict';
/**
 * franchise-deposit-check-full.js —— 加盟保证金与费项结算核对（本包 / 订阅版共用源码）
 *
 * 谁在什么时候必须做这件事：**连锁加盟总部（或区域代理）的财务 / 结算岗，与加盟商每月对账时**。
 * 加盟商这张「保证金与费项结算明细表」上每一格都能手算复现，而每月都要吵的就是这几处：
 *   · 保证金账户的余额与「期初 + 收取 − 退还 − 扣罚」对不上（账实不符、上期结转没带过来）；
 *   · 加盟费 / 管理费 / 培训费的金额与「计费基数 × 费率」对不上（基数抄错、费率用错档）；
 *   · 合计行是对外金额（据此向加盟商收款 / 划款），明细改过之后合计忘了重算；
 *   · 同一加盟商同一期间同一费项被计了两行（重复导单 / 重复计费）；
 *   · 扣罚从保证金里扣了，但扣得超过可扣的保证金，或者超过了合同约定的扣罚上限；
 *   · 基数 / 费率 / 金额这些关键格留空或是「待填」，整行就复算不出来。
 *
 * 表内勾稽（每一步都能被第三方用同一份输入复算）：
 *   保证金余额 = 保证金期初 + 保证金收取 − 保证金退还 − 保证金扣罚
 *   费项金额   = 计费基数 × 费率
 *   合计行各列 = 各明细行逐列相加（合计行没填的列不核）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）、**不写任何文件、不读环境变量**。
 *
 * 本包执行 6 项；订阅版追加 5 项（见 CHECKS_WITHHELD），其中前两项是本包**结构上做不到**的：
 * 「跨加盟商 × 跨期间汇总台账」与「按差异金额排序的处理清单」—— 本包只有逐行结论，没有跨加盟商 / 跨期间的那一层。
 *
 * ⚠️ 本工具**不判断**加盟保证金该收多少、费项费率是否与合同一致、扣罚到底该不该罚、
 *    合同条款是否合法有效、保证金是否真的收到与退还（那属于加盟合同、内部制度与银行流水的核定）：
 *    表里的基数、费率、金额、上限一律**以你填的为准**，本工具只核表内勾稽，
 *    并把可疑处按原文行号与加盟商 / 费项列出来。
 *
 * ⚠️ 付费项用**形态 A**：订阅版的付费实现集中在一条横线包住的「付费检查区」注释与入口函数之间，
 *    免费包由 tools/strip_free_engine.py 把这一整块连同运行时的付费分支一起摘掉（摘完不留付费函数）；
 *    运行时开关**只声明一次**（见入口函数第一行），注释里不要写出那一行的字面量 ——
 *    摘除工具的残渣断言是纯字符串包含判断，写了就会被判"没删干净"，整包被跳过。
 */

const CHECKS_GIVEN = [
  '保证金余额复算（保证金余额 = 保证金期初 + 保证金收取 − 保证金退还 − 保证金扣罚）',
  '费项金额复算（费项金额 = 计费基数 × 费率）',
  '合计行与明细勾稽（逐列：合计行 = 各明细行逐列相加；合计行没填的列不核）',
  '同一加盟商同一期间同一费项、且费项金额相同的重复计费检测',
  '扣罚超过可扣保证金（余额为负）/ 超过合同扣罚上限检测',
  '关键字段缺失或为占位符、金额列为负数检测',
];

const CHECKS_WITHHELD = [
  '跨加盟商 × 跨期间汇总台账（按加盟商与按结算期间归集费项金额、保证金收发扣与争议金额，'
    + '并逐户做「期初 + 收取 − 退还 − 扣罚 = 期末」的余额勾稽）',
  '按差异金额排序的处理清单（带原文行号、加盟商、结算期间、费项与建议动作）',
  '差异归因：费率档位不一致（同一加盟商同一期间同一费项出现多个费率 ⇒ 按其中最低费率折算多计金额）',
  '差异归因：基数口径不一致（同一加盟商同一期间同一费项出现多个计费基数 ⇒ 按其中最低基数折算多计金额）',
  '差异归因：扣罚缺少依据说明，以及跨期归属错位（保证金期初 ≠ 上期期末余额 / 一次性费项出现在多个结算期间）',
];

const OUT_OF_SCOPE = [
  '判断加盟合同条款是否合法有效、扣罚到底该不该罚、扣罚比例是否合规'
    + '（以加盟合同与内部制度为准；本工具只核金额算得对不对、有没有突破你自己填的上限列）',
  '判断加盟费 / 管理费 / 培训费该收多少、费率档位是否与合同约定一致（表里的基数与费率一律以你填的为准）',
  '判断保证金是否真的收到 / 退还到账（要拿银行流水、收据与退款凭证核，本工具不去查外部系统）',
  '计算保证金的利息 / 资金占用费，或处理增值税、代扣代缴与发票',
  '读取 Excel / 财务系统 / 加盟商结算系统导出文件（需要你先导出成文本贴进来）',
  '按汇率折算多币种后合并（本表按同一币种口径核对）',
  '判断「合同扣罚上限」这一列填得对不对（本工具只按你填的上限做算术比较）',
];

const SAMPLE_TEXT = [
  '加盟商名称\t加盟商编码\t结算期间\t费项名称\t计费基数\t费率\t费项金额\t保证金期初\t保证金收取\t保证金退还\t保证金扣罚\t保证金余额\t合同扣罚上限\t备注',
  '沪上餐饮管理有限公司\tJM-1001\t2026-05\t管理费\t120000.00\t3%\t3600.00\t0.00\t50000.00\t0.00\t0.00\t50000.00\t20000.00\t新签门店保证金已到账',
  '沪上餐饮管理有限公司\tJM-1001\t2026-06\t管理费\t125000.00\t3%\t3750.00\t50000.00\t0.00\t0.00\t2000.00\t48000.00\t20000.00\t逾期开票扣罚（合同5.2）',
  '苏南便利连锁有限公司\tJM-1002\t2026-06\t加盟费\t300000.00\t2%\t6000.00\t0.00\t80000.00\t0.00\t0.00\t80000.00\t30000.00\t首次加盟费与保证金一次结清',
  '皖江食品贸易有限公司\tJM-1003\t2026-05\t管理费\t145000.00\t3%\t4350.00\t0.00\t30000.00\t0.00\t0.00\t30000.00\t15000.00\t开店主保证金已到账',
  '皖江食品贸易有限公司\tJM-1003\t2026-06\t管理费\t150000.00\t3%\t4500.00\t30000.00\t0.00\t30000.00\t0.00\t0.00\t15000.00\t闭店退出已全额退还',
  '合计\t\t\t\t840000.00\t\t22200.00\t80000.00\t160000.00\t30000.00\t2000.00\t208000.00\t\t',
].join('\n');

const TOL = 0.01;

/** 本包口径的说明文本 —— 必须留在摘除标记**之前**，否则整块摘掉后免费引擎会引用不存在的常量。 */
const NOTE_FREE = `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前，兜底的宽泛别名在后。
  //    「加盟商编码」必须排在「加盟商名称」前面；「合同扣罚上限」必须排在「保证金扣罚」前面
  //    （否则上限列被扣罚列抢走 ⇒ 上限永远核不了）；「费项金额」必须排在「费项名称」前面。
  //    这类顺序错**不会报缺列，只会算错或静默不核**（tools/header_map_check.py 专治这个）。
  code: ['加盟商编码', '加盟商代码', '加盟商编号', '加盟方编码', '客户编码', '门店编码', '加盟店编码', '编码', '编号'],
  party: ['加盟商名称', '加盟商全称', '加盟方名称', '加盟方', '客户名称', '商家名称', '加盟商'],
  period: ['结算期间', '所属期间', '结算月份', '账期', '期间', '月份'],
  feeBase: ['计费基数', '收费基数', '计算基数', '计费基础', '基数'],
  feeRate: ['费率', '费率标准', '收费比例', '比例'],
  feeAmount: ['费项金额', '费用金额', '应收金额', '计费金额', '收费金额', '金额'],
  feeItem: ['费项名称', '费用名称', '费用项目', '收费项目', '费项', '费用'],
  depositOpen: ['保证金期初', '期初保证金', '保证金期初余额', '期初余额', '期初'],
  depositIn: ['保证金收取', '收取保证金', '保证金缴纳', '保证金实收', '实收保证金', '保证金收', '收取'],
  depositRefund: ['保证金退还', '退还保证金', '保证金退回', '保证金退款', '保证金退', '退还'],
  deductCap: ['合同扣罚上限', '扣罚上限', '合同上限', '扣罚限额', '扣罚封顶', '上限'],
  depositDeduct: ['保证金扣罚', '扣罚保证金', '保证金扣款', '保证金扣', '扣罚', '违约金'],
  depositBalance: ['保证金余额', '保证金结余', '保证金余', '账户余额', '余额'],
  memo: ['备注', '说明', '依据说明', '摘要'],
};

const LABELS = {
  code: '加盟商编码', party: '加盟商名称', period: '结算期间', feeItem: '费项名称',
  feeBase: '计费基数', feeRate: '费率', feeAmount: '费项金额',
  depositOpen: '保证金期初', depositIn: '保证金收取', depositRefund: '保证金退还',
  depositDeduct: '保证金扣罚', depositBalance: '保证金余额',
  deductCap: '合同扣罚上限', memo: '备注',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不拿 0 去替你假设"这笔没扣罚"） */
const REQUIRED = ['party', 'code', 'period', 'feeItem', 'feeBase', 'feeRate', 'feeAmount',
  'depositOpen', 'depositIn', 'depositRefund', 'depositDeduct', 'depositBalance'];
/** 逐行必须填的单元格（备注 / 合同扣罚上限允许留空：没扣罚、合同没约定上限） */
const CELL_REQUIRED = ['party', 'code', 'period', 'feeItem', 'feeBase', 'feeRate', 'feeAmount',
  'depositOpen', 'depositIn', 'depositRefund', 'depositDeduct', 'depositBalance'];
/** 参与金额归集的列（用于 scope 合计与订阅版汇总台账逐列合计） */
const SUM_ROLES = ['feeBase', 'feeAmount', 'depositOpen', 'depositIn', 'depositRefund',
  'depositDeduct', 'depositBalance'];
/** 负数检查的列（保证金余额为负另有更具体的结论，这里不重复报） */
const NEGATIVE_ROLES = [['feeBase', '计费基数'], ['feeAmount', '费项金额'], ['depositOpen', '保证金期初'],
  ['depositIn', '保证金收取'], ['depositRefund', '保证金退还'], ['depositDeduct', '保证金扣罚']];
/** 一次性费项关键词：这类费项在同一加盟商身上只应出现一次（订阅版跨期归属归因用） */
const ONE_TIME_FEE = /加盟费|进场费|首次|一次性|培训费|装修补贴|开业支持/;
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：|总计：)$/;
const PLACEHOLDER = /^(待填|待补|待定|未知|xxx|xxx\.xx|\?+|tbd|n\/?a|-+|—+|–+)$/i;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值'
      + '（缺一列就报缺列，不会替你按 0 算"这笔没有保证金收退"）。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function cell(v) {
  return v === undefined || v === null ? '' : String(v).trim();
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || PLACEHOLDER.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()【】\[\]]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

function normNumber(raw) {
  if (isBlank(raw)) return null;
  let s = String(raw).trim().replace(/[,，\s¥￥$]/g, '');
  const paren = /^\(.*\)$/.test(s);
  if (paren) s = s.slice(1, -1);
  const pct = /%$/.test(s);
  if (pct) s = s.replace(/%$/, '');
  if (s === '' || !/^[+-]?\d+(\.\d+)?$/.test(s)) return null;
  let n = Number(s);
  if (!Number.isFinite(n)) return null;
  if (paren) n = -n;
  if (pct) n = n / 100;
  return n;
}

const round2 = (n) => Math.round(n * 100) / 100;

/** 费率归一化成小数：`3` / `3%` ⇒ 0.03；`0.03` ⇒ 0.03。
 *  ⚠️ `normNumber` 已经负责把带 `%` 的数字折成小数（`3%` ⇒ 0.03），
 *     所以这里对带 `%` 的写法**不能再除一次 100**（第一版这么写，样例当场每行都误报）。 */
function rateRatio(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n;
  return n > 0.1 ? n / 100 : n;
}

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null, header: [] };
  const header = splitRow(raw[0]);
  const roles = header.map((h) => roleOf(h));
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
      if (role === 'party' && TOTAL_WORDS.test(cell(v))) isTotal = true;
    });
    if (isTotal) {
      totals.row = row;
      totals.line = i + 1;
      totals.rows = (totals.rows || 0) + 1;
    } else {
      items.push(row);
    }
  }
  return { items, totals, missingColumns, header };
}

const num = (row, role) => normNumber(row[role]);

function who(it) {
  const name = cell(it.party) || `第 ${it.line} 行`;
  const code = cell(it.code);
  const period = cell(it.period);
  const item = cell(it.feeItem);
  const bits = [];
  if (code) bits.push(code);
  if (period) bits.push(period);
  if (item) bits.push(item);
  return `${name}${bits.length ? `（${bits.join(' / ')}）` : ''}`;
}

const franchiseKeyOf = (it) => `${cell(it.code)}|${cell(it.party)}`;
const periodKeyOf = (it) => cell(it.period);
const feeGroupKeyOf = (it) => `${cell(it.code)}|${cell(it.party)}|${cell(it.period)}|${cell(it.feeItem)}`;

/* ================================ 本包检查项 ================================ */

/** 1. 保证金余额复算：余额 = 期初 + 收取 − 退还 − 扣罚 */
function checkDepositBalanceRecompute(it) {
  const open = num(it, 'depositOpen');
  const inAmt = num(it, 'depositIn');
  const refundAmt = num(it, 'depositRefund');
  const deductAmt = num(it, 'depositDeduct');
  const stated = num(it, 'depositBalance');
  if (open === null || inAmt === null || refundAmt === null || deductAmt === null || stated === null) return null;
  const expect = round2(open + inAmt - refundAmt - deductAmt);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '保证金余额复算不符', line: it.line,
    amount: round2(Math.abs(stated - expect)),
    message: `${who(it)}的保证金余额写的是 ${stated.toFixed(2)}，按 期初 ${open.toFixed(2)} `
      + `+ 收取 ${inAmt.toFixed(2)} − 退还 ${refundAmt.toFixed(2)} − 扣罚 ${deductAmt.toFixed(2)} `
      + `应为 ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '保证金账户的余额必须能被「期初 + 收取 − 退还 − 扣罚」复算出来：'
      + '常见错法是上一期期末没结转成这一期期初、退还款没从余额里减、或者扣罚只在备注里写了却没落进金额列。'
      + '先拿保证金台账 / 收款收据把这一户当期四笔发生额核一遍，再让余额跟着重算。',
  };
}

/** 2. 费项金额复算：费项金额 = 计费基数 × 费率 */
function checkFeeAmountRecompute(it) {
  const base = num(it, 'feeBase');
  const rate = rateRatio(it.feeRate);
  const stated = num(it, 'feeAmount');
  if (base === null || rate === null || stated === null) return null;
  const expect = round2(base * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '费项金额与基数×费率不符', line: it.line,
    amount: round2(Math.abs(stated - expect)),
    message: `${who(it)}的费项金额写的是 ${stated.toFixed(2)}，按 计费基数 ${base.toFixed(2)} `
      + `× 费率 ${(rate * 100).toFixed(4).replace(/0+$/, '').replace(/\.$/, '')}% 应为 ${expect.toFixed(2)}，`
      + `相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '费率列写 `3`、`3%`、`0.03` 都按 3% 理解；写 `1` 表示 100%，本工具不会替你猜。'
      + '先确认这一行的计费基数是什么口径（本期营收 / 采购额 / 门店数），再确认费率用的是合同里哪一档。',
  };
}

/** 3. 合计行勾稽：合计行每一列 = 各明细行逐列相加（合计行没填的列不核） */
function checkTotalRow(totals, items) {
  const out = [];
  const total = totals.row;
  if (!total) return out;
  for (const role of SUM_ROLES) {
    const stated = num(total, role);
    if (stated === null) continue;
    let sum = 0;
    for (const it of items) {
      const n = num(it, role);
      if (n !== null) sum += n;
    }
    sum = round2(sum);
    if (Math.abs(sum - stated) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: total.line,
      amount: round2(Math.abs(stated - sum)),
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行逐行相加是 ${sum.toFixed(2)}，`
        + `相差 ${round2(stated - sum).toFixed(2)}。`,
      advice: '合计行是对外金额（总部据此向加盟商收款 / 划款），先把它与明细对齐：'
        + '要么明细漏了一整行，要么明细改过之后合计没重算（最常见）。'
        + '若明细逐行都对而合计对不上，差异就出在合计行自身。',
    });
  }
  return out;
}

/** 4. 同一加盟商同一期间同一费项、且费项金额相同的重复计费
 *  ⚠️ 判据里必须带上「费项金额也相同」：只按 加盟商 + 期间 + 费项 判重，
 *     会把「同一费项按两个费率档位分行列示」这种正当写法误报成重复计费，
 *     也会让订阅版的费率 / 基数归因永远和这条撞在一起（单因隔离就做不出来了）。 */
function checkDuplicateFeeItem(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    if (isBlank(it.party) || isBlank(it.period) || isBlank(it.feeItem)) continue;
    const amount = num(it, 'feeAmount');
    if (amount === null) continue;
    const key = `${feeGroupKeyOf(it)}|${round2(amount)}`;
    if (seen.has(key)) {
      out.push({
        level: 'P0', category: '同一加盟商同一期间同一费项重复计费', line: it.line,
        amount: round2(Math.abs(amount)),
        message: `${who(it)}这一笔（费项金额 ${amount.toFixed(2)}）在第 ${seen.get(key)} 行已经计过一次，`
          + `第 ${it.line} 行又计了一次 —— 同一加盟商 + 同一结算期间 + 同一费项，金额也完全相同。`,
        advice: '同一加盟商同一期间的同一费项只应计一次：拿结算单原表核一遍，把重复的那行冲掉；'
          + '确属分期 / 分店计费的，请把结算期间或费项名称写到能区分开（例如「管理费-二期」），'
          + '并按不同档位拆行，别让两行看起来一模一样。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

/** 5. 扣罚超过可扣保证金（余额为负）/ 超过合同扣罚上限 */
function checkDeductOverLimit(items) {
  const out = [];
  for (const it of items) {
    const open = num(it, 'depositOpen');
    const inAmt = num(it, 'depositIn');
    const refundAmt = num(it, 'depositRefund');
    const deductAmt = num(it, 'depositDeduct');
    const cap = num(it, 'deductCap');
    if (deductAmt !== null && deductAmt > TOL) {
      const available = round2((open === null ? 0 : open) + (inAmt === null ? 0 : inAmt)
        - (refundAmt === null ? 0 : refundAmt));
      if (deductAmt > available + TOL) {
        out.push({
          level: 'P0', category: '扣罚超过可扣保证金（余额为负）', line: it.line,
          amount: round2(deductAmt - available),
          message: `${who(it)}的扣罚是 ${deductAmt.toFixed(2)}，但这一户可扣的保证金只有 ${available.toFixed(2)}`
            + `（期初 + 收取 − 退还），超出 ${round2(deductAmt - available).toFixed(2)} —— 扣完余额会变成负数。`,
          advice: '扣罚只能扣到保证金余额为 0 为止；超出部分要么向加盟商另行追缴（另立应收），'
            + '要么按合同约定由其他款项抵。先确认这笔扣罚的事由与金额，再决定超出部分怎么处理。',
        });
      }
    }
    if (deductAmt !== null && cap !== null && deductAmt > cap + TOL) {
      out.push({
        level: 'P1', category: '扣罚超过合同扣罚上限', line: it.line,
        amount: round2(deductAmt - cap),
        message: `${who(it)}的扣罚是 ${deductAmt.toFixed(2)}，超过这一行「合同扣罚上限」列的 ${cap.toFixed(2)}，`
          + `超出 ${round2(deductAmt - cap).toFixed(2)}。`,
        advice: '本工具只按你填的上限做算术比较，不判断这个上限填得对不对、也不判断扣罚是否合规。'
          + '请拿加盟合同里的扣罚条款对一遍：是上限填错了，还是扣罚金额算多了。',
      });
    }
  }
  return out;
}

/** 6. 关键字段缺失或为占位符 / 金额列为负数 */
function checkBlanksAndNegative(items) {
  const out = [];
  for (const it of items) {
    for (const role of CELL_REQUIRED) {
      const s = cell(it[role]);
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这一行就复算不出来。本工具不会拿 0 或默认值替你填：'
            + '确实没有发生的收退请填 0，留空表示"不知道"，这两者不能混。',
        });
      }
    }
    for (const [role, label] of NEGATIVE_ROLES) {
      const v = num(it, role);
      if (v !== null && v < -TOL) {
        out.push({
          level: 'P0', category: '金额列为负数', line: it.line,
          amount: round2(Math.abs(v)),
          message: `${who(it)}的「${label}」是 ${v.toFixed(2)}（负数）。`,
          advice: '这几列都是正数口径：退还 / 扣罚要表达"冲回"或"调减"时，请把事由写进备注而不是填负数；'
            + '保证金余额为负应当由扣罚超过可扣余额那条结论来反映。',
        });
      }
    }
  }
  return out;
}

/* ===== 以下为订阅版才执行的检查 ===== */

/** 订阅版 1：差异归因 —— 费率档位不一致（同一加盟商同一期间同一费项出现多个费率） */
function checkFeeRateDrift(items) {
  const groups = new Map();
  for (const it of items) {
    if (isBlank(it.party) || isBlank(it.period) || isBlank(it.feeItem)) continue;
    const rate = rateRatio(it.feeRate);
    const base = num(it, 'feeBase');
    if (rate === null) continue;
    const key = feeGroupKeyOf(it);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push({ line: it.line, rate, base: base === null ? 0 : base, it });
  }
  const out = [];
  for (const rows of groups.values()) {
    const rates = [];
    for (const r of rows) if (rates.indexOf(r.rate) < 0) rates.push(r.rate);
    if (rates.length <= 1) continue;
    const base = Math.min.apply(null, rates);
    let over = 0;
    for (const r of rows) if (r.rate > base + 1e-12) over += r.base * (r.rate - base);
    over = round2(over);
    const last = rows[rows.length - 1];
    out.push({
      level: 'P1', category: '差异归因：费率档位不一致（多计）', line: last.line,
      amount: over,
      message: `${who(last.it)}这一组（第 ${rows.map((r) => r.line).join('、')} 行）用到了 `
        + `${rates.length} 个费率：${rates.map((r) => round2(r * 100) + '%').join(' / ')}。`
        + `按其中最低费率 ${round2(base * 100)}% 折算，多计费项金额 ${over.toFixed(2)}。`,
      advice: '同一加盟商同一期间同一费项通常只有一个费率档位（分店 / 分品类要分行的，请按档拆开列示）。'
        + '先把这几行对回加盟合同的费率表：是调价后新旧混用，还是有一行费率用错了档。',
    });
  }
  return out;
}

/** 订阅版 2：差异归因 —— 基数口径不一致（同一加盟商同一期间同一费项出现多个计费基数） */
function checkFeeBaseDrift(items) {
  const groups = new Map();
  for (const it of items) {
    if (isBlank(it.party) || isBlank(it.period) || isBlank(it.feeItem)) continue;
    const base = num(it, 'feeBase');
    const rate = rateRatio(it.feeRate);
    if (base === null || rate === null) continue;
    const key = feeGroupKeyOf(it);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push({ line: it.line, base, rate, it });
  }
  const out = [];
  for (const rows of groups.values()) {
    const bases = [];
    for (const r of rows) if (bases.indexOf(r.base) < 0) bases.push(r.base);
    if (bases.length <= 1) continue;
    const minBase = Math.min.apply(null, bases);
    let over = 0;
    for (const r of rows) if (r.base > minBase) over += (r.base - minBase) * r.rate;
    over = round2(over);
    const last = rows[rows.length - 1];
    out.push({
      level: 'P1', category: '差异归因：基数口径不一致（多计）', line: last.line,
      amount: over,
      message: `${who(last.it)}这一组（第 ${rows.map((r) => r.line).join('、')} 行）同一费项出现了 `
        + `${bases.length} 个计费基数：${bases.map((b) => b.toFixed(2)).join(' / ')}。`
        + `按其中最低基数 ${minBase.toFixed(2)} 折算，多计费项金额 ${over.toFixed(2)}。`,
      advice: '同一加盟商同一期间同一费项的基数口径应当只有一个（本期营收 / 含税或不含税 / 自然月或结算月）。'
        + '把这几行对回结算系统导出的口径说明与合同附件：是含税与不含税混用，还是有一行基数抄错了。',
    });
  }
  return out;
}

/** 订阅版 3：差异归因 —— 扣罚缺少依据说明（扣了钱，依据栏却是空的） */
function checkDeductWithoutBasis(it) {
  const deductAmt = num(it, 'depositDeduct');
  if (deductAmt === null || deductAmt <= TOL) return null;
  if (!isBlank(it.memo)) return null;
  return {
    level: 'P1', category: '差异归因：扣罚缺少依据说明', line: it.line,
    amount: round2(deductAmt),
    message: `${who(it)}从保证金里扣了 ${deductAmt.toFixed(2)}，但「备注」列是空的 —— 台账上看不出这笔扣罚的依据。`,
    advice: '本工具只看依据栏是否为空、有没有写明扣罚事由，不判断扣罚是否合规。'
      + '请把扣罚事由与合同条款号补进备注（例如「逾期开票扣罚（合同5.2）」），否则加盟商对账时不会认这笔扣款。',
  };
}

/** 订阅版 4：差异归因 —— 保证金跨期不衔接（本期期初 ≠ 上期期末余额） */
function checkDepositChainBreak(items) {
  const byFranchisee = new Map();
  for (const it of items) {
    if (isBlank(it.party) || isBlank(it.period)) continue;
    const key = franchiseKeyOf(it);
    if (!byFranchisee.has(key)) byFranchisee.set(key, new Map());
    // 同一加盟商同一期间有多行时，取最后一行（同一户当期的保证金状态应当一致）
    byFranchisee.get(key).set(periodKeyOf(it), {
      line: it.line, period: periodKeyOf(it),
      open: num(it, 'depositOpen'), balance: num(it, 'depositBalance'), it,
    });
  }
  const out = [];
  for (const periods of byFranchisee.values()) {
    const keys = [...periods.keys()].sort();
    for (let i = 1; i < keys.length; i++) {
      const prev = periods.get(keys[i - 1]);
      const cur = periods.get(keys[i]);
      if (prev.balance === null || cur.open === null) continue;
      const gap = round2(cur.open - prev.balance);
      if (Math.abs(gap) <= TOL) continue;
      out.push({
        level: 'P1', category: '差异归因：保证金跨期不衔接', line: cur.line,
        amount: round2(Math.abs(gap)),
        message: `${who(cur.it)}的保证金期初是 ${cur.open.toFixed(2)}，但上一结算期间（${prev.period}，`
          + `第 ${prev.line} 行）的期末余额是 ${prev.balance.toFixed(2)}，相差 ${gap.toFixed(2)} —— `
          + '上期期末没有正确结转成本期期初。',
        advice: '跨期的保证金台账必须"上期期末 = 本期期初"。先确认中间是不是有未被列进本表的收退 / 扣罚，'
          + '把漏掉的那一期补进台账，再让期初跟着结转。',
      });
    }
  }
  return out;
}

/** 订阅版 5：差异归因 —— 一次性费项跨期重复归属 */
function checkOneTimeFeeRepeat(items) {
  const groups = new Map();
  for (const it of items) {
    if (isBlank(it.party) || isBlank(it.period) || isBlank(it.feeItem)) continue;
    const feeItem = cell(it.feeItem);
    if (!ONE_TIME_FEE.test(feeItem)) continue;
    const key = `${franchiseKeyOf(it)}|${feeItem}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push({ line: it.line, period: periodKeyOf(it), it });
  }
  const out = [];
  for (const rows of groups.values()) {
    const periods = [];
    for (const r of rows) if (periods.indexOf(r.period) < 0) periods.push(r.period);
    if (periods.length <= 1) continue;
    const last = rows[rows.length - 1];
    const amount = num(last.it, 'feeAmount');
    out.push({
      level: 'P1', category: '差异归因：一次性费项跨期重复归属', line: last.line,
      amount: amount === null ? 0 : round2(Math.abs(amount)),
      message: `${who(last.it)}的「${cell(last.it.feeItem)}」属于一次性费项，却出现在 `
        + `${periods.length} 个结算期间：${periods.sort().join(' / ')}`
        + `（第 ${rows.map((r) => r.line).join('、')} 行）—— 同一笔一次性费用被摊到了多个期间。`,
      advice: '加盟费 / 培训费 / 进场费这类一次性费项只应归属一个结算期间。'
        + '先确认是分期收款（那就该拆成独立费项并写明期次）还是把同一笔重复计到了两个期间。',
    });
  }
  return out;
}

/** 订阅版专有能力：跨加盟商 × 跨期间汇总台账 + 按差异金额排序的处理清单（本包结构上没有这一层）。 */
function buildFranchiseLedger(items, findings) {
  const byFranchisee = new Map();
  const byPeriod = new Map();
  const byLine = new Map();
  for (const it of items) {
    const fkey = franchiseKeyOf(it);
    const pkey = periodKeyOf(it);
    byLine.set(it.line, it);
    if (!byFranchisee.has(fkey)) {
      byFranchisee.set(fkey, {
        code: cell(it.code) || '(未填加盟商编码)',
        name: cell(it.party) || '(未填加盟商名称)',
        periods: [], rows: 0,
        fee_base_total: 0, fee_amount_total: 0,
        deposit_open_first: null, deposit_open_first_period: '',
        deposit_in_total: 0, deposit_refund_total: 0, deposit_deduct_total: 0,
        deposit_balance: null, balance_as_of_period: '',
        disputed_total: 0, disputes: [],
      });
    }
    if (!byPeriod.has(pkey)) {
      byPeriod.set(pkey, {
        period: pkey || '(未填结算期间)', rows: 0, franchisees: 0,
        fee_amount_total: 0, deposit_in_total: 0, deposit_balance_total: 0, disputed_total: 0,
      });
    }
    const f = byFranchisee.get(fkey);
    const pd = byPeriod.get(pkey);
    f.rows += 1;
    pd.rows += 1;
    if (f.periods.indexOf(pkey) < 0) f.periods.push(pkey);
    const addF = (field, role) => {
      const v = num(it, role);
      if (v !== null) f[field] = round2(f[field] + v);
    };
    addF('fee_base_total', 'feeBase');
    addF('fee_amount_total', 'feeAmount');
    addF('deposit_in_total', 'depositIn');
    addF('deposit_refund_total', 'depositRefund');
    addF('deposit_deduct_total', 'depositDeduct');
    const fa = num(it, 'feeAmount'); if (fa !== null) pd.fee_amount_total = round2(pd.fee_amount_total + fa);
    const di = num(it, 'depositIn'); if (di !== null) pd.deposit_in_total = round2(pd.deposit_in_total + di);
    const db = num(it, 'depositBalance'); if (db !== null) pd.deposit_balance_total = round2(pd.deposit_balance_total + db);
    // 期初取**最早**一期，期末余额取**最晚**一期（累计口径下这才是这一户的起止状态）
    const open = num(it, 'depositOpen');
    if (open !== null && (f.deposit_open_first === null || pkey < f.deposit_open_first_period)) {
      f.deposit_open_first = open;
      f.deposit_open_first_period = pkey;
    }
    if (db !== null && (f.deposit_balance === null || pkey >= f.balance_as_of_period)) {
      f.deposit_balance = db;
      f.balance_as_of_period = pkey;
    }
  }
  for (const f of byFranchisee.values()) {
    f.periods.sort();
    f.balance_gap = f.deposit_balance === null || f.deposit_open_first === null ? null
      : round2(f.deposit_open_first + f.deposit_in_total - f.deposit_refund_total
        - f.deposit_deduct_total - f.deposit_balance);
    f.balance_formula = '期初(最早一期) + 累计收取 − 累计退还 − 累计扣罚 = 期末余额(最晚一期)';
  }

  for (const f of findings) {
    const it = byLine.get(f.line);
    if (!it) continue;
    const fkey = franchiseKeyOf(it);
    const pkey = periodKeyOf(it);
    const amt = typeof f.amount === 'number' && Number.isFinite(f.amount) ? round2(f.amount) : 0;
    if (byFranchisee.has(fkey)) {
      const g = byFranchisee.get(fkey);
      g.disputed_total = round2(g.disputed_total + amt);
      g.disputes.push({ line: f.line, period: pkey, category: f.category, amount: amt });
    }
    if (byPeriod.has(pkey)) {
      const pd = byPeriod.get(pkey);
      pd.disputed_total = round2(pd.disputed_total + amt);
    }
  }
  const franchises = [...byFranchisee.values()]
    .sort((a, b) => (a.deposit_balance === null ? 0 : a.deposit_balance)
      - (b.deposit_balance === null ? 0 : b.deposit_balance)
      || String(a.code).localeCompare(String(b.code)));
  for (const f of franchises) f.disputes.sort((a, b) => a.line - b.line);
  const periodList = [...byPeriod.values()].sort((a, b) => String(a.period).localeCompare(String(b.period)));
  for (const pd of periodList) {
    const set = new Set();
    for (const it of items) if (periodKeyOf(it) === pd.period) set.add(franchiseKeyOf(it));
    pd.franchisees = set.size;
  }
  let disputed = 0;
  let gapTotal = 0;
  for (const f of franchises) {
    disputed = round2(disputed + f.disputed_total);
    if (typeof f.balance_gap === 'number') gapTotal = round2(gapTotal + f.balance_gap);
  }

  const queue = findings
    .filter((f) => typeof f.amount === 'number' && Number.isFinite(f.amount) && f.amount > TOL)
    .slice()
    .sort((a, b) => (b.amount - a.amount) || (a.line - b.line));
  const actionQueue = queue.map((f, idx) => {
    const it = byLine.get(f.line);
    return {
      rank: idx + 1,
      line: f.line,
      code: it ? (cell(it.code) || '(未填加盟商编码)') : '(合计行)',
      name: it ? (cell(it.party) || '(未填加盟商名称)') : '(合计行)',
      period: it ? cell(it.period) : '',
      fee_item: it ? cell(it.feeItem) : '',
      category: f.category,
      level: f.level,
      amount: round2(f.amount),
      advice: f.advice || '',
    };
  });

  return {
    by_franchisee: franchises,
    by_period: periodList,
    franchisees: franchises.length,
    periods: periodList.length,
    rows: items.length,
    disputed_total: disputed,
    balance_gap_total: gapTotal,
    action_queue: actionQueue,
    sort_rule: '台账按「期末保证金余额」升序（余额小的在前 = 需要优先确认收退与扣罚），余额相同按加盟商编码；'
      + '差异处理清单按涉及金额从大到小，金额相同按原文行号。',
    note: actionQueue.length
      ? '这是对账前的处理清单：先按金额从大到小把差异谈清楚 / 改对（重复计费、余额复算不符、扣罚超上限优先），'
        + '再按对账后的金额出具结算单。'
      : '没有算出带金额的差异 —— 不是"没问题"，是本材料在上述检查项范围内没发现差额；'
        + '范围之外的判断（费率是否符合合同、扣罚是否合规、保证金是否真的到账）本工具不做。',
  };
}

/* ============================== 主入口 ============================== */

function run(payload) {
  const p = payload;
  const paid = Boolean(p && (p.full || p.credit || p.token));
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到加盟商保证金与费项结算明细表的正文（text）—— 请把'
      + '「加盟商名称 / 加盟商编码 / 结算期间 / 费项名称 / 计费基数 / 费率 / 费项金额 / 保证金期初 / '
      + '保证金收取 / 保证金退还 / 保证金扣罚 / 保证金余额」这张表（**含表头**）整段贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `表头缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或每行都是合计行），没有任何加盟商结算明细行');
  }

  const periods = new Set();
  const franchises = new Set();
  for (const it of t.items) {
    periods.add(cell(it.period));
    franchises.add(franchiseKeyOf(it));
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkDepositBalanceRecompute(it);
    if (a) findings.push(a);
    const b = checkFeeAmountRecompute(it);
    if (b) findings.push(b);
    if (paid) {
      const c = checkDeductWithoutBasis(it);
      if (c) findings.push(c);
    }
  }
  findings.push.apply(findings, checkTotalRow(t.totals, t.items));
  findings.push.apply(findings, checkDuplicateFeeItem(t.items));
  findings.push.apply(findings, checkDeductOverLimit(t.items));
  findings.push.apply(findings, checkBlanksAndNegative(t.items));
  if (paid) findings.push.apply(findings, checkFeeRateDrift(t.items));
  if (paid) findings.push.apply(findings, checkFeeBaseDrift(t.items));
  if (paid) findings.push.apply(findings, checkDepositChainBreak(t.items));
  if (paid) findings.push.apply(findings, checkOneTimeFeeRepeat(t.items));

  const checksExecuted = CHECKS_GIVEN.slice();
  if (paid) checksExecuted.push.apply(checksExecuted, CHECKS_WITHHELD);
  const notRun = [];
  if (!paid) notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const totalsOf = {};
  for (const role of SUM_ROLES) {
    let sum = 0;
    for (const it of t.items) {
      const n = num(it, role);
      if (n !== null) sum += n;
    }
    totalsOf[`${role}_total`] = round2(sum);
  }

  let tierNote = NOTE_FREE;
  if (paid) {
    tierNote = '完整档执行全部检查项（含跨加盟商 × 跨期间汇总台账与按差异金额排序的处理清单，'
      + '以及费率档位 / 基数口径 / 扣罚依据 / 跨期归属四类差异归因）。';
  }

  const result = {
    status: 'success',
    service_type: 'FRANCHISE_DEPOSIT_CHECK',
    scope: {
      checks: checksExecuted,
      checks_not_run: notRun,
      rows: t.items.length,
      franchises: franchises.size,
      periods: periods.size,
      totals_row: Boolean(t.totals.row),
      totals_rows: t.totals.rows || 0,
      fee_base_total: totalsOf.feeBase_total,
      fee_amount_total: totalsOf.feeAmount_total,
      deposit_open_total: totalsOf.depositOpen_total,
      deposit_in_total: totalsOf.depositIn_total,
      deposit_refund_total: totalsOf.depositRefund_total,
      deposit_deduct_total: totalsOf.depositDeduct_total,
      deposit_balance_total: totalsOf.depositBalance_total,
      statement_fee_amount_total: t.totals.row ? num(t.totals.row, 'feeAmount') : null,
      rate_convention: '费率可写 3 / 3% / 0.03，均按 3% 理解；写 1 表示 100%，本工具不替你猜',
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      franchises: franchises.size,
      periods: periods.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_executed: checksExecuted,
    checks_withheld: notRun,
    checks_given: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
    note: tierNote,
    disclaimer: '只核「期初 + 收取 − 退还 − 扣罚 = 余额」「计费基数 × 费率 = 费项金额」'
      + '「合计行 = 各明细行逐列相加」这类**表内勾稽**，不判断费率该用哪一档、基数该取什么口径、'
      + '扣罚是否合规、合同条款是否合法有效、保证金是否真的收到与退还（以加盟合同、内部制度与银行流水为准）；'
      + '每条结论都带原文行号与加盟商 / 费项，可由第三方用同一份输入复算。',
  };

  if (paid) {
    const ledger = buildFranchiseLedger(t.items, findings);
    result.franchise_ledger = ledger;
    result.action_queue = ledger.action_queue;
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
  CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
