'use strict';
/**
 * saas-usage-billing-check-full.js —— SaaS订阅用量与超额计费核对（本包 / 订阅版共用源码）
 *
 * 谁在什么时候必须做这件事：**SaaS 公司的商务 / 财务，以及企业客户（甲方）的财务**，
 * 在**每月出账、客户对账、续费谈判这几个固定节点**上，都得把这张「订阅用量与超额计费明细表」核一遍。
 * 表里每一格都能手算复现，而每次吵的都是这几处：
 *   · 「套餐额度」与「实际用量」的口径不一致 —— 甲方统计到的是自己后台的调用量（含重试、含测试 Key），
 *     乙方统计到的是**计费口径**的调用量（去重、不含失败请求）⇒ 超额用量凭空多出一截；
 *   · 超额费用 = 超额用量 × 超额单价，可单价调价了、阶梯档取错了、进位规则（按千次进位）没做；
 *   · 账单金额 = 套餐费 + 超额费 + 坐席费 − 折扣，这一格是**要付出去的钱**，
 *     明细里任何一处改动忘了带上它，账单就直接对不上；
 *   · 同一份材料里同一个月同一订阅号被录了两行（续费单 + 变更单一起贴进来最常见），
 *     用量、超额费、账单一起算了两遍；
 *   · 关键格留空或写「待确认」—— 整行就复算不出来。
 *
 * 表内勾稽（每一步都能被第三方用同一份输入复算）：
 *   超额用量   = max(0, 实际用量 − 套餐额度)
 *   超额费用   = 超额用量 × 超额单价
 *   账单金额   = 套餐费 + 超额费 + 坐席费 − 折扣
 *   合计行各列 = 各明细行逐列相加（订阅版）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）、
 * **不写任何文件、不读环境变量**。
 *
 * 本包执行 6 项；订阅版追加 5 项（见 CHECKS_WITHHELD），其中最后一项是本包**结构上做不到**的：
 * 「跨客户 / 跨账期汇总台账与按多收金额排序的处理清单」—— 本包只有逐行结论，没有汇总层，
 * 也就说不清"这个月一共多收了多少、先跟哪几家谈"。
 *
 * ⚠️ 本工具**不判断**套餐额度该按哪一档报价、超额单价是否符合合同、
 *    用量统计口径（去重规则 / 重试算不算 / 测试 Key 算不算）对不对、折扣是否已审批 ——
 *    表里的套餐额度、实际用量、超额单价、折扣一律**以你填的为准**，本工具只核表内勾稽，
 *    并把可疑处按原文行号与订阅号列出来。
 *
 * 形态说明：本文件用**形态 A**（付费实现集中成一块，块首是一条横线包住的付费检查区注释），
 * 免费包由 `tools/strip_free_engine.py` 把从那条注释到主入口之间的整块
 * 连同运行时的付费分支一起摘掉，摘完的免费包里不留付费函数。
 * ⛔ 注释里不写付费开关那一行的字面量，也不写它的条件语句字面量（摘除工具的残渣断言按字符串包含判定）。
 */

const CHECKS_GIVEN = [
  '超额用量复算（超额用量 = max(0, 实际用量 − 套餐额度)）',
  '超额费用复算（超额费用 = 超额用量 × 超额单价，逐行复算）',
  '账单金额勾稽（账单金额 = 套餐费 + 超额费 + 坐席费 − 折扣）',
  '用量与套餐额度适配检测（实际用量远低于额度 ⇒ 套餐买大了、白付套餐费）',
  '同一账期同一订阅号重复行检测',
  '关键字段缺失或为占位符检测',
];

const CHECKS_WITHHELD = [
  '合计行勾稽（合计行各列 = 各明细行逐列相加，不符时报出差异金额并定位差异订阅号）',
  '折扣列异常检测（折扣超过套餐费 + 坐席费 ⇒ 把超额费也一起打折了；折扣为负 ⇒ 实收大于应收）',
  '同一客户同一账期出现多个订阅号（同一主体被重复开通套餐 ⇒ 套餐费可能被收了两遍）',
  '用量口径核对（同一客户同一账期出现多个套餐额度 ⇒ 额度口径不一致，超额用量被算高或算低）',
  '跨客户 / 跨账期汇总台账与按多收金额排序的处理清单（按客户 × 账期汇总用量 / 超额用量 / 超额费 / 账单与多收金额，按金额排序，逐条带原文行号）',
];

