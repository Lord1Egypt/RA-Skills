/**
 * Tests for thread-scoped session key promotion and OpenClaw hook ordering edge cases.
 *
 * These tests cover bugs discovered in production:
 * 1. agentEnd fires BEFORE llmOutput in OpenClaw's hook ordering — if the override
 *    map is cleaned up in agentEnd, llmOutput can't resolve the promoted key.
 * 2. OpenClaw loads the plugin twice (buffer.id=1 and buffer.id=3/4), sharing
 *    module-level maps — if agentStart deletes from pendingThreadIds, the second
 *    instance misses the threadId.
 * 3. Top-level channel messages need promotion from channel-level to thread-scoped
 *    session keys using threadId from message_received metadata.
 */
import { describe, it, expect, beforeEach } from 'vitest';
import { Resource } from '@opentelemetry/resources';
import type { ReadableSpan } from '@opentelemetry/sdk-trace-base';
import { SpanBuffer, clearSharedState } from '../src/span-buffer.js';
import { registerHooks, clearHooksState, resolveSessionKey, sessionKeyOverrides, type OpenClawPluginApi } from '../src/hooks-adapter.js';
import { traceIdFromSession } from '../src/trace-id.js';

const resource = new Resource({ 'service.name': 'openclaw-thread-test' });

beforeEach(() => {
  clearSharedState();
  clearHooksState();
});

function createMockApi() {
  const handlers = new Map<string, Array<(evt: any, ctx: any) => void>>();

  const api: OpenClawPluginApi = {
    on(event: string, handler: (evt: any, ctx: any) => void) {
      if (!handlers.has(event)) handlers.set(event, []);
      handlers.get(event)!.push(handler);
    },
    version: '0.3.2',
  };

  function fire(event: string, evt: any, ctx: any) {
    const list = handlers.get(event);
    if (list) {
      for (const handler of list) handler(evt, ctx);
    }
  }

  return { api, fire };
}

const CHANNEL_KEY = 'agent:darkhunt-support:slack:channel:c0a1897aj79';
const THREAD_TS = '1773597311.925529';
const THREAD_KEY = `${CHANNEL_KEY}:thread:${THREAD_TS}`;
const MODEL = 'claude-sonnet-4-6';

function makeCtx(sessionKey: string, overrides: Record<string, any> = {}) {
  return {
    agentId: 'darkhunt-support',
    sessionKey,
    sessionId: 'sess-1',
    channelId: 'slack',
    accountId: 'default',
    ...overrides,
  };
}

describe('Thread promotion: agentEnd fires before llmOutput', () => {
  it('generation span uses thread-scoped key even when agentEnd fires first', () => {
    const emitted: ReadableSpan[] = [];
    const buffer = new SpanBuffer(resource, 'full', (spans) => emitted.push(...spans));
    const { api, fire } = createMockApi();
    registerHooks(api, buffer);

    const ctx = makeCtx(CHANNEL_KEY);

    // 1. message_received — stores threadId for promotion
    fire('message_received', {
      from: 'slack:channel:C0A1897AJ79',
      content: 'Hello from the community',
      metadata: { threadId: THREAD_TS },
      timestamp: Date.now(),
    }, ctx);

    // 2. agentStart — promotes channel key to thread-scoped
    fire('before_agent_start', { from: 'slack:channel:C0A1897AJ79' }, ctx);

    // 3. llm_input
    fire('llm_input', {
      runId: 'run-1',
      sessionId: 'sess-1',
      provider: 'amazon-bedrock',
      model: MODEL,
      prompt: 'Hello from the community',
      historyMessages: [],
    }, ctx);

    // 4. agentEnd fires BEFORE llmOutput (OpenClaw's real ordering)
    fire('agent_end', {
      agentId: 'darkhunt-support',
      success: true,
      durationMs: 2000,
    }, ctx);

    // 5. llmOutput fires AFTER agentEnd
    fire('llm_output', {
      runId: 'run-1',
      sessionId: 'sess-1',
      provider: 'amazon-bedrock',
      model: MODEL,
      lastAssistant: { usage: { input: 100, output: 50, totalTokens: 150, cost: { total: 0 } } },
      usage: { input: 100, output: 50, total: 150 },
      assistantTexts: ['Hello! How can I help?'],
    }, ctx);

    // Find the generation span
    const genSpan = emitted.find(s => s.name.startsWith('generation'));
    expect(genSpan).toBeDefined();

    // traceId is derived from sessionKey — if the promoted thread-scoped key
    // was used, the traceId will match. If the channel-level key was used
    // (the bug), it will be different.
    const expectedTraceId = traceIdFromSession(THREAD_KEY);
    const channelTraceId = traceIdFromSession(CHANNEL_KEY);
    expect(expectedTraceId).not.toBe(channelTraceId); // sanity: they differ

    // The generation span MUST use the thread-scoped traceId
    expect(genSpan!.spanContext().traceId).toBe(expectedTraceId);

    // Agent span is suppressed — should NOT be emitted
    const agentSpan = emitted.find(s => s.name.startsWith('agent'));
    expect(agentSpan).toBeUndefined();
  });

  it('override persists across agentEnd so llmOutput can resolve it', () => {
    const emitted: ReadableSpan[] = [];
    const buffer = new SpanBuffer(resource, 'full', (spans) => emitted.push(...spans));
    const { api, fire } = createMockApi();
    registerHooks(api, buffer);

    const ctx = makeCtx(CHANNEL_KEY);

    fire('message_received', {
      from: 'slack:channel:C0A1897AJ79',
      content: 'test',
      metadata: { threadId: THREAD_TS },
    }, ctx);

    fire('before_agent_start', {}, ctx);

    // Verify override exists before agentEnd
    expect(resolveSessionKey(CHANNEL_KEY)).toBe(THREAD_KEY);

    fire('agent_end', { success: true, durationMs: 1000 }, ctx);

    // Override MUST still exist after agentEnd
    expect(resolveSessionKey(CHANNEL_KEY)).toBe(THREAD_KEY);
  });
});

