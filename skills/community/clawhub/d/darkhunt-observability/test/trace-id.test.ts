import { describe, it, expect } from 'vitest';
import { traceIdFromSession, randomSpanId } from '../src/trace-id.js';

describe('traceIdFromSession', () => {
  it('returns a 32-character hex string', () => {
    const id = traceIdFromSession('test-session-123');
    expect(id).toMatch(/^[0-9a-f]{32}$/);
  });

  it('is deterministic — same input produces same output', () => {
    const a = traceIdFromSession('817998cb-4ddd-43c3-b7f2-01bae4949267');
    const b = traceIdFromSession('817998cb-4ddd-43c3-b7f2-01bae4949267');
    expect(a).toBe(b);
  });

  it('produces different IDs for different sessions', () => {
    const a = traceIdFromSession('session-aaa');
    const b = traceIdFromSession('session-bbb');
    expect(a).not.toBe(b);
  });

  it('produces different traceIds for channel message vs thread reply (known: first message is separate trace)', () => {
    // The first message in a Slack channel has no thread ID. Thread replies have one.
    // These produce different traces — the first message is a separate trace.
    // This is acceptable: the first message is one span, the real conversation is in the thread.
    const channel = traceIdFromSession('agent:darkhunt-docs:slack:channel:c0am98auquq');
    const thread = traceIdFromSession('agent:darkhunt-docs:slack:channel:c0am98auquq:thread:1773516627.786269');
    expect(channel).not.toBe(thread);
  });

  it('produces different traceIds for different channels', () => {
    const a = traceIdFromSession('agent:main:slack:channel:aaa');
    const b = traceIdFromSession('agent:main:slack:channel:bbb');
    expect(a).not.toBe(b);
  });

  it('produces same traceId for all messages in the same thread', () => {
    const a = traceIdFromSession('agent:main:slack:channel:c0am98:thread:111');
    const b = traceIdFromSession('agent:main:slack:channel:c0am98:thread:111');
    expect(a).toBe(b);
  });
});

describe('randomSpanId', () => {
  it('returns a 16-character hex string', () => {
    const id = randomSpanId();
    expect(id).toMatch(/^[0-9a-f]{16}$/);
  });

  it('produces unique values', () => {
    const ids = new Set(Array.from({ length: 100 }, () => randomSpanId()));
    expect(ids.size).toBe(100);
  });
});