const OUT_OF_SCOPE = [
  '判断套餐额度该按哪一档报价、超额单价是否符合合同约定（本工具只核表内算术，以你填的额度与单价为准）',
  '判断用量统计口径是否正确（去重规则、失败请求算不算、测试 Key 算不算、跨月切分点——本工具不连接任何系统取数）',
  '判断折扣是否经过审批、是否符合折扣政策（本工具只做折扣与账单、折扣与折扣基数的勾稽）',
  '判断账单是否已开票、是否已回款、有没有逾期（要拿发票与银行流水核，本工具只看这张表）',
  '计算增值税 / 发票税额，或处理跨月调整、红冲与账务分录',
  '读取 Excel / 计费系统 / 财务系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '账期\t客户编码\t客户名称\t订阅号\t套餐名称\t套餐额度\t实际用量\t超额用量\t超额单价\t超额费用\t套餐费\t坐席数\t坐席费\t折扣\t账单金额\t计费状态\t备注',
  '2026-05\tC001\t杭州甲贸易有限公司\tSUB-0001\t专业版年付\t10000\t11200\t1200\t0.50\t600.00\t1000.00\t10\t100.00\t50.00\t1650.00\t已核对\t已与客户用量报表核对一致',
  '2026-05\tC001\t杭州甲贸易有限公司\tSUB-0002\t基础版月付\t5000\t4800\t0\t0.80\t0.00\t300.00\t0\t0.00\t0.00\t300.00\t已核对\t未超额，按套餐额度计费',
  '2026-05\tC002\t苏州乙机械有限公司\tSUB-0003\t企业版年付\t50000\t56000\t6000\t0.40\t2400.00\t3000.00\t20\t200.00\t100.00\t5500.00\t已核对\t已与客户用量报表核对一致',
  '2026-05\tC003\t南京丙物流有限公司\tSUB-0004\t基础版月付\t5000\t6000\t1000\t0.80\t800.00\t300.00\t5\t50.00\t0.00\t1150.00\t已核对\t已与客户用量报表核对一致',
  '2026-06\tC001\t杭州甲贸易有限公司\tSUB-0001\t专业版年付\t10000\t13000\t3000\t0.50\t1500.00\t1000.00\t10\t100.00\t0.00\t2600.00\t已核对\t已与客户用量报表核对一致',
  '2026-06\tC002\t苏州乙机械有限公司\tSUB-0003\t企业版年付\t50000\t40000\t0\t0.40\t0.00\t3000.00\t20\t200.00\t0.00\t3200.00\t已核对\t未超额，用量低于套餐额度',
  '2026-06\tC003\t南京丙物流有限公司\tSUB-0004\t基础版月付\t5000\t9000\t4000\t0.80\t3200.00\t300.00\t5\t50.00\t0.00\t3550.00\t已核对\t已与客户用量报表核对一致',
  '合计\t\t\t\t\t135000\t140000\t15200\t\t8500.00\t8900.00\t70\t700.00\t150.00\t17950.00\t\t',
].join('\n');

const TOL = 0.01;

/** 表头 → 角色。⚠️ 这里用**完全相等**匹配（不是子串包含）：
 *  「套餐额度」/「套餐费」、「超额用量」/「超额单价」/「超额费用」、「账单金额」/「坐席费」
 *  互为前缀或高度相似，一旦用子串包含匹配就会互相抢列、静默算错（`tools/header_map_check.py` 就是查这个）。
 *  客户导出的表头常带空格、全角括号、单位后缀（如「实际用量(次)」），所以先剥掉空格与括号再比。 */
const ROLES = {
  period: ['账期', '计费账期', '账单周期', '所属账期', '出账月份', '计费月份', '所属期间', '期间', '月份'],
  customerCode: ['客户编码', '客户代码', '客户编号', '客户号', '企业编码'],
  customerName: ['客户名称', '客户简称', '企业名称', '公司名称', '客户'],
  subscriptionNo: ['订阅号', '订阅编号', '订阅ID', '订阅id', '服务编号', '订单号'],
  planName: ['套餐名称', '套餐版本', '产品版本', '版本', '套餐'],
  planQuota: ['套餐额度', '套餐包含用量', '包含用量', '免费额度', '额度'],
  actualUsage: ['实际用量', '实际使用量', '计费用量', '用量'],
  overageUsage: ['超额用量', '超出用量', '超量'],
  overageUnitPrice: ['超额单价', '超量单价', '超出单价'],
  overageFee: ['超额费用', '超额费', '超量费用', '超出费用'],
  planFee: ['套餐费', '套餐费用', '订阅费', '基础费'],
  seatCount: ['坐席数', '坐席数量', '账号数', '用户数'],
  seatFee: ['坐席费', '坐席费用', '账号费'],
  discount: ['折扣', '折扣金额', '优惠', '优惠金额', '减免'],
  billAmount: ['账单金额', '应付金额', '应收金额', '本期账单', '账单'],
  billingStatus: ['计费状态', '账单状态', '状态'],
  memo: ['备注', '说明', '依据'],
};

