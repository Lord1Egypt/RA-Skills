/**
 * FTA Studio - 浏览器端图形编辑器
 *
 * 数据流：本地 state.tree  →  渲染  →  变更事件  →  保存 state
 * 计算/导入/导出委托给 /api/*（复用与 CLI 相同的引擎，保证结果一致）
 * 符号几何内置（见 SRC_SYMBOLS），与服务端 SVG 导出保持一致。
 */

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

// ===== medini / IEC 60617 符号几何（与 src/symbols.mjs 保持一致） =====
const WG = 16, HG = 11;   // 门半宽/半高

// medini 的门体：底部平直、顶部成拱，操作符（& / ≥1 / =1 / k/n）写在门体内
const SYMBOLS = {
  // AND：平底 + 半圆拱顶
  andBody: `M ${-WG} ${HG} L ${-WG} 0 A ${WG} ${HG} 0 0 1 ${WG} 0 L ${WG} ${HG} Z`,
  // OR：平底 + 尖拱顶
  orBody: `M ${-WG} ${HG} L ${-WG} 0 Q 0 ${-HG * 1.62} ${WG} 0 L ${WG} ${HG} Z`,
  // XOR：OR + 内侧平行拱线
  xorBody: `M ${-WG} ${HG} L ${-WG} 0 Q 0 ${-HG * 1.62} ${WG} 0 L ${WG} ${HG} Z`,
  xorArc: `M ${-WG * 0.62} ${HG * 0.2} Q 0 ${-HG * 1.05} ${WG * 0.62} ${HG * 0.2}`,
  // INHIBIT：AND 门体 + 下方条件线
  inhibitBody: `M ${-WG} ${HG} L ${-WG} 0 A ${WG} ${HG} 0 0 1 ${WG} 0 L ${WG} ${HG} Z`,
  inhibitStem: `M 0 ${HG} L 0 ${HG * 1.7}`,
  notBody: `M ${-WG} ${-HG} L ${WG} ${-HG} L 0 ${HG} Z`,
  voteW: WG, voteH: HG,
  pandLines: [{ x1: -WG * 0.62, y1: HG * 1.55, x2: WG * 0.62, y2: HG * 1.55 }],
};

// 门体内的操作符文字（medini 风格）
const GATE_OP = { AND: '&', PAND: '&', OR: '≥1', XOR: '=1', INHIBIT: '&' };

// ===== 状态 =====
const state = {
  tree: null,
  selected: null,
  selectedLink: null,
  dragging: null,
  linking: null,
  heat: false,        // 默认关闭 → 画布呈 medini 式纯白
  showProb: true,
  zoom: 1,
  result: null,
  heatmap: {},
  pagination: null,   // {pages, pageIndex, pageOf}
  offsets: {},        // 手动拖拽偏移 { [id]: {dx,dy} }，叠加在自动布局之上
  flash: null,        // 新添加节点的高亮 id
  nodeProbs: {},      // 分析后逐节点概率 { [id]: prob }（medini：事件上显示 Q）
  showIds: true,      // 事件编号装饰（medini 默认显示，可在 Ribbon 关闭）
};

// ===== 历史记录（撤销 / 重做）=====
const HIST = { stack: [], idx: -1, max: 150, restoring: false };

const GATEABLE_TYPES = ['top', 'intermediate'];
const TYPE_LABEL = {
  top: '顶事件', intermediate: '中间事件', basic: '基本事件',
  undeveloped: '未开发事件', house: '房屋事件', condition: '条件事件',
  external: '外部事件', comment: '注释',
};
const GATE_LABEL = {
  AND: '与门 AND', OR: '或门 OR', XOR: '异或门 XOR', NOT: '非门 NOT',
  PAND: '优先与门', INHIBIT: '禁门', VOTE: '表决门',
};

// ===== 工具 =====
function toast(msg, kind = '') {
  const t = $('#toast');
  t.textContent = msg;
  t.className = 'toast ' + kind;
  t.hidden = false;
  clearTimeout(toast._t);
  toast._t = setTimeout(() => { t.hidden = true; }, 2600);
}

function newId() {
  let n = 1;
  const used = new Set(state.tree.nodes.map((x) => x.id));
  while (used.has('N' + String(n).padStart(3, '0'))) n++;
  return 'N' + String(n).padStart(3, '0');
}

function fmtQ(x) {
  if (x == null || Number.isNaN(x)) return '—';
  if (x === 0) return '0';
  if (Math.abs(x) < 1e-3 || Math.abs(x) >= 1e5) return Number(x).toExponential(2);
  return String(Number(x.toPrecision(4)));
}

function newTree() {
  return {
    version: '1.0',
    meta: { title: '新建故障树', project: '', author: '', date: new Date().toISOString().slice(0, 10), standard: '', missionTime: null, revision: 'A', description: '' },
    settings: { missionTime: null, maxCutSetOrder: 0, truncation: 1e-12, quantification: 'auto' },
    nodes: [
      { id: 'N001', type: 'top', name: '顶事件', gate: 'OR', voteK: 2, voteN: 2, description: '', ref: '', component: '', probModel: 'fixed', prob: null, lambda: null },
    ],
    connections: [],
  };
}

// ===== 索引 =====
/** 建立索引；传入 tree 时可对子视图（如分页视图）建索引 */
function index(t) {
  const tree = t || state.tree;
  const map = new Map(tree.nodes.map((n) => [n.id, n]));
  const kids = new Map(tree.nodes.map((n) => [n.id, []]));
  for (const c of tree.connections) {
    if (kids.has(c.from) && map.has(c.to)) kids.get(c.from).push(c.to);
  }
  const hasKids = new Set(tree.connections.map((c) => c.from));
  return { map, kids, hasKids };
}

// ===== 布局（前后端同一算法思路的简化实现：纵向树形布局） =====
const LAY = {
  w: 152, h: 44, gate: 32,
  rowGap: 84, colGap: 22,
};

function computeLayout(tree) {
  const t = tree || state.tree;
  const { map, kids, hasKids } = index(t);

  // 根：优先显式的顶事件；否则取「本树内没有入边的节点」。
  // ⚠️ 不能退化成"第一个叶子" —— 分页后的一页往往没有 top 类型节点，
  // 那样会随便挑一个基本事件当根，整页只画出它自己。
  const parentIds = new Set(t.connections.map((c) => c.to));
  const roots = t.nodes.filter((n) => !parentIds.has(n.id)).map((n) => n.id);
  const rootId = t.nodes.find((n) => n.type === 'top')?.id
    || roots[0]
    || t.nodes[0]?.id;
  if (!rootId) return { pos: new Map(), w: 0, h: 0, rootId: null };
  // 多顶事件（分页视图常见）：所有无入边节点都要布局，否则后面的顶事件不会显示
  const placeRoots = roots.length ? roots : [rootId];

  // 折叠：任意节点（含根节点）都可折叠，只显示自身
  const collapsed = new Set(t.nodes.filter((n) => n.collapsed).map((n) => n.id));

  const leafW = new Map();
  const widthOf = (id) => {
    if (leafW.has(id)) return leafW.get(id);
    const ch = collapsed.has(id) ? [] : (kids.get(id) || []);
    let w;
    if (!ch.length) w = LAY.w;
    else {
      let s = 0;
      for (const k of ch) s += widthOf(k) + LAY.colGap;
      w = Math.max(LAY.w, s - LAY.colGap);
    }
    leafW.set(id, w);
    return w;
  };

  const pos = new Map();
  let maxY = 0;
  const place = (id, depth, left) => {
    const w = widthOf(id);
    const cx = left + w / 2;
    const y = depth * LAY.rowGap;
    pos.set(id, { cx, y, depth, id, node: map.get(id) });
    maxY = Math.max(maxY, y);
    const ch = collapsed.has(id) ? [] : (kids.get(id) || []);
    if (!ch.length) return;
    let cw = 0;
    for (const k of ch) cw += widthOf(k) + LAY.colGap;
    cw -= LAY.colGap;
    let cur = cx - cw / 2;
    for (const k of ch) {
      place(k, depth + 1, cur);
      cur += widthOf(k) + LAY.colGap;
    }
  };
  // 依次摆放每个根（单根树只有一项）
  let cursorX = 0;
  for (const r of placeRoots) {
    place(r, 0, cursorX);
    cursorX += widthOf(r) + LAY.colGap * 2;
  }

  // 归一化到左内边距
  let minX = Infinity;
  for (const p of pos.values()) minX = Math.min(minX, p.cx - LAY.w / 2);
  const PAD = 36;
  for (const p of pos.values()) {
    p.x = p.cx - LAY.w / 2 - minX + PAD;
    p.cx = p.x + LAY.w / 2;
  }
  // 分页视图：顶部留白，给「⤓ 分页 · 第 N 页」跳转标签让位
  // （标签画在事件框上边缘之上，首行不留白会被页眉盖住）
  if (state.pagination) {
    for (const p of pos.values()) p.y += 30;
  }
  // 叠加手动拖拽偏移（叠加在自动布局之上；坐标保持非负，画布原点固定为 0）
  const offs = state.offsets || {};
  for (const p of pos.values()) {
    const o = offs[p.id];
    if (o && (o.dx || o.dy)) {
      p.x = Math.max(2, p.x + o.dx);
      p.y = Math.max(2, p.y + o.dy);
      p.cx = p.x + LAY.w / 2;
    }
  }
  // 门坐标 + 内容包络（取节点右下角，底部留出编号标签空间）
  let maxRight = 0;
  let maxBottom = 0;
  for (const p of pos.values()) {
    p.outY = p.y + LAY.h;          // 事件框底边 = 连线起点
    p.gateY = p.outY + HG + 3;     // 门体中心：位于框下方，与框留出间隙（medini 风格）
    p.gateX = p.x + LAY.w / 2;
    maxRight = Math.max(maxRight, p.x + LAY.w);
    maxBottom = Math.max(maxBottom, p.gateY + HG * 1.9);
  }
  return { pos, w: maxRight + PAD, h: maxBottom + PAD + 44, rootId };
}

