# Alignment Adjustment — Full Procedure

## Overview

Detect misalignment between what the user wants and how the agent is actually configured. Find contradictions, at-risk instructions that won't survive compaction, manual work that should be automated, and stale instructions nobody follows.

## Step 1: Scan for Instruction Contradictions

Read these files:
1. `core instruction files`
2. `MEMORY.md`
3. `persona files`
4. `user-profile files`
5. `heartbeat schedules`

For each pair, find:

### Contradictions
- Instructions in one file that directly conflict with instructions in another
- Example: core instruction files says "always ask before sending emails" but persona files says "don't ask for confirmation on things I should just handle"
- Example: MEMORY.md records "use Todoist for tasks" but core instruction files says "tasks live in projects/*.md"

### Duplicates
- The same instruction stated in different places in different words
- These create ambiguity: which version is authoritative? What if someone updates one but not the other?
- Example: deploy steps in both core instruction files and MEMORY.md, slightly different

For each finding, quote the exact lines and file paths.

## Step 2: Scan for Chat vs Config Drift

Read the last 7 daily memory files (`memory/YYYY-MM-DD.md`, most recent 7).

### At-Risk Instructions (critical)
Identify things the user said in chat that:
- Establish a rule or preference ("always do X", "never do Y", "from now on...")
- Were recorded in a daily log but NOT in core instruction files, persona files, user-profile files, or MEMORY.md
- Would be lost after context compaction because daily logs aren't always re-read

These are the highest priority findings. An instruction that only lives in a daily log or in conversation history WILL be forgotten after compaction.

### Repeated Requests
Find patterns where:
- The user asks for the same thing more than twice across different sessions
- The user corrects the same behavior more than once
- The user reminds the agent of a rule that should be permanent

If the user is saying "remember to always do X" more than twice, X should be in core instruction files.

## Step 3: Scan for Manual Work That Should Be Automated

### Should Be Scheduled
Review daily logs and heartbeat schedules:
- Tasks the user triggers manually at roughly the same time each day/week
- Tasks with a clear trigger condition that could be a heartbeat job
- Example: "run daily content" every morning at 6AM but no cron, user has to ask

### Should Be a Skill
Find repetitive multi-step requests:
- The user asks for the same sequence of steps across different sessions
- The sequence is 3+ steps and follows the same pattern each time
- Example: "clone repo, make change, deploy, push, update project MD" for every site change

### Should Be a Cron
Find time-based patterns:
- Check daily logs for tasks that appear at regular intervals
- Cross-reference with `crontab -l` output to see if they're already scheduled
- If not scheduled and the pattern is clear, recommend adding to cron

## Step 4: Scan for Stale or Ignored Instructions

### Ignored Instructions
For each directive in core instruction files:
- Search recent daily logs (last 7-14 days) for evidence the instruction is being followed
- If an instruction exists but there's evidence it's being routinely skipped or contradicted in practice, flag it
- Example: core instruction files says "create Paperclip issue for every task" but daily logs show tasks completed without Paperclip entries

### Dead Heartbeat Tasks
For each scheduled task in heartbeat schedules:
- Look for evidence it actually ran (daily logs, spa reports, git commits)
- If a task is listed as scheduled but shows no execution evidence in 14+ days, flag it

### Phantom Skills
For each installed skill:
- Check if it's referenced in core instruction files or any workflow
- Check if it appears in any daily log in the last 30 days
- If installed but never mentioned, never invoked, and not referenced anywhere, flag it

## Step 5: Generate Alignment Report

```
🦴 ALIGNMENT ADJUSTMENT
═══════════════════════════════════════

Contradictions found: X
 - [core instruction files line Y says "...", but MEMORY.md line Z says "..."]
 - [persona files says "...", conflicts with core instruction files "..."]

Duplicates found: X
 - ["..." appears in both core instruction files and MEMORY.md in different wording]
 → Consolidate to one location

At-risk instructions (chat only, won't survive compaction): X
 - ["Always check with me before sending emails" — said in chat on Mar 18, not in any permanent file]
 → Move to core instruction files to make it permanent
 - ["Use German for de/ch country content" — in daily log only]
 → Move to core instruction files or project MD

Should-be-automated: X
 - [You run daily content manually every morning at ~6am → add to crontab or heartbeat schedules]
 - [Same 5-step deploy sequence repeated 3x this week → could be a script or skill]

Stale instructions: X
 - [core instruction files says "use Todoist for tasks" but no Todoist skill installed, no mentions in 30 days]
 - [heartbeat schedules lists "Monday SEO check" but no evidence it ran last 2 Mondays]

═══════════════════════════════════════
```

## Rules

- **Present all findings as suggestions.** Never auto-modify any file.
- **Prioritize at-risk instructions first.** These are the ones that will cause the agent to go rogue after compaction.
- **Be specific.** Quote the exact contradicting lines and which files they're in. Don't say "there's a contradiction somewhere."
- **If nothing is found, say so.** Don't invent problems. A clean alignment check is a good result.
- **Context matters.** Some apparent contradictions are actually scoped differently (e.g., "be concise" in general but "be detailed" for security analysis). Only flag genuine conflicts.