const LABELS = {
  period: '账期', customerCode: '客户编码', customerName: '客户名称', subscriptionNo: '订阅号',
  planName: '套餐名称', planQuota: '套餐额度', actualUsage: '实际用量',
  overageUsage: '超额用量', overageUnitPrice: '超额单价', overageFee: '超额费用',
  planFee: '套餐费', seatCount: '坐席数', seatFee: '坐席费', discount: '折扣',
  billAmount: '账单金额', billingStatus: '计费状态', memo: '备注',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不拿 0 去替你假设"这个月没超额"）。
 *  没有超额请把「超额用量 / 超额单价 / 超额费用」都填 0，不要留空 ——
 *  「填 0」表示"确实没有"，"留空"表示"不知道"，这两者不能混。 */
const REQUIRED = ['period', 'customerCode', 'subscriptionNo', 'planQuota', 'actualUsage',
  'overageUsage', 'overageUnitPrice', 'overageFee', 'planFee', 'seatCount', 'seatFee',
  'discount', 'billAmount', 'billingStatus'];

/** 合计行逐列复核的列：**不含超额单价**（单价加总没有意义），也不含坐席数之外的比例列。 */
const SUM_ROLES = ['planQuota', 'actualUsage', 'overageUsage', 'overageFee', 'planFee',
  'seatCount', 'seatFee', 'discount', 'billAmount'];

/** 金额列：算"多收 / 少收"与"争议金额"时只看这些列。 */
const MONEY_ROLES = ['overageFee', 'planFee', 'seatFee', 'discount', 'billAmount'];

const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：|总计：)$/;
const PLACEHOLDER = /^(待填|待补|待定|待确认|待核|xxx|xxx\.xx|\?+|tbd|n\/?a|-+)$/i;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不齐时本工具不做任何认定，也不套用默认值'
      + '（缺一列就报缺列，不会替你按 0 算"这个月没超额"）。',
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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
}

/** 表头归一：去掉空格、全角/半角括号、常见单位后缀，再与别名表**完全相等**比对。 */
function roleOf(header) {
  const h = cell(header).replace(/[\s（）()]/g, '').replace(/(次|条|个|元|万元|人民币)$/g, '');
  for (const role of Object.keys(ROLES)) {
    if (ROLES[role].indexOf(h) >= 0) return role;
  }
  return null;
}

/** 数字归一化：`12,000` / `¥1240` / `1240元` / `(120)`（会计负数）/ `0.5%` 都认，
 *  `1%` 按百分数折成 0.01。表头带「元」的列直接写数字即可。 */
function normNumber(raw) {
  if (isBlank(raw)) return null;
  const t = String(raw).trim();
  const neg = /^\(.*\)$/.test(t);
  const isPct = /%\s*$/.test(t);
  const s = (neg ? t.replace(/[()]/g, '') : t)
    .replace(/[,，\s¥￥$元次条个]/g, '')
    .replace(/%$/, '');
  const n = Number(s);
  if (!Number.isFinite(n)) return null;
  const v = isPct ? n / 100 : n;
  return neg ? -v : v;
}

const round2 = (n) => Math.round(n * 100) / 100;

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) {
    return { error: 'empty', items: [], totals: { row: null, line: 0, rows: 0 }, cols: [], missingColumns: [] };
  }
  const headers = splitRow(raw[0]);
  const cols = headers.map((h) => ({ header: h, role: roleOf(h) }));
  const have = new Set(cols.map((c) => c.role).filter(Boolean));
  const missingColumns = REQUIRED.filter((r) => !have.has(r)).map((r) => LABELS[r]);
  if (missingColumns.length) {
    return { error: 'no_header', items: [], totals: { row: null, line: 0, rows: 0 }, cols, missingColumns };
  }
  const items = [];
  let totalRow = null;
  let totalRows = 0;
  for (let i = 1; i < raw.length; i++) {
    const fields = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i] };
    cols.forEach((c, idx) => {
      if (!c.role) return;
      if (row[c.role] === undefined) row[c.role] = fields[idx] === undefined ? '' : fields[idx];
    });
    if (TOTAL_WORDS.test(cell(fields[0]))) {
      // 一份材料里拼了多期 / 多个客户时会出现多行「合计 / 小计」：只把**最后一行**当对账单总额
      // （对账单总额在最后），前面的是分组小计；行数记进 scope.totals_rows 让人看得见，不静默丢数据。
      totalRow = row;
      totalRows += 1;
    } else {
      items.push(row);
    }
  }
  return {
    items,
    totals: { row: totalRow, line: totalRow ? totalRow.line : 0, rows: totalRows },
    cols,
    missingColumns: [],
  };
}

