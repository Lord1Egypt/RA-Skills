/**
 * Topological workflow executor with conditional routing, iteration/loop
 * subgraph execution, and streaming answer support.
 *
 * Engine file — copy as-is from the skill template; do NOT edit per project.
 * Business logic lives in definition.js (data) and blocks/ (handlers).
 *
 * Definition format: see the Python twin (runner.py) — same semantics.
 * - nodes[id].parent marks iteration/loop body nodes.
 * - Parallel iteration is degraded to sequential (declared degradation).
 */
import { VariablePool } from './context.js';

const BRANCH_TYPES = new Set(['if-else', 'question-classifier']);

const OPS = {
  'contains': (a, b) => String(a).includes(String(b)),
  'not contains': (a, b) => !String(a).includes(String(b)),
  'start with': (a, b) => String(a).startsWith(String(b)),
  'end with': (a, b) => String(a).endsWith(String(b)),
  'is': (a, b) => String(a) === String(b),
  'is not': (a, b) => String(a) !== String(b),
  'empty': (a) => !a,
  'not empty': (a) => !!a,
  'exists': (a) => a != null,
  'not exists': (a) => a == null,
  'null': (a) => a == null,
  'not null': (a) => a != null,
  '=': (a, b) => a === b,
  '≠': (a, b) => a !== b,
  '>': (a, b) => Number(a) > Number(b),
  '<': (a, b) => Number(a) < Number(b),
  '≥': (a, b) => Number(a) >= Number(b),
  '≤': (a, b) => Number(a) <= Number(b),
  '>=': (a, b) => Number(a) >= Number(b),
  '<=': (a, b) => Number(a) <= Number(b),
  'in': (a, b) => String(b).split(',').includes(String(a)),
  'not in': (a, b) => !String(b).split(',').includes(String(a)),
};

export function evalCondition(cond, pool) {
  const sel = cond.variable_selector || [];
  const actual = sel.length === 2 ? pool.get(sel[0], sel[1]) : null;
  const op = OPS[cond.comparison_operator || 'is'];
  if (!op) throw new Error(`unsupported operator: ${cond.comparison_operator}`);
  return !!op(actual, cond.value);
}

function evalGroup(conds, logical, pool) {
  const results = (conds || []).map((c) => evalCondition(c, pool));
  return (logical || 'and') === 'or' ? results.some(Boolean) : results.every(Boolean);
}

export function evalBranch(node, pool) {
  const cfg = node.config;
  if (node.type === 'question-classifier') {
    // handler must have written the chosen class id to (nodeId, 'class_id')
    return new Set([String(pool.get(node.id, 'class_id', '1'))]);
  }
  if (cfg.cases) {
    for (const kase of cfg.cases) {
      const conds = kase.conditions || [];
      if (!conds.length) continue; // default/else case
      if (evalGroup(conds, kase.logical_operator, pool)) {
        return new Set([String(kase.case_id || kase.id || 'true')]);
      }
    }
    return new Set(['false']);
  }
  return evalGroup(cfg.conditions, cfg.logical_operator, pool)
    ? new Set(['true']) : new Set(['false']);
}

export class Engine {
  /**
   * @param {{nodes: Object, edges: Array, start_id: string}} definition
   * @param {Object<string, (nodeId, config, pool, engine) => void|Promise<void>>} handlers
   */
  constructor(definition, handlers) {
    this.nodes = definition.nodes;
    this.edges = definition.edges;
    this.startId = definition.start_id;
    this.handlers = handlers || {};
    this._out = new Map();
    for (const e of this.edges) {
      if (!this._out.has(e.source)) this._out.set(e.source, []);
      this._out.get(e.source).push(e);
    }
    this._children = new Map();
    for (const [nid, n] of Object.entries(this.nodes)) {
      if (n.parent) {
        if (!this._children.has(n.parent)) this._children.set(n.parent, []);
        this._children.get(n.parent).push(nid);
      }
    }
    this.pool = new VariablePool();
    this.outputs = {};
    this.answers = [];
  }

