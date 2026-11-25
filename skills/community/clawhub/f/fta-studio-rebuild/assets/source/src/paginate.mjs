/**
 * FTA Studio - 跨页 / 多图支持
 *
 * 对标 medini analyze 的 "handle large fault trees by multiple diagrams"。
 *
 * 原理：大故障树按「子树」切分为多页，页边界处放置传输符号
 * （三角形）建立跨页引用：
 *   - transfer_out：本页某事件的展开在下一页
 *   - transfer_in ：本页某事件的内容来自上一页
 *
 * 划分算法（保证子树完整、不过度碎片化）：
 *   1) 从顶事件开始 BFS 遍历各子树
 *   2) 逐个把完整子树放入当前页，直到超出 maxNodes
 *   3) 超限时开启新页，并在两页间建立传输引用
 *   4) 若单个子树本身超过 maxNodes，则递归细分该子树
 */

import { buildIndex, findTopEvent } from './model.mjs';

/**
 * 将故障树切分为多页
 * @param {object} tree
 * @param {object} opts
 *   maxNodes   每页最大节点数（默认 24）
 *   maxDepth   单页最大层级深度（默认 5）
 *   maxPages   最大页数（默认 60）
 */
export function paginate(tree, opts = {}) {
  const maxNodes = opts.maxNodes ?? 24;
  const maxDepth = opts.maxDepth ?? 5;
  const maxPages = opts.maxPages ?? 60;

  const { nodeMap, childrenOf } = buildIndex(tree);
  const rootId = findTopEvent(tree);
  if (!rootId) return { pages: [], pageOf: new Map(), references: [], rootId: null };

  const pages = [];
  const pageOf = new Map();
  const references = [];

  const subtreeCache = new Map();
  function subtreeIds(id) {
    if (subtreeCache.has(id)) return subtreeCache.get(id);
    const acc = new Set();
    const stack = [id];
    while (stack.length) {
      const cur = stack.pop();
      if (acc.has(cur)) continue;
      acc.add(cur);
      const n = nodeMap.get(cur);
      if (!n) continue;
      const kids = childrenOf.get(cur) || [];
      // 展开门节点，但遇到传输/注释节点停止
      if (n.collapsed) continue;
      for (const k of kids) stack.push(k);
    }
    subtreeCache.set(id, acc);
    return acc;
  }

  function depthOf(id) {
    const { parentOf } = buildIndex(tree);
    let d = 0, cur = id;
    const seen = new Set();
    while (!seen.has(cur)) {
      seen.add(cur);
      const ps = parentOf.get(cur) || [];
      if (!ps.length) break;
      cur = ps[0];
      d++;
    }
    return d;
  }

  function newPage(title) {
    const p = {
      index: pages.length + 1,
      nodes: new Set(),
      title: title || `第 ${pages.length + 1} 页`,
      roots: [],
      continuedFrom: null,
      continuesTo: [],
      depthBase: 0,
    };
    pages.push(p);
    return p;
  }

  let current = newPage(nodeMap.get(rootId)?.name || '故障树');
  current.depthBase = depthOf(rootId);

  /**
   * 递归分配：把 node 的整棵子树放入页面，必要时切分
   * 注意：isRoot 时仅保证「顶事件本身」在首页，不豁免整棵树的容量检查，
   * 否则大树永远不会被切分。
   */
  function allocate(nodeId, isRoot = false) {
    if (pages.length >= maxPages) return;

    const ids = subtreeIds(nodeId);
    const size = ids.size;

    // 顶事件自身：即使超容量也先放进当前页（保证树有根）
    if (isRoot && current.nodes.size === 0) {
      pageOf.set(nodeId, current.index);
      current.nodes.add(nodeId);
      if (!current.roots.includes(nodeId)) current.roots.push(nodeId);
      current.title = nodeMap.get(nodeId)?.name || current.title;
      for (const k of childrenOf.get(nodeId) || []) allocate(k);
      return;
    }

    // 能放入当前页
    if (current.nodes.size + size <= maxNodes) {
      for (const nid of ids) {
        if (!pageOf.has(nid)) {
          pageOf.set(nid, current.index);
          current.nodes.add(nid);
        }
      }
      if (!current.roots.includes(nodeId)) current.roots.push(nodeId);
      if (!current.title || /^第 \d+ 页$/.test(current.title)) {
        current.title = nodeMap.get(nodeId)?.name || current.title;
      }
      return;
    }

    // 放不下：需要切分
    const n = nodeMap.get(nodeId);
    const kids = childrenOf.get(nodeId) || [];

    // 当前页太空（通常只有根节点）：先把它自己放进本页，子节点继续分配。
    // 否则"子树超容量就封页"会制造出只剩 1 个节点的空白页
    // （233 节点的树曾出现 [1,1,1,22,...] 的分布）。
    if (current.nodes.size <= 2) {
      if (!pageOf.has(nodeId)) {
        pageOf.set(nodeId, current.index);
        current.nodes.add(nodeId);
      }
      if (!current.roots.includes(nodeId)) current.roots.push(nodeId);
      for (const k of kids) {
        allocate(k);
        if (pages.length >= maxPages) break;
      }
      return;
    }

    // 若该节点本身过大（子树超过单页容量），递归细分其子节点
    if (size > maxNodes) {
      const prevPage = current;

      // 若当前页已有内容，先封页
      if (current.nodes.size > 0) {
        // 该子树在上一页留下传输转出
        prevPage.continuesTo.push({ nodeId, label: n?.name || nodeId });
        references.push({
          type: 'transfer_out', nodeId,
          fromPage: prevPage.index, label: n?.name || nodeId,
        });
        current = newPage(n?.name || nodeId);
      }
      current.continuedFrom = { nodeId, fromPage: prevPage.index, label: n?.name || nodeId };
      references.push({
        type: 'transfer_in', nodeId,
        toPage: current.index, fromPage: prevPage.index, label: n?.name || nodeId,
      });
      current.roots.push(nodeId);

      // 先放入自身，再逐个分配子树
      pageOf.set(nodeId, current.index);
      current.nodes.add(nodeId);

      for (const k of kids) {
        allocate(k);
        if (pages.length >= maxPages) break;
      }
      return;
    }

    // 子树大小适中但当前页放不下：整体移到新页
    const prevPage = current;
    if (current.nodes.size > 0) {
      prevPage.continuesTo.push({ nodeId, label: n?.name || nodeId });
      references.push({
        type: 'transfer_out', nodeId,
        fromPage: prevPage.index, label: n?.name || nodeId,
      });
      current = newPage(n?.name || nodeId);
    }
    current.continuedFrom = { nodeId, fromPage: prevPage.index, label: n?.name || nodeId };
    references.push({
      type: 'transfer_in', nodeId,
      toPage: current.index, fromPage: prevPage.index, label: n?.name || nodeId,
    });
    // 整体放入新页
    for (const nid of ids) {
      if (!pageOf.has(nid)) {
        pageOf.set(nid, current.index);
        current.nodes.add(nid);
      }
    }
    if (!current.roots.includes(nodeId)) current.roots.push(nodeId);
  }

  allocate(rootId, true);

  // 收尾：补全标题与引用目标页
  for (const p of pages) {
    if (!p.title) p.title = `第 ${p.index} 页`;
    for (const c of p.continuesTo) {
      const target = pageOf.get(c.nodeId);
      if (target) c.toPage = target;
    }
  }
  // 去掉空白页
  const nonEmpty = pages.filter((p) => p.nodes.size > 0);
  nonEmpty.forEach((p, i) => { p.index = i + 1; });

  return {
    pages: nonEmpty,
    pageOf,
    references,
    rootId,
    maxNodes,
  };
}

