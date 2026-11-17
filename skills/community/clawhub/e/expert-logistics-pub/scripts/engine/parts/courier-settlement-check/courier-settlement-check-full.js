'use strict';
/**
 * courier-settlement-check-full.js —— 网点运费与代收货款结算核对（本包 / 订阅版共用源码）
 *
 * 谁在什么时候必须做这件事：**快递 / 快运网络的网点（加盟商、分公司）每月与总部结算时**。
 * 一张结算单上每一格都能手算复现，而每月都吵的就是这几处：
 *   · 运费按「计费重量 × 计费单价」算，计费重量却比实际重量还小 —— 运费少收，总部与网点各说各话；
 *   · 代收货款（COD）是网点替寄件人收的钱，结算时必须先扣掉代收手续费、再把净额上缴；
 *     手续费率用错、净额算错、甚至漏扣，都是真金白银；
 *   · 同一张运单被录进两行（重复粘贴最常见），运费与代收货款一起算了两遍；
 *   · 计费重量 / 单价 / 费率这些关键格留空或是「待填」，整行就复算不出来。
 *
 * 表内勾稽（每一步都能被第三方用同一份输入复算）：
 *   运费           = 计费重量 × 计费单价
 *   代收手续费     = 代收货款 × 代收手续费率
 *   代收货款应缴   = 代收货款 − 代收手续费
 *   应结金额       = 运费 + 派费 + 附加费 − 中转费 − 代收货款应缴
 *   合计行各列     = 各明细行逐列相加（订阅版）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）、**不写任何文件、不读环境变量**。
 *
 * 本包执行 6 项；订阅版追加 5 项（见 CHECKS_WITHHELD），其中最后一项是本包**结构上做不到**的：
 * 「跨网点汇总台账与按金额排序的差异处理清单」—— 本包只有逐行结论，没有跨网点的汇总层。
 *
 * ⚠️ 本工具**不判断**计费单价该按什么合同档位、抛比（体积重）怎么取、代收手续费率是否符合代收协议、
 *    代收货款是否真的收到并转付（那属于运价合同、代收协议与银行流水的核定）：表里的计费重量、计费单价、
 *    代收货款、费率、派费、中转费一律**以你填的为准**，本工具只核表内勾稽，并把可疑处按原文行号与运单号列出来。
 *
 * 形态说明：本文件用**形态 A**（付费实现集中成一块，块首是一条横线包住的付费检查区注释），
 * 免费包由 `tools/strip_free_engine.py` 把从那条注释到主入口之间的整块
 * 连同运行时的付费分支一起摘掉，摘完的免费包里不留付费函数。
 * ⛔ 注释里不写付费开关那一行的字面量，也不写它的条件语句字面量（摘除工具的残渣断言按字符串包含判定）。
 */

const CHECKS_GIVEN = [
  '运费复算（计费重量 × 计费单价 = 运费）',
  '代收货款扣减复算（代收手续费 = 代收货款 × 代收手续费率；代收货款应缴 = 代收货款 − 代收手续费）',
  '应结金额复算（运费 + 派费 + 附加费 − 中转费 − 代收货款应缴 = 应结金额）',
  '计费重量低于实际重量检测（少计费、运费少收）',
  '同一网点同一期间同一运单号重复行检测',
  '关键字段缺失或为占位符检测',
];

const CHECKS_WITHHELD = [
  '合计行勾稽（合计行各列 = 各明细行逐列相加，不符时报出差异金额并定位差异单）',
  '代收货款上缴缺口判定（代收货款 − 代收手续费 大于 代收货款应缴 ⇒ 应追缴；应缴大于代收货款 ⇒ 多缴）',
  '同一网点同一期间同一代收货款单号重复计扣判定',
  '代收手续费率不一致判定（同一网点同一期间出现多个费率 ⇒ 按其中最低费率折算多计的手续费差额）',
  '跨网点汇总台账与差异处理清单（按网点 × 期间汇总运费 / 代收货款 / 应缴 / 应结与争议金额，按金额排序，逐条带原文行号）',
];

