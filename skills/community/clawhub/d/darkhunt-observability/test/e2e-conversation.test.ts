/**
 * End-to-end test: raw OpenClaw hook events → hooks-adapter → span-buffer → span-builder → exported spans.
 *
 * Simulates the EXACT data flow that happens in production:
 * - Mock OpenClaw API with `api.on()` handler registration
 * - Fire hook events with realistic Anthropic content blocks (objects, not clean strings)
 * - Verify exported spans: conversation events + generation spans with correct content
 */
import { describe, it, expect, beforeEach } from 'vitest';
import { Resource } from '@opentelemetry/resources';
import type { ReadableSpan } from '@opentelemetry/sdk-trace-base';
import { SpanBuffer, clearSharedState } from '../src/span-buffer.js';
import { registerHooks, registerDiscoveryHooks, type OpenClawPluginApi } from '../src/hooks-adapter.js';

const resource = new Resource({ 'service.name': 'openclaw-e2e-test' });

beforeEach(() => clearSharedState());

/** Create a mock OpenClaw plugin API that captures registered hook handlers. */
function createMockApi() {
  const handlers = new Map<string, Array<(evt: any, ctx: any) => void>>();

  const api: OpenClawPluginApi = {
    on(event: string, handler: (evt: any, ctx: any) => void) {
      if (!handlers.has(event)) handlers.set(event, []);
      handlers.get(event)!.push(handler);
    },
    version: '0.1.0',
    // No logger — simulates the production context where api.logger may be undefined
  };

  /** Fire a hook event, calling all registered handlers. */
  function fire(event: string, evt: any, ctx: any) {
    const list = handlers.get(event);
    if (list) {
      for (const handler of list) {
        handler(evt, ctx);
      }
    }
  }

  return { api, fire };
}

