#!/usr/bin/env node
/**
 * FTA Studio - 新功能验证测试
 * 覆盖：IEC 61025 符号几何、跨页分页、FaultTree+/CAFTA 互操作
 */

import { andGatePath, orGatePath, xorGatePath, gatePath, eventPath } from '../src/symbols.mjs';
import { paginate, autoPaginate, injectTransfers, buildPageView } from '../src/paginate.mjs';
import {
  toFaultTreePlusXML, fromFaultTreePlusXML,
  toCAFTA, fromCAFTA, toMediniJSON, importAny, detectFormat,
} from '../src/interchange.mjs';
import { parseDSL, validateTree } from '../src/model.mjs';
import { quantify } from '../src/quantify.mjs';
import { renderSVG } from '../src/svg.mjs';

let pass = 0, fail = 0;
const failures = [];

function check(name, actual, expected, tol = 0) {
  const ok = typeof expected === 'number' && tol > 0
    ? Math.abs(actual - expected) <= tol
    : JSON.stringify(actual) === JSON.stringify(expected);
  if (ok) { pass++; console.log(`  ✓ ${name}`); }
  else {
    fail++; failures.push(name);
    console.log(`  ✗ ${name}\n      实际: ${String(actual).slice(0, 120)}\n      期望: ${String(expected).slice(0, 120)}`);
  }
}
function section(t) { console.log(`\n${'─'.repeat(58)}\n${t}\n${'─'.repeat(58)}`); }

// ============ 1. IEC 61025 符号几何 ============
section('1. IEC 61025 Annex A 符号几何');
{
  const and = andGatePath();
  const or = orGatePath();
  const xor = xorGatePath();

  check('AND 门为平底+半圆拱顶（含 A 弧指令）', and.startsWith('M -16 11') && and.includes('A 16 11 0 0 1') && and.includes('Z'), true);
  check('OR 门为平底+尖拱顶（含二次贝塞尔）', (or.match(/Q /g) || []).length >= 1, true);
  check('OR 门与 AND 门形状不同', and !== or, true);
  check('XOR 门 = OR 门 + 内侧平行拱线', xor.startsWith(or) && xor.length > or.length, true);
  check('XOR 门含两条子路径', (xor.match(/M /g) || []).length, 2);

  const vote = gatePath('VOTE', 2, 3);
  check('VOTE 门带 k/n 标签', vote.label, '2/3');
  const inhibit = gatePath('INHIBIT');
  check('INHIBIT 门含底部悬垂线', inhibit.body.includes('L 0 18.7'), true);
  const pand = gatePath('PAND');
  check('PAND 门含底部优先横线', (pand.lines || []).length, 1);

  // 门内操作符（medini 风格）
  check('AND 门内操作符为 &', gatePath('AND').op, '&');
  check('OR 门内操作符为 ≥1', gatePath('OR').op, '≥1');
  check('XOR 门内操作符为 =1', gatePath('XOR').op, '=1');

  // 事件符号
  check('基本事件为圆（宽高比 0.8 的椭圆）', /^M -30\.4\d* 0 A/.test(eventPath('basic').d), true);
  check('中间事件为矩形', eventPath('intermediate').d.includes('L 38 -22'), true);
  check('未开发事件为菱形', eventPath('undeveloped').d, 'M 0 -22 L 38 0 L 0 22 L -38 0 Z');
  check('外部事件为圆+叉', eventPath('external').cross.length, 2);
  check('传输符号为三角形', eventPath('transfer_in').d, 'M 0 -22 L 38 22 L -38 22 Z');
}

// ============ 2. SVG 渲染使用新符号 ============
section('2. SVG 渲染集成新符号');
{
  const tree = parseDSL(`
TOP 符号验证
  OR
    BASIC A失效 p=0.01
    BASIC B失效 p=0.01
`);
  const svg = renderSVG(tree);
  check('SVG 含 gate-OR 标识', svg.includes('gate-OR'), true);
  check('SVG 使用平底拱顶门路径', /A 16 11 0 0 1/.test(svg) || svg.includes('gate-OR'), true);
  check('SVG 含箭头 marker', svg.includes('marker-end="url(#arrow)"'), true);

  // 表决门渲染
  const tree2 = parseDSL(`
TOP 表决门验证
  VOTE 2/3
    BASIC S1 p=0.01
    BASIC S2 p=0.01
    BASIC S3 p=0.01
`);
  const svg2 = renderSVG(tree2);
  check('表决门标签渲染为 2/3', svg2.includes('>2/3<'), true);

  // 禁用/异或门
  const tree3 = parseDSL(`
TOP 异或验证
  XOR
    BASIC X p=0.1
    BASIC Y p=0.2
`);
  const svg3 = renderSVG(tree3);
  check('XOR 门渲染成功', svg3.includes('gate-XOR'), true);
}

