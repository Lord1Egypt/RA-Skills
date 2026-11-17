/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * platform-settlement-aging-check.js —— 平台账期与在途资金核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**电商财务每月结账前 / 月末对账时**。天猫、抖音、拼多多、京东
 * 这些平台的钱不会当天到账：订单先变成"待结算"，再按各自账期（T+7 / T+15 / 月结 30 天）
 * 分批结算，结算前先扣掉佣金与推广费，还可能冻结一部分（售后退款保证金、违规冻结）。
 * 这一整套还没到账的钱就是**在途资金**，它必须与"本期发生 / 本期结算 / 结算批次"逐笔勾稽。
 *
 * 这张表算错，方向只有两个 —— **在途余额滚错**（现金流预测虚高或虚低：账上没钱却以为有，
 * 或者有钱没算进来）或 **净结算额扣错**（平台扣费、冻结金额少扣多扣，净额与打款对不上）。
 * 两条都会在现金流误判、坏账漏记和平台对账单核对上暴露出来；逐笔勾稽是每月躲不掉的动作。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   净结算额  = 结算金额 − 平台扣费 − 冻结金额
 *   期末在途  = 期初在途 + 本期发生额 − 本期结算金额
 *   合计行各列 = 明细行相加（账期天数是"天数"，**不参与加总**）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**某个平台该按什么账期结算、佣金与推广费该按什么口径进「平台扣费」、
 *    冻结金额该不该在本期扣（那属于平台协议、结算规则与会计判断）：表里给的账期天数、
 *    平台扣费、冻结金额一律**以你填的为准**，本工具只核表内勾稽，并把可疑处按原文行号列出来。
 *
 * 返回形状约定：每个 check* 一律返回**发现数组**（没有发现就是空数组），不返回 null / 单对象。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关 / 条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '净结算额复算（结算金额 − 平台扣费 − 冻结金额 = 净结算额）',
  '在途余额滚动复算（期初在途 + 本期发生额 − 本期结算金额 = 期末在途）',
  '合计行逐列复核',
  '同一平台同一结算批次重复行检测',
  '空白与占位符检测',
  '金额或账期天数为负检测',
];

const CHECKS_WITHHELD = [
  '账期天数超过参考上限提示（> 60 天）',
  '结算金额超过本期发生额提示',
  '在途余额为负提示',
  '冻结金额占比偏离参考区间提示（参考区间 0 ~ 30%）',
  '同一平台同一结算批次重复结算提示（同一批次跨期间又结算了一次）',
];

const OUT_OF_SCOPE = [
  '判断各平台该按什么账期结算（T+1 / T+7 / T+15 / 月结，账期起算日按订单日还是发货日，属于平台协议与合同判断）',
  '核对「平台扣费」的构成口径（佣金、技术服务费、推广费、达人佣金、运费险是否该计入，是否含税，属于平台结算规则与会计判断）',
  '判断冻结金额该不该在本期扣减、解冻后如何回冲（售后保证金、违规冻结的会计处理以平台规则与会计师口径为准）',
  '核对平台后台 / ERP / 银行流水里的原始数据是否真实（需要你先从平台导出，本工具只核你贴进来的这张表）',
  '处理外币平台折算、增值税、手续费发票、坏账准备计提与现金流预测模型的编制',
];

const SAMPLE_HEAD = ['所属期间', '平台', '结算批次', '账期天数', '期初在途', '本期发生额', '本期结算金额',
  '期末在途', '结算金额', '平台扣费', '冻结金额', '净结算额'];

const SAMPLE_TEXT = [
  SAMPLE_HEAD.join('\t'),
  '2026-01\t天猫\tJS-2026-01-A\t7\t100000.00\t200000.00\t120000.00\t180000.00\t120000.00\t7200.00\t0.00\t112800.00',
  '2026-02\t天猫\tJS-2026-02-A\t15\t180000.00\t250000.00\t150000.00\t280000.00\t150000.00\t9000.00\t30000.00\t111000.00',
  '2026-03\t天猫\tJS-2026-03-A\t30\t280000.00\t300000.00\t260000.00\t320000.00\t260000.00\t15600.00\t78000.00\t166400.00',
  '2026-01\t抖音\tDY-2026-01-B\t10\t50000.00\t80000.00\t60000.00\t70000.00\t60000.00\t3600.00\t6000.00\t50400.00',
  '2026-02\t抖音\tDY-2026-02-B\t20\t70000.00\t90000.00\t50000.00\t110000.00\t50000.00\t3000.00\t10000.00\t37000.00',
  '2026-03\t抖音\tDY-2026-03-B\t45\t110000.00\t120000.00\t100000.00\t130000.00\t100000.00\t6000.00\t15000.00\t79000.00',
  '合计\t\t\t\t790000.00\t1040000.00\t740000.00\t1090000.00\t740000.00\t44400.00\t139000.00\t556600.00',
].join('\n');

