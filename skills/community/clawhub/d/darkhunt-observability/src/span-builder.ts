import {
  SpanKind,
  SpanStatusCode,
  TraceFlags,
  type HrTime,
  type SpanContext,
  type SpanStatus,
  type SpanAttributes,
} from '@opentelemetry/api';
import type { ReadableSpan } from '@opentelemetry/sdk-trace-base';
import type { IResource } from '@opentelemetry/resources';
import type {
  BufferedAgent,
  BufferedGeneration,
  BufferedTool,
  MessageInData,
  AgentEndData,
  LlmOutputData,
  ToolEndData,
  PayloadMode,
} from './types.js';
import { INSTRUMENTATION_LIBRARY } from './types.js';
import {
  applyPayloadMode,
  enforceSpanSizeLimit,
  sanitizeToolParams,
  sanitizeToolResult,
  formatToolInput,
  cleanToolResult,
  cleanGenerationOutput,
  cleanGenerationInput,
  resolveUserDisplayId,
} from './payload.js';
import type { UserIdentity, ChannelIdentity } from './types.js';

// ── Time helpers ───────────────────────────────────────────────────

export function msToHrTime(epochMs: number): HrTime {
  const seconds = Math.floor(epochMs / 1000);
  const nanos = (epochMs % 1000) * 1_000_000;
  return [seconds, nanos];
}

function hrTimeDiff(start: HrTime, end: HrTime): HrTime {
  let seconds = end[0] - start[0];
  let nanos = end[1] - start[1];
  if (nanos < 0) {
    seconds -= 1;
    nanos += 1_000_000_000;
  }
  return [seconds, nanos];
}

// ── Base span factory ──────────────────────────────────────────────

interface SpanOpts {
  name: string;
  traceId: string;
  spanId: string;
  parentSpanId?: string;
  startTime: HrTime;
  endTime: HrTime;
  status: SpanStatus;
  attributes: SpanAttributes;
  resource: IResource;
}

function createReadableSpan(opts: SpanOpts): ReadableSpan {
  const spanContext: SpanContext = {
    traceId: opts.traceId,
    spanId: opts.spanId,
    traceFlags: TraceFlags.SAMPLED,
  };

  return {
    name: opts.name,
    kind: SpanKind.INTERNAL,
    spanContext: () => spanContext,
    parentSpanId: opts.parentSpanId,
    startTime: opts.startTime,
    endTime: opts.endTime,
    status: opts.status,
    attributes: opts.attributes,
    links: [],
    events: [],
    duration: hrTimeDiff(opts.startTime, opts.endTime),
    ended: true,
    resource: opts.resource,
    instrumentationLibrary: INSTRUMENTATION_LIBRARY,
    droppedAttributesCount: 0,
    droppedEventsCount: 0,
    droppedLinksCount: 0,
  };
}

// ── Span type factories ────────────────────────────────────────────

export function buildAgentSpan(
  buffered: BufferedAgent,
  endData: AgentEndData,
  resource: IResource,
): ReadableSpan {
  const endTime = msToHrTime(endData.ts);

  const attrs: Record<string, string | number | boolean | string[]> = {
    'openclaw.observation.type': 'agent',
    'openclaw.session.id': buffered.sessionId,
    'openclaw.session.key': buffered.sessionKey,
    'openclaw.agent.id': buffered.agentId,
  };

  // User identity: prefer resolved identity over raw accountId
  const agentUserId = resolveUserDisplayId(buffered.userIdentity) || buffered.accountId;
  if (agentUserId) attrs['user.id'] = agentUserId;
  applyIdentityAttrs(attrs, buffered.userIdentity, buffered.channelIdentity);

  // Metadata — individual keyed attributes for Langfuse NUI display + filtering
  applyLangfuseObservationMetadata(attrs, buffered.userIdentity, buffered.channelIdentity, buffered.agentId);
  // Trace-level metadata (agent is the root span — sets filterable trace metadata)
  applyLangfuseTraceMetadata(attrs, buffered.userIdentity, buffered.channelIdentity);

  if (buffered.runId) attrs['openclaw.run.id'] = buffered.runId;
  const agentSvcVersion = resource.attributes['service.version'];
  if (agentSvcVersion) attrs['service.version'] = String(agentSvcVersion);
  if (buffered.traceName) attrs['openclaw.trace.name'] = buffered.traceName;
  if (buffered.traceTags) attrs['openclaw.trace.tags'] = buffered.traceTags;
  if (buffered.channel) attrs['openclaw.channel'] = buffered.channel;

  let status: SpanStatus = { code: SpanStatusCode.UNSET };
  if (!endData.success) {
    status = {
      code: SpanStatusCode.ERROR,
      message: endData.error ?? 'agent failed',
    };
    attrs['openclaw.observation.level'] = 'ERROR';
    if (endData.error) attrs['openclaw.observation.status_message'] = endData.error;
  } else {
    attrs['openclaw.observation.level'] = 'DEFAULT';
  }

  return createReadableSpan({
    name: `agent ${buffered.agentId}`,
    traceId: buffered.traceId,
    spanId: buffered.spanId,
    startTime: buffered.startTime,
    endTime,
    status,
    attributes: attrs as SpanAttributes,
    resource,
  });
}

