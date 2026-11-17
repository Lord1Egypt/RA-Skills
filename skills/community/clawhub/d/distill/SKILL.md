---
name: distill
description: >-
  Session knowledge distillation: assign what you just learned in this
  session into an agent's four-layer persistent knowledge base (rule /
  memory / skill / decision record). The core is four disciplines — search
  before adding, pick the right layer, guard against bloat, and run a
  hygiene pass before landing anything. Fits agent workflows that already
  have (or want to build) these four layers; this is not a general note-
  taking tool. Invoke explicitly at the end of a session to consolidate
  what was learned.
---

# distill — session knowledge → four-layer knowledge base

Turn "what this session just learned" into durable knowledge. This is the dual of foraging: foraging pulls external material into a project's library; distilling pushes internal experience out into persistent form.

> **Fill in paths and naming conventions for your own project and IDE.** This document uses placeholder notation and is not tied to any specific toolchain.
>
> **Prerequisite**: your agent already has (or you want to build) all four of these — persistent rules, persistent memory, skills, and decision records. If all you have is a single markdown notebook, this layering is over-engineering — just write it down.

## 1. Scan the session for distillable signals

Ask, category by category:

- **What bug did you fix**, and what was the root cause and the fix (especially anything counter-intuitive)?
- **What gotcha did you hit** (a tool's quirky behavior, an environment difference, an API that doesn't do what its docs say)?
- **What decision got made**, and were there real alternatives on the table?
- **What pattern worked, or failed** (at the methodology level)?
- **What did the user correct** ("that's wrong", "you missed X")? → **the strongest signal** — it means your default behavior systematically diverged from what they expected
- **What did you hand-build a second time** → a skill candidate

## 2. Assign each item to a layer

**Scope first, layer second.** For every candidate, ask: *would this still hold in a different project?*

- **Still holds** (a tool's quirks, how you collaborate, engineering discipline, reporting preferences) → **global scope**: the agent's global instruction file or global memory. **Never write it into a project-scoped bucket** — a project bucket is only read by sessions inside that project, so a genuinely portable lesson written there is forgotten the moment you switch projects.
- **Only holds in this project** (paths, accounts, deployment topology, business constraints, this repo's specific traps) → project scope, per the table below.
- **Before writing a memory, confirm which bucket you're actually writing into.** Memory buckets are usually derived from the working directory, so a renamed directory, or a path containing non-ASCII characters that collides on a hash, can silently route a memory into someone else's bucket.

> **Why this comes first**: a full-archive scan once found that completely generic lessons — "verify before asserting," "concurrent-session discipline" — existed in only two of thirty-odd project buckets, and every later incident traced back to a project that lacked them. The lesson had been written down; it was just written in the wrong place. The same scan found one project's memory had silently landed inside a different project's library entirely, due to a path hash collision — undetected until then.

| Signal | Goes into | Typical destination (per your IDE's convention) |
|---|---|---|
| A guardrail that should **trigger automatically** ("never do X", "when doing Y, check Z first") | **Rule** | Your IDE's rules mechanism |
| A **fact or lesson to recall on demand** (a preference, a gotcha, project state) | **Memory** | The agent's persistent memory (memory files + an index) |
| A **complete reusable workflow** | **Skill** | Your IDE's skills directory (`<name>/SKILL.md`) |
| An **architectural or process decision with real alternatives** | **Decision record** | The project's ADR directory |

Memory splits into four kinds: `user` (who they are), `feedback` (how to collaborate with them — always with a why and a how), `project` (what's currently in flight), `reference` (a pointer to something external).

## 3. Core discipline

Three rules keep distillation from rotting:

1. **Search before adding.** Before adding a rule, memory, or skill, grep for what already exists. **Already covered → update that one entry. Never create a duplicate.**
2. **Layer heuristic.** An automatic guardrail → rule; a fact to recall → memory; a reusable workflow → skill; a decision with alternatives → decision record. The same lesson can legitimately be both a memory (the fact) and a rule (the guardrail) — but don't duplicate the content twice; **the rule references the memory, it doesn't copy it.**
3. **Guard against bloat.** Rule and skill descriptions are a standing cost — every one of them burns tokens on every single session. Only keep high-value ones; a description should say only "what it is + when to use it," **never a pile of trigger keywords**; **reference, don't copy** — point at what already exists instead of re-pasting it. When in doubt, don't add it — never pad for the sake of padding.

> **Why rule 1 comes first**: in one real collaboration, the same mistake happened twice — once, a new document was created when the repository already had one covering the same ground, nobody had found it; the second time, an entire rename effort was carried out for a name that had already belonged to that account for two weeks, because a search had missed one namespace. Both traced back to the same root cause: **nobody enumerated exhaustively before acting.** A knowledge base rarely rots from having too little written down — it rots from the same fact being written three times, each version slightly contradicting the others, with nobody sure which one to trust.

## 4. Hygiene before landing anything

- **Concurrent sessions**: the repo may have another session's changes in flight → run `git status` first, and **stage only your own specific paths** (never `-A` or `.`) — don't sweep up someone else's in-progress work. Pull with `--ff-only` first if there's a remote.
- **A new skill** → also add whatever symlink or registration step your IDE needs, or it sits on disk invisible to the agent.
- **A new memory** → add one line to the memory file and one line to its index.
- **A decision record with cascading follow-ups** → verify every follow-up item actually landed where it was supposed to.
- **A finished decision record** → manually add a row to the ADR index's "recent" table. Freshness-checking tools usually don't validate this table, so a missing row drifts silently — **"the tool passed" does not mean "the index is complete"** (this exact row has been missed by three different authors in a row on one project).
- **Run the project's checks** (tests / lint / index checks) after any edit, and **they must all pass** before you commit — and run *every* check that pipeline has, not just the ones you're used to running. The one you skip is exactly the one that catches you in CI.
- Some IDE-managed directories are unreliable to write to via shell → use your editor tooling instead, and commit before you touch anything there.

## 5. Output

Give the user an **allocation table**: for each piece of knowledge, which scope it went into (global / project) × which layer (rule / memory / skill / decision record), why, and — just as important — **what you decided not to add, and why** (already covered / not high-value enough). Reporting what you left out is as important as reporting what you added — it's the proof you actually filtered, rather than dumping the whole session back out.

## Don't

- Don't pad low-value memories or rules to look thorough. The bloat tax is real: every standing description gets billed on every future session.
- Don't commit another session's in-progress changes as if they were your own distillation.
- A big decision (an architecture change, a long-running initiative) → pair it with a decision record. A small operational detail → hang it off an existing workflow or rule instead. Don't open a decision record for every little thing.
