import type { ReadableSpan } from '@opentelemetry/sdk-trace-base';
import type { IResource } from '@opentelemetry/resources';
import type { SpanBuffer } from './span-buffer.js';
import type {
  MessageInData,
  AgentStartData,
  AgentEndData,
  LlmInputData,
  LlmOutputData,
  ToolStartData,
  ToolEndData,
  HistoryMessage,
} from './types.js';
import { resolveModel, costFallback, type ConfigPricing } from './pricing.js';
import { traceIdFromSession, randomSpanId } from './trace-id.js';
import { buildDiscoveryEventSpan } from './span-builder.js';
import { parseUserIdentity, parseChannelIdentity } from './payload.js';

// ── OpenClaw Plugin SDK types ────────────────────────────────────

export interface OpenClawPluginApi {
  on(event: string, handler: (evt: any, ctx: any) => void): void;
  pluginConfig?: unknown;
  version?: string;
  processOwner?: string;
  registerService?(svc: any): void;
  registerCli?(registrar: (ctx: any) => void, opts?: { commands?: string[] }): void;
  logger?: { info: (...args: unknown[]) => void; error: (...args: unknown[]) => void };
}

// ── Hook name mapping ────────────────────────────────────────────

export interface HookMapping {
  messageIn: string;
  agentStart: string;
  agentEnd: string;
  llmInput: string;
  llmOutput: string;
  toolStart: string;
  toolEnd: string;
  shutdown: string;
}

export const DEFAULT_MAPPING: HookMapping = {
  messageIn: 'message_received',
  agentStart: 'before_agent_start',
  agentEnd: 'agent_end',
  llmInput: 'llm_input',
  llmOutput: 'llm_output',
  toolStart: 'before_tool_call',
  toolEnd: 'after_tool_call',
  shutdown: 'shutdown',
};

// ── Registration ─────────────────────────────────────────────────

export function registerHooks(
  api: OpenClawPluginApi,
  buffer: SpanBuffer,
  mapping: HookMapping = DEFAULT_MAPPING,
  modelMap?: Record<string, string>,
  configPricing?: ConfigPricing,
): void {
  // Log which hooks we're registering and available API info
  if (api.logger) {
    api.logger.info(`[tracehub] Registering hooks: ${JSON.stringify(mapping)}`);
    api.logger.info(`[tracehub] api.version: ${api.version}`);
    api.logger.info(`[tracehub] api.processOwner: ${api.processOwner}`);
    api.logger.info(`[tracehub] api keys: ${Object.keys(api).join(', ')}`);
  }

  // message_received: evt has {from, content}, ctx has {sessionKey, agentId, channelId}
  api.on(mapping.messageIn, (evt: any, ctx: any) => {
    if (api.logger) {
      api.logger.info('[tracehub] HOOK FIRED: messageIn');
      api.logger.info('[tracehub] messageIn evt keys: ' + Object.keys(evt).join(', '));
      api.logger.info('[tracehub] messageIn ctx keys: ' + Object.keys(ctx).join(', '));
      api.logger.info('[tracehub] messageIn evt.from: "' + evt.from + '" ctx.accountId: "' + ctx.accountId + '" ctx.channelId: "' + ctx.channelId + '"');
      api.logger.info('[tracehub] messageIn evt.metadata: ' + JSON.stringify(evt.metadata)?.slice(0, 500));
      api.logger.info('[tracehub] messageIn evt.timestamp: ' + evt.timestamp);
      api.logger.info('[tracehub] messageIn buffer.id: ' + (buffer as any)._debugId);
    }
    // Use sessionKey as primary trace correlation key — it includes thread IDs
    // (e.g., agent:darkhunt-support:slack:channel:c0a1897aj79:thread:1773423599.563419)
    const rawSessionKey = ctx.sessionKey ?? '';
    const from = evt.from ?? ctx.from ?? 'unknown';
    // Extract user & channel identity from metadata
    const userIdentity = parseUserIdentity(evt.metadata);
    const channelIdentity = parseChannelIdentity(evt.metadata, undefined, ctx.channelId, from);
    // Build thread correlation key from channelId + threadId (from metadata).
    // When sessionKey is missing (message_received has no ctx.sessionKey), this lets
    // us defer the span and re-attach it to the correct trace when agentStart fires.
    const channelId = ctx.channelId ?? ctx.channel ?? '';
    const threadId = evt.metadata?.threadId ?? evt.metadata?.thread_ts ?? '';
    const threadKey = channelId && threadId ? `${channelId}:${threadId}` : undefined;
    // Store threadId for agentStart to promote channel-level keys.
    // message_received typically has NO ctx.sessionKey for top-level messages,
    // so promotion happens in agentStart which has the real sessionKey.
    let sessionKey = rawSessionKey;
    if (threadId) {
      const slackChId = extractSlackChannelId(from, evt.metadata);
      if (slackChId) {
        pendingThreadIds.set(slackChId, threadId);
        if (api.logger) {
          api.logger.info(`[tracehub] Stored pending threadId for channel ${slackChId}: ${threadId}`);
        }
      }
      // If sessionKey IS available and channel-level, promote it here too
      if (rawSessionKey && !rawSessionKey.includes(':thread:')) {
        sessionKey = `${rawSessionKey}:thread:${threadId}`;
        sessionKeyOverrides.set(rawSessionKey, sessionKey);
      }
    }
    const sessionId = ctx.sessionId ?? ctx.conversationId ?? evt.sessionId ?? sessionKey;
    const data: MessageInData = {
      sessionId,
      sessionKey,
      channel: channelId || 'unknown',
      from,
      accountId: resolveUserId(ctx.accountId, from),
      contentLength: typeof evt.content === 'string' ? evt.content.length : (evt.contentLength ?? 0),
      ts: Date.now(),
      userIdentity,
      channelIdentity,
      threadKey,
    };
    buffer.onMessageIn(data);
    // Store the clean user message text under ALL available keys for generation span input
    if (typeof evt.content === 'string' && evt.content) {
      buffer.storeLastUserMessage(sessionKey || sessionId, evt.content);
      if (ctx.conversationId) buffer.storeLastUserMessage(ctx.conversationId, evt.content);
      if (ctx.sessionId && ctx.sessionId !== sessionKey) buffer.storeLastUserMessage(ctx.sessionId, evt.content);
      // Also store under raw key for cross-instance lookup
      if (rawSessionKey && rawSessionKey !== sessionKey) buffer.storeLastUserMessage(rawSessionKey, evt.content);
    }
    // Store accountId under ALL available ctx keys so agentStart (which uses ctx.sessionId) can find it
    if (data.accountId) {
      if (ctx.conversationId) buffer.storeAccountId(ctx.conversationId, data.accountId);
      if (ctx.sessionId) buffer.storeAccountId(ctx.sessionId, data.accountId);
      if (ctx.sessionKey) buffer.storeAccountId(ctx.sessionKey, data.accountId);
      // Also store under promoted thread-scoped key
      if (sessionKey !== rawSessionKey) buffer.storeAccountId(sessionKey, data.accountId);
    }
    // Store user & channel identity under all available keys
    if (userIdentity) {
      buffer.storeUserIdentity(sessionKey || sessionId, userIdentity);
      if (ctx.conversationId) buffer.storeUserIdentity(ctx.conversationId, userIdentity);
      if (ctx.sessionId && ctx.sessionId !== sessionKey) buffer.storeUserIdentity(ctx.sessionId, userIdentity);
      // Also store under raw key for cross-instance lookup
      if (rawSessionKey && rawSessionKey !== sessionKey) buffer.storeUserIdentity(rawSessionKey, userIdentity);
    }
    if (channelIdentity) {
      buffer.storeChannelIdentity(sessionKey || sessionId, channelIdentity);
      if (ctx.conversationId) buffer.storeChannelIdentity(ctx.conversationId, channelIdentity);
      if (ctx.sessionId && ctx.sessionId !== sessionKey) buffer.storeChannelIdentity(ctx.sessionId, channelIdentity);
      if (rawSessionKey && rawSessionKey !== sessionKey) buffer.storeChannelIdentity(rawSessionKey, channelIdentity);
    }
  });

  // before_agent_start: evt has {prompt}, ctx has {sessionKey, agentId}
  api.on(mapping.agentStart, (evt: any, ctx: any) => {
    const rawKey = ctx.sessionKey ?? '';
    // Promote channel-level key using pending threadId from message_received.
    // pendingThreadIds always takes priority over existing overrides — it
    // represents the CURRENT message, while an existing override may be stale
    // from a previous message on the same channel.
    let sessionKey = rawKey;
    if (rawKey && !rawKey.includes(':thread:')) {
      const chMatch = rawKey.match(/:channel:([^:]+)$/);
      if (chMatch) {
        const pendingThread = pendingThreadIds.get(chMatch[1].toLowerCase());
        if (pendingThread) {
          sessionKey = `${rawKey}:thread:${pendingThread}`;
          sessionKeyOverrides.set(rawKey, sessionKey);
          // Don't delete pendingThreadIds here — second plugin instance
          // (buffer.id=3/4) also needs to resolve the same threadId.
          // Naturally overwritten by next message on this channel.
          if (api.logger) {
            api.logger.info(`[tracehub] Promoted sessionKey in agentStart: ${sessionKey}`);
          }
        } else {
          // No pending thread — fall back to existing override if any
          sessionKey = resolveSessionKey(rawKey);
        }
      } else {
        sessionKey = resolveSessionKey(rawKey);
      }
    } else {
      sessionKey = resolveSessionKey(rawKey);
    }
    if (api.logger) {
      api.logger.info('[tracehub] HOOK FIRED: agentStart');
      const ui = buffer.getUserIdentity(sessionKey);
      api.logger.info(`[tracehub] agentStart buffer.id=${(buffer as any)._debugId} identity for "${sessionKey}": ${ui ? JSON.stringify(ui) : 'NONE'}`);
    }
    const sessionId = ctx.sessionId ?? ctx.conversationId ?? evt.sessionId ?? sessionKey;
    const from = ctx.from ?? evt.from;
    const data: AgentStartData = {
      sessionId,
      sessionKey,
      agentId: ctx.agentId ?? '',
      traceName: evt.traceName ?? (typeof evt.prompt === 'string' ? evt.prompt.slice(0, 100) : undefined),
      traceTags: evt.traceTags,
      channel: ctx.channelId,
      accountId: resolveUserId(ctx.accountId, from),
      ts: Date.now(),
    };
    buffer.onAgentStart(data);
  });

  // agent_end: evt has {success, durationMs, error}, ctx has {sessionKey, agentId}
  api.on(mapping.agentEnd, (evt: any, ctx: any) => {
    if (api.logger) api.logger.info('[tracehub] HOOK FIRED: agentEnd');
    const rawKey = ctx.sessionKey ?? '';
    const resolvedKey = resolveSessionKey(rawKey);
    // Do NOT delete sessionKeyOverrides here — agentEnd fires BEFORE llmOutput
    // in OpenClaw's hook ordering. The override will be naturally replaced by
    // the next message (serialized per channel via lane queue).
    const data: AgentEndData = {
      sessionKey: resolvedKey,
      agentId: ctx.agentId ?? '',
      success: evt.success ?? true,
      durationMs: evt.durationMs ?? 0,
      error: evt.error,
      ts: Date.now(),
    };
    buffer.onAgentEnd(data);
  });

  // llm_input: evt has {runId, sessionId, provider, model, systemPrompt, prompt, historyMessages}
  api.on(mapping.llmInput, (evt: any, ctx: any) => {
    if (api.logger) {
      api.logger.info('[tracehub] HOOK FIRED: llmInput');
      api.logger.info('[tracehub] llmInput evt keys: ' + Object.keys(evt).join(', '));
      api.logger.info('[tracehub] llmInput ctx keys: ' + Object.keys(ctx).join(', '));
      api.logger.info('[tracehub] llmInput evt.prompt type: ' + typeof evt.prompt + ' length: ' + (typeof evt.prompt === 'string' ? evt.prompt.length : 'N/A'));
      if (typeof evt.prompt === 'string') {
        api.logger.info('[tracehub] llmInput evt.prompt (first 400): ' + evt.prompt.slice(0, 400));
      }
      api.logger.info('[tracehub] llmInput ctx.messageProvider: ' + ctx.messageProvider);
      api.logger.info('[tracehub] llmInput ctx.trigger: ' + ctx.trigger);
    }

    // Extract tool results from history BEFORE creating the generation span.
    // This emits completed tool spans with their results attached.
    const sessionKey = resolveSessionKey(ctx.sessionKey ?? '');
    const toolResults = extractToolResultsFromHistory(evt.historyMessages);
    if (toolResults.size > 0) {
      if (api.logger) {
        api.logger.info(`[tracehub] Found ${toolResults.size} tool result(s) in history`);
      }
      buffer.applyToolResults(toolResults, sessionKey);
    } else {
      // No results found — flush any waiting tools so they're not held forever
      buffer.applyToolResults(new Map(), sessionKey);
    }

    const resolvedInput = resolveModel(evt.model ?? '', modelMap, configPricing);
    // Parse user/channel from prompt as fallback (in case message_received metadata was empty)
    const promptStr = typeof evt.prompt === 'string' ? evt.prompt : undefined;
    const promptUser = parseUserIdentity(undefined, promptStr);
    const promptChannel = parseChannelIdentity(undefined, promptStr, ctx.channelId);
    if (promptUser) buffer.storeUserIdentity(sessionKey, promptUser);
    if (promptChannel) buffer.storeChannelIdentity(sessionKey, promptChannel);

    const data: LlmInputData = {
      sessionId: evt.sessionId ?? ctx.sessionId ?? '',
      sessionKey,
      agentId: ctx.agentId ?? '',
      model: resolvedInput.friendlyName,
      rawModel: resolvedInput.rawModel !== resolvedInput.friendlyName ? resolvedInput.rawModel : undefined,
      provider: evt.provider ?? '',
      runId: evt.runId ?? '',
      input: promptStr,
      inputLength: promptStr ? promptStr.length : undefined,
      systemPrompt: typeof evt.systemPrompt === 'string' ? evt.systemPrompt : undefined,
      systemPromptLength: typeof evt.systemPrompt === 'string' ? evt.systemPrompt.length : undefined,
      historyLength: Array.isArray(evt.historyMessages) ? evt.historyMessages.length : undefined,
      historyMessages: safeNormalizeHistory(evt.historyMessages),
      modelParameters: evt.modelParameters ? JSON.stringify(evt.modelParameters) : undefined,
      attempt: evt.attempt,
      ts: Date.now(),
    };
    buffer.onLlmInput(data);
  });

  // llm_output: evt has {runId, sessionId, provider, model, lastAssistant, usage, assistantTexts}
  api.on(mapping.llmOutput, (evt: any, ctx: any) => {
    if (api.logger) {
      api.logger.info('[tracehub] HOOK FIRED: llmOutput');
      api.logger.info('[tracehub] llmOutput evt keys: ' + Object.keys(evt).join(', '));
      api.logger.info('[tracehub] llmOutput evt.usage: ' + JSON.stringify(evt.usage));
      api.logger.info('[tracehub] llmOutput evt.lastAssistant?.usage: ' + JSON.stringify(evt.lastAssistant?.usage));
    }
    const usage = evt.usage ?? evt.lastAssistant?.usage ?? {};
    const lastAssistant = evt.lastAssistant ?? {};

    // Resolve model name (ARN → friendly name) and look up pricing
    const rawModel = evt.model ?? lastAssistant.model ?? '';
    const resolved = resolveModel(rawModel, modelMap, configPricing);

    // Cost: use OpenClaw's reported cost, or calculate from tokens + pricing
    const inputTk = usage.inputTokens ?? usage.input_tokens ?? usage.input ?? 0;
    const outputTk = usage.outputTokens ?? usage.output_tokens ?? usage.output ?? 0;
    const cacheReadTk = usage.cacheReadInputTokens ?? usage.cacheRead ?? usage.cache_read_input_tokens;
    const cacheWriteTk = usage.cacheCreationInputTokens ?? usage.cacheWrite ?? usage.cache_creation_input_tokens;
    const fallback = costFallback(
      extractCostTotal(evt), resolved.pricing,
      inputTk, outputTk, cacheReadTk, cacheWriteTk,
    );
    const costTotal = fallback.costTotal;
    const costDetails = fallback.costBreakdown
      ? JSON.stringify(fallback.costBreakdown)
      : extractCostDetails(evt);

    const output = extractOutput(evt);
    const data: LlmOutputData = {
      sessionKey: resolveSessionKey(ctx.sessionKey ?? ''),
      runId: evt.runId ?? '',
      model: resolved.friendlyName,
      rawModel: resolved.rawModel !== resolved.friendlyName ? resolved.rawModel : undefined,
      provider: evt.provider ?? lastAssistant.provider ?? '',
      output,
      outputLength: output ? output.length : undefined,
      stopReason: lastAssistant.stopReason ?? evt.stopReason,
      inputTokens: usage.inputTokens ?? usage.input_tokens ?? usage.input,
      outputTokens: usage.outputTokens ?? usage.output_tokens ?? usage.output,
      cacheReadInputTokens: usage.cacheReadInputTokens ?? usage.cacheRead ?? usage.cache_read_input_tokens,
      cacheCreationInputTokens: usage.cacheCreationInputTokens ?? usage.cacheWrite ?? usage.cache_creation_input_tokens,
      costTotal,
      costDetails,
      completionStartTime: evt.completionStartTime,
      error: evt.error,
      ts: Date.now(),
    };
    buffer.onLlmOutput(data);
  });

  // before_tool_call: evt has {toolName, params}, ctx has {sessionKey, agentId}
  api.on(mapping.toolStart, (evt: any, ctx: any) => {
    if (api.logger) {
      api.logger.info('[tracehub] HOOK FIRED: toolStart ' + evt.toolName);
      api.logger.info('[tracehub] toolStart evt keys: ' + Object.keys(evt).join(', '));
    }
    // Use a stable fallback toolCallId: agentId + toolName + counter-like suffix.
    // Both start and end MUST use the same fallback logic for key matching.
    const toolCallId = evt.toolCallId ?? evt.callId ?? `${ctx.agentId ?? 'no-agent'}:${evt.toolName ?? 'unknown'}`;
    // Extract actual tool arguments. OpenClaw's before_tool_call provides:
    // evt.params = {name, callId, ...} — tool routing metadata, NOT the actual args.
    // The real tool input may be in evt.params.input, evt.input, or evt.args.
    const rawParams = evt.input ?? evt.args ?? evt.arguments
      ?? evt.params?.input ?? evt.params?.arguments ?? evt.params?.args
      ?? evt.parameters?.input ?? evt.parameters
      ?? evt.params;
    const parameters = rawParams
      ? (typeof rawParams === 'string' ? rawParams : JSON.stringify(rawParams))
      : undefined;
    if (api.logger) {
      api.logger.info(`[tracehub] toolStart ${evt.toolName} params: ${parameters?.slice(0, 200) ?? 'null'}`);
    }
    const data: ToolStartData = {
      sessionKey: resolveSessionKey(ctx.sessionKey ?? ''),
      agentId: ctx.agentId ?? '',
      toolName: evt.toolName ?? '',
      toolCallId,
      parameters,
      attempt: evt.attempt,
      ts: Date.now(),
    };
    buffer.onToolStart(data);
  });

  // after_tool_call: evt has {toolName, durationMs, error, result/output}, ctx has {sessionKey, agentId}
  api.on(mapping.toolEnd, (evt: any, ctx: any) => {
    if (api.logger) {
      api.logger.info('[tracehub] HOOK FIRED: toolEnd ' + evt.toolName);
      api.logger.info('[tracehub] toolEnd evt keys: ' + Object.keys(evt).join(', '));
    }
    // Must match the same fallback logic as toolStart above
    const toolCallId = evt.toolCallId ?? evt.callId ?? `${ctx.agentId ?? 'no-agent'}:${evt.toolName ?? 'unknown'}`;
    // Capture tool result directly from after_tool_call event
    const rawResult = evt.result ?? evt.output ?? evt.response ?? evt.content;
    const result = rawResult
      ? (typeof rawResult === 'string' ? rawResult : JSON.stringify(rawResult))
      : undefined;
    if (api.logger && result) {
      api.logger.info(`[tracehub] toolEnd ${evt.toolName} result (${result.length} chars)`);
    }
    const data: ToolEndData = {
      sessionKey: resolveSessionKey(ctx.sessionKey ?? ''),
      toolName: evt.toolName ?? '',
      toolCallId,
      success: !evt.error,
      durationMs: evt.durationMs,
      result,
      error: evt.error,
      ts: Date.now(),
    };
    buffer.onToolEnd(data);
  });
}