export function buildGenerationSpan(
  buffered: BufferedGeneration,
  endData: LlmOutputData,
  resource: IResource,
  payloadMode: PayloadMode,
  firstTokenTs?: number,
): ReadableSpan {
  const endTime = msToHrTime(endData.ts);

  const attrs: Record<string, string | number | boolean | string[]> = {
    'openclaw.observation.type': 'generation',
    'openclaw.observation.model.name': endData.model || buffered.model,
    'gen_ai.request.model': endData.model || buffered.model,
    'gen_ai.system': endData.provider || buffered.provider,
  };

  // Raw model identifier (full ARN) for traceability
  const rawModel = endData.rawModel || buffered.rawModel;
  if (rawModel) attrs['gen_ai.request.model.raw'] = rawModel;

  if (buffered.sessionId) attrs['openclaw.session.id'] = buffered.sessionId;

  // No user.id on generation spans — these are agent-internal operations
  // Human user identity is on the parent agent span only

  // Belt-and-suspenders: set service.version on span attrs too
  const svcVersion = resource.attributes['service.version'];
  if (svcVersion) attrs['service.version'] = String(svcVersion);

  // Tokens (always included)
  if (endData.inputTokens != null) attrs['gen_ai.usage.input_tokens'] = endData.inputTokens;
  if (endData.outputTokens != null) attrs['gen_ai.usage.output_tokens'] = endData.outputTokens;
  if (endData.cacheReadInputTokens != null) attrs['gen_ai.usage.cache_read_input_tokens'] = endData.cacheReadInputTokens;
  if (endData.cacheCreationInputTokens != null) attrs['gen_ai.usage.cache_creation_input_tokens'] = endData.cacheCreationInputTokens;

  // tokens.total — sum of all token components
  const totalTokens = (endData.inputTokens ?? 0) + (endData.outputTokens ?? 0)
    + (endData.cacheReadInputTokens ?? 0) + (endData.cacheCreationInputTokens ?? 0);
  if (totalTokens > 0) attrs['gen_ai.usage.total_tokens'] = totalTokens;

  // Cost (always included)
  if (endData.costTotal != null) attrs['openclaw.cost.total'] = endData.costTotal;
  if (endData.costDetails) {
    attrs['openclaw.observation.cost_details'] = endData.costDetails;
    // Parse cost breakdown for individual cost attributes
    try {
      const cd = JSON.parse(endData.costDetails);
      if (cd.input != null) attrs['openclaw.cost.input'] = cd.input;
      if (cd.output != null) attrs['openclaw.cost.output'] = cd.output;
      const cacheReadCost = cd.cache_read ?? cd.cacheRead;
      if (cacheReadCost != null) attrs['openclaw.cost.cache_read'] = cacheReadCost;
    } catch { /* ignore parse errors */ }
  }

  // Content metadata (always included)
  if (buffered.inputLength != null) attrs['openclaw.observation.input_length'] = buffered.inputLength;
  if (endData.outputLength != null) attrs['openclaw.observation.output_length'] = endData.outputLength;
  if (buffered.systemPromptLength != null) attrs['openclaw.observation.system_prompt_length'] = buffered.systemPromptLength;
  if (buffered.historyLength != null) attrs['openclaw.observation.history_length'] = buffered.historyLength;

  // Stop reason (always included)
  if (endData.stopReason) {
    attrs['openclaw.stop_reason'] = endData.stopReason;
    attrs['gen_ai.response.finish_reasons'] = [endData.stopReason];
  }

  // Timing — prefer runtime firstTokenTs (precise streaming event) over completionStartTime
  if (firstTokenTs) {
    const startMs = buffered.startTime[0] * 1000 + buffered.startTime[1] / 1_000_000;
    const ttft = Math.round(firstTokenTs - startMs);
    if (ttft > 0) attrs['openclaw.timing.time_to_first_token_ms'] = ttft;
  } else if (endData.completionStartTime) {
    attrs['openclaw.observation.completion_start_time'] = endData.completionStartTime;
    const completionMs = new Date(endData.completionStartTime).getTime();
    const startMs = buffered.startTime[0] * 1000 + buffered.startTime[1] / 1_000_000;
    const ttft = Math.round(completionMs - startMs);
    if (ttft > 0) attrs['openclaw.timing.time_to_first_token_ms'] = ttft;
  }
  if (buffered.attempt != null) attrs['openclaw.observation.attempt'] = buffered.attempt;

  // Content (mode-dependent) — structured message array for classification
  const structuredInput = buildStructuredInput(buffered);
  if (structuredInput) {
    attrs['openclaw.observation.input'] = structuredInput;
  }
  const cleanedOutput = cleanGenerationOutput(endData.output);
  if (cleanedOutput) {
    attrs['openclaw.observation.output'] = JSON.stringify([{ role: 'assistant', content: cleanedOutput }]);
  }
  if (buffered.systemPrompt) {
    attrs['openclaw.observation.system_prompt'] = buffered.systemPrompt;
  }
  if (buffered.modelParameters) attrs['openclaw.observation.model.parameters'] = buffered.modelParameters;

  // Metadata — individual keyed attributes for Langfuse NUI display + filtering
  applyLangfuseObservationMetadata(attrs, buffered.userIdentity, buffered.channelIdentity, buffered.agentId);

  // Apply payload mode + size limits
  const finalAttrs = enforceSpanSizeLimit(applyPayloadMode(attrs, payloadMode));

  let status: SpanStatus = { code: SpanStatusCode.UNSET };
  if (endData.error) {
    status = { code: SpanStatusCode.ERROR, message: endData.error };
    finalAttrs['openclaw.observation.level'] = 'ERROR';
    finalAttrs['openclaw.observation.status_message'] = endData.error;
  } else {
    finalAttrs['openclaw.observation.level'] = 'DEFAULT';
  }

  return createReadableSpan({
    name: `generation ${endData.model || buffered.model}`,
    traceId: buffered.traceId,
    spanId: buffered.spanId,
    parentSpanId: buffered.parentSpanId,
    startTime: buffered.startTime,
    endTime,
    status,
    attributes: finalAttrs as SpanAttributes,
    resource,
  });
}

