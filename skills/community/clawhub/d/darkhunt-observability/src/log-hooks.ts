import { SeverityNumber } from '@opentelemetry/api-logs';
import { LogRecord as SdkLogRecord } from '@opentelemetry/sdk-logs';
import type { IResource } from '@opentelemetry/resources';
import type { OpenClawPluginApi } from './hooks-adapter.js';
import type { LogHubExporter } from './log-exporter.js';
import type { PayloadMode } from './types.js';
import { INSTRUMENTATION_LIBRARY } from './types.js';
import { traceIdFromSession, randomSpanId } from './trace-id.js';
import { truncateChars, cleanGenerationOutput } from './payload.js';
import { resolveModel, costFallback, type ConfigPricing } from './pricing.js';

// ── Payload mode truncation limits ─────────────────────────────────

const DEBUG_CONTENT_CHARS = 500;

// ── Hook name mapping (same as hooks-adapter) ──────────────────────

const HOOK_NAMES = {
  messageIn: 'message_received',
  agentStart: 'before_agent_start',
  agentEnd: 'agent_end',
  llmInput: 'llm_input',
  llmOutput: 'llm_output',
  toolStart: 'before_tool_call',
  toolEnd: 'after_tool_call',
} as const;

// ── Registration ───────────────────────────────────────────────────

