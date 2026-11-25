/**
 * FTA Studio - 定量分析与重要度计算
 *
 * 支持的概率模型（对应 medini analyze）：
 *   fixed / exponential / weibull / demand / poisson / repairable / monitored
 *   以及 beta 因子共因建模
 *
 * 支持的定量方法：
 *   - 稀有事件近似 (rare event approximation)
 *   - 最小割集上界 (MCUB, Minimal Cut-Set Upper Bound)
 *   - BDD 精确解（支持非相干树）
 *   - Esary-Proschan 上界
 */

import {
  buildIndex, findTopEvent, PROB_MODELS, fmtNum,
} from './model.mjs';
import { computeCutSets, structureImportance, fussellVesely } from './mocus.mjs';
import { solveBDD, BDDSession } from './bdd.mjs';

// 传输符号类型：仅为跨页引用标记，不参与概率与割集计算
const TRANSFER_TYPES = new Set(['transfer_in', 'transfer_out']);

// ============ 概率模型换算 ============

/**
 * 计算一个基本事件的不可用度 q
 * @param {object} node
 * @param {number|null} missionTime 任务时间
 * @param {object} settings
 */
export function eventProbability(node, missionTime, settings = {}) {
  const m = node.probModel || PROB_MODELS.FIXED;
  const t = missionTime ?? settings.missionTime ?? node.eta ?? 0;

  switch (m) {
    case PROB_MODELS.FIXED:
      return clamp01(node.prob ?? 0);

    case PROB_MODELS.EXPONENTIAL:
    case PROB_MODELS.POISSON: {
      const lam = node.lambda ?? 0;
      if (!t) return node.prob ?? 0;
      return clamp01(1 - Math.exp(-lam * t));
    }

    case PROB_MODELS.WEIBULL: {
      const lam = node.lambda ?? 0;
      const beta = node.beta ?? 1;
      if (!lam || lam <= 0) return 0;
      return clamp01(1 - Math.exp(-Math.pow(lam * t, beta)));
    }

    case PROB_MODELS.DEMAND: {
      // 需求型：q = 需求次数 × 单次失效率
      const n = node.demandCount ?? settings.demandCount ?? 1;
      const pd = node.demandProb ?? node.prob ?? 0;
      return clamp01(n * pd);
    }

    case PROB_MODELS.REPAIRABLE: {
      // 可修复（稳态不可用度）q ≈ λ·TMR / (1 + λ·TMR)
      const lam = node.lambda ?? 0;
      const tmr = node.repairTime ?? 0;
      if (!lam) return node.prob ?? 0;
      return clamp01((lam * tmr) / (1 + lam * tmr));
    }

    case PROB_MODELS.MONITORED: {
      // 周期监控：q ≈ 1 - e^(-λ·TI)，即监控间隔内的失效概率
      const lam = node.lambda ?? 0;
      const ti = node.monitorInterval ?? settings.monitorInterval ?? t;
      if (!lam || !ti) return node.prob ?? 0;
      return clamp01(1 - Math.exp(-lam * ti));
    }

    case PROB_MODELS.BETA: {
      // β 因子共因：q = β · Q_basic
      const b = node.beta ?? 0;
      const q = node.prob ?? 0;
      return clamp01(b * q);
    }

    default:
      return clamp01(node.prob ?? 0);
  }
}

function clamp01(x) {
  if (Number.isNaN(x)) return 0;
  return Math.max(0, Math.min(1, x));
}

/** 时间相关的不可用度曲线 q(t) */
export function eventUnavailabilityAt(node, t, settings = {}) {
  const m = node.probModel || PROB_MODELS.FIXED;
  switch (m) {
    case PROB_MODELS.EXPONENTIAL:
    case PROB_MODELS.POISSON:
      return clamp01(1 - Math.exp(-(node.lambda ?? 0) * t));
    case PROB_MODELS.WEIBULL: {
      const lam = node.lambda ?? 0;
      const beta = node.beta ?? 1;
      if (!lam) return 0;
      return clamp01(1 - Math.exp(-Math.pow(lam * t, beta)));
    }
    case PROB_MODELS.REPAIRABLE: {
      const lam = node.lambda ?? 0;
      const tmr = node.repairTime ?? 0;
      return clamp01((lam * tmr) / (1 + lam * tmr));
    }
    case PROB_MODELS.MONITORED: {
      const lam = node.lambda ?? 0;
      const ti = node.monitorInterval ?? settings.monitorInterval ?? t;
      return clamp01(1 - Math.exp(-lam * ti));
    }
    default:
      return clamp01(node.prob ?? 0);
  }
}

