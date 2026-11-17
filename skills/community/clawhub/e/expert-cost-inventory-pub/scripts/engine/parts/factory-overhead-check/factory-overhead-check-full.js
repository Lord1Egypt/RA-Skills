'use strict';
/**
 * factory-overhead-check-full.js —— 制造费用分摊与吸收核对（本包 / 订阅版共用源码）
 *
 * 谁在什么时候必须做这件事：**每月结账与成本核算时**，制造企业要把本期归集的
 * **制造费用**（折旧、水电、维修、机物料、车间管理人员薪酬等）按**分摊基数**（工时 / 机时 / 产量）
 * 分摊到车间、产品与工序上。分摊率一错，产品成本、存货计价与毛利全部跟着错；
 * 而"分摊出去多少 + 还留多少没分摊"又必须与本期**费用总额**勾稽得上 ——
 * 分摊出去的比例就是**吸收率**：少吸收 = 费用没摊完，多吸收 = 摊得比本期发生的还多。
 * 全是算术，完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），不读写任何文件，不读环境变量。
 *
 * 契约（所有引擎一致，别改名字）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *   parseTable / roleOf / normNumber / round2 / isBlank / splitRow
 *   CHECKS_GIVEN / CHECKS_WITHHELD / OUT_OF_SCOPE / SAMPLE_TEXT / LABELS / SUM_ROLES
 *
 * 核心可算关系（都能手算复现）：
 *   分摊率      = 分摊金额 ÷ 分摊基数
 *   分摊金额    = 分摊基数 × 分摊率
 *   分摊合计    = 费用总额 − 未分摊金额（吸收差异 = 费用总额 − 分摊合计 = 未分摊金额）
 *   吸收率(%)   = 分摊合计 ÷ 费用总额 × 100
 *
 * 本包执行 6 项；订阅版追加 3 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**分摊率该定多少、不拿任何"标准费率"当标准：费率与基数口径以表里给的为准，
 *    只对表内自相矛盾的地方下结论，结论可由第三方用同一份输入复算。
 * ⚠️ 订阅版的实现集中在**买断包里**那条「订阅版才执行的检查」分隔线与 run 之间的一段；
 *    免费包里的同名引擎**不含这一段**（由 tools/strip_free_engine.py 机械摘除；
 *    改了这里的付费实现，必须重新生成免费包的那份，别手改）。
 */

const CHECKS_GIVEN = [
  '分摊率复算（分摊金额 ÷ 分摊基数 = 分摊率）',
  '分摊金额逐行复算（分摊基数 × 分摊率 = 分摊金额）',
  '分摊合计勾稽（费用总额 − 未分摊金额 = 分摊合计）',
  '吸收率复算与吸收差异（分摊合计 ÷ 费用总额 = 吸收率）',
  '同一期间同车间同费用项目重复行检测',
  '关键字段缺失或占位符检测',
];

const CHECKS_WITHHELD = [
  '跨车间 / 跨期间汇总台账（同一期间的费用总额、未分摊金额、分摊合计在各车间行之间不一致；合计行与明细加总不符）',
  '吸收差异超阈值处理清单（按差异金额排序：|费用总额 − 分摊合计| ÷ 费用总额 超过 10%）',
  '差异归因 · 产量 / 效率 / 价格三因素（需要表里给「预算产量、实际产量、单位标准工时、预算分摊率」四列）',
];

