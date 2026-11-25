/**
 * The whole-flow demo "director": schedules steps along the DAG in workflow.ts — a step is ready only when all upstream
 * steps are done — switches roles, navigates pages, and lets each page perform its step.
 *
 * - Pages hook in with useFlowStep(stepId, onEnter): when it is their step's turn they receive a ctl,
 *   report sub-step progress with ctl.sub(i) and completion with ctl.done(); walk steps are advanced by the director on sub-step timers.
 * - Autoplay: after a step finishes, dwell briefly, then enter the highest-priority ready step.
 *   Step mode: list all ready steps (parallel branches) and let a person choose the branch.
 * - Jumping to a step marks its unfinished upstream steps as "assumed done (using data already in the demo)" so dependencies hold.
 * - Navigating away from the current page mid-demo pauses automatically, so the director and the person never fight over the wheel.
 * State lives in memory only (not persisted); a reload ends the demo.
 *
 * Page contract (see references/flow-orchestration.md §4):
 * - onEnter must supply its own upstream with demo data when the page just opened and upstream output is missing
 *   (any step can be switched to at any time and replayed after finishing);
 * - steps that judge completion by a player's progress record the task id started by this entry (ctl.nonce),
 *   so a previous run's result is never mistaken for completion;
 * - read the latest state through refs in callbacks; no real downloads during a demo (flowActive()).
 */
import { useEffect, useMemo, useRef } from 'react';
import { createStore, useStore } from '@/lib/store';
import { navigate } from '@/lib/router';
import { sessionStore, setRole } from '@/state/session';
import type { ActorKey } from './actors';
import { SPEEDS, freezeClock, setClockSpeed, vClearTimeout, vSetTimeout, type Speed } from './clock';
import { HUMAN, cursorClick, cursorHover, hideCursor } from './cursor';
import { STEPS, STEP_INDEX, ancestorsOf, depsOf, orderReady, pathOf, readySteps, stepById, type StepId } from './workflow';

export type FlowMode = 'auto' | 'step';
export type FlowStatus = 'idle' | 'running' | 'step-done' | 'finished';

export interface FlowState {
  active: boolean;
  mode: FlowMode;
  idx: number;
  sub: number;
  status: FlowStatus;
  nonce: number;
  paused: boolean;
  /** The user navigated away from the current step's page mid-demo */
  left: boolean;
  completed: StepId[];
  /** Upstream steps assumed done on a jump (existing or preset demo data is used; not actually executed) */
  assumed: StepId[];
  /** Order in which steps were actually entered (used by "previous step") */
  trail: StepId[];
  startedAt: number;
  finishedAt: number;
  /** Step expanded in the navigator while no demo is running */
  focus: StepId | null;
  startOpen: boolean;
}

const INIT: FlowState = {
  active: false,
  mode: 'auto',
  idx: 0,
  sub: 0,
  status: 'idle',
  nonce: 0,
  paused: false,
  left: false,
  completed: [],
  assumed: [],
  trail: [],
  startedAt: 0,
  finishedAt: 0,
  focus: null,
  startOpen: false,
};

export const flowStore = createStore<FlowState>('flow', () => INIT, { persist: false });

/** Navigator panel state and playback speed (personal preferences, persisted) */
export const flowPrefs = createStore<{ panel: 'open' | 'compact'; speed: Speed; dock: 'open' | 'min'; dockH: number }>('flow-prefs', () => ({
  panel: 'compact',
  speed: 1,
  dock: 'open',
  dockH: 250,
}));
// Older versions saved removed speeds such as 4×: fall back to the nearest available one
if (!SPEEDS.includes(flowPrefs.get().speed)) flowPrefs.set({ speed: 2 });
setClockSpeed(flowPrefs.get().speed);

/** Change playback speed: takes effect immediately (including pending delays, pipelines and RPA replays) */
export function setFlowSpeed(speed: Speed) {
  flowPrefs.set({ speed });
  setClockSpeed(speed);
}

export function useFlow<S>(sel: (s: FlowState) => S): S {
  return useStore(flowStore, sel);
}

/* ---------------- Timers ---------------- */

const DWELL = 1600; // autoplay: pause between steps
const WALK_DEFAULT = 2600; // default dwell of a walk sub-step
const FALLBACK = 30000; // watchdog: skip a page step that reports no progress for this long, so the demo never hangs

let walkTimer = 0;
let advanceTimer = 0;
let fallbackTimer = 0;
let expectedPath: string | null = null;
/** Walk step entered while paused: starts advancing only on resume */
let pendingWalk = 0;
/** Delays registered by pages through ctl.later (owned by the current step, cleared on step change) */
let stepTimers: number[] = [];

