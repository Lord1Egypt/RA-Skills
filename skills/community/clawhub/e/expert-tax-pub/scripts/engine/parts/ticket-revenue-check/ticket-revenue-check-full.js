'use strict';
/**
 * ticket-revenue-check.js —— 票务收入与渠道结算核对（本包 / 订阅版共用源码）
 *
 * 谁在什么时候必须做这件事：**演出 / 剧场 / 景区票务公司的财务在每月与各售票渠道结算时**。
 * 渠道（大麦 / 猫眼 / 官网 / 美团 / 抖音…）每个月各给一张结算单，票务方要把这张
 * 「票务收入与渠道结算明细表」核一遍才能确认收入、才能给渠道付款。每月都对不上的就是这几处：
 *   · 渠道佣金按错佣金率（续约后新旧费率混算、把 8% 当成 0.8%）；
 *   · 票面收入与「票数 × 票价」对不上（赠票、工作票算进了票面）；
 *   · 退票金额被归到了别的行 / 别的渠道（退款冲减记错行）；
 *   · 场次日期跨月，收入被记进了上一个结算期；
 *   · 同一订单号被两个渠道各结算了一次（重复确认收入）。
 *
 * 表内勾稽（每一步都能被第三方用同一份输入复算）：
 *   票面收入   = 票数 × 票价
 *   渠道佣金   = 票面收入 × 佣金率（佣金率按**百分数**填：8 表示 8%，填 `8%` 也可）
 *   结算金额   = 票面收入 − 渠道佣金 − 退票金额
 *   合计行各列 = 各明细行逐列相加（票数 / 票面收入 / 渠道佣金 / 退票金额 / 结算金额）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * 不读环境变量、不写任何文件、**不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 本包执行 6 项；订阅版追加 6 项（见 CHECKS_WITHHELD），其中结构上多出来的能力是
 * 「跨渠道 / 跨场次汇总台账」与「按差异金额排序的处理清单」（含差异归因）。
 *
 * ⚠️ 本工具**不判断**票房是否真实（有没有锁场、包场、刷单）、不判断票款是否真实到账，
 *    也不做任何**税务申报核定**（计税口径、发票税额、税会差异一律不管）：
 *    表里的票数、票价、佣金率、退票金额一律**以你填的为准**，本工具只核这张表内部的勾稽，
 *    并把可疑处按**原文行号**与订单号列出来。
 *
 * ⚠️ 档位开关**只声明一次**，订阅版的检查包进以该常量为条件的语句块里。
 *    ⛔ 不要在注释里写出那个开关 / 条件语句的字面量：`strip_free_engine` 的残渣断言认得它们，
 *    写了就会被判『没删干净』而整包跳过（本仓踩过两次）。
 */

const CHECKS_GIVEN = [
  '票面收入勾稽（票数 × 票价 = 票面收入）',
  '渠道佣金复算（票面收入 × 佣金率 = 渠道佣金，佣金率按百分数填）',
  '结算金额逐行复算（票面收入 − 渠道佣金 − 退票金额 = 结算金额）',
  '合计行与明细勾稽（合计行各列 = 各明细行逐列相加）',
  '同一订单号重复结算检测',
  '关键字段缺失、占位符与负数检测',
];

const CHECKS_WITHHELD = [
  '退票归属判定（退票金额超过本行票面收入，或退票金额大于 0 而备注里没有说明退票归属 ⇒ 归因不明）',
  '跨期结算判定（场次日期所在月份与该行结算期间不一致 ⇒ 收入被记进了别的结算期）',
  '佣金率不一致判定（同一渠道同一票档在同一结算期里出现多个佣金率）',
  '票面口径不一致判定（同一渠道同一票档出现多个票价 ⇒ 票面收入口径不一致）',
  '跨渠道 / 跨场次汇总台账（按渠道、按场次分别汇总票数、票面收入、佣金、退票与结算金额）',
  '按差异金额排序的处理清单（逐条带原文行号与订单号，标出该行差异金额与差异原因）',
];