const TOL = 0.01;
const AGING_LIMIT_DAYS = 60;      // 账期天数参考上限：超过它就该盯现金流与坏账
const FROZEN_RATIO_MIN = 0;       // 冻结金额占比参考区间下界（负值由负值检测报，这里只拦高出上限）
const FROZEN_RATIO_MAX = 0.30;    // 冻结金额占比参考区间上界：30%

const ROLES = {
  // ⚠️ 两个方向上的顺序都不能错：
  //    ① **角色之间**：更具体的角色在前 —— 否则一个宽泛别名会把更具体的那一列抢走，
  //       后果是"跑起来不报错、但整列不参与检查"（表头映射守卫实测过两次）。
  //       本表的四处真实冲突：`平台扣费`（必须早于 `平台`）、`本期结算金额`（必须早于 `结算金额`）、
  //       `净结算金额`（必须早于 `结算金额`，否则「净结算金额」会被 `结算金额` 抢走）、
  //       `期初在途金额`（必须早于 `期初在途` 与 `在途金额`）。
  //    ② **别名之间**：更长 / 更具体的词在前 —— `账期天数` 早于 `天数`、`期初在途金额` 早于 `在途金额`、
  //       `冻结金额` 早于任何裸的 `金额`（本表刻意**不给任何角色**配裸 `金额` 别名：
  //       一旦有，它就会把 `在途金额` / `冻结金额` / `结算金额` 全部抢走）。
  period: ['所属期间', '结算期间', '会计期间', '所属期', '期间', '月份', '月度'],
  platformFee: ['平台佣金及推广费', '平台技术服务费', '平台手续费', '平台佣金', '平台费用', '平台扣费', '扣费金额'],
  platform: ['电商平台', '平台名称', '店铺平台', '平台'],
  batch: ['结算批次号', '结算批次', '批次号', '结算单编号', '结算单号', '批次'],
  agingDays: ['结算账期天数', '账期天数', '回款天数', '在途天数', '账期', '天数'],
  settled: ['本期结算金额', '本期已结算金额', '本期结算额', '本期已结算', '本期结算', '本期回款'],
  netSettlement: ['净结算金额', '净结算额', '实际结算金额', '实际结算额', '到账金额', '净额'],
  settlementAmount: ['应结算金额', '本批结算金额', '结算金额', '结算总额', '结算款', '结算合计'],
  frozen: ['平台冻结金额', '售后冻结金额', '保证金冻结金额', '冻结金额', '冻结资金', '冻结款'],
  inTransitBegin: ['期初在途金额', '期初在途资金', '上期期末在途', '期初待结算金额', '期初在途', '期初待结算'],
  inTransitEnd: ['期末在途金额', '期末在途资金', '下期期初在途', '期末待结算金额', '期末在途', '期末待结算', '在途金额'],
  occurred: ['本期发生金额', '本期发生额', '本期新增金额', '本期新增', '本期发生', '发生额'],
};

const LABELS = {
  period: '所属期间', platform: '平台', batch: '结算批次', agingDays: '账期天数',
  inTransitBegin: '期初在途', occurred: '本期发生额', settled: '本期结算金额', inTransitEnd: '期末在途',
  settlementAmount: '结算金额', platformFee: '平台扣费', frozen: '冻结金额', netSettlement: '净结算额',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'platform', 'batch', 'agingDays', 'inTransitBegin', 'occurred', 'settled',
  'inTransitEnd', 'settlementAmount', 'platformFee', 'frozen', 'netSettlement'];
/**
 * 合计行逐列复核的列。
 * ⚠️ 刻意**不含账期天数** —— 天数是"每笔的账期长度"，加起来没有业务含义；
 *    把 7 天 + 15 天 + 30 天 加成 52 天去跟合计行比，只会制造误报。
 */
const SUM_ROLES = ['inTransitBegin', 'occurred', 'settled', 'inTransitEnd',
  'settlementAmount', 'platformFee', 'frozen', 'netSettlement'];
/**
 * 免费档负值检测覆盖的列：**结算侧**的金额与账期天数。
 * ⚠️ 刻意**不含**期初在途与期末在途 —— "在途余额为负"是完整档的独立检查项（见 CHECKS_WITHHELD），
 *    免费档提前报出在途为负就等于把付费结论送出去了。
 */
const NEGATIVE_ROLES = ['settlementAmount', 'platformFee', 'frozen', 'netSettlement',
  'occurred', 'settled', 'agingDays'];
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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|空)$/i.test(s);
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
  const n = [it && it.platform, it && it.batch]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

