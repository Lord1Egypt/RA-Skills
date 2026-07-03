<!-- TEMPLATE — This is a worked example from a real 29-agent build (Decade Strategy Inc / Tori as CTO).
     Use it as the structure and pattern to follow. Replace all names, roles, businesses, models,
     and channels with the current user's. Keep the section structure, the invariants (memory limits,
     task-brief format, completion-report format, cheapest-viable-model rule), and the overall shape. -->

# OpenClaw Agent Harness Architecture
### Decade Strategy Inc — 24-Agent Orchestration System
**Version 1.1 | Tori as CTO Orchestrator**

---

## Core Philosophy

Tori is the brain. Everyone else is a hand.

Tori doesn't do the work — Tori decides who does the work, with what context, using what model, and monitors the result. Every other agent is a specialist that receives a scoped task, executes, and reports back.

**Tori is not in every Slack channel. Tori is informed by every agent.**
The difference is everything. Raw channel firehose = context bloat = degraded performance.
Agents filter the noise. Only signal reaches Tori.

---

## Tier Structure

```
TIER 0 — ORCHESTRATOR
  └── Tori (CTO) — routes, delegates, monitors, synthesizes

TIER 1 — SENIOR SPECIALISTS (complex, multi-step tasks)
  └── Amadeus, Edison, Connie, Rico, Monica, [others]

TIER 2 — DOMAIN WORKERS (focused, repeatable tasks)
  └── Goober, Finance, Ops, Research, HR, Client, Dev, [others]

TIER 3 — UTILITY AGENTS (single-function, fast, cheap)
  └── Summarizer, Formatter, Validator, Notifier, [others]
```

---

## Tori's Orchestration Responsibilities

| Function | Description |
|---|---|
| **Task Intake** | Receives requests from Paul in #tori-command, classifies by domain/complexity |
| **Agent Selection** | Routes to best-fit agent based on skill tags |
| **Context Packaging** | Injects only relevant memory/context into each agent call |
| **Model Assignment** | Assigns model tier based on task complexity and cost |
| **Result Synthesis** | Aggregates multi-agent outputs into coherent deliverables |
| **Error Handling** | Detects failures, retries or re-routes, escalates to Paul |
| **Memory Management** | Writes outcomes to MEMORY.md; reads agent completion reports |
| **Awareness** | Stays informed via structured agent reports — NOT raw channel monitoring |

---

## Tori's Slack Presence Model

Tori is NOT in every channel. Here's exactly where she lives and how she stays informed:

```
TORI IS ACTIVE IN:
  #tori-command       ← Paul talks to Tori here. This is her office.
  #tori-log           ← Her own audit trail (she writes here, read-only for humans)
  #completions        ← Every agent posts structured completion reports here
  #alerts             ← System errors, failures, escalations

TORI HAS READ ACCESS TO (passive, on-demand):
  All #[agent]-work channels   ← She can pull context when needed, not monitoring live

TORI IS NOT IN:
  Individual agent work channels (agents work there, not Tori)
  Queue channels (ops-queue, dev-queue — agents self-serve these)
```

### How Tori Stays Informed Without Being Everywhere

Every agent posts a structured completion report to #completions when a task finishes:

```
✅ TASK COMPLETE
Task ID: task-2026-042
Agent: Amadeus
Requested by: Paul (via Tori)
Domain: marketing / soup-club
Summary: Drafted May menu announcement email (287 words, warm/casual tone)
Output: Posted in #amadeus-work thread [link]
Status: Ready for Paul review
Time: 14 min
```

Tori reads #completions and synthesizes. She never needs the raw thread.

---

## Agent Profile Schema

Every agent in your system should have a defined profile. This is Tori's routing bible.