const OUT_OF_SCOPE = [
  '判断计费单价该按什么合同档位、抛比（体积重）怎么取、网点与总部的分成比例是否合理（本工具只核表内算术，以你填的计费重量与单价为准）',
  '判断代收货款是否真的收到、是否已转付给寄件人、有没有被挪占（要拿银行流水与代收货款台账核，本工具不连接任何系统取数）',
  '判断代收手续费率是否符合代收协议约定（本工具只做同一网点同一期间的多费率比对，不替你认定合同费率）',
  '判断回单（签收单）是否齐全、货损货差该不该赔（那属于业务凭证核定）',
  '计算增值税 / 发票税额，或处理跨月调整、红冲与账务分录',
  '读取 Excel / 快递系统 / 财务系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '结算期间\t网点编码\t网点名称\t运单号\t计费重量\t实际重量\t计费单价\t运费\t派费\t中转费\t附加费\t代收货款\t代收手续费率\t代收手续费\t代收货款应缴\t应结金额\t代收货款单号\t备注',
  '2026-05\tSH-A\t沪东网点\tYD2026050001\t12.5\t11.8\t4.00\t50.00\t3.00\t8.00\t2.00\t800.00\t0.01\t8.00\t792.00\t-745.00\tCOD2026050001\t代收货款已随日报上缴',
  '2026-05\tSH-A\t沪东网点\tYD2026050002\t6.0\t5.6\t4.00\t24.00\t3.00\t5.00\t0.00\t0.00\t0.0000\t0.00\t0.00\t22.00\t\t',
  '2026-05\tSH-A\t沪东网点\tYD2026050003\t20.0\t20.0\t3.50\t70.00\t3.00\t12.00\t4.00\t1200.00\t0.01\t12.00\t1188.00\t-1123.00\tCOD2026050003\t代收货款已随日报上缴',
  '2026-05\tJS-B\t苏南网点\tYD2026050004\t8.4\t7.9\t4.20\t35.28\t3.50\t6.00\t0.00\t0.00\t0.0000\t0.00\t0.00\t32.78\t\t',
  '2026-05\tJS-B\t苏南网点\tYD2026050005\t15.0\t14.2\t4.20\t63.00\t3.50\t9.00\t1.50\t500.00\t0.01\t5.00\t495.00\t-436.00\tCOD2026050005\t代收货款已随日报上缴',
  '2026-06\tSH-A\t沪东网点\tYD2026060001\t10.0\t9.5\t4.00\t40.00\t3.00\t7.00\t0.00\t300.00\t0.01\t3.00\t297.00\t-261.00\tCOD2026060001\t代收货款已随日报上缴',
  '合计\t\t\t\t71.9\t69.0\t\t282.28\t19.00\t47.00\t7.50\t2800.00\t\t28.00\t2772.00\t-2510.22\t\t',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前，兜底的宽泛别名在后。
  //    「代收货款单号」必须排在「运单号」前（否则单号被 waybill 的「单号」抢走）；
  //    「计费重量」必须排在「重量」前；「代收手续费率」→「代收手续费」→「代收货款应缴」→「代收货款」逐级收窄；
  //    「结算期间」排最前，避免「网点名称」之类的宽泛词先命中。
  period: ['结算期间', '所属期间', '费用期间', '账期', '所属月份', '结算月份', '期间', '月份', '月度'],
  siteCode: ['网点编码', '网点代码', '网点编号', '机构编码', '站点编码', '网点号'],
  siteName: ['网点名称', '网点简称', '机构名称', '站点名称', '网点', '站点'],
  codNo: ['代收货款单号', '代收单号', '货款单号', 'COD单号', '代收编号'],
  waybill: ['运单编号', '运单号', '快递单号', '面单号', '运单'],
  chargeWeight: ['计费重量', '结算重量', '计费重'],
  weight: ['实际重量', '实重', '货物重量', '毛重', '重量'],
  unitPrice: ['计费单价', '结算单价', '运价', '单价'],
  freight: ['运费金额', '运输费用', '快递费', '运费'],
  deliveryFee: ['派送费', '派件费', '末端派费', '派费'],
  transitFee: ['中转费用', '转运费', '中转费', '中转'],
  surcharge: ['附加费用', '其他费用', '加收费用', '超区费', '附加费'],
  codRate: ['代收手续费率', '代收服务费率', '手续费率', '代收费率'],
  codFee: ['代收手续费', '代收服务费', '手续费'],
  codRemit: ['代收货款应缴', '代收货款上缴', '应缴代收货款', '代收货款净额', '代收净额', '上缴金额'],
  codAmount: ['代收货款金额', '代收货款', '代收金额', '货款金额', '代收'],
  payable: ['应结金额', '应结货款', '结算金额', '应付金额', '应结'],
  memo: ['备注', '说明', '扣款说明', '依据'],
};