function clearAll() {
  vClearTimeout(walkTimer);
  vClearTimeout(advanceTimer);
  vClearTimeout(fallbackTimer);
  stepTimers.forEach((t) => vClearTimeout(t));
  stepTimers = [];
}

const st = () => flowStore.get();
const stale = (nonce: number) => !st().active || st().nonce !== nonce;

function armFallback(nonce: number) {
  vClearTimeout(fallbackTimer);
  fallbackTimer = vSetTimeout(() => {
    if (!stale(nonce) && st().status === 'running') complete(nonce);
  }, FALLBACK);
}

/* ---------------- Dependency state ---------------- */

export type StepState = 'idle' | 'running' | 'done' | 'assumed' | 'ready' | 'waiting';

const doneOf = (s: FlowState) => [...s.completed, ...s.assumed];

/** State of a step in this demo: running / done / assumed done / ready (upstream complete) / waiting for upstream */
export function stepStateOf(s: FlowState, id: StepId): StepState {
  if (!s.active) return 'idle';
  if (STEPS[s.idx]?.id === id && s.status === 'running') return 'running';
  if (s.completed.includes(id)) return 'done';
  if (s.assumed.includes(id)) return 'assumed';
  const done = new Set(doneOf(s));
  return depsOf(id).every((d) => done.has(d)) ? 'ready' : 'waiting';
}

/** Steps ready now (excluding the running one), in priority order (STEPS order, optional steps last) */
export function readyNow(s: FlowState = st()): StepId[] {
  const cur = STEPS[s.idx]?.id;
  return orderReady(doneOf(s)).filter((id) => !(s.status === 'running' && id === cur));
}

/* ---------------- Advancing steps ---------------- */

/** keepPaused: when a step is clicked while paused (DAG node, previous / next), switch to it but stay paused */
function enter(i: number, opts: { keepPaused?: boolean } = {}) {
  clearAll();
  const keep = !!opts.keepPaused;
  freezeClock(keep);
  pendingWalk = 0;
  const step = STEPS[i];
  const s = st();
  const nonce = s.nonce + 1;
  flowStore.set({
    idx: i,
    sub: 0,
    status: 'running',
    nonce,
    paused: keep,
    left: false,
    focus: null,
    // A step being re-executed no longer counts as done
    completed: s.completed.filter((x) => x !== step.id),
    assumed: s.assumed.filter((x) => x !== step.id),
    trail: s.trail[s.trail.length - 1] === step.id ? s.trail : [...s.trail, step.id],
  });
  if (sessionStore.get().role !== step.role) setRole(step.role);
  expectedPath = pathOf(step.route);
  navigate(step.route);
  if (step.drive === 'walk') {
    if (keep) pendingWalk = nonce;
    else walkTimer = vSetTimeout(() => walk(nonce, 0), 900);
  } else if (!keep) armFallback(nonce);
}

function walk(nonce: number, k: number) {
  if (stale(nonce) || st().paused) return;
  const step = STEPS[st().idx];
  if (k >= step.subs.length) {
    complete(nonce);
    return;
  }
  flowStore.set({ sub: k });
  walkTimer = vSetTimeout(() => walk(nonce, k + 1), step.subs[k].ms ?? WALK_DEFAULT);
}

function complete(nonce: number) {
  if (stale(nonce) || st().status !== 'running') return;
  vClearTimeout(fallbackTimer);
  const s = st();
  const step = STEPS[s.idx];
  const completed = s.completed.includes(step.id) ? s.completed : [...s.completed, step.id];
  const finished = readySteps([...completed, ...s.assumed]).length === 0;
  flowStore.set({ completed, status: finished ? 'finished' : 'step-done', sub: step.subs.length - 1, finishedAt: finished ? Date.now() : 0 });
  if (!finished) scheduleAdvance();
}

function scheduleAdvance() {
  const s = st();
  if (s.paused || s.status !== 'step-done') return;
  const ready = readyNow(s);
  if (!ready.length) return;
  const cur = STEPS[s.idx].id;
  // Continuation of the same backend job (e.g. RPA capture finishes, then the batch check starts): chain immediately in either mode
  const chained = ready.find((id) => stepById(id).chain && depsOf(id).includes(cur));
  const nonce = s.nonce;
  if (chained) advanceTimer = vSetTimeout(() => !stale(nonce) && enter(STEP_INDEX[chained]), 500);
  else if (s.mode === 'auto') advanceTimer = vSetTimeout(() => !stale(nonce) && enter(STEP_INDEX[ready[0]]), DWELL);
}

/**
 * Enter the target step directly (any step can run on its own: when page state is missing, the page prepares upstream output from demo data);
 * unfinished upstream steps of the target are recorded as "assumed done" (existing data is used), keeping DAG dependencies valid.
 */