// ===== 渲染 =====
const SVGNS = 'http://www.w3.org/2000/svg';
function el(tag, attrs = {}, parent) {
  const e = document.createElementNS(SVGNS, tag);
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  if (parent) parent.appendChild(e);
  return e;
}
function esc(s) {
  return String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

/** 画布标签自适应截断：中文按 1 个字号宽、西文约 0.56 个字号宽（与导出端 fitLabel 同规则） */
function fitCanvasLabel(s, maxPx, fontSize = 11.5) {
  let used = 0, out = '';
  for (const ch of String(s ?? '')) {
    const cjk = /[\u2E80-\u9FFF\u3000-\u303F\uFF00-\uFFEF]/.test(ch);
    const cw = cjk ? fontSize : fontSize * 0.56;
    if (used + cw > maxPx) return out + '…';
    used += cw; out += ch;
  }
  return out;
}

function heatFill(id) {
  if (!state.heat) return '#ffffff';
  const h = state.heatmap[id] ?? 0;
  const t = Math.max(0, Math.min(1, h));
  // 绿 -> 黄 -> 红
  const stops = [[224,242,254], [254,249,195], [254,226,150], [254,202,202]];
  const P = [0, 0.4, 0.72, 1];
  let a = stops[0], b = stops[0];
  for (let i = 0; i < P.length - 1; i++) {
    if (t >= P[i] && t <= P[i + 1]) { a = stops[i]; b = stops[i + 1]; break; }
    if (t > P[i + 1]) { a = b = stops[i + 1]; }
  }
  const f = a === b ? 0 : (t - P[0]) / (P[3] - P[0] || 1);
  const c = a.map((x, i) => Math.round(x + (b[i] - x) * Math.max(0, Math.min(1, f))));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
}

function render() {
  const svg = $('#canvas');
  svg.innerHTML = '';

  // 分页模式：仅渲染当前页的节点
  let viewTree = state.tree;
  if (state.pagination) {
    const pageIdx = state.pagination.pageIndex;
    // 页底接续事件（归属下一页，但本页要虚线保留）
    const extra = new Set(state.pagination.extraOf?.[pageIdx] || []);
    // 页顶承接事件（上一页的分页点，本页展开，同样虚线）
    const cont = new Set(state.pagination.contOf?.[pageIdx] || []);
    const ids = new Set(
      state.tree.nodes
        .filter((n) => state.pagination.pageOf[n.id] === pageIdx || extra.has(n.id))
        .map((n) => n.id)
    );
    if (ids.size) {
      viewTree = {
        ...state.tree,
        nodes: state.tree.nodes
          .filter((n) => ids.has(n.id))
          .map((n) => {
            if (extra.has(n.id)) return { ...n, __pbMarker: true, __pbExtra: true, collapsed: true };
            if (cont.has(n.id)) return { ...n, __pbMarker: true, __pbCont: true };
            return n;
          }),
        connections: state.tree.connections.filter((c) => ids.has(c.from) && ids.has(c.to)),
      };
    }
  }

  const L = computeLayout(viewTree);

  const defs = el('defs', {}, svg);
  const mk = el('marker', {
    id: 'arw', viewBox: '0 0 10 10', refX: 9.5, refY: 5,
    markerWidth: 6.5, markerHeight: 6.5, orient: 'auto-start-reverse',
  }, defs);
  el('path', { d: 'M0 0 L10 5 L0 10 z', fill: '#5b6673' }, mk);

  // 内容组（分页时整体下移）
  const gRoot = el('g', { class: 'zoom' }, svg);

  // 连线
  const { kids, hasKids, map } = index(viewTree);
  const gLink = el('g', {}, gRoot);
  for (const c of viewTree.connections) {
    const p = L.pos.get(c.from), q = L.pos.get(c.to);
    if (!p || !q) continue;
    const my = p.gateY + HG + 7;
    const d = Math.abs(p.gateX - q.cx) < 1
      ? `M ${p.gateX} ${p.outY} L ${q.cx} ${q.y}`
      : `M ${p.gateX} ${p.outY} L ${p.gateX} ${my} L ${q.cx} ${my} L ${q.cx} ${q.y}`;
    const cls = 'link' + (state.selectedLink === c ? ' sel' : '');
    el('path', { d, class: cls, 'marker-end': 'url(#arw)' }, gLink);
    const hit = el('path', { d, class: 'link-hit' }, gLink);
    hit.addEventListener('pointerdown', (ev) => {
      ev.stopPropagation();
      state.selectedLink = c;
      state.selected = null;
      render();
    });
    hit.addEventListener('dblclick', (ev) => {
      ev.stopPropagation();
      deleteConn(c);
    });
  }

  // 正在连线
  if (state.linking) {
    const from = L.pos.get(state.linking);
    if (from) el('path', {
      d: `M ${from.gateX} ${from.outY} L ${state.linking.mx} ${state.linking.my}`,
      class: 'link', 'stroke-dasharray': '4 3', 'stroke': '#2563eb',
    }, gLink);
  }

  // 节点
  const gN = el('g', {}, gRoot);
  for (const [id, p] of L.pos) {
    const n = p.node;
    const x = p.x, y = p.y, w = LAY.w, h = LAY.h;
    const fill = heatFill(id);
    const g = el('g', { class: 'node-box' + (state.selected === id ? ' node-sel' : '') }, gN);

    // 形状（medini 风格：事件=白色矩形；house/未开发/条件/传输保留专用符号）
    const shape = eventShapePath(n.type, w, h);
    const cx0 = x + w / 2, cy0 = y + h / 2;
    let shapeEl;
    if (shape.kind === 'complex') {
      shapeEl = el('path', {
        d: shape.body, transform: `translate(${cx0},${cy0})`,
        fill, stroke: '#333333', 'stroke-width': 1.1,
      }, g);
      for (const c of shape.cross) {
        el('path', {
          d: c, transform: `translate(${cx0},${cy0})`,
          fill: 'none', stroke: '#333333', 'stroke-width': 1.1,
        }, g);
      }
    } else {
      shapeEl = el('path', {
        d: shape.d, transform: `translate(${cx0},${cy0})`,
        fill, stroke: '#333333', 'stroke-width': 1.1,
        'stroke-dasharray': shape.dashed ? '4 3' : null,
      }, g);
    }
    shapeEl.setAttribute('class', 'nshape');
    // 分页标记：该事件已分到下一页，本页只保留虚线框表示"此处分页"
    if (n.__pbMarker) shapeEl.setAttribute('stroke-dasharray', '5 4');

    // 文本（medini 风格：底事件左缘红色圆点 + 文字左对齐紧随其后；其余事件居中）
    const hasProb = state.showProb && n.type === 'basic' && n.prob != null;
    const ty = y + (hasProb ? h / 2 - 4 : h / 2 + 4);
    const tx = el('text', { y: ty, class: 'node-label' }, g);
    if (n.type === 'basic') {
      const rx = w * 0.4;
      const dotX = x + w / 2 - rx + 9;
      el('circle', { cx: dotX, cy: y + h / 2, r: 3.5, class: 'basic-dot' }, g);
      tx.setAttribute('x', dotX + 9);
      tx.setAttribute('text-anchor', 'start');
      tx.textContent = fitCanvasLabel(
        n.name || TYPE_LABEL[n.type] || '',
        (x + w / 2 + rx - 8) - (dotX + 9)
      );
    } else {
      tx.setAttribute('x', x + w / 2);
      tx.setAttribute('text-anchor', 'middle');
      tx.textContent = (n.name || TYPE_LABEL[n.type] || '').slice(0, 20);
    }
    if (hasProb) {
      const tp = el('text', { x: x + w / 2, y: y + h / 2 + 11, 'text-anchor': 'middle', class: 'node-prob' }, g);
      tp.textContent = 'q=' + fmtQ(n.prob);
    }

    // 事件编号标签（medini 默认不显示，可在 Ribbon「编号」开启）
    const tagTxt = (n.ref || n.id || '').slice(0, 14);
    const tagW = Math.max(24, tagTxt.length * 5.4 + 10);
    const tagY = y + h + 12;
    const isParent = (kids.get(id) || []).length > 0;
    const tagCx = isParent ? (x + 4 + tagW / 2) : (x + w / 2);
    if (state.showIds) {
      el('rect', { x: tagCx - tagW / 2, y: tagY, width: tagW, height: 12, rx: 1, class: 'id-tag-rect' }, g);
      const tg = el('text', { x: tagCx, y: tagY + 9, 'text-anchor': 'middle', class: 'id-tag-txt' }, g);
      tg.textContent = tagTxt;
    }

    // 分析后展示该事件的概率（medini：Calculate probabilities 会在事件上显示 Q）
    if (state.nodeProbs && state.nodeProbs[id] != null &&
        !(n.type === 'basic' && state.showProb && n.prob != null)) {
      const qx = state.showIds ? tagCx : x + w / 2;
      const qy = state.showIds ? tagY + 24 : y + h + 22;
      el('text', { x: qx, y: qy, 'text-anchor': 'middle', class: 'node-q' }, g)
        .textContent = 'Q=' + fmtQ(state.nodeProbs[id]);
    }

    // 折叠徽标：右下角显示被折叠的子事件数量
    if (n.collapsed) {
      const cnt = countDescendants(id);
      const label = '+' + cnt;
      const bw = Math.max(18, label.length * 5.6 + 8);
      const bx = x + w - bw - 2;
      const by = y + h + 3;
      const bg = el('g', { class: 'collapse-badge' }, g);
      el('rect', { x: bx, y: by, width: bw, height: 13, rx: 6.5, class: 'bg' }, bg);
      el('text', { x: bx + bw / 2, y: by + 9.6, 'text-anchor': 'middle', class: 'tx' }, bg)
        .textContent = label;
    }

    // 手动分页点：上方虚线 + 标注
    //   页底（__pbExtra）：⤓ 分页 · 第 N 页 —— 这一支翻到下一页
    //   页顶（__pbCont） ：↑ 续上页 · 第 N 页 —— 由上一页分页而来
    // 有目标页时标注画成胶囊按钮，点一下直接跳过去
    if (n.pageBreak || n.__pbMarker) {
      el('line', { x1: x - 8, y1: y - 6, x2: x + w + 8, y2: y - 6, class: 'pb-line' }, g);
      const target = n.__pbMarker ? jumpTargetFor(id) : 0;
      const base = n.__pbCont ? '↑ 续上页' : '⤓ 分页';
      drawJumpChip(g, x + w / 2, y - 8, target ? `${base} · 第 ${target} 页` : base, target);
    }

    // 分析后展示该事件的概率（medini：Calculate probabilities 会在事件上显示 Q）
    if (state.nodeProbs && state.nodeProbs[id] != null &&
        !(n.type === 'basic' && state.showProb && n.prob != null)) {
      el('text', { x: tagCx, y: tagY + 24, 'text-anchor': 'middle', class: 'node-q' }, g)
        .textContent = 'Q=' + fmtQ(state.nodeProbs[id]);
    }

    // 连线端口（右侧圆点）
    const dot = el('circle', { cx: x + w, cy: y + h / 2, r: 4.2, class: 'port-dot' }, g);
    dot.addEventListener('pointerdown', (ev) => startLink(ev, id));

    // 交互（绑定真正的 SVG 元素 shapeEl，而非几何描述对象 shape）
    // 双击折叠在 startDrag 里手动判定：pointerdown 会 render() 重建元素，
    // 原生 dblclick 无法触发，故此处不再绑定 dblclick。
    shapeEl.addEventListener('pointerdown', (ev) => startDrag(ev, id));
    shapeEl.addEventListener('contextmenu', (ev) => openCtx(ev, id));
    el('title', {}, g).textContent = n.name + (n.component ? `  [${n.component}]` : '') + (n.ref ? `  ${n.ref}` : '');
  }

  // 门
  const gG = el('g', {}, gRoot);
  for (const [id, p] of L.pos) {
    const n = p.node;
    if (!n.gate) continue;
    if (!viewTree.connections.some((c) => c.from === id)) continue;
    drawGate(gG, n.gate, p.gateX, p.gateY, n.voteK, n.voteN, id);
  }

  // 选中高亮
  if (state.selected) {
    const p = L.pos.get(state.selected);
    if (p) el('rect', { x: p.x - 4, y: p.y - 4, width: LAY.w + 8, height: LAY.h + 8, fill: 'none', stroke: '#2563eb', 'stroke-width': 1.2, 'stroke-dasharray': '4 3', rx: 5 }, gRoot);
  }

  // 新添加节点 → 短暂橙色高亮环
  if (state.flash) {
    const p = L.pos.get(state.flash);
    if (p) el('rect', { x: p.x - 6, y: p.y - 6, width: LAY.w + 12, height: LAY.h + 12, rx: 6, fill: 'none', stroke: '#f59e0b', 'stroke-width': 2.4, 'stroke-dasharray': '5 3' }, gRoot);
  }

  // 分页模式：页眉 + 内容整体下移
  let contentOffset = 0;
  if (state.pagination) {
    contentOffset = 34;
    const cur = state.pagination.pages.find((x) => x.index === state.pagination.pageIndex);
    el('rect', { x: 0, y: 0, width: L.w, height: 28, fill: '#eef4ff' }, svg);
    const t = el('text', {
      x: L.w / 2, y: 18, 'text-anchor': 'middle',
      'font-size': 12.5, 'font-weight': 600, fill: '#2563eb',
    }, svg);
    t.textContent = `第 ${state.pagination.pageIndex} / ${state.pagination.total} 页 — ${cur?.title || ''}`;
  }

  // 缩放：通过 width/height 属性（布局尺寸）承载 zoom，viewBox 保持坐标系统不变。
  // svgPoint() 基于 getBoundingClientRect 反算，天然兼容此缩放方式。
  svg.setAttribute('width', L.w * state.zoom);
  svg.setAttribute('height', (L.h + contentOffset) * state.zoom);
  svg.setAttribute('viewBox', `0 0 ${L.w} ${L.h + contentOffset}`);
  if (contentOffset) {
    const g = svg.querySelector('g.zoom');
    if (g) g.setAttribute('transform', `translate(0,${contentOffset})`);
  }

  const cnt = state.pagination
    ? `${viewTree.nodes.length} 节点（本页） / ${state.tree.nodes.length} 节点（总）`
    : `${state.tree.nodes.length} 节点 / ${state.tree.connections.length} 连接`;
  $('#hint').textContent = cnt;

  // 画布浮动计数浮层（对标 medini 左上角概览）
  const ov = $('#ov-count');
  if (ov) {
    const top = state.tree.nodes.find((n) => n.type === 'top');
    ov.textContent = `节点 ${state.tree.nodes.length} · 连接 ${state.tree.connections.length}`
      + (top ? ` · 顶事件「${top.name || top.id}」` : '');
  }

  // 记录历史（拖拽 / 连线过程中不记录；撤销恢复时也不记录）
  if (!HIST.restoring && !state.dragging && !state.linking) histPush();
}

/**
 * 某个分页标记事件"对面"的那一页：
 *   页底分页点（__pbExtra）→ 它的子树真正展开的那一页（往后翻）
 *   页顶承接事件（__pbCont）→ 它被切出去的那一页（往前翻）
 * 返回 0 表示没有可跳转的目标。
 */
function jumpTargetFor(id) {
  const p = state.pagination;
  if (!p) return 0;
  const cur = p.pageIndex;
  const home = p.pageOf?.[id];
  if (home && home !== cur) return home;
  for (const [k, ids] of Object.entries(p.extraOf || {})) {
    if (Number(k) !== cur && ids.includes(id)) return Number(k);
  }
  return 0;
}

/** 分页标签：有目标页时画成可点胶囊按钮，点击跳到该事件所在的页 */
function drawJumpChip(parent, cx, baseY, text, target) {
  const g = el('g', { class: 'pb-chip' + (target ? ' can' : '') }, parent);
  const w = Math.max(38, text.length * 6.8 + 12);
  const h = 14;
  const x = cx - w / 2, y = baseY - h;
  if (target) el('rect', { x, y, width: w, height: h, rx: h / 2, class: 'pb-chip-bg' }, g);
  el('text', { x: cx, y: y + 10.4, 'text-anchor': 'middle', class: 'pb-tx' }, g).textContent = text;
  if (!target) return;
  // 透明热区：胶囊本身带 fill，指针事件已足够；再兜一层防止点在文字间隙
  el('rect', { x, y, width: w, height: h, rx: h / 2, fill: 'transparent' }, g);
  g.style.cursor = 'pointer';
  el('title', {}, g).textContent = `点击跳转到第 ${target} 页`;
  g.addEventListener('pointerdown', (ev) => ev.stopPropagation());
  g.addEventListener('click', (ev) => { ev.stopPropagation(); gotoPage(target); });
}

/** IEC 61025 事件符号路径（中心原点） */
function eventShapePath(type, W, H) {
  const w = W / 2, h = H / 2;
  switch (type) {
    case 'basic': {
      // 基本事件：圆形（节点框为固定宽高，按文字宽度略作椭圆化以保证名称可读）
      const rx = w * 0.8;
      return { kind: 'path', d: `M ${-rx} 0 A ${rx} ${h} 0 1 0 ${rx} 0 A ${rx} ${h} 0 1 0 ${-rx} 0 Z` };
    }
    case 'undeveloped':
      // 未开发事件：菱形
      return { kind: 'path', d: `M 0 ${-h} L ${w} 0 L 0 ${h} L ${-w} 0 Z` };
    case 'house':
      // 房屋事件：五边形
      return { kind: 'path', d: `M ${-w} ${h} L ${-w} ${-h * 0.28} L 0 ${-h} L ${w} ${-h * 0.28} L ${w} ${h} Z` };
    case 'condition': {
      // 条件事件：扁椭圆（与基本事件区分）
      const ry = h * 0.76;
      return { kind: 'path', d: `M ${-w} 0 A ${w} ${ry} 0 1 0 ${w} 0 A ${w} ${ry} 0 1 0 ${-w} 0 Z` };
    }
    case 'external': {
      // 外部事件：圆 + 内部叉
      const r = Math.min(w, h);
      return {
        kind: 'complex',
        body: `M ${-r} 0 A ${r} ${r} 0 1 0 ${r} 0 A ${r} ${r} 0 1 0 ${-r} 0 Z`,
        cross: [
          `M ${-r * 0.62} ${-r * 0.62} L ${r * 0.62} ${r * 0.62}`,
          `M ${r * 0.62} ${-r * 0.62} L ${-r * 0.62} ${r * 0.62}`,
        ],
      };
    }
    case 'transfer_in':
    case 'transfer_out':
      // 传输符号：三角形
      return { kind: 'path', d: `M 0 ${-h} L ${w} ${h} L ${-w} ${h} Z` };
    case 'comment':
      return { kind: 'path', d: `M ${-w} ${-h} L ${w} ${-h} L ${w} ${h} L ${-w} ${h} Z`, dashed: true };
    default:
      // 中间事件 / 顶事件：矩形
      return { kind: 'path', d: `M ${-w} ${-h} L ${w} ${-h} L ${w} ${h} L ${-w} ${h} Z` };
  }
}

function drawGate(parent, gate, cx, cy, k, n, nodeId) {
  const g = el('g', { class: 'gate-hit' }, parent);
  const S = '#ffffff', ST = '#1a1a1a';
  let body;

  switch (gate) {
    case 'AND': case 'PAND':
      body = SYMBOLS.andBody;
      break;
    case 'OR':
      body = SYMBOLS.orBody;
      break;
    case 'XOR':
      body = SYMBOLS.xorBody;
      break;
    case 'INHIBIT':
      body = SYMBOLS.inhibitBody;
      break;
    case 'NOT':
      body = SYMBOLS.notBody;
      break;
    case 'VOTE':
      body = `M ${-SYMBOLS.voteW} ${-SYMBOLS.voteH} L ${SYMBOLS.voteW} ${-SYMBOLS.voteH} L ${SYMBOLS.voteW} ${SYMBOLS.voteH} L ${-SYMBOLS.voteW} ${SYMBOLS.voteH} Z`;
      break;
    default:
      body = SYMBOLS.andBody;
  }

  el('path', {
    d: body, transform: `translate(${cx},${cy})`,
    fill: S, stroke: ST, 'stroke-width': 1.3,
    'stroke-linejoin': 'round',
  }, g);

  // XOR：门体内侧再画一条平行拱线
  if (gate === 'XOR') {
    el('path', {
      d: SYMBOLS.xorArc, transform: `translate(${cx},${cy})`,
      fill: 'none', stroke: ST, 'stroke-width': 1,
    }, g);
  }

  // INHIBIT：底部引出的条件线
  if (gate === 'INHIBIT') {
    el('path', {
      d: SYMBOLS.inhibitStem, transform: `translate(${cx},${cy})`,
      fill: 'none', stroke: ST, 'stroke-width': 1.3,
    }, g);
  }

  // PAND：底部优先次序横线
  if (gate === 'PAND') {
    for (const l of SYMBOLS.pandLines) {
      el('path', {
        d: `M ${l.x1} ${l.y1} L ${l.x2} ${l.y2}`,
        transform: `translate(${cx},${cy})`,
        fill: 'none', stroke: ST, 'stroke-width': 1,
      }, g);
    }
  }

  // 门内操作符：medini 风格（& / ≥1 / =1 / k/n）
  if (gate === 'VOTE') {
    const t = el('text', {
      x: cx, y: cy + 4, 'text-anchor': 'middle',
      'font-size': 9.5, 'font-weight': 700, fill: ST,
      'font-family': 'Consolas, monospace',
    }, g);
    t.textContent = `${k}/${n}`;
  } else if (GATE_OP[gate]) {
    const t = el('text', {
      x: cx, y: cy + HG * 0.62, 'text-anchor': 'middle', class: 'gate-op',
    }, g);
    t.textContent = GATE_OP[gate];
  }

  const hit = el('circle', { cx, cy, r: 15, fill: 'transparent' }, g);
  hit.addEventListener('pointerdown', (ev) => ev.stopPropagation());
  // medini：双击门同样折叠/展开其子树
  hit.addEventListener('dblclick', (ev) => {
    ev.stopPropagation();
    if (nodeId) toggleCollapse(nodeId); else switchTab('props');
  });
  if (nodeId) hit.addEventListener('contextmenu', (ev) => { ev.stopPropagation(); openCtx(ev, nodeId); });
}

// ===== 交互 =====
function svgPoint(ev) {
  const svg = $('#canvas');
  const r = svg.getBoundingClientRect();
  const vb = svg.viewBox.baseVal;
  const sx = vb && vb.width ? vb.width / r.width : 1;
  const sy = vb && vb.height ? vb.height / r.height : 1;
  return { x: (ev.clientX - r.left) * sx, y: (ev.clientY - r.top) * sy };
}

function select(id) {
  state.selected = id;
  state.selectedLink = null;
  render();
  renderProps();
  renderOutline();
}

// ===== 折叠 / 展开子事件（双击事件）=====
/** 统计某节点下所有后代数量（含多层） */
function countDescendants(id) {
  const { kids } = index();
  let total = 0;
  const walk = (nid) => {
    for (const k of (kids.get(nid) || [])) {
      total += 1;
      walk(k);
    }
  };
  walk(id);
  return total;
}

/**
 * 手动分页点：标记「此事件另起一页」。
 * 导出 A4 时，上一页到此为止（本事件作为页底），下一页从本事件开始展开。
 */
function togglePageBreak(id) {
  const { map, kids } = index();
  const n = map.get(id);
  if (!n) return;
  if (!(kids.get(id) || []).length) {
    toast('底事件没有子事件，不能作为分页点', 'err');
    return;
  }
  n.pageBreak = !n.pageBreak;
  state.selected = id;
  render();
  renderProps();
  const count = state.tree.nodes.filter((x) => x.pageBreak).length;
  toast(n.pageBreak
    ? `已设分页点：导出时「${n.name || id}」从新页开始（共 ${count} 个分页点）`
    : `已取消分页点（剩余 ${count} 个）`);
  // 分页视图开着时立即重算，让画布同步反映新的分页点
  if (state.pagination) computePagination();
}

/** 切换折叠状态；没有子事件的叶子节点则打开属性面板 */
function toggleCollapse(id) {
  const { map, kids } = index();
  const n = map.get(id);
  if (!n) return;
  if (!(kids.get(id) || []).length) {
    select(id);
    switchTab('props');
    return;
  }
  n.collapsed = !n.collapsed;
  state.selected = id;
  state.selectedLink = null;
  render();
  renderProps();
  renderOutline();
  fitView();   // 折叠后画布尺寸变化大，重新适配视图
  toast(n.collapsed ? `已折叠 ${countDescendants(id)} 个子事件` : '已展开子事件');
}

/** 整理子树（medini: Arrange Subtree）—— 清除该节点及其后代的拖拽偏移，恢复自动布局 */
function arrangeSubtree(id) {
  const { kids } = index();
  const ids = [id];
  const walk = (nid) => {
    for (const k of (kids.get(nid) || [])) { ids.push(k); walk(k); }
  };
  walk(id);
  for (const x of ids) delete state.offsets[x];
  render();
  renderProps();
  focusNode(id);
  const n = state.tree.nodes.find((x) => x.id === id);
  toast(`已整理「${n?.name || id}」的子树布局（${ids.length} 个事件）`);
}

/** 判断 target 是否落在 root 的子树内（用于阻止成环连接） */
function isInSubtree(root, target) {
  const { kids } = index();
  const stack = [root];
  const seen = new Set();
  while (stack.length) {
    const cur = stack.pop();
    if (cur === target) return true;
    if (seen.has(cur)) continue;
    seen.add(cur);
    for (const k of (kids.get(cur) || [])) stack.push(k);
  }
  return false;
}

/** 递归生成布尔表达式（medini: Boolean expression），同运算符的子式自动拍平 */
function boolExpr(id, parentOp = null) {
  const { kids } = index();
  const n = state.tree.nodes.find((x) => x.id === id);
  if (!n) return '';
  const ref = n.ref || n.id;
  const ch = kids.get(id) || [];
  if (!ch.length) return ref;
  const op = n.gate === 'OR' ? ' OR '
    : n.gate === 'XOR' ? ' XOR '
    : n.gate === 'NOT' ? ' NOT '
    : ' AND ';
  const parts = ch.map((k) => boolExpr(k, op));
  if (parts.length === 1) return parts[0];
  const body = parts.join(op);
  return parentOp === op ? body : `(${body})`;
}

/** 在报告的弹窗里展示该事件的布尔表达式（并尝试复制到剪贴板） */
function showBooleanExpression(id) {
  const n = state.tree.nodes.find((x) => x.id === id);
  if (!n) return;
  const text = `π[${n.ref || n.id}] = ${boolExpr(id)}`;
  $('#report-text').textContent = text;
  $('#modal-report').hidden = false;
  try {
    const p = navigator.clipboard?.writeText(text);
    if (p && typeof p.catch === 'function') p.catch(() => { /* 无焦点/无权限时静默 */ });
  } catch { /* 忽略 */ }
  toast('布尔表达式已生成（可点「复制 Markdown」再复制）', 'ok');
}

// ===== 撤销 / 重做 =====
// 采用「快照」方式：每次树或拖拽偏移发生变化就压入历史。
// render() 末尾自动比对快照，因此所有改动点（新增/删除/连线/设门/属性/导入/新建…）
// 无需逐一改造即可被记录；拖拽移动的中间过程被跳过，只在落点时记一次。
function histSnapshot() {
  return JSON.stringify({ tree: state.tree, offsets: state.offsets || {} });
}

function histButtons() {
  const u = $('#btn-undo');
  const r = $('#btn-redo');
  if (u) {
    u.disabled = HIST.idx <= 0;
    u.title = HIST.idx > 0 ? '撤销 (Ctrl+Z)' : '没有可撤销的操作';
  }
  if (r) {
    r.disabled = HIST.idx >= HIST.stack.length - 1;
    r.title = HIST.idx < HIST.stack.length - 1 ? '重做 (Ctrl+Y)' : '没有可重做的操作';
  }
}

function histPush() {
  if (HIST.restoring) return;
  const s = histSnapshot();
  if (HIST.idx >= 0 && HIST.stack[HIST.idx] === s) return;
  // 丢弃重做分支
  if (HIST.idx < HIST.stack.length - 1) HIST.stack.length = HIST.idx + 1;
  HIST.stack.push(s);
  while (HIST.stack.length > HIST.max) HIST.stack.shift();
  HIST.idx = HIST.stack.length - 1;
  histButtons();
}

/** 清空历史，把当前状态作为唯一基线（用于程序初始化完成后） */
function histReset() {
  HIST.stack = [histSnapshot()];
  HIST.idx = 0;
  histButtons();
}

function histRestore(s) {
  HIST.restoring = true;
  try {
    const o = JSON.parse(s);
    state.tree = o.tree;
    state.offsets = o.offsets || {};
    state.selectedLink = null;
    state.dragging = null;
    state.linking = null;
    state.flash = null;
    if (state.selected && !state.tree.nodes.some((n) => n.id === state.selected)) {
      state.selected = null;
    }
    state.result = null;
    state.heatmap = {};
    state.nodeProbs = {};
    render();
    renderProps();
    renderOutline();
  } finally {
    HIST.restoring = false;
  }
  histButtons();
}

function undo() {
  if (HIST.idx <= 0) return;
  HIST.idx -= 1;
  histRestore(HIST.stack[HIST.idx]);
  toast('已撤销');
}

function redo() {
  if (HIST.idx >= HIST.stack.length - 1) return;
  HIST.idx += 1;
  histRestore(HIST.stack[HIST.idx]);
  toast('已重做');
}

/** 是否为可编辑文本控件（此时 Ctrl+Z 应交给输入框自己处理） */
function isTextEditing(el) {
  if (!el) return false;
  const tag = (el.tagName || '').toUpperCase();
  return tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || el.isContentEditable;
}

// 双击检测状态：pointerdown 会 render() 重建 DOM，节点的原生 dblclick 不会触发，
// 因此自行按「同一节点 + 时间窗」判定双击。
let lastDown = { id: null, t: 0 };

function startDrag(ev, id) {
  ev.stopPropagation();

  // --- 双击判定（优先于拖拽）---
  const now = (typeof performance !== 'undefined' ? performance.now() : Date.now());
  if (lastDown.id === id && now - lastDown.t < 420) {
    lastDown = { id: null, t: 0 };
    state.dragging = null;
    toggleCollapse(id);
    return;
  }
  lastDown = { id, t: now };

  state.selected = id;
  state.selectedLink = null;
  const p0 = svgPoint(ev);
  const L = computeLayout();
  const node = L.pos.get(id);
  if (!node) return;
  const off = state.offsets[id] || { dx: 0, dy: 0 };
  state.dragging = {
    id,
    grabX: p0.x - node.x,
    grabY: p0.y - node.y,
    baseX: node.x - off.dx,
    baseY: node.y - off.dy,
    moved: false,
  };
  render();
  renderProps();
}

function startLink(ev, id) {
  ev.stopPropagation();
  ev.preventDefault();
  state.linking = { from: id, ...svgPoint(ev) };
}

window.addEventListener('pointermove', (ev) => {
  if (state.dragging) {
    const p = svgPoint(ev);
    const d = state.dragging;
    const nx = Math.max(2, p.x - d.grabX);
    const ny = Math.max(2, p.y - d.grabY);
    state.offsets[d.id] = { dx: nx - d.baseX, dy: ny - d.baseY };
    d.moved = true;
    render();
    return;
  }
  if (state.linking) {
    const p = svgPoint(ev);
    state.linking.mx = p.x; state.linking.my = p.y;
    render();
  }
});

window.addEventListener('pointerup', (ev) => {
  if (state.dragging) {
    const d = state.dragging;
    state.dragging = null;
    if (!d.moved) select(d.id);
    else histPush();          // 拖拽结束记一次历史
    return;
  }
  if (state.linking) {
    const p = svgPoint(ev);
    const L = computeLayout();
    // 找到落点节点
    let target = null;
    for (const [id, pos] of L.pos) {
      if (pos.x <= p.x && p.x <= pos.x + LAY.w && pos.y <= p.y && p.y <= pos.y + LAY.h) { target = id; break; }
    }
    const from = state.linking.from;
    state.linking = null;
    if (target && target !== from) addConnection(from, target);
    else render();
  }
});

function addConnection(from, to) {
  if (from === to) {
    toast('不能连接到自身', 'err');
    render();
    return;
  }
  if (state.tree.connections.some((c) => c.from === from && c.to === to)) {
    toast('连接已存在', 'err');
    render();
    return;
  }
  // medini：连接只能自上而下，且禁止成环（"not possible in this direction"）
  if (isInSubtree(to, from)) {
    toast('不允许的连接方向：目标在自身子树内，会形成环路', 'err');
    render();
    return;
  }
  state.tree.connections.push({ from, to });
  const { map } = index();
  const n = map.get(from);
  if (n && !n.gate) n.gate = 'OR';
  render();
}

function deleteConn(c) {
  const i = state.tree.connections.indexOf(c);
  if (i >= 0) state.tree.connections.splice(i, 1);
  state.selectedLink = null;
  render();
}

$('#canvas').addEventListener('pointerdown', (ev) => {
  if (ev.target === $('#canvas')) { state.selected = null; state.selectedLink = null; render(); renderProps(); }
});

window.addEventListener('keydown', (ev) => {
  if (/INPUT|TEXTAREA|SELECT/.test(ev.target.tagName)) return;
  if (ev.key === 'Delete' || ev.key === 'Backspace') {
    if (state.selectedLink) { ev.preventDefault(); deleteConn(state.selectedLink); }
    else if (state.selected) { ev.preventDefault(); deleteNode(state.selected); }
  }
  if (ev.key === 'Escape') {
    state.linking = null; state.dragging = null;
    state.selected = null; state.selectedLink = null; render(); renderProps();
  }
});

function deleteNode(id) {
  state.tree.nodes = state.tree.nodes.filter((n) => n.id !== id);
  state.tree.connections = state.tree.connections.filter((c) => c.from !== id && c.to !== id);
  delete state.offsets[id];
  if (state.flash === id) state.flash = null;
  if (state.selected === id) state.selected = null;
  render(); renderProps(); renderOutline();
}

// ===== 符号面板 =====
/** 添加事件节点。parentId 指定父节点（medini 式：在父节点下插入子事件）；
 *  不指定时回退到当前选中可挂载节点 / 顶事件，确保节点一定挂到树上。 */
function addEvent(type, parentId) {
  const L = computeLayout();
  const id = newId();
  const node = {
    id, type,
    name: (TYPE_LABEL[type] || '新节点') + (state.tree.nodes.filter((n) => n.type === type).length + 1),
    gate: GATEABLE_TYPES.includes(type) ? 'OR' : null,
    voteK: 2, voteN: 2, description: '', ref: '', component: '', failureMode: '',
    probModel: 'fixed', prob: type === 'basic' ? 1e-3 : null, lambda: null,
  };
  state.tree.nodes.push(node);

  const { map } = index();
  let parent = parentId || null;
  if (!parent) {
    if (state.selected && state.selected !== id &&
        GATEABLE_TYPES.includes(map.get(state.selected)?.type)) parent = state.selected;
    else parent = L.rootId;
  }
  if (parent && parent !== id &&
      !state.tree.connections.some((c) => c.from === parent && c.to === id)) {
    state.tree.connections.push({ from: parent, to: id });
    const pn = map.get(parent);
    if (pn && !pn.gate) pn.gate = 'OR';
  }

  state.selected = id;
  state.flash = id;
  clearTimeout(state._flashT);
  state._flashT = setTimeout(() => { if (state.flash === id) { state.flash = null; render(); } }, 1500);

  render(); renderProps(); renderOutline();
  focusNode(id, true);
  return id;
}

$$('.pal-item[data-add]').forEach((b) => {
  b.addEventListener('click', () => {
    const type = b.dataset.add;
    const id = addEvent(type);
    const n = state.tree.nodes.find((x) => x.id === id);
    toast(`已添加${TYPE_LABEL[type]}：${n?.name || id}`);
  });
});

// ===== 右键上下文菜单（类 medini：在节点上右键操作） =====
const CTX_CHILD_TYPES = [
  ['intermediate', '中间事件'], ['basic', '基本事件'], ['undeveloped', '未开发事件'],
  ['condition', '条件事件'], ['external', '外部事件'], ['house', '房屋事件'], ['comment', '注释'],
];
const CTX_GATES = ['AND', 'OR', 'XOR', 'NOT', 'VOTE'];

function openCtx(ev, id) {
  ev.preventDefault();
  ev.stopPropagation();
  select(id);
  const menu = $('#ctx');
  const { map } = index();
  const n = map.get(id);
  if (!n) return;
  const gateable = GATEABLE_TYPES.includes(n.type);

  let h = `<div class="ctx-label">插入子事件（在「${esc(n.name || id)}」下）</div>`;
  for (const [t, label] of CTX_CHILD_TYPES) {
    h += `<div class="ctx-item" data-act="child" data-type="${t}"><span>${label}</span><span class="ctx-sub">${TYPE_LABEL[t] || ''}</span></div>`;
  }
  if (gateable) {
    h += '<div class="ctx-sep"></div><div class="ctx-label">设置逻辑门</div>';
    for (const g of CTX_GATES) {
      const on = n.gate === g ? ' ✓' : '';
      h += `<div class="ctx-item" data-act="gate" data-gate="${g}"><span>${GATE_LABEL[g]}</span><span class="ctx-sub">${on}</span></div>`;
    }
  }
  h += '<div class="ctx-sep"></div>';
  h += `<div class="ctx-item" data-act="calc"><span>计算概率 · Calculate probabilities</span></div>`;
  h += `<div class="ctx-item" data-act="eval"><span>评估故障树 · Evaluate Fault Tree</span></div>`;
  h += '<div class="ctx-sep"></div>';
  h += `<div class="ctx-item" data-act="fold"><span>${n.collapsed ? '展开子树' : '折叠子树'}</span><span class="ctx-sub">双击</span></div>`;
  h += `<div class="ctx-item" data-act="pagebreak"><span>${n.pageBreak ? '取消分页点' : '分页：从此事件另起一页'}</span><span class="ctx-sub">${n.pageBreak ? '✓ 已设' : '打印'}</span></div>`;
  // 分页视图下，虚线分页点/承接事件才有对面的页可跳
  const jt = state.pagination ? jumpTargetFor(id) : 0;
  if (jt) h += `<div class="ctx-item" data-act="jump"><span>跳转到第 ${jt} 页</span><span class="ctx-sub">分页</span></div>`;
  h += `<div class="ctx-item" data-act="arrange"><span>整理子树 · Arrange Subtree</span></div>`;
  h += `<div class="ctx-item" data-act="boolean"><span>布尔表达式 · Boolean Expression</span></div>`;
  h += '<div class="ctx-sep"></div>';
  h += `<div class="ctx-item danger" data-act="del"><span>删除事件</span></div>`;

  menu.innerHTML = h;
  menu.hidden = false;
  const mw = menu.offsetWidth || 210, mh = menu.offsetHeight || 320;
  menu.style.left = Math.min(ev.clientX, window.innerWidth - mw - 8) + 'px';
  menu.style.top = Math.min(ev.clientY, window.innerHeight - mh - 8) + 'px';

  menu.querySelectorAll('.ctx-item').forEach((it) => {
    it.addEventListener('click', (e2) => {
      e2.stopPropagation();
      closeCtx();
      const act = it.dataset.act;
      if (act === 'child') {
        const cid = addEvent(it.dataset.type, id);
        const cn = state.tree.nodes.find((x) => x.id === cid);
        toast(`已在「${n.name || id}」下插入${TYPE_LABEL[it.dataset.type]}：${cn?.name || cid}`);
      } else if (act === 'gate') {
        const { map: m2 } = index();
        const nn = m2.get(id);
        if (nn) {
          nn.gate = it.dataset.gate;
          if (nn.gate === 'VOTE') { nn.voteK = nn.voteK || 2; nn.voteN = nn.voteN || 2; }
          render(); renderProps();
          toast(`已将「${nn.name || id}」设为 ${GATE_LABEL[nn.gate] || nn.gate}`);
        }
      } else if (act === 'del') {
        deleteNode(id);
      } else if (act === 'calc') {
        calculateThen('results');
      } else if (act === 'eval') {
        calculateThen('cutsets');
      } else if (act === 'fold') {
        toggleCollapse(id);
      } else if (act === 'pagebreak') {
        togglePageBreak(id);
      } else if (act === 'jump') {
        gotoPage(jumpTargetFor(id));
      } else if (act === 'arrange') {
        arrangeSubtree(id);
      } else if (act === 'boolean') {
        showBooleanExpression(id);
      }
    });
  });
}

function closeCtx() { const m = $('#ctx'); if (m) m.hidden = true; }

async function calculateThen(tab) {
  await calculate();
  if (tab) switchTab(tab);
}

// 关闭菜单：点击空白处 / Esc / 在空白画布右键
document.addEventListener('pointerdown', (e) => {
  const m = $('#ctx');
  if (m && !m.hidden && !m.contains(e.target)) m.hidden = true;
});
window.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeCtx(); });
$('#canvas').addEventListener('contextmenu', (e) => {
  if (e.target === $('#canvas')) { e.preventDefault(); closeCtx(); }
});