const LABELS = {
  period: '结算期间', siteCode: '网点编码', siteName: '网点名称', codNo: '代收货款单号',
  waybill: '运单号', chargeWeight: '计费重量', weight: '实际重量', unitPrice: '计费单价',
  freight: '运费', deliveryFee: '派费', transitFee: '中转费', surcharge: '附加费',
  codRate: '代收手续费率', codFee: '代收手续费', codRemit: '代收货款应缴', codAmount: '代收货款',
  payable: '应结金额', memo: '备注',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不拿 0 去替你假设"这笔没有代收货款"）。
 *  非代收货款运单请把「代收货款 / 代收手续费率 / 代收手续费 / 代收货款应缴」都填 0，不要留空 ——
 *  「填 0」表示"确实没有"，"留空"表示"不知道"，这两者不能混。 */
const REQUIRED = ['period', 'siteCode', 'waybill', 'chargeWeight', 'weight', 'unitPrice',
  'freight', 'deliveryFee', 'transitFee', 'surcharge', 'codAmount', 'codRate', 'codFee',
  'codRemit', 'payable'];

/** 合计行逐列复核的列：**不含计费单价与代收手续费率**（比率加总没有意义，它们另做一致性判定）。 */
const SUM_ROLES = ['chargeWeight', 'freight', 'deliveryFee', 'transitFee', 'surcharge',
  'codAmount', 'codFee', 'codRemit', 'payable'];

const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：|总计：)$/;
const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a|-+)$/i;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不齐时本工具不做任何认定，也不套用默认值'
      + '（缺一列就报缺列，不会替你按 0 算"这笔没有代收货款"）。',
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

function roleOf(header) {
  const h = cell(header).replace(/[\s（）()]/g, '');
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

/** 数字归一化：`1,240.00` / `¥1240` / `(1240)`（会计负数）/ `1%` 都认。`1%` 按百分数折成 0.01。
 *  费率列写 `0.01` 或 `1%` 都行；写 `1` 表示 100%，本工具不会替你猜。 */
function normNumber(raw) {
  if (isBlank(raw)) return null;
  const t = String(raw).trim();
  const neg = /^\(.*\)$/.test(t);
  const isPct = /%\s*$/.test(t);
  const s = (neg ? t.replace(/[()]/g, '') : t).replace(/[,，\s¥￥$%]/g, '');
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
      // 一份材料里拼了多期 / 多个网点时会出现多行「合计 / 小计」：只把**最后一行**当对账单总额
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
  const code = cell(it.siteCode) || '(未填网点编码)';
  const name = cell(it.siteName);
  return `网点「${code}${name ? ' ' + name : ''}」运单 ${cell(it.waybill) || '(未填运单号)'}`;
}

function siteKeyOf(it) {
  return `${cell(it.siteCode) || '(未填网点编码)'}|${cell(it.period) || '(未填期间)'}`;
}

/* ============================ 本包执行的检查项 ============================ */

function checkFreightRecompute(it) {
  const qty = num(it, 'chargeWeight');
  const price = num(it, 'unitPrice');
  const stated = num(it, 'freight');
  if (qty === null || price === null || stated === null) return null;
  const expect = round2(qty * price);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '运费复算不符', line: it.line,
    amount: round2(Math.abs(stated - expect)),
    message: `${who(it)}的运费是 ${stated.toFixed(2)}，按 计费重量 ${qty} × 计费单价 ${price} = ${expect.toFixed(2)}，`
      + `相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '运费是后面所有加减项的地基。先确认这张单的计费重量是不是取错了（抛比 / 体积重 / 续重进位），'
      + '再对一遍单价档，最后改运费 —— 计费重量或单价错一档，整车的运费都跟着错。',
  };
}

function checkCodFeeRecompute(it) {
  const amount = num(it, 'codAmount');
  const rate = num(it, 'codRate');
  const stated = num(it, 'codFee');
  if (amount === null || rate === null || stated === null) return null;
  const expect = round2(amount * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '代收手续费复算不符', line: it.line,
    amount: round2(Math.abs(stated - expect)),
    message: `${who(it)}的代收手续费是 ${stated.toFixed(2)}，按 代收货款 ${amount.toFixed(2)} × 费率 `
      + `${round2(rate * 100)}% = ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '代收手续费是网点做代收业务的收入，也是总部与网点每月最容易吵的一项。'
      + '先确认这张单的费率档（不同代收金额 / 不同客户可能分档），再改手续费；'
      + '费率列写小数（0.01）或百分数（1%）都认，但别把 1% 写成 1。',
  };
}

