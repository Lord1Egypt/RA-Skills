/**
 * manufacturing-monthly-selfcheck.js —— 制造业月度自查包（free档；每个检查复用仓库里已有的免费引擎）
 *
 * 输入：分段文本，每段以 `=== 检查名 ===` 开头，例如
 *   === 银行流水对账 ===
 *   <把该检查要求的表贴进来>
 *
 * 自包含：只用 Node 标准库，不联网；材料不足**绝不给结论**。
 */
'use strict';
const ENGINES = {
  "生产投入产出与报废率核对": require('./parts/01.js'),
  "材料领用与定额损耗核对": require('./parts/02.js'),
  "存货出入库与加权平均成本核对": require('./parts/03.js'),
};

const BUNDLE_CHECKS = ["生产投入产出与报废率核对", "材料领用与定额损耗核对", "存货出入库与加权平均成本核对"];
const CHECKS_GIVEN = BUNDLE_CHECKS.map((c) => `${c}（分段核对）`);
const CHECKS_WITHHELD = ["委外加工费与损耗核对", "材料成本差异分摊核对"];
const OUT_OF_SCOPE = [
  '替代做账或出具鉴证意见（只做表内/表间算术与勾稽核对）',
  '读取 ERP/财务系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = "=== 生产投入产出与报废率核对 ===\n工单号\t期间\t工序\t投入量\t完工量\t报废量\t期末在制\t良率\t报废率\nMO-2606-001\t2026-06-01\t下料\t1000.00\t980.00\t20.00\t0.00\t98%\t2%\nMO-2606-001\t2026-06-01\t机加工\t980.00\t960.40\t19.60\t0.00\t98%\t2%\nMO-2606-002\t2026-06-01\t装配\t500.00\t495.00\t5.00\t0.00\t99%\t1%\nMO-2606-003\t2026-06-02\t下料\t1200.00\t1188.00\t12.00\t0.00\t99%\t1%\n合计\t\t\t3680.00\t3623.40\t56.60\t0.00\n\n=== 材料领用与定额损耗核对 ===\n期间\t材料名称\t计量单位\t工程量\t工程量单位\t定额单位\t单位定额\t定额用量\t领用量\t损耗量\t损耗率\t单价\t金额\n2026-01\t螺纹钢 HRB400\t吨\t1200\tm³\tm³\t0.085\t102.00\t104.50\t2.50\t2.39%\t3800.00\t397100.00\n2026-02\t螺纹钢 HRB400\t吨\t980\tm³\tm³\t0.085\t83.30\t84.00\t0.70\t0.83%\t3850.00\t323400.00\n2026-03\t螺纹钢 HRB400\t吨\t1400\tm³\tm³\t0.085\t119.00\t124.00\t5.00\t4.03%\t3800.00\t471200.00\n2026-03\t商品混凝土 C30\tm³\t1400\tm³\tm³\t1.015\t1421.00\t1445.00\t24.00\t1.66%\t460.00\t664700.00\n合计\t\t\t\t\t\t\t1725.30\t1757.50\t32.20\t\t\t1856400.00\n\n=== 存货出入库与加权平均成本核对 ===\n存货名称\t期初数量\t期初金额\t入库数量\t入库金额\t出库数量\t出库金额\t期末数量\t期末金额\n螺纹钢HRB400\t120.00\t480000.00\t80.00\t336000.00\t150.00\t612000.00\t50.00\t204000.00\n水泥P.O42.5\t200.00\t90000.00\t100.00\t46000.00\t180.00\t81600.00\t120.00\t54400.00\n合计\t\t570000.00\t\t382000.00\t\t693600.00\t\t258400.00";

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
