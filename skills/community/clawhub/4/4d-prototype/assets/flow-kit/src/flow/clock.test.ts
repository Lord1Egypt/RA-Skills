import { describe, expect, it } from 'vitest';
import { VirtualClock } from './clock';

function setup() {
  let now = 0;
  const clock = new VirtualClock(() => now);
  const advance = (ms: number) => {
    now += ms;
    clock.tick();
  };
  return { clock, advance };
}

describe('demo virtual clock', () => {
  it('fires on real time at 1× and in half the time at 2×', () => {
    const { clock, advance } = setup();
    const hits: string[] = [];
    clock.setTimeout(() => hits.push('a'), 1000);
    advance(999);
    expect(hits).toEqual([]);
    advance(1);
    expect(hits).toEqual(['a']);
    clock.setSpeed(2);
    clock.setTimeout(() => hits.push('b'), 1000);
    advance(499);
    expect(hits).toEqual(['a']);
    advance(1);
    expect(hits).toEqual(['a', 'b']);
  });

  it('applies a speed change mid-wait immediately (elapsed time counts at the old speed)', () => {
    const { clock, advance } = setup();
    let fired = false;
    clock.setTimeout(() => (fired = true), 1000);
    advance(400); // 400 elapsed
    clock.setSpeed(4); // remaining 600 at 4× → 150ms
    advance(149);
    expect(fired).toBe(false);
    advance(1);
    expect(fired).toBe(true);
  });

  it('does not advance while frozen (paused) and continues after unfreezing', () => {
    const { clock, advance } = setup();
    let fired = false;
    clock.setTimeout(() => (fired = true), 500);
    advance(200);
    clock.setFrozen(true);
    advance(10_000);
    expect(fired).toBe(false);
    clock.setFrozen(false);
    advance(299);
    expect(fired).toBe(false);
    advance(1);
    expect(fired).toBe(true);
  });

  it('fires in due order and skips cleared timeouts', () => {
    const { clock, advance } = setup();
    const hits: number[] = [];
    clock.setTimeout(() => hits.push(2), 200);
    const id = clock.setTimeout(() => hits.push(9), 150);
    clock.setTimeout(() => hits.push(1), 100);
    clock.clearTimeout(id);
    advance(300);
    expect(hits).toEqual([1, 2]);
  });

  it('peekV reads time without firing callbacks and stops while frozen', () => {
    let now = 0;
    const clock = new VirtualClock(() => now);
    let fired = false;
    clock.setTimeout(() => (fired = true), 100);
    now = 150;
    expect(clock.peekV()).toBe(150);
    expect(fired).toBe(false);
    clock.tick();
    expect(fired).toBe(true);
    clock.setSpeed(2);
    now = 200;
    expect(clock.peekV()).toBe(250);
    clock.setFrozen(true);
    now = 400;
    expect(clock.peekV()).toBe(250);
  });
});