describe('Thread promotion: dual plugin instances', () => {
  it('second plugin instance can still resolve threadId after first instance runs agentStart', () => {
    const emitted1: ReadableSpan[] = [];
    const emitted2: ReadableSpan[] = [];
    const buffer1 = new SpanBuffer(resource, 'full', (spans) => emitted1.push(...spans));
    const buffer2 = new SpanBuffer(resource, 'full', (spans) => emitted2.push(...spans));
    const { api: api1, fire: fire1 } = createMockApi();
    const { api: api2, fire: fire2 } = createMockApi();

    // Register hooks on both instances (simulates dual plugin loading)
    registerHooks(api1, buffer1);
    registerHooks(api2, buffer2);

    const ctx = makeCtx(CHANNEL_KEY);

    // message_received fires on both instances — stores pendingThreadId
    fire1('message_received', {
      from: 'slack:channel:C0A1897AJ79',
      content: 'Hello',
      metadata: { threadId: THREAD_TS },
    }, ctx);
    fire2('message_received', {
      from: 'slack:channel:C0A1897AJ79',
      content: 'Hello',
      metadata: { threadId: THREAD_TS },
    }, ctx);

    // agentStart fires on instance 1 first — should NOT consume the threadId
    fire1('before_agent_start', { from: 'slack:channel:C0A1897AJ79' }, ctx);

    // agentStart fires on instance 2 — must ALSO be able to promote
    fire2('before_agent_start', { from: 'slack:channel:C0A1897AJ79' }, ctx);

    // Both should resolve to thread-scoped key
    expect(resolveSessionKey(CHANNEL_KEY)).toBe(THREAD_KEY);

    // Fire llm_input + llm_output on both to produce generation spans
    const llmInput = {
      runId: 'run-1', sessionId: 'sess-1',
      provider: 'amazon-bedrock', model: MODEL,
      prompt: 'Hello', historyMessages: [],
    };
    const llmOutput = {
      runId: 'run-1', sessionId: 'sess-1',
      provider: 'amazon-bedrock', model: MODEL,
      lastAssistant: { usage: { input: 10, output: 5, totalTokens: 15, cost: { total: 0 } } },
      usage: { input: 10, output: 5, total: 15 },
      assistantTexts: ['Hi!'],
    };

    fire1('llm_input', llmInput, ctx);
    fire1('llm_output', llmOutput, ctx);
    fire2('llm_input', llmInput, ctx);
    fire2('llm_output', llmOutput, ctx);

    // Both instances should produce generation spans with the thread-scoped traceId
    const expectedTraceId = traceIdFromSession(THREAD_KEY);

    const gen1 = emitted1.find(s => s.name.startsWith('generation'));
    const gen2 = emitted2.find(s => s.name.startsWith('generation'));
    expect(gen1).toBeDefined();
    expect(gen2).toBeDefined();
    expect(gen1!.spanContext().traceId).toBe(expectedTraceId);
    expect(gen2!.spanContext().traceId).toBe(expectedTraceId);
  });
});

