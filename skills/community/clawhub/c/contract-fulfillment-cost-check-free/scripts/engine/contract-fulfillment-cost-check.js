/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * contract-fulfillment-cost-check.js —— 合同履约成本与收入配比核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**按履约进度确认收入的施工 / 软件 / 服务类合同**，
 * 在**每月结账、以及给审计或客户提供"收入成本配比底稿"之前**。
 * 会计要按"合同总金额 × 履约进度"滚动确认收入，并让"累计履约成本"与"合同预计总成本"
 * 保持配比；审计与券商盯的就是这几列能不能**逐行对上、整体不跑偏**。
 *
 * 核心可算关系（都能手算复现）：
 *   本期应确认收入 = 合同总金额 × 履约进度 −（累计已确认收入 − 本期确认收入）
 *   实际成本收入比 = 累计履约成本 ÷ 累计已确认收入
 *   预计成本率     = 合同预计总成本 ÷ 合同总金额
 *   累计已确认收入 ≤ 合同总金额；已开票 / 已收款 ≤ 合同总金额
 *   合计行每一列 = 明细行逐行相加
 *
 * 免费档执行 7 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**履约进度该按投入法还是产出法计量、也不判断控制权何时转移
 *   （那属于会计判断）；它只做**同一张表内部**能算出来的算术与口径核对。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不写任何文件**。
 */

/* ⛔ 顺序即优先级：**带前缀/限定语的列必须排在裸词前面**（本仓库踩过 4 次）。
   `累计已确认收入` / `本期确认收入` 都含「确认收入」，`累计履约成本` / `本期履约成本` 都含「履约成本」，
   `合同预计总成本` 含「成本」—— 宽泛的键排前面就会把具体列**抢走**：
   表现是"某一列静默不参与检查 / 两列互相覆盖"，既不报错也不缺列，极难发现。
   所以这里的顺序是：累计 → 本期 → 预计，最后才轮到裸词。 */
const ROLES = {
  contractNo: ['合同编号', '合同号', '合同ID'],
  customer: ['客户名称', '客户简称', '客户'],
  contractAmount: ['合同总金额', '合同金额', '合同总额'],
  revenueCum: ['累计已确认收入', '累计确认收入', '累计收入'],
  revenueCur: ['本期确认收入', '本期收入', '当期确认收入'],
  costCum: ['累计履约成本', '累计合同成本'],
  costCur: ['本期履约成本', '本期合同成本'],
  costTotalEst: ['合同预计总成本', '预计总成本', '预计成本'],
  progress: ['履约进度', '完工进度', '进度'],
  invoiced: ['已开票金额', '已开票', '开票金额'],
  received: ['已收款金额', '已收款', '收款金额'],
};

const LABELS = {
  contractNo: '合同编号', customer: '客户名称', contractAmount: '合同总金额',
  revenueCum: '累计已确认收入', revenueCur: '本期确认收入',
  costCum: '累计履约成本', costCur: '本期履约成本', costTotalEst: '合同预计总成本',
  progress: '履约进度', invoiced: '已开票金额', received: '已收款金额',
};

const REQUIRED = ['contractNo', 'contractAmount', 'revenueCum', 'revenueCur',
  'costCum', 'costCur', 'costTotalEst', 'progress', 'invoiced', 'received'];
const SUM_ROLES = ['contractAmount', 'revenueCum', 'revenueCur',
  'costCum', 'costCur', 'invoiced', 'received'];
const TOTAL_WORDS = /^(合计|总计|小计|合计数?)$/;

const TOL = 0.01;                 // 金额层面的绝对容差（元）
const REV_PROGRESS_REL = 0.005;   // 免费项③：收入与进度的差异超过合同总金额的 0.5% 即报
const COST_RATIO_REL = 0.10;      // 免费项⑤：成本收入比相对预计成本率偏离超过 10% 即报
const PROGRESS_REV_REL = 0.01;    // 买断项⑤：进度应确认额与累计收入差异超过 1% 即报
const RECEIPT_INVOICE_MAX = 1.10; // 买断项④：已收款 ÷ 已开票 超过 110% 即报
/* ⚠️ 付费开关只声明一次：一个布尔表达式常量 + 一个包裹付费检查的条件分支。
   免费包的引擎由本文件**机械剥离**付费分支与付费函数生成；
   注释里不要写出那个布尔表达式或条件分支的字面量，剥离工具按纯字符串判断"是否删干净"。 */

