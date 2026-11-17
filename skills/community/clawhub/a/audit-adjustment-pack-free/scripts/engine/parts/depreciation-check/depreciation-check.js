#!/usr/bin/env node
/**
 * depreciation-check.js —— 固定资产折旧核对引擎（确定性、纯 Node 标准库）。
 *
 * 为什么做这个：
 *   **每月结账都要跑一次折旧**，而折旧表是"一旦错了会一直错下去"的典型：
 *   月折旧额按「(原值 − 残值) ÷ 使用年限 ÷ 12」直线法算，
 *   累计折旧 = 月折旧 × 已提月数，净值 = 原值 − 累计折旧。
 *   资产一多（几百上千项），手工核这三条恒等式几乎不可能，而这些**全是算术**。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约（与其它引擎一致）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *
 * 刻意不做的事：不联网、不调用大模型；材料不足不给结论；
 * **不判断某类资产该按几年折旧、残值率该定多少**（那是会计准则与公司政策的事）。
 */
'use strict';

const CHECKS_GIVEN = [
  '逐项月折旧额复核（(原值 × (1 − 残值率)) ÷ 使用年限 ÷ 12）',
  '逐项累计折旧复核（月折旧额 × 已提月数）',
  '逐项净值复核（原值 − 累计折旧）',
  '合计行复核（原值 / 本月折旧 / 累计折旧 / 净值 各列是否等于各资产之和）',
  '重复资产编号检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '超提检测（已提月数 > 使用年限 × 12）',
  '累计折旧超过「原值 − 残值」上限检测',
  '停提异常（已提月数 > 0 但本月折旧为 0）',
  '残值率区间校验（默认 0%~10%）',
];

const OUT_OF_SCOPE = [
  '判断某类固定资产该按几年折旧、残值率该定多少（那是会计准则与公司政策的事）',
  '判断是否该做减值测试、该不该转固（那是会计判断）',
  '核对固定资产实物是否真的存在（那要盘点）',
  '给出审计或税务意见',
  '读取 .xlsx（需要你先从 Excel 复制成文本贴进来）',
];

const SAMPLE_TEXT = [
  '资产编号\t资产名称\t原值\t残值率\t使用年限\t已提月数\t本月折旧\t累计折旧\t净值',
  'FA-001\t生产线设备\t120000.00\t5%\t10\t24\t950.00\t22800.00\t97200.00',
  'FA-002\t运输车辆\t60000.00\t5%\t5\t12\t950.00\t11400.00\t48600.00',
  'FA-003\t办公电脑\t36000.00\t0%\t3\t6\t1000.00\t6000.00\t30000.00',
  '合计\t\t216000.00\t\t\t\t2900.00\t40200.00\t175800.00',
].join('\n');

const RESIDUAL_MIN = 0;
const RESIDUAL_MAX = 0.10;

const ROLE_LABELS = {
  code: '资产编号', name: '资产名称', cost: '原值', residualRate: '残值率',
  life: '使用年限', months: '已提月数', monthly: '本月折旧',
  accum: '累计折旧', net: '净值',
};
const labelOf = (r) => ROLE_LABELS[r] || r;
const TOTALLED = ['cost', 'monthly', 'accum', 'net'];

const COLUMN_ROLES = [
  [/资产编号|卡片编号|资产代码|编号/, 'code'],
  [/资产名称|名称|设备名称|固定资产名称/, 'name'],
  [/原值|原价|入账价值|资产原值/, 'cost'],
  [/残值率|净残值率|预计净残值率/, 'residualRate'],
  [/使用年限|折旧年限|年限|使用寿命/, 'life'],
  [/已提月数|已计提月数|已折旧月数|已提月份/, 'months'],
  [/本月折旧|月折旧额|本期折旧|当月折旧/, 'monthly'],
  [/累计折旧|已提折旧/, 'accum'],
  [/净值|账面价值|账面净值/, 'net'],
];

const NON_AMOUNT_KWS = /备注|状态|部门|使用人|存放|日期|类别|供应商|发票/;

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