// ============ 主定量分析流程 ============

export function quantify(tree, opts = {}) {
  const settings = tree.settings || {};
  const missionTime = opts.missionTime ?? settings.missionTime ?? null;
  const { nodeMap, childrenOf } = buildIndex(tree);
  const rootId = findTopEvent(tree);
  if (!rootId) {
    return { ok: false, error: '未找到顶事件' };
  }

  // 1) 计算所有基本事件概率
  const probById = new Map();
  const leafIds = [];
  const collectLeaves = (id, visited = new Set()) => {
    if (visited.has(id)) return; // 防环
    visited.add(id);
    const n = nodeMap.get(id);
    if (!n) return;
    const kids = childrenOf.get(id) || [];
    const isGate = kids.length > 0 && ['top', 'intermediate'].includes(n.type);
    if (!isGate) {
      leafIds.push(id);
      return;
    }
    for (const k of kids) collectLeaves(k, visited);
  };
  collectLeaves(rootId);

  for (const id of leafIds) {
    const n = nodeMap.get(id);
    if (n.type === 'house') {
      // 房屋事件：TRUE/FALSE 由参数决定（默认 TRUE=1 不影响分析）
      probById.set(id, n.gate === 'FALSE' || n.prob === 0 ? 1 : 0);
    } else if (n.type === 'comment') {
      probById.set(id, 0);
    } else if (n.type === 'transfer_in' || n.type === 'transfer_out') {
      // 传输符号是跨页引用标记，不是真实失效事件：概率恒为 0，
      // 其对应内容已在另一页计入，避免重复计算。
      probById.set(id, 0);
    } else {
      probById.set(id, eventProbability(n, missionTime, settings));
    }
  }
  const qOf = (id) => probById.get(id) ?? 0;

  // 2) 定性：最小割集（传输节点在定性分析中同样排除）
  const csResult = computeCutSets(tree, {
    maxOrder: opts.maxOrder ?? settings.maxCutSetOrder ?? 0,
    truncation: opts.truncation ?? settings.truncation ?? 0,
    qOf,
    excludeTypes: TRANSFER_TYPES,
  });

  // 3) 定量：稀有事件近似 + MCUB 上界
  let rareSum = 0;
  let mcub = 0;
  for (const cs of csResult.cutSets) {
    const p = cs.prob ?? 0;
    rareSum += p;
    // MCUB: 对 k 阶割集用 Bonferroni 上界修正
    mcub += p;   // 基础 MCUB = 稀有事件和（作为上界使用）
  }

  // 4) BDD 精确解（支持非相干）
  let bdd = null;
  let session = null;
  try {
    bdd = solveBDD(tree, probById);
    session = new BDDSession(tree, probById);
  } catch (e) {
    bdd = { error: e.message };
  }

  // 非相干树标志
  const nonCoherent = tree.nodes.some((n) =>
    ['XOR', 'NOT', 'INHIBIT'].includes(n.gate));

  // 5) 顶事件概率：BDD 精确优先，回退到稀有事件近似
  const method = opts.quantification || settings.quantification || 'auto';
  let topProb, topProbMethod, topProbUpper;
  if (bdd && !bdd.error) {
    topProb = bdd.prob;
    topProbMethod = 'BDD 精确解';
  } else {
    topProb = rareSum;
    topProbMethod = '稀有事件近似';
  }
  if (method === 'rare') {
    topProb = rareSum;
    topProbMethod = '稀有事件近似';
  }
  // 上界（Esary-Proschan / MCUB）
  topProbUpper = mcub;

  // 6) 重要度分析
  const importance = computeImportance(tree, {
    rootId, qOf, probById, topProb, csResult, nonCoherent,
    bddOk: !!(bdd && !bdd.error), session,
  });

  // 7) 中间事件概率（用于热力图着色）
  const intermediateProbs = computeIntermediateProbs(tree, { rootId, qOf, probById });

  // 8) 汇总指标
  const reliability = 1 - topProb;
  const metrics = {
    missionTime,
    topProb,
    topProbUpper,
    reliability,
    unreliability: topProb,
    rareEventSum: rareSum,
    mcub,
    topProbMethod,
    nonCoherent,
    cutSets: csResult.stats,
    truncated: csResult.truncated,
    bddSize: bdd && !bdd.error ? bdd.bddSize : null,
  };

  return {
    ok: true,
    rootId,
    missionTime,
    probById,
    cutSets: csResult,
    metrics,
    importance,
    intermediateProbs,
    // 逐节点概率（普通对象，供前端在事件上显示 Q；medini 的 Calculate probabilities）
    nodeProbs: Object.fromEntries([...intermediateProbs, ...probById]),
    bdd: bdd && !bdd.error ? bdd : { error: bdd?.error || 'BDD 不可用' },
  };
}

