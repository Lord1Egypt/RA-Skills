/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * driver-freight-settlement-check.js —— 承运司机运费结算核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**物流公司 / 货主车队每月给承运商与个体司机结算运费时**。
 * 结算单上每一格都能手算复现，而每月都吵的就是这几处：
 *   · 单价按错档（按里程 vs 按吨公里），一列数字整体差一截；
 *   · 回单（签收单）没回来却已经按全额放了款，出了货损 / 货差追不回来；
 *   · 油卡抵扣被同一张充值单扣了两遍；
 *   · 罚款、押金 / 质保金扣了款，扣款依据栏却是空的，司机不认这笔钱；
 *   · 代垫过路费该加进应付里，却被漏在一张单上。
 *
 * 表内勾稽（每一步都能被第三方用同一份输入复算）：
 *   运费     = 结算数量 × 结算单价
 *   应付运费 = 运费 − 回单扣款 − 油卡抵扣 − 罚款抵扣 − 押金扣留 + 代垫过路费
 *   对账单合计 = 各明细行应付运费之和（合计行各列 = 明细行逐列相加）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 7 项；完整档追加 5 项（见 CHECKS_WITHHELD），其中最后一项是免费档**结构上做不到**的：
 * 「按司机的结算前处理清单」（本月应付与争议金额排序 + 待补回单 / 待追回扣款）。
 *
 * ⚠️ 本工具**不判断**结算单价该按什么合同档位、里程与吨公里数据是否真实、扣款依据的文本内容是否
 *    合法有效（那属于运价合同与业务凭证的核定）：表里的结算数量、结算单价、回单状态、扣款依据
 *    一律**以你填的为准**，本工具只核表内勾稽，并把可疑处按原文行号与运单号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的档位开关算成一个布尔常量，再把付费检查包进以该常量为条件的
 *    语句块（**不要**留「完整档才执行的检查」那类 MARKER —— 两个形态同时存在时
 *    `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关 / 条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量。
 */

const CHECKS_GIVEN = [
  '运费复算（结算数量 × 结算单价 = 运费）',
  '逐单应付运费复算（运费 − 回单扣款 − 油卡抵扣 − 罚款抵扣 − 押金扣留 + 代垫过路费 = 应付运费）',
  '对账单合计勾稽（合计行应付运费 = 各明细行应付运费之和，不符时报出差异金额并定位差异单）',
  '合计行逐列复核（结算数量 / 运费 / 各项抵扣 / 代垫过路费）',
  '同一司机同一期间同一运单号重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '回单缺失判定（回单状态为未回 / 未签收 / 待回的单：结算前必须补齐回单，补不齐的按合同扣款或暂缓支付）',
  '无依据扣款判定（油卡抵扣 / 罚款抵扣 / 押金扣留 / 回单扣款金额大于 0，但扣款依据栏为空或占位符 ⇒ 计入应追回的争议金额）',
  '油卡抵扣重复计扣判定（同一司机的同一油卡充值单号被多次抵扣）',
  '单价档判定（同一司机同一结算方式在同一结算期内出现多个结算单价）',
  '按司机的结算前处理清单（本月应付与争议金额排序，逐条带原文行号与运单号，列出待补回单与待追回扣款）',
];

const OUT_OF_SCOPE = [
  '判断结算单价该按什么合同档位、里程或吨公里数据是否真实（本工具只核表内算术，以你填的结算数量与单价为准）',
  '判断油卡充值、罚款、押金扣留是否真的发生过、金额与油卡系统 / 罚单是否一致（要拿原始凭证核，本工具不去查外部系统）',
  '判断扣款依据的文本内容是否合法有效（本工具只看依据栏是否为空、是否为占位符）',
  '计算个税 / 社保 / 发票税额，或处理平台司机、劳务外包等非承运结算口径',
  '读取 Excel / TMS / 油卡系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '结算期间\t司机\t车牌号\t运单号\t结算方式\t结算数量\t结算单价\t运费\t回单扣款\t油卡抵扣\t罚款抵扣\t押金扣留\t代垫过路费\t应付运费\t回单状态\t扣款依据\t油卡充值单号',
  '2026-01\t张伟\t沪A12345\tYD202601001\t按里程\t1200\t3.50\t4200.00\t0.00\t500.00\t0.00\t0.00\t300.00\t4000.00\t已回\t油卡抵扣500元含司机签字的充值单\tYK20260101',
  '2026-01\t张伟\t沪A12345\tYD202601002\t按里程\t800\t3.50\t2800.00\t0.00\t0.00\t0.00\t0.00\t120.00\t2920.00\t已回\t代垫过路费凭票报销\t',
  '2026-01\t李强\t苏B88888\tYD202601003\t按吨公里\t320\t45.00\t14400.00\t0.00\t2000.00\t0.00\t0.00\t0.00\t12400.00\t已回\t油卡抵扣2000元有充值单\tYK20260103',
  '2026-02\t张伟\t沪A12345\tYD202602001\t按里程\t1000\t3.50\t3500.00\t0.00\t300.00\t0.00\t0.00\t0.00\t3200.00\t已回\t油卡抵扣300元有充值单\tYK20260201',
  '2026-02\t李强\t苏B88888\tYD202602002\t按吨公里\t280\t45.00\t12600.00\t0.00\t0.00\t200.00\t0.00\t0.00\t12400.00\t已回\t罚款200元有罚单编号\t',
  '2026-02\t王磊\t皖C66666\tYD202602003\t按里程\t600\t4.20\t2520.00\t0.00\t0.00\t0.00\t500.00\t0.00\t2020.00\t已回\t押金扣留500元按挂靠协议\t',
  '合计\t\t\t\t\t4200\t\t40020.00\t0.00\t2800.00\t200.00\t500.00\t420.00\t36940.00\t\t\t',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前，兜底的宽泛别名在后。
  //    「应付运费」必须排在「运费」前面（否则被 freight 抢走，应付运费永远复算不了）；
  //    「油卡充值单号」必须排在「油卡抵扣」前面（否则被 fuelDeduct 的「油卡」抢走）；
  //    「回单扣款」必须排在「回单状态」前面（否则被 receiptStatus 的「回单」抢走）；
  //    「扣款依据」里**不放**裸的「扣」，免得把各项扣款列抢走。
  period: ['结算期间', '所属期间', '费用期间', '账期', '所属月份', '期间', '月份', '月度'],
  driver: ['司机姓名', '承运司机', '驾驶员姓名', '司机', '驾驶员', '车主'],
  plate: ['车牌号码', '车牌号', '车牌', '车号', '车辆'],
  waybill: ['运单编号', '运单号', '车次号', '派车单号', '托运单号'],
  rateMode: ['结算方式', '计价方式', '计费方式', '结算口径', '计价单位'],
  qty: ['结算数量', '结算里程', '结算吨公里', '里程数', '公里数', '吨公里数', '吨位数', '数量'],
  unitPrice: ['结算单价', '吨公里单价', '公里单价', '运价', '单价'],
  payable: ['应付运费', '应付金额', '实付运费', '结算应付', '应付'],
  freight: ['运费金额', '运输费用', '运费'],
  deductBasis: ['扣款依据', '扣款原因', '扣款说明', '依据', '备注'],
  fuelCardNo: ['油卡充值单号', '油卡单号', '加油卡单号', '油卡卡号'],
  receiptDeduct: ['回单扣款金额', '回单扣款', '回单扣减', '缺单扣款'],
  receiptStatus: ['回单状态', '签收单状态', '回单齐全性', '签收状态', '回单'],
  fuelDeduct: ['油卡抵扣', '油卡扣款', '油卡'],
  fineDeduct: ['罚款抵扣', '罚款扣款', '罚款'],
  depositHold: ['押金扣留', '质保金扣留', '押金扣减', '押金', '质保金', '保证金'],
  advanceToll: ['代垫过路费', '代垫路桥费', '代垫过路', '过路费', '路桥费', '代垫费用'],
};

const LABELS = {
  period: '结算期间', driver: '司机', plate: '车牌号', waybill: '运单号', rateMode: '结算方式',
  qty: '结算数量', unitPrice: '结算单价', payable: '应付运费', freight: '运费',
  deductBasis: '扣款依据', fuelCardNo: '油卡充值单号', receiptDeduct: '回单扣款',
  receiptStatus: '回单状态', fuelDeduct: '油卡抵扣', fineDeduct: '罚款抵扣',
  depositHold: '押金扣留', advanceToll: '代垫过路费',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不拿 0 去替你假设"没有这项抵扣"） */
const REQUIRED = ['period', 'driver', 'waybill', 'qty', 'unitPrice', 'freight', 'receiptDeduct',
  'fuelDeduct', 'fineDeduct', 'depositHold', 'advanceToll', 'payable'];
/** 合计行逐列复核的列：**不含结算单价**（单价是"每公里 / 每吨公里多少钱"的比率，加总没有意义）；
 *  也不含**应付运费** —— 它由对账单合计勾稽单独核（要报出与对账单的差异金额并定位差异单）。 */
const SUM_ROLES = ['qty', 'freight', 'receiptDeduct', 'fuelDeduct', 'fineDeduct', 'depositHold', 'advanceToll'];
/** 各项抵扣（负数方向）：应付运费 = 运费 − 这四项之和 + 代垫过路费 */
const DEDUCTION_ROLES = [['receiptDeduct', '回单扣款'], ['fuelDeduct', '油卡抵扣'],
  ['fineDeduct', '罚款抵扣'], ['depositHold', '押金扣留']];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：|总计：)$/;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值（缺一列抵扣就报缺列，不会替你按 0 算）。',
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

function normNumber(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
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
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i] };
    cols.forEach((c, idx) => {
      if (!c.role) return;
      if (row[c.role] === undefined) row[c.role] = cells[idx] === undefined ? '' : cells[idx];
    });
    if (TOTAL_WORDS.test(cell(cells[0]))) {
      // 一份材料里拼了多期 / 多个车队时会出现多行「合计 / 小计」：只把**最后一行**当对账单总额
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
  return `司机「${cell(it.driver) || '(未填司机)'}」运单 ${cell(it.waybill) || '(未填运单号)'}`;
}

/* ============================ 免费档执行的检查项 ============================ */

function checkFreightRecompute(it) {
  const qty = num(it, 'qty');
  const price = num(it, 'unitPrice');
  const stated = num(it, 'freight');
  if (qty === null || price === null || stated === null) return null;
  const expect = round2(qty * price);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '运费复算不符', line: it.line,
    message: `${who(it)}的运费是 ${stated.toFixed(2)}，按 结算数量 ${qty} × 结算单价 ${price} = ${expect.toFixed(2)}，`
      + `应为 ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '运费是后面所有抵扣的地基。先确认这张单的结算方式（按里程 / 按吨公里）与单价档有没有用错，再改运费 —— 单价按错档就是整体差一截。',
  };
}

