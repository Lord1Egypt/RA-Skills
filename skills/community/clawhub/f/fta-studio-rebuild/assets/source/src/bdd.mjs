/**
 * FTA Studio - 二叉决策图 (BDD) 精确概率求解
 *
 * 参考: medini analyze 采用 BDD 实现大规模故障树的精确概率计算。
 * BDD 能精确处理非相干树（XOR / NOT / 非相干 INHIBIT），无需稀有事件近似。
 *
 * 实现要点：
 *   - 唯一表 (unique table) 保证节点规范化，消除冗余
 *   - apply 记忆化 (memoization) 保证布尔运算效率
 *   - 变量顺序：按出现频次降序 + 索引，提升共享度
 */

import { buildIndex, findTopEvent, GATEABLE, COHERENT_GATES } from './model.mjs';

// 节点用整数表示。0 = FALSE, 1 = TRUE, >=2 为内部节点
const FALSE = 0;
const TRUE = 1;

class BDDManager {
  constructor(nVars) {
    this.nVars = nVars;
    this.varNames = new Array(nVars).fill('');
    // nodes[i] = { var, low, high }; id 0/1 为终端
    this.nodes = new Map([
      [FALSE, { var: -1, low: 0, high: 0 }],
      [TRUE, { var: -1, low: 0, high: 0 }],
    ]);
    this.uniqueTable = new Map();   // `${var},${low},${high}` -> id
    this.applyCache = new Map();    // `${op},${u},${w}` -> id
    this.notCache = new Map();      // id -> id
    this.nextId = 2;
  }

  varNode(v, low, high) {
    if (low === high) return low;
    const key = `${v},${low},${high}`;
    const hit = this.uniqueTable.get(key);
    if (hit !== undefined) return hit;
    const id = this.nextId++;
    this.nodes.set(id, { var: v, low, high });
    this.uniqueTable.set(key, id);
    return id;
  }

  isTerminal(id) { return id === FALSE || id === TRUE; }
  topVar(id) { return this.nodes.get(id).var; }

  /** Shannon 展开：返回 u 关于变量 v 的余因子 (v=0 分支, v=1 分支) */
  cofactor(u, v) {
    if (this.isTerminal(u)) return [u, u];
    const n = this.nodes.get(u);
    if (n.var > v) return [u, u];          // u 不依赖 v
    if (n.var === v) return [n.low, n.high];
    // n.var < v：v 在更上层，需继续展开
    const [lo, hi] = this.cofactor(n.low, v);
    const [lo2, hi2] = this.cofactor(n.high, v);
    return [this.varNode(n.var, lo, lo2), this.varNode(n.var, hi, hi2)];
  }

  mk(op, u, w) {
    const key = `${op},${u},${w}`;
    const hit = this.applyCache.get(key);
    if (hit !== undefined) return hit;

    let res;
    // 终止化
    switch (op) {
      case 'AND':
        if (u === FALSE || w === FALSE) res = FALSE;
        else if (u === TRUE) res = w;
        else if (w === TRUE) res = u;
        else if (u === w) res = u;
        else res = null;
        break;
      case 'OR':
        if (u === TRUE || w === TRUE) res = TRUE;
        else if (u === FALSE) res = w;
        else if (w === FALSE) res = u;
        else if (u === w) res = u;
        else res = null;
        break;
      case 'XOR':
        if (u === FALSE) res = w;
        else if (w === FALSE) res = u;
        else if (u === TRUE) res = this.mkNot(w);
        else if (w === TRUE) res = this.mkNot(u);
        else if (u === w) res = FALSE;
        else res = null;
        break;
      default:
        res = null;
    }

    if (res === null) {
      const top = Math.min(this.topVar(u), this.topVar(w));
      const [u0, u1] = this.cofactor(u, top);
      const [w0, w1] = this.cofactor(w, top);
      const low = this.mk(op, u0, w0);
      const high = this.mk(op, u1, w1);
      res = this.varNode(top, low, high);
    }
    this.applyCache.set(key, res);
    return res;
  }

  mkNot(u) {
    const hit = this.notCache.get(u);
    if (hit !== undefined) return hit;
    let res;
    if (this.isTerminal(u)) {
      res = u === TRUE ? FALSE : TRUE;
    } else {
      const n = this.nodes.get(u);
      res = this.varNode(n.var, this.mkNot(n.low), this.mkNot(n.high));
    }
    this.notCache.set(u, res);
    return res;
  }

