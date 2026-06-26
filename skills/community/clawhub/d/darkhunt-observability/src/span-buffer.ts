import type { ReadableSpan } from '@opentelemetry/sdk-trace-base';
import type { IResource } from '@opentelemetry/resources';
import type {
  PayloadMode,
  BufferedAgent,
  BufferedGeneration,
  BufferedTool,
  MessageInData,
  AgentStartData,
  AgentEndData,
  LlmInputData,
  LlmOutputData,
  ToolStartData,
  ToolEndData,
  UserIdentity,
  ChannelIdentity,
} from './types.js';
import { traceIdFromSession, randomSpanId } from './trace-id.js';
import { cleanGenerationOutput } from './payload.js';
import {
  buildAgentSpan,
  buildGenerationSpan,
  buildToolSpan,
  buildMessageSpan,
  buildConversationEventSpan,
  buildDiscoveryEventSpan,
  msToHrTime,
} from './span-builder.js';

export type SpansReadyCallback = (spans: ReadableSpan[]) => void;

interface CompletedTool {
  buffered: BufferedTool;
  endData: ToolEndData;
}

let bufferCounter = 0;

// ── Shared state across all SpanBuffer instances ────────────────
// OpenClaw creates a new plugin instance (and SpanBuffer) per agent run.
// User/channel identity must be shared so the agent-run instance can
// read what the message_received instance stored.
const sharedUserIdentities = new Map<string, UserIdentity>();
let sharedLatestUserIdentity: UserIdentity | undefined;
const sharedChannelIdentities = new Map<string, ChannelIdentity>();
let sharedLatestChannelIdentity: ChannelIdentity | undefined;
// Clean user message also shared (message_received → llm_input cross-instance)
const sharedLastUserMessages = new Map<string, string>();
let sharedLastCleanMessageGlobal: string | undefined;
// AccountId also shared
const sharedSessionAccountIds = new Map<string, string>();
let sharedLatestAccountId: string | undefined;
// Deferred message.in spans — stored when message_received has no sessionKey,
// emitted when agentStart provides the real session key. Keyed by threadKey (channelId:threadId).
const sharedPendingMessages = new Map<string, MessageInData>();

/** Clear all shared module-level state (for testing) */
export function clearSharedState(): void {
  sharedUserIdentities.clear();
  sharedLatestUserIdentity = undefined;
  sharedChannelIdentities.clear();
  sharedLatestChannelIdentity = undefined;
  sharedLastUserMessages.clear();
  sharedLastCleanMessageGlobal = undefined;
  sharedSessionAccountIds.clear();
  sharedLatestAccountId = undefined;
  sharedPendingMessages.clear();
}

export class SpanBuffer {
  public _debugId = ++bufferCounter;
  private agents = new Map<string, BufferedAgent>();
  private generations = new Map<string, BufferedGeneration>();
  private tools = new Map<string, BufferedTool>();
  // Track which tool.end calls we've seen (for deduplication)
  private toolEndSeen = new Map<string, boolean>();
  // Tools that have ended but await result from next llm_input
  private completedTools = new Map<string, CompletedTool>();
  // AccountId uses shared module-level maps (see above)
  // Fallback: most recent sessionId (for cron/background agents that lack session context)
  private latestSessionId?: string;
  // Runtime event data: runId from onAgentEvent lifecycle start, keyed by sessionKey
  private runtimeRunIds = new Map<string, string>();
  // Runtime event data: tool meta from onAgentEvent tool result, keyed by toolCallId
  private runtimeToolMeta = new Map<string, string>();
  // Runtime event data: first assistant token timestamp, keyed by runId
  private runtimeFirstTokenTs = new Map<string, number>();
  // Conversation dedup: fingerprints of emitted messages per session
  // Fingerprint = role + ":" + first 200 chars of content (avoids re-emitting on array mutations)
  private emittedMessageFingerprints = new Map<string, Set<string>>();
  // Clean user message uses shared module-level maps (see above)
  // Track whether system prompt has been emitted for this session
  private systemPromptEmitted = new Set<string>();
  // User/channel identity uses shared module-level maps (see above)

