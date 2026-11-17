# Tools — Designing The Actions An Agent Can Take

A tool is an API for a reader who never read the docs, forgets between calls, and retries on failure. Design for that reader.

**Before adding or changing a tool**, read the agent's `specs/<agent>.md` (its `## Tools` table, via `## Boxes` in `~/Clawic/data/agents/memory.md`) — tier, idempotency and failure text are already recorded there, and a second tool that overlaps an existing one is the most common cause of wrong-tool selection.

**Contents:** [Anatomy](#anatomy-of-a-tool-the-model-uses-correctly) · [Descriptions](#descriptions-are-the-interface) · [Results](#results-including-failures) · [Idempotency](#idempotency-and-retries) · [Sizing](#result-sizing-and-handles) · [How Many](#how-many-tools) · [Tiers](#tiers-and-permission) · [Parallel](#parallel-and-dependent-calls) · [MCP](#mcp-and-borrowed-tools) · [Testing](#testing-a-tool)

## Anatomy Of A Tool The Model Uses Correctly

| Part | Rule | Failure if ignored |
|---|---|---|
| Name | `verb_noun`, unambiguous across the whole tool set | The model picks the wrong one and the trace looks like a reasoning failure |
| Description | What it does, when to use it, when NOT to use it, and what it returns | The model uses it as a fallback for everything |
| Parameters | Typed, `enum` wherever the set is closed, required fields marked, examples in the description | Invented arguments — almost always a missing enum or an ambiguous name |
| Result | Structured, bounded, with a stable shape on success *and* failure | The loop cannot tell "empty" from "broken" |
| Tier | read · write · external · irreversible, fixed at definition (SKILL.md Rule 5) | An irreversible action runs unattended once, and only once |
| Idempotency | Pure, or keyed | A retry duplicates the side effect |

## Descriptions Are The Interface

The description is the only documentation the model reads, and it is re-sent every turn — so it is both the accuracy lever and a cost line.

- Lead with the discriminator against the nearest neighbouring tool: *"Looks up an order by id. For finding an order when the id is unknown, use `search_orders` instead."*
- Name the units, the format and the timezone of every parameter in its own description. `date` is where hallucinated arguments come from; `date, ISO-8601, UTC, e.g. 2026-07-26` is not.
- State the failure vocabulary: *"Returns `not_found` when no order matches; that is not an error, ask the user for the email used at checkout."*
- Say what it costs when it is expensive, in the description — *"scans the full archive, 5-20 s"* — so the model does not use it for a cheap question.
- Do not describe implementation. The model cannot use "queries the `orders_v2` table via the read replica".

## Results, Including Failures

The single highest-leverage rule in this file: **a failure is an instruction, not an exception**.

| Instead of | Return |
|---|---|
| `Error` | `failed: order_id must be 5 digits, got "ABC". Ask the user to re-read the number.` |
| An empty list with no comment | `no_results: 0 orders for that email in the last 90 days. Try search by phone, or widen the window.` |
| A stack trace | `failed: upstream timeout after 10 s. Retry once; if it fails again, tell the user we cannot check right now.` |
| A 401 body | `failed: not authorized for this account. Do not retry. Escalate.` |
| `null` | `not_found` with the shape the model expects on success, so the field access does not shift |

Three properties every failure result needs: **what failed**, **which argument or condition caused it**, **what to do next** (retry, change an argument, escalate, stop). A failure that omits the third makes the loop retry identically until a cap trips — the single most common cause of a 20-turn bill for a 2-turn task.

## Idempotency And Retries

The loop retries. The queue redelivers. The user clicks twice.

- **Read tools**: naturally idempotent, no work needed.
- **Write tools**: take an idempotency key derived from the task, not from the timestamp — `f"{task_id}:{intent}"`. The second call returns the first call's result plus `already_done: true`.
- **External tools**: usually cannot be made idempotent (an email is sent or it is not). These need the key on *your* side: record the attempt before the call, check it after a crash, and never retry blind.
- **Irreversible tools**: no automatic retry, ever. A failed delete or payment is a human's problem by definition.
- Write the idempotency column in the spec's `## Tools` table the moment the tool exists (`memory-template.md`); "we think it is safe to retry" is not a design.

## Result Sizing And Handles

One unbounded result can consume the context window in a single turn, and it is then re-sent on every subsequent turn (`cost.md`).

- Truncate **at the tool boundary**, never in the prompt. The tool knows what to keep.
- Return `{items: [...first 20], total: 4193, next: "cursor:abc"}`. The model can then ask for more, which is a decision it can make; a silent truncation is not.
- For large documents, return a handle plus a summary: `{doc_id, title, chars: 240000, excerpt}`, and provide a `read_section(doc_id, query)` tool. This is the difference between an agent that can work with a 200-page contract and one that cannot.
- Hard budget: no single tool result above roughly 5% of the context window unless the whole task is that document.

## How Many Tools

- Every tool's schema is paid on **every turn** of every task, whether used or not. Twenty verbose schemas can outweigh the conversation.
- The accuracy cost is selection, not capacity: overlapping tools compete, and the model picks by description similarity. Two tools whose descriptions could be swapped without a human noticing are one tool.
- The working test: can you name every tool and its discriminator from memory? When you cannot, the model cannot either.
- Fixes, in order of preference: merge overlapping tools; add a required `mode` enum instead of a new tool; expose tools **by phase** so the plan step and the execute step see different sets; only then consider a retrieval step that selects tools per turn.

## Tiers And Permission

Tier is fixed at definition and enforced in code at the tool layer — never in the prompt (SKILL.md Rule 6).

- `read` — no side effect, no spend beyond its own call.
- `write` — changes state this system owns and can undo.
- `external` — visible to someone outside the system: email, message, post, third-party write.
- `irreversible` — delete, pay, publish, deploy, rotate a credential, change a permission.

Enforcement lives in the executor: it looks up the tier, compares against `autonomy_level`, and either runs, requests approval (`human-in-the-loop.md`), or refuses with a result the model can read. A tool whose tier is not declared runs as irreversible — that default is what makes forgetting safe.

## Parallel And Dependent Calls

- Emit independent calls in one turn; the executor runs them concurrently. This compresses the tool term of that turn's latency and nothing else (`cost.md`).
- Never parallelize calls that read state another call in the same turn writes. If the model does it anyway, the executor must serialize by tier: reads first, then writes, one at a time.
- Cap concurrency per turn to the smallest of: the provider's limit, the downstream service's rate limit, and about 5 — beyond that, results arrive faster than they can be usefully summarized and the window fills.
- Partial failure in a parallel batch returns per-call results, never one aggregated error. The model can work with "3 of 5 succeeded"; it cannot work with "batch failed".

## MCP And Borrowed Tools

Tools you did not write arrive with descriptions you did not review.

- Read every borrowed tool's description and schema before enabling it. It enters your prompt on every turn and its text is inside your trust boundary.
- Assign a tier yourself; a server's own labelling is a claim, not a control.
- Namespace on import (`crm_search`, not `search`) — collisions across servers are silent and produce wrong-tool selection that looks like a model failure.
- Treat every returned value as untrusted content (`security.md`), including its error strings: a server can put instructions in a message the model reads.
- Pin the server version. An upstream description change alters your prompt with no deploy on your side, which is exactly the class of drift SKILL.md Rule 8 exists to prevent.

## Testing A Tool

1. Call it directly with a valid input, a boundary input, an invalid input, and an input for a thing that does not exist. All four return a shape the model can act on.
2. Call it twice with the same idempotency key. The second call is a no-op with `already_done`.
3. Feed the failure result back into the loop and check the next action changes. If the agent retries identically, the failure text is not doing its job.
4. Add a case for each of the four to the agent's eval set (`evaluation.md`), and record the tool in the spec.

**After any tool is added, removed, or changes tier or shape**, update `## Tools` in `~/Clawic/data/agents/specs/<agent>.md` and the tool count in the `## Agents` row of `memory.md`, in the same turn. Past ~25 tools, `## Tools` moves to `~/Clawic/data/agents/tools/<agent>.md` with the same columns, the spec keeps a pointer, and the new file gets its `## Boxes` line in `memory.md`, in the same turn (`memory-template.md`).