const CHECKS_GIVEN = [
  '合计行逐列复核（合同总金额 / 累计收入 / 本期收入 / 累计成本 / 本期成本 / 已开票 / 已收款）',
  '同一合同编号重复行检测',
  '本期确认收入 = 合同总金额 × 履约进度 −（累计已确认收入 − 本期确认收入）',
  '累计已确认收入不得超过合同总金额',
  '成本与收入配比（累计履约成本 ÷ 累计已确认收入 对比 合同预计总成本 ÷ 合同总金额）',
  '已收款 / 已开票 不得超过合同总金额',
  '空白与占位符检测（含必需列缺失）',
];

const CHECKS_WITHHELD = [
  '履约进度为 0 或 100% 但本期仍有确认收入 / 成本提示',
  '履约进度不在 0 ~ 100% 区间检测',
  '累计履约成本超过合同预计总成本检测',
  '已收款超过已开票 110% 提示（先收款后开票本身正常）',
  '累计已确认收入与「合同总金额 × 履约进度」差异超 1% 检测',
];

const OUT_OF_SCOPE = [
  '判断履约进度本身算得对不对（投入法 / 产出法、完工百分比如何计量属于会计判断）',
  '判断控制权何时转移、该不该确认收入（那是收入准则的判断）',
  '代替审计抽凭程序，也不出具审计或鉴证意见',
  '核对合同、发票、回款流水的**真伪**，或与 ERP / 合同系统的逐行明细比对',
  '读取 ERP / 合同系统 / 开票系统的导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '合同编号\t客户名称\t合同总金额\t累计已确认收入\t本期确认收入\t累计履约成本\t本期履约成本\t合同预计总成本\t履约进度\t已开票金额\t已收款金额',
  'HT-2026-001\t甲公司\t1000000.00\t400000.00\t100000.00\t240000.00\t60000.00\t600000.00\t40%\t400000.00\t350000.00',
  'HT-2026-002\t乙公司\t500000.00\t150000.00\t50000.00\t90000.00\t30000.00\t300000.00\t30%\t150000.00\t150000.00',
  '合计\t\t1500000.00\t550000.00\t150000.00\t330000.00\t90000.00\t900000.00\t\t550000.00\t500000.00',
].join('\n');

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
  if (raw === undefined || raw === null) return null;
  let s = String(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  let neg = false;
  if (/^\(.*\)$/.test(s)) { neg = true; s = s.slice(1, -1); }
  if (s.endsWith('%')) s = s.slice(0, -1);
  if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
  const n = Number(s);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

/** 履约进度：`40%` → 0.4；`0.4` → 0.4；裸写的 `40` 也按百分数理解 → 0.4 */
function normPercent(raw) {
  if (isBlank(raw)) return null;
  const n = normNumber(raw);
  if (n === null) return null;
  if (String(raw).trim().endsWith('%')) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
}

const round2 = (n) => Math.round(n * 100) / 100;
const fmtPct = (r) => `${(r * 100).toFixed(2)}%`;

const who = (it) => {
  const no = String(it.contractNo || '').trim();
  if (!no) return `第 ${it.line} 行`;
  const cu = String(it.customer || '').trim();
  return cu ? `合同 ${no}（${cu}）` : `合同 ${no}`;
};

function parseTable(text) {
  const lines = String(text).split(/\r?\n/).map((l) => l.trim()).filter((l) => l !== '');
  if (!lines.length) return { items: [], totals: {}, missingColumns: [], header: [], cols: [] };
  const header = splitRow(lines[0]);
  const cols = header.map((h, i) => ({ i, role: roleOf(h), raw: h }));
  const missingColumns = REQUIRED.filter((r) => !cols.some((c) => c.role === r));
  const items = [];
  const totals = {};
  for (let li = 1; li < lines.length; li += 1) {
    const cells = splitRow(lines[li]);
    const row = { line: li + 1 };
    cols.forEach((c) => { if (c.role) row[c.role] = cells[c.i] === undefined ? '' : cells[c.i]; });
    const label = (cells[0] || '').replace(/\s/g, '');
    if (TOTAL_WORDS.test(label)) { totals.line = li + 1; totals.row = row; continue; }
    items.push(row);
  }
  return { items, totals, missingColumns, header, cols };
}

/* ================================ 免费档检查项 ================================ */

function checkTotalRow(items, totals) {
  if (!totals.row) return [];
  const out = [];
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let sum = 0;
    let n = 0;
    for (const it of items) {
      const v = normNumber(it[role]);
      if (v === null) continue;
      sum += v;
      n += 1;
    }
    sum = round2(sum);
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        line: totals.line, level: 'P1', category: '合计复核',
        message: `合计行「${LABELS[role]}」填 ${stated}，但明细逐行相加是 ${sum}（相差 ${round2(stated - sum)}）`,
        evidence: `合计行=${stated}；明细逐行相加=${sum}；明细行数=${n}`,
      });
    }
  }
  return out;
}

