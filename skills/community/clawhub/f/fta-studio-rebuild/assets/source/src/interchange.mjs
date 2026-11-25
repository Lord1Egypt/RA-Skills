/**
 * FTA Studio - 第三方格式互操作
 *
 * Ansys medini analyze 的 FTA 交换格式（据 Ansys 官方文档 "Integration with FaultTree+"）：
 *   - 原生导入/导出格式 = Isograph FaultTree+ 结构 XML（双向）
 *   - 亦可导入 CAFTA
 *   - medini 自身工程包（.medini / Eclipse 工程）为专有格式，脱离 medini 无法生成
 *
 * 因此：
 *   medini 可打开本工具导出的文件  ⇐  导出「原生 FaultTree+ XML」
 *   本工具可打开 medini 的文件      ⇐  导入「原生 FaultTree+ XML」
 *
 * ────────────────────────────────────────────────────────────────
 *  原生 FaultTree+ XML 是「表格」结构，导出时勾选 4 张表：
 *    1. Failure Models  —— 每个基本事件/未开发事件的失效模型
 *    2. Gates           —— 所有逻辑门（含顶事件门）
 *    3. Primary Events  —— 所有底事件
 *    4. Gate Inputs     —— 门的输入连线（含次序）
 *  （表名/字段名集中定义在 FT_SCHEMA 中，若日后拿到真实样本需校准，改这里即可。）
 * ────────────────────────────────────────────────────────────────
 */

import { parseDSL, validateTree, buildIndex, findTopEvent, createNode, EVENT_TYPES } from './model.mjs';

// =====================================================================
//  FaultTree+ 原生格式 字段/类型映射（单一校准点）
// =====================================================================
export const FT_SCHEMA = {
  ns: 'http://www.isograph.com/FaultTreePlus',
  version: '13.0',
  root: 'FaultTreePlus',
  tables: { models: 'FailureModels', gates: 'Gates', events: 'PrimaryEvents', inputs: 'GateInputs' },
  rows: { model: 'FailureModel', gate: 'Gate', event: 'PrimaryEvent', input: 'GateInput' },

  // 内部逻辑门 -> FaultTree+ 门类型
  gateToFt: {
    OR: 'OR', AND: 'AND', XOR: 'EXCLUSIVE_OR', VOTE: 'VOTING',
    INHIBIT: 'INHIBIT', PAND: 'PRIORITY_AND', NOT: 'NOT',
  },
  // FaultTree+ 门类型 -> 内部逻辑门（兼容多种别名/大小写）
  gateFromFt: {
    OR: 'OR', AND: 'AND', XOR: 'XOR', EXCLUSIVE_OR: 'XOR', EXOR: 'XOR',
    VOTING: 'VOTE', VOTE: 'VOTE', 'K/N': 'VOTE', KOFN: 'VOTE', 'K_OF_N': 'VOTE',
    INHIBIT: 'INHIBIT', INHIBITING: 'INHIBIT',
    PRIORITY_AND: 'PAND', PAND: 'PAND', NOT: 'NOT',
  },

  // 内部事件类型 -> FaultTree+ 事件类型
  eventToFt: {
    top: 'Top', intermediate: 'Intermediate', basic: 'Basic',
    undeveloped: 'Undeveloped', house: 'House', condition: 'Conditioning',
    external: 'External', transfer_in: 'TransferIn', transfer_out: 'TransferOut', comment: 'Comment',
  },
  // FaultTree+ 事件类型 -> 内部事件类型
  eventFromFt: {
    TOP: 'top', TOPEVENT: 'top',
    INTERMEDIATE: 'intermediate', GATE: 'intermediate',
    BASIC: 'basic', PRIMARY: 'basic', PRIMARYEVENT: 'basic',
    UNDEVELOPED: 'undeveloped', UNDEV: 'undeveloped',
    HOUSE: 'house', CONDITIONING: 'condition', CONDITION: 'condition',
    EXTERNAL: 'external',
    TRANSFERIN: 'transfer_in', TRANSFEROUT: 'transfer_out', TRANSFER: 'transfer_in',
    COMMENT: 'comment',
  },

  // 内部概率模型 -> FaultTree+ 失效模型类型
  modelToFt: {
    fixed: 'Fixed', exponential: 'Exponential', weibull: 'Weibull',
    demand: 'Demand', repairable: 'Repairable', monitored: 'Monitored',
    poisson: 'Exponential', beta: 'Fixed',
  },
};

const norm = (s) => String(s || '').trim().toUpperCase().replace(/[\s-]+/g, '_');

function gateToFt(g) { return FT_SCHEMA.gateToFt[String(g || '').toUpperCase()] || 'OR'; }
function gateFromFt(g) {
  const k = norm(g);
  return FT_SCHEMA.gateFromFt[k] || FT_SCHEMA.gateFromFt[k.replace(/_/g, '')] || 'OR';
}
function eventTypeToFt(t) { return FT_SCHEMA.eventToFt[t] || 'Basic'; }
function eventTypeFromFt(t, fallback = 'basic') {
  const k = norm(t).replace(/_/g, '');
  return FT_SCHEMA.eventFromFt[k] || fallback;
}

