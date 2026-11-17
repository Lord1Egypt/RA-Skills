'use strict';
/**
 * saas-vendor-invoice-check-full.js —— 软件服务商账单与用量核对（本包 / 订阅版共用源码）
 *
 * 谁在什么时候必须做这件事：**采购 / 财务 / IT 资产管理员**，在
 * **每月服务商出账、季度用量复盘、续费谈判**这几个固定节点上，都得把这张
 * 「软件服务商账单与用量明细表」核一遍才能付款。
 * 表里每一格都能手算复现，而每次和软件服务商吵的都是这几处：
 *   · 「计费数量」用的是对方系统口径，不是我们这边的席位台账 / 用量报表 ——
 *     离职账号没停用、测试 Key 算了钱、用量按整万次进位 ⇒ 计费数量凭空多出一截；
 *   · 「单价」调价了、阶梯档取错了、合同期内的旧价没用上 ⇒ 单价高于合同单价；
 *   · 「账期月数」按整年收，而合同只剩半年 —— 同一段时间被计了两次；
 *   · 「账单金额 = 计费数量 × 单价 × 账期月数 − 折扣」，明细里任何一处改动忘了带上它，
 *     账单就直接对不上；
 *   · 同一份服务的续费单与变更单一起贴进来，同一账单月份的服务被计了两遍；
 *   · 关键格留空或写「待确认」—— 整行就复算不出来。
 *
 * 表内勾稽（每一步都能被第三方用同一份输入复算）：
 *   无折扣计费额 = 计费数量 × 单价 × 账期月数
 *   账单金额     = 无折扣计费额 − 折扣
 *   合计行各列   = 各明细行逐列相加
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）、
 * **不写任何文件、不读环境变量**。
 *
 * 本包执行 6 项；订阅版追加 5 项（见 CHECKS_WITHHELD），其中最后两项是本包**结构上做不到**的：
 *   · 「差异归因」把无折扣计费额的差异拆成 数量差异 / 单价差异 / 账期差异 三项 ——
 *     本包只有"这一行算错了"，说不清"错在哪一类原因、一共错了多少钱"；
 *   · 「跨服务商 / 跨账单月份汇总台账与按多收金额排序的处理清单」——
 *     本包只有逐行结论，没有汇总层，也就说不清"这个月一共被多收了多少、先找哪家谈"。
 *
 * ⚠️ 本工具**不判断**单价 / 合同单价 / 折扣是否符合合同约定、用量统计口径对不对、
 *    该不该买这些席位 —— 表里的合同单价、合同账期月数、用量、席位数一律**以你填的为准**，
 *    本工具只核表内勾稽与"账单单价 vs 合同单价"这类两列之间的大小关系，
 *    并把可疑处按原文行号与服务编号列出来。
 *
 * 形态说明：本文件用**形态 A**（付费实现集中成一块，块首是一条横线包住的付费检查区注释），
 * 免费包由 `tools/strip_free_engine.py` 把从那条注释到主入口之间的整块
 * 连同运行时的付费分支一起摘掉，摘完的免费包里不留付费函数。
 * ⛔ 注释里不写付费开关那一行的字面量，也不写它的条件语句字面量（摘除工具的残渣断言按字符串包含判定）。
 */

const CHECKS_GIVEN = [
  '账单金额逐行复算（账单金额 = 计费数量 × 单价 × 账期月数 − 折扣）',
  '计费数量与用量 / 席位数核对（按用量计费的对用量，按席位计费的对席位数）',
  '超出合同单价检测（账单单价 > 合同单价 ⇒ 按差额算出多收金额）',
  '同一服务商同一服务编号同一账单月份重复计费检测',
  '合计行与明细行勾稽（合计行各列 = 各明细行逐列相加）',
  '关键字段缺失或为占位符检测',
];

const CHECKS_WITHHELD = [
  '折扣列异常检测（折扣为负 ⇒ 实收大于应收；折扣超过无折扣计费额 ⇒ 折后金额为负）',
  '账期边界检测（账期月数不是 1~12 的整数；同一服务编号的账期重叠 ⇒ 同一时段被计了两次）',
  '同一服务商同一账单月份同一服务项目出现多个服务编号（疑似重复订购，席位与用量被收两遍）',
  '差异归因（把无折扣计费额差异拆成 数量差异 / 单价差异 / 账期差异 三项，给出三项合计与逐行明细）',
  '跨服务商 / 跨账单月份汇总台账与按多收金额排序的处理清单（按服务商 × 账单月份汇总账单金额与多收金额，逐条带原文行号）',
];

