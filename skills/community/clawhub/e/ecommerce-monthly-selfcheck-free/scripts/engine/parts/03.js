/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * live-commerce-commission-check.js —— 直播佣金与坑位费结算核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月结算日 / 付款前**。品牌方与 MCN / 达人的每一场直播，
 * 结算单上的三块钱必须自己算一遍，不能只看对方给的数：
 *
 *   应付佣金 = 结算 GMV × 佣金率
 *   实际应付 = 应付佣金 + 坑位费 − 退货扣减
 *
 * 这两条是**逐行勾稽**：佣金算高了就是多付达人钱，退货扣减漏了就是把退回来的货也付了佣金；
 * 而这张表的每一格都能手算复现，所以"对不对"完全可以机械核出来。
 *
 * 与平台后台（巨量百应 / 淘宝联盟 / 视频号助手等）结算单的一致性核对，
 * 靠的是把后台结算单的「结算 GMV / 佣金 / 坑位费 / 退货扣减」按同一口径填进这张表，
 * 再用本工具把表内勾稽与档位提示全部核一遍。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   应付佣金 = 结算 GMV × 佣金率
 *   实际应付 = 应付佣金 + 坑位费 − 退货扣减
 *   合计行各列 = 全部明细行相加（每一列都是可加口径）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**某位达人的佣金率 / 坑位费到底该按合同哪个口径算（那属于合同解释）：
 *    表里给的结算 GMV、佣金率、坑位费、退货扣减一律**以你填的为准**，本工具只核表内勾稽。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER ——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关 / 条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（saas 那一轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '应付佣金复算（结算 GMV × 佣金率 = 应付佣金）',
  '实际应付复算（应付佣金 + 坑位费 − 退货扣减 = 实际应付）',
  '合计行逐列复核',
  '同一场次重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '佣金率与合同佣金率不一致提示',
  '退货扣减超过结算 GMV 提示',
  '佣金超过结算 GMV 提示',
  '同一达人同一场次重复结算提示',
  '坑位费为零却有坑位约定（备注含坑位）提示',
];

const OUT_OF_SCOPE = [
  '判断某位达人的佣金率、坑位费到底该按合同的哪个口径算（佣金率是含税还是不含税、坑位费是否含服务费，属于合同解释，请以合同与达人约定为准）',
  '核对平台后台结算单与银行到账金额是否一致（本工具只核你贴进来的这张表的表内勾稽，不做银行流水核对）',
  '处理含税/不含税、平台技术服务费、优惠券与运费险分摊等口径差异对结算 GMV 的影响',
  '判断退货率是否异常、退货是否跨结算周期冲回（本工具只按你填的退货扣减做算术复核）',
  '读取巨量百应 / 淘宝联盟 / 视频号助手等平台后台的导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '结算期间\t直播场次\t达人名称\t结算GMV\t佣金率\t应付佣金\t坑位费\t退货扣减\t实际应付\t合同佣金率\t备注',
  '2026-01\tLC-2026-0101-A\t星野小满\t200000.00\t20%\t40000.00\t30000.00\t12000.00\t58000.00\t20%\t首场专场',
  '2026-01\tLC-2026-0101-A\t阿凯说车\t150000.00\t15%\t22500.00\t20000.00\t5000.00\t37500.00\t15%\t',
  '2026-02\tLC-2026-0205-B\t星野小满\t180000.00\t20%\t36000.00\t30000.00\t9000.00\t57000.00\t20%\t返场',
  '2026-02\tLC-2026-0205-B\t阿凯说车\t120000.00\t15%\t18000.00\t0.00\t3000.00\t15000.00\t15%\t纯佣合作无保底',
  '合计\t\t\t650000.00\t\t116500.00\t80000.00\t29000.00\t167500.00\t\t',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;                    // 比例容差：0.05 个百分点

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前（「合同佣金率」不能被「佣金率」抢走、「应付佣金」不能被更宽泛的别名抢走）
  period: ['结算期间', '所属期间', '会计期间', '账期', '期间', '月份', '月度'],
  session: ['直播场次', '场次编号', '场次号', '场次'],
  talent: ['达人名称', '达人昵称', '主播名称', '达人', '主播'],
  gmv: ['结算GMV', '结算gmv', '结算销售额', '成交金额', 'GMV', 'gmv', '销售额'],
  contractRate: ['合同佣金率', '合同约定佣金率', '约定佣金率'],
  commissionRate: ['佣金率', '佣金比例', '佣金比率', '佣金点位'],
  commission: ['应付佣金', '应付佣金金额', '达人佣金', '佣金金额', '佣金'],
  slotFee: ['坑位费', '坑位服务费', '坑位费用', '坑位'],
  returnDeduct: ['退货扣减', '退货扣款', '退货退款扣减', '退货金额', '退货'],
  payable: ['实际应付', '应付合计', '应付总额', '应付金额', '实付金额', '结算应付'],
  remark: ['备注说明', '备注', '说明'],
};

const LABELS = {
  period: '结算期间', session: '直播场次', talent: '达人名称', gmv: '结算GMV',
  commissionRate: '佣金率', commission: '应付佣金', slotFee: '坑位费',
  returnDeduct: '退货扣减', payable: '实际应付', contractRate: '合同佣金率', remark: '备注',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'session', 'talent', 'gmv', 'commissionRate', 'commission',
  'slotFee', 'returnDeduct', 'payable'];