export type ToolResultSource = 'history' | 'hook' | 'none';

export function buildToolSpan(
  buffered: BufferedTool,
  endData: ToolEndData,
  resource: IResource,
  payloadMode: PayloadMode,
  toolResult?: string,
  resultSource: ToolResultSource = 'none',
): ReadableSpan {
  const endTime = msToHrTime(endData.ts);

  const attrs: Record<string, string | number | boolean | string[]> = {
    'openclaw.observation.type': 'tool',
    'gen_ai.tool.name': buffered.toolName,
    'gen_ai.tool.call.id': buffered.toolCallId,
    'openclaw.tool.success': endData.success,
    'openclaw.tool.result_source': resultSource,
  };

  if (buffered.sessionId) attrs['openclaw.session.id'] = buffered.sessionId;
  // Tool spans are internal agent operations — no human user.id
  // (inherits from parent agent span in the trace)
  if (buffered.model) attrs['gen_ai.request.model'] = buffered.model;
  if (buffered.attempt != null) attrs['openclaw.tool.attempt'] = buffered.attempt;
  if (buffered.meta) attrs['openclaw.tool.meta'] = buffered.meta;
  const toolSvcVersion = resource.attributes['service.version'];
  if (toolSvcVersion) attrs['service.version'] = String(toolSvcVersion);

  // Identity metadata — same as generation/agent spans for consistent filtering
  applyLangfuseObservationMetadata(attrs, buffered.userIdentity, buffered.channelIdentity, buffered.agentId);

  // Tool parameters (mode-dependent + safe-tool allowlist)
  const sanitized = sanitizeToolParams(buffered.toolName, buffered.parameters, payloadMode);
  if (sanitized) attrs['openclaw.tool.parameters'] = sanitized;

  // Tool input — populate REQUEST section with the primary argument (command, path, etc.)
  const toolInput = formatToolInput(buffered.toolName, buffered.parameters);
  if (toolInput) {
    attrs['openclaw.observation.input'] = JSON.stringify([{ role: 'user', content: toolInput }]);
  }

  // Tool result — clean content wrappers, then sanitize for RESPONSE section
  const cleaned = cleanToolResult(toolResult);
  const sanitizedResult = sanitizeToolResult(buffered.toolName, cleaned ?? toolResult, payloadMode);
  if (sanitizedResult) {
    attrs['openclaw.observation.output'] = JSON.stringify([{ role: 'tool', content: sanitizedResult }]);
  }

  const finalAttrs = enforceSpanSizeLimit(attrs);

  let status: SpanStatus = { code: SpanStatusCode.UNSET };
  if (!endData.success) {
    status = {
      code: SpanStatusCode.ERROR,
      message: endData.error ?? 'tool failed',
    };
    finalAttrs['openclaw.observation.level'] = 'ERROR';
    if (endData.error) finalAttrs['openclaw.observation.status_message'] = endData.error;
  } else {
    finalAttrs['openclaw.observation.level'] = 'DEFAULT';
  }

  return createReadableSpan({
    name: buffered.toolName,
    traceId: buffered.traceId,
    spanId: buffered.spanId,
    parentSpanId: buffered.parentSpanId,
    startTime: buffered.startTime,
    endTime,
    status,
    attributes: finalAttrs as SpanAttributes,
    resource,
  });
}

