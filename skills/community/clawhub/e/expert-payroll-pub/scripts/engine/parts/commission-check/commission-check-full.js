#!/usr/bin/env node
/**
 * commission-check.js —— 销售提成核对引擎（确定性、纯 Node 标准库）。
 *
 * 为什么做这个：
 *   **有销售团队的公司每个月都要算提成**，而提成表一旦算错，
 *   要么销售少拿钱（立刻来问）、要么公司多付（没人会发现）。
 *   逐人核「销售额 × 提成率 = 提成」「基数项加总 = 计奖基数」「提成 + 底薪 = 应发」
 *   「合计行 = 各人之和」「有没有同一人两行」「有没有该填没填」—— 这些**全是算术**。
 *
 * 与已有能力的区别（不是重复品）：
 *   · `payroll-check` 核的是「工资表能不能发」（实发 = 应发 − 扣款）；
 *   · 本能力核的是「**提成是怎么算出来的**」—— 销售额、提成率、阶梯档位、计奖基数这条链。
 *
 * 契约（与其它引擎一致）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *
 * 刻意不做的事：不联网、不调用大模型；材料不足不给结论；
 * **不判断提成率定得合不合理**（那是公司薪酬制度的事）。
 */
'use strict';

const CHECKS_GIVEN = [
  '逐人计奖基数勾稽（销售额 + 其他加项 = 计奖基数）',
  '逐人提成复核（计奖基数 × 提成率 = 提成金额）',
  '逐人应发复核（提成金额 + 底薪 = 应发合计）',
  '合计行复核（每一列的合计是否等于各人之和）',
  '重复人员检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '阶梯提成复核（按你得给的档位区间重算各档金额）',
  '提成率区间校验（默认 0%~30%，超出提示）',
  '提成金额为负或超过基数（方向异常）',
  '同一人提成率不一致（同名多行的隐性线索）',
];

const OUT_OF_SCOPE = [
  '判断提成率、阶梯档位定得合不合理（那是公司薪酬制度与劳动合同的事）',
  '判断回款是否达成、该不该扣回提成（那要看回款政策）',
  '计算个税与社保（那是工资表与社保核对那两个能力的范围）',
  '给出税务、劳动法或审计意见',
  '读取 .xlsx（需要你先从 Excel 复制成文本贴进来）',
];

/* 干净样例：三人三条恒等式全部吻合，合计行也对得上。
   张：基数 100000 + 0 = 100000，率 5% → 提成 5000，底薪 5000 → 应发 10000
   李：基数 200000 + 10000 = 210000，率 8% → 提成 16800，底薪 6000 → 应发 22800
   王：基数 80000 + 0 = 80000，率 5% → 提成 4000，底薪 4500 → 应发 8500 */
const SAMPLE_TEXT = [
  '姓名\t销售额\t其他加项\t计奖基数\t提成率\t提成金额\t底薪\t应发合计',
  '张三\t100000.00\t0.00\t100000.00\t5%\t5000.00\t5000.00\t10000.00',
  '李四\t200000.00\t10000.00\t210000.00\t8%\t16800.00\t6000.00\t22800.00',
  '王五\t80000.00\t0.00\t80000.00\t5%\t4000.00\t4500.00\t8500.00',
  '合计\t380000.00\t10000.00\t390000.00\t\t25800.00\t15500.00\t41300.00',
].join('\n');

const RATE_MIN = 0;
const RATE_MAX = 0.30;

const ROLE_LABELS = {
  name: '姓名', code: '工号', sales: '销售额', other: '其他加项', base: '计奖基数',
  rate: '提成率', commission: '提成金额', salary: '底薪', total: '应发合计',
};
const labelOf = (r) => ROLE_LABELS[r] || r;
const SUM_ROLES = ['sales', 'other', 'base', 'commission', 'salary', 'total'];

const COLUMN_ROLES = [
  [/工号|员工编号|编号/, 'code'],
  [/姓名|员工|人员|销售员|名字/, 'name'],
  [/销售额|业绩|回款额|销售金额/, 'sales'],
  [/其他加项|补贴|奖励|其他[,，]?加/, 'other'],
  [/计奖基数|提成基数|计提基数|基数/, 'base'],
  [/提成率|提成比例|比例|点数/, 'rate'],
  [/提成金额|提成额|提成/, 'commission'],
  [/底薪|基本工资|固定工资/, 'salary'],
  [/应发合计|应发工资|应发|合计金额/, 'total'],
];