// ── Session key thread promotion ────────────────────────────────
// When a top-level channel message arrives, OpenClaw uses a channel-level
// sessionKey (agent:X:slack:channel:Y) with no thread suffix.  But the bot
// replies in a thread (replyToMode="all"), so follow-up messages get
// agent:X:slack:channel:Y:thread:Z.
//
// We promote the channel-level key to the thread-scoped key using the
// threadId from message_received metadata.  This way the first message
// AND all follow-ups share the same trace.
//
// Safe because OpenClaw serializes runs per sessionKey (lane queue).

/** Module-level override map — exported so SpanBuffer can resolve runtime event keys */
export const sessionKeyOverrides = new Map<string, string>();

/**
 * Pending threadIds from message_received, keyed by lowercase Slack channel ID.
 * Consumed by agentStart to promote channel-level sessionKeys to thread-scoped keys.
 *
 * Safe to use a single-slot-per-channel because OpenClaw serializes runs per channel
 * (lane queue), so only one message is being processed at a time per channel.
 */
const pendingThreadIds = new Map<string, string>();

/**
 * If the raw sessionKey has a stored thread-scoped override, return it.
 * Otherwise return the raw key unchanged.
 */
export function resolveSessionKey(raw: string): string {
  return sessionKeyOverrides.get(raw) || raw;
}

