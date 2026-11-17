/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * clinic-daily-cashier-check.js —— 门诊收费与退费日结核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每天收费处下班前**。门诊收费处每天都要日结一次：
 * 挂号、诊疗、药品、检查各渠道的收款（现金 / 扫码 / 医保）要与收费系统日报、
 * 退费单据、实际到账逐项对上。差一分钱下不了班，也对不上账。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   应收合计 = 挂号收款 + 诊疗收款 + 药品收款 + 检查收款
 *   实收净额 = 收款合计 − 退费合计
 *   合计行各列 = 明细行相加（一行 = 一个收费员一个班次一张日结单）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**某笔费用该不该收、该不该退（那属于医嘱、物价政策与医保政策判断）：
 *    表里填的各渠道金额、系统日报金额、现金缴存额一律**以你填的为准**，本工具只核表内勾稽，
 *    并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出那个开关 / 条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '应收合计=各渠道收款合计复算（挂号 + 诊疗 + 药品 + 检查 = 应收合计）',
  '实收净额复算（收款合计 − 退费合计 = 实收净额）',
  '合计行逐列复核',
  '同一收费员同一班次重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '系统日报金额与实收净额不符提示（收费系统日报与当日实收对不上）',
  '退费超过当日收款提示（当日退费合计大于当日收款合计）',
  '现金缴存额与现金收款不符（长短款）提示',
  '同一单据重复退费提示（同一单据号出现两次且都带退费金额）',
  '医保结算金额与医保回款不符提示（医保申报结算与医保实际到账对不上）',
];

const OUT_OF_SCOPE = [
  '判断某笔费用该不该收、该不该退（医嘱、诊疗规范、物价文件与收费标准口径，属于业务与物价判断，请咨询医务科与物价部门）',
  '判断医保拒付、医保扣款、DRG / DIP 结算差异的成因与申述（属于医保政策判断，请咨询医保办）',
  '读取 HIS / 收费系统 / 医保结算系统里的原始记录（需要你先导出成文本贴进来）',
  '核对银行卡 / 微信 / 支付宝 / POS 的到账流水与手续费（需要支付渠道与银行对账单）',
  '处理发票作废、红冲、跨日退费、跨月退费的会计与税务处理',
  '认定长短款的责任与赔偿（属于内部管理与人事判断）',
];