function checkCodRemitRecompute(it) {
  const amount = num(it, 'codAmount');
  const fee = num(it, 'codFee');
  const stated = num(it, 'codRemit');
  if (amount === null || fee === null || stated === null) return null;
  const expect = round2(amount - fee);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '代收货款应缴复算不符', line: it.line,
    amount: round2(Math.abs(stated - expect)),
    message: `${who(it)}的代收货款应缴是 ${stated.toFixed(2)}，按 代收货款 ${amount.toFixed(2)} − 代收手续费 `
      + `${fee.toFixed(2)} = ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '这一格是要从网点划给总部的钱：代收货款是替寄件人收的，只有手续费能留下。'
      + '常见错法：手续费扣了却又没从应缴里减、或者把手续费重复减了两次。请按代收台账一笔一笔对。',
  };
}

function checkPayableRecompute(it) {
  const freight = num(it, 'freight');
  const delivery = num(it, 'deliveryFee');
  const transit = num(it, 'transitFee');
  const surcharge = num(it, 'surcharge');
  const remit = num(it, 'codRemit');
  const stated = num(it, 'payable');
  if (freight === null || delivery === null || transit === null || surcharge === null
    || remit === null || stated === null) return null;
  const expect = round2(freight + delivery + surcharge - transit - remit);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应结金额复算不符', line: it.line,
    amount: round2(Math.abs(stated - expect)),
    message: `${who(it)}的应结金额是 ${stated.toFixed(2)}，按 运费 ${freight.toFixed(2)} + 派费 ${delivery.toFixed(2)} `
      + `+ 附加费 ${surcharge.toFixed(2)} − 中转费 ${transit.toFixed(2)} − 代收货款应缴 ${remit.toFixed(2)} `
      + `= ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '这一格是网点本期真正要向总部上缴（负数）或总部要拨付（正数）的钱。'
      + '最要紧的是代收货款应缴有没有足额扣减：漏扣就是网点少缴、多扣就是网点吃亏。先把这一行的加减对到凭证上。',
  };
}

function checkWeightUnderstated(it) {
  const charge = num(it, 'chargeWeight');
  const actual = num(it, 'weight');
  if (charge === null || actual === null) return null;
  if (charge >= actual - TOL) return null;
  const diff = round2(actual - charge);
  const price = num(it, 'unitPrice');
  const money = price === null ? 0 : round2(diff * price);
  return {
    level: 'P1', category: '计费重量低于实际重量（少计费）', line: it.line,
    amount: money,
    message: `${who(it)}的计费重量是 ${charge}，小于实际重量 ${actual}，少计 ${diff}`
      + `${price === null ? '' : `（按单价 ${price} 折算少收运费 ${money.toFixed(2)}）`}。`
      + '计费重量是"实际重量与体积重取大、再按进位规则进位"的结果，正常只可能 ≥ 实际重量。',
    advice: '先把这张单的称重记录与抛比规则调出来：多半是抄了实重、漏了体积重，或者续重进位没做。'
      + '少计费不只是少收这一单的钱，还会让网点的重量口径与总部不一致，月底越对越乱。',
  };
}