function checkPayableRecompute(it) {
  const freight = num(it, 'freight');
  const advance = num(it, 'advanceToll');
  const stated = num(it, 'payable');
  if (freight === null || advance === null || stated === null) return null;
  let expect = freight + advance;
  const parts = [];
  for (const [role, label2] of DEDUCTION_ROLES) {
    const v = num(it, role);
    if (v === null) return null;
    expect -= v;
    parts.push(`${label2} ${v.toFixed(2)}`);
  }
  expect = round2(expect);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '逐单应付运费复算不符', line: it.line,
    message: `${who(it)}的应付运费是 ${stated.toFixed(2)}，按 运费 ${freight.toFixed(2)} − ${parts.join(' − ')} `
      + `+ 代垫过路费 ${advance.toFixed(2)} = ${expect.toFixed(2)}，应为 ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '这一行就是司机拿到手的钱。常见的错法：漏加代垫过路费、押金扣了一次又在下一行再扣、回单扣款只扣了不写依据 —— 先把这张单的每一笔加减对到凭证上。',
  };
}

function checkNegative(it) {
  const out = [];
  const roles = [['freight', '运费'], ['payable', '应付运费'], ['receiptDeduct', '回单扣款'],
    ['fuelDeduct', '油卡抵扣'], ['fineDeduct', '罚款抵扣'], ['depositHold', '押金扣留'],
    ['advanceToll', '代垫过路费']];
  for (const [role, label2] of roles) {
    const v = num(it, role);
    if (v !== null && v < -TOL) {
      out.push({
        level: 'P0', category: '金额为负', line: it.line,
        message: `${who(it)}的「${label2}」是 ${v.toFixed(2)}（负数）。`,
        advice: '这几列按口径都是"正数金额"：抵扣填正数、运费与代垫填正数。负号多半是粘贴时符号掉了或公式取反了；负数会顺着算式把应付运费整体算错。',
      });
    }
  }
  return out;
}

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a|-+)$/i;

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      const s = cell(it[role]);
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这张单的应付运费就算不出来。本工具不会用 0 或默认值替你填：抵扣列填 0 表示"确实没有这项"，留空表示"不知道" —— 这两者不能混。',
        });
      }
    }
  }
  return out;
}

function checkDuplicateWaybill(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const period = cell(it.period);
    const driver = cell(it.driver);
    const waybill = cell(it.waybill);
    if (!period || !driver || !waybill) continue;
    const key = `${period}|${driver}|${waybill}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一司机同一期间同一运单号重复行', line: it.line,
        message: `司机「${driver}」${period} 的运单 ${waybill} 在第 ${seen.get(key)} 行已经结算过一次，第 ${it.line} 行又出现一次 —— 同一趟活被算了两遍运费。`,
        advice: '先看是不是重复粘贴（对账单里最常见）。确属同一运单分两段计费的，请把两段的里程 / 吨公里拆成两行并各写清说明，不要共用同一个运单号。',
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
        level: 'P0', category: '合计行与明细之和不符', line: total.line,
        message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
        advice: '要么明细行漏了运单，要么合计行没跟着更新（改过单行却没重算合计）。对账单上的合计数是对外金额，先把它与明细对齐。',
      });
    }
  }
  return out;
}