$$('.pal-item[data-gate]').forEach((b) => {
  b.addEventListener('click', () => {
    if (!state.selected) { toast('请先选中一个节点', 'err'); return; }
    const { map, hasKids } = index();
    const n = map.get(state.selected);
    if (!n) return;
    if (!GATEABLE_TYPES.includes(n.type)) { toast('只有顶事件/中间事件可设置逻辑门', 'err'); return; }
    n.gate = b.dataset.gate;
    if (n.gate === 'VOTE') { n.voteK = n.voteK || 2; n.voteN = n.voteN || 2; }
    render(); renderProps();
    toast(`已设置为 ${GATE_LABEL[n.gate] || n.gate}`);
  });
});

// ===== 属性面板 =====
const P = {
  name: $('#p-name'), type: $('#p-type'), gate: $('#p-gate'),
  votek: $('#p-votek'), voten: $('#p-voten'), model: $('#p-model'),
  prob: $('#p-prob'), lambda: $('#p-lambda'), beta: $('#p-beta'),
  nd: $('#p-nd'), dp: $('#p-dp'), tmr: $('#p-tmr'), ti: $('#p-ti'),
  comp: $('#p-comp'), ref: $('#p-ref'), desc: $('#p-desc'),
};

function fillTypeSelect() {
  P.type.innerHTML = Object.entries(TYPE_LABEL)
    .map(([v, l]) => `<option value="${v}">${l}</option>`).join('');
}