// ── Conversation event spans ──────────────────────────────────────

export function buildConversationEventSpan(
  role: string,
  content: string,
  index: number,
  sessionId: string,
  traceId: string,
  spanId: string,
  parentSpanId: string,
  ts: number,
  resource: IResource,
): ReadableSpan {
  const time = msToHrTime(ts);

  const attrs: SpanAttributes = {
    'openclaw.observation.type': 'event',
    'openclaw.observation.level': 'DEFAULT',
    'openclaw.conversation.role': role,
    'openclaw.conversation.content': content,
    'openclaw.conversation.index': index,
    'openclaw.session.id': sessionId,
  };

  return createReadableSpan({
    name: `conversation.${role}`,
    traceId,
    spanId,
    parentSpanId,
    startTime: time,
    endTime: time, // zero-duration event
    status: { code: SpanStatusCode.UNSET },
    attributes: attrs,
    resource,
  });
}

// ── Discovery event spans ─────────────────────────────────────────

/**
 * Build a generic event span for hooks we suspect exist but haven't confirmed.
 * Captures all event/context data as attributes for later analysis.
 */
export function buildDiscoveryEventSpan(
  hookName: string,
  evt: Record<string, unknown>,
  ctx: Record<string, unknown>,
  sessionId: string,
  traceId: string,
  spanId: string,
  parentSpanId: string | undefined,
  ts: number,
  resource: IResource,
): ReadableSpan {
  const time = msToHrTime(ts);

  const attrs: SpanAttributes = {
    'openclaw.observation.type': 'event',
    'openclaw.observation.level': 'DEFAULT',
    'openclaw.hook.name': hookName,
    'openclaw.session.id': sessionId,
  };

  // Capture event data as attributes (top-level scalars only, to avoid huge payloads)
  for (const [k, v] of Object.entries(evt)) {
    if (v == null) continue;
    const key = `openclaw.hook.evt.${k}`;
    if (typeof v === 'string') attrs[key] = v.slice(0, 1000);
    else if (typeof v === 'number' || typeof v === 'boolean') attrs[key] = v;
    else attrs[key] = JSON.stringify(v).slice(0, 500);
  }

  for (const [k, v] of Object.entries(ctx)) {
    if (v == null) continue;
    const key = `openclaw.hook.ctx.${k}`;
    if (typeof v === 'string') attrs[key] = v.slice(0, 1000);
    else if (typeof v === 'number' || typeof v === 'boolean') attrs[key] = v;
    else attrs[key] = JSON.stringify(v).slice(0, 500);
  }

  // Derive status from error fields
  const hasError = evt.error || ctx.error;
  const status: SpanStatus = hasError
    ? { code: SpanStatusCode.ERROR, message: String(evt.error ?? ctx.error) }
    : { code: SpanStatusCode.UNSET };

  if (hasError) attrs['openclaw.observation.level'] = 'ERROR';

  return createReadableSpan({
    name: hookName,
    traceId,
    spanId,
    parentSpanId,
    startTime: time,
    endTime: time, // zero-duration event
    status,
    attributes: attrs,
    resource,
  });
}

