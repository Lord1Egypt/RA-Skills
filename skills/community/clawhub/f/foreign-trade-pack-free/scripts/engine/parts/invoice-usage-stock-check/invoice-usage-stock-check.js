/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * invoice-usage-stock-check.js —— 发票领用存与开票数据核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月（尤其季末年末）**，财务要对发票的领、用、存做一次盘账 ——
 * 发票是**税务直接监管的实物凭证**：份数对不上、有丢失、作废率异常，
 * 都要在申报或税务检查时说得清。这是每个月都要做、且**完全能算出来对错**的活。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   期末库存 = 期初库存 + 领用 − 开出 − 作废 − 红冲
 *   本月期初 = 上月期末（跨月衔接）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 */

const CHECKS_GIVEN = [
  '库存勾稽（期初 + 领用 − 开出 − 作废 − 红冲 = 期末）',
  '期末库存为负检测',
  '开出与作废合计超过可用份数检测',
  '合计行逐列复核',
  '重复月份检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '跨月衔接检测（本月期初 = 上月期末）',
  '作废率异常检测（作废 ÷ 开出 > 5%）',
  '红冲率异常检测（红冲 ÷ 开出 > 3%）',
  '份数非整数检测（发票份数必须是整数）',
  '无领用却开出检测（本月未领用但开出了发票）',
];

const OUT_OF_SCOPE = [
  '核对开票金额与收入、税额是否一致（请用「增值税申报与账载开票三方核对」）',
  '判断作废或红冲的税务合规性（那属于税务判断）',
  '处理电子发票额度、数电票授信额度（本表只核纸质/电子发票的份数台账）',
  '读取开票系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '月份\t期初库存份数\t领用份数\t开出份数\t作废份数\t红冲份数\t期末库存份数',
  '2026-01\t50\t100\t120\t2\t1\t27',
  '2026-02\t27\t100\t110\t1\t0\t16',
  '2026-03\t16\t150\t140\t3\t1\t22',
  '合计\t\t350\t370\t6\t2\t',
].join('\n');

const TOL = 0.01;
const VOID_RATE_CAP = 0.05;      // 作废率 5%
const REVERSE_RATE_CAP = 0.03;   // 红冲率 3%

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  month: ['月份', '所属期', '期间', '月度'],
  opening: ['期初库存份数', '期初库存', '期初份数', '期初'],
  received: ['领用份数', '领用数量', '领用'],
  issued: ['开出份数', '开具份数', '开票份数', '开出'],
  voided: ['作废份数', '作废数量', '作废'],
  reversed: ['红冲份数', '红冲数量', '冲红份数', '红冲'],
  closing: ['期末库存份数', '期末库存', '期末份数', '期末'],
};

const LABELS = {
  month: '月份', opening: '期初库存份数', received: '领用份数', issued: '开出份数',
  voided: '作废份数', reversed: '红冲份数', closing: '期末库存份数',
};

const REQUIRED = ['month', 'opening', 'received', 'issued', 'voided', 'reversed', 'closing'];
const SUM_ROLES = ['received', 'issued', 'voided', 'reversed'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计)$/;

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
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '');
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
      if (role === 'month' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => (it && it.month ? `${String(it.month).trim()} 期` : `第 ${it && it.line} 行`);

/* ================================ 免费档检查项 ================================ */

function checkStockIdentity(it) {
  const open = normNumber(it.opening);
  const recv = normNumber(it.received);
  const iss = normNumber(it.issued);
  const vo = normNumber(it.voided);
  const rev = normNumber(it.reversed);
  const close = normNumber(it.closing);
  if ([open, recv, iss, vo, rev, close].some((v) => v === null)) return null;
  const expect = round2(open + recv - iss - vo - rev);
  if (Math.abs(expect - close) <= TOL) return null;
  return {
    level: 'P0', category: '库存勾稽不符', line: it.line,
    message: `${who(it)}：期初 ${open} + 领用 ${recv} − 开出 ${iss} − 作废 ${vo} − 红冲 ${rev} 应为 ${expect}，台账写的是 ${close}，相差 ${round2(close - expect)} 份。`,
  };
}

function checkNegativeClosing(it) {
  const close = normNumber(it.closing);
  if (close === null || close >= -TOL) return null;
  return {
    level: 'P0', category: '期末库存为负', line: it.line,
    message: `${who(it)}的期末库存是 ${close} 份（负数）—— 发票份数不可能为负，说明台账或领用记录有缺漏。`,
  };
}

function checkOveruse(it) {
  const open = normNumber(it.opening);
  const recv = normNumber(it.received);
  const iss = normNumber(it.issued);
  const vo = normNumber(it.voided);
  const rev = normNumber(it.reversed);
  if ([open, recv, iss, vo, rev].some((v) => v === null)) return null;
  const used = iss + vo + rev;
  const available = open + recv;
  if (used <= available + TOL) return null;
  return {
    level: 'P0', category: '开出与作废超过可用份数', line: it.line,
    message: `${who(it)}开出+作废+红冲共 ${used} 份，但可用（期初 ${open} + 领用 ${recv}）只有 ${available} 份，超出 ${round2(used - available)} 份。`,
  };
}

function checkTotalRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return out;
  let sum = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) sum += v;
  }
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  out.push({
    level: 'P0', category: '合计行与明细之和不符', line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${stated}，各期相加是 ${sum}，相差 ${round2(stated - sum)} 份。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = String(it.month || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一月份出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 至少有一行是多余的。`,
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

/* ============================ 完整档（付费）检查项 ============================ */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到台账正文（text）—— 请把「月份 / 期初 / 领用 / 开出 / 作废 / 红冲 / 期末」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `台账表头缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何月份明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkStockIdentity(it); if (a) findings.push(a);
    const b = checkNegativeClosing(it); if (b) findings.push(b);
    const c = checkOveruse(it); if (c) findings.push(c);

  }

  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let issuedTotal = 0; let voidedTotal = 0; let reversedTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.issued); if (a !== null) issuedTotal += a;
    const b = normNumber(it.voided); if (b !== null) voidedTotal += b;
    const c = normNumber(it.reversed); if (c !== null) reversedTotal += c;
  }

  const result = {
    status: 'success',
    service_type: 'INVOICE_USAGE_STOCK_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      periods: t.items.length,
      issued_total: round2(issuedTotal),
      voided_total: round2(voidedTotal),
      reversed_total: round2(reversedTotal),
      void_rate: issuedTotal > 0 ? Number((voidedTotal / issuedTotal).toFixed(6)) : null,
      reverse_rate: issuedTotal > 0 ? Number((reversedTotal / issuedTotal).toFixed(6)) : null,
      void_rate_cap: VOID_RATE_CAP,
      reverse_rate_cap: REVERSE_RATE_CAP,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      periods: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核发票领用存台账的内部勾稽与常见比例，不判断作废/红冲的税务合规性；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
