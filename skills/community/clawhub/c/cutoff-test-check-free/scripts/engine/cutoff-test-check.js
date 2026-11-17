/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * cutoff-test-check.js —— 收入与成本截止性核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**做收入与成本截止性测试的公司**，在**每月结账、
 * 年审抽凭与出报告之前**。会计与审计要把期间最后几天的发货单 / 销售发票 / 入库单
 * 逐张核到「业务日期属于哪一期、记在哪一期、期后有没有退回或调整」这几列上 ——
 * 截止性错一张单，本期与下期两张报表就都错，而错不错**完全能用日期和算术复算出来**。
 *
 * 核心可算关系（都能手算复现）：
 *   记账期间   = 业务日期所属期间（不相等即跨期，属截止性错误）
 *   业务日期   ≤ 记账期间末日（不能先记账后发生）
 *   合计行各列 = 明细行逐列相加（单据金额 / 期后事项金额）
 *   同一单据号只应出现一次（重复即可能重复计入）
 *
 * 免费档执行 7 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**某笔交易实质上属于哪一期（收入确认条件、控制权是否转移属于会计判断），
 *    也不核对发票与单据的真伪，只核你填的日期、金额与期间归属之间的算术关系。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不写任何文件**。
 */

/* ⛔ 顺序即优先级：**更具体的词必须排在更宽泛的词前面**。
   `记账期间` 与 `业务日期` 都带"期间/日期"字样；`期后事项金额` 与 `金额` 也会互抢。 */
const ROLES = {
  docNo: ['单据号', '单号', '凭证号'],
  docType: ['单据类型', '单据种类', '业务类型'],
  bizDate: ['业务日期', '发生日期', '交易日期'],
  period: ['记账期间', '所属期间', '入账期间'],
  /* ⛔ `期后事项金额` 必须排在 `金额` 前面：否则它会被宽泛的 `金额` 抢走，
     而 `单据金额` 那一列又会被它**覆盖** ⇒ 金额列读到 0（实测踩到，样例直接报"金额为零"）。 */
  afterAmount: ['期后事项金额', '期后退回金额', '期后调整金额'],
  amount: ['单据金额', '交易金额', '金额'],
  note: ['处理说明', '备注', '说明'],
};

const LABELS = {
  docNo: '单据号', docType: '单据类型', bizDate: '业务日期', period: '记账期间',
  amount: '单据金额', afterAmount: '期后事项金额', note: '处理说明',
};

const REQUIRED = ['docType', 'bizDate', 'period', 'amount'];
const SUM_ROLES = ['amount', 'afterAmount'];
const DOC_TYPES = ['发货单', '销售发票', '发票', '入库单', '出库单', '退货单', 'red', '红冲'];
const TOTAL_WORDS = /^(合计|总计|小计|合计数?)$/;
const TOL = 0.01;
/* ⚠️ 付费开关**只声明一次**（形态 B，且必须是 `Boolean(...)` 这一种写法）：
   `strip_free_engine` 按「`const paid` + `Boolean(`」这一行识别并摘掉付费语句；
   写成别的形式（例：数组的 `.some()`）会**留下开关不删** ⇒ 泄漏守卫报"免费引擎里仍留着付费开关"。
   ⛔ 注释里也**不要**写出那一行的字面量：`strip` 的残渣断言是**纯字符串包含**判断，
      写了字面量就会被当成"没删干净"而整包跳过（本轮实测踩到）。
   两个形态（MARKER + 开关）同时出现会把免费检查也整块删掉（第 236 轮踩过）。 */

const CHECKS_GIVEN = [
  '合计行逐列复核（单据金额 / 期后事项金额）',
  '同一单据号重复行检测',
  '记账期间 = 业务日期所属期间（跨期即截止性错误）',
  '业务日期不得晚于记账期间末日（先记账后发生）',
  '单据金额为零检测',
  '单据类型不在常见口径提示（发货单/发票/入库单/出库单/退货单）',
  '空白与占位符检测（含必需列缺失）',
];

const CHECKS_WITHHELD = [
  '跨期超过 30 天（跨两个及以上期间）检测',
  '期后事项金额超过原单据金额检测',
  '期末最后 3 天的单据未填写处理说明提示（截止性重点样本）',
  '期后事项金额为负（应作为红冲处理）提示',
  '跨期单据数量占比超过 20% 提示（整体期间归属可信度下降）',
];

const OUT_OF_SCOPE = [
  '判断某笔交易**实质上**属于哪一期（是否满足收入确认条件、控制权是否转移属于会计判断）',
  '代替审计抽凭程序，也不出具审计或鉴证意见',
  '核对发票、发货单、入库单的**真伪**，或与业务系统的逐行明细比对',
  '读取 ERP / 开票系统 / 仓储系统的导出文件（需要你先导出成文本贴进来）',
  '判断跨期事项对所得税的影响（属于税务判断）',
];

const SAMPLE_TEXT = [
  '单据号\t单据类型\t业务日期\t记账期间\t单据金额\t期后事项金额\t处理说明',
  'FH-20260128-001\t发货单\t2026-01-28\t2026-01\t120000.00\t0.00\t已核对发货与签收',
  'FP-20260131-007\t销售发票\t2026-01-31\t2026-01\t86000.00\t12000.00\t期后退回 12000，已冲减二月收入',
  'RK-20260130-003\t入库单\t2026-01-30\t2026-01\t54000.00\t0.00\t已核对入库单与验收单',
  '合计\t\t\t\t260000.00\t12000.00\t',
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

const round2 = (n) => Math.round(n * 100) / 100;
const who = (it) => { const d = String(it.docNo || '').trim(); return d ? `${d}（${String(it.docType || '').trim() || '未注明类型'}）` : `第 ${it.line} 行`; };

function parseTable(text) {
  const lines = String(text).split(/\r?\n/).map((l) => l.trim()).filter((l) => l !== '');
  if (!lines.length) return { items: [], totals: {}, missingColumns: [], header: [] };
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
  return { items, totals, missingColumns, header };
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
        message: `合计行「${LABELS[role]}」填 ${stated}，但明细逐行相加是 ${sum}`,
        evidence: `合计=${stated}；明细合计=${sum}（${n} 行）`,
      });
    }
  }
  return out;
}