function renderProps() {
  const { map } = index();
  const n = state.selected ? map.get(state.selected) : null;
  $('#props-empty').hidden = !!n;
  $('#props-form').hidden = !n;
  if (!n) return;

  P.name.value = n.name || '';
  P.type.value = n.type;
  const canGate = GATEABLE_TYPES.includes(n.type);
  $('#wrap-gate').style.display = canGate ? '' : 'none';
  $('#wrap-vote').style.display = canGate && n.gate === 'VOTE' ? '' : 'none';
  if (canGate) P.gate.value = n.gate || 'OR';
  P.votek.value = n.voteK ?? 2;
  P.voten.value = n.voteN ?? 2;
  P.model.value = n.probModel || 'fixed';
  P.prob.value = n.prob ?? '';
  P.lambda.value = n.lambda ?? '';
  P.beta.value = n.beta ?? '';
  P.nd.value = n.demandCount ?? '';
  P.dp.value = n.demandProb ?? '';
  P.tmr.value = n.repairTime ?? '';
  P.ti.value = n.monitorInterval ?? '';
  P.comp.value = n.component || '';
  P.ref.value = n.ref || '';
  P.desc.value = n.description || '';
  updateProbFields();
}

function updateProbFields() {
  const m = P.model.value;
  $$('[data-for]').forEach((f) => {
    f.style.display = f.dataset.for.split(',').includes(m) ? '' : 'none';
  });
}