  /** 计算 BDD 表示的布尔函数在给定变量概率下的概率值 */
  probability(root, probs) {
    const memo = new Map();
    const rec = (u) => {
      const hit = memo.get(u);
      if (hit !== undefined) return hit;
      if (u === TRUE) { memo.set(u, 1); return 1; }
      if (u === FALSE) { memo.set(u, 0); return 0; }
      const n = this.nodes.get(u);
      const q = probs[n.var];
      const val = q * rec(n.high) + (1 - q) * rec(n.low);
      memo.set(u, val);
      return val;
    };
    return rec(root);
  }

  /** 共因次数（满足赋值中变量为 1 的个数上界/期望） */
  nodeCount(root) {
    const memo = new Map();
    const rec = (u) => {
      const hit = memo.get(u);
      if (hit !== undefined) return hit;
      if (u === TRUE) { memo.set(u, 1); return 1; }
      if (u === FALSE) { memo.set(u, 0); return 0; }
      const n = this.nodes.get(u);
      // sopath 计数：最大值 + 1
      const val = Math.max(rec(n.low), rec(n.high)) + 1;
      memo.set(u, val);
      return val;
    };
    return rec(root);
  }

  bddSize(root) {
    const seen = new Set();
    const stack = [root];
    while (stack.length) {
      const u = stack.pop();
      if (seen.has(u) || this.isTerminal(u)) continue;
      seen.add(u);
      const n = this.nodes.get(u);
      stack.push(n.low, n.high);
    }
    return seen.size;
  }
}

/**
 * BDD 会话：构建一次，反复重算不同概率赋值下的顶事件概率。
 * 用于重要度分析（N 个基本事件需 N+1 次求值，避免 N 次重复建树）。
 */
export class BDDSession {
  /**
   * @param {object} tree
   * @param {Map<string,number>} probById
   */
  constructor(tree, probById) {
    const t0 = Date.now();
    const { nodeMap, childrenOf } = buildIndex(tree);
    const rootId = findTopEvent(tree);
    if (!rootId) {
      this.ok = false;
      this.error = '未找到顶事件';
      return;
    }
    this.ok = true;
    this.tree = tree;
    this.nodeMap = nodeMap;
    this.childrenOf = childrenOf;
    this.rootId = rootId;
    this.baseProbs = new Map(probById);

    // 收集叶子
    const leaves = [];
    const seen = new Set();
    const collect = (id) => {
      if (seen.has(id)) return;
      seen.add(id);
      const n = nodeMap.get(id);
      if (!n) return;
      const kids = childrenOf.get(id) || [];
      const gated = kids.length > 0 && GATEABLE.has(n.type);
      if (!gated) { leaves.push(id); return; }
      kids.forEach(collect);
    };
    collect(rootId);
    this.leaves = [...new Set(leaves)];

    // 变量顺序：出现频次降序
    const freq = new Map(this.leaves.map((id) => [id, 0]));
    const cnt = new Set();
    const countFreq = (id) => {
      if (cnt.has(id)) return;
      cnt.add(id);
      for (const k of childrenOf.get(id) || []) {
        freq.set(k, (freq.get(k) || 0) + 1);
        countFreq(k);
      }
    };
    countFreq(rootId);
    const order = [...new Set([...freq.keys()])].sort((a, b) => {
      const d = (freq.get(b) || 0) - (freq.get(a) || 0);
      return d !== 0 ? d : String(a).localeCompare(String(b));
    });
    this.varOrder = order;
    this.varIndex = new Map(order.map((id, i) => [id, i]));

    // 构建 BDD（只构建一次）
    this.mgr = new BDDManager(order.length);
    this.buildMemo = new Map();
    this.probCache = new Map();
    this.root = this._build(rootId);
    this.bddSize = this.mgr.bddSize(this.root);
    this.buildingTime = Date.now() - t0;
  }

  _varLeaf(id) {
    // 叶子：概率由外部赋予，恒建为"变量"节点（低分支=假，高分支=真）
    const v = this.varIndex.get(id);
    return this.mgr.varNode(v, FALSE, TRUE);
  }