function enterTarget(id: StepId, opts: { keepPaused?: boolean } = {}) {
  const s = st();
  const done = new Set(doneOf(s));
  const assumed = [...s.assumed, ...[...ancestorsOf(id)].filter((a) => !done.has(a))];
  flowStore.set({ assumed });
  enter(STEP_INDEX[id], opts);
}

/* ---------------- Public actions ---------------- */

export function openFlowStart() {
  flowStore.set({ startOpen: true });
}

export function closeFlowStart() {
  flowStore.set({ startOpen: false });
}

export async function startFlow(opts: { mode: FlowMode; reset: boolean; from?: StepId }) {
  clearAll();
  // Loaded on demand: reset pulls in large modules (config stores, retained results), so keep it out of the first load
  if (opts.reset) (await import('@/state/reset')).resetDemo();
  flowStore.set({ ...INIT, active: true, mode: opts.mode, startedAt: Date.now(), nonce: st().nonce });
  flowPrefs.set({ panel: 'open' });
  if (opts.from) enterTarget(opts.from);
  else enter(STEP_INDEX[readySteps([])[0]]);
}

export function stopFlow() {
  clearAll();
  freezeClock(false);
  hideCursor(true);
  expectedPath = null;
  flowStore.set({ ...INIT, nonce: st().nonce + 1 });
}

/** Next step: the highest-priority ready step; the running step is marked done (skipped) */
export function nextStep() {
  const s = st();
  if (!s.active || s.status === 'finished') return;
  const cur = STEPS[s.idx].id;
  const completed = s.status === 'running' && !s.completed.includes(cur) ? [...s.completed, cur] : s.completed;
  const ready = orderReady([...completed, ...s.assumed]);
  if (!ready.length) {
    clearAll();
    flowStore.set({ completed, status: 'finished', finishedAt: Date.now() });
    return;
  }
  flowStore.set({ completed });
  enter(STEP_INDEX[ready[0]], { keepPaused: s.paused });
}

/** Previous step: go back to the previously entered step and re-execute it */
export function prevStep() {
  const s = st();
  if (!s.active || s.trail.length < 2) return;
  const prev = s.trail[s.trail.length - 2];
  flowStore.set({ trail: s.trail.slice(0, -1) });
  enterTarget(prev, { keepPaused: s.paused });
}

export function pauseFlow() {
  if (!st().active) return;
  vClearTimeout(walkTimer);
  vClearTimeout(advanceTimer);
  vClearTimeout(fallbackTimer);
  flowStore.set({ paused: true });
  freezeClock(true);
}

export function resumeFlow() {
  const s = st();
  if (!s.active) return;
  freezeClock(false);
  if (s.left && s.status === 'running') {
    enterTarget(STEPS[s.idx].id);
    return;
  }
  flowStore.set({ paused: false });
  if (s.status === 'step-done') scheduleAdvance();
  else if (s.status === 'running') {
    if (STEPS[s.idx].drive === 'walk') {
      if (pendingWalk === s.nonce) {
        pendingWalk = 0;
        walkTimer = vSetTimeout(() => walk(s.nonce, 0), 900);
      } else walk(s.nonce, s.sub);
    } else armFallback(s.nonce);
  }
}

/** Space / big button: running → pause; paused → resume; waiting in step mode → next step */
export function togglePlay() {
  const s = st();
  if (!s.active || s.status === 'finished') return;
  if (s.paused) resumeFlow();
  else if (s.status === 'step-done' && s.mode === 'step') nextStep();
  else pauseFlow();
}

export function setFlowMode(mode: FlowMode) {
  flowStore.set({ mode });
  if (mode === 'auto') scheduleAdvance();
}

export function restartFlow() {
  void startFlow({ mode: st().mode, reset: true });
}

/**
 * During a demo (including after the whole flow has finished): switch to the step and run it; if paused, switch and stay paused.
 * A step replayed after finishing returns to "finished" when done. Without a demo: switch role and open the step's page (browse mode).
 */
export function goToStep(id: StepId) {
  const s = st();
  if (s.active) {
    // A pause caused by leaving the demo page is not a user pause: clicking a step plays immediately
    enterTarget(id, { keepPaused: s.paused && !s.left });
    return;
  }
  const step = stepById(id);
  if (sessionStore.get().role !== step.role) setRole(step.role);
  flowStore.set({ focus: id });
  navigate(step.route);
}

export function focusStep(id: StepId | null) {
  flowStore.set({ focus: id });
  if (id) flowPrefs.set({ panel: 'open' });
}