const numOrNull = (v) => (v === '' || v == null ? null : Number(v));

function bindProp(input, fn) {
  const h = () => {
    const { map } = index();
    const n = state.selected ? map.get(state.selected) : null;
    if (!n) return;
    fn(n, input);
    render();
  };
  input.addEventListener('input', h);
  input.addEventListener('change', h);
}

bindProp(P.name, (n, i) => { n.name = i.value; renderOutline(); });
bindProp(P.type, (n, i) => {
  n.type = i.value;
  if (!GATEABLE_TYPES.includes(n.type)) n.gate = null;
  else if (!n.gate) n.gate = 'OR';
  renderProps();
});
bindProp(P.gate, (n, i) => { n.gate = i.value; renderProps(); });
bindProp(P.votek, (n, i) => { n.voteK = numOrNull(i.value) || 1; });
bindProp(P.voten, (n, i) => { n.voteN = numOrNull(i.value) || 1; });
bindProp(P.model, (n, i) => { n.probModel = i.value; updateProbFields(); });
bindProp(P.prob, (n, i) => { n.prob = numOrNull(i.value); });
bindProp(P.lambda, (n, i) => { n.lambda = numOrNull(i.value); });
bindProp(P.beta, (n, i) => { n.beta = numOrNull(i.value); });
bindProp(P.nd, (n, i) => { n.demandCount = numOrNull(i.value); });
bindProp(P.dp, (n, i) => { n.demandProb = numOrNull(i.value); });
bindProp(P.tmr, (n, i) => { n.repairTime = numOrNull(i.value); });
bindProp(P.ti, (n, i) => { n.monitorInterval = numOrNull(i.value); });
bindProp(P.comp, (n, i) => { n.component = i.value; });
bindProp(P.ref, (n, i) => { n.ref = i.value; });
bindProp(P.desc, (n, i) => { n.description = i.value; });