/** Clear module-level maps (for testing) */
export function clearHooksState(): void {
  sessionKeyOverrides.clear();
  pendingThreadIds.clear();
}

/**
 * Extract Slack channel ID from evt.from ("slack:channel:C0A1897AJ79")
 * or evt.metadata.to ("channel:C0A1897AJ79"). Returns lowercase.
 */
function extractSlackChannelId(from?: string, metadata?: any): string | undefined {
  if (typeof from === 'string') {
    const match = from.match(/channel:([A-Z0-9]+)/i);
    if (match) return match[1].toLowerCase();
  }
  if (metadata?.to) {
    const match = String(metadata.to).match(/channel:([A-Z0-9]+)/i);
    if (match) return match[1].toLowerCase();
  }
  return undefined;
}

// ── User identity helper ────────────────────────────────────────

const USELESS_ACCOUNT_IDS = new Set(['undefined', 'default', 'null', '']);

function resolveUserId(accountId?: string, from?: string): string | undefined {
  // ctx.accountId is often "undefined" (webchat) or "default" (telegram) — useless
  if (accountId && !USELESS_ACCOUNT_IDS.has(accountId)) {
    return accountId;
  }
  // evt.from has "telegram:1382891386" on telegram — real user identity
  if (from && from !== 'unknown' && from !== '') {
    return from;
  }
  return undefined;
}

