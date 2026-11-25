/**
 * FTA Studio - 高层 API（供 WorkBuddy / CLI / HTTP 服务统一调用）
 *
 * 这是给 AI Agent 设计的稳定调用面。所有方法都是纯函数或幂等的，
 * 不依赖文件系统，便于在任意运行时中嵌入。
 */

import {
  createEmptyTree, createNode, parseDSL, stringifyDSL, validateTree,
  buildIndex, findTopEvent, fmtNum, EVENT_TYPES, GATE_TYPES, PROB_MODELS,
} from './model.mjs';
import { computeCutSets, structureImportance } from './mocus.mjs';
import { quantify, eventProbability, timeDependent, whatIf } from './quantify.mjs';
import { layout, outline } from './layout.mjs';
import { renderSVG } from './svg.mjs';
import { generateMarkdownReport, generateHTMLReport } from './report.mjs';

export class FTAStudio {
  constructor() {
    this.version = '1.0.0';
  }

  /** 从紧凑 DSL 文本创建故障树 */
  fromDSL(text) {
    const tree = parseDSL(text);
    const v = validateTree(tree);
    return {
      tree,
      validation: v,
      rootEvent: findTopEvent(tree),
      summary: this._summary(tree, v),
    };
  }

  /** 从 JSON 对象创建 */
  fromJSON(obj) {
    const tree = obj && Array.isArray(obj.nodes) ? obj : createEmptyTree();
    const v = validateTree(tree);
    return { tree, validation: v, rootEvent: findTopEvent(tree), summary: this._summary(tree, v) };
  }

  /** DSL 文本 -> 完整分析报告（一步到位，最常用的入口） */
  analyzeDSL(text, opts = {}) {
    const { tree, validation } = this.fromDSL(text);
    if (!validation.ok && !opts.allowInvalid) {
      return { ok: false, validation, errors: validation.errors };
    }
    return this.analyze(tree, opts);
  }

  /** JSON -> 完整分析报告 */
  analyzeJSON(obj, opts = {}) {
    const { tree, validation } = this.fromJSON(obj);
    if (!validation.ok && !opts.allowInvalid) {
      return { ok: false, validation, errors: validation.errors };
    }
    return this.analyze(tree, opts);
  }

  /**
   * 核心分析流程
   * @param {object} tree
   * @param {object} opts
   *   maxOrder        割集阶数上限
   *   truncation      概率截断
   *   quantification  'auto'|'rare'|'bdd'
   *   report          'markdown'|'html'|'json'|'none'
   *   includeDiagram  是否在 Markdown 中嵌入图形
   *   heatmap         是否计算热力图
   */
  analyze(tree, opts = {}) {
    const t0 = Date.now();
    const validation = validateTree(tree);
    const result = quantify(tree, opts);

    if (!result.ok) {
      return { ok: false, errors: validation.errors, validation };
    }

    // 热力图：基于重要度映射到每个节点
    const importanceMap = new Map();
    for (const r of result.importance || []) importanceMap.set(r.id, r.heat ?? 0);
    // 中间事件：用其子树内叶子的最大重要度
    const heatmap = buildNodeHeatmap(tree, result);

    const payload = {
      ok: true,
      version: this.version,
      meta: tree.meta,
      validation,
      rootEvent: result.rootId,
      metrics: result.metrics,
      cutSets: {
        total: result.cutSets.cutSets.length,
        byOrder: result.cutSets.stats.byOrder,
        singlePoints: result.cutSets.stats.singlePoints,
        truncated: result.cutSets.truncated,
        items: result.cutSets.cutSets.map((cs) => ({
          index: cs.index,
          order: cs.order,
          events: cs.ids,
          names: cs.names,
          probability: cs.prob,
        })),
      },
      importance: (result.importance || []).map((r) => ({
        rank: r.rank,
        id: r.id,
        name: r.name,
        component: r.component,
        ref: r.ref,
        probability: r.q,
        pWith: r.pWith,
        pWithout: r.pWithout,
        birnbaum: r.birnbaum,
        criticality: r.criticality,
        fussellVesely: r.fv,
        raw: r.raw,
        rrw: Number.isFinite(r.rrw) ? r.rrw : null,
        structureImportance: r.structureImportance,
        heat: r.heat,
      })),
      heatmap: Object.fromEntries(heatmap),
      nodeProbs: result.nodeProbs || {},
      timing: { computeMs: Date.now() - t0 },
    };

    const format = opts.report || 'json';
    if (format === 'markdown' || format === 'html') {
      const ropts = {
        heatmap,
        includeDiagram: opts.includeDiagram !== false,
        embedImage: opts.embedImage !== false,
        includeAppendix: opts.includeAppendix,
        svgFile: opts.svgFile,
      };
      if (format === 'markdown') payload.report = generateMarkdownReport(tree, result, ropts);
      else payload.report = generateHTMLReport(tree, result, ropts);
    }
    if (opts.includeSVG) {
      payload.svg = renderSVG(tree, { heatmap, showProb: true, mode: opts.mode || 'light' });
    }
    payload.outline = outline(tree);
    return payload;
  }

