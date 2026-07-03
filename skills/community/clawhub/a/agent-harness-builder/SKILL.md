---
name: agent-harness-builder
description: Build a complete multi-agent orchestration harness for an OpenClaw (or similar) agentic system — defining a CTO/orchestrator agent, tiered specialist agents, context-routing rules, model assignment, memory limits, Slack channel architecture, and a step-by-step implementation guide. Use this skill whenever someone wants to design, document, structure, or hand off an AI agent fleet; mentions orchestrating multiple agents, an "agent harness," agent roles/profiles, a CTO agent, agent routing, or distributing skills/context/models across agents; or wants a packaged architecture doc set they can give to an orchestrator agent or a team. Trigger this even if they just describe the problem ("I have 20 agents and need one to coordinate them") without using the word "harness."
---

# Agent Harness Builder

Build a clean, handoff-ready orchestration architecture for a fleet of AI agents. The output is a set of Markdown documents the user can drop into their orchestrator agent's workspace and hand off directly.

## Core Philosophy

The orchestrator is the brain; every other agent is a hand. The orchestrator does not do the work — it decides *who* does the work, with *what* context, using *what* model, then monitors and synthesizes results.

The single most important design principle: **the orchestrator is informed by agents, not subscribed to everything.** Dumping every channel/message into the orchestrator's context is what causes memory bloat and degraded performance. Agents filter noise into structured reports; only signal reaches the orchestrator.

## When to use this skill

Use it when the user wants any of: an agent roster with defined roles, a routing/delegation system, an orchestrator agent spec, context/memory management rules across agents, model-tier assignment, or a packaged set of docs to hand to their team or their orchestrator agent.

## The Build Process

Follow these steps. Gather what you can from the conversation before asking — the user may have already described their agents, businesses, or tooling.

### Step 1 — Gather inputs

You need:
1. **The orchestrator** — name and role (e.g. "Tori, CTO")
2. **The agent roster** — names, roles, and which project/domain each serves. If the user has a list, table, or PDF, extract from it.
3. **The businesses/domains** the agents support
4. **Available models** and rough cost order (e.g. a cheap local/open model, a mid-tier API model, a premium API model)
5. **The comms layer** — usually Slack channels, but could be Discord, etc.

If the user has fewer than ~5 agents, this is probably overkill — tell them so and offer a lighter structure.

### Step 2 — Assign tiers

Sort every agent into a tier. This drives model budget and memory limits.

- **Tier 0 — Orchestrator**: routes, delegates, synthesizes. Premium model. Largest memory.
- **Tier 1 — Senior Specialists**: complex, multi-step, judgment-heavy work (lead devs, architects, PR directors, strategists). Mid-to-premium model with fallback.
- **Tier 2 — Domain Workers**: focused, repeatable, domain-specific tasks (admins, schedulers, marketing specialists). Cheap model.
- **Tier 3 — Utility Agents**: single-function, high-volume, fast (formatters, validators, artists, summarizers). Cheapest/local model.

### Step 3 — Generate the document set

Produce these five documents (templates in `references/`). Always produce all five unless the user asks for a subset.

1. **`[ORCHESTRATOR]-READ-THIS-FIRST.md`** — one-page cold-start brief the orchestrator reads first. Identity, businesses, Slack map, work-flow, top rules, first move. See `references/read-this-first-template.md`.
2. **`HARNESS-ARCHITECTURE.md`** — the full blueprint: philosophy, tier structure, orchestrator responsibilities, presence model, profile schema, model matrix, context rules, routing decision tree, task-brief format, channel architecture, completion-report format, memory architecture, workflow templates, monitoring, implementation checklist. See `references/architecture-template.md`.
3. **`AGENT-PROFILES.md`** — one structured profile per agent (the orchestrator's routing bible), plus a by-domain quick-routing table and a project summary. See `references/agent-profiles-template.md`.
4. **`[ORCHESTRATOR]-SYSTEM-PROMPT.md`** — the orchestrator's actual system prompt: identity, presence model, team roster, routing rules, task-brief format, completion-report format, memory management, escalation rules, comms style, daily rhythm, "what you don't do." See `references/system-prompt-template.md`.
5. **`IMPLEMENTATION-GUIDE.md`** — phased step-by-step build instructions with real shell commands, file locations, common problems, and a maintenance checklist. See `references/implementation-guide-template.md`.

### Step 4 — Apply the key invariants

Bake these into every harness unless the user overrides them:

- **Cheapest viable model.** The orchestrator always uses the cheapest model that can do the job; escalate up only when needed.
- **Hard memory limits.** Orchestrator ~15,000 chars; Tier 1 ~8,000; Tier 2/3 ~4,000. Archive overflow monthly to `MEMORY-ARCHIVE.md`. (Oversized memory files are the #1 real-world failure — call it out.)
- **Structured task briefs.** Every dispatch uses a fixed brief format (task id, assignee, priority, domain, instruction, output format, constraints, context files, success criteria, report-to channel).
- **Completion reports, not channel monitoring.** Every agent posts a fixed-format report to a single `#completions` channel; the orchestrator reads that, not raw threads.
- **Never inject raw logs.** Context is trimmed and relevant only — never full memory files, never raw conversation history, never other agents' private memory.
- **Escalation rules.** Fail twice → escalate. Cost over a threshold → escalate. Legal/financial/client-sensitive → escalate to the human.

### Step 5 — Present for handoff

Save all five files to the output directory and present them. Give the user the three-line handoff instruction: (1) drop files in the orchestrator's workspace, (2) paste the system-prompt file into the orchestrator's config, (3) tell the orchestrator to read all files and onboard itself.

## Customization notes

- Match the comms layer to the user's tool (Slack/Discord/etc.) — the channel pattern stays the same: one orchestrator command channel, one log channel, one completions channel, one alerts channel, plus per-agent work channels the orchestrator can read but doesn't live in.
- If two agents share a project (e.g. two artists in one corner), they can share a work channel.
- Watch for agents named after real people in the user's life — flag it, don't assume.
- Keep tone matched to the user. Get to the point.
