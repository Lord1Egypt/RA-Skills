import type { PayloadMode, UserIdentity, ChannelIdentity } from './types.js';

// ── Size limits (bytes) ────────────────────────────────────────────

export const LIMIT_INPUT = 4 * 1024;
export const LIMIT_OUTPUT = 4 * 1024;
export const LIMIT_TOOL_PARAMS = 2 * 1024;
export const LIMIT_COST_DETAILS = 512;
export const LIMIT_MODEL_PARAMS = 512;
export const LIMIT_SINGLE_ATTR = 8 * 1024;
export const LIMIT_TOTAL_SPAN = 64 * 1024;

// Debug mode truncation limits (characters)
export const DEBUG_INPUT_CHARS = 500;
export const DEBUG_OUTPUT_CHARS = 500;
export const DEBUG_TOOL_PARAMS_CHARS = 1000;
export const DEBUG_SYSTEM_PROMPT_CHARS = 200;

// ── Safe-tool allowlist ────────────────────────────────────────────

const SAFE_TOOLS = new Set([
  // OpenClaw built-in tools
  'exec', 'read', 'write', 'edit',
  'web_search', 'web_fetch', 'message', 'process',
  'sessions_spawn', 'session_status', 'subagents', 'agents_list',
  'browser', 'cron', 'memory_search', 'nodes',
  'sessions_list', 'session_destroy',
  'devices_list', 'devices_approve',
  'config_get', 'config_set',
  'cron_list', 'cron_add', 'cron_remove',
  'logs', 'health',
  // Claude-style aliases
  'Read', 'Write', 'Edit', 'Grep', 'Glob', 'Bash', 'Agent',
]);

// ── Core functions ─────────────────────────────────────────────────

export function truncate(value: string, maxBytes: number): string {
  const encoded = Buffer.from(value, 'utf-8');
  if (encoded.length <= maxBytes) return value;

  const suffix = `... [truncated, ${value.length} chars total]`;
  const suffixBytes = Buffer.byteLength(suffix, 'utf-8');
  const available = maxBytes - suffixBytes;
  if (available <= 0) return suffix;

  // Truncate at byte level then decode safely
  let truncated = encoded.subarray(0, available).toString('utf-8');
  // Remove potential partial multi-byte character at the end
  if (truncated.endsWith('\uFFFD')) {
    truncated = truncated.slice(0, -1);
  }
  return truncated + suffix;
}

export function truncateChars(value: string, maxChars: number): string {
  if (value.length <= maxChars) return value;
  const suffix = `... [truncated, ${value.length} chars total]`;
  return value.slice(0, maxChars) + suffix;
}

export function shouldIncludeContent(mode: PayloadMode): boolean {
  return mode !== 'metadata';
}

export function sanitizeToolParams(
  toolName: string,
  params: string | undefined,
  mode: PayloadMode,
): string | undefined {
  if (!params) return undefined;

  // Unknown/third-party tools: redact in all modes (could contain secrets)
  if (!SAFE_TOOLS.has(toolName)) {
    // In metadata mode, skip entirely; in debug/full, show redaction marker
    if (mode === 'metadata') return undefined;
    return JSON.stringify({ redacted: true });
  }

  // Safe tools: always include params (they're operational metadata, not private content).
  // These show what happened — file paths, commands, search queries.
  if (mode === 'metadata') {
    return truncateChars(params, DEBUG_TOOL_PARAMS_CHARS);
  }

  if (mode === 'debug') {
    return truncateChars(params, DEBUG_TOOL_PARAMS_CHARS);
  }

  return truncate(params, LIMIT_TOOL_PARAMS);
}

/**
 * Extract the primary argument from tool parameters for the REQUEST section.
 * Returns the most meaningful value (command, path, query, url) for known tools.
 */
export function formatToolInput(toolName: string, parametersJson: string | undefined): string | undefined {
  if (!parametersJson) return undefined;
  try {
    const params = JSON.parse(parametersJson);
    if (typeof params === 'object' && params !== null) {
      const primary = params.command ?? params.path ?? params.file
        ?? params.query ?? params.url ?? params.pattern;
      if (primary) return String(primary);
    }
  } catch { /* not JSON */ }
  return parametersJson;
}