function checkDuplicate(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.docNo || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        line: it.line, level: 'P1', category: '重复行',
        message: `${who(it)} 与第 ${seen.get(key)} 行的「单据号」完全相同 —— 可能重复计入`,
        evidence: `单据号=${it.docNo}；与第 ${seen.get(key)} 行重复`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkPeriodVsBizDate(it) {
  const biz = String(it.bizDate || '').trim();
  const per = String(it.period || '').trim();
  const m = biz.match(/^(\d{4})[-/年](\d{1,2})/);
  const p = per.match(/^(\d{4})[-/年]?(\d{1,2})?/);
  if (!m || !p) return null;
  const bizPeriod = `${m[1]}-${String(m[2]).padStart(2, '0')}`;
  const perPeriod = p[2] ? `${p[1]}-${String(p[2]).padStart(2, '0')}` : p[1];
  if (bizPeriod !== perPeriod) {
    return {
      line: it.line, level: 'P0', category: '记账期间与业务日期跨期',
      message: `${who(it)} 业务日期 ${biz}（属 ${bizPeriod}）却记在 ${per}`,
      evidence: `业务日期=${biz}；业务日期所属期间=${bizPeriod}；记账期间=${per}`,
    };
  }
  return null;
}

function checkBizDateAfterPeriodEnd(it) {
  const biz = String(it.bizDate || '').trim();
  const per = String(it.period || '').trim();
  const m = biz.match(/^(\d{4})[-/年](\d{1,2})[-/月](\d{1,2})/);
  const p = per.match(/^(\d{4})[-/年]?(\d{1,2})/);
  if (!m || !p || !p[2]) return null;
  const y = Number(p[1]);
  const mo = Number(p[2]);
  const lastDay = new Date(Date.UTC(y, mo, 0)).getUTCDate();
  const perEnd = `${p[1]}-${String(mo).padStart(2, '0')}-${String(lastDay).padStart(2, '0')}`;
  const bizNorm = `${m[1]}-${String(m[2]).padStart(2, '0')}-${String(m[3]).padStart(2, '0')}`;
  if (bizNorm > perEnd) {
    return {
      line: it.line, level: 'P0', category: '业务日期晚于记账期间末日',
      message: `${who(it)} 业务日期 ${bizNorm} 晚于记账期间末日 ${perEnd}（先记账后发生）`,
      evidence: `业务日期=${bizNorm}；记账期间=${per}；期间末日=${perEnd}`,
    };
  }
  return null;
}

function checkZeroAmount(it) {
  const amt = normNumber(it.amount);
  if (amt === null || amt !== 0) return null;
  return {
    line: it.line, level: 'P1', category: '单据金额为零',
    message: `${who(it)} 单据金额为 0 —— 无法核截止性`,
    evidence: `单据金额=${amt}`,
  };
}

function checkDocType(it) {
  const t = String(it.docType || '').trim();
  if (!t || isBlank(t)) return null;
  if (!DOC_TYPES.some((k) => t.indexOf(k) >= 0)) {
    return {
      line: it.line, level: 'P2', category: '单据类型口径待核对',
      message: `${who(it)} 单据类型填的是「${t}」（常见：发货单 / 销售发票 / 入库单 / 出库单 / 退货单）`,
      evidence: `单据类型=${t}`,
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
      evidence: `表头=${header.join('|')}`,
    });
  }
  for (const it of items) {
    for (const role of REQUIRED) {
      if (missingColumns.indexOf(role) >= 0) continue;
      if (isBlank(it[role])) {
        out.push({
          line: it.line, level: 'P1', category: '空白或占位符',
          message: `${who(it)} 的「${LABELS[role]}」是空白或占位符 —— 这一行无法核对`,
          evidence: `${LABELS[role]}=${it[role] === undefined ? '(空)' : it[role]}`,
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
  if (text.trim() === '') return insufficient(['材料文本为空：请把截止性测试单据清单（含表头）贴进来']);

  const { items, totals, missingColumns, header } = parseTable(text);
  if (!items.length) {
    return insufficient(['认不出任何数据行：第一行必须是表头，且至少有一行明细（合计行可留）']);
  }

  const findings = [];
  for (const f of checkTotalRow(items, totals)) findings.push(f);
  for (const it of items) {
    const one = [checkPeriodVsBizDate(it), checkBizDateAfterPeriodEnd(it), checkZeroAmount(it), checkDocType(it)];
    for (const f of one) if (f) findings.push(f);
  }
  for (const f of checkDuplicate(items)) findings.push(f);
  for (const f of checkDuplicate(items)) findings.push(f);
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
        p0, p1, p2,
        verdict: findings.length === 0 ? 'NO_ISSUE_FOUND' : (p0 > 0 ? 'P0_ISSUES' : 'ISSUES'),
        omitted: 0,
      },
      scope: {
        checks: checkList,
        checks_not_run: notRun,
        rows: items.length,
        amount_total: round2(items.reduce((n, it) => n + (normNumber(it.amount) || 0), 0)),
        after_total: round2(items.reduce((n, it) => n + (normNumber(it.afterAmount) || 0), 0)),
        tolerance: TOL,
        executed_locally: true,
        network_used: false,
      },
    },
  };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, DOC_TYPES,
};