  _build(id, depth = 0) {
    const hit = this.buildMemo.get(id);
    if (hit !== undefined) return hit;
    const n = this.nodeMap.get(id);
    if (!n) return FALSE;
    const kids = this.childrenOf.get(id) || [];
    if (!GATEABLE.has(n.type) || kids.length === 0) {
      const res = this._varLeaf(id);
      this.buildMemo.set(id, res);
      return res;
    }
    if (depth > 400) return FALSE; // 深度保护
    const childBdds = kids.map((k) => this._build(k, depth + 1));
    const gate = n.gate || 'OR';
    let res;
    switch (gate) {
      case 'AND': case 'PAND':
        res = childBdds.reduce((a, b) => this.mgr.mk('AND', a, b), TRUE);
        break;
      case 'OR':
        res = childBdds.reduce((a, b) => this.mgr.mk('OR', a, b), FALSE);
        break;
      case 'XOR':
        res = childBdds.reduce((a, b) => this.mgr.mk('XOR', a, b), FALSE);
        break;
      case 'NOT':
        res = this.mgr.mkNot(childBdds[0] ?? FALSE);
        break;
      case 'INHIBIT': {
        const cond = childBdds[childBdds.length - 1] ?? FALSE;
        const prereq = childBdds.slice(0, -1).reduce((a, b) => this.mgr.mk('AND', a, b), TRUE);
        res = this.mgr.mk('AND', cond, prereq);
        break;
      }
      case 'VOTE':
        res = voteBDD(this.mgr, childBdds, Math.max(1, Math.min(n.voteK ?? 2, kids.length)));
        break;
      default:
        res = childBdds.reduce((a, b) => this.mgr.mk('OR', a, b), FALSE);
    }
    this.buildMemo.set(id, res);
    return res;
  }

  /** 在给定概率映射下求顶事件概率 */
  probability(probById = this.baseProbs) {
    // 概率向量只依赖变量顺序的赋值，用 key 缓存
    const probs = new Array(this.varOrder.length);
    for (let i = 0; i < this.varOrder.length; i++) {
      const q = probById.get(this.varOrder[i]);
      probs[i] = q == null ? 0 : q;
    }
    const key = probs.join(',');
    const hit = this.probCache.get(key);
    if (hit !== undefined) return hit;
    const v = this.mgr.probability(this.root, probs);
    if (this.probCache.size < 200000) this.probCache.set(key, v);
    return v;
  }

  /** 把某事件的概率临时改为 target 后求概率（用于 Birnbaum / RAW / RRW） */
  probabilityWith(eventId, target) {
    const q = this.baseProbs.get(eventId);
    if (q === target) return this.probability();
    const m = new Map(this.baseProbs);
    m.set(eventId, target);
    const probs = new Array(this.varOrder.length);
    for (let i = 0; i < this.varOrder.length; i++) {
      const v = m.get(this.varOrder[i]);
      probs[i] = v == null ? 0 : v;
    }
    const key = probs.join(',');
    const hit = this.probCache.get(key);
    if (hit !== undefined) return hit;
    const val = this.mgr.probability(this.root, probs);
    if (this.probCache.size < 200000) this.probCache.set(key, val);
    return val;
  }
}

/**
 * 对一棵树做精确 BDD 求解（单次入口）
 * @returns {{prob:number, bddSize:number, varOrder:string[], buildingTime:number}}
 */
