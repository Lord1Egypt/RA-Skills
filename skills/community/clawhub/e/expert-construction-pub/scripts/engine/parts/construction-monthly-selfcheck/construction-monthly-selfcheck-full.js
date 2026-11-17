/**
 * construction-monthly-selfcheck.js —— 建筑企业月度自查包（paid档；每个检查复用仓库里已有的免费引擎）
 *
 * 输入：分段文本，每段以 `=== 检查名 ===` 开头，例如
 *   === 银行流水对账 ===
 *   <把该检查要求的表贴进来>
 *
 * 自包含：只用 Node 标准库，不联网；材料不足**绝不给结论**。
 */
'use strict';
const ENGINES = {
  "分包结算与产值核对": require('./parts/01.js'),
  "工程进度款与质保金核对": require('./parts/02.js'),
  "工程产值与进度确认核对": require('./parts/03.js'),
  "建筑工人工资专户发放核对": require('./parts/04.js'),
  "项目挣值分析核对": require('./parts/05.js'),
};

const BUNDLE_CHECKS = ["分包结算与产值核对", "工程进度款与质保金核对", "工程产值与进度确认核对", "建筑工人工资专户发放核对", "项目挣值分析核对"];
const CHECKS_GIVEN = BUNDLE_CHECKS.map((c) => `${c}（分段核对）`);
const CHECKS_WITHHELD = [];
const OUT_OF_SCOPE = [
  '替代做账或出具鉴证意见（只做表内/表间算术与勾稽核对）',
  '读取 ERP/财务系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = "=== 分包结算与产值核对 ===\n期间\t分包单位\t合同额\t已完成产值\t本期产值\t质保金\t代扣款\t本期应付\t累计已付\t未付余额\t累计产值\n2026-01\t中建劳务\t1200000.00\t0.00\t300000.00\t9000.00\t3000.00\t288000.00\t288000.00\t12000.00\t300000.00\n2026-02\t中建劳务\t1200000.00\t300000.00\t400000.00\t12000.00\t4000.00\t384000.00\t672000.00\t28000.00\t700000.00\n2026-02\t宏基分包\t800000.00\t0.00\t200000.00\t6000.00\t2000.00\t192000.00\t100000.00\t100000.00\t200000.00\n合计\t\t3200000.00\t300000.00\t900000.00\t27000.00\t9000.00\t864000.00\t1060000.00\t140000.00\t1200000.00\n\n=== 工程进度款与质保金核对 ===\n标段\t合同金额\t本期完成产值\t累计完成产值\t进度款比例\t本期应付进度款\t质保金比例\t本期扣质保金\t本期实付\nA标段\t5000000.00\t800000.00\t3200000.00\t80%\t640000.00\t3%\t19200.00\t620800.00\nB标段\t3000000.00\t400000.00\t2400000.00\t80%\t320000.00\t5%\t16000.00\t304000.00\n合计\t8000000.00\t1200000.00\t5600000.00\t\t960000.00\t\t35200.00\t924800.00\n\n=== 工程产值与进度确认核对 ===\n项目名称\t期次\t形象进度\t合同额\t本期已完产值\t累计已完产值\t本期计量金额\t累计计量金额\t本期扣款\t本期应付金额\t剩余产值\n滨江路改造工程\t2026-01\t10%\t10000000.00\t1000000.00\t1000000.00\t980000.00\t980000.00\t20000.00\t980000.00\t9020000.00\n滨江路改造工程\t2026-02\t20%\t10000000.00\t1000000.00\t2000000.00\t980000.00\t1960000.00\t20000.00\t980000.00\t8040000.00\n滨江路改造工程\t2026-03\t30%\t10000000.00\t1000000.00\t3000000.00\t980000.00\t2940000.00\t20000.00\t980000.00\t7060000.00\n合计\t\t\t\t3000000.00\t\t2940000.00\t\t60000.00\t2940000.00\n\n=== 建筑工人工资专户发放核对 ===\n所属期间\t项目名称\t工人姓名\t身份证号\t所属班组\t考勤工时\t小时工资\t计件数量\t计件单价\t应发工资\t代扣项合计\t实发工资\t专户代发金额\t代发流水号\t实名制考勤记录\t当地最低工资标准\n2026-03\t幸福家园A区项目\t张建国\t3201**********1234\t钢筋班组\t200\t26.00\t-\t-\t5200.00\t220.00\t4980.00\t4980.00\tDF20260301001\t已实名打卡\t2490.00\n2026-03\t幸福家园A区项目\t李秀兰\t3201**********5678\t钢筋班组\t176\t25.00\t-\t-\t4400.00\t108.00\t4292.00\t4292.00\tDF20260301002\t已实名打卡\t2490.00\n2026-03\t幸福家园A区项目\t王志强\t3201**********9012\t木工班组\t152\t28.00\t-\t-\t4256.00\t56.00\t4200.00\t4200.00\tDF20260301003\t已实名打卡\t2490.00\n合计\t-\t-\t-\t-\t528.00\t-\t-\t-\t13856.00\t384.00\t13472.00\t13472.00\t-\t-\t-\n\n=== 项目挣值分析核对 ===\n工作包\tPV\tEV\tAC\tCV\tSV\tCPI\tSPI\n设计\t100000.00\t100000.00\t95000.00\t5000.00\t0.00\t1.05\t1.00\n采购\t200000.00\t180000.00\t200000.00\t-20000.00\t-20000.00\t0.90\t0.90\n施工\t300000.00\t240000.00\t260000.00\t-20000.00\t-60000.00\t0.92\t0.80\n合计\t600000.00\t520000.00\t555000.00\t-35000.00\t-80000.00";

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
const paid = Boolean(payload && (payload.full || payload.credit || payload.token));
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
      checks: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN.slice(),
      checks_not_run: paid ? [] : CHECKS_WITHHELD.slice(),
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
    note: paid ? '完整档执行全部检查项。' : '本版本只执行：' + CHECKS_GIVEN.join('、') + '；未执行的检查项见 scope.checks_not_run。',
    disclaimer: '只核各段表内/表间的算术与勾稽，结论可由第三方用同一份输入复算；不替代鉴证与申报。',
  };
  if (paid) {
    // 本包结构上做不到的能力：跨检查汇总整改清单（按严重度排序 + 建议动作）
    result.consolidated_actions = findings
      .slice()
      .sort((a, b) => String(a.level).localeCompare(String(b.level)) || (a.line - b.line))
      .map((f, i) => ({ order: i + 1, level: f.level, check: f.check,
                        action: f.message, evidence: f.evidence }));
  }

  return { status: 'success', result };
}

module.exports = { run, splitSections, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT };
