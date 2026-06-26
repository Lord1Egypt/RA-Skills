import type { AIChatMessage } from "../types";

const MESSAGE_OVERHEAD = 4;

/**
 * Conservative token estimator tuned for mixed Chinese / English text.
 * CJK characters cost roughly 1.6 tokens each in common BPE tokenizers,
 * while latin text averages ~4 characters per token. We round up so the
 * estimate stays on the safe (slightly high) side to avoid overflowing the
 * model's context window.
 */
export function estimateTokens(text: string): number {
  let cjk = 0;
  let other = 0;
  for (const ch of text) {
    const code = ch.codePointAt(0) ?? 0;
    const isCjk =
      (code >= 0x3000 && code <= 0x9fff) ||
      (code >= 0xf900 && code <= 0xfaff) ||
      (code >= 0xff00 && code <= 0xffef) ||
      (code >= 0x20000 && code <= 0x2a6df);
    if (isCjk) cjk += 1;
    else other += 1;
  }
  return Math.ceil(cjk * 1.6 + other / 4) + MESSAGE_OVERHEAD;
}

/**
 * Keep the most recent messages whose cumulative estimated token count stays
 * within `maxTokens`. The newest messages are always preserved; the last user
 * message is never dropped even if it alone exceeds the budget.
 */
export function truncateHistory(
  messages: AIChatMessage[],
  maxTokens = 32000
): AIChatMessage[] {
  const kept: AIChatMessage[] = [];
  let total = 0;
  for (let i = messages.length - 1; i >= 0; i -= 1) {
    const cost = estimateTokens(messages[i].content);
    if (total + cost > maxTokens && kept.length > 0) break;
    kept.unshift(messages[i]);
    total += cost;
  }
  return kept;
}
