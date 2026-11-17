/**
 * finance-monthly-selfcheck.js —— 财务月度自查包（free档；每个检查复用仓库里已有的免费引擎）
 *
 * 输入：分段文本，每段以 `=== 检查名 ===` 开头，例如
 *   === 银行流水对账 ===
 *   <把该检查要求的表贴进来>
 *
 * 自包含：只用 Node 标准库，不联网；材料不足**绝不给结论**。
 */
'use strict';
const ENGINES = {
  "应付账款账龄": require('./parts/01.js'),
  "预缴企业所得税": require('./parts/02.js'),
  "差旅费标准": require('./parts/03.js'),
};

const BUNDLE_CHECKS = ["应付账款账龄", "预缴企业所得税", "差旅费标准"];
const CHECKS_GIVEN = BUNDLE_CHECKS.map((c) => `${c}（分段核对）`);
const CHECKS_WITHHELD = ["现金盘点差异", "发票领用存"];
const OUT_OF_SCOPE = [
  '替代做账或出具鉴证意见（只做表内/表间算术与勾稽核对）',
  '读取 ERP/财务系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = "=== 应付账款账龄 ===\n供应商\t应付余额\t其中逾期金额\t逾期天数\t计划付款金额\t本期实付\n豫州建材有限公司\t380000.00\t0.00\t0\t300000.00\t300000.00\n中岳设备租赁有限公司\t120000.00\t120000.00\t45\t60000.00\t60000.00\n豫通物流有限公司\t45000.00\t0.00\t0\t45000.00\t45000.00\n合计\t545000.00\t120000.00\t\t405000.00\t405000.00\n\n=== 预缴企业所得税 ===\n所属期\t利润总额\t税率\t应预缴所得税额\t已预缴所得税额\t本期应补(退)税额\t累计应预缴所得税额\t累计已预缴所得税额\n2026-Q1\t1000000.00\t25%\t250000.00\t200000.00\t50000.00\t250000.00\t200000.00\n2026-Q2\t800000.00\t25%\t200000.00\t250000.00\t-50000.00\t450000.00\t450000.00\n2026-Q3\t1200000.00\t25%\t300000.00\t280000.00\t20000.00\t750000.00\t730000.00\n合计\t3000000.00\t\t750000.00\t730000.00\t20000.00\n\n=== 差旅费标准 ===\n姓名\t行程\t出差起止日期\t出差天数\t住宿费\t住宿费标准上限\t交通费\t交通费标准上限\t伙食补助\t伙食补助日标准\t其他费用\t报销合计\t超标金额\t审批\n张伟\t北京-上海\t2026-03-02 至 2026-03-06\t5\t2000.00\t2500.00\t1200.00\t1500.00\t500.00\t100.00\t300.00\t4000.00\t0.00\t已审批\n李娜\t广州-深圳\t2026-03-10 至 2026-03-13\t4\t1200.00\t1500.00\t600.00\t800.00\t400.00\t100.00\t0.00\t2200.00\t0.00\t已审批\n合计\t\t\t9\t3200.00\t4000.00\t1800.00\t2300.00\t900.00\t\t300.00\t6200.00\t0.00";

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