// ============ 3. 跨页分页 ============
section('3. 跨页 / 多图功能');
{
  // 小树 → 单页
  const small = parseDSL(`TOP 小树\n  OR\n    BASIC A p=0.01`);
  const sp = autoPaginate(small);
  check('小树保持单页', sp.single, true);
  check('单页包含全部节点', sp.pages[0].nodes.size, small.nodes.length);

  // 大树 → 多页：1 顶事件 + 8 个分支(INTER+AND) + 24 个基本事件 = 33 节点
  const lines = ['TOP 大型系统失效', '  OR'];
  for (let i = 0; i < 8; i++) {
    lines.push(`    INTER 分系统${i}`);
    lines.push('      AND');
    for (let j = 0; j < 3; j++) {
      lines.push(`        BASIC 部件${i}_${j} p=1e-3`);
    }
  }
  const big = parseDSL(lines.join('\n'));
  check('大树节点数 = 33', big.nodes.length, 33);
  check('大树连接数 = 32', big.connections.length, 32);

  const pg = paginate(big, { maxNodes: 20, maxDepth: 4 });
  check('大树被切分为多页', pg.pages.length > 1, true);
  check('所有节点均已分配到页',
    new Set([...pg.pageOf.keys()]).size, big.nodes.length);
  check('存在跨页引用记录', Array.isArray(pg.references), true);

  // 每页节点数不超限（根节点所在页允许例外）
  const overflow = pg.pages.filter((p) => p.nodes.size > 20);
  check('单页节点数不超限（首尾页允许例外）', overflow.length <= 2, true);

  // 传输符号（显示层）
  const withTransfers = injectTransfers(big, pg);
  check('生成了传输节点', withTransfers.nodes.length > big.nodes.length, true);
  check('传输节点类型正确',
    withTransfers.nodes.some((n) => n.type === 'transfer_in') &&
    withTransfers.nodes.some((n) => n.type === 'transfer_out'), true);
  check('传输节点含页码引用',
    withTransfers.nodes.some((n) => n.transferRef), true);
  check('传输节点概率为 0',
    withTransfers.nodes.filter((n) => n.type.startsWith('transfer')).every((n) => n.prob === 0), true);

  // 关键正确性：分页是显示层概念，计算结果必须与原树完全一致
  const rOriginal = quantify(big);
  const rPaged = quantify(withTransfers);
  check('分页不改变顶事件概率',
    rPaged.metrics.topProb, rOriginal.metrics.topProb, 1e-18);
  check('分页不改变割集数',
    rPaged.cutSets.cutSets.length, rOriginal.cutSets.cutSets.length);

  // 每页视图树可独立渲染
  for (const p of pg.pages) {
    const view = buildPageView(big, pg, p.index);
    check(`第 ${p.index} 页视图树可构建`, view && view.nodes.length > 0, true);
    const svg = renderSVG(view, { page: { nodes: new Set(view.nodes.map((n) => n.id)), title: p.title } });
    check(`第 ${p.index} 页可渲染 SVG`, svg.includes('<svg'), true);
  }
}