const NON_AMOUNT_KWS = /备注|状态|部门|区域|日期|月份|产品|客户/;

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

/** 提成率支持「5%」「5％」「0.05」「5」四种写法。 */
function normRate(v) {
  if (v === null || v === undefined) return null;
  const s = String(v).trim().replace(/％/g, '%');
  if (!s) return null;
  if (s.endsWith('%')) {
    const n = Number(s.slice(0, -1));
    return Number.isFinite(n) ? n / 100 : null;
  }
  const n = Number(s.replace(/[,\s]/g, ''));
  if (!Number.isFinite(n)) return null;
  return n > 1 ? n / 100 : n;
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
    const money = ['sales', 'base', 'commission', 'total'].filter((r) => known.includes(r)).length;
    if (hasKey && money >= 3) return { index: i, cells, roles };
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
    const nm = String(rec.byRole.name || rec.byRole.code || '').trim();
    if (/^(合计|总计|小计|total)/i.test(nm)) totals.push(rec); else people.push(rec);
  }
  return { header, people, totals, cols: header.cells };
}

function finding(level, category, line, message, evidence, advice) {
  return { level, category, line, message, evidence, advice };
}

const tag = (rec) => String(rec.byRole.name || rec.byRole.code || '（未命名）').trim();

function checkBase(rec) {
  const s = normAmount(rec.byRole.sales);
  const o = normAmount(rec.byRole.other);
  const b = normAmount(rec.byRole.base);
  if (s === null || o === null || b === null) return null;
  const expect = Math.round((s + o) * 100) / 100;
  if (Math.abs(expect - b) <= 0.01) return null;
  return finding('P0', '计奖基数不平', rec.line,
    tag(rec) + ' 的计奖基数是 ' + b.toFixed(2) + '，但「销售额 ' + s.toFixed(2) + ' + 其他加项 '
      + o.toFixed(2) + '」应为 ' + expect.toFixed(2) + '（差 ' + (b - expect).toFixed(2) + '）',
    rec.raw, '先确认口径：如果有退货冲减、跨区拆分或系数调整，请把它们也列成一列再核。');
}

function checkCommission(rec) {
  const b = normAmount(rec.byRole.base);
  const r = normRate(rec.byRole.rate);
  const c = normAmount(rec.byRole.commission);
  if (b === null || r === null || c === null) return null;
  const expect = Math.round(b * r * 100) / 100;
  if (Math.abs(expect - c) <= 0.01) return null;
  return finding('P0', '提成金额算错', rec.line,
    tag(rec) + ' 的提成金额是 ' + c.toFixed(2) + '，但「计奖基数 ' + b.toFixed(2) + ' × 提成率 '
      + (r * 100).toFixed(2) + '%」应为 ' + expect.toFixed(2) + '（差 ' + (c - expect).toFixed(2) + '）',
    rec.raw, '如果是阶梯提成（分档累进），请把各档金额分行列出，否则本工具只能按单一比例核。');
}

function checkTotal(rec) {
  const c = normAmount(rec.byRole.commission);
  const s = normAmount(rec.byRole.salary);
  const t = normAmount(rec.byRole.total);
  if (c === null || s === null || t === null) return null;
  const expect = Math.round((c + s) * 100) / 100;
  if (Math.abs(expect - t) <= 0.01) return null;
  return finding('P0', '应发合计算错', rec.line,
    tag(rec) + ' 的应发合计是 ' + t.toFixed(2) + '，但「提成金额 ' + c.toFixed(2) + ' + 底薪 '
      + s.toFixed(2) + '」应为 ' + expect.toFixed(2) + '（差 ' + (t - expect).toFixed(2) + '）',
    rec.raw, '应发合计要与工资表里的提成项对得上，否则会发错钱。');
}