export function registerLogHooks(
  api: OpenClawPluginApi,
  logExporter: LogHubExporter,
  payloadMode: PayloadMode,
  resource: IResource,
  modelMap?: Record<string, string>,
  configPricing?: ConfigPricing,
): void {
  if (api.logger) {
    api.logger.info('[tracehub-logs] Registering log hooks');
  }

  // message_received
  api.on(HOOK_NAMES.messageIn, (evt: any, ctx: any) => {
    const sessionKey = ctx.sessionKey ?? '';
    const sessionId = ctx.sessionId ?? ctx.conversationId ?? evt.sessionId ?? sessionKey;
    const traceId = traceIdFromSession(sessionKey || sessionId);
    const from = evt.from ?? ctx.from ?? 'unknown';
    const channel = ctx.channelId ?? ctx.channel ?? 'unknown';
    const contentLength = typeof evt.content === 'string' ? evt.content.length : (evt.contentLength ?? 0);

    const attrs: Record<string, string | number | boolean> = {
      'openclaw.event': 'message_received',
      'openclaw.session.id': sessionId,
      'openclaw.session.key': sessionKey,
      'openclaw.channel': channel,
      'openclaw.message.from': from,
      'openclaw.message.content_length': contentLength,
    };

    const accountId = resolveAccountId(ctx.accountId, from);
    if (accountId) attrs['user.id'] = accountId;

    if (payloadMode !== 'metadata' && typeof evt.content === 'string') {
      attrs['openclaw.message.content'] = applyContentTruncation(evt.content, payloadMode);
    }

    const threadTs = extractThreadTs(sessionKey);
    if (threadTs) attrs['openclaw.slack.thread_ts'] = threadTs;

    const record = buildLogRecord({
      severityNumber: SeverityNumber.INFO,
      severityText: 'INFO',
      body: `Message received from ${from} on ${channel} (${contentLength} chars)`,
      traceId,
      attributes: attrs,
      resource,
    });

    logExporter.enqueue([record]);
  });

  // before_agent_start
  api.on(HOOK_NAMES.agentStart, (evt: any, ctx: any) => {
    const sessionKey = ctx.sessionKey ?? '';
    const sessionId = ctx.sessionId ?? ctx.conversationId ?? evt.sessionId ?? sessionKey;
    const traceId = traceIdFromSession(sessionKey || sessionId);
    const agentId = ctx.agentId ?? '';

    const attrs: Record<string, string | number | boolean> = {
      'openclaw.event': 'before_agent_start',
      'openclaw.session.id': sessionId,
      'openclaw.session.key': ctx.sessionKey ?? '',
      'openclaw.agent.id': agentId,
    };

    if (ctx.channelId) attrs['openclaw.channel'] = ctx.channelId;
    const accountId = resolveAccountId(ctx.accountId, ctx.from ?? evt.from);
    if (accountId) attrs['user.id'] = accountId;

    const threadTs = extractThreadTs(sessionKey);
    if (threadTs) attrs['openclaw.slack.thread_ts'] = threadTs;

    const record = buildLogRecord({
      severityNumber: SeverityNumber.INFO,
      severityText: 'INFO',
      body: `Agent starting: ${agentId}`,
      traceId,
      attributes: attrs,
      resource,
    });

    logExporter.enqueue([record]);
  });

  // agent_end
  api.on(HOOK_NAMES.agentEnd, (evt: any, ctx: any) => {
    const sessionKey = ctx.sessionKey ?? '';
    const agentId = ctx.agentId ?? '';
    const success = evt.success ?? true;
    const durationMs = evt.durationMs ?? 0;

    const attrs: Record<string, string | number | boolean> = {
      'openclaw.event': 'agent_end',
      'openclaw.session.key': sessionKey,
      'openclaw.agent.id': agentId,
      'openclaw.agent.success': success,
      'openclaw.agent.duration_ms': durationMs,
    };

    if (evt.error) attrs['openclaw.error'] = evt.error;

    const severity = success ? SeverityNumber.INFO : SeverityNumber.ERROR;
    const severityText = success ? 'INFO' : 'ERROR';
    const statusStr = success ? 'completed' : `failed: ${evt.error ?? 'unknown error'}`;

    const record = buildLogRecord({
      severityNumber: severity,
      severityText,
      body: `Agent ${agentId} ${statusStr} (${durationMs}ms)`,
      attributes: attrs,
      resource,
    });

    logExporter.enqueue([record]);
  });

  // llm_input
  api.on(HOOK_NAMES.llmInput, (evt: any, ctx: any) => {
    const sessionKey = ctx.sessionKey ?? '';
    const sessionId = evt.sessionId ?? ctx.sessionId ?? sessionKey;
    const traceId = traceIdFromSession(sessionKey || sessionId);
    const resolved = resolveModel(evt.model ?? '', modelMap, configPricing);
    const model = resolved.friendlyName;
    const provider = evt.provider ?? '';
    const promptLength = typeof evt.prompt === 'string' ? evt.prompt.length : 0;
    const historyLength = Array.isArray(evt.historyMessages) ? evt.historyMessages.length : 0;

    const attrs: Record<string, string | number | boolean> = {
      'openclaw.event': 'llm_input',
      'openclaw.session.id': sessionId,
      'openclaw.session.key': ctx.sessionKey ?? '',
      'openclaw.agent.id': ctx.agentId ?? '',
      'gen_ai.request.model': model,
      'gen_ai.system': provider,
      'openclaw.llm.prompt_length': promptLength,
      'openclaw.llm.history_length': historyLength,
    };

    if (resolved.rawModel !== resolved.friendlyName) {
      attrs['gen_ai.request.model.raw'] = resolved.rawModel;
    }
    if (evt.runId) attrs['openclaw.run.id'] = evt.runId;
    if (evt.attempt != null) attrs['openclaw.llm.attempt'] = evt.attempt;

    if (payloadMode !== 'metadata' && typeof evt.prompt === 'string') {
      attrs['openclaw.llm.prompt'] = applyContentTruncation(evt.prompt, payloadMode);
    }

    // Structured messages alongside the flat prompt for better classification
    if (payloadMode !== 'metadata' && Array.isArray(evt.historyMessages) && evt.historyMessages.length > 0) {
      const structured = normalizeHistoryForLog(evt.historyMessages, payloadMode);
      if (structured) {
        attrs['openclaw.llm.prompt_structured'] = structured;
      }
    }

    const record = buildLogRecord({
      severityNumber: SeverityNumber.INFO,
      severityText: 'INFO',
      body: `LLM input: ${provider}/${model} (prompt: ${promptLength} chars, history: ${historyLength} msgs)`,
      traceId,
      attributes: attrs,
      resource,
    });

    logExporter.enqueue([record]);
  });

  // llm_output
  api.on(HOOK_NAMES.llmOutput, (evt: any, ctx: any) => {
    const sessionKey = ctx.sessionKey ?? '';
    const usage = evt.usage ?? evt.lastAssistant?.usage ?? {};
    const rawModel = evt.model ?? evt.lastAssistant?.model ?? '';
    const resolved = resolveModel(rawModel, modelMap, configPricing);
    const model = resolved.friendlyName;
    const provider = evt.provider ?? evt.lastAssistant?.provider ?? '';
    const inputTokens = usage.inputTokens ?? usage.input_tokens ?? usage.input ?? 0;
    const outputTokens = usage.outputTokens ?? usage.output_tokens ?? usage.output ?? 0;
    const cacheReadTokens = usage.cacheReadInputTokens ?? usage.cacheRead ?? usage.cache_read_input_tokens;
    const cacheCreationTokens = usage.cacheCreationInputTokens ?? usage.cacheWrite ?? usage.cache_creation_input_tokens;

    const output = extractOutput(evt);
    const outputLength = output ? output.length : 0;

    // Cost: use OpenClaw's reported cost, or calculate from tokens + pricing
    const fallback = costFallback(
      extractCostTotal(evt), resolved.pricing,
      inputTokens, outputTokens, cacheReadTokens, cacheCreationTokens,
    );
    const costTotal = fallback.costTotal;

    const attrs: Record<string, string | number | boolean> = {
      'openclaw.event': 'llm_output',
      'openclaw.session.key': sessionKey,
      'gen_ai.request.model': model,
      'gen_ai.system': provider,
      'gen_ai.usage.input_tokens': inputTokens,
      'gen_ai.usage.output_tokens': outputTokens,
      'openclaw.llm.output_length': outputLength,
    };

    if (resolved.rawModel !== resolved.friendlyName) {
      attrs['gen_ai.request.model.raw'] = resolved.rawModel;
    }
    if (evt.runId) attrs['openclaw.run.id'] = evt.runId;
    if (cacheReadTokens != null) attrs['gen_ai.usage.cache_read_input_tokens'] = cacheReadTokens;
    if (cacheCreationTokens != null) attrs['gen_ai.usage.cache_creation_input_tokens'] = cacheCreationTokens;
    if (costTotal != null) attrs['openclaw.cost.total'] = costTotal;

    const stopReason = evt.lastAssistant?.stopReason ?? evt.stopReason;
    if (stopReason) attrs['openclaw.stop_reason'] = stopReason;

    if (evt.error) attrs['openclaw.error'] = evt.error;

    if (payloadMode !== 'metadata' && output) {
      attrs['openclaw.llm.output'] = applyContentTruncation(cleanGenerationOutput(output) ?? output, payloadMode);
    }

    const severity = evt.error ? SeverityNumber.ERROR : SeverityNumber.INFO;
    const severityText = evt.error ? 'ERROR' : 'INFO';
    const costStr = costTotal != null ? `, cost: $${costTotal.toFixed(6)}` : '';

    const record = buildLogRecord({
      severityNumber: severity,
      severityText,
      body: `LLM output: ${provider}/${model} (in: ${inputTokens}, out: ${outputTokens}${costStr}, output: ${outputLength} chars)`,
      attributes: attrs,
      resource,
    });

    logExporter.enqueue([record]);
  });

  // before_tool_call
  api.on(HOOK_NAMES.toolStart, (evt: any, ctx: any) => {
    const sessionKey = ctx.sessionKey ?? '';
    const agentId = ctx.agentId ?? '';
    const toolName = evt.toolName ?? '';

    const rawParams = evt.input ?? evt.args ?? evt.arguments
      ?? evt.params?.input ?? evt.params?.arguments ?? evt.params?.args
      ?? evt.parameters?.input ?? evt.parameters
      ?? evt.params;
    const parameters = rawParams
      ? (typeof rawParams === 'string' ? rawParams : JSON.stringify(rawParams))
      : undefined;

    const attrs: Record<string, string | number | boolean> = {
      'openclaw.event': 'before_tool_call',
      'openclaw.session.key': sessionKey,
      'openclaw.agent.id': agentId,
      'gen_ai.tool.name': toolName,
    };

    const toolCallId = evt.toolCallId ?? evt.callId;
    if (toolCallId) attrs['gen_ai.tool.call.id'] = toolCallId;
    if (evt.attempt != null) attrs['openclaw.tool.attempt'] = evt.attempt;

    if (payloadMode !== 'metadata' && parameters) {
      attrs['openclaw.tool.parameters'] = applyContentTruncation(parameters, payloadMode);
    }

    const record = buildLogRecord({
      severityNumber: SeverityNumber.INFO,
      severityText: 'INFO',
      body: `Tool call: ${toolName}${parameters ? ` (${parameters.length} chars params)` : ''}`,
      attributes: attrs,
      resource,
    });

    logExporter.enqueue([record]);
  });

  // after_tool_call
  api.on(HOOK_NAMES.toolEnd, (evt: any, ctx: any) => {
    const sessionKey = ctx.sessionKey ?? '';
    const toolName = evt.toolName ?? '';
    const success = !evt.error;
    const durationMs = evt.durationMs;

    const rawResult = evt.result ?? evt.output ?? evt.response ?? evt.content;
    const result = rawResult
      ? (typeof rawResult === 'string' ? rawResult : JSON.stringify(rawResult))
      : undefined;
    const resultLength = result ? result.length : 0;

    const attrs: Record<string, string | number | boolean> = {
      'openclaw.event': 'after_tool_call',
      'openclaw.session.key': sessionKey,
      'gen_ai.tool.name': toolName,
      'openclaw.tool.success': success,
      'openclaw.tool.result_length': resultLength,
    };

    const toolCallId = evt.toolCallId ?? evt.callId;
    if (toolCallId) attrs['gen_ai.tool.call.id'] = toolCallId;
    if (durationMs != null) attrs['openclaw.tool.duration_ms'] = durationMs;
    if (evt.error) attrs['openclaw.error'] = evt.error;

    if (payloadMode !== 'metadata' && result) {
      attrs['openclaw.tool.result'] = applyContentTruncation(result, payloadMode);
    }

    const severity = success ? SeverityNumber.INFO : SeverityNumber.ERROR;
    const severityText = success ? 'INFO' : 'ERROR';
    const durationStr = durationMs != null ? ` (${durationMs}ms)` : '';
    const statusStr = success ? 'completed' : `failed: ${evt.error ?? 'unknown error'}`;

    const record = buildLogRecord({
      severityNumber: severity,
      severityText,
      body: `Tool ${toolName} ${statusStr}${durationStr} (result: ${resultLength} chars)`,
      attributes: attrs,
      resource,
    });

    logExporter.enqueue([record]);
  });
}

