---
name: brief-master
description: "Write precise execution briefs for agents, cron jobs, reviewers, researchers, and delegated coding tasks."
metadata:
  version: "0.2.1"
---
# Brief Master

Write agent briefs that agents actually execute correctly.

Every wasted token is a wasted API call. Every vague word is a future bug. Every missing acceptance criterion is a future rework cycle.

Read `references/9-dimensions.md` before extracting intent.
Read `references/brief-formats.md` for the right format per agent type.


## Safety Boundary

This skill writes briefs only. A generated brief can instruct another agent to edit code, run commands, schedule jobs, or use external services, so the user or orchestrator must review the final brief before execution.

Do not invent credentials, secret names, hostnames, destructive commands, cron schedules, repository permissions, or approval status. If a brief would require elevated access, remote execution, persistent automation, or public posting, mark that as requiring explicit approval in the brief.

## The Pipeline

1. **Detect the target** — which agent, what runtime (subagent, cron, sessions_spawn)?
2. **Extract 9 dimensions** — see `references/9-dimensions.md`
3. **Ask max 3 questions** — only if critical info is missing. Never more.
4. **Apply the right format** — see `references/brief-formats.md`
5. **Run token efficiency audit** — strip every word that doesn't change the output
6. **Deliver** — one clean brief, ready to use

## Token Efficiency Rule

"The best brief is not the longest. It's the one where every word is load-bearing."

Before delivering, ask: does removing this sentence change what the agent does? If not, cut it.

## What Makes a Bad Brief

- Vague task description ("improve the translation")
- No acceptance criteria (how does the agent know it's done?)
- Missing constraints (what must not break?)
- No non-goals (what's explicitly out of scope?)
- Too long (agent loses focus, context drifts)
- Tool-specific instructions missing (which host? which directory? which branch?)

## What Makes a Good Brief

- One clear task per brief
- Explicit ACs labelled AC1, AC2, AC3 (testable, not descriptions)
- Constraints listed
- Non-goals listed
- Correct status update blocks (start + end)
- 95% confidence gate instruction included
- Right tool commands with correct paths

## Mandatory Sections for Dev Agent Briefs

Every brief for a dev/build agent must include:

```
FIRST — update status to working with task description
...task...
LAST — update status to done + notify orchestrator
```

And the 95% confidence gate:
```
Before starting ANY work, ask clarifying questions until you are 95% confident
you can complete this task successfully. Do not start until you have that confidence.
```

See `references/brief-formats.md` for full templates.