const num = (row, role) => normNumber(row[role]);

function who(it) {
  const code = cell(it.customerCode) || '(未填客户编码)';
  const name = cell(it.customerName);
  return `客户「${code}${name ? ' ' + name : ''}」订阅 ${cell(it.subscriptionNo) || '(未填订阅号)'}`;
}

function accountKeyOf(it) {
  return `${cell(it.customerCode) || '(未填客户编码)'}|${cell(it.period) || '(未填账期)'}`;
}

/* ============================ 本包执行的检查项 ============================ */

function checkOverageUsageRecompute(it) {
  const quota = num(it, 'planQuota');
  const actual = num(it, 'actualUsage');
  const stated = num(it, 'overageUsage');
  if (quota === null || actual === null || stated === null) return null;
  const expect = round2(Math.max(0, actual - quota));
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '超额用量复算不符', line: it.line,
    amount: 0,
    message: `${who(it)}的超额用量填的是 ${stated}，按 max(0, 实际用量 ${actual} − 套餐额度 ${quota}) `
      + `= ${expect}，相差 ${round2(stated - expect)} ${stated > expect ? '（多算了用量）' : '（少算了用量）'}。`
      + (actual <= quota && stated > 0
        ? '实际用量根本没有超过套餐额度，这一行的超额用量本应是 0 —— 多半是把上月的超额量带过来了。'
        : ''),
    advice: '先确认两件事的**口径**：① 套餐额度是不是本账期的（年付套餐要按 12 个月摊，别整年额度全砸在一个月）；'
      + '② 实际用量是不是"计费口径"（去重、失败请求不计、测试 Key 不计）。'
      + '口径确认后再改超额用量 —— 它是超额费与账单金额的地基，它错一档，整行的钱都跟着错。',
  };
}

function checkOverageFeeRecompute(it) {
  const usage = num(it, 'overageUsage');
  const price = num(it, 'overageUnitPrice');
  const stated = num(it, 'overageFee');
  if (usage === null || price === null || stated === null) return null;
  const expect = round2(usage * price);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '超额费用复算不符', line: it.line,
    amount: round2(Math.abs(stated - expect)),
    message: `${who(it)}的超额费用是 ${stated.toFixed(2)}，按 超额用量 ${usage} × 超额单价 ${price} `
      + `= ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '超额费用是这张表里最容易多收客户钱的一格。三种常见错法：① 单价取错档（调价前后混用、'
      + '阶梯档按错区间）；② 用量按"千次"进位了却按实际量乘；③ 超额用量改过、费用忘了跟着重算。'
      + '请按合同的计价条款逐行复算一遍。',
  };
}

function checkBillAmountRecompute(it) {
  const planFee = num(it, 'planFee');
  const overageFee = num(it, 'overageFee');
  const seatFee = num(it, 'seatFee');
  const discount = num(it, 'discount');
  const stated = num(it, 'billAmount');
  if (planFee === null || overageFee === null || seatFee === null || discount === null || stated === null) return null;
  const expect = round2(planFee + overageFee + seatFee - discount);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '账单金额勾稽不符', line: it.line,
    amount: round2(Math.abs(stated - expect)),
    message: `${who(it)}的账单金额是 ${stated.toFixed(2)}，按 套餐费 ${planFee.toFixed(2)} + 超额费 `
      + `${overageFee.toFixed(2)} + 坐席费 ${seatFee.toFixed(2)} − 折扣 ${discount.toFixed(2)} = ${expect.toFixed(2)}，`
      + `相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '这一格是**要付出去的钱**（客户据此付款、公司据此确认收入）。'
      + '常见错法：折扣减了两次、超额费改过账单没跟着刷新、坐席费漏加。'
      + '请把这一行的加减对到销售合同与订单上，再决定是改哪一格。',
  };
}