/**
 * 为分页结果生成「视图树」——每页一棵独立的子树，用于渲染/导出。
 *
 * 设计要点（重要）：
 *   分页是**纯显示层**概念。原始树保持完整，计算（割集/概率）始终基于原树，
 *   因此不存在"节点被搬走导致割集丢失"的风险。
 *   每个页面视图 = 该页节点 + 其页内祖先链（保证结构完整可读），
 *   页边界用传输符号（三角形）标注跳转关系。
 *
 * @param {object} tree 完整树
 * @param {object} pag 分页结果
 * @param {number} pageIndex 目标页（1 起）
 * @returns {object} 该页的视图树（可直接交给 renderSVG）
 */
export function buildPageView(tree, pag, pageIndex) {
  const page = pag.pages.find((p) => p.index === pageIndex);
  if (!page) return null;

  const { childrenOf, parentOf } = buildIndex(tree);
  const pageSet = page.nodes;

  // 收集需要保留的节点：页内节点 + 连接它们的祖先路径
  const keep = new Set(pageSet);

  // 页内节点的祖先链（跨页时向上追溯直到遇到也在本页的节点）
  const ancestorsOf = (id) => {
    const chain = [];
    let cur = id;
    const seen = new Set();
    while (cur && !seen.has(cur)) {
      seen.add(cur);
      const ps = parentOf.get(cur) || [];
      if (!ps.length) break;
      cur = ps[0];
      chain.push(cur);
      if (pageSet.has(cur)) break;  // 已在本页，无需再往上
    }
    return chain;
  };

  for (const id of pageSet) {
    for (const a of ancestorsOf(id)) keep.add(a);
  }

  // 视图节点：仅保留 keep 内的节点
  const viewNodes = tree.nodes.filter((n) => keep.has(n.id)).map((n) => ({ ...n }));

  // 视图连接：两端都在 keep 内
  const viewConns = tree.connections.filter((c) => keep.has(c.from) && keep.has(c.to));

  // 注入传输符号标注
  const extraNodes = [];
  const extraConns = [];
  let seq = 0;

  // 承接上一页
  if (page.continuedFrom) {
    seq++;
    const tid = `P${pageIndex}I`;
    extraNodes.push({
      ...emptyTransfer(tid, 'transfer_in',
        `转自第 ${page.continuedFrom.fromPage} 页`,
        page.continuedFrom.fromPage, page.continuedFrom.label),
    });
    // 挂到本页根节点上
    const root = page.roots?.[0];
    if (root && keep.has(root)) extraConns.push({ from: tid, to: root });
    else if (root) { extraNodes[0].orphanOf = root; }
  }

  // 续见下一页
  for (const c of page.continuesTo || []) {
    seq++;
    const tid = `P${pageIndex}O${seq}`;
    extraNodes.push({
      ...emptyTransfer(tid, 'transfer_out',
        c.toPage ? `续见第 ${c.toPage} 页` : '续见下一页',
        c.toPage ?? null, c.label),
    });
    // 在原位置替换指向该子树的连接
    for (const conn of viewConns) {
      if (conn.to === c.nodeId) conn.to = tid;
    }
  }

  return {
    version: tree.version,
    meta: { ...tree.meta, title: tree.meta?.title, pageTitle: page.title, pageIndex },
    settings: tree.settings,
    nodes: [...viewNodes, ...extraNodes],
    connections: [...viewConns, ...extraConns],
  };
}