  constructor(
    private resource: IResource,
    private payloadMode: PayloadMode,
    private onSpansReady: SpansReadyCallback,
  ) {}

  // ── Runtime event ingestion (from onAgentEvent) ────────────────

  onRuntimeEvent(event: {
    runId: string;
    stream: string;
    data: any;
    sessionKey: string;
    ts: number;
  }): void {
    const { runId, stream, data, sessionKey } = event;

    // ── lifecycle stream ────────────────────────────────────────
    if (stream === 'lifecycle') {
      if (data?.phase === 'start') {
        // Store runId for this sessionKey so we can attach it to agent spans
        this.runtimeRunIds.set(sessionKey, runId);
        // Attach runId to existing agent buffer if it's already been created by the hook
        for (const [, agent] of this.agents) {
          if (agent.sessionKey === sessionKey && !agent.runId) {
            agent.runId = runId;
          }
        }
      }
      // lifecycle.end/error — not emitted (empty after OTLP mapping, duplicates agent span)
      return;
    }

    // ── tool stream ─────────────────────────────────────────────
    if (stream === 'tool') {
      if (data?.phase === 'result' && data?.toolCallId) {
        // Store meta description for tool spans
        if (data.meta) {
          this.runtimeToolMeta.set(data.toolCallId, data.meta);
        }
      }
      // tool.start/error — not emitted (empty after OTLP mapping, duplicates tool span)
      return;
    }

    // ── assistant stream ────────────────────────────────────────
    if (stream === 'assistant') {
      if (data?.delta) {
        // First assistant token — record timestamp for TTFT calculation
        if (!this.runtimeFirstTokenTs.has(runId)) {
          this.runtimeFirstTokenTs.set(runId, event.ts);
        }
      }
      // Don't emit individual streaming tokens as spans (too noisy)
      return;
    }

    // Unknown streams — not emitted (empty after OTLP mapping)
  }

  /** Emit a discovery event span for runtime event streams we don't have dedicated handling for */
  private emitRuntimeDiscoveryEvent(
    name: string,
    event: { runId: string; stream: string; data: any; sessionKey: string; ts: number },
  ): void {
    const traceId = traceIdFromSession(event.sessionKey || `runtime-${event.runId}`);
    const sessionId = event.sessionKey || '';

    // Find parent agent span if possible
    let parentSpanId: string | undefined;
    for (const [, agent] of this.agents) {
      if (agent.sessionKey === event.sessionKey) {
        parentSpanId = agent.spanId;
        break;
      }
    }

    const span = buildDiscoveryEventSpan(
      name,
      {
        runId: event.runId,
        stream: event.stream,
        ...(event.data ?? {}),
      },
      { sessionKey: event.sessionKey },
      sessionId,
      traceId,
      randomSpanId(),
      parentSpanId,
      event.ts,
      this.resource,
    );
    this.onSpansReady([span]);
  }

  // ── Session transcript updates ─────────────────────────────────

  /**
   * Handle session transcript updates from runtime.events.onSessionTranscriptUpdate.
   * Not emitted as spans — transcript.update fires frequently and arrives empty
   * after OTLP mapping (no content, just IDs). The actual content is already
   * captured in generation and tool spans.
   */
  onTranscriptUpdate(_event: {
    sessionKey?: string;
    sessionId?: string;
    messages?: any[];
    [key: string]: unknown;
  }): void {
    // No-op: suppressed to reduce noise
  }