const OUT_OF_SCOPE = [
  '判断分摊率该定多少（工时 / 机时口径、制造费用归集范围、车间划分，以本单位的成本核算办法为准）',
  '判断分摊基数本身是否真实（工时统计、机器运转记录、抄表数据、产量记录）',
  '判断某笔支出该不该计入制造费用（费用性质划分、资本化与费用化、制造费用与期间费用的界线）',
  '核对在产品 / 完工产品的约当产量与成本结转（那是成本分配表的范围，不是分摊表）',
  '合计行的逐列加总（免费档只核「费用总额 − 未分摊金额 = 分摊合计」这一条勾稽；完整档的汇总台账才核合计行）',
  '读取 ERP / Excel 原文件或考勤机导出（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '期间\t车间\t费用项目\t分摊基数\t分摊率\t分摊金额\t费用总额\t未分摊金额\t分摊合计\t吸收率',
  '2026-01\t一车间\t折旧费\t800.00\t12.50\t10000.00\t48000.00\t2000.00\t46000.00\t95.83',
  '2026-01\t一车间\t水电费\t600.00\t10.00\t6000.00\t48000.00\t2000.00\t46000.00\t95.83',
  '2026-01\t二车间\t折旧费\t1000.00\t12.00\t12000.00\t48000.00\t2000.00\t46000.00\t95.83',
  '2026-01\t二车间\t水电费\t900.00\t10.00\t9000.00\t48000.00\t2000.00\t46000.00\t95.83',
  '2026-01\t二车间\t维修费\t900.00\t10.00\t9000.00\t48000.00\t2000.00\t46000.00\t95.83',
  '2026-02\t一车间\t折旧费\t1200.00\t12.50\t15000.00\t52000.00\t4000.00\t48000.00\t92.31',
  '2026-02\t一车间\t水电费\t600.00\t10.00\t6000.00\t52000.00\t4000.00\t48000.00\t92.31',
  '2026-02\t二车间\t折旧费\t1000.00\t12.00\t12000.00\t52000.00\t4000.00\t48000.00\t92.31',
  '2026-02\t二车间\t水电费\t900.00\t10.00\t9000.00\t52000.00\t4000.00\t48000.00\t92.31',
  '2026-02\t二车间\t维修费\t600.00\t10.00\t6000.00\t52000.00\t4000.00\t48000.00\t92.31',
].join('\n');

const TOL = 0.01;
/* 「吸收率」在 1.5 以内视为小数比率（0.9583 ⇒ 95.83%），这是表里两种常见填法的唯一区别 */
const RATIO_LIMIT = 1.5;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的前面（第 232 轮 header_map_check 的由来）
  //    否则「预算分摊基数」会被「分摊基数」抢走、「未分摊金额」会被「分摊金额」抢走。
  allocTotal: ['分摊合计', '已分摊合计', '分摊总额', '分摊总计'],
  unallocated: ['未分摊金额', '未分摊额', '未分摊费用', '未分摊'],
  allocated: ['分摊金额', '分摊额', '已分摊金额', '计入产品成本'],
  unitStdHours: ['单位标准工时', '标准单位工时', '单位产品工时', '单位工时'],
  stdBase: ['标准分摊基数', '预算分摊基数', '标准工时基数', '预算工时'],
  stdRate: ['标准分摊率', '预算分摊率', '标准费率', '预算费率'],
  rate: ['分摊率', '分配率', '分摊费率', '费率'],
  base: ['分摊基数', '分配基数', '分摊标准', '机器工时', '机时', '工时'],
  absorb: ['吸收率', '吸收比率', '吸收比例'],
  totalCost: ['费用总额', '制造费用总额', '归集费用', '归集额', '费用合计'],
  budgetOutput: ['预算产量', '计划产量', '预算数量'],
  actualOutput: ['实际产量', '本期产量', '实际数量'],
  period: ['期间', '月份', '所属期', '会计期间'],
  workshop: ['车间', '部门', '成本中心', '分厂', '工段'],
  expItem: ['费用项目', '费用名称', '明细项目', '项目名称'],
};

const LABELS = {
  period: '期间', workshop: '车间', expItem: '费用项目', base: '分摊基数', rate: '分摊率',
  allocated: '分摊金额', totalCost: '费用总额', unallocated: '未分摊金额',
  allocTotal: '分摊合计', absorb: '吸收率',
  budgetOutput: '预算产量', actualOutput: '实际产量', unitStdHours: '单位标准工时', stdRate: '预算分摊率',
};

const REQUIRED = ['period', 'workshop', 'expItem', 'base', 'rate', 'allocated',
                  'totalCost', 'unallocated', 'allocTotal', 'absorb'];