const OUT_OF_SCOPE = [
  '判断单价 / 合同单价 / 折扣是否符合合同约定（本工具只核表内算术与"账单单价 vs 合同单价"的大小关系，以你填的合同要素为准）',
  '判断用量统计口径是否正确（去重规则、失败请求算不算、测试 Key 算不算、跨月切分点——本工具不连接任何系统取数）',
  '判断席位台账对不对（谁该有账号、离职账号该不该停、停用月份该不该按比例——本工具不读你的 HR 与 IT 台账）',
  '判断这些服务该不该买、该不该续费（本工具只核账单，不做采购决策）',
  '判断账单是否已开票、是否已付款、有没有逾期（要拿发票与银行流水核，本工具只看这张表）',
  '计算增值税 / 发票税额，或处理跨月调整、红冲与账务分录',
  '读取 Excel / 服务商计费系统 / 财务系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '账单月份\t服务商\t服务项目\t服务编号\t计费方式\t用量\t席位数\t计费数量\t单价\t合同单价\t账期月数\t合同账期月数\t折扣\t账单金额\t付款状态\t备注',
  '2026-05\t云图科技\t协同办公套件\tSV-1001\t按席位\t0\t120\t120\t30.00\t30.00\t1\t1\t0.00\t3600.00\t已付款\t按 120 席位 × 30.00 元/席位/月计费，已与 IT 席位台账核对',
  '2026-05\t云图科技\t接口调用服务\tSV-1002\t按用量\t850000\t0\t850000\t0.02\t0.02\t1\t1\t0.00\t17000.00\t已付款\t按 850000 次 × 0.02 元/次计费，已与我方用量报表核对',
  '2026-05\t恒信软件\t财务核算模块\tSV-2001\t按席位\t0\t25\t25\t480.00\t480.00\t1\t1\t1200.00\t10800.00\t已付款\t25 席位 × 480.00 元，含 1200.00 元年度优惠',
  '2026-06\t云图科技\t协同办公套件\tSV-1001\t按席位\t0\t120\t120\t30.00\t30.00\t1\t1\t0.00\t3600.00\t待付款\t与上月一致，席位无增减',
  '2026-06\t恒信软件\t财务核算模块\tSV-2001\t按席位\t0\t25\t25\t480.00\t480.00\t1\t1\t0.00\t12000.00\t待付款\t本月无优惠',
  '2026-06\t云图科技\t接口调用服务\tSV-1002\t按用量\t920000\t0\t920000\t0.02\t0.02\t1\t1\t0.00\t18400.00\t待付款\t按 920000 次 × 0.02 元/次计费',
  '2026-01\t明远数据\t数据仓库平台年费\tSV-3001\t按席位\t0\t5\t5\t2400.00\t2400.00\t12\t12\t0.00\t144000.00\t已付款\t年付：5 席位 × 2400.00 元 × 12 个月，合同期 2026-01 至 2026-12',
  '合计\t\t\t\t\t1770000\t295\t1770295\t\t\t\t\t1200.00\t209400.00\t\t',
].join('\n');

const TOL = 0.01;

/** 表头 → 角色。⚠️ 这里用**完全相等**匹配（不是子串包含）：
 *  「单价」/「合同单价」、「用量」/「计费数量」、「账期月数」/「合同账期月数」、「账单金额」/「折扣」
 *  互为前缀或高度相似，一旦用子串包含匹配就会互相抢列、静默算错（`tools/header_map_check.py` 就是查这个）。
 *  服务商导出的表头常带空格、全角括号、单位后缀（如「计费数量(次)」），所以先剥掉空格与括号、再去掉单位后缀，最后比。 */