  /** Get internal map sizes for monitoring/testing */
  getStats(): Record<string, number> {
    return {
      agents: this.agents.size,
      generations: this.generations.size,
      tools: this.tools.size,
      toolEndSeen: this.toolEndSeen.size,
      completedTools: this.completedTools.size,
      sharedSessionAccountIds: sharedSessionAccountIds.size,
      runtimeRunIds: this.runtimeRunIds.size,
      runtimeToolMeta: this.runtimeToolMeta.size,
      runtimeFirstTokenTs: this.runtimeFirstTokenTs.size,
      emittedMessageFingerprints: this.emittedMessageFingerprints.size,
      sharedLastUserMessages: sharedLastUserMessages.size,
      systemPromptEmitted: this.systemPromptEmitted.size,
      sharedPendingMessages: sharedPendingMessages.size,
    };
  }

  /** Clean up all session-scoped tracking state for a given sessionKey */
  private cleanupSession(sessionKey: string, sessionId?: string): void {
    // Clean session account IDs — messageIn stores under sessionId, sessionKey,
    // and conversationId. We collect all keys used during storeAccountId via
    // a reverse lookup: delete any key whose stored value matches our session.
    const accountId = sharedSessionAccountIds.get(sessionKey);
    if (accountId) {
      for (const [key, val] of sharedSessionAccountIds) {
        if (val === accountId) {
          sharedSessionAccountIds.delete(key);
        }
      }
    }
    sharedSessionAccountIds.delete(sessionKey);
    if (sessionId) sharedSessionAccountIds.delete(sessionId);

    this.runtimeRunIds.delete(sessionKey);
    this.runtimeFirstTokenTs.delete(sessionKey);
    this.emittedMessageFingerprints.delete(sessionKey);
    sharedLastUserMessages.delete(sessionKey);
    this.systemPromptEmitted.delete(sessionKey);
    sharedUserIdentities.delete(sessionKey);
    sharedChannelIdentities.delete(sessionKey);
    // Clean pending message for this session's thread
    const threadKey = extractThreadKey(sessionKey);
    if (threadKey) sharedPendingMessages.delete(threadKey);
    if (sessionId) {
      sharedUserIdentities.delete(sessionId);
      sharedChannelIdentities.delete(sessionId);
    }
  }

  /** Get runtime runId for a sessionKey */
  getRuntimeRunId(sessionKey: string): string | undefined {
    return this.runtimeRunIds.get(sessionKey);
  }

  /** Get and consume tool meta for a toolCallId */
  consumeToolMeta(toolCallId: string): string | undefined {
    const meta = this.runtimeToolMeta.get(toolCallId);
    if (meta) this.runtimeToolMeta.delete(toolCallId);
    return meta;
  }

  /** Get and consume first-token timestamp for a runId */
  consumeFirstTokenTs(runId: string): number | undefined {
    const ts = this.runtimeFirstTokenTs.get(runId);
    if (ts) this.runtimeFirstTokenTs.delete(runId);
    return ts;
  }

  // ── Message (immediate, no buffering) ──────────────────────────

  onMessageIn(data: MessageInData): void {
    // Store accountId for this session so generation/tool spans can use it
    if (data.accountId) {
      sharedSessionAccountIds.set(data.sessionId, data.accountId);
      if (data.sessionKey) sharedSessionAccountIds.set(data.sessionKey, data.accountId);
      sharedLatestAccountId = data.accountId;
    }

    // When sessionKey is missing (message_received doesn't provide ctx.sessionKey),
    // defer the span emission until agentStart provides the real session key.
    // This prevents the message.in span from landing in a different trace.
    if (!data.sessionKey && data.threadKey) {
      sharedPendingMessages.set(data.threadKey, data);
      return;
    }

    // Use sessionKey as the canonical session identity (includes thread IDs)
    const effectiveSessionId = data.sessionKey || data.sessionId;
    if (effectiveSessionId) {
      this.latestSessionId = effectiveSessionId;
    }
    const traceId = traceIdFromSession(effectiveSessionId);
    const spanId = randomSpanId();
    // Override sessionId with sessionKey for span attributes so Seth groups by thread
    const spanData = { ...data, sessionId: effectiveSessionId };
    const span = buildMessageSpan(spanData, traceId, spanId, this.resource);
    this.onSpansReady([span]);
  }

