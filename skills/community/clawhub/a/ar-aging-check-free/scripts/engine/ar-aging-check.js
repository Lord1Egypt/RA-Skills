#!/usr/bin/env node
/**
 * ar-aging-check.js —— 应收账款账龄核对引擎（确定性、纯 Node 标准库）。
 *
 * 为什么做这个：
 *   **每月结账、以及每次做回款预测和催收清单时**，财务都要拿应收账龄表核一遍：
 *   逐客户的「期初 + 本期应收 − 本期收款 = 期末」对不对、
 *   「各账龄分档金额之和 = 期末余额」对不对、合计行是不是各客户之和、
 *   有没有重复客户、有没有该填没填。这些**全是算术**。
 *   账龄算错的直接后果是**坏账准备提错、催收漏掉大额逾期**。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约（与其它引擎一致）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *
 * 刻意不做的事：不联网、不调用大模型；材料不足不给结论；不判断客户信用或该不该计提坏账。
 */
'use strict';

const CHECKS_GIVEN = [
  '逐客户余额勾稽（期初余额 + 本期应收 − 本期收款 = 期末余额）',
  '逐客户账龄勾稽（0-30 + 31-60 + 61-90 + 90天以上 = 期末余额）',
  '合计行复核（每一列的合计是否等于各客户之和）',
  '重复客户检测（同一客户出现两行）',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '贷方余额提示（期末余额为负，通常是预收或多收）',
  '超收检测（本期收款 > 期初余额 + 本期应收）',
  '长期挂账占比（90 天以上占期末余额的比例，默认阈值 30%）',
  '分档与余额符号矛盾（期末为负但仍有账龄分档金额）',
];

const OUT_OF_SCOPE = [
  '判断某个客户该不该计提坏账、计提多少（那是会计政策与准则的事）',
  '判断账龄分档的起始日口径（发票日 / 到期日 / 对账日，各公司不同，本工具按你给的分档核）',
  '核对与客户对账单是否一致（那要拿到对方的对账单）',
  '给出审计、税务或法律意见',
  '读取 .xlsx（需要你先从 Excel 复制成文本贴进来）',
];

const SAMPLE_TEXT = [
  '客户\t期初余额\t本期应收\t本期收款\t期末余额\t0-30天\t31-60天\t61-90天\t90天以上',
  '甲客户\t100000.00\t50000.00\t30000.00\t120000.00\t60000.00\t40000.00\t20000.00\t0.00',
  '乙客户\t50000.00\t20000.00\t60000.00\t10000.00\t10000.00\t0.00\t0.00\t0.00',
  '丙客户\t0.00\t80000.00\t30000.00\t50000.00\t30000.00\t20000.00\t0.00\t0.00',
  '合计\t150000.00\t150000.00\t120000.00\t180000.00\t100000.00\t60000.00\t20000.00\t0.00',
].join('\n');

const OVERDUE_RATIO_THRESHOLD = 0.30;

const ROLE_LABELS = {
  name: '客户', opening: '期初余额', debit: '本期应收', credit: '本期收款',
  closing: '期末余额', b0: '0-30天', b30: '31-60天', b60: '61-90天', b90: '90天以上',
};
const labelOf = (r) => ROLE_LABELS[r] || r;
const BUCKETS = ['b0', 'b30', 'b60', 'b90'];

const COLUMN_ROLES = [
  [/客户|单位名称|往来单位|公司名称|客户名称/, 'name'],
  [/期初|年初余额|上期期末|期初余额/, 'opening'],
  [/本期应收|本期发生|本月应收|应收增加|借方发生/, 'debit'],
  [/本期收款|本期收回|本月收款|贷方发生|已收款/, 'credit'],
  [/期末余额|期末数|余额/, 'closing'],
  [/90\s*天以上|90\+|一年以上|超\s*90/, 'b90'],
  [/61\s*[-~至]?\s*90/, 'b60'],
  [/31\s*[-~至]?\s*60/, 'b30'],
  [/0\s*[-~至]?\s*30|1\s*[-~至]?\s*30/, 'b0'],
];

const NON_AMOUNT_KWS = /编号|序号|备注|状态|日期|月份|账期|信用期|联系人|电话/;

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t');
  if (line.indexOf(',') >= 0) return line.split(',');
  return line.trim().split(/\s{2,}|\s+/);
}

