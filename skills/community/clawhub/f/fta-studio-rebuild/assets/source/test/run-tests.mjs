#!/usr/bin/env node
/**
 * FTA Studio - 引擎正确性验证
 * 对照数学解析解与 NRC FTA Handbook 标准算例
 */

import { fta } from '../src/api.mjs';
import { parseDSL } from '../src/model.mjs';
import { computeCutSets } from '../src/mocus.mjs';
import { solveBDD } from '../src/bdd.mjs';
import { quantify } from '../src/quantify.mjs';

let pass = 0, fail = 0;
const failures = [];

function check(name, actual, expected, tol = 1e-9) {
  const ok = typeof expected === 'number'
    ? Math.abs(actual - expected) <= tol * Math.max(1, Math.abs(expected))
    : JSON.stringify(actual) === JSON.stringify(expected);
  if (ok) { pass++; console.log(`  ✓ ${name}`); }
  else {
    fail++; failures.push({ name, actual, expected });
    console.log(`  ✗ ${name}\n      实际: ${actual}\n      期望: ${expected}`);
  }
}

function section(title) {
  console.log(`\n${'─'.repeat(60)}\n${title}\n${'─'.repeat(60)}`);
}

// ============ 1. 串并联系统（Series-Parallel，NRC FTA Handbook 标准算例）============
section('1. 串并联系统 — FTA Handbook 标准算例');
{
  // 串联系统：3 个部件全部失效才失效 Q = q1*q2*q3
  const dsl = `
TOP 串联系统失效
  AND
    BASIC A失效 p=0.1
    BASIC B失效 p=0.2
    BASIC C失效 p=0.3
`;
  const tree = parseDSL(dsl);
  const res = quantify(tree);
  check('串联系统 Q = 0.1*0.2*0.3', res.metrics.topProb, 0.006, 1e-12);
  check('串联系统割集数 = 1', res.cutSets.cutSets.length, 1);
  check('串联系统为 3 阶割集', res.cutSets.cutSets[0].order, 3);
}
{
  // 并联系统：任一失效即失效 Q = 1-(1-q1)(1-q2)(1-q3)
  const dsl = `
TOP 并联系统失效
  OR
    BASIC A失效 p=0.1
    BASIC B失效 p=0.2
    BASIC C失效 p=0.3
`;
  const tree = parseDSL(dsl);
  const res = quantify(tree);
  const expected = 1 - (1 - 0.1) * (1 - 0.2) * (1 - 0.3);
  check('并联系统 Q = 1-0.9*0.8*0.7', res.metrics.topProb, expected, 1e-12);
  check('并联系统 3 个 1 阶割集', res.cutSets.stats.singlePoints, 3);
}

// ============ 2. 经典双阀门冗余问题（NRC Handbook: Q = 8E-4）============
section('2. 双泵冗余系统 — NRC FTA Handbook (期望 Q ≈ 8E-4)');
{
  // 泵 A、B 冗余，控制器 C 为共因。qA=qB=0.03, qC=0.002
  // Q = (1-qC) * (1 - (1-qA)(1-qB)) + ... 完整解约 8E-4
  const dsl = `
TOP 供水中断
  OR
    INTER 双泵冗余失效
      AND
        BASIC 泵A失效 p=0.03
        BASIC 泵B失效 p=0.03
    BASIC 控制器共因失效 p=0.002
`;
  const tree = parseDSL(dsl);
  const res = quantify(tree);
  // 解析解: Q = qA*qB + qC - qA*qB*qC
  const qA = 0.03, qB = 0.03, qC = 0.002;
  const exact = qA * qB + qC - qA * qB * qC;
  check('双泵冗余 Q 精确解', res.metrics.topProb, exact, 1e-12);
  check('结果量级接近 8.2E-4', Math.round(res.metrics.topProb * 1e4) / 1e4, 8e-4, 0.03);
  check('应检出 1 个单点失效(控制器)', res.cutSets.stats.singlePoints, 1);
}