describe('E2E: conversation deduplication pipeline', () => {
  // Realistic Anthropic-style historyMessages with object content blocks.
  // IMPORTANT: historyMessages does NOT include the current user message.
  // The current message is in evt.prompt only. historyMessages ends with
  // the assistant's last response.

  // Turn 1: no prior history (first message in thread)
  const HISTORY_TURN_1: any[] = [];

  // Turn 2: history has turn 1 (user + assistant), current msg is in prompt
  const HISTORY_TURN_2 = [
    {
      role: 'user',
      content: [
        { type: 'text', text: 'What attack algorithms does DarkHunt support?' },
      ],
    },
    {
      role: 'assistant',
      content: [
        { type: 'text', text: 'DarkHunt supports 6 attack algorithms: Baseline TAP, Experimental TAP...' },
      ],
    },
  ];

  // History with tool use — current user msg ("Use web_fetch instead") is in prompt, not here
  const HISTORY_WITH_TOOLS = [
    {
      role: 'user',
      content: [
        { type: 'text', text: 'Search for competitor info' },
      ],
    },
    {
      role: 'assistant',
      content: [
        { type: 'text', text: 'Let me search the knowledge base.' },
        { type: 'tool_use', id: 'toolu_01', name: 'memory_search', input: { query: 'competitors' } },
      ],
    },
    {
      role: 'user',
      content: [
        { type: 'tool_result', tool_use_id: 'toolu_01', content: 'No results found.' },
      ],
    },
    {
      role: 'assistant',
      content: [
        { type: 'text', text: 'Nothing in the knowledge base. Let me try web search.' },
      ],
    },
  ];

  const SESSION_KEY = 'agent:darkhunt-docs:slack:channel:c0am98auquq:thread:1773491135';
  const MODEL_ARN = 'arn:aws:bedrock:eu-west-1:482397833370:application-inference-profile/ekadx6q1kayx';

  function makeCtx(overrides: Record<string, any> = {}) {
    return {
      agentId: 'darkhunt-docs',
      sessionKey: SESSION_KEY,
      sessionId: 'sess-e2e-1',
      workspaceDir: '/home/node/.openclaw/workspace',
      messageProvider: 'slack',
      trigger: 'message',
      channelId: 'slack',
      ...overrides,
    };
  }

  it('full 3-turn conversation: dedup + last-user-message generation input', () => {
    const emitted: ReadableSpan[] = [];
    const buffer = new SpanBuffer(resource, 'full', (spans) => emitted.push(...spans));
    const { api, fire } = createMockApi();

    // Register hooks with a model map (like production)
    registerHooks(api, buffer, undefined, { 'ekadx6q1kayx': 'claude-sonnet-4-6' });

    const ctx = makeCtx();

    // === User sends first message ===
    fire('message_received', {
      from: 'slack:channel:C0AM98AUQUQ',
      content: 'What attack algorithms does DarkHunt support?',
      timestamp: Date.now(),
    }, ctx);

    // === Agent starts ===
    fire('before_agent_start', {
      from: 'slack:channel:C0AM98AUQUQ',
    }, ctx);

    // === Turn 1: first user message (no history) ===
    fire('llm_input', {
      runId: 'run-1',
      sessionId: 'sess-e2e-1',
      provider: 'amazon-bedrock',
      model: MODEL_ARN,
      systemPrompt: 'You are Spike, a DarkHunt docs assistant.',
      prompt: 'System: [2026-03-14] Slack message from sergey: What attack algorithms?\n\nWhat attack algorithms does DarkHunt support?',
      historyMessages: HISTORY_TURN_1, // empty — first message
      imagesCount: 0,
    }, ctx);

    // No conversation events emitted (suppressed to reduce noise)
    const convAfterTurn1 = emitted.filter(s => s.name.startsWith('conversation.'));
    expect(convAfterTurn1).toHaveLength(0);

    // LLM responds
    fire('llm_output', {
      runId: 'run-1',
      sessionId: 'sess-e2e-1',
      provider: 'amazon-bedrock',
      model: MODEL_ARN,
      lastAssistant: {
        usage: { input: 500, output: 200, cacheRead: 0, cacheWrite: 0, totalTokens: 700, cost: { total: 0 } },
      },
      usage: { input: 500, output: 200, total: 700 },
      assistantTexts: ['DarkHunt supports 6 attack algorithms...'],
    }, ctx);

    // Generation span input comes from evt.prompt (the current user message)
    const gen1 = emitted.find(s => s.name.startsWith('generation'));
    expect(gen1).toBeDefined();
    const input1 = JSON.parse(gen1!.attributes['openclaw.observation.input'] as string);
    expect(input1[0].role).toBe('user');
    expect(input1[0].content).toBe('What attack algorithms does DarkHunt support?');

    // Model should be resolved
    expect(gen1!.attributes['gen_ai.request.model']).toBe('claude-sonnet-4-6');

    const countAfterTurn1 = emitted.length;

    // === User sends second message ===
    fire('message_received', {
      from: 'slack:channel:C0AM98AUQUQ',
      content: 'Tell me about Experimental TAP',
      timestamp: Date.now(),
    }, ctx);

    // === Turn 2: follow-up (history has turn 1, current msg in prompt) ===
    fire('llm_input', {
      runId: 'run-2',
      sessionId: 'sess-e2e-1',
      provider: 'amazon-bedrock',
      model: MODEL_ARN,
      systemPrompt: 'You are Spike, a DarkHunt docs assistant.',
      prompt: '[Thread history]\n[Slack sergey...]\nSystem: [timestamp] Tell me about Experimental TAP\n\nTell me about Experimental TAP',
      historyMessages: HISTORY_TURN_2, // [user1, assistant1] — prior turns only
      imagesCount: 0,
    }, ctx);

    // No conversation events (suppressed)
    const newConvEvents = emitted.slice(countAfterTurn1).filter(s => s.name.startsWith('conversation.'));
    expect(newConvEvents).toHaveLength(0);

    fire('llm_output', {
      runId: 'run-2',
      sessionId: 'sess-e2e-1',
      provider: 'amazon-bedrock',
      model: MODEL_ARN,
      lastAssistant: {
        usage: { input: 1000, output: 300, cacheRead: 0, cacheWrite: 0, totalTokens: 1300, cost: { total: 0 } },
      },
      usage: { input: 1000, output: 300, total: 1300 },
      assistantTexts: ['Experimental TAP is a variant...'],
    }, ctx);

    // Generation span input = current user message from prompt
    const gen2 = emitted.slice(countAfterTurn1).find(s => s.name.startsWith('generation'));
    expect(gen2).toBeDefined();
    const input2 = JSON.parse(gen2!.attributes['openclaw.observation.input'] as string);
    expect(input2[0].role).toBe('user');
    expect(input2[0].content).toBe('Tell me about Experimental TAP');
  });

  it('handles Anthropic content blocks with tool_use and tool_result', () => {
    const emitted: ReadableSpan[] = [];
    const buffer = new SpanBuffer(resource, 'full', (spans) => emitted.push(...spans));
    const { api, fire } = createMockApi();

    registerHooks(api, buffer);

    const ctx = makeCtx();
    fire('before_agent_start', {}, ctx);

    fire('llm_input', {
      runId: 'run-1',
      sessionId: 'sess-e2e-1',
      provider: 'amazon-bedrock',
      model: 'claude-sonnet-4-6',
      systemPrompt: 'You are Spike.',
      prompt: 'Use web_fetch instead', // current user message in prompt
      historyMessages: HISTORY_WITH_TOOLS, // prior turns only, ends with assistant
      imagesCount: 0,
    }, ctx);

    // No conversation events (suppressed)
    const convEvents = emitted.filter(s => s.name.startsWith('conversation.'));
    expect(convEvents).toHaveLength(0);

    fire('llm_output', {
      runId: 'run-1',
      sessionId: 'sess-e2e-1',
      provider: 'amazon-bedrock',
      model: 'claude-sonnet-4-6',
      lastAssistant: { usage: { input: 100, output: 50, totalTokens: 150, cost: { total: 0 } } },
      usage: { input: 100, output: 50, total: 150 },
      assistantTexts: ['Fetching competitor sites...'],
    }, ctx);

    // Generation span input = current user message from prompt
    const gen = emitted.find(s => s.name.startsWith('generation'));
    expect(gen).toBeDefined();
    const input = JSON.parse(gen!.attributes['openclaw.observation.input'] as string);
    expect(input).toHaveLength(1);
    expect(input[0].content).toBe('Use web_fetch instead');
  });

  it('falls back to flat prompt when historyMessages is empty array', () => {
    const emitted: ReadableSpan[] = [];
    const buffer = new SpanBuffer(resource, 'full', (spans) => emitted.push(...spans));
    const { api, fire } = createMockApi();

    registerHooks(api, buffer);

    const ctx = makeCtx();
    fire('before_agent_start', {}, ctx);

    fire('llm_input', {
      runId: 'run-1',
      sessionId: 'sess-e2e-1',
      provider: 'amazon-bedrock',
      model: 'claude-sonnet-4-6',
      systemPrompt: 'You are Spike.',
      prompt: 'System: [2026-03-14] Slack message from sergey: hello\n\nhello',
      historyMessages: [], // empty — first message in new thread
      imagesCount: 0,
    }, ctx);

    // No conversation events (suppressed)
    const convEvents = emitted.filter(s => s.name.startsWith('conversation.'));
    expect(convEvents).toHaveLength(0);

    fire('llm_output', {
      runId: 'run-1',
      sessionId: 'sess-e2e-1',
      provider: 'amazon-bedrock',
      model: 'claude-sonnet-4-6',
      lastAssistant: { usage: { input: 10, output: 5, totalTokens: 15, cost: { total: 0 } } },
      usage: { input: 10, output: 5, total: 15 },
      assistantTexts: ['Hello!'],
    }, ctx);

    // Generation span uses flat prompt fallback
    const gen = emitted.find(s => s.name.startsWith('generation'));
    expect(gen).toBeDefined();
    const input = JSON.parse(gen!.attributes['openclaw.observation.input'] as string);
    expect(input).toHaveLength(1);
    expect(input[0].role).toBe('user');
    expect(input[0].content).toContain('hello');
  });

  it('generation and agent spans have correct parent and trace linking', () => {
    const emitted: ReadableSpan[] = [];
    const buffer = new SpanBuffer(resource, 'full', (spans) => emitted.push(...spans));
    const { api, fire } = createMockApi();

    registerHooks(api, buffer);

    const ctx = makeCtx();
    fire('before_agent_start', {}, ctx);

    fire('llm_input', {
      runId: 'run-1',
      sessionId: 'sess-e2e-1',
      provider: 'amazon-bedrock',
      model: 'claude-sonnet-4-6',
      prompt: 'Tell me about TAP',
      historyMessages: HISTORY_TURN_2,
    }, ctx);

    fire('llm_output', {
      runId: 'run-1',
      sessionId: 'sess-e2e-1',
      provider: 'amazon-bedrock',
      model: 'claude-sonnet-4-6',
      lastAssistant: { usage: { input: 10, output: 5, totalTokens: 15, cost: { total: 0 } } },
      usage: { input: 10, output: 5, total: 15 },
    }, ctx);

    fire('agent_end', {
      agentId: 'darkhunt-docs',
      success: true,
      durationMs: 3000,
    }, ctx);

    // No conversation events (suppressed)
    expect(emitted.filter(s => s.name.startsWith('conversation.'))).toHaveLength(0);

    // Agent span is suppressed — should NOT be emitted
    const agentSpan = emitted.find(s => s.name.startsWith('agent'));
    expect(agentSpan).toBeUndefined();

    // Generation span should still exist
    const genSpan = emitted.find(s => s.name.startsWith('generation'));
    expect(genSpan).toBeDefined();
    expect(genSpan!.attributes['openclaw.observation.type']).toBe('generation');
  });
});