$('#p-delete').addEventListener('click', () => { if (state.selected) deleteNode(state.selected); });
$('#p-collapse').addEventListener('click', () => {
  if (!state.selected) return;
  const { map, kids } = index();
  const n = map.get(state.selected);
  if (!n) return;
  if (!(kids.get(n.id) || []).length) { toast('该事件没有子事件', 'err'); return; }
  n.collapsed = !n.collapsed;
  render(); renderProps(); renderOutline();
  toast(n.collapsed ? '已折叠子事件' : '已展开子事件');
});

function bindMeta() {
  $('#meta-title').value = state.tree.meta.title || '';
  $('#meta-title').addEventListener('input', (e) => { state.tree.meta.title = e.target.value; });
  $('#meta-mission').value = state.tree.settings.missionTime ?? '';
  $('#meta-mission').addEventListener('input', (e) => {
    const v = numOrNull(e.target.value);
    state.tree.settings.missionTime = v;
    state.tree.meta.missionTime = v;
  });
  const s = state.tree.settings;
  $('#s-order').value = s.maxCutSetOrder ?? 0;
  $('#s-trunc').value = s.truncation ?? 1e-12;
  $('#s-method').value = s.quantification || 'auto';
  $('#s-std').value = state.tree.meta.standard || '';
  $('#s-proj').value = state.tree.meta.project || '';
  $('#s-order').addEventListener('input', (e) => { s.maxCutSetOrder = numOrNull(e.target.value) ?? 0; });
  $('#s-trunc').addEventListener('input', (e) => { s.truncation = numOrNull(e.target.value) ?? 0; });
  $('#s-method').addEventListener('change', (e) => { s.quantification = e.target.value; });
  $('#s-std').addEventListener('input', (e) => { state.tree.meta.standard = e.target.value; });
  $('#s-proj').addEventListener('input', (e) => { state.tree.meta.project = e.target.value; });
}

// ===== 结果 / 割集 / 大纲 =====
// 统一 API 助手：按响应 Content-Type 自动解析为 JSON 或纯文本
async function api(path, body, want = 'json') {
  const res = await fetch('/api/' + path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body ?? { tree: state.tree }),
  });
  if (!res.ok) throw new Error(await res.text());
  if (want === 'text') return res.text();
  const ct = res.headers.get('Content-Type') || '';
  if (!ct.includes('application/json')) return res.text();
  return res.json();
}

async function calculate() {
  const btn = $('#btn-calc');
  btn.disabled = true;
  btn.textContent = '计算中…';
  try {
    const r = await api('analyze', { tree: state.tree, options: { report: 'none' } });
    state.result = r;
    state.heatmap = r.heatmap || {};
    state.nodeProbs = r.nodeProbs || {};
    renderResults(r);
    renderCutSets(r);
    render();
    if (!r.validation?.ok) toast('模型存在问题，请检查提示', 'err');
    else toast('分析完成', 'ok');
  } catch (e) {
    toast('计算失败: ' + e.message, 'err');
  } finally {
    btn.disabled = false;
    btn.textContent = '重新计算分析';
  }
}

function kpi(k, v, cls = '') {
  return `<div class="kpi ${cls}"><div class="k">${k}</div><div class="v">${v}</div></div>`;
}

function renderResults(r) {
  const m = r.metrics || {};
  const sp = m.cutSets?.singlePoints ?? 0;
  let h = '<div class="kpi-grid">';
  h += kpi('顶事件概率 Q(TOP)', fmtQ(m.topProb), 'hi');
  h += kpi('系统可靠度 R', fmtQ(m.reliability), 'ok');
  h += kpi('最小割集', m.cutSets?.total ?? '—');
  h += kpi('单一失效点', sp, sp > 0 ? 'hi' : 'ok');
  h += '</div>';

  h += `<div class="sec-title">求解信息</div>`;
  h += `<table class="res"><tbody>
    <tr><td>求解方法</td><td>${esc(m.topProbMethod || '—')}</td></tr>
    <tr><td>任务时间</td><td>${m.missionTime != null ? m.missionTime + ' h' : '—'}</td></tr>
    <tr><td>树结构</td><td>${m.nonCoherent ? '非相干' : '相干'}</td></tr>
    <tr><td>BDD 节点</td><td>${m.bddSize ?? '—'}</td></tr>
    <tr><td>稀有事件近似</td><td>${fmtQ(m.rareEventSum)}</td></tr>
    <tr><td>MCUB 上界</td><td>${fmtQ(m.mcub)}</td></tr>
    <tr><td>割集阶数分布</td><td>${Object.entries(m.cutSets?.byOrder || {}).map(([k, v]) => `${k}阶:${v}`).join(' / ') || '—'}</td></tr>
    <tr><td>计算耗时</td><td>${r.timing?.computeMs ?? '—'} ms</td></tr>
  </tbody></table>`;

  if (m.truncated) {
    h += `<div class="note warn">⚠ 割集已按阶数/概率阈值截断，完整性受限。可在「属性 → 模型设置」中调整阈值。</div>`;
  }
  if (sp > 0) {
    h += `<div class="note warn">⚠ 发现 <b>${sp}</b> 个单一失效点（1 阶割集）：单个基本事件失效即导致顶事件，属于系统性单点失效，须通过冗余或安全机制消除。</div>`;
  }

  const imp = r.importance || [];
  if (imp.length) {
    h += `<div class="sec-title">重要度排名（前 15）</div>`;
    h += `<table class="res"><thead><tr><th>#</th><th class="nm">事件</th><th>q</th><th>关键</th><th>FV</th></tr></thead><tbody>`;
    for (const x of imp.slice(0, 15)) {
      const b = x.criticality >= 0.5 ? 'd1' : x.criticality >= 0.2 ? 'd2' : x.criticality >= 0.05 ? 'd3' : x.criticality >= 0.01 ? 'd4' : 'dn';
      h += `<tr>
        <td>${x.rank}</td>
        <td class="nm" title="${esc(x.component || '')}">${esc(x.name)}</td>
        <td>${fmtQ(x.probability)}</td>
        <td><span class="badge ${b}">${fmtQ(x.criticality)}</span></td>
        <td>${fmtQ(x.fussellVesely)}</td>
      </tr>`;
    }
    h += '</tbody></table>';
    h += `<div class="note"><b>关键重要度</b> = q·Birnbaum / Q(TOP)，表示该事件对顶事件的实际贡献占比。<br/><b>FV</b> = 消除该事件能降低的风险比例。</div>`;
  }

  const w = (r.validation?.warnings || []);
  const e = (r.validation?.errors || []);
  if (e.length) h += `<div class="note warn"><b>错误</b><br/>${e.map(esc).join('<br/>')}</div>`;
  if (w.length) h += `<div class="note"><b>提示</b><br/>${w.slice(0, 8).map(esc).join('<br/>')}</div>`;

  $('#results-body').innerHTML = h;
}