describe('Thread promotion: channel-level key promotion', () => {
  it('promotes channel-level key to thread-scoped when threadId is in metadata', () => {
    const emitted: ReadableSpan[] = [];
    const buffer = new SpanBuffer(resource, 'full', (spans) => emitted.push(...spans));
    const { api, fire } = createMockApi();
    registerHooks(api, buffer);

    const ctx = makeCtx(CHANNEL_KEY);

    // message_received with threadId but channel-level sessionKey
    fire('message_received', {
      from: 'slack:channel:C0A1897AJ79',
      content: 'First message in channel',
      metadata: { threadId: THREAD_TS },
    }, ctx);

    // agentStart should promote the key
    fire('before_agent_start', {}, ctx);

    expect(resolveSessionKey(CHANNEL_KEY)).toBe(THREAD_KEY);
  });

  it('does not promote key that already has :thread: suffix', () => {
    const emitted: ReadableSpan[] = [];
    const buffer = new SpanBuffer(resource, 'full', (spans) => emitted.push(...spans));
    const { api, fire } = createMockApi();
    registerHooks(api, buffer);

    // sessionKey already has thread — should not be modified
    const ctx = makeCtx(THREAD_KEY);

    fire('message_received', {
      from: 'slack:channel:C0A1897AJ79',
      content: 'Follow-up in thread',
      metadata: { threadId: THREAD_TS },
    }, ctx);

    fire('before_agent_start', {}, ctx);

    // Should not create an override — key is already thread-scoped
    expect(sessionKeyOverrides.has(THREAD_KEY)).toBe(false);
    expect(resolveSessionKey(THREAD_KEY)).toBe(THREAD_KEY);
  });

  it('message_received with no threadId does not promote', () => {
    const emitted: ReadableSpan[] = [];
    const buffer = new SpanBuffer(resource, 'full', (spans) => emitted.push(...spans));
    const { api, fire } = createMockApi();
    registerHooks(api, buffer);

    const ctx = makeCtx(CHANNEL_KEY);

    // No threadId in metadata
    fire('message_received', {
      from: 'slack:channel:C0A1897AJ79',
      content: 'Message without thread',
    }, ctx);

    fire('before_agent_start', {}, ctx);

    // No promotion should happen
    expect(resolveSessionKey(CHANNEL_KEY)).toBe(CHANNEL_KEY);
  });

  it('all hooks in a full lifecycle use the promoted thread-scoped key', () => {
    const emitted: ReadableSpan[] = [];
    const buffer = new SpanBuffer(resource, 'full', (spans) => emitted.push(...spans));
    const { api, fire } = createMockApi();
    registerHooks(api, buffer);

    const ctx = makeCtx(CHANNEL_KEY);

    // Full lifecycle with OpenClaw's REAL hook ordering:
    // message_received → agentStart → llmInput → toolStart → toolEnd → llmInput → agentEnd → llmOutput
    fire('message_received', {
      from: 'slack:channel:C0A1897AJ79',
      content: 'Search for docs',
      metadata: { threadId: THREAD_TS },
    }, ctx);

    fire('before_agent_start', { from: 'slack:channel:C0A1897AJ79' }, ctx);

    fire('llm_input', {
      runId: 'run-1', sessionId: 'sess-1',
      provider: 'amazon-bedrock', model: MODEL,
      prompt: 'Search for docs', historyMessages: [],
    }, ctx);

    fire('before_tool_call', {
      toolName: 'memory_search',
      toolCallId: 'tool-1',
      params: { query: 'docs' },
    }, ctx);

    fire('after_tool_call', {
      toolName: 'memory_search',
      toolCallId: 'tool-1',
      success: true,
      result: 'Found 3 results',
      durationMs: 150,
    }, ctx);

    // Second LLM call after tool result
    fire('llm_input', {
      runId: 'run-2', sessionId: 'sess-1',
      provider: 'amazon-bedrock', model: MODEL,
      prompt: 'Search for docs',
      historyMessages: [
        { role: 'assistant', content: [{ type: 'tool_use', id: 'tool-1', name: 'memory_search', input: { query: 'docs' } }] },
        { role: 'user', content: [{ type: 'tool_result', tool_use_id: 'tool-1', content: 'Found 3 results' }] },
      ],
    }, ctx);

    // agentEnd fires BEFORE llmOutput
    fire('agent_end', { success: true, durationMs: 3000 }, ctx);

    // llmOutput fires AFTER agentEnd
    fire('llm_output', {
      runId: 'run-2', sessionId: 'sess-1',
      provider: 'amazon-bedrock', model: MODEL,
      lastAssistant: { usage: { input: 200, output: 100, totalTokens: 300, cost: { total: 0 } } },
      usage: { input: 200, output: 100, total: 300 },
      assistantTexts: ['Here are the docs...'],
    }, ctx);

    // ALL emitted spans should share the same thread-scoped traceId
    // (agent spans are suppressed, so only generation + tool spans)
    const expectedTraceId = traceIdFromSession(THREAD_KEY);
    const spansWithTrace = emitted.filter(s =>
      s.name.startsWith('generation') ||
      s.name.startsWith('tool ')
    );

    // Agent span is suppressed — should NOT be emitted
    const agentSpan = emitted.find(s => s.name.startsWith('agent'));
    expect(agentSpan).toBeUndefined();

    // At least 1 generation span (+ possibly tool span depending on flush path)
    expect(spansWithTrace.length).toBeGreaterThanOrEqual(1);
    for (const span of spansWithTrace) {
      expect(span.spanContext().traceId).toBe(expectedTraceId);
    }
  });

  it('new message on same channel replaces stale override from previous message', () => {
    const emitted: ReadableSpan[] = [];
    const buffer = new SpanBuffer(resource, 'full', (spans) => emitted.push(...spans));
    const { api, fire } = createMockApi();
    registerHooks(api, buffer);

    const ctx = makeCtx(CHANNEL_KEY);
    const OLD_THREAD = '1773677636.750389';
    const NEW_THREAD = '1773739659.379219';

    // --- First message: creates override to old thread ---
    fire('message_received', {
      from: 'slack:channel:C0A1897AJ79',
      content: 'First message',
      metadata: { threadId: OLD_THREAD },
    }, ctx);
    fire('before_agent_start', {}, ctx);
    expect(resolveSessionKey(CHANNEL_KEY)).toBe(`${CHANNEL_KEY}:thread:${OLD_THREAD}`);

    fire('llm_input', {
      runId: 'run-1', sessionId: 'sess-1',
      provider: 'amazon-bedrock', model: MODEL,
      prompt: 'First message', historyMessages: [],
    }, ctx);
    fire('agent_end', { success: true, durationMs: 1000 }, ctx);
    fire('llm_output', {
      runId: 'run-1', sessionId: 'sess-1',
      provider: 'amazon-bedrock', model: MODEL,
      lastAssistant: { usage: { input: 10, output: 5, totalTokens: 15, cost: { total: 0 } } },
      usage: { input: 10, output: 5, total: 15 },
      assistantTexts: ['Reply 1'],
    }, ctx);

    // Override still points to old thread
    expect(resolveSessionKey(CHANNEL_KEY)).toBe(`${CHANNEL_KEY}:thread:${OLD_THREAD}`);

    const countAfterMsg1 = emitted.length;

    // --- Second message: new thread on same channel ---
    fire('message_received', {
      from: 'slack:channel:C0A1897AJ79',
      content: 'Second message',
      metadata: { threadId: NEW_THREAD },
    }, ctx);
    fire('before_agent_start', {}, ctx);

    // Override MUST now point to new thread, not stale old one
    expect(resolveSessionKey(CHANNEL_KEY)).toBe(`${CHANNEL_KEY}:thread:${NEW_THREAD}`);

    fire('llm_input', {
      runId: 'run-2', sessionId: 'sess-1',
      provider: 'amazon-bedrock', model: MODEL,
      prompt: 'Second message', historyMessages: [],
    }, ctx);
    fire('agent_end', { success: true, durationMs: 1000 }, ctx);
    fire('llm_output', {
      runId: 'run-2', sessionId: 'sess-1',
      provider: 'amazon-bedrock', model: MODEL,
      lastAssistant: { usage: { input: 10, output: 5, totalTokens: 15, cost: { total: 0 } } },
      usage: { input: 10, output: 5, total: 15 },
      assistantTexts: ['Reply 2'],
    }, ctx);

    // Second message's spans must use the NEW thread's traceId
    const expectedTraceId = traceIdFromSession(`${CHANNEL_KEY}:thread:${NEW_THREAD}`);
    const oldTraceId = traceIdFromSession(`${CHANNEL_KEY}:thread:${OLD_THREAD}`);
    expect(expectedTraceId).not.toBe(oldTraceId);

    const newSpans = emitted.slice(countAfterMsg1);
    const genSpan = newSpans.find(s => s.name.startsWith('generation'));
    expect(genSpan).toBeDefined();
    expect(genSpan!.spanContext().traceId).toBe(expectedTraceId);
  });
});