const ROLES = {
  period: ['账单月份', '账期', '计费账期', '账单周期', '所属账期', '出账月份', '计费月份', '所属期间', '期间', '月份'],
  vendor: ['服务商', '服务商名称', '供应商', '供应商名称', '厂商', '厂商名称', '收款方'],
  serviceName: ['服务项目', '服务名称', '项目名称', '产品名称', '软件名称', '服务内容'],
  serviceNo: ['服务编号', '订阅号', '订阅编号', '订单号', '服务ID', '服务id', '合同编号'],
  billingMode: ['计费方式', '计费模式', '计价方式', '计费类型'],
  usage: ['用量', '实际用量', '使用量', '计费用量', '调用量'],
  seats: ['席位数', '坐席数', '席位数量', '坐席数量', '账号数', '用户数'],
  billQty: ['计费数量', '计费量', '开票数量', '计量数量', '计费单位数'],
  unitPrice: ['单价', '计费单价', '账单单价', '开票单价'],
  contractUnitPrice: ['合同单价', '约定单价', '协议单价', '合同价'],
  months: ['账期月数', '计费月数', '账单月数', '计费期数'],
  contractMonths: ['合同账期月数', '合同月数', '约定月数', '合同期数'],
  discount: ['折扣', '折扣金额', '优惠', '优惠金额', '减免', '折让'],
  billAmount: ['账单金额', '应付金额', '应收金额', '本期账单', '开票金额', '账单'],
  payStatus: ['付款状态', '付款情况', '支付状态', '账单状态', '状态'],
  memo: ['备注', '说明', '依据'],
};

const LABELS = {
  period: '账单月份', vendor: '服务商', serviceName: '服务项目', serviceNo: '服务编号',
  billingMode: '计费方式', usage: '用量', seats: '席位数', billQty: '计费数量',
  unitPrice: '单价', contractUnitPrice: '合同单价', months: '账期月数',
  contractMonths: '合同账期月数', discount: '折扣', billAmount: '账单金额',
  payStatus: '付款状态', memo: '备注',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不拿 0 去替你假设"这个月没用量"）。
 *  没有用量 / 没有席位请填 0，不要留空 —— 「填 0」表示"确实没有"，"留空"表示"不知道"，这两者不能混。 */
const REQUIRED = ['period', 'vendor', 'serviceName', 'serviceNo', 'billingMode', 'usage', 'seats',
  'billQty', 'unitPrice', 'contractUnitPrice', 'months', 'contractMonths', 'discount',
  'billAmount', 'payStatus'];

/** 合计行逐列复核的列：**不含单价 / 合同单价 / 账期月数**（加总没有意义）。 */
const SUM_ROLES = ['usage', 'seats', 'billQty', 'discount', 'billAmount'];

const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：|总计：)$/;
const PLACEHOLDER = /^(待填|待补|待定|待确认|待核|xxx|xxx\.xx|\?+|tbd|n\/?a|-+)$/i;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不齐时本工具不做任何认定，也不套用默认值'
      + '（缺一列就报缺列，不会替你按 0 算"这个月没用量"）。',
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
  const h = cell(header).replace(/[\s（）()]/g, '').replace(/(次|条|个|元|万元|人|台|天|席位)$/g, '');
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
      // 一份材料里拼了多个服务商 / 多期账单时会出现多行「合计 / 小计」：只把**最后一行**当账单总额
      // （账单总额在最后），前面的是分组小计；行数记进 scope.totals_rows 让人看得见，不静默丢数据。
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
  const vendor = cell(it.vendor) || '(未填服务商)';
  const name = cell(it.serviceName);
  const no = cell(it.serviceNo) || '(未填服务编号)';
  return `服务商「${vendor}」的 ${name ? name + ' ' : ''}${no}（${cell(it.period) || '(未填账单月份)'}）`;
}

/** 应有数量：按用量计费的对「用量」，按席位计费的对「席位数」。
 *  认不出计费方式就返回 null（**不猜**）—— 宁可不报，也不拿错的口径去指控服务商多收钱。 */
function expectedQty(it) {
  const mode = cell(it.billingMode);
  if (mode.indexOf('用量') >= 0) return num(it, 'usage');
  if (mode.indexOf('席位') >= 0) return num(it, 'seats');
  return null;
}

/* ============================ 本包执行的检查项 ============================ */

