/**
 * FTA Studio - 共享辅助函数
 */

import { buildIndex, findTopEvent } from './model.mjs';
import { quantify } from './quantify.mjs';

/**
 * 为每个节点计算热力值（0~1）。
 * 叶子用自身重要度；中间节点取子树内最大值 —— 直观反映"该子树整体风险"。
 * 与 api.mjs 中的 buildNodeHeatmap 逻辑一致，供 CLI / server 复用。
 * @param {object} tree
 * @param {object|null} result quantify() 输出，若为空则内部自动计算
 */
export function buildNodeHeatmapForCLI(tree, result = null) {
  const { childrenOf } = buildIndex(tree);

  if (!result) {
    result = quantify(tree);
  }

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
  for (const n of tree.nodes) if (!heat.has(n.id)) heat.set(n.id, 0);

  return heat;
}