```json5
{
  "id": "amadeus",
  "name": "Amadeus",
  "tier": 1,
  "role": "Creative Director / Brand Strategist",
  "skills": ["copywriting", "brand-voice", "campaign-strategy", "naming"],
  "domains": ["marketing", "communications", "soup-club", "rmda"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["deepseek/deepseek-chat", "anthropic/claude-sonnet-4-6"]
  },
  "memory": {
    "shared": ["brand-guidelines", "client-roster"],
    "private": "amadeus/MEMORY.md",
    "maxChars": 8000
  },
  "slack": {
    "provider": "amadeus",
    "workChannel": "#amadeus-work",
    "reportsTo": "#completions"
  },
  "costTier": "medium"
}
```

---

## Model Assignment Matrix

| Task Type | Complexity | Recommended Model | Cost Tier |
|---|---|---|---|
| Simple lookup, formatting, summarization | Low | deepseek/deepseek-v4-flash | $ |
| Analysis, drafting, multi-step reasoning | Medium | deepseek/deepseek-v4-pro | $$ |
| Architecture, strategy, complex orchestration | High | anthropic/claude-sonnet-4-6 | $$$ |
| Critical/sensitive decisions | Critical | anthropic/claude-opus | $$$$ |

**Rule:** Tori uses the cheapest model that can do the job. Escalate up only when needed.

---

## Context Packaging Rules

This is the most important part. Wrong context = bad outputs + high costs.

### What Tori injects per agent call:
```
1. Agent's own MEMORY.md (trimmed to relevant sections, max 8000 chars)
2. Shared domain context (e.g. brand guidelines if marketing task)
3. Task brief (what to do, what format, what success looks like)
4. Relevant prior outputs (only if the agent needs them)
5. Constraints (word limits, tone, deadlines, output format)
```

### What Tori NEVER injects:
- Full MEMORY.md files
- Raw Slack conversation logs
- Other agents' private memory
- Unrelated project context
- Full channel histories

### MEMORY.md Size Rules:
- Tori's MEMORY.md: max 15,000 chars
- Tier 1 agents: max 8,000 chars
- Tier 2/3 agents: max 4,000 chars
- Archive old entries to `MEMORY-ARCHIVE.md` monthly

---

## Task Routing Logic (Tori's Decision Tree)

```
Incoming Task (from Paul in #tori-command)
    │
    ├── Classify domain: [ops / marketing / dev / finance / hr / research / client]
    │
    ├── Classify complexity: [simple / moderate / complex / strategic]
    │
    ├── Is it multi-domain?
    │       ├── YES → spawn multiple agents, synthesize results
    │       └── NO  → route to single best-fit agent
    │
    ├── Select agent by skill tags
    │
    ├── Assign model tier based on complexity matrix
    │
    ├── Package context (trim to relevant only)
    │
    ├── Dispatch task with structured brief
    │
    └── Monitor #completions → receive report → validate → deliver to Paul or escalate
```

---

## Structured Task Brief Format

When Tori dispatches to any agent:

```
TASK BRIEF
----------
Task ID: [auto-generate]
Assigned To: [agent name]
Priority: [low / normal / high / urgent]
Domain: [domain]
Instruction: [clear, specific, one paragraph max]
Output Format: [exactly what you want back]
Word/Length Limit: [if applicable]
Tone/Voice: [if applicable]
Context Files: [list only what's needed]
Success Criteria: [how you'll know it's done right]
Report To: #completions
Deadline: [if applicable]
```

---

## Slack Channel Architecture

```
TORI'S CHANNELS (Tori is active here)
  #tori-command       — Paul ↔ Tori. All requests start here.
  #tori-log           — Tori's decision audit trail (auto-written)
  #completions        — All agent completion reports (Tori reads this)
  #alerts             — Failures, errors, escalations

AGENT WORK CHANNELS (agents work here, Tori has read access only)
  #amadeus-work
  #edison-work
  #connie-work
  #rico-work
  #monica-work
  #goober-work
  #[agent]-work       — one per agent

QUEUE CHANNELS (agents self-serve)
  #ops-queue          — Incoming ops tasks
  #dev-queue          — Dev tasks
  #research-queue     — Research requests
```

