/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * ecommerce-refund-settlement-check.js —— 电商退货退款与货款结算核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月平台结算单到账、月报出数之前**。做电商的公司，
 * 财务每个月都要把平台结算单里的货款、佣金、退货退款、赔付、扣款与订单明细逐笔对上。
 * 这张表算错，方向只有两个 —— **退货退款/扣款漏了一笔**（等于白给平台钱）或
 * **应结货款/结算净额算错**（账实不符，月报、平台对账、审计抽样三处同时暴露）。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   应结货款 = 订单金额 − 退款金额 − 平台佣金
 *   结算净额 = 应结货款 + 赔付金额 − 扣款金额
 *   合计行各列 = 明细行相加
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**佣金该按什么口径计、退货该不该回收入库、赔付与扣款该不该认（那属于
 *    平台协议、合同与会计判断）：表里给的订单金额、退款金额、平台佣金、佣金率、退货入库状态
 *    一律**以你填的为准**，本工具只核表内勾稽，并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '应结货款复算（订单金额 − 退款金额 − 平台佣金 = 应结货款）',
  '结算净额复算（应结货款 + 赔付金额 − 扣款金额 = 结算净额）',
  '合计行逐列复核',
  '同一订单号同一期间重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '退款金额超过订单金额提示',
  '平台佣金率与合同佣金率不一致提示',
  '退货已退款但未回收入库提示',
  '结算净额为负提示',
  '同一订单跨期间重复结算提示',
];

const OUT_OF_SCOPE = [
  '判断平台佣金该按什么口径计（类目费率、活动期优惠费率、达人分成、技术服务费与佣金是否分开列，属于平台协议判断）',
  '判断退货该不该回收入库、退货是否影响二次销售（属于仓储与质检判断）',
  '判断平台赔付与扣款该不该认（先行赔付、违约金、保证金扣划、罚款的认定属于合同与法务判断）',
  '核对平台结算单本身（结算单金额与银行到账流水是否一致、跨月结算的时间性差异）',
  '处理增值税、平台开票、收入确认时点与退货的会计处理（属于税务与会计政策判断）',
  '读取平台后台 / ERP / 电商中台导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '结算期间\t平台\t店铺\t订单号\t订单金额\t退款金额\t退货数量\t平台佣金\t平台佣金率\t合同佣金率\t赔付金额\t扣款金额\t应结货款\t结算净额\t退货入库状态',
  '2026-01\t天猫\tXX旗舰店\tSO-2026-0101\t1200.00\t0.00\t0\t60.00\t5.00%\t5.00%\t0.00\t0.00\t1140.00\t1140.00\t无需退货',
  '2026-01\t天猫\tXX旗舰店\tSO-2026-0102\t800.00\t200.00\t1\t40.00\t5.00%\t5.00%\t0.00\t10.00\t560.00\t550.00\t已入库',
  '2026-02\t天猫\tXX旗舰店\tSO-2026-0201\t1500.00\t0.00\t0\t75.00\t5.00%\t5.00%\t30.00\t0.00\t1425.00\t1455.00\t无需退货',
  '2026-02\t天猫\tXX旗舰店\tSO-2026-0202\t600.00\t100.00\t1\t30.00\t5.00%\t5.00%\t0.00\t0.00\t470.00\t470.00\t已入库',
  '2026-03\t京东\tXX旗舰店\tSO-2026-0301\t2000.00\t300.00\t1\t100.00\t5.00%\t5.00%\t0.00\t50.00\t1600.00\t1550.00\t已入库',
  '2026-03\t京东\tXX旗舰店\tSO-2026-0302\t900.00\t0.00\t0\t45.00\t5.00%\t5.00%\t0.00\t0.00\t855.00\t855.00\t无需退货',
  '合计\t\t\t\t7000.00\t600.00\t3\t350.00\t\t\t30.00\t60.00\t6050.00\t6020.00\t',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;      // 佣金率容差：0.05 个百分点

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前，且**别名越短越宽的角色越靠后**
  //    （「平台佣金率」不能被「平台佣金」抢走、「合同佣金率」不能被「平台佣金率」抢走、
  //      「退货入库状态」不能被「退货数量」抢走；
  //      ⚠️ `platform` 的别名里有裸词「平台」⇒ 它必须排在**所有带"平台"两字的角色之后**，
  //      否则「平台佣金」「平台佣金率」会被它整列抢走 —— 实测本引擎第一版就是这样：
  //      「平台佣金」被认成 platform ⇒ 必需列 commission 永远认不出来 ⇒ 所有输入都
  //      insufficient_input。这正是 `tools/header_map_check.py` 要钉的那类坑。）
  period: ['结算期间', '结算账期', '会计期间', '所属期间', '所属期', '账期', '期间', '月份', '月度'],
  shop: ['店铺名称', '店铺账号', '店铺', '账号', '商户', '经营主体', '主体'],
  order: ['子订单编号', '子订单号', '订单编号', '订单号', '交易号', '交易编号'],
  orderAmount: ['订单实付金额', '订单应付金额', '订单总金额', '订单金额', '成交金额', '商品金额', '实付金额', '订单总额'],
  refundAmount: ['退货退款金额', '已退款金额', '退款总金额', '退款金额', '退款总额', '退款'],
  returnStatus: ['退货入库状态', '退货回收状态', '退货状态', '入库状态', '是否入库', '回收入库'],
  returnQty: ['退货件数', '退货数量', '退回数量', '退货单数', '退货笔数'],
  compensate: ['平台赔付金额', '赔付金额', '补偿金额', '平台赔付', '赔付款', '赔付'],
  deduction: ['平台扣款金额', '扣款金额', '其他扣款', '扣减金额', '罚款金额', '扣款', '罚款'],
  contractRate: ['合同佣金率', '合同佣金比例', '合同费率', '约定佣金率', '约定费率'],
  commissionRate: ['平台佣金率', '佣金率', '佣金比例', '佣金比率', '费率'],
  commission: ['平台佣金', '佣金金额', '平台服务费', '技术服务费', '佣金'],
  platform: ['电商平台', '销售平台', '平台名称', '平台'],
  payable: ['应结算货款', '应结货款', '应付货款', '结算货款', '货款金额', '货款'],
  net: ['结算净额', '净结算额', '结算净金额', '结算净收入', '实结金额', '净额'],
};

