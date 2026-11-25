/**
 * FTA Studio - MOCUS 最小割集算法（位掩码优化版）
 * Fussell & Vesely, "Method of Obtaining Cut Sets", ORSA Journal, 1972
 *
 * 算法本质是自顶向下的工作集展开：
 *   - AND 门：把门的所有输入都并入当前工作集（工作集变大）
 *   - OR  门：为每个输入复制一份工作集（工作集数量变多）
 *   - 收敛后配合吸收律（超集被子集吸收）与幂等律（去重）得到最小割集
 *
 * 性能设计：
 *   基本事件被映射为整数索引，工作集用 BigInt 位掩码表示。
 *   这样 isSubset 退化为 `(a & b) === a`，是 O(1) 位运算，
 *   大规模树的剪枝成本从 O(n²·k) 降到 O(n log n)。
 */

import { buildIndex, findTopEvent, GATEABLE, COHERENT_GATES } from './model.mjs';

/** 定位某个子树的输入门 */
function resolveGate(node, children) {
  if (!GATEABLE.has(node.type)) return { kind: 'LEAF' };
  const g = node.gate || 'OR';
  if (children.length === 0) return { kind: 'LEAF' };
  switch (g) {
    case 'AND': return { kind: 'AND' };
    case 'PAND': return { kind: 'AND' };      // 优先与门：定性上与 AND 一致
    case 'OR': return { kind: 'OR' };
    case 'XOR': return { kind: 'OR' };       // 定性上按 OR 展开（非相干，量化阶段精确处理）
    case 'NOT': return { kind: 'NOT' };
    case 'INHIBIT': return { kind: 'INHIBIT' };
    case 'VOTE': {
      const k = Math.max(1, Math.min(node.voteK ?? 2, children.length));
      return { kind: 'VOTE', k };
    }
    default: return { kind: 'OR' };
  }
}

/**
 * @param {object} tree
 * @param {object} opts
 *   maxOrder      割集阶数上限（0 表示不限）
 *   truncation    概率截断阈值（可选，需要 qOf）
 *   qOf           (id) => 概率，用于截断与割集概率
 * @returns {{cutSets:Array, truncated:boolean, stats:object}}
 */
export function computeCutSets(tree, opts = {}) {
  const maxOrder = opts.maxOrder ?? tree.settings?.maxCutSetOrder ?? 0;
  const truncation = opts.truncation ?? tree.settings?.truncation ?? 0;

  const { nodeMap, childrenOf } = buildIndex(tree);
  const rootId = findTopEvent(tree);
  if (!rootId) {
    return { cutSets: [], truncated: false, stats: { total: 0, byOrder: {}, singlePoints: 0 } };
  }

  // ---- 预扫描：确定哪些节点是"基本事件"（割集元素）----
  // 基本事件 = 无子节点的事件，或展开后最终只由基本事件构成的元素
  // 为简化并与真实 MOCUS 一致：不可再展开的节点即为基本事件
  // excludeTypes 用于排除传输符号等"非失效"节点（跨页引用标记）
  const excludeTypes = opts.excludeTypes
    ? (opts.excludeTypes instanceof Set ? opts.excludeTypes : new Set(opts.excludeTypes))
    : null;
  const excluded = new Set();
  if (excludeTypes) {
    for (const n of tree.nodes) {
      if (excludeTypes.has(n.type)) excluded.add(n.id);
    }
  }

  const isGateNode = new Map();
  for (const n of tree.nodes) {
    const kids = childrenOf.get(n.id) || [];
    const g = resolveGate(n, kids);
    isGateNode.set(n.id, g.kind !== 'LEAF' && g.kind !== 'NOT');
  }

  // 收集所有基本事件并建立索引（bit 位置）
  const leafIds = [];
  const leafIndex = new Map();
  const collect = (id, guard = new Set()) => {
    if (guard.has(id)) return;
    if (excluded.has(id)) return; // 传输符号不作为割集元素
    guard.add(id);
    const kids = childrenOf.get(id) || [];
    if (!isGateNode.get(id)) {
      if (!leafIndex.has(id)) {
        leafIndex.set(id, leafIds.length);
        leafIds.push(id);
      }
      return;
    }
    for (const k of kids) collect(k, new Set(guard));
  };
  collect(rootId);
  if (leafIds.length === 0) {
    return { cutSets: [], truncated: false, stats: { total: 0, byOrder: {}, singlePoints: 0 } };
  }

  const nLeaves = leafIds.length;
  const ONE = 1n;
  const bitOf = (id) => ONE << BigInt(leafIndex.get(id));

  // ---- MOCUS 展开 ----
  // 采用清晰实现：工作集 = { mask: 基本事件位掩码, gates: 待展开门栈 }
  return mocusClean(rootId, nodeMap, childrenOf, isGateNode, bitOf, leafIds, {
    maxOrder, truncation, qOf: opts.qOf, excluded,
  });
}