/* 可以逐行相加的角色（合计行 = 各明细行相加） */
const SUM_ROLES = ['base', 'allocated'];
/* 期间级口径列：同一期间内各行重复填写同一个数，合计时必须**按期间去重**再相加 */
const PERIOD_ROLES = ['totalCost', 'unallocated', 'allocTotal', 'absorb'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|本期合计|合计[:：])$/;

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

/** 表头 → 角色。关键词按 ROLES 的声明顺序匹配，先命中的角色赢（更具体的别名必须排在前面）。 */
function roleOf(header) {
  const h = String(header).replace(/[\s（）()：:]/g, '');
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

function normNumber(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[¥￥$,，\s]/g, '');
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '').replace(/%$/, '');
  if (!/^-?\d+(\.\d+)?$/.test(t)) return null;
  const n = Number(t);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;
const fmt = (n) => (n === null || n === undefined ? '(空)' : Number(n).toFixed(2));

/** 吸收率统一换算成百分数：≤1.5 视为小数比率（0.9583 ⇒ 95.83） */
function absorbPct(raw) {
  const v = normNumber(raw);
  if (v === null) return null;
  return Math.abs(v) <= RATIO_LIMIT ? round2(v * 100) : v;
}

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null, header: [], cols: [] };
  const header = splitRow(raw[0]);
  const cols = header.map((h) => ({ header: h, role: roleOf(h) }));
  const roles = cols.map((c) => c.role);
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
      if ((role === 'period' || role === 'expItem') && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; } else items.push(row);
  }
  return { items, totals, missingColumns, header, cols };
}

const where = (it) => {
  const bits = [it.period, it.workshop, it.expItem]
    .map((x) => String(x === undefined ? '' : x).trim()).filter((x) => x !== '');
  return bits.length ? bits.join(' / ') : `第 ${it.line} 行`;
};
const lineOf = (it) => `第 ${it.line} 行`;

/* ================================ 本包检查项 ================================ */

/** ① 分摊率复算：分摊率 = 分摊金额 ÷ 分摊基数 */
function checkRateRecompute(it) {
  const base = normNumber(it.base);
  const amount = normNumber(it.allocated);
  const rate = normNumber(it.rate);
  if (base === null || amount === null || rate === null) return null;
  if (Math.abs(base) <= TOL) return null;              // 基数为 0 时"÷ 基数"没有意义，不下结论
  const expect = round2(amount / base);
  if (Math.abs(expect - rate) <= 0.01) return null;
  return {
    level: 'P0', category: '分摊率复算不符', line: it.line,
    message: `${where(it)}（${lineOf(it)}）：分摊金额 ${fmt(amount)} ÷ 分摊基数 ${fmt(base)} = 应为 `
      + `${expect.toFixed(2)}，表里分摊率是 ${fmt(rate)}，相差 ${fmt(round2(rate - expect))}。`,
  };
}

/** ② 分摊金额逐行复算：分摊金额 = 分摊基数 × 分摊率 */
function checkAmountRecompute(it) {
  const base = normNumber(it.base);
  const rate = normNumber(it.rate);
  const amount = normNumber(it.allocated);
  if (base === null || rate === null || amount === null) return null;
  const expect = round2(base * rate);
  if (Math.abs(expect - amount) <= TOL) return null;
  return {
    level: 'P0', category: '分摊金额逐行复算不符', line: it.line,
    message: `${where(it)}（${lineOf(it)}）：分摊基数 ${fmt(base)} × 分摊率 ${fmt(rate)} 应为 `
      + `${fmt(expect)}，表里分摊金额是 ${fmt(amount)}，相差 ${fmt(round2(amount - expect))}。`,
  };
}