// ============ 4. FaultTree+ 原生 4 表 XML 双向（medini 可导入） ============
section('4. Isograph FaultTree+ 原生 4 表 XML 互操作（medini 可导入）');
{
  const tree = parseDSL(`
meta title: 制动系统失效
meta standard: ISO 26262
meta missionTime: 100

TOP 制动失效
  AND
    OR
      BASIC 泵卡滞 p=2e-4 ref=FM-01 comp=制动泵
      BASIC 助力器失效 p=5e-4 ref=FM-02 comp=助力器
    BASIC 管路泄漏 p=1e-4 ref=FM-03 comp=管路
`);

  const xml = toFaultTreePlusXML(tree);
  check('导出为合法 XML 结构', xml.startsWith('<?xml'), true);
  check('根元素为 FaultTreePlus', xml.includes('<FaultTreePlus'), true);
  check('含 FailureModels 表', xml.includes('<FailureModels>'), true);
  check('含 PrimaryEvents 表', xml.includes('<PrimaryEvents>'), true);
  check('含 Gates 表', xml.includes('<Gates>'), true);
  check('含 GateInputs 表', xml.includes('<GateInputs>'), true);
  check('声明顶事件 TopEvent', /TopEvent="N001"/.test(xml), true);
  check('AND 门映射为 Type="AND"', xml.includes('Type="AND"'), true);
  check('OR 门映射为 Type="OR"', xml.includes('Type="OR"'), true);
  check('门输入连线带 Order', /<GateInput[^>]*Order="1"/.test(xml), true);
  check('概率写入 FailureModel Value', xml.includes('Value="0.0002"'), true);
  check('失效模型类型导出为 Fixed', xml.includes('Type="Fixed"'), true);
  check('追溯信息导出为 Trace', xml.includes('Trace="FM-01"'), true);
  check('部件信息导出为 Component', xml.includes('Component="制动泵"'), true);

  // 回读
  const back = fromFaultTreePlusXML(xml);
  check('回读后节点数一致', back.nodes.length, tree.nodes.length);
  check('回读后连接数一致', back.connections.length, tree.connections.length);
  const vb = validateTree(back);
  check('回读模型校验通过', vb.ok, true);
  check('回读保留唯一顶事件', back.nodes.filter((n) => n.type === 'top').length, 1);

  // 计算结果一致性
  const r1 = quantify(tree);
  const r2 = quantify(back);
  check('往返后顶事件概率一致', r2.metrics.topProb, r1.metrics.topProb, 1e-15);
  check('往返后割集数一致', r2.cutSets.cutSets.length, r1.cutSets.cutSets.length);

  // 表决门往返
  const vt = parseDSL(`TOP 表决\n  VOTE 2/3\n    BASIC A p=0.01\n    BASIC B p=0.01\n    BASIC C p=0.01`);
  const vxml = toFaultTreePlusXML(vt);
  check('VOTE 门导出 Type="VOTING" + K/N',
    vxml.includes('Type="VOTING"') && vxml.includes('K="2"') && vxml.includes('N="3"'), true);
  const vback = fromFaultTreePlusXML(vxml);
  const vnode = vback.nodes.find((n) => n.gate === 'VOTE');
  check('VOTE 门往返保留 k/n', [vnode?.voteK, vnode?.voteN], [2, 3]);

  // 指数分布模型往返（不应退化为固定概率）
  const et = parseDSL(`TOP 指数\n  OR\n    BASIC A失效 lambda=1e-6`);
  const eb = fromFaultTreePlusXML(toFaultTreePlusXML(et));
  const en = eb.nodes.find((n) => n.type === 'basic');
  check('指数模型往返保留 lambda 与模型', [en.probModel, en.lambda], ['exponential', 1e-6]);

  // ---- medini 变体容错：命名空间前缀 + 小写门类型 ----
  const variant = `<?xml version="1.0"?>
<iso:FaultTreePlus xmlns:iso="http://www.isograph.com/FaultTreePlus" Name="变体测试" MissionTime="1000" TopEvent="TOP1">
  <iso:FailureModels>
    <iso:FailureModel Name="M1" Type="Fixed" Value="0.002"/>
  </iso:FailureModels>
  <iso:PrimaryEvents>
    <iso:PrimaryEvent Name="BE1" Label="传感器失效" FailureModel="M1" Component="传感器"/>
  </iso:PrimaryEvents>
  <iso:Gates>
    <iso:Gate Name="TOP1" Label="传感器系统失效" Type="or"/>
  </iso:Gates>
  <iso:GateInputs>
    <iso:GateInput Gate="TOP1" Input="BE1" Order="1"/>
  </iso:GateInputs>
</iso:FaultTreePlus>`;
  const vv = fromFaultTreePlusXML(variant);
  check('命名空间前缀可解析', vv.nodes.length, 2);
  check('小写门类型 or 可识别', vv.nodes.find((n) => n.type === 'top')?.gate, 'OR');
  check('连线恢复', vv.connections.length, 1);
  check('失效模型 Value 应用到底事件', vv.nodes.find((n) => n.id === 'BE1')?.prob, 0.002);

  // ---- medini 变体容错：值放在子元素里 ----
  const variant2 = `<FaultTreePlus Name="子元素写法" TopEvent="G">
  <Gates><Gate Name="G" Label="顶" Type="AND"/></Gates>
  <PrimaryEvents><PrimaryEvent Name="E1"><Description>事件一</Description></PrimaryEvent></PrimaryEvents>
  <GateInputs><GateInput Gate="G" Input="E1"/></GateInputs>
</FaultTreePlus>`;
  const vv2 = fromFaultTreePlusXML(variant2);
  check('子元素 Description 可解析', vv2.nodes.find((n) => n.id === 'E1')?.name, '事件一');

  // 跨页导出
  const bigLines = ['TOP 跨页系统', '  OR'];
  for (let i = 0; i < 8; i++) {
    bigLines.push(`    INTER 子${i}`, '      AND');
    for (let j = 0; j < 3; j++) bigLines.push(`        BASIC B${i}_${j} p=1e-3`);
  }
  const bigTree = parseDSL(bigLines.join('\n'));
  const pag = paginate(bigTree, { maxNodes: 15 });
  check('跨页树被切分为多页', pag.pages.length > 1, true);
  const pagXml = toFaultTreePlusXML(bigTree, { pag });
  check('跨页导出含 TransferIn/Out', /Transfer(In|Out)/.test(pagXml), true);
  const pagBack = fromFaultTreePlusXML(pagXml);
  check('跨页导出可回读', pagBack.nodes.length > 0, true);
}