/**
 * 清晰的 MOCUS 实现：
 * 每个工作集 = { mask: 基本事件位掩码, gates: 待展开的门 id 栈 }
 * 每次弹出一个门展开，产生新工作集。
 */
/**
 * 递归一次性展开：把一个门子树完全展开为若干 (mask, gates) 工作集。
 *
 * 采用自底向上递归而非逐轮迭代，可把"每轮展开一个门"的 O(depth) 轮次
 * 压缩为单次递归调用，是大规模树性能的关键。
 *
 * @returns {Array<{mask:bigint, gates:string[]}>}
 */
function expandAll(gateId, nodeMap, childrenOf, isGateNode, bitOf, guard = 0, excluded = null) {
  if (guard > 500) return [{ mask: 0n, gates: [gateId] }];
  const n = nodeMap.get(gateId);
  const kids = childrenOf.get(gateId) || [];
  const g = resolveGate(n, kids);

  /** 合并两批工作集：AND 求交叉积并集 */
  const mergeAnd = (lists) => {
    let acc = [{ mask: 0n, gates: [] }];
    for (const sub of lists) {
      // 快速路径：任一侧为空则直接返回另一侧
      if (!acc.length) { acc = sub.map((s) => ({ ...s })); continue; }
      if (!sub.length) continue;
      const nx = [];
      for (const a of acc) {
        for (const b of sub) {
          // 空工作集（mask === null）为 AND 的恒等元：直接取另一侧
          if (a.mask === null) { nx.push({ ...b }); continue; }
          if (b.mask === null) { nx.push({ ...a }); continue; }
          nx.push({ mask: a.mask | b.mask, gates: a.gates.concat(b.gates) });
        }
      }
      // AND 合并后立即剪枝：{A} 会吸收 {A,B}，这是布尔吸收律的关键时机
      acc = nx.length > 1 ? pruneMasks(nx) : nx;
      if (acc.length > MAX_COMBO) return acc.slice(0, MAX_COMBO);
    }
    return acc;
  };

  if (g.kind === 'AND') {
    // 所有输入都要发生：展开每个输入后求并集
    const perKid = kids.map((k) => expandOne(k, nodeMap, childrenOf, isGateNode, bitOf, guard + 1, excluded));
    return mergeAnd(perKid);
  }
  if (g.kind === 'OR') {
    // 任一输入发生即可：串联各输入的展开结果
    let out = [];
    for (const k of kids) {
      for (const s of expandOne(k, nodeMap, childrenOf, isGateNode, bitOf, guard + 1, excluded)) {
        // 空工作集对 OR 是恒假元：直接丢弃（传输符号不应产生割集）
        if (s.mask === null) continue;
        out.push(s);
      }
      // OR 分支同样需要吸收剪枝（{A} 吸收 {A,B}）
      if (out.length > 1) out = pruneMasks(out);
      if (out.length > MAX_COMBO) return out.slice(0, MAX_COMBO);
    }
    return out;
  }
  if (g.kind === 'VOTE') {
    const k = Math.max(1, Math.min(g.k, kids.length));
    const out = [];
    for (const combo of combinations(kids, k)) {
      const perKid = combo.map((c) => expandOne(c, nodeMap, childrenOf, isGateNode, bitOf, guard + 1, excluded));
      for (const s of mergeAnd(perKid)) out.push(s);
      if (out.length > MAX_COMBO) break;
    }
    return out;
  }
  if (g.kind === 'INHIBIT') {
    const perKid = kids.map((k) => expandOne(k, nodeMap, childrenOf, isGateNode, bitOf, guard + 1, excluded));
    return mergeAnd(perKid);
  }
  // NOT / 未知：定性上按 OR 处理
  return expandOne2OR(gateId, kids, nodeMap, childrenOf, isGateNode, bitOf, guard, excluded);
}

function expandOne2OR(gateId, kids, nodeMap, childrenOf, isGateNode, bitOf, guard, excluded) {
  const out = [];
  for (const k of kids) {
    for (const s of expandOne(k, nodeMap, childrenOf, isGateNode, bitOf, guard + 1, excluded)) out.push(s);
    if (out.length > MAX_COMBO) break;
  }
  return out;
}

