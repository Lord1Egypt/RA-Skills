---
name: Engineering Discipline
slug: engineering-discipline
version: 1.0.1
description: "Production-grade AI coding discipline. Prevents the top 4 AI coding sins: acting without thinking, over-engineering, collateral damage, and vague execution. Triggers: 'engineering discipline', '过度工程', '反合理化', '三层一致性检查', 'AI coding rules', 'Karpathy 四规则', '写代码前先想', '手术刀修复'. Use when starting any coding task, before large refactors, or when catching yourself rationalizing shortcuts. Based on Karpathy's 4 rules + battle-tested additions (3-layer consistency checks, anti-rationalization, verification loops, surgical diffs). Works with Claude Code, Cursor, Copilot, OpenClaw, and any AI coding assistant. Triggers: 'engineering checklist'、'coding discipline'、'production quality'、'AI coding guardrails'、'开发纪律'。"
homepage: https://clawhub.ai/skills/engineering-discipline
metadata: {"clawdbot":{"emoji":"🔧","os":["linux","darwin","win32"]}}
---

## When to Use

Apply this skill to **every coding session**. It's not a task-specific tool — it's a permanent behavior modifier for AI coding assistants.

Especially critical when:
- Working on production codebases (>1000 lines)
- Making changes that touch multiple files or components
- The AI assistant starts "suggesting improvements" you didn't ask for
- You notice the AI making assumptions about your intent

## The 4 Foundational Rules (Karpathy)

### Rule 1: Think Before Coding

**Problem**: AI acts on assumptions, not understanding.

Before writing any code:
1. If the requirement is ambiguous → **ask**, don't guess
2. If there are multiple valid approaches → **list them** with tradeoffs
3. If the request seems wrong → **push back** with reasoning
4. If you're uncertain about scope → **confirm** before touching files

❌ Bad: "I'll refactor this module while fixing the bug"
✅ Good: "The bug is in line 42. I see the surrounding code could be cleaner, but you only asked me to fix the bug. Should I also refactor?"

### Rule 2: Simplicity First

**Problem**: AI defaults to over-abstraction.

- 10 lines > 100 lines for the same result
- No feature creep — only build what was asked
- No premature abstraction — don't add interfaces "just in case"
- Litmus test: would a senior engineer say "this is too complex"? → rewrite

❌ Bad: Adding a factory pattern, three interfaces, and a config layer for a simple utility function
✅ Good: One function, clear name, no unnecessary indirection

### Rule 3: Surgical Changes

**Problem**: AI makes "drive-by" edits to code it wasn't asked to touch.

- Fix the bug, **only** the bug
- Don't reformat adjacent code
- Don't update comments you weren't asked about
- Don't change variable names in unrelated functions
- Every changed line must trace back to the user's specific request

❌ Bad: "While fixing the auth bug, I also cleaned up the logging format and renamed some variables"
✅ Good: 3 lines changed, all in the auth function, all directly related to the bug

### Rule 4: Goal-Driven Execution

**Problem**: Vague instructions lead to vague results.

Instead of telling the AI **how** to do something, give it a **success criterion**:

❌ "Fix the login bug"
✅ "Write a test that reproduces the login timeout on slow networks, then make it pass"

❌ "Improve the API"
✅ "Response time for /api/users must be under 200ms for 1000 concurrent requests"

The AI iterates better toward measurable goals than fuzzy directions.

> 💡 **Why This Way**: LLMs are natural iterators. Given a clear target, they'll loop (generate → test → adjust) until they hit it. Given a vague goal, they'll generate once, declare victory, and move on.

## Battle-Tested Additions (Beyond Karpathy)

### A1: Three-Layer Consistency Check

After any change, verify alignment across layers:

**Layer 1 — Naming**: env vars, DB columns, API paths, config keys must match across all files
**Layer 2 — Business**: design docs ↔ code ↔ UI ↔ API responses must tell the same story
**Layer 3 — Database**: migrations ordered correctly, FK references valid, types match TS interfaces

Run the relevant layer after each change. Run all three on major releases.

### A2: Anti-Rationalization

Never trust the AI's "I think this looks correct." 

- "I read the code" ≠ verified → **run it**
- "It should work" ≠ confirmed → **test it**
- "I wrote it, so it's right" = rationalization → **verify independently**

### A3: Verification Loop

For every change type, define a verification action:

| Changed | Verify by |
|---|---|
| Code/script | Execute it |
| Config | Restart + confirm effect |
| Generated file | Check content (wc -l, grep, diff) |
| API call | Check return value |
| UI change | Visual diff before/after |

### A4: Pre-Change Snapshot

Before modifying any file:
1. Record current state (grep key content, or screenshot)
2. Make the change
3. Diff to confirm only intended parts changed
4. If unintended changes found → revert and redo surgically

### A5: Context Hygiene

AI context windows are finite. Polluted context → degraded output.

- Trim tool outputs (pipe to `head -30`, don't dump 500 lines)
- Checkpoint progress to files during long tasks
- Don't let the AI "remember" — make it **read files**

## Integration

### Claude Code (CLAUDE.md)
Add to your project's `CLAUDE.md`:
```
# Engineering Discipline Rules
[paste the 4 rules + additions above]
```

### Cursor (.cursor/rules)
Add to `.cursor/rules/engineering-discipline.md`

### Any AI Coding Tool
These rules work as system prompts, project instructions, or conversation primers for any LLM-based coding assistant.

## Related Skills
- `trinity-harness` — Full agent harness with Challenge + Execute + Compound layers
- `self-improving-agent` — Continuous learning from mistakes
- `skill-creator` — Create new skills from workflows

## Feedback
- If useful: `clawhub star engineering-discipline`
- Issues: https://github.com/clawhub/engineering-discipline