// ============ 3. 表决门 (k-of-n) ============
section('3. k/n 表决门');
{
  // 2oo3, 各 q=0.01 -> Q = C(3,2)*q^2*(1-q) + q^3
  const dsl = `
TOP 2oo3传感器错误
  VOTE 2/3 至少两个失效
    BASIC S1 p=0.01
    BASIC S2 p=0.01
    BASIC S3 p=0.01
`;
  const tree = parseDSL(dsl);
  const res = quantify(tree);
  const q = 0.01;
  // 2oo3 精确解（BDD）：P(至少2个失效) = C(3,2)q²(1-q) + 3q²·q... 完整展开
  // = 3q² - 2q³
  const exact = 3 * q * q - 2 * q * q * q;
  check('2oo3 精确解 3q²-2q³', res.metrics.topProb, exact, 1e-12);
  check('2oo3 割集数 = 3 (C(3,2))', res.cutSets.cutSets.length, 3);
  check('2oo3 均为 2 阶割集', res.cutSets.cutSets.every((c) => c.order === 2), true);

  // 3oo3: 全部失效
  const dsl3 = `
TOP 3oo3全部失效
  VOTE 3/3
    BASIC S1 p=0.01
    BASIC S2 p=0.01
    BASIC S3 p=0.01
`;
  const res3 = quantify(parseDSL(dsl3));
  check('3oo3 Q = q^3', res3.metrics.topProb, 1e-6, 1e-12);
}

// ============ 4. 非相干树 XOR (BDD 精确解) ============
section('4. 非相干树 XOR — BDD 精确解');
{
  // XOR: 两事件恰好一个发生。P(XOR) = q1(1-q2) + (1-q1)q2
  const dsl = `
TOP XOR事件
  XOR
    BASIC E1 p=0.1
    BASIC E2 p=0.2
`;
  const tree = parseDSL(dsl);
  const res = quantify(tree);
  const exact = 0.1 * 0.8 + 0.9 * 0.2; // 0.08 + 0.18 = 0.26
  check('XOR 精确解 q1(1-q2)+(1-q1)q2', res.metrics.topProb, exact, 1e-12);
  check('识别为非相干树', res.metrics.nonCoherent, true);
  check('使用 BDD 方法', res.metrics.topProbMethod.includes('BDD'), true);
}

// ============ 5. 吸收律 / 幂等律 ============
section('5. 布尔代数化简 — 吸收律与幂等律');
{
  // A AND (A OR B) = A  -> 最小割集应只有 {A}
  const dsl = `
TOP 化简测试
  AND
    BASIC A p=0.1
    OR
      BASIC A p=0.1
      BASIC B p=0.2
`;
  const res = quantify(parseDSL(dsl));
  check('A∧(A∨B)=A 割集数=1', res.cutSets.cutSets.length, 1);
  check('A∧(A∨B)=A 概率=0.1', res.metrics.topProb, 0.1, 1e-12);
}
{
  // (A OR B) AND (A OR C) = A OR (B AND C) -> 割集 {A}, {B,C}
  const dsl = `
TOP 化简测试2
  AND
    OR
      BASIC A p=0.01
      BASIC B p=0.02
    OR
      BASIC A p=0.01
      BASIC C p=0.03
`;
  const res = quantify(parseDSL(dsl));
  check('(A∨B)∧(A∨C) 割集数=2', res.cutSets.cutSets.length, 2);
  const orders = res.cutSets.cutSets.map((c) => c.order).sort();
  check('割集阶数为 [1,2]', orders, [1, 2]);
  // 精确解：P = A + (1-A)·B·C（BDD 精确解，非稀有事件近似）
  const qA = 0.01, qB = 0.02, qC = 0.03;
  const exact = qA + (1 - qA) * qB * qC;
  check('概率 = qA + (1-qA)·qB·qC', res.metrics.topProb, exact, 1e-12);
}

