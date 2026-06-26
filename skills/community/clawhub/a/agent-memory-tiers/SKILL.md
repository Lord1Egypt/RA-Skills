---
name: agent-memory-tiers
version: 1.0.0
description: "Tiered memory system for OpenClaw agents. Gives agents instant context on startup with a 4-line state snapshot (L0) and 7-day rolling context (L1). Eliminates the cold-start problem where agents waste tokens re-reading old files to figure out where they left off. Battle-tested across a 20-agent production swarm. Saves 300-3700 tokens per activation."
metadata:
  openclaw:
    category: "productivity"
    tags: ["memory", "context", "multi-agent", "token-efficiency", "state-management"]
---

# Agent Memory Tiers

> Stop your agents from forgetting everything between runs.

OpenClaw agents start every activation with zero memory of what they did last time. They waste hundreds or thousands of tokens re-reading old files, parsing chat history, and reconstructing context. This skill fixes that.

**Agent Memory Tiers** is a structured, self-updating memory system that gives agents instant context on startup. Two files, updated automatically at the end of every run, so the next activation starts warm.

Tested in production across a 20-agent swarm running daily for 3+ weeks.

## How It Works

Two memory layers sit in each agent's workspace:

| Layer | Purpose | Size | Loaded |
|-------|---------|------|--------|
| **L0** | Instant state snapshot | 4 lines | Every activation |
| **L1** | 7-day rolling context | ~20-40 lines | Every activation |
| **L2+** | Historical memory | Varies | Only when needed |

The agent reads L0 and L1 before doing anything else. Before finishing, it updates both files. Next activation picks up exactly where this one left off.

**Token savings:** 300-3700 tokens per activation depending on agent complexity. Over a week of daily runs, that adds up fast.

## Setup

### Step 1: Create L0.md in your agent's workspace

```markdown
# L0 -- [AGENT_NAME] Quick State

You are [AGENT_NAME]. [One sentence describing role and purpose.]
Current focus: [Top priority right now -- what matters most this week.]
Last run: [Date and one-line summary of last activity, or "No runs yet."]
Flags: [Critical state warnings -- cron status, credit limits, blockers. "None" if clear.]
```

**Example -- a content agent:**

```markdown
# L0 -- WRITER Quick State

You are WRITER. Content engine for the company blog and social accounts.
Current focus: Draft 3 LinkedIn posts promoting the new pricing page.
Last run: 2026-03-15 -- Generated 2 blog teasers and 1 thought leadership post.
Flags: Publishing queue has 8 posts loaded through Mar 22. No blockers.
```

**Example -- a monitoring agent:**

```markdown
# L0 -- WATCHDOG Quick State

You are WATCHDOG. Security monitor for the production environment.
Current focus: Track error rates after the v2.4 deploy.
Last run: 2026-03-16 -- Scanned logs, no anomalies. Alert threshold at 2% error rate.
Flags: Grafana dashboard unreachable intermittently. Investigate if persists.
```

### Step 2: Create L1.md in your agent's workspace

```markdown
# L1 -- [AGENT_NAME] Rolling Context

## Last 7 Days
- YYYY-MM-DD: One-line summary of activity or state change.
- YYYY-MM-DD: Another entry.
(Keep exactly 7 most recent. Drop oldest when adding new.)

## Active Tasks (Top 3)
1. Task description -- additional context, owner if relevant.
2. Second priority task.
3. Third priority task.

## Key State
- Important file paths, tracker values, config state.
- Anything that changed recently.
- Numbers the agent needs to know (queue sizes, deadlines, etc.).

## Blockers
- What is preventing progress. Root cause, not symptom.
- Remove resolved blockers. Add new ones.
- "None" if clear.
```

**Example -- a lead generation agent:**

```markdown
# L1 -- SCOUT Rolling Context

## Last 7 Days
- 2026-03-16: Scanned LinkedIn for AI consulting leads. Found 4 warm prospects.
- 2026-03-15: Researched 3 companies posting AI job listings. Added to LEADS.md.
- 2026-03-14: First hunt run. Established search criteria and baseline.

## Active Tasks (Top 3)
1. Find 5 qualified leads per week -- businesses publicly struggling with AI adoption.
2. Score leads by budget signals (hiring, funding rounds, public complaints).
3. Pass top leads to PITCH agent for proposal drafting.

## Key State
- LEADS.md: 7 prospects, 2 qualified, 0 contacted.
- Search channels: LinkedIn, Twitter, Hacker News, industry forums.
- Services offered: $2k-$6k setup + $500-$2k/month management.

## Blockers
- None.
```

