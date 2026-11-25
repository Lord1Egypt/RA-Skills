/**
 * FTA Studio - 报告生成器
 * 生成 Markdown / HTML 格式的完整 FTA 分析报告
 */

import { fmtNum, EVENT_TYPE_LABEL, PROB_MODEL_LABEL, GATE_LABEL } from './model.mjs';
import { renderSVG, svgToDataURI } from './svg.mjs';

/**
 * 生成 Markdown 报告
 * @param {object} tree
 * @param {object} result quantify() 的输出
 * @param {object} opts
 */
export function generateMarkdownReport(tree, result, opts = {}) {
  const meta = tree.meta || {};
  const m = result.metrics || {};
  const L = [];
  const now = new Date().toISOString().slice(0, 19).replace('T', ' ');

  // ============ 封面 / 标题 ============
  L.push(`# 故障树分析报告 (FTA Report)`);
  L.push('');
  L.push(`> **分析对象**：${esc(meta.title || '未命名故障树')}  `);
  L.push(`> **生成时间**：${now}  `);
  L.push(`> **任务时间 (Mission Time)**：${m.missionTime != null ? `${m.missionTime} h` : '未设定'}  `);
  L.push(`> **引用标准**：${meta.standard || 'IEC 61025 / GB/T 7826'}  `);
  L.push(`> **工具**：FTA Studio (对标 Ansys medini analyze FTA 模块)`);
  L.push('');
  if (meta.description) {
    L.push(`**分析描述**：${esc(meta.description)}`);
    L.push('');
  }
  L.push('---');
  L.push('');

  // ============ 1. 概要 ============
  L.push(`## 1. 分析概要 (Executive Summary)`);
  L.push('');
  L.push('| 指标 | 数值 | 说明 |');
  L.push('|---|---|---|');
  L.push(`| 顶事件发生概率 Q(TOP) | **${fmtSci(m.topProb)}** | ${m.topProbMethod || ''} |`);
  L.push(`| 最小割集数量 | ${m.cutSets?.total ?? '-'} | 按阶数分布：${orderDistText(m.cutSets?.byOrder)} |`);
  L.push(`| 单一失效点 (1 阶割集) | **${m.cutSets?.singlePoints ?? 0}** | 一阶割集数为单点失效，需优先消除 |`);
  L.push(`| 系统可靠度 R = 1 - Q | ${fmtSci(m.reliability)} | |`);
  if (m.missionTime != null) {
    const fit = estimateFIT(m);
    L.push(`| 平均失效率 (FIT) | ${fit == null ? '-' : fit.toFixed(2) + ' FIT'} | 基于任务时间折算 (1 FIT = 1e-9/h) |`);
  }
  L.push(`| 树结构类型 | ${m.nonCoherent ? '非相干树 (含 XOR/NOT/INHIBIT)' : '相干树 (Coherent)' } | ${m.nonCoherent ? '已使用 BDD 精确解' : '布尔代数可化简'} |`);
  if (m.bddSize != null) L.push(`| BDD 节点数 | ${m.bddSize} | 二叉决策图规模，反映计算复杂度 |`);
  if (m.truncated) L.push(`| ⚠ 割集截断 | 是 | 已按阶数/概率阈值截断，完整性受限 |`);
  L.push('');
  L.push('---');
  L.push('');

  // ============ 2. 故障树模型 ============
  L.push(`## 2. 故障树模型 (Fault Tree Model)`);
  L.push('');

  // 布尔方程
  const boolEq = treeToBoolean(tree);
  if (boolEq) {
    L.push('### 2.1 布尔结构方程');
    L.push('');
    L.push('```text');
    L.push(boolEq);
    L.push('```');
    L.push('');
  }

  // 图形
  if (opts.includeDiagram !== false) {
    L.push(`### 2.2 故障树图形`);
    L.push('');
    const svg = renderSVG(tree, {
      heatmap: opts.heatmap || {},
      showProb: true,
      mode: 'light',
    });
    if (opts.embedImage !== false) {
      L.push(`![故障树图形](${svgToDataURI(svg)})`);
      L.push('');
    }
    if (opts.svgFile) {
      L.push(`> 矢量图已导出：\`${opts.svgFile}\``);
      L.push('');
    }
  }

  // 事件清单
  L.push(`### 2.3 事件清单`);
  L.push('');
  L.push('| ID | 事件名称 | 类型 | 逻辑门 | 概率 q | 参数说明 | 追溯编号 | 部件 |');
  L.push('|---|---|---|---|---|---|---|---|');
  for (const n of tree.nodes) {
    const gate = n.gate ? (n.gate === 'VOTE' ? `${n.gate}(${n.voteK}/${n.voteN})` : n.gate) : '-';
    const q = n.type === 'basic' || n.type === 'undeveloped'
      ? fmtSci(result.probById?.get?.(n.id) ?? n.prob)
      : '-';
    const params = describeParams(n);
    L.push(`| ${n.id} | ${esc(n.name)} | ${EVENT_TYPE_LABEL[n.type] || n.type} | ${gate} | ${q} | ${params} | ${n.ref || '-'} | ${n.component || '-'} |`);
  }
  L.push('');
  L.push('---');
  L.push('');

  // ============ 3. 定性分析 ============
  L.push(`## 3. 定性分析：最小割集 (Minimal Cut Sets)`);
  L.push('');
  if (!result.cutSets?.cutSets?.length) {
    L.push('> 未生成割集。请检查故障树是否正确定义了顶事件与基本事件。');
    L.push('');
  } else {
    const byOrder = {};
    for (const cs of result.cutSets.cutSets) {
      (byOrder[cs.order] ||= []).push(cs);
    }
    L.push(`共生成 **${result.cutSets.cutSets.length}** 个最小割集，阶数分布：${orderDistText(result.cutSets.stats.byOrder)}`);
    L.push('');
    if (result.cutSets.stats.singlePoints > 0) {
      L.push(`> ⚠ **发现 ${result.cutSets.stats.singlePoints} 个单一失效点（1 阶割集）**：这些基本事件单独发生即导致顶事件，属于系统性单点失效，必须通过设计冗余、增加安全机制或调整架构消除。`);
      L.push('');
    }
    for (const order of Object.keys(byOrder).map(Number).sort((a, b) => a - b)) {
      const list = byOrder[order];
      L.push(`### 3.${order} ${order} 阶割集 (${list.length} 个)`);
      L.push('');
      L.push('| 序号 | 割集构成 | 概率 (稀有事件近似) | 占比 |');
      L.push('|---|---|---|---|');
      for (const cs of list) {
        const p = cs.prob ?? 0;
        const share = m.topProb > 0 ? ((p / m.topProb) * 100).toFixed(1) + '%' : '-';
        L.push(`| #${cs.index} | ${cs.names.map(esc).join(' **∧** ')} | ${fmtSci(p)} | ${share} |`);
      }
      L.push('');
    }
  }
  L.push('---');
  L.push('');

  // ============ 4. 定量分析 ============
  L.push(`## 4. 定量分析 (Quantitative Analysis)`);
  L.push('');
  L.push('### 4.1 顶事件概率');
  L.push('');
  L.push('| 求解方法 | Q(TOP) | 说明 |');
  L.push('|---|---|---|');
  L.push(`| ${m.topProbMethod} | **${fmtSci(m.topProb)}** | 主结果 |`);
  L.push(`| 稀有事件近似 | ${fmtSci(m.rareEventSum)} | 各最小割集概率之和，适用于低概率场景 |`);
  L.push(`| MCUB 上界 | ${fmtSci(m.mcub)} | 最小割集上界 |`);
  if (m.topProbUpper != null && m.topProbUpper > m.topProb) {
    L.push(`| Esary-Proschan 上界 | ${fmtSci(m.topProbUpper)} | ${m.nonCoherent ? '非相干树下界更有效' : '可靠性上界'} |`);
  }
  L.push('');
  L.push('> **方法说明**：BDD（二叉决策图）对布尔函数做规范化唯一表示，对非相干树可给出精确解；稀有事件近似在基本事件概率均很小时（工程上 q < 1e-2）误差可忽略。');
  L.push('');

  // 时间相关
  if (m.missionTime != null) {
    L.push('### 4.2 时间相关分析');
    L.push('');
    L.push(`在任务时间 **${m.missionTime} h** 下：`);
    L.push('');
    L.push('| 项 | 数值 |');
    L.push('|---|---|');
    L.push(`| 顶事件不可用度 Q | ${fmtSci(m.topProb)} |`);
    L.push(`| 顶事件可靠度 R | ${fmtSci(m.reliability)} |`);
    const mtbf = m.topProb > 0 ? 1 / (m.topProb / m.missionTime) : null;
    if (mtbf) L.push(`| 平均故障间隔时间 (MBBF) | ${mtbf.toExponential(3)} h |`);
    L.push('');
  }
  L.push('---');
  L.push('');

  // ============ 5. 重要度分析 ============
  L.push(`## 5. 重要度分析 (Importance Measures)`);
  L.push('');
  if (!result.importance?.length) {
    L.push('> 无基本事件，跳过重要度分析。');
    L.push('');
  } else {
    const top = result.importance.slice(0, 20);
    L.push('| 排名 | 事件名称 | 部件 | 概率 q | Birnbaum | 关键重要度 | Fussell-Vesely | RAW | RRW | 结构重要度 |');
    L.push('|---|---|---|---|---|---|---|---|---|---|');
    for (const r of top) {
      L.push(`| ${r.rank} | ${esc(r.name)} | ${r.component || '-'} | ${fmtSci(r.q)} | ${fmtSci(r.birnbaum)} | ${fmtSci(r.criticality)} | ${fmtSci(r.fv)} | ${fmtSci(r.raw)} | ${Number.isFinite(r.rrw) ? fmtSci(r.rrw) : '∞'} | ${fmtSci(r.structureImportance)} |`);
    }
    L.push('');
    if (result.importance.length > 20) {
      L.push(`> 表格仅显示前 20 项，共 ${result.importance.length} 个基本事件。完整数据见附表或 JSON 导出。`);
      L.push('');
    }
    L.push('**指标定义**：');
    L.push('');
    L.push('- **Birnbaum（概率重要度）** $B_i = \\partial Q(TOP)/\\partial q_i$：表示该基本事件概率变化对顶事件概率的边际影响，量纲为无量纲。适用于"任何部件改进收益相当"的场景。');
    L.push('- **关键重要度 (Criticality)** $I_i = q_i \\cdot B_i / Q(TOP)$：该事件对顶事件概率的实际贡献占比。当 $I_i$ 接近 1 时，仅靠更换该部件几乎可以消除全部风险。');
    L.push('- **Fussell-Vesely** $FV_i = [Q(TOP) - Q(TOP|q_i=0)] / Q(TOP)$：该事件对当前系统风险的实际贡献份额，反映"移除它能降多少风险"。');
    L.push('- **RAW (Risk Achievement Worth)** $RAW_i = Q(TOP|q_i=1)/Q(TOP)$：该事件失效时对顶事件的贡献倍数。');
    L.push('- **RRW (Risk Reduction Worth)** $RRW_i = [Q(TOP)-Q(TOP|q_i=0)]/Q(TOP|q_i=0)$：消除该事件后风险的下降倍数，衡量改进效益。');
    L.push('- **结构重要度** $I^s_i$：仅与树结构有关，反映该事件在逻辑结构上的关键程度（与概率数据无关）。');
    L.push('');

    // 关键发现
    const crit = result.importance.filter((r) => r.criticality > 0.05).slice(0, 5);
    if (crit.length) {
      L.push('**关键发现**：');
      L.push('');
      for (const c of crit) {
        L.push(`- **${esc(c.name)}**（${c.component || '未指定部件'}）关键重要度 ${fmtSci(c.criticality)}，FV=${fmtSci(c.fv)}，移除该失效可使顶事件概率下降约 ${(c.fv * 100).toFixed(1)}%。建议优先针对该部件/失效模式采取改进措施。`);
      }
      L.push('');
    }
  }
  L.push('---');
  L.push('');

  // ============ 6. 敏感性分析 ============
  L.push(`## 6. 敏感性分析 (What-If / Sensitivity)`);
  L.push('');
  if (result.importance?.length) {
    L.push('假设将单个基本事件概率降为 0（完全消除），顶事件概率变化如下：');
    L.push('');
    L.push('| 事件 | 当前 q | Q(TOP|消除) | 风险下降 |');
    L.push('|---|---|---|---|');
    for (const r of result.importance.slice(0, 10)) {
      const drop = m.topProb > 0 ? (1 - r.pWithout / m.topProb) : 0;
      L.push(`| ${esc(r.name)} | ${fmtSci(r.q)} | ${fmtSci(r.pWithout)} | ${(drop * 100).toFixed(2)}% |`);
    }
    L.push('');
  }
  L.push('---');
  L.push('');

  // ============ 7. 结论与建议 ============
  L.push(`## 7. 结论与改进建议`);
  L.push('');
  const conclusions = buildConclusions(tree, result);
  for (const c of conclusions) L.push(`- ${c}`);
  L.push('');
  L.push('---');
  L.push('');

  // ============ 附录 ============
  if (opts.includeAppendix !== false) {
    L.push(`## 附录 A. 模型元数据`);
    L.push('');
    L.push('| 项 | 值 |');
    L.push('|---|---|');
    L.push(`| 项目 | ${esc(meta.project || '-')} |`);
    L.push(`| 作者 | ${esc(meta.author || '-')} |`);
    L.push(`| 日期 | ${meta.date || '-'} |`);
    L.push(`| 版本 | ${meta.revision || 'A'} |`);
    L.push(`| 割集阶数上限 | ${tree.settings?.maxCutSetOrder || '不限'} |`);
    L.push(`| 概率截断阈值 | ${tree.settings?.truncation ?? '-'} |`);
    L.push(`| 求解方法 | ${m.topProbMethod || '-'} |`);
    L.push('');
  }

  L.push('');
  L.push(`---`);
  L.push('');
  L.push(`*本报告由 FTA Studio 自动生成。计算引擎实现 MOCUS 最小割集算法与 BDD 精确概率求解，符号体系遵循 IEC 61025。*`);

  return L.join('\n');
}