// ── Log record builder ─────────────────────────────────────────────

interface LogRecordOpts {
  severityNumber: SeverityNumber;
  severityText: string;
  body: string;
  traceId?: string;
  spanId?: string;
  attributes: Record<string, string | number | boolean>;
  resource: IResource;
}

function buildLogRecord(opts: LogRecordOpts): SdkLogRecord {
  const now = Date.now();
  const hrTime: [number, number] = [
    Math.floor(now / 1000),
    (now % 1000) * 1_000_000,
  ];

  // SdkLogRecord constructor expects a specific shape.
  // We construct it to match the @opentelemetry/sdk-logs LogRecord interface.
  const record = new SdkLogRecord(
    // LoggerProviderSharedState shim — must include logRecordLimits
    {
      resource: opts.resource,
      logRecordLimits: {
        attributeCountLimit: 128,
        attributeValueLengthLimit: Infinity,
      },
      activeProcessor: {
        onEmit(logRecord: SdkLogRecord): void {
          // no-op — we handle export ourselves via the batch exporter
        },
        forceFlush(): Promise<void> {
          return Promise.resolve();
        },
        shutdown(): Promise<void> {
          return Promise.resolve();
        },
      },
    } as any,
    // InstrumentationScope
    INSTRUMENTATION_LIBRARY,
    // LogRecord data
    {
      hrTime,
      severityNumber: opts.severityNumber,
      severityText: opts.severityText,
      body: opts.body,
      attributes: opts.attributes,
      context: undefined as any,
    } as any,
  );

  // Set trace context if available
  if (opts.traceId) {
    record.setAttribute('openclaw.trace.id', opts.traceId);
  }
  if (opts.spanId) {
    record.setAttribute('openclaw.span.id', opts.spanId);
  }

  return record;
}

