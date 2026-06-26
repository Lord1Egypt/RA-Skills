/**
 * CLI validation tests for withdraw.js
 *
 * Strategy:
 * - All tests here exercise input validation only -- the script exits before
 *   any network call, vault decryption, or SDK import.
 * - No real transactions. No --confirmed path.
 * - For preview/execution coverage, run manually: node withdraw.js <amount>
 */

import { describe, it, expect } from 'vitest';
import { spawnSync } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dir = dirname(fileURLToPath(import.meta.url));
const WITHDRAW_JS = join(__dir, '..', 'withdraw.js');

/** Run withdraw.js synchronously and return { stdout, stderr, exitCode } */
function run(args, env = {}) {
  const result = spawnSync(process.execPath, [WITHDRAW_JS, ...args], {
    env: { ...process.env, ...env },
    encoding: 'utf8',
    timeout: 10_000,
  });
  const parse = lines =>
    lines
      .trim()
      .split('\n')
      .filter(Boolean)
      .map(l => { try { return JSON.parse(l); } catch { return l; } });
  return {
    stdout: parse(result.stdout),
    stderr: parse(result.stderr),
    exitCode: result.status,
  };
}

// ---------------------------------------------------------------------------
// CLI argument validation (no network needed)
// ---------------------------------------------------------------------------

describe('CLI argument validation', () => {
  it('exits 1 with usage message when no args', () => {
    const { stderr, exitCode } = run([]);
    expect(exitCode).toBe(1);
    expect(stderr[0]).toMatchObject({ error: expect.stringContaining('Usage') });
  });

  it('exits 1 when amount is zero', () => {
    const { stderr, exitCode } = run(['0']);
    expect(exitCode).toBe(1);
    expect(stderr[0]).toMatchObject({ error: expect.stringContaining('positive') });
  });

  it('exits 1 when amount is negative', () => {
    // Negative number fails the plain-decimal regex
    const { stderr, exitCode } = run(['-5']);
    expect(exitCode).toBe(1);
    expect(stderr[0]).toMatchObject({ error: expect.stringContaining('plain decimal') });
  });

  it('exits 1 when amount is non-numeric', () => {
    const { stderr, exitCode } = run(['abc']);
    expect(exitCode).toBe(1);
    expect(stderr[0]).toMatchObject({ error: expect.stringContaining('plain decimal') });
  });

  it('exits 1 for scientific notation (1e2)', () => {
    const { stderr, exitCode } = run(['1e2']);
    expect(exitCode).toBe(1);
    expect(stderr[0]).toMatchObject({ error: expect.stringContaining('plain decimal') });
  });

  it('exits 1 for scientific notation (5E1)', () => {
    const { stderr, exitCode } = run(['5E1']);
    expect(exitCode).toBe(1);
    expect(stderr[0]).toMatchObject({ error: expect.stringContaining('plain decimal') });
  });

  it('exits 1 when amount is below 2 USDC minimum (1.5)', () => {
    const { stderr, exitCode } = run(['1.5']);
    expect(exitCode).toBe(1);
    expect(stderr[0]).toMatchObject({ error: expect.stringContaining('Minimum withdrawal') });
    expect(stderr[0].error).toContain('2 USDC');
  });

  it('exits 1 when amount is exactly 1 USDC (below minimum)', () => {
    const { stderr, exitCode } = run(['1']);
    expect(exitCode).toBe(1);
    expect(stderr[0]).toMatchObject({ error: expect.stringContaining('Minimum withdrawal') });
  });

  it('exits 1 for invalid --account value (float)', () => {
    const { stderr, exitCode } = run(['5', '--account', '1.5']);
    expect(exitCode).toBe(1);
    expect(stderr[0]).toMatchObject({ error: expect.stringContaining('non-negative integer') });
  });

  it('exits 1 for invalid --account value (negative)', () => {
    const { stderr, exitCode } = run(['5', '--account', '-1']);
    expect(exitCode).toBe(1);
    expect(stderr[0]).toMatchObject({ error: expect.stringContaining('non-negative integer') });
  });

  it('exits 1 for invalid --account value (non-numeric)', () => {
    const { stderr, exitCode } = run(['5', '--account', 'main']);
    expect(exitCode).toBe(1);
    expect(stderr[0]).toMatchObject({ error: expect.stringContaining('non-negative integer') });
  });

  it('passes validation for amount exactly at minimum (2 USDC)', () => {
    // Validation passes; script will fail later at vault/network -- not at amount check
    const { stderr, exitCode } = run(['2']);
    if (exitCode === 1) {
      expect(stderr[0].error).not.toContain('Minimum withdrawal');
      expect(stderr[0].error).not.toContain('plain decimal');
      expect(stderr[0].error).not.toContain('positive');
    }
    // exit 0 means preview succeeded (vault + HL API available) -- also acceptable
  });

  it('passes validation for integer amount (10)', () => {
    const { stderr, exitCode } = run(['10']);
    if (exitCode === 1) {
      expect(stderr[0].error).not.toContain('Minimum withdrawal');
      expect(stderr[0].error).not.toContain('plain decimal');
    }
  });

  it('passes validation for decimal amount (5.5)', () => {
    const { stderr, exitCode } = run(['5.5']);
    if (exitCode === 1) {
      expect(stderr[0].error).not.toContain('Minimum withdrawal');
      expect(stderr[0].error).not.toContain('plain decimal');
    }
  });
});