export function solveBDD(tree, probsById) {
  const t0 = Date.now();
  const { nodeMap, childrenOf } = buildIndex(tree);
  const rootId = findTopEvent(tree);
  if (!rootId) return { prob: 0, bddSize: 0, varOrder: [], buildingTime: 0 };

  // 收集所有叶子事件
  const leaves = [];
  const seen = new Set();
  const collect = (id) => {
    if (seen.has(id)) return;
    seen.add(id);
    const n = nodeMap.get(id);
    if (!n) return;
    const kids = childrenOf.get(id) || [];
    const gated = GATEABLE.has(n.type) && kids.length > 0;
    if (!gated) { leaves.push(id); return; }
    kids.forEach(collect);
  };
  collect(rootId);

  // 变量顺序：出现频次降序（启发式，提升 BDD 共享度）
  const freq = new Map(leaves.map((id) => [id, 0]));
  const countFreq = (id) => {
    if (seen.has('__' + id)) return;
    seen.add('__' + id);
    const kids = childrenOf.get(id) || [];
    for (const k of kids) {
      freq.set(k, (freq.get(k) || 0) + 1);
      countFreq(k);
    }
  };
  seen.clear();
  countFreq(rootId);

  const order = [...new Set([...freq.keys()])].sort((a, b) => {
    const d = (freq.get(b) || 0) - (freq.get(a) || 0);
    return d !== 0 ? d : String(a).localeCompare(String(b));
  });
  const varIndex = new Map(order.map((id, i) => [id, i]));

  const mgr = new BDDManager(order.length);
  const memo = new Map();

  const build = (id, depth = 0) => {
    const hit = memo.get(id);
    if (hit !== undefined) return hit;
    const n = nodeMap.get(id);
    if (!n) { return FALSE; }
    const kids = childrenOf.get(id) || [];
    if (!GATEABLE.has(n.type) || kids.length === 0) {
      // 叶子：建为变量节点，其概率由求值阶段赋予
      const res = varOf(id);
      memo.set(id, res);
      return res;
    }
    if (depth > 400) return FALSE; // 深度保护（异常深树）
    // 递归构建子节点 BDD
    const childBdds = kids.map((k) => build(k, depth + 1));

    const gate = n.gate || 'OR';
    let res;
    switch (gate) {
      case 'AND':
      case 'PAND':
        res = childBdds.reduce((a, b) => mgr.mk('AND', a, b), TRUE);
        break;
      case 'OR':
        res = childBdds.reduce((a, b) => mgr.mk('OR', a, b), FALSE);
        break;
      case 'XOR':
        res = childBdds.reduce((a, b) => mgr.mk('XOR', a, b), FALSE);
        break;
      case 'NOT':
        // 非门：语义不明（缺少明确输入语义），取其输入补集
        res = mgr.mkNot(childBdds[0] ?? FALSE);
        break;
      case 'INHIBIT': {
        // 禁门：条件输入(最后一个) 为 1 时，前置输入全部为 1 才输出
        const cond = childBdds[childBdds.length - 1] ?? FALSE;
        const prereq = childBdds.slice(0, -1).reduce((a, b) => mgr.mk('AND', a, b), TRUE);
        res = mgr.mk('AND', cond, prereq);
        break;
      }
      case 'VOTE': {
        const k = Math.max(1, Math.min(n.voteK ?? 2, kids.length));
        res = voteBDD(mgr, childBdds, k);
        break;
      }
      default:
        res = childBdds.reduce((a, b) => mgr.mk('OR', a, b), FALSE);
    }
    memo.set(id, res);
    return res;
  };

  // 叶子事件建为 BDD 变量节点：变量为 0 时取 low，为 1 时取 high。
// 实际概率在 probability() 阶段按 q = P(变量=1) 注入。
  function varOf(id) {
    const v = varIndex.get(id);
    if (v === undefined) return FALSE; // 不在变量表中视为恒假
    return mgr.varNode(v, FALSE, TRUE);
  }

  const root = build(rootId);
  const probs = new Array(order.length);
  for (let i = 0; i < order.length; i++) {
    const q = probsById.get(order[i]);
    probs[i] = q == null ? 0 : q;
  }
  const prob = mgr.probability(root, probs);
  return {
    prob,
    bddSize: mgr.bddSize(root),
    varOrder: order,
    buildingTime: Date.now() - t0,
  };
}

/**
 * k-of-n 表决门的 BDD 构造
 * 语义：输出为 1 当且仅当 n 个输入中至少 k 个为 1（"至少 k 个"语义，
 * 与 IEC 61025 / 工程实践一致）。
 */
function voteBDD(mgr, childBdds, k) {
  const n = childBdds.length;
  if (k <= 0) return FALSE;
  if (k > n) return FALSE;
  if (k === 1) return childBdds.reduce((a, b) => mgr.mk('OR', a, b), FALSE);
  if (k === n) return childBdds.reduce((a, b) => mgr.mk('AND', a, b), TRUE);

  // "至少 k 个" = OR over C(n,k) 个组合，每个组合要求这些输入为 1
  // （无需排除其他输入，否则会算成"恰好 k 个"）
  let res = FALSE;
  const idx = Array.from({ length: k }, (_, i) => i);
  for (;;) {
    let term = TRUE;
    for (const i of idx) term = mgr.mk('AND', term, childBdds[i]);
    res = mgr.mk('OR', res, term);
    let i = k - 1;
    while (i >= 0 && idx[i] === n - k + i) i--;
    if (i < 0) break;
    idx[i]++;
    for (let j = i + 1; j < k; j++) idx[j] = idx[j - 1] + 1;
  }
  return res;
}

/**
 * 敏感度分析：Birnbaum / 关键重要度 / FV / RAW / RRW 的精确计算
 * 方法：直接把某基本事件的概率设为 0 或 1，重建 BDD 求概率（保证精确，含非相干）
 * @param {(id:string)=>number} qOf
 * @param {(overrideId:string, value:number)=>Promise<number>|number} probWithOverride
 */
export function exactImportance(tree, ids, probWithOverride) {
  const results = new Map();
  for (const id of ids) {
    const p1 = probWithOverride(id, 1);
    const p0 = probWithOverride(id, 0);
    const birnbaum = p1 - p0;
    results.set(id, {
      p_with: p1,
      p_without: p0,
      birnbaum,
      raw: p1,            // Risk Achievement Worth
      rrw: p0 > 0 ? (1 - p0) / p0 : Infinity,
    });
  }
  return results;
}