const SAMPLE_TEXT = [
  '日期\t班次\t收费员\t单据号\t挂号收款\t诊疗收款\t药品收款\t检查收款\t应收合计\t现金收款\t扫码收款\t医保收款\t收款合计\t退费合计\t实收净额\t系统日报金额\t现金缴存额\t医保结算金额\t医保回款',
  '2026-03-01\t白班\t张丽\tDJ-20260301-A\t1200.00\t3400.00\t5600.00\t2800.00\t13000.00\t2000.00\t4000.00\t7000.00\t13000.00\t0.00\t13000.00\t13000.00\t2000.00\t7000.00\t7000.00',
  '2026-03-01\t夜班\t王强\tDJ-20260301-B\t300.00\t900.00\t1500.00\t600.00\t3300.00\t800.00\t1200.00\t1300.00\t3300.00\t200.00\t3100.00\t3100.00\t800.00\t1300.00\t1300.00',
  '2026-03-02\t白班\t张丽\tDJ-20260302-A\t1500.00\t2800.00\t4200.00\t1900.00\t10400.00\t1500.00\t3300.00\t5600.00\t10400.00\t350.00\t10050.00\t10050.00\t1500.00\t5600.00\t5600.00',
  '2026-03-02\t夜班\t李敏\tDJ-20260302-B\t200.00\t700.00\t1100.00\t500.00\t2500.00\t600.00\t900.00\t1000.00\t2500.00\t0.00\t2500.00\t2500.00\t600.00\t1000.00\t1000.00',
  '2026-03-03\t白班\t王强\tDJ-20260303-A\t400.00\t1000.00\t2600.00\t800.00\t4800.00\t900.00\t1500.00\t2400.00\t4800.00\t150.00\t4650.00\t4650.00\t900.00\t2400.00\t2400.00',
  '2026-03-03\t夜班\t李敏\tDJ-20260303-B\t100.00\t500.00\t800.00\t300.00\t1700.00\t400.00\t600.00\t700.00\t1700.00\t0.00\t1700.00\t1700.00\t400.00\t700.00\t700.00',
  '合计\t\t\t\t3700.00\t9300.00\t15800.00\t6900.00\t35700.00\t6200.00\t11500.00\t18000.00\t35700.00\t700.00\t35000.00\t35000.00\t6200.00\t18000.00\t18000.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前。否则宽泛别名会把具体列**抢走**
  //    （「医保结算金额」「医保回款」不能被「医保收款」抢走、
  //     「现金缴存额」不能被「现金收款」抢走、「系统日报金额」不能被别的金额列抢走）
  date: ['收费日期', '业务日期', '交易日期', '结算日期', '日结日期', '日期'],
  shift: ['班次', '班别', '值班班次'],
  cashier: ['收费员姓名', '收费员', '收银员', '收款员', '操作员'],
  docNo: ['日结单号', '收费单据号', '单据编号', '单据号', '凭证号', '流水号', '票据号'],
  sysDaily: ['系统日报金额', 'HIS日报金额', '收费系统日报', '系统日报', '日报金额', '日报'],
  cashDeposit: ['现金缴存额', '现金缴存金额', '现金送存额', '缴存现金', '现金存入', '缴存额'],
  insuranceSettle: ['医保结算金额', '医保结算款', '医保申报金额', '医保结算'],
  insuranceBack: ['医保回款', '医保拨付金额', '医保到账金额', '医保拨款', '回款金额'],
  reg: ['挂号收款', '挂号收入', '挂号金额', '挂号费', '挂号'],
  clinic: ['诊疗收款', '诊疗收入', '诊疗金额', '诊疗费', '诊疗'],
  drug: ['药品收款', '药品收入', '药品金额', '药品费', '药品'],
  exam: ['检查收款', '检查收入', '检查金额', '检查费', '检查'],
  receivable: ['应收合计', '应收金额合计', '应收金额', '应交合计', '应收'],
  received: ['收款合计', '实收合计', '收款总额', '合计收款'],
  refund: ['退费合计', '退款合计', '退费金额', '退费'],
  net: ['实收净额', '净收款金额', '结算净额', '实收金额', '净额'],
  cash: ['现金收款', '现金收入', '现金金额', '现金'],
  scan: ['扫码收款', '扫码收入', '微信收款', '支付宝收款', '聚合支付收款', '扫码'],
  insurance: ['医保收款', '医保收入', '医保统筹收款', '医保金额', '医保'],
};

const LABELS = {
  date: '日期', shift: '班次', cashier: '收费员', docNo: '单据号',
  sysDaily: '系统日报金额', cashDeposit: '现金缴存额',
  insuranceSettle: '医保结算金额', insuranceBack: '医保回款',
  reg: '挂号收款', clinic: '诊疗收款', drug: '药品收款', exam: '检查收款',
  receivable: '应收合计', received: '收款合计', refund: '退费合计', net: '实收净额',
  cash: '现金收款', scan: '扫码收款', insurance: '医保收款',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['date', 'shift', 'cashier', 'docNo', 'reg', 'clinic', 'drug', 'exam',
  'receivable', 'cash', 'scan', 'insurance', 'received', 'refund', 'net'];
/** 各渠道收款列：应收合计 = 这四列之和 */
const CHANNEL_ROLES = ['reg', 'clinic', 'drug', 'exam'];
/** 合计行逐列复核的列（都是可加总的金额列） */
const SUM_ROLES = ['reg', 'clinic', 'drug', 'exam', 'receivable', 'cash', 'scan', 'insurance',
  'received', 'refund', 'net', 'sysDaily', 'cashDeposit', 'insuranceSettle', 'insuranceBack'];
/**
 * 免费档负值检测覆盖的列。
 * ⚠️ 刻意**不含**实收净额 —— "退费超过当日收款"是完整档的独立检查项（见 CHECKS_WITHHELD），
 *    净额被退费冲成负数正是那个结论的表现，免费档提前报出来就等于把付费结论送出去了。
 */
const NEGATIVE_ROLES = ['reg', 'clinic', 'drug', 'exam', 'receivable', 'cash', 'scan', 'insurance',
  'received', 'refund', 'sysDaily', 'cashDeposit', 'insuranceSettle', 'insuranceBack'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|空|未结)$/i.test(s);
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
      if (role === 'date' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

function who(it) {
  const parts = [it && it.date, it && it.shift, it && it.cashier]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' ');
  return parts || `第 ${it && it.line} 行`;
}

function dayKeyOf(it) {
  const d = it && it.date !== undefined ? String(it.date).trim() : '';
  return d || `第 ${it && it.line} 行`;
}

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkReceivable(it) {
  const out = [];
  const stated = normNumber(it.receivable);
  const vals = CHANNEL_ROLES.map((r) => normNumber(it[r]));
  if (stated === null || vals.some((v) => v === null)) return out;
  const expect = round2(vals.reduce((a, b) => a + b, 0));
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '应收合计与各渠道收款之和不符', line: it.line,
    message: `${who(it)}：挂号 ${vals[0].toFixed(2)} + 诊疗 ${vals[1].toFixed(2)} + 药品 ${vals[2].toFixed(2)}`
      + ` + 检查 ${vals[3].toFixed(2)} = ${expect.toFixed(2)}，表里「应收合计」是 ${stated.toFixed(2)}，`
      + `相差 ${round2(stated - expect).toFixed(2)}。`
      + '应收合计就是当天日报与收费系统报表的取数口径：四个渠道里有一个填错、或者合计时漏了一个渠道，'
      + '都会让日报总账对不上。',
  });
  return out;
}

