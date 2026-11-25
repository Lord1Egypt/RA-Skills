/**
 * FTA Studio - 故障树自动布局引擎
 *
 * 采用改进的 Reingold-Tilford 有序树布局：
 *   - 逐层分配 X 坐标（保证同级子树不重叠、保持阅读顺序）
 *   - 门与事件纵向分层，连接线为正交折线
 *   - 支持子树折叠后自动重排
 */

import { buildIndex, findTopEvent } from './model.mjs';

const NODE_W = 150;      // 事件框宽度
const NODE_H = 46;       // 事件框高度
const GATE_SIZE = 34;    // 门符号边长
const LEVEL_GAP = 78;    // 层间距（门到事件）
const SIB_GAP = 26;      // 同层节点间距
const SUBTREE_GAP = 20;  // 子树间距

/**
 * @returns {{nodes:Map, width:number, height:number, links:Array}}
 */
export function layout(tree, opts = {}) {
  const { nodeMap, childrenOf, parentOf } = buildIndex(tree);
  const rootId = findTopEvent(tree);
  if (!rootId) return { nodes: new Map(), width: 0, height: 0, links: [] };

  // 多根支持（森林）：分页后的每一页只保留本页节点，
  // 页首那些"上一层被截断"的事件自然成为本页的顶事件，可能有多个。
  const roots = tree.nodes
    .filter((n) => !((parentOf.get(n.id) || []).length))
    .map((n) => n.id);
  if (!roots.length) roots.push(rootId);
  const rootSet = new Set(roots);

  const collapsed = new Set();
  for (const n of tree.nodes) if (n.collapsed && !rootSet.has(n.id)) collapsed.add(n.id);

  // 计算子树宽度
  const widthCache = new Map();
  const leafCount = new Map();
  const orderCache = new Map();

  /** 树有序遍历：保持原始子节点顺序 */
  const orderedChildren = (id) => childrenOf.get(id) || [];

  function subtreeWidth(id) {
    if (widthCache.has(id)) return widthCache.get(id);
    const n = nodeMap.get(id);
    const kids = collapsed.has(id) ? [] : orderedChildren(id);
    let w;
    if (kids.length === 0) {
      w = NODE_W;
    } else {
      let total = 0;
      for (const k of kids) total += subtreeWidth(k) + SUBTREE_GAP;
      total -= SUBTREE_GAP;
      w = Math.max(NODE_W, total);
    }
    widthCache.set(id, w);
    return w;
  }

  function countLeaves(id) {
    if (leafCount.has(id)) return leafCount.get(id);
    const kids = collapsed.has(id) ? [] : orderedChildren(id);
    let c;
    if (kids.length === 0) c = 1;
    else c = kids.reduce((a, k) => a + countLeaves(k), 0);
    leafCount.set(id, c);
    return c;
  }

  const positions = new Map();
  let depthCounter = 0;

  // 分配：父节点居中于子节点之上
  function assign(id, depth, leftX) {
    const n = nodeMap.get(id);
    const w = subtreeWidth(id);
    const kids = collapsed.has(id) ? [] : orderedChildren(id);
    const myX = leftX + w / 2;

    positions.set(id, { x: myX, depth, node: n });

    if (kids.length === 0) return;

    // 门节点位于父事件正下方
    const gateX = myX;
    const gateY = depth * LEVEL_GAP + NODE_H;

    let cursor = leftX;
    // 计算每个子树起始 x，使整体居中
    let kidsTotalW = 0;
    for (const k of kids) kidsTotalW += subtreeWidth(k) + SUBTREE_GAP;
    kidsTotalW -= SUBTREE_GAP;
    let startX = myX - kidsTotalW / 2;

    for (const k of kids) {
      const kw = subtreeWidth(k);
      assign(k, depth + 1, startX);
      startX += kw + SUBTREE_GAP;
    }
    positions.get(id).gateX = gateX;
    positions.get(id).gateY = gateY;
  }

  // 依次摆放各个根（单页森林里通常只有一个，分页视图可能有多个）
  let cursorX = 0;
  for (const r of roots) {
    assign(r, 0, cursorX);
    cursorX += subtreeWidth(r) + SUBTREE_GAP;
  }

  // 计算包围盒
  let minX = Infinity, maxX = -Infinity, maxY = 0;
  const nodes = new Map();
  for (const [id, pos] of positions) {
    const x = pos.x - NODE_W / 2;
    const y = pos.depth * LEVEL_GAP;
    nodes.set(id, {
      id,
      node: pos.node,
      x,
      y,
      cx: pos.x,
      cy: y + NODE_H / 2,
      w: NODE_W,
      h: NODE_H,
      gateX: pos.gateX ?? pos.x,
      gateY: pos.gateY ?? (y + NODE_H),
      depth: pos.depth,
      collapsed: collapsed.has(id),
    });
    minX = Math.min(minX, x);
    maxX = Math.max(maxX, x + NODE_W);
    maxY = Math.max(maxY, y + NODE_H + LEVEL_GAP * 0.4);
  }

  const pad = 40;
  // 归一化到正坐标
  for (const nd of nodes.values()) {
    nd.x -= minX - pad;
    nd.cx -= minX - pad;
    nd.gateX -= minX - pad;
  }

  const width = maxX - minX + pad * 2;
  const height = maxY + pad;

  // 生成连接线（正交折线路径）
  const links = [];
  for (const parentId of positions.keys()) {
    const kids = collapsed.has(parentId) ? [] : orderedChildren(parentId);
    if (!kids.length) continue;
    const p = nodes.get(parentId);
    for (const k of kids) {
      const c = nodes.get(k);
      if (!c) continue;
      links.push({
        from: parentId,
        to: k,
        // 正交折线：从门底部 -> 竖直 -> 水平 -> 竖直到子节点顶部
        path: orthogonalPath(
          p.gateX, p.gateY,
          c.cx, c.y,
          p.gateY + 22,
        ),
        // 扇出时用圆角折线更美观（半径由层间空隙反推，不会越过子节点顶部）
        curve: orthogonalCurve(p.gateX, p.gateY, c.cx, c.y),
      });
    }
  }

  return { nodes, links, width, height, rootId };
}