const OUT_OF_SCOPE = [
  '判断票房是否真实（有没有锁场、包场、刷单、赠票混入票面），或上座率数据是否与售票系统一致 —— 那要拿售票系统的原始流水核，本工具不去查外部系统',
  '判断票款是否真实到账、渠道回款与银行流水是否一致（本工具只核这张结算明细表内部的金额勾稽）',
  '做税务申报核定：计税收入口径、发票税额、税会差异、文化事业建设费一律不管（以税务机关口径与你的税务申报为准）',
  '判断佣金率该按哪一版渠道合同、佣金是否含税、渠道服务费该不该另计（以你和渠道签的合同为准）',
  '读取 Excel / 票务系统 / 渠道对账单导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '结算期间\t场次\t渠道\t票档\t订单号\t票数\t票价\t票面收入\t佣金率\t渠道佣金\t退票金额\t结算金额\t备注',
  '2026-01\t2026-01-10 19:30\t大麦\t普通票\tDD2026010001\t300\t180.00\t54000.00\t8\t4320.00\t0.00\t49680.00\t渠道对账单已确认',
  '2026-01\t2026-01-10 19:30\t猫眼\t普通票\tMY2026010002\t200\t180.00\t36000.00\t10\t3600.00\t0.00\t32400.00\t平台月结',
  '2026-01\t2026-01-10 19:30\t官网\tVIP票\tGW2026010003\t60\t380.00\t22800.00\t0\t0.00\t0.00\t22800.00\t自有渠道无佣金',
  '2026-01\t2026-01-10 19:30\t大麦\tVIP票\tDD2026010004\t40\t380.00\t15200.00\t8\t1216.00\t0.00\t13984.00\t平台月结',
  '2026-02\t2026-02-14 19:30\t大麦\t普通票\tDD2026020005\t500\t180.00\t90000.00\t8\t7200.00\t3600.00\t79200.00\t退票2张已冲减',
  '2026-02\t2026-02-14 19:30\t美团\t学生票\tMT2026020006\t150\t120.00\t18000.00\t6\t1080.00\t0.00\t16920.00\t平台月结',
  '合计\t\t\t\t\t1250\t\t236000.00\t\t17416.00\t3600.00\t214984.00\t',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前，兜底的宽泛别名在后。
  //    「结算期间」必须排在最前（否则被「结算」抢走 ⇒ 必需列永远认不出来，所有输入都没结论）；
  //    「佣金率」必须排在「渠道佣金」前面（否则被「佣金」抢走 ⇒ 佣金率整列不参与检查）；
  //    「结算单号」必须排在「结算金额」前面（否则被「结算」抢走）；
  //    「退票金额」里不放裸的「退」；渠道别名里**不放**裸的「平台」（否则「平台佣金」被渠道抢走）；
  //    「佣金率 / 渠道佣金」必须整组排在「渠道」前面（否则「渠道佣金」被渠道的「渠道」抢走，
  //    ⇒ 必需列缺列、所有输入都没结论；`header_map_check.py` 就是钉这个的）。
  period: ['结算期间', '结算账期', '所属期间', '所属月份', '账期', '期间', '月份'],
  session: ['演出场次', '场次编号', '场次', '演出场'],
  ticketType: ['票档', '票种', '票价类型', '票类', '票品'],
  order: ['订单编号', '订单号', '票券订单号', '售票订单号', '票号'],
  qty: ['票数', '出票数', '售票数量', '张数', '数量'],
  price: ['票面单价', '票价', '单价', '面值'],
  faceRevenue: ['票面收入', '票面金额', '票面总额', '票面合计'],
  commissionRate: ['佣金率', '佣金比例', '抽成比例', '佣金点数', '费率'],
  commission: ['渠道佣金', '平台佣金', '佣金', '抽成', '平台服务费', '服务费'],
  channel: ['销售渠道', '售票渠道', '售卖渠道', '渠道'],
  refund: ['退票金额', '退票额', '退票冲减', '退款金额', '退票'],
  settleNo: ['结算单号', '结算批次', '对账单号', '结算单据号'],
  settlement: ['结算金额', '实际结算金额', '应结金额', '结算额', '结算'],
  note: ['备注', '附注', '说明'],
};