// ── Helpers ────────────────────────────────────────────────────────

function applyContentTruncation(content: string, mode: PayloadMode): string {
  if (mode === 'debug') {
    return truncateChars(content, DEBUG_CONTENT_CHARS);
  }
  // full mode — include everything (OTLP has its own limits)
  return content;
}

const USELESS_ACCOUNT_IDS = new Set(['undefined', 'default', 'null', '']);

function resolveAccountId(accountId?: string, from?: string): string | undefined {
  if (accountId && !USELESS_ACCOUNT_IDS.has(accountId)) {
    return accountId;
  }
  if (from && from !== 'unknown' && from !== '') {
    return from;
  }
  return undefined;
}

function extractOutput(evt: any): string | undefined {
  if (Array.isArray(evt.assistantTexts) && evt.assistantTexts.length > 0) {
    return evt.assistantTexts.join('\n');
  }
  if (evt.lastAssistant?.content) {
    return typeof evt.lastAssistant.content === 'string'
      ? evt.lastAssistant.content
      : JSON.stringify(evt.lastAssistant.content);
  }
  return undefined;
}

function extractCostTotal(evt: any): number | undefined {
  const cost = evt.cost ?? evt.usage?.cost ?? evt.lastAssistant?.usage?.cost;
  if (!cost) return undefined;
  if (typeof cost === 'number') return cost;
  if (typeof cost === 'object' && typeof cost.total === 'number') return cost.total;
  return undefined;
}

