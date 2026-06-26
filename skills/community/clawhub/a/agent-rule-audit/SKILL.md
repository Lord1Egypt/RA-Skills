---
name: agent-rule-audit
description: Audit an OpenClaw agent's behavior-layer rules and prompt sources to find drift, redundancy, conflict, loss of focus, and weak behavior guidance. Use when reviewing an agent's core behavior files, any behavior-shaping correction/learnings layer that exists in the target workspace, and any explicitly referenced shared rule files; when checking why an agent behaves poorly despite many rules; when deciding which rules should stay core, move out, or be strengthened; and when running an agent self-audit.
---

# Agent Rule Audit

Audit the files that actually shape an OpenClaw agent's behavior. Focus on behavior-layer quality, not general file cleanup.

## Quick start

1. Identify the audit target: which agent/workspace is being reviewed.
2. Read the core behavior-layer files first.
3. Read shared rule files only when the core files explicitly depend on them.
4. Stay with the default core scope first. Widen only when the core files are not enough to explain the behavior, or when the user asks for a deeper audit.
5. Produce two outputs:
   - audit conclusions
   - executable restructuring recommendations
6. Separate root causes from surface symptoms.

## Default audit scope

By default, inspect only the agent's core, stable behavior files — the files most likely to be loaded every session and to consistently shape behavior.

### Core behavior layer
Read these first when present:
- `AGENTS.md`
- `SOUL.md`
- `USER.md`
- `MEMORY.md` (if present)
- `TOOLS.md`
- `IDENTITY.md`
- `HEARTBEAT.md`

See `references/openclaw-behavior-sources.md` for why these matter in OpenClaw.

## Optional widening
Only widen beyond the core set when needed, for example:
- the user explicitly asks for a broader audit
- the core files explicitly depend on another file
- the core files look fine but behavior clearly points to another steering source
- a recent correction/example cannot be explained from the core files alone

Possible widening targets:
- shared rule files explicitly referenced by the core files
- any correction / learnings / workflow-improvement layer that exists in the target workspace
- behavior-improvement or trial-related supporting files when they exist in the target workspace
- recent behavioral evidence files when they exist in the target workspace
- user-provided examples/screenshots/transcripts

## What to look for

Use the problem categories in `references/problem-types.md`.
Default categories:
- structure confusion
- repetition / redundancy
- rule conflict
- focus drift
- behavior-layer dilution from too many weak rules
- symptom-vs-root-cause confusion
- style guidance overpowering execution guidance
- stale or superseded rules not cleaned up
- trial rules that never reached the live behavior layer

## Audit workflow

### 1. Map the real behavior sources
Do not assume every file matters equally.
First answer:
- Which files are most likely shaping behavior now?
- Which are direct behavior rules vs supporting evidence?
- Which are probably ignored or low-weight?

### 2. Identify the user's real complaint
Do not let verbose files distract from the actual failure mode.
Ask or infer:
- What is the user truly unhappy with?
- What is the root problem?
- Which observed symptoms are secondary?

Example: “progress-sounding replies” may be a symptom; “not actually doing the work” may be the root issue.

### 3. Read for layering problems
Check whether files are cleanly separated by role:
- identity/persona
- working style
- hard boundaries
- task execution rules
- temporary trial rules
- business workflow rules

Flag when these are mixed together in ways that weaken the important rules.

### 4. Check alignment across files
Ask:
- Do the core live rules point in the same direction, or are they pulling behavior apart?
- Does the workspace's correction / learnings layer support or contradict the live rules?
- If the widened scope includes behavior-improvement or trial files, do those files match the live rules?
- Are older rules still pulling behavior in the wrong direction?

### 5. Judge whether the most important rule is actually prominent enough
The key audit question is not just “is the right rule written somewhere?”
It is:
- Is the right rule clear?
- Is it near the top or buried?
- Is it specific enough to change behavior?
- Is it being diluted by too many softer surrounding rules?

### 6. Recommend by role, not by habit
Do not tell the user to rewrite everything.
Recommend changes by file role:
- what should stay in `AGENTS.md`
- what should move to the workspace's correction / learnings layer
- what should move to references/review/tracking
- what should become a stronger core rule
- what should be deleted or merged

## Output structure

Use this default output shape:
1. **Audit scope** — what was checked
2. **Overall judgment** — is the behavior layer mostly aligned or not
3. **Highest-priority problems** — ranked
4. **Root cause vs symptoms** — where relevant
5. **What is already fine** — avoid over-editing
6. **Recommended changes** — concrete and file-specific

For a reusable outline, see `references/output-template.md`.

## Important judgment rules

- Do not confuse “a rule exists somewhere” with “the agent is actually being steered by it.”
- Do not recommend giant rewrites when a smaller structural cleanup would solve the issue.
- Prefer fewer, clearer, stronger rules over many overlapping weak ones.
- When the user's complaint is concrete, optimize for that real complaint first.
- If a problem is mainly workflow/process rather than prompt wording, say so plainly.

## When to widen the audit

Widen beyond the default scope only when needed, for example:
- a shared file is explicitly referenced
- the user asks for a broader workspace audit
- the core files look fine but behavior still points to another steering source
- recent behavioral evidence contains the only concrete signs of how the behavior shifted