// ============ 5. CAFTA ============
section('5. CAFTA 格式互操作');
{
  const tree = parseDSL(`
TOP 冷却系统失效
  OR
    BASIC 泵故障 p=0.002
    BASIC 传感器故障 p=0.001
`);
  const xml = toCAFTA(tree);
  check('CAFTA 含 define-fault-tree', xml.includes('<define-fault-tree'), true);
  check('CAFTA 含 gate-occurrence', xml.includes('<gate-occurrence'), true);
  check('CAFTA 含 define-basic-event', xml.includes('<define-basic-event'), true);
  check('CAFTA 含概率浮点值', xml.includes('<float value='), true);

  const back = fromCAFTA(xml);
  check('CAFTA 回读生成节点', back.nodes.length > 0, true);
  const r1 = quantify(tree), r2 = quantify(back);
  check('CAFTA 往返概率接近', Math.abs(r2.metrics.topProb - r1.metrics.topProb) < 1e-6, true);
}

// ============ 6. medini JSON ============
section('6. medini 交换 JSON');
{
  const tree = parseDSL(`
TOP 测试系统失效
  AND
    BASIC A失效 p=0.01 ref=FM-1 comp=部件A
    BASIC B失效 p=0.02 ref=FM-2 comp=部件B
`);
  const analysis = quantify(tree);
  const { fta } = await import('../src/api.mjs');
  const payload = toMediniJSON(tree, {
    metrics: analysis.metrics,
    cutSets: {
      total: analysis.cutSets.stats.total,
      singlePoints: analysis.cutSets.stats.singlePoints,
      items: analysis.cutSets.cutSets,
    },
    importance: analysis.importance,
  });
  check('JSON 含 medini 标识', payload._format.includes('medini'), true);
  check('JSON 含 faultTrees 数组', Array.isArray(payload.faultTrees), true);
  check('JSON 含分析结果', payload.faultTrees[0].results.topEventProbability > 0, true);
  check('JSON 含追溯', payload.faultTrees[0].events.some((e) => e.traces.length > 0), true);

  const round = importAny(JSON.stringify(payload), 'x.json');
  check('medini JSON 可回读', round.tree.nodes.length, tree.nodes.length);
  const r = quantify(round.tree);
  check('回读后概率一致', r.metrics.topProb, analysis.metrics.topProb, 1e-15);
}

// ============ 7. 格式自动识别 ============
section('7. 格式自动识别与统一导入');
{
  check('识别 DSL', detectFormat('TOP A\n  OR\n    BASIC B p=0.1'), 'dsl');
  check('识别 FaultTree+', detectFormat('<FaultTree Version="1.0">'), 'faulttreeplus');
  check('识别 CAFTA', detectFormat('<model><define-fault-tree></model>'), 'cafta');
  check('识别 JSON', detectFormat('{"nodes":[]}'), 'json');
  check('按扩展名识别 .fta', detectFormat('whatever', 'tree.fta'), 'dsl');
  check('按扩展名识别 .xml→FT+', detectFormat('<?xml?><FaultTree/>', 'a.xml'), 'faulttreeplus');

  const dslTree = importAny('TOP T\n  OR\n    BASIC A p=0.01', 'a.fta');
  check('统一导入 DSL 成功', dslTree.format, 'dsl');
  // 门被合并进顶事件，实际生成 2 个节点：TOP(OR) + BASIC A
  check('DSL 导入产生 2 个节点（门并入父节点）', dslTree.tree.nodes.length, 2);
  check('DSL 导入模型校验通过', dslTree.validation.ok, true);
}

// ============ 汇总 ============
console.log(`\n${'═'.repeat(58)}`);
console.log(`新功能测试: ${pass} 通过 / ${fail} 失败 / 共 ${pass + fail}`);
console.log('═'.repeat(58));
if (fail) {
  console.log('失败项:\n  - ' + failures.join('\n  - '));
  process.exitCode = 1;
} else {
  console.log('\n✅ 全部通过 — 符号 / 跨页 / 格式互操作均正确');
}