function checkDuplicateWaybill(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const period = cell(it.period);
    const site = cell(it.siteCode);
    const waybill = cell(it.waybill);
    if (!period || !site || !waybill) continue;
    const key = `${period}|${site}|${waybill}`;
    if (seen.has(key)) {
      const freight = num(it, 'freight');
      const remit = num(it, 'codRemit');
      out.push({
        level: 'P1', category: '同一网点同一期间同一运单号重复行', line: it.line,
        amount: round2(Math.abs(freight === null ? 0 : freight) + Math.abs(remit === null ? 0 : remit)),
        message: `网点「${site}」${period} 的运单 ${waybill} 在第 ${seen.get(key)} 行已经结算过一次，`
          + `第 ${it.line} 行又出现一次 —— 同一票货的运费与代收货款应缴都被算了两遍。`,
        advice: '先看是不是重复粘贴 / 重复导单（对账单里最常见）。确属同一票货分两段计费的，'
          + '请拆成两行并各写清说明与不同运单号，不要共用同一个运单号。',
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
            + '非代收货款运单请把代收货款 / 费率 / 手续费 / 应缴都填 0，留空表示"不知道"，两者不能混。',
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
        advice: '要么明细行漏了运单，要么合计行改过明细却没重算（最常见）。'
          + '合计行是对外金额（总部据此划款），先把它与明细对齐。',
      });
    }
  }
  return out;
}

function checkCodRemitGap(it) {
  const amount = num(it, 'codAmount');
  const fee = num(it, 'codFee');
  const remit = num(it, 'codRemit');
  if (amount === null || fee === null || remit === null) return [];
  if (amount <= TOL) return [];
  const out = [];
  const net = round2(amount - fee);
  const gap = round2(net - remit);
  if (gap > TOL) {
    out.push({
      level: 'P0', category: '代收货款未足额上缴（应追缴）', line: it.line,
      amount: gap,
      message: `${who(it)}代收货款 ${amount.toFixed(2)}、手续费 ${fee.toFixed(2)}，净额应为 ${net.toFixed(2)}，`
        + `但「代收货款应缴」只有 ${remit.toFixed(2)}，少缴 ${gap.toFixed(2)} —— 这笔钱网点已经收到手，`
        + '少缴部分属于应当追缴的代收货款。',
      advice: '先拿代收货款台账 + 银行到账流水把这张单核一遍：是这一行漏扣了，还是整笔代收货款还没上缴。'
        + '没上缴的要限期划回；确实是分次上缴的，请在备注里写清已缴金额与日期，别让净额凭空少一块。',
    });
  } else if (gap < -TOL) {
    out.push({
      level: 'P1', category: '代收货款应缴大于代收净额', line: it.line,
      amount: round2(-gap),
      message: `${who(it)}代收货款 ${amount.toFixed(2)} 扣手续费 ${fee.toFixed(2)} 后净额是 ${net.toFixed(2)}，`
        + `但「代收货款应缴」写的是 ${remit.toFixed(2)}，多出 ${round2(-gap).toFixed(2)} —— `
        + '要缴的钱比收到的钱还多，网点会平白吃亏。',
      advice: '多半是代收货款金额抄少了、或者手续费率用高了。把这一行的代收货款与手续费率对回原始运单，'
        + '再让应缴跟着重算；确实有总部代垫 / 补收的，请在备注里写清依据。',
    });
  }
  return out;
}