const LABELS = {
  period: '结算期间', platform: '平台', shop: '店铺', order: '订单号', orderAmount: '订单金额',
  refundAmount: '退款金额', returnStatus: '退货入库状态', returnQty: '退货数量',
  compensate: '赔付金额', deduction: '扣款金额', contractRate: '合同佣金率',
  commissionRate: '平台佣金率', commission: '平台佣金', payable: '应结货款', net: '结算净额',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'order', 'orderAmount', 'refundAmount', 'commission',
  'compensate', 'deduction', 'payable', 'net'];
/** 合计行逐列复核的列 */
const SUM_ROLES = ['orderAmount', 'refundAmount', 'returnQty', 'commission', 'compensate',
  'deduction', 'payable', 'net'];
/**
 * 免费档负值检测覆盖的列：**进货侧 / 订单侧**的金额与比率。
 * ⚠️ 刻意**不含**应结货款与结算净额 —— "退款金额超过订单金额导致应结货款为负"与
 *    "结算净额为负"都是完整档的独立检查项（见 CHECKS_WITHHELD），
 *    免费档提前报出这两个负数就等于把付费结论送出去了。
 */
const NEGATIVE_ROLES = ['orderAmount', 'refundAmount', 'returnQty', 'commission',
  'compensate', 'deduction', 'commissionRate', 'contractRate'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|合计：|汇总)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|空|暂无)$/i.test(s);
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