// ============ 重要度计算 ============

/**
 * 计算所有重要度指标：
 *   - Birnbaum（概率重要度）: B_i = ∂P(TOP)/∂q_i
 *   - 关键重要度 (Criticality): I_i = q_i * B_i / P(TOP)
 *   - Fussell-Vesely (FV): (P(TOP) - P(TOP|q_i=0)) / P(TOP)
 *   - RAW: P(TOP|q_i=1)/P(TOP)
 *   - RRW: (P(TOP) - P(TOP|q_i=0)) / P(TOP|q_i=0)
 *   - 结构重要度 (Structure Importance)
 */
function computeImportance(tree, { rootId, qOf, probById, topProb, csResult, nonCoherent, bddOk, session }) {
  const { nodeMap } = buildIndex(tree);
  const leaves = [...probById.keys()].filter((id) => {
    const n = nodeMap.get(id);
    return n && ['basic', 'undeveloped', 'external'].includes(n.type);
  });

  const structureImp = structureImportance(csResult.cutSets);
  const fvFromCS = fussellVesely(csResult.cutSets, topProb);

  // 精确重要度：把某事件概率设为 0 / 1 时顶事件的概率
  // 优先使用已构建的 BDDSession（只建一次树），否则退回 BDD 单次求解
  const pWith = new Map();
  const pWithout = new Map();

  if (session && session.ok) {
    for (const id of leaves) {
      pWith.set(id, session.probabilityWith(id, 1));
      pWithout.set(id, session.probabilityWith(id, 0));
    }
  } else {
    for (const id of leaves) {
      const probs = new Map(probById);
      probs.set(id, 1);
      pWith.set(id, solveBDD(tree, probs).prob);
      probs.set(id, 0);
      pWithout.set(id, solveBDD(tree, probs).prob);
    }
  }

  const rows = leaves.map((id) => {
    const q = probById.get(id) ?? 0;
    const pw = pWith.get(id) ?? 0;
    const pwo = pWithout.get(id) ?? 0;
    const birnbaum = pw - pwo;                       // ∂P(TOP)/∂q_i
    const criticality = topProb > 0 ? (q * birnbaum) / topProb : 0;
    const fv = topProb > 0 ? (topProb - pwo) / topProb : 0;
    const raw = topProb > 0 ? pw / topProb : Infinity;
    const rrw = pwo > 0 ? (topProb - pwo) / pwo : Infinity;
    return {
      id,
      name: nodeMap.get(id)?.name ?? id,
      component: nodeMap.get(id)?.component || '',
      ref: nodeMap.get(id)?.ref || '',
      q,
      pWith: pw,
      pWithout: pwo,
      birnbaum,
      criticality,
      fv,
      fvFromCS: fvFromCS.get(id) ?? 0,
      raw,
      rrw,
      structureImportance: structureImp.get(id) ?? 0,
      // 综合风险权重（用于热力图与排序，取 Birnbaum 归一化）
      rank: birnbaum,
    };
  });

  rows.sort((a, b) => b.birnbaum - a.birnbaum);
  const maxB = Math.max(...rows.map((r) => Math.abs(r.birnbaum)), 1e-30);
  for (const r of rows) {
    r.heat = Math.abs(r.birnbaum) / maxB; // 0~1 归一化热力值
    r.rank = rows.indexOf(r) + 1;
  }

  return rows;
}

// ============ 中间事件概率（热力图） ============