function checkDuplicateCodNo(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const site = cell(it.siteCode);
    const period = cell(it.period);
    const no = cell(it.codNo);
    if (!site || !period || !no || isBlank(no)) continue;
    const key = `${site}|${period}|${no}`;
    if (seen.has(key)) {
      const amount = num(it, 'codAmount');
      out.push({
        level: 'P0', category: '同一网点同一代收货款单号重复计扣', line: it.line,
        amount: amount === null ? 0 : round2(Math.abs(amount)),
        message: `网点「${site}」${period} 的代收货款单号 ${no} 在第 ${seen.get(key)} 行已经计过一次，`
          + `第 ${it.line} 行又计了一次 —— 同一笔代收货款被要求上缴两遍。`,
        advice: '同一张代收货款单只能上缴一次：拿代收货款台账核一遍，把重复的那笔冲回；'
          + '如果确实是两个单号填成了同一个，请按代收单原样改对。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

function checkCodRateInconsistent(items) {
  const groups = new Map();
  for (const it of items) {
    const key = siteKeyOf(it);
    const amount = num(it, 'codAmount');
    const rate = num(it, 'codRate');
    if (amount === null || rate === null || amount <= TOL) continue;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push({ line: it.line, rate, amount });
  }
  const out = [];
  for (const rows of groups.values()) {
    const rates = [];
    for (const r of rows) if (rates.indexOf(r.rate) < 0) rates.push(r.rate);
    if (rates.length <= 1) continue;
    const base = Math.min.apply(null, rates);
    let over = 0;
    for (const r of rows) if (r.rate > base + 1e-9) over += r.amount * (r.rate - base);
    over = round2(over);
    const last = rows[rows.length - 1];
    out.push({
      level: 'P1', category: '代收手续费率不一致', line: last.line,
      amount: over,
      message: `本期这一组（${rows.length} 行代收货款，第 ${rows.map((r) => r.line).join('、')} 行）`
        + `出现了 ${rates.length} 个代收手续费率：${rates.map((r) => round2(r * 100) + '%').join(' / ')}。`
        + `按其中最低费率 ${round2(base * 100)}% 折算，多计代收手续费 ${over.toFixed(2)}。`,
      advice: '同一网点同一期间的手续费率通常只有一档（分客户 / 分金额档的要按档分批列示）。'
        + '先把这几行对回代收协议：是费率调价后新旧混用，还是有一行费率抄错了。',
    });
  }
  return out;
}

/** 订阅版专有能力：跨网点汇总台账 + 按金额排序的差异处理清单（本包结构上没有这一层）。 */
function buildSiteLedger(items, findings) {
  const byKey = new Map();
  const byLine = new Map();
  const byItem = new Map();
  for (const it of items) {
    const key = siteKeyOf(it);
    byLine.set(it.line, key);
    byItem.set(it.line, it);
    if (!byKey.has(key)) {
      byKey.set(key, {
        site_code: cell(it.siteCode) || '(未填网点编码)',
        site_name: cell(it.siteName),
        period: cell(it.period) || '(未填期间)',
        rows: 0,
        freight_total: 0, delivery_fee_total: 0, transit_fee_total: 0, surcharge_total: 0,
        cod_amount_total: 0, cod_fee_total: 0, cod_remit_total: 0, payable_total: 0,
        disputed_total: 0, disputes: [],
      });
    }
    const g = byKey.get(key);
    g.rows += 1;
    const add = (field, role) => {
      const v = num(it, role);
      if (v !== null) g[field] = round2(g[field] + v);
    };
    add('freight_total', 'freight');
    add('delivery_fee_total', 'deliveryFee');
    add('transit_fee_total', 'transitFee');
    add('surcharge_total', 'surcharge');
    add('cod_amount_total', 'codAmount');
    add('cod_fee_total', 'codFee');
    add('cod_remit_total', 'codRemit');
    add('payable_total', 'payable');
  }
  for (const f of findings) {
    const key = byLine.get(f.line);
    if (!key || !byKey.has(key)) continue;
    const g = byKey.get(key);
    const amt = typeof f.amount === 'number' && Number.isFinite(f.amount) ? round2(f.amount) : 0;
    g.disputed_total = round2(g.disputed_total + amt);
    g.disputes.push({ line: f.line, category: f.category, amount: amt });
  }
  const list = [...byKey.values()].sort((a, b) => (a.payable_total - b.payable_total)
    || String(a.site_code).localeCompare(String(b.site_code))
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
      site_code: it ? (cell(it.siteCode) || '(未填网点编码)') : '(合计行)',
      waybill: it ? (cell(it.waybill) || '(未填运单号)') : '(合计行)',
      category: f.category,
      level: f.level,
      amount: round2(f.amount),
      advice: f.advice || '',
    };
  });

  return {
    by_site: list,
    sites: list.length,
    periods: new Set(items.map((it) => cell(it.period))).size,
    rows: items.length,
    disputed_total: disputed,
    action_queue: actionQueue,
    sort_rule: '台账按「应结金额」升序（越负 = 本期要向总部上缴的净额越大；正数 = 总部应拨付给网点），'
      + '金额相同按网点编码、再按期间；差异处理清单按涉及金额从大到小，金额相同按原文行号。',
    note: actionQueue.length
      ? '这是结算前的处理清单：先按金额从大到小把差异谈清楚 / 改对（争议金额、上缴缺口、重复计扣优先），'
        + '再按对账后的金额划款。'
      : '没有算出带金额的差异 —— 不是"没问题"，是本材料在上述检查项范围内没发现差额；'
        + '范围之外的判断（费率是否符合协议、货款是否真的收到）本工具不做。',
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
    return insufficient('没有收到网点运费结算单与代收货款明细表的正文（text）—— 请把'
      + '「结算期间 / 网点编码 / 运单号 / 计费重量 / 实际重量 / 计费单价 / 运费 / 派费 / 中转费 / 附加费 / '
      + '代收货款 / 代收手续费率 / 代收手续费 / 代收货款应缴 / 应结金额」这张表（含表头）整段贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `表头缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或每行都是合计行），没有任何网点结算明细行');
  }

  const periods = new Set();
  const sites = new Set();
  for (const it of t.items) {
    periods.add(cell(it.period));
    sites.add(cell(it.siteCode));
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkFreightRecompute(it);
    if (a) findings.push(a);
    const b = checkCodFeeRecompute(it);
    if (b) findings.push(b);
    const c = checkCodRemitRecompute(it);
    if (c) findings.push(c);
    const d = checkPayableRecompute(it);
    if (d) findings.push(d);
    const e = checkWeightUnderstated(it);
    if (e) findings.push(e);
    if (paid) {
      const g = checkCodRemitGap(it);
      if (g.length) findings.push.apply(findings, g);
    }
  }
  findings.push.apply(findings, checkBlanks(t.items));
  findings.push.apply(findings, checkDuplicateWaybill(t.items));
  if (paid) findings.push.apply(findings, checkDuplicateCodNo(t.items));
  if (paid) findings.push.apply(findings, checkCodRateInconsistent(t.items));
  if (paid) findings.push.apply(findings, checkTotalRow(t.totals, t.items));

  const notRun = [];
  if (!paid) notRun.push.apply(notRun, CHECKS_WITHHELD);
  const checksExecuted = CHECKS_GIVEN.slice();
  if (paid) checksExecuted.push.apply(checksExecuted, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let chargeTotal = 0;
  let freightTotal = 0;
  let codTotal = 0;
  let remitTotal = 0;
  let payableTotal = 0;
  for (const it of t.items) {
    const a = num(it, 'chargeWeight');
    if (a !== null) chargeTotal += a;
    const b = num(it, 'freight');
    if (b !== null) freightTotal += b;
    const c = num(it, 'codAmount');
    if (c !== null) codTotal += c;
    const d = num(it, 'codRemit');
    if (d !== null) remitTotal += d;
    const e = num(it, 'payable');
    if (e !== null) payableTotal += e;
  }

  let tierNote = `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`;
  if (paid) {
    tierNote = '完整档执行全部检查项（含合计勾稽、代收货款上缴缺口与费率一致性判定、'
      + '跨网点汇总台账与按金额排序的差异处理清单）。';
  }

  const result = {
    status: 'success',
    service_type: 'COURIER_SETTLEMENT_CHECK',
    scope: {
      checks: checksExecuted,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.size,
      sites: sites.size,
      totals_row: Boolean(t.totals.row),
      totals_rows: t.totals.rows || 0,
      charge_weight_total: round2(chargeTotal),
      freight_total: round2(freightTotal),
      cod_amount_total: round2(codTotal),
      cod_remit_total: round2(remitTotal),
      payable_total: round2(payableTotal),
      statement_payable_total: t.totals.row ? num(t.totals.row, 'payable') : null,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periods.size,
      sites: sites.size,
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
    disclaimer: '只核「计费重量 × 计费单价 = 运费」「代收货款 − 代收手续费 = 代收货款应缴」'
      + '「运费 + 派费 + 附加费 − 中转费 − 代收货款应缴 = 应结金额」这类**表内勾稽**，'
      + '不判断单价该按什么合同档位、抛比怎么取、代收手续费率是否符合代收协议、代收货款是否真的收到并转付'
      + '（以运价合同、代收协议与银行流水为准）；每条结论都带原文行号与运单号，可由第三方用同一份输入复算。',
  };

  if (paid) {
    const ledger = buildSiteLedger(t.items, findings);
    result.site_ledger = ledger;
    result.action_queue = ledger.action_queue;
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT,
  LABELS, REQUIRED, SUM_ROLES,
};