  /** Store accountId under additional keys (called from hooks-adapter for cross-hook matching) */
  storeAccountId(key: string, accountId: string): void {
    if (key) sharedSessionAccountIds.set(key, accountId);
  }

  /** Store user identity for a session key (shared across all buffer instances) */
  storeUserIdentity(key: string, identity: UserIdentity): void {
    if (key) {
      const existing = sharedUserIdentities.get(key);
      if (existing) {
        const merged = { ...identity };
        for (const [k, v] of Object.entries(existing)) {
          if (v && !(merged as any)[k]) (merged as any)[k] = v;
        }
        sharedUserIdentities.set(key, merged);
        sharedLatestUserIdentity = merged;
      } else {
        sharedUserIdentities.set(key, identity);
        sharedLatestUserIdentity = identity;
      }
    }
  }

  /** Store channel identity for a session key (shared across all buffer instances) */
  storeChannelIdentity(key: string, identity: ChannelIdentity): void {
    if (key) {
      const existing = sharedChannelIdentities.get(key);
      if (existing) {
        const merged = { ...identity };
        for (const [k, v] of Object.entries(existing)) {
          if (v && !(merged as any)[k]) (merged as any)[k] = v;
        }
        sharedChannelIdentities.set(key, merged);
        sharedLatestChannelIdentity = merged;
      } else {
        sharedChannelIdentities.set(key, identity);
        sharedLatestChannelIdentity = identity;
      }
    }
  }

  /** Get user identity for a session key, with global fallback */
  getUserIdentity(sessionKey: string): UserIdentity | undefined {
    return sharedUserIdentities.get(sessionKey) ?? sharedLatestUserIdentity;
  }

  /** Get channel identity for a session key, with global fallback */
  getChannelIdentity(sessionKey: string): ChannelIdentity | undefined {
    return sharedChannelIdentities.get(sessionKey) ?? sharedLatestChannelIdentity;
  }

  /** Store the clean user message from message_received for generation span input */
  storeLastUserMessage(sessionKey: string, content: string): void {
    if (content) {
      if (sessionKey) sharedLastUserMessages.set(sessionKey, content);
      sharedLastCleanMessageGlobal = content;
    }
  }

  /** Return the stored user message — try session key first, fall back to global */
  private getLastUserMessage(sessionKey: string): string | undefined {
    return sharedLastUserMessages.get(sessionKey) ?? sharedLastCleanMessageGlobal;
  }

  // ── Agent lifecycle ────────────────────────────────────────────

  onAgentStart(data: AgentStartData): void {
    const key = this.agentKey(data.sessionKey, data.agentId);
    const spanId = randomSpanId();

    // Get accountId: from agentStart ctx (if available), from stored messageIn, or latest fallback
    const accountId = data.accountId || sharedSessionAccountIds.get(data.sessionKey) || sharedSessionAccountIds.get(data.sessionId) || sharedLatestAccountId;

    // Use sessionKey as canonical session identity (includes thread IDs)
    const effectiveSessionId = data.sessionKey || data.sessionId || this.latestSessionId || '';
    if (effectiveSessionId) this.latestSessionId = effectiveSessionId;
    const traceId = traceIdFromSession(effectiveSessionId);

    this.agents.set(key, {
      sessionId: effectiveSessionId,
      sessionKey: data.sessionKey,
      agentId: data.agentId,
      spanId,
      traceId,
      startTime: msToHrTime(data.ts),
      traceName: data.traceName,
      traceTags: data.traceTags,
      channel: data.channel,
      accountId,
      runId: this.runtimeRunIds.get(data.sessionKey),
      userIdentity: this.getUserIdentity(data.sessionKey),
      channelIdentity: this.getChannelIdentity(data.sessionKey),
    });

    // Emit deferred message.in span — message_received had no sessionKey,
    // now we have the real one from agentStart. Extract channelId:threadId
    // from sessionKey to match the pending message.
    const threadKey = extractThreadKey(data.sessionKey);
    if (threadKey) {
      const pending = sharedPendingMessages.get(threadKey);
      if (pending) {
        sharedPendingMessages.delete(threadKey);
        // Emit the message span with the correct traceId and sessionId
        const msgSpanData = { ...pending, sessionId: effectiveSessionId, sessionKey: data.sessionKey };
        const msgSpan = buildMessageSpan(msgSpanData, traceId, randomSpanId(), this.resource);
        this.onSpansReady([msgSpan]);
      }
    }
  }