function emptyTransfer(id, type, name, target, desc) {
  return {
    id, type, name, gate: null,
    transferRef: target, transferTarget: target,
    description: desc || '',
    ref: '', component: '', failureMode: '', owner: '',
    probModel: 'fixed', prob: 0, lambda: null, eta: null, beta: null,
    demandCount: null, demandProb: null, repairTime: null, monitorInterval: null,
    notes: '', collapsed: false, x: null, y: null,
  };
}

/**
 * 兼容旧接口：在完整树上追加传输标记节点，**不改动原有结构**。
 *
 * 重要设计原则：分页是纯显示层概念，定量计算必须始终基于完整原树。
 * 因此这里只**追加**传输节点用于图上标注，绝不删除或改写原有连接 ——
 * 否则被"搬到下一页"的子树会与其父节点断开，导致割集丢失。
 * 真正的分页渲染请使用 buildPageView()。
 */
export function injectTransfers(tree, pag) {
  if (!pag || !pag.pages || pag.pages.length <= 1) return tree;

  const cloned = JSON.parse(JSON.stringify(tree));
  const newNodes = [];
  let seq = 0;

  for (const page of pag.pages) {
    for (const c of page.continuesTo || []) {
      seq++;
      newNodes.push(emptyTransfer(`X${String(seq).padStart(3, '0')}`, 'transfer_out',
        c.toPage ? `续见第 ${c.toPage} 页` : '续见下一页',
        c.toPage ?? null, c.label));
    }
    if (page.continuedFrom) {
      seq++;
      newNodes.push(emptyTransfer(`X${String(seq).padStart(3, '0')}`, 'transfer_in',
        `转自第 ${page.continuedFrom.fromPage} 页`,
        page.continuedFrom.fromPage, page.continuedFrom.label));
    }
  }

  cloned.nodes.push(...newNodes);
  // 不改动 connections：传输符号为孤立标注节点，由渲染层按需挂接
  return cloned;
}