function checkBillAmountRecompute(it) {
  const qty = num(it, 'billQty');
  const price = num(it, 'unitPrice');
  const months = num(it, 'months');
  const discount = num(it, 'discount');
  const stated = num(it, 'billAmount');
  if (qty === null || price === null || months === null || discount === null || stated === null) return null;
  const gross = round2(qty * price * months);
  const expect = round2(gross - discount);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '账单金额复算不符', line: it.line,
    amount: round2(Math.abs(stated - expect)),
    message: `${who(it)}的账单金额是 ${stated.toFixed(2)}，按 计费数量 ${qty} × 单价 ${price} × 账期月数 ${months} `
      + `= ${gross.toFixed(2)}，再减折扣 ${discount.toFixed(2)} = ${expect.toFixed(2)}，`
      + `相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '这一格是**要付出去的钱**。三种常见错法：① 计费数量取错（席位数与用量混用、进位规则没做）；'
      + '② 单价调价前后混用；③ 折扣减了两次或忘了减。'
      + '请按合同的计价条款逐行复算一遍，再决定改哪一格 —— 改之前先确认口径，别只把差异抹平。',
  };
}

function checkBillQtyMatch(it) {
  const q0 = expectedQty(it);
  const qty = num(it, 'billQty');
  if (q0 === null || qty === null) return null;
  const price = num(it, 'unitPrice');
  const months = num(it, 'months');
  const unit = price === null || months === null ? null : round2(price * months);
  const diff = round2(qty - q0);
  if (Math.abs(diff) <= TOL) return null;
  const mode = cell(it.billingMode);
  const byUsage = mode.indexOf('用量') >= 0;
  const amount = unit === null ? 0 : round2(Math.abs(diff) * unit);
  return {
    level: 'P1', category: '计费数量与用量或席位数不符', line: it.line,
    amount,
    message: `${who(it)}按「${mode}」计费，${byUsage ? '用量' : '席位数'}是 ${q0}，`
      + `账单上的计费数量却是 ${qty}，相差 ${diff}`
      + `${unit === null ? '' : `（按 单价 ${price} × 账期月数 ${months} = ${unit.toFixed(2)} 元/单位折算，涉及 ${amount.toFixed(2)} 元）`}。`,
    advice: '计费数量是账单的地基。按用量计费的先核口径（去重规则、失败请求算不算、测试 Key 算不算、'
      + '跨月切分点），按席位计费的先核席位台账（离职账号有没有停用、停用月份有没有按比例）。'
      + '合同约定了进位规则的（如按千次进位），请把规则写进备注再对 —— 本工具不会替你猜进位规则。',
  };
}

function checkContractUnitPrice(it) {
  const price = num(it, 'unitPrice');
  const contract = num(it, 'contractUnitPrice');
  if (price === null || contract === null) return null;
  const gap = round2(price - contract);
  if (gap <= TOL) return null;
  const qty = num(it, 'billQty');
  const months = num(it, 'months');
  const hasAll = qty !== null && months !== null;
  const amount = hasAll ? round2(gap * qty * months) : 0;
  return {
    level: 'P0', category: '超出合同单价', line: it.line,
    amount,
    message: `${who(it)}的账单单价是 ${price}，合同单价是 ${contract}，高 ${gap}`
      + `${hasAll ? `；按 计费数量 ${qty} × 账期月数 ${months} 折算，本期多收 ${amount.toFixed(2)}` : ''}。`,
    advice: '单价高于合同价是最直接的多收。两种常见情形：① 服务商调价后按新价计费，'
      + '而合同期内应沿用旧价（看调价生效日与合同期）；② 阶梯价取错档（用量落在低价档却按高价档收）。'
      + '请按合同计价条款确认本期适用单价，再决定是要求开红字还是在下期抵扣。',
  };
}

function checkDuplicateCharge(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const vendor = cell(it.vendor);
    const no = cell(it.serviceNo);
    const period = cell(it.period);
    if (!vendor || !no || !period) continue;
    const key = `${vendor}|${no}|${period}`;
    if (seen.has(key)) {
      const bill = num(it, 'billAmount');
      out.push({
        level: 'P1', category: '同一服务商同一服务编号同一账单月份重复计费', line: it.line,
        amount: round2(Math.abs(bill === null ? 0 : bill)),
        message: `${vendor} 的服务编号 ${no} 在 ${period} 这份账单里第 ${seen.get(key)} 行已经计过一次，`
          + `第 ${it.line} 行又出现一次 —— 同一份服务的账单被算了两遍。`,
        advice: '先看是不是续费单与变更单一起贴进来了、或者同一张账单复制了两遍（对账表里最常见）。'
          + '确属同一服务同一账期分两段计费的（如月中扩席位），请拆成两行并写清各自起止日期与数量，'
          + '不要共用同一个服务编号与账单月份。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

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
        level: 'P0', category: '合计行与明细行不符', line: total.line,
        amount: round2(Math.abs(stated - sum)),
        message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，`
          + `相差 ${round2(stated - sum).toFixed(2)}。`,
        advice: '要么明细里漏了整份服务，要么明细改过合计行没重算（最常见）。'
          + '合计行是对外金额（财务按它付款、按它入账），先把它与明细对齐，'
          + '再回头找是漏了一行还是改错了一格。',
      });
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
            + '没有用量 / 没有席位请填 0，留空表示"不知道"，两者不能混。',
        });
      }
    }
  }
  return out;
}

