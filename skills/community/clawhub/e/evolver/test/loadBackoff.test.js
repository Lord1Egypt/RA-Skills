'use strict';

const { describe, it, before, after } = require('node:test');
const assert = require('node:assert/strict');
const os = require('os');

const evolve = require('../src/evolve');

describe('load backoff hardening (#446 Android/Termux 0 CPU)', () => {
  const origCpus = os.cpus;
  const origLoadavg = os.loadavg;
  after(() => {
    os.cpus = origCpus;
    os.loadavg = origLoadavg;
  });

  it('detectCpuCount falls back to MIN_ASSUMED_CPU_COUNT when os.cpus() returns []', () => {
    os.cpus = () => [];
    const n = evolve.detectCpuCount();
    assert.ok(n >= 4, 'empty os.cpus() must not produce 0 cores, got ' + n);
  });

  it('detectCpuCount falls back when os.cpus() throws', () => {
    os.cpus = () => { throw new Error('ENOSYS /proc/cpuinfo'); };
    const n = evolve.detectCpuCount();
    assert.ok(n >= 4, 'throwing os.cpus() must not produce 0 cores, got ' + n);
  });

  it('detectCpuCount returns real count when available', () => {
    os.cpus = () => [{}, {}, {}];
    assert.equal(evolve.detectCpuCount(), 3);
  });

  it('getDefaultLoadMax never returns 0.0 on Android-like environments', () => {
    os.cpus = () => [];
    const max = evolve.getDefaultLoadMax();
    assert.ok(max > 0, 'default load max must be > 0 even when cpus() is empty, got ' + max);
    assert.ok(max >= 0.9, 'default load max must be at least 0.9, got ' + max);
  });

  it('getSystemLoad clamps runaway loadavg to 2x the assumed core count', () => {
    os.cpus = () => [];
    os.loadavg = () => [29.29, 29.36, 29.38];
    const load = evolve.getSystemLoad();
    assert.ok(load.load1m <= 8, 'load1m must be clamped to <= 2*4=8, got ' + load.load1m);
    assert.ok(load.load5m <= 8);
    assert.ok(load.load15m <= 8);
  });

  it('getSystemLoad preserves normal loadavg values on a healthy host', { skip: process.platform === 'win32' ? 'getSystemLoad routes Windows through _sampleWindowsCpuLoad() (process.cpuUsage delta) instead of os.loadavg, because Win32 returns [0,0,0] there. The os.loadavg mock this test installs is therefore bypassed and the assertion compares the CPU-sample fallback against 0.5. The Windows code path has its own semantics that need a separate test mocking process.cpuUsage + Date.now, not this one.' : false }, () => {
    os.cpus = () => new Array(8).fill({});
    os.loadavg = () => [0.5, 0.7, 0.9];
    const load = evolve.getSystemLoad();
    assert.equal(load.load1m, 0.5);
    assert.equal(load.load5m, 0.7);
    assert.equal(load.load15m, 0.9);
  });

  it('regression: Android/Termux [29.29, 29.36, 29.38] + 0 cores no longer forces permanent backoff', () => {
    os.cpus = () => [];
    os.loadavg = () => [29.29, 29.36, 29.38];
    const load = evolve.getSystemLoad();
    const max = evolve.getDefaultLoadMax();
    // Before the fix: max=0, load1m=29.29 -> backoff forever.
    // After the fix: max>=3.6 and load1m is clamped, so the backoff decision
    // is now driven by real overload, not by a misreported CPU count.
    assert.ok(max > 0, 'load max must be positive');
    assert.ok(load.load1m <= max * 2.5, 'clamped load must not stay orders of magnitude above max');
  });
});