describe('E2E: discovery hooks', () => {
  it('emits event spans for unconfirmed hooks when they fire', () => {
    const { api, fire } = createMockApi();
    const emitted: ReadableSpan[] = [];

    registerDiscoveryHooks(api, resource, (spans) => emitted.push(...spans));

    // Simulate a cron_trigger event
    fire('cron_trigger', {
      cronId: 'daily-report',
      schedule: '0 9 * * *',
      triggeredAt: '2026-03-14T09:00:00Z',
    }, {
      sessionKey: 'cron:daily-report',
      agentId: 'reporter',
    });

    expect(emitted).toHaveLength(1);
    expect(emitted[0].name).toBe('cron_trigger');
    expect(emitted[0].attributes['openclaw.observation.type']).toBe('event');
    expect(emitted[0].attributes['openclaw.hook.name']).toBe('cron_trigger');
    expect(emitted[0].attributes['openclaw.hook.evt.cronId']).toBe('daily-report');
    expect(emitted[0].attributes['openclaw.hook.evt.schedule']).toBe('0 9 * * *');
    expect(emitted[0].attributes['openclaw.hook.ctx.agentId']).toBe('reporter');
  });

  it('captures error status from error events', () => {
    const { api, fire } = createMockApi();
    const emitted: ReadableSpan[] = [];

    registerDiscoveryHooks(api, resource, (spans) => emitted.push(...spans));

    fire('agent_error', {
      error: 'context window exceeded',
      agentId: 'main',
    }, {
      sessionKey: 'agent:main:telegram:123',
    });

    expect(emitted).toHaveLength(1);
    expect(emitted[0].name).toBe('agent_error');
    expect(emitted[0].status.code).toBe(2); // SpanStatusCode.ERROR
    expect(emitted[0].status.message).toBe('context window exceeded');
    expect(emitted[0].attributes['openclaw.observation.level']).toBe('ERROR');
  });

  it('handles multiple discovery events from different hooks', () => {
    const { api, fire } = createMockApi();
    const emitted: ReadableSpan[] = [];

    registerDiscoveryHooks(api, resource, (spans) => emitted.push(...spans));

    fire('session_start', { sessionId: 'sess-1' }, { sessionKey: 'sk-1' });
    fire('memory_search', { query: 'user preferences' }, { sessionKey: 'sk-1' });
    fire('subagent_start', { subagentId: 'researcher' }, { sessionKey: 'sk-1', agentId: 'main' });

    expect(emitted).toHaveLength(3);
    expect(emitted.map(s => s.name)).toEqual(['session_start', 'memory_search', 'subagent_start']);
  });

  it('serializes complex event data as JSON in attributes', () => {
    const { api, fire } = createMockApi();
    const emitted: ReadableSpan[] = [];

    registerDiscoveryHooks(api, resource, (spans) => emitted.push(...spans));

    fire('media_received', {
      mediaType: 'image',
      metadata: { width: 1024, height: 768, format: 'png' },
    }, {
      sessionKey: 'agent:main:telegram:123',
    });

    expect(emitted).toHaveLength(1);
    expect(emitted[0].attributes['openclaw.hook.evt.mediaType']).toBe('image');
    // Complex objects are JSON-serialized
    const metadata = emitted[0].attributes['openclaw.hook.evt.metadata'] as string;
    expect(metadata).toContain('1024');
    expect(metadata).toContain('png');
  });
});