// ── Data extraction helpers ──────────────────────────────────────

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

function extractCostDetails(evt: any): string | undefined {
  const cost = evt.cost ?? evt.usage?.cost ?? evt.lastAssistant?.usage?.cost;
  if (!cost) return undefined;
  if (typeof cost === 'string') return cost;
  if (typeof cost === 'object') return JSON.stringify(cost);
  return undefined;
}

// ── History message normalization ────────────────────────────────

/**
 * Normalize raw historyMessages from OpenClaw into typed HistoryMessage[].
 * Preserves all messages with their roles for structured span input.
 */
function normalizeHistoryMessages(raw: unknown): HistoryMessage[] | undefined {
  if (!Array.isArray(raw) || raw.length === 0) return undefined;

  const messages: HistoryMessage[] = [];
  for (const msg of raw) {
    if (!msg || typeof msg !== 'object') continue;

    const role = String(msg.role ?? 'unknown');
    const content = contentToString(msg.content);
    if (!content && role !== 'system') continue; // skip empty non-system messages

    const entry: HistoryMessage = { role, content };
    if (msg.name) entry.name = String(msg.name);
    messages.push(entry);
  }

  return messages.length > 0 ? messages : undefined;
}

/** Safe wrapper — if normalization throws, return undefined instead of crashing the hook */
function safeNormalizeHistory(raw: unknown): HistoryMessage[] | undefined {
  try {
    return normalizeHistoryMessages(raw);
  } catch {
    return undefined;
  }
}