// ── Generation input builder ─────────────────────────────────────

/**
 * Build the generation span input.
 *
 * Priority order:
 * 1. cleanUserMessage from message_received hook — ground truth, pre-prompt
 * 2. Regex-cleaned evt.prompt — strips System: prefixes, thread history, metadata
 * 3. Raw evt.prompt truncated — last resort
 */
function buildStructuredInput(buffered: BufferedGeneration): string | undefined {
  // Priority 1: clean user message from message_received (pre-prompt, no metadata)
  if (buffered.cleanUserMessage) {
    return JSON.stringify([{ role: 'user', content: deduplicateContent(buffered.cleanUserMessage) }]);
  }

  // Priority 2: regex-cleaned evt.prompt (strips System: prefix, thread history, etc.)
  const cleaned = cleanGenerationInput(buffered.input);
  if (cleaned) {
    return JSON.stringify([{ role: 'user', content: cleaned }]);
  }

  // Priority 3: raw prompt truncated (last resort)
  if (buffered.input) {
    const truncated = buffered.input.length > 500
      ? buffered.input.slice(0, 500) + '...'
      : buffered.input;
    return JSON.stringify([{ role: 'user', content: truncated }]);
  }

  return undefined;
}

// ── Identity attribute helpers ────────────────────────────────────

/** Apply user and channel identity attributes to a span */
function applyIdentityAttrs(
  attrs: Record<string, string | number | boolean | string[]>,
  user?: UserIdentity,
  channel?: ChannelIdentity,
): void {
  if (user) {
    if (user.fullName) attrs['openclaw.user.full_name'] = user.fullName;
    if (user.email) attrs['openclaw.user.email'] = user.email;
    if (user.slackUserId) attrs['openclaw.user.slack_id'] = user.slackUserId;
    if (user.slackUsername) attrs['openclaw.user.slack_username'] = user.slackUsername;
    if (user.displayName) attrs['openclaw.user.display_name'] = user.displayName;
  }
  if (channel) {
    if (channel.name) attrs['openclaw.channel.name'] = channel.name;
    if (channel.id) attrs['openclaw.channel.id'] = channel.id;
    if (channel.provider) attrs['openclaw.channel.provider'] = channel.provider;
  }
}

/**
 * Set metadata on a span using multiple strategies for compatibility:
 *
 * 1. langfuse.observation.metadata.<key> — Langfuse OTLP convention (individual filterable keys)
 * 2. langfuse.trace.metadata.<key> — Langfuse trace-level (only on root/agent span)
 * 3. metadata — JSON string (some backends read this directly)
 * 4. openclaw.observation.metadata — JSON string (Seth may map this)
 *
 * Seth NUI is NOT standard Langfuse — it may use a different mapping.
 * Belt-and-suspenders: try all known conventions so at least one works.
 */