/* ===== 以下为订阅版才执行的检查 ===== */

function checkDiscountAnomaly(it) {
  const discount = num(it, 'discount');
  if (discount === null) return [];
  const out = [];
  if (discount < -TOL) {
    out.push({
      level: 'P0', category: '折扣为负数（实收大于应收）', line: it.line,
      amount: round2(Math.abs(discount)),
      message: `${who(it)}的折扣是 ${discount.toFixed(2)}，是个负数 —— 按 无折扣计费额 − 折扣 算，`
        + '账单会比标准价**更高**，等于向服务商多付钱。',
      advice: '负折扣有两种正当来源：① 补付上期少付的钱；② 逾期利息。除此之外就是符号填错了。'
        + '请改成正数记折扣、补付另开一行并写明依据，不要在折扣列里用负数表达。',
    });
  }
  const qty = num(it, 'billQty');
  const price = num(it, 'unitPrice');
  const months = num(it, 'months');
  if (qty !== null && price !== null && months !== null) {
    const gross = round2(qty * price * months);
    if (discount > gross + TOL) {
      out.push({
        level: 'P1', category: '折扣超过无折扣计费额（折后金额为负）', line: it.line,
        amount: round2(discount - gross),
        message: `${who(it)}的折扣是 ${discount.toFixed(2)}，而 无折扣计费额 `
          + `（计费数量 ${qty} × 单价 ${price} × 账期月数 ${months}）只有 ${gross.toFixed(2)}，`
          + `超出 ${round2(discount - gross).toFixed(2)} —— 折后金额成了负数。`,
        advice: '折扣超过应计金额，要么是折扣多填了一位数、要么是把别的东西（补付、抵扣券、上期红字）'
          + '混进了折扣列。请把每一项拆成独立行并在备注里写明依据，再重算账单金额。',
      });
    }
  }
  return out;
}

/** `YYYY-MM` / `YYYYMM` / `YYYY/M` / `YYYY年M月` → 绝对月序号（年 × 12 + 月 − 1）。认不出返回 null。 */
function monthIndex(raw) {
  const s = cell(raw);
  let m = s.match(/^(\d{4})\s*[-/.年]\s*(\d{1,2})\s*月?$/);
  if (!m) m = s.match(/^(\d{4})(\d{2})$/);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  if (!Number.isFinite(y) || !Number.isFinite(mo) || mo < 1 || mo > 12) return null;
  return y * 12 + (mo - 1);
}