/** 计算某节点在任务时间 t 下的等效不可用度 q（用于写出 FaultTree+ 可读的数值列） */
export function effectiveQ(n, t = 1) {
  const m = n.probModel || 'fixed';
  switch (m) {
    case 'exponential':
    case 'poisson':
      return n.lambda != null ? 1 - Math.exp(-n.lambda * t) : (n.prob ?? null);
    case 'weibull':
      return (n.eta != null && n.beta != null) ? 1 - Math.exp(-Math.pow(t / n.eta, n.beta)) : (n.prob ?? null);
    case 'demand':
      return (n.demandCount != null && n.demandProb != null)
        ? Math.min(1, n.demandCount * n.demandProb) : (n.prob ?? null);
    case 'repairable':
      return (n.lambda != null && n.repairTime != null)
        ? (n.lambda * n.repairTime) / (1 + n.lambda * n.repairTime) : (n.prob ?? null);
    case 'monitored':
      return (n.lambda != null && n.monitorInterval != null)
        ? 1 - Math.exp(-n.lambda * n.monitorInterval) : (n.prob ?? null);
    default:
      return n.prob ?? null;
  }
}

// =====================================================================
//  导出：内部模型 -> 原生 FaultTree+ XML（medini 可直接导入）
// =====================================================================

/**
 * @param {object} tree 内部模型
 * @param {object} opts { pag } 分页结果（可选，用于注入跨页传输符号）
 */
export function toFaultTreePlusXML(tree, opts = {}) {
  let model = tree;
  if (opts.pag && opts.pag.pages && opts.pag.pages.length > 1) {
    model = injectTransferMarkers(tree, opts.pag);
  }

  const { childrenOf } = buildIndex(model);
  const topId = findTopEvent(model);
  const missionTime = model.settings?.missionTime ?? model.meta?.missionTime ?? null;
  const S = FT_SCHEMA;

  const esc = xmlEsc;
  const L = [];
  L.push('<?xml version="1.0" encoding="UTF-8"?>');
  L.push('<!-- FTA Studio -> Isograph FaultTree+ (native) XML. Import in Ansys medini analyze via:' +
    ' new empty FTA model -> right click -> Import from FT+ (or "Import from Isograph FaultTree+"). -->');
  L.push(`<${S.root} xmlns="${S.ns}" Version="${S.version}"` +
    ` Name="${esc(model.meta?.title || 'FaultTree')}"` +
    ` Project="${esc(model.meta?.project || '')}"` +
    ` Standard="${esc(model.meta?.standard || '')}"` +
    (missionTime != null ? ` MissionTime="${missionTime}"` : '') +
    (topId ? ` TopEvent="${esc(topId)}"` : '') + '>');

  const isGate = (id) => (childrenOf.get(id) || []).length > 0;
  const gates = model.nodes.filter((n) => isGate(n.id));
  const events = model.nodes.filter((n) => !isGate(n.id));

  // ---- 表 1: Failure Models ----
  L.push(`  <${S.tables.models}>`);
  for (const n of events) {
    if (!needsFailureModel(n)) continue;
    L.push(modelLine(n, missionTime, esc));
  }
  L.push(`  </${S.tables.models}>`);

  // ---- 表 2: Primary Events ----
  L.push(`  <${S.tables.events}>`);
  for (const n of events) {
    const attrs = [
      `Name="${esc(n.id)}"`,
      `Label="${esc(n.name || '')}"`,
      `EventType="${eventTypeToFt(n.type)}"`,
    ];
    if (needsFailureModel(n)) attrs.push(`FailureModel="${esc(fmName(n.id))}"`);
    if (n.description) attrs.push(`Description="${esc(n.description)}"`);
    if (n.component) attrs.push(`Component="${esc(n.component)}"`);
    if (n.failureMode) attrs.push(`FailureMode="${esc(n.failureMode)}"`);
    if (n.ref) attrs.push(`Trace="${esc(n.ref)}"`);
    if (n.owner) attrs.push(`Owner="${esc(n.owner)}"`);
    if (n.type === 'house') attrs.push(`HouseValue="${n.prob ?? 1}"`);
    if (n.notes) attrs.push(`Notes="${esc(n.notes)}"`);
    L.push(`    <${S.rows.event} ${attrs.join(' ')}/>`);
  }
  L.push(`  </${S.tables.events}>`);

  // ---- 表 3: Gates ----
  L.push(`  <${S.tables.gates}>`);
  for (const n of gates) {
    const attrs = [
      `Name="${esc(n.id)}"`,
      `Label="${esc(n.name || '')}"`,
      `Type="${gateToFt(n.gate)}"`,
      `EventType="${eventTypeToFt(n.type)}"`,
    ];
    if (n.gate === 'VOTE') { attrs.push(`K="${n.voteK ?? 2}"`, `N="${n.voteN ?? 2}"`); }
    if (n.description) attrs.push(`Description="${esc(n.description)}"`);
    if (n.ref) attrs.push(`Trace="${esc(n.ref)}"`);
    L.push(`    <${S.rows.gate} ${attrs.join(' ')}/>`);
  }
  L.push(`  </${S.tables.gates}>`);

  // ---- 表 4: Gate Inputs ----
  L.push(`  <${S.tables.inputs}>`);
  for (const n of gates) {
    const kids = childrenOf.get(n.id) || [];
    kids.forEach((k, i) => {
      L.push(`    <${S.rows.input} Gate="${esc(n.id)}" Input="${esc(k)}" Order="${i + 1}"/>`);
    });
  }
  L.push(`  </${S.tables.inputs}>`);

  L.push(`</${S.root}>`);
  return L.join('\n') + '\n';
}