function roleOf(header) {
  const h = String(header || '').replace(/\s/g, '');
  if (!h) return 'skip';
  if (NON_AMOUNT_KWS.test(h)) return 'skip';
  for (const pair of COLUMN_ROLES) if (pair[0].test(h)) return pair[1];
  return 'extra';
}

function normAmount(v) {
  if (v === null || v === undefined) return null;
  let s = String(v).trim();
  if (!s) return null;
  let neg = false;
  if (/^\(.*\)$/.test(s)) { neg = true; s = s.slice(1, -1); }
  s = s.replace(/[¥￥,\s]/g, '').replace(/元$/, '');
  if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
  const n = Number(s);
  return neg ? -n : n;
}

function isBlank(v) {
  const s = String(v === null || v === undefined ? '' : v).trim();
  if (!s) return true;
  return /^(--+|\?\?+|N\/?A|na|待填|TODO|xxx|\*\*\*?)$/i.test(s);
}

function findHeader(lines) {
  for (let i = 0; i < Math.min(lines.length, 10); i += 1) {
    const cells = splitRow(lines[i]).map((c) => c.trim());
    const roles = cells.map(roleOf);
    const known = roles.filter((r) => r !== 'skip' && r !== 'extra');
    const hasName = known.includes('name');
    const hasMoney = known.filter((r) => r !== 'name').length >= 3;
    if (hasName && hasMoney) return { index: i, cells, roles };
  }
  return null;
}

function parseTable(text) {
  const lines = String(text).split(/\r?\n/);
  const header = findHeader(lines);
  if (!header) return { error: 'no_header' };
  const people = [];
  const totals = [];
  for (let i = header.index + 1; i < lines.length; i += 1) {
    const raw = lines[i];
    if (!raw || !raw.trim()) continue;
    const cells = splitRow(raw).map((c) => c.trim());
    const rec = { line: i + 1, raw: raw.trim(), byRole: {} };
    header.roles.forEach((role, ci) => {
      if (role === 'skip' || role === 'extra') return;
      rec.byRole[role] = cells[ci] === undefined ? '' : cells[ci];
    });
    const name = String(rec.byRole.name || '').trim();
    if (/^(合计|总计|小计|total)/i.test(name)) totals.push(rec); else people.push(rec);
  }
  return { header, people, totals, cols: header.cells };
}

function finding(level, category, line, message, evidence, advice) {
  return { level, category, line, message, evidence, advice };
}

function sumRoles(rec, roles) {
  let sum = 0;
  for (const r of roles) {
    const n = normAmount(rec.byRole[r]);
    if (n === null) return null;
    sum += n;
  }
  return Math.round(sum * 100) / 100;
}

function checkIdentity(rec) {
  const o = normAmount(rec.byRole.opening);
  const d = normAmount(rec.byRole.debit);
  const c = normAmount(rec.byRole.credit);
  const cl = normAmount(rec.byRole.closing);
  if (o === null || d === null || c === null || cl === null) return null;
  const expect = Math.round((o + d - c) * 100) / 100;
  if (Math.abs(expect - cl) <= 0.01) return null;
  return finding('P0', '期末余额不平', rec.line,
    rec.byRole.name + ' 的期末余额是 ' + cl.toFixed(2) + '，但「期初 ' + o.toFixed(2)
      + ' + 本期应收 ' + d.toFixed(2) + ' − 本期收款 ' + c.toFixed(2) + '」应为 '
      + expect.toFixed(2) + '（差 ' + (cl - expect).toFixed(2) + '）',
    rec.raw, '先确认口径：如果有退货冲销、坏账核销或汇率折算，请把它们也列成一列再核。');
}

function checkAgingSum(rec) {
  const cl = normAmount(rec.byRole.closing);
  if (cl === null) return null;
  const s = sumRoles(rec, BUCKETS);
  if (s === null) return null;
  if (Math.abs(s - cl) <= 0.01) return null;
  return finding('P0', '账龄分档之和与期末余额不符', rec.line,
    rec.byRole.name + ' 的期末余额是 ' + cl.toFixed(2) + '，但各账龄分档相加是 '
      + s.toFixed(2) + '（差 ' + (cl - s).toFixed(2) + '）',
    rec.raw, '账龄分档必须与期末余额严丝合缝；差出来的部分通常是漏分档或分错了客户。');
}