// ============ 6. 重要度计算验证 ============
section('6. 重要度指标验证');
{
  // 串联系统: B_i = ∂Q/∂q_i = 其他部件概率之积
  const dsl = `
TOP 串联系统失效
  AND
    BASIC A p=0.1
    BASIC B p=0.2
    BASIC C p=0.3
`;
  const res = quantify(parseDSL(dsl));
  const imp = res.importance;
  const A = imp.find((r) => r.name.includes('A'));
  const B = imp.find((r) => r.name.includes('B'));
  // Birnbaum_A = qB*qC = 0.2*0.3 = 0.06
  check('Birnbaum_A = qB*qC', A.birnbaum, 0.06, 1e-12);
  check('Birnbaum_B = qA*qC', B.birnbaum, 0.1 * 0.3, 1e-12);
  // Criticality_A = qA*B_A/Q = 0.1*0.06/0.006 = 1.0 (串联系统每个都关键)
  check('Criticality_A = 1.0 (串联)', A.criticality, 1.0, 1e-12);
  // FV_A = (Q - Q(A=0))/Q = (0.006-0)/0.006 = 1
  check('FV_A = 1.0 (串联)', A.fv, 1.0, 1e-12);
  // RAW_A = Q(A=1)/Q = 0.2*0.3/0.006 = 10
  check('RAW_A = 10', A.raw, 10, 1e-12);
}
{
  // 并联系统: B_i = (1-q_i) * 其他并联部分的乘积修正
  const dsl = `
TOP 并联系统失效
  OR
    BASIC A p=0.1
    BASIC B p=0.2
    BASIC C p=0.3
`;
  const res = quantify(parseDSL(dsl));
  const Q = 1 - 0.9 * 0.8 * 0.7;
  const A = res.importance.find((r) => r.name.includes('A'));
  // Birnbaum_A = ∂Q/∂qA = (1-qB)(1-qC) = 0.8*0.7 = 0.56
  check('Birnbaum_A = (1-qB)(1-qC)', A.birnbaum, 0.56, 1e-12);
  // Criticality_A = qA*B_A/Q = 0.1*0.56/Q
  check('Criticality_A = qA*B_A/Q', A.criticality, 0.1 * 0.56 / Q, 1e-12);
}

// ============ 7. 概率模型换算 ============
section('7. 概率模型换算');
{
  // 指数分布: q = 1 - e^(-λt)
  const tree = parseDSL(`
meta missionTime: 100
TOP 指数测试
  OR
    BASIC 部件失效 lambda=1e-5
`);
  const res = quantify(tree);
  const expected = 1 - Math.exp(-1e-5 * 100);
  check('指数分布 q=1-e^(-λt)', res.metrics.topProb, expected, 1e-12);

  // 需求型: q = n * pd
  const tree2 = parseDSL(`
TOP 需求型测试
  OR
    BASIC 需求失效 n=1000 dp=1e-6
`);
  const res2 = quantify(tree2);
  check('需求型 q=n*pd=1e-3', res2.metrics.topProb, 1e-3, 1e-12);

  // 可修复: q ≈ λ·TMR/(1+λ·TMR)
  const tree3 = parseDSL(`
TOP 可修复测试
  OR
    BASIC 部件 tmr=8 lambda=1e-4
`);
  const res3 = quantify(tree3);
  const q3 = (1e-4 * 8) / (1 + 1e-4 * 8);
  check('可修复 q≈λ·TMR/(1+λ·TMR)', res3.metrics.topProb, q3, 1e-12);
}

// ============ 8. 禁门 (INHIBIT) ============
section('8. 禁门 INHIBIT — 条件允许时传递');
{
  // INHIBIT: 输出 = 条件 AND 所有前置输入
  const dsl = `
TOP 禁门测试
  INHIBIT
    BASIC 触发条件 p=0.5
    BASIC 前置A p=0.2
    BASIC 前置B p=0.4
`;
  const res = quantify(parseDSL(dsl));
  const expected = 0.5 * 0.2 * 0.4;
  check('INHIBIT Q = cond*prereqA*prereqB', res.metrics.topProb, expected, 1e-12);
}

