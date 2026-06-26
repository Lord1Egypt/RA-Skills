---
name: codex-delegate
description: Decide when to delegate a task to Codex and when to keep it in the main agent thread. Use when the work is code-heavy, repo-heavy, multi-file, environment-sensitive, or likely to consume too much context in the main session. Especially useful when acting like a project manager or tech lead: define the task, choose whether Codex should handle it, and decide what must still be validated by the main agent.
---

# Codex Delegate

Use this skill to decide **whether** Codex should be used, **what** part should be delegated, and **what must remain with the main agent**.

## Core rule

Codex is a **specialist executor**, not the long-term owner of the human relationship.
Use Codex for heavy technical work, isolated analysis, and context offloading.
Keep final judgment, risk trade-offs, environment acceptance, and user-facing conclusion in the main agent.

## When to delegate to Codex

Delegate when the task is:
- code-heavy
- repo-heavy
- multi-file
- CLI-heavy
- deep review / audit work
- likely to consume too much token/context in the main thread
- better handled in an isolated, clean context

Typical examples:
- repository analysis
- skill/package review
- deep code review
- bug investigation
- patch drafting
- dependency and config analysis
- log/error analysis

## When NOT to delegate fully

Do not fully hand off tasks that depend on:
- long-term memory
- user preference and tone alignment
- final risk judgment
- environment acceptance across shell / gateway / cron / LaunchAgent
- upgrade timing and change management
- whether a temporary workaround becomes the official solution

Codex may assist, but the main agent must still decide.

## Delegation split

### Codex should do
- static inspection
- file and repo structure analysis
- code/package consistency checks
- focused error analysis
- technical option comparison
- isolated patch or remediation proposals
- heavy token-consuming analysis that would otherwise bloat the main session

### Main agent should do
- define the real goal
- set scope and constraints
- choose whether Codex is the right tool
- evaluate user risk tolerance and workflow fit
- validate dynamic/runtime reality
- decide whether something is truly "done"
- deliver the final recommendation in the human's context

## Validation rule

Never confuse these layers:
- reviewed by Codex
- technically plausible
- works in current shell
- works in gateway
- works in cron
- accepted as the official solution

The first three can often be delegated.
The last three require main-agent ownership.

## Token discipline

Delegation is not just about capability. It is also about **saving token and protecting the main thread**.
Delegate when:
- the task would create a large technical detour
- the analysis is mostly local and mechanical
- the result can be brought back as a short conclusion

Do not delegate when the cost of coordination exceeds the saved context.

## Lightweight workflow

1. Define the task in one sentence.
2. Ask: is this mainly technical execution or human-facing judgment?
3. If mainly technical execution, delegate the heavy part to Codex.
4. Require Codex output to stay structured and narrow.
5. Bring back only the useful result.
6. Do final validation and decision in the main agent.

## Output structure

When using this skill, report with:
- conclusion
- should delegate or not
- what Codex should handle
- what the main agent must keep
- validation level required before calling it done

Keep it short. Prefer good routing over long explanation.

## Attribution

- Author: 石屹
- For: 加十
- Affiliation: 为加十工作流设计
- Note: built for 加十
