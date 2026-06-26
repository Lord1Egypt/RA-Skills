---
name: token-optimizer
description: Reduce LLM API token consumption by 20-35% through pre-send estimation, memory extraction, and context compression.
version: 1.0.0
author: OpenClaw Community
tags: [optimization, tokens, cost-reduction, context-management, memory]
model: any
---

# Token Optimizer

Reduce your LLM API costs by 20-35% with three proven mechanisms: **pre-send token estimation**, **structured memory extraction**, and **context compression**. Model-agnostic, zero dependencies.

---

## Mechanism 1 — Pre-Send Token Estimation

Estimate token count *before* sending a request. If the payload exceeds a threshold, compress or truncate it. Never pay for tokens you could have avoided.

### Rules

1. **Estimate before every API call.** Use these formulas:
   - Plain text: `tokens ≈ character_count / 4`
   - JSON / structured data: `tokens ≈ character_count / 2`
   - Code (mixed): `tokens ≈ character_count / 3.5`
   - Images / PDFs: `tokens ≈ 2000` (flat per asset, regardless of size)

2. **Set a token budget per request.** Default threshold: **8 000 tokens**. Adjust per use case.

3. **If estimated tokens exceed the budget:**
   - Summarize or truncate the longest sections first.
   - Strip intermediate reasoning, keep conclusions only.
   - For JSON: remove null/empty fields, shorten keys if feeding to a model that doesn't need human-readable keys.
   - For code: send only the relevant function/class, not the full file.

4. **Log the estimate vs. actual usage** (from the API response) to calibrate over time.

### Example

```
Input: 24,000 characters of plain text
Estimated tokens: 24000 / 4 = 6,000 → under budget, send as-is.

Input: 40,000 characters of JSON
Estimated tokens: 40000 / 2 = 20,000 → over budget.
Action: strip null fields, remove redundant nested objects → 14,000 chars → 7,000 tokens → send.
```

### Reference

See [references/token-formula.md](references/token-formula.md) for the full formula breakdown with worked examples.

---

## Mechanism 2 — Memory Extraction

Instead of re-reading the entire conversation history every turn, extract and persist key information into structured memory files. On subsequent turns, load only the memory index — not the raw history.

### Rules

1. **Use a lightweight secondary model** (Haiku, GPT-4o-mini, Gemini Flash) as the memory extraction agent. Never burn expensive model tokens on bookkeeping.

2. **Maintain a session cursor.** Track which messages have already been processed. On each extraction pass, only read *new* messages since the last cursor position.

3. **Limit extraction to 5 rounds max per session.** Each round processes a batch of new messages. Stop early if no new information is found.

4. **Parallelize I/O within rounds:**
   - Round 1: all reads in parallel (gather raw content).
   - Round 2: all writes in parallel (persist extracted memories).

5. **Structure memory as index + detail files:**
   - `MEMORY.md` — index file, max 200 lines. Contains only pointers: `- [topic-name](memory/topic-name.md) — one-line description`.
   - `memory/topic-name.md` — full content for each topic with frontmatter (name, description, type).

6. **Memory types** (categorize each entry):
   - `user` — who the user is, their preferences, expertise level.
   - `feedback` — corrections and confirmed approaches (what to do / not do).
   - `project` — current goals, deadlines, decisions, constraints.
   - `reference` — pointers to external resources (URLs, dashboards, issue trackers).

7. **Do not store what can be derived.** No code snippets, no git history, no file paths — these are always available from the source. Store only non-obvious context.

### Example — Extraction Prompt

```
You are a memory extraction agent. Read the following new messages (since cursor position {cursor}).

For each piece of non-obvious information, output a JSON object:
{
  "topic": "short-kebab-case-name",
  "type": "user | feedback | project | reference",
  "description": "one-line summary for the index",
  "content": "full memory content, structured with Why and How-to-apply"
}

Rules:
- Max 5 memories per pass.
- Skip anything derivable from code, git, or existing memory.
- Convert relative dates to absolute (today is {date}).
- If a memory already exists for this topic, output an update, not a duplicate.
```

### Reference

See [references/memory-extraction-pattern.md](references/memory-extraction-pattern.md) for the full pattern with prompt templates.

---

## Mechanism 3 — Context Compression

As conversations grow, compress older exchanges into dense summaries. Keep only the last N messages in full fidelity. This prevents context windows from filling with stale reasoning.

### Rules

1. **Keep the last 6 messages uncompressed** (3 user + 3 assistant). These are "fresh" — they contain active context.

2. **Summarize everything older** into a single `<compressed-context>` block at the top of the conversation. Format:

   ```
   <compressed-context>
   ## Decisions Made
   - Chose PostgreSQL over MongoDB for the user table (reason: relational queries).
   - API rate limit set to 100 req/min per user.

   ## Current State
   - Auth module: complete, merged to main.
   - Payment integration: in progress, blocked on Stripe webhook config.

   ## Key Constraints
   - Must ship by 2026-04-15.
   - No breaking changes to public API v2.
   </compressed-context>
   ```

3. **What to keep in summaries:**
   - Decisions and their rationale.
   - Current state of work (done / in-progress / blocked).
   - Constraints and deadlines.
   - User preferences and corrections.

4. **What to discard:**
   - Intermediate reasoning ("I considered X but...").
   - Exploratory questions that were already answered.
   - Tool call details (file reads, grep results, build output).
   - Repeated or superseded information.

5. **Trigger compression when the conversation exceeds 60% of the model's context window.** Use Mechanism 1's estimation formula to check.

6. **Never compress system prompts or skill instructions.** These must remain intact.

### Example — Savings Calculation

```
Before compression:
  42 messages, ~32,000 tokens total.

After compression:
  Compressed block: ~2,000 tokens.
  Last 6 messages: ~4,500 tokens.
  Total: ~6,500 tokens.

  Savings: 32,000 - 6,500 = 25,500 tokens (80% reduction on history).
  Per-request savings (ongoing): ~25,500 tokens × $0.003/1K = $0.077 per request.
```

---

## Combined Savings Estimate

| Mechanism | Typical Savings | When It Hits |
|---|---|---|
| Pre-send estimation | 10-15% | Every request with large payloads |
| Memory extraction | 5-10% | Multi-session workflows |
| Context compression | 15-25% | Long conversations (>20 messages) |
| **Combined** | **20-35%** | **Sustained usage over a session** |

These are conservative estimates based on real-world agent workflows. Actual savings depend on conversation length, payload sizes, and how aggressively you compress.

---

## Quick Start

1. **Copy this skill** into your agent's skill directory (or paste `SKILL.md` into your system prompt).
2. **Apply Mechanism 1** immediately — add token estimation before your API calls.
3. **Set up Mechanism 2** if you run multi-turn or multi-session workflows.
4. **Enable Mechanism 3** for any conversation that runs beyond 15-20 messages.

No code to install. No dependencies. Just rules your agent follows.