function applyLangfuseObservationMetadata(
  attrs: Record<string, string | number | boolean | string[]>,
  user?: UserIdentity,
  channel?: ChannelIdentity,
  agentId?: string,
): void {
  // Strategy 1: Langfuse individual keyed attributes (filterable)
  const prefix = 'langfuse.observation.metadata';
  if (user) {
    if (user.fullName) attrs[`${prefix}.user_full_name`] = user.fullName.slice(0, 200);
    if (user.email) attrs[`${prefix}.user_email`] = user.email.slice(0, 200);
    if (user.slackUserId) attrs[`${prefix}.user_slack_id`] = user.slackUserId.slice(0, 200);
    if (user.slackUsername) attrs[`${prefix}.user_slack_username`] = user.slackUsername.slice(0, 200);
    if (user.displayName) attrs[`${prefix}.user_display_name`] = user.displayName.slice(0, 200);
  }
  if (channel) {
    if (channel.name) attrs[`${prefix}.channel_name`] = channel.name.slice(0, 200);
    if (channel.id) attrs[`${prefix}.channel_id`] = channel.id.slice(0, 200);
    if (channel.provider) attrs[`${prefix}.channel_provider`] = channel.provider.slice(0, 200);
  }
  if (agentId) attrs[`${prefix}.agent_id`] = agentId.slice(0, 200);

  // Strategy 2: JSON blob under common attribute names (for Seth / non-Langfuse backends)
  const metaJson = buildMetadataJson(user, channel, agentId);
  if (metaJson) {
    attrs['metadata'] = metaJson;
    attrs['openclaw.observation.metadata'] = metaJson;
  }
}

function applyLangfuseTraceMetadata(
  attrs: Record<string, string | number | boolean | string[]>,
  user?: UserIdentity,
  channel?: ChannelIdentity,
): void {
  const prefix = 'langfuse.trace.metadata';
  if (user) {
    if (user.fullName) attrs[`${prefix}.user_full_name`] = user.fullName.slice(0, 200);
    if (user.email) attrs[`${prefix}.user_email`] = user.email.slice(0, 200);
    if (user.slackUserId) attrs[`${prefix}.user_slack_id`] = user.slackUserId.slice(0, 200);
    if (user.slackUsername) attrs[`${prefix}.user_slack_username`] = user.slackUsername.slice(0, 200);
  }
  if (channel) {
    if (channel.name) attrs[`${prefix}.channel_name`] = channel.name.slice(0, 200);
    if (channel.id) attrs[`${prefix}.channel_id`] = channel.id.slice(0, 200);
    if (channel.provider) attrs[`${prefix}.channel_provider`] = channel.provider.slice(0, 200);
  }
}

/** Build a JSON metadata string for backends that read metadata as a blob */
function buildMetadataJson(user?: UserIdentity, channel?: ChannelIdentity, agentId?: string): string | undefined {
  const meta: Record<string, string> = {};
  if (agentId) meta['agent_id'] = agentId;
  if (user) {
    if (user.fullName) meta['user_full_name'] = user.fullName;
    if (user.email) meta['user_email'] = user.email;
    if (user.slackUserId) meta['user_slack_id'] = user.slackUserId;
    if (user.slackUsername) meta['user_slack_username'] = user.slackUsername;
  }
  if (channel) {
    if (channel.name) meta['channel_name'] = channel.name;
    if (channel.id) meta['channel_id'] = channel.id;
    if (channel.provider) meta['channel_provider'] = channel.provider;
  }
  return Object.keys(meta).length > 0 ? JSON.stringify(meta) : undefined;
}

/** Remove duplicated content — OpenClaw often sends "msg\n\nmsg" or "msg\n\n msg" */
function deduplicateContent(content: string): string {
  const parts = content.split(/\n\n\s*/);
  if (parts.length === 2 && parts[0].trim() === parts[1].trim()) {
    return parts[0].trim();
  }
  return content;
}

export function buildMessageSpan(
  data: MessageInData,
  traceId: string,
  spanId: string,
  resource: IResource,
): ReadableSpan {
  const time = msToHrTime(data.ts);

  const userDisplayId = resolveUserDisplayId(data.userIdentity) || data.accountId;
  const attrs: Record<string, string | number | boolean | string[]> = {
    'openclaw.observation.type': 'event',
    'openclaw.observation.level': 'DEFAULT',
    'openclaw.session.id': data.sessionId,
    'openclaw.channel': data.channel,
    'openclaw.message.from': data.from,
    'openclaw.message.content_length': data.contentLength,
  };
  if (userDisplayId) attrs['user.id'] = userDisplayId;
  applyIdentityAttrs(attrs, data.userIdentity, data.channelIdentity);

  return createReadableSpan({
    name: `message.in ${data.channelIdentity?.name || data.channel}`,
    traceId,
    spanId,
    startTime: time,
    endTime: time, // zero-duration
    status: { code: SpanStatusCode.UNSET },
    attributes: attrs,
    resource,
  });
}