/** 残值率支持「5%」「5％」「0.05」三种写法，统一成小数。 */
function normRate(v) {
  if (v === null || v === undefined) return null;
  let s = String(v).trim().replace(/％/g, '%');
  if (!s) return null;
  if (s.endsWith('%')) {
    const n = Number(s.slice(0, -1));
    return Number.isFinite(n) ? n / 100 : null;
  }
  const n = Number(s.replace(/[,\s]/g, ''));
  if (!Number.isFinite(n)) return null;
  return n > 1 ? n / 100 : n;   // 写成 5 的当 5% 处理
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
    const need = ['cost', 'monthly', 'accum', 'net'].filter((r) => known.includes(r));
    if (known.includes('name') && need.length >= 2) return { index: i, cells, roles };
  }
  return null;
}

function parseTable(text) {
  const lines = String(text).split(/\r?\n/);
  const header = findHeader(lines);
  if (!header) return { error: 'no_header' };
  const assets = [];
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
    const name = String(rec.byRole.name || rec.byRole.code || '').trim();
    if (/^(合计|总计|小计|total)/i.test(name)) totals.push(rec); else assets.push(rec);
  }
  return { header, assets, totals, cols: header.cells };
}

function finding(level, category, line, message, evidence, advice) {
  return { level, category, line, message, evidence, advice };
}

const who = (rec) => String(rec.byRole.name || rec.byRole.code || '（未命名资产）').trim();
const tag = (rec) => {
  const c = String(rec.byRole.code || '').trim();
  const n = String(rec.byRole.name || '').trim();
  return c && n ? c + ' ' + n : (c || n || '（未命名资产）');
};

function checkMonthly(rec) {
  const cost = normAmount(rec.byRole.cost);
  const rate = normRate(rec.byRole.residualRate);
  const life = normAmount(rec.byRole.life);
  const m = normAmount(rec.byRole.monthly);
  if (cost === null || rate === null || life === null || m === null || life === 0) return null;
  const r = rate === null ? 0 : rate;
  const expect = Math.round((cost * (1 - r)) / (life * 12) * 100) / 100;
  if (Math.abs(expect - m) <= 0.01) return null;
  return finding('P0', '本月折旧额算错', rec.line,
    tag(rec) + ' 的本月折旧是 ' + m.toFixed(2) + '，但按「原值 ' + cost.toFixed(2)
      + ' × (1 − 残值率 ' + (r * 100).toFixed(2) + '%) ÷ (' + life + ' 年 × 12)」应为 '
      + expect.toFixed(2) + '（差 ' + (m - expect).toFixed(2) + '）',
    rec.raw, '直线法月折旧额。若公司用的是双倍余额递减或年数总和法，请以你们的折旧政策为准。');
}

function checkAccum(rec) {
  const m = normAmount(rec.byRole.monthly);
  const months = normAmount(rec.byRole.months);
  const acc = normAmount(rec.byRole.accum);
  if (m === null || months === null || acc === null) return null;
  const expect = Math.round(m * months * 100) / 100;
  if (Math.abs(expect - acc) <= 0.01) return null;
  return finding('P0', '累计折旧不等于月折旧×已提月数', rec.line,
    tag(rec) + ' 的累计折旧是 ' + acc.toFixed(2) + '，但「本月折旧 ' + m.toFixed(2)
      + ' × 已提 ' + months + ' 个月」应为 ' + expect.toFixed(2) + '（差 ' + (acc - expect).toFixed(2) + '）',
    rec.raw, '若有中途调整原值或补提折旧，累计数与月折旧乘月数会不等，请按实际情况确认。');
}

function checkNet(rec) {
  const cost = normAmount(rec.byRole.cost);
  const acc = normAmount(rec.byRole.accum);
  const net = normAmount(rec.byRole.net);
  if (cost === null || acc === null || net === null) return null;
  const expect = Math.round((cost - acc) * 100) / 100;
  if (Math.abs(expect - net) <= 0.01) return null;
  return finding('P0', '净值不等于原值−累计折旧', rec.line,
    tag(rec) + ' 的净值是 ' + net.toFixed(2) + '，但「原值 ' + cost.toFixed(2) + ' − 累计折旧 '
      + acc.toFixed(2) + '」应为 ' + expect.toFixed(2) + '（差 ' + (net - expect).toFixed(2) + '）',
    rec.raw, '这三条恒等式任一不成立，资产负债表上的固定资产原值/累计折旧/净值就对不上。');
}