/** ③ 分摊合计勾稽：费用总额 − 未分摊金额 = 分摊合计 */
function checkAbsorptionBridge(it) {
  const totalCost = normNumber(it.totalCost);
  const unallocated = normNumber(it.unallocated);
  const allocTotal = normNumber(it.allocTotal);
  if (totalCost === null || unallocated === null || allocTotal === null) return null;
  const expect = round2(totalCost - unallocated);
  if (Math.abs(expect - allocTotal) <= TOL) return null;
  return {
    level: 'P0', category: '分摊合计勾稽不符', line: it.line,
    message: `${where(it)}（${lineOf(it)}）：费用总额 ${fmt(totalCost)} − 未分摊金额 ${fmt(unallocated)} = `
      + `应为 ${fmt(expect)}，表里分摊合计是 ${fmt(allocTotal)}，相差 ${fmt(round2(allocTotal - expect))} —— `
      + `已分摊 + 未分摊必须正好等于本期制造费用总额。`,
  };
}

/** ④ 吸收率复算与吸收差异：吸收率 = 分摊合计 ÷ 费用总额 × 100 */
function checkAbsorbRate(it) {
  const totalCost = normNumber(it.totalCost);
  const allocTotal = normNumber(it.allocTotal);
  const shown = absorbPct(it.absorb);
  if (totalCost === null || allocTotal === null || shown === null) return null;
  if (Math.abs(totalCost) <= TOL) return null;
  const expect = round2(allocTotal / totalCost * 100);
  if (Math.abs(shown - expect) <= 0.01) return null;
  const variance = round2(totalCost - allocTotal);
  return {
    level: 'P1', category: '吸收率与分摊比例不符', line: it.line,
    message: `${where(it)}（${lineOf(it)}）：分摊合计 ${fmt(allocTotal)} ÷ 费用总额 ${fmt(totalCost)} = 应为 `
      + `${expect.toFixed(2)}%，表里吸收率是 ${fmt(shown)}%，相差 ${(round2(shown - expect)).toFixed(2)} 个百分点；`
      + `吸收差异（费用总额 − 分摊合计）是 ${fmt(variance)}。`,
  };
}

/** ⑤ 同一期间同车间同费用项目重复行 */
function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = [String(it.period === undefined ? '' : it.period).trim(),
                 String(it.workshop === undefined ? '' : it.workshop).trim(),
                 String(it.expItem === undefined ? '' : it.expItem).trim()].join('|');
    if (key === '||') continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一期间同车间同费用项目重复行', line: it.line,
        message: `${where(it)}（${lineOf(it)}）的同一期间 / 车间 / 费用项目已在第 ${seen.get(key)} 行出现过，`
          + `第 ${it.line} 行又出现一次 —— 分摊基数与分摊金额会被重复计入。`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/** ⑥ 关键字段缺失或占位符 */
function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (!isBlank(it[role])) continue;
      const s = String(it[role] === undefined ? '' : it[role]).trim();
      out.push({
        level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
        message: `${where(it)}（${lineOf(it)}）的「${LABELS[role]}」是空的或占位符（${s || '空'}）—— `
          + `这一列缺了就没法复算，请补全或删掉这一行。`,
      });
    }
  }
  return out;
}

/* ===== 以下为订阅版才执行的检查 ===== */

const ABSORB_ALERT = 0.10;     // 吸收差异占比超过 10% ⇒ 进处理清单
const ATTRIB_ALERT = 0.10;     // 单一因素占预算费用超过 10% ⇒ 报主因
const BUDGET_ROLES = ['budgetOutput', 'actualOutput', 'unitStdHours', 'stdRate'];