  /** 只算最小割集 */
  cutSets(tree, opts = {}) {
    return computeCutSets(tree, opts);
  }

  /** 只做定量 */
  quantify(tree, opts = {}) {
    return quantify(tree, opts);
  }

  /** What-if：修改某些事件概率后重算 */
  simulate(tree, overrides = {}, opts = {}) {
    const res = whatIf(tree, overrides);
    const before = quantify(tree, opts);
    return {
      ok: true,
      before: before.metrics,
      after: res.metrics,
      delta: res.metrics.topProb - before.metrics.topProb,
      deltaPct: before.metrics.topProb > 0
        ? ((res.metrics.topProb - before.metrics.topProb) / before.metrics.topProb) * 100
        : 0,
    };
  }

  /** 时间曲线 */
  timeCurve(tree, points = 20, tMax = null) {
    return timeDependent(tree, points, tMax);
  }

  /** 渲染 SVG */
  toSVG(tree, opts = {}) {
    const res = opts.heatmap ? { importance: [] } : quantify(tree, opts);
    const heatmap = opts.heatmap || buildNodeHeatmap(tree, res);
    return renderSVG(tree, { ...opts, heatmap });
  }

  /** 序列化回 DSL */
  toDSL(tree) {
    return stringifyDSL(tree);
  }

  /** 元信息 / 能力清单 */
  capabilities() {
    return {
      name: 'FTA Studio',
      version: this.version,
      description: '对标 Ansys medini analyze 的故障树分析 (FTA) 模块',
      eventTypes: Object.entries(EVENT_TYPES).map(([k, v]) => ({ key: k, type: v })),
      gateTypes: Object.keys(GATE_TYPES),
      probabilityModels: Object.keys(PROB_MODELS),
      methods: ['MOCUS 最小割集', 'BDD 精确概率', '稀有事件近似', 'MCUB 上界'],
      importanceMeasures: ['Birnbaum', 'Criticality', 'Fussell-Vesely', 'RAW', 'RRW', 'Structure'],
      outputs: ['Markdown 报告', 'HTML 报告', 'SVG 图形', 'JSON 结果', 'JSON 结果 + 内嵌 SVG'],
      callInterface: 'Node.js (FTAStudio 类) | CLI | HTTP REST API',
    };
  }