function checkQuotaFit(it) {
  const quota = num(it, 'planQuota');
  const actual = num(it, 'actualUsage');
  const planFee = num(it, 'planFee');
  if (quota === null || actual === null) return null;
  if (quota <= 0) return null;
  const ratio = actual / quota;
  if (ratio >= 0.5) return null;
  const waste = round2(quota - actual);
  return {
    level: 'P2', category: '套餐额度远高于实际用量（套餐买大了）', line: it.line,
    amount: round2(planFee === null ? 0 : planFee),
    message: `${who(it)}的套餐额度是 ${quota}，实际用量只有 ${actual}（用了 `
      + `${Math.round(ratio * 100)}%），未用完 ${waste}${planFee === null ? '' : `，本期仍付套餐费 ${planFee.toFixed(2)}`}。`,
    advice: '这不是算错，是**续费时要谈的钱**：连续几期都远低于额度，就该降档或换成按量计费。'
      + '本工具把它列出来只是因为它是下一轮商务谈判最有价值的一条；额度本身没错就不必改。',
  };
}

function checkDuplicateSubscription(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const period = cell(it.period);
    const sub = cell(it.subscriptionNo);
    if (!period || !sub) continue;
    const key = `${period}|${sub}`;
    if (seen.has(key)) {
      const bill = num(it, 'billAmount');
      out.push({
        level: 'P1', category: '同一账期同一订阅号重复行', line: it.line,
        amount: round2(Math.abs(bill === null ? 0 : bill)),
        message: `${period} 的订阅号 ${sub} 在第 ${seen.get(key)} 行已经计过一次，第 ${it.line} 行又出现一次`
          + ' —— 同一份订阅的套餐费、超额费与账单被算了两遍。',
        advice: '先看是不是重复粘贴 / 续费单与变更单一起贴进来了（对账表里最常见）。'
          + '确属同一订阅同一账期分两段计费的（如月中升级），请拆成两行并写清起止日期与各自金额，'
          + '不要共用同一个订阅号。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      const s = cell(it[role]);
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这一行就复算不出来。本工具不会用 0 或默认值替你填：'
            + '没有超额请把超额用量 / 超额单价 / 超额费用都填 0，留空表示"不知道"，两者不能混。',
        });
      }
    }
  }
  return out;
}

