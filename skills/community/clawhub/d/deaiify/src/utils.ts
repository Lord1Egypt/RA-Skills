import { DASH_PATTERN } from "./constants.js";

/**
 * Remove fenced code blocks and inline code from text before dash detection.
 * This prevents false positives on code samples that happen to contain dashes.
 */
export function stripCodeBlocks(text: string): string {
  // Remove fenced code blocks: ```...``` (including language specifier)
  let result = text.replace(/```[\s\S]*?```/g, "");
  // Remove inline code: `...` (single line only)
  result = result.replace(/`[^`\n]+`/g, "");
  return result;
}

/**
 * Returns true if the text (outside of code blocks) contains any banned dash character.
 */
export function containsDashes(text: string): boolean {
  if (!text) return false;
  return DASH_PATTERN.test(stripCodeBlocks(text));
}

/**
 * Count whitespace-separated words in a string.
 */
export function countWords(text: string): number {
  return text.trim().split(/\s+/).filter((w) => w.length > 0).length;
}

/**
 * Verify the LLM rewrite is acceptable.
 * Rejects if:
 *   - word count drifts more than 10% from original
 *   - total length expands more than 50% over original
 *
 * Returns true if the rewrite passes, false if it should be rejected.
 */
export function verifyRewrite(original: string, rewritten: string): boolean {
  if (!rewritten || !rewritten.trim()) return false;

  const origWords = countWords(original);
  const newWords = countWords(rewritten);

  if (origWords > 0) {
    const drift = Math.abs(newWords - origWords) / origWords;
    if (drift > 0.1) return false;
  }

  if (original.length > 0) {
    const expansion = (rewritten.length - original.length) / original.length;
    if (expansion > 0.5) return false;
  }

  return true;
}