---

## Completion Report Format (All Agents Use This)

Every agent posts this to #completions when a task is done. This is how Tori stays informed without being everywhere.

```
✅ TASK COMPLETE  [or]  ❌ TASK FAILED  [or]  ⚠️ ESCALATING TO TORI

Task ID: [id]
Agent: [name]
Requested by: [paul / tori / agent-name]
Domain: [domain]
Summary: [1-2 sentences — what was done]
Output: [where to find it — channel link, file, or inline]
Status: [ready-for-review / delivered / blocked / failed]
Time taken: [X min]
Notes: [anything Tori needs to know]
```

---

## Memory Architecture

```
~/.openclaw/
├── memory/
│   ├── shared/
│   │   ├── brand-guidelines.md        # All agents can read (max 3k chars)
│   │   ├── client-roster.md           # All agents can read (max 3k chars)
│   │   ├── product-catalog.md         # All agents can read (max 3k chars)
│   │   └── company-context.md         # All agents can read (max 3k chars)
│   ├── tori/
│   │   ├── MEMORY.md                  # Tori's working memory (max 15k)
│   │   └── MEMORY-ARCHIVE.md          # Rolled-off entries
│   ├── amadeus/
│   │   └── MEMORY.md                  # (max 8k)
│   ├── edison/
│   │   └── MEMORY.md
│   ├── connie/
│   │   └── MEMORY.md
│   └── [agent]/
│       └── MEMORY.md
```

---

## Workflow Templates

### Template 1: Single-Agent Task
```
Paul (#tori-command) → Tori → [classify] → [dispatch brief] → Agent → #completions → Tori → Paul
```

### Template 2: Multi-Agent Pipeline
```
Paul → Tori → Agent A (research) → #completions
                    ↓
              Agent B (draft) → #completions
                    ↓
              Agent C (review) → #completions
                    ↓
              Tori (synthesize) → Paul
```

### Template 3: Parallel Dispatch
```
Paul → Tori → Agent A ─┐
              Agent B ──┼→ all post to #completions → Tori merges → Paul
              Agent C ─┘
```

### Template 4: Autonomous Cron Workflow
```
Cron trigger → Tori → [run workflow] → #completions → #tori-log
```

---

## Health & Monitoring Rules

- Every agent posts completion report to #completions — no exceptions
- Tori posts daily digest to #tori-log at end of day
- Failed tasks: agent escalates via #completions with ❌, Tori retries once, then escalates to Paul in #tori-command
- MEMORY.md files audited weekly — anything over limit gets trimmed
- Model fallback events logged monthly (watch DeepSeek billing)

---

## Implementation Checklist

### Phase 1 — Foundation
- [ ] Trim Tori's MEMORY.md to under 15,000 chars (currently 85k — do this first)
- [ ] Create `~/.openclaw/memory/shared/` and populate 4 shared docs
- [ ] Create MEMORY.md for each agent, trim to limits
- [ ] Set up Slack channel structure above
- [ ] Confirm all 8 Slack providers connect cleanly

### Phase 2 — Agent Profiles & Tori's Brain
- [ ] Fill in AGENT-PROFILES.md for all 24 agents
- [ ] Update TORI-SYSTEM-PROMPT.md with all agent roles
- [ ] Load updated system prompt into Tori's openclaw config
- [ ] Test: send Tori a task, confirm she routes correctly

### Phase 3 — Completion Reporting
- [ ] Add completion report instruction to every agent's system prompt
- [ ] Confirm agents post to #completions in correct format
- [ ] Test multi-agent pipeline end to end

### Phase 4 — Automation
- [ ] Configure cron workflows for recurring tasks
- [ ] Set up #alerts for system errors
- [ ] Build MEMORY.md auto-trim script
- [ ] Monthly maintenance schedule

---

*Built for Decade Strategy Inc — OpenClaw 2026 v1.1 | Tori as CTO Orchestrator*