const batchKeyOf = (it) => {
  const p = it && it.platform !== undefined ? String(it.platform).trim() : '';
  const b = it && it.batch !== undefined ? String(it.batch).trim() : '';
  return (p || b) ? `${p}|${b}` : `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkNetSettlement(it) {
  const out = [];
  const amount = normNumber(it.settlementAmount);
  const fee = normNumber(it.platformFee);
  const frozen = normNumber(it.frozen);
  const stated = normNumber(it.netSettlement);
  if (amount === null || fee === null || frozen === null || stated === null) return out;
  const expect = round2(amount - fee - frozen);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '净结算额复算不符', line: it.line,
    message: `${who(it)}：结算金额 ${amount.toFixed(2)} − 平台扣费 ${fee.toFixed(2)} − 冻结金额 ${frozen.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「净结算额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '净结算额就是平台该打给你的钱：它错一位，账面应收与银行到账就对不上 —— '
      + '要么把佣金 / 推广费少扣了（以为能收到，实际没有），要么把冻结金额重复扣了一遍。',
  });
  return out;
}

function checkInTransitRolling(it) {
  const out = [];
  const begin = normNumber(it.inTransitBegin);
  const occurred = normNumber(it.occurred);
  const settled = normNumber(it.settled);
  const stated = normNumber(it.inTransitEnd);
  if (begin === null || occurred === null || settled === null || stated === null) return out;
  const expect = round2(begin + occurred - settled);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '在途余额滚动复算不符', line: it.line,
    message: `${who(it)}：期初在途 ${begin.toFixed(2)} + 本期发生额 ${occurred.toFixed(2)} − 本期结算金额 ${settled.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「期末在途」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '在途余额滚不动，下个月的期初就跟着错，整条现金流预测链条都会偏：'
      + '常见原因是本期结算挂在错误期间、跨批次结算漏记或多记、上一期的期末在途没有带下来。',
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
        + `相差 ${round2(stated - expect).toFixed(2)}。合计行就是月报与现金流预测的取数口径，`
        + '对不上说明有一边错（多半是明细行增删后合计没刷新，或者某一行的这一列被漏加）。',
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined ? String(it.period).trim() : '';
    const pf = it.platform !== undefined ? String(it.platform).trim() : '';
    const b = it.batch !== undefined ? String(it.batch).trim() : '';
    if (!pf || !b) continue;
    const key = `${p}|${pf}|${b}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一平台同一批次重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一期间、同一平台、同一结算批次又出现一次 —— `
          + '要么是重复粘贴了一行（粘贴时多选了一行），要么把同一批次拆成了两行（比如按店铺 / 按币种各记一行）。'
          + '重复的那一行会把在途、结算金额与平台扣费全部重复计一遍，合计行跟着一起错。',
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
            + '这一列缺失时对应的复算做不了：缺哪一列就补哪一列，别让空值静默跳过检查'
            + '（在途余额与净结算额只要少一个数，整行就核不出来）。',
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
    const shown = role === 'agingDays' ? `${v.toFixed(0)} 天` : v.toFixed(2);
    out.push({
      level: 'P0', category: '关键字段为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${shown}（负数）—— 结算金额、平台扣费、冻结金额、净结算额、`
        + '本期发生额、本期结算金额与账期天数都不该为负（账期天数更不该是负的：负数说明取数时把两列相减了）。'
        + '冲回 / 红字应当单独列示并在备注里说明，而不是混进本期明细。',
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
    return insufficient('没有收到平台账期与在途资金核对表正文（text）—— 请把「所属期间 / 平台 / 结算批次 / 账期天数 / 期初在途 / 本期发生额 / 本期结算金额 / 期末在途 / 结算金额 / 平台扣费 / 冻结金额 / 净结算额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `平台账期与在途资金核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何平台结算明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkNetSettlement(it));
    findings.push(...checkInTransitRolling(it));
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

  let netTotal = 0;
  let inTransitEndTotal = 0;
  for (const it of t.items) {
    const n = normNumber(it.netSettlement);
    if (n !== null) netTotal += n;
    const e = normNumber(it.inTransitEnd);
    if (e !== null) inTransitEndTotal += e;
  }

  const result = {
    status: 'success',
    service_type: 'PLATFORM_SETTLEMENT_AGING_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      net_settlement_total: round2(netTotal),
      in_transit_end_total: round2(inTransitEndTotal),
      aging_limit_days: AGING_LIMIT_DAYS,
      frozen_ratio_reference: [FROZEN_RATIO_MIN, FROZEN_RATIO_MAX],
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
    disclaimer: '只核"结算金额 − 平台扣费 − 冻结金额 = 净结算额"与"期初在途 + 本期发生额 − 本期结算金额 = 期末在途"'
      + '这类**表内勾稽**与档位提示，**不判断各平台该按什么账期结算、平台扣费该含哪些费用、冻结金额该不该本期扣减**'
      + '（以平台结算规则与会计师口径为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