// ── Tool result extraction from history ─────────────────────────

/**
 * Parse historyMessages from llm_input to find tool_result entries.
 * Returns a map of toolCallId → result string.
 *
 * Handles multiple formats:
 * - Anthropic: {role:"user", content:[{type:"tool_result", tool_use_id:"...", content:"..."}]}
 * - OpenAI:    {role:"tool", tool_call_id:"...", content:"..."}
 * - Generic:   {role:"tool_result", tool_use_id:"...", content:"..."}
 */
function extractToolResultsFromHistory(historyMessages: unknown): Map<string, string> {
  const results = new Map<string, string>();
  if (!Array.isArray(historyMessages)) return results;

  for (const msg of historyMessages) {
    if (!msg || typeof msg !== 'object') continue;

    // Format: {role: "tool", tool_call_id: "...", content: "..."}
    const toolId = msg.tool_call_id ?? msg.tool_use_id ?? msg.toolCallId;
    if ((msg.role === 'tool' || msg.role === 'tool_result') && toolId) {
      results.set(String(toolId), contentToString(msg.content));
      continue;
    }

    // Format: {role: "user", content: [{type: "tool_result", tool_use_id: "...", content: "..."}]}
    if (Array.isArray(msg.content)) {
      for (const block of msg.content) {
        if (!block || typeof block !== 'object') continue;
        if (block.type === 'tool_result' && (block.tool_use_id || block.tool_call_id)) {
          const id = block.tool_use_id ?? block.tool_call_id;
          results.set(String(id), contentToString(block.content));
        }
      }
    }
  }

  return results;
}

