#!/usr/bin/env node
/**
 * lesson-hour-check.js —— 课时核销核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**教培 / 健身 / 美容这类"卖课时、按次消课"的机构，每月都要跟家长/会员对一次课时**：
 * 买了多少课时、已消耗多少、还剩多少、耗课金额怎么算的。单量一多（几百上千学员），
 * 人眼核不动；而这些**全是算术**。核错的后果是**退费算错、续费谈崩、甚至被投诉**。
 *
 * 与已有能力的区别：本能力核「**机构 ↔ 学员的课时账**」，不是工资表、不是平台结算。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不调用大模型；材料不足不给结论；不判断课时定价是否合理。
 */
'use strict';

const CHECKS_GIVEN = [
  '逐人课时勾稽（购买课时 − 已耗课时 = 剩余课时）',
  '逐人耗课金额复核（已耗课时 × 课时单价 = 耗课金额）',
  '合计行复核（每一列的合计是否等于各人之和）',
  '重复学员检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '超耗检测（已耗课时 > 购买课时，剩余为负）',
  '零单价却有耗课（定价缺失）检测',
  '耗课金额超过「购买课时 × 单价」上限检测',
  '课时单价不一致（同一课程应同价）',
];

const OUT_OF_SCOPE = [
  '判断课时定价、赠送课时、退费规则是否合理（那是机构制度与合同的事）',
  '核对学员是否真的来上过课（那要拿出勤记录来比）',
  '处理退费与结转（本工具只核你给出的这张表算得对不对）',
  '给出税务或法律意见',
  '读取 .xlsx（需要你先从教务系统导出、复制成文本贴进来）',
];

const SAMPLE_TEXT = [
  '学员\t购买课时\t已耗课时\t剩余课时\t课时单价\t耗课金额',
  '甲同学\t100\t40\t60\t200.00\t8000.00',
  '乙同学\t50\t50\t0\t300.00\t15000.00',
  '丙同学\t20\t5\t15\t250.00\t1250.00',
  '合计\t170\t95\t75\t\t24250.00',
].join('\n');

const PRICE_MIN = 0.01;
const PRICE_MAX = 9999;
const TOL = 0.01;

const ROLE_LABELS = {
  name: '学员', code: '学号', bought: '购买课时', used: '已耗课时',
  left: '剩余课时', price: '课时单价', amount: '耗课金额',
};
const labelOf = (r) => ROLE_LABELS[r] || r;
const SUM_ROLES = ['bought', 'used', 'left', 'amount'];
const QTY_ROLES = ['bought', 'used', 'left'];

const COLUMN_ROLES = [
  [/学号|学员编号|会员号/, 'code'],
  [/学员|会员|姓名|学生|客户/, 'name'],
  [/购买课时|购买课次|总课时|课次|购买次数/, 'bought'],
  [/已耗课时|已消课时|已上课时|已用课时|已消课次|已核销/, 'used'],
  [/剩余课时|剩余课次|余额课时|剩余次数/, 'left'],
  [/课时单价|课次单价|单价|课时费/, 'price'],
  [/耗课金额|已耗金额|消课金额|核销金额|课时金额/, 'amount'],
];

const NON_AMOUNT_KWS = /备注|状态|日期|月份|课程|班级|老师|顾问|到期/;

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
    const hasKey = known.includes('name') || known.includes('code');
    const qty = QTY_ROLES.filter((r) => known.includes(r)).length;
    if (hasKey && qty >= 2) return { index: i, cells, roles };
  }
  return null;
}

function parseTable(text) {
  const lines = String(text).split(/\r?\n/);
  const header = findHeader(lines);
  if (!header) return { error: 'no_header' };
  const items = [];
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
    const nm = String(rec.byRole.name || rec.byRole.code || '').trim();
    if (/^(合计|总计|小计|total)/i.test(nm)) totals.push(rec); else items.push(rec);
  }
  return { header, items, totals, cols: header.cells };
}

function finding(level, category, line, message, evidence, advice) {
  return { level, category, line, message, evidence, advice };
}

const tag = (rec) => String(rec.byRole.name || rec.byRole.code || '（未命名学员）').trim();

function checkHours(rec) {
  const b = normAmount(rec.byRole.bought);
  const u = normAmount(rec.byRole.used);
  const l = normAmount(rec.byRole.left);
  if (b === null || u === null || l === null) return null;
  const expect = Math.round((b - u) * 100) / 100;
  if (Math.abs(expect - l) <= TOL) return null;
  return finding('P0', '剩余课时不平', rec.line,
    tag(rec) + ' 的剩余课时是 ' + l + '，但「购买 ' + b + ' − 已耗 ' + u + '」应为 ' + expect
      + '（差 ' + (l - expect) + '）',
    rec.raw, '先确认口径：如果有赠送课时、冻结课时、跨课程结转，请把它们也列成一列再核。');
}