/**
 * Extract clean text from tool result JSON, stripping OpenClaw content wrappers.
 * Parses JSON tool results and extracts meaningful content:
 * - web_fetch: extracts text, strips SECURITY NOTICE, returns with url/status metadata
 * - memory_search: extracts result snippets
 * - Generic: extracts .text, .content[].text, or .aggregated
 */
export function cleanToolResult(result: string | undefined): string | undefined {
  if (!result) return undefined;
  try {
    const parsed = JSON.parse(result);
    if (typeof parsed !== 'object' || parsed === null) return result;

    // web_fetch result: extract the actual page text + metadata summary
    if (parsed.url && parsed.text) {
      const text = stripExternalContentWrapper(parsed.text);
      const meta = [
        `url: ${parsed.finalUrl || parsed.url}`,
        parsed.status ? `status: ${parsed.status}` : null,
        parsed.title ? `title: ${stripExternalContentWrapper(parsed.title)}` : null,
      ].filter(Boolean).join(' | ');
      return `[${meta}]\n${text}`;
    }

    // memory_search result: extract snippets
    if (Array.isArray(parsed.results)) {
      if (parsed.results.length === 0) return 'No results found.';
      const snippets = parsed.results
        .filter((r: any) => r?.snippet || r?.text)
        .map((r: any) => {
          const path = r.path ? `[${r.path}]` : '';
          const text = r.snippet || r.text;
          return `${path} ${text}`.trim();
        });
      return snippets.length > 0 ? snippets.join('\n---\n') : JSON.stringify(parsed.results);
    }

    // Error result
    if (parsed.error) {
      return `Error: ${parsed.error}${parsed.message ? ` — ${parsed.message}` : ''}`;
    }

    // Generic: content blocks
    if (Array.isArray(parsed.content)) {
      const texts = parsed.content
        .filter((b: any) => b?.type === 'text' && b?.text)
        .map((b: any) => b.text);
      if (texts.length > 0) return texts.join('\n');
    }

    if (parsed.aggregated != null) return String(parsed.aggregated);
    if (parsed.text != null) return String(parsed.text);
  } catch { /* not JSON — return as-is */ }
  return result;
}

/** Strip OpenClaw EXTERNAL_UNTRUSTED_CONTENT security wrappers from fetched content */
function stripExternalContentWrapper(text: string): string {
  if (!text) return text;
  // Remove SECURITY NOTICE block
  let cleaned = text.replace(
    /SECURITY NOTICE:.*?(?=<<<EXTERNAL_UNTRUSTED_CONTENT|$)/s,
    '',
  );
  // Remove <<<EXTERNAL_UNTRUSTED_CONTENT id="...">>\nSource: ...\n---\n
  cleaned = cleaned.replace(/<<<EXTERNAL_UNTRUSTED_CONTENT[^>]*>>>\s*\nSource:[^\n]*\n---\n?/g, '');
  // Remove <<<END_EXTERNAL_UNTRUSTED_CONTENT id="...">>>
  cleaned = cleaned.replace(/<<<END_EXTERNAL_UNTRUSTED_CONTENT[^>]*>>>/g, '');
  return cleaned.trim();
}

/**
 * @deprecated Use clean data sources instead of regex cleaning:
 *   1. message_received evt.content (pre-prompt, no wrapper)
 *   2. historyMessages[].content (structured, no wrapper)
 *   3. Raw evt.prompt shipped as-is
 *
 * This function remains for backward compatibility but should not be used
 * for generation span input. OpenClaw's prompt format is their internal
 * implementation detail — every regex here breaks when they change it.
 */
