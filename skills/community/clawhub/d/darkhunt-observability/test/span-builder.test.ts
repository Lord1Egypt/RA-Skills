import { describe, it, expect } from 'vitest';
import { SpanStatusCode } from '@opentelemetry/api';
import { Resource } from '@opentelemetry/resources';
import {
  buildAgentSpan,
  buildGenerationSpan,
  buildToolSpan,
  buildMessageSpan,
  buildConversationEventSpan,
  msToHrTime,
} from '../src/span-builder.js';
import type {
  BufferedAgent,
  BufferedGeneration,
  BufferedTool,
  AgentEndData,
  LlmOutputData,
  ToolEndData,
  MessageInData,
} from '../src/types.js';

const resource = new Resource({ 'service.name': 'openclaw' });

describe('buildAgentSpan', () => {
  const buffered: BufferedAgent = {
    sessionId: 'sess-123',
    sessionKey: 'agent:main:telegram:direct:123',
    agentId: 'main',
    spanId: 'aaaa000000000001',
    traceId: 'bbbb000000000000cccc000000000000',
    startTime: msToHrTime(1000),
    traceName: 'find files',
    traceTags: ['telegram', 'tool-use'],
    channel: 'telegram',
  };

  it('creates agent span with correct name and attributes', () => {
    const endData: AgentEndData = {
      sessionKey: 'agent:main:telegram:direct:123',
      agentId: 'main',
      success: true,
      durationMs: 5000,
      ts: 6000,
    };

    const span = buildAgentSpan(buffered, endData, resource);

    expect(span.name).toBe('agent main');
    expect(span.spanContext().traceId).toBe(buffered.traceId);
    expect(span.spanContext().spanId).toBe(buffered.spanId);
    expect(span.parentSpanId).toBeUndefined();
    expect(span.status.code).toBe(SpanStatusCode.UNSET);
    expect(span.attributes['openclaw.observation.type']).toBe('agent');
    expect(span.attributes['openclaw.observation.level']).toBe('DEFAULT');
    expect(span.attributes['openclaw.session.id']).toBe('sess-123');
    expect(span.attributes['openclaw.session.key']).toBe('agent:main:telegram:direct:123');
    expect(span.attributes['openclaw.agent.id']).toBe('main');
    expect(span.attributes['openclaw.trace.name']).toBe('find files');
    expect(span.attributes['openclaw.trace.tags']).toEqual(['telegram', 'tool-use']);
    expect(span.attributes['openclaw.channel']).toBe('telegram');
  });

  it('sets error status on failure', () => {
    const endData: AgentEndData = {
      sessionKey: 'agent:main:telegram:direct:123',
      agentId: 'main',
      success: false,
      durationMs: 100,
      error: 'timeout',
      ts: 1100,
    };

    const span = buildAgentSpan(buffered, endData, resource);
    expect(span.status.code).toBe(SpanStatusCode.ERROR);
    expect(span.status.message).toBe('timeout');
    expect(span.attributes['openclaw.observation.level']).toBe('ERROR');
    expect(span.attributes['openclaw.observation.status_message']).toBe('timeout');
  });
});

describe('buildGenerationSpan', () => {
  const buffered: BufferedGeneration = {
    spanId: 'cccc000000000002',
    parentSpanId: 'aaaa000000000001',
    traceId: 'bbbb000000000000cccc000000000000',
    model: 'claude-opus-4-6',
    provider: 'anthropic',
    startTime: msToHrTime(1000),
    input: 'find TraceHubSpan files',
    inputLength: 23,
    systemPrompt: 'You are an AI assistant for OpenClaw.',
    systemPromptLength: 31200,
    historyLength: 766,
    modelParameters: '{"temperature":1,"max_tokens":8192}',
    attempt: 1,
    sessionKey: 'agent:main:telegram:direct:123',
    sessionId: 'sess-123',
  };

  const endData: LlmOutputData = {
    sessionKey: 'agent:main:telegram:direct:123',
    runId: 'run-1',
    model: 'claude-opus-4-6',
    provider: 'anthropic',
    output: 'I will search for TraceHubSpan files.',
    outputLength: 37,
    stopReason: 'tool_use',
    inputTokens: 1,
    outputTokens: 42,
    cacheReadInputTokens: 171287,
    cacheCreationInputTokens: 258,
    costDetails: '{"input":0.00001,"output":0.001,"cache_read":0.085,"total":0.086}',
    completionStartTime: '2026-03-02T21:14:22.200Z',
    ts: 5000,
  };

  it('includes all attributes in full mode', () => {
    const span = buildGenerationSpan(buffered, endData, resource, 'full');

    expect(span.name).toBe('generation claude-opus-4-6');
    expect(span.parentSpanId).toBe('aaaa000000000001');
    expect(span.attributes['openclaw.observation.type']).toBe('generation');
    expect(span.attributes['openclaw.observation.level']).toBe('DEFAULT');
    expect(span.attributes['openclaw.session.id']).toBe('sess-123');
    expect(span.attributes['openclaw.observation.model.name']).toBe('claude-opus-4-6');
    expect(span.attributes['gen_ai.request.model']).toBe('claude-opus-4-6');
    expect(span.attributes['gen_ai.system']).toBe('anthropic');
    expect(span.attributes['gen_ai.usage.input_tokens']).toBe(1);
    expect(span.attributes['gen_ai.usage.output_tokens']).toBe(42);
    expect(span.attributes['gen_ai.usage.cache_read_input_tokens']).toBe(171287);
    expect(span.attributes['gen_ai.usage.cache_creation_input_tokens']).toBe(258);
    // tokens.total = 1 + 42 + 171287 + 258 = 171588
    expect(span.attributes['gen_ai.usage.total_tokens']).toBe(171588);
    // Cost breakdown parsed from costDetails
    expect(span.attributes['openclaw.cost.input']).toBe(0.00001);
    expect(span.attributes['openclaw.cost.output']).toBe(0.001);
    expect(span.attributes['openclaw.cost.cache_read']).toBe(0.085);
    expect(span.attributes['openclaw.observation.input']).toBe(JSON.stringify([{ role: 'user', content: 'find TraceHubSpan files' }]));
    expect(span.attributes['openclaw.observation.output']).toBe(JSON.stringify([{ role: 'assistant', content: 'I will search for TraceHubSpan files.' }]));
    expect(span.attributes['openclaw.observation.system_prompt']).toBe('You are an AI assistant for OpenClaw.');
    expect(span.attributes['openclaw.observation.model.parameters']).toBe('{"temperature":1,"max_tokens":8192}');
    expect(span.attributes['openclaw.observation.input_length']).toBe(23);
    expect(span.attributes['openclaw.observation.output_length']).toBe(37);
    expect(span.attributes['openclaw.observation.system_prompt_length']).toBe(31200);
    expect(span.attributes['openclaw.observation.history_length']).toBe(766);
    expect(span.attributes['openclaw.stop_reason']).toBe('tool_use');
    expect(span.attributes['gen_ai.response.finish_reasons']).toEqual(['tool_use']);
    expect(span.attributes['openclaw.observation.completion_start_time']).toBe('2026-03-02T21:14:22.200Z');
    // TTFT: completionStartTime (2026-03-02T21:14:22.200Z) - startTime (1000ms epoch) — large value due to test fixture
    expect(span.attributes['openclaw.timing.time_to_first_token_ms']).toBeGreaterThan(0);
    expect(span.attributes['openclaw.observation.attempt']).toBe(1);
  });

  it('strips content in metadata mode', () => {
    const span = buildGenerationSpan(buffered, endData, resource, 'metadata');

    expect(span.attributes['openclaw.observation.input']).toBeUndefined();
    expect(span.attributes['openclaw.observation.output']).toBeUndefined();
    expect(span.attributes['openclaw.observation.system_prompt']).toBeUndefined();
    expect(span.attributes['openclaw.observation.model.parameters']).toBeUndefined();
    // Metadata always present
    expect(span.attributes['openclaw.observation.input_length']).toBe(23);
    expect(span.attributes['openclaw.observation.output_length']).toBe(37);
    expect(span.attributes['gen_ai.usage.input_tokens']).toBe(1);
    expect(span.attributes['gen_ai.usage.total_tokens']).toBe(171588);
    expect(span.attributes['openclaw.cost.input']).toBe(0.00001);
    expect(span.attributes['openclaw.observation.level']).toBe('DEFAULT');
  });

  it('sets error status on LLM error', () => {
    const errorEnd = { ...endData, error: 'rate_limit_exceeded: 429' };
    const span = buildGenerationSpan(buffered, errorEnd, resource, 'metadata');
    expect(span.status.code).toBe(SpanStatusCode.ERROR);
    expect(span.status.message).toBe('rate_limit_exceeded: 429');
    expect(span.attributes['openclaw.observation.level']).toBe('ERROR');
    expect(span.attributes['openclaw.observation.status_message']).toBe('rate_limit_exceeded: 429');
  });

  it('uses cleanUserMessage when available (from message_received)', () => {
    const bufferedWithCleanMsg: BufferedGeneration = {
      ...buffered,
      input: 'System: [2026-03-14] Slack message from sergey: Tell me more.\n\nTell me more.',
      cleanUserMessage: 'Tell me more.',
      systemPrompt: 'You are a helpful assistant.',
    };

    const span = buildGenerationSpan(bufferedWithCleanMsg, endData, resource, 'full');
    const input = JSON.parse(span.attributes['openclaw.observation.input'] as string);

    // First element is always the clean user message
    expect(input[0]).toEqual({ role: 'user', content: 'Tell me more.' });
    // May have a second element with role "context" if prompt has additional content
    expect(span.attributes['openclaw.observation.system_prompt']).toBe('You are a helpful assistant.');
  });

  it('falls back to cleaned evt.prompt when cleanUserMessage is absent', () => {
    const bufferedNoCleanMsg: BufferedGeneration = {
      ...buffered,
      input: 'Tell me more.',
      cleanUserMessage: undefined,
    };

    const span = buildGenerationSpan(bufferedNoCleanMsg, endData, resource, 'full');
    const input = JSON.parse(span.attributes['openclaw.observation.input'] as string);

    expect(input).toHaveLength(1);
    expect(input[0]).toEqual({ role: 'user', content: 'Tell me more.' });
  });

  it('falls back to flat prompt when historyMessages is empty', () => {
    const bufferedNoHistory: BufferedGeneration = {
      ...buffered,
      historyMessages: undefined,
    };

    const span = buildGenerationSpan(bufferedNoHistory, endData, resource, 'full');
    const input = JSON.parse(span.attributes['openclaw.observation.input'] as string);

    // Fallback: wrapped as single user message
    expect(input).toHaveLength(1);
    expect(input[0].role).toBe('user');
    expect(input[0].content).toBe('find TraceHubSpan files');
  });
});

describe('buildToolSpan', () => {
  const buffered: BufferedTool = {
    spanId: 'dddd000000000003',
    parentSpanId: 'aaaa000000000001',
    traceId: 'bbbb000000000000cccc000000000000',
    toolName: 'Bash',
    toolCallId: 'toolu_01ABC123',
    startTime: msToHrTime(2000),
    parameters: '{"bash_command":"find","full_command":"find /proj -name TraceHubSpan*"}',
    sessionKey: 'agent:main:telegram:direct:123',
    sessionId: 'sess-123',
    accountId: 'telegram:1382891386',
  };

  it('creates tool span with correct attributes in full mode', () => {
    const endData: ToolEndData = {
      sessionKey: 'agent:main:telegram:direct:123',
      toolName: 'Bash',
      toolCallId: 'toolu_01ABC123',
      success: true,
      durationMs: 124,
      ts: 2124,
    };

    const span = buildToolSpan(buffered, endData, resource, 'full');

    expect(span.name).toBe('Bash');
    expect(span.parentSpanId).toBe('aaaa000000000001');
    expect(span.attributes['openclaw.observation.type']).toBe('tool');
    expect(span.attributes['openclaw.observation.level']).toBe('DEFAULT');
    expect(span.attributes['openclaw.session.id']).toBe('sess-123');
    expect(span.attributes['gen_ai.tool.name']).toBe('Bash');
    expect(span.attributes['gen_ai.tool.call.id']).toBe('toolu_01ABC123');
    expect(span.attributes['openclaw.tool.success']).toBe(true);
    expect(span.attributes['openclaw.tool.parameters']).toBeDefined();
  });

  it('includes safe tool params even in metadata mode', () => {
    const endData: ToolEndData = {
      sessionKey: 'agent:main:telegram:direct:123',
      toolName: 'Bash',
      toolCallId: 'toolu_01ABC123',
      success: true,
      durationMs: 124,
      ts: 2124,
    };

    const span = buildToolSpan(buffered, endData, resource, 'metadata');
    expect(span.attributes['openclaw.tool.parameters']).toBeDefined();
    expect(span.attributes['gen_ai.tool.name']).toBe('Bash');
  });

  it('sets error status on failure', () => {
    const endData: ToolEndData = {
      sessionKey: 'agent:main:telegram:direct:123',
      toolName: 'Bash',
      toolCallId: 'toolu_01ABC123',
      success: false,
      error: 'command not found: xyz',
      durationMs: 350,
      ts: 2350,
    };

    const span = buildToolSpan(buffered, endData, resource, 'debug');
    expect(span.status.code).toBe(SpanStatusCode.ERROR);
    expect(span.status.message).toBe('command not found: xyz');
    expect(span.attributes['openclaw.observation.level']).toBe('ERROR');
    expect(span.attributes['openclaw.observation.status_message']).toBe('command not found: xyz');
  });

  it('redacts unknown tool parameters', () => {
    const unknownTool: BufferedTool = {
      ...buffered,
      toolName: 'custom_dangerous_tool',
      parameters: '{"secret":"api_key_here"}',
      sessionId: 'sess-123',
    };
    const endData: ToolEndData = {
      sessionKey: 'agent:main:telegram:direct:123',
      toolName: 'custom_dangerous_tool',
      toolCallId: 'toolu_01XYZ',
      success: true,
      durationMs: 100,
      ts: 2100,
    };

    const span = buildToolSpan(unknownTool, endData, resource, 'full');
    expect(span.attributes['openclaw.tool.parameters']).toBe('{"redacted":true}');
  });
});