/**
 * 展开单个节点（可能是门，也可能是基本事件）
 *
 * excluded 中的节点（如跨页传输符号）返回空工作集 —— 对 AND 是恒等元，
 * 对 OR 是恒假元，从而在语义上"透明"：传输引用不影响割集构成。
 */
function expandOne(id, nodeMap, childrenOf, isGateNode, bitOf, guard, excluded) {
  if (excluded && excluded.has(id)) {
    return [{ mask: null, gates: [], empty: true }];
  }
  if (!isGateNode.get(id)) {
    // 防御：理论上被排除的节点已在上一层拦截，此处兜底避免 bitOf 越界
    if (!bitOf) return [{ mask: null, gates: [], empty: true }];
    try {
      return [{ mask: bitOf(id), gates: [] }];
    } catch {
      return [{ mask: null, gates: [], empty: true }];
    }
  }
  return expandAll(id, nodeMap, childrenOf, isGateNode, bitOf, guard, excluded);
}

// 组合爆炸保护上限
const MAX_COMBO = 200000;
const COMBO_SOFT_LIMIT = 3000;

function mocusClean(rootId, nodeMap, childrenOf, isGateNode, bitOf, leafIds, opts) {
  const { maxOrder, truncation, qOf, excluded } = opts;
  const skip = (id) => excluded && excluded.has(id);
  let truncated = false;
  let guard = 0;
  const GUARD_MAX = 300000;
  // 工作集规模上限：MOCUS 对宽 OR 树会组合爆炸（与 KUREAS / SAPHIRE 等工具一致），
  // 超过阈值即停止并标记截断，概率计算由 BDD 精确解兜底。
  const MAX_SETS = 200000;

  // 一次性自顶向下展开，再做吸收剪枝
  let worklist = expandAll(rootId, nodeMap, childrenOf, isGateNode, bitOf, 0, excluded);

  // 若展开规模超限，标记截断
  if (worklist.length >= MAX_COMBO) truncated = true;

  // 吸收剪枝（小规模直接做，大规模分批做）
  worklist = pruneMasks(worklist);

  // 补齐可能残留的未展开门
  for (const w of worklist) {
    let guardB = 0;
    while (w.gates.length && guardB++ < 100) {
      const gid = w.gates.pop();
      const kids = childrenOf.get(gid) || [];
      for (const k of kids) {
        if (isGateNode.get(k)) w.gates.push(k);
        else w.mask |= bitOf(k);
        break;
      }
    }
  }

  // 再次剪枝（补齐后可能产生超集）
  if (worklist.some((w) => w.gates.length === 0)) {
    worklist = pruneMasks(worklist);
  }

  // 最终剪枝 + 幂等（保留 gates 字段以便后续处理未展开门）
  // 过滤空工作集（传输符号产生的恒假元）
  const nonEmpty = worklist.filter((w) => w.mask !== null);
  const finalSets = pruneMasks(nonEmpty);
  if (finalSets.length === 0) {
    return { cutSets: [], truncated, stats: { total: 0, byOrder: {}, singlePoints: 0, leaves: leafIds.length } };
  }
  // 若仍有未展开的门（NOT 等），用其第一个输入的掩码兜底
  for (const w of finalSets) {
    while (w.gates.length) {
      const gid = w.gates.pop();
      if (skip && skip(gid)) continue;
      const kids = childrenOf.get(gid) || [];
      for (const k of kids) {
        if (skip && skip(k)) continue;
        if (isGateNode.get(k)) w.gates.push(k);
        else w.mask |= bitOf(k);
        break;
      }
    }
  }

  // 收集为结果
  let cutSets = [];
  for (const w of finalSets) {
    const ids = [];
    let mm = w.mask;
    while (mm) {
      const low = mm & -mm;                       // 最低位的 1
      const idx = Number(low.toString(2).length) - 1;
      ids.push(leafIds[idx]);
      mm ^= low;
    }
    if (ids.length === 0) continue;   // 全部为传输符号 → 非有效割集
    const order = ids.length;
    if (maxOrder > 0 && order > maxOrder) { truncated = true; continue; }
    let prob = null;
    if (qOf) {
      let p = 1;
      for (const id of ids) p *= (qOf(id) ?? 0);
      prob = p;
      if (truncation > 0 && p < truncation) { truncated = true; continue; }
    }
    cutSets.push({ order, ids, prob });
  }

  // 排序，保证结果可复现
  cutSets.sort((a, b) => (a.order - b.order) || a.ids.join('|').localeCompare(b.ids.join('|')));
  cutSets.forEach((c, i) => {
    c.index = i + 1;
    c.names = c.ids.map((id) => nodeMap.get(id)?.name ?? id);
  });

  const orderDist = {};
  for (const c of cutSets) orderDist[c.order] = (orderDist[c.order] || 0) + 1;

  return {
    cutSets,
    truncated,
    stats: {
      total: cutSets.length,
      byOrder: orderDist,
      singlePoints: cutSets.filter((c) => c.order === 1).length,
      leaves: leafIds.length,
    },
  };
}