export function cleanGenerationInput(input: string | undefined): string | undefined {
  if (!input) return undefined;

  let cleaned = input;

  // [media attached: /path/to/file.ext (mime/type) | /path] → [image: file.ext]
  cleaned = cleaned.replace(
    /\[media attached:\s*[^\]]*\/([^\s|)\]]+)\s*\([^)]*\)[^\]]*\]/g,
    (_, filename) => `[image: ${filename}]`,
  );

  // Strip image instruction block
  cleaned = cleaned.replace(
    /To send an image back.*?Keep caption in the text body\.\n?/gs,
    '',
  );

  // Strip "Conversation info (untrusted metadata):" + fenced JSON
  cleaned = cleaned.replace(
    /Conversation info \(untrusted metadata\):\s*\n```json?\n[\s\S]*?```\s*\n*/g,
    '',
  );

  // Strip "Sender (untrusted metadata):" + fenced JSON
  cleaned = cleaned.replace(
    /Sender \(untrusted metadata\):\s*\n```json?\n[\s\S]*?```\s*\n*/g,
    '',
  );

  // Strip <media:image> / <media:video> etc. tags
  cleaned = cleaned.replace(/<media:\w+>\s*/g, '');

  // Strip OpenClaw system message prefix variants:
  // "System: [timestamp] Slack message in #channel from user: ..."
  // "System: [timestamp] Slack message edited in #channel."
  // "System: [timestamp] Slack message in #channel from user: <@mention> text"
  cleaned = cleaned.replace(
    /^System:\s*\[\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}[^\]]*\]\s*Slack message(?:\s+edited)? in #\S+(?:\s+from \S+)?[.:]\s*/gm,
    '',
  );

  // Strip thread history block header
  cleaned = cleaned.replace(/^\[Thread history - for context\]\s*\n?/gm, '');

  // Strip Slack thread message lines: [Slack user (role) timestamp UTC] ...
  cleaned = cleaned.replace(/^\[Slack \S+ \(\w+\) [^\]]+\].*\n?/gm, '');

  // Strip slack message id metadata lines: [slack message id: ... channel: ...]
  cleaned = cleaned.replace(/^\[slack message id:\s*[^\]]+\]\s*\n?/gm, '');

  // Strip "Chat history since last reply (untrusted, for context):" + fenced JSON block
  cleaned = cleaned.replace(
    /Chat history since last reply \(untrusted,? for context\):\s*\n```json?\n[\s\S]*?```\s*\n*/g,
    '',
  );

  // Strip Slack user mentions: <@U098VT61MQ9>
  cleaned = cleaned.replace(/<@[A-Z0-9]+>/g, '').trim();

  // Strip "Reply instructions:" or "[reply_to_current]" routing directives
  cleaned = cleaned.replace(/^\s*Reply instructions:.*\n?/gm, '');
  cleaned = cleaned.replace(/^\s*\[reply_to_\w+\]\s*/gm, '');

  // Collapse multiple blank lines
  cleaned = cleaned.replace(/\n{3,}/g, '\n\n').trim();

  return cleaned || undefined;
}

/**
 * Clean up OpenClaw generation output by stripping internal routing tags.
 * - [[reply_to_current]], [[reply_in_thread]], [[no_reply]] etc.
 * - [reply_to_current] (bracket variant)
 */
export function cleanGenerationOutput(output: string | undefined): string | undefined {
  if (!output) return undefined;

  let cleaned = output;

  // Strip [[reply_to_current]], [[reply_in_thread]], [[no_reply]], etc.
  cleaned = cleaned.replace(/\[\[reply_to_\w+\]\]\s*/g, '');
  cleaned = cleaned.replace(/\[\[no_reply\]\]\s*/g, '');
  cleaned = cleaned.replace(/\[\[reply_\w+\]\]\s*/g, '');

  // Strip [reply_to_current] bracket variant
  cleaned = cleaned.replace(/\[reply_to_\w+\]\s*/g, '');

  return cleaned.trim() || undefined;
}

/**
 * Truncate a structured message array to fit within a byte budget.
 * Strategy: keep system prompt (first) + last N messages (recent context),
 * drop middle messages with a placeholder.
 */
export function truncateMessageArray(
  messages: Array<{ role: string; content: string }>,
  maxBytes: number,
): Array<{ role: string; content: string }> {
  if (messages.length === 0) return messages;

  const serialized = JSON.stringify(messages);
  if (Buffer.byteLength(serialized, 'utf-8') <= maxBytes) return messages;

  // Separate system message (if first) from conversation messages
  let system: { role: string; content: string } | undefined;
  let conversation: Array<{ role: string; content: string }>;

  if (messages[0].role === 'system') {
    system = messages[0];
    conversation = messages.slice(1);
  } else {
    conversation = [...messages];
  }

  // Keep last 3 conversation messages (the most recent context)
  const tailCount = Math.min(3, conversation.length);
  const tail = conversation.slice(-tailCount);
  const droppedCount = conversation.length - tailCount;

  const result: Array<{ role: string; content: string }> = [];
  if (system) result.push(system);
  if (droppedCount > 0) {
    result.push({ role: 'system', content: `[${droppedCount} earlier message(s) omitted]` });
  }
  result.push(...tail);

  // Check if it fits now
  if (Buffer.byteLength(JSON.stringify(result), 'utf-8') <= maxBytes) return result;

  // Still too large — truncate individual message content
  for (const msg of result) {
    if (msg.content.length > 200) {
      msg.content = truncateChars(msg.content, 200);
    }
  }

  // Final safety: if still too large, keep only the last user message
  if (Buffer.byteLength(JSON.stringify(result), 'utf-8') > maxBytes) {
    const lastUser = result.filter(m => m.role === 'user').pop();
    if (lastUser) return [lastUser];
    return [result[result.length - 1]];
  }

  return result;
}

