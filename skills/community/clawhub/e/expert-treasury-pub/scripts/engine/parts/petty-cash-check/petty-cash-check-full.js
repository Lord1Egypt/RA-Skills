'use strict';
/**
 * petty-cash-check.js —— 备用金与报销核销核对（本包 / 订阅版共用源码）
 *
 * 谁在什么时候必须做这件事：**月末结账、员工离职交接与内控自查时**，财务要把备用金/借支台账
 * 逐人逐笔核一遍 —— 员工先领用（借支）一笔钱，之后拿发票来报销冲销，剩下的要么退回、要么继续挂账。
 * 这条链算错会同时错三处：备用金余额错、费用错、其他应收款错；而**长期挂账的备用金既占资金、
 * 又是内控漏洞**（离职人员挂着几万块、跨年不冲销），审计与内控必查。完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   期末余额       = 上期余额 + 本期领用 − 本期报销核销
 *   本期报销核销   = 报销金额 − 退还款
 *   本期报销核销不得超过"上期余额 + 本期领用"（没领过的钱不能被核销掉）
 *
 * 本包执行 6 项；订阅版追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**备用金限额、核销时限与凭证要求（各单位制度不同）：
 *    天数只对"超过参考天数"做**提示**并明确标注是参考口径，不代替内控制度判断。
 */

const CHECKS_GIVEN = [
  '余额勾稽（上期余额 + 本期领用 − 本期报销核销 = 期末余额）',
  '报销核销勾稽（报销金额 − 退还款 = 本期报销核销）',
  '合计行逐列复核',
  '同一人同一笔重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '期末余额为负（超额报销）检测',
  '本期核销超过领用累计（上期余额 + 本期领用）检测',
  '挂账超过参考天数（90 天）提示（参考口径）',
  '同一人出现多笔未清余额提示',
  '报销金额为零却有核销记录提示',
];

const OUT_OF_SCOPE = [
  '判断备用金限额、核销时限与审批权限是否合规（各单位内控制度不同，请以本单位制度与主管口径为准）',
  '核实报销发票与凭证的真实性、合规性（本工具只核台账里的算术勾稽）',
  '处理跨年挂账的税务调整、离职追偿与坏账认定',
  '读取 ERP / OA / Excel 导出文件（需要你先导出成文本贴进来）',
];

/* 参考天数：仅供"挂账明显偏长"时提示，不是制度规定 */
const AGING_REF_DAYS = 90;

const SAMPLE_TEXT = [
  '姓名\t所属期\t上期余额\t本期领用\t报销金额\t退还款\t本期报销核销\t期末余额\t挂账天数',
  '张伟\t2026-01\t0.00\t5000.00\t3200.00\t200.00\t3000.00\t2000.00\t15',
  '李娜\t2026-01\t1000.00\t2000.00\t1500.00\t0.00\t1500.00\t1500.00\t40',
  '王强\t2026-02\t0.00\t800.00\t800.00\t0.00\t800.00\t0.00\t5',
  '合计\t\t1000.00\t7800.00\t5500.00\t200.00\t5300.00\t3500.00\t',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前（「本期报销核销」不能被「报销金额」抢走）
  person: ['姓名', '员工姓名', '员工', '责任人', '经办人'],
  period: ['所属期', '会计期间', '期间', '月份'],
  openBalance: ['上期余额', '期初余额', '上期未清余额', '上期结余'],
  advanced: ['本期领用', '本期借支', '领用金额', '本期拨付'],
  writeOff: ['本期报销核销', '报销核销', '本期核销', '核销金额'],
  claimAmount: ['报销金额', '报销单金额', '报销总额'],
  refund: ['退还款', '退还金额', '退回款', '退款'],
  closeBalance: ['期末余额', '期末未清余额', '备用金余额', '期末结余'],
  agingDays: ['挂账天数', '已挂账天数', '账龄天数', '挂账日数'],
};

const LABELS = {
  person: '姓名', period: '所属期', openBalance: '上期余额', advanced: '本期领用',
  claimAmount: '报销金额', refund: '退还款', writeOff: '本期报销核销',
  closeBalance: '期末余额', agingDays: '挂账天数',
};

const REQUIRED = ['person', 'period', 'openBalance', 'advanced', 'claimAmount', 'refund', 'writeOff', 'closeBalance'];
/* 空白检查只盯"结构性"字段：报销金额/退还款留空可能只是本期没有报销，
 * 那种情形由订阅版的「报销金额为零却有核销记录」负责，不在这里重复报。 */