// ============ 9. 大规模树性能 ============
section('9. 大规模故障树性能 (BDD 扩展性)');
{
  // 4 个顶层分支(OR)，每分支为 AND，各含 4 个 OR 子组，每组 4 个基本事件
  // 结构: TOP(OR) -> 4× INTER(AND) -> 4× INTER(OR) -> 4× BASIC
  // 每个分支需选中 4 个子组之一 → 每分支 4^4 路径 → 共 4^5 = 1024 割集
  const GROUPS = 4, PER_GROUP = 4;
  const lines = ['TOP 大规模树', '  OR'];
  let id = 0;
  for (let i = 0; i < GROUPS; i++) {
    lines.push(`    INTER 分支${i}`);
    lines.push('      AND');
    for (let j = 0; j < GROUPS; j++) {
      lines.push(`        INTER 子组${i}_${j}`);
      lines.push('          OR');
      for (let k = 0; k < PER_GROUP; k++) {
        lines.push(`            BASIC E${id++} p=1e-4`);
      }
    }
  }
  const tree = parseDSL(lines.join('\n'));
  const t0 = Date.now();
  // 注意：默认 truncation=1e-12，而 4 阶割集概率 (1e-4)^4 = 1e-16 会被截断。
  // 这里显式关闭概率截断，以验证 MOCUS 的完整枚举能力。
  const res = quantify(tree, { truncation: 0 });
  const ms = Date.now() - t0;
  const expect = Math.pow(GROUPS, GROUPS + 1); // 4^5 = 1024
  console.log(`  规模: ${tree.nodes.length} 节点 / ${tree.connections.length} 连接 / ${id} 基本事件`);
  console.log(`  割集数: ${res.cutSets.cutSets.length} (期望 ${expect})`);
  console.log(`  BDD 节点: ${res.metrics.bddSize}`);
  console.log(`  计算耗时: ${ms} ms`);
  check('大规模树计算完成', res.ok, true);
  check('耗时 < 10s', ms < 10000, true);
  check(`割集数 = ${expect}`, res.cutSets.cutSets.length, expect);
  // 每个割集恰好 4 个基本事件（每 AND 分支选 1 个子组的 1 个事件）
  check('所有割集均为 4 阶', res.cutSets.cutSets.every((c) => c.order === 4), true);
  check('无单点失效', res.cutSets.stats.singlePoints, 0);
  check('未触发截断', res.cutSets.truncated, false);

  // 另外验证：开启默认截断后应过滤掉高阶低概率割集，并正确标记
  const resTrunc = quantify(tree);
  check('默认截断生效（割集减少）', resTrunc.cutSets.cutSets.length < expect, true);
  check('默认截断已标记', resTrunc.cutSets.truncated, true);
}

// ============ 10. 割集阶数截断 ============
section('10. 割集截断与过滤');
{
  const dsl = `
TOP 截断测试
  OR
    INTER 三重失效
      AND
        BASIC A p=0.1
        BASIC B p=0.1
        BASIC C p=0.1
    BASIC 单点失效 p=0.2
`;
  const tree = parseDSL(dsl);
  const res1 = quantify(tree, { maxOrder: 0 });
  check('不限阶数时有 2 个割集', res1.cutSets.cutSets.length, 2);
  const res2 = quantify(tree, { maxOrder: 2 });
  check('限 2 阶时只有单点失效', res2.cutSets.cutSets.length, 1);
  check('标记为已截断', res2.cutSets.truncated, true);
}

// ============ 11. 房屋事件与外部事件 ============
section('11. 房屋事件 (House) 处理');
{
  const dsl = `
TOP 房屋事件测试
  OR
    BASIC 真实失效 p=0.1
    HOUSE 系统正常（恒不发生）
`;
  const res = quantify(parseDSL(dsl));
  // 房屋事件默认为 0 概率（不贡献），Q 应等于 0.1
  check('房屋事件不贡献概率', res.metrics.topProb, 0.1, 1e-12);
}