export function sanitizeToolResult(
  toolName: string,
  result: string | undefined,
  mode: PayloadMode,
): string | undefined {
  if (!result) return undefined;

  // Unknown/third-party tools: never include results
  if (!SAFE_TOOLS.has(toolName)) return undefined;

  // Safe tools: include result in all modes (it shows what happened)
  if (mode === 'metadata' || mode === 'debug') {
    return truncateChars(result, DEBUG_OUTPUT_CHARS);
  }

  return truncate(result, LIMIT_OUTPUT);
}

/**
 * Apply payload mode to content attributes.
 * Returns a new map with content attributes stripped/truncated per mode.
 */
export function applyPayloadMode(
  attrs: Record<string, string | number | boolean | string[]>,
  mode: PayloadMode,
): Record<string, string | number | boolean | string[]> {
  const result = { ...attrs };

  if (mode === 'metadata') {
    delete result['openclaw.observation.input'];
    delete result['openclaw.observation.output'];
    delete result['openclaw.observation.system_prompt'];
    delete result['openclaw.observation.model.parameters'];
    // Note: openclaw.tool.parameters is NOT deleted here — safe tool params
    // are included even in metadata mode (handled by sanitizeToolParams)
    return result;
  }

  if (mode === 'debug') {
    if (typeof result['openclaw.observation.input'] === 'string') {
      result['openclaw.observation.input'] = truncateChars(
        result['openclaw.observation.input'] as string,
        DEBUG_INPUT_CHARS,
      );
    }
    if (typeof result['openclaw.observation.output'] === 'string') {
      result['openclaw.observation.output'] = truncateChars(
        result['openclaw.observation.output'] as string,
        DEBUG_OUTPUT_CHARS,
      );
    }
    if (typeof result['openclaw.observation.system_prompt'] === 'string') {
      result['openclaw.observation.system_prompt'] = truncateChars(
        result['openclaw.observation.system_prompt'] as string,
        DEBUG_SYSTEM_PROMPT_CHARS,
      );
    }
    if (typeof result['openclaw.observation.model.parameters'] === 'string') {
      result['openclaw.observation.model.parameters'] = truncate(
        result['openclaw.observation.model.parameters'] as string,
        LIMIT_MODEL_PARAMS,
      );
    }
    // Tool params handled separately via sanitizeToolParams
  }

  // Full mode: enforce byte limits
  if (mode === 'full') {
    if (typeof result['openclaw.observation.input'] === 'string') {
      result['openclaw.observation.input'] = truncate(
        result['openclaw.observation.input'] as string,
        LIMIT_INPUT,
      );
    }
    if (typeof result['openclaw.observation.output'] === 'string') {
      result['openclaw.observation.output'] = truncate(
        result['openclaw.observation.output'] as string,
        LIMIT_OUTPUT,
      );
    }
    if (typeof result['openclaw.observation.system_prompt'] === 'string') {
      result['openclaw.observation.system_prompt'] = truncate(
        result['openclaw.observation.system_prompt'] as string,
        LIMIT_INPUT,
      );
    }
    if (typeof result['openclaw.observation.model.parameters'] === 'string') {
      result['openclaw.observation.model.parameters'] = truncate(
        result['openclaw.observation.model.parameters'] as string,
        LIMIT_MODEL_PARAMS,
      );
    }
  }

  return result;
}

/**
 * Enforce the total span size limit. If over 64KB, drop content attributes
 * first (input, output, tool.parameters, model.parameters), then truncate
 * remaining large attributes.
 */