const BLANK_ROLES = ['person', 'period', 'openBalance', 'advanced', 'writeOff', 'closeBalance'];
const SUM_ROLES = ['openBalance', 'advanced', 'claimAmount', 'refund', 'writeOff', 'closeBalance'];
const NEG_ROLES = [['openBalance', '上期余额'], ['advanced', '本期领用'], ['claimAmount', '报销金额'],
  ['refund', '退还款'], ['writeOff', '本期报销核销']];
const TOTAL_WORDS = /^(合计|总计|小计|共计|全员合计)$/;

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
      if (role === 'person' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => (it && it.person ? `${String(it.person).trim()}` : `第 ${it && it.line} 行`);

/* ================================ 本包检查项 ================================ */

function checkIdentity(it) {
  const open = normNumber(it.openBalance);
  const adv = normNumber(it.advanced);
  const off = normNumber(it.writeOff);
  const close = normNumber(it.closeBalance);
  if ([open, adv, off, close].some((v) => v === null)) return null;
  const expect = round2(open + adv - off);
  if (Math.abs(expect - close) <= TOL) return null;
  return {
    level: 'P0', category: '余额勾稽不符', line: it.line,
    message: `${who(it)}：上期余额 ${open.toFixed(2)} + 本期领用 ${adv.toFixed(2)} − 本期报销核销 ${off.toFixed(2)} 应为 ${expect.toFixed(2)}，表里期末余额写的是 ${close.toFixed(2)}，相差 ${round2(close - expect).toFixed(2)}。`,
  };
}

function checkWriteOff(it) {
  const claim = normNumber(it.claimAmount);
  const refund = normNumber(it.refund);
  const off = normNumber(it.writeOff);
  if ([claim, refund, off].some((v) => v === null)) return null;
  const expect = round2(claim - refund);
  if (Math.abs(expect - off) <= TOL) return null;
  return {
    level: 'P0', category: '报销核销勾稽不符', line: it.line,
    message: `${who(it)}：报销金额 ${claim.toFixed(2)} − 退还款 ${refund.toFixed(2)} 应为核销 ${expect.toFixed(2)}，表里本期报销核销填的是 ${off.toFixed(2)}，相差 ${round2(off - expect).toFixed(2)} —— 报销与退还是核销额的两个来源，必须相等。`,
  };
}

function checkNegativeAmount(it) {
  const out = [];
  for (const [role, label] of NEG_ROLES) {
    const v = normNumber(it[role]);
    if (v !== null && v < -TOL) {
      out.push({
        level: 'P0', category: '金额为负', line: it.line,
        message: `${who(it)}的「${label}」是 ${v.toFixed(2)}（负数）—— 冲回或红字建议单独列示，不要直接抵减本期发生额。`,
      });
    }
  }
  return out;
}

function checkTotalRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return out;
  let sum = 0;
  let n = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) { sum += v; n += 1; }
  }
  if (!n) return out;
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  out.push({
    level: 'P0', category: '合计行与明细之和不符', line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = String(it.person || '').trim();
    const d = String(it.period || '').trim();
    if (!p || !d) continue;
    const key = `${p}|${d}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一人同一笔出现重复行', line: it.line,
        message: `${who(it)}在「${d}」这一笔在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 领用与核销都会被重复计算，请合并或标明是哪一笔。`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of BLANK_ROLES) {
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

/* ============================ 订阅版检查项 ============================ */

function checkNegativeClose(it) {
  const v = normNumber(it.closeBalance);
  if (v === null || v >= -TOL) return null;
  return {
    level: 'P1', category: '期末余额为负（超额报销）', line: it.line,
    message: `${who(it)}的期末余额是 ${v.toFixed(2)}（负数）—— 备用金是"我先借给你"的钱，负数说明报销核销超过了领用累计（或退还款记反了方向），请核对。`,
  };
}

function checkOverWriteOff(it) {
  const open = normNumber(it.openBalance);
  const adv = normNumber(it.advanced);
  const off = normNumber(it.writeOff);
  if ([open, adv, off].some((v) => v === null)) return null;
  const available = round2(open + adv);
  if (off <= available + TOL) return null;
  return {
    level: 'P1', category: '本期核销超过领用累计', line: it.line,
    message: `${who(it)}本期核销 ${off.toFixed(2)}，但可用备用金只有上期余额 ${open.toFixed(2)} + 本期领用 ${adv.toFixed(2)} = ${available.toFixed(2)}，超出 ${round2(off - available).toFixed(2)} —— 没领过的钱不能被核销掉。`,
  };
}

function checkAgingOverDays(it) {
  const days = normNumber(it.agingDays);
  const close = normNumber(it.closeBalance);
  if (days === null || close === null) return null;
  if (close <= TOL) return null;
  if (days <= AGING_REF_DAYS) return null;
  return {
    level: 'P2', category: '挂账超过参考天数（参考）', line: it.line,
    message: `${who(it)}还有 ${close.toFixed(2)} 未清、已挂账 ${days.toFixed(0)} 天，超过参考天数 ${AGING_REF_DAYS} 天`
      + '（**参考口径，以本单位备用金/借支管理制度为准**）—— 长期挂账既占资金也是内控漏洞，请安排核销或退回。',
  };
}

function checkMultiOpen(items) {
  const out = [];
  const byPerson = new Map();
  for (const it of items) {
    const p = String(it.person || '').trim();
    if (!p) continue;
    const close = normNumber(it.closeBalance);
    if (close === null || close <= TOL) continue;
    if (!byPerson.has(p)) byPerson.set(p, []);
    byPerson.get(p).push({ it, close });
  }
  for (const [p, rows] of byPerson) {
    if (rows.length < 2) continue;
    let total = 0;
    for (const r of rows) total += r.close;
    const lines = rows.map((r) => r.it.line).join('、');
    out.push({
      level: 'P2', category: '同一人出现多笔未清余额', line: rows[1].it.line,
      message: `${p}有 ${rows.length} 笔未清余额（第 ${lines} 行，合计 ${round2(total).toFixed(2)}）—— 请确认是分期领用还是重复挂账，能合并的先合并。`,
    });
  }
  return out;
}

function checkZeroClaimWithWriteOff(it) {
  const claim = normNumber(it.claimAmount);
  const refund = normNumber(it.refund);
  const off = normNumber(it.writeOff);
  if (off === null || off <= TOL) return null;
  if (claim !== null && claim > TOL) return null;
  if (refund !== null && refund > TOL) return null;
  const shown = claim === null ? '空/未填' : claim.toFixed(2);
  return {
    level: 'P1', category: '报销金额为零却有核销记录', line: it.line,
    message: `${who(it)}的报销金额是 ${shown}，却有 ${off.toFixed(2)} 的报销核销记录 —— 核销额只能是"报销金额 − 退还款"，请补上报销金额或核对这笔核销的来源。`,
  };
}

/* ================================== 主入口 ================================== */

function run(payload) {
  const paid = Boolean(payload && (payload.full || payload.credit || payload.token));
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到台账正文（text）—— 请把「姓名 / 所属期 / 上期余额 / 本期领用 / 报销金额 / 退还款 / 本期报销核销 / 期末余额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `台账缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何人任何一笔明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkIdentity(it); if (a) findings.push(a);
    const b = checkWriteOff(it); if (b) findings.push(b);
    for (const x of checkNegativeAmount(it)) findings.push(x);
    if (paid) {
      const d = checkNegativeClose(it); if (d) findings.push(d);
      const e = checkOverWriteOff(it); if (e) findings.push(e);
      const f = checkAgingOverDays(it); if (f) findings.push(f);
      const g = checkZeroClaimWithWriteOff(it); if (g) findings.push(g);
    }
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);
  if (paid) {
    for (const f of checkMultiOpen(t.items)) findings.push(f);
  }

  const notRun = [];
  if (!paid) notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const periods = [];
  for (const it of t.items) {
    const d = String(it.period === undefined ? '' : it.period).trim();
    if (d && periods.indexOf(d) < 0) periods.push(d);
  }

  const result = {
    status: 'success',
    service_type: 'PETTY_CASH_CHECK',
    scope: {
      checks: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.length,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periods.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: paid ? '完整档执行全部检查项。' : `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"上期余额 + 本期领用 − 本期报销核销 = 期末余额""报销金额 − 退还款 = 本期报销核销"这类内部勾稽，'
      + '**不规定备用金限额、核销时限与凭证要求**（以本单位制度为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