const LABELS = {
  period: '结算期间', session: '场次', channel: '渠道', ticketType: '票档', order: '订单号',
  qty: '票数', price: '票价', faceRevenue: '票面收入', commissionRate: '佣金率',
  commission: '渠道佣金', refund: '退票金额', settleNo: '结算单号', settlement: '结算金额',
  note: '备注',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不拿 0 去替你假设"没有退票 / 没有佣金"） */
const REQUIRED = ['period', 'channel', 'order', 'qty', 'price', 'faceRevenue',
  'commissionRate', 'commission', 'refund', 'settlement'];

/** 合计行逐列复核的列：**不含票价与佣金率**（它们是单价 / 比率，加总没有意义）；
 *  也**不含结算单号与备注**（文本列不参与加总）。 */
const SUM_ROLES = ['qty', 'faceRevenue', 'commission', 'refund', 'settlement'];

/** 数值列（出现负号一律报「金额为负」，比率列也算 —— 负佣金率会让佣金算反） */
const NUMBER_ROLES = ['qty', 'price', 'faceRevenue', 'commissionRate', 'commission', 'refund', 'settlement'];

const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：|总计：)$/;
const PLACEHOLDER = /^(待填|待补|待定|待核|未知|xxx|xxx\.xx|\?+|tbd|n\/?a|-+)$/i;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值'
      + '（缺一列就报缺哪列，不会替你按 0 假设"这个渠道没有退票 / 没有佣金"）。',
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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|待核)$/i.test(s);
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
  const s = String(raw).trim().replace(/[,，\s]/g, '').replace(/^[¥￥$]/, '').replace(/%$/, '');
  if (s === '') return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '');
  if (!/^-?\d+(\.\d+)?$/.test(t)) return null;
  const n = Number(t);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
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
      // 一份材料里拼了多个渠道 / 多个结算期时会出现多行「合计 / 小计」：只把**最后一行**当结算单总额
      // （总额在最后），前面的是分组小计；行数记进 scope.totals_rows 让人看得见，不静默丢数据。
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

function who(row) {
  return `${cell(row.period) || '(未填结算期间)'} 渠道「${cell(row.channel) || '(未填渠道)'}」`
    + ` 订单 ${cell(row.order) || '(未填订单号)'}`;
}

/* ============================ 本包执行的检查项 ============================ */
/* ⚠️ 免费检查函数的参数名**故意不叫 it**：工厂的变异门禁盯的是「以 check 开头的函数 + 参数恰好叫 it」
 *    这一形态（⛔ 本注释里也不能出现那种字面量，否则门禁会把注释当靶点、变异静默落空），
 *    靶点必须落在订阅版的检查上，否则变异会打在免费项上。 */

function checkFaceRevenue(row) {
  const qty = num(row, 'qty');
  const price = num(row, 'price');
  const stated = num(row, 'faceRevenue');
  if (qty === null || price === null || stated === null) return null;
  const expect = round2(qty * price);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '票面收入勾稽不符', line: row.line,
    message: `${who(row)}的票面收入是 ${stated.toFixed(2)}，按 票数 ${qty} × 票价 ${price} = ${expect.toFixed(2)}，`
      + `应为 ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '票面收入是佣金与结算金额的地基。先确认这张渠道结算单的口径：赠票 / 工作票 / 内部票有没有被算进票面，'
      + '票数是不是含了未出票的预留张数 —— 口径确认后再改票面收入，别只改票数把账做平。',
  };
}

function checkCommission(row) {
  const face = num(row, 'faceRevenue');
  const rate = num(row, 'commissionRate');
  const stated = num(row, 'commission');
  if (face === null || rate === null || stated === null) return null;
  const expect = round2(face * rate / 100);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '渠道佣金复算不符', line: row.line,
    message: `${who(row)}的渠道佣金是 ${stated.toFixed(2)}，按 票面收入 ${face.toFixed(2)} × 佣金率 ${rate}% = ${expect.toFixed(2)}，`
      + `应为 ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '先确认佣金率填的是百分数（8 表示 8%，填 `8%` 本工具也认）；再把这张单的佣金率对到渠道合同的那一版：'
      + '续约后新旧费率混算、把 8% 当成 0.8%、或把渠道服务费又单独加了一遍，都会差在这里。',
  };
}