// ============ 辅助函数 ============

/** 生成树形布尔方程文本 */
function treeToBoolean(tree) {
  const { nodeMap, childrenOf } = buildIndexSafe(tree);
  const roots = tree.nodes.filter((n) => n.type === 'top');
  if (!roots.length) return '';
  const varOf = (id) => {
    const n = nodeMap.get(id);
    if (!n) return '?';
    const nm = String(n.name || n.id).replace(/[∧∨=()\[\]]/g, '');
    return nm.length > 28 ? nm.slice(0, 27) + '…' : nm;
  };
  const rec = (id, depth = 0) => {
    if (depth > 12) return '…';
    const n = nodeMap.get(id);
    if (!n) return '?';
    const kids = childrenOf.get(id) || [];
    if (!kids.length) return varOf(id);
    const parts = kids.map((k) => rec(k, depth + 1));
    const gate = n.gate || 'OR';
    // 只有多输入的门才加括号，保证运算优先级正确
    const op = (gate === 'AND' || gate === 'PAND') ? ' ∧ ' : gate === 'XOR' ? ' ⊕ ' : ' ∨ ';
    const body = parts.join(op);
    const inner = parts.length > 1 ? `(${body})` : body;
    switch (gate) {
      case 'VOTE':
        return `${varOf(id)} = 至少 ${n.voteK}/${n.voteN} 成立 ⇔ ${inner}`;
      case 'INHIBIT':
        return `${varOf(id)} = ${inner}  [条件满足时传递]`;
      case 'NOT':
        return `${varOf(id)} = ¬(${parts[0]})`;
      default:
        return `${varOf(id)} = ${inner}`;
    }
  };
  return rec(roots[0].id, 0);
}