/* ===== 以下为订阅版才执行的检查 ===== */

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
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        level: 'P0', category: '合计行与明细之和不符', line: total.line,
        amount: round2(Math.abs(stated - sum)),
        message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，`
          + `相差 ${round2(stated - sum).toFixed(2)}。`,
        advice: '要么明细里漏了整张订阅，要么明细改过合计行没重算（最常见）。'
          + '合计行是对外金额（客户按它付款、财务按它确认收入），先把它与明细对齐，'
          + '再回头找是漏了一行还是改错了一格。',
      });
    }
  }
  return out;
}

function checkDiscountAnomaly(it) {
  const planFee = num(it, 'planFee');
  const seatFee = num(it, 'seatFee');
  const discount = num(it, 'discount');
  const bill = num(it, 'billAmount');
  if (discount === null) return [];
  const out = [];
  if (discount < -TOL) {
    out.push({
      level: 'P0', category: '折扣为负数（实收大于应收）', line: it.line,
      amount: round2(Math.abs(discount)),
      message: `${who(it)}的折扣是 ${discount.toFixed(2)}，是个负数 —— 按 套餐费 + 超额费 + 坐席费 − 折扣 `
        + `算，账单会比标准价**更高**，等于向客户多收钱。`,
      advice: '负折扣有两种正当来源：① 补收上期少收的钱；② 逾期利息。除此之外就是符号填错了。'
        + '请改成正数记折扣、补收另开一行并写明依据，不要在折扣列里用负数表达补收。',
    });
  }
  const base = round2((planFee === null ? 0 : planFee) + (seatFee === null ? 0 : seatFee));
  if (discount > base + TOL) {
    out.push({
      level: 'P1', category: '折扣超过套餐费与坐席费之和（疑似把超额费也打折了）', line: it.line,
      amount: round2(discount - base),
      message: `${who(it)}的折扣是 ${discount.toFixed(2)}，而 套餐费 ${(planFee === null ? 0 : planFee).toFixed(2)} `
        + `+ 坐席费 ${(seatFee === null ? 0 : seatFee).toFixed(2)} 只有 ${base.toFixed(2)}，`
        + `超出 ${round2(discount - base).toFixed(2)} —— 超出部分只能是在给超额费打折`
        + `${bill === null ? '' : `（本行账单 ${bill.toFixed(2)}）`}。`,
      advice: '折扣一般只作用于套餐费与坐席费；超额费是"多用多付"的部分，打了折等于用量越多越便宜。'
        + '请确认合同里折扣的**基数**是什么：只让套餐费打折，超额费按原价算；'
        + '确实约定超额费也打折的，请在备注里写明条款出处。',
    });
  }
  return out;
}

function checkMultiSubscriptionSamePeriod(items) {
  const groups = new Map();
  for (const it of items) {
    const key = accountKeyOf(it);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(it);
  }
  const out = [];
  for (const rows of groups.values()) {
    const subs = [];
    for (const r of rows) {
      const s = cell(r.subscriptionNo);
      if (s && subs.indexOf(s) < 0) subs.push(s);
    }
    const dup = detectDuplicateSubscriptionBilling(rows, subs);
    if (!dup) continue;
    out.push(dup);
  }
  return out;
}

/** 同一客户同一账期多个订阅号**而且坐席费真的被收了不止一份**才算重复开通。
 *  ⛔ 只多一个订阅号不算：SaaS 里同一客户同月既有正式订阅、又有仍开着但已不收费的旧订阅
 *  （试用 / 沉睡账号 / 同一个产品的备用环境）是常态；把它们一律报出来会天天误报，
 *  误报的守卫用两次就没人信了。判据落到"钱"上：坐席费实收金额 > 单份坐席费。 */
function detectDuplicateSubscriptionBilling(rows, subs) {
  const first = rows[0];
  const seatFees = [];
  let total = 0;
  for (const r of rows) {
    const v = num(r, 'seatFee');
    if (v !== null && v > 0) {
      seatFees.push(v);
      total = round2(total + v);
    }
  }
  if (subs.length <= 1) return null;
  let minSeatFee = Infinity;
  for (const v of seatFees) if (v < minSeatFee) minSeatFee = v;
  if (seatFees.length < 2 || !Number.isFinite(minSeatFee) || total <= minSeatFee + TOL) return null;
  return {
    level: 'P1', category: '同一客户同一账期出现多个订阅号', line: first.line,
    amount: total,
    message: `客户「${cell(first.customerCode) || '(未填客户编码)'}」${cell(first.period) || '(未填账期)'} `
      + `出现了 ${subs.length} 个订阅号：${subs.join('、')}（第 ${rows.map((r) => r.line).join('、')} 行），`
      + `其中 ${seatFees.length} 个各自收了坐席费（合计 ${total.toFixed(2)}，单份最少 ${minSeatFee.toFixed(2)}）`
      + ' —— 同一主体被重复开通套餐时，坐席费与套餐费会被收两遍。',
    advice: '续费时旧订阅没关闭、又新开一个订阅，是 SaaS 里最常见的重复收费。'
      + '请确认这几个订阅号是不是同一主体的同一产品：是不同产品线就各留一行（本期无问题）；'
      + '是同一个产品被开了两次，就该关停一个并把重复的坐席费与套餐费退回去。'
      + '只多一个订阅号、且没有重复收费的（如在跑的旧订阅），本工具不报。',
  };
}

function checkQuotaInconsistent(items) {
  const groups = new Map();
  for (const it of items) {
    const key = accountKeyOf(it);
    const quota = num(it, 'planQuota');
    if (quota === null || quota <= 0) continue;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push({ line: it.line, quota, actual: num(it, 'actualUsage'), plan: cell(it.planName), sub: cell(it.subscriptionNo) });
  }
  const out = [];
  for (const [key, rows] of groups.entries()) {
    // ⛔ 判据是**同一个订阅号**在同一客户同一账期出现多个额度 —— 那才是"同一份订阅的口径不一致"
    //    （月中升级没切分、一行填月度额度一行填年度额度）。
    //    不同订阅号额度不同是**正常的**：不同产品线、不同档位、不同坐席数本来就各自一个额度。
    //    第一版按"同一客户同一账期"比，把 C001 的两份不同订阅（专业版 10000 / 基础版 5000）
    //    也报成口径不一致 —— 那是误报，会天天响（误报的守卫用两次就没人信了）。
    const bySub = new Map();
    for (const r of rows) {
      const sk = r.sub || '(未填订阅号)';
      if (!bySub.has(sk)) bySub.set(sk, []);
      bySub.get(sk).push(r);
    }
    for (const [sub, srows] of bySub.entries()) {
      const quotas = [];
      for (const r of srows) if (quotas.indexOf(r.quota) < 0) quotas.push(r.quota);
      if (quotas.length <= 1 || srows.length <= 1) continue;
      const last = srows[srows.length - 1];
      let impact = 0;
      for (const r of srows) {
        if (r.actual === null) continue;
        impact += Math.max(0, r.actual - r.quota);
      }
      impact = round2(impact);
      out.push({
        level: 'P1', category: '同一客户同一账期出现多个套餐额度（用量口径不一致）', line: last.line,
        amount: impact,
        message: `客户「${key.split('|')[0]}」${key.split('|')[1]} 的订阅 ${sub} `
          + `在第 ${srows.map((r) => r.line).join('、')} 行填了 ${quotas.length} 个不同的套餐额度：`
          + `${quotas.join(' / ')}${srows.some((r) => r.plan) ? `（套餐：${srows.map((r) => r.plan || '未填').join(' / ')}）` : ''}`
          + ` —— 同一份订阅的额度口径不一致，超额用量就会被算高或算低。`
          + `按各行分别算出的超额用量合计是 ${impact}。`,
        advice: '同一份订阅同一账期的额度通常只有一个（年付按 12 个月摊也是同一个数）。'
          + '出现多个额度多半是：升级 / 降档在月中生效没做切分、一行填的是"月度额度"另一行填的是"年度额度"。'
          + '请按合同的档位与生效日期把额度统一到一个口径上重算超额，'
          + '月中变更的请拆成两行并写清各自起止日期与额度。',
      });
    }
  }
  return out;
}

/** 订阅版专有能力：跨客户 / 跨账期汇总台账 + 按多收金额排序的处理清单（本包结构上没有这一层）。 */
function buildLedger(items, findings) {
  const byKey = new Map();
  const byLine = new Map();
  const byItem = new Map();
  for (const it of items) {
    const key = accountKeyOf(it);
    byLine.set(it.line, key);
    byItem.set(it.line, it);
    if (!byKey.has(key)) {
      byKey.set(key, {
        customer_code: cell(it.customerCode) || '(未填客户编码)',
        customer_name: cell(it.customerName),
        period: cell(it.period) || '(未填账期)',
        rows: 0,
        plan_quota_total: 0, actual_usage_total: 0, overage_usage_total: 0,
        overage_fee_total: 0, plan_fee_total: 0, seat_fee_total: 0,
        discount_total: 0, bill_total: 0, disputed_total: 0, disputes: [],
      });
    }
    const g = byKey.get(key);
    g.rows += 1;
    const add = (field, role) => {
      const v = num(it, role);
      if (v !== null) g[field] = round2(g[field] + v);
    };
    add('plan_quota_total', 'planQuota');
    add('actual_usage_total', 'actualUsage');
    add('overage_usage_total', 'overageUsage');
    add('overage_fee_total', 'overageFee');
    add('plan_fee_total', 'planFee');
    add('seat_fee_total', 'seatFee');
    add('discount_total', 'discount');
    add('bill_total', 'billAmount');
  }
  for (const f of findings) {
    const key = byLine.get(f.line);
    if (!key || !byKey.has(key)) continue;
    const g = byKey.get(key);
    const amt = typeof f.amount === 'number' && Number.isFinite(f.amount) ? round2(f.amount) : 0;
    g.disputed_total = round2(g.disputed_total + amt);
    g.disputes.push({ line: f.line, category: f.category, amount: amt });
  }
  const list = [...byKey.values()].sort((a, b) => (b.bill_total - a.bill_total)
    || String(a.customer_code).localeCompare(String(b.customer_code))
    || String(a.period).localeCompare(String(b.period)));
  for (const g of list) g.disputes.sort((a, b) => (a.line - b.line));
  let disputed = 0;
  for (const g of list) disputed = round2(disputed + g.disputed_total);

  const queue = findings
    .filter((f) => typeof f.amount === 'number' && Number.isFinite(f.amount) && f.amount > TOL)
    .slice()
    .sort((a, b) => (b.amount - a.amount) || (a.line - b.line));
  const actionQueue = queue.map((f, idx) => {
    const it = byItem.get(f.line);
    return {
      rank: idx + 1,
      line: f.line,
      customer_code: it ? (cell(it.customerCode) || '(未填客户编码)') : '(合计行)',
      subscription_no: it ? (cell(it.subscriptionNo) || '(未填订阅号)') : '(合计行)',
      category: f.category,
      level: f.level,
      amount: round2(f.amount),
      advice: f.advice || '',
    };
  });

  return {
    by_account: list,
    accounts: list.length,
    periods: new Set(items.map((it) => cell(it.period))).size,
    rows: items.length,
    disputed_total: disputed,
    action_queue: actionQueue,
    sort_rule: '台账按「账单金额」从大到小（先看金额最大的客户账期——多收钱的绝对额也最大），'
      + '金额相同按客户编码、再按账期；处理清单按涉及金额从大到小，金额相同按原文行号。',
    note: actionQueue.length
      ? '这是出账 / 续费前的处理清单：先按金额从大到小把差异谈清楚、改对（账单勾稽不符与超额费多收优先），'
        + '再按核对后的金额开票收款。'
      : '没有算出带金额的差异 —— 不是"没问题"，是本材料在上述检查项范围内没发现差额；'
        + '范围之外的判断（额度该按哪一档、用量口径对不对、折扣是否已审批）本工具不做。',
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
    return insufficient('没有收到订阅用量与超额计费明细表的正文（text）—— 请把'
      + '「账期 / 客户编码 / 客户名称 / 订阅号 / 套餐名称 / 套餐额度 / 实际用量 / 超额用量 / 超额单价 / '
      + '超额费用 / 套餐费 / 坐席数 / 坐席费 / 折扣 / 账单金额 / 计费状态」这张表（含表头）整段贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `表头缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或每行都是合计行），没有任何订阅用量与超额计费明细行');
  }

  const periods = new Set();
  const customers = new Set();
  for (const it of t.items) {
    periods.add(cell(it.period));
    customers.add(cell(it.customerCode));
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkOverageUsageRecompute(it);
    if (a) findings.push(a);
    const b = checkOverageFeeRecompute(it);
    if (b) findings.push(b);
    const c = checkBillAmountRecompute(it);
    if (c) findings.push(c);
    const d = checkQuotaFit(it);
    if (d) findings.push(d);
    if (paid) {
      const e = checkDiscountAnomaly(it);
      if (e.length) findings.push.apply(findings, e);
    }
  }
  findings.push.apply(findings, checkBlanks(t.items));
  findings.push.apply(findings, checkDuplicateSubscription(t.items));
  if (paid) findings.push.apply(findings, checkMultiSubscriptionSamePeriod(t.items));
  if (paid) findings.push.apply(findings, checkQuotaInconsistent(t.items));
  if (paid) findings.push.apply(findings, checkTotalRow(t.totals, t.items));

  const notRun = [];
  if (!paid) notRun.push.apply(notRun, CHECKS_WITHHELD);
  const checksExecuted = CHECKS_GIVEN.slice();
  if (paid) checksExecuted.push.apply(checksExecuted, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const sums = {};
  for (const role of SUM_ROLES.concat(MONEY_ROLES)) {
    let v = 0;
    for (const it of t.items) {
      const n = num(it, role);
      if (n !== null) v += n;
    }
    sums[role] = round2(v);
  }

  let tierNote = `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`;
  if (paid) {
    tierNote = '完整档执行全部检查项（含合计勾稽、折扣异常与套餐口径判定、'
      + '跨客户 / 跨账期汇总台账与按多收金额排序的处理清单）。';
  }

  const result = {
    status: 'success',
    service_type: 'SAAS_USAGE_BILLING_CHECK',
    scope: {
      checks: checksExecuted,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.size,
      customers: customers.size,
      totals_row: Boolean(t.totals.row),
      totals_rows: t.totals.rows || 0,
      plan_quota_total: sums.planQuota,
      actual_usage_total: sums.actualUsage,
      overage_usage_total: sums.overageUsage,
      overage_fee_total: sums.overageFee,
      plan_fee_total: sums.planFee,
      seat_fee_total: sums.seatFee,
      discount_total: sums.discount,
      bill_total: sums.billAmount,
      statement_bill_total: t.totals.row ? num(t.totals.row, 'billAmount') : null,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periods.size,
      customers: customers.size,
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
    disclaimer: '只核「max(0, 实际用量 − 套餐额度) = 超额用量」「超额用量 × 超额单价 = 超额费用」'
      + '「套餐费 + 超额费 + 坐席费 − 折扣 = 账单金额」这类**表内勾稽**，'
      + '不判断额度该按哪一档报价、超额单价是否符合合同、用量统计口径是否正确、折扣是否已审批'
      + '（以销售合同、计费系统与用量报表为准）；每条结论都带原文行号与订阅号，可由第三方用同一份输入复算。',
  };

  if (paid) {
    const ledger = buildLedger(t.items, findings);
    result.account_ledger = ledger;
    result.action_queue = ledger.action_queue;
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT,
  LABELS, REQUIRED, SUM_ROLES,
};