/** 汇总台账：按（期间 × 车间）聚合，再按期间汇总；期间级口径列取该单元首次出现的值 */
function buildLedger(items) {
  const cells = [];
  const index = new Map();
  for (const it of items) {
    const period = String(it.period === undefined ? '' : it.period).trim();
    const workshop = String(it.workshop === undefined ? '' : it.workshop).trim();
    const key = period + '\u0000' + workshop;
    let cell = index.get(key);
    if (!cell) {
      cell = { period: period, workshop: workshop, line: it.line, rows: 0, base: 0, allocated: 0 };
      for (const role of PERIOD_ROLES.concat(BUDGET_ROLES)) cell[role] = null;
      index.set(key, cell);
      cells.push(cell);
    }
    cell.rows += 1;
    for (const role of SUM_ROLES) {
      const v = normNumber(it[role]);
      if (v !== null) cell[role] += v;
    }
    for (const role of PERIOD_ROLES.concat(BUDGET_ROLES)) {
      if (cell[role] === null) cell[role] = normNumber(it[role]);
    }
  }
  const periods = [];
  const pIndex = new Map();
  for (const c of cells) {
    let st = pIndex.get(c.period);
    if (!st) {
      st = { period: c.period, line: c.line, rows: 0, base: 0, allocated: 0, workshops: [] };
      for (const role of PERIOD_ROLES.concat(BUDGET_ROLES)) st[role] = null;
      pIndex.set(c.period, st);
      periods.push(st);
    }
    st.rows += c.rows;
    st.base += c.base;
    st.allocated += c.allocated;
    st.workshops.push(c);
    for (const role of PERIOD_ROLES.concat(BUDGET_ROLES)) {
      if (st[role] === null) st[role] = c[role];
    }
  }
  for (const c of cells) { c.base = round2(c.base); c.allocated = round2(c.allocated); }
  for (const st of periods) { st.base = round2(st.base); st.allocated = round2(st.allocated); }
  return { cells: cells, periods: periods };
}

/** 付费检查 ①：跨车间 / 跨期间的汇总台账必须与明细自洽，合计行必须等于明细加总 */
function checkLedgerConsistency(led, totals) {
  const out = [];
  for (const st of led.periods) {
    // (a) 期间级口径列在同一期间的不同车间行之间必须一致
    for (const role of PERIOD_ROLES) {
      const first = st[role];
      if (first === null) continue;
      for (const c of st.workshops) {
        if (c[role] === null) continue;
        if (Math.abs(c[role] - first) <= TOL) continue;
        out.push({
          level: 'P0', category: '跨车间期间汇总台账不衔接', line: c.line,
          message: `${st.period} 期的「${LABELS[role]}」在车间之间不一致：台账取 ${fmt(first)}，`
            + `第 ${c.line} 行（${c.workshop || '未填车间'}）填的是 ${fmt(c[role])} —— `
            + `期间级口径列在同一期间内必须每一行都一样，否则汇总台账自己跟自己打架。`,
        });
      }
    }
    // (b) 各车间明细分摊金额加总 = 期间分摊合计
    if (st.allocTotal !== null && Math.abs(st.allocated - st.allocTotal) > TOL) {
      out.push({
        level: 'P0', category: '跨车间期间汇总台账不衔接', line: st.line,
        message: `${st.period} 期：各车间明细分摊金额合计 ${fmt(st.allocated)}，表里分摊合计是 `
          + `${fmt(st.allocTotal)}，相差 ${fmt(round2(st.allocated - st.allocTotal))} —— `
          + `按期间 × 车间汇总出来的台账必须与明细衔接。`,
      });
    }
    // (c) 分摊合计不能超过本期费用总额
    if (st.totalCost !== null && st.allocTotal !== null && st.allocTotal - st.totalCost > TOL) {
      out.push({
        level: 'P0', category: '跨车间期间汇总台账不衔接', line: st.line,
        message: `${st.period} 期：分摊合计 ${fmt(st.allocTotal)} 超过本期制造费用总额 `
          + `${fmt(st.totalCost)}，超出 ${fmt(round2(st.allocTotal - st.totalCost))} —— `
          + `分摊出去的钱不可能比本期归集的费用还多。`,
      });
    }
  }
  // (d) 合计行 = 明细加总（可加列直接相加；期间级口径列按期间去重后相加；吸收率按合计算）
  if (totals && totals.row) {
    for (const role of SUM_ROLES.concat(['totalCost', 'unallocated', 'allocTotal'])) {
      const stated = normNumber(totals.row[role]);
      if (stated === null) continue;
      const sum = round2(led.periods.reduce((s, st) => s + (st[role] || 0), 0));
      if (Math.abs(stated - sum) <= TOL) continue;
      out.push({
        level: 'P0', category: '跨车间期间汇总台账不衔接', line: totals.line,
        message: `合计行的「${LABELS[role]}」是 ${fmt(stated)}，各期台账相加是 ${fmt(sum)}，`
          + `相差 ${fmt(round2(stated - sum))}。`,
      });
    }
    const statedAbsorb = absorbPct(totals.row.absorb);
    if (statedAbsorb !== null) {
      const costSum = led.periods.reduce((s, st) => s + (st.totalCost || 0), 0);
      const allocSum = led.periods.reduce((s, st) => s + (st.allocTotal || 0), 0);
      if (Math.abs(costSum) > TOL) {
        const expectAbsorb = round2(allocSum / costSum * 100);
        if (Math.abs(statedAbsorb - expectAbsorb) > 0.01) {
          out.push({
            level: 'P0', category: '跨车间期间汇总台账不衔接', line: totals.line,
            message: `合计行的「吸收率」是 ${fmt(statedAbsorb)}%，按各期分摊合计 ${fmt(allocSum)} ÷ `
              + `各期费用总额 ${fmt(costSum)} 应为 ${expectAbsorb.toFixed(2)}% —— `
              + `比率列不能按行相加，必须按合计算。`,
          });
        }
      }
    }
  }
  return out;
}