function checkNet(it) {
  const out = [];
  const received = normNumber(it.received);
  const refund = normNumber(it.refund);
  const stated = normNumber(it.net);
  if (received === null || refund === null || stated === null) return out;
  const expect = round2(received - refund);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '实收净额复算不符', line: it.line,
    message: `${who(it)}：收款合计 ${received.toFixed(2)} − 退费合计 ${refund.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「实收净额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '实收净额是交款、缴存与日报的落脚点：这一格错了，后面每一步都会跟着错。',
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
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，本表 ${n} 行明细的「${LABELS[role]}」`
        + `相加是 ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
        + '合计行就是日报、缴款单与账务的取数口径，对不上说明有一边错。',
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const d = it.date !== undefined ? String(it.date).trim() : '';
    const s = it.shift !== undefined ? String(it.shift).trim() : '';
    const c = it.cashier !== undefined ? String(it.cashier).trim() : '';
    if (!d || !s || !c) continue;
    const key = `${d}|${s}|${c}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一收费员同一班次重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经日结过一次，第 ${it.line} 行同一日期、同一班次、`
          + '同一收费员又出现一次 —— 要么是重复粘贴了一行，要么是把同一张日结单按渠道拆成了两行。'
          + '多出来的那一行会把收款与退费都重复计一遍，交款时就对不上。',
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
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    out.push({
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— `
        + '各渠道收款、收款合计、退费合计、日报金额与缴存额都不该为负：'
        + '冲回 / 红字应当单独列示并在备注里说明，符号掉了会让当天的收款凭空变少。',
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
    return insufficient('没有收到门诊收费与退费日结核对表正文（text）—— 请把「日期 / 班次 / 收费员 / 单据号 / 挂号收款 / 诊疗收款 / 药品收款 / 检查收款 / 应收合计 / 现金收款 / 扫码收款 / 医保收款 / 收款合计 / 退费合计 / 实收净额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `门诊收费与退费日结核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何收费日结明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = dayKeyOf(it);
    if (!groups.has(k)) groups.set(k, { day: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkReceivable(it));
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

  let receivableTotal = 0;
  let receivedTotal = 0;
  let refundTotal = 0;
  let netTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.receivable);
    if (a !== null) receivableTotal += a;
    const b = normNumber(it.received);
    if (b !== null) receivedTotal += b;
    const c = normNumber(it.refund);
    if (c !== null) refundTotal += c;
    const d = normNumber(it.net);
    if (d !== null) netTotal += d;
  }

  const result = {
    status: 'success',
    service_type: 'CLINIC_DAILY_CASHIER_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      receivable_total: round2(receivableTotal),
      received_total: round2(receivedTotal),
      refund_total: round2(refundTotal),
      net_total: round2(netTotal),
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
    disclaimer: '只核"应收合计 = 各渠道收款之和"与"实收净额 = 收款合计 − 退费合计"这类**表内勾稽**与档位提示，'
      + '**不判断某笔费用该不该收 / 该不该退**（以医嘱、物价文件与医保政策为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