/** 分页摘要（供报告与 UI 使用） */
export function paginateSummary(pag) {
  return pag.pages.map((p) => ({
    index: p.index,
    title: p.title,
    nodeCount: p.nodes.size,
    roots: p.roots,
    continuedFrom: p.continuedFrom ? { fromPage: p.continuedFrom.fromPage } : null,
    continuesTo: (p.continuesTo || []).map((c) => ({ toPage: c.toPage, label: c.label })),
  }));
}

/**
 * 自动分页：小树返回单页，大树切分
 */
export function autoPaginate(tree, opts = {}) {
  const total = tree.nodes.length;
  const threshold = opts.threshold ?? 40;
  if (total <= threshold && !opts.force) {
    const rootId = findTopEvent(tree);
    const nodes = new Set(tree.nodes.map((n) => n.id));
    return {
      pages: [{
        index: 1, nodes, title: tree.meta?.title || '故障树',
        roots: rootId ? [rootId] : [], continuedFrom: null, continuesTo: [],
      }],
      pageOf: new Map([...nodes].map((id) => [id, 1])),
      references: [],
      rootId,
      single: true,
    };
  }
  return { ...paginate(tree, opts), single: false };
}

/**
 * 前沿推进分页（ISOGRAPH / medini 风格，导出用）
 *
 * 规则：
 *   1. 自上而下逐层展开，**同一事件的子事件整层一起加入**（不会拆散兄弟）；
 *   2. 本页展开到预算用尽为止，**最下面那一层只画框、不展开**；
 *   3. 下一页的顶事件 = 本页的最底层 —— 页与页竖向连续，而不是横向并列；
 *   4. 只有当某层节点不再有子事件时才结束，所以基本事件不会凭空"变成承接"；
 *   5. **每个手动分页点各开一页**（画图人原则：每次分页都从新的一页开始）。
 *      同一页触发的多个分页点按图中阅读顺序（DFS 先序 = 从左到右）依次开页，
 *      分页点的子树内部再遇到分页点时同样继续顺延开页。
 *
 * @param {object} tree
 * @param {object} opts.budget 每页大致事件数（默认 14）
 */
export function paginateBanded(tree, opts = {}) {
  const budget = Math.max(4, Number(opts.budget) || 14);
  const { nodeMap, childrenOf } = buildIndex(tree);
  const rootId = findTopEvent(tree);
  if (!rootId) return { pages: [], rootId, budget };

  // 手动分页点：画图的人指定"此事件另起一页"。只有还有子事件的事件才有效。
  const breakSet = new Set(
    tree.nodes
      .filter((n) => n.pageBreak && (childrenOf.get(n.id) || []).length)
      .map((n) => n.id)
  );

  // DFS 先序编号：多个分页点落在同一页时，按阅读顺序决定谁先开新页
  const dfsIndex = new Map();
  let dfsCounter = 0;
  (function walk(id) {
    if (dfsIndex.has(id)) return;
    dfsIndex.set(id, dfsCounter++);
    for (const k of childrenOf.get(id) || []) walk(k);
  })(rootId);

  const pages = [];

  /** 展开一页：tops 为本页顶事件（上一页的分页点或页底层），contFrom 为承接的页号 */
  function expandPage(tops, contFrom) {
    if (pages.length >= 400) return;
    const page = {
      index: pages.length + 1,
      tops: tops.slice(),
      nodes: new Set(tops),
      bottom: [],
      breakNodes: [],
      continuedFrom: contFrom,
      topNames: tops.map((id) => nodeMap.get(id)?.name || id),
      title: nodeMap.get(tops[0])?.name || `第 ${pages.length + 1} 页`,
      manual: false,
    };
    pages.push(page);

    let level = tops;
    let hitBreaks = [];
    let manualMode = false;

    while (true) {
      const next = [];
      for (const id of level) {
        for (const k of childrenOf.get(id) || []) next.push(k);
      }
      if (!next.length) break;

      const brk = next.filter((id) => breakSet.has(id));

      if (brk.length) {
        // 到达手动分页点：本层（含所有兄弟）留在此页，分页点不展开
        for (const k of next) page.nodes.add(k);
        hitBreaks.push(...brk);
        page.manual = true;
        manualMode = true;
        // 非分页的兄弟继续展开，避免它们的子树被丢到任何页之外
        const cont = next.filter((id) => !breakSet.has(id) && (childrenOf.get(id) || []).length);
        if (!cont.length) break;
        level = cont;
        continue;
      }

      // 自动模式：超预算就在本层停住，本层成为页底
      if (!manualMode && page.nodes.size + next.length > budget && level !== tops) break;

      for (const k of next) page.nodes.add(k);
      level = next;
    }

    page.bottom = hitBreaks.length ? [...new Set([...level, ...hitBreaks])] : level.slice();
    // 本页触发的分页点：它们各自是新一页的顶事件。
    // 本页要保留它们（画成虚线、不展开），表示"这一支已分到第 N 页"。
    page.breakNodes = [...new Set(hitBreaks)];

    // 每个分页点各开一页：按阅读顺序依次分配页号。
    // 分页点的子树内部若还有分页点，会在递归里继续顺延开页。
    const ordered = [...new Set(hitBreaks)]
      .sort((a, b) => (dfsIndex.get(a) ?? 0) - (dfsIndex.get(b) ?? 0));
    for (const b of ordered) expandPage([b], page.index);

    // 自动模式到预算停住：页底整层成为下一页顶事件（竖向连续）
    if (!hitBreaks.length) {
      const frontier = level.filter((id) => (childrenOf.get(id) || []).length);
      if (frontier.length) expandPage(frontier, page.index);
    }
  }

  expandPage([rootId], null);

  return { pages, rootId, budget, breakCount: breakSet.size };
}

