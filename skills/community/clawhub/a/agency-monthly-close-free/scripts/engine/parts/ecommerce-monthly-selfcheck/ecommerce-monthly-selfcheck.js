/**
 * ecommerce-monthly-selfcheck.js —— 电商财务月度自查包（free档；每个检查复用仓库里已有的免费引擎）
 *
 * 输入：分段文本，每段以 `=== 检查名 ===` 开头，例如
 *   === 银行流水对账 ===
 *   <把该检查要求的表贴进来>
 *
 * 自包含：只用 Node 标准库，不联网；材料不足**绝不给结论**。
 */
'use strict';
const ENGINES = {
  "电商平台结算核对": require('./parts/01.js'),
  "促销补贴与核销核对": require('./parts/02.js'),
  "直播佣金与坑位费结算核对": require('./parts/03.js'),
};

const BUNDLE_CHECKS = ["电商平台结算核对", "促销补贴与核销核对", "直播佣金与坑位费结算核对"];
const CHECKS_GIVEN = BUNDLE_CHECKS.map((c) => `${c}（分段核对）`);
const CHECKS_WITHHELD = ["电商退货退款与货款结算核对", "广告代理返点与框架返点核对"];
const OUT_OF_SCOPE = [
  '替代做账或出具鉴证意见（只做表内/表间算术与勾稽核对）',
  '读取 ERP/财务系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = "=== 电商平台结算核对 ===\n订单号\t商品销售额\t平台佣金\t技术服务费\t运费\t退款\t结算金额\nSO-001\t1000.00\t50.00\t10.00\t8.00\t0.00\t932.00\nSO-002\t2000.00\t100.00\t20.00\t0.00\t200.00\t1680.00\nSO-003\t500.00\t25.00\t5.00\t8.00\t0.00\t462.00\n合计\t3500.00\t175.00\t35.00\t16.00\t200.00\t3074.00\n\n=== 促销补贴与核销核对 ===\n活动\tSKU\t实际销量\t单件补贴\t应结补贴\t活动封顶\t已结补贴\t差异\n618大促\tA-100\t2000\t5.00\t10000.00\t20000.00\t10000.00\t0.00\n618大促\tB-200\t1500\t8.00\t12000.00\t20000.00\t12000.00\t0.00\n合计\t\t3500\t\t22000.00\t\t22000.00\t0.00\n\n=== 直播佣金与坑位费结算核对 ===\n结算期间\t直播场次\t达人名称\t结算GMV\t佣金率\t应付佣金\t坑位费\t退货扣减\t实际应付\t合同佣金率\t备注\n2026-01\tLC-2026-0101-A\t星野小满\t200000.00\t20%\t40000.00\t30000.00\t12000.00\t58000.00\t20%\t首场专场\n2026-01\tLC-2026-0101-A\t阿凯说车\t150000.00\t15%\t22500.00\t20000.00\t5000.00\t37500.00\t15%\t\n2026-02\tLC-2026-0205-B\t星野小满\t180000.00\t20%\t36000.00\t30000.00\t9000.00\t57000.00\t20%\t返场\n2026-02\tLC-2026-0205-B\t阿凯说车\t120000.00\t15%\t18000.00\t0.00\t3000.00\t15000.00\t15%\t纯佣合作无保底\n合计\t\t\t650000.00\t\t116500.00\t80000.00\t29000.00\t167500.00";

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