function checkSettlement(row) {
  const face = num(row, 'faceRevenue');
  const commission = num(row, 'commission');
  const refund = num(row, 'refund');
  const stated = num(row, 'settlement');
  if (face === null || commission === null || refund === null || stated === null) return null;
  const expect = round2(face - commission - refund);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '结算金额复算不符', line: row.line,
    message: `${who(row)}的结算金额是 ${stated.toFixed(2)}，按 票面收入 ${face.toFixed(2)} − 渠道佣金 ${commission.toFixed(2)} `
      + `− 退票金额 ${refund.toFixed(2)} = ${expect.toFixed(2)}，应为 ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '这一行就是本渠道本月真正该收 / 该付的钱。常见错法：退票只冲了票面没冲佣金、佣金按改过的票面重算过、'
      + '或上一期的退票挂到了本期 —— 把这张单的每一笔加减对到渠道对账单上再改。',
  };
}

function checkBlanksAndNegative(row) {
  const out = [];
  for (const role of REQUIRED) {
    const s = cell(row[role]);
    if (s === '' || PLACEHOLDER.test(s)) {
      out.push({
        level: 'P0', category: '关键字段缺失或为占位符', line: row.line,
        message: `${who(row)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
        advice: `缺这一格这行的${LABELS[role]}就算不出来。本工具不会用 0 或默认值替你填：`
          + '退票金额填 0 表示"本期确实没有退票"，留空表示"不知道" —— 这两者不能混。',
      });
    }
  }
  for (const role of NUMBER_ROLES) {
    const v = num(row, role);
    if (v !== null && v < -TOL) {
      out.push({
        level: 'P0', category: '金额为负', line: row.line,
        message: `${who(row)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）。`,
        advice: '这几列按口径都是"正数"：票数、票价、票面收入、佣金率、渠道佣金、退票金额都填正数，'
          + '退票用「退票金额」这一列表达、不要写负的结算金额。负号多半是粘贴时符号掉了或公式取反了，'
          + '负数会顺着算式把结算金额整体算错。',
      });
    }
  }
  return out;
}