function checkTotalRow(totals, people) {
  const out = [];
  if (!totals.length) return out;
  const t = totals[0];
  for (const role of Object.keys(t.byRole)) {
    if (role === 'name') continue;
    const claimed = normAmount(t.byRole[role]);
    if (claimed === null) continue;
    let sum = 0;
    let ok = true;
    for (const p of people) {
      const n = normAmount(p.byRole[role]);
      if (n === null) { ok = false; break; }
      sum += n;
    }
    if (!ok) continue;
    sum = Math.round(sum * 100) / 100;
    if (Math.abs(sum - claimed) <= 0.01) continue;
    out.push(finding('P0', '合计行算错', t.line,
      '合计行的「' + labelOf(role) + '」写的是 ' + claimed.toFixed(2) + '，但各客户相加是 '
        + sum.toFixed(2) + '（差 ' + (claimed - sum).toFixed(2) + '）',
      t.raw, '合计行常是从系统导出后手工改过，改了一处忘了另一处。'));
  }
  return out;
}

function checkDuplicates(people) {
  const seen = new Map();
  const out = [];
  for (const p of people) {
    const name = String(p.byRole.name || '').trim();
    if (!name) continue;
    if (seen.has(name)) {
      out.push(finding('P0', '同一客户出现两行', p.line,
        name + ' 出现了两次（上一次在第 ' + seen.get(name) + ' 行）',
        p.raw, '同一客户两行会让催收和坏账计提都算漏，请先合并或确认是否同一集团不同主体。'));
    } else seen.set(name, p.line);
  }
  return out;
}

function checkBlanks(people) {
  const out = [];
  const roles = Object.keys(people[0] ? people[0].byRole : {}).filter((r) => r !== 'name');
  for (const p of people) {
    const name = String(p.byRole.name || '').trim();
    if (!name) {
      out.push(finding('P0', '客户名称缺失', p.line, '这一行没有客户名称', p.raw, '请确认这一行是否有效。'));
      continue;
    }
    for (const r of roles) {
      const v = p.byRole[r];
      if (isBlank(v)) {
        out.push(finding('P1', '该填没填', p.line,
          name + ' 的「' + labelOf(r) + '」是空的或还是占位符（' + (String(v).trim() || '空') + '）',
          p.raw, '账龄表出现空列，通常是从系统导出时漏选，或模板没替换。'));
      } else if (normAmount(v) === null) {
        out.push(finding('P1', '金额无法解析', p.line,
          name + ' 的「' + labelOf(r) + '」写作「' + String(v).trim() + '」，不是能计算的金额',
          p.raw, '请确认列是否串位。'));
      }
    }
  }
  return out;
}

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。',
  };
}

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['应收账龄表原文（text）']);
  const t = parseTable(text);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的账龄表（要能认出「客户」+ 至少三个金额列，例如「期末余额」「本期应收」）',
      '从系统导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.people.length) return insufficient(['至少一个客户的明细行']);

  const threshold = payload && typeof payload.overdueRatio === 'number'
    ? payload.overdueRatio : OVERDUE_RATIO_THRESHOLD;

  const findings = [];
  const notRun = [];
  for (const p of t.people) {
    const a = checkIdentity(p); if (a) findings.push(a);
    const b = checkAgingSum(p); if (b) findings.push(b);

  }
  for (const f of checkTotalRow(t.totals, t.people)) findings.push(f);
  for (const f of checkDuplicates(t.people)) findings.push(f);
  for (const f of checkBlanks(t.people)) findings.push(f);

  const totalClosing = t.people.reduce((s, p) => {
    const n = normAmount(p.byRole.closing);
    return s + (n === null ? 0 : n);
  }, 0);
  const totalOverdue = t.people.reduce((s, p) => {
    const n = normAmount(p.byRole.b90);
    return s + (n === null ? 0 : n);
  }, 0);
  const ratio = totalClosing > 0 ? totalOverdue / totalClosing : 0;
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));

  const result = {
    findings,
    summary: {
      customers: t.people.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      closing_total: Math.round(totalClosing * 100) / 100,
      over90_total: Math.round(totalOverdue * 100) / 100,
      over90_ratio: Math.round(ratio * 10000) / 10000,
      basis: '逐客户「期初+应收−收款=期末」与「账龄分档之和=期末」比对；合计行逐列复核',
    },
    columns: t.cols,
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明这张表**算得对**，'
      + '不代表客户还得起钱、也不代表坏账准备提够了 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normAmount, isBlank, labelOf, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, ROLE_LABELS, BUCKETS, OVERDUE_RATIO_THRESHOLD,
};