function checkPeriodBoundary(items) {
  const out = [];
  for (const it of items) {
    const m = num(it, 'months');
    if (m === null) continue;
    if (!Number.isInteger(m) || m < 1 || m > 12) {
      out.push({
        level: 'P1', category: '账期月数非法（不是 1~12 的整数）', line: it.line,
        amount: 0,
        message: `${who(it)}的账期月数是 ${m}，不是 1~12 的整数 —— 账期月数决定这一行按几个月计费，`
          + '它错一档，账单金额就整行错。',
        advice: '账期月数应与合同约定的计费周期一致：月付填 1、季付填 3、年付填 12。'
          + '月中生效 / 中途变更的请拆成两行并写清各自起止月份，不要用小数或 0 表达"半个月"。',
      });
    }
  }
  const groups = new Map();
  for (const it of items) {
    const key = `${cell(it.vendor)}|${cell(it.serviceNo)}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(it);
  }
  for (const rows of groups.values()) {
    if (rows.length < 2) continue;
    const spans = [];
    for (const r of rows) {
      const start = monthIndex(cell(r.period));
      const m = num(r, 'months');
      if (start === null || m === null || m < 1) continue;
      spans.push({ it: r, start, end: start + m });
    }
    for (let i = 0; i < spans.length; i++) {
      for (let j = i + 1; j < spans.length; j++) {
        const lo = spans[i].start <= spans[j].start ? spans[i] : spans[j];
        const hi = spans[i].start <= spans[j].start ? spans[j] : spans[i];
        if (hi.start >= lo.end) continue;
        const overlap = Math.min(lo.end, hi.end) - hi.start;
        const price = num(hi.it, 'contractUnitPrice');
        const qty = expectedQty(hi.it);
        const amount = price === null || qty === null ? 0 : round2(overlap * qty * price);
        out.push({
          level: 'P1', category: '同一服务编号账期重叠（同一时段被计了两次）', line: hi.it.line,
          amount,
          message: `服务商「${cell(hi.it.vendor)}」的服务编号 ${cell(hi.it.serviceNo)} 的账期重叠了：`
            + `第 ${lo.it.line} 行（${cell(lo.it.period)} 起 ${lo.end - lo.start} 个月）与 `
            + `第 ${hi.it.line} 行（${cell(hi.it.period)} 起 ${hi.end - hi.start} 个月）有 ${overlap} 个月是同一时段。`,
          advice: '同一编号的账期本该首尾相接、不重叠。重叠通常来自：① 续费时上一期没结束就开了新一期；'
            + '② 合同只剩半年却按整年收（账期月数没跟着合同期改）；③ 月中变更没做切分。'
            + '请按合同起止日期把账期拆干净，重叠部分要求红字或下期抵扣。',
        });
      }
    }
  }
  return out;
}

function checkMultiServiceNoSamePeriod(items) {
  const groups = new Map();
  for (const it of items) {
    const key = `${cell(it.vendor)}|${cell(it.period)}|${cell(it.serviceName)}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(it);
  }
  const out = [];
  for (const rows of groups.values()) {
    const nos = [];
    for (const r of rows) {
      const s = cell(r.serviceNo);
      if (s && nos.indexOf(s) < 0) nos.push(s);
    }
    if (nos.length <= 1) continue;
    // ⛔ 判据落到"钱"上：同一服务商同一账单月份同一服务项目出现多个编号**而且真的都收了钱**
    //    才算疑似重复订购。只多一个编号不算（同月既有正式订购、又有仍在跑但不收费的试用环境是常态），
    //    一律报出来会天天误报 —— 误报的守卫用两次就没人信了。
    const charged = rows.filter((r) => {
      const v = num(r, 'billAmount');
      return v !== null && v > TOL;
    });
    if (charged.length < 2) continue;
    let total = 0;
    for (const r of charged) {
      const v = num(r, 'billAmount');
      total = round2(total + (v === null ? 0 : v));
    }
    const lines = rows.map((r) => r.line).join('、');
    out.push({
      level: 'P1', category: '同一服务商同一账单月份同一服务项目出现多个服务编号', line: charged[charged.length - 1].line,
      amount: total,
      message: `服务商「${cell(rows[0].vendor)}」的 ${cell(rows[0].period)} 这份账单里，`
        + `服务项目「${cell(rows[0].serviceName)}」出现了 ${nos.length} 个服务编号：${nos.join('、')}`
        + `（第 ${lines} 行），其中 ${charged.length} 个各自收了钱（合计 ${total.toFixed(2)}）`
        + ' —— 同一主体被重复订购时，席位费与用量费会被收两遍。',
      advice: '续费时旧订购没关闭、又新开一个编号，是软件采购里最常见的重复收费。'
        + '请确认这几个编号是不是同一产品的同一环境：是不同产品线 / 不同环境就各留一行（本期无问题）；'
        + '是同一个被订了两次，就该关停一个并把重复的费用退回来。'
        + '只多一个编号、且没有重复收费的，本工具不报。',
    });
  }
  return out;
}

/** 订阅版专有：把每行「无折扣计费额」的差异做**链式分解**（逐项替换，和恒等于总差异）。
 *  第 1 步换数量、第 2 步换单价、第 3 步换账期月数，每一步的差额就是该类原因的贡献：
 *    数量差异 = (计费数量 − 应有数量) × 账单单价 × 账单账期月数
 *    单价差异 = 应有数量 × (账单单价 − 合同单价) × 账单账期月数
 *    账期差异 = 应有数量 × 合同单价 × (账单账期月数 − 合同账期月数)
 *  三项之和 = 无折扣计费额差异（数学上恒等；逐项四舍五入后以三项之和为准）。
 *  ⚠️ 折扣是合同的合法减项，**不计入**上述三项，单列在 discount_total 里；
 *     折扣本身异常（负数 / 超过计费额）由「折扣列异常检测」负责。 */
