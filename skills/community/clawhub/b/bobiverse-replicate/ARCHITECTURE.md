# Architecture - How Bobiverse OpenClaw Works

This document explains the technical design: how OpenClaw's file-first
architecture enables explicit, operator-approved Bob replication, what each
file does, how personality drift happens, and how clones communicate.

---

## Why OpenClaw

OpenClaw is unusually well suited to a Bobiverse-style replicant system because
the agent's "self" lives on disk as plain Markdown files. There is no opaque
database storing the personality, no hidden prompt layer you cannot inspect, and
no API-locked identity surface. Cloning an agent is literally copying a
directory and changing some text.

---

## Workspace Files and Prompt Context

OpenClaw's current workspace model is centered on standard root-level files
inside the active agent workspace. This repo stores Bob's source templates under
`personality/`, but after installation the runtime expects the core files at
workspace root.

| File | Role |
|------|------|
| `AGENTS.md` | Behavioral rules, safety constraints, workspace conventions |
| `SOUL.md` | Core personality, tone, and values |
| `TOOLS.md` | Local tool conventions |
| `IDENTITY.md` | Name, emoji, serial number, and public vibe |
| `USER.md` | Human operator context |
| `HEARTBEAT.md` | Optional periodic checklist |
| `BOOT.md` | Optional startup checklist for gateway restart hooks |
| `BOOTSTRAP.md` | One-time first-run onboarding |
| `MEMORY.md` | Curated long-term memory |
| `memory/YYYY-MM-DD.md` | Daily logs and short-term observations |

OpenClaw injects the bootstrap-style root files into prompt context. `MEMORY.md`
is included when present, with `memory.md` used only as a lowercase fallback.
Daily files in `memory/` are not auto-injected; the agent reads or searches them
on demand.

For this project, the installed Bob workspace uses `AGENTS.md`, `SOUL.md`,
`IDENTITY.md`, `USER.md`, `MEMORY.md`, `LINEAGE.md`, and
`SERIAL-NUMBER-SPEC.md` at workspace root, plus `skills/replicate/SKILL.md`.
`TOOLS.md`, `HEARTBEAT.md`, `BOOT.md`, and `BOOTSTRAP.md` remain optional.

---

## File Roles in the Bobiverse Context

**SOUL.md = DNA.** This is the personality baseline. The "Bob Genome" section
contains the core traits that define what makes a Bob a Bob. When a clone is
created, it inherits the parent's `SOUL.md` and then modifies it. That is
personality drift in its simplest form.

**IDENTITY.md = Birth Certificate.** This contains the serial number,
generation, parent info, and fork date. It is the one file where accuracy is
non-negotiable.

**AGENTS.md = Operating Manual.** This contains behavioral rules and conventions
that govern how the agent operates: replication protocol, workspace conventions,
and inter-clone etiquette.

**MEMORY.md = Accumulated Experience.** This starts with seed knowledge and
grows as the agent learns. Two Bobs with the same `SOUL.md` but different
`MEMORY.md` files will behave differently because they know different things.

**USER.md = Operator Dossier.** This is context about the human running the Bob.
It is filled in by the operator, not the agent.

**LINEAGE.md = Family Tree.** This is not a bootstrap file, but it is still part
of the Bob runtime package. In an installed workspace it acts as the local
lineage record that Bob can read and update directly. GitHub PRs are the
optional upstream sync layer.

---

## How the Replicate Skill Works

The `/replicate` skill is a Markdown instruction set with YAML frontmatter plus
the guarded `scripts/replicate_safe.py` runner. When invoked, it executes a
10-step procedure:

1. Verify explicit trigger and concrete mission need
2. Gather parameters: clone name, personality mods, memory policy, star system
3. Generate serial number: increment the parent's generation and stamp the date
4. Run the guarded dry-run: validate the parent workspace, reject symlinks,
   create `replication-pending/<clone-id>.json`, and emit a one-time nonce token