export function enforceSpanSizeLimit(
  attrs: Record<string, string | number | boolean | string[]>,
  maxBytes: number = LIMIT_TOTAL_SPAN,
): Record<string, string | number | boolean | string[]> {
  const result = { ...attrs };

  // Enforce per-attribute limit
  for (const [key, val] of Object.entries(result)) {
    if (typeof val === 'string' && Buffer.byteLength(val, 'utf-8') > LIMIT_SINGLE_ATTR) {
      result[key] = truncate(val, LIMIT_SINGLE_ATTR);
    }
  }

  if (estimateSize(result) <= maxBytes) return result;

  // Drop content attributes in priority order (largest first)
  const droppable = [
    'openclaw.observation.system_prompt',
    'openclaw.observation.input',
    'openclaw.observation.output',
    'openclaw.tool.parameters',
    'openclaw.observation.model.parameters',
  ];

  for (const key of droppable) {
    delete result[key];
    if (estimateSize(result) <= maxBytes) return result;
  }

  return result;
}

// ── User & channel identity extraction ─────────────────────────────

/**
 * Extract user identity from evt.metadata (message_received) and/or evt.prompt (llm_input).
 * Sources (in priority order):
 * 1. evt.metadata — structured Slack metadata from OpenClaw
 * 2. "Sender (untrusted metadata):" JSON block in prompt
 * 3. "System: [...] Slack message in #channel from username:" line
 */
export function parseUserIdentity(metadata?: unknown, prompt?: string): UserIdentity | undefined {
  const identity: UserIdentity = {};

  // Source 1: evt.metadata from message_received
  if (metadata && typeof metadata === 'object') {
    const m = metadata as Record<string, unknown>;
    // OpenClaw Slack metadata: senderId, senderName (confirmed), plus common alternatives
    if (m.senderId) identity.slackUserId = String(m.senderId);
    if (m.userId) identity.slackUserId = identity.slackUserId || String(m.userId);
    if (m.user_id) identity.slackUserId = identity.slackUserId || String(m.user_id);
    if (m.senderName) identity.slackUsername = String(m.senderName);
    if (m.username) identity.slackUsername = identity.slackUsername || String(m.username);
    if (m.user_name) identity.slackUsername = identity.slackUsername || String(m.user_name);
    if (m.displayName) identity.displayName = String(m.displayName);
    if (m.display_name) identity.displayName = String(m.display_name);
    if (m.realName) identity.fullName = String(m.realName);
    if (m.real_name) identity.fullName = String(m.real_name);
    if (m.name) identity.fullName = identity.fullName || String(m.name);
    if (m.email) identity.email = String(m.email);
    // Nested user object
    if (m.user && typeof m.user === 'object') {
      const u = m.user as Record<string, unknown>;
      if (u.id && !identity.slackUserId) identity.slackUserId = String(u.id);
      if (u.name && !identity.slackUsername) identity.slackUsername = String(u.name);
      if (u.real_name && !identity.fullName) identity.fullName = String(u.real_name);
      if (u.email && !identity.email) identity.email = String(u.email);
      if (u.profile && typeof u.profile === 'object') {
        const p = u.profile as Record<string, unknown>;
        if (p.display_name && !identity.displayName) identity.displayName = String(p.display_name);
        if (p.real_name && !identity.fullName) identity.fullName = String(p.real_name);
        if (p.email && !identity.email) identity.email = String(p.email);
      }
    }
  }

  // Source 2: "Sender (untrusted metadata):" JSON block in prompt
  if (prompt) {
    const senderMatch = prompt.match(
      /Sender \(untrusted metadata\):\s*\n```json?\n([\s\S]*?)```/,
    );
    if (senderMatch) {
      try {
        const sender = JSON.parse(senderMatch[1]);
        if (sender.userId && !identity.slackUserId) identity.slackUserId = String(sender.userId);
        if (sender.user_id && !identity.slackUserId) identity.slackUserId = String(sender.user_id);
        if (sender.username && !identity.slackUsername) identity.slackUsername = String(sender.username);
        if (sender.name && !identity.slackUsername) identity.slackUsername = String(sender.name);
        if (sender.displayName && !identity.displayName) identity.displayName = String(sender.displayName);
        if (sender.display_name && !identity.displayName) identity.displayName = String(sender.display_name);
        if (sender.realName && !identity.fullName) identity.fullName = String(sender.realName);
        if (sender.real_name && !identity.fullName) identity.fullName = String(sender.real_name);
        if (sender.email && !identity.email) identity.email = String(sender.email);
      } catch { /* ignore parse errors */ }
    }

    // Source 3: System: line — "from username:"
    if (!identity.slackUsername) {
      const systemMatch = prompt.match(
        /^System:.*?Slack message(?:\s+edited)? in #\S+\s+from (\S+):/m,
      );
      if (systemMatch) {
        identity.slackUsername = systemMatch[1];
      }
    }
  }

  // Derive displayName if not set
  if (!identity.displayName) {
    identity.displayName = identity.slackUsername || identity.fullName;
  }

  return hasAnyField(identity) ? identity : undefined;
}