/** 付费检查 ②：吸收差异超阈值（少吸收 / 多吸收），并给出按差异金额排序的处理清单 */
function checkAbsorptionAlert(led) {
  const out = [];
  for (const st of led.periods) {
    const total = st.totalCost;
    if (total === null || Math.abs(total) <= TOL) continue;
    const alloc = st.allocTotal === null ? st.allocated : st.allocTotal;
    const diff = round2(total - alloc);
    const ratio = Math.abs(diff) / Math.abs(total);
    if (ratio <= ABSORB_ALERT) continue;
    out.push({
      level: 'P0', category: '吸收差异超阈值（按差异金额排序）', line: st.line,
      message: `${st.period} 期：制造费用总额 ${fmt(total)}，已分摊 ${fmt(alloc)}`
        + `（${st.workshops.length} 个车间、${st.rows} 行明细），吸收差异 ${fmt(diff)}，占 `
        + `${(ratio * 100).toFixed(2)}%（阈值 ${(ABSORB_ALERT * 100).toFixed(0)}%）—— `
        + `${diff > 0 ? '少吸收：费用没摊完' : '多吸收：摊得比本期发生的多'}，处理顺序见 scope.action_queue。`,
    });
  }
  return out;
}

/** 付费能力：按吸收差异金额降序的处理清单 */
function buildActionQueue(led) {
  const rows = [];
  for (const st of led.periods) {
    const total = st.totalCost;
    const alloc = st.allocTotal === null ? st.allocated : st.allocTotal;
    const diff = total === null ? null : round2(total - alloc);
    const ratio = (total === null || Math.abs(total) <= TOL) ? null : Math.abs(diff) / Math.abs(total);
    const need = ratio !== null && ratio > ABSORB_ALERT;
    rows.push({
      period: st.period,
      line: st.line,
      workshops: st.workshops.length,
      detail_rows: st.rows,
      cost_total: total,
      allocated: alloc,
      variance: diff,
      variance_pct: ratio === null ? null : round2(ratio * 100),
      status: need ? (diff > 0 ? '少吸收（费用没摊完）' : '多吸收（摊得比发生的多）') : '在阈值内，无需处理',
      action: need
        ? (diff > 0
          ? `追查没摊出去的 ${fmt(diff)}：漏摊的车间 / 费用项目，或本期不该归集进来的费用`
          : `冲回多摊的 ${fmt(Math.abs(diff))}：重复分摊、分摊基数算大，或费用总额填少了`)
        : '无需处理（吸收差异在阈值内）',
    });
  }
  rows.sort((a, b) => (Math.abs(b.variance || 0) - Math.abs(a.variance || 0))
    || String(a.period).localeCompare(String(b.period)));
  return rows;
}