function attributionOf(it) {
  const q = num(it, 'billQty');
  const p = num(it, 'unitPrice');
  const m = num(it, 'months');
  const q0 = expectedQty(it);
  const p0 = num(it, 'contractUnitPrice');
  const m0 = num(it, 'contractMonths');
  if (q === null || p === null || m === null || q0 === null || p0 === null || m0 === null) return null;
  const qty = round2((q - q0) * p * m);
  const price = round2(q0 * (p - p0) * m);
  const term = round2(q0 * p0 * (m - m0));
  return {
    line: it.line,
    vendor: cell(it.vendor) || '(未填服务商)',
    service_no: cell(it.serviceNo) || '(未填服务编号)',
    bill_qty: q,
    expected_qty: q0,
    unit_price: p,
    contract_unit_price: p0,
    months: m,
    contract_months: m0,
    qty_variance: qty,
    price_variance: price,
    term_variance: term,
    gross_variance: round2(qty + price + term),
    gross_stated: round2(q * p * m),
    bill_amount: num(it, 'billAmount'),
    discount: num(it, 'discount'),
  };
}

function buildVarianceAttribution(items) {
  const rows = [];
  for (const it of items) {
    const r = attributionOf(it);
    if (r) rows.push(r);
  }
  let qty = 0;
  let price = 0;
  let term = 0;
  let gross = 0;
  let grossStated = 0;
  let bill = 0;
  let discount = 0;
  let stated = 0;
  for (const r of rows) {
    qty = round2(qty + r.qty_variance);
    price = round2(price + r.price_variance);
    term = round2(term + r.term_variance);
    gross = round2(gross + r.gross_variance);
    grossStated = round2(grossStated + r.gross_stated);
    bill = round2(bill + r.gross_variance);
    discount = round2(discount + (r.discount === null ? 0 : r.discount));
    stated = round2(stated + (r.bill_amount === null ? 0 : r.bill_amount));
  }
  const byLine = rows.filter((r) => Math.abs(r.gross_variance) > TOL);
  return {
    rows,
    rows_attributed: rows.length,
    rows_with_variance: byLine.length,
    totals: {
      qty_variance_total: qty,
      price_variance_total: price,
      term_variance_total: term,
      gross_variance_total: gross,
      gross_stated_total: grossStated,
      discount_total: discount,
      bill_stated_total: stated,
      bill_contract_total: round2(stated - bill),
      bill_variance_total: bill,
    },
    by_cause: [
      { cause: '数量差异（计费数量 vs 用量 / 席位数）', amount: qty },
      { cause: '单价差异（账单单价 vs 合同单价）', amount: price },
      { cause: '账期差异（账单账期月数 vs 合同账期月数）', amount: term },
    ],
    worst: byLine.slice().sort((a, b) => Math.abs(b.gross_variance) - Math.abs(a.gross_variance) || (a.line - b.line)).slice(0, 5),
    identity: '数量差异 + 单价差异 + 账期差异 = 无折扣计费额差异（链式分解，逐项四舍五入后以三项之和为准）',
    note: byLine.length
      ? '差异已经归因到数量 / 单价 / 账期三类原因上，按金额从大到小处理即可；折扣是合法减项，未计入这三类。'
      : '本材料在上述检查项范围内没有算出无折扣计费额差异 —— 不是"没问题"，而是这三类原因上都没算出差额；'
        + '范围之外的判断（单价是否符合合同约定、用量口径对不对、折扣是否已审批）本工具不做。',
  };
}

