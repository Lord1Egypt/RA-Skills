/**
 * FTA Studio - 数据模型与紧凑文本 DSL 解析器
 *
 * 设计目标：让 AI（WorkBuddy）能用极简的缩进文本描述一棵故障树，
 * 同时保持与图形编辑器完全一致的结构化数据模型。
 */

// ============ 事件类型 ============
export const EVENT_TYPES = {
  TOP: 'top',                 // 顶事件
  INTER: 'intermediate',      // 中间事件
  BASIC: 'basic',             // 基本事件（底事件）
  UNDEV: 'undeveloped',       // 未开发事件
  HOUSE: 'house',             // 房屋事件（正常/非正常，TRUE/FALSE）
  CONDITION: 'condition',     // 条件事件
  EXTERNAL: 'external',       // 外部事件（系统外）
  TRANSFER_IN: 'transfer_in', // 传输符号（转入）
  TRANSFER_OUT: 'transfer_out', // 传输符号（转出）
  COMMENT: 'comment',         // 注释节点
};

export const EVENT_TYPE_LABEL = {
  top: '顶事件', intermediate: '中间事件', basic: '基本事件',
  undeveloped: '未开发事件', house: '房屋事件', condition: '条件事件',
  external: '外部事件', transfer_in: '传输转入', transfer_out: '传输转出',
  comment: '注释',
};

// 可以有子节点（作为逻辑门）的类型
export const GATEABLE = new Set(['top', 'intermediate', 'basic', 'undeveloped', 'external']);

// ============ 逻辑门类型 ============
export const GATE_TYPES = {
  AND: 'AND',       // 与门
  OR: 'OR',         // 或门
  XOR: 'XOR',       // 异或门
  VOTE: 'VOTE',     // k/n 表决门
  INHIBIT: 'INHIBIT', // 禁门（条件允许时传递）
  PAND: 'PAND',     // 优先与门（ordered）
  NOT: 'NOT',       // 非门（非相干树）
};

export const GATE_LABEL = {
  AND: '与门', OR: '或门', XOR: '异或门', VOTE: '表决门',
  INHIBIT: '禁门', PAND: '优先与门', NOT: '非门',
};

// 相干门（布尔代数可化简）
export const COHERENT_GATES = new Set(['AND', 'OR', 'VOTE', 'PAND']);

// ============ 概率模型 ============
export const PROB_MODELS = {
  FIXED: 'fixed',                 // 直接给定概率 q
  EXPONENTIAL: 'exponential',     // 指数分布 q = 1 - e^(-λt)
  WEIBULL: 'weibull',             // 威布尔 q = 1 - e^(-(t/η)^β)
  DEMAND: 'demand',               // 需求型 q = 需求次数 × 单次失效率
  POISSON: 'poisson',             // 泊松 q = 1 - e^(-λt) 成功率
  REPAIRABLE: 'repairable',       // 可修复（定期维修）q ≈ λ·TMR/(1+λ·TMR)
  MONITORED: 'monitored',         // 监控/定期测试 q ≈ 1 - e^(-λ·TI)
  BETA: 'beta',                   // β 因子共因
};

export const PROB_MODEL_LABEL = {
  fixed: '固定概率', exponential: '指数分布', weibull: '威布尔分布',
  demand: '需求型', poisson: '泊松（运行中失效）',
  repairable: '可修复', monitored: '周期监控', beta: 'β因子共因',
};

// ============ 图层/页面 ============
export function createEmptyTree(meta = {}) {
  return {
    version: '1.0',
    meta: {
      title: '未命名故障树',
      project: '',
      author: '',
      date: new Date().toISOString().slice(0, 10),
      standard: '',
      missionTime: null,      // 任务时间 t
      revision: 'A',
      description: '',
      ...meta,
    },
    settings: {
      missionTime: meta.missionTime ?? null,
      maxCutSetOrder: 0,       // 0 = 不限；否则只展开到 N 阶割集
      truncation: 1e-12,       // 概率截断阈值
      quantification: 'auto', // auto | rare | bdd | mcub
      houseTrueValue: 1,
    },
    nodes: [],
    connections: [],
  };
}