function checkAmount(rec) {
  const u = normAmount(rec.byRole.used);
  const p = normAmount(rec.byRole.price);
  const a = normAmount(rec.byRole.amount);
  if (u === null || p === null || a === null) return null;
  const expect = Math.round(u * p * 100) / 100;
  if (Math.abs(expect - a) <= TOL) return null;
  return finding('P0', '耗课金额算错', rec.line,
    tag(rec) + ' 的耗课金额是 ' + a.toFixed(2) + '，但「已耗课时 ' + u + ' × 单价 ' + p.toFixed(2)
      + '」应为 ' + expect.toFixed(2) + '（差 ' + (a - expect).toFixed(2) + '）',
    rec.raw, '耗课金额直接决定还剩多少钱可退；算错会导致退费纠纷。');
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals.length) return out;
  const t = totals[0];
  for (const role of SUM_ROLES) {
    const claimed = normAmount(t.byRole[role]);
    if (claimed === null) continue;
    let sum = 0; let ok = true;
    for (const it of items) {
      const n = normAmount(it.byRole[role]);
      if (n === null) { ok = false; break; }
      sum += n;
    }
    if (!ok) continue;
    sum = Math.round(sum * 100) / 100;
    if (Math.abs(sum - claimed) <= TOL) continue;
    out.push(finding('P0', '合计行算错', t.line,
      '合计行的「' + labelOf(role) + '」写的是 ' + claimed + '，但各人相加是 ' + sum
        + '（差 ' + Math.round((claimed - sum) * 100) / 100 + '）',
      t.raw, '合计行是机构的总账，对不上时通常有人被漏加或重复加。'));
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.name || it.byRole.code || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push(finding('P0', '同一学员出现两行', it.line,
        key + ' 出现了两次（上一次在第 ' + seen.get(key) + ' 行）',
        it.raw, '同一学员两行会让剩余课时与可退金额都算错，请先合并。'));
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  const TXT = ['name', 'code'];
  const roles = Object.keys(items[0] ? items[0].byRole : {}).filter((r) => TXT.indexOf(r) < 0);
  for (const it of items) {
    if (!String(it.byRole.name || it.byRole.code || '').trim()) {
      out.push(finding('P0', '学员无姓名也无学号', it.line, '这一行认不出是谁', it.raw,
        '请确认这一行是否有效。'));
      continue;
    }
    for (const r of roles) {
      const v = it.byRole[r];
      if (isBlank(v)) {
        out.push(finding('P1', '该填没填', it.line,
          tag(it) + ' 的「' + labelOf(r) + '」是空的或还是占位符（' + (String(v).trim() || '空') + '）',
          it.raw, '课时表出现空列，通常是从教务系统导出时漏选。'));
      } else if (normAmount(v) === null) {
        out.push(finding('P1', '数值无法解析', it.line,
          tag(it) + ' 的「' + labelOf(r) + '」写作「' + String(v).trim() + '」，不是能计算的数值',
          it.raw, '请确认列是否串位。'));
      }
    }
  }
  return out;
}

function checkOverused(rec) {
  const b = normAmount(rec.byRole.bought);
  const u = normAmount(rec.byRole.used);
  const l = normAmount(rec.byRole.left);
  if (b === null || u === null) return null;
  if (u <= b + TOL && (l === null || l >= -TOL)) return null;
  return finding('P0', '超耗课时', rec.line,
    tag(rec) + ' 购买 ' + b + ' 课时、已耗 ' + u + ' 课时'
      + (l !== null ? '、剩余 ' + l : ''),
    rec.raw, '已耗超过购买会让剩余为负；通常是漏记了续费/赠送课时，或消课记录重复。');
}

function checkZeroPrice(rec) {
  const u = normAmount(rec.byRole.used);
  const p = normAmount(rec.byRole.price);
  if (u === null || p === null) return null;
  if (u <= 0 || p > 0) return null;
  return finding('P1', '零单价却有耗课', rec.line,
    tag(rec) + ' 已耗 ' + u + ' 课时，但课时单价是 0',
    rec.raw, '单价缺失会让耗课金额算成 0，退费时就说不清了。请补上真实单价。');
}

function checkPriceRange(rec) {
  const p = normAmount(rec.byRole.price);
  if (p === null) return null;
  if (p >= PRICE_MIN - 1e-9 && p <= PRICE_MAX + 1e-9) return null;
  return finding('P1', '课时单价异常', rec.line,
    tag(rec) + ' 的课时单价是 ' + p.toFixed(2) + '，不在 ' + PRICE_MIN + '~' + PRICE_MAX + ' 之间',
    rec.raw, '可能是把课时数填到了单价列，或漏了小数点。');
}

function insufficient(missing) {
  return { status: 'insufficient_input', missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。' };
}

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['课时核销表原文（text）']);
  const t = parseTable(text);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的课时表（要能认出「学员/学号」+ 至少两个课时列，例如「购买课时」「已耗课时」）',
      '从教务系统导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一名学员的明细行']);

  const paid = Boolean(payload && (payload.full || payload.credit || payload.token));
  const findings = [];
  const notRun = [];
  for (const it of t.items) {
    const a = checkHours(it); if (a) findings.push(a);
    const b = checkAmount(it); if (b) findings.push(b);
    if (paid) {
      const o = checkOverused(it); if (o) findings.push(o);
      const z = checkZeroPrice(it); if (z) findings.push(z);
      const r = checkPriceRange(it); if (r) findings.push(r);
    }
  }
  for (const f of checkTotalRow(t.totals, t.items)) findings.push(f);
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);
  if (!paid) notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => Math.round(t.items.reduce((s, it) => {
    const n = normAmount(it.byRole[role]);
    return s + (n === null ? 0 : n);
  }, 0) * 100) / 100;

  const result = {
    findings,
    summary: {
      students: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      hours_left_total: sumOf('left'),
      amount_total: sumOf('amount'),
      basis: '逐人「购买课时−已耗课时=剩余课时」与「已耗课时×单价=耗课金额」比对；合计行逐列复核',
    },
    columns: t.cols,
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明这张表**算得对**，'
      + '不代表学员真的来上过课、也不代表定价合理 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normAmount, isBlank, labelOf,
  CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT,
  ROLE_LABELS, SUM_ROLES, QTY_ROLES,
};