function checkTotalRow(totals, assets) {
  const out = [];
  if (!totals.length) return out;
  const t = totals[0];
  for (const role of TOTALLED) {
    const claimed = normAmount(t.byRole[role]);
    if (claimed === null) continue;
    let sum = 0;
    let ok = true;
    for (const a of assets) {
      const n = normAmount(a.byRole[role]);
      if (n === null) { ok = false; break; }
      sum += n;
    }
    if (!ok) continue;
    sum = Math.round(sum * 100) / 100;
    if (Math.abs(sum - claimed) <= 0.01) continue;
    out.push(finding('P0', '合计行算错', t.line,
      '合计行的「' + labelOf(role) + '」写的是 ' + claimed.toFixed(2) + '，但各资产相加是 '
        + sum.toFixed(2) + '（差 ' + (claimed - sum).toFixed(2) + '）',
      t.raw, '合计行常是从系统导出后手工改过，改了一处忘了另一处。'));
  }
  return out;
}

function checkDuplicates(assets) {
  const seen = new Map();
  const out = [];
  for (const a of assets) {
    const key = String(a.byRole.code || a.byRole.name || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push(finding('P0', '同一资产出现两行', a.line,
        key + ' 出现了两次（上一次在第 ' + seen.get(key) + ' 行）',
        a.raw, '同一资产两行会导致重复计提折旧，请先确认。'));
    } else seen.set(key, a.line);
  }
  return out;
}

function checkBlanks(assets) {
  const out = [];
  const roles = Object.keys(assets[0] ? assets[0].byRole : {})
    .filter((r) => r !== 'name' && r !== 'code');
  for (const a of assets) {
    if (!String(a.byRole.code || a.byRole.name || '').trim()) {
      out.push(finding('P0', '资产无编号也无名称', a.line, '这一行认不出是哪个资产', a.raw,
        '请确认这一行是否有效。'));
      continue;
    }
    for (const r of roles) {
      const v = a.byRole[r];
      if (isBlank(v)) {
        out.push(finding('P1', '该填没填', a.line,
          who(a) + ' 的「' + labelOf(r) + '」是空的或还是占位符（' + (String(v).trim() || '空') + '）',
          a.raw, '折旧表出现空列，通常是从系统导出时漏选，或模板没替换。'));
      } else {
        const okNum = normAmount(v) !== null || (r === 'residualRate' && normRate(v) !== null);
        if (!okNum) {
          out.push(finding('P1', '数值无法解析', a.line,
            who(a) + ' 的「' + labelOf(r) + '」写作「' + String(v).trim() + '」，不是能计算的数值',
            a.raw, '请确认列是否串位。'));
        }
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
  if (!String(text).trim()) return insufficient(['固定资产台账原文（text）']);
  const t = parseTable(text);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的台账（要能认出「资产名称/编号」+ 至少两个金额列，例如「原值」「本月折旧」「累计折旧」「净值」）',
      '从系统导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.assets.length) return insufficient(['至少一项资产的明细行']);

  const findings = [];
  const notRun = [];
  for (const a of t.assets) {
    const m = checkMonthly(a); if (m) findings.push(m);
    const c = checkAccum(a); if (c) findings.push(c);
    const n = checkNet(a); if (n) findings.push(n);

  }
  for (const f of checkTotalRow(t.totals, t.assets)) findings.push(f);
  for (const f of checkDuplicates(t.assets)) findings.push(f);
  for (const f of checkBlanks(t.assets)) findings.push(f);
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));

  const sumOf = (role) => Math.round(t.assets.reduce((s, a) => {
    const n = normAmount(a.byRole[role]);
    return s + (n === null ? 0 : n);
  }, 0) * 100) / 100;

  const result = {
    findings,
    summary: {
      assets: t.assets.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      cost_total: sumOf('cost'),
      accum_total: sumOf('accum'),
      net_total: sumOf('net'),
      basis: '逐项复核「月折旧 =(原值×(1−残值率))÷(年限×12)」「累计=月折旧×已提月数」「净值=原值−累计」',
    },
    columns: t.cols,
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明这三条恒等式**算得对**，'
      + '不代表折旧年限、残值率选得对，也不代表资产还在 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normAmount, normRate, isBlank, labelOf, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, ROLE_LABELS, RESIDUAL_MIN, RESIDUAL_MAX,
};
