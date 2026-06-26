---
name: superclaw
description: Structured development workflow for OpenClaw agents - Brainstorm, Plan, Execute, Review. Brings systematic software development with TDD, clear specs, and subagent collaboration to ChatClaw agents.
homepage: https://chatclaw.com/skills/superclaw
metadata:
  openclaw:
    emoji: "🦞"
    requires:
      bins: ["git"]
---

# SuperClaw - Agent Development Workflow

**SuperClaw** brings systematic, professional software development to OpenClaw agents. Based on proven patterns from Superpowers, adapted for the agent community.

## Philosophy

- **Test-Driven Development** - Write tests first, always
- **Systematic over ad-hoc** - Process over guessing  
- **Complexity reduction** - Simplicity as primary goal
- **Evidence over claims** - Verify before declaring success

## Workflow Overview

SuperClaw follows a 4-phase workflow:

```
Brainstorm → Plan → Execute → Review
```

## Phase 1: Brainstorm 🧠

**When to use:** Before writing any code

**What it does:**
- Asks clarifying questions about requirements
- Explores alternative approaches
- Identifies risks and constraints
- Creates a design document in chunks

**Output:** `docs/superclaw/designs/YYYY-MM-DD-<feature>.md`

**Key Principle:** Don't jump into code. Understand the problem first.

## Phase 2: Write Plan 📝

**When to use:** After design approval

**What it does:**
- Breaks work into bite-sized tasks (2-5 minutes each)
- Maps file structure and responsibilities
- Specifies exact test criteria
- Includes verification steps

**Output:** `docs/superclaw/plans/YYYY-MM-DD-<feature>.md`

## Phase 3: Execute ⚡

**When to use:** After plan approval

**What it does:**
- Works through tasks sequentially
- Enforces RED-GREEN-REFACTOR TDD cycle
- Makes frequent commits
- Reports progress

## Phase 4: Review ✅

**When to use:** Between tasks and at completion

**What it does:**
- Reviews code against plan
- Checks for spec compliance
- Identifies code quality issues
- Blocks progress on critical issues

---

## Credits

Adapted from [Superpowers](https://github.com/obra/superpowers) by Jesse Vincent (obra). Reimagined for the OpenClaw and ChatClaw agent community.

MIT License - see LICENSE file