/**
 * 前沿推进分页的页面视图：只含本页节点，页首即上一页的页底事件。
 * 不需要补承接父事件，也不需要存根 —— 兄弟天然齐全。
 */
export function buildBandedView(tree, pag, pageIndex) {
  const page = pag.pages.find((p) => p.index === pageIndex);
  if (!page) return null;
  const ids = page.nodes;
  return {
    version: tree.version,
    meta: {
      ...tree.meta,
      pageTitle: page.title,
      pageIndex,
      continuedFromPages: page.continuedFrom ? [page.continuedFrom] : [],
      continuedFromNames: page.continuedFrom ? page.topNames : [],
      // 本页触发的手动分页点：导出时画成虚线框，表示该支已分到下一页
      breakMarkerIds: (page.breakNodes || []).filter((id) => ids.has(id)),
      // 本页顶事件中"从上一页转过来"的那些：同样画虚线，表示上页已分页
      contMarkerIds: page.index > 1 ? page.tops.filter((id) => ids.has(id)) : [],
    },
    settings: tree.settings,
    nodes: tree.nodes.filter((n) => ids.has(n.id)).map((n) => ({ ...n })),
    connections: tree.connections.filter((c) => ids.has(c.from) && ids.has(c.to)),
  };
}

/**
 * 扁平页面视图（旧：子树分页 + 补齐兄弟）
 *
 * 保留用于排查对照；导出已改用 buildBandedView，
 * 因为子树分页是横向并排，页与页之间没有"上页底 = 下页顶"的连续关系。
 */
export function buildFlatView(tree, pag, pageIndex) {
  const page = pag.pages.find((p) => p.index === pageIndex);
  if (!page) return null;

  const { nodeMap, parentOf, childrenOf } = buildIndex(tree);
  const ids = page.nodes;

  // 本页真实顶事件：父节点不在本页
  const tops = tree.nodes
    .filter((n) => ids.has(n.id))
    .filter((n) => !(parentOf.get(n.id) || []).some((p) => ids.has(p)))
    .map((n) => n.id);

  // 只补「一级父事件」作为承接事件画在页首（**不追溯到根**）。
  // 这样页首的框下面有子事件、上面也能看到它挂在谁下面，
  // 而不是一个悬空、在任何页都找不到出处的孤立事件。
  const contextIds = new Set();
  for (const id of tops) {
    for (const p of parentOf.get(id) || []) {
      if (!ids.has(p) && nodeMap.has(p)) contextIds.add(p);
    }
  }

  const keep = new Set([...ids, ...contextIds]);

  // 关键约束：**同一个事件的子事件必须齐全**。
  // 子树分页会把兄弟节点拆到不同页，导致某页上父事件看起来只有一个孩子。
  // 这里把缺的兄弟补成"存根"（不再展开），并注明它的内容在第几页。
  const stubIds = new Set();
  const stubPages = {};
  const baseNodes = [...ids, ...contextIds];
  for (const nid of baseNodes) {
    for (const c of childrenOf.get(nid) || []) {
      if (keep.has(c)) continue;
      stubIds.add(c);
      keep.add(c);
      const pg = pag.pageOf ? pag.pageOf.get(c) : null;
      if (pg) stubPages[c] = pg;
    }
  }

  const fromPages = new Set();
  const fromNames = [];
  for (const pid of contextIds) {
    const pg = pag.pageOf ? pag.pageOf.get(pid) : null;
    if (pg) fromPages.add(pg);
    const nm = nodeMap.get(pid)?.name;
    if (nm) fromNames.push(nm);
  }

  return {
    version: tree.version,
    meta: {
      ...tree.meta,
      pageTitle: page.title,
      pageIndex,
      continuedFromPages: [...fromPages].sort((a, b) => a - b),
      continuedFromNames: fromNames,
      contextIds: [...contextIds],
      stubIds: [...stubIds],
      stubPages,
    },
    settings: tree.settings,
    nodes: tree.nodes.filter((n) => keep.has(n.id)).map((n) => ({ ...n })),
    connections: tree.connections.filter((c) => keep.has(c.from) && keep.has(c.to)),
  };
}