/** 付费能力：差异归因（产量 / 效率 / 价格三因素） */
function buildAttribution(led) {
  const rows = [];
  for (const st of led.periods) {
    const A = st.totalCost;
    const H = st.base;
    const q = st.actualOutput;
    const qb = st.budgetOutput;
    const hu = st.unitStdHours;
    const R = st.stdRate;
    if (A === null || q === null || qb === null || hu === null || R === null) continue;
    if (Math.abs(H) <= TOL) continue;
    const stdHours = round2(q * hu);
    const budget = round2(qb * hu * R);
    const outputFactor = round2((q - qb) * hu * R);
    const hoursFactor = round2((H - stdHours) * R);
    const priceFactor = round2(A - H * R);
    const totalVariance = round2(A - budget);
    const residual = round2(totalVariance - (outputFactor + hoursFactor + priceFactor));
    const factors = [
      { name: '产量因素', value: outputFactor,
        why: '(实际产量 − 预算产量) × 单位标准工时 × 预算分摊率 —— 产量变了，费用自然跟着变' },
      { name: '效率因素', value: hoursFactor,
        why: '(实际分摊基数 − 标准工时) × 预算分摊率 —— 工时 / 机时用超了或省了' },
      { name: '价格因素', value: priceFactor,
        why: '实际制造费用 − 实际分摊基数 × 预算分摊率 —— 单价 / 耗费变了（涨价、加班、外修等）' },
    ];
    const main = factors.slice().sort((a, b) => Math.abs(b.value) - Math.abs(a.value))[0];
    rows.push({
      period: st.period, line: st.line, cost_actual: A, base_actual: H, std_hours: stdHours,
      budget_cost: budget, total_variance: totalVariance, residual: residual,
      factors: factors, main: main,
    });
  }
  return rows;
}

function checkVarianceAttribution(rows) {
  const out = [];
  for (const r of rows) {
    const base = Math.abs(r.budget_cost) > TOL ? Math.abs(r.budget_cost) : Math.abs(r.cost_actual);
    const mainRatio = base > TOL ? Math.abs(r.main.value) / base : 0;
    if (Math.abs(r.residual) <= 1 && mainRatio <= ATTRIB_ALERT) continue;
    out.push({
      level: 'P1', category: '差异归因（产量/效率/价格三因素）', line: r.line,
      message: `${r.period} 期：制造费用差异 ${fmt(r.total_variance)}（实际 ${fmt(r.cost_actual)} − 预算 `
        + `${fmt(r.budget_cost)}）= 产量 ${fmt(r.factors[0].value)} + 效率 ${fmt(r.factors[1].value)} + 价格 `
        + `${fmt(r.factors[2].value)}`
        + (Math.abs(r.residual) > 1 ? `；三项相加与总差异还差 ${fmt(r.residual)}（口径不可比或被手改过）` : '')
        + `。主因是${r.main.name} ${fmt(r.main.value)}（占预算费用 ${(mainRatio * 100).toFixed(2)}%）：${r.main.why}。`,
    });
  }
  return out;
}

/* ================================== 主入口 ================================== */