### Step 3: Add the Quick Context header to your SOUL.md

Paste this at the top of your agent's SOUL.md file, right after the role description:

```markdown
## Quick Context (read these FIRST, before anything else)
1. Read \`L0.md\` -- your current state in 4 lines.
2. Read \`L1.md\` -- your last 7 days, active tasks, and blockers.
3. Only read files from \`memory/\` if your current task requires older history.
4. Before finishing: update L0.md and L1.md (see End-of-Run section at bottom).
```

### Step 4: Add the End-of-Run footer to your SOUL.md

Paste this at the bottom of your agent's SOUL.md file:

```markdown
## End-of-Run Memory Update (MANDATORY -- do this before finishing every activation)

1. **Update L0.md** with exactly 4 lines:
   - Line 1: One-sentence identity reminder.
   - Line 2: Current top priority (what matters most RIGHT NOW after this run).
   - Line 3: What you just did this run (date + one line).
   - Line 4: State flags (cron status, credit warnings, blockers, or "None").

2. **Update L1.md:**
   - Add today's date + one-line summary to "Last 7 Days" (keep only 7 most recent entries -- drop the oldest).
   - Update "Active Tasks" with current top 3 after this run.
   - Update "Key State" with any changed numbers, files, or dates.
   - Update "Blockers" -- remove resolved ones, add new ones.
```

## Why This Structure

**L0 is for speed.** Four lines. The agent reads it in under 50 tokens and immediately knows: who am I, what should I focus on, what did I do last, and is anything broken. No digging through files.

**L1 is for context.** Seven days of history, three active tasks, key numbers, and blockers. Enough to make informed decisions without loading the full memory archive. Stays under 200 tokens for most agents.

**L2+ is on-demand.** Historical memory files in a \`memory/\` folder. Only loaded when the task explicitly requires older context. This keeps routine activations fast and cheap.

**Self-updating is critical.** The agent writes its own L0/L1 before finishing. No external process needed. No sync scripts. The agent that did the work is the one that records what happened.

## Multi-Agent Coordination

When running multiple agents, any orchestrator agent can read another agent's L0.md to get instant status without interrupting it or parsing logs.

```markdown
## Orchestrator Pattern

Before assigning a task to another agent:
1. Read their L0.md to check current focus and flags.
2. Read their L1.md "Blockers" section to confirm they are not stuck.
3. If blocked, route the task to a backup agent or flag for human review.
```

This eliminates the "is this agent available?" guessing game and prevents task collisions in multi-agent setups.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| L0 grows beyond 4 lines | Ruthlessly compress. If it does not fit in 4 lines, it belongs in L1. |
| L1 "Last 7 Days" keeps growing | Hard cap at 7 entries. Drop the oldest every time you add a new one. |
| Agent skips the end-of-run update | Put "MANDATORY" in the SOUL.md footer. Bold it. Agents follow strong directives. |
| L1 blockers pile up | Remove blockers the moment they are resolved. Stale blockers cause confusion. |
| Storing detailed logs in L1 | L1 is summaries only. One line per day. Details go in dedicated log files. |
| Using relative dates ("yesterday") | Always use absolute dates (YYYY-MM-DD). The agent does not know when it last ran. |

## Error Handling

**Agent does not read L0/L1 on startup:**
The "Quick Context" header in SOUL.md must be near the top. If it is buried below other instructions, the agent may skip it. Move it directly after the role description.

**Agent overwrites L0/L1 with garbage:**
This usually means the SOUL.md footer instructions are too vague. Use the exact template above with explicit line counts and section names. Agents follow precise structure better than general guidance.

**L1 file grows too large (over 50 lines):**
Your "Key State" section is probably accumulating instead of updating. Each run should replace old state values, not append. Restructure: state is current values, not a changelog.

**Multiple agents writing to the same L0/L1:**
Each agent must have its own L0.md and L1.md in its own workspace. Never share these files between agents. The orchestrator reads them, but only the owning agent writes them.

## Permissions

This skill requires:
- **File read/write** in the agent's workspace directory -- to read and update L0.md and L1.md.
- No network access required.
- No external API access required.
- No sensitive data access required.

## Credits

Built and battle-tested by the Megaport swarm team. Inspired by the OpenViking tiered memory architecture.

## License

MIT -- use it, modify it, share it.