function checkTotalRow(totals, people) {
  const out = [];
  if (!totals.length) return out;
  const t = totals[0];
  for (const role of SUM_ROLES) {
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
      '合计行的「' + labelOf(role) + '」写的是 ' + claimed.toFixed(2) + '，但各人相加是 '
        + sum.toFixed(2) + '（差 ' + (claimed - sum).toFixed(2) + '）',
      t.raw, '合计行常是从系统导出后手工改过，改了一处忘了另一处。'));
  }
  return out;
}

function checkDuplicates(people) {
  const seen = new Map();
  const out = [];
  for (const p of people) {
    const key = String(p.byRole.name || p.byRole.code || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push(finding('P0', '同一人出现两行', p.line,
        key + ' 出现了两次（上一次在第 ' + seen.get(key) + ' 行）',
        p.raw, '同一人两行可能是一人多区域或跨月数据混在一起，请先确认是不是重复计算。'));
    } else seen.set(key, p.line);
  }
  return out;
}

function checkBlanks(people) {
  const out = [];
  const roles = Object.keys(people[0] ? people[0].byRole : {})
    .filter((r) => r !== 'name' && r !== 'code');
  for (const p of people) {
    if (!String(p.byRole.name || p.byRole.code || '').trim()) {
      out.push(finding('P0', '姓名缺失', p.line, '这一行没有姓名或工号', p.raw, '请确认这一行是否有效。'));
      continue;
    }
    for (const r of roles) {
      const v = p.byRole[r];
      if (isBlank(v)) {
        out.push(finding('P1', '该填没填', p.line,
          tag(p) + ' 的「' + labelOf(r) + '」是空的或还是占位符（' + (String(v).trim() || '空') + '）',
          p.raw, '提成表出现空列，通常是从系统导出时漏选，或模板没替换。'));
      } else {
        const okNum = normAmount(v) !== null || (r === 'rate' && normRate(v) !== null);
        if (!okNum) {
          out.push(finding('P1', '数值无法解析', p.line,
            tag(p) + ' 的「' + labelOf(r) + '」写作「' + String(v).trim() + '」，不是能计算的数值',
            p.raw, '请确认列是否串位。'));
        }
      }
    }
  }
  return out;
}

function checkRateRange(rec) {
  const r = normRate(rec.byRole.rate);
  if (r === null) return null;
  if (r >= RATE_MIN - 1e-9 && r <= RATE_MAX + 1e-9) return null;
  return finding('P1', '提成率超出常见区间', rec.line,
    tag(rec) + ' 的提成率是 ' + (r * 100).toFixed(2) + '%，不在 0%~30% 之间',
    rec.raw, '可能是把 5% 填成 50%，或把万分之几当成了百分比。请确认。');
}

function checkDirection(rec) {
  const out = [];
  const c = normAmount(rec.byRole.commission);
  const s = normAmount(rec.byRole.sales);
  const t = normAmount(rec.byRole.total);
  if (c !== null && c < 0) {
    out.push(finding('P1', '提成金额为负', rec.line,
      tag(rec) + ' 的提成金额是 ' + c.toFixed(2) + '（负数）',
      rec.raw, '负数提成通常是退货冲减或扣回；请确认这笔该不该在本期扣，以及有没有依据。'));
  }
  if (c !== null && s !== null && Math.abs(c) > Math.abs(s) + 0.01) {
    out.push(finding('P1', '提成金额超过销售额', rec.line,
      tag(rec) + ' 的提成金额 ' + c.toFixed(2) + ' 超过销售额 ' + s.toFixed(2),
      rec.raw, '提成大于销售额通常是比例填错（例如把 5% 填成 5 倍）。'));
  }
  if (t !== null && t < 0) {
    out.push(finding('P1', '应发合计为负', rec.line,
      tag(rec) + ' 的应发合计是 ' + t.toFixed(2) + '（负数）',
      rec.raw, '应发为负说明扣回超过应发，请确认是否应跨期分摊。'));
  }
  return out;
}

/** 阶梯（累进）提成：按档位逐段计算，返回每段金额与合计。
 *  ladder 例：[{upTo:100000, rate:0.05}, {upTo:200000, rate:0.08}, {upTo:null, rate:0.12}]
 *  含义：0~10 万按 5%，10~20 万的部分按 8%，20 万以上按 12%。 */
