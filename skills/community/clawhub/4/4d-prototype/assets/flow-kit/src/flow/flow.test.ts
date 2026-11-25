/**
 * Workflow invariants: keep the workflow definition consistent with page wiring, anchors, data objects, DAG layout and scheduling.
 * Run them on every workflow change (new step, new dependency, reordering); any failure means some view will be wrong or the demo will hang.
 */
import { describe, expect, it } from 'vitest';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { ACTORS } from './actors';
import { DATA_OBJECTS } from './dataObjects';
import { DAG_COLS, DAG_POS, EDGES, PHASES, STEPS, STEP_INDEX, ancestorsOf, depsOf, levelOf, orderReady, pathOf, readySteps, stepById, type StepId } from './workflow';

const SRC = join(__dirname, '..');

function sources(dir: string): string[] {
  return readdirSync(dir).flatMap((f) => {
    const p = join(dir, f);
    if (statSync(p).isDirectory()) return sources(p);
    return /\.tsx?$/.test(f) && !f.endsWith('.test.ts') ? [readFileSync(p, 'utf8')] : [];
  });
}

describe('workflow definition', () => {
  const all = sources(SRC).join('\n');

  it('orders steps by phase with unique ids', () => {
    const order = STEPS.map((s) => PHASES.findIndex((p) => p.key === s.phase));
    expect(order.every((x) => x >= 0)).toBe(true);
    expect([...order].sort((a, b) => a - b)).toEqual(order);
    expect(new Set(STEPS.map((s) => s.id)).size).toBe(STEPS.length);
  });

  it('references existing actors and data objects, with at least one sub-step', () => {
    for (const s of STEPS) {
      for (const a of [s.actor, ...s.with, ...s.subs.map((x) => x.actor)]) expect(ACTORS[a], `${s.id} ${a}`).toBeTruthy();
      for (const k of [...s.inputs, ...s.outputs]) expect(DATA_OBJECTS[k], `${s.id} ${k}`).toBeTruthy();
      expect(s.subs.length, s.id).toBeGreaterThan(0);
      expect(s.with, s.id).not.toContain(s.actor);
    }
  });

  it('uses only inputs or outputs of the step in each sub-step', () => {
    for (const s of STEPS) for (const x of s.subs) expect([...s.inputs, ...s.outputs], `${s.id} ${x.title} → ${x.data}`).toContain(x.data);
  });

  it('wires every page-driven step with useFlowStep', () => {
    for (const s of STEPS.filter((x) => x.drive === 'page')) expect(all, s.id).toContain(`useFlowStep('${s.id}'`);
  });

  it('finds every highlight anchor referenced by a sub-step in the pages', () => {
    for (const s of STEPS)
      for (const x of s.subs)
        if (x.anchor) expect(all.includes(`data-flow-anchor="${x.anchor}"`) || all.includes(`anchor="${x.anchor}"`), `${s.id} → ${x.anchor}`).toBe(true);
  });

  it('chains only from the previous step on the same page', () => {
    for (const s of STEPS.filter((x) => x.chain)) {
      const prev = STEPS[STEP_INDEX[s.id] - 1];
      expect(pathOf(prev.route), s.id).toBe(pathOf(s.route));
      expect(depsOf(s.id), s.id).toContain(prev.id);
    }
  });
});

describe('workflow DAG', () => {
  it('has edges between valid steps, without duplicates or self-loops', () => {
    const ids = new Set(STEPS.map((s) => s.id));
    const keys = EDGES.map((e) => `${e.from}>${e.to}`);
    expect(new Set(keys).size).toBe(keys.length);
    for (const e of EDGES) {
      expect(ids.has(e.from) && ids.has(e.to), `${e.from}>${e.to}`).toBe(true);
      expect(e.from).not.toBe(e.to);
    }
  });

  it('is acyclic and STEPS is a topological order', () => {
    for (const e of EDGES) expect(STEP_INDEX[e.from], `${e.from}>${e.to}`).toBeLessThan(STEP_INDEX[e.to]);
    for (const s of STEPS) expect(ancestorsOf(s.id).has(s.id)).toBe(false);
  });

  it('carries edge data that matches the upstream outputs and downstream inputs', () => {
    for (const e of EDGES.filter((x) => x.data)) {
      expect(stepById(e.from).outputs, `${e.from} outputs ${e.data}`).toContain(e.data);
      expect(stepById(e.to).inputs, `${e.to} inputs ${e.data}`).toContain(e.data);
    }
  });

  it('lays out left to right: downstream columns exceed all upstream columns, no overlap, within the column count', () => {
    for (const e of EDGES) expect(DAG_POS[e.to].col, `${e.from}>${e.to}`).toBeGreaterThan(DAG_POS[e.from].col);
    const cells = STEPS.map((s) => `${DAG_POS[s.id].col}:${DAG_POS[s.id].row}`);
    expect(new Set(cells).size).toBe(cells.length);
    for (const s of STEPS) expect(DAG_POS[s.id].col).toBeLessThan(DAG_COLS);
    expect(Math.max(...STEPS.map((s) => levelOf(s.id)))).toBeLessThanOrEqual(DAG_COLS - 1);
  });

  it('visits every step exactly once when always taking the first ready step, with dependencies satisfied', () => {
    const done: StepId[] = [];
    while (done.length < STEPS.length) {
      const ready = readySteps(done);
      expect(ready.length).toBeGreaterThan(0);
      expect(depsOf(ready[0]).every((d) => done.includes(d))).toBe(true);
      done.push(ready[0]);
    }
    expect(done).toEqual(STEPS.map((s) => s.id));
    expect(readySteps(done)).toEqual([]);
  });

  function simulate(start: StepId[], assumed: StepId[]) {
    const done: StepId[] = [...assumed];
    const order: StepId[] = [];
    const run = (id: StepId) => {
      expect(depsOf(id).every((d) => done.includes(d)), id).toBe(true);
      done.push(id);
      order.push(id);
    };
    start.forEach(run);
    while (done.length < STEPS.length) run(orderReady(done)[0]);
    return order;
  }

  it('runs from the start in STEPS order', () => {
    expect(simulate([], [])).toEqual(STEPS.map((s) => s.id));
  });

  it('finishes from any starting step, with executed + assumed done = total', () => {
    for (const s of STEPS) {
      const assumed = [...ancestorsOf(s.id)];
      const order = simulate([s.id], assumed);
      expect(order.length + assumed.length, s.id).toBe(STEPS.length);
    }
  });
});

describe('requirement status of steps', () => {
  it('states a basis for every labeled step', () => {
    for (const s of STEPS.filter((x) => x.necessity)) expect(s.basis, s.id).toBeTruthy();
  });

  it('never makes a non-optional step depend on an optional one (removing optional steps keeps the main flow)', () => {
    const optional = new Set(STEPS.filter((s) => s.necessity === 'optional').map((s) => s.id));
    for (const s of STEPS.filter((x) => x.necessity !== 'optional')) expect([...ancestorsOf(s.id)].filter((a) => optional.has(a)), s.id).toEqual([]);
  });

  it('schedules optional steps last', () => {
    const order = orderReady(STEPS.filter((s) => s.necessity === 'optional').flatMap((s) => [...ancestorsOf(s.id)]));
    const firstOptional = order.findIndex((id) => stepById(id).necessity === 'optional');
    if (firstOptional >= 0) expect(order.slice(firstOptional).every((id) => stepById(id).necessity === 'optional')).toBe(true);
  });
});