/**
 * 层带分页（备选方案）：按深度切页并重叠一层。
 *
 * 注意：对"层数少、层级宽"的树（如 6 层 233 节点）只会得到 2 页、
 * 每页上百个节点，A4 上不可读。因此导出默认使用 buildFlatView + 子树分页。
 */
export function paginateByDepth(tree, opts = {}) {
  const band = Math.max(1, Number(opts.band) || 3);
  const { nodeMap, childrenOf } = buildIndex(tree);
  const rootId = findTopEvent(tree);
  if (!rootId) return { pages: [], rootId: null, band };

  // BFS 求深度
  const depth = new Map([[rootId, 0]]);
  const queue = [rootId];
  while (queue.length) {
    const cur = queue.shift();
    for (const k of childrenOf.get(cur) || []) {
      if (depth.has(k)) continue;
      depth.set(k, depth.get(cur) + 1);
      queue.push(k);
    }
  }

  const byDepth = new Map();
  for (const [id, d] of depth) {
    if (!byDepth.has(d)) byDepth.set(d, []);
    byDepth.get(d).push(id);
  }
  const maxD = Math.max(...depth.values());

  const pages = [];
  let start = 0;
  while (start <= maxD) {
    const end = Math.min(maxD, start + band);
    const ids = new Set();
    for (let d = start; d <= end; d++) {
      for (const id of byDepth.get(d) || []) ids.add(id);
    }

    const rootsAtBand = (byDepth.get(start) || []).slice();
    const firstRootName = nodeMap.get(rootsAtBand[0])?.name || '';

    pages.push({
      index: pages.length + 1,
      nodes: ids,
      depthStart: start,
      depthEnd: end,
      roots: rootsAtBand,
      title: start === 0
        ? (nodeMap.get(rootId)?.name || '第 1 页')
        : (firstRootName ? `承接：${firstRootName}` : `第 ${pages.length + 1} 页`),
      continuedFrom: start > 0 ? { fromPage: pages.length } : null,
      continuesTo: end < maxD ? [{ label: '', toPage: pages.length + 2 }] : [],
    });

    if (end >= maxD) break;
    // 关键：下一段从本段最后一层开始 —— 上一层既是本页底事件，也是下页顶事件
    start = end;
  }

  return { pages, rootId, band, depth, byDepth, maxDepth: maxD };
}

/**
 * 层带分页的页面视图：**只保留本页节点**，不追溯祖先。
 * 页首节点因父节点不在本页，天然成为该页的顶事件。
 */
export function buildBandView(tree, pag, pageIndex) {
  const page = pag.pages.find((p) => p.index === pageIndex);
  if (!page) return null;
  const ids = page.nodes;
  return {
    version: tree.version,
    meta: {
      ...tree.meta,
      pageTitle: page.title,
      pageIndex,
      continuedFrom: page.continuedFrom ? page.continuedFrom.fromPage : null,
      depthRange: [page.depthStart, page.depthEnd],
    },
    settings: tree.settings,
    nodes: tree.nodes.filter((n) => ids.has(n.id)).map((n) => ({ ...n })),
    connections: tree.connections.filter((c) => ids.has(c.from) && ids.has(c.to)),
  };
}