function buildIndexSafe(tree) {
  const nodeMap = new Map(tree.nodes.map((n) => [n.id, n]));
  const childrenOf = new Map(tree.nodes.map((n) => [n.id, []]));
  for (const c of tree.connections) {
    if (childrenOf.has(c.from) && nodeMap.has(c.to)) childrenOf.get(c.from).push(c.to);
  }
  return { nodeMap, childrenOf };
}

function describeParams(n) {
  const m = n.probModel || 'fixed';
  const parts = [];
  switch (m) {
    case 'fixed': if (n.prob != null) parts.push(`固定概率`); break;
    case 'exponential': case 'poisson':
      parts.push(`λ=${fmtNum(n.lambda)}/h`); break;
    case 'weibull':
      parts.push(`λ=${fmtNum(n.lambda)}/h, β=${n.beta ?? 1}`); break;
    case 'demand':
      parts.push(`需求${n.demandCount ?? '-'}次 × ${fmtNum(n.demandProb)}`); break;
    case 'repairable':
      parts.push(`λ=${fmtNum(n.lambda)}/h, TMR=${n.repairTime ?? '-'}h`); break;
    case 'monitored':
      parts.push(`λ=${fmtNum(n.lambda)}/h, TI=${n.monitorInterval ?? '-'}h`); break;
    case 'beta':
      parts.push(`β=${n.beta ?? '-'}`); break;
    default: break;
  }
  return parts.join(', ') || '-';
}

