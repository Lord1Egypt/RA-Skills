import type { HrTime } from '@opentelemetry/api';

// ── Plugin config ──────────────────────────────────────────────────

export type PayloadMode = 'metadata' | 'debug' | 'full';

export interface PluginConfig {
  traces_endpoint: string;
  logs_endpoint?: string;
  headers?: Record<string, string>;
  payload_mode: PayloadMode;
  batch_delay_ms: number;
  batch_max_size: number;
  export_timeout_ms: number;
  enabled: boolean;
  debug?: boolean;
  model_map?: Record<string, string>;
  model_pricing?: Record<string, { input: number; output: number; cacheRead?: number; cacheWrite?: number }>;
}

// ── Structured history message ─────────────────────────────────────

export interface HistoryMessage {
  role: string;        // "user" | "assistant" | "system" | "tool" | "tool_result"
  content: string;     // stringified content
  name?: string;       // tool name for tool messages
}

// ── User & channel identity ───────────────────────────────────────

export interface UserIdentity {
  /** Friendly display name for the User field (e.g. "aleksei.k") */
  displayName?: string;
  /** Full real name (e.g. "Aleksei Kalaitan") */
  fullName?: string;
  /** Email address */
  email?: string;
  /** Slack user ID (e.g. "U098VT61MQ9") */
  slackUserId?: string;
  /** Slack username/handle */
  slackUsername?: string;
}

export interface ChannelIdentity {
  /** Friendly channel name (e.g. "darkhunt-team") */
  name?: string;
  /** Channel ID (e.g. "C0AM98AUQUQ") */
  id?: string;
  /** Channel provider (e.g. "slack") */
  provider?: string;
}

// ── Observation types ──────────────────────────────────────────────

export type ObservationType = 'agent' | 'generation' | 'tool' | 'event';

// ── Buffered state (held between start/end events) ─────────────────

export interface BufferedAgent {
  sessionId: string;
  sessionKey: string;
  agentId: string;
  spanId: string;
  traceId: string;
  startTime: HrTime;
  traceName?: string;
  traceTags?: string[];
  channel?: string;
  accountId?: string;
  model?: string;
  /** OpenClaw native run identifier from runtime.events.onAgentEvent */
  runId?: string;
  /** Resolved user identity */
  userIdentity?: UserIdentity;
  /** Resolved channel identity */
  channelIdentity?: ChannelIdentity;
}

export interface BufferedGeneration {
  spanId: string;
  parentSpanId: string;
  traceId: string;
  model: string;
  rawModel?: string;
  provider: string;
  startTime: HrTime;
  input?: string;
  inputLength?: number;
  systemPrompt?: string;
  systemPromptLength?: number;
  historyLength?: number;
  modelParameters?: string;
  attempt?: number;
  sessionKey: string;
  sessionId: string;
  accountId?: string;
  agentId?: string;
  /** Normalized history messages for structured span input */
  historyMessages?: HistoryMessage[];
  /** Clean user message from message_received (before prompt construction) */
  cleanUserMessage?: string;
  /** Resolved user identity */
  userIdentity?: UserIdentity;
  /** Resolved channel identity */
  channelIdentity?: ChannelIdentity;
}

export interface BufferedTool {
  spanId: string;
  parentSpanId: string;
  traceId: string;
  toolName: string;
  toolCallId: string;
  startTime: HrTime;
  parameters?: string;
  attempt?: number;
  sessionKey: string;
  sessionId: string;
  accountId?: string;
  agentId?: string;
  model?: string;
  /** Human-readable tool description from runtime agent event meta */
  meta?: string;
  /** Stashed result from first tool.end event (before durationMs event arrives) */
  stashedResult?: string;
  /** Resolved user identity */
  userIdentity?: UserIdentity;
  /** Resolved channel identity */
  channelIdentity?: ChannelIdentity;
}

// ── Event data from OpenClaw hooks ─────────────────────────────────

export interface MessageInData {
  sessionId: string;
  sessionKey: string;
  channel: string;
  from: string;
  accountId?: string;
  contentLength: number;
  ts: number; // epoch ms
  /** Resolved user identity */
  userIdentity?: UserIdentity;
  /** Resolved channel identity */
  channelIdentity?: ChannelIdentity;
  /** Thread correlation key (channelId:threadId) for deferred emission when sessionKey is missing */
  threadKey?: string;
}

export interface AgentStartData {
  sessionId: string;
  sessionKey: string;
  agentId: string;
  traceName?: string;
  traceTags?: string[];
  channel?: string;
  accountId?: string;
  ts: number;
}

export interface AgentEndData {
  sessionKey: string;
  agentId: string;
  success: boolean;
  durationMs: number;
  error?: string;
  ts: number;
}

export interface LlmInputData {
  sessionId: string;
  sessionKey: string;
  agentId: string;
  model: string;
  rawModel?: string;
  provider: string;
  runId: string;
  input?: string;
  inputLength?: number;
  systemPrompt?: string;
  systemPromptLength?: number;
  historyLength?: number;
  /** Normalized structured messages from evt.historyMessages */
  historyMessages?: HistoryMessage[];
  modelParameters?: string;
  attempt?: number;
  ts: number;
}

export interface LlmOutputData {
  sessionKey: string;
  runId: string;
  model: string;
  rawModel?: string;
  provider: string;
  output?: string;
  outputLength?: number;
  stopReason?: string;
  inputTokens?: number;
  outputTokens?: number;
  cacheReadInputTokens?: number;
  cacheCreationInputTokens?: number;
  costTotal?: number;
  costDetails?: string;
  completionStartTime?: string;
  error?: string;
  ts: number;
}

export interface ToolStartData {
  sessionKey: string;
  agentId: string;
  toolName: string;
  toolCallId: string;
  parameters?: string;
  attempt?: number;
  ts: number;
}

export interface ToolEndData {
  sessionKey: string;
  toolName: string;
  toolCallId: string;
  success: boolean;
  durationMs?: number;
  result?: string;
  error?: string;
  ts: number;
}

export interface LlmUsageData {
  sessionKey: string;
  model: string;
  provider: string;
  inputTokens: number;
  outputTokens: number;
  cacheTokens?: number;
  durationMs: number;
}

// ── Instrumentation library constant ───────────────────────────────

export const INSTRUMENTATION_LIBRARY = {
  name: 'tracehub-telemetry',
  version: '0.3.7',
} as const;