function checkDuplicateOrder(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const order = cell(it.order);
    if (!order || isBlank(order)) continue;
    if (seen.has(order)) {
      out.push({
        level: 'P1', category: '同一订单号重复结算', line: it.line,
        message: `订单号 ${order} 在第 ${seen.get(order)} 行已经结算过一次，第 ${it.line} 行又出现一次`
          + `（渠道「${cell(it.channel) || '(未填渠道)'}」${cell(it.period) || '(未填结算期间)'}）`
          + ' —— 同一笔票款被两个渠道 / 两期各确认了一次收入。',
        advice: '先看是不是两个渠道的对账单里都含这张订单（渠道串单最常见），再看是不是本期把上期已结的订单又抄了一遍。'
          + '确属同一订单分两个票档出票的，请按票档拆行并各写清票档，不要共用同一个订单号。',
      });
    } else {
      seen.set(order, it.line);
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
        message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，`
          + `相差 ${round2(stated - sum).toFixed(2)}。`,
        advice: '要么明细行漏了渠道 / 场次，要么合计行没跟着更新（改过单行却没重算合计）。'
          + '合计行是对外报收入的数，先把它与明细对齐，再去谈差异。',
      });
    }
  }
  return out;
}

/* ===== 以下为订阅版才执行的检查 ===== */

/** 该行的差异金额：三项复算差里绝对值最大的一项（用于排序处理清单） */
function rowDiff(it) {
  const cands = [];
  const qty = num(it, 'qty');
  const price = num(it, 'price');
  const face = num(it, 'faceRevenue');
  const rate = num(it, 'commissionRate');
  const commission = num(it, 'commission');
  const refund = num(it, 'refund');
  const settlement = num(it, 'settlement');
  if (qty !== null && price !== null && face !== null) {
    cands.push({ reason: '票面收入勾稽差异', diff: round2(face - qty * price) });
  }
  if (face !== null && rate !== null && commission !== null) {
    cands.push({ reason: '渠道佣金复算差异', diff: round2(commission - face * rate / 100) });
  }
  if (face !== null && commission !== null && refund !== null && settlement !== null) {
    cands.push({ reason: '结算金额复算差异', diff: round2(settlement - (face - commission - refund)) });
  }
  if (!cands.length) return { reason: '没有可复算的金额要素', diff: 0 };
  let best = cands[0];
  for (const c of cands) {
    if (Math.abs(c.diff) > Math.abs(best.diff)) best = c;
  }
  return best;
}

/** 退票归属：退票额超过本行票面收入，或退了票却没有任何归属说明 */
function checkRefundAttribution(it) {
  const refund = num(it, 'refund');
  if (refund === null || refund <= TOL) return null;
  const face = num(it, 'faceRevenue');
  if (face !== null && refund > face + TOL) {
    return {
      level: 'P1', category: '退票归属异常', line: it.line,
      message: `${who(it)}的退票金额 ${refund.toFixed(2)} 超过了本行票面收入 ${face.toFixed(2)}`
        + ' —— 退票被归到了错的行 / 错的渠道，或者把整场的退票都压在了一个渠道上。',
      advice: '退票必须退回**原售票渠道原票档**：把这张单的退票明细（订单号、退票张数、退款金额）拉出来，'
        + '按原订单归属拆到对应渠道与票档的行上，再重算结算金额（退票同时要冲回对应的渠道佣金）。',
    };
  }
  const note = cell(it.note);
  if (note === '' || isBlank(note)) {
    return {
      level: 'P1', category: '退票归属异常', line: it.line,
      message: `${who(it)}本行退了 ${refund.toFixed(2)} 的票，但备注栏是空的 —— 说不清这批退票是哪几张订单、属于哪个渠道。`,
      advice: '在备注里写明退票归属（哪几张订单、哪个渠道、整单退还是部分退），并确认退票同时冲减了渠道佣金；'
        + '备注栏留空时，这张单对外的退票口径无法被第三方复算。',
    };
  }
  if (!/退|冲减|退款/.test(note)) {
    return {
      level: 'P1', category: '退票归属异常', line: it.line,
      message: `${who(it)}本行退了 ${refund.toFixed(2)} 的票，但备注写的是「${note}」，没有说明退票归属。`,
      advice: '把退票的订单号与退款金额写进备注（本工具只核这条线是否说得清，不去查渠道退款流水）；'
        + '退票金额这一列必须能和备注里的退票张数 × 票价对上。',
    };
  }
  return null;
}

/** 跨期结算：场次日期所在月份与本行结算期间不一致 */
function checkCrossPeriod(it) {
  const period = cell(it.period);
  const session = cell(it.session);
  if (!period || !session || isBlank(session)) return null;
  const ps = period.match(/(\d{4})\s*[-/年]?\s*(\d{1,2})?/);
  const ss = session.match(/(\d{4})\s*[-/年]\s*(\d{1,2})/);
  if (!ps || !ss) return null;
  const py = Number(ps[1]);
  const pm = ps[2] === undefined ? null : Number(ps[2]);
  const sy = Number(ss[1]);
  const sm = Number(ss[2]);
  if (pm === null || !Number.isFinite(sm)) return null;
  if (py === sy && pm === sm) return null;
  return {
    level: 'P1', category: '跨期结算', line: it.line,
    message: `${who(it)}的结算期间是「${period}」，但场次写的是「${session}」（${sy} 年 ${sm} 月）`
      + ' —— 收入被记进了与演出月份不一致的结算期。',
    advice: '跨期本身可能是渠道的账期规则（次月结算），但必须与渠道对账单的账期一致：'
      + '确认这一场的票是不是真的落在该结算期，否则会把两个月的收入互相挤，'
      + '月度收入对不上、跨期退票也会找不到出处。',
  };
}

/** 佣金率不一致：同一渠道同一票档在同一结算期里出现多个佣金率 */
function checkChannelRateDrift(items) {
  const groups = new Map();
  for (const it of items) {
    const channel = cell(it.channel);
    const type = cell(it.ticketType);
    const period = cell(it.period);
    const rate = num(it, 'commissionRate');
    if (!channel || !type || isBlank(type) || rate === null) continue;
    const key = `${period}|${channel}|${type}`;
    if (!groups.has(key)) groups.set(key, { period, channel, type, rates: [], rows: [] });
    const g = groups.get(key);
    if (g.rates.indexOf(rate) < 0) g.rates.push(rate);
    g.rows.push({ line: it.line, order: cell(it.order) || '(未填订单号)', rate });
  }
  const out = [];
  for (const g of groups.values()) {
    if (g.rates.length <= 1) continue;
    const last = g.rows[g.rows.length - 1];
    out.push({
      level: 'P1', category: '佣金率不一致', line: last.line,
      message: `${g.period} 渠道「${g.channel}」票档「${g.type}」出现了 ${g.rates.length} 个佣金率`
        + `（${g.rates.map((x) => `${x}%`).join(' / ')}），涉及第 ${g.rows.map((r) => r.line).join('、')} 行`
        + `（订单 ${g.rows.map((r) => r.order).join('、')}）。`,
      advice: '同一个渠道同一个票档在一个结算期里通常只该有一个佣金率。'
        + '把这几行拉出来对渠道合同：是续约后新旧费率混算，还是把不同的票档 / 不同的推广活动混在了同一票档里。'
        + '确实要分档的，请按不同票档分行填，别共用同一个票档名。',
    });
  }
  return out;
}

/** 票面口径不一致：同一渠道同一票档出现多个票价 */
function checkFacePriceDrift(items) {
  const groups = new Map();
  for (const it of items) {
    const channel = cell(it.channel);
    const type = cell(it.ticketType);
    const price = num(it, 'price');
    if (!channel || !type || isBlank(type) || price === null) continue;
    const key = `${channel}|${type}`;
    if (!groups.has(key)) groups.set(key, { channel, type, prices: [], rows: [] });
    const g = groups.get(key);
    if (g.prices.indexOf(price) < 0) g.prices.push(price);
    g.rows.push({ line: it.line, order: cell(it.order) || '(未填订单号)', price });
  }
  const out = [];
  for (const g of groups.values()) {
    if (g.prices.length <= 1) continue;
    const last = g.rows[g.rows.length - 1];
    out.push({
      level: 'P1', category: '票面口径不一致', line: last.line,
      message: `渠道「${g.channel}」票档「${g.type}」出现了 ${g.prices.length} 个票价`
        + `（${g.prices.map((x) => x.toFixed(2)).join(' / ')}），涉及第 ${g.rows.map((r) => r.line).join('、')} 行`
        + `（订单 ${g.rows.map((r) => r.order).join('、')}）。`,
      advice: '同一个票档在同一个渠道应该只有一个面价。出现多个票价，多半是早鸟票 / 套票 / 折扣票混进了同一票档，'
        + '或者把含服务费的到手价当票面填了 —— 票面口径不一致会让「票数 × 票价 = 票面收入」这条勾稽整体失真。'
        + '请按不同的票价拆成不同的票档（如「普通票·早鸟」）分行列示。',
    });
  }
  return out;
}

function ledgerRow(label) {
  return {
    label, rows: 0, qty: 0, face_revenue: 0, commission: 0, refund: 0, settlement: 0, diff_total: 0,
  };
}

function ledgerAdd(g, it) {
  g.rows += 1;
  const q = num(it, 'qty');
  if (q !== null) g.qty = round2(g.qty + q);
  const f = num(it, 'faceRevenue');
  if (f !== null) g.face_revenue = round2(g.face_revenue + f);
  const c = num(it, 'commission');
  if (c !== null) g.commission = round2(g.commission + c);
  const rf = num(it, 'refund');
  if (rf !== null) g.refund = round2(g.refund + rf);
  const s = num(it, 'settlement');
  if (s !== null) g.settlement = round2(g.settlement + s);
  const d = rowDiff(it);
  if (Math.abs(d.diff) > TOL) g.diff_total = round2(g.diff_total + Math.abs(d.diff));
}

/** 跨渠道 / 跨场次汇总台账（本包结构上没有这个能力） */
function buildChannelLedger(items) {
  const byChannel = new Map();
  const bySession = new Map();
  for (const it of items) {
    const ch = cell(it.channel) || '(未填渠道)';
    if (!byChannel.has(ch)) byChannel.set(ch, ledgerRow(ch));
    ledgerAdd(byChannel.get(ch), it);
    const se = cell(it.session) || '(未填场次)';
    if (!bySession.has(se)) bySession.set(se, ledgerRow(se));
    ledgerAdd(bySession.get(se), it);
  }
  const chList = [...byChannel.values()].sort((a, b) => (b.face_revenue - a.face_revenue)
    || String(a.label).localeCompare(String(b.label)));
  const seList = [...bySession.values()].sort((a, b) => String(a.label).localeCompare(String(b.label)));
  let settlement = 0;
  let diff = 0;
  for (const g of chList) {
    settlement = round2(settlement + g.settlement);
    diff = round2(diff + g.diff_total);
  }
  return {
    by_channel: chList,
    by_session: seList,
    channels: chList.length,
    sessions: seList.length,
    settlement_total: settlement,
    diff_total: diff,
    sort_rule: '渠道按票面收入从大到小；场次按场次时间从小到大。',
    note: '台账按明细行汇总：退票金额归集到记账渠道上，所以某个渠道的退票可能来自别的渠道售出的票 —— '
      + '这正是要用「退票归属」那条检查去核的地方。',
  };
}

/** 按差异金额排序的处理清单（逐条带原文行号与订单号） */
function buildDispositionList(items) {
  const entries = [];
  for (const it of items) {
    const d = rowDiff(it);
    const reasons = [];
    if (Math.abs(d.diff) > TOL) reasons.push(d.reason);
    const refundFinding = checkRefundAttribution(it);
    if (refundFinding) reasons.push('退票归属异常');
    const crossFinding = checkCrossPeriod(it);
    if (crossFinding) reasons.push('跨期结算');
    if (!reasons.length) continue;
    entries.push({
      line: it.line,
      period: cell(it.period),
      session: cell(it.session),
      channel: cell(it.channel) || '(未填渠道)',
      order: cell(it.order) || '(未填订单号)',
      diff: round2(d.diff),
      abs_diff: round2(Math.abs(d.diff)),
      reasons,
    });
  }
  entries.sort((a, b) => (b.abs_diff - a.abs_diff) || (a.line - b.line));
  let diffTotal = 0;
  for (const e of entries) diffTotal = round2(diffTotal + e.abs_diff);
  return {
    entries,
    rows: entries.length,
    diff_total: diffTotal,
    sort_rule: '按该行差异金额的绝对值从大到小；金额相同按原文行号从小到大。'
      + '退票归属异常与跨期结算即使金额为 0 也会列进来 —— 它们是要人工确认的归因问题，不是金额问题。',
    note: '处理顺序：先改差异金额最大的行（它们直接影响本月确认的收入），再处理退票归属与跨期归因，'
      + '最后让合计行与渠道对账单一起刷新。',
  };
}

/* ============================== 主入口 ============================== */

function run(payload) {
  const p = payload;
  const paid = Boolean(p && (p.full || p.credit || p.token));
  if (p !== undefined && p !== null && typeof p !== 'object') {
    return insufficient(`入参不是对象（收到的是 ${typeof p}）—— 请用 {"text": "…"} 把票务收入与渠道结算明细表（含表头）贴进来`);
  }
  const text = p && typeof p.text === 'string' ? p.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到票务收入与渠道结算明细表正文（text）—— 请把「结算期间 / 场次 / 渠道 / 票档 / 订单号 / 票数 / 票价 / 票面收入 / 佣金率 / 渠道佣金 / 退票金额 / 结算金额」这张表（含表头）贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `明细表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或只剩合计行），没有任何票务结算明细行');
  }

  const periods = new Set();
  const channels = new Set();
  const sessions = new Set();
  for (const it of t.items) {
    periods.add(cell(it.period));
    channels.add(cell(it.channel));
    sessions.add(cell(it.session));
  }

  const findings = [];
  for (const row of t.items) {
    const a = checkFaceRevenue(row);
    if (a) findings.push(a);
    const b = checkCommission(row);
    if (b) findings.push(b);
    const c = checkSettlement(row);
    if (c) findings.push(c);
    findings.push(...checkBlanksAndNegative(row));
    if (paid) { const d = checkRefundAttribution(row); if (d) findings.push(d); }
    if (paid) { const e = checkCrossPeriod(row); if (e) findings.push(e); }
  }
  findings.push(...checkDuplicateOrder(t.items));
  if (paid) findings.push(...checkChannelRateDrift(t.items));
  if (paid) findings.push(...checkFacePriceDrift(t.items));
  findings.push(...checkTotalRow(t.totals, t.items));

  const notRun = [];
  if (!paid) notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let qtyTotal = 0;
  let faceTotal = 0;
  let commissionTotal = 0;
  let refundTotal = 0;
  let settlementTotal = 0;
  for (const it of t.items) {
    const q = num(it, 'qty');
    if (q !== null) qtyTotal += q;
    const f = num(it, 'faceRevenue');
    if (f !== null) faceTotal += f;
    const c = num(it, 'commission');
    if (c !== null) commissionTotal += c;
    const rf = num(it, 'refund');
    if (rf !== null) refundTotal += rf;
    const s = num(it, 'settlement');
    if (s !== null) settlementTotal += s;
  }

  const result = {
    status: 'success',
    service_type: 'TICKET_REVENUE_CHECK',
    scope: {
      checks: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.size,
      channels: channels.size,
      sessions: sessions.size,
      totals_row: Boolean(t.totals.row),
      totals_rows: t.totals.rows || 0,
      qty_total: round2(qtyTotal),
      face_revenue_total: round2(faceTotal),
      commission_total: round2(commissionTotal),
      refund_total: round2(refundTotal),
      settlement_total: round2(settlementTotal),
      statement_settlement_total: t.totals.row ? num(t.totals.row, 'settlement') : null,
      commission_rate_unit: '百分数',
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periods.size,
      channels: channels.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_out_of_scope: OUT_OF_SCOPE,
    note: paid ? '完整档执行全部检查项（含跨渠道 / 跨场次汇总台账、差异归因与按差异金额排序的处理清单）。' : `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"票数 × 票价 = 票面收入"、"票面收入 × 佣金率 = 渠道佣金"、"票面收入 − 渠道佣金 − 退票金额 = 结算金额"'
      + '这三步**表内勾稽**，以及合计行与明细的加总关系；不判断票房是否真实、票款是否到账、佣金率该按哪一版合同，'
      + '**也不做任何税务申报核定**；每条结论都带**原文行号**与订单号，可由第三方用同一份输入复算。',
  };

  if (paid) {
    const ledger = buildChannelLedger(t.items);
    const plan = buildDispositionList(t.items);
    result.channel_ledger = ledger;
    result.disposition_list = plan;
    result.differential_summary = {
      rows_with_diff: plan.rows,
      diff_total: plan.diff_total,
      largest_diff: plan.entries.length ? plan.entries[0].diff : 0,
      basis: '逐行差异金额取「票面收入勾稽差、渠道佣金复算差、结算金额复算差」三项里绝对值最大的一项；'
        + '跨渠道 / 跨场次台账按行汇总，退票金额按记账渠道归集；退票归属异常与跨期结算即使金额为 0 也进处理清单。',
    };
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
  CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, REQUIRED, ROLES, NUMBER_ROLES,
};