function orderDistText(byOrder) {
  if (!byOrder) return '-';
  const e = Object.entries(byOrder).sort((a, b) => Number(a[0]) - Number(b[0]));
  return e.map(([k, v]) => `${k}阶:${v}个`).join(' / ');
}

function fmtSci(x) {
  if (x == null || Number.isNaN(x)) return '-';
  const v = Number(x);
  if (v === 0) return '0';
  if (Math.abs(v) >= 1e-3 && Math.abs(v) < 1e5) return v.toPrecision(5);
  return v.toExponential(3);
}

function estimateFIT(m) {
  if (!m.missionTime) return null;
  const rate = m.topProb / m.missionTime; // per hour
  return rate * 1e9;
}

function buildConclusions(tree, result) {
  const out = [];
  const m = result.metrics || {};
  if (result.importance?.length) {
    const r1 = result.importance[0];
    out.push(`顶事件"${tree.meta.title}"的发生概率为 **${fmtSci(m.topProb)}**，系统可靠度为 ${fmtSci(m.reliability)}。`);
    if (m.cutSets?.singlePoints > 0) {
      out.push(`模型中存在 **${m.cutSets.singlePoints} 个单一失效点**，构成系统级单点失效风险，应通过架构冗余、增加诊断覆盖率或安全机制进行缓解。`);
    }
    out.push(`从重要度看，**${r1.name}**${r1.component ? `（部件：${r1.component}）` : ''}是当前系统的首要风险源（关键重要度 ${fmtSci(r1.criticality)}），消除该失效模式可降低顶事件概率约 ${(r1.fv * 100).toFixed(1)}%。建议将其列为改进设计的首要对象。`);
    const sp = result.importance.filter((r) => r.order === undefined);
    // 列出前 5 的 FV 贡献
    const top5 = result.importance.slice(0, 5).map((r) => `${r.name}(${(r.fv * 100).toFixed(1)}%)`);
    out.push(`前 5 位风险贡献来源：${top5.join('、')}。这些事件的改进投入产出比最高。`);
  } else {
    out.push('未识别到基本事件，无法给出定量结论。');
  }
  if (m.nonCoherent) {
    out.push('本故障树包含非相干门（XOR/NOT/INHIBIT），已采用 BDD 精确求解。审查时请注意非相干逻辑的物理含义是否合理。');
  }
  return out;
}