export function createNode(id, type, name = '', extra = {}) {
  return {
    id,
    type,
    name,
    gate: GATEABLE.has(type) ? 'OR' : null,
    voteK: 2,
    voteN: 2,
    description: '',
    ref: '',           // 追溯：FMEA/需求编号
    owner: '',
    component: '',     // 所属部件
    failureMode: '',   // 失效模式
    // 概率参数
    probModel: PROB_MODELS.FIXED,
    prob: null,        // fixed 模型下的概率
    lambda: null,      // 失效率 /h
    eta: null,         // 威布尔尺度
    beta: null,        // 威布尔形状
    demandCount: null, // 需求次数
    demandProb: null,  // 单次需求失效率
    repairTime: null,  // 平均修复时间 TMR
    monitorInterval: null, // 监控周期 TI
    // 显示
    x: null,
    y: null,
    collapsed: false,
    notes: '',
    ...extra,
  };
}

// ============ 图结构辅助 ============
export function buildIndex(tree) {
  const nodeMap = new Map();
  for (const n of tree.nodes) nodeMap.set(n.id, n);
  const childrenOf = new Map();
  const parentOf = new Map();
  for (const n of tree.nodes) {
    childrenOf.set(n.id, []);
    parentOf.set(n.id, []);
  }
  for (const c of tree.connections) {
    if (!nodeMap.has(c.from) || !nodeMap.has(c.to)) continue;
    childrenOf.get(c.from).push(c.to);
    parentOf.get(c.to).push(c.from);
  }
  const roots = tree.nodes
    .filter((n) => parentOf.get(n.id).length === 0)
    .map((n) => n.id);
  return { nodeMap, childrenOf, parentOf, roots };
}

export function findTopEvent(tree) {
  const tops = tree.nodes.filter((n) => n.type === 'top');
  if (tops.length) return tops[0].id;
  const { roots } = buildIndex(tree);
  return roots[0] ?? null;
}

// 查找所有 "叶子节点"（输入到门的基本事件）
export function collectLeaves(tree, nodeId, index) {
  const { childrenOf, nodeMap } = index;
  const leaves = [];
  const seen = new Set();
  const walk = (id) => {
    if (seen.has(id)) return; // 防环
    seen.add(id);
    const kids = childrenOf.get(id) || [];
    if (kids.length === 0) {
      const n = nodeMap.get(id);
      if (n) leaves.push(n);
      return;
    }
    kids.forEach(walk);
  };
  walk(nodeId);
  return leaves;
}

/** 展开子树（跳过被折叠的中间节点），返回可达的 basic 事件集合 */
export function reachableBasics(tree, rootId) {
  const { childrenOf, nodeMap } = buildIndex(tree);
  const out = new Set();
  const seen = new Set();
  const walk = (id) => {
    if (seen.has(id)) return;
    seen.add(id);
    const n = nodeMap.get(id);
    if (!n) return;
    if (n.type === 'basic' || n.type === 'undeveloped' || n.type === 'external') {
      out.add(id);
      return;
    }
    if (n.collapsed && id !== rootId) return;
    (childrenOf.get(id) || []).forEach(walk);
  };
  walk(rootId);
  return out;
}

