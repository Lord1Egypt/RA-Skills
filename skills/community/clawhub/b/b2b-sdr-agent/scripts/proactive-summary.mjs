#!/usr/bin/env node
/**
 * proactive-summary — L2 Proactive Compaction Trigger
 *
 * Dual-threshold token monitoring with background save + forced compression.
 * Uses a small/fast model (haiku-class) for compression to minimize cost.
 * Compressed summaries are stored in ChromaDB for long-term retrieval.
 *
 * Thresholds:
 *   - 50% (BACKGROUND_THRESHOLD): Non-blocking — extract key facts to ChromaDB without compressing
 *   - 65% (COMPRESS_THRESHOLD): Blocking — full L2 compression (compress + store + trim)
 *
 * Integration:
 *   - Called by OpenClaw's compaction.memoryFlush hook (softThresholdTokens: 10000)
 *   - Can also run standalone: node proactive-summary.mjs --context <file> --output <file>
 *
 * Architecture:
 *   1. Read current conversation context
 *   2. Estimate token usage → tri-state: OK / BACKGROUND_SAVE / COMPRESS
 *   3. BACKGROUND_SAVE: Extract key facts to ChromaDB (no compression, no blocking)
 *   4. COMPRESS: Full compression via haiku-class model (fast, cheap)
 *   5. Store compressed summary in ChromaDB
 *   6. Return compressed messages (summary + last 3 raw turns)
 */

const COMPRESSION_PROMPT = `You are a conversation compressor for a B2B sales agent.
Compress the conversation history into a structured summary with ZERO information loss on critical data.

## MUST preserve verbatim:
- All numbers (prices, quantities, dates, percentages)
- Customer BANT data (Budget, Authority, Need, Timeline)
- Quotes sent and their terms
- Commitments from both sides (agent and customer)
- Customer objections and responses given
- Decision signals ("need to check with boss", "send sample")

## CAN compress:
- Small talk → "[rapport established]"
- Repeated product intros → "[introduced product X, key specs: Y, Z]"
- Multi-round confirmations → "[confirmed after discussion: X]"

## NEVER discard:
- Any specific numbers
- Incomplete action items
- Customer emotional signals

## Output format:
=== Compressed Summary (${new Date().toISOString()}) ===
[Turns] Original N → Compressed
[Stage] current_stage
[Key Facts]
1. fact
2. fact
[Preserved Verbatim]
- "exact quote or number"
[Compressed Segments]
- [topic summary]
=== End ===`;

const COMPRESS_THRESHOLD = parseFloat(process.env.COMPRESS_THRESHOLD || '0.65');
const BACKGROUND_THRESHOLD = parseFloat(process.env.BACKGROUND_THRESHOLD || '0.50');
// Backward compat: old env var still works
const TOKEN_THRESHOLD = COMPRESS_THRESHOLD;

const MODEL_CONTEXT_WINDOWS = {
  'claude-haiku-4-5': 200000,
  'claude-sonnet-4-5': 200000,
  'claude-opus-4-6': 200000,
  'gpt-4o': 128000,
  'gpt-4o-mini': 128000,
  'kimi-2.5': 128000,
  'deepseek-v3': 128000,
  'gemini-2.5-flash': 1048576,
};

function estimateTokens(text) {
  // Approximate: 1 token ≈ 4 chars for English, 2 chars for CJK
  const cjkChars = (text.match(/[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff]/g) || []).length;
  const otherChars = text.length - cjkChars;
  return Math.ceil(otherChars / 4 + cjkChars / 2);
}

const BACKGROUND_SAVE_PROMPT = `Extract key facts from this conversation for background storage. Do NOT compress — just list the important data points.

## Extract:
- Customer BANT data (Budget, Authority, Need, Timeline)
- All numbers (prices, quantities, dates, percentages)
- Commitments from both sides
- Decision signals and objections
- Stage progression

## Output format:
=== Key Facts Snapshot (${new Date().toISOString()}) ===
[Facts]
1. fact
2. fact
[Numbers]
- exact figure or quote
[Open Items]
- pending action or decision
=== End ===`;

function shouldTrigger(contextText, model) {
  const tokens = estimateTokens(contextText);
  const maxTokens = MODEL_CONTEXT_WINDOWS[model] || 128000;
  const usage = tokens / maxTokens;
  let action = 'OK';
  if (usage >= COMPRESS_THRESHOLD) action = 'COMPRESS';
  else if (usage >= BACKGROUND_THRESHOLD) action = 'BACKGROUND_SAVE';
  return { trigger: action !== 'OK', action, usage, tokens, maxTokens };
}

// Export for use as a module
export {
  COMPRESSION_PROMPT, BACKGROUND_SAVE_PROMPT,
  TOKEN_THRESHOLD, COMPRESS_THRESHOLD, BACKGROUND_THRESHOLD,
  estimateTokens, shouldTrigger,
};

// ─── CLI ────────────────────────────────────────────────────
if (process.argv[1]?.endsWith('proactive-summary.mjs')) {
  const args = process.argv.slice(2);
  const model = args.find((_, i) => args[i - 1] === '--model') || 'gpt-4o';
  const contextFile = args.find((_, i) => args[i - 1] === '--context');

  if (args.includes('--help') || !contextFile) {
    console.log(`proactive-summary — Dual-Threshold Compaction

Usage:
  node proactive-summary.mjs --context <file> [--model <model>]

Options:
  --context   Path to conversation context file (JSON array of messages)
  --model     AI model name for threshold calculation (default: gpt-4o)

Environment:
  BACKGROUND_THRESHOLD  Background save threshold (default: 0.50)
  COMPRESS_THRESHOLD    Compression threshold (default: 0.65)

Actions:
  OK              — Below 50%, no action needed
  BACKGROUND_SAVE — 50-65%, extract key facts to ChromaDB (non-blocking)
  COMPRESS        — Above 65%, full L2 compression (blocking)`);
    process.exit(0);
  }

  try {
    const { readFileSync } = await import('fs');
    const context = readFileSync(contextFile, 'utf-8');
    const result = shouldTrigger(context, model);

    const prompt = result.action === 'COMPRESS' ? COMPRESSION_PROMPT
      : result.action === 'BACKGROUND_SAVE' ? BACKGROUND_SAVE_PROMPT
      : null;

    console.log(JSON.stringify({
      ...result,
      model,
      backgroundThreshold: BACKGROUND_THRESHOLD,
      compressThreshold: COMPRESS_THRESHOLD,
      prompt,
    }, null, 2));
  } catch (e) {
    console.error(`Error: ${e.message}`);
    process.exit(1);
  }
}