describe('buildMessageSpan', () => {
  it('creates zero-duration message span', () => {
    const data: MessageInData = {
      sessionId: 'sess-123',
      sessionKey: 'agent:main:telegram:direct:123',
      channel: 'telegram',
      from: 'telegram:1382891386',
      contentLength: 24,
      ts: 1000,
    };

    const span = buildMessageSpan(data, 'bbbb000000000000cccc000000000000', 'eeee000000000004', resource);

    expect(span.name).toBe('message.in telegram');
    expect(span.startTime).toEqual(span.endTime);
    expect(span.parentSpanId).toBeUndefined();
    expect(span.attributes['openclaw.observation.type']).toBe('event');
    expect(span.attributes['openclaw.observation.level']).toBe('DEFAULT');
    expect(span.attributes['openclaw.session.id']).toBe('sess-123');
    expect(span.attributes['openclaw.channel']).toBe('telegram');
    expect(span.attributes['openclaw.message.from']).toBe('telegram:1382891386');
    expect(span.attributes['openclaw.message.content_length']).toBe(24);
  });
});

describe('msToHrTime', () => {
  it('converts epoch ms to HrTime tuple', () => {
    const hr = msToHrTime(1772486861533);
    expect(hr[0]).toBe(1772486861);
    expect(hr[1]).toBe(533000000);
  });

  it('handles exact seconds', () => {
    const hr = msToHrTime(5000);
    expect(hr[0]).toBe(5);
    expect(hr[1]).toBe(0);
  });
});

describe('buildConversationEventSpan', () => {
  it('creates a zero-duration event span with correct attributes', () => {
    const span = buildConversationEventSpan(
      'user', 'what tools do you have?', 3,
      'sess-123', 'trace-abc', 'span-001', 'parent-001', 5000, resource,
    );

    expect(span.name).toBe('conversation.user');
    expect(span.spanContext().spanId).toBe('span-001');
    expect(span.parentSpanId).toBe('parent-001');
    expect(span.attributes['openclaw.observation.type']).toBe('event');
    expect(span.attributes['openclaw.conversation.role']).toBe('user');
    expect(span.attributes['openclaw.conversation.content']).toBe('what tools do you have?');
    expect(span.attributes['openclaw.conversation.index']).toBe(3);
    expect(span.attributes['openclaw.session.id']).toBe('sess-123');
    // Zero-duration
    expect(span.startTime).toEqual(span.endTime);
  });

  it('creates assistant conversation events', () => {
    const span = buildConversationEventSpan(
      'assistant', 'Here are the tools...', 4,
      'sess-123', 'trace-abc', 'span-002', 'parent-001', 5000, resource,
    );

    expect(span.name).toBe('conversation.assistant');
    expect(span.attributes['openclaw.conversation.role']).toBe('assistant');
  });
});