function contentToString(content: unknown): string {
  if (typeof content === 'string') return content;
  if (content == null) return '';
  // Handle array content blocks: [{type:"text", text:"..."}]
  if (Array.isArray(content)) {
    return content
      .map((b: any) => (typeof b === 'string' ? b : b?.text ?? JSON.stringify(b)))
      .join('\n');
  }
  return JSON.stringify(content);
}

// ── Discovery hooks ─────────────────────────────────────────────
// These hooks have never been confirmed to fire in production.
// We register handlers that emit generic event spans capturing all
// available data, so we can see them in traces if/when they appear.

const DISCOVERY_HOOKS = [
  // Agent lifecycle
  'agent_start', 'agent_error',
  // Tool (alternative naming)
  'tool_call', 'tool_result', 'tool_error',
  // Media
  'media_received', 'media_processed', 'image_received',
  // Outbound messages
  'message_sent', 'message_delivered', 'message_error',
  // Sessions
  'session_start', 'session_end', 'session_created',
  // Cron
  'cron_start', 'cron_end', 'cron_trigger',
  // Memory
  'memory_search', 'memory_result',
  // Subagents
  'subagent_start', 'subagent_end',
  // Generic
  'error', 'warning',
] as const;

export function registerDiscoveryHooks(
  api: OpenClawPluginApi,
  resource: IResource,
  onSpansReady: (spans: ReadableSpan[]) => void,
): void {
  let registered = 0;

  for (const hookName of DISCOVERY_HOOKS) {
    try {
      api.on(hookName, (evt: any, ctx: any) => {
        try {
          const sessionKey = ctx?.sessionKey ?? '';
          const sessionId = ctx?.sessionId ?? ctx?.conversationId ?? evt?.sessionId ?? sessionKey;
          const traceId = traceIdFromSession(sessionKey || sessionId || `discovery-${hookName}`);

          // Try to find a parent agent span via sessionKey + agentId
          const parentSpanId = undefined; // no reliable way to look up without buffer access

          const span = buildDiscoveryEventSpan(
            hookName,
            evt ?? {},
            ctx ?? {},
            sessionId,
            traceId,
            randomSpanId(),
            parentSpanId,
            Date.now(),
            resource,
          );

          onSpansReady([span]);

          if (api.logger) {
            api.logger.info(`[tracehub:discovery] ★ EMITTED span for "${hookName}" — evt_keys: ${Object.keys(evt ?? {}).join(', ')}`);
          }
        } catch (err: any) {
          if (api.logger) {
            api.logger.error(`[tracehub:discovery] Error handling "${hookName}": ${err.message}`);
          }
        }
      });
      registered++;
    } catch {
      // Hook name not supported by this OpenClaw version
    }
  }

  if (api.logger) {
    api.logger.info(`[tracehub:discovery] Registered ${registered}/${DISCOVERY_HOOKS.length} discovery hooks`);
  }
}