/**
 * Extract channel identity from evt.metadata, ctx, and/or prompt.
 */
export function parseChannelIdentity(
  metadata?: unknown,
  prompt?: string,
  channelId?: string,
  from?: string,
): ChannelIdentity | undefined {
  const channel: ChannelIdentity = {};

  // From ctx.channelId or evt.from
  if (channelId) channel.provider = channelId; // "slack", "telegram", etc.

  // Extract channel ID from evt.from: "slack:channel:C0AM98AUQUQ"
  if (from) {
    const channelMatch = from.match(/^(\w+):channel:([A-Z0-9]+)$/i);
    if (channelMatch) {
      if (!channel.provider) channel.provider = channelMatch[1];
      channel.id = channelMatch[2];
    }
  }

  // From metadata
  if (metadata && typeof metadata === 'object') {
    const m = metadata as Record<string, unknown>;
    if (m.channelName) channel.name = String(m.channelName);
    if (m.channel_name) channel.name = String(m.channel_name);
    if (m.channelId && !channel.id) channel.id = String(m.channelId);
    if (m.channel_id && !channel.id) channel.id = String(m.channel_id);
    // OpenClaw metadata: "to" = "channel:C0AM98AUQUQ", "provider" = "slack"
    if (m.to && typeof m.to === 'string') {
      const toMatch = (m.to as string).match(/^channel:([A-Z0-9]+)$/i);
      if (toMatch && !channel.id) channel.id = toMatch[1];
    }
    if (m.provider && !channel.provider) channel.provider = String(m.provider);
    // Nested channel object
    if (m.channel && typeof m.channel === 'object') {
      const c = m.channel as Record<string, unknown>;
      if (c.name && !channel.name) channel.name = String(c.name);
      if (c.id && !channel.id) channel.id = String(c.id);
    }
  }

  // From prompt: "Slack message in #channel-name from user:"
  if (prompt && !channel.name) {
    const nameMatch = prompt.match(
      /^System:.*?Slack message(?:\s+edited)? in #(\S+)/m,
    );
    if (nameMatch) {
      channel.name = nameMatch[1];
    }
  }

  // From "Conversation info (untrusted metadata):" JSON block
  if (prompt && !channel.name) {
    const convMatch = prompt.match(
      /Conversation info \(untrusted metadata\):\s*\n```json?\n([\s\S]*?)```/,
    );
    if (convMatch) {
      try {
        const conv = JSON.parse(convMatch[1]);
        if (conv.channelName) channel.name = String(conv.channelName);
        if (conv.channel_name) channel.name = String(conv.channel_name);
        if (conv.channel) channel.name = String(conv.channel);
      } catch { /* ignore */ }
    }
  }

  return hasAnyField(channel) ? channel : undefined;
}

/** Return the best display string for user.id attribute */
export function resolveUserDisplayId(identity?: UserIdentity): string | undefined {
  if (!identity) return undefined;
  // Priority: slackUsername > displayName > fullName > email > slackUserId
  return identity.slackUsername || identity.displayName || identity.fullName
    || identity.email || identity.slackUserId;
}

function hasAnyField(obj: object): boolean {
  return Object.values(obj).some(v => v != null && v !== '');
}

function estimateSize(attrs: Record<string, unknown>): number {
  let size = 0;
  for (const [key, val] of Object.entries(attrs)) {
    size += Buffer.byteLength(key, 'utf-8');
    if (typeof val === 'string') {
      size += Buffer.byteLength(val, 'utf-8');
    } else if (Array.isArray(val)) {
      size += Buffer.byteLength(JSON.stringify(val), 'utf-8');
    } else {
      size += 8; // numbers, booleans
    }
  }
  return size;
}