// ============ 校验 ============
export function validateTree(tree) {
  const errors = [];
  const warnings = [];
  if (!tree || !Array.isArray(tree.nodes)) {
    errors.push('缺少 nodes 数组');
    return { errors, warnings, ok: false };
  }
  const ids = new Set();
  for (const n of tree.nodes) {
    if (!n.id) errors.push('存在无 id 节点');
    else if (ids.has(n.id)) errors.push(`节点 id 重复: ${n.id}`);
    ids.add(n.id);
    if (!EVENT_TYPES[n.type.toUpperCase?.() ?? n.type] && !Object.values(EVENT_TYPES).includes(n.type)) {
      errors.push(`节点 ${n.id} 类型非法: ${n.type}`);
    }
    if (!n.name || !String(n.name).trim()) {
      warnings.push(`节点 ${n.id} 名称为空`);
    }
    if (n.type === 'basic' && (n.prob == null || Number.isNaN(Number(n.prob)))) {
      warnings.push(`基本事件 ${n.id}(${n.name}) 未设置概率`);
    }
  }
  const topCount = tree.nodes.filter((n) => n.type === 'top').length;
  if (topCount === 0) errors.push('未定义顶事件 (top)');
  if (topCount > 1) warnings.push(`存在 ${topCount} 个顶事件，将以第一个为准进行计算`);

  for (const c of tree.connections) {
    if (!ids.has(c.from)) errors.push(`连接源不存在: ${c.from}`);
    if (!ids.has(c.to)) errors.push(`连接目标不存在: ${c.to}`);
  }
  // 环路检测
  const { childrenOf } = buildIndex(tree);
  const color = new Map();
  let cyclic = null;
  const dfs = (id, path) => {
    if (cyclic) return;
    if (color.get(id) === 1) { cyclic = [...path, id]; return; }
    if (color.get(id) === 2) return;
    color.set(id, 1);
    for (const k of childrenOf.get(id) || []) dfs(k, [...path, id]);
    color.set(id, 2);
  };
  for (const n of tree.nodes) dfs(n.id, []);
  if (cyclic) errors.push(`故障树存在环路: ${cyclic.join(' -> ')}`);

  return { errors, warnings, ok: errors.length === 0 };
}

// ============ DSL 解析器 ============
/**
 * 支持的语法（行首缩进表示层级，2 空格一级）：
 *
 *   # 注释行
 *   meta title: 车辆制动系统故障树
 *   meta missionTime: 10
 *
 *   TOP 制动系统无法建立制动力        desc=无法产生所需制动力
 *     AND
 *       OR 压力建立不良
 *         BASIC 制动泵失效 p=2e-2 ref=FMEA-001 comp=制动泵
 *         BASIC 主制动管路泄漏 p=5e-3
 *       BASIC 踏板行程不足 p=1e-3
 *     BASIC 制动液温度超限 p=1e-4
 *
 *   事件类型: TOP INTER BASIC UNDEV HOUSE COND EXT TIN TOUT
 *   门类型  : AND OR XOR VOTE INHIBIT PAND NOT
 *   VOTE 需指定: VOTE 2/3 任意两个失效
 *   属性    : key=value，p/prob 概率，lambda 失效率，ref/component/fm/desc/owner
 */