/** 费率归一化成小数：`5%` ⇒ 0.05；`0.05` ⇒ 0.05；`5` ⇒ 0.05 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
}

const round2 = (n) => Math.round(n * 100) / 100;
/** 数量列不带小数、金额列两位小数（同一条检查项里两种列都可能出现） */
const show = (role, v) => (role === 'returnQty' ? String(round2(v)) : v.toFixed(2));

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
      if (role === 'period' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const p = it && it.period !== undefined && String(it.period).trim() !== ''
    ? String(it.period).trim() : `第 ${it && it.line} 行`;
  const n = [it && it.platform, it && it.order]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkPayable(it) {
  const out = [];
  const amount = normNumber(it.orderAmount);
  const refund = normNumber(it.refundAmount);
  const commission = normNumber(it.commission);
  const stated = normNumber(it.payable);
  if (amount === null || refund === null || commission === null || stated === null) return out;
  const expect = round2(amount - refund - commission);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '应结货款复算不符', line: it.line,
    message: `${who(it)}：订单金额 ${amount.toFixed(2)} − 退款金额 ${refund.toFixed(2)} − 平台佣金 ${commission.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「应结货款」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '货款只认这三个数：订单金额 − 退款 − 佣金。退货退款漏扣一笔、佣金多算一笔，这里立刻对不上，'
      + '而这一列就是跟平台结算单对数、也是月报取数的那一列。',
  });
  return out;
}

function checkNet(it) {
  const out = [];
  const payable = normNumber(it.payable);
  const compensate = normNumber(it.compensate);
  const deduction = normNumber(it.deduction);
  const stated = normNumber(it.net);
  if (payable === null || compensate === null || deduction === null || stated === null) return out;
  const expect = round2(payable + compensate - deduction);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '结算净额复算不符', line: it.line,
    message: `${who(it)}：应结货款 ${payable.toFixed(2)} + 赔付金额 ${compensate.toFixed(2)} − 扣款金额 ${deduction.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「结算净额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '结算净额才是这一期真正能收到的钱：赔付要加、扣款要减，方向弄反或者漏了一笔扣款，'
      + '月报的收入与银行到账都会跟着错。',
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
      message: `合计行的「${LABELS[role]}」是 ${show(role, stated)}，本表 ${n} 行明细的「${LABELS[role]}」相加是 ${show(role, expect)}，`
        + `相差 ${show(role, round2(stated - expect))}。合计行就是与平台结算单对数、也是月报的取数口径，`
        + '对不上说明明细或合计至少有一边错（明细改了合计没跟着改是最常见的一种）。',
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined && it.period !== null ? String(it.period).trim() : '';
    const o = it.order !== undefined && it.order !== null ? String(it.order).trim() : '';
    if (!p || !o) continue;
    const key = `${p}|${o}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一订单号重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一结算期间、同一订单号再次出现 —— `
          + '要么是重复粘贴了一行，要么是同一笔订单被拆成两行（比如按商品、按子订单各建一行，'
          + '而订单金额又各自抄了整单金额）。多出来的那一行会把订单金额、退款与佣金都重复计一遍。',
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
        const s = String(it[role] === undefined || it[role] === null ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`
            + '这一列缺失时对应的复算做不了：缺哪一列就补哪一列，别让空值静默跳过检查。',
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const isRate = role === 'commissionRate' || role === 'contractRate';
    const v = isRate ? rateValue(it[role]) : normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    const shown = isRate ? `${(v * 100).toFixed(4)}%` : show(role, v);
    out.push({
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${shown}（负数）—— 订单金额、退款金额、退货数量、佣金、赔付与扣款都不该为负；`
        + '冲回 / 红字 / 平台倒扣应当单独列示并在备注里说明，混成正负数会让合计与净额一起错。',
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
    return insufficient('没有收到电商退货退款与货款结算核对表正文（text）—— 请把「结算期间 / 平台 / 店铺 / 订单号 / 订单金额 / 退款金额 / 退货数量 / 平台佣金 / 平台佣金率 / 合同佣金率 / 赔付金额 / 扣款金额 / 应结货款 / 结算净额 / 退货入库状态」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `电商退货退款与货款结算核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何结算明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkPayable(it));
    findings.push(...checkNet(it));
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

  const sums = { orderAmount: 0, refundAmount: 0, commission: 0, payable: 0, net: 0 };
  for (const it of t.items) {
    for (const role of Object.keys(sums)) {
      const v = normNumber(it[role]);
      if (v !== null) sums[role] += v;
    }
  }

  const result = {
    status: 'success',
    service_type: 'ECOM_REFUND_SETTLEMENT_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      order_amount_total: round2(sums.orderAmount),
      refund_total: round2(sums.refundAmount),
      commission_total: round2(sums.commission),
      payable_total: round2(sums.payable),
      net_total: round2(sums.net),
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
    disclaimer: '只核"订单金额 − 退款金额 − 平台佣金 = 应结货款"与"应结货款 + 赔付金额 − 扣款金额 = 结算净额"'
      + '这类**表内勾稽**与档位提示，**不判断平台佣金该按什么口径计、退货该不该回收入库、赔付与扣款该不该认**'
      + '（以平台结算单、平台协议与会计师口径为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