function esc(s) {
  return String(s ?? '').replace(/\|/g, '\\|');
}

/**
 * 生成 HTML 报告（自带样式）
 */
export function generateHTMLReport(tree, result, opts = {}) {
  const md = generateMarkdownReport(tree, result, opts);
  const heat = opts.heatmap || {};
  const svg = renderSVG(tree, { heatmap: heat, showProb: true, mode: 'light', width: opts.svgWidth });
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<title>故障树分析报告 - ${esc(tree.meta.title)}</title>
<style>
  :root { --bd: #e5e7eb; --tx: #1f2937; --mu: #6b7280; --ac: #2563eb; --bg: #f9fafb; }
  * { box-sizing: border-box; }
  body { font-family: -apple-system, 'Segoe UI', 'Microsoft YaHei', sans-serif; color: var(--tx); background: var(--bg); margin: 0; padding: 32px; line-height: 1.7; }
  .wrap { max-width: 1080px; margin: 0 auto; background: #fff; padding: 48px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,.1); }
  h1 { font-size: 26px; border-bottom: 3px solid var(--ac); padding-bottom: 12px; margin-top: 0; }
  h2 { font-size: 20px; margin-top: 36px; border-left: 4px solid var(--ac); padding-left: 10px; }
  h3 { font-size: 16px; margin-top: 24px; color: #374151; }
  table { border-collapse: collapse; width: 100%; margin: 14px 0; font-size: 13.5px; }
  th, td { border: 1px solid var(--bd); padding: 7px 10px; text-align: left; }
  th { background: #f3f4f6; font-weight: 600; }
  tr:nth-child(even) td { background: #fafafa; }
  code { background: #f3f4f6; padding: 2px 6px; border-radius: 4px; font-family: 'JetBrains Mono', Consolas, monospace; font-size: 13px; }
  pre { background: #1e293b; color: #e2e8f0; padding: 16px; border-radius: 8px; overflow-x: auto; font-size: 13px; line-height: 1.6; }
  pre code { background: none; color: inherit; padding: 0; }
  blockquote { border-left: 4px solid #d1d5db; background: #f9fafb; margin: 14px 0; padding: 10px 16px; color: var(--mu); }
  hr { border: none; border-top: 1px solid var(--bd); margin: 28px 0; }
  img { max-width: 100%; border: 1px solid var(--bd); border-radius: 8px; margin: 14px 0; background: #fff; }
  strong { color: #111827; }
  .diagram { overflow-x: auto; }
</style>
</head>
<body><div class="wrap">
<div class="diagram">${svg}</div>
${mdToHtml(md)}
</div></body>
</html>`;
}

/** 极简 Markdown -> HTML（覆盖我们报告里用到的语法） */
function mdToHtml(md) {
  const lines = md.split('\n');
  const out = [];
  let inTable = false, inList = false, inCode = false, inQuote = false;

  const inline = (s) => esc(s)
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
    .replace(/!\[([^\]]*)\]\((data:[^)]+)\)/g, '<img alt="$1" src="$1">')
    .replace(/\\\|/g, '|');

  const closeBlocks = () => {
    if (inTable) { out.push('</tbody></table>'); inTable = false; }
    if (inList) { out.push('</ul>'); inList = false; }
    if (inQuote) { out.push('</blockquote>'); inQuote = false; }
  };

  for (let i = 0; i < lines.length; i++) {
    const L = lines[i];
    if (L.startsWith('```')) {
      if (inCode) { out.push('</code></pre>'); inCode = false; }
      else { closeBlocks(); out.push('<pre><code>'); inCode = true; }
      continue;
    }
    if (inCode) { out.push(esc(L)); continue; }

    const t = L.trim();
    if (!t) { closeBlocks(); continue; }

    if (t.startsWith('|')) {
      const cells = t.split('|').slice(1, -1).map((c) => c.trim());
      if (/^[\s:-]+$/.test(t.replace(/\|/g, ''))) continue; // 分隔行
      if (!inTable) {
        closeBlocks();
        out.push('<table><thead><tr>' + cells.map((c) => `<th>${inline(c)}</th>`).join('') + '</tr></thead><tbody>');
        inTable = true;
      } else {
        out.push('<tr>' + cells.map((c) => `<td>${inline(c)}</td>`).join('') + '</tr>');
      }
      continue;
    }
    closeBlocks();

    if (t.startsWith('### ')) out.push(`<h3>${inline(t.slice(4))}</h3>`);
    else if (t.startsWith('## ')) out.push(`<h2>${inline(t.slice(3))}</h2>`);
    else if (t.startsWith('# ')) { /* 标题已单独渲染，跳过 */ }
    else if (t.startsWith('> ')) {
      if (!inQuote) { out.push('<blockquote>'); inQuote = true; }
      out.push(`<p>${inline(t.slice(2))}</p>`);
    }
    else if (t.startsWith('- ')) {
      if (!inList) { out.push('<ul>'); inList = true; }
      out.push(`<li>${inline(t.slice(2))}</li>`);
    }
    else if (/^---+$/.test(t)) out.push('<hr>');
    else if (t.startsWith('![')) {
      const m = t.match(/!\[([^\]]*)\]\((data:[^)]+)\)/);
      if (m) out.push(`<img alt="${m[1]}" src="${m[1]}">`);
    }
    else out.push(`<p>${inline(t)}</p>`);
  }
  closeBlocks();
  if (inCode) out.push('</code></pre>');
  return out.join('\n');
}