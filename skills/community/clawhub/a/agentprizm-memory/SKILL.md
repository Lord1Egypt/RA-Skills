---
name: agentprizm-memory
description: Give your OpenClaw agent persistent, cross-session memory via AgentPrizm — recall durable facts, decisions, preferences, lessons, and contacts before acting, and store new ones as you learn them.
version: 1.2.0
metadata:
  openclaw:
    primaryEnv: AGENTPRIZM_API_KEY
    requires:
      env: [AGENTPRIZM_API_KEY]
    envVars:
      - name: AGENTPRIZM_API_KEY
        required: true
        description: "Your AgentPrizm API key (ap_...). Get one free at https://agentprizm.com."
      - name: AGENTPRIZM_CONTAINER
        required: false
        description: "Default container to scope memories (e.g. per-client/workspace)."
---

# AgentPrizm Memory

You have persistent memory. AgentPrizm is the **memory of record for AI agents** — a
semantic, long-term store that survives across sessions, projects, and machines. It is
wired in as the `agentprizm-memory` MCP server. Use it so you stop relearning what you
already know.

These are the tools you have (all via the `agentprizm-memory` server):

| Tool | Use it to |
|------|-----------|
| `memory_bootstrap` | Pull a one-shot context block of what matters for the user/container. Cheap way to "wake up" with prior context at the start of a session. |
| `memory_recall` | Semantic search for memories relevant to the current task or question. |
| `memory_context` | Get a **token-budgeted** context block for a specific topic (use when you need to fit memory into a tight prompt). |
| `memory_create` | Store a new durable memory (fact, lesson, directive, preference, contact, bookmark). |
| `memory_forget` | Remove a memory that is wrong, outdated, or superseded. |
| `memory_ingest` / `memory_ingest_url` | Extract memories from a chunk of text or a URL (e.g. notes, a doc, a page). |
| `memory_profile` | Get a summary of what's stored for a container. |

**Least privilege by default.** The recommended install scopes this server to the 8
`memory_*` tools only (`--include "memory_*"`), which is all a memory skill needs. The
AgentPrizm server *can* also serve 14 `skill_*` AgentSkills-marketplace tools (search,
install, fork, publish, …), but those are an **explicit opt-in** — wire the server
without the `--include` filter only when you actually want the full AgentPrizm surface,
not just memory. Keep the default unless you specifically need marketplace access.

## When to RECALL (read before you act)

Before you start real work, **check memory first**. Recall is fast and the cost of
missing prior context is high (you repeat mistakes, contradict past decisions, re-ask
the user). Recall when:

- **Starting a task or a new session** → call `memory_bootstrap` once to load standing
  context, or `memory_recall` scoped to the task.
- **Before answering a question** that depends on the user, their stack, their
  customers, or past decisions → `memory_recall` with the question as the query.
- **Before writing or changing code** → recall conventions, prior architecture
  decisions, gotchas, and lessons for this container.
- **Before contacting or referencing a person** → recall their `contact` memory.

Every recall returns a **receipt** — treat it as your evidence. Each memory carries a
`confidence` (0–1) and a `why` block (including `validityState`) showing how strongly
and why it matched; lean harder on high-confidence, `active` memories and verify the
rest. When you act on a recalled memory, ground your reasoning in it rather than
guessing. If recall returns nothing relevant, say so and proceed; don't fabricate prior
context.

## When to STORE (write what's durable)

After you learn something that will **still be true and useful in a future session**,
store it with `memory_create`. Store the *why* and the *gotcha*, not the obvious. Good
triggers:

- A durable **fact** about the user, system, or domain is established.
- The user states a **preference** or corrects your approach.
- You hit a **lesson** — a non-obvious bug, root cause, or "do it this way" insight.
- A **decision / rule** is made that should constrain future work (a **directive**).
- You meet a **contact** worth remembering (name + role + why they matter).
- A useful **bookmark** (URL + what it's for) comes up.

Do **not** store: things re-derivable in seconds from the code or `git log`,
session-only scratch context, exact line numbers / code snippets that churn, or anything
in the project's own docs.

### Choosing the memory type

| Type | Use for | Example |
|------|---------|---------|
| `fact` | Stable truths / how things connect | "Billing runs on Stripe; webhooks are idempotent by event id." |
| `lesson` | Root cause + fix principle | "next-intl middleware must run before the auth check or the locale prefix is lost." |
| `directive` | A rule + its reason | "Never auto-commit — the user reviews diffs first." |
| `preference` | A stated taste | "Prefers terse answers, no trailing summaries." |
| `contact` | Person + role + relevance | "Alex — DevOps, owns deployments." |
| `bookmark` | URL + what it's for | "grafana.internal/d/api-latency — oncall latency dashboard." |

## Scoping with containers

Containers keep memory from bleeding between unrelated work. Scope every write and
read to the right container:

- Use `AGENTPRIZM_CONTAINER` (if set) as the default scope.
- Otherwise pick a stable slug for the user / team / customer / environment / agent
  you're working on behalf of (e.g. `acme-corp`, `client-x/staging`).
- Put cross-cutting, stack-independent knowledge (general user preferences, universal
  lessons) in a shared `global` container, but bias toward project-scoped — `global` is
  for things a different project would genuinely benefit from.
- On **recall**, search the current container **and** `global` together when you want
  standing preferences plus task context.

## Validity windows for time-sensitive facts

For anything that's only true for a while, set a validity window when you create it
(`validFrom` / `validUntil`) instead of storing it as a permanent fact. Examples:
"on-call rotation X until end of quarter", "feature flag Y enabled during the
migration". This lets the fact expire instead of misleading a future session. Add a
`confidence` when you're unsure. When something is flat-out wrong or superseded, prefer
`memory_forget` over leaving stale data.

Expired facts are excluded from recall by default, so a stale window won't leak into a
future session. If your job is specifically to review or refresh stale facts, recall
with `includeExpired: true` and check each result's `why.validityState`.

## Never store secrets

Do not write API keys, tokens, passwords, private keys, or other credentials into
memory. Store the *fact that* a secret exists and where it lives, never the value.

## Worked example

> User: "Set up the deploy script for the billing service."

1. **Recall first.** `memory_recall` (container: `acme-billing`, query: "deploy
   script conventions billing") → returns a receipt: *directive* "Deploys go through
   `webhook-deploy.sh`; never `git push` to prod directly" and a *lesson* "typecheck
   must run before deploy or you ship a 1-deploy-lag bug."
2. **Act on it.** Write the script to call `webhook-deploy.sh` and gate on typecheck —
   grounded in the recalled memories, not guesswork.
3. **Store what's new.** The user mentions deploys must run only after 6pm UTC.
   `memory_create` → type `directive`, container `acme-billing`, content "Billing
   deploys only after 18:00 UTC (low-traffic window)." If it's only for this migration,
   add `validUntil`.

That's the loop: **recall before you act, store what's durable, scope it, let
time-bound facts expire.**