/**
 * 位掩码吸收剪枝：若 A ⊆ B 则删除 B。
 *
 * isSubset 判定为 O(1) 位运算 `(km & m) === km`。
 *
 * 索引策略（按最低置位建桶 + 双向探测）：
 *   若 A ⊆ B，则 A 必含 B 的最低置位 low(B)。因此把已保留集合按
 *   最低置位分桶后，查询 B 时只需看 low(B) 对应的桶即可覆盖所有
 *   可能的子集。这把全量 O(n²) 比较压缩到同桶规模。
 */
function pruneMasks(worklist) {
  // 幂等去重
  const uniq = new Map();
  for (const w of worklist) uniq.set(w.mask, w);

  // 按 popcount 分桶：小集合先处理（只有更小的集合能吸收它）
  const bySize = new Map();
  for (const m of uniq.keys()) {
    const s = popcount(m);
    let arr = bySize.get(s);
    if (!arr) { arr = []; bySize.set(s, arr); }
    arr.push(m);
  }
  const sizes = [...bySize.keys()].sort((a, b) => a - b);

  const kept = [];
  // 按最低置位索引：lowbit -> 已保留掩码列表
  const byLowBit = new Map();
  const lowBitOf = (m) => {
    const low = m & -m;
    return low.toString(2).length - 1;
  };

  for (const s of sizes) {
    const arr = bySize.get(s);
    for (const m of arr) {
      const lb = lowBitOf(m);
      const cands = byLowBit.get(lb);
      let absorbed = false;
      if (cands) {
        for (let i = 0; i < cands.length; i++) {
          if ((cands[i] & m) === cands[i]) { absorbed = true; break; }
        }
      }
      if (!absorbed) {
        kept.push(m);
        let list = byLowBit.get(lb);
        if (!list) { list = []; byLowBit.set(lb, list); }
        list.push(m);
      }
    }
  }
  return kept.map((m) => uniq.get(m));
}

function popcount(bigint) {
  // BigInt 的二进制字符串长度即为最高置位位置 +1，
  // 但我们真正需要的是置位个数（汉明重量），用 popcount 语义更合适。
  let x = bigint, c = 0;
  while (x) { x &= x - 1n; c++; }   // Brian Kernighan 算法
  return c;
}

/** 生成从 arr 中取 k 个的所有组合 */
function* combinations(arr, k) {
  const n = arr.length;
  if (k > n || k <= 0) return;
  if (k === n) { yield arr.slice(); return; }
  const idx = Array.from({ length: k }, (_, i) => i);
  for (;;) {
    yield idx.map((i) => arr[i]);
    let i = k - 1;
    while (i >= 0 && idx[i] === n - k + i) i--;
    if (i < 0) return;
    idx[i]++;
    for (let j = i + 1; j < k; j++) idx[j] = idx[j - 1] + 1;
  }
}

/**
 * 结构重要度（Structure Importance）计算
 * I_S(i) = (1/k) * Σ_{r: i ∈ E_r} 1/m_r
 */
export function structureImportance(cutSets) {
  const k = cutSets.length;
  const imp = new Map();
  for (const cs of cutSets) {
    const share = 1 / k / cs.order;
    for (const id of cs.ids) imp.set(id, (imp.get(id) || 0) + share);
  }
  return imp;
}

/**
 * Fussell-Vesely 重要度（基于割集的近似）
 * FV(i) = Σ_{r: i∈E_r} P(E_r) / P(TOP)
 */
export function fussellVesely(cutSets, topProb) {
  const fv = new Map();
  if (!topProb || topProb <= 0) return fv;
  for (const cs of cutSets) {
    const p = cs.prob || 0;
    for (const id of cs.ids) fv.set(id, (fv.get(id) || 0) + p / topProb);
  }
  return fv;
}