function needsFailureModel(n) {
  return n.prob != null || n.lambda != null || n.eta != null
    || n.demandCount != null || n.repairTime != null || n.monitorInterval != null;
}
function fmName(id) { return `FM_${id}`; }

/** 生成一行 <FailureModel>，既含 medini 可读的 Type/Value，也含内部精确参数（Model/…） */
function modelLine(n, t, esc) {
  const S = FT_SCHEMA;
  const type = S.modelToFt[n.probModel || 'fixed'] || 'Fixed';
  const q = effectiveQ(n, t ?? 1);
  const a = [`Name="${esc(fmName(n.id))}"`, `Type="${type}"`, `Model="${esc(n.probModel || 'fixed')}"`];
  if (q != null) { a.push(`Value="${num(q)}"`, `Unavailability="${num(q)}"`); }
  if (n.prob != null) a.push(`Probability="${num(n.prob)}"`);
  if (n.lambda != null) a.push(`FailureRate="${num(n.lambda)}"`);
  if (n.beta != null) a.push(`Shape="${num(n.beta)}"`, `Beta="${num(n.beta)}"`);
  if (n.eta != null) a.push(`Scale="${num(n.eta)}"`, `Eta="${num(n.eta)}"`);
  if (n.demandCount != null) a.push(`DemandCount="${num(n.demandCount)}"`);
  if (n.demandProb != null) a.push(`DemandProbability="${num(n.demandProb)}"`);
  if (n.repairTime != null) a.push(`RepairTime="${num(n.repairTime)}"`);
  if (n.monitorInterval != null) a.push(`MonitorInterval="${num(n.monitorInterval)}"`);
  return `    <${S.rows.model} ${a.join(' ')}/>`;
}

// =====================================================================
//  导入：原生 FaultTree+ XML -> 内部模型
// =====================================================================

