# Rolling Decay Memory — Chain-Linked Context Blocks
# Extension to Batch Cognition System

## Concept

Memory blocks linked like a chain. Each block retains 80% of the previous block's
context by salience, drops 20% to archive. Items referenced across blocks survive
(weight resets). Items never referenced decay and fall off the working set — but
are always recoverable from the chain on disk.

Incremented by WORKFLOW (checkpoints, pauses, batch boundaries), not by time.

## Block Format

```markdown
## Block [N] — [trigger: checkpoint|pause|batch-end|resume]
- **Parent**: Block [N-1] hash/link
- **Carried** (80%): [rolling summary of surviving context]
- **Dropped** (20%): [1-line tombstones of what decayed]
- **Promoted**: [items re-referenced this block → weight reset]
- **Added**: [new items processed this block]
- **Working context size**: [token estimate]
```

## Decay Rules

1. Every item has a **salience score** (0.0 to 1.0)
2. New items enter at 1.0
3. At each block boundary, all items decay: `score *= 0.8`
4. If an item is **referenced** (comes up in THINK, connects to new item, user asks about it): `score = 1.0` (full reset)
5. Items below **0.2 threshold** drop from working context → archived with tombstone
6. Tombstone format: `[block N] "first 40 chars..." — dropped (score 0.18, never re-referenced)`

## What Survives

- Items that keep being relevant (referenced across blocks) → permanent working memory
- Items that were one-off but high-value → survive a few blocks then archive with full record
- Noise → drops after 1-2 blocks (score 1.0 → 0.8 → 0.64 → 0.51 → 0.41 → 0.33 → 0.26 → 0.21 → DROPPED)
- That's ~8 blocks before something completely unreferenced falls off

## Recovery

Nothing is deleted. The chain is on disk. To recover:
1. Read block headers backward until you find the tombstone
2. The tombstone links to the original batch doc + item number
3. Pull the full content from the batch doc

This means: **working context is always lean, but total knowledge is always complete.**

## Integration with Batch Cognition

```
SAVE → PRE-SCAN → [Block 0: all items at score 1.0]
                        │
Process items 1-5 → CHECKPOINT → [Block 1: decay, drop, promote]
                                      │
Process items 6-10 → CHECKPOINT → [Block 2: decay, drop, promote]
                                       │
                                      ...
                                       │
DONE → META-THINK → [Final Block: only high-salience items remain]
                         │
                    Surviving items → value-stack.md (permanent)
                    Dropped items → recoverable via chain
```

## Cross-Batch Persistence

When a NEW batch starts:
1. Read last batch's final block (the surviving high-salience items)
2. These enter the new batch at score 0.8 (slight decay for being from a prior batch)
3. If they connect to new items → score resets to 1.0 (cross-batch connection!)
4. If they don't connect → they continue decaying and eventually archive

This creates **compounding intelligence**: ideas that keep being relevant across multiple
batches become effectively permanent. Ideas that were one-session wonders fade gracefully.

## Why Workflow-Incremented, Not Time-Incremented

- Time-based: "delete after 7 days" — arbitrary, kills good stuff, keeps stale stuff
- Workflow-based: "decay at each cognitive checkpoint" — the WORK determines what matters
- A batch of 5 items might have 1 block. A batch of 500 might have 100 blocks.
- Pausing and resuming creates a block boundary (natural context shift)
- The user saying "actually that thing from earlier" promotes it (reference = weight reset)

## Implementation Notes

- Salience scores stored in batch doc alongside each item
- Block headers written to `systems/batch-cognition/chain/[batch-id]-blocks.md`
- Chain index: `systems/batch-cognition/chain/INDEX.md` (links all chains)
- Token budget per block: aim for working context ≤ 2,000 tokens
- Archive is the batch doc itself — always complete on disk
