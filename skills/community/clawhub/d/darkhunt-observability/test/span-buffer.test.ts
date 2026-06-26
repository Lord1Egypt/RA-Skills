import { describe, it, expect, vi, beforeEach } from 'vitest';
import { SpanStatusCode } from '@opentelemetry/api';
import { Resource } from '@opentelemetry/resources';
import type { ReadableSpan } from '@opentelemetry/sdk-trace-base';
import { SpanBuffer, clearSharedState } from '../src/span-buffer.js';
import { traceIdFromSession } from '../src/trace-id.js';

const resource = new Resource({ 'service.name': 'openclaw' });

// Clear shared module-level state between tests to prevent leaking
beforeEach(() => clearSharedState());

function createBuffer(mode: 'metadata' | 'debug' | 'full' = 'metadata') {
  const emitted: ReadableSpan[] = [];
  const buffer = new SpanBuffer(resource, mode, (spans) => emitted.push(...spans));
  return { buffer, emitted };
}

describe('SpanBuffer', () => {
  describe('message.in', () => {
    it('immediately emits a message span', () => {
      const { buffer, emitted } = createBuffer();

      buffer.onMessageIn({
        sessionId: 'sess-1',
        sessionKey: 'agent:main:telegram:direct:123',
        channel: 'telegram',
        from: 'telegram:123',
        contentLength: 24,
        ts: 1000,
      });

      expect(emitted).toHaveLength(1);
      expect(emitted[0].name).toBe('message.in telegram');
      expect(emitted[0].attributes['openclaw.observation.type']).toBe('event');
    });
  });

  describe('agent lifecycle', () => {
    it('buffers agent start and cleans up on end (agent span suppressed)', () => {
      const { buffer, emitted } = createBuffer();

      buffer.onAgentStart({
        sessionId: 'sess-1',
        sessionKey: 'agent:main:telegram:direct:123',
        agentId: 'main',
        traceName: 'test',
        ts: 1000,
      });

      expect(emitted).toHaveLength(0);

      buffer.onAgentEnd({
        sessionKey: 'agent:main:telegram:direct:123',
        agentId: 'main',
        success: true,
        durationMs: 5000,
        ts: 6000,
      });

      // Agent span is suppressed — nothing emitted
      expect(emitted).toHaveLength(0);

      // Verify cleanup: the buffered agent should be removed
      const stats = buffer.getStats();
      expect(stats.agents).toBe(0);
    });
  });

  describe('full agent turn with tools', () => {
    it('produces correct span hierarchy with tool results', () => {
      const { buffer, emitted } = createBuffer('full');
      const sessionKey = 'agent:main:telegram:direct:123';

      // 1. message.in
      buffer.onMessageIn({
        sessionId: 'sess-1',
        sessionKey,
        channel: 'telegram',
        from: 'telegram:123',
        contentLength: 24,
        ts: 1000,
      });

      // 2. agent.start
      buffer.onAgentStart({
        sessionId: 'sess-1',
        sessionKey,
        agentId: 'main',
        traceName: 'find files',
        traceTags: ['telegram'],
        channel: 'telegram',
        ts: 1100,
      });

      // 3. llm.input
      buffer.onLlmInput({
        sessionId: 'sess-1',
        sessionKey,
        agentId: 'main',
        model: 'claude-opus-4-6',
        provider: 'anthropic',
        runId: 'run-1',
        input: 'find files',
        inputLength: 10,
        ts: 1200,
      });

      // 4. llm.output (with tool_use decision)
      buffer.onLlmOutput({
        sessionKey,
        runId: 'run-1',
        model: 'claude-opus-4-6',
        provider: 'anthropic',
        output: 'I will use Bash to find files.',
        outputLength: 30,
        stopReason: 'tool_use',
        inputTokens: 1,
        outputTokens: 42,
        ts: 5200,
      });

      // 5. tool.start
      buffer.onToolStart({
        sessionKey,
        agentId: 'main',
        toolName: 'Bash',
        toolCallId: 'toolu_01',
        parameters: '{"bash_command":"find"}',
        ts: 5300,
      });

      // 6. tool.end (with durationMs)
      buffer.onToolEnd({
        sessionKey,
        toolName: 'Bash',
        toolCallId: 'toolu_01',
        success: true,
        durationMs: 124,
        ts: 5424,
      });

      // Tool is now completed but held, awaiting result from next llm_input.
      // Spans so far: message + generation (conversation events are suppressed)
      expect(emitted.length).toBeGreaterThanOrEqual(2);

      // 7. llm.input (second call — includes tool result in history)
      // Simulate applyToolResults as the hooks-adapter would do
      const toolResults = new Map([['toolu_01', 'file1.ts\nfile2.ts\nfile3.ts']]);
      buffer.applyToolResults(toolResults, sessionKey);

      // Tool span should now be emitted with result
      const toolSpanEmitted = emitted.find(s => s.attributes['openclaw.observation.type'] === 'tool');
      expect(toolSpanEmitted).toBeDefined();
      expect(toolSpanEmitted!.attributes['openclaw.observation.output']).toBeDefined();

      buffer.onLlmInput({
        sessionId: 'sess-1',
        sessionKey,
        agentId: 'main',
        model: 'claude-opus-4-6',
        provider: 'anthropic',
        runId: 'run-2',
        input: '[tool result]',
        inputLength: 13,
        ts: 5500,
      });

      // 8. llm.output
      buffer.onLlmOutput({
        sessionKey,
        runId: 'run-2',
        model: 'claude-opus-4-6',
        provider: 'anthropic',
        output: 'Found 3 files.',
        outputLength: 14,
        stopReason: 'stop',
        inputTokens: 3,
        outputTokens: 85,
        ts: 18800,
      });

      // 9. agent.end
      buffer.onAgentEnd({
        sessionKey,
        agentId: 'main',
        success: true,
        durationMs: 17741,
        ts: 18841,
      });

      // Verify required span types exist (agent span is suppressed)
      const messageSpan = emitted.find(s => s.name.startsWith('message.in'))!;
      const gens = emitted.filter(s => s.name.startsWith('generation'));
      expect(gens).toHaveLength(2);
      const gen1 = gens[0];
      const gen2 = gens[1];
      const toolSpan = emitted.find(s => s.attributes['openclaw.observation.type'] === 'tool')!;
      expect(messageSpan).toBeDefined();

      // Agent span is suppressed — should NOT be emitted
      const agentSpan = emitted.find(s => s.name.startsWith('agent'));
      expect(agentSpan).toBeUndefined();

      // Conversation events are suppressed — should NOT be emitted
      const convSpans = emitted.filter(s => s.name.startsWith('conversation.'));
      expect(convSpans).toHaveLength(0);

      // All share same traceId (derived from sessionKey, not sessionId)
      const traceId = traceIdFromSession(sessionKey);
      expect(messageSpan.spanContext().traceId).toBe(traceId);
      expect(gen1.spanContext().traceId).toBe(traceId);
      expect(toolSpan.spanContext().traceId).toBe(traceId);
      expect(gen2.spanContext().traceId).toBe(traceId);

      // Correct span types
      expect(messageSpan.attributes['openclaw.observation.type']).toBe('event');
      expect(gen1.attributes['openclaw.observation.type']).toBe('generation');
      expect(toolSpan.attributes['openclaw.observation.type']).toBe('tool');
      expect(gen2.attributes['openclaw.observation.type']).toBe('generation');
    });
  });

  describe('concurrent session isolation', () => {
    it('isolates spans from interleaved sessions', () => {
      const { buffer, emitted } = createBuffer();

      const sk1 = 'agent:main:telegram:direct:111';
      const sk2 = 'agent:bot2:webchat:group:222';

      // Session 1 agent start
      buffer.onAgentStart({
        sessionId: 'sess-A',
        sessionKey: sk1,
        agentId: 'main',
        ts: 1000,
      });

      // Session 2 agent start (interleaved)
      buffer.onAgentStart({
        sessionId: 'sess-B',
        sessionKey: sk2,
        agentId: 'bot2',
        ts: 1050,
      });

      // Session 1 llm.input
      buffer.onLlmInput({
        sessionId: 'sess-A',
        sessionKey: sk1,
        agentId: 'main',
        model: 'claude-opus-4-6',
        provider: 'anthropic',
        runId: 'run-A1',
        ts: 1100,
      });

      // Session 2 llm.input
      buffer.onLlmInput({
        sessionId: 'sess-B',
        sessionKey: sk2,
        agentId: 'bot2',
        model: 'gpt-4',
        provider: 'openai',
        runId: 'run-B1',
        ts: 1150,
      });

      // Session 2 llm.output (finishes first)
      buffer.onLlmOutput({
        sessionKey: sk2,
        runId: 'run-B1',
        model: 'gpt-4',
        provider: 'openai',
        inputTokens: 100,
        outputTokens: 50,
        ts: 3000,
      });

      // Session 1 llm.output
      buffer.onLlmOutput({
        sessionKey: sk1,
        runId: 'run-A1',
        model: 'claude-opus-4-6',
        provider: 'anthropic',
        inputTokens: 200,
        outputTokens: 80,
        ts: 4000,
      });

      // Session 2 agent end
      buffer.onAgentEnd({
        sessionKey: sk2,
        agentId: 'bot2',
        success: true,
        durationMs: 2000,
        ts: 3050,
      });

      // Session 1 agent end
      buffer.onAgentEnd({
        sessionKey: sk1,
        agentId: 'main',
        success: true,
        durationMs: 3100,
        ts: 4100,
      });

      // 2 gen spans only (agent spans are suppressed)
      expect(emitted).toHaveLength(2);

      // Verify isolation: session spans have traceId from sessionKey (not sessionId)
      const traceA = traceIdFromSession(sk1);
      const traceB = traceIdFromSession(sk2);

      const sessionASpans = emitted.filter(s => s.spanContext().traceId === traceA);
      const sessionBSpans = emitted.filter(s => s.spanContext().traceId === traceB);

      expect(sessionASpans).toHaveLength(1); // 1 gen (agent suppressed)
      expect(sessionBSpans).toHaveLength(1); // 1 gen (agent suppressed)

      // Verify models are correct (no cross-contamination)
      const genA = sessionASpans.find(s => s.attributes['openclaw.observation.type'] === 'generation')!;
      const genB = sessionBSpans.find(s => s.attributes['openclaw.observation.type'] === 'generation')!;
      expect(genA.attributes['gen_ai.request.model']).toBe('claude-opus-4-6');
      expect(genB.attributes['gen_ai.request.model']).toBe('gpt-4');
    });
  });

  describe('dual tool.end deduplication', () => {
    it('emits only on the tool.end with durationMs (on agentEnd flush)', () => {
      const { buffer, emitted } = createBuffer();
      const sk = 'agent:main:telegram:direct:123';

      buffer.onAgentStart({
        sessionId: 'sess-1',
        sessionKey: sk,
        agentId: 'main',
        ts: 1000,
      });

      buffer.onToolStart({
        sessionKey: sk,
        agentId: 'main',
        toolName: 'exec',
        toolCallId: 'tc-1',
        ts: 1100,
      });

      // First tool.end (no durationMs)
      buffer.onToolEnd({
        sessionKey: sk,
        toolName: 'exec',
        toolCallId: 'tc-1',
        success: true,
        ts: 1200,
      });

      expect(emitted).toHaveLength(0);

      // Second tool.end (with durationMs) — tool is completed but held
      buffer.onToolEnd({
        sessionKey: sk,
        toolName: 'exec',
        toolCallId: 'tc-1',
        success: true,
        durationMs: 100,
        ts: 1200,
      });

      // Tool is in completedTools, not emitted yet
      expect(emitted).toHaveLength(0);

      // agentEnd flushes the completed tool (but agent span is suppressed)
      buffer.onAgentEnd({
        sessionKey: sk,
        agentId: 'main',
        success: true,
        durationMs: 300,
        ts: 1300,
      });

      // Tool span only (agent span is suppressed)
      expect(emitted).toHaveLength(1);
      expect(emitted[0].name).toBe('exec');
      expect(emitted[0].attributes['openclaw.observation.type']).toBe('tool');
    });

    it('emits tool with result when applyToolResults is called', () => {
      const { buffer, emitted } = createBuffer('full');
      const sk = 'agent:main:telegram:direct:123';

      buffer.onAgentStart({
        sessionId: 'sess-1',
        sessionKey: sk,
        agentId: 'main',
        ts: 1000,
      });

      buffer.onToolStart({
        sessionKey: sk,
        agentId: 'main',
        toolName: 'exec',
        toolCallId: 'tc-1',
        ts: 1100,
      });

      buffer.onToolEnd({
        sessionKey: sk,
        toolName: 'exec',
        toolCallId: 'tc-1',
        success: true,
        durationMs: 100,
        ts: 1200,
      });

      expect(emitted).toHaveLength(0);

      // Simulate tool result from historyMessages
      const results = new Map([['tc-1', 'command output here']]);
      buffer.applyToolResults(results, sk);

      expect(emitted).toHaveLength(1);
      expect(emitted[0].name).toBe('exec');
      expect(emitted[0].attributes['openclaw.observation.output']).toContain('command output here');
    });
  });

  describe('runtime event integration', () => {
    it('stores runId from lifecycle start (agent span suppressed, runId available for generation spans)', () => {
      const { buffer, emitted } = createBuffer();
      const sk = 'agent:main:main';

      // Runtime lifecycle start arrives before hook
      buffer.onRuntimeEvent({
        runId: 'f4d0683a-1c8a-4f40-a75f-be67afecf285',
        stream: 'lifecycle',
        data: { phase: 'start', startedAt: 1000 },
        sessionKey: sk,
        ts: 1000,
      });

      buffer.onAgentStart({ sessionId: 'sess-1', sessionKey: sk, agentId: 'main', ts: 1000 });
      buffer.onAgentEnd({ sessionKey: sk, agentId: 'main', success: true, durationMs: 5000, ts: 6000 });

      // Agent span is suppressed — nothing emitted
      expect(emitted).toHaveLength(0);

      // Verify cleanup happened (agent was removed)
      const stats = buffer.getStats();
      expect(stats.agents).toBe(0);
    });

    it('stores runId even if lifecycle start arrives after agent start (agent span suppressed)', () => {
      const { buffer, emitted } = createBuffer();
      const sk = 'agent:main:main';

      // Hook fires first
      buffer.onAgentStart({ sessionId: 'sess-1', sessionKey: sk, agentId: 'main', ts: 1000 });

      // Runtime event arrives slightly later
      buffer.onRuntimeEvent({
        runId: 'run-abc',
        stream: 'lifecycle',
        data: { phase: 'start', startedAt: 1000 },
        sessionKey: sk,
        ts: 1000,
      });

      buffer.onAgentEnd({ sessionKey: sk, agentId: 'main', success: true, durationMs: 5000, ts: 6000 });

      // Agent span is suppressed — nothing emitted
      expect(emitted).toHaveLength(0);

      // Verify cleanup happened
      const stats = buffer.getStats();
      expect(stats.agents).toBe(0);
    });

    it('attaches tool meta from runtime tool result event', () => {
      const { buffer, emitted } = createBuffer('full');
      const sk = 'agent:main:main';

      buffer.onAgentStart({ sessionId: 'sess-1', sessionKey: sk, agentId: 'main', ts: 1000 });

      // Runtime tool result with meta
      buffer.onRuntimeEvent({
        runId: 'run-1',
        stream: 'tool',
        data: { phase: 'result', toolCallId: 'toolu_01', name: 'exec', meta: 'run openclaw cron -> search "notion"' },
        sessionKey: sk,
        ts: 1200,
      });

      buffer.onToolStart({ sessionKey: sk, agentId: 'main', toolName: 'exec', toolCallId: 'toolu_01', ts: 1100 });
      buffer.onToolEnd({ sessionKey: sk, toolName: 'exec', toolCallId: 'toolu_01', success: true, durationMs: 100, ts: 1200 });

      // Flush via agentEnd
      buffer.onAgentEnd({ sessionKey: sk, agentId: 'main', success: true, durationMs: 1000, ts: 2000 });

      const toolSpan = emitted.find(s => s.attributes['openclaw.observation.type'] === 'tool');
      expect(toolSpan).toBeDefined();
      expect(toolSpan!.attributes['openclaw.tool.meta']).toBe('run openclaw cron -> search "notion"');
    });

    it('records first-token TTFT from assistant stream event', () => {
      const { buffer, emitted } = createBuffer('full');
      const sk = 'agent:main:main';

      // Store runId for this session
      buffer.onRuntimeEvent({
        runId: 'run-x',
        stream: 'lifecycle',
        data: { phase: 'start', startedAt: 1000 },
        sessionKey: sk,
        ts: 1000,
      });

      buffer.onAgentStart({ sessionId: 'sess-1', sessionKey: sk, agentId: 'main', ts: 1000 });
      buffer.onLlmInput({
        sessionId: 'sess-1', sessionKey: sk, agentId: 'main',
        model: 'claude-opus-4-6', provider: 'anthropic', runId: 'llm-run-1', ts: 1100,
      });

      // First assistant token at ts=1500 (400ms after llm_input at 1100)
      buffer.onRuntimeEvent({
        runId: 'run-x',
        stream: 'assistant',
        data: { text: 'H', delta: 'H' },
        sessionKey: sk,
        ts: 1500,
      });

      // Second token — should NOT overwrite first
      buffer.onRuntimeEvent({
        runId: 'run-x',
        stream: 'assistant',
        data: { text: 'He', delta: 'e' },
        sessionKey: sk,
        ts: 1510,
      });

      buffer.onLlmOutput({
        sessionKey: sk, runId: 'llm-run-1',
        model: 'claude-opus-4-6', provider: 'anthropic',
        output: 'Hello', outputLength: 5, inputTokens: 10, outputTokens: 5, ts: 2000,
      });

      const genSpan = emitted.find(s => s.attributes['openclaw.observation.type'] === 'generation');
      expect(genSpan).toBeDefined();
      // TTFT should be ~400ms (1500 - 1100)
      expect(genSpan!.attributes['openclaw.timing.time_to_first_token_ms']).toBe(400);
    });
  });

  describe('orphan cleanup', () => {
    it('flushes stale buffered agents with error status', () => {
      const { buffer, emitted } = createBuffer();

      buffer.onAgentStart({
        sessionId: 'sess-1',
        sessionKey: 'agent:main:telegram:direct:123',
        agentId: 'main',
        ts: Date.now() - 400_000, // 400s ago
      });

      buffer.flushStale(300_000); // 5 min threshold

      expect(emitted).toHaveLength(1);
      expect(emitted[0].status.code).toBe(SpanStatusCode.ERROR);
      expect(emitted[0].status.message).toBe('span timed out without end event');
    });

    it('does not flush recent buffered agents', () => {
      const { buffer, emitted } = createBuffer();

      buffer.onAgentStart({
        sessionId: 'sess-1',
        sessionKey: 'agent:main:telegram:direct:123',
        agentId: 'main',
        ts: Date.now() - 1000, // 1s ago
      });

      buffer.flushStale(300_000);

      expect(emitted).toHaveLength(0);
    });
  });

  describe('conversation events are suppressed', () => {
    const sessionKey = 'agent:darkhunt-docs:slack:channel:c0am98auquq:thread:123';

    function setupAgent(buffer: SpanBuffer) {
      buffer.onAgentStart({
        sessionId: 'sess-1',
        sessionKey,
        agentId: 'darkhunt-docs',
        traceName: 'test',
        ts: 1000,
      });
    }

    it('does not emit conversation events from history messages', () => {
      const { buffer, emitted } = createBuffer('full');
      setupAgent(buffer);
      emitted.length = 0;

      buffer.onLlmInput({
        sessionId: 'sess-1',
        sessionKey,
        agentId: 'darkhunt-docs',
        model: 'claude-sonnet-4-6',
        provider: 'anthropic',
        runId: 'run-1',
        input: 'Tell me about competitors.',
        historyMessages: [
          { role: 'user', content: 'What is DarkHunt?' },
          { role: 'assistant', content: 'DarkHunt is an AI security platform.' },
        ],
        ts: 4000,
      });

      // Conversation events are suppressed — none should be emitted
      const convEvents = emitted.filter(s => s.name.startsWith('conversation.'));
      expect(convEvents).toHaveLength(0);

      buffer.onLlmOutput({
        sessionKey, runId: 'run-1', model: 'claude-sonnet-4-6', provider: 'anthropic',
        output: 'Key competitors include...', outputLength: 25,
        inputTokens: 30, outputTokens: 50, ts: 5000,
      });

      // Generation span is still emitted
      const genSpan = emitted.find(s => s.name.startsWith('generation'));
      expect(genSpan).toBeDefined();

      // No conversation events after llm output either
      const allConvEvents = emitted.filter(s => s.name.startsWith('conversation.'));
      expect(allConvEvents).toHaveLength(0);
    });

    it('does not emit conversation events even with tool/tool_result in history', () => {
      const { buffer, emitted } = createBuffer('full');
      setupAgent(buffer);
      emitted.length = 0;

      buffer.onLlmInput({
        sessionId: 'sess-1',
        sessionKey,
        agentId: 'darkhunt-docs',
        model: 'claude-sonnet-4-6',
        provider: 'anthropic',
        runId: 'run-1',
        input: 'flat prompt',
        historyMessages: [
          { role: 'user', content: 'Search for files.' },
          { role: 'assistant', content: 'Let me search.' },
          { role: 'tool', content: 'Found 3 files.', name: 'Glob' },
          { role: 'tool_result', content: 'file1.ts, file2.ts' },
          { role: 'user', content: 'Read the first one.' },
        ],
        ts: 2000,
      });

      const convEvents = emitted.filter(s => s.name.startsWith('conversation.'));
      expect(convEvents).toHaveLength(0);
    });

    it('still emits generation span with flat prompt fallback when historyMessages is undefined', () => {
      const { buffer, emitted } = createBuffer('full');
      setupAgent(buffer);
      emitted.length = 0;

      buffer.onLlmInput({
        sessionId: 'sess-1',
        sessionKey,
        agentId: 'darkhunt-docs',
        model: 'claude-sonnet-4-6',
        provider: 'anthropic',
        runId: 'run-1',
        input: 'System: [timestamp] what tools do you have',
        ts: 2000,
      });

      // No conversation events
      const convEvents = emitted.filter(s => s.name.startsWith('conversation.'));
      expect(convEvents).toHaveLength(0);

      buffer.onLlmOutput({
        sessionKey,
        runId: 'run-1',
        model: 'claude-sonnet-4-6',
        provider: 'anthropic',
        output: 'Here are the tools...',
        outputLength: 20,
        inputTokens: 10,
        outputTokens: 15,
        ts: 3000,
      });

      // Generation span uses flat prompt fallback
      const genSpan = emitted.find(s => s.name.startsWith('generation'));
      expect(genSpan).toBeDefined();
      const input = JSON.parse(genSpan!.attributes['openclaw.observation.input'] as string);
      expect(input).toHaveLength(1);
      expect(input[0].role).toBe('user');
      expect(input[0].content).toContain('what tools do you have');
    });
  });

  describe('runtime event streams', () => {
    it('does not emit discovery spans for unknown runtime streams', () => {
      const { buffer, emitted } = createBuffer();
      const sk = 'agent:main:telegram:123';

      buffer.onRuntimeEvent({
        runId: 'run-1',
        stream: 'reasoning',
        data: { text: 'thinking about the query...' },
        sessionKey: sk,
        ts: 1000,
      });

      const discoverySpans = emitted.filter(s => s.name.startsWith('runtime.'));
      expect(discoverySpans).toHaveLength(0);
    });

    it('does not emit discovery spans for lifecycle.end or lifecycle.error', () => {
      const { buffer, emitted } = createBuffer();
      const sk = 'agent:main:main';

      // lifecycle.start is handled internally (stores runId), not emitted
      buffer.onRuntimeEvent({
        runId: 'run-1',
        stream: 'lifecycle',
        data: { phase: 'start', startedAt: 1000 },
        sessionKey: sk,
        ts: 1000,
      });
      expect(emitted).toHaveLength(0);

      // lifecycle.end is now suppressed
      buffer.onRuntimeEvent({
        runId: 'run-1',
        stream: 'lifecycle',
        data: { phase: 'end', durationMs: 5000 },
        sessionKey: sk,
        ts: 6000,
      });

      const discoverySpans = emitted.filter(s => s.name.startsWith('runtime.'));
      expect(discoverySpans).toHaveLength(0);
    });

    it('does not emit discovery spans for runtime tool phases', () => {
      const { buffer, emitted } = createBuffer();
      const sk = 'agent:main:main';

      buffer.onRuntimeEvent({
        runId: 'run-1',
        stream: 'tool',
        data: { phase: 'start', toolCallId: 'tc-1', name: 'Bash' },
        sessionKey: sk,
        ts: 1100,
      });

      const discoverySpans = emitted.filter(s => s.name.startsWith('runtime.'));
      expect(discoverySpans).toHaveLength(0);
    });

    it('does not emit spans for assistant stream tokens', () => {
      const { buffer, emitted } = createBuffer();

      buffer.onRuntimeEvent({
        runId: 'run-1',
        stream: 'assistant',
        data: { delta: 'Hello' },
        sessionKey: 'agent:main:main',
        ts: 1500,
      });

      // Assistant tokens are captured for TTFT but not emitted as spans
      expect(emitted).toHaveLength(0);
    });
  });

  describe('transcript updates (suppressed)', () => {
    it('does not emit transcript.update spans', () => {
      const { buffer, emitted } = createBuffer();

      buffer.onTranscriptUpdate({
        sessionKey: 'agent:main:telegram:123',
        sessionId: 'sess-1',
        messages: [
          { role: 'user', content: 'hello' },
          { role: 'assistant', content: 'hi there' },
          { role: 'user', content: 'search for files' },
        ],
      });

      expect(emitted).toHaveLength(0);
    });

    it('is a no-op with no messages', () => {
      const { buffer, emitted } = createBuffer();

      buffer.onTranscriptUpdate({
        sessionKey: 'agent:main:main',
      });

      expect(emitted).toHaveLength(0);
    });

    it('is a no-op even with extra scalar fields', () => {
      const { buffer, emitted } = createBuffer();

      buffer.onTranscriptUpdate({
        sessionKey: 'agent:main:main',
        version: 3,
        truncated: true,
      });

      expect(emitted).toHaveLength(0);
    });
  });

  // ── Fix 1: Memory leak cleanup ─────────────────────────────────

  describe('memory cleanup', () => {
    it('cleans up session tracking maps when agent ends', () => {
      const { buffer, emitted } = createBuffer();
      const sk = 'agent:main:telegram:direct:123';

      // Simulate full session lifecycle
      buffer.onMessageIn({
        sessionId: 'sess-1', sessionKey: sk, channel: 'telegram',
        from: 'telegram:123', accountId: 'user-1', contentLength: 5, ts: 1000,
      });
      buffer.storeLastUserMessage(sk, 'hello');

      buffer.onAgentStart({
        sessionId: 'sess-1', sessionKey: sk, agentId: 'main', ts: 1100,
      });

      buffer.onLlmInput({
        sessionId: 'sess-1', sessionKey: sk, agentId: 'main',
        model: 'claude-sonnet-4-6', provider: 'anthropic', runId: 'run-1',
        ts: 1200,
      });

      buffer.onLlmOutput({
        sessionKey: sk, runId: 'run-1', model: 'claude-sonnet-4-6',
        provider: 'anthropic', inputTokens: 100, outputTokens: 50, ts: 2000,
      });

      buffer.onAgentEnd({
        sessionKey: sk, agentId: 'main', success: true, durationMs: 1000, ts: 2100,
      });

      // After agent ends, session maps should be cleaned up
      const stats = buffer.getStats();
      expect(stats.sharedSessionAccountIds).toBe(0);
      expect(stats.runtimeRunIds).toBe(0);
      expect(stats.sharedLastUserMessages).toBe(0);
      expect(stats.emittedMessageFingerprints).toBe(0);
      expect(stats.systemPromptEmitted).toBe(0);
    });

    it('flushStale also cleans up session tracking maps', () => {
      const { buffer, emitted } = createBuffer();
      const sk = 'agent:main:telegram:direct:456';
      const sessId = 'sess-stale';

      // Store state under both sessionKey and sessionId (as messageIn does)
      buffer.storeAccountId(sk, 'user-stale');
      buffer.storeAccountId(sessId, 'user-stale');
      buffer.storeLastUserMessage(sk, 'stale message');

      buffer.onAgentStart({
        sessionId: sessId, sessionKey: sk, agentId: 'main',
        ts: Date.now() - 400_000, // 400s ago
      });

      buffer.flushStale(300_000);

      const stats = buffer.getStats();
      // Stale session data should be cleaned
      expect(stats.agents).toBe(0);
      expect(stats.sharedLastUserMessages).toBe(0);
      expect(stats.sharedSessionAccountIds).toBe(0);
    });
  });

  // ── Fix 2: Error boundaries ────────────────────────────────────

  describe('error boundaries', () => {
    it('does not crash when onLlmOutput receives malformed data', () => {
      const { buffer, emitted } = createBuffer();
      const sk = 'agent:main:main';

      buffer.onAgentStart({
        sessionId: 'sess-1', sessionKey: sk, agentId: 'main', ts: 1000,
      });

      buffer.onLlmInput({
        sessionId: 'sess-1', sessionKey: sk, agentId: 'main',
        model: 'claude-sonnet-4-6', provider: 'anthropic', runId: 'run-1',
        ts: 1100,
      });

      // This should not throw even with unusual data
      expect(() => {
        buffer.onLlmOutput({
          sessionKey: sk, runId: 'run-1', model: 'claude-sonnet-4-6',
          provider: 'anthropic', inputTokens: NaN, outputTokens: undefined as any,
          ts: 2000,
        });
      }).not.toThrow();

      // Should still emit a generation span
      const genSpans = emitted.filter(s =>
        s.attributes['openclaw.observation.type'] === 'generation'
      );
      expect(genSpans.length).toBeGreaterThanOrEqual(1);
    });

    it('does not crash when onToolEnd receives undefined toolCallId', () => {
      const { buffer } = createBuffer();

      expect(() => {
        buffer.onToolEnd({
          sessionKey: 'agent:main:main',
          toolName: 'Bash',
          toolCallId: undefined as any,
          success: true,
          durationMs: 100,
          ts: 1000,
        });
      }).not.toThrow();
    });

    it('does not crash when onMessageIn receives empty data', () => {
      const { buffer } = createBuffer();

      expect(() => {
        buffer.onMessageIn({
          sessionId: '', sessionKey: '', channel: '', from: '',
          contentLength: 0, ts: 0,
        });
      }).not.toThrow();
    });
  });

  // ── Fix 3: onToolEnd should not mutate caller's data ───────────

  describe('data immutability', () => {
    it('onToolEnd does not mutate the input ToolEndData object', () => {
      const { buffer } = createBuffer();
      const sk = 'agent:main:main';

      buffer.onAgentStart({
        sessionId: 'sess-1', sessionKey: sk, agentId: 'main', ts: 1000,
      });

      buffer.onToolStart({
        sessionKey: sk, agentId: 'main', toolName: 'Bash',
        toolCallId: 'tc-1', ts: 1100,
      });

      // First tool.end stashes a result
      buffer.onToolEnd({
        sessionKey: sk, toolName: 'Bash', toolCallId: 'tc-1',
        success: true, result: 'first result', ts: 1200,
      });

      // Second tool.end — data object should NOT be mutated
      const secondEndData = {
        sessionKey: sk, toolName: 'Bash', toolCallId: 'tc-1',
        success: true, durationMs: 100, ts: 1200,
        result: undefined as string | undefined,
      };

      buffer.onToolEnd(secondEndData);

      // The original object should still have result === undefined
      expect(secondEndData.result).toBeUndefined();
    });
  });

  // ── Fix 4: completedTools flush path indicator ─────────────────

  describe('first-message cleanUserMessage fallback', () => {
    it('uses cleanUserMessage when available', () => {
      const { buffer, emitted } = createBuffer('full');
      const sk = 'agent:main:slack:channel:test';

      buffer.storeLastUserMessage(sk, 'hello');
      buffer.onAgentStart({
        sessionId: 'sess-1', sessionKey: sk, agentId: 'main', ts: 1000,
      });
      buffer.onLlmInput({
        sessionId: 'sess-1', sessionKey: sk, agentId: 'main',
        model: 'claude-sonnet-4-6', provider: 'anthropic', runId: 'run-1',
        input: 'System: [2026-03-14] Slack message from sergey: hello\n\nConversation info...',
        ts: 1100,
      });
      buffer.onLlmOutput({
        sessionKey: sk, runId: 'run-1', model: 'claude-sonnet-4-6',
        provider: 'anthropic', inputTokens: 10, outputTokens: 5, ts: 2000,
      });

      const gen = emitted.find(s => s.attributes['openclaw.observation.type'] === 'generation');
      const input = JSON.parse(gen!.attributes['openclaw.observation.input'] as string);
      expect(input[0].content).toBe('hello'); // clean, not the bloated prompt
    });

    it('falls back to truncated raw prompt when cleanUserMessage unavailable', () => {
      const { buffer, emitted } = createBuffer('full');
      const sk = 'agent:main:slack:channel:test';

      // No storeLastUserMessage — simulates restart or edit scenario
      buffer.onAgentStart({
        sessionId: 'sess-1', sessionKey: sk, agentId: 'main', ts: 1000,
      });
      buffer.onLlmInput({
        sessionId: 'sess-1', sessionKey: sk, agentId: 'main',
        model: 'claude-sonnet-4-6', provider: 'anthropic', runId: 'run-1',
        input: 'System: [timestamp] Slack message from sergey: howdy',
        ts: 1100,
      });
      buffer.onLlmOutput({
        sessionKey: sk, runId: 'run-1', model: 'claude-sonnet-4-6',
        provider: 'anthropic', inputTokens: 10, outputTokens: 5, ts: 2000,
      });

      const gen = emitted.find(s => s.attributes['openclaw.observation.type'] === 'generation');
      const input = JSON.parse(gen!.attributes['openclaw.observation.input'] as string);
      // Falls back to raw prompt (truncated), no regex cleaning
      expect(input[0].content).toContain('howdy');
    });

    it('stores cleanUserMessage under channel key so thread-start can find it', () => {
      const { buffer, emitted } = createBuffer('full');
      const channelKey = 'agent:main:slack:channel:c0am98auquq';
      const threadKey = 'agent:main:slack:channel:c0am98auquq:thread:123456';

      // message_received fires with channel key (no thread yet)
      buffer.storeLastUserMessage(channelKey, 'howdy');

      // llm_input fires with the same channel key (thread not created yet)
      buffer.onAgentStart({
        sessionId: 'sess-1', sessionKey: channelKey, agentId: 'main', ts: 1000,
      });
      buffer.onLlmInput({
        sessionId: 'sess-1', sessionKey: channelKey, agentId: 'main',
        model: 'claude-sonnet-4-6', provider: 'anthropic', runId: 'run-1',
        input: 'System: bloated prompt with howdy buried in it',
        ts: 1100,
      });
      buffer.onLlmOutput({
        sessionKey: channelKey, runId: 'run-1', model: 'claude-sonnet-4-6',
        provider: 'anthropic', inputTokens: 10, outputTokens: 5, ts: 2000,
      });

      const gen = emitted.find(s => s.attributes['openclaw.observation.type'] === 'generation');
      const input = JSON.parse(gen!.attributes['openclaw.observation.input'] as string);
      expect(input[0].content).toBe('howdy'); // found via channel key
    });
  });

  describe('conversation events suppressed across turns', () => {
    it('does not emit conversation events even with history changes across turns', () => {
      const { buffer, emitted } = createBuffer();
      const sk = 'agent:main:telegram:123';

      buffer.onAgentStart({
        sessionId: 'sess-1', sessionKey: sk, agentId: 'main', ts: 1000,
      });

      // Turn 1: 2 messages in history
      buffer.onLlmInput({
        sessionId: 'sess-1', sessionKey: sk, agentId: 'main',
        model: 'claude-sonnet-4-6', provider: 'anthropic', runId: 'run-1',
        historyMessages: [
          { role: 'user', content: 'message one' },
          { role: 'assistant', content: 'response one' },
        ],
        ts: 1100,
      });

      expect(emitted.filter(s => s.name.startsWith('conversation.'))).toHaveLength(0);

      buffer.onLlmOutput({
        sessionKey: sk, runId: 'run-1', model: 'claude-sonnet-4-6',
        provider: 'anthropic', inputTokens: 10, outputTokens: 5, ts: 2000,
      });

      // Turn 2: history changes — still no conversation events
      buffer.onLlmInput({
        sessionId: 'sess-1', sessionKey: sk, agentId: 'main',
        model: 'claude-sonnet-4-6', provider: 'anthropic', runId: 'run-2',
        historyMessages: [
          { role: 'assistant', content: 'response one' },
          { role: 'user', content: 'message two' },
        ],
        ts: 2100,
      });

      const allConvEvents = emitted.filter(s => s.name.startsWith('conversation.'));
      expect(allConvEvents).toHaveLength(0);
    });
  });

  describe('tool result source tracking', () => {
    it('marks result source as "history" when result came from applyToolResults', () => {
      const { buffer, emitted } = createBuffer('full');
      const sk = 'agent:main:main';

      buffer.onAgentStart({
        sessionId: 'sess-1', sessionKey: sk, agentId: 'main', ts: 1000,
      });

      buffer.onToolStart({
        sessionKey: sk, agentId: 'main', toolName: 'Bash',
        toolCallId: 'tc-hist', ts: 1100,
      });
      buffer.onToolEnd({
        sessionKey: sk, toolName: 'Bash', toolCallId: 'tc-hist',
        success: true, durationMs: 50, ts: 1150,
      });

      // Result arrives via history extraction (next llm_input)
      buffer.applyToolResults(new Map([['tc-hist', 'history result']]), sk);

      const toolSpan = emitted.find(s =>
        s.attributes['openclaw.observation.type'] === 'tool'
      );
      expect(toolSpan).toBeDefined();
      expect(toolSpan!.attributes['openclaw.tool.result_source']).toBe('history');
    });

    it('marks result source as "hook" when result came from after_tool_call', () => {
      const { buffer, emitted } = createBuffer('full');
      const sk = 'agent:main:main';

      buffer.onAgentStart({
        sessionId: 'sess-1', sessionKey: sk, agentId: 'main', ts: 1000,
      });

      buffer.onToolStart({
        sessionKey: sk, agentId: 'main', toolName: 'Bash',
        toolCallId: 'tc-direct', ts: 1100,
      });
      buffer.onToolEnd({
        sessionKey: sk, toolName: 'Bash', toolCallId: 'tc-direct',
        success: true, durationMs: 50, result: 'direct result', ts: 1150,
      });

      // Flushed via agentEnd (no history extraction)
      buffer.onAgentEnd({
        sessionKey: sk, agentId: 'main', success: true, durationMs: 200, ts: 1200,
      });

      const toolSpan = emitted.find(s =>
        s.attributes['openclaw.observation.type'] === 'tool'
      );
      expect(toolSpan).toBeDefined();
      expect(toolSpan!.attributes['openclaw.tool.result_source']).toBe('hook');
    });

    it('marks result source as "none" when no result available', () => {
      const { buffer, emitted } = createBuffer('full');
      const sk = 'agent:main:main';

      buffer.onAgentStart({
        sessionId: 'sess-1', sessionKey: sk, agentId: 'main', ts: 1000,
      });

      buffer.onToolStart({
        sessionKey: sk, agentId: 'main', toolName: 'Bash',
        toolCallId: 'tc-none', ts: 1100,
      });
      buffer.onToolEnd({
        sessionKey: sk, toolName: 'Bash', toolCallId: 'tc-none',
        success: true, durationMs: 50, ts: 1150,
        // no result
      });

      buffer.onAgentEnd({
        sessionKey: sk, agentId: 'main', success: true, durationMs: 200, ts: 1200,
      });

      const toolSpan = emitted.find(s =>
        s.attributes['openclaw.observation.type'] === 'tool'
      );
      expect(toolSpan).toBeDefined();
      expect(toolSpan!.attributes['openclaw.tool.result_source']).toBe('none');
    });
  });
});