function renderCutSets(r) {
  const items = r.cutSets?.items || [];
  if (!items.length) { $('#cutsets-body').innerHTML = '<div class="empty">未生成割集<br/><small>请检查顶事件与基本事件定义</small></div>'; return; }
  const m = r.metrics || {};
  let h = `<div class="note">共 <b>${items.length}</b> 个最小割集。1 阶为单点失效，需优先消除；阶数越高越难同时发生。</div>`;
  h += `<table class="res"><thead><tr><th>#</th><th>阶</th><th class="nm">构成</th><th>概率</th></tr></thead><tbody>`;
  for (const c of items.slice(0, 500)) {
    const badge = c.order === 1 ? 'd1' : c.order === 2 ? 'd2' : c.order === 3 ? 'd3' : 'dn';
    h += `<tr><td>${c.index}</td><td><span class="badge ${badge}">${c.order}</span></td>
      <td class="nm" title="${esc(c.names.join(' ∧ '))}">${esc(c.names.join(' ∧ '))}</td>
      <td>${fmtQ(c.probability)}</td></tr>`;
  }
  h += '</tbody></table>';
  if (items.length > 500) h += `<div class="note">仅显示前 500 项，共 ${items.length} 个。完整清单请导出报告。</div>`;
  $('#cutsets-body').innerHTML = h;
}

function renderOutline() {
  const { map, kids } = index();
  const rootId = state.tree.nodes.find((n) => n.type === 'top')?.id;
  if (!rootId) { $('#outline-body').innerHTML = '<div class="empty">无顶事件</div>'; return; }
  const rows = [];
  const walk = (id, d) => {
    const n = map.get(id);
    if (!n) return;
    rows.push({ d, id, n });
    if (n.collapsed) return;
    for (const k of kids.get(id) || []) walk(k, d + 1);
  };
  walk(rootId, 0);
  $('#outline-body').innerHTML = rows.map(({ d, id, n }) => `
    <div class="out-line${state.selected === id ? ' sel' : ''}" data-id="${id}" style="padding-left:${6 + d * 14}px">
      <span class="out-dot ${n.type}"></span>
      <span class="out-name">${esc(n.name || TYPE_LABEL[n.type])}</span>
      ${n.gate && kids.get(id).length ? `<span class="out-gate">${n.gate === 'VOTE' ? `${n.gate} ${n.voteK}/${n.voteN}` : n.gate}</span>` : ''}
      ${state.showProb && n.type === 'basic' && n.prob != null ? `<span class="out-prob">${fmtQ(n.prob)}</span>` : ''}
    </div>`).join('');
  $$('#outline-body .out-line').forEach((e2) => {
    e2.addEventListener('click', () => select(e2.dataset.id));
  });
}

function switchTab(name) {
  $$('.stab').forEach((b) => b.classList.toggle('active', b.dataset.tab === name));
  $$('.tabpane').forEach((p) => p.classList.toggle('active', p.id === 'tab-' + name));
}
$$('.stab').forEach((b) => b.addEventListener('click', () => switchTab(b.dataset.tab)));

// ===== 跨页 / 分页 =====

async function computePagination() {
  const maxNodes = Number($('#pg-size').value || 24);
  // 画图人设了分页点 → 严格按分页点切（不管节点多少，哪怕只有几个节点）
  const breaks = state.tree.nodes.filter((n) => n.pageBreak);
  const manual = breaks.length > 0;
  try {
    const r = await api('paginate', {
      tree: state.tree,
      options: manual ? { mode: 'band', maxNodes: 14 } : { maxNodes, force: true },
    });
    state.pagination = { ...r, pageIndex: 1 };
    $('#pagebar').hidden = r.total <= 1;
    if (r.total <= 1) {
      state.pagination = null;
      renderPageInfoIfAny();
      render();
      toast(manual
        ? `已设 ${breaks.length} 个分页点，但都落在同一页内`
        : `未设分页点：右键任意事件选「分页：从此事件另起一页」，即可自己决定分页`, 'ok');
      return;
    }
    renderPageInfo();
    render();
    toast(manual
      ? `已按 ${breaks.length} 个分页点切分为 ${r.total} 页`
      : `已自动切分为 ${r.total} 页（右键事件可手动指定分页点）`, 'ok');
  } catch (e) { toast('分页失败: ' + e.message, 'err'); }
}

function renderPageInfoIfAny() {
  if (!state.pagination) { const bar = $('#pagebar'); if (bar) bar.hidden = true; }
}

function renderPageInfo() {
  const p = state.pagination;
  if (!p) return;
  const cur = p.pages.find((x) => x.index === p.pageIndex);
  $('#pg-info').textContent = `第 ${p.pageIndex} / ${p.total} 页 — ${cur?.title || ''}（${cur?.nodeCount || 0} 节点）`;
  $('#pg-prev').disabled = p.pageIndex <= 1;
  $('#pg-next').disabled = p.pageIndex >= p.total;
  $('#pg-first').disabled = p.pageIndex <= 1;
  $('#pg-last').disabled = p.pageIndex >= p.total;
  renderJumpButton();
}

/** 分页导航条上的「跳到第 N 页」按钮：本页虚线分页点在哪一页展开 */
function renderJumpButton() {
  const b = $('#pg-jump');
  const p = state.pagination;
  if (!b) return;
  if (!p) { b.hidden = true; return; }
  // 页底的 + 页顶的都算，各自有"对面那一页"
  const marks = [
    ...(p.extraOf?.[p.pageIndex] || []),
    ...(p.contOf?.[p.pageIndex] || []),
  ];
  const targets = marks
    .map((id) => ({ id, page: jumpTargetFor(id) }))
    .filter((m) => m.page);
  if (!targets.length) { b.hidden = true; return; }
  const nm = (id) => state.tree.nodes.find((n) => n.id === id)?.name || id;
  const first = targets[0];
  b.hidden = false;
  b.textContent = `↪ 第 ${first.page} 页`;
  b.title = targets.map((m) => `「${nm(m.id)}」→ 第 ${m.page} 页`).join('\n')
    + '\n\n（也可以直接点画布上虚线框上方的绿色标签）';
  b.onclick = () => gotoPage(first.page);
}

function gotoPage(n) {
  const p = state.pagination;
  if (!p) return;
  p.pageIndex = Math.max(1, Math.min(p.total, n));
  // 清空选中，避免高亮到本页不可见的节点
  state.selected = null;
  state.selectedLink = null;
  renderPageInfo();
  render();
  renderProps();
  renderOutline();
}

function exitPagination() {
  state.pagination = null;
  $('#pagebar').hidden = true;
  render();
  toast('已退出分页视图');
}

$('#btn-pages').addEventListener('click', computePagination);
$('#pg-first').addEventListener('click', () => gotoPage(1));
$('#pg-prev').addEventListener('click', () => gotoPage(state.pagination.pageIndex - 1));
$('#pg-next').addEventListener('click', () => gotoPage(state.pagination.pageIndex + 1));
$('#pg-last').addEventListener('click', () => gotoPage(state.pagination.total));
$('#pg-reflow').addEventListener('click', () => {
  const cur = state.pagination?.pageIndex || 1;
  computePagination().then(() => gotoPage(cur));
});
$('#pg-exit').addEventListener('click', exitPagination);
$('#pg-size').addEventListener('change', () => {
  if (state.pagination) computePagination();
});

// ===== 导入导出 =====

const EXPORT_META = {
  faulttreeplus: { ext: 'xml', label: 'FaultTree+ XML', mime: 'application/xml' },
  cafta: { ext: 'xml', label: 'CAFTA XML', mime: 'application/xml' },
  medini: { ext: 'json', label: 'medini 交换 JSON', mime: 'application/json' },
  svg: { ext: 'svg', label: 'SVG 图形', mime: 'image/svg+xml' },
  a4: { ext: 'html', label: 'A4 分页图（可打印 PDF）', mime: 'text/html' },
  json: { ext: 'json', label: '内部 JSON', mime: 'application/json' },
  dsl: { ext: 'fta', label: '紧凑 DSL', mime: 'text/plain' },
};

async function doExport(fmt) {
  const meta = EXPORT_META[fmt];
  if (!meta) return;
  $('#export-menu').hidden = true;
  try {
    toast('正在导出…');
    const options = { format: fmt };
    if (state.pagination) options.maxNodes = Number($('#pg-size').value || 24);

    let content;
    if (fmt === 'svg') {
      const heatmap = state.heatmap;
      const view = await currentViewSvg(heatmap);
      content = view;
    } else if (fmt === 'a4') {
      // A4 分页 HTML：前沿推进分页，下一页顶事件 = 上一页页底事件
      // 每页事件数默认 14（字号可读）；若已打开分页面板，则采用面板设定并限制在 6..24
      const raw = Number($('#pg-size')?.value || 14);
      const budget = state.pagination ? Math.min(24, Math.max(6, raw || 14)) : 14;
      const res = await fetch('/api/svg-a4', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tree: state.tree,
          options: { budget, heatmap: true },
        }),
      });
      if (!res.ok) throw new Error('A4 分页导出失败（HTTP ' + res.status + '）');
      content = await res.text();
    } else {
      content = await api('export', { tree: state.tree, options }, 'text');
    }
    const name = (state.tree.meta?.title || 'fault-tree').replace(/[\\/:*?"<>|]/g, '_');
    download(`${name}.${meta.ext}`, content, meta.mime);
    toast(`已导出 ${meta.label}`, 'ok');
  } catch (e) {
    toast('导出失败: ' + e.message, 'err');
  }
}

async function currentViewSvg(heatmap) {
  if (state.pagination) {
    const res = await fetch('/api/page-svg', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tree: state.tree,
        options: {
          maxNodes: Number($('#pg-size').value || 24),
          pageIndex: state.pagination.pageIndex,
          force: true,
        },
      }),
    });
    return await res.text();
  }
  const res = await fetch('/api/svg', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ tree: state.tree, options: { heatmap: true } }),
  });
  return await res.text();
}

// 导出菜单
$('#btn-export-menu').addEventListener('click', (e) => {
  e.stopPropagation();
  const m = $('#export-menu');
  m.hidden = !m.hidden;
});
document.addEventListener('click', (e) => {
  const m = $('#export-menu');
  if (!m.hidden && !m.contains(e.target)) m.hidden = true;
});
$$('[data-export]').forEach((b) => b.addEventListener('click', () => doExport(b.dataset.export)));