/** 合计行逐列复核的列（这几列都是**可加**口径） */
const SUM_ROLES = ['gmv', 'commission', 'slotFee', 'returnDeduct', 'payable'];
/**
 * 免费档负值检测覆盖的列。
 * ⚠️ 刻意**不含**「实际应付」：退货扣减超过佣金 + 坑位费时，实际应付为负是**真实业务形态**
 *    （达人要倒退钱），它属于完整档「退货扣减超过结算 GMV」那条的射程，免费档提前报出来
 *    等于把付费结论送出去了。
 */
const NEGATIVE_ROLES = ['gmv', 'commission', 'slotFee', 'returnDeduct'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：|总计：|小计：)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
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

/** 比率归一化成小数：`20%` ⇒ 0.2；`0.2` ⇒ 0.2；`20` ⇒ 0.2 */
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
    // 合计行：任意一格写着「合计 / 总计 / 小计」即认定（不同人的表把合计写在第一列或第二列都有）
    let isTotal = false;
    for (const c of cells) {
      if (TOTAL_WORDS.test(String(c).trim())) { isTotal = true; break; }
    }
    roles.forEach((role, c) => {
      if (!role) return;
      row[role] = cells[c] === undefined ? '' : cells[c];
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; } else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const p = it && it.period !== undefined && String(it.period).trim() !== ''
    ? String(it.period).trim() : `第 ${it && it.line} 行`;
  const n = [it && it.session, it && it.talent]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

const sessionKeyOf = (it) => {
  const s = it && it.session !== undefined ? String(it.session).trim() : '';
  return s || `第 ${it && it.line} 行`;
};

/** 整行指纹：所有已识别角色的值（用于判"这一行是不是被原样粘了两遍"） */
const rowSignature = (it) => Object.keys(ROLES)
  .map((r) => String(it[r] === undefined || it[r] === null ? '' : it[r]).trim()).join('|');

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkCommissionRecompute(it) {
  const out = [];
  const gmv = normNumber(it.gmv);
  const rate = rateValue(it.commissionRate);
  const stated = normNumber(it.commission);
  if (gmv === null || rate === null || stated === null) return out;
  const expect = round2(gmv * rate);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '应付佣金与佣金率复算不符', line: it.line,
    message: `${who(it)}：结算 GMV ${gmv.toFixed(2)} × 佣金率 ${(rate * 100).toFixed(4)}% = ${expect.toFixed(2)}，`
      + `表里「应付佣金」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '佣金就是结算 GMV 乘佣金率，算高了就是白付给达人的钱。',
  });
  return out;
}

function checkPayableRecompute(it) {
  const out = [];
  const commission = normNumber(it.commission);
  const slot = normNumber(it.slotFee);
  const back = normNumber(it.returnDeduct);
  const stated = normNumber(it.payable);
  if (commission === null || slot === null || back === null || stated === null) return out;
  const expect = round2(commission + slot - back);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '实际应付与组成项复算不符', line: it.line,
    message: `${who(it)}：应付佣金 ${commission.toFixed(2)} + 坑位费 ${slot.toFixed(2)} − 退货扣减 ${back.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「实际应付」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '实际应付就是"佣金 + 坑位费 − 退货扣减"，这一格错了，付款金额直接跟着错。',
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
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，本表 ${n} 行明细的「${LABELS[role]}」相加是 ${expect.toFixed(2)}，`
        + `相差 ${round2(stated - expect).toFixed(2)}。合计行是付款审批看的那一行，它错了整张表都不可信。`,
    });
  }
  return out;
}

function checkDuplicateRows(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    if (!String(it.session === undefined ? '' : it.session).trim()) continue;
    const key = rowSignature(it);
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一场次重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已整行出现过，第 ${it.line} 行的场次、达人与各列金额与它一字不差 —— `
          + '这一行是被原样粘了两遍。重复的一行会让佣金、坑位费和退货扣减各被多算一次。',
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
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
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 结算 GMV、应付佣金、坑位费与退货扣减都不该为负，`
        + '退货/冲回应单独列示，并在备注里说明冲的是哪一场。',
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
    return insufficient('没有收到直播佣金与坑位费结算核对表正文（text）—— 请把「结算期间 / 直播场次 / 达人名称 / 结算GMV / 佣金率 / 应付佣金 / 坑位费 / 退货扣减 / 实际应付」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `直播佣金与坑位费结算核对表缺少必需列：${t.missingColumns.join('、')}`,
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
    findings.push(...checkCommissionRecompute(it));
    findings.push(...checkPayableRecompute(it));
    findings.push(...checkNegative(it));

  }

  findings.push(...checkTotalRow(t.totals, t.items));
  findings.push(...checkDuplicateRows(t.items));
  findings.push(...checkBlanks(t.items));

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let gmvTotal = 0;
  let payableTotal = 0;
  for (const it of t.items) {
    const g = normNumber(it.gmv);
    if (g !== null) gmvTotal += g;
    const p = normNumber(it.payable);
    if (p !== null) payableTotal += p;
  }

  const result = {
    status: 'success',
    service_type: 'LIVE_COMMERCE_COMMISSION_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      gmv_total: round2(gmvTotal),
      payable_total: round2(payableTotal),
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
    disclaimer: '只核"结算 GMV × 佣金率 = 应付佣金"、"应付佣金 + 坑位费 − 退货扣减 = 实际应付"这类**表内勾稽**与档位提示，'
      + '**不判断佣金率与坑位费到底该按合同哪个口径算**（以合同与达人约定为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