/**
 * 正交折线：竖-横-竖
 * 注意：横向段必须落在「起点与终点之间」，否则会越过子节点顶部再折回，
 * 视觉上表现为横线与箭头脱开。
 */
function orthogonalPath(x1, y1, x2, y2, midY) {
  const span = y2 - y1;
  const my = typeof midY === 'number'
    ? Math.min(Math.max(midY, y1 + 4), y2 - 4)
    : y1 + span / 2;
  if (Math.abs(x1 - x2) < 0.5) {
    return `M ${x1} ${y1} L ${x2} ${y2}`;
  }
  return `M ${x1} ${y1} L ${x1} ${my} L ${x2} ${my} L ${x2} ${y2}`;
}

/**
 * 平滑折线（圆角拐弯）
 *
 * 关键约束：一次折弯要在竖直方向占 2r（先拐进去、再拐出来），
 * 因此 r 必须由「可用竖直空间 span」反推，并保证 my + 2r <= y2。
 * 旧实现固定 my = gateY + 20、r 最大 24，而层间空隙只有 32px，
 * 结果横线跑到子节点顶部下方，再向上折回 —— 箭头与横线看起来没连上。
 */
function orthogonalCurve(x1, y1, x2, y2) {
  if (Math.abs(x1 - x2) < 0.5) {
    return `M ${x1} ${y1} L ${x2} ${y2}`;
  }
  const span = Math.max(0, y2 - y1);
  const s = Math.sign(x2 - x1);
  const r = Math.max(2, Math.min(14, Math.abs(x2 - x1) / 2, span / 3));
  const my = Math.max(y1 + 2, Math.min(y1 + span * 0.35, y2 - 2 * r - 2));
  return [
    `M ${x1} ${y1}`,
    `L ${x1} ${my}`,
    `Q ${x1} ${my + r} ${x1 + s * r} ${my + r}`,
    `L ${x2 - s * r} ${my + r}`,
    `Q ${x2} ${my + r} ${x2} ${my + 2 * r}`,
    `L ${x2} ${y2}`,
  ].join(' ');
}

/**
 * 大纲视图：生成树形文本大纲
 */
export function outline(tree) {
  const { nodeMap, childrenOf } = buildIndex(tree);
  const rootId = findTopEvent(tree);
  if (!rootId) return [];
  const lines = [];
  const walk = (id, depth, prefix = '') => {
    const n = nodeMap.get(id);
    if (!n) return;
    const kids = childrenOf.get(id) || [];
    lines.push({
      depth,
      id,
      type: n.type,
      name: n.name,
      gate: n.gate,
      collapsed: n.collapsed,
      children: kids.length,
      prob: n.prob,
      ref: n.ref,
    });
    if (n.collapsed) return;
    kids.forEach((k, i) => {
      const last = i === kids.length - 1;
      walk(k, depth + 1, prefix + (last ? '└─ ' : '├─ '));
    });
  };
  walk(rootId, 0);
  return lines;
}