function checkStatementTotal(totals, items) {
  const total = totals.row;
  if (!total) return null;
  const stated = num(total, 'payable');
  if (stated === null) return null;
  let sum = 0;
  const diffRows = [];
  for (const it of items) {
    const p = num(it, 'payable');
    if (p === null) continue;
    sum += p;
    const freight = num(it, 'freight');
    const advance = num(it, 'advanceToll');
    if (freight === null || advance === null) continue;
    let expect = freight + advance;
    let ok = true;
    for (const [role] of DEDUCTION_ROLES) {
      const v = num(it, role);
      if (v === null) { ok = false; break; }
      expect -= v;
    }
    if (!ok) continue;
    expect = round2(expect);
    if (Math.abs(expect - p) > TOL) {
      diffRows.push({ line: it.line, waybill: cell(it.waybill) || '(未填运单号)', diff: round2(p - expect) });
    }
  }
  sum = round2(sum);
  if (Math.abs(sum - stated) <= TOL) return null;
  const shown = diffRows.slice(0, 3)
    .map((d) => `第 ${d.line} 行（运单 ${d.waybill}，单行差 ${d.diff.toFixed(2)}）`).join('、');
  return {
    level: 'P0', category: '对账单合计与明细应付之和不符', line: total.line,
    message: `对账单（合计行）的应付运费是 ${stated.toFixed(2)}，各明细行应付运费相加是 ${sum.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)}。`
      + (diffRows.length
        ? `明细行里对不上的是 ${diffRows.length} 单：${shown}${diffRows.length > 3 ? ' 等' : ''}。`
        : '明细行本身每一单都能复算通过 —— 差异出在合计行或漏了整张单。'),
    advice: diffRows.length
      ? '先把上面这些差异单逐张改对，再让对账单合计跟着刷新；差异单改完合计还差，就是明细行漏了运单（或把别人的单并进来了）。'
      : '逐单都对、合计对不上：要么合计行没重算，要么有整张运单没录进明细。把对账单金额拆到每一张单上再核一次。',
  };
}