export function parseDSL(text) {
  const lines = String(text).replace(/\r\n/g, '\n').split('\n');
  const tree = createEmptyTree();
  const metas = [];
  const rootStack = []; // {indent, node}
  let topAssigned = false;

  const attrRe = /([A-Za-z_][A-Za-z0-9_]*)\s*=\s*("[^"]*"|'[^']*'|[^\s]+)/g;

  function parseAttrs(str) {
    const out = {};
    let m;
    const re = new RegExp(attrRe.source, 'g');
    while ((m = re.exec(str)) !== null) {
      let v = m[2];
      if (/^["'].*["']$/.test(v)) v = v.slice(1, -1);
      out[m[1].toLowerCase()] = v;
    }
    return out;
  }

  function num(v) {
    if (v == null) return null;
    const s = String(v).trim();
    const f = Number(s);
    if (!Number.isNaN(f)) return f;
    // 支持 2e-2, 1.5E-4 之外的写法：末尾 % 表示百分比
    if (s.endsWith('%')) {
      const p = Number(s.slice(0, -1));
      return Number.isNaN(p) ? null : p / 100;
    }
    return null;
  }

  let autoId = 0;
  const nextId = () => `N${String(++autoId).padStart(3, '0')}`;
  // 同名同类型事件复用（同一物理实体在树中出现多次时应共享概率与追溯信息）
  const registry = new Map();
  const keyOf = (type, name) => `${type}::${String(name).trim()}`;

  function upsertNode(type, name, attrs) {
    // 匿名结构节点（无名称）永不复用，保证每个门都有独立子树
    const nm = String(name ?? '').trim();
    const k = nm ? keyOf(type, nm) : null;
    if (k != null) {
      const existingId = registry.get(k);
      if (existingId != null) {
        const exist = tree.nodes.find((n) => n.id === existingId);
        if (exist) {
          applyAttrs(exist, attrs || {}, num);
          return exist;
        }
      }
    }
    const node = createNode(nextId(), type, name);
    applyAttrs(node, attrs || {}, num);
    tree.nodes.push(node);
    if (k != null) registry.set(k, node.id);
    return node;
  }

  for (let ln = 0; ln < lines.length; ln++) {
    const raw = lines[ln];
    if (!raw.trim() || raw.trim().startsWith('#')) continue;

    const indent = raw.match(/^\s*/)[0].replace(/\t/g, '  ').length;
    const content = raw.trim();

    // meta 行
    const mm = content.match(/^meta\s+([A-Za-z_][A-Za-z0-9_]*)\s*[:=]\s*(.*)$/);
    if (mm) {
      metas.push([mm[1], mm[2].trim()]);
      continue;
    }

    while (rootStack.length && rootStack[rootStack.length - 1].indent >= indent) {
      rootStack.pop();
    }
    const parent = rootStack.length ? rootStack[rootStack.length - 1] : null;

    // 分离 name 与属性
    const firstSpace = content.search(/\s/);
    let head = firstSpace === -1 ? content : content.slice(0, firstSpace);
    let rest = firstSpace === -1 ? '' : content.slice(firstSpace).trim();

    // 提取内联属性
    let attrs = {};
    const attrStart = rest.search(/\s[A-Za-z_][A-Za-z0-9_]*\s*=/);
    if (attrStart !== -1) {
      attrs = parseAttrs(rest.slice(attrStart));
      rest = rest.slice(0, attrStart).trim();
    }

    const upper = head.toUpperCase();

    // 门声明行：优先直接作用于父节点；父节点已有其他输入时才新建门容器
    const gateNames = Object.keys(GATE_TYPES);
    if (gateNames.includes(upper)) {
      let gtype = upper;
      let voteK = null, voteN = null;
      if (upper === 'VOTE') {
        const vm = rest.match(/^(\d+)\s*\/\s*(\d+)/);
        if (vm) { voteK = Number(vm[1]); voteN = Number(vm[2]); }
      }
      // 仅当父节点尚未设置门、且尚无任何子节点时，才把本门并入父节点。
      // 否则新建门容器，以正确表达 AND/OR 的同级嵌套结构
      // （例如 (A∨B)∧(A∨C) 需要两个平级的 OR 容器）。
      const parentHasKids = parent
        && tree.connections.some((c) => c.from === parent.node.id);
      const parentHasGate = parent && parent.node.__gateExplicit;
      if (parent && !parentHasKids && !parentHasGate) {
        parent.node.gate = gtype;
        parent.node.__gateExplicit = true;
        if (voteK != null) { parent.node.voteK = voteK; parent.node.voteN = voteN; }
        rootStack.push({ indent, node: parent.node });
        continue;
      }
      const gateNode = createNode(nextId(), EVENT_TYPES.INTER, '');
      gateNode.gate = gtype;
      gateNode.anon = true;
      gateNode.__gateExplicit = true;
      if (voteK != null) { gateNode.voteK = voteK; gateNode.voteN = voteN; }
      tree.nodes.push(gateNode);
      if (parent) {
        tree.connections.push({ from: parent.node.id, to: gateNode.id });
      }
      rootStack.push({ indent, node: gateNode });
      continue;
    }

    // 事件类型
    let etype = null;
    let name = head;
    const typeKeys = {
      TOP: EVENT_TYPES.TOP, INTER: EVENT_TYPES.INTER, INT: EVENT_TYPES.INTER,
      BASIC: EVENT_TYPES.BASIC, BASIC_: EVENT_TYPES.BASIC,
      UNDEV: EVENT_TYPES.UNDEV, UNDEVELOPED: EVENT_TYPES.UNDEV,
      HOUSE: EVENT_TYPES.HOUSE, COND: EVENT_TYPES.CONDITION, CONDITION: EVENT_TYPES.CONDITION,
      EXT: EVENT_TYPES.EXTERNAL, EXTERNAL: EVENT_TYPES.EXTERNAL,
      TIN: EVENT_TYPES.TRANSFER_IN, TOUT: EVENT_TYPES.TRANSFER_OUT,
      COMMENT: EVENT_TYPES.COMMENT,
    };
    if (typeKeys[upper]) {
      etype = typeKeys[upper];
      if (firstSpace === -1) {
        rest = '';
      } else {
        name = rest;
        // 名称里可能还带属性
        const as = name.search(/\s[A-Za-z_][A-Za-z0-9_]*\s*=/);
        if (as !== -1) {
          attrs = { ...parseAttrs(name.slice(as)), ...attrs };
          name = name.slice(0, as).trim();
        }
      }
    }

    if (!etype) {
      // 未标注类型：按上下文推断；有父节点则默认 basic，否则 top
      etype = parent ? EVENT_TYPES.BASIC : EVENT_TYPES.TOP;
      name = head;
    }

    const node = upsertNode(etype, name, attrs);
    if (etype === 'top') topAssigned = true;
    if (parent) {
      // 同一父节点下的重复输入（幂等）只建一次连接
      const dup = tree.connections.some(
        (c) => c.from === parent.node.id && c.to === node.id);
      if (!dup) tree.connections.push({ from: parent.node.id, to: node.id });
    }
    rootStack.push({ indent, node });
  }

  for (const [k, v] of metas) {
    if (k === 'missionTime' || k === 'mission') {
      tree.settings.missionTime = num(v);
      tree.meta.missionTime = num(v);
    } else if (['title', 'project', 'author', 'date', 'standard', 'revision', 'description'].includes(k)) {
      tree.meta[k] = v;
    }
  }
  if (!topAssigned) {
    errors: {
      // 没有 top 时，把第一个无父节点的事件提升为顶事件
      const { roots } = buildIndex(tree);
      if (roots.length && tree.nodes.length) {
        tree.nodes.find((n) => n.id === roots[0]).type = EVENT_TYPES.TOP;
      }
    }
  }
  return tree;
}

function applyAttrs(node, attrs, num) {
  // 记录显式指定的模型与特征，最后统一推断，避免属性顺序影响结果
  let explicitModel = null;
  const feats = new Set();
  for (const [k, v] of Object.entries(attrs || {})) {
    switch (k) {
      case 'p': case 'prob': case 'q':
        node.prob = num(v);
        feats.add('prob');
        break;
      case 'lambda': case 'lam': case 'l':
        node.lambda = num(v);
        feats.add('lambda');
        break;
      case 'eta': node.eta = num(v); feats.add('eta'); break;
      case 'beta': case 'shape':
        node.beta = num(v); feats.add('beta'); break;
      case 'demands': case 'n':
        node.demandCount = num(v); feats.add('demandCount'); break;
      case 'dp': case 'demandprob':
        node.demandProb = num(v); feats.add('demandProb'); break;
      case 'tmr': case 'repairtime':
        node.repairTime = num(v); feats.add('repairTime'); break;
      case 'ti': case 'monitorinterval':
        node.monitorInterval = num(v); feats.add('monitorInterval'); break;
      case 'model':
        explicitModel = String(v).toLowerCase();
        break;
      case 'ref': node.ref = v; break;
      case 'comp': case 'component': node.component = v; break;
      case 'fm': case 'failuremode': node.failureMode = v; break;
      case 'owner': node.owner = v; break;
      case 'desc': case 'description': node.description = v; break;
      case 'notes': node.notes = v; break;
      default: break;
    }
  }
  if (explicitModel) {
    node.probModel = explicitModel;
    return;
  }
  // 按已提供的特征推断最合适的概率模型（属性书写顺序不影响结果）
  if (feats.has('repairTime')) node.probModel = PROB_MODELS.REPAIRABLE;
  else if (feats.has('monitorInterval')) node.probModel = PROB_MODELS.MONITORED;
  else if (feats.has('demandCount') || feats.has('demandProb')) node.probModel = PROB_MODELS.DEMAND;
  else if (feats.has('beta') || feats.has('eta')) node.probModel = PROB_MODELS.WEIBULL;
  else if (feats.has('lambda')) node.probModel = PROB_MODELS.EXPONENTIAL;
  else if (feats.has('prob')) node.probModel = PROB_MODELS.FIXED;
}

// ============ DSL 序列化 ============
/**
 * 序列化为紧凑 DSL。
 *
 * 关键：门与事件的输出必须严格配对 ——
 *   EVENT            <- 承载门符号的事件
 *     GATE           <- 缩进一级
 *       CHILD...     <- 缩进两级
 * 若事件无门（如孤立基本事件），直接输出事件行即可。
 * 匿名中间节点（anon=true）仅承载门，输出为空的 INTER 行以保留结构。
 */
export function stringifyDSL(tree) {
  const { nodeMap, childrenOf, parentOf } = buildIndex(tree);
  const rootId = findTopEvent(tree);
  const out = [];
  out.push(`meta title: ${tree.meta.title}`);
  if (tree.meta.project) out.push(`meta project: ${tree.meta.project}`);
  if (tree.meta.standard) out.push(`meta standard: ${tree.meta.standard}`);
  if (tree.settings.missionTime != null) out.push(`meta missionTime: ${tree.settings.missionTime}`);

  const typeKey = {
    top: 'TOP', intermediate: 'INTER', basic: 'BASIC', undeveloped: 'UNDEV',
    house: 'HOUSE', condition: 'COND', external: 'EXT',
    transfer_in: 'TIN', transfer_out: 'TOUT', comment: 'COMMENT',
  };

  const emitted = new Set();

  const emitAttrs = (n) => {
    const attrs = [];
    if (n.prob != null && (n.probModel || 'fixed') === 'fixed') attrs.push(`p=${fmtNum(n.prob)}`);
    else if (n.lambda != null) attrs.push(`lambda=${fmtNum(n.lambda)}`);
    if (n.demandCount != null) attrs.push(`n=${n.demandCount}`);
    if (n.repairTime != null) attrs.push(`tmr=${n.repairTime}`);
    if (n.monitorInterval != null) attrs.push(`ti=${n.monitorInterval}`);
    if (n.beta != null && (n.probModel === 'weibull')) attrs.push(`beta=${n.beta}`);
    if (n.ref) attrs.push(`ref=${n.ref}`);
    if (n.component) attrs.push(`comp=${n.component}`);
    if (n.failureMode) attrs.push(`fm=${n.failureMode}`);
    if (n.description) attrs.push(`desc="${String(n.description).replace(/"/g, "'")}"`);
    return attrs.length ? ' ' + attrs.join(' ') : '';
  };

  const emitNode = (id, depth) => {
    if (emitted.has(id)) return;
    emitted.add(id);
    const n = nodeMap.get(id);
    if (!n) return;
    const pad = '  '.repeat(depth);
    const key = typeKey[n.type] || 'INTER';
    const kids = childrenOf.get(id) || [];
    const hasGate = kids.length > 0 && n.gate;

    if (!kids.length) {
      // 叶子：事件行 + 属性（门无意义）
      out.push(`${pad}${key} ${n.name || ''}${emitAttrs(n)}`.trimEnd());
      return;
    }
    // 非叶子：先输出事件行，再输出门行
    out.push(`${pad}${key} ${n.name || ''}${emitAttrs(n)}`.trimEnd());
    const gateStr = n.gate === 'VOTE' ? `${n.gate} ${n.voteK}/${n.voteN}` : n.gate;
    out.push(`${pad}  ${gateStr}`);
    for (const k of kids) emitNode(k, depth + 2);
  };

  if (rootId) emitNode(rootId, 0);
  // 输出未连通的分量（如传输符号转入），避免丢数据
  for (const n of tree.nodes) {
    if (!emitted.has(n.id) && (parentOf.get(n.id) || []).length === 0) {
      emitNode(n.id, 0);
    }
  }
  return out.join('\n');
}

export function fmtNum(x, digits = 6) {
  if (x == null || Number.isNaN(x)) return '-';
  const v = Number(x);
  if (v === 0) return '0';
  if (Math.abs(v) < 1e-4 || Math.abs(v) >= 1e6) return v.toExponential(3);
  return String(Number(v.toFixed(digits)));
}