export function fromFaultTreePlusXML(xml) {
  const raw = String(xml ?? '');
  // 兼容旧版自定义格式（<FaultTree><Events>…），保证历史文件仍可读回
  if (/<\s*(?:\w+:)?Events\b/i.test(raw) && !/<\s*(?:\w+:)?(GateInputs|PrimaryEvents|Gates)\b/i.test(raw)) {
    return fromFaultTreePlusLegacy(raw);
  }

  const clean = stripNs(String(raw)
    .replace(/<\?xml[^>]*\?>/g, '')
    .replace(/<!--[\s\S]*?-->/g, ''));

  const S = FT_SCHEMA;
  const rootM = clean.match(new RegExp(`<${S.root}\\b([^>]*)>`, 'i'));
  const rootAttrs = rootM ? parseAttrs(rootM[1]) : {};

  const tree = {
    version: '1.0',
    meta: {
      title: pick(rootAttrs, 'Name', 'Title', 'Description') || 'Imported FaultTree',
      project: pick(rootAttrs, 'Project') || '',
      author: pick(rootAttrs, 'Author') || '',
      date: new Date().toISOString().slice(0, 10),
      standard: pick(rootAttrs, 'Standard') || 'Isograph FaultTree+',
      missionTime: numOrNull(pick(rootAttrs, 'MissionTime', 'Mission')),
      revision: pick(rootAttrs, 'Revision') || 'A',
      description: '',
    },
    settings: {
      missionTime: numOrNull(pick(rootAttrs, 'MissionTime', 'Mission')),
      maxCutSetOrder: 0, truncation: 1e-12, quantification: 'auto',
    },
    nodes: [],
    connections: [],
  };

  const idMap = new Map();      // FT Name -> 内部 id
  const used = new Set();
  const ensureId = (name) => {
    const nm = String(name ?? '').trim();
    if (nm && !used.has(nm)) { used.add(nm); idMap.set(nm, nm); return nm; }
    let i = tree.nodes.length + 1;
    let id;
    do { id = `I${String(i++).padStart(3, '0')}`; } while (used.has(id));
    used.add(id);
    if (nm) idMap.set(nm, id);
    return id;
  };
  const nodeById = (id) => tree.nodes.find((n) => n.id === id);

  // ---- 失效模型表 ----
  const models = new Map();
  for (const { attrs, body } of rows(clean, S.tables.models, S.rows.model)) {
    const name = pick(attrs, 'Name', 'Id', 'Identifier');
    if (!name) continue;
    models.set(name, readModel(attrs, body));
  }

  // ---- 门表 ----
  for (const { attrs, body } of rows(clean, S.tables.gates, S.rows.gate)) {
    const name = pick(attrs, 'Name', 'Id', 'Identifier');
    const id = ensureId(name);
    const n = blankNode(id);
    n.name = pick(attrs, 'Label', 'Description', 'Text', 'Title') || childText(body, 'Description', 'Label', 'Text') || '';
    n.gate = gateFromFt(pick(attrs, 'Type', 'GateType', 'Logic', 'Gate'));
    const et = pick(attrs, 'EventType', 'Event', 'Type2');
    n.type = et ? eventTypeFromFt(et, 'intermediate') : 'intermediate';
    if (/^(voting|vote|k.?of.?n)$/i.test(String(pick(attrs, 'Type', 'GateType') || ''))) {
      n.voteK = numOrNull(pick(attrs, 'K', 'VoteK')) ?? 2;
      n.voteN = numOrNull(pick(attrs, 'N', 'VoteN')) ?? 2;
    }
    n.description = pick(attrs, 'Description') || childText(body, 'Description') || '';
    n.ref = pick(attrs, 'Trace', 'Traceability', 'FMEA', 'Ref') || '';
    n._isGate = true;
    tree.nodes.push(n);
  }

  // ---- 底事件表 ----
  for (const { attrs, body } of rows(clean, S.tables.events, S.rows.event)) {
    const name = pick(attrs, 'Name', 'Id', 'Identifier');
    const id = ensureId(name);
    const n = blankNode(id);
    n.name = pick(attrs, 'Label', 'Description', 'Text', 'Title') || childText(body, 'Description', 'Label', 'Text') || '';
    const et = pick(attrs, 'EventType', 'Event', 'Type');
    n.type = et ? eventTypeFromFt(et, 'basic') : 'basic';
    n.component = pick(attrs, 'Component', 'System') || childText(body, 'Component') || '';
    n.failureMode = pick(attrs, 'FailureMode', 'Mode') || childText(body, 'FailureMode') || '';
    n.ref = pick(attrs, 'Trace', 'Traceability', 'FMEA', 'Ref') || '';
    n.owner = pick(attrs, 'Owner') || '';
    n.description = pick(attrs, 'Description') || childText(body, 'Description') || '';
    n.notes = pick(attrs, 'Notes') || '';
    if (n.type === 'house') {
      const hv = numOrNull(pick(attrs, 'HouseValue', 'House'));
      n.prob = hv ?? 1; n.probModel = 'fixed';
    }
    // 关联失效模型
    const fmRef = pick(attrs, 'FailureModel', 'Model', 'FailureModelName');
    const inline = pick(attrs, 'Value', 'Unavailability', 'Probability', 'FailureRate', 'ModelType');
    if (fmRef && models.has(fmRef)) applyModel(n, models.get(fmRef));
    else if (inline) applyModel(n, readModel(attrs, body));
    tree.nodes.push(n);
  }

  // ---- 门输入表（连线） ----
  for (const { attrs } of rows(clean, S.tables.inputs, S.rows.input)) {
    const g = pick(attrs, 'Gate', 'From', 'Parent', 'Output');
    const i = pick(attrs, 'Input', 'Event', 'Child', 'To');
    const from = idMap.get(g) || (used.has(g) ? g : null);
    const to = idMap.get(i) || (used.has(i) ? i : null);
    if (!from || !to) continue;
    if (!tree.connections.some((c) => c.from === from && c.to === to)) {
      tree.connections.push({ from, to });
    }
  }

  // 无显式输入表时，退化为按 Parent 属性恢复连线
  if (!tree.connections.length) {
    for (const n of tree.nodes) {
      if (n._parent && idMap.get(n._parent)) tree.connections.push({ from: idMap.get(n._parent), to: n.id });
    }
  }

  // ---- 确定顶事件 ----
  const hasChild = new Set(tree.connections.map((c) => c.from));
  const isChild = new Set(tree.connections.map((c) => c.to));
  for (const n of tree.nodes) {
    if (n._isGate) n.type = hasChild.has(n.id) ? 'intermediate' : 'basic';
  }
  const explicitTop = pick(rootAttrs, 'TopEvent', 'Top', 'RootEvent');
  const rootIds = tree.nodes.filter((n) => n._isGate && !isChild.has(n.id)).map((n) => n.id);
  const topId = (explicitTop && (idMap.get(explicitTop) || explicitTop)) || rootIds[0] || null;
  if (topId) {
    const t = nodeById(topId);
    if (t) t.type = 'top';
  }
  for (const n of tree.nodes) delete n._isGate;
  for (const n of tree.nodes) delete n._parent;

  return tree;
}

// =====================================================================
//  旧版自定义 FaultTree+ 结构（回退解析，仅供历史文件）
// =====================================================================

function fromFaultTreePlusLegacy(xml) {
  const clean = String(xml).replace(/<\?xml[^>]*\?>/g, '');
  const tree = {
    version: '1.0',
    meta: {
      title: clean.match(/<FaultTree[^>]*Name="([^"]*)"/)?.[1] || 'Imported FaultTree',
      project: '', author: '', date: new Date().toISOString().slice(0, 10),
      standard: 'Isograph FaultTree+ (legacy)', missionTime: null, revision: 'A', description: '',
    },
    settings: { missionTime: null, maxCutSetOrder: 0, truncation: 1e-12, quantification: 'auto' },
    nodes: [], connections: [],
  };
  const idMap = new Map();
  const eventRe = /<Event\s+([^>]*?)(?:\/>|>([\s\S]*?)<\/Event>)/g;
  let m;
  const events = [];
  while ((m = eventRe.exec(clean)) !== null) events.push({ attrs: parseAttrs(m[1]), body: m[2] || '' });
  for (const { attrs, body } of events) {
    const oldId = attrs.Id;
    if (!oldId) continue;
    const newId = `I${String(tree.nodes.length + 1).padStart(3, '0')}`;
    idMap.set(oldId, newId);
    const node = blankNode(newId);
    node.type = eventTypeFromFt(attrs.Type, 'intermediate');
    node.name = attrs.Name || '';
    node.gate = attrs.Gate ? gateFromFt(attrs.Gate) : null;
    node.description = body.match(/<Description>([\s\S]*?)<\/Description>/)?.[1] || '';
    node.ref = body.match(/<Trace[^>]*Id="([^"]*)"/)?.[1] || '';
    node.component = body.match(/<Attribute[^>]*Name="Component"[^>]*>([^<]*)<\/Attribute>/)?.[1] || '';
    node.failureMode = body.match(/<Attribute[^>]*Name="FailureMode"[^>]*>([^<]*)<\/Attribute>/)?.[1] || '';
    const p = body.match(/<Probability\s+Value="([^"]*)"/);
    if (p) { node.prob = Number(p[1]); node.probModel = 'fixed'; }
    const lr = body.match(/<FailureRate\s+Value="([^"]*)"/);
    if (lr) node.lambda = Number(lr[1]);
    tree.nodes.push(node);
  }
  const connRe = /<Connection\s+From="([^"]*)"\s+Gate="([^"]*)"\s*>([\s\S]*?)<\/Connection>/g;
  while ((m = connRe.exec(clean)) !== null) {
    const fromId = idMap.get(m[1]);
    if (!fromId) continue;
    const fromNode = tree.nodes.find((n) => n.id === fromId);
    if (fromNode) fromNode.gate = gateFromFt(m[2]);
    const inputRe = /<Input\s+Event="([^"]*)"/g;
    let im;
    while ((im = inputRe.exec(m[3] || '')) !== null) {
      const toId = idMap.get(im[1]);
      if (toId) tree.connections.push({ from: fromId, to: toId });
    }
  }
  const topOld = clean.match(/<TopEvent\s+Event="([^"]*)"/)?.[1];
  if (topOld && idMap.has(topOld)) {
    const t = tree.nodes.find((n) => n.id === idMap.get(topOld));
    if (t) t.type = 'top';
  }
  return tree;
}

// =====================================================================
//  CAFTA
// =====================================================================

export function toCAFTA(tree) {
  const { nodeMap, childrenOf } = buildIndex(tree);
  const topId = findTopEvent(tree);
  const esc = (s) => String(s ?? '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

  const { parentOf } = buildIndex(tree);
  const depthCache = new Map();
  const depthOf = (id) => {
    if (depthCache.has(id)) return depthCache.get(id);
    const ps = parentOf.get(id) || [];
    const d = ps.length ? depthOf(ps[0]) + 1 : 0;
    depthCache.set(id, d);
    return d;
  };

  const lines = [];
  const emitted = new Set();
  const emitGate = (id, depth) => {
    const n = nodeMap.get(id);
    if (!n || emitted.has(id)) return;
    emitted.add(id);
    const kids = (childrenOf.get(id) || []).filter((k) => !emitted.has(k));
    if (!kids.length) return;
    const gate = (n.gate || 'OR').toLowerCase();
    const pad = '  '.repeat(depth + 3);
    lines.push(`${pad}<gate-occurrence name="${esc(id)}" gate="${gate}">`);
    for (const k of kids) {
      if ((childrenOf.get(k) || []).length === 0) lines.push(`${pad}  <basic-event name="${esc(k)}"/>`);
      else emitGate(k, depth + 1);
    }
    lines.push(`${pad}</gate-occurrence>`);
  };

  lines.push('<?xml version="1.0" encoding="UTF-8"?>');
  lines.push('<!-- CAFTA format — importable by Ansys medini analyze -->');
  lines.push('<model>');
  lines.push('  <define-fault-tree name="' + esc(tree.meta?.title || 'FaultTree') + '">');
  lines.push('    <define-gate name="' + esc(topId || 'TOP') + '" type="top" logic="' +
    ((nodeMap.get(topId)?.gate || 'OR')).toLowerCase() + '">');

  const topNode = nodeMap.get(topId);
  const topGate = (topNode?.gate || 'OR').toLowerCase();
  const topPad = '      ';
  const topKids = childrenOf.get(topId) || [];
  lines.push(`${topPad}<gate-occurrence name="${esc(topId)}" gate="${topGate}">`);
  for (const k of topKids) {
    if ((childrenOf.get(k) || []).length === 0) lines.push(`${topPad}  <basic-event name="${esc(k)}"/>`);
  }
  lines.push(`${topPad}</gate-occurrence>`);
  for (const k of topKids) {
    if ((childrenOf.get(k) || []).length > 0) emitGate(k, depthOf(k));
  }
  lines.push('    </define-gate>');

  for (const n of tree.nodes) {
    if ((childrenOf.get(n.id) || []).length > 0) continue;
    if (n.prob == null && n.lambda == null) continue;
    lines.push(`    <define-basic-event name="${esc(n.id)}" description="${esc(n.name || '')}">`);
    if (n.prob != null) lines.push(`      <float value="${n.prob}"/>`);
    else if (n.lambda != null) {
      const t = tree.settings?.missionTime ?? tree.meta?.missionTime ?? 1;
      lines.push(`      <float value="${1 - Math.exp(-n.lambda * t)}"/>`);
    }
    lines.push('    </define-basic-event>');
  }
  lines.push('  </define-fault-tree>');
  lines.push('</model>');
  return lines.join('\n');
}

export function fromCAFTA(xml) {
  const clean = String(xml).replace(/<\?xml[^>]*\?>/g, '');
  const tree = {
    version: '1.0',
    meta: {
      title: clean.match(/<define-fault-tree[^>]*name="([^"]*)"/)?.[1] || 'Imported CAFTA',
      project: 'CAFTA Import', author: '', date: new Date().toISOString().slice(0, 10),
      standard: 'CAFTA', missionTime: null, revision: 'A', description: '',
    },
    settings: { missionTime: null, maxCutSetOrder: 0, truncation: 1e-12, quantification: 'auto' },
    nodes: [], connections: [],
  };
  const byName = new Map();
  const newId = () => `C${String(tree.nodes.length + 1).padStart(3, '0')}`;
  const mkNode = (name, type, gate) => {
    if (byName.has(name)) {
      const ex = tree.nodes.find((n) => n.id === byName.get(name));
      if (gate && !ex.gate) ex.gate = gate;
      return ex.id;
    }
    const id = newId();
    const n = blankNode(id);
    n.type = type; n.name = name; n.gate = gate || null;
    tree.nodes.push(n); byName.set(name, id);
    return id;
  };

  const topName = clean.match(/<define-gate[^>]*name="([^"]*)"/)?.[1] || 'TOP';
  const topLogic = clean.match(/<define-gate[^>]*logic="([^"]*)"/)?.[1] || 'or';
  const topId = mkNode(topName, 'top', topLogic.toUpperCase());

  const beRe = /<define-basic-event[^>]*name="([^"]*)"[^>]*(?:description="([^"]*)")?[^>]*>([\s\S]*?)<\/define-basic-event>/g;
  let m;
  while ((m = beRe.exec(clean)) !== null) {
    const id = mkNode(m[1], 'basic', null);
    const n = tree.nodes.find((x) => x.id === id);
    if (m[2]) n.name = m[2];
    const fv = (m[3] || '').match(/<float value="([^"]*)"/);
    if (fv) { n.prob = Number(fv[1]); n.probModel = 'fixed'; }
  }

  const lines = clean.split('\n');
  const stack = [];
  const ind = (s) => (s.match(/^\s*/)[0] || '').length;
  for (const raw of lines) {
    const goOpen = raw.match(/^\s*<gate-occurrence[^>]*name="([^"]*)"[^>]*gate="([^"]*)"[^>]*>\s*$/);
    if (goOpen) {
      const depth = ind(raw);
      while (stack.length && stack[stack.length - 1].indent >= depth) stack.pop();
      const parentId = stack.length ? stack[stack.length - 1].id : topId;
      const id = mkNode(goOpen[1], 'intermediate', (goOpen[2] || 'or').toUpperCase());
      if (id !== parentId) tree.connections.push({ from: parentId, to: id });
      stack.push({ indent: depth, id });
      continue;
    }
    const be = raw.match(/^\s*<basic-event[^>]*name="([^"]*)"/);
    if (be) {
      const depth = ind(raw);
      while (stack.length && stack[stack.length - 1].indent >= depth) stack.pop();
      const parentId = stack.length ? stack[stack.length - 1].id : topId;
      const id = mkNode(be[1], 'basic', null);
      if (id !== parentId) tree.connections.push({ from: parentId, to: id });
    }
  }
  const seen = new Set();
  tree.connections = tree.connections.filter((c) => {
    const k = `${c.from}->${c.to}`;
    if (seen.has(k)) return false;
    seen.add(k); return true;
  });
  return tree;
}

// =====================================================================
//  medini 交换 JSON（便于脚本/API 直接喂给 medini）
// =====================================================================

export function toMediniJSON(tree, analysis) {
  const { childrenOf } = buildIndex(tree);
  return {
    _format: 'FTA Studio → medini analyze interchange',
    _version: '1.0',
    _hint: '在 medini analyze 中通过脚本 API 或 Import 导入本 JSON',
    project: tree.meta?.project || '',
    standard: tree.meta?.standard || '',
    missionTime: tree.settings?.missionTime ?? null,
    faultTrees: [{
      name: tree.meta?.title || 'FaultTree',
      topEvent: (() => {
        const top = tree.nodes.find((n) => n.type === 'top');
        return top ? { id: top.id, name: top.name } : null;
      })(),
      events: tree.nodes.map((n) => ({
        id: n.id, name: n.name, type: n.type, gate: n.gate,
        voting: n.gate === 'VOTE' ? { k: n.voteK, n: n.voteN } : undefined,
        probability: n.prob, failureRate: n.lambda,
        component: n.component, failureMode: n.failureMode,
        traces: n.ref ? [n.ref] : [], description: n.description,
        inputs: childrenOf.get(n.id) || [],
      })),
      results: analysis ? {
        topEventProbability: analysis.metrics.topProb,
        method: analysis.metrics.topProbMethod,
        cutSetCount: analysis.cutSets.total,
        singlePointsOfFailure: analysis.cutSets.singlePoints,
        minimalCutSets: analysis.cutSets.items.slice(0, 100),
        topImportance: analysis.importance.slice(0, 20).map((r) => ({
          event: r.name, component: r.component,
          criticality: r.criticality, fussellVesely: r.fussellVesely,
        })),
      } : undefined,
    }],
  };
}

// =====================================================================
//  格式自动识别 / 统一导入
// =====================================================================

export function detectFormat(content, filename = '') {
  const c = String(content).trim();
  const fn = String(filename || '').toLowerCase();
  if (fn.endsWith('.fta') || fn.endsWith('.txt')) return 'dsl';
  if (fn.endsWith('.json')) return 'json';
  if (fn.endsWith('.xml')) {
    if (/<(?:\w+:)?define-fault-tree/i.test(c)) return 'cafta';
    return 'faulttreeplus';
  }
  if (/<(?:\w+:)?define-fault-tree/i.test(c)) return 'cafta';
  if (/<(?:\w+:)?(FaultTreePlus|FaultTree|GateInputs|PrimaryEvents|Gates|Events)\b/i.test(c)) return 'faulttreeplus';
  if (c.startsWith('{') || c.startsWith('[')) return 'json';
  return 'dsl';
}

export function importAny(content, filename = '') {
  const fmt = detectFormat(content, filename);
  let tree;
  switch (fmt) {
    case 'cafta': tree = fromCAFTA(content); break;
    case 'faulttreeplus': tree = fromFaultTreePlusXML(content); break;
    case 'json': {
      const obj = typeof content === 'string' ? JSON.parse(content) : content;
      if (obj.dsl) tree = parseDSL(obj.dsl);
      else if (obj.tree) tree = obj.tree;
      else if (Array.isArray(obj.nodes)) tree = obj;
      else if (obj.faultTrees?.[0]) tree = mediniJSONToTree(obj.faultTrees[0]);
      else throw new Error('无法识别的 JSON 结构');
      break;
    }
    default: tree = parseDSL(content);
  }
  const v = validateTree(tree);
  return { tree, format: fmt, validation: v };
}

export function mediniJSONToTree(ft) {
  const tree = {
    version: '1.0',
    meta: {
      title: ft.name || 'Imported',
      project: ft.project || '', author: '', date: new Date().toISOString().slice(0, 10),
      standard: ft.standard || '', missionTime: ft.missionTime ?? null, revision: 'A', description: '',
    },
    settings: { missionTime: ft.missionTime ?? null, maxCutSetOrder: 0, truncation: 1e-12, quantification: 'auto' },
    nodes: [], connections: [],
  };
  for (const e of ft.events || []) {
    const n = blankNode(e.id);
    n.type = e.type; n.name = e.name; n.gate = e.gate || null;
    n.voteK = e.voting?.k ?? 2; n.voteN = e.voting?.n ?? 2;
    n.description = e.description || '';
    n.ref = (e.traces || [])[0] || '';
    n.component = e.component || ''; n.failureMode = e.failureMode || '';
    n.prob = e.probability ?? null; n.lambda = e.failureRate ?? null;
    tree.nodes.push(n);
    for (const inp of e.inputs || []) tree.connections.push({ from: e.id, to: inp });
  }
  if (ft.topEvent?.id) {
    const t = tree.nodes.find((n) => n.id === ft.topEvent.id);
    if (t) t.type = 'top';
  }
  return tree;
}

// =====================================================================
//  辅助
// =====================================================================

/** 注入传输标记节点（仅用于导出时标注跨页关系；只追加，不删改原连接） */
function injectTransferMarkers(tree, pag) {
  const cloned = JSON.parse(JSON.stringify(tree));
  const newNodes = [];
  let seq = 0;
  for (const page of pag.pages) {
    for (const c of page.continuesTo || []) {
      seq++;
      const targetPage = pag.pages.find((p) => p.nodes.has(c.nodeId));
      const tIdx = targetPage?.index ?? c.toPage ?? null;
      newNodes.push(mkTransfer(`TP${String(seq).padStart(3, '0')}`, 'transfer_out',
        tIdx ? `Continued on page ${tIdx}` : 'Continued on next page', tIdx, c.label));
    }
    if (page.continuedFrom) {
      seq++;
      newNodes.push(mkTransfer(`TP${String(seq).padStart(3, '0')}`, 'transfer_in',
        `Transfer from page ${page.continuedFrom.fromPage}`, page.continuedFrom.fromPage, page.continuedFrom.label));
    }
  }
  cloned.nodes.push(...newNodes);
  return cloned;
}

function mkTransfer(id, type, name, target, desc) {
  const n = blankNode(id);
  n.type = type; n.name = name; n.gate = null;
  n.transferRef = target != null ? `Page ${target}` : 'next page';
  n.transferTarget = target; n.description = desc || '';
  return n;
}

/** 生成一个字段完整的内部节点 */
function blankNode(id) {
  const n = createNode(id, 'basic', '');
  n.gate = null;
  return n;
}

/** 读取一行 <FailureModel> 的参数（既认内联属性，也认子元素） */
function readModel(attrs, body) {
  const g = (...names) => pick(attrs, ...names) ?? childText(body, ...names) ?? undefined;
  return {
    model: norm(g('Model', 'ModelType')) ? String(g('Model', 'ModelType')).toLowerCase() : null,
    type: g('Type'),
    value: numOrNull(g('Value', 'Unavailability', 'Probability', 'Q')),
    failureRate: numOrNull(g('FailureRate', 'Lambda', 'Rate')),
    beta: numOrNull(g('Shape', 'Beta')),
    eta: numOrNull(g('Scale', 'Eta')),
    demandCount: numOrNull(g('DemandCount', 'Demands')),
    demandProb: numOrNull(g('DemandProbability')),
    repairTime: numOrNull(g('RepairTime', 'TMR')),
    monitorInterval: numOrNull(g('MonitorInterval', 'TI')),
  };
}

/** 把失效模型参数写回节点 */
function applyModel(n, m) {
  if (!m) return;
  // 优先用内部模型键精确还原
  const internal = m.model ? normalizeModelKey(m.model) : null;
  if (m.failureRate != null && (m.type && /exp|poisson/i.test(m.type))) {
    n.probModel = 'exponential'; n.lambda = m.failureRate; return;
  }
  if (m.eta != null && m.beta != null) { n.probModel = 'weibull'; n.eta = m.eta; n.beta = m.beta; n.lambda = m.failureRate ?? n.lambda; return; }
  if (m.demandCount != null || m.demandProb != null) {
    n.probModel = 'demand'; n.demandCount = m.demandCount; n.demandProb = m.demandProb;
    n.prob = m.value ?? n.prob; return;
  }
  if (m.repairTime != null) { n.probModel = 'repairable'; n.lambda = m.failureRate ?? n.lambda; n.repairTime = m.repairTime; n.prob = m.value ?? n.prob; return; }
  if (m.monitorInterval != null) { n.probModel = 'monitored'; n.lambda = m.failureRate ?? n.lambda; n.monitorInterval = m.monitorInterval; n.prob = m.value ?? n.prob; return; }
  if (internal && internal !== 'fixed' && (m.failureRate != null || m.eta != null)) {
    n.probModel = internal;
    if (m.failureRate != null) n.lambda = m.failureRate;
    if (m.eta != null) n.eta = m.eta; if (m.beta != null) n.beta = m.beta;
    return;
  }
  n.prob = m.value ?? n.prob;
  n.lambda = m.failureRate ?? n.lambda;
  n.probModel = internal || (m.failureRate != null ? 'exponential' : 'fixed');
}

function normalizeModelKey(s) {
  const k = String(s).toLowerCase();
  if (['fixed', 'exponential', 'weibull', 'demand', 'repairable', 'monitored', 'poisson', 'beta'].includes(k)) return k;
  if (/exp|poisson/.test(k)) return 'exponential';
  if (/weib/.test(k)) return 'weibull';
  if (/demand|binomial/.test(k)) return 'demand';
  if (/repair/.test(k)) return 'repairable';
  if (/monitor|dormant/.test(k)) return 'monitored';
  return 'fixed';
}

/** 取某张表的所有行 */
function rows(xml, table, row) {
  const tm = xml.match(new RegExp(`<${table}\\b[^>]*>([\\s\\S]*?)</${table}>`, 'i'));
  const scope = tm ? tm[1] : xml;
  const re = new RegExp(`<${row}\\b([^>]*?)(?:/>|>([\\s\\S]*?)</${row}>)`, 'gi');
  const out = [];
  let m;
  while ((m = re.exec(scope)) !== null) out.push({ attrs: parseAttrs(m[1]), body: m[2] || '' });
  return out;
}

function parseAttrs(s) {
  const out = {};
  const re = /([A-Za-z_][\w.:-]*)\s*=\s*("([^"]*)"|'([^']*)')/g;
  let m;
  while ((m = re.exec(s)) !== null) out[m[1].replace(/^\w+:/, '')] = m[3] ?? m[4] ?? '';
  return out;
}

/** 大小写不敏感地在属性集合中取值 */
function pick(attrs, ...names) {
  const lower = {};
  for (const [k, v] of Object.entries(attrs)) lower[k.toLowerCase()] = v;
  for (const n of names) {
    const v = lower[n.toLowerCase()];
    if (v !== undefined && v !== '') return v;
  }
  return undefined;
}

function childText(body, ...names) {
  for (const n of names) {
    const m = String(body).match(new RegExp(`<${n}\\b[^>]*>([\\s\\S]*?)</${n}>`, 'i'));
    if (m) return m[1].replace(/<[^>]*>/g, '').trim();
  }
  return '';
}

function stripNs(s) {
  return String(s).replace(/<(\/?)\s*[A-Za-z_][\w.-]*:/g, '<$1');
}

function numOrNull(v) {
  if (v == null || v === '') return null;
  const f = Number(v);
  return Number.isNaN(f) ? null : f;
}

function xmlEsc(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&apos;');
}

function num(x, digits = 12) {
  if (x == null || Number.isNaN(x)) return '';
  const v = Number(x);
  if (v === 0) return '0';
  if (Math.abs(v) < 1e-4 || Math.abs(v) >= 1e6) return v.toExponential(digits);
  return String(Number(v.toFixed(digits)));
}