  async run(inputs) {
    for await (const _ of this.runStream(inputs)) { /* drain */ }
    return this.outputs;
  }

  /** Yields ['answer', text] per answer node, then ['final', outputs]. */
  async *runStream(inputs) {
    this.pool.setMany(this.startId, inputs);
    yield* this._execute(this.startId, null);
    if (this.answers.length) {
      this.outputs.answer ??= this.answers.join('');
    }
    yield ['final', this.outputs];
  }

  async *_execute(entryId, scope) {
    const queue = [entryId];
    const executed = new Set();
    while (queue.length) {
      const nid = queue.shift();
      if (executed.has(nid) || !this.nodes[nid]) continue;
      if (scope && !scope.has(nid)) continue;
      executed.add(nid);
      const node = { id: nid, ...this.nodes[nid] };
      const ntype = node.type;
      let active = null;

      if (['start', 'iteration-start', 'loop-start'].includes(ntype)) {
        // entry nodes: no-op
      } else if (BRANCH_TYPES.has(ntype)) {
        if (ntype === 'question-classifier' && this.handlers[nid]) {
          await this.handlers[nid](nid, node.config, this.pool, this);
        }
        active = evalBranch(node, this.pool);
      } else if (ntype === 'answer') {
        const text = this.pool.resolve(node.config.answer || '');
        this.answers.push(text);
        yield ['answer', text];
      } else if (ntype === 'end') {
        this._collectEnd(node);
      } else if (ntype === 'iteration') {
        await this._runIteration(nid, node);
      } else if (ntype === 'loop') {
        yield* this._runLoop(nid, node);
      } else {
        const handler = this.handlers[nid];
        if (!handler) {
          throw new Error(
            `no handler registered for node ${nid} (${ntype}); ` +
            'implement it in src/workflow/blocks/');
        }
        await handler(nid, node.config, this.pool, this);
      }

      for (const e of this._out.get(nid) || []) {
        if (scope && !scope.has(e.target)) continue;
        if (active === null || active.has(String(e.handle))) queue.push(e.target);
      }
    }
  }

  _collectEnd(node) {
    for (const out of node.config.outputs || []) {
      const sel = out.value_selector || [];
      if (sel.length === 2) this.outputs[out.variable] = this.pool.get(sel[0], sel[1]);
    }
  }

  async _runIteration(nid, node) {
    const cfg = node.config;
    const sel = cfg.iterator_selector || [];
    const items = sel.length === 2 ? this.pool.get(sel[0], sel[1]) : null;
    if (!Array.isArray(items)) {
      throw new Error(`iteration ${nid}: selector ${sel} did not resolve to a list`);
    }
    const scope = new Set(this._children.get(nid) || []);
    const entry = scope.has(`${nid}start`) ? `${nid}start` : null;
    const outSel = cfg.output_selector || [];
    const results = [];
    for (let i = 0; i < items.length; i++) {
      this.pool.set(nid, 'item', items[i]);
      this.pool.set(nid, 'index', i);
      if (entry && scope.size) {
        for await (const _ of this._execute(entry, scope)) { /* no streaming inside */ }
      }
      results.push(outSel.length === 2 ? this.pool.get(outSel[0], outSel[1]) : null);
    }
    this.pool.set(nid, 'output', results);
  }

  async *_runLoop(nid, node) {
    const cfg = node.config;
    for (const v of cfg.loop_variables || []) {
      const sel = v.value_selector || [];
      if (sel.length === 2) {
        this.pool.set(nid, v.label || v.variable || 'var', this.pool.get(sel[0], sel[1]));
      }
    }
    const scope = new Set(this._children.get(nid) || []);
    const entry = scope.has(`${nid}start`) ? `${nid}start` : null;
    const maxCount = Number(cfg.loop_count || 10);
    for (let i = 0; i < maxCount; i++) {
      if (entry && scope.size) yield* this._execute(entry, scope);
      const conds = cfg.break_conditions || [];
      if (conds.length && evalGroup(conds, cfg.logical_operator, this.pool)) break;
    }
  }
}