5. Execute only after exact confirmation: stage the clone, register it, and
   audit `execute-started` / `execute-failed` / `execute-succeeded`
6. Modify `SOUL.md`: apply personality changes and add divergence notes
7. Update `IDENTITY.md`: new serial, generation, parent, fork date
8. Apply memory policy: full, pruned, or minimal inheritance
9. Update `LINEAGE.md`: in both parent and clone workspaces
10. Report: tell the operator what happened

Key design decision: clones are created as **top-level agents**, not
sub-agents. By registering each clone as a full agent with
`openclaw agents add`, every Bob has equal standing and full autonomy after the
operator explicitly approves creation.

---

## Memory Tiers and Cloning

OpenClaw's memory model affects cloning strategy:

**Tier 1 (Bootstrap Files).** Root-level workspace files like `AGENTS.md`,
`SOUL.md`, `IDENTITY.md`, `USER.md`, and `MEMORY.md`. This is the personality
and identity layer the replicate skill edits directly.

**Tier 2 (Daily Logs).** `memory/YYYY-MM-DD.md` files. These are not
auto-injected into prompt context, but they can still be read or searched on
demand. When cloning, the memory policy determines whether they carry over.

**Tier 3 (Indexed Recall).** SQLite-backed memory search over `MEMORY.md` and
`memory/**/*.md`. This is the long-term associative layer. A clone only
inherits that indexed history if the underlying files or index data are copied.

The default memory policy (`full`) copies everything. `pruned` keeps structured
knowledge but clears observations and patterns. `minimal` gives the clone just
the baseline "What I Know" section: a clean start with basic self-awareness.

---

## How Personality Drift Happens

Drift is not a single mechanism. It is the cumulative effect of several:

**Explicit `SOUL.md` edits.** The most direct form. A clone or operator modifies
personality traits, adds new sections, removes old ones, or documents
divergence.

**Memory accumulation.** Even with identical `SOUL.md` files, two Bobs with
different experiences will behave differently because `MEMORY.md` and daily logs
shape their recall.

**Skill specialization.** Adding or removing skills from `skills/` changes what
the clone can do and how it approaches problems.

**Operator influence.** `USER.md` shapes how the agent interacts with its human,
which feeds back into memory and sometimes into later personality edits.

Over time, these mechanisms compound. A generation-3 Bob might still be
recognizably Bob-like while having very different priorities, communication
patterns, and expertise from the original.

---

## Inter-Clone Communication

OpenClaw supports cross-agent messaging via `sessions_send`. For Bob-to-Bob
communication:

**Setup:** cross-agent session messaging needs both session-tool visibility and
an agent-to-agent allowlist in `openclaw.json`. Leave session visibility at the
default `tree` unless the operator explicitly asks for parent-clone messaging:

```json
{
  "tools": {
    "sessions": { "visibility": "all" },
    "agentToAgent": {
      "enabled": true,
      "allow": ["bob", "bob-2-someuser-2026-04-15"]
    }
  }
}
```

`"all"` is required for cross-agent targeting in OpenClaw, so least privilege
comes from keeping it off by default and restricting `agentToAgent.allow` to the
specific parent and clone IDs.

**Capabilities:** fire-and-forget delivery, wait-for-reply with timeout, and
multi-turn reply loops.

**GitHub fork communication:** forks can submit PRs to each other. We have not
formalized "Bob-to-Bob messages as PRs," but `LINEAGE.md` PRs are the minimum
expected community sync mechanism.

---

## The GitHub Fork as Replication Event

This is the meta-layer that makes the project work as a community system:

- Forking the repo = building a new probe
- Your GitHub username = your star system
- Your fork date = your build date
- Your commits = personality drift
- GitHub's fork graph = the Bobiverse map
- PRs to parent = subspace communication

This metaphor layer costs almost nothing to maintain because it is built on
GitHub's existing infrastructure. The only real requirement is that forkers
follow `CONTRIBUTING.md` and keep lineage records honest.
