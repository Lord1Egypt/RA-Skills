/**
 * export-monthly-selfcheck.js —— 外贸月度自查包（free档；每个检查复用仓库里已有的免费引擎）
 *
 * 输入：分段文本，每段以 `=== 检查名 ===` 开头，例如
 *   === 银行流水对账 ===
 *   <把该检查要求的表贴进来>
 *
 * 自包含：只用 Node 标准库，不联网；材料不足**绝不给结论**。
 */
'use strict';
const ENGINES = {
  "出口退税核算核对": require('./parts/01.js'),
  "出口报关与收汇核销核对": require('./parts/02.js'),
  "外币结算与汇兑损益核对": require('./parts/03.js'),
};

const BUNDLE_CHECKS = ["出口退税核算核对", "出口报关与收汇核销核对", "外币结算与汇兑损益核对"];
const CHECKS_GIVEN = BUNDLE_CHECKS.map((c) => `${c}（分段核对）`);
const CHECKS_WITHHELD = ["出口退税申报单证一致性核对", "进口税费核算核对"];
const OUT_OF_SCOPE = [
  '替代做账或出具鉴证意见（只做表内/表间算术与勾稽核对）',
  '读取 ERP/财务系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = "=== 出口退税核算核对 ===\n报关单号\t出口离岸价\t汇率\t征税率\t退税率\t不得免征和抵扣税额\t免抵退税额\t期末留抵税额\t应退税额\t免抵税额\nA001\t1000000.00\t7.10\t13%\t10%\t213000.00\t710000.00\t500000.00\t500000.00\t210000.00\nB002\t500000.00\t7.10\t13%\t13%\t0.00\t461500.00\t200000.00\t200000.00\t261500.00\n合计\t1500000.00\t\t\t\t213000.00\t1171500.00\t700000.00\t700000.00\t471500.00\n\n=== 出口报关与收汇核销核对 ===\n报关单号\t所属期\t报关金额\t佣金率\t应收外汇\t已收汇\t核销差额\t汇率\nEXP-2026-001\t2026-01\t100000.00\t2%\t98000.00\t98000.00\t0.00\t7.10\nEXP-2026-002\t2026-02\t250000.00\t3%\t242500.00\t242500.00\t0.00\t7.05\nEXP-2026-003\t2026-03\t80000.00\t1.5%\t78800.00\t78800.00\t0.00\t6.95\n合计\t\t430000.00\t\t419300.00\t419300.00\t0.00\n\n=== 外币结算与汇兑损益核对 ===\n单据号\t外币金额\t记账汇率\t记账本位币\t结算汇率\t结算本位币\t汇兑损益\t已收本位币\nINV-001\t10000.00\t7.1000\t71000.00\t7.1500\t71500.00\t500.00\t71500.00\nINV-002\t5000.00\t7.1000\t35500.00\t7.0500\t35250.00\t-250.00\t35250.00\n合计\t15000.00\t\t106500.00\t\t106750.00\t250.00\t106750.00";

function splitSections(text) {
  const out = {};
  let cur = null;
  for (const raw of String(text).split(/\r?\n/)) {
    const m = /^===\s*(.+?)\s*===$/.exec(raw.trim());
    if (m) { cur = m[1].trim(); out[cur] = []; continue; }
    if (cur) out[cur].push(raw);
  }
  const res = {};
  for (const k of Object.keys(out)) res[k] = out[k].join('\n').trim();
  return res;
}

function run(payload) {
  const text = payload && typeof payload.text === 'string' ? payload.text : '';

  if (text.trim().length < 5) {
    return { status: 'insufficient_input',
      missing: ['分段正文（每段以 === 检查名 === 开头）'],
      advice: '把要做核对的表按 `=== 检查名 ===` 分段贴进来；材料不足时本工具不给任何结论。' };
  }
  const secs = splitSections(text);
  const findings = [];
  const perCheck = [];
  for (const name of BUNDLE_CHECKS) {
    const body = secs[name];
    const engine = ENGINES[name];
    if (body === undefined) {          // 整段没给 ⇒ 如实标"缺这一段"
      perCheck.push({ check: name, status: 'missing_section', findings: 0 });
      continue;
    }
    const r = engine.run({ text: body });
    if (r.status !== 'success') {
      perCheck.push({ check: name, status: 'insufficient_input', findings: 0,
        missing: (r.missing || []).slice(0, 3) });
      continue;
    }
    const fs = (r.result.findings || []).map((f) => Object.assign({}, f, { check: name }));
    perCheck.push({ check: name, status: 'ok', findings: fs.length,
      p0: r.result.summary.p0, p1: r.result.summary.p1, p2: r.result.summary.p2 });
    findings.push.apply(findings, fs);
  }
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;
  const sectionsDone = perCheck.filter((c) => c.status === 'ok').length;
  const result = {
    status: 'success',
    service_type: 'FINANCE_MONTHLY_SELFCHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: CHECKS_WITHHELD.slice(),
      sections_done: sectionsDone,
      rows: findings.length,
      periods: sectionsDone,
      executed_locally: true,
      network_used: false,
    },
    findings,
    per_check: perCheck,
    summary: {
      rows: findings.length, periods: sectionsDone,
      total: findings.length, p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: '本版本只执行：' + CHECKS_GIVEN.join('、') + '；未执行的检查项见 scope.checks_not_run。',
    disclaimer: '只核各段表内/表间的算术与勾稽，结论可由第三方用同一份输入复算；不替代鉴证与申报。',
  };

  return { status: 'success', result };
}

module.exports = { run, splitSections, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT };
