---
name: agent-memory-tiers-pro
version: 1.0.0
description: "Production-grade agent memory and quality system for multi-agent swarms. Extends agent-memory-tiers with an 8-point quality grading rubric, progressive disclosure for token efficiency, orchestrator coordination patterns, self-improvement protocols, and agent scoring templates. Built from 3+ weeks running a 20-agent production swarm."
metadata:
  openclaw:
    category: "productivity"
    tags: ["memory", "multi-agent", "swarm", "quality", "governance", "token-efficiency", "orchestration", "production"]
    requires:
      skills: ["agent-memory-tiers"]
---

# Agent Memory Tiers Pro

> Turn a collection of agents into a production-grade swarm.

The free **agent-memory-tiers** skill gives your agents memory. This skill gives your swarm structure, quality standards, and self-improvement. It is the difference between "I have some agents running" and "I have a system that gets better over time."

Built from running a 20-agent swarm in production daily for 3+ weeks. Every pattern here solved a real problem.

**Requires:** [agent-memory-tiers](https://clawhub.ai/skills/agent-memory-tiers) installed and configured first.

## What This Adds

| Component | What It Does |
|-----------|-------------|
| **Quality Grading Rubric** | Score any agent's SOUL.md on 8 criteria. Identify weak spots before they cause failures. |
| **Progressive Disclosure** | 3-tier token loading system. Agents only read what they need, when they need it. |
| **Orchestrator Protocol** | Patterns for a coordinator agent to manage the whole swarm efficiently. |
| **Self-Improvement Loop** | Agents log mistakes and proven approaches. The swarm learns from itself. |
| **Agent Scoring Template** | Evaluate and compare agents objectively. Know which ones need work. |

---

## 1. The 8-Point Quality Grading Rubric

Every agent SOUL.md should be scored on these 8 criteria. Use the rubric when building new agents or auditing existing ones.

```markdown
## Agent Quality Rubric

| # | Criterion | A (Top Tier) | C (Functional) | F (Broken) |
|---|-----------|-------------|----------------|-----------|
| 1 | Role Clarity | One sentence, crystal clear, no ambiguity | Vague or tries to do multiple jobs | Missing or contradictory |
| 2 | Activation Triggers | Explicit triggers + exclusion conditions | Partial triggers, some guessing | No triggers defined |
| 3 | Step-by-Step Workflow | Numbered steps with file paths and tool names | General guidance, some gaps | "Figure it out" |
| 4 | Output Format | Exact template with field names and structure | Loose format guidance | No format specified |
| 5 | Quality Checklist | Pre-completion validation steps | Partial checks | None |
| 6 | Error Handling | Common failures listed with specific fixes | Some error awareness | None |
| 7 | Boundaries | Explicit CAN and CANNOT lists | Partial limits | Vague or missing |
| 8 | Token Efficiency | Under 300 lines, references externalized | Under 500 lines | Over 500 or bloated with inline data |
```

**Targets:**
- Score A on criteria 1, 2, 4, and 7 (non-negotiable for production agents).
- No F on any criterion.
- Review and re-score every agent monthly.

### How to Score an Agent

Read the agent's SOUL.md top to bottom. For each criterion, assign A/C/F based on the rubric. Record the scores.

```markdown
## Agent Scorecard: [AGENT_NAME]

Date: YYYY-MM-DD
Scored by: [human or auditor agent name]

| Criterion | Score | Notes |
|-----------|-------|-------|
| Role Clarity | A | "Security monitor for production." Clear. |
| Activation Triggers | C | Lists triggers but no exclusion conditions. |
| Workflow | A | 12 numbered steps with file paths. |
| Output Format | A | JSON template with required fields. |
| Quality Checklist | C | 2 checks, should have 4-5. |
| Error Handling | F | No failure scenarios listed. |
| Boundaries | A | CAN: scan logs, alert. CANNOT: restart services, modify configs. |
| Token Efficiency | A | 240 lines, refs externalized. |

**Overall: 5A / 2C / 1F — Priority fix: add error handling.**
```

### Fixing Common Score Failures

**Role Clarity F → A:**

```markdown
# BAD (F):
You help with various tasks related to content and social media and marketing.

# GOOD (A):
You are WRITER. You draft social media posts for 4 accounts (2 LinkedIn, 2 X).
You do NOT publish, schedule, or manage engagement. You only write drafts.
```

**Error Handling F → A:**

```markdown
# BAD (F):
(nothing — agent has no idea what to do when things break)

# GOOD (A):
## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| "File not found: LEADS.md" | First run, file does not exist yet | Create LEADS.md with header template, then continue |
| "API rate limit reached" | Too many requests this session | Stop current task, update L0 flags: "Rate limited — retry next activation" |
| "Output exceeds 20,000 chars" | Response too large for workspace file | Split into multiple files: output-part1.md, output-part2.md |
| "Tool call failed: web_search" | Network issue or API key expired | Skip web search, use cached data from last run, flag in L1 blockers |
```

**Boundaries F → A:**

```markdown
# BAD (F):
Be careful and don't do anything dangerous.

# GOOD (A):
## Boundaries

**CAN:**
- Read and write files in own workspace
- Search the web for public information
- Draft content for human review

**CANNOT:**
- Post, publish, or send anything externally (all output goes to approval queue)
- Access other agents' workspaces (read their L0 only via orchestrator)
- Install packages, modify system config, or run shell commands
- Spend money or commit to deadlines on behalf of the user
```

---

## 2. Progressive Disclosure (Token Efficiency System)

Not every activation needs the full SOUL.md. Load information in tiers to minimize token cost.

```markdown
## Progressive Disclosure Tiers

| Tier | What Loads | When | Token Cost |
|------|-----------|------|------------|
| T1: Identity | L0.md (4 lines) + role sentence from SOUL.md | Every activation | ~50-100 tokens |
| T2: Context | L1.md (rolling 7-day state) | Every activation | ~100-200 tokens |
| T3: Full Instructions | Complete SOUL.md | When agent activates on a matching trigger | Full SOUL.md cost |
| T4: References | External docs from references/ folder | Only when task explicitly needs them | On demand |

## Rules:
- SOUL.md must stay under 500 lines. If it exceeds this, externalize reference material.
- Large data files (logs, queues, trackers) go in workspace, NOT in SOUL.md.
- Tables and templates are more token-efficient than prose. Prefer structured formats.
- If a section of SOUL.md is only used for 1 out of 10 activations, move it to references/.
```

### SOUL.md Size Budgets

```markdown
## SOUL.md Section Budget

| Section | Max Lines | Purpose |
|---------|-----------|---------|
| Role + Identity | 5 | Who am I, one sentence purpose |
| Quick Context (L0/L1 loader) | 5 | Pointer to memory files |
| Activation Triggers | 10 | When to wake up, when NOT to |
| Core Workflow | 60-80 | Numbered steps for primary tasks |
| Output Templates | 40-60 | Exact format for deliverables |
| Quality Checklist | 10-15 | Pre-completion validation |
| Error Handling | 15-20 | Failure table |
| Boundaries | 10-15 | CAN/CANNOT lists |
| End-of-Run (L0/L1 update) | 15 | Memory update mandate |
| **TOTAL** | **~200-300** | **Target range for production agents** |
```

### Externalizing References

When SOUL.md gets too large, move supporting material to separate files.

```markdown
## Reference Externalization Pattern

In SOUL.md, replace large sections with pointers:

  For detailed style guidelines, read `references/STYLE_GUIDE.md`.
  For the full client list and history, read `references/CLIENTS.md`.
  For API endpoint documentation, read `references/API_DOCS.md`.

Rules:
- Agent reads reference files ONLY when the current task needs them.
- Never inline reference content back into SOUL.md.
- Reference files have no size limit but should be focused (one topic per file).
- Update references independently of SOUL.md — they are living documents.
```

---

## 3. Orchestrator Coordination Protocol

When one agent (the orchestrator) manages a swarm of specialist agents, use these patterns.

### Swarm Status Check

```markdown
## Orchestrator: Morning Status Check

1. Read L0.md for every agent in the swarm.
2. Build a status table:

| Agent | Focus | Last Active | Flags |
|-------|-------|-------------|-------|
| WRITER | Draft LinkedIn posts | 2026-03-16 | None |
| SCOUT | Find 5 leads this week | 2026-03-16 | None |
| WATCHDOG | Monitor v2.4 deploy | 2026-03-15 | Grafana intermittent |

3. Flag any agent with:
   - Last active > 48 hours ago (may be stuck or disabled)
   - Non-empty flags (needs attention)
   - Focus misaligned with current priorities

4. Present status brief to human operator. Do NOT auto-reassign tasks.
```

### Task Routing

```markdown
## Orchestrator: Task Routing Protocol

When a new task arrives:

1. Identify which agent's role matches the task.
2. Read that agent's L0.md — check flags for blockers.
3. Read that agent's L1.md "Blockers" section — confirm agent is not stuck.
4. If agent is clear:
   - Route the task with a structured brief: WHAT (task), WHY (context), DEADLINE (if any), OUTPUT (expected deliverable format).
5. If agent is blocked:
   - Check if a backup agent can handle it.
   - If no backup, escalate to human operator with: blocked agent name, blocker description, suggested fix.
6. Never route a task to an agent whose L0 flags indicate it cannot execute right now.
```

### Cross-Agent Handoffs

```markdown
## Orchestrator: Handoff Protocol

When Agent A's output feeds into Agent B's input:

1. Agent A completes its task and writes output to a shared handoff file:
   `workspace/handoffs/[AGENT_A]-to-[AGENT_B]-YYYY-MM-DD.md`

2. Agent A updates its L0.md line 3: "Handed off [deliverable] to [AGENT_B]."

3. Orchestrator reads Agent A's L0, confirms handoff file exists.

4. Orchestrator triggers Agent B with:
   - Pointer to the handoff file
   - Context: what Agent A produced and why
   - Expected output format

5. Agent B reads the handoff file, executes its task, writes output.

6. Agent B updates its L0.md and L1.md as normal.

Rules:
- Handoff files are write-once. Agent B never modifies Agent A's output.
- Handoff files older than 7 days can be archived to handoffs/archive/.
- If the handoff file is missing or malformed, Agent B stops and flags the orchestrator.
```

---

## 4. Self-Improvement Protocol

The swarm should get better over time. These two files make that happen.

### Lessons File

Create `workspace/lessons.md` in your main workspace. Any agent (or human) can append to it.

```markdown
# Lessons Learned

Format: Date | Category | What Happened | Root Cause | Fix Applied

## Template:
- YYYY-MM-DD | [agent/system/workflow] | [what went wrong] | [why] | [what we changed]

## Examples:
- 2026-03-05 | agent | HERALD used wrong model, task failed | Model ID was invalid for provider | Updated all agents to correct model in config
- 2026-03-08 | workflow | Agent output exceeded file size cap | No size check before write | Added pre-write size validation to SOUL.md workflow
- 2026-03-10 | system | Credentials exposed in config file | Env vars stored in committed file | Moved secrets to .env.local, rotated all keys
- 2026-03-12 | agent | SCOUT searched wrong platforms | Activation trigger too broad | Added exclusion conditions to SOUL.md triggers
```

### Patterns File

Create `workspace/patterns.md` in your main workspace. When something works well, record it.

```markdown
# Proven Patterns

Format: Pattern Name | When to Use | How It Works

## Template:
### [Pattern Name]
**When:** [situation where this applies]
**How:** [step by step]
**Why it works:** [one sentence]

## Example:
### Batch-Then-Review
**When:** Agent needs to produce multiple outputs (posts, reports, emails).
**How:** Generate all items in one run. Write to a review queue file. Human reviews the batch. Approved items move to the action queue.
**Why it works:** One activation for N outputs is cheaper than N activations for N outputs. Batch review is faster for the human too.
```

### Monthly Swarm Audit

```markdown
## Monthly Audit Checklist

Run this on the 1st of every month:

1. Score every agent using the 8-point rubric. Record in scorecards/.
2. Review lessons.md — are the same mistakes repeating? If yes, the fix was insufficient.
3. Review patterns.md — are proven patterns actually being used? If not, add them to SOUL.md workflows.
4. Check L0/L1 freshness — any agent with "Last run" older than 14 days is either unused or broken.
5. Check SOUL.md sizes — any over 400 lines needs externalization.
6. Archive old handoff files (> 7 days) and resolved blockers.
7. Update the orchestrator's agent roster with any new or retired agents.

Output: One-page swarm health report for the human operator.
```

---

## 5. Agent Scoring and Comparison

Use this template to track agent quality over time.

```markdown
## Swarm Scorecard — YYYY-MM

| Agent | Role | Clarity | Triggers | Workflow | Output | Quality | Errors | Bounds | Tokens | Grade |
|-------|------|---------|----------|----------|--------|---------|--------|--------|--------|-------|
| WRITER | Content | A | A | A | A | C | A | A | A | 7A 1C |
| SCOUT | Leads | A | A | C | A | C | C | A | A | 5A 3C |
| WATCHDOG | Security | A | C | A | A | A | F | A | A | 6A 1C 1F |

**Swarm Average:** X.X / 8.0
**Weakest Criterion (swarm-wide):** [identify which criterion has the most C/F scores]
**Priority Fix:** [one action item to raise the weakest area]
```

### Tracking Improvement Over Time

```markdown
## Swarm Quality Trend

| Month | Agents | Avg Score | A% | C% | F% | Top Agent | Needs Work |
|-------|--------|-----------|----|----|----|---------|-----------|
| 2026-03 | 20 | 6.8 | 78% | 18% | 4% | LEDGER | WATCHDOG |
| 2026-04 | 22 | 7.1 | 82% | 16% | 2% | LEDGER | SCOUT |

Target: 85%+ A scores, 0% F scores within 3 months of deployment.
```

---

## Permissions

This skill requires:
- **File read/write** in agent workspace directories — to manage L0.md, L1.md, scorecards, lessons, patterns, and handoff files.
- **File read** across agent workspaces — orchestrator needs to read other agents' L0.md files (read only, never write).
- No network access required.
- No external API access required.
- No sensitive data access required.

## Credits

Built and battle-tested by the Megaport swarm team across a 20-agent production deployment. Quality rubric inspired by Anthropic's skill-building guidelines and the OpenViking tiered memory architecture.

## License

MIT — use it, modify it, share it.