  onAgentEnd(data: AgentEndData): void {
    const key = this.agentKey(data.sessionKey, data.agentId);
    const buffered = this.agents.get(key);
    if (!buffered) return;

    // Flush any completed tools still waiting for results
    this.flushCompletedToolsForSession(data.sessionKey);

    // TODO: Re-enable agent span emission once the product handles them properly.
    // Agent spans are the trace hierarchy parent (generation/tool are children).
    // They carry unique data: total agent duration (including tool wait time),
    // channel_id, user_slack_id, and success/failure status.
    //
    // Currently suppressed because:
    // 1. They show as empty cards in the lineage/trace UI (no input/output content)
    // 2. Dual plugin instances cause duplicate agent spans per interaction
    // 3. Orphaned agents from gateway restarts produce stale spans (5+ min duration)
    //
    // Product changes needed to support agent spans:
    // - Trace UI: render agent spans as a "wrapper" row showing duration + metadata,
    //   not as an empty I/O card
    // - Lineage UI: use agent span as the tree root, nest generation/tool under it
    // - Deduplication: either deduplicate by traceId+name in the trace-hub enrichment
    //   pipeline, or suppress emission from the second plugin instance (buffer.id > 1)
    // - Stale handling: filter out agent spans with durationMs > 60000 (orphans from
    //   gateway restarts) in the enrichment pipeline, or show them differently in UI
    //
    // const span = buildAgentSpan(buffered, data, this.resource);
    this.agents.delete(key);

    // Clean up all session-scoped tracking state
    this.cleanupSession(data.sessionKey, buffered.sessionId);
  }

  // ── Generation lifecycle ───────────────────────────────────────

  onLlmInput(data: LlmInputData): void {
    const key = this.generationKey(data.sessionKey, data.runId);
    const agentKey = this.agentKey(data.sessionKey, data.agentId);
    const agent = this.agents.get(agentKey);

    // Backfill: cron jobs have no messageIn, so agentStart may lack sessionId.
    // The LLM event provides evt.sessionId — propagate it to the agent buffer
    // so that subsequent tool spans also get the correct sessionId.
    if (agent && !agent.sessionId && data.sessionId) {
      agent.sessionId = data.sessionId;
    }
    // Propagate model to agent so tool spans can inherit it
    if (agent && data.model) {
      agent.model = data.model;
    }

    const spanId = randomSpanId();

    // Retrieve the clean user message stored by message_received (before prompt construction)
    const cleanUserMessage = this.getLastUserMessage(data.sessionKey);

    this.generations.set(key, {
      spanId,
      parentSpanId: agent?.spanId ?? '',
      traceId: agent?.traceId ?? traceIdFromSession(data.sessionId),
      model: data.model,
      rawModel: data.rawModel,
      provider: data.provider,
      startTime: msToHrTime(data.ts),
      input: data.input,
      inputLength: data.inputLength,
      cleanUserMessage,
      systemPrompt: data.systemPrompt,
      systemPromptLength: data.systemPromptLength,
      historyLength: data.historyLength,
      historyMessages: data.historyMessages,
      modelParameters: data.modelParameters,
      attempt: data.attempt,
      sessionKey: data.sessionKey,
      sessionId: agent?.sessionId ?? (data.sessionKey || data.sessionId) ?? '',
      accountId: agent?.accountId,
      agentId: data.agentId || agent?.agentId,
      userIdentity: this.getUserIdentity(data.sessionKey),
      channelIdentity: this.getChannelIdentity(data.sessionKey),
    });

    // Conversation event spans (system, user, assistant from history) are suppressed —
    // they arrive empty after OTLP mapping and duplicate generation input/output content.
  }