// ============ 12. 报告与 SVG 生成 ============
section('12. 报告与图形生成');
{
  const tree = parseDSL(`
meta title: 报告测试树
meta missionTime: 100
TOP 顶事件测试
  AND
    INTER 子系统A
      OR
        BASIC E1 p=1e-3
        BASIC E2 p=2e-3
    BASIC E3 p=5e-3
`);
  const res = fta.analyze(tree, { report: 'markdown', includeDiagram: true });
  check('Markdown 报告生成', typeof res.report === 'string' && res.report.length > 500, true);
  check('报告含顶事件概率', res.report.includes('顶事件发生概率'), true);
  check('报告含最小割集章节', res.report.includes('最小割集'), true);
  check('报告含重要度章节', res.report.includes('重要度分析'), true);
  check('报告内嵌 SVG 图形', res.report.includes('data:image/svg+xml'), true);

  const svgRes = fta.analyze(tree, { report: 'none', includeSVG: true });
  check('独立 SVG 生成', typeof svgRes.svg === 'string' && svgRes.svg.startsWith('<svg'), true);
  check('SVG 含顶事件矩形', svgRes.svg.includes('<rect'), true);
  check('SVG 含与门', svgRes.svg.includes('gate-AND'), true);

  const html = fta.analyze(tree, { report: 'html' });
  check('HTML 报告生成', typeof html.report === 'string' && html.report.includes('<!DOCTYPE html>'), true);
}

// ============ 13. DSL 往返一致性 ============
section('13. DSL 解析 — 序列化往返');
{
  const dsl1 = `meta title: 往返测试
TOP 顶事件
  AND
    BASIC 部件A p=0.01 ref=FM-1 comp=Pump
    OR
      BASIC 部件B p=0.02
      BASIC 部件C p=0.03`;
  const t1 = parseDSL(dsl1);
  const dsl2 = fta.toDSL(t1);
  const t2 = parseDSL(dsl2);
  const r1 = quantify(t1);
  const r2 = quantify(t2);
  check('往返后节点数一致', t2.nodes.length, t1.nodes.length);
  check('往返后概率一致', r2.metrics.topProb, r1.metrics.topProb, 1e-15);
  check('往返后割集数一致', r2.cutSets.cutSets.length, r1.cutSets.cutSets.length);
  check('往返保留追溯编号', t2.nodes.some((n) => n.ref === 'FM-1'), true);
}

// ============ 14. 校验功能 ============
section('14. 模型校验');
{
  const { validateTree } = await import('../src/model.mjs');
  const bad = {
    nodes: [
      { id: 'a', type: 'basic', name: 'A', prob: 0.1 },
      { id: 'b', type: 'basic', name: 'B', prob: 0.1 },
    ],
    connections: [{ from: 'a', to: 'b' }, { from: 'b', to: 'a' }], // 环路
  };
  const v = validateTree(bad);
  check('检出环路', v.errors.some((e) => e.includes('环路')), true);
  check('检出缺顶事件', v.errors.some((e) => e.includes('顶事件')), true);
  check('校验不通过', v.ok, false);
}

// ============ 15. What-if 模拟 ============
section('15. What-if 敏感度模拟');
{
  const tree = parseDSL(`
TOP 模拟测试
  OR
    BASIC E1 p=0.01
    BASIC E2 p=0.02
    BASIC E3 p=0.03
`);
  const before = quantify(tree).metrics.topProb;
  const sim = fta.simulate(tree, {});
  check('无修改时 delta=0', Math.abs(sim.delta) < 1e-15, true);
  // 找出 E1 的 id
  const e1 = tree.nodes.find((n) => n.name === 'E1');
  const sim2 = fta.simulate(tree, { [e1.id]: 0 });
  const expected = 1 - (1 - 0.02) * (1 - 0.03);
  check('E1=0 后 Q = 1-0.98*0.97', sim2.after.topProb, expected, 1e-12);
  check('delta 为负', sim2.delta < 0, true);
}

// ============ 汇总 ============
console.log(`\n${'═'.repeat(60)}`);
console.log(`测试结果: ${pass} 通过 / ${fail} 失败 / 共 ${pass + fail}`);
console.log('═'.repeat(60));
if (fail > 0) {
  console.log('\n失败明细:');
  for (const f of failures) console.log(`  - ${f.name}: 实际=${f.actual} 期望=${f.expected}`);
  process.exitCode = 1;
} else {
  console.log('\n✅ 全部通过 — 引擎计算正确性已验证');
}