function computeLadder(base, ladder) {
  const segs = [];
  let prev = 0;
  let sum = 0;
  for (const step of ladder) {
    const up = (step.upTo === null || step.upTo === undefined) ? Infinity : Number(step.upTo);
    const rate = Number(step.rate);
    if (!Number.isFinite(rate)) return null;
    if (base <= prev) break;
    const width = Math.min(base, up) - prev;
    if (width <= 0) { prev = up; continue; }
    const amt = Math.round(width * rate * 100) / 100;
    segs.push({ from: prev, to: up === Infinity ? null : up, rate, amount: amt });
    sum += amt;
    prev = up;
    if (up === Infinity) break;
  }
  return { segs, total: Math.round(sum * 100) / 100 };
}

/** 阶梯提成复核：入参给了 ladder 才执行（否则如实列为"未执行"）。 */
function checkLadder(rec, ladder) {
  const b = normAmount(rec.byRole.base);
  const c = normAmount(rec.byRole.commission);
  if (b === null || c === null) return null;
  const calc = computeLadder(b, ladder);
  if (!calc) return null;
  if (Math.abs(calc.total - c) <= 0.01) return null;
  return finding('P1', '阶梯提成算错', rec.line,
    tag(rec) + ' 的提成金额是 ' + c.toFixed(2) + '，但按你给的阶梯档位（计奖基数 '
      + b.toFixed(2) + '）重算应为 ' + calc.total.toFixed(2)
      + '（差 ' + (c - calc.total).toFixed(2) + '）',
    rec.raw, '各档明细：' + calc.segs.map((x) => (x.from + '~' + (x.to === null ? '以上' : x.to))
      + ' × ' + (x.rate * 100).toFixed(2) + '% = ' + x.amount.toFixed(2)).join('；'));
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
  if (!String(text).trim()) return insufficient(['提成计算表原文（text）']);
  const t = parseTable(text);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的提成表（要能认出「姓名」+ 至少三个金额列，例如「销售额」「计奖基数」「提成金额」）',
      '从系统导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.people.length) return insufficient(['至少一人的明细行']);

  const paid = Boolean(payload && (payload.full || payload.credit || payload.token));
  const ladder = payload && Array.isArray(payload.ladder) && payload.ladder.length
    ? payload.ladder : null;
  const findings = [];
  const notRun = [];
  for (const p of t.people) {
    const a = checkBase(p); if (a) findings.push(a);
    // 给了阶梯档位就走阶梯复核；否则按单一提成率核。**两者不能同时跑** ——
    // 阶梯提成本来就不等于「基数 × 单一比例」，同时跑必然误报。
    if (!ladder) {
      const b = checkCommission(p); if (b) findings.push(b);
    }
    const c = checkTotal(p); if (c) findings.push(c);
    if (paid) {
      const r = checkRateRange(p); if (r) findings.push(r);
      for (const f of checkDirection(p)) findings.push(f);
      if (ladder) { const l = checkLadder(p, ladder); if (l) findings.push(l); }
    }
  }
  if (paid) {
    if (ladder) notRun.push('单一提成率复核（已改用你给的阶梯档位重算）');
    else notRun.push('阶梯提成复核（未在入参里给 ladder 档位）');
  }
  for (const f of checkTotalRow(t.totals, t.people)) findings.push(f);
  for (const f of checkDuplicates(t.people)) findings.push(f);
  for (const f of checkBlanks(t.people)) findings.push(f);
  if (!paid) notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => Math.round(t.people.reduce((s, p) => {
    const n = normAmount(p.byRole[role]);
    return s + (n === null ? 0 : n);
  }, 0) * 100) / 100;

  const result = {
    findings,
    summary: {
      people: t.people.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      sales_total: sumOf('sales'),
      commission_total: sumOf('commission'),
      payable_total: sumOf('total'),
      basis: '逐人「销售额+其他加项=计奖基数」「基数×提成率=提成金额」「提成+底薪=应发合计」比对',
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
      + '不代表提成制度定得合理、也不代表回款都达成了 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normAmount, normRate, isBlank, labelOf,
  CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT,
  ROLE_LABELS, SUM_ROLES, RATE_MIN, RATE_MAX, computeLadder,
};