function checkDuplicate(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.contractNo || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        line: it.line, level: 'P1', category: '合同编号重复行',
        message: `${who(it)} 与第 ${seen.get(key)} 行的「合同编号」完全相同 —— 可能重复计入`,
        evidence: `合同编号=${key}；本行=第 ${it.line} 行；首次出现=第 ${seen.get(key)} 行`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkRevenueProgress(it) {
  const amount = normNumber(it.contractAmount);
  const revCum = normNumber(it.revenueCum);
  const revCur = normNumber(it.revenueCur);
  const progress = normPercent(it.progress);
  if (amount === null || amount <= 0 || revCum === null || revCur === null || progress === null) return null;
  const shouldCur = round2(amount * progress - (revCum - revCur));
  const tol = Math.max(TOL, Math.abs(amount) * REV_PROGRESS_REL);
  if (Math.abs(shouldCur - revCur) > tol) {
    return {
      line: it.line, level: 'P0', category: '本期收入与履约进度不符',
      message: `${who(it)} 按进度应确认本期收入 ${shouldCur}，但表里填的本期确认收入是 ${revCur}`
        + `（合同总金额 ${amount} × 履约进度 ${fmtPct(progress)} = ${round2(amount * progress)}，`
        + `减去上期累计 ${round2(revCum - revCur)}）`,
      evidence: `合同总金额=${amount}；履约进度=${fmtPct(progress)}；累计已确认收入=${revCum}；`
        + `本期确认收入=${revCur}；按公式应确认本期=${shouldCur}；差异=${round2(shouldCur - revCur)}`,
    };
  }
  return null;
}

function checkRevenueOverContract(it) {
  const amount = normNumber(it.contractAmount);
  const revCum = normNumber(it.revenueCum);
  if (amount === null || revCum === null) return null;
  if (revCum - amount > TOL) {
    return {
      line: it.line, level: 'P0', category: '累计收入超过合同总金额',
      message: `${who(it)} 累计已确认收入 ${revCum} 超过合同总金额 ${amount}（超出 ${round2(revCum - amount)}）`,
      evidence: `合同总金额=${amount}；累计已确认收入=${revCum}；超出=${round2(revCum - amount)}`,
    };
  }
  return null;
}

function checkCostRevenueRatio(it) {
  const amount = normNumber(it.contractAmount);
  const revCum = normNumber(it.revenueCum);
  const costCum = normNumber(it.costCum);
  const costEst = normNumber(it.costTotalEst);
  if (amount === null || amount <= 0 || revCum === null || revCum <= 0) return null;
  if (costCum === null || costEst === null || costEst <= 0) return null;
  const actual = costCum / revCum;
  const planned = costEst / amount;
  if (planned <= 0) return null;
  const dev = Math.abs(actual - planned) / planned;
  if (dev > COST_RATIO_REL) {
    return {
      line: it.line, level: 'P1', category: '成本收入配比偏离',
      message: `${who(it)} 实际成本收入比 ${fmtPct(actual)}（累计履约成本 ${costCum} ÷ 累计已确认收入 ${revCum}）`
        + ` 相对预计成本率 ${fmtPct(planned)}（合同预计总成本 ${costEst} ÷ 合同总金额 ${amount}）`
        + ` 偏离 ${fmtPct(dev)}`,
      evidence: `累计履约成本=${costCum}；累计已确认收入=${revCum}；实际成本收入比=${fmtPct(actual)}；`
        + `合同预计总成本=${costEst}；合同总金额=${amount}；预计成本率=${fmtPct(planned)}；偏离=${fmtPct(dev)}`,
    };
  }
  return null;
}

function checkReceivedOverContract(it) {
  const amount = normNumber(it.contractAmount);
  const received = normNumber(it.received);
  if (amount === null || received === null) return null;
  if (received - amount > TOL) {
    return {
      line: it.line, level: 'P1', category: '已收款超过合同总金额',
      message: `${who(it)} 已收款金额 ${received} 超过合同总金额 ${amount}（超出 ${round2(received - amount)}）`,
      evidence: `合同总金额=${amount}；已收款金额=${received}；超出=${round2(received - amount)}`,
    };
  }
  return null;
}

function checkInvoicedOverContract(it) {
  const amount = normNumber(it.contractAmount);
  const invoiced = normNumber(it.invoiced);
  if (amount === null || invoiced === null) return null;
  if (invoiced - amount > TOL) {
    return {
      line: it.line, level: 'P1', category: '已开票超过合同总金额',
      message: `${who(it)} 已开票金额 ${invoiced} 超过合同总金额 ${amount}（超出 ${round2(invoiced - amount)}）`,
      evidence: `合同总金额=${amount}；已开票金额=${invoiced}；超出=${round2(invoiced - amount)}`,
    };
  }
  return null;
}

function checkBlanks(header, items, missingColumns) {
  const out = [];
  if (missingColumns.length) {
    out.push({
      line: 1, level: 'P1', category: '列缺失',
      message: `表头缺少必需列：${missingColumns.map((r) => LABELS[r]).join('、')}`,
      evidence: `表头=${header.join('|')}；缺少=${missingColumns.map((r) => LABELS[r]).join('、')}`,
    });
  }
  for (const it of items) {
    for (const role of REQUIRED) {
      if (missingColumns.indexOf(role) >= 0) continue;
      if (isBlank(it[role])) {
        out.push({
          line: it.line, level: 'P1', category: '空白或占位符',
          message: `${who(it)} 的「${LABELS[role]}」是空白或占位符 —— 这一行无法核对`,
          evidence: `${LABELS[role]}=${it[role] === undefined ? '(空)' : it[role]}；合同编号=${it.contractNo || '(空)'}`,
        });
      }
    }
  }
  return out;
}

/* ============================== 完整档（付费）检查项 ============================== */

/* ================================== 主流程 ================================== */

function run(payload) {
  const p = payload || {};
  const text = p.text === undefined || p.text === null ? '' : String(p.text);
  if (text.trim() === '') {
    return insufficient(['材料文本为空：请把合同履约成本与收入配比表（含表头）贴进来，Tab 分隔最稳']);
  }

  const { items, totals, missingColumns, header, cols } = parseTable(text);
  if (!cols.some((c) => c.role)) {
    return insufficient(['认不出表头：第一行必须是表头（合同编号 / 合同总金额 / 累计已确认收入 / 履约进度 …），Tab 分隔最稳']);
  }
  if (!items.length) {
    return insufficient(['认不出任何数据行：表头之下至少要有 1 行合同明细（「合计」行可以留，但不能只有它）']);
  }

  const findings = [];
  for (const f of checkTotalRow(items, totals)) findings.push(f);
  for (const f of checkDuplicate(items)) findings.push(f);
  for (const it of items) {
    const one = [
      checkRevenueProgress(it),
      checkRevenueOverContract(it),
      checkCostRevenueRatio(it),
      checkReceivedOverContract(it),
      checkInvoicedOverContract(it),
    ];
    for (const f of one) if (f) findings.push(f);
  }
  for (const f of checkBlanks(header, items, missingColumns)) findings.push(f);



  findings.sort((a, b) => (a.line - b.line) || String(a.category).localeCompare(String(b.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;
  const checkList = CHECKS_GIVEN;
  const notRun = CHECKS_WITHHELD;

  return {
    status: 'success',
    result: {
      findings,
      summary: {
        rows: items.length,
        total: findings.length,
        p0,
        p1,
        p2,
        verdict: findings.length === 0 ? 'NO_ISSUE_FOUND' : (p0 > 0 ? 'P0_ISSUES' : 'ISSUES'),
        omitted: 0,
      },
      scope: {
        checks: checkList,
        checks_not_run: notRun,
        rows: items.length,
        contract_amount_total: round2(items.reduce((n, it) => n + (normNumber(it.contractAmount) || 0), 0)),
        revenue_cum_total: round2(items.reduce((n, it) => n + (normNumber(it.revenueCum) || 0), 0)),
        tolerance: TOL,
        executed_locally: true,
        network_used: false,
      },
    },
  };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
