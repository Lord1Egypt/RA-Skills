/**
 * hr-monthly-selfcheck.js —— 人力资源月度自查包（free档；每个检查复用仓库里已有的免费引擎）
 *
 * 输入：分段文本，每段以 `=== 检查名 ===` 开头，例如
 *   === 银行流水对账 ===
 *   <把该检查要求的表贴进来>
 *
 * 自包含：只用 Node 标准库，不联网；材料不足**绝不给结论**。
 */
'use strict';
const ENGINES = {
  "工资表代扣与个税社保申报核对": require('./parts/01.js'),
  "工资个税累计预扣核对": require('./parts/02.js'),
  "社保公积金缴费基数核对": require('./parts/03.js'),
};

const BUNDLE_CHECKS = ["工资表代扣与个税社保申报核对", "工资个税累计预扣核对", "社保公积金缴费基数核对"];
const CHECKS_GIVEN = BUNDLE_CHECKS.map((c) => `${c}（分段核对）`);
const CHECKS_WITHHELD = ["加班费核算核对", "职工福利费与教育经费限额核对"];
const OUT_OF_SCOPE = [
  '替代做账或出具鉴证意见（只做表内/表间算术与勾稽核对）',
  '读取 ERP/财务系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = "=== 工资表代扣与个税社保申报核对 ===\n姓名\t工资表应发\t代扣个税\t代扣社保个人部分\t个税申报税额\t社保申报个人额\n王建国\t18000.00\t890.00\t1980.00\t890.00\t1980.00\n李海涛\t12500.00\t340.00\t1375.00\t340.00\t1375.00\n赵春燕\t9800.00\t96.00\t1078.00\t96.00\t1078.00\n合计\t40300.00\t1326.00\t4433.00\t1326.00\t4433.00\n\n=== 工资个税累计预扣核对 ===\n姓名\t累计收入\t累计减除费用\t累计专项扣除\t累计专项附加扣除\t累计应纳税所得额\t累计应纳税额\t已预扣税额\t本期应预扣\n张三\t120000.00\t30000.00\t12000.00\t9000.00\t69000.00\t4380.00\t2100.00\t2280.00\n李四\t90000.00\t30000.00\t9000.00\t6000.00\t45000.00\t1980.00\t900.00\t1080.00\n合计\t210000.00\t60000.00\t21000.00\t15000.00\t114000.00\t6360.00\t3000.00\t3360.00\n\n=== 社保公积金缴费基数核对 ===\n期间\t姓名\t工资口径\t单位缴费基数\t个人缴费基数\t单位比例\t个人比例\t单位缴费\t个人缴费\t基数下限\t基数上限\t补缴金额\t基数差额\n2026-01\t张三\t10000.00\t10000.00\t10000.00\t27%\t10.5%\t2700.00\t1050.00\t5000.00\t35000.00\t0.00\t0.00\n2026-01\t李四\t15000.00\t15000.00\t15000.00\t27%\t10.5%\t4050.00\t1575.00\t5000.00\t35000.00\t0.00\t0.00\n2026-02\t张三\t10000.00\t10000.00\t10000.00\t27%\t10.5%\t2700.00\t1050.00\t5000.00\t35000.00\t0.00\t0.00\n合计\t\t35000.00\t35000.00\t35000.00\t\t\t9450.00\t3675.00\t\t\t0.00\t0.00";

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