/* ============================== 主入口 ============================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到承运司机运费结算单正文（text）—— 请把「结算期间 / 司机 / 运单号 / 结算方式 / 结算数量 / 结算单价 / 运费 / 回单扣款 / 油卡抵扣 / 罚款抵扣 / 押金扣留 / 代垫过路费 / 应付运费」这张表（含表头）贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `运费结算单缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何运单明细行');
  }

  const periods = new Set();
  for (const it of t.items) periods.add(cell(it.period));

  const findings = [];
  for (const it of t.items) {
    const a = checkFreightRecompute(it);
    if (a) findings.push(a);
    const b = checkPayableRecompute(it);
    if (b) findings.push(b);
    findings.push(...checkNegative(it));

  }
  findings.push(...checkBlanks(t.items));
  findings.push(...checkDuplicateWaybill(t.items));
  findings.push(...checkTotalRow(t.totals, t.items));
  const statement = checkStatementTotal(t.totals, t.items);
  if (statement) findings.push(statement);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let qtyTotal = 0;
  let freightTotal = 0;
  let payableTotal = 0;
  for (const it of t.items) {
    const q = num(it, 'qty');
    if (q !== null) qtyTotal += q;
    const f = num(it, 'freight');
    if (f !== null) freightTotal += f;
    const p = num(it, 'payable');
    if (p !== null) payableTotal += p;
  }

  const result = {
    status: 'success',
    service_type: 'DRIVER_FREIGHT_SETTLEMENT_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.size,
      totals_row: Boolean(t.totals.row),
      totals_rows: t.totals.rows || 0,
      qty_total: round2(qtyTotal),
      freight_total: round2(freightTotal),
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
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"结算数量 × 结算单价 = 运费"与"运费 − 各项抵扣 + 代垫过路费 = 应付运费"这类**表内勾稽**，'
      + '不判断单价该按什么合同档位、里程与吨公里是否真实、扣款依据的文本是否有效（以运价合同与业务凭证为准）；'
      + '每条结论都带原文行号与运单号，可由第三方用同一份输入复算。',
  };



  return { status: 'success', result };
}

/* ========================= 以下为完整档（付费）才执行的检查 ========================= */

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, REQUIRED, SUM_ROLES, DEDUCTION_ROLES,
};