  /** Emit individual conversation event spans for messages not yet sent. */
  private emitConversationEvents(data: LlmInputData, agent: BufferedAgent | undefined): void {
    const messages = data.historyMessages;
    if (!messages || messages.length === 0) return;

    const sessionKey = data.sessionKey;

    // Content-based dedup: track fingerprints of emitted messages.
    // Handles array mutations (moderation, insertion) without re-emitting.
    let fingerprints = this.emittedMessageFingerprints.get(sessionKey);
    if (!fingerprints) {
      fingerprints = new Set();
      this.emittedMessageFingerprints.set(sessionKey, fingerprints);
    }

    const traceId = agent?.traceId ?? traceIdFromSession(data.sessionKey || data.sessionId);
    const parentSpanId = agent?.spanId ?? '';
    const sessionId = agent?.sessionId ?? (data.sessionKey || data.sessionId) ?? '';
    const spans: ReadableSpan[] = [];

    for (let i = 0; i < messages.length; i++) {
      const msg = messages[i];
      // Skip tool messages — they have dedicated tool spans
      if (msg.role === 'tool' || msg.role === 'tool_result') continue;

      const fp = messageFingerprint(msg.role, msg.content);
      if (fingerprints.has(fp)) continue;
      fingerprints.add(fp);

      spans.push(buildConversationEventSpan(
        msg.role,
        msg.content,
        i,
        sessionId,
        traceId,
        randomSpanId(),
        parentSpanId,
        data.ts,
        this.resource,
      ));
    }

    if (spans.length > 0) {
      this.onSpansReady(spans);
    }
  }

  onLlmOutput(data: LlmOutputData): void {
    const key = this.generationKey(data.sessionKey, data.runId);
    const buffered = this.generations.get(key);
    if (!buffered) return;

    // Get first-token timestamp from runtime assistant streaming events
    const runId = this.runtimeRunIds.get(data.sessionKey);
    const firstTokenTs = runId ? this.consumeFirstTokenTs(runId) : undefined;

    const span = buildGenerationSpan(buffered, data, this.resource, this.payloadMode, firstTokenTs);
    this.generations.delete(key);

    // Conversation event spans (tool_call, assistant) suppressed —
    // output content is already in the generation span itself.
    this.onSpansReady([span]);
  }

  // ── Tool lifecycle ─────────────────────────────────────────────

  onToolStart(data: ToolStartData): void {
    const key = this.toolKey(data.sessionKey, data.toolCallId);
    const agentKey = this.agentKey(data.sessionKey, data.agentId);
    const agent = this.agents.get(agentKey);

    const spanId = randomSpanId();
    // Always produce a valid traceId: from agent context, or derive from sessionKey
    const traceId = agent?.traceId || traceIdFromSession(data.sessionKey || `orphan-tool-${data.toolCallId}`);

    this.tools.set(key, {
      spanId,
      parentSpanId: agent?.spanId ?? '',
      traceId,
      toolName: data.toolName,
      toolCallId: data.toolCallId,
      startTime: msToHrTime(data.ts),
      parameters: data.parameters,
      attempt: data.attempt,
      sessionKey: data.sessionKey,
      sessionId: agent?.sessionId ?? '',
      accountId: agent?.accountId,
      agentId: data.agentId || agent?.agentId,
      model: agent?.model,
      meta: this.runtimeToolMeta.get(data.toolCallId),
      userIdentity: agent?.userIdentity ?? this.getUserIdentity(data.sessionKey),
      channelIdentity: agent?.channelIdentity ?? this.getChannelIdentity(data.sessionKey),
    });
  }

