/**
 * Remove fenced code blocks and inline code from text before dash detection.
 * This prevents false positives on code samples that happen to contain dashes.
 */
export declare function stripCodeBlocks(text: string): string;
/**
 * Returns true if the text (outside of code blocks) contains any banned dash character.
 */
export declare function containsDashes(text: string): boolean;
/**
 * Count whitespace-separated words in a string.
 */
export declare function countWords(text: string): number;
/**
 * Verify the LLM rewrite is acceptable.
 * Rejects if:
 *   - word count drifts more than 10% from original
 *   - total length expands more than 50% over original
 *
 * Returns true if the rewrite passes, false if it should be rejected.
 */
export declare function verifyRewrite(original: string, rewritten: string): boolean;
