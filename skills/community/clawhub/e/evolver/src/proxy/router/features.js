'use strict';

// Stateless feature extraction for the Anthropic /v1/messages request body.
// Mirrors the field shapes consumed by model_router.js so pickForTurn can
// classify without per-session state. Phase C's "empty history" mode means
// last_assistant_output_tokens / last_assistant_stop_reason are always 0 /
// null; the JS classifier never reads stop_reason anyway (verified in the
// fixture round-trip; documented in model_router.js).

const PLAN_RE = /\b(plan|design|architect|brainstorm|outline|think through|let'?s think)\b/i;
const SIMPLE_LOOKUP_MAX_CHARS = 80;

function lastMessageOfRole(messages, role) {
  if (!Array.isArray(messages)) return null;
  for (let i = messages.length - 1; i >= 0; i--) {
    const m = messages[i];
    if (m && m.role === role) return m;
  }
  return null;
}

function blocksOf(msg) {
  if (!msg) return [];
  const c = msg.content;
  if (typeof c === 'string') return [{ type: 'text', text: c }];
  return Array.isArray(c) ? c : [];
}

function tailUserText(messages) {
  if (!Array.isArray(messages) || messages.length === 0) return '';
  const tail = messages[messages.length - 1];
  if (!tail || tail.role !== 'user') return '';
  return blocksOf(tail)
    .filter((b) => b && b.type === 'text' && typeof b.text === 'string')
    .map((b) => b.text)
    .join('\n');
}

function extractFeatures(body) {
  const messages = Array.isArray(body && body.messages) ? body.messages : [];

  const lastAssistant = lastMessageOfRole(messages, 'assistant');
  const lastAssistantBlocks = blocksOf(lastAssistant);
  const toolCallCount = lastAssistantBlocks.filter((b) => b && b.type === 'tool_use').length;

  const tail = messages[messages.length - 1];
  const tailIsUser = !!(tail && tail.role === 'user');
  const tailBlocks = blocksOf(tail);
  const lastUserIsToolResultOnly = tailIsUser
    && tailBlocks.length > 0
    && tailBlocks.every((b) => b && b.type === 'tool_result');

  const userText = tailUserText(messages);
  const userRequestedPlanning = userText.length > 0 && PLAN_RE.test(userText);
  const userSimpleLookup = userText.length > 0
    && !lastUserIsToolResultOnly
    && !userRequestedPlanning
    && userText.trim().length <= SIMPLE_LOOKUP_MAX_CHARS;

  // last_assistant_stop_reason is gated by the classifier's
  // post_tool_result_synthesis branch (model_router.js parity invariant).
  // We don't have the real Anthropic response on the request side, but the
  // shape of the last assistant message lets us reconstruct it deterministically:
  // an assistant message with any tool_use block must have ended with
  // stop_reason: 'tool_use' (otherwise the API would not have returned that
  // block); a text-only assistant message ended with 'end_turn' ('Stop' in the
  // Rust enum). Only 'ToolUse' is read by the classifier.
  let stopReason = null;
  if (lastAssistant) {
    stopReason = toolCallCount > 0 ? 'ToolUse' : 'Stop';
  }

  return {
    last_assistant_tool_call_count: toolCallCount,
    last_assistant_had_tool_call: toolCallCount > 0,
    last_user_is_tool_result_only: lastUserIsToolResultOnly,
    user_requested_planning: userRequestedPlanning,
    user_simple_lookup: userSimpleLookup,
    last_assistant_output_tokens: 0,
    last_assistant_stop_reason: stopReason,
  };
}

module.exports = { extractFeatures, PLAN_RE, SIMPLE_LOOKUP_MAX_CHARS };