function run(payload) {
  const p = payload && typeof payload === 'object' ? payload : {};
  const paid = Boolean(p && (p.full || p.credit || p.token));
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = typeof p.text === 'string' ? p.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到分摊表正文（text）—— 请把「期间 / 车间 / 费用项目 / 分摊基数 / 分摊率 / '
      + '分摊金额 / 费用总额 / 未分摊金额 / 分摊合计 / 吸收率」这张表（含表头）贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `分摊表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(String(text).split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或只有合计行），没有任何分摊明细行 —— 没有明细就没有可核对的东西');
  }

  const periodKeys = [];
  const workshopKeys = [];
  const seenPeriod = new Set();
  const seenWorkshop = new Set();
  let baseTotal = 0;
  let allocatedTotal = 0;
  for (const it of t.items) {
    const pk = String(it.period === undefined ? '' : it.period).trim();
    if (pk && !seenPeriod.has(pk)) { seenPeriod.add(pk); periodKeys.push(pk); }
    const wk = String(it.workshop === undefined ? '' : it.workshop).trim();
    if (wk && !seenWorkshop.has(wk)) { seenWorkshop.add(wk); workshopKeys.push(wk); }
    const b = normNumber(it.base);
    if (b !== null) baseTotal += b;
    const a = normNumber(it.allocated);
    if (a !== null) allocatedTotal += a;
  }

  const findings = [];
  for (const it of t.items) {
    const one = [checkRateRecompute(it), checkAmountRecompute(it), checkAbsorptionBridge(it), checkAbsorbRate(it)];
    for (const f of one) if (f) findings.push(f);
  }
  if (t.totals && t.totals.row) {
    // 合计行也要满足这条勾稽（合计行的逐列加总由订阅版的汇总台账核）
    const totalOne = [checkAbsorptionBridge(t.totals.row), checkAbsorbRate(t.totals.row)];
    for (const f of totalOne) if (f) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  let ledger = null;
  let actionQueue = [];
  let attribution = [];
  if (paid) {
    ledger = buildLedger(t.items);
    // `|| []` 是刻意的防御：某个付费检查被改动 / 停用时，这里退化成"没有结论"，
    // 而不是把整个引擎带崩 —— 结论消失必须看得见，不能变成一次崩溃。
    for (const f of (checkLedgerConsistency(ledger, t.totals) || [])) findings.push(f);
    for (const f of (checkAbsorptionAlert(ledger) || [])) findings.push(f);
    attribution = buildAttribution(ledger);
    for (const f of (checkVarianceAttribution(attribution) || [])) findings.push(f);
    actionQueue = buildActionQueue(ledger);
  }

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const scope = {
    checks: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_not_run: paid ? [] : CHECKS_WITHHELD,
    rows: t.items.length,
    periods: periodKeys.length,
    period_keys: periodKeys,
    base_total: round2(baseTotal),
    allocated_total: round2(allocatedTotal),
    tolerance: TOL,
    executed_locally: true,
    network_used: false,
  };
  if (paid) {
    scope.workshops = workshopKeys.length;
    scope.workshop_keys = workshopKeys;
    scope.ledger = ledger;
    scope.action_queue = actionQueue;
    scope.attribution = attribution;
    scope.absorb_alert = ABSORB_ALERT;
    scope.attribution_alert = ATTRIB_ALERT;
  }

  let note = `本版本只执行免费档的 ${CHECKS_GIVEN.length} 项检查：${CHECKS_GIVEN.join('、')}；`
    + '未执行的检查项见 scope.checks_not_run（只如实列出，绝不会伪造结论）。';
  if (paid) {
    note = `完整档执行全部 ${CHECKS_GIVEN.length + CHECKS_WITHHELD.length} 项检查`
      + `（免费档的 ${CHECKS_GIVEN.length} 项 + 完整档追加的 ${CHECKS_WITHHELD.length} 项）。`;
  }

  const result = {
    status: 'success',
    service_type: 'FACTORY_OVERHEAD_ALLOCATION_CHECK',
    scope: scope,
    findings: findings,
    summary: {
      rows: t.items.length,
      periods: periodKeys.length,
      workshops: workshopKeys.length,
      total: findings.length,
      p0: p0, p1: p1, p2: p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: note,
    disclaimer: '只核"分摊率 = 分摊金额 ÷ 分摊基数""分摊金额 = 分摊基数 × 分摊率"'
      + '"分摊合计 = 费用总额 − 未分摊金额""吸收率 = 分摊合计 ÷ 费用总额"这类**表内勾稽**，'
      + '**不规定分摊率与分摊基数口径**（以本单位成本核算办法、工时 / 机时记录与费用归集凭证为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
  CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