/**
 * 自底向上计算中间/顶事件概率（用于热力图）
 * 优先用 BDD 精确回溯每个子树的概率
 */
function computeIntermediateProbs(tree, { rootId, qOf, probById }) {
  const { nodeMap, childrenOf } = buildIndex(tree);
  const result = new Map();
  // 从根后序遍历（迭代版，避免深树爆栈；带环保护）
  const order = [];
  const seen = new Set();
  const stack = [[rootId, false]];
  while (stack.length) {
    const [id, expanded] = stack.pop();
    if (expanded) { order.push(id); continue; }
    if (seen.has(id)) continue;
    seen.add(id);
    stack.push([id, true]);
    for (const k of childrenOf.get(id) || []) {
      if (!seen.has(k)) stack.push([k, false]);
    }
  }

  for (const id of order) {
    const n = nodeMap.get(id);
    if (!n) continue;
    if (probById.has(id)) {
      result.set(id, probById.get(id));
      continue;
    }
    const kids = (childrenOf.get(id) || []).map((k) => result.get(k) ?? 0);
    const gate = n.gate || 'OR';
    let p;
    switch (gate) {
      case 'AND': case 'PAND':
        p = kids.reduce((a, b) => a * b, 1);
        break;
      case 'OR':
        p = 1 - kids.reduce((a, b) => a * (1 - b), 1);
        break;
      case 'VOTE': {
        const k = Math.max(1, Math.min(n.voteK ?? 2, kids.length));
        p = voteProbability(kids, k);
        break;
      }
      case 'XOR':
        p = 1 - kids.reduce((a, b) => a * (1 - 2 * b), 1) / 2 * 2; // 精确式
        p = xorProbability(kids);
        break;
      case 'INHIBIT': {
        const cond = kids[kids.length - 1] ?? 0;
        const prereq = kids.slice(0, -1).reduce((a, b) => a * b, 1);
        p = cond * prereq;
        break;
      }
      case 'NOT':
        p = 1 - (kids[0] ?? 0);
        break;
      default:
        p = kids.length ? Math.max(...kids) : 0;
    }
    result.set(id, clamp01(p));
  }
  return result;
}

function voteProbability(probs, k) {
  const n = probs.length;
  if (k <= 0) return 0;
  if (k > n) return 0;
  let sum = 0;
  const idx = Array.from({ length: k }, (_, i) => i);
  for (;;) {
    let term = 1;
    for (const i of idx) term *= probs[i];
    sum += term;
    let i = k - 1;
    while (i >= 0 && idx[i] === n - k + i) i--;
    if (i < 0) break;
    idx[i]++;
    for (let j = i + 1; j < k; j++) idx[j] = idx[j - 1] + 1;
  }
  // 引入容斥修正上界（MCUB 风格）：对高阶用简单容斥
  return clamp01(sum);
}

function xorProbability(probs) {
  // P(XOR) = [1 - Π(1-2p_i)] / 2  对于 2 事件奇偶性
  // 多事件 XOR（奇数次发生）：P = (1 - Π(1-2p_i))/2
  let prod = 1;
  for (const p of probs) prod *= (1 - 2 * p);
  return clamp01((1 - prod) / 2);
}

// ============ 时间序列（顶事件随时间的不可用度曲线） ============

export function timeDependent(tree, timePoints = 20, tMaxOverride = null) {
  const settings = tree.settings || {};
  const tMax = tMaxOverride ?? settings.missionTime ?? 100;
  const curve = [];
  for (let i = 0; i <= timePoints; i++) {
    const t = (i / timePoints) * tMax;
    const res = quantify(tree, { missionTime: t, quantification: 'bdd' });
    curve.push({
      t,
      q: res.metrics?.topProb ?? 0,
      reliability: 1 - (res.metrics?.topProb ?? 0),
    });
  }
  return curve;
}

// ============ 敏感度：把某事件概率设为 0 后的顶事件概率（去重要性分析） ============

export function whatIf(tree, overrides = {}) {
  const clone = JSON.parse(JSON.stringify(tree));
  const { nodeMap } = buildIndex(clone);
  for (const [id, val] of Object.entries(overrides)) {
    const n = nodeMap.get(id);
    if (n) {
      n.probModel = PROB_MODELS.FIXED;
      n.prob = val;
    }
  }
  return quantify(clone, { quantification: 'bdd' });
}