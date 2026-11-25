/**
 * Demo virtual clock: every demo animation and every director delay goes through here.
 * - Playback speed (0.25× / 0.5× / 1× / 2×) can change at any time; pending delays continue at the new speed immediately.
 * - Pausing the demo freezes the clock, so in-page pipelines, RPA replays and director scripts all stop together.
 * Implementation: virtual time = Σ(real elapsed × speed); due callbacks are fired by a lightweight ticker.
 */
import { useSyncExternalStore } from 'react';

export const SPEEDS = [0.25, 0.5, 1, 2] as const;
export type Speed = (typeof SPEEDS)[number];

export class VirtualClock {
  private v = 0;
  private last: number;
  private speed = 1;
  private frozen = false;
  private seq = 0;
  private timers = new Map<number, { due: number; fn: () => void }>();

  constructor(private now: () => number) {
    this.last = now();
  }

  /** Advance virtual time and fire due callbacks (called by the ticker or by tests) */
  tick() {
    const t = this.now();
    if (!this.frozen) this.v += (t - this.last) * this.speed;
    this.last = t;
    const due = [...this.timers].filter(([, x]) => x.due <= this.v).sort((a, b) => a[1].due - b[1].due);
    for (const [id, x] of due) {
      if (!this.timers.has(id)) continue;
      this.timers.delete(id);
      x.fn();
    }
  }

  setTimeout(fn: () => void, ms: number) {
    this.tick();
    const id = ++this.seq;
    this.timers.set(id, { due: this.v + Math.max(0, ms), fn });
    return id;
  }

  clearTimeout(id: number) {
    this.timers.delete(id);
  }

  setSpeed(s: number) {
    this.tick();
    this.speed = s;
  }

  getSpeed() {
    return this.speed;
  }

  setFrozen(f: boolean) {
    this.tick();
    this.frozen = f;
  }

  isFrozen() {
    return this.frozen;
  }

  pending() {
    return this.timers.size;
  }

  nowV() {
    this.tick();
    return this.v;
  }

  /** Read the current virtual time without firing due callbacks (safe to call during render) */
  peekV() {
    return this.frozen ? this.v : this.v + (this.now() - this.last) * this.speed;
  }
}

const hasWindow = typeof window !== 'undefined';
const clock = new VirtualClock(() => (typeof performance !== 'undefined' ? performance.now() : Date.now()));
let ticking = 0;
const listeners = new Set<() => void>();

function loop() {
  ticking = 0;
  clock.tick();
  if (clock.pending()) ticking = window.setTimeout(loop, 16);
}

function ensureTicking() {
  if (hasWindow && !ticking && clock.pending()) ticking = window.setTimeout(loop, 16);
}

/** Delay scaled by playback speed (for demos) */
export function vSetTimeout(fn: () => void, ms: number) {
  const id = clock.setTimeout(fn, ms);
  ensureTicking();
  return id;
}

export function vClearTimeout(id: number) {
  clock.clearTimeout(id);
}

export function getSpeed(): number {
  return clock.getSpeed();
}

export function setClockSpeed(s: number) {
  clock.setSpeed(s);
  listeners.forEach((l) => l());
}

export function freezeClock(f: boolean) {
  if (clock.isFrozen() === f) return;
  clock.setFrozen(f);
  listeners.forEach((l) => l());
  ensureTicking();
}

function subscribe(l: () => void) {
  listeners.add(l);
  return () => listeners.delete(l);
}

export function useSpeed() {
  return useSyncExternalStore(subscribe, getSpeed, getSpeed);
}

export function useClockFrozen() {
  return useSyncExternalStore(subscribe, () => clock.isFrozen(), () => false);
}

/** Current virtual time in ms, read-only: drive rAF animations with it; they stop automatically while the clock is frozen */
export function vNow() {
  return clock.peekV();
}