  onToolEnd(data: ToolEndData): void {
    const key = this.toolKey(data.sessionKey, data.toolCallId);
    const seenKey = key;

    // Handle dual tool.end: OpenClaw emits two tool.end records per tool.
    // First: {success, toolName}, Second: {success, toolName, durationMs}
    // Only complete the span when durationMs is present, or on the second call.
    if (data.durationMs == null) {
      // Stash result from first event onto the buffered tool — the second event
      // may not carry the result, causing silent data loss.
      if (data.result) {
        const tool = this.tools.get(key);
        if (tool && !tool.stashedResult) {
          tool.stashedResult = data.result;
        }
      }
      if (this.toolEndSeen.has(seenKey)) {
        // Second call without duration — complete anyway
        this.completeToolSpan(key, data);
        this.toolEndSeen.delete(seenKey);
      } else {
        this.toolEndSeen.set(seenKey, true);
      }
      return;
    }

    // Has durationMs — complete the span.
    // If this event lacks a result, recover from the stashed first-event result.
    // Create a copy to avoid mutating the caller's object.
    let endData = data;
    if (!data.result) {
      const tool = this.tools.get(key);
      if (tool?.stashedResult) {
        endData = { ...data, result: tool.stashedResult };
      }
    }
    this.completeToolSpan(key, endData);
    this.toolEndSeen.delete(seenKey);
  }

  /**
   * Mark a tool as completed but hold it for result extraction.
   * The span will be emitted when the next llm_input provides historyMessages
   * containing the tool result, or on agentEnd/flushStale.
   */
  private completeToolSpan(key: string, data: ToolEndData): void {
    const buffered = this.tools.get(key);
    if (!buffered) return;

    this.tools.delete(key);
    this.completedTools.set(key, { buffered, endData: data });
  }

  /**
   * Apply tool results extracted from historyMessages, then emit matched tool spans.
   * Called from hooks-adapter when llm_input provides historyMessages.
   */
  applyToolResults(results: Map<string, string>, sessionKey: string): void {
    if (results.size === 0 && this.completedTools.size === 0) return;

    const toEmit: ReadableSpan[] = [];

    for (const [key, entry] of this.completedTools) {
      if (entry.buffered.sessionKey !== sessionKey) continue;

      // Prefer historyMessages result, fall back to result captured directly from after_tool_call
      const historyResult = results.get(entry.buffered.toolCallId);
      const result = historyResult ?? entry.endData.result;
      const source = historyResult ? 'history' as const : (entry.endData.result ? 'hook' as const : 'none' as const);
      const span = buildToolSpan(entry.buffered, entry.endData, this.resource, this.payloadMode, result, source);
      toEmit.push(span);
      this.completedTools.delete(key);
    }

    if (toEmit.length > 0) {
      this.onSpansReady(toEmit);
    }
  }

  /**
   * Flush completed tools for a session (on agentEnd — no more results coming).
   * Uses result from after_tool_call if available (for single-turn tool use).
   */
  private flushCompletedToolsForSession(sessionKey: string): void {
    const toEmit: ReadableSpan[] = [];

    for (const [key, entry] of this.completedTools) {
      if (entry.buffered.sessionKey === sessionKey) {
        const source = entry.endData.result ? 'hook' as const : 'none' as const;
        const span = buildToolSpan(entry.buffered, entry.endData, this.resource, this.payloadMode, entry.endData.result, source);
        toEmit.push(span);
        this.completedTools.delete(key);
      }
    }

    if (toEmit.length > 0) {
      this.onSpansReady(toEmit);
    }
  }

  // ── Orphan cleanup ─────────────────────────────────────────────