// 导入
$('#btn-import').addEventListener('click', () => $('#file-import').click());
$('#file-import').addEventListener('change', async (e) => {
  const file = e.target.files?.[0];
  if (!file) return;
  try {
    toast('正在导入…');
    const content = await file.text();
    const r = await api('import', { content, filename: file.name });
    if (!r.ok) {
      toast('导入有问题: ' + (r.validation?.errors?.[0] || '未知错误'), 'err');
    }
    state.tree = r.tree;
    state.selected = null;
    state.result = null;
    state.heatmap = {};
    state.pagination = null;
    state.offsets = {}; state.flash = null;
    $('#pagebar').hidden = true;
    bindMeta(); fitView(); renderProps(); renderOutline();
    toast(`已导入 ${file.name}（格式：${r.format}）`, 'ok');
  } catch (err) {
    toast('导入失败: ' + err.message, 'err');
  } finally {
    e.target.value = '';
  }
});
$('#btn-new').addEventListener('click', () => {
  if (!confirm('确定新建故障树？当前内容将丢失。')) return;
  state.tree = newTree();
  state.selected = null; state.result = null; state.heatmap = {};
  state.offsets = {}; state.flash = null; state.pagination = null;
  $('#pagebar').hidden = true;
  bindMeta(); fitView(); renderProps(); renderOutline();
  toast('已新建故障树');
});

// 文档标签上的 ×：等价于「新建」
$('#btn-new-tab').addEventListener('click', () => {
  if (!confirm('新建故障树？当前内容将丢失。')) return;
  state.tree = newTree();
  state.selected = null; state.result = null; state.heatmap = {};
  state.offsets = {}; state.flash = null; state.pagination = null;
  $('#pagebar').hidden = true;
  bindMeta(); fitView(); renderProps(); renderOutline();
  toast('已新建故障树');
});

$('#btn-example').addEventListener('click', async () => {
  try {
    const list = await (await fetch('/api/examples')).json();
    const names = list.examples.map((e) => e.name);
    const pick = prompt(`加载内置示例：\n${names.join('\n')}\n\n请输入名称：`, names[0]);
    if (!pick) return;
    const r = await (await fetch('/api/example/' + encodeURIComponent(pick))).json();
    if (!r.ok) { toast(r.error || '加载失败', 'err'); return; }
    state.tree = r.tree;
    state.selected = null; state.heatmap = r.analysis?.heatmap || {}; state.result = r.analysis;
    state.offsets = {}; state.flash = null; state.pagination = null;
    $('#pagebar').hidden = true;
    bindMeta(); fitView(); renderProps(); renderOutline();
    if (r.analysis) { renderResults(r.analysis); renderCutSets(r.analysis); }
    toast(`已加载示例：${r.analysis?.meta?.title || pick}`, 'ok');
  } catch (e) { toast('加载失败: ' + e.message, 'err'); }
});

$('#btn-layout').addEventListener('click', () => {
  state.offsets = {};
  fitView();
  toast('已自动布局并适配视图');
});

// ===== 撤销 / 重做：按钮 + 快捷键 =====
$('#btn-undo').addEventListener('click', undo);
$('#btn-redo').addEventListener('click', redo);
window.addEventListener('keydown', (ev) => {
  const mod = ev.ctrlKey || ev.metaKey;
  if (!mod || isTextEditing(ev.target)) return;
  const k = (ev.key || '').toLowerCase();
  if (k === 'z' && !ev.shiftKey) {
    ev.preventDefault();
    undo();
  } else if (k === 'y' || (k === 'z' && ev.shiftKey)) {
    ev.preventDefault();
    redo();
  }
});

// ===== 视图：聚焦 / 居中 / 适配 =====
function updateZoomLabel() {
  const v = $('#zoom-val');
  if (v) v.textContent = Math.round(state.zoom * 100) + '%';
}

/** 将某个节点滚动到可视区中央（解决新节点“往右走、看不见”） */
function focusNode(id, smooth = false) {
  const sc = $('#scroll');
  if (!sc) return;
  const L = computeLayout();
  const p = L.pos.get(id);
  if (!p) return;
  const z = state.zoom;
  const cx = (p.x + LAY.w / 2) * z;
  const cy = (p.y + LAY.h / 2) * z;
  sc.scrollTo({
    left: Math.max(0, cx - sc.clientWidth / 2),
    top: Math.max(0, cy - sc.clientHeight / 2),
    behavior: smooth ? 'smooth' : 'auto',
  });
}

/** 内容整体居中 */
function centerView(smooth = false) {
  const sc = $('#scroll');
  if (!sc) return;
  const L = computeLayout();
  const z = state.zoom;
  sc.scrollTo({
    left: Math.max(0, (L.w * z - sc.clientWidth) / 2),
    top: Math.max(0, (L.h * z - sc.clientHeight) / 2),
    behavior: smooth ? 'smooth' : 'auto',
  });
}

/** 缩放到刚好容纳整棵树并居中 */
function fitView() {
  const sc = $('#scroll');
  const L = computeLayout();
  if (!L.w || !L.h) { render(); return; }
  // 容器尚未完成布局测量时，退回 100%，避免算出过小的缩放
  if (sc.clientWidth < 40 || sc.clientHeight < 40) {
    state.zoom = 1;
    updateZoomLabel();
    render();
    return;
  }
  const cw = Math.max(80, sc.clientWidth - 32);
  const ch = Math.max(80, sc.clientHeight - 32);
  const z = Math.min(cw / L.w, ch / L.h, 1.25);
  state.zoom = Math.max(0.2, Math.min(3, z));
  updateZoomLabel();
  render();
  centerView();
}

// ===== 缩放（对标 medini 视图缩放：+/-/比例/适应） =====
function applyZoom(z) {
  state.zoom = Math.max(0.2, Math.min(3, z));
  updateZoomLabel();
  render();
  if (state.selected) focusNode(state.selected);
  else centerView();
}
$('#zoom-in').addEventListener('click', () => applyZoom(state.zoom * 1.2));
$('#zoom-out').addEventListener('click', () => applyZoom(state.zoom / 1.2));
$('#zoom-val').addEventListener('click', () => applyZoom(1));
$('#btn-fit').addEventListener('click', fitView);

$('#chk-heat').addEventListener('change', (e) => { state.heat = e.target.checked; render(); });
$('#chk-prob').addEventListener('change', (e) => { state.showProb = e.target.checked; render(); renderOutline(); renderProps(); });
$('#chk-ids').addEventListener('change', (e) => { state.showIds = e.target.checked; render(); });

// ===== 图例显隐（可关闭；状态持久化到 localStorage） =====
function setLegendVisible(v, persist = true) {
  const box = $('#legend');
  const chk = $('#chk-legend');
  if (box) box.hidden = !v;
  if (chk) chk.checked = v;
  if (persist) { try { localStorage.setItem('fta.legend', v ? '1' : '0'); } catch { /* 隐私模式忽略 */ } }
}
$('#legend-close').addEventListener('click', () => setLegendVisible(false));
$('#chk-legend').addEventListener('change', (e) => setLegendVisible(e.target.checked));

$('#btn-outline').addEventListener('click', () => switchTab('outline'));
$('#btn-calc').addEventListener('click', calculate);

$('#btn-report').addEventListener('click', async () => {
  const btn = $('#btn-report');
  btn.disabled = true;
  btn.textContent = '生成中…';
  try {
    const md = await api('report', { tree: state.tree, options: { format: 'markdown', embedImage: true } }, 'text');
    $('#report-text').textContent = md;
    $('#modal-report').hidden = false;
  } catch (e) {
    toast('生成失败: ' + e.message, 'err');
  } finally {
    btn.disabled = false;
    btn.textContent = '生成报告';
  }
});

$('#btn-export').addEventListener('click', async () => {
  try {
    const res = await fetch('/api/svg', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tree: state.tree, options: { heatmap: true } }),
    });
    const svg = await res.text();
    const blob = new Blob([svg], { type: 'image/svg+xml' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = (state.tree.meta.title || 'fault-tree') + '.svg';
    a.click();
    URL.revokeObjectURL(a.href);
    toast('SVG 已导出', 'ok');
  } catch (e) { toast('导出失败: ' + e.message, 'err'); }
});

// 关闭弹窗：按钮、遮罩点击、Esc 键三通道
function closeReport() {
  $('#modal-report').hidden = true;
  $('#report-text').textContent = '';
}
$$('[data-close]').forEach((b) => b.addEventListener('click', (e) => {
  e.preventDefault();
  closeReport();
}));
$('#modal-report').addEventListener('click', (e) => {
  if (e.target === $('#modal-report')) closeReport();
});
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && !$('#modal-report').hidden) closeReport();
});

function download(name, content, type) {
  const blob = new Blob([content], { type });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = name;
  a.click();
  URL.revokeObjectURL(a.href);
}
$('#btn-copy-md').addEventListener('click', async () => {
  try { await navigator.clipboard.writeText($('#report-text').textContent); toast('已复制到剪贴板', 'ok'); }
  catch { toast('复制失败，请手动选择文本', 'err'); }
});
$('#btn-dl-md').addEventListener('click', () => {
  const txt = $('#report-text').textContent;
  if (!txt) { toast('请先生成报告', 'err'); return; }
  download((state.tree.meta.title || 'fta') + '.md', txt, 'text/markdown');
});
$('#btn-dl-html').addEventListener('click', async () => {
  try {
    const html = await api('report', { tree: state.tree, options: { format: 'html' } }, 'text');
    download((state.tree.meta.title || 'fta') + '.html', html, 'text/html');
    toast('HTML 报告已下载', 'ok');
  } catch (e) { toast('导出失败: ' + e.message, 'err'); }
});

// ===== 启动 =====
fillTypeSelect();
state.tree = newTree();
bindMeta();
updateZoomLabel();
try { if (localStorage.getItem('fta.legend') === '0') setLegendVisible(false, false); } catch { /* ignore */ }
fitView();
renderProps();
renderOutline();

// 自动载入示例，展示真实效果
(async () => {
  try {
    const r = await (await fetch('/api/example/brake')).json();
    if (r.ok) {
      state.tree = r.tree;
      state.result = r.analysis;
      state.heatmap = r.analysis?.heatmap || {};
      bindMeta(); render(); renderProps(); renderOutline();
      if (r.analysis) { renderResults(r.analysis); renderCutSets(r.analysis); }
    }
  } catch { /* 静默失败，保留空树 */ }
  // 初始化结束：把当前状态当作唯一历史基线（此时「撤销」应为不可用）
  histReset();
})();