  /** 从示例名加载模板 */
  loadExample(name) {
    const examples = {
      brake: {
        title: '车辆制动系统失效故障树',
        project: '功能安全 ISO 26262',
        standard: 'ISO 26262 / FMEDA',
        missionTime: 100,
        dsl: `meta title: 车辆制动系统无法建立制动力
meta project: 功能安全分析 (ISO 26262)
meta standard: ISO 26262 / GB/T 34590
meta missionTime: 100

TOP 制动系统无法建立制动力 [ASIL-D]
  AND
    INTER 主缸压力不足
      OR
        INTER 液压制动源失效
          OR
            BASIC 制动泵机械卡滞 p=2e-4 ref=FMEA-001 comp=制动泵
            BASIC 助力器失效 p=5e-4 ref=FMEA-002 comp=助力器
            BASIC 制动液泄漏 p=1e-4 ref=FMEA-003 comp=管路
        INTER 制动回路失效
          OR
            BASIC 轮缸内漏 p=3e-4 ref=FMEA-004 comp=轮缸
            BASIC 制动管路破裂 p=5e-5 ref=FMEA-005 comp=管路
    INTER 踏板行程传递失效
      OR
        BASIC 踏板自由行程过大 p=1e-3 ref=FMEA-006 comp=踏板
        BASIC 踏板连杆断裂 p=1e-4 ref=FMEA-007 comp=连杆`,
      },
      'power-supply': {
        title: '电源系统失效故障树',
        project: '系统可靠性分析',
        standard: 'MIL-HDBK-217F',
        missionTime: 1000,
        dsl: `meta title: 直流电源系统输出丧失
meta project: 可靠性预计
meta standard: MIL-HDBK-217F
meta missionTime: 1000

TOP 直流电源输出丧失
  OR
    INTER 一次电源失效
      OR
        BASIC 主电池内阻增大 p=1e-5 lambda=3e-9 ref=RLDB-001 comp=电池
        BASIC AC/DC 变换器失效 p=2e-5 ref=RLDB-002 comp=变换器
    INTER 冗余切换失效
      AND
        BASIC 电源一次失效 p=1e-5 ref=RLDB-001 comp=电池
        BASIC 二极管 OR-ing 失效 p=5e-6 ref=RLDB-003 comp=二极管阵列`,
      },
      'sensor-2oo3': {
        title: '2-out-of-3 传感器系统失效',
        project: 'SIL 定级',
        standard: 'IEC 61508',
        missionTime: 8760,
        dsl: `meta title: 2oo3 传感器系统错误输出
meta project: SIL 定级 (IEC 61508)
meta standard: IEC 61508
meta missionTime: 8760

TOP 2oo3 传感器系统输出错误
  OR
    INTER 至少两个传感器失效
      VOTE 2/3
        BASIC 传感器A失效 p=1e-3 ref=FM-A comp=SensorA
        BASIC 传感器B失效 p=1e-3 ref=FM-B comp=SensorB
        BASIC 传感器C失效 p=1e-3 ref=FM-C comp=SensorC
    INTER 共因与系统性失效
      OR
        BASIC 电源共因失效 p=2e-4 ref=CCF-01 comp=供电
        BASIC 环境共因失效 p=1e-4 ref=CCF-02 comp=环境
        BASIC 传感器A-B共因 p=5e-5 ref=CCF-03 comp=SensorAB`,
      },
    };
    const ex = examples[name];
    if (!ex) return { ok: false, error: `未知示例: ${name}`, available: Object.keys(examples) };
    const built = this.fromDSL(ex.dsl);
    return {
      ok: true,
      name,
      meta: ex,
      tree: built.tree,
      analysis: this.analyze(built.tree, { report: 'none' }),
      dsl: ex.dsl,
    };
  }

  _summary(tree, validation) {
    const { nodeMap } = buildIndex(tree);
    const counts = {};
    for (const n of tree.nodes) counts[n.type] = (counts[n.type] || 0) + 1;
    const gates = {};
    for (const n of tree.nodes) if (n.gate) gates[n.gate] = (gates[n.gate] || 0) + 1;
    return {
      nodeCount: tree.nodes.length,
      connectionCount: tree.connections.length,
      eventTypes: counts,
      gates,
      ok: validation.ok,
    };
  }
}

/** 为每个节点计算热力值（叶子用自身重要度，中间节点取子树最大值） */
function buildNodeHeatmap(tree, result) {
  const { childrenOf } = buildIndex(tree);
  const imp = new Map();
  for (const r of result.importance || []) imp.set(r.id, r.heat ?? 0);

  const heat = new Map();
  const seen = new Set();
  const walk = (id) => {
    if (seen.has(id)) return imp.get(id) ?? 0;
    seen.add(id);
    const own = imp.get(id);
    const kids = childrenOf.get(id) || [];
    if (!kids.length) {
      heat.set(id, own ?? 0);
      return own ?? 0;
    }
    let mx = own ?? 0;
    for (const k of kids) mx = Math.max(mx, walk(k));
    heat.set(id, mx);
    return mx;
  };
  const root = findTopEvent(tree);
  if (root) walk(root);
  // 折叠的子树节点也给一个值
  for (const n of tree.nodes) if (!heat.has(n.id)) heat.set(n.id, 0);
  return heat;
}

// 导出单例，便于快速调用
export const fta = new FTAStudio();
export default fta;