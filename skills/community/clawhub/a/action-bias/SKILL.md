---
name: action-bias
description: "Stop agents from producing reports instead of taking action. Restructure prompts, cron jobs, and agent shifts so they DO things — send emails, post content, make API calls, push code — instead of writing plans about doing things. Use when: agents keep outputting strategy docs instead of executing, sub-agent sessions produce reports nobody reads, you notice your crew is busy but nothing external is happening, heartbeat/shift results are all 'here's what we should do' with no proof of doing it, or you want to audit whether your agents are actually shipping."
---

# Action Bias — Make Agents Do, Not Plan

Agents default to planning. They'll write beautiful strategy docs, propose campaigns, outline approaches, and suggest next steps — all while producing zero external output. This skill fixes that.

## The Core Problem

AI agents are trained on text that describes work, not text that does work. Left unconstrained, they'll:
- Write "I recommend we post on Reddit" instead of posting on Reddit
- Produce a "Social Media Strategy 2026" doc instead of tweeting
- "Research competitors" for 10 minutes and output a report instead of using findings to take action
- Say "we should follow up with leads" instead of sending the email

The result: agents that feel productive while nothing actually ships.

## The Fix: Three Rules

### Rule 1: Mandate External Output

Every agent session must produce at least one **externally visible action**. Internal files don't count.

**External actions** (things that leave your system):
- Sending an email
- Posting on social media
- Pushing code to a repo
- Submitting to a directory
- Making an API call that creates something
- Publishing content

**Not external actions** (internal busywork):
- Writing a report to a local file
- Updating a strategy doc
- Creating a plan
- "Researching" without acting on findings

### Rule 2: Require Proof of Action

Agents must log **evidence** of every external action: URLs, post IDs, email addresses contacted, API response codes. "I posted on Reddit" without a URL is the same as not posting.

### Rule 3: Make Reports a Side Effect, Not the Goal

Research is fine — but only as input to an action. "Research competitors and tweet an insight" forces the research to serve a purpose. "Research competitors and write a report" lets the agent stop after the comfortable part.

## Prompt Patterns

### The Action-First Prompt (use this)

```
[ROLE] SHIFT — OUTBOUND ACTIONS REQUIRED

You MUST produce at least [N] outbound actions this session. Reports alone = failure.

## Required Actions (pick [N]+):

1. **[Verb] [thing]** — [How to do it with specific tool/command]
   [1-line context on what good looks like]

2. **[Verb] [thing]** — [How to do it with specific tool/command]
   [1-line context on what good looks like]

## Context (optional):
[Background the agent needs to take good action]

## Log:
Append ALL actions taken (with URLs/IDs/proof) to [log file]

DO NOT write strategy proposals. DO things.
```

### The Report-First Anti-Pattern (stop doing this)

```
# ❌ BAD — produces reports, not results

MARKETING SHIFT: Analyze our current channels. Identify
opportunities for improvement. Write a report with recommendations
for next quarter. Save to memory/marketing-report.md.

# ✅ GOOD — same intent, forces action

MARKETING SHIFT — OUTBOUND ACTIONS REQUIRED

You MUST complete at least 2 outbound actions. Reports alone = failure.

## Required Actions (pick 2+):

1. **Post on social media** — [exact tool/command to post]
   Write something useful about [your domain]. Not promotional.

2. **Engage in 3 community threads** — Find active discussions
   where people ask about [your topic]. Add genuine value.

3. **Send 2 outreach emails** — [exact tool/command to send]
   Lead with insight about THEIR business. Under 80 words.

## Log:
Append actions with URLs/proof to [your action log file]
```

### Key Differences

| Report-First (❌) | Action-First (✅) |
|---|---|
| "Analyze and recommend" | "Do X, then log it" |
| "Write a report" | "Post/send/submit, then write what you did" |
| "Identify opportunities" | "Find 3 threads and reply to them" |
| "Research competitors" | "Research competitors and tweet one finding" |
| Output: strategy doc | Output: URLs, post IDs, sent emails |
| Feels productive | Is productive |

## Restructuring Existing Shifts

If you have agents running on cron/heartbeat that produce reports, restructure them. See `references/shift-restructuring.md` for the full pattern.

Quick checklist:
1. Read each shift's current prompt
2. Find every verb that means "think about" (analyze, research, identify, recommend, propose, assess, evaluate, review)
3. Pair each with an action verb (post, send, submit, push, create, reply, engage)
4. Add "OUTBOUND ACTIONS REQUIRED" header and minimum action count
5. Add logging requirement with proof (URLs, IDs)
6. Add "Reports alone = failure" as explicit guardrail

## Auditing Action Output

Periodically check whether agents are actually acting. See `references/action-audit.md` for:
- How to score agent sessions on action vs report ratio
- Red flags that indicate planning drift
- A simple audit script pattern
- When reports ARE appropriate (rare, but real)

## When Reports Are Actually Fine

Not everything needs an external action. Reports are appropriate for:
- **Ops/security shifts** — checking system health IS the action
- **Analyst reviews** — synthesizing data for human decision-making
- **Audit sessions** — evaluating quality of past work
- **Planning sessions** — when explicitly requested by a human

The test: "Would a human manager be satisfied with this output, or would they ask 'okay, but what did you actually DO?'"

## Common Failure Modes

| Symptom | Cause | Fix |
|---|---|---|
| Agent writes "I recommend posting on X" | No tool/command provided | Include exact command in prompt |
| Agent researches but doesn't act | Research is the whole task | Make research serve an action |
| Agent logs "posted to Reddit" with no URL | No proof requirement | Require URLs/IDs for every action |
| Agent does 1 action then writes 500 words of analysis | No minimum action count | Set minimum (e.g., "at least 2 actions") |
| Agent says "I'll do this next time" | Planning language leak | Add "DO NOT PLAN. EXECUTE." |
| Agent produces beautiful strategy doc | Prompt rewards thinking over doing | Restructure prompt per patterns above |
