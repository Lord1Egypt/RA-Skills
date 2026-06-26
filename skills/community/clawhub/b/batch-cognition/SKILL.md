---
name: batch-cognition
version: 1.0.0
description: Process bulk prompt batches with alternating play/think cognitive loops. Use when user says "batch incoming", "multiple prompts incoming", "corpus incoming", or dumps multiple prompts separated by blank lines. Also use for Google Drive dumps, file-based prompt lists, or any bulk input requiring item-by-item execution with inference. Handles save-first (never lose input), stop-start cognition (PLAY execute then THINK infer), checkpointing, value discovery, and self-improving batch docs.
---

# Batch Cognition

Process bulk prompts with stop-start play/think cycles. Save first, lose nothing, discover value.

## Activation

User signals: "batch incoming" / "multiple prompts incoming" / "corpus incoming"

Respond: `🔁 BATCH MODE — send them. I'll save everything first, then process one-by-one.`

## Step 1: SAVE (mandatory, before any processing)

Parse input into individual prompts (split on blank lines or `---`).
Write entire batch to `workspace/systems/batch-cognition/batches/YYYY-MM-DD-HHMMSS.md`.
Read prior `value-stack.md` and last batch's meta-think for cross-batch context.
Format:

```markdown
# Batch: [timestamp]
# Source: [telegram|file|drive|paste]
# Total: [N]
# Status: SAVED

## 1. [first 60 chars of prompt]
- [ ] PENDING
> [full prompt text]

## 2. [next prompt]
- [ ] PENDING
> [full prompt text]
```

Confirm to user: "✅ Saved [N] prompts to batch doc. Starting processing."

## Step 1.5: PRE-SCAN & CLASSIFY (per item, before processing)

Read first 100 chars of each item. Classify type and assign depth budget:

| Type | Signal | Depth |
|------|--------|-------|
| INSTRUCTION | imperative verb, "do X", question | 500-5,000 tokens |
| IDEA | "what if", speculative, future-oriented | 1,000-5,000 tokens |
| MODEL_OUTPUT | AI-generated structure, assistant voice | 200-500 tokens (extract idea only) |
| SYSTEM_LOG | timestamps, paths, JSON, errors | 100-200 tokens (scan for facts) |
| HALF_THOUGHT | fragment, trails off, no clear action | 500-1,000 tokens (complete + infer) |
| REFERENCE | links, citations, docs | 100 tokens (catalog) |
| NOISE | duplicates, filler, "test" | 10 tokens (tag 🔴, skip) |
| UNKNOWN | can't classify | 1,000 tokens (deeper read) |

Add type + depth to batch doc under each item header.

## Step 2: PLAY (per prompt)

Execute the prompt. Not summarize — EXECUTE. The depth must match the item:

| Item Type | PLAY means | Minimum output |
|-----------|-----------|----------------|
| INSTRUCTION (build X) | Build it or write the code/artifact | Working artifact or complete spec |
| INSTRUCTION (research X) | Actually research, cite sources | Findings with URLs/evidence |
| IDEA (product/business) | Scope: prototype cost, token budget, hours, revenue math | Numbers, not vibes |
| MODEL_OUTPUT | Extract core, check if already done, assess current relevance | Decision: act/park/discard with reason |
| HALF_THOUGHT | Complete the thought, find the value path | Fleshed-out version with next step |

**Prototype cost formula** (for any buildable idea):
- Website/app: hours × $0 (we build) + API costs + hosting. Estimate tokens for AI-assisted build.
- Script/tool: lines of code estimate → token estimate (1 LOC ≈ 10-20 tokens to generate)
- Research: number of searches + fetches × ~500 tokens each
- Total = build tokens + test tokens + fix tokens (budget 30% extra for iteration)

**"Solid" means tested.** First pass is never solid. Flag items that need a second pass.

Append output under the prompt entry. Update status to `[~] PLAYING`.
Take factual notes: what was done, what was produced, what was discovered.

## Step 3: THINK (per prompt, immediately after PLAY)

Answer 5 questions (keep tight, 1-2 lines each):
1. **Learned**: factual takeaway
2. **Pertinent**: relevant to user's current projects/goals?
3. **Value**: creative thinking → value creation → money path?
4. **Act?**: yes/no — if yes, smallest next step
5. **Future**: park / discard / investigate deeper

Tag: 🟢 ACT NOW | 🟡 PARK | 🔴 DISCARD | 🔵 INVESTIGATE

Update status to `[x] DONE` with tag.

## Step 4: CHECKPOINT (every 5 prompts)

Brief summary: what's covered, patterns emerging, top value items so far.
Ask: "Continue, pause, or pivot?" — if no response in 30s, continue.

## Step 5: META-THINK (on "done" or batch exhausted)

Review all Think notes. Produce:
1. **Value Stack** — ranked by expected value
2. **Patterns** — themes, connections
3. **Action Items** — concrete next steps
4. **Park List** — not now but maybe later
5. **Discard List** — safe to ignore (1-line reason each)

Append to batch doc. Update status to `COMPLETE`.
Append 🟢 items to `systems/batch-cognition/value-stack.md`.
Append 🟡 items to `systems/batch-cognition/parked.md`.
Append 🔴 items to `systems/batch-cognition/discarded.md`.
Log any cross-batch connections to `systems/batch-cognition/connection-graph.md`.

## Commands (user can say anytime)

`skip` — skip current prompt | `deeper` — spend more tokens | `park` — park for later
`pause` — stop, resume later | `resume` — continue paused batch | `status` — show progress
`value stack` — show current ranked items | `done` — trigger meta-think + close

## Context Management

Rolling decay memory — each checkpoint creates a new block in a chain.
Items decay 20% per block. Referenced items reset to full weight. Below 0.2 = archived (never lost).
See [references/rolling-decay-memory.md](references/rolling-decay-memory.md) for full spec.

At each checkpoint:
1. Score all items: `salience *= 0.8`, re-referenced items → `1.0`
2. Drop items below 0.2 threshold (write tombstone, archive to disk)
3. Carry forward: rolling summary + surviving high-salience items + value stack
4. New block header written to chain file

Cross-batch: last batch's survivors enter new batch at 0.8, connect to new items → reset to 1.0.

See [references/drive-mode.md](references/drive-mode.md) when processing Drive folder dumps.

## Self-Improvement

After each batch, append to `workspace/systems/batch-cognition/learnings.md`:
- What worked / what was wasted / grouping improvements / play-think split effectiveness
- Update this skill if any rule changes warranted.

## Key Rules

- **SAVE FIRST** — never process before saving full batch to file
- **Never lose input** — if Telegram truncates or splits, wait for "done" before processing
- **Play and Think are separate** — don't blend execution with inference
- **Notes are mandatory** — both Play notes and Think notes, every prompt
- **Prompts aren't always instructions** — some are ideas, half-thoughts, value discovery. THINK phase handles these.
- **PLAY means EXECUTE, not summarize** — if it says build, build. If it says research, research with sources. If it's an idea, scope it with real numbers.
- **First pass is never final** — flag items that need deeper work. A 🟢 tag without execution is just a bookmark.
- **Prototype cost is mandatory for buildable ideas** — hours, tokens, API costs, hosting. Not vibes.