  flushStale(maxAgeMs: number): void {
    const now = Date.now();

    const staleSessions = new Map<string, string | undefined>(); // sessionKey → sessionId

    for (const [key, buffered] of this.agents) {
      const ageMs = now - hrTimeToMs(buffered.startTime);
      if (ageMs > maxAgeMs) {
        staleSessions.set(buffered.sessionKey, buffered.sessionId);
        const endData: AgentEndData = {
          sessionKey: buffered.sessionKey,
          agentId: buffered.agentId,
          success: false,
          durationMs: ageMs,
          error: 'span timed out without end event',
          ts: now,
        };
        const span = buildAgentSpan(buffered, endData, this.resource);
        this.agents.delete(key);
        this.onSpansReady([span]);
      }
    }

    for (const [key, buffered] of this.generations) {
      const ageMs = now - hrTimeToMs(buffered.startTime);
      if (ageMs > maxAgeMs) {
        const endData: LlmOutputData = {
          sessionKey: buffered.sessionKey,
          runId: '',
          model: buffered.model,
          provider: buffered.provider,
          error: 'span timed out without end event',
          ts: now,
        };
        const span = buildGenerationSpan(buffered, endData, this.resource, this.payloadMode);
        this.generations.delete(key);
        this.onSpansReady([span]);
      }
    }

    for (const [key, buffered] of this.tools) {
      const ageMs = now - hrTimeToMs(buffered.startTime);
      if (ageMs > maxAgeMs) {
        const endData: ToolEndData = {
          sessionKey: buffered.sessionKey,
          toolName: buffered.toolName,
          toolCallId: buffered.toolCallId,
          success: false,
          error: 'span timed out without end event',
          ts: now,
        };
        const span = buildToolSpan(buffered, endData, this.resource, this.payloadMode);
        this.tools.delete(key);
        this.onSpansReady([span]);
      }
    }

    // Flush completed tools waiting for results
    for (const [key, entry] of this.completedTools) {
      const ageMs = now - hrTimeToMs(entry.buffered.startTime);
      if (ageMs > maxAgeMs) {
        staleSessions.set(entry.buffered.sessionKey, entry.buffered.sessionId);
        const span = buildToolSpan(entry.buffered, entry.endData, this.resource, this.payloadMode);
        this.completedTools.delete(key);
        this.onSpansReady([span]);
      }
    }

    // Clean up session-scoped tracking state for all evicted sessions
    for (const [sessionKey, sessionId] of staleSessions) {
      this.cleanupSession(sessionKey, sessionId);
    }
  }

  // ── Key helpers ────────────────────────────────────────────────

  private agentKey(sessionKey: string, agentId: string): string {
    return `${sessionKey}:${agentId}`;
  }

  private generationKey(sessionKey: string, runId: string): string {
    return `${sessionKey}:${runId}`;
  }

  private toolKey(sessionKey: string, toolCallId: string): string {
    return `${sessionKey}:${toolCallId}`;
  }
}

function hrTimeToMs(hr: [number, number]): number {
  return hr[0] * 1000 + hr[1] / 1_000_000;
}

/**
 * Content-based fingerprint for conversation dedup.
 * Uses role + first 200 chars of content to avoid re-emitting on array mutations.
 * Trade-off: if a user sends the exact same message twice with the same role,
 * the second is skipped — acceptable for observability (identical events are noise).
 */
function messageFingerprint(role: string, content: string): string {
  return `${role}:${content.slice(0, 200)}`;
}

/**
 * Extract channelId:threadId from an OpenClaw sessionKey.
 * Format: "agent:<name>:slack:channel:<channelId>:thread:<threadId>"
 * Returns "channelId:threadId" or undefined if not parseable.
 */
function extractThreadKey(sessionKey: string): string | undefined {
  const channelMatch = sessionKey.match(/:channel:([^:]+)/);
  const threadMatch = sessionKey.match(/:thread:([^:]+)/);
  if (channelMatch && threadMatch) {
    return `${channelMatch[1]}:${threadMatch[1]}`;
  }
  return undefined;
}