/** Extract Slack thread timestamp from sessionKey (e.g., ....:thread:1773423599.563419) */
function extractThreadTs(sessionKey: string): string | undefined {
  const match = sessionKey.match(/:thread:(\d+\.\d+)$/);
  return match ? match[1] : undefined;
}

/**
 * Normalize historyMessages into a structured JSON string for log attributes.
 * Truncates individual message content to keep log size manageable.
 */
function normalizeHistoryForLog(raw: unknown, mode: PayloadMode): string | undefined {
  if (!Array.isArray(raw) || raw.length === 0) return undefined;

  const maxContentChars = mode === 'debug' ? 200 : 500;
  const messages: Array<{ role: string; content: string }> = [];

  for (const msg of raw) {
    if (!msg || typeof msg !== 'object' || !msg.role) continue;
    // Skip tool messages — they have dedicated tool log events
    if (msg.role === 'tool' || msg.role === 'tool_result') continue;

    let content: string;
    if (typeof msg.content === 'string') {
      content = msg.content;
    } else if (msg.content != null) {
      content = JSON.stringify(msg.content);
    } else {
      continue;
    }

    if (content.length > maxContentChars) {
      content = content.slice(0, maxContentChars) + '...';
    }
    messages.push({ role: msg.role, content });
  }

  return messages.length > 0 ? JSON.stringify(messages) : undefined;
}