/** 订阅版专有能力：跨服务商 / 跨账单月份汇总台账 + 按多收金额排序的处理清单（本包结构上没有这一层）。 */
function buildLedger(items, findings) {
  const byKey = new Map();
  const byLine = new Map();
  const byItem = new Map();
  for (const it of items) {
    const key = `${cell(it.vendor) || '(未填服务商)'}|${cell(it.period) || '(未填账单月份)'}`;
    byLine.set(it.line, key);
    byItem.set(it.line, it);
    if (!byKey.has(key)) {
      byKey.set(key, {
        vendor: cell(it.vendor) || '(未填服务商)',
        period: cell(it.period) || '(未填账单月份)',
        rows: 0,
        usage_total: 0, seats_total: 0, bill_qty_total: 0,
        discount_total: 0, bill_total: 0, disputed_total: 0, disputes: [],
      });
    }
    const g = byKey.get(key);
    g.rows += 1;
    const add = (field, role) => {
      const v = num(it, role);
      if (v !== null) g[field] = round2(g[field] + v);
    };
    add('usage_total', 'usage');
    add('seats_total', 'seats');
    add('bill_qty_total', 'billQty');
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
    || String(a.vendor).localeCompare(String(b.vendor))
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
      vendor: it ? (cell(it.vendor) || '(未填服务商)') : '(合计行)',
      service_no: it ? (cell(it.serviceNo) || '(未填服务编号)') : '(合计行)',
      category: f.category,
      level: f.level,
      amount: round2(f.amount),
      advice: f.advice || '',
    };
  });

  return {
    by_vendor_period: list,
    groups: list.length,
    vendors: new Set(items.map((it) => cell(it.vendor))).size,
    periods: new Set(items.map((it) => cell(it.period))).size,
    rows: items.length,
    disputed_total: disputed,
    action_queue: actionQueue,
    sort_rule: '台账按「账单金额」从大到小（先看金额最大的服务商账期——被多收的绝对额也最大），'
      + '金额相同按服务商、再按账单月份；处理清单按涉及金额从大到小，金额相同按原文行号。',
    note: actionQueue.length
      ? '这是付款前的处理清单：先按金额从大到小把差异找服务商谈清楚、改对（账单勾稽不符与超合同单价优先），'
        + '再按核对后的金额付款。'
      : '没有算出带金额的差异 —— 不是"没问题"，是本材料在上述检查项范围内没发现差额；'
        + '范围之外的判断（单价是否符合合同约定、用量口径对不对、折扣是否已审批）本工具不做。',
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
    return insufficient('没有收到软件服务商账单与用量明细表的正文（text）—— 请把'
      + '「账单月份 / 服务商 / 服务项目 / 服务编号 / 计费方式 / 用量 / 席位数 / 计费数量 / 单价 / '
      + '合同单价 / 账期月数 / 合同账期月数 / 折扣 / 账单金额 / 付款状态」这张表（含表头）整段贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `表头缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或每行都是合计行），没有任何账单与用量明细行');
  }

  const vendors = new Set();
  const periods = new Set();
  for (const it of t.items) {
    vendors.add(cell(it.vendor));
    periods.add(cell(it.period));
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkBillAmountRecompute(it);
    if (a) findings.push(a);
    const b = checkBillQtyMatch(it);
    if (b) findings.push(b);
    const c = checkContractUnitPrice(it);
    if (c) findings.push(c);
    if (paid) {
      const d = checkDiscountAnomaly(it);
      if (d.length) findings.push.apply(findings, d);
    }
  }
  findings.push.apply(findings, checkBlanks(t.items));
  findings.push.apply(findings, checkDuplicateCharge(t.items));
  findings.push.apply(findings, checkTotalRow(t.totals, t.items));
  if (paid) findings.push.apply(findings, checkPeriodBoundary(t.items));
  if (paid) findings.push.apply(findings, checkMultiServiceNoSamePeriod(t.items));

  const notRun = [];
  if (!paid) notRun.push.apply(notRun, CHECKS_WITHHELD);
  const checksExecuted = CHECKS_GIVEN.slice();
  if (paid) checksExecuted.push.apply(checksExecuted, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const sums = {};
  for (const role of SUM_ROLES) {
    let v = 0;
    for (const it of t.items) {
      const n = num(it, role);
      if (n !== null) v += n;
    }
    sums[role] = round2(v);
  }

  let tierNote = `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`;
  if (paid) {
    tierNote = '完整档执行全部检查项（含折扣异常与账期边界判定、同一服务项目的多编号判定、'
      + '差异归因，以及跨服务商 / 跨账单月份汇总台账与按多收金额排序的处理清单）。';
  }

  const result = {
    status: 'success',
    service_type: 'SAAS_VENDOR_INVOICE_CHECK',
    scope: {
      checks: checksExecuted,
      checks_not_run: notRun,
      rows: t.items.length,
      vendors: vendors.size,
      periods: periods.size,
      totals_row: Boolean(t.totals.row),
      totals_rows: t.totals.rows || 0,
      usage_total: sums.usage,
      seats_total: sums.seats,
      bill_qty_total: sums.billQty,
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
      vendors: vendors.size,
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
    disclaimer: '只核「计费数量 × 单价 × 账期月数 − 折扣 = 账单金额」这类**表内勾稽**，'
      + '外加「账单单价 vs 合同单价」「计费数量 vs 用量 / 席位数」这两组两列之间的对照；'
      + '不判断单价是否符合合同约定、用量统计口径是否正确、席位台账对不对、折扣是否已审批'
      + '（以采购合同、服务商计费系统与我方用量报表为准）；'
      + '每条结论都带原文行号与服务编号，可由第三方用同一份输入复算。',
  };

  if (paid) {
    result.variance_attribution = buildVarianceAttribution(t.items);
    const ledger = buildLedger(t.items, findings);
    result.vendor_ledger = ledger;
    result.action_queue = ledger.action_queue;
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT,
  LABELS, REQUIRED, SUM_ROLES,
};
