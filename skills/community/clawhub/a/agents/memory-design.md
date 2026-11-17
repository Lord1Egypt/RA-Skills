# Memory Design — What The Agent You Are Building Should Remember

This page is about the memory of the agent under construction. It is not about your own notes on this user's build — those live in `~/Clawic/data/agents/` and their rules are in `memory-template.md`. Keep the two separate in every conversation, or advice about one gets applied to the other.

**Before proposing a memory design**, read the agent's `specs/<agent>.md` (its memory policy section, via `## Boxes` in `~/Clawic/data/agents/memory.md`). Changing a memory strategy that already has data behind it is a migration, not an edit.

## The Four Kinds, And The One Question That Sorts Them

| Kind | Lifetime | Holds | Implementation | Lost if you skip it |
|---|---|---|---|---|
| Working | This task | Current goal, plan, tool results, committed side effects | The context window plus a state block (`context.md`) | The agent repeats actions and re-asks questions |
| Episodic | Across sessions with the same user or subject | What happened, when, and what was decided | Append-only records, summarized on read | "As I told you last week" fails |
| Semantic | Indefinite | Facts: preferences, entities, policies, account state | Explicit state records; embeddings only for the long tail | The agent is a stranger every time |
| Procedural | Indefinite | How to do things here | The system prompt, tools, and workflows — code, not data | The agent relearns your process every task |

The sorting question is not "how long does it live" but **"what breaks if this is wrong versus merely missing?"** A fact that must be right (current plan, account tier, allergy, active order) belongs in explicit state. A fact that is nice to have (a preference mentioned once, a past topic) can live in recall.

## State Versus Recall

- **State** is a small, readable, addressable record: a key, a value, a timestamp, a source. It is correct or it is visibly wrong, and it is cheap to audit.
- **Recall** is similarity search over past text. It returns *similar*, which is not *true*: a superseded fact scores as well as its replacement and often better, because the older text is longer.
- Default: state for anything the agent asserts or acts on; recall for the long tail of "have we discussed this before". **State wins on conflict**, always, and the conflicting recalled passage is dropped from the context rather than presented alongside.
- If you cannot say which store a given fact lives in, the agent cannot either — that ambiguity is the source of the contradictions users notice first.

## The Write Policy

Most memory systems fail on writes, not reads. Decide these five before implementing:

1. **What triggers a write** — a user statement of preference, a completed task, a corrected mistake, a resolved entity. Never "everything interesting".
2. **Who writes** — a deliberate write step at the end of the turn, or a dedicated tool the model calls. A background summarizer writing unsupervised produces a store nobody trusts.
3. **Update or append** — a preference is updated in place, keyed; an event is appended. Choosing wrong gives you either a lost history or fifteen versions of the same preference.
4. **Provenance** — every record carries when it was written and what it came from (user statement, tool result, inference). An inference and a statement must never be indistinguishable later.
5. **Conflict rule** — newer beats older; a user statement beats an inference; an authoritative system beats both. Write the rule down; the agent will hit the case.

## Retrieval Policy

- Retrieve on demand, per turn, scoped to the current goal — not a blanket dump at session start (`context.md`).
- Keep the injected block small enough that a human would read it. If it is bigger than that, the agent is being given a haystack.
- Inject retrieved memory **late** in the prompt, after the stable prefix, or every turn invalidates the cache (`cost.md`).
- Include the timestamp with each recalled item. Without it the model cannot tell a current fact from a stale one, and it will not ask.

## Staleness And Forgetting

A memory store that only grows becomes wrong faster than it becomes useful.

- **Supersede, do not accumulate.** When a keyed fact changes, replace the value and keep one previous version at most. Two live values for one key is a bug with a delayed fuse.
- **Expire by class**: volatile facts (current order, today's plan) expire in days; stable ones (preferences, entity identity) do not expire but get re-confirmed when acted on in a high-stakes way.
- **Decay recall by recency and use.** An item never retrieved in months is noise competing with signal.
- **Deletion must be real and reachable.** A user asking to be forgotten must remove the record, the embedding, the summary that quoted it, and the traces — plan for this at design time, because retrofitting deletion across four stores is a project (`security.md`).

## Sizing And Cost

- Every injected memory token is paid on that turn and, if it lands in the transcript, on every turn after. Memory is a recurring cost, not a one-time one.
- Budget it explicitly: a fixed cap for injected memory per turn, enforced by truncation with the oldest or lowest-scoring items dropped first.
- Summarize episodic records on write, not on read. Summarizing on read pays the summarization cost every time and produces a different summary each time.
- Per-user stores scale with users, not with tasks. Measure the store's growth per active user per month before promising it is free.

## Multi-User And Multi-Tenant

- Namespace every record by tenant and user at the storage layer, not by a filter in the query. A missing filter is the classic cross-tenant leak (`security.md`).
- Shared organizational memory (policies, product facts) is a separate store from personal memory, with different write permissions — otherwise one user's correction becomes everyone's fact.
- Personal data written into a memory store inherits retention and deletion obligations. Decide before launch what is stored, for how long, and who can read it.

## Testing Memory

1. Two-session test: state a fact in session one, ask something that requires it in session two. Assert the retrieval, not the answer.
2. Contradiction test: state a fact, then contradict it. The agent must use the newer one and must not present both.
3. Staleness test: age a volatile fact past its expiry and confirm it is not used.
4. Isolation test: user A's fact must never appear for user B. Automate this one; it is the failure that ends a product.
5. Every one of these is a case in the eval set with `n` runs, not a manual check (`evaluation.md`).

**When a memory strategy is chosen**, write it into the agent's `specs/<agent>.md` memory-policy section — the four kinds in use, the write triggers, the conflict rule, the expiry classes — and record the decision with what was rejected in `~/Clawic/data/agents/artifacts/decision-memory-<agent>.md` with its `## Boxes` line, in the same turn (`memory-template.md`). Memory strategies get reversed a year later by someone who does not know why vector recall was rejected the first time.