/*
 * Navigating away from the current step's page mid-demo:
 * - step still running → pause (page state is lost; the step is re-executed on resume);
 * - step finished, waiting for the next → don't interrupt, just record that page state is lost (later steps prepare from demo data).
 */
if (typeof window !== 'undefined') {
  window.addEventListener('hashchange', () => {
    const s = st();
    if (!s.active || s.status === 'finished' || !expectedPath) return;
    const path = window.location.hash.replace(/^#/, '').split('?')[0] || '/';
    if (path === expectedPath || s.left) return;
    // After leaving the demo page the user may work on other pages: a frozen clock must not affect them
    freezeClock(false);
    if (s.status === 'running') {
      vClearTimeout(walkTimer);
      vClearTimeout(advanceTimer);
      vClearTimeout(fallbackTimer);
      flowStore.set({ paused: true, left: true });
    } else flowStore.set({ left: true });
  });
}

/* ---------------- Page hook ---------------- */

export interface FlowCtl {
  nonce: number;
  /** Report the current sub-step (index into the step's subs in workflow.ts) */
  sub: (i: number) => void;
  /** This step is complete */
  done: () => void;
  /** Delayed call; cancelled automatically on step change or page unmount */
  later: (ms: number, fn: () => void) => void;
  /** Move the demo cursor to the element and click, then run the action (skipped if the step has changed) */
  click: (target: string | Element, fn?: () => void, actor?: ActorKey) => void;
  /** Move the demo cursor over the element (no click); optionally run then on arrival */
  hover: (target: string | Element, then?: () => void, actor?: ActorKey) => void;
}

/** The "person" operating now: the current sub-step's actor if human, else a human owner / collaborator of the step, else the first human role */
function operator(): ActorKey {
  const s = st();
  const step = STEPS[s.idx];
  const sub = step?.subs[s.sub]?.actor;
  if (sub && HUMAN.includes(sub)) return sub;
  if (step && HUMAN.includes(step.actor)) return step.actor;
  const h = step?.with.find((a) => HUMAN.includes(a));
  return h ?? HUMAN[0];
}

function cursorApi(nonce: number) {
  const ok = () => !stale(nonce);
  return {
    click: (target: string | Element, fn?: () => void, actor?: ActorKey) =>
      cursorClick(
        target,
        actor ?? operator(),
        () => {
          fn?.();
          // If a machine takes over after the click (e.g. "run check" hands off to the backend batch), hide the cursor once the click animation ends
          const s = st();
          const sub = STEPS[s.idx]?.subs[s.sub];
          if (sub && !HUMAN.includes(sub.actor)) hideCursor();
        },
        ok,
      ),
    hover: (target: string | Element, then?: () => void, actor?: ActorKey) => cursorHover(target, actor ?? operator(), then && (() => ok() && then())),
  };
}

/**
 * Hook a page into the whole-flow demo:
 * - returns ctl while it is this page's step (report progress from effects), otherwise null;
 * - onEnter: called once on entering the step (may return a cleanup, called on step change or unmount).
 */
export function useFlowStep(id: StepId, onEnter?: (ctl: FlowCtl) => void | (() => void)): FlowCtl | null {
  const nonce = useFlow((s) => (s.active && STEPS[s.idx]?.id === id ? s.nonce : 0));
  const ctl = useMemo<FlowCtl | null>(() => {
    if (!nonce) return null;
    return {
      nonce,
      sub: (i) => {
        if (stale(nonce) || st().status !== 'running') return;
        if (st().sub !== i) flowStore.set({ sub: i });
        armFallback(nonce);
      },
      done: () => complete(nonce),
      later: (ms, fn) => {
        stepTimers.push(vSetTimeout(() => !stale(nonce) && fn(), ms));
      },
      ...cursorApi(nonce),
    };
  }, [nonce]);
  const ref = useRef(onEnter);
  ref.current = onEnter;
  useEffect(() => {
    if (!ctl || !ref.current) return;
    const timers: number[] = [];
    const scoped: FlowCtl = {
      ...ctl,
      later: (ms, fn) => {
        timers.push(vSetTimeout(() => !stale(ctl.nonce) && fn(), ms));
      },
    };
    let cleanup: void | (() => void);
    // Defer to the next tick: React StrictMode's mount-unmount-mount in development then runs it only once
    const t = window.setTimeout(() => {
      cleanup = ref.current?.(scoped);
    }, 0);
    return () => {
      window.clearTimeout(t);
      timers.forEach((x) => vClearTimeout(x));
      if (typeof cleanup === 'function') cleanup();
    };
  }, [ctl]);
  return ctl;
}

/** Outside React: is a whole-flow demo running? */
export function flowActive() {
  return st().active;
}
